# Independent K13 review

All scripts in this directory are independent of the main checker and generation
implementation. They import only other modules in this directory, the Python
standard library, and (where explicitly stated below) NetworkX 3.5. Python was
3.14.7. The graph inputs are the literal frozen planar-code bytes; no checker
infers coverage merely from a generated JSON list.

## Results and interfaces

- [check.py](check.py) independently parses `spheres19.pc`, follows the dart
  permutation, checks connectedness and Euler genus zero, and checks all 23
  nineteen-vertex triangulations. It deletes **all 306 degree-five roots**,
  retains original sphere vertex identifiers, verifies the prescribed C5 face,
  and reconstructs the complete collar and every inner chord from original
  directed faces. It computes all ten complete relation fibres.
- [relations.json.gz](relations.json.gz) stores all 306 original-label graphs,
  faces, degree data, collars, ten rows including complete lifts, and all ten
  whole-graph D5 frames. There are 3,060 accepted fibres and 41,021 full lifts;
  every relation is 1023. No fibre in this specific family is empty.
- [review.py](review.py) compares all generated source structures with those
  reconstructed independently. [review.json](review.json) records the result
  and seven rejecting controls: missing chord, wrong outer face, wrong B,
  degree miscount, omitted accepted lift, wrong mask, and omitted root. A
  C5-with-chord calibration directly tests a nonconstant D5 orbit.
- [compare_main.py](compare_main.py) compares all original edges, rotation,
  faces, degrees, collar data, mappings, every full lift, all ten row counts,
  and all ten D5 frames with the 23 compressed main core files. This translates
  each main canonical vertex back to its actual original vertex before
  comparison. [compare_main.json](compare_main.json) records equality of all
  41,021 lifts and six rejecting controls that directly corrupt copies of the
  main certificates.
- [calibration_check.py](calibration_check.py) independently recomputes the
  main C5, chord02 and wheel5 calibration certificates. Their masks are 1023,
  1016 and 91, with eight rejected fibres in total. Each D5 frame is checked
  by globally relabelling every full lift and comparing a fresh fixed-boundary
  CSP search. [calibration_review.json](calibration_review.json) records 300
  row/frame comparisons and rejection of an invented lift in an empty fibre.

The domain solver differs from the main sequential backtracking implementation.
A vertex domain initially contains all four colors, except for the fixed literal
B assignment. A singleton domain removes its color from adjacent domains;
propagation repeats to a fixed point. A singleton conflict rejects that branch.
Otherwise the smallest nonsingleton domain is chosen and each remaining color
is branched on separately. Each deletion follows a literal original edge;
each proper coloring survives exactly one branch and is output once. Thus both
nonempty fibres and exhaustive rejection are checked on the same entire graph.
No independent piece, side, color row or interface is separately normalized.

## Independent finite-coverage checks

[inner_coverage.py](inner_coverage.py) reads every one of the 2,472 min-degree-four
fourteen-vertex sphere rotations independently. It takes every cone vertex of
degree 9 through 12, deletes it, checks its specified outer face, and enumerates
**every** five-apex subset containing all H-degree-three boundary vertices.
Only the two necessary degree filters in the paper proof are used.

| h | All cone roots | After only I-degree >= 5 | After both degree conditions | Apex subsets |
|---:|---:|---:|---:|---:|
| 4 | 629 | 24 | 19 | 27 |
| 5 | 214 | 24 | 1 | 1 |
| 6 | 41 | 12 | 0 | 0 |
| 7 | 2 | 2 | 0 | 0 |

The root/apex-subset key set agrees exactly with the 28 generated inner cores.
Every completed nineteen-vertex rotation is checked, including its untouched
original H, each attachment, the explicit mapping to the primary sphere, the
recorded global orientation sign and the target B frame. Separately searched
root-preserving VF2 isomorphisms, followed by cyclic-order verification under a
**single global orientation**, match all 45 primary h=4,5 roots to the inner
cores. This comparison does not trust the saved isomorphism list.

The same checker enumerates all nonnegative named five-part compositions for
h=4,5,6,7 and checks all 736 saved entries, the 10/16/26/38 D5 representative
orbits, and every permitted placement of each inner core into a named
configuration. Results and all input hashes are in
[inner_coverage.json](inner_coverage.json).

[small_exhaustive.py](small_exhaustive.py) uses a different generation method:
it enumerates **all labelled simple edge subsets** with 3n-6 edges for n=4..7,
then uses NetworkX planarity and isomorphism to obtain the sphere classes.
This is a finite independent completeness check of a smaller domain, not a
second proof of full nineteen-vertex generation.

| n | All tested edge sets | Planar labelled triangulations | Isomorphism classes |
|---:|---:|---:|---:|
| 4 | 1 | 1 | 1 |
| 5 | 10 | 10 | 1 |
| 6 | 455 | 195 | 2 |
| 7 | 54,264 | 5,712 | 5 |

Each class matches exactly one plantri output. The edge-subset universe is
complete by construction; min degree three is a necessary condition for a
simple sphere triangulation at these sizes. NetworkX 3.5 is used only for this
small-domain planarity/isomorphism calibration and the independent rooted
isomorphism search in `inner_coverage.py`; graph/fibre replay itself uses only
the standard library. Results are in [small_exhaustive.json](small_exhaustive.json).

The two large generation paths still share plantri. Their universal coverage
rests on [the source and cone proofs](../PROOF.md) and the cited external
construction theorems. Neither the independent relation solver, the small test,
nor agreement between finite output lists alone proves that external theorem.
No new Lean statement is supplied here.

## Replaying the checks

From the isolated repository root:

```bash
python3 audits/2026-10-13-k13-collar-50d5474/independent/check.py --check
python3 audits/2026-10-13-k13-collar-50d5474/independent/review.py --check
python3 audits/2026-10-13-k13-collar-50d5474/independent/compare_main.py --check
python3 audits/2026-10-13-k13-collar-50d5474/independent/calibration_check.py --check
uv run --with networkx==3.5 python audits/2026-10-13-k13-collar-50d5474/independent/inner_coverage.py --check
uv run --with networkx==3.5 python audits/2026-10-13-k13-collar-50d5474/independent/small_exhaustive.py --check
```

The local actual NetworkX runs used the existing interpreter
`/home/ray/developer/ai/math/.venv/bin/python`; no package installation was needed.
Normal and `PYTHONHASHSEED=17` runs compare mathematical outputs byte-for-byte.
The small exhaustive comparison omits only plantri's elapsed-time stderr from
its replay equality. The final orientation assertions were added after the
initial inner check; its two `*_v2.log` files replay the unchanged certificate.

## Run history

Initial source review output is retained as `review.v1.json` and accompanying
logs; the current version adds the nonconstant D5 calibration. An initial main
comparison attempt assumed `y` was a flat list, whereas the main schema stores
five named per-B lists. This raised `TypeError` before any comparison certificate
was written. The comparator was corrected to flatten those five lists for its
set comparison; the original empty stdout files are preserved under
`compare_main*.schema-failure.stdout.log`. The error text was visible in the
session tool output, not redirected to those stdout files. Subsequent normal
and seed17 main comparisons both passed. No failed mathematical certificate
was deleted or replaced.
