# Fixed-rotation directed search and its boundary

The search checks concrete sphere rotation systems. It does not assume that
S5 excludes a return of period four. Each `search-inputs/nN.ascii` line gives
all clockwise neighbor lists, using vertex names `a,b,...`; the entire original
graph, its embedding, and the particular neighbor order at every center are
therefore retained. `search-generation.json` preserves generator arguments,
stdout/stderr and output hashes. The generator binary and its hash are also
recorded in `search-certificate.json`.

For every line, the checker traverses every directed edge to rebuild the
original triangular faces and verifies connectedness and Euler characteristic
two. It enumerates every simple cycle of length three through five exactly
once (least vertex first, smaller of the two directions). Deleting its edges
from the face dual gives the two actual open sides. Degree at least five,
absence of separating triangles/quadrangles, and S5 are checked from this
original embedding. No path or side from another source is used.

For every legal input graph and every degree-five center, `boundary` is
precisely that center's displayed neighbor order, with its displayed first
entry. There is no additional quotient by boundary rotation or reflection,
and no claim that all ten frames were searched. After deleting the center,
the private vertices are put in ascending original-label order. A backtracking
search lists every complete literal proper coloring whose ordered boundary is
`(0,1,0,2,3)`. At every node it chooses an uncolored vertex and branches over
exactly all colors absent from its already colored neighbors. This gives
soundness, completeness and uniqueness by the usual induction on the number
of uncolored vertices. It retains the whole exterior O.

The partial H map performs the five prescribed exchanges. Every exchange
uses a fresh full-O BFS in the current two-color induced subgraph. A row is
kept only when all five displayed boundary colorings match the prescribed
ones. The final map `(2,3,1,0)` is applied globally to the full exterior
coloring. Kept rows have pairwise distinct targets, checked explicitly; this
also follows from reversing the five actual swaps and global normalization.
All cycles of this partial map are obtained by following its arrows until a
previously seen state, a local repeated state, or an undefined arrow is
reached. The certificate stores fibre sizes, successful round counts and all
cycle lengths separately for every eligible center of every input graph.

A four-cycle in this partial map would establish only a legal local return.
Its complete Kempe component would still have to be independently explored
to decide whether it is blocked. The producer schema for any such witness
retains all original edges, sphere faces, rotation, ordered boundary, four
full literal source colorings and all twenty actual swaps. All swap vertex
labels refer to the original graph; each complete color vector is ordered by
`exterior_vertices`. No witness is silently classified as blocked.

The same full-O engine was also run against the frozen Errera source and its
five earlier legal S5 diagonal-flip controls, preserving the original frame
`[0,1,2,3,4]`. `search-control-check.json` records their complete fixed-frame
fibre sizes, successful rounds, cycles, original graphs and faces, and the
source's forbidden separating five-cycle. It recovers the genuine Errera
four-cycle and no cycle in its five repaired controls. These are controls,
not a proof that all S5 repairs remove all possible four-cycles.

The bounded zero result concerns only the supplied concrete inputs and their
specified frames. Generation completeness beyond these supplied inputs is a
separate dependency on plantri. It neither proves the unrestricted S5
four-cycle candidate nor excludes periods six and above in general, and it
does not prove Q5 or a general Kempe escape theorem. The producer replay is
an exact Python finite computation, not a Lean theorem.

## Independent finite-input review

`c5_period4_s5_search_review.py` does not import the producer. It rebuilds the
face permutation and verifies the connected spherical triangulation, then
uses deletion of the original cycle vertices to check the separating sides.
For this method, the following planar fact is used: in a simple spherical
triangulation a minimal vertex separator is an induced cycle. Thus minimum
degree five and no separating triangles or quadrangles imply five-connectivity.
When deleting a C5 disconnects the graph, every remaining component must
have at least five neighbors on C5, hence all five. Two components in the
same open side would supply disjoint paths between alternating boundary
pairs (take b0–b2 through one and b1–b3 through the other), contradicting
Jordan separation in that disk. Each nonempty open side therefore corresponds
to exactly one vertex-deletion component. Comparing their sizes tests S5
independently of the producer's face-dual traversal.

The independent reviewer enumerates the complete literal fibre using bit
domains and reversible domain updates. It computes actual whole-O components
with color-class bitsets, applies the global alignment to all original vertices,
and peels states of indegree zero from the partial map. Zero residual states
prove that no directed cycle remains; this differs from the producer's orbit
following algorithm. All 13 order domains and all center counts match the
stored producer data; see `search-independent-n24.json`. This is finite-input
verification, with the same catalogue/frame boundary stated above.

Reproduction (from the canonical repository root):

```bash
python3 scripts/c5_period4_s5_search.py --generate
python3 scripts/c5_period4_s5_search.py --check
python3 scripts/c5_period4_s5_search.py --controls
python3 scripts/c5_period4_s5_search.py --controls --check
```

The first command generates and scans orders 12 through 24. The second replays
the preserved concrete ASCII inputs without invoking the generator. The
control commands operate only on the earlier frozen Errera/flip input. A new
checkout must restore any audit artifacts archived by the repository's
ordinary audit custody rules before replay.

## Recorded finite result

| Original order | Input spheres | S5 spheres | Degree-five centers | Complete ABACD fibre states | Complete single H rounds |
| --- | ---: | ---: | ---: | ---: | ---: |
| 12 | 1 | 1 | 12 | 24 | 0 |
| 13 | 0 | 0 | 0 | 0 | 0 |
| 14 | 1 | 1 | 12 | 48 | 0 |
| 15 | 1 | 1 | 12 | 42 | 0 |
| 16 | 3 | 3 | 38 | 226 | 0 |
| 17 | 4 | 3 | 37 | 332 | 25 |
| 18 | 12 | 11 | 142 | 1,435 | 3 |
| 19 | 23 | 20 | 263 | 3,473 | 9 |
| 20 | 71 | 62 | 838 | 15,525 | 153 |
| 21 | 187 | 157 | 2,179 | 50,457 | 466 |
| 22 | 627 | 517 | 7,379 | 228,235 | 2,035 |
| 23 | 1,970 | 1,571 | 23,067 | 932,897 | 5,792 |
| 24 | 6,833 | 5,343 | 80,690 | 4,274,320 | 32,993 |

Totals: 9,733 supplied original spheres, 7,690 structurally legal S5 spheres,
114,669 degree-five centers, 5,507,014 complete fixed-literal fibre colorings,
and 41,476 successful single H rounds. Every tested partial H map is acyclic.
There is no period-four witness in this finite fixed-frame domain. This does
not settle the unrestricted candidate.
