# W7 38型排除與兩型原面點：相連證據發布核對

2026-10-21；Git BASE `d23f94f739468593db653ec03f903c30adfd5fb0`。
使用者要求整理進展並 commit + push。本次只發布五組既有相連研究與對應文件；
數學命題、完整前提、原40型已排38型及兩型OPEN停止點見
[整理紀錄](../../docs/history/2026-10-21-w7-remaining-two-publish.md)。
本次不擴大研究枚舉，不新增來源排除或Lean定理。

## 保存與可攜性

[來源清單](source-inventory.json)凍結84份原研究產物與13份不可變重播依賴，
去重後共97個檔案、33,673,758 bytes。原研究證明、證書、logs與receipts保持bytes。
[SOURCE_SHA256SUMS](SOURCE_SHA256SUMS)可從專案根目錄逐檔核對；四個舊routing
文件的歷史雜湊另列，兩份即時導覽變動不冒充數學輸入漂移。

全部13份舊依賴已在Git，五組新產物沒有被忽略的缺件。三個大型資料檔已為
既有gzip，直接納入Git；沒有改變壓縮內容、archive index或artifact例外。
本次獨立只讀審查與隔離staged來源重播均另存本目錄。

## 實際檢查

[重播紀錄](replay.json)列出六個原checker各normal與seed17 optimized的12次
完整命令、退出碼、耗時與新log SHA；使用原負控制，不傳`--build`。
[發布檢查](checks.json)分開記錄Lean、文件、stage artifact policy、
whitespace、來源保存與可攜重播結果。正式docs DocGraph與全樹歷史
frozen／scratch duplicate-ID診斷分開；不把後者寫成通過。

```bash
sha256sum --check --quiet audits/2026-10-21-w7-progress-publish-d23f94f/SOURCE_SHA256SUMS
python3 -B audits/2026-10-21-w7-transport-synthesis-d23f94f/short_check.py --controls
python3 -B audits/2026-10-21-w7-transport-synthesis-d23f94f/independent.py --controls
```

12次原checker重播全部通過，normal與seed17 optimized輸出逐字相等；
隔離staged目錄另匯出並核對全部97份來源，短證與原面點兩次重播亦通過，
見[可攜重播](portability.json)。`lake build`完成8832 jobs。文件、正式docs
DocGraph、stage artifact policy與whitespace均通過；全樹仍有72項既有
frozen／scratch duplicate-ID診斷，沒有本輪新audit出現在錯誤中。
[獨立發布審查](review.json)確認完整來源範圍、依賴與OPEN邊界。

未重新執行大型LP、數值求解、原圖廣泛枚舉或不相連研究線。
工具與Lean來源未修改；既有Lean build成功不形式化本輪紙面拓撲。
只排除具名子型，profile0／1、一般W7、J1／J2與具體較小bad仍OPEN。
發布後commit、遠端分支與CI狀態以即時Git／GitHub核對為準。
