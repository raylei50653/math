# Independent review of the fixed-split orbit-count theorem

Scope: read-only paper and checker-logic review by the classification worker,
independent of the Kempe author. Files reviewed: `../kempe/PROOF.md` and
`../kempe/checker.py`. No producer was imported and no graph-realization
conclusion is inferred from its primal solutions.

Reviewed proof SHA256:
`78e9d4bf5a8633a4d347f18e9f5fe17328727c7314e7d11769193a880068953a`.

Verdict: **accepted**. The generic orbit cone is a universal necessary
condition for one fixed graph's complete counts. The triangulated boundary
component identity is also sound. The distinction between discarded
*saved vectors*, forced zero *fibers*, and excluded *source queries* is
maintained. In particular this Kempe stage alone excludes zero queries.

## One fixed graph and the complete commuting orbit

For a fixed subset S of V(H), the two pair-induced graphs are fixed actual
graphs. If both are bipartite, every one of their connected components has
exactly two proper colorings in its designated two-color pair, including
singleton components. Their independent orientations give all full H
colorings having exactly S in the first color pair. Edges across S and its
complement are automatically proper. Thus no graph or component partition
is changed between the colorings being counted.

Every boundary-meeting component changes at least one boundary position
when flipped. Disjoint components change disjoint nonempty position sets,
so the 2^b boundary words are distinct. Each has exactly 2^k extensions in
this orbit from the k components missing the boundary. Summing over S is
an exact nonnegative decomposition, not an assumption of nonnegative
coefficients in the unrelated equality-partition span.

The necessary noncrossing condition on the two families *together* is
correct because all distinct component subgraphs are vertex-disjoint.
Same-pair adjacent boundary vertices must be in the same component via
their original C8 edge. The finite partition enumeration only enlarges
the set of possible actual orbits, so its lack of graph realizations for
some columns cannot invalidate necessity.

## The normalizer and count scale

The eight permutations preserving the unordered pair split act on full
colorings by one common renaming. Actual literal extension counts are
invariant under this action. For any boundary word in a representative's
D-orbit, exactly `8/s_r` group elements send it to that representative.
Consequently the coefficient `(8/s_r) * |O intersect D.r|` is the correct
unnormalized eight-translate sum. Dividing by eight to average, or dividing
an integer column by its gcd, only rescales a nonnegative coefficient.

This does not multiply the actual x_p by its S4 orbit size. Mapping the
821 normalizer representatives to the common 274 canonical words retains
the equality of counts across all color renamings, including the two-color
stabilizer. The checker reconstructs literal D-orbits and directly sums
all component flips and all eight global color permutations, separately
checking the producer's formula.

## Triangulated boundary component count

The pair-membership function takes values zero and one on vertices. Each
proper triangle contains both values, so its half-level set is a single
segment joining the midpoints of the two cross-pair edges. Across an
internal edge the two segments join without branching; at C8 there is
exactly one endpoint per cross-pair edge. The result is disjoint properly
embedded arcs and simple closed curves, with exactly t/2 arcs.

The t/2 disjoint proper arcs divide the disk into t/2+1 boundary-incident
regions. A closed component cannot meet or enclose a proper arc reaching
the disk boundary, and merely cuts off an interior region. It therefore
does not change that boundary-region count. Each complementary region
retracts, triangle by triangle, onto the vertices and original edges of
one pair; connected regions correspond exactly to connected components
of the induced pair graphs. Hence `b=t/2+1` without a bound on H's size.
The t=0 case is included: an alternating two-color boundary is itself in
one boundary-meeting pair component, even if interior loops occur.

## Exact dual implications and residual scope

The recorded dual identity gives `x_i = -z dot x_tilde` because all other
terms are already-proved zero coordinates. An actual count vector's
nonnegative orbit decomposition gives `z dot x_tilde >= 0`; with x_i>=0
this forces x_i=0. Checking every generic generator supported in U is
sufficient: positive coefficients of generators leaving U are impossible
by nonnegativity and the known zeros outside U. Checking all 91 equality
columns establishes the identity throughout the already-proved signed
span. No nonnegative equality expansion has been inserted.

The four forced fibers use the generic cone, so their validity does not
depend on the triangulated filtering argument. The six separating duals
also validate on the full generic cone. Exact primal witnesses only show
that the strengthened necessary system remains feasible. They do not
construct a single H implementing different orbits, pair splits, original
rotations, J_e fibers, or the source-minimality replacement restrictions.

The later cofacial-quotient exclusion of c16-941 and c32-941 is a separate
source-geometric step. Keeping their feasible Kempe witnesses correctly
documents the strict limitation of the orbit-count test. For the eight
remaining queries, the checker additionally tests positivity for all 91
cofacial-identification equality columns, so no quotient condition is
silently dropped when adopting the new count witnesses.
