# B cross-review of A

Reviewed `A/PROOF.md` only after independently completing `B/PROOF.md`.
Verdict: **PASS within the stated conditional scope**.

The following points were checked independently.

1. The same-old-colour criterion is exact. A selected minority vertex
   makes its triangle monochromatic, and selecting both majority
   vertices does the same. These are respectively the bad-corner and
   P-independence conditions. No other triangle type fails.
2. The full region adjacency graph is a tree even when some primal
   components border several nested cycles. The shore formula in (A4)
   cancels internal boundaries twice and retains the specified complete
   cycle once. It therefore supports both the all-even criterion (A5)
   and the complete odd-count formula (A6).
3. For a selected opposite-valued adjacent pair, all shared triangles
   remain nonmonochromatic. The two actual shared triangles account
   for exactly two bad corners in total. Checking their locations,
   as A explicitly requires, is essential; the sum alone is weaker.
4. The boundary of the two dual faces is one simple alternating cycle
   under the rotation test. Mark preservation follows from the literal
   selected vertices, not a relabelling of e,f,g.
5. The complete component list after the switch is exhaustive. In
   particular the residual component containing the remaining Q5 path
   need not be presumed touched; A's definition correctly retains it
   among the untouched components when appropriate.
6. The merged-component parity cancellation is valid. It uses the
   original charges `q(K2)=q(T)=1`, `q(U0)=0` and equal parity of the
   two selected degrees. It does not require each touched component
   separately even or exclude repeated incidences to a touched piece.
7. The untriggered source-realizability boundary, absence of a universal
   pair witness, and unchanged complete reconstruction cost are explicit.

The independent B proof adds exact source degree restrictions, excludes
T leaves from this pair family, and treats the coupled 5/5/5 case.
These additions do not repair the remaining existence gap in A.

## Root integration review

Reviewed the root `PROOF.md` after the independent proof and A review.
Verdict: **PASS within the stated conditional scope**. Its section 5
correctly requires all three actual degrees to be five, excludes v,w
as the shared outside vertex, derives two complete T branches, and
retains their common odd-parity obstruction. It does not infer that
this degree pattern occurs in every source or that equal branch
parities must be even.

One exposition defect in B's own section 7 was corrected during
cross-review: three region nodes with charges 1,1,0 alone do not force
two odd region-tree edges. The corrected proof explicitly uses that
the two complete complement cycles cover the even-order cubic D.
At least one is odd by the component criterion, so both must be odd.
The root integration does not rely on the defective abbreviated
inference.
