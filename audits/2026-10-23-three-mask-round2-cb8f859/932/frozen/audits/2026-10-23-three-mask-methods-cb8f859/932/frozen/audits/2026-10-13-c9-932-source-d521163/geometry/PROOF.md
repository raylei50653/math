# C9-932: a fresh original-apex degree theorem

Scope: the frozen frontier package in this audit, globally smallest number
`k` of original inner vertices among **all** complete C5 relations outside
K, then maximum edges; `Sigma(G)=932` and `h=4`. This is not fixed-mask
minimality. All names, attachments, rotations and literal colors below
belong to one original graph. No C8 apex theorem or C8 counting interface
is an input.

Subject to the finite replay recorded in this audit's counts and review
artifacts, the conclusion is

\[
 d_H(a_i)\ge4\quad(0\le i<5),\qquad k\ge18. \tag{1}
\]

The exact h=4,932 scope is essential. Neither general 932 exclusion nor
any h>=5 assertion follows.

## 1. Original contract and named local geometry

The frozen `c9/geometry/PROOF.md` and `ADOPTION.md` supply the induced
original C9, the complete 20 named residual collars, and the original
small-cap facts. Write the actual inner cycle in its inherited direction
as

```
C = (a0, y1_1,...,y1_e1, a1, y2_1,...,y2_e2, a2,
     y3_1,...,y3_e3, a3, y4_1,...,y4_e4, a4,
     y0_1,...,y0_e0).
```

Here `a_i` touches exactly `b_i,b_(i+1)` outside H, and `y_i_j` touches
exactly `b_i`. The outer excess vector has sum four and is in one of the
source families: two nonadjacent entries equal two; or three consecutive
positive entries with multiset {2,1,1}. No row receives its own choice of
these data. `|V(H)|=k`, `I=V(H)\C` has `m=k-9` vertices, and initially

\[
d_H(A)\ge3,\quad d_H(Y)\ge4,\quad d_H(I)\ge5. \tag{2}
\]

For the candidate apex `a=a_i`, let `u` and `v` be its predecessor and
successor on this **actual** C. Precisely,

\[
u=\begin{cases}y_{i,e_i}&e_i>0,\\a_{i-1}&e_i=0,\end{cases}
\quad
v=\begin{cases}y_{i+1,1}&e_{i+1}>0,\\a_{i+1}&e_{i+1}=0.\end{cases} \tag{3}
\]

Suppose `d_H(a)=3`. Since C is induced, its third neighbor `t` is in I.
The inner sector at a is triangulated, so its two actual H faces are
`(u,a,t)` and `(a,v,t)`. In particular `ut,tv` are original edges. The
complete original neighbor cycle of a is, up to reversing the entire
embedding,

\[
(b_i,b_{i+1},v,t,u), \tag{4}
\]

and its five actual incident triangular faces are

\[
(a,b_i,b_{i+1}),\ (a,b_{i+1},v),\ (a,v,t),\
(a,t,u),\ (a,u,b_i). \tag{5}
\]

All six named vertices `a,b_i,b_(i+1),u,v,t` are distinct. The first,
second and fifth faces are the original annulus faces, including when
u or v is another apex. Thus `d_G(a)=5`. The statement does **not**
specify t's other neighbors: these remain actual vertices of the same H.

## 2. Legal operations and exact budgets

Only deletion of a is needed to establish the counting identity below.
Let `J=H-a`. Removing the two triangles incident with a exposes the
simple boundary

\[
C'=(C-a)\text{ with the path }u,t,v\text{ in place of }u,a,v.
\]

It has length nine, not eight. The vertices u,t,v are distinct, t was
strictly inside C, and the two original faces have disjoint interiors;
therefore their removal gives a plane disk with simple outer boundary
C'. All other vertices, edges and faces retain their original embedding.
J is simple and loopless and has `k-1` vertices and `m-1` strict inner
vertices relative to C'. The original eight C contacts other than a keep
their names; the ninth boundary contact is the original t. In the full G,
deleting a removes exactly its five edges in (4), leaves `k+4` total
vertices and `k-1` original inner vertices, and merges its five incident
faces into one face in the inherited planar loopless disk; all original B names
and surviving annulus attachments are unchanged, but the old annulus
is no longer a complete B--C9 collar. We never claim it is another one
of the twenty sources.

For clarity, the common auxiliary operations have the following separate
contracts. They are not needed to borrow a C8 theorem.

| Operation | Embedding and loop condition | Total vertices and contact map |
| --- | --- | --- |
| Identify any independent noncrossing partition pi of original C in H | Draw block trees outside C and contract them. Induced C makes each independent block loopless; simplify parallel edges. | `k-9+q<=k`, for q blocks; every original c maps to its own named block. |
| Identify u with v in H | They are nonadjacent, at C distance two; an outer-face arc can be contracted without an original loop. | `k-1`; u,v map to one vertex and every other original vertex retains its name. |
| Identify u with v in J | They remain nonadjacent and are cofacial on C'. Contract an outer-face arc and simplify parallels. | `k-2`; same original contact map, with a absent. |
| Add uv to J across its outer face beside the exposed path u,t,v | `uv` was absent by induced C. The new arc completes the empty new triangular face u,t,v, and the long original C arc plus uv is a simple C8. | `k-1`; the eight original C vertices other than a form its boundary, and t becomes strict inner. |

For the final operation the new face `utv` is an auxiliary face, not an
asserted original face. Its C8 disk has `m=k-9` strict inner vertices;
t loses neighbor a and can have degree only four. Its boundary has four
original apices and four original Y vertices, not the five-apex,
three-Y h=3 collar. Its full attachment to original B is missing a.
Thus this legitimate C8 operation fails essential parts of the old C8
source contract, even before comparing the complete row relation. No
old eight-item C8 result applies to it.

Every identification above lies below the same source-relative bound:
the frozen descent lemma guarantees colorability for loopless planar
graphs on at most `k+5` vertices. It does not invoke universal planar
four-colorability. The quotient's coloring pulls back through the
specified original contact map. It is not automatically a coloring
of the original full G. No quotient operation identifies any original
edge's endpoints, and no hidden vertex is added to the stated budgets.

## 3. Exact C9 full-lift degree-three identity

Fix a literal proper assignment `r` to the eight original vertices
`C\{a}` such that `r(u)=r(v)=c`. Let `{i,j,l}` be the other three colors.
For each `d` in this set, let `z_d(r)` be the number of full colorings of
this one J extending r and assigning the original t color d. This is
well defined even when the fiber is empty. The original edges `ut,tv`
force `t!=c`, so these three z values exhaust all J lifts of r.

Let `x_d(r)` be the number of full colorings of the original H extending
r and assigning a color d. Reinsert exactly the original a and its
three H edges. Each J coloring with t color j or l gives precisely one
H lift with a color i; no other J coloring does. Thus, as identities of
full lifts of one graph,

\[
x_i=z_j+z_l,\qquad x_j=z_i+z_l,\qquad x_l=z_i+z_j. \tag{6}
\]

In particular

\[
x_i\le x_j+x_l,\qquad x_j\le x_i+x_l,\qquad
x_l\le x_i+x_j. \tag{7}
\]

The exact integer version also has
`z_i=(x_j+x_l-x_i)/2`, and cyclic analogues, so the sums have the
corresponding parity. The finite exclusion only uses (7); no inference
from parity is needed. In support form, a positive row in this triple
cannot have both other rows zero.

If `r(u)!=r(v)`, t avoids those two colors and the two possible colors
for a exchange the two corresponding J-counts. This gives no additional
triangle inequality and is not used to invent one.

There are 820 proper C9 S4 row orbits, rather than the C8 interface's
274. For an orbit representative p, define `x_p` as the extension count
for that fixed literal representative. One simultaneous permutation of
all four colors is a bijection of full H lifts, so every literal row
normalized to p has the same count `x_p`. To translate (6)--(7), first
form all three literal C9 rows with the same r and then normalize each
entire row. If indices coincide, their algebraic multiplicities must be
retained. There is no separate normalization of r, t, the annulus or an
individual piece; there is no division by an orbit size.

## 4. Why the finite support certificate is a source exclusion

Fix one of the twenty original collars and one of its five named
apices. Assume this apex has degree three. Define all `x_p>=0` using
the same original H. The original annulus gives, for every p, its full
column of possible original B rows, with all empty fibers retained.
Since `Sigma(G)=932`, a positive x can occur only at a column contained
in 932, and the positive columns together must cover every accepted
932 row. In particular the actual support is nonempty.

Every Kempe operation is a swap of actual components of this same full
H coloring. Its boundary partition is one of the generic C9 noncrossing
options; the whole resulting row orbit therefore lies in the actual
support. Likewise (7) is an inequality on the same x. Starting with the
frozen necessary support, either of the following deletion rules
preserves its containment of the actual support:

1. Delete a row when one of its color splits has no allowable whole
   Kempe orbit in the current support.
2. Delete a row in a D3 triple when both alternative rows are absent.

For the second rule, (7) would read `x_p<=0` if the row were positive.
For the first rule, the actual full coloring supplies an allowable
component partition and all its swaps, a contradiction to the deletion
condition. This proves the invariant by induction over every recorded
round. It uses neither independent feasibility of different rows nor
separately selected H graphs.

The new C9-only certificate enumerates all `20*5=100` original
collar/apex hypotheses. Its accepted result is that every final support
is empty. A deterministic replay must check each deletion's literal
indices and its then-current premises, not only the final cardinality.
The original complete relation 932 is nonempty, so no actual H can have
such a support. Together with (2), this proves all five inequalities in
(1), separately for every original named collar.

The original 232 noncrossing quotient positivity conditions are
inequalities on this same x:

\[
\sum_{p:\,p\text{ constant on every block of }\pi}x_p>0. \tag{8}
\]

Their legitimacy is the first row of the operations table, with
`k-9+q<=k`, and the source-relative size lemma. They may be retained in
the joint necessary system. Empty support violates all of them as well,
but they are not a substitute for the D3 or Kempe replay and are not
needed for the final contradiction. No 274-dimensional equality span is
imported. The proof needs only the exact C9 counts, their nonnegativity,
the actual Kempe support implication, (7), and accepted outer-row
positivity. An empty support is an exact infeasibility certificate for
this necessary system and consequently an original-source exclusion of
the specified degree-three hypothesis.

## 5. New C9-only short-contact restrictions and k>=18

After the preceding theorem, every original C vertex has H-degree at
least four. Let x be any strict inner H vertex touching two C vertices.
If their circular distance is two, the short C arc and the two original
x edges bound a C4 cap. That cap is empty under the original source
contract. Its only possible diagonal is from x to the middle C vertex,
because a diagonal joining the arc endpoints would be a C chord.
The middle vertex's full inner H sector is in this cap, so its H-degree
is three, a contradiction.

If the circular distance is three, the analogous cap has boundary C5.
An empty cap must be the fan at x: every other candidate diagonal would
join nonconsecutive original C vertices. Both short-arc middle vertices
then have H-degree three. If the cap is W5, those same two middle
vertices each have just their two cap-boundary neighbors and the unique
wheel center, again H-degree three. Their complete H inner sectors lie
in the cap in both cases. These are all possibilities from the original
C5-cap lemma, again a contradiction. Therefore

\[
 x\in I,\ c_r,c_s\in N_H(x)\cap C
 \ \Longrightarrow\ \operatorname{dist}_{C9}(r,s)\in\{1,4\}.
 \tag{9}
\]

Each original C edge `c_i c_(i+1)` has an actual inner triangular face
with third vertex `t_i`. Induced C ensures `t_i` is in I. If two distinct
edges had the same third vertex, that vertex would touch their endpoint
union. Any two distinct edges of a nine-cycle have among their
endpoints a pair at circular distance two or three, contradicting (9).
The elementary finite fact is checked for all 36 unordered edge pairs
by `geometry/check.py`; its certificate retains an explicit bad pair
for each, rather than only a count. Consequently the nine `t_i` are
pairwise distinct, giving

\[
 m=|I|\ge9,\qquad\boxed{k=9+m\ge18}. \tag{10}
\]

For a precise remaining geometric boundary, every set of C contacts
obeying (9) has size at most three. The allowed triples are exactly

\[
 \{c_i,c_{i+1},c_{i+5}\}\quad (i\bmod9). \tag{11}
\]

Indeed a triple with no adjacent C pair would require all three pair
distances four, impossible because distance-four adjacency forms a
nine-cycle. An adjacent pair c_i,c_(i+1) has only c_(i+5) at allowed
distance from both; no fourth vertex can join this triple. The small
checker enumerates all 512 subsets only to verify this fixed C9 fact.
This is not a source graph search and asserts no realization of any
allowed contact set. In particular, importing the C8 conclusion that
an inner vertex has at most two boundary contacts would be false as an
inference from the presently proved C9 restrictions. Larger caps and
common realization of these remaining contacts are outside this result.

## 6. Adoption boundary

The local faces and identities above are paper statements; the complete
100-case contradiction additionally depends on the new producer and
independent replay of its finite certificate. The old C9 frontier
certificate remains frozen. The small geometry checker validates the
finite nine-cycle endpoint facts in section 5; it does not validate the
source cap theorem by testing graphs.

The result rules out degree-three original apices in the twenty named
h=4,932 sources and raises their conditional original inner-vertex
bound to 18. It neither realizes a remaining source nor excludes all
h=4 sources, and it closes no h>=5 or general 932 branch. No new Lean
theorem or universal planar four-colorability assertion is made.
