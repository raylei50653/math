# A cross-review of independent executable evidence

This review is read-only outside A. It distinguishes independent graph
compilation, finite whole-graph checks, and the arbitrary-size paper theorem.

## B local compiler

Read `B/check_local_operators.py` in full and independently ran
`python3 -B audits/2026-10-19-c5-pr-disk-semantics-ed59843/B/check_local_operators.py --check`.
Exit status was zero. The replay reported 5,120 local assignments, 200 integer
matrix entries, 2,048 formal-mask transfers, 264 source transitions, and four
rejected controls. It independently obtained 312 proper P patch colourings,
240 proper R patch colourings, and 240 proper literal target tuples per
operator.

The compiler defines the six-vertex P graph and five-vertex R graph before
reading the source matrices, and enumerates assignments against their actual
edges. It therefore does not derive its answer from a supplied transition
table. Its new boundary orders match A's paper construction. The final matrix
comparison is a comparison to the imported claim, rather than its definition.

Every proper literal target has all ten source slots, including empty slots;
each stored local assignment includes a permutation of the whole palette.
The code checks the inverse palette permutation on every vertex, and checks
all S4 orbits and invariance under target recolouring. In particular it does
not identify separate boundary marginals. Improper target tuples are rejected
by the actual new boundary edges during the exhaustive local assignment
enumeration. The retained detailed fibre tables concern the 240 proper target
tuples; the remaining improper cases are also covered by the explicit gate
in A's full literal fibre statement.

The four controls change the rotation, remove the old-b0 spoke, omit source
colour transport, or transpose the matrix convention. Each fails a concrete
coefficient comparison. No material finding.

## C whole-graph construction and fibre enumeration

Read `C/check_full_graph.py` in full and independently ran
`python3 -B audits/2026-10-19-c5-pr-disk-semantics-ed59843/C/check_full_graph.py --check`.
Exit status was zero. The replay reported 792 graph cases, 7,920 complete
canonical literal fibres, 2,278 empty fibres and 10,642 complete colourings;
all matrix and support comparisons passed. Seven controls were detected.

The graph constructor retains every original edge and vertex. P adds exactly
the three named edges and the two consistently oriented triangular cells;
R only changes the boundary starting point. The validator checks every edge's
cell incidence, Euler characteristic, orientation, connectivity, and every
boundary/interior vertex link. For these finite constructions this is a
substantive cellulation check, rather than just unconstrained planarity.

The fibre enumerator fixes literal boundary colours and exhausts assignments
on every interior vertex by graph constraints. Its branching heuristic does
not use source matrices, source masks or canonical row transitions. Matrices
are used only afterwards to form the independent comparison counts. Fibre
entries retain the complete assignment, with empty string representing the
unique empty interior assignment and empty list representing an empty fibre.

These cases reproduce the two grammars' minimum representatives and their P/R
successors. They corroborate the arbitrary-size bijection but do not replace
it or constitute source coverage for all disks. No material finding.

## Root integer decoder

Read `check_count_decoder.py` in full. Its multiplication order executes each
word left to right on column count vectors. Its observation rows match
`(9,1,4,6)`, and its ten selected coordinates match A's count-decoder
corollary. The symbolic `D E = I` check proves the result for all nonnegative
integer ten-vectors. The two image equations use ordinary addition in the
count case, correctly distinguishing it from Boolean OR in the support case.
The symbolic converse uses ten independent coordinates and verifies `E D`
on the constrained image. No material finding.

The integer matrix identity does not prove graph legality; that authority is
A's fibre theorem and B's graph compilation. Likewise the count decoder does
not mean that the complete sets of source colourings are recovered from just
their cardinalities, and no universal 132-state count machine is asserted.

Independently ran
`python3 -B audits/2026-10-19-c5-pr-disk-semantics-ed59843/check_count_decoder.py --check`.
Exit status was zero, reporting the integer left inverse, exact nonnegative
integer image and frozen custody all passed.

## Integrated report

Reviewed the complete root `REPORT.md` against A's proof and the frozen source
matrices. The arbitrary-disk class permits chords and does not rely on the
132-state closure; its fibre statement uses a fixed source graph and a fixed
literal palette. Each P table entry and each R table entry agrees with the
independent literal table in A's review. The count inverse has all ten correct
coordinates and ordinary addition in its redundant count equation. Seed counts
and per-operation interior costs agree with the actual graph definitions.

The transfer of the older 132-state lower bound is justified: every F word now
has a legal graph interpretation with the same support, and the distinguishing
common suffixes remain legal from each actual graph. The report correctly
limits that claim to support behaviour in the generated grammar, distinguishes
it from counting machines, and leaves all-disk grammar coverage open.

Two editorial path errors were reported to root for correction before final
sealing: use `A/additional-inputs.json` for A's custody manifest and the singular
`C/check_full_graph.py` for C's replay script. Also requested the explicit word
`proper` before the target-beta fibre equation; the section's fibre definition
already restricted its domain to proper tuples, but this makes the gate
precondition immediate to readers. No unresolved mathematical finding.
