# C review of B and root integration

Reviewed the current `B/PROOF.md` against frozen BASE
`9f1fe84f73aabfa87a33d28754633bae6bf0b707` and the actual written formulas.
This is independent paper cross-review, not source realization or Lean.

## Findings

1. B1's complete-cut oddness formula is correct. A fragment complement
   partitions into closed components and full paths, including internal
   length-zero paths at repeated exterior endpoints. Every newly closed
   global cycle uses the actual paired paths and actual joining edges.
2. B2's partial composition is associative on the retained data: a closed
   component has no exposed port and can close only once. Intermediate
   min-plus minimization is legitimate because the interface retains
   everything used by later gluing within the stated matching domain.
3. The structural-state bound is finite for fixed boundary/mark counts,
   while integer oddness costs remain unbounded. The necessary parity
   equation correctly counts `n = r + sum(path lengths) + sum(cycle lengths)`.
4. B3's direction is correct: old response no larger than smaller-patch
   response transfers every smaller-patch success back to the old graph.
   Contraposition transfers old failure to the smaller graph. Equality of
   full matching tables is unnecessary for that one optimized query.
5. One substantive wording issue was found and corrected: minimizing the
   joint predicate can change internal mark membership from 101 to 110.
   The theorem now preserves actual exterior matching, literal mark
   identities, and target predicate; exact memberships require a further
   conditioning key. This is appropriate for the combined objective.
6. Same-source application remains conditional on exact relational
   factorization in the retained full source key. A formal tag alone does
   not supply original colouring/lift extension. B states this limitation
   and the completed-source size obligation explicitly.

The corrected statements pass. This review does not independently replay
B's finite checker; the root replay is recorded separately.

## Root REPORT section 4

The rank/quotient statement and the effective rank-one consequence are
consistent with C1--C3. In particular every e-preserving even reference has
one positive region containing all old odd cycles at an odd joint minimizer;
full positive regions from different references therefore overlap.

Requested clarification: the arbitrary-size one-region concentration controls
are not asserted globally minimizing for a fixed affine family. The rank
bound itself gives no bound on the odd-cycle count inside a region; do not
upgrade those controls to unbounded oddness at a source joint minimizer.
