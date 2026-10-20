# A. The active-f seven-cap has no additional contact with m

Frozen BASE: `3d325d7197aa05815c71bedc52c1b253d736c7bb`.
This is an arbitrary-size paper exclusion in the original completed-source
contract. It uses an ordinary `101` matching, with no minimum-oddness,
two-complement-cycle, or reference-colouring assumption.

## 1. One source, one disk, and adopted facts

Keep the same globally minimum completed no4ct C5 source G, its secondary
maximum-edge choice, ordered boundary `(x,y,a,b,c)`, original apexes
`(r,t,p,q,s)`, actual attachments, private vertices and rotations. In the
fixed r=6 branch, retain the complete U319 relation in the literal order
`(z,s,v,w,t,p,q)`, including empty complete fibres and every original r
lift. The actual graphs are `J=U/(s=t)`, `m=[s=t]`, and `D=J*`; the literal
dual marks are `e=(vw)*`, `f=(pq)*`, `g=(mz)*`. No extra hypothesis on the
original degree of v is introduced.

Take any actual perfect matching `M in P101`, so `e,g in M` and `f not in M`.
Suppose `D-M` has a nonfacial complete seven-cycle C containing f. Set
`X=V(C)`. The frozen [active-f geometry](../frozen/audits/2026-10-17-r6-active-f-seven-ffea555/B/PROOF.md)
gives an actual two-star closed disk K with interior centres u,h, where
`u in {p,q}` has J degree four and h has unchanged original/J degree five.
Its actual boundary Q5 is induced; its five edges are exactly the primal
images of the five spokes `delta_D(X) subseteq M`. Every J triangle is an
actual face. The disk contains precisely its two centres and five rim
vertices, and

`V(Q5) intersect {m,z,v,w} = {z}`,

`E_J({u,h},{m,v,w}) = empty`.

The adopted original small-cap theorem is [no4ct cap §3](../frozen/audits/2026-10-13-c5-no4ct-frontier-6943561/w5/PROOF.md):
every original C4 has empty bounded interior, and every proper original
C5 has empty bounded interior or exactly one full W5 centre. In
particular an induced original C4 is impossible, and an induced proper
original C5 has the full W5 cap. Its strict smaller-source hypotheses
are already proved in that authority; no universal C4-representative
statement or Four Colour Theorem is substituted here.

We use the [compatible C5 classification C1.4](../frozen/audits/2026-10-16-r6-319-continuation-f1faf74/C/PROOF.md)
and the original [low-p/q degree theorem](../frozen/audits/2026-10-14-lowpq-source-676b102/pq/PROOF.md):

`d_G(p)=5 => d_G(a)>=6`,

`d_G(q)=5 => d_G(c)>=6`.

The four graph nonedges `ell-s,ell-t,n-s,n-t` on the low-p side are
retained together exactly as justified in the frozen active-f proof §2.
They are universal graph consequences for this same G, proved using
separately existing complete colourings. Their assignments are never
joined into one colouring. Reflection retains the corresponding four
nonedges for `ell_q,n_c`. The present proof constructs no new colouring.

To prevent the old notation collision, n below is the original private
vertex called m in the old low-p paper; it is distinct from the quotient
hub `m=[s=t]`. Write `alpha0,beta0` for the old alpha,beta: the literal
original face apexes on `ta,sc`, respectively. In J, m and z have exactly
these two common neighbours. The notation does not introduce new pins.

## 2. The two rim neighbours of z cannot meet m

For any rim edge `zu in E(Q5)`, its dual `(zu)*` is one of the five
matching spokes. If `mu` were an edge, the triangle mzu would be an
actual J face. Its dual vertex would be incident with the two distinct
matching edges `g=(mz)*` and `(zu)*`. Therefore

`zu in E(Q5) => mu not in E(J)`.                         (A1)

This argument uses the same matching M as the seven-cap. It does not
select a reference matching or a colour class.

## 3. The p,ell case: both private contacts are impossible

Here the full original links and the actual rim are

`N_G(p)=(a,b,q,ell,n)`,

`N_G(ell)=(p,q,u1,u2,n)`,

`Q5=(z,q,u1,u2,n)`.

All entries are distinct actual original vertices, except for the stated
quotient z. In particular `d_G(p)=d_G(ell)=5`, `a0>=6`, `c0>=5`.
The frozen source nonedges give `mp,mell,mn` absent; (A1) gives mq absent.
Only `mu1,mu2` remain. A retained neighbour of m comes from exactly one
of its original disjoint sectors `L_s,L_t`, so each putative contact has
the indicated original s-side or t-side lift.

The induced Q5 excludes its chords `zu1,zu2,qu2,qn,u1n`. The induced
complete p link also excludes zell in J. A nonedge `zu_i` means both
original `au_i,cu_i` are absent; zell similarly excludes both aell,cell.
These statements concern ordinary retained vertices, so no lost boundary
edge or independently chosen lift is involved.

### 3.1. Contact mu1

If it comes from s, the original cycle `(s,c,q,u1)` is induced. Its two
diagonals sq and cu1 are absent: sq follows from mq and cu1 from zu1.
This contradicts the original empty-C4 theorem. Thus a contact mu1 must
come from t.

In that event the original proper five-cycle

`(t,a,n,ell,u1)`                                       (A2)

has all five actual edges. Its five possible chords are absent:

| chord | reason |
| --- | --- |
| tn | original low-p nonedge |
| tell | original low-p nonedge |
| aell | zell is absent in the induced J p link |
| au1 | zu1 is an absent Q5 chord |
| nu1 | nu1 is an absent Q5 chord |

Hence (A2) is induced. Its compatible lift is the J cycle
`(m,z,n,ell,u1)`, with n in the original a sector and u1 in the t sector.
The actual face on ta inside its cap is `ta alpha0`, so the original
cap centre is exactly alpha0, as in C1.4. It has all five spokes and the
five actual triangular cap faces. In particular the new faces include
`(n,ell,alpha0)` and `(n,alpha0,a)`.

The original p link already supplies `(a,n,p)` and `(p,n,ell)`.
At the original interior vertex n these four actual triangular faces
give the closed link

`N_G(n)=(a,p,ell,alpha0)`.

The link of an original interior vertex is one simple circle; the
displayed closed four-edge subcircle leaves no further neighbour slot.
Thus its complete original degree is four, contradicting the original
inner-degree lower bound five. Contact mu1 is impossible.

### 3.2. Contact mu2

If it comes from t, the original C4 `(t,a,n,u2)` is induced: its only
diagonals tn and au2 are absent by the source nonedge and the Q5 chord
zu2. Hence it cannot occur.

If it comes from s, the original proper C5

`(s,c,q,ell,u2)`                                       (A3)

is induced. Its five chords and reasons are

| chord | reason |
| --- | --- |
| sq | mq is absent by (A1) |
| sell | original low-p nonedge |
| cell | zell is absent in the induced J p link |
| cu2 | zu2 is an absent Q5 chord |
| qu2 | qu2 is an absent Q5 chord |

This is the compatible original sc lift. The unique full W5 cap centre
is the literal beta0. Its faces include `(c,q,beta0)`, `(q,ell,beta0)`,
and `(s,c,beta0)`. The old facial sectors give `(c,b,q)`, `(b,p,q)`,
`(p,ell,q)` and `(x,c,s)`. Consequently the complete interior link and
complete boundary link, respectively, are

`N_G(q)=(c,b,p,ell,beta0)`,

`N_G(c)=(x,s,beta0,q,b)`.

For q the displayed triangles close its entire circular link. For the
boundary vertex c they fill the entire interior link path between its
two boundary neighbours x,b. Thus `d_G(q)=d_G(c)=5`, contradicting
`d_G(q)=5 => d_G(c)>=6`. Contact mu2 is impossible.

## 4. The p,n case: the one remaining private contact is impossible

Here the unchanged original five-degree centre has links

`N_G(n)=(p,ell,u1,u2,a)`,

`N_J(n)=(p,ell,u1,u2,z)`,

and the actual induced rim is `Q5=(z,q,ell,u1,u2)`.
The original edge na is the source of its J edge nz; no original nz
edge is fabricated. The known centre nonedges exclude mp,mn, and the
same original low-p nonedges exclude mell. By (A1), mq and mu2 are
absent. Only mu1 remains.

If it comes from t, `(t,a,n,u1)` is an original induced C4: tn is a
source nonedge and au1 is absent because zu1 is a Q5 chord. If it comes
from s, the original proper cycle `(s,c,q,ell,u1)` is induced. Its
possible chords are sq, sell, cell, cu1, qu1. These are absent,
respectively, by (A1), the source nonedge, and the three Q5 nonedges
zell,zu1,qu1. Its compatible full star centre is beta0. Exactly the
same actual facial list as in §3.2 closes

`N_G(q)=(c,b,p,ell,beta0)`,

`N_G(c)=(x,s,beta0,q,b)`.

Again q and c both have complete original degree five, contradicting
the low-q theorem. Thus mu1 is impossible in this centre position too.

## 5. Both q-centred positions in the same source

Apply the literal whole-source relabelling

`(x,y),(a,c),(p,q),(s,t),(v,w),(alpha0,beta0)`.

It fixes m,z, sends the original private n to n_c, and sends ell to the
literal other pq-face vertex ell_q. It transports all edges, nonedges,
original sectors, full source fibres and r lifts together; it is not an
assertion that G has an automorphism or that two independent witnesses
can be spliced. The q-side theorem applies universally to the relabelled
description of this same source. For clarity, all its residual cases are:

| centres and rim | contact and original side | impossible induced C4, or forced compatible C5 and complete links |
| --- | --- | --- |
| `q,ell_q`; `(z,p,u1',u2',n_c)` | `mu1'` from t | C4 `(t,a,p,u1')`; diagonals tp,au1' are absent |
| same | `mu1'` from s | C5 `(s,c,n_c,ell_q,u1')` forces beta0; `N_G(n_c)=(c,q,ell_q,beta0)`, degree four |
| same | `mu2'` from s | C4 `(s,c,n_c,u2')`; diagonals sn_c,cu2' are absent |
| same | `mu2'` from t | C5 `(t,a,p,ell_q,u2')` forces alpha0; `N_G(p)=(a,b,q,ell_q,alpha0)`, `N_G(a)=(y,t,alpha0,p,b)` |
| `q,n_c`; `(z,p,ell_q,u1',u2')` | `mu1'` from s | C4 `(s,c,n_c,u1')`; diagonals sn_c,cu1' are absent |
| same | `mu1'` from t | C5 `(t,a,p,ell_q,u1')` forces alpha0 and the same complete p and a links |

Each five-cycle's chord list is exactly the literal image of the five
listed in §§3–4. In the first forced-star row n_c is an original
interior vertex of complete degree four. In the latter two rows the
complete links give `d_G(p)=d_G(a)=5`, contradicting the low-p theorem.
All other rim contacts are already excluded by (A1) or the reflected
source nonedges. Centre contacts with m were excluded in the adopted
active-f geometry. This accounts for all four possible centre positions.

## 6. Cap–m exclusion and the entire m-face distance

Combining the four positions with §2 gives the arbitrary-size conclusion

`N_J(m) intersect V(K) = {z}`.                          (G)

The inclusion of z is literal: mz is the retained marked primal edge.
No other cap centre or rim vertex can be adjacent to m.

Let `partial F_m` be the actual D face boundary dual to the primal vertex
m. Its dual vertices are precisely the primal triangular faces containing
m. No such face belongs to X, because every face in K avoids m. If such
a dual vertex had a neighbour in X, their primal triangles would share
a rim edge uv of K. The exterior triangle containing m would then be
the actual face muv. Thus both distinct endpoints u,v of that rim edge
would belong to `N_J(m) intersect V(K)`. By (G) that set is the singleton
{z}, a contradiction. Therefore

`dist_D(X,V(partial F_m)) >= 2`.                        (G2)

This concerns the full m-face, strengthening the previous statement
only about endpoints of g. It is a full-dual distance assertion; it
does not separate components after arbitrary more distant connections.

## 7. Authority and remaining boundary

The proof excludes every additional cap–m contact in the stated
arbitrary-size original source. It requires neither two complete
complement cycles, minimum oddness, a chosen reference R, nor a chosen
actual full colouring. Original small-cap, full-link and low-degree
theorems supply the contradiction. No independent palette witnesses
or projected matching fibres are combined.

No finite control is needed to establish these purely original-source
link contradictions, and none is presented as source coverage. The
frozen authority files are verified separately in [input-check.json](input-check.json).
No genuine target source is supplied: source realization is **not
triggered**. No new Lean theorem is claimed. (G2) alone does not prove
SEP. The remaining active-f seven-caps, the actual two-cycle matching
repair, other odd components, H-connected residuals,
`W110+W101>0`, even-complement positivity, and complete319 stay **OPEN**.
