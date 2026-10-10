# N45-L2C: independent LOW2 artifact, tool, and coverage audit

BASE: `dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`.

**Verdict: ACCEPT_SCOPED_ARTIFACT_INTEGRITY. No blocking artifact finding.** This audit does not decide the six paper claims or formally adopt LOW2. BASE arguments and the external Gallai theorem remain mathematical dependencies for separate paper review. No source realization, new Lean, or general N2/E result follows from these tool checks.

The worker delivery examined is `audits/2026-10-10-n45-s-low2/`. Its complete 85-file tree is copied into [frozen/worker](frozen/worker/); [inputs.json](inputs.json) records every digest and the independently checked capture boundary. [independent-judgment.json](independent-judgment.json) gives the structured verdict. Existing worker and old audit bytes were preserved. Only this exclusive audit directory was written; no commit, push, PR, external message, or delegation was made.

## Exact seal coverage

The primary worker manifest has **66 regular payload files and zero symlinks**. Delivery excludes exactly 19 relative paths: top-level `MANIFEST.sha256`, `delivery.json`, `receipt.json`, and the 16 specifically named `receipt/{run}.{stdout,stderr}.log` files. The exclusion compares complete relative paths. It does not exclude matching basenames anywhere else.

The chain is complete: delivery binds the primary manifest and receipt JSON; receipt JSON binds all 16 named logs. There are 17 receipt metadata files including `receipt.json`, plus the primary manifest and delivery. All 85 regular files have a named place in that structure. Nested LOW1 and L1R delivery files and LOW1's `seal-final-v4/commands.json` are ordinary payload and included. The independent reviewer seal also excludes only exact top-level paths, so the whole frozen 85-file worker, including its receipt metadata, is protected by the reviewer manifest.

| Worker object | SHA-256 |
| --- | --- |
| `MANIFEST.sha256` | `eb80de720c9089b7e8e61671949be1c84a2312995379a18c84a1206f83d8f752` |
| `receipt.json` | `dbebff864f9f61e6059cce4f6a3028372abf486c3b1169d4f1ecaf822b902ef0` |
| `delivery.json` | `5458cdafce8599d7612c67410a3c727c49d98520c5b5f842b841502201800930` |
| `REPORT.md` | `1459d6265a4a2d087399029c4d0c8ec0a19a8b4bad509d1b3082d4465c206446` |

All four named BASE objects were independently obtained with `git show`, their Git object IDs checked with `git rev-parse`, and their frozen bytes compared. The eight task pins were independently rehashed against current inputs at capture. The 20 named frozen current inputs all match their recorded hashes, including the task text and eight pins. The external PDF bytes match the named BASE PDF; the worker's HTTP retrieval and theorem interpretation are not independently re-performed by this artifact audit.

## Actual replays and rejection stages

[checker.py](checker.py) is independently authored standard-library code. It does not import worker code or execute worker mutators. Its reproducible scope is frozen artifact evidence; its output explicitly excludes current whole-workspace coverage and mathematical proof.

[checks.json](checks.json) contains actual subprocess commands, environments, exit codes, and persistent stdout/stderr. Normal and seed17 each exit 0 and their stdout is byte-identical. The six original worker negative fixture types were independently replayed with the following actual results:

| Control | Actual exit | Rejection stage |
| --- | --- | --- |
| bad digest | 2 | manifest digest |
| missing nested delivery | 2 | exact payload inventory |
| duplicate path | 2 | manifest duplicate path |
| unsafe path | 2 | manifest unsafe path |
| missing payload | 2 | exact payload inventory |
| bad receipt | 2 | final delivery receipt binding |

An additional negative removes the nested LOW1 receipt command file from an otherwise correct manifest. It exits 2 at exact payload inventory validation. This directly checks preservation of nested receipt metadata without relying on basename exclusions.

All these artifact controls are classified `triggered and holds` for their declared synthetic artifact conditions. They are not LOW2 graph source controls and are not a trigger count for source realizability.

The original worker normal and seed17 sealing commands used `--payload-only`, so those receipts do not individually prove the final receipt chain. Parent root recorded full strict normal and seed17 checks, both exit 0 with matching stdout, before adding new supervisor or reviewer directories. It also recorded actual digest and final-delivery bad-receipt rejects, each exit 2 at the specified stage. Those results are frozen in [root-initial-strict-replays.json](frozen/root-initial-strict-replays.json) and bound by [inputs.json](inputs.json). The independently authored checker here checks the complete final frozen chain on every positive replay.

The original sealing-time bad-receipt command imported `verify` and overrode `read_json` only for the absent final delivery, returning a provisional delivery whose receipt digest was zero. Its exit 2 demonstrates that synthetic binding probe. It does not establish generic checker soundness or cover receipt-log tampering at all later stages. This limitation is explicitly recorded in the worker receipt. This reviewer independently rejects the persisted bad receipt against the actual frozen final delivery, without an override.

## Workspace and historical coverage boundaries

At capture, this audit independently rehashed **32,177** pre-existing regular file records and checked their modes, **27** symlink targets, and the existence of **four** nested repository directory entries. The worker's initial tracked and cached Git diffs were byte-equal to the live diffs. Eight task pins matched. Existing named files did not drift during this capture.

The four directory entries are `audits/2026-10-09-n45-pc/source/`, `audits/2026-10-09-n45-pg/base-source/`, `audits/2026-10-09-n45-pr/base-source/`, and `audits/2026-10-09-n45-u/source/`. Their contents are not recursively hashed by those directory records. This audit preserves that limitation.

The worker strict verifier requires exact equality to its original Git-listed inventory. New isolated root and reviewer audits change that inventory, and later authorized adoption may change live pins or diffs. Those are reasons to replay the frozen independent checker, not to weaken the sealed worker verifier or claim current workspace equality. This audit does not repeat the original exact live inventory after the new directories have appeared.

Seven worker check commands retain their recorded exits and logs. Current formal documentation DocGraph passed with 62 documents, 213 relations and five families. Retained BASE link checking failed with the same two historical missing paths. Whole-worktree DocGraph failed with 62 duplicate-ID errors due to retained copies. The historical E4 provenance FAIL is declared retained and was not rerun. This reviewer does not delete any retained copies or change those FAIL records, and does not claim current docs acceptance from those earlier logs.

The six claim IDs and full contract copies are intact; all are explicitly non-machine-proved. `source_controls=[]` and `source_control_evaluation="not established; not executed; no trigger count"` are preserved. Finite source controls were neither established nor executed. No source trigger count or source exclusion is inferred. No new Lean was created and no `lake build` was run.

## Read-only replay

Use `python3 -B audits/2026-10-10-n45-l2c/checker.py` for the frozen worker chain. Use `PYTHONHASHSEED=17 python3 -B audits/2026-10-10-n45-l2c/checker.py` for the deterministic replay. To verify this entire independently sealed audit as well, use `python3 -B audits/2026-10-10-n45-l2c/verify.py` and the same command with `PYTHONHASHSEED=17`.

The exclusive capture, checks, and seal scripts are retained for review; they are not read-only replay entry points and must not be rerun into this sealed directory. [delivery.json](delivery.json) binds the reviewer manifest, [receipt.json](receipt.json), and exact seal metadata. A failed seal would remain preserved under a separate version; this delivery's seal succeeds without an overwritten attempt.
