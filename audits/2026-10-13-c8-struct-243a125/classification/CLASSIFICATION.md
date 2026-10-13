# Ten named residuals: five whole-collar equivalence pairs

Status: **proved** for the explicit isomorphism of named query contracts;
**necessary-condition residual** describes every query at the frozen input.
This symmetry classification alone proves no exclusion. The subsequent
[cofacial quotient theorem](QUOTIENT_PROOF.md), combined with the induced-C8
geometry theorem, **excludes c16-941 and c32-941**; eight queries remain.
Input bytes are those frozen in this audit. All ten full
274-coordinate vectors, ten outer counts, named C8 orders, collar edges,
attachments, positive supports, and transport permutations are in
`classification.json`.

## Exact equivalences

The outer row order is the complete ten-row order
`01012 01021 01023 01201 01202 01203 01212 01213 01231 01232`.
The action on B is specified as the image of each *old* index. Transport
every vertex, edge, full lift, and color assignment by this single map.
Only after transporting a whole word may one apply a common permutation
of the four color names to choose its canonical representative. There are
no independent normalizations of pieces or row-dependent label maps.

For target 933, its stabilizer in the dihedral group of the ordered C5 is
exactly the identity and `b_i -> b_(3-i)`. For target 941, it is exactly
the identity and `b_i -> b_(1-i)`, with all indices modulo five.

| Target | Named query pair | Named extras, source -> destination | Positive support size | Transported saved vectors |
| --- | --- | --- | ---: | --- |
| 933 | c15 -> c18 | (0,1,2,0,0) -> (0,2,1,0,0) | 134 | Different; not proportional |
| 941 | c04 -> c07 | (0,0,1,0,2) -> (0,0,2,0,1) | 193 | Different; not proportional |
| 941 | c15 -> c20 | (0,1,2,0,0) -> (1,0,0,0,2) | 173 | Different; not proportional |
| 941 | c16 -> c32 | (0,2,0,0,1) -> (2,0,1,0,0) | 102 | Exactly equal |
| 941 | c18 -> c30 | (0,2,1,0,0) -> (2,0,0,0,1) | 175 | Different; not proportional |

Every pair has exactly matching *full* positive supports under its explicit
274-coordinate permutation. Equal size was not used to assert equivalence.
The different stored vectors are separate witnesses in equivalent necessary
condition systems. They are not required to be equal or proportional.

For a reflection `b_i -> b_(k-i)`, the apex and private-point maps are

```
a_i -> a_(k-i-1)
y_(i,j) -> y_(k-i,t_i+1-j).
```

The second formula reverses the entire ordered private interval. This is
essential when `t_i=2`. Under the source/destination naming in the table,
the source C8 position maps for 933 are `[5,4,3,2,1,0,7,6]`; for all four
941 pairs they are `[0,7,6,5,4,3,2,1]`. The ten outer-row maps are,
respectively,

```
933: [0,6,7,4,3,5,1,2,9,8]
941: [3,1,8,0,6,7,4,5,2,9].
```

This is a proof-transport equivalence between explicitly named contracts.
It does not change labels inside a fixed source or identify two arbitrary
actual H graphs. A source exclusion for a representative would transport
to its partner by this global map, provided the proof preserves all the
source hypotheses.

## Universality of the transport

The collar consists of B edges, C8 edges, and each recorded attachment edge.
The maps preserve all three complete edge sets. They reverse the cyclic
orders of both boundary components coherently and preserve the annular
incidences and all private interval orders under reflection. Apply the
reflection to an arbitrary disk embedding of H, regardless of the number
of internal vertices, retaining its internal vertex identities. The
result is a disk embedding with the destination named collar. Degrees,
triangular faces, separating triangles, and incidences are preserved.

Sending the color of each vertex to its image gives a bijection on full
proper colorings, with the same global color frame. The explicitly checked
outer-row permutation stabilizes the whole target relation, including
all rejected rows. Thus all source hypotheses and the entire ten-row
relation transport together. The argument is valid for arbitrary finite
H. It is a structural symmetry theorem, not a realization theorem.

The independent checker enumerates all 120 permutations of B, selects the
ten C5 automorphisms, and calculates the two complete target stabilizers.
It checks the collar edge and attachment maps, cyclic orientation, all
274 inner pattern maps, and all `5 * 10 * 274 = 13,700` transfer entries.
It also checks each transported complete vector and all ten outer counts.

## Conditional support-to-edge obstructions

The following elementary necessary condition is valid for every finite
graph: if `uv` is an edge, no proper-coloring extension with boundary
colors `p(u)=p(v)` exists. Consequently one positive boundary extension
count with `p(u)=p(v)` certifies that `uv` is not an edge. This implication
does not depend on planarity or the interior size.

For each of the 20 nonadjacent C8 pairs, `classification.json` records the
complete list of positive saved-vector coordinates with equal endpoint
colors, including empty lists. Exact checking gives:

* In eight queries, all 20 pairs have positive equality witnesses. Any H
  realizing exactly that saved positive support must have chordless C8.
* In c16-941 and c32-941, 19 pairs have positive equality witnesses. The
  remaining pair is `(a1,a4)`; the positive-equality test alone does not
  forbid this edge. The separate cofacial quotient theorem strengthens
  this observation: the absence of every equal row from the complete
  upper forces the edge in an actual planar H, and the induced-C8 theorem
  then excludes both complete queries.

These are **conditional** statements about a graph realizing the complete
saved support (or those complete saved vectors up to positive scaling).
An actual source is only known to have support *contained in* the final
upper. It may omit the equality witnesses. Therefore these observations
alone do not forbid C8 chords in every actual source or classify all source
geometries. The cofacial proof uses absence from the full upper rather than
positivity in a selected vector, so it also applies to all smaller actual
supports. The ten saved input vectors and classifications remain intact.

## Replay

```
python3 audits/2026-10-13-c8-struct-243a125/classification/checker.py
python3 audits/2026-10-13-c8-struct-243a125/classification/negative_controls.py
python3 audits/2026-10-13-c8-struct-243a125/classification/verify.py
```

The producer writes exclusively to a new output; regeneration can use
`generate.py --output /tmp/fresh-classification.json`. The replay compares
default and seed-17 output bytes and runs the checker CLI on deliberately
corrupted certificates. It never calls the old transfer/Kempe/count solver.
