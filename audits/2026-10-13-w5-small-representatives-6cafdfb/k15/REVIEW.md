# K15 prerequisites and W5 application

2026-10-13. Parent BASE `6cafdfb02fe5892a49eee21f92aea2369a25c022`.
This review writes only this exclusive `k15/` directory. The screenshot was
not attached; the checked authority is the repository's K15 entry, frozen
parent K15 REPORT/PROOF, its original immutable checker/certificate, and the
normal-form proof. No original certificate, shared document, Git object,
commit, or push was changed.

## Exact theorem domain

The accepted theorem is `K_{<=15}=K_{<=5}=K132`, for finite simple graphs
embedded in a closed disk with the fixed five distinct ordered original
boundary vertices B forming the specified C5. All nonboundary vertices lie
strictly inside; nonboundary edges lie inside except at endpoints. Boundary
chords are permitted. The relation is the complete ten-row proper four-color
extension support, with only a common global S4 color permutation quotiented.
Empty fibres are part of the complete relation.

Connectedness, 2-connectedness, an induced/chordless outer B, triangular inner
faces, boundary degree >=4, and interior degree >=5 are **not premises imposed
on every input disk or representative**. They are derived for a hypothetical
counterexample chosen by minimum interior order among **all** catalogue-outside
sources, followed by maximum edge count. K14 then forces its order to be
exactly fifteen. The root-deletion finite domain can be larger than that
minimum-source domain; possible boundary chords are retained and harmless.
No edge-critical, N2, excess-two, Gallai, collar, private-rank, or fixed-mask
premise is imported.

Adding a cone vertex outside B produces an order-21 minimum-degree-five
sphere triangulation. All degree-five roots of all 192 generated embedded
classes, together with every common D5 frame, cover the possible minimal
sources. Deleting every such root and checking its complete relation proves
the upper containment. Existing <=5-interior disk witnesses prove the reverse
containment. This is not an enumeration of every arbitrary <=15-interior disk.

The theorem retains the accepted K14/normal-form/degree dependencies, the
upstream Kempe and exterior compatibility screen with 4CT, the earlier
Dvorak--Lidicky external bound, the published plantri generation theorem and
the frozen plantri/Python implementations. This review did not replay the
375,126,827-candidate minimum-four generation or prove those imported theorems.
No new Lean theorem is supplied.

## Catalogue witness contract

The frozen catalogue has 132 masks, each with a concrete simple apex-planar
ordered-B disk witness and at most five interior vertices. It includes
boundary-chord witnesses; the 132 stored witnesses include 30 with B chords
(25 with one chord, 5 with two). Thus neither `K132` nor membership in it means
that its stored witness has induced B. The normal-form finite checker verifies
all ten rows of each witness and its apex planarity; K15's main replay checks
catalogue identity and all root masks, and does not independently reconstruct
all catalogue witness embeddings.

A catalogue disk witness supplies B and its complete Sigma. It does **not**
supply the five distinct U pins, their induced ordered C5, an empty inner U
face, a named center v, an annulus rotation/ownership contract, or all B/U
three-color support R^3. It therefore cannot be silently reinterpreted as a
same-slot W5 annulus representative. Any construction adding that interface
must separately certify its legality and Sigma preservation.

## Correct application to a legal representative

Let A' be a legal same-slot annulus with distinct boundary rings B and U,
r' private vertices, and no hidden interface vertices. Add a new center v
in the empty U face and exactly the five edges vu_i. If the resulting G' is
a finite simple ordered-B disk, then

    |V(G') \ B| = 5 + r' + 1 = 6 + r'.

Consequently `r'<=9` gives `6+r'<=15` and hence `Sigma(G') in K132`.
If the preservation theorem gives **complete** `Sigma(G')=Sigma(G)`, this
also places Sigma(G) in K132. Equal coloring counts are unnecessary. A proof
of `R_A^3=R_A'^3` is a stronger sufficient condition, not a prerequisite for
using K15. Representative degree floors, triangular inner faces, minimality,
and source private-rank restrictions are also unnecessary for this step.

For a globally interior-minimum catalogue-outside source G containing a
fully internal W5, K15 already gives k>=16 and r=k-6>=10. Thus `r'<=9`
automatically gives r'<r. More generally, **any** legal same-slot replacement
with complete Sigma equality and r'<r contradicts this global source
minimality, even if r'>9 and K15 is unavailable for G'. For an arbitrary
nonminimal input, r'<=9 alone does not guarantee strict shrinkage; r'<r must
be checked separately.

## Actual replay

`run.py` executes the original read-only main and independent comparison in
normal and `PYTHONHASHSEED=17` environments. All four commands returned zero.
Their exact argv, cwd, elapsed times, output hashes, and output are under
`logs/`. Each implementation's normal/seed17 stdout is byte-identical.

The replay recomputed 192 sphere classes, 2,714 roots, 27,140 literal rows,
and all 624,617 complete coloring lifts. Every rooted complete relation is
1023. The independent original-label propagated-domain solver agrees with
every complete saved fibre after the single whole-graph vertex map. Main
full-fibre payload SHA256:
`24e3e89af3d800fcc84128ad90304d9797f21d967429b358f16b3c1e725c465d`.
The two preexisting planar_code streams have equal complete embedding sets;
generation was not rerun in this review.

## Residual obligations

K15 supports the **conditional consequence** of a legal r'<=9 representative.
It does not construct one for arbitrary annuli, does not give an arbitrary
annulus R^3 compression theorem, and does not prove general nine-private-vertex
representative existence. Those claims remain OPEN. General >=16-interior
catalogue-outside sources, arbitrary-size 933/941 source exclusion, and
`K_infinity=K132` likewise remain OPEN. The actual 933/941 minimal source is
`not triggered`; its absence from this finite sphere domain is useful only
through the complete minimum-source coverage proof.
