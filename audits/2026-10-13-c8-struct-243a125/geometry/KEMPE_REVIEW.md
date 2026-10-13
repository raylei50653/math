# Independent review of the fixed-split Kempe certificate

Reviewer scope: paper soundness of `../kempe/PROOF.md`, independent inspection of
the checker, and a fresh exact replay. No producer code was imported in this
review and no solver result is a premise. The replay output is preserved in
[kempe_independent_check.log](kempe_independent_check.log).

**Result: PASS for the stated necessary-condition theorem and exact certificates,
with the conditional dual scope below.** This review does not prove graph
realization or source exclusion from a feasible cone witness.

## 1. Same-graph transport and weights

For a fixed graph and fixed split 01|23, changing the orientation of a two-color
component leaves every vertex's pair membership unchanged. The two induced
graphs, all of their actual components, and their boundary contacts therefore
remain exactly the same. Conversely, a vertex subset S whose two induced graphs
are bipartite determines one complete component-swap orbit: orient every
component independently. Boundary-touching components have nonempty disjoint
supports, so all 2^b boundary words are distinct; components missing the boundary
give the common multiplicity 2^k on every word. Summing by S counts each full
coloring once. This proves the nonnegative orbit expansion on the same H.

The order-eight split normalizer preserves this family of orbits. The count for
a literal word is invariant under its action. For a representative r, exactly
8/|D.r| group elements send any one word in D.r to r. Thus the stored coefficient
(8/|D.r|)|O∩D.r| has the correct stabilizer weight. Dividing each generator by its
positive gcd merely rescales its cone coefficient. The 821 rows retain all
different positions of the fixed split relative to an S4 pattern; constraining
each row to the same x at its normalized pattern imposes the needed S4
invariance. Collapsing to 274 rows before this step would not do that.

This averaging does not claim all three complementary-split component systems
coexist on a graph: it is a necessary consequence of the existing single graph,
and feasible artificial coefficients need not realize such a graph.

## 2. Triangular face interfaces

A proper triangular face uses both pair labels, so its pair-label 1/2 contour
is one segment joining two distinct edge midpoints. Across faces these segments
make disjoint arcs and closed curves; no contour passes through a graph vertex.
If t boundary edges change pair, there are t/2 proper arcs. These arcs divide a
disk into t/2+1 boundary-incident regions. Each closed curve creates exactly one
additional region missing the original boundary and changes no boundary-region
count, including for nested loops. Within each face each side of the contour
retracts to that pair's vertices and same-pair edge (if present); these local
retractions glue, identifying regions exactly with pair-induced components.
Hence the number b of boundary components is t/2+1, independently of graph size.

This verifies the paper's restriction from 1,552 generic generators to 981
triangulated generators. All actual interfaces are covered; the converse is not
claimed. The proof uses actual triangular faces and their common embedding.

## 3. Exact dual scope

The six old-vector separators are nonnegative on every generic generator and
strictly negative on the named frozen vector. These prove that those vectors
cannot be actual graph counts. They do not exclude a query having other vectors.

The four forced-zero duals have a different, conditional scope: they are
nonnegative on every generic generator whose entire support is contained in the
query's already-proved upper U. Every actual positive orbit coefficient meets
this restriction by nonnegativity and the known zero counts outside U.
The checked signed-span identity is

    -z·x_lifted + a·x = x_i,

where a is supported outside U. Thus x_i=−z·x_lifted≤0; x_i≥0 forces x_i=0.
This sign and the conditional support restriction were independently checked.

For clarity, those four forced-zero duals are **not** globally nonnegative on
all 1,552 generic generators. Direct exact inspection gives:

| Query / fibre | Minimum on all generic generators | Number of negative generators |
| --- | ---: | ---: |
| c15-941 / 98 | −104267/39728 | 324 |
| c15-941 / 159 | −69/82 | 274 |
| c20-941 / 34 | −57739/27420 | 322 |
| c20-941 / 54 | −3337/2408 | 238 |

All such negative columns are irrelevant only because the source's proved
zero-outside-U condition forbids their positive coefficients. An earlier broad
wording in the proof's section 3 was reported to the author and corrected; the
checker and the detailed section 4 already used the correct conditional scope.

## 4. Replay and limits

The fresh solver-free checker independently regenerated all 6,564 literal words,
821 normalizer rows, 1,552 generic generators and 981 triangulated generators.
It checked exact rational common counts, signed equality coefficients,
nonnegative orbit decompositions, every original attachment and boundary order,
all ten outer-row counts, the new Boolean support closures, all six separators,
and the four conditional zero identities. After the author's final addition,
the replay also checked all 91 noncrossing-identification positivity conditions
on each of the eight root-level surviving witnesses. Five corrupted certificates were
rejected (multiplicity, dual sign, named fibre, identity, boundary order).

The cone stage retains ten feasible query witnesses. Root-level use of the
induced-C8 theorem and planar identification is a separate source theorem and
can exclude queries despite that cone feasibility. Remaining graph realization
requires one shared triangulated H, its original rotation and degree data, and
compatible actual component systems; none follows from this finite cone.
