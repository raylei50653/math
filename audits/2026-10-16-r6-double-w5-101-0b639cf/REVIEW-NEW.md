# Independent review of the new double-W5 deductions

**Historical preliminary review, superseded by [REVIEW.md](REVIEW.md).**
The partial boundary described below preceded the radius-two proof.
The final integrated proof excludes the entire double-W5 class; the
remaining OPEN case is the nonwheel seven-cut alternative.

2026-10-16; research BASE `0b639cf`. Reviewer: the independent agent
that first reconstructed the preceding chorded-five proof in
[REVIEW-PRIOR.md](REVIEW-PRIOR.md), without consulting its old REVIEW.
This review records independent derivations from the actual face bits,
the exact curvature identity, and previously adopted original-source
theorems. It will be supplemented after the integrated PROOF is fixed.

## 1. Sector count and disjointness of the wheels

I independently checked the draft [RESEARCH-B.md](RESEARCH-B.md).
Its basic face-bit identity is exact. For a two-W5 barrier the entire
cut budget is spent on the two components, so S has no internal edges
and no edges to X. Common-111 saturation puts f between two different
components. Thus the only equal-bit primal adjacencies are the three
literal marks and the ten wheel spokes; their bits are 00 for vw,mz
and 11 for pq and the spokes.

At m, each original s/t interval has endpoint faces 0. No internal 00
transition is available. A singleton 1 block has two transitions, and
a wheel 11 block has three. Counting the actual source interval gives
`d_G(u)-3=2k_u+3t_u`, where t_u counts m-wheel centres in that original
sector. Since `d_G(u)<=8`, two wheel blocks cannot occur in one sector.
This is a count on the retained rotation, not an arbitrary binary word.

The curvature identity then gives exactly three preliminary rows:

* m in no wheel: both original degrees are odd and at least seven;
  the upper bound forces `(s,t)=(7,7)`, m has degree nine, and its two
  excess units force `r_cap=0` and all other excess zero.
* m in one wheel: epsilon is one, so `r_cap=0`, excess is zero, m has
  its even minimum eight, and the degrees are `(6,7)` or `(7,6)`.
* m in both wheels: `r_cap=1`, excess is zero, m has its odd minimum
  seven, and both original degrees are six, with one wheel per sector.

In the last row, the sector word is exactly 0110. The corresponding
wheel rims contain m,w,alpha and m,v,beta respectively. At a degree-four
pin v or w, the transition 00 across the actual vw edge and the spoke
transition 11 cannot share an incident face, so they are opposite in
the four-face rotation. If d is the actual third vertex of the other
vw face, the wheel rim therefore contains both m and d. Applying this
at v and w places two distinct vertices m,d in both rims, contradicting
`r_cap<=1`. The third row is genuinely excluded for arbitrary size.

Thus the two complete wheel neighbourhoods are disjoint. Every vertex
other than possibly m has its exact parity-sensitive minimum degree.
The first two rows give the claimed improvement `s,t<=7`.

One small presentation repair was identified in B3: if the other v/w
pin entered the SAME m-wheel, it would not create a second m incidence.
It is instead excluded because an induced wheel rim cannot contain the
triangle m,v,w. Entry into the other wheel creates the forbidden second
m incidence. With these two cases stated, the claimed v/w membership
classification is valid.

## 2. The original zpq face is a singleton

The complete star of a wheel centre contains exactly its five component
faces. If face zpq were in either wheel component, that centre would
be one of z,p,q. The adopted centre-outside-T theorem excludes all three.
The face is neither in X (the marks are vertex-disjoint in D) nor in S
(it is an endpoint of f, so common-111 saturation puts it in a residual
odd component). With only the two wheels as nonsingleton components,
zpq is therefore a singleton odd component. This argument applies to
each wheel, not merely to a selected one.

Saturation also puts the other endpoint of f in a different component.
Before further geometry, the exhaustive possibilities are another
singleton or one of these two wheels. It cannot join the two wheels,
and zpq itself cannot be assigned to either wheel.

## 3. A shorter source contradiction excludes f entering a wheel

The established disjointness and zero excess away from m make this
subcase especially rigid. If the other pq face is in a wheel with
centre u, then u cannot be p or q. Since the triangle contains its wheel
centre, it is exactly pqu; hence p,q are rim vertices of this same wheel.
Both pins lie in exactly one wheel neighbourhood. Their initial marked
odd parity is flipped once, so their exact J degree is four. The retained
source identities give `d_G(p)=d_G(q)=5`.

Now use the adopted **original-source double-low theorem**:

`d_G(p)=d_G(q)=5 => d_G(ell)>=6`,

where ell is the third vertex of the actual pq face opposite zpq. Its
primary authority is
[`c4-return-branches/pq/PROOF.md`, section 5](../2026-10-14-c4-return-branches-a11d4bb/pq/PROOF.md).
The hypotheses are precisely the globally minimum, secondary
maximum-edge no4ct source with original x,y,b of degree four; there is
no source-order upper bound or high-apex assumption. In this subcase
ell is literally u. But a retained original W5 centre has complete
original degree five, giving the contradiction `5>=6`.

I checked the cited theorem's proof rather than relying only on its
appearance in a source classification table. Deleting p,q exposes the
actual C4 disk K with the unchanged inner edge xy. The original cap
lifts transfer the full xy-palette constraint to K. Assuming ell has
degree five exposes its actual degree-three deletion disk L. Every
complete L colouring has no rainbow outer row, a nonempty ABAC/BC
fibre, and an empty ABAB/BC fibre. The original return lemma switches
the actual BC component of the last outer vertex and injects the former
full fibre into the latter, preserving the same xy edge palette. The
inverse switch recovers the original complete colouring. This is an
arbitrary-size contradiction with the original source, not a finite
local colour table promoted to source existence.

The return lemma's authority is
[`c4-c5-recursion/fibre/PROOF.md`, section 1](../2026-10-14-c4-c5-recursion-fdd3e22/fibre/PROOF.md).
Its use in the double-low theorem preserves actual disk boundary order,
the no-rainbow premise, and the same original edge xy. The proof supplies
the nonempty starting fibre. No independent matching witness or graph
is substituted here.

Consequently f joins two singleton components. A separate useful converse
checks the p/q position: if p were on a wheel rim, its four-face rotation
would have the 11 transition pq and the 11 spoke. They cannot be opposite,
which would make every transition 11, contradicting the exact equal-bit
edge list. Their common face must be the non-zpq face on pq, placing that
face in the wheel already excluded. Thus p and q avoid both wheel rims.
The argument at q is identical. Both pins consequently have J degree five
and original degree six in every surviving double-W5 case.

## 4. The proposed longer fan closure

I also reconstructed the longer proposed contradiction, conditional on
the same disjoint-rim and exact-degree deductions. It is sound, but the
source double-low theorem makes it unnecessary.

Write the f-wheel rim `p,q,A,B,C`. The degree-four p,q links force the
actual edges zC,zA. Once the original low-p/q theorem gives a,c at least
six, a z-wheel would imply h=3, contrary to a+c at least twelve. Thus z
is in no wheel, its exact degree is seven, h=4, and a=c=6. Its actual
induced link is `m,alpha,C,p,q,A,beta`.

B differs from alpha and beta: otherwise the wheel edges AB or BC would
be respectively the forbidden chords A-alpha or C-beta of that link.
The vertices A,C are outside T because they neighbour z, and neither
can be v or w. They have exact degree five. The known facial incidences
at C give the link path `B,u,p,z,alpha`, forcing B-alpha to close it;
at A they similarly force B-beta. If B is v or w its five distinct
neighbours already contradict exact degree four. Otherwise B is outside
T with exact degree five, and its link path `alpha,C,u,A,beta` forces
the forbidden edge alpha-beta. Every count uses distinct literal vertices;
the induced z link handles the potential identifications.

## 5. Additional h=3 exclusion

The z-sector word deserves combining with the existing source table.
Because zpq is a singleton and zp,zq are not spokes or marks, each of
these edges is a bit change. Counting from the forced mz face to the
face just before zpq gives exactly

`a0-4=2k_a+3t_a`, `c0-4=2k_c+3t_c`,

where `t_a+t_c` is the number of z-wheels (zero or one). This remains
valid when alpha=p or beta=q: the corresponding intermediate word has
zero transitions. Zero excess away from m gives z degree six when it
is on a wheel, hence h=3. The sector equations then force
`(a0,c0)=(7,4)` or `(4,7)`.

However the adopted h=3 source classification, under the same x,y,b
degree-four positions, permits only `(a0,c0)=(5,6)` or `(6,5)`.
See the full named residual table in
[`no4ct-C8/REPORT.md`, section 3](../2026-10-13-c5-no4ct-c8-6cafdfb/REPORT.md):
among its eight rows, imposing extras zero at x,y,b leaves exactly
c04-941 and c07-941. Thus both z-wheel macrotypes are excluded.
This is reuse of an adopted arbitrary-source necessary classification;
it is not new bounded-source enumeration or a source realization claim.

Every remaining double-W5 case therefore has z outside both wheels,
z degree seven, h=4, and `(a0,c0)` among `(4,8),(6,6),(8,4)` before any
additional original-source exclusions. Together with the first two
m rows and the singleton-to-singleton f placement, this is a genuine
new restriction of the proof boundary. It still does not exclude every
double-W5 source or the separate nonwheel seven-cut case.

## 6. Scope of this review

The deductions above pass independent paper reconstruction, including
the indicated B3 presentation repair. The integrated proof, custody
manifest, checker and final verification records remain to be reviewed
when present. No computational PASS or source example has been inferred
from this paper review. Ordinary and even-complement matching existence,
the full 319 exclusion, and unbounded catalogue equality remain separate
OPEN obligations.
