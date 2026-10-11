# Independent unary and whole-source fixed controls

BASE is the parent audit's immutable `BASE.json`. Every input read by
`checker.py` is a hash-checked frozen snapshot. No old checker was imported or
executed, and no old artifact was regenerated. All writes are in this directory.

The independent algorithm chooses the next vertex by its current smallest color
domain, retains its original ordered tuple, and sorts the complete resulting
lifts. Blocks are reconstructed by recursively splitting the literal graph at
articulation vertices. All prerequisite facts are derived from original edges.
This differs from the old numeric-order DFS and Tarjan traversal.

The fixed 97 original unary pieces have 970 rows and 15,520 ambient pin cells,
including 2,048 empty cells. Every complete tuple agrees with both the original
component-slack snapshot and the prior unary snapshot. Prerequisites give
42 `triggered and holds`, all with k=2, and 55 `not triggered`. The three old
named local controls also agree in every one of their ten rows and 160 cells.

For each of the 63 whole original graphs, the new artifact additionally retains
all ten rows of direct complete whole-graph 16-pin fibres, including empty
cells. These 630 rows and 10,080 cells agree tuple by tuple with the Cartesian
join of the literal component fibres and all original fixed-fixed edge filters.
The complete Sigma is recomputed independently. None equals 933, 941, or any
common D5 image of either mask. Thus all 63 full target-source controls are
`not triggered`; there is no target-source exclusion or realization result.

The boundary arithmetic is solved by enumerating actual boundary-point choices
in the same three literal rows. All five point and five edge signatures and all
25 ordered-pair classifications agree with the frozen prior table. Four pairs
are rowwise distinct. Of ten distinct-edge triples, two admit an abstract cycle
palette, and zero admit all three actual attachment points simultaneously.

Two further fixed local fixtures preserve complete ten-row, 16-pin relations:

- The original p–w–q positive fixture with contacts split as r–p, s–w, r–q has
  a D,D full lift only in q3 among q0, q1, q3. The complete D,D cells equal the
  original unary fixture in all ten rows.
- One vertex adjacent to both roots and frame points 0,1 accepts D,D in every
  row, hence in all three designated unused-D rows.

These fixtures have no disk, Sigma-criticality, or N2 target-source claim.

`observations.json` was exclusively created: 7,411,936 bytes, SHA-256
`1c84f695ad436fb3e49916a7df421175ebf58df06be556e18c850458bd06e76c`.
Normal and `PYTHONHASHSEED=17` read-only checks pass with identical output.
The retained corrupted copy deletes one complete unary lift and is rejected
with exit 1 and `artifact mismatch`. Re-generation against the existing artifact
is rejected with `FileExistsError`, preserving its hash. Details are in
`verification.json` and `transfer-verification.json`.

The initial generation failed before writing an artifact because a summary's
q-index order followed canonical row traversal while the old artifact sorted
q indices. Sorting the summary repaired this representational mismatch;
`generation.log` and successful `generation-v2.log` are both retained.

These checks do not verify disk rotation, source Sigma-criticality, arbitrary
block-tree case-split completeness, source existence, or a Lean theorem. They
do not expand the fixed control domain into a graph search.
