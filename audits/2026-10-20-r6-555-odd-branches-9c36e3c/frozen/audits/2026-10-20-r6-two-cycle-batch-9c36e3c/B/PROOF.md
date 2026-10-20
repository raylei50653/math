# B. Actual blockers, paired switches, and the complete parity criterion

Frozen BASE: `9c36e3c4789dfec07d60ec4e042f0bafe17451d1`.
Independent write scope: this audit's `B/` directory. The arguments below
were developed from the frozen prior proof and original geometry, before
reading either new A or C output. They are arbitrary-size conditional
theorems and necessary source restrictions, not a universal repair.

## 1. The same source and the adopted geometric facts

Retain the entire original globally minimum completed-source contract:
the ordered C5 frame, its actual rotations and attachments, secondary
maximum-edge choice, complete U319 fibres including empties, every full
original lift and all original r lifts. Work only in

`J=U/(s=t)`, `D=J*`, `e=(vw)*`, `f=(pq)*`, `g=(mz)*`.

Fix the same actual `M in P101` whose complete complement is `C7 ⊔ O`,
with both cycles odd. The frozen
[prior proof](../frozen/audits/2026-10-20-r6-two-cycle-repair-9c36e3c/PROOF.md)
and its
[literal-sector proof](../frozen/audits/2026-10-20-r6-two-cycle-repair-9c36e3c/B/PROOF.md)
identify the actual primal spanning graph

`P=(V(J), M*) = K2 ⊔ T ⊔ U0`.

The centre `K2={u,h}` has degrees four and five. T is a tree containing
vw; U0 is unicyclic, with unique rim Q5 and mz in the tree at z.
Every P edge joins equal values of the same actual weak binary colouring:
K2 and T have value one, U0 value zero. Every triangular face has exactly
one P edge. The two safe rim vertices are `A=r45`, `B=r56`; both
are ordinary, have J degree at least five, and have h as their only
centre neighbour.

The frozen
[source geometry](../frozen/audits/2026-10-20-r6-two-cycle-repair-9c36e3c/B/frozen/j-source-geometry.md)
proves that J is simple and every triangle is facial. In particular the
ends of any edge have exactly its two actual facial third vertices as
common neighbours. Only v,w,p,q can have degree four. No new theorem
about colourability or smaller-source realizability is assumed here.

For any vertex set S define its **degree parity**

`q(S) = sum_{x in S} d_J(x) mod 2`.

All degrees in this definition are the original degrees in this fixed J.

## 2. Full complement cycles and the region tree

This section independently verifies a useful complete-cycle criterion.
It applies to any perfect matching N of this same plane cubic D. Let
`P_N=(V(J),N*)` and retain all of its components, including isolated
vertices if there are any.

The full complement `F_N=D-N` is a disjoint union of embedded simple
cycles. Its complementary regions correspond exactly to the components
of P_N: paths through a primal edge cross an N edge and never an F_N
edge, and conversely the usual dual face adjacency inside a region
connects all its primal vertices through N*.

Make a graph H whose vertices are those regions and whose edge for each
full F_N cycle joins its two incident regions. H is a tree. One can add
the disjoint Jordan cycles successively; each new curve lies in one
existing region and splits it in two, replacing one node by two nodes
joined by the new edge. This proves both connectivity and absence of a
cycle in H, including nested Jordan curves.

For a P_N component S, each primal edge leaving S is dual to one of the
complete cycles incident to its region. No edge of N* leaves S. Hence

`q(S) = |delta_J(S)| mod 2`

`     = sum_{C incident to S in H} |E(C)| mod 2`.             (B1)

If every full cycle is even, every component has degree parity zero.
Conversely, if every component has degree parity zero, take a leaf of
H. Its one incident cycle has even length by (B1). Delete that leaf and
edge and continue. Every edge of H has even length.

Thus the exact equivalence is

> `D-N` is entirely even if and only if every full component of P_N
> has even degree parity.                                      (B2)

The statement checks every component and therefore every complete outer
cycle. Checking only the sum of component parities would say nothing:
that total is always even.

For the fixed original M, the region tree is the three-node path
`K2 -- C7 -- U0 -- O -- T`. Consequently

`q(K2)=1`, `q(T)=1`, `q(U0)=0`.                              (B3)

The first identity also follows directly from `4+5=9`.

## 3. Exact cut admissibility and why the two safe rims do not suffice

Let X be any actual primal vertex set. Toggling the binary value on X
changes the monochromatic edges from P to `P triangle delta_J(X)`.
At an actual triangle, write ab for its unique P edge and c for the
third vertex. With membership indicators `x_a,x_b,x_c`, the new triangle
is nonmonochromatic exactly when

`x_a != x_b`, or `x_a=x_b=x_c`.                              (B4)

Equivalently, if both ends of the original P edge are on one side of
the cut, its third vertex must be on that same side. This condition
simultaneously applies to X and its complement. Merely taking a
one-sided closure is insufficient.

When (B4) holds at every triangle, each nonempty dual cut intersection
contains one M edge and one non-M edge. Thus the dual cut is a
vertex-disjoint batch of M-alternating cycles, and its switch is a
perfect matching. The converse follows at the same individual triangles.

In particular, let t be the actual outer third vertex of the Q5 edge AB.
The two incident triangles of AB are `hAB` and `tAB`; t belongs to T.
If both A and B lie in X, (B4) forces both h and t into X.
Therefore `delta_J({A,B})` is not an alternating batch. The same
observation applies to every selected P edge, including any additional
tree edge added during a proposed larger switch. A construction
containing both safe rims must close these actual triangles and must
also obey the complementary closure condition.

This gives a necessary source restriction on coupled switches; it does
not prove that the required closure avoids e or preserves the f/g
relation.

## 4. An adjacent pair can cross a rotational blocker

Choose one actual safe rim vertex rho and an actual neighbour
`tau in T \ {v,w}`. Their edge is not in P. Put `X={rho,tau}`.
Neither endpoint is any of m,z,v,w,p,q, so its dual cut avoids all
three marked edges e,f,g.

Call a triangle **blocking at x** if x is its minority-valued vertex,
or equivalently neither of its two incident edges at x belongs to P.
The pair cut is alternating if and only if every triangle blocking at
rho or tau contains the edge rho-tau. Indeed, a triangle containing
exactly one selected vertex stays valid precisely when that selected
vertex is not its old minority. Every triangle containing both selected
vertices is automatically valid, since their old values differ.

There are exactly two triangles containing rho-tau. Each is blocking
at exactly one of rho,tau, because the third vertex shares exactly one
of their old values. Thus the criterion implies that the total number
of blockers at the two vertices is exactly two. This count alone is
not sufficient unless their actual locations are checked.

The dual cut is a single simple cycle. The two dual faces for rho and
tau share their one edge, and their only common boundary vertices are
its endpoints: an additional common boundary vertex would be another
primal triangle through rho-tau. Their union is therefore a disk. Its
boundary has length `d_J(rho)+d_J(tau)-2`.

The resulting matching

`N = M triangle delta_J({rho,tau})*`

belongs to P101 whenever the actual blocker criterion holds. In
particular this construction may use two odd-degree vertices, although
neither one alone has an alternating full facial boundary.

## 5. Source degree restrictions for an eligible pair

No two P neighbours of any vertex are consecutive in its rotation:
the corresponding triangular face would be monochromatic. If a vertex
x has k P neighbours and degree d, the number of blocking faces at x is

`b_x=d-2k`.                                                (B5)

For rho, let s be its number of attached U0-tree children. Its P
neighbours are exactly those s children and its two Q5 neighbours.
For tau, its P neighbours are exactly its neighbours in T. Hence

`b_rho=d_J(rho)-2s-4`,

`b_tau=d_J(tau)-2 deg_T(tau)`.                              (B6)

These are exact counts in the original rotation. For an admissible pair
they obey `b_rho+b_tau=2`. If rho is rotationally blocked, the only
possibilities are

| Blocker counts | Original rho degree | Original tau degree | Source lower bound |
| --- | --- | --- | --- |
| `(b_rho,b_tau)=(1,1)` | `2s+5` | `2 deg_T(tau)+1` | `deg_T(tau)>=2` |
| `(b_rho,b_tau)=(2,0)` | `2s+6` | `2 deg_T(tau)` | `deg_T(tau)>=3` |

In the second row, rho's two blockers must be the two faces at
rho-tau. In its rotation they form a run of three consecutive T
neighbours, with tau in the middle. In the first row the two faces
have opposite minority vertices.

Consequently:

* A safe rim with at least three blockers cannot be repaired by any
  single adjacent pair of this form.
* A T leaf cannot be the partner in any admissible pair, even when
  rho itself is unblocked. The leaf has `b_tau=d_J(tau)-2>=3`
  because tau avoids the possible degree-four vertices v,w.
* The admissibility condition forces `d_J(rho)+d_J(tau)` even.

These restrictions concern only this explicitly described pair family.
They do not rule out larger cuts or multi-cycle batches.

## 6. Exact parity test after the pair switch

Assume the actual blocker criterion in section 4. Delete rho from U0.
The remaining components are its s complete child subtrees and the
complete component containing the remaining Q5 path. Call these `U_i`.
Delete tau from T and call its complete components `T_j`.

Say `T_j` is touched if it contains a neighbour of rho other than tau.
Say `U_i` is touched if it contains a neighbour of tau other than rho.
The terms refer to the actual original J adjacency. In particular the
component containing the remaining rim is not assumed touched.

The full components after the switch are exactly:

1. `R={rho} union K2 union (all touched T_j)`;
2. `S={tau} union (all touched U_i)`;
3. each untouched T_j and each untouched U_i separately.

To verify the list, old internal edges of every listed piece are
unchanged. The newly monochromatic edges at rho join it to h and its
old T neighbours other than tau. Those at tau join it to its old U0
neighbours other than rho. The edge rho-tau remains nonmonochromatic.
There are no centre-T incidences and rho's only centre neighbour is h.
No other edge changes membership in P. Multiple incidences to one
touched component do not alter this component list.

The pair is a full even-complement repair if and only if **every
untouched U_i and T_j has even degree parity**. Necessity follows from
(B2). For sufficiency, suppose those parities all vanish. By (B3),

`q(R)=q(rho)+q(K2)+sum_touched q(T_j)`

`    =q(rho)+1+[q(T)+q(tau)]`

`    =q(rho)+q(tau)=0`,

`q(S)=q(tau)+sum_touched q(U_i)`

`    =q(tau)+q(U0)+q(rho)=0`.

The final equality uses even `d_J(rho)+d_J(tau)`. Thus all full
components are even, and (B2) proves that every complete complement
cycle is even. This calculation permits either value for each touched
piece; it does not separately impose evenness on pieces which merge.

This extends the preceding single-face condition: odd-degree branches
may be absorbed into the opposite switched vertex's new component.
Their actual attachment, not just their parities in isolation, decides
whether they are absorbed.

## 7. A coupled degree-five configuration has one exact parity blocker

The source restrictions give a more specific statement about both safe
rims at once. Suppose

`d_J(A)=d_J(B)=5`

and the actual outer third vertex t of AB satisfies

`t notin {v,w}`, `d_J(t)=5`.                                (B7)

By (B6), each safe degree-five rim has no attached U0-tree child and
exactly one blocker. Let their other T neighbours be a and b,
respectively. Thus their rotations have the respective outer runs
`a,t` and `t,b`. The faces `Aat` and `Btb` imply that a,b are T
neighbours of t.

The vertices a,b are distinct. Otherwise their common value would be
a third common neighbour of A and B, in addition to h and t, contrary
to the facial-triangle property. Since t has degree five and at least
two P neighbours, (B5) gives `deg_T(t)=2` and `b_t=1`.
Its unique blocking face is `tAB`. Therefore both pair cuts

`delta_J({A,t})*` and `delta_J({B,t})*`

are automatically M-alternating and preserve all marks.

The two components of T-t are T_a and T_b. In the A switch, A touches
only T_a; U0-A is connected and is touched by t through B. Thus the
only untouched component is T_b. Similarly the B switch has precisely
T_a untouched. Finally,

`q(T_a)+q(T_b)=q(T)+q(t)=1+1=0`.                            (B8)

The two parities agree. It follows that the two pair switches both
give full even complements when the two T branches are even; both
fail when the two T branches are odd.

In the failing case the new primal graph has exactly three components,
with charges `1,1,0`. Its region tree has two edges, so the switched
complement has exactly two complete cycles. By (B2) at least one is
odd. Since the cubic graph D has even order and these cycles cover all
its vertices, their lengths have even sum, forcing both cycles odd.
The charges alone, without this even-order fact, would not determine
both tree-edge parities. There is no omitted additional outer component
in this conclusion.

This is an exact arbitrary-size coupling, not an assertion that (B7)
occurs in an original minimum source. It identifies the remaining
obstruction in this degree-five configuration as two actual odd
branches of the same T. No source theorem supplied here excludes
those two odd branches.

## 8. Scope and remaining obligation

The complete-cycle criterion (B2), pair criterion, untouched-component
parity test and degree restrictions are paper statements for arbitrary
source size. Section 7 proves a coupled special case; it does not
prove that either safe rim or its outer neighbour has degree five.
An arbitrary larger cut still needs all triangle constraints (B4),
the original mark conditions, and even degree parity of every complete
resulting primal component.

Neither simultaneous single-face obstruction nor failure of every
eligible pair is excluded. The general same-source two-cycle repair,
joint even positivity, `omega_e=0`, complete319 and a smaller bad source
remain OPEN. Original source realization is not triggered. This proof
supplies no new Lean theorem, no 4CT invocation, no new complete-fibre
enumeration, and no change to the existing `k>=25` or reconstruction
cost `k+5`.
