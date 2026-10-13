# Independent review of the boundary count

2026-10-12. This review uses the frozen degree-restriction result and the
cofacial normal form. It checks a conditional paper argument; no actual
outside-catalogue graph is supplied or assumed to have been enumerated.

## Premises and status

Let G be a source outside the union-closed catalogue K, chosen with globally
minimum interior count and then maximum edge count. Its named outer cycle B
is a chordless C5. The graph is simple, its bounded faces are triangles, all
interior degrees are at least five, all boundary degrees are at least four,
and there is no occupied separating triangle. Every C4 disk relation has a
representative with at most three interior vertices, in the same ordered
four-vertex colour frame. These are inherited premises, not conclusions of
this review.

Verdict: the no-occupied-C4 lemma, boundary-neighbour classification, exact
count of five double neighbours, and the deep-degree-five identity below
are valid under these premises.

## 1. Replacement followed by counting excludes occupied C4 disks

Take any simple C4 Q in G and its bounded closed disk H. Let t be its strict
interior vertex count. These vertices are interior vertices of G, even when
some vertices of Q belong to B. No strict interior vertex has neighbours
outside H, by Jordan separation.

If t is greater than three, replace H by a C4 representative with at most
three interior vertices. Equality of the full named C4 relation preserves
every outside boundary assignment: restrict one whole-graph colouring to Q,
use the replacement extension in exactly those four colours, and conversely.
Thus the operation preserves the complete original C5 relation and lowers
the global interior count, contradicting minimality. Boundary vertices are
not identified. If a replacement chord duplicates an existing outside edge,
parallel copies may be simplified without changing colourability or the
original outer cycle. The replacement need not preserve the normal form;
minimality ranges over all disk sources.

It remains to rule out t=1,2,3. Let q count diagonals of Q lying in H, let i
count edges between strict interior vertices, and let j count edges between
strict interior and boundary vertices. Triangulation and Euler give

    |E(H)| = 3t + 5,
    i + j = 3t + 1 - q.

Every strict interior degree in H is at least five. Therefore

    5t <= 2i + j = i + 3t + 1 - q,
    i >= 2t - 1 + q >= 2t - 1.

For t=1,2,3 this contradicts i <= t(t-1)/2. Hence every C4 has empty bounded
interior. Boundary diagonals were retained in the count, so this reasoning
does not silently assume that Q is induced.

## 2. Every interior vertex has at most two boundary neighbours

Suppose an interior vertex x has two nonadjacent neighbours a,c on B. Name
the unique two-edge boundary arc a-b-c, so B=(a,b,c,d,e). The simple cycle
Q=(a,b,c,x) bounds a C4 disk whose interior is empty by section 1.

That quadrilateral is triangulated. Its diagonal cannot be ac, since B is
chordless, so bx is an edge. Its two inner faces are abx and bcx. As ab and
bc are boundary edges of G, these two triangles fill the entire disk-side
angular sector at b. No other edge at b can leave this sector without
crossing Q, while the other sector is exterior to B. Thus b has precisely
the neighbours a,c,x, contradicting its degree of at least four.

Consequently any two boundary neighbours of an interior vertex are adjacent
on B. A C5 has no three pairwise adjacent vertices, so every interior vertex
has zero, one, or two boundary neighbours; in the last case they are adjacent.

## 3. Exactly five interior vertices have two boundary neighbours

For each boundary edge ab, the bounded incident triangular face is abx with
x interior: x cannot be another boundary vertex because B has no chords.
Thus each boundary edge has at least one common interior neighbour.

It has at most one. If abx is its facial triangle and y is another common
interior neighbour, the bounded triangle aby contains x. This is an occupied
separating triangle, which is forbidden. Equivalently, two different triangles
on the disk side of the same boundary edge are nested there, and the farther
one contains the third vertex of the facial triangle.

The five resulting common neighbours are distinct. A vertex serving two
different boundary edges would have at least three boundary neighbours,
contrary to section 2. Conversely, every interior vertex with two boundary
neighbours serves their common boundary edge. Hence the number of such
vertices is exactly five.

## 4. The exact deep-degree-five identity

Let D_B be the sum of the five boundary degrees, L the set of interior
vertices with at least one boundary neighbour, and

    E_7 = sum over interior vertices of degree >=7 of (degree-6).

There are D_B-10 edges between B and its interior. The five double neighbours
account for ten of them; all remaining vertices of L account for one each.
Therefore

    |L| = (D_B-10)-5 = D_B-15.

Euler and the minimum interior degree give

    n_5 = D_B-14 + E_7.

Let L_6 be the vertices in L of degree at least six, and let n_5^deep count
degree-five interior vertices having no boundary neighbour. Then

    n_5^deep = n_5 - (|L|-|L_6|)
             = 1 + E_7 + |L_6| >= 1.

Thus a degree-five interior vertex with no neighbour on B necessarily exists.
Its cyclic five-neighbour link is a C5 consisting entirely of interior
vertices. The link is induced: a chord between two nonconsecutive neighbours,
together with the central vertex, would form a triangle whose two sectors
contain other neighbours, so its bounded side is occupied. The five facial
star triangles tile the link disk and its only strict interior vertex is the
central vertex.

This establishes an all-interior induced five-wheel. It does not by itself
provide a smaller source with the same complete original C5 relation.

## 5. Adjacent boundary contacts still have a larger outside interface

For a degree-five vertex with B=(a,b,c,d,e) and cyclic link
(a,b,x,y,z), the wheel shares the edge ab with B. Its complementary disk has
boundary (a,z,y,x,b,c,d,e), a C8. It is not a pair of smaller C5 disks. If a
and b both have degree four, their forced cap diagonals ez and cx remove two
ears, leaving a C6 interface. The inherited C4/C5 replacement lemmas alone
do not supply a complete relation replacement for these C8/C6 interfaces.
The counting argument avoids needing such a replacement by selecting a
degree-five vertex with no boundary contact.

## 6. Additional checked consequence: every other occupied C5 is a wheel

Let Q be a simple C5 distinct from B. Chordlessness of B implies Q uses at
least one interior vertex of G. Consequently its strict interior count t is
less than the global interior count. Its disk relation is in K by global
minimality and has a representative with at most five strict interior
vertices. Replacement in the same named colour frame gives t<=5.

For 2<=t<=5, every strict interior vertex must have a neighbour on Q: it has
degree at least five and at most t-1<=4 strict interior neighbours. Let I be
the graph induced by the t strict interior vertices, with its inherited
plane drawing. Every vertex of I is incident with its unbounded face,
because its edge to Q is disjoint from I except at that vertex, and Q lies
outside I. Thus I is outerplanar and has at most 2t-3 edges.

On the other hand, let q count Q-diagonals inside the disk, i=|E(I)|, and j
count edges between I and Q. Euler gives

    i+j = 3t+2-q,
    5t <= 2i+j = i+3t+2-q,
    i >= 2t-2+q >= 2t-2,

contradicting outerplanarity. Hence t is zero or one. When t=1 the same
inequality forces q=0, and its sole interior vertex is adjacent to all five
vertices of Q. Every occupied C5 other than the original boundary therefore
bounds precisely a facial five-wheel.

This conclusion uses the inherited five-interior catalogue representative
bound in addition to the premises listed in section 1. It is a structural
restriction and still does not remove the wheel while preserving its full
relation.

## 7. The boundary degree sum is at least 21

The proposed strengthening is valid. Suppose D_B=20. Since every boundary
degree is at least four, all five boundary degrees are exactly four. Write
B=(b_0,...,b_4), with cyclic subscripts, and let x_i be the unique interior
common neighbour of the boundary edge b_i b_(i+1). Section 3 shows that the
five x_i are distinct.

At b_i the only interior neighbours are x_(i-1) and x_i: they are already
distinct neighbours supplied by its two boundary edges, and its total degree
is four. The triangular fan on the disk side of b_i therefore consists of

    b_(i-1) b_i x_(i-1),
    b_i x_(i-1) x_i,
    b_i b_(i+1) x_i.

In particular x_(i-1)x_i is an edge for each i. Thus
Q=(x_0,...,x_4) is a simple C5. The five boundary-edge triangles together with
the five middle fan triangles are ten distinct faces forming a triangulated
annulus between B and Q. One can verify its topology directly: its outer
boundary is B, its inner boundary is Q, and both vertex lists are distinct
and disjoint. Its open faces contain no vertices. Consequently every interior
vertex of G other than x_0,...,x_4 lies strictly inside Q.

The strict interior count of Q is therefore k(G)-5. The inherited
K_(<=12)=K bound gives k(G)>=13, so this count is at least eight. Since Q is
not B, section 6 allows at most one strict interior vertex, a contradiction.
It follows that

    D_B >= 21,
    n_5 = D_B-14+E_7 >= 7.

This is stronger than the inherited n_5>=6 lower bound. The exact deep-wheel
identity from section 4 remains unchanged. The punctured-icosahedron finite
control has D_B=20 and k=6, so it illustrates the sharp small annulus-plus-hub
case and does not trigger the minimum-outside-source k>=13 premise used here.
