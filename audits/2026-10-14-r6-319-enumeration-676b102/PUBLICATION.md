# Audit-only publication

2026-10-14. User explicitly requested commit + push of this audit only.
Publication parent: `3953c85e334b96533e44652df065640f5463715a`.

The immutable [research report](REPORT.md), [coverage proof](PROOF.md),
[verification record](VERIFICATION.md), original manifests, all full-run
certificates and historical failed/negative controls retain their bytes.
Their statements that the research run had not committed/pushed describe
the original delivery; this note records the later publication step.

The scope is the named global-minimum-source branch with original x,y,b
degree four and r degree six: k23 and k24 are excluded, hence k>=25.
General K<=22 is unchanged; unbounded319 and the other source branches stay
OPEN. This is finite computation with the recorded source/generator trust,
not a new Lean theorem.

## Restore and replay

Frozen files, files at least1MB and historical whitespace inputs from this
audit alone are stored through the existing archive. The selected paths and
new blobs are listed in [publication-archive.json](publication-archive.json).
The original live files are unchanged. From the repository root, restore
archived inputs before following the original replay instructions:

```sh
python3 tools/audit_archive.py restore
cd audits/2026-10-14-r6-319-enumeration-676b102
python3 -B src/controls.py
python3 -B validation/verify_run_parallel.py 29
python3 -B validation/verify_run_parallel.py 30
```

The publication validation reconstructs all536 sealed artifacts from the
Git index and indexed archive blobs into a fresh temporary directory,
verifies all original sizes/hashes and replays controls and pilot witnesses
there. Its receipt is [publication-validation.json](publication-validation.json).
The normal and seed17 complete production replays were already successful
in the research run and are retained; full generation is not repeated for
this unchanged-byte publication.

Publication checks also include normal/seed17 local controls, the complete
pilot witness replay, generated-artifact policy, whitespace and document
navigation. `lake build` completed8832 jobs with existing linter warnings;
it does not formalize the new enumeration.

Only this audit, its archive blobs and the necessary archive index/ignore
entries are staged. README, HANDOFF, STATUS and the source/guide summaries
were reviewed and left unchanged under the requested audit-only publication
scope; this commit does not perform a separate shared-document adoption.
