# Fixed-split Kempe transport counts on one disk graph

**Status: proved.** The orbit-count theorem below holds for every finite
plane graph H in a disk with the named proper boundary cycle C8. It uses
neither source minimality, the Four Colour Theorem, a degree hypothesis,
nor a nonnegative noncrossing-equality expansion. A second geometric
restriction applies when H triangulates the disk. These are necessary
conditions, not realization criteria.

## 1. Full-coloring orbits and exact transport multiplicities

Fix the literal color set {0,1,2,3} and its complementary split
{0,1}|{2,3}. For a proper full coloring f of this **one fixed H**, put
S=f^{-1}({0,1}). In every coloring obtained by swapping either pair on
any one of its components, S is unchanged, and both induced graphs H[S]
and H[V(H)\\S] are unchanged. Thus their actual connected components and
all their boundary intersections are unchanged. The independent component
swaps form a commuting family of involutions. This assertion relates
complete colorings of the same graph; it does not choose a new partition
independently for each boundary row.

Conversely, fix S for which both induced graphs are bipartite. Orient the
two-coloring independently on every component. This gives **all** proper
four-colorings with that S: edges between the two parts are automatically
proper. If there are b components meeting C8 and k components not meeting
C8, then each of the 2^b distinct resulting boundary words has exactly
2^k full extensions within this orbit. The distinction of the boundary
words follows because each boundary component has a nonempty, disjoint
set of positions whose colors change when it is swapped.

Let O be these 2^b boundary words and 1_O their literal indicator. The
boundary extension-count vector of H therefore has the exact expansion

    X = sum_{admissible vertex subsets S} 2^{k(S)} 1_{O(S)}.

All coefficients in this expansion are nonnegative. These are actual
Kempe-orbit indicators, **not** the noncrossing equality columns E_pi
whose inclusion-exclusion coefficients have unrestricted signs.

The partition pi of C8 by actual components must satisfy:

1. every block uses one complementary pair;
2. its blocks, from both pairs together, are noncrossing;
3. adjacent boundary vertices in the same pair lie in the same block,
   because their original boundary edge is present.

Condition 2 follows from the Jordan separation obstruction for two
disjoint connected subgraphs with alternating boundary contacts. These
three finite conditions are necessary for every actual orbit regardless
of the number of vertices in H. Enumerating all such pairs (word,pi)
therefore gives a universally sound finite cone. No assertion is made
that every enumerated partition is realized by a graph, or that the
separately enumerated partitions can coexist on one graph.

## 2. Color-frame quotient and the two-color stabilizer

The subgroup D of S4 preserving the unordered split {0,1}|{2,3} has order
8. It partitions the 6,564 proper literal C8 words into **821** orbits.
For a D-orbit representative r, let s_r be its D-orbit size, either 4 or
8. In contrast, the familiar S4 quotient has 274 rows, one with orbit
size 12 and 273 with size 24. A common graph's x_p is its count for one
literal representative, with **no** S4 orbit-size multiplier.

For each orbit indicator O from section 1, average its eight D-translates.
Before dividing by 8, its coordinate at representative r is

    v_r = (8/s_r) |O intersect D.r|.

This follows by counting the group elements sending each word of O to r;
the stabilizer has size 8/s_r. Divide v by the gcd of its nonzero entries
only to obtain a primitive integer cone generator. The resulting count
vector on 821 coordinates is x_{p(r)}. It belongs to the cone generated
by these primitive v, because X is D-invariant and averaging preserves a
nonnegative decomposition. A representation in this averaged cone is
also a representation in the original fixed-split cone: every averaged
generator is itself a sum of fixed-split orbit indicators.

The 821-coordinate construction is important. Collapsing immediately to
274 rows would discard compatibility between different ways the fixed
split meets the used colors. The equality constraints on the 821 rows
retain that compatibility through the common x_{p(r)}.

Independent complete enumeration yields **1,552** distinct generic
primitive generators. This is a complete finite classification of the
stated necessary boundary orbit conditions, justified for arbitrarily
large H by section 1. It is not a complete graph classification.

## 3. Triangulated-disk boundary component count

Suppose every bounded face of H is a triangle and let t be the number of
boundary edges whose endpoints belong to different complementary pairs.
Then the number b of pair-components meeting the boundary satisfies

    b = t/2 + 1.

To see this, assign the value 0 or 1 to each vertex according to its pair,
and extend linearly across every triangular face. A proper triangle uses
both pairs, so the inverse image of 1/2 inside that face is a single
segment. These segments join to disjoint embedded arcs and closed curves;
there are exactly t boundary endpoints and hence t/2 proper arcs. Adding
these disjoint arcs to the disk successively produces t/2+1 regions
incident to the boundary. Closed curves may add interior regions but
never change the number of regions incident to the boundary. Within
each face, the region on either side of the segment retracts to the
vertices and edges of that pair. Gluing these retractions proves that
the regions are in bijection with pair-induced connected components.
Therefore b=t/2+1. This proof does not assume any bound on interior size.

Filtering the complete boundary classification by this equality leaves
**981** distinct primitive generators. Every new primal witness in
`certificate.json` uses this smaller cone. However, the old-vector separating duals validate on **all 1,552 generic
generators**, and the four forced-zero proofs validate on **all generic
generators supported within the proved upper U**. The latter restriction
is justified by nonnegativity and the already proved zeros outside U.
Their validity does not depend on section 3.

## 4. Exact inequalities and fibre exclusions

Use the 274 by 91 frozen noncrossing-equality matrix E from the parent
count audit. The established universal signed-span condition is x=Ec.
Let U be one query's frozen v2 upper. Actual counts have x_i=0 outside U.
Only generators whose entire support maps into U can occur with positive
coefficient, since all generator coordinates and coefficients are
nonnegative.

For a forced-zero certificate at index i, the checker verifies rational
vectors z on 821 coordinates and a supported outside U such that

    - sum_r z_r E_{p(r),j} + sum_k a_k E_{k,j} = E_{i,j}

for all 91 columns j, and z dot v >= 0 for every generic generator whose
support is contained in U. For any actual nonnegative orbit expansion,

    0 = sum_v lambda_v (z dot v) + x_i.

Both summands are nonnegative, so x_i=0. This yields the following
**proved conditional source-fibre exclusions** (conditioning only on the
named query's original collar and target):

| Query | C8 row index | Literal word in that query's named cyclic order |
| --- | ---: | --- |
| c15-941 | 98 | 01201201 |
| c15-941 | 159 | 01210201 |
| c20-941 | 34 | 01020121 |
| c20-941 | 54 | 01021021 |

The c15 order is `(a0,y1_1,a1,y2_1,y2_2,a2,a3,a4)`; the c20 order is
`(a0,a1,a2,a3,y4_1,y4_2,a4,y0_1)`. The checker checks these labels and all
original supports against the frozen literal interface. Thus the four
identities refer to the same original named boundary, without rotating
or independently normalizing pieces.

Both supports shrink from 173 to **171**. A primal witness positive on
all other U-coordinates shows these are exactly the forced zeros in the
combined cone/span/zero system. The other eight queries retain their
whole frozen supports.

## 5. What the new count test excludes, and what it does not

Six frozen v2 count vectors are outside even the generic orbit cone:
c04-941, c07-941, c15-941, c18-941, c20-941, c30-941. For each, a stored
rational z has nonnegative product with every one of the 1,552 generic
generators but negative product with the old count vector. The exact
negative products are respectively -169/48, -1509/770, -16/3, -13/4,
-5, and -34/5. Those old vectors are **counterexamples to the weakened
claim** that the previous count-span and Boolean-closure conditions imply
these new same-graph transport conditions. They are not graph examples.

The other four old vectors have exact nonnegative decompositions in the
981-generator triangulated cone. All ten queries also have new exact
rational witnesses x=Ec in that cone, with the maximal supports described
above and the exact ten-row outer pattern. These are **necessary-condition
residuals at the orbit-count stage**. This stage excludes **0/10 source
queries**. The later source-cofacial argument in the root report excludes
c16-941 and c32-941 independently; keeping their cone witnesses here
records the limit of this particular necessary condition.

For each of the other eight witnesses, the checker additionally verifies
`sum_i E[i,j]*x_i > 0` for every one of the 91 nonzero equality columns.
Thus those eight witnesses pass the root argument's necessary
noncrossing-identification positivity conditions as well.

The remaining missing condition is realization of these counts, all
boundary component partitions, and the transports for different splits
by the **same** graph satisfying the original attachments, triangular
rotation, degree constraints and separating-cycle restrictions. The cone
permits independently assigning orbit weights to compatible boundary
interfaces; it does not identify the underlying vertex subsets or
simultaneously realize the component systems. Nor does it provide the
complete graph-specific J_e fibres needed to apply the five-degree-wheel
cross-edge bijections or force a boundary-preserving escape. No such
compatibility or source realization is assumed here.

## 6. Verification and controls

`checker.py` uses only Python's standard library and Fraction arithmetic.
It independently enumerates all 6,564 literal words, all 821 D-orbits,
all noncrossing component partitions, and both complete cone column sets.
It also checks every stored generator witness by explicitly applying all
component swaps and all eight color permutations. It imports none of
the producer's code and uses no optimization solver.

It checks exact cone decompositions, the common count span, full named
collar data, transfer counts on all ten rows, Boolean closure of each new
support, every globally required generic-cone separator inequality, and all
U-restricted generic-cone forced-zero
identities. Five negative controls corrupt an orbit coefficient, a dual
sign, a named fibre word, a forced-zero identity, and the named boundary
order. CLI corruption controls additionally run the real checker on
malformed certificates and require nonzero exit.

Discovery uses SciPy only to propose primal and dual vectors. Every
proposal is rationalized and checked exactly before writing the final
certificate. No floating-point optimizer result is a proof premise.
