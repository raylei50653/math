# A cross-review of the integrated proof and C controls

BASE `9c36e3c4789dfec07d60ec4e042f0bafe17451d1`.
Read-only review targets: root `PROOF.md`, `B/PROOF.md` sections4--6,
and `C/REPORT.md`. The reviewer did not edit these targets.

## Result

PASS for the stated conditional theorem and exact interface.
No unconditional source repair or source exclusion is established
or claimed by these reviewed statements.

## Integrated proof

1. The literal sector table correctly transports the cap faces:
   with f01, z is sector12; with f12, one whole-disk orientation puts
   z in sector61. The two h-only sectors45,56 are therefore safe
   for both cap-centre forms. Replacing g by an arbitrary cap-side
   chord would invalidate this safety premise.
2. The monotone path proof is valid. Each followed chord skips a
   closed interval disjoint from the other skipped intervals;
   matching disjointness and planar noncrossing prevent a backward
   next chord. Successful closure is one actual alternating simple
   cycle avoiding all literal marks.
3. Full-cycle accounting is exact: every used chord and its skipped
   O arc is a complete new cycle; the remaining O arc joins the
   complete cap path through both spokes. Skipped-subarc endpoints
   belong to their pocket cycles. There is exactly one remaining
   full cycle, so `odd(D-N)=j+(j mod2)`. The proof includes all
   vertices and every new complete cycle.
4. The primal facial interpretation also passes: each visited
   exterior triangle either has a root-child P edge, which keeps
   the walk on the root's dual face, or two T vertices, which gives
   the exact opposite-side blocker. Completion is precisely the
   full alternating dual facial boundary. With s children it has
   `s+2` P and `s+2` non-P incidences, giving degree `2s+4`.
   The complete child-subtree cut count gives pocket length
   `sum d_J-2|S|+2`, hence parity equal to the whole subtree's
   degree sum. Original degree bounds correctly exclude the
   no-child four-cycle switch in a source.
5. The thirteen-state interface is necessary and sufficient on one
   actual O. A three-spoke exterior has `|O|-1` complement edges:
   after retaining every even closed component, its unique path
   is even. A one-spoke exterior has `|O|-2` complement edges:
   its two paths have opposite parity. Distinct endpoint pairings
   produce one even combined cycle; equal pairings require
   pairwise equal parity. The exact cap table and no-internal-odd
   condition are retained.
6. The ordered-O bit criterion is a bijection with actual exterior
   matchings. Both endpoints of each old chord must be covered by
   selected O edges together, and each port's coverage equals its
   spoke-removal bit. The e and g coverage equations give exactly
   the required marks. Complete exterior components are then
   reconstructed, not selected independently.

## Independent comparison with C

A's separately implemented recursion and ordered-O assembly agree
on all PMs of the same four fixed graphs:

| C control | All PMs | Joint even PMs |
| --- | ---: | ---: |
| Weak wrong-sector graph | 36 | 0 |
| Literal safe cap-disappearance graph | 47 | 6 |
| Literal even-jump graph | 22 | 3 |
| Literal odd-jump graph | 55 | 6 |

These counts agree with C's full fibre totals. A's independent
complete-cycle computations also reproduce:

* the weak graph's odd jump gives full lengths4,14 but uses g,
  so is not mark-safe;
* the direct literal interval gives one full even20-cycle;
* the other safe nonmonotone cycle gives full lengths9,11;
* the literal even jump gives full lengths3,15;
* the literal odd jump gives full lengths4,16.

C appropriately separates exact named local incidence from original
source realization, identifies the weak graph's wrong z sector,
and retains all complete cycles and empty fibres. Its triangle/
degree failures and missing all-distinct reference for the even-jump
control are not hidden. A's checker does not independently certify
C's oriented sphere rotations or every labelled Tait row; those
remain C's explicitly identified evidence. No inference here uses
these finite graphs as original sources or as all-size coverage.
