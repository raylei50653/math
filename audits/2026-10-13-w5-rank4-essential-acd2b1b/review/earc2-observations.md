# E-ARC2 compositional observations, not adopted closure

2026-10-13; BASE `acd2b1beea6c909edade565a00eeeeac05d2b3a7`.
This note records a read-only research pass before the reviewer was reassigned
to W5. It does not alter any E-ARC2 source ledger or claim a new whole-class
exclusion. No associated source search or complete finite replay was performed.

The current remaining source classes are EARC-NA1, EARC-AD0, EARC-AD1-A4,
EARC-AD1-LOW and EARC-AD2, as specified by the N2-bridge parent ledger.
Generalized N2 is already excluded at its original E4 contract.

The following deductions concern EARC-AD0 only, with all original source,
complete-Sigma, attachment and same-frame hypotheses retained:

1. **Both roots have at most two spokes.** E6 Section 4, lines 119–145, permits
   three spokes only for mask941 and the literal set013. The later pair-critical
   theorem, Section 4, lines 144–156, permits only012/014/034/123 in that mask.
   Their intersection is empty. The statement is a composition of existing
   necessary conditions already required by the parent ledger.
2. **A proper two-root45/54 core omits one original spoke.** E6 gives exactly
   one original unary per root, with incidence `4-t_r`. The previous deduction
   makes both incidences at least two, so an incidence-one unary omission is
   unavailable. The general saturation/core-identity argument then leaves only
   one spoke omission. A single-root exception is still possible.
3. **An original55 core can occur only at an isolated rejected position.**
   `docs/c5_no_mixed_span_budget.md` Section 1, lines 38–48, states the exact
   adjacent-root, no-mixed, minimal-q source contract. Its Section 4 concludes
   that every such minimal core accepts both adjacent singleton positions.
   Applying this only when the actual G is minimal for the selected row shows
   that canonical mask933/940 has no original55 row; every rejected position
   has a rejected neighbour. For mask941, whose rejected set is {0,1,3}, only
   q3 can have an original55 core; q0/q1 require proper cores or the at-most-one
   single-root exception. This does not make G minimal for any selected row.
4. **In a proper45/54 core the high root has two spokes.** Relative to its unique
   degree-five root s, the two original components are U_s and `r+U_r`, with
   incidences `(4-t_s,1)`. The existing single-spoke(3,1) and no-spoke(4,1)
   minimal-q source exclusions remove t_s=1 and t_s=0; t_s<=2 was established
   above. Precise inputs are `docs/c5_single_spoke_three_one.md` Sections 1–4
   and `docs/c5_no_spoke_exterior.md`'s (4,1) source exclusion; their T4/minimal-q
   use is also summarized in `docs/c5_excess_one_subcovers.md` Section 2.

These statements still leave full same-row joints, remaining spoke omissions,
the possible single-root row and the isolated original55 row. They have not
been separately adopted or propagated into the shared documentation. In
particular they do not close AD0, E-ARC2 or Conjecture E.
