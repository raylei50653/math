# C₅ 私有內點反向接合：具名平面見證與原框阻斷

2026-09-30。接續[正向私有內點稽核](c5_two_vertex_private_topology.md)，
只處理[八點接合](c5_two_vertex_join.md)已保存的
`private_interiors_reverse`：R127 `(0,2)` 接 R167 `(3,1)`。
指定十五點三十五邊圖的平面性、兩來源 disk 內部互斥及兩原框阻斷
已完成。證據為紙面拓撲＋Python 固定圖證書，未新增 Lean theorem。
目前停止點與下一題由[兩點重疊導覽](c5_two_vertex_overlap_guide.md)維護。

2026-09-30 後續：[混合外框完整 relation](c5_two_vertex_mixed_frame.md)
已沿用面 19 的 `(a0,a4,a3,a2,b2)`，由完整 J 投影與原圖十內點延拓
確認 R255／8 軌道／192 賦色，並核對既有單內點 disk 代表。
同日[第二混合框](c5_two_vertex_second_mixed_frame.md)亦完成面 21 的
`(a0,b4,b0,a2,a1)`：完整 R1022／9 軌道／216 賦色，等於雙內點
disk 代表，與第一框非 D₅ 等價。
下文保留拓撲輪的當時語境；新結果不改寫本輪 artifact 或原八點 J。

2026-09-30 後續：[六例 transport audit](c5_two_vertex_repair_transport.md)
已證此圖原 U 上恰只有上述兩條可用五框，其餘三條五環由交錯原路徑阻斷；
這是五框可用性的完備核對，不是全部嵌入分類。

## 1. 原代表、反向雙射與結論

識別 x=a0=b3、y=a2=b1；保留原 R127 的五個私有內點、原 R167 的
兩個私有內點，以及補回原框後的全部來源邊。兩側只共用 x、y，
沒有共同邊、額外識別、新增邊或換代表。

```text
U   = (a0, a1, a2, a3, a4, b0, b2, b4)
C_A = (a0, a1, a2, a3, a4)
C_B = (b0, a2, b2, a0, b4)
```

| 問題 | 結論 | 證據 |
| --- | --- | --- |
| 原接合圖抽象平面 | 是 | 全部 70 條有向邊的面置換、22 面、Euler=2 |
| 兩來源各在自己的原 disk 內，且 disk 內部互斥 | 是 | 同一環序／外面的逐邊側別與七個私有內點位置 |
| C_A 作整圖 disk 外界 | 不可能，涵蓋所有嵌入 | A 原框上的一對交錯原路徑 |
| C_B 作整圖 disk 外界 | 不可能，涵蓋所有嵌入 | B 原框上的另一對交錯原路徑 |
| 完整 J 與五點投影 | 60 軌道／1,440 賦色；R127／R167 | 直接重算原圖所有八點賦色的七內點延拓 |
| 同一 U 欄序下與正向 J 相等 | 否 | 44 個共同 patterns，各有 16 個獨有 patterns |

「原框作整圖 disk 外界」要求整張接合圖均在該原 C₅ 的閉 disk 內。
正向、反向雖有相同可行性結論與投影 mask，仍是不同的具名圖及
完整八點 relation。兩個來源投影本身已有原來源 disk 實現；本輪
沒有排除任何 class 或刪除 relation row。

## 2. 反向圖自己的平面與 disk 正見證

[Companion artifact](../artifacts/c5_two_vertex_overlap/private_reverse_topology.json)
保存反向圖每個原頂點的 clockwise rotation。候選由保留 A 來源環序、
按反向識別重新接入 B 來源構造；正式重播不以此構造說明作接受依據，
而是從反向來源映射重建原邊，獨立核對完整面置換及側別。

22 面為 **20 個三角形、兩個五邊形**；全部面均為 simple cycle，
面長總和為 70，`15−35+22=2`。連通 rotation 所定義的可定向帶狀圖
補入面 disk 後為球面；指定面 19

```text
a0–a4–a3–a2–b2–a0
```

為外面，即得平面嵌入。另一個五邊形是面 21：
`a0–b4–b0–a2–a1–a0`。面長分布與正向已保存見證的四邊形／六邊形
不同；這裡只核對一份反向環序，不宣稱面長分布是所有嵌入的不變量。

| 原框 | inside 面 ID | 按原具名方向的有界側 | inside／boundary／outside 邊數 |
| --- | --- | --- | --- |
| A | 0–12 | 右側 | 17／5／13 |
| B | 13–18、20 | 左側 | 8／5／22 |

A 的 22 條來源邊全在 A disk 內或邊界，B 的 13 條來源邊全在 B disk
內或邊界；每個私有內點的全部 incident edges 都嚴格在自己的 disk
內。另一來源的邊內部均在該 disk 外。兩個 inside 面集互斥，原框只
交於 x、y，故兩個有界閉 disk 的交集恰為這兩點。

所選整圖外面是一條**混合原點的 C₅**，並非 A 或 B 原框。它的存在
與下節兩原框阻斷相容。本輪尚未將完整 J 投影到這個新框，亦未用
此新框建立後繼 class。指定一般接合政策仍未給定，所以
`prescribed_transition_legality=unknown` 保留。

## 3. 原框阻斷：重新核對反向原邊與環序

使用[正向報告 §3](c5_two_vertex_private_topology.md#3-兩個原框的所有嵌入阻斷)
的紙面 crosscut 論證：disk 邊界上的四端點若交錯，內部不碰邊界的
兩條頂點互斥原路徑不能同時置於 disk 內。此為 Jordan 分離的推論，
Python 核對的是下表所有組合前提。

| 待排除原框 | 路徑 P | 路徑 Q | 沿反向圖原框的端點次序 |
| --- | --- | --- | --- |
| A | a0–b2–a2（B 原框） | a1–A_inner9–A_inner5–A_inner7–a3（A 原內部） | a0、a1、a2、a3：P,Q,P,Q |
| B | a0–a1–a2（A 原框） | b0–B_inner6–b2（B 原內部） | b0、a2、b2、a0：Q,P,Q,P |

路徑的名稱恰與正向相同，**其邊存在性、來源所有權及 B 框的循環
次序仍按反向映射重新檢查**。每行的兩路徑 simple、頂點互斥，
內部不碰該原框，四端點相異且交錯。若該框是整圖 disk 外界，
兩路徑必同在 disk 內，矛盾。因此否定涵蓋此反向圖的所有嵌入，
不限於 §2 的見證。沒有加入假想弦或使用平面性 oracle 的拒絕結果。

## 4. 完整 J 及反向不能省略的具名控制

Checker 分別對正向、反向原圖的全部 `4^8=65,536` 份八點賦色，
以實際原邊求七個原私有內點延拓；核對完整接受集合、每份保存的
全圖染色 witness 及共同 S₄ 正規化。反向的兩個完整五點投影仍精確
為 R127／R167。

兩份 J 各有 60 軌道，其中 44 軌道共同、各 16 軌道獨有；相應具名
賦色數是共同 1,056、各獨有 384。Artifact 保存三個完整 pattern
集合，並給出以下可直接辨別的控制（依 §1 的 U 欄序）：

| 八點 pattern | 可延拓來源 | 在另一圖的直接拒絕原因 |
| --- | --- | --- |
| `(0,1,2,0,1,1,1,0)` | 正向 | 反向原 B 框邊 a0–b4 兩端皆 0 |
| `(0,1,2,0,1,0,1,3)` | 反向 | 正向原 B 框邊 a0–b0 兩端皆 0 |

兩個正例均另存十五點全圖染色。所有比較使用同一具名欄序與共同
色框；沒有逐來源改色或從五點 mask／軌道數推斷完整 J 相等。

## 5. 重播、信任界線與停止點

[Checker](../scripts/c5_two_vertex_private_reverse_topology.py)只用標準
函式庫，重用面置換、disk 側別、交錯路徑及整圖染色的既有 verifier。
證書綁定舊接合 artifact、自身與所有匯入 checker 的 SHA-256；
舊接合 artifact 的來源 SHA 也會核對，再從 `cells.json` 原代表重建
全部來源邊。未改寫正向或主例拓撲證書，亦未改寫舊 artifact 的
`geometry=unknown`。

```bash
python3 scripts/c5_two_vertex_private_reverse_topology.py
python3 scripts/c5_two_vertex_private_reverse_topology.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_private_reverse_topology.py --check
python3 scripts/c5_two_vertex_private_topology.py --check
python3 scripts/c5_two_vertex_join_topology.py --check
python3 scripts/c5_two_vertex_join.py --check
python3 scripts/c5_two_vertex_overlap.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際結果及未重跑範圍見[本輪紀錄](history/2026-09-30-c5-two-vertex-private-reverse-topology.md)。
本輪止於指定反向代表的三項拓撲可行性與完整 J 綁定；未遍歷所有
環序／區域型，未擴及同 Σ 的其他實現。混合外框的完整 relation、
其他三份控制的拓撲、一般政策、完整後繼表、多步充分性與
`K∞=K≤5` 保留。紙面球面／disk 推論未 Lean 化；`lake build`
只驗既有 Lean，未新增 `native_decide` 證書。
