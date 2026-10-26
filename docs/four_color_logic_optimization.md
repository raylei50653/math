# 四色消元的完整因子前綴剪枝

2026-10-26。接續[流程優化](four_color_flow_optimization.md)及[RAM索引](four_color_ram_indexes.md)，
本輪比較消元的邏輯流程：在一張因子的全部座標已確定時立即核對其完整列，提前排除
不可能延伸的候選前綴。新增可選 `--bucket-method prefix`，預設仍為 `anchor`。
所屬研究線見[四色實驗導覽](four_color_guide.md)。

## 改動與全解保留

舊流程選一張完整因子作起點，補齊所有未覆蓋座標後，才依序核對其他因子。
前綴流程保留同一個起點、補點順序與每點的全部候選色；每張因子在其最後一個所需
座標補齊時核對一次。若完整列不在該因子中，後面補任何色都無法修復這份前綴，
因此略過整個後綴。已通過的因子不需在每個葉節點重查。

例如已補齊 `a,b` 且完整因子要求 `a≠b`，遇到 `a=b` 就不必展開後面的 `c,d`。
這只否定該前綴，其他前綴仍全部枚舉；不是提前選定一份原圖染色。

對任一原桶合法完整指派，其起點列必存在，每個已補前綴的完整因子也必成立，
故不會被剪掉。反向而言，每份到達葉節點的指派都已通過桶內所有完整因子。
補點順序固定且各色恰遍歷一次，合法完整指派不重複；最後仍按完整邊界分組，
保存被消去點的全部可用色。兩流程因此計算同一份完整自然連接及全部 fibres。

`input_relations`、`source_domains`、有序邊界、原邊來源與字面色框保留；域內未列出的
邊界仍是空 fibre。沒有改動消元選點、傳播規則、最後倒序回寫或原邊／固定色驗證。
顯式深度迭代避免 Python 遞迴深度限制，不保存所有中間組合。完整表及紀錄預檢成功後
才提交消元記錄；工作或儲存中斷不發布半份 fibres，也不提前寫色。

## 同四十例比較

沿用原四十份凍結原圖及固定色，同樣開啟交集、原環、部分輻條共同條件與RAM索引，
每例工作五百萬次、完整生成表／紀錄各百萬列，完整事件紀錄啟用。

| 流程 | 可解／無解／超限 | 總工作檢查 |
| --- | ---: | ---: |
| 原完整候選枚舉 | 27／13／0 | 11,968,026 |
| 完整因子前綴剪枝 | 27／13／0 | 10,433,208 |
| 逐因子完整接合原型 | 27／13／0 | 10,926,701 |

前綴剪枝總檢查少12.82%；22例減少、13例相同、5例略增，沒有一般加速保證。
100點 `random_triangulation_n100_seed1_compatible` 由2,705,961降為2,098,063次，少22.47%。
試驗也實作了以完整共同接口逐因子接合的串流原型；雖然減少工作計數，本次單輪
求解合計14.13秒，高於基準13.86秒；前綴原型為12.66秒。
這些時間是選型時同環境的單次觀察，不能當穩定速度比例。逐表接合保留為實驗來源，
沒有接入主程式；正式兩模式的量測另存於各自 `timings.json`。

三種原型的四十份完整輸出，只排除頂層及各事件中的 `checks`、`candidate_checks`、
`relation_checks` 後，逐份完全相同。正式API另新增 `bucket_method` 欄位；對照器在
排除該欄前確認每份 report 和完整結果實際使用指定模式，避免兩次誤跑同一模式。
因此相同的不只有判定，還包含每步候選域、事件順序及說明、因果原邊、所有消元
輸入表、全部回填選項、空 fibre 語義、最後色號與其他統計。

獨立參考仍分層：4份缺口控制核全部原邊解，24份結構圖核完整全域投影，12份隨機圖
核原指定合法見證或凍結窮盡無解參考；沒有宣稱枚舉全部隨機圖解。

## 新圖與中斷核對

另以不使用求解器驗證函式的獨立程式，枚舉164份新圖的原邊解，包括全部64份四點圖、
各自的固定色／非連續ID版本、32份六點隨機圖，以及空圖、孤立點、K₅、K₆。
每圖跑純因子及共同傳播兩配置，每版本328次，均294可解／34無解。

每版本核對1,279份消元紀錄、54,421份完整桶指派與14,891個邊界 fibres，
其中6,620個是空 fibre；164份原圖合計23,050份原邊合法解全部保留。
三版本的完整語義輸出及消元紀錄逐份相同。前綴版另核小四環250個工作預算及71個
儲存容量，沒有提前寫色或半份紀錄；逐表接合版亦核292個工作預算與71個儲存容量。
正式模式的回歸測試另涵蓋所測小四環的全部工作預算及儲存容量切點、字面色框、CLI與比較器負控制。
242項相關測試通過。正式正常／seed-17兩次重播的80份完整gzip結果逐位元組一致，
7份metadata的完整JSON相同；時間與執行log不納入確定性比較。49份最終來源逐份核對，
正式兩模式80份結果各自與凍結原型完全相同，只有新增模式欄位。

`candidate_checks` 在前綴模式計實際嘗試的部分延伸，而非只計完整葉候選。
故工作統計的操作單位有明確區別，不能把兩模式的候選數直接當速度比例。
在相同的小工作預算下，中斷位置及是否完成可能不同；`limit` 仍只表示未判定。
所有完成消元與回寫的數學結論保持；消元前一般傳播完備性、固定資源內一般保證、
C₅／W7來源排除及Lean狀態沒有因此改變。

## 使用與證據

```bash
python3 scripts/four_color_lab.py solve graph.json --engine constraints --bucket-method prefix --intersections --cycles --cycle-contexts --cycle-context-search partial --interface-cache --max-checks 5000000 --max-table-rows 1000000 --json /tmp/four-color-prefix.json
uv run --with-requirements requirements.txt python scripts/four_color_logic_experiment.py --out-dir /tmp/four-color-logic-replay
python3 -m unittest discover -s tools/tests -p 'test_four_color*.py'
```

實驗輸出目錄必須是新路徑；不覆寫舊證據。可重複 `--case NAME` 選子集，收據依實際
選取的案例群記錄覆蓋。Python API 用 `solve_constraints(..., bucket_method="prefix")`。

- [正式模式比較](../artifacts/four_color_logic_optimization/comparison/comparison.json)：完整語義摘要及逐例雜湊；各模式 report 指向完整gzip紀錄。
- [選型實驗](../artifacts/four_color_logic_optimization/exploration.json)：原枚舉、前綴與逐表接合的結果、工作、時間及來源雜湊；三份凍結程式保留在同目錄的 `exploration-sources`。
- [獨立核對收據](../artifacts/four_color_logic_optimization/independent-checks/receipt.json)及[重播程式](../artifacts/four_color_logic_optimization/independent-checks/check_independent.py)。
- [相關測試](../artifacts/four_color_logic_optimization/tests.log)、[來源與重播核對](../artifacts/four_color_logic_optimization/verification.json)。
- [文件檢查](../artifacts/four_color_logic_optimization/docs-check.log)及[正式docs DocGraph](../artifacts/four_color_logic_optimization/docgraph-docs.log)。

兩份較大的report摘要只移除JSON空白以保存，所有欄位保持，轉換雜湊見
[儲存格式收據](../artifacts/four_color_logic_optimization/archive-format.json)；完整gzip結果未改動。

2026-10-26發布核對：本報告的 `final-source` 是採用無損mask前的凍結版本；
`verify_replay.py` 會要求工作樹來源等於該版本，並寫入歷史收據，不能作目前工作樹的只讀checker。
後續無損表示的完整輸出相等性見[回填壓縮報告](four_color_retention.md)，
本次來源／完整紀錄的只讀核對入口見[發布紀錄](history/2026-10-26-four-color-prefix-retention-publish.md)。

有限實驗驗證實作，前綴排除的全解保留來自上述完整因子論證；這不是一般效率定理或整份Python形式化證明。
