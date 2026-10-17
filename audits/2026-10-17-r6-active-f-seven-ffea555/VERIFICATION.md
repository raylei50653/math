# 本輪驗證與證據層

2026-10-17；研究 BASE `ffea555fc2a896d8166ce198ca28ed9262912f25`。
任意大小定理是 [PROOF](PROOF.md) 的紙面推論；
[A](A/REVIEW.md)、[B](B/REVIEW.md)、[C](C/REVIEW.md) 分別交叉審核。
根代理另核對實際三角面、完整鄰環、標記匹配身份與條件下降的量詞。
整合稿的 C 交換規則節號已修為 §6；沒有改變數學命題。

本輪12份整合收據均符合預期：正常檢查exit 0，污染manifest明確exit 1。
17份authority輸入零漂移；A正常／seed17完整重建一致。正式文件檢查覆蓋
694份Markdown、9135條本地連結；formal／scoped DocGraph皆97份metadata文件、
383條relations、零錯誤。本輪9份活躍audit Markdown的本地連結皆有效。
既有Lean庫 `lake build` 通過8832 jobs；既有linter warnings保留。

## 證據與收據入口

| 檢查 | 範圍與收據 |
| --- | --- |
| BASE custody，正常與 seed17 | [check.py](check.py) 對回 17 份 Git BASE bytes／SHA256，允許明列 routing drift；[正常](verification/custody.json)、[seed17](verification/custody-seed17.json) |
| BASE manifest 污染負控制 | 只污染另存的 manifest，不動原件；預期拒絕；[收據](verification/custody-negative.json) |
| A 完整局部匹配算術 | 四組反射面系統共128個binary賦值；包括空矛盾slice、刪前提反控制及退化三角面拒絕；[完整證書](A/certificate.json)、[開發與負控制收據](A/VERIFICATION.json) |
| A 正常／seed17 再播 | 重建整份局部關係；[正常](verification/A-replay.json)、[seed17](verification/A-seed17.json)；不是原來源枚舉 |
| 前輪 root checker | 沿用完整七缺陷分類與區域定理的既有證據；本輪重播其11份輸入custody與標記算術；[收據](verification/parent-replay.json) |
| 文件及連結 | [正式文件](verification/docs.json)、[活躍audit連結](verification/audit-links.json)；frozen原稿保持原始bytes，不改寫其歷史相對引用 |
| DocGraph | [正式範圍](verification/docgraph-formal.json)、[連同本輪範圍](verification/docgraph-scoped.json)；不宣稱全樹歷史文件零錯誤 |
| Lean | [lake build](verification/lake.json)，只建置既有庫；沒有新增Lean theorem |
| whitespace | [tracked diff](verification/diff-check.json) 與本輪活躍文字檔核對；不正規化frozen證據 |

收據逐份記實際 argv、exit code、stdout／stderr hash；總表見
[verification/summary.json](verification/summary.json)。A 的缺列污染及重複建立
拒絕保留在 A 原收據，不覆寫開發證書。根 manifest 污染控制與其明確拒絕另存。
最終audit檔案bytes另封存於 [OUTPUTS.sha256](OUTPUTS.sha256)，可在repo根目錄
用 `sha256sum -c audits/2026-10-17-r6-active-f-seven-ffea555/OUTPUTS.sha256` 核對。

首次 freeze 嘗試一條不存在的舊PROOF路徑，於寫manifest前停止；一般檔案搜尋
找到真實 REPORT.md、r6/PROOF.md 後，對已複製bytes核對再完成凍結。
[FREEZE-NOTE](FREEZE-NOTE.txt) 保留這項路徑修正；沒有更動任何舊權威檔案。

## 解讀與未重跑項目

局部算術校準已觸發且成立；真正最小來源實例未供應，來源實現為 **not triggered**。
零來源命中不當作排除證據；新子類排除由真實面與匹配身份的紙面論證支持。
區域分離存在性仍 OPEN，不能由定位、有限局部態或最小化定義推出。

本輪不重跑舊大型來源枚舉、九框計數、前輪A的912匹配對或其他完整固定圖控制，
不修改外部定理信任界線；全樹DocGraph及大型產物Git index政策未作本輪驗證宣稱。
本輪新增檔案均小於1 MB；沒有改動產物政策、stage、commit或push。
既有Lean建置通過也不把新紙證升為形式化結果。
