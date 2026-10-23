# Later 941 publication replays

`run.py` replays the 13 assigned later directories against the publication
`BASE.json` byte/SHA inventory. It writes only this receipt directory, never
runs `produce.py`, `--produce`, or `--generate`, and leaves all custody guards
enabled. Run it from any working directory with `python3 -B /path/to/run.py`.

The 13 `check.py` entries use the normal, seed-17 optimized, and negative
commands in their `REPORT.md` where commands are listed. For the four reports
without a command block (`gamma8-empty-k-stars`, `gamma8-k-star-review`,
`gamma8-n7-review`, `gamma8-resource-review`), their argparse declarations and
main functions were inspected before using the same read-only pattern. The
independent `gamma8-k-star-review/check_transfers.py` and the round-5
`transfer_caps.py` each receive an additional normal/seed-17/negative triple.

Seed-17 mode always sets `PYTHONHASHSEED=17` and runs `python3 -B -O`.
`--seed 17` is included only where the CLI supports it. Round-5 and round-6
integration checkers, the N7 independent review, and both transfer checkers
have no `--seed` argument. Normal and negative runs explicitly unset an
inherited `PYTHONHASHSEED`. The three workers each have a 900-second subprocess
timeout. `plan.json` is the complete argv list; each command has separate
stdout, stderr, and JSON metadata including exit code, elapsed time, relevant
environment, output hashes, and parsed payload. Ambient environment secrets
are not serialized.

`source-before.json` and `source-after.json` compare all frozen files in the
13 assigned directories to `BASE.json`. `SUMMARY.json` records actual replay
results and compares every normal/seed-17 JSON payload after removing the
explicit `seed` field. It recognizes both the top-level and `validation`
PASS schemas; all 15 negative runs must also report rejected semantic
controls. `python3 -B /path/to/run.py --summarize` rechecks raw stdout/stderr
hashes and parsed payloads before regenerating the receipt summary. A failed
checker or negative control remains a failed receipt; this runner does not
alter its inputs to obtain a pass.

`run_external_round7.py` separately replays the exact six external-negative
argv entries from the original round-7 `VERIFICATION.json`, against its
retained `negative-inputs-v2` files. Each fresh receipt requires exit code 1
and the original expected rejection-reason substring. Results and original
argv provenance are in `EXTERNAL-SUMMARY.json` and `external-plan.json`;
`external-source-before.json` and `external-source-after.json` independently
repeat the frozen source checks.

The completed main replay passed 45/45 commands, rejected 125 semantic
controls, and matched all 15 normal/seed-17 payloads. The six external
negatives all rejected with their expected reasons. All four source custody
checks covered 588 frozen files and found zero drift.

These are finite replay receipts. They do not establish source realization,
exclude any remaining original source, add a Lean theorem, or close matching.
