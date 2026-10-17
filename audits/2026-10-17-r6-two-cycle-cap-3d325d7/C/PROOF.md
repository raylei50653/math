# C. The exact common-colour z-cycle criterion for R100 separation

Frozen BASE: `3d325d7197aa05815c71bedc52c1b253d736c7bb`.
This independent paper audit writes only `C/`. It proves the separation
criterion and the stated short-cycle exclusions for the same arbitrary-size
hypothetical source. It supplies neither a separating colouring nor a
matching repair.

## 1. One source, one matching, and one complete colouring

Keep the original minimum completed no4ct C5 source G, its ordered boundary
`(x,y,a,b,c)`, supports, attachments, rotation, and all private vertices.
Retain the entire U319 relation on `(z,s,v,w,t,p,q)`, including empty
complete fibres and all original r lifts. The actual graphs and literal
marks are

`J=U/(s=t)`, `m=[s=t]`, `D=J*`,
`e=(vw)*`, `f=(pq)*`, `g=(mz)*`.

No original `d_G(v)=5` assumption is added. Fix any ordinary actual
`M in P101`, so e,g belong to M and f does not. Suppose the complete
complement `F=D-M` has a nonfacial seven-component C containing f.
Write `X=V(C)`. The frozen
[seven-cap geometry](../frozen/audits/2026-10-17-r6-active-f-seven-ffea555/B/PROOF.md)
provides its actual two-star disk K, with centres p,h in the p-centred
case, or q,h in the reflected case. Its five actual rim edges are dual
to all five matching spokes. The only M-dual edge at either centre is
the centre edge ph, or qh, respectively. In particular, for

`P=(V(J),M*)`,

both centres have P-degree one. This is an ordinary matching statement;
M itself is not assumed to be an even-complement matching.

Fix **one actual complete all-distinct source colouring** chi on this
same graph. Normalize its three Tait colours by

`chi(e)=alpha`, `chi(f)=beta`, `chi(g)=gamma`,
`R=R100=chi^{-1}(alpha)`.

R is a whole actual perfect matching with even complement. Set

`L_R=D-(M intersect R)`,
`S_R=(V(J),(M intersect R)*)`.

The marks satisfy `e in M intersect R`, `f notin M union R`,
`g in M\R`. Thus f and g are edges of L_R, and their whole edges each
belong to well-defined L_R components. Let W_C denote the component
containing C and W_g the component containing g. No local row or
independently feasible colour choice substitutes for chi.

## 2. Faces of S_R and the exact separation criterion

For a spanning subgraph S of a connected sphere graph J, the faces of
embedded S correspond exactly to the components of the dual formed by
retaining precisely the duals of edges outside S. To see this directly,
start with the triangular faces of J. Crossing an edge outside S joins
its two incident face interiors; these are exactly the dual adjacencies
which remain. Their connected unions are the open faces of S. Isolated
vertices and bridges of S do not create extra faces, and the same
argument applies when S is disconnected.

Apply this to S_R. Since neither pq nor mz is an S_R edge, each of their
interior points lies in an open face of S_R. The face containing
`mid(pq)` corresponds to W_C: the complete f edge lies in C. The face
containing `mid(mz)` corresponds to W_g. Consequently

`W_C != W_g`

holds exactly when those two points lie in different faces of S_R.

Two points outside a finite embedded graph lie in different faces if
and only if some simple cycle in that graph separates them on the
sphere. One elementary proof is to take a boundary walk which separates
the faces and split it at repeated vertices: its closed walks decompose
into simple cycles, and at least one of them has odd separation parity
for the two points. Bridges occur twice in a boundary walk and
contribute no separation. The reverse implication is the Jordan curve
theorem. Thus this assertion does not require the boundary of a face of
S_R to be a single simple cycle.

In the p-centred case use the actual embedded path

`T=mid(mz)-z-p-mid(pq)`.

Its edge segments avoid S_R:

* mz is absent from R* because g has colour gamma;
* zp is absent from M* because `(zp)*` is on C;
* pq is absent from M* because f is absent from M.

The displayed path is simple; its only internal primal vertices are
z,p. A simple cycle Z of S_R cannot contain p, since
`deg_{S_R}(p)<=deg_P(p)=1`. Hence such a cycle can meet T only at z.
If it separates the path endpoints, it must meet T; therefore it passes
through z. Since neither zm nor zp is a Z edge, those two rays lie in
the open local sectors determined by the two Z darts at z. The endpoints
of T are on opposite sides of Z exactly when these rays lie in opposite
sectors. T otherwise avoids Z, so this local condition is also sufficient.

We have proved the exact criterion:

**Theorem C1 (actual z-cycle criterion).** In the p-centred case,

`W_C(R100) != W_g(R100)`

if and only if S_R contains an actual simple cycle Z through z whose
two darts at z put the actual rays zm and zp in opposite local sectors.
For a q-centred cap, replace zp by zq throughout, using the actual path
`mid(mz)-z-q-mid(pq)` and `deg_{S_R}(q)<=1`.

The criterion refers to a cycle all of whose edges simultaneously
belong to this one actual `M intersect R100`. Existence of a suitable
cycle of P alone does not establish the criterion.

## 3. Every cycle in S_R is even

Use the common four-colour difference frame of chi, with its three
nonzero differences identified with alpha,beta,gamma in `F_2^2`.
Equivalently, the Tait edge differences integrate on the sphere to a
proper vertex four-colouring of J: each triangular face has all three
nonzero differences, whose sum is zero, and every sphere cycle bounds
a sum of faces. Every S_R edge has the same nonzero difference alpha.
Traversing a cycle of length k in S_R therefore gives

`0=k alpha`,

which forces k even. This argument retains one complete colouring and
one difference frame for all the edges. It does not combine edgewise
possibilities from different chi.

## 4. A p-centred separating four-cycle cannot use zq

In this section let `a0=d_G(a)`, `c0=d_G(c)`. To keep vertex and Tait
colour names distinct, call the actual third vertices of the original
faces on ta and sc respectively alpha0,beta0. The frozen
[sector identities](../frozen/audits/2026-10-16-r6-319-continuation-f1faf74/C/PROOF.md)
are

`N_J(z)-{m}=L_a disjoint-union L_c`,
`N_J(m)-{z}=L_s disjoint-union L_t`,
`L_t intersect L_a={alpha0}`, `L_s intersect L_c={beta0}`,
`L_s intersect L_a=L_t intersect L_c=empty`.

They are literal consecutive sectors in the retained source rotation.
The z rotation, starting just after m, runs through the a-sector to p,
then through the edge pq to q, then through the c-sector back to m.
In particular `p in L_a`, `q in L_c`, and
`beta0=q iff c0=4`. Frozen seven-cap geometry gives
`a0>=6,c0>=5` for either p-centred position h=ell or h=n.

Suppose a cycle satisfying Theorem C1 is a four-cycle and uses zq.
Write its order

`Z=(z,A,B,q)`.

The required separation of zm and zp in the actual z rotation forces
`A in L_a` and `A!=p`. The centres p,h cannot occur anywhere on Z,
because each has P-degree one. Also B cannot be m: a putative mq edge
would place q in `N_J(m) intersect L_c={beta0}`, forcing c0=4,
contrary to c0>=5. Thus A,B,q are distinct retained original vertices,
and the following is a literal simple proper original five-cycle:

`H=(a,A,B,q,b)`.

The edge aA is original because A lies in L_a; AB and Bq are retained
original edges; qb and ba are the original boundary incidences. This
argument does not need H to be induced.

The complete original a rotation ends with `...,n,p,b`, and A occurs
before p in its internal sector. The bounded side of H at a is the
sector between aA and the original boundary edge ab which contains ap.
Since p is not on H, p lies strictly in H's bounded cap. The actual edge
ph cannot cross H, and h is not on H either, so h lies in the same cap.
There are therefore at least two original vertices strictly inside H.
This contradicts the frozen
[proper original C5 cap theorem](../frozen/audits/2026-10-13-c5-no4ct-frontier-6943561/w5/PROOF.md),
which permits at most one.

**Theorem C2 (short-cycle exclusion).** A p-centred S_R separating
four-cycle cannot use zq. The literal reflected conclusion is that a
q-centred separating four-cycle cannot use zp. Both statements hold
for both allowed ordinary-centre positions, without oddness minimality
or an original `d_G(v)=5` assumption.

## 5. The degree-five opposite-sector corollary

If the cap is p-centred and c0=5, the complete original c rotation is

`N_G(c)=(x,s,beta0,q,b)`.

Hence the entire c-sector of z is exactly `{beta0,q}`. The actual face
`mz beta0` exists in J. Its dual vertex is already matched by
`g=(mz)* in M`; therefore `(z beta0)* notin M`, and z beta0 is absent
from P and S_R. For a cycle satisfying Theorem C1, the z dart on the
side of zp opposite zm must be in the c-sector: there is no a-sector
vertex beyond p before q. Thus its only available c-sector edge is zq.

If such a cycle had length four, Theorem C2 would exclude it. All
S_R cycles are even by section 3, and J is simple, so no shorter even
simple cycle exists. We conclude

`p-centred cap and c0=5 => every separating S_R cycle has length >=6`.

Full reflection of the **same source**, including its rotation, marks,
and the whole colouring chi, gives

`q-centred cap and a0=5 => every separating S_R cycle has length >=6`.

No lower bound six is claimed in the general case. If both z darts
range through arbitrary opposite sectors, lifting a four-cycle to G
can yield an original six-cycle. The frozen proper-C5 theorem then
does not apply.

## 6. Verification and authority boundary

Before writing, all 13 root manifest inputs were checked against their
frozen byte lengths and SHA256 digests; drift was zero. The new results
are arbitrary-size conditional paper statements. There is no finite
source example, no new source-realizability control, no external theorem
or 4CT invocation, and no new Lean theorem. No commit or push was made.

Theorem C1 gives an exact existence target for references to which SEP
could apply. It constructs no such reference. In the two-complete-odd-circle
branch, the independent all-reference obstruction prevents its hypothesis
from holding for fixed M; that branch instead needs an actual matching
repair. The remaining active-f seven-caps, other odd complementary
components, the H-connected case, `W110+W101>0`, and complete319 remain
**OPEN**. The earlier completed-source reconstruction cost `k+5` is
unchanged.
