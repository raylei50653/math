# N2-BRIDGE: original-quantifier and portability ledger

Frozen BASE `243a125a80e4d8de40957f59d8da0bdbc974cf69`.
This ledger reads theorem statements and proofs, not STATUS as a source of
parent quantifiers. References below point to frozen inputs. Dates and OPEN
labels in those inputs retain their historical meaning.

## 1. Three different domains

Write I={0,1,3}, with q0=01212, q1=01202, q3=01021. The other T3 rows are
q2=01201 and q4=01012. T4 consists of the five four-color rows; the ten rows
are complete ordered-boundary S4 orbits, with no independent D5 quotient of
pieces or boundary positions.

* **F-N2:** the complete-Sigma N2 contract used by the original55 and
  LL-CUT+diag chain: Sigma933/941 or one common D5 image of the entire source.
* **W-N2:** original E3/E4 three-rejection N2: T4 accepted, q0/q1/q3 rejected,
  q2/q4 unprescribed, complete-Sigma edge-critical, epsilon=2, nonadjacent
  degree-five roots and exactly two original mixed components.
* **E-ARC2-CEX:** a counterexample to the original E-ARC2 proposition. Its
  parent domain additionally says `1 <= |Q| <= 4`. Before classifying the
  roots or mixed components, the whole graph is transported once so I is
  rejected. This is not the same domain as arbitrary W-N2.

| Premise | F-N2 | W-N2, original E4 | E-ARC2-CEX |
| --- | --- | --- | --- |
| Finite simple induced-C5 disk, original ordered B | Required | Required | Required |
| Same graph, original edges/rotation/contacts/support/owners, complete fibres and lifts | Required | Required | Required for every decomposition/transport |
| T4 all accepted | Required; also follows from the exact masks | **Explicitly required**, not removed by saying three-row | Explicit in Conjecture E |
| q0,q1,q3 rejected after one common transport | Required | Required | Derived from failure of the three-point-arc conclusion |
| q2,q4 | Exact mask fixes them | Neither individually fixed | At least one accepts, because all five rejected is outside the parent domain |
| Every original non-B edge complete-Sigma-critical | Required | **Explicitly required** | Required |
| Every edge releases at least one row in I | Derived by E3 saturation | Derived by the same argument | Derived after selecting I |
| Every edge releases every row in I | Not a source axiom; a later N2 conclusion | Not a source axiom | Not a parent conclusion in general |
| epsilon=2 | Explicit source restriction | Explicit source restriction | Exact layer in the E-ARC2 proposition |
| H ignores free isolated coordinates | Same convention | Same convention | Same convention |
| Effective degree at least four and H connected | General critical-source derivation; reiterated | E2/E3 derivation | General derivation; also explicit in Conjecture E |
| Full B-touch | Derived from two distinct rejected singleton rows | Same E2/E3 derivation | Same derivation in the counterexample branch |
| Full degree profile 5,5,4,...,4 | N2 condition | E4 source condition | After unique-degree6 exclusion; not a starting axiom |
| Nonadjacent roots, exactly two mixed | N2 condition | N2 condition | One branch of the parent classification |
| Pieces one-sided; mixed actual support nonempty | Derived for N2 | E3/E4 derivation, independent of q2/q4 | Derived only in the relevant branch |
| Each rejected row has G itself as its sole effective minimal core | Obtained through 44/45/54 exclusions | **Was not available merely from the three-row statement** | False as a universal parent inference; single-root/core exceptions remain |
| H biconnected | Additional conclusion in the no-unary original55 subdomain | Not a parent axiom | Not a parent axiom |

Original sources: [E4 §1, lines 85–112](../frozen/artifacts/c5_excess_two_e4/REPORT.md),
[E3 §§1–2.1](../frozen/artifacts/c5_excess_two_e3/REPORT.md),
[synthesis §8.1, lines 428–487](../frozen/docs/c5_research_synthesis.md),
[LL-CUT contract, lines 8–43](../frozen/audits/2026-10-13-n2-ll-cut-3097ef5/CONTRACT.md).

The exact relation arithmetic is:

| Complete mask in the fixed I frame | Q | q2 | q4 | Original E-ARC2 domain? |
| ---: | --- | --- | --- | --- |
| 941 | 013 | accept | accept | yes |
| 933 | 0123 | reject | accept | yes |
| 940 | 0134 | accept | reject | yes |
| 932 | 01234 | reject | reject | **no** |

The common reflection `phi(j)=1-j (mod 5)` maps 940 to933, preserves I as a
set, exchanges q2/q4, and transports every source datum. Therefore the
complete-Sigma N2 results already cover the N2 branch of the *original*
E-ARC2 counterexample domain. The sole extra spectrum in W-N2 is932. This
deduction assigns no optional row before the source is split into these four
mutually exclusive cases; it is not an existence assertion for any mask.

Source: [E5 §1](../frozen/artifacts/c5_excess_two_e5/REPORT.md),
[E4 §6, lines 353–362](../frozen/artifacts/c5_excess_two_e4/REPORT.md),
[synthesis, lines 483–488](../frozen/docs/c5_research_synthesis.md).

## 2. Four notions of criticality

| Name | Exact quantifier | Logical role |
| --- | --- | --- |
| Complete-Sigma edge-critical | For every non-B e, some row rejected by G extends to G-e | Present in both F-N2 and W-N2. It does not identify the row. |
| I-triple-critical | For every non-B e, some i in I extends to G-e | Stronger in general. E3 §2.1 proves it here from the source contract and epsilon=2. |
| Minimal q-core M | M rejects one fixed q, and every proper B-preserving subgraph of M accepts q | A property of the actual subgraph M; it makes each edge of M critical for q and hence for its own complete Sigma. |
| Simultaneous original55 minimality | For each rejected q, original G is itself its minimal core | Stronger than triple-critical. It yields every non-B deletion accepts all originally rejected rows, and hence all ten rows because acceptance is monotone. |

E3 does not select witnesses from different rows and combine them. It takes
an inclusion-minimal subgraph M still rejecting all three rows. Its own
effective degrees are at least four. The excess difference is a sum of
nonnegative original degree losses. If epsilon(M)=2, a retained surplus root
and degree-four saturation propagate over connected H to force M=G. A
proper M has epsilon at most one, where E2 forbids the nonadjacent pair in I.
Thus no edge can preserve all three rejections. This is not a proof of
selected-row minimality of G for every i.

Sources: [E3 §2.1](../frozen/artifacts/c5_excess_two_e3/REPORT.md),
[E4 §1, lines 103–106](../frozen/artifacts/c5_excess_two_e4/REPORT.md),
[pair-critical §2, lines 59–79](../frozen/docs/c5_excess_two_arc_pair_critical.md).

## 3. Theorem-by-theorem portability

“Direct” always retains the theorem's actual local graph hypotheses. It does
not permit replacing full relations by marginals or applying a source lemma
to a merely feasible matrix. “Conditional” specifies which derived premise
must first be supplied in the weaker source domain.

| Existing theorem / proof step | W-N2 portability at BASE | Exact dependency and new bridge disposition |
| --- | --- | --- |
| E2 degree/H/full-touch and epsilon0/1 laws | Direct | General T4/Sigma-critical sources, or a newly minimalized derivative. Paper/Gallai and finite terminal classification remain dependencies. |
| E3 triple-critical/saturation | Direct | epsilon2, connected H, degree-valid minimal subgraph, E2. No optional row role. |
| E3 original root deletion and whole-component saturation | Direct | Full original degrees; actual unary sides and same-row complete lifts. N2 has no single-root core because each mixed-incidence total is at least two. |
| E4 N-empty-separating, N-theta and N2-short-no-unary | Direct | Original topology, critical witnesses, complete degree-four lists; N-diagonal requires the actual short support and its original outside hubs. |
| E4 N1-22-44 | Direct, outside N2 | Uses the three named rejections and the actual direct-bridge all-four core; no q2/q4 role. |
| U1 no-mixed44, U2 adjacent-two-mixed44, U3 sole-mixed44 | Published complete-mask scope retained | The audit does not generalize these N2-external theorems. For E-ARC2 their original exact-mask hypotheses are already met. |
| U4 N2 two-root44 exclusion | Header was F-N2 only; proof transfers | New [U4-3R](U4_TRANSFER.md) verifies all source-to-domain steps and uses the mask-free 828-by-four T3 collision theorem. It does not rely on target comparisons or target zero triggers. |
| Pair-critical theorem P: every proper subgraph rejects at most one row | Direct **if** `|Z(G)|<=1` | Its §3 is expressly mask independent. Its old §4 obtained Z through exact-mask44 exclusions. New U4-3R plus N2 root-deletion gives Z empty also for932. |
| Component-edge release / full exterior projection | Direct | Every point of original C has full degree four. For e incident with C, `pi_out Col(G-e)=Col(G-C)`. This is not equality of internal fibres. |
| Component common slack `D_C subset Q(G-C)` | Direct | Same-row full exterior coloring plus actual repeated attachments; the bound `|Q(G-C)|<=1` additionally needs P. |
| Every mixed or incidence>=2 unary deletion accepts all ten rows | Conditional on no44 and no single-root core | The proof is degree loss plus a minimal core in the actual derivative; now supplied by U4-3R/root deletion. |
| All component deletions accept all ten rows | Old proof requires N45-U | A unit unary can lower only one root tofour. The old theorem used X=G-U=M and the full exact-U contract. Three-row criticality alone did not establish this. The932 bridge supplies a different leaf-block proof before using the conclusion. |
| N45 exact-U and exact-S covered identities | Full-mask scope retained | Their headers require completeSigma933/941/common image, actual derivative X=M, same-row minimality, exact original omission and complete fibres. No silent transfer of the old adoption chain to932. |
| Spoke leaf/palette signature argument | Conditional local transfer | Needs three distinct nonconsecutive rejected rows with complete G-C exterior lifts, adjacent-pair attachment bound, full B-touch, original Gallai palettes. The actual argument does not inspect q2/q4. For932 three such rows can be chosen among the four or more that extend G-C. |
| No-unary H biconnected | Conditional local transfer | Uses the original leaf-block exclusion and two actual mixed paths. It does not follow from general q-minimality alone. |
| SD-A (biconnected single deficit) | Direct at its own hypotheses | A derivative has one degree5, all others4, same biconnected H, and one rejected proper row. No minimality or exact mask required. External Cranston–Rabern/disk-minor dependency retained. Cannot apply to degree5/5 G. |
| No-unary root-spoke exclusion | Conditional local transfer | Once original H biconnected and the actual piece/attachment constraints hold, two same-H SD-A applications plus star geometry and same-row N-diagonal suffice. No q2/q4 role. |
| Original55 common capacity | Conditional local transfer | Root degree5, original C relations, nonempty legal opposite-pin sets; `O=0` uses actual same-row root-spoke restoration. It is not obtained merely by writing a capacity equation. |
| Original55 unary escape / partition / two-contact Diff proof | Conditional local transfer | Requires the specific original Gallai/attachment/leaf hypotheses and complete same-row component deletion lifts used in its proof. The complete-mask headers alone do not license transfer. |
| Original55 one-long, double-long, LL-CUT+diag | Conditional local transfer | Requires actual original55 structural conclusions, capacities, leaf restrictions and full local fibres. The last minor/diagonal/capacity contradictions do not read optional row acceptance. The bridge must first derive their hypotheses on932. |
| ES/ER lower bound `|H|>=10` for exact targets | Not used as an automatic932 lower bound | Finite source-domain filter must be checked; no absence-of-target inference is needed for the new bridge. |
| Near-triangulation / minimal-inner-order / W5 / h>=3 | Not applicable | Different minimality and degree contracts; excluded from this proof chain. |

Proof anchors: [component slack §§2–5](../frozen/docs/c5_excess_two_arc_component_slack.md),
[spoke closure §§1–6](../frozen/docs/c5_excess_two_arc_spoke_closure.md),
[N45 §1](../frozen/docs/c5_excess_two_nonadjacent_unit_core45.md),
[original55 common capacity §2](../frozen/docs/c5_excess_two_n2_residual_unification.md),
[diagonal §1](../frozen/docs/c5_excess_two_n2_diagonal_three_row.md),
[LL-CUT dependency table](../frozen/audits/2026-10-13-n2-ll-cut-3097ef5/CONTRACT.md).

## 4. The actual missing premise, before the new bridge

The first unsupported inference was **not** “LL-CUT needs q2 accepted.”
LL-CUT's final local proof does not inspect q2/q4. The gap occurs upstream:
the full source contract was used to import the 44 and N45 exclusions,
which produced same-row component/spoke restoration, local attachment
bounds, and the original Gallai/leaf structure. A graph satisfying only the
three-row E4 contract had not yet been proved to have those properties.

A minimal useful first bridge is the falsifiable source theorem U4-3R
stated separately above. It uses the actual 828-core terminal statement,
not the theorem header's exact-target label. It proves Z empty and P. In the
only uncovered complete spectrum932, the stronger five-row refusal then
supplies repeated-row constraints unavailable from an arbitrary three-row
partial description. All remaining transfer steps must explicitly establish
the local hypotheses in the table; they cannot be inferred from “no target
source found.”

The gap is therefore finite in spectrum but structural in proof obligations:
one extra mask, and a missing route from its original critical source to the
restoration/leaf/capacity premises. Neither T4 nor epsilon nor the5/5 profile
was absent from the original W-N2 parent.

## 5. Evidence separation

The ordinary paper proof, the existing all-four finite terminal theorem,
the new finite control audit, and the external degree-list/Gallai/SD-A chain
are separate evidence layers. Existing full-target zero-trigger controls are
not source exclusions. A control falsifying a weakened local claim is not
an E-ARC2 counterexample unless it satisfies every E-ARC2 source premise.
No part of this audit supplies a new Lean theorem.
