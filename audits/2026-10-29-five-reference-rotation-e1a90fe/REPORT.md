# Common odd-cycle rotation receipt

2026-10-29. BASE `e1a90fea41702d7c98747716a5960198aecbecb3`.
Canonical proof and scope: [five-reference common rotation](../../docs/c5_five_reference_common_rotation.md).

Paper: R5-SIDE proves even side-changing hit count on one actual O with one
shared rotation word; R5-SEG proves odd interior alternating segments,
noncrossing within each reference, and exterior endpoint-type parity.
R5-ONEHIT derives equal endpoint sides and, for inward endpoints, an even
complete reference-return path. Chords retain both endpoint incidences.
No external theorem or Lean proof is claimed.

`verification.json` independently re-enumerates complete ordinary/even
families on the old 16 disks and frozen F4 disk. All five adjacent families
are examined. There are 3 positive-odd minimizers, 9 reference combinations,
12 odd-cycle/reference checks, 68 full region batches and 30 explicit
ten-family-pair records containing all 9 reference products. Missing families
are explicit. No disk in this finite set has all five star families present.

The frozen F4 candidate still has its nine-cycle and two disjoint cross
segments; it passes common side parity and actual segment tests. It is not
a PM04 minimizer, so no minimum-only C1 claim is attached. IDs 12 and 14
retain the original six concentration tests and thirty legal shared cuts.

Separate complete algebraic control: deterministic triangle expansion of
the marked star, 15 internal vertices/25 edges, complete 0/2/4 families,
all five even star families singleton, adjacent even families empty.
All five double-dimer equations are 8=8; all five hits, full C1 regions,
36 region batches and exact rewires pass. Proposed odd-triangle side word
100 fails the new equations; actual reference constraints plus the exterior
leaf allow 000. All ten full family products retained. The old full boundary
and shared-cut tests already reject this marked graph (five crossing products,
25 canonical actions with no feasible assignments), so this is NOT a new
exclusion beyond that full package and NOT a plane source.

F5-CHAIN9 is a separate abstract profile relation. Each singleton has a
retained length-eight arc and allows an even length-two return; the
concentration summaries satisfy C1's bound. All ten pairs have 32 common
side words; every four-reference subset has 8; the full five-reference
common side relation is empty. No actual full Q or matching families are
claimed at this profile layer.

Validation executed:

```bash
python3 scripts/c5_five_reference_rotation_verification.py --check audits/2026-10-29-five-reference-rotation-e1a90fe/verification.json
python3 scripts/c5_two_reference_parity_verification.py --check audits/2026-10-29-two-reference-parity-e1a90fe/verification.json
python3 scripts/c5_parity_shared_cut_verification.py --check audits/2026-10-29-parity-shared-cut-e1a90fe/verification.json
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
python3 tools/docgraph check
git diff --check
```

All three research certificate checks PASS, including the old original
source hashes. `git diff --check` PASS. Formal-docs DocGraph PASS:
98 documents, 386 relations, 12 families, zero errors.
The whole-worktree DocGraph FAILS with 72 duplicate-ID errors in retained
audit/scratch copies; no copies were deleted. `check_docs.py` FAILS with four
errors in concurrent files outside this change: missing saturated-hub
verification JSON; missing three-step-source-invariant results/verification
JSON; three-step-source-invariant report not yet directly indexed by STATUS.
No errors were reported for this new report or its links. These are the
observed check results at execution, not a claim that unrelated concurrent
work is finished or frozen.

Closure scope: only the named local lemmas and the stated candidate
rejections. General simultaneous five-reference blocking, E932 and 4CT
remain OPEN. No broad F4/P4 generator extension, commit or push.

Updated: canonical source, its two immediate entry reports, relevant guide
paragraphs, parity task entry and STATUS link. Reviewed-unchanged: HANDOFF
and README (no research-line/status change); the original scripts and
certificates (frozen bytes retained). Propagation stops at local source and
direct topic routing; no parent existence theorem is closed or superseded.
