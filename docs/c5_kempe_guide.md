# Kempe／重接／計數與策略導覽

更新：2026-10-02。本頁維護本線現況；證明及實際重播範圍見各報告。
研究線標記見 [HANDOFF](HANDOFF.md)，完整索引見 [STATUS](STATUS.md)，
共通信任界線見 [DOCUMENTATION](DOCUMENTATION.md)。

## 1. 目標與範圍

研究固定來源圖上的換色、完整有序關係及計數限制，尋找可證的出口機制。
必要條件、固定圖閉包與一般 disk 定理分開；本線不宣稱已證 `K∞=K≤5`。

## 2. 項目現況

| 項目 | 已知結果與未涵蓋範圍 | 報告入口 |
| --- | --- | --- |
| 933／941 的 excess／容量／跨度 | 933 已提高至 ε≥2；941 的 ε=1、t=1 已由兩個原省略核心的六跨度與 binary 原邊完整 relation 排除，現只餘 t=2、3。一般來源仍未排除，未 Lean 化 | [941 single-spoke](c5_941_single_spoke.md)、[四容量子覆蓋](c5_excess_one_subcovers.md)、[前輪下界](c5_independent_support_capacity.md) |
| Kempe screen／邊位置對座標 | screen 等價於 20 條蘊涵，1,024 masks 已核對；未新增排除，一般 adjacent-singleton lemma 未證 | [screen](c5_kempe_screen.md)、[座標](c5_edge_pair_coordinates.md) |
| 循環流與計數 | 六維／153 支撐／十二循環；36 份基底覆蓋證三套分開整數 orbit 條件不再收緊恆等式解；未排除平面來源 | [循環流](c5_circulation.md) |
| Count cone／class 計數 | near-triangulation 化約、部分 Lean 代數與 class 級紙面計數已有；cone／connectivity 缺口仍在 | [count cone](c5_count_cone_bridge.md)、[B₅ face](c5_b5_face.md)、[class 計數](c5_kempe_class_counts.md) |
| 同染色有序重接 | 一步精確公式及同圖三配對同 state／不同後繼反例；record 110 已另由原圖 K5 排除，有限可迭代 state 未證 | [有序重接](c5_dual_path_surgery.md)、[來源排除](c5_single_spoke_two_two_minor.md) |
| Connectivity／候選 state | 同圖更新與有限控制可重播；AB-only／固定 AB\|CD 猜測有反例，多候選不能任意拼成可實現 state | [connectivity](c5_kempe_connectivity.md)、[AB cube](c5_ab_swap_cube.md)、[choices](c5_edge_choices.md) |
| Cut／behavior | retained-component 重建有 Lean 支援；粗 cut 摘要有反例，有界 behavior 控制不證多步充分性 | [cut](c5_cut_interfaces.md)、[behavior](c5_behavior_refinement_results.md)、[state 導覽](c5_state_guide.md) |
| 固定圖策略與 repair | survivor-811 固定閉包、必要低谷／回升與 B₂ 準備已保存；一般 K=4 策略、共同安全 repair 機制未證 | [barriers](c5_strategy_barriers.md)、[repair](c5_repair_interface.md) |

## 3. 停止點與保留缺口

933 已證 ε≥2，941 仍為 ε≥1；沒有一般候選排除或普遍六跨度結論。
941 的 ε=1 必恰有一份原二接點 C₂，另有三份單容量因子；現只餘 t=2、3。
q₀、q₁ 的真子核心省略身份不共用，C₂ 在兩列都禁包含 D 的二色集。
q₃ 若以整圖為 minimal core，C₂ 恰禁 {D}；若有真子核心，仍禁包含 D 的二色集。
t=1、(2,1,1) 已完成來源排除：非平凡 C₂ 迫三個原末端各有三點支援，
共同跨度至少六；C₂=原邊時 F 只能空或二色，不能滿足 q₃ 的 {D}。
下一步固定 t=2、(2,1)，保留兩條具名 spokes、同一 C₂ 的原有序接點
及全部附件、一份 unary 和 q₀、q₁ 的不同省略身份；分開「都省略 spoke」
與「一列省略 unary」，檢查共同支援及完整十列，不另開大圖枚舉。
詳見 [新來源排除報告](c5_941_single_spoke.md) 及
[省略分類](c5_excess_one_subcovers.md#6-新下界及-941-的精確殘餘)。

本線另保留一般 connectivity 限制、可迭代充分 state 及共同安全 repair 的缺口；
不再把邊際配對、獨立 orbit 分解或一次 cut 重建當作一般解法。
完整有序關係須共同對齊色框，保留同一原圖的 components、接線與操作身份。
固定圖成功歷程不提供跨圖常數上界。這些其他問題未在本輪啟動新搜尋。
單側與共同出口的當前接手點見 [weak-deletion 導覽](c5_weak_deletion_guide.md)。

## 4. 閱讀與重播入口

933／941 先讀 [941 single-spoke](c5_941_single_spoke.md) 及
[本輪紀錄](history/2026-10-02-941-single-spoke.md)，省略 witnesses 見
[四容量子覆蓋](c5_excess_one_subcovers.md)，前提見
[容量下界](c5_independent_support_capacity.md)。最小重播：

```bash
python3 scripts/c5_941_single_spoke.py --check
python3 scripts/c5_excess_one_subcovers.py --check
python3 scripts/c5_independent_support_capacity.py --check
python3 scripts/c5_single_spoke_root_conservation.py --check
```

先讀 screen／座標與循環流的必要條件，再讀有序重接的一步公式和反例；
策略路線由 barriers 接到 repair interface。各報告列出 checker 與 artifact，
重播時使用原報告指定範圍，不把生成器當成只讀檢查。
循環流的當輪驗證見 [2026-09-27 紀錄](history/2026-09-27-circulation.md)。
紙面推導、Python 固定域證書與個別 Lean 代數結果分開；未形式化平面來源排除。
