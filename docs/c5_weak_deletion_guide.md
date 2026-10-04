# Weak-deletion／單側與共同出口導覽

更新：2026-10-04。本頁整理既有成果，不新增研究結論。
研究線標記見 [HANDOFF](HANDOFF.md)，全文件索引見 [STATUS](STATUS.md)，
共通信任界線與工作約定見 [DOCUMENTATION](DOCUMENTATION.md)。

本批成果及D至D₅稽核的發布驗證見[發布紀錄](history/2026-10-04-c5-parallel-progress-publish.md)；
新checkout的凍結快照／完整輸出先依[封存還原說明](../audits/README.md)還原。

主線首批[開放葉 ledger 與趨勢](c5_open_leaf_ledger.md)以共鄰 P₃ 的固定
3500 個 case／geometry／join keys 計數：C₂→C₃→C₄ 各閉合一葉，
目前 3497 葉未稽核／未關閉，36 cases／140 geometries 均仍開放。
這是具名目錄的階段趨勢；全主線葉總數及每日下降率尚未知。
**後續（2026-10-04，任務 W）：** [q-core 盾弧預算](c5_qcore_shield_budget.md)的紙面定理 C-W
把其餘 3497 keys 全部作來源排除；[D₆ 稽核](../audits/2026-10-04-task-d6/REPORT.md)確認並補零-unary 側，故 C §1 整個共鄰端點 P₃ 分支排除完成（原 ledger 尚未合併）；見 §3。

## 1. 目標與範圍

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
| 唯一 mixed 共鄰端點 P₃ | 任意 unary 大小的雙扇區與 triangle tether 引理；x₁ 強制唯一框色 2 時來源排除，x₂ 附件為色 2 時只留 used-singleton／pair；仍留 36 具名必要 residual，未證出口 | [短子弧與完整殘留](c5_mixed_p3_common_endpoint.md) |
| 共鄰 P₃ 一色支援三接點 unary | CPP-134-1／geometry 30／side_join 20：任意大小化約迫原 triangle，原外路給 K₅ subdivision；只關閉這份側接合，未 Lean 化 | [C₂ 原身份與 minor](c5_mixed_p3_one_color_ternary_unary.md) |
| 共鄰 P₃ 雙框點三接點 unary | CPP-134-1／geometry 34／side_join 20：原禁色 slack 排接點碰 b₂，palette 分 T／N 葉，原外路 K₅ 排 N 後重證葉數；任意 unary 大小，只關閉這份側接合，未 Lean 化 | [C₃ 原雙框點葉與 bridges](c5_mixed_p3_two_frame_ternary_unary.md) |
| 共鄰 P₃ 雙框點兩份 unary | CPP-134-1／geometry 34／join60：逐份自身附件固定 0、1；兩份完整原 relations／bridges 對 2↔3 封閉，與指定禁色各自矛盾；任意大小來源排除，其他 joins 保留 | [C₄ 逐份完整關係](c5_mixed_p3_two_frame_two_unary.md) |
| 更一般 roots／出口 | degree≥6、多 degree-5、非樹／非相鄰 roots 與共同出口仍開放 | [Root 預算](c5_root_degree_excess.md)、[一般出口界線](c5_single_sided_exit.md) |

先讀候選與 minimal obstruction，再讀條件式出口的適用範圍，最後接到本線停止點。

## 3. 精確停止點與下一個窄問題

**本線精確停止點：no-mixed 指定 p₁、p₂ 已有免表共同存在性分離；
唯一 mixed 原 P₃ 的兩個不同接點、各一 root incidence 接線，全部
residual 均已作任意 unary 大小的 disk 來源排除；共鄰端點已有雙扇區
引理及部分來源排除；前層保留 36 具名必要案例，後續已關閉其中
CPP-134-1／geometry 30 及 34／side_join 20 的兩份原三接點身份。未 Lean 化。**

[Mixed 容量](c5_mixed_capacity_contacts.md)從完整關係證明：固定另一 root
顏色後，禁止本側顏色至多等於本側 incidences；source unary 禁色互不
重疊且缺額至多一，共十八必要側型。此容量部分容許多 mixed。
各一 incidence 的任意大 mixed 分量至多禁兩個有序色對；唯一 mixed 時，
新出現兩側 E 同為一個 pair、mixed 恰禁兩個非對角的分支。
固定 q 三點控制保留 P₃ 的 (1,1)／(1,2)／(2,1)，triangle 另留 (2,2)。
這些必要色角色不自動帶有實際支援或 disk 實現。
[P₃ 對稱分支](c5_mixed_p3_symmetric.md)現已證三個原 lists 相同、
原五環內側為空。兩份完整 root 側支援與三份星狀附件各有正跨度，
恰用完五條框邊；整側 E 的色置換不變性給矛盾。這是來源排除，
不是 target 接受；未把 P₃ 換成 shared singleton，未限制 unary 大小。

[非對稱分支](c5_mixed_p3_asymmetric.md)補齊 (1,2)／(2,1)：
完整 P₃ 拒絕迫使被拒絕的 root 色對含第四色。若一色側剩第四色，
其支援須見三色；若剩已用色 a，另一側的 {a,3} 迫支援見另外兩色，
沿原環序共需至少六框邊。容許一色側零跨度，不套用五正跨度等號。
26,400 組正規化必要側角色全排除，零 target，不是 disk 實現分類。

[中點／端點接線](c5_mixed_p3_middle_endpoint.md)現已排除 masks=(0,1,2)
及整份 root 交換／路徑反向型。完整 P₃ 只禁 (a,3)，原 x₀ 的三份
附件迫見三色；保留 x₀ 的四個連通區塊環序給兩種 residual 各至少
六框邊。22,400 組必要側角色全排除，零 target；未刪 x₀ 或換成 K2。

**任務 C：[共鄰端點 P₃](c5_mixed_p3_common_endpoint.md)** 處理 masks=(0,0,3) 及
反向型 (3,0,0)，保留原鏈、各點 (3,2,1) 份附件與任意 unary。
完整 triples={(3,d,a),(3,d,3)}，{a,c,d}={0,1,2}，禁對為
(a,3)/(3,a)。原 x₀ star、x₁ rooted Y 把兩完整側支援限制到同一
長度≤3 的 J；原 x₁–x₂–S₂ tether 再迫兩側位於 S₂ 同側。
d=2 的兩角色全部來源排除；c=2 只留 {a}/T 或 T/{a}；a=2 仍保留。
固定控制存36具名local／residual、140必要幾何及rotation正控制，
保留全部900側接合；骨架未證原unary、degree與逐邊minimality實現，0 target。

[C₂ 一色支援](c5_mixed_p3_one_color_ternary_unary.md)已關閉固定
CPP-134-1／geometry 30／side_join_id 20：自身支援恰 {b₁}、完整 degree 四
給 unary 最小內度二；Gallai／連通外部 K₄ 排除後，兩個 leaf blocks
至少耗四個原接點，故原 unary 恰為 triangle。原 z–x₂–b₄–b₃–b₂–b₁
外路給 K₅ subdivision。局部 degree／九條刪邊解除可成立，矛盾在共同
平面性；前層 36／140／900 表保持原資料，未作整份案例或 profile 刪除。

[C₃ 雙框點支援](c5_mixed_p3_two_frame_ternary_unary.md)已關閉固定
CPP-134-1／geometry 34／side_join_id 20。禁色 z=0 的 strict degree list
先迫原接點不能碰 b₂；leaf odd cycle 的 private vertices 仍可為
非接點雙框點型 N。原 z–x₂–b₄ 與框路把純 N 葉提成 K₅ minor，
剩下純接點型 T 葉才可計費；兩葉耗四接點，單 block 迫回只碰 b₁
的 triangle，與指定雙框點支援矛盾。原 N odd cycle＋bridge＋T triangle
控制保有 degree 四、六完整 tuples 及逐邊刪除解除，顯示原幾何步驟必要。
原 w relation／P₃／全部附件保持；前層表不刪，未算整份 case 完成。

[C₄ 逐份完整關係](c5_mixed_p3_two_frame_two_unary.md)已關閉
**CPP-134-1／geometry 34／side_join_id 60、side IDs=(27,1)**：
保留原 P₃／共同色框／w 原三接點；z 的兩份 unary 接點數 (2,1)、
禁色 ({0,3},{2})。逐份自身支援包含於 {b₁,b₂}，九份 necessary covers
均使完整原 lifts 對 2↔3 封閉，兩份指定完整 relations 各自矛盾。
任意大小原 bridges 同時保持；整側禁色不變不能取代原 ownership。
停止於這個固定 key；其他 joins、geometry35、root 交換型或整份 case
沒有逐份登記完成，原 36／140／900 表及稽核快照保持。若續作其他 keys，
先選具名 geometry／join，再核對各分量自身附件與完整 relation，不能任意分配整側支援。
下一具名未稽核入口為 **CPP-134-1／geometry35／join20、side IDs=(8,1)**：
自身支援A_z={b₁,b₂}、A_w={b₂,b₃,b₄}，各側一份ternary unary且無spokes，
禁色分別{0,2,3}／{0,2}。contacts順序及未知完整relations見D₅ scope ledger；
此處只定位原表entry，沒有分析或新增排除。
同一 ternary 引理對其他 w 角色的逐份覆蓋也未展開。

**後續（2026-10-04，任務 W；取代上述 geometry35 入口）：** [q-core 盾弧預算](c5_qcore_shield_budget.md)
給不需 T4 的紙面定理 C-W：C* 的原支援 |S₀|=3 迫 |σ_C*|≥2；每份 unary 若支援落在一條框邊，
原外路 r–x₂–x₁–x₀–b_h 接上短支援 hub 論證給 K₅，故 |σ_D|≥2；三份 one-sided 盾弧互斥，
需 6>5 條框邊。固定目錄每葉兩側都至少一份 unary，**3497 keys 全部來源排除，目錄剩 0**；
連同 C₂／C₃／C₄，固定目錄已無殘留。[D₆ 獨立稽核](../audits/2026-10-04-task-d6/REPORT.md)逐項重推確認，並補出零-unary 側排除（[W 報告 §8](c5_qcore_shield_budget.md#8-稽核後更正與補證2026-10-04d₆-之後)），所以 **C §1 前提下整個共鄰端點 P₃ 來源分支排除完成**。verdict 已改為修訂版（舊版保存為 v1），重播通過。
整合者已重播 checker（一般與 seed17 bytes 相同），並逐步核對證明及首列的手算盾弧
（C* 支援 {0,1,4} 佔 {40,01}，兩份 unary 只剩三邊）。任務 C 當輪刻意不用 Gallai，
短支援引理與跨 root 盾弧互斥（`0b5e00a`）都在其後，所以舊殘留與此排除不衝突。
原 [ledger](c5_open_leaf_ledger.md) 尚未以 `--write` 合併；36／140／900 表與 rotation 控制保留。

**下一入口（2026-10-04 記錄，優先於逐 key 工作）：**
1. ~~獨立稽核任務 W~~（D₆ 已完成）。剩下依 [D₆ 合併計畫](../audits/2026-10-04-task-d6/scope_history/MERGE_PLAN.md)
   合併 ledger：重算器 `STAGES` 改具名規格、加 batch 抽取與 `--dry-run`，輸出到新版本目錄，原 C₄ ledger 不變。
2. 把定理 W-A（q-core 中 unary |σ|≥2、盾弧互斥、至多兩份 unary）統一套到本線其餘保留分支：
   更多 incidences、更大／多 mixed。先判定哪些分支含**三個不同**原 one-sided pieces 各有盾弧≥2
   （unary 需由 q-critical 接點邊取拒絕見證並有避開自身的外路），它們由同一六邊矛盾直接排除；其餘再逐型處理。
   不帶 criticality／degree 前提的「長支援分量＋兩份 unary 不可能」是錯的（D₆ §2.7 反例）。停止條件：出現 roots 不連通的分隔型分量，
   或 unary 找不到避開自身的外路，保存具名配置後停止推廣。
全部具名殘留、側角色及 replay 見[報告 §5–6](c5_mixed_p3_common_endpoint.md#5-固定控制完整殘留清單與重播)。
不能拆共鄰點或改成 shared singleton。其餘更多 incidences 的接線仍保留。
先前 D₂ 對 C 的覆蓋限於當輪停止點與重播入口；A／B 新增身份／完整 joint／witness
稽核的範圍另見[D₂整合稽核](../audits/2026-10-04-task-d2/REPORT.md)，不把其覆蓋算入C。

[無增長](c5_no_mixed_no_growth.md)與[增長完備性](c5_no_mixed_growth_completion.md)
已關閉 no-mixed 有害增長缺口；不重啟十五類支援枚舉。
更大 mixed、多 mixed 的跨列／幾何、逐染色 repair、非相鄰 roots、多
degree-5、degree≥6 與一般／共同出口仍保留。
完整 Σ 的出口接合仍明用來源雙缺失與刪邊繼承。

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
| 共鄰原 P₃ 的雙扇區／tether | 原鏈與 (3,2,1) 附件把全部側支援限制到長度≤3 子弧、兩 roots 在 S₂ 同側；部分 source 排除，36 案例保留 | [共鄰短子弧](c5_mixed_p3_common_endpoint.md) §3–6 |
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

C₄已由[D₅固定快照與獨立稽核](../audits/2026-10-04-task-d5/REPORT.md)驗收：
九份逐分量自身支援、27完整relation組合及原bridges／lifts保持。
只新增(CPP-134-1,34,60)，連同C₂／C₃恰三keys，另外3497keys未關閉；
3500keys與原36／140／900表完整保留，w完整relation仍未知。

正式返回C₃的獨立驗收與固定快照見[D₄整合稽核](../audits/2026-10-04-task-d4/REPORT.md)，
前序C／C₂的完整relation／空fibres／原K₅覆蓋見[D₃稽核](../audits/2026-10-04-task-d3/REPORT.md)。
合用C₂／C₃只登記(CPP-134-1,30,20)與(CPP-134-1,34,20)兩keys；
3500份具名必要geometry×join索引全部保存，原36／140／900表不刪。
該次 D₄ 沒有把 geometry34／join60、其他 w 角色或整個 case 視為已驗收；
後續 [C₄](c5_mixed_p3_two_frame_two_unary.md)另只登記 (CPP-134-1,34,60) 排除。

最近 C₄ 輪的實際驗證、命令、證據界線與未重跑範圍見
[兩份原 unary 紀錄](history/2026-10-04-mixed-p3-two-frame-two-unary.md)。最小入口：

```bash
python3 scripts/c5_mixed_p3_two_frame_two_unary.py --check
python3 scripts/c5_mixed_p3_two_frame_ternary_unary.py --check
python3 scripts/c5_mixed_p3_one_color_ternary_unary.py --check
python3 scripts/c5_mixed_p3_common_endpoint.py --check
```

C₂ 原驗證見[一色支援紀錄](history/2026-10-04-mixed-p3-one-color-ternary-unary.md)。

前一共鄰端點輪重跑新 checker（一般與 `PYTHONHASHSEED=17`）、mixed
容量、middle-endpoint、完整有序介面、既有 Lean build 及文件／DocGraph；
命令及未重跑範圍見[共鄰紀錄](history/2026-10-04-mixed-p3-common-endpoint.md)。
最小入口：

```bash
python3 scripts/c5_mixed_p3_common_endpoint.py --check
PYTHONHASHSEED=17 python3 scripts/c5_mixed_p3_common_endpoint.py --check
```

最近中點／端點輪重跑新 checker（一般及 `PYTHONHASHSEED=17`）、
mixed 容量、非對稱、完整有序色對介面、既有 Lean build 及文件／DocGraph；
確切命令與未重跑範圍見[中點／端點紀錄](history/2026-09-30-mixed-p3-middle-endpoint.md)。最小入口：

```bash
python3 scripts/c5_mixed_p3_middle_endpoint.py --check
PYTHONHASHSEED=17 python3 scripts/c5_mixed_p3_middle_endpoint.py --check
python3 scripts/c5_mixed_capacity_contacts.py --check
python3 scripts/c5_mixed_p3_asymmetric.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
```

先前 P₃ 非對稱分支輪重跑新 checker（一般及 `PYTHONHASHSEED=17`）、
前層對稱、mixed 容量、完整有序色對介面、既有 Lean build 及文件／DocGraph；
確切命令與未重跑範圍見[非對稱紀錄](history/2026-09-30-mixed-p3-asymmetric.md)。最小入口：

```bash
python3 scripts/c5_mixed_p3_asymmetric.py --check
PYTHONHASHSEED=17 python3 scripts/c5_mixed_p3_asymmetric.py --check
python3 scripts/c5_mixed_p3_symmetric.py --check
python3 scripts/c5_mixed_capacity_contacts.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
```

先前增長完備性輪重跑新 checker（一般及 `PYTHONHASHSEED=17`）、前層
no-growth／local-screen／root-transport、文件／DocGraph 與既有 Lean build；
確切命令及未重跑範圍見[增長紀錄](history/2026-09-29-no-mixed-growth-completion.md)。最小入口：

```bash
python3 scripts/c5_no_mixed_growth_completion.py --check
PYTHONHASHSEED=17 python3 scripts/c5_no_mixed_growth_completion.py --check
python3 scripts/c5_no_mixed_no_growth.py --check
python3 scripts/c5_no_mixed_local_screen.py --check
python3 scripts/c5_no_mixed_root_transport.py --check
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

增長 checker 重播紙面指定框弧及原外路，不搜尋舊框弧規則；
無增長 checker 只用標準函式庫，獨立重建原共同側弧、候選域及短側
論證步驟；不讀舊接受 flags。局部 checker 重算全部增長候選，重用
既有支援穩定子、固定框弧及 minor 控制函式，不讀取舊 target 接受或
排除 flags 作判定。Root-transport
獨立核對搬運、側弧配置、候選域及三介面逐候選相等。十五類完整
重播屬[前輪跨度整理](history/2026-09-29-no-mixed-span-budget.md)，不是
最近增長完備性輪重跑。舊 (2,2) 文件 SHA 差異及內容重播見
[缺額型紀錄](history/2026-09-29-adjacent-no-mixed-t2-t0-pairs.md)。

雙拒絕 atlas 與 Lean axiom audit 另見 [分類報告](c5_two_rejection_proof_zh.md) 與 [Lean 工具](lean_two_rejection_tools.md)。
原重疊型研究輪未單獨重跑 t2 初層／interfaces、其餘 mixed／唯一 degree-5 完成表、雙拒絕 atlas、R 系列、profiles／閉包及 Lean axiom audit。
發布狀態以即時 Git 為準；歷史生成器可能覆寫 artifacts，勿把重建指令當只讀 checker。
早期交接見 [HANDOFF_HISTORY](HANDOFF_HISTORY.md) 與 [2026-09-22 快照](HANDOFF_2026-09-22.md)；歷史待辦與 Git 狀態均非現況。
