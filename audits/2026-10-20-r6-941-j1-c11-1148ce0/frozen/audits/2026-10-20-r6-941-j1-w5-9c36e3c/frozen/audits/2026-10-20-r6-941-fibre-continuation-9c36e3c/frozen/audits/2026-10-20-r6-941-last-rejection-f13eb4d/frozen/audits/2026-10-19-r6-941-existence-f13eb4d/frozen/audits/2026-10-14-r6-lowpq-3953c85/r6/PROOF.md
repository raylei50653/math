# The r=6, p=5 intersection forces two new original nonedges

Frozen BASE: `3953c85e334b96533e44652df065640f5463715a`.
All degree statements refer to the original C5 disk G. This argument uses
source minimality and two actual faces of one graph; it holds for arbitrary
source size and does not use a finite source enumeration or 4CT.

Under the fixed minimum-source contract, with
`d_G(x)=d_G(y)=d_G(b)=4`, assume `d_G(r)=6` and `d_G(p)=5`.
Write the original links as

`N_G(r)=(x,y,t,w,v,s)`, `N_G(p)=(a,b,q,ell,m)`.

Then the new conclusion is

**`ell-v, ell-w are not original edges of G`.**

The same argument produces two separately nonempty, explicitly specified
unions of complete-colouring fibres on the literal graph
`W=R-{r,p}`. Neither union is declared to have both constituent fibres
nonempty. The entire `r=6,p=5,a>=6` source branch remains OPEN.

## 1. Fixed source, retained edges, and inherited constraints

The [original geometry](../../2026-10-14-c4-mask13-joint6-fdd3e22/SOURCE_GEOMETRY.md)
uses the original boundary `(x,y,a,b,c)` and its five apexes `r,t,p,q,s`.
After identifying a,c to z and deleting x,y,b, the graph R has k+1 total
vertices and actual outer C4 `(z,s,r,t)`, with complete support mask13.
Every remaining original edge is retained. The original face zpq remains.

The [degree-six transfer](../../2026-10-14-c4-c5-recursion-fdd3e22/degree4/R6_TRANSFER.md)
and [complete-support theorem](../../2026-10-14-cofacial-fibres-676b102/r6/PROOF.md)
give `U=R-r`, its induced actual outer C5 `(z,s,v,w,t)`, and
`Sigma(U)=319`. In particular its only possible complete boundary row
with s=w is ABABC; its only possible complete row with v=t is ABCAC.
All statements are in a common colour frame.

The [low-p proof](../../2026-10-14-lowpq-source-676b102/pq/PROOF.md)
gives `a>=6`, hence m is distinct from t. Its full ABABCAB fibre excludes
ms,mt, and its earlier companion excludes ell-s,ell-t. The
[collar proof](../../2026-10-14-lowpq-source-676b102/r6/PROOF.md)
gives mv,mw. The four nonedges pv,pw,qv,qw and the induced p link imply
that ell,m are distinct from v,w. Thus all eight named vertices below
are pairwise distinct. The existing proof also excludes r-ell.

Deleting p from U gives the literal graph W, with k-1 total vertices and
the two actual faces

`F5=(z,s,v,w,t)`, `F4=(z,q,ell,m)`.

Their closures share exactly z. The five F5 chords are absent. The two
F4 diagonals z-ell and q-m are absent. The existing mv,mw,ms,mt and all
other original nonedges are preserved as source facts; they do not impose
extra unequal-colour constraints in the local checker. The two new
nonedges ell-v and ell-w have not been assumed here.

For any one complete W colouring, legal p colours are exactly the colours
missing from `(z,q,ell,m)`; legal r colours are exactly those missing from
`(s,v,w,t)`. The choices are independent because pr is a nonedge. Each
legal p lift is a complete colouring of the same U, so its outer boundary
must lie in 319, even when it has no r lift. For every p/r product member,
all legal xy assignments must be retained. Reconstructing T0 adds exactly

`rs,rv,rw,rt,pz,pq,pell,pm,zx,sx,rx,xy,zy,ry,ty`.

The complete R table is the inherited [JOINT_FIBRES](../../2026-10-14-c4-mask13-joint6-fdd3e22/JOINT_FIBRES.md):
ABAB forces complementary pq; ABAC is empty; ABCB forces pq to avoid z
and contain the missing colour; ABCD forces pq to use the s,t palette.
This includes the Kempe-derived ABCB condition, not just target-cap failure.

## 2. Simultaneous identifications on the two actual faces

Draw one new s-w arc in the open face F5 and one new z-ell arc in the
open face F4. Their closures are disjoint: the first has neither endpoint
z, and the interiors lie in different open faces. Contract both arcs.
The only nontrivial classes are `{s,w}` and `{z,ell}`. Each class is an
original nonedge, so no retained edge becomes a loop. Suppress parallel
copies without deleting any edge constraint. This gives a loopless planar
quotient J with k-3 vertices. For example the image of zq is a surviving
edge. No putative ell-v edge would become a loop in this construction:
ell and v have not been identified.

The adopted thin C5 cap construction puts a four-edge path with three new
vertices beside a surviving edge and makes its empty side exterior. It
produces a legitimate comparison disk with `(k-3)+3-5=k-5<k` inner vertices.
By the original global minimum-source contract its complete relation lies
in the nonempty K132 catalogue. A complete colouring therefore pulls back
to a complete colouring of this same W with

`f(s)=f(w)` and `f(z)=f(ell)`.

Repeat separately using a v-t arc in F5 and the same z-ell arc in F4.
The classes are now `{v,t}` and `{z,ell}`, again disjoint nonedges. The
identical cap budget proves a second, separately quantified complete W
colouring with

`g(v)=g(t)` and `g(z)=g(ell)`.

This is a statement about two source-colourable quotients, not a simultaneous
colouring satisfying all four equalities. The two outer chords s-w and v-t
cross in F5 and cannot be contracted together by this construction.

## 3. Forced complete fibre unions and the new original-edge exclusions

For the first witness, z=ell means that p has at most three neighbour
colours. At least one p lift therefore exists. Each such lift belongs to U,
so `Sigma(U)=319` and s=w force

`(z,s,v,w,t)=(A,B,A,B,C)`

after one common normalization. In particular **ell=v=A**. The existence
of this complete W colouring immediately contradicts any original ell-v
edge, which would have been retained. Thus ell-v is absent in G.

For the second witness, the same p-lift argument and v=t force

`(z,s,v,w,t)=(A,B,C,A,C)`.

Now **ell=w=A**, proving the original nonedge ell-w. These implications
use the full existence of a W colouring and preservation of original
edges; they are not statements about independent marginal supports.

The exact remaining local colours can also be derived without computation.
In either displayed boundary row, the unique r colour is D. The resulting
R row `(z,s,r,t)=(A,B,D,C)` is rainbow, hence every legal p lift satisfies
`{p,q}={B,C}`. If m were not D, D would be legal at p, since z=ell=A and
q is B or C. This is forbidden. Therefore m=D, and p is uniquely the
other member of `{B,C}`. The unique xy lift is `(C,B)`.

With ordered W pins `(z,s,v,w,t,q,ell,m)`, the two separately nonempty
complete-colouring unions are consequently

| Legal quotient equalities | Complete W fibre union | All cap lifts in the same frame |
| --- | --- | --- |
| s=w, z=ell | ABABCBAD or ABABCCAD | r=m=D; pq=CB or BC; xy=CB |
| v=t, z=ell | ABCACBAD or ABCACCAD | r=m=D; pq=CB or BC; xy=CB |

Each row of the table asserts that at least one of its two full fibres is
nonempty. It does not assert both individual fibres exist, equal counts,
or any Kempe path between them. If the optional original edge qs exists
(equivalently c=4), then the q=B option is impossible in each row, and the
remaining individual fibre is nonempty. This conditional refinement does
not remove the c=4 source branch.

Literal reflection of the entire source exchanges
`x/y,a/c,p/q,s/t,v/w`. Writing the reflected q link as
`(c,b,p,ell,n)` gives the same conclusions for `r=6,q=5`. The pq opposite
face vertex ell is transported with the whole graph and remains the same
original vertex when both p and q have degree five.

## 4. What can and cannot be added to the quotients

The new nonedges make the three-vertex classes `{z,v,ell}` and
`{z,w,ell}` independent. Each is realized by an arc from z in each actual
face; its planar quotient therefore has a nonempty complete W fibre.
The exact local screen leaves 16 canonical rows for either class, so this
step supplies no local contradiction.

Adding s=w to `{z,v,ell}` is not licensed: z-v and s-w have alternating
endpoints on the actual C5. Likewise adding v=t to `{z,w,ell}` would cross
z-w. Adding q=m to a quotient using z=ell crosses the two F4 diagonals.
The nonedges mv,mw do not by themselves supply a cofacial m-v or m-w arc.
A path through z would merge m with its adjacent vertex z and create a
loop. No arbitrary planar embedding change is asserted.

The legal disjoint choices s=w,q=m and v=t,q=m have two surviving rows
each (recorded in the certificate); they force ell=r after lifting and
recover an already known nonedge. We do not count that recovery as a new
source restriction.

This records a finite, specified family of two-face identifications. It is
not an exhaustive claim about all possible graph surgeries or Kempe
arguments. In particular a nonempty local table does not realize any
minimum source or show that the full source hypotheses are consistent.

## 5. Verification and precise stopping point

[check.py](check.py) visits all `4^8=65536` labelled assignments and all
5040 proper face assignments. For each one it compares direct enumeration
of every `(r,p,x,y)` lift against the independent product construction.
It retains all 210 canonical proper rows in [certificate.json](certificate.json),
including every full lift, every target-success lift, and all empty cells.
The full inherited R rule and complete U support upper bound leave 120
necessary rows; 60 have no p lift and 42 have no r lift. The certificate
keeps all ten outer fibres, including the three forbidden U rows whose W
colourings can only have empty p lift. Every bit of 319 has locally
p-liftable rows; this is only compatibility with the known exact support,
not a new proof of source realizability or a multiplicity model.

The paper argument supplies the actual-face planarity, strict cap budget,
nonempty complete W fibres, and resulting original nonedges. The program
checks only the specified finite colour arithmetic. It binds all six direct
tracked proof inputs and its own source by SHA256; the root INPUTS seal
also records the exact BASE custody. Logs and receipts retain a normal
replay, a seed17 replay, and rejection of a corrupted actual cap lift.

The [independent cap checker](../review/independent_caps.py) imports none
of this checker. It uses the older seven-pin R6_TRANSFER table and direct
original-edge tests to verify all 210 canonical rows, all full cap lifts,
the 120 necessary rows, and the 2/2/16/16 quotient-slice counts; its
[result](../review/independent-caps.json) agrees. The independent geometry
review also confirms the two quotient embeddings and the strict k-5 cap
budget. Neither finite checker certifies arbitrary plane embeddings.

**New:** the arbitrary-size intersection `r=6,p=5` (and reflection)
excludes original ell-v and ell-w edges and has the two complete fibre
unions above. **Still OPEN:** the full `r=6,p=5,a>=6` source intersection,
its reflection, mask319, and the remaining low-p/q sources. No new degree
excess, k bound, unbounded closure, external enumeration, or Lean theorem
is claimed. The general `K<=22=K<=5=K132`, minimal-source `k>=23`, and
conditional `p,q>=6 => k>=28` retain their previous scopes.
