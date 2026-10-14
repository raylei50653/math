# Verification of the other return branches

2026-10-14. BASE and immutable direct input hashes are in
[INPUTS.json](INPUTS.json). This audit was developed in an exclusive detached
worktree at the same BASE as the canonical main checkout. Only the connected
new audit and its local documentation consumers were adopted; no old
mathematical certificate was overwritten. No commit or push occurred during
the research stage. The subsequently authorized connected publication is
recorded in [publication history](../../docs/history/2026-10-14-c4-return-branches-publish.md).

## Mathematical review

- [High-r review of p/q](r_high/PQ_REVIEW.md) independently verifies the
  two exterior-quotient size calculations, exact mask14, both complete-fibre
  maps, and the role-swapped degree-five return. The new source conclusion
  is p=q=5⇒ell≥6; the surviving double-low branch remains OPEN.
- [Rotation and p/q review](general/INDEPENDENT_REVIEW.md) verifies complete
  singleton transport, exact side scopes, and the p/q paper results.
- [p/q review of high-r](pq/HIGH_REVIEW.md) verifies the actual zr nonedge,
  quotient colourability at k−3 interiors, all three proper C5 z=r types,
  the generic956／1012／1020 frontier and the alias424 exclusion. Thus
  a=4⇒t≥6 and c=4⇒s≥6 in all three retained source cases.
- The root independently checked the general missing-colour attachments
  and the subset X0↔Y0 full-fibre switch, together with the displayed source
  quotient and degree-loss calculations. The general return ends in an
  admitted sector; no full mask13 exclusion is claimed.

## Read-only computational replays

The four final local checkers verify fixed finite domains. They do not
enumerate source graphs or construct actual target-source controls.

```sh
python3 -B audits/2026-10-14-c4-return-branches-a11d4bb/pq/check.py --check
python3 -B audits/2026-10-14-c4-return-branches-a11d4bb/r_high/check_high.py --check
python3 -B audits/2026-10-14-c4-return-branches-a11d4bb/general/check_general.py --check
python3 -B audits/2026-10-14-c4-return-branches-a11d4bb/rotation/check_rotation.py --check
```

Each was replayed normally and with `PYTHONHASHSEED=17`; all passed. Each
also rejects an independently corrupted certificate. Commands, stdout,
stderr, exit codes and expected negative outcomes are retained in
[p/q receipts](pq/receipts.json), [high-r receipts](r_high/logs/v2-receipts.json),
[general receipts](general/receipts.json), and
[rotation receipts](logs/rotation-receipts.json).

The original return checker also passed normal and seed17 replay; see
[baseline receipts](logs/baseline-receipts.json). Frozen-input verification
records zero drift in [frozen-drift.json](logs/frozen-drift.json).

Initial tuple/list serialization mismatches, failed preliminary assertions
about the nine-vertex non-source disk, and the weaker high-r ten-mask/424
control remain retained. The latter control was mathematically sound at
its necessary-model level: the paper quotient argument supplies the new
premise that eliminates its alias source domain and seven generic masks.
An admitted non-source calibration graph does not rescue that source domain.

Final root replay and documentation receipts are in
[adoption-receipts.json](logs/adoption-receipts.json). Formal-doc DocGraph
and the whole-tree check are reported separately. Existing duplicate IDs
in retained frozen/scratch history are preserved and are not erased to
obtain a whole-tree PASS.

Actual documentation results: check_docs PASS (684 Markdown files and
8,917 links), formal-doc DocGraph PASS (97 documents, 380 relations), and
git diff --check PASS. Whole-tree DocGraph FAIL with70 duplicate-ID errors;
its stdout and stderr exactly match the retained prior audit baseline, as
recorded in [baseline comparison](logs/whole-docgraph-baseline-comparison.json).
The new audit's57 local Markdown links were also checked directly, with no
missing paths or anchors; all14 frozen inputs still have zero drift. See
[final custody](logs/final-custody.json).

## Scope and propagation

New arbitrary-size paper scope: single-p/q exact mask14 with full-fibre
split; double-low ell≥6; all-three-source a=4⇒t≥6 and c=4⇒s≥6; restricted
rotated side bounds; generic t=5 three-mask frontier. New finite scope:
all-lift tables, necessary component closure, honest non-source full-fibre
controls and source-colour-hypothesis transport. The r=7 model retains
26 outer types and111 joint orbits, with no source exclusion.

The C4 topic, Kempe guide and STATUS direct entry are updated. The parent
mask13, T／T0 and catalogue equality remain OPEN with the same common
k≥23 bound; cross-line synthesis and no4ct handoff remain accurate as
broader OPEN summaries and are reviewed unchanged. No HANDOFF research-line
or active-marker change occurred. Propagation stops at the direct topic.
There is no new Lean theorem or external theorem/enumeration replay.
