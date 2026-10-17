# B review: accepted exact scope and remaining repair

BASE `3d325d7197aa05815c71bedc52c1b253d736c7bb`.
This independent review covers the user's sections 1, 2 and 5 and the
paper argument in [PROOF.md](PROOF.md). Cross-review status is recorded
in the root integration; this note does not speak for another worker.

## Accepted claims

1. **Universal reference parity.** Every full L_R component is even
   order, since it is a union of whole even D-R cycles, and therefore
   contains an even number of whole odd F cycles. This applies to every
   actual even-complement reference. If exactly two odd F cycles exist,
   they are always together. Extra even F cycles may lie elsewhere.
2. **Two total cycles.** If F has precisely C7 and one other complete
   cycle, that cycle is odd. The universal parity lemma puts the two
   cycles together and they span D, so every such L_R is connected.
   The fixed-M all-distinct reference objective is exactly |V(D)|.
3. **Exact primal count.** The spanning P=M* has n-2 edges and two
   faces, including isolated vertices in the count. Euler yields three
   components and cycle rank one. Actual rim spokes supply the unique
   simple cycle Q5; no remote extra cycle is possible.
4. **Exact component placement.** The binary integration is valid on
   the sphere because every triangular facial sum is zero. Normalize
   Q5 to zero; g=mz and the actual face mvw give m=z=0, v=w=1. The
   complete actual two-star cap makes u,h degree-one vertices in P,
   so they form a whole K2. These facts identify all three components
   without assuming their locations in advance. In particular mz joins
   m to z in the Q5 component and is a bridge rooted at z; vw is a
   bridge in the other tree component.
5. **Reference forest explanation.** A common-edge cycle in S_R has
   constant nonzero primal colour difference and must have even length.
   P's unique cycle has length five. Thus S_R is a forest for every
   even-complement R, and its omitted-edge dual L_R is connected.
6. **Repair obligation.** For actual disjoint M-alternating cycles,
   avoiding e and toggling f iff g are necessary and sufficient for
   the new perfect matching to remain in P101 union P110. A strict
   decrease from exactly two full odd cycles gives zero odd cycles.
   No such alternating batch has been constructed here.

## Failure modes checked

* `two odd F cycles` must not be silently replaced by `two total F
  cycles`. An explicit connected cubic graph with two triangles and a
  square has an even reference whose exchange regions have sizes six
  and four. The two odd cycles co-locate; L_R is still disconnected.
* The even-complement assumption cannot be dropped. On the triangular
  prism, M equals its rungs and R=M leaves two separate odd triangles.
* No argument combines independently normalized source colourings,
  incomplete fibres or local exterior states. Sigma is a derived
  binary assignment on this one J, not a substitute U319 witness.
* A cycle of S_R is constrained by one full R at once. A general even
  cycle of P alone has no claim to a simultaneous source colour class.
* Full Euler and full complement counts retain isolated P vertices,
  remote F cycles and every original vertex. No local repair is
  counted as a global oddness decrease.
* (B3) is a universal obstruction under a conditional subcase. It
  neither realizes nor excludes that subcase in a genuine minimum
  original source.

## Evidence and stop rule

The source facts used are in the frozen active-f B and C proofs and
the sealed prior J geometry file identified in the root INPUTS. The
small controls in [check_controls.py](check_controls.py) check scope
only. Their ordinary and seed-17 outputs agree, and a missing-edge
reference is rejected. No broad source enumeration is performed.

All 13 direct frozen inputs and all 77 previous-inventory files were
independently checked against exact byte lengths and SHA256 digests;
drift was zero. This includes the original literal mvw face authority.

## Integration verdict

ACCEPT the root [PROOF](../PROOF.md), sections 3 and 5, root
[REPORT](../REPORT.md), and the updated Kempe guide's active-f entry.
They distinguish all even-complement references from actual R100
references, and distinguish exactly two odd F cycles (allowing extra
even cycles) from exactly two total F cycles. The additional g-endpoint
condition is retained for the first obstruction; universal L_R
connectedness is asserted only in the second case. The sigma and Tait
four-colour assignments are kept distinct, and the exact three full
P components and mz/vw bridge placements are faithfully summarized.
The repair conditions avoid e and toggle f iff g on actual disjoint
alternating cycles; a strict full oddness decrease from two reaches
zero. The routing explicitly retains the unsolved repair, all source
realizability limitations and global OPEN endpoints. No integration
change is required by this review.

There is no new Lean theorem and no new source realization. The two
complete-cycle repair, the remaining active-f seven-cap, other odd
complements, H-connected cases, `W110+W101>0`, `omega_e=0`, and full319
remain OPEN. Changing R for fixed M cannot solve SEP in the two-total-
cycle subcase; the next authorized mathematical obligation must change
M or independently exclude that subcase.
