# A/B independent custody and source-provenance review

BASE: `f2692089ad4259808e27d9b7e882ac09505b180a`.
Targets: `N45-S-LONG-S-DIRECT` and `N45-S-LONG-S-FIBRE`.
This review verifies delivery bytes and source provenance. It does not judge the paper proofs,
source-exclusion candidates, source realization, or Lean. No target/shared file was modified.
Root owns the final acceptance judgment and native execution logs of the persisted verifier.

## Exact delivered trees and hashes

| Target | Payload files | Payload bytes | Actual regular files | Directories | BASE/live/frozen inputs |
| --- | ---: | ---: | ---: | ---: | ---: |
| DIRECT | 51 | 3,000,959 | 53 | 13 | 18 |
| FIBRE | 846 | 55,949,264 | 847 | 18 | 58 |

The independently scanned relative file and directory sets match the declared inventories.
Every payload SHA256 and size agrees. There are no symlinks, special files, missing files,
extra files, unsafe relative paths, or duplicate payload paths.

DIRECT precise metadata exclusions are `delivery.json` and `seal-receipt.json` only.
The latter independently binds the former's SHA256. Its quarantine snapshot remains hashed payload.
FIBRE excludes only `delivery.json`. The following historical drafts remain hashed payload,
explicitly outside current authority: `inputs-initial.json`, `metadata-initial/claims.json`,
`metadata-initial/obligations.json`, `metadata-initial/reviews.json`.

| Artifact | SHA256 |
| --- | --- |
| DIRECT delivery.json | `13532f13ff6ca1ef1954d840365aef1de69dbef250707bb1c4efa6fd0c16a15f` |
| DIRECT REPORT.md | `052dec22898f9ab51169b40a2901affc68ff3028bd12854cc09a8614431f8d7c` |
| FIBRE delivery.json | `5ef4df9be39637f68bde661d2b724eb9ab7671754dea588938093e76abced0ab` |
| FIBRE REPORT.md | `68f26177e3ecf1b144eb21b3c8fc25fd89fe66b40832a6b5df89a168c630da90` |
| FIBRE certificate.json | `e06951edd8150a4f70de270fada08239799dd9ac61fb4fb3552755e667dddd93` |

## BASE authority and external pin

All 18 DIRECT and 58 FIBRE registered frozen inputs equal their recorded Git blob IDs and
actual Git blob bytes at BASE, their recorded SHA256/size, and current live paths.
The complete frozen directory sets equal the registered inputs plus DIRECT's external PDF.
Current BASE paper citations resolve to registered verified inputs: eight distinct DIRECT
frozen evidence paths and eighteen FIBRE evidence paths. Neither current claims file cites
quarantine, superseded drafts, or the missing artifact paths below as admitted authority.

Both declared external PDF pins are 164,927 bytes with SHA256
`50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea`.
DIRECT stores it at `frozen/external/gallai.pdf`; FIBRE at `external/gallai.pdf`.
The declared URL is `https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf`, with Git blob null.
This custody review verified cached bytes/declarations and did not refetch origin or validate
external theorem applicability.

## Missing artifact findings retained

DIRECT's `SOURCE-ARTIFACT-NOT-IN-BASE` identifies
`artifacts/c5_no_spoke_exterior/observations.json`.
The BASE Git check independently returns exit128. The quarantine snapshot is 2,314,779 bytes,
SHA256 `d13c5aa2e94a610f3b220b57e03903170eb641871c04103ec12ed5cf5d3dd14d`,
and equals the current on-disk original. It remains excluded from mathematical authority;
no dependent BASE artifact replay or baseline replacement is claimed.

FIBRE's `BASE-FINAL-JSON-MISSING` identifies
`artifacts/c5_single_spoke_residual_locality/observations.json`.
The BASE Git check independently returns exit128. Its recorded exploratory physical-read hash
`24f8d039c905bfc51ce3a806f58edae7f89155282ca87e70cd8751b8db565118`
equals the current live bytes. It is not an admitted frozen input or claim/control authority.
The separately tracked original `(2,2)` observations, final support table, and paper reports
are admitted and verified at BASE; the missing final JSON replay remains unexecuted.

These findings are nonblocking for the delivered byte custody and explicitly conditional
paper provenance. They continue to block treating the absent BASE artifact replays as verified.
No qualifying finite source is established by either delivery.

## Execution and historical recording limits

The reviewer ran FIBRE `checker.py --check` read-only: exit0, reproduced canonical SHA256 above.
The specified negative certificate was run with `--check --certificate`: expected exit1.
Its unique JSON-content change is `controls[0].rows[0].C.assignments[0][0]`: 0 to 99;
its larger byte size reflects formatting rather than further content changes.
These checks preserve the source-status boundary; they are not paper-proof validation.

DIRECT openly states in `execution-notes.json` that initial setup had merged tool streams,
without reconstructed separate stdout/stderr. Its later verification captures are separate.
FIBRE `finalize.py` lines 8-19 reconstructs streams/metadata for the earlier tool-observed
`seal-attempt1` forward-link failure. This review cannot independently certify those reconstructed
historical streams as native subprocess capture. They are not current theorem/certificate evidence.
The remaining current byte checks and explicit historical/current authority separation pass.

Only the clearly read-only FIBRE checker `--check` forms were executed in this subreview.
DIRECT `validate.py --contents --manifest` is read-only by inspection; root owns its replay.
FIBRE `seal.py --check-only` writes logs and `final-checks.json` and must not be used as a
read-only replay. No setup/seal/finalize/generation wrapper was run by this reviewer.

## Reproducible custody verification

[independent-custody.py](independent-custody.py) uses only the Python standard library,
reads both full delivery trees, all registered BASE/live/frozen inputs and external pins,
and repeats each expected missing-BASE-blob check. It prints JSON and writes no files.
It checks exact directory/file types and inventories, before/after target-tree equality,
metadata exclusions, historical payload declarations, hashes, and receipt binding.

Run from the repository root:

```sh
python3 -B audits/2026-10-11-n45-s-long-s-review/independent-custody.py
```

Root captures native stdout/stderr, command and exit metadata separately.
No custody blocker was found. Mathematical acceptance remains a separate review obligation.
