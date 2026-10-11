# N45-S 含 long：保留完整 U/L/S 的同源契約與必要化約

2026-10-10。任務 ID：`N45-S-LONG-CONTRACT`。輸入 BASE：
`0d76c4c887033e565eaa0ca4d2a515619d7c97f3`；舊研究 BASE：
`dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。
51 份實讀權威輸入對回當前 BASE Git objects，見 [inputs.json](inputs.json)。

**交付：精確契約、任意大小必要化約、完整 lift 介面的有限校準與未解義務。**
選定分支仍 **OPEN**，本輪不採納新的來源全排。U 在降度側／另一側、S 的真框邊
pair／singleton 都保留；這不是所有含 long 殘留的完整分類。
三份只讀分工核對幾何、關係與前提，根 agent 對回以下論證；不是新一輪 closure 驗收。
目前停止點連回 [Kempe 導覽](../../docs/c5_kempe_guide.md)。

## 1. 原身份：十二項契約

以下是待排來源的共同假設，不是有限 checker 已找到的來源。

| ID | 精確前提／資料義務 |
| --- | --- |
| K1 | G 任意大小有限簡單 disk 圖，外面為具名 ordered induced C5，B=(b0,…,b4)；供給全部原 vertices、edges、rotation。 |
| K2 | 完整有序 Σ(G)=933／941 或整圖共同 D5 像；所有非框邊 Σ-critical。 |
| K3 | 有效 H 連通，ε(G)=2；恰兩個原 degree5 roots r,s，rs 不存在，其餘有效原內點完整 degree4；原 full B-touch。自由孤立內點另留完整染色因子。 |
| K4 | H−{r,s} 的完整分量**恰**為 U,L,S。U 只接一個 root；L/S 各接兩 roots，原支援非空。所有原件 one-sided。 |
| K5 | L 的 actual support 不包含於任何真框邊兩端；S 的 actual support 包含於某真框邊兩端，所以為真 pair 或 singleton。不能預設 S 是單頂點。 |
| K6 | e=rb_i 是具名原 spoke。V(X)=V(G)，E(X)=E(G)−{e}；U/L/S、全部原 contacts／附件／bridges 都保留。 |
| K7 | 對固定原拒絕 literal β，**X=G−e=M 自己**是 inclusion-minimal β-core，root degrees=(4,5)。不是先取另一份小 core 後稱它 X。 |
| K8 | U 的 owner 是 r 或 s；其原 contact 數 n_U≥1，不預設 unit。每個原 shared r/s contact 只有一個 actual vertex／tuple 座標。 |
| K9 | ordered contacts、ownership、原 edges、actual attachments／support、bridges、rotation 與框順序跨列不變；D5／root 交換搬整份資料。 |
| K10 | 十個 literal 代表，各保全部16 ordered root pins、diagonal／空 fibres；每個完整 contact tuple 保全部 local preimages，接合保全部整圖 lifts。 |
| K11 | 原 G 每條非框邊 f 的 Σ-critical witness：某 γ_f∉Σ(G) 及 G−f 完整 lift。各邊／piece 的 γ_f 可不同。 |
| K12 | X 每條 retained 非框邊 f 的 **同一 β** 刪邊完整 witness。G−f 與 X−f 的圖、列、assignments 分開；恢復 e 另核 r 色。 |

原共同假設見 [N45 權威 §1](../../docs/c5_excess_two_nonadjacent_unit_core45.md)。
原 G 不必對 β minimal：本身份明設刪 e 仍拒絕 β。K7／K12 才给 X 自己的
β-critical⇒Σ-critical；一般 spoke derivative 不能自 G 遺傳 criticality。

令 t_r,t_s 為**原** spoke 數，k_T^r,k_T^s 為 T=L/S 的原 root incidence，
m_r=k_L^r+k_S^r，m_s=k_L^s+k_S^s。原 degree 身份為

\[
t_r+m_r+1[U\text{ owner}=r]n_U=5,\quad
t_s+m_s+1[U\text{ owner}=s]n_U=5,\quad t_r\ge1,\ m_r,m_s\ge2.
\]

X 的 r-spokes 恰 t_r−1，s-spokes仍 t_s。每個原 piece 點 v 的完整 degree 身份是
deg_T(v)+1[rv∈E(G)]+1[sv∈E(G)]+|N_B(v)|=4；shared contact 算兩條邊，
不算兩個獨立可染座標。任意大小 pieces、原 bridge 長度與旁支均無上界。

## 2. 原盾弧費：pair 與 singleton 必須分開

刪任何一 mixed 後，另一 mixed 仍以實際原 contacts 連 r,s；刪 U 後也連通。
因此三件原 one-sided。對每件 T，沿原定義
K_T=B∪G[T]∪E(T,B)，F_T 為含完整 H−T 的原內面，σ_G(T) 是不在 ∂F_T 的框邊。

原 critical-contact full lift 限制到 G−U 給不能接回整 U 的 outside witness；
原 full B-touch 和 H−U 的連通性供給避 U 外路。沿用
[原盾弧 §2–3](../../docs/c5_unary_shield_budget.md)與
[B-S0](../../docs/c5_phase_b_common_lemmas.md)，有

\[
|\sigma_G(U)|\ge2,\quad |\sigma_G(L)|\ge2,\quad
\sigma_G(U),\sigma_G(L),\sigma_G(S)\text{ 兩兩邊互斥},\quad
\sum_T|\sigma_G(T)|\le5.
\]

不同見證列只用來收**同一原圖的幾何費**，不加跨列禁色容量；e 不收 piece 費。

| S 的 actual support | 原盾弧長度 (U,L,S) | 原支援 |
| --- | --- | --- |
| 真框邊 pair | 恰 (2,2,1) | U/L 各連續三點，S 恰該真邊兩端 |
| singleton | (2,2,0)、(2,3,0)、(3,2,0) | U/L 的長2／3分別為連續三／四點，S 保原單點 |

singleton 的零盾弧另有原面證明：若 proper σ_S 非空，其兩不同端點都必是
actual attachment（端點若無附件，兩框邊在 K_S 同面，不能恰一條在 ∂F_S）；
若 σ_S=B，原 full B-touch 又迫 support=B。兩種都與 singleton 矛盾。
不能只從「未收正費」推出零盾弧，也不能把長3弧叫三點支援。

每條原 spoke（**包括 e**）及別件附件都避開每段 σ_G(T) 的框內點。
這是原圖面限制，不重新計算 σ_X，也不刪去盾內點上 T 自己的原附件。

## 3. 兩個任意大小結構必要式

**SL-TOUCH：此選定 X 自己 full B-touch。** 原來源盾弧引理2適用於 U/L，
给 N_B(U)=V(σ_U)、N_B(L)=V(σ_L)。兩弧邊互斥，聯集含至少四條 C5 邊，
其端點聯集必是 B。U/L 所有 actual attachments 在 X 全留，故

\[
N_B^X(U\cup L)=N_B^G(U\cup L)=B.
\]

這是本選定分支的新必要化約，由原支援證得；不是 generic G−spoke 繼承 full B-touch。
U/L 盾內點仍各有其 owner piece 附件，所以整 U 省略的「未接框點」換色論證不適用。

**SL-STAR：沒有 U 的 root 至多兩條原 spokes。** 記該 root 為 b。若 t_b=3，
H−b={另一 root}∪U∪L∪S 原連通，整塊落在 B 加原 b-star 的同一個面。
原 full B-touch 迫兩個非 spoke 框點都在該面，star gaps 必為1,1,3。
每件 T 的非框部分都在長3面；另外兩個小面不含 T，可經 b-star 原邊在 K_T 補圖中
到 b∈H−T，故其框邊屬 ∂F_T，不屬 σ_T。因此全部原 σ_T 都包含於長3弧。
U/L 已需四條互斥盾邊，2+2>3，矛盾。這不需要 S 收正費。

此步重新核過 [S06 原 star 論證](../2026-10-09-n45-s/REPORT.md)
及 [SU-A §5.1](../2026-10-09-n45-su-a/REPORT.md) 的充分前提；原兩-short假設只用於
其費用下界，本次用已獨立取得的 U+L 費取代。

由 degree 身份、SL-STAR 與 e 存在，得到以下**必要 profiles，尚未證來源實現**：

| U owner | 原 incidence／spoke 必要域 |
| --- | --- |
| r | (t_r,n_U,m_r)=(1,1,3),(1,2,2),(2,1,2)；(t_s,m_s)=(0,5),(1,4),(2,3) |
| s | (t_r,m_r)=(1,4),(2,3)；(t_s,n_U,m_s)=(0,1,4),(0,2,3),(0,3,2),(1,1,3),(1,2,2),(2,1,2) |

每份 profile 再保存各 k_L,k_S≥1 的全部 splits，不能只存 m 的 marginals。
singleton S 由已採納 [S04](../2026-10-09-n45-s/REPORT.md)
給 k_S^r+k_S^s≥4，所以 m_r+m_s≥6；這只刪不合必要式的 profile。

**Pair 的額外原幾何。** 真 pair 時，whole D5 搬成 U012／L234／S40；
原 U owner 記 a，另一 root 記 b。逐項重新檢查
[PG-02 六原 bags／九原鄰接](../2026-10-09-n45-pg/REPORT.md)
的弱前提：三原件互斥連通、指定 actual support 附件、a−U 至少一 contact、
兩 roots 到 L/S 的正 contacts、框邊與平面性。該 minor 證明不需 U 的 contact 唯一，
也不需刪 U，故此處仍得 N_B(a)⊆{b0,b2}、N_B(b)⊆{b4}。
於是 pair 且 U在r 時 t_s≤1；pair 且 U在s 時 t_r=1、m_r=4。
只轉用此弱 lemma，不轉用 PG 的整份 LP 身份、pair 單頂點 S 排除或 coloring replacement。

## 4. 完整跨列 joint、16 pins 與空 fibres

共同 literal 代表依序為
`01012,01021,01023,01201,01202,01203,01212,01213,01231,01232`。
q0,…,q4 的 indices=(6,4,3,1,0)，T4={2,5,7,8,9}；
941 拒絕位置 Q(G)={0,1,3}，933 為{0,1,2,3}。非 canonical 圖須共同搬整圖。

对 T=U/L/S，Λ_T(γ) 是滿足全部原 internal edges／actual B attachments 的
所有完整 assignments。R_T(γ) 按原 ordered contact list 投影，每個 tuple 保存
全部 preimages；不是只留 contact 色集合或一份 lift。

\[
\Lambda_T(\gamma;a,b)=\{f\in\Lambda_T(\gamma):
f(v)\ne a\ (v\in N_T(r)),\ f(v)\ne b\ (v\in N_T(s))\}.
\]

無 owner 的不等式不加；shared contact 的兩不等式作用同一 f(v)。每列保全部
(a,b)∈Col²，包括diagonal、空 fibre。令 A_T(γ) 為非空 pinned fibres 的完整 ordered relation。
U 的完整避色查詢 F_U(γ)={c:Λ_U(γ;c)=∅}；F_U 允許空，並不是替代 R_U 的輸入。

由 retained spokes 的 literal singleton factors，以及 U 在其 owner 的 F_U，定義
E_r^X(γ)、E_s(γ)。則

\[
J_X(\gamma)=(E_r^X\times E_s)\cap A_L(\gamma)\cap A_S(\gamma).
\]

每個非空 joint fibre 的**全部**整圖 lifts 是同框 pinned piece lifts 的 restriction／union，
加 B、r,s 與自由孤立點的全因子。須与直接在原 X edges 上枚舉的全部 lifts 逐項相等；
同样核 G。此存在性／完整 lift 介面是 [E4 §6](../../artifacts/c5_excess_two_e4/REPORT.md)
與 PC 可沿用的語義；PC 的刪整 U derivative／LP source 判定不可沿用。

不同列所有 Λ/R/空 fibres 必由同一原 U/L/S、attachments、contacts 與 rotation 生成。
若 γ 在 actual support 上恰為 πβ，同一色雙射 π 可搬該 piece 的全部 assignments、tuples
與 pins；組裝仍須回到共同 literal 色框，不能各件獨立選色名來拼來源。

## 5. β 的 zero slack 與原附件必要限制

對每個 b∈E_s(β)，令 C_T(b)={a:(a,b)∉A_T(β)}、V_b=C_L(b)∪C_S(b)。
原完整 degree4 contact slack 給 |C_T(b)|≤k_T^r。r-side retained factors F_j
的 incidence 記 n_j；spoke n_j=|F_j|=1，U 的 n_j=n_U。

\[
\begin{aligned}
D&=\sum_j(n_j-|F_j|),&O&=\sum_j|F_j|-|\bigcup_jF_j|,\\
\delta_b&=m_r-|C_L(b)|-|C_S(b)|,&
o_b&=|C_L(b)|+|C_S(b)|-|V_b|,\\
\lambda_b&=|V_b\setminus E_r^X|.
\end{aligned}
\]

所有項非負；|E_s|≥m_s−1≥1。对**同一 β 的每個 b**，已採納 S02／B-C2 給

\[
D+O+\delta_b+o_b+\lambda_b=\deg_X(r)-4=0.
\]

所以 |E_r^X|=m_r，r-side factors 兩兩不交；若 U 在 r，|F_U(β)|=n_U。
每欄 |C_L|=k_L^r、|C_S|=k_S^r、E_r^X=C_L(b)⊔C_S(b)，没有外溢禁色。
U 在 s 時沒有這項 r-side unary 等式；不能預填其 F_U(β) singleton。

更精確地，固定 s=b 的**每份**完整 T lift，在 k_T^r 個原 r-contacts 上恰見
C_T(b) 的 k_T^r 個不同色：禁色欄是所有這些 contact 色集合的交集，滿額迫每份
集合完全等於該欄。空 fibres仍照留，不能取一份方便的 witness 作整 relation。

原 N-diagonal 给全部 proper γ、全部 d 的 (d,d)∈A_S(γ)。所以 core β 上若
d∈E_r^X∩E_s，必由 L 禁 (d,d)。但 U 保留後可能擋住三色列的未用色 D，
E_r^X∩E_s 也可能空；不能抄整 U 省略的「共同 D 必在兩側」或「L 必禁 (D,D)」。
四色 proper 列更不預設未用色。這些 diagonal 查詢仍留在全部16 fibres中。

另有可直接重證的原附件必要式：若 v 是 T=L/S 的 s-contact、vh 是原 B attachment，
則 β(h)∉E_s。否則固定 s=β(h)，该點的 s／框限制重色，对任意 r pin 都產生
至少一點 strict degree-list slack，完整連通 T 可染，迫 C_T(s)=∅，違反正值滿額欄。
這重新核過 [PG-04 局部證明](../2026-10-09-n45-pg/REPORT.md)，不需其整 U 省略身份。

恢復 β 的 spoke 色 c=β(b_i)：若 c∉E_r^X，唯一 retained side factor 禁 c，
原 degree5 的新增一單位為 O=1；若 c∈E_r^X，每欄恰一 mixed 禁 c，新增 λ=1。
mixed owner 可隨 b 改變；unary blocker 不能冒充重色 spoke 套 E4-D。

## 6. 恢復 e 與新接受列的必要恒等式

对每份 proper literal γ、每個 root pin (a,b)，c_γ=γ(b_i)，有**整個 lift 集合**等式

\[
\mathcal L_G(\gamma;a,b)=
\begin{cases}\mathcal L_X(\gamma;a,b),&a\ne c_\gamma,\\
\varnothing,&a=c_\gamma,
\end{cases}\qquad
J_G=J_X\cap\{a\ne c_\gamma\}.
\]

因此指定 X 延拓要恢复成 G，必須其完整 lift 的 r 色避 c_γ。
新接受列 Δ=Σ(X)−Σ(G) 上 J_X≠∅，且**全部** X lifts 的 r 色恰 c_γ。
這是 spoke forcing；不是刪 U 時與原 U contact palette 同 singleton 的 forcing。

本輪另推得一個不需「拒絕」的同列恒等式。對任意 γ 的每個 b∈E_s，
令 N_b=|E_r^X−V_b|，所有 factors／columns在该 γ 重新计算。degree4 給
|E_r^X|=m_r+D+O，且
δ_b+o_b+λ_b=m_r−|V_b∩E_r^X|=m_r−|E_r^X|+N_b，故

\[
\boxed{D+O+\delta_b+o_b+\lambda_b=N_b.}
\]

在 γ∈Δ，spoke forcing 給 N_b∈{0,1}，至少一欄為1，因而 D+O≤1。

| Δ 上的 side slack | 必要完整欄形態 |
| --- | --- |
| D+O=1 | 每個 b∈E_s 都接受；mixed 三項全零；J_X={c_γ}×E_s，raw columns 分割 E_r^X−{c_γ}。 |
| D+O=0 | 空欄 mixed 三項全零；接受欄 mixed 三項之和為1，且唯一可用 r 色為 c_γ。 |

這個恒等式保留 U；不能套 PR 無 unary 特例，不能跨 γ 加禁色容量。
[B-C2 degree 計數](../../docs/c5_phase_b_common_lemmas.md)
是紙面推導依據；有限 checker 的1096個集合算術案例只校準恒等式。

## 7. 同一 X 的跨列域與實際單-root 重辨識

ε(X)=1，X 自己 β-minimal 给每條 retained 非框邊同 β witness，從而自己 Σ-critical。
沿 E2，Q(X) 只能空／單點／相鄰pair；此身份 β∈Q(X) 排除空：

| 原 Σ | Q(G) | 非空 Q(X) 必要域，再只留含 β 的項 |
| --- | --- | --- |
| 941 | {0,1,3} | {0},{1},{3},{0,1} |
| 933 | {0,1,2,3} | 四單點；{0,1},{1,2},{2,3} |

因此 Δ 非空：941 至少一列，933 至少兩列。933 的 q2 不漏；不預设 β 是 U 盾中點。
每個 Δ 的完整 spoke-forcing schedule 必與其余九列来自同一原圖。

X−s 的**实际原分量**可重新命名，但不收縮或替換：

| U owner | H_X−s 的完整分量 | 原 s contact 數 |
| --- | --- | --- |
| r | sole C={r}∪U∪L∪S | m_s=5−t_s |
| s | C={r}∪L∪S，及完整 U | (m_s,n_U)，和為5−t_s |

全部 C 點在 X 完整 degree4。C 的 relation 由原 pieces 接合時，必須留 r 色作額外
fibre 座標；丟掉它便無法核恢復 e。每份 C tuple／assignment 与实际 C edges 逐項對回。

X own minimality 迫 retained s-spokes 的 β 色互異。若 U在r，degree-list slack 與
每條 s-spoke 刪邊 β witness 另给精确 F_C=Col−{β(s-spokes)}=E_s。
若 U在s，必核完整 F_C∪F_U 與 spokes 覆蓋 Col，以及每條 retained contact 的 private witness；
不預设 C/U 的禁色角色。

下一輪可核的**舊定理映射目標，本輪不算新採納排除**：

| 實際 X 身份 | 原 BASE 目標與尚須逐項綁定的資料 |
| --- | --- |
| U在r，t_s=0／1／2 | sole C 的(5)／(4)／(3)：實際 C vertices、原 ordered contacts、同 β、精確 F_C、X own witnesses、外路及完整 r fibres。 |
| U在s，t_s=0 | no-spoke 的(4,1)／(3,2)：兩完整分量、private 禁色、原外hub路、contact assignments及全部空 fibres。 |
| U在s，t_s=1 | single-spoke 的(3,1)／(2,2)：完整 C/U 接合、實際 support、β witness、r fibres。 |
| U在s，t_s=2 | two-spoke 的(2,1)：兩原 spokes 的 literal 色、原分量及完整 tuples，整圖共同搬運。 |

映射入口：[no-spoke](../../docs/c5_no_spoke_exterior.md)、
[single-spoke four](../../docs/c5_single_spoke_four.md)、
[single-spoke three-one](../../docs/c5_single_spoke_three_one.md)、
[two-spoke three contacts](../../docs/c5_two_spoke_three_contacts.md)。
舊定理的來源排除、指定 X 延拓、恢复成 G 是三種不同結論，須按實際命題分開核。

## 8. 有限核對、版本與實際停止點

[checker.py](checker.py) 不 import 研究 checker；只重播51份 frozen inputs 中的19份既有 N2 原圖。
從 original edges 重建完整 components、contacts、shared identity、actual support，
以 MRV 完整回溯核 local tuples／全部 preimages，再与整圖直接全部 assignments 比較。
G 及每條具名 spoke 的精確 X=G−e，在十列核16 pins、空 fibres與恢复过滤。
未搜尋新圖／提高 k，也未作 graph-specific shield／rotation／criticality validator。

| 有限層 | 實算／判定 |
| --- | --- |
| 原 relation／joint／恢复介面 | 19圖、570 piece rows、9120 piece pin fibres；G3040、X7520整圖pin fibres；38 shared-contact incidences，完整 lifts 相等：**triggered and holds**。 |
| 原拒絕 row×spoke | 47 queries 全部 X 接受；全部 X lifts 的降度 root 色等於省略 spoke 的 literal 色；拒絕45／54 minimal來源：**not triggered**。 |
| long 控制 | 4份有long mixed，均缺原 b4 full B-touch，不能觸發來源盾弧支援等式；其 U 支援是三點，不能誤寫成short U。 |
| 完整 target Σ | 19圖的直接重建 masks 均有9個接受列，無933／941或whole D5像：**not triggered**。 |
| 集合算術 | 1096份非空E／raw-column案例驗N_b恒等式；列必要 masks與pair incidence splits：**triggered and holds**，純必要介面算術。 |
| 選定來源全契約 | 缺完整targetΣ、full B-touch long來源及拒絕minimal X；**not triggered**，沒有source排除／source實現。 |

正式有限證書為 [certificate-v2.json](certificate-v2.json)。第一生成的 `long_mixed=0`
inventory斷言失敗，原 log 保留於 [generation-attempt1.json](generation-attempt1.json)。
初版 [certificate.json](certificate.json) 誤把四份long控制的缺前提寫成short U；原 bytes 保留，
**不採用其 coverage metadata**。v2 按原邊更正為缺b4，另逐圖直接核完整Σ與touch，詳見
[checks.json](checks.json)。這些工具更正不改本輪紙面契約／必要式。

重播：

```sh
python3 -B audits/2026-10-10-n45-s-long-contract/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-10-n45-s-long-contract/checker.py --check
```

本輪普通／seed17重播、錯證書拒絕、exclusive-create拒覆寫、frozen inputs漂移核對及文件／
Lean build結果以 [checks.json](checks.json) 為準。沒有新增Lean theorem，build不能形式化本輪
紙面支援／拓撲論證。原盾弧與BASE圖類定理仍保其已採納紙面及外部degree-list／Gallai信任依賴。

**未解障礙 SL-SOURCE。** 要么供給同一原G的完整契約資料，要么在上述必要域內建立
任意大小來源反證；目前沒有把三件收成有限 coloring 模板的保relation定理。
仍需同時綁定十列 full joint／所有空 fibres、原 G各邊critical見證、X同β minimal見證、
原支援／附件／rotation與Δ forcing。Scalar profiles 或邊際關係不能代替這項同源義務。

**下一最小義務 SL-MAP。** 先核 U在r 的實際 sole C 對BASE(5)/(4)/(3)的完整前提映射；
U在s 保 C/U兩件與 r fibres，按 t_s=0/1/2核來源排除或指定延拓的精確種類。
有真pair／singleton S都须明列覆盖，恢复 e 維持§6的完整 lift 条件。
本輪停於契約與必要化約，不宣稱含long全排；無U（含兩long）、其他45／54身份、原55、
無45／54來源、一般N2／E及ε≥3仍OPEN。

L0新增此證據／來源报告；L1只連結N45權威入口、Kempe對應停止點與STATUS短索引。
既有兩short與整U排除不變；沒有closure／supersession，無L2觸發，HANDOFF／README無新路由變動。
本輪未commit／push／PR，舊worker／證書及歷史FAIL保留。
