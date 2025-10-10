#!/usr/bin/env python3
"""
Utility to extract structurally dissimilar examples by computing Jaccard similarity
directly from the unified analysis JSON (and optionally from a pre-computed matrix).

When sourcing data from JSON, each image is represented by the set of leaf attributes
assigned to it (recursing through nested dictionaries/lists) plus the image identifier
itself. The script can either:

* emit every image pair whose similarity falls below a chosen threshold (default mode), or
* greedily select a deduplicated list of images such that no remaining pair has
  similarity above the threshold (``--unique`` mode).
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableSet, Sequence, Tuple


Pair = Tuple[str, str, float]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Select image pairs whose Jaccard similarity falls below a threshold.",
    )
    parser.add_argument(
        "--analysis-json",
        type=Path,
        help="Path to unifiedAnalysis.json (primary data source).",
    )
    parser.add_argument(
        "--matrix",
        type=Path,
        help="Fallback path to a CSV Jaccard similarity matrix (e.g. imageJaccardSimilaritymatrix.csv).",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        help="Maximum similarity score to keep (pairs with similarity strictly below this value are selected).",
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Destination file to write the selected image pairs (CSV with image_a,image_b,similarity).",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=0,
        help="Optional cap on the number of lowest-similarity pairs to emit (0 keeps all qualifying pairs).",
    )
    parser.add_argument(
        "--require-extension",
        action="store_true",
        help="Drop any images that do not already end in .jpg or .png. By default filenames are left untouched.",
    )
    parser.add_argument(
        "--unique",
        action="store_true",
        help="Write a single-column CSV of unique image names instead of pair-wise entries.",
    )
    return parser.parse_args()


def validate_source(args: argparse.Namespace) -> None:
    if args.analysis_json and args.matrix:
        raise ValueError("Specify only one of --analysis-json or --matrix.")
    if not args.analysis_json and not args.matrix:
        raise ValueError("Provide --analysis-json (preferred) or --matrix as input.")
    if args.threshold is None:
        raise ValueError("--threshold is required.")
    if args.unique and not args.analysis_json:
        raise ValueError("--unique mode currently requires --analysis-json input.")


def load_header(reader: Iterable[List[str]]) -> Tuple[List[str], Dict[str, int]]:
    try:
        header = next(reader)
    except StopIteration as exc:  # pragma: no cover - defensive guard
        raise ValueError("Matrix CSV is empty.") from exc

    if not header:
        raise ValueError("Matrix CSV header row is empty.")

    column_names = [name.strip() for name in header[1:]]
    index_map = {name: idx for idx, name in enumerate(column_names)}
    return column_names, index_map


def gather_pairs(
    reader: Iterable[List[str]],
    column_names: List[str],
    index_map: Dict[str, int],
    threshold: float,
) -> List[Pair]:
    selected: List[Pair] = []
    for row in reader:
        if not row:
            continue

        row_image = row[0].strip()
        if not row_image:
            continue

        row_index = index_map.get(row_image)
        if row_index is None:
            # The row might belong to a filtered matrix whose header omitted this image.
            # Skip gracefully so the script can be re-used across slightly different dumps.
            continue

        for col_index, col_image in enumerate(column_names):
            if col_index <= row_index:
                continue  # avoid duplicate pairs and the diagonal

            raw_value = row[col_index + 1] if col_index + 1 < len(row) else ""
            try:
                similarity = float(raw_value)
            except (TypeError, ValueError):
                continue  # missing or non-numeric value

            if similarity < threshold:
                selected.append((row_image, col_image, similarity))

    return selected


def _add_token(value, tokens: MutableSet[str]) -> None:
    if value is None:
        return
    tokens.add(str(value))


def _collect_tokens(value, tokens: MutableSet[str]) -> None:
    if isinstance(value, Mapping):
        for item in value.values():
            _collect_tokens(item, tokens)
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        for item in value:
            _collect_tokens(item, tokens)
    else:
        _add_token(value, tokens)


def load_image_feature_sets(json_path: Path, require_extension: bool) -> Dict[str, MutableSet[str]]:
    with json_path.open() as f:
        data = json.load(f)

    features: Dict[str, MutableSet[str]] = {}

    for entries in data.values():
        for entry in entries:
            image_id = entry.get("id")
            if not image_id:
                continue

            if require_extension and not image_id.lower().endswith((".jpg", ".png")):
                continue

            tokens: MutableSet[str] = set()
            tokens.add(image_id)
            value = entry.get("value", {})
            _collect_tokens(value, tokens)
            features[image_id] = tokens

    return features


def jaccard_similarity(tokens_a: MutableSet[str], tokens_b: MutableSet[str]) -> float:
    union = tokens_a | tokens_b
    if not union:
        return 0.0
    intersection = tokens_a & tokens_b
    return len(intersection) / len(union)


def gather_pairs_from_features(
    features: Dict[str, MutableSet[str]],
    threshold: float,
) -> List[Pair]:
    image_ids = sorted(features)
    selected: List[Pair] = []
    for idx, image_a in enumerate(image_ids):
        tokens_a = features[image_a]
        for image_b in image_ids[idx + 1 :]:
            tokens_b = features[image_b]
            similarity = jaccard_similarity(tokens_a, tokens_b)
            if similarity < threshold:
                selected.append((image_a, image_b, similarity))
    return selected


def write_pairs(pairs: List[Pair], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["image_a", "image_b", "similarity"])
        for image_a, image_b, similarity in pairs:
            writer.writerow([image_a, image_b, f"{similarity:.6f}"])


def write_unique_images(image_names: Iterable[str], destination: Path) -> None:
    sorted_names = sorted(image_names)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["image"])
        for image_name in sorted_names:
            writer.writerow([image_name])


def select_unique_images(
    features: Dict[str, MutableSet[str]],
    threshold: float,
) -> Tuple[List[str], List[Pair]]:
    selected: List[str] = []
    collisions: List[Pair] = []

    for image_id in sorted(features):
        tokens = features[image_id]
        keep = True
        for kept_id in selected:
            similarity = jaccard_similarity(tokens, features[kept_id])
            if similarity >= threshold:
                collisions.append((kept_id, image_id, similarity))
                keep = False
                break
        if keep:
            selected.append(image_id)

    return selected, collisions


def main() -> None:
    args = parse_args()
    validate_source(args)

    features = None
    if args.analysis_json:
        features = load_image_feature_sets(args.analysis_json, args.require_extension)

    if args.unique:
        assert features is not None  # validated earlier
        selected_images, collisions = select_unique_images(features, args.threshold)
        write_unique_images(selected_images, args.output)
        source_display = args.analysis_json
        print(
            f"Selected {len(selected_images)} images (removed {len(collisions)}) "
            f"with threshold {args.threshold} from {source_display} -> {args.output}"
        )
        return

    if args.analysis_json:
        pairs = gather_pairs_from_features(features, args.threshold)
    else:
        with args.matrix.open(newline="") as f:
            reader = csv.reader(f)
            column_names, index_map = load_header(reader)
            pairs = gather_pairs(reader, column_names, index_map, args.threshold)

    if args.top_k and args.top_k > 0:
        pairs.sort(key=lambda item: item[2])
        pairs = pairs[: args.top_k]
    else:
        pairs.sort(key=lambda item: item[2])

    write_pairs(pairs, args.output)

    source_display = args.analysis_json if args.analysis_json else args.matrix
    print(
        f"Selected {len(pairs)} pairs below threshold {args.threshold} "
        f"from {source_display} -> {args.output}"
    )


if __name__ == "__main__":
    main()
