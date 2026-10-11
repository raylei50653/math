# N45-S-LONG-S-T2-Q0-RESTORE independent paper review

2026-10-11. BASE `f2692089ad4259808e27d9b7e882ac09505b180a`.

All nine delivered claims are supported in the assigned K1–K12 domain. No
blocking mathematical defect or correction was found. The three schedules
933/0234, 941/023 and 941/024 are excluded by the same complete q2 restoration
argument. This judgment retains the explicitly inherited SF-QX trust boundary;
it does not independently re-prove or replay that historical chain.

The target delivery and shared files were read only. No new result from the
same-round T1, beta=q2 or block-transfer tasks was read or used. This review
creates only this file and the additional authority-pin record in the fresh
supervision directory. Runtime replay and custody acceptance are separate root
review obligations.

## Nine claims

References to REPORT lines below mean the original delivered
`audits/2026-10-11-n45-s-long-s-t2-q0-restore/REPORT.md`.

| Claim | Judgment | Exact evidence and scope |
| --- | --- | --- |
| T2Q0-S3 | accepted | REPORT:68–72. Actual U012 has identical boundary values at beta, q1 and q2. Identity preserves all full assignments, contact tuples, preimages and pinned empties. The accepted role gives F_U(beta)={1}; s-spokes02 forbid0/2, so any full X lift in these rows has s=3. U has a complete preimage avoiding3. |
| T2Q0-BETA-PARTITION | accepted | REPORT:74–91. At fixed s=3, complete degree4 and connected L/S give nonempty assignment sets before pinning r. The two actual r contacts bound each forbidden column by2; rejection of beta forces their union to cover Col, hence both have size2 and are disjoint. The original short-S N-diagonal sufficient premises are mapped below and give3 outside D_S. |
| T2Q0-L-Q1-TRANSPORT | accepted | REPORT:95–107. Applying (0 1) to every original L vertex maps actual support234 values212 to202. Both root pins move by the same permutation; for s=3 that pin stays fixed. All internal edges, actual attachments, shared contacts, full tuples, every preimage and empty fibres are preserved bijectively. |
| T2Q0-S2-FORCED | accepted | REPORT:109–129. If2 is absent from D_S, size2 and the N-diagonal restriction force D_S={0,1}, D_L={2,3}. The L permutation preserves this D_L, while S40 and U012 stay identical. All sixteen q1 X fibres are then empty. Each assigned original signature accepts q1, whose original G lift restricts to X, giving the contradiction. |
| T2Q0-S-Q2-TRANSPORT | accepted | REPORT:133–142. Applying (1 2) to every original S vertex maps actual support40 values20 to10, and beta pins(2,3) to q2 pins(1,3). The same full assignment, tuple, preimage and empty-fibre proof applies; no component or contact is replaced. |
| T2Q0-Q2-EMPTY1 | accepted | REPORT:143–150. The forbidden beta S(2,3) fibre transports to the empty q2 S(1,3) fibre. A complete q2 X lift with pins(1,3) would restrict into that empty set. All other s pins are ruled out by retained original spokes or actual U, so every r=1 X fibre is empty. |
| T2Q0-Q2-RESTORE | accepted relative to inherited SF-QX | REPORT:151–165. Accepted Q(X)={beta} gives a complete q2 X lift. Every such lift has r different from1=q2(b4), so restoring exactly original rb4 changes no lift. The complete X(q2) and G(q2) lift sets coincide, including their ordered pins and complete preimages. |
| T2Q0-COVER3 | accepted | REPORT:44–53,163–179. Each of the three original same-frame Q(G) sets contains q2 and omits q1. Thus q2 is in Delta for each schedule and the restored complete G lift contradicts its original rejection. One Delta row per schedule suffices. Individual q3/q4 restorations remain unproved, accurately recorded, and are not needed to cover these schedules. |
| T2Q0-CALIBRATION | independent arithmetic accepted; runtime separate | REPORT:169–200 and delivered proof-calibration/coverage JSON. A separate Python calculation imported no research checker and matched all three two-colour column cases, both full sixteen-pin transport maps and all480 ambient coverage cells. This verifies bounded interface arithmetic, not graph realizability or arbitrary-size topology. |

## Direct derivation of the beta partition

Fix s=3 and T equal to the actual L or S. Before pinning r, give each T vertex
the colours that avoid all its actual beta boundary neighbours and, when it is
an s-contact, the fixed colour3. K3/K4 supply connected T and complete original
degree4; consequently each list has size at least

`deg_T(v) + 1[v is an actual r-contact]`.

If an actual vertex is shared by the two roots, its s restriction is imposed
once on that vertex and its retained r incidence still supplies the indicated
strict slack. Each T has two actual r contacts and hence a vertex with strict
slack. Connected spanning-tree greedy colouring supplies a complete T
assignment at s=3 before any r colour is excluded.

For each such assignment f, let M_f be the set of colours appearing on its
two actual r neighbours. A pin r=a extends through T exactly when some such
assignment has a outside M_f. Therefore

`D_T(beta;3) = intersection_f M_f`, and `|D_T(beta;3)| <= 2`.

These are derived queries of the full assignment sets; neither their values
nor this intersection construction substitutes for the complete relations or
preimages. At beta, U admits s=3, there is no retained r-spoke and no rs edge,
and all isolated factors are nonempty. If a colour belonged to neither
forbidden column, the complete L/S preimages and a complete U preimage would
join at that common actual r colour and s=3 to colour X. Beta rejection thus
forces the two columns to cover all four colours. Their two upper bounds
force size2 each and a disjoint union equal to Col. This direct derivation
checks the sufficient premises behind the inherited long-contract §5 formula;
it does not add a new source assumption.

## Full sufficient premises for original S N-diagonal

The consulted upstream statement is BASE
`artifacts/c5_excess_two_e4/REPORT.md:225–245`, with its later explicit interface
in BASE `docs/c5_phase_b_common_lemmas.md:110–121`. The proof is a local list
and exterior-hub argument; it does not assume that the supplied root pins
already extend to a legal colouring of the entire exterior.

The required premises all hold on the same original G:

* The disk is finite and simple with the named original ordered C5.
* The actual S is connected, one-sided and every S vertex has complete
  original degree4. Its internal external neighbours are only the original
  r/s roots and actual boundary attachments.
* Its actual support is the true frame edge pair{b4,b0}. S may have arbitrarily
  many vertices, blocks, bridges and branches.
* The actual exterior `H-S={r,s} union U union L` is connected: L attaches to
  both roots and U attaches to s. This statement does not use a new edge or
  a reduced replacement for any original piece.
* Every frame point outside{b4,b0} has an actual exterior attachment: b1 and
  b2 are touched by U012, and b2 and b3 by L234. These original attachments
  remain in G and in X; omission rb4 is outside S and is not needed for them.

At beta, the support colours at b4/b0 are2/0 and the common root pin is3.
The three original connected, disjoint exterior bags in E4 are{b4}, {b0}
and `(H-S) union (B minus {b4,b0})`. The last bag is connected through the
actual exterior attachments, contains both roots, and sees only root pin3
at its S neighbours. Each bag sees one colour at its actual S adjacency;
their interior auxiliary colours do not enter S's lists. The original frame
edges provide the pairwise bag adjacencies. E4's tight-list/hub contradiction
therefore gives the complete local extension at root pins(3,3), establishing
`Lambda_S(beta;3,3)` nonempty and `3 not in D_S(beta;3)`.

This application uses original full B-touch and original exterior
connectivity. It does not infer them for an arbitrary spoke derivative or
require G to be beta-minimal. The only pin pair needed here is(3,3), although
the upstream lemma has the wider all-diagonal conclusion.

## Complete transports and common-frame join

For a colour permutation pi and any original piece assignment f, define its
image by `(pi f)(v)=pi(f(v))` on every original vertex of that piece. Proper
internal edges remain proper, and the actual support equality with the target
boundary row preserves every original attachment inequality. Each root-contact
inequality `f(v) != a` becomes `pi(f(v)) != pi(a)`. On a shared contact both
root inequalities act on that same original vertex and move together. The
inverse permutation supplies the inverse on all assignments and preimages.
An empty fibre maps to an empty fibre as well.

L uses pi=(0 1), taking beta234=212 to q1_234=202. S and U have identical
actual attachments at beta/q1 and use identity. The q1 contradiction uses
these maps as complete queries and then asks whether L/S are nonempty at
one common q1 pin; it never combines independently normalized sources.

S uses pi=(1 2), taking beta40=20 to q2_40=10, fixing s=3 and sending r2
to r1. A q2 whole-graph lift must restrict to that actual S fibre. Its
emptiness alone rules out r1, without choosing a convenient witness on L.
All other components, the same original r/s vertices, boundary, original
edges and isolated factors remain in each complete X lift. Restoring rb4
then tests the literal inequality on that same lift and that same r.

## Coverage and trust boundary

Independent bounded arithmetic gave three column cases,32 full ordered-pin
maps and480 ambient coverage cells. Each delivered schedule has ten literal
rows and sixteen ordered pins per row; its Delta is exactly Q(G) minus{q0}.
Each has q1 accepted in G and q2 rejected in G. The delivered collective
q2 restoration pool is exactly `(r,s)=(0,3),(2,3),(3,3)`; no particular one
of these fibres is claimed to be individually nonempty. Their union is
nonempty by inherited SF-QX, and every member restores rb4.

The new q1 contradiction derives its existence from K2 directly and needs
no missing final JSON. The new q2 existence statement deliberately inherits
sealed review SF-QX, SF-T2-EXTEND and the E2 paper/finite-terminal chain;
this paper review did not newly replay that chain. Missing no-spoke and
residual-locality BASE blobs remain provenance findings and cannot be
substituted by physical or quarantine payloads.

The accepted conclusion is confined to original U owner=s, pair S40,
r-split(2,2), t_s=2 with original spokes02 and beta=q0, under every assigned
K1–K12 premise and inherited authority dependency. The three schedules are
necessary source profiles, not three actual graph realizations. Source
controls remain `not triggered` with executed=false and trigger_count=null.
No new actual source, source realization, Lean theorem, general N45/N2/E
closure, t_s=1 exclusion or beta=q2 exclusion is established by this review.

## Consulted authority

Main mathematical inputs: original delivered REPORT/claims/coverage and
proof-calibration; dispatch TASK_B_T2_Q0; dispatched frozen long-contract
REPORT; sealed original fibre REPORT and sealed fibre-paper-review. The live
copies of those upstream audit reports were consulted and the root custody
review must continue to bind them to their pinned frozen authority.

Additional direct proof inputs, not in the dispatch's twelve BASE entries,
are recorded in `paper-extra-authority-pins.json`: BASE E4 REPORT and BASE
Phase B common lemmas. Each live file was compared byte-for-byte with its
exact BASE blob and matched. The root may freeze those exact bytes for the
supervision record. No external theorem was newly downloaded.
