# C8 剝層的完整染色轉移

2026-10-13。具名結構、來源前提與 m=10 完備分類見
[structure/PROOF.md](structure/PROOF.md)。本節的轉移定理只需要有限簡單平面圖
及其固定嵌入；不需要全域最小性、四色定理或內點大小上限。
四色集固定為 \(A=\{0,1,2,3\}\)，所有組件都沿用同一色框。

## 1. 第一層：原 C8 與內側外面

令 \(Q=H[I]\)，\(S\) 是 Q 的無界面所 incident 的**原頂點集合**，
不是無界面 walk 的位置集合。結構證明給出

\[
S=\{x\in I:N_H(x)\cap C\ne\varnothing\}.
\]

對任一 literal 指派 \(a\in A^C\)，令 \(\mathcal F_H(a)\) 是 H 在 C 固定 a
時的全部完整染色；對 \(b\in A^S\)，同樣定義 \(\mathcal F_Q(b)\)。
若 a 或 b 違反相應 induced graph 的邊，fibre 就是空集。令

\[
K_C(a,b)=
\prod_{cx\in E(H),\ c\in C,\ x\in S}[a(c)\ne b(x)].
\]

則有逐份完整 lifts 的雙射分解

\[
\boxed{\quad
\mathcal F_H(a)=
\bigsqcup_{b\in A^S:\ K_C(a,b)=1}
\{a\cup f:f\in\mathcal F_Q(b)\}.
\quad} \tag{T1}
\]

若 a improper，右側也定義為空。所有 C–I 原邊的內端都在 S；H 的其餘邊
恰為 C 邊及 Q 邊。因此右側每份 union 恰為一份 H 染色，反向由限制得到唯一
b 與 f。不同 b 的完整染色互斥，空 fibres 全部保留。相應精確計數為

\[
N_H(a)=[a\text{ proper on }H[C]]
\sum_{b\in A^S}K_C(a,b)N_Q(b). \tag{T2}
\]

若使用有重複接點的 boundary walk \(W=(w_0,\ldots,w_{L-1})\)，其位置指派
\(\widetilde b\in A^L\) 必須先乘上

\[
\Delta_W(\widetilde b)=
\prod_{j<k:\ w_j=w_k}[\widetilde b_j=\widetilde b_k]. \tag{T3}
\]

只有 \(\Delta_W=1\) 的指派才是原 S 上的指派。正對雙接點 x 的兩次出現
始終是同一原點；bridge 的往返也不能建立兩份獨立端點。

## 2. 分支與 bridge：共用接點的完整 join

在 one-pinch 類，Q 的兩個 disk blocks \(D_L,D_R\) 只共用 x。把 b 限制為
\(b_L,b_R\)，則

\[
\mathcal F_Q(b)=
\mathcal F_{D_L}(b_L)\Join_{x}\mathcal F_{D_R}(b_R),
\qquad
N_Q(b)=N_{D_L}(b_L)N_{D_R}(b_R). \tag{T4}
\]

\(\Join_x\) 比對具名原點 x 的 literal 色，並合併其餘原頂點。計數式之所以
能相乘，是 x 的色已由**同一份** b 固定，兩份內點集合互不相交，且沒有跨
block 邊。若 x 尚未固定，須在相同色值上求和：

\[
N_Q=\sum_{c\in A}N_{D_L}(x=c)N_{D_R}(x=c), \tag{T5}
\]

其中其餘固定 pins 仍保留。不能將兩個各自非空的投影相乘。

在 two-pinch 類，兩個 terminal disk blocks 的接點為 x、y，唯一中間 block
是原 bridge xy。因此

\[
\begin{aligned}
\mathcal F_Q(b)&=
\mathcal F_{D_L}(b_L)\Join_x\mathcal F_{xy}(b|_{\{x,y\}})
\Join_y\mathcal F_{D_R}(b_R),\\
N_Q(b)&=[b(x)\ne b(y)]N_{D_L}(b_L)N_{D_R}(b_R).
\end{aligned} \tag{T6}
\]

同一公式亦適用任意後續層的 block-cut forest：每條原邊只由其 block 檢查，
每個 articulation 的色在所有 incident blocks 中一致，未固定的接點色只求和
一次。孤點 block 在固定色下有恰一份 lift，edge block 在兩端異色下有恰一份
lift；不在定義時漏掉這些終止類。

## 3. 任意大小的反覆剝層定理

從固定原嵌入的 \(R_0=Q\) 開始。對每一 \(R_\ell\) 的連通分量，各取其無界面
所 incident 的原頂點；合起來記為 \(S_\ell\)。定義

\[
R_{\ell+1}=R_\ell-S_\ell.
\]

空圖的 expose 集合為空。每個非空有限分量至少有一個無界面頂點，故序列
嚴格減少頂點，至多 \(|I|\) 步終止。分量的外面可為簡單環、帶 articulation
的 walk、bridge 往返或單點；算法每一類都定義。

在本題的三角化原圖中，每個 survivor component 的有界面仍為原三角面。
任何 survivor 簡單環內側都不能含剛刪去的 outer-face 點；否則該點原先也被
這個未刪原環與無界面分開。環內的原點與原邊因此全部保留，不會把原三角面
合併成新有界大面。於是後續層仍可按原面與原 rotation 分解為 disk blocks、
bridge 與孤點，沒有擅自補邊或另選嵌入。這個保面性不恢復原 C8 度數界。

**跨層鄰接引理。** 若 \(uv\in E(R_\ell)\)、\(u\in S_\ell\)、
\(v\in R_{\ell+1}\)，則 \(v\in S_{\ell+1}\)。在 u 所 incident 的無界面內
取一條抵達 u 的曲線；刪去 u 及其 incident edges 後，沿 uv 的細管可抵達 v，
管的內部避開剩餘圖。因此 v incident 於其分量的無界面。這也證明所有原邊
只連接同層或相邻兩層，沒有越過下一層的未記錄附件。

對 \(a\in A^{S_\ell}\)，定義 \(\mathcal F_\ell(a)\) 為 R_l 的完整 fibre，並令

\[
K_\ell(a,b)=
\prod_{uv\in E(R_\ell),\ u\in S_\ell,\ v\in S_{\ell+1}}
[a(u)\ne b(v)].
\]

則逐層有

\[
\boxed{\mathcal F_\ell(a)=
\bigsqcup_{b\in A^{S_{\ell+1}}:\ K_\ell(a,b)=1}
\{a\cup f:f\in\mathcal F_{\ell+1}(b)\}.} \tag{T7}
\]

a improper 時右側為空。證明與 T1 相同，使用跨層鄰接引理檢查所有邊。
在空圖終止處，\(\mathcal F_L(\varnothing)=\{\varnothing\}\)，計數恰一。
因此

\[
N_\ell(a)=[a\text{ proper on }R_\ell[S_\ell]]
\sum_b K_\ell(a,b)N_{\ell+1}(b) \tag{T8}
\]

是任意有限大小、保存原點身份的完整轉移；逐層保留 lifts 時是雙射重建，
只保留 counts 時給出精確計數，只保留零／非零時給出完整可延伸關係。
不同分量的 literal 指派可取 Cartesian product；有共用原點的 blocks 則須
用 T4–T6 的 join。三者不可互換。

這裡不保證 \(|S_\ell|\le8\)，也不保證每層同時滿足第一層的 C8 度數、induced
及至多兩附件契約。後續層若要採用特定 C8 簡化，必須重新逐項驗證。
有限 state 數為 \(4^{|S_\ell|}\)，所以這是任意大小的正確剝層機制，沒有得到
大小無關的固定寬度壓縮或來源排除定理。

## 4. 接回原 B 與完整十列

對固定的八項原 B–C collar 之一，令 \(K_{BC}(p,a)\) 檢查**全部**原 collar
邊。對原 B literal row p 有

\[
\mathcal F_G(p)=
\bigsqcup_{a\in A^C:\ K_{BC}(p,a)=1}
\{p\cup f:f\in\mathcal F_H(a)\},
\qquad
N_G(p)=\sum_a K_{BC}(p,a)N_H(a). \tag{T9}
\]

p improper 時 fibre 空。按舊契約的同一十列順序取
\(\Sigma(G)=\sum_i2^i[N_G(p_i)>0]\)。整份 Sigma 的投影在完成共同 join 後才取；
不以每列另選一份 H、另改 collar 或各自正規化兩個 pieces。

校準可只列 C8 的 274 個 S4-orbit 代表，但內介面始終使用 literal 四色。
任一共用置換 \(\pi\) 的合法搬運為
\(\pi:\mathcal F_H(a)\to\mathcal F_H(\pi a)\)，同時作用於全部原頂點。
兩個獨立正規化的代表需要先還原到同一色框，才能套 T1–T9。
