# Round3 Kempe: an exact common-graph lift is impossible

BASE `6ddea32a81349821ad3724ae1652bddb9c6a7b04`.
The [proof](PROOF.md) adds a common-original-edge necessary condition and
uses it to exclude every finite-order, single-valued S4-equivariant graph lift
of the prior720-state witness. This is a graph-realizability obstruction for that
specific transition table; the full22-row relation and original319 source remain
OPEN.

For every original vertex, retain its colour at all states as one function.
Original edges must have different endpoint colours at every state, so every
candidate graph maps into the maximal graph on compatible functions. A required
bichromatic pin path must survive that map.

Only Layer0 is needed. All432 literal states reduce by global S4 covariance to
18 four-valued variables. All stored individual switches yield53 binary tables.
A complete47-node search tree proves that exactly25 functions are possible;
their maximal common-edge graph has41 edges. At state0 `ABABCBC`, the required
CD block `{t,q}` is impossible: t's type19 can reach only `{15,19,24}`, while
q has type18. The same check finds1056 failed block incidences.

The main obstruction uses only the weak pointwise switch law. It does not assume
that all hidden components are visible or that the product of visible switches
acts globally on a genuine graph. An optional stricter exact-cube filter leaves
13 functions and18 edges and gives the same failed-incidence count.

The complete functions, edges, failed blocks and exhaustive search proof are in
[certificate.json](certificate.json). [check.py](check.py) reconstructs them;
[verify.py](verify.py) independently checks the proof tree and all graph data
without importing the generator. Normal/seed17 runs of both pass; missing-type,
false-edge and missing-branch certificates are rejected by both. Exclusive
certificate regeneration is rejected. A genuine K3 positive control passes.
See [verification](VERIFICATION.md) and [input custody](INPUTS.json).

A many-state hidden-colouring refinement may have no transition-compatible
single-valued section; it is not excluded. Different partitions or transitions
on the same22 rows are likewise untouched. No original degree/collar source was
realized, no complete319 exclusion or improved k bound was obtained, no Lean
theorem was added, and omega=0 and the general main claim remain OPEN. No
commit/push was performed.

The independent [six-pin cross-review](../2026-10-15-six-pin-lifts-6ddea32/CROSS_REVIEW.md)
accepts this exact scope. A further
[root replay](../2026-10-15-route-round3-6ddea32/common-graph-independent.json)
uses fixed-order DFS with429 nodes and independently obtains the same25
functions,41 edges and pin-type indices. This audit's
[XOR cross-review](CROSS_REVIEW.md) also accepts the separate batch-descent
results with their source-level obligations left OPEN.
