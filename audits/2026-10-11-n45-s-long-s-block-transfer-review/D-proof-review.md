# Independent D proof and bounded calibration review

The seven claims of `N45-S-LONG-S-BLOCK-TRANSFER` are supported in their stated identity/calibration/inherited-domain scopes. No mathematical blocker was found. Recommend accepting the arbitrary-size paper identities and the fixed finite interface calibration after root's independent custody and native replay checks. D proves no new schedule exclusion and leaves its inherited restoration lemma open.

This review used the original D report, claims, proof, interface schema, fixed cases, checker/direct code and certificate; the dispatched `TASK_D_TRANSFER.md`; and the frozen accepted inputs inside D. No result from the same-wave q0/q2 workers was used. Original target, shared files, and historical inputs were kept read-only; no Git action was performed.

Bound target delivery SHA256: `ee7bd0093a4e244ee0d8c1af65f0ddedd95125861b5816c8dcbb7975aa43e0ed`. Certificate SHA256: `0c94b0b708e4e50fbcc11960d96591c39620dbe0a0b78e97fed23f4e14882fb8`. Common BASE: `f2692089ad4259808e27d9b7e882ac09505b180a`.

## Paper judgment by claim

| Claim | Independent judgment and exact boundary |
| --- | --- |
| TF-BLOCK | Accept the arbitrary-size identity. The actual vertex/block incidence tree retains every original vertex. Each bridge checks its original edge; each odd cycle checks all edges including its closing edge, without replacing a long cycle by a triangle. Each block assignment agrees with child subtree assignments at the actual articulation vertex. Parent attachment constraints are explicitly deferred to the parent vertex recurrence and applied there exactly once. Disjoint subtree domains intersect only at their named parent coordinates. Restriction uniquely recovers every local assignment, and compatible union is its inverse. The argument requires the actual edge partition/incidence tree and literal attachments; it does not require degree4, disk topology, K11/K12, or bounded size. |
| TF-FIBRES | Accept the exact interface identity. The root colour and every ordered contact coordinate are deterministic readings of the same complete original-vertex assignment. Restricting the assignment bijection to a specified tuple/r fibre therefore preserves every preimage and its emptiness. Repeated shared roles read one actual vertex coordinate, so incompatible repeated tuple values are empty. Complete vectors also preserve longer ordered r-contact lists and branch coordinates even when the stored ambient index uses only the two s contacts. All 64 ambient tuple/r cells and 16 ordered r/s pins, including diagonal and empty cells, are required. |
| TF-X | Accept conditionally on the explicitly supplied same actual X: complete C/U components, no cross component edge, all literal attachments, original s-contact edges and retained s-spokes, no rs or retained r-spoke, and all isolated original vertices. Restriction/union gives the full Cartesian factorization with actual U preimages and the whole `Col^I` factor. The fixed microcases supply C alone and cannot execute this whole-source claim. |
| TF-RESTORE | Accept the exact same-vertex identity for G=X+rb4. Every complete lift already satisfies all retained edges; the only added condition is the original r colour differing from this row's literal b4 colour. The restored set equals the X set at allowed pins and is empty otherwise. q0/q1/q4 use b4 colour2, q2/q3 colour1; the T4 literals also use their actual final digit. C fragment filters are not labelled as computed G lifts. |
| TF-COLOR | Accept with its stated per-attachment and root/shared-coordinate conditions. A palette permutation maps every original piece coordinate and every tuple/preimage; internal inequalities are invariant and each actual attachment's target colour is checked. Pinned coordinates transform as well. Component joins require coherent target pins and one common target literal frame; an independent piece normalization alone is insufficient. |
| TF-FINITE | Accept the fixed calibration, supported by the new independent original-edge reconstruction described below. This covers four valid named C fragments, ten rows each, all full assignments/ambient cells/pins/spoke filters, and all three exact retained corruptions. BRIDGE_BAD6 remains a degree4-premise counterexample, not a K1–K12 source. |
| TF-DOMAIN | Accept as an inherited necessary-domain ledger. Every original sealed remaining-schedule field is unchanged; all 24 schedules and 38 s-spoke variants retain all ten literals and 16 pins, giving 6,080 symbolic positions. Four historical exclusions retain their old review authority/dependencies. No source relation or preimage count is supplied, no new restored row/minor is claimed, and the named residual stays `same-source-Delta-restorable-r-fibre-nonemptiness`. |

The identity proof is valid for arbitrary finite decompositions; it does not promise practical complete enumeration at arbitrary size. The executable validation has the dispatched fixed size bounds. The recurrence itself supplies no cross-row nonemptiness theorem and does not restore an originally rejected row merely because X accepts it.

## Independent reconstruction from original edges

The new [independent-D-check.py](independent-D-check.py) imports only standard-library modules. It imports no D transfer/checker/direct implementation. It validates original vertices, edges, attachments, ordered contacts, ownership, L/S separation, rotation neighbour data, retained degrees, and the supplied block edge partition with a connected acyclic incidence graph. The latter verifies actual bridge/cycle blocks independently of the worker's Tarjan implementation. Rotation checks retain original neighbours, including rb4, but do not validate a disk embedding.

Colour assignments are then constructed using dynamic minimum-remaining-colour DFS on the original edge constraints. This algorithm neither uses blocks for colouring nor uses the worker direct enumerator's Cartesian-product method. It retains every assignment in the original vertex order, groups all tuple/r inverse images, builds all 16 original pins and three literal spoke factors, and applies the original rb4 filter. The resulting complete object and its canonical bytes match the certificate.

The executable was tested read-only with exit0 and no stderr. Root captures a fresh native run in this review directory. The check reports exactly:

| Item | Independently reconstructed result |
| --- | ---: |
| Valid named cases | 4 |
| Literal rows | 40 |
| Complete original C assignments | 1,344 |
| Ambient tuple/r cells | 2,560 |
| Empty ambient cells | 1,966 |
| Ordered r/s pin cells | 640 |
| Literal-spoke-filtered pin cells | 1,920 |

Counts by case, in the fixed ten-literal order:

| Case | Per-row assignment counts | Total |
| --- | --- | ---: |
| TT5 | 21,21,21,21,18,21,15,18,18,15 | 189 |
| T5_7 | 40,40,40,49,44,49,32,37,37,32 | 400 |
| BRIDGE_FIX6 | 21,21,21,18,38,18,41,21,21,41 | 261 |
| NONROOT_CYCLE7 | 62,62,62,44,36,44,42,50,50,42 | 494 |

All five named declarations remain present. BRIDGE_BAD6 independently fails only at original l0: degree within C=3, two B attachments, zero s-contact incidence, hence full degree5. Its failed record is retained exactly in the degree audit and certificate. BRIDGE_FIX6 is a new declaration with the same original bridge branch and one fewer l0 attachment. The four valid cases have complete retained degree4 at every C vertex. The declared limits remain eight cases and eleven C vertices; this delivery declares five cases with at most seven vertices. The separate bootstrap declaration contains no colouring enumeration, and the certificate binds the fixed cases SHA; custody/native event review is root's separate responsibility.

Shared r/s contact roles are exercised by original vertices such as l1/s1. The non-root bridge branch retains l2 and its edge l0-l2. The non-root cycle case retains all vertices and all three original triangle edges at l0. None is compressed to a tuple representative.

## Three exact retained negative controls

The independent verifier reconstructed each corruption from its own expected certificate and compared the entire resulting object with the retained negative file:

- `negative-r-colour.json`: only the first full preimage's original r coordinate in TT5 /01012 /tuple(0,1),r2 changes from2 to3.
- `negative-empty-cell.json`: precisely TT5 /01012 /tuple(0,0),r0, with an empty preimage list, is deleted from the ambient inventory.
- `negative-missing-branch.json`: precisely original l2 is removed from BRIDGE_FIX6's vertex order and from every complete assignment/preimage vector, including ambient, pin, spoke-filtered and restored vectors. The independent original graph still requires l2 and original l0-l2.

All three objects differ from the independent original-edge reconstruction in the intended way. Worker checker/direct rejection logs additionally name the required cell or original vertex; root performs fresh native replays of both read-only validators. Neither the negative controls nor the failed declaration is a satisfying target source.

## Source and inherited-domain boundaries

The old frozen ledger remains 28 raw schedules minus four old q0-to-q1 restoration exclusions, leaving24. D retains14 t_s1 schedules with two original spoke variants each, and10 t_s2 schedules with one variant each. Each symbolic pin correctly computes its retained-spoke factor and original rb4 condition from the literal row. Concrete C/U/X/G source data remains unprovided; target execution is false and trigger count null (`not triggered`). No same-wave exclusions were substituted into this ledger.

Whole-X/G factors and nonempty isolated-vertex factors have paper identities but were not executed in the finite controls. Actual U, disk topology, original G Sigma-critical deletion witnesses, and X's same-beta minimal witnesses were not established. Consequently this calibration establishes no source existence, new schedule exclusion, new Lean theorem, or general N45/N2/E closure.

The open source lemma is exactly the same-source simultaneous nonemptiness requirement: some gamma in the complete Delta, s colour b allowed by original spokes and actual U, and original r colour a different from gamma(b4), must have a complete C preimage avoiding b at both actual s contacts. In a purported source all such restorable C fibres would have to be empty. The recurrence names those fibres precisely and does not prove one is nonempty.

The external Gallai theorem is inherited background for the accepted source block structure; the present restriction/union identity does not invoke it. The two missing BASE observations findings prevent dependent old finite replays and were not replaced by physical/quarantine data. This review adds no fresh primary-source validation of inherited terminal/source lemmas.

## Read-only replay interface

Source inspection confirms the following worker commands are read-only, including the checker setting `sys.dont_write_bytecode=True` before local imports:

```text
python3 -B <D>/checker.py --check
PYTHONHASHSEED=17 python3 -B <D>/checker.py --check
python3 -B <D>/checker.py --check --certificate <D>/<negative-file>
python3 -B <D>/direct_enumerator.py --check --certificate <D>/certificate.json
PYTHONHASHSEED=17 python3 -B <D>/direct_enumerator.py --check --certificate <D>/certificate.json
python3 -B <D>/direct_enumerator.py --check --certificate <D>/<negative-file>
```

Do not use `--write` or execute generation/bootstrap/build/finalization/logging wrappers against the immutable target. Run the independent verifier with:

```text
python3 -B audits/2026-10-11-n45-s-long-s-block-transfer-review/independent-D-check.py
```

It performs no writes or Git actions and emits only stdout JSON. Target entry types/hashes are checked before and after its run. Fresh native command/stdout/stderr/exit records belong exclusively in this review directory.
