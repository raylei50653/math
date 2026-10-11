# N45-S-LONG-S-BLOCK-TRANSFER：原 C block-tree 的完整 assignment／r-fibre transfer

2026-10-11。任務 D。**全文待獨立驗收。**
共同 Git BASE 為 `f2692089ad4259808e27d9b7e882ac09505b180a`。
本文件證任意大小原 block decomposition 的接合恆等式，以及精確的完整介面語義；
不負責任何 remaining schedule 的來源排除。有限 microcases 的實算由另外的
`cases.json`、certificate、checker 與無 transfer/checker imports 的 direct enumerator 承擔。

## 1. 權威、量詞與完整來源界線

本次只讀派工包驗證 `check_dispatch.py --check` 通過。輸入依
[input-pins.json](../2026-10-11-n45-s-long-s-rfibre-dispatch/input-pins.json) 分別是 BASE Git blobs
與 sealed audit SHA256；兩者不能互稱。已讀 frozen long-contract §1 的 K1–K12 全部條款、
sealed review 的 REPORT／acceptance／corrections／fibre-paper-review，以及原 B REPORT §§2–9
和 obligations。原 B 的 pending 欄位保持其歷史 bytes；採納範圍只按 review 更正附錄。
其中三十個 query 的分類沿用 `12+4+10+4`，`SF-RESIDUAL` 的必要依賴包含
`SF-T2-Q0-Q1-RESTORED`。本文件不重播上輪十九個 controls，不读取缺 BASE blob 的終局 JSON。

來源應用保留全部共同 K1–K12：具名 ordered induced-C5 disk 的全原 edges／rotation；
完整 transported Σ=933／941；ε=2；非相鄰原 degree5 r/s；其餘有效原內點完整 degree4；
原 H 連通且 full B-touch；原 pieces 恰 U/L/S，U owner=s；actual supports／attachments、
ordered/shared contacts、ownership 與 bridges 跨列固定；G 自己的各邊 Σ-critical witnesses；
以及 **X=G−e=M 自己**的同 β inclusion-minimality 與每條 retained 非框邊的完整刪邊 witnesses。
自由孤立原內點的完整染色因子保留。任務 D 的圖形校準不建立上述來源前提。

本次指定原身份為 actual U012／L234／S40、原 e=rb4、t_r=1、X 無 retained r-spoke、
原 r-split `(k_L^r,k_S^r)=(2,2)`。actual H_X−s 的完整分量是
`C={r}∪L∪S` 與完整 U。已採納 review 的兩個剩餘 profiles 是
`(t_s,m_s,n_U)=(1,2,2)` 與 `(2,2,1)`；故 C 的 actual ordered s-contacts
為 `P_C=(u_L,u_S)`，U 的為 `P_U=(v_1,…,v_n)`，n=2／1。
一個原頂點可以同時是 r-contact 與 s-contact，仍只用該頂點的一個顏色。
S 不預設單頂點，L/S 的內部大小、原 bridge 深度、cycle 長度與旁支數不設上界。

**TF-BLOCK 的量詞。** 對每個有限具名 actual connected C，其每條原 edge 正好属于一個
actual bridge／odd-cycle block、block 之間按 actual cutvertices 接合，對每份 literal
attachment 資料及每個 γ，下面 recurrence 與 C 的所有完整 proper assignments 雙射。
它的前提只有 actual decomposition 與字面附件。degree4、disk rotation、K11/K12 不參與
這個接合恆等式的證明。把符合 K1–K12 的来源映射到此類 C 時，原 r 上兩個 odd-cycle
blocks 的結構屬已採納 `SF-SPLIT-EXCLUSION`；不得從一個 finite fragment 反推出來源結構。

## 2. 字面 constraints 與 actual block incidence tree

令 Col={0,1,2,3}。对每個原 v∈V(C) 記其全部 actual boundary attachments
`N_B(v)`，並令

\[
D_\gamma(v)=Col\setminus\{\gamma(b_h):vb_h\in E(X)\}.
\]

先不 pin s。定义完整集合

\[
\Lambda_C(\gamma)=\{f:V(C)\to Col:
 f(v)\in D_\gamma(v)\ \forall v,
 f(v)\ne f(w)\ \forall vw\in E(C)\}.
\tag{C-ASSIGN}
\]

所有原 C 頂點，包括沒有 contact 的遠端旁支點，都是 f 的座標。原 rb4 不在 X，
因此不寫入 `D_γ(r)`。本身份中 r 無 retained B attachment 且 rs 不存在，
所以 `D_γ(r)=Col`、`deg_C(r)=4`。原 s-contact 先記其原頂點，避 s 的 pin 延後施加。

构造二部 incidence tree T：一類節點是 **每個原 C vertex**，另一類是每個 actual block，
v 與 K 相鄰當且僅當 v∈V(K)。非 cutvertex 也保留作 vertex leaf。標準 block decomposition
中，blocks edge-disjoint，不同 blocks 的交集至多一個 actual cutvertex，且這個 incidence
圖是樹。也可直接把「實際 decomposition 的 incidence 圖是樹」列為 TF-BLOCK 的輸入條件；
不以猜測的 block list 替代原 C。

把 T 根設為原 r。每個 block K 有唯一 parent vertex p(K)；其餘 `V(K)−{p(K)}` 是 child
vertex nodes。每個 v 的 child blocks 記为 Ch(v)。對頂點 v，W_v 是其 rooted subtree 中
全部原 vertex nodes；對 block K，W_K 是其 rooted subtree 的全部原 vertex nodes **加上** p(K)。
不同 child block 的 W_K 只交於其共同 parent vertex。不同 child vertex 的 W_u 互斥。
這些 actual sets 給出接合時的域，沒有壓縮、contract 或 replacement。

原 r 的兩個 child blocks `K_L,K_S` 都是 odd cycles；它們在 r 各貢獻兩條原邊，
其下全部原頂點分别为 L 與 S。以下 recurrence 也在每個非根 cutvertex 展開全部 child
bridges／odd cycles，所以保留 non-root articulation 及任意深度旁支。

## 3. 原 bridge／任意長 odd cycle 的局部規則

对每个 actual block K，令 E_K 是它的原 edges，定义

\[
\mathcal P_K=\{x:V(K)\to Col:
 x(v)\ne x(w)\ \forall vw\in E_K\}.
\tag{LOCAL}
\]

這裡是全部 **完整局部 assignments**，並非可用色集合或存在性摘要。

* 若 K 是原 bridge pq，局部規則為 `x(p)≠x(q)`，兩個原 endpoint 座標均保留。
* 若 K 是原 odd cycle `(z_0,…,z_{2h})`，h≥1，局部規則為
  `x(z_i)≠x(z_{i+1})`（0≤i<2h）且 `x(z_{2h})≠x(z_0)`。
  cycle 的全部 `2h+1` 原座標與 closing edge 均保留；不把長 cycle 換成 triangle。

固定 parent colour d 可按原 cycle 順序逐點展開所有顏色，並核 closing edge，取得
`{x∈P_K:x(p(K))=d}`。bridge 亦直接展開另一 endpoint 的全部三個異色。
這只是局部集合的實作方法；其正確性是逐原 edge inequality 的定義。
attachment constraints 在 vertex recurrence 施加，不憑 list 大小猜局部 assignment。

## 4. 完整 recurrence 與 restriction／union 雙射

對任意 d∈Col 定義 A_v^γ(d) 為 W_v 上全部 assignments 的集合，B_K^γ(d) 為 W_K 上
全部 assignments 的集合。遞迴規則如下。
對 B_K 而言 parent p(K) 的 attachment unary constraint 留給其上方 vertex recurrence；
W_K 的其餘原頂點之附件均須滿足。這個分工不省略 parent 的實際附件。

若 d∉D_γ(v)，`A_v^γ(d)=∅`。若 d∈D_γ(v)，則

\[
\mathcal A_v^\gamma(d)=
\left\{\{v\mapsto d\}\cup\bigcup_{K\in Ch(v)} g_K:
    g_K\in\mathcal B_K^\gamma(d)\ \forall K\in Ch(v)\right\}.
\tag{V-REC}
\]

對 block K，令 p=p(K)。則

\[
\mathcal B_K^\gamma(d)=
\left\{x\cup\bigcup_{u\in V(K)-\{p\}}f_u:
    x\in\mathcal P_K,
    x(p)=d,
    f_u\in\mathcal A_u^\gamma(x(u))\ \forall u\in V(K)-\{p\}\right\}.
\tag{K-REC}
\]

各 union 都在重複的 actual vertex 上同色。leaf v 的 V-REC 在 d∈D_γ(v) 時是
單元素完整 assignment `{v↦d}`，否則空。空 family 的 product 是一份空選擇；任一 child
集合為空就沒有此分支。所有 colour choices 與全部 child assignments 均展开，不捨棄重複
contact tuple 的不同 preimages。boundary constraints 對每個 actual vertex node 核一次。

**雙射證明。** 对 rooted incidence tree 從 leaves 歸納。V-REC 的子域只交 v，且各
`g_K(v)=d`，故 union 是 well-defined。沒有連接兩個不同 child block 私有頂點的原 edge；
否則那條 edge 的 actual block 會使 incidence 圖出現跨 subtree 連接而不是此树。
各 g_K 已滿足其 subtree 原 edges；頂點 v 的所有字面附件在 V-REC 核過，所以 union
proper。反向將一份 W_v 上的完整 proper assignment 限制到每個 W_K，就取得唯一全部
g_K 与 v=d。這兩個 restriction／union 映射互逆。

K-REC 中，x 核過 K 的全部原 edges；每個 f_u 核過 child subtree 的所有 edges／附件，
且 `f_u(u)=x(u)`。不同 W_u 互斥，與 V(K) 僅交各自 u，故 union proper。反向由完整
assignment 唯一限制出 `x=f|V(K)` 和每個 `f_u=f|W_u`；兩方向亦互逆。歸納完成。

於根得到

\[
\boxed{\Lambda_C(\gamma)=\coprod_{a\in Col}\mathcal A_r^\gamma(a).}
\tag{TF-BLOCK}
\]

每份 f 的 r 色唯一，故此 coproduct 真正 disjoint。全 assignments 一對一對回原頂點與
原邊；旁支頂點亦在雙射的域内。這個證明沒有使用 bounded size、cycle 長度上界、
complete degree4、Σ-criticality 或同 β 刪邊 witnesses。

亦可把 (TF-BLOCK) 写成全部 local block assignments 的 natural join：每個 actual cutvertex
取同一顏色，再交每個原 vertex 的字面附件 unary relation。完整 preimage 記錄是這個 join
的全域 assignments；只保存局部非空性／端點可用色集合不足以代表此 join。

## 5. ordered tuples／全部 preimages／r 色與空 ambient fibres

任取固定 actual ordered contact list P=(p_1,…,p_m)，每個 p_i 是具名原頂點。
若相同原 vertex 同時出現在不同角色，不能建立兩個獨立顏色；所有角色都讀 f(v)。
本 assigned domain 的 s-interface 是 P_C=(u_L,u_S)。定义

\[
\Phi_C(\gamma;\tau,a)=
\{f\in\Lambda_C(\gamma):
    (f(u_L),f(u_S))=\tau,\ f(r)=a\},
\quad (\tau,a)\in Col^2\times Col.
\tag{AMBIENT}
\]

保存 **全部 64 個有序 ambient cells**；空集合亦是該 named cell 的完整資料。
每個 preimage 是 f 在全部原 V(C) 上的 assignment。contact tuple／r 色是 f 的確定函数，
而 TF-BLOCK 的雙射保同一個 f，故雙射限制到每个 `Φ_C(γ;τ,a)` 仍互逆。
因此全部 preimages、r 色與空 fibres 同時保留；沒有另行決定它們的數目。
任意較長的 contact lists 亦由同一論證保全部 `Col^m×Col` ambient cells。

特别可取 P 為原 ordered r-contact lists（L/S 各兩點）、原 ordered s-contact list、
任何其他 interface contact lists 的固定串接。若同一原 vertex 在此串接出現兩次，
對應 tuple 座標必相等；不符合此相等式的 ambient cells 都是空。由完整 named f
直接读取每一座標，得到每個 ordered contact tuple 的全部 inverse images；从任何
現有完整 vector list 重新按 P 分组也是精确的同一集合。只保 s-tuple/r 的有限
certificate 不会丢掉 r-contact tuple 資料，因为其中每份 preimage 仍是包含全部
原 r/s-contact vertices 的完整 f；没有只保留 tuple marginal 或一份 representative。

有限 certificate 的 vectors 只是以 cases.json 的固定 original vertex order 表達 f。
必須保存完整 vertex list，以及每份 vector 的相同長度；未接到 interface 的原旁支
頂點仍不可省略。對任一 named τ/a cell 的刪除，即使其 preimage list 為空，亦不是同一介面。

對 **全部16 ordered pins** `(a,b)∈Col²` 定义

\[
\boxed{\Lambda_C(\gamma;a,b)=
\{f\in\Lambda_C(\gamma):f(r)=a,
   f(v)\ne b\ \forall v\in P_C\}
 =\coprod_{\tau\in(Col-\{b\})^2}\Phi_C(\gamma;\tau,a).}
\tag{C-PIN}
\]

ambient cells 只按字面避 s pin b 過濾。若 s-contact 亦是原 r-contact，其原 C edge
已核 `f(v)≠a`，此處再核 `f(v)≠b`；兩者作用於同一原 f(v)。diagonal a=b 與空 pins 全保留。
本式没有包含 actual U 或 s-spokes，故 C-PIN 的非空性不能單獨稱為 X 延拓。

全部十個共同 literal 依下表逐列使用同一原 C／附件；每列皆有全部64 ambient cells
與全部16 ordered pins。原 edge 恢復色為本列 **literal 的最後一位**。

| index | literal γ | 名稱 | γ(b4) |
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

T4 同樣按 literal 核，不能借一個不存在的未用色。

## 6. 何時能接 actual U、s-spokes 與自由孤立點

假設另已供給 **同一來源** actual X 的全部原 vertices／edges：frame B、s、兩完整
H_X−s 分量 C/U，以及自由孤立點 I；C/U 間沒有原 edge，rs 不存在，X 無 retained
r-spoke。所有非框邊正是 C／U internal edges、actual B attachments、原 s-contact edges
與 retained s-spokes。若 missing U 或 missing G，以下是紙面恆等式，沒有 executed source。

由 actual U 原 edges／附件定义其完整 `Λ_U(γ)` 与 ambient

\[
\Phi_U(\gamma;\upsilon)=
\{u\in\Lambda_U(\gamma):u(P_U)=\upsilon\},
\quad \upsilon\in Col^n,
\]

全部 ambient cells 與完整 U preimages 均保留，包括空 cells。令

\[
\Lambda_U(\gamma;b)=
\coprod_{\upsilon\in(Col-\{b\})^n}\Phi_U(\gamma;\upsilon),
\qquad
S_\gamma(b)=1[b\ne\gamma(b_h)\ \forall sb_h\in E(X)].
\]

以 `[S_γ(b)]` 表示條件為真時含一個空 assignment 的集合，為假時空集合。
任意 proper γ、全部 ordered a,b 上有完整 restriction／union 雙射

\[
\boxed{\mathcal L_X(\gamma;a,b)\ \cong
 [S_\gamma(b)]\times\Lambda_C(\gamma;a,b)
 \times\Lambda_U(\gamma;b)\times Col^I.}
\tag{TF-X}
\]

逐 tuple 的版本保完整 ambient preimages：

\[
\mathcal L_X(\gamma;a,b)\cong [S_\gamma(b)]\times
\coprod_{\substack{\tau\in(Col-\{b\})^2\\
                    \upsilon\in(Col-\{b\})^n}}
 \Phi_C(\gamma;\tau,a)\times\Phi_U(\gamma;\upsilon)\times Col^I.
\tag{TF-X-FIBRE}
\]

union 加上固定 frame γ 與 s=b；r 已是 C 中的原座標。各 component 內邊與附件由
其完整 assignment 滿足，所有 s-contact inequalities 由同一 b 滿足，actual s-spokes
由同列 S_γ 滿足，isolated 點无 edges。反向完整 X lift 的 restriction 唯一给出這些因子；
因此全 lifts 雙射而非只有存在性。自由孤立集合 I=∅ 時 `Col^I` 是 singleton，非空时
每份孤立點 assignment 都是独立 factor。K11/K12 不用於 TF-X 的正確性；若要主張输入
就是 assigned target source，仍须另外證其全 K1–K12，不能由這個 factorization 推得。

microcases 只供 actual C fragment，沒有 actual U、完整 G、Σ-critical witnesses 或 X 同 β
minimal witnesses；故其中 C-PIN／spoke-filtered C-PIN 即使非空，whole-X/G/source coverage
仍是 `executed=false, trigger_count=null, status="not triggered"`。
不得以抽象 U relation 接成所謂 target-source lifts。

## 7. 只恢復原 e=rb4 的完整 filter

在同一原 vertices 上，G 比 X 恰多一條原 edge rb4。因此對全部 γ、全部16 ordered pins
與全部完整 lifts，

\[
\boxed{\mathcal L_G(\gamma;a,b)=
\begin{cases}
\mathcal L_X(\gamma;a,b),&a\ne\gamma(b4),\\
\varnothing,&a=\gamma(b4).
\end{cases}}
\tag{TF-RESTORE}
\]

這是身份 map／empty filter 的精確等式。C microcertificate 的 `restored_preimages`
只是對 C-PIN 的 a 施此 filter；沒有供 actual U/G 时不能稱它已計算完整 G lifts。

任一 schedule 的精確待解式是：存在同來源 γ∈Δ=Q(G)−{β}，及 ordered a,b，满足

\[
a\ne\gamma(b4),\quad S_\gamma(b)=1,\quad
\Lambda_C(\gamma;a,b)\ne\varnothing,\quad
\Lambda_U(\gamma;b)\ne\varnothing.
\tag{OPEN-RESTORE}
\]

此時 TF-X/TF-RESTORE 才给一份原 G 的完整 lift，含全部原旁支与 isolated 色因子。
等價地，令 `F_U(γ)={b:Λ_U(γ;b)=∅}`、`E_s(γ)={b:S_γ(b)=1}`，則需

\[
\exists \gamma\in\Delta,\ \exists b\in E_s(\gamma)-F_U(\gamma),
\exists a\ne\gamma(b4),\ \exists\tau\in(Col-\{b\})^2:
\Phi_C(\gamma;\tau,a)\ne\varnothing.
\]

F_U 在這裡只縮寫一個實際完整 assignment 避色查詢，不替代 U 全 relation／preimages。
在真來源上，G 拒 γ 而 X 接 γ 必迫所有非空 full X lifts 的 r 色等於 γ(b4)。因此這些
真來源要求的空 fibres 是 precisely
`Φ_C(γ;τ,a)=∅` 對每個 `a≠γ(b4)`、每個允許 b 与 `τ∈(Col−{b})²`；所需否定仍是
同一來源上一份如此要求为空的完整 preimage，而不是另一來源的方便 witness。
若 b 的 actual U fibre 為空或其 s-spoke factor 為零，C 的此 ambient fibre 可以非空，
仍不能推出 source contradiction。

## 8. 跨列色搬運的精確條件

固定同一 actual piece T、所有原 edges／vertex names、ordered/shared contacts 与字面附件。
若色雙射 π:Col→Col 對每條原 attachment vb_h 均满足
`π(γ(b_h))=γ′(b_h)`，則 `f↦π∘f` 是完整 assignment 雙射
`Λ_T(γ)→Λ_T(γ′)`，inverse 为 `π⁻¹`。internal inequalities 保持，attachment inequalities
由上述逐原附件条件保持；tuple 的每個座標與每份 preimage 同搬，空 fibres 同搬。

若该 piece 接 r/s，pinned query 的精確目标是 `(π(a),π(b))`，不是仍写 `(a,b)`。
若 pins 要保持 a,b，必须 π 固定它們。若搬的是含原 r 的整个 C，r 色亦從 a 搬成 π(a)。
對任何完整 ordered τ，有

\[
\Phi_T(\gamma;\tau,a)\cong
\Phi_T(\gamma';\pi\tau,\pi(a))
\]

（T 含 r 时适用 r coordinate；U 无该座標）。若 attachments 不逐項滿足、pins 不匹配、
shared original vertex 的颜色不一致，這個 mapping 不是已證的 transfer。

整圖 D5／color normalization 只允许一次共同搬动原 frame、所有 vertices、attachments、
rotation、e、β、Σ 与 witness 数据。已固定字面框後，piece 色搬運是 **同一原 piece 的
查詢雙射**；每個 transported query 先寫回共同 γ′ 的字面颜色与 target pins，再按 TF-X
接合。对某特定 query 可采用不同 piece 的已證色雙射，但必须使共同 root pins／shared
原座標完全一致，并逐件符合 actual attachments 的颜色。不得把不同原圖的 relations
混合，也不能把各 piece 独立正規化后未返回共同 literal 色框就作來源結論。

TF-BLOCK/TF-X 本身不产生跨列非空性：即使 C 在 γ 的某个 r-fibre 非空，它在 γ′ 的
restorable r-fibre 仍须上述完整雙射或额外几何引理。此任務沒有新增較強 cross-row fibre
lemma，因而沒有抽象 relation 反例或新增 conditional source 排除。

## 9. remaining schedules、精確 OPEN fibres與停止點

下表只是 sealed adopted review 的二十四個 **必要 schedules**，不是来源图数；
t_s=1 每項仍分 actual s-spoke b0／b2 两变体，t_s=2 原 spokes 恰 b0,b2。
profile labels 保原 r、原 e=rb4、C/U 身份。`β→Δ` 的每个数字表示 q 的位置，不是 literal
index；十列仍按 §5 的固定顺序。表列全 Δ；没有 finite actual source relation 数值。

| Σ orbit／transported Q(G) | t_s=1，β→完整 Δ | t_s=2，β→完整 Δ |
| --- | --- | --- |
| 941／013 | 3→01 | 已由上轮 q0→q1 恢復排除此项 |
| 941／134 | 3→14；4→13 | 无允许 β |
| 941／024 | 4→02 | 0→24；2→04 |
| 941／124 | 4→12 | 2→14 |
| 941／023 | 3→02 | 0→23；2→03 |
| 933／1234 | 3→124；4→123 | 2→134 |
| 933／0234 | 3→024；4→023 | 0→234；2→034 |
| 933／0134 | 3→014；4→013 | 已由上轮 q0→q1 恢復排除此项 |
| 933／0124 | 4→012 | 2→014；β0 已由上轮恢復排除 |
| 933／0123 | 3→012 | 2→013；β0 已由上轮恢復排除 |

表中 t_s=1 为14 schedules／28原 spoke 变体，t_s=2 为10 schedules／10变体；
共24 schedules／38 schedules-spoke 变体。这不含 complete geometry 数目，不是38个来源。
上轮28−4=24的四个删除依赖 SF-T2-Q0-Q1-RESTORED，非本任務新增排除。

對每個表項、每个原 spoke 变体、每列 q∈Δ，complete ambient／pin obligation 為：

* `a=c_γ=γ(b4)` 的 X fibres 可能非空，這是已接受 X row 的必要至少一份 lift 所在处。
* 所有 `a≠c_γ` 且 S_γ(b)=1、actual `Λ_U(γ;b)≠∅` 的 pins，真來源要求
  `Λ_C(γ;a,b)=∅`；逐 τ 形式是 OPEN-RESTORE 下列的必要空 `Φ_C` fibres。
* b 被原 s-spoke 禁止或其 actual U fibre 空时，full X/G pin 必空；C interface 本身继续
  保存全部 preimages，不自動清空这个 C ambient cell。
* β 的全部 full X pins 空。Δ 以外已接受的原 G row（包括 T4）至少有一份恢复 lift，
  但其具体 C/U pins／preimages 未供 source 时不得填数字。

本文件的终点是任意大小 TF-BLOCK、全部 fibres 的保真性、TF-X 与 TF-RESTORE 恒等式。
尚未对任何 remaining schedule 证明 OPEN-RESTORE，也没有同源 minor extraction。
卡住的具名引理仍是 **same-source Δ restorable r-fibre nonemptiness**：从 K1–K12 加原
attachments／block geometry，證至少一個 Δ row 有同步 actual U preimage 的
`a≠γ(b4)` C preimage。此 recurrence 提供准确数据接口，但不提供这項非空性。

紙面 recurrence 可在 arbitrary actual decomposition 下成立；finite 校准只验证指定微案例
transfer；target source 未建立／未執行，source realizability 未證；没有新增 Lean theorem；
没有一般 N45/N2/E、ε≥3 或任意剩餘來源排除。所有本次结果仍 **待獨立驗收**。
