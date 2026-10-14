# C4 返回旁支的相接發布

2026-10-14。研究 BASE `a11d4bb`。使用者明確要求 commit + push；本次只發布
[返回旁支報告](../../audits/2026-10-14-c4-return-branches-a11d4bb/REPORT.md)
及相接證明、完整局部控制、certificate、獨立審閱、保留失敗紀錄與檢查 logs，
加上 C4 專題、Kempe 導覽、STATUS 和本紀錄。

## 結論與保存範圍

全數限定於原 x,y,b 都四度的 no4ct 全域最小目錄外來源。同一原圖、具名
接點、原邊／rotation、共同色框與全部完整 fibres 的條件均保留。

- p 或 q 五度給精確 mask14 的較小 C4 介面及 rainbow fibre split；單低度支 OPEN。
- p=q=5 迫 pq 的另一面頂點 ell 原度至少六；雙低度且 ell≥6 仍 OPEN。
- a=4⇒t≥6、c=4⇒s≥6，三種來源均適用；一般 t=5 的 C5 支持只留956／1012／1020。
- 整圖旋轉的 p/q 下界保持原 singleton 空 fibre 限制；不得推到不滿足前提的941。
- 一般 mask13 的返回落入允許 sector；r=7 的必要 C6 模型仍存活。

一般 K≤22／k≥23 不變，任意大小 catalogue 等式與一般 T／T0 延拓仍 OPEN。
沒有新增來源實現、外部完整枚舉或 Lean theorem。舊 certificate、初次失敗與
較弱 intermediate controls 均保留；所有新 JSON 均低於1 MB，不追加 archive。

## 發布核對

四份最終 local checker 的普通 replay PASS；研究階段的 seed17及 corrupted
certificate負控制也已通過並保留。本次只讀再核對未更動的最終證書，不重生成
或覆寫它們。相接 manifest與14份 frozen inputs SHA256核對通過。

`lake build` PASS，8,832 jobs，沿用既有 linter warnings；這不表示本次紙面
拓撲或 Python 控制已形式化。文件、正式 docs DocGraph、staged whitespace
與 generated-artifact policy 的本次結果見
[發布檢查 receipts](../../audits/2026-10-14-c4-return-branches-a11d4bb/logs/publication-receipts.json)。
全樹 DocGraph 沿用已保存的70筆 frozen／scratch duplicate-ID錯誤；研究階段
輸出與前輪基準逐 byte 相同，沒有為製造 PASS 刪除歷史。

發布前 fetch 與 remote main 均為 BASE。只 stage 上述 whitelist，push後核對
`HEAD=origin/main=remote main` 並確認乾淨工作樹；即時 Git 是發布狀態權威。

Updated：C4 專題、Kempe 導覽與 STATUS 直接條目、本發布歷史。
Reviewed-unchanged：README／HANDOFF 路由及 tags、no4ct handoff、synthesis 的
一般 OPEN 界線。Propagation stop：直接主題；未擴大來源或 general closure scope。
