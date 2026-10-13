# C9 prerequisites and transfer boundary

Scope: the parent audit's frozen BASE and globally minimal catalogue-outside
source, then maximum edges. These are source-relative statements, not fixed
mask minimality or unrestricted planar colorability.

| Claim | Precise inputs | Conclusion and limitation |
| --- | --- | --- |
| Original C9 and degrees | Frozen collar report; h=4; original rotation and actual faces | Five A have H-degree>=3, four Y have H-degree>=4; H has k total vertices and k-9 strict inner vertices |
| Empty C3/C4; C5 empty or W5 | Frozen C8 geometry §2; restricted C4 cap s<k; truly smaller C5 source | Applies to original caps bounded entirely by original inner vertices; no arbitrary C4 representative theorem |
| One-ear dichotomy | Small caps; original degree bounds; planar noncrossing chords; exactly five A | Induced C9, or exactly one distance-four chord cutting off a literal W5 with three A middle vertices |
| Named ear coverage | Five cyclic A triples; two intervening e gaps zero; remaining gaps sum four | 70 ordered collars; 75 possible (e,chord) interfaces; positions are alternatives, never simultaneously realized ears |
| Literal ear mask | Original chord plus all five center spokes | Endpoint colors differ and short C5 uses exactly three colors; each allowed row has one center lift |
| Residual C6 | Delete exactly three middle A plus the W5 center; retain original long arc and uv | Total vertices k-4, strict inner vertices k-10; induced C6; long-middle A/Y degrees retained, endpoints only degree>=3 |
| Exact B--D join | Original annulus, actual W5 ear, actual residual disk, shared named D and shared uv | Complete fibers, including empties; same-row full lifts glued through literal D colors; no C5 catalogue claim for D |
| Cofacial equality positivity | Source-relative loopless planar colorability at N<=k+5; actual independent boundary blocks | C9 q-block quotient has k-9+q<=k vertices; additional ear chord uv must remain a forbidden equal-color pair |
| Boundary degree budget | Euler plus original A/Y degrees; actual chord count | Exact sum_C(d_H-3)=3m-3-j+c>=h; for induced C9 h<=2m-2; no improvement over inherited k>=16 |
| Finite support/Kempe pruning | Complete original annulus transfer, actual ear mask when present, actual noncrossing Kempe orbits | Necessary relations only; no implication that a surviving support has a common source |

The frozen reports provide paper prerequisites. The new [proof](PROOF.md)
provides the C9 geometry and exact join independently of any finite producer.
Finite counts or query statuses must be read from the parent's current
certificate; this table does not predeclare them PASS.

OPEN: h>=4 arbitrary-size source exclusion, surviving full-relation common
source realizability, general 932 exclusion (which carries the Four Colour
Theorem difficulty), the general catalogue theorem, and Lean formalization.
