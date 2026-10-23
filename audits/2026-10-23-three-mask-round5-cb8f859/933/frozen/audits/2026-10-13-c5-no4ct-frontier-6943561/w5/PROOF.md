# 無四色定理前提：小 cap 與全內部 induced W5 的接入

2026-10-13。固定 BASE `6943561e644e7598342d1ccd7df44dac0ebcd5cf`；輸入
由本包 [INPUTS](../INPUTS.json) 凍結。本證明只把既有小 separator／全內部
五輪的結構結果接到新的 932／933／941 全域最小來源契約，不新增一般來源排除，
不引用四色定理，也不沿用舊普遍 C4 代表定理。

## 1. 精確來源與已取得前提

K 是 132 個具體完整 C5 關係及其至多五內點 witnesses。若有目錄外來源，
在所有有限簡單 plane disk-C5 圖中，先最小化原框 B=(b0,…,b4) 內點數 k，
再最大化邊數，取 G；原始圖類容許 chords 及不連通。

使用已去除 4CT 前提的 [度數接入](../frozen/audits/2026-10-13-c5-no4ct-degrees-6cafdfb/REPORT.md)
及 [完整外圈接入](../frozen/audits/2026-10-13-c5-no4ct-collar-6cafdfb/REPORT.md)：
G 簡單、二連通、B induced、內面全三角，k≥16；每個原內點完整 degree≥5，
每個 B 點 degree≥4，沒有 occupied triangle。共同搬運整圖與原色框後，
完整關係屬於 {932,933,941}。以下推導不使用 singleton support 非空，故包含 932。

唯一使用的 C4 代表引理是：**C4 disk 若有 s<k 個私有內點，則其完整有序
C4 延伸關係有至多三內點的合法 disk 代表。** 對任何少於 k 內點的 C5
disk，則由全域最小性，其完整關係在 K，有至多五內點的代表。
這兩條量詞均保留嚴格大小限制；不能提升成任意大小代表命題。

## 2. 原 C4／proper C5 的 cap 確實較小

取 G 的原簡單 cycle C，長四，或長五且 C≠B。其有界側是原 disk 中不含
B 外面的那一側，s 為嚴格位於該側的原點數。因 B induced，只有 B 本身
才可能是僅用 B 點的五環，B 點亦不能形成四環。因此 C 至少有一個原內點
位於介面。若 i(C)=|V(C)\B|，則

\[
i(C)\ge1,\qquad s\le k-i(C)<k.                         \tag{1}
\]

故 C4 可實際使用受限三內點代表，proper C5 可使用 K 的五內點代表。
替換保留每個介面原點及順序；補圖中的每份 literal 介面色列能跨一側填充，
當且僅當能跨另一側填充。兩邊使用同一顏色名稱；平行的介面邊僅簡化重複，
不識別不同介面原點。於是原 B 的完整 Σ 不變。若代表有 s′ 個私有內點，
新來源內點數為 k−s+s′；全域最小性因而給

\[
C_4:\ s\le3;\qquad C_5\ne B:\ s\le5.                 \tag{2}
\]

代表不需承繼來源的 degree 或三角化條件。這裡保持的是完整延伸存在性，
不主張兩側 full fibres 等基數或存在染色雙射。

## 3. 小 patch 的初等 degree 計帳

考慮原三角化 cap，boundary 長 b≤5，私有內點數 s；令 q 為 boundary
chords 數，eII、eIB 為其內點邊與內點到 boundary 的邊數。Euler 給

\[
|E|=3s+2b-3,\qquad eII+eIB=3s+b-3-q.
\]

每個嚴格 cap 內點的 cap-degree 等於完整 G-degree：離開 cap 的原邊會
穿越 C。因此所有這些 degree≥5，得到

\[
eII\ge 2s-b+3+q.                                      \tag{3}
\]

若 2≤s≤5，每個 cap 內點都有 boundary 鄰點，否則 degree≤s−1≤4。
boundary 位於內點 induced 子圖的無界面；每條通往 boundary 的原邊均
顯示其內端 incident 此無界面。故內點子圖是 simple outerplane，即使
不連通亦有 eII≤2s−3。與 (3) 及 b≤5 矛盾。

若 s=1，唯一內点 degree≤b：b=4 不可能；b=5 強迫五條 spokes。
Euler 此時給 |E|=10，故沒有額外 boundary chord，cap 恰為 W5。
接 (2)，已證

\[
\boxed{\text{每個原 C4 的有界內部皆空；每個 proper C5 的有界內部
皆空或恰為一個 W5 中心。}}                            \tag{4}
\]

## 4. 原框接點的精確數目

若原內點 x 同接 B 上非相鄰的 a,c，寫其短原框弧為 a−b−c。
原 C4 a−b−c−x−a 依 (4) 無內點；其內側由兩三角面填滿。B induced
排除 ac，故唯一 diagonal 是 bx。此 cap 佔滿 b 的內側 sector，於是
b 的原完整鄰集僅 {a,c,x}，與 degree≥4 矛盾。

因此每個原內點至多接兩個 B 點，雙接只能相鄰。每條 B 邊有一個內側
三角面 apex；這五個 apex 互異，否則同一點會接至少三個 B 點。任何
另一點同接該 B 邊兩端，都會與該邊形成包含原 facial apex 的 occupied
triangle。故 **恰有五個原內點雙接 B**，其餘第一層點各接一次。

令 L1 為所有接 B 的原內點，D_B=Σ_{b∈B}d_G(b)。B 到內部共有 D_B−10
條原邊，雙接恰有五點，故

\[
|L1|=D_B-15.                                          \tag{5}
\]

## 5. 深層五度點的精確 identity 與 induced W5

令 h1 為 L1 中完整 degree≥6 的原點數，並令

\[
X=\sum_{x\notin B,\ d_G(x)\ge7}(d_G(x)-6),\qquad
n5=|\{x\notin B:d_G(x)=5\}|.
\]

**h1 與上游的原框超額 h_B=D_B−20 是不同參數。** 對三角化 C5 disk，
|E(G)|=3k+7，Euler degree identity 給 n5=D_B−14+X。第一層恰有
|L1|−h1 個五度點。與 (5) 相減，得到

\[
\boxed{|\{x\notin B\cup L1:d_G(x)=5\}|=1+X+h1\ge1.}   \tag{6}
\]

取其中一個原五度點 v。它不接 B；五個 cyclic 鄰點 U=(u0,…,u4) 都是
互異的原內點。原三角面使 consecutive u_i 相鄰，五個 incident 面填滿
U 的有界 disk，恰含中心 v。若非 consecutive 鄰點之間有 chord，與
v 的兩條 spokes 形成原三角形；其兩側各留下非空 U 開弧，故有界側
包含原點，違反無 occupied triangle。因此 U 無 chord，得到

\[
\boxed{\text{932／933／941 的每份全域最小來源皆有全內部 induced W5。}} \tag{7}
\]

其中中心完整鄰集恰為 U，B/U 十個原 pins 互異，U disk 恰含 v 和五個
原三角面。刪 v 後是保留這些原 pins／rotation 的合法 annulus。

## 6. 接入界線

這是 [舊結構證明](../frozen/audits/2026-10-12-c5-deep-five-wheel-01a12ffa/review/separator_proof.md)
§§1–5 的 no4ct 依賴修復與重新推導；舊普遍 C4 前提由 (1) 中的實際
s<k 取代。沒有新增有限來源搜尋、一般 annulus 代表或保完整 Σ 的五輪縮減。
本包也未採納舊私人圈秩下界：ρ≥5 若要接入三支，仍須另逐條重證其來源
前提並接回原有限覆核。一般 932／933／941 排除、h≥4 無界來源及
K∞=K≤5 全部保持 OPEN；932 的一般排除仍與四色定理等價。未新增 Lean theorem。
