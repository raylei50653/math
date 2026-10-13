# Independent final paper review

2026-10-13. Reviewed the parent `REPORT.md` and the canonical
`docs/c5_neartri_boundary_collar.md`, including the stronger cap conclusion.
No shared document was edited by this reviewer.

**Mathematical verdict: PASS for finite simple (equivalently here, loopless)
disk graphs.** The direct count-and-transfer argument excludes the remaining
941 h=2 source. The existing fan cap and 4CT additionally exclude every full
disk-C7 relation contained in U. The quantifier is over arbitrary interior
size, not a bounded graph census.

## Independently checked evidence

- The preserved named C7 is `(a0,a1,y2,a2,a3,y4,a4)`; its actual attachments
  are `({b0,b1},{b1,b2},{b2},{b2,b3},{b3,b4},{b4},{b4,b0})`. These agree with
  the frozen outer transfer for extras `(0,0,1,0,1)`.
- Each x_p counts extensions of one fixed literal boundary assignment under
  the same literal four colors. It is not an orbit total. All coordinates
  refer to the same H. Global color permutations give the needed bijections
  when passing between literal assignments and stored representatives.
- Inclusion-exclusion gives the stated factor `(-1)^|F| 4^k0(F)`. Components
  meeting the boundary contribute one forced color if the boundary word is
  constant on their block and zero otherwise. Disjoint components induce a
  noncrossing partition in a disk. No positivity is required for these
  expansion coefficients; positivity is used only for actual x_p.
- `joint/count_identity.py --check` passed: all seven exact identities are
  checked against all 429 noncrossing partitions. There are 36 active
  columns, 91 proper rows, and rejected-row rank 31. The first four
  identities force indices 42,49,73,75 to zero under U. The last three give
  `x6+x35=0`, `x58=x6`, `x89=x6`. All their right-hand rows lie outside U.
- `topology/count_review.py` passed its independently generated 429
  partitions, all seven identities, and the recomputed transfer preimages
  `[6,58,89]` of required outer `01232`.
- `caps/independent_verify.py` passed all 91 transfer rows, 273 independently
  reconstructed Kempe split obligations, all 3,383 literal caps and 307,853
  fixed-row queries, and the qualified row42-forcing chains.

## Stronger fan argument

The reviewer separately recomputed the relation of the literal fan having
the C7 edges and chords `(0,2),(0,3),(0,4),(0,5)`. The mask is exactly
`2339273691857418867305349120`, containing 16 of the 91 rows. Its intersection
with U is exactly index 89, word `0123231`. The same literal fan is already
present in the frozen cap catalog, with seven vertices and precisely those
eleven edges.

Embedding this fan in the opposite disk and identifying the seven original
boundary vertices gives a planar graph. If H already has a fan chord, any
duplicate parallel edge can be suppressed without changing proper
colorings. For a finite loopless graph, 4CT gives a proper coloring of the
union. Its common named boundary row belongs to both full relations, hence
must be row89 if the relation of H is contained in U. Thus x89 is positive,
contradicting the certified zero. This proves that U contains no complete
relation of a legal disk-C7 source, rather than only excluding equality
S=U or only excluding transfer=941.

## Scope and wording findings

The paper separates direct transfer exclusion from the stronger conclusion
that additionally invokes 4CT. It retains general h>=3, sources above the
old finite vertex cutoff, and K-infinity=K-at-most-5 as OPEN. Raising h and
the Euler consequence n5>=9 applies only to the stated minimal/maximal
normal form. No Lean formalization is claimed.

Four small wording corrections were sent to the parent for its shared-doc
edit pass:

1. Make "finite simple" or "finite loopless" explicit in the strongest
   universal graph quantifier. Loops would invalidate 4CT; the actual source
   convention is already simple.
2. Include the new common count restrictions in the canonical table's
   provenance; Kempe closure alone left the h=2 case.
3. Qualify the canonical doc's row42 Kempe forcing by the hypothesis
   `transfer=941`, since the chains start from required outer `01232`.
4. Restrict the standard-library dependency statement to the core count/cap
   replay scripts; optional topology controls use NetworkX.

No use of the withdrawn exploratory V9 claim appears in the reviewed
reports. It was never written into a certificate or proof. The valid
identities use exact Fraction coefficients, assert denominator one before
integer conversion, and are verified again on every partition; they are
unaffected by that discarded exploration.
