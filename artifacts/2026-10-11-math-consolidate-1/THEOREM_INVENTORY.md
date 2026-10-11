# MATH-CONSOLIDATE-1：Theorem inventory

日期：2026-10-11；固定 HEAD：`8c56b76922a1c7ac4c011096f2041b49c4a67cc8`。
狀態權威為 [目前 N45 canonical](../../docs/c5_excess_two_nonadjacent_unit_core45.md) 與其後正式採納 review／history。此文件是整編索引；候選包裝或新名稱不成為新採納。

## 口徑、量詞與證據等級

所有來源排除均量化 **每個任意有限大小原圖、每份滿足完整合同的具名原資料、每個允許的原省略及同一拒絕 literal β**，結論為合同不可能成立。除命題明說外，piece 大小、旁支大小、橋／臂／奇環長度無上界。每個 all-row helper 的 γ 是全部 proper literal `B→Col`，全部 ambient tuples／pins／preimages 均量化，包含空 fibres。

「最小已知充分前提」在端點欄保留目前已採完整合同；在局部 helper 欄列出已有證明實際需要的充分接口。不宣稱個別前提邏輯必要，也不以已排來源上的 vacuity 證明新局部引理。

| 分母 | 本 inventory 筆數 | 如何解讀 |
| --- | ---: | --- |
| 焦點分支排除 | 13 | U-LP/SS 2、LOW/HIGH 5、LONG 2、BR-SD 4；每支完整合同分列 |
| 前置窄排除 | 4 | S 兩 unary、U 兩 unary、U 兩 short、PG 的整份 S 單頂點 |
| SD 適用性 subset | 3 | 加實際二連通前提；第三支為相鄰來源背景，非 N45§1 非相鄰域 |
| 合成 corollaries | 4 | U、LOW、HIGH、S-SHORT；不是另四個互斥來源或新增全域閉合 |
| canonical 原表 | 33 行 bundle | 不把 slash-separated claim IDs 當獨立定理數；LONG／SD另列 |
| LONG-S 原 labels | 61 | 54 paper／helper／必要條件，5 finite calibration，2歷史 ledger；不是61端點定理 |

因此選定來源排除／適用性記錄共 **20**，另列 **4** 合成。此為可重算的本輪分母，不是全 repository 的定理總數；彼此有重疊。輔助表是接口／比較記錄，不作 unique adopted helper 數的虛假加總。

**證據標記：** A=完整契約內已採任意大小 paper；E=正式外部數學依賴（講義與期刊分開）；F=固定域有限控制；C=custody／seal；P=本輪提出的重述／包裝或未證推廣；O=OPEN。A+E 不等於 Lean；F/C 不證任意大小；actual source not triggered 不是 source exclusion。

**ignored coordinates 校正。** 通用 `Z` 是原內圖中孤立但仍可能有 B 附件的點，因子為 `J_γ=∏_{z∈Z}(Col−γ(N_B(z)))`；只有無任何原鄰居的 `I_free` 給 `Col^I_free`。HIGH 的 frozen H3/K3 明寫的自由 I 合同照留，不能把 I 等同所有 B-only Z。所有接合須保原座標；忘 Z 的投影不是完整 assignments 雙射。下列 DATA 的 I 使用此精確區分。

## A. U／LOW／HIGH：完整合同、端點與共用接口

### A2. Fully quantified source macros

These macros are display abbreviations, not generalized/adopted new theorems. Every endpoint below is ∀ all tuples satisfying its complete macro ⇒ contradiction; there is no size, bridge length, arm length, or piece-size bound. Where γ is used in a relation identity its quantifier is every proper **literal** map B→Col, Col={0,1,2,3}; every root pin and every ordered ambient tuple remains quantified even when its fibre is empty.

#### DATA(G,X,B,r,s,pieces,β)

All original vertices/edges, named and ordered contacts, a shared-contact vertex as one variable, actual attachments and actual supports, ownership, original bridges, disk rotation and its restriction, one literal four-colour frame, complete contact relations, all ambient empty/nonempty fibres, all r/s pins, and **all assignments/full lifts** are retained. Original G, derivative X and any contact-deleted graph have their own vertex/edge sets and lifts. Original ignored points Z retain J_γ=∏_{z∈Z}(Col−γ(N_B(z))); the explicitly adjacency-free I_free factors are Col^I_free. A D5 frame action, S4 colour action, or root swap is applied jointly to the entire graph and all data; no component is independently normalized. Minors prove nonplanarity only and cannot replace colouring factors. Geometric costs may add for original pieces whose critical witnesses use different rows; forbidden-colour capacities may not add across rows. The canonical singleton-position indices are (q0,q1,q2,q3,q4)=(6,4,3,1,0); 941 rejects q0/q1/q3, 933 also q2; T4={2,5,7,8,9} is accepted.

#### C(G,B,r,s,pieces,β,X)

1. G is an arbitrary finite simple disk graph; ordered B=(b0,…,b4) is its induced C5 outer face.
2. Complete ordered Σ(G)=933/941, or one common whole-graph D5 image; every nonboundary edge is Σ-critical; ε(G)=2.
3. Effective induced interior H ignores original isolated vertices, is connected and full B-touch. Exactly two original nonadjacent roots r,s have complete degree5, rs∉E(G); all other effective original interior vertices have complete degree4.
4. H−{r,s} has exactly two complete mixed components P,Q and any unary components; all are connected/one-sided with nonempty actual support. Mixed contacts have positive incidence on both roots. E3's original full-B/one-sided consequences are retained.
5. β is an original rejected literal row, β∉Σ(G). X=M is its own inclusion-minimal β-rejecting core with root degrees45/54. One common root swap names r as the degree-decreased root. X's β-criticality follows from **X=M**, never from original G's Σ-criticality alone.
6. DATA holds, complete original mixed components are retained, and there is no colouring-star substitution or partial-U omission.

C_S=C plus e=rb_i an original spoke and **X=G−e=M**, with every original vertex and every edge other than e retained. C_U=C plus a complete original unary U whose only original root-contact is rx and **X=G−V(U)=M**, all pieces other than U and all their original edges/spokes/attachments retained. The word unit means original root incidence1, not a nonempty forbidden palette at each row.

Provenance: canonical `:78-102`; original S `audits/2026-10-09-n45-s/REPORT.md:23-49`; original U `audits/2026-10-09-n45-u/REPORT.md:17-38`; latest SU adoption `:11-14`.

#### Expanded HIGH H1–H13 and HIGH3 K1–K13

The table below supplies every clause rather than relying on an unexplained label. H1=HIGH1, H2=HIGH2, K=HIGH3 in the three branch columns; the labels H1–H13 in source reports are premise IDs and must not be confused with branch names.

| Premise ID | HIGH1 full value | HIGH2 full value | HIGH3 full value |
|---|---|---|---|
| 1 | Finite arbitrary-size simple disk G; ordered induced outer C5 B | Same explicit G/B condition | Same explicit G/B condition |
| 2 | Complete ordered Σ(G)=933/941 or one common whole D5 image; every nonboundary edge Σ-critical; ε2 | Same complete Σ/criticality/ε2 condition | Same complete Σ/criticality/ε2 condition |
| 3 | Effective H connected, full B-touch; ignored original I have all four free-colour factors expressly required by frozen H3/K3; no extra B-only ignored points are admitted by this clause | Same effective H/full-B and the expressly required four-colour free-I condition; generic J_γ does not broaden this adopted clause | Same effective H/full-B and the expressly required four-colour free-I condition; generic J_γ does not broaden this adopted clause |
| 4 | Original r,s nonadjacent complete degree5; other effective original interior vertices complete degree4 | Same original degrees and no rs | Same original degrees and no rs |
| 5 | H−{r,s} exactly connected one-sided U,P,Q with nonempty actual support | Same three complete original components | Same three complete original components |
| 6 | P/Q actual support exactly endpoints of a true original boundary edge; positive incidence at both roots; ownership/all attachments preserved | Same true-edge/positive incidence/attachments/ownership | Same true-edge/positive incidence/attachments/ownership |
| 7 | U only adjacent to s among roots; exactly original sx, no U–r; whole U retained | U only adjacent to s among roots; exactly original sx1,sx2, x1≠x2, no U–r; whole U retained | U only adjacent to s among roots; exactly original sx1,sx2,sx3, all distinct, no U–r; whole U retained |
| 8 | Original mixed incidence (m_r,m_s)=(3,2), s has one P and one Q contact, r allocations1/2; named identities retained | Same allocations and original identities | Same allocations; original/shared identities retained |
| 9 | Original r has two distinct spokes e=rb_i,rb_j; only e omitted, rb_j retained; original s has two retained spokes | Original r has two distinct spokes e=rb_i,rb_j; only e omitted, rb_j retained; original s has exactly one retained sb_k | Original r exactly rb_i,rb_j, i≠j; only e=rb_i omitted, rb_j retained; original s has no spoke |
| 10 | Fixed original rejected literal β; X=G−e=M itself inclusion-minimal45/54 β core; root swap only names degree-decreased r | Fixed original rejected **three-colour** literal β; X=G−e=M itself inclusion-minimal45/54 β core; no inherited minimality | Fixed original rejected literal β; X=G−e=M itself inclusion-minimal45/54 β core; root swap jointly names r |
| 11 | Whole U/P/Q vertices, internal edges, rootcontacts, boundary attachments, other spokes retained; no additions/substitution/partial piece deletion | Only e omitted; whole U/P/Q vertices, internal edges, contacts, boundary attachments and other spokes retained; no added edge/substitution/shrinking/partial U deletion | Except e all original vertices, internal edges, contacts, boundary attachments/spokes retained; no shrinking/partial U deletion/addition |
| 12 | Named/ordered/shared contacts single original variable; actual support/ownership, bridges/rotation, common literal four-colour frame, ten complete relations, all pins, ambient empty/nonempty fibres/full lifts retained | Every listed DATA clause retained, especially U's complete two-contact fibre and original cycle | Every listed DATA clause retained, including all three U contacts, all ambient fibres and original free factors |
| 13 | Whole-graph D5/S4/root swap on all data; keep933 q2; β need not be U-shield midpoint; G/X/contact-deleted graph have separate edges/lifts | Whole-graph D5/S4/root swap on all data; keep933 q2; no U-midpoint assumption; distinguish each graph's edges/lifts | Whole-graph D5/S4/root swap on all data; keep933 q2; no U-midpoint assumption; each graph's vertices/edges/lifts distinct; minors only refute planarity |

Exact primary provenance: HIGH1 `audits/2026-10-10-n45-s-high1/REPORT.md:21-36`, adopted repetition `audits/2026-10-10-n45-high1-supervision/REPORT.md:16-28`; HIGH2 `audits/2026-10-10-n45-s-high2/REPORT.md:25-37`; HIGH3 `audits/2026-10-10-n45-h3a/frozen/authority/common-contract.md:18-32`; latest adopted K mapping `audits/2026-10-10-n45-high23-supervision/REPORT.md:71-85`.

The word “Same” in the table refers to the concrete condition printed in that row, not to a whole unexplained contract. All fourteen nontrivial DATA details are explicitly defined above. We recommend any final artifact use the full concrete text if ambiguity remains.

### A3. Endpoint theorem inventory

Status A means adopted arbitrary-size paper **inside full named contract**, retaining frozen BASE paper and external Gallai trust, with no new Lean formalization and no certified actual N45 source. “Min known sufficient” in this table is the complete adopted branch contract; smaller independently proved helper interfaces are catalogued in §4. We do not label unreviewed removal of source clauses a weakest-hypotheses theorem.

| ID / quantified theorem | Full branch condition beyond C_S/C_U | Dependency path and source | Evidence/status |
|---|---|---|---|
| PRE-S-U2: ∀ C_S with two different original unary pieces ⇒ ⊥ | Original unary incidences arbitrary; e is spoke, not piece omission. Mixeds may include long | Original witness/one-sided shields, N-diagonal, S02 low-root zero slack, S04 low-incidence universal relation; original S `:148-175`, adoption SU `:19` | A; fixed exact-source controls not triggered |
| PRE-U-U2: ∀ C_U with another distinct original unary V ⇒ ⊥ | Only omitted U incidence1; V capacity arbitrary | U-WIT, U-CAP, U-S3, N-diagonal/shield; original U `:212-241`, SU `:22` | A; no N2 u2 source control |
| PRE-U-2SHORT: ∀ C_U with both original mixeds short ⇒ ⊥ | U-U2 first yields unique original U; X has no unary; both original diagonal relations retained | Same β's unused D, full mixed N-diagonal lifts at r=s=D ⇒ X acceptsβ; original U `:243-251`, SU `:22` | A; exact-source antecedent not triggered |
| PRE-PG-S1: ∀ LP-contract below with V(S)={v} ⇒ ⊥ | Whole original S is one vertex; **not** singleton support; in U012/L234/S40 frame its four original edges rv,sv,b0v,b4v retain identity | PG02 restricted spokes + U-CAP positive raw columns + PG04 strict slack; original PG `:188-199`, PGA `:126-130`, P adoption `:8-16` | A; 12 local negative controls calibrate full16-pin oracle, no complete source |
| END-U-LP: ∀ C_U with unique original U, one long L and short S actual support exactly true edge endpoints ⇒ ⊥ | Complete original unit rx; original shield lengths(U,L,S)=(2,2,1) partition all five edges, actual U/L support their three consecutive vertices; DATA. Zero slack/Δ forcing retained as original necessary information but not a required proof edge | Unattached U-shield midpoint m in X; T4⇒β=q_m; actual sole C={r}∪L∪S; X's own min; exact F_C and t_s=0/1/2 ⇒ BASE (5)/(4)/(3); PA `:46-171`, canonical `:146-164` | A by P supervision `:7-16`; finite exact source not triggered; BASE+external trust |
| END-U-SS: ∀ C_U with unique U, long L, S actual support singleton, total original S incidence≥4 ⇒ ⊥ | Original equalities t_r+k_L^r+k_S^r+1=5 and t_s+k_L^s+k_S^s=5; all original full-data clauses; no size bound | U/L shield costs(2,2),(2,3),(3,2); two unattached points⇒Σ(X)=Ω or one midpoint⇒same sole-C map; SSA `:35-56,79-150,152-194`, canonical `:166-178` | A by SS supervision `:8-11,29-62`; source controls not established/executed; no trigger count |
| END-LOW1: ∀ C_S with unique U owner=r, unique rx, both P/Q true-edge support, (m_r,m_s)=(2,3), original r/s two spokes each ⇒ ⊥ | s allocation1/2; r one contact to each P/Q; e only omitted; U full; β arbitrary original rejected literal, no midpoint condition | Actual sole C={r}∪U∪P∪Q, full join, min-witness F complement two s-spoke colours; BASE3 original K5; LOW1 `:18-36,52-66,69-171`, adoption LOW1 `:8-40`; canonical `:190-214` | A; no new finite source/control count; relation toy only |
| END-LOW2: ∀ C_S with unique U owner=r, contacts rx1/rx2 distinct, P/Q true-edge support, (m_r,m_s)=(2,3), r exactly one spoke e, s two retained spokes ⇒ ⊥ | Both U contacts and original x1–x2/r cycle full; r one contact to each P/Q, s allocation1/2; no midpoint condition | Same actual sole-C BASE3 sufficient interface after separately proving original r complete4 and no B/s neighbor; LOW2 `:20-39,46-143,147-211`; adoption LOW2 `:14-40`; canonical `:216-235` | A; no new finite source; toy/fixed schemas calibration only |
| END-HIGH1: ∀ full expanded HIGH1 H1–H13 ⇒ ⊥ | All13 clauses above; no reduced branch adoption | Original G K33⇒P/Q vertex-disjoint support⇒U three-point consecutive T; local capacity1 support symmetry + diagonal G lifts at r=s=D⇒Q(G)⊆T; Σ933 four rejects/Σ941 three nonconsecutive rejects contradict | A ten internal claims; HIGH1 adoption `:30-65`; canonical `:249-279`; source not established/executed |
| END-HIGH2: ∀ full expanded HIGH2 H1–H13 ⇒ ⊥ | All13 clauses above; arbitrary size two complete W preserved; refined construction γ exactly3 colours | Complete(2,2) join/min cover⇒C singleton/U pair; original O′ K33, shield supportT; sameβ Gallai pair bridge/W supply + frame K5⇒one original edge and true-edge supports; all-properγ palette transport; three-colour G restoration⇒Q(G)⊆B−T≤2 | A refined exclusion; original unrefined all-proper-unused-D claim GAP remains; latest HIGH23 `:38-69`, canonical `:282-313`; no source triggers |
| END-HIGH3: ∀ full expanded K1–K13 ⇒ ⊥ | All13 clauses above; U incidence3, s no spoke | Actual components C/U ordered contacts(2,3); complete private cover Col and \|F_C\|≤2⇒\|F_U\|≥2; original retained path s–P–r–rb_j provides exterior avoiding whole U; BASE no-spoke(3,2) original X K5, no restore e | A K-scoped; HIGH23 `:71-85`, canonical `:315-332`; no finite source/Lean |
| COR-U: ∀ C_U ⇒ ⊥ | Complete C_U, not arbitrary U omission | U-U2⇒unique U; U-two-short and 2+2+2 shields⇒long/short; S nonempty short⇒edge pair or singleton; edge pair⇒LP; singleton incidence≤3 forbidden by U-S3, incidence≥4⇒SS | A separate scoped composition: SSA `:220-248`, SS supervision `:68-83`, canonical `:180-188` |
| COR-LOW: ∀ C_S plus S06's unique U owner=r, P/Q true-edge support, mixed(2,3) ⇒ ⊥ | Exactly LOW residual, original omitted spoke exists | Original5=2+u+t with u,t≥1⇒(u,t)=(1,2)/(2,1); each full LOW1/2 contract checked, not just count | A separate composition LOW2 supervision `:43-50`, canonical `:237-247` |
| COR-HIGH: ∀ C_S plus S06's unique U owner=s, P/Q true-edge support, mixed(3,2) ⇒ ⊥ | Exactly HIGH residual; r original two spokes with one omitted | Original5=2+u+t_s, u≥1,t_s≥0⇒(1,2)/(2,1)/(3,0); full HIGH1/2/3 contracts checked | A composition HIGH23 `:87-95`, canonical `:334-342` |
| COR-S-SHORT: ∀ C_S plus both original mixeds short ⇒ ⊥ | Full §1 source, original components/witnesses literalβ all retained | S05/S06⇒unique unary and LOW/HIGH necessities; COR-LOW/COR-HIGH; canonical `:334-346`, HIGH23 `:87-95` | A scoped two-short branch only; general S remains OPEN |

### A4. Directly reusable helper inventory (independently justified interfaces)

Every quantified local helper fixes a single original graph/piece and its actual edge and attachment data. The shorter premises below are **explicitly proved in cited sources**, rather than inferred by vacuity from END-U/LOW/HIGH exclusion. Repackaging their statements under new names is a proposal; it changes no adoption status.

| ID / complete statement and minimal known sufficient interface | Original claims / provenance / evidence |
|---|---|
| H-JOIN: For any finite graph with an explicitly complete vertex partition into roots, actual pieces, B and I, and an explicitly complete edge inventory (piece internal/actual B edges, named root-contact inequalities, retained root-spoke inequalities), ∀proper literalγ and all root/contact pins, restriction/union is a bijection between full graph assignments and the simultaneous complete-piece factor join. Shared vertices remain single variables; every ambient empty fibre retained. No planarity/minimality/degree/Σ requirement | R10 `docs/c5_degree5_interfaces.md:88-110`; LOW1-JOIN; LOW2-JOIN `:94-144`; HIGH1 `:93-131`; HIGH2 `:75-96`; SS `:125-134`; paper direct edge argument |
| H-RESTORE: If X=G−e with original e=rb_i and every other vertex/edge/data fixed, ∀proper literalγ and all a,b, full lifts L_G(γ;a,b)={f∈L_X(γ;a,b):a≠γ(b_i)}; thus equal L_X when a≠γ(b_i), empty otherwise. Full assignment identity, no pin projection first | HIGH1-RESTORE; HIGH2-RESTORE; LOW1/2-JOIN; canonical `:199-204,224-227,256-260,289-291`; paper direct one-edge condition |
| H-MIN: For every specified X=M inclusion-minimal β-rejecting core, every retained nonboundary edge h has a full **same literalβ** lift in X−h; β-critical⇒Σ(X)-critical. This premise belongs to X. In particular two X-spokes at the same root cannot have equal β-colour | LOW1 `:64-66`; LOW2 `:49-66,147-150`; HIGH1/2-CORE; SS `:111-116,138-140`; not arbitrary derivative heredity |
| H-SLACK: For any finite nonempty connected simple C and degree-list L with \|L(v)\|≥deg_C(v), if one vertex is strict then C is L-colourable; equivalently rejection forces all tight. No planarity/minimality/Gallai hypothesis | Local elementary greedy proof R10 `:125-127`; frozen primary Gallai text `audits/2026-10-10-n45-ssa/gallai-primary.txt:166-177`; external statement, locally explained proof |
| H-GALLAI: For any finite connected C and degree-assignment M, C rejects M iff C is a Gallai tree with block palettes: clique palette \|V(K)\|−1, odd-cycle2, incident palettes disjoint and their union equals M(v); singleton uses M=∅/empty block family. Distinct rejection assignments are on the **same actual C** | Frozen primary `gallai-primary.txt:202-214`; R10 `:118-141`; external Gallai trust, no new local Lean |
| H-RELEASE: For any connected degree4 component C with all external neighbors in the fixed B∪{z}, actual lists and all ordered z contacts, for every properγ/every z pin a, deleting any edge incident to C makes all C constraints extend for that a. Cases internal bridge/nonbridge/contact/B edge retained explicitly; no planarity/minimality/Gallai assumption | R10 `:143-159`; repeated HIGH1-F, H2-F; paper H-SLACK only |
| H-COVER: For a fixed source with unique complete degree5 z, others4, connected effective H, ordered actual components C_i of H−z, with β a proper three-colour row and all root-spoke β colours distinct, edge-β-minimal rejection iff union F_i=A_z(β) and each F_i has a private colour. F_i uses complete tuples/lifts. Distinct-spoke premise comes from H-MIN when source is minimal; no need source Σ933/941/T4 | R10 `:171-190`; LOW1/2-F, SS-SPOKES, HIGH1-F, H2-F, H3 cover; paper using H-JOIN/H-RELEASE |
| H-SOLE-F: Specialize H-COVER to actual sole connected C: unpinned R_C(β)≠∅ by H-SLACK and F_C(β)=Col−β(N_B(z)). With distinct original spoke colours t, \|F_C\|=4−t and \|P\|=5−t. Actual degree_X4, ordered distinct contacts, all lifts kept; not every pin nonempty | PA `:105-131`; SSA `:136-150`; LOW1/2-F; LONG-R same mathematical interface elsewhere; paper specialization of existing R10 |
| H-COLUMN: For the vertex×block incidence matrix of any finite connected graph C and its complete family of nontrivial maximal blocks and each block's actual vertex set, columns are linearly independent over R. Leaf-block private vertex eliminates each coefficient. Singleton case excluded or treated separately | BASE3 `docs/c5_two_spoke_three_contacts.md:71-76`; BASE4 `docs/c5_single_spoke_four.md:75-78`; BASE5 `docs/c5_no_spoke_exterior.md:139-141`; repeated LOW maps; elementary paper |
| H-PAIR-DIFF: On one actual connected C with two rejecting degree-assignments M_a,M_b and Gallai palettes S_K^a,S_K^b, if indicator difference M_a−M_b=1_P(e_b−e_a), column independence forces each active block to exchange a↔b; unchanged colours retain membership. For ≥3 rejected pins, the same RHS and injectivity force one common coefficient τ across all pairs; τ_K∈{−1,0,1}. Full palette disjointness and actual block identities necessary | BASE3 `:50-106`, BASE4 `:59-107`, BASE5 `:139-164`; LOW1/2; not yet a separately adopted general τ lemma name but original elementary argument exists |
| H-TRI: In connected K4-free actual degree4 C with exactly three distinct actual root contacts P, two distinct rejected root pins satisfying the preceding common-list difference and disjoint block palettes, active incidence forest has exactly three leaves; hence one original active triangle plus three arbitrary-length bridge arms, endpoints exactly P, including zero arms. Arm parity and inactive blocks kept. Tethers conclusion additionally needs complete degree4/exact external-neighbor constraints, rejection and no other root contacts | BASE no-spoke `docs/c5_no_spoke_exterior.md:180-206` explicitly states smaller common interface; BASE3 `:84-142`; original X/B tethers require H-SLACK fill argument; repeated LOW maps/HIGH3 map |
| H-SOLE-3: A finite simple induced-C5 disk X, own edge-β-minimal rejection for a proper **three-colour literalβ**, unique complete5 z/others4, actual connected sole C=H_X−z with three distinct original contacts, two retained z-spokes with distinctβ colours, original ordered attachments/rotation/full lifts ⇒ contradiction. No originalΣ933/941, no T4/second rejection, no unattached-midpoint assumption | BASE3 `:28-37,180-183`; LOW1/2 and U/SS t2 mappings establish all prerequisites. Existing theorem, safe citation replaces repeated triangle/tether/K5 derivations |
| H-SOLE-012: Same actual single-root disk/minimality/complete degree/sole-component/full-data interface with t=0,1,2 root spokes and 5−t distinct ordered contacts, distinctβ-spoke colours and exactF=Col−β(N_B(z)) ⇒ contradiction via separate BASE5/4/3 proofs. **t=0 requires no exterior z–B path** and must keep K4 permitted until even-leaf proof. t1/t2 use retained spokes and original tethers | PA `:119-169`; SSA `:152-194`; BASE5 `:128-176`; BASE4 `:33-71,109-190`; BASE3 above. This is a proposed combined wrapper of three existing theorems, not an unknown uniform classification |
| H-UNATTACHED: Every induced-C5 graph X acceptingT4 with v∈B having no neighbor outsideB accepts Ω−{q_v}. Two distinct such vertices implyΣ(X)=Ω. Arbitrary size, no disk/minimality/degree assumption. Proof modifies one point in one full lift | `docs/c5_unattached_boundary.md:16-44`; PA-UNTOP `:63-75`; SSA-U2/U3 `:89-105`; existing arbitrary-size paper |
| H-UNIT: Every actual connected original unary U, all points complete4, only root-contact rx, and any proper literalγ: full unpinned contact palette T_U nonempty, F_U={a} iffT_U={a}, otherwiseF_U=∅. In X=G−V(U), equality of all16 root-pair supports for G−rx andX, preserving each graph's own full lifts. Ifγ∈Σ(X)−Σ(G), **all** X-lift r projections andT_U are the same singleton. The last conclusion needs such newly acceptedγ and original critical contact for nonemptyΔ, not core rejectedβ | Original U `:54-88`; SU adoption `:20`; H1 rejection uses first part. Full-lift counts are not equal when the graphs have different vertices; only pair supports match, with U assignments separately retained |
| H-WIT-SHIELD: For any actual original piece with aΣ-critical contact, a full new-row edge-deleted witness restricts to a rejecting outside witness. If original G effective H is connected/full-B and H−piece connected, a short-support original unary has the required outside owner-to-complement-frame path; original unary shield length≥2. Each piece's witness may use a differentγ but **same original G/embedding** geometric costs add. Not all forbiddenF at coreβ nonempty | Original U `:95-107`; original S `:166-175`; original shield/B-S0 (external Gallai inherited); paper |
| H-TRANSPORT: For any fixed complete original piece/actual attachments/ordered/shared contacts, support-compatible colour bijectionπ sends every full assignment, tuple, pin and empty fibre atβ bijectively to those atγ wheneverγ=πβ on every actual support vertex. No size/disk/criticality/degree assumptions | PA `:180`; HIGH1 capacity-one stabilizer; HIGH2 rooted W palettes; independently adopted PR-TRANSPORT |
| H-SATURATION: For any fixed nonempty s-compatible complete relation with k different original r-contact vertices and F intersection of each complete compatible tuple's colour set, if\|F\|=k then each tuple sees exactlyF and those k contact colours are distinct. All full assignments remain behind tuples | PA `:182`; independently adopted PR-SATURATION; no disk/degree/sourceΣ requirement |
| H-ENDPOINT: Connected complete-degree4 actual P with planarity and2/3 disjoint connected pairwise-adjacent outside bags covering **all N(P)**, where N(P)∩each bag is pinned to one bag-constant colour distinct between bags ⇒ original hub/Gallai K5 rejection impossible. Three-point support version also demands P a complete H−owner-roots component, all interior neighbors exactly designated owners, K=H−P nonemptyconnected, fullB, support exactlyh–m–k, all owner pins assigned endpoint colours. Outside need not itself be properly coloured | PA `:181,186-192`; adopted PR-ENDPOINT; no arbitrary subset or missing complete-degree4 extension |
| H-ESCAPE: G obtained fromX by restoring actual wholeU with unique crossingrx, originalγ unary palette={a}, β′∈Σ(G), support-compatibleπ mapsγ toβ′ ⇒ any fullG lift atβ′ restricts toX withr≠πa. Does not repair any specifiedX colouring | PA `:183`; independently adopted PR-ESCAPE |
| H-FORCING: Complete χ=0 joint, fixed E_r,E_s, local nonempty fibres defining complete raw columns with\|F_C(b)\|≤k_C^r, original degree4 incidence \|E_r\|=m_r+d_r, nonemptyfulljoint r projection={a}. Then nonnegative δ+o+λ=n_b−d_r withn_b∈{0,1}; d_r≤1, and d_r=1 forces eachn_b=1, all three defects0, fulljoint={a}×E_s. No disk/criticality/Σ/cross-row capacity assumption | PA `:184`; adopted PR-FORCING; k_C and original incidence identities cannot be dropped |
| H-ZERO: C_S or C_U at same rejectedβ withχ=0, complete mixedrawtuple columns, low rootcomplete4, E_s nonempty and full side incidence/slack identity ⇒ D+O+δ+o+λ=0; each nonnegative item0, each raw mixed column saturated and partitionE_r. Restoring spoke and restoring unit differ: spoke gives O/λ only; unit may giveD whenF_U empty | Original S `:83-108,110-121`; original U `:132-168`; B-C2; canonical `:107-109,143-144`; candidate unified statement only after explicitly preserving omission-specific identity |
| H-SINGLE-SUPPORT-LOW: S04's local one-sided complete4 mixed/full-B disk, actual support exactlyoneh, both root incidencespositive,total≤3 ⇒ all-properγ compatibilityCol² via full N-diagonal and stabilizer orbits. Different theorem U-S3: actual original mixed with critical-contact witness, H−Pconnected/full-B, allpointcomplete4 and totalpositiveincidence≤3 ⇒ actualsupport≥2. U-S3 does not assert universal relation of an arbitrarily supplied piece | Original S `:124-146`; original U `:174-210`; SU `:19-26`; separate adopted conclusions |

There are 23 helper inventory entries here, counting H-SINGLE-SUPPORT-LOW as **one comparison entry containing two different original helpers**, not “23 unique adopted general theorems.” If the final report uses helper-theorem counts it should split that comparison entry into two and give a carefully defined denominator; several entries (H-JOIN, H-RESTORE, H-PAIR-DIFF, H-SOLE-012) are proposed display wrappers of existing proofs rather than existing standalone adopted names.

## B. LONG：完整K1–K12與端點／profiles

### B2. Fully quantified LONG contract macro K_LONG

The two endpoint exclusions quantify over **every finite graph of arbitrary size, every fixed original rejected literal boundary row β, every original named spoke e, and every supplied original datum satisfying all twelve clauses** below. There is no bound on piece vertex count, odd-cycle length, original bridge/arm length, branch depth or number of branches. Whole-graph D5/root and S4 transport means transport of every edge, contact, support, rotation, witness and full assignment; it is never independent component normalization.

The full macro transcribes the smallest already adopted source contract, rather than asserting its clauses are individually logically necessary. Source: `audits/2026-10-10-n45-s-long-contract/REPORT.md`:14–47.

| Clause | Complete sufficient premise / data obligation |
| --- | --- |
| K1 | G is a finite simple disk graph of arbitrary size with named ordered induced outer C5 B=(b0,…,b4); all original vertices, edges and rotation are supplied. |
| K2 | The complete ordered boundary acceptance set Σ(G) is 933 or 941, or one common D5 image of the entire source; every non-frame edge is Σ-critical. |
| K3 | The effective interior H, excluding isolated interior vertices, is connected and has excess ε(G)=2. It has exactly two original degree5 roots r,s, rs is absent, and every other effective original interior vertex has its complete original degree4. Original full B-touch holds. Every ignored original coordinate retains its actual allowed-color factor; adjacency-free isolated vertices give the full Col factor. |
| K4 | The **complete actual components** of H−{r,s} are exactly U,L,S. U contacts just one root; both L and S contact both roots. Each original component has nonempty actual boundary support and is one-sided. |
| K5 | L's actual boundary support is not contained in the two endpoints of any true frame edge; S's actual support is contained in the endpoints of some true frame edge, and hence is either that genuine pair or a singleton. S is not assumed to be a single vertex. |
| K6 | e=rb_i is the named original spoke. X has exactly V(G) and E(G)−{e}; U,L,S and every original contact, attachment and bridge are retained. |
| K7 | For the **same fixed original rejected literal β**, X=G−e=M **itself** is an inclusion-minimal β-rejecting core with its own root degrees (4,5). X cannot be replaced by a smaller independently selected core. |
| K8 | The original owner of U is r or s and its original root-contact count n_U≥1 is unrestricted; it need not be a unit. A vertex shared by r/s contact roles is one actual vertex and one tuple coordinate. |
| K9 | Named ordered contacts, ownership, original edges, actual attachments/supports, original bridges, rotation and frame order are fixed across all rows; a D5 or root exchange transports the entire datum. |
| K10 | All ten literal representatives, all sixteen ordered root pins including the diagonal and all empty fibres are retained. Each complete contact tuple retains **all** local preimages and every assembled full-graph lift. |
| K11 | For every original non-frame edge f of G, a Σ-critical witness is supplied: an original row γ_f∉Σ(G) and a complete G−f lift. Witness rows may differ between edges/pieces and may not be added as coloring capacity. |
| K12 | For every retained non-frame edge f of X, a complete X−f deletion witness at the **same β** is supplied. G−f and X−f have their own vertices/edges/rows/assignments; restoring e additionally checks the retained original r color. |

Col={0,1,2,3}. The ten literal representatives in order are `01012,01021,01023,01201,01202,01203,01212,01213,01231,01232`; q0,…,q4 have representative indices (6,4,3,1,0); T4 indices are {2,5,7,8,9}. The canonical rejected point sets are 941:Q(G)={0,1,3}, 933:Q(G)={0,1,2,3}. If the source uses another D5 presentation, these sets, actual supports and **all** lifts are transported together. Source: long-contract:125–159 and canonical:101–102.

### B3. Endpoint inventory

| ID | Complete quantifier and sufficient premise | Conclusion | Direct dependencies | Evidence / current status |
| --- | --- | --- | --- | --- |
| LONG-R | ∀(G,β,e,original datum) satisfying K_LONG, with U owner=r; every pair/singleton S and every permitted U incidence (including2). | No such source exists. Actual H_X−s is sole C={r}∪U∪L∪S; s is its only effective degree5 vertex. | SL-TOUCH; SL-STAR; actual sole-C join; X's own witnesses; t_s=0/1/2 dispatch to BASE(5)/(4)/(3); Gallai degree-list/palette theorem. | Adopted arbitrary-size paper exclusion. Canonical:348–362; LONG-R REPORT:15–143. Its 26 omissions /260 rows /4160 pins /250880 ambient r-fibres are finite interface calibration, source not triggered. |
| LONG-S | ∀(G,β,e,original datum) satisfying K_LONG, with U owner=s; every pair/singleton S, every positive permitted L/S root-incidence split and U incidence. | No such source exists. Covers all six (t_s,m_s,n_U) profiles under K_LONG. | DIRECT four profiles; FIBRE singleton and pair13/31 exclusion; historical q0→q1 four schedules; T2q0 three; T2q2 seven; T1 fourteen. D transfer is not a source-exclusion dependency. | Adopted arbitrary-size scoped paper exclusion. Canonical:364–415; DIRECT/FIBRE and four independent reviews; later canonical integration. No finite target source / source realization / new Lean / general N45 closure. |
| LONG-selected composition | ∀K_LONG sources, U owner∈{r,s}. | Selected complete U/long/short, original-spoke-omission, X=M same-β-minimal contract is impossible. | LONG-R + LONG-S; the two owner cases are exhaustive only under K4/K8. | Adopted scoped aggregate, **not** a third logically independent endpoint theorem. Canonical:402–406. |

The two endpoint count is appropriate. Do not count the six profiles or 28 schedules as extra theorem endpoints, and do not count the owner composition as a newly proved broader source identity.

### B4. LONG-R helper inventory (with smallest extracted sufficient premise)

| Helper | Quantifier / smallest known sufficient premise | Exact conclusion / dependencies / source |
| --- | --- | --- |
| SL-TOUCH | Every K_LONG source, both owners, both S support types. Original U,L each have ≥2 edge-disjoint shield edges and support equals their shield endpoints; all actual U/L attachments retained in X. | N_B^X(U∪L)=B, hence this selected X is full B-touch. It is **not** generic spoke-deletion inheritance. long-contract:83–92. |
| SL-STAR | Every K_LONG source; root not owning U; assume its original t=3, original full B-touch and H−root connected. | Original star has gaps1,1,3; all piece shields lie in its long3 face, contradicting U+L shield cost≥4. Thus t≤2; does not require S positive shield cost. long-contract:94–103. |
| SL-PG-pair ports | Every pair-support K_LONG source, whole-graph frame U012/L234/S40; three disjoint connected original pieces, owner–U contact, both roots–L/S contacts, actual attachment endpoints and planar disk. | Same original six-bag/nine-edge K3,3 proves owner spokes⊆{b0,b2}, non-owner spokes⊆{b4}; unary incidence need not equal1. Pair only; singleton uses a different argument. long-contract:116–123. |
| SL-R-CORE | K_LONG + U owner=r. | Actual sole C, all its vertices complete degree4 in X; s unique degree5; actual ordered contacts P have m_s=5−t_s distinct vertices. LONG-R:32–48. |
| SL-R-JOIN | Any actual same-edge decomposition C={r}∪U∪L∪S, no cross piece edges, actual attachment/spoke factors. All proper literal γ and all ambient (a,τ), then all16(a,b). | Unpinned-s C complete assignments are disjoint coproduct over retained-spoke-allowed r=a of the full U/L/S assignments avoiding a. Restriction/union gives exact full X lifts; all r fibres and empty cells retained. No degree4/minimality/disk/Σ premise needed for this identity. LONG-R:50–76. |
| SL-R-F | Connected complete-degree4 C, nonempty actual contact P, own fixed-β rejected X and own retained s-spoke same-β deletion witnesses; all assignments. | R_C nonempty by slack; retained s-spoke β colors distinct and F_C(β)=Col−β(N_B(s)), \|F_C\|=4−t_s. No second rejected row, no Σ(X)=933/941 assumption. LONG-R:78–91. |
| SL-R-MAP | Actual finite simple induced-C5 disk X, own edge-minimal three-color β obstruction, unique degree5 s, sole degree4 C with5−t_s distinct contacts, exact F_C; for t1/t2 actual retained hub path. | One whole-graph D5/S4 β→01012 transport satisfies BASE hypotheses. t0 needs neither exterior s−B path nor K4-free; t2 uses arbitrary **different** spoke colors/positions, no forced canonical positions. LONG-R:93–111. |
| SL-R-T0 | SL-R-MAP with t_s=0, five actual contacts, F_C=Col. | Four true palettes share coefficient τ; active forest leaves=2h+2k cannot equal5. K4 remains allowed. Contradiction in X. BASE no-spoke §4; LONG-R:115–120. |
| SL-R-T1 | SL-R-MAP with t_s=1, four contacts, F_C three colors, original retained s-spoke hub. | Two original disjoint active triangles and one original negative bridge; full degree4/branch recoloring gives3 mutually disjoint true boundary tethers; original retained edges produce K5 in X. BASE single-spoke-four §§1–5; LONG-R:122–128. |
| SL-R-T2 | SL-R-MAP with t_s=2, three contacts, complementary two-color F_C, distinct retained spoke colors. | One active triangle and three arbitrary/zero-length original bridge arms +3 original tethers yield retained-edge K5 in X. BASE two-spoke-three-contacts §§1–5; LONG-R:130–135. |

### B5. LONG-S exact profile and schedule partition

Under U owner=s, m_s+n_U+t_s=5 with m_s≥2,n_U≥1 gives exactly six ordered profiles. ORIGINAL counts are used.

| (t_s,m_s,n_U) | All-size proof branch | Completeness / unchanged boundary |
| --- | --- | --- |
| (0,4,1) | DIRECT SD-NS41 | All allowed actual splits, pair/singleton; C4 has3 true forbidden colors. |
| (0,3,2) | DIRECT SD-NS32 | All allowed splits, pair/singleton; C3 has≥2 forbidden colors, actual U supplies exterior path. |
| (0,2,3) | DIRECT SD-NS23 | Theorem dummy roles swap: original U3 is selected component, original C2 supplies exterior path; C and r fibres do not change names/data. |
| (1,3,1) | DIRECT SD-SP31 | C3 has exactly2 true forbidden colors; retained original s-spoke supplies hub adjacency. |
| (1,2,2) | FIBRE then T1 | Singleton and pair13/31 excluded. Remaining pair22 β=q3/q4, each7 schedules and two s-spoke positions b0/b2, total14 schedules/28 queries. |
| (2,2,1) | FIBRE then T2 | Singleton and pair13/31 excluded. Remaining pair22 β=q0/q2, each7 raw schedules; q0 previous4+new3, q2 new7. |

FIBRE residual frame is actual U012/L234/S40, e=rb4, t_r=1 (X no retained r-spoke), original r-split22 and s-split11; C={r}∪L∪S and complete original U are **two** actual H_X−s components. Every bridge/cycle/branch size is unbounded. Sources: canonical:376–406; FIBRE REPORT:142–186,216–302.

T1 βq4 proof uses original retained K5; βq3 proves S **has** exactly two actual vertices (it is not an input shortcut), and constructs q0/q1 complete same-source r≠2 lifts. For βq3 the nonempty object is a union over suitable (a,b); it does not claim each fixed root fibre nonempty. T1 independent REPORT:17–36.

T2q0 applies precisely to 933/0234,941/023,941/024. Original G accepts q1. Complete S transport makes q2 r=1 fibre empty; SF-QX gives complete q2 X-lift **union** nonempty, and each such lift restores rb4. It proves no per-fixed-pin nonemptiness, no q3/q4 restoration. T2q0 independent REPORT:11–31.

T2q2 derives β-local L and S seed assignments at **different r values**, then transports them into common q3/q4 frame and pins(0,3), uses target-row U strict slack, and joins actual complete preimage sets. Both L_X(q3;0,3) and L_X(q4;0,3) are nonempty and restored. q4 covers933/0124,933/0234,933/1234,941/024,941/124; q3 covers933/0123,941/023. These target existence proofs do not use SF-QX or historical finite-terminal for existence; β U-role still depends on SF-T2-ROLE. T2q2 independent REPORT:10–29.

## C. BR-SD：四個已採來源合同

### C1. 目前正式狀態，先於歷史 wording

四份 **1a／1c／1e／1g 均已正式採納**，共四個互相有不同 source domain 的 scoped exclusions。不是四份候選、不是父身份 closure。

| 定理 | 現行採納權威 | 原證明及獨立數學核查 | 層級 |
| --- | --- | --- | --- |
| BR-SD-1a | `docs/c5_excess_two_nonadjacent_unit_core45.md:444–486` | `audits/2026-10-11-br-sd-1a-0f181045/PROOF.md:10–85`；`agents/paper/REVIEW.md:9–117` | 任意有限大小紙面＋外部 Gallai；finite 只校準；actual source not triggered；Lean 0 |
| BR-SD-1c | canonical `488–543` | `audits/2026-10-11-br-sd-1c-fd6e1112/PROOF.md:8–159,180–191`；`agents/paper/REVIEW.final-v2.md:13–38` | 同上；counterexample 限撤 pair 或錯誤 cutpoint 推論 |
| BR-SD-1e | canonical `545–597` | `audits/2026-10-11-br-sd-1e-337d018b/PROOF.md:8–185`；`agents/paper/REVIEW.final.md:16–69,107–114` | 同上；原 PROOF 的 candidate 是當輪歷史，不是現在 status |
| BR-SD-1g | canonical `599–680`；`docs/history/2026-10-11-br-sd-1g-adoption.md:3–33` | `audits/2026-10-11-br-sd-1g-dbdc4c35/PROOF.md:8–147`；`audits/2026-10-11-br-sd-1g-adopt-6eae3597/REVIEW.md:13–30`、`agents/proof/REVIEW.md:42–148` | exact source 八項合同正式 ACCEPTED；review 原文的「未正式採納」仍留歷史；actual source NOT TRIGGERED；Lean 0 |

採納不來自 custody PASS 或 fixtures。原 1g-adopt 的 `ADOPTION_DECISION.md:5–6` 只裁 ACCEPTABLE、不當時採納；現在狀態由 canonical 及其後 adoption history 決定。

### C2. 完整量詞的共同 source macro BRC

以下 BRC 是來源合同的**純文字共同因式**，不准用「證明沒用到」刪掉它。每個 exclusion 的命題均為：

> 對每一份任意大小有限原 G，以及同一份具名資料 `(B,Col,Σ,r,s,e,M=X,β,L,S,p,q,全部附件／rotation／witnesses／relations／fibres／full lifts)`，若 BRC 的全部條件、下面的共同骨架及該分支條件同時成立，則推出矛盾。

1. **原來源／完整 Σ。** G 是有限簡單 disk 圖，`B=(b0,…,b4)` 是指定 ordered induced C5 外邊界。完整有序 `Σ(G)=933／941`，或以一份 D5 作用共同搬運整圖、框位置、root roles、全部接線和 relations 的像；不單獨商去框位置。`ε(G)=Σ_{y∈H_G}(deg_G(y)−4)=2`。每條原非框邊 f 都 Σ-critical，即 `Σ(G−f)⊋Σ(G)`；保 f 自己的完整刪邊 witnesses（解除的原列可隨 f 不同），不是以某一 β 見證包代替全部 Σ。
2. **有效內圖／degree／touch。** effective H_G 連通，恰有原不相鄰 degree5 roots r/s，`rs∉E(G)`，其餘有效原內點完整 G-degree4；degree 包含原全部 B 附件。原 full B-touch 即五個 b 都由原內部碰到。effective-H 忽略的原內圖孤立點 Z 仍保原頂點座標、B 附件及完整允許色因子。
3. **完整 pieces。** `H_G−{r,s}=L⊔S` 恰為兩份完整原 mixed 連通分量，各接兩 roots，U=0；兩份 one-sided（刪該 piece 後 effective H 非空連通），原 actual support 非空。L long，即 `N_B^G(L)` 不包含於任何真框邊兩端；S short，且更精確地 `N_B^G(S)=T_B={b_i,b_(i+1)}` 恰同一真框邊的兩端。S 全部原點的 B 附件 subset T_B，完整聯集恰 T_B。不是 S 單頂點，亦不是僅色數／marginal。
4. **原 exact-S／M 自身最小性。** e=`rb_j` 是 r 唯一原 B-spoke；`V(M)=V(G)`、`E(M)=E(G)−{e}` 且 `X=M`。對同一 literal proper、恰用三色的 β，M 自己拒絕 β 且自己是保 B 的邊集 inclusion-minimal β-core；每條 retained 非框邊 f 有 M−f 的**同一 β**完整刪邊 witness。G 的 Σ-critical 不代替 M 的拒絕或最小性。原 G 所有其他點／邊完整留下。
5. **M degrees／contacts／sole C。** M 中 s 完整 degree5，其餘有效內點完整4。s 原三條 B-spokes 全留，原內鄰恰相異有序 `p∈L`、`q∈S`。`C=H_M−s={r}∪L∪S` 是實際 sole connected component；r 對 L/S 各有兩原 contacts（split22），`d_C(r)=4`、`N_B^M(r)=∅`。45／54 僅以整份資料共同 root-role 交換處理。
6. **所有原坐標與證據。** 全部 original vertices／edges、named／ordered／shared contacts 的單一 actual 座標、actual attachments／supports、完整 ownership、原 bridge 身份／端點、rotation／disk embedding、同一 literal 四色 `Col` 和 β 全保；G、M、各刪邊圖分別保自己的 witnesses、完整 relations／fibres（含空 fibres）與 full lifts。不得只保 marginals、拆 shared coordinates、獨立改色各 block／piece、用抽象 lists 或容量列替代原來源。

共同來源：canonical `78–103,451–468,497–509,555–570,614–647`。定義補足：`docs/c5_common_language.md:32–40`（critical／one-sided／effective-H）；`docs/c5_unary_shield_budget.md:30–41`（full touch／support）；`audits/2026-10-09-n45-s/REPORT.md:22–28`（long／short）；完整 witnesses 量詞見 `audits/2026-10-10-n45-s-long-contract/REPORT.md:29–35`。

### C3. 共同骨架 SK，以及四個完整分支差異

**SK。** 同一原 C 的骨架 C0 原邊恰三個 maximal 原 cycle blocks J1/J2/J3、唯一環間原 bridge uv、兩原 simple bridge arms，無額外骨架邊。環長各任意奇數≥3；`J1∩J2={r}`、J3 與兩者不交。`u∈J2−{r}` 私有、`v∈J3` 私有，uv 是唯一環間 bridge。p-arm 在 J1 私有錨點 a1 到 p，q-arm 在 J3 私有錨點 a3 到 q，原邊長 h/ℓ 各為任意非負整數。h=0 只作原同點 `p=a1`；ℓ=0 只作 `q=a3`。允許 `a3=v`，不准偷加 `a3≠v`。正長 off-cycle 臂點與三環、另一臂及非本臂端點互斥；p≠q。`J1−r`／p-arm off-cycle 屬原 L；`J2−r`、uv、J3／q-arm off-cycle 屬原 S。所有骨架原 edges／blocks／bridge 及附件身份全保。

| ID／完整分支命題 | 分支量詞、最小已知充分 source premise | 結論／實際短證明 |
| --- | --- | --- |
| **BR-A** | BRC+SK，`C=C0`，無任何其他 C block／旁支。J1/J2/J3 各奇長無上界、h/ℓ≥0、a3=v 許可 | source 不可能。兩原 private witnesses `w1∈J1−{r,a1}`、`w2∈J2−{r,u}` 各存在、單 block、非 s-contact；lists 含同一 D，shared r palette 矛盾。來源 canonical `451–484`、1a PROOF `44–85` |
| **BR-C** | BRC+SK，恰一份有限非空 off-skeleton 原 W，`V(C)=V(C0)⊔W`、C[W] 連通、`N_C(W)={x}`、`x∈J1∪J2`；可有多條 x–W 邊，無第二接點、cross edge、額外 s-contact、其他旁支／接線。W 在 J1/J2 分別屬完整原 L/S（x=r 列先超 degree4 排除）。J3/q 原附件／接線不變：其他 block 接 J3 至多 v/a3；q 為该側唯一 s-contact；q-arm 各邊是原 bridge，a3 外全部臂點（含 q）只有路徑 C 鄰居。所有奇長、h/ℓ、有限 W 大小及允許 x 均全稱 | source 不可能。**最短 route 為末端引理**；degree4 首先排非法 x，全部其他 x 都由未受影響 J3/q pair terminal 排除，無須三路分類。來源 canonical `497–533`、1c PROOF `115–159,182–185`；最終 reviewer `REVIEW.final-v2.md:29–34` 明確覆核全接點 |
| **BR-E** | BRC+SK，恰一份有限非空原 W，`V(C)=V(C0)⊔W`、C[W] 連通、`N_C(W)={x}`、`x∈J3∪q-arm`；多条 x–W 邊許可。W 屬完整原 S，其全部原附件在同一 T_B，S 完整 support 聯集仍恰 T_B。無第二接點、W–s 邊、cross edge、其他旁支或 J1/J2 新接線。任意全部三環奇長、h/ℓ≥0、有限非空 W、全部允許 x 及 a3=v | source 不可能。a3=v 且 x=a3=v 的零臂／正臂都已飽和，非空 W 超度；其餘以單接點保持兩 private witnesses，引用 shared-D 矛盾。來源 canonical `555–591`、1e PROOF `45–185`。**不依 terminal lemma** |
| **BR-G** | BRC+SK，額外 `J1=(r,a1,x1)` 指定 triangle；J2/J3 仍任意奇長≥3。恰兩份原有限非空 Wi，`V(C)=V(C0)⊔W1⊔W2`、C[Wi] 連通、`N_C(W1)={x1}`、`N_C(W2)={x2}`，`x2∈J3∪q-arm`。W1 属原 L、W2 属原 S；多条 xi–Wi 原邊許可。無 Wi 間邊、第二骨架接點、额外 s-contact、第三旁支、cross edge 或其他 blocks 接線。每個 y 原附件 A(y) 和 `4=d_C(y)+\|A(y)\|+1[sy]` 保留；全部合法 x2、mi、原具名重合、h/ℓ≥0、有限 Wi 全稱 | source 不可能。W1 耗掉 J1 唯一 private witness，W2 可破壞 J3/q terminal；J2 w2 仍保，實際 pair 迫 `P_J2={T,D}`。S 所有其他點需要 T/D，q 含 T 禁 D；exclusive blocks 不可跨 J2，有限 incidence tree 交替不回頭路矛盾。來源 canonical `611–674`、1g PROOF `97–147`、fresh review `REVIEW.md:22–30` |

四個 BRC+分支是各自**最小已知已採納 source contract**，沒有證明它們是邏輯上必要／全球最弱。下節可以明列實際 used premises，不能把 used-premise 抽取改寫成新的來源排除採納。

#### 度數容量及允許重合，不能在壓縮時漏掉

接 W 的具名 x，令 `m=|N_C(x)∩W|≥1`、k 原實際 B 附件數、t=1[sx]。同一候選原來源必有 `4=d_C0(x)+m+k+t`。**不是向舊已滿度圖加邊，再刪附件補 k。**

1c：x=r 骨架 degree4，任何 m≥1 即超度。x=a1（h=0:2+1／h>0:3+0）或 x=u(3+0) 只允 m=1,k=0、首 W-block 為 bridge。其餘 J1/J2 私有點 d0=2,t=0，m=1,k=1 或 m=2,k=0。首 W-block 只有一份，因 C[W] 連通；不能把 m=2 畫成兩獨立首 bridges。1c PROOF `37–54`。

1e/g 的 q-side x（g 改稱 x2/m2）：

| x | d0+t | 合法非空 W 必要 m/k |
| --- | --- | --- |
| x=a3=v，ℓ=0 | 3+1 | 全排，k=−m<0 |
| x=a3=v，ℓ>0 | 4+0 | 全排，k=−m<0 |
| v≠a3 | 3+0 | m=1,k=0 |
| a3≠v，ℓ=0，q=a3 | 2+1 | m=1,k=0 |
| a3≠v，ℓ>0 | 3+0 | m=1,k=0 |
| ordinary J3 點 | 2+0 | m=1,k=1 或 m=2,k=0 |
| off-cycle q，ℓ>0 | 1+1 | m=1,k=1 或 m=2,k=0 |
| 正長臂內點 | 2+0 | m=1,k=1 或 m=2,k=0；ℓ=1 內點列空 |

來源 1e PROOF `47–81`、1g MAPPING `119–162`。Wi 內點无 s-contact。W2 或原 S-owned W 的 k≤2，故 C-degree≥2，degree1 葉不合法；W1 在 L 不受 pair 上限，C-degree1 可要求三 B 附件（只是一份必要配置，非 source realization）。1g x1 d0=2,t=0，只允 m1=1,k=1 或 m1=2,k=0，x1 不得與 r/a1/p/q 重合，source `MAPPING.md:105–117`。

## D. SD-A、三項二連通適用性與直接外部依賴

| ID／完整量詞及最小已知充分前提 | 結論、依賴與來源 | 證據／目前狀態 |
| --- | --- | --- |
| SD-A：∀有限簡單 ordered induced-C5 disk M，H=M−B 二連通且至少3點，恰一原內點 s 完整 M-degree5、其餘完整4；∀proper 四色 β，若 M 拒 β | d_H(s)=2 且 H−s 為 Gallai tree。完整 degree 含 B 附件；不需 minimality、T4、Σ933/941 或先驗 tight lists。Cranston–Rabern 正式 Main Lemma／Theorem B + 同圖 K4/B→K5 + Gallai。見 [interfaces§7](../../docs/c5_degree5_interfaces.md)、[SD-A報告§1–7](../../audits/2026-10-11-c5-single-deficit-biconnected-5e7a5ffd/REPORT.md) | A+正式期刊 E；960 assignments、758 minor controls 為 F；actual disk minor target not triggered；新Lean0 |
| APP-LL：∀C_S、原U=0、兩原mixed都long；另供 actual X=M 自身同β minimal／拒絕、完整4/5/4與 H_M 二連通 | 原三-spoke star 的長3面無法容兩份≥2盾弧，迫 s內度≥3；SD-A迫內度2，矛盾。原盾費仍收原G，不從X繼承幾何 | A限定subset，父兩long仍OPEN。canonical:432；[適用性表](../../audits/2026-10-11-single-deficit-applicability-804e3b0b1b/APPLICABILITY.md)凍結的 A待驗conditional措辭保留 |
| APP-LS1：∀同上完整非相鄰來源，但一long L／singleton-support short S、原U=0、actual X=M、完整4/5/4及 H_M 二連通 | SD-A給 s-contact各1；r每側≤2，S總incidence≤3。S04／S3在完整原full-B／critical-contact前提下與最小拒絕衝突 | A限定subset；非二連通與完整父身份仍OPEN。canonical:433，適用性表10–11 |
| APP-AD2：∀有限簡單原ordered induced-C5 disk G，完整Σ933/941或整圖D5像、Σ-critical、ε=2，有效H連通full-B；原相鄰degree5 roots r/s（保原rs）、其餘有效內點完整4，H−{r,s}恰兩完整one-sided mixed且原support非空、兩側positive contacts；具名單側unit spoke或整unit省略保rs與兩mixed。另供actual X=M自身同一properβ minimal／拒絕、M中s唯一完整5而其餘有效內點完整4、H_M二連通；全部原ordered/shared資料、附件、witnesses及full lifts保留 | 原 rs及兩mixed contacts迫 d_H(s)≥3，與SD-A的2矛盾。原adjacent合同沿[適用性報告](../../audits/2026-10-11-single-deficit-applicability-804e3b0b1b/REPORT.md)逐项保留；此條不套 C_S 的rs不存在前提 | A限定adjacent subset；不新增完整AD2／N45閉合。canonical:437–438 |
| E-Gallai：∀有限非空connected simple C及degree assignment L | 不可染的tight／blockwise-uniform刻畫、incident-disjoint palettes；見 COMMON C3及BR GA。直接 primary：[Dvořák講義](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，印刷p5–6；frozen hash見原SOURCE | E（作者講義），本輪live PDF核讀；不宣稱期刊或Lean |
| E-CR：Cranston–Rabern單缺額二連通分類／AT⇒choosable 的正式版範圍 | 只流向 SD-A／APP；不流向 BR-SD。正式版 Theorem B及Main Lemma的精確前提／圖D由原SD-A查證採用；文本抽取≥3可能誤為>3，原視讀finding保留 | E（EJC24(3),2017,#P3.29），[正式PDF](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v24i3p29/pdf/)，原report印刷頁2–4；本輪沒有重證外部分類 |

## E. canonical 33行原索引的覆蓋與剩餘必要命題

下列保持原 bundle 的結論與邊界，用於核對沒有遺漏來源 ID；**不是把每行登記為一個新定理**。完整量詞按 A 的 C_S/C_U、各支完整合同、B 的 K_LONG 或 C 的 BRC/SK 解讀；條件特化詳下補表。這些既有結論的狀態以 canonical 為 A（其中 profiles 為必要身份、工具為 F）；本輪索引名為 P。

| CLAIM | 已採納的精確結果 | 界線 |
| --- | --- | --- |
| N45-S-01／N45-U-CROSS | ε(X)=1；保完整 Σ minimalize 後用 E2，Q(X) 只能為 Q(G) 內的空集、單點或相鄰 pair；含 core β 的七格必要表保留933 q2 | 必要 masks 不給 disk 實現；X=M 才另有 β-critical⇒Σ-critical |
| N45-S-02／N45-U-CAP | 共同拒絕 β、每個 b∈E_s 的 degree4 側完整 joint 有 D+O+δ+o+λ=0；五項各零，mixed raw columns 滿額、互斥、聯集恰 E_r^X | 要完整 tuples 及 E_s 非空；不從 marginals 或其他列補容量 |
| N45-S-03 | 恢復 spoke 色 c：c∉E_r^X 時唯一 retained side blocker 給 O=1；c∈E_r^X 時每欄唯一 mixed owner 給 λ=1 | owner 可隨欄變；unary blocker 不滿足重色 spoke 的 E4-D 前提 |
| N45-S-04 | 原 singleton mixed support、兩側 incidence 正且總≤3 時，固定 support 色的 S3 軌道與 N-diagonal 迫完整 compatibility 為 Col² | 不排總 incidence≥4；不獨立正規化 pieces |
| N45-S-05 | 指定 S 身份的原 u=2 子型不存在；兩 short 時總 mixed incidence≤5 且兩份原 support 都是真 edge-pair | 含 long 用2+2+2；兩 short 用1+1+2+2，省略原 piece 仍付原費；spoke 不收 piece 費 |
| N45-S-06 | S 身份兩 short 時恰一份原 unary，unary 側／無 unary 側 mixed incidence 為2／3；原輪只留 LOW／HIGH 必要身份 | 原三 spoke star 的唯一長3面論證；不搬 U4 retained44／O11 下界；限定 LOW／HIGH 分別由 LOW1–LOW2／HIGH1–HIGH3 覆蓋排除；只關§1精確 S 的兩 short 分支 |
| N45-U-REL | 原 U 的 contact palette T_U 非空；T_U 單點才 F_U 單點，否則 F_U=∅；整 U 省略與刪唯一 contact 的 root-pair 集合相等 | 在新接受 γ∈Σ(X)∖Σ(G)，全部 X lifts 的 r 投影與 T_U 同 singleton；core 拒絕 β 不迫 F_U 非空 |
| N45-U-WIT | 每份原 piece 由自己的 critical contact 給拒絕接回的 outside witness；原 unary 有避自身外路，省略 U 仍收原盾弧≥2 | 不要求不同 pieces 用同一列，但原圖與幾何不變 |
| N45-U-S3 | 原 one-sided mixed、完整 degree4、full B-touch、原 critical-contact witness、兩側正 incidence 且總≤3，則 actual support 至少二點 | Gallai/K4 tethers／末端計數／triangle K5 bags，另有 N-empty＋N-diagonal＋S3 交叉證明；總≥4未涵蓋 |
| N45-U-U2 | 指定整 U 省略身份的原 u=2 子型不存在 | 原 U 仍收費；有 long 先排，兩 short 再由低 incidence 支援下界收1+1+2+2 |
| N45-U-SHORT | 指定整 U 省略身份不能有兩份 short mixed | 排兩 unary 後 X 無 unary，共同未用色 D 與兩份原 short 的完整 diagonal lifts 接回 X，違反 β 拒絕 |
| N45-U-RES | 整 U 省略化約為唯一原 U、一 long L、一 short S；pair／singleton 支援由 LP／SS 分別排除 | 化約、LP、SS 的完整前提逐項保留，合成只關本頁 U 身份 |
| N45-PG-01／03／RES | 原2+2+1有十個 whole-frame named partitions；L/S 原 r–s 路給 Jordan cycle與非 bridge contacts；八種 spoke sets／56正 incidence profiles | 八張 embedding與56 profiles只作抽象控制／必要身份，沒有有限正常形或來源實現 |
| N45-PG-02 | 共同框 U012／L234／S40 下，三組原 K₃,₃ bags 迫 N_B(r)⊆{b0,b2}、N_B(s)⊆{b4} | 保每條原附件／contact；minor只證非平面 |
| N45-PG-04／05 | core β 的各 raw column 非空迫 s-contact 附件色不在 E_s；排掉 edge-pair 支援、整份 S 單頂點子型 | 頂點數一與 singleton support 分開；逐欄前提不可略 |
| N45-PR-TRANSPORT／ENDPOINT／SATURATION／ESCAPE／FORCING | 全 lifts 的 support-compatible 色雙射、原 hub endpoint 接回、滿額 contact 色集、接受列 escape、singleton 投影的逐欄一單位身份 | 各自充分前提見 PA §5；ENDPOINT 必須是完整原 piece、全部內鄰為指定 owner roots且完整 degree4；不給指定 coloring repair或來源實現 |
| N45-PR-UNTOP／LP-EXCLUSION | 原 U 盾中點未接 X 內部，迫 β=q_m；X−s 為唯一原 degree4 分量，接回既有單-root (5)/(4)/(3) 排除 | 任意大小 paper＋明列 BASE／外部 Gallai；只關 N45-U-LP，沒有新 Lean |
| N45-SS-COST／UNTOP／U3／U2 | 原 U/L 盾費只容(2,2)、(2,3)、(3,2)；長3的兩內點迫Σ(X)=Ω，長2迫β=q_m | singleton S不收pair費；長3 support可有四點，沒有套LP三點前提 |
| N45-SS-X-CORE／COMPONENT／SPOKES／T0／T1／T2／EXCLUSION | X自己minimal、完整degrees及實際sole C；原spokes／精確F_C接回三份BASE排除，N45-U-SS全排 | SSA十一項paper成立；SSG四項幾何／改色另核；SSC只核完整性，SS source count未計算 |
| N45-U scoped composition | 已採納U-U2／SHORT／S3／RES、LP與SS窮盡§1精確整U省略身份，該身份不存在 | 不是一般U省略、spoke省略、原55或全部N2／E；SSA§8獨立核覆蓋 |
| LOW1-CORE／COMP／JOIN／F／MAP／EXCLUSION | X=G−rb_i=M 自己 minimal；U 全留，X−s 恰 sole C，三原 contacts、二異色 s-spokes與精確 F 接回 BASE 原 K₅ 排除 | 完整 LOW1 契約、原 U incidence1；L1A／L1R 各核六 claim，外部 Gallai 明列；LOW2／HIGH／long 未涵蓋 |
| LOW2-CORE／COMP／JOIN／F／MAP／EXCLUSION | 原 U 的兩 r-contacts 與 cycle 全留；X=G−rb_i=M 自己 minimal，r 無框邊，sole C 的完整 join／精確 F 接回 BASE 原 K₅ 排除 | 完整 LOW2 十二項契約；L2A／L2R 各核六 claim；BASE／外部 Gallai 明列，工具 PASS 不證 paper |
| S-SHORT-U-LOW scoped composition | §1 精確 S 身份中，LOW 的原 U incidence／r-spokes 只有(1,2)、(2,1)，各由完整 LOW1／LOW2 排除 | L2A §7 獨立核逐項契約與窮盡；不關 HIGH、long、其他 core 或全部 S／N2／E |
| HIGH1-CORE／COMP／JOIN／RESTORE／F／MAP | X自己的45／54身份；實際C與U的(2,1)完整接合、全部r色fibres與原e恢復條件；BASE (2,1)的排除／指定X延拓分清 | 全部H1–H13；X指定延拓不提升為G；H1A／H1R各核十claim，工具不裁paper |
| HIGH1-K33／ARC／REJECT／EXCLUSION | 原G的六bags九鄰接迫P/Q支援邊頂點互斥；原U盾弧長2、support連續三點；同列未用D的完整G lifts迫Q(G)⊆該三點，矛盾完整933／941 | 任意大小paper＋明列BASE／Gallai信任；只關U incidence1在s且s兩spokes的HIGH1，無新有限來源或Lean |
| HIGH2-CORE／COMP／JOIN／RESTORE／F／K33／ARC／MAP／BRIDGE／SPLIT／PALETTE | 原雙 U-contact／single s-spoke；完整(2,2)接合保 r fibres，原 O′ 補 K₃,₃、完整 W 支援及 rooted assignments 成立 | 全部 H1–H13；H2A／H2R 紙面核對，H2C 只核工具，原錯量詞另列 finding |
| HIGH2-EXCLUSION（精化） | 每 proper 三色 γ 在原 U 三點 T 見三色時，原 r=s=Dγ 的完整 G lifts 含恢復 e；Q(G)⊆B−T，故至多兩拒點 | 只縮窄接回構造的 γ 量詞；JOIN／RESTORE／PALETTE 仍保全部 proper γ；不改原 worker |
| HIGH3 scoped exclusion | X自己 minimal、s無spoke、實際 C/U contacts=(2,3)，完整覆蓋迫三接點 U 至少兩禁色；原 X K₅ 排除 | 完整 K1–K13；H3A／H3R／H3G 獨立核 BASE no-spoke §§1–3、5，無新充分前提 |
| S-SHORT scoped composition | §1精確 S 的 LOW兩支與 HIGH三支互斥窮盡，各自完整契約排除，故兩原 mixed 都 short 的身份不存在 | H2A及父端核覆蓋；含long、其他core身份、一般N2／E均未關 |
| BR-SD-1a scoped exclusion | N45-S-NOU-LS-PAIR 的 split22／共用 r 雙環／三環單 bridge 無旁支精確合同不可能成立；任意奇環長與原外臂長 | 完整前提見§2.11；獨立紙面驗證、封存與發布已完成，不依 SD-A／二連通；父身份仍 OPEN |
| BR-SD-1c scoped exclusion | 同一 N45-S-NOU-LS-PAIR／split22 原三環單 bridge 骨架，新增一份有限非空原 pendant W 只接 J1/J2，保 actual S pair support 及未改動 J3／q 外臂的精確合同不可能成立 | 任意奇環／p、q 外臂長／有限 W 大小及所有允許接點；完整前提與局部引理界線見§2.11，父身份仍 OPEN，無新來源或 Lean |
| BR-SD-1e scoped exclusion | 同一 N45-S-NOU-LS-PAIR／split22 原三環單 bridge 骨架，恰一份有限非空原 W 唯一接 J3／q 外臂、保 actual S pair support 及完整原 degree／資料的精確合同不可能成立 | 全部允許接點、任意奇環／p、q 外臂長／有限 W 大小及具名重合；完整前提與 private-witness preservation lemma 界線見§2.11，不依1c terminal lemma，父身份仍 OPEN |
| BR-SD-1g scoped exclusion（雙原旁支／J2 屏障） | 同一 N45-S-NOU-LS-PAIR／split22 原三環單 bridge，J1 指定 triangle，恰兩原 W1/W2 分別唯一接 J1 的 x1 與 J3／q 臂的 x2；完整精確來源合同不可能成立 | 任意原 J2/J3 奇長、可零長 p/q 臂、有限非空 Wi 大小、合法接點與重合；S short／actual pair、M 自身同 β minimal 且拒絕及全部原資料全保，完整八項合同見§2.11。父 OPEN，actual source NOT TRIGGERED，無新 Lean |

| 補充 ID／完整局部量詞與充分前提 | 精確結論、依賴、原來源 |
| --- | --- |
| CROSS：∀C_S/C_U，對X的完整Σ保B取Σ-minimal derivative（若X=M另有自身Σ-critical），ε(X)=1 | E2使Q(X)只可能Q(G)内空集／singleton／相鄰pair；保coreβ七格含933q2。不給必要mask的disk實現。原[S§3](../../audits/2026-10-09-n45-s/REPORT.md)、[U§3](../../audits/2026-10-09-n45-u/REPORT.md)；依E2，見canonical108 |
| SPOKE-ONE：∀C_S，固定同一拒β、每個b∈E_s與完整raw columns，恢復e的色c=β(b_i) | c∉E_r^X由唯一retained-side blocker給O=1；c∈E_r^X由該欄唯一mixed owner給λ=1。owner可隨欄變；unary blocker不能冒用E4-D重色spoke。原S03、canonical110；依B-C2逐欄零slack |
| PG-PART：∀END-U-LP合同，原盾(U,L,S)邊長(2,2,1)，每個named原partition與所有whole-frame D5/root搬運 | 取a mod5、d=±1，U support=(b_a,b_(a+d),b_(a+2d))及前兩原框邊，L support=(b_(a+2d),b_(a+3d),b_(a+4d))及接著兩邊，S support=(b_(a+4d),b_a)及最後邊；恰10原named partitions；共同框U012/L234/S40。原[PG§2](../../audits/2026-10-09-n45-pg/REPORT.md):52–97；10不是來源數 |
| PG-GEOM：∀同上合同／共同框，保原L/S的完整r–s路及原attachments | L/S兩路給原Jordan cycle；每piece內兩contact間路上的邊／root-contact非H bridge；不把contraction圖當染色替身。原PG§4:134–158；只證原幾何身份 |
| PG-SP：∀同上原幾何、全部原spokes及attachments | 三組原K₃,₃ bags迫 N_B(r)⊆{b0,b2}、N_B(s)⊆{b4}。省略整U時仍保原G的spokes限制；原PG§3:98–132 |
| PG-ATT：∀END-U-LP，原sameβ零slack且每個raw mixed欄非空，actual s-contact與其每條B附件 | 附件β色不在E_s，否则該contact不能避固定s色而raw欄空；對shared contact保一原座標。原PG§5:160–186；不許把各contact marginal相乘 |
| PG-RES：∀滿PG-SP及完整原 degree identities的positive incidence配置 | 原 r-spokes任一subset{0,2}、s-spokes任一subset{4}共8 sets；m_r=4−t_r、m_s=5−t_s，各mixed r/s allocation正，合計(3+2+2+1)(4+3)=56必要profiles。不是survivors／actual sources；原PG§7:202–235；有限正常形／來源實現另負義務 |
| SS-COST：∀END-U-SS原full contract | U/L原費給有序(2,2),(2,3),(3,2)，singleton S不按pair收費；長3的support可4點。原SSA§3–4與canonical166–180；不得套LP三點前提 |
| SHORT-NEC：∀C_S且兩原mixed都short | S05/06給唯一原unary、兩true-edge supports、unary側mixed2另一側3；LOW/HIGH後續逐合同窮盡。最終COR-S-SHORT已採，原必要化約不是再一份獨立全排 |

## F. LONG-S 全部原 claim labels 與採納更正

### F10. Complete LONG-S claim-label inventory (61 labels, not61 endpoint theorems)

This appendix keeps every adopted worker label so a reviewer can map source proofs to the compressed organization. The last column transcribes recorded dependencies where present, otherwise the recorded premises; it is not a claim that the historical JSON was a complete DAG. The explicit corrected DAG and inferred SF edges are below. All source-specific SD/SF/T1/T2Q0/CQ2 claims inherit K_LONG and the explicit profile/frame domain in 模組B2/B5; the quantifier column retains any smaller generic helper scope. For TF, the actual decomposition premises are in COMMON C1與D採納界線以及原source `transfer-proof.md`:34–39,101–185; TF-BLOCK/FIBRES/COLOR/RESTORE identities do **not** require K_LONG. Generic CQ2-SLACK takes its displayed connected degree-list premise, rather than all source assumptions. A named original-graph minor always requires the displayed actual disjoint/connected bags and exterior paths, never just a count.

The current status of every label below is accepted in its recorded scope (with FIBRE/T1/q2 corrections); the worker's candidate/pending field is preserved historical evidence. There are12 SD+15 SF+9 T1+9 T2Q0+9 CQ2+7 TF labels =61, comprising54 paper/necessary-condition/aggregate/helper labels,5 finite-calibration labels and2 historical-domain ledger labels (SF-RESIDUAL,TF-DOMAIN). This is a label inventory, not a set of61 independent mathematical results.

#### DIRECT

Domain / smallest verified contract: all four DIRECT profiles; full K_LONG. Complete explicit premises: `audits/2026-10-11-n45-s-long-s-direct/claims.json`. Current adoption: `audits/2026-10-11-n45-s-long-s-review/direct-paper-review.md:17–28`.

| Label | Complete stated quantifier | Exact conclusion | Recorded premise / proof dependency |
| --- | --- | --- | --- |
| SD-CORE | For every finite arbitrary-size G satisfying the common contract and any one of the four profiles. | Actual X has unique full degree5 root s, all C/U vertices full degree4, and exactly the two complete named components with original ordered contacts. | long-contract K1-K12 retained with K8 strengthened to original U owner=s; Only original e=rb_i omitted; X=G-e=M itself beta-minimal; same literal beta; Actual components H_X-s are full C={r}∪L∪S and full U; All original named/ordered/shared contacts, attachments/supports, ownership, bridges, rotation and literal frame retained; All ten complete relations, preimages, 16 root pins, diagonal, empty fibres, full lifts and isolated-point factors retained |
| SD-JOIN | For every such G, every proper literal gamma, every ordered (a,b)∈Col² and every ambient contact tuple. | J1/J2 preserve all local preimages, r fibres, empty cells and full lifts; J3 is exact original-spoke restoration. | SD-CORE |
| SD-F | For every such G and its rejected literal beta; arbitrary gamma for nonempty unpinned relations/capacity/contact-release. | Full-assignment F_C∪F_U=A_s(beta), both private differences nonempty, \|F_C\|≤m_s, \|F_U\|≤n_U; spoke colors outside both F; all contact releases have full assignments. | SD-CORE; SD-JOIN |
| SD-OUT | For every such no-spoke X and selected actual component D=C or U. | Q_U within full original U avoids C; Q_C within original L⊆C avoids U; both retained original s-B paths exist without e or r-spokes. | SD-CORE; SD-F |
| SD-K4 | For every such X, for each actual component D=C,U and any true forbidden color d∈F_D(beta). | No D has a K4 block; no-spoke uses the other actual component's path, single-spoke uses retained original sb_j, with four original tethers. | SD-CORE; SD-F; SD-OUT |
| SD-THREE | For every selected actual degree4 component D with exactly three contacts and at least two true forbidden colors, in the stated contract. | One original active triangle, three arbitrary-length bridge arms and three original mutually disjoint boundary tethers yield a retained-edge K5 once the verified outside hub adjacency is supplied. | SD-K4; SD-F |
| SD-FOUR | For every actual C with four contacts and three true forbidden colors, in the stated contract. | The common palette coefficient forces two disjoint original triangles and exactly one original bridge with no contact arms; three original tethers and Q_U give retained-edge K5. | SD-K4; SD-F; SD-OUT |
| SD-NS41 | For every G satisfying the full common contract with t_s=0,(m_s,n_U)=(4,1), either pair/singleton S and every permitted incidence realization. | Such X identity does not exist: actual C maps to no-spoke four-contact three-forbidden exclusion; retained X edges certify K5. | SD-FOUR; SD-JOIN |
| SD-NS32 | For every G satisfying the full common contract with t_s=0,(m_s,n_U)=(3,2), either pair/singleton S and every permitted incidence realization. | Such X identity does not exist: \|F_C\|≥2, original C maps to no-spoke three-contact exclusion using original U outside path. | SD-THREE; SD-OUT; SD-JOIN |
| SD-NS23 | For every G satisfying the full common contract with t_s=0,(m_s,n_U)=(2,3), either pair/singleton S and every permitted incidence realization. | Such X identity does not exist: \|F_U\|≥2, original U is theorem selected component; original C identity and all r fibres retained, Q_C supplies final original adjacency. | SD-THREE; SD-OUT; SD-JOIN |
| SD-SP31 | For every G satisfying the full common contract with t_s=1,(m_s,n_U)=(3,1), either pair/singleton S and every permitted incidence realization. | Such X identity does not exist: exact two-forbidden C and singleton-forbidden U map to single-spoke (3,1), with actual retained sb_j giving K5 final adjacency. | SD-THREE; SD-JOIN |
| SD-COVER | For each of the four specified profiles, every permitted positive scalar L/S incidence split and every original actual named realization satisfying the complete contract, independently of piece size or branch length/depth. | The four profiles are covered without restricting pair/singleton S or actual contacts; all other profiles and general N2/E are outside scope. | SD-NS41; SD-NS32; SD-NS23; SD-SP31 |

#### FIBRE

Domain / smallest verified contract: profiles(1,2,2),(2,2,1); full K_LONG; SF-T1-MAP partition is corrected12+4+10+4; SF-RESIDUAL adds SF-T2-Q0-Q1-RESTORED. Complete explicit premises: `audits/2026-10-11-n45-s-long-s-fibre/claims.json`. Current adoption: `audits/2026-10-11-n45-s-long-s-review/fibre-paper-review.md:22–36`.

| Label | Complete stated quantifier | Exact conclusion | Recorded premise / proof dependency |
| --- | --- | --- | --- |
| SF-JOIN | Every finite source satisfying K; every proper literal gamma; all 16 ordered r/s pins | Restriction/union identifies the complete C/U product at one s color with all X lifts, retaining every preimage, r fibre, empty fibre and isolated free factor. | K1–K12 exactly; original U owner=s; (t_s,m_s,n_U)=(1,2,2) or (2,2,1); actual original vertices/edges and contacts; no s pin before constructing C/U |
| SF-PRIVATE | Every such X; every retained s-spoke and every component/contact incident edge | F_C(beta) union F_U(beta)=Col-beta(N_B(s)); private_C and private_U are nonempty; each contact has a full same-beta private witness. | K1–K12 exactly; original U owner=s; (t_s,m_s,n_U)=(1,2,2) or (2,2,1); X own same-beta deletion witnesses |
| SF-R-PROFILES | Both specified profiles; both S support types; all positive original r-contact splits | Both support types force t_r=1 and no retained r-spoke. Pair admits (1,3),(2,2),(3,1) before Gallai; singleton only (1,3). | K1–K12 exactly; original U owner=s; (t_s,m_s,n_U)=(1,2,2) or (2,2,1); original shield/star restrictions; singleton S04 |
| SF-SPLIT-EXCLUSION | Every arbitrary-size source in K and the two profiles | C is K4-free Gallai; r meets exactly two odd-cycle blocks, so k_L^r=k_S^r=2. Singleton S and pair r-splits (1,3)/(3,1) have no source under this contract. | K1–K12 exactly; original U owner=s; (t_s,m_s,n_U)=(1,2,2) or (2,2,1); SF-PRIVATE; SF-R-PROFILES; external connected degree-list Gallai characterization; BASE connected-exterior K4 lemma |
| SF-C-BOUND | For every proper gamma of the same remaining pair (2,2) source, including every T4 row | \|F_C(gamma)\|<=1; F_C may be empty away from beta. At beta: t_s=1 gives singleton C and complementary pair U; t_s=2 gives complementary singleton C/U. | K1–K12 exactly; original U owner=s; (t_s,m_s,n_U)=(1,2,2) or (2,2,1); SF-SPLIT-EXCLUSION structure; BASE any-row double-forbidden bridge-path lemma |
| SF-T1-MAP | Every remaining pair source; all five beta positions, two original s-spokes and three singleton C roles | Only four final necessary queries remain: beta3/spoke0 record511; beta3/spoke2 record90; beta4/spoke0 record90; beta4/spoke2 record511; C forbids1, U forbids{2,3}. They are not source realizations. | K1–K12 exactly; original U owner=s; (t_s,m_s,n_U)=(1,2,2) or (2,2,1); t_s=1; SF-C-BOUND; actual support C0234/U012 after a single common whole-source normalization; BASE arbitrary-size complete support/schema cover and all subsequent source exclusions |
| SF-T1-EXTEND | Every actual T4-accepting X in the single-spoke (2,2) BASE class | X extends the two adjacent-singleton rows to beta. This does not control the color of internal vertex r. | K1–K12 exactly; original U owner=s; (t_s,m_s,n_U)=(1,2,2) or (2,2,1); t_s=1; own beta minimality and actual complete C/U (2,2) |
| SF-T2-MAP | Every remaining pair source, all original beta rows and both forbidden-role orders | Only beta0 or beta2 are compatible: beta3/4 duplicate spoke color; beta1 transports to forbidden03. Both C/U role orders were considered before further proof. | K1–K12 exactly; original U owner=s; (t_s,m_s,n_U)=(1,2,2) or (2,2,1); t_s=2; C0234/U012; s-spokes02; named e=rb4 in the same geometry frame; BASE complete sector theorem |
| SF-T2-ROLE | Every source remaining after SF-T2-MAP | F_C(beta)={unused3}, F_U(beta)={used beta1=1}. The alternative C=1 yields an actual three-color pentagon obstruction with shared odd cycles and is excluded. | K1–K12 exactly; original U owner=s; (t_s,m_s,n_U)=(1,2,2) or (2,2,1); t_s=2; SF-SPLIT-EXCLUSION; actual induced pentagon Gamma=(s,b0,b4,b3,b2); BASE all-degree4 minimal three-color singleton structure without T4 |
| SF-T2-EXTEND | Every remaining actual t_s=2 source; both beta0/beta2 presentations | BASE gives the two adjacent-singleton X extensions; no internal r color bound follows. | K1–K12 exactly; original U owner=s; (t_s,m_s,n_U)=(1,2,2) or (2,2,1); SF-T2-ROLE; same-source nonadjacent Case II, with joint whole-source reflection when needed |
| SF-QX | Every remaining source in either specified profile | Q(X)={beta}; every gamma in the entire transported Q(G)-{beta} is accepted by X. | K1–K12 exactly; original U owner=s; (t_s,m_s,n_U)=(1,2,2) or (2,2,1); BASE X extension of both beta neighbors; X epsilon1 and own Sigma-criticality; BASE E2 QX singleton/adjacent-pair theorem |
| SF-RESTORE | Every proper gamma, all16 pins and all complete lifts of the same G/X | L_G(gamma;a,b)=L_X(gamma;a,b) when a!=gamma(b_i), otherwise empty. On Delta=Q(G)-Q(X), all X lifts have r=gamma(b_i). | K1–K12 exactly; original U owner=s; (t_s,m_s,n_U)=(1,2,2) or (2,2,1); X differs by only the named original e=rb_i |
| SF-T2-Q0-Q1-RESTORED | Every remaining t_s=2 source with beta=q0, and all its complete X lifts at gamma=q1 | All X(q1) lifts have s=3 and r!=2, so every lift restores rb4. If q1 belongs to transported Q(G), this is a limited source contradiction. | K1–K12 exactly; original U owner=s; (t_s,m_s,n_U)=(1,2,2) or (2,2,1); SF-T2-ROLE; same-source U012 identical beta/gamma attachments; L234 complete (0 1) transport fixing r2/s3; S40 identical attachments; BASE q1 X extension |
| SF-RESIDUAL | Every remaining pair(2,2) source and its entire transported 933/941 rejection set | Original G restoration was proved only for t_s2 beta0->q1. Four of the 28 raw Q/beta schedules are excluded when q1 is an original rejection; 24 remain. Exact residual is the same-source ten-row r-fibre/geometry obligation on original rb4. | K1–K12 exactly; original U owner=s; (t_s,m_s,n_U)=(1,2,2) or (2,2,1); SF-QX; SF-RESTORE; SF-T2-Q0-Q1-RESTORED (mandatory adopted correction) |
| SF-FINITE | 19 frozen prior controls; 21 original r-spoke omissions; all10 literals and16 pins | Complete unpinned C piece join, C/U joint, direct whole X lifts and exact G spoke filter agree; all ambient C r fibres and all tuple preimages saved. | fixed BASE original edge inventories; no new graphs or graph-size search |

#### T1

Domain / smallest verified contract: profile(1,2,2),pair22,βq3/q4,s-spoke b0/b2,U012/L234/S40,e=rb4; full K_LONG; coverage with1132-field overlay. Complete explicit premises: `audits/2026-10-11-n45-s-long-s-t1-rfibre/claims.json`. Current adoption: `audits/2026-10-11-n45-s-long-s-t1-rfibre-review/REPORT.md:10–36`.

| Label | Complete stated quantifier | Exact conclusion | Recorded premise / proof dependency |
| --- | --- | --- | --- |
| T1-AUTHORITY-DOMAIN | For every finite arbitrary-size original G in each of 14 schedules and both original spoke variants. | FCbeta={1},FUbeta={2,3}; QX={beta}; beta s1 raw L/S r-forbidden columns each size2 partition Col; S N-diagonal excludes1. | BASE long-contract §§1,5; sealed SF-PRIVATE, SF-SPLIT-EXCLUSION, SF-QX, SF-RESIDUAL; B-QUERY-PARTITION=12+4+10+4; B-RESIDUAL-DEPENDENCY=SF-T2-Q0-Q1-RESTORED |
| T1-PATH-STABILIZER | For every finite connected K4-free Gallai original two-contact piece and every current literal query with two truly forbidden root colours; all branch sizes unbounded. | Original odd bridge path; whole path blocks residual pair F; every colour permutation fixing all actual block external colours preserves F. | BASE single-spoke-two-two §3; BASE two-two-minor §2; BASE branch-palettes §2; pinned Gallai Lemma7/Theorem10 |
| T1-ORIGINAL-MINORS | For every actual adjacent pair of path blocks in S touching04, or U touching02, with the explicitly disjoint actual exterior root-to-frame path. | A connected disjoint original-edge K5 minor, using retained X edges and not rb4. | T1-PATH-STABILIZER; original induced-C5 and actual connected pieces |
| T1-Q4-SOURCE-MINOR | For every assigned beta=q4 source, in all seven QG schedules and both s-spokes; arbitrary size. | S r-forbidden pair is02; every original path block touches04; K5 minor contradicts original disk. | T1-PATH-STABILIZER; T1-ORIGINAL-MINORS; inherited S N-diagonal |
| T1-Q3-ACTUAL-S-EDGE | For every assigned beta=q3 source, both s-spokes, arbitrary original S/bridges/branches. | DS=23, DL=01; original S has exactly u,v with N_G(u)={r,v,b0,b4}, N_G(v)={r,u,s,b0}; original ordered contacts retained. | T1-PATH-STABILIZER; T1-ORIGINAL-MINORS; finite leaf-block argument from complete degree4 |
| T1-U012-COMPATIBLE-PREIMAGE | For every such original source, at gamma=q0 and q1, on its complete actual U. | There exists b in{1,3} with complete U preimage avoiding b, common to q0/q1; refusing both gives current-row pair13 and original K5 minor. | T1-PATH-STABILIZER; T1-ORIGINAL-MINORS; BASE degree5-tree-components §1; BASE degree5-interfaces §§2-3; q0/q1 actual U equality |
| T1-Q3-Q0-Q1-RFIBRE-RESTORE | For every assigned beta=q3 source and each gamma in{q0,q1}, both s-spokes and arbitrary L/U sizes. | There exist ordered pins(a,b), b in{1,3}, a!=2, with complete same-source X lift; full C/U preimages join and original rb4 restores. | T1-Q3-ACTUAL-S-EDGE; T1-U012-COMPATIBLE-PREIMAGE; complete degree4 strict-slack greedy; full restriction/union and exact restoration filter |
| T1-ASSIGNED-COVER | For every G satisfying K1-K12 in each of the exact 28 assigned schedule×spoke queries. | q3 queries restore a Delta row; q4 queries yield original K5 minor; all 28 assigned queries have a scoped source contradiction candidate. No extra sufficient source premise. | T1-Q4-SOURCE-MINOR; T1-Q3-Q0-Q1-RFIBRE-RESTORE; T1-AUTHORITY-DOMAIN; sealed corrected SF-RESIDUAL with restoration dependency |
| T1-FINITE-CALIBRATION | Exactly fixed finite input: 48 S stabilizer cases, 8 U cases, 8 conditional S template pins, 18 path-minor skeletons and 2 leaf skeletons; all 24 colour permutations. | Normal and seed17 read-only outputs match; two broken minor skeletons and one corrupted certificate are rejected. | calibration-input SHA256 c6bcd70dfea81194211928da0c2e6c8874c804cefa60559d55883c3c85f67a89; calibrate.py and native logs; arbitrary-size paper remains separate |

#### T2-q0

Domain / smallest verified contract: profile(2,2,1),pair22,βq0,spokes02,three assignedQG schedules; full K_LONG; SF-QX trust retained. Complete explicit premises: `audits/2026-10-11-n45-s-long-s-t2-q0-restore/claims.json`. Current adoption: `audits/2026-10-11-n45-s-long-s-t2-q0-restore-review/REPORT.md:11–31`.

| Label | Complete stated quantifier | Exact conclusion | Recorded premise / proof dependency |
| --- | --- | --- | --- |
| T2Q0-S3 | For every assigned-contract source and eta in {beta,q1,q2}, every full X(eta) lift | s=3; complete U preimage avoiding 3 is nonempty; U fibres coincide across these rows | sealed review SF-T2-ROLE; K6/K8/K9/K10 |
| T2Q0-BETA-PARTITION | For every assigned-contract source, at the original beta / s=3 pin | D_L(beta;3) disjoint-union D_S(beta;3)=Col, both size 2, and 3 not in D_S(beta;3) | BASE long-contract section 5; sealed original B REPORT section 4; T2Q0-S3 |
| T2Q0-L-Q1-TRANSPORT | For every original full L assignment and every ordered (a,b) pin | pi01 maps Lambda_L(beta;a,b) bijectively to Lambda_L(q1;pi01(a),pi01(b)); at b=3 the forbidden r column maps by pi01 | K9/K10; literal support identity 212 -> 202 |
| T2Q0-S2-FORCED | For every source satisfying all assigned premises | 2 is in D_S(beta;3), so Lambda_S(beta;2,3) is empty | T2Q0-S3; T2Q0-BETA-PARTITION; T2Q0-L-Q1-TRANSPORT |
| T2Q0-S-Q2-TRANSPORT | For every original full S assignment and every ordered (a,b) pin | pi12 maps Lambda_S(beta;a,b) bijectively to Lambda_S(q2;pi12(a),pi12(b)); beta(2,3) maps to q2(1,3) | K9/K10; literal support identity 20 -> 10 |
| T2Q0-Q2-EMPTY1 | For every assigned-contract source and every b in Col | L_X(q2;1,b) is empty; all q2 lifts have s=3 | T2Q0-S2-FORCED; T2Q0-S-Q2-TRANSPORT; T2Q0-S3; sealed review SF-JOIN |
| T2Q0-Q2-RESTORE | For every assigned-contract source, there exists a complete q2 X lift; every such lift | has r != 1 and is a complete G(q2) lift; the full q2 X and G lift sets coincide | T2Q0-Q2-EMPTY1; sealed review accepted SF-QX; sealed review SF-T2-EXTEND and inherited E2 chain; sealed review SF-RESTORE |
| T2Q0-COVER3 | For each of the three assigned schedules and every source satisfying all K1-K12 premises | there is a complete restored q2 lift, contradicting original G rejection; no source in the three schedules | T2Q0-Q2-RESTORE; K2 exact original rejection sets |
| T2Q0-CALIBRATION | For every one of the fixed three abstract column cases and two literal support transports | column arithmetic and all sixteen pin maps match proof-calibration.json; assigned coverage has ten rows x sixteen pins per schedule | control-plan.json; proof-calibration.json |

#### T2-q2

Domain / smallest verified contract: profile(2,2,1),pair22,βq2,spokes02,seven assignedQG schedules; full K_LONG;112-cell empty overlay. Complete explicit premises: `audits/2026-10-11-n45-s-long-s-t2-q2-restore/claims.json`. Current adoption: `audits/2026-10-11-n45-s-long-s-t2-q2-restore-review/REPORT.md:10–38`.

| Label | Complete stated quantifier | Exact conclusion | Recorded premise / proof dependency |
| --- | --- | --- | --- |
| CQ2-SLACK | Every finite connected original piece and lists with \|M(v)\|>=deg_T(v), strict at one vertex | The set of complete assignments is nonempty by spanning-tree child-before-parent greedy; includes shared r/s contact slack | direct proof REPORT §2 |
| CQ2-CAPACITY | Every same source, proper gamma, fixed s=b, T=L/S; all four r pins | Forbidden r set B_T has size <= original k_T^r=2; complete tuple/preimage semantics retained | CQ2-SLACK; original full degree identity; pick a complete tuple only to bound its universal forbidden intersection |
| CQ2-S-BETA | Every same source; beta=q2; r=0 and r=1 | Lambda_S(beta;0,3) and Lambda_S(beta;1,3) are nonempty full fibres; pre-s assignments and transposition(2 3) preserve every original shared coordinate | CQ2-SLACK; actual beta S40=10; unique s-contact |
| CQ2-BETA-PARTITION | Every same source; beta=q2 and fixed s=3; all r pins | B_S(3)={2,3}; B_L(3)={0,1}; complete local seed fibres L(beta;2,3) and S(beta;0,3) nonempty; these are not a beta whole-graph lift | CQ2-CAPACITY; CQ2-S-BETA; X rejection and complete same-pin restriction/union; accepted SF-T2-ROLE only for F_U(beta)={1}; review SHA256 authority |
| CQ2-U-TARGET | Every same actual U; gamma in {q3=01021,q4=01012} | All gamma U012 attachments are010; full U preimages avoiding3 exist by slack and transposition(2 3) | CQ2-SLACK; original n_U=1; actual gamma U query010 |
| CQ2-Q4-FULL | Every same source; gamma=q4; full pin fibre (r,s)=(0,3) | Full L_X(q4;0,3) and L_G(q4;0,3) nonempty, exactly full product of all transported actual piece preimages and original isolated factor; r0 != gamma(b4)=2 restores original rb4 | CQ2-BETA-PARTITION; CQ2-U-TARGET; L map(0 1 2):201->012, pins(2,3)->(0,3); S map(1 2):10->20, pins(0,3) fixed; retained actual s-spokes both0; complete same-frame union |
| CQ2-Q3-FULL | Every same source; gamma=q3; full pin fibre (r,s)=(0,3) | Full L_X(q3;0,3) and L_G(q3;0,3) nonempty, exactly full product of all transported actual piece preimages and original isolated factor; r0 != gamma(b4)=1 restores original rb4 | CQ2-BETA-PARTITION; CQ2-U-TARGET; L map(0 2):201->021, pins(2,3)->(0,3); S identity:10->10, pins(0,3) fixed; retained actual s-spokes both0; complete same-frame union |
| CQ2-COVER7 | For every assigned schedule, every original source satisfying all K1-K12 and its same-frame Q(G) | No such original source: at least one proved q3/q4 restored row belongs to Delta=Q(G)-{q2}, contradicting full G rejection; all seven covered without additional sufficient premise | CQ2-Q3-FULL; CQ2-Q4-FULL; full assigned schedules; sealed obligations.json and task dispatch; SF-RESIDUAL adopted only with SF-T2-Q0-Q1-RESTORED dependency addendum; 12+4+10+4 correction retained |
| CQ2-CALIBRATION | Only fixed 720 literal-map comparisons, six beta partitions, seven schedules and 1120 symbolic ordered pin cells | Ordinary and seed17 replay byte-identical; two bad certificates refused; native captures retained | checker.py; calibration.json; checks.json |

#### D

Domain / smallest verified contract: actual same-original-vertex/edge block decomposition and literal constraints; source conclusions additionally require K_LONG; new source exclusions0. Complete explicit premises: `audits/2026-10-11-n45-s-long-s-block-transfer/claims.json`. Current adoption: `audits/2026-10-11-n45-s-long-s-block-transfer-review/D-proof-review.md:13–19`.

| Label | Complete stated quantifier | Exact conclusion | Recorded premise / proof dependency |
| --- | --- | --- | --- |
| TF-BLOCK | every finite actual connected C with actual bridge/odd-cycle block-tree, every literal attachment assignment gamma | V-REC/K-REC restriction and union are mutually inverse on every complete proper original-C assignment | local original edge inequalities; induction on actual block incidence tree |
| TF-FIBRES | every original ordered contact list including repeated shared vertices, every ambient tuple and r colour, every ordered(a,b) | bijection restricts to all full tuple inverse images; all empty cells, r colours, diagonal pins and original branch coordinates retained | TF-BLOCK |
| TF-X | every actual X with same original C/U components, every proper gamma and all16 pins | all full X lifts biject to spoke-factor times Lambda_C(gamma;a,b) times actual Lambda_U(gamma;b) times Col^I | TF-FIBRES; restriction/union on disjoint actual components |
| TF-RESTORE | every same original pair G=X+rb4, every literal gamma and ordered(a,b) | full G lift set equals full X lift set for a!=literal gamma(b4), otherwise empty; no unused-colour substitution | original edge inequality |
| TF-COLOR | every fixed actual piece and colour permutation pi satisfying each literal attachment and root-pin constraint | full assignments and every tuple inverse image transport bijectively; return to common literal frame before component join | bijection of four colours; TF-FIBRES; TF-X |
| TF-FINITE | exactly four valid named C microcases,ten literal rows,all64 ambient cells,all16 pins and three spoke factors per row | all1344 full assignments and complete interface preimages match independent original-edge enumeration; three corrupt certificates rejected | TF-BLOCK implementation; independent stdlib direct enumerator |
| TF-DOMAIN | 24 inherited necessary schedules and every original s-spoke variant (38 variant records) | full Delta and ten rows/all16 pins preserved as symbolic source obligations; no target relation or preimage count fabricated | SF-QX; SF-RESTORE; SF-T2-Q0-Q1-RESTORED; query partition12+4+10+4; sealed remaining-schedules.json |
