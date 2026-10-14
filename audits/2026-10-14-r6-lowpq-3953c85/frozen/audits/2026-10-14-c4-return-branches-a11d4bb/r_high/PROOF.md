# Surviving high-r branches: a direct t deletion and the exact C6 frontier

BASE is `a11d4bb949843aceeda7cc560d075716c71de80f`, in the exclusive
`math-c4-return-branches-a11d4bb` worktree. This file writes only the new
`r_high/` audit. The [input seal](../INPUTS.json), original
[SOURCE_GEOMETRY](../../2026-10-14-c4-mask13-joint6-fdd3e22/SOURCE_GEOMETRY.md),
[JOINT_FIBRES](../../2026-10-14-c4-mask13-joint6-fdd3e22/JOINT_FIBRES.md), and
[previous degree-six transfer](../../2026-10-14-c4-c5-recursion-fdd3e22/degree4/R6_TRANSFER.md)
are authority. No existing report or certificate is modified.

The new arbitrary-size conditional exclusion is

`d_G(a)=4 => d_G(t)>=6`, and by reflection `d_G(c)=4 => d_G(s)>=6`.

It applies within the fixed original x,y,b-four-degree source, for every
r degree. In the remaining t=5 branch, the smaller direct-deletion C5
support is narrowed to956/1012/1020. The original assumptions are the no4ct globally minimum noncatalogue C5
source G, `d_G(x)=d_G(y)=d_G(b)=4`, with literal original apexes
`(r,t,p,q,s)`. Its disk R has boundary `(z,s,r,t)`, `k+1` total vertices,
and retained facial triangle `zpq`. The previous return proof excludes
`d_G(r)=5`; the previous degree-six proof gives
`d_G(r)=6 => d_G(s),d_G(t)>=6`. Those results are already proved. This
audit does not claim a new exclusion of r=6, r=7, or arbitrary high r.

## 1. A C5 frontier when t still has original degree five

The direct deletion below is different from first deleting r. It applies
without assuming r=6. Since r=5 is excluded and r=6,t=5 is excluded, its
remaining live source domain has `d_G(r)>=7`.

Assume `d_G(t)=5`. In R, t has degree four: it lost exactly the edge ty,
and a was renamed z. The original fan exposes

`N_R(t)=(z,h,w,r)`.

Delete t with its actual edges and no identifications. The resulting disk

`V=R-t`, boundary `(z,s,r,w,h)`,

has k total vertices and `k-5<k` interior vertices. The boundary is a
simple Jordan cycle because the two intermediate vertices h,w in the
degree-four fan are distinct and strictly internal before deletion. The
inner fan's three faces become exterior; all other faces and all original
edges remain unchanged. Inducedness is unnecessary for the relative
minimum-source C5 catalogue step.

The forbidden edge tq prevents either exposed vertex from being q. The
only permitted coincidence with the marked triangle is `h=p`: indeed
`tp` holds exactly when original `d_G(a)=4`; its original facial triangle
at a places p at h, next to z. Thus p cannot equal w. If h differs from
p, both p,q remain internal. If h=p, retain the original p as the fifth
boundary vertex; q remains internal and the original triangle zpq is
still facial. There is no second copy of p.

For **each complete V colouring**, every colour absent from
`{f(z),f(r),f(w),f(h)}` is a legal t colour. All those lifts must satisfy
the original R joint table simultaneously, with the exact same unchanged
p,q colours. The R table is ABAB/CD, ABAC/empty, ABCB/{CD,BD}, ABCD/BD.
The following direct table takes the intersection over all t lifts.

| V boundary `(z,s,r,w,h)` | All t colours | Permitted ordered pq, h distinct from p |
| --- | --- | --- |
| ABABC | D | empty |
| ABACB | D | empty |
| ABACD | B | CD,DC |
| ABCAB | D | BD,DB |
| ABCAC | B,D | BD,DB |
| ABCAD | B | BD,CD,DB,DC |
| ABCBC | D | BD,DB |
| ABCBD | none | BC,BD,CB,CD,DB,DC |
| ABCDB | none | BC,BD,CB,CD,DB,DC |
| ABCDC | B | BD,CD,DB,DC |

The bit order is the frozen K132 ten-row order, starting at zero. Its
upper outer mask is1020. A complete V colouring with no t lift remains
in V's complete relation; it cannot be discarded. Minimum-source
minimality places the complete outer support in K132. The mask1020 screen
first allows exactly

`424,440,564,572,628,632,636,956,960,976,1000,1012,1016,1020`.

The exact necessary Kempe closure described in section3 removes the four
candidates564,572,628,636. Thus the new precise source frontier is

`t=5, h!=p => Sigma(V) in {424,440,632,956,960,976,1000,1012,1016,1020}`.

This is an intermediate finite certified necessary reduction of the
arbitrary-size source branch. It does not give full-fibre equality with
catalogue representatives. An additional geometric minimum-source step
narrows it further.

The original z,r are nonadjacent and now lie on V's actual exterior.
Identify them along the exterior and suppress parallel edges. The
quotient is loopless, simple and planar, with k-1 vertices. It still has
the triangle zpq, hence has an edge. Choose an edge incident with a face,
designate that face exterior, and attach a path of length four between
its endpoints. Keep the original edge as the fifth side of the new
outer C5 and choose the empty side of this cycle as exterior. This adds
three vertices, giving a legal disk with k+2 total vertices and
`k-3<k` interiors. Its K132 relation is nonempty by original minimum-source
minimality. Restrict a colouring to the quotient and pull it back to
V: this supplies a complete V colouring with z=r.

There are **three** canonical C5 rows with z=r: ABABC,ABACB,ABACD.
The first two are empty by the all-t-lifts table, so the actual ABACD
fibre is nonempty. Of the ten intermediate masks, only956,1012,1020
contain that row. Thus the final generic frontier is

`t=5, h!=p => Sigma(V) in {956,1012,1020}`.

The quotient supplies existence on one explicitly constructed smaller
graph. It does not identify quotient fibres with catalogue representative
fibres or assert colourability of arbitrary planar graphs. Reflection
`(x,y),(a,c),(p,q),(s,t)` gives the corresponding s=5 frontier.

## 2. The literal h=p subcase

When h=p, the actual boundary is `(z,s,r,w,p)` and q is still internal.
The direct all-t-lifts table is the following six-distinct-pin table.

| V boundary | Permitted q |
| --- | --- |
| ABABC | empty |
| ABACB | empty |
| ABACD | C |
| ABCAB | D |
| ABCAC | empty |
| ABCAD | B,C |
| ABCBC | empty |
| ABCBD | B,C |
| ABCDB | C,D |
| ABCDC | D |

The upper mask is940, and the only K132 mask contained in940 is424.
Necessary Kempe closure further leaves exactly four canonical full pin
rows, with q appended after the five boundary pins:

`ABCABD, ABCADB, ABCBDB, ABCDBD`.

Before applying the exterior quotient, the necessary implication is

`t=5, a=4 => Sigma(V)=424`,

and its complete six-pin relation is contained in those four rows and
their common S4 renamings. Each of the four outer rows is present because
mask424 contains all four; in this subcase only one q colour survives in
each canonical row. This does not determine full-fibre multiplicities.
But mask424 contains none of ABABC,ABACB,ABACD, whereas the original
nonedge zr and the exterior quotient argument above supply a complete
V colouring with z=r. This is a contradiction. Thus this alias branch
is genuinely excluded, without assuming r=6 and without the finite
terminal closure refinement:

`d_G(a)=4 => d_G(t)>=6`.

Reflecting all original names gives `d_G(c)=4 => d_G(s)>=6`.
These are new conditional source exclusions, not an exclusion of all
original t=5 or all high-r sources. In particular every remaining t=5
source has original a>=5 and its V support is956/1012/1020.

A named finite calibration graph realizes this **six-pin** relation:
take the C5 `(z,s,r,w,p)`, add the two chords zr,rp, and stellate the
central triangle zrp with q. The inner faces are
`zsr,rwp,zrq,rpq,pzq`. Direct enumeration saves every complete colouring:
there are96, exactly the 24 common renamings of the four displayed rows.
It obeys every direct all-t-lifts condition and uses an actual plane
embedding and actual complete fibres. However, **zr,rp,rq are all
source-forbidden edges**. This is a calibration graph, not an original
source or a counterexample to the desired source exclusion. It shows
that the marked palette table alone does not supply a contradiction.
The actual source's nonedge zr, absent in this calibration graph, supplies
the exterior-quotient existence step that closes the alias subbranch.

## 3. Why the finite closure is a necessary source theorem

Keep every literal marked colouring row, including improper or empty
boundary fibres as empty entries. For any one actual full colouring of V
and one complementary pairing of the four colours, take the actual
maximal components of its two induced colour-pair subgraphs and project
their vertex sets to the marked pins. These projected blocks respect
mandatory edges and are noncrossing **only on the actual outer C5**.
No internal pin is artificially placed on the Jordan boundary.

Switching any subset of these maximal components yields another complete
colouring of the **same** V. All resulting marked rows must remain in the
all-t-lifts relation and in its exact outer support. The terminal model
retains a row only if each complementary pairing has some such terminal
partition whose entire simultaneous-switch orbit stays in the retained
rows. Actual full colouring rows cannot be removed in any iteration:
induction supplies every successor from their same actual components.

Consequently a candidate exact outer mask m is impossible when this
necessary closure loses one of m's outer rows. That is exactly what
happens to564,572,628,636. The finite model's surviving partitions are
necessary witnesses only; they need not arise from one graph or one
consistent system of components across different colour pairings.
Multiplicity is not represented, and no actual fibres are identified
between different graphs.

## 4. Original r=7 exposes C6, with no direct return contradiction

Assume `d_G(r)=7`. The degree in R is five. Write the original fan as
`N_R(r)=(s,v,w,h,t)` and delete r. The literal smaller disk

`U7=R-r`, boundary `(z,s,v,w,h,t)`,

has k total vertices and `k-6<k` interior vertices. Its boundary is
induced: z has no additional common neighbour with r, so zv,zw,zh are
absent; every chord between nonconsecutive members of r's inner fan
would make a nonfacial triangle through r in the four-connected T0;
st is already forbidden. The marks p,q remain distinct internal
vertices with the same original facial triangle zpq.

For each complete U7 colouring, all r colours absent from
`{f(s),f(v),f(w),f(h),f(t)}` must obey the same original R table. This is
the exact local eight-pin all-lift screen. There are31 canonical proper
C6 outer words. Five words have empty marked fibres under this screen:

`ABCBCD, ABCBDC, ABCDBC, ABCDBD, ABCDCD`.

The other26 words allow111 canonical joint rows. With the honest C6
noncrossing condition, every one of those111 rows survives all three
complementary-pair terminal closure tests; the first iteration removes
zero rows. The certificate gives a valid terminal partition and its
whole successor orbit for every retained row and pairing. This is not
an exact common-count witness, an actual graph, or a source realization.

The original C4 return hypothesis is unavailable here. For example,
`(z,s,v,w,h,t)=ABABCD` gives all four neighbour colours at r, so there is
no r lift, while `(z,s,h,t)=ABCD` is rainbow. The all-lift screen admits
this row and every proper pq palette. Thus one cannot infer that a
chosen four-point restriction has no rainbow from the empty R ABAC
fibre. Those four points also do not bound a literal C4 disk. Adding
or suppressing edges to manufacture such a disk would change the graph
and its full fibres.

For r=6, the existing exact integer witnesses on masks271,314,319 already
show that the previous terminal support and common-count equations do
not contradict one another. This audit does not rerun that solver or
convert count feasibility into source realizability.

## 5. Replay and claim boundary

Run:

```sh
python3 -B audits/2026-10-14-c4-return-branches-a11d4bb/r_high/check_high.py --check
```

[high-v2.json](high-v2.json) binds the checker and the frozen transfer helper
and catalogue hashes. The checker independently compares the literal
equality predicate with a canonical joint-row table over all16,384
generic and4,096 alias labelled assignments; the r=7 screen checks all
65,536 labelled eight-pin assignments. It preserves the full common
colour frame, all legal lifts, and empty cells. It also saves the named
control graph's entire96 complete colourings. Normal and seed17 replays
and a corrupted-certificate negative check are retained in [logs](logs/).

The direct deletion, exterior-quotient colourability, and component-closure
soundness are arbitrary-size arguments on the original source. The finite
part computes their exact necessary frontiers. The alias support424
contradiction needs only its all-lift table, accepted K132 membership,
and the original nonedge zr. None of the surviving states is claimed to
realize a source. General t=5 with r>=7 and a>=5, r=6 as a whole, r=7 as a whole,
and the unbounded catalogue equality remain OPEN. No external theorem,
new broad enumeration, Lean theorem, commit, or push is used here.
The initial weaker frontier certificate [high.json](high.json) and its
bound checker [check_high_initial.py](check_high_initial.py) are retained
unchanged; they precede the source exterior-quotient screen.
