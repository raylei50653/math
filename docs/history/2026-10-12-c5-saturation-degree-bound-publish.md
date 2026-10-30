# 最小來源度數界：本地整理與提交

2026-10-12。使用者授權「整理後 commit，給衍生任務描述自行發布」。
本輪只作本地提交，沒有 push 或外部發布。
採納 BASE 為 `5d70a39940182ea37c9ca5d36d9ebb7f612160ad`；提交 SHA 以 Git 為準。

## 採納範圍

[權威入口](../archive/reports/c5/structure/c5_saturation_degree_bound.md) 接續已發布的共面正規形與十二內點界，
採納條件性 C4 三內點代表、全域最小目錄外來源的邊界度數≥4、內部≥5、n5≥6。
[證據包](../../audits/2026-10-12-c5-saturation-degree-bound/REPORT.md) 凍結五份輸入，
保存兩個反控制、全部 labelled fibres、可重播 checker 與獨立 conditional PASS 審查。

沒有具體 933／941 來源，沒有新增 Lean theorem、沒有重播外部計算定理。
十三內點以上、五度配置可縮減性及 K∞=K≤5 仍 OPEN。
紙面普遍性、有限證書與既有 Lean 回歸分開。

## 文件與衍生工作

新增 canonical、證據包及[三份可發布任務](../tasks/c5_degree5_link_tasks.md)；
README／HANDOFF／STATUS／Kempe guide 接入新入口，共面報告加日期後續連結。
degree-5／R、E-ARC2／N2、synthesis、Lean guide 的舊身份與覆蓋 reviewed-unchanged：
本輪最大邊數、全域最小來源不能自動取得其 edge-critical、deficiency 或 Gallai 前提。
文件傳播在直接來源及 consumer 層停止。

任務 A 分類 degree-5 link 位置及 pinned patch 契約；B 核對固定實際圖的十列完整
重接與負控制；C 只核對指定兩外框接點的 C5＋C5 cap 子域，完整 132² joins。
任務 C 的兩個 cap witnesses 加四個介面內點至多十四內點，須直接證產出在 K；
不由十二內點界代替核對。三份尚未執行，也不預設彼此結果。

## 驗證與提交隔離

實際命令、exit code 及輸出見證據包的 `VERIFICATION.json` 與 `logs/`。
normal／seed17／不同 cwd 的完整 replay 均 PASS；破損空 fibre、缺凍結輸入、
覆寫既有證書三項負控制均正確拒絕。舊 cofacial v2 只讀 replay PASS，核對
132 witnesses／8778 unions／十 candidates。五份凍結輸入 SHA256 全數核回。
新證書使用 compact JSON 保存同一份完整資料，328,802 bytes，SHA256 為
`b8ebeeb6fc06bf3a5036e17789c14cb839cec57dd0a8dda18f6f7f162447e965`。

文件檢查 PASS（630 Markdown／7,843 本地連結）；正式 docs DocGraph PASS
（62 documents／213 relations）；`lake build` PASS（8,831 jobs，既有 linter
warnings 保留）；`git diff --check` PASS。
全工作樹 DocGraph **FAIL**：62 個既有 duplicate-ID errors，沒有本輪新檔案列入
錯誤。完整輸出保存，不刪除舊 audits／scratch 快照來隱藏失敗。

提交使用獨立 Git index 與 connected 明列白名單。發布前已有 74 份 unrelated
staged paths；其 mode／blob 必逐項核回。README 原有暫存新增內容亦保留，
只納入本輪新增入口列。原 scratch 及舊證書保持不變。
本輪提交路徑乾淨不代表整個工作樹 clean；未授權遠端操作。
