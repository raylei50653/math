# Task C44′: Sigma compatibility of two-root (4,4) cores

2026-10-06. Base `integrate-kprime-e3 @ 32c51fa76dd992474f124b3686b6b23c6040e7ab`;
branch `task-c44p-screen`, worktree `/home/ray/developer/ai/math-task-c44p`.
**Finite classification complete; compatible-core branch taken.** All 2,416
saved occurrences, representing 213 distinct literal edge sets, are compatible.
The exhaustive two-private-vertex classification has 125 literal placements,
30 disk placements and 10 compatible disk placements. Independent recomputation
agrees throughout. The screen therefore supplies no absence theorem.

The named cores **C44P-AD2-012-034** and **C44P-MIXED3-001** include graphs,
embeddings, complete relations, matching target images and witnesses. Neither
is a construction of a source whose complete Sigma is 933/941. The arbitrary-size
target-source absence statement remains unproved. Generalization stops here,
as requested. Current research navigation remains in the
[Kempe guide section 3](../../docs/c5_kempe_guide.md#3-停止點與保留缺口);
the guide is intentionally unchanged for the integrator.

## 1. Definitions and their sources

| Term | Exact convention | Source |
| --- | --- | --- |
| Frame | The named induced cycle B=(0,1,2,3,4), retaining edges 01,12,23,34,04. Private vertices lie inside this disk boundary. | [ES section 1](../../docs/c5_excess_two_finite_search.md#1-完整前提與計數範圍) |
| Sigma | The subset of ten proper boundary rows that extend to a proper four-colouring of the entire literal graph. One common S4 permutation acts on the whole colouring; frame vertices and attachments remain named. | [ES section 1](../../docs/c5_excess_two_finite_search.md#1-完整前提與計數範圍), [REPS definition](../../scripts/c5_kempe_screen.py) |
| q-core and minimality | A subgraph containing B and rejecting the same literal row q. Inclusion-minimality permits nonframe-edge and private-vertex deletion, ignoring isolated private vertices. Equivalently, rejection persists in M but every M-e accepts q for each nonframe edge e. | [C44 definitions](../c5_excess_two_c44/REPORT.md#1-definitions-fixed-before-implementation), [C44 proof notes](../c5_excess_two_c44/PROOF_NOTES.md#1-definitions-and-sources), [q-core definitions](../../docs/c5_qcore_shield_budget.md#1-原定義依賴與證據層) |
| Original roots in part (a) | Labels 5,6 from the original AD/NA source, even after their degrees fall to four in the core. AD/NA describes the source's root adjacency. A core of an AD source can have lost edge 56. | [C44 definitions](../c5_excess_two_c44/REPORT.md#1-definitions-fixed-before-implementation) |
| Core size and mixed | Private size is the number of effective vertices outside B; total size is five larger. A mixed component is a component after removing B and the two named original roots, retaining contacts to both roots. | [C44 proof notes](../c5_excess_two_c44/PROOF_NOTES.md#1-definitions-and-sources) |
| Duplicate core in part (a) | Exactly the same sorted full literal edge set, including frame and private labels. No private relabelling or graph-isomorphism quotient is imposed. All occurrences retain their source and literal rejection row. | This task's requested duplicate convention |
| D5 and compatibility | All maps g(i)=(s*i+r) mod 5, s in {1,-1}, r in {0,...,4}, act simultaneously on the frame. A core is compatible if at least one transported full 933/941 row set is contained in Sigma(M). | [C44′ proposal](../../docs/c5_kempe_guide.md#3-停止點與保留缺口), this task's inclusion definition |

The REPS row order is fixed as follows; a mask has bit i precisely when row i
is accepted. All implementation copies are cross-checked against this order.

| Index | Literal row | T4 |
| ---: | --- | --- |
| 0 | 01012 | no |
| 1 | 01021 | no |
| 2 | 01023 | yes |
| 3 | 01201 | no |
| 4 | 01202 | no |
| 5 | 01203 | yes |
| 6 | 01212 | no |
| 7 | 01213 | yes |
| 8 | 01231 | yes |
| 9 | 01232 | yes |

Thus T4 has indices {2,5,7,8,9}, mask 932. The literal targets accept indices
{0,2,5,7,8,9} for 933 and {0,2,3,5,7,8,9} for 941. For a forward vertex map g,
the transported row satisfies q'(g(i))=q(i), followed by one common colour
normalization. The main algorithms use first-appearance normalization; the
independent implementation constructs all 24 S4 permutations explicitly.
No exterior screen or theorem in the REPS-defining module is invoked.

There are 20 target/element pairs. Repeated masks remain separate records,
so every match has an explicit group element. Their distinct image masks are
933: {933,934,940,948,996} and 941: {941,949,950,998,1004}. No independent
normalization of components, supports or graph relations is performed.

## 2. Same-frame monotonicity

Let M be a subgraph of G retaining the named frame and its five edges. Any
proper colouring of G extending a literal boundary row restricts to a proper
colouring of M extending that very row. Deleting nonframe edges or private
vertices therefore can only add accepted rows:

\[
\Sigma(G)\subseteq\Sigma(M).
\]

Taking one shared S4 quotient preserves this inclusion. If Sigma(G) equals a
whole-graph D5 image of 933 or 941, that literal image must be contained in
Sigma(M). This proves the necessity of compatibility. Its converse is not
claimed: a match does not supply the missing source, its other cores,
criticality, or its embedding with additional vertices.

## 3. Saved-core screen: part (a)

Read exactly the 19 chunks in [the C44 orbit directory](../c5_excess_two_c44/orbits/chunk_0001.json).
Both roots' presence and degrees are recomputed from their literal edges;
the selected population is AD 2,360 and NA 56, including critical and
noncritical sources. An occurrence is a specific saved source representative,
literal rejection row and core entry, not a labelled-graph count.

| Source type | Population | Occurrences | Compatible | Incompatible | Distinct literal cores | Mixed occurrences |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| AD | critical | 26 | 26 | 0 | 22 | 25 |
| AD | noncritical | 2,334 | 2,334 | 0 | 159 | 2,068 |
| NA | critical | 0 | 0 | 0 | 0 | 0 |
| NA | noncritical | 56 | 56 | 0 | 38 | 56 |
| Total | all | 2,416 | 2,416 | 0 | 213 | 2,149 |

Distinct counts overlap: AD has 176 literal cores, NA has 38, and one is
shared across source types. Five AD cores occur in both critical and
noncritical populations. Consequently these distinct counts are not additive.
All 267 nonmixed occurrences are also compatible.

The complete joint size/mixed breakdown follows. Every count in it is
compatible, with zero incompatible occurrences; total size is private size + 5.
Distinct counts within groups again need not be additive.

| Source type | Population | Private size | Mixed | Occurrences | Distinct literal cores |
| --- | --- | ---: | --- | ---: | ---: |
| AD | critical | 2 | no | 1 | 1 |
| AD | critical | 3 | yes | 9 | 7 |
| AD | critical | 6 | yes | 16 | 14 |
| AD | noncritical | 2 | no | 211 | 1 |
| AD | noncritical | 3 | yes | 1,989 | 63 |
| AD | noncritical | 4 | no | 31 | 8 |
| AD | noncritical | 5 | no | 16 | 12 |
| AD | noncritical | 5 | yes | 39 | 27 |
| AD | noncritical | 6 | no | 6 | 6 |
| AD | noncritical | 6 | yes | 22 | 22 |
| AD | noncritical | 7 | yes | 9 | 9 |
| AD | noncritical | 8 | no | 2 | 2 |
| AD | noncritical | 9 | yes | 9 | 9 |
| NA | noncritical | 5 | yes | 32 | 14 |
| NA | noncritical | 6 | yes | 24 | 24 |

Every saved complete mask agrees with the main DFS recomputation and the
independent frontier DP. There are **zero Sigma differences and zero recomputed
metadata differences**. The five masks and occurrence counts are:

| Sigma(M) | Rejected row | Occurrences |
| ---: | ---: | ---: |
| 959 | 6 | 1,735 |
| 1007 | 4 | 154 |
| 1015 | 3 | 168 |
| 1021 | 1 | 32 |
| 1022 | 0 | 327 |

Each rejects only one three-colour row. A D5 image of either target can be
chosen to reject that row, so inclusion follows. Every core matches eight
933 group elements (four distinct images) and six 941 elements (three distinct
images). All matches, including the group elements, are saved. This explanation
uses the recomputed row sets; the saved mask was only a comparison value.

The [summary](saved_screen_summary.json) has the 19 input hashes, 24 actual
ER embedding-source hashes, chunk manifest, mismatch arrays and weighted
counts. The [catalog](saved_screen/catalog/chunk_0001.json) names all cores
`C44P-S0001` through `C44P-S0213`, saving full graphs, colourings, complete
rejection trees, deletion witnesses and inherited rotations. The
[occurrence chunks](saved_screen/occurrences/chunk_0001.json) keep all 2,416
source/row/core JSON pointers, source population, saved and recomputed masks,
size/mixed data, named-core references and all matching group elements.
Identical literal edge sets share one decision calculation but retain every
occurrence. For each nonmatching image, the output also supplies a missing
target row and its core rejection-tree reference. Each compatible core has
six nonmatching target/element pairs, and these witnesses are saved too.
This population has no core for which all 20 pairs fail.

## 4. Exhaustive two-private-vertex classification: part (b)

### 4.1 Complete placement domain and disk proof

Let the only private vertices be r=5 and s=6, both of degree four. The only
possible private edge is rs. If it is present, each root has exactly three
distinct spokes, giving binomial(5,3)^2=100 ordered placements. If absent,
each has four distinct spokes, giving binomial(5,4)^2=25. These are all 125
graphs of the stipulated shape. No bound on a possible containing source's
size is used in this classification.

Draw r's star in the disk. Its spokes divide the disk into sectors bounded by
two consecutive spokes and the closed boundary arc between their contacts.
This separation follows from the Jordan theorem. The private vertex s lies
inside one sector; all of its spokes must terminate on that sector's closed
boundary arc. Otherwise a spoke crosses r's star. Conversely, if all s
contacts lie on one such arc, place s inside the sector and draw its fan;
when rs is present, add the fan edge to r along the same sector. Thus containment
of s's contacts in one closed sector arc is an exact embedding criterion.

In the nonadjacent case r has four contacts, leaving only one missing frame
vertex. Each sector arc has at most three frame vertices, so four s contacts
cannot fit. **All 25 nonadjacent placements are impossible disk embeddings.**
This is a paper exclusion, independent of a planarity library.

Among r's ten three-sets, the five consecutive triples have one four-vertex
sector and two two-vertex sectors. The large sector permits four three-sets
for s, giving 20 placements. The other five triples each have two three-vertex
sectors, each allowing one s three-set, giving ten more. Exactly **30 adjacent
placements are disks**. The remaining 70 adjacent placements fail the same
sector criterion. Explicit sphere and disk rotations are saved for all 30;
apex planarity corroborates all 125 sector decisions.

Simultaneous D5 transport and root swap give 20 graph maps. All literal
placements remain saved, including every impossible case, while the full graph
quotient has nine adjacent and three nonadjacent orbits. The 30 disk placements
form exactly two orbits: 20 with representatives 012/023 and ten with
representative 012/034. The former share two frame contacts, the latter one.
The complete orbit members and stabilizers are in [two_private.json](two_private.json).

### 4.2 Complete Sigma, minimality and compatibility

For a row q, define L_r as the four colours minus the colours seen by r's
spokes, and similarly L_s. With no rs, acceptance is exactly nonemptiness
of both lists. With rs, acceptance is exactly existence of unequal a in L_r
and b in L_s. There are no other private vertices or constraints.

In the adjacent case both lists are nonempty; rejection is equivalent to
L_r=L_s={c}. Each root's three spokes then see three distinct colours.
Deleting a spoke frees its boundary colour for that root while the other keeps
c; deleting rs lets both take c. Thus every rejected row has the whole adjacent
graph as its unique inclusion-minimal core. In the nonadjacent case, rejection
means one or both roots see all four colours. The corresponding four-spoke
stars are exactly the minimal cores; the whole two-root graph is never minimal.
The main implementation also enumerates every nonframe-edge subset (at most
256 per graph) and saves all minimal cores, their rejection witnesses and
every deletion colouring. The independent implementation separately enumerates
those subsets and checks equality.

| Root adjacency | Literal placements | All graph orbits | Disk placements | Disk orbits | Compatible disk placements | Compatible disk orbits |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Adjacent | 100 | 9 | 30 | 2 | 10 | 1 |
| Nonadjacent | 25 | 3 | 0 | 0 | 0 | 0 |
| Total | 125 | 12 | 30 | 2 | 10 | 1 |

All 30 disk placements have minimal rejection rows: ten reject one row each,
and 20 reject two each, totalling 50 placement/row occurrences. Only the ten
compatible ones inherit all T4 rows and can pass a target-source subgraph screen.
Of all abstract placements, 60 are compatible, including 50 that fail the disk
criterion; these extra abstract matches are not disk cores.

For representative 012/023, Sigma=831 rejects indices 6 and 7; index 7 is T4.
Every target image contains all T4, so the entire 20-placement disk orbit is
incompatible. Each failed target image has a saved missing row and literal
list rejection witness. For representative 012/034, Sigma=959 rejects only
index 6, so all ten placements in that orbit are compatible. Both the literal
933 and literal 941 are contained in this representative's relation.

### 4.3 Full literal placement and orbit tables

`AD`/`NA` here describes the placement's own root adjacency. The table includes
all 125 abstract placements to record every nonembedding case. `W` gives exactly
the rejected rows for which the whole placement is a minimal core; a graph
accepting every row has empty `W`. Only rows marked Disk=yes describe disk
placements. Matching targets means some D5 image of that target, and the
exact elements and images are in the JSON. The standalone generated copy is
[two_private_table.md](two_private_table.md).

| Literal placement | D5 x root-swap representative | Disk | Sigma | Rejected rows | W | Compatible | Matching targets |
| --- | --- | --- | ---: | --- | --- | --- | --- |
| AD-012-012 | AD-012-012 | no | 7 | 3,4,5,6,7,8,9 | 3,4,5,6,7,8,9 | no | none |
| AD-012-013 | AD-012-013 | no | 1023 | empty | empty | yes | 933,941 |
| AD-012-014 | AD-012-014 | no | 431 | 4,6,9 | 4,6,9 | no | none |
| AD-012-023 | AD-012-023 | yes | 831 | 6,7 | 6,7 | no | none |
| AD-012-024 | AD-012-023 | yes | 759 | 3,8 | 3,8 | no | none |
| AD-012-034 | AD-012-034 | yes | 959 | 6 | 6 | yes | 933,941 |
| AD-012-123 | AD-012-014 | no | 967 | 3,4,5 | 3,4,5 | no | none |
| AD-012-124 | AD-012-013 | no | 1023 | empty | empty | yes | 933,941 |
| AD-012-134 | AD-014-023 | no | 1007 | 4 | 4 | yes | 933,941 |
| AD-012-234 | AD-012-034 | yes | 1015 | 3 | 3 | yes | 933,941 |
| AD-013-012 | AD-012-013 | no | 1023 | empty | empty | yes | 933,941 |
| AD-013-013 | AD-013-013 | no | 249 | 1,2,8,9 | 1,2,8,9 | no | none |
| AD-013-014 | AD-012-013 | no | 1023 | empty | empty | yes | 933,941 |
| AD-013-023 | AD-013-023 | no | 1023 | empty | empty | yes | 933,941 |
| AD-013-024 | AD-013-024 | no | 1023 | empty | empty | yes | 933,941 |
| AD-013-034 | AD-012-023 | yes | 765 | 1,8 | 1,8 | no | none |
| AD-013-123 | AD-012-023 | yes | 1017 | 1,2 | 1,2 | no | none |
| AD-013-124 | AD-013-024 | no | 1023 | empty | empty | yes | 933,941 |
| AD-013-134 | AD-013-023 | no | 1023 | empty | empty | yes | 933,941 |
| AD-013-234 | AD-014-023 | no | 1021 | 1 | 1 | yes | 933,941 |
| AD-014-012 | AD-012-014 | no | 431 | 4,6,9 | 4,6,9 | no | none |
| AD-014-013 | AD-012-013 | no | 1023 | empty | empty | yes | 933,941 |
| AD-014-014 | AD-012-012 | no | 266 | 0,2,4,5,6,7,9 | 0,2,4,5,6,7,9 | no | none |
| AD-014-023 | AD-014-023 | no | 959 | 6 | 6 | yes | 933,941 |
| AD-014-024 | AD-012-013 | no | 1023 | empty | empty | yes | 933,941 |
| AD-014-034 | AD-012-014 | no | 830 | 0,6,7 | 0,6,7 | no | none |
| AD-014-123 | AD-012-034 | yes | 1007 | 4 | 4 | yes | 933,941 |
| AD-014-124 | AD-012-023 | yes | 1018 | 0,2 | 0,2 | no | none |
| AD-014-134 | AD-012-023 | yes | 975 | 4,5 | 4,5 | no | none |
| AD-014-234 | AD-012-034 | yes | 1022 | 0 | 0 | yes | 933,941 |
| AD-023-012 | AD-012-023 | yes | 831 | 6,7 | 6,7 | no | none |
| AD-023-013 | AD-013-023 | no | 1023 | empty | empty | yes | 933,941 |
| AD-023-014 | AD-014-023 | no | 959 | 6 | 6 | yes | 933,941 |
| AD-023-023 | AD-013-013 | no | 63 | 6,7,8,9 | 6,7,8,9 | no | none |
| AD-023-024 | AD-013-023 | no | 1023 | empty | empty | yes | 933,941 |
| AD-023-034 | AD-012-023 | yes | 447 | 6,9 | 6,9 | no | none |
| AD-023-123 | AD-012-013 | no | 1023 | empty | empty | yes | 933,941 |
| AD-023-124 | AD-013-024 | no | 1023 | empty | empty | yes | 933,941 |
| AD-023-134 | AD-013-024 | no | 1023 | empty | empty | yes | 933,941 |
| AD-023-234 | AD-012-013 | no | 1023 | empty | empty | yes | 933,941 |
| AD-024-012 | AD-012-023 | yes | 759 | 3,8 | 3,8 | no | none |
| AD-024-013 | AD-013-024 | no | 1023 | empty | empty | yes | 933,941 |
| AD-024-014 | AD-012-013 | no | 1023 | empty | empty | yes | 933,941 |
| AD-024-023 | AD-013-023 | no | 1023 | empty | empty | yes | 933,941 |
| AD-024-024 | AD-013-013 | no | 599 | 3,5,7,8 | 3,5,7,8 | no | none |
| AD-024-034 | AD-012-013 | no | 1023 | empty | empty | yes | 933,941 |
| AD-024-123 | AD-014-023 | no | 1015 | 3 | 3 | yes | 933,941 |
| AD-024-124 | AD-013-023 | no | 1023 | empty | empty | yes | 933,941 |
| AD-024-134 | AD-013-024 | no | 1023 | empty | empty | yes | 933,941 |
| AD-024-234 | AD-012-023 | yes | 983 | 3,5 | 3,5 | no | none |
| AD-034-012 | AD-012-034 | yes | 959 | 6 | 6 | yes | 933,941 |
| AD-034-013 | AD-012-023 | yes | 765 | 1,8 | 1,8 | no | none |
| AD-034-014 | AD-012-014 | no | 830 | 0,6,7 | 0,6,7 | no | none |
| AD-034-023 | AD-012-023 | yes | 447 | 6,9 | 6,9 | no | none |
| AD-034-024 | AD-012-013 | no | 1023 | empty | empty | yes | 933,941 |
| AD-034-034 | AD-012-012 | no | 56 | 0,1,2,6,7,8,9 | 0,1,2,6,7,8,9 | no | none |
| AD-034-123 | AD-012-034 | yes | 1021 | 1 | 1 | yes | 933,941 |
| AD-034-124 | AD-014-023 | no | 1022 | 0 | 0 | yes | 933,941 |
| AD-034-134 | AD-012-013 | no | 1023 | empty | empty | yes | 933,941 |
| AD-034-234 | AD-012-014 | no | 1016 | 0,1,2 | 0,1,2 | no | none |
| AD-123-012 | AD-012-014 | no | 967 | 3,4,5 | 3,4,5 | no | none |
| AD-123-013 | AD-012-023 | yes | 1017 | 1,2 | 1,2 | no | none |
| AD-123-014 | AD-012-034 | yes | 1007 | 4 | 4 | yes | 933,941 |
| AD-123-023 | AD-012-013 | no | 1023 | empty | empty | yes | 933,941 |
| AD-123-024 | AD-014-023 | no | 1015 | 3 | 3 | yes | 933,941 |
| AD-123-034 | AD-012-034 | yes | 1021 | 1 | 1 | yes | 933,941 |
| AD-123-123 | AD-012-012 | no | 193 | 1,2,3,4,5,8,9 | 1,2,3,4,5,8,9 | no | none |
| AD-123-124 | AD-012-013 | no | 1023 | empty | empty | yes | 933,941 |
| AD-123-134 | AD-012-023 | yes | 495 | 4,9 | 4,9 | no | none |
| AD-123-234 | AD-012-014 | no | 757 | 1,3,8 | 1,3,8 | no | none |
| AD-124-012 | AD-012-013 | no | 1023 | empty | empty | yes | 933,941 |
| AD-124-013 | AD-013-024 | no | 1023 | empty | empty | yes | 933,941 |
| AD-124-014 | AD-012-023 | yes | 1018 | 0,2 | 0,2 | no | none |
| AD-124-023 | AD-013-024 | no | 1023 | empty | empty | yes | 933,941 |
| AD-124-024 | AD-013-023 | no | 1023 | empty | empty | yes | 933,941 |
| AD-124-034 | AD-014-023 | no | 1022 | 0 | 0 | yes | 933,941 |
| AD-124-123 | AD-012-013 | no | 1023 | empty | empty | yes | 933,941 |
| AD-124-124 | AD-013-013 | no | 858 | 0,2,5,7 | 0,2,5,7 | no | none |
| AD-124-134 | AD-013-023 | no | 1023 | empty | empty | yes | 933,941 |
| AD-124-234 | AD-012-023 | yes | 894 | 0,7 | 0,7 | no | none |
| AD-134-012 | AD-014-023 | no | 1007 | 4 | 4 | yes | 933,941 |
| AD-134-013 | AD-013-023 | no | 1023 | empty | empty | yes | 933,941 |
| AD-134-014 | AD-012-023 | yes | 975 | 4,5 | 4,5 | no | none |
| AD-134-023 | AD-013-024 | no | 1023 | empty | empty | yes | 933,941 |
| AD-134-024 | AD-013-024 | no | 1023 | empty | empty | yes | 933,941 |
| AD-134-034 | AD-012-013 | no | 1023 | empty | empty | yes | 933,941 |
| AD-134-123 | AD-012-023 | yes | 495 | 4,9 | 4,9 | no | none |
| AD-134-124 | AD-013-023 | no | 1023 | empty | empty | yes | 933,941 |
| AD-134-134 | AD-013-013 | no | 459 | 2,4,5,9 | 2,4,5,9 | no | none |
| AD-134-234 | AD-012-013 | no | 1023 | empty | empty | yes | 933,941 |
| AD-234-012 | AD-012-034 | yes | 1015 | 3 | 3 | yes | 933,941 |
| AD-234-013 | AD-014-023 | no | 1021 | 1 | 1 | yes | 933,941 |
| AD-234-014 | AD-012-034 | yes | 1022 | 0 | 0 | yes | 933,941 |
| AD-234-023 | AD-012-013 | no | 1023 | empty | empty | yes | 933,941 |
| AD-234-024 | AD-012-023 | yes | 983 | 3,5 | 3,5 | no | none |
| AD-234-034 | AD-012-014 | no | 1016 | 0,1,2 | 0,1,2 | no | none |
| AD-234-123 | AD-012-014 | no | 757 | 1,3,8 | 1,3,8 | no | none |
| AD-234-124 | AD-012-023 | yes | 894 | 0,7 | 0,7 | no | none |
| AD-234-134 | AD-012-013 | no | 1023 | empty | empty | yes | 933,941 |
| AD-234-234 | AD-012-012 | no | 592 | 0,1,2,3,5,7,8 | 0,1,2,3,5,7,8 | no | none |
| NA-0123-0123 | NA-0123-0123 | no | 255 | 8,9 | empty | no | none |
| NA-0123-0124 | NA-0123-0124 | no | 95 | 5,7,8,9 | empty | no | none |
| NA-0123-0134 | NA-0123-0134 | no | 251 | 2,8,9 | empty | no | none |
| NA-0123-0234 | NA-0123-0134 | no | 127 | 7,8,9 | empty | no | none |
| NA-0123-1234 | NA-0123-0124 | no | 219 | 2,5,8,9 | empty | no | none |
| NA-0124-0123 | NA-0123-0124 | no | 95 | 5,7,8,9 | empty | no | none |
| NA-0124-0124 | NA-0123-0123 | no | 863 | 5,7 | empty | no | none |
| NA-0124-0134 | NA-0123-0124 | no | 347 | 2,5,7,9 | empty | no | none |
| NA-0124-0234 | NA-0123-0134 | no | 607 | 5,7,8 | empty | no | none |
| NA-0124-1234 | NA-0123-0134 | no | 859 | 2,5,7 | empty | no | none |
| NA-0134-0123 | NA-0123-0134 | no | 251 | 2,8,9 | empty | no | none |
| NA-0134-0124 | NA-0123-0124 | no | 347 | 2,5,7,9 | empty | no | none |
| NA-0134-0134 | NA-0123-0123 | no | 507 | 2,9 | empty | no | none |
| NA-0134-0234 | NA-0123-0124 | no | 123 | 2,7,8,9 | empty | no | none |
| NA-0134-1234 | NA-0123-0134 | no | 475 | 2,5,9 | empty | no | none |
| NA-0234-0123 | NA-0123-0134 | no | 127 | 7,8,9 | empty | no | none |
| NA-0234-0124 | NA-0123-0134 | no | 607 | 5,7,8 | empty | no | none |
| NA-0234-0134 | NA-0123-0124 | no | 123 | 2,7,8,9 | empty | no | none |
| NA-0234-0234 | NA-0123-0123 | no | 639 | 7,8 | empty | no | none |
| NA-0234-1234 | NA-0123-0124 | no | 603 | 2,5,7,8 | empty | no | none |
| NA-1234-0123 | NA-0123-0124 | no | 219 | 2,5,8,9 | empty | no | none |
| NA-1234-0124 | NA-0123-0134 | no | 859 | 2,5,7 | empty | no | none |
| NA-1234-0134 | NA-0123-0134 | no | 475 | 2,5,9 | empty | no | none |
| NA-1234-0234 | NA-0123-0124 | no | 603 | 2,5,7,8 | empty | no | none |
| NA-1234-1234 | NA-0123-0123 | no | 987 | 2,5 | empty | no | none |

The 12 group orbits (nine AD, three NA) are:

| Representative | Literal count | Stabilizer | Disk | Sigma | Compatible |
| --- | ---: | ---: | --- | ---: | --- |
| AD-012-012 | 5 | 4 | no | 7 | no |
| AD-012-013 | 20 | 1 | no | 1023 | yes |
| AD-012-014 | 10 | 2 | no | 431 | no |
| AD-012-023 | 20 | 1 | yes | 831 | no |
| AD-012-034 | 10 | 2 | yes | 959 | yes |
| AD-013-013 | 5 | 4 | no | 249 | no |
| AD-013-023 | 10 | 2 | no | 1023 | yes |
| AD-013-024 | 10 | 2 | no | 1023 | yes |
| AD-014-023 | 10 | 2 | no | 959 | yes |
| NA-0123-0123 | 5 | 4 | no | 255 | no |
| NA-0123-0124 | 10 | 2 | no | 95 | no |
| NA-0123-0134 | 10 | 2 | no | 251 | no |

## 5. Named cores and the branch result

The certificate [C44P-AD2-012-034](named_C44P-AD2-012-034.json) has r spokes
{0,1,2}, s spokes {0,3,4}, and root edge 56. Its nonframe edges are
05,15,25,06,36,46,56. Both degrees are four; it has two private vertices and
no mixed component. Its disk uses r's sector from 2 through 3,4 to 0.
Its complete Sigma is 959. At row 6, q=01212, both roots see 0,1,2 and are
forced to 3, which edge 56 rejects. All seven edge deletion colourings and
every accepted-row colouring are saved. The matching identity element
s=1,r=0 gives **933 subset 959 and 941 subset 959** directly in the literal frame.

The certificate [C44P-MIXED3-001](saved_screen/named_C44P-MIXED3-001.json),
catalog name C44P-S0001, comes from the saved critical AD3 source with Sigma956.
Its private vertices are {5,6,7}, with triangle edges 56,57,67 and spokes
5->{2,3}, 6->{0,1}, 7->{1,2}. The retained mixed component is {7}; each original
root's core degree is four. Its complete Sigma is 1022 and its rejected row
0 is 01012. Each triangle vertex then has list {2,3}, so the triangle rejects;
deleting any spoke frees a third colour, and deleting any triangle edge leaves
a two-colourable path. The inherited embedding and all witnesses are saved.
Forward rotation s=1,r=1 sends 933 to 996 and 941 to 998, both contained in
1022. This exhibits compatibility for a retained mixed core as well.

The conditional all-incompatible branch does not apply. In particular the
proposed source-size-independent lemma excluding all two-private-vertex cores
cannot be obtained from this screen. Compatibility leaves ten such disk
placements. No counterexample to the target-source absence statement has been
constructed, since the named cores have Sigma959/1022 rather than a target
relation, and the recorded source of the mixed core has Sigma956. No new
source search, arbitrary-size absence proof, per-spoke-pair case tree or
missing-lemma proof route is pursued after this branch result.

## 6. Algorithms and independent verification

[The saved screen](../../scripts/c5_excess_two_c44p_screen.py) implements its
own literal four-colour DFS, choosing an unassigned vertex with the fewest
available colours. Each accepted row has a complete colouring. Each rejected
row has a four-way tree: every colour either identifies a monochromatic edge
to an assigned neighbour or recursively assigns that colour. A separate
coverage checker validates every rejection tree. Complete Sigma is computed
from these ten decisions, before comparing saved masks.

[The two-private implementation](../../scripts/c5_excess_two_c44p_two_private.py)
uses the list formula above, all edge subsets for minimal cores, its own whole
graph D5/root-swap reduction, the sector test, and saved rotation certificates.
It enumerates all placements before any graph quotient. NetworkX 3.5 supplies
corroborative apex-planarity checks and rotation construction; disk completeness
and nonadjacent impossibility have the preceding paper proof.

[The independent implementation](../../scripts/c5_excess_two_c44p_independent.py)
reads the original C44 inputs and the definition documents, without reading or
importing either new main implementation. For part (a), it uses numeric-order
frontier DP, merging colourings only when their sufficient frontier colour
tuple agrees. For the row quotient, it enumerates all 240 proper literal frame
words and all 24 S4 permutations. For part (b), it independently enumerates
every literal placement and all 16 root colour pairs for every raw frame word,
including each nonframe-edge deletion and every candidate minimal subcore.
This Cartesian computation and frontier DP agree on every full relation and
deletion relation.

[independent.json](independent.json) records both independent tables and the
comparison with every main occurrence and placement. Its checks include
full Sigma, target group actions and matches, disk status, orbit equivalence,
sizes/stabilizers, complete minimal-core lists, acceptance and deletion
witnesses, rejection-tree coverage, inherited source hashes and rotation faces.
No main mathematical routine is imported to establish agreement. The default
and seed17 replays recompute the products and compare exact bytes, not just
saved digest fields.

## 7. Trust boundaries and replay

Paper results here are restriction monotonicity, the complete 125-placement
coverage, the star-sector embedding criterion and nonadjacent impossibility,
the list decision/minimality arguments, and the explicit named-core colouring
arguments. Parts (a) and (b)'s exact tables and cross-checks are finite Python
certificates. Part (a) uses already saved C44 cores through k=9, their saved
source-criticality labels and inherited ER embeddings. It does not newly prove
source criticality or the completeness of that source search.
Part (b)'s graph-shape classification is complete without a source-size bound,
but it has compatible cases and yields no target-source absence theorem.

No four-colour-theorem oracle or unproved boundary-state statement is assumed.
No Lean file changed and no new Lean theorem is claimed; `lake build` was not
run. No new source was searched and no k>=10 enumeration was started.
The individual scientific recomputations are small serial runs; agent
concurrency and all jobs stayed within the requested ceiling of 16, and no
command was estimated above two hours.

From this worktree root, use the pinned interpreter. Initial generators write
only the new task outputs; all later validation is read-only `--check`.

```sh
PY=/home/ray/developer/ai/math/.venv/bin/python
$PY scripts/c5_excess_two_c44p_screen.py --check
$PY scripts/c5_excess_two_c44p_two_private.py --check
$PY scripts/c5_excess_two_c44p_independent.py --check
PYTHONHASHSEED=17 $PY scripts/c5_excess_two_c44p_screen.py --check
PYTHONHASHSEED=17 $PY scripts/c5_excess_two_c44p_two_private.py --check
PYTHONHASHSEED=17 $PY scripts/c5_excess_two_c44p_independent.py --check
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

[The validation driver](../../scripts/c5_excess_two_c44p_validate.py) runs exactly
these nine commands and writes [validation.json](validation.json) with actual
exit codes, command/stdout/stderr SHA256, per-command product-manifest hashes,
and individual code/artifact digests. It deliberately omits the validation
file's own digest to avoid a self-reference.
Final documentation checks and `git diff --cached --check` after staging the
complete bundle are also recorded in that ledger.

The initial checkout's documentation check failed on two archived historical
paths. The authorized `python3 tools/audit_archive.py restore --artifacts`
restored exact bytes successfully: 2,540 files and 1,460 unique blobs checked.
The initial failure and restore result are preserved in the validation ledger;
final document checks are rerun against the restored checkout. No historical
certificate is rewritten. This worktree and its Git directory remained writable;
no standalone clone or bundle fallback was needed. Only this report/evidence/code
bundle and one STATUS index line are committed, with no push or merge.
