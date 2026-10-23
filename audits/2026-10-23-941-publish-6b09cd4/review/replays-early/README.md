# Early publication replays

These receipts replay 19 directories from the publication `BASE.json`, excluding
the 13 directories assigned to the later replay batch. The original 1,790 audit
files matched the frozen byte counts and SHA-256 values before and after the run.

All **62 commands passed**: 57 commands copied from the reports, the independent
`gamma8-chi-review/check_cover.py` normal/seed17/negative triple, and two runs of
`wrong-side-general/review_empty_m2.py`. All 21 normal/seed17 payload pairs agree
after removing only fields named `seed`. The 20 semantic-negative commands
rejected 260 in-memory damaged cases.

The supplementary `review_empty_m2.py` uses Python assertions, so both its normal
and seed17 runs retain assertions; it is not run with `-O`. The other seed17 runs
use the documented `PYTHONHASHSEED=17` and `-O` modes. The `joint-bpaths` and
`u-link` checkers emit custody/validation JSON without a top-level status; their
zero exit status and documented validation schema are recorded explicitly.

Each command receipt preserves argv, environment overrides, UTC start, timeout,
elapsed time, exit status, complete stdout/stderr, and parsed JSON. No producer,
certificate generator, or receipt writer inside an original audit was invoked.
No source hash guard was bypassed. These are finite calibrations; full source
realization and general exclusion claims retain their report boundaries.

Reproduce from the repository root:

```sh
python3 -B audits/2026-10-23-941-publish-6b09cd4/review/replays-early/run_replays.py
```

See `COMMANDS.json` for the exact command plan and `SUMMARY.json` for the machine
readable result and both full-source integrity checks.
