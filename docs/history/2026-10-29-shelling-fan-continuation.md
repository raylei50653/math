# 2026-10-29：剝殼 fan、完整關係與換色提升續推

權威來源為[剝殼報告](../archive/reports/planar-sources/four_color_shelling_verification.md#fan-與-middle-tree-的縮窄)；
本頁只保存當輪驗證範圍，不另維護主題裁決。

後續[整理發布紀錄](2026-10-29-continuations-publication.md)保存本次獨立重播、
大型證書封存與檢查；發布狀態以即時 Git 為準。

紙證補上 middle-tree 計數、至多四鄰點正向還原、兩個任意大小構造族，以及同一見證的
雙色分量交換提升 iff。五點三角雙錐否定「剩餘圖合法換色必保留累積關係」；
一般共同解存在性、五鄰點以上修復及 932 排除仍 OPEN，沒有新增 Lean。

[核對程式](../../scripts/four_color_shelling_fan_verification.py)與
[證書](../../audits/2026-10-29-shelling-fan-continuation/fans.json)保存完整列與 fibres。
另行重播輸出與證書逐份 JSON 相等，程式及幾何依賴的 SHA256 均吻合。
15 個幾何來源、9 圖 38 階段完整關係、158 份小 fan 前綴染色、946 份提升請求及
12 個構造實例全部核對；74 份提升請求被正確拒絕，未把負例誤記為原圖無解。
固定初始三角形的染色核對利用全域色置換，未增加主問題的固定色假設。

程式 SHA256：`e54a91689cae4e4c64895be842086e682cd874fe38fc5a08ef3c7861a92d4812`。
證書 SHA256：`cf625f585b1015c8d13ec7612e60a089daa78295ae3814b09f5cc1449d9a956d`。

文件傳遞：更新專題報告、4CT 導覽的直接入口及 STATUS 對應列；四項驗證父報告的
「單環成立、一般存在性仍缺」仍正確，核對後不改。HANDOFF 研究線及活躍標記不變。
主求解器、既有完整消元 Lean 及 BFS 效能結論均未改動。

Markdown 的本地連結／索引／入口檢查通過。文件檢查區分正式 docs 與全工作樹：
正式 docs DocGraph 通過；全工作樹 DocGraph
仍有 72 項歷史／scratch 重複 ID 錯誤，未清除快照掩蓋它們。`git diff --check` 通過。
