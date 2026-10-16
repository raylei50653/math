# Independent review: cofacial fibres and a low-p source exclusion

BASE: `676b1024715f24a0d969fba90baab21b756406e2`.
This review reads the frozen source contracts and uses no Four Colour
Theorem, external enumeration, or Lean theorem. Its mathematical conclusions
are an arbitrary-size conditional exclusion of one complete source subbranch
and a forced same-source complete fibre for the surviving p=5 branch.

## Reviewed input and cap admissibility

The authoritative inputs are the previous
[source geometry](../../2026-10-14-c4-mask13-joint6-fdd3e22/SOURCE_GEOMETRY.md),
[adjacent-four reduction](../../2026-10-14-c4-triangle-core-b66f592/ADJACENT4.md),
[single-p deletion](../../2026-10-14-c4-return-branches-a11d4bb/pq/PROOF.md),
and [higher-r quotient construction](../../2026-10-14-c4-return-branches-a11d4bb/r_high/PROOF.md).

The three-new-vertex cap is admissible for a simple planar quotient even
if it has cutvertices. The original cell class in
[the enumerator specification](../../../docs/c5_cell_enumerator.md) §0.1
places no triangulation or connectivity restriction on interior edges.
The [no4ct source contract](../../2026-10-13-c5-no4ct-frontier-6943561/w5/PROOF.md)
explicitly allows chords and disconnected graphs in the initial class;
2-connectivity and triangulation are derived properties of the selected
minimum source. They are not eligibility conditions on a smaller disk.

Given an edge uv of a simple planar graph J with n vertices, draw a new
length-four uv path through three new vertices in a thin strip of an
incident face. Its union with uv bounds an empty C5 face. Choose this face
as exterior on the sphere. All of J lies in the closed complementary disk,
and the result has n+3 total vertices and n-2 interiors. Therefore, if
n-2<k, original source minimality and the nonempty K132 catalogue supply
a complete J colouring. This conclusion is source-relative, not a general
colourability theorem for planar graphs.

## New complete subbranch exclusion

Under the fixed original `d_G(x)=d_G(y)=d_G(b)=4` source contract,

`d_G(p)=5 => d_G(a)>=5`,

and by the established reflection,

`d_G(q)=5 => d_G(c)>=5`.

Equivalently, `a=4 => p>=6` and `c=4 => q>=6`, using the existing original
inner degree lower bound five. This does not prove p,q>=6 generally.

### Literal geometry

Assume p=5 and a=4. The p-link in T0 is `(z,q,ell,m)`. Source geometry
gives `tp iff a=4`, hence tp exists. The vertex t is not z or q, and it
cannot be ell because ell is adjacent to q while tq is a forbidden
original apex edge. Thus m=t. The vertices z,s,r,t,q,ell are distinct.

Let `D=T0-{x,y,p}=R-p`. It has k vertices. The original exterior face of
R has cycle `Q=(z,s,r,t)`; deleting p exposes a second face
`P=(z,q,ell,t)`. Their common edge is zt. These are two distinct faces,
with disjoint interiors. All undeleted original edges are retained.

Add a zr arc inside Q and a qt arc inside P. Their endpoints are distinct,
and their interiors are disjoint. Contract both arcs and suppress parallel
edges. The identification blocks are exactly `{z,r}` and `{q,t}`.
Both original pairs are nonedges: zr by inducedness of Q and qt by the
source apex theorem (also by inducedness of P). Thus the quotient J is
loopless, simple and planar. It has k-2 vertices and retains the edge
between the two blocks coming from zt. The cap above has k+1 vertices,
five boundary vertices and k-4<k interiors. It is source-colourable.

Pulling one such colouring back to D gives a single complete colouring f
with `f(z)=f(r)` and `f(q)=f(t)`. These are simultaneous constraints in
one legal quotient, not two existential witnesses combined afterwards.

### Same-colouring contradiction

Restore p. Its neighbour colours are those of z,q,ell,t; since q=t,
they use at most three colours. At least one p colour is available, so
this gives a complete colouring of the actual R, with unchanged colours
at z,s,r,t,q.

Since z=r, its Q word is ABAB or ABAC. The exact R relation is mask13,
so ABAC is absent and the word must be ABAB. Consequently s=t=q.
The universal ABAB full-fibre condition says that pq uses the two colours
absent from the Q boundary. But q has the boundary colour at s=t. This is
a contradiction. No property of an abstract mask14 representative is used.

### Independent finite verification

[check_alias_local.py](check_alias_local.py) enumerates all labelled pin
assignments on `(z,s,r,t,ell,q)` that satisfy the original seven D edges,
z=r and q=t. It then directly tests every x,y,p assignment against the
eleven original restoration edges, without importing the R/H tables.

[alias-local.json](alias-local.json) records all 108 proper pin assignments,
all 384 complete local restoration lifts, and all 288 lifts with
`{x,y}!={p,q}`. Every one of the 108 pin assignments has at least one target
lift. This verifies the local obstruction independently. Quotient topology,
source minimality, and the implication m=t remain the paper arguments above.

Replay:

```sh
python3 -B audits/2026-10-14-cofacial-fibres-676b102/review/check_alias_local.py
```

## Failed shortcut and remaining scope

When m differs from t, deleting x,y,p creates two different C4 faces
sharing only z. Their union is not one face. An initial exploratory idea
to identify r=q across this union is not justified and is rejected.
Neither an eight-term facial walk nor a simple C4 may replace these two
actual face boundaries.

One may still simultaneously identify z=r in Q and q=m in P. This supplies
a single D colouring with those equalities. Restoring p then forces
s=t and makes pq complementary to z,s, so q=m is distinct from s=t.
There is a useful additional forced equality. Apply one global colour
renaming to write `z=r=A`, `s=t=B`, `q=m=C`. Every legal p colour must be D.
The vertex ell is not C because qell is an edge. It cannot be A, because
then p=B is also a legal lift and violates the same R ABAB condition. It
cannot be D, because p then cannot use D. Consequently `ell=B`.

Thus every p=5 source has a complete D colouring with literal pin word

`(z,s,r,t,q,ell,m) = (A,B,A,B,C,B,C)`.

More precisely, **every** complete D colouring satisfying z=r and q=m
has this word up to one global S4 renaming, and the double quotient proves
that this joint fibre is nonempty. The proof retains one original graph
and all its edges; it is not a construction of a representative graph.
It gives the new source nonedge consequences

`s-ell not in E(T0)` and `t-ell not in E(T0)`.

Either edge would join equal colours in this forced complete fibre. The
same fibre also excludes m=t directly; hence it subsumes the degree
subbranch argument above. The three colour classes are distinct, and
z,r,q,m,s,t,ell remain their actual named vertices.

[check_double_quotient.py](check_double_quotient.py) independently checks
all 324 labelled proper D pin assignments with z=r and q=m, and all 1,152
complete x,y,p restoration lifts using only original edges. Exactly 24
assignments satisfy universal target failure: the complete S4 orbit of
ABABCBC. [double-quotient.json](double-quotient.json) retains every row and
lift, including every rejected row. The alias test remains a separate
direct-edge check of the 108-row m=t domain.

This exact fibre is consistent as a local table when m differs from t.
It does not exclude the remaining general p=5 source.

The [exploratory C6 screen](explore_alias.py) and
[its complete output](alias-screen.json) are retained separately. They
delete zt in the alias case, enumerate 31 canonical C6 rows and all 15
noncrossing loopless boundary partitions, and find one zero-survivor
partition, exactly z=r and t=q. They retain all six rows with z=t, which
do not restore zt. This screen suggested the valid two-face construction;
it is not the theorem's authority or an assertion of any source realization.

The original H identifications z=ell and q=m only reproduce the two
previously proved nonempty diagonal fibres. They alone give no general
mask14 exclusion. The full p=5 branch with a>=5 remains OPEN, as does its
reflected q=5 branch with c>=5. No general K<=22 improvement is claimed.
