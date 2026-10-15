# Same-state Kempe cubes: an explicit 720-state survivor

BASE `6ddea32a81349821ad3724ae1652bddb9c6a7b04`. The exact frozen authority
and provenance of first-round uncommitted inputs are in [INPUTS](INPUTS.json).
This proof establishes a limit of the explicitly defined finite switch
axioms below. It supplies neither a graph nor a genuine source.

## 1. Contract and precise result

Retain the original globally minimum noncatalogue C5 source G, the fixed
original degree-four boundary vertices x,y,b, and original degree-six r.
The prescribed quotient/deletion gives the same U with induced outer C5
`(z,s,v,w,t)` and interior facial triangle `zpq`; its ordered pins are
`(z,s,v,w,t,p,q)`. All original remaining edges, nonedges, rotation and
original degree requirements remain part of the source contract. U has
exact complete outer support 319. For each complete U colouring, **every**
legal colour of r must obey the inherited JOINT6 table. If no r colour is
legal, the universal condition is true and the U colouring is retained.

Let A be the resulting 26 canonical pin rows. The old noncrossing
single-pair fixed point leaves 22 rows, denoted L. We construct a finite
set X of 720 abstract states with:

1. one literal seven-pin row at each state, with canonical support exactly L;
2. one simultaneous assignment of all six two-colour terminal partitions
   at that same state;
3. deterministic successors for every visible component switch;
4. invariant partitions throughout each complementary-pair cube;
5. exact reversibility and commutation of all component switches belonging
   to one complementary pairing;
6. a global S4 action transporting states, all partitions, and all switches;
7. the product of all component switches in any one colour pair equal to
   the corresponding global colour transposition.

Every successor remains in X, so arbitrary successive switches, including
sequences changing pairings, are defined on the same state space. All 22
rows remain present. Thus these axioms alone, even imposed together,
cannot remove any of the 22 rows. This does **not** assert that components
for different pairings arise from the edges of one graph.

## 2. The actual-graph laws and the abstraction boundary

Fix a finite graph H and a complete proper four-colouring f. For one
complementary pairing `ab|cd`, the maximal ab and cd components partition
V(H). Swapping colours on any subset preserves the vertex sets of *all*
these components: the vertex set of each induced two-colour graph is
unchanged, and its edges are original fixed edges. The switches are
commuting involutions. If there are b components meeting the pins and h
components meeting no pin, their action is a Boolean cube on b+h bits.
The visible b bits yield distinct literal pin rows; the hidden h bits do
not alter that row. Swapping all ab components is global a/b renaming.
These assertions use the same full colouring and fixed original graph.

The six actual component partitions coexist at f. At a successor colouring
the four partitions for overlapping colour pairs may change, whereas the
two partitions of the switched complementary pairing stay fixed. Global
colour renaming transports every component and every switch. Mandatory
pin edges force endpoints in the same applicable component; the honest
outer C5 imposes noncrossing on complementary components.

Our finite abstraction remembers a state, its literal pin row, all six
terminal partitions, the switch transitions and the global colour action.
It does not remember hidden vertex identities, common original-edge
incidences, paths, or the rotation outside the outer noncrossing test.
An actual graph yields such data with possible hidden switches. In the
particular witness below all components are visible, so no hidden switches
are needed and the global-product law holds using visible switches alone.
We do not assert that arbitrary genuine sources have no hidden components.

The construction is a countermodel to deduction from this list of switch
laws and terminal tests. It is not a sound replacement of the full source
by a seven-vertex graph. In particular the original degree, collar and
nonedge hypotheses remain unrepresented; they cannot be inferred from
partitions or from successful replay.

## 3. Construction with one global colour frame

Each state is a pair `(ell,r)`, where ell is a layer and r is a **literal**
seven-pin row. Within one layer a row identifies exactly one state. Different
layers may have the same row; these are different abstract states. Global
sigma in S4 acts by `(ell,r) -> (ell,sigma r)`.

The five layers have the following canonical supports:

- Layer0 has the 18 positive rows from the old exact count witness, whose
  complete list is retained in the new certificate. Its partition choices
  are solved anew; we do not reuse the old arbitrary count decomposition.
- Layer1: `ABABCBC, ABACBCB, ABACDCD`.
- Layer2: `ABABCCB, ABACBBC, ABACDDC`.
- Layer3: `ABCABBC, ABCACBC, ABCADBC`.
- Layer4: `ABCABCB, ABCACCB, ABCADCB`.

A proper C5 uses at least three colours, so each row has24 distinct global
renamings. Hence the layer sizes are 432,72,72,72,72, totalling 720.
Their union of canonical supports is exactly L. Eight canonical rows have
count2 and the other fourteen count1. These are abstract counts.

For a canonical row r and complementary pairing P, choose an admissible
partition pair pi. Its cube consists of independently swapping each block.
For every cube row r', canonicalize with a **single common** colour
permutation on all seven pins; transport P and pi by that same permutation.
This yields a finite set of forced `(canonical row, pairing, partition)`
choices. Reject a choice if it forces conflicting partitions for one
`(row,pairing)` variable. Cover all such variables exactly once by these
forced classes. The tiny exact-cover search uses fixed deterministic tie
breaks and integer/set operations only. It requires no numerical solver.

The certificate saves all 30 canonical row occurrences and their three
chosen partition pairs. Expanding each by S4 gives all 720 states. To switch
a block, swap its colours in r and keep ell. The exact-cover constraints
ensure that the target state exists and that its same-pair partition is
unchanged. Consequently every cube is a consistent family of successors,
not a collection of independently selected endpoint witnesses.

The global colour action was defined on complete states, not only on row
counts. The checker additionally tests all 24 permutations at every state,
including transport of the individual component-switch map. The product
of all blocks of one pair changes precisely those colours in r, and keeps
ell, so it is exactly the prescribed global transposition on X. Thus the
usual S4 group relations also hold on states.

## 4. Complete verification and a useful non-realizability control

The saved certificate contains every state, all its terminal partitions,
and every cube target indexed by bitmask. For each state and pairing the
checker verifies the equation

`C_m(C_n(x)) = C_(m xor n)(x)`

on the stored state ids, including `C_0(x)=x`. This checks reversibility,
commutation, and consistency for all cube subsets. It does not demand
commutation of arbitrary overlapping colour-pair switches.

The complete literal checks comprise:

| Check | Number |
| --- | ---: |
| States | 720 |
| Same-pairing cube targets, all masks | 18,816 |
| Cube composition equations | 202,752 |
| S4 partition transports | 51,840 |
| S4 individual-switch transports | 153,216 |
| Whole-pair products equal global swaps | 4,320 |

A second verifier reads the stored tables directly, without calling the
exact-cover search, and verifies every stored target and cube equation.
The main reconstruction also independently compares the all-r predicate
on all `4^7` assignments with the frozen original implementation. It checks
that the saved support is exactly the old22-row fixed point and its outer
mask is319. Empty all-r fibres were never discarded.

As a safeguard against calling this a graph, the intersection of all
inequality constraints holding across the 22 supported rows has precisely
the eight skeleton edges: the outer C5 and triangle zpq. Any simple graph
whose vertex set consists of these seven pins and which admits all the
supported rows must be a subgraph of that skeleton. But `ABABCBD` properly
colours the full skeleton and lies outside the witness support. It also
violates the all-r screen. Therefore **no graph on just these seven vertices
has the witness's exact support**. This does not rule out a realization
with additional vertices, and it is not a source exclusion.

## 5. What has and has not become compatible

This audit makes the same-state bookkeeping stronger than isolated
partition options or common counts: three partition pairs coexist on
every state, the target states are shared, all transitions compose, and
S4 relabelling commutes with switching. The old count certificate only
promised common row multiplicities and orbit decompositions. Its particular
choice of decompositions was not promised to be S4-covariant; finding that
it fails this new condition is not an error in that earlier certificate.

The still-missing compatibility is geometric: one common vertex set and
one common edge set must induce all six partitions at every colouring,
and their changes under overlapping-pair switches must arise from those
same edges. This can impose identities not expressed in the finite axioms
above. The model supplies no collar, original nonedge realization, degree
witness, or plane embedding. It cannot be used as a truth witness for the
r6 source, nor as a counterexample to its exclusion.

Paper scope: elementary actual-graph switch laws and the meaning of this
finite abstraction. Finite scope: the full720-state witness and every
listed verification. Genuine target sources: zero, `not triggered`.
Source exclusion, improved order bound, new Lean theorem and the general
claim remain OPEN. No commit or push is part of this audit.
