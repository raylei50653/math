# W7 connected publication dependency and artifact review

Read-only review of the three pending W7 audit roots. No source/audit bytes,
Git index, archive index, or solver state were changed. All review writes are
inside this new dependency directory. Scientific/finite/necessary-cone status
is unchanged; all results remain OPEN without an exact certificate.

## Connected scope and exact preservation whitelist

All three roots are connected to the requested publication:

1. `2026-10-20-w7-count-cone-d5b8a86` supplies the complete source contract,
   integer checker, exact incomplete residual, and sealed numerical attempts.
2. `2026-10-20-w7-count-opt-d5b8a86` supplies the X-only model, original
   coordinate maps, pinned cache, optimization history, and the original warm X.
3. `2026-10-21-w7-reuse-d5b8a86` consumes those inputs and supplies the literal
   template/rank proofs, compiled CPU operator, independent checks, and one
   bounded numerical trial.

The explicit [all-connected-paths.txt](all-connected-paths.txt) lists **251
non-transient files / 119,118,856 bytes**. This is the full connected preservation
set, not a request for blanket staging. Only bytecode and native build outputs
are excluded; their source/build rules remain included. The historical failed
and unfinished attempts belong to the evidence record, and cone OUTPUTS.json
also seals their saved payloads, so silently dropping them breaks custody.

| Root | Preserve files | Raw bytes | Suggested archived files |
| --- | ---: | ---: | ---: |
| cone | 96 | 81,688,506 | 19 |
| opt | 85 | 28,020,139 | 13 |
| reuse | 70 | 9,410,211 | 3 |

The [ordinary-paths.txt](ordinary-paths.txt) whitelist contains 216 files /
7,341,064 bytes. The [archive-paths.txt](archive-paths.txt) whitelist contains
35 paths / 111,777,792 raw bytes, selected for size >=1,000,000 bytes or
historical whitespace. These paths deduplicate to 32 new blobs, estimated at
54,556,051 gzip bytes using the same deterministic GzipFile settings as
`tools/audit_archive.py`; see [archive-estimate.json](archive-estimate.json).

Use the existing archive append mechanism with this explicit path whitelist,
preserving the originals and every old ARCHIVE record. Stage only the listed
ordinary paths plus the newly added archive blobs/index/ignore changes and the
connected publication/routing records. No new generated-artifact exception is
needed. `cone/BASE.json` is 1,075,046 bytes and is the strict current
`check_generated_artifacts.py` JSON-policy blocker if staged as an ordinary
file. Other large NPZ/pickle/gzip payloads are outside that checker's suffix
set but are included in the archive recommendation for storage consistency.

## Provenance and replay dependencies

The [inventory](inventory.json) checks every pinned input and output seal:

- Cone BASE: all 2,649 input paths exist and match SHA256; every one is already
  covered by existing Git files or existing ARCHIVE records.
- Reuse BASE: all nine inputs match SHA256. Its four not-yet-published inputs
  are cone/MODEL.md, opt/model.py, opt/cache/model.npz, and opt/HANDOFF.md; all
  four are included in the preservation set.
- Cone OUTPUTS: all 88 records match. Reuse OUTPUTS: all 69 records match.
- Original caps.json.gz and orbits.json.gz are already tracked, ordinary gzip
  files at the original five-edge audit path.

The 7,198,761-byte model.npz is a replay dependency, not disposable scratch.
The compiled operator requires its exact frozen SHA256; model.py rebuilding
arrays is not a substitute for preserving those bytes. The independent algebra
probe has separately reconstructed every cached array from the original pinned
caps/orbits JSONs. Likewise, the 3,416,699-byte old warm vector and the
5,617,918-byte new trial vector are necessary to replay the published numerical
comparison. No pickle was deserialized during this publication review.

A new checkout must restore archived bytes before existing custody/checker
commands. Use the established archive restore procedure (including artifacts
when required by broader project checks), then the cone/reuse replays. Repeated
benchmark or solver runs are not required to verify the saved numerical trial.

STATUS.md and the Kempe guide currently match the reused frozen routing input
hashes. Preserve their current dirty bytes before publication edits; later
explicitly authorized routing drift must be checked against that snapshot.
Do not edit the sealed BASE/OUTPUTS files to conceal routing updates.

## Local-path portability findings

1. **Saved trial warm path.** The sealed trial input.json records an absolute
   `/home/ray/developer/ai/math/.../runs/all-cu-pdlp/vectors.npz` path, and the
   sealed review/check_trial.py uses `Path(input['warm'])` directly. An exported
   checkout would otherwise read the original workspace or fail when it is
   absent. Preserve these sealed bytes. Add a publication-level portable replay
   that resolves this known recorded warm path to the exported repository path
   and verifies the same recorded SHA256, and document that adapter explicitly.
2. **GPU discovery wrapper.** opt/gpy has a session scratchpad default for
   CUOPT_VENV. It is historical discovery tooling, not a dependency of CPU
   template/operator/trial replay. GPU exploration requires a caller-selected
   CUOPT_VENV built with the pinned versions documented in that wrapper.
3. **Native binaries.** The operator builds from kernels.cpp with local g++ and
   a source/compiler/flags keyed cache. Local shared libraries and bytecode are
   ignored/transient and should not be staged. The CPU module requires NumPy;
   checker/LinearOperator comparisons use SciPy through opt/py's pinned uv
   environment. No scratchpad native library is needed.

These are publication/replay issues, not mathematical scope changes or reasons
to alter existing evidence. The portable replay is now implemented in [../verify.py](../verify.py).
Its default stdlib custody/archive/seal check and --numerical --controls both
passed in the live checkout. The latter independently recomputes all saved
trial metrics and the coefficientwise majorant/diagonal bounds without
importing the sealed absolute-path checker, running a solver, or compiling a
native library. It resolves its repository root from its own file location,
works without .git, rejects unexpected recorded warm paths, and always reads
the accepted warm file from the current checkout. No output files are written
by default. An altered-seal SHA negative control is rejected in memory.

Replay after restoring archived bytes:

```sh
python3 -B audits/2026-10-21-w7-publish-d5b8a86/verify.py --controls
audits/2026-10-20-w7-count-opt-d5b8a86/py -B audits/2026-10-21-w7-publish-d5b8a86/verify.py --numerical --controls
```

The final Git-index export/restore check and commit/push receipts are owned by
the publication coordinator; this dependency review grants no Git mutations.
