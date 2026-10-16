# Independent mathematical review

Research BASE `120aae90cab8bc4881916adc598cf344f2f20f4b`.
Verdict: **PASS for the stated arbitrary-size necessary conditions and
the exact matching interface; grade B. Ordinary 101 nonemptiness remains
OPEN.** This verdict concerns the paper claims below. Build and repository
checks are reported separately in VERIFICATION.md.

The reviewer independently read the original J geometry, original-sector
C4 theorem, CAP A/B/C proofs, chorded-five proof and double-W5 proof,
then reconstructed the arguments in [GEOMETRY.md](GEOMETRY.md) and
[MATCHING.md](MATCHING.md). The final canonical [PROOF.md](PROOF.md)
and [REPORT.md](REPORT.md) were also independently checked against both
routes and accepted with the same PASS verdict. Preliminary checks and a corrected discarded
small-case calculation are retained in [REVIEW-NOTES.md](REVIEW-NOTES.md).
No frozen proof or original graph was changed. No external theorem was
adopted during review.

## 1. Disk theorem and source geometry

Factor-criticality gives minimum internal degree two and excludes a
bridge. For a subcubic graph, absence of bridges then excludes an
articulation. This legitimately supplies seven distinct degree-two
ports and two-connectivity of the same D[C], because tau=1 means f
has not removed an internal edge. Factor-criticality without the
subcubic hypothesis would not supply two-connectivity.

The possible hole was checked explicitly. Disconnected D-C must have
components with cut sizes three and four. The three-cut component is
a singleton t in S; it is excluded from X by its forced mate, and from
other residual components by the literal uniqueness of f. Adding this
t to C produces a four-bond whose two sides have more than two faces.
Faciality of every triangle makes that C4 induced. The source-sector
argument then excludes all four hub-incidence cases, including the
z-only case: zpq is in C, its other f endpoint is outside C union {t},
so pq would be on an induced C4 containing z. This establishes diskhood
rather than assuming it from cut size seven.

An interior boundary chord would give a bridge in D[C]. All six pins
are excluded from the strict interior by X or tau=1. Consequently each
interior vertex has its complete original J degree at least five, and
the disk counts |C|=2i+5 and E_ii+E_ib=3i+4 use every actual face.
Exterior chords are explicitly allowed; inducedness of the C7 is not
being asserted.

## 2. Uniform odd-interior bound

The full monochromatic-edge set is exactly the three original marks
and every edge dual to D[C]. Weighted face parity gives

`Delta=i_odd+b_odd-2epsilon-10`.

The m-sector argument supplies the essential additional information.
A C block at m has t_m+1 faces, so its contribution to the zero-to-zero
face-transition count is t_m+2. Singleton blocks contribute two. The
unchanged source-sector lengths therefore force both original s,t
degrees to be odd and at least seven whenever epsilon=0. Then m has
odd degree at least nine, exceeding its odd minimum seven by at least
two. When epsilon=1 the ordinary nonnegative excess bound suffices.
Thus Delta>=2(1-epsilon), and

`i_odd+b_odd>=12`, `i_odd>=5`, `i>=5`, `|C|>=15`.

These are arbitrary-size conclusions. In particular they exclude the
entire unbounded class having at most four odd-degree strict-interior
vertices, irrespective of the number of even-degree interior vertices.
The proof does not use the finite calibration to infer the uniform
bound. Its dependence on the original m sectors is explicit.

## 3. Exact common-family matching interface

The disjoint product decomposition retains each actual internal
matching and its matching on the unchanged actual exterior. All
singleton internal deletion fibres are nonempty by factor-criticality;
larger odd fibres may be empty and even deletion fibres are empty by
parity. For the entire same P111 family, cut tightness restricts the
crossing set to one port. This does not quantify over arbitrary
perfect matchings or assume that the 110 residual also fails.

Within the source disk, complementary paths pair the unselected ports
without crossing. The elementary pairing counts give the syntactic
registries of 560 tight and 1206 general odd-crossing states. The
complement-edge count independently gives

`sum(path parities)+number of odd internal cycles = 1-r (mod 2)`.

For eta=0 this makes 140 tight cells, and 302 cells in the full registry,
universally empty. The corresponding upper bounds 420 and 904 are
valid; realization of every remaining signature is not claimed.

The parity join is an iff on full matching records. Repeated exterior
endpoints are handled by labelled cut incidences and zero-edge paths,
so they do not introduce an unstated distinctness premise. The full
path and cycle lists remain inside every state fibre. The finite key
does not determine their numbers of Tait or vertex-colouring lifts;
retaining those lists is necessary and is stated explicitly. An odd
complement remains an ordinary matching with an empty even-colour fibre.
The same-family uncrossing identities preserve their simultaneous
quantifier over all M in P111.

## 4. Calculation scope and controls

The reviewer independently reconstructed the thirteen-face synthetic
disk and implemented [check_geometry.py](check_geometry.py). The
certificate checks its orientable disk incidence, every vertex link,
all triangles, all induced C4/C5, seven ordered dual ports and all 24
perfect-matching lifts over the thirteen single-vertex deletions.
Normal and explicit seed-17 replay give the same canonical certificate.
The disk has no induced C4; its four induced C5 each bound one complete
degree-five interior wheel. It has four odd interior vertices and six
odd inward boundary degrees, so it calibrates the weaker local Euler
identity while failing the new full source-sector obligation.

It is explicitly a synthetic local patch. It carries neither the full
six-pin assignment nor an original-source completion; all source-level
numerical tests are `not triggered`. The geometry certificate rejects
a changed face or a promotion to source realization. The matching
controls preserve all matching records and empty cells on their stated
finite graphs; their doubled gluing controls use distinct exterior
endpoints. The repeated-endpoint extension is justified by the paper
incidence argument, not claimed as part of those doubled controls.

## 5. Corrections and remaining mathematical gap

Three review issues were resolved before acceptance. A preliminary i=3
disk calculation had E_ii=3 instead of the correct E_ii=2; the final
uniform source-sector proof bypasses this calculation entirely. The
exterior parity join now explicitly retains coincident endpoint
incidences and zero-length paths. In canonical PROOF.md equation (8),
the exterior fibre is now explicitly every perfect matching of
`(D-C)-{v_j:j in A}` together with the selected cut edges, filtered by
the required and forbidden marks and empty when selected outside
endpoints coincide. The reviewer rechecked this correction and its
literal product bijection. The canonical wrappers preserve the
triangular-hole argument, odd-interior bound, 420/904 upper bounds and
all stated OPEN boundaries. No unresolved defect in the stated new
lemmas was found.

The remaining problem is to exclude the actual seven-port disk with
at least five odd strict-interior vertices and its unchanged exterior,
or provide a reduction preserving the entire original contract.
Neither the lower bound nor the bounded interface proves that the
remaining interface is empty, bounds the source order, supplies a
replacement gadget, or produces a smaller completed bad source.

Therefore A grade is not justified. The new unbounded excluded class
and reusable necessary condition justify B grade. Ordinary 101
matching existence, its even-complement strengthening,
W110+W101>0, full 319 exclusion and the general K-infinity statement
remain OPEN. The existing k+5 reconstruction cost, K_<=22=K_<=5 and
fixed-r6 k>=25 are unchanged. Lean build success, when reported,
does not formalize these new paper lemmas. No commit or push authority
is inferred from this review.
