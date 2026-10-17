# A: two nonempty cofacial equality quotients, with every z fibre retained

BASE `e98a1cc1afd9a428600dcf4027d8138078c01650`. This audit writes only
the exclusive directory `A/`. The authority is the root `BASE.json` and
the immutable files under `../frozen/`; no source graph is supplied.

The new conclusion is a pair of **relative nonemptiness obligations** for
actual cofacial quotients of the same source. It does not establish
`W110+W101>0` or exclude complete 319. A separate section turns one old
finite Kempe elimination into a complete-colouring paper bijection; that
section is explicitly not a new exclusion beyond the frozen finite screen.

## 1. Fixed source, original edges, and the exact quotient domain

Fix the globally minimum-interior-vertex, then maximum-edge no4ct C5
source G from the frozen contract, with original boundary `(x,y,a,b,c)`,
`d_G(x)=d_G(y)=d_G(b)=4`, and `d_G(r)=6`. Put
`a0=d_G(a)`, `c0=d_G(c)`, and `h=a0+c0-8>=3`.
All names refer to the original source. Use the already proved

`U=R-r`, `J=U/(s=t)`, `m=[s=t]`,

with original r rotation `(x,y,t,w,v,s)`, U boundary
`(z,s,v,w,t)`, and `Sigma(U)=319`.
The six J vertices `(m,z,v,w,p,q)` are distinct; its actual faces include
`mvw,zpq`, and `mz` is a retained edge. J has `k-1` vertices. Every
triangle of J is facial, so deleting z exposes its actual induced link
cycle as one face of `B=J-z`.

The original induced-apex theorem says

`sp,tq notin E(G)`,
`tp in E(G) iff a0=4`, `sq in E(G) iff c0=4`.

No other identification creates an m-p or m-q edge. Therefore, literally,

`mp in E(J) iff a0=4`, `mq in E(J) iff c0=4`.             (1)

Both m and p, and both m and q, lie on the actual face exposed by deleting
z, since all three are original neighbours of z. Thus:

* if `a0>4`, define `H_p=(J-z)/(m=p)`;
* if `c0>4`, define `H_q=(J-z)/(m=q)`.

Each indicated identification is of a cofacial nonedge. Draw its new arc
inside that face, contract the arc, and suppress parallel edges. No
original edge becomes a loop. This is an actual planar quotient, not a
claim that m and p or q were cofacial in J before z was deleted.
At least one quotient is defined, because `a0+c0>=11` excludes
`a0=c0=4`. Both are defined if both original degrees exceed four.

## 2. Relative minimality proves each defined quotient nonempty

For either defined H, deleting z and identifying one distinct pair gives
exactly `|V(H)|=k-3`. It has an edge: the triangle mvw survives with its
three vertices distinct (p and q were distinct from v,w).

Apply the frozen cofacial-cap construction to **this entire H**. Choose
one retained edge uv and draw a new length-four path from u to v along
one incident face side. Declare the empty five-cycle between that path
and uv to be the exterior boundary. The resulting legitimate C5 disk
has three new vertices and

`k(cap(H))=(k-3)+3-5=k-5<k`.

The comparison class permits inner cutvertices, chords and nontriangular
faces. It does not require the comparison disk to have the source normal
form. Its complete relation belongs to K132 by global source minimality;
all K132 relations are nonempty. Consequently cap(H), and hence H, has
a complete proper four-colouring in the literal colour frame. Thus

`a0>4 ==> Col_4(H_p) != empty`,
`c0>4 ==> Col_4(H_q) != empty`.                         (2)

The witnesses for H_p and H_q are separately quantified. They are not
combined into one colouring. No universal planar-colourability theorem
is used. Relative minimality is the essential source premise here.

## 3. Exact z fibres over every complete quotient colouring

Let `L_z=N_J(z)` denote the full original link, including every fan
vertex. A complete H_p colouring pulls back bijectively to a complete
colouring chi of `J-z` with `chi(m)=chi(p)`; H_q has the symmetric
bijection with `chi(m)=chi(q)`. Parallel-edge suppression loses no
proper-colouring constraint. Define from this very full colouring

`A_z(chi)={0,1,2,3} minus chi(L_z)`.

The full J lift fibre is exactly

`K_z(chi)={chi extended by z=b : b in A_z(chi)}`.        (3)

This is a pointwise bijection retaining every private vertex. In
particular `A_z=empty` is a genuine empty full-colouring fibre.

For H_p set `c=chi(m)=chi(p)` and `d=chi(q)`. The edge pq gives c!=d;
triangle mvw gives two distinct colours `u=chi(v),v0=chi(w)`, both
different from c. Every nonempty lift in (3) is an actual colouring of
the same J. The complete frozen all-r obligation is

`(d(vw)=d(pq)) iff (d(vw)=d(mz))`.                     (FJ)

In a lift with z=b, FJ holds **if and only if**

`{b,d}={u,v0}`.                                      (4p)

Proof: if b is the fourth colour of triangle mvw, FJ requires
`{p,q}={v,w}`, which is impossible because p=m has colour c. Otherwise
b is one of u,v0, and the complete all-r table requires pq to contain
the other member of `{u,v0}`. Since p has colour c, this member must
be q. Conversely that assignment is exactly the permitted case.
This is also a direct XOR check; it is independent of a colour renaming.

Apply (4p) to **every** b in the full fibre (3). The exact obligation is

`A_z(chi) subseteq {u,v0} minus {d}` and `d in {u,v0}`
whenever `A_z(chi) != empty`.                         (5p)

Equivalently, the only possibilities are:

1. `A_z=empty`;
2. q equals one of v,w and `A_z` is exactly the singleton containing
   the other one's colour.

For H_q the same conclusion holds with p and q interchanged:
if `A_z!=empty`, p equals one of v,w and the unique missing colour
is the other one's colour. The original individual p/q assignments
are retained; they have not been normalized independently.

Thus every complete colouring of either defined H uses at least three
colours on the **entire actual** link L_z. If the unmerged pq endpoint
has the fourth colour of mvw, every such colouring uses all four
colours on L_z and has no J lift. These are necessary, arbitrary-size
source restrictions on the complete nonempty quotient relations (2).

Every genuine J lift in (3) splits m back into s,t of the same colour.
The unique legal r colour is the fourth colour of `(m,v,w)`. It is
retained, and FJ was derived using its entire all-r obligation. No
other U fibre, including `s!=t` or no-r fibres, is deleted by the
construction or replaced by this quotient relation.

## 4. Why quotient nonemptiness does not supply a J witness

Statements (2) and (3) give a nonempty **set of complete base
colourings**, with the complete lift set over each base. They do not
assert that any of those lift sets is nonempty. The allowed first
case in section 3 can occur in a genuine planar local control.

The control used by `check.py` is the actual two-star disk with paths

`P_m=(alpha,u,w,v,r0,beta)`,
`P_z=(alpha,p,q,j,beta)`,

outer cycle `P_m` followed by `reverse(P_z)`, hubs m,z, edge mz,
m adjacent to all P_m and z adjacent to all P_z. Its two hub degrees
are 7 and 6, respectively. Delete z and identify m=p along its exposed
face. The complete quotient colouring

`m=p:0, alpha:1, u:2, w:3, v:2, r0:1, beta:3, j:2, q:1`

is proper. Its entire old L_z uses `{0,1,2,3}`, so `A_z=empty`;
q is the fourth colour of mvw. Every vertex and every edge of this
small quotient is checked. This is a local calibration, not a source
realization and not a graph satisfying all source constraints.

No edge qv or qw has been inserted: they are not known to be cofacial
in H_p. Adding them solely to force the fourth colour would require
a separate embedding proof. Likewise, reinstating z after the
noncofacial identification in J is not licensed by the planar
identification proof for J-z.

The exact remaining direct obligation is to prove that, in one of the
defined **same-source** quotients, some complete colouring has a
nonempty A_z and violates (4p) or its reflection. The source conditions
above currently do not force even `A_z!=empty`. No numerical decrease
here is a smaller bad-source descent: reversing the quotient and
restoring z gives J, then splitting m and restoring the five original
vertices costs the original completed total `k+5`.

## 5. Paper lift of an existing complete-U finite elimination

This section is a paper proof of restrictions already present in the
frozen `degree4/transfer.json` Kempe fixed point. It adds an explicit
complete-fibre bijection but does not strengthen that finite screen.

Use literal colour names A,B,C,D and write F(X) for all complete U
colourings with its ordered boundary `(z,s,v,w,t)=X`.
For every source colouring in F(ABACD),

`pq contains D=chi(t)`.                               (6)

Proof: z,t are in one AD component by their boundary edge. If v is
outside that component, switching its AD component changes the
boundary to the forbidden ABCDC. Hence z,v,t lie in one AD component.
The actual AD path z--v has alternating outer endpoints with any BC
path s--w. Thus s,w are in different BC components. Switch the BC
component of s. The new literal boundary is `(A,C,A,C,D)`. The full
all-r table for this ABABC-type boundary forces pq palette `{C,D}`.
The switch cannot create a D-coloured vertex, so the old pq already
contained D. This excludes precisely the old BC and CB no-r entries.

There is a full-colouring bijection

`F(A,B,A,C,D) <--> F(A,C,A,C,D)`,                      (7)

given in each direction by switching the maximal BC component of s.
For the reverse direction, if v were outside the AD component of z,t,
the v-component switch would give the forbidden ABCBC. Thus the same
Jordan argument disconnects s,w in BC. The s-component switch in
both directions is well-defined and fixes z,v,w,t individually;
its own vertex set is unchanged, so it is an exact inverse. Every
private vertex is switched according to its actual component.

For p/q the pointwise rule in (7) is simply: interchange B,C exactly
at those original endpoints lying in that same component; D is
fixed. Since pq is an edge, if both endpoints are in BC they are
switched together. This is a rule on each full colouring, not a
statement that independent ordered fibres coincide.

Reflect the original graph by
`s<->t,v<->w,p<->q,a<->c,x<->y`, then make one common colour renaming.
This proves the reflected complete bijection between the ABCAC and
ABCAD sectors and, in every F(ABCAD) colouring,

`pq contains B=chi(s)`.                               (8)

Exactly four canonical rows of the initial 26-row upper table are
excluded: `ABACDBC,ABACDCB,ABCADCD,ABCADDC`. The remaining 22 canonical
rows are a necessary screen, not an exact source relation. All empty
fibres remain present. The source's seven boundary bits remain
unchanged, and complete 319 remains OPEN.

## 6. Verification and authority boundary

`check.py` independently checks the exact cofacial-fibre algebra,
every complete colouring and all empty/nonempty z fibres of the
nine-vertex quotient control, and the listed explicit saturation
witness. It separately enumerates the 16,384 seven-pin assignments
to verify the complete all-r table and the four old eliminated rows.
The active `sealed-certificate.json` explicitly retains all 16,384
positions in lexicographic order, every original r lift, and the
zero slots of the initial and refined upper relations. Its 624 and
528 positive labelled slots are upper-relation entries, not counts
of actual source full-colouring fibres.
For an improper seven-pin assignment the full local r fibre is empty;
raw colours merely avoiding the four r neighbours are recorded separately.
It does not test source realizability or infer an arbitrary-size
embedding from finite graphs. Normal and seed-17 replay and negative
controls are in `VERIFICATION.json`.

The first normal replay failed because Python tuples in the calculation
were compared directly with JSON lists. `initial-check.py`, the original
`certificate.json`, and `initial-normal.stderr` preserve that failure.
The corrected checker normalizes JSON structure before comparison;
no mathematical row changed. The intermediate `final-certificate.json`
is retained; `complete-certificate.json` adds the explicit dense zero
slots requested during independent review. The active sealed certificate
also separates raw neighbour-avoiding colours from full local r lifts
on improper seven-pin rows. Its normal, seed-17, missing-empty-fibre,
wrong-count, missing-zero-slot, improper-row-r-lift, and exclusive-create
checks all have the expected outcomes.

The arbitrary-size results are the original-face quotient construction,
relative-minimality nonemptiness, and the complete-fibre proofs above.
Source-level numerical coverage is `not triggered`: no hypothetical
minimum source has been supplied. The full source exclusion,
`W110+W101>0`, omega zero, and a strict completed-source descent remain
OPEN. No external theorem, 4CT oracle, Lean, commit, or push is used.
