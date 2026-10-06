# C44: definitions and the counterexample branch

2026-10-06. This note records the definition review and an elementary argument
for the first small counterexample. The task's statistics, saved graph certificate,
brute-force comparison and validation are recorded in [REPORT](REPORT.md).
The current research stopping point remains in the
[Kempe guide](../../docs/c5_kempe_guide.md#3-停止點與保留缺口).

## 1. Definitions and sources

The source graph has a fixed ordered induced boundary cycle
`B=(0,1,2,3,4)`. A proper boundary row is interpreted in one shared literal
four-colour frame. Its acceptance means that it extends to a proper colouring of
the entire graph. The ten-row order and the singleton-position map are those of
[ES §1](../../docs/c5_excess_two_finite_search.md#1-完整前提與計數範圍).
All boundary edges are retained in every core.

For a source rejection row `q`, a **q-core** is a subgraph containing `B` that
still rejects that same literal row. A **minimal q-core** is inclusion-minimal
among these subgraphs, after ignoring isolated interior vertices. This is
subgraph minimality, so edges as well as interior vertices may be deleted; it
does not mean a vertex-induced subgraph or a minimum-cardinality obstruction.
The sources are
[independent-support capacity §1](../../docs/c5_independent_support_capacity.md#1-兩種-minimality-與來源的基本結構)
and [q-core shield §1](../../docs/c5_qcore_shield_budget.md#1-原定義依賴與證據層).
The latter explicitly states the equivalent test: `M` rejects `q` and every
nonboundary edge deletion `M-e` accepts `q`. Indeed, any proper edge subgraph is
contained in some `M-e`, and accepting colourings survive subsequent deletion.
Every minimal core inherits the source's accepted T4 rows, while its complete
`Σ(M)` can be strictly larger than `Σ(G)`.

NA and AD have two **original named roots**, `5,6`, of source degree five;
they are respectively nonadjacent and adjacent. D6 has the single original
named root `5`, of source degree six. These labels are fixed by
[ES §1](../../docs/c5_excess_two_finite_search.md#1-完整前提與計數範圍)
and [ER §1](../../docs/c5_excess_two_independent_search.md#1-問題群作用與獨立性界線).
The **core root degree pair** for NA/AD is
`(deg_M(5),deg_M(6))`, measured in the core and including all retained boundary
attachments and interior edges. A missing root is recorded as absent, not as
an effective degree-zero interior vertex. D6 has a single-entry root degree
type. The core can retain original roots even when their core degree is four;
the term `(4,4)` refers to these original labels, not to the set of vertices
whose core degree is at least five. See
[E3 nonadjacent notes §5](../c5_excess_two_e3/nonadjacent_notes.md#5-每列-q-core-的完整原省略分類)
and E4C's explicit core identities D5–D7 and D13–D14 in
[E4C §3](../c5_excess_two_e4c/REPORT.md#3-全部引理中間步驟的前提與結論).

For NA/AD, a **mixed component in a core** is a connected component of the
core's effective interior after removing the two original named roots, with
at least one retained core contact to each root. Unary components contact
exactly one root. This preserves the source ownership convention of
[E3 nonadjacent notes §2](../c5_excess_two_e3/nonadjacent_notes.md#2-原分量刪-root-與例外全部可直接移植)
and [E4 core constraints §1](../c5_excess_two_e4/CORE_CONSTRAINTS.md#1-前提與完整原身份).
Recomputing the root set as degree-at-least-five vertices of the core would
make a `(4,4)` core have no roots, so it is unsuitable for the requested
mixed-component statistic. With one original D6 root there is no two-root
mixed component.

The effective private core size is `|V(M)\B|`; the full vertex size is five
more. Ordered root degrees and a sorted root degree type should both be saved:
root swap exchanges `(4,5)` and `(5,4)`, while the named per-row certificate
continues to identify which root lost an incidence.

## 2. The exact ER AD3 graph and two minimal `(4,4)` cores

Use the ER input
[AD3 chunk](../c5_excess_two_independent_search/AD_k3/q_orbits/chunk_0001.json),
JSON pointer `/q_orbits/0`. Its complete boundary relation is `Σ(G)=956`, with
rejected singleton positions `Q={0,3,4}`. The original private vertices are
`5,6,7`, with degrees `(5,5,4)`, hence excess two. Apart from the five boundary
edges, its complete edge set is

```text
06, 16, 17, 25, 27, 35, 45, 46, 56, 57, 67.
```

The roots `5,6` are adjacent. The original mixed component is the singleton
`{7}`, with contacts `57,67` and boundary attachments `17,27`.
The input saves the apex rotation and all original edge-deletion witnesses,
so the original disk and Σ-critical conditions are checked on this same
named graph. Its ER representation differs from the ES representation of
the orbit: ER uses its own refinement adjacency code, whereas ES minimizes
the complete edge list. This distinction is stated in
[ER §3](../../docs/c5_excess_two_independent_search.md#3-σcriticalitycanonical-與小域控制).
One must transport the graph and row together when switching representatives.

Take row index `0`, the literal row `q=01012`, whose singleton is position `4`.
Its unused fourth colour is `3`. The primary named counterexample core is
`M=G-7`, deleting the entire original mixed component and all four incident
edges. Its nonboundary edges are

```text
06, 16, 25, 35, 45, 46, 56.
```

Both original roots have core degree four. Root `5` sees colours `0,1,2` at
boundary vertices `2,3,4`; root `6` sees colours `0,1,2` at `0,1,4`.
Both roots are therefore forced to colour `3`, contradicting the retained
edge `56`. Thus `M` rejects `q`.

It is inclusion-minimal. After deleting a spoke, give its root the boundary
colour formerly prohibited by that spoke and give the other root colour `3`.
The root's other two spokes see the other two boundary colours, so this is a
proper full colouring of that edge-deleted core. After deleting `56`, colour
both roots `3`. The exact seven witnesses, in root order `(5,6)`, are:

| Deleted core edge | Root colour pair |
| --- | --- |
| `06` | `(3,0)` |
| `16` | `(3,1)` |
| `25` | `(0,3)` |
| `35` | `(1,3)` |
| `45` | `(2,3)` |
| `46` | `(3,2)` |
| `56` | `(3,3)` |

This core has two effective private vertices, seven full vertices, seven
nonboundary edges, no mixed component and complete relation `Σ(M)=1022`.
Its disk embedding is inherited by deleting vertex `7` from the original
embedding. Rejection and minimality here have elementary colouring proofs;
they do not use a four-colour-theorem oracle.

There is a second minimal core for this same graph and row:
`M'=G-45-46`. Its private interior is the triangle `5,6,7`. Each triangle
vertex sees boundary colours `0,1` on its two retained spokes, so all three
have the common list `{2,3}`. The triangle cannot be coloured from that list.
Deleting any triangle edge leaves a two-colourable path; deleting a spoke
allows its incident triangle vertex a third colour. Thus `M'` is also
inclusion-minimal, has root pair `(4,4)`, and retains the original mixed
component `{7}`. It has three private vertices and eight full vertices.

An independent exhaustive check of this one row examined all `2^11=2048`
subsets of the original nonboundary edge set and all `4^3=64` private colour
tuples. It found exactly these two minimal cores. Direct Cartesian-product
colouring separately gave `Σ(G)=956`, with accepted-tuple counts
`[0,0,1,1,1,2,0,1,1,1]`, and `Σ(M)=1022`, with counts
`[0,1,1,1,1,1,1,1,2,2]` in the established ten-row order. This independent
local check is corroborative; the saved global brute-force comparison and
validation in the main report cover the full requested small domain.

## 3. Branch result and theorem boundary

The unqualified statement “ε=2 rejection rows have no two-root `(4,4)` core”
is false, even for a Σ-critical induced-C5 disk with all interior degrees
at least four. The exact AD3 graph above has two such cores for one actual
rejection row. Following the task's counterexample branch, generalization
stops here. No new per-spoke-pair case tree or paper proof of a wider absence
claim is attempted.

This graph is **not** a counterexample to the narrower proposed statement
with the additional complete-relation assumption `Σ(G)=933/941`, or an
entire-graph D5 image of either target. It rejects three singleton positions,
so it cannot be a D5 image of `933`, which rejects four. Its three rejected
positions form one cyclic arc, whereas the rejected positions of `941`
have two cyclic components; this invariant excludes a D5 image of `941`.
The target assumption is essential to the existing mixed-core series. For
example, [mixed omission §1](../../docs/c5_excess_two_mixed_omission.md#1-同一原來源與省略圖)
explicitly assumes complete `Σ=933/941`, so it does not imply that `G-7`
accepts every row in the present graph.

The finite ES/ER search found no source graph with either target complete
relation through `k=9`; absence of target-source examples makes that
restricted theorem untested by an actual antecedent in this finite domain.
No arbitrary-size theorem, ε≥3 conclusion, new Lean proof, or search
completeness theorem follows from these statistics.

For reference, the user's suggested E3 disjoint-path argument is actually
in [E3 nonadjacent notes §5](../c5_excess_two_e3/nonadjacent_notes.md#5-每列-q-core-的完整原省略分類),
while E3 REPORT §4 concerns degree-six roots. That argument bounds retained
mixed components of a **nonadjacent**, all-degree-four core. The primary
counterexample has adjacent roots and no retained mixed component, and
the second has just one retained mixed component, so neither contradicts
that reduction. Likewise
[E4 N1-22-44](../c5_excess_two_e4/REPORT.md#3-n1-主攻22-mixed-加-44-core-整類排除)
requires nonadjacent roots, a unique mixed component with original incidence
`(2,2)`, and the specified three rejected rows. Those premises do not hold
here.
