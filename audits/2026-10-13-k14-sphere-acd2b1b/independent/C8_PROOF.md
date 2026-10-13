# C8 equality case: a structural exclusion of fourteen inner vertices

This note uses the same globally minimal, edge-maximal source G, ordered original
C5 boundary B, actual C8 collar C, and original inner disk H as the existing C8
apex theorem. It neither changes G nor identifies colorings from different sources.

## Assumptions and upstream references

The existing source reductions give an induced C8 boundary for H, triangular inner
faces, every C vertex of H-degree at least four, and every strict inner vertex of
H-degree at least five. The five apex inequalities are the result of all forty
original apex-degree-three exclusions; the three other boundary inequalities come
from their single original B attachments. See `docs/c5_c8_apex_degree.md`, sections
1 and 4, and `audits/2026-10-13-c8-apex-degree-45bc1c3/PROOF.md`, sections 1 and 5.
No N2, edge-critical, Gallai, or additional color-count assumption is introduced.

Write I=V(H)\V(C), m=|I|, Q=H[I]. The original number k of vertices strictly inside
B is k=8+m. The existing exact curvature identity is

    n5(I) = 6 + sum_{c in C}(d_H(c)-4)
                + sum_{v in I, d_H(v)>=7}(d_H(v)-6).

Consequently m>=6. We prove that equality m=6 is impossible.

## 1. Equality determines every relevant degree

If m=6, every term on the right beyond 6 must vanish. Therefore all six I vertices
have H-degree exactly five, and all eight C vertices have H-degree exactly four.
The disk Euler formula gives |E(H)|=3m+2|C|-3=31. Each C vertex has two C neighbors
and exactly two I neighbors because C is induced, so |E(C,I)|=16. Hence

    |V(Q)|=6, |E(Q)|=31-8-16=7, sum_{v in I} d_Q(v)=14.

## 2. Every inner vertex has an even number of original C neighbors

For each c_i in the fixed cyclic order of C, its original inner link is the path

    c_(i-1), u_i, v_i, c_(i+1),

where u_i and v_i are distinct I vertices. All three successive pairs give the
original incident triangular faces. In particular, an edge c_i q with q in I
belongs to exactly one triangular face whose other edge is a C edge: if q=u_i it
is the c_(i-1)c_i face, and if q=v_i it is the c_i c_(i+1) face.

For a fixed q in I, pair each incidence c_i q with the other endpoint incidence
of that unique C-edge triangle. This pairing has no fixed points and is an
involution. It uses actual faces of the same H; no generic boundary identification
or relation replacement is involved. Thus |N_H(q) intersect C| is even, and

    d_Q(q)=5-|N_H(q) intersect C|

is a positive odd integer. Since the sum of the six d_Q values is 14, at least one
q has d_Q(q)=1.

## 3. Such an inner leaf is impossible

Let r be q's sole Q neighbor. The other four neighbors of q lie on C. Since q is
strictly internal in a simple triangulated disk, its cyclic link is a simple
5-cycle consisting, in one orientation, of

    r, c1, c2, c3, c4.

In particular, qc1c2 and qc2c3 are distinct original triangular faces. Both c1c2
and c2c3 are edges of C: all four named c vertices lie on the induced C and the
link supplies the edges. They are therefore the two C edges incident with c2.
This makes the original third vertex of both adjacent C-edge faces equal to q.
But section 2 shows that those two third vertices at every c2 are its two
*distinct* I neighbors. This contradiction excludes q.

Thus m=6 is impossible, giving the independent structural improvement

    h=3  ==>  k(G)>=15.

The proof applies to all eight original C8 necessary-condition residuals and
excludes their fourteen-inner-vertex subdomain. It does not exclude an entire
unbounded residual, raise h>=3 or n5>=9, or prove a general K bound by itself.
It is a paper argument using already accepted C8 hypotheses, with no new Lean
formalization and no finite-source enumeration premise.

## 4. The next equality case also fails: m=7

In fact the same original-face argument excludes seven strict inner vertices and
improves the conditional bound further to **h=3 implies k(G)>=16**.

We first record two elementary facts under the original general hypotheses
(induced C, every C-degree at least four, every I-degree at least five).

* Q is connected. The I-neighbors in the inner link of any C vertex form a
  nonempty path in Q. Consecutive C links share their original C-edge third vertex,
  so all those paths lie in one component. Every component of Q must meet C,
  because H is connected; hence there is just that component. This is also the
  argument already recorded in K13-COLLAR PROOF section 4.2.
* Q has no vertex of degree one. The cyclic link of such a vertex would contain
  its sole Q neighbor followed by at least four C neighbors. Three successive C
  neighbors would make the middle one's two C-edge third vertices the same q and
  leave that C vertex with H-degree three. The two original triangular faces at
  the middle vertex fill its entire inner sector, so this contradicts its degree
  bound even when other C vertices have degree greater than four. Connectedness
  and m>=6 also rule out Q-degree zero. Thus every Q-degree is at least two.

For m=7, curvature and the degree lower bounds allow exactly the following cases:

(A) Six I vertices have H-degree five, the seventh has degree six, and every C
vertex has degree four.

(B) All seven I vertices have H-degree five, exactly one C vertex has degree five,
and the other seven C vertices have degree four.

Indeed a strict inner vertex of degree at least seven would contribute at least
one to the curvature excess, requiring at least seven degree-five vertices in
addition to itself, already more than m=7.

### Case (A)

The face pairing of section 2 makes every C-neighbor count even. Hence the six
H-degree-five vertices have odd Q-degree, at least three; the H-degree-six vertex
has even Q-degree, at least two. Euler gives |E(Q)|=10, so the sum of Q-degrees is
20. Equality in the preceding lower bound forces the six Q-degrees to be three
and the remaining one to be two. Consequently their C-neighbor counts are two
and four, respectively: every vertex of Q is incident with its outer face.

For clarity, each original edge from such a vertex to C lies in the component of
the complement of Q containing C and the outside of H, so it witnesses incidence
with this same outer face. Thus Q is a simple outerplane graph. A simple outerplanar
graph on at least two vertices has at least two vertices of degree at most two.
One direct proof is to add edges in an outerplane embedding until it is maximal;
the resulting triangulated polygon has at least two ears (take two leaves in its
triangle weak-dual tree), and their degrees in the original graph are no larger.
Q instead has exactly one vertex of degree at most two, a contradiction.

### Case (B)

At the exceptional degree-five C vertex c*, its original inner link is

    previous_C, u, v, w, next_C

with u,v,w distinct in I. The original C-edge triangles account for all C-I
incidences in fixed-point-free pairs except the single middle edge c*v. Thus every
I vertex other than v has an even number of C neighbors, while v has an odd
number. Since all seven H-degrees are five, six Q-degrees are odd and the last is
even. The no-leaf fact gives a total Q-degree of at least 6*3+2=20.

But there are 17 C-I edges and |E(H)|=34, so |E(Q)|=34-8-17=9 and the actual sum is
18. This contradiction excludes case (B).

Together with sections 1-3 and the upstream m>=6 bound, this proves

    h=3  ==>  |I|>=8  ==>  k(G)>=16.

Both cases use the original degree multiset and original triangular faces. They
add a paper structural constraint on all eight source contracts, without changing
their full-relation upper bounds or combining independently feasible color data.
The eight unbounded residuals, h>=4 branches, and the general conjecture remain
open. No enumeration, external coloring theorem beyond the already accepted
upstream hypotheses, or new Lean result is claimed by this extension.
