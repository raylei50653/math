# W5 私人圈秩三：essential 分支的完整排除

BASE：`45bc1c3dc9dacaee1b10df9d64f1c6a27bb0e954`。
本檔先把任意大小原來源化為完整有限域，然後才使用染色核心。
凍結輸入及 hashes 見 `../BASE.json`；原證據不作改動。

## 1. 量詞、原圖與繼承前提

固定在**所有**目錄外 disk-C5 圖中先最小化內點數、再最大化邊數的 G。
取任意合法全內部 induced W5，原中心 v、原循環鄰點 U=(u0,…,u4)，
原外框 B=(b0,…,b4)。十 pins 互異；U 有界側恰由 v 及五個三角面填滿。
記 A=G−v，P=V(G)\(B∪U∪{v})，F=G[P]，r=|P|，c=c(F)，q=ρ(F)。
本輪只反設 q=3 且 F 有一個 essential cycle，即分隔 B 與 U 的私人簡單環。

沿用凍結來源鏈的結論：A 是有限簡單 plane annulus，B/U 是 induced C5，
指定 U 空面以外全部 annular 面三角化；r=k−6≥7；每個私人點的**完整
G-degree≥5**；每個私人點在 B 上至多有兩個鄰點，兩個時必相鄰。
原圖每個簡單 C4 的有界內部無頂點。由 ui−v−uj−x−ui，後一條也排除
私人點 x 在 U 上的非相鄰雙附件，所以在 U 上同樣至多兩個相鄰鄰點。
故 d_T(x)=|N_G(x)∩(B∪U)|≤4，d_G(x)=d_F(x)+d_T(x)。
F 無孤立點；私人 leaf 必恰接 B/U 各兩個相鄰 pins。

沒有加入 F 連通、私人 degree≥5、edge-critical、N2、ε 或 Gallai 假設。
上游 K≤12=K≤5、四色定理及外部計數信任邊界不變。

## 2. 任意圈秩的原面恆等式

令 p 是 B–U 原邊數，a 是全 terminal annular 三角面數，h 是 PPP 三角面數，
M 是各含一個 B、U、私人點的三角面數。由 annulus Euler，

\[
e(A)=3r+20,\qquad t(A)=2r+10,\qquad e(F)=r-c+q.
\]

恰含兩個私人點的面數是 2e(F)−3h。十條 B/U 環邊的 annular incident 面
中，a 個全 terminal，另外 10−a 個恰有一私人點。逐類計全部三角面得

\[
2r+10=h+(2e(F)-3h)+(10-a)+a+M,
\quad M=2(c-q+h).
\]

全 terminal 三角面恰為 BBU 或 BUU，每份有兩條 B–U 邊；逐 B–U 邊
計兩側原面得 2p=2a+M。因此

\[
p=a+c-q+h. \tag{1}
\]

terminal–P 邊數為 2r+10+c−q−p，所以

\[
\sum_{x\in P}d_G(x)=4r+10+q-c-p,
\qquad r\le10+q-c-p. \tag{2}
\]

以上是一般 q 的重新推導；沒有把 rank-two 常數直接移用。

## 3. Essential 位置迫 c=1、M=0、F 無葉

平面 F 恰有 q 個有界面。B 在無界面，連通且與 F 不交的 U/v 在同一面。
一個不含 U/v 的有界 F 面沒有其他 G 頂點：私人點已全包括在 F，B 在
無界面。其他原邊也不能越過 F 邊界進入該面。因此它本身必是原 PPP
三角面；這同時排除 slit、重經 bridge 及多邊界分量的空面。

Essential 假設等價於 U/v 落在一個有界 F 面，故 h=q−1；Jordan 分隔
又給 p=0。代入 (1) 得 0=a+c−1，因 c≥1，所以

\[
c=1,\quad a=0,\quad p=0,\quad M=0,\quad h=q-1. \tag{3}
\]

若私人 leaf x 存在，其四個 terminal 鄰點在原 rotation 中、移去唯一
私人鄰點後形成一條 link 路徑。此路徑同時含 B/U，必有一次相鄰 B/U
切換，與 x 形成 M 面，矛盾。因此 d_F≥2。

同理，若 PPP 三角面頂點 x 的 d_F(x)=2，該三角面占去两私人邊間的一個
sector；所有 terminal 位於另一個連續 link 區間。完整 degree≥5 迫至少
三個 terminal，由每環最多兩個可知 B/U 都出現，因此也迫 M 面。
所以**每個 PPP 三角面頂點都具有私人 degree≥3**。

## 4. q=3 唯一私人圖：diamond 的兩 tips 外接一條路徑

現在 q=3，(3) 給 F 連通、有恰兩個 PPP 三角面、私人最小 degree≥2。
又 e(F)=r+2，故

\[
\sum_{x\in P}(d_F(x)-2)=4. \tag{4}
\]

兩個不同 bounded triangular faces 的頂點聯集至少有四點。若兩面有同一
三點邊界且位於三角形兩側，連通的 F 只能是該三角形，違 q=3。
由上一節，這些點每個在 (4) 至少貢獻一；因此聯集恰四點、每点私人
degree 恰三，其他私人點 degree 恰二。兩三角面恰共享一條原邊。

記共享邊為 qBqU，另兩點為 x,y。兩面及全部 diamond 原邊為

`xqB, xqU, yqB, yqU, qBqU`。

此時 qB/qU 已各有三條私人邊，不能再接私人邊；x/y 在 diamond 中
各 degree 二，各還須恰接一條私人邊。其餘私人點 degree 二，且 F 連通，
因此 diamond 以外的私人邊恰構成一條覆蓋全部其他私人點的簡單 x–y 路徑 Q。
不能另有 disjoint cycle，也不能有附樹、其他分量、分支或遺漏的 subdivision。
此處只是辨認原圖，沒有刪去、識別或替換原邊。

兩 PPP 面共享邊的聯集是填滿的 diamond disk；Q 在其外側。F 的另外
兩個面分別是無界面及含 U 的有界面。qB、qU 的標記依此確定：qB incident
無界面，qU incident 含 U 面。兩面邊界分別是 Q 加 xqBy、Q 加 xqUy。
所以兩個 branch 頂點的唯一 terminal sector 分別只含 B、只含 U。
完整 degree≥5 及附件界迫 qB 恰接兩個相鄰 B pins，qU 恰接兩個相鄰 U pins；
兩點完整 degree 都恰五。

由 (2)，r≤10+3−1=12。上游 r≥7，故

\[
7\le r\le12,\qquad |E(Q)|=r-3\in\{4,5,6,7,8,9\}. \tag{5}
\]

另一個檢查是 essential face 的 boundary cycle 長 r−1，環內含 U∪{v}
六點；上游 C4/C5 小環限制也迫 r−1≥6。所有任意長路徑已由 (5) 有界化。

## 5. 原 rotation 與所有附件的 word 表示

只為記錄，把 Q 與「x–y diamond gap」排成一個 cyclic backbone
z0=x,z1=y,z2,…,z_(s−1)，s=r−2；gap 是 z0 到 z1。
這個 gap 並不是原邊，不得把 xy 加入原來源。其他 backbone 邊全是 Q 的原邊。

每條 Q 邊的兩個原面 third vertices 分別來自 B/U。對普通 backbone 點，
其兩條私人邊的兩個 sectors 分別只含 B/U terminal；對 x/y，另有一個 PPP
sector，其他兩個 sectors 仍分別只含 B/U。因此每個 backbone 點在兩環
各至少有一個鄰點，至多兩個相鄰鄰點。沿原 contour 前進時，用

\[
O=(0,0),\quad B=(1,0),\quad U=(0,1),\quad D=(1,1)
\]

記此點在兩環消耗的環邊數：delta=0 表示接當前一個 pin；delta=1 表示
另接下一個 pin，兩者的原三角面填滿該 sector。
普通點的私人 degree 是二，故完整 degree=4+deltaB+deltaU≥5，letters
恰可為 B/U/D；兩 tips 的私人 degree 是三，故完整 degree=5+deltaB+deltaU，
letters 恰可為 O/B/U/D。

走過 gap 時，qB 的 B 附件消耗一條 B 環邊，qU 的 U 附件消耗一條 U 環邊，
故另加 (1,1)。因 p=a=0，各 B/U 環邊的唯一 annular incident face 都是
其 terminal–private fan 中的一面。按原面順序繞行必各恰用完五條原環邊，
不能提前閉合、重複使用或獨立翻向。因此完整參數域為

\[
s=5,\ldots,10;\quad w_0,w_1\in\{O,B,U,D\};\quad
w_i\in\{B,U,D\}\ (i\ge2);\quad
\sum_i\delta_B(w_i)=\sum_i\delta_U(w_i)=4. \tag{6}
\]

原邊分四類：十條 B/U 環邊、Q 邊、五條 diamond 邊、私人–terminal
附件。(6) 逐類恢復全部原邊。G 再加原中心及五條 spokes；沒有 B–U 邊，
沒有其餘原邊。checker 以有向原三角面重算 darts、rotation、Euler、私人
degree、完整 degree、全部 pin 順序及原 U 空面，不能只靠抽象平面性。

**固定原 pins。** 對原來源選 x 為起 tip、按上述 cyclic contour 選共同
方向，並記錄 canonical-to-original maps

\[
g_B(i)=s_B+\epsilon i,\qquad g_U(i)=s_U+\epsilon i\pmod5,
\qquad\epsilon\in\{1,-1\}.
\]

兩環使用同一 ε，各自起點可不同。如果原 U 以 boundary-face 方向書寫，
先顯式記錄它與共同座標的固定換算，不能暗中獨立反 U。私人點依原 Q、
原 x/y、原 qB/qU 映回，中心映回原 v。由此是完整帶嵌入圖同構，逐份搬運
同一 G 或 A 的 full lift；顏色仍在共同 {0,1,2,3} 中，沒有獨立正規化 U。

## 6. 有限完整染色核心及排除

(6) 在 r=7,…,12 的全部 linear words 數分別為

| r | 7 | 8 | 9 | 10 | 11 | 12 | 合計 |
|---|---:|---:|---:|---:|---:|---:|---:|
| words | 22 | 131 | 340 | 440 | 280 | 70 | 1,283 |

保留重複嵌入描述，不依賴同構去重。這是包含所有原來源的**較大必要域**：
不另強制模板的全部 B/U 度數、外圈 collar 或每一個小分隔環前提；保留此類
額外模板不影響排除，因域中每份仍是具指定 B/U 面的實際 plane annulus，
完整私人 degree≥5，且最後每份均 Sigma=1023。每個模板保存實際原邊、有向面、rotation、
pin map、每一固定外框 beta 的全部 1,024 個 U cells，包括空 fibre，以及每份
完整 A coloring。U 恰用三色的每份 A lift 唯一接中心；checker 另直接枚舉
G 的全部完整 lifts，逐列驗證兩者完全相同。此處不拼接不同 rows 的見證，
不以邊界 marginals 重建完整染色。

主程序得到全部 **1,283 份 Sigma=1023**，共 13,137,920 cells，其中
12,714,781 empty cells、730,480 A lifts、352,020 G lifts。逐 cell 的獨立
重算及反控制由本包其他紀錄承擔；這些有限數字本身不證任意大小覆蓋，覆蓋
來自 §§1–5。

原來源只可能是 933/941 的整圖 D5 像；而全收十列的 1023 在共同 pin
映回下仍全收十列。因此每個 (6) 模板及每個映回的原來源都不可能目錄外。
這排除 q=3 的**全部 essential 位置**。本輪直接由完整 Sigma=1023
與目錄外來源身份矛盾，不另構造代表，也不宣稱保 U 支援或 fibre 重數。

## 7. 可採納的新界線

接既有 q≥3，得到在完整最小來源前提下：

* 任取合法全內部 W5，如果私人圖有 essential cycle，則 q≥4。
* 若 q=3，U/v 必位於 F 的無界面；其三個 bounded F faces 全是 PPP 三角面。
  此時 M=2c、p=a+c≥1，且 r≤13−2c−a≤11。

第二項只給必要條件，不完成 contractible q=3 的來源分類或染色排除。
尤其不能採納一般 q≥4、所有 rank-three 排除、一般小 annulus 代表或
K∞=K≤5。真正最小 933/941 來源仍為 `not triggered`；普遍排除來自紙面
完備化約與完整有限核心，而不是零 triggers。沒有新增 Lean theorem。
