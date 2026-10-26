# 四色求解以額外記憶體保存完整關係

2026-10-25。接續[增量傳播與精確枚舉優化](four_color_flow_optimization.md)，所屬研究線見
[四色實驗導覽](four_color_guide.md)。使用者已授權利用額外記憶體；此前預算比較保留為歷史基準。

2026-10-25澄清後續：[RAM索引換速度](four_color_ram_indexes.md)處理實際保留中間索引以減少重算；
本頁只記儲存容量提高後完成最後一例，不能以此宣稱已實作時間／記憶體演算法取捨。

2026-10-26更新：[反例修復](four_color_guarantee_gap.md#2026-10-26修復與保留範圍)
將目前預設改為 `min(max_checks,1000000)`，顯式容量契約不變。
下文十萬列預設與量測保留為2026-10-25歷史記錄。

## 實驗前登記

上一輪僅餘 `random_triangulation_n100_seed1_compatible`：100點294邊，消元89點、
3,504,472次檢查後，下一份完整證書快照將超過100,000列，故回傳 `limit`。
這是列數預算，尚未量測實際峰值記憶體；不是作業系統已無可用RAM。

本輪將儲存預算獨立成API／CLI選項，未指定時維持原 `min(max_checks,100000)` 行為。
明確指定時可提高生成關係表及完整紀錄的列數預算，主工作上限仍為5,000,000次。
各預算分別計數，維持全部有序共同列、完整回填色、空fibres及原邊來源；不略過公開快照。
先比較100,000列與1,000,000列，後者是允許保存的容量，不預先配置百萬列。

先核對該剩餘例，再以原四十份凍結原圖／固定色比較兩種容量。每份圖、每個模式都用
新程序依次執行，量測求解前／後及驗證與序列化後的程序峰值RSS，避免先前案例的峰值混入。
RSS是程序生命期的高水位，含載入來源／輸入的成本，不當成求解器專用配置位元組；
牆鐘時間與RSS另存，確定性記錄仍作正常／seed-17逐位元組核對。

正確性沿用四份原邊窮盡控制、二十四份結構圖全域投影及十二份隨機圖的指定見證／
凍結窮盡無解參考，所有完成染色逐原邊及固定色核對。增加API／CLI預算及兩種超限的
回歸核對；保留舊預設、禁止以 `limit` 推成無解，未固定點在完整消元成功前不寫色。

## 結果與停止點

同四十份原圖／固定色、每例五百萬次工作上限，完整紀錄始終啟用。兩種儲存容量各執行
四十個獨立新程序，僅調整列數上限：

| 同批四十例 | 100,000列 | 1,000,000列 |
| --- | ---: | ---: |
| 合法完整染色 | 26 | 27 |
| 固定色無延伸 | 13 | 13 |
| 未判定 `limit` | 1 | 0 |
| 總工作檢查 | 16,934,922 | 16,954,720 |
| 本次求解秒數合計 | 14.9799 | 15.0877 |

額外19,798次工作用來完成原超限例的最後11次消元與回填；原本完成的39份判定保持不變。
所有40份完成判定均符合原獨立參考，全部合法輸出逐原邊與固定色核對通過。
兩模式均無事件截斷、無結構投影核對超限。

### 最後一例的實際記憶體

`random_triangulation_n100_seed1_compatible`，100點294邊：

| 同一原圖、同一固定色 | 100,000列 | 1,000,000列 |
| --- | ---: | ---: |
| 結果／成功消元 | `limit`／89點 | `colored`／100點 |
| 工作檢查 | 3,504,472 | 3,524,270 |
| 已提交生成表列 | 48,437 | 51,304 |
| 已提交完整紀錄列 | 96,271 | 108,004 |
| 求解後程序峰值RSS | 98.6 MiB | 103.6 MiB |
| 驗證及序列化後程序峰值RSS | 204.1 MiB | 223.4 MiB |
| 求解秒數 | 2.3862 | 2.4272 |

最終只實際保存108,004列完整紀錄；容量設為百萬列不會預先配置百萬列。
同一案例求解後峰值增加約5.0 MiB，連同完整驗證及gzip輸出後的峰值增加約19.3 MiB。
後者也是本次四十例的最大程序峰值。峰值包含來源載入、輸入與獨立參考；不是單獨
求解器物件的大小，也不是記憶體配額。列數與RAM位元組沒有固定換算，寬列會更昂貴。
本表是Linux新程序的一次量測；時間及RSS不提供一般效能保證。

## 使用方式與正確性

新增Python參數 `solve_constraints(..., max_table_rows=1_000_000)` 與CLI
`--max-table-rows 1000000`。只在約束引擎適用；搜尋引擎明確拒絕此參數。
未指定或使用 `None` 時仍採 `min(max_checks,TABLE_ROW_CEILING)`，預設為十萬列。
明確指定時獨立於工作次數，僅接受非負整數；零容量仍可安全回傳 `limit`。
累積生成表（含共同條件／九點表）與累積完整證書快照仍分別遵守該列數上限。

例如在已有原圖JSON上，以原五百萬次工作預算允許更多儲存：

```bash
python3 scripts/four_color_lab.py solve graph.json --engine constraints --intersections --cycles --cycle-contexts --cycle-context-search partial --max-checks 5000000 --max-table-rows 1000000 --json /tmp/four-color-memory-result.json
```

這次只改預算設定與量測，不改已有精確消元／回填規則，也不略去完整公開快照。
完整有序關係、每份邊界的全部回填色、空fibres、原邊及固定色均保留；兩種超限仍是未判定。
四份原邊獨立窮盡控制保留全部解，二十四份結構圖保留完整全域投影；十二份隨機圖仍僅
核十份指定合法見證或兩份凍結窮盡無解參考，不擴大成全部隨機解枚舉。

213項相關測試全通過，新增7項涵蓋預設相容、嚴格整數型別、零／精確容量邊界、
生成表與完整證書分別計數、主工作上限不變、完整fibres及CLI傳遞／錯誤用法。
十萬列模式的40份完整gzip記錄與前輪逐位元組一致；原39份已完成案例在兩種容量下
除儲存上限欄位外的完整求解記錄也完全相同。

正常／seed-17各執行80個獨立程序，輸入、清單、摘要與完整gzip等323檔逐位元組一致；
RSS／時間及執行log不納入此比較。基準44份及新版本46份來源逐一核對hash並保存快照。
文件連結／導覽檢查及正式`docs/` DocGraph通過；全工作樹DocGraph仍報72項歷史快照
重複ID，另存失敗紀錄，不混稱全域通過。

## 證據與重播

下列命令預設使用目前程式，核對目前行為；精確歷史重播須在新的暫存重播根目錄
配置當輪來源與driver。driver以自身位置決定專案根目錄；後續RAM索引版不應當成
本輪凍結產生器。既有證據的bytes與SHA保持原樣。

- [凍結原四十例](../artifacts/four_color_memory_optimization/inputs.json)、[改動前來源清單](../artifacts/four_color_memory_optimization/baseline-manifest.json)。
- [兩種容量完整比較](../artifacts/four_color_memory_optimization/comparison/report.json)、[獨立程序RSS與時間](../artifacts/four_color_memory_optimization/comparison/timings.json)、[執行進度](../artifacts/four_color_memory_optimization/comparison.log)。
- [完整回歸紀錄](../artifacts/four_color_memory_optimization/tests.log)、[來源／完整記錄／重播核對收據](../artifacts/four_color_memory_optimization/verification.json)。各案例的`worker_report`及`full_record`指向單一新程序的參考核對與完整gzip記錄；來源快照保留於證據根目錄的`baseline-source`與`optimized-source`。
- [文件檢查](../artifacts/four_color_memory_optimization/docs-check.log)、[正式DocGraph](../artifacts/four_color_memory_optimization/docgraph-docs.log)、[全樹DocGraph失敗紀錄](../artifacts/four_color_memory_optimization/docgraph-whole-tree.log)。

重播使用新的輸出目錄，避免改寫既有證據：

```bash
uv run --with-requirements requirements.txt python scripts/four_color_memory_experiment.py --out-dir /tmp/four-color-memory-replay
PYTHONHASHSEED=17 uv run --with-requirements requirements.txt python scripts/four_color_memory_experiment.py --out-dir /tmp/four-color-memory-seed17-replay
python3 -m unittest discover -s tools/tests -p 'test_four_color*.py'
```

本批四十例在提高儲存容量後全部完成，仍是固定有限輸入的實作核對。一般圖在固定
時間／記憶體內的完備保證、一般跨區傳播完備性與其他C₅／W7研究線不變；沒有新增Lean定理。
