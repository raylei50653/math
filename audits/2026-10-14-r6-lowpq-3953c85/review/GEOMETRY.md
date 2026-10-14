# Independent geometry and quotient review

BASE: `3953c85e334b96533e44652df065640f5463715a`. This review uses the
fixed globally minimum noncatalogue source with original boundary
`B=(x,y,a,b,c)` and `d_G(x)=d_G(y)=d_G(b)=4`. Every degree below is an
original G degree. It does not assert a source realization or general
catalogue improvement.

## 1. The two faces in the r=6, p=5 intersection

The inherited source facts are in
[source geometry](../../2026-10-14-c4-mask13-joint6-fdd3e22/SOURCE_GEOMETRY.md),
[degree-six transfer](../../2026-10-14-c4-c5-recursion-fdd3e22/degree4/R6_TRANSFER.md),
[low-p proof](../../2026-10-14-lowpq-source-676b102/pq/PROOF.md), and
[collar exclusions](../../2026-10-14-lowpq-source-676b102/r6/PROOF.md).

The literal graph `W=R-{r,p}` has `k-1` vertices. Its actual faces are
`F=(z,s,v,w,t)` and `P=(z,q,ell,m)`; their interiors are disjoint and their
boundary cycles share exactly z. The eight named vertices are distinct.
In particular, p is adjacent to ell,m and not v,w, so neither ell nor m
can alias v or w. The previously excluded a=4 case removes the sole
possible alias m=t. The other aliases are excluded by the induced p link,
the distinct original apexes, and p's original nonedges to r,s,t.

The original low-p argument gives `ell-s,ell-t,m-s,m-t` as nonedges.
The r=6 collar lemma gives `m-v,m-w`. The collar lemma by itself says
nothing about ell-v or ell-w: ell is not an original a/c neighbour,
because z-ell is absent in the induced p link.

For a simultaneous quotient, it is sufficient to draw added arcs in
the specified faces with disjoint interiors and to contract their
components, provided every resulting equivalence class is an independent
set of the original W. This includes nonedges across different faces
when the arcs join through their common endpoint z; such a cross-face
class requires checking every cross pair, not merely each drawn arc.
No original edge can be removed to repair a loop. Parallel edges can be
suppressed without changing the exact complete-colouring pullback.

## 2. Independently checked new nonedges ell-v and ell-w

Simultaneously draw the diagonals s-w in F and z-ell in P. The classes
`{s,w}` and `{z,ell}` are disjoint independent sets, and the arcs occupy
different faces. The loopless planar quotient has `k-3` vertices and a
surviving edge (for example the image of zs). The established thin-C5
cap adds three vertices; its C5 interior count is `k-5<k`. Minimum-source
colourability therefore supplies one complete W colouring with
`s=w` and `z=ell`.

Since z=ell, p has at most three neighbour colours and has a legal lift
to the same U=W+p. Its boundary is in the exact support319. The only
support319 row satisfying s=w is ABABC on `(z,s,v,w,t)`. Thus z=v, and
the same complete W colouring has ell=v. Every original retained edge
is proper in that colouring, so `ell-v` cannot be an original edge.

Similarly, the disjoint identifications `{v,t}` and `{z,ell}` force
the support319 row ABCAC. Consequently z=w=ell in one complete W
colouring, excluding the original edge `ell-w`.

These are separately existing full colourings. No assertion combines
their pin values into one colouring. The two faces and quotient budget
are unchanged by unknown edges between their other retained pins.

After these nonedges are established, `{z,v,ell}` and `{z,w,ell}` are
legal individual identification classes using a tree with one arc in
each face. Their legality does not extend to crossed diagonals: z-v
and s-w cross in F, as do z-w and v-t; z-ell and q-m cross in P.
Thus these pairs cannot be combined by this particular facial-arc proof.

## 3. Induced collar for every h in the fixed three-four-degree branch

This statement does not assume r=6 or p=5. Put
`alpha=d_G(a)-4`, `gamma=d_G(c)-4`, and `h=alpha+gamma`.
The original collar is

`C=(r,t,A_1,...,A_alpha,p,q,C_1,...,C_gamma,s)`.

In the four-connected sphere triangulation T0, the z-link is the cycle
`(x,y,t,A_1,...,A_alpha,p,q,C_1,...,C_gamma,s)`.
It is induced: any chord would give a nonfacial triangle through z,
contrary to four-connectivity. Delete x,y from this link. The remaining
path is induced. Its vertices are exactly `N_R(z)`; the established
identity `N_R(z) intersect N_R(r)={s,t}` shows that adding r introduces
only the two cycle edges r-s and r-t. Hence the original collar C is an
induced cycle of length `h+5`, for every h in this fixed source branch.

Let H be its bounded triangular disk and let
`Pprivate=V(G) minus (B union C)`. Define

`E=sum_{u notin B}(d_G(u)-5)=k-h-6`,
`E_C=sum_{u in C}(d_G(u)-5)`,
`e_P=|E(G[Pprivate])|`.

Then `|Pprivate|=k-h-5=E+1`. Each of the five apexes has two original B
neighbours and two collar neighbours. Each of the h other collar
vertices has one original B neighbour and two collar neighbours. Since
the collar is induced, their remaining neighbours are precisely private
vertices. Consequently

`|E(C,Pprivate)|=5+2h+E_C`.

Private vertices have no B neighbours, and their total degree is
`5(E+1)+(E-E_C)`. Equating this with
`|E(C,Pprivate)|+2e_P` yields the exact identity

`h=3E-E_C-e_P`.

The induced private graph is connected. Indeed every bounded triangular
face of H has a private vertex (an all-collar triangle would require a
collar chord), and every inner edge has a private endpoint. Adjacent
bounded faces therefore have their private vertices in the same private
component. The dual adjacency graph of the bounded triangular faces of
a disk is connected, and every private vertex belongs to one such face.
Thus `e_P>=|Pprivate|-1=E`.

Writing `rho=e_P-|Pprivate|+1>=0`, the same exact identity is

`h=2E-E_C-rho`, equivalently `3h=2k-12-E_C-rho`.

The old source theorem r>=6 implies `E_C>=1`. Thus k<=27 forces h<=13.
This excludes all h>=14 in the fixed branch; it does not upgrade the
general catalogue equality or eliminate the lower-h source residual.

## 4. Additional cycle in the r=6 private graph

For r=6 the consecutive r neighbours v,w are private: neither is in B
or the original collar. The original face r-v-w lies on one side of vw.
Let j be the third vertex of the face on its other side. This j is
distinct from r,v,w. It cannot belong to B, because v,w have no original
B neighbours. It cannot be any collar a-neighbour other than t, nor any
collar c-neighbour other than s, by the inherited collar exclusion lemma.
It cannot be t because t-v is absent, and cannot be s because s-w is
absent. This exhausts the collar. Therefore j is private, and v,w,j form
a triangle in the private graph.

Hence r=6 forces `rho>=1`. Also the inherited r=6 theorem gives r,s,t>=6,
so `E_C>=3`. Substitution into the exact identity gives

`h<=2E-4`, or `3h<=2k-16`.

In particular, `r=6 and k<=27 => h<=12`. This strengthening does not
depend on p=5 or the new ell-v/ell-w nonedges. It is a structural degree
bound and does not exclude the entire r=6 source branch.

## 5. Stronger general private-cycle bound, independently reviewed

The companion h18 investigation strengthens the preceding degree bound
without assuming r=6. It also uses the accepted
[double-low ell bound](../../2026-10-14-c4-return-branches-a11d4bb/pq/PROOF.md)
and [zero-side s/t bounds](../../2026-10-14-c4-return-branches-a11d4bb/r_high/PROOF.md).
First, `E>=3` in every source in this fixed branch.
If r=6, r,s,t already contribute three units. If r>=7, r contributes
at least two; either one of p,q is high and contributes another unit,
or p=q=5 and their opposite-face vertex ell has degree at least six.
These vertices are distinct. Likewise `E_C>=2`: r>=7 supplies two, and
r=6 instead supplies three via r,s,t. Hence there are at least four
private vertices.

There is no leaf u of the connected private graph. If u had just one
private neighbour v, the rest of its original degree, at least four
vertices, would be collar neighbours. In the cyclic link of u, they
form one contiguous list `c_1,...,c_L` with v the other vertex. Every
consecutive pair is a collar edge; the collar is induced, so the list
is a path on the actual collar. Each intermediate c_i has just the
three H neighbours `c_(i-1),u,c_(i+1)`: the two actual triangles at
u-c_i fill its entire H-side sector between its two collar edges.

There are at least two such consecutive intermediate vertices. A
single-contact collar vertex would then have original degree four,
which is forbidden; every intermediate vertex is therefore a
degree-five apex. The only possible adjacent pair of degree-five
apexes on C is p,q. The pairs r,t and s,r include r>=6. The pair t,p
is adjacent only when alpha=0, which forces t>=6. The pair q,s is
adjacent only when gamma=0, which forces s>=6. Consequently L=4,
the intermediate vertices are exactly p,q, and d_G(u)=5. The other
original face of pq has third vertex u=ell. But p=q=5 forces ell>=6,
a contradiction.

The private graph is thus connected with minimum degree at least two.
If its cycle rank were one, it would be exactly one cycle on all its
vertices. The collar lies outside that cycle; there are no other
private vertices inside it. Since the cycle has at least four vertices,
triangulation of its empty bounded side would require a private chord,
contrary to the graph being exactly a cycle. Therefore `rho>=2`.

The exact identity from Section 3 now gives, throughout the fixed
three-four-degree source branch,

`3h=2k-12-E_C-rho <= 2k-16`.

In particular **k<=27 forces h<=12**. This subsumes the weaker h<=13
consequence and excludes the proposed h=18 extreme without mixing
relations from different vertex-deletion graphs. The r=6 private
triangle in Section 4 remains a separate geometric consistency check.

## 6. Review boundary

The arguments above are paper geometry and exact degree counting. They
do not need a large graph enumeration, an abstract count-feasibility
claim, or a new external theorem. The two new ell nonedges use the old
complete support319 theorem only after guaranteeing a legal p lift of
the same W colouring. Numerical local cap checks in the companion audit
are separate evidence; this file does not treat them as a planar
embedding certificate.

The final [r6 proof](../r6/PROOF.md) and [h18 proof](../h18/PROOF.md)
were read independently in full and pass this review. Their stated
limits are necessary: ell-v/ell-w do not exclude all r=6 sources, and
the new h<=12 active-domain bound does not change the general K<=22
catalogue equality. Each of the two r6 complete-fibre unions is
nonempty; its individual constituent fibres are not separately asserted
nonempty without an additional source condition.

[independent_caps.py](independent_caps.py) imports no companion checker.
It uses the inherited degree-six transfer table and independently tests
every literal cap edge on all 210 canonical proper eight-pin rows.
[Its result](independent-caps.json) matches every full cap lift and all
120 necessary rows in the companion certificate, including the two
2-row fibre unions and both 16-row three-vertex quotient slices.
These nonempty local slices are not source realizations.
