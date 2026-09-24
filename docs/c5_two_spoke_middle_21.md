# Middle adjacent two-spoke (2,1): three exterior hubs and a K5 minor

2026-09-24. **Both S={b1,b2} orders are impossible.** This extends the
[adjacent (2,1) proof](c5_two_spoke_adjacent_21.md) while retaining the two
separate components. The new case is a bridge with palette {3}: its two
sides each meet all three exterior colors, and give a different K5 minor.
Priority and remaining work: [HANDOFF](HANDOFF.md).

## 1. Source hypotheses and exact relations

G is a finite simple induced-C5 disk graph, with ordered boundary
B=(b0,b1,b2,b3,b4), q=01012, and connected effective interior H a minimal
q-obstruction. Its unique complete degree-five vertex z has boundary
neighbors S={b1,b2}; every other interior vertex has complete degree four.
H−z has exactly two components C₂,C₁ with distinct original contacts
P₂=(s,t), P₁=(r). Both lie in Γ=(z,b2,b3,b4,b0,b1), by the
[two-spoke region theorem](c5_degree5_two_spoke_sectors.md).
T4 acceptance can be included but is not needed for the exclusion below.

Use the actual boundary lists L_b(v)=U minus b(N_B(v)), U={0,1,2,3}, and
retain the full relation R₂(b) of ordered (s,t) colors and the root set
R₁(b), each from complete colorings of its own unchanged component.
The [R10 interface](c5_degree5_interfaces.md) gives precisely:

| Order | F_C₂(q) | F_C₁(q) | A (forbids 2) | D (forbids 3) |
| --- | --- | --- | --- | --- |
| I | {2} | {3} | C₂ | C₁ |
| II | {3} | {2} | C₁ | C₂ |

If F_C₂(q)={a}, every tuple in R₂(q) contains a, and for each e≠a
some tuple avoids e in both coordinates. Releasing zs alone and zt alone
also gives tuples (a,y), (x,a) with y,x≠a, respectively, by tight-list
slack. Those tuples need not share a coloring. If F_C₁(q)={d}, then
R₁(q)={d}. For every proper row b the exact join remains

```
Z_G(b) = (U \ {b1,b2}) \ (F_C₂(b) ∪ F_C₁(b)).
```

No endpoint marginals are multiplied, no components are merged, and the
z=2 and z=3 queries are not treated as two uncolorable assignments on A.

## 2. Crosscuts and three connected exterior sets

A must touch b4: otherwise swapping 2 and 3 preserves all its boundary
constraints but changes its forbidden singleton. D must touch all three
q-colors, by swapping any missing boundary color with 3. In particular
both have an actual z–b4 path, Q_A and Q_D, with interiors in their own
component and disjoint from B. Choose simple paths using original contacts
and actual b4 attachments. They are internally disjoint crosscuts of Γ.

The connected component A, disjoint from the interior of Q_D and unable
to pass through its endpoints, lies wholly on one side of Q_D. Thus

```
N_B(A) ⊆ {b1,b0,b4}  (left),  or  {b2,b3,b4}  (right).
```

Unlike S={b0,b1}, both boundary arcs see colors 0,1,2. Neither side order
is ruled out by the stabilizer alone. Nevertheless, define disjoint,
connected exterior branch sets, all disjoint from A:

| Side of A | X0 | X1 | X2 | Original edges between the three sets |
| --- | --- | --- | --- | --- |
| left | {b0} | {b1} | V(Q_D) | b0b1, b0b4, b1z |
| right | {b2} | {b3} | V(Q_D) | b2b3, b2z, b3b4 |

They form a triangle of branch sets. At the fixed query z=2, every actual
exterior neighbor of A with color h belongs to Xh. The internal vertices
of Q_D need not be colorable with color 2, or even be assigned a coloring:
X2 is a connected set for a minor, not a coloring replacement of D.
There are no A–D edges. This distinction is essential to both orders.

## 3. The absent-color bridge is the new obstruction

Fix q and z=2 on A. Write M(v)=L_q(v) minus {2} at original contacts,
and M(v)=L_q(v) elsewhere. A is uncolorable; all lists are tight and
external neighbor colors are distinct. Every M(v) contains 3, since its
actual exterior uses only 0,1,2. A cannot be a singleton: tightness would
require an empty list.

Use the ordinary all-positive specialization of the external degree-list
characterization ([Schweser–Stiebitz, Lemmas 2.2 and 2.4](https://arxiv.org/html/1507.04569v1)):
A has clique/odd-cycle blocks with disjoint incident palettes whose union
at v is M(v). A K4 block already gives K5 by the
[connected-exterior lemma](c5_degree5_tree_components.md#1-連通外框排除-degree-4-分量的-k4),
using the connected source exterior B∪{z}. A K5 block would use all four
edges at its vertices and disconnect A from z; larger cliques violate
the degree bound. Hence only bridges and odd cycles remain.

For any bridge uv with palette {h}, delete uv. Both sides have a slack
root, hence nonempty coloring sets. Their root sets are exactly {h}:
removing h at the root restores a tight uncolorable block assignment on
that side. This also follows by eliminating leaf blocks toward the root.
All of this uses the same M and actual exterior of A.

If h=3, each bridge side W_u,W_v must touch each exterior color 0,1,2.
If a color k were absent from one side's actual exterior, swapping k and
3 in a coloring of that side would change its forced root color and
preserve all its constraints. Consequently the following five connected
sets give all ten adjacencies of K5 in the unchanged source:

```
W_u, W_v, X0, X1, X2.
```

The bridge gives W_u–W_v; the actual attachments give all six W–X edges;
the three X–X edges were recorded in §2. This handles arbitrary bridge
side sizes and contact locations, without replacing a 3-forcer by a
fictitious 3-colored boundary vertex.

This is the precise new phenomenon when both arcs see all three colors:
a branch can force the absent color 3 without having a 3-colored exterior
neighbor. The old two-color paired-palette argument does not apply. The
three connected exterior sets convert that phenomenon into an obstruction.

## 4. A leaf odd cycle gives the other obstruction

If there is a bridge with palette {3}, §3 applies. Otherwise choose a
leaf block K of the finite block-cut tree. It cannot be a bridge: its
private endpoint would have a singleton list containing 3. It is therefore
an odd cycle with palette P={3,h}, h∈{0,1,2}, because every private vertex
has list P and contains 3. Write {k,l}={0,1,2}\{h}.

Let x be the cut vertex of K, or any chosen vertex if A=K. Every other
vertex of K has exactly two actual exterior neighbors, one of color k
and one of color l, by complete degree four and tightness. Let W be A
with those private cycle vertices removed. W is nonempty and connected.
Keep its original lists M, including the unchanged list at x.

Its root set at x is exactly P. Indeed any W-coloring with x outside P
would extend over the remaining path of K, whose lists all equal P,
contradicting uncolorability of A. Conversely x lost two edges when K's
private vertices were removed. Its list has slack two in W; deleting
one of 3,h still leaves slack one, so the connected slack-list lemma
produces a coloring with the other root color. Thus both 3 and h occur.
These are colorings of W, not colorings spliced from different z queries.

W must have actual exterior attachments of colors k and l. If k were
absent, swapping 3 and k in a W-coloring with root 3 would preserve all
constraints and give root k outside P, a contradiction; similarly for l.
This includes the single-cycle case W={x}.

Split the path K−x into two nonempty contiguous arcs V0,V1. The five
branch sets

```
V0, V1, W, Xk, Xl
```

are connected and disjoint. The three edges around the cycle give the
three pairwise adjacencies among V0,V1,W. Each private arc has actual
attachments to both Xk and Xl; W has both attachments by the preceding
root argument. Finally Xk–Xl is an original edge from §2. These are all
ten adjacencies of K5 in the unchanged source.

Only the leaf block's palette is asserted to contain 3. Internal odd
cycles with palettes avoiding 3 are allowed, and are retained inside W;
there is no assumption that all cycles are vertex-disjoint or that all
remaining directions are bridges. No bound on block count, cycle length,
or bridge length is used.

## 5. Classification, certificate, and limits

Both forbidden orders, and either crosscut side for A, are excluded.
The witness always uses a block or bridge of A and the original path Q_D
through the other component. C₂'s two named contacts and C₁'s one contact
remain separate until the final minor certificate. No use is made of the
completed (3) theorem or of a fictitious common three-contact relation.

[Checker](../scripts/c5_two_spoke_middle_21.py) and
[artifact](../artifacts/c5_two_spoke_middle_21/observations.json) check
leaf root relations, bridge support stabilizers, explicit K5 branch
sets for both sides and orders, and complete component relations on
concrete nonplanar algebra controls. Samples are finite controls, not an
enumeration of disk cores or the proof for arbitrary sources. The latter
is the crosscut and palette argument above. Trust: paper proof plus the
external degree-list theorem and existing K4 lemma; no new Lean theorem.

Of the original 18 necessary (2,1) entries, four have now been excluded
(two here, two for S={b0,b1}); the other 14 are not classified here.
Reflection transport for S={b2,b3} remains to be recorded explicitly.
General core existence/separation, t≤1, common exits, and K∞=K≤5 remain
open. No profile or fixed-point artifacts were altered.

```bash
python3 scripts/c5_two_spoke_middle_21.py --check
python3 scripts/c5_two_spoke_adjacent_21.py --check
python3 scripts/c5_degree5_two_spoke_sectors.py --check
lake build
python3 scripts/check_docs.py
git diff --check
```

Actual checks are recorded in the [research record](history/2026-09-24-middle-two-one.md).
