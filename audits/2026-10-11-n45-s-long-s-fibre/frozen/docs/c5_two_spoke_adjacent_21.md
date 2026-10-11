---
docgraph:
  id: c5.two-spoke-adjacent-21
  family:
    - c5
    - c5.two-spoke
  requires:
    - c5.degree5-two-spoke-sectors
    - c5.degree5-interfaces
---
# Adjacent two-spoke (2,1): separate components and a source-fixed K5 minor

後續（2026-09-24）：[q-preserving 反射與下一相鄰 orbit](c5_two_spoke_reflection.md)
已將 S={b0,b1} 排除搬到 S={b2,b3}；六個 (2,1) 表項累計排除，尚餘四相鄰、
八非相鄰項。下一相鄰 orbit 有必要 split-support 定理及八個只缺 q 的既有
disk 控制；一般單缺失分離未證。下文數字與停止點保留當輪語境。

後續（2026-09-24）：[中間相鄰 (2,1) 排除](c5_two_spoke_middle_21.md) 已排除
S={b1,b2} 的兩種次序；palette {3} bridge／leaf odd cycle 與三個連通外部
branch sets 給同圖 K5 minor。原 18 個 (2,1) 表項累計四個排除，尚有 14 個
未分類；下文數字及停止點保留當輪語境。

2026-09-24. This treats exactly S={b0,b1}, q=01012, and both orders
of the singleton forbidden sets in the [two-spoke table](c5_degree5_two_spoke_sectors.md).
Dependencies are [R10](c5_degree5_interfaces.md), the connected-exterior
[K4 lemma](c5_degree5_tree_components.md#1-連通外框排除-degree-4-分量的-k4),
and the external degree-list characterization. Priority: [HANDOFF](HANDOFF.md).

**Result: both specified configurations are impossible.** The obstruction
uses an odd cycle in one component and a z-to-b4 path in the other. It does
not merge C₂ and C₁ or invoke the completed (3) theorem. Neither T4 acceptance
nor a second rejected boundary row is needed once the hypotheses below hold.
The other 16 entries of the previous 18-entry necessary table are not
classified by this report.

## 1. Hypotheses and the two independent z queries

G is a finite simple induced-C5 disk graph with boundary B=(b0,...,b4).
The effective interior H is a minimal q-obstruction. Its unique complete
degree-five vertex z has boundary neighbors exactly {b0,b1}; every other
interior vertex has complete degree four. H−z has exactly two components:

- C₂, with two distinct original contacts P₂={s,t};
- C₁, with its original contact P₁={r}.

Both lie in the long region Γ=(z,b1,b2,b3,b4,b0). Retain every actual boundary
attachment and every intermediate bridge. With U={0,1,2,3}, write

```
L(v) = U \ q(N_B(v)),
M_a(v) = L(v) \ ({a} if v is an original contact else ∅).
```

R10 gives exactly the two possibilities

| Order | F_C₂(q) | F_C₁(q) |
| --- | --- | --- |
| I | {2} | {3} |
| II | {3} | {2} |

Name the component forbidding 2 **A** and the component forbidding 3 **D**.
These are aliases, not a union: (A,D)=(C₂,C₁) in I and (C₁,C₂) in II.

For either component, only its forbidden query is uncolorable. Its M_a
lists are then tight, its external colors are distinct at every vertex,
and it has disjoint block palettes. The other z queries are colorable.
There are not two uncolorable palette decompositions on either component
to subtract, unlike (3).

More explicitly, if F_C₁(q)={d}, its full root set is R_C₁(q)={d}, so it
accepts precisely z≠d. If F_C₂(q)={a}, retain the ordered relation
R₂⊆U². Every (x,y)∈R₂ has x=a or y=a, and for each e≠a some tuple avoids
e in both coordinates. Releasing only zs or only zt and using tight-list
slack also gives tuples (a,y), (x,a) with x,y≠a. These need not be the same
coloring; no Cartesian product of endpoint marginals is taken.

## 2. Two disjoint paths force the 2-forbidden component to the short side

For a fixed component C, a color permutation fixing every color on its
actual boundary attachments must preserve F_C(q). Since q uses no 3:

- F_C(q)={2} forces a b4 attachment: otherwise swapping 2 and 3 fixes all
  its boundary constraints and changes its forbidden singleton.
- F_C(q)={3} forces attachments of each color 0,1,2: omit any color h and
  swapping h with 3 gives the same contradiction. In particular D touches
  b4 and at least one of b1,b3.

Choose a simple path Q_A from z through A to b4, using an original z
contact and a real b4 attachment; choose Q_D similarly. Their interiors
are disjoint and avoid B. Both are crosscuts of the same Γ disk, from z to
b4. The two boundary arcs between their endpoints are

```
I_short = (z,b0,b4),    I_long = (z,b1,b2,b3,b4).
```

The paths have a linear order between these arcs. The component containing
the short-side path is confined to the short side of the other path:
it is connected, disjoint from that crosscut, and cannot pass through z or
b4 as an interior vertex. Thus all its boundary attachments lie in
{b0,b4}. It cannot be D, which must touch color 1. Consequently

```
N_B(A) ⊆ {b0,b4},    Q_D ⊆ {z,b4} ∪ D.                (1)
```

This reasoning uses both separate components and their actual paths. It
does not choose attachment sets independently from a position table.

There is already an exact finite interface at this point. For every proper
boundary row b, choose one global permutation π with π(0)=b0, π(2)=b4.
Equation (1) makes it a coloring bijection on A, hence

```
F_A(b)={b4},
Z_G(b) = (U \ {b0,b1,b4}) \ F_D(b).                    (2)
```

Here b0,b1,b4 denote the colors in row b. This holds for all 240 labeled
proper rows, with D unchanged in the same color frame. Deleting A except
Q_A and contracting its internal path vertices into z would realize the
spoke zb4 while fixing every boundary vertex and all of D. Equality (2),
not a generic claim about minors, proves the exact z-query semantics.
We do not need that replacement: the original graph already has a minor
obstruction as follows.

## 3. Same-source palettes of A at z=2

Fix z=2 throughout this section. All external colors seen by A are 0 or 2.
Its uncolorable degree lists M=M₂ therefore contain both 1 and 3 at every
vertex. Tightness gives |M(v)|=deg_A(v); in particular A is not a singleton.

The external degree-list theorem supplies a Gallai block decomposition with
palettes S_K whose disjoint union at v is M(v). We use the ordinary,
all-positive specialization of [Schweser–Stiebitz, Lemmas 2.2 and 2.4](https://arxiv.org/html/1507.04569v1),
as in R10. This is an external theorem, not a result of the checker.

The vertex/block incidence matrix has independent columns: a private vertex
of a leaf block determines that column coefficient, then remove the block
and continue. The equations

```
Σ_(K contains v) (1_[1∈S_K] − 1_[3∈S_K]) = 0
```

therefore imply 1∈S_K iff 3∈S_K, separately for each actual block K.
The connected-exterior K4 lemma applies here: B∪{z} is connected, A has
complete degree four, and its z=2 query is uncolorable. A K4 block would
already give a source-fixed K5 minor. K5 is itself nonplanar; larger
cliques violate the degree bound. Thus the remaining blocks are precisely

- bridges with singleton palette {0} or {2};
- odd cycles, including triangles, with palette {1,3}.

Every vertex belongs to exactly one of these odd cycles, since its list
contains 1 and 3 and incident palettes are disjoint. In particular an odd
cycle exists, different cycles are vertex-disjoint, and the intervening
bridges are all original bridges of A. This is an arbitrary-size structure
statement, with no bound on cycle lengths, count, or bridge distances.

At any cycle vertex v the two cycle edges use two of its four incident
edges. The two other directions are original external edges or bridges.
Disjoint palette union, together with tight external colors, labels those
two directions **one 0 and one 2**. A direct external edge has its actual
external color; a bridge has its singleton palette color.

These palettes certify only z=2. Changing z to 3 changes the contact lists
to (M₂(v)∪{2})\{3}, leaving noncontact lists unchanged. The new assignment
is colorable because F_A(q)={2}; it is not assigned a second uncolorable
palette decomposition. Equation (2) controls all the z queries without
discarding the two-contact relation when A=C₂.

## 4. Each labeled bridge direction reaches the matching actual exterior

Take a cycle K in A and a bridge vw leaving K, with palette {h}, h∈{0,2}.
Let W be its side away from K. Deleting vw leaves both sides colorable
by the slack-list lemma. In any coloring of either side the bridge root
is forced to h: delete leaf blocks away from that root; their palettes
are removed at their cut vertices, leaving precisely the missing bridge
palette {h} at the root. Equivalently, reducing the root list by h gives
the uncolorable tight block assignment on that side, while slack gives
nonempty root possibilities before the reduction.

W must have an actual exterior neighbor colored h. Otherwise swapping h
and the absent exterior color 3 in a coloring of W changes its forced
root color while preserving every exterior constraint, a contradiction.
Take a path from w to such an attachment, stopping at its first exterior
vertex. Together with vw it is an actual tether from v:

- label 0 reaches b0;
- label 2 reaches z or b4.

A direct exterior edge is the length-one case. For one fixed cycle, all
bridge sides in all these directions are disjoint: a return to another
cycle vertex, or an intersection of two sides, would make the leaving
edge belong to a larger block, not a bridge. Therefore all selected
tethers have disjoint interiors and avoid K. They also avoid D entirely.
Tethers may share their exterior endpoints, which is exactly what the
two hub branch sets below require.

## 5. Explicit K5 branch sets in the unchanged source

Partition the cyclically ordered vertices of K into three nonempty
contiguous arcs V0,V1,V2. Each arc is connected, and the three cycle edges
between arcs give pairwise adjacency. Define two further branch sets:

```
O0 = {b0} ∪ interiors of all selected 0-tethers,
O2 = V(Q_D) ∪ interiors of all selected 2-tethers.
```

Both are connected. The tethers to O2 end at z or b4, which are connected
by the actual path Q_D through the other component. The five sets are
pairwise disjoint. Every Vi has a tether to each Oj; every pair of Vi is
adjacent along K; and O0 is adjacent to O2 by the original boundary edge
b0b4. These are all ten edges of a K5 minor. This contradicts planarity.

The proof works with either contact count in A. The table in §1 records
which component owns the cycle and which supplies Q_D. Both original
contacts of C₂ remain in the source, whether or not a chosen minor witness
uses both edges. Contracting branch sets is only the final nonplanarity
certificate, not a merging of C₂/C₁ into a three-contact coloring component.
The boundary cycle and its cyclic order were preserved throughout the
extraction; only the final obstruction contracts boundary-containing sets.

## 6. Certificate, scope, and next entry

[Checker](../scripts/c5_two_spoke_adjacent_21.py) and
[artifact](../artifacts/c5_two_spoke_adjacent_21/observations.json) contain:

- all 32 actual-boundary-support subsets and their singleton stabilizers;
- 240 labeled proper rows with the common-permutation transport in (2),
  and 3,840 join checks against every possible forbidden mask of D;
- all four local palette/exterior partitions at a cycle vertex;
- two concrete triangle list controls, one with each contact count, with
  complete contact tuples on all 240 rows (480 checks). The two-contact
  control also demonstrates the failure of independent endpoint marginals;
- 48 explicit K5 certificates, with cycle lengths 3,5,7,9, both component
  orders, direct/subdivided tethers, and two lengths of the separate D path.
  Each certificate checks two connected, disjoint interior components,
  their named two/one contact sets, branch-set connectivity/disjointness,
  and an original edge for every required adjacency.

Minor samples are extracted-shape subgraphs, not complete degree-four
candidate cores or disk witnesses. Their forbidden labels name their roles
in the paper extraction, not a coloring computation on incomplete samples.
Arbitrary sizes, crosscut ordering, and actual-tether extraction are proved
above, not inferred from the finite samples.

Trust: paper proof plus the external degree-list theorem and the existing
K4 lemma, with Python local certificates. No new Lean theorem. The two
specified entries of the 18-entry (2,1) table are excluded; no conclusion
here reclassifies the other 16, t≤1, general single-sided exits, common
exits, or K∞=K≤5. No 603 profiles or fixed-point artifacts were changed.

```bash
python3 scripts/c5_two_spoke_adjacent_21.py --check
python3 scripts/c5_degree5_two_spoke_sectors.py --check
python3 scripts/check_docs.py
git diff --check
```

Actual validation and the exact remaining entry are recorded in the
[research record](history/2026-09-24-adjacent-two-one.md).
