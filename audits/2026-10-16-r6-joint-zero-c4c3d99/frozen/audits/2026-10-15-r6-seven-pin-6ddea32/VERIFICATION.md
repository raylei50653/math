# Replays and negative controls

All commands were run from `/home/ray/developer/ai/math`. The two generation
commands used exclusive-create files. The main checker and certificate were
then retained without modification; the review-requested unsplit control is
a separate supplemental checker and separate certificate.

```sh
python3 -B audits/2026-10-15-r6-seven-pin-6ddea32/check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-15-r6-seven-pin-6ddea32/check.py --check
python3 -B audits/2026-10-15-r6-seven-pin-6ddea32/check_unsplit.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-15-r6-seven-pin-6ddea32/check_unsplit.py --check
```

All four replays returned0. The main result is60 proper row orbits,
180 pairing cases,1,080 partition options, zero extra rejections, and the
8-point mask319 graph with216 complete labelled colourings and zero
nonfacial triangles. The independent unsplit comparison enumerates the
full restricted set and finds660 old options removed across180 cases.
In particular the specified ABABCBC/AB|CD partition has no unsplit witness;
this is stronger than merely observing that the first stored witness split z.

The main certificate's empty ABABCBC seven-pin fibre was deliberately
changed to contain `ABABCCDD`. This is invalid both as an asserted fibre
and as a literal seven-pin projection. Recomputing the entire certificate
rejects it with return1. The supplemental rejected-option total was
changed to zero; the supplemental checker likewise rejects with return1.
The failed files are retained separately:

```sh
python3 -B audits/2026-10-15-r6-seven-pin-6ddea32/check.py --check --certificate audits/2026-10-15-r6-seven-pin-6ddea32/tampered-negative.json
python3 -B audits/2026-10-15-r6-seven-pin-6ddea32/check_unsplit.py --check --certificate audits/2026-10-15-r6-seven-pin-6ddea32/unsplit-tampered-negative.json
```

These two commands are expected to fail. Actual stdout/stderr and exit
receipts are under [logs](logs), in `receipts.json` and
`unsplit-receipts.json`.

Every replay checks each frozen authority file against INPUTS.json and
also compares the current original path with the same SHA256. All
recorded frozen and live input drift checks passed. No mutable current
document is used without this check. The main certificate binds the
checker and input manifest by SHA256; the supplemental certificate binds
both its checker and the unmodified main checker.

`probe.py` retains the exploratory implementation; it is not an authority
or replay entrypoint. The canonical finite evidence is `check.py`,
`certificate.json`, `check_unsplit.py`, and `unsplit-certificate.json`.
The source-theorem status remains `not triggered` throughout. Finite
model equality and an explicit weak graph do not constitute a minimum
source realization or exclusion. No Lean or plantri run was performed.
