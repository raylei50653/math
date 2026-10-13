# K15: complete source coverage

2026-10-13. The immutable inputs are the Git objects listed in `BASE.json` at
`6cafdfb`. This is a continuation of the K14 proof, with fifteen interior
vertices and sphere order twenty-one. It is not an arbitrary-size exclusion.

## Source and minimality

Let K be the existing 132 complete ordered C5 boundary relations. Each member
has an at-most-five-interior-vertex witness. Suppose a finite simple disk graph
with at most fifteen interior vertices has relation outside K. Among **all**
catalogue-outside sources minimize interior order k, then maximize edge count.
The previously established K14 equality gives k=15. The frozen cofacial normal
form and degree theorem give a simple disk with chordless original ordered
boundary B, triangular inner faces, boundary degree at least four, and interior
degree at least five. These are global-minimum-source hypotheses. No
edge-critical, N2, excess-two, Gallai, or collar hypothesis is added.

## Complete finite domain

In the actual exterior face of G add a new vertex z joined to exactly the five
original boundary vertices. The result is a simple sphere triangulation S with
21 vertices, 57 edges and 38 triangular faces. Every degree is at least five,
and z has degree five. Conversely, delete any degree-five vertex of any such
sphere, retaining its five cyclically ordered original neighbors as B. The
result has 20 vertices, fifteen interior vertices, 52 edges, one specified
pentagonal face and 33 triangular faces. Its B vertices have degree at least
four and its other vertices degree at least five.

The converse domain can contain sources which fail other minimum-source
conditions. They are all retained. In particular the generation and coloring
checks use no h, C8, chord, private-rank, or relation-mask pruning.

The published minimum-five construction underlying the frozen plantri 5.8
source supplies every embedded isomorphism class of S. Every degree-five root
of every generated representative is retained. Any embedding isomorphism from
an original coned source sends z to one retained root, and the ordered original
B to one of its ten cyclic starting-point/direction frames. This transports
the whole graph, edges, rotations, directed faces, pins and colorings together.
No independent normalization of pieces is used. Thus the finite domain covers
every possible fifteen-interior-vertex minimum source.

## Relation obligation and conclusion

For each root, compute all complete lifts of each of the ten literal boundary
rows, preserving empty fibres. An independent propagated-domain solver works
from the original sphere labels; the common whole-graph map is applied only
after it returns its full lifts. Exact list equality, together with topology
and root-coverage checks, supplies the finite relation obligation.

If every resulting complete relation belongs to K, the assumed minimum source
cannot occur. Along with the existing witnesses this proves

    K_{<=15} = K_{<=5} = K132.

The machine result and complete data are recorded separately in `REPORT.md`
and `summary.json`. Zero realized 933/941 sources alone is not the proof:
coverage of the entire source domain and full relation checking are necessary.

## External and computational trust

The generation authority is Brinkmann--McKay's minimum-five construction,
[Construction of planar triangulations with minimum degree 5](https://users.cecs.anu.edu.au/~bdm/plantri/min5paper_sc.pdf),
Theorems 1 and 3 and the corrected proof of Theorem 2. The second entrypoint
uses their minimum-four construction from
[Fast generation of planar graphs](https://users.cecs.anu.edu.au/~bdm/papers/plantri-full.pdf),
Section 2, Figure 6, with a degree-five test only at output. It does not prune
generation recursion. These routes share part of plantri's implementation and
are not claimed to be separate verified implementations. The precise imported
theorem and code boundary is frozen from the K13 completeness report.

The accepted upstream K14/normal-form results retain their own dependencies,
including the earlier Dvorak--Lidicky counting result and the universal screen.
This audit does not extend that paper's strict fewer-than-thirty bound, does
not replay its computational proof, and adds no Lean theorem. General
K_infinity=K132, sixteen or more interior vertices, and arbitrary-size
933/941 source exclusion remain open.
