# 圈秩一的任意大小結構化約

BASE：`3097ef5be241b7777451a5ef8a663f3987d6b866`。本檔只在本次隔離包新增。
以下是紙面結構證明；有限染色核心及獨立重算另見本包 REPORT 的證據入口。
沒有把森林證明套在含環图上，也沒有假設私人圖連通。

## 1. 來源、上游依賴及森林信任邊界

固定全部目錄外 disk-C5 來源中先最小化內點數、再最大化邊數的 G。
令原有序外框為 B，取任意一個符合正式槽位契約的全內部 induced W5：
中心 v、原循環鄰點 U，B/U 十個 pins 不同，U 的內盤只有 v 及五條 spokes。
令 A=G−v、P=V(G)\(B∪U∪{v})、r=|P|、F=G[P]。

本證明只用下列已核對的最小來源結論：

1. G 是有限簡單二連通 disk 圖，B/U 都是 induced C5，A 的十條邊界邊之間
   全是三角面。來源內點數 k≥13，因此 r=k−6≥7。
2. 每個原內點的 **G 中完整度數** 至少五；特別是每個私人點的完整度數至少五。
   這不是 d_F≥5。事實上本證明最後的必要核心全是 d_F=2。
3. 每個原內點在 B 上至多有兩個鄰點，若兩個則相鄰。
4. 每個簡單 C4 的有界內部都沒有頂點。

來源為正式文檔
[`c5_cofacial_normal_form.md`](../../../docs/c5_cofacial_normal_form.md)、
[`c5_saturation_degree_bound.md`](../../../docs/c5_saturation_degree_bound.md)、
[`c5_degree5_link_reductions.md`](../../../docs/c5_degree5_link_reductions.md)。
第 3、4 項的具體上游紙面機制，另核讀
[`deep-five-wheel REPORT §§2,4`](../../2026-10-12-c5-deep-five-wheel-01a12ffa/REPORT.md)：
C4 cap 以完整關係代表及最小性先界 t≤3，再由完整 degree 與面數排 t>0；
若私人點接非相鄰的 B 點，短側 C4 被迫清空並使中間 B 點 degree 三，矛盾。
所以這裡沒有把任意環當作 clique separator，沒有新增 N2、edge-critical、
ε、兩 root 或 Gallai 前提。上游 K≤12 的外部定理及計算證書信任邊界保留。

第 4 項亦給 U 附件界：若 x∈P 接兩個不相鄰的 ui、uj，簡單 C4
`ui−v−uj−x−ui` 把 U 的兩條非空開弧分居兩側，有界側含 U 點，矛盾。
故每個私人點在 U 上也至多接兩個、若兩個則相鄰。以

\[
d_T(x)=|N_G(x)\cap(B\cup U)|
\]

記 terminal 度數，則 `d_T(x)≤4`，而 `d_G(x)=d_F(x)+d_T(x)`。
因此 F 沒有孤立點。若 d_F(x)=1，則恰有兩個 B、兩個 U 鄰點，且 d_G(x)=5。

已完整核讀前輪的 forest REPORT、独立 forest review，以及三色 support、
代表與 conditional REPORT。森林的紙面化約使用 `|E(F)|=r−c` 及沒有 PPP 面，
先得 `M=2c,p=a+c,r≤10−2c`，再得到七／八點單一路徑和完備 70 模板。
該結论依赖明列來源前提、原 rotation 分類與每模板完整染色重算；不是無界搜尋
推論。本輪不能沿用它的面式，因为圈秩一改變 `|E(F)|`，且可出現 PPP 三角面。
下節重新計數，並把此例外獨立處理。

## 2. 圈秩一的圖與幾何分解

假設 `ρ(F)=|E(F)|−r+c=1`，其中 c 計全部私人分量，包括原本可能的孤立點。
每個連通分量的圈秩非負，故恰有一個分量是單環圖，其餘分量是樹。
前節已由完整 degree 排除孤立點。記唯一簡單環為 C。

單環分量由 C 加上附在 C 各點的根樹構成：每個離開 C 的樹只能接一個 C 點，
且只經一條根邊相接，否則會多出一個環。其他私人分量是非平凡樹。
這是 **原誘導圖** 的分解，保留所有原樹邊；不是刪枝操作。

嵌入中的 C 是簡單 Jordan 環。B 全在其外侧；連通的 U 與 C 不交，故 U 全在
一側。只有以下兩種幾何：

* contractible：U 及 v 在 C 外，C 有界內部沒有任何 terminal。
* essential：C 分隔 B 與 U，U 及 v 在 C 有界內部。

任何通向 B/U 的原附件都必須留在其端點所在的 C 側，不得穿過 C。
尤其 essential 時沒有 B–U 邊。兩側的染色接合在 §7 明確保留同一完整 C 指派。

**contractible 的內側必為空。** 若有私人點嚴格在 C 內，該側每個離開 C 的
根樹有一個非根 leaf；完全位於內側的另一樹分量亦有 leaf。它無法跨 C 接 B/U，
也不能多接另一個 C 點，否則破壞圈秩一。故此點的完整 degree 至多一，矛盾。
沒有內點後，C 也不能有 chord，否則 F 多環。C 內側因此是一個原面；由原內面
三角化，C 恰為一個 facial C3。

令 h 是全私人三角面數。任何這樣的面給 F 的一個 cycle，故必是唯一 C。
上述兩分支精確給出

\[
h=1\quad\text{(contractible)},\qquad h=0\quad\text{(essential)}.
\]

essential 中即使 C 本身長三也不可能是三角面，因它內側有 U/v；沒有另外的
私人三角形。後面會直接得到 |C|≥7，不需在此借用 C5 separator 界。

## 3. 原面與完整 degree 的重新計數

令 p 為 B–U 邊數，a 為只有 terminal 的 annular 三角面數，M 為恰有
一個 B、一個 U、一個 P 的三角面數。B/U induced C5 保證全 terminal 面
只有 BBU 或 BUU 型，各有一條原環邊及兩條 B–U 邊。

A 有 r+10 點、十條邊界邊，所有 annular 面三角化。Euler 及面長總和給

\[
e(A)=3r+20,\qquad t(A)=2r+10,\qquad e(F)=r-c+1.       \tag{1}
\]

每條私人邊兩側各有一個 annular 面。恰有兩個私人點的三角面數故為
`2e(F)−3h`。十條環邊各在 annulus 側有一面，其中 a 條屬於全 terminal 面，
餘下 `10−a` 面各有一個私人點及兩個同環 terminal。合計全部面得

\[
2r+10=h+(2e(F)-3h)+(10-a)+a+M,
\]

從而

\[
\boxed{M=2(c-1+h).}                                  \tag{2}
\]

再數 B–U 邊的兩側：每個 a 面使用兩條，每個 M 面使用一條，故

\[
2p=2a+M,\qquad\boxed{p=a+c-1+h.}                     \tag{3}
\]

terminal–P 邊共有 `e(A)−10−p−e(F)=2r+9+c−p`。所以完整私人 degree 總和為

\[
\sum_{x\in P}d_G(x)=2e(F)+(2r+9+c-p)=4r+11-c-p.
\]

套用的是原完整 degree≥5，得到

\[
\boxed{r\le11-c-p=12-2c-a-h.}                        \tag{4}
\]

這些式子涵蓋所有分量、樹枝及兩種環位置，沒有先限制私人點數。

## 4. contractible 分支的紙面排除

先記一個局部事實：私人 leaf x 的唯一私人鄰點，在原 rotation 中刪去後，
剩下四個 terminal 鄰點形成一條 link 路徑。它有兩個 B 與兩個 U，故至少一對
相鄰項一個在 B、一個在 U。因 G 內面三角化，這一對與 x 給一個 M 面。
不同私人點所給的 M 面不同，因每個 M 面只有一個私人點。

contractible 時 C 是空 facial triangle，h=1，式 (2) 要求 `M=2c`。
對三個 C 頂點分别作如下計帳：

* 若該點 x 沒有離開 C 的私人樹枝，則 d_F(x)=2；完整 degree≥5 迫至少三個
  terminal 鄰點。每環至多兩個，故 B/U 皆出現。C 的兩條 incident edges
  在 C 內侧夾成 facial triangle，所有 terminal 鄰點都沿另一側同一 link 路徑
  排列。因此有相鄰的異環 pair，給一個以 x 為私人點的 M 面。
* 若 x 有私人樹枝，任取一根。該有限根樹有非 C leaf y；依局部事實，y 給
  一個 M 面。不同 C 頂點的根樹不相交，所取 leaves 不同。

三個 C 頂點因此供應 **三個不同的 M 面**，不要求樹枝可刪、可縮或保關係。
另外每個非環私人樹分量至少有兩個 leaves，總共再供應至少 `2(c−1)` 個不同
M 面，且與前三個不重複。所以

\[
M\ge3+2(c-1)=2c+1>2c,
\]

與面式矛盾。

**結論 C：在來源完整前提下，私人圖圈秩一且唯一環 contractible 不可能。**
這是任意大小、任意分量數、任意樹枝的純紙面排除；沒有代表、没有借用有限染色
搜尋。任取符合槽位前提的 W5 都適用。亦未將任意 cycle 当作 clique separator。

## 5. essential 分支只有七至十點純環

C 分隔 B/U，因此 p=0；且 h=0。式 (3) 給

\[
0=a+c-1,
\]

所以 `a=0,c=1`：原 F 已連通，其他樹分量全部排除。式 (2) 再給 `M=0`。
若單環分量還有私人樹枝，就有私人 leaf；§4 的局部事實給一個 M 面，矛盾。
因此 **全部私人圖恰等於唯一 essential cycle C**，沒有枝或其他分量。

由 (4) 及 r≥7，得到

\[
\boxed{F=C_r,\qquad7\le r\le10,\qquad p=a=M=0.}       \tag{5}
\]

所有原 annular 邊均屬 B/U/C 三條環，或 B–C、U–C attachments；
沒有 B–U 邊、C chords、私人分支或隱藏接點。每個 x∈C 的完整 degree
為 `2+d_T(x)`；其兩侧分别接 B/U，且每側接一或兩個相鄰 pins。

## 6. 1652 個循環詞的完整嵌入覆蓋

此節提供可查驗的完備分類，不以有限搜尋猜範圍。
沿原 C 記頂點 `x0,…,x_(r−1)`，並固定繼承自 annulus 的方向。

每条 C 邊在 B 側與 U 側各有一個三角面。第三點必分别在 B、U：
沒有其他私人點可形成額外 PPP 面，也沒有跨 C 的原邊。因而每個 x 在每側
至少有一個 terminal 鄰點；前述附件界又使每側至多兩個，且若兩個則相鄰。

在 x 的 B 側 link 中，從前一條 C 邊的 third vertex 走到下一條 C 邊的
third vertex：若只有一個 B 鄰點，位置不變；若有兩個，恰沿 B 的一條原邊
前進。U 側同理。原面方向固定前進方向，不能獨立反向或跳接。
每一原 B/U 邊在 annulus 側只有一個面；又 a=0，所以它必且只能由某個 x
的這種二鄰點 fan 使用。故每側在走完 C 一周時，**恰依原順序使用五條環邊
一次**，沒有倒退、重複、漏邊或額外繞行。

將 x 的兩側前進數記為 `(dB,dU)`。每個值在 `{0,1}`，而
`d_G(x)=4+dB+dU≥5`，故只允許三種 letters

\[
X=(1,0),\qquad Y=(0,1),\qquad Z=(1,1).
\]

環的一周滿足 `ΣdB=ΣdU=5`，所以三種 letters 數量精確為

\[
(n_X,n_Y,n_Z)=(r-5,r-5,10-r).                         \tag{6}
\]

全部必要詞可保留首點冗餘，不必作同構去重：

| r | `(nX,nY,nZ)` | 全部 linear words 數 |
| --- | --- | ---: |
| 7 | `(2,2,3)` | 210 |
| 8 | `(3,3,2)` | 560 |
| 9 | `(4,4,1)` | 630 |
| 10 | `(5,5,0)` | 252 |
| 合計 | | 1652 |

**全部原邊與面重建。** 指定 word、原 x0、B/U 起始 third vertices，即可逐步
恢復所有原 attachments：初始狀態 `(j,k)=(0,0)`；第 i 步在 B 接
`b_j`，若 dB=1 再接 `b_(j+1)`；在 U 接 `u_k`，若 dU=1 再接
`u_(k+1)`。所有 indices mod 5。更新 `(j,k)←(j+dB,k+dU)`；
每條 `x_i x_(i+1)` 两侧的 third vertices 為更新后的 `b_j,u_k`。
在共向環座標下，對應定向面可取

```
(b_j,b_(j+1),x_i)        when dB=1, before update
(u_(k+1),u_k,x_i)        when dU=1, before update
(x_i,b_j,x_(i+1))        after update
(x_i,x_(i+1),u_k)        after update
```

再加指定的反向 B 外面及正向 U 空內面。這給 `10+2r` annular 三角面及
`3r+20` 邊，已達 Euler 所需全部面／邊，沒有未記錄邊可另加。
每個字母都由相鄰原面推導，故原 rotation 與全部 attachments 已由此恢復。

此分類只要求**覆蓋來源**。其中有些詞可违反尚未用到的其他最小來源條件，
不影響在較大必要域證排除。有限核心必對以上全清單核對實際面、dart、rotation、
B 外面與 U 空內面，而不能只測抽象平面性。

**搬回原 pins。** 起始 third vertices 可分别平移 B/U 的起點。共同方向固定後，
canonical-to-original maps 為 `gB(i)=sB+εi`、`gU(i)=sU+εi`，indices mod 5；
若反向遍歷整個嵌入，兩側 ε 必同時改變。不得把只反轉 U 當自由同構。
原 C 點依實際環次序映回，中心映回 v。使用者給定的原 pin 順序若以相反的
邊界面方向記錄，須先保留該記錄與本節共向座標的顯式對照，不能暗改原順序。
此為整個帶嵌入圖的重標記，沒有獨立換色或丟棄 attachments。

## 7. 同一 C 指派的完整兩層接合

必要核心幾何分成 B–C 與 C–U 兩層。令 σ 是 C 的完整 literal 四色 tuple；
兩層圖分别為外層 L、內層 I，均保留全部原邊及所有原 pin labels。
對固定 `(β,τ)`，完整 A fibre 有精確分解

\[
J_A(\beta,\tau)=
\bigsqcup_{\sigma\in\{0,1,2,3\}^{r}}
J_L(\beta,\sigma)\ \Join_{\sigma}\ J_I(\sigma,\tau).  \tag{7}
\]

此處兩側必使用同一 σ，且重複的 C 色只保留一份；沒有私人枝或其他分量需要
省略。左右若只各自存在某個 σ，其 marginals 不足以證明同一接合非空。
有限 checker 可以直接枚舉完整 A/G，而無須以 (7) 作計算；若使用 transfer，
必保留上述同一 σ 的 joint。

原 word 與原圖間是完整圖同構，因此其染色搬運是逐點 relabel 的真正雙射，
不是私人縮減。不論有限核心最後給何種 Σ，都須先由這個共同 label map
搬回原 B；若全收十列則任意 D5 搬回仍全收十列。

## 8. 有限核心結果、保存強度與採納

本包主生成與獨立完整探索均已核對全 1652 詞，全部補中心後 `Σ=1023∈K`。
共保存 16,916,480 個 named cells，其中 16,448,400 格為空；完整 A/G lifts
分别為 657,580／320,840。正式逐證書比較、normal/seed17 與負控制結果以
[`../controls/summary.json`](../controls/summary.json)、
[`../independent/verification.json`](../independent/verification.json) 及父 REPORT 為準。

因此每個可能 essential 來源的完整 Σ 亦為 1023，和來源目錄外身份矛盾。
與 contractible 紙面排除合併後，即得

\[
\boxed{\text{任意合法全內部 induced W5 均有 }\rho(G[P])\ne1.}
\]

再接既有完整森林排除，即得 `ρ(G[P])≥2`。有限 kernel 的數目不是普遍量詞
來源；普遍性来自 §§2–6 的任意大小、所有分量與原嵌入完備化約。

上述 source-to-word 改名保留全部 full lifts，是完整圖同構，沒有減少內點。
另有只保補中心後完整 Σ 的 r′=0 同槽位 prism 代表，及 r=7,…,10 到 r′=0
的嚴格縮減，詳見 [`REPRESENTATIVE.md`](REPRESENTATIVE.md)。兩種搬運不可混為
一談：word 同構保全部 pins 及 lifts；prism 替換只保原 B。

若只比較補中心後外框關係，正確目標是 `pr_B R_A³`；若另宣稱保持 R³，則必
逐 `(β,τ)` 保留三色 named cells 並交付雙向 total 搬運。兩者不能在計算或
結論中混用。上述有限排除只需要完整 capped Σ，全 fibres 的保存用於核對與
反控制，沒有從相同 Σ 反推相同 R³、fibre 重數或可逆私人 assignment。

真正最小 933／941 來源仍是 `not triggered`。本紙面化約不構造這種來源，
也不從零 triggers 推排除。沒有新增 Lean theorem；本任務未證一般私人含環
來源有 r≤6 代表，未證 K∞=K≤5。
