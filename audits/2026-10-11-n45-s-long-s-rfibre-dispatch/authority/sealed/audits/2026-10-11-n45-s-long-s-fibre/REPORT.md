# N45-S-LONG-S-FIBRE：完整 C/U private covering、BASE 路由與原 spoke fibre 缺口

2026-10-11。BASE `f2692089ad4259808e27d9b7e882ac09505b180a`。
**交付為待獨立驗收的紙面候選與有限介面校準；不自行採納或更新共享研究狀態。**

結果：兩個指定 profile 都重證完整 C/U private covering。任意大小的同列
Gallai／原 block 論證排 singleton S 及 pair 的原 r-contact splits `(1,3)/(3,1)`；
pair 只剩 `(2,2)`。single-spoke 的必要表只剩 β singleton 在原盾框的 3／4；
two-spoke 只剩 0／2，且其兩禁色角色由實際五邊面推得，沒有預填 U 禁未用色。
two-spoke β=q0 的 q1 延拓另可用同源完整 fibre 雙射恢復原 `e`，排除 q1 原拒的
限定 profiles。其餘 X 延拓尚不能直接恢復原 `e`；本輪停在 §9 的具名原邊／literal／
完整 r-fibre 義務，**沒有排除全部 pair `(2,2)`，沒有一般含 long closure**。

## 1. 精確來源契約與凍結邊界

逐項保留 [long-contract §§1–7](../2026-10-10-n45-s-long-contract/REPORT.md)，另固定原 U owner=s。

| 契約 | 本輪完整前提／資料義務 |
| --- | --- |
| K1 | 任意大小有限簡單 disk G，原 ordered induced C5 `B=(b0,…,b4)`；完整 vertices、edges、rotation。 |
| K2 | 完整有序 Σ(G)=933／941 或整圖共同 D5 像，所有非框邊 Σ-critical。 |
| K3 | 原有效 H 連通、full B-touch、ε=2；非相鄰原 degree5 roots r,s，其餘有效原內點完整 degree4；自由孤立點另留全部 assignments。 |
| K4 | H−{r,s} 完整原分量恰 U,L,S；U 只接 s，L/S 各接兩 roots，原 one-sided、actual support 非空。 |
| K5 | L long：actual support 不含於真框邊兩端；S short：真框邊 pair／singleton 分開，S 不預設單頂點。 |
| K6 | 只省略具名原 `e=rb_i`；V(X)=V(G)，E(X)=E(G)−{e}，所有原 pieces、contacts、附件、bridges 全留。 |
| K7 | 固定原拒絕 literal β，X=G−e=M 自己是 inclusion-minimal β-core，完整 root degrees=(4,5)。 |
| K8 | 原 U 的 owner=s，n_U≥1；named/ordered/shared contacts 按實際 vertices，shared contact 只有一個座標。 |
| K9 | ownership、原 edges、attachments/support、bridges、rotation、框順序跨列不變；D5/S4/root swap 只共同搬整份資料。 |
| K10 | 十列、全部 16 ordered root pins、diagonal、空 fibres；每個完整 tuple 的全部 preimages、全部 full lifts。 |
| K11 | 原 G 每條非框邊各有自己的原 Σ-critical γ_f 與 G−f 完整 lift；不能當成 X 同β witness。 |
| K12 | X 每條 retained 非框邊有 X−f 的同一 β 完整 witness；恢復 e 另核同 lift 的 r 色。 |

只處理 `(t_s,m_s,n_U)=(1,2,2)`、`(2,2,1)`。H_X−s 的實際兩分量為
`C={r}∪L∪S` 及完整 U；m_s+n_U+t_s=5。不擴 graph/k、不重開整 U、兩 short、
owner-r 或其它 core 身份；[owner-r 後續](../2026-10-10-n45-s-long-r-map/REPORT.md)僅核 scope。
[N45 §§2.5–2.7](../../docs/c5_excess_two_nonadjacent_unit_core45.md)只供比较，沒有移植 HIGH。

[inputs.json](inputs.json) 凍結 58 份實讀 BASE Git blobs，逐份記原路徑、Git blob、
SHA256、原始 bytes 與 frozen path；讀取時 HEAD=BASE，當時工作樹乾淨。
補充輸入只增加已核同一 BASE 的 degree4 guide，不更新 BASE。外部 Gallai PDF 另凍結
`external/gallai.pdf`，標外部來源、Git blob=null，與 repo 權威分開。

**BASE finding：** `artifacts/c5_single_spoke_residual_locality/observations.json` 在磁碟存在，
但沒有指定 BASE blob。根 agent 的初步磁碟讀取在 admission 核對前發生，該內容已排除
於所有 claims／controls；不當替代 BASE。`git show` 的實際 exit128/stdout/stderr 及
physical SHA256 保在 [source-findings.json](source-findings.json)、`logs/missing-final-json.*`。
原 `(2,2)` observations、終局 `support_table.md` 與紙面報告都有 BASE blob，可分別使用。
沒有重播或重造缺少的終局 JSON。兩個不存在的探索文件及一次錯讀 `roots` key 的失敗也保留，
均不作数学依賴。

## 2. 尚未 pin s 的全部 assignments、tuples、preimages 與 r fibres

令 Col={0,1,2,3}；對每個 proper literal γ，Λ_T(γ) 是原 T 滿足全部
internal edges 與 actual B attachments 的完整 assignments。所有原 r/s contacts
仍在 T 裡，先只加 r 的避色，**不加 s 色**：

\[
\Lambda_T^\circ(\gamma;a)=\{f\in\Lambda_T(\gamma):
 f(v)\ne a\text{ for every }v\in N_T(r)\},\quad T=L,S.
\]

\[
\Lambda_C(\gamma)=\coprod_{a\in A_r^X(\gamma)}
 \{r=a\}\times\Lambda_L^\circ(\gamma;a)\times\Lambda_S^\circ(\gamma;a),
\quad A_r^X=Col-\gamma(N_B^X(r)).
\]

Λ_U(γ) 保留全部原 assignments。令原 ordered lists
`P_C=(u_L,u_S)`、`P_U=(v_1,…,v_n)`，其中 m_s=2 迫 k_L^s=k_S^s=1，
U 的 n=2／1。接點可同時是 r-contact，仍只用其原 vertex 的一個顏色。
按 P_C／P_U 投影得到完整 R_C、R_U，保留

\[
\Phi_C(\gamma;\tau,a)=\{h\in\Lambda_C(\gamma):h(P_C)=\tau,h(r)=a\},
\qquad \Phi_U(\gamma;\upsilon)=\{h\in\Lambda_U(\gamma):h(P_U)=\upsilon\}.
\]

ambient 為全部 `(τ,a)∈Col²×Col` 及 `υ∈Col^n`，**空 fibres 也有位置**。
每個非空 fibre 是全部 preimages，沒有選一份方便 coloring。restriction／union
在同一原 vertices／edges 上互逆，因此這不是先 pin s 再量化掉 s 的不完整 relation。

固定同一 s=b 後，全部 X lifts 精確為

\[
\mathcal L_X(\gamma;a,b)\cong
1[b\notin\gamma(N_B(s))]
\coprod_{\tau\in(Col-\{b\})^2,\,\upsilon\in(Col-\{b\})^n}
\Phi_C(\gamma;\tau,a)\times\Phi_U(\gamma;\upsilon)
\times Col^{I_{\rm isolated}}.
\]

這個雙射對全部十列、16 pins 與 diagonal 成立。某 piece 的支援列可由色置換搬運時，
只用雙射證明它的完整 assignments／preimages 同搬；接合前回到同一 literal 色框。
不同 pieces 不獨立正規化。所有跨列語義都来自同一 G。

本輪沒有供給符合 K1–K12 的 finite source，故這是任意大小的精確語義構造，
不是捏造具體來源的 tuple 數。§10 的實算只使用 BASE 已封存的 19 份控制原圖。

## 3. 用 X 自己的 β witnesses 重證 private covering

未 pin s 时，C／U 每點完整 degree4；boundary lists 滿足
`|L_γ(v)|≥deg_T(v)+1[v∈P_T]`。有原 contact 提供 strict slack，
connected spanning-tree greedy 保證 Λ_C、Λ_U 非空。定義

\[
F_T(\gamma)=\bigcap_{\tau\in R_T(\gamma)}set(\tau),
\quad E_s(\gamma)=Col-\gamma(N_B(s)).
\]

任取一份 tuple 得 `|F_C|≤2`、`|F_U|≤n_U`。固定 s=b 後不可染正好是 b∈F_T，
這只是特定共同避色查詢的投影，不能反推 R_T 或 r fibres。

先核 X own minimality：若兩 retained s-spokes 在 β 下同色，刪一條不改 constraints，
仍拒 β，矛盾。故它們的 β 色互異。對每條 sb_h 的 X−sb_h 完整 β witness，
s 必取 β(b_h)，否則原邊已可恢復，得到 X coloring。該 witness 的完整 C／U
assignments 都避此色，所以 `β(b_h)∉F_C∪F_U`。β 拒絕則給反向包含，得到

\[
\boxed{F_C(\beta)\cup F_U(\beta)=E_s(\beta).}
\]

對**每條** retained contact su_L／su_S，取 X−su_j 同β完整 witness w_j；
b=w_j(s)∈E_s，U 完整 assignment 避 b，所以 b∉F_U；原 X 拒絕，故 b∈F_C。
完整 C tuple 恰在被刪 contact 等於 b，其它 contacts 避 b（否則不能恢復／仍違反其它邊）。
這逐接點給 C 的 private witness。對每條 U-contact 同理給 `F_U−F_C` 中的色與
完整 U tuple／outside C assignment。它們的色可以隨原邊改變，沒有任選同一 witness。

對 internal／B-attachment incident edge 亦可用同β witness 取得其所在 component 的
private 色；[R10 分量解除 §§2–4](../../docs/c5_degree5_interfaces.md)以原 degree4
lists／slack 證每個禁色在刪任一 incident edge 後解除。刪 bridge 时兩側均有 slack。
所以每件 Private 非空，覆蓋由 X 自己證得；G 的 Σ-critical witnesses 沒有替代這一步。

| profile | 尚未加結構限制的完整 β 角色 |
| --- | --- |
| t_s=1，n_U=2，|E_s|=3 | `(1,2)`、`(2,1)`、`(2,2)` 重疊一色；每件各有 private 色。 |
| t_s=2，n_U=1，|E_s|=2 | C/U 是兩個不同 singleton，兩個次序都保留。若 E_s={c,Dβ}，先不指定誰禁 c／Dβ。 |

對 pair 禁色的二接點 relation，全部 tuples 必含那兩色，逐接點解除／greedy
給兩個交換 tuples，故完整 relation 恰為 `{(a,d),(d,a)}`。singleton 禁色的 relation
在 BASE 95 個 schemas 中；全部 preimages 與 C 的 r fibres 仍是來源特定資料。

## 4. 原 r-spokes、全部 splits 與新的同列排除候選

long-contract §§2–3 的原盾與 star 必要式給無 U 的 r：
`(t_r,m_r)=(1,4)/(2,3)`。這是原 G 身份，X retained r-spokes=t_r−1。

| S | 原必要 profiles（尚未用下列 Gallai 論證） |
| --- | --- |
| 真 pair | 共同整圖 geometry 成 `U012/L234/S40`；原幾何迫 N_B(r)⊆{b4}，故 e=rb4、t_r=1；r splits 全部 `(1,3),(2,2),(3,1)`。 |
| singleton | [S04](../2026-10-09-n45-s/REPORT.md)迫 k_S^r+k_S^s≥4；k_S^s=1，故 k_S^r≥3。m_r≤4、k_L^r≥1，迫 t_r=1、split `(1,3)`；t_r=2 沒有允許 split。 |

因此兩種支援都沒有 retained r-spoke，不把 pair 的 geometry 冒移 singleton。

Private_C 非空給某 `d∈E_s(β)` 使 C 固定 s=d 的 degree-lists 不可染。
[外部 Dvořák Lemma7／Theorem10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
使同一實際 C 為 Gallai tree。`B∪{s}` 由本题 retained s-spoke 連通，
[connected-exterior K4 lemma](../../docs/c5_degree5_tree_components.md#1-連通外框排除-degree-4-分量的-k4)
的完整 degree4、private pin、原 hub 路前提吻合，故 C K4-free；更大 clique 亦違反平面性。
C blocks 只能是 bridges／odd cycles。這條 hub 路在 X 裡，不用被省略 e。

C−r 的實際分量恰 L、S，所以 r 是 cut vertex，恰 incident 兩個 blocks K_L、K_S；
每件的所有 r-neighbors 正好是該 block 的 r-neighbors。r 無框鄰／s 鄰，deg_C(r)=4。
bridge 在 r 貢獻1，odd cycle 貢獻2；兩項和4迫

\[
\boxed{K_L,K_S\text{ 都是 odd-cycle blocks，}\quad k_L^r=k_S^r=2.}
\]

因此 singleton 的 `(1,3)` 與 pair 的 `(1,3)/(3,1)` 在本完整契約中是
**任意大小來源排除候選**；pair `(2,2)` 保留。不收縮或替換 L/S，s-contact
在 cycle 上／任意原旁支、cycle 長度、bridge 深度、其餘 blocks、所有 actual attachments 全保。

另對**全部 proper γ**證 `|F_C(γ)|≤1`：若禁兩色，
[BASE 任意列雙禁色 bridge-path 引理](../../docs/c5_single_spoke_two_two.md#雙禁色的同圖奇數-bridge-路徑)
迫兩個原 s-contacts 間的 block path 全為原 bridges。一 contact 在 L、一在 S，
路徑必通 r 並經 K_L、K_S，與它們為 odd cycles 矛盾。這一步不要求 X 是 γ-minimal。
故 β 角色進一步為

\[
t_s=1:\quad F_C=\{d\},\ F_U=E_s-\{d\}\text{ 恰 pair};
\qquad t_s=2:\quad F_C,F_U\text{ 為互補 singleton}.
\]

其它 γ 的 F_C 可以空；不能把 β 角色填滿十列。core 只有一個可用 s 色 d，
long-contract §5 的 r zero-slack 欄在此同一 d 給 `C_L(d)⊔C_S(d)=Col`、各大小2；
沒有把此 β 欄分配成每列的資料。

## 5. BASE 前提逐項映射及結論種類

把實際 X 記成 BASE 的 minimal obstruction，z=s、兩完整分量 C/U。

| BASE 前提 | 同一實際 X 提供 |
| --- | --- |
| finite simple induced-C5 disk、有效 H 連通 | 原 G 刪 e 的 restriction，原 edges／rotation；原 C/U 仍各接 s。 |
| own minimal q-obstruction | K7/K12，β 以一次共同 D5/S4 搬為 q=01012；全部 witnesses／contacts／e／Σ 同搬。 |
| 唯一完整 degree5=z，其他有效內點 degree4 | s=5；r 只刪 e 降4；原 pieces 全留。 |
| H−z actual components、原不同 ordered contacts | §2 的實際 C/U；分拆 `(2,2)`／`(2,1)`；不合併分量。 |
| T4 全收 | Σ(X)⊇Σ(G)，原 G 接受全部 T4；不設 Σ(X)=933／941。 |
| 完整 forbidden／private、actual support、slit/sector 幾何 | §2–3 的全部 assignments 与 X own witnesses；原 X embedding。 |
| 恢復原 spoke 的額外條件 | BASE 指定延拓沒有提供；須 §8 的同一 full lift r≠γ(b_i)。 |

pair geometry 一次共同搬成 `U012/L234/S40` 後，actual support
`N_B(C)=0234`、`N_B(U)=012`、e=rb4、s-spokes⊆{b0,b2}。
**Q(G) 同時搬成原 target mask 的 D5 像，不能又獨立硬設 canonical 013／0123。**
以下 §6–9 固定這份 geometry frame；所有比較仍保整份 transported Q(G)。

| BASE 結果 | 正確種類／在本題的用途 |
| --- | --- |
| single-spoke 必要表的 T4 排除與後續原 minor 排除 | 來源排除；各附充分前提與 arbitrary-size 覆蓋，不把 retained IDs 當來源。 |
| single-spoke 終局 102 retained 的 p1/p2 | 指定 X 延拓；尚無 r 色保証。 |
| two-spoke sector 禁位／相鄰 01,12,23 minors | 來源排除，不需恢復 e。 |
| adjacent 34,40 split-support | Σ(X) 單缺 β；不排這些 X 存在，且恢復 e另核。 |
| nonadjacent 14,24 的 Case I–IV | 指定 X 的兩鄰列延拓；不把其反設「X 拒」改成「G 拒」。 |
| §4、§7 的新 Gallai／三色 virtual-frame 論證 | 本完整契約內的來源排除／角色必要式候選；不是 HIGH 結論。 |

## 6. t_s=1、(2,2)：全部 pair 角色路由

[single-spoke 原完整分類](../../docs/c5_single_spoke_two_two.md)保 actual supports、
完整 relation schemas、全部 slit lifts/contact words；反射只是同一整圖搬運。
[終局 residual locality §4](../../docs/c5_single_spoke_residual_locality.md#4-完整表與條件式出口的接合)
沿任意大小覆蓋給：符合 own-minimal q、實際 `(2,2)`、T4 的來源，都接受
`p1=01021`、`p2=01212`，即 β 的兩鄰 singleton 列。
278 原 T4-retained 表項的來源排除与 102 retained 指定延拓分开；數字是 BASE 證據，
不是本輪 source trigger。

本題 pair 的全部查詢是 β=q_j（五位置）×原 s-spoke 0／2×F_C 的三個可用色，
共30。逐 query 保 `(boundary move,color move,reflection)`、原具名 ordered C/U identities；
與 BASE 原 observations／終局 tracked table 对回，完整結果在
`certificate.json:pair_t1_BASE_mapping`。沒有透過 final JSON 的磁碟替代。

| β位置 | s-spoke | 仍在終局表的原 F_C/F_U | BASE record |
| --- | --- | --- | --- |
| 3，01021 | b0 | `{1}/{2,3}` | 511 |
| 3，01021 | b2 | `{1}/{2,3}` | 90（共同搬後） |
| 4，01012 | b0 | `{1}/{2,3}` | 90 |
| 4，01012 | b2 | `{1}/{2,3}` | 511（共同搬後） |

其餘26 query：14沒有通過原必要表的完整支援／色穩定子條件；4在原表 T4-excluded；
8在原 T4-retained 而被後續來源排除。這個劃分由具名表查詢核，
來源排除所依的任意大小論證在 minor/external/frame-arc/cross-row/two-arc/
first-bridge/residual-locality 的 frozen BASE 報告。**不是僅從缺 ID 得出一般不存在**。
這些必要表通過也未驗原 C 在 r 的兩共享 cycles 可實現。

兩指定 X 延拓列為 q_(j−1)、q_(j+1)。原 G 必拒與否須檢查同框 Q(G)：
若 target∈Q(G)，才是恢复反證候選；target∉Q(G) 原本接受，不能拿來反證。
例如 geometry frame Q(G)=013、β=q3 时指定 q2/q4 都原本接受。

X 自己 ε=1、Σ-critical、T4，long-contract §7/E2 给 Q(X) 單點／相鄰 pair，
且含 β；兩鄰都接受排掉兩相鄰 pair。因此 **Q(X)={β}**。
這是 BASE／E2 組合的紙面候選，並非從 p1/p2 一句單獨斷言完整 Σ。
所以其餘所有原拒列 Δ=Q(G)−{β} 都 X 接受；全部恢復仍留 §8–9。

## 7. t_s=2、(2,1)：全部 sectors、兩禁色角色與實際五邊面

先只由 §3 的 private covering 得兩角色 `(F_C,F_U)=({c},{Dβ})` 或反序。
共同搬 β→q=01012 后，[two-spoke sector 必要表](../../docs/c5_degree5_two_spoke_sectors.md)
的全部位置路由如下，含禁色與區域的所有次序：

| q 框的 s-spoke pair | BASE 路由 |
| --- | --- |
| 02、13 | β 同色，own minimality 排除。 |
| 01 | adjacent (2,1) 原 K5，兩 forbidden 次序。 |
| 12 | middle (2,1) 原 K5，兩次序／兩 crosscut side。 |
| 23 | 同一整圖 reflection 搬 01 排除。 |
| 34、40 | 两 orders 的 split-support 精確 all-row laws給 Σ(X)=Ω−{β}；來源可能存在。 |
| 03 | 不在 `(2,1)` 必要表；stabilizer/T4 source contradiction。 |
| 14、24 | 兩區域次序×兩禁色次序，nonadjacent Case I–IV給兩指定 X 延拓。 |

主要入口與後續全部凍結：adjacent、middle、reflection、split-support、nonadjacent；
singleton S 已由 §4 全排。pair 原 s-spokes 為02，core β 同色先排 q3/q4；
β=q1 whole transport 得03，由 sector來源必要式排除；只剩 β=q0／q2。
q2 是否原拒仍由同框 transported Q(G) 決定，不只拿原 canonical 933 的 q2 当可用。

**兩禁色角色的推導。** pair 的 C 在實際五邊面
`Γ=(s,b0,b4,b3,b2)`，短面包含完整 U，原 s-spokes 正是 Γ 的兩框邊。
令 F_C(β)={d}，保 Γ 与 C 全部原 edges／contacts／attachments 得 Y。
Γ induced C5：原 B 無 chord，s 恰兩原 spokes；Y 的全部 C 點仍完整 degree4。
Pin s=d，literal `δ=(d,β0,β4,β3,β2)` proper，Y 拒 δ。
degree-list tight 与每 retained 非框邊的 slack 直接給 Y 自己 δ-minimal。

| β | 若 d=另一已用色 β1=1，Γ 的 literal δ |
| --- | --- |
| q0=01212 | 10212，proper 三色 singleton |
| q2=01201 | 10102，proper 三色 singleton |

[BASE multi-odd-cycles](../../docs/c5_multi_odd_cycles.md)的精確前提是三色 singleton、
own minimal、全 degree4、connected、odd-cycle/bridge blocks；**不需 T4**。
它迫 cycle blocks 為頂點互斥 triangles；與 §4 的 r 上兩共享 odd cycles 矛盾。
故排 d=β1，推得

\[
\boxed{F_C(\beta)=\{D_\beta\}=\{3\},\quad F_U(\beta)=\{\beta(b1)\}=\{1\}.}
\]

這是推得的角色，與 HIGH 兩 short 的 U 禁未用色角色不同。
d=Dβ 時 δ 是四色；上述三色定理不適用。Y 不繼承原 B 的全部 T4／所有 s pins，
不能另用全 degree4 單缺失定理排此四色身份。

β=q0 共同 transport 為 spokes14、C pentagon／U quadrilateral，角色 C₂禁3／C₁禁0，
即 nonadjacent Case II；β=q2 為24，再整圖 reflection 得同 Case II。
BASE 此 Case II 的 pB completion 只反設 X 拒 pB，沒有本題恢复 e 的 r-fibre 結論。
兩指定鄰列都 X 接受，再用 E2 如 §6 得 **Q(X)={β}**。

## 8. 十列、16 pins、空 fibres與恢復原 e 的精確判準

令 c_γ=γ(b_i)。在全部 proper γ、所有 ordered (a,b) 與**全部 lifts**上，

\[
\mathcal L_G(\gamma;a,b)=
\begin{cases}\mathcal L_X(\gamma;a,b),&a\ne c_\gamma,\\
\varnothing,&a=c_\gamma.\end{cases}
\]

故 BASE 指定延拓 γ 只給 `J_X(γ)≠∅`。若 γ∈Q(G)，恢复反證需要同一原圖

\[
\exists b\in E_s(\gamma)-F_U(\gamma),\ exists\tau\in(Col-\{b\})^2,
\ \exists a\ne c_\gamma:\quad\Phi_C(\gamma;\tau,a)\ne\varnothing.
\tag{RESTORE}
\]

完整 U preimage 必同步取相同 b；该式实际组合的是 §2 的全部 assignments。
任何真來源上，原 G 拒绝反而迫全部非空 X lifts 的 r=c_γ。
所以 Δ 上的 a≠c fibres 全空是**真來源必要式**；要排剩餘來源，必用同源
跨列／几何證某一如此必要空 fibre 其實非空。没有「拿另一份方便 witness」步。

**T2-q0→q1-RESTORE：有一份限定的完整恢复证明。** 只取 t_s=2、β=q0=01212、
γ=q1=01202；§7已推 FUβ={1}。同一原 U012 上 β/γ 逐附件相同，都为012，
故 U 的全部 assignments／tuples／preimages／pinned fibres相同，FUγ={1}。
s-spokes b0,b2 仍禁0,2，故**全部** Xγ lifts 必取 s=3。

L 的 actual support234上 β列212、γ列202，由 π=(0 1)双射全部 L assignments，
π固定 r=2、s=3。全部 ordered/shared contact constraints 同时搬，所以
`Λ_L(γ;2,3)=πΛ_L(β;2,3)`，含空 fibres与全部preimages。
S 的 actual support40在两列同为20，其全部 pinned fibres相同。
r没有retainedspoke；U避s=3的完整preimages非空。于是两列的完整 X(2,3) fibre
由 L 的 π、S/U的恒等及同一isolated factor建立双射。
Xβ全部pins为空，故 Xγ(2,3)也空；其他 s pins 已被相同spokes/U限制排除。
BASE给 Xγ非空，所以**每一** Xγ完整lift都满足 r≠2=γ(b4)，全部可恢復 e=rb4。
如果 q1∈同框 Q(G)，这就是原 G 的拒绝列，得到源矛盾。

这一双射只是同一实际 piece 的查询搬运；pins保持2/3，所有数据回到共同γ框接合，
没有为不同pieces独立选择来源或正規化。它覆蓋全部lift，不仅一份witness。
因此限定排除候选是 `t_s=2,β=q0,q1∈Q(G)`；不声称 β=q2 或其它原拒列的恢复。

十列依序與原 e=rb4 的字面色：

| index | literal γ | 類型 | γ(b4) |
| --- | --- | --- | ---: |
| 0 | 01012 | q4 | 2 |
| 1 | 01021 | q3 | 1 |
| 2 | 01023 | T4 | 3 |
| 3 | 01201 | q2 | 1 |
| 4 | 01202 | q1 | 2 |
| 5 | 01203 | T4 | 3 |
| 6 | 01212 | q0 | 2 |
| 7 | 01213 | T4 | 3 |
| 8 | 01231 | T4 | 1 |
| 9 | 01232 | T4 | 2 |

对每个必要 profile，`obligations.json`列全部十列與每列16 pins。
β 列全部 X fibres 空；Δ 列 X 非空且 r 只能是 γ4；其餘列 G 接受保证至少一份
r≠γ4 的 X lift。未建立 source 的具体 relations／preimages 不捏数值，均标待供给。
全部 diagonal 与空 fibres 保留。T4 的 G 接受来自 K2；没有在四色列指定未用色。

## 9. 全拒絕集合覆蓋及具名停止點

固定上述 geometry frame 的 941 全 D5 orbit 是
`013,134,024,124,023`；933 全 orbit 是各 `B−{k}`。
`certificate.json:schedules` 保存两profile合计28个 `(t_s,Q(G),β)`；
每份 Q 同时约束原 Σ、β、全部 Δ 与原 e literal。完整 Δ 如下：

这是恢复检查前的完整必要表。下列 `†` 组合已由 T2-q0→q1-RESTORE 给限定来源排除；
其余共24个Q/β schedules保留为必要域，不当来源证书。

| 941 Q(G) | t_s=1 可用 β → Δ | t_s=2 可用 β → Δ |
| --- | --- | --- |
| 013 | 3 → 01 | 0 → 13 † |
| 134 | 3 → 14；4 → 13 | 无0/2，排除此组合 |
| 024 | 4 → 02 | 0 → 24；2 → 04 |
| 124 | 4 → 12 | 2 → 14 |
| 023 | 3 → 02 | 0 → 23；2 → 03 |

| 933 Q(G) | t_s=1 可用 β → Δ | t_s=2 可用 β → Δ |
| --- | --- | --- |
| 1234 | 3 → 124；4 → 123 | 2 → 134 |
| 0234 | 3 → 024；4 → 023 | 0 → 234；2 → 034 |
| 0134 | 3 → 014；4 → 013 | 0 → 134 † |
| 0124 | 4 → 012 | 0 → 124 †；2 → 014 |
| 0123 | 3 → 012 | 0 → 123 †；2 → 013 |

933 的 q2 在每個對應拒絕集合／Δ 中保留；沒有預設 β 為 U 盾中點。
每一 Δ 列都是**原 G 必拒、X 已由 BASE+E2 接受**；†组合的q1已建立RESTORE，
其余组合尚无原拒列的RESTORE证明。
不同列的 relations／geometries 不能从独立来源拼出来。

具名最小缺口（必要 profiles，**未證來源存在**）：

| 身份 | 原 literal 與缺口 |
| --- | --- |
| T1-P22：U012/L234/S40，r兩oddcycle blocks，原 s-spoke b0或b2，e=rb4，β=q3=01021，Q(G)=013 | FCβ={1},FUβ={2,3}；J_X(q3)空。Δ={q0=01212,q1=01202} 的全部 X lifts 若来自真來源必须r=2。需在同源全部 fibres 證其中至少一列有r∈{0,1,3}的完整lift。BASE兩鄰q2/q4都原本接受，不能直接用作反證。 |
| T2-P22：同geometry／r blocks，s-spokes b0,b2，e=rb4，β=q0=01212，Q(G)=024 | FCβ={3},FUβ={1}；J_X(q0)空。Δ={q2=01201,q4=01012}：前者需r≠1、後者需r≠2。q4是BASE指定原拒鄰列；q2由E2得到X接受。q1已可恢復但原G本来接受它，故不产生源矛盾；这两原拒列仍欠RESTORE。 |

本輪可交限定排除候選：singleton全部、pair splits13/31、t1其餘β角色表項、
t2重色／禁位／另一已用色FC角色、t2 βq0且q1原拒的profiles。剩pair22的上述原邊義務保持 OPEN；
沒有宣称 scalar roles 或工具PASS已證來源可實現／全排，也不推一般 N2/E。

## 10. 有限控制、實際命令、依賴與驗收

[checker.py](checker.py)只读58份 frozen inputs，不import既有研究checkers。
從 prior contract 的19份**既有**控制原图，固定 U owner=s、另一root=r，
只作其原 r-spoke 省略（21份）；未生成新图或提高k。每列从原边重建 C/U 全部
unpinned assignments、全部 ambient tuples／preimages、C全r fibres，再與兩原mixed
unpinned join、16 pins 的直接 X 全lifts及 G恢复filter逐項相等。
原 contacts、attachments、shield metadata、rotation整份保存；此工具未驗它们满足本任務來源契約。

| 有限控制 | 實算／精確判定 |
| --- | --- |
| 原 C/U 完整介面 | 19圖、21省略、210十列row、3360 ordered root-pin fibres；13440 ambient C r fibres，10240空：**triggered and holds**。 |
| 全preimages／C piece join／直接X/G恢复 | 每份control逐assignment相等：**triggered and holds**。 |
| 自由孤立因子 | 代码保完整factor；控制没有非空孤立因子：**not triggered**（非空因子）。 |
| β角色 arithmetic、30原pair必要表query、28 full-Q schedules | 重算同域必要条件：**triggered and holds**；不是来源图trigger。 |
| endpoint marginals代完整R | 保存pair relation与其marginal产品禁色不同：**counterexample**。 |
| 丢r投影后将X接受视为恢复G | 保存非空X而恢复filter空的抽象relation：**counterexample**。 |
| K1–K12 finite source | **not triggered**；未建立或执行本任務finite source validator，trigger_count=null。控制X全接受十列，不能作为β-minimal来源。 |
| BASE終局JSON重播 | **not triggered**，指定BASE缺blob，finding保留；不能由disk替代。 |

实际命令、stdout/stderr、exit逐份在 `logs/`，见 [checks.json](checks.json)：

```sh
python3 -B audits/2026-10-11-n45-s-long-s-fibre/setup.py
python3 -B audits/2026-10-11-n45-s-long-s-fibre/checker.py --write
python3 -B audits/2026-10-11-n45-s-long-s-fibre/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-n45-s-long-s-fibre/checker.py --check
python3 -B audits/2026-10-11-n45-s-long-s-fibre/checker.py --check --certificate audits/2026-10-11-n45-s-long-s-fibre/negative-corrupt-certificate.json
```

普通／seed17 exit0、canonical bytes一致；corrupt完整C assignment被拒（exit1），
再次exclusive-create被拒（exit1），原canonical未覆寫；失败input／stdout/stderr皆保存。
未重播旧全量catalogue或所有BASE末端证书；未运行Lean/lake、没有新Lean theorem。
工具不承担任意大小纸面证明。外部degree-list／Gallai、BASE原盾、K4外hub、bridge-path、
全degree4三色结构与指定延拓链分别列在 [claims.json](claims.json)，保未解依赖／信任层。

三份本任務内部唯讀分工核 routes／cover／原blocks，根agent核回，不是同批其它任务新成果，
也不是本交付的独立验收。`reviews.json`列范围及已纠正的双重normalization／四色virtual-frame风险。
最终frozen/worktree/BASE drift、专属目录inventory与file hashes见 `final-checks.json`、
[delivery.json](delivery.json)。metadata仅排除delivery本身以免递归self-hash，明列排除理由。
共享docs、旧audits、证书、其它任务输出只读；不commit/push/PR、不发外部消息。
