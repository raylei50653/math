# N45-S-LONG-S-T2-Q2-RESTORE independent paper review

2026-10-11. BASE `f2692089ad4259808e27d9b7e882ac09505b180a`.

The eight mathematical claims are supported in their assigned K1–K12 domain.
Both complete fibres `L_X(q3;0,3)` and `L_X(q4;0,3)` are nonempty by direct
same-source construction, and every lift in each restores original rb4.
Together they exclude all seven assigned schedules. No additional sufficient
source assumption or blocking mathematical gap was found.

One correctable coverage omission was found:112 known empty X cells at s=1
in four T4 rows were recorded as source-specific. Adoption of the symbolic
coverage must include `q2-coverage-corrections.json`; original target bytes
remain unchanged. The omission does not affect either restored fibre, the
seven-schedule proof or the literal calibration counts. The ninth claim's
native runtime/custody assertions are separate root review obligations.

This review did not use any same-round q0 restoration or transfer result as
a mathematical premise. It did not execute the worker checker or modify the
target, shared files, historical certificates or dispatch. Only files explicitly
authorized in this fresh supervision directory were created. No extra BASE
proof input was required: the new slack, capacity, symmetry, transport and
restriction/union arguments are directly proved below, using the dispatched
source contract and its sealed adopted role statement.

## Nine claim judgments

All REPORT line references below refer to the original target
`audits/2026-10-11-n45-s-long-s-t2-q2-restore/REPORT.md`.

| Claim | Judgment | Exact evidence and scope |
| --- | --- | --- |
| CQ2-SLACK | accepted | REPORT:39–60. Connected spanning-tree child-before-parent greedy proves degree-sized lists with one strict-slack vertex are colourable. The complete original degree identity supplies that slack from an unpinned actual contact, including a shared r/s contact. |
| CQ2-CAPACITY | accepted | REPORT:49–56. Fixing s while leaving r unpinned supplies nonempty complete assignments. A forbidden r colour must occur in every assignment's two actual r-contact colours; their full universal intersection has size at most2. This argument is valid for every proper boundary row and fixed s pin; it does not identify the full relation with a marginal. |
| CQ2-S-BETA | accepted | REPORT:58–70. At beta=q2, actual S40 has values10. For r0 or r1, pre-s full assignments exist by slack. The global-on-S transposition(2 3) fixes every actual boundary attachment and those r pins. The unique s contact can therefore avoid3, giving both complete pinned fibres nonempty. Shared-contact identity is preserved. |
| CQ2-BETA-PARTITION | accepted relative to the sealed beta role | REPORT:72–82. Actual U supplies a complete preimage avoiding3, s-spokes02 allow3 and r has no retained spoke. X rejects beta, so the two forbidden r columns cover Col; the two capacity bounds and S's nonempty r0/r1 fibres force B_S={2,3}, B_L={0,1}. L(beta;2,3) and S(beta;0,3) are nonempty local seeds with different beta r pins, explicitly not a beta whole-graph lift. |
| CQ2-U-TARGET | accepted | REPORT:102–104,118–119. At q3/q4 the same actual U012 has values010. Unpinned-s degree4 slack gives a complete U assignment, and(2 3) fixes every attachment while allowing the unique contact to avoid3. This proves a complete target preimage directly and does not claim a beta-to-target U bijection. |
| CQ2-Q4-FULL | accepted | REPORT:89–113. Full L(0 1 2) and S(1 2) maps carry the separate beta seeds into the same actual q4 frame and common pins(0,3). Joining their complete preimage sets with target U and the full isolated factor produces exactly the complete X fibre, nonempty. Its r0 differs from original b4 colour2, so the same full fibre equals the G fibre. |
| CQ2-Q3-FULL | accepted | REPORT:117–128. Full L(0 2), S identity and the separately proved target U give the same complete product at q3 pins(0,3). Its r0 differs from original b4 colour1. The exact s=3 forbidden columns additionally imply that r1/r2/r3 fibres are empty while r0 is nonempty in both target rows. |
| CQ2-COVER7 | accepted; coverage metadata requires overlay | REPORT:132–150. The seven full Q(G) sets have the delivered Delta=Q(G) minus{q2}. Each contains at least one restored q3/q4 row. Five schedules can select q4 and the remaining two select q3. Their original G rejections contradict those restored complete lifts. Separate q0/q1 restorations are not needed. The112-cell correction concerns other T4 pins and changes no schedule coverage. |
| CQ2-CALIBRATION | independent arithmetic accepted; native runtime separate | REPORT:154–159. A separate read-only Python calculation, importing no checker, matched720 support/permutation comparisons, six beta partitions, two proof transport records and1120 ambient ordered-pin positions. Ordinary/seed17 and negative-certificate runtime claims require the root's native replay. Their declared literal/count scope does not validate the coverage necessary-emptiness field and cannot certify a finite source. |

## Direct arbitrary-size source proof

Use one original source normalized jointly once, with actual U012/L234/S40,
beta=q2=01201, original spokes s-b0/s-b2 and omitted original e=rb4.
The actual original r/s incidences of L/S are(2,1); U has one s contact and
no r contact. K3/K4 give connected pieces and complete original degree4:

`deg_T(v) + 1[rv] + 1[sv] + |N_B(v)| = 4`.

There are no edges between distinct actual pieces. The roots are nonadjacent,
X retains no r-spoke, and every other original edge and attachment remains.
All local assignment sets below are defined on those actual original vertices,
including every contact tuple preimage, empty fibre and shared coordinate.

First, connected lists of size at least internal degree and strict at one
vertex admit a complete assignment. Root a spanning tree at a strict-slack
vertex and colour children before parents. A nonroot has its parent uncoloured
and at most internal degree minus1 previously coloured neighbours. The final
root has more list colours than its degree. No graph-size or block assumption
enters this construction.

Fix s=3 and leave r unpinned. Removing actual boundary colours and the s
colour at its contact leaves lists of size at least
`deg_T(v)+1[rv]` on T=L/S. Each has actual r contacts, so a complete assignment
exists. For any such assignment f, write M_f for the colours on its two actual
r neighbours. The forbidden column is precisely `intersection_f M_f`, because
r=a can be pinned when at least one complete assignment avoids a at both
original r contacts. Its size is at most2. This intersection is a derived
full-assignment query; all assignments and their preimages remain in the proof.

Conversely, fix r=a in S and leave s unpinned. Lists have size at least
`deg_S(v)+1[sv]`; the unique s-contact provides strict slack. If that vertex
also contacts r, its one actual r inequality has already been imposed while
the distinct s edge still supplies this one unit of slack. Thus complete
pre-s assignments exist for a=0 and a=1.

At beta, S's actual attachment values are10. Applying(2 3) to every original
S vertex preserves the entire pre-s assignment set at either of these r pins.
If the unique s contact has colour3, this image has colour2; otherwise the
initial complete assignment already avoids3. Hence the complete S fibres at
pins(0,3) and(1,3) are nonempty.

The inherited beta role gives actual U a complete preimage avoiding3, and
the retained spokes have colours0/2. If a colour avoided both mixed forbidden
columns, complete actual L/S assignments at that common pin and the U
preimage would join to colour X at beta. Beta rejection therefore forces a
four-colour union. Each forbidden column has size at most2, and the S column
contains neither0 nor1. Consequently S forbids exactly{2,3} and L exactly{0,1}.
This yields the two local seeds L(beta;2,3) and S(beta;0,3). Their different
beta r values are never presented as a common beta colouring.

At q4=01012, the L support changes201 to012. The colour cycle
pi=(0 1 2), with map0->1,1->2,2->0 and3 fixed, carries the entire L(beta;2,3)
assignment set to L(q4;0,3). S support changes10 to20, and(1 2) carries the
entire S(beta;0,3) set to S(q4;0,3). At q3=01021, L support changes201 to021
under(0 2), likewise sending pins(2,3) to(0,3); S support stays10 and uses identity.

Every map acts on every original vertex of its piece. Internal inequalities
remain proper; each actual boundary attachment colour moves to its exact
target literal colour; the two contact inequalities at a shared vertex move
together with the root pins. The inverse permutation supplies the inverse
on each complete assignment and on every contact tuple's full preimage set.
All sixteen ordered pins, including diagonals and empties, transport by the
same formula. Original edges, contacts, bridges, rotation and piece identities
are not changed by these colour-query maps.

The actual U query is010 in both target rows. It is not a colour-permutation
image of the beta012 query, and no such bijection is assumed. Instead,
complete degree4 plus the unpinned unique s-contact gives a complete target
U assignment. The transposition(2 3) fixes its actual attachment colours0/1
and permits the unique contact to avoid3. This proves a target full preimage
independently of beta transport and independently of Q(X).

All three target assignment sets are now in one common target frame, with
the same actual pins r0/s3. The retained spokes both have target colour0,
which is compatible with s3. Restriction/union identifies the full pin fibre
exactly with

`Lambda_L(target;0,3) x Lambda_S(target;0,3) x Lambda_U(target;3) x Col^I`.

The actual pieces have no inter-piece edge, and their only external neighbours
are the fixed original roots and boundary. The product therefore keeps all
compatible full assignments and every preimage and is bijective to the
complete X fibre. Each factor is nonempty. Every lift has r0 different from
the original b4 colour1 at q3 and2 at q4, and therefore already satisfies the
sole omitted original rb4. This restores the same full lift on the same G.

The forbidden s=3 columns also transport exactly: at q3 they are L{1,2}
and S{2,3}; at q4 they are L{1,2} and S{1,3}. Thus in this slice the r0
whole fibre is nonempty and all three other r fibres are empty. This says
nothing unsupported about the remaining target s slices.

## Correctable symbolic coverage omission

`q2-coverage-corrections.json` binds the original coverage SHA256 and lists
each affected schedule/literal/ordered pin, its indices and exact JSON
pointers, original value, corrected value and reason. The rows are T4
literals01203,01213,01231,01232, with r in{0,1,2,3} and s=1.

On every actual U attachment, each of those rows agrees with beta=q2 on
support012. Identity therefore preserves all complete U assignments and
preimages. Inherited `F_U(beta)={1}` gives `Lambda_U(row;1)` empty, so any
complete X lift at such a pin would restrict into an empty actual U fibre.
All112 cells must consequently be recorded as necessarily empty.

Each original cell was checked: `X_necessary_under_true_source` is
`source-specific; not supplied`, and `necessary_empty_reasons` is empty.
These are112 actual changes from unknown to empty, not merely additional
reasons for already-empty cells. None of those s=1 pins conflicts with
spoke colours0/2. The exact multiplicity is7 schedules x4 literals x4 r pins.
The overlay changes those two fields only. Existing G edge-filter and
row-rejection flags retain their separate meanings and are not rewritten.

The counts720/6/7/1120 are unchanged. The calibration data's ambient cells
contain literal colours and pin positions, not these necessary-emptiness
values; its runtime claim is therefore unaffected within its declared scope.
CQ2-COVER7 remains mathematically accepted. Raw coverage adoption must carry
this overlay, and literal-calibration acceptance must not be described as
validation of every symbolic necessary-emptiness statement.

## Coverage and inherited authority boundary

The selected rows are q3 for933/0123 and941/023; q4 for933/0124,933/0234,
933/1234,941/024 and941/124. In every case the chosen row is an original
same-frame G rejection in Delta. Each source would therefore have both a
rejected G row and the complete restored G lift constructed above.
Separate q0/q1 restorations remain unproved and are not required for these
seven schedules. No same-round q0/D result is used to cover any case.

The dispatched sealed SF-T2-ROLE is used for beta U's complete preimage
avoiding3; its source argument is frozen original fibre REPORT:274–297,
with the conclusion at291–293 and acceptance in frozen fibre-paper-review:30.
The role and its upstream Gallai/multi-odd-cycle authority remain an explicit
inherited paper/external dependency; this review does not claim a new proof
or fresh replay of that historical role chain.

Inherited Q(X)={beta}, SF-T2-EXTEND and the E2 finite-terminal chain are not
needed to establish the two new target fibres, which are constructed directly.
The target coverage still uses inherited Q(X) to label other unconstructed
rows as accepted; acceptance of those background labels retains that existing
trust boundary. This distinction does not discard QX from the dispatched
contract or upgrade its historical evidence.

The original K1–K12 source identity remains the theorem's stated scope, with
U owner=s, pair S40, r-split(2,2), t_s=2, spokes02 and beta=q2. The proof
does not impose any size bound on original pieces, cycle lengths, bridges
or branches and does not reduce S to a single vertex. No actual source
assignment, tuple value, preimage count or graph realization was supplied.
Source status remains `not triggered`, executed=false, trigger_count=null.
There is no new Lean theorem or general N45/N2/E closure.

## Consulted files

Target REPORT, claims, coverage, calibration and calibration-plan; the retained
rejected-candidate was checked as an unused abstract lemma counterexample;
the checker was read solely to confirm that its declared calibration data
does not validate necessary-emptiness fields and was never executed.
Dispatch TASK_C_T2_Q2 and the target's frozen dispatched long-contract REPORT,
original fibre REPORT and adopted fibre-paper-review supply the source
identity, full-assignment semantics and inherited role. No extra BASE proof
outside those already pinned authorities was used.
