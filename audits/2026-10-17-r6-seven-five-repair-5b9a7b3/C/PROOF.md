# C: exact marked-cap placement and the remaining split-cap obstruction

BASE `5b9a7b3190c84bc10ff99608e372a9b4be57a0f6`, 2026-10-17.
This is an independent paper audit of the marked-cut route. The new
placement exclusion in section 3 uses the adopted marked-six theorem.
The remaining H-connected repair / strict oddness descent remains **OPEN**;
section 5 independently proves strict descent for a neutral whole cluster.

## 1. Source and authority

Keep the whole original minimum no4ct C5 source, its fixed support,
ordered contacts, rotation, actual attachments, private vertices, complete
U319 fibres including empty ones, and every original r lift. Set
`J=U/(s=t)`, `D=J*`, `e=(vw)*`, `f=(pq)*`, `g=(mz)*`.
The marks are literal edges in this same graph. The original four
terminals v,w,p,q are distinct, and every cross edge between {v,w} and
{p,q}, as well as zv,zw, is absent.

Let M be a joint oddness-minimal PM in `P110 union P101`. Assume its
complement has a nonfacial seven-component C, put `X=V(C)` and
`B=delta_D(X)`, and take the source-supplied even111 PM M0 with
`|M0 intersect B|=3`. No assertion below requires an independent outside
witness. Every outside path and every untouched outside component remains
part of this same D.

Use the frozen [seven-defect classification A1--A3](../../2026-10-17-r6-joint-positive-113e41f/A/PROOF.md):
`D[X]` is C plus exactly one chord d in M, bounding a four-face and
a five-face; its five distinct external spokes are precisely B and belong
to M. Their exterior contains a whole component of D-M. The two primal
face centres have degrees four and five, with the degree-four centre in
`{v,w,p,q}`. Also use [R6-MARKED-SIX](../../2026-10-17-r6-marked-six-exclusion-6c420f3/PROOF.md):
every cyclic cut containing e and f has size at least seven. Cyclic means
each induced side contains a cycle; neither side need be assumed connected.

## 2. Complete centre trichotomy

Let u be the degree-four centre of the cap. An edge incident with u in J
has its dual edge on the boundary of u's dual face. Within the two-face
cap this dual edge is either on C or is the shared chord d.

* If `u in {v,w}`, then e is such an edge. Since `e in M`, e cannot lie
  on C, so `d=e`, and the other centre is the opposite member of {v,w}.
* If `u in {p,q}` and `M in P110`, the same argument with `f in M`
  gives `d=f`, and the other centre is the opposite member of {p,q}.
* If `u in {p,q}` and `M in P101`, then `f notin M`, so `f in E(C)`.
  The other centre is an ordinary degree-five vertex h, as in A3: it
  cannot be the other p/q (that would make f the chord), v/w (the cross
  nonedges), or a hub (the hub degree bounds).

These cases exhaust every nonfacial seven-component of a joint M.
In particular, **at least one of e,f is entirely internal to X**.

In the chord-e case both f and g are entirely exterior to X. They cannot
be cap edges because their primal endpoints are not the two centres v,w.
If f were a spoke, its primal edge pq would bound a triangle with a centre
v or w, violating the cross nonedges. If g were a spoke, mz would bound a
triangle with a centre v or w, violating zv,zw.

In the chord-f case e is entirely exterior by the same cross-nonedge
argument. The omitted g is also entirely exterior: A3 excludes g from C,
the cap centres exclude it from the chord, and `B subset M` excludes the
omitted edge g from B.

The active-f case has the additional exclusion proved next.

## 3. A concrete forbidden-six-cut construction

**Lemma C1 (spoke / cycle placement exclusion).** If `f in E(C)`, then
`e notin B`.

**Proof.** Suppose `e in B`. The primal edges vw,pq have four distinct
endpoints. A triangular J face cannot contain both, so their dual edges
e,f have no common D endpoint.

Every C edge has an endpoint a other than the two chord endpoints. Choose
such an endpoint of f. Because e,f have no common endpoint, e is not
incident with a. The vertex a has exactly two neighbours inside X, namely
its two C neighbours, and one spoke outside. Define the explicit set

`Y = X minus {a}`.

Removing a from X removes its one spoke from B and adds its two C edges
to the cut. Consequently

`|delta_D(Y)| = 5 - 1 + 2 = 6`.

The edge f has exactly one endpoint in Y, so `f in delta_D(Y)`. The cap
endpoint of e is in Y, and its other endpoint is outside X, so
`e in delta_D(Y)` as well.

The chord separates C into its four-face and five-face. The chosen a lies
on exactly one of their open C arcs. The other entire facial cycle avoids
a and belongs to D[Y]. The complement of Y contains the whole exterior
`V(D) minus X`, which contains a complete D-M cycle distinct from C.
Thus both induced sides contain a cycle. This is a cyclic six-cut
containing e,f, contrary to R6-MARKED-SIX. QED.

In the active-f case e is neither a C edge (`e in M`) nor the chord
(its primal endpoints v,w are not the cap centres). C1 therefore proves
that **e is entirely exterior to X**. The common g is not on C or the
chord by the hub degree bounds; it may be a spoke or entirely exterior.
No absence of a spoke g is claimed in this case.

This application of marked-six is a genuine arbitrary-size paper
exclusion. It only excludes a mark placement. It does not exclude the
active-f cap with e exterior.

## 4. The comparison batch has exactly one marked obstruction

Put `h=g, k=f` in direction 110, and `h=f, k=g` in direction 101.
The actual symmetric difference `M triangle M0` avoids the common marks
e,k and contains h. Let H be its unique component containing h.
All components are disjoint alternating even cycles.

For any subbatch of these specific components, the flipped PM stays in
the joint family exactly when H is not chosen. Indeed e,k are untouched;
choosing H changes the sole omitted mark h from zero to one, landing in
111. A subbatch of this fixed comparison can never switch 110 to 101 or
vice versa, since the common k is not on the difference. Other actual
alternating batches in D are not ruled out.

Because precisely two spokes lie in `M minus M0`, exactly one difference
cycle K crosses B, twice. Its part in X is a single alternating path:
there is no internal alternating cycle since d is the only internal
M edge. It consists of either one C edge (d common) or three edges using
d (d changed). The remainder is the actual outside path, with arbitrary
length. Every other difference component avoids X. In the active-f case
`f in C intersect M0`, so necessarily `K=H`. In the chord-e and chord-f
cases the chord is common, the internal path is one edge, and the omitted
mark lies on the outside path if `K=H`.

Neither `K != H` nor a neutral single switch supplies strict global
oddness descent by itself: every resulting complete complementary
component still has to be retained and counted.

## 5. Whole influence clusters and why their boundary is insufficient

For completeness, form a bipartite incidence graph whose nodes are all
whole cycles of F=D-M and all difference cycles of `M triangle M0`,
joining two nodes if their actual vertex sets meet. For an incidence
component, let Z be the union of its vertex sets. Every F edge stays
inside one component, and every changed M edge lies on a difference cycle.
It follows that

`delta_D(Z) subset M intersect M0`.

Flipping all difference cycles in the component replaces the complement
on Z by the actual F0=D-M0 on Z. Every F0 edge also remains within Z:
an unchanged F edge does so already, and a new complementary edge lies
on a difference cycle. Hence the entire new complement on Z is even.
Outside Z no matching edge changed.

If the component containing C avoided H, this flip would preserve the
joint identity and remove at least the odd C while introducing no odd
component. Joint oddness-minimality therefore forces that component to
contain H. In the active-f case this is immediate from `K=H`.

This exact cluster conclusion does **not** give the required forbidden
cut. The cluster contains all X. By section 2 one of e,f has both
endpoints in X, so it cannot belong to `delta_D(Z)`. More generally:

**Every candidate Y with `X subset Y` fails to have both e,f in its cut.**

Any successful blocked-repair-to-forbidden-cut proof must therefore split
the seven-cap, and must prove that each resulting side still has a cycle.
Neither a bound on a whole cluster boundary nor the fact that H is reached
in the incidence graph provides that split or a cut-size bound. For a
chord e or f, separating its endpoints destroys every cycle internal to
the seven-cap, so the side in question needs a cycle supplied elsewhere
in the actual graph. The potentially unbounded outside paths and remote
components are exactly where this missing work remains.

## 6. Finite calibration and precise endpoint

The accompanying checker calibrates the explicit C1 construction on the
literal seven-cycle-plus-chord cap, glued to a second cap across its five
ports. It checks every C-edge f and every nonincident spoke e, retaining
all 25 edge placements and the whole outside seven-cycle. It independently
reconstructs delta(Y), its exact six edges, both marked incidences and
cycles in both induced sides. A malformed certificate is rejected.
This toy graph has neither the named source geometry nor the U319 fibres,
and generally violates marked-six precisely in the tested placements.
Its status is **finite calibration**, not a source witness or source
counterexample. The source-realizability control is **not triggered**.

The paper endpoint is the complete centre trichotomy, the strict
spoke/cycle placement exclusion via the explicit cyclic six-cut, actual
joint strict oddness descent for every neutral whole cluster, and the
necessary H-cluster obstruction for a joint minimizer. No repair for the
remaining H-connected case has been proved. No construction of the
remaining split-cap marked cut has been proved. Joint positivity,
`omega_e=0`, complete319, and a new Lean theorem remain **OPEN**.
All work is within the same graph, with zero reconstruction cost; this
does not change the original k+5 source reconstruction cost.
