# 最小來源的全內部五輪與具名重接界線

2026-10-13 最新後續：[K15-SPHERE](c5_k15_sphere.md)證 `K≤15=K≤5`，一般來源至少十六內點；
[C8原接點／剝層定理](c5_c8_peeling.md)另證 `h=3 ⇒ k≥19`；八項無界來源仍 OPEN。
八項無界殘留與一般主命題仍OPEN；下文及舊證書保存各原輪次語境。


2026-10-13 最新後續：[圈秩四兩分支排除](c5_w5_private_rank4.md)
合併contractible的6,389模板與新essential的2,872模板，
得到任取合法全內部W5的私人 `ρ(F)≥5`。一般縮減／小代表及主命題仍OPEN；
下文原輪次界線與證書保留，不宣稱不同圖的R³等價。


2026-10-13 最新後續：[K14-SPHERE](c5_k14_sphere.md) 已證 `K≤14=K≤5`，
一般目錄外來源至少十五內點；同份新紙面證明給 `h=3 ⇒ k≥16`。
下文先前界線與證書保留當輪語境，h≥3、n₅≥9不提高。


2026-10-13 後續：[K13-COLLAR](c5_k13_collar.md) 已證 `K≤13=K≤5`，
一般目錄外來源至少十四內點；下文原輪次的 k≥13 前提與證書不改。

2026-10-12。本頁接續 [最小來源度數界](c5_saturation_degree_bound.md)，
採納全內部五輪及 [A／B／C 任務](tasks/c5_degree5_link_tasks.md) 的隔離交付。
目前停止點由 [Kempe 導覽](c5_kempe_guide.md) 維護；
本次驗證與封存範圍見 [發布紀錄](history/2026-10-12-degree5-collar-progress-publish.md)。
同日後續 [W5 具名完整關係縮減](c5_w5_marked_relation.md) 已用五個合法單對商圖的
完整拉回重建 H／G 全部 fibres；一般正聯集縮減與 annulus 小代表仍 OPEN。
2026-10-13 [跨原邊缺陷搬運](c5_cross_edge_kempe.md) 另證五條 spokes 的 J_e
完整 lifts 雙射與同一染色的 Kempe 路徑限制；一般來源排除仍 OPEN。
同日 [三色支援與私人森林排除](c5_w5_three_color_support.md) 已證最小來源的
annulus 私人圖必含環，並以三色具名 support 給補中心後的雙向 full-lift
對照契約；一般同槽位 r≤6 代表仍未構造。
同日 [私人單環排除](c5_w5_private_unicyclic.md)進一步證任取合法全內部W5的
私人圈秩至少二；環繞U的必要單環域可嚴格替成只保Σ的prism，不保R³。
同日[私人雙環排除](c5_w5_private_rank2.md)覆蓋全部圈秩二來源，以四個實際代表
嚴格保持完整Σ，得到私人圈秩至少三；一般縮減與r≤6代表仍OPEN。

## 1. 共同來源與全內部五輪

固定簡單平面 disk 圖及有序原框 B。在所有完整十列 Σ 不屬於 K132 的來源中，
先最小化內點、再最大化邊數，沿用共面正規形、K≤12=K≤5、原邊界度數≥4、
原內部度數≥5 及無 occupied separating triangle。這些前提不等於舊
edge-critical／ε／Gallai 身份；不得移植到 E-ARC2／N2 證書。

[全內部五輪報告](../audits/2026-10-12-c5-deep-five-wheel-01a12ffa/REPORT.md)
證每個 C4 的有界內部為空；異於 B 的 C5，其有界內部為空或恰為一個 W5 中心。
完整 cap 替換保持共同 pins 及全部延伸存在性，不要求新舊 fibres 等基數。
原框接觸的計數進一步迫存在 degree-5 原內點 v，其五個鄰點也全部是原內點，
形成 induced 五輪。這是上述最小來源的條件性紙面定理，尚未給出保 Σ 的縮減。

[完整外圈限制](c5_neartri_boundary_collar.md) 已於2026-10-13排除941的最後C7上界，
五度內點下界對933／941均為九；它涵蓋較早下界，並保留全內部五輪的存在結論。

## 2. 三份任務的交付與範圍

| 任務 | 已完成內容 | 保留界線／證據 |
| --- | --- | --- |
| [A：位置與替換契約](../audits/2026-10-12-degree5-link-a-e293fc11/REPORT.md) | 九種具名 link 位置、原區域 ownership、十列雙向 full lifts；m≥3 及兩個非相鄰 m=2 型排除 | 剩 m=0 annulus、m=1 pinched boundary、相鄰 m=2 的 C8；紙面＋九個 literal 骨架及漏 pin 反控制，正式證書為 v2 |
| [B：同源重接控制](../audits/2026-10-12-degree5-star-b-6ef2c06c/REPORT.md) | 132 份目錄圖加 W5、77 個標記；385 刪 spoke、345 flip、290 quotient 的完整十列／空 fibres／full lifts | 1,020 項均未保持完整 Σ；只對固定圖與選定嵌入成立，不證一般縮減不可能，正式證書為 v2 |
| [C：C5＋C5 cap 閉合](../audits/2026-10-12-degree5-c5-c5-cap-dcdad039/REPORT.md) | 全部 132²=17,424 有序 pairs 得 66 種輸出，全在 K；657,432 joint blocks、2,606,752 full lifts 與 literal DFS 相同 | 指定來源位置的條件排除，獨立於 A／crosscut；不是一般目錄完備性，最多十四內點的重建圖直接查 K |

A／全內部五輪／外圈 crosscut 各有紙面來源排除；C 另完成原規格的全部有限接合，
不再列為未執行。B 的零等價操作只是該固定域結果。真正 933／941 最小目錄外
來源仍為 `not triggered`；上述普遍結論來自紙面適用性、有限完整證書及明列上游前提。
本輪沒有新增 Lean theorem；外部計數證明及上游大型枚舉沒有重跑。

## 3. 精確停止點與重播

已保證可選 m=0 的全內部五輪。刪中心後需保留原 B 與鄰環 U 的十個 pins、
annulus 拓撲及同一外部圖的完整 J_p(B,U)，含全部空 cells 與 full lifts。
普通外 C5 的小代表會忘掉 U 及中心的接回空位，不能替代這份 marked relation。
後續 [具名完整關係縮減](c5_w5_marked_relation.md) 已證五個合法單對商圖的完整
拉回聯集等於全部 H lifts；同一 lift 的重數二恰能唯一接回中心。
五種三色型的精確分解仍依賴共同 lifts，交叉双對識別不構成合法局部正聯集。
剩餘義務是把這份完整資料轉成保整份 Σ 的合法正聯集縮減，或構造同槽位小代表。
計數上的 m=0 代表界為 6+r≤12；m=1 的 5+r≤12 及相鄰 m=2 的 4+r8≤12
仍是其他介面的待證界，並未構造這些代表。

941 的 C7 55列必要上界已由[完整外圈報告](c5_neartri_boundary_collar.md)排除；
後續[C8-STRUCT](../audits/2026-10-13-c8-struct-243a125/REPORT.md)將70查詢收窄為
62項排除、8份必要條件殘留，仍只採納h≥3、n₅≥9。
後續[圈秩三 essential 排除](c5_w5_private_rank3_essential.md)及
[contractible 完整排除](c5_w5_private_rank3_contractible.md)已覆蓋ρ=3的兩分支，
任取合法全內部W5均有私人ρ≥4；後者2,270模板的完整Σ皆屬K132，不需代表。
一般ρ≥4來源的縮減、h≥3來源實現、跨原邊 J_e 同步、十四內點以上來源
及 K∞=K≤5 仍 **OPEN**。

```bash
python3 audits/2026-10-12-c5-deep-five-wheel-01a12ffa/controls/check.py --check audits/2026-10-12-c5-deep-five-wheel-01a12ffa/controls/certificate.json
.venv/bin/python -B audits/2026-10-12-degree5-link-a-e293fc11/controls/check.py --check audits/2026-10-12-degree5-link-a-e293fc11/controls/certificate.v2.json
.venv/bin/python -B audits/2026-10-12-degree5-star-b-6ef2c06c/controls/check.py --check audits/2026-10-12-degree5-star-b-6ef2c06c/controls/certificate.v2.json
.venv/bin/python -B audits/2026-10-12-degree5-c5-c5-cap-dcdad039/controls/checker.py --check
```

新 checkout 先按 [封存說明](../audits/README.md) 還原原始 audit bytes；
seed17、獨立 checker、負控制及凍結 hash 的完整入口見各隔離 REPORT／VERIFICATION。
較早度數界探索保存於 [原 scratch 紀錄](../scratch/c5-sigma-saturation-20261012-01a12fdf/RESULT.txt)，
正式採納以度數界及本頁所連證據包為準。
