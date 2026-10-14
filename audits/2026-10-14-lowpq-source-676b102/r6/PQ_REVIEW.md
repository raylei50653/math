# Independent review of the low-p source exclusion

Reviewed [the low-p proof](../pq/PROOF.md), its [checker](../pq/check.py),
and the connected [root report](../REPORT.md), from the literal original
source and the prior cofacial full-fibre contract. This is a separate
paper review by the r6 worker; it does not replace the main certificate.

**Verdict: the arbitrary-size implication p=5 => a>=6, and its literal
reflection, are supported by the stated source assumptions.** The proof
does not exclude the whole p=5 branch or mask319.

1. **Original nonedge r-ell.** The cycle `(y,a,p,ell,r)` is simple and
   proper if r-ell is assumed. The original boundary edge ya fixes its
   bounded side. At y that side contains t, so the existing original
   small-C5 theorem forces t to be the unique W5 centre. The resulting
   original edge tp contradicts the already established p=5 => a>=5.
   This uses no new colouring assumption and is sufficient to rule out
   the third possible loop in the later quotient.

2. **The actual two faces and the identification.** Prior p=5,a=4
   exclusion gives m!=t, and the actual deleted faces Q and P share only
   z. The z-r and z-ell arcs occupy different open faces and share one
   endpoint; their union is an embedded tree. Each of the three pairs
   in `{z,r,ell}` is an original nonedge, so the contraction introduces
   no loop. Original edges between different equivalence classes remain,
   modulo suppression of parallel copies. No assumption that r and ell
   are individually cofacial is required.

3. **Strict minimum-source budget.** D has k vertices, the quotient k-2,
   and the cap adds three. Its specified C5 thus has k-4 interior
   vertices, strictly below the original k. An edge survives, and the
   cap is in the original comparison class even if the quotient is not
   triangulated. The catalogue's nonemptiness therefore gives an actual
   complete colouring and a complete pullback to the one D.

4. **Universal lifts, not independent witnesses.** For any pulled-back
   colouring with z=r=ell=A, p has at least one legal colour. Every such
   p colour yields a complete R colouring, so empty ABAC forces s=t=B.
   The ABAB palette condition applies to every p lift with that same
   unchanged q. It forces q=C, then forces m=B because otherwise p=B
   would be a legal forbidden lift. Thus the complete ABABCAB fibre is
   nonempty. Its forced equality m=t contradicts the actual tm edge
   when a=5. This is a source exclusion, not only a necessary model.

5. **Arithmetic check.** An independent direct enumeration, importing
   no audit checker, iterated all 4^7 pin assignments, the two four-face
   edge sets, and all 4^3 ordered p,x,y cap assignments. Among the 324
   proper labelled rows satisfying z=r=ell, exactly 24 have every full
   T0 lift obeying the failing equal-palette condition. They are exactly
   the common S4 renamings of ABABCAB, each with two full cap lifts.
   This agrees with the main checker and root's independent checker.
   The main checker's product table is compared to direct original-edge
   tests for every proper labelled row; its certificate retains empty
   cap fibres as well. The universal condition includes vacuous rows
   elsewhere, but no quotient-slice row is vacuous: p has a lift and
   z=r guarantees a legal xy cap.

6. **Scope and historical evidence.** Old ABABCBC and new ABABCAB are
   separately existing colourings of the same D; the proof does not
   combine them into a single colouring. The p=q=5 result remains only
   a,c,ell>=6, with h>=4 before any other source-domain restrictions.
   The two a=5 low-degree explorations are correctly marked as contained
   checks. The root report preserves p5a>=6, r6p5/r6q5, mask319, and the
   unrestricted higher-r and T/T0 branches as OPEN. Its statement about
   t=5,a=5 is restricted to the low-p intersection, as required.

The finite calculation verifies local lift arithmetic only. The face
geometry, nonedge, cap construction and arbitrary-size implication are
the reviewed paper steps above. The report's source-realizability,
external-enumeration, Lean, and global-catalogue limits are correct.
