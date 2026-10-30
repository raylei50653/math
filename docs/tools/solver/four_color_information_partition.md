# 依當前訊息選擇工作區與消元順序

2026-10-27。接續[靜態分區比較](four_color_partition.md)：原圖割點／BFS不能反映
推理後的共同因子，本輪改用當前因子範圍、完整表列數與候選域，動態建立工作區。
三種模式皆已接入約束引擎，預設仍為 `none`。
**已消除本批靜態分區的超限，但尚未測到整體加速。** 最佳新模式總檢查少0.41%，
求解時間與表列數仍略增；不用這個結果宣稱已找到更快的通用分區。
本頁保留當輪分區比較；後續[傳播流程優化](four_color_delta_propagation.md)在固定同一分區下
重用完整支援與變動接口，information模式實測13.35→12.09秒，完整語義輸出相等。

[排程實作](../../../scripts/four_color_partition.py) ·
[完整比較](../../../artifacts/four_color_information_partition_final/comparison.json) ·
[測試](../../../tools/tests/test_four_color_partition.py)

## 實際使用的訊息

每次傳播穩定後，從**全部當前因子**建立變數相鄰圖：在同一因子範圍內的點互相連接。
對候選消元點v，令Uᵥ為全部相交因子的聯合範圍、Dₓ為目前候選色、R_f為完整因子表。
估計使用：

\[
A(v)=\min_{f\ni v}|R_f|\prod_{x\in U_v\setminus\operatorname{scope}(f)}|D_x|,
\qquad
W(v)=A(v)(1+\#\{f:v\in f\})+\sum_{f\ni v}|R_f|.
\]

無相交因子時，A(v)=|Dᵥ|。A是從一張完整起始表枚舉其餘座標的候選數上界；
W將因子數與讀表規模納入排序，**不是實際prefix工作、傳播工作或耗時的上界**。
這些值只作排程估計，不作存在性判定，不以單點域乘積代替共同關係。

| 選項 | 如何選擇下一點 |
| --- | --- |
| `adaptive` | 先限於當下全圖最小的「新增填邊數、接口點數」級別；優先留在目前工作區，再比A與輸入位置。 |
| `information` | 同一結構級別內，先選最小A，再優先目前工作區。 |
| `message` | 全圖先按W，再按新增填邊數與接口點數排序；不限制為全圖min-fill同級，最後才以工作區打破平手。 |

當區內沒有符合上述條件的候選點，就立即放棄繼續完成舊區，重新選種子點。
從種子沿**當前因子相鄰圖**擴張到最多 `partition_block_size` 點；每次加入使外部接口
候選域乘積最小的鄰點，再比較接口點數、與區內的連結數、A與輸入位置。
預設工作區大小12。區塊規劃不按原頂點標號大小，而按輸入位置打破平手。

這是允許中途換區的**重疊工作區排程**，不是承諾把整圖一次切成互不重疊且各自解完的區塊。
已消元點不再處理；未消元的區內點可進入新工作區。輸出 `partition_plan.regions`
保存每次規劃的成員與接口；`groups` 保存各區實際嘗試的點，超限最後一步可能尚未完成。
`decisions` 保存每步的選點、估計及當下全圖min-fill基準，可追蹤換區理由。

## 正確性與資源邊界

模式只改下一個消元點。核心仍合併全部含該點的因子、生成完整投影與所有fibres；
原邊、固定色、跨工作區因子與字面色框不變。代價估計錯誤最多導致效率退步，
不能刪除任何真解。每步消去一個原點，無資源限制且完整計算時依既有
[消元與共同回填契約](four_color_completeness.md)終止並精確判定。

前兩種模式只保證**當下狀態**的結構級別等於全圖min-fill最佳級別，
不保證後續軌跡、最大接口或整次成本等於原本執行。`message`更沒有這項逐步結構限制。
全部模式最後才回填；中斷不提交部分表，不將 `limit` 當無解。

規劃只讀域大小、因子範圍與列數，不枚舉表列。但它仍有實際CPU成本；
計時包含規劃，`checks`僅沿用原關係計算計費，未將這些排程操作算入。
`candidate_evaluations`另記各步被評估的候選點總數，並非全部規劃指令數。
一般速度改善、最佳分區、固定寬度及Python排程形式化驗證均未建立。

## 固定40例完整比較

同一份原圖與固定色、相同prefix枚舉及傳播選項，每例5,000,000工作、1,000,000表列，
工作區上限12；此次四個模式依次執行，測試程序在比較結束後才啟動。
耗時為本機單次觀察，未作重複量測或統計加速宣稱。

| 模式 | 完成／超限 | 總檢查 | 較原模式 | 累計產生表列 | 最大嘗試接口 | 求解秒數 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 原本 `none` | 40／0 | 10,433,208 | 基準 | 149,040 | 10 | 12.46 |
| `adaptive` | 40／0 | 10,391,990 | −0.40% | 152,211 | 10 | 13.27 |
| `information` | 40／0 | 10,390,284 | −0.41% | 151,632 | 10 | 12.80 |
| `message` | 40／0 | 10,751,514 | +3.05% | 161,022 | 13 | 13.75 |

全部均27份 `colored`、13份 `unsatisfiable`，各自符合原圖獨立參考。
前兩種模式各有12例少檢查、18例相同、10例增加；`message`為15／13／12例。
列數是累計生成表的指標，不當作RSS。各模式 `timings.json` 保留程序高水位RSS。

具名收益與退步都保留：

| 案例 | 原模式 | 新模式 | 差異 |
| --- | ---: | ---: | --- |
| `equality-chain-m4-overlap` | 105,074 | information 99,305 | 少5.49%。 |
| `random_triangulation_n100_seed1_compatible` | 2,098,063 | information 2,027,937 | 少3.34%。 |
| `equality-chain-m12-compatible` | 212,863 | information 223,554 | 增5.02%；上一輪靜態割點則500萬次超限。 |
| `random_triangulation_n100_seed0_trial` | 1,012,199 | message 930,744 | 少8.05%。 |
| `random_triangulation_n60_seed1_compatible` | 834,953 | message 993,868 | 增19.03%。 |

推論範圍：當前因子資訊足以讓分區避開上一輪的巨大接口，但局部訊息成本不代表
整次成本。W沒有預測消元後的新增因子、後續域傳播及重查成本；因此某一步便宜，
後面仍可能更貴。此三模式均未顯示足以替換預設的整體收益。

## 驗證與停止點

138份小圖條件×7種策略逐份核對原邊完整解集合，並逐桶用Cartesian定義核對全部fibres，
包含空列；四點圖全64種各兩份固定色條件，另10份帶不同標號的六點圖。
三個新模式各重用固定色、反向標號／完整色框、K₅空fibre、逐工作預算中斷測試；
所有策略另測兩種桶枚舉下的儲存中斷，不能提前寫色或提交部分表。

另測新跨區因子使舊區失去優先權時必須換區、完整表列數變化必須重估，
及動態CLI輸出的實際工作分組。全套四色測試357項通過。

40例×4模式均保留完整壓縮紀錄、原圖hash、來源快照與trace檢查。
4例核對所有原邊枚舉解；24例核對精確全域投影、無投影超限；
10例只核指定獨立見證，另2例用獨立無解參考。後12例不宣稱全解逐份核對。
不同消元順序的表與最後見證可不同，核對的是各自保留同一原圖語義。

目前完成的是三種依當前資訊排程的有限比較，保留原預設。
若接續，具體問題是估計**消元後的傳播成本**，並以新的獨立樣本驗證，
而不是只按當前訊息大小排序。本輪未做自動挑贏家、多步前瞻、區塊結果快取或平行求解。

## 使用與重播

```bash
python3 scripts/four_color_lab.py solve graph.json --engine constraints \
  --partition information --partition-block-size 12 --bucket-method prefix \
  --json result.json

uv run --with-requirements requirements.txt python scripts/four_color_partition_experiment.py \
  --out-dir /tmp/four-color-information-replay --strategies none adaptive information message

python3 -m unittest discover -s tools/tests -p 'test_four_color_partition.py' -v
```

API：`solve_constraints(graph, partition_strategy="information", partition_block_size=12)`。
比較目錄必須尚未存在。完整來源、壓縮紀錄及逐例保存範圍隨實驗輸出；
初試兩模式證據另保留於 `artifacts/four_color_information_partition/`。

本輪更新此權威報告、靜態分區接續入口、約束引擎、四色導覽與STATUS。
完整消元的任意合法次序契約不變；HANDOFF、4CT與D停止點沒有新結論。
