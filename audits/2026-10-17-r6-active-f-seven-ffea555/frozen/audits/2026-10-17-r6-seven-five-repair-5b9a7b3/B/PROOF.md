# B: the complete chorded-seven cap relation and the one-path interface

Frozen BASE `5b9a7b3190c84bc10ff99608e372a9b4be57a0f6`.
This note proves arbitrary-size necessary consequences of the adopted
seven-cycle classification, and separately seals a complete finite local
relation. It proves neither a marked repair nor a source exclusion.

## 1. Same source, exact local coordinates

Keep the original minimum completed no4ct C5 source, the same support,
ordered contacts, attachments, rotation, complete U319 fibres including
empties, and all original r lifts. The actual graphs remain
`J=U/(s=t)`, `m=[s=t]`, `D=J*`, with literal
`e=(vw)*`, `f=(pq)*`, `g=(mz)*`. No local relation below selects a new
source, changes a colouring frame, or replaces a complete colouring lift.

Take an ordinary matching `M` in `P110 ∪ P101` whose complement has a
nonfacial seven-component C. The frozen classification A1--A3 gives one
chord and five matching spokes. Label the seven vertices in cycle order
`0,1,2,3,4,5,6`, with the unique chord `03`. The quadrilateral is
`0-1-2-3-0`; the pentagon is `0-3-4-5-6-0`. The five ordered ports are
`P=(1,2,4,5,6)`. These labels describe the actual fixed embedding, up to
choosing the first chord endpoint. They impose no identification between
different source instances.

Put `X=V(C)`, `H=D[X]`, and let `b_i` be the actual spoke at port i.
Then

`E(H)=E(C) ∪ {03}`, `B_C=δ_D(X)={b_1,b_2,b_4,b_5,b_6}`,

and `M ∩ E(H)={03}`, `B_C ⊆ M`. The five exterior endpoints are distinct.
In particular every component of `D-X` in the old complement is a whole
old complementary cycle, and none is discarded by the local notation.

The source supplies a complete even-complement 111 matching M0 on this
same D. Its existence and its distinction from an ordinary joint matching
are taken only from the frozen complete-111 bridge. Denote

`S={i∈P:b_i∈M0}`, `N=M0∩E(H)`.

Every vertex in S is externally matched, and N matches each vertex of
`V(H)\S` exactly once. This describes an exact local matching fibre for
each of all 32 spoke subsets, independently of whether a local state has
any extension to the full source.

## 2. The five-spoke exclusion

**Lemma B1.** `|M0∩B_C|∈{1,3}`.

**Proof.** The sum of matching degrees over the seven vertices of X is

`7=2|M0∩E(H)|+|M0∩B_C|`.

The boundary count is odd, hence is 1, 3 or 5. If it is 5, all port
vertices are matched outward, so the two remaining vertices 0,3 must use
the chord. Thus the restriction of M0 agrees with M at every incidence
of C. All seven edges of C remain in `D-M0`, and every C vertex has
complementary degree exactly two there. Consequently C is a whole odd
component of `D-M0`, contradicting its even complement. QED.

This argument uses the supplied full even endpoint; it does not assume
that an arbitrary local matching has an even extension.

## 3. Complete local matching relation, including empty fibres

Write `ij` for the undirected edge with endpoints i,j. All nonempty
fibres `(S,N)` are exactly the following. Where a row lists two choices,
they are separate whole matchings, never pieces that may be joined.

| S | all N in the fibre |
| --- | --- |
| `{1}` | `{06,23,45}` |
| `{2}` | `{01,34,56}` |
| `{4}` | `{01,23,56}`; `{03,12,56}` |
| `{5}` | `{06,12,34}` |
| `{6}` | `{01,23,45}`; `{03,12,45}` |
| `{1,2,4}` | `{03,56}` |
| `{1,2,5}` | `{06,34}` |
| `{1,2,6}` | `{03,45}` |
| `{1,4,5}` | `{06,23}` |
| `{2,5,6}` | `{01,34}` |
| `{4,5,6}` | `{01,23}`; `{03,12}` |
| `{1,2,4,5,6}` | `{03}` |

Every even-cardinality S has an empty fibre: this includes the empty
subset, all ten pairs and all five four-subsets. The remaining empty
odd-cardinality fibres are

`S∈{{1,4,6},{1,5,6},{2,4,5},{2,4,6}}`.

Thus the complete relation has 32 rows, exactly 12 nonempty rows, and
15 internal matchings. It contains seven size-three matchings before
applying the necessary evenness condition below.

**Paper derivation.** When the chord is absent from N, N is a matching
of the remaining cycle runs after deleting S. Each such path has a perfect
matching exactly when its order is even; that matching is unique, by
successively forcing the edge at a path endpoint. When `03∈N`, delete
`S∪{0,3}` and apply the same rule to the resulting runs of the two open
arcs `(1,2)` and `(4,5,6)`. These two disjoint cases give exactly the
displayed relation. Odd remaining order excludes each even-cardinality S.
No bound on the number of exterior vertices is used.

## 4. The three-spoke case has six even-compatible local states

**Lemma B2.** Under `|S|=3`, the complete cap complements and local
difference paths are exactly those in the next table. A path denotes its
entire ordered edge sequence. The local difference path is the part
inside H; appending the two changed spokes gives the boundary-to-boundary
part of `M△M0`.

| S | N | `H-N`, with every component retained | local difference path |
| --- | --- | --- | --- |
| `124` | `03,56` | path `5-4-3-2-1-0-6` | `5-6` |
| `125` | `06,34` | cycle `0-1-2-3-0`; path `4-5-6` | `4-3-0-6` |
| `126` | `03,45` | path `4-3-2-1-0-6-5` | `4-5` |
| `145` | `06,23` | path `2-1-0-3-4-5-6` | `2-3-0-6` |
| `256` | `01,34` | path `1-2-3-0-6-5-4` | `1-0-3-4` |
| `456` | `01,23` | cycle `0-3-4-5-6-0`; path `1-2` | `1-0-3-2` |
| `456` | `03,12` | path `1-0-6-5-4-3-2` | `1-2` |

The sixth row is impossible for the full even M0: its internal pentagon
is closed in the full complement, because all five of its vertices have
complementary degree two already within H. It remains in the complete
local relation and is explicitly labelled incompatible with an even
endpoint. The remaining six rows satisfy the local necessary conditions
for an even endpoint. This label asserts no full-graph extension.

In five surviving rows the unique cap complementary path has length six;
in the exceptional row S=125 it has length two and there is also a whole
even quadrilateral. Thus the original odd component is removed inside X
without creating a closed odd cap component when the actual global
difference component through X is flipped. Whether the *full complement*
has fewer odd components remains a separate exterior obligation.

**Proof.** Subtract N from the eight explicit edges of H in each of the
seven size-three entries of the complete relation. The table lists every
remaining edge exactly once. The difference uses the old chord exactly
when N omits it, the new cycle matching edges in N, and exactly the two
spokes not selected by M0. These are the displayed paths with their
spokes appended. QED.

Every surviving cap complementary path has even length. On the actual
even endpoint M0, the two complementary spokes and the actual exterior
complementary path complete it to a whole even cycle. Therefore that
exterior complementary path has even length too. This statement concerns
the M0 complement. The exterior path in `M△M0` is a different object.

## 5. The exact actual difference interface for arbitrary-size exteriors

**Lemma B3.** If `|S|=3`, exactly one component Q of `M△M0` meets X.
It consists of the cap difference path from Lemma B2, the two changed
spokes, and one actual exterior alternating path. Every other component
of `M△M0` is an alternating cycle contained in `D-X`.

**Proof.** A symmetric difference of two actual perfect matchings is a
union of vertex-disjoint alternating cycles. Exactly the two spokes in
`B_C\M0` belong to the difference. Their ends on X are joined by the
unique local difference path in the table. There is no additional local
alternating cycle: M has only one internal matching edge, whereas any
alternating cycle in a simple graph needs at least two M edges. The
unique global difference cycle containing the two spokes consequently
has one exterior path joining their exterior endpoints, with no further
crossing of the five-cut. No other difference component meets X. QED.

The exterior alternating path begins and ends with `M0\M` edges, so it
has odd length. Its interior may encounter arbitrarily many old
complementary cycles. The remote difference cycles remain part of the
complete same-graph representation. They may meet the *same old
complementary components* as that exterior path despite being vertex
disjoint from it. Neither this lemma nor the evenness of the full M0
endpoint licenses dropping them in a full oddness calculation.

For comparison, if `|S|=1`, there are exactly two cap difference paths,
with four changed spokes. The two actual exterior difference paths may
join them into one global alternating cycle or two. A single assumed
global cycle is therefore specific to `|S|=3`.

## 6. Literal mark placement can force the obstruction onto Q

Let h be the active omitted mark: `h=g` for 110 and `h=f` for 101.
The other mark j among f,g belongs to both M and M0, and so does e.
Consequently the full reference difference avoids e,j and contains h.
For batches chosen from its components, the adopted union-preservation
condition is exactly to omit the unique component containing h.

**Corollary B4.** In direction 101, if C contains f, then the unique
difference component Q of Lemma B3 contains f. In the chosen coordinates
there is precisely one surviving three-spoke state for each possible f
placement:

| actual f edge | S | N |
| --- | --- | --- |
| `01` | `256` | `{01,34}` |
| `12` | `456` | `{03,12}` |
| `23` | `145` | `{06,23}` |

**Proof.** Frozen A3 places the degree-four centre at the actual terminal
p or q, and its adjacent degree-five centre outside the six exceptional
vertices. Thus f is on the quadrilateral boundary rather than the chord
or pentagon-only arc; in these coordinates it is one of `01,12,23`.
It belongs to M0 and not M. Inspecting the complete seven three-spoke
entries, and deleting the closed-pentagon state, gives exactly the three
displayed possibilities. Each displayed f lies on the unique local
difference path, hence on Q. QED.

Thus in this legitimate source subclass, no union-preserving batch
selected from the components of this fixed reference difference can
change C: Q is forbidden, and all other components avoid X. This is an
obstruction to this reference-difference repair, not an obstruction to
all actual alternating batches in D. In particular one must still study
batches outside this fixed decomposition, potentially flipping f and g
together, or produce the requested explicit forbidden cyclic cut.

In direction 110, frozen A3 says a nonfacial C cannot contain g. Since
g is also absent from M, it cannot be a matching chord or spoke either.
Hence both ends of g lie outside X. If Q is blocked by g, that obstruction
is on its actual exterior alternating path, with no local bound on its
distance or the size of the exterior.

If e is the chord, it belongs to both M and M0. Only the three
chord-retaining size-three states survive (`124`, `126`, `456` with
N containing `03`), and the cap difference path is a single cycle edge.
The same observation applies if the common mark f in direction 110 is
the chord. This restriction follows from actual edge identity, without
normalizing marks independently of the local state.

Nothing above constructs a vertex set Y with `e,f∈δ_D(Y)` or proves
that both sides of such a cut contain cycles. The five-cut `B_C` is
cyclic, but in the f-containing case f lies on C and is not in `B_C`.
It therefore does not trigger R6-MARKED-SIX by itself.

## 7. Finite certificate and exact remaining boundary

`check.py` reconstructs every one of the 32 local spoke rows by two
independent methods: recursive forced matching of uncovered vertices,
and all 256 subsets of the eight internal edges checked by degree sums.
It retains all 15 internal matchings, every full labelled cap complement,
every full labelled difference fragment, and the three actual-f
specializations. Empty rows and the locally odd three-spoke endpoint are
retained explicitly. Exterior stubs retain their actual port label; no
exterior graph, full source colouring, or realizability witness is
generated.

The checker verifies all 11 frozen input files against both their sealed
SHA256 values and their Git objects at BASE. Its active certificate is
`certificate.json`, generated with exclusive-create semantics. Normal
and `PYTHONHASHSEED=17` read-only replay, a missing-empty-row corruption,
a changed full-fragment corruption, and duplicate exclusive-create
rejection are recorded in `VERIFICATION.json`.

The paper results B1--B4 hold for the actual arbitrary-size source under
their stated premises. The certificate validates the complete local
relation only; a full original source input is **not triggered**. The
missing source implication remains either a mark-preserving actual
batch with strict decrease of the complete complementary odd-component
count, or an explicit cyclic cut of size at most six containing e,f.
The ordinary-family existence, the supplied even 111 witness, and the
finite local relation do not supply this implication. Joint positivity,
complete319 exclusion and any new Lean theorem remain **OPEN**. All
operations stay on the same graph and have zero reconstruction cost;
the previously recorded completed-source reconstruction cost k+5 remains
unchanged. No commit or push is performed.
