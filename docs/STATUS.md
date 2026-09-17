# 文件狀態與可能變化追蹤

更新日期：2026-09-17。前輪整理基準為 `fb6216e`；目前 HEAD 為 `7fdc19e`。
恰一個長環研究見 §7；本輪保留其未提交成果，完成多長環遞迴與連續縮減，見 §8。
此頁是目前文件索引及後續觀察紀錄，詳細數學敘述仍以原報告為準。
研究主入口是 [HANDOFF.md](HANDOFF.md)，逐輪原始交接保存在
[HANDOFF_HISTORY.md](HANDOFF_HISTORY.md)。新成果是紙面歸納與化約控制，未擴大 disk catalog。

## 1. 閱讀順序與文件角色

| 需求 | 入口 | 用途 |
| --- | --- | --- |
| 接續當前研究 | [HANDOFF.md](HANDOFF.md) | 現況、精確停止點、信任界線及最小重播命令 |
| 找報告或追蹤待變化項目 | 本頁 §2–4 | 70 份專題文件的分組索引、已被後續處理的舊問題、仍待驗證的方向 |
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
| [四環鏈](c5_four_triangle_chain.md)、[四環分叉](c5_four_triangle_star.md)、[bridge pruning](c5_shared_pair_bridge.md) | 恰四環全部連接型排除；其下一題由新 triangle-tree 報告處理；一般替換仍是紙面，介面及拓撲控制為 Python 證書 |
| [任意 triangle tree](c5_triangle_tree_palettes.md) | 七種介面歸納、非 D 二色禁集吸收與閉鄰域 minor；全 degree-4 連通 triangles／bridges 類別中，triangles 必互斥且至多二，不需 T4；未 Lean 化 |
| [長 odd-cycle root](c5_odd_cycle_roots.md) | 一般 root 有十一種介面；不可著色時仍為互補 pairs；保留三點縮成 triangle，排除恰一個長環加任意 triangles／bridges，不需 T4；紙面＋既有證書，未 Lean 化 |
| [多長 odd-cycle](c5_multi_odd_cycles.md) | 十一種介面在任意有限環樹封閉；連續 minor 排除 odd-cycles／bridges 類別中的所有長環，剩餘 triangles 互斥且至多二；不需 T4，紙面＋有限證書，未 Lean 化 |

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
| 長環 root 的「下一題兩個長環」 | [多長環報告](c5_multi_odd_cycles.md) 已完成兩環的連續縮減，並明列任意多長環的歸納與終止論證；下一題為 K4／bridge 介面 |
| 較早 handoff 的「completion 未證」 | [同頂點 completion](c5_completion_weak_bisimulation.md) 已有紙面證明；topology 未 Lean 化仍成立 |
| 較早 block 報告說「未新增 Lean theorem」 | 指該輪整個化約；後來共有 list 引理進入 [ForcingLists.lean](../Math/ForcingLists.lean)，不代表 minor／disk 論證也進入 Lean |
| 各輪「尚未提交／推送」 | 屬於當時狀態；從 `7fdc19e` 接續的兩輪長環研究隨本次提交一併發布；即時發布狀態以 Git 為準 |
| enumerator 兩個「§14」 | edge-mask 仍為 §14；獨立 cross-check 改為 §16，對應導引一併更正 |

本輪對近期主線報告補上後續連結，保留原輪次內容。歷史交接以快照方式保存，
不逐句改寫當時的未知或發布紀錄。

## 4. 可能出現新變化的地方

以下起於 **2026-09-17 閱讀既有材料時的追蹤紀錄**。R1–R3 已由同日接手研究
完成，R4–R6 保留；後續完成 R7–R8，新增 R9。各項成果層級與範圍仍以連結報告為準。

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

- **狀態：下一個窄問題，未啟動。**
- 在完整 degree=4 下，K4 無法與其他 cycle block 共用點，只能經 bridges
  接到其餘 blocks。先核對其四頂點的三色 residual lists／bridge forcing。
- 再找 boundary 固定的必要 minor 或 disk 排除；保留新 spokes 的 minimality
  核對。含 K4 的一般 block tree 及 degree≥5 尚未由 R8 涵蓋。

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
