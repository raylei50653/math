# 四色求解與共同約束實驗導覽

<a id="最新進度"></a>

## 研究概況與閱讀入口

這條線研究如何逐步處理圖的著色限制，保留所有可行的組合，最後接回一份完整染色。
它提供[4CT主線](4ct_guide.md#精確消元主線的研究契約)使用的求解與核對工具；
主攻及第一個研究工作由該研究契約維護。

先讀下方[流程說明](#先理解整個流程)，就能掌握原圖、消元與回填的關係。
要查已有成果的精確範圍，可從[解空間與接口](four_color_mathematical_model.md)、
[有限域分解](four_color_bounded_projection.md)及[六邊割來源](four_color_six_cut_exclusion.md)進入。
各項結果、未解義務與實測數字以原報告為準；其他問題依[報告入口](#報告與證據入口)查找。

## 目標與範圍

工具要找出一份符合全部原邊與指定顏色的完整染色，或判定這些條件無法共同滿足。
輸入可以是一般有限簡單無向圖；平面結構的研究另由[4CT導覽](4ct_guide.md)組織。
求解器與原型讓我們觀察哪些限制可以提前傳播、哪些組合必須共同處理，以及不同表示的成本。

## 先理解整個流程

1. **從原圖出發。** 每條邊要求兩端異色，指定顏色也一起保留。各份局部資料都對應同一張圖。
2. **逐步消元。** 處理一個頂點時，把它與周圍限制合併，記下剩餘部分哪些著色還能接回它。
   這些新限制繼續參與後面的處理；只記每點各有哪些顏色，會丟失點與點之間的組合關係。
3. **最後共同回填。** 先找到一份同時滿足剩餘限制的著色，再倒序接回已處理的頂點，核對全部原邊。
   局部各自有選擇，仍可能無法共同相容。

「完整接口」記錄一組相接頂點的可行著色組合；每個組合能接回的內部選項稱為 fibre。
需要精確定義時查[接口語義](four_color_mathematical_model.md#原問題是一份共同指派)，
需要核對整個流程為何能保解及回填時查[完備性證明](four_color_completeness.md)。

## 報告與證據入口

下表按想理解的問題分組，保留影響方法選擇的短限定；完整前提、結論、證據與後續來源由各報告維護。

### 語義、完整性與表示

| 想查的問題 | 來源 |
| --- | --- |
| 消元與回填在程式中如何運作 | [約束引擎](four_color_constraints.md) |
| 為什麼有解能回填、無解能判否，需要哪些條件 | [完整消元的完備性](four_color_completeness.md) |
| 全部解、完整接口與回填選項如何對應 | [解空間與接口語義](four_color_mathematical_model.md) |
| 要保留多少選項，壓縮時不能丟掉什麼 | [可能性保留與回填壓縮](four_color_retention.md) |
| 中途停止後如何表示原問題的全部解 | [部分消元歷史](four_color_partial_history.md)：獨立原型，未接主求解器。 |
| 一次大投影能否由多個較小投影精確表達 | [有限域分解消元](four_color_bounded_projection.md#lean文獻與研究界線)：獨立原型，未整合；整次成本可能退步。 |
| 不展開完整大表，如何逐次詢問接口 | [局部資訊與按需查詢](four_color_local_information.md#2026-10-26按需查詢局部接口)：獨立原型，未列舉全部fibres。 |

### 傳播與找型

| 想查的問題 | 來源 |
| --- | --- |
| 選點、試色、回退與原圖衝突如何展示 | [四條規則與播放器](four_color_lab.md) |
| 不同局部結果如何在共同接口上篩選 | [共同接口交集](four_color_intersections.md) |
| 如何把交集與原環限制一起使用 | [交集與原環閉合](four_color_combined_cycles.md) |
| 傳播穩定為什麼仍可能沒有共同解 | [保證與缺口](four_color_guarantee_gap.md) |
| 如何把同一中心的條件帶進環上推理 | [共同條件原環與接口](four_color_cycle_contexts.md) |
| 如何搜尋部分原輻條提供的限制 | [部分輻條搜尋](four_color_partial_spokes.md) |
| 具名九點構型提供什麼共同關係 | [九點共同限制](four_color_joint_constraints.md) |
| 如何辨認該構型並交給主傳播 | [九點自動找型](four_color_joint_propagation.md) |
| 哪些局部衝突可由原邊與候選域核對 | [已知衝突子型](four_color_conflicts.md) |
| 五環支援與雙中心限制如何推出 | [C₅結構自約束](four_color_c5_structure.md) |
| 如何尋找五環並查閱其著色關係 | [C₅推導與查表](four_color_c5.md) |

### 分區、重用與成本

| 想查的問題 | 來源 |
| --- | --- |
| 各種方法的適用條件、額外成本及退步例 | [方案橫向比較](four_color_method_comparison.md) |
| 數學分析提出哪些運算候選 | [數學優化候選](four_color_mathematical_optimization.md)：獨立原型，未接主引擎。 |
| 先分區再接邊界會如何影響工作量 | [分區消元策略](four_color_partition.md#同40例結果)：可選；固定批次整體退步，保留原預設。 |
| 能否依當前限制調整分區 | [動態訊息分區](four_color_information_partition.md#固定40例完整比較)：已整合，本批未見整體加速。 |
| 如何減少傳播時的重複處理 | [delta傳播](four_color_delta_propagation.md#最終結果)：有限比較有改善，保留scan預設。 |
| 如何沿完整接口支援的流失繼續傳播 | [完整支援流失](four_color_support_loss.md#同40例比較未見整體加速)：可選，本批未見整體改善。 |
| 圈區與掃描次序如何影響接口訊息 | [圈區與實際接口訊息](four_color_region_messages.md)：求一解原型，有限樣本有收益也有退步。 |
| 哪些換色對稱能重用子樹的查詢答案 | [子樹換色快取](four_color_local_symmetry.md#保留邊界)：未接主引擎；求一解，未列舉全部fibres。 |
| 較大原圖中的工作量與見證如何核對 | [較大原圖](four_color_larger_structures.md) |
| 流程中如何減少重複查詢與候選枚舉 | [流程優化](four_color_flow_optimization.md) |
| 工作上限與完整紀錄容量如何分開設定 | [記憶體與紀錄容量](four_color_memory_optimization.md) |
| 保留哪些索引可以換取查詢成本的降低 | [RAM索引](four_color_ram_indexes.md) |
| 前綴剪枝、等色類與共同換色如何使用 | [邏輯優化](four_color_logic_optimization.md) |

### 原圖結構與邊割

| 想查的問題 | 來源 |
| --- | --- |
| 完整接口與交換鎖定能否增加既有D判準的排除 | [D與鎖定比較及停止裁決](ck_d_lock_comparison.md#證據層重播與停止範圍)：指定鎖定條件無增益，已停止擴枚舉。 |
| 最小無解核心對原邊與小邊割有什麼要求 | [最小核心與小邊割](four_color_critical_obstructions.md) |
| 六跨邊的換色障礙如何分類 | [六跨邊分類](four_color_six_edge_cuts.md) |
| 平面來源如何補上六邊割排除，後續缺口在哪裡 | [hub輪圈與六邊割排除](four_color_six_cut_exclusion.md) |

## 精確停止點

一般判定與共同回填的保證，查[完備性證明](four_color_completeness.md)中的完整關係、
可靠傳播與無資源限制前提；各欄非空、各表非空或兩兩相容不足以保證共同解，
相關反例與接口條件見[保證與缺口](four_color_guarantee_gap.md)及[接口語義](four_color_mathematical_model.md)。

`limit` 表示未判定；指定顏色下的無解只否定該條件的延伸。
紙證、Lean核心與Python實作的對應範圍由[數學模型](four_color_mathematical_model.md)說明；
各方法的成本與退步例由[橫向比較](four_color_method_comparison.md)及原報告維護。

平面結構的目標、未解義務與第一個研究工作見[4CT研究契約](4ct_guide.md#精確消元主線的研究契約)；
六邊來源與七邊前沿見[邊割報告](four_color_six_cut_exclusion.md)。

<a id="近期里程碑"></a>

流程與表示的演進可由上述來源的日期、後續連結及[既有發布紀錄](history/2026-10-29-four-color-progress-publication.md)追查。

## 使用與重播

只讀測試不重建已保存的實驗記錄：

```bash
python3 -m unittest discover -s tools/tests -p 'test_four_color*.py' -v
```

各專題中的 13、25、80 等測試數是當輪紀錄；目前總數以這次命令的實際輸出為準。
歷史驗證檔的來源 hash 可能屬於當輪版本，須對照同輪來源快照，不能當成目前程式 hash。

下列命令產生新檔；請在專案根目錄執行。`demo`、各種 experiment／audit 的預設輸出
會寫入既有 `artifacts/`，可能覆寫保存結果；重播時明確指定新的 `--out` 或 `--out-dir`。
最新有限比較可沿用凍結輸入，在新目錄重播：

```bash
python3 scripts/four_color_lab.py demo --out /tmp/four-color-demo-replay
python3 scripts/four_color_lab.py solve graph.json --engine constraints --intersections --cycles --cycle-contexts --joint-constraints --json /tmp/four-color-result.json --html /tmp/four-color-replay.html
python3 scripts/four_color_joint_propagation_experiment.py --out-dir /tmp/four-color-joint-replay
```

命令列啟用 `--c5` 時預設 `--c5-method structure`；Python API 的 `c5_method` 預設仍是 `table`。
共同條件接口需要同時啟用交集及原環閉合；這些選項不取代保留原邊及最後的完整驗證。
