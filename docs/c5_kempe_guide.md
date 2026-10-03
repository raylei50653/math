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
| 雙 root 的 ε=2 收窄 | 相鄰 mixed 刪 roots／zw 全收；相鄰唯一 mixed 已全排 (4,4) 核心、五-spoke 原來源及四-spoke (3,1) 全部 incidence 分拆，含 root 交換。(2,2)、mixed-(1,1) 加各側一 unary 的共用 spoke-pair 已排除 7／9 份，unequal pairs 仍保留 40／66 份。較少 spokes、單省略及原 (5,5) 核心亦保留。紙面＋Python，ε≥3 未證，未 Lean 化 | [共用 pair 的原三角延拓](c5_excess_two_mixed_core_four_spoke_equal_pair.md)、[原四接點 leaf-slack](c5_excess_two_mixed_core_four_spoke_quaternary.md)、[原三接點身份](c5_excess_two_mixed_core_four_spoke_ternary.md)、[binary 端點 hub](c5_excess_two_mixed_core_four_spoke_hubs.md)、[兩 unary 排除](c5_excess_two_mixed_core_four_spoke_singles.md) |
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
| 四-spoke (3,1) 的 mixed-(1,1) 加兩原單接點 unary | 原 Σ-critical witnesses、b–a–框點外路徑與短支援定理迫三份原分量跨度至少六，與共同五段 lifts 矛盾，含 root 交換；288 同源支援域與完整五點 joint 核對 | [兩原 unary 的六跨度排除](c5_excess_two_mixed_core_four_spoke_singles.md) |
| 四-spoke (3,1) 的 mixed-(1,1) 加一原 binary unary | 原 star 殘留32／64份由同列 tightness／端點 hub 的二、三 hub Gallai K₅ 全排，含root交換；192原query、10,752完整U schemas與42原degree圖核對。完成這個原incidence子型，ε≥3未證 | [同列端點 hub 排除](c5_excess_two_mixed_core_four_spoke_hubs.md)、[原 star](c5_excess_two_mixed_core_four_spoke_star.md)、[marked-leaf](c5_excess_two_mixed_core_four_spoke_binary.md) |
| 四-spoke (3,1) 的 mixed-(1,2) 加一原單接點 unary | 同色原 spoke 省略後 M 自己 minimal；原 K=C+a 的三接點 (a,y₀,y₁) 接上既有 active-triangle K₅，全部20／60框架全排，含root交換。200 queries、50完整degree圖、1,500 joints／24,000纖維；紙面＋Python，ε≥3未證 | [原三接點身份與整型排除](c5_excess_two_mixed_core_four_spoke_ternary.md) |
| 四-spoke (3,1) 的 mixed-(1,3) 無 unary | 原 K=C+a 的四 contacts=(a,y₀,y₁,y₂) 要求三禁色，但 marked leaf 迫至多二；原逆序貪婪直接構造 M／G 延拓，20／60 框架全排，含 root 交換。80 完整 degree 圖、2,400 joints／38,400 纖維及 2,400 貪婪 witnesses；結合前三子型完成全部 (3,1) incidence 分拆 | [原四接點 leaf-slack 排除](c5_excess_two_mixed_core_four_spoke_quaternary.md) |
| 四-spoke (2,2) 的 mixed-(1,1) 加各側一原 unary：共用 pair | 原 spoke diamond 封 C 於一個原三角形，既有三-hub 引理延拓每份合法原三角染色；接原 G−C 全收迫 G 全收，排除相同 pair 的 7／9 份，含原 01／01 與 root 交換。仍保留 40／66 unequal-pair 框架；36 完整 degree 圖、2,520 joints／40,320 fibres | [共用 pair 的 sealed mixed 排除](c5_excess_two_mixed_core_four_spoke_equal_pair.md) |

**停止點：(3,1) 全部四份 incidence 分拆封閉；新 (2,2)、mixed-(1,1)
加各側一原 unary 的共用 spoke-pair 窄排除已完成，含原 01／01 與
root 交換。** 原 diamond 的兩-root faces 封整份 C 在一個原三角區域，
實際支援只能碰其一個原框點。固定合法三角染色後，既有三-hub
Gallai 引理給原 C 的整份 extension；與同一原 G−C 全收接合，迫
G 全收，來源矛盾。任意大小 topology／Gallai 合成由紙面證明承擔。
933／941 的 47／75 份 (2,2) 必要框架中排除 7／9 份；**unequal
pairs 的 40／66 份仍保留，整份 mixed-(1,1) 加兩 unary 尚未完成。**
其中共用一個原框點者為 26／48 份，不相交者為 14／18 份；
[整理 audit](history/2026-10-03-excess-two-four-spoke-progress-publish.md#整理時核對的發現)
保存全部具名骨架與原 rotations，分組不提供新來源排除或實現性。

下一窄入口為原 a=5、b=6、spokes=01／02，source indices=97／133，
root 交換為 111／153。保留同一 R_C(x,y)、R_U(u)、R_V(v)、
實際附件／supports、原環序與完整 (a,b,x,y,u,v) joint，分清 x=y
與 x≠y。先分析原 C 所在 face 的實際支援包絡；不以整個 sector
或 endpoint marginals 代替原 relation，不重開來源圖枚舉。

其他 (2,2) incidence、較少 spokes、原 unary 單省略，以及原 G 自己是
(5,5) q-core 的分支仍保留；不能套唯一 degree-5 分離定理。
相鄰多 mixed 在刪 zw 全收後的原來源、no-mixed、非相鄰雙 roots
與 unary 側例外亦保留。**單 spoke 省略尚未整型排除，ε≥3 未證。**
指定列出口不提升為完整候選排除，不重開來源圖枚舉。

本線另保留一般 connectivity、可迭代充分 state 及共同安全 repair
的缺口。固定圖成功歷程不提供跨圖常數上界；一般單側／共同出口
與 K∞=K≤5 未證，接手點見 [weak-deletion 導覽](c5_weak_deletion_guide.md)。

## 4. 閱讀與重播入口

本次七輪的完成範圍、具名殘留、文件 hash 漂移及實際發布驗證見
[四-spoke 整理與發布紀錄](history/2026-10-03-excess-two-four-spoke-progress-publish.md)。
前序九輪的完成範圍、整理發現、實際重播與貼用摘要見
[雙 root 進展整理與提交紀錄](history/2026-10-03-excess-two-dual-root-progress-commit.md)。
最新先讀 [共用 pair 的 sealed mixed 排除](c5_excess_two_mixed_core_four_spoke_equal_pair.md)
與 [本輪研究紀錄](history/2026-10-03-excess-two-four-spoke-equal-pair.md)，
再讀 [原四接點 leaf-slack 排除](c5_excess_two_mixed_core_four_spoke_quaternary.md)，
再讀 [原三接點身份與整型排除](c5_excess_two_mixed_core_four_spoke_ternary.md)，
再讀 [同列端點 hub 整型排除](c5_excess_two_mixed_core_four_spoke_hubs.md)，
再讀 [原三-spoke star 扇區排除](c5_excess_two_mixed_core_four_spoke_star.md)，
再讀 [四-spoke binary 必要化約](c5_excess_two_mixed_core_four_spoke_binary.md)，
再讀 [四-spoke 六跨度排除](c5_excess_two_mixed_core_four_spoke_singles.md)，
再讀 [原 leaf 色纖維](c5_excess_two_mixed_core_leaf_fibers.md)，
再讀 [單 spoke 原附件化約](c5_excess_two_mixed_core_single_spoke.md)
與 [省略原 mixed](c5_excess_two_mixed_omission.md)；前置核心身份及
刪 root／zw 化約由 §3 報告表往回追。各輪詳細驗證保留在報告所連研究紀錄。

前序九份 checker 的歷史重播命令（本次只重跑 leaf；文件 hash 漂移另述）：

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

共用 pair 證書以
`PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_equal_pair.py --check`
重播，保存完整原 C／U／V、六點 joints、空纖維、全部 unequal-pair
具名殘留；並唯讀重算既有三-hub payload 相同。原四接點 leaf-slack 證書以
`PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_quaternary.py --check`
重播，保存完整四點 relations、六點 joints 及原 spanning-tree 全圖 witnesses。
原三接點身份證書以
`PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_ternary.py --check`
重播，並精確重算既有(3,1)完整payload；其獨立checker為
`PYTHONHASHSEED=17 python3 scripts/c5_single_spoke_three_one.py --check`。
原單spoke歷史byte-check有三份既有docs hash漂移；前輪完整數學payload
已唯讀重算相同，本輪沿用該audit，詳見[原三接點身份紀錄](history/2026-10-03-excess-two-four-spoke-ternary.md)。
同列端點 hub 證書以
`PYTHONHASHSEED=17 python3 scripts/c5_excess_two_four_spoke_binary_hubs.py --check`
重播。原 star 證書以
`PYTHONHASHSEED=17 python3 scripts/c5_excess_two_four_spoke_binary_star.py --check`
重播，只需 Python 標準函式庫。四-spoke binary 證書另以
`PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_four_spoke_binary.py --check`
重播。兩 unary 的原 `c5_excess_two_mixed_core_four_spoke_singles.py --check`
因 leaf 文件的一份 hash 漂移而未通過；以
`PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_four_spoke_progress_audit.py --check`
完整重算數學 payload 及非文件 inputs，保存差異與原證書。
原 byte-check 狀態與實際沿用／重跑範圍見本次整理紀錄。

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
