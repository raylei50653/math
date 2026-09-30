# C₅ 私有內點兩點接合：平面見證與兩個原框阻斷

2026-09-30。接續[具名八點接合](c5_two_vertex_join.md)及
[純 C₅ 主例拓撲](c5_two_vertex_join_topology.md)，只處理已保存的
`private_interiors`：R127 `(0,2)` 接 R167 `(1,3)`。
指定十五點三十五邊圖的抽象平面性及兩個原框可行性已完成。
證據為紙面交錯路徑論證＋Python 固定圖證書，未新增 Lean theorem。
目前研究停止點見[兩點重疊導覽](c5_two_vertex_overlap_guide.md)。

2026-09-30 後續：[反向雙射拓撲](c5_two_vertex_private_reverse_topology.md)
亦已對原代表完成平面、來源 disk 內部互斥及兩原框阻斷；完整 J
與正向各有 16 個獨有 patterns。以下保留本輪的正向證據與停止點。

2026-09-30 後續：[六例 transport audit](c5_two_vertex_repair_transport.md)已對
同一正向圖的全部五條 U 上五環逐條核對：兩條混合框可作整圖外界，
新增肯定 rotation；三條被原路徑阻斷，原 A/B 阻斷維持成立。
兩框拉回 P=114 軌道，r*=4，全部十五組極小 repairs 已保存。

## 1. 結論與同圖前提

只識別 x=a0=b1、y=a2=b3；兩側原邊、五個 A 私有內點、兩個 B
私有內點全部保留。沒有新增邊、收縮路徑或更換代表，兩側沒有共同邊。
原框具名環序為

```text
C_A = (a0, a1, a2, a3, a4)
C_B = (b0, a0, b2, a2, b4)
```

「原框可作整圖 disk 外界」指存在平面嵌入，使該原 C₅ 恰為 disk
邊界，整張接合圖都在此閉 disk 內；不能只檢查原來源圖在其中。

| 問題 | 結論 | 證據 |
| --- | --- | --- |
| 整圖是否抽象平面 | 是 | 完整 rotation、70 條有向邊、22 面、Euler=2 |
| C_A 能否作整圖 disk 外界 | 否，所有嵌入皆不行 | 原圖兩條端點交錯且互斥的路徑 |
| C_B 能否作整圖 disk 外界 | 否，所有嵌入皆不行 | 另一對原圖交錯路徑 |
| 兩來源能否同時各在自己的原 disk 中，且兩 disk 內部互斥 | 是 | 同一平面見證的逐邊側別與私有內點位置 |

完整八點 J 仍是 **60 個共同 S₄ 軌道／1,440 份具名賦色**，
`π_A J=R127`、`π_B J=R167`。Checker 重算完整集合及保存的所有染色
witness，沒有用點對投影代替 J，也沒有刪除任何 class 或 relation row。

這是指定代表圖的結論，不是同 Σ 所有實現的分類。兩個投影本身仍有
disk 實現：原來源圖就是見證。不能從「接合圖不能以原框作外界」推成
「其五點 relation 沒有任何 disk 實現」。未來是否可用投影替換整圖，
仍取決於被隱藏頂點是否還會被接觸。

## 2. 抽象平面及保留私有內部的正見證

[Companion artifact](../artifacts/c5_two_vertex_overlap/private_topology.json)
保存每個原頂點的完整 clockwise 環序。Checker 沿有向邊反向後取
clockwise 前一項的面置換走遍所有面，核對：

- rotation 的鄰接恰為原十五點三十五邊圖，連通且每條有向邊使用一次；
- 22 個面均為 simple cycle，面長為 20 個三角形、一個四邊形及一個六邊形；
- 面長總和為 70，`15−35+22=2`。

將依 rotation 接起的定向帶狀圖之每個面補入圓盤，得到連通可定向
閉曲面；Euler=2 給球面。指定面 19

```text
a0–a4–a3–a2–b4–b0–a0
```

為外面，即得到所需的平面嵌入。這只是**一份存在見證**，沒有遍歷
此圖全部環序或分類所有區域重疊型。

沿原框切開面對偶後，各得到內外兩個面集。指定外面所在的一側是
outside，另一側是 bounded disk；原框方向及逐原邊位置如下。

| 原框 | inside 面 ID | 原框有界側 | inside／boundary／outside 邊數 |
| --- | --- | --- | --- |
| A | 0–12 | 按原具名方向為右側 | 17／5／13 |
| B | 13–18、21 | 按原具名方向為左側 | 8／5／22 |

全部 22 條 A 邊在 A disk 內或邊界，五個 `A_inner5,…,A_inner9`
嚴格在內；全部 13 條 B 邊在 B disk 內或邊界，兩個
`B_inner5,B_inner6` 嚴格在內。另一來源的邊內部全部在自己的 disk
外側。兩個 inside 面集互斥，兩條原框也只交於 x、y，故兩個有界閉
disk 的交集恰為這兩點。

這支持「原來源 disk 內部互斥」的接法；同時兩個 disk 都不容納整圖。
使用者尚未選定一般接合政策，所以 `prescribed_transition_legality`
仍為 `unknown`。正見證不把未知政策改成已允許。

## 3. 兩個原框的所有嵌入阻斷

使用以下紙面事實：若 simple cycle C 是 disk 邊界，兩條 simple
路徑的端點是 C 上四個相異點，兩路徑內部不碰 C，且端點沿 C
交錯，則這兩條路徑不能在 disk 內互斥。第一條路徑是一條 crosscut；
由 Jordan 分離，第二條的兩端在它分出的兩側，必須與它相交。
平面圖嵌入中，頂點互斥的原路徑不會相交，故矛盾。

本例使用下列**實際原路徑**，不要求添加假想弦：

| 待排除原框 | 路徑 P | 路徑 Q | 沿原框的端點次序 |
| --- | --- | --- | --- |
| A | a0–b2–a2（B 原框路徑） | a1–A_inner9–A_inner5–A_inner7–a3（A 原內部） | a0、a1、a2、a3，即 P,Q,P,Q |
| B | a0–a1–a2（A 原框路徑） | b0–B_inner6–b2（B 原內部） | b0、a0、b2、a2，即 Q,P,Q,P |

每一行的兩條路徑均為 simple、頂點互斥，只有端點在待排除原框上，
所用每條邊都能在保存的同一來源映射查回。假設整圖在該原框所圍的
disk 內，就迫使同一行的兩條路徑也在該 disk 內，與交錯性矛盾。
因此 A、B 各自都不可能作整圖外界；這個否定不只針對 §2 的環序。

正見證把每行兩路徑置於待排除原框的不同側，所以與整圖平面性相容。
私有內點正是這次與純 C₅ 主例不同的阻斷來源，不能套用四條裸 x–y
路徑的全環序分類。

## 4. 證書、重播與信任界線

[Checker](../scripts/c5_two_vertex_private_topology.py)只用標準函式庫，
重用既有 face／disk-side verifier 及整圖染色 backtracking。
它核對舊接合 artifact 的來源 SHA，從 `cells.json` 重建兩來源原邊
並補框，確認與同一合成圖相等。新 artifact 綁定舊 artifact、所有
匯入 checker 檔及自身的 SHA-256，保存完整來源映射、全部原邊、
完整 J、兩個投影、60 份全圖染色 witnesses、平面環序及兩份阻斷。

環序探索曾使用本機 NetworkX 3.6.1；其 API 回傳 embedding 或
Kuratowski 子圖的意義見[官方文件](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.planarity.check_planarity.html)。
保存的 checker 不匯入它、不信任平面性接受 flag，也不靠其非平面
輸出排除原框。否定證據就是 §3 的原圖路徑；肯定證據是 §2 的
面置換。由這些有限條件推到球面、disk 與交錯路徑矛盾仍是紙面拓撲，
沒有新增 Lean 或 `native_decide` 證明。

```bash
python3 scripts/c5_two_vertex_private_topology.py
python3 scripts/c5_two_vertex_private_topology.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_private_topology.py --check
python3 scripts/c5_two_vertex_join.py --check
python3 scripts/c5_two_vertex_overlap.py --check
python3 scripts/c5_two_vertex_join_topology.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 checker 對所有 `4^8=65,536` 份八點賦色求原七內點延拓，核對
接受集合、共同 S₄ patterns、所有染色 witnesses 及兩側完整投影。
實際執行結果見[本輪紀錄](history/2026-09-30-c5-two-vertex-private-topology.md)。
本輪未改寫舊接合 artifact 的 `geometry=unknown`；新拓撲狀態由
companion 及導覽承載。

指定 `private_interiors` 的三個可行性問題已完成；反向雙射控制、
其他代表的拓撲、所有嵌入／重疊型分類、一般接合政策、完整後繼表、
多步摘要充分性與 `K∞=K≤5` 仍保留。`lake build` 僅驗既有 Lean。
