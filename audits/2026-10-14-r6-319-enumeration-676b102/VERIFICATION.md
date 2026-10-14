# Verification and replay

Run commands below from this audit directory. INPUTS.json binds all frozen
authority bytes, including the current uncommitted cofacial supplement.
The final MANIFEST.json inventories the new bundle; historical inputs and
failed/negative controls are retained, not silently repaired or overwritten.

## Generator and coverage

The frozen plantri C source is built with `cc -O3`; command lines, compiler
output and environment are in logs/compile-plantri.json,
logs/compile-r6-filter.json and logs/environment.json. FILTER and SUMMARY are
the only plugin hooks. `return 0` suppresses normal plantri output, so its
last line says zero output graphs; **R6_COUNTS.spheres** counts every
unfiltered generator callback and is the generation-coverage authority.

The full sums are 4,412,031 for n29 and 16,248,772 for n30, agreeing with the
frozen guide. Each run has all32 distinct residues with denominator32.
Generation and search receipts have each input/certificate SHA256. The
runner refuses existing run directories and binds all production source
and executable bytes before and after the run.

Unfiltered planar_code for the n29 0/256 control contains11,648 graphs.
Independent Python reconstructs every original graph, all roots/frames and
every filter, agreeing exactly with all C counters and named outputs.
This is a full comparison of the stated control shard, **not** a second
independent full generation at n29/n30.

```sh
python3 -B src/search.py coverage runs/pilot29-raw.pc runs/pilot29-filter.jsonl logs/pilot29-filter.json
PYTHONHASHSEED=17 python3 -B src/search.py coverage runs/pilot29-raw.pc runs/pilot29-filter.jsonl logs/pilot29-filter.json
```

An initial coverage comparison failed because planar_code breadth-first
renumbers vertices while FILTER sees internal labels. The corrected checker
transports the entire rotation and all pins by one BFS relabeling. Retained
evidence: validation/search-before-pc-relabel.py and
validation/pilot29-coverage.stderr; successful v2 and seed17 logs are separate.
The C predicate and the search solver did not change in this repair.

## Exact witness replay and controls

The replay reconstructs U directly from original sphere edges and the
literal a=c quotient, checks every point and edge of every saved coloring,
and checks the specified forbidden outer row or an actual forbidden r lift.
It compares all frame counts, sphere counts, receipts, hashes and aggregate
summaries. It does not call the search solver for the witnessed outcomes
that occur in these two full runs.

```sh
python3 -B validation/verify_run_parallel.py 29
PYTHONHASHSEED=17 python3 -B validation/verify_run_parallel.py 29
python3 -B validation/verify_run_parallel.py 30
PYTHONHASHSEED=17 python3 -B validation/verify_run_parallel.py 30
python3 -B src/controls.py
PYTHONHASHSEED=17 python3 -B src/controls.py
```

For n29 the first normal full replay used validation/verify_run.py, whose
threads invoke the same verifier directly. The parallel wrapper instead
uses independent Python subprocesses for better CPU utilization.

Controls verify all30 complete small-representative fibres by direct
product, the entire4^7 all-r-lifts table, and rejection of an improper full
coloring, wrong row, and exchanged literal p/q pins. Additional retained
negative files omit one frame or alter the total count; replay rejects both,
as recorded in validation/coverage-negative.json. Solver timeouts are never
treated as empty fibres; production search has no such cutoff.

Near-miss full fibres are computed by two different recursive algorithms
and compared as complete sorted lists. Their data include empty outer
fibres, original graph rotations, all names and complete joint counts.
The generation commands below are exclusive writers and are already run:

```sh
python3 -B validation/near_misses.py 29
python3 -B validation/near_misses.py 30
```

To repeat production in a fresh bundle, preserve INPUTS.json and frozen/,
copy the unchanged src/ and create empty logs/ and runs/ directories, then
execute `python3 -B src/run.py 29` and `python3 -B src/run.py 30`.
The existing complete runs intentionally cannot be overwritten.

## Trust and scope

The finite conclusion uses the inherited source lemmas, the published
plantri completeness theorem and C implementation, complete finite
generation/partition coverage, and independently checked original-edge
color witnesses. The independent Python filter check covers the11,648-graph
control shard; every **retained** full-run graph also has its frames
independently reconstructed during search. A verified generator, full second
generator, Lean formalization and arbitrary-size exclusion are not claimed.

No whole-repository Lean or DocGraph replay is required by these isolated
audit-only additions. Final local-link, bundle-hash and frozen-input
checks, and the final per-run replay statuses, are recorded below after
completion.

## Final results

| Check | Result and retained log/data |
| --- | --- |
| n29 all32 partitions,2,060,174 full witnesses | PASS; validation/n29-replay.stdout |
| n29 full seed17 replay | PASS; validation/n29-replay-seed17.stdout |
| n30 all32 partitions,7,880,088 full witnesses | PASS; validation/n30-replay.stdout |
| n30 full seed17 replay | PASS; validation/n30-replay-seed17.stdout |
| Complete independent raw/filter shard comparison | PASS default and seed17; validation/pilot29-coverage-v2.stdout and validation/pilot29-coverage-seed17.stdout |
| Brute-force fibre and entire seven-pin table controls | PASS default and seed17; validation/controls.stdout and validation/controls-seed17.stdout |
| Wrong color, row or pins | All3 rejected; controls logs |
| Missing frame or altered summary | Both rejected; validation/coverage-negative.json |
| n29 near misses | All4 are319; all2,160 full lifts agree between both algorithms; validation/n29-near-misses.summary.json |
| n30 near misses | All52 are319; all34,704 full lifts agree between both algorithms; validation/n30-near-misses.summary.json |
| Nonfacial-triangle diagnostic on all56 near-miss frames | Every frame fails this additional source requirement; validation/n29-structural-controls.json and validation/n30-structural-controls.json |

The frozen-input and local-document validation is in validation/final-checks.json.
MANIFEST.json lists final file hashes; an exported copy is accepted only after
every listed byte count and hash has been checked. No source realization,
all-size theorem, new general K bound, or new Lean theorem is asserted.
