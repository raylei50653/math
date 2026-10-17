# B: the v5 source forbids every six-cycle through both marked edges

BASE `113e41f7023aa00c8257b815ce8727035b648f26`. This worker writes only
`B/`. The source is the original minimum no4ct disk G, with its single fixed
original support S in `{932,933,941}`. All nine original F pins
`(c,s,j,i,w,t,a,p,q)`, every private colouring, every empty fibre and every
five-vertex `(v,r,x,y,b)` reconstruction remain as in the frozen source
proof. No new colouring is assembled from independent witnesses.

Assume original `d_G(v)=5`. The frozen C proof gives the actual hexagonal
disk H with boundary `(z,s,j,i,w,t)`, the two actual caps V_i,V_j with
complete supports 1022, and the 58-row upper relation. Its final-step C6
addendum proves that the following six canonical rows of the **complete** H
relation have nonempty fibres, conditional on this same source:

```
ABACDBCD  ABACDBDC
ABCADBCD  ABCADBDC
ABCDABCD  ABCDABDC
```

The pin order is `(z,s,j,i,w,t,p,q)`. The single global exchange C/D also
gives the other six literal rows with `z=A,s=t=B`, `(j,i,w)` a permutation
of `(A,C,D)` and `(p,q)` either `(C,D)` or `(D,C)`. Each witness has all four
colours on `(s,j,i,w)`, hence its v lift is empty. The argument below uses
these genuine complete witnesses to exclude edges; it never restores v over
one of their empty fibres.

## B1. New nonedges and exact two-step reachability

**Theorem B1.** In the original graph and in H, none of

`jp, jq, ip, iq`

is an edge. Moreover `zi,zj` are absent in H/J; for each of i,j, both
original incidences to a,c are consequently absent.

Proof. For each displayed pair there is a compulsory complete H colouring
in which its two endpoints have the same colour. An actual edge would make
that particular complete colouring improper. The pairs zi,zj occur with
both endpoints A in the compulsory rows. The quotient identifying a,c to z
retains every incidence to the other named pins, so absence of zi or zj
forbids both original split incidences. This argument works for arbitrary
source size. It uses existence of a separate complete witness for each
nonedge and does not require those witnesses to be compatible. QED.

The old source already excludes vp,vq,wp,wq. In J=U/(s=t), put m=[s=t].
The literal v link is the four-cycle `(m,j,i,w)`, so

```
N_J(v) intersect N_J(p) = {m} if mp is an edge, and empty otherwise;
N_J(v) intersect N_J(q) = {m} if mq is an edge, and empty otherwise.
```

The source identities are `mp iff d_G(a)=4` and
`mq iff d_G(c)=4`; at most one occurs because `d_G(a)+d_G(c)>=11`.
Thus v has a two-edge path to at most one of p,q. In the graph J-m it has
no two-edge path to either. This gives more source geometry than merely
recording the four compulsory nonedges.

## B2. No six-cycle contains both e=vw and f=pq

**Theorem B2.** Under original v5, every simple J cycle containing both
marked edges vw and pq has length at least seven.

Proof. The preceding source already excludes lengths at most five. If
there were a simple six-cycle containing both disjoint edges, its two
connecting paths would each have length two: a direct edge between either
endpoint pair is forbidden. Write the cycle, allowing the literal
interchange of p and q, as

`(v,m,p,q,h,w)`.

Indeed its connector next to v belongs to N_J(v)={m,j,i,w}. Simplicity
excludes w, and B1 excludes j,i. The displayed m and h are distinct; all
six vertices are distinct. Also h is not z, since zw is an original source
nonedge; it is not m, and none of the deleted collar vertices is in J.
The edge mp implies the original a degree is
four and the literal endpoint identity alpha=p. Also mq is absent, since
that would give c=4 simultaneously. The marked face mvw supplies the
chord mw. Deleting its v ear exposes the pentagon

`Q=(m,p,q,h,w)`.

Both p and w belong to the original t sector of N_J(m): p=alpha, and w
is the mandatory r-fan endpoint. Therefore Q lifts literally to the
proper original G five-cycle

`Q_G=(t,p,q,h,w)`.

The other four vertices are retained original inner vertices; none is t,
and all are distinct. Q_G differs from the original exterior five-cycle.
Its bounded cap is therefore either empty or exactly one degree-five W5
centre, by the frozen original small-cap theorem. The bounded side here
is determined in G, not chosen freely in J. In particular a,b lie outside
Q_G because they lie on the original exterior boundary. At p the original
outside wedge is exactly the three facial triangles

`(t,p,a), (a,p,b), (b,p,q)`.

The first is a face because a=4; the second is the original ab apex face;
the third is a face in the original degree-four b fan. These faces fix the
entire outside link segment `t,a,b,q` at p. There is no room for an extra
outside neighbour of p.

If the cap is empty, it is a triangulated pentagon. Its only possible
diagonals are th and ph: the other three candidates tq,pw,qw are absent
by mq absent and the original cross-nonedges. A triangulated pentagon has
two diagonals, hence its faces are `(t,p,h),(p,q,h),(t,h,w)`. The inside
link segment at p is exactly `t,h,q`. If the cap has one W5 centre u,
its inside link segment at p is exactly `t,u,q`. In either case combining
that inside segment with the fixed outside segment gives exactly five
original neighbours of p:

`N_G(p)={t,a,b,q,h}` or `{t,a,b,q,u}`.

Thus d_G(p)=5 while d_G(a)=4. This contradicts the frozen low-p theorem
`d_G(p)=5 => d_G(a)>=6`. In the reflected endpoint case mq is the edge,
and the same proof gives q=5,c=4, contradicting the reflected theorem.
No six-cycle is possible. QED.

This proof does not assume Q is induced. Both the empty triangulated cap
and the singleton W5 cap are explicitly covered. It also does not assume
p has original degree six merely because it has a marked boundary role.

## B3. Dual consequence and stopping boundary

**Corollary B3.** Every cyclic six-edge cut of the actual cubic dual D=J*
avoids containing both e=(vw)* and f=(pq)*.

To justify the bond step, J has no separating triangle, so every three-edge
bond of D cuts off a single vertex. A connected component C containing a
cycle therefore has at least four edges leaving it, provided the other side
also contains a cycle. If a cyclic six-cut side had a second component,
that second component would have at least three exiting edges by
three-edge connectivity, for a total of at least seven. Thus both sides of
a cyclic six-cut are connected. It is a bond, and its actual primal image
is a simple six-cycle. Theorem B2 applies.

This strengthens the existing at-most-five-edge marked separation on the
v5 branch to the six-edge interface. It does not bound source size, prove
ordinary matching implies an even complement, or force a Kempe path to a
violating complete colouring. The compulsory H rows still have empty v
fibres. All 58 upper rows, both cap supports 1022, U support 319 and the
completed-source reconstruction cost k+5 remain; v5 itself and
`W110+W101>0` remain OPEN. Source instances supplied: zero, not triggered.
No external theorem, general 4CT, Lean theorem, shared-document write,
commit or push is introduced.

## B4. Finite calibration and custody

`check.py` checks frozen hashes, the exact compulsory rows and their
same-colour witnesses, all labelled local six-cycle connectors, and both
pentagon-cap possibilities. The cap check independently enumerates every
noncrossing set of pentagon diagonals, and separately glues the W5 star;
in each retained case it checks the complete cyclic link at p and its
five original neighbours. A small-cut arithmetic check records why a
cycle-bearing disconnected side cannot have six exiting edges. These are
finite calibrations of the local steps. The arbitrary-size argument is B2,
and the source existence input is the separately frozen C6 theorem.

The original F relation is checked for its three fixed masks and complete
five-vertex reconstruction tables through the frozen source seals; it is
not recomputed with a mask chosen per row. Empty fibres are kept intact.
Normal and seed17 replay and deliberate witness/cap corruption rejection
are retained in `VERIFICATION.json`.
