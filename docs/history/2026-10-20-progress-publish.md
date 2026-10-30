# 941 fibre、兩圈條件修復與 P/R 來源覆蓋整理發布

2026-10-20。發布前 HEAD 為 `9c36e3c4789dfec07d60ec4e042f0bafe17451d1`。
使用者明確要求整理目前進展並 `commit + push`；本紀錄保存本次整理及驗證，
不改寫各輪報告「未提交／推送」的歷史語境，也不改動凍結證書。

## 成果與精確停止點

| 研究線 | 本次納入的進展 | 保留缺口 |
| --- | --- | --- |
| 941 最後拒絕 | [fibre 搬運](../../audits/2026-10-20-r6-941-fibre-transport-9c36e3c/REPORT.md)與[續進](../../audits/2026-10-20-r6-941-fibre-continuation-9c36e3c/REPORT.md)：J1 零值目標為兩項；J2 為六項，拒絕計數恰為六項和的兩倍。J1 只能在指定分離層交換。 | 一般 J1／J2 的最後 `01021`、同一候選三拒絕及嚴格較小 bad 仍 OPEN。 |
| J1 原 W5 三邊路 | [同一 k−6 候選](../../audits/2026-10-20-r6-941-j1-w5-9c36e3c/REPORT.md)保 `01232` 且三拒絕完整 fibres 全空，排除 n=5；另排四條原弦。 | 整個子支只剩 n≥6 的 induced C11；須保留 n 的額外私有附件。 |
| 兩完整補圈修復 | [單面／同 O 判準](../../audits/2026-10-20-r6-two-cycle-repair-9c36e3c/REPORT.md)、[相鄰雙點](../../audits/2026-10-20-r6-two-cycle-batch-9c36e3c/REPORT.md)至[5／5／5 四點十圈](../../audits/2026-10-20-r6-555-odd-branches-9c36e3c/REPORT.md)：同一 M、原 rotation、三標記及全部完整分量同時滿足，後者完成該條件型，補圖恰為兩個偶圈。 | 尚未證來源必落該度數型；其他度數型、普遍修復與聯合偶補正值仍 OPEN。固定控制的來源實現仍 not triggered。 |
| P/R 來源覆蓋 | [精確合同與真圖控制](../../audits/2026-10-20-c5-pr-source-coverage-9c36e3c/REPORT.md)：未來四列支援等價完整十列；一般保計數代表命題由真 disk 反駁；另得逆操作、可剝子類及固定 17P 外補。 | 一般支援覆蓋與指定 r6 代表仍 OPEN。後繼入 K、改框增點外補及不可剝均不裁決原框來源覆蓋。 |

紙面任意大小條件證明、有限完整 fibres／匹配／cut 證書及 Lean 分開。
沒有新增 Lean theorem；一般 `K≤22`、固定 r6 的 `k≥25` 不變。
`W110+W101>0`、`omega_e=0`、完整319及 `K∞=K≤5` 均未閉合。

## 發布範圍與證據保存

七組 audit 的 2,924 份非快取原檔逐 bytes／SHA 封存於
[SOURCE_FILES](../../audits/2026-10-20-progress-publication-9c36e3c/SOURCE_FILES.json)。
其中 78 份遞迴 frozen 依賴被既有 ignore 規則遮住，依
[精確清單](../../audits/2026-10-20-progress-publication-9c36e3c/required-ignored-inputs.json)
納入；兩個未列封存的 `__pycache__` 保持忽略。
獨立 [Git index 核對](../../audits/2026-10-20-progress-publication-9c36e3c/index-review/summary.json)
確認全部 2,924 份來源 bytes／SHA 相符，2,444 筆依賴均在暫存區，非路由輸入零漂移。
11 份超過 1 MB 的 JSON 依既有政策登記確切大小與 SHA，見
[新增例外](../../audits/2026-10-20-progress-publication-9c36e3c/artifact-exceptions-added.json)；
checker 與政策門檻不變。凍結依賴、失敗探索及既有負控制保留原位元組。

Updated：Kempe／state 導覽及 STATUS 的對應索引、停止點；STATUS 頁首壓縮為當前摘要，
發布紀錄移入歷史區。Reviewed-unchanged：README／HANDOFF 的研究入口、研究線與進行中標記。
Propagation stop：L2；已完成者限於具名子案，兩條父研究線仍 OPEN，未改全域命題。
目前研究接續以 [Kempe 導覽](../archive/guides/c5_kempe_guide.md)與 [state 導覽](../archive/guides/c5_state_guide.md)為準。

## 本次驗證

三路獨立唯讀審核重新執行七組證據：941 三套與兩圈三套各自正常／
`PYTHONHASHSEED=17` 全通過，組內完整 stdout 相同；P/R 五套 checker 正常與
異 cwd／seed17 共十次通過。各組既有污染控制與暫存副本的排他建立控制均按預期拒絕，
原證書與凍結檔案零漂移。精確 argv、退出碼、雜湊與原始輸出保存於
[941](../../audits/2026-10-20-progress-publication-9c36e3c/review-941/summary.json)、
[兩圈](../../audits/2026-10-20-progress-publication-9c36e3c/review-cycles/review.json)、
[P/R](../../audits/2026-10-20-progress-publication-9c36e3c/review-pr/review-results.json)。
941 review 的一次錯誤 CLI 呼叫保留紀錄，已用正確 `--source` 重跑，確認實際比對拒絕。

本次 `lake build` 完成 8832 jobs，只有既有 linter warnings；這不形式化新紙證。
artifact policy 的 34 項測試通過；首次測試檔名寫錯而沒有執行任何測試的紀錄保留，
已以正確檔名重跑。完整 staged 空白檢查的 62 個警告全是八份已封存 patch／diff 的
單空白上下文行；保留其 SHA，精確排除這八檔後，其餘 staged 檔案通過。
文件、正式 docs DocGraph、artifact policy、Git index custody 及空白檢查的最後結果見
[發布檢查](../../audits/2026-10-20-progress-publication-9c36e3c/publication-checks.json)。
全工作樹 DocGraph 仍有 72 個 duplicate-id 診斷，涉及保留的 frozen／scratch／歷史副本；
不宣稱全樹通過，也不刪證據消除診斷。

最終 commit、push 與本地／tracking／遠端 SHA 一致性以完成發布時的即時 Git 核對為準；
本紀錄不預先宣稱遠端 CI 成功。
