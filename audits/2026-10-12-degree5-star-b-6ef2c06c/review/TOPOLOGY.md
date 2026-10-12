# Fixed topology domain

This note concerns only topology and operation eligibility. `topology.py` does
not enumerate colourings and does not inspect transformation outcomes. It reads
only the frozen literal catalogue and its frozen cofacial v2 certificate. The
132 catalogue witnesses give 76 interior degree-5 marks. The separately named
literal `W5` source adds one mark, even though its edges equal the catalogue
witness for relation 91.

The upstream catalogue and cofacial v2 certificate do **not** supply historical
rotations. Consequently this control freezes one reconstructed disk embedding
per literal graph. It does not claim to recover unavailable historical rotations
or to test every embedding. The deterministic rule is NetworkX 3.5 planarity on
sorted nodes and sorted edges after adjoining an apex adjacent to all five
boundary labels; delete that apex; reflect the whole rotation when necessary so
that `[0,1,2,3,4]` is the forward outer facial walk. Every rotation list is then
cyclically normalized by its least neighbor. All 133 source records exist before
operation construction. No graph is recoloured during either phase.

The final domain SHA256 is
`2bcacec6f103d19962158ca38591f5f9c8f3708217b893d49b8a22a57fbedd01`.
The canonical JSON hash of the source records, including rotations, is
`a8b4561a3425b7b42f14e196c34b21ce3ced8e4c10417637c30648263d2366c4`.
One API-only revision changed operation kind strings and operation ordering
before outcomes were computed; it left every source record and rotation
unchanged. The root agent explicitly requested that revision.

| Domain item | Count |
| --- | ---: |
| Sources | 133 |
| Interior degree-5 marks | 77 |
| Original-mark boundary-pattern rows | 770 |
| Spoke deletions | 385 |
| Flip candidates / eligible flips | 385 / 345 |
| Set-partition candidates, including identity | 4004 |
| Eligible equality quotients | 290 |
| All eligible operations | 1020 |
| Operation boundary-pattern rows | 10200 |

Only 57 of the 77 cyclic neighbor lists actually have every successive link
edge. The other 20 are retained as cyclic lists without calling them a C5 link.
The histogram of numbers of boundary neighbors is `2:5, 3:55, 4:15, 5:2`.

## Inherited rotations

The graph record has sorted original integer `nodes`, unchanged named
`boundary=[0,1,2,3,4]`, sorted undirected `edges`, and a `rotation` object whose
string keys give clockwise neighbor lists. Faces use the dart successor
`(u,v) -> (v, predecessor_of_u_in_rotation[v])`, and each facial walk is
normalized only by a cyclic shift, never independently reversed. All graphs in
this domain are connected. Each recorded simple graph checks symmetric darts,
simple adjacency, Euler characteristic `V-E+F=2`, and the exact forward outer
face. All transformed rotations come from the following surgery, with no
planarity reembedding after the source rotation is chosen.

* Delete: erase both darts of the selected original spoke.
* Flip: inspect both directed incident face walks in the original rotation.
  They must be inner triangles with four distinct vertices in their union,
  and their opposite diagonal must be absent. Erase the spoke, obtaining the
  inherited quadrilateral face, and insert the new diagonal in its two face
  corners. The certificate keeps both original triangular walks and the
  quadrilateral walk.
* Quotient: delete the center, insert noncrossing chord trees into the five
  former spoke slots, contract their ribbons, and delete surplus parallel
  source edges. All original boundary edges are retained.

For the last operation, let the center's clockwise neighbor list be
`L=(l0,...,l4)`. A regular neighborhood of the embedded star provides a disk
with these five attachment sectors even when successive neighbors are not
adjacent in the source graph. A set partition is noncrossing precisely when
there are no positions `a<b<c<d` with `a,c` in one block and `b,d` in another.
For each nonsingleton block use the fan from its earliest `L` position. Such
fans have pairwise disjoint interiors. At `li`, replace its old spoke dart by
the new chord darts in order `l(i+1),...,l(i-1)`. This explicitly preserves the
outside source rotation and places every new arc inside the old star disk.

Ribbon contraction is recorded with persistent source-edge and chord IDs.
If the contracted edge has endpoint orders `(e,A)` and `(e,B)`, the merged
vertex has cyclic order `(A,B)`. The full intermediate ribbon rotations are
saved after every contraction. The final representative of a block is its
boundary label when one exists, otherwise its least original label. A block
containing two boundary labels is rejected. An original edge with both ends in
one block is rejected before any construction, so no original edge becomes a
loop. This original-graph nonadjacency condition does not exclude a pair merely
because its positions happen to be successive in `L`.

Every quotient edge has its complete original edge preimage, the retained
source edge, and the removed parallel preimages. The deterministic selection
retains an original boundary edge first and otherwise the lexicographically
least source edge. Erasing a parallel ribbon preserves the existing plane
embedding and has no effect on proper-colouring equality constraints. There
are 265 quotients with parallel simplification, removing 340 surplus source
edges in total.

All 52 restricted-growth strings are checked for each mark, including the
recorded but ineligible identity. Each candidate records its actual blocks,
crossing quadruples, boundary collisions, and adjacent identified pairs.
The 290 legal quotients consist of 275 single-pair identifications, 10
triple-block identifications, and 5 identifications of two disjoint pairs.
The explicit W5 has five deletions, five flips, and no legal quotient, because
every neighbor is an original boundary label.

## Source ownership

Each mark records the named interface `B union L`, each boundary label's
positions in the two cycles, all original spokes, and all bridges over that
interface. A bridge is either one component off the interface together with
all its incident edges and named support, or an original edge entirely in the
interface. These records partition the original edge set exactly. The center
component is explicitly marked. Components and cut edges of the deleted-center
graph are also recorded. Quotient maps and edge preimages transport these
original ownership records without inventing new independent contacts.

## Replay performed

Both commands passed against the final frozen domain:

```sh
PYTHONHASHSEED=0 .venv/bin/python audits/2026-10-12-degree5-star-b-6ef2c06c/controls/topology.py --check
PYTHONHASHSEED=17 .venv/bin/python audits/2026-10-12-degree5-star-b-6ef2c06c/controls/topology.py --check
```

These checks establish deterministic regeneration and the topology checks
implemented above. Independent topology and colouring verification is reported
separately by the main checker. This note makes no statement about relation
preservation, a minimum outside-catalogue source, or the general degree-5
reducibility problem.
