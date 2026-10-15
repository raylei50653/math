# Six-pin forcing: exact colourability obligations and a source-specific obstruction

BASE `6ddea32a81349821ad3724ae1652bddb9c6a7b04`.
The [input seal](INPUTS.json) distinguishes tracked authority from the two
uncommitted first-round reports. All statements below concern the same
original globally minimum noncatalogue C5 disk G, with original boundary
`(x,y,a,b,c)`, apexes `(r,t,p,q,s)`, and
`d_G(x)=d_G(y)=d_G(b)=4`, `d_G(r)=6`.
Write `a0=d_G(a)`, `c0=d_G(c)` to distinguish degrees from vertices.
The existing source facts give `a0,c0>=4`, `a0+c0-8=h>=3`.

This audit proves a method obstruction, not exclusion of the source:
**the natural whole-graph quotients identifying s=t with p or q are
always looped or nonplanar. The four more precise forcing quotients are
also looped or nonplanar.** The obstruction follows from new explicit
common-neighbour identities in the original source, rather than from
the old 26-row relation alone.

## 1. Source, all-r lifts, and the target event

Use the original construction `R=T0-{x,y}`, `U=R-r`. The graph U has k
vertices, `3k-8` edges, and the induced exterior C5 `(z,s,v,w,t)`;
all inner faces are triangles. The seven pins `(z,s,v,w,t,p,q)` are
distinct, p,q are internal, and zpq is the original facial triangle.
The only possible extra edges among the seven pins are

`tp iff a0=4`, `sq iff c0=4`;

the mandatory edges are `zs,sv,vw,wt,tz,zp,zq,pq`.
In particular all four edges between `{p,q}` and `{v,w}` are absent.
This is the frozen [source geometry](frozen/audits/2026-10-14-c4-mask13-joint6-fdd3e22/SOURCE_GEOMETRY.md)
and [degree-six transfer](frozen/audits/2026-10-14-c4-c5-recursion-fdd3e22/degree4/R6_TRANSFER.md).

For any complete U colouring f, define the event

`E(f): s=t and {p,q} is disjoint from {v,w}`.

All symbols in colour equalities denote values in this one complete
colouring. Because `sv,vw,wt` are edges, s=t,v,w have three distinct
colours. Since pq is an edge, E forces pq to be exactly the complementary
two colours to vw. Thus exactly one of p,q equals s=t. Since z is
adjacent to both p and q, exactly one of v,w equals z. Consequently E
is the disjoint union of four cases

`E_{d,e}: s=t=d, z=e, opposite(d) != opposite(e)`,

where `d in {p,q}`, `e in {v,w}`, and opposite interchanges each pair.
The final inequality is essential. In each case the four colour classes
are `{s,t,d}`, `{z,e}`, `{opposite(e)}`, `{opposite(d)}`.

The r colour is unique and equals opposite(d): the full legal set is
`{0,1,2,3} minus {s,v,w,t}`. This is the same original r lift, with
exactly the edges `rs,rv,rw,rt`. The R frame has `s=t`, `z!=r`, while
pq omits the other colour on vw, violating the already proved R joint
condition. This recovers why E is forbidden in a true source without
discarding any U colouring merely for lacking an r lift. Outside E,
empty r-lift sets remain legitimate and are retained in the checker.

## 2. Exact finite family of whole-graph obligations

All quotients retain every original edge; loops are retained as a
colourability obstruction, and only duplicate parallel constraints are
suppressed. Vertices not in an indicated class retain their identities.

Define `H_d=U/(s=t=d) + opposite(d)v + opposite(d)w`.
There is a literal bijection

`Col_4(H_d) <-> {complete f in Col_4(U): E(f), s=t=d}`.

For the four finer obligations define

`K_{d,e}=U/({s,t,d},{z,e}) + opposite(d)opposite(e)`.

The original edge `z opposite(d)` already enforces the other required
inequality. Hence

`Col_4(K_{d,e}) <-> {complete f in Col_4(U): E_{d,e}(f)}`.

These are bijections on full colourings, including every private vertex,
and hold fibre by fibre in one fixed colour frame. No quotient witness
can be chosen independently of its lift. Thus

`|E(U)| = |Col_4(H_p)|+|Col_4(H_q)|`

`       = sum_{d in {p,q},e in {v,w}} |Col_4(K_{d,e})|`.

Empty fibres and looped graphs contribute zero. This supplies two, or
four, exact colourability obligations. It does not establish any one
of them. The remainder proves that relative planar-source minimality
cannot establish them by these direct constructions.

## 3. Three original common-neighbour lemmas

The frozen [small-cap theorem](frozen/audits/2026-10-13-c5-no4ct-frontier-6943561/w5/PROOF.md)
states that every original simple C4 has empty bounded interior, and
every proper original C5 has empty bounded interior or a unique W5
centre of complete original degree five. These are relative-minimum
theorems; no general Four Colour Theorem is used here.

### 3.1 The pair s,t

`N_G(s) intersect N_G(t)={r}`.

The edge contacts exclude all original B vertices from this intersection.
Suppose an additional common inner neighbour j exists. The original
cycle `C=(x,s,j,t,y)` is simple: j differs from r and from its four
listed vertices, and none of those identifications is permitted by the
original apex contacts. It is proper because it contains inner vertices.
Its bounded side near the original edge xy is the inside of G. At x,
the original four-neighbour order `(y,r,s,c)` places the original edge
xr strictly between xy and xs in that bounded sector. The vertex r is
not on C; the edge xr cannot cross C, so r is strictly inside C.
The small-C5 theorem makes r its unique degree-five centre, contradicting
`d_G(r)=6`. The argument uses the original disk and its actual rotation.

After deletion of r and identification a=c=z, this becomes

`N_U(s) intersect N_U(t)={z}`.                         (1)

### 3.2 The nonconsecutive apex pair s,p

`N_G(s) intersect N_G(p)` is `{q}` if sq is an edge and is empty otherwise.

Again no B vertex is a common neighbour, by the original contacts. If
an additional common inner neighbour j differs from q, use the simple
proper original cycle `C=(s,c,b,p,j)`. All vertices are distinct; in
particular j cannot be b,c because s-b and p-c are forbidden contacts.
At b the original four-neighbour order `(a,p,q,c)` puts bq strictly
inside the sector between bc and bp on the side avoiding the exterior
of G. Since q is not on C, it is strictly inside. The small-C5 theorem
therefore forces q to be the complete degree-five centre and, in
particular, forces qs. The source geometry then gives c0=4. This
contradicts the already proved
[low-q theorem](frozen/audits/2026-10-14-lowpq-source-676b102/pq/PROOF.md)
`d_G(q)=5 => c0>=6`. Thus no such j exists.

In U the new common neighbour z is present, so

`N_U(s) intersect N_U(p)={z} union ({q} if c0=4)`.      (2)

The same argument reflected in the entire original source gives the
corresponding pair t,q. It is not an independent renaming of a piece.

### 3.3 The consecutive apex pair t,p when tp is absent

Assume a0>=5, equivalently tp is absent. Then

`N_U(t) intersect N_U(p)={z} union ({j_a} if a0=5)`,    (3)

where j_a, when present, is the unique middle vertex of the original
inner a-fan `(t,j_a,p)`.

In G, a is a common neighbour. Any other common neighbour j is an inner
vertex by the original contacts. The cycle `(t,a,p,j)` is simple.
Near a its bounded sector is the original inner sector from at to ap,
avoiding the original boundary edges ay and ab. The C4 theorem leaves
that bounded disk without vertices. It is triangulated, tp is absent,
and so its diagonal must be aj. The faces atj and ajp fill precisely
that inner sector. Hence the full original a-fan is `(y,t,j,p,b)`,
and a0=5. Conversely that fan at a0=5 provides the unique such j.
When a,c become z there is no other new common neighbour: t is not
adjacent to c and p is not adjacent to c. This proves (3).

The common neighbours in (1)--(3) are exact sets in the same graph.
The possible q and j_a are distinct, since j_a is adjacent to original
a whereas q is not. Literal reflection supplies all q-side identities.

The frozen [collar-neighbour lemma](frozen/audits/2026-10-14-lowpq-source-676b102/r6/PROOF.md)
also gives the exact identities

`N_U(z) intersect N_U(v)={s}`,
`N_U(z) intersect N_U(w)={t}`.                         (4)

Indeed every z-neighbour comes from an original a/c-neighbour; that
lemma excludes all its v/w contacts except the actual fan edges sv,tw.
The induced C5 supplies the other missing edges vt,sw.

## 4. A planar first step, followed by a necessarily nonplanar step

The pair s,t is a nonedge on the actual exterior of U. The frozen
[cofacial construction](frozen/audits/2026-10-14-cofacial-fibres-676b102/r6/PROOF.md)
therefore constructs `J=U/(s=t)` as a loopless planar graph. Identity
(1) says exactly one parallel-edge pair, the two edges to z, is
suppressed. Thus

`|V(J)|=k-1`, `|E(J)|=3k-9=3|V(J)|-6`.

It is a simple sphere triangulation. Its actual exterior triangle is
`([s=t],v,w)`; the original face zpq is retained. A thin C5 cap gives
`k-3<k` interior vertices, so source minimality supplies a complete J
colouring and hence a nonempty complete s=t fibre in U. No marked
p/q fibre of J has been specified by that existence argument.

If a0=4, identifying p with `[s=t]` contracts the original edge tp
and creates a loop. Suppose a0>=5. Put

`delta_p = [a0=5]+[c0=4]`.

Equations (1)--(3) show that identifying `{s,t,p}` suppresses exactly
`2+delta_p` edges: three edges to z become one, plus one duplicate at
j_a when a0=5 and one at q when c0=4. All other original incidences
are single, by the exact common-neighbour sets. The two indicators
cannot both be one, since then h=1, contrary to h>=3. Hence delta_p<=1.
For `I_p=U/(s=t=p)` we obtain

`|V(I_p)|=k-2`, `|E(I_p)|=3k-10-delta_p`.

This exceeds `3|V(I_p)|-6=3k-12` by `2-delta_p>=1`.
So I_p is nonplanar in **every** embedding. Adding the two forcing
edges to obtain H_p cannot repair this. It has excess `4-delta_p>=3`.

On the reflected side, sq creates a loop when c0=4. Otherwise define
`delta_q=[c0=5]+[a0=4]<=1`; the same conclusions hold for I_q,H_q.

For the finer quotient, after forming I_d, (4) says z and e have
exactly one common neighbour, the merged vertex `[s=t=d]`. Their
identification suppresses precisely one additional edge. The remaining
forcing edge `opposite(d)opposite(e)` is an original nonedge and has
distinct, unchanged endpoints. Thus every loopless K_{d,e} has

`|V(K_{d,e})|=k-3`, `|E(K_{d,e})|=3k-10-delta_d`.

Its planar edge bound is `3k-15`, exceeded by `5-delta_d>=4`.
This is a fresh count for the final quotient; nonplanarity of an
intermediate graph alone would not justify nonplanarity after another
identification.

| Construction | Vertices | Edges in loopless case | Planar excess |
| --- | ---: | ---: | ---: |
| J=U/(s=t) | k-1 | 3k-9 | 0; explicitly planar |
| I_d=U/(s=t=d) | k-2 | 3k-10-delta_d | 2-delta_d>=1 |
| H_d | k-2 | 3k-8-delta_d | 4-delta_d>=3 |
| K_{d,e} | k-3 | 3k-10-delta_d | 5-delta_d>=4 |

In particular no sequence of face-interior arcs realizing exactly these
classes while retaining all original edges can exist. Such an embedded
forest would contract to a planar graph, contradicting the final count.
This is stronger than observing crossing arcs in the original exterior;
it also rules out a different planar embedding of the specified quotient.

## 5. The unsplit augmentation and completion cost

The single construction `U/(s=t)+pv+pw+qv+qw` contains a literal K3,3
with parts `{z,v,w}` and `{[s=t],p,q}`. All nine cross edges are either
mandatory original edges or the four added edges. No source-specific
degree or common-neighbour lemma is needed for this obstruction.

If one ignored planarity, a thin cap on I_d or H_d would numerically
have k-4 interior vertices, and one on K_{d,e} would have k-5.
These are not legal planar comparison disks. Their numerical budgets
do not activate minimum-source colourability. No Four Colour Theorem
is being used to colour a nonplanar graph.

There is also no completed-source descent hidden in the quotient size.
U has k vertices and reconstructing the original G restores five net
vertices: r,x,y,b and the split of z into a,c. From I_d one must first
split the triple class, restoring two vertices; from K_{d,e} one must
also split `{z,e}`, restoring three in total. Therefore

`(k-2)+2+5=(k-3)+3+5=k+5=|V(G)|`.

This records the exact completed-source cost. It does not assert that
every quotient colouring has all original G lifts: the whole point is
to force a forbidden U event before that reconstruction. The quotient
bijections in section 2 only claim complete U fibres with the indicated
equalities and inequalities.

## 6. Verification and remaining obligation

The [checker](checks/check_forcing.py) independently enumerates all
proper seven-pin assignments, computes every r lift, and proves the
two- and four-obligation decomposition directly. It does not import or
rebuild the old 26-row table. Whole-graph controls include an eighth
private vertex, all original edges, all complete colourings, and every
local-proper seven-pin fibre including empties. Quotient colourings are
pulled back and compared with these exact whole-graph fibres.

Five exhaustive degree classes under a0,c0>=4 and a0+c0>=11 verify
the duplicate-edge arithmetic. Their incidence models are not source
graphs. The arbitrary-size common-neighbour and nonplanarity results
are the paper arguments above; finite checks do not certify those
topological premises. Genuine minimum sources supplied: zero,
**not triggered**. The required forbidden complete U colouring, an
alternative planar construction or genuine strict completed-source
descent, all-size 319 exclusion, and the general theorem remain OPEN.

There is no new Lean result, external enumeration, shared-doc mutation,
commit, or push in this audit.
