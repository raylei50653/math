# R6／941 同候選存在性與最後拒絕：發布紀錄

日期：2026-10-20。來源 BASE：`f13eb4d0887d962021992ae7afe3323af4d79cd3`。
使用者明確授權 `commit + push`。本紀錄追加發布資訊；不改寫歷史報告的「未 commit／push」或已封存證據。

本次一併發布 [同候選存在性](../2026-10-19-r6-941-existence-f13eb4d/REPORT.md) 與
[最後拒絕](../2026-10-20-r6-941-last-rejection-f13eb4d/REPORT.md) 兩輪證據、直接導覽與完整重播依賴。
前輪的 J1／J2 保接受及兩拒絕空；後輪把最後 `01021` 精確縮為八／十二個完整 fibres，並給出原分量限制及仍存活的必要整數控制。
主存在性、同候選最後拒絕與嚴格較小 bad 仍 **OPEN**；沒有來源實現或新 Lean 定理。

## 發布範圍與封存

- [SOURCE_FILES.json](SOURCE_FILES.json) 逐檔記錄兩輪 audit、兩份導覽、artifact policy 及必要上游原檔的位元組數與 SHA256。
- 新一輪 INPUTS 封存了 39 份被上游 ignore 規則遮住的依賴；其凍結副本與原檔均按精確路徑納入，供 root checker 在新 checkout 核對原檔。清單見 [凍結副本](required-ignored-inputs.json) 與 [原檔及 SHA](required-original-inputs.json)。此舉不把 discovery 升格為來源實現或正式定理。
- 十份超過 1 MB 的 JSON 依現行政策登記確切大小與 SHA；只增加 [列出的例外](artifact-exceptions-added.json)，未放寬 checker 或既有政策。
- 原 INPUTS／OUTPUTS、失敗探索與 notation-before 記錄維持原位元組。README／HANDOFF 的研究入口及結構未變。

## 驗證與邊界

前輪 root checker 在本次發布重新執行正常與 `PYTHONHASHSEED=17`：兩者通過，完整輸出相同；見 [existence-replays.json](existence-replays.json)。
後輪同一工作階段的正常／seed17、獨立交叉審查、語義負控制與錯誤 SHA 拒絕已通過，原結果保存在 [checks.json](../2026-10-20-r6-941-last-rejection-f13eb4d/checks.json)。發布另核對 Git index 中全部凍結／歷史輸入及輸出封存，避免只在原工作樹可重播。

同一工作階段的 `lake build` 通過 8832 jobs；沒有 Lean 變更，發布不重跑無關研究。文件、正式 docs 範圍 DocGraph、artifact index policy 與提交空白檢查的實際結果另記於[本次 checks.json](checks.json)。
Git index 已逐 SHA 核對 2313 份相關檔案；完整空白檢查的 46 個警告僅來自四份已封存歷史 diff 的空白上下文行。保留這四份原位元組，精確排除它們後，其餘 staged 檔案通過；詳見 [檢查明細](publication-checks.json)。
全工作樹 DocGraph 的既有診斷仍是 72 個 duplicate-id，涉及保留的 scratch／歷史／凍結副本；不宣稱全樹通過，也不刪封存來消除診斷。

本紀錄不預先宣稱遠端 CI 成功。最終提交 SHA、推送及本地／tracking／遠端一致性由發布完成時的 Git 核對回報。
