# W5-RANK4-C：一般面計帳、附件界及分量數

2026-10-13。固定 BASE `acd2b1beea6c909edade565a00eeeeac05d2b3a7`。
本檔重新證明所需一般恆等式及 rank-four 分量界；不將任務描述或舊 rank-three
表格視為本轮定理。原輸入及逐 byte hash 見 [BASE.json](../BASE.json)。

## 1. 來源、具名 pins 與已採納依賴

G 是全部完整外框關係不屬 K132 的 disk-C5 來源中，先最小化內點數 k、
再最大化邊數的來源。任取合法全內部 induced W5，其中心是原點 v，循環
鄰點為原具名 `U=(u0,u1,u2,u3,u4)`；原外框是 `B=(b0,b1,b2,b3,b4)`。
十 pins 互異，v 的完整鄰集恰為 U，U 的有界 disk 恰有 v 與五個原三角面。
令

\[
T=B\cup U,\qquad A=G-v,\qquad
P=V(G)\setminus(T\cup\{v\}),\qquad F=G[P],
\]
\[
r=|P|=k-6,\qquad c=c(F),\qquad \rho=|E(F)|-r+c.
\]

F 保留所有原私人點、私人邊及原嵌入，包括分量、原橋、cut vertices 與
subdivisions。下文的 degree 若寫 d_G，必指完整原 G-degree。

本輪沿用而不重新證明下列 BASE 定理鏈：

1. [共面正規形](../../../docs/c5_cofacial_normal_form.md)：G 簡單、二連通，
   B 是 induced C5，所有有界面是三角面。刪去 v 後，A 有指定 B 外面、
   U 空內面，其餘 annular 原面都是三角面。
2. [完整度數界](../../../docs/c5_saturation_degree_bound.md)：每個原內點
   d_G≥5。這包括 P 與 U，不是 d_F≥5。
3. [完整外圈限制](../../../docs/c5_neartri_boundary_collar.md) §2：
   沒有內點同時鄰接兩個不相鄰 B pins。
4. [全內部五輪／小 cap](../../../docs/c5_degree5_link_reductions.md)：
   每個簡單原 C4 的有界內部沒有頂點；合法全內部 W5 保有上述完整 disk。
5. [K13-COLLAR](../../../docs/c5_k13_collar.md)：K≤13=K≤5，故 k≥14、r≥8。
   [圈秩三兩分支排除](../../../docs/c5_w5_private_rank3_contractible.md)
   已给任取合法 W5 的 ρ≥4；本檔研究其等號分支。

這些上游來源定理接入既有四色定理、K132 目錄與外部有界計數定理；本輪沒有
重播外部論文的計算證明，也沒有增加新的外部定理。以下計帳是普通有限 plane
graph 的 Euler、原面與 degree 論證，不使用 N2、edge-critical、Gallai、私人
連通或縮減代表。固定假設為 ρ=4 且 U/v 位於 F 的無界面。

## 2. 每環附件至多二；排私人孤立點

對任意 x∈P，第 1 節第 3 項使 N_G(x)∩B 至多兩點，兩點時相鄰：C5 的
任意三點必含不相鄰的一對。

U 版可獨立由原 C4 限制推出。若 x 同時接不相鄰的 u_i、u_j，則原邊
形成簡單 C4 `x-u_i-v-u_j-x`。原 W5 disk 中從 u_i 到 u_j 的兩條 U 弧
都至少含一個其他 U 點。這個 C4 的兩條 v-spokes 在 v 的兩側各留一個
非空 U 弧扇區；x 及兩條 x-spokes 在原 U disk 外。Jordan 分離故使該
C4 的有界側包含其中一條 U 弧的至少一個原頂點，違反 C4 的有界內部
無頂點。因此 N_G(x)∩U 也至多兩點，兩點時相鄰。

v 的完整鄰集為 U，故 x 不接 v，並且

\[
d_G(x)=d_F(x)+d_T(x),\qquad
d_T(x)=|N_G(x)\cap B|+|N_G(x)\cap U|\le4.
\]

d_G(x)≥5 立即給 d_F(x)≥1。因此 **F 沒有孤立點，每個私人分量至少兩點**。
若 x 是私人 leaf，則 d_F(x)=1、d_G(x)=5、d_T(x)=4；其原附件恰為 B/U
各兩個相鄰 pins。這是原附件的結論，不刪 leaf，也不壓平原橋。

## 3. 不預設 contractible 的一般圈秩公式

以下計數在原 A 的面、邊上進行，均保留 multiplicity：一條 bridge 的兩側
分別計入。設

* t_P：三個頂點全在 P 的原三角面數；
* a：三個頂點全在 T 的 annular 原三角面數；
* p：B–U 原邊數；
* M：頂點分別在 B、U、P 的原三角面數。

令 f 為 annular 三角面總數。A 連通，頂點數 r+10；它的兩個指定非三角面
各長五。Euler 與面邊 incidence 給

\[
(r+10)-e(A)+(f+2)=2,\qquad 2e(A)=3f+10,
\]

所以 e(A)=3r+20、f=2r+10。因 e(F)=r−c+ρ，每條私人邊兩側均是 annular
原三角面；PPP 面用三次、恰含兩私人點的面用一次，因此後者面數是
`2e(F)−3t_P`。

B/U 各 induced C5，故每份全 terminal 面只能為 BBU 或 BUU，恰使用一條
原環邊；反之十條原環邊各有恰一個 annular incident 面。因此一私人點與
兩同環 pins 的原三角面恰有 `10−a` 份。按以上五種互斥面類計帳：

\[
2r+10=t_P+(2e(F)-3t_P)+(10-a)+a+M.
\]

代入 e(F) 得

\[
\boxed{M=2(c-\rho+t_P).}
\]

每條 B–U 邊的兩側各是一份原三角面。全 terminal 面含兩條 B–U 邊，
BUP 面含一條，其餘面不含，故

\[
2p=2a+M,\qquad \boxed{p=a+c-\rho+t_P.}
\]

全部 A 原邊分為十條原環邊、p 條 B–U 邊、e(F) 條私人邊及 e(T,P) 條
附件邊。因而

\[
e(T,P)=3r+20-10-p-e(F)=2r+10+c-\rho-p,
\]
\[
\boxed{\sum_{x\in P}d_G(x)=2e(F)+e(T,P)=4r+10+\rho-c-p.}
\]

上述式子允許 F 不連通、帶橋、帶 leaf 及 cut vertices，沒有套入 essential
域的 p=0、M=0 或 c=1。t_P 是 PPP 原面數，與外框 degree 超額符號無關。

## 4. Contractible 時 t_P=ρ，包括多邊界與 slit 的情況

有限 plane F 的 Euler 式給面數 `e(F)−r+c+1=ρ+1`，故有界 F 面恰有 ρ
份。B 位於 F 無界面，contractible 假設使整個連通的 U/v 也位於同一無界面。

取任一有界 F 面的開區域 D。沒有 G 頂點在 D：私人頂點全已屬 F，terminal
及 v 全在無界面。也沒有 G 邊能穿過 D；私人–私人原邊全已在 F，其餘原邊
有 terminal/v 端點，若進入 D 必穿過 F 的邊或頂點，違反原 plane embedding。
因此 D 就是原 G 的一份面，而非删點後合併出的面。它必是簡單 PPP 三角面。

這同時排除有界 F 面的多個邊界分量，與 bridge 兩側重走造成的 slit：
那些邊界形式不是原 G 的三角面。反方向，每個原 PPP 三角面內部亦沒有
F 點邊，所以它恰是 F 的有界面。二者一一對應，得到 **t_P=ρ**。

此論證沒有先假定每個分量 outerplane，沒有用「一個環對一個原面」，也沒有
把 hole 內其他私人分量忽略。F 可仍有多個分量；結論只描述其有界面。

在任意 contractible 圈秩 q 中，第 3 節因此給

\[
M=2c,\quad p=a+c,\quad
\sum_{x\in P}d_G(x)=4r+10+q-2c-a.
\]

本輪 q=4，與所有私人點完整 degree≥5 接合得

\[
5r\le4r+14-2c-a,\qquad
\boxed{8\le r\le14-2c-a.}
\]

更精確地，原私人 degree 超額恰為

\[
\sum_{x\in P}(d_G(x)-5)=14-2c-a-r\ge0.
\]

等號時所有私人點完整 degree 恰五；它不自動限制 U 的完整 degree，後續
模板仍須逐點檢查 U。a≥0，且 a≤10 是原環邊計帳的結果。

## 5. 正式排除 c≥3

r≥8 確保 F 非空，故 c≥1。若 c≥4，第 4 節給 r≤14−8=6，矛盾。
若 c=3，則 `8≤r≤8−a`，故 r=8、a=0；三個分量各至少两點，其大小
分割只有 `4+2+2` 或 `3+3+2`。簡單圖在這兩種分割中最多分別有

\[
\binom42+\binom22+\binom22=8,
\qquad
\binom32+\binom32+\binom22=7
\]

條邊。然而 ρ=4 要求 `e(F)=r−c+4=9`，兩種均矛盾。這一步甚至不需要
各分量的 planarity 或 block 分類，不是由有限生成器的零結果推論。

因此正式得到如下必要域：

| c | 私人點 r | 來源內點 k=r+6 | a 的必要範圍 | p | M |
|---|---|---|---|---|---|
| 1 | 8≤r≤12 | 14≤k≤18 | 0≤a≤12−r | a+1 | 2 |
| 2 | 8≤r≤10 | 14≤k≤16 | 0≤a≤10−r | a+2 | 4 |

c=1 的分量圈秩為 `(4)`；c=2 的非負分量圈秩只有 `(4,0)`、`(3,1)`、
`(2,2)`，包括分量交換。圈秩零分量是至少兩點的原樹。這是計帳階段的
必要清單；本檔尚未排除多 cyclic blocks，也未宣稱表內每格可實現。

## 6. 結論層級与 essential 剩餘

§§2–5 是在所列上游來源契約下的紙面定理，涵蓋任意 k、任取合法全內部
W5；不依賴本輪生成或染色結果。它只將 contractible rank-four 化為上述
有限大小域，並不完成来源排除。結構分類、原 rotation 模板與完整十列
染色各須另行證明及核對。

BASE 的 [essential 證據](../../../docs/c5_w5_private_rank3_essential.md)
正式結論是「含 essential 私人環則 ρ≥4」，不是 ρ≥5。其有限 1,283 模板
使用的是 ρ=3 的 diamond 結構，不能當作 essential rank-four 排除。因此
即使本輪 contractible rank-four 全部排除，普遍私人圈秩下界仍只能保持四；
提高為五另需完整 essential rank-four 證明。K∞=K≤5 始終保持 OPEN。

本文不作相同 Σ ⇒ 相同 R³ 的推論，不給十 pin 關係的縮減代表，也不新增
Lean theorem。所有具名 B/U pins、rotation、原面、完整 fibres 與 full lifts
的保存義務留給本輪各自明列的證書，不能由計帳式代替。
