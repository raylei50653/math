# 四色求解以記憶體索引換取速度

2026-10-25。接續[儲存容量比較](four_color_memory_optimization.md)，所屬研究線見
[四色實驗導覽](../four_color_guide.md)。使用者澄清要讓演算法一次保留更多資料以換取速度；
上一輪增加完整紀錄容量只處理人為上限，沒有完成此項時間／記憶體取捨。

## 實驗前登記

目前同四十例、百萬列容量、每例五百萬次工作上限全部完成。16,954,720次檢查中，
完整接口交集占41.12%，共同條件查詢占31.46%。兩表revision快取已存在，但一張未變更的
完整表對不同鄰表交集時，仍會重新投影及掃描全部列。

本輪候選是保留實際可重用的記憶體索引：依同一因子身份、revision及**完整有序共同接口**，
保存「共同色組 → 原完整列引用」及完整投影。後續交集重用索引，只取回存活群組的完整列；
不把三元以上共同關係拆成獨立二元或單點支援。可同時保留多張表、多個接口的索引，
另設可重算快取的容量；滿額時淘汰或回到原查詢，不藉此判定無解。

索引完成後才發布；因子列revision變更或退休即失效。對實際索引建立、查詢與取回完整列
逐次計費，未完成查詢不提交部分篩選。原輸入、完整fibres、空列、全部回填色及原邊來源保留。
若共同條件的冗餘查詢仍是瓶頸，可再用記憶體scope索引排除不可能涵蓋接口的因子。
另保留穩定有序配對陣列及因子引用，避免每輪重排配對及重找物件身份；仍逐配對核對
兩個revision，依原順序重查，不能因早期快取命中漏掉稍後修改的關係。

比較快取關閉／開啟，兩者均採同四十份凍結原圖／固定色、百萬列紀錄容量、五百萬次工作，
原推理選項及獨立驗證不變。每份圖／每個模式用獨立新程序依次量測時間與求解後峰值RSS，
另記驗證及完整輸出後的峰值。記錄實際快取條目／完整列引用數，不能只憑容量數值宣稱吃了RAM。
先以幾份已知較貴案例核對，再比較整批；正常／seed-17的確定性記錄另作重播比較。

## 結果與停止點

本輪實作三份保留於RAM的資料：完整接口分組索引、涵蓋因子的scope索引，以及依原次序
排列的因子配對陣列。配對檢查直接讀取兩個因子的當前revision；共同條件只掃描真正
涵蓋完整接口的候選因子。所有候選仍逐完整原列核對，沒有以索引非空推成全圖有解。

同四十份凍結原圖／固定色，兩模式均使用五百萬次工作、百萬列完整紀錄容量，只有RAM
索引模式不同；每例／每模式均在獨立新程序依次執行：

| 同批四十例 | 關閉RAM索引 | 開啟RAM索引 |
| --- | ---: | ---: |
| 合法完整染色／固定色無延伸／超限 | 27／13／0 | 27／13／0 |
| 總工作檢查 | 16,954,720 | 11,968,026 |
| 求解秒數合計 | 15.2653 | 12.8173 |
| 含啟動、獨立核對及輸出的程序秒數合計 | 39.7278 | 37.3278 |
| 最大求解後程序峰值RSS | 103.6 MiB | 106.2 MiB |
| 最大驗證與序列化後程序峰值RSS | 223.9 MiB | 227.2 MiB |

本次求解耗時少16.04%，檢查少29.41%；兩種容量／工作上限相同，收益來自實際索引重用。
這是單次同環境有限比較；34例求解較快，6份很快判否的案例各慢約0.1–0.4毫秒，
不聲稱所有輸入都更快。RSS是程序生命期高水位，含載入來源、輸入及參考，不是單獨
求解器配置量；較晚的峰值還含獨立驗證、完整JSON與gzip輸出。

快取有164,795次命中、55,205份完整索引建立；單次求解最多同時保留156,305份原完整列引用。
本批未達一百萬列引用的快取上限，沒有容量淘汰。這些是實際存入RAM的可重用資料，
不是只增加允許的列數；群組引用既有不可變完整列，未額外複製其顏色資料。

## 實作、正確性與驗證

新增 `use_interface_cache=True`／CLI `--interface-cache`，需同時啟用完整接口交集。
`interface_cache_max_rows`／`--interface-cache-max-rows`控制保留的完整列引用數，預設一百萬；
它與生成表／完整證書的 `max_table_rows` 是不同預算。未開啟時保留原查詢路徑。
快取以LRU淘汰完整索引；單份索引過大則改用原完整投影／過濾，仍可精確求解。

每份快取只屬於同一次求解的同一因子身份、revision及完整有序接口。分組保留全部私有
座標；完整共同色組交集後，只取回被保留群組的原完整列。三元parity負控制仍可判出
所有二元投影看不出的矛盾。來源身份／revision改變或因子退休時清除索引，避免歷史列誤用。
索引建立中斷不發布半份索引，因子篩選中斷不改輸入表；共同條件新增因子與涵蓋索引
均先完成預算預檢，才共同提交域／因子變更。未固定點仍等全部精確消元成功才寫色。

兩模式四十例的完整消元紀錄逐份相同，包含完整候選域、輸入關係、全部非空fibres與
空列語義；最終色、候選域及原圖也相同。與上一輪同四十例比較，關閉模式的舊統計
全部保持，兩模式的上述完整關係／最終色亦與前輪一致。原四份原邊窮盡控制、二十四份
結構圖全域投影及十二份隨機圖的指定見證／凍結窮盡無解參考均通過，不擴大隨機解覆蓋。

233項相關測試全通過，含新增20項RAM索引／配對順序／版本失效／淘汰與過大退回／中斷原子性／
API與CLI回歸。正常／seed-17各執行80個獨立程序，323份確定性資料逐位元組一致；
時間、RSS及執行log不納入此比較。基準46份及最終47份來源逐一核對hash並保存快照。
文件連結／導覽及正式`docs/` DocGraph通過；全工作樹DocGraph另報72項歷史快照的重複ID，
保留失敗紀錄，不混稱全域通過。

## 證據與重播

- [凍結四十例](../../../artifacts/four_color_ram_indexes/inputs.json)、[基準來源清單](../../../artifacts/four_color_ram_indexes/baseline-manifest.json)。
- [完整關／開比較](../../../artifacts/four_color_ram_indexes/comparison/report.json)、[獨立程序時間與RSS](../../../artifacts/four_color_ram_indexes/comparison/timings.json)、[執行紀錄](../../../artifacts/four_color_ram_indexes/comparison.log)。
- [完整回歸測試紀錄](../../../artifacts/four_color_ram_indexes/tests.log)、[來源／完整fibres／重播核對收據](../../../artifacts/four_color_ram_indexes/verification.json)。每例的`worker_report`及`full_record`指向該獨立程序的全部核對與完整gzip記錄；來源快照保留於證據根目錄的`baseline-source`／`optimized-source`。
- [文件檢查](../../../artifacts/four_color_ram_indexes/docs-check.log)、[正式DocGraph](../../../artifacts/four_color_ram_indexes/docgraph-docs.log)、[全樹DocGraph失敗紀錄](../../../artifacts/four_color_ram_indexes/docgraph-whole-tree.log)。

在既有原圖上使用：

```bash
python3 scripts/four_color_lab.py solve graph.json --engine constraints --intersections --cycles --cycle-contexts --cycle-context-search partial --interface-cache --max-checks 5000000 --max-table-rows 1000000 --json /tmp/four-color-indexed-result.json
```

重播使用新目錄，保留前輪證據：

```bash
uv run --with-requirements requirements.txt python scripts/four_color_memory_experiment.py --out-dir /tmp/four-color-ram-replay --inputs artifacts/four_color_ram_indexes/inputs.json --row-limits 1000000 --cache-modes off on
PYTHONHASHSEED=17 uv run --with-requirements requirements.txt python scripts/four_color_memory_experiment.py --out-dir /tmp/four-color-ram-seed17-replay --inputs artifacts/four_color_ram_indexes/inputs.json --row-limits 1000000 --cache-modes off on
python3 -m unittest discover -s tools/tests -p 'test_four_color*.py'
```

有限圖結果不推成一般效率或傳播完備性，其他C₅／W7停止點不變；沒有新增Lean定理。
