# W7 逐型排除與原面點整理發布

2026-10-21；發布前 Git BASE `d23f94f739468593db653ec03f903c30adfd5fb0`。
依使用者要求整理目前進展並 commit + push 五組相連成果：
[證明總稿](../../audits/2026-10-21-w7-transport-synthesis-d23f94f/REPORT.md)、
[原u3w八型](../../audits/2026-10-21-w7-u3w-d23f94f/REPORT.md)、
[原u1w四型](../../audits/2026-10-21-w7-u1w-d23f94f/REPORT.md)、
[其餘十二型中的十型](../../audits/2026-10-21-w7-other-types-d23f94f/REPORT.md)、
[剩餘兩型的原面點與完整link](../../audits/2026-10-21-w7-private-face-points-d23f94f/REPORT.md)。
重播、保存與提交核對另見[發布報告](../../audits/2026-10-21-w7-progress-publish-d23f94f/REPORT.md)。

在完整原941／Q1接受零／J1 type III五邊路／嚴格only-R-W7契約下，
本輪24份必要原接觸再排22份；連同既有兩個v分支，原40型已排38型。
u3w以四推導態、29個完整incident分支排八型；u1w以五推導態、40分支排四型；
u4v、u3s、u2v、u2w四個獨立原邊引理再排十個不同full15型。
每個分支使用同一原D的全部完整fibres、原307,197欄、全部私有點與cap lifts；
沒有把v／w交換當圖對稱，也沒有拼接不同來源的可行片段。

[完整殘餘](../../audits/2026-10-21-w7-transport-synthesis-d23f94f/RESIDUAL.json)
只餘profile0無弦與profile1僅au4。前者有五個不同D私有第三面點；
後者首點必為原框點a，僅其餘四個私有。兩target中各第三點只能用0／3色。
原完整link與a／q的03分離迫一個原D私有鄰點y，色為中心的相反12色，
且它與原C7的接觸恰只有該中心。每份target著色各自存在y，不固定所有正量
共同使用同一份著色或同一個y。

令U={u4,u3,u2,u1,L}，profile1必有某個U點原度數≥6；
profile0必有n原度數≥7，或某個U點原度數≥6。這是指定低度子案排除，
沒有關閉兩個profile。完整有序接合界面的支援關係相等，加合法原外框／plane
接合與內點嚴格下降，已足以保原Σ941並使用全域最小性；目前未構造具體替代。
若另要保存現有計數模型或個別cap assignment，需另證更強的完整fibre傳輸。

本次保存84份研究產物與13份不可變重播依賴，97個不同來源檔案共
33,673,758 bytes。全部13份舊依賴已在Git，既有gzip完整殘餘直接納入提交；
沒有新增ARCHIVE紀錄、忽略規則或大型JSON例外。研究報告與舊驗證的
「未commit／未push」保留當輪語境，本次驗證與即時Git狀態另記。

Closure scope：u3w八型、u1w四型及另外十型；原40型累計38型排除。
Updated：五組相連證據、Kempe導覽、STATUS直接索引與本次發布紀錄。
Reviewed-unchanged：原三批40／32／24型的歷史凍結證據、State導覽、
HANDOFF研究線及README；一般J1兩項／J2六項與Lean邊界不變。
Remaining OPEN：兩型較高度數來源、精確必要計數錐、來源實現、具體較小
替換、一般W7／C7多內點／J1／J2、strict smaller bad及主命題。
Propagation stop：L2；具名子型排除沒有關閉父W7，沒有新Lean定理。
目前接續入口由[Kempe導覽](../c5_kempe_guide.md)維護。
