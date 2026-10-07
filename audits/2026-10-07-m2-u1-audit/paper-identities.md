# M2 paper subaudit: U1 identities, leaf forcing, and the six-vertex subcase

Date: 2026-10-07. Frozen candidate: `ba0b447f09617591d9f2ba81c988f537af771791`.
Read-only checkout: `/tmp/math-m2-ba0b447-audit`.
Scope: `docs/c5_excess_two_no_mixed_core44.md` sections 1–2 and 3.1.
Only this new audit note was written by this subaudit. No candidate source,
producer, original certificate, or historical audit was repaired or regenerated.

**Verdict: holds under the stated source premises and the explicitly inherited
upstream classifications. No new gap or counterexample was found in this
scope.** This verdict audits the paper reduction; it does not independently
certify the 344-domain enumeration, 3,498 restorations, or the histogram. The
separate M2 finite audit must supply those conclusions.

## 1. Source and core premises

All line references below point to the frozen candidate. `U1` abbreviates
`docs/c5_excess_two_no_mixed_core44.md`.

| Premise | Frozen source | Scope check |
| --- | --- | --- |
| Finite simple graph with an ordered induced C5 as disk boundary | U1:14–17 | The disk boundary and its order are required for the shield/classification dependencies; general planarity is insufficient. |
| Complete Sigma is 933/941 or one whole-graph D5 image; every nonframe edge is Sigma-critical | U1:14–15 | Both masks contain all T4 rows. This does not make the original G minimal for any one rejected row. |
| Connected effective H; adjacent original degree-five roots z,w; other effective original vertices have complete degree four | U1:15–17 | Degrees count actual spokes and all original internal incidences. Isolated private vertices are ignored. |
| No mixed original component in H minus z,w | U1:17 | A remaining original piece has one owner. In particular, zw is the only possible internal connection between the two original root sides. |
| M is an inclusion-minimal rejecting q-core, containing B, retaining z,w, with their M-degrees both four | U1:19–20 | Minimality means minimal among all rejecting subgraphs, followed by selecting the subtype which retains both roots. It does not mean minimal only among subgraphs constrained to keep positive root degree. This is fixed by `artifacts/c5_excess_two_c44/REPORT.md`:21–24 and the explicit reference in `artifacts/c5_excess_two_c44pp/REPORT.md`:50–51. |
| q-core conventions and inherited T4/disk | `docs/c5_excess_two_root_deletions.md`:41–44; `docs/c5_degree4_guide.md`:21–24 | Every nonframe M-edge deletion accepts q; every effective M-private vertex has degree at least four; M's effective interior is connected. These facts concern M itself. |
| Original full B-touch needed by E6-D | `docs/c5_independent_support_capacity.md`:60–66 | Complete target Sigma rejects several distinct singleton rows, so the union of the required four-point supports is all five frame points. This is the same source G and same boundary. |
| Reduction to E6's literal frame | `artifacts/c5_excess_two_c44pp/REPORT.md`:53–60 | One whole-graph D5 transport takes the target orbit to literal 933 or 941, hence to E6's fixed three rejected rows. Original pieces, attachments, roots and their ownership travel together; componentwise normalization is not used. |

The minimality interpretation above resolves a possible ambiguity in U1:19;
the cited definition already fixes it, so it is not a new finding.

## 2. Original zw and whole-piece saturation

**Original zw retention — holds (U1:21–22).** Suppose M omitted zw. At the
fixed literal boundary coloring q, the two original root sides have disjoint
private vertex sets and no connecting private edge. Their colorings can be
combined because B is already fixed. If M rejects q, at least one side rejects
q. Dropping the other effective root side leaves a proper rejecting subgraph,
contrary to the global inclusion-minimality of M. Since z and w are effective
and each has M-degree four, this is a strict deletion. This argument permits
the root-deletion exception in the original G and does not assert that G minus
zw accepts every boundary row. Equivalently, the connected-interior property
of a minimal q-core forces the only possible internal joining edge zw.

**Original pieces all or none — holds (U1:20–21).** A retained effective
original nonroot vertex has M-degree at least four and G-degree exactly four,
so all its original incident edges survive. Along the connected original
piece this forces every original vertex, attachment, ordered contact and root
incidence to survive. If no effective vertex survives, the whole piece is
absent. This is the explicit saturation proof in
`docs/c5_excess_two_root_deletions.md`:62–66 and the C44 definition at
`artifacts/c5_excess_two_c44/REPORT.md`:30–34. It does not replace the original
complete relation by endpoint marginals.

## 3. E6-D and completeness of the corrected identities

**Same-source E6-D dependency — holds (U1:24–25).** After the whole-graph
transport described above, all its premises match. E6's root incidence
equation is `t_r + sum k_r(P) = 4` after subtracting zw
(`artifacts/c5_excess_two_e6/REPORT.md`:77–83). T4 gives `t_r <= 3`, so each
no-mixed root has an original unary. The original shield budget permits at
most two unary pieces, hence exactly one original U_z and U_w and capacities
`k_r = 4 - t_r` (E6:121–125). This applies to the original sides, not to
separately normalized replacement sides.

The complete all-degree-four classification applied to M gives internal
maximum degree at most three: the zero-triangle case is a path
(`docs/c5_tree_cores.md`:14–23); single-triangle branches do not fork and each
triangle vertex has at most one outgoing branch
(`docs/c5_triangle_forks.md`:17–19 and `docs/c5_triangle_branches.md`:20–24,
43–47); the two-triangle case is the six-vertex direct bridge
(`docs/c5_two_triangle_blocks.md`:18–27). Their admissibility as the only
cases follows from `docs/c5_k4_blocks.md`:104–122. This is an inherited
classification, not a new finite or Lean result.

Since each root drops from original degree five to M-degree four, the omitted
incidence per side is exactly one. With original zw retained and no original
mixed component, saturation leaves exactly these possibilities:

| Loss at z | Loss at w | Necessary original identity | Verdict and reason |
| --- | --- | --- | --- |
| One original spoke | One original spoke | (2,2), or 941 (2,3), including root exchange | Holds. If U_r is retained, its root internal degree is `1 + k_r = 5 - t_r <= 3`, so `t_r >= 2`. E6 gives `t_r <= 3` and forbids both sides being three. |
| One original spoke | One entire capacity-one U_w | (2,3), including root exchange; three-spoke side only the 941 literal 013 type | Holds. Omitting U_w costs one iff `k_w=1`, hence `t_w=3`; the other side must have `t_z>=2` and cannot also have three. |
| One entire capacity-one U_z | One entire capacity-one U_w | Would require (3,3) | Impossible by E6:127–132; not an additional admissible U1 identity. |

There is no root-side loss of a partial U, two spokes, or a capacity-two-or-more
U: these violate saturation or the exact loss-one equation. No other piece
exists under the exactly-two-unary conclusion. Thus U1:29–34 is exhaustive.

**941 three-spoke correction — holds (U1:36–40).** E6:127–133 explicitly
allows a 941 three-spoke side, only literal `S_r=013`, with U support 123 or
034. It forbids two such sides and gives `t_r <= 2` only for 933/940/932.
Retaining a capacity-one U and omitting a spoke leaves internal root degree
two, so the core maximum-degree-three condition cannot remove this case.
The old narrowed U1 identity is preserved as historical text with a direct
correction (`artifacts/c5_excess_two_c44pp/REPORT.md`:196–212). The new U1
argument does not rely on the old narrowing. This is a necessary identity,
not evidence that a complete target-Sigma source exists.

## 4. Spoke plus unit U: leaf forcing and triangle palette

| Audited step | Precise premises and dependency | Verdict |
| --- | --- | --- |
| Original U_z forces an original zxy triangle (U1:44–50) | After root exchange, retained U_z has capacity two and two distinct contacts x,y, because G is simple. A simple original x-to-y path in connected U_z plus zx,zy is a cycle. M's complete degree is four at every effective private vertex and M inherits T4/disk. The classification in `docs/c5_k4_blocks.md`:104–122 prohibits every cycle length other than three. Therefore the path is xy and zxy is an original triangle. | Holds. No replacement contact identity is introduced. |
| M has no second cycle (U1:51–53) | The same full classification permits at most two mutually disjoint triangles. If there were a second, `docs/c5_two_triangle_blocks.md`:18–27 forces the exact two-triangle six-vertex bridge graph, with no external tree. But w has internal degree one (only zw), whereas that six-vertex graph has no leaf. | Holds. Hence zxy is the unique cycle. w is one single-vertex branch of that triangle; the argument need not assert that all other U_z tree branches are absent. |
| Three w-spokes have three different q colors (U1:55–57) | w has all three original spokes and no retained U_w. If two spokes repeat a forbidden q color, deleting one preserves the entire q-coloring constraint at w and therefore keeps M rejecting, contrary to M's own edge criticality. q is a three-color row because all T4 rows are accepted. | Holds. The three spokes see all three used colors; the only legal w color is the unused D. |
| Complete w-side root relation is exactly {D} (U1:57–58) | Cutting original zw leaves the w-side as exactly w with its three named spokes. It has a coloring, uniquely w=D. Since M-zw accepts q by M-minimality, both sides' root relations are nonempty. With no allowed unequal pair, both must equal {D}. See the general bridge-forcing proof in `docs/c5_triangle_branches.md`:26–28 or `docs/c5_k4_blocks.md`:34–36. | Holds. This conclusion comes from one full coloring problem at the same fixed q, not from unrelated root marginals. |
| Triangle palette excludes a D-forcing outgoing branch (U1:60–62) | Apply `docs/c5_triangle_branches.md`:20–41 to M, whose unique cycle is the triangle, which is disk and minimal for q with all complete degrees four. At the triangle, bridge colors are distinct colors in its own lists; after deleting them the three remaining two-color lists coincide as P, every branch color lies outside P, and the inherited disk argument gives D in P. | Holds. The branch zw forces D, but D belongs to P, a contradiction. |

This excludes the spoke/unit identity without restricting the omitted
original U_w's size or its original complete relation. All forcing and palette
minimality is that of M; G is never asserted to be q-minimal.

## 5. Original (2,2): direct six-vertex reduction

**Paper reduction — holds (U1:102–107).** Both original unary pieces survive
and each has two distinct original contacts. The connected-piece path argument
above yields one original triangle at z and another at w. Original U_z and U_w
are different components of H minus z,w, so their vertices are disjoint; the
two triangles also use different roots. The whole-degree-four classification
rules out a third cycle, and the two-triangle classification
(`docs/c5_two_triangle_blocks.md`:18–27) forces exactly six private vertices,
the single direct bridge, and no other branches. Since original zw is present,
it is that direct bridge. Each U is exactly one original edge. No arbitrary
length unary remnant is being replaced by a topology contraction here: the
original M itself has this six-vertex graph.

After one whole-graph D5/S4 alignment of q to 01012, M lies in the 64 named
q-critical disk lifts of that classification. Each has complete Sigma 1022
(`docs/c5_two_triangle_blocks.md`:24–27, 146–148). The number 64 counts named
template lifts, not nonisomorphic source graphs. Each bridge root already has
one named spoke and has four absent C5 spoke positions, so adding one original
spoke at each root gives 4 times 4 restorations per core and 64 times 16 =
1,024. Dropping source disk and Sigma-criticality filters enlarges the domain
and is sound for exclusion. Complete ten-row Sigma, the histogram and D5
target-disjointness (U1:112–124) are finite assertions deferred to the separate
independent M2 checker; this paper note does not count their ordinary replay
as independent evidence.

## 6. Inherited audits, controls, and trust limits

- E6-D is independently reread here. Its upstream proof/classification and
  original shield theorem remain dependencies. The existing D9 audit is
  explicitly inherited: `audits/2026-10-06-task-d9/audit_e5.md`:16–19, 33,
  155–165 records the source scope and audits exactly this no-mixed budget.
- D9's actual no-mixed source antecedent is **not triggered** in all 90 AD
  transported cases (`audits/2026-10-06-task-d9/audit_e6.md`:127–130,
  153–166). The fixed selected-triple premise is also not triggered in
  0/9 original AD orbits and 0/90 transported cases. Those controls do not
  establish a target-Sigma no-mixed source realization or check the new U1
  paper contradiction through an actual source example.
- The inherited mixed-specific audit may support the shared degree-four
  dependencies, but its original scope is exactly one original mixed
  (`audits/2026-10-07-c44pp-mixed-audit/REPORT.md`:10–15). Its source-specific
  omission assertions are not applied to no-mixed. Its generic bridge-marker
  transfer belongs to the separate M2 section-3 audit.
- The triangle-palette argument includes a finite topology/NetworkX trust
  boundary: `docs/c5_triangle_branches.md`:37–51, 66–72 explicitly says the
  no-D template exclusion uses planarity replay without saved per-case
  Kuratowski subdivisions. This subaudit did not rerun all 177,280 templates.
- The six-vertex two-triangle classification has an inherited explicit
  subdivision/rotation certificate boundary:
  `docs/c5_two_triangle_blocks.md`:160–172 records 649 subdivisions,
  accepted rotations and byte replay without a new planarity search. Those
  upstream certificates were not all independently rerun by this subaudit.
- The full-degree-four synthesis retains the external degree-choosability /
  Gallai theorem and older paper/finite topology dependencies
  (`docs/c5_k4_blocks.md`:104–123). No external theorem was newly restated
  from uncertain recollection and no external browsing was needed.
- **Triggered and holds** for the finite necessary-core domain and
  **counterexample** counts must come from the independent finite M2 audit.
  This paper review supplies no new actual target-source positive control.
  No counterexample or blocking gap was found analytically.
- No Lean theorem, LC build, source-generation completeness, epsilon-at-least-
  three result, three-row generalization, or general exit statement follows
  from this subaudit. U2–U4 and all stated remaining core types stay open.

## 7. Audited input inventory

Commands used were ordinary `rg`, line-numbered documentation reads,
`git rev-parse HEAD`, `git status --short`, and SHA256/size calculations using
Python standard-library `pathlib`/`hashlib`. HEAD matched the frozen SHA;
initial `git status --short` printed no paths. No producer was imported.

| Input | Bytes | SHA256 |
| --- | ---: | --- |
| `docs/c5_excess_two_no_mixed_core44.md` | 8880 | `ab3dcd2ff66ec3a2508f91d74991d8f04fa7f9446c2addf5430d5e1b5f798dab` |
| `artifacts/c5_excess_two_c44/REPORT.md` | 19971 | `4e601a9a87e52a801d10e373b84f1fce765011ffb8a9377e905faa264783b6f6` |
| `artifacts/c5_excess_two_c44pp/REPORT.md` | 21727 | `6baa1dff6f1a280b5e05c272b9f16a46b38a16f026ab969288281e8e5d891179` |
| `artifacts/c5_excess_two_e6/REPORT.md` | 24146 | `1746ec1cdcabf228115bf50405f94ae3636812d060100b51b7d9f65868177847` |
| `docs/c5_excess_two_root_deletions.md` | 16312 | `a8d356c724808f87ed2f4e30a49f0a59e8c970789ce05fdec2934cfde9ed5af2` |
| `docs/c5_degree4_guide.md` | 12308 | `7ebf678a4952821f1d9a4c3faf7330bceb7f182dade789d9b330e40bfb5f3a05` |
| `docs/c5_independent_support_capacity.md` | 14655 | `708b42914db89f4e4308e1b33b4a76785be2f9c478edcc1e8757e64cd5d0a4bf` |
| `docs/c5_tree_cores.md` | 11254 | `61aec0f34adba46ec7cfaf58208f37a5820f14e93d9e1fe663c4a642947bd8fb` |
| `docs/c5_triangle_forks.md` | 6826 | `022d55244351c95480158f5c4d81b8915463dad302a5988248f231008dc4d43f` |
| `docs/c5_k4_blocks.md` | 10086 | `0f226a399da4f5f2be29ae6c90124689d7159153cd709e7e21138d78fa7239e6` |
| `docs/c5_triangle_branches.md` | 7631 | `116372cc8cf1eb06253d165d17be51ab7c8753619b25e1dc029a173c1a2c9901` |
| `docs/c5_two_triangle_blocks.md` | 10999 | `f30700bb24953a3532113cdd6259aacdbe13732931a1fd629a379bf10fd5b541` |
| `audits/2026-10-06-task-d9/audit_e5.md` | 21116 | `b55a10e8b69989a5edefaf0c21b17eadccaea82515f2aa2512d492430d54a765` |
| `audits/2026-10-06-task-d9/audit_e6.md` | 15234 | `2bc311669071fa4365cddacb99f4b3e8730341e062521e9ffe085dae50fe45cb` |
| `audits/2026-10-07-c44pp-mixed-audit/REPORT.md` | 7433 | `81b83315dde45b8add60f4c70caec5eef84a206f20351cbc4969b8899ef55636` |

A standard-library subprocess comparison read each of these 15 paths from
the exact frozen Git commit (`git show SHA:path`) and compared it to checkout
bytes: exit 0, 15 exact byte matches, zero mismatches. The aggregate M2 report
should also include its whole candidate/tree inventory and final drift check.
This note has no requested candidate-source edit, no new failure reproduction,
and no blocking finding.
