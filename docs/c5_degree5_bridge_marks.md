# 互斥雙 triangles：同點接入的標記二色介面

發布整理（2026-09-18）：本報告隨 R16–R20 一併提交。下文的「未提交／HEAD／
下一題」保留各輪當時狀態；最新停止點見 [HANDOFF](HANDOFF.md)，
本次提交核對見 [STATUS §22](STATUS.md#22-r16r20-提交整理與核對)。


後續（R19）：[標記路徑 minor 與同點排除](c5_degree5_bridge_mark_minors.md)
已補完下述來源 minors 與全部 571,400 接線的拓撲覆蓋；同點接入已排除。
以下保留 R18 當時的成果與停止點，原 script／artifact 未改。

2026-09-18，R18。接續未提交的 [R17](c5_degree5_bridge_arms.md)，HEAD 為
`b55abf4`。本輪完成剩餘位置的局部介面及候選正常形之 fixed-q 語意核對，
**尚未完成這些位置的 disk 排除**。沒有新增 Lean theorem，沒有 commit／push。

## 1. 範圍與 root 引理

沿用 q=(A,B,A,B,C)、D=3、N_B(z)={b0,b1,b4}、F_C(q)={D}。
兩個互斥 triangle 由 bridge 路徑連接，每條中間 bridge 都分隔兩個 z 接點；
不符合此分隔者由 R16 化回單環／樹。沒有接點的外枝依既有引理消去。

若某側的外臂與中間 bridge 在同一環點 r 接入，r 已有兩條環邊及兩條
路徑邊，沒有 attachment。另兩個私有點的 residual lists 記為 S、T，
各恰二色，且不依賴 z 色。完整 root 可取色集為

```
M(r) = U\S   若 S=T；
M(r) = U     若 S≠T。
```

S=T 時，r 取 S 中的色會把兩私有點壓成同一色；r 在 S 外時則可讓它們
分取 S 的兩色。S≠T 時，刪去任意 root 色後仍能在 S、T 中選兩個不同色：
唯一失敗情形是兩邊都只剩同一 singleton，這會反推 S=T。
checker 以完整三點 tuples 核對全部 36 組有序 pairs。

在拒絕 D 的來源中，S≠T 的四色 root 會讓路徑傳遞產生 slack，此後不再
能輸出指定 singleton；若另一端是不同點接入的 triangle，它有一個三色
端點便可著色。因此必要情形是 S=T，可把此 triangle 的 root 視為
**標記二色 list U\S**。這是完整固定-q 介面，與 z 色無關。

## 2. 一側同點：帶一個標記的外臂

將另一側（不同點接入）triangle 記為 (u,v,w)。從 z 經同點 triangle
root 再沿中間 bridges 到 u，整段成為帶一個標記的二色 list 路徑；
另一條 z–v 外臂沒有標記。問題因而具有單 triangle 報告的不同接點語意：

```
L(w)=P, L(u)=P∪{c}, L(v)=P∪{d}；
兩路徑在 z=D 時各輸出 c、d，且 c,d∉P。
```

兩路徑由從 D 出發的強迫色序列表示。單 triangle 的反向唯一性保證，
z≠D 時不會再輸出同一指定 singleton，故 F 恰為 {D}。

刪閉段時按「list 步驟」追蹤標記，不能按相同顏色認作同一個環點。
若標記仍在，保留原 triangle 私有點及 attachments；若標記被移除，
需一併刪掉該 triangle 私有點及 attachments，轉入已有單 triangle 型。
未刪掉標記的終端序列各為簡單路徑，帶標記的一側最多三個內點。

候選正常形從單 triangle 的 408 型中，在左臂每個內點各放一個標記，
得到 **858 型**。交換兩環名稱即可涵蓋另一側同點的位置，無需重命名
boundary 或顏色。此處標記代表加入一個真正 triangle，不是普通兩條 spokes。

## 3. 兩側同點：帶兩個標記的閉序列

兩個 triangle roots 都成為標記二色 lists；連同兩外臂及中間 bridges，
得到兩端皆接 z 的二色 list 路徑。兩個標記是不同步驟，可相鄰。
F={D} 的精確判準沿用樹報告：強迫色序列從 D 回到 D，至少使用三色。

只刪除「刪完仍至少三色」的閉段。若刪掉一個／兩個標記，同時移除其
私有 triangle，分別化入既有單 triangle／樹型；保留兩個標記時，終端是
既有五種不可再刪閉序列之一，在不同步驟標記兩個位置。

因此候選正常形數是

```
6 × [C(3,2) + C(4,2) + C(4,2) + C(4,2) + C(5,2)] = 186。
```

反向控制 D,A,D,B,D 有 F={D}，任意刪掉首個閉段得到 D,B,D 卻有 F={B,D}。
因此不能獨立將兩臂任意縮短，或只保留「拒絕 D」作為正確性條件。

## 4. 本輪證書實際驗證的範圍

[程式](../scripts/c5_degree5_bridge_marks.py)、
[證書](../artifacts/c5_degree5_bridge_marks/observations.json)。

| 項目 | 本輪結果 |
| --- | --- |
| Root 介面 | 36 組 pairs，以完整三點色 tuples 驗證 |
| 候選正常形 | 一側同點 858 型；兩側同點 186 型 |
| 具體代表 | 每型選一組實際 arc 接線，保存完整圖及 attachment roles；degree(z)=5，其餘有效內點 degree=4；兩個互斥 triangles |
| 完整固定-q 語意 | 每張代表直接求四種 z 色，只有 D 不延拓；保存其餘三種 coloring |
| Minimality | 每張代表直接求每條非 boundary 邊刪除後的 q-coloring，全部保存 |
| 標記縮減控制 | 從 D 出發、至多六步的全部相鄰異色色序列；6,015 個單標記開序列及 3,426 個雙標記合格閉序列；12,711 次刪閉段 |
| 標記去留 | 開序列保留／刪除標記 1,323／4,692；閉序列剩 0／1／2 標記 342／1,818／1,266 |
| 退化控制 | 保存 F={D} 變成 F={B,D} 的錯誤縮減 |

縮減控制檢查保留步驟的 list 完全相同；開序列保留指定 singleton 的唯一
反向輸入，閉序列每步保留完整 F={D}。這些是**色序列控制**，沒有保存
長來源圖的 boundary 固定 branch sets，不能稱為已驗證的來源 minor。

每型只檢查一組實際接線，**尚未檢查其餘 B-spoke 接 b1／b3 的拓撲選擇**；
本輪沒有呼叫 planarity，也沒有產生非平面 subdivisions。正常形代表
minimality 不等於 disk realizability。無界縮減的標記刪除構造已寫出，
後續仍需落實 source-to-target minors 及正常形的完整拓撲覆蓋。

## 5. 重播與下一步

```bash
uv run --with networkx==3.5 python scripts/c5_degree5_bridge_marks.py --check
uv run --with networkx==3.5 python scripts/c5_degree5_bridge_triangles.py --check
lake build
git diff --check
```

`--check` 唯讀、重算並逐 byte 比對證書；保存程式與依賴 SHA256。
本輪不改 R16／R17 scripts 或 artifacts，也不重跑 R17 的 36,672 型覆蓋。

下一步直接使用本輪 **1,044 型**：先構造保留／刪除標記的真正 boundary
固定 minors，包含兩標記同時刪除、前綴縮入 z、兩標記相鄰等來源；再沿用
R17 的 Boolean cube 覆蓋方法處理全部實際 boundary 接線。
在這兩項完成之前，不宣稱同點接入或所有互斥雙 triangles 已排除。
兩環含長環、更多環、其他 degree-5 分拆、一般 degree≥5、單側／共同出口
與 `K∞=K≤5` 仍開放。
