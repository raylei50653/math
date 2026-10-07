# M3 C44 / C44′ fresh-checkout replay

Candidate: `ba0b447f09617591d9f2ba81c988f537af771791`

Checkout: `/tmp/math-m3-ba0b447`

Interpreter: `/home/ray/developer/ai/math/.venv/bin/python`

Overall result: **FAIL** — 10 / 11 required checks passed. All named checks were executed. Every command has its actual exit code, argv, environment overrides and stdout/stderr digests in [c44-summary.json](c44-summary.json) and the individual command records.

| Check | Result | Exit | Seconds |
| --- | --- | ---: | ---: |
| c44-input-audit | FAIL | 1 | 2.445 |
| c44-small | PASS | 0 | 9.468 |
| c44-full-default | PASS | 0 | 12.679 |
| c44-full-seed17 | PASS | 0 | 11.487 |
| c44-algorithm-audit | PASS | 0 | 0.707 |
| c44p-screen-default | PASS | 0 | 0.939 |
| c44p-two-private-default | PASS | 0 | 0.728 |
| c44p-independent-default | PASS | 0 | 2.713 |
| c44p-screen-seed17 | PASS | 0 | 0.864 |
| c44p-two-private-seed17 | PASS | 0 | 0.695 |
| c44p-independent-seed17 | PASS | 0 | 2.579 |

## Finding M3-C44-INPUT-AUDIT-001

[C44 input audit](commands/c44-input-audit.json) failed with `AssertionError: input audit byte mismatch`; its [original stderr](logs/c44-input-audit.stderr.log) remains intact.

The [read-only normalized diagnostic](logs/c44-input-audit-diagnostic-normalized.stdout.log) found exactly two serialized differences, both in `layers[6]` (NA, k=9):

- `es_source_present`: saved `false`, recomputed `true`.
- `es_source_hash_matches`: saved `null`, recomputed `true`.

The restored source is `artifacts/c5_excess_two_finite_search/NA_k9_validate.json`; its expected and actual SHA256 agree at `0b08675df72ecd21415d8fb54df567fc2daa7b802df9bc22c97f4cd6f89dc9bb`. The remaining serialized fields are equal.

Saved ledger SHA256: `7d4a8de877e0d3618661cbf3ffe28b4dd1b778cfcaae03d393e278a765287adb` (106167 bytes). Recomputed ledger SHA256: `68ef7bb2e52230ea7aa620650dc30fd961dde3c0fb0e859d0c3eb69a03b1d207` (106166 bytes). This is saved presence/hash-check metadata drift following archive restoration; it is not a new mathematical counterexample. No saved ledger or candidate source was repaired. The earlier unnormalized diagnostic also reported equal D5 arrays as Python tuple/list type differences; the normalized diagnostic compares serialized JSON and removes that diagnostic artifact.

## Passed finite scope

C44 small reran its independent brute gate: k≤5 gives 32 q-orbits / 36 rejection rows, and k=6 gives 81 q-orbits / 85 rows, with complete row-core lists equal. Ordinary and seed17 full replays both passed for 9644 NA/AD/D6 q-orbits through k=9 and checked 104507 core edge-deletion witnesses. The algorithm audit passed for 60 graphs / 600 Cartesian peel rows.

C44′ screen, two-private classification and independent implementation all passed in ordinary and seed17 modes. The saved screen recomputed 49 output files for 2416 occurrences / 213 distinct literal cores, with zero byte, Sigma or metadata mismatches. All 2416 occurrences are compatible. The 125 literal two-private placements include 30 disk placements and 10 compatible disk placements. Independent raw-colour and disk cross-check mismatch counts are zero.

All mathematical commands used `--check`, and `PYTHONDONTWRITEBYTECODE=1` was explicit. C44 used at most eight jobs; C44′ runs were serial. The validation driver was not used because it rewrites its saved validation ledger.

## Limits and work outside this assignment

These are finite recomputations and compatibility checks. They do not establish new source criticality, source-search completeness beyond the inherited inputs, full 933/941 source realizability, or a general absence theorem. The exact-byte input-audit failure remains a failure even though the mathematical core computations passed.

No Lean build / axiom audit, M2 paper audit, k≥10 enumeration, commit, push, PR or remote CI was performed by this subtask. The parent M3 audit owns the checkout-wide before/after drift verification.
