# T1 一般正對切口定理：採納與證據整合

2026-10-14。研究及審查 BASE `77fbd5da7ba273f0af7c75175dc08376d2282f46`。
已整合主工作樹，未 commit／push；即時提交狀態以 Git 為準。

同日後續：[C4／T1／Lean 整理發布](2026-10-14-c4-t1-lean-progress-publish.md)
記錄本次使用者授權的 commit＋push、共同 k≥23 的界線同步與重播；下文保留採納當輪語境。

**Closure scope：** 在原 no4ct 全域最小 C5 來源契約下，`h=3⇒p=0`。
全部 PINCH／BRIDGE 排除，不限制單接點數或兩側內點數。
原 s≥2 逐級任務被一般定理涵蓋，第一剝層改從 RING 接續。

**Canonical Source + Evidence：** [C8 剝層／T1-CROSSCUT](../c5_c8_peeling.md#t1-crosscut)
為權威入口，[採納記錄](../../audits/2026-10-14-t1-crosscut-review-77fbd5d/ADOPTION.md)
接原來源覆蓋、完整支援論證及有限證書。核心32項／512,568矩形足夠；
含額外控制的64項／701,020矩形、59,156份 P lifts 全通過，共同缺失
接受列為01232。證据是紙面＋Python；沒有新增 Lean theorem。

**Updated：** C8 權威頁、[no4ct 交接](../tasks/c5_no4ct_handoff.md)、
[Kempe 導覽](../c5_kempe_guide.md)、[STATUS](../STATUS.md)已更新採納狀態、
停止點及重播入口。原 audit 的161份封存證據和舊 T1 歷史結果未改寫；
97份大型、凍結或重複 payload 接入既有 archive，保留精確 bytes。

**Reviewed-unchanged：** C8 apex／inner-collar 的來源引理與下界仍有效，
其八項無界來源 OPEN 與 RING 殘留相容。共同語言與 research synthesis
沒有依賴 s≥2 作當前 C8 停止點，一般主命題仍 OPEN。研究線、活躍標記
及根入口路由未變，HANDOFF 無須修改。README 與 workflow 的既存本地
改動保持原 bytes，未混入本次研究修改。

**Remaining OPEN：** RING、h≥4、一般來源縮減與 `K∞=K≤5`。
既有一般 k≥16、h=3⇒k≥19 不提高，不將十九內點界套到 h≥4。

**Propagation stop：** 停在直接父主題及 consumers（L2）；
沒有研究線增減或全域命題 closure，不改寫其他線與歷史快照。

實際重播、archive、文件、既有 Lean 回歸與生成物檢查結果見
[INTEGRATION.json](../../audits/2026-10-14-t1-crosscut-review-77fbd5d/INTEGRATION.json)。
全樹 DocGraph 的 frozen duplicate-ID 歷史另外記錄，不刪除歷史證據來
製造 PASS；正式 docs 檢查與全樹結果分列。
