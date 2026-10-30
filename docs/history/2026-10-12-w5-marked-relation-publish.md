# W5 具名完整關係縮減採納與發布

2026-10-12。使用者授權「整理目前進展 commit + push」。起點 HEAD 與遠端 main
均為 `e299ae987fcc4cdeb55dd41bede0a3a7c9d9db86`；起始工作樹只有本輪 W5 隔離包未追蹤。
本次以 [具名完整關係縮減](../archive/reports/c5/structure/c5_w5_marked_relation.md) 為正式來源入口。

## 採納範圍

固定原 B/U、色框與全內部 induced W5 的空面槽位，五個合法 k−2 單對商圖的完整
染色拉回同一 H=G−v；其聯集重建全部 H fibres，重數二的 lifts 恰可唯一補中心。
34 圖、348,160 格及其空 fibres、全部完整 lifts、反控制與獨立審查相連採納。
普遍結論由紙面證明支撐，有限證書只校準明列圖域。

只保外圈、獨立正規化 U、各自成功的 witnesses 都有反控制。
零新頂點的局部加邊／非交叉識別正聯集亦有精確的普遍限制，但不排除特定
annulus 過濾多餘 lifts。普通正聯集縮減、r≤6 annulus 代表、一般來源與
`K∞=K≤5` 保持 OPEN；真正 933／941 最小目錄外來源仍 `not triggered`。

## 原證據與本次核對

原 [隔離包](../../audits/2026-10-12-w5-marked-relation-e299ae98/REPORT.md)
連同 manifest 共42檔直接納入 Git。原41個 manifest entries 的 bytes／SHA256
及九份 frozen inputs 均不改；82,360-byte gzip 正式證書、六份破損 fixtures 與
失敗 logs 原樣保留，無需追加大型產物封存。原報告的「未採納／未提交」是隔離
交付當時的語境，本次採納及發布由本頁記錄，不覆寫舊 seal。

本次發布另存 [核對結果](../../audits/2026-10-12-w5-marked-relation-publication/verification.json)
及 logs。從 Git index 匯出完整42檔，在新目錄逐一核對 manifest，並重播正常、
seed17 及獨立完整枚舉，驗證新 checkout 的證據包可獨立重播。沒有重跑六份負控制
或上游大型枚舉／外部計數證書；沿用原已封存結果。

文件連結／索引、正式 docs DocGraph、staged whitespace 及大型產物 index 檢查
均通過；文件檢查為636份 Markdown／7,905個本地連結。三項新副本重播亦全通過。
全工作樹 DocGraph 保留62項歷史 duplicate-ID errors，不當成全域 PASS。
`lake build` 本次作既有 Lean 回歸通過（8,831 jobs），沒有新增 Lean theorem，不能把紙面五輪縮減
稱為已形式化。實際命令、exit codes 與摘要以新核對結果為準。

## 文件傳播

Updated：新 canonical 入口、五度鄰環父入口、Kempe guide、STATUS 及本發布紀錄。
Reviewed-unchanged：README／HANDOFF 的研究入口與活躍線未變；共面正規形、度數界、
三份原任務及外圈報告的父命題 OPEN 仍正確。舊 E-ARC2／N2、degree-5／R 與
Lean guide 沒有取得新前提或 theorem；原隔離報告、manifest 及歷史紀錄不改。
Closure scope：只採納完整染色資料的五商圖無損重建及明列局部限制。
Remaining OPEN：合法正聯集縮減、同槽位小代表與一般主命題；Propagation stop：L2。

提交使用相連白名單；推送後核對 HEAD、origin/main、遠端 main 與乾淨工作樹，
最終提交 SHA 以 Git 及本次回覆為準。
