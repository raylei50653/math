# 共同切口與剝殼 fan 續進整理發布

2026-10-29。依使用者要求，從基準 `f5bedfd7f32ef4542700ab5623535ed056963022`
整理[計數／手術共同切口](../four_color_counts_surgery_continuation.md)與
[剝殼 fan 續進](../four_color_shelling_verification.md#fan-與-middle-tree-的縮窄)，
連同五支 checker、完整小型證書及直接文件更新一同發布。

共同切口拒絕的是指定非 disk 的 932 完整交換模型；真 disk 的反例則否定指定分量摘要的
迭代充分性。剝殼結果補上 middle-tree 計數、至多四鄰點還原及同一見證的換色提升條件。
兩者均保留一般 932、共同解存在性與 4CT 的 OPEN 邊界；沒有新增 Lean 定理。
本次沒有修改主求解器或擴大研究枚舉。

## 證據保存與本次驗證

- 四份 counts／surgery 的 `--check` 及 shelling fan 重播均與原證書逐 byte 相等，
  命令、摘要與 hashes 見[研究重播收據](../../audits/2026-10-29-continuations-publication-f5bedfd/research-replay.json)。
- [工具測試](../../audits/2026-10-29-continuations-publication-f5bedfd/tool-tests.log)：515 項通過。
  本次未修改 Lean；未重跑 Lean build，也不將有限 Python 結果當作 Lean 證明。
- 原研究檔與五支 checker 的[SHA256 清單](../../audits/2026-10-29-continuations-publication-f5bedfd/SOURCE_SHA256SUMS)
  保存來源身份。兩份大型 JSON 僅追加至既有 ARCHIVE，新增兩個 gzip blobs；
  [封存核對](../../audits/2026-10-29-continuations-publication-f5bedfd/archive-check.json)
  確認原始 bytes、壓縮 hashes、臨時路徑還原及全部舊 records 不變。
  本地未壓縮檔保留；新 checkout 先依[封存說明](../../audits/README.md#新-checkout-的還原)
  執行 `python3 tools/audit_archive.py restore --artifacts`。
- 文件連結／索引、正式 docs DocGraph、Git index 產物政策及 staged whitespace 結果見
  [發布檢查](../../audits/2026-10-29-continuations-publication-f5bedfd/checks.json)。
  全工作樹 DocGraph 仍有 72 項保留快照／scratch 的 duplicate-ID 錯誤，另存完整 log；
  不將正式 docs 通過改稱全域通過。

導覽、直接接口 consumer 與 STATUS 已更新；兩份原研究紀錄保留當輪語境並連到本頁。
父命題未收尾，HANDOFF 的研究線及活躍標記不變。本次只提交相連檔案，沒有新增儲存例外。
推送後核對本地、tracking、遠端分支 SHA 與工作樹；遠端 CI 分開回報。
