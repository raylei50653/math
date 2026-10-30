# Task 3 receipt: named true-source subclass exclusions

2026-10-29. BASE `e1a90fea41702d7c98747716a5960198aecbecb3`.
Canonical source: [source exclusions](../../docs/c5_five_reference_source_exclusion.md).
Proposal preceded the new certificate. Existing dirty work was preserved;
no commit, push, generator expansion, external theorem or 4CT oracle.

Paper closure scope:

- R5-FACIALITY: connected spanning union of actual singleton reference hits
  forces the actual side word to be all exterior and the bounded interior
  to contain no network vertex or edge, including chords.
- F5-NONFACIAL-COVER: a nonfacial actual odd cycle must have at least two
  original cycle edges omitted from the union of all complete singleton
  reference hits. Transition edges supply the two omissions.
- F5-TRIANGLE-LEAF: under full Gamma support, a nonfacial actual odd triangle
  of Q-M cannot be incident directly to a terminal. Exposing and matching
  that terminal force distinct singleton-hit triangle edges and faciality.

Source connectivity and actual nonempty interior derive the two side
values; neither opposite F5-CHAIN9 anchors nor a single-gap side word is
assumed. These proofs do not require minimality, and apply to the required
minimum-odd matching subclass. C1 is preserved, not used to splice regions
from different references. No Lean formalization is claimed.

`verify.py` independently regenerates the old five-reference JSON and
requires byte equality. All complete references, 68 minimum C1 batches,
all ten pair products (including empty statuses), full segments, the
nonminimum nine-cycle source and both three-family controls are retained.
There are 4 source tests and 5 cycle records: 3 nonfacial records (the same
seven-cycle under two different minima plus the nine-cycle), 1 connected
singleton union forcing a facial triangle, zero violations. The only
triangle/terminal record lacks exposing references and is explicitly not
triggered. No full-five plane example is present; zero examples is not the
paper proof of either exclusion.

`cut_audit.py` uses the unchanged old common-cut predicate on all ten
complete even two-leaf families, all complement-component 2/3 phases,
all open two-color strands and all common port-side words. Counting all
colorings modulo color-name permutations is justified by terminal color
multiplicities 3,1,1. Original graph 12: 6 references, 14 phases, 70/70
actions feasible. Original graph 14: 4 references, 8 phases, 40/40 feasible.
Frozen F4: 7 references, 18 phases, 90/90 feasible. Non-disk expanded
pentagram: 5 references, 10 phases, 50/50 rejected. Thus the true-disk
controls all survive and the old non-disk candidate cannot witness a
strict gain. No strict-gain claim, nor general implication in either
direction between the new lemma and the old cut predicate, is made.

The frozen three entry certificates and old source scripts remain
unchanged; the new certificate records source SHA256 values. New source
code lives only in this task's audit directory.

Validation performed:

- New `verify.py --check verification.json`: PASS, including byte-equal
  independent replay of the frozen five-reference certificate and all
  source/cut checks above.
- `git diff --check`: PASS.
- Formal-docs DocGraph: PASS, 98 documents, 386 relations, 12 families.
- Whole-worktree DocGraph: FAIL, 72 duplicate-ID errors from retained
  audit/scratch source copies (98 documents, 371 relations, 12 families).
  No retained copies were deleted.
- `scripts/check_docs.py`: FAIL, two errors in concurrent work outside
  this task: missing no-hub-bipyramid verification JSON, and
  `docs/c5_kempe_blocked_realizability.md` not directly indexed by STATUS.
  It scanned 793 Markdown files / 10570 local links; no error was reported
  for this task's source/evidence links. These are the observed results,
  not a claim that concurrent work is frozen or complete.

Updated: new canonical report/evidence, immediate source-page follow-up
links, relevant Kempe/4CT guide paragraphs, parity task entry, STATUS index.
Reviewed-unchanged: P3 shared-cut source (its general multi-reference
existence obligation is still OPEN), HANDOFF and README (no research-line
or active-status change). Propagation stops at the direct parent/topic
routing: no general existence theorem is closed or superseded.

Remaining OPEN: full five-reference blocking outside the two named source
subclasses; forcing arbitrary sources into an excluded subclass; strict
gain or redundancy relative to old cuts; E932, 4CT and P4 extension.
