# Cross-review: the common-graph colour-function obstruction

Reviewed `audits/2026-10-15-kempe-common-graph-6ddea32/PROOF.md`,
`check.py`, `verify.py`, and `certificate.json`. Exact hashes and the
normal/seed17 independent-verifier receipts are in
[CROSS_VERIFICATION.json](CROSS_VERIFICATION.json). Review result: **PASS
within the stated single-valued S4-equivariant state-lift contract**.

The finite domain is complete for this contract. A Layer0 row uses at
least three colours, so its S4 stabilizer fixes all four colours and is
trivial. The432 literal states therefore have18 free orbits. A vertex
colour function is exactly one four-valued choice at each canonical row;
there is no additional vertex-count cutoff. Every literal individual
switch contributes its necessary two-variable constraint. The
independent verifier checks each eliminated value against the current
domains and checks that each branch contains all surviving choices.
Its47-node tree yields exactly25 functions. The root's separate
fixed-order429-node DFS obtains the identical ordered function list,
maximal edge list, and seven pin-function indices; I compared these
artifacts directly, without importing the generator.

For arbitrary finite H, each original vertex maps to its colour function.
An original edge can join two types only if their colours differ at
every literal state. Thus the41-edge graph containing **all** such pairs
is an overapproximation of every admissible original graph. Equal
functions at distinct nonadjacent vertices are harmless: a graph path
still maps to a walk, and each vertex in a fixed bichromatic path maps
to the corresponding bichromatic induced type graph. The argument
needs neither injectivity, equality of complete colouring sets, planar
embedding, nor a bound on the number of hidden original vertices.

At state0 `ABABCBC`, the stored CD block requires t and q connected.
Their types19 and18 lie in different components of the full induced
CD type graph: `{15,19,24}` versus `{16,17,18,20,21,22,23}`. Because even
the maximal graph lacks a path, deleting allowable edges or duplicating
types cannot produce one. This one incidence is enough; the additional
1055 failed incidences are not needed to multiply the conclusion.

The weak pointwise law allows a vertex either to stay fixed or to follow
the displayed colour transposition. It does not assume that every hidden
component is visible. The stricter13-function cube refinement is not
used in the main contradiction. The paper appropriately separates that
stronger optional assumption.

The scope boundary must remain literal in any synthesis: an exact lift
here includes the declared S4 action on full colourings and a single
full-colouring choice per displayed state. A many-valued hidden-state
cover need not admit a transition-compatible equivariant section.
Different partitions/transitions on the same22 rows are also outside
the theorem. Thus the common-graph result excludes this chosen720-state
table under the stated lift contract, not the full22-row relation or
the original complete319 source. Those remain OPEN, with no genuine
source instance supplied. No blocking issue was found in that scoped
claim.
