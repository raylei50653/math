# A. Actual switches, complete oddness surgery, and the marked influence component

Frozen BASE `5b9a7b3190c84bc10ff99608e372a9b4be57a0f6`, 2026-10-17.
This is an arbitrary-size conditional paper result in the exact source,
with a separate finite control. It does not exclude all nonfacial seven-defects.

## 1. Contract and the one forbidden difference cycle

Keep the original minimum no4ct C5 source, original ordered contacts,
rotation, attachments, complete U319 fibres including empties, and every
original r lift. All matchings below live in its actual
`D=(U/(s=t))*`; the literal marks remain
`e=(vw)*`, `f=(pq)*`, `g=(mz)*`. The frozen source-supplied M0 is a complete
even-complement 111 matching, as established by frozen
`2026-10-16-r6-319-complete-e98a1cc/B/PROOF.md`.

Let `M in F_e=P110 union P101` and `F=D-M`. Write h for the mark omitted
by M (g in direction110, f in direction101), and k for the other mark
among f,g. Then e,k belong to both M and M0, while `h in M0-M`.
The actual difference `M triangle M0` consists of vertex-disjoint
alternating cycles. Exactly one, called H, contains h. Every difference
cycle avoids e,k. Thus for a batch of these actual cycles:

`M triangle E(batch) in F_e` if and only if `H is not in batch`.

This follows directly from the adopted XOR mark criterion. A difference
batch toward this fixed 111 witness keeps the initial joint direction;
the general joint exchange criterion also allows direction changes, but
such changes are not supplied by these particular difference cycles.

## 2. The actual cap path and its unique difference cycle

Let C be a nonfacial seven-component of F. Its adopted classification
gives exactly one internal M chord and five M spokes constituting the
actual cyclic five-cut `B_C=delta(V(C))`. Label the cap, only for this
local proof, by cyclic order `C=(0,1,2,3,4,5,6)` and chord03. The ports
are 1,2,4,5,6. This relabelling is an isomorphism of the actual cap; it
does not rename original marks or replace any exterior witness.

Perfect-matching cut parity gives `|M0 intersect B_C|` odd. The value5
would force chord03 in M0 and leave C as a complete odd component of
`D-M0`. Therefore the value is1 or3. In the present value3 subcase, let
u,v be the two ports whose spokes are omitted by M0.

There are exactly the following six possibilities compatible with the
even complement of M0. Each row retains the other three actual spokes.

| Changed ports u,v | Internal M0 edges | Complement inside the cap |
| --- | --- | --- |
| 1,2 | 03,12 | one 1--2 path of length6 |
| 4,5 | 03,45 | one 4--5 path of length6 |
| 5,6 | 03,56 | one 5--6 path of length6 |
| 1,4 | 01,34 | one 1--4 path of length6 |
| 2,6 | 06,23 | one 2--6 path of length6 |
| 4,6 | 06,34 | one 4--6 path of length2 and one complete even4-cycle |

To verify completeness, remove the three kept port vertices. The four
remaining vertices are 0,3,u,v; enumerate their two-edge perfect
matchings in `C+03`. Pairing 0 with3 allows only the adjacent port pairs
12,45,56. Otherwise pair 0 to1 or6 and 3 to2 or4. The additional case
u,v=1,2 with internal edges01,23 leaves the complete cap5-cycle
`(0,3,4,5,6)` in `D-M0`, so is impossible. The other three pairings are
exactly the last three rows above. This is a local classification of
the given M0, with no independent exterior feasibility claim.

In every row, the part of `M triangle M0` inside the cap is a single
u--v path, of length1 in the first three rows and length3 in the last
three. The two changed spokes are the only difference edges of B_C.
Consequently precisely one actual alternating cycle Q meets B_C: it is
this cap path, the two changed spokes, and one actual outside
alternating path between their outer ends. The other difference cycles
lie entirely outside the cap. In particular, `Q is safe iff Q != H`.
This describes the existing outside path; its length and intersections
with complete old complementary cycles are unrestricted.

## 3. Exact surgery retains every complete outside component

The following is an exact criterion for any Q from section2, regardless
of whether it is safe. Put

`B_Q=E(Q) intersect (M0-M)`, `A_Q=E(Q) intersect (M-M0)`.

Remove B_Q from every entire old F cycle it touches, retaining all the
resulting paths, their actual endpoint labels, and their integer lengths.
The removed edges form a matching, so each endpoint belongs to exactly
one path and one A_Q edge. Add A_Q. The union is exactly the changed
part of `D-(M triangle E(Q))`; every untouched whole F cycle persists.

For each retained path, make an abstract edge labelled by its length
modulo2. Label each added A_Q edge by1. Each resulting component is a
cycle, whose length parity is exactly the XOR of its edge labels.
The same path collection joined instead by B_Q reconstructs the entire
old touched F cycles, again with joining-edge labels1. Hence

`Delta odd = odd(path pairing + A_Q) - odd(path pairing + B_Q)`.

The pairing is from this actual outside graph. Arbitrary independent
boundary pairings or separately chosen marginal parities are not allowed.
This identity follows by partitioning each complete new or old component
into its retained paths and joining edges, and counting its total length.

One can express the seven-cap contribution more directly. Remove the
outside edges of B_Q from the complete exterior F cycles that Q touches.
Let o_ext be the number of those old exterior cycles that are odd. Add
the exterior A_Q edges and the single bridge through the two spokes and
the cap complement path. The bridge has even length (2+6 or2+2).
Let o_new be the number of odd complete cycles in this reconnected
outside-plus-bridge graph. The optional internal4-cycle is even. Thus

`Delta odd = o_new - o_ext - 1`.

Every other exterior F cycle is retained, including remote odd cycles.
Total parity gives `o_new == o_ext+1 (mod2)`, either by counting the
same vertex support or by observing that the replaced cap has odd order.
Therefore the exact strict-descent condition is

`o_new <= o_ext-1`.

In particular, if Q touches only even exterior F cycles (`o_ext=0`),
Q cannot strictly decrease full oddness. It can remove C while creating
another odd component. This is a rigorous obstruction to inferring
descent merely from safe marks and disappearance of the old seven-cycle.

## 4. A larger actual batch gives a stronger all-size criterion

Set `K=D-(M intersect M0)=F union (D-M0)`. Retain its complete vertex
set, including components unaffected by the difference. Every difference
cycle lies in one component W of K. Every old F cycle and every reference
`F0=D-M0` cycle also lies entirely in one W. The components W are
equivalently the actual incidence clusters obtained by joining
difference cycles whenever they touch the same complete old F cycle,
with untouched F cycles retained as separate components.

**Theorem A1 (complete-component safe descent).** For a component W of K,
let A_W be all actual difference cycles contained in W and define
`N=M triangle E(A_W)`. Then

1. `D-N` equals F0 on W and equals F outside W;
2. `odd(D-N)=odd(F)-odd(F[W])`;
3. if W does not contain H, N belongs to the same joint direction as M;
4. if W contains any old odd F component and avoids H, this is a strict
   joint descent of at least2 in full oddness.

**Proof.** Every edge crossing W is absent from K and therefore belongs
to `M intersect M0`. Its endpoints remain matched across the cut, and
it is absent from both complements. Every noncommon matching edge
inside W lies on exactly one actual difference cycle there. Flipping all
these cycles makes the matching equal to M0 on every edge internal to W,
and keeps M outside W and all common boundary matching edges. It follows
that the complementary restrictions are exactly as in1. All complete
F0 components are even, proving2. The only forbidden difference cycle is
H, proving3. Finally W is a union of complete even F0 cycles and has
even order. Since F[W] is a disjoint union of complete cycles on the same
vertices, its number of odd components is even. If positive it is at
least2, proving4. QED.

This is an actual same-graph batch, with no reconstruction cost and no
discarded remote components. It applies to every odd defect, including
the present nonfacial seven-subclass. The strict-descent criterion
requires more than mark safety `Q != H`: even a safe Q may need remote
difference cycles, and an eventual safe repair is guaranteed when its
complete K component avoids H.

**Corollary A2 (where a joint minimizer can be odd).** If M is an oddness
minimum over the joint union, every odd F component lies in the single
K component W_h containing H (equivalently containing the literal h
edge). Every other K component has entirely even F complement. Hence
the present C must lie in W_h.

Otherwise A1 produces a permitted strict descent, contradicting
minimality. In incidence language, there is a chain of actual difference
cycles from Q to H, successive cycles joined through complete old F
cycles. The chain can pass arbitrarily far outside the five-cut.

## 5. The influence obstruction does not yet give the forbidden marked cut

For every component W of K,

`delta(W) subseteq M intersect M0`, `|W| even`, `|delta(W)| even`.

If W is proper and contains C, both sides of this boundary contain
complete F cycles, so the boundary is cyclic. However there is no upper
bound6 on its size and no reason that it contains both e and f. In
direction101, the active mark is f and lies strictly inside W_h, so this
particular component boundary never contains f. In direction110, if
both e and f belong to the boundary, R6-MARKED-SIX only implies its even
size is at least8. If W_h is the whole graph, its boundary is empty.

Thus A2 precisely locates marked influence, but does not manufacture the
required vertex set Y. A proof completing the user target must still
show that the actual C-to-H influence forces another safe oddness-lowering
batch, or explicitly construct a cyclic `delta(Y)` containing e,f of
size at most6. Neither assertion follows from A1/A2 or the local table.
Possible additional exchanges outside `M triangle M0`, including a
110-to101 change, remain available but are not established here.

## 6. Finite controls and evidence authority

The stdlib checker `check.py` freezes the exact BASE bytes of the existing
flipped-icosahedral input graph under `A/frozen/`, with provenance and SHA
in `INPUT.json`. It reconstructs the complete cubic dual, independently
enumerates all38 PMs, retains every whole complementary cycle, and checks
A1 on every component for every M and every even-complement M0. It also
reconstructs every value3 nonfacial seven-cap presentation in this fixed
control. It is a calibration, not source enumeration or source realization.
The active seal is `certificate-v2.json`; `certificate.json` is the
retained initial development seal. Replay, hash-order replay, malformed
certificate rejection and exclusive-create rejection are in
`VERIFICATION.json`.

A second explicitly given plane control demonstrates the necessity of
the outside parity condition. Its old complement cycles are
`(0,1,2,3,4,5,6)`, `(7,8,9,10,11,12,13,14)`, and
`(15,16,17,18,19)`, of lengths7,8,5. Its matching is

`{03,1-7,2-8,4-9,5-10,6-19,11-15,12-16,13-17,14-18}`.

The two disjoint actual alternating4-cycles are
`Q=(1,2,8,7)` and `H=(11,12,16,15)`.
Take `e=03`, `f=4-9`, `g=11-12`, and
`M0=M triangle E(Q) triangle E(H)`. The latter has an even20-cycle
complement and is111; M is110. Exactly three cap spokes are in M0.
Q avoids all three marks, removes the old seven-cycle, and changes the
full complement from lengths7,8,5 to15,5. Its full oddness stays2.
Both difference cycles are in the same actual influence component.
The checker supplies the complete oriented sphere faces, verifies every
edge incidence and Euler characteristic, and reconstructs all complements.
No source contract, joint minimality, or R6-MARKED-SIX hypothesis is
asserted for this illustrative control. It refutes only the proposed
inference from safe Q and cap disappearance to strict full descent.

The arbitrary-size claims are the local exact classification, exact
surgery criterion, and A1/A2. The requested unconditional subclass
exclusion remains OPEN. No new Lean theorem, full319 exclusion, joint
positivity, source instance, or smaller completed bad source is claimed.
