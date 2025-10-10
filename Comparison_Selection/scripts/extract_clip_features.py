#!/usr/bin/env python3
"""
Extract CLIP image embeddings for UDrive datasets with GPU-friendly batching.

Typical usage (ArgoVerse1 example):

    python Selection/extract_clip_features.py \
        --dataset ArgoVerse1 \
        --analysis-json Analysis/ArgoVerse1/unifiedAnalysis.json \
        --image-root Analysis/ArgoVerse1/combined \
        --output-dir Selection/features/ArgoVerse1 \
        --batch-size 32 \
        --precision fp16

Notes:
    * Requires `torch` and `open_clip_torch` (install via `pip install open_clip_torch`).
    * Processes each listed image exactly once; missing files are reported and skipped.
    * Outputs:
        - `features.npy` (NumPy array of shape [N, D], float16/float32)
        - `index.json`   (metadata with dataset, model, image ids, source paths)
        - `missing.txt`  (optional, only if some inputs could not be resolved)
"""

from __future__ import annotations

import argparse
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
import torch
from PIL import Image, UnidentifiedImageError
from torch.utils.data import DataLoader, Dataset

LOGGER = logging.getLogger("extract_clip_features")


@dataclass
class ImageRecord:
    idx: int
    image_id: str
    path: Path


class ImageDataset(Dataset):
    """Thin dataset wrapper around pre-resolved image paths."""

    def __init__(self, records: Sequence[ImageRecord], preprocess) -> None:
        self.records = records
        self.preprocess = preprocess

    def __len__(self) -> int:
        return len(self.records)

    def __getitem__(self, index: int) -> Tuple[torch.Tensor, int]:
        record = self.records[index]
        try:
            image = Image.open(record.path).convert("RGB")
        except (FileNotFoundError, UnidentifiedImageError) as exc:
            raise RuntimeError(f"Failed to load image: {record.path}") from exc
        tensor = self.preprocess(image)
        return tensor, index


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract CLIP embeddings for dataset images listed in unifiedAnalysis.json.",
    )
    parser.add_argument("--dataset", required=True, help="Dataset name (for logging/metadata).")
    parser.add_argument(
        "--analysis-json",
        required=True,
        type=Path,
        help="Path to unifiedAnalysis.json enumerating images.",
    )
    parser.add_argument(
        "--image-root",
        required=True,
        type=Path,
        help="Directory containing the raw image files.",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory where feature files will be written.",
    )
    parser.add_argument(
        "--model-name",
        default="ViT-B-32",
        help="CLIP variant to load via open_clip (default: ViT-B-32).",
    )
    parser.add_argument(
        "--pretrained",
        default="openai",
        help="Pretrained weights identifier for open_clip (default: openai).",
    )
    parser.add_argument(
        "--precision",
        choices=("fp32", "fp16"),
        default="fp16",
        help="Computation/output precision (fp16 recommended for RTX 3080).",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=32,
        help="Images per GPU batch; adjust based on VRAM (default: 32).",
    )
    parser.add_argument(
        "--num-workers",
        type=int,
        default=4,
        help="DataLoader workers (set 0 on Windows or when hitting PIL thread issues).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Optional cap on number of images to process (useful for dry-runs).",
    )
    parser.add_argument(
        "--start-index",
        type=int,
        default=0,
        help="Skip the first N images (basic resume support when running in chunks).",
    )
    parser.add_argument(
        "--scan-root",
        action="store_true",
        help="Pre-scan the image root to build a filename->path map (handles nested layouts).",
    )
    parser.add_argument(
        "--write-missing",
        action="store_true",
        help="Emit missing image names into missing.txt inside the output directory.",
    )
    parser.add_argument(
        "--log-interval",
        type=int,
        default=50,
        help="Log every N batches to show progress (default: 50).",
    )
    parser.add_argument(
        "--device",
        default="cuda" if torch.cuda.is_available() else "cpu",
        help="Computation device (default: auto-detect CUDA).",
    )
    parser.add_argument(
        "--allow-missing",
        action="store_true",
        help="Continue even if some images are missing (they are skipped).",
    )
    return parser.parse_args()


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s %(name)s: %(message)s",
    )


def load_analysis_image_ids(json_path: Path) -> List[str]:
    with json_path.open() as f:
        payload = json.load(f)

    image_ids: List[str] = []
    for entries in payload.values():
        for entry in entries:
            image_id = entry.get("id") or entry.get("image_id")
            if image_id:
                image_ids.append(image_id)
    unique_ids = list(dict.fromkeys(image_ids))  # preserve order, drop duplicates
    LOGGER.info("Loaded %d unique image ids from %s", len(unique_ids), json_path)
    return unique_ids


def build_filename_index(image_root: Path) -> Dict[str, Path]:
    LOGGER.info("Scanning %s for image files...", image_root)
    mapping: Dict[str, Path] = {}
    for path in image_root.rglob("*"):
        if path.is_dir():
            continue
        mapping.setdefault(path.name, path)
    LOGGER.info("Indexed %d files under %s", len(mapping), image_root)
    return mapping


def resolve_image_paths(
    image_ids: Iterable[str],
    image_root: Path,
    scan_map: Optional[Dict[str, Path]],
) -> Tuple[List[ImageRecord], List[str]]:
    records: List[ImageRecord] = []
    missing: List[str] = []

    for idx, image_id in enumerate(image_ids):
        candidate = image_root / image_id
        if candidate.exists():
            records.append(ImageRecord(idx=idx, image_id=image_id, path=candidate))
            continue

        if scan_map:
            mapped = scan_map.get(image_id)
            if mapped and mapped.exists():
                records.append(ImageRecord(idx=idx, image_id=image_id, path=mapped))
                continue

        missing.append(image_id)

    return records, missing


def trim_records(
    records: Sequence[ImageRecord],
    start_index: int,
    limit: int,
) -> List[ImageRecord]:
    if start_index >= len(records):
        return []
    sliced = records[start_index:]
    if limit and limit > 0:
        sliced = sliced[:limit]

    # Re-index sequentially for downstream DataLoader logic
    trimmed: List[ImageRecord] = []
    for new_idx, record in enumerate(sliced):
        trimmed.append(ImageRecord(idx=new_idx, image_id=record.image_id, path=record.path))
    return trimmed


def ensure_output_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def save_metadata(
    output_dir: Path,
    dataset: str,
    model_name: str,
    pretrained: str,
    precision: str,
    image_records: Sequence[ImageRecord],
    source_json: Path,
    image_root: Path,
    args: argparse.Namespace,
) -> None:
    meta = {
        "dataset": dataset,
        "model_name": model_name,
        "pretrained": pretrained,
        "precision": precision,
        "num_images": len(image_records),
        "analysis_json": str(source_json),
        "image_root": str(image_root),
        "image_ids": [record.image_id for record in image_records],
        "image_paths": [str(record.path) for record in image_records],
        "arguments": {
            "batch_size": args.batch_size,
            "num_workers": args.num_workers,
            "limit": args.limit,
            "start_index": args.start_index,
            "scan_root": args.scan_root,
            "allow_missing": args.allow_missing,
        },
    }

    index_path = output_dir / "index.json"
    with index_path.open("w") as f:
        json.dump(meta, f, indent=2)
    LOGGER.info("Wrote metadata to %s", index_path)


def write_missing_list(output_dir: Path, missing: Sequence[str]) -> None:
    if not missing:
        return
    missing_path = output_dir / "missing.txt"
    with missing_path.open("w") as f:
        for item in missing:
            f.write(f"{item}\n")
    LOGGER.warning("Logged %d missing images to %s", len(missing), missing_path)


def main() -> None:
    setup_logging()
    args = parse_args()

    device = torch.device(args.device)
    LOGGER.info(
        "Using device %s (cuda available: %s)", device, torch.cuda.is_available()
    )

    image_ids = load_analysis_image_ids(args.analysis_json)

    scan_map = build_filename_index(args.image_root) if args.scan_root else None

    records, missing = resolve_image_paths(image_ids, args.image_root, scan_map)
    if missing:
        message = f"{len(missing)} images could not be resolved under {args.image_root}"
        if not args.allow_missing:
            LOGGER.error(message)
            raise SystemExit("Abort: missing images encountered (use --allow-missing to skip).")
        LOGGER.warning("%s (they will be skipped).", message)

    filtered_records = trim_records(records, args.start_index, args.limit)
    if not filtered_records:
        LOGGER.error("No images to process after applying start_index/limit filters.")
        raise SystemExit(1)

    ensure_output_dir(args.output_dir)
    if args.write_missing and missing:
        write_missing_list(args.output_dir, missing)

    try:
        import open_clip  # type: ignore
    except ImportError as exc:  # pragma: no cover - dependency guard
        LOGGER.error("open_clip_torch is required. Install with `pip install open_clip_torch`.")
        raise SystemExit(1) from exc

    LOGGER.info("Preparing CLIP model %s (%s)", args.model_name, args.pretrained)
    model, _, preprocess = open_clip.create_model_and_transforms(
        args.model_name, pretrained=args.pretrained, device=device
    )
    model.eval()

    autocast_enabled = args.precision == "fp16"
    dtype = np.float16 if args.precision == "fp16" else np.float32

    dataset = ImageDataset(filtered_records, preprocess)
    loader = DataLoader(
        dataset,
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        pin_memory=device.type == "cuda",
        shuffle=False,
    )

    feature_store: Optional[np.ndarray] = None
    feature_dim: Optional[int] = None
    total = len(filtered_records)
    processed = 0

    with torch.no_grad():
        for step, (images, indices) in enumerate(loader):
            images = images.to(device, non_blocking=True)
            with torch.cuda.amp.autocast(enabled=autocast_enabled):
                embeddings = model.encode_image(images)
            embeddings = embeddings.float()
            embeddings = embeddings / embeddings.norm(dim=-1, keepdim=True)
            embeddings_cpu = embeddings.cpu().numpy().astype(dtype)

            if feature_store is None:
                feature_dim = embeddings_cpu.shape[1]
                feature_store = np.zeros((total, feature_dim), dtype=dtype)
                LOGGER.info("Allocating feature buffer of shape (%d, %d)", total, feature_dim)

            feature_store[indices.numpy()] = embeddings_cpu
            processed += embeddings_cpu.shape[0]

            if (step + 1) % args.log_interval == 0 or processed == total:
                LOGGER.info("Processed %d/%d images", processed, total)

            if device.type == "cuda":
                torch.cuda.empty_cache()

    if feature_store is None or feature_dim is None:
        LOGGER.error("No embeddings were generated; exiting.")
        raise SystemExit(1)

    feature_path = args.output_dir / "features.npy"
    np.save(feature_path, feature_store)
    LOGGER.info("Saved embeddings to %s", feature_path)

    save_metadata(
        args.output_dir,
        dataset=args.dataset,
        model_name=args.model_name,
        pretrained=args.pretrained,
        precision=args.precision,
        image_records=filtered_records,
        source_json=args.analysis_json,
        image_root=args.image_root,
        args=args,
    )

    if args.write_missing and missing:
        write_missing_list(args.output_dir, missing)

    LOGGER.info(
        "Completed feature extraction for %d images (skipped %d missing).",
        total,
        len(missing),
    )


if __name__ == "__main__":
    main()
