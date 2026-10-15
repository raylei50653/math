# Cross-review: three-edge ordinary matchings

Reviewed `audits/2026-10-15-three-edge-matchings-6ddea32/PROOF.md`, `check.py`,
`certificate.json` and `graphs.json`. Their exact hashes are in
[logs/matching-independent.json](logs/matching-independent.json).
**Accepted within the stated conditional source domain; no blocking issue found.**
No file in the audited directory was changed.

The induced-matching argument keeps the original six named endpoints. A dual
endpoint is an original triangular face, so two original disjoint marked edges
cannot share a dual endpoint. If the two forced dual edges had an extra edge
between their endpoints, the corresponding two original triangles would share
two vertices. For vw/pq this forces one of pv,pw,qv,qw; for vw/mz it forces zv
or zw. The source nonedges therefore justify the stronger induced conclusion.
It is not inferred merely from pairwise disjointness of the three dual edges.

Deleting the four endpoints X of the forced edges and the forbidden edge h
gives an exact complete residual-PM bijection. Cubicity, three-edge connectivity
and exactly two internal X edges give `3q<=3|S|+10`; even order makes
`q-|S|` even, so every violation has deficiency exactly2. Adding two adjacent
universal vertices verifies maximum matching deficiency2 using only the stated
Tutte theorem. Selecting a largest-cardinality violating S correctly eliminates
even components and proves every remaining component factor-critical by applying
Tutte after deletion of an arbitrary vertex.

The cut-budget calculation uses **all** components of H-S and original Q edges.
S degrees contribute `3|S|-2|E(S)|-|E(S,X)|`; X contributes
`12-2|E(X)|-|E(S,X)|`; the deleted h contributes2 exactly when its endpoints lie
in different remaining components. Substituting q=|S|+2 gives
`sum mu+|E(S)|+|E(S,X)|=3-|E(X)|+tau`, hence1+tau in the source. The table of
at most two5-cut components, or one7-cut component, follows without discarding
the all-singleton case.

For a connected5-cut component, three-edge connectivity makes its complement
connected (two complementary components would already need at least six cut
edges). The bond therefore corresponds to a simple primal C5. When it avoids
m,z, the forced-edge endpoint faces put both complete primal stars outside the
component. Applying the stated source cap theorem then leaves an empty
pentagon or W5; the empty cap's three-face dual tree is not factor-critical.
The resulting W5/localization is a necessary source restriction, not an
exclusion. The7-cut and all-singleton possibilities remain explicitly OPEN.

The factor12 in the complete-colouring counts is correct: three choices of the
common nonzero edge difference and four original root colours, multiplying the
full `2^c` even-complement lift count. Odd-complement fibres remain empty. The
ordinary PM residual test says nothing about positivity of W when its family is
nonempty. The proof keeps these two failure mechanisms separate.

The original checker replay passed; stdout/stderr are in
`logs/matching-cross.stdout` and `logs/matching-cross.stderr` (stderr empty).
The independent [review_matchings.py](review_matchings.py), without importing
the original checker, re-enumerates all PM using reversed vertex branching,
reconstructs residual families, complement parity and full/empty fibre counts,
checks every Tutte deletion set, and rechecks all maximal-barrier
factor-critical deletions and cut budgets from original Q edges. All four
controls pass. The reviewed hashes and detailed counts accompany its output.

Petersen is expressly a nonplanar control; the weaker triangulation controls are
not full minimum sources. The auxiliary residual H is not treated as a smaller
completed C5 source. Source ordinary-family existence, even-complement positive
counts, complete319 exclusion, and the general main claim are not established
by this review.
