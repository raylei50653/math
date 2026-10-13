# K15／C8／無四色定理前提路線發布核對

2026-10-13。數學採納範圍、證據層與OPEN義務見
[整理發布紀錄](../../docs/history/2026-10-13-k15-c8-no4ct-publish.md)。
本包保存本次整合及驗證；不修改十份原audit。

[IMPORTED.json](IMPORTED.json)記966原檔的SHA256／大小／mode，
[ARCHIVE_SELECTION.json](ARCHIVE_SELECTION.json)限定本次封存路徑，
[ARCHIVE_APPEND.json](ARCHIVE_APPEND.json)保留原ARCHIVE摘要與追加records。
[verify.py](verify.py)核對原檔集合、BASE ancestry、原bytes及舊records保持，
亦可由gzip封存驗證未還原的原檔。保存核對不取代數學重播或來源完備性。

```bash
python3 -B audits/2026-10-13-k15-c8-no4ct-publication/verify.py
python3 tools/audit_archive.py restore --artifacts
```

本次數學重播：[22項K15／C8／W5](validation/math-results.json)、
[9項no4ct上游與接入](validation/no4ct-results.json)，全部退出0。
正常／seed17、獨立完整fibres、負控制、K15校準與W5χ控制分列。
no4ct collar的五項子檢查以唯讀NetworkX3.5路徑執行；保留原uv launcher。
新[run_no4ct.py](run_no4ct.py)僅記錄本次環境與命令，不變更原checker。

[lake build](validation/lake-build.log)完成8,831 jobs，只驗既有Lean回歸。
文件及發布檢查見validation目錄：正式docs通過，全域DocGraph的62項
既有duplicate-ID仍FAIL。初次文件missing-publication-page診斷保留；
完整文件建立後重查。Git index保存核對涵蓋每個原檔的實際staged bytes、
封存blob與mode；所有旧ARCHIVE records不變。

未重跑完整plantri生成、外部Corollary20 cone證書、歷史大規模產物生成，
未重新檢索文獻，沒有新增Lean theorem。文獻適用性及W5構造的4CT前提
保留原報告；新的no4ct接入只使用其明列的最小來源與相對大小契約。

發布檢查初次plain Python測試缺NetworkX，使用已確認3.5路徑後94項通過；
Git將一份原PDF視為文字而報whitespace，已按原bytes追加封存，原PDF保留。
初次診斷亦保存，修復儲存方式後重新核對index與whitespace。
