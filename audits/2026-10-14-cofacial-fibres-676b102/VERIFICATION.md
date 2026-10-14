# Verification and retained evidence

2026-10-14. BASE is `676b1024715f24a0d969fba90baab21b756406e2`.
The initial canonical worktree was clean at this BASE; a live read of remote
main returned that same commit. Research used the detached worktree named in
[INPUTS.json](INPUTS.json), then copied only the new audit and five connected
documentation files to the canonical workspace. No commit or push was made.

## Mathematical review and finite scope

- [r6 proof](r6/PROOF.md): independent audit of the original induced C5,
  nonedges, two separate quotients, `k-3` cap budget, and the fixed ten rows.
- [low-p proof](pq/PROOF.md): same-source two-face construction, simultaneous
  quotient, `k-4` cap budget, exact generic full fibre, and literal alias exclusion.
- [independent review](review/REVIEW.md) and [second peer review](r6/PQ_PEER_REVIEW.md):
  original face interiors and retained edges, no-loop proof, full-colouring
  pullback, all p lifts, and reflected scope checked independently.
- [r6 final certificate](r6/r6-final.json): all 1024 boundary assignments,
  240 proper assignments, ten global-S4 rows, and 132 frozen catalogue masks.
- [pq final certificate](pq/certificate-final.json): all 16384 seven-pin assignments,
  1764 proper labelled face rows, 74 canonical rows, and all original cap lifts.
  The quotient slice has 324 labelled rows and 1152 complete lifts; only the
  24 common global renamings of ABABCBC satisfy universal target failure.
- [independent alias check](review/alias-local.json): 108 labelled rows,
  384 complete lifts, 288 palette-changing lifts; every row has such a lift.
  [Independent generic check](review/double-quotient.json) reproduces the
  quotient slice and its exact 24 survivors from original edges.

Finite checks verify the displayed colour arithmetic. Planarity, original
contact identities and relative minimum-source colourability are the paper
arguments; no finite output is treated as a realization of the actual source.
The exploratory C6 deletion in review/ is retained with its limitations;
the adopted proof retains zt and uses the two actual faces directly.

## Read-only replay

From repository root:

```sh
python3 -B audits/2026-10-14-cofacial-fibres-676b102/r6/check_r6.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-14-cofacial-fibres-676b102/r6/check_r6.py --check
python3 -B audits/2026-10-14-cofacial-fibres-676b102/pq/check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-14-cofacial-fibres-676b102/pq/check.py --check --seed 17
python3 -B audits/2026-10-14-cofacial-fibres-676b102/review/check_alias_local.py
python3 -B audits/2026-10-14-cofacial-fibres-676b102/review/check_double_quotient.py
python3 -B audits/2026-10-14-c4-c5-recursion-fdd3e22/fibre/r6_counts/check_counts.py --check
```

The r6 [final receipts](r6/logs/final/receipts.json) retain default and seed17
PASS, corrupted-certificate rejection and rejected overwrite with unchanged
certificate SHA256. The earlier certificate, its exact historical checker,
and its receipts remain present. The pq directory retains its corresponding
normal, seed17 and negative-control outputs. Consolidated checks and exit
codes are recorded in [logs/receipts.json](logs/receipts.json).

Actual consolidated results in the canonical workspace:

| Check | Result |
| --- | --- |
| r6 default and seed17; pq default and seed17 | PASS |
| Independent alias and generic original-edge replays | PASS; both JSON outputs equal their saved certificates |
| Historical r6 integer-count checker | PASS for its original three necessary models |
| Frozen inputs / historical audit custody | 16 inputs, zero drift; both old audit trees unchanged from BASE |
| `scripts/check_docs.py` | PASS: 685 Markdown files, 8926 local links |
| Formal docs DocGraph | PASS: 97 documents, 381 relations, 12 families, zero errors |
| Whole-tree DocGraph | FAIL: 70 duplicate-ID errors, same 70 IDs as the pre-change BASE check; no new error IDs |
| New non-frozen audit Markdown links | 58 local targets, all exist |
| `git diff --check` | PASS |

The whole-tree comparison includes the additional frozen copies without
removing historical documents. Its unchanged failure is not reported as
a PASS and does not replace the separate formal-doc result.

## Custody and documentation scope

The 16 frozen inputs must retain their INPUTS.json hashes. The historical
transfer, count certificate, old audit reports and manifests remain byte-for-byte
unchanged in the canonical tree. The source-strengthening layer is separate.
The final MANIFEST.json inventories this new audit, excluding itself.

Connected documentation: C4 parent, Kempe guide, STATUS, no4ct handoff and
the C4 row in research synthesis. HANDOFF and README need no changes because
research-line routing did not change. General `K<=22=K<=5=K132`, `k>=23`,
high-p/q conditional `k>=28`, and all other T/T0 branches retain their scope.

Formal-document checks and whole-tree DocGraph are reported separately in
the consolidated receipts. Historical duplicate IDs must remain visible;
no evidence is removed to obtain PASS. No full Lean build, new Lean theorem,
plantri run or external exhaustive enumeration is claimed.
