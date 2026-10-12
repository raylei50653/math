# Replay and certificate custody

The authoritative result is `certificate.v2.json`, documented by
`../REPORT.md`. `certificate.json` is the superseded first generation, retained
only for provenance: its candidate scoring violates two preregistered details.
The current checker intentionally rejects that first generation.

From the repository root, with Python and NetworkX **3.5**:

```sh
.venv/bin/python -B audits/2026-10-12-degree5-star-b-6ef2c06c/controls/check.py --check audits/2026-10-12-degree5-star-b-6ef2c06c/controls/certificate.v2.json
PYTHONHASHSEED=17 .venv/bin/python -B audits/2026-10-12-degree5-star-b-6ef2c06c/controls/check.py --seed 17 --check audits/2026-10-12-degree5-star-b-6ef2c06c/controls/certificate.v2.json
```

The complete replay validates frozen BASE inputs and design hashes, reconstructs
the chosen source rotations and every candidate operation, independently checks
candidate completeness and literal transformations, and compares product/MRV
full-coloring lists. Geometry checks include the explicit inherited rotations,
oriented outer boundary, face walks, Euler characteristic, apex planarity, and
augmented chord graphs used for quotient surgery.

`topology.py` never computes colorings. `independent.py` imports neither the
topology producer nor the inherited catalogue checker. `check.py` preserves all
ten rows and full lifts, including the empty interface fibres through the
documented lossless default-empty encoding.

`validate.py --tag NEW_TAG` reruns the normal, seed-17/from-other-cwd, inherited,
and corrupted-certificate checks, writing exclusively named logs and
`../VALIDATION.NEW_TAG.json`. Choose a new tag each time; old results are not
overwritten. Malformed test files are temporary local copies; exact mutation
recipes and SHA-256 digests are retained. The completed final run is
`../VALIDATION.final.json`.

No command above edits shared repository files or original upstream evidence.
`--write controls/NEW_NAME.json` must receive an absent target inside this
exclusive controls directory. Full certificate generation/replay assumes the
fixed NetworkX version because embedding choice precedes coloring evaluation.

The finite controls supply no globally minimal outside-K source and no general
reducibility or Lean theorem.
