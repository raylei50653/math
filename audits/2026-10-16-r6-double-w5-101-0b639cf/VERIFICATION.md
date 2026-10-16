# Verification and custody

2026-10-16. BASE `0b639cf5ffd57e8e394add4e0b56cd60cc2ce38c`.
The arbitrary-size theorem is [PROOF.md](PROOF.md), independently rebuilt
in [REVIEW.md](REVIEW.md). The earlier five-cut proof was independently
reviewed first, without using its old REVIEW; see [REVIEW-PRIOR.md](REVIEW-PRIOR.md).
These are paper proofs, not new Lean theorems. The last contradiction
does not depend on the optional inherited h=3 finite collar classification.

## Executed replay and negative controls

[verification-runs.json](verification-runs.json) and
[verification-final-runs.json](verification-final-runs.json) preserve exact
commands, environments, exit codes and timings. Each command has separate
stdout/stderr files under logs; no earlier frozen certificate was rewritten.

| Check | Observed result |
| --- | --- |
| New sector/W5 checker, normal and `PYTHONHASHSEED=17` | PASS; identical output, all 32 port fibres including 21 empty fibres retained |
| New radius-two checker, normal and seed 17 | PASS; identical output, literal 11V/25E/15F disk, five complete facial-ear stars, 12V/30E/20F cap sphere |
| Corrupt empty matching fibre | Rejected, exit 1 |
| Promote sector certificate to source exclusion | Rejected, exit 1 |
| Remove a recorded radius-two face | Rejected, exit 1 |
| Promote radius-two control to a source realization | Rejected, exit 1 |
| Recreate either existing certificate with `--write` | Rejected, exit 1; exclusive creation retained |
| Previous chorded-five certificate, normal and seed 17 | PASS |
| Original double-low return checker | PASS |
| Previous curvature, common-111 saturation, local W5 fibre checkers | PASS; saturation used `uv run --with-requirements requirements.txt` |
| `lake build` | PASS, exit 0; existing linter warnings retained in logs |
| `python3 -B scripts/check_docs.py` | PASS: 688 Markdown files, 9040 local links |
| Scoped `tools/docgraph --include 'docs/**/*.md' check` | PASS: 97 documents, 383 relations, zero errors |
| `git diff --check` | PASS |

The local topology calibration does not prove that an arbitrary source
contains the radius-two disk. That conclusion uses the complete degree-five
links and source faciality in PROOF section 9.2. Its face IDs and rotations
are retained in full. The local matching checker enumerates all half-edge
port assignments and every internal matching lift, not marginals. Neither
checker supplies a minimum source: source numerical coverage is
**not triggered**, and both explicitly reject source promotion.

No original full colouring relation or r lift was regenerated or discarded.
The original full-fibre return theorem and the actual source geometry are
paper dependencies, separately reviewed and frozen at BASE.

## Whole-tree failure and historical guards

Whole-tree DocGraph **FAILS** with 70 duplicate-ID errors. We also ran it
on an exact temporary tree of all 3489 tracked Markdown files at BASE;
that tree already has the same 70 error kinds and logical IDs. See
[docgraph-baseline-comparison.json](docgraph-baseline-comparison.json).
The messages are not byte-identical: the live tree also contains retained
ignored scratch/history copies and this audit's verbatim frozen snapshots.
No old snapshot was deleted or edited to manufacture PASS. Formal-doc
success is not reported as whole-tree success.

The previous chorded-five verification already records a JOINT-ZERO
live-routing STATUS hash failure. This round does not rerun or reinterpret
that historical guard as current routing authority. Instead it replays the
needed mathematical calibration checkers and independently compares every
one of the three old audits' 424 files and their membership against this
task's exact BASE. The original logs and seals remain unchanged.

## Custody, seal and propagation

[BASE.json](BASE.json) records the original clean HEAD, the 424 old audit
file hashes, and verbatim copies of 21 authority/routing inputs. The new
[check_bundle.py](check_bundle.py) checks old file membership and bytes,
frozen input bytes, allowed routing edits, new Python syntax, local links
and the [MANIFEST.json](MANIFEST.json) seal. Its PASS is a delivery/custody
check, not a mathematical proof verifier. The final seal excludes only
itself and Python cache files; seal replay is read-only.

Normal and seed-17 certificate logs are compared byte for byte. New source
files are AST parsed; frozen Python and certificate bytes are not patched.
The build ran once, with no Lean source change and no parallel build.
All warnings were already in existing Lean files; no new formalization
or axiom claim follows from this build.

Propagation reviewed the current Kempe guide, STATUS direct index, C4
parent and State active-route pointer. They now state that 101 ordinary
failure only retains the nonwheel seven-cut class. Earlier audit reports
and publication histories retain their dated claims. README and HANDOFF
need no change because the research lines and user workflow are unchanged.
The other C8 use of the words “double W5” describes a different chorded
peeling configuration and is not changed by this 101 theorem.

The numerical bounds, completed-source return cost k+5, 110 residuals,
even-complement positivity, full319 and the general theorem are unchanged.
No commit or push was requested or performed.

## Replay commands

From the repository root:

```sh
python3 -B audits/2026-10-16-r6-double-w5-101-0b639cf/check.py --check audits/2026-10-16-r6-double-w5-101-0b639cf/certificate.json
PYTHONHASHSEED=17 python3 -B audits/2026-10-16-r6-double-w5-101-0b639cf/check.py --check audits/2026-10-16-r6-double-w5-101-0b639cf/certificate.json
python3 -B audits/2026-10-16-r6-double-w5-101-0b639cf/check_radius2.py --check audits/2026-10-16-r6-double-w5-101-0b639cf/certificate-radius2.json
PYTHONHASHSEED=17 python3 -B audits/2026-10-16-r6-double-w5-101-0b639cf/check_radius2.py --check audits/2026-10-16-r6-double-w5-101-0b639cf/certificate-radius2.json
python3 -B audits/2026-10-16-r6-double-w5-101-0b639cf/check_bundle.py
```
