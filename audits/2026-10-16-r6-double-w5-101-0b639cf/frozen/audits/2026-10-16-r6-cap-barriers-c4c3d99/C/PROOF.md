# R6-CAP-BARRIERS C: lifted pentagons and the first possible exchanges

BASE `c4c3d99`. Fix the full original globally minimum, secondary
maximum-edge no4ct source and the same legal `J=U/(s=t)`, `m=[s=t]`,
`D=J*`. The three literal marks are `e=(vw)*`, `f=(pq)*`, `g=(mz)*`.
All original degrees, sectors, rotations, complete colour fibres and
all-r obligations are retained. No graph is replaced in the conclusions.

Inputs are the frozen [source geometry](../frozen/audits/2026-10-15-j-source-geometry-6ddea32/PROOF.md),
[previous oddness proof](../frozen/audits/2026-10-16-r6-joint-zero-c4c3d99/B/PROOF.md),
and [original-sector proof](../frozen/audits/2026-10-16-r6-joint-zero-c4c3d99/C/PROOF.md).
The results below are arbitrary-size paper statements. The finite local
check at the end does not supply a source or prove a descending exchange.

## C1. Induced pentagons that do not cross an original sector

Keep the literal disjoint sectors `L_s,L_t` at m and `L_a,L_c` at z
from the previous C proof. Their common-neighbour exceptions alpha,beta,
including alpha=p or beta=q, remain literal original vertices.

**Theorem C1 (lifted pentagon).** Let Q be an induced C5 in J. It bounds
one retained original degree-five W5 cap whenever one of these holds:

1. Q avoids m and z.
2. Q contains m alone, and its two neighbours on Q both belong to L_s
   or both belong to L_t.
3. Q contains z alone, and its two neighbours on Q both belong to L_a
   or both belong to L_c.
4. Q contains both hubs. Write its order `m,z,u,v,w,m`; this order is
   possible because inducedness forces mz to be a cycle edge. Then
   `(u in L_a,w in L_t)` or `(u in L_c,w in L_s)`.

Here "retained original W5" means that the centre is an original G
degree-five inner vertex, all five original spokes survive, and its
complete degree in J is still five. The theorem identifies a disk on
one side of Q. It does not assign that side to a separately specified
Tutte component.

**Proof.** Case 1 is the frozen short-cap theorem. In case 2 replace m
by s or t, according to the common sector. This gives a literal proper
original G C5 with the same other four vertices. In case 3 replace z
by a or c. The original proper-C5 cap theorem also applies to these
cycles that contain an original boundary vertex. In case 4 replace
the consecutive pair m,z by t,a or s,c, using the original edge ta or
sc respectively. Each displayed lift is a simple original cycle, and
the specified quotient maps its five vertices bijectively onto Q.

The bounded original disk is empty or a single full degree-five W5.
An empty triangulated pentagon has a diagonal. In each displayed lift
that original diagonal survives and would be a chord of Q. Thus the
empty case contradicts inducedness.

The remaining disk has a centre with exactly its five cycle neighbours
in G. This centre cannot be an original boundary vertex, because it is
strictly inside the original bounded disk. It cannot be any of the
removed inner vertices r,s,t, whose original degrees are at least six.
Therefore it is retained. No two of its five neighbours are identified:
the lift uses at most one of s,t and at most one of a,c, and its five
images were already shown distinct. All its five spokes survive, and
it has no other original edge from which an additional J incidence
could arise. The original bounded cap is consequently an unchanged
drawn W5 disk in J, with centre of complete J degree five. QED.

The centre is also different from v,w,p,q. Indeed v,w have an original
edge to r, and p,q have an original edge to b. Neither r nor b occurs
on any lifted rim above. Such an extra edge would contradict the
centre's complete original degree-five wheel neighbourhood.

**Corollary C1.1.** An induced J C5 that is not the rim of a retained
original W5 must cross an original sector. With only m on the rim its
two neighbours occupy opposite s/t sectors; with only z they occupy
opposite a/c fans. With both hubs and the order above, the only remaining
pairs are `(L_a,L_s)` and `(L_c,L_t)`.

This extends the preceding induced-C4 restriction to the non-W5
pentagons. The crossed alternatives are necessary, not realizability
claims. Some could still bound a degree-five J wheel whose centre is
one of the special vertices and did not have degree five in G.

### C1.2. Side assignment for an actual barrier component

Suppose a component C of either barrier has an actual induced C5 primal
cut boundary satisfying C1. Let X be its four forced dual vertices.
Then C is exactly the dual five-cycle inside the W5 side.

Indeed, the simple primal cut cycle divides the sphere into precisely
the two sides C and its complement. If C were opposite the W5 disk,
all four vertices of X would be among that disk's five dual faces.
Any four vertices of a five-cycle induce exactly three edges. This
contradicts the frozen induced-forced-pair identity
`D[X]={a,b}`, which has exactly two edges. Therefore C is the W5 side.

Together with [A3](../A/PROOF.md#a3-no-single-wheel-barrier), this
excludes every sector-compatible induced boundary in a one-five-cut
barrier. If two five-cut components both satisfy C1, both are actual
wheels and A4's simultaneous overlap and degree rigidity applies.
This application explicitly resolves the side choice; it does not
declare an arbitrary noninduced cut boundary to be induced.

### C1.3. Every induced five-cut boundary in direction 101 is a wheel

**Theorem C1.3.** In the 101 residual `H=D-X-f`, where
`X=V(e) union V(g)`, choose any maximum-cardinality Tutte barrier.
If a component C has an induced five-cycle Q as its actual primal cut
boundary, then C is a complete retained original W5 component.
Consequently a one-five-cut 101 barrier must have a noninduced boundary.

**Proof.** The two faces on mz belong to X, so neither belongs to C.
Thus `mz notin Q`. If Q contained both m,z, their retained edge mz
would have to be a Q edge by inducedness, a contradiction. If Q avoids
both hubs, C1 and C1.2 already give the conclusion.

Suppose Q contains m alone. Because Q is a simple Jordan boundary,
the faces of C incident with m form precisely one consecutive angular
interval between Q's two rays at m. This interval is nonempty. Among
the excluded faces in X are `mvw`, `mz alpha` and `mz beta`.
In the literal link cycle of m these are the three edges
`vw`, `z-alpha` and `z-beta`. Deleting those edges leaves the singleton
z and the two original sector paths L_s,L_t. The nonempty C interval
must lie in one of these paths, so Q's two neighbours at m belong to
the same original sector. C1.2 now applies to C1 case 2 and gives the
retained W5 component.

Suppose instead Q contains z alone. Again C has one nonempty angular
face interval at z. It avoids the two forced faces `mz alpha` and
`mz beta`. Deleting their link edges `m-alpha`, `m-beta` leaves the
singleton m and the actual path P_z from alpha to beta through p,q.
Thus the C interval is a subpath of P_z. If its two endpoint rays
belong to the same original a/c fan, C1 case 3 and C1.2 give the wheel.
If they belong to opposite fans, the unique subpath between them
contains the edge pq. Therefore the actual dual vertex corresponding
to the face zpq belongs to C.

The common 111 matching saturation theorem [B1](../B/PROOF.md#1-every-violating-set-is-aligned-with-every-111-matching)
gives tau=1: the forbidden edge f joins two different components of
H-S. Since zpq is one endpoint of f and lies in C, its other endpoint
lies outside C. Hence `f in delta_D(C)`, or equivalently `pq in Q`.
But Q also contains z. The three vertices z,p,q are a facial triangle
of J, and an induced five-cycle cannot contain all three vertices of
a triangle. This contradiction excludes the opposite-fan case.

The endpoint identifications alpha=p or beta=q do not alter either
interval argument. They shorten the relevant sector paths but retain
the specific faces `mz alpha`, `mz beta` and `zpq`, and the edge pq is
still the unique transition between the two disjoint a/c fans.
All cases give the asserted wheel component. Finally, [A3](../A/PROOF.md#a3-no-single-wheel-barrier)
excludes a maximum barrier whose only non-singleton component is this
wheel, proving the consequence for one-five-cut 101 barriers. QED.

For two five-cut components this theorem applies to each induced
boundary separately. If both boundaries are induced, both components
are wheels and A4's exact common-neighbour and degree restrictions
apply. No conclusion here excludes a noninduced five-cut boundary or
settles a seven-cut component. The original-sector interval argument
was independently reviewed in [A's review](../A/REVIEW-101-INDUCED5.md).

## C2. The positive joint minimum has fewer exceptional pentagons

For the same joint family

`F_e={M perfect matching of D: e in M, |M intersect {f,g}|=1}`,

suppose it is nonempty and its global minimum `omega_e` is positive.
Choose any global minimizer M. The previous complete integration lemma
gives its unique unordered primal bit partition and induced
monochromatic graph B. A shortest odd cycle Q of B is induced in J
and has length at least five.

**Corollary C2.** Such Q has length at least seven, is a retained
original W5 rim, or is a pentagon in one of C1.1's crossed sectors.
In direction 110, the last alternative cannot contain both hubs.

**Proof.** Apply C1 to the length-five case. In direction 110 the
literal bit partition has m and z on opposite sides, so a monochromatic
cycle cannot contain both. In direction 101 the hubs have the same
bit; no corresponding exclusion follows. QED.

When Q is a retained W5 rim, every rim vertex has one bit, so its
centre has the other bit: otherwise a wheel face would be
monochromatic, contradicting the partition lemma. The five primal rim
edges have duals in M, while the five spokes do not. Therefore the five
actual wheel faces form a whole odd pentagonal component of D-M,
including when the rim contains m or z. This is a same-graph oddness
conclusion and does not identify a Tutte factor-critical component.

This improves the old residual "a pentagon through either hub" to
"a pentagon crossing an original sector", while retaining W5 and long
odd cycles as separate residuals. It does not show any such pentagon
is removable by a permitted exchange.

## C3. No legal single square exchange

**Lemma C3.** Every D four-cycle is the boundary of one of the dual
faces v,w,p,q. In particular no such cycle contains g.

**Proof.** The frozen source gives a simple cubic three-edge-connected
plane D and primal minimum degree at least four. First every D
triangle is facial: if both sides had vertices, each side would need
at least three attachment edges by three-edge-connectivity, while the
three cycle vertices have only three incidences left. A triangle has
no chord, so an empty side is a face. Its primal dual would have degree
three, impossible. Thus D has no triangle.

A four-cycle consequently has no chord. If both its sides had
vertices, the same attachment count would require at least six edges,
while the four cubic cycle vertices have only four incidences left.
Hence one side is empty and the cycle is facial. The corresponding J
vertex has degree four, so it is one of v,w,p,q. The endpoints of g
are the primal vertices m,z of degrees at least seven and six; thus g
is incident with none of these degree-four dual faces. QED.

**Corollary C3.1.** A single M-alternating cycle taking one member of
F_e to another has length at least six. If a permitted two-cycle batch
contains a four-cycle, that square is the face p or q, and its partner
contains g and has length at least six.

Indeed a square at v or w contains e, so switching it removes the
fixed e. A square at p or q contains f and neither e nor g, so switching
it alone changes exactly one of f,g and leaves F_e. In a permitted
batch the square must therefore be of the latter type and its disjoint
partner must change g. The partner cannot be a square by C3. Alternating
cycles are even, and D is simple and triangle-free, giving the stated
lower bounds. QED.

Thus a local square switch that breaks a saturated W5 complementary
pentagon is never a legal single joint exchange. This is an obstruction
to that proposed repair, not a claim that larger exchanges fail.

## C4. Focused local calibration and remaining obligation

The independent standard-library checker enumerates every one of the
64 bit assignments and all 120 complete four-colourings of the literal
six-vertex W5. It retains every bit fibre, including empty ones. Exactly
22 bit assignments have one monochromatic edge in each triangular
wheel face. Their selected boundary half-edge counts are 1,3,5 with
multiplicities 10,10,2. The last two assignments are precisely the
monochromatic odd rims and have empty complete-colouring fibres.

The checker also enumerates the marked-square membership truth table,
including both possible memberships of f and the paired-switch case.
This calibrates C2's local pentagon and C3's membership argument. The
original C5 lift and plane attachment argument are paper proofs; the
checker does not claim to verify arbitrary source geometry.

The target still needs either a source proof of ordinary joint
nonemptiness and an even complement, or a complete same-source colouring
that violates the full all-r criterion. No assertion here supplies a
descending oddness move, an even endpoint, or source exclusion.
`W110+W101>0`, the complete319 exclusion and the general unbounded claim
remain OPEN. No graph change or reconstruction is performed; using W/J
to return to a completed source still costs k+5. No new external
theorem, 4CT, Lean result, commit or push is used.
