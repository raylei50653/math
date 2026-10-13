# Independent review of the N2-BRIDGE synthesis

BASE `243a125a80e4d8de40957f59d8da0bdbc974cf69`.

**Paper verdict: PASS for Theorem NB at the exact original E4 N2 contract.**
The audit closes the missing932 branch by original-source arguments, with
the inherited U4 finite terminal and external Gallai/hub dependencies
explicit. E-ARC2 is not completed. There is no new Lean theorem.

The reviewer read the parent-authored [CLOSURE](../paper/CLOSURE.md) and the
separately authored [BRIDGE_LEMMAS](../paper/BRIDGE_LEMMAS.md), then checked
their consumers against the actual frozen original proof bodies listed
below. The reviewer authored the premise ledger and U4 portability note;
this document therefore does **not** describe the U4 note's self-check as
an independent review. The separate numeric U4 extraction and historical
independent domain checker are their own evidence layers.

## 1. Quantifier review

| Claim checked | Verdict | Reason |
| --- | --- | --- |
| W-N2 retains T4 and complete-Sigma edge-criticality | PASS | E4 §1 explicitly requires both. “Three-row” frees q2/q4, not criticality, excess or the degree profile. |
| Exactly four possible complete masks | PASS | T4 fixes five accepted rows and I fixes three rejected rows; two remaining Boolean positions give941/933/940/932. |
|941/933/940 use the existing full contract | PASS | All structural source conditions are E3/E4 consequences. The940-to933 reflection moves the entire source and preserves the selected triple as a set. |
|932 remains a separate proof case | PASS | No accepted q2 or q4 is guessed. In this case all five T3 rows are actually rejected. |
| Triple-critical versus per-row critical | PASS | The new route does not assume G minimal for each selected row. Component witnesses are separately established before their use. |
| E-ARC2 residual | PASS | The original parent restricts `1<=|Q|<=4`.932 is outside it, epsilon>=3 is automatic for Conjecture E, and N1/adjacent source classes remain. |

The initial CLOSURE draft described U4 as an at-least-two-rejections
theorem while its new formal statement fixed three rows. The proof may
support the stronger scope, but the reviewer requested alignment to the
stated original three-row domain. No stronger U4 scope is needed for932.

## 2. Local-witness and topology review

| Claim checked | Verdict | Original-graph check |
| --- | --- | --- |
| P from Z empty | PASS conditional on U4-3R | N2 root omission is impossible by the mixed-incidence budget. With no44 core, no excess-zero core remains. Pair-critical §3 expressly has no target-mask hypothesis. |
| Component-edge full exterior projection | PASS | Connected degree-four component lists have slack after an original incident edge is removed; each resulting part of an internal-edge deletion has an endpoint with slack. Full exterior assignments are held fixed. Internal fibre equality is not asserted. |
|932 root/nonroot attachment cap | PASS | Each nonadjacent boundary pair repeats in two actual rejected singleton rows. Deleting one spoke retains both rejections, violating P. This includes roots without invoking SD-A. |
| Four-row signature bridge | PASS | For each C separately, G-C accepts at least four rows. Every nonadjacent pair is detected and the vertex/edge signatures remain distinct after removing any one row. Exterior pins can differ across rows; ordinary private vertices see neither root. |
| Leaf-block original minors | PASS | The leaf private points have their actual attachments fixed by those signatures. Complementary H sets stay connected; full B-touch supplies the remaining B-path tether. The K5 bags use only original edges. |
| At most one ordinary private point per odd cycle | PASS | The tether meets the cycle away from the two degree-two ordinary vertices. The two cycle arcs and complementary B path supply the five disjoint bags. |
| Unit unary exclusion | PASS | A multiblock tree requires at least two private leaf contacts; all single-block possibilities fail degree/ordinary-point/minor conditions. No N45 theorem is imported. |
| All original C deletions accept ten rows | PASS | Mixed deletion gives either a prohibited root omission or a44 core. A nonunit unary deletion lowers its owner belowfour, forcing a prohibited root omission. T4 acceptance is monotone. |
| Central H block and attachment injection | PASS | Any leaf H-block outside the central root block must contain a root; the block-cut tree then puts it directly at that root. Nonroot H-degree-two points lie in biconnected blocks. The same-block K5 and different-block K3,3 arguments cover both possibilities. |
| C has no K4 block | PASS | Its four degree-four external directions are disjoint original branches, each reaching G-C directly or through a private leaf contact. Connected G-C gives the fifth K5 bag. |

References actually read: frozen
`c5_excess_two_arc_pair_critical.md` §§2–3,
`c5_excess_two_arc_component_slack.md` §§2–5,
`c5_excess_two_arc_spoke_closure.md` §§2–4,
`c5_excess_two_arc_size_bound.md` §§2–4,
and `c5_excess_two_root_deletions.md` §§1–3.

## 3. Unary discharge review

The relevant unary theorems distinguish their published complete-source
headers from explicitly listed *local* hypotheses. All of those local
hypotheses are now proved in the932 graph: connected full-degree-four
original U; bridge/odd-cycle blocks; private leaf contacts; at most one
ordinary private point per odd cycle; adjacent-pair attachments; support
at least three; original H-degree-two attachment injection.

| Step | Verdict | Detailed check |
| --- | --- | --- |
| Presence of U forbids singleton mixed support | PASS | Use actual bags `{r} union U`, `{s} union other-mixed`, and B. A complete G-P exterior witness is now available; merging equal pin-color bags is permitted only at their N(P) intersections. |
| u<=1 and no two-long-plus-U | PASS | Actual disjoint shield costs give1+1+2+2>5 or2+2+2>5. No separating component is charged. |
| U with two short mixed | PASS | The existing full block-tree proof gives one same-row owner-D lift. Both original short components accept that exact(D,D), so the full lifts glue. |
| UC3 / BR-U3CAP | PASS | k_U=3 forces no owner spokes and one incidence to each mixed. Fix any legal other-root pin. Each mixed forbids at most one owner color by complete-fibre B-C2, so refusal forces `|F_U|>=2`. This is independent of spoke-factor disjointness. |
| Three-contact U contradiction | PASS | The D-escape chooses one row; the used-color theorem gives at most one forbidden used color in that same row. All forbidden colors then number at most one, contradicting UC3. No cross-row capacities are added. |
| Two-contact U, one long and one short | PASS | Shield costs force a genuine three-point U support. The local U2-DIFF-ALL proof covers every possible block chain by the two-edge injection and five shapes, with its last barbell excluded by an original K5. A designated Diff row exists; the actual owner pin from G-U is extended. |

Proof bodies actually checked: frozen
`c5_excess_two_n2_unary_three_row_escape.md` §§1–4, including the single-block,
two-leaf and three-leaf case split;
`c5_excess_two_n2_partition_rule.md` §6, including the stated local used-color
bound; and `c5_excess_two_n2_unary_diff_closure.md` §§1–3, including the original
five-shape hypothesis list and barbell bags.

The UC3 replacement is material. The old original55 common-capacity proof
used same-row spoke-deletion witnesses to make external factors disjoint.
Those witnesses have not yet been established in this new source domain.
The new argument derives exactly the needed k_U=3 lower bound without that
assumption, and does not reuse the stronger old formula.

## 4. No-unary and final long discharge

With u=0, H is biconnected. All roots have at most two adjacent boundary
neighbors, so H-degree-two vertices are nonroots and the proven attachment
injection covers the entire set used by the old local arguments. For each
proper row, no unary exists and the spoke colors are distinct; hence

`|E_v|=4-t_v=k_P^v+k_Q^v-1`.

This formula does not require every root-spoke deletion to release the row.
The complete-fibre capacity arguments are therefore available directly.

| Consumer | Verdict | Hypothesis check |
| --- | --- | --- |
| E4 short diagonal | PASS | Same actual short support, connected exterior hubs, same pins, no root edge. |
| Low-contact long escape | PASS | Its proof uses the same local unary block-count argument with the set of root-contact vertices; ownership is preserved and irrelevant only because both pins are D. |
| One-long OL | PASS | Checked OL-C, permanent-failure leaf minor, leaf-edge injection and OL-F fixed-root exterior slack. All use proved topology/degrees/attachments and literal I. Source-size bounds are not used. |
| Double-long T0/T1 | PASS | Checked shared/nonshared cases, actual contact attachments, original H minor, and capacity cases. No optional row role. |
| Two-long support/spoke residual table | PASS | Actual shield supports give(2,2)/(2,3) lengths. The same-boundary-edge two-root K5 lemma uses the biconnected central block and original paths. Both are now available. |
| LL-CUT+diag | PASS | Checked original K5-H and K3,3-O bags, full-fibre diagonal failure consequences, and all(1,1),(2,1),(2,0) incidence cases. The added diagonal cells have original-list proofs. |
| Final join | PASS | One literal row and one ordered pair are used for both original mixed full lifts. Every original root/contact/frame edge is checked; no independent piece normalization or marginal product appears. |

Proof bodies actually checked: frozen
`c5_excess_two_n2_diagonal_three_row.md` §3,
`c5_excess_two_n2_long_synchrony.md` §2,
`c5_excess_two_n2_one_long_closure.md` §§1–5,
`c5_excess_two_n2_double_long_joint.md` §§1–4,
and old LL-CUT `paper/TOPOLOGY.md` §§1–8.

Thus Theorem NB follows on its stated source contract. The932 route does
not need the old N45 adoption chain, a single-deficit theorem for the
degree5/5 source, a larger-excess bound, a near-triangulation assumption,
or a source realization inferred from an abstract matrix.

## 5. Evidence and adoption boundary

* The arbitrary-size conclusion is the paper synthesis reviewed above.
* The all-four original-graph classification and marked-core terminal
  theorem remain inherited inputs. The reviewer ran both old U4 checkers
  read-only with exit0, including3,312 non-q T3 collisions and all132,480
  root fibres; the new controls audit independently extracts the needed
  mask-free property. These are not target-source searches.
* The external degree-list/Gallai theorem and original hub-minor results
  retain their stated trust boundaries. No external theorem is silently
  generalized to a different graph or list assignment.
* Finite negative controls refute only their actually weakened local
  claims. Complete target source controls remain `not triggered`, which
  is not the reason the source is excluded.
* Final file custody, deterministic replay, mutation controls and document
  checks are reported separately in the audit validation record. This
  paper PASS does not assert those commands have all finished.

Adoption is therefore **generalized N2, original E4 contract, paper proof
with retained external and finite-terminal dependencies**. E-ARC2 remains
OPEN on the five named residual source classes in
[PARENT_COVERAGE](../paper/PARENT_COVERAGE.md). No commit, push, publication,
or Lean-formalization claim follows from this review.
