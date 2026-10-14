# T1-CROSSCUT 採納與主工作樹整合

2026-10-14。採納原 no4ct 全域最小內點、再最大邊數來源契約下的
**`h=3⇒p=0`**。全部 PINCH／BRIDGE 排除，單接點數及兩片內部大小
無上限；RING、h≥4、一般 K∞=K≤5 仍 OPEN。既有 k 下界不提高。

權威入口是 [C8 剝層定理](../../docs/c5_c8_peeling.md#t1-crosscut)，
目前停止點見 [no4ct 交接](../../docs/tasks/c5_no4ct_handoff.md)及
[Kempe 導覽](../../docs/c5_kempe_guide.md)。本次已整合主工作樹，未 commit／push。

## 採納依據

[原審查報告](REPORT.md)、[任意來源覆蓋](review/SOURCE_COVERAGE.md)、
[完整支援論證](review/SUPPORT_LOGIC.md)與 [VERIFICATION.json](VERIFICATION.json)
構成紙面及有限計算依據。核心32項／512,568矩形已足夠；包含額外
BRIDGE 控制的64項／701,020矩形及59,156份完整 P lifts 均重播通過。
外框共同缺失列是 `01232`。這些是固定外側及支援的有限判準，任意來源
覆蓋由紙面證明承擔；沒有用固定大小圖搜尋代替無界論證。

證據層為 agent 輔助紙面審查、兩套原核對程式與另一份獨立核心重建。
原7種 disk 正控制、8項證書負控制，以及新增4項具名槽位負控制保留。
沒有新增 Lean theorem，也不稱為外部人類審查。`lake build` 是既有
形式化的回歸檢查，不能解讀為 T1-CROSSCUT 已形式化。

## 原封存與本次整合的區別

原161份證據及 [SEAL.json](SEAL.json) 保持逐 byte 不變，seal SHA256 為
`9e546e2ba778fed50a0e498a5cc3c87fe940ea097878873d6336a2ca09a996a6`。
原 REPORT／VERIFICATION 中「尚未整合 main」描述審查完成當時；本頁
记录本次採納。舊 T1 的 s=0／1 證據亦保留，原 s≥2 接續任務已被涵蓋。

原 `verify_review.py` 會要求 live 輸入等於 BASE，應留在原隔離審查環境
重播。主工作樹改用 [check_adoption.py](check_adoption.py)：

- 固定原 seal、14份 BASE 輸入、原 zip／41份 manifest 及全部已存證據；
- 只容許明列的 C8 權威頁與 no4ct 交接頁因採納而變動，輸出舊／新 hash；
- `--check` 核對封存與已存結果，重建93組 Kempe 規則及7種 disk 控制；
- `--replay` 另由原獨立 verifier 完整重算64份外側、全部矩形及 literal lifts；
- `--negative` 執行8項證書與4項具名覆蓋破損控制。

允許已採納文件更新不等於證明任意後續文字正確。本次審閱的文件與
採納程式 hash 另存 [ADOPTION_INPUTS.json](ADOPTION_INPUTS.json)。

## 封存與重播

[PACKAGING.json](PACKAGING.json) 列出97份接入既有 audit archive 的
凍結、重複及大型檔案。舊 ARCHIVE 記錄與 blob 全未改動；原檔仍在本機，
repo 保存其精確壓縮 bytes，不重寫證書。
目前 checker 可直接從 archive 讀缺少的原路徑，無須先解壓全部 audit；
已用缺少全部97份原始檔的[乾淨副本](ARCHIVE_ONLY_CHECK.json)驗證。

在 repo 根目錄執行：

```sh
python3 -B audits/2026-10-14-t1-crosscut-review-77fbd5d/check_adoption.py --check --negative
python3 -B audits/2026-10-14-t1-crosscut-review-77fbd5d/check_adoption.py --replay
PYTHONHASHSEED=17 python3 -B audits/2026-10-14-t1-crosscut-review-77fbd5d/check_adoption.py --replay
python3 -B tools/audit_archive.py verify --artifacts
```

若要直接使用歷史 producer，先依 repo 說明以 `tools/audit_archive.py restore`
還原資料，再使用新輸出目錄，避免覆寫歷史證書。
本次完整驗證清單見 [INTEGRATION.json](INTEGRATION.json)，
文件傳播與未涵蓋範圍見[整合紀錄](../../docs/history/2026-10-14-t1-crosscut-adoption.md)。
