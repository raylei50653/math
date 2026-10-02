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
| 933／941 的 excess／容量／跨度 | 兩候選均已證 ε≥2；唯一 degree-6 root 的雙 spoke、t=2 spoke＋unary 及 t=3 原 triangle 位置分支已排除。t=3 以完整接合與共享省略限制關閉兩色存活留下的 1,254 個比較，原 unary 任意大小保持。紙面＋Python、未 Lean 化；path／tail 位置、其餘 ε=2 及一般來源保留 | [t=3 triangle 排除](c5_excess_two_three_spoke_unary.md)、[t=2 排除](c5_excess_two_spoke_unary.md)、[雙 spoke 排除](c5_excess_two_double_spoke.md)、[941 ε≥2](c5_941_three_spoke.md) |
| Kempe screen／邊位置對座標 | screen 等價於 20 條蘊涵，1,024 masks 已核對；未新增排除，一般 adjacent-singleton lemma 未證 | [screen](c5_kempe_screen.md)、[座標](c5_edge_pair_coordinates.md) |
| 循環流與計數 | 六維／153 支撐／十二循環；36 份基底覆蓋證三套分開整數 orbit 條件不再收緊恆等式解；未排除平面來源 | [循環流](c5_circulation.md) |
| Count cone／class 計數 | near-triangulation 化約、部分 Lean 代數與 class 級紙面計數已有；cone／connectivity 缺口仍在 | [count cone](c5_count_cone_bridge.md)、[B₅ face](c5_b5_face.md)、[class 計數](c5_kempe_class_counts.md) |
| 同染色有序重接 | 一步精確公式及同圖三配對同 state／不同後繼反例；record 110 已另由原圖 K5 排除，有限可迭代 state 未證 | [有序重接](c5_dual_path_surgery.md)、[來源排除](c5_single_spoke_two_two_minor.md) |
| Connectivity／候選 state | 同圖更新與有限控制可重播；AB-only／固定 AB\|CD 猜測有反例，多候選不能任意拼成可實現 state | [connectivity](c5_kempe_connectivity.md)、[AB cube](c5_ab_swap_cube.md)、[choices](c5_edge_choices.md) |
| Cut／behavior | retained-component 重建有 Lean 支援；粗 cut 摘要有反例，有界 behavior 控制不證多步充分性 | [cut](c5_cut_interfaces.md)、[behavior](c5_behavior_refinement_results.md)、[state 導覽](c5_state_guide.md) |
| 固定圖策略與 repair | survivor-811 固定閉包、必要低谷／回升與 B₂ 準備已保存；一般 K=4 策略、共同安全 repair 機制未證 | [barriers](c5_strategy_barriers.md)、[repair](c5_repair_interface.md) |

## 3. 停止點與保留缺口

933、941 的固定完整 Σ、edge-minimal C₅ disk 來源均已證 ε≥2；
沒有一般候選排除、ε=2 實現或普遍六跨度結論。
941 的 ε=1 各型已全排除：t=1 用共同三葉支援，t=2 用保留原四接點的
spoke 接回，最後 t=3 用原 triangle degree-2 位置及 (r,x,y) 完整關係。
前輪 118 個必要核心／398 個原 root 位置的 1,194 次接回皆無 941。
無枝 triangle 的 36 份 T4 全收支援未篩 disk；其放寬域可有其他三拒絕型，
所以不宣稱全部接回至多兩拒絕。詳見 [three-spoke 報告](c5_941_three_spoke.md)。

ε=2、唯一 degree-6 root 的**雙 spoke 省略核心條件分支已排除**：
刪去兩條原 spokes 若仍拒絕 singleton 列，全 degree-4 分類迫原 t=3、
內部 degree=3；原四接點化約後，148 個 marked cores 的 888 次雙接回
全無 933／941。432 個 T4 全收模型至多拒絕兩個相鄰 singleton 列。
因此候選來源刪去任意兩條不同原 spokes 必接受全部十列。
詳見 [新報告](c5_excess_two_double_spoke.md)；沒有提高共同 ε≥2 下界。

**t=2 的 spoke＋原 unary 省略核心分支亦已排除**：148 個原四接點
核心的 592 次 spoke 接回，對 933／941 各五像的 5,920 次比較全部排除。
原 unary 在全部十列均有非空 endpoint relation；凡核心接回後 root
有至少兩色，就能保留完整 tuple 並接上同一原 unary。五接點公式保留
原 v、附件與 ownership；不需枚舉 unary 或收緊其支援。
詳見 [spoke＋unary 報告](c5_excess_two_spoke_unary.md)。因此在唯一
degree-6、t=2 等候選前提下，省略任一原 unary 及任一原 spoke 必全收 Ω。
必要區間仍含三拒絕 mask，沒有「所有接回至多兩拒絕」的推論。

**t=3 的原 triangle 位置亦已排除**：118 bases／398 marked roots 的
1,194 次接回，對兩候選五像的 11,940 個比較全排除。兩色存活仍留
1,254 個；1,200 個迫同一 G−C₂ 拒絕兩列，違反全 degree-4 單缺失，
其餘 54 個迫具名雙 spoke 省略仍拒絕，違反前述結論。
原 (r,x,y,v) 完整接合、V 的任意大小及全部附件保持，詳見
[t=3 triangle 報告](c5_excess_two_three_spoke_unary.md)。

**下一個窄問題：同一 ε=2、唯一 degree-6 root、t=3 的 spoke＋unary
省略分支，改限 r 位於剩餘全 degree-4 核心的 path／tail。**
此時 r 的兩個原內部鄰點 x、y 分屬兩份 unary U₁、U₂，原 G−r 則有
U₁、U₂、V 三份。先保留這三個原分量、三條 spokes 及所有省略身份，
檢查全 degree-4 省略圖的跨列單缺失限制是否足夠；若需縮路徑，必須
另證原 (r,x,y,v) 關係保持，不能套用本輪 triangle 398 位置涵蓋。
省略兩份 unary／一份 binary、沒有全 degree-4 真子核心的情形，以及
兩個 degree-5 roots（含 mixed）亦均保留。

本線另保留一般 connectivity 限制、可迭代充分 state 及共同安全 repair 的缺口；
不再把邊際配對、獨立 orbit 分解或一次 cut 重建當作一般解法。
完整有序關係須共同對齊色框，保留同一原圖的 components、接線與操作身份。
固定圖成功歷程不提供跨圖常數上界。這些其他問題未在本輪啟動新搜尋。
單側與共同出口的當前接手點見 [weak-deletion 導覽](c5_weak_deletion_guide.md)。

## 4. 閱讀與重播入口

整批成果的發布範圍與本次實際重播見
[進展整理與發布紀錄](history/2026-10-02-excess-progress-publish.md)。

933／941 先讀 [t=3 triangle spoke＋unary 排除](c5_excess_two_three_spoke_unary.md)
及[本輪紀錄](history/2026-10-02-excess-two-three-spoke-unary.md)，前序見
[t=2 spoke＋unary 排除](c5_excess_two_spoke_unary.md)、
[雙 spoke 排除](c5_excess_two_double_spoke.md)，共同下界見
[941 three-spoke／ε≥2](c5_941_three_spoke.md)，省略 witnesses 見
[四容量子覆蓋](c5_excess_one_subcovers.md)，前提見
[容量下界](c5_independent_support_capacity.md)。最小重播：

```bash
python3 scripts/c5_excess_two_three_spoke_unary.py --check
python3 scripts/c5_excess_two_spoke_unary.py --check
python3 scripts/c5_excess_two_double_spoke.py --check
python3 scripts/c5_941_three_spoke.py --check
python3 scripts/c5_941_two_spoke.py --check
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
