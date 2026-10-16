# R6-JOINT-ZERO C: original-sector restrictions and complete hub lifts

Frozen BASE: `c4c3d99`. Fix the original globally minimum noncatalogue
C5 source, its secondary maximum-edge choice, and
`d_G(x)=d_G(y)=d_G(b)=4`, `d_G(r)=6`. All names, rotations and retained
edges are those of the legal construction `J=U/(s=t)`, `m=[s=t]`.
The two specified faces are `mvw`, `zpq`; `mz` is retained. The actual
embedded cubic dual is `D=J*`.

The arbitrary-size new result here is the original-sector restriction on
cyclic four-edge cuts, in C2--C3. The complete hub criterion and guaranteed
starting colouring in C4--C5 are supporting consequences of already
proved statements. None proves `W110+W101>0`.

## C1. Literal sectors and the exact small-cap premise

All J vertices other than m,z are original G inner vertices. Define four
sets using the original edges, with the identified vertices excluded:

* `L_s={u in V(J)-{m,z}: su in E(U)}`;
* `L_t={u in V(J)-{m,z}: tu in E(U)}`;
* `L_a={u in V(J)-{m,z}: au in E(G)}`;
* `L_c={u in V(J)-{m,z}: cu in E(G)}`.

The frozen source construction proves the disjoint decompositions

`N_J(m)-{z}=L_s disjoint-union L_t`,
`N_J(z)-{m}=L_a disjoint-union L_c`.

The first follows from `N_U(s) intersect N_U(t)={z}`. The second uses
the original rule that an inner vertex cannot meet both nonadjacent
boundary vertices a,c. These sets are consecutive original fan sectors,
not independently selected parts of a link cycle. The common-neighbour
identities additionally give

`L_t intersect L_a={alpha}`, `L_s intersect L_c={beta}`,
`L_s intersect L_a=L_t intersect L_c=empty`.

The original source theorem says **every proper original G C4 has empty
bounded cap**. It applies also when that cycle meets the original outer
boundary. This scope is stated in frozen SOURCE_GEOMETRY section 1 and
used there in section 2 for cycles such as `r-y-a-p-r`. Its underlying
authority is frozen `w5/PROOF.md`, sections 3--4. Since every original
bounded face is triangular, such an empty C4 has a diagonal. We use this
original cap theorem, not four-connectivity alone.

## C2. Induced C4s must cross the original sectors

**Theorem C.** Every induced four-cycle Q in this same J satisfies exactly
one of the following geometric cases:

1. If `m in Q`, `z notin Q`, the two Q-neighbours of m lie one in L_s
   and one in L_t.
2. If `z in Q`, `m notin Q`, the two Q-neighbours of z lie one in L_a
   and one in L_c.
3. If both m,z are in Q, then Q uses mz and has order `m,z,u,v`.
   Its remaining vertices obey either `(u in L_a, v in L_s)` or
   `(u in L_c, v in L_t)`.

In particular the compatible old sectors `(L_a,L_t)` and `(L_c,L_s)`
are impossible in case 3. No induced Q avoids both m,z, by the frozen
source geometry theorem.

**Proof.** In case 1 write `Q=m,u,v,w,m`. If u,w both lie in L_s,
the literal original cycle `s,u,v,w,s` is a proper G C4. Its required
diagonal is either uw or sv. The first survives as uw in J; the second
survives as mv. Either is a chord of Q. The same proof applies when
both lie in L_t. Their unique sector membership leaves only opposite
sectors. No vertex of this lifted cycle is r, a collapsed boundary
vertex, or the other one of s,t.

In case 2 write `Q=z,u,v,w,z`. If u,w both lie in L_a, use the literal
original cycle `a,u,v,w,a`. Its required diagonal uw or av survives as
uw or zv, again a chord. This cycle has just one original boundary
vertex, a, which is permitted by C1. The c case is identical.

If Q contains both m,z, their retained edge is a chord unless it is a
cycle edge. Thus write `Q=m,z,u,v,m`. The absence of the two Q chords
also gives `mu,zv notin E(J)`. If `u in L_a` and `v in L_t`, the literal
original cycle is `t,a,u,v,t`, using the original edge ta. Its diagonal
tu or av would survive as mu or zv. Both are forbidden by inducedness,
contradicting the empty-cap theorem. If `u in L_c`, `v in L_s`, use
`s,c,u,v,s` and the original edge sc. The two disjoint sector
decompositions leave exactly the crossed alternatives stated above.
All lifted vertices are distinct, and every diagonal is retained by
the prescribed construction. QED.

This is a strict geometric refinement of the old localization
"every induced C4 meets m or z": it specifies which original sectors
each such cycle must cross. It excludes a whole arbitrary-size family
of candidate source separators without claiming that all crossed
separators are realizable.

## C3. The actual dual-cut consequence

Let delta_D(X) be a four-edge cut with cycles on both sides. Both sides
are connected: otherwise two distinct components of one side would
each have at least three outgoing edges, contradicting cut size four.
Thus the cut is a bond, and its primal image is a simple J C4. That C4
is induced. Indeed a chord would form two triangles, each facial by the
frozen four-connectivity proof, leaving one dual side as the two-vertex
tree of those faces, which cannot contain a cycle.

Theorem C therefore applies to every such actual cut. If it meets only
the dual face m, its two incident boundary edges must use opposite
original s/t sectors; the analogous statement at z uses a/c sectors.
If it meets both faces, it contains the original marked edge `g=mz*`,
and the two other incident cut edges have the crossed incidence in C2.3.
This restriction is available to either ordinary-matching obstruction
and to the positive-oddness branch on the same D. It asserts neither
that a cut exists nor that the surviving cut types cannot coexist.

## C4. Full hub criterion without a two-colour-path restriction

Let `W=J-{m,z}` be the exact two-star complementary disk, with its
retained paths P_m,P_z. For **each complete** proper W colouring chi set

`A_m={0,1,2,3} minus chi(V(P_m))`,
`A_z={0,1,2,3} minus chi(V(P_z))`,
`K(chi)={(a,b): a in A_m, b in A_z, a!=b}`,
`T(chi)={a XOR b: (a,b) in K(chi)}`.

Write `d_e=chi(v) XOR chi(w)`, `d_f=chi(p) XOR chi(q)`. The frozen
complete all-r theorem gives the exact necessary and sufficient
condition that **all** hub lifts of this one complete chi pass:

* if `d_e=d_f`, then `T(chi) subset-of {d_e}`;
* if `d_e!=d_f`, then `d_e notin T(chi)`.

Every empty K is retained and passes vacuously. For nonempty K, any
failure gives a literal pair (a,b), hence a complete J colouring and
its unique r lift, on the same original graph and in the same colour
frame. This is simply the complete FJ formula with its quantifiers
retained; it introduces no extra premise about the path palettes or
the parity of hub degrees. In particular a violating fibre need not
have `|A_m|=|A_z|=2`.

The special distinct-size-two missing-palette witness remains confined
to even/even hub degrees, as the frozen proof established. It is not
used as a premise of Theorem C or as the general witness obligation.

## C5. A guaranteed complete all-equal starting state

The frozen exact outer support `Sigma(U)=319` contains the row
`(z,s,v,w,t)=(A,B,C,D,B)`. Its presence means at least one complete U
colouring with that literal row exists; it is not an independent
boundary assignment. Since s=t, it descends to a complete J colouring
with `m=B,z=A,v=C,w=D`. The full all-r row forces `{p,q}={C,D}`.
Consequently its three specified differences satisfy `d_e=d_f=d_g`.

For the orientation `p=C,q=D`, every such complete colouring has these
two actual primal Kempe connections:

`m--p in {B,C}`, `m--q in {B,D}`.

For example m,v are joined by their original BC edge. If p were in
another BC component, switch just that component. It changes p from C
to B while z=A and q=D remain fixed. The new pq difference differs
from the unchanged common e=g difference, violating FJ. Thus m and p
are connected. The m--q proof is the BD version. Exchange p,q in these
statements when their colours are reversed. This agrees with
the frozen requirement that f,g belong to one dual two-colour cycle
in each of the two relevant Tait pairs. No stronger unproved primal
linkage is supplied to A or B.

In particular the superficially symmetric requirements `z--v in AC`
and `z--w in AD` do not follow by this argument: a separate v component
could be switched from C to A, changing e while f=g stay fixed, which
produces the allowed type `f=g!=e`. The distinguished role of e cannot
be silently symmetrized.

Also both hubs individually have no alternative legal colour while all
other J vertices are fixed: if m or z could be recoloured, g would
change while the equal e,f remained fixed, violating FJ. This is a
consequence in a guaranteed colouring, not a claim that every W fibre
is nonempty or that the joint family has an even-complement member.

## C6. Scope and verification

Theorem C is a new arbitrary-size source separator restriction. The
complete lift criterion and guaranteed starting state are support for
the joint target; they do not establish a new positivity theorem.
The full target, positive minimum oddness case, source exclusion and
general `K_infinity=K_<=5` remain OPEN. The general finite bound remains
`K_<=22=K_<=5`; the fixed branch retains its existing conditional
`k>=25`. No source deletion/reconnection or strict descent is claimed;
reconstruction through W/J still costs k+5 total source vertices.

The local checker independently verifies the full hub-difference
criterion against direct original r-lift rules for every proper local
row, including all possible missing-colour sets compatible with the
same complete-path endpoint colours. Its role is finite interface
calibration; the original cap and sector theorem are paper results.
Actual minimum sources supplied: zero, `not triggered`. No external
theorem, 4CT invocation, new Lean theorem, commit or push is introduced.
