# 2026-10-12 大型產物生成驗證

儲存政策與實際生成分開檢查。本輪實際生成結果為 **PARTIAL**：160支登錄產生器
中137支通過，166份主要產物中143份重新生成後與紀錄的 SHA256／大小一致。
1支產生器輸出不一致、21支被它的依賴阻擋，另1支受執行環境限制未完成。
此結論只涵蓋 MANIFEST 主要產物，不推進任何研究命題的 closure。

## 執行方式與證據

來源 HEAD：`ab0862485b30b12b538c734271f354630afa8e26`，另使用本次 staged
儲存整理的 index。使用實際 Git history 的隔離 shared clone，以 `checkout-index`
匯出 staged 檔案；先由 gzip 封存驗證並恢復165份 MANIFEST 輸入，總計
2,819,933,578 bytes。使用 Python 3.14.7、networkx 3.5、`PYTHONHASHSEED=0`。
生成均在隔離目錄進行，不改根工作區原證書或歷史稽核。

第一輪命令為 `python tools/artifacts.py rebuild --all -j 4`，未使用
`--keep-going`。它移開已登錄的主要輸出、實際執行產生器，再比較大小與 SHA256；
遇到失敗或不同 bytes 時恢復原檔。第一輪128支通過、6支失敗、2支不一致、
23支阻擋，exit code 1。其後只針對具體生成方式修補所影響的產生器重試，
未重複已通過的128支；另加入實際重建的新 probe。

逐輪證據保留，不以重試結果覆寫初次失敗：

- [整批第一輪結果](first-pass.json)與[完整 log](rebuild.log)。
- [生成方式修補後重試](retry.json)與[log](retry.log)。
- [明確 --write 的重試](retry-write.json)與[log](retry-write.log)。
- [新登錄 probe 的實際重建](probe-rebuild.json)。
- [合併結果、每支產生器與每份主要產物狀態](generation.json)，含環境、
  index／工具／MANIFEST／證據檔案 hash。

## 修補與仍未通過的項目

`tools/artifacts.py` 明列四支產生器會排他建立的小型伴隨檔，避免既有小檔
阻止大檔重建；重試時亦核對伴隨檔與當輪重建前 bytes 一致。excess-rejection
原產物使用 `--max-k 5 --greedy-trials 40 --seed 17`，補入明確參數。
QCORE 與 open-leaf-ledger 需要 `--write` 才會輸出檔案；初次 QCORE 缺少
封存輸入，恢復 D5 scope ledger 後又暴露缺少 `--write`，兩次失敗均保持紀錄。
參數會納入 producer fingerprint；只對實際重建一致的項目更新登錄 fingerprint。

先前僅被 ignore 的 `artifacts/c5_excess_two_e4/control_probe/split_hub_probe.json`
已補入 MANIFEST，明確使用同目錄的已追蹤 `.py` 產生器。它有5,312,816 bytes，
實際重建 hash 為
`e7286d173cedb86c22fb3f07c2d5e49969e98e25f634a6aa7b02436bebef64c1`，
與原檔一致，並已加入主封存。

剩餘項目如下：

| 狀態 | 產生器 | 原因與處理 |
| --- | --- | --- |
| mismatch | `c5_excess_two_mixed_core_single_spoke.py` | 只有三份文件的 `input_sha256` 漂移；見[差異](mixed-core-diff.json)。保留原證書與新差異，不自動接受新 bytes。 |
| blocked | 上述 mixed-core 的21支下游產生器 | 未執行，保留阻擋狀態；需先解決完整歷史輸入的 provenance。清單見 generation.json。 |
| failed / unverified | `c5_excess_two_finite_search.py` | multiprocessing forkserver 的 AF_UNIX socket 被執行環境拒絕，PermissionError。大型 k9 有限搜尋未完成，不能把恢復封存視為生成通過。 |

## 未涵蓋時的處理

新的已追蹤 JSON、JSONL、NDJSON、JSON5、bin 達1,000,000 bytes 時，儲存 CI
預設拒絕。可生成的產物先補明確 recipe、完整參數與輸出集合，實際生成比較後
才登錄 MANIFEST、加入 ignore 並移除原檔追蹤。歷史 hash／失敗紀錄／seal
需要固定保存時，核對 gzip 還原後封存；直接追蹤則必須有逐檔理由，frozen
例外另鎖大小與 SHA256。不得以 blanket exception 或 `record` 洗掉失敗。

此次本地 `artifacts/` 掃描，在排除明列 FROZEN 後沒有未登錄的大型受控副檔名
產物。[儲存驗證](storage-verification.json)亦確認移出的26份原檔 bytes／mode
與 gzip 還原一致、舊 ARCHIVE 的 file／blob records 全部不變、新 probe 可還原。
這是本次工作區觀察，CI 無法發現新 checkout 中不存在的未登錄、已忽略產物。

儲存 CI 不執行整批生成，也不完整驗證小檔、其他副檔名、壓縮檔、所有未追蹤
輸出、依賴圖或封存還原。`status` 的 `ok` 是主要檔案與 fingerprint 檢查，
不能取代本報告的生成結果。伴隨檔只與當輪既有 bytes 比較，未記錄其歷史
hash；缺少伴隨檔時只要求生成後存在，`status`／預設 `rebuild` 不完整檢查它們。
`.rebuilt`／`.recorded` 是可能被再次重試替換的 scratch；歷史結果以本輪保存的
receipts 為準。MANIFEST 外的小型產物與獨立 provenance checker 仍需各自驗證。
