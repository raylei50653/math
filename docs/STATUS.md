# 文件狀態與可能變化追蹤

整理日期：2026-09-17。依本地 HEAD `fb6216e` 的文件、程式與既有證書核對；
開始時工作樹乾淨。此頁是目前文件索引及後續觀察紀錄，詳細數學敘述仍以原報告為準。
研究主入口是 [HANDOFF.md](HANDOFF.md)，逐輪原始交接保存在
[HANDOFF_HISTORY.md](HANDOFF_HISTORY.md)。本次沒有新增研究結論或擴大搜尋範圍。

## 1. 閱讀順序與文件角色

| 需求 | 入口 | 用途 |
| --- | --- | --- |
| 接續當前研究 | [HANDOFF.md](HANDOFF.md) | 現況、精確停止點、信任界線及最小重播命令 |
| 找報告或追蹤待變化項目 | 本頁 §2–4 | 67 份專題文件的分組索引、已被後續處理的舊問題、仍待驗證的方向 |
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
| [四環鏈](c5_four_triangle_chain.md)、[四環分叉](c5_four_triangle_star.md)、[bridge pruning](c5_shared_pair_bridge.md) | 恰四環全部連接型排除；當前停止在任意純共用點 triangle tree；一般替換仍是紙面，介面及拓撲控制為 Python 證書 |

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
| 四環分叉的「bridge 混合型未涵蓋」 | [bridge pruning](c5_shared_pair_bridge.md) 已補齊恰四環；一般更大 cluster 仍未解 |
| 較早 handoff 的「completion 未證」 | [同頂點 completion](c5_completion_weak_bisimulation.md) 已有紙面證明；topology 未 Lean 化仍成立 |
| 較早 block 報告說「未新增 Lean theorem」 | 指該輪整個化約；後來共有 list 引理進入 [ForcingLists.lean](../Math/ForcingLists.lean)，不代表 minor／disk 論證也進入 Lean |
| 各輪「尚未提交／推送」 | 屬於當時狀態；本次起點 HEAD `fb6216e` 已包含近期三輪成果，工作樹乾淨；本次未查遠端同步狀態 |
| enumerator 兩個「§14」 | edge-mask 仍為 §14；獨立 cross-check 改為 §16，對應導引一併更正 |

本輪對近期主線報告補上後續連結，保留原輪次內容。歷史交接以快照方式保存，
不逐句改寫當時的未知或發布紀錄。

## 4. 可能出現新變化的地方

以下均為 **2026-09-17 閱讀既有材料時的追蹤紀錄**。優先級是接手建議；
不表示已有新證書、啟動新搜尋或證明了一般化。後續若有進展，應補日期、
來源、驗證命令、適用範圍與反例，再更新此處狀態。

### R1：bridge pruning 可能給出更強的 cluster 篩選

- **狀態：可由現有紙面論證檢查的推論，尚未另立一般定理。**
- 來源：[bridge pruning §1、§3](c5_shared_pair_bridge.md)。隔離選定 cluster 的論證
  沒有限制外側 triangle 總數；在同樣全 degree-4、連通、所有其他 blocks 為 bridges／triangles
  的 minimal q-obstruction 中，任何大小 2、3、4 的完整 cluster 似乎都可直接排除。
- 下一個確認：逐項核對對任意總環數的反覆替換是否始終維持原假設；若成立，
  剩餘 cluster 尺寸只能為 1 或至少 5，且全為 1 的三環以上情形已有互斥結果排除。
  這不等於從一個大 cluster 任選四環就能剪出已排除模板。

### R2：鏈與分叉的 palette 規則可能統一為樹上遞迴

- **狀態：優先研究候選，未證。**
- 來源：[鏈的 transfer](c5_four_triangle_chain.md) 與 [分叉禁集](c5_four_triangle_star.md)。
  鏈上非空二色禁集只在互補 palette 時傳遞，空禁集不恢復；分叉的不可著色
  則要求三個末端 palettes 相同。兩者提示可檢驗一套任意 triangle tree 的相容規則。
- 下一個確認：先寫清 root 可取色集合、分叉合併與 minimality 的作用，
  用既有鏈／分叉與 rooted pair 的 D singleton 當控制。即使 list 規則成立，
  仍要另證可實現的 disk minor，不能把 palette 遞迴當作拓撲排除。

### R3：從大 cluster 抽出小 minor 是真正的幾何接點

- **狀態：優先缺口，已有介面反例約束。**
- 來源：[root 介面反例](c5_root_interfaces.md)、[四環鏈](c5_four_triangle_chain.md)、
  [bridge pruning](c5_shared_pair_bridge.md)。共享點已由兩個 triangles 用滿 degree=4，
  其介面是二色禁集；刪去／收縮子樹可能改變度數、list 與逐邊 minimality。
- 下一個確認：選一條可歸納的局部替換，逐一核對 boundary 固定、必要 minor、
  q 不可延拓，以及後續排除定理真正需要的假設。不能借用 bridge 的 singleton
  證明，也不能假定固定 q 替換保持完整 root interface 或 Σ。

### R4：bridge pruning 的證明已穩定，可能值得接入 Lean

- **狀態：形式化候選，未啟動。**
- 來源：[ForcingLists.lean](../Math/ForcingLists.lean) 與 [bridge pruning §1](c5_shared_pair_bridge.md)。
  singleton／swap 的代數已形式化；新 D 葉點三條 spokes 的刪邊延拓論證已補齊。
- 下一個確認：先定義 boundary 固定的圖替換與 edge-minimality，將染色延拓和
  degree 保持分開證；minor／disk 層另外建立所需模型，不能用新增 topology 公理代替。
  這條線提升證明可信度，本身不封閉任意 cluster 的研究缺口。

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

## 5. 本次整理與驗證紀錄

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
