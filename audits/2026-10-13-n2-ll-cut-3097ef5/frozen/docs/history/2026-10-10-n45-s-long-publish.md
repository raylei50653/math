# 2026-10-10：N45-S 含 long 契約與 U 在 r 的限定排除發布

BASE `0d76c4c887033e565eaa0ca4d2a515619d7c97f3`。
使用者明確要求 `commit + push`；本輪提交兩份相連交付、四份文件更新與必要封存資料。
最終 commit／origin 狀態以 Git 即時回讀為準；原報告「未 commit／push」保留交付時語境。

[同源契約與必要化約](../../audits/2026-10-10-n45-s-long-contract/REPORT.md)
保完整原 U／long L／short S，只刪原 r-spoke e，且 X=G−e=M 自身 minimal；
原盾弧費、zero-slack、十 literal 列、全 root pins／空 fibres及恢復 e 分層核對。
[SL-MAP-R](../../audits/2026-10-10-n45-s-long-r-map/REPORT.md)
另限定 U owner=r，實際 sole C、X 自己的 witnesses與精確 F 接回 BASE(5)/(4)/(3)，
pair／singleton S 皆排除。紙面依 BASE／外部 Gallai；有限介面校準來源仍 not triggered，
沒有新 Lean theorem。U owner=s 的 actual C/U、無 U 的 long／兩 long、其他 core 與一般 N2／E仍 OPEN。
目前停止點見 [Kempe 導覽](../c5_kempe_guide.md)。

## 原 bytes 封存與重播

兩個 delivery manifests 的60／40份 payload全部核回；原檔與失敗版保留。
三份大型證書共100,441,362 bytes，使用既有 [audit archive](../../tools/audit_archive.py)
新增三個content-addressed gzip blobs，共1,999,113 bytes。
append在只含本輪兩個目錄、既有索引／ignore複本的隔離repo執行，
沒有掃入其他舊audits或MANIFEST artifacts；全部舊archive records不變。
三份compressed／uncompressed hashes及fresh round-trip bytes均相等，見
[封存檢查](../../audits/2026-10-10-n45-s-long-publication/archive-checks.json)。
runtime cache留本地、未發布；前輪directory inventory的cache差異及所有FAIL保留，
不宣稱整棵歷史worker directory零漂移。原delivery shared hashes保交付時快照，
STATUS新增本頁索引後不再稱其舊hash為current。

新checkout按既有順序還原封存；本輪三證書在第一步由通用索引還原，
第二步供給既有N45報告的相連歷史證據。checker所需BASE commit須在Git歷史內。

```sh
python3 tools/audit_archive.py restore --artifacts
python3 audits/2026-10-10-n45-publication/archive.py restore
python3 -B audits/2026-10-10-n45-s-long-contract/checker.py --check
python3 -B audits/2026-10-10-n45-s-long-r-map/checker.py --check
```

兩checker在交付時normal／seed17均已實跑一致，負控制與frozen漂移核對皆通過；
發布文件／封存檢查另見
[publication checks](../../audits/2026-10-10-n45-s-long-publication/publication-checks.json)。
沿用此前成功的lake build，之後沒有Lean變更；未重跑build或whole-worktree DocGraph，
不宣稱紙面已形式化或歷史duplicate IDs已消除。README／HANDOFF無新路由語義，停止L2。
