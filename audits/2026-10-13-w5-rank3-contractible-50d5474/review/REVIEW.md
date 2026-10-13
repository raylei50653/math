# W5-RANK3-C：獨立原面、blocks 與完整來源審查

固定 BASE `50d5474f2446403f3b3001d5943571184c8c9936`。
本審查直接閱讀正式 essential proof、rank-two STRUCTURE／REPRESENTATIVE、
私人單環／三色支援及共面正規形，重新證明本分支；沒有把 essential 的
`c=1,p=0,M=0` 或無葉性搬到本域。來源是全部目錄外 disk-C5 圖中先最小化
內點、再最大化邊數的 G，W5 任取，B/U 原 pins 與共同色框始終固定。
本檔前六節是紙面覆蓋審查；最後一節記本輪有限證據的實際驗證狀態。

## 1. 一般圈秩原面計帳與 contractible 位置

令 `q=e(F)-r+c`，`c` 起初包括全部私人分量及孤立點。原 annulus 的
Euler 式及邊面 incidence 給 `e(A)=3r+20`、原 annular 三角面數 `2r+10`。
PPP、PPT、同環 TTP、全 terminal、BUP 五類面數分別為

`t_P, 2e(F)-3t_P, 10-a, a, M`。

相加並以每條 B–U 邊恰有兩側得

\[
M=2(c-q+t_P),\qquad 2p=2a+M,
\qquad p=a+c-q+t_P.
\]

另由 `e(T,P)=e(A)-e(F)-10-p` 重算

\[
\sum_{x\in P}d_G(x)=2e(F)+e(T,P)=4r+10+q-c-p.
\]

F 的平面 Euler 式给有界面數恰 q，並不需要 F 連通。
假設 U/v 位於 F 的無界面，B 同樣位於無界面。任一有界 F 面的開區域內
既無 F 點邊，亦無 B/U/v；任何其餘 G 邊的 terminal 端點均在外部，不能
不穿 F 邊界而進入。故該面就是 G 原面，必為原 PPP 三角面。多邊界分量
或 bridge slit 不能是原三角面，故這些可能也被此論證排除。
因此 q=3 時 **恰有三個原 PPP 面**，而

\[
M=2c,\quad p=a+c,\quad
\sum d_G=4r+13-2c-a,\quad 7\le r\le13-2c-a.
\]

這最後一界使用完整 `d_G≥5`；不是私人 degree 下界。
每個私人點在兩環各至多兩附件，所以孤立點完整 degree 至多四，矛盾。
`c≥4` 時 `r≤5`。`c=3` 只能 `r=7,a=0`；三分量各至少兩點，大小恰
`3,2,2`，簡單私人圖至多 `3+1+1=5` 邊，而圈秩三要求 `e(F)=7`。
所以獨立確認完整剩餘域恰為

| c | r | a | p | M |
|---|---|---|---|---|
| 1 | 7…11 | 0…11−r | a+1 | 2 |
| 2 | 7…9 | 0…9−r | a+2 | 4 |

## 2. 三個原面迫完整 cyclic-block 清單

考慮 F 中任一含環的 2-connected block H。H 的外 facial boundary 是簡單
cycle，長度記 `l≥3`；其內部頂點數記 i。H 的每個有界面都必是 F 的原
PPP 三角面：若在 H 的某個內面插入別的 block、pendant bridge 或私人
分量，該插入物外側的一個 F 有界面將有 cutvertex、bridge 重經或多個
boundary components，不能是三角面。若有邊在兩個 H 頂點間進入該面，
則它本來就在同一 2-connected block，不能算作 H 外物。

寫 `q_H=e(H)-v(H)+1`。面長計數給

\[
2e(H)=3q_H+l,\qquad v(H)=l+i,
\qquad l+2i=q_H+2.
\]

圈秩按 blocks 相加，且總和三。因此每個 cyclic block 只可能是：

| q_H | (l,i) | 原 block |
|---|---|---|
| 1 | (3,0) | 原 facial triangle |
| 2 | (4,0) | 原四邊形加一條 diagonal，即 diamond |
| 3 | (5,0) | 原五邊形的三角剖分 |
| 3 | (3,1) | K4；唯一內部點完整 degree 三，來源排除 |

最後一列的內部點沒有 terminal 附件，亦不能有位於原三角面內的額外私人
分枝，所以是原圖上的直接完整 degree 矛盾，不是按名稱刪除核心。
五邊形的兩條不交 diagonal 必有共同端點，因此其三角剖分恰為五點 fan。
這個推導沒有預設 outerplanarity；恰是 `l+2i` 與完整 degree 排除內點。
原 subdivisions 也未被省略：任何 cyclic boundary 邊細分都會違反上述
原三角面／Euler 長度式；連接各 blocks 的原路徑則仍完整保留。

## 3. 可重用的 M 充足計帳引理

定義 `L(F)` 為私人 leaves 與 incident PPP 面的私人 degree 二點的總數。
每個這樣的點至少供應一份 BUP 原面：leaf 的唯一私人鄰点移去後，四個
terminal 鄰點在 link 成一段，兩環都出現；PPP degree 二點的三角 sector
另一側是 terminal link interval，完整 degree 至少五迫至少三 terminal，
同樣包含兩環。每段至少一次 B/U 轉換。不同私人點的供應面不同，因 BUP
面恰有一個私人點。因此 **`M≥L(F)`**。

一個孤立 triangle block 有三個可計帳耳，diamond 有兩個，五點 fan 有兩個。
把同一分量的 s 個 cyclic blocks 以原 block tree 的原橋路徑及 cutvertices
接起來，每接入一個新 cyclic block 至多失去兩個這樣的耳：新 block 的
接點一個，既有部分的接點至多一個。原 bridge 分叉可先納入連接子樹，
不會減少更多耳。等價地，把 cyclic blocks 視為葉／節點、非 block 的
連接點視為 Steiner nodes，連接樹在 block 上的 incidence 數至多
`2(s−1)`；非 block Steiner nodes 在最小連接樹中 degree 至少二。

之後加入所有剩餘原附樹不會降低 L：若根原本有一份計帳，這份最多消失
一次，而非空附樹有至少一個新的 leaf；若根不被計帳則只增加 leaves。
不同附樹的新 leaves 不同，故不存在重複消耗。任何其他非平凡樹分量
另供應至少兩個 leaves。於是圈秩三的原 block 分配給出：

| cyclic blocks／分量 | cyclic 部分的 L 下界 |
|---|---:|
| 三個 triangle blocks 在同一分量 | 3+3+3−4=5 |
| diamond 與 triangle 在同一分量 | 2+3−2=3 |
| 一個五點 fan block | 2 |
| 圈秩分配 (2,1)，分量各自任意附樹 | 至少 2+3=5 |

與 `M=2c` 比較，前三列若再有 `c−1` 個樹分量，要再加 `2(c−1)`。
故多 block 的 rank-three 分量全部排除，`c=2` 的 `(2,1)` 全部排除。
唯一尚可的私人圖由**一個五點 fan，加兩耳的可空原路徑，以及 c−1 個
非平凡原路徑分量**構成。

取等號還證明：fan 其他三點不能有附樹；每耳至多一條 path，不能分叉；
額外樹分量恰有兩葉，故是 path。只有各分量的兩端供應 BUP 面，且每端
恰一份，其餘私人點沒有 BUP 面。此處來源可以有 leaves，從未使用 M=0。

## 4. 原 rotation 與 strip 覆蓋

寫 fan 外 cycle 為 `x,z,y,t,w,x`，diagonals 為 `zw,zt`。兩耳為 x,y；
短側 `x-z-y` 的中點 z 私人 degree 四；長側 `x-w-t-y` 的中點 w,t
私人 degree 三。沿完整私人外 contour 走，bridges 正反兩側各走一次。
terminal 類別切換恰對應 BUP 面；每分量只有兩次切換、都在兩端，故
兩條端到端 contour arcs 分別只見 B、只見 U。

因此 z 僅接一環，完整 degree 要求一或兩個該環相鄰 pins；w,t 只接
另一環，完整 degree 迫各接該環兩相鄰 pins。短側消耗零或一條 rim edge，
長側消耗恰兩條。兩種短側類別 B/U 都必保留，不能獨立反轉一環。
尾路／其他 path 的每條 bridge 兩側 third vertices 分別來自 B/U。

`p=a+c≥1`。沿全部 B–U crosscuts 切開 annulus，crosscut 之間的每個
region 兩側最多供應兩份 BUP 面。每個私人分量已要兩份，故每 region
至多一個私人分量；每個含私人點的 region 就是上述 fan/path strip。
無私人點的 region 因三角化且內部沒有 B–U 邊，必恰是全 terminal 三角面。
總 region sequence 是一個 fan strip、`c−1` 個 path strips、a 個全 terminal
triangles。允許 crosscuts 共 pins 及 p=1 的同邊兩側。

這說明所有附路、原 bridges 的兩側、cutvertices、三角面的相對位置及
全部 terminal 邊均被此 strip 域涵蓋；沒有因方便編碼而刪掉來源。

## 5. 完整有限字域與固定 pins

每個 backbone 點記 `O,B,U,D=(0,0),(1,0),(0,1),(1,1)`。其兩側每環
至少一個 attachment；每個 1 再用下一個 pin。完整 degree 直接決定域：
leaf 只可 D；無尾耳及普通內點不可 O；有尾耳可四種。fan gap 另增加
短側 `apex_step∈{0,1}`、長側 2。起點與終點各給 BUP 面；各全 terminal
triangle 只讓對應一環前進一步。

使用**整數**前進量各等於五，不只檢查 mod 5 端點相同。全部原邊分為
兩環邊、私人 fan/path 邊、terminal–private 邊、B–U 邊，均由此資料
逐類恢復；每面及每個 bridge 的兩側亦固定。必要模板可保留未使用的
更強來源條件，但每份模板本身須是合法的指定外面／U 空面 annulus。

獨立枚舉採完整 four-letter products、完整 region-order products 後
按 integral rim budgets 過濾；主 checker 則由已消耗步長求所需 B/U
terminal triangles，再枚舉其 multiset permutations。兩者不共用域生成器。
`independent/check.py --list` 重算得：

| c | r=7 | r=8 | r=9 | r=10 | r=11 | 合計 |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 444 | 608 | 626 | 384 | 100 | 2,162 |
| 2 | 48 | 44 | 16 | — | — | 108 |

總數 2,270。這項數字只核對紙面域；不自行证明 source exclusion。
原圖對模板的 pins maps 是兩環各自起點、共同 ambient 方向的完整嵌入
同構；所有 B/U/private 顏色同時搬運，同一個 S4 色置換作用整份 lift。
任何一般 mask／代表必按同一 B map 拉回；不能獨立正規化兩環。

## 6. 染色保存與來源排除的義務

獨立 checker 從鄰點區間建 literal edges，從保存 rotation 走全部面，
重算 components、rho、每點完整 G-degree／F-degree、t_P、a、p、M。
再以固定頂點次序分別直接 DFS 枚舉 A 和補中心 G，逐列逐 cell 比較完整
fibres，包括所有空 cells 及全部 full lifts；不匯入主生成器。
三色 U 每份 A lift 補唯一缺色中心，主 checker 另作同一份 lift 對照。

若完整必要域所有 Σ 屬 K132，即直接矛盾目錄外來源；若使用較小代表，
只須完整 `pr_B R³` 相同且內點嚴格減少。相同 Σ 不推出相同 R³；任何
代表只保 Σ 時，U 色、中心色及 fibre 重數皆不在保存結論內。

## 7. 實際有限驗證與採納狀態

紙面 general-q 公式、`t_P=3`、`c≤2`、完整 block 分類、M 計帳、原
rotation 與字域覆蓋通過獨立審查。另逐節核對本輪
`structure/ATTACHMENTS.md` 及主 checker 的原面重建：兩種 apex 方向、
零／一步短側、所有 tails、tree component、region orders 均在完整域內。

本審查實際執行完整 independent replay，結果見
[independent.log](../logs/independent.log)：

* 2,270 份來源必要模板，c=1 的 2,162 份及 c=2 的 108 份全部涵蓋。
* 23,244,800 cells、22,713,170 空 cells、928,404 A full lifts、465,866 G full lifts。
* 完整 Σ 分佈為 `1023:2216,639:32,511:8,767:8,1007:2,91:2,1021:1,1022:1`。

獨立 checker 驗證 `CATALOGUE_INPUT.json` 固定 BASE、實際 frozen bytes
及 SHA256、十列順序與 K132 的 132 entries，再對每份直接算得的完整 Σ
核對 membership；上述八種均在 K132。來源 maps 是整圖同構，目錄亦涵蓋
原 B 的 D5 重新標號，故拉回每份原來源的完整 Σ 仍在目錄內。
這與目錄外身份矛盾，無須建立同槽位縮減代表。

`independent/negative.py --write` 與 `--check` 完整重播，見
[negative.log](../logs/negative.log)、[negative-replay.log](../logs/negative-replay.log)。
两份 c=1/c=2 正控制先由兩 checker 接受；漏私人原邊、錯 rho、漏樹分量、
錯 U pin map、反 U 空面、把 G-degree 改為 F-degree、漏 A full lift、
誤用 essential 的 M=0 共八種缺陷，各被兩個 validator 拒絕，合計十六次。
每項保存完整 source key/hash、精確 mutation、損壞 record hash 及拒絕結果。

同份負控制 artifact 還保存實際 prism 的所有原邊、面、rotation、pins、
10,240 cells 與 A/G 全 lifts。獨立 DFS 及主 checker 重算都確認它與一份
fan source 的 Σ 同為1023，但在 `beta=01012,tau=10103`，source cell 空、
prism cell 非空。因此「相同 Σ 蘊涵相同 R³」有實際 counterexample。
這份 prism 僅為保存強度控制；本輪排除方法是直接 K132 membership，
不宣稱為全部來源建立 R³／同槽位 annulus 代表。

**最終獨立審查 PASS：全部 contractible 圈秩三來源排除。** 接既有
essential 圈秩三排除及既有圈秩至少三，完整最小來源的**任取**合法全內部
W5 都滿足 `ρ(G[P])≥4`；沒有將存在一個可選 W5 偷換為任取量詞。

沿用上游 K132、4CT 及外部計數信任邊界；不借用並行 K13 任務結果。
沒有新增 Lean theorem。真正最小 933／941 來源實例為 `not triggered`，
這與普遍紙面覆蓋及有限模板檢查分開；一般小代表及 `K∞=K≤5` 仍 OPEN。

執行紀錄保留：第一次 independent 命令在 shell 重導向時因尚無 `logs/`
目錄而未啟動 checker；建立新目錄後重跑即得到上述完整 PASS。沒有刪改
舊證據或以失敗重播更新既有 certificate。
