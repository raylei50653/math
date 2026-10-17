# R6-MARKED-SIX 驗證紀錄

BASE `6c420f3ca77d60952ed76f93dff7449c522715ca`；2026-10-17。

三路獨立重建及其交叉審核見 [REPORT](REPORT.md#2-證明的三個獨立檢查點)。
審核對象為完整 [PROOF](PROOF.md)，SHA256
`463cb574f3d8bf4b7abd1de668ae1f67d31f07b42838406c621cc04de73aef10`。
新來源紙證沒有 Lean 化；有限校準不替代任意大小拓撲。

| 證據 | 已完成結果 |
| --- | --- |
| A 兩步引理 | 正常／seed17輸出相同；刪原非邊、增W5 chord兩個負控制均拒絕 |
| B 六圈分類 | 兩配對、四端點變體、四完整p/q鄰環；正常／seed17通過，錯誤q度數證書及覆寫均拒絕 |
| C 固定圖 | 38 PM、3聯合101、5標記六圈、2 cyclic六割；正常／seed17通過，七種污染及覆寫均拒絕 |
| root 來源與交換 | 22個 frozen 輸入逐一與 BASE Git object 相同、live數學來源無漂移；正常／seed17、錯誤交換證書拒絕與覆寫保護均通過 |
| `lake build` | exit 0，8832 jobs；既有linter warnings保留，未新增Lean theorem |
| `scripts/check_docs.py` | exit 0 |
| 正式 docs DocGraph | exit 0，97 documents、383 relations、0 errors |
| 正式 docs 加本輪有效報告的 scoped DocGraph | exit 0；不將 frozen metadata 當作當前獨立文件 |
| whole-tree DocGraph | exit 1；與開始時相同70個錯誤身份，並非全樹通過 |
| 本輪有效 Markdown 本地連結 | 53個目標全部存在；完整紙證SHA與B/C交叉審核一致 |
| `git diff --check` | exit 0；另核對新增有效文字，保留 frozen 原bytes |

A/B/C 的逐項 receipts 在各自目錄；root 重播及負控制見
[REPLAYS](integration/REPLAYS.json)，建置見 [LAKE_BUILD](integration/LAKE_BUILD.json)，
文件檢查的命令、exit code及log hash見 [FINAL_CHECKS](integration/FINAL_CHECKS.json)。

首次把本輪整個目錄（含 frozen）當作獨立 DocGraph 範圍，得到一個
unknown-target：凍結 c4-triangle-core 的上游 c4-boundary-pivot 不在該子集。
這份失敗log仍保留。後續檢查明列正式 docs 加有效 audit 報告，排除把封存
metadata當新權威的錯誤範圍，結果通過；未改動 frozen 來消除錯誤。

全樹的70個既有錯誤身份完全相同；新增凍結 c4 入口只使既有
duplicate-id診斷多列一份封存路徑。去掉這個額外路徑後，全樹輸出與開始時
逐byte相同，見 [DOCGRAPH_COMPARISON](integration/DOCGRAPH_COMPARISON.json)。
因此只報正式／有效範圍通過，明確保留whole-tree失敗。

封存清單 [SHA256SUMS](SHA256SUMS)綁定本audit與三份更新後routing文件，
由 `sha256sum -c` 只讀重播。不以本文或任何程式PASS宣稱新的Lean拓撲定理。

原來源數學檔案與舊證書保留；README、HANDOFF及舊歷史報告不改寫。
本輪不重跑外部枚舉、舊大型有限搜尋或前輪九框計數；沿用它們的已封存範圍。
沒有 commit 或 push。
