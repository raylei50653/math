# Verification, independent review and retained custody

2026-10-14. BASE is `676b1024715f24a0d969fba90baab21b756406e2`.
The exclusive detached worktree is recorded in [INPUTS.json](INPUTS.json).
The prior uncommitted cofacial audit is a separately sealed overlay.
Routing files have immutable snapshots; the previous audit is unchanged.

## Mathematical checks

- [Main paper proof](pq/PROOF.md): original proper C5, its bounded side,
  the nonedge r-ell, the two facial arcs sharing z, the independent class
  `{z,r,ell}`, the `k-4<k` comparison budget, and every original cap lift.
- [Independent source review](classification/REVIEW.md): the same geometric
  and full-fibre obligations, the a=5 fan, reflected scope, and degree budget.
- [r6 source geometry](r6/PROOF.md): two explicit proper original C5 cycles
  exclude the specified collar-to-link edges for arbitrary source size.
- The prior ABABCBC and new ABABCAB fibres are separately nonempty on the
  same literal graph. No joint witness satisfying both words is claimed.

The main checker reconstructs 16,384 labelled assignments, 1,764 proper
two-face assignments, 74 common-colour orbits, and all 2,160 labelled cap
lifts. Every proper orbit retains all its lifts, including empty cells.
The triple quotient has 324 labelled rows; its universal-failure survivors
are precisely the 24 global colour renamings of ABABCAB.

Two independent direct-edge checks import no research checker:
[classification checker](classification/check_common_fibre.py) retains all
324 quotient rows and their 1,152 lifts; [integrator check](review/direct_lifts.py)
reconstructs the same slice. The 24 survivor rows have 48 complete lifts.
Adding the original edge mt or ms removes every survivor.

These checks validate fixed local arithmetic. They do not enumerate actual
target sources or certify arbitrary planar embeddings. The arbitrary-size
source exclusion is the paper argument. No new Lean theorem is claimed.

## Read-only commands

Run from repository root:

```sh
python3 -B audits/2026-10-14-lowpq-source-676b102/pq/check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-14-lowpq-source-676b102/pq/check.py --check
python3 -B audits/2026-10-14-lowpq-source-676b102/classification/check_common_fibre.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-14-lowpq-source-676b102/classification/check_common_fibre.py --check
python3 -B audits/2026-10-14-lowpq-source-676b102/review/direct_lifts.py
python3 -B audits/2026-10-14-lowpq-source-676b102/r6/check_inputs.py
python3 -B audits/2026-10-14-cofacial-fibres-676b102/r6/check_r6.py --check
python3 -B audits/2026-10-14-cofacial-fibres-676b102/pq/check.py --check
python3 -B audits/2026-10-14-c4-c5-recursion-fdd3e22/fibre/r6_counts/check_counts.py --check
```

The r6 checker is custody-only. The historical count checker replays the
three old necessary models; it does not solve a new integer model.
Negative controls and exclusive-create tests are recorded in the respective
[pq receipts](pq/receipts.json),
[classification receipts](classification/receipts.json), and
[r6 receipts](r6/logs/receipts.json). Failed generation and weaker explored
arguments remain in the audit; none is silently overwritten as a success.

## Consolidated validation and publication

The final canonical-workspace checks are retained in `logs/`; their commands,
exit codes, frozen custody and documentation results are recorded in
`logs/final-receipts.json`. Existing Lean compilation is recorded separately
in [lake-build.json](logs/lake-build.json): `lake build` passed; this establishes
only the existing Lean library's build, not formalization of the new proof.

The pre-integration whole-tree DocGraph check is retained in
[baseline stdout](logs/docgraph-before.stdout) and
[baseline stderr](logs/docgraph-before.stderr). It failed on 70 historical
duplicate-ID errors. Formal docs and the whole tree are checked separately;
no historical evidence is removed to obtain a pass.

Actual consolidated results:

| Check | Result |
| --- | --- |
| Main and independent fibre replays, normal and seed17 | PASS |
| Removed-full-lift negative controls | Rejected as expected |
| r6 input seal, normal/seed17 and corrupted-seal control | PASS / rejected as expected; custody only |
| Frozen authority and historical audit custody | 105 files checked, zero drift; historical tracked audits unchanged |
| New non-frozen audit Markdown targets | 73 targets, all exist |
| Existing `lake build` | PASS; no new theorem |
| `scripts/check_docs.py` | PASS: 686 Markdown files, 8,945 local links |
| Formal docs DocGraph | PASS: 97 documents, 382 relations, zero errors |
| Whole-tree DocGraph | FAIL: the same 70 historical duplicate-ID error keys; zero new keys |
| `git diff --check` | PASS |
| Staged whitespace and generated-artifact policy | PASS |

The [whole-tree comparison](logs/docgraph-comparison.json) records the exact
error-key set. Additional frozen evidence is retained; this unchanged
historical failure is not reported as a whole-tree pass.

Only the two connected audit bundles, five affected current documentation
files and the [publication record](../../docs/history/2026-10-14-lowpq-source-publish.md)
are in scope for this authorized commit/push. README and HANDOFF routing
were reviewed unchanged. General T/T0 extension, K-infinity, the 319 source,
and p5a>=6 remain OPEN. The manifest inventories the final new audit,
excluding itself. Live Git determines publication status.
