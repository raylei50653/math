# Task C44: all minimal rejected-row cores in the epsilon-two finite domain

2026-10-06. Base `b2ca452`, task branch `task-c44-cores`. **Statistics complete
through k=9; counterexample branch taken.** The broad assertion that epsilon-two
rejection rows have no two-original-root `(4,4)` core is false. The smallest
source example is named **C44-AD3-row0-44**. It is Sigma-critical, but its
complete Sigma is 956, outside the D5 orbits of 933 and 941. Consequently it
does not refute the more restrictive statement with that additional hypothesis.
No source satisfying the target complete-Sigma hypothesis occurs in this finite
input domain, so that restrictive statement has no actual antecedent control here.

The [Kempe guide stopping point](../../docs/c5_kempe_guide.md#3-停止點與保留缺口)
is unchanged. This report and one STATUS index line are the only documentation
integration changes; historical certificates are unchanged. No push or merge.

## 1. Definitions fixed before implementation

| Term | Exact definition used | Definition source |
| --- | --- | --- |
| Boundary and Sigma | Ordered induced cycle B=(0,1,2,3,4), retaining its five edges. Sigma is the accepting subset of the ten proper rows in the established REPS order, modulo one shared S4 colour permutation. A row is rejected exactly when no full proper four-colouring extends that literal row. | [ES section 1](../../docs/c5_excess_two_finite_search.md#1-完整前提與計數範圍), [ER section 1](../../docs/c5_excess_two_independent_search.md#1-問題群作用與獨立性界線) |
| q-core | A subgraph M of the source G retaining B and its five frame edges and rejecting the same fixed literal row q. Sigma(M) can be strictly larger than Sigma(G). | [Support-capacity section 1](../../docs/c5_independent_support_capacity.md#1-兩種-minimality-與來源的基本結構) |
| Minimal core | Inclusion-minimal among those subgraphs, permitting edge and private-vertex deletions and ignoring isolated private vertices. Equivalently, M rejects q and every nonframe edge deletion M-e accepts q. This is not minimum cardinality or vertex-induced minimality. | [q-core shield section 1](../../docs/c5_qcore_shield_budget.md#1-原定義依賴與證據層), [E4C section 2](../c5_excess_two_e4c/REPORT.md#2-實算摘要) |
| Original roots | NA and AD have source roots 5,6 of full degree five, respectively nonadjacent and adjacent. D6 has the single source root 5 of full degree six. Every other source private vertex has full degree four. | [ES section 1](../../docs/c5_excess_two_finite_search.md#1-完整前提與計數範圍) |
| Root degree type in a core | Ordered degrees (deg_M(5),deg_M(6)) for NA/AD, counting all retained spokes and interior edges. Record an omitted root as null/absent. Aggregate (4,5) with (5,4) under root swap, retaining the ordered values in each row record. D6 has one entry. | [E3 nonadjacent section 5](../c5_excess_two_e3/nonadjacent_notes.md#5-每列-q-core-的完整原省略分類), [E4C D5-D7/D13-D14](../c5_excess_two_e4c/REPORT.md#3-全部引理中間步驟的前提與結論) |
| Core size | Save both the number of effective private vertices and total vertex size, which is five larger. | Effective-interior convention in the two definition sources above |
| Mixed component | A component of the core's effective interior after removing the original named roots, with a retained contact to both roots. Roots retain their source identity even when their core degrees fall to four. There is no two-root mixed component for D6. | Original-piece ownership in [E3 nonadjacent section 2](../c5_excess_two_e3/nonadjacent_notes.md#2-原分量刪-root-與例外全部可直接移植) and [E4C D5/D6](../c5_excess_two_e4c/REPORT.md#3-全部引理中間步驟的前提與結論) |

The complete definition review and elementary counterexample proof are in
[PROOF_NOTES](PROOF_NOTES.md). Definitions were read and settled before the
core algorithms were written. Retained original degree-four vertices must keep
every incident original edge: a minimal core has private degree at least four,
and its degrees cannot exceed the source degrees. This saturation fact does not
assume source Sigma-criticality and is consistent with the fixed-root ownership
used in the JSON.

## 2. Inputs and finite coverage

Read the specified [ES](../../docs/c5_excess_two_finite_search.md),
[ER](../../docs/c5_excess_two_independent_search.md),
[E4C](../c5_excess_two_e4c/REPORT.md), and
[E4 N1-22-44](../c5_excess_two_e4/REPORT.md#3-n1-主攻22-mixed-加-44-core-整類排除).
Use all 54 saved ER q-orbit chunks in its 21 layers, k=3,...,9. The smaller
k=1,2 layers are empty by the source root degree and three-spoke requirements;
NA requires at least two source roots. No new graph generation was necessary.

Every source is a finite simple ordered induced-C5 disk, accepts T4 (mask 932),
has nonempty singleton-rejection set Q, prescribed interior degrees and
epsilon=sum(deg_G(v)-4)=2. The saved search domain additionally has connected
interior H and at most three spokes per private vertex. The **q population does
not require Sigma-criticality**; the critical subset requires strict expansion
of complete Sigma after every nonframe edge deletion. Source-specific lemmas
requiring criticality or full Sigma=933/941 are not applied to noncritical inputs.

| Root type | All q-orbits | Rejection rows | Critical orbits | Critical rejection rows |
| --- | ---: | ---: | ---: | ---: |
| NA | 3,706 | 3,720 | 54 | 60 |
| AD | 3,278 | 3,450 | 9 | 16 |
| D6 | 2,660 | 2,813 | 116 | 117 |
| Total | 9,644 | 9,983 | 179 | 193 |

[input_audit.json](input_audit.json), produced by the
[input checker](../../scripts/c5_excess_two_c44_input_audit.py), checks every
chunk hash and manifest count, graph degree/domain, augmented and disk rotation,
86,457 accepted witnesses and 91,160 new-row deletion witnesses. All 9,644
rotations have a C5 boundary face and genus-zero Euler characteristic. C44
also recomputes every source complete Sigma and all 234,477 complete deletion
masks; each equals the saved ER value and gives the same critical flag.

Finite graph-set completeness is inherited from the saved ES/ER comparison,
which used two generators; the ER generator depends on plantri. This task
does not rerun those generators or prove arbitrary-size completeness.
Twenty accessible ES layer files have the hashes recorded in ER; the ignored
large `NA_k9_validate.json` is absent in this checkout. Its ER q chunks are all
present and hash-verified. No old artifact was rebuilt or rewritten.

## 3. Specialized algorithm and exactness

The [main checker](../../scripts/c5_excess_two_c44.py) uses one literal graph
and frame throughout. It enumerates all minimal rejecting edge sets separately
for every rejected row, with memoization by the entire named edge set.

1. **Safe degree peeling.** Remove private vertices of current degree below
   four until stable. Every colouring of the remainder extends greedily in
   reverse removal order. Thus peeling preserves each row's acceptance, and
   cannot remove any minimal core contained in the current graph. This uses
   the elementary [W1 degree argument](../../docs/c5_qcore_shield_budget.md#22-非空連通與-degree-四下界), not a topology oracle.
2. **One-pass criticality.** Fixed-q assignments with zero monochromatic
   nonframe edges colour the parent; assignments with exactly one such edge e
   colour precisely the deletion G-e. Enumerate all assignments with at most
   one violation. Each edge is counted when its second endpoint is assigned.
   Accepted rows persist under deletion; combining the passes for the original
   rejected rows therefore supplies every complete Sigma(G-e) at once, without
   separate edge-by-edge colouring searches. The elementary equivalence is
   the one audited in [ES section 2.3](../../docs/c5_excess_two_finite_search.md#23-一次-criticality-的精確性).
3. **Correct monotone direction.** Edge deletion enlarges the extension set.
   If a child accepts q, every subgraph of it accepts q and its entire downward
   branch is discarded. A rejecting child is retained. No inference from a
   rejecting parent to a rejecting descendant is used.
4. **Exhaustiveness.** If a current rejecting graph contains a proper minimal
   core M, some current nonframe edge outside M can be removed while retaining
   M and rejection. Peeling preserves M. Repeating such choices reaches M;
   memoization only merges identical states. A rejecting terminal has an
   accepting witness for every retained nonframe edge, so it is minimal.
5. **Canonical reduction.** Input ER representatives have already reduced the
   complete graph under D5 times root swap times permutations of ordinary
   degree-four vertices (D6 has no root swap). ES independently compared the
   same graph-orbit sets. This reduction moves all actual attachments together.
   Within a representative, every distinct literal row-core edge set is saved;
   cores are not independently normalized or collapsed by their degree type.

Core complete Sigma is independently recomputed by ER frontier DP; every
minimality witness is checked directly against all retained edges and the
fixed literal row. No marginal relation replaces a complete graph. The full
run examined 34,576 peeled states, made 636,007 one-pass deletion decisions,
and checked 104,507 core edge-deletion witnesses.

The additional [algorithm audit](algorithm_audit.json) checks seeded direct
Cartesian controls for one-pass and peeling and the named core embedding.
No four-colour-theorem oracle, boundary-state conjecture, E4 source exclusion,
or new per-spoke-pair tree is used in the core search.

## 4. Brute-force gate, saved comparison and cost

The independent [brute module](../../scripts/c5_excess_two_c44_brute.py)
visits every one of the 2^m nonframe-edge subsets, with direct numeric-order
four-colour DFS. It shares only the boundary REPS, not the core recursion,
peeling, one-pass colouring, or rejection pruning. Its degree filter retains
private degrees zero or at least four, a separately proved necessary condition
for minimality. It then selects minimal rejecting sets by exact containment.
For k<=5 the entirely unfiltered version is also run and agrees exactly.
The brute author's reading also included ES section 2; no ES implementation
was read or imported. This is implementation independence, not a blind-document claim.

| Gate | q-orbits | Rejection rows | Edge subsets visited | Degree-valid subsets | Minimal core occurrences | Mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| k<=5 | 32 | 36 | 1,550,336 | 351 | 49 | 0 |
| k=6 | 81 | 85 | 25,952,256 | 845 | 112 | 0 |

[brute_comparison.json](brute_comparison.json) saves **both complete minimal
edge-set lists for every row**, equality flags, subset/DFS counts, and the
unfiltered k<=5 counts. The final small gate took 8.803 seconds and completed
before any larger-k result was trusted. The first gate, before adding the
saved unfiltered check, had already passed in 4.121 seconds.

After that gate, 64 k=9 representatives took 0.450 seconds on one job, giving
a linear one-job estimate of about 68 seconds for all inputs. This was a timing
estimate, not a mathematical bound, and was below two hours. The full generation
took 10.070 seconds with eight jobs. [performance.json](performance.json)
saves the estimate. Replay concurrency is at most 16 workers; no k>=10 run,
new graph search, or new pair case tree was started.

## 5. Minimal-core statistics

Numbers below count **core occurrences per canonical source representative
and literal rejection row**. A core recurring in another row or source is
counted again. They are not counts of globally nonisomorphic cores.
`absent,4` means one original root was omitted. D6 degrees are single entries.
The JSON also saves source orbit weights and corresponding labelled occurrence
totals; those are weighted core occurrences, not graph or embedding counts.

| Population | Source type | (4,4) | (4,5) or (5,4) | (5,5) | (absent,4) | D6 degree 4 | D6 degree 5 | D6 degree 6 | Total |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| All q | NA | 56 | 122 | 48 | 3,552 | - | - | - | 3,778 |
| All q | AD | 2,360 | 113 | 3 | 1,564 | - | - | - | 4,040 |
| All q | D6 | - | - | - | - | 3,190 | 46 | 115 | 3,351 |
| Critical | NA | 0 | 12 | 48 | 0 | - | - | - | 60 |
| Critical | AD | 26 | 0 | 3 | 0 | - | - | - | 29 |
| Critical | D6 | - | - | - | - | 2 | 0 | 115 | 117 |

| Population/type | Private size histogram (size: occurrences) | Mixed occurrences | Cores per row histogram (cores: rows) |
| --- | --- | ---: | --- |
| All q / NA | 2:1297, 3:2207, 4:48, 5:52, 6:49, 7:6, 8:46, 9:73 | 226 | 1:3662, 2:58 |
| All q / AD | 2:635, 3:3046, 4:97, 5:112, 6:92, 7:18, 8:9, 9:31 | 2193 | 1:2862, 2:587, 4:1 |
| All q / D6 | 2:498, 3:2482, 4:86, 5:97, 6:57, 7:25, 8:51, 9:55 | 0 | 1:2275, 2:538 |
| Critical / NA | 6:9, 7:2, 8:22, 9:27 | 60 | 1:60 |
| Critical / AD | 2:1, 3:9, 6:16, 7:1, 9:2 | 28 | 1:3, 2:13 |
| Critical / D6 | 3:2, 4:2, 5:8, 6:4, 7:25, 8:41, 9:35 | 0 | 1:117 |

There are 11,169 core occurrences in all q rows, and 206 in critical rows.
Six critical AD source orbits have a `(4,4)` core. The 54 critical NA orbits
reproduce E4C's absence and its unordered degree counts 48 of (5,5), 12 of (4,5).
Noncritical NA sources do have `(4,4)` cores; the population distinction matters.

[summary.json](summary.json) contains complete joint degree/size/mixed tables,
histograms, weighted counts and the manifest of 19 output chunks.
Each chunk in [orbits](orbits/chunk_0001.json) saves every source graph's code,
full edge set, roots, complete Sigma, source reference/hash, critical flag,
orbit weight, and every row's full list of minimal cores with their named
vertices/edges, ordered root degrees, both sizes, mixed components and full
core Sigma. These 19 chunks total 12,624,615 bytes; each is below 1 MB.

## 6. Named counterexample and elementary proof

[counterexample_C44-AD3-row0-44.json](counterexample_C44-AD3-row0-44.json)
uses the exact ER AD3 representative at `/q_orbits/0` of
[the AD3 source chunk](../c5_excess_two_independent_search/AD_k3/q_orbits/chunk_0001.json).
Original interior vertices 5,6,7 have degrees 5,5,4. Its nonframe edges are

```text
06, 16, 17, 25, 27, 35, 45, 46, 56, 57, 67.
```

Its complete Sigma is 956, Q={0,3,4}, and every original nonframe edge is
Sigma-critical. Fixed literal row index 0 is `01012`, singleton position 4.
Delete vertex 7, giving the core with nonframe edges

```text
06, 16, 25, 35, 45, 46, 56.
```

Both roots now have degree four. Each sees boundary colours 0,1,2 at its three
spokes, so both must have colour 3. Edge 56 forbids that. Deleting a spoke
lets its root take the formerly prohibited boundary colour while the other
root has colour 3; deleting 56 allows both roots colour 3. This proves rejection
and inclusion-minimality on paper. The core has two private vertices, seven
total vertices, no mixed component, and complete Sigma 1022.

The certificate saves the original graph, original augmented embedding and
complete deletion masks/witnesses, the literal rejection row, core graph,
inherited core rotation and all faces, all seven full minimality witnesses,
and an independent Cartesian rejection check (16 assignments, zero accepted).
The inherited embedding has V=8,E=17,F=11 after adding apex 8, with Euler
characteristic 2 and the original C5 as disk boundary.

The same source and row also have the size-three minimal core G-45-46,
retaining mixed vertex 7. Its interior triangle has common lists {2,3}.
Both cores are saved in the full per-row output; the independent AD3 subset
check finds exactly these two. [PROOF_NOTES](PROOF_NOTES.md) gives the second
core's elementary minimality argument and the primary seven root-pair witnesses.

## 7. Proof status and trust boundaries

The task's counterexample stop condition is met. **No general no-(4,4) theorem
is proposed.** The counterexample is already Sigma-critical, so that condition
alone does not rescue the broad assertion.

The statement adding **full Sigma=933/941 (or one whole-graph D5 image),
Sigma-criticality, induced-C5 disk, interior degree at least four, and epsilon
two** remains unresolved at arbitrary size. The saved D5 action audit finds
zero source graphs with either target relation in the finite domain. This is
absence of an antecedent, not experimental confirmation of that theorem.
No counterexample satisfying its full-Sigma hypothesis is claimed here.

E3's suggested disjoint-path reduction is in
[nonadjacent notes section 5](../c5_excess_two_e3/nonadjacent_notes.md#5-每列-q-core-的完整原省略分類);
E3 REPORT section 4 concerns degree-six roots. It restricts a nonadjacent
all-degree-four core with two retained mixed components. E4 N1-22-44 requires
nonadjacent roots, a sole original mixed component of incidence (2,2), and
the three specified rejected rows. The named source has adjacent roots and
mixed incidence (1,1); neither reduction applies. The mixed-core series
also retains its full-Sigma hypotheses. No missing lemma or new proof attempt
is manufactured after the counterexample stop rule.

New paper evidence here consists of the core-algorithm correctness arguments
and the elementary named counterexample proof. Statistics, graph embeddings
and witnesses are Python finite certificates. Existing source reductions and
ES/ER graph completeness retain their original external/tool dependencies.
No new Lean theorem, four-colour theorem oracle, boundary-state theorem,
epsilon>=3 conclusion or K-infinity equality is asserted. `lake build` was
intentionally not rerun: no Lean file changed and this task adds no Lean claim.

## 8. Replay, validation and delivery

Use the pinned environment, from the repository root. Generate only into an
absent output location; subsequent executions use byte-comparing `--check`.
All mathematical outputs are deterministic and exclusive-created.

```sh
PY=/home/ray/developer/ai/math/.venv/bin/python
$PY scripts/c5_excess_two_c44_input_audit.py --check
$PY scripts/c5_excess_two_c44.py --stage small --check --jobs 8
$PY scripts/c5_excess_two_c44.py --stage full --check --jobs 8
PYTHONHASHSEED=17 $PY scripts/c5_excess_two_c44.py --stage full --check --jobs 8
$PY scripts/c5_excess_two_c44_algorithm_audit.py --check
$PY scripts/check_docs.py
$PY tools/docgraph check
git diff --check
```

[validation.json](validation.json) records actual commands, exit codes,
replay scope, input/output hashes, and delivery limitations. Ordinary and
seed17 full replay compare the entire full mathematical output set, not just
saved checksums. Small replay reruns the independent brute gate.

The initial specified sibling worktree was successfully created at b2ca452.
During execution the environment switched to permitting writes only in the
original workspace and `/tmp`, with the original `.git` read-only. Work
continued in a standalone writable clone `/tmp/math-task-c44`, on the same
task branch/base. The completed clone is retained at
`/home/ray/developer/ai/math/scratch/task-c44-delivery/repository`; the task
commit and transport bundle are produced from that clone. The sibling worktree
remains at its original base. Installing that commit into the original linked
task worktree requires a writable original Git directory.
This location limitation does not change the input files or finite computation.

The documentation checker has two baseline missing paths, independently
confirmed before adding C44: the D5 `c4/scope_ledger.json` and the D2
`integration_doc_changes.diff`. They are outside this task and are preserved;
validation records the actual check result, rather than claiming a clean
documentation check. Guide, HANDOFF, README and all historical artifacts are
unchanged. Only the requested STATUS index line is added. No push or merge.
