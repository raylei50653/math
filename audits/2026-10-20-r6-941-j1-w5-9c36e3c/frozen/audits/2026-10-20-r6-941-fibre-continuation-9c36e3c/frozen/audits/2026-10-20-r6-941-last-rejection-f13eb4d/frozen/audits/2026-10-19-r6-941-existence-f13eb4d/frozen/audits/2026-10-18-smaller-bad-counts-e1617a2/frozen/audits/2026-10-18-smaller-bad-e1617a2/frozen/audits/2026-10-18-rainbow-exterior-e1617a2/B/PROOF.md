# B. Same-colouring exterior Kempe constraints for the fixed fan at b

Frozen BASE `e1617a2756813327d7ad333cfdd0fd92fa9efc38`.
This independent paper audit uses the frozen smaller-source C proof and
active-f B proof listed in the parent INPUTS. It never combines components
from different colourings. The general switch principle is the established
boundary-anchored component criterion; the new content is its exact
specialization to these fixed original candidates and their accepted sector.

## 1. Literal source and candidates

Fix one original plane C5 source G with ordered boundary
`B=(x,y,a,b,c)`. Its three complete fibres for `01021,01202,01212` are empty.
Its `01232` fibre is nonempty. Retain the complete original graph, actual
embedding, all private vertices and the four named rows without independently
normalizing an interface or a component.

For the detailed statements below, use the original site `(p,h)=(p,ell)`:

```
N_G(p)=(a,b,q,h,n),       N_G(h)=(p,q,L,R,n),
N_G(b)={a,c,p,q},         qc in E(G).
```

Both p and h have original degree five. Their two closed stars have precisely
these two interior vertices and genuine simple boundary
`C=(a,b,q,L,R,n)`. The six rim vertices are distinct. The named boundary
vertices retain their original roles; in particular q,n are interior
vertices, not pins of the original C5. These are the source hypotheses of
the frozen original construction, including the original degree-four b.
No assumption about a perfect matching, a reference, or its oddness is used.

The two fixed candidates delete p,h and fill this disk by respectively
`aq,aL,aR` (H_a) and `bn,bL,bR` (H_b). Existing parallel copies, if any,
are suppressed without deleting the original inequality. Both are completed
`k-2` graphs on the same original ordered C5. The full exterior is unchanged.

For either candidate and every complete colouring chi, its full old lift
fibre is

```
{(P,H): P notin {a,b,q,n}, H notin {q,n,L,R,P}},
```

with letters on the right denoting their actual colours in chi. This fibre
is nonempty exactly when `{a,b,q,n}` is not rainbow. In H_b the explicit
lift sets h=b and chooses any missing gate colour for p. Thus every complete
colouring of any rejected row in either candidate has a rainbow gate.

## 2. The non-b fan cannot meet the specified four-query certificate

In H_a, b has the complete neighbour set `{a,c,q}`. In any complete accepted
`01232` colouring, a=c=2, b=3, and q is a colour t in `{0,1}`. Let `s=1-t`.
Changing only b from 3 to s is proper and produces `01202` when t=1 or
`01212` when t=0. The candidate graph and all other vertex colours are fixed.

Consequently

```
F_01232(H_a) nonempty =>
F_01202(H_a) union F_01212(H_a) nonempty.
```

It is impossible to establish the desired three empty fibres on an accepting
H_a. This is an arbitrary-exterior obstruction to the specified four-query
certificate. It does not exclude a different outside-K132 certificate for
this graph.

The source empties sharpen this further. Before changing b, n differs from
a=2. After changing b to s, the gate can be rainbow only if n=3. Therefore
**every** accepted H_a colouring has n=3=b, including any colouring not
initially known to lift. It is therefore liftable. All work toward this
particular accepted-plus-three-empty certificate must use the fixed H_b
branch (or a newly proved different operation). Accepted-branch coverage
by a pair does not establish that H_b accepts.

The same b-degree argument applies at the other p-centred site after its
literal mapping, and under full reflection at the two q-centred sites.
The companion A audit supplies the all-four-site identities and counts.
The detailed exterior tables below are **only** for the displayed `(p,ell)`
site; its gate pair q,n must not be reused unchanged at `(p,n_a)`.

## 3. Boundary-anchored pairs, with exact original-edge authority

For one complete rejected-row colouring of H_b, consider any two of the
four gate vertices, with distinct colours i,j. If their actual maximal
`{i,j}` components are distinct, both components must meet the original
boundary B. Otherwise switching the one that misses B leaves the entire
row fixed and makes the two gate colours equal. The resulting complete
H_b colouring has a nonempty old lift, contrary to that source row's empty
full fibre.

This criterion is simultaneous within the one colouring. It asserts neither
that arbitrary contact alternatives are independent nor that their paths
can be retained after another Kempe switch.

Its proof uses only the literal four-gate lift theorem, so it applies at all
four source sites with their actual `(A,B,Q,N)` labels. This generic scope
does not transport the following site-specific palette table without also
transporting every original boundary colour and attachment.

Four of the six gate pairs are already connected by actual candidate edges:
`ab, an, bq, bn`. Only `(a,q)` and `(q,n)` can add information. Crucially,
**every added edge of H_b is incident with b**. Every two-colour component
whose palette avoids chi(b) therefore consists entirely of edges of the
original surviving graph `G-{p,h}`. All nonautomatic components in the next
table have this property. Original rim edges such as qL, LR and Rn are
permitted parts of these original exterior components; they are not added
fan edges.

## 4. Exact forced exterior table for all five rainbow sectors

Write `u ~ij v` for membership in the same actual `{i,j}` component in this
one full H_b colouring. A component assertion here includes every private
vertex on the path and concerns this candidate's full fibre, including
the possibility that the entire fibre is empty.

| Original row | (q,n) | Necessary original-exterior condition |
| --- | --- | --- |
| 01021 | (3,1) | `K03(q)` meets `{a,x}`; and either `q ~13 n`, or their components are distinct with `c in K13(q)` and `y in K13(n)` |
| 01202 | (1,3) | `q ~13 n` |
| 01202 | (3,1) | `q ~13 n` |
| 01212 | (0,3) | `q ~03 n` |
| 01212 | (3,0) | `q ~03 n` |

The palettes and sectors are exhaustive because qb,qc and the rainbow gate
are actual simultaneous constraints. In particular the fourth colour on q
has not been omitted.

For `01202`, the q,n palette is `{1,3}` and its only original boundary
vertex is y. If q,n had distinct components, at least one would miss y and
therefore all of B. Switching that component gives q=n and the forbidden
old lift. For `01212` the identical argument uses palette `{0,3}` and its
single boundary vertex x. This proves an actual q-to-n connection, stronger
than the previous alternatives `n -> {q,y}` or `n -> {q,x}`.

For `01021`, q=3,n=1. The q-component in palette `{1,3}` already contains c
by the original edge qc. If n is in a distinct component, its component
cannot contain c; it must contain y, since these are the only boundary
vertices of that palette. For the pair a=0,q=3, the only boundary vertices
in palette `{0,3}` are a,x. If K03(q) missed both, switching it would give
q=a without changing B. This supplies the other asserted contact.

In the last four sectors, the other nonautomatic pair `(a,q)` needs no
additional condition: a is itself on B and q is already joined to the
boundary vertex c of colour a by qc. Thus both its possibly distinct
components are already boundary-anchored.

This table is the entire specialization of the one-switch gate criterion.
It is not a proof of three empty fibres. In particular the `01021` paths
have palettes 03 and 13, which share colour 3. Alternating endpoints do
not make these paths disjoint. Even a forced intersection at a 3-coloured
vertex does not turn the 03 segment from q into a 13 segment. A crossing
argument that ignores this issue would silently use a false path implication.

## 5. A forced exterior path in each old-liftable accepted H_b colouring

Take one complete H_b colouring of `01232` with nonrainbow gate. This includes
every original accepted colouring whose retained branch is H_b, but does
not assume that all accepted H_b colourings are old-liftable.

Put q=t in `{0,1}` and s=1-t. The fan edge bn and original edge an imply
n differs from 3 and 2; the nonrainbow gate therefore forces n=q=t. The
rim and fan constraints force

```
a=c=2, b=3, q=n=t, {L,R}={2,s}.
```

Let Z be the unique vertex of `{L,R}` of colour s. The actual `{s,3}`
component containing b must contain x if s=0, or y if s=1. Otherwise
switching that complete component fixes every boundary vertex except b,
changes b to s, leaves q=n=t, and produces the corresponding rejected row
with a nonrainbow gate. The explicit lift then contradicts the source.

In H_b the only neighbour of b of colour s is Z: its complete neighbour
set is `{a,c,q,n,L,R}`. A simple path from b to its forced boundary anchor
therefore begins bZ and never returns to b. Removing this first edge gives
a path from Z to that anchor in `H_b-b`. Every edge of this path is an
original surviving edge, since all added fan edges are incident with b.

This is an accepted-colouring constraint in a palette different from the
rejected-row table. It supplies no permission to combine their paths.

## 6. Conditional planar crosscut refinement

The following geometric refinement has one explicit additional hypothesis:
the complementary exterior of the two-star cap together with triangle bcq
is a genuine closed disk E with simple boundary

```
(a,n,R,L,q,c,x,y).
```

All eight named vertices must be distinct, and the displayed cyclic order
must be the actual original rotation. This is true of the completed control
in the frozen C proof. We do not treat that control as verifying this
additional hypothesis for every hypothetical source. Application to an
arbitrary source requires its own exact collar/rotation verification; no
extra coincidence is silently ruled out here.

Under this additional hypothesis, the Z-to-anchor path of section 5 lies
in E and can be chosen simple. Its palette is `{s,3}`. The only boundary
vertices of E in this palette are Z and the anchor itself: the other L/R
vertex, a,c have colour 2; q,n and the remaining x/y vertex have colour t.
Thus its interior misses the boundary of E and it is a genuine crosscut.

For either Z=R or Z=L and either anchor x or y, the endpoints q,n lie on
opposite boundary arcs cut off by this crosscut. Every `{2,t}` path is
vertex-disjoint from it. Planarity therefore forbids a q-to-n path of
palette `{2,t}` in E. The original rim edges an and qc give the sharper
partition

```
{a,n} in one {2,t} component,
{q,c} in another {2,t} component,
and those two components are distinct.
```

This is a genuine one-colouring disjoint-palette separation. It is compatible
with the preceding rejected-row q-to-n connections: they are assertions
about different colourings and different palettes. There is no established
transport identifying these components across the rows.

## 7. Exact remaining obligations

The non-b-rooted fan cannot satisfy the specified four-query certificate.
For the fixed b-rooted fan the remaining requirements for that certificate
are:

1. Prove it has an accepted full colouring. An original accepted witness
   with h=b suffices; pair coverage alone does not supply this branch.
2. Exclude its complete `01021,01202,01212` rainbow fibres together, using
   the same original exterior and actual component transport. The table
   records necessary simultaneous connections, not their incompatibility.
3. If using section 6 on the source rather than as a conditional geometric
   lemma, verify its genuine eight-gon hypothesis in that same source.

No complete three-fibre exclusion or smaller bad source is proved. No new
finite-patch search, external theorem, source realization, ordinary-matching
claim, even-complement positivity, full319 conclusion, or Lean theorem is
introduced by this paper audit.
