# A cross-review of the integrated marked-six argument

Reviewer: the independent A cap/sector worker. Frozen authority is the parent
`INPUTS.json` at BASE `6c420f3ca77d60952ed76f93dff7449c522715ca`.
Review scope: root `PROOF.md`, especially §§1–3. The separately written
`A/PROOF.md` reconstructs both boundary caps without using the integrated
argument as authority.

## Root §§1–3

No mathematical gap was found in these sections. The following points are
the substantive checks, rather than finite-data implications.

1. **mp/mq identity.** The common-neighbour theorem is sufficient: pz and
   qz are edges of the actual face z-p-q, so mp or mq makes the corresponding
   terminal a common neighbour of m,z. There are only alpha,beta, and a/c
   fan disjointness excludes assigning p to beta or q to alpha. The endpoint
   identities then force a0=4 or c0=4. No v5-only adjacency assertion enters.
2. **Proper original cycle.** An ordinary J midpoint is a retained original
   inner vertex, distinct from all absorbed/deleted vertices; it cannot
   coincide with t in Q_a or s in Q_c. Both proposed caps therefore are
   simple original C5s meeting the exterior boundary at exactly one vertex.
   They satisfy the strict smaller-source comparison: four original inner
   vertices already lie on the cap interface, so the cap has at most k-4
   private original vertices.
3. **Actual bounded sector.** At a, the facial wedges yat and abp and the
   original exterior wedge fix the outside arc. Every remaining a ray is
   between at and ap on the bounded side. Thus an ah chord, if present,
   also lies in the bounded cap; it cannot escape the W5 no-chord result
   by being drawn outside. The c,x,s,q,b calculation is the same direct
   argument at c, in the same original graph.
4. **Both cap types.** Empty caps give at most the midpoint as a fifth
   neighbour. Single-centre caps give exactly five neighbours because their
   boundary chord is forbidden. The integrated proof uses the full W5
   conclusion, avoiding the erroneous bound six that the weaker “at most
   one interior vertex” statement would permit.
5. **Complete six-cycle partition.** Removing two disjoint marked edges
   from a simple six-cycle leaves two disjoint paths. All four forbidden
   cross edges make each path have length at least two; hence exactly two.
   The two displayed terminal pairings exhaust the possibilities, their
   midpoints are distinct, and z cannot be a midpoint. Pairing I is therefore
   excluded by a0+c0>=11 with no unstated degree restriction.

## Remaining integrated sections

The two-star disk used in §4 is the actual disk in the frozen geometry §5,
including alpha=p or beta=q. Alternating boundary endpoints exclude two
vertex-disjoint paths in that disk even if a midpoint lies on its boundary:
the finite disjoint paths have disjoint neighbourhoods and their nonendpoint
boundary contacts can be moved into the disk. Both exceptional cap
calculations then use actual original vertices and the fixed outside link
segment at p or q. In particular c0>=7 in the mp case excludes tq, and
a0>=7 in the mq case excludes sp. The two missing diagonal sets and their
five-neighbour conclusions are correct. No reflected support or v5 theorem
is required.

The §5 cut-to-bond step also preserves the necessary hypothesis that both
cut sides contain cycles. A cycle-bearing component has at least four exit
edges because its complement contains a cycle and a three-edge cut only
isolates a vertex; a further same-side component costs at least three more.
For a cut of size at most six neither side can be disconnected. The planar
bond dual is then a simple J cycle containing the two actual primal marks.

This review establishes no matching-oddness descent. The separate marked
alternating-cycle condition in §6 correctly preserves e and changes f,g
together when starting inside P110 union P101; that identity alone places
no bound on the number of odd complement cycles.

## B paper and checker cross-review

`B/PROOF.md` was also read after its completion. Its §§2–6 agree with the
independent cap bounds and the integrated argument. In particular it does
not use the rejected old crossed-pentagon lift: pairing I is removed by
the different original boundary cap, and its two pairing-II caps use t
or s only after the actual mp/mq geometry places both corresponding rays
in that original sector. The exterior p/q link segments are full facial
segments, so no additional uncounted exterior neighbour remains.

The B checker separately enumerates both labelled connector pairings,
allows all four alpha=p/beta=q endpoint combinations, and reconstructs
the p/q links by gluing actual cap triangles to the three fixed exterior
faces. Its graph of each reconstructed link is connected and 2-regular
on exactly five neighbour labels. This is an appropriate local calibration
of the paper degree calculation. The checker explicitly attributes the
Jordan theorem, actual sectors and arbitrary-size coverage to the paper;
its zero genuine source instances are correctly labelled not triggered.

No missing connector case, unsupported source reflection, or circular use
of v5 was found. This conclusion is limited to the marked-six theorem and
its cyclic-cut corollary; the absence of a general oddness-descent theorem
remains material and is correctly retained.
