# D₅ B₄ independent audit

The returned B₄ branch is accepted at its exact scope: **W933-129**, literal
roots `a=5,b=6`, original spokes `04/12`, original long face
`[2,6,5,4,3]` with envelope `{2,3,4}`, and a designated shared original
contact whose actual boundary attachment is **exactly `{4}`**. Six shared
identities give eight designated choices; their conditional attachment branches
are excluded. D4 has no shared contact and is not a target of this exclusion.
This registers no exclusion of the whole skeleton, the whole long face, any
other actual attachment branch, or a root-swapped named source.

`scope_ledger.json` preserves all 20 original 933 named rows and all 20 original
941 named rows, and records the seven identities individually. The ledger does
not rewrite the original B or B₃ artifact. Source omission/q-core conclusions
are inherited as exact data, not promoted to pinned-pair edge minimality.

## Original-graph paper proof

Under the stated B source hypotheses, H−{a,b} is the single original connected
component C with no unary. Every original C vertex has full degree four,
each root has two distinct C contacts, and the original induced C₅ boundary
is preserved. A designated shared v has external neighbors exactly a,b,b₄;
hence deg_C(v)=1. Its original C edge vt is a bridge. Since each root has
another distinct original contact, C−v is nonempty. Removing a leaf from a
connected graph leaves **K=C−v connected**, including every other original
edge, contact, bridge, block and side branch.

The complete original cut of K consists of ax*,by*,vt and every actual K−B
edge. Even if x*=y*, the root incidences ax* and by* are distinct edges.
Summing the full degree four at every K vertex therefore gives
`4|K|=2|E(K)|+3+n_B`. The left side and twice the internal edge count are
even, so n_B is an odd nonnegative integer and consequently positive.
There is an actual original K−B edge.

The five bags `{a},{b},{v},B,K` are nonempty, pairwise disjoint, and connected.
All ten bag pairs have original edges: ab,av,bv; an a-spoke, a b-spoke,vb₄;
ax*,by*,vt; and the parity-forced K−B edge. Contracting connected bags yields
K₅. Contraction preserves planar embeddability, while K₅ violates the planar
simple-graph bound `|E|≤3|V|−6` (10>9). The assumed disk source is impossible.
This argument works for singleton K, arbitrary bridges, blocks and side
branches; it does not invoke Gallai terminal-block classification, use the
finite graph catalogue as a source classification, or claim that minor
contraction preserves relations, pinned fibres, or Sigma.

The report's geometric star insertion is a separate crosscheck. Independent
rotation enumeration found all two original disk rotations among 64 original
rotation candidates. Each of the 108 original-order-preserving insertions of
av,bv,b₄v was assessed. Exactly one extension per original rotation places v
in the named long face, leaving the sole common a,b,v face the triangle abv.
The principal degree-parity/minor proof does not depend on this crosscheck.

## Lists and external theorem boundary

Original-edge enumeration of G−C reproduces every legal root pair of rejected
rows 1,3,4,6: 11 pairs in total. The shared leaf is tight with a singleton list
in all 11. The row-4 list for 01202 is `{3}`, `{0}`, `{1}` for root pairs
`(1,0)`, `(1,3)`, `(3,0)` respectively. B₃'s degree-one strict-slack exclusion
is inapplicable to this exact frame.

All actual attachment subsets were independently generated from the long-face
envelope and exact same-frame lists. The original table has 13 permissible
owner/attachment candidates. Checking the same actual bridge neighbor across
all 11 row/pairs gives 143 checks and removes exactly five candidates, leaving
eight. For every owner, the remaining attachments are ∅ or `{4}`. The 13→8
step is a necessary-list calculation; survivors are not source realizations.
They are closed by the separate complete original-cut proof above.

[Zdeněk Dvořák, *List coloring and Gallai trees*](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf),
Lemma 7 on PDF page 5, states the connected degree-assignment conclusion used
for this ancillary table. The live primary PDF was reviewed and downloaded;
its 164,927 bytes match the preserved D₄ PDF exactly, SHA256
`50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea`.
See `primary_source_review.json` and `gallai-primary.pdf`.

The required strict-slack fact also has a direct proof: root a spanning tree
at a vertex whose list size exceeds its internal degree. Greedily color all
other vertices in decreasing tree depth; each has an uncolored parent and
thus at most degree−1 already colored neighbors. Color the root last; its
strict slack supplies a color. For K, fixing v's singleton only removes that
color at t. If the color was already absent from t's list, t becomes a strict
slack vertex and the whole connected K colors, then v attaches. No theorem
about terminal blocks or pinned-pair minimality is needed.

## Independent finite certificate

`audit_b4.py` imports only the audit-local `independent_core.py` and Python
stdlib. The helper derives from the preserved D₄ B₃ independent utility,
with provenance/hash recorded in `audit_source_versions.json`; it adds freshly
generated full coloring witnesses. No research checker, enumerator, relation
join helper, or witness validator is imported.

The audit reconstructs each of 40 literal full-degree graphs from the actual
original edges, rather than accepting component metadata. It validates actual
attachments, owners, ordered contacts, identity equalities, boundary order,
complete degree counts, every original C bridge set, K connectivity, all
original cuts and odd positive n_B. Eight controls have the minimal two-shared
original C edge and singleton K. It validates 40 nonempty/disjoint/connected
five-bag minors and all 400 interbag original edge witnesses. It checks all
752 stored connectivity paths and the 16 additional actual subdivision paths,
for **768 original-edge paths** in total.

It independently rebuilds all 400 full R_C relations and 2,400 full original
whole-graph joints over the ten literal boundary rows, including G, all four
literal original spoke deletions, and G−C. All 38,400 pinned root-pair fibres
are separately enumerated, including **29,768 empty fibres**. The original
5,336 R_C witnesses, 25,416 joint witnesses and 25,416 repeated pinned joint
witnesses are validated on exact original edges and their common color frame.
An additional 5,336 newly generated R_C witnesses and 25,416 newly generated
joint witnesses are independently validated and preserved in `relations.json`.

All 1,600 spoke restorations and 1,200 literal root-swap relation/fibre checks
pass. For each global S₄ permutation, the entire boundary and every shared
color are moved together. The audit independently re-enumerates 9,600 complete
transported C relations and **57,600 complete transported whole-graph joints**,
and validates all **609,984** transported individual original joint witnesses.
These transformations register no new named source exclusion.

The 40 finite controls are full-degree graphs with K₅ minors, not disk sources.
They prove the claimed fixed-domain relation and witness checks. The arbitrary
size source exclusion is the separate original-graph paper argument. No new
Lean theorem was added; `lake build` does not formalize this paper topology,
source family, or full relation semantics. Epsilon≥3, all mixed22, source
realizability, general exits and K∞=K≤5 remain unproved.

## Attempts, versions, replay

Every attempt has immutable source copies, source hashes, `run.log`,
`results.json` and separate `execution_metadata.json`. Failures keep their
tracebacks. Attempts and the original D₄ package are not overwritten.

- `default/attempts/0001`: failed because the new audit compared producer face
  enumeration literally against its independently ordered dart traversal.
  The cycles were the same modulo starting vertex. This audit-only failure is
  preserved. The fix compares directed face cycles modulo their starting
  vertex; no graph orientation, production report, checker, helper, or artifact
  was changed.
- `default/attempts/0002` and `seed17/attempts/0001`: passed the first independent
  full enumeration. These successful earlier-source records are preserved.
- `default-final/attempts/0001` and `seed17-final/attempts/0001`: passed the final
  source after stronger original-bridge, regenerated-witness and selected
  K−B path validation. Timings were 11.007 and 10.839 seconds respectively.
  Their `results.json`, `relations.json`, `scope_ledger.json`, `exact_lists.json`
  and audit version JSON are byte-identical. Paths and timings are kept outside
  the semantic results. `final_comparison.json` records exact hashes.

The canonical `results.json`, `relations.json`, `scope_ledger.json` and
`exact_lists.json` are copies of the final successful default immutable attempt.
Final source hashes are:

| Source | SHA256 |
| --- | --- |
| `audit_b4.py` | `23cab5a101438c673b27683fc1c1bc38544cc4eb39f161ea9406e44e479a1fb8` |
| `independent_core.py` | `2fe4ddffda62a36b22c6f4224189f226ba56a8b7d15c7865b3f3d43de3829afa` |

Replay into a fresh output directory:

```bash
python3 audits/2026-10-04-task-d5/b4/audit_b4.py \
  --repo audits/2026-10-04-task-d5/snapshot \
  --output audits/2026-10-04-task-d5/checks/b4-final-root-replay
```

Stop at the accepted shared-{4} branch. No research expansion, commit or push
is authorized or performed by this independent B₄ audit.
