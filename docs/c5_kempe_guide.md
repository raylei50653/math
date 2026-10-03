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
| 933／941 的 excess／容量／跨度 | 兩候選均已證 ε≥2。唯一 degree-6 root 的 t=1 七分拆及 t=2 五分拆均已作整型來源排除；t=2 復用原短支援、共同 active forest、singleton profiles 與首橋局部 residual。同前提下 t∉{1,2}；任意大小紙面＋Python、未 Lean 化，其餘 ε=2 與一般來源保留 | [t=2 全分拆總報告](c5_excess_two_two_spoke_complete.md)、[t=1 全分拆總報告](c5_excess_two_single_spoke_complete.md)、[短支援引理](c5_short_support_singleton.md)、[t=3 binary 省略](c5_excess_two_binary_omission.md)、[941 ε≥2](c5_941_three_spoke.md) |
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

**t=3 的 path／tail 分支亦已排除，且得到較強的三原 unary 排除**：
十種原 spokes、八種 D 身份、兩候選各五像共 800 個必要比較；省略身份
共享與 D 守恆仍留 225 cases，同一原支援的正跨度／D 跨度及三 spokes
共同扇區限制全數排除。核對 33,750 份完整四接點接合；沒有圖枚舉或
路徑替換。詳見 [三 unary 報告](c5_excess_two_three_unary.md)。因此唯一
degree-6、t=3 候選省略任一原 unary 及任一原 spoke 都必全收 Ω。

**t=3、(2,1) 的原 binary 省略分支亦已排除**：同一原 V 的 D 身份、
原 C₂／V 在三 spokes 扇區內的共同支援弧，配合上述兩種具名省略全收，
排除 250 份包絡配置下的 2,030 個候選比較。只看整個扇區仍留 30 份，
共同支援弧的不重疊是必要新增資訊。983,025 次完整四接點接合控制通過。
詳見 [binary 省略報告](c5_excess_two_binary_omission.md)。因此該型所有容量二
省略均全收，若來源存在，每個 minimal rejected-row core 都須有 degree≥5。
這沒有排除整份 (2,1) 或提高共同 ε≥2 下界。

**t=2、(2,2) 的原 binary 省略分支亦已排除**：398 個具名原 root
位置的 3,980 個候選比較先剩 90 個；原核心的明確 apex K₃,₃ 排除
54 個，其餘 36 個迫第二份原 binary 省略核心。24 個沒有符合原 spokes
的第二核心，最後 12 個的 2,376 次同框五接點接合全不符目標。
詳見 [雙 binary 報告](c5_excess_two_two_binary.md)。兩份 binary 省略均全收，
該型已無全 degree-4 真子核心；後續原首橋報告再排除整份 (2,2)，
前序省略證書保留，未提高 ε≥2。

**t=2、(2,1,1) 的兩份原 unary 省略分支亦已排除**：沿用 398 個
原 triangle 位置的 3,980 比較；841 個比較有空必要列、1,945 個迫同一
binary 省略圖拒絕至少兩列，其餘 1,194 個在原核心拒絕列已不符目標。
24,975 次完整五接點接合控制通過。不需 D 身份守恆或新增支援幾何，
詳見 [兩 unary 報告](c5_excess_two_two_unary.md)。連同前序，該型全部
unit-pair 省略全收；當輪留下的原 binary 身份已由下述後續涵蓋。

**t=2、(2,1,1) 的原 binary 省略分支亦已排除**：省略核心迫兩份原
unary 恰有一份 D carrier。全部 unit-pair 全收及 D 守恆仍留 560 個
代數 cases；三份原分量的共同支援弧給 65,100 次比較，全有空必要列。
46,800 次完整五接點接合控制通過，詳見
[binary＋兩 unary 型報告](c5_excess_two_binary_two_unary.md)。因此該型
所有容量二省略均全收，已無全 degree-4 真子核心；後續短支援引理
再以三分量六跨度排除整型，詳見 [t=1 合成報告的共同推論](c5_excess_two_single_spoke_complete.md#4-結論證據層與停止點)。
共同下界仍 ε≥2。

**t=2、(1,1,1,1) 四原 unary 整型已排除**：完整 Σ edge-minimality
使每份原支援至少跨一段；D 身份另需一段。同一嵌入五段預算迫唯一
D 分量，其固定支援恰為三個連續框點，所有拒絕 singleton 位置都須
落在其中。933 的四位置及 941 的非連續三位置均不可能。
50 次目標／弧比較、810,000 次完整五接點控制通過，詳見
[四原 unary 報告](c5_excess_two_four_unary.md)。共同下界仍 ε≥2。

**t=1 的全部七分拆已作整型來源排除。** 原分量若支援包含於一條
框邊，其任一禁色都由兩／三外部 hubs 的 Gallai K₅ 排除；同源
Σ-minimality 及完整支援因此迫每份原分量至少兩段跨度。三份以上
原分量均超出五段預算，完成 (3,1,1)、(2,2,1)、(2,1,1,1) 及五 unary。
單分量 (5) 的共同五葉 active tree 只有兩形狀，原 tethers 均給 K₅。
最後 (3,2) 保留原 binary 路徑塊及 ternary 的 D 身份，(4,1) 則保留
四個原接點、共同 active forest 及兩份固定末端區塊，分別關閉全部
100 個同源必要查詢。詳見 [全分拆總報告](c5_excess_two_single_spoke_complete.md)
及 [本輪紀錄](history/2026-10-03-excess-two-single-spoke-complete.md)。
既有原 binary／兩 unary 省略證書仍保留，現在整型已由後續排除。

**t=2 的全部五分拆亦已作整型來源排除。** (2,1,1)／四 unary 由
原短支援跨度下界直接排除。(3,1) 復用 t=1 singleton profiles，16 份
具名扇區位置、107,296 十列 profile 對全無目標。(4) 的 200 份查詢，
一半違反四接點三禁色 K₅，另一半保留同一原四葉 active forest 的
兩末端袋，其非空共同支援族不能在原 spoke 扇區並排。(2,2) 的
40 份具名位置／400 查詢，用原 pair 路徑仍留下 20 份抽象資料；
補入同一原首橋兩端的共用 β、singleton 列的局部 residual 及跨列
完整搬運後全排。詳見 [t=2 合成報告](c5_excess_two_two_spoke_complete.md)
及 [本輪紀錄](history/2026-10-03-excess-two-two-spoke-complete.md)；
整理與發布重播見 [發布紀錄](history/2026-10-03-excess-two-two-spoke-publish.md)。

**停止點：同一來源前提下 t∉{1,2}；下一窄問題為 t=3、(2,1)
整型來源。** 原 binary 省略已全收，但不能以此代替整型反證。
先保留兩原分量、原有序 contacts、三條 spokes 的共同扇區、真實
支援端點及同一色框，檢查 t=2 的首橋／局部 residual 工具是否適用。
停止於可證整型排除或具名必要殘留，不重開來源圖枚舉。其餘 t、
兩個 degree-5 roots（含 mixed）及一般來源仍保留；共同下界維持
ε≥2。先前 t=1 批成果見 [進展整理與發布紀錄](history/2026-10-03-excess-progress-publish.md)。

本線另保留一般 connectivity 限制、可迭代充分 state 及共同安全 repair 的缺口；
不再把邊際配對、獨立 orbit 分解或一次 cut 重建當作一般解法。
完整有序關係須共同對齊色框，保留同一原圖的 components、接線與操作身份。
固定圖成功歷程不提供跨圖常數上界。這些其他問題未在本輪啟動新搜尋。
單側與共同出口的當前接手點見 [weak-deletion 導覽](c5_weak_deletion_guide.md)。

## 4. 閱讀與重播入口

本批成果的發布範圍與實際重播見
[2026-10-03 發布紀錄](history/2026-10-03-excess-progress-publish.md)；
共同下界及前三個省略分支的前輪發布見
[2026-10-02 發布紀錄](history/2026-10-02-excess-progress-publish.md)。

933／941 先讀 [t=2 全分拆總報告](c5_excess_two_two_spoke_complete.md)及
[本輪紀錄](history/2026-10-03-excess-two-two-spoke-complete.md)，再讀
[兩 binary／首橋](c5_excess_two_two_spoke_binary.md)、
[四接點／末端袋](c5_excess_two_two_spoke_four.md)及
[ternary／unary profiles](c5_excess_two_two_spoke_ternary.md)。前序復用入口是
[t=1 全分拆總報告](c5_excess_two_single_spoke_complete.md)及
[本輪研究紀錄](history/2026-10-03-excess-two-single-spoke-complete.md)，再讀
[短支援引理](c5_short_support_singleton.md)、[四接點＋unary](c5_excess_two_four_one.md)、
[ternary／binary](c5_excess_two_ternary_binary.md)及 [五接點](c5_excess_two_five_contact.md)。
原省略證書及前序入口：[t=1 binary 省略](c5_excess_two_single_spoke_binary.md)及
[本輪研究紀錄](history/2026-10-03-excess-two-single-spoke-binary.md)，再讀 [t=1 兩 unary 省略](c5_excess_two_single_spoke_two_unary.md)及
[本輪研究紀錄](history/2026-10-03-excess-two-single-spoke-two-unary.md)，再讀 [四原 unary 排除](c5_excess_two_four_unary.md)及
[本輪研究紀錄](history/2026-10-03-excess-two-four-unary.md)，再讀 [t=2 binary＋兩 unary 型](c5_excess_two_binary_two_unary.md)及
[本輪研究紀錄](history/2026-10-03-excess-two-binary-two-unary.md)，再讀 [t=2 兩 unary 省略排除](c5_excess_two_two_unary.md)及
[本輪研究紀錄](history/2026-10-03-excess-two-two-unary.md)，再讀 [t=2 雙 binary 省略排除](c5_excess_two_two_binary.md)及
[本輪研究紀錄](history/2026-10-02-excess-two-two-binary.md)，再讀 [binary 省略排除](c5_excess_two_binary_omission.md)及
[本輪研究紀錄](history/2026-10-02-excess-two-binary-omission.md)，再讀 [三原 unary 共同扇區排除](c5_excess_two_three_unary.md)及
[三 unary 研究紀錄](history/2026-10-02-excess-two-three-unary.md)，再讀 [t=3 triangle spoke＋unary 排除](c5_excess_two_three_spoke_unary.md)
及[triangle 研究紀錄](history/2026-10-02-excess-two-three-spoke-unary.md)，前序見
[t=2 spoke＋unary 排除](c5_excess_two_spoke_unary.md)、
[雙 spoke 排除](c5_excess_two_double_spoke.md)，共同下界見
[941 three-spoke／ε≥2](c5_941_three_spoke.md)，省略 witnesses 見
[四容量子覆蓋](c5_excess_one_subcovers.md)，前提見
[容量下界](c5_independent_support_capacity.md)。最小重播：

```bash
python3 scripts/c5_excess_two_two_spoke_binary.py --check
python3 scripts/c5_excess_two_two_spoke_four.py --check
python3 scripts/c5_excess_two_two_spoke_ternary.py --check
python3 scripts/c5_single_spoke_first_bridge.py --check
python3 scripts/c5_single_spoke_residual_locality.py --check
python3 scripts/c5_short_support_singleton.py --check
python3 scripts/c5_excess_two_five_contact.py --check
python3 scripts/c5_excess_two_four_one.py --check
python3 scripts/c5_excess_two_ternary_binary.py --check
python3 scripts/c5_excess_two_ternary_two_unary.py --check
python3 scripts/c5_excess_two_binary_three_unary.py --check
python3 scripts/c5_excess_two_five_unary.py --check
python3 scripts/c5_excess_two_single_spoke_binary.py --check
python3 scripts/c5_excess_two_single_spoke_two_unary.py --check
python3 scripts/c5_excess_two_four_unary.py --check
python3 scripts/c5_excess_two_binary_two_unary.py --check
python3 scripts/c5_excess_two_two_unary.py --check
python3 scripts/c5_excess_two_two_binary.py --check
python3 scripts/c5_excess_two_binary_omission.py --check
python3 scripts/c5_excess_two_three_unary.py --check
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
