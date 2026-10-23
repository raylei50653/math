# C9 prerequisite: one literal W5 ear or an induced boundary

2026-10-13. Research BASE `6943561e644e7598342d1ccd7df44dac0ebcd5cf`.
This proof applies to the globally smallest source outside K, then maximum
number of edges, in the full original disk-C5 class. It is not a statement
about a separately minimal fixed mask. No Four Colour Theorem is assumed.
All inputs are frozen in the parent audit's [INPUTS](../../INPUTS.json).

**Result.** If the original boundary excess is h=4, the actual inner C9 is
either induced or has exactly one chord. In the latter case that chord cuts
off a W5 whose three short-arc middle vertices are original apices. The
remaining disk has the literal long C6 as boundary. This is a structural
prerequisite for complete transfer queries, not an exclusion of h=4 sources.

## 1. Exact inherited hypotheses

K is the fixed catalogue of 132 complete C5 relations, with witnesses having
at most five inner vertices. Assume a source outside K exists; choose its
original inner-vertex count k globally smallest, then maximize edges. The
frozen [handoff](../../frozen/docs/tasks/c5_no4ct_handoff.md) and the
[collar report](../../frozen/audits/2026-10-13-c5-no4ct-collar-6cafdfb/REPORT.md)
give a simple 2-connected near-triangulation G, chordless named boundary
B=(b0,...,b4), no occupied separating triangle, and no length-two crosscut
between nonadjacent B vertices. After one joint D5 transport of G, B and all
rows, its complete relation is one of 932, 933, 941. In particular k>=16,
every original inner vertex has degree at least five, and every B vertex
has degree at least four.

Let e_i=d_G(b_i)-4 and sum e_i=h=4. The actual first collar has five distinct
apices a_i, one for each original edge b_i b_(i+1), and four distinct y
vertices, each touching only its named original b_i. Its exact cyclic order
is inherited from the original rotation:

```
C=(a0, y_(1,*), a1, y_(2,*), a2, y_(3,*), a3,
      y_(4,*), a4, y_(0,*)).
```

Write A={a0,...,a4}, Y for the four y vertices, and H for the disk inside C.
H contains all k original inner vertices; I=V(H)\C has m=k-9 vertices.
The actual degree bounds, obtained by removing the original B attachments,
are

\[
d_H(a)\ge3\ (a\in A),\qquad d_H(y)\ge4\ (y\in Y),\qquad
d_H(v)\ge5\ (v\in I). \tag{1}
\]

The frozen [C8 geometry proof §2](../../frozen/audits/2026-10-13-c5-no4ct-c8-6cafdfb/geometry/PROOF.md)
proves the following *original-cap* fact under this same global source
contract, without using h=3: an internal C3 or C4 cap is empty; an internal
C5 cap is empty or exactly W5. Such a cap has s<k private inner vertices,
because its boundary contains original inner vertices. This is the exact
size needed for the restricted C4 representative lemma and the smaller C5
catalogue relation. It is not a universal C4 representation theorem.

## 2. Short chords and the ear dichotomy

Suppose uv is a chord of the actual C9. The shorter C arc from u to v has
length d in {2,3,4}; together with uv it bounds a cap completely inside H.

For d=2 the C3 cap is empty. Its middle C vertex has its entire H inner
sector in that cap, and has H-degree two, contrary to (1).

For d=3 the C4 cap is empty and triangulated. A polygon triangulation has
two nonadjacent ears. The chord endpoints are adjacent in this cap, so
some ear is a short-arc middle vertex; its full H-degree is two. For C4
this can also be checked directly from its single diagonal. This again
contradicts (1).

For d=4 the short cap has boundary C5. An empty triangulated C5 likewise
has an ear distinct from the endpoints of its distinguished edge uv,
and would force full H-degree two. Therefore the short cap is exactly W5.
Name its unique center z. If the short arc is

\[
(u,w_1,w_2,w_3,v),
\]

its original edges are exactly this path, uv, and the five spokes from z.
Each w_j has its entire inner H sector in this cap, so

\[
d_H(w_j)=3,
\]

and hence w_1,w_2,w_3 all belong to A, by (1). They have original G-degree
five; z also has original G-degree five. These are actual original
vertices and a single actual cap, not row-dependent witnesses.

There cannot be two distinct C9 chords. To see this without an embedding
enumeration, rotate a first chord to (c0,c4), whose short-arc middle
vertices are c1,c2,c3. A distinct distance-four chord drawn without
crossing it must lie in its long arc (c4,c5,c6,c7,c8,c0): the short arc
has only four edges, so a second distance-four chord there would be the
same chord. On the long arc, the only distance-four possibilities are
(c4,c8) and (c5,c0). Their respective short-arc middle sets are
{c5,c6,c7} and {c6,c7,c8}, both disjoint from {c1,c2,c3}. Either would
require six distinct members of A. There are only five. Thus

\[
\boxed{H[C]=C9\quad\text{or}\quad H[C]=C9+uv
\text{ with one literal W5 short-side ear.}} \tag{2}
\]

In particular, if this named C9 has no three consecutive A vertices,
it is induced. The general h=4 contract does allow three consecutive
A vertices, so (2) does not justify imposing induced C9 in every query.

## 3. Exact eligible named ears and literal row mask

For an ordered e with sum e_i=4, an eligible ear is determined by a run
of three consecutive apices on C. Its chord joins the two C vertices
immediately outside that run. There are five possible cyclic apex runs.
For any selected run, the two intervening e gaps must be zero. The other
three gaps sum to four, so there are binomial(6,2)=15 ordered choices.
Consequently the full named local interface has

\[
\boxed{\binom{8}{4}=70\text{ collars and }5\binom{6}{2}=75
\text{ eligible }(e,uv)\text{ ear positions}.} \tag{3}
\]

The numbers of collars with respectively zero, one, two, or three eligible
ear positions are 20, 30, 15, 5. For a direct count, collars with one
positive gap number 5 and have three adjacent pairs of zero gaps. With
two positive gaps, each of their ten positions has three positive
compositions of four: adjacent positive positions give two adjacent
zero pairs (15 collars), nonadjacent ones give one (15 collars). With
three positive gaps, each of ten positions again has three compositions:
adjacent zero positions give one eligible pair (15 collars), nonadjacent
ones give none (15 collars). Four positive gaps give the remaining five
collars with no eligible pair. Several positions in one collar are
alternative possibilities: (2) permits at most one of them in a source.
This is a finite interface count, not a count of actual source graphs.

For a fixed literal proper C9 assignment q, the actual ear has a lift
precisely when

\[
q(u)\ne q(v),\qquad
|\{q(u),q(w_1),q(w_2),q(w_3),q(v)\}|=3. \tag{4}
\]

Necessity follows from the original chord and the center's adjacency to
all five short-cap vertices. Conversely (4) permits exactly one center
color, the fourth color absent from the C5. All spokes are then proper.
The five-cycle is odd, so under the chord inequality it cannot use two
colors; therefore the equivalent test "at most three colors" is safe
only while retaining that original chord inequality.

Let E_uv be the complete set of proper literal C9 rows satisfying (4),
including all disallowed rows as empty fibers. In the one-ear case the
actual complete relation S=Sigma_C(H) obeys S⊆E_uv. The C9 annulus
transfer remains exact: every inner literal assignment is glued to the
same literal assignment of the original collar, with no independent S4
normalization of pieces. A necessary-support calculation may intersect
its upper bound with E_uv and run noncrossing Kempe deletions. It must
not regard a surviving support as a realized H.

The unique-center statement is a full-lift fact for this cap. It does
not assert that arbitrary cap replacement preserves lift counts.

## 4. The actual residual C6 and full separator join

Delete z,w_1,w_2,w_3 from H. The remaining disk L has the original long
arc from v to u together with the original chord uv as its named C6
boundary D. Its actual triangulated faces and inherited embedding are
kept. Its sizes are

\[
|V(L)|=k-4,\qquad |V(L)\setminus D|=m-1=k-10. \tag{5}
\]

There are no D boundary chords, since any such edge would be a second
original C9 chord. The four long-arc middle vertices keep their full
H degrees, so their A/Y bounds are still three/four. Each endpoint loses
only its short-arc neighbor and z when passing from H to L. Nevertheless
each endpoint has L-degree at least three: an endpoint of degree two
in a triangulated chordless C6 would force an edge between its two D
neighbors, which is a D boundary chord. At least two of the four
long-arc middle vertices are Y, since four Y vertices exist and at most
two can be the endpoints. The strict inner L vertices have their
original G degree at least five. These precise bounds do not give
degree four at all six D vertices.

Let P be the original B--C9 annulus together with this actual W5 ear.
For a fixed literal outer row p and a fixed literal proper D assignment r,
retain the *full* patch fiber F_P(p,r), including empties. The original
graph is exactly P∪L with common vertex set D; the original edge uv is
shared and is retained as a properness requirement in both parts. Hence

\[
\mathcal F_G(p)=\bigsqcup_{r\text{ proper on actual }D}
\mathcal F_P(p,r)\mathbin{\Join}_r\mathcal F_L(r). \tag{6}
\]

The join identifies the six original named vertices and their literal
colors. Restricting a full G lift gives the necessary direction;
joining the two full lifts gives the sufficient direction, since all
original edges lie in P or L. Distinct r give disjoint full lifts.
Equation (6) neither replaces a C6 relation by a C5 catalogue mask nor
forgets the original chord.

## 5. Source-relative equality quotients

The frozen [no4ct dependency report](../../frozen/audits/2026-10-13-c5-no4ct-dependency-6cafdfb/REPORT.md)
and [C8 geometry §4](../../frozen/audits/2026-10-13-c5-no4ct-c8-6cafdfb/geometry/PROOF.md)
show, in this fixed global source contract, that every loopless planar
graph with at most k+5 vertices is four-colorable. An uncolorable graph
of N<=k+5 vertices would descend to a 932 C5 source having at most
N-6<k inner vertices. This contradicts global source minimality; it is
not an invocation of universal planar colorability.

If two distinct vertices on the outer face of actual H are nonadjacent,
joining them through that face and contracting the added arc gives a
loopless planar quotient on k-1 vertices. Its coloring lifts to one
complete coloring of the same H in which the two named vertices have
the same literal color. More generally, let pi be a noncrossing
partition of the actual C9 whose blocks are independent in **actual**
H[C]. Drawing disjoint block trees outside C and contracting them
produces a loopless planar quotient on k-9+q vertices, where q is the
number of blocks. Thus the actual complete H extension counts satisfy

\[
\sum_{r\text{ proper on actual }H[C],\ r\text{ constant on each pi block}}
x_r>0. \tag{7}
\]

Different blocks may receive the same color. The quotient's vertices
are at most k, so the source-relative bound applies. In the ear branch,
a block containing both u and v is not independent, creates a loop,
and cannot be used in (7). Formula (4) also implies that rows violating
the ear mask have x_r=0. Consequently one must test (7) against the
same literal support **and** the ear mask, not against separately
feasible marginals.

The induced C9 branch has every boundary pair except the nine cycle
edges available for this argument. The ear branch has the additional
forbidden pair uv. The actual residual L likewise has source-relative
quotient positivity; a q-block quotient on D has k-10+q<=k-4 vertices.

## 6. Degree budget and stopping boundary

For general H with boundary length n=5+h, strict inner count m, c boundary
chords, j edges inside I, and s edges between C and I, Euler gives

\[
c+j+s=3m+n-3,\qquad
\sum_{v\in C}(d_H(v)-3)=3m-3-j+c\ge h. \tag{8}
\]

In the induced branch H[I] is connected: the inner-neighbor paths
around consecutive boundary vertices meet at each original boundary
edge's third point; every other inner component must attach to this
connected union. Thus j>=m-1 and h<=2m-2. For the h=4 ear branch the
ear center is an isolated H[I] vertex, and L's strict inner induced
graph is connected. At least one such vertex exists since D is
chordless and triangulated. In fact one is insufficient, because then
L=W6 and its four long-arc middle points all have degree three,
contrary to at least two being Y. Therefore m>=3 in both h=4 branches.
This only yields k>=12; the already inherited k>=16 is stronger.

The new result is the complete geometric dichotomy and its literal
interfaces, including the 75 potential W5 ears. It does not raise k,
h or n5, exclude general 932/933/941 sources, or prove K-infinity=K<=5.
No new Lean theorem is asserted. Passing finite necessary queries
does not settle their common-source realizability.
