# P1–P3 local continuation receipt

2026-10-29. BASE e1a90fea41702d7c98747716a5960198aecbecb3.
[Proposal](PROPOSAL.md) was recorded before experiments.
Canonical mathematical source: [five-leaf continuation](../../docs/c5_parity_shared_cut_continuation.md).

Paper scope: complete parity-free crossing-path lemma, six-term double-dimer
identity, exact retained-segment parity reconstruction, five-leaf fixed-word
complete-region repair, and terminal-support bound at a fixed-word minimizer.
These proofs do not use 4CT or matching reachability as an existence oracle.
No new Lean theorem.

Finite same-source evidence: [verification.json](verification.json), including
all original edges, oriented disk faces, empty and complete PM families,
full regions, original matching IDs, and source SHA256 values.
16 deterministic plane C5 disks, seed 20261029; every PM family after deletion
of zero/two/four leaves is enumerated. 80 condensation identities, 38
minimizer/reference pairs, 292 whole-region batches, 45 segment rewires pass.
Six pairs have positive old oddness. Their 30 actual even-reference cut
actions all admit common sides/noncrossing exterior strands. The marked
pentagram has only diagonal PM families and fails all five condensation
identities; its 150 actual cut actions all fail. The pentagon passes all 150.
An explicit path between two old exposed leaves produces a zero-exposed
intermediate, excluded from two-exposed matching families.

Commands actually executed:

```bash
python3 scripts/c5_parity_shared_cut_verification.py --out audits/2026-10-29-parity-shared-cut-e1a90fe/verification.json
python3 scripts/c5_parity_shared_cut_verification.py --check audits/2026-10-29-parity-shared-cut-e1a90fe/verification.json
git diff --check
```

The certificate replay passed. Root owns final STATUS/guide routing and
repository-wide checks; an intermediate check_docs run correctly required
STATUS entries for the four concurrent new reports and files not yet written
by other workers. The docs-only DocGraph check passed at that point. Do not
interpret the intermediate routing failure as a mathematical failure or as a
final repository gate result.

Closure scope: only the stated local lemmas, not P1/P2/P3 full acceptance.
Updated: task status explicitly distinguishes partially started P1–P3 from
unstarted P4; counts/shared-cut source links to the new matching continuation.
Reviewed-unchanged: original C1 proof and no4ct equivalent formulations remain
valid; the new proof treats open paths and leaf incidence separately.
Remaining OPEN: K132 applicability table, full frozen F4 failure analysis,
smaller parity invariant, five-reference planar coexistence exclusion, general
(E), 932/933/941 and 4CT. No new reducible configuration.
Propagation stop: topic sources plus direct index/guide integration by root;
HANDOFF research-line tags do not change. No commit or push performed.
