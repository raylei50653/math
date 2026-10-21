# W7 原接觸結構與兩批八型排除整理發布

2026-10-21；發布前 Git BASE `30f2d19275657393b7354ed75eca31439d8ee12b`。
本次依使用者要求整理並 commit + push 三組相連成果：
[原接觸結構](../../audits/2026-10-21-w7-structural-30f2d19/REPORT.md)、
[原 u3v 八型排除](../../audits/2026-10-21-w7-u3v-30f2d19/REPORT.md)、
[原 u1v 八型排除](../../audits/2026-10-21-w7-u1v-30f2d19/REPORT.md)。
原研究報告與 receipts 的「未提交／未push」保留當輪語境；
本次重播與保存核對另見[發布報告](../../audits/2026-10-21-w7-structural-publish-30f2d19/REPORT.md)。

嚴格941／J1 only-R／W7契約下，原接觸112→69，實際正witness的必要覆蓋限40型；
原u3v與u1v的兩批各八型，再以同一D完整fibres的字面Kempe作用分別排除。
目前剩24型：12份B-joined二欄型、12份全15欄型，均只列必要覆蓋。
完整原接觸、原弦與target欄ID保留於
[24型殘餘](../../audits/2026-10-21-w7-u1v-30f2d19/RESIDUAL.json)。

兩批排除均使用原307,197欄及同一字面鏈
`Z44459≤Z44111≤Z44127`，以各自原邊的同色終點給零；
u1v證明沒有借用u3v前提或圖對稱。全部原私有分量與cap lifts的量詞保留。
任意k模板秩公式由紙證承擔；六模板有限重播僅核對相容性，
signed rational span不保證非負解或全域共享Z相容。

三組108份原始證據保持bytes，與90份去重BASE依賴及一份間接幾何證明，
合計123個不同來源檔案、17,029,875 bytes。既有壓縮閉包直接納入Git，
間接證明由既有封存還原；沒有新增archive records。
新checkout先還原既有封存，再核對全部來源：

```bash
python3 -B tools/audit_archive.py restore --artifacts
sha256sum --check --quiet audits/2026-10-21-w7-structural-publish-30f2d19/SOURCE_SHA256SUMS
```

本次normal／seed17重播、負控制、獨立審查、Lean及文件檢查的實際結果，
由發布報告與其驗證紀錄分開保存。原研究的六筆routing hashes只是歷史快照標記；
其中未保存的中途dirty文件不冒稱已還原，亦不列為不可變數學輸入。
正式docs DocGraph與全樹歷史duplicate-ID診斷分開記錄。

Closure scope：原完整契約內的u3v／u1v兩批八型，合計16型來源排除。
Updated：Kempe導覽、STATUS及本次發布入口；不改寫前輪40型／32型凍結報告。
Reviewed-unchanged：HANDOFF研究線、State導覽、一般來源與Lean狀態。
Remaining OPEN：其餘24型、一般W7、原必要計數錐、C7多內點、type I／更長路、
一般J1／J2、嚴格較小bad與主命題；沒有新Lean定理。
Propagation stop：L2；父W7沒有closure，無法上推一般主命題。
下一個窄義務由[Kempe導覽](../c5_kempe_guide.md)維護。
