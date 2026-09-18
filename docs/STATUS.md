# 文件狀態與可能變化追蹤

更新日期：2026-09-18。本次提交整合基準 `be97121` 之後的 R11–R15 五輪成果。
發布前核對見 §16；共用點雙 triangle、單長奇環、單 triangle、樹及區域見 §15–11。
先前兩輪長環研究與發布紀錄保留於 §7–8。
此頁是目前文件索引及後續觀察紀錄，詳細數學敘述仍以原報告為準。
研究主入口是 [HANDOFF.md](HANDOFF.md)，逐輪原始交接保存在
[HANDOFF_HISTORY.md](HANDOFF_HISTORY.md)。新成果是紙面歸納與化約控制，未擴大 disk catalog。
§11–15 及專題報告中的「HEAD／未提交」保留研究當時狀態；即時發布狀態以 Git 為準。

## 1. 閱讀順序與文件角色

| 需求 | 入口 | 用途 |
| --- | --- | --- |
| 接續當前研究 | [HANDOFF.md](HANDOFF.md) | 現況、精確停止點、信任界線及最小重播命令 |
| 找報告或追蹤待變化項目 | 本頁 §2–4 | 77 份專題文件的分組索引、已被後續處理的舊問題、仍待驗證的方向 |
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
| [三-spoke 單長奇環二接點](c5_degree5_odd_cycle_components.md) | 保留接點縮成 triangle，保持全部固定-q z 色及 minimality；任意單 odd-cycle 加 bridges 排除，147 張具名來源 minor 控制；多環仍開放，未 Lean 化 |
| [三-spoke 共用點雙 triangle](c5_degree5_shared_triangles.md) | 共用 cut vertex 的任意二接點位置／外枝排除；888 模板、295,920 接線非 disk；互斥雙 triangle 的 bridge 路徑仍開放，未 Lean 化 |

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
| 較早 handoff 的「completion 未證」 | [同頂點 completion](c5_completion_weak_bisimulation.md) 已有紙面證明；topology 未 Lean 化仍成立 |
| 較早 block 報告說「未新增 Lean theorem」 | 指該輪整個化約；後來共有 list 引理進入 [ForcingLists.lean](../Math/ForcingLists.lean)，不代表 minor／disk 論證也進入 Lean |
| 各輪「尚未提交／推送」 | 屬於當時狀態；長環兩輪已隨 `dad5940`、R9–R10 已隨 `be97121` 發布；本次整合 R11–R15，核對見 §16；即時發布狀態以 Git 為準 |
| enumerator 兩個「§14」 | edge-mask 仍為 §14；獨立 cross-check 改為 §16，對應導引一併更正 |

本輪對近期主線報告補上後續連結，保留原輪次內容。歷史交接以快照方式保存，
不逐句改寫當時的未知或發布紀錄。

## 4. 可能出現新變化的地方

以下起於 **2026-09-17 閱讀既有材料時的追蹤紀錄**。R1–R3 已由同日接手研究
完成，R4–R6 保留；後續完成 R7–R9、R10 染色介面、R11 區域化約、R12 樹分支、
R13 單 triangle、R14 單長奇環與 R15 共用點雙 triangle 分支。
互斥雙環及更多環三-spoke 分量與一般 degree-5 排除仍開放。
各項成果層級與範圍仍以連結報告為準。

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
