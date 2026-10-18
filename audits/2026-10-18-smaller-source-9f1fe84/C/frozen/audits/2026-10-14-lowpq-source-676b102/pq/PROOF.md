# Low p excludes the original a-degree-five branch

Frozen BASE: `676b1024715f24a0d969fba90baab21b756406e2`, together with the
explicit cofacial-results overlay in [INPUTS](../INPUTS.json). All degrees
below are degrees in the original disk G. No Four Colour Theorem is used.

**New arbitrary-size source conclusion:** under the fixed minimum-source
contract and `d_G(x)=d_G(y)=d_G(b)=4`,

`d_G(p)=5 => d_G(a)>=6`, and, by literal reflection,
`d_G(q)=5 => d_G(c)>=6`.

Thus the whole original branch `p=5,a=5` is excluded, regardless of q or r.
The previously open branches `p=5,a>=6` and its reflection remain OPEN.
This does not prove p,q>=6, a general k>=28 bound, or catalogue equality.

## 1. Exact original source and the one common graph

Use the frozen [source geometry](../../2026-10-14-c4-mask13-joint6-fdd3e22/SOURCE_GEOMETRY.md),
[adjacent-four proof](../../2026-10-14-c4-triangle-core-b66f592/ADJACENT4.md),
and [preceding common-fibre proof](../../2026-10-14-cofacial-fibres-676b102/pq/PROOF.md).
G is a globally minimum noncatalogue C5 disk, with boundary `(x,y,a,b,c)`
and k inner vertices, in the adopted no4ct 932/933/941 contract. It is
triangulated, its original inner degrees are at least five, its boundary
degrees are at least four, every original C4 has empty bounded interior,
and every proper original C5 has empty bounded interior or a single W5
centre. Original triangles have empty bounded interiors. These statements
are available under their strict smaller-source hypotheses.

The original apexes of xy, ya, ab, bc, cx are r,t,p,q,s. Construct the same
T0 as in the authority: identify a,c to z and delete u,b. It is a simple
4-connected sphere triangulation with k+3 vertices and the original
designated facial triangles zxy,zpq. Failure means that **every complete
T0 colouring** has the same palette on xy and pq, in one common frame.

Assume p has original degree five. Its original facial link is
`(a,b,q,ell,m)`; its T0 link is `(z,q,ell,m)`. Put

`D=T0-{x,y,p}=R-p`.

This is the literal k-vertex graph from the preceding audit. It has actual
faces `Q=(z,s,r,t)` and `P=(z,q,ell,m)`. The earlier common quotient proved
p=5 implies a>=5. Consequently m!=t and these faces share exactly z.
All seven named vertices are distinct. The induced p link gives zell and
qm as nonedges, and the original xy deletion gives zr as a nonedge.

All original edges outside the deleted caps remain. Reconstructing T0
adds exactly

`zx,sx,rx,xy,zy,ry,ty,pz,pq,pell,pm`.

For each **one complete D colouring**, its legal p colours and legal
ordered xy assignments form their Cartesian product, since p has no edge
to x or y. Every product member is the corresponding complete T0 lift.
The original faces zxy,zpq are thereby restored literally.

In R, Q has exactly mask13. Its ABAC fibre is empty, and every ABAB
complete colouring has pq palette CD after normalization to Q=ABAB.
These full-fibre facts, not only their projected supports, are used below.

## 2. The additional nonedge r-ell

We first make an implicit consequence of the original small-cycle
geometry explicit:

`r ell is not an edge of G`.

Otherwise `C=(y,a,p,ell,r)` is a simple proper original C5. All named
vertices are distinct; ell is an original inner vertex and is neither
t nor any boundary vertex. The edge ya lies on the original boundary.
At y the original cyclic order is `(a,t,r,x)`, up to reversal. The bounded
side of C uses the internal sector from ya to yr, and contains t strictly
inside. Thus the small-C5 result makes t the unique interior vertex.
Planarity then confines every neighbour of t to C. Since d_G(t)>=5,
t is adjacent to all five vertices of C, including p and ell.

The edge tp forces a=4 by the original apex geometry, contradicting the
already proved p=5=>a>=5. Equivalently, the forced edge t-ell contradicts
the prior ABABCBC full-fibre nonedge. This proves r-ell is absent.

This is a new explicit geometric consequence of existing theorems, not
an independent claim that the full p=5 branch has been excluded. Indeed
the same hypothetical C would give t=5,a=4 and already contradict the
older a=4=>t>=6 theorem.

## 3. A legal three-vertex identification across the two actual faces

Draw an arc z-r in the open face Q and an arc z-ell in the open face P.
Their interiors are disjoint. The arcs share only their endpoint z and
form an embedded tree. Contract this tree and suppress parallel edges.
The only nontrivial equivalence class is exactly `{z,r,ell}`.

All three possible edges within that class are absent: zr from the
induced Q, zell from the induced p link, and rell from Section 2. Thus
the quotient J is loopless and planar. This is not a claim that r and
ell alone were originally cofacial; the two arcs lie in their separately
specified actual faces and share the retained vertex z. No other edge
is removed. An edge survives, for example the image of zs.

The quotient has k-2 vertices. Add a four-edge path with three new
vertices alongside a surviving edge in one face, retaining that edge as
the fifth side of a simple C5. Designate the thin empty side as exterior.
This legal disk has `(k-2)+3-5=k-4<k` inner vertices. The original global
minimality puts its complete relation in the nonempty K132 catalogue.
A complete colouring restricts to J and pulls back to a complete
colouring f of this **one literal D** satisfying

`f(z)=f(r)=f(ell)`.

This proves existence on a particular strictly smaller planar quotient,
not colourability of arbitrary planar graphs or equality of fibres with
a catalogue representative.

## 4. The new forced full fibre

Consider any complete D colouring with z=r=ell. The p neighbours
`z,q,ell,m` have at most three colours, so at least one p lift exists.
Every legal p lift is a complete R colouring. Since z=r, Q is either
ABAB or ABAC; the latter is forbidden. Hence s=t. Normalize the one
common frame as

`z=r=ell=A`, `s=t=B`.

For **every** legal p lift, the ABAB full-fibre condition says pq uses
the complementary colours C,D. In particular q is neither A nor B;
call q=C. Every legal p colour must then be D.

If m were not B, colour B would be legal at p, since its other three
neighbours have colours A,C,A. This contradicts the preceding universal
condition. Therefore m=B. Conversely with these pin colours p is
uniquely D, and the two legal xy lifts are precisely CD and DC.

We have proved the new nonempty **complete-colouring** fibre

`(z,s,r,t,q,ell,m)=ABABCAB`.

Every colouring in this fibre has the stated full cap lifts. Because
every original edge between retained vertices remains, its existence
forbids both original edges m-s and m-t. The m-s conclusion is already
available from original geometry; m-t is the useful new restriction.

The preceding audit separately proved a nonempty fibre **ABABCBC** on
the same ordered pins of this same D. These are two separately existing
complete colourings, obtained from different quotients. We do not
combine their assignments into one colouring, assert equal multiplicity,
or assert a Kempe path between them.

## 5. Exclusion of a=5, and the reflected source

The original p link supplies the face a-p-m. The original ya apex is t,
and p=5 has already forced a>=5 and m!=t. If a=5, its complete neighbour
list is exactly `(y,t,m,p,b)` in cyclic order. Thus t-m is an original
edge (and a-t-m is a face). This contradicts Section 4.

Therefore p=5 forces **a>=6**, at every size and for each of 932,933,941.
No singleton rotation or additional r-degree premise is used.

Reflect the whole original disk by `(x,y),(a,c),(p,q),(s,t)`. If the
q link is `(c,b,p,ell,n)`, the reflected theorem gives q=5=>c>=6, and
forbids n-s and n-t. All identifications, colour names, and lifts are
transported together.

For p=q=5 the earlier ell>=6 remains; the new conclusion is now
`a,c,ell>=6` and therefore `h=d_G(a)+d_G(c)-8>=4`.
The double-low branch with these stronger bounds remains OPEN. For
p=5,q>=6, only a>=6 has been proved. In particular no lower bound on c
beyond the existing source bounds is inferred from this asymmetric case.

## 6. Replay and scope

[check.py](check.py) reconstructs all 4^7 labelled assignments of the two
literal faces. For each proper pin row it independently computes all
legal ordered `(p,x,y)` cap lifts by direct original-edge tests and by
the product of the p and xy tables. Every canonical row, every complete
lift, every successful target lift, and empty cells are retained in
[certificate-final.json](certificate-final.json). The z=r=ell slice
among locally all-failing rows is exactly ABABCAB; the earlier z=r and
q=m slice is exactly ABABCBC. Adding m-t eliminates the new slice.

Normal and seed17 replay logs are [check-final.log](check-final.log) and
[check-seed17.log](check-seed17.log). The negative control removes one
actual ABABCAB cap lift and must be rejected; its receipt is retained in
[check-negative.log](check-negative.log). [receipts.json](receipts.json)
records commands, exit codes and hashes. The checker verifies every
authority entry on every run: immutable audit paths directly, and routing
documents at their manifest-specified frozen paths. Certificate generation
is exclusive-create. The first generation failed before creating a
certificate because it assumed every immutable input had a duplicate
frozen copy; [generate.log](generate.log) retains this path-handling error.
The repair follows the actual manifest's explicit frozen_path field and
does not change any mathematical row.

These finite checks establish only the fixed local arithmetic. The
source nonedge, two-face planarity, minimum-source existence, degree
implication, and arbitrary-size exclusion are Sections 1-5. There are
no supplied genuine target sources to realize the residual, and no new
external enumeration or Lean theorem. The full low-p branch and its
reflection remain OPEN. The narrower a=5,m=5 and a=5,t=5 explorations
are retained as superseded work in [EXPLORATION.md](EXPLORATION.md).
