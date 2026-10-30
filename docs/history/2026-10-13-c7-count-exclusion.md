# C₇ 共同計數排除 941 的最後 h=2 外圈

2026-10-13。[權威入口](../archive/reports/c5/structure/c5_neartri_boundary_collar.md)／
[完整證明與證據](../../audits/2026-10-13-c7-joint-kempe-19209f4c/REPORT.md)。
後續整理與發布見[同日整批紀錄](2026-10-13-progress-publish.md)；
下文「本輪沒有commit／push」是本次數學交付當時的狀態。

Closure scope：具名 C₇ `(a0,a1,y2,a2,a3,y4,a4)` 的既有55列上界 U，
不包含任何合法 disk 圖的完整關係。任意有限平面內側圖的共同延伸計數
由 inclusion–exclusion 落在 noncrossing equality vectors 的線性包；
七份精確恆等式迫外列 `01232` 的三個前像全拒絕。既有 fan cap 加4CT
另排除 S⊆U 本身。原最小目錄外來源因此均必 h≥3、n5≥9。

Evidence：429 partitions／91列／7恆等式，完整具名外圈 lifts，獨立標準庫
重建；沿用3,383 caps，72個通過舊必要條件的抽象關係作反控制。
四張 literal count 控制有364個完整邊界查詢、492份全圖lifts；另有獨立
topology控制及證書破壞測試。實際結果見
[verification.json](../../audits/2026-10-13-c7-joint-kempe-19209f4c/verification.json)。
普遍引理為紙面證明，表等式為精確Python證書，未新增Lean theorem。

Updated：外圈權威報告、Kempe導覽及STATUS的對應條目；直接父來源
cofacial normal form／saturation degree bound與degree5 link報告的後續摘要，
將941舊八點界更新為九點，保留各原報告當輪證據。

Reviewed-unchanged：HANDOFF與README的研究線及路由未變；W5存在與商圖
完整拉回依然有效；同期跨邊研究的條件結論不因下界變強而失效。
既有舊audit、歷史快照與ε／N2／E-ARC2來源契約未修改。

Remaining OPEN：h≥3來源、十三內點以上一般來源、普遍跨邊同步、K∞=K≤5。
Propagation stop：L2；本葉排除沒有關閉父命題，沒有新研究線或全域路由變更。
同期其他工作保留；本輪沒有commit／push。
