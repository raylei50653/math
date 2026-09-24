# 2026-09-24: adjacent two-spoke (2,1), separate-component obstruction

Scope: S={b0,b1}, q=01012, both singleton forbidden-color orders, C₂ and
C₁ distinct in the long boundary region. The [report](../c5_two_spoke_adjacent_21.md)
proves that neither configuration is planar under the stated minimal-core
and complete-degree hypotheses. T4 and second-row rejection are unnecessary.

The short-side component forbids 2 and sees only {b0,b4}. At z=2 its common
{1,3} odd-cycle palettes yield tethers of colors 0 and 2. A path through
the other component connects z to b4, giving two adjacent hubs and a K5
minor. The full forbidden-color interface F_A(b)={b4} is also derived,
but no component is merged and the completed (3) case is not used.

New fixed-domain checks: 32 support subsets, 240 boundary transports,
3,840 joins, four palette partitions, 480 concrete full-relation rows,
and 48 K5 branch-set certificates retaining named C₂/C₁ contact sets.
The minor samples are incomplete extracted subgraphs, not disk/core
realizability claims. Arbitrary-length extraction is a paper proof.

Trust: paper argument, external degree-list characterization, existing
connected-exterior K4 lemma, Python local checks. No new Lean theorem.
The previous 18-entry (2,1) table loses these two entries only in this
report; the other 16 entries were not classified here. Next: S={b1,b2},
whose two z–b4 boundary arcs both see all three q colors. The reflected
S={b2,b3} transfer should also be recorded explicitly in a later update.
General exits, t≤1, the R31 source-minor gap, and K∞=K≤5 remain open.

Executed successfully:

```bash
python3 scripts/c5_two_spoke_adjacent_21.py --check
python3 scripts/c5_degree5_two_spoke_sectors.py --check
lake build
python3 scripts/check_docs.py
git diff --check
```

The sector checker reproduces its historical 18 retained (2,1) / 6 retained
(3) configurations; the new theorem is a subsequent filter, not a rewrite
of that artifact. `lake build` completed all 8,823 jobs with existing
AttachmentOrder/SymRelabel linter warnings. It does not formalize this proof.
Research-turn documentation validation checked 147 Markdown files and
1,934 local links; publication adds the report to README navigation.

Existing R10, K4, three-contact, and five-target certificates were cited,
not rerun. No atlas, graph-catalogue expansion, or fixed-point run was done.
The subsequent publication request authorizes commit and push of the
connected checker, artifact, report, README, handoff, status, and history
bundle. Research checks and the Lean build above are reused; documentation
and diff checks are repeated after the publication edits. The original
sector table, 603 profiles, fixed point, and historical certificates remain
unchanged. Publication SHA and remote equality are verified after pushing.
