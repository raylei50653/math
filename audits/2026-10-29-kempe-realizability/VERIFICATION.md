# 研究收尾與驗證範圍

2026-10-29。權威來源為 [封鎖來源報告](../../docs/c5_kempe_blocked_realizability.md)。
實際命令、返回碼與來源 hashes 見 [verification.json](verification.json)。

Closure scope：同一原三角面附件排除五步正規化回返的全部奇週期；
模二 cocycle 排週期二，故封鎖分量的固定字面 fibre 為偶數且至少四。
排除具名 SINGLE-FIBRE-5 完整傳輸模型與 THIN-932 的奇數／二份 fibre 候選，
沒有排除 support 932 的全部來源，沒有新 D-可約構形或一般逃逸定理。

證據：原附件及面鏈化約為紙面；精確有限 cocycles、具名模型、完整真圖著色、
全部實際交換、一／二層獨立局部／遠端 fibres 及遠端重接為 Python。
獨立 checker 重建 cocycle 域與真週期四的三角面填充，未匯入主同調生成器。
未新增 Lean，也未用 4CT oracle；既有 22 內點界的外部 census 未重跑。

八項新／舊數學重播全部通過。`check_docs.py`、正式 docs 範圍的 DocGraph、
`git diff --check` 通過。全樹 DocGraph 仍有歷史／凍結副本重複 ID；
本輪沒有改寫那些歷史資料。兩個大型證書依既有 audit archive 保存原 bytes 的 gzip，
本機 live JSON 仍在；新 checkout 先執行 `python3 tools/audit_archive.py restore --artifacts`。

Updated：新報告、五支新 checker 與證書；4CT／Kempe 導覽加入直接來源，STATUS 加短索引。
Reviewed-unchanged：原 D 單 split 停止裁決、C5→C4 22 內點界、class 計數及其證據邊界；
HANDOFF 的研究線及標記沒有變更。
Remaining OPEN：合法 S5 來源較長偶週期、m≥4 的實際全封鎖分量、固定星與整個允許局部族命題。
Propagation stop：主題報告及直接導覽／索引；沒有封閉父層 4CT 或一般932，不向上改寫為已證。

工作樹原有及同時進行的其他研究變更保持原狀；本輪沒有 commit 或 push。
