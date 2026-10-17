# Verification and adoption

2026-10-16, BASE `f1faf743833c51ddc5efbe9e0f390b87b9f2311d`.
The original [BASE](BASE.json) seals 21 inputs; [additional inputs](ADDITIONAL_INPUTS.json)
seal three further proofs at the identical Git BASE. The original receipt was
not rewritten. Workers wrote only their exclusive A, B, C directories;
root wrote integration files and three directly affected routing documents.

## Adopted paper results

* A: two complete-source Kempe bijections, actual all-distinct J colourings
  in both z=v and z=w sectors, `N=24(n0+n4)`, and
  `W010=W001=2(n0+n4)>0`. At least one defined H_p/H_q has an actual
  nonempty z lift. Root, B and C independently reviewed the full-colouring
  inverse, the Jordan argument, the 24 colour frames and the factor12.
* B: the exact pentagon port interface and the protected f-containing
  exterior arc of a shortest eligible ordinary101 switch. Root, A and C
  accepted the simple alternating shortcut and its precise limitation.
* C: the induced-C5 source-sector classification, including the original
  degree-six p/q centre exceptions, and the actual chorded-cut ear/core
  reduction. Root and A reviewed the exceptions. The initial marked-ear
  wording was corrected to assert existence, retaining possible other ears.
  The separately frozen exact common-neighbour identities then prove that
  every cyclic five-cut crosses at most one marked edge; root reviewed this
  argument and replayed its independent finite deductions.

Reviews are retained in [A/CROSS_REVIEW](A/CROSS_REVIEW.md),
[B/REVIEW-A](B/REVIEW-A.md) and [C/REVIEW_A_B](C/REVIEW_A_B.md).
The additional input is used by [C/MARKED_CUTS](C/MARKED_CUTS.md), without
changing the earlier worker seal or claiming a new actual source control.

## Read-only replays and rejection controls

All commands below passed in normal and `PYTHONHASHSEED=17` environments;
B also uses `--seed 17` to vary enumeration order while comparing the entire
canonical certificate. Root separately replayed each active certificate.

```sh
python3 -B audits/2026-10-16-r6-319-continuation-f1faf74/A/check.py --check
python3 -B audits/2026-10-16-r6-319-continuation-f1faf74/B/verify.py --check audits/2026-10-16-r6-319-continuation-f1faf74/B/certificate.json
python3 -B audits/2026-10-16-r6-319-continuation-f1faf74/C/check.py --certificate audits/2026-10-16-r6-319-continuation-f1faf74/C/certificate-v2.json
python3 -B audits/2026-10-16-r6-319-continuation-f1faf74/C/check_marked_cuts.py
python3 -B audits/2026-10-16-r6-319-continuation-f1faf74/integration/independent_interface.py --check audits/2026-10-16-r6-319-continuation-f1faf74/integration/independent-interface.json
```

| Evidence | Coverage and actual outcome |
| --- | --- |
| A | 16,384 zero-inclusive seven-pin positions, full r fibres, exact forward/reverse component options; no-all-distinct relaxation leaves six rows with support266 |
| B | 32 port fibres, 11 nonempty and 21 empty; 30 local Tait rows; full J/PM fibres on four fixed graphs; 186 one-port and 193 three-port defect cases |
| C | 642 cycle records, 234 cyclic five-cuts, 186 chorded ear/core cases on four embedded controls; both literal p/q endpoint exceptions retained |
| C marked cuts | five unbounded degree classes, ten oriented core cases; every optional j/opposite endpoint kept; finite five-vertex graph deductions agree |
| Root independent arithmetic | direct original R rule over all16,384 positions; 1,440 proper positions, 624 universally admissible and 288 proper empty r fibres; 192 labelled forward/reverse cases |

These are finite calibration counts, not actual full source-colouring counts.
Every control's complete-source status is **not triggered**. The arbitrary-size
authority is the paper argument under the original source hypotheses.

Damaged complete r fibres, omitted empty port fibres, wrong shortcut edges,
unprotected exterior arcs, invented empty matching lifts, wrong four-cut
cores, erased endpoint exceptions, and erased optional-j chords were rejected.
Exclusive creation rejected attempts to overwrite active certificates.
The root independent certificate also rejected a changed case count and
an overwrite attempt. Full outcomes and stdout/stderr remain in
[A receipts](A/logs/receipts.json), [B verification](B/VERIFICATION.json),
[C verification](C/VERIFICATION.json),
[C marked verification](C/MARKED_CUTS_VERIFICATION.json), and
[root initial verification](integration/root-initial-verification.json).

Root's cross-replays are in [root-replays](integration/root-replays.json),
with the corrected engineering run in [final-checks](integration/final-checks.json).
The first DocGraph call incorrectly used the module entrypoint and failed
to import docgraph; the supported directory entrypoint passed. The initial
six-milestone guide check failed, then passed after removing its oldest
milestone row. Both failures are retained. The initial freeze stopped on a
nonexistent checker filename; copied bytes were compared to BASE before
the remaining correct inputs were added. No failed result is counted as PASS.

## Engineering and custody

`lake build` completed successfully, 8,832 jobs, with existing linter warnings
in AttachmentOrder and SymRelabel. There is no new Lean source or theorem.
`python3 scripts/check_docs.py` passed: 691 Markdown files and 9,089 local
links. Formal-doc scope passed with the actual entrypoint:

```sh
uv run --with networkx==3.5 python tools/docgraph --include 'docs/**/*.md' check
```

It checked 97 documents, 383 relations and 12 families, with zero errors.
Whole-tree DocGraph was not rerun; formal-doc success makes no claim about
historical/frozen duplicate metadata. `git diff --check` passed for the
tracked routing edits. New authored Markdown/Python whitespace and complete
frozen-input custody are checked separately during final sealing.

The bundle [manifest](MANIFEST.json) seals the complete new audit and the
three routing-file hashes. Its read-only replay is:

```sh
python3 -B audits/2026-10-16-r6-319-continuation-f1faf74/integration/check_bundle.py
```

This checker requires HEAD still equal to the research BASE, verifies all24
frozen inputs against their Git objects, permits only the three declared
routing files to differ from their old source snapshots, and checks every
sealed audit file. It is a research-workspace replay, not a publication
checker. No commit, push, general source enumeration or external theorem
adoption occurred.

The target `W110+W101>0`, `omega_e=0`, complete319 exclusion and strict
completed-source descent remain **OPEN**. The final graph still has k+5
vertices. None of the accepted tests is labelled a proof of these endpoints.
