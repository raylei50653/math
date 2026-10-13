# W5-RANK4-C：全部原附件、strip 字與 pin 搬運

固定 BASE：`main@acd2b1b`。本檔承接 `CORE.md` 的紙面分類，不借用 rank3
染色結論。每個原私人分量都有兩個指定 ends，各在原 rotation 給恰一個
BUP 面；其他私人點没有 BUP 面。兩個 ends 之間保留 hexagon、diamond、
原 bridge paths、shared cutvertices 與全部原 subdivision 點。

## 1. 原 contour 迫兩側 terminal arcs

沿每個私人分量的原無界 facial contour 走一周，每條 bridge 的兩側各
走一次。對每條不屬 PPP 面的私人 edge side，原三角面的第三點必是
terminal，給該 side 一個 B 或 U 標記。在同一原點、相鄰私人 darts 間，
terminal neighbours 是一個原 link interval；每次相鄰 terminal 從 B
切到 U 或反向，恰對應一個 BUP 原面。PPP sector 沒有 terminal，也沒有
新切換。

每個分量恰有兩個 BUP 面，而且分別位於兩個 designated ends。因此其
兩段 ends-to-ends contour 一段全是 B，另一段全是 U。同環原 terminal
link 只可按原環的連續次序走，不能跳 pin、逆向後再前進，或單獨翻轉
某一個環。每次同環前進都使用該原環邊唯一的 annular incident triangle；
反向重走或在另一 fan 再用同一環邊，就會給它第二個 annular 面，矛盾。
原 rotation 因而固定各 fan 的共同前進方向。每個 exposed 私人 boundary edge 的第三點尤其迫兩個端點
都至少接到該側一個 pin。

非 cut 的 polygon 內側點只出現在其中一段 contour，故只接該段所屬
的環。即使 H-fan 的 apex 已有私人 degree 五，也不能選零 terminal：
它的 exposed boundary edges 各有 terminal third vertex。每環最多兩個
附件且相鄰，所以這類點的附件只能是一個當前 pin，或當前 pin 加下一個。

backbone 上每個點出現在兩段 contour，或是兩段的共同 end，因此至少
接當前 B pin 與當前 U pin。shared diamond ear 是同一個原頂點，其
兩個外側 sectors 分別在 B、U contour 上；它不被複製、拆點或獨立上色。

## 2. Crosscuts 給完整 cyclic region 分解

一般式 p=a+c≥1，所以存在原 B–U edge。沿所有原 B–U edges 依原
rotation 切開 annulus，得到 cyclic disk regions。允許相鄰 crosscuts
共 endpoint；p=1 時同一原邊的兩個不同 sides 成為切開 disk 的兩界。

私人分量不能跨 crosscut。每個 region 的 BUP 面只能 incident 於其
兩個 bounding crosscut sides，每側至多一個，所以至多兩個。一個完整
私人分量已恰需兩個，故含私人點的 region 恰含一個完整私人分量，並在
兩端各有一個 BUP 面。不含私人點的 region 內既無 B–U edge，也無同環
chord，原三角化迫它恰是一個 BBU 或 BUU 原三角面。

因此全部原 regions，沒有遺漏，恰為 c 個私人 strips 與 a 個 terminal
triangles。每條 B/U 原環邊在 annulus 側恰屬一個私人 fan 或 terminal
triangle，所以環邊前進總量必分別精確為五。兩環用整數記進度、mod5
記 pin 名；不把提前繞回當作新的自由度。

## 3. 完整原私人 strip 的 atom 編碼

每個 strip 的 backbone 原點依序為 z0,…,z_s，s≥1。相邻 backbone
點由一個 atom 接合；atom E 是實際原邊，atom D/H 是實際 polygon
block。polygon endpoints 本身就是兩個 backbone 點；其他 polygon
點是各 atom 獨有的原點，沒有新增或刪去 source 點。

所有 polygon 頂點以原邊界次序 0,…,n−1 命名，起始 ear 是 0，終止 ear
是 q。B 側走 `0,1,…,q`，U 側走 `0,n−1,…,q`。以下列出完整 rooted
型；邊界原邊永遠全部存在，表中只列 diagonals。

| atom | n | q | diagonals | 類型 |
|---|---:|---:|---|---|
| D | 4 | 2 | 13 | diamond |
| H0 | 6 | 2 | 13,14,15 | fan，B 側短 |
| H1 | 6 | 3 | 14,15,24 | zigzag，一種相對次序 |
| H2 | 6 | 3 | 15,24,25 | zigzag，另一種相對次序 |
| H3 | 6 | 4 | 15,25,35 | fan，U 側短 |

CORE 的兩個 unrooted hexagon 型在指定起始 ear、指定 B 側後恰產生
上表四個 rooted 型。改選起始 end、共同反向或交換兩側，都仍在這四型
之內；沒有對 B、U 各自做不相容的獨立正規化。

令 E^t 表示 t 條實際原 bridge edges（t≥0）。完整 atom word 域為

* H strip：`E^t Hh E^u`，h∈{0,1,2,3}，t,u≥0。
* DD strip：`E^t D E^q D E^u`，t,q,u≥0。
* D strip：`E^t D E^u`，t,u≥0。
* P strip：`E^t`，t≥1。

DD 的 q=0 恰為兩 diamonds 共用同一 ear；q=1 是兩個不同 ears 之間的
一條原 bridge；更大的 q 逐點保留其內部 subdivisions。這些參數沒有
把 shared ear 誤當一條長度零但有兩個不同 endpoints 的邊。

全圖 component 類型只有 c=1 的 H 或 DD，以及 c=2 的 H+P、DD+P、
D+D。私人點數分別由 atoms 的實際 union 計算：E 增加一點，D 相較於
一個 endpoint 增加三點，H 增加五點；每條完整 strip 的初始點再加一。
因此 H 有6+t+u點，DD 有7+t+q+u點，D 有4+t+u點，P 有t+1點。

## 4. 字母與全部完整 degree 條件

在某個 backbone 原點 z 到達時，當前共向 pins 為 (b_j,u_k)。令字母
`O=(0,0), B=(1,0), U=(0,1), D=(1,1)`。z 一定接 b_j、u_k；某座標
為1時再接該環下一 pin，形成使用該環邊的原 fan triangle，然後更新進度。

若 z incident 於 e 個 E atoms、b 個 polygon atoms，原私人 degree
恰為 `d_F=e+2b`，其中 e+b 為1或2。全部允許 letters 由唯一條件

\[
d_G(z)=d_F(z)+2+\delta_B+\delta_U\ge5                 \tag{1}
\]

選出；兩個座標仍各至多1。逐型為

| backbone 原點 | d_F | 允許 letters |
|---|---:|---|
| strip end，只接 E（leaf） | 1 | D |
| strip end，只接 polygon（無尾 ear） | 2 | B,U,D |
| 兩個 E 之間 | 2 | B,U,D |
| E 與 polygon 之間（帶尾或連接 ear） | 3 | O,B,U,D |
| DD 共 ear | 4 | O,B,U,D |

DD 共 ear 的完整 degree 是 `6+δB+δU`，不是 `4+δB+δU`，也不是兩個
獨立 endpoint degree 的和。所有字母均在同一個原點、同一個原色框實現。

polygon atom 的每個非 backbone 原點 w 僅接其側的一個或兩個連續 pins。
以 bit δ=0/1 記它是否再接下一 pin。若其私人 degree 為 d，則

\[
d_G(w)=d+1+\delta\ge5.                                  \tag{2}
\]

因此 d=3 迫 δ=1，d=4、5 允許 δ=0或1。這裡的 `+1` 必須保留；私人
degree五的 apex 也至少有一個原 terminal 鄰點。每個 D 的兩側內點 degree
均為3，所以兩側各前進1。H0/H3 的長側三點各前進1，短側 apex 前進0或1。
H1/H2 的兩側各有一個 degree3 點、一個 degree4 點，依原順序各自取 bits。

完成 backbone 字母之後再走下一 atom：E 不另消耗環邊，polygon 按兩
段原 contour 的內點順序處理其 bit strings。這保留所有原 fan intervals，
而不是只保存兩側的總前進量或 degree marginals。

## 5. 全部 literal edges、faces 與 rotation 恢復

下面給一致有向面的通用規則。B 外面指定為 `(b0,b4,b3,b2,b1)`，U 空面
指定為 `(u0,u1,u2,u3,u4)`。

每個 strip 在起始 pins (b_j,u_k) 加起面 `(b_j,z0,u_k)`；終點處加末面
`(u_k,z_s,b_j)`。每個 backbone 字母的 B fan 面（若 δB=1）是
`(b_j,b_(j+1),z)`，U fan 面（若 δU=1）是 `(u_(k+1),u_k,z)`，然後
按字母更新 pins。E atom 的兩面是 `(b_j,z_next,z)`、`(u_k,z,z_next)`。

對 polygon atom，B arc 從 x 走向 y：每到內點 w，先加其前一條原邊
的外面 `(b_j,w,w_prev)`；若 bit=1，加 `(b_j,b_(j+1),w)` 並更新 j；
走完所有內點後加 `(b_j,y,w_last)`。U arc 亦從 x 走向 y，但依反向
polygon 次序：相應面為 `(u_k,w_prev,w)`、可選 fan 面
`(u_(k+1),u_k,w)`，及最後 `(u_k,w_last,y)`。所有 PPP polygon faces
按表中原三角化恢復，方向與頂點 0,…,n−1 的原環方向一致。

terminal triangle 的兩型分別是 `(b_j,b_(j+1),u_k)`（前進1,0）與
`(b_j,u_(k+1),u_k)`（前進0,1）。其兩條原 B–U edges 完整保留。

literal edges 就是上述有向面的全部無向邊，另含十條 B/U 原環邊。
沒有可漏掉的第五類原邊：原 A 邊全部屬於 B/U 邊、私人邊、私人–terminal
邊與 B–U 邊。補回中心 v 與五條原 spokes，以五個 `(ui,u_(i+1),v)`
原三角面取代空 U 面。

checker 應由 faces 驗證每個 dart 恰出現一次、反 dart 存在、每點的
link 是單一 cyclic rotation、連通與 Euler 特徵二；另重算原 B 外面、
原 U 空面、私人 components/degree、ρ=t_P=4、M=2c、p=a+c、所有私人
完整 degrees、每環附件界與總前進量(5,5)。抽象可平面嵌入不能代替指定
原 rotation。可保留其他來源条件未用盡的必要模板，但不能用無效嵌入模板
代替原來源。

## 6. 有限必要域的枚舉與完備性

依次列舉 c=1/2、上述全部 component 類型、所有非負 E 長度，使
`8≤r≤14−2c`；依 (1)(2) 列舉每個 backbone word 與 polygon bit strings。
取得私人 strips 的總 B/U 前進量 db,du，補入恰 `5−db` 個 B 型及
`5−du` 個 U 型 terminal triangles，要求兩者非負且總和
`a≤14−2c−r`。

保留所有私人 strips 的允許 cyclic 次序與所有 terminal triangle 次序。
可把第一個私人 strip 起始 cross edge 固定為 B0–U0，再於各私人 strip
之後放入任意 B/U triangle word；這涵蓋三角面在兩 strips 之前、之間、
之後的全部相對位置。對 c=2 同型 D+D 可保留重複表示，不依賴同構去重
正確性。最終每環總前進量必為五。

完備性的方向是從任意原來源讀出此組資料：CORE 先給唯一存活私人形狀；
§1 讀出兩側；§2 讀出完整原 region sequence；§3 逐點讀出 E/blocks；
§4 讀出所有實際 fan letters/bits；原環各五邊給進度條件。§5 再逐面
恢复同一原圖。因此有限域的覆蓋來自這個紙面反向構造；生成器零漏差的
核對只驗證程式是否實作此域，不是一般來源完備性本身。

## 7. 同一十 pins、完整 lifts 與保存強度

canonical pins 搬回原來源時保存

\[
g_B(i)=s_B+\varepsilon i\pmod5,\qquad
g_U(i)=s_U+\varepsilon i\pmod5,\qquad\varepsilon\in\{1,-1\}.
\]

兩環共享同一 ε，各自起點可以不同。若 U 的既有命名採面邊界方向，先
記錄它與此共向座標的固定換算，不得暗中獨立反 U。所有 backbone 點、
polygon 內點與中心 v 按原 contour 的同一份 bijection 映回；DD 共 ear
只映到一個原 cutvertex。這是具完整原 embedding 的同構，所以逐點搬運
同一固定四色框中的全部 A/G full lifts，保十 pins、中心色及所有空 fibres。

source-to-template 沒有減少頂點，也不提供任何縮減代表。有限 checker
若逐份證明完整補中心 Σ∈K132，即可直接反駁目錄外来源身份；相同 Σ
本身仍不能推出 R³ 等價。全部十列、空格與 full lifts 必須來自同一份
具名原圖及同一色框，不能拼接各自成功的 marginals。

本檔是原附件的紙面完備性證明；數量、完整染色證書、獨立 checker、
不同搜尋次序與負控制由 audit 的實際輸出另外承擔，沒有新增 Lean theorem。
