# 本輪驗證範圍

2026-10-17；BASE `5b9a7b3190c84bc10ff99608e372a9b4be57a0f6`。

| 檢查 | 實際結果 | 證據與限制 |
| --- | --- | --- |
| root normal／seed17 | PASS；11份BASE逐檔相等、數學來源live零漂移、一般與參考批次標記表相符 | [收據](integration/root-checks.json)；只驗custody與Boolean算術 |
| root 污染／覆寫 | 缺少完整標記列與排他建立均拒絕 | 同上；預期exit 1 |
| A normal／seed17 | PASS；38 PM、24偶參考、912匹配對、928區域、28三-spoke七圈對 | [收據](A/VERIFICATION.json)；active `certificate-v2.json` |
| A 完整補圖控制 | 安全Q前後完整補圈(7,8,5)→(15,5)，奇數2→2；M0為偶20圈 | 有限平面圖，未主張來源、最小性或marked-six |
| B normal／seed17 | PASS；32完整列、12非空列、15內部匹配、六個三-spoke局部相容態 | [收據](B/VERIFICATION.json)；雙重獨立重建，所有空格及完整片段保留 |
| C normal／seed17 | PASS；25份非共端e-spoke／f-cycle標記位置，各有完整六割及兩側圈 | [收據](C/VERIFICATION.json)；有限double-cap校準 |
| A/B/C 污染／覆寫 | 全部預期拒絕 | 各分支收據；B另核對缺空列及改完整片段兩種污染 |
| root整合重播A/B/C | 全部exit 0 | [收據](integration/replays.json)；root獨立執行分支checker |
| 三路紙證交叉審查 | 均通過 | A/B/C的`REVIEW-INTEGRATION.md`；不以Python取代任意大小論證 |
| `lake build` | exit 0，8832 jobs；既有linter warnings保留 | [收據](integration/lake.json)；僅既有Lean庫，沒有新Lean theorem |
| `scripts/check_docs.py` | exit 0；693 Markdown、9120連結 | [收據](integration/docs.json)；正式文件、anchor、索引、交接與guide欄位 |
| formal-docs DocGraph | exit 0；97 documents、383 relations、12 families、零error／note | 同上；`--include 'docs/**/*.md'` |
| scoped DocGraph | exit 0；同為97個具metadata文件，零error／note | 同上；另include本輪audit Markdown，不把無metadata紙證視為形式依賴證明 |

本輪任意大小結論是紙面層：完整區域避H時的實際嚴格下降，以及具名
`Y=X−{a}` 排除主動f七圈的e-spoke。有限checker只校準完整局部關係、固定圖
與集合／邊／完整補圈計算。真正最小來源供應 **not triggered**。

本輪沒有重跑whole-tree DocGraph、舊大型來源枚舉、九框精確計數或整套工具測試；
沒有宣稱全樹文件無錯或新紙證已Lean化。數學來源、舊封存證據不改寫。
本輪只有新audit及Kempe導覽／STATUS變動，沒有commit或push。

最後的新audit Markdown本地連結與工作樹空白檢查另見
[final-checks](integration/final-checks.json)；本audit內容的獨立hash seal見
[SHA256SUMS](SHA256SUMS)。hash seal不包含自身。
