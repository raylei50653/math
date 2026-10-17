# Verification and custody

2026-10-16; BASE `e98a1cc1afd9a428600dcf4027d8138078c01650`.
The exact mathematical scope and OPEN boundary are in [REPORT.md](REPORT.md).

The active group replays are:

```sh
python3 -B audits/2026-10-16-r6-319-complete-e98a1cc/A/check.py --check
python3 -B audits/2026-10-16-r6-319-complete-e98a1cc/B/verify.py --check audits/2026-10-16-r6-319-complete-e98a1cc/B/certificate.json
python3 -B audits/2026-10-16-r6-319-complete-e98a1cc/C/verify.py --check
python3 -B audits/2026-10-16-r6-319-complete-e98a1cc/integration/check_independent.py --check audits/2026-10-16-r6-319-complete-e98a1cc/integration/independent.json
```

The A active certificate is `A/sealed-certificate.json`; its earlier
certificates and the tuple/list normalization failure remain retained.
The B certificate keeps every complete fixed-alpha colouring fibre and
each full transition trace. The C certificate keeps dense six-/seven-pin
counts including zeros, all private lifts, every hub fibre and every r lift.

Each group records normal and seed-17 replay and malformed-certificate
rejection in its local verification receipt. The A/B/C paper arguments
were independently cross-reviewed. The root direct-assignment replay
imports none of those checkers and independently reconstructs all J/U
colourings and all dual matchings of the planar countercontrol.
The root review corrected the draft transition-count summary; see
[INITIAL-REVIEW.md](integration/INITIAL-REVIEW.md).

## Completed checks

| Scope | Observed result |
| --- | --- |
| A active certificate | Normal and seed17 PASS; four corrupted-certificate controls and exclusive-create refusal PASS; 2688 complete quotient colourings, including 1296 empty z fibres |
| B complete transitions | Normal and seed17 PASS; three corrupted-certificate controls rejected; four fixed graphs, all PMs and all complete fixed-alpha labellings checked |
| C embedded countercontrol | Normal and seed17 PASS; four corrupted-certificate controls and exclusive-create refusal PASS; all dense pin counts and original r lifts retained |
| Root independent reconstruction | PASS for 144 complete J colourings, 432 complete U colourings, all18 PMs, and dense six-/seven-pin fibres; seed17 reproduces it and a corrupted positive-W claim is rejected |
| Local documentation | `python3 scripts/check_docs.py`: PASS, 690 Markdown files and9070 local links |
| Formal docs DocGraph | `python3 tools/docgraph --include 'docs/**/*.md' check`: PASS,97 documents,383 relations,0 errors |
| Whole-tree DocGraph | `python3 tools/docgraph check`: FAIL,70 errors; the same70 errors occur with the new audit removed; two existing duplicate-ID diagnostics also name new frozen copies |
| Existing Lean library | `lake build`: completed successfully,8832 jobs; existing style/linter warnings replayed; no new Lean source or theorem |
| Whitespace and custody | `git diff --check` PASS; input check PASS with245 immutable frozen authority files and zero drift |

Group command details and negative controls are retained in
[A/VERIFICATION.json](A/VERIFICATION.json),
[B/VERIFICATION.json](B/VERIFICATION.json) and
[C/VERIFICATION.json](C/VERIFICATION.json).
The root [independent receipt](integration/independent.json) is bound to
the final C certificate SHA256
`22e67138fa399716d446da5f0fb0400fc21cb04c88c8dbb6b97dd1708defd5c2`.
Its [seed17/negative logs and group-receipt checks](integration/root-replays.json)
retain the failed first metadata aggregation described in the review record.
The [DocGraph comparison](integration/docgraph-comparison.json) records
the exact full-tree failures, without treating formal-doc success as
whole-tree success. The root library build was executed in this turn;
its successful process completion is recorded in the final-check receipt.

## Independent mathematical review

The group papers were cross-reviewed in
[A/REVIEW-B.md](A/REVIEW-B.md), [B/REVIEW-A.md](B/REVIEW-A.md) and
[C/CROSS_REVIEW_A_B.md](C/CROSS_REVIEW_A_B.md).
Final report adoption was reviewed separately in
[A/REVIEW-INTEGRATION.md](A/REVIEW-INTEGRATION.md),
[B/REVIEW-INTEGRATION.md](B/REVIEW-INTEGRATION.md) and
[C/REVIEW-INTEGRATION.md](C/REVIEW-INTEGRATION.md).
The small h-definition and J-deletion wording suggestions were adopted.
The incorrect six-two-transition draft summary was corrected to four
two-transition labellings and two four-transition labellings.

## Frozen scope and replay

[BASE.json](BASE.json) freezes245 authority files at the recorded clean HEAD.
The already-frozen routing documents may change only in the four declared
paths; every other live authority file must remain byte-identical.
The additional state-guide routing snapshot was read using `git show BASE:path`.
The final [MANIFEST.json](MANIFEST.json) binds the audit file membership,
every retained byte and the four resulting routing documents.

```sh
python3 -B audits/2026-10-16-r6-319-complete-e98a1cc/check_bundle.py --check
```

This check validates frozen-input hashes, the exclusive output boundary,
Python syntax and new local Markdown links. The manifest itself and Python
bytecode caches are excluded from its file-content map. Normal root and
group replays are read-only. Original-source controls remain `not triggered`;
the main positivity claim is **OPEN**. No commit, push, old certificate
rewrite, external enumeration rerun or new Lean proof was performed.
