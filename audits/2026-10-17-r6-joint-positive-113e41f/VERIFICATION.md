# Verification and authority boundary

BASE is `113e41f7023aa00c8257b815ce8727035b648f26`.
[BASE.json](BASE.json) seals 202 initial inputs; the two additional input
manifests seal four further original authority files. Frozen copies retain
their exact bytes. Live routing documents may change as authorized by this
research update; the old mathematical inputs may not.

## Research replays

Run from the repository root:

```sh
python3 -B audits/2026-10-17-r6-joint-positive-113e41f/A/check.py
python3 -B audits/2026-10-17-r6-joint-positive-113e41f/B/check.py --check audits/2026-10-17-r6-joint-positive-113e41f/B/certificate.json
python3 -B audits/2026-10-17-r6-joint-positive-113e41f/C/check.py
python3 -B audits/2026-10-17-r6-joint-positive-113e41f/integration/full_count_cone.py --source-mask 932 --certificate audits/2026-10-17-r6-joint-positive-113e41f/integration/counts932.json
```

Repeat the last command with both occurrences of 932 replaced by 933 and
941. Repeat the read-only commands with `PYTHONHASHSEED=17`. A also accepts
`--seed 17`; its matching enumeration is exhaustive and does not sample.
The count solver used SciPy 1.18.1 through `uv run --no-project --with scipy`;
the saved rational certificates need only stdlib Python to verify.

Worker receipts:

* [A](A/VERIFICATION.json): active certificate-v3, normal/seed17,
  corrupted chord rejection and exclusive-create rejection. The v2
  tuple-versus-list replay failure and original seals are preserved.
* [B](B/VERIFICATION.json): corrected scope, normal/seed17, three negative
  controls and exclusive-create. [Rejected initial evidence](B/initial/REJECTED.md)
  retains the failed topology claim, including the earlier checker PASS.
* [C](C/VERIFICATION.json): all 16384 pin slots and complete r fibres,
  normal/seed17, missing-zero-slot rejection and exclusive-create.
* [Full count cone](integration/COUNT_VERIFICATION.json) and
  [exclusive-create](integration/COUNT_EXCLUSIVE.json): all three exact
  witnesses, seed17 and changed-count/cube-weight/projection rejections.

Paper results were independently reconstructed: [A review](integration/REVIEW-A.md),
[corrected B review](A/REVIEW-B.md), [C root review](integration/REVIEW-C.md),
[C peer review](B/REVIEW-C.md), and [full labelled count review](C/REVIEW-COUNT.md).
The last review independently reconstructs all 8688 labelled rows for
original support932 without importing the root's orbit helpers.

## Verification scope

Finite graph controls positively exercise both nonfacial and facial
seven-defect shapes. They are not minimum no4ct sources. Source realizability
is **not triggered**, with zero supplied source instances. The arbitrary-size
authority for the new source implications is the paper proofs plus their
explicit previously sealed source theorems; the checkers calibrate local
arithmetic and finite controls. The full-nine-boundary count result is exact
constructive feasibility of a relaxation, not a graph realization.

`lake build` completed successfully with 8832 jobs during this turn, with
existing AttachmentOrder/SymRelabel linter warnings. No Lean source changed
and no new paper theorem is claimed formalized. No external theorem or
4CT was used. No unrelated research enumeration or generated-artifact suite
was rerun. Final root replay, documentation, DocGraph and custody receipts
are recorded under `integration/`.

## Final root results

[FINAL_CHECKS](integration/FINAL_CHECKS.json) records successful independent
root replays of A, corrected B and C, documentation checks, formal-doc
DocGraph, the scoped DocGraph and `git diff --check`. Whole-tree DocGraph
returns exit 1 and has 70 duplicate-ID diagnostics; it is **not** reported
as passing. [Comparison](integration/DOCGRAPH_COMPARISON.json) separately
reconstructs the 70 diagnostic groups with the new audit excluded. The
new frozen routing copies retain their original IDs; historical evidence
was not normalized or removed to hide duplicate occurrences.

[Custody](integration/CUSTODY.json) verifies all 206 frozen inputs and
their live mathematical originals without drift. The only live changes
among authority paths are the three authorized routing documents STATUS,
the Kempe guide and the C4 direct-parent entry. HEAD remains the frozen
BASE; no commit or push occurred.

The completed bundle is listed in `MANIFEST.json` and `SHA256SUMS`.
From the repository root, the latter replays with:

```sh
sha256sum -c audits/2026-10-17-r6-joint-positive-113e41f/SHA256SUMS
```

The custody and bundle hashes verify identities, not the mathematical
soundness of an arbitrary-size proof. In particular the rejected B draft
is preserved as rejected evidence, never as an accepted theorem.
