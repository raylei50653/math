# Independent custody review: N45-S-LONG-S-T2-Q0-RESTORE

The independent read-only custody review found no payload, authority, or recorded-input drift defect. This judgment concerns custody and bounded calibration records; it does not adopt a mathematical claim. Target output and shared files were not modified.

## Bound delivery and exact tree

- Target: `audits/2026-10-11-n45-s-long-s-t2-q0-restore/`.
- BASE and current HEAD: `f2692089ad4259808e27d9b7e882ac09505b180a`.
- `delivery.json`: 13,113 bytes; SHA256 `920a7161ac5c758dea78c45b9360eb00f81bc6f91ea0c39b45e09723e026b349`.
- Exact payload: 76 files, 1,665,969 bytes. The sole metadata exclusion is `delivery.json`.
- Complete target tree: 77 regular files and 5 directories. No symlinks, special entries, duplicated payload paths, missing/extra payload entries, or payload hash mismatches were found.
- Target still says `待獨立驗收` and `adopted=false`; independent acceptance belongs in this fresh review, not in the worker's immutable original.

## Authority and recorded custody

The 23 dispatch authorities remain correctly separated: 12 BASE Git blobs and 11 sealed physical audit inputs. The BASE inputs match the dispatched Git blob IDs, SHA256 and sizes, current original files, and frozen dispatch copies. The sealed audit inputs match their current original and frozen copies and explicitly retain `git_blob=null` and `included_in_BASE_claimed=false`. The current acceptance and corrections are the adoption authority; original pending claim fields remain historical provenance.

All 3 dispatch metadata pins (`input-pins.json`, dispatch `delivery.json`, and `TASK_B_T2_Q0.md`) match. All 60 recorded custody files match before, after, and currently available bytes. Recorded files include dispatch authorities, frozen copies, dispatch metadata, adopted originals, and the old B certificate/input manifest. The old B certificate is 1,644,932 bytes, SHA256 `e06951edd8150a4f70de270fada08239799dd9ac61fb4fb3552755e667dddd93`. Tracked diff from HEAD is empty. The 60-file statement applies to that explicit set, not to every repository artifact or untracked worker file.

Both reported missing BASE observations were independently confirmed with `git show BASE:path`: exit 128, empty stdout, and the diagnostic that the physical path exists on disk but is absent from BASE:

- `artifacts/c5_no_spoke_exterior/observations.json`.
- `artifacts/c5_single_spoke_residual_locality/observations.json`.

They were not admitted through physical or quarantine substitution. Dependent finite replays were not executed. These findings preserve the inherited finite-terminal trust boundary; they do not establish failure of the new paper argument.

## Retained metadata history and streams

`metadata-initial/` has 16 sealed files: four principal metadata/negative-control JSON files and twelve native command/stdout/stderr files. `metadata-corrections.json` describes per-literal b4-colour precision and the distinction between three schedule/spoke combinations and one distinct spoke variant. Initial records are explicitly historical and do not govern final claims. No reconstructed-stream declaration or adoption-authority substitution was found.

Current normal and seed17 stdout have the identical SHA256 `f3d77fb17c5aa4fedbd88d16a48543a3a9116c695cee654204726d55e066b292`; both stderr files are empty. Stored command records declare exit 0. Both stored negative controls declare exit 1 and retain the expected assertion messages: `calibration certificate mismatch` and `coverage mismatch (all diagonal/empty pin positions required)`. These historical observations are supplemented by root's fresh native replay captures; custody review did not invoke target execution.

The checker validates three abstract forbidden-column cases, two literal-support transports with sixteen ordered pin maps each, and 480 schedule/literal/pin positions. It does not enumerate actual graph assignments, run a finite target source, rerun the old 19 graph controls, establish source existence, prove the paper argument, or establish Lean/general closure. Target-source execution remains false and trigger count remains null (`not triggered`).

The Gallai PDF pin is an inherited dependency from the accepted review: SHA256 `50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea`, 164,927 bytes, no Git blob. Worker metadata explicitly says the origin was not refetched and a direct external theorem revalidation was not executed. This custody review does not upgrade that inherited dependency into a fresh primary-source theorem validation.

## Safe replay interface

Source inspection confirms these target commands are read-only:

```text
python3 -B <target>/audit.py check
PYTHONHASHSEED=17 python3 -B <target>/audit.py check
python3 -B <target>/audit.py check --certificate <target>/negative-controls/bad-q2-column.json
python3 -B <target>/audit.py check --coverage <target>/negative-controls/missing-diagonal.json
python3 -B <target>/audit.py verify-delivery
```

Do not execute target modes `build`, `run-checks`, or `finish`: they create files inside the immutable worker directory. `verify-delivery` alone does not inspect filesystem entry types; this independent custody check supplements it with an exact type/inventory check.

Run the fresh independent custody verifier with:

```text
python3 -B audits/2026-10-11-n45-s-long-s-t2-q0-restore-review/independent-custody.py
```

It performs independent checks without importing the worker checker or writing any files. It emits a JSON inventory/result to stdout. Root captures native stdout, stderr, exit, and the exact command in this fresh review directory.
