# R6-JOINT-ZERO B: the joint minimum and its literal primal obstruction

Frozen BASE: `c4c3d99`. All statements use the same original source G,
`d_G(x)=d_G(y)=d_G(b)=4`, `d_G(r)=6`, the legal retained-edge sphere
triangulation `J=U/(s=t)`, and its actual dual `D=J*`. The marks remain
`e=(vw)*`, `f=(pq)*`, `g=(mz)*`. No graph or marked edge is replaced.

The frozen inputs are the [batch proof](../frozen/audits/2026-10-15-xor-batch-descent-6ddea32/PROOF.md),
[source geometry](../frozen/audits/2026-10-15-j-source-geometry-6ddea32/PROOF.md),
and [full return bridge](../frozen/audits/2026-10-15-route-round4-6ddea32/FULL_J_BRIDGE.md).
No external theorem or four-colour theorem is used below.

## B1. The shared-e joint exchange graph is connected

Set `F_e={M PM of D: e in M, |M intersect {f,g}|=1}`. Its basic exchanges
are a single M-alternating cycle avoiding e and containing zero or two
of f,g, or two vertex-disjoint M-alternating cycles avoiding e, one
containing f and the other g, flipped simultaneously.

**Lemma B1.** If F_e is nonempty, these exchanges connect it.

For M,N in F_e, the symmetric difference is a disjoint union of
alternating even cycles and avoids e. If M,N have the same marked
direction, it avoids f,g too, and its components can be flipped one at
a time. Otherwise it contains both f,g. Flip their common component,
or flip their two different components simultaneously. Every remaining
component avoids all marks and can be flipped individually. Disjointness
means that an unflipped component is still alternating after preceding
steps. Every intermediate matching retains e and exactly one of f,g.
The final matching is precisely N. QED.

For t difference components the constructed path has t steps, or t-1
when f,g occupy different components. This is the requested extension of
the frozen XOR proof with e fixed. It does not supply an even endpoint.

## B2. Global minimum, with both directions included

If F_e is empty, only the ordinary-matching analysis applies. Otherwise
define `omega_e=min_{M in F_e} odd(D-M)` and choose a global minimizer M.
The whole joint family is finite. As |V(D)| is even and D-M spans D,
its odd-cycle count is even; hence omega_e is either zero or at least two.

The exact finite equivalence is

`W110+W101>0 iff F_e is nonempty and omega_e=0`.

Every summand at an even-complement M is positive, and every M with an
odd complementary cycle has an empty complete Tait fibre. The minimum
is taken over both directions; no assertion that either separate
direction has positive weight is needed.

The source already supplies a concrete even-complement matching outside
this union. Its complete Sigma319 relation includes the original U row
`(z,s,v,w,t)=(A,B,C,D,B)`, namely ABCDB. The literal
[all-r transfer table](../frozen/audits/2026-10-15-three-edge-matchings-6ddea32/frozen/audits/2026-10-14-c4-c5-recursion-fdd3e22/degree4/R6_TRANSFER.md)
forces the pq palette to be CD in that same complete colouring. Since
s=t, it descends to J with m=B,z=A,v=C,w=D and pq=CD. In F_2^2 the
three differences are equal, so their common Tait-colour matching
contains all of e,f,g and has even complement. This is a source-supplied
111 endpoint, not a premise that an arbitrary planar graph is colourable.
It lies outside F_e. Comparing a joint matching with it yields a
symmetric difference containing exactly one of f,g; the batch which
changes that mark crosses the boundary of F_e. B1 therefore does not
connect this known even endpoint to the joint family, and its existence
alone proves neither ordinary joint nonemptiness nor omega_e=0.

At a positive global minimum every permitted batch has nonnegative
oddness change. The frozen complete path-surgery formula applies
unchanged, with the extra requirement that the batch avoids e. This is
a necessary condition at a minimizer, not a proof of a descending batch.
Even a connected exchange graph may have every vertex of positive
oddness. Independent single-cycle changes cannot be added when their
surgeries touch a common old complementary cycle.

## B3. An exact primal bipartiteness interpretation

This part turns an oddness obstruction into an actual cycle of the
original J, without referring to a chosen sequence of exchanges.

**Lemma B3.** For every PM M of D there is exactly one unordered
partition `{V_0,V_1}` of V(J) such that the original edges within its
parts are exactly M*. Each J face has two edges across the parts and
one inside a part. Moreover, if `B=J[V_0] union J[V_1]`, then

`D-M is all-even iff B is bipartite`,

`components(B)=cycles(D-M)+1`.

**Proof.** Give a primal edge value zero when its dual lies in M, and
value one otherwise. The sum around each triangular face is zero over
F_2, since exactly one of its three dual incidences lies in M. Every
primal cycle is the mod-two sum of its enclosed triangular faces.
Consequently these edge values integrate uniquely to vertex bits after
fixing the bit of one root. Complementing all bits is the only other
choice. This proves the partition statement.

Each edge of B must acquire opposite second bits when a bit is refined
to a colour in F_2^2. All edges crossing the partition are already
proper regardless of their second bits. Thus proper refinements exist
exactly when B is bipartite. In every such refinement the dual Tait
colour `(0,1)` occurs exactly at M, so the other two colours alternate
around D-M; its cycles must all be even. Conversely an all-even D-M
can be alternately coloured by the other two nonzero differences.
Together with `(0,1)` on M this has sum zero around every primal face,
and hence integrates to a proper F_2^2 colouring of the same J. Its
first coordinate is the specified partition. This proves the equivalence.

For the component count, remove the drawn disjoint Jordan cycles of
D-M from the sphere. They leave `cycles(D-M)+1` regions. Primal vertices
joined by B-edges stay in a single region. Conversely the triangular
dual construction shows that all primal vertices in each region are
connected by B-edges: its cells are joined across precisely those
primal edges whose dual is not drawn. Thus the regions are exactly the
components of B, giving the formula. Equivalently this is the elementary
plane deletion-duality identity between primal components and dual faces.
QED.

With a fixed root first bit, the complete proper-colouring fibre has
size `2^components(B)=2^(cycles(D-M)+1)` when B is bipartite, and zero
otherwise. Each bipartite component has both second-bit choices; all
choices are retained simultaneously. The extra factor two relative to
`2^cycles(D-M)` is the second coordinate of the primal root colour.
Thus this correspondence includes every empty fibre.

In the 110 direction the literal partition satisfies, up to global
bit complementation,

`m=p=q in V_0`, `z=v=w in V_1`.

In the 101 direction it satisfies

`m=z in V_0`, `v=w in V_1`, and p,q have different bits.

These follow from the actual two triangles mvw and zpq and the edge mz;
they impose no extra adjacency or arbitrary terminal placement.

## B4. A positive minimum has a concrete original odd-cycle witness

**Proposition B4.** Suppose F_e is nonempty and omega_e is positive.
For every global minimizer M, the induced monochromatic graph B from B3
has a shortest odd cycle C. It is an induced cycle of J of length at
least five, all of whose original edges have their dual in M. One of
the following holds:

1. C passes through m or z;
2. C has length at least seven;
3. C is the original five-vertex rim of a retained degree-five W5 cap,
   whose centre is outside both closed stars of m,z. Its five interior dual faces
   form a whole odd component of D-M, and every edge of its five-edge
   dual cut lies in M.

**Proof.** B is nonbipartite by B3, so it has an odd cycle; choose one
of smallest length. A chord would split it into two shorter cycles,
exactly one of them odd, contradicting that choice. All vertices on C
have the same bit, so every J chord would also be a B chord. Thus C is
induced in the entire J. A monochromatic triangle is impossible because
every face has one monochromatic edge, and the source J has no nonfacial
triangles. Hence |C|>=5. If it avoids m,z and has length five, the frozen
source small-cap theorem applies to precisely these original vertices
and edges. Its empty-cap alternative has a diagonal and contradicts
inducedness. The cap is therefore the single original degree-five W5
centre u, away from m,z and all four marked face vertices.

The rim vertices have one bit, and u must have the other bit because
every wheel triangle has exactly one monochromatic edge. All five rim
edges consequently belong to M*, and none of the five spokes does.
In D, the five wheel faces are connected cyclically by the dual spokes;
these are exactly their two D-M incidences. Thus they form one entire
odd complementary pentagon. Their five dual rim edges are the whole
cut of this same actual cap and all belong to M. QED.

The rim itself may contain vertices adjacent to m or z. No stronger
rim-distance restriction is asserted or used in this proof.

This supplies a literal original cycle for an oddness obstruction and
identifies the W5 cap also present in A's surviving five-cut barriers.
It does not turn a nonempty matching family into a Tutte failure: the
oddness pentagon here has all five cut edges selected by the actual M,
whereas A studies factor-critical components in a different residual.
Nor does the proposition exclude the W5 cap, a longer odd cycle, or a
cycle through the hubs. Even existence of one global minimizer with
such a cap does not prove that the cap is removable by an allowed batch.

## B5. Verification and exact remaining obligation

The independent standard-library checker reconstructs each dual from
all frozen primal faces, enumerates every PM and complete colouring of
the three planar controls, and verifies the integrated partition,
component identity, bipartiteness equivalence, literal marked bit rows,
and complete fibre sizes including zero. It explicitly constructs the
B1 path for every ordered pair in each marked joint family. A separate
Petersen marking with a nonempty joint family checks that connectedness
can coexist with positive global minimum; that graph is not planar and
has no source claim. No finite control is passed off as a source.

B1 and B3 are all-size auxiliary identities. B4 is a source-conditional
localization, not an omega=0 theorem or the principal new exclusion of
this round; the latter is A's independently reviewed singleton-barrier
exclusion. The two cases remaining for the main objective are exactly:

* both ordinary families empty, now with A's surviving nontrivial caps;
* at least one ordinary family nonempty but every joint matching having
  an odd complement, with B4's literal odd-cycle obstruction.

All matching and colouring transformations above keep the entire same
graph. Their zero reconstruction cost is not a smaller completed source.
Restoring W/J to the original construction still returns to k+5. This
work proves neither joint positive weight, fixed-degree r=6 exclusion,
a new numerical bound, a result for r>=7, nor any Lean theorem.
