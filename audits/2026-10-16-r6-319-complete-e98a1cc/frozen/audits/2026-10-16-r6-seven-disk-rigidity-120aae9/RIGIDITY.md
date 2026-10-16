# Five odd interior vertices are impossible in the same source

Research BASE `120aae90cab8bc4881916adc598cf344f2f20f4b`.
This is an arbitrary-size paper proof for the literal seven-cut disk of
the [preceding theorem](../2026-10-16-r6-101-nonwheel-seven-cut-120aae9/PROOF.md).
It preserves that same `G,J,D,S,C`, all actual edges and rotations,
all complete fibres including empty ones, and every original lift.
No graph, barrier, or colouring relation is replaced.

The result is the whole unbounded exclusion `I=5`, where I counts odd
complete-degree vertices strictly inside the disk. The number of even
interior vertices is arbitrary. Together with the preceding theorem,
this gives `I>=6` and `|C|>=17`. It does not prove ordinary 101 matching
existence or exclude every surviving seven-port disk.

## 1. Exact inputs

Use the preceding proof's actual closed triangulated disk R, with simple
seven-cycle boundary Q and no Q chord on the R side. Its face set is C.
Its interior avoids the six distinct vertices

`T0={m,z,v,w,p,q}`.

All J triangles are actual faces. Every induced J four-cycle meets m or
z, and obeys the exact original-sector restrictions of
[C2](../2026-10-16-r6-joint-zero-c4c3d99/C/PROOF.md):

* with m alone its rays lie in opposite `L_s,L_t` sectors;
* with z alone its rays lie in opposite `L_a,L_c` sectors;
* with both hubs it has order `m,z,u,v`, and the other two rays have
  `(u in L_a,v in L_s)` or `(u in L_c,v in L_t)`.

The actual link of m comprises its original s path, edge vw and original
t path; the actual link of z comprises its a path, edge pq and original
c path. Their common faces are `mz alpha,mz beta`, with

`alpha in L_t intersection L_a`, `beta in L_s intersection L_c`.

Let d denote the third vertex of the actual other vw face. The four
forced zero faces are

`X={mvw,dvw,mz alpha,mz beta}`.

Give `S union X` faces bit zero, and every residual odd-component face
bit one. The complete monochromatic primal edge set is exactly

`{vw,pq,mz} union {the nonboundary edges of R}`.                (1)

In particular all C faces have bit one, while `zpq` has bit one: both
endpoints of f avoid S and X. The original degree formulas are

`d_J(m)=d_G(s)+d_G(t)-5`, `d_G(s),d_G(t)>=6`,

`d_J(z)=d_G(a)+d_G(c)-5`, `d_G(a),d_G(c)>=4`.

For boundary u, `t_u>=1` is its number of strictly interior neighbours,
and `d_R(u)=2+t_u`. Let B count odd t_u and let epsilon be one exactly
when m belongs to Q and t_m is odd. The preceding proof gives

`Delta=I+B-2 epsilon-10`, `Delta>=2(1-epsilon)`.                (2)

Here Delta is the sum of nonnegative even excesses over the exact
parity-dependent degree minima in the preceding proof. These are
arbitrary-size same-source facts, not finite controls.

## 2. Equality forces three ordinary exterior ears

Assume `I=5`. Equation (2) gives `B>=7`, so

`B=7`, `Delta=2(1-epsilon)`.                                 (3)

Thus every t_u is odd. The m-sector bound uses all available excess:
if m is absent, the two original sector equations force both original
s,t degrees odd and at least seven, so m alone contributes at least two.
If m is present, epsilon is one and Delta is zero. Consequently every
non-m vertex attains its parity-dependent minimum.

The interior vertices therefore have complete degree five when odd and
six when even. The disk curvature identity, obtained by substituting
`E_ii+E_ib=3i+4` into the sum of interior degrees, is

`sum_{u in Q} t_u=8+sum_{a interior}(6-d_J(a))=13`.            (4)

A generic boundary vertex, outside T0, has odd complete degree five.
Any of v,w,p,q on Q has even complete degree four. Any boundary z has
even complete degree six.

**The face zpq is outside R.** If it belonged to C, all three of its
vertices would have to lie on Q, since none can be strictly interior.
Every edge of that triangle would then be a Q edge: an edge between Q
vertices on the R side cannot be a chord. A seven-cycle contains no
triangle. This proves the assertion without assuming where f crosses.

If m belongs to Q, its complete even degree is eight. Hence its original
degrees are six and seven. The sector containing C obeys the exact word
equation

`d_G(u)-3=2k+t_m+2`, `u in {s,t}`.                           (5)

Since t_m is odd, that sector has even original degree, hence degree
six. Equation (5) becomes `3=2k+t_m+2`, forcing `t_m=1`.

If z belongs to Q, its complete degree is six. Hence its positive odd
t_z is one or three. If it were three, its R interval would contain
four faces, leaving exactly two exterior faces at z. Both mz faces
are exterior, as is the distinct face zpq just proved outside R. This
is impossible. Thus `t_z=1`, without an h=3 classification or extra
fan calculation.

For any of v,w,p,q on Q, `2+t_u<=4` and t_u is positive odd, giving
`t_u=1`. For an ordinary boundary vertex `2+t_u<=5`, so t_u is one
or three. Equation (4) consequently forces exactly THREE ordinary
vertices with t_u three; all four other Q vertices have t_u one.

At such an ordinary vertex u, its complete degree five equals d_R(u).
Its R face interval contains four faces; the one remaining face is the
actual exterior triangular ear

`F_u=(u_-,u,u_+)`,

where u_-,u_+ are its Q neighbours. Two such vertices cannot be adjacent:
their exterior faces on the common Q edge would have to coincide, which
would identify two distinct vertices of the simple seven-cycle. Thus
the three ear centres are pairwise nonadjacent.

Attach these three actual exterior faces to R. The result R4 is a
closed disk whose boundary Q4 is the simple four-cycle obtained by
deleting the three nonadjacent ear centres from the Q word and adding
their exterior chords. The old ear centres become interior; no other
vertices change from boundary to interior. All six T0 vertices remain
on or outside Q4.

Each added ear has bit zero. Its two old Q edges are incident with its
ordinary centre, so neither is pq. Their C sides have bit one; (1)
therefore makes the other face zero. In particular none of the added
ears is zpq, and zpq is outside R4.

## 3. The compressed four-cycle is induced

Suppose Q4 had a chord. Its two resulting triangles are actual faces.
The R4 side has at least the fifteen faces of C and the three added
ears; it cannot be the two-triangle side. Consequently the opposite
side must be exactly the two actual triangular faces, and it has no
strictly interior vertex.

But all six distinct T0 vertices are on or outside Q4, while that
exterior has no interior vertex. This would put six distinct vertices
on four boundary positions. Hence Q4 is induced.

This argument permits added ears in X. It neither assumes all forced
faces stay outside R4 nor discards boundary chords of the original Q.

## 4. Which forced faces can have been filled

The marked edge of an added X ear must be its new chord, because both
other edges are old Q edges with C on the R side. Its ear centre is
ordinary, so mvw is never an added ear. The only possible e ear is dvw,
centred at d, and the only possible g ears are `mz alpha,mz beta`,
centred at alpha or beta respectively. If one of these named centres
is in T0, that possibility is automatically absent.

Both g faces cannot be ears. That would put both paths `m,alpha,z` and
`m,beta,z` on Q, using the two Q neighbours of both m and z and closing
a four-cycle inside the simple seven-cycle. Thus the exhaustive cases
are: no X ear, only e, only one g, or both e and one g.

### No X ear

R4 avoids all four forced faces. If Q4 avoids m,z, it violates source
C2. If it meets both, inducedness makes mz a Q4 edge, but neither of
its actual faces is in R4. If it meets m alone, its R4 interval avoids
mvw and both mz faces, so its two rays are in the same original s/t
sector, again violating C2. If it meets z alone, C2 requires opposite
a/c rays. The R4 interval avoids both mz faces and must therefore
contain zpq. That face was proved outside R4. All possibilities fail.

### Only the e ear

The new boundary contains vw. It cannot also contain m: an induced
four-cycle cannot contain the actual triangle mvw. If it avoids z as
well, C2 already fails. Otherwise z is its only hub, and the preceding
opposite-fan argument applies because both mz faces remain outside R4.
It again wrongly puts zpq in R4.

### Only one g ear

Suppose first the ear is `mz alpha`. The boundary Q4 contains mz, and
has order `m,z,u,v`. At m, the R4 side of mz is the side through alpha.
Its interval avoids mvw and the other mz face; hence its other ray v
lies in the original t sector L_t. The exact both-hub C2 restriction
then forces `u in L_c`.

At z the same R4 interval starts from m through alpha in L_a and ends
at u in L_c. It avoids the other mz face. In the literal z link the
route from L_a to L_c avoiding m passes through the face zpq. Thus
zpq belongs to R4, the same contradiction as before.

For the ear `mz beta`, exchange `(alpha,L_t,L_a)` with
`(beta,L_s,L_c)`. The m ray lies in L_s, the source theorem forces the
other z ray into L_a, and the R4 interval again passes through zpq.

### Both an e ear and a g ear

The four distinct surviving endpoints m,z,v,w occupy all four Q4
positions. The triangle mvw then contradicts inducedness. This last
case is impossible independently of the sectors.

All cases contradict the same source. Therefore `I=5` is impossible.

## 5. Scope

The old theorem excluded every source obstruction with at most four
odd interior vertices; this proof excludes five. Even interior vertices
were never counted or bounded. The resulting arbitrary-size necessary
condition is

`I>=6`, `i>=6`, `|C|=2i+5>=17`.

The 420 tight matching-signature bound, the complete port fibres and
their empty cells, all matching and Tait lifts, the original all-r
condition, and the same exterior D-C are retained verbatim. Filling
faces above is a geometric examination of the same J; it is not a
source replacement, and no reconstruction/descent is claimed.

No source realization, external theorem, Lean theorem, ordinary 101
existence, even-complement positivity, complete319 exclusion, commit
or push follows from this proof. The remaining case has at least six
odd interior vertices and remains OPEN.
