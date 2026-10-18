# Independent review of C and integration of the four-query interface

Reviewer A; 2026-10-18; frozen BASE
`9f1fe84f73aabfa87a33d28754633bae6bf0b707`.

Reviewed `C/PROOF.md`, `C/check.py`, `C/controls.json`, and integration
`REPORT.md` sections 2 and 5. Verdict: **PASS within the stated scope**.

## Mathematical checks

1. C1 uses full components of `D-(M intersect R)`. Every cut edge is a common
   unchanged matching edge, and no old or reference complementary cycle crosses
   a region boundary. Thus selected whole regions can be exchanged independently;
   full oddness decreases by exactly the sum of their old odd-cycle counts.
   The latter counts are even because every region is also tiled by even
   reference cycles. This is the correct use of complete complements.
2. C2 is an exact equivalence for these region operations. Over F2, membership
   in the span of zero-gain syndromes is realized by a subset, so a dependence
   among positive-region images supplies an actual zero-syndrome positive-gain
   batch. Conversely every such batch gives a nontrivial dependence. The
   dimension bound correctly uses the image of A and subtracts the zero-gain
   span. It bounds regions, not the number of odd cycles or graph size.
3. C3's pairwise vertex-disjointness is sufficient even for different references:
   unchanged boundary matching edges separate all affected complementary cycles.
   At an odd joint minimizer, every e-preserving reference's unique positive
   region contains every old odd cycle. Therefore two positive regions from
   such references cannot be vertex-disjoint. This correctly blocks the proposed
   automatic use of cross-reference whole-region repair.
4. The source family has independent equations `chi_e=1` and
   `chi_f+chi_g=1`. When R preserves e, all available syndromes have zero first
   coordinate, so the effective rank is at most one. Existing XOR batch
   connectivity and the original one-blocker theorem are explicitly acknowledged
   as prior work, not counted again as new source exclusions.
5. Exactly two old odd cycles need not make the complete exchange graph
   connected if there are additional old even cycles. C correctly separates
   the parity fact (the two odd cycles are in one region) from connectedness
   when the two cycles span the graph. A's initial ambiguous phrase was corrected
   after B's review to say exactly two complete complement cycles, both odd.

## Independent replay and finite authority

I executed `python3 -B C/check.py` from its absolute audit-relative path,
parsed its stdout independently, and compared the entire resulting JSON with
stored `C/controls.json`; equality passed. Results:

* 12-vertex graph: 8 perfect matchings, 3 even references, 24 pairs and 48
  whole-region batches; exact parity, gain, syndrome and quotient-rank tests pass.
* 24-vertex connected simple cubic graph: 32 perfect matchings, affine family
  size 4, exhaustive global minimum oddness 4; the exhibited reference has two
  gain-2 regions of independent syndromes 1 and 2.
* One-region concentration controls have 4, 6, 8, 16, 32 old odd cycles and
  12, 18, 24, 48, 96 vertices respectively. The paper construction covers all
  even Hamiltonian cubic base orders; finite checks only calibrate five cases.
* Using the odd reference R=M triggers the intended parity-premise rejection.

The 24-vertex example proves sharpness for C2's general affine setting, not for
the literal source equations or an actual U319 source. C states this distinction.
The infinite concentration construction does not assert that its old matching
is a minimum of a source family. No source existence or positivity follows.

## Root REPORT sections 2 and 5

The finite four-query statements match A's exhaustive certificate: one accepted
row, three rejected rows, 64 compatible raw masks, minimum scope counts 5/2/1,
and witnesses 774/564/960/165 upon dropping individual queries. The reported
minimum applies to coordinatewise acceptance/rejection tests only.

The smaller-source use is valid because no4ct minimality ranges over all disk
sources outside K132. The replacement can leave the r6/319 class and change the
other six rows, provided it is one legal completed graph, accepts 01232, rejects
all three specified rows, and has strictly smaller completed interior size.
The report retains these conditions and the existing W5 five-quotient no-go.
It does not claim an actual replacement, terminal matching, or parent closure.
