# A common-edge obstruction for the 720-state Kempe witness

BASE `6ddea32a81349821ad3724ae1652bddb9c6a7b04`.
[INPUTS.json](INPUTS.json) freezes the round-two witness and its stated source
contract; the third-round custody manifest is also frozen. No old file is edited.

## 1. Precise theorem and the unresolved boundary

**Theorem (finite certificate below).** The round-two 720-state witness has no
single-valued, S4-equivariant common-graph lift, on any finite number of vertices.
Already its 432-state Layer0 cannot have such a lift. The graph need not be
planar; no degree, collar, or seven-vertex size restriction is assumed.

The exact meaning of a lift here is a graph H with seven distinct ordered pins
`(z,s,v,w,t,p,q)` and a proper colouring `F_x:V(H)->{A,B,C,D}` for every abstract
state x, satisfying all three conditions:

1. `F_x` has the stored literal pin row at x. For every colour permutation sigma,
   `F_(sigma x)=sigma F_x` on **every original vertex**, with the round-two state
   action (layer fixed, literal row globally renamed).
2. For a stored visible ab-component switch `x -> y`, every original vertex u
   satisfies `F_y(u) in {F_x(u), tau_ab(F_x(u))}`. This is only a necessary law;
   it does not require the switched vertices to be one connected component.
3. Pins placed in the same stored ab block at x are connected in the induced
   subgraph `H[F_x^-1({a,b})]`. Even the requirement that different stored blocks
   be disconnected is unnecessary for this obstruction.

Every exact realization of all six partitions and all stored switch transitions
by one graph satisfies these three weaker requirements. Therefore the theorem
also rules out that exact realization. A realization need not have these states
as its complete colouring set, and distinct states need not be required to lift
to distinct full colourings: the argument does not use either restriction.

This is **not** a theorem that the 22 canonical rows lack a graph realization.
A graph could realize those pin rows with different partitions or transitions.
Nor does it rule out a many-state refinement/cover whose projection has hidden
colourings above an abstract state. Such a cover may have no single-valued,
S4-equivariant choice of representatives compatible with all stored transitions.
The theorem forbids that choice of representatives for this particular table.
In particular, it does not assume that a genuine target source has no hidden
components or that its visible switches multiply to a full global colour swap.

## 2. General colour-function lemma: one original edge set

For each original vertex u define its colour function

`f_u(x) = F_x(u)`.

Let T be **all** functions from the selected abstract state set to four colours
which satisfy condition 1's S4 covariance and condition 2's pointwise switch law.
Define the finite graph Q on T by

`fg is an edge of Q  <=>  f(x) != g(x) for every selected state x`.

If uv is an original edge of H, properness gives `f_u f_v in E(Q)`. Thus
`u -> f_u` is a graph homomorphism `H -> Q`. Two distinct original vertices may
have the same colour function, but adjacent vertices cannot: collapsing equal
functions creates no loop and loses no projected path. No assumption about the
number of original vertices is needed.

For a fixed x and colour pair ab, every ab-path in H maps to a walk in the
induced subgraph `Q[{f:f(x) in {a,b}}]`. Consequently:

> Every required same-component pin block must have all its pin functions in
> one component of this induced type graph.

This necessary condition uses one function for each original vertex across all
states, and one common original-edge constraint across all colour pairs. It is
stronger than choosing a separate connecting path for each pairing. Q includes
all admissible functions, even functions unused by H, and every allowable edge.
It is therefore an overapproximation: a missing path in Q proves a missing path
in every H. This is an arbitrary-finite-order obstruction, not a bounded graph
search with zero hits.

One can also derive the same-pair edge constraint for free. At x, if the two
endpoint colours are a and b and only one endpoint changes under an ab switch,
the target endpoints have equal colours. Hence an edge of Q cannot have exactly
one endpoint change in that situation. The main proof does not impose a separate
unproved rule about how hidden components are assigned to visible blocks.

## 3. Complete enumeration of T for Layer0

Every Layer0 pin row uses at least three colours. Its S4 orbit is free, so a
covariant colour function is determined by one of four values on each canonical
row. There are 18 canonical rows, ordered as follows:

```
ABABCBC ABABCCB ABACBBC ABACBCB ABACBCD ABACBDC
ABACDBD ABACDDB ABCABBC ABCABCB ABCABCD ABCABDC
ABCACBC ABCACCB ABCADBD ABCADDB ABCDBCD ABCDBDC
```

These represent all 432 Layer0 states. For each individual stored switch,
transport its source and target to these canonical rows using the same literal
colour frame. The pointwise switch condition gives a binary relation on the two
canonical values. Intersect all relations with the same variable pair; self
relations are retained. There are exactly 53 nonempty stored constraint tables.
They are necessary and sufficient for the weak pointwise law on **every** stored
individual switch in Layer0, since each literal transition is included.

`check.py` performs exhaustive finite-domain search over these 18 four-valued
variables, with arc consistency and complete branching. It records every value
elimination and every branch. `verify.py` independently reconstructs the tables
from literal transitions, verifies that each eliminated value has no support in
the indicated current neighboring domain, and verifies that each branch covers
every remaining value. It does not import the generator or execute its search.
The resulting proof tree has 47 nodes. Every live leaf is checked against every
binary relation. Thus no member of T can be omitted by the pruning.

Exactly 25 functions survive. The complete vectors, in the preceding row order,
are stored in the certificate; their zero-based indices are:

| Type | Canonical colour values |
| --- | --- |
| 0 | AAAAAAAAAAAAAAAAAA |
| 1 | AAAAAAAACCCCCCCCCC |
| 2 | BBBBBBBBBBBBBBBBBB |
| 3 | BBBBBBCCBBBBCCCCBB |
| 4 | BBBBDDBBBBDDBBBBAA |
| 5 | BBBBDDCCBBDDCCCCAA |
| 6 | BBBCCDBBBCCDBBBBCD |
| 7 | BBBCCDCCBCCDCCCCCD |
| 8 | BBCBDCBBCBDCBBBBDC |
| 9 | BBCBDCCCCBDCCCCCDC |
| 10 | BBCCCCCCAAAAAAAADD |
| 11 | BCBBBBBDBBBBBCBDBB |
| 12 | BCBBDDBDBBDDBCBDAA |
| 13 | BCBCCDBDBCCDBCBDCD |
| 14 | BCCBDCBDCBDCBCBDDC |
| 15 | CBBBBBDBBBBBCBDBBB |
| 16 | CBBBDDDBBBDDCBDBAA |
| 17 | CBBCCDDBBCCDCBDBCD |
| 18 | CBCBDCDBCBDCCBDBDC |
| 19 | CCBBBBDDBBBBCCDDBB |
| 20 | CCBBDDDDBBDDCCDDAA |
| 21 | CCBCCDDDBCCDCCDDCD |
| 22 | CCCBDCDDCBDCCCDDDC |
| 23 | DDDDBBCCDDBBDDCCBB |
| 24 | DDDDDDCCDDDDDDCCAA |

The seven original pins have type indices `(0,2,1,10,19,13,18)` respectively.
Checking all pairs of functions at all 432 states gives exactly 41 edges of Q;
the certificate stores the entire edge list.

## 4. An explicit missing path

At state0 the literal pin row is `ABABCBC`. Its AB|CD partition requires the
CD block `{t,q}`, that is pin indices `{4,6}`, to be connected. Their function
indices are `19` and `18`.

The C/D vertices of Q at state0 are precisely types15 through24. The entire
induced edge set is

```
15-24  16-23  17-23  18-23  19-24  20-23  21-23  22-23.
```

Thus there are exactly two components:

- `{15,19,24}`, containing t;
- `{16,17,18,20,21,22,23}`, containing q.

No CD path can join t and q in any common graph lift. This contradicts the
stored block and proves the theorem. Exhaustive inspection of all required
blocks in Layer0 finds 1,056 failed state/pair/block incidences, all retained in
the certificate. A single displayed incidence suffices for the conclusion.

## 5. Optional strict-cube refinement, kept separate

If a lift additionally realizes each stored switch as exactly one maximal
component and realizes the stored product of visible pair switches as the full
global colour transposition on H, then every vertex belongs to a visible
component for each colour pair containing its current colour. Otherwise a hidden
component's vertices would remain fixed under that product while the global
transposition changes them.

For a complementary-pair cube, every vertex therefore changes on precisely one
component bit. At every cube mask m its value is its initial colour or the
corresponding transposed colour according as that bit of m is zero or one. The
component vertex sets are unchanged throughout this cube. This is a valid
necessary condition under the **additional exact-lift assumptions**, not a law
asserted for visible switches of every genuine graph with hidden components.

Filtering the 25 weak functions by this entire-cube law leaves 13. Their maximal
common-edge graph has 18 edges and still has 1,056 failed incidences. Both checkers
reconstruct these numbers. The strict refinement is unnecessary for Section4's
obstruction and does not strengthen the source-level conclusion.

## 6. Controls and scope

A positive control takes K3 with all three vertices pinned and all 24 labelled
colourings. The same weak-type construction has four functions and its maximal
type graph is K4. Every required block is connected, so the necessary-condition
checker accepts this genuine graph control. K4 in this test is the maximal type
graph, not an assertion that K3 was reconstructed uniquely.

Normal and seed17 reconstructions, independent proof-tree replays, three kinds
of corrupted certificate, and exclusive-create rejection are recorded in
[VERIFICATION.md](VERIFICATION.md). All inputs are hash bound. No planarity
library, SAT package, numerical solver, external theorem, or 4CT is used.

The original r6 source still retains exact outer support319, all complete U
colourings and every legal r lift (including vacuous empty r fibres), original
edges/nonedges, degree requirements, collar, and rotation. This audit introduces
no graph satisfying those requirements. The finite 720-state countermodel to
switch-axiom deduction remains valid as an abstract system; it has now been
proved unsuitable as a single-valued common-graph realization.

| Layer of claim | Status |
| --- | --- |
| General colour-function/common-edge necessary condition | Proved elementary lemma |
| Exact single-valued lift of this 720-state table | Excluded, arbitrary finite graph order |
| Hidden-state cover/refinement of the table | OPEN |
| Graph realization or exclusion of the full22-row relation | OPEN |
| Original degree/collar r6 source with complete319 support | Not triggered; exclusion OPEN |
| Better source order bound | None |
| New Lean theorem | None |
| General main claim / omega=0 | OPEN |

No commit or push is part of this audit.
