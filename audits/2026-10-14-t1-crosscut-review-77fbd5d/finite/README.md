# Independent essential finite reconstruction

`reconstruct.py` was implemented from the frozen notes and the original
`77fbd5d` named collar definitions before any supplied candidate output data
was inspected. It imports neither candidate algorithms nor candidate data.
`compare_candidate.py` was added afterward and reads only candidate JSON data.

The reconstruction reproduces all **32** essential single-original-vertex
crosscut cases: **512,568** maximal safe rectangles and **25,348** shell literal
lifts, counted with the eight original query identities. The post-Kempe output
masks are exactly **0, 165, 424, 429**; every rectangle misses original B row
`01232` (bit 9). This is a finite support obstruction. Its application to every
original source requires the separate source coverage and gluing arguments.
The additional 32 BRIDGE shells are outside this reconstruction's scope.

## Replay

From the repository worktree root:

```sh
python3 -B audits/2026-10-14-t1-crosscut-review-77fbd5d/finite/reconstruct.py --output-dir /tmp/t1-finite-normal-new
PYTHONHASHSEED=17 python3 -B audits/2026-10-14-t1-crosscut-review-77fbd5d/finite/reconstruct.py --output-dir /tmp/t1-finite-seed17-new
```

Use new output paths: certificate writes are exclusive and refuse to replace
earlier evidence. The existing candidate comparison is retained in
`candidate_comparison.json`; its checker reads candidate data without importing
candidate algorithms. Normal replay took approximately 14 seconds in this audit environment. Normal
and seed-17 `certificate.json.gz` and `summary.json` are byte-identical;
`determinism.json` records lengths and SHA256 values. Runtime is excluded from
the deterministic output and retained in the logs.

## Calculation and complete certificate

The shell consists of the original named B–C8 annulus and one original `x`
joined to `c_i,c_(i+4)`. Its vertex order is
`b0,b1,b2,b3,b4,c0,c1,c2,c3,c4,c5,c6,c7,x`. Fixed-order DFS lists every literal
shell coloring for each canonical original B row. Both C6 indices are then
read from that same coloring. Every one of the 31 × 31 transfer entries is
stored, including zero entries.

Kempe rules enumerate all 203 partitions of the six boundary positions, retain
the 132 noncrossing partitions, then impose the complementary-color-pair and
boundary-edge conditions. Each admissible partition stores all outcomes of
independently exchanging every boundary-contacting component. The deletion
operator updates all rows synchronously until no further deletion occurs.

The maximal rectangles are obtained from the complete family of intersections
of the safe row-neighbor sets. Both closure equalities are checked for every
rectangle; empty-side rectangles are included when maximal. Each rectangle is
shrunk separately on its two sides before the transfer union is formed.

`certificate.json.gz` contains the original row orders, all Kempe rules and
their partition evidence, and 32 case records. Each case stores:

- `vertices`, `edges`, `interfaces`, `original_to_C8`: exact shell identity;
- `full_lifts[B index]`: complete sorted literal coloring strings;
- `matrix[q][r]`: original ten-row output mask, retaining zero pairs;
- `safe_neighbors`: all 31 safe-neighbor bitmasks;
- `rectangles`: every `[A,B,kappa(A),kappa(B),possible,missing]` record;
- named query, original collar, target, counts, and output distribution.

`candidate_comparison.json` records exact equality with every supplied
essential candidate graph, transfer entry, six-column rectangle record, and
literal shell lift. It does not independently validate the candidate's extra
BRIDGE cases or establish the source geometry. Those are separate audit tasks.
