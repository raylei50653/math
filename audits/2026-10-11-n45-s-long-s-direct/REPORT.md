# N45-S-LONG-S-DIRECT：U owner=s 的實際 C/U 四個 direct profiles

任務 ID：`N45-S-LONG-S-DIRECT`。工作目錄 `/home/ray/developer/ai/math`。
指定及實讀 HEAD：`f2692089ad4259808e27d9b7e882ac09505b180a`。
成果 **待獨立驗收**；不更新共享研究狀態。

**交付結論：四個指定 profiles 的任意大小紙面排除候選。**
在下列完整契約內，`t_s=0,(m_s,n_U)=(4,1),(3,2),(2,3)` 與
`t_s=1,(m_s,n_U)=(3,1)` 都能逐項接回 BASE 的來源排除。
反證完全在實際 X 內；pair／singleton S、全部允許原 incidence splits、
原 shared contacts、任意 piece 大小／bridge 長度／旁支深度均保留。
未發現數學映射所缺的 BASE 充分前提；這不是整個 U-owner-s 分支的閉合。

**另有 custody finding，並已停止相應有限重播：**
`artifacts/c5_no_spoke_exterior/observations.json` 現場存在，但指定 BASE 無此
Git blob，`git show` exit128。其 bytes 只隔離於 `quarantine/`，不作權威輸入，
不升格基準，不執行依賴它的 artifact replay。18 份實際凍結 BASE 文件／程式
均逐 byte 對回 Git objects；外部 Gallai 講義另列，不冒稱 BASE object。
見 [inputs.json](inputs.json)、[findings.json](findings.json) 與
[失敗紀錄](logs/freeze-additional.json)。紙面映射與此有限證書 provenance 缺口分列。

## 1. 十二項共同契約及本輪固定域

逐項保留 frozen [long-contract REPORT §1](frozen/audits/2026-10-10-n45-s-long-contract/REPORT.md)：

| ID | 本輪精確假設與資料義務 |
| --- | --- |
| K1 | 任意大小有限簡單 induced-C5 disk；B=(b0,…,b4) 具名有序；完整原 vertices、edges、rotation。 |
| K2 | 完整有序 Σ(G)=933／941 或共同整圖 D5 像；所有非框邊 Σ-critical。 |
| K3 | 有效 H 連通、ε(G)=2、原 full B-touch；非相鄰原 degree5 roots r,s；其餘有效原內點完整 degree4。自由孤立原點保存完整自由染色因子。 |
| K4 | H−{r,s} 完整原分量恰 U,L,S；U 只接其 owner，L/S 各接兩 roots；三件 one-sided、actual support 非空。 |
| K5 | L actual support 不包含於真框邊兩端；S 包含於某真框邊兩端，真 pair／singleton 分列；不假設 S 單頂點。 |
| K6 | 只省略具名原 spoke e=rb_i；V(X)=V(G)，E(X)=E(G)−{e}。原 U/L/S、全部 contact 邊、attachments、bridges 保留。 |
| K7 | X=G−e=M **自己**是同一 literal β 的 inclusion-minimal 拒絕 core，X root degrees=(4,5)。 |
| K8 | 本輪固定原 U owner=s，n_U≥1；shared r/s contact 是單一 actual vertex／tuple 座標。 |
| K9 | 跨列固定 named/ordered contacts、ownership、edges、actual supports、bridges、rotation、框順序；D5/S4/root swap 只能共同搬運整份資料。 |
| K10 | 十列各保存全部16 ordered root pins、diagonal、空 fibres；完整 contact tuples 的全部 preimages 及 full lifts。 |
| K11 | 原 G 每條非框邊 f 的 Σ-critical witness 是自身 G−f 的某 γ_f 完整 lift；不同 f 的列可不同。 |
| K12 | X 每條 retained 非框邊 f 有 **同一 β** 的 X−f 完整 witness；不從 G−f 借 minimality；恢復 e 另核 r 色。 |

本輪只處理下列互斥 profiles，顺序固定為 `(m_s,n_U)`：

| profile ID | t_s | (m_s,n_U) | BASE 目標 |
| --- | ---: | --- | --- |
| NS41 | 0 | (4,1) | no-spoke (4,1) |
| NS32 | 0 | (3,2) | no-spoke (3,2) |
| NS23 | 0 | (2,3) | no-spoke (3,2)，只交換 theorem dummy roles |
| SP31 | 1 | (3,1) | single-spoke (3,1) |

每案仍有 `m_s+n_U+t_s=5`。以下不假設 β 是 U 盾中點，不重開整 U 省略、
兩 short 或 U-owner-r 已採納分支，不擴 graph/k。

## 2. 重建實際 X 的原點、原邊、degrees、contacts 與 supports

令原 r/s 對 T=L,S 的 contacts 為 P_T^r/P_T^s，U 的 contacts 為 P_U。
在有效內部，實際 H_X−s 的完整兩分量是

\[
V(C)=\{r\}\cup V(L)\cup V(S),\qquad
E(C)=E(L)\cup E(S)\cup E(r,L)\cup E(r,S),
\]

以及 **完整原 U**。L/S 各有 r-contact，所以 C 連通；U 連通。
無 C–U、r–U、rs 或 inter-piece 邊。自由孤立點另乘全因子，不冒作有效分量。
P_C=N_L(s)∪N_S(s)、P_U=N_U(s)，依原 s-contact 資料的限制順序，
不先按件重排。兩集互斥，大小 m_s、n_U；同件 shared r/s contact 的两條邊
作用於同一 actual vertex，絕不創造第二座標。

X 中 s 是唯一完整 degree5 有效內點，r 因只刪 e 降為完整 degree4；
C/U 其餘有效點仍完整 degree4。逐點核為

\[
\deg_D(v)+1[v\in P_D]+|N_B^X(v)|=4\quad(D=C,U),
\qquad N_B^X(r)=N_B^G(r)\setminus\{b_i\},\quad r\notin P_C.
\]

原 G 的 r 身份是 `t_r+m_r=5`；X 的 r-spokes 為 t_r−1。
對 v∈T=L,S，原逐點身份是
`deg_T(v)+1[rv]+1[sv]+|N_B(v)|=4`，shared contact 計兩條原邊。
U 沒有 r 鄰居。actual supports 恰

\[
\operatorname{supp}_B(C)=N_B^X(r)\cup\operatorname{supp}_B(L)
 \cup\operatorname{supp}_B(S),\qquad
\operatorname{supp}_B(U)=N_B^G(U).
\]

每一附件仍是原具名邊；沒有以 support 集取代各點鄰接。
原 disk embedding restricted 到 X，B 邊全留。long-contract §3 的 U/L 盾支援
聯集給 X 自己 full B-touch；本輪外路只需兩件 actual support 非空。
每條 retained f 的 X−f 同 β witness 來自 K7/K12，與 G 的 γ_f witnesses 分開。
沒有提供一張實現這些假設的 finite source；以上是對任意假設來源的重建公式。

## 3. 完整 assignments、全部 r fibres 與恢復 e

Col={0,1,2,3}。十個 literal representatives 依序為
`01012,01021,01023,01201,01202,01203,01212,01213,01231,01232`。
q0,…,q4 對應 literal indices `(6,4,3,1,0)`；T4 indices 為 `(2,5,7,8,9)`。
933 的 q-position 2 是 literal `01201`，保留其全部資料；不誤作 literal index2。

對每個 proper γ，Λ_T^r(γ;a) 是 T=L,S 的全部完整 assignments，滿足
全部原 internal edges／actual B attachments，且全部 P_T^r 避 a；
**此處不 pin s，不加 s-contact 避色**。令 A_r^X(γ)=Col−γ(N_B^X(r))。則

\[
\Lambda_C(\gamma)=\coprod_{a\in A_r^X(\gamma)}
 \{r\mapsto a\}\times\Lambda_L^r(\gamma;a)\times\Lambda_S^r(\gamma;a).
\tag{J1}
\]

原頂點上的 restriction／union 互逆：所有 C 邊正是 §2 列出的原邊，
L/S 互斥，r/shared-contact 限制仍作用於同一變數。
U 用其全部原 internal/B 邊的 Λ_U(γ)，不預填 U 的禁色。
投影到原 ordered P_C/P_U 得 R_C/R_U，每個 tuple 保存全部 preimages。
令 Φ_C(γ;τ,a) 為 tuple τ、r=a 的全部完整 C assignments；
對 **所有** `(τ,a)∈Col^{P_C}×Col` 保存 ambient fibres，含空者。
Φ_U(γ;υ) 亦保存全部 preimages，不能從已 pin s 的 relation 量化掉 s 後冒稱 J1。

對全部16 ordered root pins (a,b)，令 A_s(γ)=Col−γ(N_B(s))，完整 lift 等式是

\[
\mathcal L_X(\gamma;a,b)\cong
1[b\in A_s(\gamma)]
\coprod_{\substack{\tau\in(Col\setminus\{b\})^{P_C}\\
                  \upsilon\in(Col\setminus\{b\})^{P_U}}}
\Phi_C(\gamma;\tau,a)\times\Phi_U(\gamma;\upsilon)\times Col^{I_{\rm free}}.
\tag{J2}
\]

diagonal 与全部空 cells 保留。恢復 e 在 **同一完整 lift** 上精確過濾：

\[
\mathcal L_G(\gamma;a,b)=
 \begin{cases}\mathcal L_X(\gamma;a,b),&a\ne\gamma(b_i),\\
 \varnothing,&a=\gamma(b_i).\end{cases}\tag{J3}
\]

本輪反證不需恢復 e，但不丟此 r 座標。J1–J3 是紙面集合雙射，
本輪沒有將其說成已在 finite source 上逐項枚舉核對。

## 4. 同列不可刪減覆蓋、private color 與完整 contact witnesses

對 D=C,U，以全部完整 assignments 定義

\[
R_D(\gamma)=\{(f(v))_{v\in P_D}:f\in\Lambda_D(\gamma)\},\qquad
F_D(\gamma)=\bigcap_{\tau\in R_D(\gamma)}\operatorname{set}(\tau).
\tag{F1}
\]

未 pin s 時 L_γ(v)=Col−γ(N_B^X(v)) 满足
`|L_γ(v)|≥deg_D(v)+1[v∈P_D]`。D 連通且 P_D 非空；以一個 strict-slack
contact 為根由葉向根貪婪，故 R_D 非空，`|F_C|≤m_s`、`|F_U|≤n_U`。
F1 是完整 tuples 的交集，不是 contact marginals 的交集。

X 拒絕 β與 J2 給 `A_s(β)⊆F_C(β)∪F_U(β)`。
X-own minimality 使 retained s-spokes 的 β 色互異：重色時刪一條不改約束，
仍拒絕，違 K12。刪任一 retained s-spoke sb_j 的完整 β witness 必取
`s=β(b_j)`，否則已可恢復該邊；其完整 C/U assignments 皆避此色。
所以每個 spoke 色均不屬兩 F，從而

\[
F_C(\beta)\cup F_U(\beta)=A_s(\beta),\qquad |A_s|=4-t_s.\tag{F2}
\]

刪某 D 的 retained s-contact 邊，K12 給同 β full witness。
它在另一完整分量仍合法，s 色 d∈A_s 不被另一分量禁；
若 d 也不被本分量禁，便能用完整 assignments 接成 X，矛盾。因此

\[
F_C\setminus F_U\ne\varnothing,\qquad F_U\setminus F_C\ne\varnothing.\tag{F3}
\]

更精確的局部 witness 沿 BASE interfaces §3：對任何 proper γ、d∈F_D(γ)，
再對 P_D 刪色 d 的 lists M_d(v) 有 degree-list 下界；不可染迫處處 tight。
刪一條 contact 邊即新增該點的 d，連通 slack-greedy 可染。
其完整 tuple 恰在該具名座標出現 d，其餘接點全避 d；否则原查詢已可染。
C witness 保留實際 r 色，允許它依 j,d 改變，不宣稱全部 r fibres 非空。
碰 D 的原 internal/B 邊解除亦如 BASE degree-list 引理：非bridge 留連通 slack，
bridge 兩側各有 endpoint slack。此核對適用於 X 自己的 degree4 D。

| profile | F2/F3 及容量強迫的全部必要大小形態 |
| --- | --- |
| NS41 | F_U={u}，F_C=Col−{u}，恰三禁色。 |
| NS32 | (|F_C|,|F_U|,|交集|) 為 (2,2,0)、(3,1,0)、(3,2,1)，故 |F_C|≥2。 |
| NS23 | 為 (1,3,0)、(2,2,0)、(2,3,1)，故 |F_U|≥2。 |
| SP31 | F_U={u}，F_C=A_s−{u}，恰兩禁色；唯一 spoke 色在兩 F 外。 |

這是必要形態，不是可實現圖清單。private/exact covering 只在同一 β 主張；
其他 γ 的 F 允許空，所有列仍來自同一原邊與 actual attachments。

## 5. BASE 充分前提的逐項映射

β被 X 拒絕即被原 G 拒絕；完整933/941接受全部 T4，故 β是三色 proper C5 row。
一次共同整圖 D5/S4 可將它呈現為 q=01012，須同搬 G/X/e、原邊、rotation、
contacts、attachments、十列 relations、全部 preimages、root pins 及 witnesses。
BASE 已涵蓋任意 spoke 位置／private 禁色，不另固定 spoke 色或 u。
不要求 Σ(X)=933/941，亦不要求第二列拒絕或 β 是 U 盾中點。

| BASE 充分前提 | 實際 X 的供給與核對 |
| --- | --- |
| finite simple induced-C5 disk、有效 H 連通 | 原 G restricted embedding；只刪 spoke，原 H 不變，B 邊全留。 |
| 核心自己 edge-minimal q-obstruction | K7/K12，整圖共同搬 β；不是 G 的跨列 criticality。 |
| 唯一完整degree5 root，其餘有效內點完整degree4 | z=s；§2 逐點原邊身份，r 的 lists 使用 N_B^X(r)。 |
| 實際完整分量、相異 ordered contacts、actual supports | §2 恰 C/U，全部原點／邊／附件，§3 完整 fibres。 |
| 不可刪減同列 covering、各分量 private color | §4 F1–F3，由完整 assignments 與同 β witnesses。 |
| no-spoke 真外 s–B 路避指定分量 | 選 C 時取 Q_U；選 U 時取 Q_C，見下。 |
| connected-exterior K4 排除 | no-spoke 以另一完整分量 Q 補 hub；single-spoke 以 retained sb_j 補 hub。 |
| 三／四接點拒絕 palettes、原 tethers、K5 十鄰接 | §§6–7 的任意大小 block／degree 論證和具名原邊證書。 |

**真實外路。** 對選定原 C，取 U 的任一 actual s-contact，沿完整連通 U
到一條 actual U–B attachment，得 `Q_U=s w_0…w_k b_j`，內部完全在 U。
對選定原 U，取 L 的任一 actual s-contact，沿完整連通 L 到 actual L–B attachment，
得 `Q_C=s p_0…p_k b_j`，內部在 L⊆C。兩路均在 X，第一次碰 B 即止；
不使用省略 e，不需 retained r-spoke。L/U 原 support 非空由 K4/K5 提供。
BASE no-spoke §2 另可由 private F 的全分量 S4 不變性推得每件碰 B。

**K4。** 對 D=C/U，取其一個真禁色，tight degree-lists／Gallai 適用。
若 J 是 K4 block，其四點完整 degree4 各恰一條外方向，到 B∪{s} 或沿原 bridge
進互斥支路。刪該 bridge 後兩側可染；拒絕迫兩側 roots 可取色集為同一 singleton。
支路若不碰 B∪{s}，全部 lists 是 Col，可全域換色，不能 singleton，矛盾。
所以四條原 tethers 存在，內部互斥。no-spoke 中 Q 的內部在另一分量，
將 B、{s}、Q 與四條 tethers 去掉 J 端點後部分合成連通 O；
四個 J singleton 與 O 的六 clique 邊／四 tether 首邊给 K5。
single-spoke 直接用 retained sb_j 連 B∪{s}，同一論證適用。
這精確核對 no-spoke §§2–3 與 tree-components §1；不把 t>0 lemma 直接偷套 t=0。

## 6. 原三／四接點 active 結構與 tethers 的任意大小推導

依 external degree-list/Gallai 定理，對同一完整 D 的每份拒絕 lists 有
blockwise-uniform palettes；incident palettes 同列互斥，聯集恰 list。
K4 已由 §5 排除，較大 clique 由 planarity 排除；其餘為 bridges/odd cycles。
同一 vertex–block incidence matrix I 的欄獨立：leaf block private vertex
先決定其係數，再移去該 block 歸納。此處保全部原 blocks，不分別挑方便子圖。

**三接點、至少兩禁色。** 選兩個真禁色 a,b；tightness 保接點的 boundary 色
避兩色，因此 list 差恰 `1_P(e_b−e_a)`。欄獨立給每個 palette 不變或恰交換 a,b。
同頂點同列 palettes 互斥；接點 incident 恰一個正 active block，其他 active 點
一正一負。完整 active incidence forest 有恰三葉，故只有一個非空分量；
葉公式 `3=2+Σ(deg−2)` 迫唯一 triangle，餘為原 bridge arms。
三臂終點恰原三 contacts，零臂允許，原長度任意且同 parity。
沒有 inactive block 介入兩接點間 active 路，也沒有額外 active 旁支。

triangle 每點已有兩 triangle 邊及一條 arm/contact 邊；完整 degree4
留恰一條其他原邊。它直達 B，或經原 bridge 進 inactive W。
W 不含任何 s-contact，不接另一分量，不回接 active 結構；三 W 互斥。
若 W 不碰 B，移去 W 後剩餘連通 D 在原 M_a 下有 slack，可染；
W 的 bridge root 在 W 內 degree3、其餘點degree4，全 Col lists 可染。
整支換色使 bridge endpoints 異色，便拼回被拒絕的 D，矛盾。
故有三條真 boundary tethers，內部互斥且避 triangle/arms/s/另一分量。
依 BASE three-one §§2–3，此證明不限制 piece、臂長或支路深度。

**四接點、三禁色。** 在同一 D 比較三份 palettes，欄獨立迫共同 τ：
`Iτ=1_P`。三色集 A_3、剩下一色 h 給正 palette `A_3−{d}`（odd cycle），
負 palette `{d}`（bridge）或 `{d,h}`（odd cycle），τ=0 者不 active。
正 block 不能是 bridge，此步需三份拒絕。接點一正、非接點一正一負，
每個 active forest 分量至少三葉；共四葉迫連通，葉公式迫兩 triangle。
負 triangle 要三個互異正 blocks，與只有兩 triangles 矛盾。
兩 triangles 因同列 palettes 不交而不能共享 cut vertex；負 bridges 只能
連兩個正 triangles，所以恰一條 bridge，contact arms 長度為零。
原角色為 `{a,b,x}`、`{c,d,y}`、原 bridge xy，原四 contacts 是 a,b,c,d。
左 triangle 三點各剩恰一原邊；同一 inactive-branch/slack 換色論證給三條
真 boundary tethers。依 BASE single-spoke-four §§2–4；不借 sole-component
spoke 前提作 no-spoke hub，hub 由 §5 的另一原分量路獨立提供。

## 7. 四案逐案排除、缺少前提及原邊 K5 證書

### 7.1 NS41：t_s=0，(m_s,n_U)=(4,1)

§4 給完整 F_U={u}、F_C=Col−{u}。原 C 是四接點、三拒絕、K4-free，
§6 迫兩正 triangles `{a,b,x}`／`{c,d,y}` 及原 xy。
外 Q=Q_U，其第一原邊為 s w_0。令 T_a,T_b,T_x 為左 triangle 真 tethers。
五個互斥連通 bags 為

\[
\{a\},\{b\},\{x\},Z=\{s,c,d,y\},\quad
O=B\cup\bigcup_{v=a,b,x}(V(T_v)\setminus\{v\})
  \cup(V(Q_U)\setminus\{s\}).
\]

十條原邊證書：`ab,ax,bx`；`as,bs,xy`；三 tether 首邊；`s w_0`。
Z 由原 sc/sd 与右 triangle 連通，O 由原 B、tethers、Q_U 去 s 後路段連通。
全部邊在 X，最後一條是 **原 U-contact**，不是 spoke。
符合 no-spoke §5 的四接點三拒絕排除。
**已證映射：全部；缺少數學前提：無；依賴：§§4–6、BASE no-spoke §5／four §§2–5、外部 Gallai。**

### 7.2 NS32：t_s=0，(m_s,n_U)=(3,2)

`|F_U|≤2` 與覆蓋四色給 `|F_C|≥2`，選 C 的兩個真禁色。
§6 給原 triangle v0v1v2、三完整 arms v_i…u_i、三真 tethers T_i。
令 V_i 為原臂全部頂點，Z={s}，

\[
O=B\cup\bigcup_i(V(T_i)\setminus\{v_i\})\cup(V(Q_U)\setminus\{s\}).
\]

五 bags 为 V0,V1,V2,Z,O。十條原邊證書：三 `v_i v_j` triangle 邊、
三 `s u_i` contacts、三 tether 首邊、`s w_0`（Q_U 的原 U-contact 首邊）。
臂零長／任意長、tether 共 boundary 終點都保互斥連通 bags；
正是 no-spoke §5 三接點至少兩禁色排除，反證在 X。
**已證映射：全部；缺少數學前提：無；依賴：§§4–6、BASE no-spoke §5／three-one §§2–3、外部 Gallai。**

### 7.3 NS23：t_s=0，(m_s,n_U)=(2,3)

`|F_C|≤2` 迫 `|F_U|≥2`。只在 theorem dummy variables 中設定
`D_active=完整原 U`、`D_outside=原 C`、z=s；**原 C 名稱和完整 r fibres 不變**。
對原 U 的三原 contacts 用 §6 三接點定理；Q=Q_C 由原 s–L contact 起，
沿原 L 到 actual L–B attachment。
沿 §7.2 bags 公式，arms/tethers 全在 U，Q 的內部在 L⊆C；
最後原邊證書是 `s p_0`（原 C 中的 s–L contact），其餘九條仍为
三 U triangle 邊、三原 s–U contact 邊、三 U tether 首邊。
使用 Q 不收縮或更換原 C 的 coloring relation，§3 Φ_C(γ;τ,a) 原封保留。
**已證映射：全部，含 role swap；缺少數學前提：無；依賴同 §7.2，另需 §3 保原 C／r fibres。**

### 7.4 SP31：t_s=1，(m_s,n_U)=(3,1)

唯一 retained **原 s-spoke** 為 sb_j，c_sp=β(b_j)。
`F_U={u}`、`F_C=(Col−{c_sp})−{u}` 恰兩真禁色。
原 B∪{s} 經 retained sb_j 連通，K4 的 hub 前提直接吻合，毋須 Q。
§6 三接點結構給原 C triangle/arms/tethers。
令 Z={s}、V_i 為原三完整 arms，`O=B∪⋃(V(T_i)−{v_i})`。
十原邊為三 triangle 邊、三 `s u_i` contacts、三 tether 首邊、**retained sb_j**。
完整 U、其 contact／全部附件仍在 X，仅未用於 minor。
符合 single-spoke-three-one §§1–4、所有 spoke 位置與 private 色 u，反證在 X。
**已證映射：全部；缺少數學前提：無；依賴：§§4–6、BASE tree-components §1／single-spoke-cores §2／three-one §§1–4、外部 Gallai。**

以上為對每個假設來源可提取的 **具名原邊證書 schema**，不是已實現來源的
數值 adjacency list；不存在有限原 source 時不捏造其頂點／邊紀錄。
minor 只反證平面性，不作保 Σ 的 coloring replacement，不需先恢复 e。

## 8. pair／singleton 與全部允許原 incidence splits

令 x=k_S^r、y=k_S^s，則 k_L^r=m_r−x、k_L^s=m_s−y。
long-contract §3 給 `(t_r,m_r)=(1,4)` 或 `(2,3)`。
每個表項均量化其全部 actual named contact realizations、overlaps、rotation、
attachments 和逐點完整 degree 身份；表是 **必要算術域**，不是來源實現。

**Pair S：** whole-graph U012/L234/S40 presentation 的原 PG 幾何迫
`t_r=1,m_r=4`，原 e=rb4，若有 s-spoke 其端點在 b0/b2。
這個幾何 presentation 與 β→q 只能共同搬運，不獨立硬固定兩份 normalization。
全部正 splits：`x∈{1,2,3}`、`y∈{1,…,m_s−1}`。

| profile | pair 的 (x,y) 完整域 | raw split 數 |
| --- | --- | ---: |
| NS41 | {1,2,3}×{1,2,3} | 9 |
| NS32 | {1,2,3}×{1,2} | 6 |
| NS23 | {1,2,3}×{1} | 3 |
| SP31 | {1,2,3}×{1,2} | 6 |

**Singleton S：** 保原單點 support，盾弧配置 `(2,2,0),(2,3,0),(3,2,0)`
全留；不預設 singleton 框位置。沿已採納必要式 `x+y≥4`：

| profile | (t_r,m_r) | 全部 (x,y) |
| --- | --- | --- |
| NS41 | (1,4) | (1,3),(2,2),(2,3),(3,1),(3,2),(3,3) |
| NS41 | (2,3) | (1,3),(2,2),(2,3) |
| NS32 | (1,4) | (2,2),(3,1),(3,2) |
| NS32 | (2,3) | (2,2) |
| NS23 | (1,4) | (3,1) |
| NS23 | (2,3) | 無，因 x+y≤3；不是 finite source 零觸發排除。 |
| SP31 | (1,4) | (2,2),(3,1),(3,2) |
| SP31 | (2,3) | (2,2) |

§7 每案不挑某一 split，故上述所有必要 splits 全覆蓋。
每一原同件 r/s 接點可 shared 或不同，只受原圖 simplicity／degree／rotation
约束；沒有以兩件 marginals 認證 shared-contact 可實現性。

## 9. 依賴、凍結、核對與證據分層

紙面直接依賴均為指定 BASE 的 frozen bytes：interfaces §§1–4；
no-spoke §§1–3、5；single-spoke-cores §§1–3；three-one §§1–4；
four §§1–5；tree-components §1；long-contract §§1–7；
long-r-map 仅保留此前 unpinned-s/r-fibre 方法及 owner-s OPEN 邊界。
本輪沒有借同批其他任務的新結果。三份只讀子核對属于本任務內部核對，
各只讀本目錄 frozen inputs；根端已重讀關鍵論證，不構成獨立採納。
見 [reviews.json](reviews.json)。

外部信任單列：
[Dvořák《List coloring and Gallai trees》](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
的 Lemma 7／Theorem 10。已實讀講義 PDF 第5–6頁：connected degree assignment
不可染時處處 tight，並有 Gallai/blockwise-uniform 刻畫。講義 PDF 的 byte hash、
URL、抓取時間列在 inputs.json 的 external_inputs；不稱它為 BASE Git theorem
或本輪 Python／Lean 證明。本輪原 active-tree／外路／tether／K5 推導仍由 §§5–7 承擔。

| 證據層／控制 | 本輪狀態及界線 |
| --- | --- |
| 任意大小紙面候選 | 四案映射及 X 內原邊 K5 反證成立於完整契約，待獨立驗收。 |
| 外部定理 | Gallai/degree-list 講義單列信任；已實讀，不是新正式化。 |
| NS41 finite source | **not triggered**；未建立、未執行 finite source，trigger_count=null。 |
| NS32 finite source | **not triggered**；未建立、未執行 finite source，trigger_count=null。 |
| NS23 finite source | **not triggered**；未建立、未執行 finite source，trigger_count=null。 |
| SP31 finite source | **not triggered**；未建立、未執行 finite source，trigger_count=null。 |
| BASE artifact replay | **not triggered**；SOURCE-ARTIFACT-NOT-IN-BASE，未執行，無 PASS。 |
| 來源實現 | 未建立；本輪沒有聲稱任何 target graph 存在或來源 oracle 完備。 |
| Lean | 未新增 theorem，未執行 lake build；紙面拓撲未 Lean 化。 |
| 交付結構／hash 核對 | 獨立記錄實際命令／stdout／stderr／exit；通過只代表 bytes/custody。 |
| 一般命題 | 一般 N2/E、一般核心／共同出口及完整 owner-s 閉合均未主張。 |

claims.json 每項列量詞、前提、結論類型、證據、依賴及未解義務。
來源 finding 原 exit128 保留；正常／seed17及負控制僅驗交付結構／hash，
不將其當 source controls。零觸發不是來源排除；此處 source 根本未執行，
因此不用零冒稱 trigger 數。未重播 shared docgraph、舊 certificates 或 Lean。

[checks.json](checks.json) 保存正常／seed17 的 stdout/stderr byte equality，
及兩份刻意破壞 input/payload hash 的 metadata 各以 exit1 拒絕。
初始 setup 工具只回傳 merged stream，原 command/output 原樣保留，沒有捏造
分開 streams；`SOURCE-MISMATCH-additional.json` 另保實際 `git show` stderr。
後續 run_logged.py／seal.py 保存逐條實際 command、分開 stdout/stderr、exit。
見 [execution-notes.json](execution-notes.json) 與最終 [seal-receipt.json](seal-receipt.json)。

在 repo 根目錄可只讀重播交付驗證（不重建／覆寫 manifest）：

```sh
python3 -B audits/2026-10-11-n45-s-long-s-direct/validate.py --contents --manifest audits/2026-10-11-n45-s-long-s-direct/delivery.json
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-n45-s-long-s-direct/validate.py --contents --manifest audits/2026-10-11-n45-s-long-s-direct/delivery.json
```

## 10. 精確停止點與交付權限

停止於 **四個指定 profiles 全部的限定契約任意大小排除候選**。
每案已證映射、沒有缺少數學充分前提；未解義務為獨立驗收、外部／BASE 紙面信任
及正式化界線。另交 SOURCE-ARTIFACT-NOT-IN-BASE，不自行補造／升格有限證書基準。
U-owner-s 的 `(t_s,m_s,n_U)=(1,2,2),(2,2,1)`、其他含long身份、其他cores、
原55、一般N2/E仍在本任務之外；不得由本四案聲稱全部閉合。

只新增本專屬目錄，shared docs／舊 audits／證書及其他輸出只讀。
沒有 commit/push/PR 或外部訊息。delivery.json 逐檔列 SHA256，
明列 `delivery.json` 自身及 `seal-receipt.json` 為精確 metadata 排除，
不以萬用規則排除未知檔。驗收者可重算全部 frozen/raw/log bytes。
