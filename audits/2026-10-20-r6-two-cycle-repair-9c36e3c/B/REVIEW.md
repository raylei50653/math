# Independent review and checks

BASE `9c36e3c4789dfec07d60ec4e042f0bafe17451d1`.

1. B independently checked A's literal cap-face lists and f/z sectors.
   They agree with B's original-source normalization.
2. A's monotone forward argument is valid: a later backward chord
   would either reuse a matched endpoint or cross an already skipped
   chord. Its full complementary-cycle decomposition and
   `j+(j mod 2)` oddness formula are valid. The preliminary wording
   “outside interiors of skipped subarcs” omitted the fact that both
   jump endpoints belong to the detached cycle; A corrected this to
   exclude the entire closed skipped subarc.
3. B independently enumerated all local cap matchings from the eight
   literal internal cap edges. There are 15 local states: seven with
   one selected spoke, seven with three and one with five. Exactly 13
   contain no closed odd cap component. Full component/path data are
   in [independent-check.json](independent-check.json). This checks the
   interface algebra only, not source realization or existence of an
   exterior witness.
4. B verified the additional frozen original-J input byte count and
   SHA256 against [INPUTS.json](INPUTS.json).
5. A independently reviewed B's side/sector geometry, literal z/f
   positions, named g-branch cut count (G1)--(G2), and complete facial
   characterization (S1)--(S2). No mathematical defect was identified.
   The ordinary degree bound correctly excludes the finite `s=0`
   four-cycle control from being an actual safe-sector source repair.

The principal new source result is conditional: a safe rim vertex
with alternating incident matching membership and even degree sum in
every detached child subtree yields an actual even-complement
P101 matching by flipping its entire dual face. Neither independent
review proves that every original source has such a vertex, nor that
another admissible matching repair must exist if both vertices fail.

## Final integration review

B independently read the integrated root `PROOF.md` and `C/REPORT.md`
after the source and finite-control results had been combined.

* The root link to B section 6 uses the correct heading anchor.
* The integrated facial-switch statement retains the actual rotation,
  the entire attached P subtrees and every complete new complement
  cycle. Its degree count and even-degree-sum equivalence agree with
  (S1)--(S2), with degree at least six conditional on a successful
  alternating facial switch.
* The integrated exact exterior interface retains the complete same O,
  the common e/f/g test and all closed components; it makes no
  independent marginal or source-realization assertion.
* C correctly separates its weak no-repair graph, which fails the
  literal z sector, from the controls retaining the local named
  incidences. Its safe cap-removing switch explicitly retains both
  complete odd cycles, and the jump-parity controls retain all their
  complete cycles. Each control remains outside the original-source
  authority.

No substantive defect was found. The only suggested wording refinement
was to repeat “on success” in the integrated degree-at-least-six
sentence, so that it cannot be quoted in isolation as an unconditional
degree bound on both safe rim vertices.
