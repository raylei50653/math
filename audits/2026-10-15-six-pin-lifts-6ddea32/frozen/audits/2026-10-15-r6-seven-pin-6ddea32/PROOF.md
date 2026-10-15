# A precise limit of the facial-triangle partition refinement

BASE: `6ddea32a81349821ad3724ae1652bddb9c6a7b04`.
This is a finite representation identity and an explicit plane-graph
counterexample to a weaker proposed statement. It does not exclude or
realize a minimum source.

## 1. Original source and the proposed extra information

The original minimum-source contract is the one frozen in INPUTS.json:
G has ordered C5 boundary `(x,y,a,b,c)`, minimum inner order k outside K132,
maximum edge count at that order, and original x,y,b degree four. In the
r-degree-six branch, identify a,c as z and perform the prescribed deletions,
obtaining U with actual induced outer C5 `(z,s,v,w,t)` and actual inner
triangular face `zpq`. The pins are distinct and ordered
`(z,s,v,w,t,p,q)`. Every original remaining edge is retained. U has k total
vertices; p,q are internal. Its complete outer support is exactly319.

For every complete U colouring, every legal colour of r on its neighbours
`s,v,w,t` must satisfy the inherited JOINT6 condition. There are 26 S4
orbits of pin rows passing that necessary all-r screen. Rows with no r
lift are retained. The previous necessary Kempe fixed point has 22 rows.
Nothing in this audit changes that original source contract.

The old partition relaxation uses the five honest outer terminals and
mandatory edges of C5 plus triangle zpq. A natural proposed refinement
also uses that zpq is an actual face, with the fixed wedge order at z.
The precise refinement below adds no restriction to the old relaxation.
This assertion is limited to this partition abstraction; it does not say
that all arguments using the facial triangle are ineffective.

## 2. Cutting the common boundary vertex correctly

The two faces have disjoint interiors and their closures meet only at z.
Split z along these two face sectors into z_left and z_right, distributing
its incident original edges according to the original rotation. The
resulting boundary order is

`(z_left,s,v,w,t,z_right,p,q)`.

The boundary edges are the eight consecutive pairs. In particular z_left
inherits zs,zq, and z_right inherits zt,zp. All unspecified incident edges
stay in their actual wedge. Both copies have the same literal colour.
An entire reflection reverses the whole order; it does not permit
independent reflection or recolouring of the inner triangle.

For one complementary colour pairing, such as AB|CD, the actual maximal
components induce a noncrossing partition of these eight boundary
positions. Splitting z can split its original component into at most two
components: each resulting piece must contain one copy of z, since before
the split every vertex of that component had a path to z. No component
not containing z changes. When the copies are identified again, the
blocks containing the two copies merge.

Consequently a necessary refinement of an old seven-terminal partition
is the existence of an eight-position noncrossing partition that:

1. has blocks confined to one complementary colour pair;
2. joins endpoints of each bichromatic boundary edge;
3. projects to the specified original partition when both copies of z are
   identified and their two blocks merged.

It would be incorrect to require the two copies of z to remain connected
in the cut graph. For example, for row ABABCBC and pairing AB|CD, the old
partition has AB block `{z,s,v,w,p}` and CD block `{t,q}`. A cut witness is

`AB: {z_left,s,v,w}, {z_right,p}; CD: {t,q}`.

It is noncrossing in the stated eight-position order. Merging the two AB
blocks before the noncrossing test creates alternating positions
`w,t,z_right,q`, incorrectly rejecting this option. Equal colours of the
copies do not imply connectivity in the graph after splitting. The separate
`check_unsplit.py` exhaustively enumerates the unsplit projected set and
checks that this exact option is absent; it does not infer absence merely
from the first stored split witness. Across all180 cases, the unsplit
restriction removes660 old options. Those abstract options alone are not
asserted to be realized by source graphs.

## 3. Exact finite identity, including all proper rows

For every proper assignment of colours to C5 and triangle zpq, and for
each complementary pairing, the set of original terminal partitions in
the old model is exactly the projection of the cut model from section2.
This is a finite identity, verified exhaustively with two independently
implemented partition constructions:

- 60 canonical proper seven-pin rows, representing all 1,440 labelled rows;
- all three pairings, hence 180 row/pairing cases;
- exactly 1,080 old partition options, all with explicit cut witnesses;
- zero additional or missing projected options.

The old side uses the frozen recursive-insertion implementation. The cut
side independently enumerates restricted-growth strings on each colour
pair's boundary positions, tests all alternating quadruples among eight
positions, and only then identifies the copies of z. It is not a search
only over refinements already assumed to pass the old test. Set equality
therefore checks both directions. Global colour permutations account for
every labelled row, since a proper C5 uses at least three colours and has
trivial stabilizer under S4.

Among the 26 rows passing all r lifts, there are 468 partition options
before requiring switch successors to remain in the upper relation. The
same 22 rows survive the necessary fixed point. The first round removes
exactly ABACDBC, ABACDCB, ABCADCD, ABCADDC, as in the old control.
Every option has exactly the same projected switch successors after the
refinement, because switching a component occurs in the original graph:
when the z component was split, its two pieces must be switched together.
Thus any count model built exclusively from these original projected
switch orbits also receives no new constraints from this refinement.
We have not solved another count program or checked realizability of
components across different pairings.

This finite identity says that the specified extra face-partition
relaxation is redundant. It supplies no plane graph realizing one of its
rows, partitions, switch systems, or count witnesses. Unrecorded original
edges and compatibility between different pairings remain possible
sources of stronger constraints.

## 4. Explicit counterexample to a weaker graph statement

The assertion

> An induced outer C5 with support319 and an inner facial triangle zpq
> sharing only z with the outer C5 must have a nonfacial triangle

is false, even for a simple triangulated disk whose three internal
vertices all have degree at least four.

Use vertices0,...,7, outer order `(0,1,2,3,4)` and seven pins
`(z,s,v,w,t,p,q)=(0,1,2,3,4,6,5)`. Vertex7 is an additional interior vertex.
Besides the outer cycle, the edges are

`05,25,35,06,36,46,07,17,27,56,57`.

One exact straight-line drawing is

`0=(0,4), 1=(-4,1), 2=(-3,-3), 3=(3,-3), 4=(4,1),`
`5=(0,0), 6=(2,1), 7=(-2,1)`.

Its nine bounded facial triangles, written as unordered sets, are

`017,046,056,057,127,235,257,346,356`.

These are all triangles of the graph. The face z-p-q is056. The graph
therefore has no nonfacial triangle. Its fixed-outer complete-fibre count
vector in the frozen ten-row order is

`(1,2,1,2,1,1,0,0,1,0)`,

so its exact outer support is319. There are 216 complete labelled
colourings. A propagation recursion and an independent direct test of
all4^8 assignments agree on the entire set. The certificate includes all
216, every one of the ten outer fibres, and all60 canonical seven-pin
fibres including the empty ones. The literal p/q order is retained.

This graph is the known small319 representative, reconstructed and checked
here as a counterexample to the proposed weaker structural statement. It
is not presented as a newly discovered graph or a counterexample to the
actual source claim.

It fails the actual source hypotheses in several concrete ways:

- U-degrees of s,t are3, whereas r6 sources require at least4.
- U-degree of z is5. In the original fixed branch it is `h+4>=7`.
- Original-source forbidden cross edges occur: p-w, q-v and q-w.
- It fails the all-r JOINT6 requirement. For example its complete U
  colouring `ABABCCDD` in vertex order0,...,7 has seven-pin row ABABCDC;
  the only r colour is D, but the required pq palette BC is instead DC.
- It has only three U interior vertices. The actual current minimum-source
  size and global minimality/normal-form hypotheses are not satisfied.

These failures are recorded, not repaired by independently replacing
fibres or by relabelling p,q after the computation. Thus the weak
counterexample only proves that support319, facial zpq and absence of
nonfacial triangles alone are insufficient to describe the source.

## 5. Scope and next mathematical obligation

The original arbitrary-size r6/319 exclusion remains OPEN. This audit
shows that adding the one touching facial triangle to the specified
single-pair noncrossing partition model cannot provide that exclusion.
A successful argument must add information absent from this model, such
as original degree and collar restrictions, more retained vertices, or
compatibility of actual components across different pairings and
successive switches. No claim here supplies such an argument.

Paper scope: the cut operation and the necessity of its relaxation.
Finite scope: the exact equality of the two partition spaces and the
complete explicit weak graph control. Genuine target sources: zero,
`not triggered`. New source exclusion, increased k bound, 4CT invocation,
Lean theorem, and publication/merge action: none.
