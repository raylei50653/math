# Final structural attempt: exact same-direction transport and its obstruction

The sealed A proof, checker, certificate and receipts are unchanged. This
attempt uses the new actual all-distinct J witnesses, the frozen full
source return rule FJ, and the additional old common-neighbour identities
now frozen by root. It does not claim a further source exclusion.

## 1. A genuine same-direction partial bijection

Use three distinct literal colours A,B,C, with D the fourth. Let u be
one of the original p,q and let d be the other. Define E_v(u) to be all
complete colourings of the **same original J**, with

`m=u=C`, `z=v=A`, `w=d=B`.

Define E_w(u) by

`m=u=C`, `z=w=A`, `v=d=B`.

Both are full all-distinct sectors. Their individual complete fibres may
be empty. In either sector the actual edges vw and zd are AB edges.
Let E_v^sep(u), E_w^sep(u) denote the full subfibres where those two
edges belong to different maximal AB components.

**Lemma.** There is a literal full-colouring bijection

`E_v^sep(u) <--> E_w^sep(u)`.

It interchanges A,B on the entire maximal AB component containing vw.
Because zd lies in another component, z and d do not change. Neither
m nor u has an AB colour, so they also stay fixed. The two rim colours
are interchanged, giving the stated other sector with exactly the same
equality direction m=u. Every original edge and private vertex is
retained. The maximal AB vertex sets do not change under this exchange,
so the separated condition persists and the same operation is its
inverse. The original r lift remains exactly D.

Consequently the counts of these **separated** full subfibres agree.
It does not follow that the unrestricted E_v(u),E_w(u) counts agree.

If vw and zd lie in one AB component, every AB-component exchange
either changes none of the marked vertices, or changes z together with
both v,w and d. In the latter case z retains its equality with the same
rim endpoint. Thus the entire AB exchange cube preserves the v/w sector
in this connected case. It cannot supply the missing transport.

The old exact identity

`N_J(z) intersect N_J(v) = N_J(z) intersect N_J(w) = {m}`

does not prohibit that connected AB component. For example an AB path
from z=A to the equal-coloured rim endpoint has length at least four:
a two-edge path would have a common B neighbour, while the sole common
neighbour m has colour C. Arbitrarily long such paths are not ruled out
by the common-neighbour identity or C3's short-cut restriction.

## 2. What actual quotient extension now supplies

The new theorem guarantees E_v(p) union E_v(q) nonempty, and independently
E_w(p) union E_w(q) nonempty. If a0=4, mp is an edge, so E_v(p),E_w(p)
are empty and both guaranteed witnesses have u=q. If c0=4, the reflected
statement forces u=p. When both degrees exceed four, the two guaranteed
witnesses can in principle use different equality directions. If a
guaranteed witness lies in a separated subfibre, the lemma supplies
both outer orientations in its own direction. A source avoiding that
conclusion must put every relevant one-direction witness in the actual
connected AB case; no proof excludes that case here.

Fix one such actual colouring in E_v(u), and delete z. Its complete
base colouring of the defined H_u has a nonempty actual z fibre. The
previous-round exact all-r restriction now makes this fibre precisely
the singleton `{A}`: the unmerged pq endpoint d has colour B=w and the
only allowed z colour is A=v. In E_w(u) the same statement holds with
v,w interchanged. Hence the new witness overcomes the old possibility
that every base fibre is empty, while still occupying exactly the
previously permitted singleton case.

In particular the full original z-link uses all three colours B,C,D:
m and u supply C, d supplies B, and some actual additional fan vertex
supplies D. Recolouring z to D would yield the forbidden equality
`e=g!=f`, so the D fan vertex is an actual locking obstruction, not an
omitted empty row. If a0=4, that D vertex lies in the long original c
fan, since the short a fan ends immediately at alpha=p; the reflected
statement holds when c0=4. Neither fan's length or old short-cycle
restriction has been shown to eliminate such a vertex.

The two actual outer-sector witnesses are not two possible z lifts
over one fixed full H_u colouring. Their original v,w assignments
already differ, and their private colourings may differ as well.
Their missing-colour sets therefore cannot be united to create a
two-colour z fibre. The exact same-direction bijection above transports
one entire colouring when its component condition holds, but still
transports an allowed singleton fibre to an allowed singleton fibre.

## 3. Precise endpoint

The source now supplies full all-distinct witnesses and positive
W010/W001, plus at least one genuinely extending equality quotient.
This attempt has not converted one into a forbidden full lift. A real
next step would have to eliminate the connected AB obstruction using
additional original-source geometry, or construct one full quotient
colouring whose actual missing-colour fibre violates its allowed
singleton rule. Paths or missing colours from independently feasible
complete colourings cannot be joined for that purpose.

All operations here remain on the same J; they supply no smaller bad
source. Completion still returns total k+5. Target `W110+W101>0`, full
319 exclusion and the main theorem remain OPEN. Actual minimum-source
checking remains **not triggered**; no new external or Lean theorem is
used.

## 4. Final independent C review

The final C/MARKED_CUTS.md and revised C2 ear argument were independently
reviewed. The existential zpq ear is justified, including the alternative
three-face pentagon tree when neither zp nor zq is a cycle edge. The
induced C4 core then requires mq and zA absent; the exact common-neighbour
formula leaves only repeated z/p or the j_c vertex adjacent to z, all
excluded. Reflection handles the other orientation. The crossed-star
exception alpha=p or beta=q correctly retains original degree6 and J
degree5. C/check.py (active v2) and C/check_marked_cuts.py both replayed
successfully. C3 is accepted as a same-source restriction, with no claim
that it repairs long odd complement cycles.
