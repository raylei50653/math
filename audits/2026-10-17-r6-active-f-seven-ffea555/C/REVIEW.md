# C independent cross-review of A, B, and the root integration

2026-10-17; frozen BASE `ffea555fc2a896d8166ce198ca28ed9262912f25`.
Reviewed the current [A](../A/PROOF.md), [B](../B/PROOF.md), and
[root integration](../PROOF.md) against the relevant copied inputs.
This review writes only `C/`; it does not modify those reports.

## Findings

No mathematical blocker was found in the stated source-conditional
paper results. The reviewed versions keep arbitrary ordinary P101
matchings separate from complete-colouring witnesses and make no
existence claim for the four residual degree rows.

* A's opposite-degree-four implication uses the two actual primal
  triangles at a shared dual incidence, followed by the actual z,p,q
  triangle. Its seven-cycle application is valid because pz or qz is
  on the two-face boundary unless it is the shared centre edge; the
  ordinary centre is explicitly different from z. Its same-side
  alternative uses the adopted original low-p/q degree bound.
* A's degree-six argument applies only to centres p,n_a or q,n_c.
  The complete original degree-six rotation supplies a distinct extra
  vertex alpha or beta. Its dual spoke collides with the already
  selected g at the actual outer face. The p,ell and q,ell_q positions
  are not upgraded to the stronger degree-seven conclusion.
* B conjoins separately proved **graph nonedges** from two nonempty
  complete fibres of the same original graph. It does not combine the
  fibres' private colour values or their Kempe components. Its exclusion
  of ell-v/ell-w uses a full original degree-five link in precisely the
  ordinary-centre subcase; its further citation of a stronger existing
  result is explicitly distinguished.
* B's Q5 disk description is supported by the frozen fact that every
  primal triangle is facial. Adjacent centres have exactly the two
  common neighbours given by their actual incident faces. Their star
  boundary is therefore the specified simple five-cycle; the adopted
  matching-spoke argument supplies its inducedness. The localization
  excludes m,v,w from this boundary and includes z; it makes no claim
  about the full exchange graph's connected components.
* B's mark exteriority and distance follow from the absence of centre
  incidences and then from the matching identity at a marked endpoint.
  Distance at least two is correctly kept separate from reference-region
  separation, including paths through remote complete complementary
  cycles.
* The root keeps the universal source-conditional degree exclusions,
  necessary localization, and conditional R100 descent distinct. Its
  remaining separator obligation has the correct existential quantifier
  over **one actual complete all-distinct source colouring** for each
  fixed M and C. Its joint-minimizer formulation is the contrapositive
  of the conditional descent, rather than a proof of separation.
* The root retains one- and three-spoke R100 references, all complete
  outside components in oddness accounting, the zero reconstruction
  cost on the same D, and the unchanged completed-source cost k+5.
  Joint positivity, complete319, and other odd-defect classes stay OPEN.

The root's reference to the Kempe move/update discussion should point
to **C section 6**, not C section 5. This is a section-label correction,
not a proof gap; the root has been notified.

## Scope

The evidence read for this review is the current paper text and the
sealed original geometry, low-p/q fibres, collar, and seven-cycle
classification. It is not a new certificate replay or a finite source
realizability check. No new tests or theorem authority are introduced.
No commit or push was performed.
