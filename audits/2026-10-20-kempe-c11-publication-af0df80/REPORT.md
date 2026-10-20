# Connected J1 C11 and Kempe iteration publication custody

2026-10-20. User explicitly requested current-progress organization, commit and push.
The exclusive [BASE](BASE.json) and [initial status](initial-status.txt) precede
publication edits. The existing unpushed `af0df80` commit is included in delivery.

The scientific results, boundaries and next entry points are summarized in the
[publication record](../../docs/history/2026-10-20-kempe-c11-progress-publish.md).
Original audit reports, frozen inputs, failed exploration and negative controls
retain their bytes and historical no-commit/no-push statements.

[SOURCE_FILES](SOURCE_FILES.json) records all 1,509 non-cache files of the three
new audits before publication work. [Required ignored inputs](required-ignored-inputs.json)
lists the 39 exact source paths hidden by existing ignore rules. Seven generated
JSON files receive exact frozen-byte exceptions in the existing policy; the
threshold and policy checker are unchanged.

Independent normal/seed17 replays, controls and scientific review receipts:

- [C11](review-c11/summary.json)
- [Kempe](review-kempe/summary.json)
- [Project checks](review-project/summary.json)
- [Final staged checks](publication-checks.json)
- [Independent final index review](index-review/summary.json)

After staging or checkout, replay source custody with:

```bash
python3 -B audits/2026-10-20-kempe-c11-publication-af0df80/check_custody.py
```

The checker compares all original source bytes with both worktree and Git index;
it also checks required ignored dependencies and the seven staged policy entries.
Routing-before copies preserve the uncommitted documentation state at this
publication's start. They do not replace the original audits' frozen authority.

Paper source semantics, finite certificates and Lean remain distinct. Only the
named J1 original W5 three-edge branch closes; general J1/J2, bounded state
representation, smaller bad and the main theorem remain OPEN. `lake build` does
not formalize the new arguments. Whole-tree DocGraph retains 72 historical
duplicate-ID errors; only the formal docs scope passes.

Commit/push, clean status, remote equality and CI status are checked live after
publication and are not preclaimed here.
