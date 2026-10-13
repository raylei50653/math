# W5-RANK2：任意大小原面、度數與原旋轉化約

BASE：`243a125a80e4d8de40957f59d8da0bdbc974cf69`。
本檔的量詞是完整最小目錄外來源；紙面化約先於有限核心。
來源輸入的逐檔 hash 見 [BASE.json](../BASE.json)，上游只讀副本在 `../frozen/`。

## 1. 精確來源與繼承前提

固定全部目錄外 disk-C5 圖中先最小化內點數、再最大化邊數的 G。
取任意合法全內部 induced W5，中心 v、原循環鄰點
U=(u0,…,u4)，原外框 B=(b0,…,b4)，十 pins 互異。
令 A=G−v，P=V(G)\\(B∪U∪{v})，r=|P|=k−6，F=G[P]。
反設 ρ(F)=2；c 計全部私人分量，起初包括孤立點。

只沿用凍結上游已證的完整來源條件：A 是有限簡單 plane annulus，B/U induced
C5，U 是指定空內面，其他 annular 面全部三角化；k≥13，故 r≥7；原內點的
**完整 G-degree≥5**；每個私人點在 B 上至多兩鄰點且兩點必相鄰；每個簡單
C4 的有界內部無頂點。後一條以 `ui−v−uj−x−ui` 給出同樣的 U 附件界。
所以

\[
d_T(x)=|N_G(x)\cap(B\cup U)|\le4,\qquad d_G(x)=d_F(x)+d_T(x).
\]

F 因而無孤立點。私人 leaf 必恰接兩個相鄰 B pins 與兩個相鄰 U pins，完整
degree 恰五。沒有假設 d_F≥5、F 連通、N2、ε=2、edge-critical 或 Gallai。
未重播的外部 K≤12 計數定理信任邊界與上游相同。

## 2. 不依賴圈位置的面與度數恆等式

令 p=#(B–U 邊)，a=#(全 terminal annular 三角面)，
h=#(PPP 三角面)，M=#(BUP 三角面)。所有 a 面都是 BBU 或 BUU。
由 annulus Euler 及面長總和，

\[
e(A)=3r+20,\quad t(A)=2r+10,\quad e(F)=r-c+2.                 \tag{1}
\]

恰有兩個私人頂點的面數為 2e(F)−3h；恰有一個私人頂點與同環兩 pins 的面數
為 10−a。把 h、2e(F)−3h、10−a、a、M 相加，得到

\[
\boxed{M=2(c-2+h)},\qquad
\boxed{p=a+c-2+h}.                                         \tag{2}
\]

第二式來自逐邊計 B–U 兩側：2p=2a+M。
terminal–P 邊數等於 2r+8+c−p，因此

\[
\boxed{\sum_{x\in P}d_G(x)=4r+12-c-p},\qquad
\boxed{r\le12-c-p=14-2c-a-h\le11}.                          \tag{3}
\]

最後的 ≤11 使用 c≥1、p≥0。這是對任意大小及所有分量先行證明的普遍有限
上界；沒有把圈秩一的常數代入，也沒有套用森林 h=0。

## 3. F 的面與環位置

平面 F 的面數為 1+ρ(F)=3，故恰有兩個 bounded faces，無論 F 是否連通。
B 在 unbounded face；連通且與 F 不交的 U 與 v 同在一個 F face。

**無 terminal 的 bounded F face 必是原 PPP 三角面。** 把 F 看作包含其全部
原點、原邊的 plane 子圖。F face 的開區域中沒有私人點或私人邊。若該 face
不含 U/v，它亦無 B/U/v。G 的任何其餘邊都有 terminal/v 端點，不可能進入
這個區域而不穿過 F。因此該區域本身是 G 的一個面；G 的二連通及原內面
三角化迫其邊界是三角形。這同時排除無 terminal 的多邊界環帶面，以及在該
面內另藏私人分量或附枝的說法：那些點邊本來就屬於 F。

因此只有以下兩個完整位置分支：

* **E：U 在 bounded F face。** 至少一個私人簡單環分隔 B/U，另個 bounded
  face 是 PPP 三角面，所以 h=1，且 Jordan 分隔迫 p=0。
* **N：U 在 unbounded F face。** 兩個 bounded faces 都是 PPP 三角面，所以
  h=2。所有私人簡單環均 contractible；這不是預設，而是 F face 的結論。

有 private essential cycle 當且僅當屬 E。這一分割涵蓋不同分量的嵌套、
theta 三條路所定各環、以及共享點/橋接兩環的相對位置。

## 4. M 面計帳與 essential 的完整排除

記兩個局部計帳事實。

1. 私人 leaf 的原 rotation 去掉唯一私人鄰點後，剩四 terminal 鄰點成 link
   路徑，其中同時有 B/U，故至少一個相鄰 B/U pair 給 M 面。
2. 若一個 PPP 三角面的頂點 x 有 d_F(x)=2，兩私人邊在三角面側相鄰；所有
   terminal 鄰點在另一個 link 區間。d_G≥5 迫至少三 terminal，因此 B/U
   都出現，同樣至少供應一個 M 面。

不同私人點計到的 M 面不同，因每個 M 面只有一個私人點。

在 E 分支，(2) 給 0=p=a+c−1，故 a=0、c=1、M=0。事實 1 排除私人
leaves，故 F 等於其 2-core，所有私人 degree≥2。
又

\[
\sum_{x\in P}(d_F(x)-2)=2e(F)-2r=2.
\]

唯一 PPP 三角面的三個頂點不可能都私人 degree≥3；至少一個是 degree 二。
事實 2 迫 M≥1，矛盾。**故所有 essential 位置、所有四大核心類型在 E 分支
都已任意大小排除。** 這裡沒有用有限染色、代表或非 clique separator 黏合。

## 5. 無 essential 時只剩 diamond 與兩端路徑

在 N 分支 h=2，(2)–(3) 化為

\[
M=2c,\qquad p=a+c,\qquad 7\le r\le12-2c-a.                 \tag{4}
\]

先在原有限簡單圖上取 2-core，再壓低 degree 二路徑。圈秩分配只能是 1+1 或
2。連通 rank-two core 的非 degree 二 excess 總和為二：一個 degree 四分支
點給 figure-eight；兩個 degree 三分支點給 theta 或 barbell。壓縮後的 loop
只代表原簡單環，平行邊只代表內部互不相交的原路徑；不得把原圖變成多重圖
來源。每個被剝除的非平凡樹接到 core 的恰一根，其他分量是樹。

兩 bounded faces 都是空三角面，故：

| 原 core 類型 | N 分支的原 core | 一定供應 M 的不同根/葉數 |
| --- | --- | ---: |
| 兩個單環分量 | 兩個不嵌套的三角形 | 6 |
| figure-eight | 共享一點的兩三角形 | 4 |
| barbell | 兩三角形以任意非空路徑相接 | 4 |
| theta | 兩三角形共享一條邊，即 diamond | 2 |

表中的「根/葉」有精確意義：對列入計帳的 core degree 二頂點，若沒有附樹，
用 §4 事實 2；若有附樹，選該根的一個非 core leaf，用事實 1。不同根的
附樹不相交，所以沒有重複計帳。兩單環分量的每個三角頂點均列入；figure-eight
及 barbell 列入不接另一環/橋的四個頂點；diamond 列入兩 tips。
每個額外樹分量另有至少兩 leaves。

因此前面三類分別給 M≥6+2(c−2)=2c+2，或 M≥4+2(c−1)=2c+2，違反 (4)。
theta 的兩 bounded 面共享一條 branch-to-branch 路徑；若三條路長是 l1,l2,l3，
兩個面三角迫 l1+l2=l2+l3=3。若 l2=2，另外兩條均長一，違反原簡單圖；
所以 l2=1，l1=l3=2，確為 diamond，未漏 subdivisions。

寫 diamond branch vertices 為 qB,qU，tips 為 x,y，全部 core 邊恰為
`xqB,xqU,yqB,yqU,qBqU`。目前下標只是方便；§6 才證明其附件分側。
兩個 tip 各供應至少一 M，其餘 c−1 樹分量各至少二，已用盡 M=2c。
因此每項都必取等號：

* qB/qU 不得有任何附樹，否則額外 leaf 供應超額 M。
* 每個 tip 的附樹至多一棵，且只能是單一路徑；否則至少兩 leaves。
* 每個其他樹分量恰有兩 leaves，因此是非平凡路徑。
* 每個 tip 或其路徑末端恰供應一個 M；其他私人點完全沒有 M。

所以 F 完整地由一個「diamond＋兩端可空路徑」分量與 c−1 個非平凡路徑
分量組成。沒有刪掉任何原樹邊。由 (4) 及 r≥7，必 c=1 或 c=2：

\[
\begin{array}{c|c|c}
c&r&a\\\hline
1&7\le r\le10&0\le a\le10-r\\
2&7\le r\le8&0\le a\le8-r.
\end{array}                                                \tag{5}
\]

diamond 的外 C4 內只有原 diagonal qBqU，沒有頂點；上游「C4 內無頂點」
不排除這個合法情形。此處不能聲稱 occupied-C4 矛盾。

## 6. 原 rotation 迫兩側附件與 strip

逐一沿私人分量的外 facial contour 走一周，bridges 按兩側各走一次。
在兩個相鄰私人 darts 之間，terminal 鄰點形成原 link 區間。相鄰 terminal
從 B 改為 U 或 U 改為 B，恰對應一個 M 三角面；沒有 M 的區間只能含單一
terminal 類型。私人邊的非 PPP 側亦由其原三角面標記 B 或 U。

每個分量恰有兩次 B/U 切換，且在其兩個指定末端；故 contour 的兩段分別
全標 B、全標 U。具體說，從一個末端到另一個末端，外 contour 的兩個方向
各先沿一端附路的一側到 tip，再沿 diamond 外 C4 的一側到另一 tip，再沿
另一端附路的一側到另一末端；每條 bridge 正反兩次出現，兩條 contour 弧
恰分別經過一個 branch vertex。所以 diamond 兩 branch vertices 位於這兩段
的不同段，這不是由抽象 support 或圖形直覺指定兩側。因此
它們一個只接 B、另一個只接 U，現在依此命名 qB、qU。各自 d_F=3，完整
degree≥5 與附件界迫恰接該環的兩個相鄰 pins，完整 degree 恰五。
兩條尖端路徑的每條私人邊，其兩原面 third vertices 分別是 B、U。
其他路徑分量同樣成立。這是同一原 rotation 的結论，不能把兩側分別反向。

每條 B–U 邊是 annulus crosscut。p=a+c≥1；先沿其中一條切開 annulus，再
把其餘互不穿越的 cross edges 依原順序切開，得到循序相接的 regions。
允許相鄰 cross edges 共端點，也允許 p=1 時同一原邊作切開盤的兩側。
每個 region 的其餘邊界是 B/U 的前進子弧，內部無 B–U 邊。

若 region 有私人分量，其兩 bounding cross-edge sides 合計至多提供兩個
M 面；每個私人分量已必供應兩個，故 region 恰有一個私人分量。若無私人
點，原三角化且無內部 cross edge 迫 region 恰為一個 BBU 或 BUU 三角面。
反之私人分量不能跨 cross edge，所以沒有分量遺失。
因此 cyclic region sequence **恰為一個 diamond strip、c−1 個 path strips
及 a 個 terminal triangles**。每個 strip 的全部原附件在兩側按 pins 原順序
前進，每環邊恰由一個 fan/triangle 使用一次，總前進量各為五。

## 7. 完備有限參數域與原邊重建

可從 diamond strip 的起始 cross edge 開始，以共同平面方向設定當前 pins
(b_j,u_k)，初值 (j,k)=(0,0)。所有 index mod 5，但使用邊界邊的計數保留
整數前進量；全序列精確要求總前進量 (5,5)。其餘 regions 的全部次序均枚舉。

**terminal triangle。** B 型前進 (1,0)，原邊界面是 `(b_j,b_(j+1),u_k)`；
U 型前進 (0,1)，面是 `(b_j,u_(k+1),u_k)`。包含起訖 cross edges。

**path strip。** 私人 path 為 z0,…,z_(n−1)，n≥2。
每點配置 (δB,δU)∈{0,1}²；兩 endpoints 強制 (1,1)，其他點排除 (0,0)。
點 z 在 B 接當前 b_j，δB=1 時另接 b_(j+1)；U 同理。
每點後更新 j,k。每條 zz_next 的兩側第三點是更新後的 b_j,u_k。
起點/終點各與起始/最後 cross edge 成一個 M 面。

**diamond strip。** 設 backbone z0,…,z_(s−1)，s≥2，選 gap
g∈{0,…,s−2}。保留 path 邊但刪掉 z_g z_(g+1)，加入 qB,qU 與五條 core 邊
`z_g qB,z_g qU,z_(g+1) qB,z_(g+1) qU,qB qU`。
這個分量有 s+2 私人點。backbone 點的附件仍由 (δB,δU) 決定，允許域如下：

| 點的位置 | 允許 (δB,δU) |
| --- | --- |
| endpoint 且不是 gap tip（私人 leaf） | (1,1) |
| endpoint 且是 gap tip | (1,0),(0,1),(1,1) |
| internal 且不是 gap tip | (1,0),(0,1),(1,1) |
| internal 且是 gap tip | (0,0),(1,0),(0,1),(1,1) |

走過 gap 時，另增加 B/U 各一次前進。若當時 pins 是 (b_j,u_k)，則
qB 接 b_j,b_(j+1)，qU 接 u_k,u_(k+1)，更新 (j,k)←(j+1,k+1)。
此四 terminal 邊、五 core 邊與 incident faces 都必保留；尤其不能漏中間
原邊 qBqU。gap 兩側的三角面及兩 PPP 面唯一由這個順序決定。
普通 path 邊與兩端 M 面照前述方式重建。

各允許域直接等同完整 degree≥5：普通 internal path 點 degree=4+δB+δU；
有尾的 tip degree=5+δB+δU；無尾 tip degree=4+δB+δU；leaf degree=3+δB+δU。
qB/qU degree=5。所有 terminal 附件都是從原面推導，沒有更換 source 身份。

完整枚舉域為 (5) 的 c,r,a；一個 diamond 分量及 c−1 個 n≥2 paths 的私人
點數總和 r；diamond gap 的全部位置；上述 letters 的全部選擇；a 個 terminal
triangles 的全部 B/U 類型；diamond 後其他 regions 的全部排列；總前進量(5,5)。
可保留重複描述，不需假設同構去重正確。若某必要模板違反尚未使用的來源
条件，仍可保留在較大必要域中排除；但有限 checker 必核對每份实际 plane
annulus，而不能只以抽象平面性代替指定外面、U 空面與原 rotation。

**原邊不漏的核對。** 原圖中的邊只可能是十條框邊、私人 core/path 邊、
私人–terminal 附件、B–U cross edges。前述參數逐類全數恢復；原三角面也逐一
恢復。checker 應另從定向面重算 dart、rotation、Euler，驗證 e(A)=3r+20、
t(A)=2r+10、h=2、M=2c、p=a+c 及全部 pin 次序。

**搬回原 pins。** 對一份原來源，先在其原 rotation 中選 diamond 起始側及
方向，保留 canonical-to-original maps

\[
g_B(i)=s_B+\epsilon i,\quad g_U(i)=s_U+\epsilon i\pmod5,
\qquad \epsilon\in\{1,-1\}.
\]

兩環使用同一方向 ε；各自起點可以不同。若使用者的 U 序是 boundary-face
方向而 B 是共向座標，先記錄此固定換算，不能暗中單獨翻 U。
私人點依實際 backbone/gap/path 次序映回，中心映回 v。
所得是完整帶嵌入圖同構，逐点搬運每份 full lift，保十 pins 及中心色；它
**不是縮減代表**。只有另證 Σ 相等且 r′<r 的合法圖才能使用最小性。

## 8. 紙面結論與計算界線

不經有限搜尋已完成：全部 essential 位置排除；無 essential 時兩個分離單環、
figure-eight、barbell 排除；theta 完整化為 (5)–§7 的有限 diamond-strip 域。
普遍性來自原面與原 rotation 的覆蓋證明，不來自任意截斷搜尋。

主 generator 的完整參數域有 974 個帶描述模板；主重算得到 970 個 Σ=1023、
2 個 Σ=639、1 個 Σ=1021、1 個 Σ=959。它們**並非全部全收十列**。
逐 cell/full-lift 的獨立重算，見父 REPORT 及其驗證檔。四種 mask 都有合法
同槽位代表，实际原邊、定向面、rotation、pin map 及完整 fibres 另見
[REPRESENTATIVE.md](REPRESENTATIVE.md)：

| Σ | 來源模板數 | 代表 | r′ |
| ---: | ---: | --- | ---: |
| 1023 | 970 | 五條對應跨環邊的 prism | 0 |
| 639 | 2 | diamond word `BU`、gap 0、後接 `BBBUUU` | 4 |
| 959 | 1 | diamond word `BD`、gap 0、後接 `BUUBU` | 4 |
| 1021 | 1 | diamond word `UU`、gap 0、後接 `BBUBBU` | 4 |

表中字母 B/U 的步長為 (1,0)/(0,1)，D=(1,1)；後接文字是 terminal triangles，
非附加私人點。每份代表保留十原 pins 與指定空 U 面，再補原中心槽位。
藉 §7 共同 pin map 搬回原外框，完整 Σ 不變，且

\[
k′=6+r′\le10<13\le6+r=k.
\]

這直接違反全域最小內點性，**無須另查四種 mask 的目錄 membership**。
故在主/獨立完整驗證支持下，theta 最後有限域也全部排除，接 §§4–5 得
ρ(F)≠2；再接凍結上游 ρ(F)≥2，採納任意合法全內部 W5 的
**ρ(G[P])≥3**。其中任意大小覆蓋屬紙面證明，974 模板及四代表的染色
關係屬有限完整核對，兩層證據沒有互代。

這些縮減只保 `pr_B R_A³`；不宣稱 `R_A³` 相等，不保 U 的個別染色支援
或中心色，更不保 fibre 重數。全 source-to-template 同構仍保十 pins 與
全部 lifts，與 template-to-representative 的弱保存目標分開。

真正最小 933／941 來源是 **not triggered**。本紙面化約不宣稱構造這種來源，
也不從零 triggers 推出排除。沒有新增 Lean theorem 或改動封存證據。
