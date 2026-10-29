# 四色求解流程的增量傳播優化

2026-10-25。接續[部分輻條搜尋](four_color_partial_spokes.md)及
[九點自動找型](four_color_joint_propagation.md)。所屬研究線見
[四色實驗導覽](four_color_guide.md)。

2026-10-25後續：[利用額外記憶體](four_color_memory_optimization.md)新增可設的列數容量，
同四十例在百萬列容量下全部完成。本頁保留原十萬列上限的比較與停止點。
2026-10-27後續：[變動接口與完整支援重用](four_color_delta_propagation.md)
新增可選delta傳播；固定40例完整輸出相等，原排程總檢查少1.60%、實測時間少8.92%。

## 實驗前登記

目標是降低同一原圖、同一字面固定色條件下的重複工作，不提高工作／儲存上限，
不以局部關係非空替代完整消元及原邊驗證。此前部分輻條四十例中的十份 `limit`
合計五千萬次檢查，其中 44,093,684 次為接口交集；單例占 84.09%–93.00%。
原流程每次消元重新建立接口配對並丟棄兩表 revision 快取，未變更關係也重算。

預先採用的候選改動：

1. 以同一次求解內的穩定關係身份及 revision 保存完整共同接口的查詢結果。
   因子新增／退休只更新相關配對；關係列改變時才重新查詢。
2. 若仍有必要，按關係 revision 及完整局部候選域避免重複的一元支援過濾；
   所有更動仍保留原邊來源及完整聯合列。

量測沿用前輪四十份凍結原圖／固定色與每圖 5,000,000 次檢查、100,000 列儲存上限，
開啟交集、原環、部分輻條共同條件；不額外啟用九點找型或已知衝突捷徑。
先保存本輪改動前的來源，再比較工作次數、交集次數、結果及消元數；牆鐘時間另列，
不以時間取代工作量或正確性證據。不得覆寫前輪證據。

核對範圍沿用四份缺口／控制的全部原邊解、二十四份結構例的完整全域投影，
以及十二份隨機例的指定合法見證／凍結窮盡無解參考。另以小圖獨立原邊枚舉
核對快取失效、關係新增／退休、重標號與超限中斷；不把隨機指定見證擴大為全部解。

## 結果與停止點

第一階段增量傳播已沿用四十例完成比較：原 17 可解／13 無解／10 超限，改後
26 可解／13 無解／1 超限；總檢查 84,859,273 → 30,090,655。全部完成判定與
獨立參考一致，沒有記錄截斷或全域投影核對超限。此階段證據另存，不覆寫。

### 第二階段實驗前登記

僅餘 `random_triangulation_n100_seed1_compatible`，已由消元 12 點推進至 79 點，
但仍達五百萬次上限。新增候選改動：消元時選一張完整因子作起點，枚舉它的全部列，
再只補齊它未覆蓋的邊界座標，逐一核對其餘全部桶內因子；不先選定任何實際點色。
以 `因子列數 × 未覆蓋座標的候選域大小乘積` 選擇較小的起點，並為實際列訪問、
完整候選及關係查詢計費。每份滿足原桶的完整指派恰有一份起點列，故不省略任何解；
最後按完整邊界分組保存被消去點的全部色，空 fibre 語義不變。空桶保留自由點分支。

再次使用同四十例、同工作／儲存上限及原獨立參考，另核對小圖全部消元輸入表的完整
fibres、原邊解、孤立點及中斷。結果如下。

## 最終比較

三模式均使用同一批四十份原圖與字面固定色，每例工作上限五百萬、生成表及完整紀錄
各沿用十萬列上限；同樣開啟交集、原環及部分輻條，不啟用額外九點找型或衝突捷徑。

| 同批四十例 | 改動前 | 僅增量傳播 | 加完整因子起點枚舉 |
| --- | ---: | ---: | ---: |
| 合法完整染色 | 17 | 26 | 26 |
| 固定色無延伸 | 13 | 13 | 13 |
| 未判定 `limit` | 10 | 1 | 1 |
| 總工作檢查 | 84,859,273 | 30,090,655 | 16,934,922 |
| 接口交集檢查 | 71,697,624 | 6,256,723 | 6,965,165 |
| 本次求解牆鐘秒數 | 41.4163 | 18.8728 | 16.1621 |

總工作減少 80.04%；牆鐘時間為同環境依次執行的單次觀察，不提供一般效能保證。
最終模式的接口工作高於中間模式，是剩餘原圖多完成十次消元與新的關係過濾，
不是相同前綴重查變多。這些總數包含超限前工作，不將超限當作無解。
原先三十份完成案例全部保持同判定；九份原超限案例取得逐原邊與固定色核對的合法染色。

唯一未完成例仍為 `random_triangulation_n100_seed1_compatible`（100點、294邊）：
改動前在12次消元／五百萬檢查停止；最終在89次消元／3,504,472次檢查停止，
原因改為完整紀錄下一份快照將超過100,000列，當時已提交96,271列紀錄。
它有前輪獨立合法見證；本輪完整紀錄模式仍只回傳 `limit`，沒有新增點色或可解證書。

## 正確性、驗證與來源

完整原圖與固定色 hash 均未變。四份缺口／控制保存原邊獨立窮盡的0／6／90／0解；
二十四份結構例核對全部全域解在每份已保存關係及回填選項的投影；十二份隨機例仍只
保留十份指定合法見證或兩份凍結窮盡無解參考，沒有擴大成隨機圖全部解枚舉。
三模式所有完成判定均符合獨立參考，無事件截斷或投影核對超限。

增量索引按完整共享座標建立配對，只在因子身份或revision變更時重算。普通因子快取
另核對完整局部域，只有完整過濾及支援投影後才提交。退休因子移除快取引用。
共同接口始終使用整列，不把三元以上關係拆成獨立二元支援。

精確桶枚舉仍處理全部含消去點的輸入因子。任一滿足桶的完整指派必唯一限制到一份
起點列與未覆蓋邊界延伸；反之，只有通過其餘全部因子的指派才加入輸出。
按完整邊界保存全部消去點色，因此保有原完整自然連接、全部fibres及空列語義。
自由點的空桶保留全部可用色；工作或紀錄超限不提交半份消元記錄，也不提前寫色。

新增回歸包含同revision新因子、配對位置移動、後續刪列喚醒前配對、退休引用釋放、
三元parity負控制、索引中斷恢復；另以完整笛卡兒定義核每份小圖桶的所有fibres與空列，
核固定／自由孤立點、非連續原ID與反向色框、K5桶矛盾，以及小四環的全部241個中斷預算。
完整測試與重播核對收據見下列證據；有限Python驗證不等於整份實作形式化驗證。

206項相關測試全通過。正常／seed-17的輸入、來源清單、摘要及四十份gzip記錄共43檔
逐位元組一致，牆鐘時間另存並排除於此比較。最終43份依賴來源逐份核對hash並保存快照；
原基準41份及中間模式42份來源亦保留。新驅動程式的hash另列於收據。

文件連結／導覽檢查與正式`docs/` DocGraph通過；全工作樹DocGraph另報72項歷史快照的
重複ID，保持失敗紀錄，不混稱全域通過。這些檢查不裁決算法完備性或數學排除。

證據入口：

- [凍結原四十例](../artifacts/four_color_flow_optimization/prior-inputs.json)、[改動前來源清單](../artifacts/four_color_flow_optimization/baseline-manifest.json)。
- [改動前完整比較](../artifacts/four_color_flow_optimization/baseline/report.json)、[增量傳播比較](../artifacts/four_color_flow_optimization/incremental/report.json)、[最終比較](../artifacts/four_color_flow_optimization/optimized/report.json)。
- [改動前時間](../artifacts/four_color_flow_optimization/baseline/timings.json)、[最終時間](../artifacts/four_color_flow_optimization/optimized/timings.json)另存，不納入逐位元組重播比較。
- [完整回歸紀錄](../artifacts/four_color_flow_optimization/tests.log)、[來源／重播／比較核對收據](../artifacts/four_color_flow_optimization/verification.json)。各份比較的`full_record`列出完整gzip記錄的相對路徑；來源快照位於證據根目錄的`baseline-source`／`incremental-source`／`optimized-source`。
- [文件檢查](../artifacts/four_color_flow_optimization/docs-check.log)、[正式DocGraph](../artifacts/four_color_flow_optimization/docgraph-docs.log)、[全樹DocGraph失敗紀錄](../artifacts/four_color_flow_optimization/docgraph-whole-tree.log)。

## 重播與停止點

本頁保存各階段的凍結來源與結果。下列命令預設使用目前driver，核對目前行為；
若要逐位元組重現歷史報告，須在新的暫存重播根目錄配置對應階段的來源與當輪driver。
driver以自身位置決定專案根目錄，不能只切換solver而沿用錯輪driver來宣稱歷史重播。

在新的輸出目錄執行，保留既有證據：

```bash
uv run --with-requirements requirements.txt python scripts/four_color_flow_experiment.py --solver-source artifacts/four_color_flow_optimization/baseline-source/scripts --out-dir /tmp/four-color-flow-baseline-replay
uv run --with-requirements requirements.txt python scripts/four_color_flow_experiment.py --out-dir /tmp/four-color-flow-optimized-replay
PYTHONHASHSEED=17 uv run --with-requirements requirements.txt python scripts/four_color_flow_experiment.py --out-dir /tmp/four-color-flow-seed17-replay
python3 -m unittest discover -s tools/tests -p 'test_four_color*.py'
```

演算法優化隨現有約束引擎生效，沒有更改原推理選項的預設開關或主工作／儲存上限。
下一個窄問題是最後一例的完整紀錄儲存成本；本輪不提高上限、不改證書格式，
不將省略公開完整快照當作相同核對條件下完成。一般傳播完備性、一般效率保證及
其他 C₅／W7 研究線的停止點均保持原狀；沒有新增Lean定理或重跑Lean build。
