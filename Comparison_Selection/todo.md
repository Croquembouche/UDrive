# Follow-up Data Selection TODO

- [ ] Confirm the Jaccard similarity structure inside each `Analysis/<Dataset>/unifiedAnalysis.json` by loading one file, logging the full key hierarchy, and noting the exact field names that hold image IDs, similarity scores, and optional metadata.
- [ ] Decide the shared interface for the selector (threshold input, output format, location under `Comparison_Selection/`) by drafting a short RFC that lists CLI arguments, default thresholds, expected output filenames, and how errors are reported.
- [ ] Sketch shared helpers to read the unified analysis payloads and normalise image-pair identifiers by prototyping a Python module that loads JSON, lowercases extensions, deduplicates pairs, and exposes a reusable iterator.
- [ ] Draft a verification checklist—quick statistical summary, spot-check a few pairs, confirm path casing—so each dataset-specific selector has an explicit validation procedure before being marked done.

## Dataset scripts

The goal for every dataset is a script that filters all image pairs with Jaccard similarity below a configurable threshold and writes a compact report that is easy to feed into deeper review.

- [ ] **ArgoVerse1** — implement a script that loads `Analysis/ArgoVerse1/unifiedAnalysis.json` (mind the camelCase naming), filters any pair whose Jaccard similarity falls below the threshold, sorts results by ascending similarity, and emits a plain-text list with `.jpg` / `.png` suffixes under `Comparison_Selection/Argoverse1/low_similarity_pairs.txt`.
- [ ] **Cityscapes** — replicate the selector for `Analysis/Cityscapes/unifiedAnalysis.json`, verify that every output path resolves relative to `Analysis/Cityscapes/image_subgraph/`, and persist results with explicit `.png` endings so downstream tooling recognises them.
- [ ] **Kitti** — adapt the selector for `Analysis/Kitti/unifiedAnalysis.json`, handle images that may be stored without extensions by appending `.png` or `.jpg` as needed, and save the curated list to `Comparison_Selection/KITTI/low_similarity_pairs.txt`.
- [ ] **nuScenes** — implement parsing for `Analysis/nuScenes/unifiedAnalysis.json`, carry forward scenario or sample identifiers for traceability, and output the filtered `.jpg` / `.png` pairs to `Comparison_Selection/nuScenes/low_similarity_pairs.txt`.

## Integration and polish

- [ ] Decide where to expose the threshold by drafting CLI help text, adding environment variable overrides, and demonstrating usage in a short README snippet.
- [ ] Add lightweight logging or console summaries that print dataset name, threshold, total pairs scanned, and count selected, ensuring the log format can be grepped during experiments.
- [ ] Ensure each selector documents where the corresponding raw images/labels live by adding module-level constants or config stubs that point to the image and label roots for the planned retrieval script.
- [ ] Optionally bundle a BATched runner that executes all selectors with the same threshold, collects outputs into `Comparison_Selection/UDrive/combined_pairs.csv`, and prints a per-dataset tally.
- [ ] Update repository docs—likely `README.md` or dataset-specific notes—with a section that explains how to run the selectors, interpret their output, and hook them into the retrieval pipeline.

## Baseline comparisons

- [ ] Define the embedding space for traditional selectors—CLIP ViT-B/32 embeddings or dataset-specific backbone features—by scripting a batch extractor that caches vectors on disk so repeated runs are feasible on a single RTX 3080.
- [ ] Implement or integrate k-center, farthest-point, and entropy-based filters (Faiss-based k-center, simple farthest-first traversal, softmax entropy from a lightweight classifier) so they process the cached embeddings and emit `.jpg` / `.png` pair lists compatible with the structural selector outputs.
- [ ] Run each baseline on every dataset with matched selection budgets (e.g., same number of pairs as the Jaccard method), log GPU memory consumption, and save the results next to the structural picks for direct comparison.
- [ ] Collect evaluation signals by computing structural overlap statistics, embedding-space coverage metrics (mean pairwise distances, cluster coverage), and qualitative notes from spot-checking samples; store these in a shared CSV or notebook.
- [ ] Summarise findings in a short report—tables of metrics, runtime/GPU usage notes, and narrative observations—that highlights where the structural approach diverges from embedding or uncertainty baselines and discusses feasibility on the available hardware.
