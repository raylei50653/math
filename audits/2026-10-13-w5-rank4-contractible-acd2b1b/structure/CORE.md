# W5-RANK4-C：完整私人 block 分類及等號結構

固定來源：`main@acd2b1b`。完整 hash、凍結輸入與一般計帳見本 audit 的
`BASE.json`、`frozen/` 及 `FORMULAS.md`。本檔是原圖的紙面必要域證明；
沒有把有限生成器的輸出當作完備性論證，也沒有修改任何原邊或原面。

## 1. 精確契約與本檔使用的計帳

G 是全部目錄外 disk-C5 來源中先最小化內點數 k、再最大化邊數者。
任取合法全內部 induced W5，原中心 v，原環 U=(u0,…,u4)，原外框
B=(b0,…,b4)。十 pins 互異。令 A=G−v、P=V(G)\(B∪U∪{v})、
F=G[P]、r=|P|=k−6、c=c(F)。反設 ρ(F)=4，且 U/v 在 F 的無界面。

只使用完整來源已給的以下事實：A 為原 B/U annulus，B/U 都是 induced
C5，其他面都是原三角面；私人點完整 d_G≥5；每個私人點在 B、U 各至多
接兩個 pins，接兩個時相鄰。本輪 K≤13=K≤5 給 r≥8。一般計帳獨立給出

\[
t_P=4,\qquad M=2c,\qquad p=a+c,\qquad
\sum_{x\in P}d_G(x)=4r+14-2c-a,\qquad
8\le r\le14-2c-a.                                      \tag{1}
\]

其中 t_P 是原 PPP 三角面數、M 是原 BUP 面數、a 是全 terminal 原三角面
數、p 是原 B–U 邊數。每個私人點的 terminal degree 至多四，所以沒有私人
孤立點。c≥4 時 (1) 迫 r≤6；c=3 時迫 r=8、a=0，三個非平凡分量的大小
只能是 (4,2,2) 或 (3,3,2)，私人邊至多8或7條，但圈秩四要求
e(F)=r−c+4=9。故 c≤2，精確剩餘必要域為

| c | r | k | a |
|---:|---|---|---|
| 1 | 8≤r≤12 | 14≤k≤18 | 0≤a≤12−r |
| 2 | 8≤r≤10 | 14≤k≤16 | 0≤a≤10−r |

沒有加入 N2、edge-critical、Gallai、私人連通或縮減代表前提。

## 2. 四個 bounded faces 迫每個私人點在原無界面上

contractible 前提使 F 的四個有界面都是原 PPP 三角面，沒有 terminal、
私人點或隱藏邊在其開面內；多邊界分量與重經 bridge 的 slit 也被原三角面
排除。這個結論使用不連通 Euler 公式，並沒有先假設 F 連通。

若私人點 z 不 incident 於 F 的無界面，任何 terminal 邊都不能到達 z：
它必須從一個 bounded F 三角面的 sector 进入，而該 sector 已是空的原
三角面。故 d_G(z)=d_F(z)。z 的每個 incident sector 都是一個 bounded
F 面的 corner；每個簡單三角面在 z 至多有一個 corner。總共只有四個
bounded faces，因此 d_G(z)≤4，矛盾。

所以 **F 的每個原頂點都 incident 於其無界面**。這是原嵌入的 outerplane
結論，不是重新選擇方便的 embedding；所有 bridges、cut vertices 與原
rotation 均保留。

## 3. 所有圈秩至多四的 cyclic blocks

令 H 是原 F 的 maximal 二連通 cyclic block，h=ρ(H)。其 bounded
faces 都是原 PPP 三角面。理由如下：bounded H face 的邊界是原私人
簡單環；其內若有私人頂點，該點就不可能 incident 於 F 的無界面，違反
§2。若有不含新點的私人 chord，它與 H 屬同一二連通 block，違反 H 的
maximal 性。terminals 則全部在 F 無界面，不能在此簡單環內。故該 face
没有任何其他原點邊，恰是原 PPP 三角面。這也排除內藏分量、附樹及 slit。

設 H 有 n 點，原簡單外面長 b，嚴格內部點数 i。Euler 與面長式為

\[
e=n-1+h,\qquad 3h+b=2e,\qquad
n=h+2-i,\qquad b=h+2-2i.                                \tag{2}
\]

暫不刪去 i>0 的代數候選，式 (2) 給以下全部可能。rank4 的 i=1 項分成內點 degree
三、四兩種：degree 四時是四角錐；degree 三時是三角化四邊形的一個三角
面內再放一點。沒有其他項，因 b≥3、h≤4 迫 i≤1。

| h | i | 原 block |
|---:|---:|---|
| 1 | 0 | 三角形 |
| 2 | 0 | 三角化四邊形，即 diamond |
| 3 | 0 | 三角化五邊形，唯一 fan 型 |
| 3 | 1 | 外三角形內一點，即 K4 |
| 4 | 0 | 三角化六邊形，下述三型 |
| 4 | 1 | 四角錐；或三角化四邊形的一個原三角面內加一點 |

所有 i=1 項由 §2 排除；也可直接看到其原內點完整 degree 至多四。
因此真正來源只容許 triangulated polygon blocks。它們沒有可任意細分的
cyclic 邊：細分任何原邊都破壞 incident PPP 原三角面。不同 blocks 之間
的 bridge paths 及附樹仍可有任意原 subdivision 點。

六邊形外面依序命名 0,1,2,3,4,5。其完整三型如下；表中只列除六条原
邊界邊以外的 diagonals，ear 指在該 block 中 degree 二的原點。

| 型 | 原 diagonals | degrees (0,…,5) | ears |
|---|---|---|---|
| H-fan | 02,03,04 | 5,2,3,3,3,2 | 1,5 |
| H-zigzag | 02,03,35 | 4,2,3,4,2,3 | 1,4 |
| H-central | 02,04,24 | 4,2,4,2,4,2 | 1,3,5 |

**三型完備性的紙面證明。** 三角化六邊形有四個 PPP 面，弱對偶是四點
樹，故只有四點 path 與三葉 star。star 迫中央三角形的三條邊各貼一個
ear，恰 H-central。path 的中間兩面先組成 diamond；兩端面各貼到不同
中間面的原邊界邊。兩條被貼的邊若共享 diamond 的同一個 degree 三點，
得到 H-fan；若不共享該點，得到 H-zigzag。交換兩個中間面及反向外輪廓
涵蓋其餘選擇。這是原 boundary 次序下的分類，不以程式找到三型為證。

三角形有三 ears；diamond、五邊形 fan、H-fan、H-zigzag 各有兩 ears；
H-central 有三 ears。

## 4. 原 block-cut tree 的 ear／leaf 注入式計帳

私人 leaf x 必接 B/U 各兩個相鄰 pins 才能達到 d_G≥5。其原 rotation
移去唯一私人鄰點後的 terminal link 同時含 B、U，因此至少一次相鄰類型
切換給一個原 BUP 面。

若 x 是 PPP 面的角，且 d_F(x)=2，該 PPP 面占一個 sector；另一 sector
的全部 terminal link 至少有三點，因此亦同時含 B、U，給一個 BUP 面。
不同私人點供應的 BUP 面不同，因每個 BUP 面只有一個私人點。

對一個含 m≥1 個 cyclic blocks H_j 的分量，在原 block-cut tree 取連接
全部 cyclic-block nodes 的最小子樹 S。其所有 leaves 是 cyclic blocks。
只為計数抑去非 cyclic 的 degree 二 nodes；其餘非 cyclic nodes degree
至少三。樹的 degree-sum 公式給

\[
\sum_{j=1}^{m}\deg_S(H_j)\le2(m-1).                       \tag{3}
\]

若 H_j 有 e_j 個 ears，每個 S incidence 至多使用其中一個 ear。
至少 `Σ e_j−2(m−1)` 個 ear incidences 沒有被連接 skeleton 使用。
這些未使用 ears 是不同原頂點：若兩 blocks 共用它，該點必已在 S 中。
每個未使用 ear 若沒有附樹，就用 degree 二的 BUP charge；若有附樹，就
選該 ear 外的一個私人 leaf。不同 ears 的附樹不相交，否則原圖中形成
另一 cyclic block，與 S 的選取矛盾。因此該分量至少供應

\[
L=\sum_j e_j-2(m-1)                                      \tag{4}
\]

個不同 BUP 面。完全沒有 cyclic block 的非平凡樹分量，則由兩個不同
leaves 至少供應兩個 BUP 面。這個論證保留 shared cutvertices、任意
長橋路徑及全部 subdivisions；不把私人 degree 當完整 degree。

把 e_j=2+ε_j 代入 (4)，每個含環分量至少需 `2+Σ ε_j` 個 BUP 面。
全圖 M=2c 已被每個分量的基本兩個 charges 用盡，所以 **任何三-ear
block 都不可能**。特別排除全部 triangle blocks 與 H-central。

剩下的 cyclic blocks 只可能有 rank 2、3、4，而總圈秩是四。所以全圖
只能是一個二-ear rank4 hexagon，或兩個 diamonds。這也直接排除
`3+1`、`2+1+1`、`1+1+1+1`，涵蓋同一分量、分散分量及附帶樹分量。
分量分配 `(3,1)` 不另遺留；rank-one 分量本身至少需三個 BUP 面。

## 5. M 等號迫全部附樹與兩 diamond 連接方式

以下每個分量都恰有兩個 BUP 面，不容許其他原點產生額外 charge。

**H 類：單一 hexagon。** 唯一 cyclic block 是 H-fan 或 H-zigzag。
它的两 ears 各可接一條可空的原路徑；任何非 ear 點接附樹會另外產生
未被計入的私人 leaf，故不許。ear 的附樹若分叉或有兩支，亦至少產生
兩個 leaves，超過該 ear 的一個預算。所以各 ear 只能有一條可空 tail。
其餘 c−1 個分量都是非平凡原路徑，因只有兩個 leaves 的有限樹恰為 path。

**DD 類：兩 diamonds 在同一分量。** 兩個 cyclic-block nodes 的
connecting skeleton 是唯一原 path，兩端各占一個 block incidence。
為達 (4) 的等號，兩端必各使用一個 ear；若使用非 ear，就多出至少一個
未使用 ear charge。兩 blocks 可在各自的一個 ear 共用同一原 cutvertex；
否則以任意正長度原 bridge path 連接兩 ears。每個 diamond 的另一 ear
各帶一條可空 tail。connecting path 的內點、兩個連接 ears（包括共用
cutvertex）以及其他非 ear 點都不能有額外附樹，否則另生一個 leaf。
其餘 c−1 個分量是非平凡原路徑。

**D+D 類：兩 diamonds 在不同分量。** 只可能 c=2。每個分量只有一個
diamond，其兩 ears 各帶一條可空 tail；非 ear 不接附樹。沒有額外分量。

每個含環分量的兩個 designated ends 是未用於连接的 ears：若該 ear 有
非空 tail，就以 tail 的末端取代。其兩個 BUP 面恰在這兩 ends 各一個。
非平凡 path 分量也恰在兩末端各有一個。上述論證沒有移除任何原點；
shared ear 不被拆成兩點，bridge path 不被收縮，tail 長度也沒有按染色
等價改寫。

## 6. 精確存活清單與尚待驗證的範圍

| 類 | c=1 | c=2 |
|---|---|---|
| H-fan | 一個 fan hexagon，加兩條可空 ear tails | 同左，加一個非平凡 path |
| H-zigzag | 一個 zigzag hexagon，加兩條可空 ear tails | 同左，加一個非平凡 path |
| DD | 兩 diamonds 共 ear，或經 ear-to-ear bridge path 相接；兩端可空 tails | 同左，加一個非平凡 path |
| D+D | 不適用 | 每個 diamond 分量在其兩 ears 各帶可空 tail |

全表仍需 `8≤r≤14−2c−a`、原 terminal 附件界、完整 degree、同一原
B/U rotation 及原面。有限大小界之前，§2–§5 的分類與排除對任意 r
成立；本檔沒有從有限搜尋無反例推得結構定理。

下一步的完整來源到 strip 化約見 `ATTACHMENTS.md`。source-to-template
須是保原十 pins、全部原點邊及 rotation 的同構，從而保全部十列關係、
空 fibres 及 full lifts。這不是縮減代表，也不把相同 Σ 當作 R³ 等價。
本檔自身只交付完整必要結構分類與上列部分排除；最終是否排除所有來源，
須由全部必要模板的完整 Σ∈K132 驗證或另一個紙面矛盾決定。

證據類型：紙面定理，條件依賴固定 BASE 的來源契約與 K≤13=K≤5；
没有新增 Lean theorem。一般 `K∞=K≤5` 維持 **OPEN**。
