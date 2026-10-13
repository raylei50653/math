# K14／W5 圈秩四與組合圖譜發布核對

2026-10-13。採納範圍、信任層與OPEN界線見
[整理發布紀錄](../../docs/history/2026-10-13-k14-rank4-atlas-publish.md)。
本包只保存本次主線整合與驗證，不修改三份原audit。

## 原始 bytes

[IMPORTED.json](IMPORTED.json)保存185份原檔的SHA256／大小／mode；
[ARCHIVE_APPEND.json](ARCHIVE_APPEND.json)記錄舊records摘要及11 paths／7 blobs的追加。
[verify.py](verify.py)核對原檔集合、BASE ancestry、原bytes及舊archive records不變，
亦可從封存核對尚未restore的檔案。這是保存核對，不重證數學結論。

```bash
python3 -B audits/2026-10-13-k14-rank4-atlas-publication/verify.py
python3 tools/audit_archive.py restore --artifacts
```

Contractible原verify已在staging前通過，其歷史HEAD／空index條件不改。
三包數學checker仍按原報告重播；restore後可直接執行。

## 本次重播與限制

[驗證紀錄](validation/results.json)保存實際命令、退出碼與log入口。
K14主／獨立重播比對1,001根圖、10,010列及180,228 full lifts。
Contractible主／獨立重播覆蓋6,389模板、65,423,360 cells；essential覆蓋
2,872模板、29,409,280 cells。必要domain／計數、負控制與空fibre校準均通過。
圖譜normal／seed17、Kempe screen及132原witness核對通過。

正式文件與DocGraph、Lean回歸、儲存政策、staged whitespace及實際Git index
匯出均按本次紀錄分列。全域DocGraph保留62個既有duplicate-ID失敗。
新index子集匯出最初漏帶既有去重blob及rank3輸入；補齊已追蹤依賴並逐byte
還原後，發布保存核對與K14／essential原delivery核對通過，初次失敗logs保留。
新增歷史連結的初次錨點錯誤修正後，文件檢查通過；首次診斷亦保留。
沒有重跑完整球面生成、外部文獻計算證書或瀏覽器互動測試，沒有新增Lean theorem。
