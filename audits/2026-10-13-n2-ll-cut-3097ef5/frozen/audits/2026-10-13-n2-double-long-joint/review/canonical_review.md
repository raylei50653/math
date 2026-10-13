# Final independent canonical-document review

Reviewed `docs/c5_excess_two_n2_double_long_joint.md` against the frozen source
contract, `../paper/REPORT.md`, `structure.md`, `../controls/REPORT.md`, the
retained local/control counts, and the matrix artifact. This review does not
modify shared documentation or use the concurrent one-long result.

**Verdict:** the mathematical claims and evidence boundaries are supported.
Two small presentation corrections were reported to the author: explicitly
separate the both-shared case before invoking HD in the T1 paragraph, and repair
the changed independent-review section anchor. An explicit reference to the
adopted full-B-touch support-interval equality was also recommended for clarity.
The final re-read confirms all three corrections are now present; no outstanding
finding remains in this review.

The following points were checked independently:

- The support-size table uses more than a shield-edge lower bound. Full
  B-touch and the original one-sided support-interval theorem give
  `S_C=V(sigma_C)`. The two disjoint long shield arcs consequently have lengths
  `{2,2}` or `{2,3}`, and exactly the displayed support sizes `{3,3}` or `{3,4}`.
- T0 is proved on every fixed designated row using complete original lifts.
  T1 may select a low-contact escape row only when the other piece accepts all
  three designated diagonal cells. The shared, single-block, and arbitrary
  block-chain cases remain accounted for. No result asserts closure for t=2/3.
- The remaining spoke distributions, up to exchanging roots, are `(2,0)`,
  `(1,1)`, and `(2,1)`. Their legal pin rectangles have 8, 9, and 6 cells,
  respectively. Hence at most nine binary cells and at most 512 assignments
  are correct for the remaining branch; this is an interface bound, not a
  bound on the sizes of the two original pieces.
- LL-CUT is explicitly scoped to that remaining full-source branch. Its basic
  certified cells and the strengthened `+diag` version remain distinct.
  Feasible matrices are not promoted to actual rejected fibres or source
  realizations. A refutation must use the same qualified original source.
- The old exact four-contact path has support012, so its original shield is
  precisely the two edges01,12. Another long's edge-disjoint shield cannot
  have all its vertices inside012: a connected arc with at least two edges
  on those three vertices would reuse01,12. Thus the other original mixed
  piece really does have an attachment at3 or4. The two displayed original
  K3,3 constructions therefore exclude this exact path from the requested
  two-long source, without excluding unrelated high-contact all-I pieces.
- The minimum k=4 statement is confined to the retained local diagonal
  obstruction, using the already adopted low-contact theorem under its local
  premises. It is not claimed to minimize a qualified original N2 source,
  any arbitrary failed joint, or all possible counterexamples.
- The reported finite counts agree with the artifacts: 320 local cells,
  80 empty local cells, 856 local tuples, 160 joint cells, 181 full global
  lifts, 48 collision-plus-capacity triggers and 29 cross-collision triggers.
  The supplemental minor artifact has four K5 controls, 20 bag spanning
  trees and 40 original cross adjacencies, with zero full T1/target triggers.
  The matrix artifact has ten literal control rows and all 81 abstract
  incidence profiles, and records maximum remaining dimensions nine/512.
- The exact local path and the fixed two-path graph are identified as local
  controls, with nonplanarity and target nontriggering explicitly stated.
  Existing Lean build success, if reported in the receipt, is not a new
  formalization of these paper arguments.
- The frozen full hypotheses and adopted pre-existing inputs suffice for all
  new proofs. The concurrent one-long exclusion is neither invoked in T0/T1
  nor used to establish the new double-long residual. Its mention as separate
  working-tree activity does not change the authority of the frozen audit.

No new source enumeration, full-source counterexample, full `(2,0)` closure,
commit, or push is asserted by this review.
