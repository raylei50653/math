# Experiment artifact custody

1. The agent created and checked v1 `check.py` and `certificate.json`.
   The successful certificate size was 78,897 bytes.
2. The agent found the explicit second-step boundary readout and announced an
   intention to add it. Before the parent's preserve-v1 message arrived, the
   agent added one helper and one result field to the checker, removed its
   just-generated certificate, and generated and checked transient v2.
   That certificate was 79,929 bytes.
3. The parent requested preservation of v1. The agent reversed exactly that
   helper/result-field patch and restored the canonical JSON by removing the
   extra field and recomputing the restored checker's embedded SHA. The
   restored v1 `--check` passed and its size returned to 78,897 bytes.
4. A further parent instruction to archive v2 before restoration arrived
   after restoration had completed. Therefore no pre-restoration byte copy
   of v2 was captured. The agent reconstructed the transient v2 code from
   the recorded reversible patch and its certificate from v1 plus the
   recorded second-step field, under separately and exclusively created
   `*.transient-v2-reconstructed.*` paths. These are explicitly
   **reconstructions**, not captured frozen v2 evidence.

No frozen input, source graph, or root-level file was changed. The original
v1 filenames are the stable evidence. This custody note records the incident
instead of silently treating the transient update as absent.

| File | Bytes | SHA-256 |
|---|---:|---|
| `check.py` | 12,857 | `49be4422650b9553cc598455f6e4db5534e042bce921eddb320a71560d969d75` |
| `certificate.json` | 78,897 | `38620e54bf88dccfb50d8e72b65fce7139359cb0533c1b2b628e831f7b7ec4f3` |
| `check.transient-v2-reconstructed.py` | 13,597 | `fb54c7b8e66857224ea5e939da3b333191c7949b75544c662b0b5177f324250c` |
| `certificate.transient-v2-reconstructed.json` | 79,929 | `a2993ad7396169088100fe32d2c65e715602f33d4ff87ea32f033ba9e002af95` |

The stable v1 certificate's embedded checker SHA equals the restored v1
checker SHA above. Restoring the literal old patch and canonical encoding is
reproducible; no independent pre-edit checksum of the transient v2 was
captured. The reconstructed v2 checker retains its original filename-relative
output logic and is not a separately configured runnable checker. Use only
`check.py --check` for the stable certificate.

The parent did not capture an independent pre-edit checksum of original v1
either. Consequently byte identity to that earlier v1 is based on reversing
the recorded patch and recovering the earlier size, not an independently
saved pre-edit hash. Current checker/certificate consistency and all reported
mathematical results are separately established by fresh deterministic replay
and the independent review. Frozen authority inputs retain their original hashes.
