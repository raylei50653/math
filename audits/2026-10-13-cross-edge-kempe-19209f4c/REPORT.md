# 跨原邊 Kempe 缺陷的共同 lift 搬運

2026-10-13。BASE=`19209f4cf68261fdce5e84a7804cfe04ae0957bf`，固定輸入及
SHA-256 見 [BASE.json](BASE.json)。原始來源為
[共面正規形](../../docs/c5_cofacial_normal_form.md)、
[完整外圈](../../docs/c5_neartri_boundary_collar.md) 及
[全內部 W5](../../docs/c5_degree5_link_reductions.md)。

本輪得到真正跨邊的完整染色雙射：同一五度中心的拒絕列缺陷以三份為一組，
保留全部其他頂點的實際顏色；兩個相鄰五度中心之間還有經共同原邊的精確搬運。
它給五條 spokes 的線性恆等式及同一 lift 的二色路徑限制。
**未證普遍共同拒絕列的共同染色，也未排除 933／941。**
實際目標來源仍為 `not triggered`；有限負控制只反駁明列的廣義拼接命題。

## 1. 原逐邊引理：量詞及完整合同

固定有限簡單 plane disk 圖 G、原有序外框 B=(b0,…,b4) 及色集 C={0,1,2,3}。
所有十列代表及整張圖只作一次共同 D5／S4 搬運。十列順序沿用原來源。
在所有完整 Σ 不在 K132 的來源中，先最小化內點，再最大化邊數，
得到 chordless-C5 近三角化 G，Σ(G)=R∈{933,941}。
這不包含 edge-critical、Gallai、舊 ε 或 N2 的假設。

對非邊界原邊 e=st，兩個相異三角面 stu、stv 的 opposite vertices 必為
相異 u,v。四條側邊與原旋轉均保留。在原頂點集合上定義

\[
J_e(p;a,b)=\{f:V(G)\to C:f\text{ proper on }G-e,\ f|_B=p,
 [f(s)\ne f(t)]=a,\ [f(u)\ne f(v)]=b\}.
\]

全部十列、四格及空 fibres 都屬於合同。若至少一個 opposite vertex 是內點，則

\[
J_e(01232;1,0)\ne\varnothing
\Longrightarrow
\exists p\notin R\ \exists f\in J_e(p;0,0). \tag{E}
\]

證明沿用凍結的 `rewire_analysis.md` §3.1：原接受列的 u=v 使
Q=(G-e)/(u=v) 合法且減少內點；故 Σ(Q)∈K132 且含 01232。
目錄中沒有含 01232 且包含於 R 的關係，所以 Q 接受某個原拒絕列 p。
把其完整染色拉回 G-e；u=v，且 s=t，否則可恢復 e 而違反 p 被 G 拒絕。
四條側邊使兩個等色對用不同顏色。

對 933，可用 01231 作另一份起始列，但不能把兩次所得邊數相加。
沒有 opposite 內點時，減少原內點且保五個原 labels 的識別論證不適用。
對五度內點的兩條同色-opposite spokes，該適用性由已證的無二邊 crosscut
保證：若兩個 opposite 都在 B，它們不相鄰，形成被排除的 crosscut。

若先固定同一接受列的完整染色 α，令 E(α) 為其適用的 opposite 同色原邊，
(E) 的正確量詞為

\[
\forall\alpha\ \forall e\in E(\alpha)\ \exists p_e\notin R\ \exists f_e\in J_e(p_e;0,0).
\]

不能交換成存在共同 p 或共同 f。更強地，若 e≠d，任何兩份單邊缺陷的完整
原頂點染色都不可能相同：J_e(p;0,b) 使 e 單色，但 J_d(q;0,b') 必使 e proper。
把兩份資料嵌入 G−{e,d} 不會消除此衝突。

## 2. 五度中心的全列跨邊定理

此節本身不需最小性、933／941、4CT 或平面計數定理。只需內點 v 的全部鄰點
按原旋轉為 U=(u0,…,u4)，五個 vu_i u_(i+1) 為實際三角面。
若只作代數版本，可將 u_(i−1),u_(i+1) 指定為 J_ei 的 pins 而僅要求 rim 邊；
本文的原面 opposite 語義使用前述面條件。最小來源的輪符合這些前提。
令 H=G-v、e_i=vu_i，下標皆模五。完整 H 染色在 U 上只能有 (2,1,1,1)
或 (2,2,1) 兩種重數型。

- A_i(p)：H 的完整 p-lifts，U 用四色且 u_(i−1)=u_(i+1)。
- T_i(p)：H 的完整 p-lifts，U 用三色且唯一 singleton 位於 u_i。

五份 A_i 及五份 T_i 兩兩不交，聯集是 H 的全部 p-lifts。
令 ρ_v 為刪去中心值的限制映射。逐份完整染色有

\[
\begin{aligned}
\rho_v J_{e_i}(p;0,0)&=A_i,\\
\rho_v J_{e_i}(p;0,1)&=A_{i+2}\mathbin{\dot\cup}A_{i+3}\mathbin{\dot\cup}T_i,\\
\rho_v J_{e_i}(p;1,0)&=T_{i+2}\mathbin{\dot\cup}T_{i+3},\\
\rho_v J_{e_i}(p;1,1)&=T_{i-1}\mathbin{\dot\cup}T_i\mathbin{\dot\cup}T_{i+1}.
\end{aligned} \tag{W}
\]

每一式的限制映射都是雙射：第一座標為零時中心必取 u_i 的顏色；為一時
中心必取三色 U 的唯一缺色。證明只需按上述兩種 proper C5 型逐位置核對，
詳見 [完整證明](theory/THEORY.md)。因此不是端點投影相等或只比 counts。

特別對被 G 拒絕的 p，所有 T_i 都空。任一 f∈J_ei(p;0,0) 唯一對應另外
兩份 J_e(i+2)(p;0,1)、J_e(i+3)(p;0,1) 的完整 lifts；只改 v 的值，
其餘全部頂點及原邊界 p 完全相同。三份染色分屬不同的單邊刪除圖。
同一 H lift 反而不可能同時屬於兩份不同的 A_i。

記 N_i^{ab}(p)=|J_ei(p;a,b)|、t_i=|T_i|，則

\[
t_i=N_i^{01}-N_{i+2}^{00}-N_{i+3}^{00}\ge0,\qquad
|\mathcal C_G(p)|=\sum_i N_i^{01}-2\sum_i N_i^{00}. \tag{C}
\]

拒絕列特別滿足 N_i^{01}=N_(i+2)^{00}+N_(i+3)^{00}。
這是多條原邊必共同滿足的條件；單邊非空的任意表通常不滿足它。
既有 W5 marked relation 用商圖重數重建 H/G；本輪 (W) 則給原邊 J_e 之間
逐 lift 的搬運及其跨中心相容性，並不把前序重建公式另稱為新結果。

## 3. 同一原邊連接兩個五度中心

若 v,w 都是五度內點，e=vw 分別是 v-star 的 e_i 與 w-star 的 d_j，
則對每個原拒絕列 p，有自然雙射

\[
J_{e_{i+2}}(p;0,0)\ \dot\cup\ J_{e_{i+3}}(p;0,0)
\ \longleftrightarrow\ J_e(p;0,1)
\ \longleftrightarrow\
J_{d_{j+2}}(p;0,0)\ \dot\cup\ J_{d_{j+3}}(p;0,0). \tag{A}
\]

左箭頭只改 v；右箭頭只改 w。中間必須是**同一份**原 G-e 完整染色。
故合成保留 V(G)\{v,w} 上的每個顏色，且两側 00 counts 的和相等。
這不是將兩個獨立成功的 witnesses 拼接。最小來源是否必有相鄰五度中心，
本輪沒有證明；(W) 則已適用於每一個保證存在的五度中心。

令 m5(e) 為 e 的五度內點端數，求和只取接觸五度內點的原邊。
對全部五度內點加總 (C)，得到同一 G 的
全域恆等式

\[
\sum_e m5(e)\bigl(N_e^{01}(p)-2N_e^{00}(p)\bigr)
=n_5|\mathcal C_G(p)|. \tag{G}
\]

不同中心不共用 H_v；這裡共用的是每條原邊唯一的 J_e 及其 full lifts。
拒絕列使右側為零。九／八下界不迫這個等式矛盾。

## 4. 同一 lift 的重色路徑與條件排除

在 A_i 的共同 H lift η 中，把 rim 色寫成
(a,b,c,d,b)，起點為 i；a,b,c,d 互異。考慮兩個在 rim 次序中不相鄰的 singleton pairs
(u_i,u_(i+2)) 及 (u_i,u_(i+3))，各用它們的兩種實際顏色形成 H 的二色子圖。

**路徑／邊界限制。** 若 p 被 G 拒絕，則每個 pair 必滿足以下二者之一：
兩端在同一二色分量；或兩端的不同二色分量都碰到原外框 B。
在全內部 W5 上，後一情形供應兩條實際通向 B 的二色路徑，不能只記端點色。
兩個 pair 的分量及路徑必來自同一 η。

證明：若兩端不連通且其中一端分量不碰 B，交換那個分量的兩色。
兩個 rim singleton 合為同色，U 只用三色；p 保持不變，便可補回中心，矛盾。

**單步條件排除。** 若最小來源的任一保證存在的拒絕列缺陷，其 η 違反上述
任一 pair 的限制，就已排除該來源，故適用於 933 及 941。
在「一次不碰 B 的 Kempe 分量交換，然後補中心」這個明確機制內，這個條件
也是必要的：相鄰 singleton pair 已由 rim 邊連通；任何 singleton 與重色 b
至少有一條 rim 邊相接。交換這些其他色對都不會使 rim 色數從四降至三。
所以不能在此機制內再弱化條件。多步交換的充分條件可以更弱，本輪未分類。
若某一相關色對在 B 上至多出現一個頂點，兩個不同分量不可能都碰 B，
拒絕便強制兩個 singleton 之間存在實際二色路徑。933／941 的拒絕列皆用三色；
當該色對恰為原框缺色與原框 singleton 色時適用，但不能預設輪上的色位。
完整證明、既有引理的審查與目錄投影障礙見 [獨立審查](review/KEMPE_REVIEW.md)。

## 5. 九／八下界能供應甚麼

固定同一份原 01232 染色 α。每個五度內點正好有兩條相鄰 spokes 的 opposite
同色，共 2n5 個具名 incidence。逐個選 (E) 的一份拒絕列見證，933 有四個
拒絕列、941 有三個；鴿籠原理迫某一 p 分別承接至少五／六個 incidence，
因而至少涉及三個五度中心及三條不同原邊。這只同步 row。
再選這三個中心，各由 (W) 供應至少三條 p 單邊缺陷 spokes，共至少九個
incidence。三個中心之間最多有三條原邊可重複計入，因此同一 p 實際有至少
六條不同原邊的單邊缺陷（00 或 01）。仍不共用它們的完整染色。

若同一中心的兩條相鄰觸發 spokes 恰選到相同 p，(W) 又迫該中心五條 spokes
全有 p 的單邊缺陷；兩份 00 仍在不同 A_i，不能聲稱共同 H lift。
全內部 W5 供應 §4 所需真正內部 pins，但沒有保證存在可交換的邊界自由分量。

## 6. 有限控制及信任界線

固定域為 `outer_w5`、`prism` 及 annulus 對角線 masks 0、1、3 三張圖。
五圖共有 16 個五度內點輪、19 條相鄰五度中心原邊；去重後 61 份原邊表，
共 2,440 格（1,063 空格）、4,894 份完整 J lifts。另保留 1,253 份 H lifts、
403 份 G lifts 及 7,518 份二色分量分割，核對全部保持 B 不變的單分量交換。
完整證書與重播結果記於 [VERIFICATION.md](VERIFICATION.md)。

### 6.1 同一拒絕列也不能把兩份 00 合為共同 H lift

`triangulated_03` 的原點名為 b_i=i、u_i=5+i、v=10。
原邊為 B、U 的環邊，全部 b_i u_i、全部 vu_i，以及
b0u1、b1u2、b3u2、b4u3、b0u4。原面由各 annular quadrangle
(b_i,b_(i+1),u_(i+1),u_i) 沿上述對角線切開，再加五個 vu_i u_(i+1) 構成。
故是具名 disk near-triangulation，W5 全在內部。其完整 Σ=959，僅拒絕 01212。

固定 p=01212，H=G-v **恰有**下列四份完整 lifts；B 固定為 p，所以列出的 U
加上 B 已是全部 H 染色。各自補上表中 v 色便是對應原邊的 00 full lift。

| 00 spoke i | U 的五個實際色值 | v 色 |
|---|---|---:|
| 1 | 32301 | 2 |
| 2 | 23031 | 0 |
| 3 | 12303 | 0 |
| 4 | 32031 | 1 |

五份 A_i 的大小為 (0,1,1,1,1)，兩兩不交；01 counts 為 (2,2,1,1,2)。
例如 U=12303 的共同 H lift 分別給 spoke 3 的 00（v=0）、spoke 0 的 01
（v=1）、spoke 1 的 01（v=2）。這正是 (W) 允許的同步，不是兩份 00 相等。
相同圖中有非相鄰 singleton 二色分量分離卻兩者都碰 B 的情形，顯示條件排除
不能刪掉「至少一個分量避開 B」。

### 6.2 其他負控制

外框就是 rim 的 `outer_w5`，五條 spokes 的 00 拒絕列支援依序只有
01231、01023、01213、01232、01203。各自非空，卻沒有共同列。
其全內部 W5 與目標 R 前提都未觸發。`prism` 另保存單獨正規化 U 會破坏
五條原 b_i u_i 邊的完整反例，以及保持 B 的單步 Kempe escape 正控制。

上述廣義拼接宣稱標為 `counterexample`；(W)、共同中間 lift、(G) 及單步判準
標為 `triggered and holds`；實際最小 933／941 與 n5≥9／8 圖域標為
`not triggered`。不把一般圖反例搬成最小來源反例。

每張控制圖保留原 B、literal edges、oriented faces、rotation、全部十列四格、
空 fibres、完整 lifts 及跨邊原映射。負控制不滿足最小目錄外身份，不能稱為
933／941 反例。來源／目錄最小性假設只用於 (E) 與九／八／全內部輪的供應；
(W)、(A)、(G) 與單步 Kempe 引理本身由直接紙面證明成立。

沒有新增 Lean theorem；Lean build 只作既有專案回歸。未重播外部計數論文或
上游大型枚舉。一般同步、十三內點以上來源及 K∞=K≤5 仍 OPEN。

本轮達到的是完整跨邊 constraint 與精確同步障礙；下一步窄義務是由同一來源
拓撲／完整關係強制 §4 的某個自由分量，或分析實際缺陷搬運軌道能否到達它。
不能以獨立染色的路徑交叉、零 target controls 或 counts 相等代替此義務。
