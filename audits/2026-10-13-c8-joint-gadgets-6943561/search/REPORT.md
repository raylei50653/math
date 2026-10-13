# Complete five-private-vertex C8 cap test

The eight frozen necessary support bounds are hit by **every simple plane C8
disk cap having at most five private vertices**. This finite negative result is
conditional on the frozen plantri generator's advertised completeness; all
emitted embeddings, complete extension fibres, and named boundary maps are
checked directly. It closes the search for a single pure cap in that exact
budget as a way of rejecting one of these eight upper supports. It does not
construct a residual source or prove that the true source relation hits a cap.

The [triangulation completion proof](../theory/PROOF.md) extends an arbitrary
simple disk cap to a triangulated disk on the same vertices and the same outer
cycle. Adding edges only removes accepted boundary rows. Hence a rejecting cap
would give a rejecting triangulated cap, with no increase in the vertex budget.

The bundled plantri 5.8 source and guide are frozen in [vendor](vendor/).
The guide's `-P` section, lines 444–490, specifies simple embedded disks with a
distinguished simple outer cycle and triangular internal faces. The command
`plantri -aP8c2m2 n`, for `n=8,...,13`, permits boundary chords and degree-two
boundary vertices. Interior vertices in a triangulated disk necessarily have
degree at least three. These options cover the completions in the proof.

| Private vertices | Embedded isomorphism classes | Stored complete fibres |
| ---: | ---: | ---: |
| 0 | 12 | 3,288 |
| 1 | 91 | 24,934 |
| 2 | 685 | 187,690 |
| 3 | 5,051 | 1,383,974 |
| 4 | 38,078 | 10,433,372 |
| 5 | 290,595 | 79,623,030 |
| Total | 334,512 | 91,656,288 |

Every class receives all 16 dihedral maps to each query's actual named C8.
Thus 5,352,192 orientations, counted with duplicates, yield 42,817,536
cap/query tests. These are not counts of distinct labelled caps. There are no
zero intersections. The minimum support intersections are:

| Query | Minimum |
| --- | ---: |
| c04-941, c07-941 | 2 |
| c15-933, c15-941, c18-933, c18-941, c20-941, c30-941 | 4 |

The [producer](scan.cpp) traverses the emitted rotation system, checks that all
faces except the unique C8 are triangles and checks Euler's equation. It assigns
all 274 frozen literal boundary rows and enumerates every private colouring,
including empty fibres. The query transformations transport whole rows in one
common colour frame. There is no separate normalization of unrelated pieces.

The [results](RESULTS.json) document the exact encoding and raw-data hashes.
For each `h`, `data/hh.ascii.gz` contains every original rotation system;
`data/hh.counts.u16le.gz` contains the complete literal fibre counts; and
`data/hh.tuples.u16le.gz` contains **all 26,145,720 private lift tuples**, including
the empty tuple when `h=0`. Fibre counts delimit tuples, and zero counts preserve
all empty fibres. Each tuple uses two bits per private vertex in the fixed
colour frame. The whole full-lift relation is reconstructible, not merely its
marginals or support mask.

[Eight named witnesses](witnesses.json.gz) retain explicit full tuples for all
274 rows on five-private-vertex caps, with adjacent private vertices. Each
attains its query's global minimum intersection. Their independent
[Python brute-force checker](witnesses.py) iterates all `4^5` private assignments
for every literal row, compares complete counts, and rejects deleted lifts,
changed boundary names, and false empty intersections.

Reproduction:

```bash
python3 -B audits/2026-10-13-c8-joint-gadgets-6943561/search/run.py --check
python3 -B audits/2026-10-13-c8-joint-gadgets-6943561/search/witnesses.py --check
```

The full independent review is recorded by the parent audit. Enumeration
coverage is a plantri dependency, not a newly proved generation theorem. No
four-colour theorem is assumed in the finite calculations, and no Lean theorem
is added. This result does not cover auxiliary operations identifying original
boundary vertices, a larger budget, simultaneous constraints on other faces,
or actual source count-vector realizability. Those require separate arguments.
