# C8 short crosscuts and the nine-vertex inner core

2026-10-13. BASE `6cafdfb02fe5892a49eee21f92aea2369a25c022`.

The source is the same globally vertex-minimal, then edge-maximal disk-C5 graph G
outside K132, with its ordered original boundary B and its complete relation 933
or 941 in one fixed color frame. Restrict to h=3. The eight named source contracts
and their original collars are unchanged. Write C=(c0,...,c7) for that original
collar, H for C together with its closed inner side, I=V(H) minus V(C), m=|I|,
and Q=H[I]. The original number of inner vertices is k=8+m.

Frozen upstream hypotheses used here are: C is induced; all inner faces of H are
triangles; every C vertex has H-degree at least four; every I vertex has H-degree
at least five; original internal C4 caps are empty; original internal C5 caps are
empty or exactly W5. The last two cap facts use global source minimality and
complete-relation replacement, as proved in the frozen C8-STRUCT geometry note.
Their direct prior proof is also frozen from
`audits/2026-10-12-c5-deep-five-wheel-01a12ffa/REPORT.md`, sections 1-3; the cap
cycles need not be induced.
No edge-critical, N2, Gallai, or epsilon premise is introduced.

## 1. No I vertex joins C vertices at cyclic distance two or three

Suppose x in I is adjacent to c_i and c_j at shortest cyclic C distance d=2 or 3.
Take their short C arc P. The simple cycle P+c_jx+xc_i bounds the cap on the
P side of this crosscut. This is a C4 or C5 entirely inside original B, and the
interior H sector at every strict internal vertex of P is entirely in this cap.
The cap has no original B vertices inside, so the upstream cap theorem applies.

When d=2 the C4 cap is empty. Its unique triangulation diagonal must join x to
the middle C vertex: the other diagonal would be a forbidden C chord. That
middle vertex consequently has exactly three H neighbors, a contradiction.

When d=3 an empty C5 cap also has only one possible triangulation: both diagonals
join x to the two intermediate C vertices, since all other candidate diagonals
are C chords. Both intermediate C vertices then have H-degree three. If the cap
is W5, each intermediate C vertex instead sees its two C neighbors and the W5
center, again giving H-degree three. Both cases contradict the degree bound.

Thus distances two and three are impossible, for arbitrary finite m. This uses
the original edges and their disk sides, not an equality inferred from a chosen
coloring or a necessary count vector.

## 2. At most two C neighbors; eight distinct original third vertices

For any x in I, any two of its C neighbors must have cyclic distance one or four.
Fixing one such neighbor c_i leaves only c_(i-1), c_(i+1), c_(i+4) as possible
others. Any two of these three have cyclic distance two or three. Hence

    |N_H(x) intersect C| <= 2.                                      (1)

Let t_i be the third vertex of the original triangular face at C edge c_i c_(i+1).
Each t_i belongs to I since C is induced. If two distinct C edges had the same
third vertex, that vertex would have at least three C neighbors, contrary to (1).
Thus t0,...,t7 are eight distinct original vertices. Each has exactly its two
displayed C neighbors and no other C attachment.

## 3. At least one vertex lies beyond those eight third vertices

Q is connected. At a C vertex, all its I neighbors form a nonempty path in Q in
the original inner link. Consecutive links share their original edge third
vertex t_i; all vertices of Q meeting C therefore lie in one component. Every
component must meet C since H is connected, proving the claim.

An original edge from x in I to C witnesses incidence of x with the outer face
of Q: its interior avoids Q and reaches the component outside C. If every I
vertex met C, Q would therefore be outerplane. But (1) and d_H(x)>=5 imply
d_Q(x)>=3 for every such vertex. A simple outerplanar graph on at least two
vertices has at least two vertices of degree at most two, a contradiction.
(Complete the outerplane graph to a triangulated polygon and use its two ears.)

Consequently some r in I has no C neighbor. Together with the eight distinct
t_i this proves m>=9, equivalently h=3 implies k>=17. This part is a paper
structural result and uses no finite graph search or coloring computation.

## 4. Equality m=9 has a unique H

Suppose m=9. The eight t_i and the nonattaching vertex r exhaust I. There are
exactly sixteen C-I edges. As each C vertex has its two C neighbors and H-degree
at least four, every C vertex has degree exactly four. Its original inner link
is therefore

    c_(i-1), t_(i-1), t_i, c_(i+1).

In particular, consecutive t vertices are adjacent. The eight C-edge triangles
and eight link triangles form the actual triangulated annulus between C and
the simple cycle T=(t0,...,t7). Its inside contains only r. There are no extra
C attachments. The Q-degree of each t_i is at least three because its H-degree
is at least five and exactly two neighbors lie on C.

There is no chord of T. A purported chord cuts off on the side avoiding r a
triangulated polygon with no inner vertices. This polygon has an ear away from
the chord endpoints: for a triangle it is the third vertex; otherwise its two
ears cannot both be the adjacent chord endpoints. At that ear the complete
inward sector of Q lies in this polygon, giving Q-degree two, a contradiction.

Thus the only possible inner edges of T join r to its vertices. Triangulation
then requires all eight edges rt_i. Therefore Q=W8, and H is uniquely the
C8-to-C8 annulus capped by that W8. Every t_i has H-degree five, r has degree
eight, and every C vertex has H-degree four. The uniqueness is as the original
named, embedded graph; it is not merely a degree-sequence assertion.

## 5. The unique equality core gives complete Sigma=1023 in every contract

Attach this forced H to each of the eight original B-to-C collars. The original
attachment formula is frozen COVERAGE section 2: a_i sees b_i,b_(i+1), private
y_(i,j) sees only b_i, and the C order includes the private vertices in their
original interval order. No additional edge, separately normalized piece, or
row-dependent choice is permitted. The complete resulting graph has 22 vertices,
58 edges, and 37 original inner triangular faces.

`certificate.json.gz` records its original vertex order, all edges, oriented
inner faces, and every full lift for each of the ten fixed literal B rows.
`check.py` reconstructs the original collars directly, checks the oriented
triangulated disk, enumerates all complete lifts in each fixed frame, and
compares the entire certificate including all ten fibres. The common row order
is

    01012 01021 01023 01201 01202 01203 01212 01213 01231 01232.

| Contract | Complete fibre counts in that order |
| --- | --- |
| c15-933 | 90, 60, 62, 22, 26, 24, 48, 46, 16, 20 |
| c18-933 | 90, 48, 46, 26, 22, 24, 60, 62, 20, 16 |
| c04-941 | 52, 26, 20, 40, 44, 34, 64, 54, 28, 32 |
| c07-941 | 40, 26, 28, 52, 64, 54, 44, 34, 20, 32 |
| c15-941 | 90, 60, 62, 22, 26, 24, 48, 46, 16, 20 |
| c18-941 | 90, 48, 46, 26, 22, 24, 60, 62, 20, 16 |
| c20-941 | 22, 60, 16, 90, 48, 46, 26, 24, 62, 20 |
| c30-941 | 26, 48, 20, 90, 60, 62, 22, 24, 46, 16 |

All ten fibres are nonempty in every case, so every resulting complete relation
is 1023, contradicting the asserted 933 or 941 source. This excludes m=9 in all
eight contracts. The enumeration is only the complete-coloring check of the
paper-forced equality graphs; no larger graph generator is used.

Combining sections 1-5 gives

    h=3 ==> m>=10 ==> k(G)>=18.

All eight unbounded contracts remain OPEN. At BASE the general bound was K<=14;
this audit alone does not change it or the common h>=3 and n5>=9 bounds, and it
does not settle unrestricted h>=4 branches. The new arbitrary
size geometry excludes precisely the forbidden distance-two/distance-three
attachments; the additional source-size bound excludes k<=17 within h=3. No
new Lean theorem, unrestricted K bound, or actual 933/941 source is claimed.
