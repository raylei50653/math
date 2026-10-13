# 最小來源的全內部五輪與具名重接界線

2026-10-12。本頁接續 [最小來源度數界](c5_saturation_degree_bound.md)，
採納全內部五輪及 [A／B／C 任務](tasks/c5_degree5_link_tasks.md) 的隔離交付。
目前停止點由 [Kempe 導覽](c5_kempe_guide.md) 維護；
本次驗證與封存範圍見 [發布紀錄](history/2026-10-12-degree5-collar-progress-publish.md)。
同日後續 [W5 具名完整關係縮減](c5_w5_marked_relation.md) 已用五個合法單對商圖的
完整拉回重建 H／G 全部 fibres；一般正聯集縮減與 annulus 小代表仍 OPEN。
2026-10-13 [跨原邊缺陷搬運](c5_cross_edge_kempe.md) 另證五條 spokes 的 J_e
完整 lifts 雙射與同一染色的 Kempe 路徑限制；一般來源排除仍 OPEN。

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

941 的 C7 55列必要上界、h≥3 外圈、跨原邊 J_e 同步、十三內點以上來源、
一般五度縮減及 K∞=K≤5 仍 **OPEN**。

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
