# A. A two-face repair across a rotational blocker

BASE `9c36e3c4789dfec07d60ec4e042f0bafe17451d1`.
This independent derivation writes only to the present `A/` directory.
The previous complete two-cycle audit is frozen under
[`../frozen/audits/2026-10-20-r6-two-cycle-repair-9c36e3c`](../frozen/audits/2026-10-20-r6-two-cycle-repair-9c36e3c/PROOF.md).
No external theorem or finite search supplies source existence.

## 1. Literal source and the binary partition

Retain the same globally minimum completed no4ct C5 source, secondary
maximum-edge choice, ordered `(x,y,a,b,c)`, actual original x,y,b degree
four and r degree six, support in `{932,933,941}`, original rotation,
private contacts, complete U319 fibres including empties, complete
`(v,r,x,y,b)` reconstruction and all original r lifts. There is no added
original v-degree-five premise and no independently normalized piece.
The graphs and marked edges remain

`J=U/(s=t), m=[s=t], D=J*`,

`e=(vw)*, f=(pq)*, g=(mz)*`.

Fix the same actual `M in P101` with its two **complete** complement
cycles `D-M=C7 disjoint-union O`. All components below are complete
components of the indicated actual spanning subgraph.

The frozen primal graph `P=(V(J),M*)` has three components: the centre
edge K2 on u,h, the tree T containing vw, and the unicyclic component
U0 containing the rim Q5 and mz. Write b=0 on U0 and b=1 on K2 and T.
The frozen region identification gives exactly

`xy in P iff b(x)=b(y)`.

Every facial triangle has two vertices of one b-value and one of the
other; its unique monochromatic edge is its M edge. J is the original
simple four-connected sphere triangulation, so the dual faces below
are its actual embedded dual faces.

For a vertex set Y, define its original degree charge

`q(Y) = sum_{x in Y} d_J(x) mod 2`.

The complete cycle boundaries immediately give

`q(K2)=1, q(T)=1, q(U0)=0`.                         (A1)

For example K2 has boundary C7; T has boundary O; U0 has both
boundaries, so its degree charge is `7+|O|=0 mod 2`.

## 2. Admissible sets and why single-colour enlargement is limited

For any X, flip b exactly on X and call the result b_X. Set

`Q_X = (delta_J(X))*`.

At a dual vertex, its primal triangle meets delta(X) in zero or two
edges. Those two edges alternate with respect to M exactly when one
is the triangle's unique monochromatic edge. Thus the following are
equivalent:

1. b_X has no monochromatic facial triangle.
2. At every mixed triangle for X, its two cut edges contain precisely
   one P edge.
3. Q_X is a vertex-disjoint union of actual M-alternating cycles.

When these hold, call X admissible and define `N=M triangle Q_X`.
This is an actual perfect matching on the same D, and

`N* = P triangle delta_J(X)`

is exactly the graph of monochromatic edges of b_X. All cycles of
Q_X are switched together, so separate feasibility witnesses are
never assembled.

Conversely, for any actual perfect matching N on D, its symmetric
difference with M is a disjoint union of alternating Jordan cycles.
Choose X by taking the symmetric difference of their primal interior
vertex sets, in the same embedding. Crossing a primal edge changes
this interior parity exactly when its dual edge is in `M triangle N`.
Thus `Q_X=M triangle N`. Connectivity of J makes X unique up to
complement. This general representation covers all actual matchings;
the pair theorem below deliberately restricts X to two specified
adjacent vertices. For the desired marked family one must still
impose `e in N` and `f in N iff g notin N` on that same N.

Call a face a **bad corner at x** when x is its sole b-value; the
face's P edge then avoids x. Let k(x) be the number of such faces.
No facial triangle has both incident edges at x in P. Each P edge
at x lies in exactly two faces, so

`k(x)=d_J(x)-2d_P(x)`.                              (A2)

In particular x has an M-alternating dual facial boundary exactly
when k(x)=0, or equivalently its incident P/non-P edges alternate
in the actual rotation.

If X is contained entirely in one original b-colour, it is admissible
**if and only if** both of the following hold:

* X is independent in P;
* k(x)=0 for every x in X.

Indeed a selected minority vertex alone in its triangle creates a
monochromatic triangle; selecting both majority vertices does the
same. These are exactly the two listed prohibitions. Consequently,
adding any number of vertices of U0 to a safe rim vertex with a bad
corner cannot cure that rotational obstruction. A repair that flips
that rim vertex must also flip vertices of the other original colour.
This is a limitation of this whole one-colour class, not an
obstruction to arbitrary repairs.

## 3. An exact complete-cycle charge criterion

For any admissible X, let `P_X=(V(J),N*)`. The complete cycles of
`D-N` are pairwise disjoint Jordan curves. Their complementary
regions correspond bijectively to the complete components of P_X:
crossing an N edge joins the incident primal vertices without
crossing a complementary cycle, and every region is exhausted by
these adjacencies.

Make a graph R with one vertex per region and one edge per complete
cycle, joining its two sides. Disjoint Jordan curves cut the sphere
successively into one extra region, so R is a tree. This remains
true for nested curves and for annular regions.

For a region/component H, the sum of lengths of its incident
complete boundary cycles is `|delta_J(V(H))|`. Therefore

`q(H) = sum_{C incident to H} |C| mod 2`.            (A3)

For a given complete cycle C, remove its edge from R and let Z
be either full shore, considered as the union of its primal
components. Summing (A3) across that shore cancels all internal
cycle boundaries and gives

`|C| mod 2 = q(Z)`.                                (A4)

It follows that

`D-N has only even complete cycles`

`iff every complete component H of P_X has q(H)=0`. (A5)

The forward implication is (A3). For the reverse implication,
(A4) makes every tree edge even. It would be insufficient to
check only one annular component or to sum all charges globally:
the exact test checks every complete P_X component.

More precisely the complete odd-cycle count is

`sum_{edge C of R} (q(either full shore at C) mod 2)`. (A6)

This counts outer and nested cycles alike.

## 4. The adjacent two-face repair

Let rho be either of the two actual safe rim vertices, r45 or r56.
Let tau be an actual neighbour of rho in `T-{v,w}`. These letters
name one original graph vertex each.

Take `X={rho,tau}`. The edge rho tau is non-P. The two dual faces
corresponding to rho and tau share exactly its dual edge and its
two endpoints. Indeed each shared dual vertex is a primal face
containing rho tau, and the original sphere triangulation has
exactly its two incident faces. The two dual facial boundaries are
simple, so their union is a disk and its full boundary is Q_X.
Thus Q_X is a single simple cycle of length
`d_J(rho)+d_J(tau)-2`.

**Rotation test.** X is admissible if and only if every bad corner
at rho or tau is one of the two actual triangles incident with the
edge rho tau.

To prove it, a triangle containing neither selected vertex is
unchanged. A triangle containing exactly one selected vertex
remains nonmonochromatic exactly when that vertex is not its
minority. A triangle containing both selected vertices always
remains nonmonochromatic, because their original and new b-values
are opposite.

In each of the two shared triangles the third vertex matches
exactly one endpoint's b-value, giving exactly one bad corner at
the other endpoint. Therefore every admissible pair satisfies

`k(rho)+k(tau)=2`,

`d_J(rho)=d_J(tau) mod 2`.                          (A7)

The possible defect counts are `(0,2),(1,1),(2,0)`. In particular
the middle case gives a valid alternating boundary even though
neither individual facial boundary is alternating. Equality of
the counts alone is not the rotation test: all their actual bad
corners must be incident with this same original edge.

The safe rho is distinct from p,q,m,z,v,w, while tau lies in T
and is not v or w. Hence X meets no endpoint of vw,pq,mz. Its cut
avoids e,f,g, so an admissible pair produces `N in P101`.

To state the exact parity test, delete rho from U0 and tau from T:

* A component H of `T-tau` is **untouched** when no vertex of H
  is adjacent to rho in J.
* A component L of `U0-rho` is **untouched** when no vertex of L
  is adjacent to tau in J.

Every component is retained, including isolated vertices and
the full subtrees rooted at the removed rim vertex. These tests
use all actual J neighbours, not only P edges.

**Theorem A2 (two-face conditional repair).** Suppose the rotation
test holds. Flipping the full boundary of the two adjacent dual
faces gives an even-complement `N in P101` **if and only if**
every untouched component in these two lists has even original
degree charge.

Proof. Removing the P edges incident to rho and tau gives precisely
the residual components just listed, plus K2 and the two selected
vertices. The newly inserted monochromatic edges give exactly:

1. One b_X=1 component consisting of rho, K2, and all components of
   `T-tau` touched by rho. It contains K2 because rho is adjacent
   to its actual centre h.
2. One b_X=0 component consisting of tau and all components of
   `U0-rho` touched by tau.
3. Each untouched residual component, individually.

There are no other edges between these pieces: originally every
edge within one b-colour was already a P edge, and the only
vertices changing colour are rho and tau. Their shared edge
remains bichromatic. Item 2 permits tau by itself if no residual
component is touched.

Put `epsilon=q({rho})=q({tau})`, using (A7).
If every untouched residual component has charge zero, the charge
in item 1 is

`q(K2)+epsilon+q(T-{tau}) = 1+epsilon+1+epsilon = 0`,

and the charge in item 2 is

`epsilon+q(U0-{rho}) = epsilon+0+epsilon = 0`.

All components are then even, so (A5) proves that **every** complete
new complement cycle is even. Conversely an odd untouched component
survives as a complete odd-charge P_X component, and (A5) excludes
an all-even complement. This proves both directions.

The theorem can absorb an odd-charge child subtree of rho into
the component of tau, provided that actual subtree has a J
neighbour at tau. An odd untouched child remains an obstruction.
It can also absorb odd pieces of `T-tau` into rho's centre component.
These are complete subtree/component statements and require one
compatible pair; they are not separate marginal conditions.

## 5. Scope and remaining obligation

Theorem A2 is an arbitrary-size conditional construction extending
the single-face rule to a single alternating boundary around two
adjacent faces. It explicitly admits two odd-degree selected
vertices with one rotational blocker each, a case where neither
single facial switch is legal. Theorem A2's complete parity
criterion handles all new external circles.

No argument here proves that a source with both old safe facial
repairs blocked contains a rho,tau satisfying both tests. Failure
of every such pair does not exclude larger sets or several
alternating cycles. The general same-source two-cycle repair,
joint even positivity `W110+W101>0`, `omega_e=0`, complete319 and
a strictly smaller bad source remain OPEN. Source realizability
is `not triggered`, and no new Lean theorem is claimed. The
established fixed-r6 lower bound k>=25 and complete reconstruction
cost k+5 are unchanged.

## 6. Independent finite cross-review

[check.py](check.py) imports no C checker functions. It independently
walks every directed edge of C's fixed rotation, reconstructs the
entire primal dual and all triangular faces, recursively enumerates
every perfect matching, and compares complete complement components
with the original-degree component test. It then checks the actual
bad-corner condition and exact untouched-component criterion for all
eligible safe-rim/T pairs in those controls.

The seven fixed controls have 275 complete perfect matchings. The
checker tests ten graph-level adjacent-pair candidates, including one
locally rejected candidate in the weak nonliteral control. Its nine
literal candidates agree with C. Six pairs are admissible; three pass
the complete parity test and three fail it. In the `literal_both_outside_blocked`
control, the degree-five pairs `{5,8}` and `{6,8}` leave complete
lengths `3,19` and `11,11`, respectively. The alternative pair `{6,9}`,
of original degrees five and three, gives a complete even 22-cycle.
Thus legal paired alternation alone is still insufficient, and the
successful weak example does not trigger the source degree bounds.
The other two successful pair controls have degrees five/three and
six/four. Two controls also have parallel primal edges; those are
explicitly weak graphs, not instances of the original simple J.

Normal and seed-17 replay are byte-identical in
[independent-check.json](independent-check.json) and
[independent-check-seed17.json](independent-check-seed17.json).
Deleting a matching row and changing the fixed rotation are both
rejected by the independent reconstruction. The source status of
every finite control is `not triggered`; no original complete fibres
or r lifts are claimed by this review.
