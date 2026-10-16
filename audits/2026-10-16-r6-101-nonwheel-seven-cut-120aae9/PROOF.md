# R6-101-NONWHEEL-SEVEN-CUT：五個奇度內點與精確七埠介面

2026-10-16。研究 BASE `120aae90cab8bc4881916adc598cf344f2f20f4b`。
結果為 **B：任意大小必要條件與完整無界子類排除**。
幾何與匹配的獨立推導分別見 [GEOMETRY](GEOMETRY.md) 與
[MATCHING](MATCHING.md)，獨立審查見 [REVIEW](REVIEW.md)。

## 1. 同一來源與採用的結果

固定原全域最小、次級最大邊數的非目錄 no4ct C5 來源 G，
有序邊界 `(x,y,a,b,c)`，原 `d_G(x)=d_G(y)=d_G(b)=4`、`d_G(r)=6`。
所有圖、邊、rotation、完整染色 fibres（含空者）及全部 r lifts 保留。
使用同一合法 `J=U/(s=t)`、`m=[s=t]`、實際球面對偶 `D=J*`，
`e=(vw)*, f=(pq)*, g=(mz)*`；`X=V(e)∪V(g)`、`H=D-X-f`。
令 S 是 H 任意最大基數 Tutte 違反集。

採用已證結果：唯一非 singleton 奇分量 C 是 factor-critical，
`|δ_D(C)|=7`；f 連接兩個不同奇分量；
`q=|S|+2`、`E_D(S)=E_D(S,X)=∅`、`D[X]={e,g}`。
同一非空 `P111={M∈PM(D):e,f,g∈M}` 的**每個** M 皆滿足
`|M∩δ_D(C)|=1`，且兩個 f 端點均不在 S 或 X。

採用的來源幾何是：每個 J 三角形均為實際面；D 無一、二割，
三割皆為頂點星；所有 induced C4 必碰 m 或 z，並跨原 s/t 或 a/c
扇區。m 的原 sector 長度為 `d_G(s)-3,d_G(t)-3`，
`d_G(s),d_G(t)≥6`，`d_J(m)=d_G(s)+d_G(t)-5`。
其指定面是 `mvw,zpq,mzα,mzβ`。
詳細依賴入口與完整條件見 [GEOMETRY G1](GEOMETRY.md#g1-adopted-inputs-and-the-new-theorem)
及 [BASE](BASE.json)。本輪不增加外部定理。

## 2. 七割確實是一個 disk

因 f 在不同分量間，`H[C]=D[C]`。factor-critical 性排除內度一頂點：
刪除其唯一鄰點後它會孤立。C 亦無 bridge；若 bridge 分成奇、偶兩側，
刪除偶側端點後，奇側孤立且無 perfect matching。
在最大度三下，割點若分出兩個分量，每個分量須至少兩條連線，
否則有 bridge，將迫割點度至少四。因此 C 二連通。

先不能假定 δ(C) 是 bond。若 D-C 不連通，各分量割至少三，總和七，
故只能是三割與四割。三割一側是 singleton t，三個鄰點全在 C。
t 不在 X，否則其 forced mate 在 X；亦不在另一 H-S 分量，
因分量間至多只有 f 一條邊。因此 `t∈S`。

填入此面，`A=C∪{t}` 與其補集均連通，割為四。其實際邊界是簡單 Q4。
兩側各至少四面：A 至少四面，補側包含 X 四面。
若 Q4 有弦，來源 facial triangle 性會使一側僅有兩面，矛盾；故 Q4 induced。
A 完全避開 X。若 Q4 避開兩 hub，違反來源 C4 定理；若同時包含兩 hub，
mz 必是邊界邊，但其兩面均在 X，矛盾。
若只含 m，A 的面區間避開 mvw 與兩個 mz 面，兩射線在同一原扇區，
違反 C4 必跨扇區。
若只含 z，兩射線必跨 a/c fan；避開 mz 兩面的 A 區間必包含 zpq。
t 在 S 且非 f 端點，故 zpq 在 C。另一 f 端點不在 A，
所以 pq 在 Q4；這使 z,p,q 三角形位於 induced C4，矛盾。

因此 D-C 連通，δ(C) 是 bond；其 primal image 為簡單七圈 Q，
C 恰為其一側全部三角面，形成實際封閉 disk R。
若 Q 的弦位於 R，該弦分開兩個非空面區，其 dual edge 為 C 的 bridge。
故**所有弦只能在盤外**；沒有宣稱 Q 無弦。
每個 C 面至多接一條 Q 邊，因其內度至少二，故七條割邊有七個不同內端點。

設 `T0={m,z,v,w,p,q}`。其頂點皆不可能嚴格在 R 內：
m,z,v,w 會把 forced face 放入 C；p,q 會把 f 兩端同放 C。
每個內點完整 J 度至少五。對 Q 頂點 u 設 t_u 為其嚴格內部鄰點數，
則盤內度恰為 `2+t_u`，且 `t_u≥1`。設內點數 i，Euler 給出

`|C|=2i+5`。                                                (1)

## 3. 局部奇度的精確全域曲率

給 S∪X 面 bit 0，所有 H-S 分量 bit 1。完整 monochromatic primal 邊集是

`{vw,pq,mz} ∪ {R 的所有非邊界邊}`。                         (2)

這是 cut budget 與 f 實際位置的結果。沒有增加 S 內邊或 S-X 邊。
令 o_u 為完整 J 度的奇偶，奇偶相容最小度依次為

| 頂點 | 最小度 |
| --- | --- |
| m | `8-o_m` |
| z | `6+o_z` |
| v,w,p,q | `4+o_u` |
| 其餘 | `6-o_u` |

令 Δ 為完整 J 各點實際度減去表中最小度的總和。
各項皆為非負偶數。已採用的 Euler 恆等式為

`12=Qcharge-Δ`，
`Qcharge=6+o_m-o_z-Σ_{v,w,p,q}o_u+Σ_{u∉T0}o_u`。             (3)

令 I 為 R 嚴格內點中完整度為奇數的個數，B 為七個 Q 頂點中 t_u 奇數的個數；
`ε=1` 當且僅當 `m∈Q` 且 t_m 奇數，否則為零。
只有三條 marked 邊時，T0 恰全奇，`Qcharge=2`。
面 bit 轉換在完整 link 上有偶數次，故完整度 parity 等於 monochromatic
邊 incidence parity。(2) 的非邊界邊 incidence，在內點為完整度，
在 Q 上為 t_u，其餘為零。每次奇 incidence flip 增加 charge 一，
唯 m 的 flip 減少一。故精確地

`Qcharge=2+I+B-2ε`，`Δ=I+B-2ε-10`。                         (4)

## 4. 原 m 扇區另強迫兩個曲率單位

R 在 m 的面（若存在）為一個區間，避開 X 中的 mvw 及兩個 mz 面，
故只能位於一個原 s/t 扇區，長度是 `t_m+1`。
其他 bit 1 blocks 全為 singleton。扇區內無連續 00（budget 為零），
亦無其他連續 11：在 m 的 shared edge 不可能是 pq，故只有同一 C 的面
才會連成 11。兩端的指定面皆為 0。

對有 k 個 singleton blocks 的原扇區 u∈{s,t}，實際面字串給出

`d_G(u)-3=2k`，若無 C block；
`d_G(u)-3=2k+t_m+2`，若有 C block。                         (5)

若 ε=0，兩個原度均為奇數，且至少七，故 `d_J(m)≥9`。
m 的 parity 為奇，最小度七，單 m 的 excess 已至少二。
若 ε=1，只需 Δ≥0。因此

`Δ≥2(1-ε)`。                                               (6)

合併 (4)、(6) 即得**任意大小**必要條件

`I+B≥12`，故 `I≥5`、`i≥5`、`|C|≥15`。                      (7)

這排除了所有 I≤4 的來源障礙；其偶度內點數可任意多。
推導沒有使用小階枚舉，也沒有進行來源替換或下降。

## 5. 全匹配 lifts 的有限介面

在同一 Q 的實際 cyclic order 上依序標七條割邊 `b_j=u_jv_j`。
對每個 selected ports 集 A，保存**完整** `F_A=PM(C-{u_j:j∈A})`。
偶數 |A| fibres 為空，七個 singleton fibres 皆非空。
外側 fibre E_A 保存 `PM((D-C)-{v_j:j∈A})` 的每個完整匹配，
連同 selected cut edges `{b_j:j∈A}`，依全部 required／forbidden marks 篩選；
若 selected v_j 重合則 E_A 為空。外部始終是同一實際 D-C，
只有所選割邊已匹配的端點按式刪除。限制與取 union 給出字面 bijection

`PM(D;marks)=⊔_A F_A×E_A`；`P111=⊔_j F_{ {j} }×E_{ {j} }`。  (8)

因此任何固定外側 witness 支持 j 時，F_{ {j} } 的每個內匹配均以該 witness
接成同一 P111 成員。若 f 跨 C，只有其實際 port 可被 P111 選取。

對內匹配 N，C-N 是 cycles 加上 paths，後者配對所有未選的 ports。
在實際 disk 中 paths 互不相交，故配對 noncrossing。記錄 selected A、配對 π、
各 path 長度 parity 向量 α，及「有奇內 cycle」bit η；每格仍保存全部 N、
完整 paths/cycles 及空 fibres。tight |A|=1 有七個選擇、五個六點
noncrossing 配對、八種 parity、兩種 η，完整 registry 共 560 格。

若 `r=(7-|A|)/2`，則 C-N 邊數為 `|C|-r`，故
`Σα+#odd internal cycles≡1-r (mod 2)`。
η=0 的 tight 格須 Σα 偶數，排除 140 個必空格，最多 **420 個有效簽名**。
全 ordinary registry 為 `2(7·5·8+35·2·4+21·2+1)=1206` 格，
其中 302 格必空，最多 904 個有效簽名；仍保留全部空格。

內外 complement paths 以未選 cut incidences 接合。外端點可以重合，
此時相鄰 cut incidences 間保留長度零的外側 path。
全域 complement 偶，當且僅當內外無奇內 cycle，且每個交替配對圈的
path parity xor 為零；每圈穿割次數為偶數，故 cut 邊不改此 parity。
每個偶圈保留另外兩色的所有交替指派；奇圈的完整 Tait fibre 為空。
此為完整 matching/Tait lifts 的相容性判準，不將普通 PM 存在性提升成偶補正值。
完整雙向證明及相同 P111 的 crossing-cut identities 見
[MATCHING M2–M5](MATCHING.md#m2-full-singleton-fibres-and-one-unchanged-exterior)。

## 6. 精確停止點

剩餘是至少十五個對偶頂點、至少五個奇度 primal 內點的七埠 disk，
內部無 T0、邊界弦全在外側，且須以同一原外部滿足 (4)–(8)、
所有原扇區、小 C4/C5 定理與全部來源 fibres。其內部大小沒有上界。
420 是 matching 相容性簽名上界；不是來源圖目錄，也不是已證合法替換。
證明此同來源介面不可實現，或構造保全原 fibres 的合法下降，仍 OPEN。

本輪沒有證明 101 普通 PM 存在性、101 偶補正值、`W110+W101>0`、
完整319排除或一般 `K∞=K≤5`。既有 `K≤22=K≤5`、固定 r6 的 `k≥25`
及 completed-source 接回成本 `k+5` 均不變。
有限 checker 的 synthetic patches 不是符合來源契約的實例；紙面任意大小證明、
有限證書與既有 Lean build 的身份分開。沒有新增 Lean theorem。
