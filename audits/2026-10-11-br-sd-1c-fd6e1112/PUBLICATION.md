# BR-SD-1c audit 的 Git 發布階段

2026-10-11。Owner 在完成獨立審查與封存後明確授權「整理後 commit + push」。
本階段發布既有 audit；原 REPORT／PROOF／MAPPING／authority／seal／reviews／controls
保持原 bytes，原文件的「未 commit／push」描述原執行時點，不改寫成後來的發布狀態。
Git 發布結果以提交、tracking ref、遠端 main 與工作樹的實際回讀為準。

## 提交範圍與數學界線

只提交本 `audits/2026-10-11-br-sd-1c-fd6e1112/` 及本發布說明／必要 receipts。
原90個檔案的 SHA256／size／mode 先保存於 [original-bundle](publication/original-bundle.json)。
按 repo 既有 `tools/audit_archive.py` 選取規則核本 audit，沒有 snapshot、大於等於1MB或
歷史 whitespace 檔需另行壓縮；見 [archive-policy](publication/archive-policy.json)。
因此全部直接作普通 Git files，ARCHIVE、compressed blobs、.gitignore 不需變動。

發布內容仍只支持 REPORT 的原 N45-S-NOU-LS-PAIR split22／單一原 W 接 J1或J2、
保 actual S pair support 及未改動 J3／q 外臂的任意大小 scoped exclusion。
原 palettes／source-realizability／finite／Lean 層級與所有 OPEN 邊界不變。
本階段没有 canonical 採納；共享 README／HANDOFF／STATUS、研究線導覽、N45 canonical
及 BR-SD-1a／1b 保持原 bytes。直接發布 audit，不以 Git push 裁決父身份或一般 Gallai trees。

## 發布後只讀重播

```sh
python3 -B audits/2026-10-11-br-sd-1c-fd6e1112/verify.py --check
python3 -B audits/2026-10-11-br-sd-1c-fd6e1112/agents/controls/checker.py --check --certificate audits/2026-10-11-br-sd-1c-fd6e1112/agents/controls/certificate.normal.json
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-br-sd-1c-fd6e1112/agents/controls/checker.py --check --certificate audits/2026-10-11-br-sd-1c-fd6e1112/agents/controls/certificate.normal.json
python3 -B audits/2026-10-11-br-sd-1c-fd6e1112/agents/controls/independent_edges.py --certificate audits/2026-10-11-br-sd-1c-fd6e1112/agents/controls/certificate.normal.json
```

`verify.py --check` 核81 sealed payloads、17 frozen authority inputs與指定 BASE Git blobs，
適用發布後 HEAD。`--live` 另固定原 HEAD=fd6e1112及當時 tracked/index/exclusive-write 狀態，
只適用研究執行時點；提交後不以預期 HEAD／index drift 宣稱原封存損壞，也不改寫原 verifier。
本 audit 所有新資料直接入 Git，無需為這份 audit 還原壓縮路徑。
controls checker 另綁五份 live provenance 的 hash；本次沒有更改它們，故重播適用。
若將來 canonical／舊 provenance 有授權變更，請回到此發布 snapshot 重播 controls，
分清 provenance drift 與数学失效，不為求 PASS 改写原證書或封存。

本階段的 controls／原邊 reconstruction／損壞 tuple 負控制、文件檢查與既有 Lean build
結果見 [checks](publication/checks.json)；index逐 byte 與原bundle核對見
[stage-validation](publication/stage-validation.json)。checks僅報實際執行的範圍。
既有 Lean build 不把本紙面 Gallai／source 論證提升為新增 Lean theorem。
沒有重跑原 BR-SD-1a controls、大型來源枚舉或全工作樹 DocGraph。
