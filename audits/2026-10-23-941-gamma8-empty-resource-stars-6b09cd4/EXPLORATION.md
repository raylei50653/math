# Retained preliminary controls

`explore.py`, `explore-partial.py`, `explore-*.json`, and `partial-*.json` are retained bounded exploration using the previous checker. They are not the independent verification authority. The final `check.py` imports no prior checker, independently reconstructs original-edge/full-star constraints, and is replayed in `runs/normal-final.json`, `runs/seed17-final.json`, and `runs/negative-v2.json`.

`runs/normal.json` predates the explicit routing snapshots and certificate-scope sidecar; `normal-final.json` is the final normal receipt. The generation failure record retains a missing-filename attempt; no certificate was overwritten.
