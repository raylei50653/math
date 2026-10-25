# 四色求解與共同約束實驗導覽

## 最新進度

現況核對：2026-10-25。這是獨立有限圖演算法實驗；研究線排程以 [HANDOFF](HANDOFF.md) 為準。

| 欄位 | 現況 |
| --- | --- |
| 階段／生命週期 | 已完成下列有限實作及比較；九點缺口已補上，一般跨區傳播完備性仍未解。 |
| 最近研究更新 | 2026-10-25：[自動找型與主傳播](four_color_joint_propagation.md)在首次消元前產出 `(0,6,9)` 三點等色表。 |
| 上次完成 | 30份條件／兩模式60份完整執行；全部3,168份原邊解記錄保留，未固定主例48／48；異色固定例4→0次消元。 |
| 目前停止點 | 局部表、完整共同接口交集及條件原環都非空，仍不保證整圖有共同延伸；見[精確停止點](#精確停止點)。 |
| 下一步 | 已登記九點型的自動找型與主傳播已接入；其他構型、受限搜尋優化與一般條件關係學習仍待選定。 |
| 接手入口 | [約束語義](four_color_constraints.md)、[數學保障](four_color_cycle_contexts.md#數學保障範圍)、[保證與缺口](four_color_guarantee_gap.md)、[重播](#使用與重播)。 |

### 近期里程碑

| 日期／階段 | 進展與來源 |
| --- | --- |
| 2026-10-25／兩種引擎 | [逐點試色](four_color_lab.md)與[完整關係消元](four_color_constraints.md)建立原圖追蹤及倒序回填。 |
| 2026-10-25／五環與衝突 | [C₅結構](four_color_c5_structure.md)及[衝突子型](four_color_conflicts.md)保留字面框與原邊。 |
| 2026-10-25／跨區交集 | [共同接口](four_color_intersections.md)傳過[長鏈與分支](four_color_larger_structures.md)，長奇環仍有缺口。 |
| 2026-10-25／原環閉合 | [共同傳播](four_color_combined_cycles.md)識別該批十一無解例；[新反例](four_color_guarantee_gap.md)否定一般保證。 |
| 2026-10-25／共同條件與構型限制 | [條件接口](four_color_cycle_contexts.md)及[部分輻條](four_color_partial_spokes.md)補上十二／九點提前判否；[共同限制登記](four_color_joint_constraints.md)與[自動找型](four_color_joint_propagation.md)接入三點等色表。 |

下表依問題列出權威報告；各報告保留當輪數字、來源快照及歷史模式，不以後續版本改寫。

## 目標與範圍

目標是在同一份有限簡單無向原圖、同一組固定色與字面色號 0–3 下，找出一份合法完整染色，
或在精確窮盡／空關係時判定該固定色沒有延伸。求解器不假定輸入平面；平面樣本另作平面性核對。
每份成功結果都逐原邊、逐固定色驗證；多解可以保留，最後只需回填一份共同見證。

目前優先比較回填前排除不相容組合的能力、矛盾前的消元數，以及全部合法解或指定見證的保留範圍。
早期效能比較仍是所測樣本的歷史量測；不同引擎的試色次數與關係檢查次數不能直接當速度比例。

## 報告與證據入口

| 問題／方法 | 權威報告 | 當前適用範圍 |
| --- | --- | --- |
| 選點、唯一色強迫、回退與原圖衝突追蹤 | [四色實驗](four_color_lab.md) | 完整搜尋、分支失敗與固定色無延伸分開。 |
| 完整聯合關係消元及倒序回填 | [約束引擎](four_color_constraints.md) | 全部消元成功可構造共同見證；表格可能指數成長。 |
| 240 列索引、無弦五環與有界找環 | [C₅ 推導與查表](four_color_c5.md) | 掃描截斷只略過可選推理，不代表沒有五環。 |
| 已知充分矛盾子型及完整星形 fibres | [衝突子型](four_color_conflicts.md) | 核對原子圖與當前候選域；沒有一般衝突分類。 |
| 五環雙向支援、唯一逃逸、雙中心等色 | [C₅ 結構自約束](four_color_c5_structure.md) | 精確局部支援；等色因子仍與全部原約束共同使用。 |
| 接口接合、16 狀態原環與低階投影反例 | [局部資訊外推](four_color_local_information.md) | 完整 separator 契約可接合；全部三點投影一般不足。 |
| 共同接口整列交集及衝突優先控制 | [交集傳播](four_color_intersections.md) | 保留多列，不混接各欄的不同見證。 |
| 長鏈、分支、長環及固定色三角剖分 | [較大原圖](four_color_larger_structures.md) | 三十六份具名條件；結構投影與隨機指定見證分開核對。 |
| 交集與同一原環反覆回饋 | [共同傳播](four_color_combined_cycles.md) | 三十六份條件、三模式；有界基本環搜尋不等於全部環。 |
| 穩定未衝突的反例與完整消元保證 | [保證與缺口](four_color_guarantee_gap.md) | 十二點奇輪及九點固定色反例；樹證書尚未實作輸出。 |
| 同一中心條件、二／三元接口與回饋 | [共同條件接口](four_color_cycle_contexts.md) | 一般解保留及任意長中心環的局部精確性；四十例與九點缺口另列。 |
| 搜尋部分原輻條、跨區接口回饋 | [部分輻條搜尋](four_color_partial_spokes.md) | 九點4→0次消元；四十例有10份工作超限，沒有一般完備性或加速保證。 |
| 構型需處理的共同關係 | [九點共同限制登記](four_color_joint_constraints.md) | 21條必要原邊推出 `u=v=h`；三元完整fibres與當輪手動映射原型，後續接入見自動找型報告。 |
| 自動辨識與共同限制主傳播 | [九點自動找型](four_color_joint_propagation.md) | 消元前輸出三點等色表；30份條件60次完整執行、全部原邊解保留；具名有界搜尋，無一般完備性保證。 |

## 精確停止點

傳播穩定、每點候選非空、每張表非空及兩兩共同接口一致，均不等於整份共同關係非空。
原環支援保留同一首點色；條件原環再保留同一中心色，仍只把必要的二／三元投影交回交集，
不能據此任選各點支援，或宣稱任意多表網路在消元前都可判定。

[數學保障](four_color_cycle_contexts.md#數學保障範圍)適用任意有限簡單無向圖的全部解保留，
以及已完成查詢的任意長度中心環；共同三色域奇輪的排除可推至任意奇數環長。
零消元須在首次消元前命中並完成查詢，現有有界搜尋不保證此事。
九點缺口是歷史鄰域搜尋的界線，部分輻條模式已補上這份固定色判否；它不是二／三元因子無法表達問題的證明。
非空若要保證共同解，仍須完整消元成功、單例驗證或符合完整樹形接合條件。

另已登記九點構型的 `(0,6,9)` 三點等色必要因子，並由[自動找型](four_color_joint_propagation.md)
核對21條必要原邊，在首次消元前加入主傳播。它在較大目標圖中是必要限制，
裸構型的非空fibres不能自行保證滿足目標圖外側附件。

最新可選部分輻條模式將十二點奇輪及九點固定色反例都提前至零次消元；歷史鄰域模式的九點例仍需四次。
確切原圖、固定色、完整記錄與獨立參考見[最新結果](four_color_partial_spokes.md#驗證結果)。
求解器在完整精確消元全部成功、未遇工作或儲存限制後，由保存的回填表構造一份共同染色。
`limit` 始終是未判定；有固定色時，`unsatisfiable` 只否定該固定色延伸。

完整關係消元的等價性與接合論證是紙面說明，有限測試核對 Python 實作；沒有新增 Lean 定理。
這批實驗不改變 C₅／W7／J1／J2 的原來源排除、來源覆蓋或 P1–P4 停止點，
也沒有一般固定大小接口、普遍免消元完成或一般加速保證。

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
