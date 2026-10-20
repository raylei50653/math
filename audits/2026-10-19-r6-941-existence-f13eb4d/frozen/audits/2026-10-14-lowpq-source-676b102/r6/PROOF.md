# Degree-six r: original collar edges excluded; mask319 remains OPEN

This is a paper source-geometry argument at frozen BASE
`676b1024715f24a0d969fba90baab21b756406e2`, with the prior cofacial overlay
sealed by [the parent inputs](../INPUTS.json). It writes only this new
`r6/` audit. The claim is an arbitrary-size conditional source exclusion,
not a finite-source enumeration or a new Kempe-count constraint.

Within the original globally minimum noncatalogue C5 source, with
`d_G(x)=d_G(y)=d_G(b)=4`, assume `d_G(r)=6`. In the original r fan

`N_G(r)=(x,y,t,w,v,s)`,

all edges from an original inner neighbour of a other than t to either
v or w are absent. The reflected statement holds for an original inner
neighbour of c other than s. In particular, if p has original degree five
and its original link is `(a,b,q,ell,m)`, then

`mv,mw not in E(G)`.

These are excluded original-edge subbranches. They do not exclude
`r=6,p=5`, `r=6,q=5`, or mask319.

## 1. Exact source facts used

The [original source geometry](../../2026-10-14-c4-mask13-joint6-fdd3e22/SOURCE_GEOMETRY.md)
fixes the original boundary `(x,y,a,b,c)` and the five original apexes
`(r,t,p,q,s)`. The identification a=c=z and deletion of x,y,b gives the
literal R with boundary `(z,s,r,t)` and `k+1` vertices. Its complete C4
support is mask13, with the original facial triangle zpq retained.
All degrees in this report are degrees in G.

The [degree-six transfer](../../2026-10-14-c4-c5-recursion-fdd3e22/degree4/R6_TRANSFER.md)
proves:

- The original r fan is exactly `(x,y,t,w,v,s)`.
- `U=R-r` has induced boundary `(z,s,v,w,t)`, k total vertices, and
  the retained face zpq.
- `d_G(s),d_G(t)>=6`.
- `pv,pw,qv,qw` are original nonedges.

The [cofacial argument](../../2026-10-14-cofacial-fibres-676b102/r6/PROOF.md)
then proves `Sigma(U)=319`. Its two mandatory outer fibres come from
separate source-colourable quotients; they are not one simultaneous
colouring.

The only separator fact needed below is the already adopted
[proper-C5 cap theorem](../../2026-10-13-c5-no4ct-frontier-6943561/w5/PROOF.md),
section 3: every original simple C5 other than B has either no vertex
in its bounded interior or exactly one vertex, which is adjacent to all
five cycle vertices and has complete original degree five. The cap's
bounded side is the side avoiding the exterior of the original disk G.
This fact uses original minimum-source comparison, not 4CT.

The original a-neighbours y,b are boundary vertices. Its inner neighbours
include t,p. An inner neighbour j of a other than t cannot be r,s,v,w:
ra is forbidden, s has exactly its two allowed original boundary contacts
c,x, and av,aw are excluded by the original common-neighbour theorem
`N_R(z) intersect N_R(r)={s,t}`. Thus every cycle below is simple, with
five distinct original vertices.

## 2. The collar-neighbour lemma

Let j be any original inner neighbour of a other than t. We exclude both
jv and jw directly in G.

**First, jv is absent.** Suppose jv were an original edge. The original
cycle

`C_v=(r,y,a,j,v)`

is simple and proper. It contains the original boundary edge ya, so its
bounded side is fixed: near y it is the sector between ya and yr that
contains t. The actual r fan supplies the edge tw. Neither t nor w
is a cycle vertex, and tw cannot cross C_v; consequently w lies on the
same bounded side as t. Equivalently, the bounded r-sector is the one
from y to v through t,w in `(x,y,t,w,v,s)`. Thus both distinct vertices
t,w are strictly inside C_v. This contradicts the proper-C5 cap theorem,
which permits at most one bounded-interior vertex.

**Second, jw is absent.** Suppose jw were an original edge. The original
simple proper cycle

`C_w=(r,y,a,j,w)`

again has the side fixed by its boundary edge ya. Its bounded r-sector
runs from y to w through t. Hence t is strictly inside C_w. The same
cap theorem forces t to be its unique interior vertex, adjacent to all
five cycle vertices, with its entire original neighbourhood

`N_G(t)={r,y,a,j,w}`.

In particular `d_G(t)=5`. This contradicts the already proved
`r=6 => d_G(t)>=6`.

All other original edges are retained; no edge is suppressed, no pin is
moved, and neither cycle is manufactured in a colour quotient. Extra
putative chords do not weaken the cap theorem: the occupied proper C5
is forced to be the five-wheel, with precisely the listed centre spokes.

Reflecting the entire original source by

`(x,y),(a,c),(p,q),(s,t),(v,w)`

proves the corresponding statement for every original inner neighbour
of c other than s. For the c-side proof, jw would give two interior
vertices s,v, while jv would force `d_G(s)=5`.

Equivalently, with `I=V(G) minus V(B)`, the new geometric restriction is

`E_G({v,w}, (N_G(a) intersect I) minus {t}) = empty`,

`E_G({v,w}, (N_G(c) intersect I) minus {s}) = empty`.

The exceptions t and s are essential: the mandatory fan edges tw and sv
remain. The theorem says nothing about edges from v,w to vertices that
are not original neighbours of a or c.

## 3. What is new, and the low-p/q specialization

Taking j=p on the a side and j=q on the c side recovers the four old
nonedges `pv,pw,qv,qw`. Those four conclusions are historical input,
not new results of this audit. The new statement covers every additional
original a/c neighbour as well.

If `d_G(p)=5`, its original link is `(a,b,q,ell,m)` and therefore am is
an original edge. The [prior common-fibre theorem](../../2026-10-14-cofacial-fibres-676b102/pq/PROOF.md)
excludes a=4 and its literal alias m=t. Thus m is an original inner
neighbour of a different from t, so the lemma gives the genuinely new
specified-edge exclusions

`r=6,p=5 => mv,mw not in E(G)`.

Under reflection, write the original q link as `(c,b,p,ell,n)`; then

`r=6,q=5 => nv,nw not in E(G)`.

The new [low-p companion proof](../pq/PROOF.md) further excludes the
entire a=5 branch, and hence gives `p=5 => a>=6`; its reflection gives
`q=5 => c>=6`. This stronger degree conclusion is adopted from that
separate proof, not derived from the collar-neighbour lemma. It applies
for every r, so it also narrows the current r=6 intersection.

In the remaining r=6,p=5 case, ell and m are distinct from v,w because
p is adjacent to ell,m but not v,w. The literal graph

`W=R-{r,p}`

has the two actual faces `(z,s,v,w,t)` and `(z,q,ell,m)`, sharing only z.
No claim makes ell,v,w cofacial. In particular, this audit has not
excluded ell-v or ell-w, and it does not infer them from the new
nonedges involving m.

## 4. Limited higher-r check and exact stop

The higher-r task was checked only in the connected low-p subdomain.
If p=5,a=5,t=5, the original a fan forces the intermediate t-link pin
to be the same original vertex m appearing in the p link. Deleting p,t
then exposes actual faces `(z,s,r,w,m)` and `(z,q,ell,m)`, sharing the
retained edge zm. A simultaneous identification z=r=ell has no
compatible universal p/t cap lift. This is a valid weaker subbranch
argument, but the companion theorem now excludes all p=5,a=5, regardless
of t. It is therefore recorded only as a contained check and is not
counted as an independent stronger source exclusion. No extra finite
model was generated for it.

The live task-3 intersection with p=5 is consequently

`r>=7,t=5,p=5,a>=6`.

Its direct t-deletion support remains among `956,1012,1020`; no one of
those masks is removed here. For the task-3 branch without p=5, the
existing condition is still `r>=7,t=5,a>=5`: this audit does not exclude
all sources with a=5,t=5. The reflected distinctions are retained.

For task 2, mask319 and both low-degree intersections remain OPEN:

`r=6,p=5,a>=6`, and `r=6,q=5,c>=6`.

The collar theorem excludes original source graphs with the specified
forbidden edges, but a nonempty set of necessary local colour rows is
not a source realization. No actual minimum source was produced. No
common integer count model, terminal closure, or enlarged contact model
was solved. The historical integer witnesses remain unchanged and keep
their old necessary-model meaning.

The remaining missing step is a contradiction on complete colourings of
one surviving original source, using its actual edges, face geometry,
and cross-colour Kempe components. The two cofacial witnesses for mask319
cannot be asserted to coexist: their simultaneous boundary equalities
would select the already forbidden ABCBC row, and the two chords cross
on the actual C5. The separate low-p complete fibres also cannot be
combined into one colouring merely because each exists.

## 5. Evidence and claim boundary

This report is a source-geometry proof. It needs no additional finite
colour-count certificate: the two proper-C5 cycles and their original
rotation determine the contradiction. The [source seal](SOURCE_SEAL.json)
and [custody checker](check_inputs.py) record and verify the exact direct
inputs, including the immutable parent input manifest. The checker only
verifies input custody; it does not claim to certify arbitrary plane
embeddings or the paper argument. Default and seed17 replays, and a
corrupted-seal rejection, are retained under [logs](logs/receipts.json).

The general k>=23 bound, the high-p/q conditional k>=28 bound, the
remaining r=6 and higher-r sources, the unrestricted T/T0 branches, and
`K_infinity=K_{<=5}` retain their previous scopes. No external enumeration,
new Lean theorem, runtime claim, or publication action is part of this
sub-audit.
