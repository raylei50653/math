# C8 no4CT independent review

2026-10-13. Scope: the same globally minimum-interior C5 source outside the
fixed 132-relation catalogue K, then maximum edges. All mathematical input
artifacts are frozen under the parent audit. This reviewer wrote only `review/`.

**Conclusion: the bounded cofacial repair is sound; the complete C8 dependency
chain can be adopted for this minimum source without assuming 4CT.** The
unrestricted cofacial-colourability theorem in the old report is not adopted.
All three unbounded source branches and the main proposition remain OPEN.

## 1. The crucial bounded implication

Let the original source have k interior vertices. The frozen no4CT dependency
report's Lemma A establishes, without 4CT, that a non-four-colourable planar
graph on at most N vertices produces a C5 disk of complete relation 932 with
at most N-6 interior vertices. The proof takes a vertex-minimum noncolourable
plane graph, triangulates on the same vertex set, excludes degrees at most
four by deletion/planar identification, and deletes an Euler-guaranteed
degree-five vertex. Smaller-graph colourability comes from that graph's
minimality. The complete relation 932 follows from the stated Kempe fact, or
from all five nonadjacent-neighbour identifications. No colouring theorem for
arbitrary planar graphs is assumed in this argument.

If any planar graph on at most k+5 vertices were noncolourable, Lemma A would
produce a 932 disk with at most k-1 interior vertices. Since 932 is outside K,
this contradicts the original **global** minimum. Consequently every planar
graph on at most k+5 vertices is four-colourable, conditional on this fixed
minimum source. It would be invalid to minimize only among sources of the same
mask: the descending source may belong to a different branch.

The original C8 inner disk H contains exactly all k original interior vertices.
For two distinct nonadjacent cofacial H vertices, add one exterior arc and
contract it. The simplified planar quotient has k-1 vertices and no loop.
The bounded implication therefore colours it. Pulling back produces one full
colouring of the same original H with both named vertices equal. All original
edges and a single global colour frame survive the pullback. No boundary
colour is prescribed in advance, and no claim of a degree-preserving quotient
is needed.

For an independent noncrossing partition pi of the induced original C8, its
blocks can be joined by mutually disjoint exterior trees using the original
boundary vertices. The quotient has exactly k-8+|pi| vertices, at most k, so the
same bounded implication applies to every one of the 91 partitions. Original
edges cannot become loops because each block is independent. Distinct blocks
may receive the same colour. This proves positivity of the **sum** of complete
equality fibres, not positivity of every row and not nonnegative equality
expansion coefficients.

This is a source-relative theorem for every finite value of k. Omitting its
size/minimality premise would reinstate the old 4CT dependency.

## 2. Cap and degree checks

For a C4 or C5 cycle wholly inside the original B, let s count the strict
interior of its chosen disk side. Its cycle vertices themselves are original
interior vertices, so s<=k-4 or s<=k-5, respectively; in particular s<k. The
restricted no4CT C4 representative lemma therefore applies, and the C5
relation belongs to K by global minimality. Complete literal boundary
relations permit replacing the cap by at most three or five interior vertices.
This preserves the whole original B relation, including rejection rows and
empty fibres. It does not preserve extension counts or require any new graph
to retain the old degree/saturation properties.

Original vertices strictly inside a cap have no neighbours on the other side
of its Jordan boundary. Their cap degrees equal their degrees in G and are at
least five. The Euler/outerplane argument then makes C4 caps empty and C5 caps
empty or W5. Absence of occupied C3 uses an existing full colouring of the
same original G, available also in branch 932; it does not need nonempty
singleton support P. These facts imply induced C8 with the original five apex
degree bounds and three private-point degree bounds exactly as in the frozen
geometry proof.

The two quotient exclusions use the original pair (a1,a4): positions (3,7) in
c16-941 and (1,5) in c32-941. In each case all 74 proper normalized equality
rows lie outside the complete necessary upper. Thus the full H colouring just
obtained cannot exist. This excludes the whole query, even when the true
source support is a strict subset of the upper.

## 3. Independent finite reconstruction

[check.py](check.py) imports no producer module or previous checker. It directly
enumerates all 65,536 C8 colour words and all 1,024 C5 words, obtaining 6,564/274
proper literal/normalized C8 words and 240/10 C5 words. Restricted-growth
partitions give 4,140 partitions, 1,430 noncrossing partitions and 91 independent
partitions. All equality row sets and all 910 frozen upper intersections are
recomputed; the two excluded queries have nine empty intersections each, and
all 91 intersections also remain nonempty for each of the eight refined
residual uppers.

For each proper C8 word and each complementary colour split, the script freshly
enumerates the noncrossing monochromatic-component partitions, enforces every
same-group boundary edge, and swaps every component subset. It then constructs
all 35 literal collars with sum(t)=3, enumerates every complete B+C8 annulus
fibre including empties, and iterates its own boolean necessary-closure
algorithm for 932, 933 and 941.

Comparison with the new producer covers every full annulus fibre, all column
masks, all component-swap orbit masks, all 105 initial/final supports and outer
unions, all accepted-row preimages, and all 95,900 transfer coefficients. The
transfer-count check explicitly handles the alternating C8 orbit of size 12;
other proper C8 orbits have size 24, as do all proper C5 orbits.

All 35 new 932 queries are excluded. Thirty fixed points are empty. The five
pure-placement cases `(0,0,0,0,3)` and its rotations have 100-row fixed points
whose complete transfer image is empty. These nonempty fixed points cannot
produce any of the five required 932 outer rows. No actual source graph was
generated, and no zero-source sample is used as exclusion evidence.

The finite producer separately replays the three old common-count exclusions
and fixed-split counts. This review checked their no4CT proof dependencies; the
independent script does not claim to rederive their exact rational certificates.
The final accounting is 92 transfer/Kempe exclusions, three common-count
exclusions and two bounded-cofacial exclusions, leaving eight of 105 queries.

## 4. Downstream adoption and precise bounds

The frozen apex proof uses the same full H extension counts: at a degree-three
apex, the three counts are z1+z2, z1+z3, z2+z3, with repeated normalized indices
retaining multiplicity. The subsequent support pruning and two exact rational
certificates use signed equality span and nonnegative reversible Kempe orbit
weights, followed by positivity of an accepted original outer row. There is no
additional 4CT existence step once the eight-query upper is repaired.

The frozen short-crosscut/m=9 proof and peeling/m=10 proof use the repaired
original C3/C4/C5 cap facts, induced C8, actual triangular faces, and degree
bounds. Their finite colourings belong to the complete small graphs forced by
the paper classifications. Thus they transfer without changing any original
attachment or full fibre. With their recorded replays, h=3 implies k>=19 for
the new minimum-source contract. The first peeling classification and general
full-fibre separator recurrence also transfer, but fixed C8 width and repeated
inheritance of the initial degree/contact hypotheses do not follow.

There is a separate branch-specific improvement: 932 already has h>=3 from
the previous audit, and all h=3 collars are now excluded, hence 932 forces
h>=4. The exact original curvature identity

```
n5 = 6+h+sum_{original interior v, d(v)>=7}(d(v)-6)
```

gives n5>=10 in this branch. The common bounds remain h>=3 and n5>=9 because
eight 933/941 h=3 contracts remain. General k>=16 is unchanged; h=3's k>=19
does not apply to h>=4. Nothing here excludes unbounded 932, 933, 941, realizes
a residual necessary vector, proves the main proposition, or adds a Lean
theorem.

Commands and output hashes are in [VERIFICATION.json](VERIFICATION.json).
