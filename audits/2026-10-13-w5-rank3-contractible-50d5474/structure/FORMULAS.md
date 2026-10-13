# W5-RANK3-C：來源、一般圈秩計帳及剩餘分量數

2026-10-13，固定 BASE `50d5474f2446403f3b3001d5943571184c8c9936`。
輸入逐 byte 保存於 `../frozen/`，hash 見 [BASE.json](../BASE.json)。
本輪從 k≥13 開始，完全不使用並行 K13-COLLAR 或未提交 Cell/K4 結果。

## 1. 量詞及完整來源契約

G 是**全部**完整外框關係不在 K132 的 disk-C5 圖中，先最小化內點數 k、
再最大化邊數的來源。任取合法全內部 induced W5，原中心 v、原循環鄰點
U=(u0,…,u4)，原外框 B=(b0,…,b4)；十 pins 互異，U 內恰為 v 及五個
原三角面。A=G−v，P=V(G)\(B∪U∪{v})，F=G[P]，r=|P|=k−6，
c=c(F)，ρ=e(F)−r+c。反設 ρ=3 且 U/v 位於 F 的無界面。

沿用凍結來源鏈：A 是指定 B 外面、U 空內面的有限簡單 plane annulus；
B/U 各 induced C5，其餘 annular 面全部三角化；r≥7；每個私人點完整
d_G≥5；在 B、U 各至多兩個鄰點，兩個時必相鄰。後者在 U 的版本來自
原 C4 小 cap 限制，並非改換 source 身份。

故 d_G(x)=d_F(x)+d_T(x)，d_T(x)≤4。F 無孤立點；leaf 必完整度五並恰有
B/U 各兩個相鄰附件。起初沒有假設 F 連通、私人度至少五、私人無葉，
也沒有 N2、ε、edge-critical 或 Gallai 前提。

## 2. 一般圈秩公式的本輪核對

令 t_P 為 PPP 原三角面數，a 為全 terminal 原三角面數，p 為 B–U 原邊數，
M 為 BUP 原三角面數。t_P 與外圈超額 h 無關。

annulus Euler 與面長總和给 e(A)=3r+20、三角面數 2r+10。
因 e(F)=r−c+ρ，恰含兩私人點的面數為 2e(F)−3t_P。
全 terminal 三角面只有 BBU/BUU：同一 induced C5 不含三角形。
每份全 terminal 面恰使用一條 B/U 原環邊，故有一私人點、兩同環 pins
的原面數恰為 10−a。完整逐類計帳為

\[
2r+10=t_P+(2e(F)-3t_P)+(10-a)+a+M,
\qquad M=2(c-\rho+t_P).
\]

逐 B–U 邊的兩側計面，2p=2a+M，因而

\[
p=a+c-\rho+t_P.
\]

除十條框邊、p 條 cross edges 與 e(F) 條私人邊後，terminal–P 邊數為
2r+10+c−ρ−p。完整私人 degree 總和遂為

\[
\sum_{x\in P}d_G(x)=2e(F)+e(T,P)=4r+10+\rho-c-p.
\]

這是任意圈秩公式；不把 essential 的 p=0、M=0 或 c=1 移植到此處。

## 3. 為何 t_P=3，包括不連通及 slit 面

任意 plane F 恰有 ρ 個有界面；此為不連通 Euler 公式 e−r+c+1。
F 已含全部私人點及其間全部原邊，故每個面開區域無私人點/邊。
B 位於無界面；本分支的連通 U/v 亦在無界面，所以每個有界面開區域
沒有任何 G 頂點。其餘 G 邊有 terminal/v 端點，無法不穿越 F 而進入
此面。於是每個有界 F 面本身就是原 G 面，必是 PPP 三角面。
這同時排除多邊界分量、重經 bridge 的 slit 面：原 G 的該面是三角面。

反過來 PPP 原三角面也是 F 的有界面。因此 t_P=ρ=3，代入得到

\[
M=2c,\quad p=a+c,\quad
\sum_{x\in P}d_G(x)=4r+13-2c-a,\quad
7\le r\le13-2c-a.
\]

## 4. 正式排除 c≥3

c≥4 時 r≤13−8=5，違反 r≥7。
c=3 時 r≤7−a，故 r=7、a=0。每個私人分量至少兩點，三分量大小只能
3、2、2；簡單圖最多有 binom(3,2)+1+1=5 條私人邊。
但圈秩三要求 e(F)=r−c+3=7，矛盾。

所以本輪正式採納的剩餘必要域恰為

| c | r | a | p | M |
|---|---|---|---|---|
| 1 | 7≤r≤11 | 0≤a≤11−r | a+1 | 2 |
| 2 | 7≤r≤9 | 0≤a≤9−r | a+2 | 4 |

c=1 的圈秩分配是 (3)。c=2 是 (3,0) 或 (2,1)，包括分量交換。
rank-zero 分量是非平凡樹。上述表只是必要化約；完整 block/附樹排除見
[CORE.md](CORE.md)，原 rotation 及附件完備域見 [ATTACHMENTS.md](ATTACHMENTS.md)。
本節沒有憑任務描述直接採納 c≤2，也沒有把有界 r 搜尋當作核心覆蓋证明。
