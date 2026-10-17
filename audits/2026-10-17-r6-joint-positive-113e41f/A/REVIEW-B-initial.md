# Independent A review of B's six-cycle claim

Reviewed the B/PROOF.md draft at BASE
`113e41f7023aa00c8257b815ce8727035b648f26`, against the frozen continuation
C sectors and the additionally frozen low-p theorem. This is a mathematical
cross-review, not a source-realizability test.

**Verdict on the reviewed draft: B1 passes; B2's mp branch passes; the stated
all-six-cycle B2 and therefore B3 do not yet pass.** The obstruction is the
mq branch, not the local empty-cap diagonal arithmetic.

1. The compulsory complete H fibres legitimately forbid ip,iq,jp,jq and
   zi,zj. Separate existential full witnesses suffice to forbid separate
   actual edges; they need not be superposed. The exact common-neighbour
   calculation at v then follows from its full four-neighbour J link.
2. In the mp branch, the six-cycle has order `(v,m,p,q,h,w)`. The two Q
   neighbours p,w of m are both in L_t, since mp makes alpha=p. The quotient
   pentagon therefore lifts literally to `(t,p,q,h,w)` in original G.
   The original vertices a,b are exterior, so the three actual faces
   `tpa,apb,bpq` occupy the exterior Q wedge at p. Their facial incidence
   proves that the complete outside link arc is t,a,b,q; extra neighbours
   cannot be inserted into this arc. The original proper-C5 small-cap
   theorem applies on the actual bounded side; the original collar is
   exterior, so this cap is a strict smaller-source subproblem. The two
   possible remaining diagonals are th,ph, giving the unique empty cap,
   while the singleton W5 cap gives the stated other inside arc. Both force
   original p degree five. The frozen low-p theorem excludes this together
   with a degree four. This is a valid arbitrary-size mp-branch exclusion.
3. The other connector is genuinely different. Its six-cycle is
   `(v,m,q,p,h,w)`. Deleting the v ear yields `(m,q,p,h,w)`. Now mq makes
   beta=q, so **q belongs to L_s while w belongs to L_t**. These two
   incidences cannot both lift through one original representative of m.
   In particular `(t,q,p,h,w)` need not even be an original cycle (tq is
   absent), and `(s,q,p,h,w)` need not be a cycle (sw is absent). The
   original proper-C5 cap theorem is unavailable for this crossed quotient
   pentagon. Literal reflection swaps v,w as well as p,q and s,t; it sends
   the hypothesis v5 to w5, so it cannot silently prove this second branch
   under the original v5 hypothesis.
4. The proposed cyclic-six-cut-to-bond argument itself is correct: if a
   side containing a cycle were disconnected, its cyclic component would
   have at least four exiting edges, because a three-cut is trivial and
   the other side also contains a cycle. Another component contributes at
   least three, exceeding six. But its application inherits B2's missing
   mq branch.

A sound immediate replacement is: under original v5, any six-cycle through
both marks, if one exists, must have the **crossed** order
`(v,m,q,p,h,w)`, with `mq`, hence original c degree four. There are none
when mq is absent. The reflected statement under original w5 has the
corresponding reflected crossed residual. This is a positive narrowing of
actual six-cycles, and does not exclude that residual or prove joint
positivity. A checker of only the two local cap alternatives cannot validate
the missing source lift, since those alternatives already assume a literal
original C5 exists.

No source instances were supplied: not triggered. No finite zero or local
cap certificate can substitute for the missing all-size crossed-branch
argument. No old evidence, B output, source relation or shared routing was
changed by this review.
