# 文件狀態與可能變化追蹤

更新日期：2026-09-18。本次提交自 `e14874d` 整合 R24–R31 與文件盤點。
最新研究 R31 見 §35，文件盤點見 §36，本次發布核對見 §37；既有發布核對見 §27。
各輪當時的未提交狀態保留於原節；即時提交與遠端 SHA 以 Git 為準。
早期發布核對見 §16；共用點雙 triangle、單長奇環、單 triangle、樹及區域見 §15–11。
先前兩輪長環研究與發布紀錄保留於 §7–8。
此頁是目前文件索引及後續觀察紀錄，詳細數學敘述仍以原報告為準。
研究主入口是 [HANDOFF.md](HANDOFF.md)，逐輪原始交接保存在
[HANDOFF_HISTORY.md](HANDOFF_HISTORY.md)。新成果是紙面歸納與化約控制，未擴大 disk catalog。
§11–15 及專題報告中的「HEAD／未提交」保留研究當時狀態；即時發布狀態以 Git 為準。

## 1. 閱讀順序與文件角色

| 需求 | 入口 | 用途 |
| --- | --- | --- |
| 接續當前研究 | [HANDOFF.md](HANDOFF.md) | 現況、精確停止點、信任界線及最小重播命令 |
| 找報告或追蹤待變化項目 | 本頁 §2–4 | 專題文件的分組索引、已被後續處理的舊問題、仍待驗證的方向 |
| 核對主命題與證明路線 | [C5 boundary relations](c5_boundary_relations.md) | K∞=K≤5、有界代表與局部壓縮的區分；§5.1 是早期路線成果，近期 block 進度見交接 |
| 核對某項數學結論 | §2 對應專題報告 | 前提、紙面論證、具名 Lean 定理、script／artifact 與驗證限制 |
| 查當時的數字、命令或發布說明 | [歷史交接](HANDOFF_HISTORY.md) | 原 2,695 行全文保留；「最新／下一步／未提交」只描述各輪當時狀態 |

**讀表約定：**「已完成」只對該文件明列的範圍成立；「有限」不代表任意圖；
「紙面＋證書」不代表整個命題已 Lean 化。「較早報告」仍可作證據來源，
其舊停止點若已被續作處理，應讀 §3 的後續入口。

## 2. 專題文件全索引

### 2.1 目前主線：weak deletion 與 minimal obstruction

| 文件 | 現況與剩餘界線 |
| --- | --- |
| [同末端不同二接點正常形](c5_degree5_same_terminal_triangles.md) | R31：408 模板／327,968 接線非 disk；任意長來源 minors 待補，是目前下一題 |
| [中間二接點來源 minors](c5_degree5_middle_cycle_minors.md)、[中間 C5 正常形](c5_degree5_middle_pentagon.md) | R29–R30：正常形覆蓋與 boundary 固定來源 minors 合成，排除任意長中間不同二接點鏈型 |
| [三環鏈全部接點位置](c5_degree5_three_cycle_positions.md) | R28 完整 list 接合；不同點 F={D}，同點保留完整 F；中間二接點圖層由 R29–R30 補完，同末端由 R31 完成正常形 |
| [末端二臂來源 minors](c5_degree5_three_cycle_minors.md)、[三個 triangle 正常形](c5_degree5_three_triangles.md)、[三環鏈 root](c5_degree5_three_cycle_roots.md) | R25–R27：完整接合、正常形與來源 minors 已接通，排除末端各一臂的任意長共用點鏈型；一般三環未完成 |
| [共用點雙奇環來源 minors](c5_degree5_shared_cycle_minors.md)、[共用點四列介面](c5_degree5_shared_cycle_roots.md) | R23–R24：四列布林縮環與真正來源 minors 分開驗證；結合互斥型完成恰兩個 odd-cycle blocks，完整 root／交集不保持 |
| [互斥雙長環](c5_degree5_two_long_cycles.md)、[混合雙環來源 minors](c5_degree5_long_triangle_minors.md)、[混合雙環 root](c5_degree5_long_triangle_roots.md) | R20–R22：混合 root 介面、來源 minors 與連續縮減已接通，互斥雙環任意長度排除 |
| [標記路徑 minor 與同點排除](c5_degree5_bridge_mark_minors.md) | 1,044 型／571,400 接線完整非 disk 覆蓋；198 長來源／432 次真正 minors；結合 R15–R17 排除恰兩個 triangles；含長環後由 R21–R24 補完 |
| [同點接入標記介面](c5_degree5_bridge_marks.md) | 36 組 root 查詢、858＋186 型及 12,711 次色序列縮減；來源 minors 與拓撲覆蓋由 R19 補完 |
| [互斥雙環任意外臂](c5_degree5_bridge_arms.md) | 兩側不同環點接入的任意外臂排除；36,672 模板／246,645,568 接線完整覆蓋，同點接入後由 R18–R19 補完 |
| [互斥雙環 bridge](c5_degree5_bridge_triangles.md) | 同側接點化回單環；直接私有接點子型任意長 bridge 排除，132 模板／43,696 lifts 非 disk；剩餘外臂位置後由 R17–R19 補完 |
| [單邊刪除](c5_disk_deletions.md)、[A/B weak successors](c5_disk_weak_successors.md) | 同 Σ 不決定完整單步後繼；指定 A/B 的 silent closure／weak successors 已核對，不能外推全部圖 |
| [完整 k≤3 audit](c5_weak_deletion_audit.md)、[completion／bisimulation](c5_completion_weak_bisimulation.md) | 1,246,132 raw states 無碰撞；同頂點 completion 已有紙面證明，一般 bisimulation／finite traces 有假設式 Lean 定理；拓撲與生成器未形式化 |
| [87-state quotient](c5_weak_quotient.md)、[候選 A/B/C](c5_weak_candidates.md) | W 不等於 inclusion Hasse diagram，可達閉包也不等於 inclusion order；三個候選的一般版仍未證 |
| [最小阻礙與三出口](c5_weak_critical_cores.md)、[repair sets／dual flows](c5_weak_flow_repairs.md) | 一般紙面充要條件已建立；非同面控制指出 disk 前提不能省；一般單側與共同出口仍未證 |
| [至多三內點](c5_weak_list_cores.md)、[四內點](c5_four_vertex_cores.md) | disk／T4 小核心的單缺失分類已完成；存在無界大小的單缺失核心，不能改猜全部 minimal core 內點數有界 |
| [odd-join 家族](c5_odd_join_cores.md)、[degree-4 樹](c5_tree_cores.md) | 各自整個無界家族的單缺失分離已有紙面化約＋有限證書；不是一般 minimal quotient 分類 |
| [triangle 接枝](c5_triangle_branches.md)、[root 介面](c5_root_interfaces.md) | 兩尾可同面；兩點 forcer 的完整 root 介面替換已有反例，必須保留適用範圍；後續路徑／分叉工作已處理原窄問題 |
| [triangle 路徑枝](c5_triangle_path_reduction.md)、[第一分叉](c5_triangle_forks.md) | 任意長路徑、任意外掛樹的全 degree-4 單 triangle 分支已處理；T4 下只缺 q |
| [cycle-5／單環](c5_pentagon_branches.md)、[兩 triangle blocks](c5_two_triangle_blocks.md) | 全 degree-4 單環長度至少 5 排除；兩 triangle blocks 只剩直接 bridge 六內點正常形，存活者只缺 q |
| [互斥多環](c5_three_triangle_blocks.md)、[三環共用點](c5_shared_triangle_blocks.md) | 頂點互斥 triangles 任意總數至多二；恰三環全部連接型排除；不能把「互斥」限制去掉 |
| [四環鏈](c5_four_triangle_chain.md)、[四環分叉](c5_four_triangle_star.md)、[bridge pruning](c5_shared_pair_bridge.md) | 恰四環全部連接型排除；其下一題由 triangle-tree 報告處理；一般替換仍是紙面，介面及拓撲控制為 Python 證書 |
| [任意 triangle tree](c5_triangle_tree_palettes.md) | 七種介面歸納、非 D 二色禁集吸收與閉鄰域 minor；全 degree-4 連通 triangles／bridges 類別中，triangles 必互斥且至多二，不需 T4；未 Lean 化 |
| [長 odd-cycle root](c5_odd_cycle_roots.md) | 一般 root 有十一種介面；不可著色時仍為互補 pairs；保留三點縮成 triangle，排除恰一個長環加任意 triangles／bridges，不需 T4；紙面＋既有證書，未 Lean 化 |
| [多長 odd-cycle](c5_multi_odd_cycles.md) | 十一種介面在任意有限環樹封閉；連續 minor 排除 odd-cycles／bridges 類別中的所有長環，剩餘 triangles 互斥且至多二；不需 T4，紙面＋有限證書，未 Lean 化 |
| [K4 block／全 degree-4 合成](c5_k4_blocks.md) | K4 經 boundary 接路給 K5 minor；結合 Gallai-tree 與既有分類，接受 T4 的全 degree-4 disk minimal obstruction 只缺 q；紙面＋證書，未 Lean 化 |
| [唯一 degree-5 完整接點介面](c5_degree5_interfaces.md) | 共同端點關係、禁色覆蓋的 minimality 充要條件、分量刪邊解除及固定來源圖至多四開關；disk／T4 幾何排除仍開放，紙面＋證書，未 Lean 化 |
| [三-spoke 區域化約](c5_degree5_sectors.md) | 單一二接點分量縮到兩個鏡像 pentagon；完整接合代數與非 minimal disk 控制，最終排除仍未解；紙面＋證書，未 Lean 化 |
| [三-spoke 任意樹分量／連通外框](c5_degree5_tree_components.md) | 任意樹的固定-q 化約與五種閉色序列、648 個必要 lifts 排除；t≥1 的 degree-4 分量不含 K4；含 cycle 的分拆 (2) 仍未解，未 Lean 化 |
| [三-spoke 單 triangle 二接點](c5_degree5_triangle_components.md) | 旁支／共同／不同接點三型全部排除；528 模板、89,224 接線非 disk，不限 bridges 長度或分叉；單長環由下一列處理，未 Lean 化 |
| [三-spoke 單長奇環二接點](c5_degree5_odd_cycle_components.md) | 保留接點縮成 triangle，保持全部固定-q z 色及 minimality；任意單 odd-cycle 加 bridges 排除，147 張具名來源 minor 控制；雙環由 R15–R24 補完，一般多環仍開放，未 Lean 化 |
| [三-spoke 共用點雙 triangle](c5_degree5_shared_triangles.md) | 共用 cut vertex 的任意二接點位置／外枝排除；888 模板、295,920 接線非 disk；互斥雙 triangle 後由 R16–R19 補完，未 Lean 化 |

### 2.2 Kempe、計數與固定圖策略

| 文件 | 現況與剩餘界線 |
| --- | --- |
| [Kempe screen](c5_kempe_screen.md)、[adjacent-singleton 計數](c5_adjacent_singleton_counts.md) | 必要條件與剩餘候選已保存；一般 adjacent-singleton lemma 未證，與主線的相鄰雙「缺失」候選 A 不同 |
| [count-cone bridge](c5_count_cone_bridge.md)、[B₅ face](c5_b5_face.md)、[Kempe-class 計數](c5_kempe_class_counts.md) | near-triangulation 化約、部分 Lean 代數及 class 級紙面計數已完成；普通 pairing 不給最終矛盾，cone／connectivity 缺口仍在 |
| [connectivity surgery](c5_kempe_connectivity.md)、[AB 立方體](c5_ab_swap_cube.md)、[complementary 立方體](c5_complementary_cube.md)、[高度數 disk](c5_corner_disks.md) | 同圖 connectivity 更新與控制可重播；AB-only 必逃逸、固定 AB\|CD 必失敗等推測已有反例；較早低度數零 survivor 不再是一般候選依據 |
| [edge states](c5_edge_states.md)、[incidence](c5_edge_incidence.md)、[edge switches](c5_edge_switches.md)、[多候選 choices](c5_edge_choices.md) | pairing／incidence 壓縮不足與 coherent witness 操作已核對；多候選欄位不能任意拼成同一個可實現 state |
| [cut interfaces](c5_cut_interfaces.md)、[cut observations](c5_cut_observations.md)、[equal-cut witness](c5_equal_cut_witness.md) | retained components 的一般重建已有 Lean 支援；粗 cut 量與同 cut 長度不足已有實現反例；一步重建不等於多步充分狀態 |
| [behavior 提案](c5_behavior_refinement.md)、[第一輪](c5_behavior_refinement_results.md)、[radius 2](c5_behavior_radius2.md)、[cycle ablation](c5_cycle_ablation.md) | 提案與有限結果分開；兩／三步 iff 為條件式紙面引理，未 Lean 化，也未證閉包充分性 |
| [策略閉包](c5_strategy_safe.md)、[barriers](c5_strategy_barriers.md)、[禁補償](c5_strategy_no_comp.md)、[alternative exit](c5_alternative_exit.md) | survivor-811 固定閉包與必要低谷／回升已保存；不能據此證一般 K=4 策略或要求每步 cycle complexity 不增 |
| [local exit](c5_local_exit.md)、[singleton preparation](c5_singleton_preparation.md)、[guard repair](c5_guard_repair.md)、[repair interface](c5_repair_interface.md) | 條件引理與 B₂ 有限準備已保存；來源 7／17 同候選介面卻 Δχ=−1／+1，共同安全機制仍未證 |

### 2.3 基礎、枚舉、grammar 與其他支線

| 文件 | 現況與剩餘界線 |
| --- | --- |
| [Lean 接合基礎](lean_root_interfaces.md) | 15 個普通 Lean 定理與報告對照；刪邊解除、奇環剛性及 minor／disk 層仍未形式化 |
| [研究目標](c5_boundary_relations.md) | 主命題未證；全域存在小代表、指定局部規則的完備性必須分開 |
| [phase 1](phase1.md)、[BAD 構造](construction.md)、[gadgets](gadgets.md) | 基礎 exact relation／有限 Lean 證書與 gadget synthesis；一般 planar、separating C5 的 BAD 不構成 disk 反例 |
| [automata](automata.md)、[attachment normal form](attachment_normal_form.md)、[topology completeness](topology_completeness.md) | 固定 triangle grammar 的染色語義、normal form、GeoReject 與 endpoint-order 編譯已形式化；embedding 抽取與 topology soundness 仍在紙面層 |
| [fan pentagon](fan_pentagon.md)、[boundary relation 庫](boundary_relations.md)、[pp relations](pp_relations.md) | 固定 grammar 的 87 states 與完整 relation／pair 查詢已保存；pp 求值器仍屬 Python 層，87 不是一般 cell catalogue 的 132 |
| [state language](state_language.md)、[stepwise sufficiency](stepwise_state_sufficiency.md)、[local closure](local_closure.md)、[C5 interface 想法](c5_interface_idea.md) | 表示法、strip／fan 的有界控制及 separator 引理可用；一般移動前緣、context／future 充分性、C6／C7 轉接仍待證或未啟動 |
| [cell enumerator](c5_cell_enumerator.md) | R1／SYM／prefix／DFS／bitmask／integer viable 的 Lean 鏈與外部信任已明列；k=6、7 獨立重現僅為有界計算證據；原重複 §14 已整理為 §16 |
| [extension effects](extension_effects.md) | 一般圖的新增點／邊完整 relation 變化已觀察；pair projections 漏掉高階限制，geometry=unknown 的 rows 不能當 disk transitions |

各表只概括成果層級；具體 theorem 名稱、公理審計、證書及完整重播命令仍放原報告。

## 3. 已被後續成果處理的舊停止點

以下是文件整理時確認的狀態轉移，不是本次重新證明。

| 舊問題或容易誤讀的字樣 | 目前讀法／後續入口 |
| --- | --- |
| triangle path 報告說「外掛樹分叉仍未解」 | [第一分叉報告](c5_triangle_forks.md) 已排除任意深度分叉 |
| 第一分叉報告的「下一題 cycle-5」 | [單環報告](c5_pentagon_branches.md) 已排除長度至少 5 的唯一 cycle |
| 兩環報告的「下一題三環」 | [互斥三環](c5_three_triangle_blocks.md) 與 [共用點三環](c5_shared_triangle_blocks.md) 已補齊恰三環 |
| 三環共用點的「下一題四環鏈」 | [四環鏈](c5_four_triangle_chain.md) 已完成 |
| 四環鏈的「下一題分叉型」 | [四環分叉](c5_four_triangle_star.md) 已完成 |
| 四環分叉的「bridge 混合型未涵蓋」 | [bridge pruning](c5_shared_pair_bridge.md) 已補齊恰四環；任意 cluster 再由下一列的新報告處理 |
| bridge pruning 的「任意共用點 cluster 未解」 | [palette／minor 報告](c5_triangle_tree_palettes.md) 已排除任意大小的非平凡 cluster；下一題是較長 odd-cycle 的共用點介面 |
| triangle-tree 的「下一題一個長 odd-cycle」 | [長環 root 報告](c5_odd_cycle_roots.md) 已完成介面分類及恰一個長環的排除 |
| 長環 root 的「下一題兩個長環」 | [多長環報告](c5_multi_odd_cycles.md) 已完成兩環的連續縮減，並明列任意多長環的歸納與終止論證；K4／bridge 下一題已由下列新報告處理 |
| 多長環的「含 K4 未處理」 | [K4 報告](c5_k4_blocks.md) 已排除 K4 並合成全 degree-4 的單缺失結論；下一題為恰一個 degree-5 內點 |
| K4 報告的「degree-5 完整接點介面尚未啟動」 | [新介面報告](c5_degree5_interfaces.md) 已完成染色與 minimality 公式；下一題縮到三條 z-spokes 及單一二接點 Gallai 分量 |
| 完整接點報告的「三-spoke／二接點 disk 位置未處理」 | [區域化約](c5_degree5_sectors.md) 已縮到兩個鏡像 pentagon；四色列與刪-spoke minimality 的共同實現仍未解 |
| 區域報告的「pentagon 尚無 block／path 排除」 | [樹分量報告](c5_degree5_tree_components.md) 已排除任意樹 C、t≥1 的 K4 block；含 cycle 的二接點介面仍開放 |
| 樹報告的「下一題 C 恰含一個 triangle」 | [單 triangle 報告](c5_degree5_triangle_components.md) 已處理全部接點位置及外枝；下一題為恰一個長 odd-cycle |
| 單 triangle 報告的「下一題恰一個長 odd-cycle」 | [單長奇環報告](c5_degree5_odd_cycle_components.md) 已完成保留接點縮環及三型排除；下一題為恰兩個 triangle blocks |
| 單長奇環報告的「下一題恰兩個 triangles」 | [共用點雙環報告](c5_degree5_shared_triangles.md) 已排除共用 cut vertex 分支；下一題收窄為兩個互斥 triangles 的 bridge 路徑 |
| R16／R17 的「外臂／同點接入未處理」及 R18 的「來源 minor／拓撲覆蓋未完成」 | [R19](c5_degree5_bridge_mark_minors.md) 補齊同點接入；結合 R15–R17，恰兩個 triangle blocks 已排除。下一題是長奇環與 triangle 的耦合 root 介面 |
| R20／R23 的「長環來源 minor 未完成」 | [R21](c5_degree5_long_triangle_minors.md)、[R22](c5_degree5_two_long_cycles.md)、[R24](c5_degree5_shared_cycle_minors.md) 補完混合、互斥雙長環與共用點雙奇環 |
| R24 的「下一題三環完整二接點關係」 | [R25](c5_degree5_three_cycle_roots.md) 已完成末端二臂介面；[R28](c5_degree5_three_cycle_positions.md) 擴至同鏈全部接點位置 |
| R25／R26 的「末端二臂來源 minor 待補」 | [R27](c5_degree5_three_cycle_minors.md) 已補完任意長來源與拓撲合成 |
| R28／R29 的「中間二接點圖層／來源 minor 未解」 | [R29](c5_degree5_middle_pentagon.md) 完成正常形，[R30](c5_degree5_middle_cycle_minors.md) 補完來源 minors |
| R30 的「同末端不同二接點正常形待做」 | [R31](c5_degree5_same_terminal_triangles.md) 已完成正常形；此型任意長來源 minors 仍開放 |
| 較早 handoff 的「completion 未證」 | [同頂點 completion](c5_completion_weak_bisimulation.md) 已有紙面證明；topology 未 Lean 化仍成立 |
| 較早 block 報告說「未新增 Lean theorem」 | 指該輪整個化約；後來共有 list 引理進入 [ForcingLists.lean](../Math/ForcingLists.lean)，不代表 minor／disk 論證也進入 Lean |
| 各輪「尚未提交／推送」 | 屬於當時狀態；長環兩輪已隨 `dad5940`、R9–R10 已隨 `be97121` 發布；R11–R15、R16–R20、R21–R23 的發布分見 §16、§22、§27；R24–R31 隨本次提交整合，見 §37；即時發布狀態以 Git 為準 |
| enumerator 兩個「§14」 | edge-mask 仍為 §14；獨立 cross-check 改為 §16，對應導引一併更正 |

本輪對近期主線報告補上後續連結，保留原輪次內容。歷史交接以快照方式保存，
不逐句改寫當時的未知或發布紀錄。

## 4. 可能出現新變化的地方

截至 **2026-09-18／R31** 的待追蹤項目如下；這是文件盤點提出的後續觀察，
不是新增研究結果。每項只有達到對應證據條件後，才更新結論。

| 項目 | 現況與可能的新變化 | 更新結論前要看到的證據 |
| --- | --- | --- |
| 同末端不同二接點的任意長來源 | **優先**：R31 只完成正常形；補齊後可擴大到此型任意環長／臂長 | boundary 固定 branch sets，保留共用點／兩接點／palette 錨點，逐步 degrees、完整四列、刪邊著色及 R31 拓撲合成；參考 [R30](c5_degree5_middle_cycle_minors.md) |
| 末端與中間、同點會合 | [R28](c5_degree5_three_cycle_positions.md) 已有 list 介面，圖層未完成；同點存在 1,872 組雙拒絕控制 | 同點須查完整 F 與 minimality，再建實際接線、正常形拓撲及來源 minors；不能只核對 D |
| 環間 bridge、其他分拆 (2)、更多環 | 現有 R27／R30 只覆蓋指定共用點鏈，尚無一般三環定理 | 各連接型的共同接點關係、化約及來源拓撲；無接點末端不可未驗證就刪除 |
| 可重用 Lean 基礎 | [接合定理](lean_root_interfaces.md) 已完成；degree-list slack、R10 全列刪邊解除、R23 奇環剛性可再推進 | 明確 Lean theorem 與 axiom audit；build 成功不使紙面圖替換自動形式化 |
| 一般單側／共同出口 | degree-4 與部分 degree-5 block 成果尚不能推出候選 A | 分別補一般分離與共同 pivotal edge 證明；兩個單側出口不足以推出共同出口 |
| 文件與發布同步 | R24–R31 報告、scripts、artifacts 隨本次提交整合；入口容易落後逐輪紀錄 | 新成果同步 README、HANDOFF、此頁索引／追蹤表與前輪後續連結；發布時另核對 Git 及對應 checker |

以下 R1–R15 保留早期追蹤來源；其輪次狀態以各節為準。
R16–R24 已完成恰兩個 odd-cycle blocks；R25–R31 的演進見 §29–35。
R4–R6 仍為保留方向，不因本次整理而重啟研究或擴大枚舉。

### R1：bridge pruning 給出任意總環數的 cluster 隔離

- **狀態：2026-09-17 已確認，紙面推論。**
- [新報告 §1](c5_triangle_tree_palettes.md) 核對每條外向 bridge 的替換保留
  全部前提，外側可含任意數量 cycles。可先隔離任意 maximal cluster。
- 配合 R2、R3，任意大小至少二的 cluster 皆排除，超過原來只篩 2／3／4 的推論。
  仍不能任選四環刪去其餘部分；可用選法是 R3 的完整閉鄰域。

### R2：鏈與分叉的 palette 規則統一為樹上遞迴

- **狀態：2026-09-17 紙面歸納完成，局部代數與具名控制重播通過。**
- [新報告 §2](c5_triangle_tree_palettes.md)：任意 rooted 子樹可取色集合只有
  六個二色集合或 U。全圖不可著色恰在每環有二色 palette、相鄰環互補，
  每個私有點 list 等於所屬環 palette；故每棵樹恰六種拒絕配置。
- bridge root 的三色 list／singleton 與此處共享點 U-list 是不同介面；
  rooted pair 的 D singleton 不被誤排除。此規則本身未宣稱 disk 性。

### R3：從大 cluster 抽出保留閉鄰域的小 minor

- **狀態：2026-09-17 紙面 minor 完成，48 個結構控制／63 次子樹吸收通過。**
- [新報告 §3–4](c5_triangle_tree_palettes.md)：不含 D 的二色禁集可吸收成
  兩條 spokes。新 spoke minimality 使用對側 root 能取禁集兩色的前提。
- 保留不含 D 的中心環與全部鄰環，外側禁集全不含 D；所得二／三／四環
  星形接上既有排除。保持 boundary 固定、degree、固定 q 及 minimality；
  不聲稱完整 Σ 或任意 boundary pattern 的介面等價。

### R4：bridge pruning 的證明已穩定，可能值得接入 Lean

- **狀態：形式化候選，未啟動。**
- 來源：[ForcingLists.lean](../Math/ForcingLists.lean) 與 [bridge pruning §1](c5_shared_pair_bridge.md)。
  singleton／swap 的代數已形式化；新 D 葉點三條 spokes 的刪邊延拓論證已補齊。
- 下一個確認：先定義 boundary 固定的圖替換與 edge-minimality，將染色延拓和
  degree 保持分開證；minor／disk 層另外建立所需模型，不能用新增 topology 公理代替。
  可一併處理新兩-spoke 替換；本輪 cluster 缺口已在紙面層完成，尚未形式化。

### R5：candidate A 的共同出口仍需獨立追蹤

- **狀態：一般單側與共同出口皆未證。**
- 來源：[critical cores §2](c5_weak_critical_cores.md)、[flow repairs](c5_weak_flow_repairs.md)。
  現在的 block 進度集中於 minimal obstruction 的單缺失分離。
- 下一個確認：只有找到兩側分離後，才處理共同 pivotal edge；多個替代 minimal
  obstructions 可能破壞代表圖的「共享邊＋各一私有邊」機制。不能由兩個單側出口
  自動推出共同出口，也不能把兩個 boundary fibres 當成同一完整染色。

### R6：retained-port 與 weak quotient 的充分性仍是不同問題

- **狀態：保留支線，未重啟。**
- 來源：[repair interface](c5_repair_interface.md)、[weak audit](c5_weak_deletion_audit.md)、
  [completion](c5_completion_weak_bisimulation.md)。前者已知來源 7／17 的碰撞，
  後者只有 k≤3 的 W 充分性計算與條件式 Lean bridge。
- 下一個確認：若要統一或壓縮 state，先固定操作語義，再要求候選介面通過既有
  碰撞／完整 witness history 控制。一步重建、固定圖策略與跨圖 weak congruence
  不能相互替代；本次沒有理由直接擴大 k 或重搜 survivor 閉包。

### R7：較長 odd-cycle 與 triangles 共用點的介面

- **狀態：2026-09-17 已完成，紙面論證與有限控制。**
- [長環 root 報告](c5_odd_cycle_roots.md)：一般七種介面不封閉，須加四種
  三色集合；不可著色的 mixed cluster 仍強迫相鄰環互補 pairs。
- 保留長環三點及至少一個共用點，縮成 triangle，透過 degree-list 貪婪
  引理核對 minimality，接回 triangle-tree 排除。全 degree-4、恰一個
  長 odd-cycle 加任意 triangles／bridges 的 disk minimal q-obstruction 不存在。
- 不需 T4；未聲稱完整 Σ 保持或新增 Lean theorem。30 個具名 minor 控制
  已連到既有小型模板 subdivisions；一般覆蓋由紙面論證承擔。

### R8：兩個長 odd-cycle blocks 的介面與連續縮減

- **狀態：2026-09-17 已完成，紙面論證與有限控制。**
- [多長環報告](c5_multi_odd_cycles.md)：十一種訊息在任意有限 odd-cycle
  tree 封閉，不可著色仍等價於互補 palettes；三色訊息只能出現在可著色配置。
- 保留兩長環間的路徑，連續縮減每步維持 boundary 固定、degree、q 拒絕及
  minimality。另固定環樹一條邊，按長環數嚴格下降，明確涵蓋任意多長環。
- 全 degree-4、連通的 odd-cycles／bridges disk minimal q-obstruction
  沒有長環，triangles 必互斥且至多二。不需 T4；未宣稱完整 Σ 或新增 Lean theorem。

### R9：K4 block 的三色 residual lists 與 bridge 介面

- **狀態：2026-09-18 已完成，紙面證明與有限證書。**
- [K4 報告 §1–3](c5_k4_blocks.md)：四個 residual lists 必同為三色 P，外接
  方向強迫共同補色；每個外側必碰 boundary，四路徑與 boundary 給出 K5 minor。
  全 degree-4 planar minimal q-obstruction 不含 K4 block；不需 T4。
- §4 結合外部 degree-choosability 定理及既有全部 block 分類，得到接受 T4
  的全 degree-4 disk minimal obstruction 只缺 q；無內點數上限，尚未 Lean 化。
- 256 個 unrooted、64 個 rooted 配置；289 個正常形與 10 個具名分枝控制，
  均保存刪邊 coloring 及兩層 minor 證書。最後 K5 收縮只用來排除 planarity，
  不宣稱是 boundary 固定操作或保持完整 Σ。

### R10：唯一 degree-5 內點與 degree-4 分量的接點介面

- **狀態：2026-09-18 完整染色介面及 minimality 等價式已完成；disk／T4 排除未完成。**
- [新報告](c5_degree5_interfaces.md) 保留全部有序端點 tuples／共同色框，
  F_C(b) 與 A_z(b) 給出每列精確延拓式；tight degree lists 提供 block palette 證書。
- 刪分量任一 incident edge 即對所有 b 解除該分量限制。minimality 等價於
  q 下禁色不可刪減地覆蓋 A_z；至少一個多接點分量，剩十三個必要接點分拆。
  固定來源圖全部刪邊後代至多四個二元開關，不是跨圖充分 state 或小 disk 代表。
- 32 個既有 degree-5 disk witnesses、7,680 個完整 boundary rows 通過核對；
  16 個 T4 單缺失，另 16 個雙缺失都拒絕某個 T4。全部 witnesses 皆有 marginal 失敗。
- 下一題取三條 z-boundary spokes、單一二接點 Gallai 分量：F_C(q)={D} 能否
  與相鄰三色雙缺失／全部 T4 在同一 C5 disk 共存。暫不增加 k 或外枝 catalog。

### R11：三-spoke／二接點分量的 disk 區域

- **狀態：2026-09-18 區域化約完成，最後的 pentagon 四色延拓問題仍開放。**
- [新報告](c5_degree5_sectors.md)：連通分量只佔一區；十二種位置中，禁色交換
  排除八種、T4 改色排除兩種，只剩兩個互為鏡像的長區域，沒有內點數上限。
- 移動 boundary 得到 K=(z,b1,b2,b3,b4)，指定拒絕列為 (D,B,A,B,C)。
  proper S_K 的接合代數仍容許雙缺失；minimality 還需要 z=B、C 的域外列。
- 具名 disk 控制具有 degree 序列 (5,4,4)、相鄰雙缺失及全部 T4，但其
  F_C(q)={C,D}，z 的 C-spoke 可刪，所以不是目標反例。
- 下一題保留 F_C(q)={D} 研究此 pentagon 的 block palettes／刪-spoke 延拓；
  不重跑 catalog，也不把前輪全 degree-4 三色定理套到此四色拒絕列。

### R12：三-spoke 任意樹與 degree-4 分量的 K4

- **狀態：2026-09-18 任意樹排除及 t≥1 的 K4 排除完成，紙面＋有限證書。**
- [新報告](c5_degree5_tree_components.md)：消去兩接點主路徑外的任意 forcing
  分枝，保持固定 q 的全部 z 色查詢；F={D} 等價於至少三色的 D 閉序列。
- 刪除閉子序列得到五種形狀（包含必要的五步 lollipop），其 648 個 lifts
  全非 disk。任意樹的無界覆蓋由紙面化約承擔，不是有界搜尋外推。
- t≥1 時 B∪{z} 連通，degree-4 分量 K4 的四條外接路徑產生 K5 minor；
  此步不需 T4。t=0 不由這個引理排除。
- 此輪提出的單 triangle 問題已由 R13 完成，單長奇環再由 R14 處理。
  同一 block 多接點仍須共同接合，不能分拆為獨立 marginals。

### R13：三-spoke 單 triangle 二接點

- **狀態：2026-09-18 紙面化約及有限證書完成。**
- [新報告](c5_degree5_triangle_components.md) 依接點位置分三型，保留完整
  fixed-q 禁色、真實 attachments 及 boundary 固定 minors；全部必要 lifts 非 disk。
- 此輪提出的單長 odd-cycle 已由 R14 處理；一般多環、degree-5 與主命題仍未證。

### R14：三-spoke 單長奇環二接點

- **狀態：2026-09-18 紙面化約及有限 minor 控制完成。**
- [新報告](c5_degree5_odd_cycle_components.md)：拒絕 D 強迫共同二色 palette，
  共同接點保留 root 色集，不同接點保留全部四個 z 色查詢；旁支型回到樹。
- 任意單 odd-cycle 加 bridges 已排除；明列不保持完整二元關係的反向控制，
  不宣稱完整 Σ／T4 保持，沒有新 Lean theorem。
- 下一題為恰兩個 triangle blocks，分共用點與 bridge 路徑連接，保留兩個
  z 接點的實際位置及共同色框；不直接逐環套用本輪結果或擴大 catalog。

### R15：三-spoke 共用點雙 triangle 二接點

- **狀態：2026-09-18 共用 cut vertex 分支完成，紙面＋有限證書。**
- [新報告](c5_degree5_shared_triangles.md)：互補 palettes 共同接合，按接點位置
  化成兩條簡單色序列或帶標記閉序列，旁支則化回樹。888 個必要模板、
  295,920 個實際接線全非 disk；固定 q 全部 z 色及 minimality 保持。
- 下一題是兩個互斥 triangles 的 bridge 路徑，先分析接點跨切口的共同
  z 色依賴；不直接套全 degree-4 整圖的 bridge 縮短。
- 沒有完成整個雙 triangle 分支、一般多環或 degree-5 定理，未新增 Lean theorem。

## 5. 前輪文件整理與驗證紀錄（基準 fb6216e）

- 原 `HANDOFF.md` 全文移存歷史，新的交接集中於當前結果與停止點。
- 建立本頁全索引與 R1–R6 追蹤；README 改成分層入口；近期報告補上後續狀態，
  enumerator 獨立重現章節改為 §16。

| 本輪核對 | 結果 |
| --- | --- |
| 文件索引與歷史保存 | 67 份專題報告全部有入口；歷史正文與整理前 `HEAD:docs/HANDOFF.md` 完全相同；現況交接縮為 106 行 |
| README／docs 本地連結 | 601 個本地檔案連結均存在，16 個章節片段均有對應標題；新舊文件 whitespace 核對通過 |
| `uv run --with networkx==3.5 python scripts/c5_shared_pair_bridge.py --check` | 逐 byte 重播通過：864 個 root 配置、12 個 singleton、64 個 bridge 控制、3 個 D 模板對應；包含來源及依賴證書 hashes 比對 |
| `lake build` | 通過，8,821 jobs；只有既有 `AttachmentOrder`／`SymRelabel` lint 警告 |
| `lake env lean Math/ForcingListsAudit.lean` | 20 個具名定理均只依賴 `propext`、`Classical.choice`、`Quot.sound`，沒有 `sorryAx` 或 native 計算公理 |
| `git diff --check`／變更範圍 | 通過；變更限 README 與 docs，程式、Lean 原始碼和 artifacts 未改 |

本輪只重播上述最新介面 checker，未重播五份依賴的完整拓撲枚舉、k≤3 全量
deletion audit 或 k=6／7 搜尋。那些結果引用原報告及其既有驗證紀錄。

文件整理與上述驗證已完成，隨本次提交發布；未啟動後續研究或大範圍枚舉。

## 6. 本輪接手研究與驗證紀錄（基準 76e6f44）

本輪選擇 R2，推導 palette 規則後接上 R3 的兩-spoke minor，並確認 R1。
新報告、script、artifact 已整合至 README／HANDOFF；既有證書與 Lean 原始碼未改。

| 本輪核對 | 結果 |
| --- | --- |
| 新 `c5_triangle_tree_palettes.py --check` | 逐 byte 重播通過：49 個 apex 輸入、343 個根 triangle 輸入、48 個替換輸入、48 個結構控制及 63 次子樹吸收；核對來源／目標 criticality、boundary 固定的 minor branch sets、既有模板同構與 subdivisions |
| 六份依賴 checker | bridge pruning、兩環、共用點三環、互斥多環、四環鏈及四環 star 均通過；重播既有拓撲證書，沒有新 planarity search |
| `lake build` | 通過，8,821 jobs；只有既有 `AttachmentOrder`／`SymRelabel` lint 警告 |
| `lake env lean Math/ForcingListsAudit.lean` | 既有 20 個定理均只依賴 `propext`、`Classical.choice`、`Quot.sound`；本輪未新增 Lean 定理 |
| 文件與變更範圍 | 611 個本地連結存在、68 份專題報告全部有索引；新檔 whitespace 與 `git diff --check` 通過；既有 scripts／artifacts、Lean 原始碼與歷史交接未改 |

無界結論依賴新紙面歸納／minor 及既有小型 topology 證書，不能把結構控制
視為一般定理的計算證明。本輪產物隨本次 commit 保存，未 push；停止在 R7，未啟動大枚舉。

## 7. 長 odd-cycle 研究與驗證紀錄（基準 7fdc19e）

完成 R7，新報告、script、artifact 已整合至 README／HANDOFF。
既有 scripts／artifacts、Lean 原始碼與歷史交接未改；沒有新 planarity search。

| 本輪核對 | 結果 |
| --- | --- |
| 新 `c5_odd_cycle_roots.py --check` | 逐 byte 重播通過；C3／C5／C7 共 120,099 個 rooted 輸入、16,807 個 unrooted C5 輸入、30 個具名 shortening 控制；核對 root、criticality、branch sets、目標同構及既有 pruning／subdivisions |
| triangle-tree checker | 49 個 apex、343 個根 triangle、48 個替換輸入、48 個結構控制與 63 次 pruning 重播通過 |
| pentagon checker | 67,648 個既有 lifts、56 份 subdivisions 全量重播通過 |
| `lake build` | 通過，8,821 jobs；僅既有 `AttachmentOrder`／`SymRelabel` lint 警告。本輪無 Lean 修改，未重跑公理審計 |
| 文件與 whitespace | 623 個 README／docs 本地檔案連結存在、69 份專題報告有索引；新檔 whitespace 與 `git diff --check` 通過 |

沒有重跑更早六份 triangle 依賴的全量枚舉，也沒有擴大 disk catalog。
新結果是紙面論證與有限證書；主命題仍未證。研究未 commit／push，停止在 R8。

## 8. 多長 odd-cycle 研究與驗證紀錄（基準 7fdc19e，接續未提交成果）

完成 R8，並以明確歸納及終止論證推廣到任意有限長環數。新增報告、script、
artifact，更新 README／HANDOFF 與前報告後續入口；前輪程式／證書原封保留。

| 本輪核對 | 結果 |
| --- | --- |
| 新 `c5_multi_odd_cycles.py --check` | 逐 byte 重播通過：14,762 個 rooted 輸入、121 對介面接合、2 個三色遞迴控制、60 個結構控制及 138 次縮減；各中間圖核對 degree／criticality／root 訊息，branch sets 合成回來源並接既有小模板 subdivisions |
| 三份直接依賴 checker | odd-cycle root、triangle-tree、pentagon 均通過；單環 67,648 lifts／56 subdivisions 沿用既有證書全量重播，無新 planarity search |
| `lake build` | 通過，8,821 jobs；只有既有 `AttachmentOrder`／`SymRelabel` lint；本輪無 Lean 修改，未重跑公理審計 |
| 文件與 whitespace | 636 個 README／docs 本地檔案連結存在、70 份專題報告有索引；新檔 whitespace 及 `git diff --check` 通過 |

沒有擴大 disk catalog 或重播更早六份 triangle 依賴的全量枚舉。任意長度／
環數的覆蓋屬紙面證明，固定 q minor 不聲稱完整 Σ 保持。兩輪研究的程式、
證書、報告與交接隨本次提交一併發布；停止在 R9 的 K4／bridge 介面，主命題仍未證。

## 9. K4 排除與 degree-4 合成（基準 dad5940）

完成 R9：獨立紙面 K5 minor 排除任意外側的 K4 block，核對 residual lists，
並接上既有定理得到接受 T4 的全 degree-4 disk minimal obstruction 只缺 q。
新增 script／artifact／報告，更新 README、HANDOFF、本頁與多長環後續入口。
既有 scripts／artifacts、Lean 原始碼與歷史交接保持原樣；成果與 §10 一併提交發布。

| 本輪核對 | 結果 |
| --- | --- |
| 新 `c5_k4_blocks.py --check` | 逐 byte 重播：256 個 unrooted、64 個 rooted 配置；289 個正常形、10 個具名分枝；299 張圖均核對 degree、q 拒絕、每條非 boundary 邊的刪邊 coloring、bridge 雙側 singleton、boundary 固定 minor 及來源圖上的 K5 minor |
| 多長環 checker | 14,762 個 rooted 輸入、121 對接合、2 個三色控制、60 個結構控制／138 次縮減重播通過 |
| 樹核心 checker | Y／palette 既有拓撲證書與長路徑控制全量重播通過；未擴大模板域 |
| Triangle fork checker | 90,112 個 lifts、88 份 subdivisions 全量重播通過 |
| 兩 triangle checker | 既有六類模板、649 份 subdivisions 重播通過 |
| `lake build` | 通過，8,821 jobs；只有既有 `AttachmentOrder`／`SymRelabel` lint；本輪未改 Lean，未重跑公理審計 |
| 文件與 whitespace | README／docs 共 652 個本地檔案連結、71 份專題索引及新檔 whitespace 已核對；`git diff --check` 通過 |

已查核外部 degree-choosability 定理的原論文摘要；合成的外部定理依賴在新報告
§4 明列。沒有重播所有傳遞依賴 checker、k≤3 deletion audit 或 k=6／7 搜尋，
沒有新 planarity search。全 degree-4 結論是紙面合成，不是有限計算外推或 Lean
定理；`K∞=K≤5` 仍未證。停止在 R10 的介面推導，未啟動 degree-5 搜尋。

## 10. 唯一 degree-5 接點介面（接續未提交 R9）

從 HEAD `dad5940` 與 R9 未提交產物接手，完成 R10 的染色介面部分。
新報告給出所有接點共同關係、tight-list／block palettes、分量刪邊解除、
minimality 的不可刪減覆蓋充要條件，以及固定來源圖全部刪邊後代至多四開關。
一般 disk／T4 排除未完成，沒有新增 Lean theorem。

| 本輪核對 | 結果 |
| --- | --- |
| 新 `c5_degree5_interfaces.py --check` | 逐 byte 重播通過；108 個局部介面控制，以 factor elimination／完整 tuples 交叉核對，並核對 block-palette 禁色證書 |
| 既有 disk witnesses | 從舊 cyclic probe 選出全部 32 個唯一 degree-5 witnesses，核對 input／source SHA256 及封存 apex rotation；沒有重跑圖生成器 |
| 完整關係／共同色框 | 7,680 個 proper boundary rows、30,720 個固定 z 色查詢均與直接著色相符；十個 canonical rows 另保存完整接點 tuples、內點 witnesses 與禁色 palettes |
| Minimality／刪邊公式 | 19,200 個 canonical boundary／刪邊／z 色查詢及分量解除核對通過；384 個全部開關配置、3,840 個 canonical rows 重建相符；保存全部 q 刪邊 coloring |
| T4 與投影控制 | 16 個 T4 單缺失、16 個拒絕某 T4 的雙缺失；全 32 個皆有端點一維 marginals 誤允許 z 色的 witness |
| `lake build` | 通過，8,821 jobs；僅既有 `AttachmentOrder`／`SymRelabel` lint。本輪未修改 Lean，未重跑公理審計 |
| 文件與 whitespace | README／docs 的 665 個本地檔案連結、72 份專題索引、新檔 whitespace 及 `git diff --check` 通過 |

已核對外部 blockwise-uniform characterization 的 Theorem 10 及 slack Lemma 7，
來源與信任範圍見新報告 §2。無界覆蓋／解除結論由紙面證明承擔，有限控制
不窮盡十三個接點分拆。既有 scripts／artifacts 與歷史交接未改，前輪未提交
產物完整保留；本輪只為前報告補後續連結，沒有重播舊全量 checker 或新 planarity search。

停止在三條 z-boundary spokes 與單一二接點 Gallai 分量：F_C(q)={D} 是否能
同時有相鄰三色雙缺失及全部 T4 的共同 disk 實現性。兩輪 scripts、artifacts、
報告及入口文件隨本次提交一併發布；研究停止點與信任範圍不變。

## 11. 三-spoke 區域化約（基準 be97121）

從乾淨工作樹接手，選 R10 的三-spoke／單一二接點分支，完成 R11 區域化約。
新增報告、script、artifact，更新 README／HANDOFF／本頁與前報告後續入口。
沒有修改既有 scripts／artifacts、Lean 原始碼或歷史交接，未 commit／push。

| 本輪核對 | 結果 |
| --- | --- |
| 新 `c5_degree5_sectors.py --check` | 逐 byte 重播通過；十二個 spoke／區域位置，八個缺色交換排除、兩個 T4 改色排除、兩個鏡像保留型 |
| 五邊形接合 | 全部 1,024 個抽象 proper-C5 relations、245,760 個完整 boundary rows；T4 加拒絕 q 留下 24 個抽象輸入／12 個輸出，未視為 disk 分類 |
| 具名非 minimal 控制 | 沿用一個舊 catalogue witness；新圖完整 240 rows、十列共同端點 tuples、全部非 boundary 刪邊及一份 apex rotation 通過；只有 z 的 C-spoke 刪後仍拒絕 q |
| 前輪完整介面 checker | 108 個代數控制、32 個既有 disk witnesses、7,680 個完整 rows、30,720 個固定 z 查詢及 384 個刪邊開關配置重播通過 |
| `lake build` | 通過，8,821 jobs；只有既有 `AttachmentOrder`／`SymRelabel` lint。本輪沒有 Lean 修改，未重跑公理審計 |
| 文件與 whitespace | README／docs 的 677 個本地檔案連結、73 份專題索引及新檔 whitespace 核對通過；`git diff --check` 通過 |

一般區域限制是紙面平面分離與禁色對稱論證；有限計算未取代任意大小的
證明。只為一個明列控制使用 planarity，沒有重新生成 catalogue 或擴大 k。
停止在單一 pentagon 四色列的 block palettes／刪-spoke 延拓條件；分拆 (2)
最後排除、一般 degree-5 與主命題仍未證。

## 12. 三-spoke 任意樹排除（接續未提交區域成果）

HEAD 仍為 `be97121`；前輪三-spoke 區域 script／artifact 原封保留。
完成 R12，新增任意樹排除與連通外框 K4 引理的報告、script、artifact，更新
README／HANDOFF／本頁及前報告後續入口。兩輪成果均未 commit／push。

| 本輪核對 | 結果 |
| --- | --- |
| 新 checker `--check` | 逐 byte 重播通過；9,330 組二色 lists 以完整 tuples／集合傳遞／被迫序列交叉核對；22,128 條至少三色的 D 閉序列縮至五型 |
| 五型全部接線 | 30 種 palette 序列、648 個 lifts，全部核對 degree、F={D} 及逐非 boundary 刪邊 coloring；31 份 K5／K3,3 subdivisions，重播不呼叫 planarity |
| 長正常形 | 30 個具名來源、60 次縮減，逐步及合成 boundary 固定 minors；最終非平面 minor 合成回各來源的 apex 圖 |
| 原始樹分枝 | 10 個具名控制含非 D 尾枝、長 D 分枝及 D 分叉，核對完整 root 色集、固定-q 禁色保持及來源上的 topology minor；包含接點不是原樹葉端的例子 |
| K4 外框控制 | 一張含兩個 z 接點及兩個 D forcers 的 K4 圖，核對 F={D}、逐邊 criticality 及來源圖上的直接 K5 minor |
| 前輪區域 checker | 十二個區域位置、1,024 個抽象 relations／245,760 個完整 rows、具名非 minimal disk 控制重播通過；前輪 artifact 未改 |
| `lake build` | 通過，8,821 jobs；只有既有 `AttachmentOrder`／`SymRelabel` lint。本輪未改 Lean，未重跑公理審計 |
| 文件與 whitespace | README／docs 的 691 個本地檔案連結、74 份專題索引及新檔 whitespace 核對通過；`git diff --check` 通過 |

無界結論分別由分枝 forcing、閉色序列分類與真正 minor 構造承擔；有限
模板非 disk 仍含 Python／subdivision checker／apex-disk 紙面等價的信任。
沒有擴大 graph catalog，沒有新增 Lean theorem。樹分支已完成；下一題是
C 恰含一個 triangle block 的二接點介面，含 cycle 的一般分拆 (2) 與主命題仍未證。

## 13. 三-spoke 單 triangle 二接點排除

HEAD 仍為 `be97121`，接續前兩輪未提交成果；前輪 scripts／artifacts 原封保留。
完成 R13：旁支 triangle 化回樹，共同接點化為帶標記五型，不同接點兩臂
各化為簡單色序列。不限制接點位置、路徑長度或外枝分叉，未新增 Lean theorem。

| 本輪核對 | 結果 |
| --- | --- |
| 新 checker `--check` | 528 個必要 palette 模板、89,224 個實際接線及 143 份 K5／K3,3 subdivisions 逐 byte 重播；不呼叫 planarity |
| 共同色框／minimality | 每模板代表直接核對四個 z 色與全部 q 刪邊 coloring；其餘接線逐張核對 degree、內部邊及 boundary 色多重集，按 attachment role 搬運 fixed-q 染色問題 |
| 路徑代數 | 1,555 組 pairs 的完整 tuples／集合傳遞交叉核對，另檢查指定 singleton 反向唯一性；無界覆蓋為紙面歸納 |
| 長／旁支控制 | 24 個不同接點來源、48 次縮減；10 個共同接點來源、20 次縮減，4 個保留 triangle、6 個轉樹；5 個旁支 triangle 控制。逐步及合成 boundary 固定 minors、來源非平面證書通過 |
| 直接依賴 | 任意樹及區域 checker 均重播通過；沒有重跑舊全量 catalogue／deletion audit |
| `lake build` | 通過，8,821 jobs；只有既有 AttachmentOrder／SymRelabel lint，沒有 Lean 修改或新公理審計 |
| 文件與 whitespace | README／HANDOFF／STATUS 及前報告後續入口已整合；703 個本地檔案連結、新檔 whitespace 及 `git diff --check` 通過 |

化約後模板的非 disk 證書不取代無界覆蓋證明，也不保持完整 Σ／T4；T4
僅用於原圖的區域定位。停止在恰一個長 odd-cycle；一般多環分拆 (2)、其他
接點分拆、degree-5 單缺失與主命題仍未證。三輪成果均未 commit／push。

## 14. 三-spoke 單長奇環二接點排除

HEAD 仍為 `be97121`，接續前三輪未提交成果，完成 R14。新報告按旁支、
共同接點、不同接點三型，給出任意長奇環縮為 triangle／樹的真正 minor。
全部固定-q z 色查詢、degrees 及 minimality 保持；原始 T4 只用於區域定位。
不保持任意二元接點關係，明列具體反向控制，沒有新增 Lean theorem。

| 本輪核對 | 結果 |
| --- | --- |
| 新 `c5_degree5_odd_cycle_components.py --check` | 證書逐 byte 重播通過；保存程式、依賴及 triangle／樹輸入證書 SHA256 |
| Cycle list 判準 | 23,748 組：C3／C4 所有至少二色 lists、C5 所有二色 lists；路徑動態規劃與完整 tuples 交叉核對 |
| 接點介面 | 12,000 個不同接點訊息查詢、600 個共同接點查詢，四種環長；完整 z 查詢保持，另保存二元關係不保持的 (2,2) 控制 |
| 真實來源圖 | 不同接點 72、共同接點 60、旁支 15，共 147 張；環長 5／7／9，含不同 arc 奇偶與零長臂。逐張核對 degrees、四個 z 色、所有非 boundary 刪邊 coloring、boundary 固定 minor |
| 非平面證書 | 全部來源的 apex 圖各有直接核對的 K5／K3,3 minor，由前輪證書合成；不呼叫 planarity，也沒有新拓撲搜尋 |
| 前輪 triangle checker | 528 模板、89,224 接線、143 份 subdivisions 及既有長／旁支控制完整重播通過 |
| 前輪樹 checker | 9,330 組 lists、22,128 條閉序列、648 lifts、31 份 subdivisions 及長／外枝／K4 控制完整重播通過 |
| `lake build` | 通過，8,821 jobs；僅既有 AttachmentOrder／SymRelabel lint，未改 Lean 或重跑公理審計 |
| 文件與 whitespace | README／docs 共 718 個本地檔案連結、76 份專題索引、新檔 whitespace 及 `git diff --check` 通過 |

README／HANDOFF／本頁及單 triangle 報告後續入口已整合。無界覆蓋由紙面
list 判準、接合分析與 minor 構造承擔，有限控制不外推一般 degree-5 定理。
前三輪 scripts／artifacts 原封保留；未重跑舊全量 catalogue／deletion audit。
停止在恰兩個 triangle blocks，其餘為 bridges；至少兩環的一般分拆 (2)、
其餘接點分拆與主命題仍未證。四輪研究成果未 commit／push。

## 15. 三-spoke 共用點雙 triangle 排除

HEAD 仍為 `be97121`，接續前四輪未提交成果，完成 R15 的共用 cut vertex
分支。先分類兩接點到 cluster 的位置，再用互補 palettes 的共同 root
接合、兩條簡單色序列或帶標記閉序列給出任意臂長／外枝的紙面覆蓋。
不同位置的完整 fixed-q F、degrees 及 minimality 保持，沒有新增 Lean theorem。

| 本輪核對 | 結果 |
| --- | --- |
| 新 `c5_degree5_shared_triangles.py --check` | 證書逐 byte 重播通過，保存程式／依賴與 triangle／樹輸入證書 SHA256 |
| Root 接合代數 | 121 個至少二色 lists 的 triangle root 查詢、14,641 個五點共同 root 查詢；獨立完整色 tuples 核對互補 palette 判準 |
| 必要正常形與 topology | 同環不同點 408 型／158,496 lifts，分處兩環 360 型／126,096 lifts，同點會合 120 型／11,328 lifts；合計 888 型／295,920 lifts，全部非 disk，199 份 subdivisions，重播不呼叫 planarity |
| 固定 q 與 minimality | 每模板代表直接核對四個 z 色與全部非 boundary 刪邊 coloring；其他接線逐張核對完整 degrees、內部邊、boundary 色多重集，依 attachment role 搬運 fixed-q 問題 |
| 長來源與真正 minors | 同環 24、分處兩環 24、標記型 10，共 58 張長來源／116 次縮減；標記型 4 張保留 cluster、6 張化回樹。逐步及合成 boundary 固定 minors、全部來源的非平面 minor 通過 |
| 旁支與反向控制 | 5 張整個雙 triangle cluster 位於單 bridge 旁支的來源化回樹，核對 forcer、criticality 與來源 topology；另保存二色閉序列 F={A,D} 的非 minimal 控制 |
| 接手及直接依賴 | 單長奇環、單 triangle、任意樹三份 checker 本輪重播通過；前四輪 scripts／artifacts 原封保留，未重跑舊全量 catalogue／deletion audit |
| `lake build` | 通過，8,821 jobs；僅既有 AttachmentOrder／SymRelabel lint；未改 Lean 或重跑公理審計 |
| 文件與 whitespace | README／docs 的 734 個本地檔案連結、77 份專題索引、新 script／報告 whitespace 及 `git diff --check` 通過 |

README／HANDOFF／本頁與前輪報告的後續入口已整合。無界結論來自紙面
位置覆蓋、訊息判準及 minor 構造；有限接線證書不外推一般 degree-5。
下一題收窄為兩個互斥 triangles 的 bridge 路徑；兩環恰含長環、更多環、
其他接點分拆及主命題仍未解。本輪與前四輪共五輪成果未 commit／push。

## 16. R11–R15 成果整理與發布前核對

2026-09-18，依使用者要求整理並 commit／push。基準為 `be97121`，本次一併
納入五份新 scripts、五份 observations 證書、五份專題報告及入口文件。
README 改為五輪成果表；HANDOFF 保留精確前提、停止點與六份 checker 的
完整重播入口；各報告補上發布註記，原輪次的未知與未提交狀態保留為歷史。

| 本次實際核對 | 結果 |
| --- | --- |
| 區域 `c5_degree5_sectors.py --check` | 通過；12 個區域、1,024 個抽象 relations、245,760 rows 及非 minimal disk 控制 |
| 樹 `c5_degree5_tree_components.py --check` | 通過；9,330 組 lists、22,128 條閉序列、648 lifts、31 份 subdivisions 及來源 minors |
| 單 triangle `c5_degree5_triangle_components.py --check` | 通過；528 模板、89,224 lifts、143 份 subdivisions 及長／旁支控制 |
| 單長奇環 `c5_degree5_odd_cycle_components.py --check` | 通過；23,748 組 cycle lists、12,600 個接點訊息查詢、147 張來源控制 |
| 共用點雙 triangle `c5_degree5_shared_triangles.py --check` | 通過；888 模板、295,920 lifts、199 份 subdivisions、58 張長來源／116 次縮減及 5 張旁支來源 |
| 既有完整介面 `c5_degree5_interfaces.py --check` | 通過；108 個局部控制、32 個 disk witnesses、7,680 個完整 rows、30,720 個固定 z 查詢及 384 個刪邊開關配置 |
| `lake build` | 通過，8,821 jobs；僅既有 AttachmentOrder／SymRelabel lint，未修改 Lean 或重跑公理審計 |

本次整理未修改研究 scripts 或 observations，六份 checker 均以 `--check`
逐 byte 比對保存證書，沒有擴大 catalogue 或重新生成證書。
提交前另核對 README／docs 的 747 個本地檔案連結、77 份專題索引與 staged whitespace。

停止點仍是三-spoke 型中兩個頂點互斥 triangles 的 bridge 路徑；兩環含長環、
更多環、其他接點分拆及一般 degree-5 結論仍未解。紙面無界化約、Python
有限證書與 Lean 形式化分開；本次沒有新增數學結論或 Lean theorem。

## 17. R16 互斥雙 triangles 的 bridge 切口與直接私有接點

2026-09-18，從乾淨 HEAD `b55abf4` 接手。選定交接指定的互斥雙 triangle
問題，完成其中直接私有接點子型，未完成全部接點位置。另由既有不含接點
旁支消去引理，排除任一兩環間 bridge 讓兩個 z 接點留在同側的來源。

| 本輪核對 | 結果 |
| --- | --- |
| 新 bridge checker（`--check` 逐 byte 重播通過） | 132 個必要模板、43,696 個實際接線全部非 disk；29 份保存 subdivisions，重播不呼叫 planarity |
| 局部接合 | 256 組端點色集（含空集合）、24 個 triangle root 查詢；保存忘記共同 z 色會漏掉 D 的控制 |
| 長路徑來源 | 18 張，九組有序 palettes 的端點／內部閉段；來源／目標 degrees、四種 z 色、逐邊刪除 coloring、真正 boundary 固定 minor 及來源非平面 minor 通過 |
| 文件與 whitespace | 756 個本地檔案連結、新檔 whitespace 及 `git diff --check` 通過 |
| 接手 checker | 單長奇環 23,748 組 lists、12,600 個訊息查詢、147 張來源通過；沒有重跑既有全量 catalog |
| `lake build` | 通過，8,821 jobs；僅既有 AttachmentOrder／SymRelabel lint；未修改 Lean |

bridge 色序列刪除重複色後至多四條邊；每步保留完整 F={D} 及 minimality。
無界覆蓋是紙面論證，有限拓撲及來源控制為 Python 證書，沒有新增 Lean theorem。
報告／README／HANDOFF 已整合。下一步為兩側外臂及同一環點接入；互斥雙環
全部位置、一般 degree-5 及主命題仍未解。本輪未 commit／push。

## 18. R17 互斥雙 triangles 不同環點接入的任意外臂

2026-09-18，接續未提交 R16，HEAD 仍為 `b55abf4`。兩側外臂各在不同於
bridge 端點的環點接入時，任意長臂／中間路徑及不含接點外枝皆排除。
指定 singleton 的唯一反向輸入給出四列 triangle root 訊息，據此建立
三條路徑的獨立縮減；S／T 允許含 D，不能直接搬用 R16 的 palette 限制。

| 本輪核對 | 結果 |
| --- | --- |
| 必要正常形 | 36,672 型；兩臂各至多三內點，中間至多四條 bridge |
| 全部接線選擇 | 246,645,568 種，全非 disk；以 709 份 subdivisions、36,732 次子 cube 引用完整覆蓋，沒有逐張展開或抽樣 |
| 局部代數 | 1,128 個完整 tuples root 查詢；6,561 組 Boolean cube 差集與完整 truth table 交叉核對 |
| 長來源及 minors | 72 張／216 次縮減；每步 degrees、全部固定-q z 色、逐邊刪除 coloring、boundary 固定 minors 及合成回來源的非平面 minor 通過 |
| 新 checker 重播 | `--check` 逐 byte 比對通過；保存 subdivisions 的接線覆蓋全部重建，未呼叫 planarity |
| R16 checker | 132 模板／43,696 lifts／29 subdivisions／18 張長來源重播通過；既有研究 scripts／artifacts 未修改 |
| `lake build` | 通過，8,821 jobs；僅既有 AttachmentOrder／SymRelabel lint；沒有新增 Lean theorem |
| 文件與 whitespace | 765 個本地檔案連結、新檔 whitespace 及 `git diff --check` 通過 |

新 checker 對每模板核對 F={D}、接線 degree 及拓撲覆蓋；模板一般
minimality 使用紙面分量解除引理，有限長來源另有直接 coloring 控制。
任意長度覆蓋由紙面證明承擔，不以有限證書冒充一般 Lean theorem。

下一題是至少一側外臂在該環 bridge 端點接入，先以標記二色 list 處理；
所有互斥雙環、一般 degree-5 及主命題仍未解。報告／README／HANDOFF
已整合。本輪與 R16 未 commit／push。

## 19. R18 同點接入的標記二色介面與候選正常形

2026-09-18，接手 HEAD `b55abf4` 及未提交 R16／R17。依交接選定至少一側
外臂在該環 bridge 端點接入的缺口，完成 root 介面及標記正常形語意。
本輪**尚未完成同點接入的 disk 排除**；報告見
[標記二色介面](c5_degree5_bridge_marks.md)。

| 本輪實際核對 | 結果 |
| --- | --- |
| 同點 root | 36 組有序二色 lists 完整 tuples；相同 pair 給互補二色 root，不同 pairs 給四色 root |
| 候選正常形 | 一側同點 858 型、兩側同點 186 型；每型一張具體 arc 接線代表 |
| 直接 coloring | 全部 1,044 張代表核對 degrees、兩個互斥 triangles、四種 z 色及全部非 boundary 刪邊 coloring；證書保存圖與著色 witnesses |
| 色序列縮減 | 至多六步全部色序列及標記位置，共 6,015 個開序列、3,426 個閉序列、12,711 次縮減；核對保留 lists、指定 singleton 反向唯一性或完整 F={D} |
| 退化控制 | D,A,D,B,D 縮成 D,B,D 會從單禁色變為雙禁色，已保存 |
| 新 checker | `c5_degree5_bridge_marks.py --check` 逐 byte 重播通過；保存程式／依賴 SHA256；不呼叫 planarity |
| 接手重播 | R16 `c5_degree5_bridge_triangles.py --check` 通過：132 型、43,696 lifts、29 subdivisions、18 長來源；未重跑 R17 大覆蓋 |
| `lake build` | 通過，8,821 jobs；僅既有 AttachmentOrder／SymRelabel lint；未新增 Lean theorem |
| 文件核對 | 四份本輪入口／報告的 207 個本地檔案連結、新程式／報告 whitespace 及 `git diff --check` 通過 |

README／HANDOFF 已更新。本輪只建立 fixed-q 介面及候選正常形語意，沒有
把色序列縮減冒充 boundary 固定 source minor，也沒有把代表的 minimality
冒充 disk realizability。下一步用已保存的 1,044 型落實長來源 branch sets，
再做全部 B-spoke 選項的拓撲 cube 覆蓋。一般互斥雙環、degree-5 排除及
主命題仍未證；R16／R17 scripts／artifacts 保留原狀，本輪未 commit／push。

## 20. R19 標記路徑來源 minors 與同點接入排除

2026-09-18，接手 HEAD `b55abf4` 及未提交 R16–R18，選定 R18 明列的
來源 minor／完整接線拓撲缺口，完成 [同點接入排除](c5_degree5_bridge_mark_minors.md)。
結合 R15–R17，唯一 degree-5、三-spoke、連通二接點分量恰含兩個 triangle
blocks 其餘 bridges 時，接受 T4 的 disk minimal q-obstruction 不存在；
包含共用點與互斥兩型，不限制臂長及外枝分叉。沒有新增 Lean theorem。

| 本輪核對 | 結果 |
| --- | --- |
| 接手 R18 `--check` | 858＋186 型、36 組 root 查詢、12,711 次色序列縮減逐 byte 重播通過 |
| Git 收尾 | HEAD、origin/main 與 `git ls-remote` 的遠端 main 同為 `b55abf416be524b20f096a6be99b2233266ddcd0`；R16–R19 保留未提交 |
| 全部接線拓撲 | 單標記 533,728、雙標記 37,672，共 571,400 種；130 份 subdivisions、1,069 次子 cube 引用，全部餘集為空 |
| 正常形語意 | 重算全部 1,044 張代表的四種 z 色及逐邊刪除 coloring，與 R18 原證書一致；核對 degrees 與真正兩個互斥 triangles |
| 長來源與真正 minors | 198 張／432 次縮減；來源及每步目標 degrees、四種 z 色、全部刪邊 coloring 通過；保存逐步／合成 boundary 固定 branch sets 及合成回來源的非平面 minor |
| 標記邊界控制 | 單標記最終剩 0／1：30／18 張；雙標記剩 0／1／2：60／30／60 張；含相鄰標記、30 步同時刪兩標記、六張整條臂收進 z |
| 新 checker 唯讀重播 | `--check` 逐 byte 通過；停用 planarity oracle 後仍通過；重播前後三份輸入與輸出證書 SHA256 完全相同 |
| 覆蓋算法 | 沿用 R17 cube 差集，重跑 6,561 組獨立 truth-table 核對；未重跑 R17 的 36,672 型大覆蓋 |
| `lake build` | 通過，8,821 jobs；僅既有 AttachmentOrder／SymRelabel lint；未改 Lean 或重跑公理審計 |
| 文件與 whitespace | README／HANDOFF／STATUS 及 R17／R18 後續入口已整合；本地文件連結、新檔 whitespace 及 `git diff --check` 通過 |

無界來源覆蓋依賴紙面標記步驟歸納、真正 minor 構造及既有分量解除引理；
有限 topology／coloring 證書不取代一般證明或 Lean 形式化，不保持完整 Σ。
R16–R18 scripts／artifacts 原封保留。本輪亦未 commit／push。

下一題收窄為一個長奇環與一個 triangle 的互斥雙 block 分量：先核對
全部 z 色的條件 root 介面，再決定能否保留接點縮成 triangle。
兩長環、共用點長環、更多環、其他 degree-5 分拆、單側／共同出口與
`K∞=K≤5` 仍開放。精確入口與反向控制要求見 HANDOFF §2。

## 21. R20 長奇環加 triangle 的完整條件 root 介面

2026-09-18，接手 HEAD `b55abf4` 及未提交 R16–R19，完成交接指定的
[混合雙環 root 介面](c5_degree5_long_triangle_roots.md)。拒絕 D 強迫長環
私有 lists 具有共同二色 palette；不同接點的四列為 singleton／三色 list，
同點為互補 pair 減外臂 singleton 禁色。兩者皆與保留接點的 triangle 相同。
任意環長的證明在紙面層，尚未新增混合來源的 boundary 固定 minor 證書。

| 本輪核對 | 結果 |
| --- | --- |
| 未假設共同 palette 的 C5 | 不同接點 34,560、同點 1,296 組；DP 與完整 tuples 一致，驗證 singleton 的共同 palette 必要性 |
| 任意臂 transfer | 67 個可達四列 profiles、全部六種 pair 後繼閉合；268 列最短來源路徑的完整 tuples 核對 |
| 四列縮環介面 | C3／C5／C7／C9；不同點 2,280、同點 1,608 次四列查詢與 triangle 完全一致 |
| 中間 bridge 耦合 | 12＋18 種介面，全部 60,300 次查詢；4,266 次 F={D}，18 次含 D 另拒絕一色，沒有把 D 拒絕當作完整 F |
| 反向控制 | 非共同 palette 的三色 root、同點非恆定四列、任意二元 pinning 不保持、具體耦合雙禁色 |
| 新 checker | `uv run python scripts/c5_degree5_long_triangle_roots.py --check` 唯讀逐 byte 通過；僅標準庫，保存程式及查詢 SHA256 |
| `lake build` | 通過，8,821 jobs；僅既有 AttachmentOrder／SymRelabel lint，無新增 Lean theorem |
| 文件整合 | README／HANDOFF／R19 後續入口及本報告；本地檔案連結、新檔 whitespace 與 `git diff --check` 通過 |

本輪沒有重跑 R17／R19 大覆蓋，沒有修改既有 scripts／artifacts。未 commit／push。
停止點是完整條件 root 介面，不是混合雙環的完整 disk 排除；下一步為
兩側各同點／不同點的四類真實來源，保留接點縮環、degrees／四種 z 色／
逐邊刪除著色及既有非平面 minor 的合成。兩長環、共用點長環、更多環、
其他 degree-5 分拆及一般主命題仍開放。


## 22. R16–R20 提交整理與核對

2026-09-18，依使用者 commit + push 指示，一併提交五輪 scripts、observations
證書、研究報告及 README／HANDOFF／STATUS；基準為 `b55abf4`。
各輪「未提交／下一題」保留為歷史紀錄，報告頂端增加發布說明。

- 五份證書的全部 `source_sha256`／`input_sha256` 均與目前檔案一致；
  沒有變更研究程式或證書，也未重跑 R17／R19 大型拓撲覆蓋。
- 沿用本次工作已通過的 R20 唯讀逐 byte checker 及 `lake build`（8,821 jobs）；
  R16–R19 的既有重播結果分別見 §17–20，未把指紋核對稱為重新重播。
- 提交前核對本地文件連結及 staged whitespace；本地與 origin/main 在基準上同步。

研究停止點不變：混合長環＋triangle 的完整四列 root 介面已完成，尚待真正
來源 minor、degrees／逐邊刪除著色及非平面 minor 合成。未新增 Lean theorem。
推送後的本地／tracking／遠端 SHA 核對由交付訊息記錄。

## 23. R21 混合互斥雙環的來源 minor 與排除

2026-09-18，從乾淨 HEAD `3d6a647` 接手，選擇 R20 明列的真正來源 minor
缺口，完成 [一長奇環＋triangle 排除](c5_degree5_long_triangle_minors.md)。
在唯一 degree-5、三-spoke、連通二接點分量、接受全部 T4 的 C5 disk
minimal q-obstruction 前提下，恰含一長奇環與一 triangle 的互斥雙環
分量不存在；不限制環長、臂長或無接點外枝。沒有新增 Lean theorem。

| 本輪核對 | 結果 |
| --- | --- |
| 接手 R20 重播 | 四列 root／67 profiles／60,300 耦合查詢及反向控制，唯讀逐 byte 通過 |
| 一般來源構造 | 保留長環接點及實際 attachments，三段 arc 收縮為 triangle；完整四列及 degrees 保持，再依分量解除引理重建 minimality |
| 有限控制域 | 四種有序接點型各 36 張，共 144 張；六個 palettes、環長 5／7／9；48 個既有目標，涵蓋短／長路徑代表 |
| 著色及 minor | 來源／目標全部 z 色與逐邊刪除 coloring 通過；來源 8,946 份刪邊著色；boundary 固定 minor 與合成來源 K5／K3,3 minor 逐張驗證 |
| 新 checker | `c5_degree5_long_triangle_minors.py --check` 唯讀逐 byte 通過；保存來源及輸入指紋，不呼叫 planarity oracle |
| 既有覆蓋 | 直接重播所用 subdivisions；未重跑 R17／R19 大枚舉，既有 scripts／artifacts 不變 |
| `lake build` | 通過，8,821 jobs；僅既有 SymRelabel／AttachmentOrder lint |
| 文件整合 | README／HANDOFF／R20 後續入口與新報告已整合，本地連結及 whitespace 核對通過 |

本輪為紙面化約＋有限 Python 證書，不保持完整 Σ 或任意二元 pinning。
無界排除使用 R20 一般公式、三段 arc 的一般 minor 構造及 R17／R19
既有任意路徑縮減與完整接線覆蓋；144 張來源僅驗證實作與機制。

下一題是兩個互斥長 odd-cycle blocks 的連續縮減：先核對第一次縮環
對第二側前提的保留，再保存兩步及合成來源證書。共用點長環、更多環、
其他 degree-5 分拆、一般出口及 `K∞=K≤5` 仍開放。本輪未 commit／push。

## 24. R22 兩個互斥長奇環的連續縮減

2026-09-18，從 HEAD `3d6a647` 及未提交 R21 繼續，完成
[雙長環連續縮減](c5_degree5_two_long_cycles.md)。拒絕 D 的雙側 singleton
必要性不依賴另一側為 triangle；第一側縮環保持雙側完整四列、另一側
attachments／lists／degrees、中間 bridge 與 F={D}，故第二側可接續縮減。
結合 R16–R21，唯一 degree-5、三-spoke、連通二接點分量恰含兩個互斥
odd-cycle blocks、其餘 bridges 時，接受全部 T4 的 disk minimal
q-obstruction 不存在，不限制兩環長度與路徑長度。

| 本輪核對 | 結果 |
| --- | --- |
| 真正雙長環來源 | 144 張，四種有序接點型各 36 張；有序環長 (5,7)、(7,9)、(9,5)，21 組實際 palette pairs |
| 連續縮減 | 左右兩個順序共 288 條兩步縮減、576 個逐步 minor，合成 branch sets 相同，boundary 及 z 始終 singleton |
| 完整四列 | 四階段圖各自切開 bridge 方向，18,432 次直接 (z色,root色) pinning；兩側四列跨階段一致 |
| degrees／minimality | 來源、兩種中間圖、雙 triangle 目標直接核對；來源 12,258 份刪邊著色，四階段合計 37,224 份 |
| 非平面 minor | 重驗既有 target subdivision，逐來源合成並驗證 K5／K3,3 minor |
| 新 checker | `c5_degree5_two_long_cycles.py --check` 唯讀逐 byte 通過，不呼叫 planarity oracle |
| 既有資料 | R21 及更早 scripts／artifacts 不變；核對來源與輸入指紋，直接重算所用圖與 witnesses，未重跑大拓撲覆蓋 |
| `lake build` | 通過，8,821 jobs；僅既有 SymRelabel／AttachmentOrder lint，未新增 Lean theorem |
| 文件 | README／HANDOFF／R21 後續入口與 R22 報告已整合，本地連結與 whitespace 核對通過 |

成果仍為紙面化約＋Python 有限證書；144 張來源不代表無界枚舉或全部
接線窮盡，不宣稱完整 Σ 或任意 pinning 保持。下一題為共用 cut vertex
且至少一環長於三的雙環：先求共同點的完整 root 集與交集，不套用
bridge 兩端 singleton 判準。其他 degree-5 分拆、一般出口及主命題
仍未證。R21–R22 均未 commit／push。

## 25. R23 共用點雙奇環的四列可延拓介面

2026-09-18，核對 HEAD `3d6a647` 及未提交 R21–R22 後，沿交接進入
[共用點長環介面](c5_degree5_shared_cycle_roots.md)。證明自由 root 奇環
色集至少二色，恰為二色 iff 私有 lists 全為共同二色 palette。因此
共用點雙環拒絕 iff 兩側私有 lists 為互補共同 palettes。

三種接點型保留 r 及接點縮環，保持四列可延拓布林值與完整 F；
完整側 root 集甚至共同點交集可改變，已保存兩個具體反向控制。
同點型另外保留雙禁色控制，未將僅拒絕 D 當成 minimality。

| 本輪核對 | 結果 |
| --- | --- |
| 接手 R22 | 唯讀 checker 通過：144 來源、576 逐步 minor、37,224 份四階段刪邊著色 |
| 一般 list 控制 | C5 全部 14,641 組至少二色 lists 與獨立暴力著色一致；C7 46,656 組二色 lists 核對剛性 |
| 四列比較 | 67 個外臂 profiles；同環不同點 27,750、分處兩環 10,560、同點 5,280 組；環長 3／5／7／9 |
| 新 checker | `uv run python scripts/c5_degree5_shared_cycle_roots.py --check` 唯讀逐 byte 通過，保存來源指紋及 query digest |
| 既有覆蓋 | 未重跑 R15／R17／R19 大型拓撲覆蓋；既有研究 scripts／artifacts 不變 |
| Lean | `lake build` 通過，8,821 jobs，只有既有 lint；未新增 Lean theorem |

本輪是紙面 list 論證＋有限 Python 證書，未新增 disk 排除或完整 Σ
保持結論。分處兩環的有限控制採同長同位置，不宣稱所有環長／位置對
窮盡。無界介面判準由報告的一般論證承擔。

下一步為共用點一長環／雙長環真正來源 minor、degrees／逐邊刪除
著色與 R15 非平面 minor 合成。README／HANDOFF 已更新；
R21–R23 未 commit／push，一般 degree-5 與 `K∞=K≤5` 仍未證。


## 26. 可重用接合語義的 Lean 基礎

2026-09-18。在 R21–R23 未提交成果上補入
[RootInterfaces](lean_root_interfaces.md)，由 `Math.lean` 匯入。
15 個普通 Lean 定理涵蓋共同接點／禁色、中心 `A \ ⋃ F` 接合、共用
root 交集、路徑一步訊息與不可刪減覆蓋的 private 色計數。

- 全部新定理 axiom audit 僅含標準 axioms 的子集，無 `sorryAx`／`Lean.ofReduceBool`。
- `lake build`、`lake env lean Math/RootInterfacesAudit.lean`、`git diff --check` 通過。
- 未重跑研究 Python checkers 或大拓撲覆蓋；既有研究 scripts／artifacts 不變。
- degree-4 全列刪邊解除、R23 奇環 root 剛性、縮環及圖層／拓撲合成仍未形式化。

R23 下一題仍是共用點長環來源 minor；本輪不新增 disk 排除。
所有本地研究成果及本輪 Lean／文件均未 commit／push。


## 27. R21–R23 與 Lean 接合基礎發布核對

2026-09-18，使用者要求 commit + push。本次整合三輪研究 scripts／
certificates／reports、15 個普通 Lean 接合定理與 audit、README／HANDOFF。
前述 §23–26 的「未提交」保留作當輪歷史，當前發布範圍以本節為準。

| 核對 | 結果 |
| --- | --- |
| R20 `c5_degree5_long_triangle_roots.py --check` | 通過：67 個 profiles、60,300 次耦合查詢 |
| R21 `c5_degree5_long_triangle_minors.py --check` | 通過：144 張來源、8,946 份刪邊著色 |
| R22 `c5_degree5_two_long_cycles.py --check` | 通過：144 張來源、576 個逐步 minors、18,432 次 root pinning、37,224 份四階段刪邊著色 |
| R23 `c5_degree5_shared_cycle_roots.py --check` | 通過：14,641 組 C5／46,656 組 C7；三類四列查詢 27,750／10,560／5,280 |
| Lean | 沿用同一工作階段、未再更動程式碼的全庫 build（8,822 jobs）及全部 15 個定理的 axiom audit；無 sorryAx／Lean.ofReduceBool，只有既有 lint |
| 發布檢查 | diff whitespace 與文件連結核對；發布前遠端 main 為 `3d6a647` |

未重跑 R15／R17／R19 大型拓撲覆蓋；未改動研究 scripts／artifacts。
R21–R23 的一般研究論證仍為紙面＋Python；新 Lean 定理的範圍見
[接合基礎](lean_root_interfaces.md)。R23 共用點長環來源 minor、
degrees／刪邊著色及拓撲合成仍是下一步，未新增 disk 排除結論。


## 28. R24 共用點雙奇環來源 minor 與排除

2026-09-18，從乾淨 HEAD `e14874d` 接手，完成
[共用點雙奇環來源 minor](c5_degree5_shared_cycle_minors.md)。三段 arc
收縮保留共同點與接點；共享 root branch set 合併兩側吸收頂點後仍
連通，兩種縮減順序的合成相同。由 R23 四列判準保持 F={D}，再以
完整 degrees／分量解除引理重建 minimality，接 R15 任意臂長及拓撲覆蓋。

**三-spoke、連通二接點分量恰含兩個 odd-cycle blocks 的全部位置與
任意環長已排除**（互斥為 R22，共用點為 R24）。這是紙面＋Python，
未新增 Lean theorem，不保持完整 root 或 Σ。

| 核對 | 結果 |
| --- | --- |
| R23 checker | 唯讀逐 byte 通過；14,641／46,656 組一般 lists 與三類四列查詢 |
| R24 來源 | 180 張；三類各 60；36 個目標，有序環長 (5,3)、(3,7)、(5,7)、(7,9)、(9,5) |
| Minor／四列 | 360 條兩步縮減，720 個逐步 minors（混合型含 identity）；四階段 2,880 次 z 色查詢 |
| 刪邊著色 | 來源 11,520 份，四階段合計 36,360 份；直接核對 pins 及全部邊 |
| 拓撲 | 重驗所用 R15 subdivisions，逐來源合成 K5／K3,3 minor；新 checker 停用 planarity APIs 後逐 byte 通過 |
| 反向控制 | 同點閉序列 (D,0,D) 的長環／triangle 圖皆 F={0,D}；刪 z–b0 仍不可著色，排除 minimality |
| 既有資料 | R15／R17／R19 大覆蓋未重跑；核對依賴指紋，既有 scripts／artifacts 不變 |
| Lean | `lake build` 通過，8,822 jobs，僅既有 AttachmentOrder／SymRelabel lint；未重跑無變更的 root axiom audit |
| 文件 | README／HANDOFF／R23 後續入口更新，新增 R24 報告；連結與 whitespace 核對 |

本輪未 commit／push。下一題為三環共用點鏈，先求中間環的完整有序
二接點關係，不能以獨立 root 色集接合。一般更多環、其他 degree-5
分拆、共同出口及 `K∞=K≤5` 仍開放。

## 29. R25 三環共用點鏈的 fixed-q 介面

2026-09-18，接手 HEAD `e14874d` 與未提交 R24。新增
[三環鏈介面](c5_degree5_three_cycle_roots.md)：兩臂分處末端環，保留
中間環完整有序二接點關係，以 R2∩(E1×E3) 接合。奇環 list 引理與
R23 root 剛性推出拒絕 D 時 T–S–T palettes，全部四列 F={D}。
保留接點與 palette 錨點的 list 縮環可按任意順序做，保持可延拓性。

| 本輪核對 | 結果 |
| --- | --- |
| R25 中間環 | 5,324 組 C5 完整 relations 與獨立暴力 coloring 一致；644,204 組端點限制核對拒絕充要條件 |
| R25 三環鏈 | 324,120 組四列查詢；四組有序環長、全部接點位置、六 palettes、67 profiles 中所有 D 相容組合；全部八種縮環子集 |
| R25 反向控制 | 完整中間關係改變、實際接合關係改變、邊際投影接合假陽性；保存具體 lists／profiles／pin |
| R25 重播 | 新 checker 唯讀逐 byte 通過；無 topology oracle |
| R24 重播 | 180 張來源、720 個逐步 minors、36,360 份四階段刪邊著色通過；既有 scripts／artifacts 未修改 |
| Lean | `lake build` 通過，8,822 jobs，僅既有 lint；未新增 Lean theorem、未重跑 root axiom audit |
| 文件 | README／HANDOFF 更新；新增報告連結、whitespace 核對通過 |

R15／R17／R19 大覆蓋與 R20／R23 standalone checker 本輪未重跑。
本輪依賴 R20 path profiles 實作與既有 root 紙面論證；新結果的信任層
為紙面＋Python 固定域控制，不是來源 minor、完整 Σ 或三環 disk 排除。

下一步先建立三個 triangle 鏈正常形的實際 attachments／臂接線，核對
完整 degrees、四列與逐邊刪除著色，再做 topology 證書；之後接長環
boundary 固定來源 minors。其他三環接點型與一般更多環仍開放。
R24–R25 均未 commit／push。

## 30. R26 三個 triangle 鏈正常形拓撲

2026-09-18，接手 HEAD `e14874d` 與未提交 R24–R25。新增
[三個 triangle 鏈正常形](c5_degree5_three_triangles.md)：兩臂各接
末端私有點、T–S–T palettes、臂為簡單色序列。完成該有限正常形域的
全部實際接線、degrees、四列、逐邊刪除著色與非 disk 證書。

| 本輪核對 | 結果 |
| --- | --- |
| 模板及接線 | 408 個有序模板；327,968 個實際接線，全部非 disk |
| 完整 fixed-q 介面 | 408 個代表圖各四種 z 色，共 1,632 次；全部 F={D}；另直接核對原圖 q 拒絕 |
| Minimality | 保存 19,020 份代表圖非 boundary 邊刪除著色，直接驗證 pins、色域及每條邊 |
| 同模板搬運 | 每張接線核對頂點、內部邊、degree=4／5 及各內點 boundary 色多重集；按 attachment role 搬運 fixed-q 證書 |
| 拓撲 | 72 份 K3,3 subdivisions 覆蓋所有 boundary-apex augmentations；逐接線驗證實際路徑 |
| R26 重播 | 停用 planarity APIs 後唯讀逐 byte 通過；完整 327,968 接線 coverage digest 一致 |
| R25 重播 | 唯讀逐 byte 通過：5,324 組中間 relations、644,204 組端點限制、324,120 組四列查詢 |
| Lean | `lake build` 通過，8,822 jobs，僅既有 lint；未新增 Lean theorem、未重跑 root axiom audit |
| 文件 | 新增報告及 README／HANDOFF／R25 後續入口；文件連結與 whitespace 通過 |

本輪未重跑 R15／R17／R19 大覆蓋、R24 及 R20／R23 standalone checker；
既有研究 scripts／artifacts 未改動。R26 生成時用 NetworkX 找 subdivision；
重播停用 planarity APIs，只檢查保存的證書路徑、完整接線 coverage digest
與本地程式依賴 fingerprints。

下一步以 R26 已存正常形為目標，補任意長環與重複色臂的 boundary
固定來源 minors、四列與刪邊著色，再合成非平面證書回來源。本輪尚未
宣布任意三環鏈排除，更未完成其他接點型、一般 degree-5 或 `K∞=K≤5`。
R24–R26 均未 commit／push。

## 31. R27 三環共用點鏈來源 minors

2026-09-18，接手 HEAD `e14874d` 與未提交 R24–R26。新增
[三環鏈來源 minors](c5_degree5_three_cycle_minors.md)，完成兩外臂各在
末端私有點之共用點鏈的任意長環與重複色臂化約；其餘三環型仍開放。

| 本輪核對 | 結果 |
| --- | --- |
| 有限來源 | 48 個 seed 選取、兩種擴充，共 96 份控制／90 張不同標號來源；有序環長 (5,7,9)、(7,9,5) |
| 縮環 | 每來源全部八個子集、十二個逐步 minor；共 1,152 步；576 條順序核對合成相等 |
| 縮臂 | 288 個逐步 minor，含整條臂吸收進 z；boundary singleton 始終固定 |
| 四列 | 1,056 個圖階段、4,224 次 z 色，全部 F={D}；另核對 q 拒絕 |
| Minimality | 保存並直接驗證 82,848 份完整非 boundary 邊刪除著色 |
| 拓撲 | 96 份來源控制全部合成 R26 已存 subdivision 為來源 augmentation 非平面 minor |
| 重播 | 生成與 --check 均停用 planarity APIs；核對程式／輸入 hashes，緊湊 JSON 唯讀逐 byte 通過 |
| Lean | `lake build` 通過（8,822 jobs，既有 lint）；未新增 Lean theorem |

R26 全部接線覆蓋、R25 standalone checker 及 R15／R17／R19 大覆蓋
本輪未重跑；依賴既有紙面與覆蓋，直接重驗本輪所用 R26 subdivisions。
未改動既有研究 scripts／artifacts；README／HANDOFF／R26 已補後續入口，
本輪文件連結與 `git diff --check` 通過。證書保留全部 witnesses，採緊湊
JSON（15,331,986 bytes）。
下一步分類同鏈其他接點位置，先檢查無接點末端環消去能否回到已知少環
結果；一般三環、bridge 連接型、degree≥5 與 `K∞=K≤5` 仍開放。
R24–R27 未 commit／push。

## 32. R28 三環鏈全部接點位置介面

2026-09-18，接手 HEAD `e14874d` 與未提交 R24–R27。新增
[全部接點位置介面](c5_degree5_three_cycle_positions.md)，沿用完整
有序接合，把 T–S–T 剛性擴至同末端、末端與中間、同中間及同點會合。
不同接點完整 F={D}；同點 root 為其有效 palette 的互補 pair，仍須
檢查全部四列。無接點的共用點末端環留下二色限制，不能直接刪去。

兩個不同接點同在中間環時，兩共用點加兩接點共四個不同標記；本輪
保留標記的 list 縮環目標為 C3–C5–C3，其餘位置為三個 triangles。
只證任意子集替換保持四列布林值／F，不宣稱完整 Q、Σ 或圖層 minor。

| 本輪核對 | 結果 |
| --- | --- |
| 任意 lists | 三個 triangles 的五個私有 lists 各取全部 11 種至少二色集合；161,051 組用獨立圖回溯核對，恰六組拒絕 |
| 接點控制 | 環長 (3,3,3)、(5,5,5)、(5,7,9)；全部中間第二共用點位置及可重複接點對，67 個 profiles 中所有 D 相容組合 |
| 四列查詢 | 614,736 組，包含 573,552 組不同點、41,184 組同點；各驗全部四種 z 色與八個縮環子集 |
| C5 目標 | 39,960 組兩個不同接點同中間環的查詢 |
| 獨立條件化圖控制 | 54,096 列 triangle 查詢另用不依賴 transfer 的圖回溯核對 |
| 反向控制 | 同點另拒一色 1,872 組；保存一份具體 witness，另存刪末端環改變延拓性、有序關係改變、四標記需 C5 三份控制 |
| R28 重播 | 新 checker 唯讀逐 byte 通過；保存直接本地程式依賴 hashes 與 query digest；無 topology oracle |
| R27 重播 | 96 份來源、1,152 縮環、288 縮臂、4,224 次 z 色及 82,848 份刪邊著色通過；不修改既有證書 |
| Lean | `lake build` 通過（8,822 jobs，僅既有 lint）；未新增 Lean theorem、未重跑 root axiom audit |
| 文件 | README／HANDOFF／R27 補最新入口；本地連結及 whitespace 通過 |

R25／R26 standalone checker、R15／R17／R19 大覆蓋、R20／R23 standalone
checker 本輪未重跑。新 checker 引用 R20 的 path profiles 與 R25 有序
關係實作，另以上述獨立圖回溯核對；一般長度範圍由 R28 紙面推導承擔。
既有 scripts／artifacts 未改動。本輪沒有新增來源 minor 或 disk 排除。

下一步優先建立 C3–C5–C3 型的實際接線、degrees、四列及逐邊刪除著色，
再求拓撲證書或障礙；R26 的三個 triangles 覆蓋不能直接引用到此型。
其他新位置圖層排除、環間 bridge 型與一般三環仍開放，`K∞=K≤5` 未證。
R24–R28 未 commit／push。

## 33. R29 C3–C5–C3 中間二接點正常形

2026-09-18，接手 HEAD `e14874d` 與未提交 R24–R28。新增
[C3–C5–C3 實際接線與拓撲](c5_degree5_middle_pentagon.md)，完成兩個
不同接點同在中間 C5、末端均為 triangle、簡單色序列外臂的正常形。
全部接線非 disk；任意長來源 minor 尚未建立，未宣布一般三環排除。

| 本輪核對 | 結果 |
| --- | --- |
| 循環位置 | 第一共用點在 slot 0，第二共用點四種位置，每種三組私有接點對；共 12 種，不除去鏡像重複 |
| 必要模板 | 每位置 408 個 palette／有序簡單臂組合，共 4,896 個 |
| 實際接線 | 19,693,824 種具名接線；不是非同構圖數；全部非 disk |
| 四列 | 19,584 次 z 色查詢，全部完整 F={D}；另驗原圖 q 拒絕 |
| Minimality | 286,128 份非 boundary 邊刪除後完整 q-coloring，逐頂點／pin／邊核對 |
| 同模板搬運 | 每個獨立變數只替換同內點的 b1／b3 spoke，核對邊差集與變數互異；任意组合保 degrees 與 fixed-q 著色 |
| 拓撲 | 428 份保存的 K3,3 subdivisions；4,908 次子 cube 引用覆蓋全部接線 |
| Cube 運算 | 四變數全部 6,561 組 cube 對用獨立真值表核對差集及互斥 |
| R29 重播 | 停用 planarity APIs，直接驗保存路徑及完整 cube 覆蓋；來源／載入依賴 hashes 與 25,993,740-byte 緊湊 JSON 唯讀逐 byte 通過 |
| R28 重播 | 161,051 組任意 lists、614,736 組四列查詢及反向控制通過 |
| Lean | `lake build` 通過（8,822 jobs，僅既有 lint）；未新增 Lean theorem、未重跑 root axiom audit |
| 文件 | README／HANDOFF／R28 補後續入口；本地連結及 `git diff --check` 通過 |

R27／R26 standalone checker、R15／R17／R19 大覆蓋、R20／R23 standalone
checker 本輪未重跑；未引用其拓撲覆蓋代替本輪 C5 正常形證書。沿用
R13 attachment／simple-walk helpers、既有圖著色與 subdivision checker、
R17 cube 差集，相關載入本地程式 hashes 均記入新證書；未修改既有 scripts
或 artifacts。本輪證書不依賴舊 observations.json。

下一步建立任意長奇環與重複色臂來源到本輪正常形的 boundary 固定 minors，
保留四個中間標記及 palette 錨點，再合成非平面證書回來源。
其他接點型、環間 bridge 型及一般三環仍開放，完整 Q／Σ 不宣稱保持，
`K∞=K≤5` 未證。R24–R29 未 commit／push。

## 34. R30 中間二接點三環鏈來源 minors

2026-09-18，接手 HEAD `e14874d` 與未提交 R24–R29。新增
[中間二接點任意長來源 minors](c5_degree5_middle_cycle_minors.md)，保留
兩共用點、兩接點與 palette 錨點，縮任意長奇環至 C3–C5–C3，再縮
重複色外臂，合成 R29 已存非平面證書回來源。
**三環共用點鏈、兩個不同私有接點均在中間環的任意長型已排除。**
前提仍是三-spoke、唯一 degree-5、其餘 degree-4、接受全部 T4 的 disk
minimal q-obstruction，及既有 forcing-list 正規化；一般三環未排除。

| 本輪核對 | 結果 |
| --- | --- |
| 來源域 | 12 位置×6 palettes×4 有序終色對，共 288 個 seed／288 張不同標號來源圖 |
| 長環 | 長度 (5,7,9) 或 (7,11,5)，中間五段含偶數 arcs；全部八個縮環子集 |
| 縮環 minors | 3,456 個逐步 boundary 固定 minors；1,728 個縮環順序核對合成相等 |
| 縮臂 minors | 864 步，含前綴／內部／後綴閉段；36 張來源最後兩臂均直接接 z |
| 保留點 | 所有階段 branch sets 非空、互斥、連通；boundary singleton；九個環保留點各自分離，縮臂可吸收進 z |
| 四列與 degrees | 3,168 個圖階段、12,672 次 z 色查詢，完整 F={D}，z degree=5，其餘有效內點 degree=4 |
| Minimality | 273,168 份非 boundary 邊刪除後完整 q-coloring，逐 pin／頂點／邊核對；原圖 q 拒絕 |
| 拓撲合成 | 288 個實際 R29 目標模板；使用 162 份不同已存 K3,3 subdivisions，得到 288 份來源 augmentation 的 K3,3 minor |
| R30 重播 | 生成及 checker 都停用 planarity APIs；來源／載入依賴及 R29 artifact hashes、52,270,485-byte JSON 唯讀逐 byte 核對 |
| Lean | `lake build` 通過（8,822 jobs，僅既有 lint）；未新增 Lean theorem、未重跑 root axiom audit |
| 文件 | README／HANDOFF 更新精確停止點，R29 補後續入口；本地連結及 `git diff --check` 核對 |

任意長度結論由紙面 branch-set 構造、R28 接合判準及 R29 正常形全覆蓋
共同承擔，有限來源控制不是任意長度的枚舉證明。R29 全部 19,693,824
接線覆蓋與 R28 standalone checker 本輪未重跑；核對 R29 程式指紋，
逐筆直接驗本輪所用 subdivisions，再驗合成來源每條模型邊。
R27／R26、R15／R17／R19 大覆蓋亦未重跑。既有 scripts／artifacts 未改。

下一步是同末端兩個不同私有接點的 C3–C3–C3 正常形實際接線與拓撲
覆蓋；不能直接刪無接點末端環，也不能套用 R26 的不同接點位置域。
末端與中間、同點會合、環間 bridge、其他分拆 (2) 及一般三環仍開放。
完整 Q／Σ 不宣稱保持；`K∞=K≤5` 未證。R24–R30 未 commit／push。

## 35. R31 同末端不同二接點正常形

2026-09-18，接手 HEAD `e14874d` 與未提交 R24–R30。新增
[同末端不同二接點正常形拓撲](c5_degree5_same_terminal_triangles.md)，
完成 C3–C3–C3、兩臂同在一個末端不同私有點、簡單色序列外臂的
全部實際接線非 disk 覆蓋。保留另一無接點末端環的二色限制。
任意長來源 minor 尚待建立；一般三環仍未排除。

| 本輪核對 | 結果 |
| --- | --- |
| 必要模板 | 六個中間 palettes、有序簡單臂對，共 408 個 |
| 實際接線 | 327,968 種具名接線，全部非 disk；不是非同構圖數 |
| 四列與 degrees | 1,632 次 z 色查詢，完整 F={D}；z degree=5，其餘有效內點 degree=4；原圖 q 拒絕 |
| Minimality | 19,020 份非 boundary 邊刪除後完整 q-coloring，逐 pin／頂點／邊核對 |
| 同模板搬運 | 每個變數只替換同內點的 b1／b3 spoke，逐一核對邊差集及變數互異；搬運全部 fixed-q 著色 |
| 拓撲 | 68 份保存 subdivisions、435 次子 cube 引用，覆蓋全部接線 |
| Cube 控制 | 四變數全部 6,561 組 cube 對，真值表核對差集及互斥性 |
| R31 重播 | 停用 planarity APIs，直接驗路徑及完整 cube 覆蓋；來源／本地依賴 hashes、1,592,286-byte JSON 唯讀逐 byte 通過 |
| Lean | `lake build` 通過（8,822 jobs，僅既有 lint）；未新增 theorem、未重跑 root axiom audit |
| 文件 | README／HANDOFF 更新入口，R30 補後續連結；本地連結及 whitespace 核對 |

沿用 R13 attachment／simple-walk helpers、既有圖著色與 subdivision
validator、R17 cube 差集，載入本地程式 hashes 記入新證書。未讀取舊
observations.json，未修改既有 scripts／artifacts。R28 紙面判準引用，
standalone checker 未重跑；R30／R29／R27／R26、R15／R17／R19
既有大覆蓋亦未重跑。本輪拓撲覆蓋不引用 R26 的不同位置域。

下一步建立此型任意長來源 boundary 固定 minors，保留共用點、兩接點
及中間／無接點末端 palette 錨點；再縮外臂並合成 R31 拓撲證書回來源。
末端與中間、同點、環間 bridge、其他分拆 (2) 及一般三環仍開放。
完整 Q／Σ 不宣稱保持，`K∞=K≤5` 未證。R24–R31 未 commit／push。

## 36. 文件現況盤點與變化追蹤

2026-09-18，文件整理；沒有新增數學結論。接手時 HEAD 與本地
`origin/main` 均為 `e14874dbf4426150a19bf4435b90ff0fad98bb07`；
未連線核對遠端。既有四份 tracked 文件變更與 R24–R31 八組未追蹤
報告／script／artifact 保留，未 commit／push。

- 將 STATUS 頁首從 R28 更新至 R31；README 去除重複的逐輪敘述，
  改為目前適用範圍與報告入口。HANDOFF 區分最新研究驗證與本次文件盤點。
- §2 補入先前遺漏的 12 份文件，涵蓋 R20–R31 與 Lean 接合基礎；
  共 97 份 docs Markdown，其中本頁為索引，另外 96 份均有 §1–2 入口。
- §3 補已被續作解決的停止點；R25／R27／R28 及 Lean 接合說明補最新
  後續入口，原研究輪的論證與驗證紀錄保留。
- §4 記錄六項可能改變結論或文件狀態的方向，列明需要的新證據。
- 本次核對文件索引覆蓋、本地 Markdown 連結及 `git diff --check`。
  未重跑 Python 研究 checker、Lean build 或 axiom audit；前輪驗證只引用
  原紀錄，尤其 R31 見 §35。未修改 scripts、artifacts 或 Lean 原始碼。

精確停止點仍是 R31 同末端不同二接點的任意長來源 minors，見
[HANDOFF §2](HANDOFF.md#2-精確停止點與下一個窄問題)。一般三環、一般
degree-5 與 `K∞=K≤5` 仍未證。

## 37. R24–R31 整合提交與發布核對

2026-09-18，依使用者 `commit + push` 指示，自 `e14874d` 整合
R24–R31 的八份報告、八個 scripts、八份 artifacts，以及文件入口、
後續連結與變化追蹤。提交前遠端 `main` 與本地 HEAD 均為
`e14874dbf4426150a19bf4435b90ff0fad98bb07`；使用一般 push，不強制覆寫。
本節描述此次提交的驗證範圍，最終提交 SHA 與推送結果以 Git 為準。

| 核對 | 結果 |
| --- | --- |
| R24 共用點雙奇環 minors | `c5_degree5_shared_cycle_minors.py --check` 通過，180 張來源 |
| R25 三環鏈 root | `c5_degree5_three_cycle_roots.py --check` 通過，324,120 次四列查詢 |
| R26 末端二臂正常形 | `c5_degree5_three_triangles.py --check` 通過，408 模板／327,968 接線 |
| R27 末端二臂來源 minors | `c5_degree5_three_cycle_minors.py --check` 通過，96 張來源 |
| R28 全部接點位置介面 | `c5_degree5_three_cycle_positions.py --check` 通過，含 1,872 組同點雙拒絕控制 |
| R29 中間 C5 正常形 | `c5_degree5_middle_pentagon.py --check` 通過，4,896 模板／19,693,824 接線 |
| R30 中間二接點來源 minors | `c5_degree5_middle_cycle_minors.py --check` 通過，288 張來源／273,168 份刪邊著色 |
| R31 同末端正常形 | `c5_degree5_same_terminal_triangles.py --check` 通過，408 模板／327,968 接線 |
| Lean | `lake build` 通過，8,822 jobs；僅既有 lint，未新增 Lean theorem |
| 文件 | docs 全索引、本地連結目標及 `git diff --check` 核對通過 |

上述 scripts 均位於 `scripts/`，統一使用
`uv run --with networkx==3.5 python scripts/<檔名> --check`；唯讀重建
並比對既有證書，不重新搜尋拓撲 witnesses。研究 scripts／artifacts
內容未因發布而修改。R15／R17／R19 等較早 standalone checker 與
Lean axiom audit 本次未重跑；其既有紀錄與本次重播範圍分開。

本次發布不擴大數學結論：R31 同末端型任意長來源 minors 仍待補，
一般三環、degree-5、共同出口及 `K∞=K≤5` 仍未證。各專題報告與本頁
歷史節中的「未提交」描述該研究輪當時狀態，並非此次整合後的發布狀態。


## 38. 相鄰雙缺失的 12-bit 定向實驗

2026-09-18，依使用者指定轉向五個 sector 目標的實現性，見
[報告](c5_sector_targets.md)。獨立重現抽象篩選 3,072／640／5；
14 份已存圖接線對照未命中。固定目標 3647，完整窮舉 |C|≤3 的
1,548 份有標號 degree／接點候選，130 份 disk，零命中；
相鄰雙缺失 disk 圖只重現既有 {C,D} 二內點控制，沒有新一般機制。
不自動增加大小或環數；R31 來源 minor 缺口保留但暫不優先。

本輪新 checker `c5_sector_targets.py --check`、`lake build` 及
`git diff --check` 通過；舊控制在新 checker 直接驗完整列與刪邊，
舊 standalone checker／R24–R31 大覆蓋未重跑。未新增 Lean theorem，
未 commit／push；核心猜測、一般 degree-5 與主命題仍未證。


## 39. 3903 的既有非 disk 正控制

2026-09-18，見 [報告](c5_sector_positive_control.md)。只掃已保存樹分量
648 個 templates 的實際 edges：22 份 proper=831、完整=3903，均為
四內點 sector 且本身非平面。選第 41 號，獨立核對 K／G 各 240 列及
16 條非 boundary 邊刪除；原圖相鄰雙缺失且 minimal。保存全部 22 份
K3,3 subdivisions，checker 禁用 planarity oracle 直接重播。

新 checker `c5_sector_positive_control.py --check`、`lake build` 及
`git diff --check` 通過。沒有生成新圖族、未掃完其他既有候選，未重跑
舊覆蓋或 |C|≤3 生成器。使用者分層稽核另標為外部結果，沒有冒充本輪重播。
本輪證明 3903 的 degree／染色條件可以共存；尚未證任何一般 disk 排除，
亦無平面非 disk 控制。保留 not(E_B and E_C) 的待證形式，不預設禁 C，
不擴及其他四目標。未新增 Lean theorem，未 commit／push。


## 40. 831 的平面／disk 等價與必要連接

2026-09-18，見 [報告](c5_sector_structural.md)。採納使用者的前提修正：
induced 框圈＋非空連通內部給出平面⇔指定 disk 的一般紙面引理，
取消 §39 保留的平面非 disk 分支。831 的 proper 條件相等公式及
五個 chord 排除已核對全部 240 列。

以單次 Kempe swap 紙面推導四項必要連接；proper 01232 下的 b1–b3
路徑給出同一染色的互補色分離。但既有正控制也通過此局部條件，
跨列共同 witness 仍未建立，一般 3903 非平面仍未證。
新 `c5_sector_structural.py --check`、`lake build`、`git diff --check`
通過；只核對單張已存控制的 2／3／2／1 份延拓，未重播其餘正控制、
未生成新圖、未新增 Lean theorem。未 commit／push。


## 41. Sector 三輪研究整合提交

2026-09-18，依使用者「紀錄 commit」指示，整合 §38–§40 的三份報告、
三個 scripts、三份 artifacts，以及 README／HANDOFF／STATUS；只提交，不 push。
研究輪中的「未 commit／push」保留為當時紀錄，後續狀態以本節及 Git 為準。

本對話已完成三個新 checker 的 `--check`，以及最後一輪的 `lake build`
（8,822 jobs，僅既有 lint）。本次整理沒有改動程式或證書，沿用這些通過
結果；提交前另核對 staged diff whitespace 及文件連結。沒有重跑舊大覆蓋。

停止點不變：平面／disk 等價及 831 的條件相等已作紙面推導，
3903 必然非平面仍待證；不同染色的必要連接不可直接拼成共同 subdivision。
未新增 Lean theorem，不自動擴大圖搜尋。

## 42. Tutte 依賴鏈與較小證書

2026-09-18，依使用者「整理 commit + push」指示，整理
[拓撲報告](c5_sector_structural.md) 與 [正控制](c5_sector_positive_control.md)，
同步 README／HANDOFF。補入 Tutte《How to Draw a Graph》(3.1)/(5.1)
的原文出處、單一 Γ-bridge 前提、兩個前提控制，以及交替互斥路徑到
K3,3 subdivision 的最短內部連接構造。開口圖與內部分裂的適用界線保留。

第 41 號正控制新增不使用 u 的九路徑證書，內點僅 b3、w；
structural script／artifact schema 2 直接驗邊、端點、簡單性與內點互斥。
這不是保持染色介面的刪點化約，也不是一般兩路徑存在性的證明。

本輪實際重播：

- `uv run --with networkx==3.5 python scripts/c5_sector_structural.py --check`：
  240 proper 列、五個 chord、四項必要連接與新增九路徑證書通過。
- `uv run --with networkx==3.5 python scripts/c5_sector_positive_control.py --check`：
  648 份既有模板、22 份正控制、7,776 次列交叉核對與選定原圖 16 次刪邊通過。
- `lake build`：8,822 jobs 成功，只有既有 lint；`git diff --check` 通過。

未生成新圖、未重播舊 R 系列大覆蓋、未新增 Lean theorem。
停止點：831＋雙開口是否強迫兩條交替互斥 Γ-paths 尚待證；路徑可來自
不同染色，但必須證明互斥。3903 一般排除、其他四目標及 R31 缺口不變。
本次發布包含先前已提交但未 push 的 sector 三輪提交 e1b18de；
最終本地／tracking／remote SHA 與乾淨狀態於 push 後核對，以 Git 為準。

## 43. 3903 強迫連通抽取

2026-09-18，見 [報告](c5_sector_forced_connectivity.md)。依使用者指示，
固定圖大小，完成十個接受列 × 六色對的 boundary 分量分割抽取；
任意塊子集交换不能落入兩拒絕列，七個未指定開口列保留未知。
排除 14 個分割案例；加入同色對／互補色對的不交錯條件後，每列仍有
局部抽象存活者，不構成圖實現或一般排除。

固定 22 份既有正控制，重驗十二位簽章與全部 650 份接受延拓；118 份
出現互補色交錯，每張各從一份共同染色抽出 P、Q、最短內部 R 與
K3,3 九路徑，直接驗邊及內點互斥，不使用 planarity oracle。
第 9 列的全部 32 份延拓沒有互補色交錯，否定鎖定該列的更強抽取候選。
下一步只研究跨列交換相容性與「某列存在」的強迫抽取，不增加圖大小。

新 checker `c5_sector_forced_connectivity.py --check`、`lake build`、
`git diff --check` 通過；旧 checker／minimality／R 系列大覆蓋未重跑。
未新增 Lean theorem；一般 3903 非平面、其他目標與 R31 缺口保留。
本輪未 commit／push。


## 44. 3903 跨列分割閉包與實際交換軌道

2026-09-18，見 [跨列交換報告](c5_sector_cross_row.md)。交換任意 s/t
分量保持 s/t 與互補色對的誘導子圖；加入全域色交換的精確重標，對
全部 19 列的 670 個局部 disk profiles 做後繼閉包，刪去 67 個後穩定
在 603 個。十個接受列皆有存活者，這套規則尚不能推出共同路徑見證。
保存所有刪除原因及最終每項交換要求的後繼；不是共同圖實現證書。

固定 22 張控制的全部 19 列共有 1,100 份全域色置換正規化染色。
逐一保存所有單分量交換（包含不碰框的分量），每張恰有一個軌道；
每份染色至多三步到達指定接受列的共同見證，終點共 118 份。
每個終點驗 P/Q/R 及九路徑，每個非終點保存距離遞減的交換步驟。
這是固定控制結果，未證一般 Kempe 連通性、三步界或一般共同見證。

下一缺口是混合色對分量的變化、共同內部圖與交換歷史的相容性。
本輪不生成新圖；一般 3903 非平面、其他四目標與 R31 缺口保留。
重播 `c5_sector_cross_row.py --check`、前輪
`c5_sector_forced_connectivity.py --check`、`lake build` 及
`git diff --check`；未重跑舊 standalone checker、minimality 或 R 系列
大覆蓋。未新增 Lean theorem，未 commit／push。


## 45. 3903 兩輪成果整合提交與發布

2026-09-18，依使用者「整理一下 commit + push」指示，整合
[強迫連通抽取](c5_sector_forced_connectivity.md) 與
[跨列交換](c5_sector_cross_row.md) 的兩份報告、兩個 scripts、兩份
artifacts，並同步 README／HANDOFF／STATUS。研究輪中的
「未 commit／push」保留為歷史狀態，本節記錄本次提交發布範圍。

程式與證書沿用研究輪版本。本對話已重播兩個 `--check`，
`lake build` 成功（8,822 jobs，僅既有 lint）；發布整理只更動文件，
沿用這些驗證結果，另核對文件連結與 staged diff whitespace。
未重跑舊 standalone checker、原圖 minimality 或 R 系列大覆蓋。

精確停止點不變：兩色分割保持的跨列閉包仍有 603 個 profiles；
22 張控制的單軌道及至多三步到見證，只是固定圖結果。下一缺口是
混合色對分量的實際變化與共同交換歷史；一般 3903 非平面仍未證。
未增加圖大小、未新增 Lean theorem。提交後 push 至 origin/main，
並核對本地／tracking／remote SHA 一致及乾淨狀態；最終結果以 Git 為準。
