# Cross-review: complete two-sheet common-graph covers

Reviewed `../2026-10-15-kempe-state-covers-6ddea32/PROOF.md`, `REPORT.md`,
`SEARCH_NOTES.md`, `check.py`, `space.py`, `certificate.json`, and both formal
graph files. The input hashes and replay receipts are recorded in
[CROSS_VERIFICATION.json](CROSS_VERIFICATION.json).

**Verdict: PASS in the stated Layer0/common-graph domain.** The two explicit
graphs are complete-colouring witnesses, not selected subsets of their proper
colourings. No full720, planar-source, degree/collar, or complete319 exclusion
follows. The paper states those limits correctly.

## 1. Cover definition and hidden components

The projection preserves the literal seven-pin row and all six actual maximal
bichromatic component partitions. Each visible transition is an actual
component exchange on one common original graph. Global S4 acts on the whole
colouring and preserves the original graph and named pins. These are the
required compatibility conditions; the definition does not assume a section.

A hidden component exchange preserves the literal pin row but can change other
pair partitions, and hence can change an abstract state in the full five-layer
table. The reviewed paper explicitly distinguishes this from a hidden-loop
cover. Its lower bound is correctly stated as

`m_pin(F) >= sum_P 2^(h_ab+h_cd) - 2`.

Within a complementary pairing, hidden components are disjoint and every
subset gives a distinct complete colouring. The three resulting cubes meet
only at the original colouring: a changed vertex determines the unique
complementary pairing containing its old/new unordered colour pair. This
proves the bound on the complete literal-pin-row fibre. Applying it to a
single abstract-state fibre requires the stated hidden-loop hypothesis, or
uniqueness of the state with that row. Layer0 has that uniqueness.

The diamond example has the actual edge set `01,02,12,13,23`, all48 proper
colourings, and24 triangle rows. At row ABC, the fourth vertex is A or D;
the visible AD switch at pin0 fixes it, whereas global AD changes it.
The resulting contradiction excludes an S4-equivariant switch-compatible
section. It does not presume that either of the two lifts can be discarded.

## 2. Two-sheet classification and search scope

Every base row uses at least three colours, so its S4 stabilizer is trivial.
Choosing sheet labels over each canonical row and transporting by S4 therefore
introduces no additional stabilizer data. A visible switch uniquely specifies
its changed pin block and colour pair, so the undirected edge-orbit encoding
does not conflate distinct parallel switch generators. Reversibility, square
equations, and canonical-row gauge changes give the stated binary voltage
classification. The exact rank calculation replays to quotient dimension117.

The extra visible-product/global-transposition equations are an additional
restriction. They are valid for the two actual graphs because all components
are visible. They cannot be imposed on arbitrary covers with hidden components.
Their quotient dimension is13 over all five layers and9 on Layer0. Thus512 is
only the restricted Layer0 search domain. The discovery counts are expressly
exploratory; none is needed for the positive graph theorem or promoted to an
exhaustive arbitrary-cover/source exclusion.

## 3. Independent complete original-edge verification

[check_cover75.py](check_cover75.py) does not import the reviewed implementation.
It reads the75-vertex original edge list, fixes the original z,p,q triangle to
0,1,2, and exhaustively enumerates all remaining colourings by a separate
single-vertex search. It finds36 normalized colourings in1462 search nodes.
Their24 global renamings are exactly the864 full tuples prescribed by the
graph's colour vectors. All432 literal Layer0 rows have exactly two lifts.

Original-edge BFS independently checks all8160 actual component exchanges and
26112 complete complementary-pair cube masks. Every component meets a pin,
and every projected partition and successor agrees with the frozen old table.
The same direct exchanges give inconsistent equations for an S4-equivariant
section. The complete evidence, including all36 normalized colourings, is
[cover75-independent.json](cover75-independent.json).

Normal and seed17 runs agree. A certificate missing one complete normalized
colouring is rejected. The formal `graph-75.json` is byte-for-byte identical
to the independently checked immutable discovery graph. The reviewed official
checker also passes normal and seed17 runs for both graphs, including all
20736 global actions per graph. Root separately verifies the121-vertex graph
from original edges in `../2026-10-15-route-round4-6ddea32/check_cover_graph.py`
and `cover-graph-independent.json`; it obtains the same36/864 counts and
8160/26112 component/cube counts.

The six-step actual visible closed walk in PROOF §6 has total sheet voltage1.
Its base endpoint is its start, while its complete-colouring endpoint is the
other sheet. This excludes any visible-switch-compatible section, even without
requiring S4 compatibility. It is stronger than the independent section
equation check and follows directly from the verified lifted transitions.

## 4. Retained boundaries

The two complete graphs realize Layer0's18 canonical rows and outer mask319.
They do not realize the whole720-state table or all22 rows. Their edge counts
prove these displayed simple graphs nonplanar. Neither the maximal-type-graph
construction nor that density argument excludes a different planar graph,
a suitable edge subgraph, or a construction with duplicated function types.
No original source rotation, collar, degree conditions, or completed-source
descent is supplied. Those domains, omega=0, and the general claim remain OPEN.

No file in the reviewed audit or any previous audit was edited by this review.
