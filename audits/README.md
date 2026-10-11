# 稽核封存與還原

本目錄保存 [D](2026-10-04-task-d/REPORT.md)、
[D₂](2026-10-04-task-d2/REPORT.md)、[D₃](2026-10-04-task-d3/REPORT.md)、
[D₄](2026-10-04-task-d4/REPORT.md)與[D₅](2026-10-04-task-d5/REPORT.md)
各自截點的獨立稽核、完整關係、空 fibres、witnesses、來源版本與成功／失敗紀錄。
原四份文件 hash 漂移及所有中途失敗保持原結果；固定 Python 證書與任意大小
紙面／外部定理、Lean 狀態分開。現行研究停止點由兩份研究線導覽維護。

## 新 checkout 的還原

小型報告、工具與 metadata 直接由 Git 保存。凍結快照、大型輸出及含歷史
whitespace 診斷的原文字，以 [ARCHIVE.json](ARCHIVE.json) 記錄原路徑、
SHA256、大小及 mode；原 bytes 按 SHA256 去重後，以 deterministic gzip
存於 `.archive/blobs/`，壓縮檔亦有獨立 SHA256。此封存不修改原 artifacts
或各稽核的 DELIVERY 表。本地原始檔仍保留，只在 Git 忽略它們的未壓縮副本。

先還原所有原路徑，再讀 snapshot 或執行原稽核封存驗證：

```bash
python3 tools/audit_archive.py restore --artifacts
python3 tools/audit_archive.py verify --artifacts
python3 audits/2026-10-04-task-d4/seal_delivery.py verify
python3 audits/2026-10-04-task-d5/seal_delivery.py verify
```

還原工具逐 byte 驗證原 SHA256 與大小；遇到不同的現有檔案會停止，
不覆寫既有研究資料。`snapshot` symlink 指向同包的 `.snapshot/`，
兩者隨原交付保持。`__pycache__`／`.pyc` 是衍生快取，不屬封存來源。

D₅ 的固定副本已包含實際 runtime 輸入，可在新的 output 路徑重播：

```bash
python3 audits/2026-10-04-task-d5/run_validation.py --scope original --output /tmp/math-d5-replay-fresh
```

詳細獨立稽核命令及信任界線見各 REPORT。這些命令保存原失敗並要求新的
output 路徑；歷史 absolute 路徑與執行時間是原紀錄，不替換成新執行資料。
大型 live `artifacts/` 仍沿用 [MANIFEST](../artifacts/MANIFEST.json) 的生成／
hash 政策；本封存另保存稽核當時的完整 bytes，不以目前 producer 重生成舊快照。
`--artifacts` 另按現行 MANIFEST 的原 SHA256／大小，從同一封存恢復160份
live大型產物；不修改MANIFEST，也不以重生成修正歷史文件hash漂移。

## 2026-10-04 發布快照

2345 個原路徑共 5,328,242,164 bytes，去重為 1437 個 blobs、
103,526,298 compressed bytes；每個 blob 小於 6 MB。
發布前以獨立的 Git index 匯出重建原路徑，核對原 D₄／D₅ DELIVERY 表，
並重播固定副本的相關 checkers。驗證範圍與下一入口見
[發布紀錄](../docs/history/2026-10-04-c5-parallel-progress-publish.md)。

## 2026-10-08 U2–U4 與交付稽核整批發布

[本批紀錄](../docs/history/2026-10-08-core44-batch-publish.md)保存U2–U4來源、
完整relation證書與四包M4／M5的595檔原交付證據。
ARCHIVE現有2388個原路徑、1,466個blobs、107,359,489 compressed bytes；
本次只追加三個原路徑與六個blobs，原2385項／1460個blob records全部保持。
新增五份MANIFEST大型證書亦可由上述`restore --artifacts`逐byte還原。
M4文件CI FAIL與M5當輪pending、原strict FAIL及whitespace保持歷史結果；
本批新的本地驗證見[publication report](2026-10-08-core44-batch-publication/REPORT.md)。

## 2026-10-11 單缺額查證與適用性

[A定理查證](2026-10-11-c5-single-deficit-biconnected-5e7a5ffd/REPORT.md)與
[B適用性](2026-10-11-single-deficit-applicability-804e3b0b1b/REPORT.md)共630檔原bytes保留。
本批依既有封存格式只追加兩audit的7個大型路徑／6個blobs；舊ARCHIVE records不改。
fresh checkout仍先用上述restore指令。A的舊live HEAD／docs checker保留當輪语境，
出版後使用[新入口](2026-10-11-single-deficit-publication/verify.py)的frozen-BASE overlay重播，
原checker與證書不改。B的原frozen-input verifier可直接在新HEAD執行。
本輪來源範圍、BR-SD-1a待獨立封存的任務與實際驗證見
[整理紀錄](../docs/history/2026-10-11-single-deficit-progress.md)。
