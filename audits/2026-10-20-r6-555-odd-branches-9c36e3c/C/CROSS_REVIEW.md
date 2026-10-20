# C review of the independent A and B proofs

Reviewed [A/PROOF.md](../A/PROOF.md) and
[B/PROOF.md](../B/PROOF.md) after independently rebuilding every matching
and cut of the frozen local 5/5/5 odd-branches control. Result: **PASS**
for the conditional four-vertex repair; no coverage statement is inferred.

Both proofs preserve the same actual source, original matching, ordered
contacts, literal marks, complete fibres and full lifts. Their local
`t=τ` notation is expressly separated from the original split apex t;
their local a,b,c labels do not rename original source contacts.

The original degree-five stars force the complete list of twelve actual
triangles touching `X={h,A,B,t}`. The two internal triangles are hAB and
tAB. The other ten, in the given order, form one simple dual decagon.
The crossed primal edges alternate between the five original P edges
`LA,at,tb,BR,hu` and the five original non-P edges
`hL,Aa,tc,bB,Rh`. Thus the construction switches one actual alternating
cycle of the fixed M and respects the original rotations. It does not
rely on separate marginal local rotations.

All four selected vertices avoid the actual marked endpoints. The new
matching retains e and g and omits f individually, so the stronger
P101 condition holds. No new choice of marks is made.

The complete new component partition is exactly `{u}`,
`(T-t) union {A,B}`, and `(U0-{A,B}) union {h,t}`. The first follows
from deleting uh. The second is connected through the actual path
`a-A-B-b`; it contains both entire T branches. The third contains the
entire connected remaining U0 and attaches h via L,R and t via c.
The complete change list leaves no edge between these sets. The parity
calculations use full original degrees and give zero separately for
all three components. The frozen region-tree criterion then handles
every full complement cycle, including the outer one.

The finite replay agrees in one simultaneous witness: row 55, selected
vertices `{2,5,6,8}`, component degree sums `4,26,36`, unchanged mark
type 101, and full complement lengths `4,18`. The explicit complete
cycles agree with the paper formula `C4 disjoint-union C_(|O|+3)`.

The argument does not need the two branches to be odd. Their two odd
values in the requested subcase are absorbed in the same actual
connected new component, so no untouched odd component is hidden.
Both independent proofs correctly limit their conclusion to the
conditional 5/5/5 geometry. The finite control has degree-three
vertices and parallel primal edges; neither paper proof derives its
source authority from that control. Source realization is not triggered,
and universal coverage and other degree patterns remain open.
