# 三-spoke 的單長奇環二接點分量排除

文件整理（2026-09-23），R14：單奇環加 bridges 排除完成；雙環由 [R15–R24](c5_degree5_shared_cycle_minors.md) 接續完成。
系列定位見 [degree-5／R 系列導讀](c5_degree5_guide.md)，研究優先序見
[HANDOFF](HANDOFF.md)。下文「下一步／未解／未提交」保留當輪語境；
歷次驗證與發布見 [研究歷史](STATUS_HISTORY.md)，不代表本次重新驗證。

發布整理（2026-09-18）：本報告隨 R11–R15 五輪成果一併提交。下文的
「未提交／HEAD／下一題」保留各輪當時狀態；最新停止點見
[HANDOFF](HANDOFF.md)，發布前核對見 [STATUS 歷史 §16](STATUS_HISTORY.md#16-r11r15-成果整理與發布前核對)。

後續（2026-09-18）：[共用點雙 triangle 報告](c5_degree5_shared_triangles.md)
已排除恰兩個 triangles 共用 cut vertex 的二接點分量，涵蓋任意臂長及外枝。
下一題收窄到兩個互斥 triangles 的 bridge 路徑；以下保留本輪成果及原始停止點。

2026-09-18。HEAD `be97121`，接續三輪未提交成果。
完成交接指定的下一題：**唯一 degree-5 點 z 有三條 boundary spokes，H−z
是恰含一個長 odd-cycle、其餘為 bridges 的連通二接點分量時，不存在接受
全部 T4 的 C5 disk minimal q-obstruction。** 環長、兩接點位置、通向環的
路徑長度與外枝分叉皆無上限。

關鍵是保留接點的 cycle-to-triangle minor，接上
[單 triangle 報告](c5_degree5_triangle_components.md) 的已證非 disk 正常形。
結合該報告與樹分量結果，三-spoke 型的 C 現在必含至少兩個 odd-cycle blocks。
這是紙面證明加有限 Python 控制；沒有新增 Lean theorem，沒有證一般
degree-5 單缺失或 `K∞=K≤5`，沒有新增 graph catalog。四輪成果未 commit／push。

## 1. 固定介面與三種位置

沿用 [區域定位](c5_degree5_sectors.md) 及
[完整禁色介面](c5_degree5_interfaces.md)：

```
q=(A,B,A,B,C), U={0,1,2,3}, D=3,
N_B(z)={b0,b1,b4}, F_C(q)={D}.
```

分量 C 只接 arc (b1,b2,b3,b4) 上的 boundary 點；另一種位置由鏡像處理。
令 J 是長度 m≥5 的唯一奇環，s,t 為 z 的兩個不同接點。刪去 J 的邊後，
每個剩餘樹分量恰包含 J 的一個頂點，故有三種情形：

1. s,t 分屬不同樹分量：兩條互斥路徑到 J 的不同頂點 u,v。
2. s,t 同屬一樹分量，且 s–t 路徑經過該 cycle 頂點 r：共同接點 r。
3. s–t 路徑不碰 J：J 完全位於一個不含 z 接點的 bridge 旁支。

路徑可零長；共同接點型的兩臂不能同時零長，因 s≠t。
按 [單 triangle 報告 §2](c5_degree5_triangle_components.md#2-不含保留接點的單-bridge-外枝可消去)
消去不含 s,t 的外枝。該引理不要求外枝是樹，因此情形 3 可整個消去含 J
的旁支，化回已排除的樹正常形。

以下處理情形 1、2。保留所有通向 J 的路徑，消去其餘外枝。每個非 D
外接禁色以來源圖中的實際同色 spoke 實現；D 禁色以帶三種 q 色 spokes
的 D 葉點實現。外接禁色互異，且這一步保留全部 F_C(q)、完整 degrees、
boundary singleton branch sets 及 minimality。

## 2. 奇環的 list 判準及使用範圍

**引理。** 在 cycle 上，每個 list 至少有兩色時，不可著色 iff 環長為奇數、
全部 lists 都是同一個二色 pair S。

若相鄰 x,y 的 lists 不同，可選方向使某色 c∈L(x)\L(y)。先把 x 塗 c，
再沿不先經 y 的方向逐點貪婪，最後塗 y。每個中間點只需避開前一點；
y 的 list 本來就不含 c，所以最後亦只需避開前一點。若全部 lists 相同，
至少三色可直接將 cycle 三著色；二色則恰由長度奇偶決定。

這是本報告自足的初等證明。背景中的 Gallai-tree 必要條件仍沿用完整介面
報告及 [Dvořák 的 degree-list characterization](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
（Theorem 10）；本輪查核原文，但不把外部一般定理視為本輪 Python／Lean 證書。

每條通向 cycle 的路徑，除 cycle 端點外都帶二色 residual lists。
固定 z=a 後，路徑末端可取色集 M 非空：若 M={c}，對 cycle 端點只禁止 c；
若 |M|≥2，對 cycle 端點沒有額外限制。路徑可以零長，此時 M={a}。
這是精確的存在量化，兩臂只有在共同固定 a 後才可分開求值。

不同接點 u,v 原有三色 lists，各臂最多刪一色；共同接點 r 原有四色 list，
兩臂合計最多刪兩色。未標記 cycle 點原有二色 lists。因此對任意 z=a，
cycle 的每個有效 list 都至少二色，可用上述引理。

特別在 a=D 下，整圖不可著色，故未標記 cycle 點的 lists 必全為同一 S。
這個結論使用拒絕 D；不能宣稱任意可著色的長環都有 triangle 的完整介面。

## 3. 不同 cycle 接點：保留四個 z 色查詢

記兩臂在 z=a 下的訊息為 M_u(a)、M_v(a)。由 a=D 下的拒絕，存在
c_u,c_v∈U\S，使

```
L(u)=S∪{c_u}, L(v)=S∪{c_v},
M_u(D)={c_u}, M_v(D)={c_v}.
```

未標記 cycle 點的 lists 都是 S。對任意 a，cycle 不可著色 iff

```
M_u(a)={c_u} 且 M_v(a)={c_v}.                 (1)
```

理由是有效 lists 必全部恰為 S，而每臂只會刪除一個 singleton 或不刪。
將 J 換成保留 u,v 與一個未標記點 w 的 triangle，保留同樣 lists、兩臂
及所有保留點 attachments 後，其拒絕條件仍恰為 (1)。所以全部四種 a 的
可延拓性相同，**完整 F_C(q) 保持為 {D}**。

此處不需要把兩臂各自縮短，也不把同分量的接點當成獨立 marginals。
若之後要縮臂，可使用單 triangle 報告的指定 singleton 反向唯一性及
簡單色序列化約；本次 cycle 縮減先原樣保留兩臂。

**界線控制。** 取 S={0,1}、c_u=c_v=2，C5 上 u,v 位於位置 0、2，其他點
list 為 S。共同端點 tuple (2,2) 可延拓，例如 (2,0,2,0,1)。縮成 triangle
後 u,v 相鄰，該 tuple 不可延拓。所以這個 minor 不保持任意 pinning 的
二元關係；(1) 的正確性依賴兩端三色 lists 與臂訊息的特定查詢方式。
也沒有保持完整 boundary Σ 的宣稱。

## 4. 共同 cycle 接點：保留完整 root 可取色集

共同接點 r 有兩條 cycle 邊與兩條朝 z 的方向，沒有額外 attachments。
在拒絕 D 下，其餘 m−1 個 cycle 點的 lists 全為同一 S。只看 cycle
本身，r 的完整可取色集恰為 **U\S**：

- r∈S 時，兩個鄰點均須取 S 的另一色；中間是偶數個點的二色路徑，
  兩端必異色，因此不能完成。
- r∉S 時，剩餘偶數點路徑可交替用 S，兩端都與 r 異色，所以可完成。

保留 r 與另外兩點縮成 triangle 後，這個 root 色集完全相同。兩臂保持
原樣，因此不只拒絕 D，對全部四個 z 色的接合結果也完全相同。
沒有各自縮掉兩臂的閉色序列，所以不會把單禁色退化成雙禁色。

## 5. 真正的 boundary 固定 minor 與排除

不同接點型保留 u,v 及任意第三點；共同接點型保留 r 及任意另外兩點。
三點按原 cycle 次序記為 x0,x1,x2。對每段 xi 到 x(i+1) 的 cycle arc，
先刪除其中所有不保留點的 spokes／D 葉點，再把 arc 的內部點全部收縮
進 xi，留下最後一條到 x(i+1) 的邊。三個 branch sets 互不相交且連通，
target 恰有三條 triangle 邊。

此操作不新增邊、不識別 boundary，也不識別任何兩個保留 cycle 接點。
三段的長度可以有不同奇偶；不要求每段各自收縮偶數條邊，只要求最終
source 與 target 都是奇環。兩臂及保留點的所有 attachments 保持，z
仍為 singleton branch set、degree=5；其他內點完整 degree 仍為 4。
新圖 H−z 仍連通且恰有一個 triangle block，其餘為 bridges。

§3、§4 給全部 F_C(q)={D}；q 下各點實際 spokes 的顏色仍互異。因此
[完整介面 §4](c5_degree5_interfaces.md#4-minimality-的充要條件與接點限制)
重新給出所有非 boundary 邊的 criticality。這是依已證染色介面重建
minimality，不是假設一般 graph minor 自動保持 minimal obstruction。

假想來源為 disk，則 target 仍為 disk，且所有分量 spokes 仍位於原 arc。
接上 **單 triangle 報告 §3–6 的正常形與非 disk 證書**：它們只需該 arc、
degrees 及 F={D}，不要求 target 仍接受全部 T4。T4 只用於原圖最初的
區域定位；所以中途沒有丟失一個後續必需的 T4 前提。旁支型則接樹正常形。
兩者皆矛盾，完成任意長度的單奇環排除。

## 6. 有限控制、重播與信任範圍

[checker](../scripts/c5_degree5_odd_cycle_components.py)、
[certificate](../artifacts/c5_degree5_odd_cycle_components/observations.json)。

| 核對項目 | 固定域與結果 |
| --- | --- |
| Cycle list 引理 | C3、C4 的所有至少二色 lists，C5 的所有二色 lists，共 23,748 組；路徑動態規劃與完整 tuples 交叉核對 |
| 不同接點介面 | 六種 S、兩端各兩種補色、C3／C5／C7／C9 的全部不同接點距離、singleton／無限制訊息，共 12,000 次查詢；縮成 triangle 的可延拓性一致 |
| 共同接點介面 | 六種 S、四種環長、兩臂各五種訊息，共 600 次查詢；另核對 root 色集恰為 U\S |
| 真實圖與 minor | 不同接點 72 張、共同接點 60 張、旁支 15 張；環長 5、7、9。逐張核對 degrees、四個 z 色、每條非 boundary 邊刪除的 q-coloring、boundary 固定 branch sets |
| 來源非平面證書 | 全部 147 張來源的 apex 圖，各從已保存的 triangle／樹 subdivision 合成 K5 或 K3,3 minor，直接核對來源邊與 branch sets；不呼叫 planarity |
| 不保持二元關係的控制 | 保存 §3 的 (2,2) tuple、C5 完整 coloring 與 triangle 拒絕 |

三段 arc 長度分別取 (1,2,2)、(2,1,4)、(3,4,2)，含兩段偶數長的情況，
不是只測各邊偶數次 subdivision。不同接點控制涵蓋六種 S 及全部 c_u,c_v，
包括零長臂；共同接點控制涵蓋五種閉色序列的每個標記位置。
新插入點的 B-spoke 接點在 b1／b3 間變換，D 葉點也保留實際接線。
這些具名來源只驗證實作與機制；任意環長、位置、外枝的覆蓋由 §1–5 承擔。

程式及直接／既有相關依賴、兩份輸入證書的 SHA256 一併保存；`--check`
重算並逐 byte 比對。新 checker 不重建 triangle 的 89,224 個 lifts，完整
既有模板覆蓋另由下列前輪 checker 重播。

```bash
uv run --with networkx==3.5 python scripts/c5_degree5_odd_cycle_components.py --check
uv run --with networkx==3.5 python scripts/c5_degree5_triangle_components.py --check
uv run --with networkx==3.5 python scripts/c5_degree5_tree_components.py --check
lake build
git diff --check
```

本輪實際驗證見 [STATUS 歷史 §14](STATUS_HISTORY.md#14-三-spoke-單長奇環二接點排除)。
沒有修改前三輪 scripts／artifacts，沒有新 planarity search、Lean theorem、
舊全量 catalogue 或 deletion audit 重跑。Apex-disk 等價與 minor／無界化約
仍是紙面信任，Python 證書不是一般拓撲形式化。

## 7. 精確停止點

三-spoke、單一二接點分量的 C 已排除任意樹與任意單 odd-cycle 加 bridges；
K4 由既有連通外框引理排除。因此未解來源必含至少兩個 odd-cycle blocks。

**下一個窄問題：C 恰有兩個 triangle blocks，其餘為 bridges。**
先分兩環共用 cut vertex、兩環由 bridge 路徑相連，保留兩個 z 接點在
block-cut tree 的實際位置，並先消去不含接點的單 bridge 外枝。研究雙環
共同色框下 F_C(q)={D} 的正常形與 boundary 固定 minor，不能把兩環的
root marginals 獨立拼接，也不直接把本輪單環結果逐環套用。

兩環中含長環、更多環、其餘接點分拆、一般 degree≥5、單側／共同出口、
候選 A、一般 weak-deletion congruence 與 `K∞=K≤5` 各自仍需證明。
