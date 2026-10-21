# W7 run templates: exact reusable local incidence, cone OPEN

The frozen W7 incidence has substantial repeated local structure even though
equitable refinement of the full LP is discrete. Its 428,506 unpruned columns
come from six universal run templates containing only 5,033 columns in total.
After the existing zero closure, all 307,197 surviving columns are exactly the
corresponding template restrictions. No states, fibres, or original columns are
identified with one another in this representation.

## Literal relabeling and exact check

For a normalized half-row `t`, retain its binary palette word `q_i=t_i//2`.
Every column keeps this word fixed. Collapse each maximal cyclic run of one
palette to one contact. If the word has `2k` transitions, it has `2k` contacts.
Run 0 contains rim position 0 and possibly a suffix across the cyclic seam;
run 1 begins at the first opposite-palette position. Inside a run, properness
forces alternating bits. The H normalization fixes the phase of runs 0 and 1
to zero, leaving the phases of runs 2 through `2k-1` as a `2k-2` bit index.
Bit `r-2` is the low colour bit at the first position of run `r`.

Every original contact partition is constant on each palette run: two adjacent
distinct blocks must be on opposite sides of its block-adjacency bipartition.
The transition requirement then gives `b=k+1` blocks. Collapsing or expanding
the runs preserves the noncrossing condition, the block-adjacency bipartition,
and the independent component flips. Consequently run lengths and rim positions
only determine the literal relabeling; the local incidence depends on `k`.
For each reduced contact partition, the column is one coset of its `k-1`
independent non-anchor block flips in the local phase cube.

`probe.py --build --full-generation` replayed the original 742,900 partitions,
41,834 admissible partitions and 428,506 generated columns. Its full ordered
column-family SHA256 is exactly the frozen
`530aeac43e108f7c94f1e120ec341c18528d36dc3fd41356b5f3b79b3b94a7d5`.
Thus completeness was checked against the full family, not inferred from the
union of surviving columns.

| 2k runs | membership words | local rows | local columns | entries per column |
| ---: | ---: | ---: | ---: | ---: |
| 2 | 78 | 1 | 1 | 1 |
| 4 | 715 | 4 | 4 | 2 |
| 6 | 1,716 | 16 | 20 | 4 |
| 8 | 1,287 | 64 | 112 | 8 |
| 10 | 286 | 256 | 672 | 16 |
| 12 | 13 | 1,024 | 4,224 | 32 |

The partition counts per template are `1,2,5,14,42,132`; direct reduced
enumeration establishes these finite counts. The expected expanded totals are
`sum choose(13,2k)*partitions[k] = 41,834` and
`sum choose(13,2k)*columns[k] = 428,506`, independently matching the replay.

## Reuse after the existing zeros

For every one of the 4,095 binary membership words, keep its exact live local-row
mask and retain only template columns wholly contained in that mask. This
reconstructs exactly every surviving frozen column with its original index.
Only 335 distinct `(k, live row mask)` shapes occur, including two empty shapes;
333 have nonempty incidence. Their counts by `k=1..6` are
`2,8,81,155,83,6`. The most frequent identical mask occurs 1,216 times; others
occur 737 and 574 times. A local projection, factorization, pricing kernel, or
local cone calculation can therefore be cached once per exact shape and reused
with separate literal inputs and witnesses for each occurrence.

The repeated nonempty shapes contain 696,389 incidence entries once, versus
4,264,208 entries after expansion: a measured factor of 6.12 in stored local
incidence. The six full templates plus complete row map and surviving-column
map occupy 2,435,032 gzip bytes in total. This comparison concerns those
representation files; the original orbit artifact also stores closure metadata.
The application probe separately materializes both local matrix orientations
and the instance gather/scatter maps; 6.12 is an incidence-reuse factor, not a
measured process-memory reduction.

Each local column additionally factors as a Cartesian product of its two
palette phase supports. At `k=6`, 4,224 columns reuse only 903 distinct support
factors on either palette; each factor side has 4,224 entries in total. This
factorization was checked for every template column. It is a further kernel
design option; no faster implementation from these factors is claimed here.

## Implemented matrix application and limits

`apply_probe.py` caches the 333 nonempty matrices and batches the separate
vectors having the same shape. It implements both `C x` and `C^T y` while
preserving the original 183,924 half-row coordinates and 307,197 column
coordinates. Both directions match the frozen matrix exactly on deterministic
signed integer inputs. Corrupting a cached incidence coefficient is detected.

The fair float benchmark converts coefficients to float before timing either
path. Median of nine applications in `apply_report.json`: frozen `C` 2.83 ms,
templates 3.84 ms; frozen `C^T` 2.88 ms, templates 3.71 ms. This Python/SciPy
implementation is slower, because gathering, scattering and 333 small calls
outweigh the storage reuse. Earlier mixed-integer/float timings were discarded.
The evidence supports local caching and reduced repeated preprocessing; it does
not yet support replacing production sparse matvecs for speed.

These are exact incidence and representation results. They do not identify
different states, merge their full fibres, remove the shared-Z compatibility,
or establish positivity, a feasible joint cone point, source exclusion,
source realization, a smaller bad source, or a Lean theorem. Dense-basis
elimination and exact certificate construction remain separate obligations.

## Reproduction and exports

Default runs check existing artifacts read-only. `--build` is required to write.

```
python3 -B audits/2026-10-21-w7-reuse-d5b8a86/templates/probe.py --full-generation
PYTHONHASHSEED=17 python3 -B audits/2026-10-21-w7-reuse-d5b8a86/templates/probe.py --full-generation
audits/2026-10-20-w7-count-opt-d5b8a86/py -B audits/2026-10-21-w7-reuse-d5b8a86/templates/apply_probe.py
```

`templates.json.gz` holds the six lexicographically sorted template families.
`row_map.json.gz` retains all 199,290 original half-rows, including dead fibres,
with original canonical state id, membership word, run count, local phase index
and live flag. Membership is encoded as `sum q_i*2^i`.
`column_map.json.gz` retains original surviving column order and maps each
column to its membership word and template column. There is no lost gauge:
the literal encoded half-row and original state are explicitly stored.

The probe also reconstructs a frozen literal column and confirms rejection
after independently changing its template support and its template-column
mapping. Original artifacts remain read-only throughout.

Normal and `PYTHONHASHSEED=17` full-generation read-only replays both passed;
the numerical-environment read-only application check passed as well. Their
outputs are `check-normal.log`, `check-hash17.log` and `apply-check.log`.
