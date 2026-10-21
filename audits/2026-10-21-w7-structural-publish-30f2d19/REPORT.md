# W7 結構與 u3v／u1v 相連證據發布核對

2026-10-21；Git BASE `30f2d19275657393b7354ed75eca31439d8ee12b`。
使用者要求整理進展並 commit + push；本次發布三組既有相連審核及對應文件。
數學結論、完整前提與24型停止點見[整理紀錄](../../docs/history/2026-10-21-w7-structural-publish.md)。
本次不新增來源排除或Lean定理，保留原研究報告與驗證紀錄的bytes。

## 保存範圍

[來源清單](source-inventory.json)記錄108份新audit產物、90份BASE凍結依賴，
另加一份間接幾何證明；重疊去重後共123檔、17,029,875 bytes。
[SOURCE_SHA256SUMS](SOURCE_SHA256SUMS)從專案根目錄核對全部原bytes。
三組BASE的非routing輸入逐項對回原SHA與大小，沒有科學輸入漂移。
原u3v完整八型閉包保留既有gzip，無需新增ARCHIVE、忽略規則或大型JSON例外。

六筆原routing-snapshot hashes保留在清單中作歷史標記；其中中途dirty
routing的bytes未由原審核保存，因此不宣稱還原那些中間文件。
這些標記不作不可變數學輸入；本次STATUS／guide變動由Git diff與文件審查核對。
原研究的`commit_push_run:false`等欄位不改寫；發布以即時Git狀態為準。

## 驗證與重播

本次按三份`research-checks.json`的原命令重播，保留各自normal及
`PYTHONHASHSEED=17`設定；u3v／u1v的seed17另使用原`-O`設定。
完整命令、exit code及新log SHA見[重播紀錄](replay.json)。
28次重播均通過，含原負控制；三組108份原產物的bytes與舊proof／log hashes不變。
兩組獨立只讀審查分別核對structural與u3v／u1v，摘要見[審查紀錄](review.json)。
隔離index來源的重播另核對封存還原與間接依賴，見[可攜重播](portability.json)。
Lean、文件、工具測試、stage artifact與whitespace檢查見[發布檢查](checks.json)。
`lake build`完成8832 jobs；鎖定依賴環境的94項工具測試及18項DocGraph測試通過。
全樹DocGraph的既有72項frozen／scratch重複ID另存診斷，不視為正式docs失敗。

```bash
python3 -B tools/audit_archive.py restore --artifacts
sha256sum --check --quiet audits/2026-10-21-w7-structural-publish-30f2d19/SOURCE_SHA256SUMS
python3 -B audits/2026-10-21-w7-u1v-30f2d19/closure/compact.py --controls
python3 -B audits/2026-10-21-w7-u1v-30f2d19/closure/source_bridge.py
```

未重新執行大型LP、數值試跑、原圖廣泛枚舉或不相連研究線；
完整來源的紙面量詞、有限邊界證書及Lean既有build分開。
一般W7、原必要錐、其餘24型、J1／J2、較小bad與主命題仍OPEN。
