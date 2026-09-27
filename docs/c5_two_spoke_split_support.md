# Split-support adjacent (2,1): the complete boundary-row relation

後續（2026-09-27）：[非相鄰 two-spoke 分離](c5_two_spoke_nonadjacent.md)
已證八個非相鄰表項的指定相鄰 p 可延拓，完成唯一 degree-5 的 t=2 出口接合。
下文未解項與數字保留當輪語境；一般單側出口仍未證。

2026-09-24. Dependencies: [support and reflection](c5_two_spoke_reflection.md),
[R10 contact interfaces](c5_degree5_interfaces.md), and the existing
[degree-four block classification](c5_k4_blocks.md). Priority: [HANDOFF](HANDOFF.md).

**Theorem.** Under the split-support source hypotheses below, both contact
orders have the following exact laws, for every proper labeled boundary row b:

```
F_A(b) = {b2}                 if b1=b3, and ∅ otherwise;
F_D(b) = U\{b0,b1,b4}        if b1≠b4, and ∅ otherwise;
Z_G(b) = (U\{b3,b4}) \ (F_A(b) ∪ F_D(b)).                 (1)
```

Consequently `Σ(G)=Ω\{01012}`: all 216 other labeled proper rows extend,
and precisely the 24 color relabelings of q do not. There is no second-missing
disk witness in this class. The formulas include all hub colors, rather than
only Boolean extension. They do not identify different sources' full contact
relations: those remain ordered, source-specific relations as described in §6.

For S={b4,b0}, the result is obtained **only by the established reflection
transport**, not by a second classification. This closes the four remaining
adjacent entries as possible second-missing cores; it does not exclude their
existence. In particular the existing order-I disk witnesses remain valid.

## 1. Source, contacts, and proof boundary

G is a finite simple induced-C5 disk graph with ordered boundary b0,…,b4,
q=01012, connected minimal q-obstruction H, unique complete degree-five
vertex z with N_B(z)={b3,b4}, and all other interior degrees four.
H−z has C₂ with its two distinct ordered contacts (s,t), and C₁ with its
single contact r. By the preceding support theorem, name the components

```
A: F_A(q)={0}, N_B(A)={b1,b2,b3};
D: F_D(q)={3}, N_B(D)={b0,b1,b4}.
```

Either (A,D)=(C₂,C₁) or (C₁,C₂). No component is merged with the other;
no attachments, contacts, or intermediate bridges are silently discarded.
T4 acceptance belongs to the original hypotheses used to reach this stage.
After these supports and q-forbidden sets are established, the proof below
does not need an additional T4 assumption.

The arbitrary-size reduction here **reuses** the earlier degree-four paper
and finite-minor theorems. It is not a new proof of all those theorems, and
is not an extrapolation from the eight small positive controls. The new
finite forms, complete tuples, topology certificates, and row algebra are
in [the checker](../scripts/c5_two_spoke_split_support.py) and
[the artifact](../artifacts/c5_two_spoke_split_support/observations.json).

## 2. A useful consequence of the existing degree-four classification

**Unattached-singleton cyclic lemma.** Suppose a C5 disk minimal obstruction
to a three-color singleton row has all complete interior degrees four,
connected interior, at least one cycle, and no interior attachment to the
singleton boundary vertex. Its interior is either a triangle or two
vertex-disjoint triangles joined by one direct bridge, with no other vertices.
This assertion does not require T4 acceptance.

Here is the precise dependency chain, to distinguish an actual structural
classification from a relation-preserving minor claim.

1. Degree-choosability makes the interior a Gallai tree; the
   [K4 theorem](c5_k4_blocks.md) excludes K4 blocks.
2. [The arbitrary-cycle theorem](c5_multi_odd_cycles.md) excludes long cycles
   and shared cycle vertices and bounds the triangle count by two. Its
   structural statement does not require T4.
3. With two triangles, [the two-triangle theorem](c5_two_triangle_blocks.md)
   says the **actual source** consists of those triangles and a direct bridge.
4. With one triangle, [the fork theorem](c5_triangle_forks.md) excludes
   branching tails. If a path tail exists, the endpoint-minor step in
   [path reduction §2](c5_triangle_path_reduction.md#2-先取-canonical-endpoint-minor)
   produces one of the 18 canonical disk bases. Each such base has an
   attachment to the singleton boundary vertex. This can also be read from
   the root neighborhoods in §3 of that report; the new checker verifies it
   directly on all 18 saved bases. The endpoint minor only deletes spokes
   or contracts interior edges, so it cannot introduce an attachment to a
   boundary vertex that had none. Thus there are no tails.

Only the endpoint-minor necessity is used in step 4, not a claim that an
arbitrary minor preserves a full relation. The later all-row transfer or
T4 corollaries of those reports are unnecessary here.

## 3. Classifying A without changing its contacts

Choose a simple path from z through D to b1, using an original contact and
an actual b1 attachment. Together with z–b3–b2–b1 it bounds the side
containing A. Connectedness and disjointness from D keep all of A on that
side. Suppress the path to z–d–b1, retaining one internal vertex as d,
and delete everything outside the resulting disk. Keep **all** of A,
its edges, its boundary attachments, and its original z contacts.
The new ordered boundary is

```
(z,b3,b2,b1,d), with row (0,1,0,1,2).
```

The dummy d has no A attachment. In this auxiliary disk z is a boundary
vertex; all interior vertices are exactly those of A, still of complete
degree four. F_A(q)={0} says this row is rejected. Every nonboundary edge
is critical by the degree-list slack lemma: deleting an external edge
adds list slack, deleting a nonbridge gives degree slack, and deleting a
bridge gives slack on both connected sides. A cannot be a tree, since
all its boundary lists contain 2 and 3, which properly color any tree.
Thus §2 applies to this **unchanged component A**.

The remaining finite classification retains the named boundary and ports.
For each of the two actual interior graphs, assign each vertex exactly
4−deg_A(v) distinct boundary neighbors among the first four padded
positions. Their q colors must be distinct. Require support all four
positions, one or two contacts at padded position 0, and q-rejection.
These conditions give:

| Actual A graph | Degree/support assignments | q-rejecting | Disk | Contact counts among disk forms |
| --- | ---: | ---: | ---: | --- |
| Triangle | 36 | 36 | 24 | 12 with one, 12 with two |
| Two triangles and a bridge | 1,814 | 914 | 40 | all with two |

These are labeled local lifts, not isomorphism-class counts or a claim that
every form can be coupled to a compatible D in the original source. The 886 nondisk
forms have explicit K5/K3,3 subdivision certificates in their boundary-apex
graphs. Each of the 64 disk forms has an apex rotation with Euler
characteristic two. `--check` checks those certificates without asking a
planarity oracle. The classification covers arbitrary A because §2 gives
the two actual graphs first; it is not a cutoff on a general graph search.

For every surviving form, the checker enumerates the **complete** relation
on its one or two contacts for all 240 labeled rows and all four simultaneous
hub queries. It also retains its padded q edge-deletion colorings. The result
is exactly the first formula in (1). A source's chosen ordering (s,t) is
carried by the graph isomorphism: if the recorded contact order is reversed,
both tuple coordinates are reversed together, never independently projected.

In particular, the previously unknown three-distinct-color input on
(b1,b2,b3) has **no forbidden hub color**, for either contact count.

## 4. The merged row of D: excluding boundary-colored bans

The three-distinct-color input on (b0,b1,b4) is already a permutation of
D's q input. Transport of its whole contact relation gives the second
formula in (1) when b1≠b4. It remains to analyze b1=b4. Normalize these
three boundary values to (0,1,1). Let k=|P_D|≤2.

First, D's contact relation is nonempty on every row: before prescribing
z, a contact has at least one unit of list slack, and connected greedy
coloring applies. Hence `|F_D|≤k`, because every forbidden color must occur
in any one complete k-tuple. Swapping the two unused colors 2 and 3 also
preserves the **whole** relation, so either both are forbidden or neither is.

Suppose a boundary color a∈{0,1} were forbidden on this merged input.
Its tight uncolorable residual lists contain 2 and 3 at every vertex.
Write its block palettes S_K. Independence of the vertex/block incidence
columns implies `2∈S_K iff 3∈S_K` for every block. In particular **no bridge
palette contains 3**. We do not infer a complete cycle classification from
this observation.

Compare with the actual q input and its forbidden query z=3, with palettes
T_K. The presence of color 3 in the vertex lists changes only at the k
original contacts, where it changes from present to absent. Thus

```
Σ_(K contains v) (1_[3∈T_K] − 1_[3∈S_K]) = −1_[v∈P_D].    (2)
```

For clarity, the small-leaf argument is as follows. Keep just blocks with
nonzero coefficient in (2), and their incident vertices. At a noncontact,
there are zero or two active incidences, the latter with opposite signs;
at each contact there is exactly one, of negative sign. Palette disjointness
ensures these are the only possibilities. This is a subforest of the
block incidence tree. Block nodes have degree |V(K)|≥2; vertex nodes have
degree two except for the k contact leaves. A nonempty finite tree has at
least two leaves. With k≤2, the only possibility is one path, with all
block nodes of degree two, hence all active blocks are bridges.
But every initial bridge excludes 3, so its coefficient in (2) is 0 or +1,
never negative. This contradicts either contact leaf. Thus 0 and 1 are
not forbidden. This reasoning also handles k=1, where the leaf count alone
is already contradictory.

For k=1 the unused pair is too large for |F_D|≤1, so F_D is empty. For k=2
there is exactly one remaining possibility to exclude: F_D={2,3}.

## 5. Excluding D's last exceptional pair by a degree-four completion

Suppose k=2 and D forbids {2,3} on the merged input. Retain the original
C5, D, z, both original z–D edges, and z's original spokes b3,b4; delete A.
Call this graph K. It is a disk subgraph of the source. Every interior
vertex, **including z**, now has complete degree four, and its interior
is connected. On the proper row

```
p=(0,1,2,0,1),
```

z's available colors are {2,3}, exactly D's forbidden set. K rejects p.
It is minimal: deleting an edge incident to D releases all D bans by R10;
deleting a z spoke releases 0 or 1, neither forbidden. The singleton of p
is b2, which has no interior attachment in K. Finally its interior has a
cycle, because D is connected and z has two distinct contacts in D.
Therefore §2 applies again, this time to the actual interior D∪{z}.

It is a triangle or two triangles with a direct bridge. Since z has
interior degree two, it is a non-bridge vertex of a triangle. Up to renaming
interior vertices (preserving z and transporting the ordered contacts),
the entire list of candidates is:

```
z=5, contacts=(6,7).
One triangle:  D vertices 6,7; edge 67.
Two triangles: D vertices 6,7,8,9,10; edges 67,68,89,8-10,9-10.
```

All D boundary neighbors belong to {b0,b1,b4}. Completing degree four gives
9 attachment assignments for the first graph and 243 for the second.
For each the certificate retains the complete ordered contact tuples on
both original q and p. **None** has both F_D(q)={3} and F_D(p)={2,3}.
This last contradiction is algebraic; no additional disk filtering is used.
The 252 assignments are a generous cover, including graphs failing other
source conditions. Hence the exceptional pair cannot occur and F_D is empty
on every merged row, completing (1).

This completion is used only inside a contradiction about the same D. It
neither substitutes its independent marginal lists nor modifies A's relation
in the original graph.

## 6. Complete relations, exact join, and single missing

For an arbitrary original source retain four **full** seed relations:
A on Q and on t=(0,1,2,3,1), and D on Q and on p=(0,1,2,0,1).
They have the source's actual ordered contacts and actual attachments.
For A choose the Q seed when b1=b3 and the t seed otherwise. For D choose
the Q seed when b1≠b4 and the p seed otherwise. A color permutation agreeing
on that component's three support vertices transports every complete
coloring, hence its entire seed relation, to R_C(b). Any admissible
permutation gives the same result by the seed stabilizer. These are
bijections on whole colorings; each resulting relation is in the target
row's common color frame before the join.

Thus the retained joint contact relation at every labeled row is exactly

```
J_G(b) = {(a,t_A,t_D) :
  a∉{b3,b4}, t_A∈R_A(b), t_D∈R_D(b),
  every coordinate of both t_A and t_D differs from a}.
```

The product here joins **different connected components after fixing a**;
it never replaces R_C₂ by a product of its endpoint marginals. The 64 A
forms record all their tuples, and the existing source controls retain
both components' complete tuples. D's full seeds remain source-specific;
(1) is not asserted to recover them from their forbidden projections.
Projection of this exact J onto a gives precisely Z_G in (1).

To see the Boolean classification directly, if b1≠b3 then F_A is empty and
D forbids at most one color, while z has two available colors. If b1=b3,
properness gives b1≠b4, so D's forbidden set is one color d outside
{b0,b1,b4}. A forbids b2. These cover both available hub colors exactly
when b0=b2. Together b0=b2 and b1=b3 describe the q orbit among proper C5
rows. This proves the single-missing conclusion in both contact orders.

[TwoSpokeSplitSupport.lean](../Math/TwoSpokeSplitSupport.lean) proves the finite
all-row algebra by ordinary `decide`, conditional on the paper formulas;
it does not formalize the disk or degree-four classification.

## 7. S={b4,b0} solely by reflection transport

Apply the existing rho(i)=3−i and pi=(0 1) to the **same** source, its actual
attachments, its ordered contacts, and every whole-component coloring.
The formalized `contactRelation_transport`, `forbidden_transport` and
`q_contactRelation` in [TwoSpokeReflection.lean](../Math/TwoSpokeReflection.lean)
give R*_C(Tb)=pi R_C(b) and F*_C(Tb)=pi F_C(b). Component roles and contact
orders do not exchange. Reflect the disk embedding as in the preceding report.
Consequently the transported laws, now written in the reflected row, are

```
F_A(b) = {b1}                 if b0=b2, and ∅ otherwise;
F_D(b) = U\{b2,b3,b4}        if b2≠b4, and ∅ otherwise;
Z_G(b) = (U\{b4,b0}) \ (F_A(b) ∪ F_D(b)).
```

The new Lean `reflection_transport` derives the reflected acceptance theorem
from transport and the unreflected classification. There is no independent
{b4,b0} graph enumeration. The checker verifies the row images and full
A-tuple transport as controls of the same formalized operation.

## 8. Trust, validation, and remaining work

Evidence layers are: inherited paper topology/minor theorems and external
degree-list characterization; the new paper completion and palette-difference
arguments; fixed-domain Python form/tuple/topology certificates; ordinary
Lean finite-row and reflection proofs. The arbitrary-size source theorem
is **not fully Lean formalized**. The previous large degree-four minor
catalogues are cited dependencies, not newly enumerated source graphs.

Reproduction and actual execution details are in the
[research record](history/2026-09-24-split-support.md):

```bash
python3 scripts/c5_two_spoke_split_support.py --check
python3 scripts/c5_two_spoke_reflection.py --check
lake build
lake env lean Math/TwoSpokeSplitSupportAudit.lean
python3 scripts/check_docs.py
git diff --check
```

This proves both adjacent split-support orders single-missing, without
settling whether order II itself is realizable. Eight nonadjacent (2,1)
entries, t≤1, general core separation, the common pivotal edge, and K∞=K≤5
remain open. No 603-profile or fixed-point artifact is changed.
