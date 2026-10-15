# Cross-review: XOR batch descent

Reviewed `audits/2026-10-15-xor-batch-descent-6ddea32/PROOF.md`, `check.py`,
`graphs.json`, and `certificate.json`. Their reviewed hashes are recorded in
[logs/xor-independent-review.json](logs/xor-independent-review.json).
Conclusion: **accepted within the stated scope; no blocking mathematical or
certificate defect found.** No audited file was changed by this reviewer.

## Paper claims

- Theorem A's symmetric-difference cycles are vertex-disjoint. Same-direction
  endpoints avoid both marked edges; opposite-direction endpoints put both
  marked edges either in one cycle or in two separate cycles. Grouping exactly
  those two cycles gives a legal XOR-preserving step, without assuming a valid
  one-cycle intermediate state. Subsequent untouched cycles remain alternating.
  This proves connectedness for every nonempty XOR matching set and does not
  assume an even-complement endpoint.
- The batch formula uses all paths of `F-B` and both complete connector sets.
  Since B is a matching in the two-factor, the cut components have two endpoints
  and no isolated vertex. Edge parity sums in the compressed degree-two
  multigraph correctly count the complete rejoined cycles. B1 requires disjoint
  old-factor supports; B2's exactly-one-cut hypothesis makes the path
  substitution proof valid. Neither argument allows adding individual deltas
  when the two exchange cycles touch a shared old complement cycle.
- The local Tait map uses the non-alpha colour of the marked edge that is not
  alpha. It swaps the union of one or two actual alpha/beta components containing
  the marked edges. The reverse determines the same beta and the same component
  union, so this is an involution on complete labelled colourings. Empty odd
  fibres remain empty and equal direction weights may both be zero.

The independently checked36-point batch `83 -> 187` has individual changes
`[0,0]` and joint change `+2`. This concrete warning is now included in the
reviewed proof. For Tutte `0 -> 407`, the individual changes are `[0,+2]` and
the joint change is0. These examples confirm why overlapping supports must be
handled by one joint surgery.

## Finite verification

The original full checker was replayed successfully; its output is in
[logs/xor-cross-replay.stdout](logs/xor-cross-replay.stdout), with empty stderr.
The separate [review_xor.py](review_xor.py) imports none of that checker. It:

1. Enumerates every perfect matching again using greatest-remaining-vertex
   branching and compares the complete matching sets.
2. Computes complement components from original edge sets and rechecks oddness,
   all stored full Tait lifts, and every empty fibre.
3. Reconstructs the complete primitive move table from every pair of XOR states.
4. Reconstructs the actual colour components in every stored local colour
   switch and checks the complete target colouring.
5. Recomputes every start batch's individual and joint oddness changes.

All pass for the two markings of the36-point graph, the46-point Tutte graph, and
Petersen. Counts of basic moves are respectively2518, 6683, 18817, and6.
The original checker additionally verifies the saved spherical faces, rotation,
named primal edge/nonedge roles, degrees, and all cuts of size at most3 for the
stronger marked36-point control.

## Scope accepted

The stronger36-point marking satisfies more named necessary geometry but still
has no complete minimum-source construction or original empty-fibre witness.
Petersen supplies only the general cubic distinction between connectedness and
a positive even-complement fibre; it is explicitly nonplanar. Tutte's batch
escape is one finite control, and its nontrivial3-cut excludes it from the full
source class. These are not source counterexamples.

Every operation preserves the complete original graph, so no completed-source
size decrease has been established. The strictly decreasing oddness argument is
conditional on supplying a descending batch at every positive-oddness source
state; that supply is still OPEN. Source omega=0, full319 exclusion, and the
general main theorem are not upgraded by this review.
