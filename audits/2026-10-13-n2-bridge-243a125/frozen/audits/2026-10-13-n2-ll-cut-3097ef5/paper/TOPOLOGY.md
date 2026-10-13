# Same-source leaf minors and LL-CUT+diag

Frozen BASE: `3097ef5be241b7777451a5ef8a663f3987d6b866`.
All inputs used below are the copies in `../frozen/docs/` and the frozen
upstream double-long audit. This note proves the strengthened route on the
three remaining spoke distributions. It does **not** prove that the basic
source-data-only sets S themselves must produce a cut.

## 1. Contract and exact adopted inputs

The source is the full original55 N2 source in the task: a finite simple
planar disk with the original ordered induced boundary C5, complete
Sigma 933/941 or one common D5 image, T4 accepted, every nonboundary edge
Sigma-critical, epsilon two, connected effective H touching all B, exactly
two nonadjacent original complete-degree-five roots r,s, and all other
effective interior vertices of original complete degree four. H minus the
roots has exactly the two original long mixed components P,Q; no unary
component is present. H is biconnected, the two pieces are one-sided, and
all original vertices, edges, contact identities and owners, attachments,
rotation, bridges and branches are retained. Free isolated coordinates
retain their independent four-color product factor.

The following are the precise upstream premises used, not new assumptions:

| Frozen source | Actual premise used here |
| --- | --- |
| `c5_excess_two_arc_spoke_closure.md`, Sections 2,3,6 | All original interior vertices have at most two boundary neighbors, adjacent if there are two; a multiblock piece has a private root-contact in every leaf block. |
| `c5_excess_two_arc_size_bound.md`, Sections 3,4 | Distinct original H-degree-two vertices have distinct boundary-edge attachments; each original piece has only bridge and odd-cycle blocks. |
| `c5_excess_two_n2_diagonal_three_row.md`, Sections 1,3 | Original noncolorable degree lists are tight and decompose into disjoint incident block palettes; a shared contact accepts every diagonal; any original long with at most three root incidences accepts `(D,D)` in at least one designated row. |
| `c5_unary_shield_budget.md`, Section 2 | The two actual supports equal their shield vertex sets; the shields have disjoint boundary-edge sets and forbid external attachments at their interior points. |
| `c5_excess_two_n2_double_long_joint.md`, Sections 2,4 | Basic certified cells and simultaneous row/column matrix capacities, with incidences counted separately for shared contacts. |

The low-incidence escape uses the original leaf-contact theorem, degree-four
lists, at most one ordinary private point per odd cycle, and the global
boundary-edge attachment injection. These are all valid in the present
full source; it is not an assertion about arbitrary local gadgets.
Gallai's degree-list result is used through the already adopted frozen
source, without introducing an external theorem or importing a different
minimal-interior/maximal-edge model. In particular no degree-at-least-five,
`h>=3`, or W5 premise from that different model is used.

Fix the literal rows `q0=01212`, `q1=01202`, `q3=01021`, with `D=3`.
The roots and both original pieces keep this one frame throughout.

## 2. Two original minor lemmas

Let C be either original long and C' the other. Let p,z be adjacent private
vertices of a leaf odd-cycle block of C, or adjacent vertices of its only
cycle block. Assume they are nonshared contacts, each with its one actual
boundary neighbor. Write `C0=C-{p,z}`. The original graph induced by C0 is
connected and nonempty: deleting two adjacent private cycle vertices leaves
the complementary cycle path and all other blocks connected. Each of p,z
has its other original cycle neighbor in C0, including the triangle case.

### K5-H: common actual boundary neighbor

Suppose both p,z have the same boundary neighbor h. No spoke at h is
required. Put `R={r,s} union C'`, which is connected because C' is mixed.
Choose `a in S_C' - {h}` and `b in S_C - {a,h}`. Both choices exist because
both actual supports have at least three vertices. The C attachment at b
survives in C0, since p,z attach only to h. Let A be the boundary a-h arc
avoiding b, and A' the complementary a-h arc containing b. The five bags are

```
{p}, {z}, {h}, R union (V(A)-{h}), C0 union (V(A')-{a,h}).
```

They are disjoint. The fourth is connected by the actual C'-a attachment;
the fifth by the surviving C0-b attachment. The ten pair adjacencies are:

| Pair | Original cross edge |
| --- | --- |
| p,z | Their cycle edge pz |
| p,h and z,h | Their respective original boundary attachments |
| p,fourth and z,fourth | Their respective original root-contact edges |
| p,fifth and z,fifth | Their other respective cycle edges into C0 |
| h,fourth | Last edge of boundary arc A |
| h,fifth | Last edge of boundary arc A' |
| fourth,fifth | First edge of boundary arc A' at a |

Thus the original G has a K5 minor, contradicting planarity. The owners may
be equal or different. No color equality is treated as a graph edge.

### K33-O: different owners

Suppose p is r-owned, z is s-owned, and `k_C^s>=2`. The six bags, grouped by
the two sides of K3,3, are

```
left:  {p}, {s}, B
right: {r} union C', {z}, C0.
```

They are disjoint and connected. The nine original cross edges are:

| Left bag | To r union C' | To z | To C0 |
| --- | --- | --- | --- |
| p | pr | pz | p's other cycle edge |
| s | An original s-C' contact edge | sz | Another original s-C contact edge |
| B | An actual C' boundary attachment | z's actual boundary attachment | A surviving actual C0 boundary attachment |

The last s-C edge exists because s has at least two incidences in C, z uses
one, and p is not s-adjacent. The surviving C0 boundary attachment exists
because C has at least three support points, while p,z together attach at
at most two. This proves all nine adjacencies in the original graph.
If instead `k_C^r>=2`, exchange the names of p,z and r,s. In particular,
when both root incidence counts are at least two, adjacent private contacts
of different owners are impossible.

These two lemmas are genuine original-graph obstructions. Their proof
retains the other long and its actual attachments. They do not apply after
replacing that long by an abstract relation or by a claimed color edge.

## 3. Leaf consequences for actual diagonal fibres

Suppose the complete fibre `F_C(q_i;D,D)` is empty. Then C has no shared
contact. At a private cycle contact the list excludes D, whereas at an
ordinary private cycle vertex the list contains D. By the original
leaf-contact theorem there is a private contact; all private vertices have
the same cycle palette, so every private cycle vertex must be a contact.
It has exactly one boundary neighbor, by original complete degree four.
For a sole cycle there is a contact because C is mixed, and the same
argument applies to all vertices. A failed diagonal therefore has:

- every leaf cycle's entire private path made of contacts, at least two;
- every leaf bridge's private endpoint made of one nonshared contact with
  two adjacent original boundary neighbors;
- no shared contact anywhere in C.

For a single bridge, both endpoints have the latter form. A singleton long
is impossible because every interior vertex has boundary support size at
most two. All statements concern the full fibre, including emptiness, not
a partial coloring at the leaf.

**Permanent-failure consequence PF.** If C fails `(D,D)` in all three
literal rows, it has no leaf cycle and is not a sole cycle. Indeed all
private vertices in such a cycle are contacts, and palette equality says
their actual boundary neighbors have the same color in every row. The
five boundary signatures `000,111,220,102,221` are distinct; thus all those
neighbors are the same original h. Adjacent private contacts contradict
K5-H. For a sole cycle the same proof applies. Hence a permanently failing
long either is a single bridge or has at least two leaf bridges.

This statement uses the same original attachments in all three rows. It
does not identify unrelated boundary points separately in each row.

## 4. Consequences of avoiding every basic cut

Assume the basic sets do not overlap and the basic matrix is feasible in
each designated row. Its capacity inequalities imply

```
k_C^other >= 2  =>  W_C^v subset Z(T_v),
Z(T) = {h : q_i(h) belongs to q_i(T) for all i in {0,1,3}}.
```

For example a safe P row fixes all its entries to zero, while its lower
bound is `k_P^s-1`; this is impossible if `k_P^s>=2`. The Q case follows by
the complementary upper bound and the exact root degree equation. Thus
this is a consequence of the **basic** matrices, not an extra acceptance
cell. In the fixed frame:

```
Z(empty)=empty; Z({h})={h};
Z(12)=124; Z(40)=024;
Z(e)=e for the other three boundary edges e.
```

When a root has two spokes in the remaining {3,3} support domain, those
spokes form the unique unused boundary edge e. For either long C,
`Z(e) intersect S_C` is an independent subset of B: normally its only
point is the support endpoint on e; for e=12 or 40 it may additionally
contain the common endpoint of the two shields. These are the two
nonadjacent endpoints of the three-vertex support. In particular this
intersection contains no original boundary edge. This finite literal-frame
fact is checked for all five placements, without normalizing q rowwise.

## 5. All (1,1) spoke distributions: strengthened closure

Write the single spoke sites as h_r,h_s. If C has at least two incidences
at each root, Section 4 gives `W_C^r subset {h_r}` and
`W_C^s subset {h_s}`. A failed diagonal has no leaf bridge, because its
private contact needs two boundary neighbors belonging to the owner's W.

In a leaf cycle, every private vertex would be a contact. Two consecutive
ones with the same owner share that owner's h and contradict K5-H. Two
with different owners contradict K33-O. There are at least two consecutive
private vertices, so no leaf cycle is possible either. The sole-cycle and
sole-bridge cases obey the same arguments; a singleton is not long.
Therefore every such C accepts `(D,D)` in **all three rows**. This includes
shared C directly by slack. Call this conclusion HH11.

The incidence totals at both roots are four. If no piece has at least two
incidences at both roots, the only possibility, up to exchanging P,Q, is
`P=(1,3), Q=(3,1)`. Its 3-by-3 basic matrix has

```
sum M >= 3*(3-1)=6  but  sum M <= 3*1=3,
```

so it was already cut. Otherwise either both pieces satisfy HH11, or one
does and the other has at most three total incidences. In the latter case
the adopted low-incidence escape gives a diagonal lift of the other piece
in one row; HH11 supplies its partner in that exact same row and pins.
Thus all remaining {3,3} and {3,4} supports with spokes (1,1) are excluded
by **LL-CUT+diag**, without a size bound.

## 6. All (2,1) spoke distributions: strengthened closure

The r incidence total is three, so name pieces with `k_P^r=1,k_Q^r=2`.
The s total is four. If `k_P^s=3`, the 2-by-3 matrix gives the basic cut

```
sum M >= 2*(3-1)=4  but  sum M <= 3*1=3.
```

Otherwise `k_P^s<=2` and `k_Q^s>=2`. By Section 4,
`W_Q^r subset Z(T_r) intersect S_Q`, an independent set, and
`W_Q^s subset {h_s}`. Neither owner can supply the adjacent pair needed by
a leaf bridge in a failed diagonal.

Under a failed diagonal, each leaf cycle has a private path of contacts.
K33-O forbids consecutive contacts with different owners; hence that entire
private path has one owner. If it is s-owned, two consecutive contacts have
the same sole boundary neighbor h_s, contrary to K5-H. Thus every leaf
cycle would use at least two r incidences. A multiblock piece has at least
two leaf blocks, requiring at least four r incidences, contrary to
`k_Q^r=2`. A sole cycle has all its vertices contacts; K33-O forbids changes
of owner around it, contrary to Q being mixed. A single bridge is already
excluded and a singleton is not long. Therefore Q accepts all three
`(D,D)` cells. P has at most three incidences, so its existing escape joins
with Q in the same literal row. This proves LL-CUT+diag throughout (2,1).

## 7. All (2,0) spoke distributions: strengthened closure

Again name `k_P^r=1,k_Q^r=2`; now the s total is five. If `k_P^s=4`, the
2-by-4 matrix already gives

```
sum M >= 2*(4-1)=6  but  sum M <= 4*1=4.
```

Otherwise `k_Q^s>=2`. Section 4 gives `W_Q^s=empty` and
`W_Q^r subset Z(T_r) intersect S_Q`, an independent set. Thus a failed
diagonal has no leaf bridge; every private contact of a leaf cycle would
be r-owned. Each such leaf uses at least two r incidences, so the two
leaves of a multiblock piece exceed `k_Q^r=2`. In a sole cycle every vertex
would be an r-contact, contrary to mixedness. Hence Q accepts `(D,D)` in
all three rows.

If `k_P^s<=2`, P has at most three incidences and the existing escape
finishes. The only remaining case is `P=(1,3), Q=(2,2)`. If P accepts a
designated diagonal there is again a joint. Otherwise PF says that P has
only bridge leaf blocks. It is neither a singleton nor a single bridge
(a nonshared single bridge has only two root incidences). There are at
least two leaf bridges. Their private contacts cannot be r-owned, since
`k_P^s=3` makes `W_P^r subset Z(T_r) intersect S_P`, which contains no
boundary edge. Thus they are s-owned.

Their boundary-edge attachments are distinct by the original H-degree-two
attachment injection. The three-vertex support S_P contains exactly two
boundary edges, so the two leaves attach to both of them and
`W_P^s=S_P`. Every consecutive three-vertex boundary arc has a designated
row i using three different colors. As s has no spokes,
`|X_P^s(i)|=3`. Each of the two matrix rows consequently has three forced
zeros from these actual s-contact attachments and at most one remaining
entry. But its required lower bound is `k_P^s-1=2`:

```
2 <= sum_y M(x,y) <= 4-3=1.
```

This is a specific basic row cut, triggered by the actual two original
leaf-bridge attachments. Thus all possibilities in (2,0) are excluded by
the strengthened argument.

## 8. Meaning of the result and its boundary

Define the named strengthened sets by adding only actual complete
diagonal acceptance information:

```
S_C^diag(i) = S_C(i) union {(D,D) : F_C(q_i;D,D) is nonempty}.
```

The additional acceptance statements in Sections 5-7 are proved by the
original degree-list and minor arguments above, not inserted from an
unreported coloring enumeration. If any basic matrix is cut, the basic
theorem gives a same-row complete joint. Otherwise these proofs produce
a row with both actual diagonal fibres nonempty. Consequently
**LL-CUT+diag holds in all three remaining spoke domains**, and excludes
the full original55 double-long source on its full original contract.

**Basic LL-CUT remains unproved as a source-data certificate mechanism.**
The proof uses complete diagonal acceptance which may be absent from S.
An abstract all-three-feasible basic profile is neither a source
realization nor a counterexample. The source exclusion is the conclusion
licensed by the strengthened theorem; it must not be reported as having
shown a basic S overlap or a basic infeasible matrix in every projected
profile. No source has been exhibited and complete-source finite controls
remain `not triggered`.

Each final diagonal join uses one original q_i, the same literal pins
`r=s=D`, both complete original piece tuples and every original spoke.
The roots are nonadjacent; D occurs nowhere on B. The two remaining vertex
sets are disjoint and have no cross edge, by their definition as original
components of H minus the roots. Thus every original edge is checked in
the combined lift, and free-coordinate product factors are retained.

These are arbitrary-size paper arguments. Finite minor/geometry controls
test their stated interfaces and original bags; they do not replace the
proof or certify a complete source. No Lean theorem, source enumeration,
commit, push, PR, issue, or external message is part of this note. Parent
N2 and E-ARC2 classification coverage requires a separate premise check.

## 9. Finite arithmetic evidence

[topology_arithmetic.json](topology_arithmetic.json) records all ten ordered
placements of the two three-point shields, the literal unused spoke edge,
its exact Z closure and each piece's resulting contact sites. Every such
site set is checked to contain no boundary edge, including e=12 and e=40.
The same artifact records the separating three-color rows for each of the
five literal three-point supports, all nine (1,1)-spoke incidence splits,
and the three explicit total-capacity cuts. The latter are independently
checked by enumerating every matrix with the stated bounds; the final
three-forced-zero row cut is independently checked over its sixteen rows.

[topology_checker.py](topology_checker.py) generates this small necessary
boundary interface and replays the exact artifact. It never enumerates or
qualifies source graphs. [topology_verification.json](topology_verification.json)
records normal and `PYTHONHASHSEED=17` success with identical output, and
rejection of the preserved corrupt artifact whose first total lower bound
was changed from six to three. Complete-source finite status stays
`not triggered`; actual original K5/K3,3 bag controls are under `../controls/`.

```bash
python3 -B audits/2026-10-13-n2-ll-cut-3097ef5/paper/topology_checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-n2-ll-cut-3097ef5/paper/topology_checker.py --check
```
