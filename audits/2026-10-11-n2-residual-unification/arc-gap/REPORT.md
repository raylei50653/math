# N2 原55的共同跨列缺口：獨立文件分析

2026-10-11。BASE / 核對 HEAD：`5f0979793c19e452dbb5fc7e9fe7e43cb8a991cc`。
只讀既有共享 docs / scripts / artifacts；本報告是本目錄的獨占新增文件。
沒有 source 搜尋、既有證書修改、commit、push、Lean theorem 或來源 closure。
原55、N2、E-ARC2 均保留 **OPEN**。

## 1. 採用的完整來源契約及現在真的已有的共同條件

令 T(G) 表示 `docs/c5_excess_two_arc_spoke_closure.md:24–39` 及
`docs/c5_excess_two_arc_size_bound.md:24–33` 的全部契約：指定有序 induced-C5 disk
外框 B；完整 Σ933 / 941 或整圖共同 D5 像；T4 全收；所有非框邊 Σ-critical；
有效 H 連通、full B-touch；ε=2；兩個非相鄰完整 degree5 roots r,s；
其他有效內點完整 degree4；H−{r,s} 恰兩份原 mixed P,Q，其餘 unary；
pieces one-sided、兩 mixed actual supports 非空。共同搬運後指定
q0=01212、q1=01202、q3=01021 拒絕。原 contacts、附件、owner、rotation、
bridges、空 fibres 及全部 lifts 始終保留。

在 T(G) 下，目前已有的共同必要條件為：

1. 對每個非框邊 e，Σ(G−e)=Ω；因而對每個拒絕列，有效原 G 自身是唯一
   minimal q-core，roots 保持55。這是比一般 Σ-critical 更強的每列 q-minimality。
   依據 `docs/c5_excess_two_arc_spoke_closure.md:219–227`。
2. 包括 roots 在內，每個內點至多接兩個相鄰框點；roots 原 H-degree 至少3。
   依據同文件 `229–233`。不能把兩條 spoke 的邊數當成兩份 piece 的盾弧收費。
3. H 有含 r,s 的中央二連通 block K0；其餘 blocks 只可能是直接在 r 或 s
   接 K0 的二連通 leaf block。每個 root 至多一個；unary 與其一一對應。
   因而 u≤2，u=2 時 owners 不同；H 無 bridge。
   依據 `docs/c5_excess_two_arc_size_bound.md:48–75`。
4. 每份原 C 是 K4-free、僅含 bridges / 奇環 blocks 的 cactus（或 singleton）；
   每份 C 至少兩條 root incidences；全 H 的 degree-two 點至多5。
   依據 `docs/c5_excess_two_arc_spoke_closure.md:122–131`，
   `docs/c5_excess_two_arc_size_bound.md:79–118,122–132`。
5. 保完整原分量及 root incidence，得到 |H|≤35−6u−3t。
   依據 `docs/c5_excess_two_arc_size_bound.md:173–194`。

它們是原圖的共同結構；不是存在性證書。原55的缺口已不再是
「每列選哪個45 / 54 / 55 core」，而是同一55圖的三列完整關係不能共同拒絕的證明。

## 2. 可單獨抽出的較弱共同引理：原55每欄只剩一單位

以下是現有採納輸入的直接紙面推論，可作共同接口；它不證 N2 排除。

固定同一原 G 及 i∈{0,1,3}。對 unary U 以完整原 contact tuples 定義
F_U(q_i) 為不能延拓到 U 的 owner root 色集，k_U 為原 root incidence。
對側 r 定義

\[
D_r^u(i)=\sum_{U\text{ at }r}(k_U-|F_U(q_i)|),\qquad
m_r=k_P^r+k_Q^r,
\]

\[
E_r(i)=\{0,1,2,3\}\setminus
\left(q_i(N_B(r))\cup\bigcup_{U\text{ at }r}F_U(q_i)\right).
\]

對原 mixed C 定義 A_C(i) 為同一完整 tuple 同時避開兩組 root pins 的接受關係。
固定 b∈E_s(i)，令 G_C^r(i,b)={a:(a,b)∉A_C(i)}，
V=G_P^r(i,b)∪G_Q^r(i,b)，並設

\[
\delta=\sum_{C=P,Q}(k_C^r-|G_C^r(i,b)|),\quad
o=\sum_{C=P,Q}|G_C^r(i,b)|-|V|,\quad
\lambda=|V\setminus E_r(i)|.
\]

**共同逐欄引理。** 在完整 T(G) 下，對每個指定 i、每個有序 root 選擇
r/s，以及每個 b∈E_s(i)，

\[
\boxed{O_r^u(i)=0,\quad |E_r(i)|=m_r-1+D_r^u(i),\quad
D_r^u(i)+\delta+o+\lambda=1.}
\]

全部項非負；D_r^u(i)∈{0,1}；沒有 unary 的一側 D_r^u(i)=0；
因 m_r≥2，E_r(i)、E_s(i) 均非空。

*證明。* 先用 degree4 slack 得 |F_U|≤k_U，以及每份 mixed 每欄
|G_C^r(i,b)|≤k_C^r。這正是 `docs/c5_phase_b_common_lemmas.md:233–239`
的完整 tuple 容量論證，不取 contact marginals。

每側至多一份 unary，來自中央 block 引理。同一 root 的原 spokes 至多兩條，
若有兩條，其框端點相鄰，故在每個 proper q_i 下顏色互異。
對原 spoke rb_j，取 G−rb_j 的同 q_i 完整染色（第1節條件1）。
r 必取 q_i(b_j)，否則該染色本來就可恢復 rb_j、染回 G。
原 U 全部仍在，故 q_i(b_j)∉F_U(q_i)。所以原 spokes 的 singleton factors
互不重疊，也與唯一可能的 unary factor 不重疊，O_r^u(i)=0。

原 degree5 計數 t_r+k_U+m_r=5，因此
|E_r(i)|=4−t_r−|F_U|=m_r−1+D_r^u(i)≥m_r−1≥1。
（無 U 時 k_U=|F_U|=0。）同理 E_s 非空。
q_i 拒絕給 E_r(i)⊆V；B-C2 取 χ=0、deg_G(r)=5 得
D_r^u+O_r^u+δ+o+λ=1。代 O=0 即得。∎

這是55與45降度侧的精確差別：45降度側的同式右端為0，
原55右端為1。不能將45 / 54的「五項皆零」搬到原55。
依據 `docs/c5_phase_b_common_lemmas.md:228–248,270–273`。

**量詞邊界。** 每個 i、b 可有不同完整 witnesses 及 block palettes。
此引理沒有給三列共同 pins，沒有給三列費用不重用，也沒有推出
∑_{i}D_r^u(i)≤1 或三列總費用必須由同一單位支付。
舊 Phase B 已明列這個升級缺口（`264–268,292–297`）。

## 3. 仍缺哪些結構橋梁

原完整 root joint 是

\[
J_G(q_i)=(E_r(i)\times E_s(i))\cap A_P(i)\cap A_Q(i).
\]

其每一接受 pair 必帶各份原 piece 的同框完整 lift。
依據 `artifacts/c5_excess_two_e4/REPORT.md:315–336`。
target contradiction 須證至少一個 i∈{0,1,3} 有 J_G(q_i)≠∅。
目前的拓撲、大小、每欄容量均沒有給出這份 joint witness。

| 原族（ℓ 為 long mixed 數） | 已有共同資訊 | 一個精確、仍未證的充分橋梁 |
| --- | --- | --- |
| ℓ=2,u=0 | E_r,E_s 含三色列的未用色3；兩 long 各有完整 A | 存在指定 i，使 (3,3) 同時在 A_P(i),A_Q(i)；或更一般一個原 joint pair。分別非空的 A 不足 |
| ℓ=1,u=0 | short 的所有 diagonal pins 可延拓；3∈E_r∩E_s | 存在指定 i，使 (3,3)∈A_long(i)；或與 short 同時接受的 off-diagonal pair |
| ℓ=1,u=1 | unary owner 唯一，完整 E 與兩 A 保留 | 存在 i 使 3∉F_U(q_i) 且 (3,3)∈A_long(i)，或直接證完整 J 非空。两件必在同一列成立 |
| ℓ=0,u=1 | 每個 short 全收 diagonal；每列拒絕迫 E_r∩E_s=∅ | 存在指定 i 使3∉F_U(q_i)；這立即讓兩root均取3。故殘留必要條件為三列均3∈F_U(q_i) |
| ℓ=0,u=2 | owners不同；每列拒絕迫 E_r∩E_s=∅ | 初稿缺口已被本輪新三hub引理排除，見§6；它不是仍存活的參數情形 |

表中最後欄是「如果獨立證成即可接回」的明確弱候選，不是新增已知前提，
也不宣稱一定是最好或最弱的證法。完整 J 非空可由其他 off-diagonal pair 實現，
所以3-diagonal條件只是充分條件。short diagonal 的精確輸入是
`artifacts/c5_excess_two_e4/REPORT.md:253–265`、
`docs/c5_phase_b_common_lemmas.md:115–131`。

跨列缺少的核心仍是：將同一原中央 block / leaf unary 的 palettes、
contact tuple fibres 與三份拒絕欄，連到一份不可重用的共同幾何或容量限制。
以下捷徑均不能供給它：

- **SD-A。** 其假設恰一完整 degree5，其餘4，且內圖二連通；
  結論該root內度2。原 G 有兩完整degree5，不能用。
  含 U 時整個 H 又可能有root割點；K0二連通不等於 H二連通。
  刪一條spoke後雖成45 / 54，現在每份 derivative 全收，故 SD-A 的拒絕前提不成立。
  需要另證雙缺額版，或給中央 block 可正確容納完整 unary 禁色的 list 定理；
  它不隨單缺額定理自動成立。
  精確 SD-A 见 `docs/c5_degree5_interfaces.md:264–284`，現行停止點见
  `docs/c5_excess_two_arc_spoke_closure.md:290–294`。
- **一般 B-S1 / 猜想 S。** 若獨立證成固定目標的每份 mixed 都 long，
  B-S0可排有unary的三份 pieces，但無unary、兩long仍需 joint。
  B-S1仍OPEN；S935反駁去掉固定目標 mask 的版本。
  见 `docs/c5_phase_b_common_lemmas.md:133–149`。
- **大小有限或個別relations非空。** |H|≤35 未給足以衝突的下界；
  一份較大 lower bound / 證到≤9 必須另有證明。既有 k≤9無反例
  尚不覆蓋10–35。见 `docs/c5_excess_two_arc_size_bound.md:248–252`。
  各列 pins 可不同，不能以每列存在一組 witness 改成存在一組 pins供所有列。

## 4. 三點弧命題的方向：能排目標，但不能充當未證結構前提

令 Γ(G) 為 E-ARC2 的一般完整來源前提及1≤|Q|≤4。其待證命題為

\[
\forall G\,[\Gamma(G)\land\varepsilon(G)=2
\Rightarrow Q(G)\text{ 包含於某連續三點弧}].
\]

原域五環集合算術表明，不能包含於三點弧等價於 Q含某個D5像的{0,1,3}。
因此一旦一般E-ARC2独立證成，當然排除 T(G)。但如果用未證E-ARC2
先推出「N2不存在」或用不存在的來源真空地推出某個缺條件，再宣稱
以該條件證E-ARC2，會循環。原55 gap本來就是该母目標的一個必要子域。
精確方向见 `docs/c5_research_synthesis.md:454–480,482–505`。

可合法分離的較弱目標是 **限制在完整非相鄰、恰兩mixed N2的三點弧定理**：
對一般Γ中的N2來源證 Arc(Q)，且證明不得引用一般E-ARC2、B-E或ε≥3。
它若獨立完成便排本N2原55域；反向仍不能推出一般E-ARC2，因N1、相鄰、
單-root例外等另保留。僅將「三點弧」改名為「完整J不能三列皆空」
也沒有自動減少证明義務：在固定target域，後者正是本N2排除要證的結論。

本報告第2節的逐欄引理是可用的較弱、非循環共同接口；第3節的diagonal
橋梁是可單獨研究的充分候選。它們既不假設母猜想成立，也尚不閉合N2。

## 5. 驗證及停止點

本輪是逐條文件契約及初等容量推導的獨立只讀檢查；沒有重新稽核上游
44 / N45 / SD-A全部採納，沒有搜尋來源圖，也沒有新finite target trigger。
既有 finite 控制在完整Σ933 / 941 target來源均0觸發，應保留
`not triggered`，不能把它改成新來源排除證據。
见 `docs/c5_excess_two_arc_pair_critical.md:166–180`、
`docs/c5_excess_two_arc_component_slack.md:191–205`、
`docs/c5_excess_two_arc_spoke_closure.md:244–252`、
`docs/c5_excess_two_arc_size_bound.md:202–217`。

新增只讀固定控制：`check_capacity.py` 使用既有63份原source記錄與全部
complete local pin fibres，按原edges、原coordinates另以numeric DFS核對
原整圖接受性與每條非框邊的同列刪邊接受性；不生成任何圖。
非相鄰、恰兩mixed、每側至多一unary的較弱結構條件觸發19圖，
全部19個拒絕三色列同q-minimal；38次有序root方向及74個逐欄等式
均 `triggered and holds`。完整target來源0個，`not triggered`。
未重驗原disk rotation或上游搜尋完整性；此控制只檢驗較弱條件下的容量接口。
產物為 `capacity_controls.json`，普通及seed17 `--check`可重播。
首輪spoke endpoint索引錯誤在產物寫出前exit1，留在 `failed_generation.txt`。

待整合者對第2節新共同引理獨立核對後，可採用其精確量詞。
原55及E-ARC2始終 **OPEN**；没有以共同必要條件取代尚缺的完整證明。

## 6. 後續獨立核對：三hub直接排singleton的有U或spoke情形

`structure/REPORT.md` 首稿的 u=2 五邊partition / h分支已完成獨立核對；
其再次D5標準化後不能默認literal q0仍拒絕的措辭問題已傳回父端。
下述新的共同引理不需任何D5標準化，取代該較繁路線。

**新共同來源引理。** 完整 T(G) 若有singleton-support mixed P，
則必 u=0、t=0。

*獨立核對。* 設 N_B(P)={h}，另一原mixed為Q，它連通、兩root contacts
正且actual boundary support非空。若有原U，交換root次序使owner為r，取

\[
R=\{r\}\cup U,\qquad S=\{s\}\cup Q,\qquad T=B.
\]

R由原U–r邊連通；S由原Q–s邊連通；B本來連通。
三bags互斥且不含P。R–S鄰接由原r–Q邊；R–T由U的實際框附件
（原盾弧定理已保U至少三點support）；S–T由Q非空實際框附件。
P為原 H−{r,s} 的完整分量，故其外鄰集恰 {r,s,h}，分别落於R,S,T。

若u=0但t>0，交換roots讓r有原spoke，改取R={r}，S,T同上。
R–T由該原spoke；其餘連通、鄰接、N(P)覆盖完全不變。

分量必留給G−P同一原拒絕q0的完整外部染色ψ，且它不能補回P。
ψ在各bag與N(P)的交集只有一個pin，必為常色；按pin色合併同色bags。
它們原本兩兩相鄰，故每份合併仍連通，剩餘bags仍互斥且兩兩相鄰，
N(P)各bag常色互異。P連通、原每點完整degree4，完全滿足原hub定理B
（`docs/c5_unary_shield_budget.md:155–179`），得K5 minor矛盾。
沒有要求整個R/S/T在ψ下同色；沒有重染任何外部頂點；沒有拼接不同列的witness。

因此若u=2，兩U各收至少2盾邊，兩mixed必short。
新引理排其singleton，非空short只剩真框邊pair，各再收1盾邊；
同一原五環上2+2+1+1=6>5，直接排完整目標N2的u=2子族。
此推導比初稿省去singleton k≥4、incidence分拆、框partition及h分支，
也同時收窄u=1各族的short支援必pair。

獨立判決：這份新共同引理及其u=2推論在完整契約下紙面成立，
可接入父端新報告；不是一般原55排除、不是完整N2 / E-ARC2 closure，
沒有新的finite target來源或Lean theorem。
