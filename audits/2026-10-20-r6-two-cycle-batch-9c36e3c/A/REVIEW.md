# A cross-review

Independent derivation in `A/PROOF.md` preceded reading current B or C.
Cross-review then covered B's completed paper, the root integration,
and C's fixed certificate. Verdict: **PASS within conditional scope**.

The arbitrary-size paired-switch test agrees with the independent A
derivation: all actual blocking triangles must lie at the shared
non-P edge, and all untouched complete residual components must have
even original degree charge. The degree restrictions follow from
`d_J-2d_P`; in particular a source T leaf is excluded because the
partner avoids v,w and has original degree at least five.

B's 5/5/5 specialization checks correctly. A degree-five safe rim
has no child and one blocking face. Its two T neighbours include
the actual outer third vertex t of AB. The other two T neighbours,
a and b, are distinct because otherwise A,B would have a third
common neighbour; the same-source no-separating-triangle authority
forbids that. Degree five at t then forces P-degree two and unique
blocking face tAB. Each pair is admissible, U0 minus the selected
rim remains connected and touched, and the other T branch is the
only untouched component.

During review, both A and root noted that charges 1,1,0 on a
three-node region tree alone do not force two odd tree edges.
B corrected that abbreviated inference: there are exactly two
complete complement cycles; the odd component charge forces at
least one odd cycle; the even order of cubic D then forces both
cycles odd. The current root integration makes no unsupported
stronger inference.

The root integration preserves the same original source, marks,
complete fibres, rotations, arbitrary-size scope, conditional
existence boundary, and reconstruction cost. Its all-batch
component criterion accounts for every full outer or nested cycle.
The 5/5/5 entry remains a conditional source case, not a universal
source degree assertion.

For finite evidence, `A/check.py` reconstructs all C rotations
without importing C code, enumerates all 275 perfect matchings
directly, and checks ten graph-level adjacent-pair candidates,
including one locally rejected candidate in the weak nonliteral
control. Its nine literal candidates agree with C's count. Six
pairs are alternating; exactly three satisfy complete parity. It
independently verifies C's three new positive pair witnesses and
the two 5/5/5 negative witnesses. Normal and seed17 output bytes
agree; damaged rotation and missing matching are rejected.
The successful pair controls have degrees 5/3, 5/3, and 6/4 and
cannot trigger the original source degree assumptions. Two
controls additionally have parallel primal edges. All controls
remain `source_realizability=not triggered`.
