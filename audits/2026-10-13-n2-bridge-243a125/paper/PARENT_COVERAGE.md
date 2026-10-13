# Parent classification and the exact E-ARC2 residual

BASE `243a125a80e4d8de40957f59d8da0bdbc974cf69`.
The coverage below uses the original E3/E4/E5/E6 source contracts and the
subsequent exact-mask theorems. It distinguishes a whole source's surplus
roots from roots retained by one of its actual minimal cores.

## 1. E-ARC2 is an epsilon-two obligation in a bounded-Q domain

Conjecture E assumes a finite simple ordered induced-C5 disk, T4 acceptance,
complete-Sigma edge-criticality, effective degree at least four and connected
H. Its quantified rejection domain is `1<=|Q|<=4`. E-ARC2 is

`epsilon(G)=2 => Q(G) is contained in some consecutive three-point arc`.

By the original five-cycle set classification, a counterexample has, after
one whole-source D5 transport, the three rejections q0,q1,q3 and complete
mask941,933,or940. Mask940 is the common reflected933 source. The all-five
mask932 is outside this parent proposition. E2 already handles epsilon0/1;
epsilon>=3 automatically satisfies Conjecture E because its right-hand side
is at most three. No larger-excess source is a remaining E-ARC2 obligation.

Source: [synthesis §8.1, lines 430–487](../frozen/docs/c5_research_synthesis.md).

## 2. Complete top-level coverage

The degree-valid epsilon-two profile is either one degree-six root or two
degree-five roots, all other effective interior degrees four. In the
two-root case let delta indicate the original root edge and let m be the
number of original mixed components of H minus the two roots.

| Whole-source class | Coverage in E-ARC2-CEX | Original source support |
| --- | --- | --- |
| Unique degree-six root | Excluded | E3 §4, with D8 DG6-1's five relative spoke positions for the t=1 partitions(4,1)/(3,2); the old restricted t=1 table alone is insufficient. |
| Nonadjacent roots, m=0 | Impossible | Connected H requires an original mixed connection. |
| Nonadjacent roots, m=1 (N1) | **OPEN**, named below | E3 §5 / E4 §§3,6. |
| Nonadjacent roots, m=2 (N2) | Excluded | Complete masks941/933/940 fall under the prior full contract. The new [Theorem NB](CLOSURE.md) additionally excludes932 and therefore covers the entire original E4 three-row N2 contract. |
| Nonadjacent roots, m>=3 (N3) | Excluded | E4 §5 original theta plus N-empty; all core identities. |
| Adjacent roots, m=0 | **OPEN**, named below | E6 §4 full original two-side interface. |
| Adjacent roots, m=1 | **OPEN**, narrowed below | E3/E5/E6 plus the old complete-mask spoke/source exclusions. |
| Adjacent roots, m=2 | **OPEN**, named below | E6 §§2–3, with later U2 excluding its44 cores only. |
| Adjacent roots, m>=3 | Excluded | E6 §2 four original internally disjoint paths and N-empty; all core identities. |

Sources: [E3 §§2.1,4–6,10](../frozen/artifacts/c5_excess_two_e3/REPORT.md),
[E4 §§3–6](../frozen/artifacts/c5_excess_two_e4/REPORT.md),
[E6 §§2–4](../frozen/artifacts/c5_excess_two_e6/REPORT.md),
[D8](../frozen/audits/2026-10-04-task-d8/REPORT.md).

These cases are disjoint and exhaustive by delta and m. The surviving
families are necessary source classes, not claims that any member exists.

## 3. Core coverage is separate from source coverage

For all original E-ARC2 counterexample masks, the adopted two-root44
coverage is complete: U1 handles adjacent no-mixed, U2 adjacent two-mixed,
U3 nonadjacent sole-mixed, U4 nonadjacent two-mixed, and the earlier
adjacent-sole-mixed series covers its remaining44 identities. Larger m
was already impossible or incompatible with an all-four core.

This does **not** make every source an original55 obstruction.

| Core identity inside a surviving whole source | Exact remaining location / identity |
| --- | --- |
| Two-root44 | Excluded throughout E-ARC2-CEX by its full-mask theorems. For generalized N2, U4-3R supplies the new mask-free proof. |
| Two-root45/54 | Still possible in N1 and adjacent m=0/1/2. Degree-four saturation makes every original component whole; the lower-degree side omits exactly one original spoke or an entire incidence-one unary. No mixed can be partly retained. |
| Two-root55 | The core must be the original G by saturation over connected H. Such whole-source identities remain only in N1 and the adjacent classes after the N2 exclusion. |
| Single-root core | It is an all-degree-four original unary side S_r, not a degree-six whole source. At most one rejected position can have any such core. It can occur only in N1 with the retained root's total mixed incidence one, or in adjacent m=0. |
| No root in a rejected core | Impossible by degree-four saturation and connected H. |

For adjacent m>=1, every rejected core retains both roots and their
original edge: both root deletions and deletion of that original edge
accept all rows. For nonadjacent N2, both root deletions accept all rows
because both mixed-incidence totals are at least two. No single-root
exception is hidden in the N2 conclusion.

Sources: [root-deletion §§1–4, lines 62–177](../frozen/docs/c5_excess_two_root_deletions.md),
[component slack §4, lines 142–146](../frozen/docs/c5_excess_two_arc_component_slack.md),
[E6 §3](../frozen/artifacts/c5_excess_two_e6/REPORT.md),
[full-mask U1](../frozen/docs/c5_excess_two_no_mixed_core44.md),
[U2](../frozen/docs/c5_excess_two_adjacent_two_mixed_core44.md),
[U3](../frozen/docs/c5_excess_two_nonadjacent_one_mixed_core44.md),
[U3 mixed12/21](../frozen/docs/c5_excess_two_nonadjacent_mixed12_core44.md).

## 4. Named residual source ledger

All five rows below retain ordered B, actual original attachments/rotation,
ordered and shared contact identities, all original component relations,
empty fibres, full lifts and complete criticality witnesses in one frame.
Every residual must also satisfy the general pair-critical theorem P and
the original common-slack restrictions; a failed local condition removes
that candidate rather than enlarging the source class.

| Residual ID | Source conditions and retained complete interface | Core possibilities |
| --- | --- | --- |
| **EARC-NA1** | Nonadjacent roots with one original separating mixed C; all other components unary, u<=2. C has nonempty support, and original H has a cycle. No one-sided shield charge is assigned to the separating C. Keep the full same-row joint `(E_r x E_s) intersect A_C`, including literal shared contacts. |45/54, original55, and at most one single-root4 exception as specified above. The formerly remaining44 types are excluded by complete-mask U3; the E4 mixed22+44 theorem is not generalized to arbitrary mixed22 sources. |
| **EARC-AD0** | Adjacent roots with no mixed. Exactly one original unary at each root. If root r has t_r spokes, its unary has `4-t_r` incidences. The two whole-side shields have lengths>=2 and sum<=5. For941 one side may have the literal three-spoke set013, with unary support123 or034; otherwise both sides have at most two spokes. For933 both sides have at most two;940 follows its whole-source reflection. Keep `(E_r x E_s) minus diagonal` and the two whole original unary relations. |45/54, original55; at most one single-root4 exception. Two-root44 is excluded by U1. |
| **EARC-AD1-A4** | Adjacent roots, exactly one mixed, total spokes four. All(3,1)/(1,3) source partitions are excluded. Of(2,2), mixed11 plus the two side units and mixed22/no-unary are excluded. The remaining shape is mixed12 plus one unit unary at its incidence-one root, or the common root exchange. Its owner's spoke pair is an actual boundary edge; the pairs are unequal; its unary shield has length exactly three. If that shield is h0h1h2h3 in original cyclic order, owner spokes are h0h4 or h3h4 and the other pair is the other edge or h0h3. Delete the already excluded original named01/23,01/12,01/01,04/04 scopes only at their actual common transported frames. Preserve `R_C(x,y0,y1)`, `R_U(u)` and the full six-role same-row joint. |Original55, or a45/54 core obtained by deleting one original spoke at the incidence-two root. In this A shape G-U and the owner's spoke deletions already accept all rows, so they cannot supply a rejected core. |
| **EARC-AD1-LOW** | Adjacent roots, exactly one mixed, total spokes<=3. Keep the original degree equations `t_v+sum_C k_C^v=4`, all actual unary and sole-mixed relations, all shields and original supports. No finite exact-target ledger for four/five spokes supplies coverage of this source class. |45/54 or original55; no single-root exception because m>=1. |
| **EARC-AD2** | Adjacent roots, exactly two mixed; each root's spokes<=2 by its original incidence budget. The boundary-containing face of their theta is bounded by the two mixed paths; the original root edge is on the interior side. All pieces are one-sided, mixed supports nonempty, unary number<=2, original shield cost<=5. Keep `(E_r x E_s minus diagonal) intersect A_P intersect A_Q`. |45/54 (one original side-unit omission) or original55. Its mixed11-omission44 identities are excluded by U2; root and original root-edge omissions are excluded. |

The source class EARC-AD1 is partitioned by total spokes into the two rows
AD1-A4 and AD1-LOW. Six spokes were excluded in the original single-spoke
reduction, and five spokes in the original leaf-fibre theorem. The four-spoke
exclusions are original source theorems with their complete-mask hypotheses,
which every E-ARC2 counterexample already satisfies. This does not revive
E5/E6's older G1/G2/G3 entries as new obligations merely because those
historical tasks were seeking different three-row proofs.

Sources for the adjacent refinement:
[single-spoke §§3–4](../frozen/docs/c5_excess_two_mixed_core_single_spoke.md),
[five-spoke theorem](../frozen/docs/c5_excess_two_mixed_core_leaf_fibers.md),
[four-spoke31 singles](../frozen/docs/c5_excess_two_mixed_core_four_spoke_singles.md),
[binary](../frozen/docs/c5_excess_two_mixed_core_four_spoke_hubs.md),
[ternary](../frozen/docs/c5_excess_two_mixed_core_four_spoke_ternary.md),
[quaternary](../frozen/docs/c5_excess_two_mixed_core_four_spoke_quaternary.md),
[four-spoke22 mixed11](../frozen/docs/c5_excess_two_mixed_core_four_spoke_disjoint_pairs.md),
[E5 L8 mixed22 exclusion](../frozen/artifacts/c5_excess_two_e5/REPORT.md),
[A original contract and fibres](../frozen/docs/c5_excess_two_mixed_core_four_spoke_mixed12.md),
[E6 §§4,6,8](../frozen/artifacts/c5_excess_two_e6/REPORT.md).

The ledger is deliberately stated by original source conditions. It is not
a list of marginal relation schedules; satisfying these necessary filters
does not prove planar realizability or criticality. Additional previously
proved local restrictions remain enforceable at their literal original
scope. The audit has not re-enumerated the historical source keys.

## 5. What the new bridge changes

Before this audit, the published original55 nine-grid exclusion already
covered the N2 piece of E-ARC2's actual complete-mask counterexample domain.
The new theorem removes the last spectrum gap in the *stronger* original
E4 three-row N2 contract by excluding932. It also supplies explicit
mask-independent local witness lemmas that can be tested outside the
vanishing complete target class.

Thus generalized N2 is complete at that exact original E4 contract, while
E-ARC2 remains OPEN on EARC-NA1, EARC-AD0, EARC-AD1-A4,
EARC-AD1-LOW and EARC-AD2. Their remaining core identities are specified
above. No claim is made that the N2 theorem alone closes any of these
other source classes, that a zero-trigger test excludes them, or that the
new paper proof is Lean-formalized.
