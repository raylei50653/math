# Two-reference parity continuation receipt

2026-10-29. BASE e1a90fea41702d7c98747716a5960198aecbecb3.
The workspace includes the previous continuation bundle; its old hashes,
certificates and receipts are retained unchanged. No commit or push.
[Proposal](PROPOSAL.md) preceded both the 16-graph experiment and directed
F4-prefix freeze amendment.

Canonical source: [two-reference report](../../docs/c5_two_reference_parity_continuation.md).
Paper scope: every new odd complement cycle hits both alpha-minus-M and
gamma-minus-M; its common retained segments cross the selected/unselected
complete-difference-component partition at least twice. With no difference
cycles, at least two vertex-disjoint actual retained segments join the two
paths. These are necessary statements; neither forces evenness.

[verification.json](verification.json) freezes all 16 previous disk inputs,
all independently re-enumerated PM families, every eligible alpha/gamma pair,
both complete paths and all cycle subsets, full complements and original odd
cycle edges. Fourteen disks do not trigger the reference setup; disks 6 and 9
each trigger one pair, all two target candidates are even.

To provide genuine F4 failure data, only the first 15 inputs in the existing
seed-5/200 domain are replayed. First graph-wide failure is generator index
14 (10 primal vertices), with one alpha14/gamma02 pair, no difference cycle,
and a unique target candidate in PM04 with an actual nine-cycle. All three
target families have another even-complement matching. The two inter-path
retained segments have lengths one and one; another same-path segment has
length four and three difference connectors give odd total length nine.
The complete matching families and every candidate are saved. No new seed,
generator, graph budget or broad P4 mechanism search.

Five-star reference-pair table: three pairs triggered and seven not triggered;
only 02,13,14 have even references in this control. It does not instantiate a
five-reference blocking source. Five-reference/ten-pair planar exclusion,
all F4 failure classification, (E), 932/933/941 and 4CT stay OPEN.

Commands actually executed:

```bash
python3 scripts/c5_two_reference_parity_verification.py --out audits/2026-10-29-two-reference-parity-e1a90fe/verification.json
python3 scripts/c5_two_reference_parity_verification.py --check audits/2026-10-29-two-reference-parity-e1a90fe/verification.json
python3 scripts/c5_parity_swap_probe.py 5 15
python3 -m py_compile scripts/c5_two_reference_parity_verification.py
git diff --check
```

The exact certificate replay passed; original exploratory script agrees on
one graph-wide failure with an independently existing good target. Its stdout
is retained in [legacy-probe-prefix.txt](legacy-probe-prefix.txt).
Root owns final routing changes and repository-wide documentation checks.

Closure scope: T1/T2 and the specified finite F4 freeze, not P2 full acceptance.
Updated: this new source and evidence only. Root adds continuation links.
Reviewed-unchanged: previous P1/P3 local proofs and receipts; no assertion that
matching-difference paths are complete Tait components. No Lean claim.
Propagation stop: topic source, direct parent and index routing by root.
