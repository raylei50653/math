# R6-CAP-BARRIERS independent adoption review

2026-10-16. Scope: the same full no4ct minimum C5 source, fixed degree-four
x,y,b and degree-six r, literal J and its embedded dual, all three marks.
The root agent read all three proofs and checked the following arguments
independently. B reviewed A separately; C's independent A/B review is
retained in [C/CROSS_REVIEW_AB.md](C/CROSS_REVIEW_AB.md).

## Weighted curvature and wheel components

Accepted [A1--A4](A/PROOF.md). The even-parity minima contribute exactly
`-2+0+4*2=6`; changing parity contributes +1 at m and unmarked vertices,
and -1 at z and the other four pins. Each degree slack is a nonnegative
even integer. Thus `12=Q-L` is an equality for the original J.

The barrier bit assignment counts every internal component edge and
every possible location of the forbidden edge. It is essential to use
D[C], not silently identify it with H[C]. For a wheel, an internal
forbidden edge would turn H[C] into an odd path, violating
factor-criticality. A centre at a forced endpoint meets X. Together these
exclude every marked centre and justify the literal wheel support.

The sole-W5 bounds are 8 or 10 for tau=0 and at most10 for tau=1.
The sole-W7 bound is at most10, even before its centre's degree slack
is subtracted. These contradict Euler12 at every source size.
For two W5 components, their disjoint sets of faces exclude adjacent
centres; the overlap consists of rim vertices. Starting with all T odd,
every symmetric-difference flip raises Q by one except m. This yields
the exact equality `L=2(1-r_cap-epsilon)` and the stated degree bounds.
The bounds s,t<=8 and h<=6 apply only in this two-wheel subcase.

The W5-side identification is valid: the five-cut is a bond, since two
components of its complement would require at least six outgoing edges.
If the W5 were on the side opposite C, all four X vertices would lie
in its dual C5. Any four C5 vertices induce three edges, contradicting
the original induced forced pair with exactly two. This supplies the
missing side assignment before applying the sole-wheel exclusion.

## A single common matching family

Accepted [B1 and the common-cut identities](B/PROOF.md). For every actual
M111, each odd residual component requires a positive odd number of
matching crossings. At most |S| incidences come from S and two from h;
q=|S|+2 forces every bound to be an equality. It applies to every violating
S, including nonmaximum ones and those with even components.

The intersection/union and difference cut equations are direct matching
edge counts. The parity of the intersection selects two odd sets, each
requiring at least one crossing, so the two remaining counts must be
one and the extra twice-counted term zero. The matching is common to
both original barriers throughout. This is not a claim that arbitrary
independent matching witnesses can be joined.

The re-marked control is explicitly auxiliary: its maximum primal degree
is six and it has no declared original source contacts. Its ordinary
joint failure already has singleton barriers, which the real source
excludes. It refutes only the proposed weaker even111/cyclic-four-cut
shortcut. It does not refute the source target.

## Original pentagons and allowed exchanges

Accepted [C1--C3](C/PROOF.md). Every displayed pentagon lift uses original
edges, distinct original vertices, and at most one vertex of each
identified pair. Any diagonal of an empty original cap survives as a
chord. A single degree-five cap centre cannot be a removed inner vertex
of degree at least six or an original boundary vertex. Its complete
five-neighbour set survives injectively. A's side lemma then permits
using this wheel for an actual induced five-cut barrier.

Noninduced five-cut boundaries are kept separate; an exterior chord
does not automatically contradict factor-criticality. Likewise a
seven-cut component is not silently treated as a disk or wheel.

Accepted the later C1.3 after reading [A's independent interval review](A/REVIEW-101-INDUCED5.md).
In 101, removing the three excluded face-edges from link(m) leaves only
the two literal original sector paths and isolated z. At z, removing
the two excluded face-edges leaves P_z and isolated m. An opposite-fan
subpath of P_z necessarily traverses pq, so its cap contains the actual
face zpq. B1 then puts pq on the boundary; with z on that same induced
pentagon, the triangle zpq is a contradiction. Thus each induced
five-cut component in 101 is a wheel, and the sole-five-cut row must
have a noninduced boundary. This proof also covers the endpoint
identifications alpha=p and beta=q; no numerical control is claimed
to certify this Jordan-interval statement.

For C3, a cubic cycle has one unused incidence per vertex. If both drawn
sides contain vertices, three-edge-connectivity requires at least three
attachments on each side. This rules out nonfacial triangles and squares;
the primal minimum degree rules out facial triangles as well. Squares
are consequently the degree-four faces v,w,p,q. Their marked-edge
membership gives the claimed single/batch restrictions, without assuming
that larger permitted exchanges exist or decrease oddness.

## Evidence and limits

Paper arguments establish arbitrary-size implications. Finite checks
reconstruct their stated algebraic or local graph controls; all minimum
source numerical tests remain `not triggered`. In particular B's actual
control cap pairs have zero crossing-pair triggers; its 720 separate
K3,3 checks calibrate the algebra, not source geometry.

All adopted statements preserve the same complete graph and marked
frame. None proves an ordinary joint matching, an even endpoint, or
completed-source descent. W110+W101>0, full319, the general T/T0 problem
and K-infinity remain OPEN. The previous k+5 reconstruction cost and
numerical bounds are unchanged. No new external theorem or Lean result
is asserted.
