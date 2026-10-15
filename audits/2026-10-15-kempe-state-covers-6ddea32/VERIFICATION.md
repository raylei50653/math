# Formal replay and independent checks

```sh
python audits/2026-10-15-kempe-state-covers-6ddea32/check.py
PYTHONHASHSEED=17 python audits/2026-10-15-kempe-state-covers-6ddea32/check.py
```

Both pass, in about a second each. Every replay checks original/frozen input
hashes, graph hashes, exact cover-space equations/ranks, both complete graph
colouring sets, all six actual component partitions, full component switches,
whole cubes, global colour renaming and monodromy. The certificate is compared
in full, including every normalized full colouring, rather than summary counts.

The saved `missing-full-colouring`, `wrong-monodromy` and `wrong-cover-rank`
certificates are each rejected. `--write` rejects the already existing
certificate through exclusive create. All six command receipts and stdout/stderr
are in [logs/receipts.json](logs/receipts.json).

An initial JSON replay exposed a tuple/list comparison issue in the diamond
control's edge metadata. The checker now emits JSON-native lists. The graph
files and certificate did not change. The root retained that preliminary failed
replay separately, then repeated all five main positive/negative checks
successfully; it is not counted as a successful run.

Independent original-edge verifications:

- The root's `route-round4-6ddea32/check_cover_graph.py` independently enumerates
  all121-point graph colourings with single-vertex DSATUR (2834 nodes) and checks
  all components and transitions. Its `cover-graph-independent.json` records
 36 normalized/864 complete colourings,8160 individual components/switches,
 26112 cube masks and hidden count0.
- The geometry reviewer's `j-source-geometry-6ddea32/check_cover75.py` independently
  does the corresponding75-point check (1462 DSATUR nodes), obtains the same
 36/864 complete sets and component/switch counts, and independently detects
 the incompatible section equations. Normal/seed17 pass and a missing-full-
 colouring corruption is rejected; see its `cover75-independent.json` and
 `CROSS_REPLAY.json`.

These independently rebuilt full colourings and components support the positive
graph theorem. The512-class discovery records are exploratory provenance only;
no source or full720 exclusion relies on treating that search as an authority.
The separate matching cross-review and its independent residual/barrier replay
are in [CROSS_REVIEW.md](CROSS_REVIEW.md).
