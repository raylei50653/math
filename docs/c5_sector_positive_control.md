# 3903 的既有非 disk 正控制

2026-09-18。**找到所需正控制**，沒有擴大生成範圍：來源是已保存的
[樹分量證書](../artifacts/c5_degree5_tree_components/observations.json)
`templates[41]`（從 0 起算），不是新生成的 |C|=4 搜尋。
它的 sector K 滿足 proper Σ=831、E_B=E_C=true，即完整簽章 3903。
K 本身非平面；這不是「K 平面但指定 C5 不同面」的例子。
本輪未證一般 disk 排除，未新增 Lean theorem。

後續修正：[拓撲與條件相等引理](c5_sector_structural.md) 已由一般論證證明，
在 induced 框圈＋非空連通 C 的子類，平面等價於指定 disk。
「平面但非 disk」分支已取消；不是由本報告的 22 份控制外推。

提交整理：本報告與程式／證書隨三輪成果整合提交，不 push；驗證沿用與
歷史狀態說明見 [STATUS §41](STATUS.md#41-sector-三輪研究整合提交)。

## 1. 實際接線及開口結果

沿用原圖 boundary b0,…,b4、內點 z=5，取 u=6、v=7、w=8、x=9。
原圖含 C5 框邊，另有：

```
z ~ b0,b1,b4,u,x
u ~ v,b1,b4       v ~ w,b1,b4
w ~ x,b1,b2       x ~ b2,b3
```

每條邊只需加入一次。C 是路徑 u–v–w–x，四點完整 degree 都是 4，
z 在原圖 degree=5，兩個不同內接點為 u,x。
移除 b0（其鄰居恰為 b1,b4,z）得到 K，不丟棄任何碰 C 的邊。
K 的有序框為 `(z,b1,b2,b3,b4)`；artifact 將 z 重標為 0，其餘標號保留。

使用 [十二列順序](c5_sector_targets.md#1-查詢域與五個目標)：
proper 十列只拒絕第 6、7 列，mask=831；第 10、11 列都接受，故 mask=3903。
在原 q 色框 A=0、B=1、C=2、D=3 下，路徑的 boundary residual lists 為
`{A,D},{A,D},{C,D},{C,D}`。可手核對下列 fixed-q 著色：

| z 色 | (u,v,w,x) 的一份延拓 |
| --- | --- |
| A | (D,A,D,C) |
| B | (A,D,C,D) |
| C | (A,D,C,D) |
| D | 不存在：依序迫使 (A,D,C,D)，末端撞 z=D |

因此 F_C(q)={D}，並非只驗兩個開口正例。
回到原 boundary，Σ(G)=958，恰拒絕 q=01012 及 p=01212；
其 singleton 位置 b4、b0 相鄰。全部 T4 接受。
逐一刪除原圖 16 條非 boundary 邊，q 都可延拓，故此圖確為 minimal
q-obstruction；它欠缺的是 disk 條件。不能稱為 disk Candidate A 反例。

## 2. 可直接手核對的非平面證書

K 內有 K3,3 subdivision，兩側 branch vertices 為
`{b2,v,x}` 與 `{b3,u,w}`。九條路徑如下：

| 左側頂點 | 到 b3 | 到 u | 到 w |
| --- | --- | --- | --- |
| b2 | b2–b3 | b2–b1–u | b2–w |
| v | v–b4–b3 | v–u | v–w |
| x | x–b3 | x–z–u | x–w |

路徑內點僅 b1、b4、z，各使用一次，且都不是 branch vertices；所有邊均
屬上列 K 的實際邊。因此不需要外加 apex，就可驗證 K 非平面。
這個具體連接衝突給出研究材料，但不表示所有 3903 實現必有同一 subdivision。

## 2a. 保留框圈的較小證書

同一張第 41 號控制另有 P=z–x–b2、Q=b1–v–b4，端點沿框圈交替，
兩路徑頂點互斥；C 中的 R=x–w–v 連接其內點。九條分支為：

| 左側 | 到 b1 | 到 b4 | 到 x |
| --- | --- | --- | --- |
| z | z–b1 | z–b4 | z–x |
| b2 | b2–b1 | b2–b3–b4 | b2–x |
| v | v–b1 | v–b4 | v–w–x |

內點僅 b3、w，不使用 u。這是取非平面子圖的證書，不是保持 Σ 或
minimality 的刪點化約。原證書與其餘 21 份控制不變。
新證書存於 [structural artifact](../artifacts/c5_sector_structural/observations.json)
的 `smaller_subdivision`，由 structural checker 直接核對，不用平面性 oracle。
一般構造與尚待證的兩路徑存在性見 [拓撲報告 §1a](c5_sector_structural.md#1a-交替互斥路徑的構造式非平面證書)。

## 3. 有界的既有資料稽核

本輪只讀該份既有證書的全部 648 個 templates 明列的 `edges`。
未重新生成正常形，未枚舉新接線，也未掃完所有其他非 disk artifacts。
全部 648 份都通過指定 degree、連通、兩個內接點及外側 b0 可移除檢查。
每張圖的十二列以完整圖回溯與獨立的樹 list 訊息遞迴交叉核對，共 7,776 列。

| 層次 | 命中數（保存的有標號接線） |
| --- | ---: |
| proper 十位=831 | 22 |
| 完整十二位=3903 | 22 |
| K 本身非平面 | 22 |
| K 平面但非 disk | 0 |

22 份的 C 都有四點，不將它們說成 22 個不同同構型。
其來源索引是 41,42,44,45,47,48,49,50,51,53,54，及各加 120。
所有 proper 命中均保存完整 sector 邊與 K3,3 subdivision；其餘 626 份
本輪只記染色層結果，拓撲標示未檢查，不把舊報告的非 disk 判斷當作
本輪 K 本身的非平面性核對。

第 41 號另以獨立的內部四色 assignment 窮舉對照回溯染色，核對：
十二列、K 的全部 240 個 proper 有標號 boundary rows、G 的全部 240 列、
全部 16 條刪邊；正例保存實際 coloring。
初次尋找 subdivision 使用 NetworkX 3.5；`--check` 禁用 planarity oracle，
直接逐邊檢查保存的路徑、內點互斥及 K3,3 incidence。

## 4. 分層初測的來源界線與下一問

使用者另回報同一 |C|≤3 範圍的獨立分層稽核：proper masks
575、631、823、829 各零命中，831 有兩份且都是 1855；即使不要求 disk，
相鄰雙缺失也只有這兩份。其 18,576 次交叉染色及 NetworkX 3.6.1
拓撲檢查屬使用者腳本結果；sandbox 附件在此工作環境不可讀，本輪
沒有將它們冒充 repo checker 重播，也未修改前輪的搜尋證書。

本輪正控制排除了「3903 被一般 degree／接點／跨列染色條件直接禁止」
這個可能：那些條件確能共存，甚至原圖 minimality 也成立。
在本報告的子類，平面與指定 disk 已由後續一般引理證明等價；不再
保留兩者的研究分岔。22 份控制只承擔具體正例證據，不承擔一般排除。

當前待證問題精確保留為：指定 disk 結構、連通 C、內點 degree=4、
z 有兩個不同內接點時，是否

```
Σ(K)=831  =>  not (E_B and E_C) ?
```

不預設一定額外禁 C；即使此式證成，也不排除另外四個目標。
下一步可研究此正控制的三組互不相交連接，哪些能由 Σ=831 與兩開口
共同接受在任意實現中導出。尚無這個必然性引理，不自動擴大搜尋。

## 5. 重播與信任範圍

[checker](../scripts/c5_sector_positive_control.py)、
[certificate](../artifacts/c5_sector_positive_control/observations.json)。
保存來源及直接程式依賴 SHA256；來源舊證書不改寫。

```bash
uv run --with networkx==3.5 python scripts/c5_sector_positive_control.py --check
lake build
git diff --check
```

本輪新 checker、Lean build 及 whitespace 檢查通過。舊樹分量完整 checker、
前輪 |C|≤3 生成器及其他 R 系列覆蓋沒有重跑。新結果是固定具體圖的
Python 染色／subdivision 證書，不是新 Lean theorem。未 commit／push。
