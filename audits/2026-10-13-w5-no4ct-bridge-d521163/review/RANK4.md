# W5-NO4CT-BRIDGE：圈秩四來源覆蓋的獨立接入審查

2026-10-13。橋接 BASE：`d521163`；本審查只新增本檔，不修改任何舊證明、
原 BASE、證書或 seal。兩份原 rank-four audit 的 BASE 均保留
`acd2b1beea6c909edade565a00eeeeac05d2b3a7`。

**判定：圈秩四的 essential、contractible 兩支皆接通 932／933／941。
沒有尚待修復的 rank-four 前提。** 這是新來源契約導出舊有限必要域的證明；
舊完整染色證書只按原 manifest、摘要與 receipts 接入。本文本身不承擔
圈秩零至三的接入，也沒有重播全部舊染色。父層須將低圈秩接入另行採納後，
才合併為任取合法 W5 的私人圈秩至少五。

## 1. 實際消費的共同局部契約

給定任取的合法全內部 induced W5，定義原十 pins B/U、中心 v、A=G-v、
P=V(G)\(B∪U∪{v})、F=G[P]、r=|P|=k−6、c=c(F)、q=ρ(F)。
以下 L1–L5 足以逐句重用兩份 rank-four 的來源分類；不需要來源 mask
恰為933或941，也不需要以4CT推出的普遍 exterior screen。

| 編號 | 分類實際使用的事實 | 新 no4ct 來源依據／修復 |
|---|---|---|
| L1 | A 有指定 induced C5 外面 B 與空內面 U，十 pins 互異，其他原面全三角；中心完整鄰集恰 U | frontier `w5/PROOF.md` §§1、5；任取合法 W5 的定義本身給 U disk 與 ownership |
| L2 | 每個私人點的**完整** d_G≥5 | frontier §1 引 no4ct 度數接入；不假設 d_F≥5 |
| L3 | 每個私人點在 B、U 各至多兩個附件，雙接時相鄰 | B：frontier §4；U：下面 C4 Jordan 論證 |
| L4 | r≥8 | 新 no4ct k≥16 給較強 r≥10，從而滿足舊有限域起點；不重新引用舊 K13 的4CT前提 |
| L5 | 完整原 Σ 不在同一132個具體關係 K；K 在外框 D5 搬運下封閉 | 新全域最小目錄外契約及 K132 witnesses；舊 contractible `catalogue.py`／獨立 checker 對固定 masks 的有限封閉性 receipts |

frontier 入口為 `audits/2026-10-13-c5-no4ct-frontier-6943561/w5/PROOF.md`
與同目錄 `DEPENDENCIES.md`。其新論證已把原簡單 C4 的私人 cap 大小寫為
s≤k−i(C)<k，因此適用受限 C4 代表，不借用任意大小 C4 定理。proper C5
的相同嚴格大小論證在 frontier 中亦已修復，但兩份 rank-four 的分類本身
**不再消費 proper C5 cap 引理**。

對 L3 的 U 側，假設 x∈P 同接非相鄰 ui、uj。原簡單 C4
x−ui−v−uj−x 的 v-spokes 兩側各有一段非空 U 開弧，而 x 在合法 U disk
外。Jordan 分離使其中一段開弧的原 U 點落入該 C4 有界側，違反 frontier
已證的原 C4 有界內部為空。故 U 附件至多二且相鄰。這只用指定原 cap，
沒有任何 universal screen 或 singleton support 非空假設。

因此 d_G(x)=d_F(x)+d_T(x)、d_T(x)≤4，給 d_F(x)≥1。私人 degree-one
點的完整 degree 恰五，B/U 各有兩個相鄰附件。後續所有對私人 degree 的
要求都由這些等式與原 faces 推出，並非將 d_G≥5 偷換成 d_F≥5。

## 2. 兩個幾何分支窮盡，計帳沒有 mask 條件

原 B 位於 F 無界面；連通的 U 加中心位於某一 F 面。若它位於無界面，
就是 contractible 分支；否則有原 F 簡單環分隔它與 B，是 essential 分支。
反向由 Jordan 分離亦成立。這是原 plane embedding 的面位置二分，
容許 F 不連通、cutvertices、bridges 以及任意 subdivisions，不是先選
一個方便的 embedding 或只看抽象 cycle-space generators。

令 t 為 PPP 原三角面數，M 為 BUP 原三角面數，a 為全 terminal annular
三角面數，p 為 B–U 原邊數。逐原面／原邊 incidence 給

\[
M=2(c-q+t),\qquad p=a+c-q+t,\qquad
\sum_{x\in P}d_G(x)=4r+10+q-c-p.                 \tag{1}
\]

這些等式來自 e(A)=3r+20、annular 三角面數2r+10及 e(F)=r−c+q。
每條 bridge 的兩 sides 分別计入；沒有私人連通、933／941 singleton、
N2、edge-critical、Gallai 或 coloring screen 假設。

F 共 q 個有界面。contractible 時，全部 terminals 與 v 在無界面，
其他 F 開面沒有刪去的 G 點、也不可能有從 terminal 進入的原邊，故每個
有界 F 面就是原 PPP 三角面；含多重 boundary 或 slit 的形式也因此排除，
t=q。essential 時恰一份有界面含 U/v，其他都同理為 PPP 原三角面，
t=q−1；分隔環使 p=0，再由 (1) 得 a=0,c=1,M=0。

原 rank-four 分類反設 q=4 就可開始；前置 q≥4 只曾用於當時的合併表述，
不是其 q=4 必要域分類的邏輯前提。故不會以尚待橋接的低圈秩結論循環證明。

## 3. Contractible：全部分量、blocks、bridges、細分及附件

直接採納的原紙面為
`audits/2026-10-13-w5-rank4-contractible-acd2b1b/structure/FORMULAS.md`、
`CORE.md`、`ATTACHMENTS.md`，逐項以 L1–L5 重接。

q=4 時 t=4、M=2c、p=a+c，完整 degree 計帳給
r≤14−2c−a。新 r≥10 直接迫 c≤2，必要大小域為 c=1 的10≤r≤12，
c=2 的r=10,a=0。它是舊 c=1 的8≤r≤12與c=2的8≤r≤10域的子集。

如果私人點不 incident 原 F 無界面，沒有 terminal 邊能到達它，它的
所有 sectors 都是四份原 PPP 三角面的 corners，完整 degree≤4，矛盾。
故 F 在原 embedding 中 outerplane。cyclic blocks 的有界面全是原三角面；
rank h 的 block 邊界／內點式 b+2i=h+2 給 h≤4 的完整小 block 清單。
內點型由上項排除；六邊形三角化恰 fan、zigzag、central 三型。

对一個有 m 個 cyclic blocks 的分量，原 block-cut skeleton 滿足
Σ deg_S(H_j)≤2(m−1)，包含共 cutvertex 及實際橋路徑。
每個未被 skeleton 使用的 ear，若無附樹則由原 degree-two PPP corner
收取一個 BUP 面，若有附樹則由該樹 leaf 收取一個；不同 ears 的收費點
不同。無環的非平凡樹分量至少有兩 leaves，也需兩 BUP 面。
因全域 M=2c 已把每分量兩面的基本額用盡，全部三-ear blocks 排除，包含
triangle 與 central hexagon。等號又排除非 ear 附樹及 branching tails。

因此全部存活分配恰 H、DD、H+P、DD+P、D+D：H是兩-ear hexagon；DD
是同分量兩 diamonds 共同一 ear 或由 ear-to-ear 原橋路徑連接；D+D是
分開的兩個 diamond 分量；P是非平凡 path。所有兩端 tails 可空，DD共 ear
保同一原點，所有非零橋長、tails 及 subdivisions 均保留。rank分配
3+1、2+1+1、1+1+1+1並無遺漏，均因 triangle block 多需 BUP 面而排除。

每個分量恰有兩個 BUP 面，沿原無界 contour（bridge雙側分別行走）
讀出兩段單色 B/U terminal arcs。原 B–U crosscuts 把 annulus 切成 c 個
私人 strips 及 a 個 terminal triangles，包含相鄰 crosscuts 共 endpoint
及 p=1 同一邊兩側的情形。每條原 B/U 環邊只有一份 annular 面，故兩環
各須恰走五步，不能獨立反向、重用某環邊或漏掉 terminal triangle gaps。

原 H0–H3 四個 rooted hexagons 覆蓋 fan／zigzag 的全部起始 ear 與 B/U
方位。E／D／H atoms 保原邊、blocks及共享點；backbone 字母
O/B/U/D依 d_G=d_F+2+δB+δU≥5取值；polygon非backbone點用
 d_G=d_F+1+δ≥5，故私人degree-five fan apex仍至少一個terminal。
全部原面逐份重建，形成同一原圖、原rotation、十pins與中心ownership
的同構；它不是縮小代表。

生成器 `controls/check.py` 的 `parameters()`（約110–131行）只依上述
c/r、family、實際E長度、degree、環前進量及a上界生成。
主迴圈對每份 `fill(make(param))` 後才計算 Σ membership，沒有先以
933／941、目錄 membership、screen或singleton支援篩掉來源。
Bdegree≥4與Udegree≥5僅作flags，保留816份額外模板而不刪；必要域超集
因此仍涵蓋新三支來源。

## 4. Essential：PPP交疊、原外路及兩方位

直接採納的原紙面為
`audits/2026-10-13-w5-rank4-essential-acd2b1b/structure/PROOF.md`。
q=4 給 c=1,p=a=M=0,t=3，Σ_Pd_G=4r+13，故10≤r≤13。
M=0排除私人leaf；一個incident PPP face的私人degree-two點，其另一
sector因完整degree≥5至少有三個terminal鄰點，迫B/U切換及BUP面。
故這類點d_F≥3，且全圖Σ(d_F−2)=6。

三個PPP面的聯集因此至多六點。以共享原邊的clusters完整分類：
三面連邊cluster給pentagon fan或K4；K4有一點被三個PPPsectors囲滿而
完整degree三，矛盾。diamond加第三triangle若不交有七點；若只共一點
則excess至少七；若共兩個不相鄰tips，聯集已用完excess六，但第三面新點
還需增加私人degree，亦矛盾。三個不共享邊clusters至少六點，等號時又有
共點degree至少四，使excess超標。易漏的「共两個非相鄰tips」分支已保留。

唯一pentagon fan的原degree profile為4,3,3,2,2。兩ears各需要額外一條
私人邊，用盡excess；連通性因而迫fan外全體原邊是唯一ear-to-ear簡單
外路徑。沒有分離cycle、附樹、branch、額外分量或刪去的subdivision。

fan短側apex在該側一／二相鄰pins，長側兩點各恰兩pins；短側接B或接U
兩方位均保留。兩ears允許O/B/U/D，其他路徑點允許B/U/D；長度s=r−3，
短apex增量d∈{0,1}，words總增量為(5−d,3)。這已保留全部原附件。
`controls/check.py` 的 `words`／`run` 對全部r,d,flip,word計算完整染色後
才assert Σ=1023；沒有任何933／941-only filter。被重用的舊 `fill`／
`lifts` 直接枚舉同一固定β下全部四色assignments，也沒有screen假設。

## 5. 舊有限證據的精確採纳與較強大小域

以下是兩份原 `controls/summary.json` 的既有結果；此審查未重算染色：

| 分支 | 原完整必要域 | 完整Σ結果 | canonical解壓證書SHA-256 |
|---|---:|---|---|
| contractible | 6,389 | 511、639、767、895、1019、1023，全部∈K132 | `d72dcbdab3fbb00ac79344d7645ff0921f89fa798030e76fd9ed51bdd6b4ee8d` |
| essential | 2,872 | 全部1023∈K132 | `621fc7c1c57bdcb3917943d03911d768cd251e37cd570087cff191bdd0436f26` |

新 r≥10 只縮小來源可能域。把原summary的`types`／`by_r`按r≥10相加，
可讀出下表；它是**舊摘要metadata篩選**，不是新模板生成、新染色重播或
新的完整fibres receipt，更不是實際最小來源個數。

| 分支 | r | c/a細分的原必要模板數 | 小計 |
|---|---:|---|---:|
| contractible | 10 | c1:a0=966,a1=590,a2=162；c2:a0=68 | 1,786 |
| contractible | 11 | c1:a0=759,a1=190 | 949 |
| contractible | 12 | c1:a0=220 | 220 |
| contractible | 合計 | 仍保留未用盡來源degree條件的超集 | 2,955 |
| essential | 10／11／12／13 | 840／912／504／112 | 2,368 |

原contractible壓縮證書SHA為
`b5f14291115e4b8955c075bb96ed171c4621ecfc31a096ecb32f9bc05d794594`；
原essential壓縮證書SHA為
`70e63163dce7037a411cbaf22f1beb272e48a81fe72e5ee2c99ac9222816877c`。
兩份原 `DELIVERY.json` 封存證書、summary、proof、generator、review及
`VERIFICATION.json`，其原receipts記主normal／seed17、獨立完整染色和
破損控制。本輪父層的custody replay對原manifest bytes核對；不把hash核對
說成新完整染色重播，也不改寫原報告尚列4CT信任的歷史依賴。

source-to-template同構使用共同方向ε、B/U各自起點，私人點依原contour
映回，中心映回v；同一原β列中的全A/G lifts逐點搬運，包括空fibres。
只有共同S4顏色更名，不可獨立正規化U。K132的D5封閉性處理原B pin拉回。
因此任一新no4ct來源若q=4，其原完整Σ必屬K132，直接矛盾目錄外身份。
真正最小來源仍not triggered；排除依靠任意來源覆蓋與已凍結全模板結果。

## 6. 採納界線

已完成具名接入引理 **W5-NO4CT-R4-C** 與 **W5-NO4CT-R4-E**：
在新全域最小目錄外三支契約下，任取合法全內部induced W5，私人ρ=4
的兩個原拓撲分支均不可能。不存在rank-four-only的未修復大定理。

此結論不證一般ρ≥5來源的排除、普遍九點W5代表、一般annulus縮減、
不同圖間R³／fibre重數等價、K∞=K≤5或任何新Lean theorem。父層合併前
仍須另核對零至三圈秩；本檔沒有以舊「ρ≥5」標題直接承繼該結論。
