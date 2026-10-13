# 最小目錄外來源的 annulus 私人部分不可能是森林

2026-10-13。BASE `19209f4cf68261fdce5e84a7804cfe04ae0957bf`。
這是本輪新增的**來源條件性排除**；不是任意 annulus 的小代表定理。
上游輸入由 [INPUTS](../INPUTS.json) 凍結，最小來源的前提取自
[全內部五輪](../../../docs/c5_degree5_link_reductions.md)。

## 1. 定理及精確來源

假設存在完整外框關係不屬於 K 的 disk C5 來源。在全部這類來源中，先最小化
內點數 k，再最大化邊數，得到 G。取上游保證的任一全內部 induced W5，中心 v，
原循環鄰點 U=(u0,...,u4)，原外框 B=(b0,...,b4)。設

\[
 P=V(G)\setminus(B\cup U\cup\{v\}),\quad r=|P|=k-6,
 \qquad F=G[P].
\]

**FOREST-EXCLUSION：F 必含有環。**

這對每個符合原槽位前提的全內部五輪成立，不只對某個重新選取的輪成立。
因此後續針對真正最小 933／941 來源的 annulus 替換，可排除「私人 induced graph
為森林」整類，包括任意多分量、任意大小樹與分支樹；不必先假定私人點數有界。

使用的已知前提恰為：k≥13、G 的內面三角化、B/U 均 induced 且不交、U 內恰有 v、
原內點 degree≥5、沒有 occupied triangle 或 occupied C4，以及原內點不接兩個
不相鄰 B 點。它們来自全域最小來源及既有十二內點界，不能移植到 edge-critical、
N2 或任意 Σ-飽和圖。沒有使用來源的 Gallai／degree-list 身份。

## 2. 森林假設給出的無界到有界化約

反設 F 為森林，c 為分量數。r≥7，所以 c≥1。令 p 為原 B–U 邊數，
a 為 annulus 中沒有私人點的三角面數，M 為恰含一個 B、一個 U、一個 P 的面數。

每個私人點至多接兩個 B，且若有兩個則相鄰。U 亦如此：若私人點 x 接非相鄰
u_i,u_j，C4 `u_i-v-u_j-x` 的內側 spokes 與外側 x 路徑，把 U 的兩段非空開弧
分居兩側。其有界內側至少含一個 U 點，違反 occupied C4 排除。
因此任何私人點的 terminal 鄰點至多四，F 沒有 isolated vertex。

annulus 有 r+10 個頂點，十條邊界邊，全部 annular faces 為三角形。Euler 給

\[
 e=3r+20,\qquad t=2r+10,\qquad |E(F)|=r-c.
\]

森林無全私人三角形，每條 F 邊的兩側各有一個「兩私人、一 terminal」面，
所以這類面共有 2(r-c)。若 x 是恰一私人點的面數，則

\[
 x-M+a=10,\qquad M+2a=2p,\qquad t=2(r-c)+x+a.
\]

第一式按十條環邊計數；全 terminal 三角形恰含一條環邊和兩條跨環邊。
第二式按跨環邊兩側計數。消去 x,t，得到

\[
 \boxed{p=c+a\ge c,\qquad M=2c.}
\]

私人 degree 總和又是

\[
 \sum_{z\in P}d_G(z)=4r+10-c-p\ge5r,
 \qquad r\le10-c-p\le10-2c.                 \tag{1}
\]

任一私人 leaf 有一個私人鄰點，故必有兩個 B 鄰點、兩個 U 鄰點，degree 恰五。
在其五鄰點旋轉中，一個私人鄰點至多隔開一次 B/U 轉換，另一次給一個 M 面。
每個樹分量至少兩個 leaves，不同 leaves 給不同 M 面，而 M=2c。因此每個分量
恰有兩個 leaves，必為路徑，且其他私人點不貢獻 M 面。

由 r≥7 和 (1)，c=1，且數值僅可能為

| r | p | a | 私人 degree 超過五的總額 |
|---:|---:|---:|---:|
| 8 | 1 | 0 | 0 |
| 7 | 1 | 0 | 1 |
| 7 | 2 | 1 | 0 |

這一步已將任意大小的私人森林來源嚴格化成七／八點單一路徑；沒有用有限搜尋
猜測上述界。獨立推導見 [forest review](../conditional/forest_review.md)。

## 3. 保原旋轉的 70 個完整模板

把唯一私人路徑按原圖標為 x0,...,x_(r-1)。每條路徑邊的兩側各有一個 terminal
面頂點。沿任一側前進時，第三點不可能從 B 換到 U：這會在中間私人點的 link
遇到 B–U 邊，產生已排除的非 endpoint M 面。端點的唯一 M 面則迫兩側一邊是 B，
另一邊是 U。故路徑兩側的 ownership 全程固定。

每個內部路徑點在各側有一或兩個 terminal 鄰點；若有兩個必沿該原環相鄰。
原環邊在 annulus 側只有一個面，於是每側沿其環走過的邊既不能重複也不能倒退。
每個私人點可記成一步 `(dB,dU)`，其中 dB,dU∈{0,1}。
兩端各為 `(1,1)`；內部因 degree≥5，僅有 `(1,0),(0,1),(1,1)`。

p=1 時唯一跨環邊兩側的面由兩個 endpoints 所有，兩側各完整走過五條原環邊。
p=2 時 a=1，兩條跨環邊必和一條 B 或 U 邊形成唯一全 terminal 三角形；
路徑端點各接其一側。相應環已有一條邊由該三角形占用，故路徑只走四條，
另一環仍走五條。這給出以下全部必要詞：

| 模板 | 中間步數及多重集 | 數量 |
|---|---|---:|
| p=1,r=8 | 3×(1,0), 3×(0,1) | 20 |
| p=1,r=7 | 2×(1,0), 2×(0,1), 1×(1,1) | 30 |
| p=2,r=7，B 三角面 | 2×(1,0), 3×(0,1) | 10 |
| p=2,r=7，U 三角面 | 3×(1,0), 2×(0,1) | 10 |

端點及環步序決定全部原邊與全部面：每個前進的環邊配當前私人點；每條私人
路徑邊配兩側當前 B/U 點；再加兩個端點 M 面及可選的全 terminal 三角面。
Euler 邊數已滿，無未記錄邊可另加。這證明 70 模板覆蓋森林假設的全部必要情形。
有些模板仍可能違反其他來源前提；此處保留它們，擴大核對域不影響排除。

模板索引使用 B/U 起點平移及必要的方向搬運，把被選跨環邊或三角面移到位置零。
這是**整個嵌入圖的具名同構**，不獨立正規化顏色；實際來源須同時保留逆 label map、
原旋轉及原私人路徑次序。每個模板的證書仍固定 B=0..4、U=5..9 並保存全部 literal
fibres。下面全部十列皆接受，所以無论原 B 的起點／方向為何，搬回後仍全收十列；
無須把不同 U 關係視為相同，更不會拼接不同模板的 witnesses。

## 4. 有限核心的完整核對

[checker](check.py) 直接生成上述所有多重集排列及其定向面表；核對每條 dart
恰一次、每點 rotation 單一循環、連通與 Euler characteristic 2。B 為原外面，U
為空內面；每條環邊、私人邊與接線都來自該模板，沒有只測抽象平面性。

對每圖、每個原 B 十列，直接枚舉全部 H=G−v lifts，分入所有 1024 個 U cells，
包括空格。U 恰三色者補其唯一缺色到中心；再與直接 G DFS 的完整 lifts 逐份比較。
全部結果為

\[
 \boxed{\Sigma(G_{\rm template})=1023\quad\text{for all 70 templates}.}
\]

完整證書 [certificate.json.gz](certificate.json.gz) 及 [summary](summary.json) 保存
716,800 cells、701,956 個空 cells、18,282 份 H lifts 及 9,308 份 G lifts。
每圖都有全部十列的實際完整延伸，不只是不存在 933／941 的 aggregate 搜尋數。
獨立程式與理論核對另见 [independent review](../t1/forest_independent.md)。

因此任意假定的森林來源由 §2–3 落在上述完整必要域，§4 給其原框關係 1023∈K，
和目錄外身份矛盾，完成 FOREST-EXCLUSION。一般性來自 §2–3 的紙面完備化約；
有限 DFS 只負責已證足夠的 70 個 kernel，並未提升任意有限圖搜尋為普遍結論。

## 5. 重播與沒有排除的範圍

```bash
python3 -B audits/2026-10-13-w5-three-support-19209f4c/forest/check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-w5-three-support-19209f4c/forest/check.py --check
```

紙面結論是 `conditional source exclusion`；70 個 literal graphs 為
`triggered and holds`；它們不是最小目錄外來源，真正 933／941 source 為
`not triggered`。沒有新 Lean theorem，沒有重跑上游外部計數證明。

本結果不構造保持三色具名 support 的一般 r≤6 代表，亦不主張模板可換成某個
同 support 的 r≤6 annulus。留下的私人圖含環；可能是 contractible facial cycles，
不能逕稱有 essential cycle。來源專用的 cyclic-private annulus 壓縮、改動更大
區域、其他合法 full-lift 縮減，以及一般 K∞=K≤5 均仍 OPEN。
