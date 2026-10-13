# Weak-deletion／單側與共同出口導覽

更新：2026-10-09（現況與來源入口整理；不新增研究結論）。
研究線標記見 [HANDOFF](HANDOFF.md)，全文件索引見 [STATUS](STATUS.md)，
共通信任界線與工作約定見 [DOCUMENTATION](DOCUMENTATION.md)。

本批成果及D至D₅稽核的發布驗證見[發布紀錄](history/2026-10-04-c5-parallel-progress-publish.md)；
新checkout的凍結快照／完整輸出先依[封存還原說明](../audits/README.md)還原。

共鄰端點 P₃ 已由 C-W／D₆ 在 C §1 前提下完成來源排除；
[固定目錄 cw-v1](c5_open_leaf_ledger.md)已無開放 keys。
該子題的權威論證入口及本線仍未解義務見 [§3](#3-精確停止點與下一個窄問題)。
固定目錄不代表全主線葉總數；全主線葉數與每日下降率仍未知。

## 1. 目標與範圍

跨線接續（2026-10-08）：[Phase B 分析](c5_phase_b_common_lemmas.md)統一
W-A／C-W的有原見證盾弧接口與條件容量；保留q-minimal／Σ-critical差別。
存在性分離到指定source染色的repair仍需操作／fibre匹配，未新增一般出口證明。

主命題 **`K∞=K≤5` 仍未證**。目前仍走 weak-deletion 候選 A 的
minimal obstruction 路線：先完成 single-sided exit 的可處理核心，再處理
一般／共同出口。唯一 degree-5 全部核心、唯一 mixed singleton、唯一 mixed K2
及 no-mixed 全部分拆均已由指定雙列分離或來源排除接回條件式出口；
一般出口仍未證。No-mixed 的統整與共同 source 結構見下列總覽。

## 2. 項目現況與閱讀順序

以下完成狀態均限於原報告前提；必要表不代表 disk 可實現性。

| 項目 | 現況／剩餘範圍 | 證據入口 |
| --- | --- | --- |
| Weak successors／候選 A、B、C | 固定域 audit 與同頂點 completion 已有；一般候選仍未證 | [候選](c5_weak_candidates.md)、[completion](c5_completion_weak_bisimulation.md) |
| Minimal obstruction 與出口 | 條件式接合已完成；一般單側與共同出口未證 | [三出口](c5_weak_critical_cores.md)、[單側出口](c5_single_sided_exit.md) |
| 全 degree-4 | 指定 disk／T4 前提下只缺 q；紙面＋外部定理＋證書 | [degree-4 導覽](c5_degree4_guide.md) |
| 唯一 degree-5 | 全部核心的指定雙列分離接回條件式出口；不是完整來源分類 | [單側出口](c5_single_sided_exit.md)、[R 系列的獨立缺口](c5_degree5_guide.md) |
| 相鄰雙 root／唯一 mixed singleton | 全部支援完成並接回出口 | [34／40 收尾](c5_adjacent_degree5_singleton_end_arc.md) |
| 相鄰雙 root／唯一 mixed K2 | 全部九組接線完成；區分雙列分離與來源排除 | [四 incidence 收尾](c5_adjacent_degree5_mixed_edge_k4.md) |
| No-mixed 全十五類 | 八類來源排除、七類雙列分離，原 3,548 接合全部覆蓋 | [十五類總覽與證據總表](c5_no_mixed_span_budget.md) |
| No-mixed 通用 source 結構 | m+s+a≤5；至少一條 root-spoke、無 source 重疊、至多一份飽和二禁色分量 | [側跨度紙面推導](c5_no_mixed_span_budget.md#2-從原圖導出框弧成本) |
| No-mixed 跨列分離 | 2,082 份必要支援的 4,164 target 全接受；既有局部篩選保留較強上界；後續已給免查表存在性證明 | [局部規則與覆蓋](c5_no_mixed_local_screen.md) |
| No-mixed 搬運與精確介面 | 紙面證成每 root 至多一份不可搬運分量，雙不可搬運只可能 AA/AB/AC；全部候選介面無損，守恆不升 pair 由後續免表證成，逐染色 repair 未構造 | [逐 root 界及獨立重播](c5_no_mixed_hypothesis_audit.md#31-逐-root-不可搬運界) |
| No-mixed 統一局部篩選 | 2,240 增長候選排除 2,208，32 份不影響 R；增長排除的免表完備性由後續三弧位置證成 | [增長、端點與全路徑交換](c5_no_mixed_local_screen.md) |
| No-mixed 無增長共同分離 | 短側弧與未見兩色交換不變性，免查表地排除同 singleton；7,848 joins 回歸通過 | [無增長紙面證明](c5_no_mixed_no_growth.md) |
| No-mixed 增長完備性／共同分離 | 三個側弧位置直接指定框弧，排除所有影響 R 的增長；指定 p₁、p₂ 存在性分離已免查表證成 | [增長完備性](c5_no_mixed_growth_completion.md) |
| 較大 mixed 容量／最小接點型 | 任意大小逐欄容量、unary 無重疊及缺額至多一，收成十八側型；各一 incidence 至多兩禁對；唯一 mixed 三點形完成必要接線控制，其餘幾何未完成 | [容量與三點介面](c5_mixed_capacity_contacts.md) |
| 唯一 mixed P₃ 對稱分支 | 兩端各一 incidence、兩側 E 同 pair 時，原五環空內側與五份實際支援排除全部 disk 來源；任意 unary 大小、不需 T4／Gallai | [原五環與完整側支援](c5_mixed_p3_symmetric.md) |
| 唯一 mixed P₃ 非對稱／兩端接線完成 | (1,2) 及 root 交換型由六跨度排除，容許一色側零跨度；結合對稱分支完成兩端各一 incidence 全 residual；其他接線保留 | [原環序的六跨度](c5_mixed_p3_asymmetric.md) |
| 唯一 mixed P₃ 中點／端點接線 | 原未接 root 末端的三色附件與四區塊環序排除全部 residual；連同兩端接線，兩個不同接點、各一 incidence 已全來源排除 | [保留末端的六跨度](c5_mixed_p3_middle_endpoint.md) |
| 唯一 mixed 共鄰端點 P₃ | C §1 前提下整個來源分支已排除，unary 大小不限、不需 T4；一般出口仍 OPEN，舊必要表保留 | [權威論證與 D₆ 補證](c5_qcore_shield_budget.md)、[前層原身份](c5_mixed_p3_common_endpoint.md) |
| 共鄰 P₃ 的 C₂／C₃／C₄ 前序 | 當輪各關閉一個原 key；整支後續由上列 C-W／D₆ 涵蓋，原 key 證據保留，未 Lean 化 | [C₂](c5_mixed_p3_one_color_ternary_unary.md)、[C₃](c5_mixed_p3_two_frame_ternary_unary.md)、[C₄](c5_mixed_p3_two_frame_two_unary.md) |
| 更一般 roots／出口 | degree≥6、多 degree-5、非樹／非相鄰 roots 與共同出口仍開放 | [Root 預算](c5_root_degree_excess.md)、[一般出口界線](c5_single_sided_exit.md) |

先讀候選與 minimal obstruction，再讀條件式出口的適用範圍，最後接到本線停止點。

## 3. 精確停止點與下一個窄問題

**已完成：** no-mixed 的指定 p₁、p₂ 已有免表共同存在性分離；唯一 mixed
原 P₃ 的不同接點各一 root incidence，以及 C §1 的共鄰端點分支，均已完成
任意 unary 大小的 disk 來源排除。這些結果未完成一般／共同出口，未 Lean 化。

### 共鄰端點 P₃：權威來源入口

本子題判定原 P₃ 只在端點同接兩 roots 的來源是否可能。
權威論證入口為 [C-W 報告](c5_qcore_shield_budget.md)：[§1](c5_qcore_shield_budget.md#1-原定義依賴與證據層)
給定義／信任層，§4–5 給正 unary 側的紙面排除，
[§8](c5_qcore_shield_budget.md#8-稽核後更正與補證2026-10-04d₆-之後)
導向 [D₆ 獨立稽核](../audits/2026-10-04-task-d6/REPORT.md)的零-unary 補證。
互補論證保留原路徑，由這一入口閱讀，毋須先找整份 STATUS。

完整前提沿用 [C §1](c5_mixed_p3_common_endpoint.md#1-原-source-前提與完整三點關係)：
有限簡單 induced-C₅ disk q-core，q=01012；兩相鄰 degree-5 roots z,w；
唯一 mixed 是原鏈 x₀x₁x₂，僅 x₂ 同接 z,w，框附件數為 (3,2,1)；
其餘完整 degree 四、原 unary 大小不限，不需 T4。同一原圖的接點、附件、
ownership、bridges、環序與共同色框始終保留。
正 unary 側的原三份 one-sided pieces 需六條互斥框邊，零-unary 側由補證涵蓋；
不能只憑固定目錄歸零推論整型完成。紙面＋外部 Gallai／minor 與固定 key
Python 證書各有責任，未新增 Lean 定理。

C₂／C₃／C₄ 的三個原 key、36／140／900 前層必要表與 rotation 控制都是
歷史證據；cw-v1 已合併 W batch，geometry35／join20 不再是當前待辦。
詳見 [ledger 的後續關係](c5_open_leaf_ledger.md)及 [§4 證據入口](#4-重播入口與驗證範圍)。

### 剩餘義務與下一個窄問題

更多 incidences、更大／多 mixed、逐染色 repair、非相鄰或更多 roots、
degree≥6、一般／共同出口與 `K∞=K≤5` 仍 OPEN。固定 q 的排除不能提升為
固定完整 Σ 來源分類，存在性分離不能提升為指定 source 染色的操作式 repair。

下一窄問題是檢查其餘保留分支能否提供三份**不同原 one-sided pieces**的
同源盾弧見證，入口為 [W-A](c5_qcore_shield_budget.md#33-定理-w-aunary-長盾弧及共同五邊預算)
與 [Phase B 的 B-S0](c5_phase_b_common_lemmas.md#21-b-s0有原見證的共同盾弧排除準則)。
先核 q-critical 原接點邊、每份 unary 避開自身的外路與各 piece 自身支援；
roots 不連通的分隔型，或找不到所需外路時，保存具名配置並停止推廣。
不帶 criticality／degree 前提的廣義六邊說法已有反例（D₆ §2.7）。
不重啟十五類枚舉或已關閉的 geometry keys。

### 可重用證明工具與界線

| 工具／機制 | 可安全使用的結論 | 主要入口 |
| --- | --- | --- |
| 完整關係搬運＋容量上界 | actual support 上存在共同色置換時精確搬運；否則只保留包含真實 F 的完整上界 | [t₂/t₁ 支援表](c5_adjacent_degree5_no_mixed_t2_t1.md) §4 |
| Root 色相容搬運／局部 preimages | H⊆G⊆E；全部可搬運時 G=E，必保留同一 target 色框 | [搬運引理](c5_no_mixed_hypothesis_audit.md#2-完整搬運的充分條件以及較弱版本) |
| 單框點精確化約 | 固定外部完整關係後至多兩份未知原分量；不刪外部幾何路徑 | [單框點介面](c5_no_mixed_hypothesis_audit.md#3-單框點化約與精確共同介面) |
| 逐 root 不可搬運界與 D_p 介面 | 各 root 至多一份未知 target 關係，雙不可搬運只可能 AA/AB/AC；不是固定一份 source 染色後的單分量 repair | [紙面界與精確搬運](c5_no_mixed_hypothesis_audit.md#31-逐-root-不可搬運界) |
| 禁色增長的共同局部篩選 | 守恆 palettes／非守恆原端點規則加 R 不相交條件；後續三弧位置補齊影響 R 的免表完備性 | [統一規則及界線](c5_no_mixed_local_screen.md#3-同一局部規則的兩個分支) |
| 無增長共同分離 | 短側弧 singleton 限為中間色或第四色；對側兩個未見色的交換不變性排除同 singleton | [短側引理與定理](c5_no_mixed_no_growth.md#4-三色-c5-的唯一單現點與無增長定理) |
| 增長完備性與共同分離 | 三弧位置固定配方排除有害增長，與無增長定理合成指定 p₁、p₂ 的存在性分離 | [位置引理及合成](c5_no_mixed_growth_completion.md#4-剩下的-pair-必不影響-r並完成共同分離) |
| Root degree 超額預算 | source q 的 no-mixed minimal core 有 D+O+κ=degree−4；不是 target 等式 | [Root 預算](c5_root_degree_excess.md) §1–3 |
| Mixed 容量與接點化約 | source unary 無重疊、D≤1；各一 incidence 至多兩禁對；三點控制不外推任意大小接線 | [Mixed 容量](c5_mixed_capacity_contacts.md) §2–6 |
| 完整 root 側支援不變性 | 原 E 為 pair 時，全部 unary／spokes 的實際支援聯集至少見兩色；P₃ 對稱分支五跨度排除，不替換原分量介面 | [P₃ 紙面排除](c5_mixed_p3_symmetric.md) §3–4 |
| 一色／兩色側支援共同計費 | 一色側可零跨度；原環序中三個必要已見色與 P₃ 支援共需六框邊，排除兩端接線的非對稱 residual | [非對稱六跨度](c5_mixed_p3_asymmetric.md) §3–4 |
| 原末端保留的四區塊與兩弧計費 | 中點／端點接線的未接 root 末端迫見三色；完整禁對與側支援給六框邊下界，不改換原 P₃ 介面 | [中點／端點排除](c5_mixed_p3_middle_endpoint.md) §2–4 |
| 共鄰原 P₃ 的雙扇區／tether | 原鏈與 (3,2,1) 附件限制側支援；完整分支排除依 C-W／D₆，原 36 案例只作歷史必要表 | [原短子弧](c5_mixed_p3_common_endpoint.md)、[後續權威入口](c5_qcore_shield_budget.md) |
| 單框點三接點 unary／原外路 | 最小內度二、原接點葉數與 connected exterior K₄ 排除迫原 triangle，原 z–B 路給 K₅ subdivision；固定 C₂ 身份 | [一色支援](c5_mixed_p3_one_color_ternary_unary.md) §2–5 |
| 雙框點三接點 unary／新非接點葉 | 禁色 slack 排接點碰同色框點，原 block palette 分接點／雙框點非接點葉；後者由原外路 K₅ 排除，才可用葉接點預算；固定 C₃ 身份 | [雙框點葉](c5_mixed_p3_two_frame_ternary_unary.md) §2–6 |
| 雙 root source 側跨度 | m+s+a≤5，八類來源排除；不能將成本未超額視為來源存在 | [十五類總覽](c5_no_mixed_span_budget.md) §2 |
| 樹上 edge-minimal list obstruction | root 樹有 κ=0，lists 由 incident 邊色完整描述；不能把 source 邊色直接傳到 p | [Root 預算](c5_root_degree_excess.md) §4–5 |
| actual support／annulus 次序 | 保留原分量與具名接點後得到任意大小必要覆蓋；必要表不等於 disk 實現 | [t₂/t₁ 支援表](c5_adjacent_degree5_no_mixed_t2_t1.md) §2–3 |
| 原外部路徑＋固定框弧 minor | 可排除來源或使用 target 拒絕假設排除某候選；兩者必分開記錄 | [t₂/t₁ bridge](c5_adjacent_degree5_no_mixed_t2_t1_bridge.md) |
| 端點／bridge palette 相容性 | source/target 不全域守恆時，仍可利用同一原路徑端點 tightness 與完整 relation | [t₂/t₁ endpoints](c5_adjacent_degree5_no_mixed_t2_t1_endpoints.md) |
| 整份拒絕證書 palette 交換 | 幾何排除其他選擇後，可在同一原 C 上重建額外 source 禁色 | [t₂/t₂ path palettes](c5_adjacent_degree5_no_mixed_t2_path_palettes.md) |

目前已證的高階 source 結構是 [Root 預算](c5_root_degree_excess.md)：
D+O+κ=degree−4，以及樹骨架 κ=0。**尚未證**的是：
超出本文 no-mixed 圖類的「交換或幾何阻斷」完備性，以及任意 degree-5 root 樹的跨列分離。
相鄰雙 degree-5 的 no-mixed 分拆已全部由雙列分離或來源排除涵蓋。

已關閉的主線家族：唯一 degree-5 全部分支、唯一 mixed singleton 全支援、
唯一 mixed K2 全接線，以及 no-mixed 十五類。原輪的分類、支援、具名
見證與當輪未決保持歷史語境，現況及數字統一由[新總覽](c5_no_mixed_span_budget.md)
連回各完成報告。一般化缺口不因有限表覆蓋完成而消失。

證據層保持分開：紙面證明、外部 degree-list 定理、Python 固定域控制、
Lean 普通證明與 Lean `native_decide` 不互相代替。必要支援／minor skeleton
不是來源實現證書；固定 q 結論也不自動提升成完整 Σ。

## 4. 重播入口與驗證範圍

當前共鄰端點 P₃ 證據由 [C-W §6](c5_qcore_shield_budget.md#6-checkerartifact實際重播)
與 §8 連向 checker、逐 key verdict 及 D₆；ledger 的完整重播見
[帳目報告](c5_open_leaf_ledger.md)。新 checkout 先依頁首封存說明還原大檔。

```bash
python3 scripts/c5_qcore_shield_screen.py --check
python3 scripts/c5_open_leaf_ledger.py --check
```

前者核對固定目錄及盾弧證書，後者核對既有帳目，不代替任意大小紙面證明。
本輪只整理文件，沒有重跑上述研究 checker 或 Lean build。
一般及 seed17 的實際重播、封存與歷史 hash 界線見 [W 發布紀錄](history/2026-10-04-c5-parallel-progress-publish.md)。

| 需要的下層證據 | 來源／當輪驗證入口 |
| --- | --- |
| 共鄰 P₃ 原身份、完整 triples、36／140／900 控制 | [C 報告](c5_mixed_p3_common_endpoint.md)、[當輪紀錄](history/2026-10-04-mixed-p3-common-endpoint.md)、[D₃](../audits/2026-10-04-task-d3/REPORT.md) |
| C₂／C₃／C₄ 的原三個 key | [C₂](c5_mixed_p3_one_color_ternary_unary.md)、[C₃](c5_mixed_p3_two_frame_ternary_unary.md)、[C₄](c5_mixed_p3_two_frame_two_unary.md)、[D₄](../audits/2026-10-04-task-d4/REPORT.md)、[D₅](../audits/2026-10-04-task-d5/REPORT.md)；[C₂ 紀錄](history/2026-10-04-mixed-p3-one-color-ternary-unary.md)、[C₄ 紀錄](history/2026-10-04-mixed-p3-two-frame-two-unary.md) |
| P₃ 不同接點：中點／端點與兩端非對稱 | [中點／端點報告](c5_mixed_p3_middle_endpoint.md)、[非對稱報告](c5_mixed_p3_asymmetric.md)、[中點／端點紀錄](history/2026-09-30-mixed-p3-middle-endpoint.md)、[非對稱紀錄](history/2026-09-30-mixed-p3-asymmetric.md) |
| No-mixed 共同分離、搬運與十五類覆蓋 | [增長完備性](c5_no_mixed_growth_completion.md)、[無增長](c5_no_mixed_no_growth.md)、[增長紀錄](history/2026-09-29-no-mixed-growth-completion.md)、[跨度紀錄](history/2026-09-29-no-mixed-span-budget.md)、[舊 hash 差異](history/2026-09-29-adjacent-no-mixed-t2-t0-pairs.md) |
| 雙拒絕分類與 Lean 具名工具 | [分類報告](c5_two_rejection_proof_zh.md)、[Lean 工具](lean_two_rejection_tools.md) |

當輪未解、驗證與發布事實由各原報告／歷史紀錄保留，不在導覽逐輪同步。
必要支援／minor skeleton 不代表來源實現；固定 q 不自動提升為完整 Σ。
發布狀態以即時 Git 為準；生成器可能覆寫 artifacts，重建指令不等於只讀 checker。
早期交接見 [HANDOFF_HISTORY](HANDOFF_HISTORY.md) 與 [2026-09-22 快照](HANDOFF_2026-09-22.md)。
