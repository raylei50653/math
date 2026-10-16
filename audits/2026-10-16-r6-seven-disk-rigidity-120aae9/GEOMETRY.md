# Seven-disk rigidity: the actual exterior forces three ordinary ears

BASE `120aae90cab8bc4881916adc598cf344f2f20f4b`. All arguments concern
one unchanged original source, its legal J, actual sphere dual D, fixed
marks e,f,g, and the same maximum-cardinality barrier S and component C.
Nothing is substituted, contracted in the source, or recoloured. Filling
actual exterior faces below is only a way of recognizing a separator in
this same embedding.

## 1. Adopted exact inputs

Use the sealed [seven-disk geometry](../2026-10-16-r6-101-nonwheel-seven-cut-120aae9/GEOMETRY.md),
particularly G1--G6. The actual faces C form a triangulated disk R with
simple boundary Q of length seven. No Q chord is on the R side. No member
of T={m,z,v,w,p,q} is strictly inside R. Every boundary vertex u has at
least one strictly interior neighbour; call their number t_u. Put
I=# odd-complete-degree vertices strictly inside R, B=# odd t_u, and
epsilon=1 exactly when m is on Q with odd t_m. The inherited exact equations
are

    Delta=I+B-2 epsilon-10,     Delta>=2(1-epsilon),

where every individual degree excess is nonnegative and even. The
parity-sensitive complete-degree minima are m:8-o, z:6+o,
v,w,p,q:4+o, and every other vertex:6-o.

The inherited source geometry also supplies: every triangle of J is an
actual face; every induced C4 meets m or z, with the exact original-sector
crossings of [Theorem C](../2026-10-16-r6-joint-zero-c4c3d99/C/PROOF.md#c2-induced-c4s-must-cross-the-original-sectors).
The sectors are L_s,L_t at m and L_a,L_c at z. The two mz faces are
mz alpha, mz beta, with alpha in L_t intersect L_a and beta in L_s
intersect L_c. The specified e face is mvw and specified f face is zpq.
The other e face is denoted vwj. All four faces X=V(e) union V(g) avoid C,
D[X]={e,g}, and no f endpoint belongs to S or X. The only residual
component of size greater than one is C. The complete monochromatic
primal-edge set is exactly {vw,pq,mz} union (all nonboundary R edges).
Across any Q edge other than pq, the exterior face is therefore in S union X.
If pq lies on Q, its exterior face is the other residual f endpoint.

The original m sector lengths and degree identity are

    d_G(s),d_G(t)>=6,   d_J(m)=d_G(s)+d_G(t)-5.

If the C block is in a sector belonging to u=s or t, the exact face word
has d_G(u)-3=2k+t_m+2; the other sector has d_G(u')-3=2k'.
These are adopted arbitrary-size source statements, not finite controls.

## 2. The full excess cancels: three ordinary ears are compulsory

No equality case is assumed here. For every vertex u let s_u be its
nonnegative even complete-degree excess over its parity-sensitive minimum.
Put Delta_i=sum of s_u over vertices strictly inside R. The interior
contains no T vertex, so its complete degree is 6-o_u+s_u. Consequently
its total curvature is I-Delta_i. The exact disk Euler identity is

    sum_Q t_u = 8+I-Delta_i.                                  (G1)

For u on Q put beta_u=t_u mod 2 and l_u=2-beta_u. Thus l is one
for odd t and two for even t, and sum_Q l_u=14-B.

First note that **zpq is outside R**, without any assumption on I or
Delta. A C face on these three T vertices would have every vertex on
Q, since none can be strictly interior. Every edge of that triangle
would then be a Q edge, since an R-side Q chord is forbidden. A simple
seven-cycle cannot contain the three edges of a triangle.

The exact degree-parity and original-sector bounds give the following
complete boundary accounting.

* Ordinary u outside T has complete degree d=6-beta+s_u. Its difference
  d-d_R is nonnegative and even. If positive, it is at least two, giving
  t_u<=l_u+s_u. If zero, exactly one actual exterior triangular face is
  incident with u; it joins its two Q neighbours and is an ordinary
  exterior ear. In that case t_u=l_u+s_u+2.
* For v,w,p,q the complete degree is d=5-beta+s_u. The difference
  d-d_R is a nonnegative odd number, hence at least one. Therefore
  t_u<=l_u+s_u.
* For z the complete degree is d=7-beta+s_z. Its exterior face interval
  contains the two mz faces and the distinct face zpq. Its length
  d-t_z-1 is even and at least three, hence at least four. Thus
  t_z<=d-5=l_z+s_z.
* If m lies on Q, its C block lies in one original s/t sector. The
  sector containing C has original degree at least t_m+5. The other
  sector has odd original degree at least seven, by its alternating
  zero-to-zero face word. Thus d_J(m)>=t_m+7. As its complete minimum
  is 7+beta_m, this gives t_m<=beta_m+s_m. For odd t_m this is
  t_m<=l_m+s_m; for even t_m it is the stronger
  t_m<=l_m+s_m-2.
* If m is absent from Q, both original sector degrees are odd and at
  least seven. Its complete odd degree is at least nine, so s_m>=2.
  This excess is outside both the disk interior and its boundary.

Let h count ordinary exterior ears. The preceding bounds are about
actual complete degrees and actual exterior faces; even excesses of
any magnitude are retained. Sum them over Q. If m is on Q with even t,
subtract two at m. If m is absent from Q, remove its at-least-two
outside excess from the available boundary excess. Both cases are
exactly the correction -2(1-epsilon). All other exterior excess is
nonnegative. Therefore

    sum_Q t_u <= 14-B+(Delta-Delta_i)-2(1-epsilon)+2h.          (G2)

Substitute the adopted exact global identity
Delta=I+B-2epsilon-10. Every I,B,epsilon and excess term is retained;
the right side becomes I+2-Delta_i+2h. Comparing with (G1) yields

    8+I-Delta_i <= I+2-Delta_i+2h,     hence h>=3.             (G3)

This proves the compulsory-ear statement for **every** seven-disk
candidate, with arbitrary interior size and arbitrary degree excess.
It is stronger than excluding a curvature equality stratum.

## 3. Three actual exterior ears produce an induced four-cycle

For an ordinary ear centre u, its sole exterior face is the actual
triangle u^- u u^+, where u^-,u^+ are its two Q neighbours. Neither
old Q edge is pq, because its centre u is outside T. The exact face-bit
identity therefore makes this ear a zero face, in S union X.

Two ordinary ear centres cannot be consecutive on Q: their common Q
edge would have two different exterior incident faces. Their equality
would identify two distinct vertices of the simple seven-cycle. Thus
all ear centres are pairwise nonadjacent. A seven-cycle has independent
sets of size at most three. Equation (G3) now gives **exactly three**
ordinary exterior ears.

Fill these three actual exterior triangular faces simultaneously.
The resulting disk A has simple boundary Q4, obtained from Q by deleting
those three nonadjacent centres. All six distinct T vertices remain on
or outside Q4, because only the ordinary centres became interior.

**Q4 is induced.** A chord would produce two actual facial triangles.
One side of Q4 would consist of exactly those two faces. Its A side
contains the at-least-fifteen faces of C plus the three ears, so the
two-face side would be exterior. That exterior has no strictly interior
vertex. All six T vertices, which are on or outside Q4, would therefore
have to occupy its four boundary positions, impossible.

For an independent check of inducedness, count X ears. At most one ear
can belong to either forced pair V(e) or V(g): otherwise Q would contain
two length-two paths between the marked edge endpoints, and would itself
be a four-cycle. If at most one X ear was filled, the exterior retains
at least three X faces. If two were filled, the two remaining X faces
are from different pairs and are nonadjacent, since D[X]={e,g}. In
neither case can that exterior be a two-face disk.

The face zpq was outside R and is not an added zero ear. It is therefore
outside A. No f endpoint is an added ear, since all ears belong to
S union X. We will use the impossibility of zpq belonging to A below.

## 4. Every possible set of forced ears is excluded by the source sectors

There are four possibilities for which marked pairs supply an X ear.

**No X ear.** A avoids all X. If Q4 avoids both hubs, it violates the
source C4 theorem. If it contains both, mz must be a Q4 edge, but both
its incident faces are outside A, impossible for a boundary edge. If
it contains m alone, its A face interval avoids mvw and both mz faces;
its two rays lie in one original s/t sector, contradicting the required
C4 crossing. If it contains z alone, the required a/c crossing and the
avoidance of both mz faces force its A interval to include zpq, contrary
to the preceding paragraph.

**An e ear and no g ear.** The e ear must be vwj: the other face mvw
cannot be centred at an ordinary vertex. Thus vw is a Q4 edge, and
v,w lie on Q4. If m were also on Q4, the facial triangle mvw would be
a chorded triple in Q4, violating inducedness. Therefore m is absent;
the C4 theorem forces z to be present. Both mz faces are outside A,
so the required a/c crossing again puts zpq in A, a contradiction.

**A g ear and no e ear.** First suppose that ear is mz alpha; the beta
case is the reflected argument. Q4 uses edge mz. Write Q4=m,z,u,v,m.
At m, the original C interval starts with its ray m alpha and lies in
one original sector, here L_t. Adding S ears can extend this interval
without crossing mvw or either mz face. Adding the chosen mz alpha ear
changes its first boundary ray to mz. Its other ray mv therefore still
has v in L_t. The exact induced-C4 sector theorem now forces u in L_c.
At z, the A interval from mz goes through the included alpha face and
then from alpha in L_a toward u in L_c, away from the excluded mz beta
face. It must cross the edge pq in the actual link of z and include
zpq. This is the same forbidden occurrence above. For mz beta, the
remaining m ray is in L_s, the remaining z ray is forced into L_a,
and the arc from beta in L_c again crosses pq.

**Both an e ear and a g ear.** Q4 contains v,w from its vw edge and m,z
from its mz edge. These are its four vertices. The facial triangle mvw
then contradicts inducedness immediately.

All possibilities are impossible. The complete seven-cut disk case is
therefore excluded, with arbitrary interior size and arbitrary excess.
This is an impossibility theorem for the adopted original-source
seven-cut obstruction. It uses its same J,D,S,C, actual original sectors
and all forced faces; no synthetic disk is promoted to a source.

## 5. A local finite patch explains the source authority boundary

An explicitly labelled disk with seven boundary vertices and six interior
vertices exists with five degree-5 interior vertices and one degree-6
interior vertex. It has no induced C4; its five induced C5s are exactly
links of degree-5 interior vertices and bound their full W5 caps. Its
boundary t values are 3,1,3,1,3,1,1. Its dual patch is factor-critical
with seven distinct degree-two ports. This is a synthetic local patch,
not a source: the preceding arbitrary-size source theorem prevents it
from being completed to the required common exterior, original sectors
and barrier, at any degree excess. In particular a seven-disk local
census by itself cannot establish the complete source exclusion.

The independent checker geometry_check.py validates the local identities,
all 59 deletion matching lifts of that synthetic patch, their literal
nonempty fibres, and the collar parity calculation for five interior
vertices. Its 128 ordered port fibres retain 116 matching lifts and 77
empty fibres (including 13 empty fibres with odd selected-port count). Its certificate retains all complete local matching fibres,
including empty multiport fibres. Finite controls are supplementary;
the source-sector argument in sections 2--4 is the all-size proof.

### 5.1 Independent five-interior collar calculation

In the formerly surviving equality case I=5 and i=5,
all five interior degrees are five, and the induced interior
core K has five vertices and six edges. K is connected: each Q-edge face
has an interior third vertex; the interior neighbour paths at consecutive
Q vertices join these into a connected collar, and every other interior
vertex joins this collar in the disk. Every bounded K face is triangular,
since Q is outside K. Euler gives exactly two bounded faces and the full
exterior facial walk has length six, with repetitions retained.

The only possible cores are two triangles sharing one vertex (bowtie),
or a diamond (two triangles sharing an edge) with a pendant vertex.
An actual exterior corner of K must have at least one Q neighbour. A
vertex with r occurrences on the exterior walk consequently needs at
least r distinct Q neighbours. If it needs more than r, it must be the
third vertex of at least one Q-edge face. Around the triangulated collar,
a Q vertex with t interior neighbours advances t-1 steps in the exterior
K walk. All t are odd, so every Q-edge face owner occurs in one fixed
parity class of that six-step walk.

In the bowtie, the degree-four shared vertex occurs twice but has only
one Q neighbour, impossible. A diamond leaf attached at a degree-three
diamond vertex has the same defect. In the only remaining type, let C
be the leaf attachment, E the leaf, A,B the diamond's shared-edge
vertices and D the other degree-two diamond vertex. The actual walk is

    C,E,C,A,D,B.

E needs four Q neighbours, while D needs three; each occurs once, so
both must own a Q edge. They occur at opposite walk parities, impossible.
The checker exhausts all 135 labelled cores (15 bowties, 60 attachments
at shared diamond vertices, 60 at outer diamond vertices), preserving
all repeated exterior-walk occurrences. This is an independent finite
calibration of the local i=5 exclusion. The general theorem in sections 2--4 permits arbitrarily many interior
vertices of either parity and arbitrary excess, and uses the actual
source exterior and original sectors.

## 6. Exact authority boundary

The seven-cut obstruction is excluded on the same original source, with
its same colour frame, all complete fibres including empties, and every
r lift. The full-excess inequality makes no bound on interior size or
degree. The filling operation recognizes an existing four-cycle; it
constructs no replacement source or descent measure.

The consequence for ordinary 101 existence is obtained only after
combining this impossibility with the previously proved exhaustive
Tutte-barrier reduction; that deduction and its exact dependencies belong
to the main proof of this audit. This geometry result alone does not
claim even-complement positivity, W110+W101>0, complete319 exclusion or
the general K_infinity=K_<=5 statement. Those stronger obligations remain
separate. The full tight signature registry and all original fibres
are retained; no signature cell is discarded by a marginal argument.

No external theorem, new Lean theorem, commit or push is used here.
