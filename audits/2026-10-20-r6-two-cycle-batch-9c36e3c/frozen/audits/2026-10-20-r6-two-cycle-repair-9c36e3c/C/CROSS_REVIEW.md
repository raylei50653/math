# C independent review of A and B

Read A/PROOF.md and B/PROOF.md after the four-control seal.
The actual alternating-switch calculations in all four C controls agree with
A's complete-cycle description, the formula `j+(j mod2)`, and the exact mark
test. In the weak no-repair control the otherwise successful odd-arc chain
contains g, precisely exposing the missing literal z-sector requirement.
The literal no-descent control additionally shows that using an exterior-side
chord can retain complete oddness2 despite safety and cap disappearance.

A's thirteen-state test correctly requires complete exterior closed cycles in
addition to the open path pairing. Its |S|=3 and |S|=1 parity counts retain the
entire odd-order O, rather than marginal parities. Its Boolean selection of O
edges covers both endpoints of each original matching chord together; this is
exactly the local matching constraint, and the complements in A3 follow
edge-by-edge. No source witness is inferred from the finite interface.

B's face interpretation is compatible with the explicit controls. The direct
positive has safe root degree4 and no child, which B excludes in the actual
source. The odd-jump positive has root degree6 but its child degree4; the pocket
has length4. The even-jump negative has root degree6 and a child degree3; its
pocket is the complete odd3-cycle. These checks demonstrate why the fixed
controls calibrate the combinatorial formulas but do not trigger the source
branch with all degree assumptions.

One wording issue was sent to A: in its complete main-cycle description,
skipped-subarc endpoints belong to their separate pocket cycles. The main
cycle contains only O vertices outside the union of the **closed** skipped
subarcs. This is a wording clarification, not a change to A's edge-by-edge proof.

B's bounds also give explicit additional source failures of C's literal
controls: the no-descent graph has d(m)=5, the even-skip graph d(m)=3, and the
odd-skip graph d(m)=4, all below the actual source bound d(m)>=7. The smaller
controls have no original completed source, no complete U319 fibres or lifts,
and no source-realizability authority.
