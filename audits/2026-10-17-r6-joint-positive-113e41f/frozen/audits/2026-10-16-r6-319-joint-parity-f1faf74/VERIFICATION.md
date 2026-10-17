# Verification and evidence boundaries

The immutable working-tree input snapshot is listed in [BASE.json](BASE.json).
Two later mathematical inputs were frozen separately in
[ADDITIONAL_INPUTS.json](ADDITIONAL_INPUTS.json) and
[SOURCE_G_INPUT.json](SOURCE_G_INPUT.json); the original BASE was not rewritten.
The connected output seal is [MANIFEST.json](MANIFEST.json). Only the three
shared routing/summary documents are allowed to differ from their initial
snapshot; old mathematical inputs and the pre-existing continuation remain
byte-identical. See the final custody receipt in `integration/`.

## Active replays

Run from the repository root:

```sh
python3 -B audits/2026-10-16-r6-319-joint-parity-f1faf74/A/check.py
python3 -B audits/2026-10-16-r6-319-joint-parity-f1faf74/A/review_c_independent.py
python3 -B audits/2026-10-16-r6-319-joint-parity-f1faf74/A/count_cone.py
python3 -B audits/2026-10-16-r6-319-joint-parity-f1faf74/B/verify.py --check audits/2026-10-16-r6-319-joint-parity-f1faf74/B/certificate.json
python3 -B audits/2026-10-16-r6-319-joint-parity-f1faf74/B/check_source_lifts.py --check audits/2026-10-16-r6-319-joint-parity-f1faf74/B/SOURCE_LIFTS_CERTIFICATE.json
python3 -B audits/2026-10-16-r6-319-joint-parity-f1faf74/C/check.py
python3 -B audits/2026-10-16-r6-319-joint-parity-f1faf74/C/check_final_step.py --check audits/2026-10-16-r6-319-joint-parity-f1faf74/C/final-step-certificate.json
python3 -B audits/2026-10-16-r6-319-joint-parity-f1faf74/integration/independent_control.py
python3 -B audits/2026-10-16-r6-319-joint-parity-f1faf74/integration/independent_mandatory.py
python3 -B audits/2026-10-16-r6-319-joint-parity-f1faf74/integration/check_bundle.py
```

All active certificate checks are read-only and use the standard library.
The exploratory count-cone solver used SciPy, but the saved rational witness
is checked exactly with `fractions.Fraction` without the solver dependency.
A's active local certificate is `certificate-v2.json`; its earlier writer and
certificate are retained as historical files. The count-cone active witness
is `count-cone-feasible-v2.json`.

## Mathematical checks

| Evidence | What was verified | Boundary |
| --- | --- | --- |
| A | All16384 seven-pin positions, all r lifts, commuting whole component maps, singleton and mixed-link algebra | Conditional paper maps, no source realization |
| C shared H | Same H and ordered six-boundary components, all1521 K132 support pairs, unique(1022,1022) | Exhaustive necessary-condition elimination |
| A independent C replay | Independent65536-row nested-lift reconstruction and six-/split-nine-boundary mask-pair checks | No import of C's checker; agrees99→81 |
| C original F | All820 proper nine-boundary colour orbits,475 empty five-point fibres,648 local lifts; improper rows retained as empty | Three fixed original supports processed separately |
| B independent F replay | Explicit original edge graph, all4^5 assignments per row, full upper tables607/659/716 and all supplied fixed-row lifts | Independently checks local lifts; does not independently reprove C's fixed-point algorithm |
| C full-source closure | 607→362,659→536,716→662; common H upper relation58, two cap supports1022 | Actual private fibres may still be empty; v5 is not excluded |
| C final step / root independent replay | All58 single-row absence tests; six delete-one cases lose U bit8, proving12 literal complete H fibres nonempty | Every such fibre has no v lift; actual K C4 closure34→34 |
| A common count cone |1392 labelled rows, three families of290 cubes, one shared count vector,25 positive support obligations | Exact rational feasible relaxation, no source realization |
| B finite plane control |288 complete colourings,38 PMs, all cuts and24360 marked triples | Global joint oddness2 only for the explicitly weaker premise set |
| Root independent control | Direct4^9 assignments, bit-mask PMs, primal-cycle reconstruction of small cuts | Confirms2 cyclic four-cuts,22 cyclic five-cuts and absent literal source layout |

Normal and seed17 replay receipts and all negative controls are retained in
`A/VERIFICATION-v2.json`, `B/VERIFICATION.json`, `C/VERIFICATION.json`, and
the root's `integration/replays-*.json`. They reject lost empty slots, lost
full lifts/cube members, invented even-joint fibres, stale marked endpoints,
invented source layouts, corrupted rational counts, and overwrite attempts.
The initial ineffective A negative mutation is retained and distinguished
from its corrected rejecting control. No historical certificate was silently
replaced to hide a failed run.
The final source-existence/C4 check has its separate
`C/FINAL_STEP_VERIFICATION.json`; its earlier sealed C inputs were unchanged.

## Repository checks and scope

`lake build` completed successfully with8832 jobs. Existing AttachmentOrder
and SymRelabel linter warnings remain; no Lean source was changed and no new
paper or finite statement is claimed formalized. The final repository check
receipt records `scripts/check_docs.py`, formal-doc-scoped DocGraph, and
`git diff --check`. Whole-tree DocGraph and old large source enumerations were
not rerun; a formal-doc pass is not a whole-tree pass.

The new source statements preserve all named edges, original degrees,
ordered boundaries and all reconstruction fibres. Actual globally minimum
source instances supplied: zero, **not triggered**. Full319 exclusion,
v/w5 exclusion, omega_e=0, the general main theorem, and strict completed-source
descent remain open. No commit or push was requested or performed.
