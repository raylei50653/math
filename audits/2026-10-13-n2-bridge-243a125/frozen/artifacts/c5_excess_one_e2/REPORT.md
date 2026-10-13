# 任務 E2：猜想 E 的 ε≤1 層

2026-10-04；基準 `ca3870f9b79684c2100480d0dc04523899666928`，
分支 `shield-budget-hub-principle`。本任務只新增報告、scripts 及 artifacts；
不修改導覽、STATUS、README、HANDOFF，不 commit、不 push。
工作區其他任務的既有及並行變更不屬本交付。

**獨立稽核（2026-10-04，D₇）**：[稽核報告](../../audits/2026-10-04-task-d7/REPORT.md)確認 (a)、(b) 的最終論證，另列一項產物缺口（舊 sidebranch 層的 one-pendant 說法），已修補，見 §9。

**結論：(a) 成立；(b) 成立，依賴下列紙面化約與固定有限末端證書。**
ε=0 的飽和推導已補完整；ε=1 的三點弧 Q（935）及不相鄰二點 Q（951）
均可排除。不是從有限構造沒有找到反例，推斷任意大小結論。
各分支的大小無關論證、有限必要域及依賴界線分別寫在 §4–5。
整合與現行排程仍由
[Kempe 導覽](../../docs/c5_kempe_guide.md#3-停止點與保留缺口) 維護。

## 1. 完整前提與證據層

G 為有限簡單圖，B=(b₀,…,b₄) 是指定有序 induced C₅，具有以 B 圍外面的
disk embedding，其餘頂點私有。Ω 是十個完整有序合法 boundary 列的共同
S₄ 色名置換軌道，T4 的索引為 {2,5,7,8,9}，mask 第 i 位是
`pattern_order[i]`；不先商掉 D₅ 框位置。G 接受全部 T4，且每條非框邊 e
滿足 Σ(G−e)⊋Σ(G)。Q 是拒絕的三色 singleton 位置集合。

沿用[容量報告](../../docs/c5_independent_support_capacity.md#1-兩種-minimality-與來源的基本結構)
的**有效內點**慣例：忽略孤立私有頂點，H 是其誘導圖，
ε=Σ_{v∈H}(deg_G(v)−4)。這是必需的定義校準：邊 minimality 不會刪除
孤立頂點；若把任意添加的孤立點也算進 ε，每個會貢獻 −4，低 ε 陳述便
不是同一命題。下文所有 degree 都包含實際框附件，並在所指原圖／core 自己計算。

| 證據層 | 本輪使用與界線 |
| --- | --- |
| 紙面證明 | §2–3 的前提推導與 ε=0 飽和；§4 的 935 任意大小化約；§5 的 951 全部分支化約、共同 palette／盾弧／terminal-block 排除 |
| 沿用的紙面＋有限末端證據 | 全 degree-4 分類、唯一 degree-5 相鄰列分離、原首點／接點保持的尾枝 transfer；沒有重跑其大模板枚舉 |
| 外部定理 | Gallai degree-list／blockwise-uniform 刻畫；用於拒絕 lists 的 block palettes，沒有當作 Python／Lean 成果 |
| Python 有限域證書 | 新 checkers 的具名必要表、完整 ordered relations、原圖 minor witnesses 及明定構造族；不是任意大小來源搜尋 |
| Lean | 沒有新增 theorem，沒有執行 `lake build`；本輪紙面拓撲與完整分類未 Lean 化 |

外部定理的精確版本是 Dvořák 講義
[List coloring and Gallai trees，Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)：
連通圖的 lists 至少等於各點 degree 而不可著色時，lists 處處 tight，
圖是 Gallai tree，lists 是各 block palettes 的不交聯集。本輪重新讀取此來源。
沒有使用四色定理作搜尋或實現性 oracle。

## 2. 一般 Σ-minimal 來源的前提推導

以下不假設 P 是獨立集，也不限定 mask=933／941。

**內點 degree≥4。** 選有效內點 v 的任一 incident 非框邊 e。
Σ-criticality 提供一個 G−e 可延拓、G 不可延拓的 boundary 列 q。
保留這份完整染色在 G−v 上；若 deg_G(v)≤3，四色中仍有一色避開 v 的
全部鄰色，可補回 v，矛盾。因此每個有效內點完整 degree≥4。

**未接框點引理。** 若一個接受 T4 的帶框子圖拒絕 singleton-i 列 q_i，
它的 actual support 必含 B∖{b_i}。否則，對未碰內部且不是 singleton 的
框點 v，將 q_i(v) 改成未用色 D，所得 proper 列恰用四色；延拓後只將 v
改回原色，便得到 q_i 的同圖完整染色。這是
[未接內點引理](../../docs/c5_unattached_boundary.md#1-不依賴-degree-或-disk-的改色引理)。
所以拒絕一列需至少四個框接點；拒絕兩個不同 singleton 列，G 必碰齊五框點。

**H 連通。** 對每個 H 分量 C，令 G_C 保留 B、C 及全部 C–B 附件。
在同一有序框與同一 literal color frame 中，Σ(G)=⋂_C Σ(G_C)。
每個 G_C 繼承 T4。若 Σ(G_C)=Ω，刪除它的任何非框邊仍接受 Ω，
全圖 Σ 就不變，違反 criticality。因此每份有效分量都拒絕某個三色列，
actual support 各至少四點。C₅ 上兩個四點支援總能各選一對交錯的端點：
先取第一支援的四點，第二支援至少含其中三點，而這三點含四點環序的
一組對角點，另一組交給第一支援。若有兩個分量，便有兩條內部不交的
原路徑連接交錯端點，與 disk 分離矛盾。因此 Q≠∅ 時 H 非空連通。
這裡取交集的是完整列，不是獨立正規化後的分量 masks。

**單列 core 的 degree 與連通性。** 對 q∉Σ(G)，在有限非框邊集合中
取 inclusion-minimal 拒絕 q 的子圖 M_q，保留 B、忽略孤立內點。
M_q 繼承 induced 框、disk 及 T4，但不繼承 Σ(G) 相等。
其每條非框邊 q-critical；用上面的刪 v 補色論證得到每個有效內點
deg_{M_q}≥4。其內部若不連通，只保留其中拒絕 q 的一個分量已足夠，
違反 minimality；故內部非空連通。不能把來源 Σ-criticality 與單列
q-criticality 混用。

若 Q=∅，(a) 的結論直接成立；而 Σ-criticality 其實使 G 沒有非框邊。
因此 ε=1 的來源不會有空 Q。

## 3. (a) ε=0 的完整飽和段落

反設 Q 非空，取任意 q∉Σ(G) 及上述 M_q。§2 已證 H 非空連通，
每個有效內點在 G 中 degree≥4；ε=0 因而使全部 degree 恰為四。
M_q 含至少一個有效內點 v，否則只有 induced 框 B，必可延拓 q。
對任何已在 M_q 中的有效內點 v，有
4≤deg_{M_q}(v)≤deg_G(v)=4，故它保留 G 中**全部** incident 邊。
特別地，每個原內鄰点也進入 M_q。沿同一原 H 的路徑傳播，所有有效
內點以及其全部內部／框附件邊均進入 M_q，所以 M_q=G（孤立點忽略）。

現在 G 自己是接受 T4、全部有效內點完整 degree=4 的 disk minimal
q-obstruction，符合
[全 degree-4 結論的完整前提](../../docs/c5_degree4_guide.md#1-完成的結論與完整前提)。
因此 Σ(G)=Ω∖{q}，Q 恰為一點。連同 Q=∅ 的情形，得到
**ε=0 ⇒ |Q|≤1**。此段沒有把「H 連通」或「degree≥4」當額外假設，
而是從來源 criticality、T4、disk 推出；也沒有假設 P 獨立。

### 3.1 ε=1 的共同 root 與省略身份

ε=1 時唯一 root r 的完整 degree=5，其餘有效內點 degree=4。
每個 M_q 都含 r：若不含 r，從任一 core 內點開始，degree-4 飽和保留
它在 H−r 所在原分量的全部原邊；該分量經原邊接到 r（H 連通），矛盾。
core 中 r 的 degree 只能為 4 或 5。若是 5，所有原分量、全部 spokes
沿飽和進入，M_q=G；若是 4，恰省略一条 r incidence。省略 spoke 時
所有原分量保留；省略分量時，因每個被保留 degree-4 點保留全部原邊，
只能整份省略一个單接點原分量。容量至少二的原分量不可部分省略。

對具名單容量因子 i，G∖i 若拒絕 q，自己就是全 degree-4 core，
故 Σ(G∖i)=Ω∖{q}。**不同拒絕列不能共用同一原省略身份。**
這是[四容量子覆蓋 §1](../../docs/c5_excess_one_subcovers.md#1-同源因子真子核心與省略區域)
的推廣，保留同一原圖與因子身份。

### 3.2 盾弧工具在新 masks 的適用範圍

當 |Q|≥2，§2 已給 H 連通、碰齊 B、degree≥4。因此
[盾弧引理 1、2 與定理 A](../../docs/c5_unary_shield_budget.md)
在本輪唯一 root 設定中的證明可逐步重用：每份 H−r 原分量是 unary、
one-sided；取其原接點邊的 critical witness 得非空禁色，再用避開該
分量的 r–B 原路徑及短支援引理，排除支援包含於一條框邊。
故每份原分量 actual support 是至少三個連續框點，盾弧長至少二；
同一原嵌入的盾弧邊互斥，總長≤5，所以原分量至多兩份。
這一重用不依賴 P 獨立；原報告的 (S) 中「Σ=933／941」在此僅透過
已補證的上述結構前提使用。

### 3.3 完整來源分支與較大 Q

本輪的雙列論證只假設兩個指定 singleton 列拒絕及全部 T4 接受，不要求
其餘三色列接受。因此它們也排除包含不相鄰二點的較大 Q；不是只判定
完整 mask 恰為 951 的來源。C₅ 上 |Q|≥3 必含不相鄰二點，故 §5 完成後，
ε=1 確只剩一點或相鄰兩點。§4 另獨立處理三點弧，供工具校準。

若每個所選拒絕列都以 G 自己為 minimal core，沿用的是一般
T4／minimal-q 來源分類，而非原 933／941 的特殊 core 身份表：

| root-spokes t | 全部容量分拆的處理 | 本輪需處理的剩餘 |
| --- | --- | --- |
| 0 | [no-spoke §4–5](../../docs/c5_no_spoke_exterior.md) 排除 (5)、(4,1)、(3,2)、(3,1,1)；(2,2,1)、(2,1,1,1) 違反 §3.2 的至多兩分量 | 無 |
| 1 | [(4)](../../docs/c5_single_spoke_four.md) 與 [(3,1)](../../docs/c5_single_spoke_three_one.md) 已作來源排除；(2,1,1) 違反 §3.2 | (2,2) |
| 2 | [(3) 的排除](../../docs/c5_two_spoke_three_contacts.md#5-second-rows-scope-and-remaining-cases)允許任意位置的兩條異色 spokes；(1,1,1) 不能讓三份分量各有 private colour | (2,1) |
| 3 | full minimal q 的 root 只有一個可用色，不可由兩份分量各承擔私有色 | (2) |

這些紙面來源排除只需 minimal-q、連通 H、指定 disk 框與完整 degrees；
不依賴 P 獨立。t≥4 與 T4 接受矛盾：可取一列 T4 令任選四個 spoke
端點四色互異，r 無可用色。若已有真子核心，§3.1 的飽和與原 degree-4
結構已把原分量容量限制為至多二、至多一份 binary，另在 §5.4 處理。
所有至少三份原分量的分拆（也包含 t=0 的 (1⁵)、t=1 的 (1⁴)）
都直接由 §3.2 排除；没有在表中省略一个可能来源。

## 4. 935：ε=1 的三點弧 Q 排除

每個三點弧中的位置都有拒絕的框鄰點。
[四容量子覆蓋 §2](../../docs/c5_excess_one_subcovers.md#2-只用-t4-的-minimal-degree-5-相鄰列分離)
已核對：接受 T4 的唯一 degree-5 minimal q_i-core 接受兩個相鄰
singleton 列。其來源分離引理不要求 P 獨立，不要求完整 Σ 恰缺兩列。
所以本題三個拒絕列都不能以 G 自己作 minimal core，必各有真子核心，
三份原省略身份互斥。

若所有因子容量一，
[跨列未用色守恆與五單容量論證](../../docs/c5_excess_one_subcovers.md#5-五個單容量因子不可能拒絕三個-singleton-列)
給 |Q|≤2，矛盾。這個推導使用同一原 unary 的 D／非 D 身份、三個不同
拒絕列及省略身份不重用，沒有使用 P 獨立。

取任一全 degree-4 真子核心。原 r 及任何 binary 分量的兩接點形成
該 core 的**原 triangle**；全 degree-4 結構迫每份原分量容量≤2，
至多一份容量二。因此恰一份 binary C₂，另三個容量一因子。
t=0 時省略任何 unary，r 仍在 triangle 上接兩條 bridges，違反原
degree-4 接枝限制；t=1 時可省略的只有兩份 unary（省略 spoke 仍有
兩 bridges），不足以供三個不同列；因此只剩 t=2 或 t=3。

t=2 的三個單容量因子是兩 spokes 與一 unary。至少一個拒絕列省略
spoke；t=3 的可省略身份全是 spokes。選其中一份 G−e，整圖共同
D₅ 搬運及 S₄ 換色將它的拒絕列對齊 q₄=01012；之後所有原座標、
attachments、components、rows 同時搬運，不獨立正規化各 relation。

原 r 在 G−e 的內部 degree 分別為三或二。沿用
[two-spoke 的原接點保持 transfer](../../docs/c5_941_two_spoke.md#3-從-bridge-保持提升到原接點保持)
與[three-spoke 的 binary joint 接回](../../docs/c5_941_three_spoke.md#3-保持同一-c₂-的有序-relation-後接回)：
任意長 path tails 可縮至既有 endpoint bases，保持每個 proper boundary
row 的原首點全部可取色；按原 parent 色接合，保持 ordered
(r,x,y,u) 或 (r,x,y) **共同 relation**。接回 e 僅過濾 r≠b(e)，
所以原完整 Σ 保持。这是任意大小涵蓋步驟；新 checker 沒有重新枚舉
任意大小圖，也沒有以 endpoint marginals 相乘代替原共同 relation。

[新 checker](../../scripts/c5_excess_one_e2_935.py) 只讀既有 t=2／3
封存表，獨立核對完整染色、原 tuples／full witnesses 及每次接回。
592 份 t=2 接回的 T4 全收結果只含一點或相鄰兩點 Q。
1,194 份 t=3 接回中，只有九份 T4 全收結果有三點弧 Q，全部來自無枝
triangle 必要模型，mask 分別 942、956、1012 各三份。

九份均為原 triangle rxy；x、y 共同接同一相鄰框點對 {a,b}，
r 恰接 B∖{a,b}。在**原圖**取 K₃,₃ 的 branch sets：
左側 {a},{b},{r}，右側 {x},{y},B∖{a,b}。
最後一袋是連通的三框點路徑；a、b 各接它的一個框端點，r 由原 spoke
接它；a、b、r 又各有原邊接 x、y。六袋互不相交，九份跨組鄰接全在
原圖，得到 K₃,₃ minor，與平面性矛盾。

因此 **ε=1 不會有三點弧 Q**。此結論是任意大小紙面化約、沿用的
分類／transfer 及新固定有限末端證書的合成；不把 1,786 份有限模型
本身稱為任意大小圖的枚舉。九份 relaxed 三點弧圖不是猜想 E 反例。

## 5. 951：完整分支排除

不相鄰二點 Q 的每個拒絕位置都沒有拒絕的框鄰點。
因此 §4 的「每列必有真子核心」不能使用；可能 G 自己同時是兩列的
minimal core。這正是 933／941 ε=1 證明無法直接推廣的步驟。
不能因為 951 已有 ε=2 代表，就假設 ε=1 不可實現。

### 5.1 唯一 binary、三-spoke、兩列皆以 G 為 core

將其中一列對齊 q=q₄=01012。沿用三-spoke 區域定位，原 spokes
只能為 {b₀,b₁,b₄}、C 在長 arc 1234，或其整圖反射。
若另一不相鄰列是 singleton-2，這三 spokes 有重色，不能是 minimal
該列的 G；故本支只須 p=q₁=01202（反射型共同搬運）。
兩列下 root 的唯一可用色均是 D=3；同一原二接點分量 C 拒絕 root=D。
在區域框 (r,b₁,b₂,b₃,b₄)，兩份 literal rows 為
δ=(3,1,0,1,2)、δ′=(3,1,2,0,2)。不各自重新命名顏色。

對每點 v∈C，固定外部 root=D 後的 lists 至少為 deg_C(v)，拒絕迫
處處 tight。Gallai 外部定理給兩份各自的 block palettes，但都在同一
原 C、同一 contacts 與 attachments 上。色 D 恰在非 contact 的 list 中。
δ 下 b₁,b₃ 同色；δ′ 下 b₂,b₄ 同色，所以任何 actual attachment 集
都不可包含 13 或 24。非 contact 的 private degree-two 點，其兩個框鄰点
只能是 12、14、23、34；各對在兩列中的共同 palette 對唯一決定該 actual pair。

| actual pair ij | lists 的兩份 common palette | 非 D 色對 |
| --- | --- | --- |
| 12 | ({2,3},{0,3}) | (2,0) |
| 14 | ({0,3},{0,3}) | (0,0) |
| 23 | ({2,3},{1,3}) | (2,1) |
| 34 | ({0,3},{1,3}) | (0,1) |

**末端 blocks。** 無 contact 的 bridge leaf 需要三個框鄰点，但 1234 的
任一三點集都含 13 或 24，與 tightness 矛盾。有 private contact 的
末端 nonbridge block，其全部 private points 的 D membership 相同，
所以全部是 contacts；triangle 就用盡兩 contacts，K₄ 需要至少三個。
若圖不只這一 block，另一末端 block 無 contact，落入下述排除；若只有
一個 nonbridge block，全部至少三個點都須是 contacts，也不可能。
K₄ 由 r∪B 的原連通外框引理排除。

無 private contact 的末端 odd cycle，其 private points 的共同 palette
對迫它們接同一 actual pair ij。取兩個相鄰 private 點 u,v。
H∖{u,v} 連通，保留兩 contacts 與 r，並各由原 cycle 邊接到 u,v。
若 ij=12／23／34，五袋為 {u},{v},{b_i},{b_j}，
W=(H∖{u,v})∪(B∖{b_i,b_j})；W 經 rb₀ 連通，且四個 singleton
構成 K₄、各接 W，給 K₅。若 ij=14，改取
{u},{v},{b₁,b₀},{b₄}，W=(H∖{u,v})∪{b₂,b₃}。
G 碰齊 B，b₂、b₃ 都有不在 {u,v} 的原內鄰点，所以 W 連通；
原 rb₁、rb₄、框邊及 cycle 邊仍給全部十條 K₅ 鄰接。

因此每個末端 block 都是 bridge，且其 leaf 恰為兩 contacts。
**這還不能直接說 C 是 path**，因內部可能有 odd-cycle block。
block-cut tree 只有兩個末端，為一條鏈；從一端 contact 沿 bridges
走到第一個 nonbridge block J。初始 bridge 的兩列 palette 色對屬於
A={(2,0),(0,0),(2,1),(0,1)}，後續 ordinary path 點的 lists 如表，
故 bridge palette 交替屬於 A 與 {(3,3)}。不同 A 元素可以在中途改變，
沒有聲稱非 D 色名沿整條路徑守恆。

J 若存在，K₄ 已排，只能是 odd cycle，有兩個 cutpoints 與至少一個
private noncontact。其 palette 對由該 private point 的 actual pair ij
決定，包含 D。入口 cutpoint 在 C 內 degree=3，恰接一個框點 b_k；
palette 包含性與共同 tightness 迫 k∈{i,j}，故入橋 palette 等於另一
端框點的兩列色對，只可能在
B′={(1,1),(0,2),(1,0),(2,2)}。
B′ 與 A∪{(3,3)} 不交，矛盾。此步補足任意數目 internal cycles 的缺口，
不是只排末端 cycles 就推 path。

所以 C 真的是 contacts 為兩端的原 path。相同表的轉移使每條非 D／非 D
palette bridge 的兩端具有相同 actual pair ij。任選此邊 uv，
H∖{u,v} 經 r 仍連通；用上面的同五袋 K₅ minor 全排，包含兩點 path
及任意長 path。因此本支有任意大小排除；finite controls 只核對共同
附件表、轉移與具名 minor，不代替這段論證。

### 5.2 一-spoke：(2,2)，兩列皆以 G 為 core

本節的色表是同一來源的**必要介面**；不假設每份抽象表可實現為圖。
沿用[通用來源表 §4](../../docs/c5_single_spoke_residual_locality.md#4-完整表與條件式出口的接合)
的最後 102 records。它只需 T4／minimal-q，已用來源排除刪去 pair／pair
型，剩 51 份禁色大小 (1,2) 與 51 份 (2,1)。**不是**從 ε 預算本身
推得這個限制：不可刪减四色覆蓋本來容許兩份 binary 禁色 pair 重疊。
對遠列以整圖共同 D₅／S₄ 搬運後也必匹配同一通用必要表。
再取 actual supports、盾弧互斥與全框限制，得 30 個來源身份、54 個
双列 schedules。它們逐一保留原分量、全部支援、列及禁色身份。

以 q=q₄=01012、唯一 spoke rb₀ 為例，原 record 31 有兩份 binary：
C₀ 支援 012，F₀(q)={1}；C₁ 支援 0234，F₁(q)={2,3}。
第二不相鄰列 p=q₂=01201 的候選覆蓋是
F₀(p)={1}、F₁(p)={2,3}。此具名候選可排除。

同一 C₁ 在 q、p 均禁 {2,3}，兩份 root=2／3 拒絕 palettes 的差異
迫兩 contacts 間是同一條奇數長**原 bridge path**；原 bridges 的唯一
路徑性使兩列使用字面相同的 path 與全部 off-path blocks W_j。
刪去 path 邊後，每個 W_j 的 root residual 在兩列均為 {2,3}。
rooted-palette 唯一性使任何固定 t(T_j) 的色置換都保持 residual。
若某個被 residual 排除的已用色 c 未被 W_j 的自身支援看到，
交換 c 與未用色 3 就破壞該不變性，矛盾。因此每個 T_j 在兩列都需
看到 0、1；在支援 0234 上，q 的色 1 只在 b₃，p 的色 1 只在 b₄，
故每個 W_j 都實際碰 b₃、b₄。

取原首橋 x₀x₁ 的 W₀、W₁，令 J 是 path 加兩原 r-contact 邊的 cycle。
W₀、W₁、{b₃}、{b₄}、(V(J)∖{x₀,x₁})∪{b₀,b₁,b₂}
是五個原 K₅ branch sets；最後一袋經 rb₀ 連通，其十條鄰接正是
[原首橋 minor](../../docs/c5_single_spoke_residual_locality.md#3-record-90-的兩個共用-β)
的接線。必要支援表及同一原首橋 minor 先排 36 個 schedules，留下 18。

**內部橋的 carrier 變換。** 對其中 14 個 schedules，有同一原 binary
在一列禁 {a,D}，另一列禁 singleton c≠D。第一列的飽和给两 contacts
之間同一奇數長原 bridge path；每个 path block 的 residual 恰為 {a,D}。
第二列中，使用的是 rooted off-path palettes 的 D membership 守恆，
不是把整份 binary 當成單接點分量：所有 off-path private 點都不是
原 r-contact，D 在兩列的外部 lists 中同樣出現；從末端 block 的共同
palette 與割點不交聯集逐項歸納，D 在每份 off-path palette 的身份不變。
因此每個原 path block 的 residual 仍含 D。
其橋 palettes 因而在 D／非 D 之間交替；端點禁色 c 迫首末橋為 D。
這些 residual 是精確可延拓 lists：rooted block subtree 可以延拓 parent
色，恰當且僅當該色不在根的 palettes 聯集；bridge／odd cycle 逐項
可證，再由 block tree 的葉向根歸納接回全部原子樹。
若全部偶數橋都为 c，則每个 residual 恰 {c,D}，奇數長原 path 在 root
固定 c 或 D 時都不可染；原 binary 會禁兩色，
與此列只禁 c 矛盾。故有一条原偶數橋 palette 是 d∉{c,D}，其两端
residual 均为 {d,D}。同一雙列支援穩定子表及這條**原內部橋**的框弧
K₅ minor 排掉 14 個 schedules。這不假設非 D 色沿整條 path 不變。

**最後四份。** record 82：spoke rb₀，C₀ 支援 034、F₀(q)={1}，
C₁ 支援 0123、F₁(q)={2,3}；p=q₂=01201 可要求同一覆蓋
F₀(p)={1}、F₁(p)={2,3}。C₁ 的同一原 path block T_j 仍容許
01、012、013、123、0123。record 317 只是兩份原分量的身份互換。
另兩份 record 477／817 的 spoke 是 rb₁，pair 分量支援 0134；其共同
path-block 支援含 b₀。它們的完整具名身份為
`951-T1-82-2-1-23`、`951-T1-317-2-23-1`、
`951-T1-477-2-0-23`、`951-T1-817-2-23-0`。

各 W_j 是連通且 one-sided 的**原頂點集合**；H−W_j 經其他 path 段
及 r 仍連通。純盾弧引理可套在這些集合，未要求它們是 H−r 的整份
原分量。全框支援使每份 actual support 等於其連續盾弧的頂點集。
每個 W_j 都見共同必見點（82／317 為 b₁；477／817 為 b₀），因此
各占該框點的一條 incident 盾邊。盾邊互斥使 W_j 至多兩份。
原 path 長度為奇數，故恰只有一條 bridge、兩份 W。
保留原 pair 分量的完整支援後，兩 W 的支援被迫為 01 與 123
（82／317），或 01 與 034（477／817），允許互換原 contact 的方向。

短 W01 的任何路徑外分量之外部內點鄰居只有原 parent，接點邊可有多條；
全部點完整 degree=4，
支援包含於框邊 01。原接點邊的 critical witness 给非空禁色；利用
原 r／另一分量到框補弧的路徑，短支援 hub 引理排掉該分量。
所以 W01 是自己的原 contact 點。不能因此假設較長 W 的旁支也是
一個 bridge pendant；以下同時處理所有 rooted block subtrees。

長 W123 在 q 下只看見 0、1；長 W034 在 p 下只看見 0、1。
若有任何 path 外 block，沿原 block tree 取 terminal block，它的
private 點都不是原 r-contacts。Bridge 私有葉點需要三個相異實際框
鄰色，與只見兩色及 degree-list tightness 矛盾。K₄ 已由連通外框引理排除。
Terminal odd cycle 的私有點完整 degree=4，恰有兩個實際框鄰点；
W123 的可能 pair 是 12／23，其 q palette 均 {2,D}，而 p palettes
分別 {0,D}／{1,D}。W034 的可能 pair 是 04／34，交換兩列角色亦得到
兩個不同 partner palettes。同一 cycle 在 partner 列的 palette 必一致，
因此全部 private 點都接**同一實際相鄰框點對**。
取相鄰 private 點 u,v：刪去它們後 H 仍連通，框補弧含原 spoke 端點，
故 {u},{v},{b_i},{b_j},(H−{u,v})∪(B−{b_i,b_j}) 是五個原 K₅ 袋。
這也處理 terminal cycle 本身穿過 W 根的情形，不依賴其長度。

所以長 W 無任何 off-path block，只剩其原 contact；它在 H 中只有
r 邊與那條 path 邊，完整 degree=4 只允許兩個直接框附件，不能承擔
三點 actual support。四份全部排除，54 個 schedules 的剩餘數為零。
最初 18-open snapshot 原樣保留；最後正確的 terminal-block 證書是
[final_sidebranch_terminal_blocks.json](../c5_excess_one_e2_951_remaining/final_sidebranch_terminal_blocks.json)，
其中的任意旁支論證取代較早 sidebranch layer 的「一份 pendant」敘述。

### 5.3 兩-spoke：(2,1)，兩列皆以 G 為 core

相鄰 spokes 的既有來源排除／[split-support 定理](../../docs/c5_two_spoke_split_support.md#1-source-contacts-and-proof-boundary)
已給 singleton-only Σ；其前提只需 T4／minimal-q，未借用來源恰缺兩列。
另見[兩-spoke 完整分類範圍](../../docs/c5_two_spoke_nonadjacent.md#7-exit-integration-and-exact-scope)。
只剩非相鄰 spokes。對 q=q₄=01012，遠列為 p=q₁=01202 時共同異色
spoke pair 只有 14；遠列 q₂=01201 時只有 24。後者經兩列共用的
幾何反射 φ(i)=3−i mod5，再對各整圖列作共同 S₄ 色名搬運，成為前者。
所有附件、原 contacts、tuple 座標及兩份分量同時搬運；從未分別
正規化原分量。新有限證書核對兩個朝向及 160 份完整 tuple 搬運。

沿用[必要區域定理](../../docs/c5_degree5_two_spoke_sectors.md)，短區域 piece
J 的實際支援為 014，長區域 L 的支援包含於 1234。兩列在 014 上逐點
相同，故 J 的**完整有序 relation** 相同。兩 spokes 均禁止 1、2。
q／p-criticality 要每份 piece 有私有禁色，所以 J、L 在兩列分別禁
singleton 0、D，不能互換；容量分配只有以下四種：

| 型 | L | J |
| --- | --- | --- |
| I | binary，禁 0 | unary，禁 D |
| II | binary，禁 D | unary，禁 0 |
| III | unary，禁 0 | binary，禁 D |
| IV | unary，禁 D | binary，禁 0 |

對兩份原拒絕 witness 分別固定 r=0 或 D，L 的 lists 均處處 tight。
非 contact 的 private odd-cycle 點仍用 §5.1 的四個 pair／joint palette
表；signature 單射。非 contact 的 bridge leaf 需要三個 1234 框鄰，
必含 q 重色 13 或 p 重色 24，不能共同 tight。K₄ 同樣已排。

r=D（II／IV）時，contact 的 list 不含 D，非 contact 的 list 含 D，
同一 terminal cycle 的 private 點不能混合兩類。r=0（I／III）時，
這個 D-membership 說法不成立；改用完整 joint palette：contact private
cycle 點的外鄰只能是 {r,b₁}／{r,b₄}，palettes 分別
({2,D},{2,D})／({1,D},{1,D})，均與四個非 contact signatures 不同。
所以兩種 root pin 下都不能混合；無 contact 的 terminal cycle 全部
私有點有同一 actual pair，取相鄰兩點便得原 K₅。
對相鄰 pair，原 r–J–b₀ 路徑取代 §5.1 的 rb₀，連起補框弧；pair14
時 full B-touch 迫 b₂、b₃ 仍接剩餘 L，使用同一五袋構造。

每個 terminal block 因而都需要 private contact。Unary L 只有一個
contact：兩個 terminal blocks 不可能；唯一 nonbridge block 也需
至少兩個 private contacts；singleton L 的 r 加三個 1234 框鄰同樣
不能共同 tight。因此 III、IV 全排。

Binary L 則兩 terminal blocks 只能是 contacts 所在的 bridges。
§5.1 的 first-internal-cycle 不交色對论證仍適用：ordinary bridges
只進入 A 或 (D,D)，而首次 odd cycle 的入口橋必進入 B′，兩者不交。
所以 L 是原 path。r=D 时，任一 A 橋兩端的 actual pair 相同，原 K₅
排掉 II。r=0 时，两 contact 葉的唯一共同 tight 框鄰為 14，初始橋
palette 是 (D,D)。兩點 path 会使全圖只碰 014，違反全框；更長 path
必有一條 A 橋，兩個非 contact 端點 pair 相同，原 K₅ 排掉 I。
這處理任意長原 path 與任意多 internal blocks，不以 L4／L6 控制圖
作大小截斷。四種分配全部排除。

### 5.4 有真子核心：省略 spoke 或整份 unary

選一個有真子核心的拒絕列 q。原 degree-4 結構把全部原分量容量限制
為至多二、至多一份 binary（§3.1、§4）。沒有 binary 時，§3.2 迫
恰三 spokes、兩 unary；其盾弧都長二，旋轉後支援為 012、234，
spokes 為 024。只有一個三色 singleton 列使三 spokes rainbow。
其餘四列若拒絕，兩 unary 必分別禁 D 與剩餘已用色；能禁 D 的 unary
必看到全部三個已用色，且禁色 singleton 的 D 身份在整個 actual
support 色名搬運下保持。將它的支援列搬到一份 root rainbow 的 T4
列，即仍禁 root 的唯一可用色，與 T4 全收矛盾。新 certificate 保存
20 份完整支援／共同 S₄／T4 反證。因此全單容量型實際有 |Q|≤1。

有 binary 時，t=0 或 t=1 會有至少三份原分量，與 §3.2 矛盾。
t=3 的 proper core 只可省略 spoke；t=2 若省略 spoke，§4 的原接點
保持 transfer 與 592／1,194 接回證書，連同 §4 的九份原 K₃,₃ 排除，
已給 **零個 disk** T4 全收且含非相鄰二拒絕的結果。原 t=3 必要表
確有九份三點弧控制；不能把未加入 minor 的 raw 表寫成零。
因此只剩具名入口 `951-T2-C2-U-omit-U`：兩 spokes、
一份 binary C、一份 unary U，K=G−U 是全 degree-4、恰拒絕 q 的 core。

U 的盾弧至少長二，且其內點不能被 K 碰到。K 接受 T4，只缺 singleton-h
列 q；未接框點引理迫 K 碰 B∖{h}。因此 U 盾弧恰長二、支援 a–h–b。
若 C 盾弧長三，兩 spokes 必在 a、b；另一非相鄰 singleton 列 p 在
a、b 重色，若 G 拒絕 p 即可省略重色 spoke，已由前項排除。

若 C 盾弧長二，整圖共同 D₅ 搬運對齊 U012（q singleton-1）、C234。
具體地，先旋轉得 U012；C 是 234 或 340，後者再用幾何反射
i↦2−i mod5，將 C340 搬到 C234、保留 U012，並對整份 q 同時交換
色名 0、2，還原 q=01202。這個共同反射也交換兩個遠 singleton 位置，
而下文逐項處理兩者。可用 spoke
端點為 0、2、4。24 在 q 重色，不能讓 cap(C)=2 補滿 root 的三個
可用色；02 在任一遠列 p 重色，已由 spoke 省略分支排除。故只剩 04。
此時 q=01202。另一遠列 singleton-3 的 p=01021，U012 只見 0、1，
它不能以 capacity one 禁 root 的可用色 2 或 D（未用色穩定子會同時
禁二色）；K 本來接受 p，故 G 也接受。最後只須 p=01012（singleton-4）。
r 的可用色為 1、D；U012 同樣不能禁 D，所以只須證 C 在 p 允許 r=D。

K 不碰 q 的 singleton-1，且原 r 加 C 的兩 contacts 有 cycle。
[Unattached-singleton cyclic lemma](../../docs/c5_two_spoke_split_support.md#2-a-useful-consequence-of-the-existing-degree-four-classification)
逐項沿用已有 degree-4 **實際原圖**分類，迫 K 的內部是 triangle，
或兩個互斥 triangles 以一條直接 bridge 連接，沒有 tails。r 的內部
degree=2，故 C 只有兩點原 edge，或五點（二點 path 末端接 triangle）。
保留 C 的全部原附件在 234，完整 degree=4 給正好 9＋243=252 個形式；
不作任意來源大小枚舉，也不把一般 minor 當成 relation 保持。

新固定有限证书逐份核對 K 的完整十列，40 份拒絕 q 且接受 T4。
其中 36 份在 p、r=D 有完整 extension witness。餘下四份都有兩個
相鄰 private triangle 點 u,v 共同接實際相鄰框點對 23 或 34。
H_K−{u,v} 連通，B 補弧含 b₀，原 rb₀ 連起剩餘內部；五袋
{u},{v},{b_i},{b_j},(H_K−{u,v})∪(B−{b_i,b_j}) 及全部十條原邊
構成 K₅ minor。它們連 K 都非平面，不可能來自 disk G。
因此最後省略 U 的配置也全排。

合併 §3.3 與 §5.1–5.4，任意大小 ε=1 來源不能拒絕兩個非相鄰
singleton 列。連同 Q 非空，得到 **ε=1 ⇒ Q 是一點或相鄰兩點**。

## 6. 933／941 的證明何處依賴拒絕集合形狀

| 原步驟 | 能否移植 | 所用特徵與限制 |
| --- | --- | --- |
| degree≥4、H 連通、兩列以上碰齊 B | 可以 | §2 已從一般來源前提推出；不需 P 獨立 |
| 唯一 root、完整原分量／contacts、D+O=1 | 可以 | ε=1 與同一原圖；不准用 endpoint marginals |
| 四容量省略身份跨列互斥 | 可以 | 每份省略圖全 degree-4、恰缺一列 |
| minimal degree-5 q-core 接受兩鄰列 | 可以 | 既有分离引理只需 T4、q-minimal；不需其餘列全接受 |
| 933 每列都有真子核心 | 只對有拒絕鄰點的 Q 位置 | 用 Q 的相鄰性；935 可套，951 不能 |
| 941 的 q₀、q₁ 真子核心與 q₃ 特殊身份 | 不直接套新 masks | 用 Q={0,1,3} 及兩個鄰列的精確角色；不是一般 ε=1 結構 |
| 五單容量至多二拒絕 | 可以 | 原 unary 的 D 身份守恆與省略身份；不需 P 獨立 |
| 941 single-spoke 的二色／singleton-D 三列機制 | 不直接套 | 固定 Q 的三列 palette 身份，951 沒有被迫的兩個真子核心 |
| t=2／3 spoke 接回必要域與原 joint transfer | 可以，在確有省略 spoke 的前提下 | 新 checker 讀完整結果；原「沒有 941」斷言本身不排 935／951 |
| 盾弧 A／hub B | 可重用相应結構／拒絕見證前提 | B 的 hubs 必須在同一原圖逐項構造；不能因有數量預算便假定它們存在 |

P 獨立不是 degree、飽和或共有 color frame 的前提；它在原來源論證中
決定了 933／941 的 Q 形狀及各列 core／禁色角色。把這些角色移除後，
需要補 §5 的雙 full-minimal 論證及 unary-omission 分支，而不能直接
引用「已有 933／941 下界」。本輪已補上這些步驟。

## 7. 證書、實際執行與交付界線

[935 observations](../c5_excess_one_e2_935/observations.json) 保存全部原來源
model／base／added-spoke 身份，完整 joints 的摘要校驗，以及九份三點弧
控制的全部原 tuples、literal full-color witnesses、actual attachments、
components、K₃,₃ bags／九条原邊。
舊 artifacts 全部只讀；必要封存檔本機已存在，沒有重跑還原或舊 producer。
新 checkout 若缺 runtime inputs，先依[封存說明](../../audits/README.md)
還原，不用現行 producer 重生成歷史 snapshot。

新證書的具名路徑與精確作用：

| checker／artifact | 有限範圍與結果 |
| --- | --- |
| [935 checker](../../scripts/c5_excess_one_e2_935.py)、[observations](../c5_excess_one_e2_935/observations.json) | 592＋1,194 份原接點保持 spoke 接回；9 份三點弧原 K₃,₃；零份恰為不相鄰二點 Q 的 T4 結果，亦零份 disk 三點弧 |
| [951 three-spoke checker](../../scripts/c5_excess_one_e2_951_three_spoke.py)、[observations](../c5_excess_one_e2_951_three_spoke/observations.json) | 共同 attachment／cycle 入口表，6 份具名原 K₅；4 份完整控制圖与 960 份 literal boundary rows |
| [951 two-spoke checker](../../scripts/c5_excess_one_e2_951_two_spoke.py)、[observations](../c5_excess_one_e2_951_two_spoke/observations.json) | 2 份 root pin 表、2 个遠列朝向、160 份整圖 tuple 搬運、4 份原 K₅、720 份 literal boundary rows |
| [951 remaining checker](../../scripts/c5_excess_one_e2_951_remaining.py)、[initial observations](../c5_excess_one_e2_951_remaining/observations.json)、[interior bridges](../c5_excess_one_e2_951_remaining/interior_bridges_and_sidebranches.json)、[final terminal blocks](../c5_excess_one_e2_951_remaining/final_sidebranch_terminal_blocks.json) | 54→18→4→0 份 t=1 necessary schedules；20 份 all-unit T4 搬運控制；12 份 final terminal-cycle 原 K₅ 骨架 |
| [951 unary-core checker](../../scripts/c5_excess_one_e2_951_unary_core.py)、[observations](../c5_excess_one_e2_951_unary_core/observations.json) | 252 份由實際原圖分類得到的形式；40 份 T4／q，36 份 p、root=D 完整 witness，另 4 份原 K₅；656 份 q-critical 刪邊 witnesses |

另外做過停止條件要求的具體實現嘗試：限定原分量為兩／四點 path 或
三點 triangle，共 9,504 份附件 assignments。保留的 14 張 T4 全收、
非相鄰 Q 圖（8 張 mask 1014、6 張 mask 1006）全部 **非 disk**；
[subdivisions.json](../c5_excess_one_e2_951_remaining/subdivisions.json) 保存它們
在指定框 **boundary-apex 圖**中的實際邊 K₅／K₃,₃ subdivisions。
這裡不把 apex obstruction 說成原 G 非平面。另保留 disk、ε=1 的
`951-failed-T3-UU-triangle-plus-leaf`，mask 982 額外拒絕 T4 的索引 5，
所以不是反例。這些構造只覆蓋寫明的固定族；任意大小排除由 §5 負責。

基準來源與同期變更：remaining checker 的文件 SHA 以
`git show ca3870f:<path>` 讀指定基準，原 snapshot 不重寫。其餘原
source scripts／artifacts 仍按所存 bytes 核對。同期盾弧引理 1(d) 的
開面措辭修正不改結論；本報告的互斥使用開面，不假設面閉包不交。
較早必要表中標記 open 的欄位是歷史 stage；後續閉合由具名新 layer
及本報告给出，沒有為消除 open 字樣覆寫原 snapshot。

實際執行結果逐條保存於 [validation.json](validation.json)。五個上述
checker 都以 `.venv/bin/python scripts/<name>.py --check` 執行，且都以
`PYTHONHASHSEED=17 .venv/bin/python scripts/<name>.py --check` 重播。
十條命令全部 exit 0，普通／seed-17 的 JSON 摘要相同，各 artifact 逐 byte
相符。其他實際命令與輸出：

```text
python3 scripts/check_docs.py
OK: 545 Markdown files, 5770 local links; anchors, index, handoff checked

python3 tools/docgraph check
OK: 62 documents, 213 relations, 5 families; 0 errors, 0 notes

git diff --check
exit 0，無輸出
```

沒有執行 `lake build`，沒有新增 Lean theorem。
全域文件規則見[DOCUMENTATION](../../docs/DOCUMENTATION.md)。
本報告放在任務 artifact 目錄，保持發派者負責 STATUS／導覽整合的約定。

## 8. 剩餘界線

本輪關閉的是上述來源前提下猜想 E 的 ε≤1 層；没有證明 ε≥2 層或
一般 e(Q)≤ε，也沒有證明任意必要 relation 可以 disk 實現。沒有把
定理 A 的数量預算當作任意 hubs 自動存在，没有完成 E／S／K／W
其他猜想、一般 transition 安全或 K∞=K≤5。紙面分類與原圖拓撲未
Lean 化；有限末端部分需連同所引用歷史分類／transfer 證據一起閱讀。

## 9. 稽核後更正（2026-10-04，D₇ 之後）

依 [D₇ 稽核 §10](../../audits/2026-10-04-task-d7/REPORT.md#10-整合者應寫回的更正) 寫回；§1–8 保留原輪語境。

1. **產物取代標記（必要更正）。** 舊 `interior_bridges_and_sidebranches.json` 的「long block has one pendant component」
   未證，不承擔任意大小結案。checker 現於該層加 `superseded_by`、`historical_mechanism_status`，
   把 `remaining_t1_double_minimal_schedules=0` 改為 `open_schedules_after_this_layer=4`；
   結案數 `remaining_t1_double_minimal_schedules=0` 移到
   [final terminal-block 層](../c5_excess_one_e2_951_remaining/final_sidebranch_terminal_blocks.json)，CLI 的 final 數字改讀該層。
   兩份原檔保存為 `*.v1-ca3870f.json`（D₇ 稽核對象）；`observations.json`、`subdivisions.json` 逐 byte 未變。
   一般與 seed17 `--check` 均 exit 0。
2. **適用範圍澄清。** §5 開頭「不相鄰二點 Q 的每個位置沒有拒絕鄰點」只在 Q 恰兩點時字面成立。
   一般陳述是：所選兩列彼此不相鄰；若 Q 另含拒絕鄰列，相應列已有真子核心。
   兩列皆 full-minimal 走 §5.1–5.3，任一列有真子核心走 §5.4；不依賴其餘三色列被接受。
3. **顯式歸納。** §5.2 的 D-membership 守恆按 rooted block tree 由葉向根扣 palette，
   bridge／odd cycle 各以精確 parent query 驗證；不可誤套整份 binary 的 unary 守恆。完整寫法見 D₇ §5。
4. **標記完備性。** §5.1 首個 cycle 的入口 cutpoint 不是 contact（兩 contacts 已在末端 leaves）；
   §5.4 雙 triangle 的 bridge 可從任一 contact 端出發，原圖同構連同兩 contacts 交換涵蓋兩個朝向。
5. **ε=1 的實質使用。** D₇ §8 把論證鏈套到 E1 的 Σ=951（4,4,4,4,6）與 Σ=935（4,5,5）ε=2 代表，
   兩者都在應失效的前提處停止。
