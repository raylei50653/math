# B: transition parity from the same complete 111 colouring

Frozen BASE `e98a1cc1afd9a428600dcf4027d8138078c01650`.
The source is the same original minimum C5 source, with its ordered
contacts, rotation, all complete colouring fibres including empty ones,
all original r lifts, and literal `J=U/(s=t)`, `D=J*`,
`e=(vw)*`, `f=(pq)*`, `g=(mz)*`.
The authority is the frozen source-geometry proof, FULL_J_BRIDGE,
joint-zero B proof, seven-disk-rigidity proof, and xor-batch-descent proof.
No arbitrary planar colouring oracle, four-colour theorem, external
theorem, or source replacement is used below.

The frozen source already supplies a **complete** J colouring whose
three marked differences are equal, hence a labelled Tait colouring of
this actual D with `e,f,g` all colour alpha. Write M0 for that alpha
matching. Its entire complement F0 is even and has the other labelled
colours beta,gamma. Independently, seven-disk-rigidity supplies an
ordinary 101 matching. These are distinct kinds of witnesses.

## B1. A concrete single-cycle presentation of ordinary 101

Take any ordinary 101 matching N. The symmetric difference M0 xor N is
a union of vertex-disjoint alternating even cycles. It avoids e,g and
contains f. The unique component Q containing f therefore avoids e,g.
Flipping just this component gives

`N_Q=M0 xor E(Q)`, with `e,g in N_Q` and `f not in N_Q`.

This proves that the family of such actual alternating cycles Q is
nonempty. It makes no claim that N_Q has the least possible oddness,
or that an even 101 endpoint would always have a single-cycle
presentation from this particular M0. For 110 one instead takes the
component containing g in a difference with a 110 matching and avoids
e,f. A joint matching in the opposite direction need not exist.

## B2. The complete transition-parity identity

More generally take any batch of vertex-disjoint M0-alternating cycles
and let N be its flip. Put `A=M0 minus N`, `B=N minus M0`.
Every endpoint x of an edge in A is incident with exactly one B edge;
write `b(x)=0` if that B edge has original colour beta and `b(x)=1`
if it has original colour gamma. An edge xy of A is a **transition**
exactly when `b(x) != b(y)`.

**Theorem B2.** For each entire component C of D minus N,

`|C| mod 2 = |E(C) intersect transitions| mod 2`.

Consequently every new odd component contains a transition edge,
the total transition count t is even, and

`odd(D-N) <= t`.

**Proof.** Remove the B edges from the even beta/gamma cycles F0.
Any untouched F0 cycle remains even. Every touched component splits
into paths whose endpoints are the endpoints of the removed B edges.
Because B is a matching these paths are nondegenerate, and every
endpoint is an endpoint of exactly one A edge.

For such a path P with endpoints x,y, its first and last edge colours
are opposite to the respective removed B colours. The old beta/gamma
alternation therefore gives the exact formula

`|E(P)| mod 2 = 1 + b(x) + b(y) mod 2`.

Retain every path, both of its labelled endpoints and every A edge.
The new complement is exactly these paths joined by A, together with
the untouched even cycles. Any new component assembled from k paths
contains k A edges. Its length parity is thus

`k + sum_P (1+b(x_P)+b(y_P)) = sum_A (b(x)+b(y)) mod 2`,

which is its number of transition A edges modulo two. All endpoints
are used exactly once, so no independent witnesses have been joined.
Along each original alternating cycle the successive B colours form
a cyclic binary word; its number of changes is even. Summing over
the batch proves t even. Each odd new component needs at least one
different transition edge, giving the bound. QED.

The original beta/gamma colouring is fixed throughout. The theorem
does not discard any beta/gamma alternation choice: it applies to each
of their complete choices separately. N with an odd component has an
empty complete Tait-colouring fibre; no colouring of N is invented.
If every new component contains an even number of transitions, all
its two-colour alternations give the full `2^cycles(D-N)` labelled
Tait fibre, and integration retains all four primal root colours.

## B3. The two-transition obstruction is exact

For a Q supplied by B1, let t(Q) count the transitions in B2. Then

* `t(Q)=0` already gives even 101, and hence joint positive weight;
* `t(Q)=2` gives either even 101 or exactly two odd components;
* in the latter case each odd component contains exactly one of the
  two transition edges; in the former they belong to the same entire
  complementary component.

Thus a proof that Q can be chosen with two transitions would give
`omega_e <= 2`. To give positivity it must also prove that the two
transitions are on the same new complementary component. This second
obligation is real and cannot be supplied by planarity alone.

The exact all-size sufficient criterion is: **some source-supplied Q
has an even number of transitions on every entire new complementary
component**. This criterion can also be applied to a full batch that
produces either joint direction; it imposes no separate positivity of
W110 and W101.

The minimum of t(Q) over B1's nonempty finite family is a finite even
integer. Its value is a computable upper bound for omega_e, not a
proof that it is zero or at most two. Source-safe Kempe coincidences
show only that the wholly beta or wholly gamma f-cycle cannot serve
as Q: those cycles also contain g. There is presently no proof that
mixed cycles satisfying the required transition placement exist.

## B4. What a source W5 defect and a marked defect must look like

First, any odd new complementary pentagon contains **exactly one**
transition. Indeed A is a matching, so a five-cycle contains at most
two A edges; B2 says its transition count is odd. This applies in
particular to each literal retained W5 cap identified by frozen B4.
Its five dual spoke edges form the complete odd complementary
pentagon. Its sole transition is on one of those original spokes.

Such a W5 pentagon avoids all three marked dual edges. Its original
centre is outside both closed hub stars and is none of v,w,p,q.
No spoke can therefore be vw, pq, or mz. Thus, if f itself is a
transition in B1 and its new component is odd, that component is
not one of the retained W5 caps away from the hubs.

There is also a short-cycle classification for the actual D.
Every D cycle of length at most five is facial. To see this, a
triangle is chordless. If it had vertices on both sides, each side's
vertex set would need at least three outgoing edges by three-edge
connectivity, whereas its three boundary vertices have only three
edges outside the cycle in total. Hence one side is empty and it is
facial. J has minimum degree four, so such a triangular D face does
not exist. A four- or five-cycle has no chord, since a chord would
make a triangle. The same two-sided cut argument, with at most five
available outgoing edges, makes it facial as well.

In particular, an odd complementary component containing f has length
at least seven, or is the facial pentagon of a degree-five original
J vertex p or q. These are the only dual faces incident with f.
In the 101 bit partition exactly one of p,q has its bit opposite
to z; only that vertex can be such a pentagon centre, since a whole
facial complementary cycle requires every edge at its primal centre
to cross the bit partition. In original G this exceptional centre has
degree six, by the retained formula `d_J(p)=d_G(p)-1` and its q version.

This distinguishes the marked defect from an ordinary remote W5 cap.
It does not exclude the exceptional degree-six original p/q case or
an arbitrary longer odd component. No deletion has been performed.

## B5. A complete planar negative control of the missing implication

The ten-vertex triangulation in [countercontrol.json](countercontrol.json)
is independently reconstructed from its complete primal face set.
It has all 144 labelled J colourings, all 18 ordinary dual matchings,
and every complete fixed-alpha colouring fibre, including six empty
ones, in [certificate.json](certificate.json). The marks have the
literal indices `(e,f,g)=(1,21,6)` of that control.

All its complete J colourings obey the FJ relation. It has an even 111
matching and a unique ordinary joint matching, in direction 101.
For the even 111 matching

`M0={1,3,6,10,13,16,19,21}`

the single f-containing difference cycle is

`Q={8,10,12,13,14,16,18,19,20,21}`,

and its ordinary 101 flip is

`N={1,3,6,8,12,14,18,20}`.

For all four root-normalized labelled beta/gamma choices on this M0,
t(Q)=2 and the two transitions lie on different new components of
lengths nine and seven. For example one complete choice gives
transitions 16 and 21, on the nine- and seven-cycle respectively.
The control has a second even 111 matching
`{1,6,10,11,13,15,19,21}`, whose complement is one sixteen-cycle.
Its two root-normalized beta/gamma choices both have four transitions
on the single twelve-edge difference cycle with N; three belong to the new
nine-cycle and one to the new seven-cycle. These two choices are
distinct from the first M0's four two-transition choices.
Thus even a two-transition ordinary f-switch can stop at oddness two
in a planar four-connected primal. The control's hub degrees are
five, violating the source bounds `d_J(m)>=7`, `d_J(z)>=6`; this is
not a counterexample to the full source claim.

The checker separately enumerates all complete colourings and all PMs
of the three frozen planar controls and this new control. For every
even starting matching, every complete beta/gamma choice with a fixed
root, every endpoint PM, its full symmetric-difference batch, and
each single component, it verifies B2 on every whole new complement
cycle. No actual minimum source is supplied: source **not triggered**.

## B6. Scope and exact remaining proof obligation

B1 and B2 give an all-size concrete defect presentation and an exact
transition formula from the same source-provided even endpoint.
B3 isolates the extra placement condition beyond merely finding two
colour changes. B4 identifies exactly one transition in each remote
W5 defect and localizes a short defect containing f to one exceptional
original degree-six terminal. The finite controls validate these
identities and explicitly reject the unsupported planar implication.

The main remaining obligation is source-specific: prove an allowed
batch whose transitions occur evenly on each entire new complement,
or a strict oddness decrease at every positive joint global minimum,
or a legal completed-source decrease retaining every original fibre.
There is no proved upper bound on t(Q), no proved repair of its split
two-transition case, and no elimination of arbitrary long odd cycles.

All operations above stay on the actual same J,D. They have zero
reconstruction cost but give no smaller completed source; the frozen
W/J-to-G reconstruction cost remains k+5. The joint positivity
`W110+W101>0`, full Sigma319 exclusion, the general main claim, and
any new Lean theorem remain OPEN. No commit or push is performed.
