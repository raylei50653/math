# N45-S-LONG-S-DIRECT independent paper review

Review date: 2026-10-11. Task A: `N45-S-LONG-S-DIRECT`.
BASE: `f2692089ad4259808e27d9b7e882ac09505b180a`.
Reviewed deliverable: `audits/2026-10-11-n45-s-long-s-direct/REPORT.md` and `claims.json`.

**Recommendation: accept the four scoped arbitrary-size paper exclusions under the exact K1–K12 contract, with original U owner=s and X=G−rb_i itself the same-β minimal core. No blocking mathematical defect was found.**

This is an independent read-only paper audit, not a delivery-hash-only check. The original A/B/C directories and shared documents were not edited. Task B conclusions were not inspected or used. The prior task C calibration was not used to prove any A paper claim. This note persists completed review work; it does not rerun or broaden the research.

## Claim-by-claim judgments

Line references below refer to the delivered Task A REPORT.md.

| Claim | Judgment | Independently reviewed reason | Reference |
| --- | --- | --- | --- |
| SD-CORE | Accept | Actual H_X−s components are complete C={r}∪L∪S and U; r has full degree4 after deleting only its original spoke, s has full degree5, all other effective C/U vertices full degree4. Shared contacts remain actual vertices. | REPORT.md:53–92 |
| SD-JOIN | Accept | Restriction/union on the original edge decomposition gives unpinned-s C assignments, C/U joining and exact original-spoke restoration. Full contact tuples, all preimages, ambient empty cells and the r coordinate remain quantified; the proof does not assert all r fibres are nonempty. | REPORT.md:94–139 |
| SD-F | Accept | Unpinned local nonemptiness follows from connected degree-list slack at an actual contact. X-own same-β retained-edge witnesses give exact covering, private colours and distinct retained s-spoke colours. Contact release uses the same complete degree4 component and produces an actual full assignment. | REPORT.md:141–190 |
| SD-OUT | Accept | Q_U uses an actual s–U contact, a path inside complete U and an actual U–B attachment; Q_C uses an actual s–L contact and a path inside L⊆C to B. Both exist in X, avoid the selected component, stop at first B contact and do not use e or a retained r-spoke. | REPORT.md:211–216 |
| SD-K4 | Accept | A K4 block leaves exactly one original external direction at each vertex. Bridge deletion gives colourable sides; rejection forces a singleton bridge interface, and a branch without B/s constraints cannot force a singleton because its whole colouring permits S4 transport. Four actual tethers and the supplied exterior hub yield all ten K5 adjacencies. | REPORT.md:218–226 |
| SD-THREE | Accept | Two actual forbidden colours on the same component give palette membership differences on the same vertex–block incidence matrix. Its column independence and palette disjointness force a three-leaf active forest, hence one original triangle and three bridge arms. Full degree4 leaves one spare direction at each triangle vertex; inactive branches must reach B by the slack-colouring and whole-branch colour-permutation contradiction. The resulting original tethers are internally disjoint and avoid the arms and s. | REPORT.md:236–251 |
| SD-FOUR | Accept | Three actual forbidden colours share one coefficient vector. Positive palettes are A3−{d}, so positive active blocks cannot be bridges. The four-leaf forest is connected and has two triangle nodes; a negative triangle would require three distinct positive blocks. Two positive triangles cannot share a cutvertex, and only one negative bridge connects them, with no contact arms. The same actual-tether argument applies. | REPORT.md:253–264 |
| SD-NS41 | Accept | F_U is a singleton and F_C its three-colour complement. Actual C supplies the four-contact structure. The five bags are disjoint and connected; three triangle edges, as/bs/xy, three tether first edges and the original U-contact first edge of Q_U give the ten K5 adjacencies entirely inside X. | REPORT.md:268–285 |
| SD-NS32 | Accept | Capacity of the two-contact U and exact four-colour covering give at least two actual forbidden colours for three-contact C. Triangle arms, original s-contacts, actual tethers and Q_U supply all ten K5 adjacencies in X. | REPORT.md:287–301 |
| SD-NS23 | Accept | Capacity of two-contact C gives at least two forbidden colours for three-contact U. Only theorem dummy roles change: U is the selected component, actual C is the outside component and z=s. Actual C and all r fibres are retained. Q_C lies inside original L⊆C and supplies the final adjacency; all other bags lie in U/B/{s}. | REPORT.md:303–313 |
| SD-SP31 | Accept | Exact covering gives singleton F_U and exactly two forbidden colours for three-contact C. Retained original sb_j connects the exterior hub and supplies the final K5 adjacency. Complete U remains in X although unused by the minor. | REPORT.md:315–325 |
| SD-COVER | Accept | The minor proofs do not select a convenient incidence split, attachment pattern or shared-contact realization. All permitted pair/singleton scalar splits listed in §8 remain within the quantified source contract; the arithmetic tables are necessary domains, not realized sources. | REPORT.md:331–366 |

## BASE and external theorem verification

The review independently read all 18 frozen BASE input files from Task A's `inputs.json`, checked their SHA256 against that manifest, and compared their bytes with `git show BASE:path`. All 18 comparisons passed. No Task A metadata validator or mutation wrapper was run for this paper audit.

The decisive frozen BASE paper comparisons were:

- `frozen/docs/c5_degree5_interfaces.md` §§1–4: full relations, degree-list tightness, contact/incident-edge release and own-core private covering.
- `frozen/docs/c5_no_spoke_exterior.md` §§1–3 and 5: no-spoke minimal-core source assumptions, genuine component-avoiding external paths, K4 exterior hub, three-/four-contact extraction and all original minor adjacencies. Its hypotheses impose no T4 acceptance, second rejecting row or source size bound.
- `frozen/docs/c5_single_spoke_three_one.md` §§1–4: exact (3,1) covering, common-source two-palette active forest, arbitrary bridge arms, actual boundary tethers and retained-spoke K5.
- `frozen/docs/c5_single_spoke_four.md` §§1–5: three-palette common coefficient, exclusion of positive bridges, two-triangle/one-bridge structure and actual tethers. Task A supplies the no-spoke hub independently rather than borrowing this paper's sole-component spoke assumption.
- `frozen/docs/c5_degree5_tree_components.md` §1: connected exterior K4 extraction.
- `frozen/audits/2026-10-10-n45-s-long-contract/REPORT.md` §§2–3: retained actual supports, full-touch and star necessary bounds, pair geometry, and the retained adopted singleton incidence bound.

The frozen external primary lecture PDF was read directly with `pdftotext -f 5 -l 6 -layout ... -`, producing stdout only. Its Lemma 7 supplies tightness for a connected uncolourable degree assignment; Theorem 10 supplies the Gallai-tree/blockwise-uniform characterization with incident palettes disjoint and their union equal to the vertex list. These are exactly the external hypotheses used in the paper argument. The active-forest, tether, exterior-path and K5 steps are separately provided by the paper argument, not claimed to follow from the PDF alone.

External source: Zdeněk Dvořák, *List coloring and Gallai trees*, <https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf>. Task A records PDF SHA256 `50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea` in its external-input metadata. This external theorem remains an explicit trust dependency; this review does not convert it into a new Lean or Python theorem.

## Exact accepted scope

The accepted profiles use the actual-X contact order `(m_s,n_U)`:

| Profile | t_s | (m_s,n_U) | Selected actual component / final hub adjacency |
| --- | ---: | --- | --- |
| NS41 | 0 | (4,1) | Four-contact C / original first U-contact edge of Q_U |
| NS32 | 0 | (3,2) | Three-contact C / original first U-contact edge of Q_U |
| NS23 | 0 | (2,3) | Three-contact U / original first s–L edge of Q_C |
| SP31 | 1 | (3,1) | Three-contact C / retained original s-spoke sb_j |

Each statement quantifies arbitrary finite piece size, bridge length and branch depth, pair/singleton S, and every permitted actual incidence/shared-contact/attachment realization satisfying the complete source contract. The source is one named induced-C5 disk G with the original complete Σ=933/941 or a whole-graph D5 image, the original degree/ownership/support/criticality premises and all K1–K12 data obligations retained. The only omitted edge is original e=rb_i; X itself supplies all same-β minimal witnesses. The contradiction is a K5 minor in X and does not require recovery of e or a convenient selected r-colour lift.

## Findings and unresolved boundaries

No blocking mathematical defect or additional unproved sufficient source hypothesis was found for these four profiles.

Task A reports that `artifacts/c5_no_spoke_exterior/observations.json` exists locally but lacks the requested direct BASE Git blob. That custody finding concerns only the stopped finite artifact replay. No paper step above depends on the observations bytes: the independent argument uses the frozen BASE paper statements and proofs, original source hypotheses and the separately identified external theorem. This review does not adopt the quarantined observations or claim its replay passed.

The following remain outside this acceptance:

- Target finite-source construction/execution and source realizability: not established; the four finite source controls remain `not triggered`, not a numerical source-exclusion enumeration.
- New Lean formalization: not established or executed.
- Remaining U-owner=s profiles `(t_s,m_s,n_U)=(1,2,2),(2,2,1)` and full U-owner=s closure.
- Other core identities, original55, general N45/N2/E, ε≥3 and the general main theorem.
- Any promotion of the original-edge K5 minor to a boundary-fixed colouring replacement or a full-Σ-preserving reduction.

The four arbitrary-size conclusions are paper exclusions under the exact contract. Their proof strength and scope do not derive from finite calibration PASS, custody PASS or zero source triggers.
