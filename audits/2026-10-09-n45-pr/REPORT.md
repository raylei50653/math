# N45-PR：同源十列 transport、singleton forcing 與 LP 紙面排除候選

2026-10-09。任務 **N45-PR**；BASE／獨立 clean checkout HEAD：
`dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。
**完成本任務的任意大小紙面交付：N45-U-LP 不存在（在下列全部前提及明列 BASE 紙面依賴內）。**
這是新 paper 候選，待返回後的獨立增量審閱與監督採納；沒有更新共享權威頁的 CLOSED 狀態。

關鍵不是有限 relation 表的零 survivor，而是原 U 盾弧中點在 X 中完全未接內部；
完整 T4 接受迫 core β 的 singleton 正在該點。將低 degree root r 視為 X 中的原 degree4
頂點後，X−s 的**實際原分量**只有 C={r}∪L∪S。高 degree root s 在 β 至多有兩條
不同色 spokes，恰落入已證的單分量 (5)、(4)、(3) 排除。§5 逐項給前提對照。
沒有 contraction、coloring replacement、新 graph 搜尋或新任意大小正常形假設。

同時交付五項可重用的完整 relation／forcing 引理（§2–4）。有限證書只承擔其固定控制
校準及七格必要表的覆蓋帳，不承擔 paper 的無界 Gallai／拓撲證明。

[正式 checker](checker-final.py) · [正式證書](certificate-final.json) ·
[輸入](inputs.json) · [新增 BASE 依賴](supplementary-inputs.json) ·
[逐命令檢查](checks.json) · [輸出 hash 清單](MANIFEST.sha256) · [封存回條](delivery.json)。
初始 [checker](checker.py)／[certificate](certificate.json) 保留當時的必要 tensor 階段；
正式交付以 `checker-final.py`／`certificate-final.json` 為準，沒有覆寫初版或失敗紀錄。

## 1. 精確命題、來源與信任範圍

**N45-PR-LP-EXCLUSION 的量詞。** 所有任意大小有限簡單 disk 原圖 G、具名原 pieces
U,L,S、原拒絕 literal β 與 X；不對頂點數、bridge 長度或 contacts 數新增上限。

全部本輪圖前提如下：

- 指定有序 induced 外框 B=(b0,…,b4)；完整 Σ(G)=933／941，或對**整圖共同**搬運的 D5 像。
  每條非框邊 Σ-critical；有效 H 忽略孤立內點，ε(G)=2。
- 恰兩非相鄰原 degree5 roots r,s，其餘有效原內點完整 degree4；原 full B-touch、H 連通。
  H−{r,s} 恰兩完整 mixed L,S 及唯一完整 unary U；所有 pieces one-sided。
- 唯一原 unary U 的唯一原 root-contact 為 rx。X=G−V(U)=M 是 β 的
  inclusion-minimal 原 45／54 core；共同 root 交換後 deg_X(r)=4、deg_X(s)=5。
  X 保留兩份 mixed、全部其餘原頂點、附件、內邊、spokes 與原 rotation 的限制。
- L 原 support long；S 原 actual support 為真框邊兩端點。沿已採納結果，原盾弧
  (σ_U,σ_L,σ_S) 長度為 (2,2,1)，邊互斥且分割五框邊；U/L support 各為該三點連續弧。
- 所有 named ordered contacts、shared contact 單一座標、實際附件／support、ownership、
  原 bridges、rotation、同一 literal 色框、完整 tuples／空 fibres／全部 full lifts 固定。
  每份 mixed 在兩側 root incidence 均正。

**權威版本。** 新 [N45 入口](frozen/docs/c5_excess_two_nonadjacent_unit_core45.md)、
[任務全文](frozen/docs/history/2026-10-09-n45-u-long-short-pair-tasks.md)、
[U](frozen/audits/2026-10-09-n45-u/REPORT.md)、
[SU-A](frozen/audits/2026-10-09-n45-su-a/REPORT.md)、
[SU-J](frozen/audits/2026-10-09-n45-su-j/REPORT.md) 及
[監督採納](frozen/audits/2026-10-09-n45-su-supervision/REPORT.md) 均為 frozen 工作交付，
不是 BASE Git blob。任務頭九個指定 SHA256 全部相符；SU-A 56、SU-J 5952 項
manifest 逐 bytes／精確 inventory 驗證，S/U/J 的 22／39／90 authored snapshots 對回。
J 指定 certificate 的實際路徑是 `results/certificate.json`。

數學 BASE 依賴只讀本目錄 [clean checkout](base-source/docs/HANDOFF.md)，
全部指定閱讀另對 `git show BASE:path` 的原 bytes。

| 依賴／證據層 | 本輪用途與充分前提 |
| --- | --- |
| [E2 §2、§3.3](base-source/artifacts/c5_excess_one_e2/REPORT.md) | T4 未接框點改色、唯一 degree5 minimal-q 分支；不將 ε1 的 Q 分類當來源實現 |
| [原盾弧 §2](base-source/docs/c5_unary_shield_budget.md) | σ_U 長2的原內點不被 H−U 碰到；不假設 X 自己 full B-touch |
| [E4 §4.1、§6](base-source/artifacts/c5_excess_two_e4/REPORT.md) | 原 local hub（只需 N(P) 上 pins）、完整 tuple 接合、χ=0；不把 minors 當 replacement |
| [B-C2](base-source/docs/c5_phase_b_common_lemmas.md) | 完整原 degree4 mixed 欄界與 raw-column 容量；不跨列加容量 |
| [未接框點引理 §1](base-source/docs/c5_unattached_boundary.md) | induced C5＋T4＋一個無內鄰框點 ⇒ Σ 至多只拒其 singleton；不需 X full B-touch |
| [no-spoke §4](base-source/docs/c5_no_spoke_exterior.md) | 唯一 degree5、minimal-q、H−root 為一份五接點 C：四份原 block palettes 的偶數接點矛盾；不需 root–B 外路 |
| [single-spoke (4) §1–5](base-source/docs/c5_single_spoke_four.md) | 唯一 degree5、minimal-q、一 spoke、一份四接點 C：同一三份 palettes／active blocks／原 K5 |
| [two-spoke (3) §1–5](base-source/docs/c5_two_spoke_three_contacts.md) | 唯一 degree5、minimal-q、兩條不同 β 色 spokes、一份三接點 C：原 active triangle／三 arms／tethers／K5；§5 明涵蓋任意 spoke 位置 |
| 外部 Gallai | Dvořák [Lemma7／Theorem10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，PDF 第5／6頁；本輪讀原始 PDF 核其陳述。嚴格 slack⇒可染、不可染 degree assignment⇒原 Gallai／blockwise-uniform。外部依賴另列 |

本輪重新讀上述 BASE 的具名充分前提及關鍵排除步驟；沒有重證所有上游 theorem 或重跑
上游全部 Python／Lean。BASE 任意大小紙面與外部分類是新 paper 的明示信任依賴。

## 2. N45-PR-TRANSPORT：同一 piece 的全部 lifts 搬運

**量詞與最弱充分前提。** 任意固定具名 piece P，固定全部原內邊、P–B attachments、
ordered contacts 及 shared identity。對任意 proper literal β,γ 及**一個**色雙射 π∈S4，
若每個 b∈actual support S_P 都滿足 γ(b)=π(β(b))，則

`Lifts_P(γ) = {π∘f : f∈Lifts_P(β)}`，

且完整 ordered R_P、每個 tuple 的全部 full lifts、任意 root pins 的完整 fibre
都按同一 π 雙射。empty fibre 亦搬運到 empty fibre；逆搬用 π⁻¹。

**證明。** 每條原內邊的不等色性由雙射保留；每條原附件 vb 的色禁令由
γ(b)=πβ(b) 逐原邊保留。接點讀取同一原頂點，shared 坐標只映一次；
全部 root-contact 不等式與 pins 一起映射。逆映射給完整性，而非只有 inclusion。
不需要 disk、criticality 或大小界。

此 lemma 不是逐 piece 重新正規化 source。比較兩份全图列時，各 piece 的查詢須
落回該列同一組 literal pins；不同 pieces 的 support transport π 可以不同，
但不能將它們搬出的 pins 各自當同一個全圖 pin。整圖 D5／root swap 則連所有
附件、contacts、vertices、rotation 與 literal frame 一起搬；root swap 轉置全部 fibres。

對 LP 的三点 U/L support，局部色形只有 ABA=010、ABC=012；S pair 只有 AB=01。
因此十列完整介面由**同一原圖的五份原 tensor**
`R_U^ABA,R_U^ABC,R_L^ABA,R_L^ABC,R_S^AB` 搬運取得。
每份 tensor 仍含任意大小的原 interiors／完整 tuple／全部 lifts；有限 tensor 種類
不代表有限 graph 正常形或可實現性。它們也不構成 specified-colouring repair：本輪不
要求修改一份已指定全圖染色，沒有 replacement theorem。

證據層：上述任意大小代數 paper；固定控制直接由原 edges 重建 690 份 relations／
2986 full piece lifts，核 9721 個 support-compatible 色雙射及155536個完整 pin fibres。
未涵蓋：未證任意抽象 tensor 是 disk degree4／critical source 的 tensor。
Finding：無 transport 反例；來源 coverage 另見 §7。

## 3. N45-PR-ENDPOINT、SATURATION 與 ESCAPE

### 3.1 Endpoint 色的原 hub 局部接回

**充分前提。** 原 disk G，連通 P 完整 degree4；H−P 原連通、G full B-touch；
actual support 為三個連續框點 h–m–k。P 的全部 root 鄰點都在 H−P。
對任意 proper β，若把 P 的所有 owner roots 同時指定為 a=β(h)，則 P 有完整 lift；
a=β(k) 對稱。對 mixed L 是 endpoint 色的 diagonal acceptance；對 unary U 是 root 接回。

**原 bags。** 記 K=H−P。若 β(h)≠β(k)，取

`X0 = K ∪ (B\{m,k}), X1={m}, X2={k}`。

B\{m,k} 是含 h 的原三点框路徑；兩個位於 P support 外的框点被 full B-touch
迫由 K 碰到。因此 X0 原連通。三袋互斥、避 P；原框邊 h–m、m–k 及 k 的另一框邊
給三條袋間鄰接。N(P)∩X0 只有 owner roots 與 h，皆 pin a；另兩袋分別見 β(m),β(k)，
三色互異。若 β(h)=β(k)，將 X0 與 {k} 合併為 K∪(B\{m})，與 {m} 成兩袋。

反設不可填，完整 degree4 lists tight；逐點禁止同色袋中重鄰，使收縮只在 minor
反證內保 degree/lists。BASE E4 §4.1 的 **local** hub 原則／原兩三 hub Gallai K5
給非平面矛盾。只指定 N(P) 上 pins，不假設整個 outside 已有合法染色。
沒有聲稱 auxiliary hubs 是 coloring replacement 或保持 Σ 的來源操作。

U 的 T_U 非空且 T_U singleton 才 F_U singleton。Endpoint 接回排除 singleton 等於
support 的兩端色。ABA 的兩個未見色可互換而 R_U 不變，singleton 不可能是其中一個。
故有新的必要 forcing 角色表：

| 原 U support 色形 | 若 T_U 是 singleton，其唯一容許角色 |
| --- | --- |
| ABA | 中點色 β(m) |
| ABC | 中點色 β(m)，或 support 未見的唯一第四色 |

這在 Δ 每列成立；同一色形的角色由 TRANSPORT 固定，不能每列改選。
固定控制有18份 eligible 原 triple unary，360個 endpoint pins，各交原 bags、原 spanning
edges、袋間原邊與完整 piece lift。既存域沒有長 mixed triple 的控制；該新應用由 paper
充分前提承擔，不借 unary 控制充當長 mixed 來源控制。

### 3.2 每個 saturated raw column 迫所有 contact lifts 滿色

**N45-PR-SATURATION。** 固定同一原 mixed C、β、s=b，完整 s-compatible relation
非空；r 有 k 個不同原 contacts。令 F_C(b) 為從整份 relation 取得的 forbidden r column。
若 |F_C(b)|=k，則**每個** s-compatible full lift 在 k 個 r contacts 上都用 k 個不同色，
其色集合恰是 F_C(b)。

證明：每個 forbidden a 必出現在每個 s-compatible 完整 contact tuple 的 r 位置；
所以 F_C(b) 包含於每份 tuple 的該色集合。只有 k 個位置，兩者大小 k 迫相等。
shared r/s contact 在同一 tuple 中同時受 s=b 約束，沒有另製 marginal。
不需 disk；缺完整 relation 非空／不同具名 contacts 時不得搬用。

在 core β 的五項 zero slack 下，對每個 b∈E_s，原 L/S 全部 s-compatible lifts
各滿 k_L^r／k_S^r 個不同色；兩色集合互斥並分割 E_r^X，long 禁(D,D)，short 收(D,D)。
固定控制100個 raw saturated columns核全部相容 tuples／全部 lifts；不只挑一個 witness。

### 3.3 原接受列的同 shape escape 義務

**N45-PR-ESCAPE。** 任意固定 G=X 接回原唯一-contact U，沿 U-REL 的精確完整 join。
若 γ∈Δ 使 T_U(γ)={a}，且已接受的 β′∈Σ(G) 在 U support 上可由 π 從 γ 搬到，
則 T_U(β′)={π(a)}，而 X 在 β′ 必有完整 lift，其 r 色不等於 π(a)。

證明：TRANSPORT 先搬整 U palette。G 在 β′ 的合法 full lift 限制到 X；原 rx
必合法，所以其中 r 避开 U 唯一色。它的全部原 contact tuples 與 interiors 保留。
這是接受列的存在見證義務，不是只看 endpoint marginals 的 repair 或跨列容量收費。
證書逐七格、十列列出 same-shape 的原接受列；沒有補造目標來源 lift。

三項皆為任意大小 paper；未涵蓋任意 abstract relation schedule 的原圖實現。
Finding：mixed-long endpoint 與精確 LP positive source 控制缺失，不由有限 PASS 填補。

## 4. N45-PR-FORCING：新接受列的逐欄容量只留一單位

**量詞／充分前提。** 任意同一原 X，非相鄰 roots r,s；X 恰兩 complete mixed、無 unary，
其餘 piece 頂點完整 degree4，deg_X(r)=4。任意 proper γ，完整 X join 非空且
全部 X lifts 的 r 投影是 {a}；局部 s=b fibre 非空及原 contact 欄界 |F_C(b)|≤k_C^r。
這些局部前提由原 degree4 strict slack 給出。沒有指定 target、disk 或 arbitrary-size 正常形。

記 t_r 為原 retained spokes 數、m_r=k_L^r+k_S^r，
`d_r=t_r−|γ(N_B(r))|` 為 spoke 重色數。因此
`|E_r|=m_r+d_r`（t_r+m_r=4）。對每個 b∈E_s，以完整 tuple 算 raw columns
F_L(b),F_S(b)、V_b=F_L(b)∪F_S(b)，並令

`n_b=|E_r\V_b|∈{0,1}`，
`δ_b=m_r−|F_L(b)|−|F_S(b)|`，
`o_b=|F_L(b)|+|F_S(b)|−|V_b|`，
`λ_b=|V_b\E_r|`。

三項皆非負，且精確有

`δ_b + o_b + λ_b = n_b − d_r`。

**證明。** 完整 joint 使 E_r\V_b 為該 b 欄的全部接受 r 色；singleton 投影迫它
為 ∅ 或 {a}。左式=m_r−|V_b∩E_r|=m_r−|E_r|+n_b，代入 degree 計數。
由非空 joint 至少一欄 n_b=1，得 d_r≤1：

- d_r=0：空欄三项各零；接受欄三项之和恰1。
- d_r=1：所有 b∈E_s 都有 n_b=1且δ=o=λ=0；每欄 L/S saturated、互斥並分割
  E_r\{a}，a 對兩 mixed 都可接回。因此完整 K_X(γ)={a}×E_s，而非只找到一個 pin pair。

這是同一 γ 的精確恒等式；core β 的五項零與其他 γ 的一單位不能相加。
Δ 上再用 U-REL，a 等於同一原 U palette 的唯一色。不同 rows 的全部欄由同一原 tensors
給出，不另取 pieces 或逐列 S4。

固定控制：7份 N2 整 U derivatives 的70列完整 join重核，29列 singleton r-projection，
其中7列是真正原 G 新接受 γ；全部29列 d_r=0。d_r=1 的 Cartesian 情形缺控制；
任意大小結論由上述 algebra 承擔。原 N1 derivatives 另列 not triggered，不能補 N2 coverage。

## 5. N45-PR-UNTOP 與 LP 任意大小排除

### 5.1 原未接框點迫 Q(X) 為唯一 singleton

設原 U support 為 h–m–k、原盾弧就是兩邊 h–m,m–k。
BASE 原盾弧引理1(c) 說 N_B(H−U) 不碰 σ_U 的內點 m。
U 外的所有原內点，包括 r,s、L,S、全部 root spokes，均在 H−U。
所以整 U 省略後 **m 在 X 中沒有 B 外鄰點**。這是在原 G 上推出的實際邊限制；
没有錯用 σ_X(U)，也沒有假設 X full B-touch。

X 作為 G 子圖接受所有 T4。BASE 未接框點引理按同一 full coloring 改回 m，
推出 `Σ(X)⊇Ω\{q_m}`。X 拒絕 core β，故

`β=q_m（同一 canonical 列的所有 S4 像），Q(X)={m}`。

因此不是任選七格 Q 必要表的一個 mask。所有七格均先保留，然後原幾何實際
排掉錯 β 或相鄰 pair；933 的 q2 在中點 m=2 時照常保留。
Δ 的精確新列是 `Q(G)\{m}`，canonical 941 有2列、933有3列；每列仍滿足 §3–4
的同源 singleton forcing 與原接受列 escape。它們的容量没有跨列相加。

### 5.2 把 r 放回 degree4 層，得到 X 的 sole component

X 自己 β-minimal，因此刪任何 retained 非框邊都接受 β；這一步使用 X=M，
不是將原 G 的 Σ-criticality 無條件遺傳給 derivative。
原 s 無 U 邊，所以 deg_X(s)=5；r 只失 rx，所以 deg_X(r)=4。
其餘原 retained 頂點完整 degree4，X 仍是同一 induced-C5 disk 子圖。

在 X 的唯一 degree5 root s 下，實際

`C = H_X−{s} = {r}∪V(L)∪V(S)`

連通：原 L,S 各連通，且各有至少一條原 r-contact，兩份便由**同一原頂點 r**接在一起。
所有 s 到 C 的原 edges 仍在，contacts 是原 L/S 的 s-contact 聯集，每個原 vertex
只一座標；若一份 piece 在 r/s 有 shared contact，該座標仍只讀一次。
C 每個頂點在 X 完整 degree4，s 是唯一 degree5，沒有其餘 X−s 分量。

這只是依實際 degree 重新辨識 X 的連通分量，沒有合併頂點或作 coloring replacement。
其完整 R_C 由同一 literal β 的原 r 色、spokes、整 L/S tuples 及 full lifts 接合而成：

`Lifts_C(β) = ⋃_{a∈E_r^X} {r↦a} × Lifts_L(β;r=a) × Lifts_S(β;r=a)`。

s-contact tuples 由上述完整 lifts 在原 ordered contacts 上讀取；保留全部 fibres。
在新 γ／其餘九列也用**完全相同的原 C**與原邊式，不逐列選另一分量。
X 的 β 拒絕因此等價於 sole C 阻擋 s 的全部可用色。

### 5.3 β-minimality 迫 t_s≤2；三個既有任意大小分支全排

m 在 X 沒有內鄰點，故 s 的所有 spokes 端點在 B\{m}。β=q_m 在這四個框點
只有兩色。若 s 有兩條同 β 色 spokes，刪其中一條不改任何 root 色限制，
X 仍拒 β，違反 X 的 edge β-minimality。故 s 的 spokes 色互異，`0≤t_s≤2`。

因 X−s=C 是一份原連通分量，s 的剩餘 `5−t_s` incident 邊全部是 C contacts。
未固定 s 時 C 的完整 relation 非空，由 contacts strict slack 保證。
β-minimality 也保每條 spoke 色不在 F_C：刪該 spoke 後的接受 β full lift只能
使用其釋放的 root 色（其他 root 色原本都被拒絕）。因此

`F_C(β)=Col\β(N_B(s))`，大小為 `4−t_s`。

| t_s | 實際 X−s 分拆／完整禁色 | 已證排除與逐項適用核對 |
| --- | --- | --- |
| 0 | sole C，有5具名 contacts，F_C=Col | no-spoke §4 的同一四份 Gallai palettes 迫 contact 數偶數；5矛盾。沒有假設 s 與 B 在 C 外連通 |
| 1 | sole C，有4具名 contacts，F_C 為其餘三色 | single-spoke (4) 的同一三份 palettes 迫兩 active triangles＋原 bridge，原 boundary tethers 給 K5；原 spoke 提供外部連通 |
| 2 | sole C，有3具名 contacts，F_C 為其餘兩色 | two-spoke (3) 的兩份同源 palettes、同一 active triangle／三 arms／原 tethers 給 K5；§5 明許任意兩個 β 異色 spoke 位置，已由 minimality 證異色 |

三個原 theorem 的 source hypotheses 全由 X 自身驗得：有限簡單 induced-C5 disk、
有效內部連通、edge minimal-q、唯一完整 degree5、其餘完整 degree4、sole C、相應 t_s。
必要時對**整 X 及其原 contacts／rotation**共同 D5＋S4，把 β 搬成 q=01012；
不是獨立正規化 C，也不要求 β 的拒絕位置仍是 canonical target 的同一 index。
三個排除不需第二列拒絕或 T4；本題額外 T4 已用於 §5.1。沒有未知有限化約義務。

結論：所有 t_s 皆矛盾，因此本任務定義的 N45-U-LP 不存在。
證據層：任意大小 paper，明依 BASE 單-root 排除及外部 Gallai；無新 Lean。
Finding：本輪發現可用的原未接框點／實際 sole-component 對接，沒有改動或否定已採納 S/U claim。

### 5.4 七格、D5 及 root swap 的覆蓋

證書保留原941／933七格共15個 (β,Q_X) 選項；十個具名(2,2,1)盾分割均列出十個
literal β 及 support 色形。共150個必要 mask cases中，120個因 core β≠U中點、
16個因 Q_X 為 pair 而由 §5.1 排掉；剩14個（941六、933八）各對上 t_s=0,1,2 三分，
共42個條件分支由 §5.3 的原 theorem 排除。這是 proof 的算術覆蓋帳，不是150張來源圖。

十個 whole-frame D5 action 逐列搬 actual β 再用同一全圖 S4 還原 canonical frame；
完整 mask一起搬，沒有將所有 relocated target 重新叫 canonical933／941。
root r,s 的共同交換轉置所有 fibres／owner contacts，低度側仍命名 r，以上論證相同。
未對 PG 結果作前提，沒有等待或讀 PG／PC 新交付。

## 6. 未涵蓋、coverage 與 finding

| 項目 | 分類／本輪界線 |
| --- | --- |
| 五項 relation lemmas | 任意大小 paper 在各自充分前提內；固定 complete-lift calibration另列 |
| N45-U-LP 排除候選 | §1全部前提內有完整任意大小 proof；新採納待獨立增量審閱；不是有限零survivor推論 |
| 精確 LP 原來源 positive control | **not triggered**，既存11份整 U derivative 均缺完整 LP／target／拒絕core契約；7份N2、4份N1分列 |
| Endpoint lemma | 18份 unary triple 有控制；長 mixed triple **缺控制**，不是 counterexample |
| Forcing d_r=1 分支 | **缺控制**；29份實際 singleton 行均 d_r=0 |
| Source counterexample／abstract collision | 沒有建立任何一份；不把必要 masks、tuple刪漏負資料或 certificate損壞叫数学source反例 |
| 歷史 provenance | 舊 E4 core／reductions byte replay FAIL繼續保留；舊 E3 REPORT來源hash不同，本輪沒有重跑或改舊證書 |
| 原 u2、兩short、U1–U4 | 沿已採納結果；本輪沒有重開、擴大搜尋或重新宣稱全套驗證 |
| singleton short、S LOW/HIGH/long、原55、其他core、一般N2/E、ε≥3 | 本輪未作裁決，維持原權威頁 OPEN。新 proof 僅交 LP scope；不自行選下一個分支 |
| Lean／source realization | 無新 theorem／native_decide，未建立目標 source；finite controls不替代上游任意大小分類 |

N45-PR-F01：新的 LP 紙面排除須獨立審查 §5 的「原盾弧內點→X未接框點→實際 sole C→
三個已證原 theorem」前提鏈；目前只有本執行者 paper 交付，沒有冒稱監督已正式採納。
N45-PR-F02：精確來源控制及 mixed endpoint／d_r=1 控制缺口如上；不要求擴大 k 找控制。
N45-PR-F03：本輪 setup 首次錯讀 J certificate top-level 路徑而 exit1；修正為
`results/certificate.json` 後九個指定 anchors／精確 manifests全過。原 setup及failure紀錄保留。
三次 wrapper option位置错误沒有啟動目標checker；按 argparse 的正確位置重跑，原記錄保留。

## 7. 固定證書、實際重播與保留 FAIL

本輪 checker 使用標準函式庫，沒有 import worker checker。只在已凍結 SU-J 原23張圖的
69份 pieces（最大3頂點）重建完整 local colorings；沒有枚舉新 pieces／source或調高 k。
每份 solver oracle 是原內邊＋全部原 attachments；完整 tuple／shared coordinates／full lifts
逐份對保存的 SU-J relation。所有16 pin fibres、空 fibres及各 root方向照留。

| 正式 checker 的固定計數 | 內容 |
| --- | --- |
| 690 relations／2986完整piece lifts／11040 pin fibres | 對原edges獨立重建，全部相符 |
| 9721 full-lift transport maps／155536 pin-fibre transports | 每個 actual-support-compatible全色雙射及全部16fibres；重複來回不是不同source數 |
| 360 endpoint pins | 18份原 unary triple ×10列×2端點；交原hub bags／連通邊／全部袋間原邊及完整piece lift |
| 100 saturated columns | 每個 s-compatible tuple／全部原lift在 r contacts 上確為滿額同色集合 |
| 29 singleton rows／7新γ | N2 retained two-mixed join；逐欄δ+o+λ=n−d_r；d_r=1沒有控制 |
| 7格、15選項、10盾分割、10 D5 actions | 紙面必要表及原圖搬運的有限索引校準；LP來源0觸發 |

```sh
python3 -B audits/2026-10-09-n45-pr/checker-final.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-09-n45-pr/checker-final.py --check
```

正式 certificate SHA256：
`d7d59397814d3007067374e9cb5fc737589d6bfdd33c9f609924bc645b663827`。
普通／seed17各 exit0且逐byte相同；--check不寫任何輸入或證書。
existing-certificate生成拒絕與損壞certificate拒絕各預期exit1，原證書未覆寫。
刪一整個含 shared contact 的 tuple／其合法原 full lift 作負資料，原邊枚舉 oracle
確實發現漏資料；見 [负控制](negative/omitted-complete-tuple.json)。不是原圖反例。

| 文件／邊界檢查 | 實際結果 |
| --- | --- |
| fresh BASE check_docs | **FAIL，exit1**：586 Markdown／6982 links，兩個歷史缺檔（下列路徑） |
| fresh BASE 正式 docs DocGraph | exit0，62 documents／213 relations／5 families／0 errors |
| 主worktree whole DocGraph | **FAIL，exit1**：62 duplicate-ID errors；scratch、U／SU-J及本輪clean checkout等來源副本保留 |
| shared／BASE tracked git diff --check | 各exit0；僅驗其tracked diff，自己的新增text／JSON／links另核 |
| 最終 input bytes／mtime、own checkout HEAD／clean status及輸出檢查 | 見 checks.json 與 output-validation.json；實际凍結時核，不將其他worker新增目錄誤作本任務寫入 |

fresh BASE仍缺 `audits/2026-10-04-task-d5/c4/scope_ledger.json` 與
`audits/2026-10-04-task-d2/integration_doc_changes.diff`。沒有補造或刪檔隱藏FAIL；
正式 docs PASS不改稱whole-worktree PASS，歷史E4 FAIL也不改稱通過。

未跑：S/U/J/SU-J全部原checker二次重播（本輪另有獨立原邊local oracle），
全部上游枚舉／minimal cores、ES/ER、U1–U4、新k、Lean build／axioms、remote CI。
理由：新增的是 paper 接合與指定fixed-calibration；沒有改上游或新增Lean claim。

## 8. 返回、傳播與停止點

L0交付只在本fresh目錄。已核 BASE DOCUMENTATION、HANDOFF、STATUS、Kempe相關OPEN入口；
當前 frozen N45 authority亦仍OPEN。使用者任務明令不改共享文件，故此paper候選在本目錄
交獨立審阅，由監督驗收後更新 authority／guide／STATUS及直接父題。沒有提前管理closure。
父N2／一般E未被本輪關閉；不依本paper先选下一個residual。

返回的精確增量審查點：

1. 對回九anchors與manifest／正式證書hash，再核全部原輸入immutable。
2. 審 §5.1 的原σ_U中點在 X 無任何內邊、T4改色且保933q2。
3. 審 §5.2 是實際 X−s 連通C，r自身原degree4、完整relation沒有換圖或拆shared coordinate。
4. 審 §5.3 三條舊theorem的充分前提，尤其 t=0不用外部root–B路、t=2任意異色spokes。
5. 新結論只採纳 N45-U-LP；endpoint／forcing通用lemma按各自較弱前提另裁決，finite coverage分開。

Closure scope／Canonical Source＋Evidence：本報告 §1、§5與具名BASE依賴；本finite證書只校準。
Updated：本N45-PR fresh交付。Reviewed-unchanged：共享N45、Kempe guide、Phase B、E4及STATUS；
待新paper正式採納才傳播。Remaining OPEN：所有任務排除在外的來源線，以及本paper的獨立採納。
Propagation stop：L0交付／L1只讀對回，沒有共享寫入、commit、push、PR、外部訊息或sub-agent。
