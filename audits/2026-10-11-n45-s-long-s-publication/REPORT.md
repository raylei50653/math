# N45-S-LONG-S 相連證據發布

2026-10-11；BASE `f2692089ad4259808e27d9b7e882ac09505b180a`。
使用者明確要求commit＋push。提交包含15棵既有worker／review／派工／closeout目錄、
本發布紀錄、五份相連研究文件、一份採納history，以及必要archive index／ignore／新blobs。
最終commit、本地／tracking／remote main及工作樹狀態以Git即時回讀為準。
既有sealed reports的pending、shared_documents_updated=false及未commit／push保其原截點語境。
沒有修改原交付、證書或任何已封存review／closeout bytes。

完整研究scope、上游信任鏈、更正overlays與OPEN界線見
[N45§2.10](../../docs/c5_excess_two_nonadjacent_unit_core45.md#210-n45-s-long-s完整-cu-與原-r-fibre-恢復的限定覆蓋)及
[採納紀錄](../../docs/history/2026-10-11-n45-s-long-s-adoption.md)。
發布不增加來源排除、source realizability、Lean或一般N45／N2／E closure。

## 原bytes與archive

[plan.json](plan.json)固定15棵相連目錄的1,727 regular files／166,489,899 bytes及原SHA／mode。
沒有symlink、empty directory、cache或局部repository需要額外搬運。
只將這15棵原目錄、舊ARCHIVE index與gitignore複本供給隔離root，執行既有
`python3 -B tools/audit_archive.py append --repo <isolated root>`；沒有全域掃舊audits。
原23個≥1 MB輸出共146,081,323 bytes按原SHA去重，沿用3個舊blobs，新增16個gzip blobs
共2,845,190 bytes。所有23路徑round-trip逐byte相等，原2391 paths／1469 blob records全不變。
詳見[archive-command.json](archive-command.json)與[archive-checks.json](archive-checks.json)。
原未壓縮檔保留本地；新checkout從archive還原其原路徑、SHA、大小與mode。

## 新checkout與驗證

先依既有還原入口補齊歷史相連資料，然後執行不依賴live shared pins／HEAD==BASE的封存檢查：

```sh
python3 tools/audit_archive.py restore --artifacts
python3 audits/2026-10-10-n45-publication/archive.py restore
python3 -B audits/2026-10-11-n45-s-long-s-publication/verify_payload.py --check
python3 -B audits/2026-10-11-n45-s-long-s-closeout/verify.py --check
python3 -B audits/2026-10-11-n45-s-long-s-t2-q0-restore-review/seal_review.py --directory audits/2026-10-11-n45-s-long-s-t1-rfibre-review --check
python3 -B audits/2026-10-11-n45-s-long-s-t2-q0-restore-review/seal_review.py --directory audits/2026-10-11-n45-s-long-s-t2-q0-restore-review --check
python3 -B audits/2026-10-11-n45-s-long-s-t2-q0-restore-review/seal_review.py --directory audits/2026-10-11-n45-s-long-s-t2-q2-restore-review --check
python3 -B audits/2026-10-11-n45-s-long-s-t2-q0-restore-review/seal_review.py --directory audits/2026-10-11-n45-s-long-s-block-transfer-review --check
python3 -B audits/2026-10-11-n45-s-long-s-t2-q0-restore-review/seal_review.py --directory audits/2026-10-11-n45-s-long-s-closeout --check
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
```

本輪從Git index匯出獨立快照，按上述還原入口核原15目錄所有1,727檔案，以及相連review／closeout完整seal。
實際命令／stdout／stderr／exit、fresh還原範圍與文件檢查見
[publication-checks.json](publication-checks.json)，各項原生輸出亦各自保存。
fresh export還原後，全部15目錄1,727檔案的SHA／size／mode相等，closeout guard、
四新review及closeout完整seal、文件連結與formal docs DocGraph均實跑exit0。
Git index核1,704個普通原檔精確stage、23個原檔由archive還原，沒有未封存的ignore漏列；
所有新增blobs均stage，範圍核對見[index-coverage.json](index-coverage.json)。
不重跑要求舊live shared文件零漂移的worker checkers、舊19 controls或缺BASE blobs有限鏈。
本地收尾已實跑lake build且其後沒有Lean變更，沿用該成功紀錄；沒有新Lean形式化宣稱。
正式docs與全工作樹DocGraph分開；後者的62項歷史duplicate-ID保留，未宣稱全域PASS或重跑。
README／HANDOFF路由與標記無變動，不為發布重寫；數學文件傳播仍停L2。
