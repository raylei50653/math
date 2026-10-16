# C independent review of A and B

2026-10-16, frozen BASE f1faf743833c51ddc5efbe9e0f390b87b9f2311d.
Read A/PROOF.md and B/PROOF.md after writing C/PROOF.md. This review is
paper-level; each worker remains responsible for its independent replay.

A: ACCEPT. The forward AD obstruction uses the absent ABCBD row; the
reverse obstruction uses the actual unique r=A lift and its full palette
requirement, rather than source projection alone. Jordan separation uses
four distinct alternating outer endpoints, and the retained wt edge fixes
both w,t outside the swapped s-component. A BC component swap retains its
vertex set, giving the claimed literal inverse on every private colouring.
The reflected t-map uses one common graph reflection/colour renaming.
For the count, every all-distinct row has exactly one of z=v,z=w; in either
sector the literal three-colour frame is uniquely recovered, so its 24
permutations are disjoint. Therefore N=24(n0+n4) has no double-counting.
Under source FJ, patterns010 and001 exclude the only alternative two-equal
triple; with fixed Tait colour each weight has four primal root lifts,
then the three equivalent Tait colours give N=12W010=12W001. The new
nonempty H_p/H_q lift follows from m equalling exactly one pq endpoint,
not from combining separate cofacial witnesses. The proof retains the
forbidden target W110/W101 as OPEN.

B: ACCEPT. Removing both internal M0 edges from the one-port pentagon
leaves exactly two exterior arcs; the noncrossing pairing and single-cycle
condition force P14/P23. Replacing P23 by x2x3 is alternating and simple;
the two distinct ports ensure a strict length reduction. The inserted
edge is a real unmarked spoke and the original Q avoids e,g. Thus the
minimality argument forces f onto the discarded arc, as stated. This is
a protected-root obstruction, not an oddness decrease. The 32-port table
retains the 21 empty rows and its unique five-port filling explains why
fixed-port local rematching cannot remove the odd pentagon. The explicit
shortest-Q negative calibration is correctly limited to an arbitrary
shortest choice, since an even endpoint occurs at the same minimum length.
The source colourings supplied by A are not merged with M0 or N.

No permission or publication authority is inferred by this review.

Independent C replay also passed:

`python3 -B audits/2026-10-16-r6-319-continuation-f1faf74/A/check.py --check`
returned zero, reconstructing 16,384 positions and eight finite component
map rows, with the all-distinct-free support266.

`python3 -B audits/2026-10-16-r6-319-continuation-f1faf74/B/verify.py --check audits/2026-10-16-r6-319-continuation-f1faf74/B/certificate.json`
returned zero, reconstructing the32/11 port table,30 local Tait rows,
all four controls,186 one-port and193 three-port checks.

The initial replay invocations omitted each script's required check flag:
A safely rejected exclusive creation of its existing certificate, and B
rejected the missing output/check argument. Both were rerun with the
correct read-only arguments above. No A/B file was changed.
