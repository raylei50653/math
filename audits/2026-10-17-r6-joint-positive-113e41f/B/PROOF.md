# B: the v5 source restricts six-cycles through both marked edges

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

## B2. The unique crossed six-cycle residual

**Theorem B2.** Under original v5, every simple J six-cycle containing both
marked edges vw and pq has, up to reversing its cyclic order, exactly the
form

`(v,m,q,p,h,w)`.

It necessarily has `mq`, so `d_G(c)=4`, `d_G(a)>=7`, and `q=beta`.
In particular, if the same source additionally has `d_G(c)>=5`, there is
no simple six-cycle containing both vw and pq. The theorem does not exclude
the displayed crossed residual when c=4.

Proof. The old source excludes cycles of length at most five through both
marked edges. In a simple six-cycle its two connecting paths must each
have length two, since all four direct cross edges are forbidden. At v the
connector belongs to N_J(v)={m,j,i,w}; simplicity excludes w and B1 excludes
j,i. Thus the only two orders, up to reversal, are

`(v,m,p,q,h,w)` and `(v,m,q,p,h,w)`.

All six vertices are distinct. Also h is not z because zw is absent, and
no deleted collar vertex is in J. We exclude the first order and keep the
second as an explicit residual.

In the first order, mp implies a=4 and p=alpha. Also mq is absent because
a+c>=11. The marked face mvw supplies the chord mw; deleting its v ear
exposes Q=(m,p,q,h,w). Both p and w lie in the original t sector of N_J(m).
Consequently Q lifts literally to the proper original G five-cycle

`Q_G=(t,p,q,h,w)`.

The other four points are distinct original inner vertices, and Q_G is
not the original exterior boundary. Its bounded cap is empty or precisely
one degree-five W5 centre. This is the frozen original small-cap theorem;
the bounded side is determined in G. In particular a,b lie outside Q_G
because they are original exterior vertices. At p the outside wedge is
exactly the three actual facial triangles

`(t,p,a), (a,p,b), (b,p,q)`.

The first follows from a=4, the second is the original ab apex face, and
the third is in the original degree-four b fan. They fix the entire
outside link segment t,a,b,q at p, leaving no extra outside neighbour.

For an empty cap, the pentagon's only possible diagonals are th and ph:
tq is absent because mq is absent, and pw,qw are old cross-nonedges.
Both diagonals must occur in a triangulated pentagon. The inside link at
p is exactly t,h,q. For a single W5 centre u, that link is exactly t,u,q.
Combining it with the fixed outside segment gives

`N_G(p)={t,a,b,q,h}` or `{t,a,b,q,u}`.

Thus p=5,a=4, contradicting the frozen low-p theorem p=5=>a>=6. This
excludes the first order, including its chorded and induced pentagon cases.

The second order has mq, hence c=4, q=beta and a>=7. Here q lies in L_s
and w lies in L_t. Its pentagon Q=(m,q,p,h,w) cannot be lifted using one
original s/t representative. The small-cap step just used is therefore
unavailable. The initial draft incorrectly called this a reflected copy;
a whole reflection also exchanges v,w and changes the v5 hypothesis.
No contradiction is asserted for this crossed case. QED.

## B3. Actual six-cut classification and stopping boundary

**Corollary B3.** Under original v5, every cyclic six-edge cut of the
actual cubic dual D=J* containing e=(vw)* and f=(pq)* has the primal
boundary `(v,m,q,p,h,w)` above. Such a cut requires c=4 and a>=7. Hence
original v5 together with c>=5 excludes every such cyclic six-cut.

For the bond step, J has no separating triangle, so every three-edge bond
of D cuts off one vertex. A connected cut-side component containing a cycle
therefore has at least four exiting edges when the other cut side contains
a cycle. Any additional component costs at least three exiting edges by
three-edge connectivity, giving at least seven. Both sides of a cyclic
six-cut are consequently connected. Its actual primal image is a simple
six-cycle, to which B2 applies.

This excludes one entire source-sector branch of the six-edge interface
and specifies the remaining original boundary degrees. It does not bound
source size or force a violating complete colouring. All 58 H upper rows,
both 1022 cap supports, U support 319 and reconstruction cost k+5 remain;
v5 itself and W110+W101>0 remain OPEN. Source instances: zero, not triggered.
No external theorem, 4CT, Lean claim, shared-document edit, commit or push.

The full original boundary reflection is
`(x,y,a,b,c) -> (y,x,c,b,a)`. On the ten canonical rows its index map is
`[3,1,8,0,6,7,4,5,2,9]`: it fixes masks932 and941 but sends933 to940.
This worker does not silently apply the sealed three-mask C6 calculation
to940. Thus no unqualified w5 or simultaneous v5/w5 corollary is claimed
here. The missing reflected-source admission is separate from the crossed
mq geometry.

The rejected initial all-six-cycle proof, checker, certificate and PASS
receipts are preserved byte for byte under initial/. That checker verified
the cap degree once a same-sector lift was assumed; it did not check that
premise for mq. Its PASS does not validate the rejected statement. Active
certificate.json explicitly records mp as excluded and mq as OPEN.

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
