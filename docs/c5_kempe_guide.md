# Kempe／重接／計數與策略導覽

更新：2026-10-03。本頁維護本線現況；證明及實際重播範圍見各報告。
研究線標記見 [HANDOFF](HANDOFF.md)，完整索引見 [STATUS](STATUS.md)，
共通信任界線見 [DOCUMENTATION](DOCUMENTATION.md)。

## 1. 目標與範圍

研究固定來源圖上的換色、完整有序關係及計數限制，尋找可證的出口機制。
必要條件、固定圖閉包與一般 disk 定理分開；本線不宣稱已證 `K∞=K≤5`。

## 2. 項目現況

| 項目 | 已知結果與未涵蓋範圍 | 報告入口 |
| --- | --- | --- |
| 933／941 的 excess／容量／跨度 | 兩候選均已證 ε≥2。唯一 degree-6 root 的 t=0、1、2、3 全部分拆均已作整型來源排除，T4 迫 t≤3，完成此 ε=2 分支。t=0 的 (6) 用飽和兩 K₄，(4,2) 用原 binary 路徑的同源框弧 K₅；若 ε=2，只剩兩個 degree-5 roots。任意大小紙面＋Python、未 Lean 化，一般來源保留 | [t=0 全分拆總報告](c5_excess_two_no_spoke_complete.md)、[t=3 全分拆總報告](c5_excess_two_three_spoke_complete.md)、[t=2 全分拆總報告](c5_excess_two_two_spoke_complete.md)、[t=1 全分拆總報告](c5_excess_two_single_spoke_complete.md)、[941 ε≥2](c5_941_three_spoke.md) |
| 雙 root 的 ε=2 收窄 | 相鄰 mixed 刪 roots／zw 全收；相鄰唯一 mixed 的 ε=2 分支已全排 (4,4) 核心，原 leaf joint 色纖維與同一 unary 雙列 palette／K₅ 全排五-spoke 原來源，該分支的兩候選總 spokes 都≤4。原單 spoke 省略若拒絕，省略圖自己是唯一 degree-5 minimal q-core；單省略及 (5,5) 原核心仍保留。紙面＋Python，ε≥3 未證，未 Lean 化 | [原 leaf 色纖維與五-spoke 排除](c5_excess_two_mixed_core_leaf_fibers.md)、[單 spoke 原附件化約](c5_excess_two_mixed_core_single_spoke.md)、[省略原 mixed 全收](c5_excess_two_mixed_omission.md) |
| Kempe screen／邊位置對座標 | screen 等價於 20 條蘊涵，1,024 masks 已核對；未新增排除，一般 adjacent-singleton lemma 未證 | [screen](c5_kempe_screen.md)、[座標](c5_edge_pair_coordinates.md) |
| 循環流與計數 | 六維／153 支撐／十二循環；36 份基底覆蓋證三套分開整數 orbit 條件不再收緊恆等式解；未排除平面來源 | [循環流](c5_circulation.md) |
| Count cone／class 計數 | near-triangulation 化約、部分 Lean 代數與 class 級紙面計數已有；cone／connectivity 缺口仍在 | [count cone](c5_count_cone_bridge.md)、[B₅ face](c5_b5_face.md)、[class 計數](c5_kempe_class_counts.md) |
| 同染色有序重接 | 一步精確公式及同圖三配對同 state／不同後繼反例；record 110 已另由原圖 K5 排除，有限可迭代 state 未證 | [有序重接](c5_dual_path_surgery.md)、[來源排除](c5_single_spoke_two_two_minor.md) |
| Connectivity／候選 state | 同圖更新與有限控制可重播；AB-only／固定 AB\|CD 猜測有反例，多候選不能任意拼成可實現 state | [connectivity](c5_kempe_connectivity.md)、[AB cube](c5_ab_swap_cube.md)、[choices](c5_edge_choices.md) |
| Cut／behavior | retained-component 重建有 Lean 支援；粗 cut 摘要有反例，有界 behavior 控制不證多步充分性 | [cut](c5_cut_interfaces.md)、[behavior](c5_behavior_refinement_results.md)、[state 導覽](c5_state_guide.md) |
| 固定圖策略與 repair | survivor-811 固定閉包、必要低谷／回升與 B₂ 準備已保存；一般 K=4 策略、共同安全 repair 機制未證 | [barriers](c5_strategy_barriers.md)、[repair](c5_repair_interface.md) |

## 3. 停止點與保留缺口

本線候選來源前提是固定完整 Σ=933／941 或整圖 D₅ 像、每條非框邊
Σ-critical、指定有序 induced-C₅ disk、所有有效內點完整 degree≥4。
原分量、有序 contacts、實際 attachments／supports、ownership、嵌入
環序及同一字面四色框始終保持。任意大小化約由紙面與明列外部依賴
承擔；Python 檢查固定必要域、完整 tuples／fibres 及具名 minors。

**共同 ε≥2；唯一 degree-6 的 ε=2 分支已全排。** 941 的 ε=1
全部分支及唯一 degree-6 的 t=0、1、2、3 全分拆見 §2 原報告。
因此 ε=2 只剩兩個完整 degree-5 roots。

| 雙 root 分支 | 最新已完成範圍 | 精確報告 |
| --- | --- | --- |
| 原 root 刪除 | 至少一個刪 root 圖全收，另一個至多缺一列；相鄰且有 mixed 時兩者均全收 | [完整 Σ 與原刪除](c5_excess_two_root_deletions.md) |
| 相鄰 mixed 的原 zw 省略 | 雙 triangle、原樹／偶數路徑與單 triangle 接回全排；Σ(G−zw)=Ω | [雙 triangle](c5_excess_two_root_deletions.md)、[原路徑](c5_excess_two_path_edge.md)、[單 triangle](c5_excess_two_triangle_edge.md) |
| 相鄰唯一 mixed 的 (4,4) q-core | 保留 mixed 的雙 spoke、spoke＋unary、雙 unary 身份及只省略 incidence-(1,1) mixed 的身份均全排 | [原身份表](c5_excess_two_mixed_core_spokes.md)、[spoke＋unary](c5_excess_two_mixed_core_spoke_unary.md)、[雙 unary](c5_excess_two_mixed_core_two_unary.md)、[mixed 省略](c5_excess_two_mixed_omission.md) |
| 相鄰唯一 mixed 的單 spoke 省略 | 省略圖若拒絕 q，自己就是唯一 degree-5 minimal q-core；同色原 spoke 身份限制三-spoke 附件 | [單 spoke 原附件化約](c5_excess_two_mixed_core_single_spoke.md) |
| 相鄰唯一 mixed 的五-spoke 原來源 | 八份具名附件共同搬運至 998／1004；原 (b,a,y,u) joint leaf 纖維、同一 unary 雙列 palette 與原圖 K₅ 全排；兩候選總 spokes 都≤4 | [原 leaf 色纖維](c5_excess_two_mixed_core_leaf_fibers.md) |

**下一窄入口：四-spoke 的 (3,1) 及 root 交換。** 先固定原 mixed
incidence-(1,1) 與一-spoke 側兩份原單接點 unary；省略三-spoke
側的同色原 spoke 後得到 t=1、(2,1,1) core。保留原 leaf、原 C
及兩 unary 的完整 joint relations、全部實際附件與同一色框，
分析接回那一條原 spoke。停止於可證窄排除或具名必要殘留。

這是選定的 (3,1) 子型；同型的一-spoke 側原 incidence 預算還容許
mixed-(1,1) 加一 binary、mixed-(1,2) 加一 unary、mixed-(1,3) 且
無 unary。這些僅是原 incidence 必要分拆，仍保留且未證 disk 實現。

其他四-spoke 型、較少 spokes、原 unary 單省略，以及原 G 自己是
(5,5) q-core 的分支仍保留；不能套唯一 degree-5 分離定理。
相鄰多 mixed 在刪 zw 全收後的原來源、no-mixed、非相鄰雙 roots
與 unary 側例外亦保留。**單 spoke 省略尚未整型排除，ε≥3 未證。**
指定列出口不提升為完整候選排除，不重開來源圖枚舉。

本線另保留一般 connectivity、可迭代充分 state 及共同安全 repair
的缺口。固定圖成功歷程不提供跨圖常數上界；一般單側／共同出口
與 K∞=K≤5 未證，接手點見 [weak-deletion 導覽](c5_weak_deletion_guide.md)。

## 4. 閱讀與重播入口

本批九輪的完成範圍、整理發現、實際重播與貼用摘要見
[雙 root 進展整理與提交紀錄](history/2026-10-03-excess-two-dual-root-progress-commit.md)。
最新先讀 [原 leaf 色纖維](c5_excess_two_mixed_core_leaf_fibers.md)，
再讀 [單 spoke 原附件化約](c5_excess_two_mixed_core_single_spoke.md)
與 [省略原 mixed](c5_excess_two_mixed_omission.md)；前置核心身份及
刪 root／zw 化約由 §3 報告表往回追。各輪詳細驗證保留在報告所連研究紀錄。

本批九份 checker 的固定證書重播：

```bash
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_root_deletions.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_path_edge.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_triangle_edge.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_spokes.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_spoke_unary.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_two_unary.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_omission.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_single_spoke.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_leaf_fibers.py --check
```

前序唯一 degree-6 分支依序讀 [t=0](c5_excess_two_no_spoke_complete.md)、
[t=3](c5_excess_two_three_spoke_complete.md)、
[t=2](c5_excess_two_two_spoke_complete.md)、
[t=1](c5_excess_two_single_spoke_complete.md) 的全分拆總報告，
再追各報告所連原省略證書、[短支援引理](c5_short_support_singleton.md)、
原首橋及末端區塊。共同下界見 [941 ε≥2](c5_941_three_spoke.md)，
minimality 前提見 [容量下界](c5_independent_support_capacity.md)。
前序實際發布範圍見 [唯一 degree-6](history/2026-10-03-excess-two-degree-six-publish.md)、
[t=2](history/2026-10-03-excess-two-two-spoke-publish.md)、
[t=1](history/2026-10-03-excess-progress-publish.md) 的紀錄；沿用證據不等於本輪重跑。

其他路線先讀 screen／座標與循環流的必要條件，再讀有序重接的一步
公式和反例；策略由 barriers 接到 repair interface。各報告列出
checker 與 artifact，使用原報告指定範圍，生成器會寫檔。
循環流驗證見 [2026-09-27 紀錄](history/2026-09-27-circulation.md)。
紙面推導、Python 固定域證書與個別 Lean 代數結果分開；未形式化平面來源排除。
