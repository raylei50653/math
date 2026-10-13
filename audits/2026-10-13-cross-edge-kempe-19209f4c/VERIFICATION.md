# 驗證與研究更新範圍

2026-10-13，BASE=`19209f4cf68261fdce5e84a7804cfe04ae0957bf`。
完整數學結果見 [REPORT.md](REPORT.md)，固定輸入見 [BASE.json](BASE.json)。

## 1. 實際完成的核對

| 核對 | 結果與範圍 |
|---|---|
| 主要完整圖 checker | normal、PYTHONHASHSEED=17 加 DFS seed17 均 PASS，canonical certificate SHA 相同 |
| 固定圖域 | 5 圖；16 個五度輪；61 份去重原邊表；19 條相鄰五度中心邊 |
| 全部四格 | 2,440 格，含 1,063 空格；完整 J lifts 4,894 份 |
| 原圖／刪中心 | 50 個 G 列共 403 lifts；160 個 wheel-row 共 1,253 H lifts |
| 二色分量 | 7,518 份分割及 4,870 次保持 B 的單分量交換，全部保存原頂點值 |
| 獨立完整重算 | 另一支不匯入主 checker 的直接 Cartesian product 枚舉，重算 G/H/J 及二色分量／交換 |
| 跨中心完整搬運 | 14 個拒絕列／共邊查詢，8 個非空觸發，共 10 份可逆 full-lift 搬運；其餘頂點逐色不變 |
| 獨立局部邏輯 | 4,800 個字面 rim／spoke／四格校準；5,280 個抽象分量交換校準，其中 960 escapes |
| 目錄投影 | 從固定 K132 的 keys 重算 R 的全部 supersets；不重做目錄圖枚舉 |
| 破損證書 | 刪完整 H lift、改 J 色值、刪空格、改共享邊重數、破壞 Kempe 分量五類均被拒絕 |
| 獨立負控制 | 第二支 checker 另拒絕漏 J lift、填入空 J 格、漏 H lift 三類破損；原證書不變 |
| I/O | 預設只讀；明示 write 也拒絕覆寫既有證書；核對前後 artifact hashes 不變 |
| 固定輸入 | 12 個 frozen 檔均與 BASE SHA-256 相同 |
| Lean 回歸 | `lake build` 成功，8,831 jobs；既有 linter warnings 保留，無新 Lean theorem |
| 最終文件檢查 | PASS：639 Markdown、7,956 local links；本輪自有 6 份 Markdown 的 26 個 links 另核對通過 |
| 空白檢查 | `git diff --check` PASS |

主要憑據：
[controls/validation.json](controls/validation.json)、
[controls/summary.json](controls/summary.json)、
[完整壓縮證書](controls/certificate.json.gz)、
[獨立重算](review/independent_full_lifts.json)、
[獨立局部／目錄結果](review/catalogue_check.json)、
[數學審查](review/KEMPE_REVIEW.md)、
[Lean log](logs/lake-build.log)。

證書解壓後 canonical SHA-256：
`8bcc3f9dd04ae7cec9f3079797cfa669b2e111ff42a190ffbda5b80eab4575d5`。
壓縮檔 SHA-256：
`200109de855e537cbcd5871015873528afb0d2be7c3e8dcd493d34fd05750960`。

## 2. 重播

從 repository root 執行；主要 checker 與兩份獨立 checker 均預設只讀。

```bash
python3 -B audits/2026-10-13-cross-edge-kempe-19209f4c/controls/check_cross_edge.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-cross-edge-kempe-19209f4c/controls/check_cross_edge.py --check --seed 17
python3 -B audits/2026-10-13-cross-edge-kempe-19209f4c/review/catalogue_check.py
python3 -B audits/2026-10-13-cross-edge-kempe-19209f4c/review/independent_full_lifts.py
python3 -B audits/2026-10-13-cross-edge-kempe-19209f4c/review/independent_full_lifts.py --negative-controls
python3 -B audits/2026-10-13-cross-edge-kempe-19209f4c/controls/validate_controls.py
python3 scripts/check_docs.py
git diff --check
lake build
```

破損證書驗證器使用暫存目錄，證書維持原 bytes；validation 的寫入方式見
[controls/README.md](controls/README.md)。正式文件檢查及最終 hash receipts
見 [verification.json](verification.json) 及後續成功的
[verification-final.json](verification-final.json)。自有證據封存 hashes 見
[MANIFEST.sha256](MANIFEST.sha256)。不把 whole-tree DocGraph 或未執行的
外部計算列為通過；本輪未使用 Graphify，也未重跑外部論文或上游大型枚舉。

## 3. 結論層次

`triggered and holds`：固定圖上的完整雙射、計數式、共享邊相容性、單步判準。
`counterexample`：只保獨立 row／獨立 00 witness／獨立色正規化的廣義拼接。
`not triggered`：實際最小目錄外 Σ=933／941；n5≥9／8 的來源圖控制。
一般紙面定理依完整證明成立，不由有限控制的零 target 推出。

## 4. 文件核對及保留邊界

Closure scope：五度輪的完整 J_e 跨邊雙射、相鄰五度中心搬運、加權計數式及
一次保持原框的單分量 Kempe escape 判準；包含逐邊量詞修正及完整負控制。

Canonical Source：新增 `docs/c5_cross_edge_kempe.md`，連向本隔離報告與證據。
Updated：Kempe 導覽相關子節、STATUS 索引，以及兩份指定來源和五度輪來源的
有日期後續連結。原逐邊證明、原證書及其他工作者的隔離目錄保持不動。

Reviewed-unchanged：README／HANDOFF 的研究線入口與 tags 未改變，按現行
DOCUMENTATION.md 無需加入逐輪摘要；W5 marked relation 的既有重數重建及
一般縮減 OPEN 語義未變。較早來源正文保留當輪停止點，由頁首連到本輪結果。

Remaining OPEN：強制邊界自由分量或多步 escape、非相鄰中心的普遍 witnesses
同步、933／941 排除、一般 K∞=K≤5 及新結果 Lean 化。
Propagation stop：L2，沒有父題來源排除或全域主命題 closure，無須改跨線 synthesis。
本輪沒有 commit 或 push。

執行期間另一路修改了外圈 C7 與 N2 文件；本輪的數學输入仍固定在 BASE 的
九／八下界，不把並行成果算入本輪證明或驗證。後續更強度數界不影響此推導。
共享文件僅加入本輪直接連結，保留其他工作的內容；不把整份工作樹 diff 都算作
本輪變更。文件全域检查的第一次收尾重播曾遇到四個其他工作中尚未建立的
連結目標；第二次剩一個並行工作連結，兩次失敗均保留。最終全域檢查已通過，
見 [成功 log](logs/docs-final-v2.log)；未改動那些其他工作的目標檔以使檢查通過。
