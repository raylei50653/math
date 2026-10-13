# Common supports, branching, loops, and clique overlaps

This is an isolated constructive four-color audit. Every graph and every pin is
literal. Colors are the single global frame `0,1,2,3`. The examples are not
claimed to be low-excess, Sigma-critical sources in the original C5 problem.

## 1. An ordinary path does not transmit a named inequality

Fix `v0=2` on a path of `n` vertices. There are exactly `3^(n-1)` full
colorings. At one edge, the other endpoint must differ from `v0`. At distance
two or greater, all four endpoint colors occur. The length-two witnesses
`(v0,v1,v2)=(2,0,2)` and `(2,0,1)` exhibit equality and inequality on the same
literal path and frame. Thus composing edges alone never makes inequality
transitive.

## 2. Reusing two literal support vertices

Let `T` be a nonempty connected tree. Add vertices `a,b`, the edge `ab`, and
every edge from each hub to every vertex of `T`. Write this graph as `K2 join T`.

* The graph is planar **if and only if `T` is a path**, allowing a one-vertex
  path. If `T` has a degree-three vertex `v` with neighbors `x,y,z`, the nine
  cross-edges between `{a,b,v}` and `{x,y,z}` form a literal `K3,3` subgraph.
  Extra edges such as `ab` do not remove that obstruction.
* Conversely, for a path `v0,...,v(n-1)`, start with triangle `a,b,v0`; insert
  each subsequent `vi` in the active triangular face `a,b,v(i-1)`, joined to
  its three corners. This proves planarity for every path length.
* Pinning `a=0,b=1,v0=2` leaves exactly one coloring: `vi=2` for even `i`,
  and `vi=3` for odd `i`. Without pins there are exactly 24 colorings.
  In particular, arbitrarily separated path indices of opposite parity have
  forced different colors, including nonadjacent vertices.
* This construction has **ambient graph distance at most two** between path
  vertices, because either hub is a shortcut. Its arbitrarily long path index
  is not an arbitrarily large metric propagation distance.

The same degree-three obstruction persists if `ab` is deleted. With distinct
external pins on `a,b`, the coloring relation also remains unchanged. Without
that edge or distinct pins, `a=b` becomes possible; the tree then has three
available colors, so nonadjacent parity forcing disappears. With `a=b=0` and
`v0=2`, a path has `2^(n-1)` full colorings.

For example, the planar graph on `(v0,v1,v2,v3,a,b)` has the complete pinned
coloring list `[(2,3,2,3,0,1)]`. Replacing the path by the three-leaf star gives
the complete pinned list `[(2,3,3,3,0,1)]` but makes the graph nonplanar.
Color consistency therefore does not certify a noncrossing realization.

## 3. Closing a common-support wire

Replace `T` by a cycle `C_n`, `n>=3`.

* With the edge `ab`, the graph has `N=n+2` vertices and `3n+1=3N-5` edges.
  It is nonplanar by the simple planar edge bound. Even cycles remain fully
  color-consistent under distinct hub pins; odd cycles have no extension.
* Without `ab`, the suspension of the cycle is planar: put one hub on either
  side of the cycle. Distinct hub pins extend exactly when `n` is even.
* Without any pin forcing `a!=b`, an odd cycle forces `a=b`: the cycle uses
  at least three colors, and both hubs must use its remaining fourth color.
  Even cycles allow both equal and distinct hub colors.

Thus removing an edge can restore a planar closed wire, but can also remove
the source of the distinct support colors. The two requirements must be
checked together in the same graph.

## 4. Sharing a vertex, edge, or triangle between tetrahedra

Take several copies of `K4` sharing the same clique, with all other vertices
distinct. Pin all four colors on the first copy.

| Shared clique | Choices per additional copy | Relation between named private vertices on different copies | Planarity |
| --- | ---: | --- | --- |
| one vertex | 6 | equality and inequality both possible | any number of copies |
| one edge | 2 | equality and inequality both possible | any number of copies |
| one triangle | 1 | private apex colors forced equal | at most two copies |

The counts are `(4-t)!` for clique size `t`: these are independent
permutations of the unshared palette, not extra global color renamings.
For an edge overlap, the two full vectors are
`(s0,s1,p00,p01,p10,p11)=(0,1,2,3,2,3)` and `(0,1,2,3,3,2)`.
The unordered complementary pair transfers; the named private color does not.

For triangle overlap, two apexes are forced equal and can occupy opposite
sides of the triangle. A third apex produces a literal `K3,3` between the
three triangle vertices and three apexes. This obstruction applies to reuse
of the *same* triangle, not to recursively inserting vertices in different
new triangular faces.

Planarity for arbitrarily many edge-overlap copies can be seen by drawing
`K2` joined to a matching: order each matched pair consecutively around the
two-hub embedding and draw its matching edge in the intervening face.

## 5. Distinct support vertices with externally imposed colors

For each vertex `v` of any tree `T`, add two private leaves `a_v,b_v` and
externally pin them to `0,1`. The literal graph remains a tree, hence planar,
with arbitrary branching. With one root of `T` pinned to `2`, every vertex
of `T` has one determined parity color in `{2,3}`.

This is a valid full-precoloring example, and it uses distinct literal support
vertices. It does **not** construct a graph mechanism enforcing all the
support equalities. If the leaf pins are removed, the graph is simply a tree:
with its root fixed, each other vertex has three choices, and the desired
nonadjacent forced relations disappear. The example identifies the missing
source obligation rather than silently supplying it.

## Reproduction and evidence

Run from the repository root:

```sh
.venv/bin/python audits/2026-10-13-forced-inequality-19209f4c/alternatives/check_alternatives.py --check audits/2026-10-13-forced-inequality-19209f4c/alternatives/results.v2.json
env PYTHONHASHSEED=17 .venv/bin/python audits/2026-10-13-forced-inequality-19209f4c/alternatives/check_alternatives.py --check audits/2026-10-13-forced-inequality-19209f4c/alternatives/results.v2.json
```

Both read-only replays exactly matched `results.v2.json`, SHA-256
`9ab6ced92935226e683e7fe88ebc49f5962dfa31487a001c35a96791b4ce985e`.
Generation requires explicit `--write PATH` and exclusively creates the new
path; existing artifacts cannot be overwritten. The earlier `results.json`
is retained as the initial record; `results.v2.json` adds all 16 terminal
fibres explicitly, including empty cells.
There are **84 cases**, of which **81 are completely enumerated**, containing
**12,650 full proper colorings** altogether. Three large unpinned private-leaf
trees are explicitly marked formula-only. Tested ranges are paths with 2--8
vertices, stars with 1--5 leaves, cycles with 3--8 vertices, and clique books
with 2--5 pages. The infinite family claims above have separate elementary
proofs; the finite tests are calibration, not their substitute.

Every enumerated row stores the literal node order, edges, pins, complete
coloring vectors, complete terminal relation and fibres, equality/difference witnesses,
and either a planar rotation system or a Kuratowski edge certificate. Empty
relations occur in the odd closed-wire cases with distinct hub pins. No
four-color theorem oracle is used.
