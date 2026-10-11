# 互斥雙 triangles：不同環點接入的任意外臂

文件整理（2026-09-23），R17：不同環點接入排除完成；至少一側同點接入由 [R18–R19](c5_degree5_bridge_mark_minors.md) 補完。
系列定位見 [degree-5／R 系列導讀](c5_degree5_guide.md)，研究優先序見
[HANDOFF](HANDOFF.md)。下文「下一步／未解／未提交」保留當輪語境；
歷次驗證與發布見 [研究歷史](STATUS_HISTORY.md)，不代表本次重新驗證。

發布整理（2026-09-18）：本報告隨 R16–R20 一併提交。下文的「未提交／HEAD／
下一題」保留各輪當時狀態；最新停止點見 [HANDOFF](HANDOFF.md)，
本次提交核對見 [STATUS 歷史 §22](STATUS_HISTORY.md#22-r16r20-提交整理與核對)。


後續（R19）：[標記路徑 minor 與同點排除](c5_degree5_bridge_mark_minors.md)
已完成至少一側同點接入；結合 R16，本範圍的互斥雙 triangles 已全部排除。
以下保留 R17 當時的成果與停止點，原 script／artifact 未改。

2026-09-18。接續未提交的 [R16 直接私有接點](c5_degree5_bridge_triangles.md)。
本輪完成排除：兩個 z 接點各經任意長外臂到達一個 triangle，且該環的
外臂接入點不同於兩環間 bridge 路徑端點時，不存在目標 disk obstruction。
零長臂、任意長中間 bridge 路徑及不含接點的外枝皆包含在內。
**這不是所有互斥雙 triangle 接點位置的排除。**

## 1. 位置範圍與必要 lists

沿用 R16 的 q=(A,B,A,B,C)、D=3、N_B(z)={b0,b1,b4} 與 arc b1,b2,b3,b4。
C=H−z 有兩個互斥 triangle blocks，其餘 bridges，所有 C 點完整 degree=4。
目標是接受全部 T4 的 disk minimal q-obstruction，因此 F_C(q)={D}。
若兩環間某條 bridge 不分隔兩個 z 接點，已由 R16 化回單環／樹排除。

本輪令兩環為 (r,p,u)、(v,t,w)，兩環間路徑端點為 r,v，兩條 z 外臂
分別到 p,t，且 p≠r、t≠v。以下公式均以左側 (r,p,u) 說明。
外臂可以零內點，代表 z 直接鄰接 p。所有不含 z 接點的 bridge 外枝先用既有單 bridge 引理消去，
保留實際同色 spokes 或 D 葉點，不要求原外枝為樹。

消去後，r,p 的 lists 各有三色，u 有二色；外臂及中間路徑內點均有
二色 lists。固定 z=D 後，若外臂不輸出 singleton，p 仍有完整三色，
triangle 對 r 沒有限制。若輸出 singleton，但 p 的有效二色 list 不同
於 u 的 list，triangle 亦對 r 沒有限制。

兩環私有點消去後，中間路徑的端點至少各有一色。只要一端至少兩色，
從另一端向此端貪婪著色即可。因此拒絕 D 必須使每個 triangle 端點
都成為 singleton。左側必存在二色 palette S 及色 d,c∉S，使

```
L(u)=S, L(p)=S∪{d}, L(r)=S∪{c}；
外臂在 z=D 時恰輸出 {d}，triangle 在 r 恰輸出 {c}。
```

**S 現在允許含 D。** 不能再沿用 R16 的 S⊆{A,B,C} 限制。
外臂被迫訊息可記作色序列 D=a₀,…,aₖ=d，各內點 list 是
{aᵢ₋₁,aᵢ}，相鄰色不同。若途中首次出現兩色訊息，之後每個二色 list
都完整可取，末端不可能回到 singleton，故此表示涵蓋任意長臂。

右側同理用 T、e、h。中間 bridge 路徑色序列 c=c₀,…,cₘ₋₁=h，
m≥1，相鄰不同，各內點 list 為 {cᵢ₋₁,cᵢ}。這是 R16 的路徑判準，
沒有把不同 z 色下的兩側訊息獨立重新命名。

## 2. 指定 singleton 的唯一反向輸入

沿用 [單 triangle §3](c5_degree5_triangle_components.md#3-路徑訊息及指定-singleton-的唯一反向輸入)：
對固定二色 list 路徑，指定末端 singleton {d} 的輸入色至多一個。
因從末端向前，每步都只能取該二色 list 的另一色。

此處 D 已是該輸入，故 a≠D 時外臂絕不輸出 {d}。它可能輸出另一個
singleton，或一個二色集；不需要也沒有假設四列臂訊息完全相同。
於是 p 的有效 list 若為二色便不同於 S，否則仍有三色。依 triangle
root 公式，對 r 沒有額外限制。**完整條件 root 訊息**恰為

```
M_r(a)={c}       若 a=D；
M_r(a)=S∪{c}    若 a≠D。
```

所以任意合法左右色序列及 bridge 色序列都給 F={D}：D 的 singleton
沿中間路徑碰撞；其他 a 的兩端各有三色，存在 slack，必可著色。
這不是把臂的全部介面宣稱相同，而是證明接上本 triangle 後的四列 root
訊息相同。刪 z-spoke 所釋放的三種色也包含在內。

## 3. 三條路徑的真正 minor 縮減

左右外臂各刪除重複色之間的閉段，得到從 D 到 d／e 的簡單序列。
若終色 D，最終為零內點臂；否則至多三個臂內點。具體 minor 沿用
單 triangle：刪掉被移除內點的 attachments，將該段收縮進前一保留點；
前綴收進 z，triangle 三點各自保留。兩臂只共享 z，不會合併兩個接點。

中間路徑沿用 R16 刪閉段，保留兩個 triangle root 及其 attachments，
終止於互異 bridge 色序列，至多四條邊。每次保留點的色對／外接禁色
不變，degree 恢復 4／5，所有 boundary 頂點為 singleton branch sets。

縮短後仍從 D 輸出相同指定 singleton，§2 因而保留全部四列 triangle
root 訊息；bridge 縮短仍保留完整 F={D}。由既有 degree-4 分量解除引理，
每步仍是 minimal q-obstruction。未宣稱保持任意 boundary row 或完整 Σ。

無界來源遂化為以下有限必要 schema：S,T 是 U 的任意二色 pairs；
兩臂各為 D 到 S／T 外一色的簡單序列；bridge 是長度 1 至 4 的互異
色序列，其首末色分別在 S／T 外。共 **36,672 型**，包含 R16 的 132 型。

## 4. 接線覆蓋的證書方法

在指定 arc，A spoke 固定接 b2、C 固定接 b4；每個 B spoke 可獨立接
b1 或 b3。D 葉點固定保留 A、C spokes，其 B spoke 也有獨立二元選擇。
因此一個模板的全部接線恰是一個有限 Boolean cube，沒有省略同色接點。

checker 將每張 boundary-apex 圖拆成固定邊與每變數的兩條候選 B 邊。
一份 K5／K3,3 subdivision 只要求其路徑實際用到的邊；所需的 B 邊形成
一個 partial assignment，證明整個子 cube 都非平面。其餘變數任意取值
只會在這份 subdivision 外更換邊，不能破壞證書。

每模板從全部選擇開始，依次精確扣去證書覆蓋的子 cube，直到餘集為空。
扣除算法將餘集保存成互斥 cubes；重播另以四變數所有 6,561 組 cube
差集與完整 truth table 交叉核對。這是完整接線覆蓋，不是抽樣或估算。

`--check` 不呼叫 planarity：逐份驗證 subdivision 的來源邊、branch 點
及內部互斥，再核對覆蓋餘集為空。指紋涵蓋模板、固定邊、每個二元
接線選項及引用的證書；程式與依賴 hashes、networkx 版本亦保存。

每模板用條件訊息逐列核對 F={D}，具體接線檢查 degree；任意刪邊可著色
由紙面分量解除引理承擔。長來源控制另直接求全部四種 z 色及每條非
boundary 刪邊 coloring，不把這些有限控制當作任意來源的證明。

本輪完成結果：

| 證據 | 數字與範圍 |
| --- | --- |
| 必要模板 | 36,672 型，含零長臂及 S／T 含 D 的情形 |
| 實際接線選擇 | 246,645,568 種，全部非 disk；每型 2–20 個二元變數 |
| 拓撲覆蓋 | 709 份 subdivisions、36,732 次子 cube 引用；逐模板餘集為空 |
| 條件 root 代數 | 1,128 個完整 tuples 查詢，涵蓋簡單臂、前綴及內部閉段 |
| 覆蓋算法 | 6,561 組四變數 cube 差集，與完整 truth table 核對 |
| 長來源 | 72 張，全部 36 組有序 palettes 各兩型；216 次縮減 |

每張長來源及每步目標直接核對完整 degrees、四個 z 色、全部非 boundary
刪邊 coloring。另保存每步與合成的 boundary 固定 branch sets，並將最後
正常形的非平面 minor 合成回來源。來源控制不是任意外臂的有限窮盡，
任意長度由 §1–3 的紙面論證承擔。

假想 disk 來源在固定 boundary 的 minor 下，必落入本節某個非 disk
正常形，矛盾。T4 僅用於最初的區域定位，中間 minors 不必保持 T4。

## 5. 重播與停止點

[checker](../scripts/c5_degree5_bridge_arms.py)、
[certificate](../artifacts/c5_degree5_bridge_arms/observations.json)。

```bash
uv run --with networkx==3.5 python scripts/c5_degree5_bridge_arms.py --check
uv run --with networkx==3.5 python scripts/c5_degree5_bridge_triangles.py --check
lake build
git diff --check
```

執行與整合紀錄見 [STATUS 歷史 §18](STATUS_HISTORY.md#18-r17-互斥雙-triangles-不同環點接入的任意外臂)。
下一個位置缺口是**至少一側外臂在該環的 bridge 端點接入**：該點在
保留骨架已有四條 incident edges，triangle 的兩個私有點把它限制在
互補二色 palette，不能套用本輪三色 root 公式。

一般互斥雙環、兩環含長環、更多環、其他接點分拆、一般 degree≥5、
單側／共同出口與 `K∞=K≤5` 仍未證。成果是紙面化約與 Python 有限
證書，未新增 Lean theorem。本輪與 R16 未 commit／push。
