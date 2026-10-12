# Fixed-evidence boundary-partition fibre controls

The fixed controls pass. Every tested interface equality class has one
permutation of the four colours taking its representative's **complete ordered
tuple relation** onto every member's relation, including empty relations.
External-colour collision slack also holds in every triggered saved cell.
This is calibration of the uniform laws on saved pieces; source realization,
N2-55, and E-ARC2 remain separate and OPEN.

## Frozen scope and tuple custody

`../BASE.json` fixes head
`8b76dcc82adabba679e7b0d2ef6dbe6eb9cc37f3` and twelve exact snapshots.
The checker verifies every snapshot's byte size and SHA256 before reading
evidence. It uses only the saved full fibres in the long-mask controls and
high-contact controls, with the original component-slack observations as a
second custody check. It never imports the old motif generator or enumerates
new source graphs or attachment patterns.

The 228 saved local pieces consist of 179 original components, 45 saved bounded
motif exemplars, two saved joint-control pieces, and two saved high-contact
pieces. All are connected and every C vertex has total degree four. Each piece
retains its ordered original C vertices, ordered roots and contact ownership,
original region edges, actual boundary attachments, and actual support.
The local region owns precisely edges incident with C. The complete original
graph's remaining fixed-fixed edges are checked separately in each full join.
No rotation or source realization is supplied by this calibration.

The source of each full relation is its frozen file SHA256, JSON pointer,
original row index, and ordered pin index. Cell index is `16 * row + pin`.
`cell_maps` records target cell, representative cell, a four-colour permutation
index, full relation size, and SHA256 of the complete transported relation.
The checker reads and maps every original full tuple; it does not establish
bijections by comparing counts or marginal palettes. Empty cells remain explicit
in the 160-map coverage of every piece. The tuples themselves stay in the frozen
sources, so this artifact does not duplicate them.

## Complete relation checks

| Check | Result |
| --- | ---: |
| Frozen input hashes and byte sizes | 12 verified |
| Original-source component row identities and full fibre custody | 1,790 |
| Saved local pieces | 228 |
| Complete local cells independently recalculated by DFS | 36,480 |
| Complete local ordered tuples checked | 106,760 |
| Explicit empty local cells | 3,643 |
| Complete representative-to-cell tuple bijections | 36,480 |
| Maps using a nonidentity colour permutation | 24,816 |
| Actual-support-plus-roots equality classes | 5,246 |
| Original graphs plus named joint graphs | 63 + 2 |
| Full same-row, same-ordered-pin joins checked | 10,400 |
| Explicit empty full join cells | 7,534 |
| Complete global rows reconstructed and independently recalculated | 650 |

The 179 original pieces also match the original component-slack vertex sets,
edge sets, root order, literal row colours, and all full local fibres. Their
saved global full lifts match the older source hashes using that source's
original compact JSON encoding. The new relation hashes use sorted,
two-space-indented JSON followed by a newline, as defined in `encoded`.

## The uniform three-arc state space

For each of the five ordered consecutive arcs `(a,b,c)`, the interface
`(a,b,c,r,s)` has exactly 26 equality partitions across the ten saved boundary
rows and sixteen ordered root pins. There are ten classes with `a=c` and sixteen
with distinct endpoints. The complete class memberships are saved in
`boundary_geometry.ordered_three_arc_interface_classes`; root roles stay
ordered. This gives a reusable 160-to-26 reduction for a fixed piece supported
inside such an arc, without a separate proof for each contact pattern.

There are 203 saved pieces with support contained in at least one consecutive
three-point arc, giving 248 fixed piece/arc incidences. Every incidence has
diagonal rejection mask in `{empty, Eq(A), Diff(A), I}` on the three target rows.
The `three_arc_incidences` field records its mask type and the full 26-class
off-diagonal interface filter, including actual roots.

## External-colour collision slack

For each saved cell the checker inspects the **actual external neighbours** of
each original C vertex. If two distinct external neighbours receive the same
fixed colour, the full fibre must be nonempty. A trigger records the original
C vertex, the two actual external neighbours, and their common fixed colour;
the complete frozen fibre supplies all witnesses.

| Collision-slack control | Cells / classes |
| --- | ---: |
| `triggered and holds` cells | 24,715 |
| `not triggered` cells | 11,765 |
| Empty cells among `not triggered` | 3,643 |
| Degree-four hypothesis not applicable | 0 |
| Collision equality classes on actual support plus roots | 3,694 |
| Residual equality classes on actual support plus roots | 1,552 |
| Full 26-class three-arc incidences, counted with multiplicity | 6,448 |
| Collision-filtered three-arc classes | 4,464 |
| Residual three-arc classes | 1,984 |

Collision is invariant under the recorded full interface partition: every
member of a class has the same collision status. All 3,643 empty local cells
occur in classes where the collision trigger is absent. Absence of this trigger
does not assert rejection: many cells in the residual classes remain nonempty.
The residual class count depends on the actual attachment and ownership map;
in these 248 incidences it ranges from 3 to 19 of the 26 classes. This is a
uniform partition filter with fixed graph geometry, not a universal claim that
every piece has the same list of surviving classes.

## Two edge-disjoint arcs

For each cyclic labeling `(a,b,h,c,d)`, take `A=(a,b,h)` and `B=(h,c,d)`.
The remaining literal original boundary edge is `da`. `Eq(A)` and `Eq(B)` cannot
hold together: they would give `a=h=d`, contrary to properness on `da`.
The checker verifies this on all 240 labeled proper four-colour C5 boundaries,
in each of the five rotations. The argument itself only uses that literal edge.

Consequently, an `Eq(A)` rejection together with a `Diff(B)` rejection has an
escape on an `Eq(B)` row; the symmetric mixed case uses an `Eq(A)` row. The saved
three-row sets contain those rows in every rotation. Two `Diff` masks cover all
three target rows, and in fact cover all 30 labeled proper three-colour C5
boundaries with a fourth spare diagonal colour D. This explains that obstruction
uniformly instead of treating individual motifs as separate cases.

These statements concern diagonal rejection classes. Each actual graph join
still uses one original row and one ordered pin pair, with all complete local
tuples joined at those same coordinates. Independently chosen local
permutations do not authorize joining pieces from different original rows.
The saved `negative_separate_path_escapes` graph is retained and its complete
same-row join rejects all three diagonal target rows despite separate local
escapes.

The saved `four_contact_long_path` has full rejection mask I. Therefore a
universal mask law excluding I is a `counterexample`, even for three-consecutive
support. The four-class law itself includes that witness.

## Deterministic replay and corruption controls

Run from the repository root:

```sh
python audits/2026-10-12-n2-boundary-partition-law/controls/checker.py --check
```

The replay independently recomputes all fixed cells and joins, checks all
tuple maps, compares the entire observation artifact, and verifies the receipt
including checker and observation hashes. To test a separate artifact, use
`--artifact PATH`; this follows the same complete map verification path.

The following deliberate corruptions are rejected: a complete fibre digest
changed while keeping its tuple count, omission of an empty cell, substitution
of the wrong colour permutation, and one tuple colour changed while retaining
the relation size. The last case invokes the same complete tuple-bijection
routine used for positive checks. The independently invoked CLI also rejects
a copied artifact with a changed complete-fibre digest and returns nonzero.

`verification.json` records PASS and these rejection reasons. Complete target
sources: 0 (`not triggered`). N2-55 and E-ARC2: OPEN. No Lean result, source
exclusion, source realization, or parent closure is asserted.
