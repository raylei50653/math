# Exact finite interface replay

The [paper](../paper/REPORT.md) proves the capacity-assignment implication.
`matrix.py` implements it with literal original root-color labels. Every free
binary assignment is checked; an independent checker instead enumerates row
subsets and compares exact feasible-matrix counts. Necessary cut inequalities
are checked by direct counting; no unproved completeness of those cuts is used.

`BASE.json` freezes the finalized, full-fibre original graph control. The
checker reconstructs actual W sets and safe cells from its original edges,
checks each against full original tuples, and compares matrix conclusions
with the actual same-original-H joint in all ten literal rows. Original full
lifts remain in the frozen input, with SHA and exact JSON pointers in outputs.

Eighty-one degree-compatible abstract incidence profiles calibrate the small
integer matrix; they are not graphs. A separate two-by-three control has one
certified accepted cell for each piece and a feasible matrix, preventing the
mistake that separate witnesses force a common joint. A three-by-three control
with a whole safe row has no matrix by surplus incidence and a violated cut,
even without directly overlapping safe cells.

After T0/T1, remaining spoke profiles have 8,9 or6 cells. Thus their maximum is
nine cells and 512 assignments, irrespective of original piece size. All
full-target source statuses remain `not triggered`. A feasible matrix is only
an abstract capacity allocation and supplies no actual original fibre.

```bash
python3 -B audits/2026-10-13-n2-double-long-joint/joint/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-n2-double-long-joint/joint/checker.py --check
```

The deterministic artifact is 33,197 bytes, SHA256
`6eac3a2ae83cc5c38f026ba9dffa0d88d4c051868188ff24b3c9a56d825d79d9`.
Normal, seed17 and deliberately corrupted-certificate checks are recorded
in the parent [verification](../verification.json).
