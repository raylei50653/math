# 941 publication: independent source-scope and inventory review

2026-10-23. Read-only review of the 32 new research `REPORT.md` files, the
existing changes to `docs/c5_kempe_guide.md` and `docs/STATUS.md`, and the latest
round-seven `PROOF.md`. This publication note is new; the reviewed research
audits and their frozen inputs were not modified by the reviewer.

## Consolidated result

The current guide and STATUS agree with the round-seven report and proof:

- The complete joint-star certificate excludes all 154 entrances for the
  empty-M2, T6, seven-resource cases containing two N points or one N and one K.
  The remaining case is d != U, K0 + K2, with a sealed K8 collar.
- All 21 ordered caps retain 5754 complete fibres, including 3003 empty fibres,
  and 4236 complete seven-point lifts. The 72 safe candidates cover 1041 fibres;
  the four cap classes retain 30 / 85 / 116 / 108 possible accepted fibres per
  cap. The full K8 replacement remains OPEN.
- The bounds remain eight exterior private points for the empty branch and
  all 11 necessary types, nine for nonempty M2, and ten for nonsingleton M2.
  The empty T8 branch has at least ten. The common k >= 23 bound is unchanged.

The relevant current authority is
`audits/2026-10-23-941-types-wrong-side-round7-6b09cd4/REPORT.md`, lines 9-29
and 42-44, and its `PROOF.md`, sections 1-5. This review checked document
consistency and the stated proof interface; it is not a new formal theorem or
an independent execution of all mathematical checkers.

## Same-source and same-H requirements

The latest proof preserves one original G/F, its rotation and attachments,
ordered B14 contacts, the literal phi/psi frame, complete original components,
empty fibres, and full lifts. The complete joint-star join adds every spoke and
link edge to the same accumulating graph and retains previously completed
stars. It does not combine independently feasible marginal stars.

For each actual complete 01232 witness covered by a safe candidate, the witness
selects one candidate once and thereby fixes one H. Every complete coloring in
each of 01021, 01202, and 01212 of that same H pulls back through the fixed
quotient map to the same original exterior and a full lift of the original cap.
Different rejected rows do not receive different candidates or palettes. The
size decrease of 7 / 9 / 10 is the completed graph decrease, not an uncharged
local deletion. See round-seven `PROOF.md`, section 4, especially lines 135-149.

## Coverage and OPEN boundaries

The 154-entry exclusion has a source-coverage argument: complete R-neighbor
closure and the full allowed-original-neighbor envelope put every source in
the stated seven-resource domain into the joint cycle catalogs. Arbitrarily
many spectator points outside Z cannot supply missing R-star neighbors.
Unknown exterior K/U stars remain open. Independent DFS and cycle-catalog
joins supply the finite zero result; the source-envelope completeness is
carried by the paper argument. A fixed control PASS alone is not a source
exclusion.

This coverage is scoped to the original Gamma8 / exactly two interior points,
11 necessary types, empty M2, T6, and seven-resource domain. It does not cover
|Z| >= 8 or prove an actual source exists. The finite controls are
`triggered and holds`; an actual complete source instance remains
`not triggered`.

Nonempty residual K8 fibres do not establish source realizability, do not show
that no further safe candidate exists, and do not settle their compatibility
with the same actual exterior. Full K8 replacement, the new eight-resource
nonempty branch, the 11 complete types, more interior points, longer Gamma,
general wrong-side, the initial eight pairings, 941/W7/J1/J2, general smaller
bad graphs, and matching remain OPEN. No new Lean theorem is claimed.

## Historical status and routing cleanup

The research reports are immutable records of their writing-time state. Their
older bounds, superseded next obligations, and statements such as
`未commit/push` describe that time; publication should explain this convention
without rewriting frozen research bytes.

Two routing cleanups were recommended to the publisher:

- The guide's round-three milestone (reviewed at line 23) gives the historical
  nonempty-eight / empty-seven bounds. Mark these as that round's bounds and
  say later rounds raise them to nine / eight, so they cannot be read as the
  current stopping point.
- The guide's publication link (reviewed at line 28) names only the earlier
  five-round publication. Add the new 941 publication receipt as the current
  link and retain the earlier receipt as history.

The reviewer checked local Markdown links in all 32 new `REPORT.md` files plus
the guide and STATUS: **34 files, zero missing local targets**. Anchors were not
independently validated by that existence check.

## Independent publication inventory check

`BASE.json` was compared against every regular on-disk file in its 32 listed
research directories and against `git ls-files --others --exclude-standard` in
those same directories. The three path sets agree exactly:

- 32 original research directories;
- 1790 original files, totaling 206002019 bytes;
- no extra, missing, or omitted untracked original file;
- every original file's bytes and SHA256 match its frozen BASE entry.

The repository generated-artifact check uses an inclusive 1000000-byte
threshold for JSON/JSONL/NDJSON/JSON5/BIN files. The original publication scope
contains exactly **48 JSON files at or above that threshold**, totaling
142648116 bytes. None had an existing policy exception at review time. They
need 48 exact `kind: frozen` entries with the frozen size and SHA256 and a
nonempty reason if all original evidence is to remain tracked. The reviewer
did not edit the exception policy or Git state. Final staged-index policy
validation remains a publisher check after those entries are added.

## Final policy and routing recheck

A fresh read after the publisher's policy update supersedes the earlier
registration-status statement above: **all 48 required frozen entries are now
present** in `tools/generated_artifact_exceptions.json`.

The reviewer compared the current policy with `git show HEAD:` of the same
path. All 119 original exception records remain semantically identical,
including every original field value; non-`files` top-level policy fields are
also unchanged. Exactly 48 paths were added, giving 167 exceptions in total.
The added paths are exactly the BASE inventory's 48 generated JSON files at or
above 1000000 bytes, with no missing or extra path. Every new record has
`kind: frozen`, a nonempty reason, and exactly the BASE byte count and SHA256.
Fresh hashing of those on-disk files also agrees. The separate
`review/artifact-exceptions.json` receipt has 48 unique added paths and exactly
the same path/bytes/SHA256 triples and 119-to-167 counts. No policy or Git state
was mutated by the reviewer.

Both guide cleanup recommendations are applied: the round-three milestone now
labels its eight/seven bounds as historical and records the later nine/eight
bounds; the current publication link points to
`docs/history/2026-10-23-941-gamma8-publish.md` while retaining the prior
three-line five-round publication as history. The exact original 34-file
local-link existence check was repeated after these changes and again found
zero missing targets. The current source-scope and OPEN-boundary wording remains
consistent with the round-seven report/proof.

This final recheck confirms policy contents and document routing. Validation
against the final staged Git index and isolated staged-source replay remains
the publisher's subsequent check.
