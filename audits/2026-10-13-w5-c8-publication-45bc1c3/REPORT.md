# W5／C₈ 本輪成果發布核對

2026-10-13，BASE `45bc1c3dc9dacaee1b10df9d64f1c6a27bb0e954`。
採納範圍與保留界線見[發布紀錄](../../docs/history/2026-10-13-w5-rank3-c8-apex-publish.md)。
原研究包保持 bytes；本包保存此次 replay、封存與精確提交範圍的證據。

[original-bundles.json](original-bundles.json)列兩包全部 75 檔的原 hash／大小／mode。
[archive-before.json](archive-before.json)及[archive-paths.json](archive-paths.json)
保存原封存身份與這次三個指定路徑；[archive-append.log](archive-append.log)
記錄 append 結果。舊 2,479 路徑及 1,543 blobs 的 records 均保持。

W5 主／獨立完整重播及 manifest 紀錄在 logs 的 `math-w5-publication-*`；
C₈ 主／獨立支援／兩份 dual／控制的完整 stdout、stderr 與命令結果在
logs 的 `math-c8-publication-*`。兩包皆 PASS，沒有重跑上游來源大枚舉或外部
大型證書；本輪已完成的 Lean 回歸及 seed17／負控制以原研究紀錄為準。

原封存三檔的完整 bytes 由 Git index 中 blobs 還原；其餘檔案由直接 Git
blobs 還原。發布驗證以[verification.json](verification.json)及
[custody.json](custody.json)為準，不以工作樹檔案的存在代替提交完整性。
正式文件 DocGraph 與全工作樹的既有 62 個 duplicate-ID 失敗分開記錄。

暫存快照文件檢查通過：652 份 Markdown、8,155 個 local links；正式 DocGraph
62 文件／213 關係／5 families、零錯誤；工具測試 56 項通過。後兩項結果
由本輪工具輸出記錄，未另捕捉 raw log。產物政策與暫存空白檢查亦通過。
快照準備時的跨檔案系統及四份上游次級封存缺檔已修復，嘗試紀錄保留。

其他 Cell 翻邊工具、K4 研究與文件未列入白名單；共用 STATUS 只 stage 本輪片段。
推送 SHA 與即時剩餘變更由最後 Git 核對及回覆負責。
