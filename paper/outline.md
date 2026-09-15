# Paper outline（草稿 v0，2026-09-15）

工作標題（暫）：**Boundary-colouring states of planar patches with a five-cycle boundary:
finite-state models, sealed C5 cells, and a Lean-verified reduction chain**

來源：`docs/HANDOFF.md`（主）、各 `docs/*.md`、`Math/*.lean`、`artifacts/*`。
本文件只整理「論文可以寫什麼、每個 claim 的信任層級、對應的定理／證書在哪」；
不新增數學結果。信任標籤沿用 repo 慣例：**[L]** proved in Lean、**[C]** computationally
observed／verified、**[P]** 紙面證明未 Lean 化、**[?]** conjectured／unresolved。
複合標籤：**[L, native]** = Lean 定理但公理含 `native_decide` 計算公理；**[artifact-data]** = 陳述對象是
`artifacts/` 匯出／轉錄的資料，Lean 證的是嵌入資料、搜尋完備性另屬 [C]。逐條依據見
`artifacts/paper_audit/audit_table.md`（`python3 scripts/paper_audit.py --check`）。末尾 §14 是「遺漏檢查」——對照 repo 後發現 HANDOFF 頂端或 README 沒有帶到、寫論文時容易漏的東西。

---

## 0. 一句話定位與明確不主張

- 研究對象：平面 patch 沿有序 C5 邊界暴露的 boundary-colouring 關係 Σ（可延伸成 proper 4-colouring 的
  boundary assignments 集合），以及它在黏合、剪枝、有限狀態掃描下的行為。
- 主要貢獻（依章節）：
  1. Σ 的精確語意、S4 十-orbit 無損壓縮、黏合 = 交集，以及「壓縮不能丟 alignment」的反例 [L]。
  2. separating-C5 平面 BAD 圖（11 頂點 26 邊，Σ 恰為 T4）與其由 primitive gadgets 反向合成 [L]+[C]。
  3. triangle grammar 上的 ColorDFA／GeometryDFA：染色側完全封口（`reject_iff_hall`），幾何側
     attachment normal form ⇒ `|R| ≤ 3` [L]；topology completeness 仍開放 [?]。
  4. 逐步填色的資訊充分性：固定 window 不充分、fan 4／5 residual 類數 55／97 下界 [L]、雙側 437 類 [C]。
  5. 密封 C5 cell 目錄 $|K_0..K_5| = 11/22/52/87/112/132$ [C]，R1／SYM 的 Lean 證明與 reduced DFS
     完整性鏈（prefix partition、viable soundness、graph bridge、DFS reachability、bitmask、popcount）[L]；
     $K_6=K_7=K_5$ 條件式 [C]，$K_\infty=K_5$ [?]。
  6. 通往 $K_\infty=K_5$ 的必要條件：Kempe screen 1023→153→142 [C]、chord-total 計數恆等式 [P]、
     XOR parity word 四對一與 Dvořák–Lidický Conjecture 9 的翻譯 [L]、near-triangulation 歸約 [P]、
     B₅ face 的 gluing 限制 [C]+[P]。Adjacent-singleton lemma 明列為 **未證**。
- **不主張**：不證四色定理；不以 4CT 當搜尋 oracle（例外：§11 的 exterior-cell 相交測試明確使用 4CT
  與 disk gluing，論文要標出）；不假設 boundary-state conjecture；不把「平面圖中指定 C5」偷換成
  「C5 是 disk 外邊界」；不把有限層飽和外推成 $K_\infty=K_5$。

## 1. Introduction

1.1 動機：是否存在小的、composition-preserving 的 boundary quotient 描述 relevant planar patches；
    之後才談 transition system 的 closed SCC（HANDOFF §1）。
1.2 為什麼 C5：C5 disk patch GOOD ⇔ 補回 apex 可染，直接連到四色問題（phase1.md）。
1.3 兩個關鍵區分（貫穿全文）：
    - disk 外邊界 vs separating cycle（§4 的 BAD 圖屬後者）；
    - Σ（染色資訊）vs 幾何合法性（§5.3：同 Σ 不同 disk 合法性）。
1.4 結果總覽表（每列標 [L]/[C]/[P]/[?]）。
1.5 與文獻：RSST 1997（背景，非依賴）；Dvořák–Lidický 2019/2020 *Coloring count cones of planar graphs*
    （Conjecture 9、Corollary 20、B₅ 12 rays、Lemma 6／7／13.2）；Dvořák–Swart 2025
    *A note on extendable sets of colorings and rooted minors*（方向參考，尚未導出任何引理）；
    MIT *Some Graph Theory* §14.3（Jordan／bridge interlacement 背景）。

## 2. Trust hierarchy and verification protocol

- 三層標籤定義（HANDOFF §2 表）。
- Lean 內再分：普通證明／kernel `decide`／`native_decide`（額外信任 native compiler 與
  `..._native.native_decide.ax_1_1` 計算公理）。**論文需逐模組列表**，不能用「多數有限計算用 native_decide」
  一句帶過：新模組（C5Counts、C5ParityWord、NearTriangulation、EdgeMask、IntegerViable、ReducedDFS、
  ReducedViable、ReducedGraphBridge、PrefixPartition、SymNormalForm、LocalClosure、GeoRejectBridge 等）
  無 native；舊模組（Enumeration、Certificates、GadgetSynthesis、GeometryDFA、HallTriangle regression、
  StepwiseReplay、SymRelabel 的兩條 list 事實…）有。用 `grep -c native_decide Math/*.lean` 產表。
- 公理審計：18 份 `artifacts/**/lean-audit*.txt`（`#print axioms` 實際輸出）；全庫無 `sorry`／`admit`。
  論文級集中審計 `Math/PaperAudit.lean` → `artifacts/paper_audit/audit_table.md`：184 個 paper-referenced
  declarations，112 普通證明／10 kernel `decide`／52 `native_decide`／10 定義，27 條為 artifact-data；
  除 `native_decide` 計算公理外無非標準公理。repo-wide `native_decide` 77 處、19 檔（`native_decide_inventory.txt`）。
- Python 側協定：每個結果有 deterministic artifact ＋ `--check` 逐 byte replay；Lean 重驗 graph／boundary／
  colouring claims，不信任 Python 的 BAD 結論。
- 拓撲信任層（未 Lean 化、以標準定理解釋）：NetworkX planarity／apex test、「兩 disk 沿 C5 黏合必平面」、
  Jordan／K3,3 障礙、rotation system ⇒ disk embedding。

## 3. Preliminaries: the five-boundary relation Σ

- 定義：`Color := Fin 4`，有序 boundary injection，`SigmaAt`／`Sigma`；GOOD／BAD／T4（`Math/Boundary.lean`）[L]。
- 枚舉：240 proper C5 colourings（120 三色＋120 四色）；S4 orbits 10；S4×D5 orbits 2；十個 canonical reps
  （`Math/Enumeration.lean`）[L, native]。
- 十-bit 編碼無損且保交集；上界 1024 個 bitsets，不宣稱全可實現（`State.color_abstraction_exact`、
  `abstract_intersection`、`color_state_count`）[L, native]（經 `color_orbits_cover`；`abstract_intersection` 本身普通證明）。
- 黏合：不相交內部、共享有序 boundary ⇒ `Σ(union) = Σ1 ∩ Σ2`；relational composition、hide、結合律、
  S4-equivariance（`GadgetRelations.lean`、`LocalClosure.summary_glue`／`replacement`）[L]。
- Alignment 不可省略：`C5+02` 與 `C5+03` 的 Σ 互為 reflection，接 `C5+03+13` 後一 BAD 一 GOOD
  （`AlignmentCounterexample.lean`：`same_D5_class_different_context_answer`；`Certificates.coarse_not_congruent`、
  `glued_bad`）[L, native]。
- 純交集 transition 只會縮小、不能修 BAD、SCC 為 singleton（`State.lean`：`intersection_cannot_repair`、
  `intersection_scc_singleton`）[L]。

## 4. Finite searches and the separating-C5 counterexample

4.1 n = 5, 6：1,056 labeled C5-supergraphs，883 planar，250 BAD，全由 Lean 重驗；最小 (5,8) 含 boundary K4，
    非 disk patch（`all_certificates_bad`、`no_bad_with_fewer_edges`）[L, native, artifact-data]+[C]。
4.2 累積條件實驗表（phase1.md）：cofacial 一項即殺光全部 BAD（223 圖 0 BAD）；其後的零不是額外證據 [C]。
4.3 Induced-C5 搜尋 n = 5..9 候選數 1／32／2,047／258,096／61,450,327，無 planar BAD；**n = 10 未窮舉** [C]。
4.4 11 頂點構造：兩個 8-vertex disk patches 沿 C5 黏合，27→26 邊，Σ = T4（120）；deletion-minimal，
    非全域 minimum（`ConstructedAnalysis.minimal_sigma_exact`）[L, native, artifact-data]。
4.5 注意：`artifacts/construction/minimized.jsonl` 與 `artifacts/gadgets/bad_certificates.jsonl` 第一行是
    **兩張不同的 26 邊圖**（Σ 都是 T4，邊集不同）；論文用哪張要固定。

## 5. Gadget synthesis and geometric obstructions

5.1 Primitives：NEQ、EQ（K5−xy）、K4 frame（相對色座標）；共用 frame vs 各自隱藏 frame 的接線差異
    （`neq_exact`、`eq_exact`、`shared_frame`、`independent_frames`）[L, native]。
5.2 有限 grammar「有序 induced C5 ＋ 內部 K3 ＋ 任意 boundary-to-K3 邊」：32,768 接線 → 7,194 disk-accepted →
    42 exact Σ；單 component 無 exact T4；903 state pairs，10 對交集恰 T4；十個 target 各有
    graph certificate（五個 26 邊、五個 27 邊）（`GadgetLibrary`／`GadgetTargets`／`GadgetSynthesis.all_targets_exact`）
    [L, native, artifact-data]+[C]：Lean 證每張嵌入圖的 exact Σ／T4，42／10 的完備性是 [C]。
5.3 幾何障礙（HANDOFF §6，**未 Lean 化** [C]/[P]）：
    - 交錯端點路徑 P = 0–5–2、Q = 1–10–3 ⇒ 兩塊必分居兩側（十張 target 逐行表）。
    - P／Q／R 例：三個 disk patches Σ 全為 240，P∪R 是 disk、Q∪R 不是（apex ⇒ K3,3）——**完整 Σ 不含幾何資訊**。
    - Primitive port 障礙：K5−xy 的 x,y 不可同面；K4 frame 四 port 不可同面。

## 6. Finite-state synthesis on the triangle grammar

6.1 ColorDFA：沿邊界掃描的染色自動機，`mem_sigma_triangle`／`splitSigma_triangle` 對每個 attachment word
    是普通證明 [L]；`wordOfMask` 雙射避免 Pi-type 枚舉（工程備註）。
6.2 GeometryDFA：`rotationOf`／`checkRotation`（Euler、C5 facial）；`accept_certificate` forward soundness [L, native]
    （經 `accepted_masks_have_rotation`）；`accepted_count = 7194` [L, native]，與 NetworkX apex test 一致 [C]；
    **completeness 未證** [?]。
6.3 Colour semantics closed：`k3_uncolorable_iff`（mathlib Hall）→ `reject_iff_hall`：
    `¬Accept ↔ PairPinnedToFourth ∨ TripleRestrictedToTwo` [L]（普通證明＋kernel `decide`；`regression_guard` 為 native）。
6.4 Winding ⇒ block：`runOK_iff_blocks`、`attachment_block`（`AttachmentBlock.lean`，無枚舉）[L]。
6.5 Hall witness 去色：`GeoReject`、`reject_iff_geometry`、`threeProfile_eq_geo` [L]。
6.6 Attachment budget：fan excess ≤ winding、總 attachment ≤ 8、共同鄰居 ≤ 2 [L]。
6.7 Cut-necklace normal form：`annulusAccept_iff_normalForm` 雙向；六種 incidence regimes
    `(E,X,Z) ∈ {(1,4,0),(2,2,1),(2,3,0),(3,0,2),(3,1,1),(3,2,0)}`；飽和／含空位／一二 junction 的環序
    （`AttachmentSignature`／`Saturated`／`Gaps`／`Order`）[L]。
6.8 Bridge：`runOK_rejection_le_three`、`|R|=3` ⇒ degree 型 (2,3,3) 且 R 為 cyclic 3-interval；
    profile ≥ 2、等號相鄰對（`GeoRejectBridge.lean`）[L]。
6.9 Z5 現象：三色 acceptance 32 種實現 21 種、size 2 只有相鄰對、十組 T4 pairs 恰為互補 profile
    （`z5_profiles_checked`）[L, native]，但只是此 grammar 內的檢查，不是 disk patch 的 lemma；其 Z5 解釋為 [C]。
6.10 Topology completeness：`AttachmentEndpoints.lean` 證端點環序 → normal form → AnnulusAccept [L]；
     embedding → 端點環序（Jordan／vertex-star splitting／spanning-arc cutting）只有紙面（topology_completeness.md）[P]/[?]。

## 7. Generic boundary relations, fan pentagon, pp-expressions

7.1 Fan pentagon grammar（內部五邊形 + 13、14）：$2^{25}$ 完整 replay，174,456 disk-accepted，87 exact Σ
    （含原 42）；三色 profiles 仍 21 種；`mask=1116616/Σbits=767` 恰拒絕 01231 的全域換色
    （`sigma_exact` [L, native, artifact-data]；`two_colour_obstruction` 普通證明 [L]）+[C]。
7.2 完整 boundary relation 為主狀態：`BoundaryRelations.lean` 泛型 full relation／condition／projection／
    nonvacuous forcing [L]；`C5PairForcing.lean`：R767 與全體 proper C5 的所有 pair projections 相同、
    conditional forcing 不同（`pairwise_information_insufficient`）[L, native]（四條 C5PairForcing 有限事實全 native）。
7.3 Python catalog：87 完整 states、750 條最小條件規則、211,410 pair 查詢、3,828 aligned meet [C]。
7.4 pp-expression 層（`PPRelations.lean` 的 denotation 與 meet／hide 語意法則 [L]；106 公式 replay [C]）。
7.5 討論表示法（state_language.md：Interface/State/Branch/Choice；七個動詞）——規格，非引擎。

## 8. Stepwise colouring: information sufficiency and strip automata

8.1 問題陳述（stepwise_state_sufficiency.md 第一部分）：Q1 存在可成功後繼／Q2 安全剪枝；充分性判準
    「同狀態、可被 continuation 區分 ⇒ 不充分」；$S_n=(a_{n-1},a_n,a_{n+1},q_n)$；顏色參照命名規則
    （首次遇色依序 b,c,d；$b^\pm$ 是 occurrence 參照，不是 bit）。
8.2 七次試跑摘要表（HANDOFF 表＋試跑七）：C5 場上 Σ 壓縮全被否定；strip 上固定 window 不充分、
    埋深 d 時類數成長（fan 3：2,5,9,14；fan 4：3,8,22,63）；對齊參照自動機穩態 3/4/12/13/28/41 [C]。
    注意撤回：「任何固定容量都不夠」的舊結論已撤回，改為「一般深度 |Q| 無界」[?]。
8.3 Lean：`StepwiseState.lean` 泛型換色／register／pumping 區分定理 [L]；`StripGraph.lean` 的
    `search_iff`／`verdict_iff` 已驗證著色檢查器；`fan4_nerode_lower_bound`（55）、`fan5_nerode_lower_bound`（97）、
    `fan5_extendable_iff`（21,845 字）[L, native, artifact-data]（表格由 `export_stepwise.py` 匯出）。
8.4 fan 4 完整 signature（55 類、8 signatures）、fan 5（97 類 = E1+S4+P12+U12+U24+A36+F6+T1+dead1）、
    fan 5 雙側 437 類（425 無限語言，僅 24 種已命名）[C]。
8.5 Committed-colour 分層 strip（§9j）：活類 ⇔ constraint map；$(3)^n$ trap horizon 到 n−2；
    trap 結構（§9k）：forced cone 精確 certificate、$P_h$ 剛性 pattern、recovery map R 不回 $W_\forall$ [C]。
8.6 未動的待釐清：是否允許 Kempe 換色；S 是否判合法性。

## 9. Local closure and fixed-endpoint wiring

- `summary_glue`、任意 context 的 `replacement`、`relation_count = 2^{4^k}`、degree-2 path 色中性、hub 缺色條件 [L]。
- R1（放 §10 也可）：密封私有頂點 deg ≤ 3 ⇒ `summary_eq_deletePrivate`／`sigma_eq_delete_private` [L]。
- `LocalWiring.lean`：fixed-endpoint pairwise-conflict grammar 的 forbidden-set 摘要封閉、等價 iff 摘要相等 [L]。
- 固定 3/4/5/6 端點非交叉路徑 grammar：活 residual 1/3/11/45 類；C4 wheel 84→60；P+T 同側、Q+T 有 K5 subdivision 障礙 [C]。

## 10. Sealed C5 cells: catalogue and the reduced-search completeness chain

10.1 Cell 規格：$(k,M)$、$U(k)$ = 5 chords + 5k attachments + C(k,2) interior 邊；bit j 的精確語義；
     S4 進 key、D5 不進（c5_cell_enumerator.md §0）。
10.2 精確枚舉 $k \le 5$（$2^{40}$）：$|K_0..K_5| = 11/22/52/87/112/132$，24 個 D5 orbits；原 42 與 87 個 Σ 全在 $K_5$；
     separating C5 的 meet 涵蓋 1,023 個非空 mask [C]。
10.3 Σ bridge：production 十 bit ≡ 規格，$k\le3$ 全宇宙、$k=4$ DFS 節點 20,904,415、132 witness、極端與隨機 case，零 mismatch [C]。
10.4 R1 [L]；SYM：`Sigma_relabel`（Σ 與標號無關）＋ `exists_sorted_relabel`（任意 k 的非遞增代表）[L]；
     checker A1–A5'（$k\le3$ 全宇宙；**k = 4, 5 orbit 檢查未跑**）[C]。
10.5 R2（長度 ≤ 5 分隔環 + 較小 disk 實現）：診斷用，非 $K_6=K_5$ 前提 [C]。
10.6 $K_6 = K_7 = K_5 = 132$ **條件式**：前提表（R1 [L]、SYM 2a/2b [L]、程式正確實作 [C, 僅 $k\le5$ 驗證]）；
     新增序列 11,11,30,35,25,20,0,0；$K_\infty=K_5$ [?]。
10.7 Reduced DFS 完整性鏈（全部普通證明、無 native）[L]：
     - `PrefixPartition`：`unique_owner`／`covered_iff`／`owner_at_end`；
     - `ReducedViable`：`viable_of_survivor`／`rejection_sound`／`retained_owner`；
     - `ReducedGraphBridge`：`degree_eq_graph`／`attValue_eq_attMask`／`survivor_iff`；
     - `ReducedDFS`：`state_invariant`／`prefix_reachable`／`worker_reachable`／`split_graph_complete`；
     - `EdgeMask`：encode 單射、AND／prefix／shift 對應、`reach_iff`；decode 需 n < 2^E（反例 decode 3 8）；
     - `IntegerViable`：`popcount_encode`、`viable_encode_iff`、`viable_reach_iff`。
     對應 checkers：prefix（k=3：645 tasks、205 圖）、viable（133,181 prefixes 零誤剪）、graph bridge（66,592 圖）、
     bitmask（2,047 masks／257-bit）[C]。
10.8 觀察：`viable=True` 不是精確可完成性（k=2 有 3,264 個無完成圖的前綴）[C]。
10.9 **鏈上仍缺**：Python 執行語義（bit 操作、建表、early-break）、完整 graph／apex 表示、染色表 AND 語義、
     planarity oracle、scheduler 恰執行一次。論文要以「Lean 形式化的是有限集合上的控制模型，不是程式 refinement」陳述。

## 11. Towards $K_\infty = K_5$: necessary conditions and the adjacent-singleton gap

11.1 Kempe screen：1,023 非空 masks → 153（平面 Kempe 必要條件，與內點數無關）→ 142（與全部已知 exterior cells
     非空相交，**使用 4CT 與 disk gluing**）⊇ 132；差額恰兩個 D5 orbits（T4+singleton、T4+independent 2-set）[C]。
     boundary push 1,530／1,420 轉移封閉 ⇒ 重複 push 無新排除力 [C]。
11.2 **Adjacent-singleton lemma（UNPROVED）**：disk cell G，$T_4\subseteq\Sigma(G)$ ⇒ $E(C_5[P(G)])\neq\varnothing$。
     條件式推導 $K_\infty\subseteq K_5$ 的路線（需：此引理＋拓撲 bridge＋有限分類認證）[?]。
     可用簡化：T4 全收 ⇒ boundary 無 chord [P]。
11.3 計數恆等式 [P]：五條 chord 的 $x_{uv}+y_u+y_v$ 相同（inclusion–exclusion + noncrossing partition，
     42 partitions 有限部分已檢）；132 witness 全符合；11 個 independent supports 的抽象向量同時滿足恆等式與
     Kempe split 分解 ⇒ 兩類必要條件仍不足 [C]。
11.4 Lean 化的代數層 [L]：`C5Counts`（`ofCoefficients_chordTotalConst`、`conjecture9_iff`：$\Sigma x\le3\Sigma y \iff m\le0$、
     `all_chords_positive`、`counterexample_violates_conjecture9`）；`C5ParityWord`（`fiber_card` 240 = 4·60、
     `extensionCount_of_edgeWord`、`IsParityWord`、`fiber_partition`）；`NearTriangulation`（`ear_or_hub`、
     `two_periodic_of_no_ear`、Euler `counts`、`corollary20_range`：$2k+4<30\iff k\le12$）。
11.5 文獻翻譯：Dvořák–Lidický Conjecture 9 ≡ $m\le0$（較強猜想，不可當已證）；Corollary 20（電腦輔助，
     未重播）排除 $k\le12$ 的 near-triangulation 反例 [P]。
11.6 反例歸約 [P]：保留一個四色 fiber ⇒ 任何同邊界 supergraph 仍反例；移枝塊 + ears/hub 補完 ⇒
     near-triangulation（允許平行邊）；polygon 長度 3..9 的 1,231 orbits 補完驗證 [C]。
11.7 B₅ face [C]+[P]：12 rays 轉錄，$R_{5,12}=t$、$F_0=R_{5,9}$、$F_2=R_{5,7}$；requested faces = cone(t,F₀)、
     cone(t,F₀,F₂)；12×12 pairing 與 10 個 D5 alignments；planar context $Q=R_{5,3}$ 給 $6c>0$ 非矛盾；
     只有 wheel ray 與 t 正交且與每 fan pairing 6 ⇒ 單次 pairing closure 排除不了 c > 0。Fan-trap corollary 只給可達
     family，非 invariant set。12-ray 完備性引用 Lemma 6 未重算。
11.8 未 Lean 化的拓撲層（列表）：inclusion–exclusion 從 disk graph 出 $a_0,a_e$；block decomposition Σ(B)=Σ(G)；
     face 結構／平行邊／`fill_polygon` 終止；dual graph 與 near-cubic 類對應。

## 12. Open problems（集中列出，論文結尾）

1. Adjacent-singleton lemma；同圖不同完整染色間的 Kempe connectivity 相容性。
2. Near-triangulation 中排除 $P\subseteq e$ 且 $x_e>0$（只需這個 support 分支）。
3. 超出單次 pairing 的圖變換／bridge 引理以證 face 上 c = 0。
4. Triangle grammar 的 topology completeness（embedding ⇒ 端點環序）；一般 disk 的 geometry signature 充分性。
5. $K_\infty=K_5$；$k\ge8$ 的不可約圖直接生成（R2 單調子情況）。
6. Stepwise：一般深度 $|Q(d)|$ 成長律；fan 5 雙側 401 種未命名語言；fan 6 未開始；Kempe 換色版本。
7. reduced-search 鏈：Python refinement、planarity oracle、scheduler。
8. 記錄但未啟動：C6／C7 經額外內點轉接成 C5 interface（c5_interface_idea.md）；活動面 introduce/close/forget；
   週期／博弈控制（local_closure.md §8）。

## 13. Reproducibility appendix

- 工具鏈：Lean/mathlib `v4.34.0-rc2`（`lean-toolchain`、`lake-manifest.json`；不自動 `lake update`）；
  Python `uv run --with networkx==3.5 --with rustworkx==0.17.1`。
- 一鍵驗證清單（從 HANDOFF 各停止點的 bash 區塊彙整）：`lake build`；各 `*Audit.lean`；
  `check_search／check_construction／check_gadgets／check_automata／check_stepwise --fast／check_pp_relations／
  check_fan_pentagon／check_c5_relation_library`；`local_closure --check`、`state_views --check`；
  c5 系列 `c5_sigma_bridge --quick`、`c5_sym_check --quick`、`c5_prefix_check／c5_viable_check／c5_graph_bridge_check／
  c5_bitmask_check／c5_kempe_screen／c5_adjacent_singleton_counts／c5_count_cone_bridge／c5_b5_face --check`。
- 執行時間備註：$k=5$ 精確 17 min／30 workers；$k=7$ reduced 36 min；GeometryDFA native 3–4 min；
  `regression_guard` 2.5 min；`check_stepwise` 全量 9 min。
- Artifact 索引：`artifacts/{boundary,construction,gadgets,automata,fan_pentagon,boundary_relations,pp_relations,
  stepwise,local_closure,state_views,sym_relabel,c5_cells,induced}`；`cells.json` sha256 記在各 report 內。
- 附錄表：Lean 模組 → 章節；定理名索引（本文件 §3–§11 已列）。

---

## 14. 遺漏檢查（對照 repo 後的清單）

以下是寫論文前該補、或 HANDOFF 頂端／README 沒帶到的項目。分「內容遺漏」「一致性」「工程／文件」三類。

### 14.1 內容上容易漏掉、但 repo 已有的結果

| # | 項目 | 在哪 | 建議 |
| --- | --- | --- | --- |
| 1 | `AlignmentCounterexample.lean`（reflection 在 D5 中、同 D5 類不同 context 答案） | HANDOFF §3 文字有，§8 檔案導航表**沒有** | 進 §3；加到檔案表 |
| 2 | phase1 累積條件實驗表（cofacial 即殺光 BAD；其後的零非證據） | 只在 `phase1.md` | 進 §4.2，它是「為何轉向 gadget 合成」的動機 |
| 3 | `State.lean` 的 `intersection_cannot_repair`／`intersection_scc_singleton` | HANDOFF §7.2 一句 | 進 §3，是「純交集 transition 不夠」的形式化理由 |
| 4 | `LocalWiring.lean`（forbidden-set 摘要封閉、交錯 chord grammar 實例） | 只在 local closure 段落 | 進 §9；檔案表沒列 |
| 5 | `ConstructedOriginal`／`ConstructedMinimal` 與 gadget 26 邊圖是兩張不同圖 | HANDOFF §5 末段警告 | §4.5 固定論文用哪張，附兩者邊集 |
| 6 | `C5PairForcing.pairwise_information_insufficient`（pair projections 相同、conditional forcing 不同） | boundary_relations.md | 進 §7.2；這是「完整 relation 為主狀態」的定理依據 |
| 7 | `AttachmentEndpoints.lean` 與 topology_completeness.md 的紙面論證（annulus、slot 分離、端點環序引理） | 標為歷史 | §6.10 要明列「已證的編譯接口」與「未證的 embedding 抽取」 |
| 8 | fan 5 雙側 437 類中 401 種無限語言未命名；左右 ID 語意（`reversed_word_class`）約定 | HANDOFF 歷史段 | §8.4 與 §12 open problems |
| 9 | stepwise 的撤回紀錄：「任何固定容量都不夠」已撤回；試跑六 nearest-occurrence 只否定具體版本 | §9d | 論文只能寫修正後敘述，不能引舊表 |
| 10 | `viable=True` 非精確 oracle（k=2 有 3,264 反例前綴） | §11.3 | 進 §10.8；防止讀者把 viable 當可完成性 |
| 11 | k=4,5 的 SYM orbit 檢查沒跑（$2^{31}$／$2^{40}$）；舊 `sym_check.json` 的 A3 語意錯誤只保留為歷史 | §7.3／停止點 | §10.4 明寫；論文不引舊 A3 數字 |
| 12 | Kempe screen 第二步（→142）**用了 4CT 與 disk gluing** | c5_kempe_screen.md §3 | 與 §0「不以 4CT 當 oracle」並列說明：這是必要條件篩選，不是搜尋剪枝 |
| 13 | 抽象計數向量 $N_P=t+\sum_{i\in P}f_i$ 通過恆等式＋Kempe split＋exterior screen ⇒ 這兩類必要條件不足 | adjacent_singleton_counts.md §3.2 | 進 §11.3，是「為何要新的結構引理」的證據 |
| 14 | Fan-trap corollary 的平行邊適用性需補論證；12-ray 完備性依文獻 Lemma 6 | c5_b5_face.md §5 | §11.7 逐條標 [P] 與引用 |
| 15 | `c5_interface_idea.md`（C6/C7 轉接 C5；十-orbit 容量 vs 關係集合編碼；五點投影漏六點 obstruction 的診斷例） | HANDOFF §1 一句 | §12 記為未啟動想法 |
| 16 | 工程 lemma：`wordOfMask_bijective`、`acceptB_iff`、`rotationTable` 物化 | HANDOFF §9 | 可放 reproducibility 附錄，解釋為何 native 檢查可行 |

### 14.2 一致性／敘述需對齊

- **$K_6=K_5$ 的信任層級**：HANDOFF 不同時期措辭不一（「條件式」vs 直接寫等號）。論文統一按
  `c5_cell_enumerator.md §6.0` 前提表：R1 [L]、SYM 2a/2b [L]、實作 [C 僅 $k\le5$]。
- **「多數有限計算用 native_decide」**（HANDOFF §2）已不準確；paper-referenced 184 條中 52 條 native，§2 用 audit 表。
- **§7.2「未開始」五項**（topology certificate 資料、embedding 模型、P/Q/R 形式化、composition congruence 測試、
  closure/SCC）至今仍未開始；論文 open problems 要如實列。
- **兩種 count 語意**：文獻 dual 計數 vs 本 repo 固定 assignment 計數（不乘 4），`extensionCount_of_edgeWord` 已處理；
  論文引用 Conjecture 9 時要寫清翻譯。
- **D5 orbit 數**：132 Σ = 24 個 D5 orbits；phase1 的「2 個 S4×D5 reps」是 colouring 類不是 state 數——兩處不要混。
- Dvořák–Swart 目前只是方向參考；不能在論文寫成已用到其結果。

### 14.3 工程／文件層面

- `README.md` 檔案表只列 ~8 個模組，且仍留 GitHub Pages 模板段落；論文投稿前應同步 §8 檔案導航或指向 HANDOFF。
- `CITATION.cff` abstract 停在 automata 階段（未提 C5 cell、reduced chain、count-cone 工作），version 0.1.0；
  論文引用前更新。
- 公理審計覆蓋：已由 `Math/PaperAudit.lean` 集中處理（含 `State`、`SplitCertificate`、`AlignmentCounterexample`、
  `BoundaryRelations`、`LocalWiring`、`AttachmentEndpoints`）；outline 新增 Lean 名稱時同步加進去。
- 既有 build warnings（`AttachmentOrder`、`SymRelabel` linter）— 投稿前清掉或在附錄註明。
- 論文用的數字（如 7,194、42、87、132、133,181、20,904,415、1,231、437）應由 `--check` artifacts 直接引，
  並在附錄列 artifact 路徑與 sha256，而不是手抄 HANDOFF。
- 圖表候選：11 頂點 BAD 圖與兩側三色模式；P/Q/R 例；六種 incidence regime 環序；fan 5 signature 表；
  $K_k$ 增長序列；Kempe screen 漏斗 1023→153→142→132；B₅ 12 rays 與 pairing 矩陣。
