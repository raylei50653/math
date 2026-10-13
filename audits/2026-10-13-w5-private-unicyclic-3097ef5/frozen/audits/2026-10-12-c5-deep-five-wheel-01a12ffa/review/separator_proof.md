# Small separators and an interior five-wheel

2026-10-12. Conditional paper proof; no new outside-catalogue source is
constructed, and this is not a Lean proof.

## Fixed premises

Let `G` be a source outside the 132-relation catalogue `K`, chosen first with
minimum number `k` of vertices strictly inside its fixed named outer C5 `B`,
and then with maximum number of edges. Use the established conclusions:

* `k >= 13`; `G` is simple, with chordless outer C5 and triangular inner faces.
* All original interior degrees are at least five; all original boundary
  degrees are at least four.
* No triangle has a vertex strictly inside it.
* Every C4 disk relation has a representative with at most three interior
  vertices. Every C5 disk with fewer than `k` interior vertices has its relation
  in `K` and hence a representative with at most five interior vertices.

All replacement relations have fixed ordered interface labels and one common
colour frame. Replacing an inside disk by an equal complete interface relation
preserves the complete relation on `B`: a colouring of the complementary disk
extends across one filling exactly when its actual ordered interface colouring
extends across the other. Parallel copies of interface edges are simplified.
There are no vertex identifications between different interface positions.

For a simple cycle `C` drawn in the closed disk, its inside means the side not
containing the exterior of `B`. A proper C5 means `C != B` as embedded cycles.

## 1. A small-patch counting lemma

Consider a triangulated disk with boundary length `b`, with `t` interior
vertices, each of degree at least five within that disk. Write `q` for its
number of boundary chords, `e_II` for its number of edges between interior
vertices, and `e_IB` for its number of interior-to-boundary edges. Euler gives

\[
 E=3t+2b-3,\qquad e_{II}+e_{IB}=3t+b-3-q.
\]

The sum of the interior degrees therefore gives

\[
 5t\le 2e_{II}+e_{IB}=3t+b-3-q+e_{II},\qquad
 e_{II}\ge2t-b+3+q. \tag{1}
\]

If `2 <= t <= 5`, each interior vertex has a boundary neighbour: otherwise
it has degree at most `t-1 <= 4`. The embedded graph `H` induced by the interior
vertices is consequently outerplane. Indeed, the boundary cycle lies in the
unbounded component of the complement of `H`, and an edge from a vertex of
`H` to that boundary shows that vertex is incident with the unbounded face.
The simple outerplanar edge bound, valid also for disconnected `H`, is

\[
 e_{II}\le2t-3. \tag{2}
\]

For `b <= 5`, (1) contradicts (2). For `t=1`, the single interior vertex has
degree at most `b`, so `b=4` is impossible, while `b=5` forces all five spokes.
Euler then leaves no boundary chord. Thus a C4 disk with `t <= 3` and all
interior degrees at least five has `t=0`; a C5 disk with `t <= 5` under the same
degree condition has `t=0` or is exactly a five-wheel with `t=1`.

The degree of a vertex strictly inside any cycle of `G` equals its degree in
the enclosed disk: an edge leaving that disk would cross the cycle. Hence the
lemma applies to the caps below.

## 2. No occupied four-cycle

If a C4 encloses `t>3` vertices, replacement by its at-most-three-interior
representative strictly reduces the original interior count while preserving
the complete relation on `B`. This contradicts the global minimum defining
`G`. Hence `t<=3`, and the small-patch lemma gives `t=0`.

Thus every C4 of `G` has an empty inside. It may bound two facial triangles;
the conclusion concerns enclosed vertices, not the existence of a diagonal.

## 3. Every proper five-cycle is empty or a five-wheel

Because `B` is chordless, a proper C5 contains an original interior vertex.
At least that vertex is on the cap interface rather than strictly inside it,
so its interior count `t` is strictly less than `k`. Its relation therefore
belongs to `K`. Replacing it by a representative with at most five interior
vertices shows `t<=5`, by global minimum of `k`.

The small-patch lemma now gives `t=0` or `t=1`; the latter case is exactly the
five-wheel. In particular, there is no proper C5 enclosing two or more vertices.
The exclusion `C != B` is essential: `B` encloses all `k` original interiors,
so its relation cannot be assumed to lie in `K`.

## 4. Which outer vertices can one interior vertex meet?

Suppose an interior vertex `x` meets two nonadjacent vertices `a,c` of `B`.
Write the shorter outer arc as `a-b-c`. The cycle `a-b-c-x-a` is a C4 and
has no vertex inside. Its inside must be triangulated. The diagonal `ac` is
forbidden by chordlessness of `B`, so the diagonal is `bx`.

The cap occupies the entire interior sector at the boundary vertex `b`.
Consequently its only neighbours in `G` are `a,c,x`, contrary to boundary
degree at least four. Thus every interior vertex has at most two neighbours
on `B`; if it has two, they are adjacent on `B`.

Every boundary edge has a facial triangle with one interior third vertex.
No second interior vertex can meet both ends of this same boundary edge:
two triangles on the disk side of that edge would be nested, and the larger
one would be an occupied triangle. The third vertices for the five boundary
edges are distinct, because one common vertex would have at least three
boundary neighbours. Thus precisely five interior vertices have two boundary
neighbours.

## 5. A degree-five vertex whose whole link is interior

Let `L1` be the interior vertices adjacent to `B`, let `D_B` be the sum of the
five degrees on `B`, and define

\[
 X=\sum_{v\text{ interior},\ \deg v\ge7}(\deg v-6),\qquad
 h=|\{v\in L_1:\deg v\ge6\}|.
\]

The boundary-to-interior incidence count is `D_B-10`. The preceding section
shows that every vertex in `L1` contributes one, with an additional contribution
from exactly five vertices. Thus

\[
 |L_1|=D_B-15.
\]

Euler's previously established degree identity says `n5=D_B-14+X`. Subtracting
the `|L1|-h` degree-five vertices in the first layer gives the exact identity

\[
 \boxed{n_5(V(G)\setminus(B\cup L_1))=1+X+h\ge1.}
\]

So some degree-five interior vertex has no boundary neighbour. Its five cyclic
neighbours are five distinct original interior vertices and form a C5. The
five incident triangles fill its inside, containing only the centre. The rim
has no chord: any chord between nonconsecutive neighbours, together with the
centre, would be an occupied triangle on one of its sides. Equivalently the
neighbourhood is an induced five-wheel entirely away from `B`.

This guarantees the interior five-cycle requested by the next local question.
It does not yet provide a replacement preserving the complete relation.

## 6. The apex sphere has only trivial separators of order at most five

Add one new vertex `A` outside `B`, joined to each of its five vertices, to
obtain the simple sphere triangulation `T`. Every vertex of `T` has degree
at least five.

A triangle avoiding `A` is nonseparating by the inherited no-occupied-triangle
result. A triangle through `A` uses adjacent vertices of `B`, since `B` has
no chord; it is one of the five new facial triangles. Thus `T` has no
separating triangle.

A chorded C4 cannot separate: its chord divides one side into two triangles,
neither of which can contain a vertex. A chordless separating C4 avoiding
`A` would be an occupied C4 of `G`, already excluded. A chordless C4 through
`A` would have form `A-a-x-c-A`, with `x` an original interior vertex and
`a,c` nonadjacent on `B`; Section 4 excludes this. Thus `T` has no separating
C4 either.

A chorded C5 cannot separate: a chord divides one side into a triangle and a
C4. By the preceding results each such small cycle has an empty side, and its
side containing the other arc of the original C5 is nonempty; hence both
pieces on the chord side are empty. (For the C4 piece, that other arc contains
one vertex; for the triangle piece, it contains two.) The original C5 has an
empty side.

Now take a chordless separating C5 in `T`.

* If it avoids `A` and is `B`, the side outside `G` consists of the singleton
  `A`. If it avoids `A` and differs from `B`, Section 3 shows its inside
  consists of one vertex, whose neighbourhood is this C5.
* If it contains `A`, write it as `A-a-x-y-c-A`. Chordlessness forces `x,y`
  to be original interior vertices, and `a,c` to be nonadjacent on `B`. Write
  their short outer arc as `a-b-c`. The short cap `a-b-c-y-x-a` is a proper
  C5 in `G`, so it has zero or one vertex inside. If there is one, the cap is
  a five-wheel, and `b` has only the three neighbours `a,c` and the cap centre
  in `G`, contrary to boundary degree at least four. Hence the cap is empty.
  The short side of the original apex C5 consists exactly of `b`. Its degree
  condition forces both edges `bx,by`; its neighbours in `T` are precisely
  `A,a,x,y,c`, so it is a degree-five vertex.

Therefore `T` has no separating cycles of length three or four, and every
separating C5 has a singleton side. This explicit cycle statement is the
standard internally-six-connected triangulation condition; the terminology
does not mean that `T` is six-vertex-connected. In particular its apex has
degree five. These structural conclusions do not settle `K_infinity = K`.
