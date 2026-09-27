# degree-5／R 系列導讀：介面、排除範圍與保留缺口

後續（2026-09-27）：[root 守恆全表掃描](c5_single_spoke_root_sweep.md) 將通用
單接點條件套用到 114 筆，新增 14 個接受查詢；目前 80 筆兩列已證、34 查詢未決。

後續（2026-09-27）：[單接點未用色守恆](c5_single_spoke_root_conservation.md)
已證 (012,04,234)、禁 3 者二接點的 p₂ 延拓；目前 66 筆兩列已證、
48 查詢未決。下文數字與停止點保留各原輪次語境。

後續（2026-09-27）：[旁支 K5 minor](c5_single_spoke_branch_minor.md) 已證
指定 (01,04,1234)、禁 3 者二接點分支的 p₁ 延拓；114 筆現為 64 筆
兩列已證、50 個指定查詢未決。下文保留原輪次結論及數字。

後續（2026-09-27）：[single-spoke 外部雙路徑 completion](c5_single_spoke_completion.md)
保留同圖二接點分量，沿用 degree-4 分類及既有有限完整關係證書；
(2,1,1) 的 114 筆配置中現有 62 筆兩個指定 p 已證，52 筆各剩一列。


後續（2026-09-27）：[single-spoke 必要化約](c5_single_spoke_cores.md) 完成 t=1
四型不可刪減覆蓋、接點區塊與反射；(2,1,1) 只剩 19 種必要實際支援型，
已完成部分指定 p 延拓，全部 t=1 仍未解。t=2 已由 [非相鄰分離](c5_two_spoke_nonadjacent.md)
及既有結果完成出口接合；下文舊停止點保留歷史語境。


後續（2026-09-24）：[未接內點引理](c5_unattached_boundary.md) 已證 (3) 非相鄰
S={b0,b3} 型只缺 q；雙缺失目標尚餘 23 個兩-spoke 配置待分離。

後續（2026-09-24）：[兩-spoke 區域化約](c5_degree5_two_spoke_sectors.md)
將 t=2 的 (3)／(2,1) 收窄為 24 個必要配置；尚未完成這些核心的分離。

文件整理：2026-09-23；研究依據截至 2026-09-22。本頁不新增研究結論。
研究優先序只見 [HANDOFF](HANDOFF.md)，全專案索引見 [STATUS](STATUS.md)。
前置的樹、triangle、長奇環與 K4 依賴見 [全 degree-4／block 導讀](c5_degree4_guide.md)。
此處 R9–R31 是研究輪次；不是其他報告參考文獻中的 [R1]、[R2] 編號。

## 1. 目前完成到哪裡

**一般 degree-5 排除仍未完成。** 在唯一 degree-5 內點 z 有三條 boundary
spokes、C=H−z 為連通二接點分量、其餘有效內點完整 degree=4，且來源是
接受全部 T4 的 C5 disk minimal q-obstruction 的指定前提下，已有：

| 分量或接點型 | 現況與結論入口 |
| --- | --- |
| 樹；恰一個 odd-cycle block，其餘 bridges | [R12](c5_degree5_tree_components.md)、[R13–R14](c5_degree5_odd_cycle_components.md) 任意大小排除 |
| 恰兩個 odd-cycle blocks，其餘 bridges | 互斥型 [R22](c5_degree5_two_long_cycles.md) 與共用點型 [R24](c5_degree5_shared_cycle_minors.md) 合成完成；環長、外臂不限 |
| 三環共用點鏈，兩臂各在末端私有點 | [R27](c5_degree5_three_cycle_minors.md) 任意長來源 minors 與拓撲合成完成 |
| 同一三環鏈，兩個不同私有接點在中間環 | [R29–R30](c5_degree5_middle_cycle_minors.md) 正常形及任意長來源排除完成 |
| 同一三環鏈，兩個不同接點在同一末端環 | [R31](c5_degree5_same_terminal_triangles.md) 僅完成正常形；任意長來源 minors 待補 |
| 末端與中間、同點會合、環間 bridge、一般三環／更多環、其他 degree-5 分拆 | 未由上述指定型排除涵蓋 |

三環共用點鏈指 J1∩J2={r12}、J2∩J3={r23}、J1∩J3=∅、r12≠r23。
表中是各篇紙面化約與有限證書的合成範圍；詳細前提以原報告為準。
[R9](c5_k4_blocks.md) 的全 degree-4 **整圖**結論不能直接套到帶 z 的分量。
R31 是保留缺口；目前研究優先序仍由 HANDOFF 管理。

## 2. 符號與證據界線

- R10 對任意 proper boundary row b 定義共同接點關係 R_C(b)、禁色 F_C(b)
  與 z 的可用色 A_z(b)。精確接合為 `Z_G(b)=A_z(b) \ ⋃_C F_C(b)`；
  可延拓 iff Z_G(b) 非空。同一分量的端點 marginals 不能相乘代替共同關係。
- R11 起聚焦三-spoke 分拆 (2)：z 剩餘兩條內邊進入同一分量 C。
  原框 q=(A,B,A,B,C)，D 為第四色；區域框 (z,b1,b2,b3,b4) 的 D 列為
  (D,B,A,B,C)。這個區域重寫不自動接受全部 T4。
- 固定 q 的「四列」是逐一查詢四個 z 色，須保留完整 F_C(q)，不能只驗拒絕 D。
  它不等於全部 boundary rows 的完整 Σ，亦不保證完整 root 關係或任意 pinning。
- 介面等價、有限正常形非 disk 覆蓋、任意長來源的 boundary 固定 minor
  是不同證據步驟。須保留實際 attachments、共同色框、degree、逐邊刪除著色，
  並將正常形拓撲證書合成回同一來源圖。
- 任意大小推論依原報告的紙面化約及所引用的外部 degree-list 定理；
  Python 保存固定域控制／minor 證書。[Lean 接合基礎](lean_root_interfaces.md)
  支援一般代數步驟，未形式化整套 Gallai／disk／來源 minor 論證。

## 3. R9–R31 閱讀與後續對照

先讀 R9–R11 確认整圖與分量的差別，再按需要選零／一環、雙環或三環分支。
以下各列記錄報告的保留用途；已被後續補完的舊停止點不另列為待辦。

| 輪次與報告 | 成果及後續關係 |
| --- | --- |
| [R9：全 degree-4 合成](c5_k4_blocks.md) | K4 排除與既有 block 分類合成；唯一 degree-5 的完整介面由 [R10](c5_degree5_interfaces.md) 接續。 |
| [R10：完整多接點介面](c5_degree5_interfaces.md) | 染色與 minimality 介面已完成；[R11](c5_degree5_sectors.md) 起處理三-spoke 分拆 (2)，一般 degree-5 幾何排除仍開放。 |
| [R11：三-spoke 區域定位](c5_degree5_sectors.md) | 兩個鏡像 pentagon 化約保留；[R12](c5_degree5_tree_components.md) 至 [R24](c5_degree5_shared_cycle_minors.md) 已處理零／一／二環，分拆 (2) 整體仍開放。 |
| [R12：任意樹與 K4 引理](c5_degree5_tree_components.md) | 任意樹排除完成；單環由 [R13–R14](c5_degree5_odd_cycle_components.md)、雙環由 [R15–R24](c5_degree5_shared_cycle_minors.md) 接續完成。 |
| [R13：單 triangle](c5_degree5_triangle_components.md) | 指定單 triangle 分量排除完成；[R14](c5_degree5_odd_cycle_components.md) 已補任意單奇環。 |
| [R14：任意單奇環](c5_degree5_odd_cycle_components.md) | 單奇環加 bridges 排除完成；雙環由 [R15–R24](c5_degree5_shared_cycle_minors.md) 接續完成。 |
| [R15：共用點雙 triangles](c5_degree5_shared_triangles.md) | 共用點型排除完成；互斥 triangles 由 [R16–R19](c5_degree5_bridge_mark_minors.md)、共用點長環由 [R23–R24](c5_degree5_shared_cycle_minors.md) 補完。 |
| [R16：互斥 triangles 的 bridge](c5_degree5_bridge_triangles.md) | 直接私有接點與旁支化約保留；任意外臂及同點接入由 [R17](c5_degree5_bridge_arms.md) 與 [R18–R19](c5_degree5_bridge_mark_minors.md) 補完。 |
| [R17：不同環點的任意外臂](c5_degree5_bridge_arms.md) | 不同環點接入排除完成；至少一側同點接入由 [R18–R19](c5_degree5_bridge_mark_minors.md) 補完。 |
| [R18：同點標記介面](c5_degree5_bridge_marks.md) | 標記介面與正常形保留；[R19](c5_degree5_bridge_mark_minors.md) 已補真正來源 minors 及完整接線拓撲覆蓋。 |
| [R19：同點來源 minors](c5_degree5_bridge_mark_minors.md) | 結合 R15–R17 完成恰兩個 triangles；含長環的雙環由 [R20–R24](c5_degree5_shared_cycle_minors.md) 補完。 |
| [R20：長環加 triangle 的四列介面](c5_degree5_long_triangle_roots.md) | 完整條件 root 介面保留；[R21](c5_degree5_long_triangle_minors.md) 已補混合雙環來源 minors 與圖層排除。 |
| [R21：混合雙環來源 minors](c5_degree5_long_triangle_minors.md) | 互斥混合雙環排除完成；[R22](c5_degree5_two_long_cycles.md) 補雙長環，[R24](c5_degree5_shared_cycle_minors.md) 補共用點型。 |
| [R22：互斥雙長環](c5_degree5_two_long_cycles.md) | 互斥雙奇環任意長度排除完成；共用點型由 [R23–R24](c5_degree5_shared_cycle_minors.md) 補完。 |
| [R23：共用點四列介面](c5_degree5_shared_cycle_roots.md) | 四列布林縮環與完整 root 不保持的控制保留；[R24](c5_degree5_shared_cycle_minors.md) 已補圖層來源 minors 及排除。 |
| [R24：共用點雙奇環來源 minors](c5_degree5_shared_cycle_minors.md) | 結合 R22 完成恰兩個 odd-cycle blocks；指定三環鏈由 [R25–R27](c5_degree5_three_cycle_minors.md) 接續，一般三環仍開放。 |
| [R25：末端各一臂的三環介面](c5_degree5_three_cycle_roots.md) | 完整有序接合保留；[R26](c5_degree5_three_triangles.md) 完成正常形，[R27](c5_degree5_three_cycle_minors.md) 完成此型任意長來源 minors。 |
| [R26：末端各一臂正常形](c5_degree5_three_triangles.md) | 正常形拓撲覆蓋完成；[R27](c5_degree5_three_cycle_minors.md) 已補此型任意長來源 minors 及拓撲合成。 |
| [R27：末端各一臂來源 minors](c5_degree5_three_cycle_minors.md) | 末端各一臂的共用點三環鏈排除完成；其他位置見 [R28](c5_degree5_three_cycle_positions.md)，一般三環仍開放。 |
| [R28：三環鏈全部接點位置](c5_degree5_three_cycle_positions.md) | 完整 list 接合保留；[R29–R30](c5_degree5_middle_cycle_minors.md) 已完成中間不同二接點排除，[R31](c5_degree5_same_terminal_triangles.md) 僅完成同末端不同二接點正常形。 |
| [R29：中間二接點 C3–C5–C3](c5_degree5_middle_pentagon.md) | 正常形拓撲覆蓋完成；[R30](c5_degree5_middle_cycle_minors.md) 已補中間不同二接點的任意長來源 minors。 |
| [R30：中間二接點來源 minors](c5_degree5_middle_cycle_minors.md) | 中間不同二接點鏈型排除完成；[R31](c5_degree5_same_terminal_triangles.md) 已完成同末端不同二接點正常形，該型任意長來源 minors 仍待補。 |
| [R31：同末端不同二接點正常形](c5_degree5_same_terminal_triangles.md) | 408 模板／327,968 接線的正常形非 disk 覆蓋完成；任意長來源 minors 仍是保留缺口，不能宣稱此型已任意長排除。 |

## 4. R31 保留缺口與重播入口

R31 已有同末端不同二接點的 C3–C3–C3 簡單臂正常形非 disk 證書。
仍須把任意長奇環及重複色外臂化到該目標：接點末端保留共用點與兩接點，
中間保留兩共用點與 S 錨點，另一末端保留共用點與兩個 T 錨點；
建立 boundary 固定且互斥的 branch sets，再縮臂、逐步核對 degree、四列與
刪邊著色，最後合成拓撲證書回來源。精確要求見 [R31 §4](c5_degree5_same_terminal_triangles.md#4-精確停止點)。
R28 的 list 等價及 R30 的另一接點型不能取代這一步。

各報告保留指定依賴、重播命令及實際重跑／沿用的範圍。degree-5 報告對應
同名 `scripts/c5_degree5_<主題>.py` 與 `artifacts/c5_degree5_<主題>/observations.json`。
例如 R31 的 [checker](../scripts/c5_degree5_same_terminal_triangles.py) 與
[證書](../artifacts/c5_degree5_same_terminal_triangles/observations.json) 只重播正常形覆蓋；
通過不會補上任意長來源缺口。R9 對應 [K4 checker](../scripts/c5_k4_blocks.py)，
Lean 支援的精確 theorem 與 axiom audit 見 [接合基礎](lean_root_interfaces.md)。

[研究歷史](STATUS_HISTORY.md) §9–16 記錄 R9–R15，§17–22 記錄 R16–R20，
§23–27 記錄 R21–R23 與 Lean 接合基礎，§28–37 記錄 R24–R31 與發布核對。
R 編號不等於 STATUS 歷史節號。提交狀態以即時 Git 為準。

本次僅整理文件，未重跑研究 checker、大型枚舉或 Lean build。
文件檢查：`python3 scripts/check_docs.py`、`git diff --check`。
一般單側／共同出口、候選 A 與 `K∞=K≤5` 仍未證。
