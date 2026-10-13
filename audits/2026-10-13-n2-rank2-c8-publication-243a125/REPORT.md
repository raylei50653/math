# 三份研究交付的整理與發布核對

2026-10-13，BASE `243a125a80e4d8de40957f59d8da0bdbc974cf69`。
本包只記N2-BRIDGE、W5-RANK2、C8-STRUCT的原證據保存、focused replay
及相連文件發布。採納前提與OPEN邊界見[整理紀錄](../../docs/history/2026-10-13-n2-rank2-c8-publish.md)。

[N2 receipt](n2/N2_REVIEW.json)、[W5 receipt](w5/receipt.json)及
[C8 receipt](c8/receipt.json)保存本次實際命令、exit與結果。
N2／W5部分stdout未另存檔；receipt清楚標成工具輸出的觀察摘要，
W5 observed-summary檔案為摘要轉錄，不冒稱raw logs。
原U4回歸有本包n2目錄的實際logs；C8 receipt含實際stdout及stdout／stderr hashes。
Receipt中的原 `/tmp` 路徑保留重播出處，其對應檔案已複製到本包。

[原檔manifest](original-bundles.json)鎖定三份隔離包的390個非快取原檔，
記錄SHA256、大小與mode。[封存前摘要](archive-before.json)、
[選定路徑](archive-paths.json)與[append紀錄](archive-append.log)保存封存範圍；
原audit、sealed bytes及歷史失敗不改寫。
[verification.json](verification.json)逐項記錄本次文件／儲存／Lean核對與未重跑範圍。
Git index輸出與逐byte封存還原的最後核對記於custody.json。

## 本次核對結果

- 三份主／獨立checker、normal／seed17及指定負控制通過；完整命令及觀察結果由上述三份receipt負責。
- `lake build`回歸通過，8831 jobs，既有linter warnings保留；沒有新增Lean theorem。
- 文件連結／索引、正式docs DocGraph、56項儲存工具測試、staged大型產物policy與Git whitespace通過。
- 全工作樹DocGraph為FAIL，62個保留副本／scratch duplicate-ID；沒有把正式docs通過改稱全域通過。
- 390個原payload從Git index重新輸出：383份直接檔案與7份gzip原路徑全部SHA256／大小／mode相符；live原檔亦零漂移。
- 舊2472個封存路徑records及1540個blob records全保持；本批只新增7個路徑、3個blobs。

新checkout先執行 `python3 tools/audit_archive.py restore --artifacts`，
再依原報告重播checker。沒有來源圖大枚舉、外部證書重播或新增Lean theorem；
`lake build`只是現有專案回歸。正式docs與全工作樹DocGraph分列，
保留副本duplicate-ID的FAIL不由正式docs PASS取代。
本地checks不聲稱遠端CI已通過；發布SHA与工作樹由即時Git及最終回覆確認。
