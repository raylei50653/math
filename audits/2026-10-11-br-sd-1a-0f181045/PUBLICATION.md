# BR-SD-1a audit 的 Git 發布階段

2026-10-11。使用者在獨立驗證完成後明確授權 `commit + push`。
本階段發布既有 audit 封存與必要 archive 資料；原 REPORT／PROOF／authority／seal
均保持其封存時 bytes。它們的「未 commit／push／發布」描述原稽核階段。
Git 發布結果以當前 commit／remote 回讀為準，不將歷史欄位覆寫。

## scope 與證據

發布內容只包含本 BR-SD-1a audit、追加的 compressed blobs、ARCHIVE索引與相應 .gitignore路徑。
原65 sealed payload、680舊檔與所有負控制保持原bytes；額外publication receipts分開保存。
紙面來源矛盾仍限原明列 no-U／long L／真pair short S、split22／三環單bridge無旁支合同。
沒有新增actual target來源或Lean theorem，也沒有修改 canonical採納／OPEN分類。
README、HANDOFF、STATUS及研究線導覽保持現狀；這次直接發布audit，不另進行研究狀態整合。

## 發布後重播

fresh checkout先還原compressed archive原路徑：

```sh
python3 tools/audit_archive.py restore
python3 -B audits/2026-10-11-br-sd-1a-0f181045/verify.py --check
python3 -B audits/2026-10-11-br-sd-1a-0f181045/agents/controls/checker.py --check --certificate audits/2026-10-11-br-sd-1a-0f181045/agents/controls/certificate.normal.json
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-br-sd-1a-0f181045/agents/controls/checker.py --check --certificate audits/2026-10-11-br-sd-1a-0f181045/agents/controls/certificate.normal.json
python3 -B audits/2026-10-11-br-sd-1a-0f181045/independent_fibres.py --check --certificate audits/2026-10-11-br-sd-1a-0f181045/agents/controls/certificate.normal.json
```

`verify.py --check`核原frozen／指定Git blobs／seal，適用發布後HEAD。
`--live`另外固定HEAD=0f181045及原tracked/index／exclusive-write狀態，
只是原執行時custody模式；新增commit後不再適用，不能把預期HEAD drift當原證據損壞。
原checker不為配合publication改寫。

本階段重播、lake build、archive增量與Git index原bytes還原核對見publication/ receipts。
lake build通過只核目前repo既有Lean建置，不表示本紙面矛盾已Lean化。
原大枚舉與一般來源搜尋沒有重跑。
