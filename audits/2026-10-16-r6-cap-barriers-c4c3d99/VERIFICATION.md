# R6-CAP-BARRIERS verification and delivery

2026-10-16. The paper results are [A](A/PROOF.md), [B](B/PROOF.md),
[C](C/PROOF.md); independent adoption is recorded in [REVIEW](REVIEW.md)
and the specific [101 interval review](A/REVIEW-101-INDUCED5.md).
These are arbitrary-size source-conditional proofs, not conclusions
extrapolated from small graphs. No new external theorem or Lean result
is used.

## Replays and negative controls

| Scope | Result and evidence |
| --- | --- |
| A weighted parity | Normal/seed17 identical; 9,516 two-wheel membership-quotient states, all one-wheel bounds, literal spokes and four-of-five C5 side check. Deliberately wrong constant and m-toggle sign rejected by direct comparison. [normal output](A/check-normal.json), [seed17 output](A/check-seed17.json) |
| B common matchings | Five fixed controls; 12 actual barrier/matching saturation checks. Actual crossing-cap-pair triggers are zero, explicitly retained. A separate complete K3,3 matching control supplies 720 nonvacuous cut-algebra checks. Normal/seed17 identical; corrupted tau and exclusive-create rejected. [receipt](B/VERIFICATION.json) |
| C complete local fibres | All64 bit assignments and120 complete W5 colourings,22 valid partial-matching states,2 valid empty fibres. Normal/seed17 identical; missing odd-rim and falsely allowed square certificates rejected; exclusive-create rejected. [receipt](C/VERIFICATION.json) |
| Root independent replay | A and C normal/seed17: [commands and exits](root-replay-AC.json). B final certificate normal/seed17: [commands and exits](root-replay-B.json). All exit0 and matching outputs |
| Source authority | All289 prior-audit input files unchanged;23 frozen input copies retained. Previous audit's own sealed-bundle checker also passed. [BASE](BASE.json), [bundle checker](check_bundle.py) |

All original minimum-source numerical tests remain **not triggered**.
A checks the finite parity-membership quotient, B includes an explicitly
re-marked nonsource negative control, and C checks a local wheel and
complete local fibres. None is a full minimum source or a new census.
The 101 original face-interval theorem is paper evidence with independent
review; its later addition changed no checker or numerical certificate.

B's final authority is [certificate-v2.json](B/certificate-v2.json).
The earlier [certificate.json](B/certificate.json) is retained unchanged
from before adding the explicit nonvacuous cut-algebra control. It is
not the final replay target. A emits deterministic calibration receipts,
not a source certificate; its negative controls concern the charge
formulas. B/C provide separate malformed-certificate and overwrite tests.

Replays from the repository root:

```sh
python3 -B audits/2026-10-16-r6-cap-barriers-c4c3d99/A/check.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-16-r6-cap-barriers-c4c3d99/A/check.py --seed 17
python3 -B audits/2026-10-16-r6-cap-barriers-c4c3d99/B/check.py --verify audits/2026-10-16-r6-cap-barriers-c4c3d99/B/certificate-v2.json
python3 -B audits/2026-10-16-r6-cap-barriers-c4c3d99/C/check.py --check audits/2026-10-16-r6-cap-barriers-c4c3d99/C/certificate.json
python3 -B audits/2026-10-16-r6-cap-barriers-c4c3d99/check_bundle.py
```

For B/C the same check commands were also run with `PYTHONHASHSEED=17`.
The bundle checker verifies frozen bytes, prior authority, permitted
routing drift, new Python syntax, local file links and sealed membership;
it explicitly does not certify mathematical proof correctness.

## Documents and custody

The four pre-existing dirty routing files were snapshotted before this
continuation. New evidence is confined to this audit; previous reports,
certificates and frozen files retain their original bytes. Git HEAD
remains c4c3d99. No commit or push was performed.

Formal documentation checks and tracked whitespace passed. The initial
document check counted687 Markdown files and9016 local links; scoped
DocGraph counted97 documents,383 relations and0 errors. Final checks
after the 101 corollary are recorded separately in
[final-checks.json](final-checks.json). Whole-tree DocGraph was not run;
the scoped PASS is not reported as a whole-tree result. Existing source
censuses and Lean builds were not rerun because neither changed.

The final inventory is [MANIFEST.json](MANIFEST.json). Its own bytes are
excluded from the inventory; every other delivered file, including frozen
copies and negative controls, is hashed. The sealed bundle is checked
read-only after inventory creation.

## Propagation and remaining scope

- Updated: Kempe guide's active stop, evidence row and milestone; STATUS's
  direct report index and current summary; the direct C4 parent entry;
  State guide's active-route pointer only.
- Reviewed unchanged: HANDOFF research lines, general C4 finite theorem,
  fixed r6 census bounds and all previous audit evidence. The new theorem
  is about wheel and induced-five-cut subclasses, not full-source closure.
- Remaining OPEN: 101 noninduced single-five-cut barriers, other surviving
  nonwheel five/seven-cut and paired-five-cut configurations, joint
  positive minimum oddness, full319, general T/T0, r>=7 and K-infinity.
- Propagation stop: L2 direct parent. No new general numerical bound or
  research-line change justifies editing README or the global synthesis.

Reconstruction remains k+5; the general K<=22 statement and fixed r6
k>=25 bound are unchanged. The exact theorem/finite/source/Lean boundaries
are preserved in the report and current research entry points.
