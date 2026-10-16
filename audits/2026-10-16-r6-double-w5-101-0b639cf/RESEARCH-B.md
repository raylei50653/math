# R6-DOUBLE-W5-101 B: local face words and disjoint wheel rims

This is a paper proof at BASE `0b639cf`, on the complete same original
minimum C5 source and its actual embedded `J=U/(s=t)`, `D=J*`.
It uses the already adopted chorded-five conclusion separately for each
five-cut component, the common-111 saturation, and the weighted curvature
identity. It does not construct a source or claim a completed-source descent.

## B1. Standing data and the actual face bits

Suppose the maximum 101 barrier has two complete W5 components `C1,C2`,
with original degree-five centres `c1,c2`. Let `Ri=N_J(ci)` be their induced
five-cycle rims and `Ki=Ri union {ci}`. Let

`r_cap=|K1 intersect K2|`,
`epsilon=1` when m is in exactly one Ki, and zero otherwise.

The adopted results give nonadjacent centres outside
`T={m,z,v,w,p,q}`, `r_cap+epsilon<=1`,
`Delta=2(1-r_cap-epsilon)`, `6<=d_G(s),d_G(t)<=8`, and `3<=h<=6`.
Here Delta is the total degree excess over the parity-sensitive minima.

Give bit zero to faces in `S union X`, and bit one to every component of
`H-S`. Since the two wheels spend the whole cut budget, `S` is independent
and has no edge to X. Since the common 111 theorem gives `tau=1`, f joins
two distinct odd components. Therefore the entire monochromatic primal-edge
set is exactly

`{vw,pq,mz} union {all spokes of the two actual wheels}`.       (B1)

The edges vw and mz have two bit-zero incident faces. The edge pq and
every wheel spoke have two bit-one incident faces. Every other primal
edge has opposite face bits. These are actual faces of the same J.

A wheel rim cannot contain both m and z: its inducedness would place mz
on its rim, and one of that wheel's actual incident faces would then be
one of the two forced X faces on mz. That is impossible.

## B2. Exact original s/t-sector words

For `u=s,t`, let `t_u` count the wheels whose rim contains m and whose
centre lies in the literal original u-sector. The original link interval
from the corresponding mz face to mvw has `d_G(u)-3` transitions between
consecutive incident faces of m. Both endpoint faces are in X and have
bit zero. The interval contains no other zero-zero transition: the only
zero-zero primal edge incident with m is mz, outside its interior.
Each wheel counted by t_u contributes exactly one one-one transition,
its spoke `m ci`. The remaining bit-one blocks are singleton faces;
write their number as `k_u>=0`. Thus the actual word is composed of
blocks `0,1,0` and `0,1,1,0`, with their endpoint zeros identified, and

`d_G(u)-3 = 2 k_u + 3 t_u`.                                (B2)

The two centres cannot occupy the same sector with `t_u=2`, since that
would require `d_G(u)>=9`. Consequently each t_u is zero or one.
The curvature bound gives only the following three preliminary cases:

| Case | Wheel incidence at m | `r_cap` | Original s/t degrees | `d_J(m)` | Excess |
| --- | --- | ---: | --- | ---: | --- |
| I | neither wheel | 0 | `(7,7)` | 9 | Delta=2, entirely at m |
| II | exactly one wheel | 0 | `(6,7)` or `(7,6)` | 8 | Delta=0 |
| III | both wheels | 1, common rim point m | `(6,6)` | 7 | Delta=0 |

Here is the justification that the table is exhaustive. If m is in
neither wheel, B2 makes both source degrees odd, hence both seven. Thus
`d_J(m)=9`, two above its odd minimum seven. It uses the whole permitted
Delta and forces `r_cap=0`. This also rules out a common rim point other
than m. If m belongs to exactly one wheel, `epsilon=1`, so `r_cap=0`
and Delta=0. Its parity minimum is eight; the source degree sum is then
13, with the wheel in the degree-six sector and the other sector degree
seven. If m belongs to both wheels, `r_cap=1`, Delta=0, and its parity
is unchanged odd, so `d_J(m)=7`; both source degrees are six. Formula
B2 puts one wheel in each sector.

In particular **degree eight for either original s or t is excluded**.
In all three preliminary cases every vertex other than m attains its
parity-sensitive minimum. In Case I m is the sole exceptional vertex;
in Cases II and III it also attains its minimum.

## B3. The common-rim case is impossible

First record a local observation valid whenever a marked pin v or w lies
on one wheel rim. Such a pin has degree four: its initial all-three-marked
parity is odd, one wheel flips it to even, and it has no available degree
excess. Write `d` for the third vertex of the OTHER actual face on vw,
so the two faces on vw are `mvw` and `dvw`, both in X. The wheel centre
c is different from d, because the complete star of c avoids X.

Around the degree-four pin, vw is a zero-zero transition and the wheel
spoke is a one-one transition. They cannot be adjacent transitions, since
that would make their shared face have both bits. They are therefore
opposite transitions of this four-face rotation. At w the two wheel faces
are consequently `mwc` and `dwc`; at v they are `mvc` and `dvc`.
Thus the wheel rim contains **both m and d**. This conclusion retains
the actual d and the original vw edge.

In preliminary Case III, the t-sector has the exact word `0,1,1,0`.
Its original link path is `z,alpha,c_t,w`, followed by the edge wv.
Hence its wheel rim contains m,w,alpha. Likewise the s-sector wheel rim
contains m,v,beta. Applying the preceding degree-four observation at w
and v puts the same actual d in both rims. The rims therefore share at
least the two distinct vertices m,d, contradicting `r_cap<=1`.

**Theorem B3. Every surviving pair of 101 W5 rims is vertex-disjoint.**
The centres are already distinct, outside the other rim, and nonadjacent,
so the two complete six-vertex wheel neighbourhoods are disjoint as well.
The entire shared-rim alternative of the earlier curvature classification
is excluded by an arbitrary-size same-source proof.

It also follows that in Case I neither v nor w belongs to either wheel.
In Case II exactly one of v,w belongs to the unique m-wheel, namely w
in the t-degree-six sector or v in the s-degree-six sector. The other
pin cannot belong to the same wheel, since an induced rim cannot contain
the triangle m,v,w. It cannot belong to the other wheel, since the
preceding observation would force a second m incidence. The m-wheel's rim contains the corresponding
alpha/beta and the literal other vw-face vertex d.

## B4. z and the complete remaining fan table

Since the two rims are disjoint, at most one wheel rim contains z.
Let `n_z` denote this number. A wheel cannot contain both hubs, as in B1.
The source degree identity is `d_J(z)=h+3`. All non-m excess is zero.
The initial all-three-marked parity at z is odd. Hence

* `n_z=0` gives `d_J(z)=7` and h=4;
* `n_z=1` gives `d_J(z)=6` and h=3.

For completeness, let `a0=d_G(a)`, `c0=d_G(c)`. The facial vertex zpq
is a singleton component: a full wheel containing it would have centre
z,p or q, all forbidden by the centre-outside-T theorem. Along the
original a-fan from the X face mz alpha to singleton zpq, each intermediate
component block has one face, except a wheel at z has two consecutive
faces. All intervening zero faces belong to S. Counting those blocks gives

`a0-4=2 k_a+3 t_a`, `c0-4=2 k_c+3 t_c`,                     (B3)

where `t_a+t_c=n_z`. Endpoint coincidences alpha=p or beta=q mean that
the relevant intermediate word is empty; they do not change B3.
With h already fixed, the only possible original fan degrees are

| z-wheel count | h | `(a0,c0)` | Wheel location |
| ---: | ---: | --- | --- |
| 0 | 4 | `(4,8)`, `(6,6)`, `(8,4)` | none |
| 1 | 3 | `(7,4)`, `(4,7)` | the degree-seven fan |

Together with B3, the surviving configurations have precisely four named
macrotypes: I0, I1, II0, II1, where the Roman numeral specifies the m
incidence and the suffix is n_z. This is a finite classification of the
hub incidence and original fan words, **not** a finite classification of
all private vertices or a source realizability assertion. Source order
remains unbounded, and all actual exterior edges are retained.

## B5. All z-wheel types are excluded by an existing source theorem

The preceding B4 table would require `(a0,c0)=(7,4)` or `(4,7)` whenever
z lies on one rim. However, the already adopted original-source h=3
classification gives only `(a0,c0)=(5,6)` or `(6,5)` under the present
`d_G(x)=d_G(y)=d_G(b)=4` branch. See the literal source table in
`audits/2026-10-14-c4-mask13-joint6-fdd3e22/SOURCE_GEOMETRY.md`, section 4.1,
which cites the complete no4ct C8 necessary-residue classification.
The named pairs are disjoint. Therefore **neither wheel rim contains z**,
`h=4` and `d_J(z)=7` in every surviving case.

This use is a same-source restriction at h=3, not an extension of the
h=3 classification to general sources or to h>=4.

There is also a direct exclusion of preliminary Case II1, independent of
that h=3 table. Take `(a0,c0)=(7,4)`. The z-wheel in the seven-degree fan
has rim containing alpha, whereas beta=q. An m-wheel in the s-degree-six
sector would contain beta=q, impossible once f is singleton-to-singleton
and q avoids the rims (B6). Thus the m-wheel would be in the t-degree-six
sector, and its rim also contains alpha. This contradicts disjointness.
Reflecting the names treats `(4,7)`. The h=3 table additionally excludes I1.

## B6. The forbidden edge is singleton-to-singleton

The independent A/C proof establishes that f cannot enter either wheel.
A particularly short source argument is available: if its other endpoint
were `pqu` in a wheel, its centre would have to be u, outside T. The
same degree-minimum argument makes `d_J(p)=d_J(q)=4`, so their complete
original degrees are both five. The previously adopted literal
LL-C4 endpoint theorem says that when the original p and q both have
degree five, the other pq-face vertex has original degree at least six.
Here that vertex is u, whose retained full original wheel degree is
five, a contradiction. This imports the existing endpoint theorem on
its exact original p,q and actual other face, with no re-marking.

Consequently both ends of f are singleton odd components. Moreover p
and q avoid both wheel rims. Indeed, if p belonged to one rim, its degree
would be four; its face rotation would have the one-one pq transition
between two singleton faces and a second one-one transition at its wheel
spoke. Opposite positions make all four faces one and give extra
monochromatic edges; adjacent positions make their shared face belong
both to a singleton and a wheel. Both contradict B1. The argument at q
is identical. Therefore

`d_J(p)=d_J(q)=5`, `d_G(p)=d_G(q)=6`.

Together with B3, the remaining marked-pin membership is exact:

* In Case I, all six pins m,z,v,w,p,q avoid both wheel neighbourhoods.
* In Case II, the m-wheel contains m and exactly one of v,w; its rim
  contains w,alpha in the t-degree-six case and v,beta in the s-degree-six
  case. The second wheel avoids every pin in T. The pins z,p,q and the
  other v/w avoid both wheels.

## B7. Seven remaining named degree classes

Since p,q avoid both wheels, `a0=4` (alpha=p) forbids the m-wheel in the
t-degree-six sector, whose rim would contain alpha. Similarly `c0=4`
(beta=q) forbids the m-wheel in the s-degree-six sector. B4 now gives
exactly seven possible oriented tuples
`(d_G(s),d_G(t),a0,c0)`:

| Class | `(s,t,a0,c0)` degrees | m-wheel |
| --- | --- | --- |
| I-48 | `(7,7,4,8)` | none |
| I-66 | `(7,7,6,6)` | none |
| I-84 | `(7,7,8,4)` | none |
| II-s-48 | `(6,7,4,8)` | s-sector, rim contains m,v,beta |
| II-s-66 | `(6,7,6,6)` | s-sector, rim contains m,v,beta |
| II-t-66 | `(7,6,6,6)` | t-sector, rim contains m,w,alpha |
| II-t-84 | `(7,6,8,4)` | t-sector, rim contains m,w,alpha |

This is a finite classification of the original hub degrees and fan
words. It is not a finite classification of the entire private graph.
The complete exterior graph and all its original edge identities remain
part of each case, and source order is unbounded.

The source consequences are stronger than the previous
`s,t<=8`, `h<=6`: now `s,t<=7`, `h=4`, the two rims are disjoint and
avoid z, f joins two singletons, and the seven named classes exhaust the
same-source possibilities. The shared-rim class, every degree-eight s/t
class, every z-wheel class, all h-five/six classes, the f-wheel class,
and the endpoint-forbidden orientations above are excluded.

Neither these seven cases nor a private exterior disk satisfying them
is asserted realizable as a globally minimum source. The outstanding
geometric obligation is to use the retained exterior disk, the full all-r
colouring condition, or a common-family crossing 110 barrier to exclude
the seven cases. No numerical source, independent matching witness,
omitted empty fibre or re-marked control is used here. B1--B7 are paper
arguments; finite verification can check only the exact word algebra and
seven-row arithmetic. No completed-source replacement, stronger k bound,
4CT invocation, new Lean theorem, commit or push is claimed here.

## B8. Radius-two disk of a pure degree-five wheel

**Theorem B8 (independently reviewed).** Under the
same surviving double-wheel conditions, a wheel avoiding every vertex of T
is impossible. There is at least one such wheel in every remaining case:
in Case I both are pure; in Case II the wheel other than the m-wheel is pure.
The independent reviewer reconstructed this radius-two argument and
reported PASS; see the final parent review for its custody record.

Let c be its centre and `u_0,...,u_4` its rim in cyclic order. All six
vertices have full J degree five. For each i let a_i be the third vertex
of the actual exterior face on edge `u_i u_(i+1)` (indices modulo five).
No a_i is c or a rim vertex, by faciality and inducedness of the wheel rim.

First, `a_(i-1)!=a_i`. Equality would make the two complete wheel faces
and the two exterior faces at u_i close a four-face rotation, giving
`d_J(u_i)=4`, a contradiction. The five neighbours of u_i are therefore
exactly `c,u_(i-1),u_(i+1),a_(i-1),a_i`. Its remaining face is
`u_i a_(i-1) a_i`. In particular the a_i form a closed five-edge walk.
Any nonadjacent repetition has cyclic distance two. If `a_i=a_(i+2)`,
then this vertex is adjacent to both `u_(i+1),u_(i+2)`. Their triangle
must be the actual exterior face on that rim edge, forcing
`a_i=a_(i+1)`, already excluded. Hence all five a_i are distinct.

The five centre faces, five rim-exterior faces and five remaining u_i
faces form a connected embedded surface R with simple boundary
`Q=(a_0,...,a_4)`: every c/u_i link is complete, each a_i has exactly its
three consecutive displayed inner faces, and the only edges incident
with just one displayed face are the five Q edges. There are eleven
vertices, twenty-five edges and fifteen faces, so its Euler
characteristic is one. As a connected subsurface of the sphere with
one boundary component, R is an actual disk. Its six strictly interior
vertices are exactly c and the u_i. Its interior faces have the following
actual barrier bits:

* `c u_i u_(i+1)`: bit one, in the wheel;
* `u_i u_(i+1) a_i`: bit zero, outside the wheel;
* `u_i a_(i-1) a_i`: bit one, a singleton component.

The second class is zero because the wheel boundary edges avoid every
marked primal edge (their endpoints are pure rim vertices). It is in S,
since every X face contains at least two T vertices, whereas this class
of face has two pure rim vertices and at most one T vertex. The third
class is one by the opposite-bit condition on edges `u_i a_i`. It cannot
be in the first wheel, since it does not contain c. If it belonged to the
other wheel, its centre would be one of a_(i-1),a_i (it cannot be u_i,
which belongs to the first rim). That centre would be adjacent to u_i,
putting u_i in both closed wheel neighbourhoods, contrary to disjointness.
Hence these five faces are singleton components. In particular the three-face interval
of R at every a_i has bits `1,0,1`.

### B8.1 Q is induced

A chord a_i a_(i+2) gives the facial exterior triangle
`a_i a_(i+1) a_(i+2)`: it cannot be an R face, whose complete face set is
already displayed. Together with the three R faces at a_(i+1), it closes
that vertex's rotation and forces its full degree to be four. Only v,w
could have degree four in the surviving cases. If either has degree four,
it lies on the m-wheel and its full neighbour set is
`{m, the other vw pin, d, the m-wheel centre}`, where d is the actual other
vw-face vertex and also belongs to that m-wheel's rim (B3). None of those
four vertices belongs to this pure wheel's rim. But a_(i+1) has the two
pure rim neighbours `u_(i+1),u_(i+2)`, a contradiction. Therefore Q has no
chord.

### B8.2 Every possible hub position contradicts the source C5 theorem

If Q avoids both m,z, the adopted short-cap theorem says that one side
is a complete retained W5. It cannot be R, which has six interior
vertices. If the other side is W5, then the whole sphere consists of
this fifteen-face disk and that five-face wheel. Every Q vertex has
exactly its two Q neighbours, its two interior u neighbours, and the
exterior wheel centre as neighbours, hence degree five; all R interior
vertices and the exterior centre also have degree five. This contradicts
`d_J(m)>=7`.

If Q contains m alone, its R interval is the three actual faces
`m u_i a_(i-1)`, `m u_i u_(i+1)`, `m u_(i+1) a_(i+1)` of bits `1,0,1`.
None is in X: the zero middle face contains two pure rim vertices, whereas
every X face incident with m is one of `mvw,mz alpha,mz beta` and contains
another marked vertex. Deleting those three X faces from the link of m
leaves the singleton z and the two original sector paths. This nonempty
R interval lies in one original sector, so the Q neighbours of m lie in
the same original s/t sector. The adopted lifted-pentagon theorem C1
therefore again gives a complete retained W5 on one side, and the preceding
six-interior-vertices/all-degree-five contradiction applies.

If Q contains z alone, its R interval likewise has bits `1,0,1`, avoids
the two X faces on mz, and cannot contain zpq: each bit-one endpoint
face contains a pure rim vertex u_i or u_(i+1), whereas p,q avoid the two
wheel rims, and the middle face has bit zero. Thus the R interval avoids
all three separating link edges `m-alpha,m-beta,pq`. The Q neighbours
of z lie in one original a/c fan. The lifted-pentagon theorem again
produces the same impossible opposite W5 side.

If Q contains both m,z, its inducedness puts mz on the cycle. But the R
face on any Q boundary edge `a_(i-1) a_i` is
`u_i a_(i-1) a_i`, of bit one, whereas both actual faces on mz have bit
zero in X. This is an immediate contradiction.

All four hub positions are excluded. Therefore no pure wheel exists.
Since one necessarily exists in each remaining double-wheel case, this
radius-two argument excludes the whole double-W5 maximum 101 barrier.
The seven B7 classes were intermediate candidate classes; none remains
OPEN after B8. The other non-wheel seven-cut 101 branch remains OPEN,
as do the independent 110, even-complement and complete319 obligations.
