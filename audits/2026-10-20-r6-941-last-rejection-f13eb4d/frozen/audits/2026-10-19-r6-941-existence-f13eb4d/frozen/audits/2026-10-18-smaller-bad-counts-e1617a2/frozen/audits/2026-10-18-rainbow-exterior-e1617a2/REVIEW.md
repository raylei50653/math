# Independent review and integration boundary

BASE `e1617a2756813327d7ad333cfdd0fd92fa9efc38`; 2026-10-18.

Three independent lanes read the frozen original graph contract. A and B
independently found the b-only recolouring obstruction; C reconstructed the
fixed completed graph and its full fibres without importing the prior checker.

- [A review of B](A/REVIEW-B.md) checks all five negative rainbow sectors,
  the accepted fan-B Z path, and the explicitly conditional eight-gon crosscut.
- [C review of A](C/REVIEW-A.md) checks the all-four-site b neighbourhood,
  paired original emptiness, exact inverse maps and fixed colour frame.
- [B review](B/REVIEW.md) checks the integration scope and retains the
  additional simple-exterior hypothesis for the crosscut lemma.

Root independently reconstructed the b recolouring, the removal of the
fourth-colour apex sectors, the exact full-fibre equality, the old accepted
branch split, and the two-colour boundary-anchor pigeonhole argument.
Root also checked that the candidate fan adds only b-incident edges, so the
specified fan-B components use actual surviving original edges.

One scope correction was adopted before integration: failure of this fixed
four-query certificate is not a proof that the candidate belongs to K132.
Another outside-K132 certificate has not been excluded. The published root
report, A/B/C proofs and current guide retain this distinction.

The simple eight-gon crosscut is a conditional paper lemma. Its universal
applicability to the hypothetical source was not verified and is not used to
claim the three fan-B fibres empty. The fixed control has nonempty original
negative fibres, so every source-emptiness implication there is explicitly
not-triggered. Actual control failures carry the resulting original full lifts.

Replay results are recorded in [checks.json](checks.json) and the independent
[C validation record](C/validation.json). The v1 C certificate is retained as
a draft; the current checker defaults to `C/certificate-v2.json`.

Closure scope: the accepting fan-A route to the specified four-query
certificate is excluded under the complete b-neighbourhood hypothesis.
Fan-B acceptance, all three complete rainbow exclusions, source realization,
smaller badness and global closure remain OPEN. No new Lean theorem is claimed.

Propagation: current guide and STATUS changed because the previous choice
of either accepting fan must be narrowed for this certificate. The old
two-fan geometry and acceptance cover remain valid. The direct parent
four-query sufficient certificate remains valid. README/HANDOFF navigation
and research-line tags are unchanged; the older frozen authorities are
unchanged. No commit or push is included in this work.
