# 原Q的近接點弦排除、s=0完整annulus排除及兩個深點

2026-10-23；BASE `cb8f8593e273a7426ecadd59797a6e643cc4768e`。
固定[SOURCE_CONTRACT](../SOURCE_CONTRACT.md)的同一全域最小no4ct、完整Σ932、
h=4來源，全部二十份原collar。不是在932內另取最小圖。

**新結論：single contacts總數s≥1，原Q嚴格內部至少兩個深點；任何真Q弦
的兩端，其全部原C contacts間最小距離至少3。** 零pair且s≥1的一般來源
仍OPEN，共同k≥23不變；Q仍可能有弦。

## 1. 固定原圖與原Q

第四輪已排原C9的全部距四接點。寫原C為`(c0,...,c8)`，九條原邊的面第三
點為t_i；它們互異，完整C contacts恰為`{c_i,c_(i+1)}`。其他接C的原內點
只接一個C點。將只接c_i的點按其同一原內側rotation依序寫為
`z_(i,1),...,z_(i,s_i)`，令` s=Σs_i`。它們與t_i沒有alias。

原C全部內鄰點形成簡單原圈

`Q=(t0,z_(1,1),...,t1,...,t8,z_(0,1),...)`，長9+s。

原J=H−C是以Q為外框的三角disk；不接C的原點恰為Q嚴格內點，以下稱深點，
數目d。Q不先當induced。原完整度數給

`d_J(t_i)≥3，d_J(z_(i,j))≥4，深點degree≥5`。           (1)

原`k=18+s+d`，第四輪已知d≥1。原有界C3／C4 cap空，原C5 cap空或恰W5，
都是同一全域來源的small-cap前提；它們只適用原cycle的指定內側，不是一般
C4代表定理。原C無弦，無原內點有三個C contacts。

## 2. 任何真Q弦的兩端原C接點都距離至少3

令xy是J中一條**非Q邊**的原Q弦。從x、y的非空完整C contact sets各選
c_i、c_j，使原C圓周距離δ最小。δ≤2時如下。

若δ=0，原C3 `c_i-x-y-c_i`有界側在C內。原C3 cap空，因此x、y在c_i的
原內側link必相鄰；否則這個原三角形會嚴格含中間link頂點。它們因而在
該段Q上相鄰，xy其實是原Q邊，與弦假設矛盾。這保留了「同owner可以有
原Q邊」的例外，沒有把相鄰點的原面誤排。

若δ=1，原C4 `c_i-c_j-y-x-c_i`的有界側在C內。原邊c_i c_j的原內側面
第三點t恰在這個cap；因最小距離為1，x、y不共享任何C contact，故t不可能
等於x或y，亦不可能是另一C點。因此t嚴格在cap內，撞原C4 cap空。

若δ=2，取短原弧`c_i-c_h-c_j`，構成原C5

`c_i-c_h-c_j-y-x-c_i`。

五條可能對角線中，c_i c_j是禁止的C弦；其餘四條會使某端點多接另一端
或中間C點，將contact sets的最小距離降為0或1，均不存在。空C5不能在沒有
任何可用對角線下三角剖分。若cap為W5，其原中心同時接c_i、c_h、c_j三個
原C點，與第二輪無三接點定理矛盾。

這些cycle的邊都在原C閉disk內，其有界開部不含B或其他原C點；沿原C邊的
H內側三角面位於該有界側。故所用small-cap的側別與原來源合同相符。得到

`xy為真Q弦 ⇒ min{dist_C(a,b):a∈N_C(x),b∈N_C(y)}≥3`。 (2)

固定有限certificate只核18種原contact types（九T類、九single-owner Z類）
全部162種端點類型pair，包括同owner的兩個不同single點；54種通過(2)的
必要測試。這不是54張可實現來源圖，也沒有假設single點數有界。

## 3. 每條Q弦的兩側各有深點

任一真原Q弦xy與任一Q弧形成一個原cell。反設其中一側沒有深點，該側就
是沒有嚴格內點的多邊形三角剖分。其弦端點x、y在此polygon上相鄰，所以
至少有一個不是x、y的耳點：三角形時取第三點；至少四邊時用兩個不相鄰耳。

這個耳點位於Q弧開部，它在J的完整內側sector都在該cell，不能有跨xy或
越過外框Q的原邊。因此它的**完整J-degree**為2，違反(1)。故

`每條真Q弦的兩個原cell都至少一個深點`。                (3)

特別地，若d=1，Q必induced。J此時只有一個深點且沒有Q弦，每條Q邊的原
內側三角面第三點只能是同一深點，所以J恰為Q-wheel，全部Q點的J-degree為3。
由(1)可知沒有single點，即

`d=1 ⇒ s=0`。                                         (4)

下面用完整同源關係排s=0，再由(4)推出d≥2；不是先把一般Q當induced。

## 4. 任意s的完整原annulus與可變single contacts

對任一固定s向量與同一原Q，原C–Q annulus是九個原C邊面，加九個原c_i
link扇區。固定一份完整literal proper Q word σ。令

`L_i=(t_(i−1),z_(i,1),...,z_(i,s_i),t_i)`，

`P_i(σ)={0,1,2,3}\{σ(v):v∈L_i}`。

此annulus的全部full lifts恰為原C9的literal colors `a_i∈P_i(σ)`，且
`a_i≠a_(i+1)`。每一份完整tuple按**原有序C+Q**保存；空fibres亦保留。
若D_i是allowed colors P_i的4×4對角矩陣，K的entries為`K_ab=1[a≠b]`，
其總full-lift數精確為

`T(σ)=tr(D_0 K D_1 K ... D_8 K)`。                      (5)

這只是同一原annulus的有限colors求和，不代換原J、不刪single點，也不是
可變大小來源的充分表示。原H的完整集合接合為

`F_H(c) ≅ ⨆_(literal proper σ on Q) F_annulus(c,σ) × F_J(σ)`。(6)

共同原Q頂點的literal colors完全相同，原annulus包含C的全部鄰點，沒有
未知跨cell attachments；反向聯集是同一原H full lift。無新點、新邊或
completion成本。所有S4搬運均作用整份C+Q tuple，沒有分別正規化兩側。

一般s>0時，proper Q word可能有T(σ)=0。例：s_0=1、其餘0，Q10按原順序
交替用0、1；全部P_i={2,3}，奇C9無法二染，故T=0。這種Q word**不能**
只因annulus無lift便從原J支持刪掉；J或可染它，卻不延伸到H。此點明確
阻止把下一節s=0論證不加前提地移植到一般s。

## 5. s=0的完整C9–Q9矩陣及全lift必要拉回

現在只假設s=0。原Q為`(t0,...,t8)`，仍可有弦；原J與所有未知深點、弦、
rotation都保留。原annulus恰有18份有向三角面：

`(c_i,c_(i+1),t_i)`及`(c_i,t_i,t_(i−1))`。

對Q的全部820份canonical proper rows逐份固定literal代表，完整列舉C的
全部colorings，按**整條C**一次S4編碼分入820份C rows。此矩陣完整672400
fibres，其中661743空、10657非空，共10798份完整18點full lifts。每份Q row
都有至少一份C lift；這項非空前提逐820列獨立核，不因一般s的想像而補入。

固定一個原collar，令S_C為繼承的同一原H必要C-row支持（352／356／376列）。
若某Q row p在同一原J真正正，取其一份full J coloring；由(6)，**每份**
annulus C lift都接成原H full coloring。因此所有輸出的C rows必在S_C。
所以真正J支持包含於

`S_Q={p : 該p的全部annulus C-row輸出都在S_C}`。          (7)

這是universal all-lift拉回。只找到一份good C lift不夠，漏掉一份bad C lift
會把(7)改成錯的存在量詞。若某Q row無C lift，本應在(7)中**真空地保留**；
本s=0矩陣恰零份這種row，仍由checker明確確認。

對二十份原collar逐份使用(7)，Q初始支持為：五份大小6、十份大小13、五份
大小18。原Σ932非空，故原J可染，其真正Q支持非空。

對同一J一份正row的每個互補palette split，實際完整分量partition提供一份
完整noncrossing boundary orbit。全部子集分量交換仍為同一J的full colorings，
所以整個orbit都正。若某split的**每份**可能完整orbit皆碰到S_Q外的row，
該row才可刪。未知Q弦可進一步限制實際partition，但使用全部generic options
仍是sound必要上界；不要求Q induced。

完整證書對二十份原query各一個同步批次，將入場Q支持全部刪空，共250次
**帶s=0假設**的Q-row刪除。每批保留before、所有row及全部failed splits、
after；checker從4862份NC partitions重建49356份whole options逐份全orbit核。
真正J支持不可能被必要刪除刪空，故全部二十份原s=0假設逐一排除：

`s≥1`。                                               (8)

配合(4)得

`d≥2，k=18+s+d≥20+s`。                               (9)

這是single/deep結構及局部負擔界，不提高共同k≥23。原C9無條件支持沒有新
row deletion；剩下s≥1的一般零pair來源仍OPEN。

## 6. 獨立核對與保留Q弦的真disk反控制

producer從固定Q row出發列C lifts；獨立checker反向從全部canonical **C**
rows出發列Q lifts，對整份18點tuple作共同S4搬運到canonical Q，完整tuple
去重後重建全部672400 fibres，逐空／非空集合與10798 full tuples完全相等。
它不import producer，另重建所有whole options，按當時支持核二十批。
二十原collar的原名、attachments、rotation、有向面及完整case canonical
SHA逐份綁定；原B–C fibres與full lifts依凍結authority完整保留。

為防止把新結論誤寫為「Q induced」，另保存一張有向三角disk H：23點、
s_0=2、s_4=1，其餘0，Q長12、兩個深點，真Q弦恰

`t4-z0a，t4-z0b，z0b-z4`。

全部原C contacts精確符合九t／三single／兩deep；C-degree≥4，其他原點
degree≥5。checker核所有原邊兩側、完整links、Euler、全部contacts及Q弦；
原C3／C4 caps皆空，全部C5 caps空或W5。三條Q弦各側皆一個深點。因此
保留的局部degree/contact/cap前提與s≥1、d≥2、H有23點，仍不足推出Q induced。

這張圖沒有原B、完整Σ932或全域最小性，完整來源狀態是`not triggered`；
它僅作induced-Q過強推論的`counterexample`，不是原來源存在或來源排除。
可變single annulus另逐full tuple核兩個literal控制：(5)的s=1空band例，及
s=3／Q12的非空例（6份C lifts）。前者為`counterexample`護欄，後者
`triggered and holds`；均不提供完整來源。

16份immutable authority與六份routing入場快照分開凍結；normal／seed17、
13項語義反控制及drift結果見[VERIFICATION](../VERIFICATION.json)。新certificate
exclusive-create，沒有覆寫舊audit、shared docs、Lean或Git。

## 7. 精確停止點

已排s=0，且真Q弦只可連contact-distance≥3的原Q點；每條弦兩側皆深點，
實際來源至少一single、兩deep。一般s≥1、Q有弦／無弦兩支皆未排。
下一窄義務是在同一原Q上保留空band狀態，將(5)–(7)與完整J relation共同
推進，或用(2)的合法原弦cell提供可回填化約。不能把s固定0、把Q當induced，
也不能把空band row當來源不存在。一般932、h≥5、smaller bad、K∞及Lean
仍OPEN，共同k≥23不變。
