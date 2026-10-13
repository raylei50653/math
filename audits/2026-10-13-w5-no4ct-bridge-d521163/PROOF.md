# W5-NO4CT-BRIDGE：三支共同私人圈秩下界

2026-10-13，BASE `d5211633ba80c2b10cb12eaa8189421e35a31cc3`。
輸入與舊 seal 見 [INPUTS](INPUTS.json)，逐項依賴見 [DEPENDENCIES](DEPENDENCIES.md)。
本證明抽取舊分類真正使用的局部前提，再從新 no4ct 契約逐條供應；
不把舊來源定理整包改稱無四色定理前提。

## 1. 定理、量詞及共同局部前提

K 是固定 132 個完整有序 C5 關係及其至多五內點 witnesses。假定目錄外
disk-C5 來源存在，在**所有**完整 Σ 不屬 K 的有限簡單 plane disk-C5 圖中，
先最小化內點數 k，再最大化邊數，取 G。原始比較圖類允許 chords 及不連通。
採用已接通 no4ct 的正規形、完整度數界及 K≤15；保留其外部有限計算信任。
不要求某個固定 mask 自己最小，也不加入 N2、ε、edge-critical 或 Gallai。

**W5-NO4CT-BRIDGE 定理。** 對上述 G 的**任意**合法全內部 induced W5，
記原中心 v、原循環鄰環 U=(u0,…,u4)、原有序外框 B=(b0,…,b4)，令

\[
P=V(G)\setminus(B\cup U\cup\{v\}),\quad F=G[P],\quad r=|P|=k-6.
\]

則對 932／933／941 三支共同有

\[
\boxed{\rho(F)=|E(F)|-|V(F)|+c(F)\ge5.}
\]

c 計所有私人分量，包括尚未排除的孤立分量。合法 W5 意指 B/U 十 pins
互異，v 的完整鄰集恰為 U，U induced，U 有界 disk 恰由 v 和五個原三角面
填滿。全內部 W5 的存在由 frontier 已供應；以下選擇任意一個，不只選其
存在證明所找到的中心。

舊低圈秩分類只消費下面的局部前提 L：

1. A=G−v 是指定 B 外面／U 空內面的原 plane annulus，B/U 各 induced C5，
   其他原面全部三角化；沒有刪任何私人點或私人邊。
2. 每個 x∈P 的**完整** d_G(x)≥5，且 x 不接 v。
3. 每個 x∈P 在 B、U 各至多接兩個 pins；雙接必相鄰。
4. r≥8 足供全部舊分類（ρ≤3 原下界 r≥7；ρ=4 原下界 r≥8）。

來源面、rotation、所有分量、cutvertices、bridges、subdivisions、原附件
都屬 L 中的原圖資料。Σ 的 933／941 特性不是 L 的一項。本輪實際供應
更強的 r≥10，使用原必要模板超集即可，不修改它們的 BASE 或參數域。

## 2. 新契約供應 L：相對 cap 與雙環附件

新 [frontier W5 證明](../2026-10-13-c5-no4ct-frontier-6943561/w5/PROOF.md)
§§1–5 已在三支下給 G 簡單二連通、B induced、原內面三角、d_G(B)≥4、
d_G(V\B)≥5、無 occupied triangle、k≥16，以及合法全內部 W5 存在。
因此 L1、L2、L4 已供應。下面明列 L3 的來源，避免漏掉接觸原框的小 cap。

**CAP-REL 引理（已由 frontier 證成，本輪接入）。** 每個原簡單 C4，及
每個異於 B 的原簡單 C5，其有界 cap 的私有內點數 s 都嚴格小於 k。
因 B induced，此環必含 i(C)≥1 個原內點作介面，故

\[
s\le k-i(C)<k.
\]

此式也涵蓋環接觸 B；不只處理完全內部環。B 上的點不會嚴格位於內部
cap。受限 C4 引理遂給 ≤3 內點的完整有序關係代表；proper C5 則由全域
最小性進 K，給 ≤5 內點代表。同一 literal 介面指派的延伸存在性保持，
故替換保持完整外 B 關係，最小性迫 C4 的 s≤3、proper C5 的 s≤5。
原 cap 內點 degree 等於 d_G，配合小 patch Euler／outerplane 計帳，得到
原 C4 有界側空，proper C5 有界側空或恰為 W5。
這裡不使用任意大小 C4 代表，也不把 full-lift 存在性說成等量雙射。

**ATT-B 引理。** 若內點 x 接 B 上不相鄰 a,c，短原框弧寫 a−b−c。
原 C4 a−b−c−x 的有界側空；原三角化及 B induced 迫唯一 diagonal bx，
且此 cap 佔滿 b 的內侧 sector。因此 N_G(b)={a,c,x}，違反 d_G(b)≥4。
故每個私人點至多接兩個相鄰 B pins。此為 frontier §4 的原框證明，
不借用僅屬 933／941 的舊外框計數結論。

**ATT-U 引理（本輪明示共同接點）。** 若 x∈P 接 U 的不相鄰 ui,uj，
原 C4 x−ui−v−uj−x 的兩條 v-spokes 在原輪盤內分開 U 的兩條開弧。
两開弧皆非空；x 與其接 U 的邊在原 U disk 外，故 Jordan 分離使此
C4 兩側各有一條非空 U 開弧。其有界側含原 U 點，違反 CAP-REL 的
C4 空 cap 結論。因此 U 的雙接亦必相鄰，至多二。

這兩條附件引理對任選合法 W5 皆成立。其後只用

\[
d_G(x)=d_F(x)+d_{B\cup U}(x),\qquad d_{B\cup U}(x)\le4.
\]

所以 F 無孤立點；私人 leaf 的完整 degree 恰五，且 B/U 各接兩個相鄰
pins。**沒有推出 d_F≥5**。proper C5 結論供應上游來源結構，低圈秩模板
分類在取得 L 後不再消費它。普遍 exterior 4CT screen、singleton support
非空及一般九點 W5 代表也都不進入 L。

## 3. 任意分量、橋及原面位置的共同計帳

令 q=ρ(F)、c=c(F)，t 為 PPP 原三角面數，p 為 B–U 原邊數，a 為全
terminal annular 原三角面數，M 為 BUP 原三角面數。A 連通（G 二連通），
兩指定面長五；Euler 及 face incidence 得

\[
e(A)=3r+20,\qquad f_{\rm ann}(A)=2r+10,\qquad e(F)=r-c+q.
\]

私人邊兩側分別計 incidence，bridge 也算兩側。恰含兩私人點的面有
2e(F)−3t 份；十條環邊各有唯一 annular incident 面，恰一私人點及兩個
同環 pins 的面有 10−a 份。於是

\[
\boxed{M=2(c-q+t),\quad p=a+c-q+t,\quad
\sum_{x\in P}d_G(x)=4r+10+q-c-p.}                 \tag{1}
\]

F 的有界面數是 q；B 位於無界面，連通 U/v 位於同一個 F 面。不含 U/v
的有界 F 面沒有其他 G 頂點，也沒有可跨其邊界進入的原邊，故就是 PPP
原三角面。這包括多邊界分量與 bridge slit 的候選：它們不能充當原三角面，
因此被排除，並未被忽略。反向每個 PPP 原面也是這樣的 F 面。

**FACE-SPLIT 引理。** U/v 位於 F 無界面，稱 contractible 分支，此時
t=q。否則 U/v 位於一個有界 F 面，某個 boundary walk 可去回溯分解出
包圍它的簡單原環，即 essential 分支，此時 t=q−1。兩支互斥且窮盡
同一原嵌入；不是要求每個私人環 individually essential。

Contractible 時由 (1) 與完整度數得

\[
M=2c,\quad p=a+c,\quad r\le10+q-2c-a.             \tag{2}
\]

Essential 環阻斷 B–U 原邊，p=0；(1) 迫 a+c−1=0，故

\[
c=1,\quad a=p=M=0,\quad t=q-1,\quad r\le9+q.    \tag{3}
\]

私人 leaf 必產生 BUP 面，故 (3) 排 leaf。PPP 面角若 d_F=2，另一個
terminal sector 至少有三 pins，亦迫 BUP 面，故 essential 分支每個
PPP 面角 d_F≥3。這些結論不能反向移到 (2)。

## 4. 森林至圈秩二的來源覆蓋

細部逐原來源審查見 [LOWRANK](review/LOWRANK.md)，原分類入口為
[單環 STRUCTURE](../2026-10-13-w5-private-unicyclic-3097ef5/structure/STRUCTURE.md)、
[雙環 TOPOLOGY](../2026-10-13-w5-rank2-243a125/structure/TOPOLOGY.md)及
[雙環 STRUCTURE](../2026-10-13-w5-rank2-243a125/structure/STRUCTURE.md)。
它們取得 L 後的論證均不查来源 mask。

* q=0：必為 contractible，(2) 給 r≤10−2c−a≤8，與 r≥10 矛盾。
  因此本輪森林直接紙面排除；舊 70 模板及 receipts 保存，不重播染色。
* q=1 contractible：唯一 cyclic block 是 PPP 三角形，三個根各由自身
  degree-two 角或原附樹的 leaf 貢獻不同 M 面；其餘樹分量各至少兩個。
  故 M≥3+2(c−1)>2c，矛盾。Essential 時無 leaf、無附樹、無其他分量，
  F 恰為原純環。其兩側原 fan 每步只能 (1,0)、(0,1)、(1,1)，總量各五。
  (3) 與 r≥10 迫 r=10，落入舊 1,652 模板中的 252 份；完整 Σ=1023。
* q=2：原 2-core 分類為分離雙單環、figure-eight、barbell、theta，
  保留所有根樹、獨立樹分量及原細分。FACE-SPLIT 同時處理 nested、共點、
  共路徑及 U 所在面。Essential 時 t=1、私人 excess
  Σ(d_F−2)=2，但 PPP 三個角各至少一份 excess，矛盾。
  Contractible 的兩個 PPP 面若不共原邊，就由三角 blocks 的 ear／leaf
  計帳超過 M=2c；只留 diamond theta、其兩 ears 的原 tails 及容許 path
  分量。等號禁止分叉及非 ear 附樹。由 (2)、r≥10 迫 c=1,r=10,a=0。
  原 strip 編碼覆蓋舊 974 模板中的 70 份；完整 Σ=1023。

q=1/2 的最後數字是舊 immutable 模板索引的子域，不是本輪重算染色。
也可直接使用舊全域 masks 均在 K 的既有結論，無須縮減代表。

## 5. 圈秩三、四的全部幾何分支與模板接入

詳見 [RANK3](review/RANK3.md)、[RANK4](review/RANK4.md)。Contractible 的
原有界面全為 PPP 三角面；q≤4 時若私人點不 incident 無界面，它不能接
terminal，且其全部 sectors 至多是 q 個三角面角，給 d_G≤4，矛盾。
因此原 F outerplane。其 cyclic blocks 是三角化 polygons；cyclic 邊
不能任意細分而保留原三角面，原 bridge paths／tails 的 subdivisions 則
完整保留。這是原面結論，沒有換嵌入或把原橋收縮。

對含 m 個 cyclic blocks 的私人分量，以 e_j 記每 block 的 ears 數。
在 block-cut tree 的最小連接骨架，cyclic block incidences 總和至多
2(m−1)。未用於接合的 ears 以自身或原附樹 leaf 注入不同 BUP 面，至少
供應 Σe_j−2(m−1) 份；純樹分量至少兩份。M=2c 因此排除三-ear blocks，
並迫留下的兩-ear 接合、tails、純樹全部取等號。這處保留共 cutvertex，
兩個 ears 共用時不拆點，也不把長度零接合當成有兩個端點的邊。

| q／分支 | 紙面分類所得原圖形狀及完整覆盖 | 新 r≥10 下落入原模板的域 |
|---|---|---|
| 3 contractible | 唯一 pentagon fan block、兩 ear tails；可另有 path。triangle+diamond／三 triangles 由 M 預算排除，K4 內點由完整 degree 排除 | c=1,r=10或11；c=2 的 r≤9 已排。原 2,270 份中 484 份 |
| 3 essential | t=2、c=1、M=0、私人 excess 四。兩 PPP 面只能共邊成 diamond；唯一 ear-to-ear 原外路涵蓋全部其餘私人點 | r=10..12；原 1,283 份中 790 份 |
| 4 contractible | 三角化六邊形的 fan／zigzag 兩-ear 型，或兩 diamonds；central 三-ear 型及含 triangle 的分配均排。全族 H、DD、H+P、DD+P、D+D 保留 shared ear／全部橋長／tails | c=1,r=10..12；c=2,r=10,a=0。原 6,389 份中 2,955 份 |
| 4 essential | t=3、c=1、M=0、私人 excess 六。PPP 面交疊分類排 K4、分離 clusters、只共一點／兩非鄰點等項；恰成 pentagon fan 加唯一 ear-to-ear 原外路 | r=10..13；原 2,872 份中 2,368 份，含短側接 B/U、apex 一／二附件 |

每個分支從原 contour 讀 terminal link intervals；每環附件至多兩個相鄰
pins，故每次前進只有 0 或 1。每條原環邊恰有唯一 annular incident 面，
兩環总前進量各五，不能倒退重用、跳 pin、漏邊或獨立反向。
Contractible 有 p=a+c≥1：沿所有原 B–U crosscuts 切開後，region 恰為
一個私人 strip 或一個 terminal triangle。每個分量恰需兩個 M 面，而
每 region 至多兩個，故不會把另一私人分量隱藏於同 region；p=1 時保留
同一 crosscut 的兩個 sides，共 endpoint 的 crosscuts 亦保留。
Essential 無 crosscut，兩側 contour 及唯一原外路讀出 cyclic words。

原 generator 先完整列出這些參數、原 faces 和 edges，再算 Σ，沒有以
mask=933/941 或接受 singleton 列篩除來源。Contractible rank4 的
816 份未滿足額外 B/U degree 的模板仍保留，正說明它是必要域超集。

各分支重建是原帶嵌入圖同構：

\[
g_B(i)=s_B+\epsilon i,\quad g_U(i)=s_U+\epsilon i\pmod5,
\qquad\epsilon\in\{1,-1\}.
\]

兩環共享方向，各自可換起點；若原 U 按面方向命名，先記固定方向換算。
此映射搬運十 pins、中心 ownership、所有點邊、面、rotation、全部空／非空
fibres 與 A/G full lifts；只容許全圖共同 S4 更名。不使用不同列 witnesses
拼接，不把同 Σ 當同 R³，更不宣稱不同圖 fibres 等量。

## 6. 不改舊 seal 的有限證據接合與結論

原七份完整證據共 15,510 模板，所有完整 Σ 均在固定 K。
本輪 [evidence.py](evidence.py) 按原 SHA／manifest 核對證據 bytes、summaries
與既有正常／seed17／獨立覆核 receipts；沒有重枚舉原染色或改舊 BASE。
其中 r≥10 的數字 6,919 只是由舊摘要／索引限制出的必要子域；完整度數、
其他小 cap 條件或來源身份可再排去其中部分，不宣稱它們可實現為最小來源。
本輪另核對 K 的全部 D5 搬運封閉，故 canonical Σ∈K 拉回原 B 仍在 K。

假設 q≤4，§§3–5 先把任何原來源完整放入對應必要域，然後才使用該域的
完整 Σ∈K，與來源目錄外身份矛盾。這一步的矛盾對 932、933、941 均相同；
不需先排 932，也不需普遍 planar colourability。於是任取合法 W5 都有 q≥5。

本輪沒有剩餘低圈秩前提缺口。這是**新來源契約下的條件定理**：紙面來源
覆蓋＋沿用有限完整證書＋明列 no4ct 上游信任；不是 Lean theorem。
真正最小三支來源仍為 `not triggered`，零觸發不承擔排除。
一般 q≥5 來源的縮減、無界三支排除及 K∞=K≤5 仍 OPEN。
一般九點 W5 代表不在本定理前提或交付內容，亦未展開圈秩五／六枚舉。
