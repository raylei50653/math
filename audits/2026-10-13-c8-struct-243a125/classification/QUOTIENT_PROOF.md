# Cofacial equality gives two universal source exclusions

Status: **proved**, under the frozen global minimal-source contract,
the [induced-C8 theorem](../geometry/PROOF.md), and the four-color theorem.
The excluded queries are **c16-941 and c32-941**. The other eight remain
**necessary-condition residuals**. This proof concerns every finite size
of the same original H; it is not finite graph calibration.

## 1. Universal cofacial equality lemma

Let u and v be distinct nonadjacent vertices incident with one face of a
finite loopless plane graph H. Draw a new uv arc entirely within that face,
and contract the new edge. The resulting plane multigraph has no loop:
the only original edge that could become a loop is an existing uv edge,
which was excluded. Delete parallel duplicates and apply the four-color
theorem. Lifting that coloring back to H gives a proper full coloring with
u and v equal. This preserves every original edge and uses one global
color frame. It is an existence theorem for an entire H coloring, not a
gluing of color marginals.

Thus two cofacial vertices are different in **every** full four-coloring
if and only if they are adjacent. The forward direction is the lemma;
the reverse is edge properness. Neither H's size nor its internal degrees
enter the lemma. The four-color theorem is the same external existence
principle already admitted in the frozen source screen.

## 2. The complete finite boundary version

Suppose H has an induced facial boundary C8. Let pi be any noncrossing
partition of its eight named vertices in which no block contains two
consecutive C8 vertices. Every block is an independent set in H, because
the C8 is induced. Draw disjoint trees connecting the vertices of each
block in the disk on the *exterior* side of C8. Such trees exist for every
noncrossing partition: in a model disk the convex hulls of distinct blocks
are disjoint, and each block can be joined within its own hull. Transfer
that drawing to the outside disk on the sphere. Singleton blocks need no
tree, and small perturbations put all added edge interiors off C8.

Contract each of these trees. An original H edge becomes a loop only if
both endpoints belong to one block, which independence rules out. The
added trees themselves create no loops after contraction. The quotient
is a loopless planar multigraph, so four colors suffice. Its lifted full
H coloring is constant on every pi block. Additional equalities between
different blocks are allowed; requiring their colors to differ would be
an unjustified strengthening.

If x_p is the complete extension count of one fixed literal boundary word,
the consequence is

```
sum {x_p : p is proper on C8 and constant on every block of pi} > 0.
```

Each whole H coloring can be globally color-normalized to one of the 274
canonical proper C8 words. Equality constraints survive this common
permutation, so at least one displayed x_p is positive. There is no
division by an orbit size and no claim that a particular p must extend.
For actual integer counts the same sum is at least one; the proof uses
only positivity.

The 1,430 noncrossing partitions contain exactly 91 whose blocks are
independent on C8. Enumerating these 91 interfaces is a **complete finite
core of this arbitrary-size theorem**, because all other H information
is handled by the planar quotient and four-color theorem. No enumeration
of bounded-size source graphs is involved.

## 3. Exact c16/c32 contradiction in the original named frame

The previously certified full relation of every candidate H is contained
in its final upper U. In c16-941 and c32-941, U has 102 rows. Their C8 orders
and the positions of the same named pair are:

| Query | C8 order | Positions of (a1,a4), zero-based |
| --- | --- | --- |
| c16-941 | a0,y1_1,y1_2,a1,a2,a3,y4_1,a4 | (3,7) |
| c32-941 | a0,a1,y2_1,a2,a3,a4,y0_1,y0_2 | (1,5) |

For either named position pair, precisely **74 of the 274** proper C8
words have equal endpoint colors. The complete list of these 74 words'
indices is stored in `quotient.json`, together with all 274 named words.
The intersection with U is empty in both cases. This vanishing already
holds for the old pre-count-refinement Kempe upper, and therefore is not
an artifact of selecting one saved nonnegative vector.

Consequently every full H coloring would have to make a1 and a4 different.
The cofacial equality lemma forces the original edge a1-a4. But a1 and a4
are nonconsecutive on the named C8 in both queries, so this is a C8 chord.
The arbitrary-size source geometry theorem excludes every such chord.
This contradiction excludes the **whole query**, including every possible
smaller actual support, rather than just its saved positive vector.

The pair proof does not identify, rename, or alter any original B label in
the claimed source. The planar quotient is an auxiliary existence proof
for a full coloring of the original H. That coloring is returned to H in
the same global color frame. The frozen transfer and full-upper theorem
then apply to the original named collar and its complete ten-row relation,
including rejected rows and empty fibers.

## 4. Exact remaining boundary conditions

For each of the ten queries the certificate records the full intersection
of U with every one of the 91 equality conditions, including empty lists.
Both excluded queries have nine empty intersections. All 91 intersections
are nonempty for each of the remaining eight queries:

```
c15-933, c18-933,
c04-941, c07-941, c15-941, c18-941, c20-941, c30-941.
```

Their saved vectors are positive on every row of U, so they satisfy these
91 positivity conditions simultaneously. This does not realize any graph
or establish the remaining source conditions. It only marks the exact
boundary of this quotient theorem's exclusion power on the frozen uppers.

Together with the prior 60 exclusions, the C8 total is now 62 excluded
queries and eight residual queries. The global lower bounds stay h≥3 and
n5≥9. Neither h≥4 nor n5≥10 follows from two exclusions.

## 5. Independent verification

`quotient_checker.py` enumerates all 65,536 literal eight-position words
to recover the 6,564 proper words and their 274 color orbits. It independently
enumerates all 4,140 set partitions using block insertion, filters the
1,430 noncrossing ones, and then the 91 proper-block partitions. It checks
every complete equality row list, all 910 upper intersections, both
74-row pair certificates, all named positions, and all eight residuals.
The universal graph implication is proved above and in the geometry
paper; the checker verifies its entire finite interface core.

The complete eight-position word enumeration is finite interface
classification, not a source-size cutoff. It introduces no assumptions
on nonnegative equality expansion coefficients and reruns no previous
transfer/Kempe/count relaxation.
