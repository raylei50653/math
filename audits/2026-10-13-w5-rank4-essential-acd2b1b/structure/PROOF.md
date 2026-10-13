# W5-RANK4-E：essential 私人圈秩四的完整來源化約

固定 HEAD `acd2b1beea6c909edade565a00eeeeac05d2b3a7`。輸入 bytes、Git blobs、
工作樹快照與各自權限見 [BASE](../BASE.json)。本證明只用固定 HEAD 的來源鏈；
未追蹤的 rank4-contractible 結果只供後續合併結論，不是本證明的前提。

## 1. 完整最小來源與一般 essential 計帳

G 在所有完整外框關係不屬 K132 的 disk-C5 圖中先最小化內點數 k，再最大化
邊數。任取合法全內部 induced W5，保留原中心 v、原外框 B=(b0,…,b4)、
原鄰環 U=(u0,…,u4)、十 pins、原面與 rotation。U 的有界 disk 恰含 v 及
五個原三角面。令 A=G−v，P=V(G)\(B∪U∪{v})，F=G[P]，r=|P|=k−6，
c=c(F)，q=ρ(F)。反設 q=4，且 F 中有分隔 B/U 的 essential 簡單環。

固定 HEAD 的 K≤13=K≤5 給 k≥14、r≥8。原最小來源正規形給 B/U induced
C5、其餘 annular 原面三角化、每個內點完整 d_G≥5。外框附件界給每個
私人點至多兩個相鄰 B pins。U 版由原 C4 cap 推出：若 x 接兩個不相鄰
U pins ui、uj，原 C4 x−ui−v−uj−x 的有界側會包含非空的另一 U 弧，
違反所有原簡單 C4 有界內部無點。因此每環各至多兩個相鄰附件，d_T≤4。
所有這些都是完整 G 的條件；沒有加入 N2、edge-critical、Gallai 或 F 連通。

以 h 記 PPP 原三角面數，p 記 B–U 原邊數，a 記全 terminal annular 原
三角面數，M 記 BUP 原三角面數。固定 rank3-essential 紙面已對任意 q
逐原面／邊證明

\[
M=2(c-q+h),\quad p=a+c-q+h,\quad
\sum_{x\in P}d_G(x)=4r+10+q-c-p.                 \tag{1}
\]

F 有 q 個有界面。U/v 位於其中一個；任何其他有界 F 面沒有 G 頂點或
可越界進入的原邊，必恰是 PPP 原三角面。此說法包含多個私人分量、slits
與 bridges；沒有把抽象獨立環當原面。故 h=q−1=3。Essential 環阻斷 B–U
邊，p=0；(1) 給 0=a+c−1，因 c≥1、a≥0，得到

\[
c=1,\quad a=p=M=0,\quad h=3,\quad
8\le r\le13,\quad \sum_P(d_G-5)=13-r.          \tag{2}
\]

由 d_T≤4 先排 F 孤立點。若私人 leaf 存在，完整度數迫它在 B/U 各接兩
pins；其唯一私人邊以外的連續 terminal link 必有 B/U 切換，產生 BUP
面，矛盾。故 δ(F)≥2。若 x incident PPP 面且 d_F(x)=2，該 PPP 面占去
一個 sector，另一個 terminal link 至少含三 pins，亦迫 BUP 面。因此

\[
x\text{ incident PPP face}\Rightarrow d_F(x)\ge3,
\qquad \sum_P(d_F-2)=2(q-1)=6.                 \tag{3}
\]

## 2. 三個 PPP 原面的全部交疊型

令 S 為三個 PPP 面邊界的聯集。由 (3)，|V(S)|≤6。以「共享原邊」定義
這三個面的 adjacency graph；同一原邊至多 incident 兩個原面。

若三面 edge-connected，先合併相鄰兩面得到 diamond。第三面若增加一點，
是沿 diamond 邊貼三角形所得的三角化五邊形，唯一無標記型為 fan。若
不增加點，必補成 K4 的三個面。在後一情形，K4 中不 incident 第四個面
的那一點被三個原 PPP sectors 圍滿，不能再有私人邊或 terminal 邊，故
其完整 d_G=3，矛盾。不存在沿同一條邊再貼第三面。

若恰兩個 edge-clusters，則是 diamond 加一個三角面。兩者不交時有七點，
違反 |V(S)|≤6。恰共享一點時有六點，但該點在 S 已 degree≥4；所有六點
均需 d_F≥3，故總 excess 至少七。恰共享兩點時，為避免兩 clusters 合併，
這两點只能是 diamond 中唯一不相鄰的兩 tips。於是 S 有五點、八邊，
Σ_{V(S)}(d_S−2)=6；第三三角面的新點卻在 S 只有 degree 二，依 (3) 尚須
額外私人邊，令完整 excess 超過六。共享三點則必共享原邊，非本情形。
這個「共享兩個不相鄰原點」分支沒有被省略。

若三面各自為一個 edge-cluster，每對至多共一點，故頂點聯集至少六點。
若恰六點，至少一個共有點 incident 兩組互不重疊的兩條三角面邊，已
有 degree≥4；其餘五點各需 degree≥3，仍超過 excess 六。更多點亦矛盾。

所以三個 PPP 面恰組成三角化五邊形 fan。其依原外輪廓依序為

`x — qS — y — q1 — q0 — x`，

原 diagonals 為 qS–q0、qS–q1；原三角面為 xqSq0、qSq1q0、yq1qS。
在 S 的 degree profile 是 qS:4、q0/q1:3、x/y:2，已使用 excess 四。
依 (3)，兩 ears x/y 各尚須至少一條私人邊，剛好用完餘下二。因此在 F 中
qS degree 四，q0/q1/x/y degree 三，所有其餘私人點 degree 二。

S 外的私人邊只能接兩 ears，各接一條。刪去 S 的邊後，含額外邊的部分
有兩個 degree-one ends x/y，其餘點 degree 二，且 F 連通。它恰是一條
涵蓋全部其他私人點的簡單 x–y 原路徑 Q。不能另有 disjoint cycle、附樹、
分叉、額外分量或遺漏 subdivision。Q 的長度 r−4 介於四至九。

## 3. 原 annulus 位置与全部 terminal 附件

fan 的三個三角面填滿一個原 disk。Q 位於這個 disk 外，F 的另外兩個面
是無界面與含 U 的面，面邊界分別由 Q 接 fan 的一條 x–y arc 組成。
短 arc 是 x−qS−y，長 arc 是 x−q0−q1−y。保留兩種方位：短側接 B 或接 U。
以下先寫短側接 B；另一方位由交換 B/U 並反向全部 faces 構造。

qS 唯一 terminal sector 只含 B，d_F(qS)=4 迫一或兩個 B pins；兩個
時相鄰。記 d=0 或1為該 sector 消耗的 B 環邊數。q0/q1 只接 U，私人
degree 三各迫兩個相鄰 U pins，合計消耗兩條 U 環邊。

將 gap x→y 與反向 Q 排成 cyclic backbone z0=x,z1=y,z2,…,z(s−1)，
s=r−3。gap 不是原邊，絕不加入 xy。Q 上每條原邊的兩側第三點分別在
B/U。每個 backbone 點的兩個 terminal sectors 各至少一 pin，各至多
兩個相鄰 pins。令 letter O/B/U/D 分別表示增量 (0,0)/(1,0)/(0,1)/(1,1)。
兩 ears 的私人 degree 三容許全部四 letters；其餘 backbone 點私人
degree 二，需要至少一側額外 pin，故只容許 B/U/D。

兩個 terminal 環各有五條原邊，其唯一 annular incident 三角面均出現在
上述 fans，不能重用、漏用或獨立反向。因此完整必要域為

\[
r=8,\ldots,13;\quad s=r-3;\quad d\in\{0,1\};\quad
w_0,w_1\in\{O,B,U,D\};\quad w_i\in\{B,U,D\}\ (i\ge2),
\]
\[
\sum_i\delta_B(w_i)=5-d,\qquad \sum_i\delta_U(w_i)=3,       \tag{4}
\]

另有短側 B/U 兩種方位。普通 sectors、七條 fan 原邊、Q、十條環邊及
指定中心 spokes 恢復全部原圖；沒有橋收縮、ear 識別或額外改邊。

原 pins 拉回明存 g_B(i)=s_B+εi、g_U(i)=s_U+εi (mod5)，使用共同
ε∈{±1}，兩起點可不同。若 U 原名按 face direction，先記明固定換算。
私人點依原 Q、fan、rotation 映回，中心映回 v。此為同一原帶嵌入圖的
同構，逐字搬運十 pins 與全部 A/G full lifts；只可共同 S4 重命名顏色，
不得獨立正規化 U 或拼接不同 rows。

## 4. 完整 finite domain 與關係排除

(4) 不是以搜尋上限猜出的域；上限來自 (1)–(2)，完備性來自 §§2–3。
按 r、d 分別的 words 數可由
`[x^(5-d)y^3](1+x+y+xy)^2(x+y+xy)^(r-5)` 獨立核對：

| r | d=0 | d=1 | 含兩種方位的模板數 |
|---:|---:|---:|---:|
| 8 | 10 | 38 | 96 |
| 9 | 80 | 124 | 408 |
| 10 | 235 | 185 | 840 |
| 11 | 326 | 130 | 912 |
| 12 | 217 | 35 | 504 |
| 13 | 56 | 0 | 112 |
| 合計 | 924 | 512 | 2,872 |

此域只強制本證明使用的原圖／私人 degree 條件，保留可能不符其他來源
限制的模板，故是必要域超集。完整 B/U degree flags 隨原圖保存，不能稱
每份模板為真正最小目錄外來源。

逐份證書保存 literal edges、原 faces、rotation、pins、ownership、完整
G/F degrees，十個固定 beta rows，每列全部1,024個 literal U cells，
包括空 fibres，以及所有完整 A lifts 與 G lifts。主 checker 直接枚舉 G，
另與從三色 U 的 A lifts 唯一補中心所得完整列表比較；獨立 checker 自
neighbours 重建原邊、自 rotation walk 重建原面，固定 U→中心→私人點
次序直接枚舉 A/G。它們比较完整列表而非只有 mask 或 hash。

全部2,872份的完整 Σ 均為1023，含29,409,280 cells、28,345,408空格、
2,051,516份 A lifts、1,017,324份 G lifts。Σ=1023在原 B 的 D5 搬運及
共同色框下仍是全收十列，並屬固定 K132；故每一可能原來源均與目錄外
身份矛盾。這完成 essential q=4 排除，不需要較小代表，也不宣稱 R³ 等價。

## 5. 證據與精確界線

本證明是固定來源契約下的紙面完備化約，加上述有限 Python 完整證書。
真正最小目錄外来源仍 `not triggered`；排除來自全域覆蓋＋全模板關係，
不是零 trigger。沿用上游 K132、K≤13、四色定理與外部計數信任範圍，
本輪沒有重建上游全部證書，也沒有新增 Lean theorem。

本 audit 自身結論為：任取合法 W5，若 F 有 essential 環，則ρ(F)≥5。
固定 HEAD 只給 contractible 的ρ≥4。另行審查／採納凍結的未追蹤
rank4-contractible audit 後，兩者才共同給任取合法 W5 的ρ≥5。
一般ρ≥5排除、一般 annulus 小代表、保R³縮減及 K∞=K≤5 仍 OPEN。
