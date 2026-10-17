# C: all induced five-cycles and the remaining crossed sectors

BASE `f1faf743833c51ddc5efbe9e0f390b87b9f2311d`. This worker writes only
`C/`; authority inputs are immutable under `../frozen/`. The new arbitrary-size
result is Theorem C1: it extends the old sector restriction from four-cycles
to **every induced five-cycle**, rather than only a five-cut appearing in a
particular ordinary-matching barrier. C2 states the exact dual-cut consequence,
including chorded five-cycles. No original minimum source has been supplied.

## 1. Source, original sectors, and retained relation

Keep the same globally minimum no4ct C5 source G, with the secondary
maximum-edge choice, original boundary `(x,y,a,b,c)`, degrees
`d_G(x)=d_G(y)=d_G(b)=4`, `d_G(r)=6`, and original r rotation
`(x,y,t,w,v,s)`. We use the proved construction

`U=R-r`, boundary `(z,s,v,w,t)`, `Sigma(U)=319`,
`J=U/(s=t)`, `m=[s=t]`, `D=J*`.

The literal marked primal edges are `e=vw`, `f=pq`, `g=mz`; the same letters
on D mean their actual duals. The faces `mvw` and `zpq` and all original
rotations remain fixed. Every J triangle is facial. Let

`L_s={u: su in E(U), u!=z}`, `L_t={u: tu in E(U), u!=z}`,
`L_a={u: au in E(G), u!=s,t}`, `L_c={u: cu in E(G), u!=s,t}`,

where all sets are viewed as retained J vertices, excluding m,z. They are the
original consecutive link sectors, and

`N_J(m)-{z}=L_s disjoint-union L_t`,
`N_J(z)-{m}=L_a disjoint-union L_c`,
`L_t intersect L_a={alpha}`, `L_s intersect L_c={beta}`,
`L_s intersect L_a=L_t intersect L_c=empty`.

Here alpha and beta are the actual two common neighbours of m,z, not new
pins. The original faces on ta and sc are respectively `ta alpha` and
`sc beta`; `alpha=p iff d_G(a)=4`, `beta=q iff d_G(c)=4`.
In particular `v in L_s`, `w in L_t`, `p in L_a`, `q in L_c`.

The old proof gave `E_J(L_s,L_t)={vw}`. There is also the literal identity

`E_J(L_a,L_c)={pq}`.                                      (1)

Indeed a crossed edge gives a triangle through z. It must be facial, hence
consecutive on the actual z link. After deleting m that link is the one
path through the a sector, the edge pq, and the c sector. Its only crossed
edge is pq. This uses the actual rotation, rather than an independent
partition of N(z).

The retained source statement about colourings remains the entire seven-pin
relation in `(z,s,v,w,t,p,q)`, with every complete private colouring, every
empty fibre, and **all** legal r colours. On the s=t subrelation it implies
`(d_e=d_f) iff (d_e=d_g)`. Nothing below replaces the U relation by a J
projection or deletes s!=t or no-r fibres.

## 2. The new five-cycle classification

**Theorem C1.** Let Q be any induced J five-cycle. The following cases hold.

1. If Q avoids m,z, one side is exactly the star disk of a retained vertex
   h of original and J degree five. It is adjacent to neither m nor z.
2. Suppose Q contains m and avoids z. If the two Q neighbours of m belong
   to the same sector L_s or L_t, one side is exactly a degree-five star
   disk, with centre h in that very sector. Its J degree is five; it is
   not adjacent to z, and it is none of `v,w,p,q,alpha,beta`.
3. Suppose Q contains z and avoids m. If the two Q neighbours of z belong
   to the same sector L_a or L_c, the corresponding statement holds with
   centre h in that sector, not adjacent to m, and avoiding the same six
   named retained vertices.
4. Suppose Q contains both m,z. Their edge is a Q edge. Write its cyclic
   order `Q=(m,z,A,B,C)`. If `(A in L_a,C in L_t)`, one side is exactly
   the star disk of **the literal alpha**. Thus `d_G(alpha)=d_J(alpha)=5`
   and `alpha!=p`. If `(A in L_c,C in L_s)`, the centre is beta, with
   both degrees five and `beta!=q`.
5. In the crossed case `(A in L_c,C in L_t)`, a one-vertex star side
   can only have centre `alpha=p`, of J degree five and original degree
   six. In the crossed case `(A in L_a,C in L_s)`, its only possible
   centre is `beta=q`, with those same respective degrees. Conversely,
   either indicated endpoint identity together with J degree five gives
   just such an induced link five-cycle. At most one of the two
   exceptions can exist, since `d_G(a)+d_G(c)>=11`.

Thus an induced five-cycle with no degree-five star side must cross the
original sectors at its single hub, or use crossed incidences at both
hubs. It cannot avoid both hubs. Compatible cases in part 4 are absent
when the indicated literal common neighbour has degree other than five,
or is the prohibited endpoint p or q.

**Proof.** Every proper original G five-cycle has bounded cap empty or a
single original degree-five vertex adjacent to all five cycle vertices.
An empty triangulated pentagon has a diagonal. Therefore an induced
five-cycle that lifts literally to an original five-cycle must have the
single-vertex cap. No chord of that original cycle can be hidden: every
possible chord survives in J. The removed inner vertex r has degree six;
the split s,t have degrees at least six; other removed vertices are on the
original exterior and cannot lie strictly inside an original cycle.

In case 1 the cycle is already literal in G. A centre cannot be v or w,
because its original edge to r leaves the cap; it cannot be p or q because
of their original boundary contacts. Its five original edges are all to
Q, so it has no edge to s,t,a,c and hence none to m,z. Its degree is
unchanged. This is the already proved no-hub case, included to make the
classification exhaustive.

In case 2 lift m to its indicated representative s or t. The two cycle
edges incident with m are then actual edges incident with that one
representative. All other vertices and edges lift literally, yielding an
original C5. The original cap theorem and inducedness give its centre h.
The only original vertices of this cycle are the chosen s/t and four
other retained inner vertices. The extra original r edge excludes v,w as
centres, and the a/b/c contacts exclude p,q. The original a/c contacts
exclude alpha,beta. All five original neighbours of h are on the lifted
cycle, so h has no original a/c edge or other s/t edge; it lies in the
specified one sector, has no J edge to z and retains degree five.
Case 3 is the same argument lifting z to a or c. A centre's original r
edge excludes v,w, its other original boundary contact excludes p,q,
and the original t/s edges exclude alpha,beta. None of r,s,t can itself
be a centre, since their complete original degrees exceed five. Again
the five neighbours are exactly the literal lifted cycle.

In case 4, mz must be consecutive, since otherwise it is a chord of Q.
For `(L_a,L_t)` lift Q to the original proper five-cycle
`(t,a,A,B,C)`, using the original edge ta. Its bounded cap is one
degree-five centre h. The face at the ta edge inside this original cycle
is `ta h`. The two actual incident faces of ta are `ta y` and
`ta alpha`. The outer-boundary vertex y is not strictly inside the cycle,
so h=alpha. If alpha were p, its original edge to b would leave the cap;
therefore alpha!=p. No adjacency of alpha is lost in forming J, as all
five of its original neighbours are precisely the lifted cycle. The
`(L_c,L_s)` case uses original sc and its actual faces `sc x`,
`sc beta`, proving the reflected statement.

For case 5, any centre of a J star disk on Q would be adjacent to both
m,z, hence is alpha or beta. Its induced link is exactly Q. At alpha,
the next boundary vertex after m, away from z, is in L_t: the t-sector
has at least three vertices. At z, the next boundary vertex after alpha,
away from m, is in L_a unless alpha=p; in that endpoint case it is
literally q, in L_c. Thus the link of an alpha centre has compatible
`(L_a,L_t)` incidence except exactly when alpha=p, when it has crossed
`(L_c,L_t)` incidence. The beta argument is reflected. If alpha=p,
`d_J(p)=d_G(p)-1`, so a degree-five star centre has original degree six;
for beta=q the same formula holds. Conversely every J vertex of degree
five has induced link C5, since every triangle is facial; these literal
endpoint cases therefore give the claimed crossed star disks. Finally
`alpha=p` and `beta=q` simultaneously would mean `d_G(a)=d_G(c)=4`,
contrary to h>=3. QED.

This endpoint exception is essential. The original small-cap argument
proves original degree five in the compatible case, but cannot be
reused to give a crossed cap centre original degree five: a marked p or q
centre loses its original b edge in forming J. No p/q copy or suppressed
boundary contact is introduced to remove that exception.

## 3. All actual cyclic five-edge cuts, with the chord case retained

The dual D is cubic and three-edge-connected. A cut with four or five
edges has connected sides, since two components on one side would each
have at least three exiting edges. Therefore it is a bond and its actual
primal image is a simple four- or five-cycle. Say a cut is cyclic when
each induced dual side contains a cycle.

**Theorem C2.** Every cyclic five-edge cut of this same D is of one of
the following forms.

* Its primal C5 is induced. Then C1 applies. Each noncrossed case is a
  single pentagonal dual face, corresponding to its exact degree-five
  centre. Crossed both-hub star cases are precisely the marked-centre
  exceptions of C1.5. Every non-star case crosses the specified sectors.
* Its primal C5 has a chord. One chord cuts off an actual triangular
  face. Deleting that triangle's dual vertex from its cut side yields
  an actual cyclic four-edge bond with induced primal C4. The original
  five-cut side is this four-cut side plus the one facial-triangle dual
  vertex, attached by its dual edge on the chord. The old complete C4
  sector theorem applies to this four-cut core.

**Proof of the second case.** A chord of a C5 separates a triangle and a
quadrilateral. The triangle is facial. On the side containing that
triangle, its dual vertex has just one edge into the quadrilateral patch;
it is a leaf attached on the chord. Removing it preserves the existence
of a cycle on that side. The other side already has a cycle and gains
the removed triangle vertex across two edges, so remains cyclic.
Consequently the quadrilateral bounds a cyclic four-cut. It has no
diagonal: two facial triangles on such a diagonal would leave a
two-vertex dual tree on one side. The core is therefore an induced C4.
This argument chooses an actual embedded chord and its actual face; it
does not identify separate feasible cut witnesses.

The useful elementary marked-edge corollaries are stated separately;
they follow from old literal local geometry, rather than being credited
as new source exclusions.

* No J cycle of length at most five contains both e and f. The four
  forbidden cross edges `pv,pw,qv,qw` require two connecting paths of
  length at least two between the disjoint edges, giving cycle length
  at least six.
* An induced J cycle of length at least four containing m cannot contain
  both v,w: their triangle with m supplies a chord. The analogous
  statement holds for z and p,q. In particular an induced C5 contains
  at most one of e,f,g.
* If a five-cut contains e,g, it has a triangular ear equal to the marked
  face mvw, and the corresponding cyclic C4 core contains g. If it
  contains f,g there is such an ear equal to zpq. Other ears may also
  occur. Five-cuts containing e,f are impossible. Thus
  every five-cut containing two marked edges reduces to a source-sector
  restricted C4 core, rather than an uncontrolled induced C5.

For the e,g statement the original nonedges zv,zw force the two other
cycle edges at v,w to give the mvw ear; removing its middle v/w vertex
retains mz. For f,g, the edge f=pq is a cycle edge. If at least one of
zp,zq is also a cycle edge, zpq is an ear with middle vertex p or q, so
its core retains mz. If neither is a cycle edge, write Q (up to swapping
p,q) as `(m,z,A,p,q)`. Both zp,zq are chords. The actual faces `zAp`,
`zpq`, `zmq` form a three-triangle pentagon disk, whose dual side is a
three-vertex tree. That contradicts cyclicity. Hence the indicated ear
always exists; this argument asserts existence, not uniqueness.

## 4. What this adds and the remaining proof obligation

C1 excludes an arbitrary-size family of proposed induced five-separators
without assuming it occurs in a maximal Tutte barrier. It also makes the
two compatible both-hub cases exact: their centres are alpha or beta,
with original degree five, rather than an unnamed permissible W5. It
also isolates the crossed marked-centre exceptions, with original degree
six, which a hub-only projection would conceal. C2
records the chord case needed before using this theorem for arbitrary
dual cuts. The mixed-sector five-cycles remain uncontrolled and are not
declared realizable. The existence of an ordinary 101 matching is still
separate from an even complement.

These are restrictions on the very same completed source, not a new
boundary relation or a replacement representative. Every full U fibre,
all seven pins, and every r lift remain under the original universal
obligation. No source graph is supplied: source enumeration is
**not triggered**. The target `W110+W101>0`, complete319 exclusion and
the general main statement remain OPEN. Restoration from U still costs
five vertices; the completed total is `k+5`, so this is no strict descent.
There is no general 4CT use, external theorem, Lean claim, shared-document
write, commit or push.

## 5. Finite calibration

`check.py` reconstructs four explicitly pinned embedded controls: an icosahedron
with fixed pins and exact sectors, and the nine-boundary two-star disk
closed by one outer cone vertex in three literal pin/sector choices.
Those choices retain generic endpoints, alpha=p, and beta=q separately. Neither is asserted to be an original
source. It independently enumerates every primal C4/C5, constructs the
actual cubic dual from the rotations, and checks every cyclic five-cut
ear/core relation and every marked-edge corollary. It retains every
cycle and cut record, including noncyclic cut sides; no colouring
relation is projected or claimed by this geometric checker.

The icosahedron positively calibrates both compatible forced
common-neighbour centres. The cone endpoint choices positively
calibrate the crossed marked-centre exceptions.
The cone control deliberately exhibits noncrossed induced C5s without a
one-centre side: it lacks the original small-cap premise. This is a
negative control against deriving C1 from facial triangles and sectors
alone. The paper proof, rather than this finite test, supplies the
original-source cap premise.

Default and seed-17 replay must reproduce active `certificate-v2.json`. A corrupted
cut-core certificate must fail; a second creation must reject overwrite.
Receipts, stdout and stderr are retained in `VERIFICATION.json` and
`logs/`. The certificate binds this proof, checker, BASE and relevant
frozen authority hashes.


The geometric runs reconstruct 642 cycle records across the four pinned
controls: 234 cyclic five-cut records, including 186 chorded cases.
The three cone choices retain respectively 4,5,5 noncrossed induced C5
controls without the original forced cap. The alpha=p and beta=q choices
each retain one crossed marked-centre star. These numbers are finite
calibration coverage, not coverage of minimum sources.

Development receipts: the first unsealed checker attempt caught a wrong
p label in the beta=q cone control (p must be vertex10, immediately before
q, rather than vertex8). No certificate was written on that failed pass.
`initial-certificate.json` and `certificate.json` retain the subsequent
intermediate seals before the final ear/core wording and active filename
were fixed; they are not the active replay authority.
