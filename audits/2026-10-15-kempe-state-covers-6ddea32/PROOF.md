# A genuine two-sheet common-graph cover of Layer0

BASE `6ddea32a81349821ad3724ae1652bddb9c6a7b04`.
Inputs are frozen in [INPUTS.json](INPUTS.json). The old720-state table is unchanged.

## 1. Main result and its exact scope

There is a connected simple graph H on **75 vertices and353 edges**, with seven
pairwise distinct ordered original pins `(z,s,v,w,t,p,q)`, such that:

1. H has exactly864 complete labelled proper four-colourings.
2. They project two-to-one onto the432 states of the old table's **Layer0**.
3. In every complete colouring, all six two-colour component partitions on the
   seven pins are exactly the stored partitions of the projected state.
4. Every stored visible component switch is induced by switching the unique
   corresponding maximal component in this **same original graph H**.
5. Every maximal two-colour component meets the pins. There are no hidden
   components, in any of the864 complete colourings.
6. The projection commutes with the full global S4 action.
7. A six-switch closed walk in the base exchanges the two full colourings above
   a state. Thus there is **no section compatible with all visible switches**,
   even before asking that a section also be S4-equivariant.

The exact graph is [graph-75.json](graph-75.json). Its SHA256 is
`e78e3dfb3b6a7ea7458cb4b42b93d605fd3c06941da5314c497c280f06158bd6`.
A second graph on121 vertices and711 edges has the same properties and is stored
in [graph-121.json](graph-121.json), SHA256
`dfcbffbe01ec168e85c525d956105f79262db4bfbcdc0429476a57fd4e763c11`.

These are genuine complete-colouring common-graph witnesses for Layer0, not
merely abstract switch systems or selected colouring subsets. They have18
canonical seven-pin rows and exact outer mask319. They do **not** cover the full
720-state/five-layer table or all22 canonical rows. Both displayed graphs are
nonplanar:353>3·75−6 and711>3·121−6. This proves nonplanarity of these two graphs
only; it does not exclude a suitable planar subgraph, another graph, or a
realization that duplicates colour-function types. No original degree/collar
source is supplied and no source exclusion follows.

## 2. Projection, hidden switches, and sections

For a graph H, use its entire set `Col4(H)` of proper labelled four-colourings.
A cover of a specified invariant subsystem X of the stored table consists of a
surjection `pi:Col4(H)->X` with these requirements:

- Every colouring has the literal ordered pin row and all six terminal
  partitions stored at its image.
- If B is a stored ab block, switch the actual maximal ab component containing
  those pins. The resulting full colouring projects to the stored successor
  `T_(ab,B)(x)`. These actual switches are involutions and give bijections
  between the corresponding fibres.
- `pi(sigma F)=sigma pi(F)` for every global colour permutation sigma, without
  changing any original vertex, edge, pin, or attachment identity.

A hidden-component switch always preserves the literal pin row. For the full
720-state table, that alone need not preserve the abstract state: the same
literal row can occur in different layers. Thus a general projection may send a
hidden switch to another state with the same row. The additional requirement
that every hidden switch stays in its abstract-state fibre defines a
**hidden-loop cover**. It is not silently imposed on all possible sources.
Layer0 has exactly one abstract state for each literal pin row, so this
qualification disappears there. The two constructed covers have no hidden
components anyway.

An m-sheet cover has m full colourings in every abstract-state fibre. A section
chooses one full colouring F_x above each x; switch compatibility requires
`F_(T(x))` to be the actual switch of F_x. A choice of one colouring per state
without this compatibility is not a section usable in the previous audit's
colour-function argument. The six-step monodromy below proves that such a
compatible choice need not exist in a genuine finite graph cover.

## 3. A sharp hidden-component fibre bound

Fix one complete colouring F of an arbitrary finite graph with named pins. Let
`h_ab` be the number of maximal ab components avoiding every pin. For each of the
three complementary pairings `P=ab|cd`, set `H_P=h_ab+h_cd`. Let `m_pin(F)` be the
number of **all complete colourings with the same literal pin row as F**. Then

    m_pin(F) >= 1 + sum_P (2^H_P - 1)
             = 2^H_AB|CD + 2^H_AC|BD + 2^H_AD|BC - 2.

For one pairing, independently switch any subset of its hidden components.
Their original vertex sets are disjoint, remain the same throughout that cube,
and are all nonempty. Consequently its2^H_P outputs are distinct and all have
the same pin row. Two nonidentity outputs from different complementary
pairings cannot coincide: choose a vertex whose colour changed. The unordered
pair consisting of its old and new colours belongs to exactly one of the
three complementary pairings, contradicting membership in both. The three
cubes therefore meet only at F. This proves the bound directly.

This also implies the weaker six-pair bound
`m_pin(F)>=1+sum_ab(2^h_ab-1)`. If `m_pin(F)=2`, at most one hidden component
exists among all six colour pairs. This is a bound on the literal-pin fibre.
For a hidden-loop cover one can apply the same argument within its state
fibre; for a general full720 projection, the unconditional right comparison is
`m_pin(r)=sum_{x with row r}|pi^-1(x)|`, not one selected state's sheet count.

A small genuine no-section control is the planar diamond with edges
`01,02,12,13,23`, pins0,1,2, and hidden vertex3. It has48 complete colourings
above24 K3 pin states, two per state. At row ABC, vertex3 has colour A or D.
The visible AD component containing pin0 is `{0}`, while `{3}` is hidden.
Switching `{0}` has the same base effect as global A/D renaming, but fixes
vertex3. Global renaming changes vertex3 in both lifts, so no compatible
S4-equivariant section exists. The hidden-fibre bound is exactly2 here.
The larger witnesses strengthen this control by having **zero** hidden
components yet still having nontrivial cover monodromy.

## 4. Complete two-sheet visible-cube parametrization

This section classifies abstract two-sheet lifts of the fixed visible
transitions, S4 action, and same-pairing cubes. It does not assert graph
realizability of every such lift.

Because every base row uses at least three colours, its S4 orbit is free.
Label the two fibres over a canonical row by0,1, and transport these labels by
S4. In this gauge, a global colour permutation preserves the sheet label.
Each lifted visible edge then has a voltage `d_e in F2`: it sends sheet
`epsilon` to `epsilon+d_e`. Reversibility makes the voltage undirected; S4
covariance makes it constant on each S4 orbit of edges. Cube commutation is
exactly the equation that every square has voltage sum0. These equations are
also sufficient: squares generate every closed walk within a Boolean cube,
so lifting a whole cube is independent of the order of its component bits.

Changing the chosen labels above a canonical row adds its coboundary to all
incident voltages. Thus quotienting by this gauge space classifies covers up to
an isomorphism over the identity base that commutes with S4. `space.py` records
all edge orbits and every linear equation, computes ranks by exact GF2
elimination, and records a basis for the subdomain described below.

| Layer | Canonical rows | Edge orbits | Square rank | Solution dimension | Gauge rank | Quotient dimension |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 18 | 112 | 30 | 82 | 17 | 65 |
| 1,2,3,4, each | 3 | 18 | 3 | 15 | 2 | 13 |
| All five | 30 | 184 | 42 | 142 | 25 | 117 |

There are consequently2^117 abstract two-sheet visible-cube/S4 cover classes
of the full table in this sense. Hidden-component and original-edge conditions
have not yet been imposed on that entire family.

A useful **additional restriction** requires the product of all visible
switches in each one colour pair to equal the global transposition on the
lifted state. This gives further linear equations: the voltage sum along that
product must vanish. It is not a necessary law for arbitrary covers with hidden
components. For a genuine graph satisfying it, all pair components are visible:
the product of every hidden component would otherwise change its nonempty
vertex set, while the full component product is global renaming.

In this restricted subdomain, Layer0 has kernel dimension26, gauge rank17,
and quotient dimension9; each smaller layer has kernel dimension3 and gauge
rank2. Hence2^13 full-table cover classes remain, with2^9=512 possibilities on
Layer0. Nonzero quotient voltage does not imply a section; the actual graphs
below provide an explicit failure.

## 5. Explicit graph construction and complete verification

The75-vertex witness uses the112 edge-orbit order saved in the certificate and
voltage

    0x448800114400001429.

Its nonzero indices are
`0,3,5,10,12,34,38,40,44,59,63,66,70`.
The121-vertex witness has voltage `0x1429`. These identifiers do not depend on
calling a result merely “search class101” or “class5”.

A graph file contains one36-entry vector per vertex, one original edge list,
and the ordered seven pin vertices. The36 entries are indexed by the18
canonical Layer0 rows, each with its two sheets. At literal state x and sheet
j, transport that canonical vector entry by the **one common S4 frame** mapping
its canonical pin row to x. This defines one full colouring on all original
vertices. The graph file fixes the same original edge set for all these
colourings and all colour pairs.

`check.py` verifies properness and distinctness of all864 displayed colourings.
It then independently enumerates **all** proper colourings of each original
graph, fixing the original pin triangle `(z,p,q)` to `(A,B,C)`. This loses only
the free global S4 factor24. Deterministic domain propagation followed by
branching over every remaining value finds exactly36 normalized colourings:
79 search nodes for the75-vertex graph and85 for the121-vertex graph. Their24
renamings are compared as whole vertex-colour tuples with the displayed864
states, and the sets agree exactly. Every pin row has exactly two complete
lifts; no extra colouring or empty fibre was silently omitted.

For each graph, direct original-edge BFS then checks:

| Complete check | Count |
| --- | ---: |
| Actual components and individual switches | 8,160 |
| Whole complementary-pair cube masks | 26,112 |
| Full-colouring S4 actions | 20,736 |
| Hidden components | 0 |

No terminal partition is selected independently of a full colouring. Every
actual switched full tuple is looked up in the same864-state set and its base
successor and sheet voltage are checked. The independent root verifier uses a
separate single-vertex DSATUR enumeration and original-edge BFS on the121-point
graph; the geometry reviewer independently does the same for the75-point graph.
Both obtain exactly36 normalized and864 labelled colourings and the same
components/switch counts, without importing this audit's implementation.

The discovery search examined512 restricted Layer0 voltage classes:458 fail the
old first weak type-graph path test,54 pass that test,10 pass the subsequent
strict cube/block tests, and2 survive repeated deletion of types lacking a path
to their designated visible pins. These search records are retained as
exploratory provenance in [SEARCH_NOTES.md](SEARCH_NOTES.md). The main positive
result does not depend on claiming a complete exclusion for the other classes:
it follows directly from the original graph files, complete colourings, and
all-component checks just described.

## 6. Six-step monodromy and the previous obstruction

For the75-vertex graph the following actual visible-switch walk starts at
`(state0,sheet0)` and ends at `(state0,sheet1)`:

| Base source | Base target | Pairing index | Component bit | Sheet change |
| --- | --- | ---: | ---: | ---: |
| ABABCBC | ABADCBC | 1 | 2 | 1 |
| ABADCBC | ABDACBC | 2 | 1 | 0 |
| ABDACBC | ABCACBC | 0 | 1 | 0 |
| ABCACBC | ACBACBC | 2 | 1 | 0 |
| ACBACBC | ACABCBC | 0 | 1 | 0 |
| ACABCBC | ABABCBC | 2 | 1 | 0 |

The pairing order and bit order are exactly the frozen old table's orders.
The total voltage is1. The same walk also exchanges sheets in the121-vertex
graph. If a section respected all visible switches, following this closed base
walk would both preserve its selected full colouring over state0 and exchange
it with the other full colouring. This is a contradiction.

Thus the previous25-type no-section obstruction cannot be upgraded to an
arbitrary finite-cover obstruction merely by assuming that a compatible
section exists. Here a common graph really does exist, with complete colourings
and all stored Layer0 partitions, while that section does not. Each original
vertex instead has a colour function on the **864 lifted states**. Replacing
its two correlated sheet values by independent marginals would discard the
very information that permits the common original edges.

## 7. Boundaries retained

The75/121 graphs demonstrate a two-sheet cover of Layer0,18 canonical rows,
and outer support319. They do not cover all five layers or all22 rows. Their
nonplanarity does not prove the absence of a planar realization or an edge
subgraph preserving all required components. The original degrees, nonedges,
rotation, collar, global minimality and completed-source contract are not
supplied. General hidden-state covers of the full720 table, full22-row/source
realizability, complete319 source exclusion, omega=0, and the general main
claim remain OPEN. No new source order bound or Lean theorem is claimed.
No old audit/shared document was edited and no commit or push was performed.
