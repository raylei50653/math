# Low p: a common-source fibre and an excluded literal contact

Frozen BASE is `676b1024715f24a0d969fba90baab21b756406e2`.
This is an arbitrary-size argument on the original minimum source. It proves

`d_G(p)=5 => d_G(a)>=5`, and by reflection `d_G(q)=5 => d_G(c)>=5`.

It also forces a nonempty **joint complete-colouring fibre** in the common
deletion graph when p has degree five, and therefore forbids both original
edges ell-s and ell-t in this low-p branch. The remaining p=5,a>=5 and
q=5,c>=5 source branches are OPEN. In particular this does not prove
p,q>=6 or extend the general catalogue bound.

## 1. Authority and literal common graph

Use the frozen [source geometry](../frozen/audits/2026-10-14-c4-mask13-joint6-fdd3e22/SOURCE_GEOMETRY.md),
[adjacent-four cap](../frozen/audits/2026-10-14-c4-triangle-core-b66f592/ADJACENT4.md),
and [low-p proof](../frozen/audits/2026-10-14-c4-return-branches-a11d4bb/pq/PROOF.md).
The original globally minimum noncatalogue C5 disk G has inner count k,
boundary `(x,y,a,b,c)`, and `d_G(x)=d_G(y)=d_G(b)=4`.
The actual sphere triangulation T0 has k+3 vertices and the distinct
designated faces zxy and zpq. Neither p nor q is adjacent to x or y.
Failure means, for **every complete T0 colouring f in one colour frame**,

`{f(x),f(y)}={f(p),f(q)}`.

The smaller disk R=T0-{x,y}, with Q=(z,s,r,t), has mask13.
Its ABAC fibre is empty; every ABAB full colouring has pq palette CD.
These two facts alone suffice for the exclusion below.

Suppose d_G(p)=5. The original link of p, in an appropriate orientation,
is `(a,b,q,ell,m)`; its T0 link is `(z,q,ell,m)`. Let

`D=T0-{x,y,p}=R-p=H-{x,y}`.

This is one literal graph with k vertices. Deleting the two-vertex xy cap
exposes the actual C4 face Q=(z,s,r,t); deleting p exposes the actual C4
face P=(z,q,ell,m). We retain every other original edge. These are two
distinct faces, not one manufactured C4 boundary.

The cycles share z. Their only possible additional common vertex is
m=t, and this happens exactly when d_G(a)=4. Indeed pr and ps are
source-forbidden. If pt exists, source geometry gives d_G(a)=4, and
the facial triangle apt is the face of ap opposite apb. Thus t=m in
the displayed actual p link; it cannot be ell. Conversely a=4 gives
the original edge pt and hence m=t. The other named apexes are distinct.
Consequently when m!=t the two faces share only z, and when m=t they
share the **retained edge zt**. Their open facial interiors are disjoint
in both cases. There is no claim that pins from their different interiors
are cofacial.

The original cap edges which restore T0 from D are exactly

`zx,sx,rx,xy,zy,ry,ty,pz,pq,pell,pm`.

For each one complete D colouring, the legal xy assignments and legal p
colours form their Cartesian product, because p has no edge to x or y.
All of these lifts use that same D colouring; no independent witnesses
are combined.

## 2. Two simultaneous facial identifications are source-colourable

The opposite pairs z,r in Q and q,m in P are nonedges. Draw an arc from
z to r in the open Q face and an arc from q to m in the open P face,
then contract both arcs. Their four endpoints are distinct, including in
the m=t case. Their interiors lie in different faces and do not cross.
The equivalence classes are exactly `{z,r}` and `{q,m}`. Since both
classes are independent, no loop results. Suppress any parallel edges.
This produces a loopless planar quotient J with k-2 vertices.

This construction is valid even when the two faces share zt: the edge
zt is retained, and each added arc is confined to its own original
face. We do not delete zt or admit any additional colouring with z=t.

An edge remains, for example the image of zs. Choose a face incident
with an edge, attach a four-edge path with three new vertices alongside
that edge in the face, and designate the empty side of the resulting
simple C5 as exterior. This is the same minimum-source cap construction
already used in the frozen proofs. Its total count is

`(k-2)+3=k+1`, so its inner count is `k+1-5=k-4<k`.

Original minimality puts its complete relation in the nonempty K132
catalogue. A complete colouring restricts to J and pulls back to a
complete D colouring satisfying simultaneously

`f(z)=f(r)` and `f(q)=f(m)`.

This is existence on one specific smaller planar quotient. It is neither
a general planar-colourability assertion nor a fibre identification with
a catalogue representative.

## 3. The exact joint fibre forced by that quotient

Consider **any** complete D colouring satisfying those two equalities.
Because q=m, p's four neighbours use at most three colours, so at least
one p lift exists. Every such lift gives a complete R colouring. Since
z=r, the Q word can only be ABAB or ABAC. The second is forbidden;
therefore s=t. Normalize one common frame so z=r=A and s=t=B.

Every p lift now lies in R's ABAB fibre. Hence for **every** legal p
colour its pq palette is CD. In particular q is neither A nor B; call
q=m=C. The missing colour D must be the only legal p colour. If ell=A
or C, both B and D would be legal at p, contradicting the universal
ABAB palette condition. If ell=D, p=B would be legal and would also
contradict it. Thus ell=B and p=D.

We have proved that every colouring from this quotient lies in the single
joint orbit

`(z,s,r,t,q,ell,m)=(A,B,A,B,C,B,C)`.

When all seven pins are distinct, the quotient argument proves that this
full D fibre is nonempty (and so is every common global colour renaming).
Its p lift is uniquely D. Its two xy lifts are exactly `(C,D)` and `(D,C)`.
Both are full T0 lifts of that same D colouring, with the required equal
palettes. In H they lie in the actual P=ABCB diagonal fibre after the
single global B,C renaming. This is a new shared-source existence
constraint, rather than separate mask13 and mask14 witnesses.

The statement concerns every full colouring in the specified D fibre;
it does not prescribe its multiplicity or assert that the rest of D's
complete relation is known.

Since ell,s,t are distinct original vertices and every original edge
between them is retained in D, the existence of this same-colouring fibre
also gives the arbitrary-size source conclusions

`d_G(p)=5 => ell-s not in E(G) and ell-t not in E(G)`.

Thus either of these two geometrically specified edge subbranches is
excluded. They are actual source nonedge conclusions, not a claim that
one can identify those vertices in a later face. In the alias m=t case,
the mandatory link edge ell-m would already contradict ell and t having
the same colour.

## 4. Exclusion of p=5,a=4

If additionally d_G(a)=4, Section 1 gives the literal equality m=t.
But Section 3 forces m=C and t=B in the same complete colouring, with
B and C distinct. This contradicts Section 2's existence theorem.

Equivalently, directly in the alias graph identify z=r and q=t across
the two genuine faces `(z,s,r,t)` and `(z,q,ell,t)`. A p lift always
exists, since q=t. The forbidden R ABAC row forces s=t=q, whereas the
R ABAB requirement says pq avoids the colour of s. This is impossible.

Thus `d_G(p)=5 and d_G(a)=4` is excluded for every size in this source.
The original outer minimum degree is four, so p=5 forces a>=5.
The literal reflection `(x,y),(a,c),(p,q),(s,t)` gives q=5 forces c>=5.
The argument needs no high-r hypothesis and no new finite catalogue.
It does not use a hypothetical crossing identification on one C4.

## 5. Focused replay and remaining work

[check.py](check.py) independently enumerates the 4^7 labelled assignments on the
two literal four-cycle faces, with all 4^3 x,y,p restoration assignments.
Its certificate retains every canonical proper seven-pin row, every legal
full cap lift, and every target-failure-violating lift, including empty
cells. It compares a direct original-edge test with independent product
tables for the xy and p caps. The simultaneous-quotient slice has exactly
the one common orbit ABABCBC among rows for which every cap lift fails
the target. The literal alias m=t slice has no such surviving row.

The [final certificate](certificate-final.json) binds the checker and
frozen authority manifest; each replay verifies every frozen input hash.
Run from the repository root:

```sh
python3 -B audits/2026-10-14-cofacial-fibres-676b102/pq/check.py --check
```

[Default](check-final.log) and [seed17](check-seed17.log) replays PASS.
The [negative control](tampered-negative.json) omits one legal full lift
from ABABCBC and is [rejected](check-negative.log) as expected.
[Receipts](receipts.json) retain commands, exit codes, and artifact hashes.
The initial valid [certificate](certificate-initial.json),
[checker](check_initial.py), and [generation log](generate.log) remain
historical evidence; the final version additionally binds frozen inputs
and checks the ell-s/ell-t edge exclusions. New generation requires the
explicit `--write` option and an unused output path. These finite checks
verify local full-lift arithmetic; facial planarity, the original contact
identity, and minimum-source colourability are the arbitrary-size proof
above. The [separate review checker](../review/check_alias_local.py)
reconstructs the alias cap directly.

The new source exclusion leaves p=5,a>=5 and its reflection OPEN.
The additional ell-s and ell-t nonedges must be retained in those residuals.
The generic joint orbit is consistent locally and is not a source
realization. No full mask14 exclusion, p,q>=6 theorem, general bound
improvement, external enumeration, or new Lean theorem is claimed.
