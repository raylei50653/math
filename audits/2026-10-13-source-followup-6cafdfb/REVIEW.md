# Independent K15 source-domain and derivative review

BASE: `6cafdfb02fe5892a49eee21f92aea2369a25c022`.
Review ownership: this exclusive directory only; no shared documents or old
certificates changed. BASE source documents and the exact working K15 checker
revision reviewed here are frozen separately under `frozen/`; hashes are in
`BASE.json`. The K15 work is concurrent, so these working snapshots are not
misrepresented as committed BASE inputs.

## Source-domain proof

Suppose there exists a C5 disk source with at most fifteen interior vertices
and complete ordered relation outside K132. Minimize interior vertices among
**all** catalogue-outside sources, then maximize edges. The BASE K14 theorem
forces exactly fifteen interior vertices. The BASE normal-form and degree
lemmas give a finite simple near-triangulation, its five boundary degrees at
least four, and every interior degree at least five. They do not require an
edge-critical source, epsilon=2, N2, a fixed mask, or a fixed collar.

Add a new vertex z in the original outer disk and its five spokes to the
original C5. This preserves every original edge and gives a simple sphere
triangulation with 21 vertices, 57 edges, 38 triangular faces, minimum degree
five, and deg(z)=5. Thus every such source maps to a degree-five rooted member
of the complete minimum-five order-21 sphere family. Conversely, deleting
any degree-five root leaves 20 vertices, 52 edges, 34 faces, fifteen strict
interior vertices and the five original root-neighbors in their cyclic order.
The unique nontriangular face has length five. Possible chords of that face
are deliberately retained; the inverse domain may be larger than the source
domain, which is harmless.

Taking every degree-five vertex in every sphere representative, and all five
cyclic starts in both directions, covers every labeled ordered boundary of
an original source. Reflection transports the whole embedding. The source,
root, original edges, rotation, outer face and all ten coloring fibres travel
under the same map. No independently normalized pieces are combined.
Therefore complete K132 membership for every retained root/frame contradicts
the hypothesized source. Along with the existing five-interior-vertex K132
witnesses, this proves K<=15=K132 **if** the complete generation and full-fibre
checks finish successfully. No finite count alone establishes completeness.

## Code review

The primary derivative was compared line by line with frozen K14 code.
Its changes are K15 names/schema/file paths, sphere dimensions
20/54/36 -> 21/57/38, root range 20 -> 21, disk dimensions
19/49/32 -> 20/52/34, and removal of the unrelated C8_INPUTS check.
Those replacements are mathematically correct. No search pruning was added.

The primary solver pins the literal five-letter row, enumerates all four
colors at each remaining vertex, tests all original adjacencies, and records
all full lifts. All ten rows, including empties, are stored. The independent
solver reconstructs original-label roots from a separately implemented
parser/face traversal and uses propagated-domain coloring. It compares
literal full-lift sets after one explicit original-to-canonical map. Its
root-index dictionary, visited-set equality and strict row zips reject lost
roots and lost rows. D5 counts use the shared boundary map; the unused fourth
color in a three-color boundary row has a unique normalization.

The second generator compiles the min4 route with a FILTER callback only.
The callback reads degrees at output time, with no PREFILTER or recursion
pruning. It accepts exactly min-degree-five outputs. This is an independent
construction route within plantri, not an independent generator implementation.
The full construction and canonical-path completeness remain the published
Brinkmann--McKay dependencies carried by the frozen K13 generation notes.
The main checker independently checks simplicity, reciprocal edges,
connectedness, the rotation's genus zero, triangular sphere faces, root
outer-face order, degrees and Euler curvature.

No source-contract or dimension defect was found in the reviewed revision.
Numeric completion status belongs in `RESULT.json`, generated after the
parent's immutable certificate and both streams are available.

## General-source literature boundary

No new arbitrary-size exclusion was obtained. The limited live primary-source
check found the known count-cone obstruction still stated as a conjecture in
[Dvorak--Lidicky, Coloring count cones of planar graphs](https://onlinelibrary.wiley.com/doi/10.1002/jgt.22767).
This is not a claim that all subsequent literature was exhaustively searched.
[Dvorak--Swart, Theorem 3](https://arxiv.org/html/2504.07764v1)
constructs graphs with excluded rooted/clique minors; for four colors it does
not promise a planar realization and does not eliminate 933 or 941.
The existing repo's five-pole face calculation already records why one planar
cap's positive gluing count does not create a Four Color Theorem contradiction.

Thus K15 is a bounded strengthening only. Arbitrary-size 933/941 exclusion,
K-infinity=K132, all eight unbounded h=3 collar contracts, and a new Lean
formalization remain open. No repeated search was used to relabel an
untriggered general source as excluded.

## Final completion addendum

The final `PROOF.md` was read in full. Its global minimality, cone, every-root
coverage and whole-embedding D5 argument are correct and match this review.
Its 33 triangular disk faces plus the pentagonal outer face agree with the
34 total faces. It does not assert an arbitrary-size theorem.

The parent's generated certificate is now present. A third small checker
`audit_aggregates.py`, importing neither parent checker, independently parses
both raw planar_code streams and reconstructs all primary roots. It finds
192 spheres in each stream, 2,714 degree-five roots, 27,140 literal rows,
and 624,617 saved complete lifts. Every saved lift is proper on all 52
original disk edges, has the correct literal boundary row, and is distinct
within its fibre. Every saved root mapping/rotation/edge set is reconstructed
exactly. All 2,714 complete saved relations equal 1023. The h histogram is
`0:56,1:211,2:563,3:947,4:717,5:188,6:27,7:3,8:2`.
These checks validate all saved lifts and coverage metadata; exhaustive-search
completeness remains the separate primary/independent-solver obligation.
No additional parent full-search replay was redundantly run by this reviewer.

`RESULT.json` records the certificate/payload hashes and numerical result.
`FINAL_INPUTS.json` adds exact snapshots of the final proof, streams, summary,
generator and receipts while preserving every earlier snapshot and BASE hash.
The six originally reviewed K15 working files have zero drift. The certificate
payload SHA256 is
`24e3e89af3d800fcc84128ad90304d9797f21d967429b358f16b3c1e725c465d`.

Review outcome: **PASS for the source-domain proof, derivative dimensions,
full rooted coverage metadata, and saved-lift validity**. Complete solver and
generation replay results are reported by the parent audit. No review finding
blocks its bounded K15 conclusion; no general 933/941 closure is inferred.
