# W5-RANK3-C：原 rotation 的完備 fan-strip 附件域

固定 BASE `50d5474f2446403f3b3001d5943571184c8c9936`。本檔只處理
contractible ρ(F)=3。一般面式、c≤2 及完整私人核心分類分別由本目錄的
前提／結構證明承擔。本節使用其已證結論：唯一含環私人分量由一個三角化
五邊形 block、其兩個 ears 各接一條可空原路徑構成；其餘 c−1 個分量是
非平凡原路徑。兩個 fan 分量末端及每個其他 path 的兩末端各供應恰一個
BUP 面，用盡 M=2c；其餘私人點沒有 BUP 面。所有原橋、附枝及 cut vertices
都保留在上述實際圖內，沒有按顏色可縮性刪去任何點邊。

## 1. 原 contour、兩個切換及兩側附件

沿一個私人分量的無界 facial contour 走一周；每條 bridge 按其原兩側各走
一次。在相鄰兩個私人 darts 之間，所有原 terminal 鄰點形成一個 link 區間。
原 annular 面均為三角面，所以區間中相鄰 terminal 必以原邊相接。一對相鄰
terminal 屬於不同環，恰給一個 BUP 面；同環的相鄰 terminal 必是該環的
相鄰 pins。每條私人邊的非 PPP 側由其 incident 原面的第三點標記為 B 或 U。

每個分量恰有兩個 BUP 面，且位於上述兩個末端。因此 contour 只切換兩次，
兩次之間的兩段分別全是 B 側及 U 側。若某個非末端點的兩個私人 darts
夾成原 PPP 面，該 sector 沒有 terminal，不應計作新的切換。對其餘 sector，
相鄰三角面的第三點在同一環內依原邊順序連接，故不能跳 pin、倒退或單獨
反轉某一環。

將三角化五邊形的兩 ears 記作 x,y，唯一私人 block-degree 四點記 z；另兩點
記 w,t，使其外 contour 的兩條 x–y 弧分別為 `x-z-y` 與 `x-w-t-y`。
完整 block 原邊恰為

```
xz, yz, zw, zt, xw, wt, ty.
```

三個原 PPP 面是 xzw、wzt、tzy（方向見 §4）。短弧及長弧必落在兩個不同的
terminal 側。沒有在這一步把 B/U 附件獨立重定向。現令 `apex=B` 表示短弧
在 B 側；`apex=U` 表示短弧在 U 側。

z 不接私人附樹，其完整 G-degree 是 `4+d_T(z)`。它只有一個外側 link 區間，
且沒有 BUP 面，故全部 terminal 鄰點在短弧一側的同一環。完整 degree≥5
迫至少一個；每環附件界迫至多兩個，兩個時相鄰。因此 z 的 fan 消耗
`apex_step∈{0,1}` 條該側原環邊。w、t 各只有三個私人鄰點，亦各只接長弧
一側的同一環。完整 degree≥5 與附件界迫各恰接兩個相鄰 pins，所以長弧
依次消耗兩條原環邊。w、t 在原邊 wt 的同側三角面共享其第三 terminal；
因此兩次前進是連續的，不能各自選擇獨立起點。

帶尾的 ear 有三條私人邊，分別在兩個外側 sectors 接 B/U；無尾的 ear 有
兩條私人邊，外側 link 含其唯一 BUP 切換。兩種 ear 均在兩環各至少接一個
pin，至多兩個相鄰 pins。普通 path 的 internal 點亦分別在兩側接 B/U；
私人 leaf 的完整 degree 迫恰接每環兩個相鄰 pins。這包括每條 bridge 的
正反兩側，未將它只記一次。

## 2. B–U 原 cross edges 切成完整 cyclic region sequence

一般式給 `p=a+c≥1`。每條 B–U 原邊是一條 annulus crosscut。先沿其中一條
切開 annulus，再沿其餘 cross edges 依原 rotation 的順序切開，得到依序
相接的 disk regions。允許相鄰 cross edges 共端點；p=1 時同一原邊作切開
盤的兩個不同邊界側。每個 region 的其他邊界是原 B/U 的前進子弧，其內部
沒有 B–U 邊。

私人分量不能越過 cross edge。某 region 的 BUP 面只可能 incident 於其
兩個 bounding cross-edge sides，每側至多一個，所以合計至多兩個。一個
私人分量已恰供應兩個 BUP 面，因此含私人點的 region 恰包含一個完整私人
分量，且兩個 bounding sides 各供應其一個 BUP 面。

若 region 不含私人點，則它沒有內部 B–U 邊，也沒有同環 chords（原 B/U
均 induced）。內部無任何可供三角化的點邊，所以該 region 本身恰為一個
BBU 或 BUU 原三角面。由此全部 regions，無一遺漏，依循環原順序組成：

* 一個 pentagon-fan strip；
* c−1 個非平凡 path strips；
* a 個全 terminal triangles。

沒有假定原圖已符合方便的 strip 編碼；strip 結論來自原 crosscuts、面预算
及原面三角化。各 B/U 原環邊在 annulus 側只有一個 incident 面，必恰由
上述某個私人 fan 或 terminal triangle 使用一次。故全 region sequence
在 B/U 兩環各前進精確五條邊。

## 3. 完整必要參數與所有 degree 條件

从 fan-strip 起始 cross edge 開始，記當前共向 pins 為 `(b_j,u_k)`；canonical
起點取 `(j,k)=(0,0)`，但保留 §5 的原 pin map。indices 取 mod 5，前進量
用整數累計，不把提前閉合視為額外自由度。

用字母 `O=(0,0), B=(1,0), U=(0,1), D=(1,1)` 記私人點在兩環的前進量。
一點先接兩環當前 pin；某座標為 1 時再接該環下一 pin，形成使用那條
原環邊的原三角面。接完後按字母更新 j,k。

fan 分量的 backbone 為 `z0,…,z_(s−1)`，s≥2；選
`gap∈{0,…,s−2}`，兩個 gap 端點是 x=z_gap、y=z_(gap+1)。這兩點之間
**沒有**原邊 xy；以 §1 的三個額外點及七條原 block 邊取代。其餘 backbone
相鄰點都有原 path 邊。fan 分量私人點數是 s+3。

| backbone 點 | d_F | 允許字母 |
|---|---:|---|
| endpoint，非 gap ear（leaf） | 1 | D |
| endpoint，同時為 gap ear | 2 | B,U,D |
| internal，非 gap ear | 2 | B,U,D |
| internal，同時為 gap ear | 3 | O,B,U,D |

表中每列是完整 degree `d_G=d_F+2+δB+δU≥5` 的直接等價式，並非私人
degree≥5。走過 gap 時，額外前進 `(apex_step,2)`（apex=B）或
`(2,apex_step)`（apex=U）。短弧頂點 degree 為 `5+apex_step`，長弧兩点各
完整 degree 五。

其他 path strip 的點数 t≥2，兩 endpoints 強制 D，internal 點為 B/U/D；
它沒有 gap，也沒有額外前進。terminal triangle B／U 分別前進 (1,0)／(0,1)。

完整參數域如下，允許重複描述而不依赖同構去重：

1. c=1：7≤r≤11；c=2：7≤r≤9。
2. c=1 時 t=0；c=2 時 `2≤t≤r−5`，fan backbone 長 `s=r−t−3≥2`。
3. gap 全部 s−1 個位置；backbone 全部符合上表的字；apex=B/U；
   apex_step=0/1；如有另一 path，取其全部合法字。
4. 計算所有私人 strips 在兩環的前進量 db,du。補入 `ab=5−db` 個 B 型及
   `au=5−du` 個 U 型 terminal triangles，要求 ab,au≥0，且
   `a=ab+au≤13−2c−r`。
5. fan 後全部 B/U terminal triangles 與另一個 path（若有）的每種排列。
   每次以一個 strip 或一個 triangle 逐原面前進，最終總前進量恰為 (5,5)。

此域不對尚未用到的完整 U-degree、小 cap 或其他來源條件作額外篩選。
故其中可能有不是最小來源的必要模板；每份模板仍必通過實際指定嵌入、
私人完整 G-degree、附件及面式核對。普遍覆蓋先來自上述原圖推導，r≤11
只是已證大小界，不是憑方便挑選有限圖的理由。

## 4. 全部 literal edges 與原定向面重建

以 B apex 為例，gap 前當前 pins 是 `(b_j,u_k)`，令 α=apex_step。gap 的
非 PPP 原面精確為

```
(b_j,z,x), (b_(j+α),y,z),
(u_k,x,w), (u_(k+1),w,t), (u_(k+1),u_k,w),
(u_(k+2),t,y), (u_(k+2),u_(k+1),t),
```

若 α=1，另有 `(b_j,b_(j+1),z)`；三個 PPP 面是
`(x,z,w),(w,z,t),(t,z,y)`。走完更新 `(j,k)←(j+α,k+2)`。
U apex 由對調上述兩側 terminal 環、並將 **每份 gadget 面整體反向** 得到；
不得只改 U pins 或只反指定 U 面。

每個普通 backbone/path 點的兩個同環 fan 面（若相應 letter 座標為 1）是
`(b_j,b_(j+1),z_i)` 與 `(u_(k+1),u_k,z_i)`。更新字母後，普通 path 原邊
`z_i z_(i+1)` 的兩面是 `(b_j,z_(i+1),z_i)`、`(u_k,z_i,z_(i+1))`。
每個 strip 的起面是 `(b_j,z0,u_k)`，末面是 `(u_k,z_last,b_j)`。
terminal triangle 兩型為 `(b_j,b_(j+1),u_k)`、
`(b_j,u_(k+1),u_k)`，並作相應前進。

最後指定 B 外面 `(b0,b4,b3,b2,b1)` 及 U 空面 `(u0,u1,u2,u3,u4)`。
原 A 邊只能屬於十條 B/U 邊、私人邊、private–terminal 附件、B–U edges
四類；前述所有面逐類恢復全部四類，沒有可隱藏的原邊。補中心後另加 v
與五條原 spokes，以五個 `(ui,u_(i+1),v)` 三角面取代空 U 面。

主 checker 逐圖驗證每個 facial dart 恰出現一次、反 dart 存在、每個 vertex
link 是單一 cyclic rotation、連通及 Euler 特徵二。另重算所有 literal
edges、私人連通分量、degree、`ρ=3,t_P=3,M=2c,p=a+c` 及
`Σd_G(P)=4r+13−c−p`。因此「可抽象平面嵌入」不能替代本輪原 B 外面、
原 U 空面及完整 rotation 的要求。

## 5. 同一原圖、同一色框下的 pin map 與關係

對每份來源，在原 rotation 選 fan 的起始 cross edge、共同方向及兩環起點。
完整 canonical-to-original maps 是

```
g_B(i)=s_B+εi mod 5,    g_U(i)=s_U+εi mod 5,    ε∈{+1,−1}.
```

兩環用同一 ε，各自起點可不同。若原 U 順序按 boundary-face 方向書寫，
先保存該方向與此共向座標間的固定換算，不可暗中只翻 U。私人點依實際
backbone、gap block 及其他 path 次序映回，中心映回 v。

source-to-template 因此是完整具名帶嵌入圖同構；它逐點搬運同一固定四色框
中的所有 A/G full lifts，保留十 pins、中心與所有空 fibres。所有 B/U 色列
都在同一份來源及同一 palette 下計算。這個同構不是嚴格縮減代表，也不代表
若另一圖恰有相同 Σ 就有相同 R³。模板檢查直接枚舉完整 A 與完整補中心 G，
不拼接兩個各自成功但共享 pins 不同的 marginals。

有限計算結果、縮減（若有）及其保存強度由本輪 REPORT、完整證書及独立
核對明列；本檔自身提供必要參數域的覆蓋及原邊／原面恢復證明。
