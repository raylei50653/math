# R6-DOUBLE-W5-101: no double-W5 maximum barrier in the original source

2026-10-16. Research BASE `0b639cf5ffd57e8e394add4e0b56cd60cc2ce38c`.
All previous audits are read-only; [BASE.json](BASE.json) records their
424 original file hashes and the frozen authority inputs used here.

## 1. Contract, dependencies and theorem

Retain one original globally minimum noncatalogue no4ct C5 disk G,
secondary maximum edge count, ordered boundary `(x,y,a,b,c)`, original
`d_G(x)=d_G(y)=d_G(b)=4`, `d_G(r)=6`, the legal retained-edge sphere
`J=U/(s=t)`, `m=[s=t]`, its actual spherical dual D, and literal edges
`e=(vw)*`, `f=(pq)*`, `g=(mz)*`. Put

`X=V(e) union V(g)`, `H=D-X-f`.

Choose ANY maximum-cardinality Tutte-violating set S of H and suppose
it has two complete W5 components C1,C2. Write ci for their original
degree-five centres, Ri for their complete induced rims, and
`Ki={ci} union Ri`. All other components are singletons. Every statement
below applies to this same graph and separately to every such S.

The adopted inputs are:

* [Source geometry](../2026-10-15-j-source-geometry-6ddea32/PROOF.md):
  every J triangle is facial; exact original sectors and degrees;
  `N(m) intersect N(z)={alpha,beta}`, `alpha beta` absent,
  `alpha=p iff d_G(a)=4`, `beta=q iff d_G(c)=4`, and `zv,zw` absent.
* [Five-cut theorem](../2026-10-16-r6-chorded-five-c4c3d99/PROOF.md):
  every 101 five-cut component is a retained original W5. Its independent
  reconstruction is [REVIEW-PRIOR.md](REVIEW-PRIOR.md).
* [Curvature A4](../2026-10-16-r6-cap-barriers-c4c3d99/A/PROOF.md):
  centres outside `T={m,z,v,w,p,q}`, distinct and nonadjacent;
  `r_cap=|K1 intersect K2|`,
  `epsilon=1` iff m belongs to exactly one Ki,
  `r_cap+epsilon<=1`, `Delta=2(1-r_cap-epsilon)`;
  `6<=d_G(s),d_G(t)<=8`, `3<=h=d_G(a)+d_G(c)-8<=6`.
* [Common-111 saturation B1](../2026-10-16-r6-cap-barriers-c4c3d99/B/PROOF.md):
  the entire family `P111={M perfect matching: e,f,g in M}` is nonempty;
  f joins different odd components, every such component has exactly one
  crossing in every M, and `E_D(S)=E_D(S,X)=empty` in the two-wheel row.
* [Original double-low theorem, section 5](../2026-10-14-c4-return-branches-a11d4bb/pq/PROOF.md):
  `d_G(p)=d_G(q)=5` forces original degree at least six at ell, the
  third vertex of the other pq face. It uses the full-fibre
  [return injection](../2026-10-14-c4-c5-recursion-fdd3e22/fibre/PROOF.md).
* [Lifted-pentagon theorem C1](../2026-10-16-r6-cap-barriers-c4c3d99/C/PROOF.md):
  an induced J C5 avoiding m,z, or meeting one hub with its two neighbours
  in the same original sector, has a retained original W5 on one side.
  This is an arbitrary-size original-cycle lifting theorem, not a census.

**Theorem (arbitrary-size source exclusion).** No maximum-cardinality
101 Tutte-violating barrier has two complete W5 components. Consequently,
under the adopted five-cut and previous singleton exclusions, ordinary
101 matching failure can only have a maximum barrier with one seven-cut
component which is not a complete W7.

The proof first obtains these necessary conditions on a hypothetical pair:

1. The dual face `zpq` is a singleton odd component.
2. `K1 intersect K2=empty`.
3. BOTH endpoints of f are singleton odd components. Neither p nor q
   lies on either rim, and `d_G(p)=d_G(q)=6`.
4. At least one wheel avoids ALL of T, and its centre and all five rim
   vertices have complete degree five. The optional intermediate seven
   sector types in sections 6--7 are all finally excluded by section 9.
5. The common nonempty P111 family simultaneously obeys the wheel tight
   cuts and the specified-edge restrictions in section 8.

Section 9 closes the contradiction by expanding that wheel's actual
second neighbourhood. It does not bound the private graph by enumeration.

## 2. The singleton face and the exact parity data

Both f endpoints avoid S and X by common-111 saturation. Every face of
a complete wheel contains its centre. All three vertices of zpq belong
to T, whereas both centres are outside T. Thus zpq is in neither wheel,
and it is a singleton odd component. This proves the proposed single-point
lemma without choosing a convenient matching or drawing.

Give bit zero to dual vertices in `S union X` and bit one to all the
components of `H-S`. The complete monochromatic primal-edge set is

`F*={vw,pq,mz} union {all spokes of both actual wheels}`.       (1)

Here vw,mz have two zero faces; pq and the spokes have two one faces.
All other edges have opposite face bits. In particular a one-one edge
between distinct residual components can only be pq. This uses both
`tau=1` and the zero remaining S budget, before any local word argument.

The initial three marked edges give odd parity at T and even parity
elsewhere. A wheel flips its centre and its five rim vertices. The
parity-sensitive degree minima are

| Vertex | Minimum J degree with parity o |
| --- | --- |
| m | `8-o` |
| z | `6+o` |
| v,w,p,q | `4+o` |
| every other vertex | `6-o` |

Delta is the sum of the nonnegative even excesses over these minima.
The exact formula above comes from Euler, without a colouring oracle.

No wheel rim contains both m,z: inducedness would make mz a rim edge,
but both of its incident faces are in X and neither is in a wheel.

## 3. The m sectors use all available degree excess

For u=s,t let `t_u` count wheels having m on their rim with centre in
the original u sector. Let `k_u` count singleton one-blocks in that
sector. Its endpoint faces are the corresponding mz face and mvw,
both zero, and the number of face transitions between them is `d_G(u)-3`.
There is no interior zero-zero transition. Every wheel contributes a
two-face one-block, and every other one-block is a singleton. Indeed any
two consecutive one faces, apart from pq which is not incident with m,
must be in the same complete wheel and share its spoke at m. Thus

`d_G(u)-3 = 2 k_u + 3 t_u`.                                  (2)

Since `6<=d_G(u)<=8`, two wheels cannot occupy the same sector.
There are three preliminary cases:

| Case | Number of rims containing m | Original `(d_G(s),d_G(t))` | `d_J(m)` | Excess |
| --- | ---: | --- | ---: | --- |
| I | 0 | `(7,7)` | 9 | Delta=2, all at m |
| II | 1 | `(6,7)` or `(7,6)` | 8 | Delta=0 |
| III | 2 | `(6,6)` | 7 | Delta=0, common rim m |

For case I, (2) makes both source degrees odd, hence seven. The odd m
degree nine uses two units of excess, so curvature forces `r_cap=0`.
For case II epsilon=1, hence r_cap=0 and Delta=0; m is even with
degree eight, giving degree sum thirteen and the wheel in the six-sector.
For case III the common m already uses r_cap=1. Its unchanged odd
parity and zero excess give m degree seven, hence both original degrees
six; (2) puts one wheel in each sector. In EVERY case all non-m vertices
attain their parity-sensitive minima. In particular a unique-rim pin
among v,w,p,q has J degree four.

## 4. Two rims cannot share m

Let d be the actual third vertex of the other face on vw. Thus the two
X faces are mvw and dvw, with d distinct from m,v,w and from either
wheel centre. If v or w is on a unique wheel rim it has degree four.
Its face rotation has a zero-zero transition at vw and a one-one
transition at its wheel spoke. These transitions cannot be adjacent:
their common face would need both bits. They are therefore opposite
in its four-face rotation. At v its wheel faces are `mvc,dvc`, and at
w they are `mwc,dwc`. In either case the rim contains BOTH m and d.

In case III the two sector words are exactly `0,1,1,0`. The original
t-sector link is `z,alpha,c_t,w`; the s-sector link is `z,beta,c_s,v`.
Their wheels contain `(m,alpha,w)` and `(m,beta,v)` on their rims.
The preceding degree-four observation puts the same d on both rims.
They share distinct m,d, contradicting `r_cap<=1`. Case III is impossible.
This also proves the rims, and hence K1,K2, are disjoint in all cases.

The same observation proves v,w membership exactly: in case I neither
lies on a wheel; in case II the s-wheel contains v and the t-wheel
contains w, respectively. The other pin cannot be in another wheel,
since that would force a second m incidence. Nor can it be in the same
wheel: its induced rim would contain the triangle m,v,w. Thus the other
pin belongs to no wheel.

## 5. The forbidden edge cannot enter a wheel

Write the other actual face on pq as `upq`. If it were in a wheel,
its centre must be u: p,q are in T. Thus p,q are consecutive vertices
on that wheel's rim. The disjoint-rim conclusion and zero non-m excess
give `d_J(p)=d_J(q)=4`, so `d_G(p)=d_G(q)=5`.

This wheel is retained from G with complete original centre degree five.
Moreover u is precisely the original ell of the other pq face: the
retained actual face upq is unchanged by the quotients. The original
double-low theorem gives `d_G(u)>=6`, a contradiction. Consequently
upq is also a singleton odd component. No f endpoint lies in a wheel.

Neither p nor q can nevertheless lie on a rim. At such a pin degree
four leaves only two faces after the two singleton faces zpq,upq are
removed. A wheel at the pin must occupy those two consecutive remaining
faces. At each end it would adjoin one of the singleton faces across a
non-pq edge, impossible by (1). Therefore p,q avoid both wheels; their
unchanged odd parity and zero excess give J degree five, original degree
six. This also excludes the full f-to-wheel placement subclass.

The double-low input is a same-source theorem. Its proof restores every
local lift of one disk and applies a return injection on that disk;
no separately feasible colourings are joined in the present deduction.

## 6. The exact z fan alternatives and an optional source cross-check

Disjointness gives `n_z`, the number of rims containing z, at most one.
Since all z excess is zero, its marked odd parity gives

`n_z=0 => d_J(z)=7, h=4`,
`n_z=1 => d_J(z)=6, h=3`.                                    (3)

The original a fan runs from zero face mz alpha to singleton face zpq;
the c fan runs from mz beta to that same singleton. If `t_a,t_c` count
the respective wheels at z and `k_a,k_c` count the intervening singleton
blocks, the same literal face-word count gives

`d_G(a)-4=2 k_a+3 t_a`, `d_G(c)-4=2 k_c+3 t_c`.               (4)

At the final singleton zpq a zero face must intervene after every
previous one-block; its incident zp,zq edges cannot join components.
This explains the endpoint difference between (2) and (4). The formulas
also cover an empty fan when alpha=p or beta=q.

If n_z=1, (3)--(4) force `(d_G(a),d_G(c))=(7,4),(4,7)` with the wheel
in the seven-fan. If n_z=0, (3)--(4) give

`h=4`, `(d_G(a),d_G(c))=(4,8),(6,6),(8,4)`.                 (5)

An optional cross-check uses the adopted
[original h=3 source classification, section 4.1](../2026-10-14-c4-mask13-joint6-fdd3e22/SOURCE_GEOMETRY.md),
which permits only `(5,6),(6,5)` here. With its original finite collar
interface and no4ct bridge trust layer retained, this excludes n_z=1
already and gives the seven intermediate types below. **The final
exclusion in section 9 does not use this h=3 classification or this
optional deletion.** It treats case I with either value of n_z and
excludes case II with n_z=1 directly by original face geometry.

## 7. Seven intermediate named sector types (all excluded in section 9)

In case II the six-sector rim contains beta,v for the s-wheel, and
alpha,w for the t-wheel. Since p,q avoid all wheels, alpha=p excludes
an a-degree-four t-wheel; beta=q excludes a c-degree-four s-wheel.
The complete necessary table, with source names fixed, is therefore:

| Type | `(d_G(s),d_G(t))` | `(d_G(a),d_G(c))` | m-wheel location | `(d_G(v),d_G(w))` |
| --- | --- | --- | --- | --- |
| I-48 | `(7,7)` | `(4,8)` | none | `(6,6)` |
| I-66 | `(7,7)` | `(6,6)` | none | `(6,6)` |
| I-84 | `(7,7)` | `(8,4)` | none | `(6,6)` |
| II-s-48 | `(6,7)` | `(4,8)` | s | `(5,6)` |
| II-s-66 | `(6,7)` | `(6,6)` | s | `(5,6)` |
| II-t-66 | `(7,6)` | `(6,6)` | t | `(6,5)` |
| II-t-84 | `(7,6)` | `(8,4)` | t | `(6,5)` |

Every row has original `p=q=6`, J z degree seven and h=4. Each is a
necessary structural class, not a numerical source witness or a claim
that its private graph is finite. Under Sigma932 the previously adopted
h=4 table additionally permits only the a=c=6 rows; we do not need that
extra restriction for the theorem and do not broaden it to other masks.

The actual m words in cases I/II are `0,1,0,1,0` in a seven-sector and
`0,1,1,0` in a six-sector. The z fan words are `0,1` for degree four,
`0,1,0,1` for degree six and `0,1,0,1,0,1` for degree eight. The final
one in both z words is the same original face zpq. Wheel labels at m
are interchangeable, while every original vertex and edge remains fixed.

## 8. Entire matching family and crossing-cut restrictions

For every M in the same nonempty P111, each of C1,C2 is tight:

`|M intersect delta_D(Ci)|=1`.                               (6)

The two singleton faces of f are already matched to each other by f.
Consequently **every other edge incident with either f endpoint is
absent from every M in P111**. Both endpoints are in H-S; their four
remaining neighbours lie in S or X, because f is the only deleted edge
between components. The four primal edges in question are `zp,zq,up,uq`,
with the actual u retained; u need not be a new anonymous vertex.

For crossing components C from this 101 barrier and K from ANY
maximum-cardinality 110 Tutte-violating barrier on the same D, both
components are odd and both cuts are tight on ALL of P111. With
nonempty intersection, differences and exterior, the exact identities are

`2 = M(delta(C intersect K)) + M(delta(C union K))`
`    + 2 M(E(C-K,K-C))` for odd intersection, and

`2 = M(delta(C-K)) + M(delta(K-C))`
`    + 2 M(E(C intersect K,V(D)-(C union K)))` for even intersection.

The two displayed odd-set crossing counts are at least one. Thus each is
one and the last edge class is absent from EVERY common matching. Any
of e,f,g in the forbidden class immediately excludes that crossing
placement, since all three are present in every common matching. These
are same-graph tests on actual edges; no independent barriers are glued.
Without a forced edge in that class the identity supplies no contradiction.
We do not assume the 110 obstruction exists or is a pair of wheels.

## 9. Expanding one pure degree-five wheel closes the contradiction

### 9.1 A pure wheel exists without the optional h=3 source table

In case I neither wheel meets m,v,w,p,q. At most one rim contains z,
so at least one wheel avoids all of T. In case II the unique m-wheel
contains the only possible v/w rim pin, while p,q avoid both wheels.
If no rim contains z, the other wheel again avoids all of T.

It remains to exclude case II with a rim containing z. The z-wheel
cannot be the m-wheel. Suppose the m-wheel is in the t sector. Its
short sector link is `z,alpha,c_t,w`; it has alpha on its rim, so
alpha cannot be p, because p avoids the wheels. Hence `d_G(a)!=4`.
But (3)--(4) in this n_z=1 case leave only `(a0,c0)=(7,4),(4,7)`;
therefore `(a0,c0)=(7,4)`. Its actual a-fan word is `0,1,1,0,1`.
The first two one faces belong to the z-wheel and have alpha on that
wheel's rim. Both wheels now share alpha, contradicting disjointness.
For an s-sector m-wheel interchange alpha,a,p,t,w with beta,c,q,s,v;
the same argument excludes it. This handles literal endpoint identities
as well: the degree-four fan endpoint is the actual p or q, not a new pin.

Choose the resulting pure wheel with centre c and rim
`u_0,u_1,u_2,u_3,u_4` in its actual rotation (indices modulo five).
All six vertices avoid T, and K1,K2 are disjoint. Their parity is odd;
zero non-m excess from section 3 gives complete J degree FIVE at all six.

### 9.2 Its actual second neighbourhood is a fifteen-face disk

For each rim edge `u_i u_{i+1}`, let a_i be the third vertex of its
other actual triangular face, opposite c. It is outside the six-vertex
wheel: any other rim vertex in that face would create a rim chord.
Consecutive a's are distinct. If `a_{i-1}=a_i`, the four known faces
around u_i close its entire link on four vertices, contradicting its
degree five. Its degree-five link is therefore exactly

`c,u_{i+1},a_i,a_{i-1},u_{i-1},c`.

In particular `a_{i-1} a_i` is an edge, and `u_i a_{i-1} a_i` is a
face. Nonconsecutive a's are also distinct: if `a_i=a_{i+2}`, their
common vertex is adjacent to both `u_{i+1},u_{i+2}`. The resulting
triangle is facial. Its face on their rim edge is necessarily the
external face, so `a_{i+1}=a_i`, the excluded consecutive coincidence.
Every nonconsecutive pair on a five-cycle has this form up to reversal.

Thus the a's form a simple cycle Q. The following fifteen distinct actual
faces form a disk R with boundary Q and exactly six interior vertices:

* five centre faces `c u_i u_{i+1}`;
* five external rim faces `u_i u_{i+1} a_i`;
* five corner faces `u_i a_{i-1} a_i`.

All vertices are distinct in the indicated inner/outer layers. The actual
face attachments and the complete links of c,u_i show that this union
is a disk, not merely a boundary walk or an abstract replacement patch.
Explicitly it has 11 vertices, 25 edges and 15 faces, Euler characteristic
one, one simple boundary Q and the complete interior links just displayed.
At each a_i its R interval consists of exactly the three faces

`u_i a_{i-1} a_i`, `u_i u_{i+1} a_i`, `u_{i+1} a_i a_{i+1}`.     (7)

Their bits are respectively **1,0,1**. The middle face is across the
rim from a wheel face; its rim edge is not a marked edge, so it is zero.
It is not in X, since it contains two vertices outside T, whereas every
X face contains two endpoints of a marked edge in T. Thus it belongs
to S. Each corner face then has bit one. It is neither in the selected
wheel nor in the other wheel: that would put its u_i on the other rim
(or make u_i its centre), contradicting disjointness. Therefore every
corner face in (7) is a SINGLETON component.

### 9.3 Q has no chord

Suppose Q has the chord `a_{i-1} a_{i+1}` across a_i. Its triangular
ear is an actual facial triangle, by source faciality. It cannot be
on the R side: the R interval (7) has three faces at a_i, whereas the
facial ear has only one. The facial ear is therefore outside R, and
together with (7) closes the entire link of a_i. Hence a_i has degree
four and its complete neighbour set is

`{a_{i-1},a_{i+1},u_i,u_{i+1}}`.                              (8)

Case I has no degree-four vertex anywhere: the exact minima and exhausted
excess give m=9, z=6 or 7, all pins degree five, and every other vertex
degree five or six. Case II has only one possible degree-four vertex,
the v/w pin on its m-wheel. By section 4 its complete neighbour set is
`{m,other v/w pin,d,c_m}`. Each of these is either in that m-wheel's K
or in T, hence outside the pure wheel. It cannot contain u_i or u_{i+1},
as (8) requires. This is a contradiction in both cases.

Every chord of a C5 spans a two-edge path. Thus Q is induced, with no
omitted second-chord or exceptional-sector case.

### 9.4 The actual hub positions make Q a lifted pentagon

If Q avoids m,z, the lifted-pentagon theorem C1 applies directly.

If Q contains m alone, its three R faces at m have the 1,0,1 word (7).
The two one faces avoid X. The middle zero face contains two pure rim
vertices and is in S, so also avoids X. In particular the interval
avoids mvw and both mz faces. Removing their three edges from link(m)
leaves the isolated z and the two original s/t sector paths. The
nonempty R interval lies in one sector path, so Q's two neighbours at
m are in that same original sector. Theorem C1 case 2 applies.

If Q contains z alone, the same interval avoids both mz faces. It also
avoids the SINGLETON face zpq: neither one face in (7) can be zpq,
because each contains a pure rim vertex outside T; the middle face is
zero, whereas zpq is one. Removing the two mz link edges and pq from
link(z) leaves the isolated m and the separate original a/c fan paths.
The R interval lies within one fan. Hence Q's two neighbours at z are
in the same original fan, and theorem C1 case 3 applies. This covers
alpha=p and beta=q without treating them as distinct new vertices.

Finally Q cannot contain both hubs. Its inducedness would force mz to
be a boundary edge. But the actual R face on every edge of Q is one
of the singleton corner faces (bit one), whereas BOTH mz faces are in
X (bit zero). This is impossible.

In every possible case Q therefore has a complete retained W5 on one
side. Its R side has six strictly interior vertices, so it is not that
one-centre W5 side. The complementary side must be the W5. J consequently
consists of c, the five u's, the five a's and that one outside centre.
Every vertex has degree five: each a_i has its two Q neighbours, u_i,
u_{i+1}, and the outside centre; the other degrees are already fixed.
This contradicts `d_J(m)>=7` (and also `d_J(z)>=6`).

This completes the arbitrary-size exclusion for the chosen S. Since S
was arbitrary, every double-W5 maximum 101 barrier is excluded. The
optional seven-sector table is exhausted by this proof; no row remains
OPEN and no source order or finite census was used in closing it.

## 10. Evidence level and exact remaining obligation

Sections 2--5 and 9, using only the direct fan equations (3)--(4) from
section 6, prove the theorem from arbitrary-size paper source inputs.
The optional seven-row cross-check additionally uses the previously
adopted h=3 finite interface/source bridge. [check.py](check.py) enumerates the finite
sector-word algebra and every local W5 matching fibre, including empty
fibres; it is not a source verifier. No new genuine minimum source or
synthetic whole-source realization is supplied: target coverage is
`not triggered`. Every complete original colouring fibre and every legal
r lift remains part of the standing contract, without projection.

The entire double-W5 branch is excluded. Ordinary 101 failure still may
have a nonwheel seven-cut maximum barrier. The 110 residuals and
even-complement positivity remain OPEN. An ordinary perfect matching is not an even-complement
matching. No complete319 exclusion, new order bound, strict descent,
external theorem or new Lean theorem is claimed. Reconstruction remains
k+5; general K<=22 and the fixed-r6 k>=25 statement are unchanged.
