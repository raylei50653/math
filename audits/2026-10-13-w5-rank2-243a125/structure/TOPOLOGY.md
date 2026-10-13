# 圈秩二：完整 2-core 分類與環位置排除

BASE：`243a125a80e4d8de40957f59d8da0bdbc974cf69`。本檔是任意大小的紙面
證明，沒有以有限枚舉代替完備性；所有 pruning / suppression 都只作分類，
沒有聲稱這些操作保染色或是合法代表。採用的輸入已封存於
[`../frozen/`](../frozen/)，原證據不作更改。

## 1. 精確來源與唯一使用的上游前提

G 是全部目錄外 disk-C5 圖中先最小化內點數、再最大化邊數的來源。
固定任意合法全內部 induced W5，其中心 v、原有序 rim U，以及原外框 B；
B/U 十個 pins 互異，U 的有界側恰含 v 與五條 spokes。令

\[
P=V(G)\setminus(B\cup U\cup\{v\}),\quad F=G[P],\quad
r=|P|,\quad c=c(F),\quad \rho(F)=|E(F)|-r+c=2.
\]

下列前提均是既有完整來源信任鏈的結論，而非本輪新增假設：

1. G 是有限簡單二連通 plane disk 圖；B/U 是 induced C5；A=G-v 的 annular
   面皆為三角形；r=k-6≥7。
2. 每個原內點的 **完整 G-degree** 至少五。
3. 每個私人點在 B 上至多有兩個鄰點，若兩個則相鄰；每個簡單 C4 的有界
   內部沒有頂點。

與上一輪相同，第 3 項也給 U 的同樣附件界：若 x 接 U 上非相鄰兩點，
`ui-v-uj-x-ui` 是一個 C4，U 的兩條非空開弧位於它的兩側，故其有界側
含頂點，矛盾。於是

\[
d_T(x)=|N_G(x)\cap(B\cup U)|\le4,
\qquad d_G(x)=d_F(x)+d_T(x).
\]

特別地，F 無孤立點；私人 leaf 恰有兩個相鄰 B 鄰點與兩個相鄰 U 鄰點，
完整 degree 恰為五。全篇沒有假設 d_F≥5，也沒有 N2、ε、edge-critical
或 Gallai 條件。詳細上游來源見封存
[`STRUCTURE §§1–3`](../frozen/audits/2026-10-13-w5-private-unicyclic-3097ef5/structure/STRUCTURE.md)、
[`共面正規形`](../frozen/docs/c5_cofacial_normal_form.md) 及
[`全內部 W5`](../frozen/docs/c5_degree5_link_reductions.md)。

## 2. 原有限簡單圖的四型覆蓋

每個連通分量的圈秩皆非負，且各分量圈秩相加為二。因此恰有以下兩種
分配：兩個圈秩一分量，或一個圈秩二分量；其餘分量均是樹。
這一步原本包含孤立點，之後才由 §1 的完整度數排除它們。

反覆刪去 degree 零／一點取得每個有環分量的 2-core。每次刪 leaf 及其
一條邊保持該分量的圈秩；有環分量的 core 非空而且連通。core 外的
每棵樹只以一條根邊接到一個 core 頂點：若含環，或經兩條根邊接回
core，相關路徑不會被 leaf pruning 刪去。另有任意獨立樹分量。
因此這個分解保留全部原附枝、原頂點及原邊，並未把它們實際刪除。

* 圈秩一的連通 core 具有 e=n，因此
  `Σ(deg_core-2)=0`。每點 degree 至少二，故 core 是一條簡單環。
* 圈秩二的連通 core 具有 e=n+1，因此

  \[
  \sum_{x\in\mathrm{core}}(\deg_{\mathrm{core}}(x)-2)=2.
  \]

  所以非 degree-two 分支點只有兩種配置：一個 degree-four 點，或兩個
  degree-three 點；其餘點全為 degree two。

只為分類而抑制 degree-two 路徑，允許所得核含 loops／parallel edges：

* 一個 degree-four 點時，核是同一點上的兩個 loops，恢復 subdivision
  就是 **figure-eight**：兩個簡單環只共享一個點。
* 兩個 degree-three 點 s,t 時，設兩點的 loop 數為 Ls,Lt，s-t 邊數為 m。
  連通性給 m≥1，而 `2Ls+m=2Lt+m=3`。只有 `(Ls,Lt,m)=(0,0,3)` 或
  `(1,1,1)`，分別是 **theta**（三条內點互斥的 s-t 路徑）與
  **barbell/dumbbell**（兩個不相交環由一條路徑連接）。

加上第一個分量分配，全部四型正是：

| 類型 | 有環分量 | 原 2-core | 仍需保留的原圖資料 |
|---|---:|---|---|
| 分離雙單環 | 2 | 兩條不相交簡單環 | 所有根樹、獨立樹分量及 subdivisions |
| theta | 1 | 三条內點互斥 s-t 路徑 | 同上 |
| figure-eight | 1 | 兩環共一點 | 同上 |
| barbell/dumbbell | 1 | 兩環由非空路徑接合 | 同上 |

原圖簡單性不能在抑制後丟失：原 loop 的展開環長至少三；theta 的三条
原路徑中至多一条長一；barbell 的接合路徑長至少一。這證明覆蓋任意
原始大小，不靠圖形直覺，也沒有預設私人圖連通。

## 3. 用 F 的實際面完整記錄環位置

保留 F 從 G 繼承的 plane embedding，將面理解為平面補集的連通區域；
邊界可以是閉 walk、含 bridge 重複，或有多個邊界分量。Euler 給

\[
f(F)=|E(F)|-r+c+1=3.
\]

故 F 恰有兩個有界面，不論 F 是否連通、有多少樹或孤立點。
B 位於 F 的無界面；連通且與 F 不交的 U 全位於同一個 F 面。U 所在的
面也含 v，因 U 槽位內沒有私人點。每條 F 中簡單環 C 均由 Jordan 分離
精確分類：U 在 C 的有界側是 essential，否則是 contractible。

**空面引理。** 不含 U 的有界 F 面 D 必是原 G 的 PPP 三角面。
證明：D 內沒有私人頂點或私人邊，否則它們本來就是 F 的一部分；
B、U、v 均不在 D。G 的其他邊也不可能穿越 F 的邊界進入 D，或在沒有
內部 endpoint 的情況下留在 D。故 D 本身是原 G 的一個面，三角化
迫其邊界是三个互異私人點及其三條原邊。尤其帶樹枝 slit、bridge
重複或多邊界分量的空區域不能冒充三角面。

反過來，每個原 PPP 三角面就是一個不含 U 的有界 F 面。因此若 h 記
原 PPP 三角面數，則精確地

\[
\boxed{h=2\quad\hbox{若所有私人環 contractible};\qquad
h=1\quad\hbox{若存在 essential 私人環}.}
\tag{T1}
\]

這裡也使用標準 plane graph 事實：有界面的任一點被某個 boundary
簡單環包圍；可從包含該面的閉 boundary walk 去掉回溯並分解成簡單環
得到。因此「U 在 F 的有界面」當且僅當存在 essential cycle。

這個面表示保留所有相對位置，而不是只看抽象 core：

* 分離雙環／barbell 的兩個 Jordan 環，其有界盤或互不相交，或一個
  包含另一個。U 在每個合法補集面的位置都須分別考慮。若 U 在兩個
  nested 環的內側，兩環之間的區域不含 terminal；分離型該面有兩個
  boundary components，barbell 型另有接合路徑的雙重邊界，均違空面引理。
  若 U 在兩環之間，則外環 essential、內環 contractible；並未預先排除此位置。
* figure-eight 的兩個 Jordan 盤可在共同點外互不相交，或在共同點相切
  且一盤在另一盤內。後一情形中夾層面 boundary walk 重經共同點；
  此面只有在含 U 時才不被空面引理立即排除。
* theta 的三条路徑按原 rotation 列為三個相鄰 pair；其中兩個 pair
  界定有界面，另一個是外圍環。U 若在無界面，三環皆 contractible；
  若在一個有界面，該面的環與外圍環 essential，另一個有界面環
  contractible。這明確允許兩個 essential cycles 共享一整條路徑。

樹枝與其他分量的實際位置仍沿原面保留；若它們造成不含 U 的有界面
有 slit 或額外 boundary component，就由空面引理排除，並非自行刪枝。
所以 (T1) 適用所有相對位置，沒有假定所有環繞 U。

## 4. 新面數及完整度數式

令 p 為 B-U 原邊數，a 為全 terminal 的 annular 三角面數，M 為恰含
一個 B、一個 U、一個私人點的三角面數。以下全部從原面重算：

\[
e(A)=3r+20,\qquad t(A)=2r+10,\qquad e(F)=r-c+2.
\]

恰有兩個私人點的面數是 `2e(F)-3h`。十條 B/U 環邊各在 annulus 側
有一面，其中 a 個是全 terminal 面，另 `10-a` 個有一私人點。
因此

\[
2r+10=h+(2e(F)-3h)+(10-a)+a+M,
\]

而每條 B-U 邊兩側的計數給 `2p=2a+M`。於是

\[
\boxed{M=2(c-2+h),\qquad p=a+c-2+h.}\tag{T2}
\]

terminal-P 原邊數是 `2r+8+c-p`，故

\[
\sum_{x\in P}d_G(x)=4r+12-c-p,\qquad
\boxed{r\le12-c-p=14-2c-a-h.}\tag{T3}
\]

即使尚未分類 core，已有 r≤11 的普遍必要上界；無 essential 時
進一步是 r≤10。這些常數不是把單環／森林式機械替换所得。

## 5. 原 rotation 的 M 面見證

**Leaf 見證。** 若 x 是 F 的 leaf，§1 給它兩個 B 鄰點及兩個 U 鄰點。
在 x 的原 cyclic link 中去掉唯一私人鄰點後，四個 terminal 形成一條
連續路徑，必有相鄰的 B-U pair。原內面三角化使它與 x 構成 M 面。
不同 leaf 給不同 M 面，因每個 M 面只有一個私人點。

**Facial degree-two 見證。** 若 x 的兩條私人 incident edges 在原
PPP 三角面相鄰，且 d_F(x)=2，完整 degree≥5 迫至少三個 terminal
鄰點，B/U 皆出現。PPP 面占去兩條私人邊之間的一個空 sector，所有
terminals 在另一個連續 link 路徑內；故同樣給一個 M 面。

**Root-or-leaf 見證。** 若 x 在 2-core 中 degree two 且 incident
某原 PPP 三角面，則無 off-core 附枝時用上一段；有附枝時，選其一
原根樹的非 core leaf，用 leaf 見證。不同 core roots 的根樹不相交，
因此不同 roots 的見證不同。每個獨立非平凡樹分量另至少有兩個 leaves，
給兩份不同 M 見證。這只是原圖中的計帳，沒有刪去或替換任何原邊。

## 6. 所有 essential 位置均排除

假設存在 essential 私人 cycle。Jordan 分隔先給 p=0；(T1) 給 h=1。
代入 (T2)，得到

\[
0=a+c-1,\qquad c=1,\quad a=0,\quad M=0.
\]

兩個分離单環型因 c≥2 已排除。任何私人附枝含 leaf，與 M=0 矛盾；
因此 F 恰等於連通 rank-two 2-core。依 §2，整個 F 中至多兩個頂點
的 degree 超過二。唯一 PPP 三角面有三个互異頂點，其中至少一個
x 具有 d_F(x)=2；§5 的 facial degree-two 見證卻給 M≥1，矛盾。

**結論 T-E：四型中所有含 essential cycle 的位置全部不可能。**
這包含共享路徑的兩個 essential theta cycles、相切／nested 的環位置，
及所有附枝、subdivisions、其他私人分量。證明不使用有限染色核心。

## 7. 無 essential 時的三型排除與唯一核心

現在 h=2，故 (T2) 為 `M=2c`、`p=a+c`。兩個有界 F 面皆是原 PPP
三角面；特別地不容許不含 U 的 nested 空夾層或內側樹枝。

* **分離雙單環。** 兩個 core 環各是 facial C3，合計六個 core
  degree-two roots。§5 至少給六份 M 見證；另外 c-2 個樹分量各給兩份。
  因而 `M≥6+2(c-2)=2c+2`，矛盾。
* **Figure-eight。** 兩個 bounded faces 迫兩個環各為 facial C3，
  共點之外有四個 core degree-two roots。因此
  `M≥4+2(c-1)=2c+2`，矛盾。
* **Barbell/dumbbell。** 兩個環各為 facial C3，每環避開接合路徑
  endpoint 的兩點共給四個 core degree-two roots；任意長的原接合
  路徑不改此計數。因此同樣 `M≥4+2(c-1)=2c+2`，矛盾。
* **Theta。** 按原 rotation 記三条 s-t 路徑中共界兩個有界面的
  路徑長為 l0，其餘為 l1,l2。兩個三角面精確迫
  `l0+l1=l0+l2=3`。三者皆正，所以只可能 `(l0,l1,l2)=(1,2,2)`
  或 `(2,1,1)`；後者含兩條不同 s-t 原邊，違原圖簡單性。
  故 core **必為 diamond K4-e**：兩個三角面共享一條原邊。

**結論 T-N：無 essential 分支的四型中，前三型普遍排除；theta
只能留下 contractible diamond core，帶尚未在本檔排除的原附樹與
獨立樹分量。** 其必要上界為 `7≤r≤12-2c-a≤10`。diamond 的兩個
core degree-two roots 加其他樹分量只給 `M≥2+2(c-1)=2c`，此處
沒有嚴格矛盾，不能重用前三型的超額論證。

## 8. 本檔採納界線

本檔完成四型的任意大小覆蓋、全部相對環位置的面表示、所有 essential
位置排除，以及無 essential 時分離雙單環／figure-eight／barbell 的
排除。留下唯一 contractible diamond theta 核；其進一步原附件義務
由本包其他結構文件處理。

本檔沒有建立 annulus 代表、沒有聲稱保存 Σ 或 R³，也沒有把 r≤10
的有限必要域直接當成來源不存在。單憑本檔仍只能維持既有 ρ(F)≥2，
不能採納 ρ(F)≥3。真正最小 933／941 來源的實例控制是 `not triggered`；
以上排除來自明列完整來源前提的紙面推論，並不來自零觸發控制。
