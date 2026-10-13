# Independent weakening notes

BASE `243a125a80e4d8de40957f59d8da0bdbc974cf69`.
This review reads the original E3, E4, component-slack, spoke-closure,
size-bound, diagonal, partition, unary-Diff and LL-CUT proof texts. It does
not infer their quantifiers from STATUS.

## Findings

1. E3 Section 2.1 derives **union** triple-criticality: every original
   nonboundary edge releases at least one selected row. It explicitly
   does not derive minimality for each row. Replacing its existential
   row by a universal row would be a quantifier error.
2. Fixed T4 plus rejection of q0,q1,q3 allows exactly masks
   932,933,940,941. In particular neither q2 nor q4 can be prefilled
   from the parent premise. Existing E3 explicitly records 932 as an
   uncovered complete-mask possibility.
3. The latest LL proof does not inspect q2 or q4 inside its leaf minors,
   capacity matrices, diagonal escape or final lifts. Its fixed-mask
   dependence enters through the upstream supply of component omission
   witnesses, root attachment bounds and original block structure.
4. BR-CW3 supplies those component structural facts from a local complete
   outside witness for each component and each of three selected rows.
   Minimality for each row is sufficient but stronger than necessary.
   Component-row witnesses leave a distinct root-spoke obligation.
5. BR-5SLACK exploits the extra **rejection** in 932. Four actual outside
   witness rows per component suffice: every nonadjacent B pair repeats
   in two of the five rows, and any four columns distinguish all five
   original boundary-edge and boundary-vertex attachments. The chosen
   four rows may differ between components. No same-row full coloring
   is fabricated by combining them.
6. The leaf-contact and unit-unary exclusion proofs use actual K5 bags,
   full B-touch and original complete degree four. They do not use
   N45-U. BR-RETAIN still explicitly requires genuine 932-domain
   exclusions of root-omitting cores and two-root44 cores.
7. BR-5P gives the root attachment bound directly in 932: two repeated
   rows survive deletion of a redundant spoke, contradicting P. Thus
   the 932 bridge does not require SD-A. The separate optional
   BR-SPOKE0 route is valid only after u=0 gives biconnected H and then
   applies SD-A twice to that same H. An arbitrary edge-critical N2
   source is never silently declared biconnected.
8. The original common-capacity formula used root-spoke deletion
   witnesses to show unary forbidden colors avoid all spoke colors.
   This cannot be cited before spoke closure. BR-U3CAP repairs the
   needed k_U=3 case: its owner has no spokes, and the direct complete
   fibre capacity argument needs none of those witnesses.

## Checks performed by this reviewer

The literal five-row table was independently generated directly from
the strings and confirms collision pairs 02→34,03→12,13→04,14→23,24→01.
For each of the five omitted rows, both the five vertex signatures and
the five boundary-edge color-pair signatures are injective (5/5).
This is finite boundary arithmetic, not a source search.

Dvorak's primary PDF was read live. Lemma 7 supplies strict-slack
colorability; Theorem 10 supplies original Gallai blocks and disjoint
incident palettes for an uncolorable degree assignment. These results
do not provide the source disk, the criticality witnesses, full B-touch,
or the actual minor bags; those are separately checked in BRIDGE_LEMMAS.

The same-component projection identity was checked at the full outside
vertex set. It does not assert equality of internal fibre counts.
Shared contacts retain both root incidences, and pins are never
normalized separately across rows or components.

## Boundaries for the parent synthesis

The no-two-root44 premise in BR-RETAIN must be proved in 932; merely
citing the historical full-mask U4 conclusion is insufficient. The
general proper-subgraph P theorem requires its Z bound first. The
nonempty mixed support input is available at E3's broader three-row
level and must remain recorded. Root-spoke closure in the presence of
unary has not been established by this review; the parent may instead
exclude unary using the fully checked local unary lemmas and BR-U3CAP.

## Independent review of CLOSURE theorem NB

After writing the local bridge lemmas, this reviewer independently read
the complete candidate `paper/CLOSURE.md` and `paper/U4_TRANSFER.md`.
**Verdict: the new 932 synthesis is supported by its stated premises and
the explicitly retained inherited classification/finite-terminal inputs.**
No remaining mathematical gap was found in the bridge from 932 to the
local unary and no-unary exclusions. This verdict is a paper review, not
a new source graph or a Lean verification.

The critical checks were:

- U4-3R's finite statement quantifies over every other T3 row of an
  actual all-four core, so it survives the missing acceptance bits.
  Restoration uses one accepted root pair outside an actual partial
  matching of the omitted mixed piece. It does not claim that T4 is
  preserved, or that complete Sigma of core and source coincide.
- U4 plus the root-deletion argument gives Z empty before P is invoked.
  P restricts every interior boundary attachment in 932 by two preserved
  rejection rows. The proof therefore has no use of SD-A.
- Each component's four witnessed rows suffice separately; the
  signatures and minors require common original attachments, not common
  root pins or common witness-row sets between different components.
- Unit-U exclusion precedes component full retention. Retention then
  follows from the explicitly absent 44 and root-omitting core cases.
  No N45 statement is used to bootstrap its own hypotheses.
- The original block-cut argument and nonroot attachment injection
  cover arbitrary component lengths. BR-5P puts roots at H-degree at
  least three, so all H-degree-two vertices used by the local unary
  proofs are indeed the covered nonroots.
- For k_U=3, the owner has no spokes. A full coloring of C with that
  owner unpinned exists by strict slack at an actual owner-contact;
  its contact colors show at most k_C owner colors can be forbidden.
  This directly validates UC3 without the old spoke-factor disjointness
  identity. The contradictory upper and lower bounds use the same row.
- For k_U=2 and one long, the shield costs force a three-point actual
  U-support. The local U2-DIFF-ALL five-shape theorem applies with all
  of its degree, leaf, private-point, injection and planarity premises.
  Its full-color acceptance extends the actual owner pin of one full
  G-U lift; no diagonal marginal is substituted.
- With no unary, the exact root incidence equations require only the
  adjacent-spoke bound. Two-short, one-long and two-long are exhaustive.
  The OL and LL proof bodies use the listed structural consumers and
  selected-row full lifts, with no hidden q2/q4 status or spoke-critical
  witness. Their basic LL matrix interface is not promoted to closure.

The old 933/941/orbit source exclusion remains a separate inherited
input. Combining it with the new 932 proof and the exact four-mask
partition proves generalized N2 **within original E4's contract**.
E-ARC2 is not closed by this argument: N1 and adjacent-root sources still
require their own coverage. Full target controls remain not triggered;
that status is not a premise of this verdict.

No new Lean theorem, original-source enumeration, commit or push was
performed by this reviewer. No old audit, manifest or certificate was
edited.
