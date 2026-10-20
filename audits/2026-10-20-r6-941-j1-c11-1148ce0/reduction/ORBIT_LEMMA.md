# Same-source complementary-pair orbit counts

Fix the entire actual triangulated disk
`F'=G-{b,p,h,R,x,y,r}` with ordered rim
`(a,n,u2,u1,L,q,c,s,v,w,t)` and every original private vertex and edge.
For a canonical proper four-colour rim state i, let z_i be its complete
fixed-labelled-colour extension count. Global colour permutations give
bijections between the corresponding full fibres. This is a single common
count vector, with all frozen proved-zero coordinates equal to zero.

## Actual complete orbits

Use the fixed colour split `{0,1}|{2,3}`. For every complete colouring,
partition all vertices into connected components of the two induced palette
subgraphs. Independently interchanging0/1 or2/3 on any whole component gives
another proper complete colouring. The palette membership and its connected
components remain unchanged under every such exchange. Therefore these
exchanges partition the finite set of complete colourings into disjoint
orbits. If an orbit has b components meeting the rim and c components meeting
no rim vertex, its size is exactly2^(b+c).

Its rim projection has exactly2^b distinct literal tuples: each boundary
component contains a rim vertex whose colour changes when that component is
flipped. Each projected tuple has exactly2^c full members of this same orbit.
The count2^c includes every private vertex and every component invisible from
the rim; no private attachment is discarded or recoloured independently of
its actual connected component.

## Why every actual boundary partition is in the frozen family

The boundary-contact partition of the b actual components is noncrossing,
by the planar embedding and the disjointness of the components. The palette
sides of consecutive blocks are opposite whenever the blocks differ.

There is also the exact triangulation identity

```
number of palette changes around the rim = 2(b-1).
```

One way to see this is to draw, in every original triangular face, the arc
joining the midpoints of its two edges whose endpoint palette sides differ.
A proper triangle uses three colours, so it has precisely two such edges.
The face arcs join through interior edges into pairwise disjoint closed
curves and properly embedded open arcs. Every open arc ends at two rim
palette changes. If there are m open arcs, they cut the disk into m+1 regions
meeting the rim. Closed curves only enclose components invisible from the
rim and do not alter this number. The regions meeting the rim are exactly
the b connected palette components meeting the rim: the face construction
is the boundary of a regular neighbourhood of the palette subgraphs.
Consequently b=m+1 and the rim has2m=2(b-1) changes. Equivalently, adjacency
of these boundary regions is a tree, whose sides have the two palette labels.

The frozen enumerator lists all noncrossing partitions, retains precisely
those with this transition count and a bipartite block-adjacency graph, and
assigns the two possible palette-side orientations. Hence it includes the
boundary partition of every actual complete colouring. Extra enumerated
partitions, if any, only enlarge the necessary cone. This is a paper planar
argument about the actual disk; it is not established merely by enumeration.

## Exact normalization and the shared count identity

Let H be the eight global permutations preserving the unordered palette pair
`{{0,1},{2,3}}`. Frozen half-state rows are the H-orbits of proper literal rim
colourings. Every proper C11 colouring uses at least three colours, so its
H-stabilizer is trivial. The frozen `hsize` is thus8; retaining that recorded
size also avoids depending on this simplification.

For half-state h let i(h) be its canonical full-S4 state. The number of
complete colourings whose literal rim lies in h is exactly

```
A[h,i(h)] z[i(h)] = hsize[h] z[i(h)].
```

The frozen column for a boundary partition and a representative rim tuple
records, for every h, how many of its2^b independently flipped literal tuples
fall in h. This is the integer column B[:,j]. Replacing a literal representative
by its H-canonical representative preserves this aggregated column, so an
actual orbit always maps to one of the generated columns.

Sum over the disjoint actual complete orbits and group equal columns. If
`X_j` is the sum of2^c over actual orbits producing column j, then

```
A z = B X,             z >= 0,   X >= 0.
```

In fact these source weights are nonnegative integers. Passing to nonnegative
real weights enlarges the feasible set and is legitimate for a separating
identity. Every palette row uses the same z, so the equation does not combine
independently feasible colour-pair models or different original graphs.

No signed planar-span representation is needed for this identity.

## Strict positive quantity

The selected original J1 W5 three-edge path supplies an actual complete
F' colouring with rim
`(0,1,2,1,2,3,1,2,e0,e1,2)`, where `(e0,e1)` is either `(0,1)` or `(1,0)`.
The frozen canonical IDs are5093 and5100. Therefore

```
z[5093] + z[5100] > 0.
```

Neither summand is separately required to be positive. A complete exact
certificate deriving its sum to be zero from `A z = B X`, the frozen zero
coordinates, and nonnegativity would exclude this source branch directly,
without constructing a smaller candidate or importing a signed-span theorem.

## The checked 132-term cancellation

The frozen necessary-live set L has5951 core states. A half-state is live
precisely when its canonical core state is in L. There are17853 live
half-states. Every other half-state has actual full count zero. Since all
entries of B and all actual orbit weights X are nonnegative, any column
having a nonzero entry in one of those zero rows has X_j=0. Exactly20794
columns remain after this logically justified elimination.

The derived `reduced-orbit-certificate.json` gives a function λ on the live
half-state rows with exactly132 nonzero integer values:64 entries+1 and68
entries−1. Direct integer evaluation gives both identities

```
Σ_h λ_h A[h,i] = -16,   if i is5093 or5100;
Σ_h λ_h A[h,i] =   0,   for every other i in L;

Σ_h λ_h B[h,j] = 0,     for every one of the20794 remaining columns j.
```

The second identity is equality for every surviving column; no rounding,
strict slack, optimization status, or signed-span equation is used. Multiply
the actual common source equation `A z = B X` by λ after the zero-column
elimination. The exact result is

```
-16 * (z[5093] + z[5100]) = 0.
```

This contradicts the actual selected short-witness positivity established
above. Consequently the named original J1 W5 three-edge-path source with
`d_G(n)>=6` and the induced C11 interface is impossible.

`verify_orbit_arithmetic.py` independently recomputes the original full
integer identity from the frozen K row and column data, without using the
discovery sparse equation matrices. `verify_reduced_orbit.py` additionally
checks every one of the132-term identities above against every live core
state and every surviving column. These checks do not replace the paper
source-to-orbit argument or the frozen upstream zero-fibre theorem.

The conclusion is confined to this named source branch. It constructs no
smaller bad candidate, invokes no four-colour theorem or matching premise,
and does not close every J1/J2 branch or add a Lean theorem.
