# Verification and evidence boundary

2026-10-18; frozen BASE `9f1fe84f73aabfa87a33d28754633bae6bf0b707`.
All commands below are run from the repository root.

## Paper review

- [A's signed contextual replacement](A/ANALYSIS.md) was independently reviewed
  by B in [REVIEW-A](B/REVIEW-A.md). The root separately reconstructed the
  catalogue result using coordinate combinations and sets of projected tuples.
- [B's arbitrary-boundary response lemmas](B/PROOF.md) were independently reviewed
  by C in [REVIEW-B](C/REVIEW-B.md).
- [C's affine repair and rank lemmas](C/PROOF.md) were independently reviewed by A
  in [REVIEW-C](A/REVIEW-C.md), including a separate execution of the graph controls.
- Root read all three proofs and integrated their actual scopes in [REPORT](REPORT.md).

Two review corrections were incorporated before final sealing: exactly two
**complete complement cycles**, both odd, are needed for universal connectedness;
two odd cycles plus other even cycles do not suffice. Context response for the
joint predicate can switch 101 to 110, so it preserves literal mark identities
and the target predicate, not necessarily all individual membership bits.
The arbitrary-many-odd-cycles control is not asserted to be a joint minimizer.

## Read-only replay

```sh
python3 -B audits/2026-10-18-abstraction-bottleneck-9f1fe84/check.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-18-abstraction-bottleneck-9f1fe84/check.py
```

Both passed. The root checker verifies all 19 frozen inputs against both their
SHA-256 and their exact Git objects at BASE, reconstructs the four-query
certificate independently, executes A/B/C, compares B/C to saved complete
control outputs, and rejects a deliberately corrupted A certificate in an
isolated temporary directory. It never edits the authoritative certificate.
When OUTPUTS.sha256 is present it also verifies the sealed outputs.

Direct entry points, all replayed by the root checker:

```sh
python3 -B audits/2026-10-18-abstraction-bottleneck-9f1fe84/A/check_signed_interface.py
python3 -B audits/2026-10-18-abstraction-bottleneck-9f1fe84/B/check_interface.py
python3 -B audits/2026-10-18-abstraction-bottleneck-9f1fe84/C/check.py
```

| Scope | Actual result |
| --- | --- |
| A catalogue | 132 distinct masks; all 3×1024 observation scopes; 528 countermodels for at most three queries; minimum four-query counts 5/2/1; common 64-mask abstract cylinder disjoint from K |
| B graph controls | Four decompositions on K4, triangular prism and Petersen; complete matching reconstruction and marked optima 0/0/0/2; parity, pairing, closed-odd-count, zero-length and wrong-direction controls |
| C graph controls | 24 matching/reference pairs and 48 batches; connected 24-vertex sharp rank-two control with all 32 PMs and family minimum oddness four; arbitrary concentration family and odd-reference rejection |
| Corrupted certificate | Changing accepted_query_mask from 512 to 0 is rejected by the actual A checker |
| Frozen inputs | 19 exact matches to BASE; frozen bytes never replaced by current routing documents |

The original K≤5 enumeration and its witness enumeration were not rerun.
The finite controls do not verify arbitrary-size topology or supply an original
minimum source. General conclusions rely on the paper arguments just reviewed.

## Documentation and scope

Executed successfully:

```sh
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
git diff --check
```

Documentation result: 696 Markdown files, 9160 local links, anchors, report
index, handoff and guide progress checks passed. Formal-doc DocGraph result:
97 documents, 383 relations, 12 families, zero errors and zero notes.
Whole-tree DocGraph was not rerun; formal-doc success is not a whole-tree result.
New audit Markdown link targets were also checked separately.

No Lean source or dependency changed. No lake build was run and no new paper
theorem is claimed Lean-formalized. No 4CT or new external theorem is used in
the new lemmas; the multipole paper linked in REPORT is context, not a proof input.

Updated: this audit, the Kempe guide's current abstraction/next obligation, and
the STATUS index. Reviewed unchanged: README/HANDOFF research lines and tags,
old sealed mathematics, old two-cycle repair obligation and all parent OPEN
claims. Propagation stops at L1. No commit or push was performed.
