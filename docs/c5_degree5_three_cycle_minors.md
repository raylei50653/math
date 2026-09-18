# 三環共用點鏈：任意長環與重複色外臂的來源 minors

2026-09-18，R27。接手 HEAD `e14874d` 與未提交 R24–R26。
本輪未 commit／push；成果為紙面構造＋Python 有限來源證書，未新增 Lean theorem。

**在 R25 的三環共用點鏈型，任意奇環長度與重複色外臂可化到 R26 的
三個 triangle 正常形，並合成來源非 disk 證書。** 精確範圍是
J1∩J2={r12}、J2∩J3={r23}、J1∩J3=∅、r12≠r23，兩條外臂
分別接末端環私有點。沿用三-spoke 區域定位與 forcing-list 正規化；
唯一 degree-5 點為 z，其餘有效內點完整 degree=4，來源為接受全部 T4
的 C5 disk minimal q-obstruction。這個型因此被排除。
**其他三環接點／連接型及一般三環排除仍未完成。**

## 1. 長環的 boundary 固定 minor

依 [R25](c5_degree5_three_cycle_roots.md)，固定 q=(A,B,A,B,C)、z=D
時拒絕強迫 T–S–T 交替 palettes，S=U\T。每個末端環保留其共用點、
外臂接點及任一其他私有 T 點；中間環保留兩共用點及任一私有 S 點。
這些點各自存在，包含原環就是 triangle 的情形。

按來源環的循環次序記三個保留點 v0,v1,v2。每段 vi→v(i+1) arc
的內點全部收進 vi 的 branch set，刪除其 attachments 與私有 D 葉；
保留端點的 attachments 和兩臂。末段邊實現目標 triangle 邊。
三段可以有偶數長度，只要求總環長為奇數，沒有逐段奇偶的限制。

三環同時做此構造時，r12 的 branch set 是 J1、J2 分配給它的
兩段之聯集，兩段只在 r12 相交；r23 同理。中間環的兩段內點
互斥，所以這兩個共用點不會被識別。所有 branch sets 連通、非空、
互斥；boundary 點與 z 仍為 singleton。末端接點及 palette 錨點
各自留在自己的 branch set，任何 branch set 恰含一個保留點。

也可一次只縮一個環。三個環任一順序都給出同一組合成 branch sets，
各中間圖均保留原有 attachments 與外臂。共用點仍有四條環邊，接點
仍有兩條環邊、一條臂邊及一個禁色，其餘私有點兩條環邊及兩個禁色；
故 degree=4／5 不變。這是實際刪點、刪邊與收縮構造，非僅 list 替換。

## 2. 重複色臂的真正 minor

任一外臂的強迫色序列記為 w=(D,...,c)，c∈S；每對相鄰不同色
wi,wi+1 對應一個 list={wi,wi+1} 的臂點，末端接點 list=T∪{c}。
若 wi=wj，i<j，刪掉該閉段，改為 w[:i]+w[j:]。

把沿臂由 z 開始的點列記作 p0=z,p1,...,pn；pk 是第 k 個
二色 list 點，w 長度為 n+1。保留 pi，將 pi+1,...,pj 收進
pi 的 branch set；刪除被收進點的 attachments／D 葉，保留 pi 的
attachments（i=0 時保留 z 的三 spokes）。其餘臂點、環點及其
attachments 都單獨保留。因 wi=wj，下一個保留臂點的 list 與所需
色轉移一致，最後一條臂邊仍接同一末端環點。

每步嚴格縮短色序列，故終止於不重複四色的簡單序列。若終色為 D，
終點與起點相同，最終整條臂收進 z，得到直接接入；兩條臂若都如此，
它們只在 z 相交，所以 z 的合成 branch set 仍連通且與其他集合互斥。
此處 boundary 始終固定，但 **z 在縮臂後不必是 singleton**。
兩個共用點及所有環上保留點不會被縮臂識別。

保留臂點仍有兩條路徑邊與兩個禁色，末端接點仍有一條臂邊，z 仍恰有
三 spokes 與兩條臂邊。保留的 boundary 接線按原來源搬運，不能任意
選一個同色 boundary 點替換。最終圖恰屬 R26 的 408 模板及其實際接線域。

## 3. 四列、minimality 與拓撲合成

縮任意子集的環時，[R25 §3](c5_degree5_three_cycle_roots.md#3-可保持的縮環語義)
保證四列可延拓布林值不變。縮臂後，D 列仍輸出原終色 c，且此指定
singleton 的反向輸入唯一；a≠D 不會輸出 c。每個末端環仍保留未標記
T 錨點，因此 R25 的完整接合判準再次給出 F={D}。這不要求保存
中間環完整二元關係、末端完整 root 色集、任意 pinning 或完整 Σ。

所有中間圖 q 不可著色；刪除任一碰到 degree-4 分量的邊，依
[R11 分量解除引理](c5_degree5_interfaces.md#3-刪除分量任一邊禁色全部解除)
在 z=D 可延拓。刪 z 的一條 spoke 釋放其 q 色 a≠D，該列已可延拓。
因此每個中間圖重新得到逐邊 minimality，而非假設 minor 自動保持它。

把 R26 目標的五個 boundary 點接一個外部 apex，其已存 K3,3
subdivision 收成 minor，再與來源→目標的 branch sets 合成；來源
augmentation 的 apex 單獨保留。每條目標邊均核對實際來源邊，得到
來源 augmentation 的 K3,3 minor。假想來源若能嵌入 C5 外邊界 disk，
augmentation 必 planar，矛盾。T4 只用於原先的區域定位；不要求
收縮後保持所有 T4 rows。任意長度覆蓋來自上述一般構造與 R26 完整
正常形覆蓋；下節有限控制用來驗證實作，並非任意長度的枚舉證明。

## 4. 有限來源控制及重播

[checker](../scripts/c5_degree5_three_cycle_minors.py)、
[certificate](../artifacts/c5_degree5_three_cycle_minors/observations.json)。
按六個 S 及兩臂各自終色分 24 桶，從 R26 每桶取最短／最長臂 seed，
共 48 個 seed（seed 標籤不宣稱互異圖）。每個 seed 做兩種重複色擴充，
包含前綴、內部／後綴閉段、整條 D→D 臂；再擴三環成 (5,7,9) 或
(7,9,5)。三段 arc 分別採 (1,2,2)、(2,1,4)、(3,4,2)。
縮臂的終點模板由實際簡單序列重新定位，未假定必回原 seed。

共有 96 份來源控制，對應 90 張不同標號來源圖；48 個 seed 選取對應
45 個不同模板，縮臂後使用 56 個不同 R26 目標模板。
每份來源控制核對全部八個縮環子集、cube 的十二個逐步 minor、全部六個
環縮減順序的合成相等；再逐步縮兩臂。每個圖階段直接檢查 degrees、
四種 z 色、q 拒絕，並保存所有非 boundary 邊刪除後的完整著色。
每張來源均保存合成 boundary 固定 minor 及來源非平面 minor。

生成及 `--check` 都停用 NetworkX planarity APIs；只讀取 R26 已存
subdivisions，直接核對所用路徑及 branch sets。保存所有載入的本地
程式 hashes 與 R26 artifact hash；證書採緊湊 JSON 保留全部 witnesses，
checker 唯讀逐 byte 比對。
本輪統計與實際驗證結果見 [STATUS §31](STATUS.md#31-r27-三環共用點鏈來源-minors)。

```bash
uv run --with networkx==3.5 python scripts/c5_degree5_three_cycle_minors.py --check
lake build
git diff --check
```

R26 的全部 327,968 接線與 R25 完整介面 checker 本輪不重跑；依賴其
既有覆蓋／紙面判準，並核對 R26 程式指紋與本輪每個所用 subdivision。
R15／R17／R19 大覆蓋亦不重跑。Lean build 不代表本輪結果已 Lean 化。

## 5. 下一個窄問題

後續 R28 已完成同鏈全部接點位置的 list 介面，並指出兩個不同接點
同在中間環時需用保留四標記的 C5 目標；見 [R28](c5_degree5_three_cycle_positions.md)。
後續 [R29–R30](c5_degree5_middle_cycle_minors.md) 已完成中間不同二接點
的任意長圖層排除；[R31](c5_degree5_same_terminal_triangles.md) 已完成
同末端不同二接點正常形。以下保留 R27 當輪停止點；最新待辦見
[HANDOFF](HANDOFF.md)。

本輪只封閉 **兩臂在末端私有點的三環共用點鏈**。下一步先分類同一
J1–J2–J3 鏈中，兩臂未各落末端環的接點型：同末端環、末端與中間、
兩臂在中間，以及外部先會合。先確認無接點的末端環消去後是否交回
既有零／一／二環結果；若留下非平凡二接點限制，再求完整接合關係。
環間含 bridge 的三環連接型亦未由本輪處理。
一般三環、更多環、degree-5／degree≥5、單側／共同出口及 `K∞=K≤5`
仍未證；不以這個鏈型排除代替一般三環定理。
