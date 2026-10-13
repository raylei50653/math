# E-ARC2 original55 double-long joint audit

2026-10-13; frozen HEAD `19209f4cf68261fdce5e84a7804cfe04ae0957bf`.
The [canonical report](../../docs/c5_excess_two_n2_double_long_joint.md) owns
the result, proof, exact residual and replay entry points.

## Result and scope

Within the full original55 N2 double-long contract, arbitrary-size paper
arguments exclude total root-spoke counts t=0 and t=1. The new collision plus
capacity synchronization keeps one original graph, one literal row, ordered
root pins and complete piece lifts. The leaf K5 obstruction is on original
branch sets; no relation is transferred to a contracted graph.

Remaining source profiles are support sizes {3,3} with t=2 or3, and {3,4}
with t=2. They retain at least one long with k>=4. The explicit OPEN sufficient
subproposition LL-CUT uses a necessary common rejection-assignment matrix on
at most nine literal cells (512 assignments per row). A feasible matrix is
neither an actual rejection table nor a source realization certificate.
Full (2,0), original55, N2 and E-ARC2 remain OPEN.

## Authority and independent review

- [BASE](BASE.json): thirteen original input snapshots and hashes.
- [General joint/capacity paper](paper/REPORT.md): original full-fibre lemmas,
  matrix necessity, counting cuts and independent T0/T1 review.
- [Structure proof](review/structure.md): shield/spoke geometry and full T0/T1
  proofs, including shared contacts, arbitrary leaf-cycle lengths and K5 bags.
- [Independent matrix paper review](review/matrix_paper_review.md).
- [Final canonical review](review/canonical_review.md).
- [Full same-source control](controls/REPORT.md): exact path relation, complete
  original joint, and K3,3 obstruction to co-realizing this precise path.
- [Supplemental K5 review](controls/SUPPLEMENTAL_MINOR_REVIEW.md): four ownership
  calibrations, explicitly not full T1 or target-source triggers.
- [Matrix replay](joint/REPORT.md): original control plus bounded arithmetic;
  no source graph enumeration.
- [Verification receipt](verification.json): actual commands, failures and scope.

The underlying external degree-list/Gallai and original N45/44/capacity
dependencies are inherited from the frozen reports. No new external theorem
or Lean theorem is introduced. All complete-target finite controls are
`not triggered`; they are not used as source exclusions.

## Custody and documentation propagation

All new audit evidence is inside this exclusive directory; old certificates
are untouched. The mathematical BASE snapshots remain immutable. Shared
documents changed concurrently after freezing: one-long closure and unrelated
C7/W5/Kempe work appeared. Their pre-edit routing bytes are retained in
`routing-before-edit/`; [one-long impact review](paper/concurrent/IMPACT.md)
records why that new result is not an input to this proof.

Updated direct consumers: the new canonical report, Kempe guide, its STATUS
entry, and dated follow-up links in original residual/long-synchrony reports.
README/HANDOFF were checked: topic routes and active-line tags are unchanged.
The existing general size formula and parent OPEN status remain valid; no
global synthesis claim needs replacing. Propagation stops at direct consumers.
Other concurrent changes are outside this task's custody.

No commit or push was requested or performed. Existing Lean build is a
regression check only; it does not formalize these paper proofs. No upstream
ES/ER enumeration, 10-35 vertex source search, or complete N45/SD-A replay was run.

## Actual final checks

All three mathematical checkers passed normal and seed17 replay; corrupted
fibre, external-factor, minor and matrix certificates were rejected. The
thirteen frozen source files have zero hash drift. Formal-docs DocGraph,
`lake build` (8,831 jobs), and `git diff --check` passed. New untracked Markdown
and Python files were separately checked for trailing whitespace.

The final full-repository `check_docs.py` run has one outstanding error in
concurrent work: `docs/c5_forced_inequality_transport.md` links to the not-yet
present `audits/2026-10-13-forced-inequality-19209f4c/REPORT.md`. This task's
new report and links have no reported errors. The initial and final failed
logs are retained; no unrelated report was created to mask that failure.
