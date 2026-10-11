# 3903：拒絕列的緊 list 與內部葉點排除

後續狀態（2026-09-23）：[雙拒絕分類](c5_two_rejection_proof_zh.md) 已在
induced-C5 disk、非空連通內部、內點完整 degree≤4、b0 恰兩個不同內鄰點
的圖類內排除 3903。本文正文保留當輪結論與停止點；閱讀順序及證據界線見
[3903 系列導讀](c5_sector_3903_guide.md)。
非空交集的兩種 corner 次序已由 [偶圈報告](c5_sector_corner_even_cycle.md)
與 [末端 block 報告](c5_sector_terminal_blocks.md) 完成排除；
空交集另見 [空分支末端報告](c5_sector_empty_terminal.md)。

本報告保留研究當輪狀態；三輪整合與發布重播範圍見
[STATUS §63](STATUS.md#63-3903-三輪成果整合與發布)。

2026-09-21，接續 [第二種 corner 的停止點](c5_sector_corner_even_cycle.md)。
接手 HEAD `ca0e44b`；保留前兩輪未提交成果。本輪不擴大圖搜尋。
**非空葉點分支若實現 3903，則內部 C 的最小度數至少 2；b 的框鄰居
只能是 {0} 或 {0,3}。** 這裡排除的是 C 的葉點；w 仍是二色分量 S
的葉點，而 deg_C(w)=3，兩者不矛盾。

## 1. 拒絕列強迫每點都緊

G 保留框路徑 1–2–3–4，C 非空連通，所有內點完整 degree≤4。
對任一被拒絕的 proper 開口列 β，設 A(v)=N_G(v)∩Γ，並令

```
Lβ(v) = {0,1,2,3} \ β(A(v))。
|Lβ(v)| ≥ 4−|A(v)| ≥ deg_C(v)。
```

若任一點 x 有嚴格餘量 |Lβ(x)|>deg_C(x)，取以 x 為根的生成樹，
由葉向根貪婪染色。每個非根點在被染色時至少還有未染的父點，故
至多 deg_C(v)−1 個已染鄰點；根最後亦有嚴格餘量。這便給出延拓，
與拒絕矛盾。因此每個不等式都取等號：

```
deg_G(v)=4，|Lβ(v)|=deg_C(v)，β 在 A(v) 上單射。
```

這個論證不需 minimality、planarity 或 Gallai 定理。特別地，若有一個
內點完整 degree<4，則全部開口列皆接受，不能是 3903。

3903 拒絕 α=01212 與 δ=01213。對 α 的單射性已強迫
**沒有內點同時鄰接 1、3，也沒有內點同時鄰接 2、4**。
δ 沒有追加這類禁對，但它能區分框點 2 與 4 的 list 效果。
上述單射條件是必要條件；不能反向由 lists 都緊推出拒絕。
例如一條內部邊的兩端分別有 list {0}、{1}，都緊且可染。

## 2. 兩列共同保留的框鄰接資訊

以下 i∈{1,3}；同一行只表示兩種明列接線具有相同 list pair。
框點身份仍須保留，不能在 embedding 或路徑中合併 1、3。

| A(v) | Lα(v) | Lδ(v) |
| --- | --- | --- |
| ∅ | 0123 | 0123 |
| {0} | 123 | 123 |
| {i} | 023 | 023 |
| {2} | 013 | 013 |
| {4} | 013 | 012 |
| {0,i} | 23 | 23 |
| {0,2} | 13 | 13 |
| {0,4} | 13 | 12 |
| {i,2} | 03 | 03 |
| {i,4} | 03 | 02 |
| {0,i,2} | 3 | 3 |
| {0,i,4} | 3 | 2 |

表列完整 degree=4 下所有 18 個必要框鄰集，形成 12 種共同 list pair。
四個以上框鄰居因 α 只有三色而不可能。兩個必要框鄰集有相同 list
pair，恰等價於它們只差選框點 1 或 3；尤其不能把 2、4 當成同一接點。
這是逐點資訊，不是兩列 root 關係，更不是完整 Σ 的充分 state。

## 3. b 不鄰接 2，故 C 沒有葉點

現在加回非空分支及同一 c、S、c′、J、S′ 的所有前提。
由 [corner-gates §3](c5_sector_corner_gates.md#3-兩種分離結論)，第二種
次序中，每條 S′−{1} 的 b–2 路徑都須經過 T₂、T₃；兩者不相交，
且只含內點。若 b2 是邊，由 c(b)=1、c(2)=0 及 b,2∈S′，它本身就是
這樣的路徑，唯一內點為 b，不可能同時碰兩種 stars。因此 **b2 不存在**。
第一種次序也有同樣結論，但 3903 已由前報告排除了第一種。
此論證沒有假設 S′−{1} 原先連通：假想的 b2 邊本身提供了所需路徑。

已知 c 的框列為 01021、c(b)=1，所以 properness 又禁止 b1、b4。
由 b0 存在，得到 **A(b)={0} 或 {0,3}**。§1 的完整 degree=4 因而給出
**deg_C(b)=3 或 2**。

假設 C 有葉點 v。§1 使 |A(v)|=3；由表，每個三框鄰集都包含 0。
然而 N_G(0)={b,w}，故 v 只能是 b 或 w。上段排除 b；而
N_G(w)={0,p,q,r} 且 p,q,r 是互異內點，故 deg_C(w)=3，也不是葉點。
C 含互異的 w,b,p,q,r，且連通，沒有孤立點。因此 **δ(C)≥2**。

葉點排除只需 α 的拒絕、既有非空分支與 corner 分離條件；並不需要
假稱兩個拒絕列都不可或缺。第二列的新增用途是 §2 的共同接線辨識。

## 4. 下一個窄問題與信任範圍

由拒絕列及 degree-list，C 必為 Gallai tree，沿用並重新核對
[Cranston–Rabern 的 degree-choosability 敘述](https://arxiv.org/abs/1511.00350)。
又因目前的 c 已是 C 的四色染色，C 不含 K5。所以 blocks 只能是
bridges、奇圈或 K4；三角形視為奇圈。§3 排除 terminal bridge，但
**沒有排除連接兩個非平凡 blocks 的中間 bridges**。

因此下一步可直接研究第二種 corner 下的**末端奇圈／K4 blocks**，
聯立表中的兩列 lists、b 的兩種框鄰集與 p,q,r 的位置；仍須保留
S′−{1} 切斷 b、2 的分支。未證末端 block 的共同 palette 定理或接回
排除，不能把局部 list 表當成完整 block 的充分介面。

[checker](../scripts/c5_sector_rejection_lists.py) 對 degree≤4 容許的
31 個框鄰子集核對 18 個緊子集、12 個共同 list 類、四個葉點接線；
舊染色將葉點 b 縮到 {0,2,3}，再由既有 b–2 障礙排除。
[JSON](../artifacts/c5_sector_rejection_lists/observations.json) 保存表、
反向控制、兩種 b 接線及依賴 hashes。它只核對局部算術與所引用的
corner 結果，不以有限表代替任意大小的貪婪染色／葉點排除證明。

本輪沒有新增候選圖或染色搜尋、沒有刪除 profiles；603 沿用，固定點
未重算。非空 ≥8、總體 ≥6 下界不變，空交集分支仍開放。一般 3903、
R31、共同出口及主命題仍未證。紙面＋Python；Gallai 結構使用外部
標準定理，未新增 Lean theorem，未 commit／push。

```bash
uv run python scripts/c5_sector_rejection_lists.py --check
uv run --with networkx==3.5 python scripts/c5_sector_transition_control.py --check
uv run python scripts/c5_sector_corner_gates.py --check
uv run python scripts/c5_sector_leaf_corners.py --check
lake build
git diff --check
```
