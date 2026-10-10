# N45-U：整份原 unit unary 省略的窄排除與精確殘留

2026-10-09。任務 N45-U；執行者狀態：**完成第一批窄交付，待交叉驗收**。
BASE 與獨立 worktree HEAD 均為
`dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`，未提交。
輸出只在 `audits/2026-10-09-n45-u/`；`source/` 是保留的 detached BASE worktree。

**紙面結果：指定 N45-U 身份不可能有兩份原 unary；也不可能有兩份 short mixed。
剩餘必為恰一份原 unary U（即整份省略者）、一份 long mixed L 與一份 short mixed S。**
這不是全 N2、全部 45／54 或猜想 E 的排除。下列任意大小證明交 A 審閱；
固定 controls 只校準完整 relation 與必要式，沒有實現完整目標來源。

交付：[checker.py](checker.py)、[certificate-final.json](certificate-final.json)、
[inputs.json](inputs.json)、[checks.json](checks.json)、[residual.json](residual.json)。
所有重播使用本目錄保留的 BASE inputs，不混用主 worktree 的未提交路由修改。

## 1. 精確量詞、原身份與依賴

下文主命題量化所有滿足下列前提的 G、U、β、M，不限制 |U| 或 mixed 大小。

- G 有限簡單；有序 induced C₅ 外框 B=(b₀,…,b₄) 圍 disk 外面；
  完整有序 Σ(G)=933／941，或共同搬運**整圖**得到的 D₅ 像。
  每條非框邊對 Σ(G) critical；有效內部 H 忽略孤立內點，ε(G)=2。
- H 恰有非相鄰完整 degree-5 roots r,s，其餘點在原 G 完整 degree4。
  H−{r,s} 恰有兩份完整 mixed P,Q，其餘為 unary。
  r 表示 degree 下降側，因此同時涵蓋原 (4,5) 與 root 交換後的 (5,4)。
- U 是原 H−{r,s} 的完整 unary；唯一原 root-contact 是 rx，
  不要求 U 是 singleton，不要求每列 F_U 非空。
  X=G−V(U)=M 是 G 拒絕列 β 的 inclusion-minimal core；其自身 root degrees 是 (4,5)。
  全部其他原 pieces、附件、內邊、spokes 與兩份 mixed 都保留。
- 共同 canonical 色框中 q₀=01212/index6、q₁=01202/index4、q₃=01021/index1 拒絕；
  941 接受 q₂=01201/index3 與 q₄=01012/index0；933 拒絕 q₂、接受 q₄。
  T4={2,5,7,8,9} 全收。故本任務的 β 是三色列，933 的 β=q₂ 亦涵蓋。

沿 BASE 可用的推導是 H 連通、全 B-touch、兩 mixed 均有非空 actual support，
以及全部原 pieces one-sided。刪任一 mixed，另一份仍提供 r–s 原路；
刪 unary，原 roots 與其他 pieces 仍連通。
沒有把不同 β 的 core 拼成同一圖。

| 依賴 | BASE 段落／本輪使用 |
| --- | --- |
| 原省略身份 | [E3 nonadjacent §5](source/artifacts/c5_excess_two_e3/nonadjacent_notes.md#5-每列-q-core-的完整原省略分類)、[E4 §6](source/artifacts/c5_excess_two_e4/REPORT.md#6-完整原-relation-的參數化交付與-core-身份)：45／54 恰省一原 side unit，兩 mixed 保留 |
| E4-U／E2 | [CORE §2](source/artifacts/c5_excess_two_e4/CORE_CONSTRAINTS.md#2-n1unit-side-derivative-不必預填-criticality)、[E2 REPORT](source/artifacts/c5_excess_one_e2/REPORT.md)：先同 Σ minimalize，再用 ε≤1 的 Q 分類 |
| N-diagonal | [E4 §4.1](source/artifacts/c5_excess_two_e4/REPORT.md#41-新引理-n-diagonal只指定-nc-的局部-list-版本)：在原 G 的 full B-touch／one-sided 前提下，short mixed 接受每個 (a,a) |
| 原盾弧／B-S0 | [原盾弧 §2–4](source/docs/c5_unary_shield_budget.md)、[Phase B §2.1](source/docs/c5_phase_b_common_lemmas.md#21-b-s0有原見證的共同盾弧排除準則)：原 unary 付≥2，one-sided 盾弧邊互斥 |
| B-C2 | [Phase B §3.2](source/docs/c5_phase_b_common_lemmas.md#32-b-c2任意两自由roots的條件逐欄容量定理)：χ=0 的共同 β／pins 完整 joint 容量式 |
| U4 的搬用界線 | [U4 §2](source/docs/c5_excess_two_nonadjacent_two_mixed_core44.md#2-原支援下界盾弧與新的三-spoke收窄)：不搬 retained44／O11 的下界；本輪重新證小 incidence 下界 |
| 外部 degree-list | Dvořák，[List coloring and Gallai trees](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，Lemma7／Theorem10，PDF 第5–6頁：連通 degree lists 不可染時處處 tight，且圖為 Gallai tree。本輪重新讀取並保存 [PDF](gallai.pdf) 與 hash |

這些沿用的上游 paper／有限分類沒有在本輪全套重跑；其信任不能算作新 Python 或 Lean 證據。

## 2. N45-U-REL：完整 unary relation 與 contact 刪除等價

**量詞／前提。** 任意大小連通原 unary U，唯一 root 邊 rx，每個 U 點在原 G degree4；
任意共同 proper β。此局部結論不需 disk、Σ-critical 或 β-minimality。

以原唯一 contact x 定義 R_U(β)；每一 contact 色保存 U **全部頂點**的 full lifts，
滿足原 U 內邊及全部 U–B 附件。令 T_U(β) 為 x 色集合，

\[
 F_U(β)=\{a:\nexists f\in R_U(β),\ f(x)\ne a\}.
\]

暫不固定 r 時，U 的 lists 滿足 |L(v)|≥deg_U(v)，且 x 有至少一份 strict slack。
以 x 為最後點的生成樹貪婪染色給完整 lift，因此 T_U 非空。
於是 F_U={a} 當且僅當 T_U={a}；|T_U|≥2 時 F_U=∅。
**capacity-one 只表示原 incidence=1；F_U 允許空。**

令 K_X(β) 是 X 全圖染色的有序 (r,s) 投影；它仍帶所有 retained contact tuples 與全圖 lifts。
精確接回是

\[
 K_G(β)=\{(a,b)\in K_X(β):\exists f\in R_U(β), f(x)\ne a\}.
\]

刪唯一原 contact e=rx 後 U 不再接任何 root，前述 slack 對所有 proper β 仍成立。
因此 **K_{G−e}(β)=K_X(β)**，包括全部16 pins與空 fibres；但兩圖的頂點集合、
實際 U 與全圖 lifts 分開保存，沒有把 U 替成新頂點。

原 e Σ-critical 給非空 Δ=Σ(X)∖Σ(G)。對每個 γ∈Δ，
K_X(γ) 非空而 K_G(γ) 空，故

\[
 \pi_rK_X(γ)=T_U(γ)=F_U(γ)=\{a_γ\}.
\]

這是同一 γ 的**所有 X lifts**共同強迫，並非跨列相乘。
對本任務的 core 拒絕列 β，K_X(β) 本來就空，故不由這個論證推出 F_U(β) 非空。

**證據層：paper＋有限 Python。** 11份整 unit derivatives、110份 U 列中 F 空38列／singleton72列；
每份完整 R_U、原 contact、full lifts 都在證書。NA8-0003 原 U=P1={8,9}、contact x=9，
γ=index3=01201 時 T_U={1,2,3}、F_U=∅。這是「capacity-one 每列都 singleton」的具名負控制；
不是目標 933／941 或 N2 反例。

## 3. N45-U-WIT／N45-U-CROSS：原見證收費與跨列限制

**N45-U-WIT。量詞／前提：§1 的任意原 piece。** 取該 piece 的原 contact 邊 e，
選 γ_e∈Σ(G−e)∖Σ(G) 與完整 literal lift f_e。
限制到 G−piece 得合法 outside ψ_e，且不能填回完整 piece：否則會接受原拒絕列 γ_e。
原 degree4 給 degree lists；不可接回迫 tightness。
各 piece 的 γ_e 可以不同，亦可以不同於 core β。

對原 unary V，若 support 包含於框邊 hk 的端點，任取 B∖{h,k} 中的框点 t。
full B-touch 給 H−V 的原 t 附件；H−V 連通，故其 owner root 有避開 V 的內部路，
最後以該附件抵達 t，路內點不碰 B。這補齊 B-S0 的外路前提。
原短支援／hub 引理與 ψ_e 給矛盾，所以每份原 unary 支援≥3、原盾弧長≥2。
盾弧在同一 G 互斥。**即使 U 不在 M 中，它仍付原 σ_G(U)，不計 σ_M(U)。**

**N45-U-CROSS。量詞／前提：任意上述 unit derivative X，含保 B／T4／degree≥4，
不先假設 X Σ-critical。** ε(X)=1：刪去的 U 點在原 G surplus 都零，只使 r 降一度。
先取保 B、Σ(Y)=Σ(X) 的 inclusion-minimal Y。Y 自己 Σ-critical；
E4-U 的 exact surplus difference 給 ε(Y)≤1，E2 給 Q(X) 空、單點或相鄰二點。
本任務另有 X=M 的 β-minimality，可獨立推出 X 每條非框刪邊接受 β，
但上述跨列式不需要預填這項性質。

以下 q 下標是 C₅ singleton 位置，並非 cells index；每格還必須含 core β。

| 完整 Σ(G) | β | Q(X) 的全部容許必要值 |
| --- | --- | --- |
| 941 | q₀ | {q₀}、{q₀,q₁} |
| 941 | q₁ | {q₁}、{q₀,q₁} |
| 941 | q₃ | {q₃} |
| 933 | q₀ | {q₀}、{q₀,q₁} |
| 933 | q₁ | {q₁}、{q₀,q₁}、{q₁,q₂} |
| 933 | q₂ | {q₂}、{q₁,q₂}、{q₂,q₃} |
| 933 | q₃ | {q₃}、{q₂,q₃} |

因此同一 X 不會同拒 q₃ 與 q₀／q₁；Δ 對941至少一列、933至少兩列。
Δ 上每列均有 §2 的整 U 強迫義務。表是 E2 後的有限 mask 算術，沒有宣稱實現。
所有 claim 共同交換 r,s 後成立。

## 4. N45-U-CAP：degree4 側的零餘額與原 U 的一單位位置

**量詞／前提。** §1 的同一 core 拒絕列 β、任意 b∈E_s(β)，用原 mixed 完整 tuples。
E_r^X 排除 X 的全部 spokes／retained unary 禁色；E_s 是未變的另一側。
令 m_r=k_P^r+k_Q^r、m_s=k_P^s+k_Q^s；兩者≥2。
對任何原 unary V，其 F_V 大小≤原 incidence n_V：選一個完整 lift，
所有被禁 root 色必出現在該 lift 的 contact tuple 中。故

\[
 |E_r^X|\ge m_r,\qquad |E_s|\ge m_s-1\ge1.
\]

B-C2 可對同一 β 的全部 b∈E_s 使用。χ=0，deg_X(r)=4，故

\[
 D_X^u+O_X^u+\delta+o+\lambda_X=0.
\]

每項非負，所以全部為零；尤其對**每個** b∈E_s，

\[
 |G_P(b)|=k_P^r,\quad |G_Q(b)|=k_Q^r,\quad
 G_P(b)\cap G_Q(b)=\varnothing,\quad G_P(b)\cup G_Q(b)=E_r^X.
\]

這是完整原兩mixed的逐欄必要剛性；不從端點 marginals 推 relation。
恢復 U 後右側變1，原 G 的一單位只可能放在下列一處：

| 同一 β 的 U | (D_G^u,O_G^u,δ,o,λ_G) |
| --- | --- |
| F_U=∅ | (1,0,0,0,0) |
| F_U={a} 且 a∉E_r^X | (0,1,0,0,0) |
| F_U={a} 且 a∈E_r^X | (0,0,0,0,1) |

證明：兩mixed的 raw columns 未變；D 增 1−|F_U|，O 增 |F_U∖E_r^X|，
由 E_r^X⊆G_P(b)∪G_Q(b)，λ 增 |F_U∩E_r^X|。
不能把此 β 的一單位與 γ_e 或 Δ 的其他列容量相加。

**證據層：paper＋固定 Python。** 四個 N1 整 unary omission controls 觸發四份低度側欄，
都是 λ 型；r=6 的 NA8-0010 校準 root 交換。D／O 型及 N2 拒絕 derivative 欄無 controls。
原 G capacity 觸發90欄；unit X 觸發12欄（兩方向合計），均滿足自身 degree−4。

## 5. N45-U-S3：總 root incidence 至多三的 mixed 必有二點支援

**量詞／全部前提。** 任意有限簡單 disk G，原有效 H 連通且 full B-touch，
恰兩 roots r,s；P 是 H−{r,s} 的原 mixed，每點原 degree4，H−P 連通，
P 有一条 Σ-critical 原 contact，且 k_P^r+k_P^s≤3。
不需要 P 為 singleton、兩-root44身份、T4 或指定 β；γ_e 可是另一列。
**結論：|N_B(P)|≥2。**

反設 P 至多碰一框點 h。§3 的 contact witness 给 P 不可染的 degree lists，
所以由外部 Gallai 定理，P 是 Gallai tree。

先排 K₄ block J。每個 J 點已占三條 clique 邊，原 degree4 只剩一個外接方向。
若該方向沿 P 中 bridge 進入支枝 T，因 J 是 block，四條支枝互斥且不能返回另一 J 點。
T 必有到 G−P 的附件：否則 T 各點原 degree4，唯一離開 T 的邊是進 J 的 bridge，
握手式 4|T|=2|E(T)|+1 矛盾。故四個 J 點各有互斥 tethers 到 G−P。
H−P 連通，且至少四個框點有 H−P 附件，B 連通，所以 G−P 連通。
將這個外部及 tethers 尾部合成 hub，配四個 J singleton bags 得原 K₅ minor。
K₅ 或更大 clique block 本身已非平面。故 Gallai blocks 只剩 bridges／odd cycles。

每個 P 點至多一條 B 邊，故其 root incidence 至少 3−deg_P(v)。

- 多block時至少兩個末端block。末端bridge的 private leaf 消耗≥2條 root 邊；
  末端odd cycle至少兩個 private degree-two點，合計亦≥2。
  兩個互斥 private 集總消耗≥4，矛盾。
- 單block singleton 的 degree≤兩root加一框點=3；单bridge兩點合計需≥4 contacts。
- 單odd cycle長 n≥3，每點需≥1 root contact；≤3预算只剩 triangle，
  且每點恰一原root邊及一條到同一 h 的原附件。
  取 Y=(H−P)∪(B∖{h})，full B-touch 使 Y 連通，且由框邊與 h 相鄰。
  三個 P singleton bags、{h}、Y 兩兩相鄰，得到原 K₅ minor。

全部可能均矛盾。此論證涵蓋任意大小 Gallai tree，沒有小圖枚舉完備性假設；
所有收縮只證非平面性，沒有作染色替換。

**證據層：paper＋外部 Gallai；Python 22份實例只核必要結論。**
19個 N2 中11圖 full B-touch，22 mixed 均 incidence≤3且 support≥2。
singleton-support 反證支枝、K₄ block／長 Gallai tree 沒有目標來源 controls。
本 claim 不給 incidence≥4 mixed 的普遍支援下界。

## 6. N45-U-U2：兩份原 unary 子族排除

**量詞／前提：§1 全部來源／省略前提，另有兩份不同原 unary U,V；
其 contact capacities 任意，只有省略者 U 的 incidence=1。**

兩 unary 原盾弧各≥2；若任一 mixed long，另付≥2，總6>5。
故兩mixed都 short，其 support 非空，皆包含於某條框邊端點（singleton 亦包含）。
原 G 的 N-diagonal 给兩mixed接受全部 (a,a)，原 relation 未被 U 省略改變。
X 在 β 拒絕，因此 E_r^X∩E_s=∅；否則同色 pins 與各整份原 lifts 接回 X。
用 §4 的度數下界，

\[
 m_r+(m_s-1)\le |E_r^X|+|E_s|\le4,
 \qquad m_r+m_s\le5.
\]

P,Q 各至少一條 r 邊與一條 s 邊，故各總 incidence≥2；合計≤5 使每份≤3。
§5 分別給兩mixed支援≥2；short＋原支援區間給原盾弧各≥1。
於是同一原 G 的四份不同 pieces 收費

\[
 1+1+2+2\le5,
\]

矛盾。**排除兩份原 unary 的 N45-U 子族。** 沒有沿用 U4 的 retained44 下界；
也沒有將 γ_e 與 β 的染色容量相加。
此證明其實只需 X 在某 proper β 拒絕，不需 X 的 β-minimality；原固定來源前提照保留。

**證據層：任意大小 paper＋外部 Gallai，待 A 驗收。**
固定保存資料沒有 N2 u=2 或 N2 45／54 unit omission antecedent；有限 coverage 為 not triggered。

## 7. N45-U-SHORT／N45-U-RES：只剩一 long／一 short 的原身份

§3 給原 unary 至多兩份，U 存在且 §6 排掉兩份，故**恰一份原 unary U**。
若兩mixed都 short，X 已無 unary。β 是三色列，令 D 為共同未用色。
所有原 spokes 均避 D；原 G 的 N-diagonal 给 (D,D)∈A_P(β)∩A_Q(β)。
將兩份原完整 lifts 在同一 β／D pins 拼回 X，會接受 β，矛盾。
**這排除恰一份 unary、兩short 的 N45-U 子族，且不要求 X 自己 full B-touch。**
若兩mixed都 long，與 U 原收費合計≥2+2+2>5。
故只剩一 long L、一 short S、唯一原 unary U 的身份。

保留的**精確必要式**如下，並保存於 [residual.json](residual.json)；不是來源構造。

\[
 t_r+k_L^r+k_S^r+1=5,\qquad
 t_s+k_L^s+k_S^s=5,\qquad k_L^r,k_L^s,k_S^r,k_S^s\ge1.
\]

- 原 U 與 L 的盾弧各≥2，S 非空 short。因此 S 原盾弧≤1。
  若 S 支援為真框邊兩點，三份盾長必為 (U,L,S)=(2,2,1)，
  U、L 各支援三個連續框點，全部五框邊費用用盡。
- 若 S 為 singleton 支援，σ_G(S)=0，§5 迫 k_S^r+k_S^s≥4。
  U／L 盾長只能 (2,2)、(2,3)、(3,2)；r 方向 k_S^r≤3、s 方向 k_S^s≤4。
  原 degree 預算仍須逐項核；不是列出的每個整數接線都有 disk 實現。
- β-minimal X 保留全部 spokes，故每個 root 的 spokes 在此 β 色互異；
  重色 pair 刪其中一條仍等價，會違反 minimality。
  X 沒有 unary，E_r^X、E_s 都含 D；short S 接受 (D,D)，
  因 X 拒絕，**long L 必禁止 (D,D)**。
- 對每個 b∈E_s，L/S 的原 forbidden columns 必滿額且互斥分割 E_r^X（§4）。
  對 Δ 的每個 γ，原 U 全 contact palette與 X 的 r 投影又須同為 singleton（§2）。
  這些在同一來源 G、共同色框中跨列成立，沒有獨立挑選各列 relation。

**下一個最小待補義務 N45-U-OPEN-L。** 在上述唯一 U／long L／short S 原身份中，
保全三份原 actual support／contacts／附件／rotation／bridges與完整十列 relations，
證明 L 在 β 禁止 (D,D)、且其全部 b∈E_s 欄滿額分割，同時相容於 Δ 上的 U／X
singleton forcing 是否可能。現在没有來源排除／實現定理；必要 interface 停在此處。
singleton S 另有 N45-U-OPEN-S4：總 incidence≥4 時，需原 critical witnesses 的
Gallai／外部 hub 義務；不得把 §5 的≤3下界外推。

## 8. 有限 controls、完整證書與 coverage

獨立 stdlib checker 不 import 舊 checker 決策邏輯。
先從 BASE 54檔原 edges 重建 m 作 inventory，保存舊 core fields 作比較／選取資訊。
完整重算19份 m=2 圖，另取4份保存的整 unary omission N1 controls：
NA8-0003/index0、NA8-0007/index3、NA8-0009/index0、NA8-0010/index0。
四份均驗 X 精確省略完整 U，且每條 retained 非框刪邊有 β full lift；
沒有重新枚舉全部 minimal cores，inventory 其餘 core 數是保存資料核對。

證書保留原圖 vertices／edges、完整 degrees、ordered distinct／shared contacts、owners、
全部 actual attachments／support、原 H／piece bridges、rotation／faces、原盾弧、
全部10列16pins（含 diagonal、空 fibres），每個 contact tuple 的全部 full piece lifts，
每個非空整圖 fibre 的 full graph lift，及原 contact 刪除的 outside 拒絕見證。
contact-edge G−rx 與整份省略 X 的字面 lifts 各自保存。

| 核對 | 數字與結果 |
| --- | --- |
| 固定原圖 | 23＝19 N2＋4 N1；沒有新圖族搜尋 |
| 原 whole-graph root-pair queries | 3680；完整 tuple join 與直接原邊回溯一致 |
| 原完整 piece relations／local pin fibres | 690／11040；tuple及全部piece lifts與保存資料相等 |
| full piece lifts | 2986 |
| 原非框刪邊 | 555；逐項 strict Σ-critical，保存所有新增 canonical rows 的 full lifts |
| 整 unit derivatives | 11＝7 N2＋4 N1；X 與 G−rx 各1760 root-pair queries |
| N1 unary omission minimal rows | 4，完整原2頂點 U，含 r,s 交換 |
| N2 unary omission minimal rows | **0**；7份 unit derivatives 均完整 Σ=1023 |
| 小 incidence 支援引理 | 22份 triggered and holds；singleton 反證分支沒有來源 control |
| G／X B-C2 | 90／12份欄 triggered and holds；未觸發逐項列原因 |
| unit 一單位位置 | 4份 N1 欄，全為 λ 型；D／O 型無觸發控制 |
| 過強「unit 每列 F singleton」 | **counterexample**：38個 F 空列；不是目標來源反例 |
| 完整 933／941、N2 45／54、兩原 unary 排除前提 | **not triggered**；逐項缺失前提在 coverage 中 |

有限資料沒有一份完整目標來源；没有將19圖無該 core 寫成來源不存在。
任意大小證明由 §2–7 承擔，Python 只做上述固定校準。
沒有新增 Lean source、theorem、native_decide 或 lake build 紀錄。

## 9. 重播、失敗保留、寫入範圍與返回格式

在 canonical Math root 可重播：

```sh
python3 audits/2026-10-09-n45-u/checker.py --check
PYTHONHASHSEED=17 python3 audits/2026-10-09-n45-u/checker.py --check
```

普通與 seed17 均 exit0，重建 final certificate 逐 byte 相等；checker 的73份監看檔零byte漂移。
正式證書7682242 bytes，SHA256
`1f7dc2f13fa372150f2d915fd10494986c2f0a3aa08fa965c8b2f013315980d0`。
生成只 open('xb')，`--check` 不寫；最後的 exclusive-create 拒絕及文件檢查見 checks.json。

首個草稿生成 exit1：誤將保存的 tuple dictionaries 與新 list of tuples 比較。
沒有寫證書；修正為比較 tuples **與全部 lifts**，第二次生成成功。
第二次的 [certificate.json](certificate.json) 是保留的初版控制證書，
補原 bridges與coverage後另 exclusive-create `certificate-final.json`，沒有覆寫初版。
舊生成失敗、版本hash與logs全部保留。

讀取的70份 BASE inputs與外部 PDF hashes 在 inputs.json；結束時逐份重核，source HEAD不變且工作樹乾淨。
主 worktree 既有 STATUS／guide／任務檔不屬本交付，本任務未寫它們或其他任務輸出。
收尾觀察到這三份路由文件在並行工作中均有 byte 漂移，main HEAD 仍等於 BASE；
接手與收尾的 hashes 原樣保留，不把路由漂移說成零漂移，也不混入獨立 BASE 數學輸入。
source worktree 的存在會加入一份保留文件副本；不能以 formal-docs 檢查代替主全工作樹檢查。
本輪只跑本任務重播與文件檢查，未跑 E3／E4／E4C 大枚舉、U1–U4、ES／ER 或 Lean。

| 文件／範圍檢查 | 實際結果 |
| --- | --- |
| BASE worktree `python3 scripts/check_docs.py` | **exit1**；586 Markdown／6982 links，兩個舊未跟踪產物在獨立 checkout 缺檔，見下列路徑 |
| BASE worktree formal DocGraph | exit0；62 documents／213 relations／5 families，0 errors／notes |
| 主 worktree whole DocGraph | **exit1**；62 duplicate-id errors，列出 canonical docs、既存 scratch副本及本輪保留的 source/docs；沒有刪副本隱藏失敗 |
| 本交付 whitespace／REPORT 本地路徑 | tracked `git diff --check` exit0；6份新文字的 no-index `--check` exit1且無diagnostic（有差異），另核逐行 trailing whitespace／末尾換行；詳細記 checks.json |

BASE 文件檢查的兩個缺路徑原樣保留：
`audits/2026-10-04-task-d5/c4/scope_ledger.json` 與
`audits/2026-10-04-task-d2/integration_doc_changes.diff`。
本輪沒有補造舊產物、還原大枚舉或改其歷史來源；formal DocGraph PASS 不是全域 PASS。

**Findings：** N45-U-F1＝capacity-one 不保每列 singleton，已有具名原2頂點 U／完整 lifts；
N45-U-F2＝N2 45／54 unit omission及兩-unary前提缺控制，保持 not triggered；
N45-U-F3＝incidence≥4 singleton mixed 的支援／hub 義務保 OPEN；
N45-U-PROV＝三份非權威路由輸入有並行 byte 漂移，權威70份 BASE inputs 無漂移。
首輪沒有完整目標來源反例，也未委派 sub-agents、commit、push、開 PR 或對外發訊息。

**統一返回。** 任務 N45-U；完成第一批窄命題／residual 交付，等待 A 的 paper audit 與 J 增量校準。
CLAIM：REL、WIT、CROSS、CAP、S3、U2、SHORT、RES；量詞／前提／依賴／scope見各節。
適用933／941、共同D₅、root交換、全部實際拒絕β（含933 q₂）；只研究整 unit unary 省略。
證據：paper／外部Gallai／固定Python；無Lean。可關閉的子型僅兩原 unary與兩short mixed。
仍 OPEN＝唯一U＋一long／一short 的完整同源跨列接合、spoke省略任務、其他core與一般N2／E。
交付SHA未提交，以 checks.json 的 payload hashes 凍結。

**父題／consumers核對。** BASE E4 §4.3／§6、Phase B §2.1、Kempe導覽§3／STATUS仍保留 N2 45／54。
本交付為未採納窄結果，不改權威父報告或路由；依任務交監督端驗收後再整合，傳播停在L2。
