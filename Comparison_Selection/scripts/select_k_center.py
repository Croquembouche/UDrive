#!/usr/bin/env python3
"""
Greedy k-center / farthest-point image selector operating on cached CLIP embeddings.

Example usage:

    python Selection/select_k_center.py \
        --features Selection/features/ArgoVerse1/features.npy \
        --index Selection/features/ArgoVerse1/index.json \
        --budget 78 \
        --output Selection/Argoverse1/k_center_top78.csv \
        --metric cosine

The script assumes embeddings are already L2-normalised (as produced by
``extract_clip_features.py``). It emits a CSV listing each chosen image and the
distance to its closest already-selected neighbour at the time of selection.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import List, Sequence, Tuple

import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Select a k-center subset from cached feature embeddings.",
    )
    parser.add_argument(
        "--features",
        required=True,
        type=Path,
        help="Path to the NumPy feature matrix (features.npy).",
    )
    parser.add_argument(
        "--index",
        required=True,
        type=Path,
        help="Path to the metadata JSON produced alongside the features.",
    )
    parser.add_argument(
        "--budget",
        required=True,
        type=int,
        help="Number of images to select.",
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Destination CSV for the selected image names.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=13,
        help="Random seed used when choosing the initial point (default: 13).",
    )
    parser.add_argument(
        "--metric",
        choices=("cosine",),
        default="cosine",
        help="Distance metric (currently only cosine distance is supported).",
    )
    parser.add_argument(
        "--start-index",
        type=int,
        default=-1,
        help="Optional explicit first index to seed the selection (overrides RNG).",
    )
    return parser.parse_args()


def load_data(features_path: Path, index_path: Path) -> Tuple[np.ndarray, List[str]]:
    features = np.load(features_path)
    with index_path.open() as f:
        meta = json.load(f)
    image_ids = meta.get("image_ids")
    if image_ids is None:
        raise ValueError("index.json is missing the 'image_ids' list.")
    if len(image_ids) != features.shape[0]:
        raise ValueError(
            f"Mismatch between features ({features.shape[0]}) and image_ids ({len(image_ids)})."
        )
    return features, image_ids


def initialise_selection(
    num_items: int,
    start_index: int,
    rng: np.random.Generator,
) -> int:
    if start_index >= 0:
        if start_index >= num_items:
            raise ValueError(f"start_index ({start_index}) exceeds number of items ({num_items}).")
        return start_index
    return int(rng.integers(0, num_items))


def greedy_k_center(
    features: np.ndarray,
    budget: int,
    start_index: int,
    rng: np.random.Generator,
) -> Tuple[List[int], List[float]]:
    num_items = features.shape[0]
    if budget <= 0:
        raise ValueError("Budget must be positive.")
    if budget > num_items:
        budget = num_items

    selected_indices: List[int] = []
    selection_distances: List[float] = []

    first = initialise_selection(num_items, start_index, rng)
    selected_indices.append(first)
    selection_distances.append(0.0)

    # Initialise distance-to-selected array with distances to the first point.
    # Cosine distance = 1 - cosine similarity (assuming normalised vectors).
    similarities = features @ features[first]
    min_distances = 1.0 - similarities
    min_distances[first] = -np.inf  # exclude already selected

    while len(selected_indices) < budget:
        next_index = int(np.argmax(min_distances))
        next_distance = float(min_distances[next_index])

        if not np.isfinite(next_distance) or next_distance <= 0:
            # Remaining points are identical (or extremely close) to selected ones.
            break

        selected_indices.append(next_index)
        selection_distances.append(next_distance)

        # Update distances.
        new_similarities = features @ features[next_index]
        new_distances = 1.0 - new_similarities
        min_distances = np.minimum(min_distances, new_distances)
        min_distances[next_index] = -np.inf

    return selected_indices, selection_distances


def write_output(
    output_path: Path,
    image_ids: Sequence[str],
    indices: Sequence[int],
    distances: Sequence[float],
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "image", "min_distance"])
        for rank, (idx, dist) in enumerate(zip(indices, distances), start=1):
            writer.writerow([rank, image_ids[idx], f"{dist:.6f}"])


def main() -> None:
    args = parse_args()
    features, image_ids = load_data(args.features, args.index)

    rng = np.random.default_rng(args.seed)
    selected_indices, distances = greedy_k_center(
        features, args.budget, args.start_index, rng
    )

    write_output(args.output, image_ids, selected_indices, distances)

    print(
        f"Selected {len(selected_indices)} images "
        f"-> {args.output} (seed={args.seed}, start_index={args.start_index})"
    )


if __name__ == "__main__":
    main()
