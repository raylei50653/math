# W7 剩餘兩型：完整第二層與局部縮減審核發布

2026-10-21；發布前 Git BASE `13e51db3ec3d8d7ec7eeef60167afdc19ad956c4`。
依使用者要求整理目前進展並 commit + push 四組相連成果；
[整合報告](../../audits/2026-10-21-w7-remaining-two-13e51db/REPORT.md)為本輪來源入口，
[發布核對](../../audits/2026-10-21-w7-interface-publish-13e51db/REPORT.md)保存新重播與來源清單。

在原941／Q1接受零／J1 type III五邊路／嚴格only-R-W7契約下，
[原第二層紙證](../../audits/2026-10-21-w7-profile0-13e51db/PROOF.md)證兩型全部外側鄰點
構成原 induced 簡單圈 S，內部恰為 C7 與 R 共八原點。profile0／1 的圈長
分別為 8+K／7+K，且 K≥1；七列表保同一 S 字面色列的全部 lifts 與空 fibres。
任意長度的原圖結構由紙證承擔；49個 collar 及365個完整 fibre 控制只作有限校準。

[profile1 的555 patch](../../audits/2026-10-21-w7-profile1-13e51db/REPORT.md)
完整31列為14非空、17空；同一六點界面、至多兩內點的通用較小替換路線
有兩色障礙，602個三角化候選均引入原空列。
[52個刪點cap候選](../../audits/2026-10-21-w7-replacement-13e51db/PROOF.md)
在兩型必要支持上皆有洩漏；這些必要格未被實際來源觸發。
profile1 的完整 n-star 限制亦未進一步縮支持，兩target仍存活。
原40型仍排38、餘0／1；上述局部障礙均不構成來源排除或來源實現。

本次保存64份原研究產物，另核對12份已追蹤的不可變重播依賴，
共76個不同來源檔案、26,465,807 bytes。20份凍結輸入逐位元組對回 Git BASE；
原證明、證書、logs及verification保持bytes。既有gzip直接納入Git，
沒有新增archive紀錄、忽略規則或大型JSON例外。
原整合報告及verification的「未commit／未push」是研究核對當時的紀錄，
本次發布另由此紀錄及即時Git狀態承接。

五個checker的normal與seed17 optimized共十次重播全部通過、stdout逐字相等；
三份外部污染證書皆以exit 1拒絕，profile1及n-star內部負控制亦通過。
`lake build`完成8832 jobs，94項工具測試通過；文件、正式docs DocGraph、
Git index儲存規則、來源保存及隔離重播結果見發布核對。
全樹DocGraph仍有72項歷史duplicate-ID診斷，逐項與前輪相同，與正式docs檢查分開。

Closure scope：原第二層無弦圈、完整八內點界面及具名通用局部替換障礙；新增profile排除0。
Updated：四組相連證據、Kempe導覽、STATUS對應索引與本次發布紀錄。
Reviewed-unchanged：前輪38型排除、兩型清單、一般J1兩項／J2六項；README及HANDOFF入口。
Remaining OPEN：profiles0／1來源排除、精確必要計數錐、原E條件替換、來源實現、
一般W7／C7多內點／J1／J2、嚴格較小bad及主命題；沒有新Lean定理。
Propagation stop：L1；沒有新增profile closure，父題邊界未改。
目前停止點與接續入口由[Kempe導覽](../c5_kempe_guide.md)維護。
