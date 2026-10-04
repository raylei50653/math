# 任務 E6：相鄰雙 degree-5 roots 的 ε=2 殘留

2026-10-04；基準 `integrate-kprime-e3 @ d00aba4e10ea2d05ab216fedd94f5a166b2777ad`。
獨立 worktree `/home/ray/developer/ai/math-task-e6-adjacent`，分支 `task-e6-adjacent`。
只新增本任務檔案；不修改歷史文件、報告、checker；不 commit／push。

**相鄰 m≤2 已證；G1–G4 與 J6 得到新的整型必要限制，仍有精確殘留。**
沒有證成猜想 E 的整個 ε=2 層，也沒有把殘留全部交給 K′。
沒有逐 source key 枚舉，沒有構造候選反例，沒有發現新的前序判定錯誤。

## 1. 前提、列身份與依賴

G 有限簡單，指定有序 induced C₅ `B=(b₀,…,b₄)` 圍 disk 外面。
全部 T4 接受，每條非框邊 Σ-critical；有效私有內點 H 忽略孤立點。
兩個相鄰 roots z,w 完整 degree 五，其餘完整 degree 四，ε=2。
完整 degree 包含全部原內邊與 actual 框附件。H 連通；兩個拒絕列迫全 B-touch。

固定拒絕三列：q₀=`01212`（row 6）、q₁=`01202`（row 4）、q₃=`01021`（row 1）。
q₂=`01201`（row 3）、q₄=`01012`（row 0）不預填接受性。
因此四個互斥完整 mask 是 941、933、940、932；T4 mask=932。

使用 [E3 §2.1、§3、§6、§10](../c5_excess_two_e3/REPORT.md)、
[E3 相鄰審查](../c5_excess_two_e3/adjacent_notes.md)、
[E5 L1–L8](../c5_excess_two_e5/REPORT.md)、
[E4 N-empty-separating、N-theta](../c5_excess_two_e4/REPORT.md)、
[原盾弧／hub 原則](../../docs/c5_unary_shield_budget.md)、
[單接點固定色守恆 §2](../../docs/c5_single_spoke_root_conservation.md)。
E3 對 A 前序的過強依賴已在其 §10 更正，這裡直接使用 E5 L6。

紙面論證負責任意大小的 Jordan、Gallai、原 core 分類與 hub 推導。
Python 只重算指定圖的完整染色、實際 rotation／盾弧及固定字面欄位。
沒有四色定理 oracle，沒有新增 Lean theorem，也未執行 lake build。

## 2. E6-A：四條原路證明相鄰 m≤2

反設有三份不同原 mixed `C₁,C₂,C₃`。每份連通且接 z,w，取簡單路
`Pᵢ=z–xᵢ↝Cᵢ yᵢ–w`；容許 xᵢ=yᵢ，此時路長二。
另外取 `P₀=zw`。四路內部互斥且全部不碰 B，形成四條平行邊的平面 subdivision。
每個面的邊界恰由兩條循環相鄰路徑組成。
唯一包含 B 的互補區是無界面，其邊界是某兩路組成的 Jordan cycle J。

必須分開兩種情形：

1. **zw 是外側邊界的一條路。** 另一條邊界路是 mixed 路；剩餘兩條 mixed 路的內點均在 J 有界側。
2. **zw 不在外側邊界。** J 由兩條 mixed 路圍成；第三條 mixed 路的內點與 zw 均在有界側。

兩者都至少有一份內側 mixed C。不是只看所取路：**整份原 C** 連通、
與 J 不交（roots 不屬 C，另外兩路屬不同 pieces），又有內點在有界側，
所以其全部原頂點、原內邊都在有界側。任何 actual C–B 邊都必穿越 J，
故 `N_B(C)=∅`。

逐一核對 N-empty 的前提：C 是原 degree-four piece，外鄰僅 z,w；
刪 C 後 zw 仍在，其餘每份 piece 接至少一個 root，所以 H−C 連通，C one-sided。
C 無框附件，原全 B-touch 不受刪 C 影響，故 G−C 連通。
對合法外染色，zw 迫 z,w 異色；`{z},{w}` 是原連通、互斥、相鄰的兩個 hubs，
各在 N(C) 上只見對應 root 色。由原 degree-four tightness 及 hub 原則，C 可完整接回。

這正是 E3 one-sided N-empty 的適用情形；也獨立符合 E4 N-empty-separating
的「G−C 連通」分支。其 separating／無框 appendage 分支在此沒有觸發，
不假造替代路，也不給 separating piece 收盾弧。
取任一原 root–C 邊 e 的 Σ-critical witness：G−e 的新染色限制到 G−C，
再完整接回原 C，就成為原 G 的延拓，矛盾。故 **m≤2**。

本論證不讀指定三列的身份；H 連通等來源結構仍必須成立。
J6 的全部 `m≥3`，包含 `(4,5)`、`(5,4)`、原 `(5,5)` cores，四分支一律關閉。

**m=2 的附帶限制。** 任取兩份 mixed 的原路與 zw，得到 theta。
若 zw 參與含 B 面的邊界，另一份 mixed 的整份原分量被封在內側，仍違 N-empty。
所以此面必由兩條 mixed 路圍成，zw 在其有界側。

[reductions.json](reductions.json) 保存兩份無交叉直線 disk、完整 rotations／faces，
分別覆蓋上述兩種外側邊界；內側分量另帶一個 off-path 原頂點，實際驗整份支援為空。
它們只是拓撲示例，不冒充 degree-valid Σ-critical 正控制。

## 3. E6-B／C：J6 的共同 core、欄位與框邊預算

令 t_r 為 root 原 spokes 數，k_r(P) 為 piece P 對 r 的全部實際 incidences。
每 root 滿足 `t_r+Σ_P k_r(P)=4`；T4 使 t_r≤3。
zw 使所有原 pieces one-sided。沿用原 critical witness 的盾弧論證：
每份 unary 的 actual support 是至少三點連續框弧、盾弧長至少二；
全部 pieces 的盾弧邊互斥、總長≤5，所以 unary 數 u≤2。
long mixed（支援不包含於任何框邊）亦成本至少二；兩點 short mixed 成本一，
singleton 支援成本零。所有成本均取同一原嵌入的 actual 盾弧。

L1 給每個 proper S 的 Q_S 為空、單點或相鄰 pair。
因此每條非框邊刪除至少釋放 `|Q_G|−2` 個原拒絕列，且釋放 q₀/q₁/q₃ 至少一個。
這不是把 G 當成每列自己的 minimal q-core，也不是 Σ(S)=Ω。

對 m≥1，原 root／zw 全收引理迫任一 q-core 保留 z,w,zw。
原 degree-four 飽和使每份原 piece 全取或全不取；省略向量之和屬 `{0,1}²`。

| q-core 的原 root degrees | 唯一可能的省略身份 |
| --- | --- |
| (4,5)／(5,4) | 降度側一條原 spoke，或一整份 capacity-one unary |
| (4,4) | 每側各一個 unit side 因子，或只省略一整份 incidence-(1,1) mixed |
| (5,5) | 無；由原連通 H 飽和傳播，core 就是原 G |

m=2 時保留两份 mixed 会与 zw 形成长至少四的原环，违反全四 core 分类。
故其 (4,4) 只能省略一份 mixed11；剩下 mixed 也必须 incidence11、两 contacts 同是原 x，
形成原 zwx triangle。被省略的 mixed 的两 contacts 不要求相同。
m=1 retaining (4,4) 同样迫 C11 共用 x；双-spoke 省略已由 E3 三列论证排除。
这些身份没有排除其余 (4,5)/(5,4)/(5,5) 的完整跨列 joints。

**E6-C：通用 spoke 冗餘限制。** 對 e=rb_j，定義
`D_e={q∈Q_G: 某另一原 r-spoke rb_k 滿足 β_q(j)=β_q(k)}`。
在同一 β 下刪 e 完全不改 root guard，所以 `D_e⊆Q_(G−e)`。
L1 迫 D_e 亦為空、單點或相鄰 pair。十個三-spoke 子集的字面欄位給：

| 完整 mask | 通用 L1 的必要三-spoke 集 | G2／G3 可另用 E5 L3 的較強必要集 |
| --- | --- | --- |
| 941 | 012、013、014、034、123、234 | 012、014、034、123 |
| 933 | 012、014、034、123、234 | 012、123 |
| 940 | 012、014、034、123、234 | 014、034 |
| 932 | 012、014、034、123、234 | 空 |

通用欄位表適用任何 mixed 數及 core 型；沒有把 E5 L3 擴張到未知的 J6 身份。
有限 checker 記錄全部十個子集／每條原 spoke 的 D_e，而非逐來源 key。

## 4. E6-D：no-mixed 的整側預算與精確殘留

m=0 時每個 root 的剩餘容量四；t_r≤3 迫每側至少一份 unary。
總 unary≤2，所以恰一份 U_z、一份 U_w，容量為 `4−t_z`、`4−t_w`。
令完整原側 `A_r={r}∪U_r`。兩側連通、互斥，補側也連通；
純拓撲盾弧引理的證明適用這兩個集合，無需其所有點 degree 四。
全 B-touch 給整側支援區間；其長度 λ_z,λ_w 至少二，且 λ_z+λ_w≤5。

若 t_r=3，spokes 避開 U_r 盾弧內點，而 U_r 支援至少三點。
三條 spokes 至多兩條在該弧兩端，因此整側至少碰四點，λ_r≥3。
不能兩側都三 spokes；若有三-spoke 側，其 unary 盾弧恰二、整側盾弧恰三。
該側三 spokes 是 unary 弧兩端加另一整側端點，必是非連續三點集。
與 §3 的通用 L1 欄位相交後：941 只可能原 `S_r=013`；933／940／932 的 no-mixed
roots 均 t_r≤2。941 的三-spoke 側 actual U 支援只可能 123 或 034。
這裡保留原框位置，沒有用 D₅ 把固定三列任意旋轉。

對完整 R_U 及原所有 contacts，令
`F_U(β)=⋂_(tuple∈R_U(β)) set(tuple)`，
`E_r(β)=[4]−β(S_r)−F_(U_r)(β)`。
精確接合是 `(E_z×E_w)−Δ`；G−zw 的接合是 `E_z×E_w`。
非空對角乘積拒絕原 G 時必 `E_z=E_w={c}`；不把 c 預填成未用色。
原刪 root 至多一個單拒絕例外，不能假設兩刪 root 圖均 Ω。

**no-mixed 殘留：** 941 保留上述可能一側三-spoke，以及兩側≤2 spokes；
933／940／932 僅兩側≤2。每側單一原 U 的容量、actual support／盾弧、完整 R_U、
E_r 及所有刪邊 witnesses 均需共同保存。尚未证明这些跨列条件无来源。
歷史 no-mixed 的單 q-minimal 禁色預算，沒有直接套到這裡的 Σ-critical G。

## 5. E6-E／F：G2、G3 的長 unary 與 endpoint 引理

**E6-E（使用三列）：G2／G3 的 sole b-unary 盾弧必恰二。**
E5 L3–L4 使 a 三-spoke 集是 §3 最右欄的連續三點集。
H−a=b+C+U 連通；整份落在 a-star 的同一個面。
三個框 gaps 長度為 1、1、3。假設 |σ_U|≥3，該面必是三邊 gap，
且 U 的 actual 盾弧佔滿它；大於三亦不可能。
b 的原 spokes 與整份 C 支援只能在 gap 兩端；兩端不相鄰，C 的支援連續性迫至多單點。

取所選三列中使 gap 端點同色 c 的一列。a 有兩合法色，b 的 spokes 都見 c，
所以 b 先有三合法色。完整 U 關係的共同避色容量至多一（G2）或二（G3），
故仍有合法 b 色，且可選不同的 a 色。兩 roots 均避開 c。
三個原 hubs `{a},{b},B` 連通互斥、兩兩相鄰，在 N(C) 上分別只見 a 色、b 色、c。
若 C 無框附件則只用兩 root hubs。hub 原則使完整原 C 可接回，故 G 接受該指定列，矛盾。
所以長 unary 整型排除，精確保留 |σ_U|=2，不先借省略圖全收。

**E6-F（不讀三列）：三點 unary 支援的 endpoint 色不能被禁止。**
令 `S_U={h₀,h₁,h₂}` 是實際三點連續框弧，owner r，固定任意 proper β。
反設 d=β(h₀)∈F_U(β)，即固定 r=d 時原 U 不可接回，degree lists 處處 tight。
H−U 連通，full B-touch 使其有支援外的原附件。
若 β(h₂)≠d，取原 bags
`Z=(H−U)∪(B−{h₁,h₂})`、`{h₁}`、`{h₂}`。
Z 由上述原附件連通；三袋由框邊兩兩相鄰，且在 N(U) 上見三個互異色。
若 β(h₂)=d，改用 `Z=(H−U)∪(B−{h₁})`、`{h₁}`，得到兩個相鄰異色 bags。
同色 owner／端點合袋前，tightness 已禁止同一 U 點在同袋有兩個外鄰，故 degree 與 lists 保持。
此處是 pin-only 的局部 list/minor 推廣：不假設 r=d 能延拓成原 G−U 的合法外染色（owner 的 spoke 可能禁止此色）。
上述 bags 只在 N(U) 上需要同色；收縮後可合法染為兩／三個不同色，U 的 lists 與完整 degree 四保持，
所以是在這個原圖 minor 上使用既有 hub 原則。二／三-hub 原則給矛盾。另一端點對稱。
因此 **`F_U(β)∩{β(h₀),β(h₂)}=∅`**，使用完整 tuple 避色而非 contact marginals。

G3 刪 a 的同色 endpoint spoke 後，K=C+a 的完整雙接點避色集合满足 `F_K⊆L`，
其中 L 是 a 剩餘兩色。這是 marked-leaf slack 接回；不宣稱 F_K=L。
U 盾弧恰二，在三邊 gap 的一個二邊子弧上；其一端色是共同 gap 端點色 c。
F_K 與 F_U 都不含 c，所以拒絕迫 b-spoke 見 c。
此時 b 的合法域為 L 加 a-middle 色 r；r 必由 U 阻擋，E6-F 迫 r 為 U 支援內點色。
得到整型必要來源表：

| S_a | 原指定 query | actual S_U | 唯一 b-spoke 的原框位置 |
| --- | --- | --- | --- |
| 012 | q₃=01021 | 034 | 0 或 2 |
| 123 | q₀=01212 | 034 | 1 或 3 |
| 014 | q₃=01021 | 123 | 1 或 4 |
| 034 | q₁=01202 | 123 | 0 或 3 |

941 保留四列；933 只保留前兩列；940 只保留後兩列；932 已由 E5 排除。
剩餘仍是完整 C11 反像／雙接點 U schemas、actual 原支援與同框 joint，未計入舊 116/256→32/64 ledger。

## 6. E6-G：G4 排除全部二邊 unary

E5 L6 給每個原拒絕列的真實 identity `R_U(β;u)=P_N(β)={d_β}`，且 d_β∈A_a(β)。
兩 a-spoke 省略 Ω 迫 S_a 為實際框邊；E5 L7 已排 equal pairs。

假設 U 盾弧恰二，actual support 為 h₀h₁h₂。
每個非框 pair（包含 h₀,h₂）在某個所選 q 重色。
在此 q，支援只見兩色，交換兩個未見色的穩定子保持整份原 U、全部 actual 附件；
singleton relation 必固定，故 d_q 是已見色。E6-F 又禁止 endpoint 色，所以 d_q=β_q(h₁)≠3。

每個所選 q 下固定 owner=d_q，U 都有真實拒絕 tight degree lists。
同一原 U 只有 contact u；全部非 contact 的 lists 始終含未用色 D=3。
[單接點固定色引理 §2](../../docs/c5_single_spoke_root_conservation.md#2-單接點固定色引理)
的同一原 block-tree 歸納，迫 contact 的 D-membership 在這三份實際拒絕 assignments 相同。
所以全部 d_q≠3。再用 E6-F，三色列的 singleton 只能是其 actual 支援內點色。

盾弧內點 h₁ 不屬 S_a；S_a 是框邊，至少一個端點與 h₁ 不相鄰。
該 pair 在某個所選 q 重色，遂使 d_q=β_q(h₁) 是 a 原 spoke 禁色，與 d_q∈A_a 矛盾。
因此 **G4 的 |σ_U|=2 四分支全排**。這是任意大小原關係／palette 論證，不是對舊 frames 刪表。

保留 unequal pairs 時，裸骨架 B、a,b、ab 與四 spokes 的每個 a-incident face 都只碰 B 的真子集：
S_a 是框邊，它的短三角面不能含 b（Sb≠Sa 至少有一個其他框接點）；
b 位於另一長面，ab 與 b 向該長框弧的原 spoke 把它分成真子弧。
整份連通 U 經 au 位於一個 a-incident face，所以 S_U≠B。
由支援區間論證，盾弧長四或五都會要求 S_U=B，因此亦排除。
**這裡沒有把 σ=B 代入只適用 σ≠B 的「避內點」限制。**

G4 精確殘留為 actual `σ_U=h₀h₁h₂h₃`，長三；其內點 h₁,h₂ 不可有原 root spokes。
可用原框點只有 `{h₀,h₃,h₄}`，S_a 是其中一條框邊 `{h₀,h₄}` 或 `{h₃,h₄}`；
S_b 不同，故是另一條框邊或非框 pair `{h₀,h₃}`。
h₀…h₄ 保持原有序 cyclic frame，每個实际位置仍單獨具名。
未知仍是完整 `R_C(x,y₀,y₁)`、全部 lifts／共同 root fibres 与跨列来源排除。
原 01/23、01/12 的已证局部出口沿用，不把它们当作任意 D₅ 的新 coverage。

## 7. E6-H：G1 用 actual core 分組，不預填 Ω

**retaining spoke＋unit-unary (4,4) core。**
設 M 省略 a 的一條 spoke 與 b 的一份 unit U，且拒絕 q。
M 全四飽和，自身是該 q-core；retained C11 的兩 contacts 共用 x，構成原 abx triangle。
全四分類使每個 root 至多另留一份 unit unary（不得另有共享 root 的 cycle／非 cycle 分叉）。
記其數 u_a,u_b∈{0,1}。原 unary 數 `1+u_a+u_b≤2`，原 spokes `(3−u_a,2−u_b)`。

- (0,0)：G2 mixed11＋sole b-unitU；只保留 |σ_U|=2，932 已排。
- (0,1)：原 (3,1) mixed11＋兩份 b-unitU，已由 E3 三份原 piece 的六邊預算排除。
- (1,0)：J4 mixed11＋各側 unitU，屬本任務範圍外。
- (1,1)：三份 unary，與共同預算矛盾。

故 G1 此入口只剩 G2 的二邊 unary 或 J4，無需舊 exact-target predecessor 全收。
J4 中此 retained core 共用 x，加兩 unary 迫 C 短，E3 共用-contact 引理化到其指定 K′ 輸入；
這是入口轉交，沒有執行 K′，也沒有排除 J4。

**只省略唯一 mixed11 的 (4,4) core。**
若 M=G−C 拒絕 q，all-four 分類的原 H_M 是 path／帶 path-arms 的 single triangle／直接橋接兩 triangle。
ab 是 bridge。令 k_r 為該側所有原 unary incidences；
`deg_HM(r)=1+k_r≤3`，故 k_r≤2，`t_r=3−k_r≥1`。
k_r=2 必在原 triangle 上，兩 contacts 相鄰且同屬一份 binary-U；
兩份獨立 unitU 會造成分類禁止的非 cycle 分叉。
至 root 交換，精確分組是：

| (k_z,k_w) | 原 spokes | 原來源分組 |
| --- | --- | --- |
| (0,0) | (3,3) | J6：六 spokes、C11、無 unary |
| (1,0) | (2,3) | G2：一份 unitU |
| (2,0) | (1,3) | G3：一份 binary-U |
| (1,1) | (2,2) | J4：各側 unitU |
| (1,2) | (2,1) | J6：unitU＋binary-U |
| (2,2) | (1,1) | J6：各側 binary-U |

這只是**存在 rejecting predecessor 時**的來源分組，沒有斷言所有原 M 拒絕，亦沒有 Σ(M)=Ω。
L1／全四分類只給 M 為 Ω 或只缺一列；若只缺一列，需保存其完整 witness，不能套舊十列全收 filter。

## 8. 項目 × 四分支狀態表與停止點

「排」是任意大小整型來源排除；「限」表示已有必要限制仍保留完整原圖族。

| 項目 | 941 | 933 | 940 | 932 |
| --- | --- | --- | --- | --- |
| 相鄰 m≥3，J6 全部 core 型 | 排，E6-A | 排 | 排 | 排 |
| J6 m=2 | 限：兩 mixed；44 僅 mixed11 omission；zw 非 theta 外界路 | 同左 | 同左 | 同左 |
| J6 no-mixed | 限：兩 U；三-spoke 僅013，或雙側≤2 | 限：雙側≤2 spokes | 同左 | 同左 |
| J6 少 spokes／原55 core | 限：§3 原 unit/core/盾弧/joint | 同左 | 同左 | 同左 |
| G1 retaining spoke＋unary | G2 二邊 U 或 J4 | 同左 | 同左 | 只餘 J4 入口 |
| G1 只省略 mixed11 | §7 的 J2／J3／J4／J6 原族；Ω 未證 | 同左 | 同左 | J2/J3 已排；J4/J6 保留 |
| G2 mixed11＋unitU | 限：U 盾弧恰二，S_a=012/014/034/123 | 限：012/123 | 限：014/034 | 排，E5 |
| G3 binary-U coverage | 限：§5 四份 literal 支援約束 | 限：§5 前兩份 | 限：§5 後兩份 | 排，E5 |
| G4 A unequal frames | 限：U 盾弧恰三，§6 原 spokes 限制 | 同左 | 同左 | 同左 |
| J4／K′ | 範圍外；G1 明確轉交其共用 x 入口 | 同左 | 同左 | 同左 |

附帶涵蓋 J4 的只是通用 L1、spoke 冗餘、原盾弧預算，以及每份二邊 U 的 endpoint 禁色限制。
不宣告其舊 47/75 ledger 的新三列 coverage，也不宣告 K′ 成立。
E5 已排的 J2 mixed12、J3 ternary、B mixed22 持續有效，沒有重開。

剩餘工作須保留同一原圖的 named contacts、literal shared vertex、ownership、actual attachments、
原 cyclic order／faces、全部原內邊、完整 tuples／lifts、root fibres（含空 fibres）與跨列刪邊 witness。
下一入口是 §3–§7 的這些原 joint 關係；需要逐 key 枚舉即依停止 (a) 記為缺口。
本輪沒有啟動逐 key 工作。沒有 candidate，也沒有停止 (b)/(c) 事件。

## 9. AD 正控制與證據界線

完整讀取 ES 的 `AD_k{3,6,7,9}_validate/crit_orbits/` 共 9 個代表：1＋2＋1＋5。
[controls checker](../../scripts/c5_excess_two_e6_controls.py)獨立求解 90 份整圖 D₅ 像，
重算十列完整 Σ、全部原非框刪邊 Σ／新列／全圖 witness、實際 degree／原 pieces／支援／rotation。
另把原 E1 935 完整具名圖與 ES 942 做原框及必要 root 交換的全圖對應；兩者都保留。
沒有控制滿足本題三列；所有未使用三列的新中間引理都核對其實際 antecedent。

主 checker 實際結果：0 controls excluded；2,050 個 maximal proper 刪邊，
藉拒絕集合向下單調覆蓋 6,742,364,070 個 proper edge-subsets（90 份有標號 D₅ 圖的計數，非獨立圖數）；
1,560 個 exact degree-valid 原子圖；230 份 actual piece 盾弧；
5,510 份真實 exterior refused component pins 的 tightness／Gallai；370 次 spoke 冗餘查詢。

L1 對所有 proper 子圖的驗證不是隨機抽樣：任一 proper edge-subset 均包含於某個已驗 G−e，
其 Q 是 Q_(G−e) 的子集；空／singleton／相鄰 pair 類對取子集封閉。
原 core 飽和的 degree-valid 檢查則在每份指定控制完整遍歷全取／全不取 pieces 與原 root 因子選擇。
沒有枚舉新來源 key。

控制全部 m=1：m≤2、支援非空、one-sided、原 incidence、盾弧與 Euler 預算實際成立；
N-empty 的空支援 antecedent、m≥3 四路、m=2 外界路、no-mixed 及 G2/G3 長 U 的 antecedent 為零。
它們沒有被控制排除，但這些不可能分支的反證前提沒有非空控制實例，不能稱其拓撲被正控制形式證明。
A／B／binary／ternary 原來源 antecedents 缺；E5 L3 的實際 J2 antecedent 為20。
[local controls checker](../../scripts/c5_excess_two_e6_local_controls.py) 與
[local_controls.json](local_controls.json) 實際核對 140 份原 U／D₅ 像的 1,400 個 endpoint queries；
340 份單接點 singleton refusal 的原 tight lists，及同一 U 的 260 對未用色 membership 比較。
另有 260 份 rejecting 全四原 q-cores，逐條原非框邊核對 q-critical 全圖 witnesses。
G1 spoke+unary 分組的實際 antecedent 為160（G2 40、附帶 J4 120）；
G1 mixed-only 分組的實際 antecedent 為10，只有 k=(0,0)，其 k=1／k=2 子步沒有非空控制。
其 (0,1) 兩 unitU 排除亦無合格 antecedent；紙面依賴與空前提清楚分開。
G3 的四份 literal queries 保留24份必要 palette 解，不稱來源實現；
G4 二邊 U 的15份 arc／Sa-edge 欄位 queries，守恆前8份 singleton schedules、守恆後0份。
這些是固定五框點／四色情況的完整必要算術，不是逐來源 key 或逐 frame 的幾何 ledger。

## 10. Exclusive-create、重播與實際 exit code

Python 固定使用 `/home/ray/developer/ai/math/.venv/bin/python`（3.14、NetworkX 3.5）。
每個 checker／正式產物只以 exclusive-create 新建；`--check` 只讀、逐 byte 重播。
自己的失敗草稿保留於 worktree 外後才重新 exclusive-create；沒有修改基準檔案。
所有 checker 都 serial，最多一個 worker；本任務總 worker 上限八。

| 實際命令 | exit code |
| --- | ---: |
| reductions 生成 | 0 |
| reductions --check | 0 |
| PYTHONHASHSEED=17 reductions --check | 0 |
| controls 最終生成 | 0 |
| controls --check | 0 |
| PYTHONHASHSEED=17 controls --check | 0 |
| local_controls 生成 | 0 |
| local_controls --check | 0 |
| PYTHONHASHSEED=17 local_controls --check | 0 |
| check_docs | 1：只出現下列兩個基準 missing paths |
| docgraph check | 0：62 documents、213 relations、5 families |
| git diff --check | 0 |

實際完整 stdout／exit codes／全部新檔 SHA 與 branch／HEAD／tracked diff 位於 `validation.json`。
初次 controls 草稿 exit1 是 ES 存檔 pretty-JSON hash 格式與 E5 compact hash 格式混淆；
修正本任務新草稿後上述正式檢查通過，不是前序數學判定錯誤。
初始較大控制產物的 `tools/artifacts.py record` exit1（不能推定 producer）；
本任務改用無損短欄位序列保存刪邊資料，最終 controls.json 為 982,689 bytes，local_controls.json 為 856,916 bytes，
各自低於 1,000,000 門檻，無需改 MANIFEST／.gitignore；基準工具原樣保留。

```text
missing path: docs/c5_open_leaf_ledger.md:78: ../audits/2026-10-04-task-d5/c4/scope_ledger.json
missing path: docs/history/2026-10-04-task-d2-integration-audit.md:39: ../../audits/2026-10-04-task-d2/integration_doc_changes.diff
```

`git diff --check` 對 untracked 檔不檢查內容，故 validation 另對所有新增文本執行 no-index whitespace 檢查。
no-index 與 /dev/null 比較新檔的 raw exit1 表示存在 diff；stdout／stderr 無任何 whitespace 診斷時記為 whitespace 通過，
不把此正常差異 exit1 寫成 tracked `git diff --check` 失敗。
不從 check_docs 的已知失敗宣稱通過；不重建無關 ignored 大產物以消除此兩條基準缺檔。

新引理清單：E6-A 四路／m≤2 及 m2 外界路；E6-B 原 incidence/core 分類介面；
E6-C 通用 L1 冗餘 spoke；E6-D no-mixed 整側幾何與分支限制；
E6-E G2/G3 長 unary 排除；E6-F endpoint 禁色；E6-G A 二邊 unary 排除／三邊殘留；
E6-H G1 actual predecessor 来源分组。
