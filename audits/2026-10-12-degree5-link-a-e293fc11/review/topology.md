# Independent topology review: Task A

This first-stage topology proof is retained as review history. Its initial
five-residual stopping point is superseded by `small-cap-refinement.md` and
the final addendum in `final-proof-review.md`: M2-46 and M2-55 are also
excluded, leaving M0, M1, and M2E. The nine-type geometry remains unchanged.

2026-10-12. BASE: `bc7c0820e6b5e585869b8a59e04f52da0dad2d33`.
Only the frozen Task A brief and frozen degree-bound theorem are used. This
review does not assume Task B or Task C. Statements about the putative source
are conditional paper statements, not findings of an actual outside-catalogue
graph.

## 1. Source and embedded star

Let `B=(a,b,c,d,e)` be the original, named outer boundary of the given embedded
source `G`. Use all frozen premises: global minimum interior order among all
sources outside `K`, edge maximality at that order, simple and 2-connected
near-triangulation, induced `B`, no occupied triangle, interior degrees at least
5, boundary degrees at least 4, and `k(G)>=13`. The small representative bounds
are C4 at most 3 and C5 at most 5; the latter is applied to smaller actual C5
caps through global minimality. None is an edge-criticality premise.

The exclusion of an occupied triangle follows from the frozen minimality
argument: fix one proper coloring of its interior and triangle; all proper
triangle assignments are in one color-permutation orbit, so every outside lift
extends after permuting that inside coloring. Clearing vertices strictly inside
the triangle preserves the full outer relation and decreases the interior
order. A triangle drawn inside `B` cannot contain any original boundary vertex
strictly inside it. Thus this clearing preserves all five named outer pins.

For an interior vertex `v` of degree 5, its five neighbors are distinct because
`G` is simple. Their actual rotation at `v` is
`L=(ell_0,ell_1,ell_2,ell_3,ell_4)`. Each consecutive pair is joined by the third
edge of the corresponding triangular face. These five edges make a simple
Jordan C5, and the union `D_L` of the five closed incident triangular faces is
a closed disk. Its only vertex strictly inside is `v`; its graph is exactly the
five-wheel. In particular this does not initially say that `L` is disjoint from
the outer boundary.

The cycle `L` is induced. A chord between nonconsecutive neighbors lies outside
the five open triangular faces. Together with its two spokes it gives a
triangle. The two nonempty arcs of `L` between those neighbors put another
neighbor on each side of this triangle, by the actual rotation at `v`. In
particular the bounded side contains a vertex, contradicting the occupied
triangle exclusion. This argument also covers chords whose endpoints touch
`B`; no entirely interior link hypothesis was used.

## 2. Contact-order and shared-edge facts

Write `S=V(B) intersect V(L)`, `m=|S|`. Both cycles are induced, so the graphs
they induce on `S` agree. In particular, a pair of contacts is adjacent in `B`
if and only if it is adjacent in `L`, and that is the very same original edge.
There are no geometrically distinct parallel copies of that edge in `G`.

The closed disk `D_L` lies in the closed outer disk `D_B`. The two boundaries
can therefore meet only tangentially at their shared vertices or along their
shared edges. Their contact orders agree up to a global reversal. One proof
is the crosscut criterion: arcs of a Jordan curve in a disk cannot join
alternating boundary endpoints without intersecting. Applying it to the
successive contact arcs of `L` rules out any non-circular ordering of three or
more contacts. For two contacts, the additional datum is which of the two
`L` arcs borders each outer arc; the contact set alone does not determine this.

Orient both geometric disk boundaries consistently for this paragraph. Along
every shared edge they run in the same direction: the interior of `D_L` must
be on the same side of that edge as the interior of `D_B`. Each pair of matched
successive contact arcs then either consists of the same shared edge, leaving
no two-dimensional complementary region, or consists of two internally
disjoint paths which bound one cap. These are actual closures of components
of `int(D_B) minus D_L`; they are not inferred merely from abstract masks.
For `m>=2`, their boundaries are simple whenever the matched paths are not a
shared edge. No further contacts can occur in the interiors of those paths.

If three contacts form a common consecutive path `p-q-r`, the original inner
sector at `q` is filled by the two star faces `pqv` and `qrv`. There is no sector
left for another incident edge. Thus `N_G(q)={p,r,v}` and `deg_G(q)=3`, contrary
to the frozen boundary-degree bound. This excludes every shared path of length
at least two, not just a drawing with no additional edges shown.

## 3. Exhaustive contact table with named representatives

The following table uses `B=(a,b,c,d,e)` throughout. Both listed cycles have
the same geometric orientation. The new letters `x,y,z,w,t` denote distinct
original interior vertices, and all of them are distinct from `v`. A cap
boundary may be reversed without changing its set of named positions, provided
the relation and all attachments are transported with that reversal.

| m | Contact type | Representative L | Actual complementary regions / boundary walks | Source consequence |
|---|---|---|---|---|
| 0 | no contact | `(x,y,z,w,t)` | annulus, boundary components `B` and `L` | remains open |
| 1 | one point | `(a,x,y,z,w)` | one pinched region, boundary walk `(a,b,c,d,e,a,w,z,y,x,a)` | remains open |
| 2 | adjacent contacts | `(a,b,x,y,z)` | shared edge `ab`; one C8 cap `(b,c,d,e,a,z,y,x)` | remains open |
| 2 | nonadjacent; short matched short | `(a,x,c,y,z)` | C4 `(a,b,c,x)` and C6 `(c,d,e,a,z,y)` | remains open |
| 2 | nonadjacent; short matched long | `(a,x,y,c,z)` | C5 `(a,b,c,y,x)` and C5 `(c,d,e,a,z)` | remains open under Task A bounds |
| 3 | three consecutive | `(a,b,c,x,y)` | shared path `a-b-c`; C6 `(c,d,e,a,y,x)` | impossible: `deg(b)=3` |
| 3 | edge plus isolated contact | `(a,b,x,d,y)` | shared edge `ab`; C4 `(b,c,d,x)` and C4 `(d,e,a,y)` | excluded by replacement bound 9 |
| 4 | four consecutive | `(a,b,c,d,x)` | shared path `a-b-c-d`; C4 `(d,e,a,x)` | impossible: `deg(b)=deg(c)=3` |
| 5 | both cycles equal | `(a,b,c,d,e)` | no cap; original graph is the five-wheel | impossible: each boundary degree 3 |

This is an exhaustive table, not a claim that each surviving row has an actual
outside-`K` source. For a subset of a five-cycle: size 2 means an edge or a
nonedge; size 3 means a consecutive path or an edge plus an isolated vertex;
size 4 means a consecutive path of length 3; size 5 is the whole cycle. The
shared-edge and circular-order facts force the displayed `L` contact graphs.
For two nonadjacent contacts the outer and link arc lengths are each `{2,3}`;
the only two physical matchings give `{4,6}` or `{5,5}`. For an adjacent pair,
the length-1 arcs are the very same edge, so the remaining lengths are `4+4=8`.
They cannot be freely re-paired to fabricate smaller caps.

To instantiate the table in a source, select its actual outer labels, actual
link labels, and matching arc sides, then transport every table symbol and
every incidence together. A rotation or reflection used as a D5 simplification
acts on the entire named source, including `B`, `L`, `v`, all attachments, and
all relation coordinates. It is not permissible to normalize `B` and `L`
independently. The table does not prescribe an independent relabeling of a
given source.

In particular Task C writes `B=(a,b,c,d,e), L=(a,x,c,y,z)` with the link in the
opposite geometric orientation to this table. Its explicitly specified cap
boundaries `(a,b,c,y,z)` and `(a,x,c,d,e)` select the C5+C5 row. There is no
contradiction with this table's C4+C6 representative bearing a similar tuple:
the actual rotation and arc pairing are essential. No Task C conclusion is
used here.

## 4. Region ownership, possible chords, and non-disk cases

Keep the wheel, all original outer edges, and their common identities as a
fixed skeleton. Every other original edge has its open drawing in exactly one
complementary region. It belongs to that region even if both endpoints are
skeleton vertices. Every nonskeleton vertex belongs to exactly one open
region. An edge cannot join private vertices of different caps, or a cap
private vertex to a pin outside that cap boundary: it would cross a skeleton
edge or pass through a vertex without that vertex being its endpoint. The
same statement applies to whole components and bridges and determines their
ownership from the original embedding.

A cap patch consists of all vertices and edges in its closed region, with
its stated boundary edges. It is a geometric subgraph, not necessarily the
induced graph on that vertex set. In the adjacent-contact C8 row, `ab` belongs
to `B` and the fixed wheel; it is not in the C8 cap even though its endpoints
are cap pins. This is the principal shared-edge case that an induced-subgraph
description would get wrong. When two patches include a common boundary edge,
both copies impose the same proper-color inequality, and the assembled simple
graph retains a single original edge identity.

An original chord of a simple cap cannot join two nonconsecutive `B` vertices
or two nonconsecutive `L` vertices, because both are induced. At a contact pin,
every other cap pin belongs to at least one of those two cycles. Consequently
every possible additional cap-boundary chord joins a `B`-exclusive pin to an
`L`-exclusive pin. Such chords must lie in that cap with the original rotation,
must not cross, and any triangle they create must be facial (have no vertex
strictly inside). The precise endpoint families in the still relevant rows
are:

| Region | B-exclusive pins | L-exclusive pins | Possible chord family before triangle/degree tests |
|---|---|---|---|
| C8 `(b,c,d,e,a,z,y,x)` | `c,d,e` | `x,y,z` | `{c,d,e} x {x,y,z}` |
| C4 `(a,b,c,x)` | `b` | `x` | `bx` |
| C6 `(c,d,e,a,z,y)` | `d,e` | `y,z` | `{d,e} x {y,z}` |
| first C5 `(a,b,c,y,x)` | `b` | `x,y` | `bx,by` |
| second C5 `(c,d,e,a,z)` | `d,e` | `z` | `dz,ez` |
| first m=3 C4 `(b,c,d,x)` | `c` | `x` | `cx` |
| second m=3 C4 `(d,e,a,y)` | `e` | `y` | `ey` |

In fact the sole candidate chord of any displayed C4 cap is impossible in
the conditional source. It divides that cap into two triangles. Neither can
contain a vertex, so its link-exclusive pin has precisely two link neighbors,
the center `v`, and the opposite outer pin as neighbors: degree 4. This
contradicts the interior degree bound. The C4 representative theorem does not
need this extra restriction and may use a representative with a different
internal structure. No analogous unproved exclusion is asserted for the
remaining mixed chord families. For the rejected m=3 path row the analogous
family is `{d,e} x {x,y}`, and for m=4 it is `ex`.

For m=0 the complement is an actual annulus with two disjoint five-vertex
boundary components. Its full interface is the union of those ten named pins.
An original edge from a `B` pin to an `L` pin is a radial connection in this
annulus, not a chord of a C5 disk. More generally choose an actual simple path
`Q` of length `r` from `B` to `L`, with internal vertices off both cycles.
Cutting the annulus along `Q` produces a disk whose boundary has length
`10+2r`: a traversal of `B`, one copy of `Q`, a reverse traversal of `L`, and
the other copy of `Q` in reverse. Every vertex of `Q`, including the endpoints,
has its duplicated boundary occurrences tied to the same original pin by an
equality condition. Those equality constraints and all actual attachments
must be retained. Such a cut neither produces an ordinary C5 disk nor supplies
a five-interior-vertex representative. If the `r-1` internal path vertices are
fixed interface pins, they must also be counted as retained original interior
vertices in any replacement. The ordinary original source is connected, so a
path of the stated kind exists; a shortest route between the two cycles may
be chosen.

For m=1 the two Jordan boundaries touch at `a`. There is one connected open
complementary region. Its closure has the displayed boundary walk of length
10, in which `a` occurs twice before the final closure. A punctured small
neighborhood of `a` in this closure has two sectors, so it is not a closed
disk with a simple boundary. Cutting at the contact produces a disk with two
copies of `a`, which must receive the same color and be glued back in the
original two sectors. This is a pinned, pinched-disk replacement problem, not
an ordinary C5 cap. The shared contact is one original vertex, not two
independently colored vertices. Additional pin-to-pin edges here can only
join `{b,c,d,e}` to `{x,y,z,w}`; their sectors and any resulting subdivisions
must be recorded. In m=0 the corresponding endpoint family is all `B x L`.

## 5. Counts and the precisely bounded consequence

For the region decomposition above, the retained original interior skeleton
vertices are exactly `v` and `V(L) minus V(B)`. Thus

`t = 1+(5-m) = 6-m`.

All private vertices of different replacement patches are required to be
fresh and disjoint. If `h_i'` is the number of private vertices of patch `i`,
with every boundary pin already in the retained skeleton, the assembled
graph has

`k(H) = 6-m + sum_i h_i'`.

This is an exact equality for this replacement convention. Outer pins do not
contribute to `k(H)`; each link-exclusive original pin contributes once even
if it is present in multiple boundary descriptions. Any separately fixed
private contact or cutting-path vertex must be added to `t` explicitly and
removed from the private count. A representative patch need not remain
triangulated or maintain the old degrees: an actual simple disk source with
the same complete outer relation suffices for the contradiction.

| Row | Retained original interior pins and center | Available private-vertex bound | Consequence / exact missing numerical target |
|---|---|---|---|
| m=0 annulus | `v,x,y,z,w,t` (6) | no annular pinned bound inherited | need annular representative `h'<=6` to reach 12 |
| m=1 pinched | `v,x,y,z,w` (5) | no pinched nine-distinct-pin bound inherited | need `h'<=7` |
| m=2 shared edge | `v,x,y,z` (4) | no C8 bound inherited | need C8 `h'<=8` |
| m=2 C4+C6 | `v,x,y,z` (4) | `3+h_6'` | need C6 `h_6'<=5`, or any sum `h_4'+h_6'<=8` |
| m=2 C5+C5 | `v,x,y,z` (4) | `5+5` | only `k(H)<=14`; need private sum at most 8 for the twelve bound |
| m=3 edge+isolated | `v,x,y` (3) | `3+3` | `k(H)<=9`, impossible for outside K |
| m=3 common path | `v,x,y` (3) | no C6 bound needed | already excluded by boundary degree 3 |
| m=4 | `v,x` (2) | C4 at most 3 if considered | already excluded by boundary degree 3; formal count at most 5 |
| m=5 | `v` (1) | no private region | the wheel has one interior vertex and boundary degree 3 |

Every actual C5 cap used above has strictly fewer interior vertices than `G`,
since at least the center `v` and all link-exclusive boundary pins have ceased
to be its interior vertices. Relabel its five boundary positions to the stated
named order. Global minimality therefore puts its complete relation in `K`,
so it has an actual at-most-five representative. The C4 bound applies to each
actual C4 cap without requiring the whole source's relation or an independent
normalization of its colors.

For m=3 edge+isolated, replace its two C4 caps by the inherited at-most-three
representatives, retaining all their named boundary pins and the wheel. Each
can be embedded in its own original cap with the original boundary order;
private vertices are disjoint. The full-interface replacement lemma gives
`Sigma(H)=Sigma(G)`. There are at most `3+3+3=9` interior vertices, so the frozen
`K_{<=12}=K` puts this relation in `K`, a contradiction. This proves the new
conditional geometric restriction

**Every degree-5 interior vertex of the globally minimal outside-K source has
at most two original outer-boundary neighbors.**

It does not close any of the five residual rows with m=0, m=1, or m=2. In
particular the C5+C5 estimate is 14, and Task A cannot replace that number by
12 or import a not-yet-established cap-pair closure.

## 6. Replacement interface check

For completeness, the topological proof uses the following exact form of the
replacement premise. For a patch `P_i`, let `I_i` contain every actual shared
vertex with the fixed exterior, with original labels and identities. Let
`R_i` be the set of all proper four-color assignments on `I_i` that extend to
`P_i`. Equality `R_i=R_i'` is in one fixed color set; no quotient is taken
independently in separate pieces. For each fixed outer assignment `beta`,
the complete set of interface assignments accepted by the glued graph is the
join of the exterior relation with all `R_i`, restricting to `beta` on `B`.

Given an old full coloring, restrict it to the fixed exterior and all `I_i`.
For each `i`, relation equality supplies a new full patch coloring on exactly
those interface colors. Their private vertices are disjoint and all edges are
owned by the fixed exterior or one patch, so they glue to a new full coloring.
The reverse construction uses `R_i'=R_i` in the other direction. These maps
are existential lift constructions, not a bijection of colorings or equality
of fibre cardinalities. They apply to every one of the ten named outer rows,
including empty rows, and to any proper color names in those rows.

The new patches must also admit the stated common-pin embedding in the
original regions, preserve every boundary edge/pin and the required sectors,
and yield a simple graph after removing only duplicate edges with identical
endpoints. Relation equality alone is no guarantee of embedding. In the two
genuine disk caps of the m=3 row, an actual C4 disk representative with the
fixed cyclic boundary provides exactly the required embedding.

If an extra shared pin is omitted and only an outer-boundary projection is
preserved, the failed step is explicit: existence of some new extension with
the same projected colors does not imply existence with the particular color
already fixed at that omitted pin by the exterior. Separate normalization of
the color names has the same defect at multiple shared pins. Keeping a
repeated pin as two unrelated variables additionally changes the graph and
the join. None of these weaker premises justifies the counts above.

## 7. Evidence boundary

The contact classification, full-interface applicability, and the m>=3
exclusion above are conditional paper proofs from the frozen source premises.
This review alone performs no finite coloring enumeration and establishes no
new Lean theorem. Literal diagnostic contact skeletons can illustrate the
listed rotations, but they are not outside-`K` sources and need not satisfy
the source degree bounds. Their existence cannot convert any residual row
into a realized source. The 933/941 source predicate is `not triggered` here;
the general outside-catalogue conjecture remains open.
