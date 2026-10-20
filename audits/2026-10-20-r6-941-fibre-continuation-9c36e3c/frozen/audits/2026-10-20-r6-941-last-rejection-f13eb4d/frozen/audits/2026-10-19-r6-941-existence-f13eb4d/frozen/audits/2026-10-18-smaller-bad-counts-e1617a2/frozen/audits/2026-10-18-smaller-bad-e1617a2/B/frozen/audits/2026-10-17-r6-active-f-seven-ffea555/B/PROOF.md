# B: the remaining active-f seven-cap meets only the z hub

Frozen BASE: `ffea555fc2a896d8166ce198ca28ed9262912f25`.
This independent paper audit accepts the localization and the four-row
necessary-degree table below. It proves an arbitrary-size statement about
the same hypothetical original source; it does not establish reference
region separation or even-complement positivity.

## 1. Fixed source and notation

Keep the original minimum completed no4ct C5 source G, its ordered boundary
`(x,y,a,b,c)`, original apexes `(r,t,p,q,s)`, actual supports, attachments,
rotation and private vertices. Keep the entire U319 relation on
`(z,s,v,w,t,p,q)`, including empty complete fibres and every original r
lift, and the actual graphs `J=U/(s=t)`, `m=[s=t]`, `D=J*`. The literal
marks are `e=(vw)*`, `f=(pq)*`, `g=(mz)*`. There is no additional
assumption that original v has degree five.

Take any ordinary perfect matching `M in P101`: `e,g in M`, `f not in M`.
Suppose a nonfacial seven-component C of `D-M` contains f, and put
`X=V(C)`. The adopted [seven-cycle classification A2--A3](../frozen/audits/2026-10-17-r6-joint-positive-113e41f/A/PROOF.md)
gives one centre `u in {p,q}` of J degree four, one ordinary centre h of
unchanged original/J degree five, one matching chord `(uh)*`, and exactly
five matching spokes `delta_D(X)`. The ordinary centre avoids
`{m,z,v,w,p,q}`. This uses an ordinary matching and requires neither a
Tait colouring for M nor oddness minimality.

Write `a0=d_G(a)`, `c0=d_G(c)`. For the p-centred case write the original
facial link as

`N_G(p)=(a,b,q,ell,n)`.

Here n is the vertex called **m in the old low-p files**. It is an
original vertex, distinct from the present quotient hub `m=[s=t]`.
The exact degree formula and the original fan give

`d_G(p)=5`, `a0>=6`, `N_J(p)=(z,q,ell,n)`.

The last list is an induced facial link. Therefore h is exactly ell or n;
z is a hub and q would make f the common chord rather than a boundary
edge of C. The reflected q-centred list is

`N_G(q)=(c,b,p,ell_q,n_c)`, `N_J(q)=(z,p,ell_q,n_c)`,

with `d_G(q)=5`, `c0>=6`. The notation ell_q denotes the literal
reflection of ell. If both low links occur in one G, ell and ell_q are
the same original third vertex of the face on pq opposite bpq.

## 2. Why the separately proved nonedges can be retained together

The [cofacial low-p proof, section 3](../frozen/audits/2026-10-14-cofacial-fibres-676b102/pq/PROOF.md)
constructs a nonempty complete-colouring fibre on one literal deletion
graph and proves the original graph facts

`ell-s, ell-t not in E(G)`.

The [subsequent low-p proof, section 4](../frozen/audits/2026-10-14-lowpq-source-676b102/pq/PROOF.md)
constructs another nonempty complete-colouring fibre and proves

`n-s, n-t not in E(G)`.

Both arguments retain each of these putative original edges in their
respective deletion graph. In each argument a complete colouring would
assign its two endpoints the same colour, contradicting that retained
edge. Each conclusion is thus a graph nonedge of this same G, universally
under the common low-p source assumptions. The conjunction of the four
nonedges is valid. No assignment, multiplicity, private colour or Kempe
component from the two different colourings is combined.

Merging s,t creates no additional h-m incidence beyond an original
h-s or h-t edge. Consequently

`ell-m, n-m not in E(J)`.

Also p-m is absent, directly from the displayed complete p link. All
these vertices are distinct: the low-p proof has already excluded a0=4
and a0=5, and its original fan has n distinct from t. The old complete
fibres retain their original quantifiers and all their complete lifts;
none is asserted to be a colouring of the odd-complement matching M.

The [original collar lemma, sections 1--3](../frozen/audits/2026-10-14-lowpq-source-676b102/r6/PROOF.md)
gives

`pv,pw,qv,qw,nv,nw not in E(G)`.

For n this uses its original a-incidence and n!=t. These nonedges survive
unchanged in J. If h=ell, its ordinary degree five is original degree
five, and its complete original facial link must be

`N_G(ell)=(p,q,u1,u2,n)`.

Indeed the original p link already supplies the consecutive faces
`pqell` and `pell n`; degree five leaves exactly the two intermediate
neighbours u1,u2. If ell were adjacent to v or w, that neighbour could
only be u1 or u2: p,q,n are distinct from v,w. At u1 the consecutive
link edge would give qv or qw; at u2 it would give nv or nw. Every one
of these edges is absent. Therefore

`h=ell and d_G(ell)=5 => ell-v,ell-w not in E(G)`.

Together these prove, in both allowed centre positions,

`E_J({p,h},{m,v,w}) = empty`.

The already published [later r6-low-p proof](../frozen/audits/2026-10-14-r6-lowpq-3953c85/r6/PROOF.md)
independently gives ell-v and ell-w for all r=6,p=5, without the extra
ell-degree-five premise. The preceding direct triangular-link proof
uses only the weaker facts required for this present seven-cap.

## 3. Constructing Q5 explicitly

Each dual vertex in X is a primal triangular face incident with p or h.
The two faces shared by these adjacent centres are counted once, so
there are `4+5-2=7` such triangles. They form the actual closed disk K
which is the union of their two closed primal stars. Its interior
vertices are precisely p,h; the actual outer boundary is Q5.

There are exactly two common neighbours of p,h: any common neighbour
makes a primal triangle on ph, every primal triangle is facial, and ph
has exactly its two actual incident faces. Thus the two complementary
link paths meet just at their endpoints and Q5 is a simple five-cycle.
More explicitly:

| centres | complete five-degree link | actual boundary order of Q5 |
| --- | --- | --- |
| p,ell | `(p,q,u1,u2,n)` at ell | `(z,q,u1,u2,n)` |
| p,n | `(p,ell,u1,u2,z)` at n | `(z,q,ell,u1,u2)` |

Each displayed row follows the link orientation; reversing the entire
row gives the same actual embedded boundary. In the second row z is
the image of the original neighbour a of n; no fictitious original
n-z edge is introduced. The five boundary primal edges correspond
exactly to the five spokes `delta_D(X)`. This is the adopted induced
Q5: a putative chord would yield a facial triangle with two matching
spokes incident at one dual vertex, violating the matching property.

In particular

`V(Q5) = (N_J(p) union N_J(h)) minus {p,h}`.

Since z is a neighbour of p and is neither centre, z lies on Q5. The
absence of centre incidences to m,v,w from section 2 excludes all three
of those vertices from its boundary. We obtain the exact localization

`V(Q5) intersect {m,z,v,w} = {z}`.

Reflect the entire original source by

`(x,y),(a,c),(p,q),(s,t),(v,w)`.

It fixes the quotient hubs m,z and transports all retained edges,
nonedges, faces, original sectors and full fibres together. On the q
side the corresponding complete links and Q5 boundaries are

| centres | complete five-degree link | actual boundary order of Q5 |
| --- | --- | --- |
| q,ell_q | `(q,p,u1',u2',n_c)` at ell_q | `(z,p,u1',u2',n_c)` |
| q,n_c | `(q,ell_q,u1',u2',z)` at n_c | `(z,p,ell_q,u1',u2')` |

The reflected source nonedges are `ell_q-s,ell_q-t,n_c-s,n_c-t`,
`n_cv,n_cw,pv,pw`; the same five-degree link argument excludes
ell_q-v,ell_q-w in its ordinary-centre subcase. Thus the exact same
hub-intersection conclusion holds on the q side as well.

## 4. Both common marks are wholly exterior, at distance at least two

The complete disk description shows that neither endpoint of e or g
belongs to X. Indeed a dual endpoint of e is a triangular primal face
containing vw. For such a triangle to be in X it would also have to
contain a centre u or h; section 2 excludes even an incidence from a
centre to v or w. A dual endpoint of g is a triangular primal face
containing mz. Its belonging to X would require centre adjacency to m,
which is also absent. Hence

`V(e) intersect X = V(g) intersect X = empty`.

Equivalently, a marked matching edge incident with X could only be the
unique internal chord or a spoke. Neither primal mark is uh, and Q5
avoids v,w,m, so neither mark belongs to its spoke set. This checks the
same conclusion through the exhaustive matching incidences at X.

Finally let t be any endpoint of e or g. It is exterior and already
matched by that marked edge. If t had a neighbour in X, their edge
would be a spoke in `delta_D(X) subseteq M`, distinct from the marked
edge whose two endpoints are exterior. That would give two matching
edges at t. Therefore no such edge exists, and

`dist_D(X,V(e) union V(g)) >= 2`.

This distance concerns the full dual graph. It does not say that these
sets lie in different components of any complete exchange graph.

## 5. Independent check of the necessary-degree table

Here are the local matching reasons needed in addition to the frozen
low-p/low-q degree bounds; they also check that the table records only
necessary conditions.

If c0=4, the original c-fan endpoint is literally beta=q. The actual
faces at mz and pq include `mzq` and `zpq`. Since g is selected,
`(zq)* not in M`; since f is omitted, the dual vertex of `zpq` then
forces `(zp)* in M`. A p-centred seven-cap would have `(zp)*` on C,
because z is not its ordinary centre. This is impossible. A q-centred
cap has original q degree five and already forces c0>=6. Thus c0=4
admits neither centre. The reflected argument uses the actual faces
`mzp,zpq`: g forces `(zp)* not in M`, then f's omission forces
`(zq)* in M`, excluding the q-centred cap; p-centred caps already force
a0>=6. Therefore a0=4 is excluded as well.

If the centres are p,n and a0=6, the complete original a fan is
`(y,t,alpha,n,p,b)` with all six neighbours distinct. Its true triangles
give `T=(m,z,alpha)` and `T'=(z,alpha,n)` in J. The dual vertex of T
is outside X, since T contains neither p nor n; that of T' is inside X,
since n is a centre. Therefore `(z alpha)*` is a spoke and belongs to
M. It is incident with the dual vertex of T, which is already matched
by g. This is impossible. The prior a0>=6 bound strengthens to a0>=7
in this particular centre position. Full reflection gives c0>=7 for
the q,n_c position, using `T=(m,z,beta)`, `T'=(z,beta,n_c)`.

The original boundary lower bound four, together with these arguments,
gives exactly:

| four-degree J centre | ordinary original five-degree centre | necessary original degrees |
| --- | --- | --- |
| p | ell, the other pq-face vertex | `a0>=6, c0>=5` |
| p | n, the a-fan neighbour immediately before p | `a0>=7, c0>=5` |
| q | ell_q, the other pq-face vertex | `a0>=5, c0>=6` |
| q | n_c, the c-fan neighbour immediately before q | `a0>=5, c0>=7` |

The ordinary-centre distinction is essential. No a0>=7 conclusion is
made for the p,ell row, nor c0>=7 for q,ell_q. None of these necessary
rows is asserted realizable by an original minimum source.

## 6. Evidence boundary

All 17 copied inputs in the parent [INPUTS.json](../INPUTS.json) were
checked against their recorded byte counts and SHA256 values; drift was
zero. The source geometric proof above has no finite enumeration
premise. No new finite-colouring table, source example, external theorem,
4CT invocation or Lean theorem is used or produced. In particular the
complete U319 relation and every original lift retain their previous
authority, and no supplied actual minimum source triggers the target.

The a0=4/c0=4 exclusion and specified a0=6/c0=6 exclusion are complete
arbitrary-size subcase exclusions. The remaining active-f seven-caps,
their possible complete-region connection to a marked obstruction,
other odd components, `W110+W101>0`, even-complement positivity and
complete319 remain OPEN. The exteriority and distance conclusion alone
does not establish `W_C(R100) != W_g(R100)` for any actual reference.
