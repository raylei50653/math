# N45-S-HIGH2：雙 U-contact／single spoke 的完整契約排除候選

2026-10-10。BASE 與執行 HEAD 均為
`dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。
[正式任務全文](frozen/current/docs/history/2026-10-10-n45-high1-adoption.md)、
[八 pins 與完整凍結索引](inputs-final.json)逐檔核回。

**交付：全部 H1–H13 內，任意大小原來源 G 不存在的 paper 候選，待獨立採納。**
關鍵不是 X 的指定 p 延拓：原 U 的双禁色迫原 bridge 路徑，原 K₅ bags
迫路徑只有一條邊，但兩端的完整旁支仍任意大。由完整 rooted assignments
得到所有列的 U 二元關係；在 U 盾上看見三色的列，直接構造恢復 e 的原 G full lift。
因此 Q(G) 至多含另外兩個 singleton 位置，與完整 933／941 矛盾。

本輪未建立或執行具名 finite HIGH2 source，沒有 source trigger 數，沒有新 Lean。
Python 只校準固定 toy、位置／色算術和封存；不裁決任意大小 paper 證明。
HIGH3／long／原55／其他 cores／一般 N2／E 保持 OPEN；不自行寫入共享權威頁。

## 1. 完整契約、量詞與信任

以下每個結論均在全部 H1–H13 下量化任意有限大小原 G。
子引理即使只用其中一些前提，本輪不擴大交付範圍。

| 前提 | 固定原來源身份 |
| --- | --- |
| H1 | 有限簡單 disk G，有序 induced 外框 C5 B=(b0,…,b4) |
| H2 | 完整有序 Σ(G)=933／941 或一次共同整圖 D5 像；每條非框邊 Σ-critical；ε(G)=2 |
| H3 | 有效 H 忽略原孤立內點 I，連通、full B-touch；I 保留全部四色自由 assignments |
| H4 | 恰兩原非相鄰 degree5 roots r,s；其餘有效原內點完整 degree4 |
| H5 | H−{r,s} 原分量恰 U,P,Q；三份 connected、one-sided、actual support 非空 |
| H6 | P/Q 的 actual support 各恰一條真原框邊兩端；各有正 r/s incidence；actual attachments／ownership 全留 |
| H7 | U 只接 s，恰原邊 sx1、sx2，x1≠x2，無 U–r；U 整份保留 |
| H8 | mixed incidence=(3,2)，s 對 P/Q 各一，r 分配1與2；原具名 identity 不換 |
| H9 | 原 r 兩 spokes，只省略 e=rb_i，X 保 rb_j；原 s 唯一 spoke sb_k 全留 |
| H10 | 固定原拒絕三色 literal β，X=G−e=M 自己是 β inclusion-minimal45／54 core；不用 G criticality 遺傳 |
| H11 | 只刪 e；U/P/Q 所有原頂點、內邊、contacts、框附件及其他 spokes 全留，無新增／替換／縮 piece／部分 U 刪除 |
| H12 | named／ordered／shared contacts 單一原變量；actual supports／ownership、bridges／rotation、共同 literal 四色框、十列完整 relations、全部 pins、ambient 空／非空 fibres 與 full lifts 全留 |
| H13 | D5／S4／root swap 只共同搬整圖及所有資料；933 q2 全留，不假定 β 是 U 盾中點；G／X／刪 contact 圖分清原邊及 lifts |

逐 claim 的量詞、完整前提索引、依賴及 trust 見 [claims](claims.json)。
HIGH1 與其三份獨立稽核只供身份參照，不用作 HIGH2 的充分前提。

| 凍結依賴 | 用途與證據層 |
| --- | --- |
| [R10](frozen/base/docs/c5_degree5_interfaces.md) §§1–4、[weak lists](frozen/base/docs/c5_weak_list_cores.md) §1 | 完整 relation、degree-list slack、逐 incident-edge 解除及不可刪減覆蓋，paper |
| [single-spoke cores](frozen/base/docs/c5_single_spoke_cores.md)、[(2,2)](frozen/base/docs/c5_single_spoke_two_two.md) §§1–3 | 原接點區塊／slit 次序、角色、pair relation、原奇數 bridge 路徑，paper＋外部 degree-list |
| [E4](frozen/base/artifacts/c5_excess_two_e4/REPORT.md) §4.1 | 每 proper γ、每同色 root pin 的局部 N-diagonal 完整 lift；不假造外部合法染色 |
| [shield](frozen/base/docs/c5_unary_shield_budget.md) §§2–3 | 原 one-sided 盾連續／互斥、full B-touch 支援等於盾頂點、critical U-contact 迫盾長≥2 |
| [minor](frozen/base/docs/c5_single_spoke_two_two_minor.md) §2、[branch palettes](frozen/base/docs/c5_single_spoke_branch_palettes.md) §2 | 原雙拒絕 palettes、每完整 W 的 residual 穩定子、實際色供應，paper |
| [external](frozen/base/docs/c5_single_spoke_two_two_external.md) §§1–2、[frame arc](frozen/base/docs/c5_single_spoke_frame_arc.md) §§1–3 | 同源 actual attachments、原外路及任意兩 W 的五 bags／十原鄰接，paper |
| [cross row](frozen/base/docs/c5_single_spoke_cross_row.md)、[two arc](frozen/base/docs/c5_single_spoke_two_arc.md)、[first bridge](frozen/base/docs/c5_single_spoke_first_bridge.md)、[locality](frozen/base/docs/c5_single_spoke_residual_locality.md) | 區分來源 K₅ 排除與指定 X 的 p1/p2 延拓；不將 target 查詢當 G 延拓 |
| [short support](frozen/base/docs/c5_short_support_singleton.md)、[connected exterior K4](frozen/base/docs/c5_degree5_tree_components.md) | shield／N-diagonal 及 K4-free 的 BASE 信任依賴 |
| [官方 Gallai 講義](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)、[凍結 PDF](frozen/gallai.pdf) | Lemma7 tightness、Theorem10 block palettes；外部 trust，不是本輪 Python／Lean 定理 |

已讀取官方 PDF 的 degree assignment 與不可著色前提；使用 palettes 必先取得拒絕。
所有候選保留上述 BASE 紙面依賴，沒有以 checker 通過替代這些無界論證。

## 2. H2-CORE／COMP：X 自己的 degree 與完整原分量

唯一省略 e 令 r 完整 degree 從 3 mixed+2 spokes=5 降為4；仍有 rb_j。
s 為 2 mixed+2 U+1 spoke=5，其餘有效原內點為4。
H10 直接給 X 每條非框邊自己的 β-critical full witness；不是 G-criticality 的遺傳。
H_X=H_G，X 保外框及 disk，且 Σ(G)⊆Σ(X)，所以 X 繼承全部 T4。

H_X−s 的完整原頂點分割恰為 C={r}∪P∪Q 及 U。
C 內邊恰 E(P)∪E(Q)∪E(r,P)∪E(r,Q)，三條原 r contacts 全留；
全部 C–B 邊恰 E(P,B)∪E(Q,B)∪{rb_j}。
U 的內邊／框附件恰 E(U)／E(U,B)，兩分量之間沒有邊。
P/Q 原 connected 且各接 r，故 C connected；U 原 connected。
兩 s–C 接點為不同原 pieces 的 yP、yQ，兩 s–U 接點為 x1、x2。

保 s 四 contacts 的總 rotation，以及 C、U 各自在該 rotation 中的 ordered sublist。
所有 shared r/s contact 始終是同一原頂點、一個色變量。
U 的完整 x1–x2 路與 sx1、sx2 所形成的原 cycle 均保留；此處未把 U 降成單 contact。

## 3. H2-JOIN／RESTORE：每 literal、每 pin 的完整 fibres

Col={0,1,2,3}。對每 proper literal γ，S_C(γ)、S_U(γ) 分別是原完整分量
全部合法 assignments，含各自所有原框附件；S_C 尤含 f(r)≠γ(b_j)。
以原 ordered sublists 定義所有 ambient fibres，支援外仍記空集合：

```text
Fib_C(γ,t,c)={f∈S_C(γ): (f(yP),f(yQ))=t, f(r)=c}, t∈Col²,c∈Col;
Fib_U(γ,u)={f∈S_U(γ): (f(x1),f(x2))=u}, u∈Col².
R_C(γ)={t: 存在 c 且 Fib_C(γ,t,c)非空}; R_U(γ) 同理。
```

X 的全部 full lifts restriction／union 雙射於：同一 s 色 a≠γ(b_k)，
任意 t,u,c 與 f_C∈Fib_C(γ,t,c)、f_U∈Fib_U(γ,u)，t,u 四座標皆避 a，
再加任意 I→Col 的 assignments。固定任何 r/s pins 只取其對應 fibres，空 query 不丟。
restriction 取同一 full coloring；union 因 C/U 不交且無跨邊，只需四條 s-contact 不等式。
C 內 P/Q 也只在同一 r=c 下接合；P 或 Q 的兩個 r contacts 同時約束同一原 coloring。
不乘 marginals，不重新正規化各分量，也不分拆 shared contact 變量。

G 的 full lifts 恰為這份 X 資料再加 **c≠γ(b_i)** 的子集。
因此一個 X 指定延拓／可用 s 色，要提升為 G，必須在該 query 的完整 r 投影有
γ(b_i) 以外的色。下文直接提供 r=D 的原 G lifts；沒有猜測 r 投影。

## 4. H2-F：完整量詞迫實際 C/U 角色 (1,2)

每原 C/U 點在 X 完整 degree4。對每 γ、每 s 色 a，各接點扣 a 後 lists 至少
為分量內 degree；不扣 a 時接點嚴格多一色，所以 R_C、R_U 均非空，|F|≤2。
令 F_T(γ)={a: 原 T 沒有完整 assignment 同時避兩 s-contact 的 a}。
這是整二元 R 的 tuple 色集交集，不是兩 endpoint palettes 的交集。

R10 的解除引理在 X 上逐 incident edge 成立，包括分量內部橋、非橋、框附件與 s-contact。
刪原邊造成的完整解除 witness 保原頂點；橋刪後對兩側各用 strict slack。
H10 的 full X 刪邊 witnesses 因而給 A=Col\{β(b_k)}、F_C∪F_U=A，
每份 F 都有 private colour。刪 s 唯一 spoke 的 witness 排除 β(b_k) 被任一 F 禁止。

對任意 proper γ、任意 a≠γ(b_j)，置 r=s=a。
原 P/Q 的 N-diagonal 各提供全部 contacts 同時避 a 的完整 coloring，且 retained rb_j 合法。
因此 **F_C(γ)⊆{γ(b_j)}**，含所有 colour pins 的量詞，不只已存在外部 coloring 的情況。
令 a0=β(b_j)、c0=β(b_k)。private-cover 迫

```text
a0≠c0,
F_C(β)={a0},
F_U(β)=Col\{a0,c0}={D,h},
R_U(β)={(D,h),(h,D)}.
```

D 為 β 未用色，h 為 β 的第三個已用色。pair relation 的兩個方向由各原 sx1／sx2
刪邊解除 witness 取得：在刪該邊的 full U coloring 中，恰該座標必等於被查色。
故已證 C/U 實際角色為 (1,2)，排除本契約的 (2,1)、(2,2)；不借 HIGH1 容量≤1。

## 5. H2-K33／ARC：例外共端的原邊補齊

先證 U 盾長≥2，尚不假定 P/Q 支援頂點互斥。
取任一原 sxν 的 Σ-critical 新列 witness f∈Lift(G−sxν)，必有 f(s)=f(xν)。
限制到原 G−U，仍含恢復邊 e 與其他所有原邊；若完整 U 可同時避 f(s)，便接回 G，矛盾。
所以該列 U 的完整 forbidden query 非空。H−U={r,s}∪P∪Q 原 connected；
full B-touch 與原外路符合 BASE shield 定理 A，得 |σ_U|≥2、|S_U|≥3。

P/Q 的原盾各恰其真支援框邊，且盾邊互斥，所以它們是不同框邊。
若共端 v，六 bags 左 P、Q、O，右 {r}、{s}、{v}。
當 b_k≠v，O=B−{v} 是原框路徑。當 b_k=v，選 actual U 附件 u–b_h、h≠v，
改取 **O′=(B−{v})∪U**。U 原 connected，該原附件使 O′ connected；
六 bags 仍互斥，沒有把 U 放進 P/Q 或 roots。

| 九對 adjacency | 原邊 witness |
| --- | --- |
| P–r、P–s、Q–r、Q–s | 各自原 contacts；r 的三 contacts 沒有被改成一條 |
| P–v、Q–v | 各原 actual support 的附件 |
| O／O′–v | 原框邊 |
| O／O′–r | r 原兩個不同 spoke endpoints 至少一個≠v；容許使用原 e，只在 G 上取 minor |
| O–s，或 O′–s | b_k≠v 時原 sb_k；b_k=v 時原 sx1（sx2 也可） |

因此原 G 含 K₃,₃ minor，矛盾 disk planarity。例外 case 未假造 O–s 的第二條 spoke。
P/Q 支援框邊必頂點互斥。剩餘三條框邊分成長2及長1兩段；U 盾連續且≥2，
只可能取長2段。full B-touch 的支援引理給
**S_U=T={b_L,b_m,b_R} 三個連續原點，σ_U=b_Lb_mb_R**。
中點 b_m 不被 H−U 碰到，原 r/s spokes 也避 b_m。
P/Q 四支援端點恰 B−{b_m}，故 **S_C=B−{b_m}**；尤其 C 碰到 T 外的兩個點。

## 6. H2-MAP：BASE 的來源排除與指定 X 查詢分清

X 已有 unique degree5 z=s、sole spoke sb_k、兩完整二接點分量 C/U、其餘 degree4、
自己的 β-minimality／disk／T4；逐點符合 BASE single-spoke (2,2) §1。
同一全圖 D5/S4 把 β 化為 q=01012 後，保原 C/U 身份與兩 ordered sublists，
不能用必要表項反過來製造 source。

BASE slit 次序還要求兩 actual support lifts 有一個整區塊在另一個之前。
沒有這種 lifts 的位置直接是 BASE crosscut 原來源排除，沒有 necessary record。
有 record 的位置逐一對回凍結表，C 為 singleton、U 為 pair，並保所有原 placement／contact word。
[certificate](certificate.json)保這份具名位置 mapping；表號只標 identity，不證實現。

BASE minor／external／frame-arc 是具名原 bags 的來源排除；cross-row／two-arc／
first-bridge／locality 的指定 p1/p2 extension 則只是 X 的 colour query。
例如 actual (0234,012)、({1},{2,3})、s-spoke0 對回 record90；
另一保留角色共同搬運後對回 record511，四個無 slit placement 的位置另列原來源排除。
後續 locality 的 p2 是 X 結果；它未保本題 r-fibre，不能直接接回 e。
下文用 U 原路與 full assignments 另建原 G lifts，避開這個缺口。

## 7. H2-BRIDGE／SPLIT：原 U 路恰一邊，旁支完整保留

§4 的兩個拒絕 s pins D,h 在同一原 U 上給 degree-lists、tight block palettes。
X 的 connected exterior B∪{s} 經 sole spoke connected，故 BASE K4-free 前提成立。
BASE (2,2) pair 論證給唯一 x1–x2 的原 bridge 路徑
P_U=(z0=x1,…,zℓ=x2)，ℓ≥1 奇數；J=P_U∪{sx1,sx2} 為原 simple cycle。
刪 P_U 的橋邊只用來**定義** Wν：含 zν 的整份原連通旁支塊。
Wν 互不相交、各含一個路徑點，合起來仍是全部 U；不刪任何頂點／附件來替換 colouring。

令 Tν 是整個 Wν 的 actual support，含 zν 直接附件。
BASE minor §2 的雙 palette residual 為 {D,h}，逐色穩定子迫
**{a0,c0}⊆β(Tν)**，每個 Wν 都必見兩個實際供應色。
此處使用兩份已存在的拒絕證書，不把 residual 當作 arbitrary rooted colour palette。

凡兩個不同 W 同時接到兩個具名框點 b_a,b_b，可在 C 中取原路
s–yP–…–u–b_t，其中 t∈B−T。C connected 且實際碰這兩個外點，
故可選原 simple L，內部全在 C，避 U 與其他框點，b_t 與 b_a,b_b 互異。
沿 BASE frame-arc §3，以 b_a,b_b,b_t 起三份連通框弧 X_a,X_b,D_t。
取 i<j：A=⋃_(ν=i)^(j−1)Wν、A′=Wj、
Z=(V(J)\{zi,…,zj})∪V(L)∪D_t。
五 bags A,A′,Z,X_a,X_b 連通且互斥，十原鄰接為原 bridge、兩 cycle 邊、
四條 W actual attachments，以及三條框切口邊。原路 L 在 Z 中共用，不要求兩條獨立外路。
這是 X⊆G 的原 K₅ witness，不能用作 colour-preserving contraction。

若 β(T) 有三色，a0,c0 在 T 各有唯一供應點；全部 W 都碰同一兩點，
任兩 W 即给上述 K₅，矛盾。因此 β(T) 只有兩色，為 β(b_L)=β(b_R)≠β(b_m)。
每個 W 必碰 b_m 及至少一個外端 b_L/b_R。
任何兩 W 共享同一外端也給 K₅。若 W 至少三份，鴿籠原理必有此共享；
所以恰兩份 W、ℓ=1，原 x1x2 就是 bridge。
若一份 W 同時碰兩外端，與另一份也共享外端，仍矛盾。
故以實際支援命名（可對應 x1/x2 任一原 ordered 方向）：

```text
U=W_L ⊔ W_R，唯一跨塊原邊 x_Lx_R；全部旁支／blocks／attachments 留在各 W。
S(W_L)={b_L,b_m}, S(W_R)={b_m,b_R}。
```

這是任意大小的 actual-support 結論，不是兩內點正常形；W_L/W_R 的大小無上界。

## 8. H2-PALETTE／EXCLUSION：原全 assignments 與恢復 e 的 G lifts

對任意 γ、c，令 K_W(γ,c) 是 W 的全部原合法 assignments 且 root 色=c，
含 W 的全部原框附件。定義 A_W(γ)={c:K_W(γ,c)≠∅}，其他 ambient fibres 仍為空。
原唯一 bridge 給 **整個 U assignments** 的 restriction／union 雙射：
f_L∈K_WL(γ,d)、f_R∈K_WR(γ,h′)，且 d≠h′。
由 β 的完整 R_U={(D,h),(h,D)} 可得 A_WL(β)=A_WR(β)={D,h}：
兩個 tuple 各供應兩個 root 色；任何額外 root 色可與另一塊已存在的 D 色接合，
造成不含雙禁色的完整 tuple，矛盾。這一步用完整 factor join，沒有假定 residual 等於 A_W。

β 在每個 actual 支援 pair 上為相異兩色，{D,h} 正是其補集。
W 的完整 constraints 僅依賴它實際支援 pair 的 literal 色；合法 assignments 在
四色置換下有逐 assignment 雙射。因此對每 proper γ：

```text
A_WL(γ)=Col\{γ(b_L),γ(b_m)},
A_WR(γ)=Col\{γ(b_m),γ(b_R)},
R_U(γ)={(d,h′): d∈A_WL(γ), h′∈A_WR(γ), d≠h′}。
```

精確說，先用一次作用**全部原資料**的 S4，把 β 的該原 pair 映至 γ 的該原 pair；
W 的其餘 boundary 值沒有入射邊，不影響其完整 constraints，再比較同一 W 的 γ query。
這是在共同 literal γ 框內證原 fibres 的非空支援，不把各分量獨立 normalize 或改成另一來源。
最終保留 K_W 全部 assignments，以同一 γ、同一原 bridge 接合，沒有用 palette 取代 full lifts。

若 γ 在 T 見三色，以上兩 palette 分別含 γ(b_R)、γ(b_L)。
取相應原 full W assignments，使 x_L=γ(b_R)、x_R=γ(b_L)；兩 root 色互異。
令 Dγ 為 γ 的未用色，置 **原 r=s=Dγ**。
U 兩原 contacts 都避 Dγ；P/Q 的 N-diagonal 各供完整 assignments 同時避 Dγ。
三份原 pieces 與同一 r/s pins、任意 I 自由 assignments union，即原 G full lift。
所有原 spokes，包括恢復 e=rb_i，均合法，因 **Dγ≠γ(b_i)**。
因此完整 r 投影有明確色 Dγ，沒有把 X 延拓猜成 G 延拓。

三色 C5 的 singleton 位置 k 在 T iff γ 在 T 見三色。
故 **Q(G)⊆B−T**，右側僅兩點。完整 933 的 Q={0,1,2,3} 四點（含 q2），
完整 941 的 Q={0,1,3} 三點都不可能包含於此兩點集。
一次共同 D5 不改大小／包含性，共同 S4 不改 singleton 位置；全部原 β／spoke orbits 都涵蓋。
原 U ordered x1/x2 反向只交換所讀 tuple 的座標，不改任何 contact identity 或 full assignment。
所以完整 H1–H13 來源不存在，**僅為本輪 paper 候選，待獨立採納**。

## 9. 工具校準、實際失敗與封存

[checker](checker.py)只用標準庫；[certificate](certificate.json)為 exclusive-create。
每項 control 明列 `triggered and holds`／`not triggered`／`counterexample`，
沒有把 source 前提未觸發寫成 paper exclusion。

| 控制 | 實際 scope |
| --- | --- |
| 固定同源 toy | 240 proper literal rows、十 canonical rows 的全64 C tuple/r fibres、全16 U fibres、全16 r/s pins，完整 assignments 包含孤立 I 的4因子；X/G 分別21,120／7,488份 full lifts；Cartesian restriction/union 對獨立直接整圖列舉，triggered and holds；無 rotation／完整來源證明 |
| marginals 與恢復 e 的過強版本 | 真 U pair relation 與 Cartesian marginals 禁色不同；另保 X query 有 lift 而全部 G query 被原 e 排掉的 pinned toy，counterexample；不是 HIGH2 source 反例 |
| 不可刪減覆蓋／K₃,₃／K₅ schemas | 6 cover、1,000 K₃,₃、180 K₅ schemas，只核固定色算術、具名袋連通／不交／九或十原鄰接；triggered and holds；有限 schema 不是任意大小圖的 cover |
| U 支援／rooted palette／十列與 orbit 算術 | 1,800支援 cases、1,350完整 factor 算術、1,200 all-row U relations、600 literal singleton／100全 D5 cases；逐完整 tuple，933 q2全留；triggered and holds；無界 palettes／鴿籠及 source 推导仍是 paper |
| finite HIGH2 source | not triggered：未建立、未執行，trigger_count=null；沒有以0 triggers 推得排除 |

[toy 實際來源界線](toy-source-boundary.json)另外核回：它在240列的 G 均有 lift，
恢復 e 對 Σ 冗餘，不滿原 β rejection／X minimality／G 每非框邊 criticality。
所以 toy 明確不是 HIGH2 source，沒有拿未提供的 rotation 當 disk 證書。

實際命令、stdout／stderr／exit 由 [runner](run.py)逐項 exclusive 保存於 logs。
正常／seed17 checker 重播及 read-only 封存結果見 [final checks](checks-final.json) 與 [receipt](receipt.json)，
[首版 checks](checks.json)保留當時的驗證範圍。
receipt 的兩封存子命令保完整 stdout／stderr、exit、cwd、environment 與 hashes。
[manifest](manifest.json)、[delivery](delivery.json)、receipt 逐一綁定；只排除三個
精確 top-level 當前 metadata，negative/nested 的 manifest／delivery／receipt 都是 payload。

| 實跑／拒絕阶段 | 結果與限制 |
| --- | --- |
| normal／seed17 checker | 各 exit0，stdout／stderr相同；certificate 5,775,010bytes，SHA256 `124b85f922c53e76d80b4c2e395bbecff9b6a9192491e66ecee120d347db575a` |
| wrong certificate／wrong input index | 各 exit2，分別在 certificate byte comparison／input validation 拒絕 |
| existing certificate generation | exit2，exclusive certificate create 拒絕，原 certificate bytes 不改 |
| nested receipt omission | 真正 stdin manifest probe exit2，missing 僅 negative/nested/receipt.json，extra/drift皆空 |
| 官方 Gallai bytes | HTTP200，164,927bytes，與 frozen PDF byte-identical；不將 PDF hash 當定理形式化 |
| check_docs／正式 docs DocGraph | 各 exit0，594 Markdown／7,189 local links；62 documents／213 relations／0 errors |
| whole-worktree DocGraph | exit1，62 duplicate-ID errors；完整 stdout／stderr保留，沒有刪 frozen／scratch 解錯 |
| git diff --check | exit0；只核既有 tracked diff whitespace，不替代新 audit 文本核對 |
| outside custody | 初次 exit1；保完整結果與 [custody finding](custody-findings.json)。新 HIGH3／progress-management 路徑出現，outside Git status 並非 unchanged；四個既存 nested-repository directory markers 的錯誤 missing 標記另辨識為未做內容 inventory，原 snapshot／fail log 不改 |
| final source／local／outside checks | 41 frozen inputs／八pins零漂移，既有 indexed regular／symlink 零 byte 漂移；local links／新文本 whitespace 範圍 exit0，封存前僅三個 metadata 連結待建立；outside custody 仍 exit1，來源與整個工作樹界線分開 |

本 report 初次 local check 在 checks.json 尚未建立時也記 missing link；該失敗保留，
後續新 summary 及全部本地連結／新文本 whitespace 另實跑核對。
既有 indexed regular／symlink 的內容及41 frozen inputs／八pins各自核，不用 outside 新增狀態
推稱 source input drift，也不將 source pins 通過改稱整个工作樹 custody 通過。

首版 generation 在 **BASE mapping** 階段 exit2，沒有生成 certificate；
保 [原 checker](checker-v1.py)與 logs/generation 三檔。原因是把 slit-order 已排除的位置
誤要求都有 necessary record。修正為逐實際 lifted supports 檢查：無 placement 是來源排除，
有 record 則保原 role/query。沒有更新 pin 或忽略前提失敗。
[optional freeze finding](dependency-freeze-finding.json)另保不存在的 optional BASE artifact lookup；
未冒稱重播該 artifact，所需 locality theorem 由實際 frozen BASE 文本提供。

全工作樹 DocGraph 的 duplicate-ID FAIL、BASE 兩個 missing-doc 路徑、歷史 E4
provenance replay FAIL 都保留。正式 docs 通過不提升為全域通過，也不修 shared／刪 scratch。
未重跑上游數學分類 generators／來源搜尋／historical provenance／Lean build 或 axioms。

重播（canonical repo root）：

```bash
python3 -B audits/2026-10-10-n45-s-high2/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-10-n45-s-high2/checker.py --check
python3 -B audits/2026-10-10-n45-s-high2/seal.py --check-delivery
PYTHONHASHSEED=17 python3 -B audits/2026-10-10-n45-s-high2/seal.py --check-delivery
```

## 10. 精確停點與 review 入口

候選完成 CORE／COMP／JOIN／RESTORE／F／K33／ARC／MAP／BRIDGE／SPLIT／PALETTE／EXCLUSION。
需獨立 reviewer 核全部 H1–H13、原 critical contact witness、例外 O′ 的九鄰接、
每 W 的實際供應、frame-arc 十原鄰接、任意大小兩 W 及其完整 all-row assignments，
再核 r=Dγ 的恢復邊與全來源 orbit。checker／封存不裁 paper，沒有自行採納。

只新增本專屬 audit。L1 已核 authority／Kempe guide／STATUS 的 HIGH2 OPEN 入口；
此為待獨立採納候選，不修改 shared／old audit、不 commit／push／PR、無再委派或外部訊息。
記錄 33,139 個接手時 Git indexed paths，其中四個是未 hash 內容的 directory markers；
indexed regular／symlink／missing paths 分別核對，outside 新增／Git-status 差異照實保留。
ignored files、directory-marker 子樹與 .git 不在該 inventory，不能宣稱整個 filesystem custody。
HIGH3／long／其他 cores／原55／一般 N2／E／ε≥3 與 Lean 仍 OPEN。
Propagation stop：L0 專屬 evidence 交付；獨立採納及共享文件傳播留待後續授權。
