# N45-PA：N45-PR 紙面候選獨立增量審閱

2026-10-10。BASE：`dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。
本審閱只裁決 N45-PR 紙面；不讀 PG／PC 或本輪 supervisor 的新判定，不作新圖搜尋、來源實現、finite source validator、commit／push／PR。

**獨立裁決：N45-PR 的 N45-U-LP 任意大小排除，在 frozen 任務的全部前提與下列 BASE／外部信任依賴內成立，可供監督採納。**
TRANSPORT、ENDPOINT、SATURATION、ESCAPE、FORCING 也各在本文明列的充分前提內成立；它們不是 LP closure 的替代證據。
本文沒有更新任何共享權威頁。singleton short、S LOW／HIGH／long、原 55、其他 cores、一般 N2／E、ε≥3 均未裁決。

[逐 claim 裁決](independent-judgment.json) · [初始輸入](inputs.json) · [追加輸入](inputs-additional.json) · [檢查](checks.json) · [hash inventory](MANIFEST.sha256) · [回條](delivery.json)。

## 1. 不可变輸入與證據分層

主要紙面輸入是 [frozen N45-PR REPORT](frozen/worker/REPORT.md)，SHA256
`ebcda98bf4f243aaa171d0192724e12690d3565c45fbb6b44b1a738ebcd083da`。
正式 certificate SHA256
`d7d59397814d3007067374e9cb5fc737589d6bfdd33c9f609924bc645b663827`，與 checker 原 bytes 一起保留，只用來辨識有限校準的範圍。

[frozen 任務全文](frozen/worker-authority/docs/history/2026-10-09-n45-u-long-short-pair-tasks.md) 和
[frozen N45 權威頁](frozen/worker-authority/docs/c5_excess_two_nonadjacent_unit_core45.md) 是新工作前提，不是 BASE blobs。
後者 SHA256 `d27e84297a20a14e793bd74d4d223983e67e9b4378eb22f3c6b17bfe4a895462`。
本審閱核對 worker frozen 的九個指定 anchors 的 bytes/hash，未藉閱讀舊稽核判定代替本次推導，也未重新裁決已採納 S/U 全套。

最先以 exclusive-create 建立本 fresh 目錄，固定必要紙面及 BASE Git blobs；所有數學 BASE 依賴均再對 `git show BASE:path`，不是採用當前共享頁或 worker checkout 的未驗 bytes。
初始及追加清單合計 31 份 snapshot records；其中 18 份數學／治理／來源檔是 Git blobs。
目前 HEAD 是 BASE，工作樹原已含其他任務的 tracked／untracked 修改；本審閱只新增本目錄。
HANDOFF／STATUS 的當前版本只是導航，數學裁決以 frozen authority、worker REPORT 和 Git objects 為準。

| 證據層 | 本審閱用途與 trust boundary |
| --- | --- |
| 獨立紙面 | 本文 §2–5 的同圖推導、逐 theorem 前提核對，以及五個 relation lemmas 的獨立證明 |
| 已採納 frozen 結果 | 2+2+1 原盾弧與原 U／L 三點支援是本題明示前提；沒有重開上游 S/U、U1–U4 |
| BASE 紙面 | 盾弧 restriction、local hub、單-root (5)/(4)/(3) 排除按具名條件使用；沒有把一般唯一 degree5 分離定理或 full-Σ 分類代入 |
| 外部 primary | 凍結 Dvořák PDF 的 Lemma 7、Theorem 10；並非 Python／Lean 定理。本文核其原文陳述，不宣稱重證其全部證明 |
| 有限校準 | worker certificate 的 690 relations、2986 lifts、360 endpoint pins、100 saturated columns、29 forcing rows 等只作標明控制域；本審閱不重跑來源資料，不由 0 trigger 作排除 |
| 新機械核對 | 只核輸入 immutability／Git blobs／既有 certificate metadata／十個 boundary rows 的 q/T4 與 D5 索引；沒有圖或 piece 搜尋 |
| Lean／source realization | 無新 Lean theorem、native_decide 或目標 source；均不由本文補立 |

外部 PDF 是 Git object `BASE:audits/2026-10-04-task-d4/a3/gallai-primary-source.pdf`，SHA256
`50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea`。
標題、作者與 [官方原文位置](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf) 相符；本次使用凍結內容，未宣稱 live 網頁核回。
[完整 text extraction](gallai-primary-extraction.txt) 保留 PDF 第 5／6 頁的相關陳述。
連通 degree assignment 不可染時處處 tight；不可染的刻畫是同一 Gallai tree 上 blockwise-uniform palettes，incident palettes 互斥且聯集是原 list。
嚴格 slack 的可染性也可直接以 rooted spanning tree 逆序貪婪證出。

## 2. LP 排除使用的全部原來源前提

量詞是任意大小有限簡單原 disk 圖 G；不是固定 controls 或 tensor templates。

1. B=(b0,…,b4) 是有序 induced C5 外面；完整 Σ(G) 為 933／941 或對整圖共同搬運的 D5 像，故接受 T4。非框邊 Σ-critical，ε(G)=2，有效 H 忽略孤立內點而連通，原 G full B-touch。
2. 原 r,s 非相鄰、完整 degree5；其餘有效原內點完整 degree4。H−{r,s} 恰為原連通 mixed L,S 及唯一原 unary U；每份 one-sided，mixed 在兩 root 的 incidence 均正。
3. U 只有一條原 root-contact rx，且 X=G−V(U)=M 是原拒絕 literal β 的 inclusion-minimal 非框邊 core；共同交換 roots 後 r 是降度側。這是 X 自身 β-edge-minimal，不能只假設原 G Σ-critical。
4. 原 short S 的 actual support 恰為真框邊兩端；原 L long。已採納前提給原 σ_U、σ_L、σ_S 長度 (2,2,1)，邊互斥並分割五框邊；U/L actual support 各是原三点連續弧。
5. 同一原 vertices／edges／named ordered contacts／shared identity／attachments／support／ownership／bridges／rotation／literal frame／完整 tuples、空 fibres、全部 full lifts 固定。X 原保留 L、S、roots、其餘 attachments、全部 retained spokes 與原 rotation 限制。

第 4 點由 frozen 前提承擔。本文核心論證只需要其中 U 盾弧長 2 與原 restriction；没有因此擴張採納範圍到任務外的其他 S 支援。
core β 的 zero slack、short 收(D,D)、long 禁(D,D)、新 γ singleton forcing 等仍是 frozen 必要條件，但 LP 排除本身不需把这些不同列容量相加，也不需把五個新 relation lemmas當作無界 closure 前提。

## 3. REPORT §5.1–5.2：逐步獨立核對

### PA-UNTOP：原盾弧中點與 T4 改色

依 [BASE shield §2 引理 1(c)](frozen/base/docs/c5_unary_shield_budget.md)，對原 one-sided U，σ_U≠B 時 H−U 的 boundary 附件不能碰 σ_U 內點。
σ_U=h–m–k 長 2，只有內點 m；r、s、L、S 全在 H−U，所以 m 不能有任何 retained root spoke 或其他 retained 內點鄰居。
X 恰整份刪 U，因此 `N_X(m)\B=∅`。這個限制是在原 G 中得出，不是另給被刪 U 一條 X 盾弧，也没有假設 X full B-touch。

G 接受 T4，刪 U 使 X 接受 T4。對任一三色列 α≠q_m，m 的色至少還在另一框點出現；將 m 改為未用第四色得到 proper T4 列，取 X 的同一份完整 lift，再將 m 改回。
induced B 及 m 無內鄰使兩條框邊仍合法，所有內邊不變。這正逐條满足
[BASE unattached-boundary §1](frozen/base/docs/c5_unattached_boundary.md)。故 `Σ(X)⊇Ω\{q_m}`。
X 拒絕 β，唯一可能是 β=q_m 的 S4 類，且 `Q(X)={m}`。

canonical q indices=(6,4,3,1,0)，933 的 q2 仍是合法原拒絕列；m=2 時它保留，並未被 941 表覆蓋掉。
Δ 精確為 Q(G)\{m}，941 有 2 列、933 有 3 列；這是同一 X 的接受差，不是選另一張 derivative。
此步證據是同圖完整改色 paper，有限 boundary-row 核對只核索引。
**裁決：成立。**

### PA-MINIMAL：X 自己的 edge minimality 與 degree

M 的 inclusion-minimality 是本題原身份，不是原 Σ-criticality 的遺傳敘述。
若任一 retained 非框邊 e 可刪後仍拒 β，X−e 就是更小的拒絕子圖，矛盾；所以每條 retained e 刪後均接受 β。
此已足夠滿足三條單-root theorem 的 edge-minimal-q 前提。

U 是 H−{r,s} 的完整分量，與 L/S 無邊，且只有 rx 接 root；r 恰失一 incidence 成 degree4，s 不失任何邊仍 degree5，所有其餘 retained 內點仍有原完整 degree4。
X 保留 B 的所有框邊與無 chord 性及原 disk 嵌入。有效 H_X 無額外孤立點。
**裁決：成立，必須保留 `X=M` 的原前提；一般整 U derivative 無此保證。**

### PA-COMPONENT：C 是實際原分量，relation 沒有換圖

`H_X−s=C={r}∪V(L)∪V(S)`。
L、S 原各連通，兩份各有原 r-contact，故同一原 r 將兩份接成一個連通圖；沒有第二份 X−s 分量。
C 每點在 X 的完整 degree4，s 是 X 唯一 degree5。
原圖 simple，故 s 的 incident C edges 對應互異原 vertices；即使某 piece contact 同時接 r 和 s，它在完整 relation 中仍是同一座標。

未 pin s 的完整 lifts 精確為

`Lifts_C(α)=⋃_{a∈E_r^X(α)} {r↦a}×Lifts_L(α;r=a)×Lifts_S(α;r=a)`。

這個 Cartesian 接合只發生在不同完整分量 L/S：它們內部無交集且無跨邊；所有 r 邊、r spokes、原附件已逐條施加。
同一 piece 的各 contact 不能各取一個 marginal。由這些完整 lifts 讀取原有序 s-contact tuple，再施加 s=b 取得全部原 fibre；shared contact 仍只讀一次。
此式對每個 literal α 都使用同一 C 和同一原 edges，没有 contraction、replacement、逐列選圖或改 contacts。
**裁決：成立。**

## 4. REPORT §5.3：單-root theorem 的完整前提映射

### PA-SPOKES：t_s≤2、relation 非空與 F_C 精確

β=q_m；B\{m} 的四點只有兩色，且 s 無到 m 的 spoke。
若兩條 s-spokes 的 β 色相同，刪任一條完全不改 s 的可用色，所有其餘約束也不變，X 仍拒 β，違反 X 自身 minimality。
所以 retained spokes 的 β 色互異，`t_s∈{0,1,2}`。
完整 degree5 給 s–C contacts 恰 `5−t_s` 個互異原頂點。

C 未 pin s 的 lists 至少等於其 internal degrees，每個 s-contact 因未施加 s 色而多一份 strict slack。C 連通且有 contacts，故完整 R_C(β) 非空。
X 拒 β 使 E_s⊆F_C。刪 s 的任一 spoke後，原 E_s 仍全被 C 禁止，接受 β 的新 full lift只能令 s 取該 spoke 唯一釋放的色；因此每個 spoke 色都不在 F_C。
于是 `F_C=Col\β(N_B(s))`，大小 4−t_s。这不是从有限禁色表假设出的覆盖。
**裁決：成立。**

共同前提映射如下；它們都在 X 自己計算。

| 單-root theorem 前提 | X 中的原 witness／推導 |
| --- | --- |
| 任意大小有限 simple induced-C5 disk | X 為原 G 的整 U 省略子圖；框與原嵌入保留 |
| 有效 H 非空連通 | C 原連通，且 s 有 5−t_s≥3 條原 contacts 接 C |
| edge-minimal-q | PA-MINIMAL，由 `X=M` 給 retained 邊的 β 刪邊 acceptance |
| 唯一完整 degree5 root | s=5；r 與 L/S 所有 vertices 在 X 完整 degree4 |
| H−root 一份原 C | PA-COMPONENT，兩份 mixed 经同一 r 原接合 |
| 相應原 spokes／互異 contacts | PA-SPOKES，t_s≤2、5−t_s 個原 s-neighbors |
| 完整同列 R_C、禁色 F_C | PA-COMPONENT 的全部 full lifts；PA-SPOKES 的非空及完整 intersection |
| q=01012 表記 | 對整個 X 共同 D5＋S4，將 β singleton m 搬到 b4；全部 contacts／attachments／rotation／literal pins 一起搬 |

三條 theorem 不另需原 G full Σ=933／941、T4、第二列拒絕或 X full B-touch。
本題 T4 已在 PA-UNTOP 使用，不能擅將 X 有空框點視為單-root theorem 不適用。

### PA-T0：no-spoke §4 的 (5)

[BASE no-spoke §4](frozen/base/docs/c5_no_spoke_exterior.md) 明說本節不需 §2–3 的 C 外連通或 K4-free。
t_s=0 時 C 有 5 原 contacts，F_C=四個色。同一 C 的四份不可染 tight lists 给一個共同 block-difference 係數 τ，`Iτ=1_P`。
block incidence matrix 的欄獨立由 leaf block 私有點消去得出，不是為每對顏色選另一棵樹。
四份 palettes 迫正 active block 的 palette 為 Col\{d}，因此是 K4；負 active block palette為 {d}，因此是 bridge。planarity 只排更大 clique，不排掉這裡必須保留的 K4。
incident palette 互斥使 contact vertex 在 active forest 的 degree1，其餘 active vertex degree2；block nodes degree4或2。
若有 h 個非空 components、k 個 K4 nodes，葉數是 `|P|=2h+2k`，必偶數，與 5 矛盾。
没有假定 s 與 B 在 C 外另有一條路，也沒有循環套用多分量 K4-free。
**裁決：成立，t_s=0 完全涵蓋。**

### PA-T1：single-spoke (4) §1–5

[BASE single-spoke-four](frozen/base/docs/c5_single_spoke_four.md) 的 sole C、4 ordered contacts、三個 forbidden root colors皆已映射。
原 spoke 使 B∪{s} 真正連通，故 [BASE connected-exterior K4 lemma](frozen/base/docs/c5_degree5_tree_components.md) 可排 C 的 K4 block。
三份同一 C 的 palettes 共用 τ；四葉 active forest 是兩個正 triangles 加一條負原 bridge，没有接點外臂。這個無界結構是紙面推導，不依 skeleton 長度上限。
左 triangle 的三點各在完整 degree4 下留一條原外接邊。若進入不含 contacts 的 inactive 旁支且該旁支不碰 B，刪旁支後有 slack，旁支自身以全四色 lists 著色，再整體置換避開接頭即可拼回不可染列，矛盾。
故三條原 boundary tethers存在，內部互斥並避 active 結構和 s。
原 branch sets `{a},{b},{x},{s,c,d,y}, B∪(三條 tethers 去掉 triangle 起點)` 互斥連通；最後一對鄰接正由唯一原 spoke提供，其他九對由 triangles、contacts、bridge及tether首邊提供。
只得到非平面 K5 minor，沒有把 boundary 合併當染色操作。
**裁決：成立，t_s=1 完全涵蓋。**

### PA-T2：two-spoke (3) §1–5，包括任意異色 spoke 位置

[BASE two-spoke-three-contacts](frozen/base/docs/c5_two_spoke_three_contacts.md) 開头雖以相鄰 b0,b1 表記，§5 明涵蓋任意兩個不同 β 色 spokes。
這不是未證的幾何替代：證明實際只使用兩份 full tight lists、它們在三個原 contacts 上的逐色差、complete degree4 與至少一條 root–B spoke。
同一 block incidence 的三葉 active forest 迫一個 triangle 加三條任意長 bridge arms，終點恰是三個原 contacts；零臂也保原 contact edge。
完整 degree4 及無 contact 的 inactive 旁支 argument 给三條實際 boundary tethers。
`{s}`、三個 triangle＋完整 arm branch sets、`B∪(三条 tethers 内部)` 互斥連通；三條原 contacts、triangle 邊、tethers 与一條原 spoke 給十對原邊鄰接。
更換異色 spoke位置不会改变上述 minor witness 的存在；只对整图统一命名 spoke 两色和其余两色，不重排 boundary、不换 C、arms 或 contacts。
本題 minimality 已證異色；β singleton m 無內鄰也保证两 spoke色来自 B\{m}。
没有額外要求第二拒絕列或 T4。
**裁決：成立，t_s=2 的任意異色位置完全涵蓋。**

### PA-LP-EXCLUSION 與 scope

t_s 只可能 0、1、2，而三個各自充分的原 theorem 全部導致矛盾。因此 frozen N45-U-LP 原來源不存在。
这是 conditional 任意大小 paper，信任 BASE 具名證明與外部 Gallai；不是 worker certificate 寫入「contradiction」就算證明。
採納只建議 N45-U-LP。更廣圖類未審，即使某些推導形式上只用了較少前提，仍不據此擴大本輪 closure。
**裁決：成立，可供監督採納。**

## 5. 五個 relation lemmas 各自的充分前提與裁決

以下不借 LP 不存在來作 vacuous proof；均在各自一般介面內獨立核對。

| CLAIM | 最弱使用介面與原圖充分條件 | 獨立推導／裁決 |
| --- | --- | --- |
| N45-PR-TRANSPORT | 固定 piece 內邊、全部 actual attachments、ordered contacts與shared identity；一個色雙射 π 在每個實際 support 上使 γ=πβ。若有 pins，它們一起映射 | 每條原不等色及每條附件禁色逐邊保持；π⁻¹ 给逆映射，故全部 lifts、完整 tuples、全部含空 fibres 双射。**成立**；不需 disk／criticality／degree／大小界 |
| N45-PR-ENDPOINT | 直接局部原則只需 connected complete-degree4 P、planarity、覆盖全部 N(P) 的2或3個互斥連通pairwise-adjacent bags、bag内N(P) pins各为不同常色。三点支援版本以原 P為H−roots完整分量、K=H−P非空連通、full B-touch、support恰h–m–k及所有owner roots pin端点色保证这些bags | 若端点色不同，bags=`K∪(B\{m,k}),{m},{k}`；端点同色則合併k進大袋。两个support外框点由K原touch，给大袋连通；框边给全部bag邻接。N(P)只含原owner contacts与h,m,k；不要求outside整图合法染色。tightness禁止同点有两个同bag外邻，contract仅在minor反证保持degree/lists。BASE E4§4.1 local hub／两三hub Gallai给K5。**成立** |
| N45-PR-SATURATION | 一个固定非空s-compatible complete relation，k个不同原r contacts；F是全部兼容tuple的contact色集交，且|F|=k | 每份完整tuple的r色集含F而至多k色，所以恰是F，contacts色各异。应用到全部full lifts由tuple完整性给出。**成立**；不需disk／degree／目标Σ |
| N45-PR-ESCAPE | 原G=X接回原U，唯一跨边rx；γ的原U palette={a}；β′是G接受列，且一個π在U actual support上搬γ到β′ | TRANSPORT搬palette为{πa}。β′任一G full lift限制到X，并由原rx强制r≠πa。**成立**；γ不必属于Δ，亦不需criticality／LP／degree；绝不保证指定coloring的repair |
| N45-PR-FORCING | complete χ=0 joint，固定E_r,E_s，局部非空fibres给完整raw columns且|F_C(b)|≤k_C^r；degree4低root的原incidence identity `|E_r|=m_r+d_r`；非空joint全部r投影={a}。原two-mixed无unary、r=4及piece complete degree4／r正incidence给这些条件 | 完整joint使allowed r=`E_r\V_b`⊆{a}，n_b=0或1。δ+o+λ=`m_r−|V_b∩E_r|=n_b−d_r`。所有项非负、至少一接受栏给d_r≤1；d_r=1迫每栏n=1且三项0，故全部joint={a}×E_s。**成立**；不需disk／criticality／target／跨列容量 |

ENDPOINT 的「原 piece」必须展开成 **P 的所有内鄰恰為已指定 owner roots**；否则 `N(P)∩大袋` 不一定全是端點色。
这是沿原 piece 定义已有的前提，本文将其显写以便独立引用，不把lemma扩成任意vertex subset版。
完整 degree4也不能在后续单独引用时遗漏。

U 的 singleton role 是 ENDPOINT 的独立 corollary：unit contact palette 非空；endpoint 两色不可是唯一palette色。
ABA 时交换support未见两色保持全部原lists和lift集合，singleton不能落在未见两色；因此只能是中点色。
ABC 时剩中点色或唯一未见第四色。TRANSPORT使同一shape角色相同，不允许每列独立挑role。
**裁决：成立；单独列为 PA-U-ROLE。**

三点U/L只有ABA、ABC两种literal色shape，edge-pair S只有AB，所以五份原tensor可以搬十列完整介面。
这只减少色shape查询種類；tensor仍含任意大原interiors和full lifts。不同piece可用不同support-compatible π作计算，但各查詢必须还原到同一全图literal pins；不能将不同搬出pins直接当成同一全图pins。
没有任意抽象tensor的source-realizability theorem，没有specified-colouring repair／replacement。

## 6. 七格、D5、root交换与有限控制边界

worker 保留 7格／15个(β,Q_X)选项，10份named shield partitions；PA-UNTOP从150个必要mask组合排120个β中点不符及16个pair，余14个只需t_s三分，42项是纸面覆盖账。
此独立审阅从BASE cells原十列校准q-index／target mask／T4改色与whole-frame D5；没有把这些组合叫150张来源图。
D5和S4作用于整X的全部edges、contacts、attachments、rotation和字面frame；root交换也共同交换owner labels及完整fibres。933 q2保持有名身份，搬后不擅改叫canonical原target。

| calibration／coverage | 本審閱分类 |
| --- | --- |
| worker transport 9721 maps／155536 fibres、690 relations、2986 lifts | worker fixed calibration metadata；hash已核，不作为paper充分性证明；未在本任务重复replay |
| 360 endpoint pins | 原18份triple unary有控制；long mixed triple缺控制，不能由unary控制补source coverage |
| 100 saturated columns | worker全部兼容tuple/lift校准；不证明LP來源存在或不存在 |
| 29 singleton rows／7新γ | 固定N2 derivative的interface校准；全部d_r=0，d_r=1缺positive control；algebra独立成立 |
| 11原整U derivative | 7 N2、4 N1；certificate均标not triggered。精确LP／target／拒绝minimal45/54来源没有positive control；本文不自行复验finite source契约，不把0触发作排除 |
| 抽象mask与负资料 | 不构成数学source反例；本文没有建立source counterexample |

finite不足以提供缺失的long-mixed、d_r=1、精确LP正控制；这些缺控制不使已有paper推导自动失效，也不被PASS消除。

## 7. Findings、未覆盖与检查

- **N45-PA-F01：未发现本契约内的纸面断点。** 原shield中点→X实际未接框点→同图T4改色→X原sole C→t_s三分的所有关键前提已逐项对回；推荐只采纳N45-U-LP。
- **N45-PA-F02：独立引述ENDPOINT时须显写原piece边界。** connected P alone不够；需N(P)内邻全是已指定owner roots，及complete degree4。原worker在“原piece”语义内满足，本文不改其字节。
- **N45-PA-F03：控制缺口保留。** long-mixed endpoint、forcing d_r=1、精确LP来源仍缺positive control；不称数学反例或一般proof failure。
- **N45-PA-F04：trust boundary固定。** 结论明依BASE任意大小(5)/(4)/(3)证明与外部Gallai刻画；本审阅核应用及相关证明步骤，但没有重跑全部上游Python、重证所有分类或新增Lean形式化。
- **N45-PA-F05：历史FAIL不改写。** frozen worker所报E4历史byte replay/provenance FAIL、fresh BASE两历史缺档、whole-worktree DocGraph duplicate IDs原样保留；本paper审阅没有把它们重新标PASS或声称重新执行这些治理检查。

未覆盖：singleton short、所有S身份LOW/HIGH/long、原55、其他core、一般N2/E、ε≥3、任意tensor来源实现、指定coloring repair、全部上游test／Lean／remote CI。
当前任务以只读paper审阅完成；没有选择下一residual、没有共享更新、没有提交或外部动作。

本目录自身新文本／JSON／hash inventory与输入immutability结果见checks.json；初始direct pdftotext文本以及后来exclusive-create的正式extraction均保留，未覆盖任何既有文件。
manifest精确含所有regular payload，仅排除根MANIFEST.sha256与delivery.json以避免循环；delivery绑定manifest及independent-judgment SHA。
