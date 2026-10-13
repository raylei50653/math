# W5-RANK3-C：原 blocks、M 計帳與完備 pentagon-strip 化約

固定 BASE：`50d5474f2446403f3b3001d5943571184c8c9936`。
本檔是紙面覆蓋論證；不以有限生成器的成功取代來源化約。
沿用完整最小目錄外 disk-C5 來源 G，及**任取**合法全內部原 W5。
記 A=G−v、P=V(G)\(B∪U∪{v})、F=G[P]、r=|P|、c=c(F)。
本輪反設 ρ(F)=3，且 U/v 位於 F 的無界面。全部圖、blocks、paths、
rotation 及 faces 均指原圖；下面辨認結構沒有修改任何原邊。

## 1. 只使用 contractible 域的輸入

一般面恆等式在本輪另行核對。contractible 條件令三個有界 F 面恰是三個
原 PPP 三角面，故

\[
t_P=3,\quad M=2c,\quad p=a+c,\quad
\sum_{x\in P}d_G(x)=4r+13-2c-a,\quad 7\le r\le13-2c-a.
\]

每個私人點對 B、U 各至多兩個鄰點，兩個時相鄰；因此
`d_G(x)=d_F(x)+d_T(x)`，`d_T(x)≤4`。完整 `d_G(x)≥5` 排除私人孤立點。
本輪已核對的分量收窄只留下

| c | r | a | p | M |
|---:|---|---|---|---:|
| 1 | 7≤r≤11 | 0≤a≤11−r | a+1 | 2 |
| 2 | 7≤r≤9 | 0≤a≤9−r | a+2 | 4 |

這裡沒有使用 essential 域的 c=1、p=0、M=0 或私人無葉。
沒有額外假設 N2、ε、edge-critical、Gallai，亦沒有把私人 degree 當完整 degree。

## 2. 所有循環 blocks 的原嵌入分類

取 F 的標準 block-cut 分解；bridge blocks 及私人樹均保留。
一個含環的 block H 是原嵌入中的二連通簡單 plane 圖，其每個面邊界均為
簡單環。每個 bounded H face 的內部沒有 B、U、v：它的邊界是私人簡單環，
而全部 terminal 在 F 的無界面。

**有界 block 面不能藏私人點或別的 block。** 若一個 bounded H face
內尚有原點邊，把 G 在其簡單邊界所圍 disk 中的全部點邊加入。這是一個
內面全部三角化、外邊界簡單的 disk 圖，因此二連通：若有 cut vertex，
繞該點某個分隔 sector 的面邊界就重經該點，與所有內面三角且外邊界簡單
矛盾。這個私人二連通子圖包含 H 的該面邊界，與 H 的並仍二連通，違反
H 是 maximal block。故該面没有任何原點邊，必是 PPP 原三角面。
同一論證排除了內藏分量、橋的 slit 及 bounded block face 中的附樹。

令 h=ρ(H)，令 n、b、i 分別是 H 的點數、簡單外面邊界長及嚴格內部點數。
H 的 h 個有界面全是三角形，故

\[
e=n-1+h,\qquad 3h+b=2e,
\qquad n=h+2-i,\quad b=h+2-2i.                 \tag{1}
\]

總圈秩只有三，故每個 h≤3；b≥3 及原簡單性給出以下**完整**清單。

| h | 可能的原 block | 私人 block-degree 二的點數 |
|---:|---|---:|
| 1 | 原三角形，n=b=3 | 3 |
| 2 | 原 diamond：兩個三角面共一原邊，n=b=4 | 2 |
| 3 | 三角化原五邊形，n=b=5 | 2 |
| 3 | 外三角形加一個內點，即原 K4，n=4、b=3 | 0 |

五邊形的兩條 noncrossing diagonals 必共端點；故其三 PPP 面形成長二的
face-dual path，唯一原抽象形狀為 fan。這不是先假設三角面連通：其他
block 分布在下一節逐一處理。式 (1) 同時排除在這些 cyclic blocks 中
任意 subdivision；一旦 subdivide 原 core 邊便破壞其 bounded 三角面。
連接不同 blocks 的任意長橋路徑仍完全保留。

**K4 在原圖直接不合法。** 不能因為圖畫像 outerplanar 而删掉其內點。
設其唯一嚴格內部私人點為 z。三個 incident sectors 已是原 PPP 三角面；
任何其他原邊或 terminal 附件都無法進入这些空面。因此 z 在完整 G 中
只有 K4 的三個鄰點，即 d_G(z)=3，直接違反 d_G≥5。這也與原 occupied
triangle 限制相符，但排除本身只需完整 degree 及原面。

**另一个独立的原面核對。** 若私人點 z 不 incident 於 F 的無界面，任何
terminal 附件都無法接到 z，故 d_G(z)=d_F(z)。其所有 incident sectors 都
是 bounded F faces；每個 bounded face 是簡單 PPP 三角面，在 z 至多給
一個 corner。總共只有三面，故 d_G(z)≤3，矛盾。於是每個私人點都 incident
F 的無界面。這是由原 face 與完整 degree 推出的 outerplane 結論，不是
按圖形直覺預設；它也獨立檢查上面 K4 內點不能遺漏。

所以原私人 blocks 的圈秩分配只有：一個 pentagon block；或一個 diamond
加一個 triangle；或三個 triangles。它們可共享 cut vertices、經橋路徑
相接、分布在不同分量；任意附樹暫時都保留。

## 3. 可重用的 block-ear／leaf 計帳引理

先核對兩個局部事實：

1. 私人 leaf x 只有一個私人鄰點，故完整 degree 及附件界迫其接 B/U 各
   兩個相鄰 pins。原 rotation 中移去唯一私人鄰點後的 terminal link 是
   路徑，包含 B、U，故相鄰的異類 pair 至少給一個 BUP 原面。
2. 若原 PPP 三角面上的 x 在 F 中 degree 二，該面占一個 sector；全部
   terminal 在另一個 link 區間。完整 degree≥5 迫至少三 terminal，必
   同時有 B、U，因而至少給一個 BUP 原面。

兩個不同私人點不能被計入同一 BUP 面，因該面只有一個私人點。

考慮一個有 m≥1 個 cyclic blocks 的私人分量。令 e_j 是第 j 個 block
中 block-degree 二的點數（上表的 ears）。在 block-cut tree 中取連接
全部 cyclic-block nodes 的最小子樹，保留原 cut vertices 及橋路徑。
這是辨認原 connecting skeleton，沒有收縮原來源。
壓低此樹中非 cyclic nodes 的 degree 二點，只為**計數**；其他非 cyclic
nodes 的 degree 至少三，所有 leaf nodes 都是 cyclic blocks。
樹的 degree-sum 恆等式給

\[
\sum_{j=1}^m\deg_{\mathrm{skeleton}}(H_j)\le2(m-1).       \tag{2}
\]

若兩個 blocks 在同一原點相接，block-cut tree 中的該 cutvertex node
照常保留；因此 (2) 也涵蓋 figure-eight、共點三角群與一般 cutvertices。
每個 skeleton incidence 至多使用該 block 的一個 ear，所以至少

\[
L=\sum_j e_j-2(m-1)                                    \tag{3}
\]

個不同 ear 點不接 connecting skeleton 的其他部分。若這個 ear 沒有
額外附樹，它在 F 中 degree 二，用局部事實 2；若有附樹，在其中取一個
非 skeleton 私人 leaf，用事實 1。被剝除的每棵樹只接 skeleton 一個根，
否則其中的循環會產生另一個 cyclic block。因此不同所選 ear 的附樹
互不相交，得到 L 個**不同私人點**，供應 L 個**不同原 BUP 面**。
任何完全沒有 cyclic block 的非平凡樹分量另至少供應兩個 leaf charges。

這是下界引理；不需要假設所有原 M 面已如此找到。把額外附樹接到
一個 ear 可以把其 degree 二 charge 換成 leaf charge，不能消除 charge。

## 4. 所有多 cyclic-block 分支排除；完整原 F 剩餘形狀

若 c=1，圈秩三的分配如下：

| 分配 | 不同 BUP 面的下界 | 與 M=2 的比較 |
|---|---:|---|
| 一個 pentagon | 2 | 可取等號 |
| diamond + triangle | 2+3−2=3 | 矛盾 |
| 三個 triangles | 3+3+3−4=5 | 矛盾 |

若 c=2，兩個分量的圈秩只可能是 (3,0) 或 (2,1)，允許整體交換。
對 (3,0)，樹分量至少另供應兩個，故 diamond+triangle 或三 triangle
的 rank-three 分量分別迫 M≥5 或7，均違反 M=4。
對 (2,1)，rank-two 分量若為 diamond 至少供應2，若是兩 triangles
至少供應3+3−2=4；rank-one 分量必至少供應3。故總 M≥5，矛盾。

因此**兩個 c 分支共同的唯一存活形狀**是：一個 pentagon block，
其餘 c−1 個分量全是非平凡樹。pentagon 的兩個 ears 各供應一 charge，
每個樹分量至少兩個，恰好已用盡 M=2c，所以逐項取等號：

* pentagon 的三個非 ear 點沒有任何附樹，否則另生未計的私人 leaf。
* 每個 ear 的全部附樹只能是一條可空的單一路徑；分叉或兩棵附樹會有
  至少兩個 leaves，超出該 ear 的一個 charge。
* 每個額外樹分量恰有兩個 leaves，所以是非平凡原路徑。
* pentagon 分量恰有兩個 M 面，分別在兩個 ear（其尾為空時）或其尾末端；
  每個其他路徑也恰在兩個端點各有一個 M 面。其他私人點没有 M 面。

所有原 bridges、cut vertices、tails 及其每個 subdivision 點都在這個
描述中保留。這不是把 rank-two 的四型清單套到 rank-three。

## 5. 原 facial contour 迫 terminal 分側與全部附件

命名 pentagon 外面邊界為

`x – q1 – q2 – y – q0 – x`，

原 diagonals 為 `q0q1,q0q2`。其中 x,y 是 ears，q0 是 degree 四 apex，
q1,q2 各私人 degree 三。x、y 各自可接一條向外尾路徑。

沿每個私人分量的外 facial contour 走一周，原 bridge 的兩側各走一次。
在相鄰私人 darts 間，原 terminal 鄰點構成 link 區間；每次 B/U 類型
切換恰對應該私人點的一個 M 面。每條非 PPP 面側的私人邊亦有其原
terminal third vertex，給該 contour side 的 B/U 標記。
由 §4，每個分量只有兩次切換，而且恰在其兩個指定端點。故兩個端點
之間的兩段 contour 一段全 B，另一段全 U。

在 pentagon 上，短段通過 q0，長段通過 q1、q2；故 q0 只接一個環，
q1、q2 只接另一個環。先稱 q0 側為 B 型，反型交換 B/U 後完整保留。
原完整 degree 及附件界迫：

* q0 有一個或兩個相鄰 B 鄰點，完整 degree 分別是5或6。
* q1、q2 各有恰兩個相鄰 U 鄰點，完整 degree 都是5。
* 每條尾路徑及其餘路徑分量的每條私人邊，兩個原 face third vertices
  分別是 B、U。每個 backbone 點在兩環各至少有一個鄰點。

沒有把兩段 contour 獨立翻轉。q0 只接一個 pin 的可能性是必要分支，
不能為方便沿用 diamond 的「每側固定前進一格」。

現在 p=a+c≥1。按原 cyclic 次序沿全部 B–U 原邊切開 annulus；允許
相鄰 cross edges 共端點，以及 p=1 時同一原邊成為切開 disk 的兩側。
各 region 的其餘邊界是 B/U 的原前進子弧，內部不再有 cross edge。
一個私人分量不能跨過 cross edge。每個私人分量已有恰兩個 M 面，
而每個 region 的兩個 bounding cross-edge sides 合計只能承擔兩個
M 面，所以每個有私人點的 region 恰含一個私人分量。
若 region 無私人點，內部又無 cross edge，原三角化迫它恰為一個
BBU 或 BUU 原三角面。因此完整 cyclic region sequence 是

**一個 pentagon strip、c−1 個非平凡 path strips、a 個 terminal triangles。**

同一 ring 的附件沿原邊界順序前進；每條 B/U 原環邊恰屬一個私人 fan
或 terminal triangle，所以兩個環的整數總前進量各恰為五。

## 6. 完備 word/strip 參數與 literal 原邊恢復

從 pentagon strip 的起始 cross edge 開始，以同一平面方向記當前 pins
為 (b_j,u_k)。索引取 mod5，但前進量在整數上累加，完整序列必總計(5,5)。
包括 a 個 terminal triangles 與其他 path strips 的所有 cyclic 後續次序。

**Terminal triangle。** B 型前進(1,0)，原面為
`(b_j,b_(j+1),u_k)`；U 型前進(0,1)，原面為
`(b_j,u_(k+1),u_k)`。起訖 cross edges 都保留。

**Path strip。** 私人原 path 為 z0,…,z_(n−1)，n≥2。每個 z 接當前
b_j、u_k；可再各接下一 pin，以 δB、δU∈{0,1}記錄。處理 z 後更新
(j,k)←(j+δB,k+δU)。每條 zz_next 的兩個原面 third vertices 是
更新後的 b_j、u_k。端點強制(δB,δU)=(1,1)，內點排除(0,0)。
起點和終點各與起訖 cross edge 構成唯一 M 面。

**Pentagon strip。** 以 backbone z0,…,z_(s−1)，s≥2，保留兩條原 tails，
選 gap g∈{0,…,s−2}，令 x=z_g、y=z_(g+1)。gap 本身不是原邊。
在原 backbone path 中不加入 xy，加入新私人點 q0,q1,q2 及七條原邊

`xq0, yq0, xq1, q1q2, q2y, q0q1, q0q2`。

PPP 原面恰是 `xq0q1`、`q0q1q2`、`q0q2y`，其一致有向版本由原
指定外面與 contour 決定。backbone 各點的附件規則如下：

| 點的位置 | 允許 (δB,δU) |
|---|---|
| endpoint 且不是 gap tip，即私人 leaf | (1,1) |
| endpoint 且是 gap tip，即沒有尾的 ear | (1,0),(0,1),(1,1) |
| internal 且不是 gap tip | (1,0),(0,1),(1,1) |
| internal 且是 gap tip，即有尾的 ear | (0,0),(1,0),(0,1),(1,1) |

在 x 已處理之後、y 尚未處理之前插入 gap。若為 B 型，取 δ∈{0,1}：

* q0 接 b_j，且 δ=1 時另接 b_(j+1)。
* q1 接 u_k、u_(k+1)；q2 接 u_(k+1)、u_(k+2)。
* gap 的整數前進量是 (δ,2)。

U 型把 B/U 角色交換，前進量是(2,δ)，不改變原五邊形上的相對次序。
表格的每項直接等同完整 degree≥5：普通 internal 點為4+δB+δU；
有尾的 ear 為5+δB+δU；無尾 ear 為4+δB+δU；私人 leaf 為3+δB+δU。
q0 為5+δ，q1、q2 為5。

完整參數域是 §1 的 c,r,a；pentagon strip 有 s+3 私人點；每個額外
path strip 至少兩點；所有私人點数合計 r；全部 gaps、兩種型、δ∈{0,1}、
上表的全部 letters、全部 terminal-triangle 型及後續次序，總前進量(5,5)。
可保留重複描述，不要求同構去重正確。任何違反其他尚未使用來源條件的
模板可保留在較大的必要域中，但 checker 必另驗它確為指定 annulus。

**逐類不漏邊。** 全部 A 原邊只有十條 B/U 框邊、七條 pentagon core
邊、兩個 tails 及 path components 的全部私人邊、上述私人–terminal
附件、region 分界的全部 B–U 邊。全部面由 PPP 三面、每個私人邊的
非 PPP sides、同環 fan triangles、各 region 端 M 面及 terminal
triangles 恢復。沒有隱藏邊或獨立拼接的 marginal。
checker 應從有向面另重算 darts、rotation、Euler、空 U 面、全部 degree、
三個 PPP 面、M=2c、p=a+c 及(5,5)框邊使用量。

**同一原色框。** canonical 圖搬回原來源時保留

\[
g_B(i)=s_B+\epsilon i,\qquad
g_U(i)=s_U+\epsilon i\pmod5,\qquad\epsilon\in\{1,-1\}.
\]

两圈同一方向 ε，起點可不同。若使用的 U 列採面邊界方向，先記錄該固定
換算，不能暗中單獨反 U。私人點按上述原 contour、gap、tails 與 region
次序逐點映回，中心映回 v。這是完整帶原 embedding 的同構，所以保
全部 B/U pins、中心色及每個 full lift；它本身尚不是較小代表。

## 7. 紙面採納及染色驗證界線

本檔已任意大小、任取合法 W5 地排除 K4 block、全部多 cyclic-block
配置、c=2 的(2,1)分配，並把全部未排除來源完整化為上節 pentagon-strip
有限必要域。存活域包含 c=1 與 c=2 的(3,0)，沒有把它們僅憑結構視為矛盾。

最強可重用機制是：**contractible 三角化 block 的精確面計數，加上
block-cut skeleton 的 ear/leaf 注入式 M 計帳**。它同時控制分量、附樹、
bridges、cut vertices 及 terminal switches；並給出保持原 rotation 的
完整附件參數。最終來源排除仍須對全部參數模板核對完整補中心外框 Σ，
且逐模板證 Σ∈K132，或交付保同一原 B 完整 Σ 且嚴格減點的合法代表。
若只證 Σ 相等，不可宣稱 R³ 相等或保各 U pin／中心色的代表搬運。
本檔沒有新增 Lean theorem。
