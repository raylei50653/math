# Independent conditional degree-three deletion audit

2026-10-14. This records and checks the user's proposed local step. The
stronger `r`-degree-five exclusion reviewed in [KEMPE_REVIEW](KEMPE_REVIEW.md)
eliminates its whole premise; this local lemma remains a valid intermediate
proof, not an additional nonvacuous source family.

## 1. Frozen input and exact claim

Use the working-tree authority frozen by [INPUTS](../INPUTS.json), especially
[SOURCE_GEOMETRY](../frozen/audits/2026-10-14-c4-mask13-joint6-fdd3e22/SOURCE_GEOMETRY.md)
sections 2, 3, 5 and the
[relative C4 lemma](../frozen/audits/2026-10-13-c5-no4ct-degrees-6cafdfb/REPORT.md)
section 3. These are the no4ct globally minimum noncatalogue source premises.
The original C5 frame is `(x,y,a,b,c)`, with original inner count `k`, and
`d_G(x)=d_G(y)=d_G(b)=4`. Assume also `d_G(r)=5`.

The frozen reduction gives an actual triangulated disk `R'` with induced
outer boundary `(z,s,v,t)`, `k` total vertices, and exact support mask 7.
The original vertices `p,q` are internal, with facial triangle `zpq`.
Every complete colouring, in one common frame, obeys

| Boundary of R' | Required unordered pq palette |
| --- | --- |
| ABAB | CD |
| ABAC | BC |
| ABCB | CD |

There are no ABCD colourings. The first row uses the frozen actual-component
Kempe theorem [JOINT_FIBRES](../frozen/audits/2026-10-14-c4-mask13-joint6-fdd3e22/JOINT_FIBRES.md),
not just the cap extension table. We prove conditionally that
`d_G(s),d_G(t)>=6`.

## 2. The deletion is a legal smaller disk, including a pin coincidence

Suppose `d_G(s)=5`. The original lower bound is already `d_G(s)>=5`, so
this is the only case needing exclusion. In passing from G to R', s loses
exactly its edges to x and r; its edge to c becomes the single edge to z.
Consequently `d_R'(s)=3`. Its boundary neighbours are z,v. Write its third
neighbour as w, with its inner facial fan `z-s-w` and `w-s-v`.

The vertices z,w,v,t are distinct: simplicity separates w from z,v, and
the already forbidden edge st rules out w=t. The original forbidden edge
sp rules out w=p. Vertex v has no original boundary contact, so it is
distinct from p,q. **The equality w=q is permitted.** It occurs only if
sq is an edge, hence only if the original c has degree four. Nothing in
this argument assumes otherwise.

Delete s and its three incident edges, without adding or identifying
vertices. Its two inner faces become part of the exterior, exposing the
simple boundary `(z,w,v,t)` of a triangulated disk U. The original p is
still strictly internal because p was internal and was not adjacent to s.
Vertex q can become the boundary vertex w. Thus U has `k-1` total vertices
and `k-5<k` interior vertices.

The new boundary is induced as well. Edge zv is absent by the frozen
geometry. If wt were an edge, it would split U into triangles zwt and
wvt. One of their disk sides would contain the strictly internal p;
the other side contains the deleted exterior vertices x,y. Hence that
triangle would be nonfacial in T0. This contradicts the frozen
4-connectivity of T0: every T0 triangle is facial. No inducedness claim
depends on q remaining internal.

All original U edges and all colours of p and q remain fixed when s is
restored. Every colour absent from `{f(z),f(w),f(v)}` is a legal colour
for s, with no further edge condition. All those extensions must obey
the R' table simultaneously.

## 3. Complete local extension table

Fix the literal U boundary `(z,w,v,t)` in the common colour frame. The
entry in the third column is the requirement on the **same unchanged**
pq palette imposed by that complete s lift.

| U boundary | All s colours | Requirements from the corresponding R' lifts |
| --- | --- | --- |
| ABAB | C,D | s=C requires BC; s=D requires BD |
| ABAC | C,D | s=C requires BD; s=D requires CD |
| ABCB | D | the lift has four distinct boundary colours, forbidden |
| ABCD | D | s=D requires BC |

The first two rows require one fixed two-element palette to equal two
different sets. The third row has a forbidden lift. Hence all three
fibres are empty. Only ABCD can survive, and every such colouring has
`{f(p),f(q)}={f(w),f(v)}`. If w=q, this last condition simply forces
`f(p)=f(v)`; it does not rescue any forbidden row.

It follows that the **complete** C4 support of U is either mask 0 or
mask 8. The source-relative C4 lemma applies because U is a legal disk
with `k-5<k` interior vertices and restricts its support to
`{7,10,11,12,13,14,15}`. Neither 0 nor 8 is permitted. This contradiction
excludes `d_G(s)=5`.

Reflect the original frame by simultaneously interchanging
`(x,y)`, `(a,c)`, `(p,q)`, and `(s,t)`. The R' palette table is invariant
under this reflection, after a common colour renaming where needed.
The identical argument excludes `d_G(t)=5`; on this side the newly
exposed vertex may be p and q stays internal. Therefore

`d_G(r)=5 => d_G(s),d_G(t)>=6`

within the stated original source branch. There is no corresponding
degree-three v case: `d_R'(v)=d_G(v)-1>=4`, since v has no original B
contact and only loses r.

## 4. Executable control and scope

Run `python3 -B audits/2026-10-14-c4-c5-recursion-fdd3e22/degree3/check.py --check`.
The checker compares two independently written predicates on all literal
proper boundary assignments and ordered pq assignments. One implements
the colour-equality rule directly; the other transports the three
canonical rows through all 24 global colour permutations. Both enumerate
**all** legal s colours. It separately checks w=q and the reflected w=p
pin coincidences, and records an existential-lift negative control.

The certificate verifies this finite implication. Disk surgery, original
degree loss, and the invocation of source minimality are paper arguments
in sections 1-3. No source graph is enumerated or asserted realizable;
there is no universal C4 classification, 4CT dependency, Lean theorem,
or global decreasing recurrence in this result.
