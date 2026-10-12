# Independent check

This sub-audit reads only frozen inputs and does not import the main checker.
`python review/independent_join.py --check` independently reconstructs all 24
global colour renamings of every accepted cap row, then tests all ordered
`(x,y,z,v)` assignments in the fixed original boundary frame.

The 17,424 ordered cap pairs yield 66 distinct output relations, all in the
frozen 132-relation catalogue. Their complete interface joins contain 657,432
tuples in total. `independent_join.json` records every pair's output mask, ten
row tuple counts including zeroes, output histogram and a digest of the ordered
complete joints. The main certificate must separately supply full literal
graph fibres and literal embeddings; this smaller independent file does not
claim to replace those obligations.

The distinct output masks have frozen minimum-representative interior-count
distribution `{0:6, 1:6, 2:16, 3:17, 4:11, 5:10}`. Actual glued literal graphs may
have 14 interior vertices, so the membership result uses direct catalogue
lookup, never the twelve-interior-vertex bound.

## Topology conditions reviewed

For the stated conditional source, the five triangular faces incident to the
degree-five interior vertex form a closed disk with simple boundary
`(a,x,c,y,z)`. Simplicity follows from distinct neighbors in a simple graph.
The required orientation is an explicit restriction of Task C: its complement
inside the original outer disk has disk closures `(a,b,c,y,z)` and
`(a,x,c,d,e)`. Their interiors are disjoint; their closures meet only at `a,c`.
Jordan separation prohibits an edge with endpoints in the two different open
cap regions. Every original interior vertex outside the center disk belongs to
one cap, giving the exact count `k(G)=k(P)+k(Q)+4`. This argument is conditional
and does not claim an actual minimum outside-catalogue source was found.

The representatives can have an `ac` chord even though the original outer
boundary is chordless. Exactly seven frozen representatives have this chord:
`424,440,632,960,976,1000,1016`. Thus 49 ordered pairs create two embedded `ac`
arcs before simple-graph reduction. Both arcs lie in their own cap disks; they
do not pass through the center disk. Deleting one whole embedded arc, while
retaining the other arc in its original sector, preserves all colourings and
the degree-five star rotation. Identifying the arcs as geometric objects is
unnecessary and would need a separate argument.

A planarity check that freely re-embeds the abstract simple graph would not by
itself certify the intended cap sectors and original star. The main checker
should construct a rotation by substituting cap faces into the named skeleton,
then splice the two incident faces when deleting the selected duplicate edge.

Status of this independent fixed-frame relation check: `triggered and holds`.
Status of an actual minimum outside-catalogue source: `not triggered`.

## Main implementation and paper review

Reviewed `controls/checker.py` at SHA-256
`c6599b40b7a098c54f0bfb1692235f76bdf6e982396695abc399cc9129279b9a`
and `paper/PAPER.md` at SHA-256
`03dd93fa5533812572a12b5df151c1e78465c0c329758be0cb31d23fd5a42fd5`.
No mathematical or implementation correctness blocker was found.

The primary cap fibres explicitly list all 240 proper actual boundary
assignments, including empty private-colouring arrays. Each joint block fixes
the same `a,c` colours, all `x,y,z,v` colours, and two fibre indices. Expansion
takes the entire Cartesian product of both private-colouring arrays. Thus the
encoding retains all full colourings and cannot combine incompatible marginal
choices. Every original outer row is explicit. The independently implemented
whole-graph MRV search keeps all four initial colour choices, removes only
colours of assigned adjacent vertices, restores changed domains after each
branch, and saves every completed colouring. Exact sorted-list comparison,
rather than existence or a digest alone, establishes equality with the product
expansion in the main checker.

The main rotation construction substitutes each cap's full interior face set
into the named skeleton. Its dart corner successors form one cyclic rotation
at each vertex. The cap, unsimplified composite, and simplified graph each
receive the relevant sphere Euler checks. Removing the redundant `Q` chord
deletes its two darts; it does not move the retained `P` chord or star.

`python review/compare_certificate.py --check` is a separate standard-library
replay that **does not import the main checker**. Its recorded outcome is
`compare_certificate.json`. It verifies:

* Every one of 17,424 pair masks and all ten row tuple counts agrees with the
  independent fixed-frame join.
* The complete ordered joint digest agrees:
  `92f81a2f8858ab8aad55a189ffbaeb901efbcf6575286be954e7cbfc46ea82b3`.
* Each literal simple edge set equals the independently mapped frozen cap
  edges and fixed star skeleton, with no unidentified private vertices.
* All 17,424 stored rotations have exact incident darts, connected graphs,
  Euler characteristic two, the designated outer `B` face, center rotation
  `L`, and all five oriented star triangle faces. Their stored face lists
  equal independently traversed dart orbits.
* Exactly 49 records simplify the duplicate `ac`, each preserving the `P`
  arc and deleting the `Q` arc.
* All 150,158 accepting-row literal whole-graph witnesses have the prescribed
  outer colours and satisfy every literal edge; empty rows have no witness.

The reviewed main certificate SHA-256 is
`2b4b956d10a39cb91ee44f41fccde880eed1d1bf17981de87d67386aa177ba3d`.

The paper's crosscut decomposition keeps the original source rotation and
gives all bridge and attachment ownership. Its induced-link argument uses the
frozen source's separating-triangle exclusion; the bounded triangle side
cannot contain an outer-boundary point. The exact count `p+q+4`, use of global
minimum interior count for each original cap, and full-lift constructions in
both directions are sufficient for the stated conditional exclusion. The
paper explicitly handles restriction to a cap whose duplicate `ac` was
deleted: the retained `P` arc still enforces `A != C`. It neither claims
equinumerous old and new fibres nor uses the twelve-vertex bound at fourteen
vertices. Its stated OPEN residuals and `not triggered` source status remain
appropriate.
