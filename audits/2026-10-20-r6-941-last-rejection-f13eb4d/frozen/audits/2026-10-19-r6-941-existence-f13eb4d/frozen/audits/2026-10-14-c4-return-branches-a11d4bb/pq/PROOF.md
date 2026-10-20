# Original p/q degree-five branches: exact mask14 and a double-low bound

Frozen BASE `a11d4bb`. This is an arbitrary-size paper calculation on the
same globally minimum no4ct source, original graph and colour frame. It
does not exclude either original degree-five branch. It proves a smaller
exact full-fibre residual and an additional bound when both branches occur.

## 1. Literal hypotheses and names

Use [SOURCE_GEOMETRY](../../2026-10-14-c4-mask13-joint6-fdd3e22/SOURCE_GEOMETRY.md),
[ADJACENT4](../../2026-10-14-c4-triangle-core-b66f592/ADJACENT4.md),
and [JOINT_FIBRES](../../2026-10-14-c4-mask13-joint6-fdd3e22/JOINT_FIBRES.md)
at the frozen BASE. The source has `B=(x,y,a,b,c)`, original inner count k,
and `d_G(x)=d_G(y)=d_G(b)=4`. The actual simple sphere triangulation T0 has
`k+3` vertices, no nonfacial triangles, and designated facial triangles
`zxy` and `zpq`. Vertices p,q are adjacent to neither x nor y. Original
target failure is the universal same-colouring statement

`{f(x),f(y)}={f(p),f(q)}` for every complete proper T0 colouring f.

This is a comparison inside one complete colouring. No independent face
colourings or separately normalized tuples are used below. The triangle
`zxy` is retained literally throughout; it is never replaced by a boundary
representative.

## 2. Delete one original degree-five vertex

Suppose `d_G(p)=5`. Its actual T0 degree is four. Name its facial neighbour
cycle, in one of its two orientations,

`N_T0(p)=(z,q,ell,m)`.

These four vertices are distinct. The two opposite pairs have no edges:
a diagonal in this link would give a nonfacial triangle in T0, with p on
one side and another link vertex on the other. Delete p and designate
the resulting quadrangular face as exterior. This gives the induced C4
disk H with literal outer boundary `(z,q,ell,m)`. It has `k+2` vertices,
`k-2<k` interiors, and the unchanged facial triangle zxy strictly inside
apart from its boundary vertex z. Neither x nor y becomes a boundary pin.

For every complete H colouring, restore p with **each** colour absent
from its four neighbours. The exact local table is

| H outer word | All p colours | Universal requirement on unchanged xy |
| --- | --- | --- |
| ABAB | C,D | simultaneously BC and BD; impossible |
| ABAC | D | BD |
| ABCB | D | BD |
| ABCD | none | no p-lift condition |

For example, the first row has two distinct complete T0 lifts with exactly
the same colours at x,y,q. Target failure requires the same fixed xy palette
to equal both `{B,C}` and `{B,D}`. Thus the entire H ABAB fibre is empty.
The two diagonal rows each force xy=BD on every complete lift separately.

The source-relative C4 theorem applies to H, so its support is initially
in `{10,12,14}` in bit order ABAB,ABAC,ABCB,ABCD. In particular its rainbow
fibre is nonempty. The no-rainbow hypothesis of the original return lemma
has failed at this precise step.

## 3. Both diagonal fibres are nonempty: H has exactly mask14

Identify z and ell along the exterior of H and suppress parallel edges.
They are nonadjacent, so this gives a loopless planar graph with `k+1`
vertices. To obtain its colourability from original source minimality,
choose an edge and add an exterior path of length four between its endpoints,
retaining the edge as the fifth side of an outer C5. The resulting disk has
`k+4` vertices and `k-1<k` interiors. Its catalogue relation is nonempty,
so its restriction colours the quotient. Lift this colouring to H. It has
z=ell and therefore is ABAB or ABAC after one common colour renaming.
ABAB is impossible, so H has a nonempty ABAC fibre.

Perform the same legal exterior identification of q,m. Its lifted colouring
is ABAB or ABCB; hence ABCB is nonempty as well. Both operations retain all
original graph edges modulo their explicitly named identifications. They
provide existence and do not identify their colouring fibres with each other.

Consequently

`d_G(p)=5 ==> support(H)=14={ABAC,ABCB,ABCD}`.

This uses only colourability of two strictly smaller, explicitly constructed
graphs under the frozen minimum-source contract. It is not a claim that
arbitrary planar graphs are colourable.

## 4. Exact complete-fibre split of the rainbow row

Write F(W) for all complete H colourings with the literal word W in the
common frame `(A,B,C,D)`. All maximal components below are in this same H.
The mandatory edges are the actual boundary cycle and triangle zxy.

In every `f in F(ABAC)`, q,m belong to one BC component: switching m's
component otherwise gives the forbidden ABAB boundary. Therefore z,ell
are disconnected in the complementary AD subgraph, by Jordan separation.
The D-coloured endpoint of xy is adjacent to z and lies in z's AD component;
the B-coloured endpoint is outside AD. Switch ell's AD component and then
apply the single global permutation `C<->D` to every vertex. The resulting
word is ABCD and the xy palette is BC.

In every `f in F(ABCB)`, z,ell are connected in AC, since an ell-component
switch would otherwise give ABAB. Thus q,m are disconnected in BD. Switch
m's BD component. The resulting word is ABCD. The edge xy puts both its
endpoints in one BD component, so its unordered palette remains BD. Its
order reverses exactly if that component is m's component.

For completeness the rainbow fibre cannot use xy=CD. Suppose it did.
If z,ell were disconnected in AC, switching ell would give ABAD while
fixing xy: its C endpoint is adjacent to z and its D endpoint is outside AC.
But the ABAD diagonal requires xy=BC, a contradiction. Hence z,ell are
connected in AC. If q,m were disconnected in BD, switching m would give
ABCB; the C endpoint of xy would remain C, contradicting that row's forced
BD palette. Thus q,m are connected in BD too. These two vertex-disjoint
complementary paths have alternating endpoints on the original C4 boundary,
which is impossible.

Let `U={g in F(ABCD): xy=BC}` and `V={g in F(ABCD): xy=BD}`.
In U, z,ell must be disconnected in AC: otherwise Jordan separation
disconnects q,m in BD, and the m switch gives ABCB still containing C at xy.
Conversely switching ell's AC component gives ABAD with xy=BC, and one
global `C<->D` renaming gives ABAC with xy=BD. This is the exact inverse of
the first construction, because a maximal component keeps its vertex set
after its own switch and the colour permutation is applied globally.

In V, z,ell must be connected in AC: an ell switch otherwise gives ABAD
while retaining xy=BD, contrary to that row's BC requirement. Thus q,m are
disconnected in BD. Switching m back gives ABCB with the same unordered xy
palette, the exact inverse of the second construction.

We have the full-colouring bijections and disjoint split

`F(ABAC) <--> U`, `F(ABCB) <--> V`, `F(ABCD)=U disjoint-union V`.

All four sets are nonempty. Both maps act on every vertex of a complete
colouring and preserve actual edges; the first includes the stated global
colour permutation and the second can reverse the ordered xy colours.
In particular `|F(ABCD)|=|F(ABAC)|+|F(ABCB)|`, but the exact maps contain
more information than this finite count identity.

Conversely, mask14 with the two universal diagonal palette conditions is
the exact single-p-deletion target-failure residual: the table in §2 lists
every possible p lift, and none of the rainbow colourings lifts. The new
rainbow split is a consequence of that exact residual, not an extra source
realization assumption. It does not contradict the residual.

The whole statement applies to q by taking its literal degree-four link
`(z,p,ell,n)`. This is a role exchange in the same T0 target comparison;
it does not rotate the original singleton fibre hypotheses.

## 5. If p=q=5, their other shared neighbour has original degree at least six

Assume both original degrees are five. The two actual pq faces are zpq
and `p-q-ell`. The links are `(z,q,ell,m)` and `(z,p,ell,n)`. The four
vertices z,m,ell,n are distinct; if m=n then pq would lie in the third
triangle pqm as well as its two facial triangles, contradicting the absence
of nonfacial triangles. Delete p,q. Their combined facial fan exposes the
simple C4 `(z,m,ell,n)` of a disk K with `k+1` vertices. The diagonal z-ell
is absent by the p-link argument. A putative diagonal m-n would divide K
into two triangles, one strictly containing x or y, contrary to T0's
triangle faciality. Both x and y remain strictly interior since they were
adjacent to neither deleted vertex. Thus this is an induced smaller disk.

Restore p,q with their exact original cap edges. The full local cap table is

| K outer word | All ordered (p,q) lifts | Required unchanged xy palette |
| --- | --- | --- |
| ABAB | CD,DC | CD |
| ABAC | CB,CD,DB | three distinct palettes; impossible |
| ABCB | none | none directly |
| ABCD | DB | BD |

This is the literal original two-vertex cap with the roles `(x,y)` and
`(p,q)` exchanged. The relative C4 list leaves masks12/13; the exterior
z=ell identification has k vertices and is source-colourable via a C5 cap
with k-2 interiors, so ABAB is nonempty. Hence K is exactly mask13 with
universal xy=CD in ABAB and xy=BD in ABCD. The actual-component
JOINT_FIBRES argument applies unchanged with edge xy: every ABCB complete
colouring contains the missing colour on xy.

The vertex ell is an original inner vertex distinct from every B vertex.
It is neither p nor q, so the original b is not its neighbour; the added
u contacts only B. Identifying a,c creates no duplicate ell edge, by the
original adjacent-boundary-contact restriction. Hence its T0 degree is
exactly its original G degree, and deleting p,q loses exactly those
two edges. Thus `d_K(ell)=d_G(ell)-2`. It is also adjacent to neither x nor
y: the original degree-four x,y neighbour lists contain only B vertices
and r,s,t, and ell is none of those, since their forbidden p/q edges rule
them out. Consequently deleting ell never exposes x or y as a boundary pin.

Suppose `d_G(ell)=5`, so its K degree is three, with actual neighbours m,w,n.
Delete ell to obtain the disk L with outer `(z,m,w,n)`. Its vertices are
distinct, z-w is absent (otherwise one of triangles zmw,zwn strictly
contains x or y in T0), and x,y remain inside with their edge and facial
triangle at z. All ell lifts and the same-colouring K joint constraints give

| L outer word | All ell colours | xy palette in every complete colouring |
| --- | --- | --- |
| ABAB | C,D | CD |
| ABAC | D | BC |
| ABCB | A,D | CD |
| ABCD | A | forbidden K ABAC lift |

The ABAB row uses the compulsory missing colour in both ABCB lifts: the
same unchanged xy must contain D in the ell=C lift and C in the ell=D lift.
The rainbow row of K supplies a complete L ABAC colouring after the common
`C<->D` renaming: w is forced to A by its three neighbours m=B,ell=C,n=D.
Thus L has no rainbow and has a nonempty ABAC fibre with xy=BC.

Apply [the original return lemma](../../2026-10-14-c4-c5-recursion-fdd3e22/fibre/PROOF.md)
to the actual disk L and actual edge xy. It injects that nonempty ABAC/BC
fibre into ABAB/BC; the displayed ABAB row makes the latter empty. This is
an arbitrary-size contradiction. The original inner lower bound was five,
so

`d_G(p)=d_G(q)=5 ==> d_G(ell)>=6`.

This excludes the three simultaneous original degrees `p=q=ell=5`.
It does not exclude the double-low branch when ell is at least six.

## 6. Replay, countercontrols, and surviving obligation

Run `python3 -B audits/2026-10-14-c4-return-branches-a11d4bb/pq/check.py --check`.
[certificate-final.json](certificate-final.json) records exhaustive local assignments
for the single deletion, double deletion, and last degree-three restoration.
Each test includes every legal local lift, both xy orders, and empty cells.
Geometry, source minimality, and the Kempe/Jordan proof are the paper
arguments above, not consequences of this finite replay.

One explicitly named seven-vertex induced triangulated C4 disk has mask14.
The certificate lists its original edges, eight inner triangular faces,
and **all** complete fixed-frame fibres, including the empty ABAB fibre.
Its displayed oriented faces have Euler characteristic two, exactly one
copy of each directed edge, and a single cyclic neighbour link at every
vertex. These checks validate the stated sphere embedding with its named
outer face, beyond edge-incidence counts alone.
Its diagonal xy palette condition fails and a literal ABAC witness is saved.
Thus mask14 by itself does not retain the target-failure joint condition.
This disk is a non-source countercontrol, not a source realization.

A separately labelled S4-closed abstract six-pin relation retains both
required diagonal palettes, the two rainbow sectors, their positive fibre
counts, and their count identity. It illustrates why these retained finite
conditions do not themselves contradict each other. Its graph realizability
is not asserted, and it is not substituted for the actual H fibres.

The first `--check` log failed because Python tuple/list representation
was compared directly to its JSON encoding; the comparison now normalizes
through JSON. [check-first.log](check-first.log) is retained alongside
[generate.log](generate.log) and the PASS [check-final.log](check-final.log).
No mathematical row or generated certificate was changed by that repair.
The later final certificate adds the explicit embedding validation; the
original [certificate.json](certificate.json) is retained as historical
evidence. [receipts.json](receipts.json) records default and seed17 PASS,
plus an expected rejection of [tampered-negative.json](tampered-negative.json)
whose ABAB restoration table omits one required p lift. The checker accepts
an explicit `--certificate PATH` for this independent corruption control.

The surviving obligation is to exclude an actual induced C4 disk H from
the fixed source with exact mask14, its original internal face zxy, universal
xy=BD on both diagonal fibres, the displayed rainbow full-fibre split, and
the original degree/attachment/small-cycle restrictions. Alternatively a
source-preserving operation must yield a complete target T0 colouring.
The no-rainbow return hypothesis is absent, so the old lemma alone supplies
no exclusion of p=5 or q=5. General joint closure, source realizability,
unbounded catalogue equality, and Lean remain OPEN.
