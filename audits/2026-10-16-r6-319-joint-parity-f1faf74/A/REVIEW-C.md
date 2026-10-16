# Independent review of C: marked four-cuts and the common-H two-cap screen

Reviewed against the root's frozen source contract at BASE
`f1faf743833c51ddc5efbe9e0f390b87b9f2311d`.
The current `C/PROOF.md` and `C/explore_shared_caps.py` were read directly.
This review writes only A files and imports no C checker.

**Accepted within the stated necessary scope:** every actual cyclic
four-cut avoids e,f; and, conditionally on original `d_G(v)=5`, both
actual five-boundary completions must have full outer mask1022.
The latter is finite certificate-backed narrowing under the already
assumed K132 authority, not a source realization or v5 exclusion.

## 1. Geometry and smaller comparison graphs

For a cyclic four-cut the frozen primal argument gives an induced C4
meeting m or z. A C4 containing vw cannot contain m without a chord
and cannot contain z without zv or zw. A C4 containing pq cannot
contain z without a chord. In the remaining order `(p,q,A,m)`, the
mp edge means original a-degree4 and hence c-degree at least7.
The frozen common-neighbour identity then reduces possible A to z,p;
one repeats a cycle vertex and the other introduces the zp chord.
The reflected order is identical. The new theorem is sound; it does
not identify an odd complementary cycle with an edge cut.

For original v-degree5, its original neighbours `(r,w,i,j,s)` are
distinct, and i,j are different from p,q because pv,qv are absent.
Deleting v from the actual U exposes the simple boundary
`(z,s,j,i,w,t)`. The old graph may have further chords; none are
deleted by this construction. Original no-separating-triangle geometry
excludes si and jw, the only new edges used by the two completions.
Drawing si along the exposed s-j-i arc leaves the actual C5 boundary
`(z,s,i,w,t)` and puts j inside. The reflected jw operation does the
same for `(z,s,j,w,t)`. Each graph has `k-1` total vertices and `k-6`
interior vertices, within the original smaller-C5 comparison class.
There is no assumed general planar-colourability theorem.

## 2. Why the two masks can legitimately constrain one full H relation

Let H be this one actual graph U-v. The map deleting the added edge
is a bijection from complete colourings of V_i to complete H
colourings satisfying `s!=i`; all other vertices retain their original
private colours. Likewise Col(V_j) is exactly the `j!=w` subset of
the same Col(H). Thus if their actual complete outer masks are M_i
and M_j, every full H colouring simultaneously satisfies the two
appropriate implications:

`s!=i ==> boundary_i belongs to M_i`,
`j!=w ==> boundary_j belongs to M_j`.

When an antecedent fails, that cap projection is empty, not a rejected
H colouring. Applying both implications row by row is sound and does
not combine independent witnesses. It is essential that H itself,
not a chosen cap, is the graph used for subsequent component swaps.

For every complete H colouring, the legal v colours are exactly those
avoiding s,j,i,w. Each such lift has all its r colours avoiding
s,v,w,t. All pairs of legal lifts must satisfy the original return
rule. A colouring with an empty v fibre is retained, as is a legal
v lift with an empty r fibre. Projecting all v lifts produces exactly
the full U outer support. Thus the required projected support319 is
an equality of a complete same-graph relation, not an existence claim
about individually selectable v or r colours.

## 3. Finite Kempe necessity and independent reconstruction

C enumerates component partitions for the two complementary palettes.
Every retained visible same-palette edge joins its endpoints within
one component. Two different actual components cannot have alternating
endpoints on H's literal six-vertex outer boundary; testing all ordered
four-subsets of those six vertices is a valid necessary Jordan test.
Interior p,q are not assigned a fictitious outer order. Every whole
component subset is switched, including both complementary palettes,
before one common normalization. This preserves necessity through
each greatest-fixed-point removal.

The independent [checker](review_c_independent.py) rebuilds partitions
by restricted-growth strings and tests alternating arcs by a different
implementation. It derives the initial table from the original literal
R palette table, not C's formula or saved upper rows. It imports no C
module. Normal and seed17 independently agree with every one of C's
1521 candidate-pair records:

| Quantity | Rebuilt result |
| --- | ---: |
| All eight-pin assignments | 65536 |
| Proper assignments with empty v fibre | 1008 |
| Empty r fibres over proper H assignments and legal v lifts | 864 |
| Canonical full-lift upper rows | 99 |
| Closure sizes | 99,85,83,81 |
| Candidate actual-mask pairs | 1521 |
| Surviving pair | (1022,1022) |
| Remaining necessary H rows | 81 |

Receipts are `independent-C-normal.json`, `independent-C-seed17.json`
and their full subprocess records under `logs/`. The K132 bytes have
SHA256 `04650cea947a5086360e895c1a7350690f53da745314379a3328b97ee02d81b8`,
matching the pre-existing catalogue and frozen degree4 copy. The root
records this new explicit input separately in ADDITIONAL_INPUTS.json,
leaving the original BASE manifest unchanged.

## 4. Original nine-boundary split check

Deleting original x,y,b,r,v from G, before identifying a,c, exposes
the actual simple boundary `(c,s,j,i,w,t,a,p,q)`. The two original
vertices a,c remain distinct. Full H colourings pull back exactly to
full colourings of this graph with `a=c=z`, including every private
vertex. Its nine boundary edges map to the retained H skeleton.

The actual two-colour components of the split graph need not connect
a to c. Under the actual quotient a=c, components containing either
copy merge into a single component; every other component is unchanged.
The two copies have the same colour, so they occur in the same palette.
Thus testing the actual nine-boundary noncrossing condition first,
then merging precisely the a/c components, gives a valid necessary
class of whole-H component swaps. C's `opts9` follows this order and
does not impose a pre-existing path between the split copies.

The independent checker reconstructs these split partitions and
component mergers without importing C code. It reproduces all closure
sizes and all1521 pair decisions: the stable relation remains81 rows
and the unique pair remains `(1022,1022)`. The extra geometric test is
legitimate but gives no additional exclusion in this finite screen.

## 5. Boundary of the conclusion

The exact conditional consequence is that if the genuine original
v5 branch exists, its two actual cap masks are1022. Since1022 omits
only ABABC among the ten canonical C5 frames, this is a useful strong
necessary constraint. It does not construct an H realizing the81
surviving rows, identify their multiplicities, or show that every
permitted component partition is realizable. The actual full H
relation can be a proper subrelation with the same three projections.
There are zero supplied minimum sources, so source checking remains
`not triggered`.

There is no smaller bad-source conclusion: restoring v after removing
the added cap edge and then restoring the original source returns
`(k-1)+1+5=k+5`. Joint even-complement positivity, v/w degree-five
exclusion, and complete319 remain OPEN.
