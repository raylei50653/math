# Independent literal verification

This review covers Task B in this isolated audit. The verifier is
`controls/independent.py`; it imports neither the producer nor the topology
module nor the frozen catalogue checker. The final independent certificate
comparison below uses `controls/certificate.v2.json`.

## Implemented checks

- `enumerate_lifts(graph, beta)` enumerates every proper four-colouring by
  recursive minimum-remaining-values backtracking. It starts with the actual
  five named boundary assignments, recomputes domains from already assigned
  neighbours, and returns all full colour vectors sorted lexicographically.
  Vector positions are exactly `graph.nodes`, which must be sorted original
  integer labels; labels are never compacted after deletion or quotient.
- `PATTERNS` separately records the frozen ten row patterns. No colour is
  renamed or canonically chosen during full-lift enumeration.
- `verify_graph(graph)` reconstructs all oriented face walks from the supplied
  clockwise rotation and literal edges using the predecessor dart rule. It
  checks the full face multiset, occurrence of forward named boundary
  `(0,1,2,3,4)`, and Euler characteristic separately for every component.
- Disconnected components and isolated interior vertices are accepted with
  explicit semantics: an isolate contributes face `[v]`; component outside
  faces merge to one global outside face. Euler is also checked in this global
  accounting. Such components can be placed inside the boundary disk without
  changing their rotations.
- NetworkX independently tests the literal graph and the graph augmented by
  an apex adjacent to the five distinct boundary labels. The rotation and
  forward boundary checks establish the supplied embedding; apex planarity
  is an additional independent cofacial test.
- `verify_operation(source, mark, operation)` independently checks literal
  vertex/edge transformations, original spoke identity, incident triangular
  faces and absent flip diagonal, preservation of surviving cyclic neighbor
  order, quotient block noncrossing/nonadjacency and boundary injectivity,
  every original vertex's quotient name, and complete quotient edge preimages.
  It does not call the topology producer or the ribbon-contraction routine.
- `verify_domain(domain)` independently generates all 52 set partitions from
  all `5^5` strings and compares every candidate's original-label blocks,
  cyclic crossings, boundary collisions and original-edge obstructions. It
  also checks every original degree-five mark, all five spoke deletions, the
  five original-face flip candidates per mark, and the exact admitted operation
  lists. This makes the complete admission sweep replayable in the main checker.

## Executed calibration of the independent module

Executed with `/home/ray/developer/ai/math/.venv/bin/python` and NetworkX 3.5:

1. A wheel with centre label `7` preserves nonconsecutive IDs, passes both
   embedding and apex tests, and yields ten full-lift counts
   `[1,1,0,1,1,0,1,0,0,0]`.
2. The disconnected graph comprising named C5, isolate `7`, and edge `8-9`
   passes component and global Euler checks. Every one of its ten full-lift
   lists exactly equals an independent Cartesian-product enumeration.
3. Corrupting the boundary labels, a face walk, or a rotation neighbour is
   rejected.

These calibrations are tests of the verifier. They are not additional source
controls, degree-5 operations, or evidence for universal reducibility.

## Producer and certificate review

The first producer used the first member in cyclic L order as the root of each
block's pair constraints, whereas the frozen paper contract fixes the least
actual vertex label. It also scored Q-PAIR-CENTER once per operation, whereas
the paper specifies a boundary-row/full-H-lift instance. Both issues were
reported and corrected. The first certificate is retained only as superseded
provenance; all conclusions below refer to v2. These are scoring-contract
corrections, with no change to the frozen source or legal operation domain.

The corrected producer's common deleted-spoke rows use the original sorted
node order. Deletions precede flips in the frozen operation order, so the common
graph is registered before each flip lookup. Original-spoke and new-diagonal
inequalities filter the same full lift list. Quotient pullbacks index the
explicit original-to-quotient label map and correctly retain gaps in labels.
No unresolved semantic defect was found in those constructions.

Executed an additional independent sweep without importing the producer or
topology module:

- All 133 originals, 77 centre deletions, 385 spoke deletions, 345 flips,
  290 quotient graphs, and 290 augmented chord graphs passed independent
  rotation, Euler, forward B, literal planarity and apex-planarity checks:
  1,520 geometry records in total.
- All 1,020 operations passed `verify_operation` using direct literal source
  edges and maps. Independently canonicalizing all `5^5` label strings yielded
  exactly the 52 set partitions, matching each of the 77 candidate tables.
  Independent admission formulas agreed on all 4,004 quotient candidates and
  all 385 flip candidates, and their admitted operation lists were complete.
  The replayable domain function also rejected four separate corruptions:
  a missing partition record, changed flip admission, missing spoke operation,
  and missing source mark.
- Every row in every one of the 1,230 v2 graph records matched the independently
  generated full MRV list: 12,300 graph/boundary rows and 994 distinct literal
  graphs. This includes all empties, every color choice on every interior
  vertex, and all transformed graphs.
- Direct comparison of accepted row sets reproduced the full operation table:
  deletions: 385 strictly larger; flips: 320 incomparable, 20 strictly smaller,
  5 strictly larger; quotients: 205 incomparable, 75 strictly smaller,
  10 strictly larger. No operation in this fixed domain has equal Sigma.
- Recomputing the fixed actual-label pair constraints from v2 full H lifts
  independently reproduced Q-PAIR-CENTER's 2,340 triggered lift instances,
  1,710 holds and 630 failures, and Q-SEPARATE-JOIN's 60 triggered row instances,
  all 60 holds and no failures. The latter is fixed-domain calibration only.

Certificate-corruption tests are executed and recorded by the root audit's
replay runner; they are not relabeled as this reviewer's separate execution.
The independent module's own graph-corruption tests are recorded above.

No universal outside-K source claim, Tasks A/C conclusion, or Lean result is
inferred from these finite controls.
