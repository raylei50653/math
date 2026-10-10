# N45-SSA：N45-U-SS 獨立增量 paper 裁決

2026-10-10。任務根 `/home/ray/developer/ai/math`；HEAD／BASE 均為
`dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。

**裁決：候選的全部 11 項 claims，在下述完整 SS 契約與明列信任依賴內成立；
未發現阻擋採納的新推理缺口。建議限定採納 N45-U-SS 任意大小 paper 排除。**
§8 另核限定父身份的互斥、窮盡覆蓋：已採納 U 化約及 LP，與本 SS 合成後，
足以排除 authority §1 精確的整 U 省略 N45-U 身份。此 corollary 仍限
`X=G−V(U)=M`、唯一原 root-contact、原兩 mixed 等全部前提。

候選入口是本次凍結的 [REPORT](frozen/candidate/REPORT.md) 與
[claims](frozen/candidate/claims.json)。逐 claim 的獨立理由、分支前提、trust 與
block 欄在 [independent-judgment.json](independent-judgment.json)。
本稿是 paper 稽核；没有建立有限 SS source、正控制、來源實現或新 Lean 證明。

## 1. 凍結與獨立性

先讀現行 HANDOFF／STATUS／DOCUMENTATION 及 Git state，依文件入口查找；未用 Graphify。
以 exclusive-create 新增本目錄，未改 worker、共享頁或其他 audit。
[inputs](inputs.json) 凍結候選 REPORT／claims／inputs／inputs-additional，並額外保留候選
checks、verifier、manifest、delivery；所有必要既有依賴另外凍結。

BASE 文件均重新執行 `git show BASE:path` 取得 bytes，`git rev-parse BASE:path` 取得 blob OID，
與 worker frozen 及指定 SHA256 三方核對。五個 current-work pins（authority、原 PR REPORT、
PA judgment、原 U REPORT、SU-A judgment）均逐 byte/hash 核回，但它們不是 BASE blobs。
现行入口、历史派工、既有採納報告另標 current context；BASE 缺檔 probe 的 exit128 保留。

本 SS 裁決直接從原邊、shield／T4 及三份 BASE theorem 重推；沒有以 LP 已成立裁決證 SS。
PA／SU-A 已採納結論只在其明列信任界內重用；§8 因監督新增的父身份覆蓋要求，
才閱讀既有 PA 的 LP 完整前提與既有 SU-A 的 U-U2／SHORT／RES。
未讀任何別位本輪 reviewer 或根的新裁決；未委派 subagent、commit、push、PR 或對外發訊息。
工具可核文件、時間與 hash，不能證明閱讀者的心理獨立性；這是本稽核的直接聲明。

## 2. 主量詞、完整 SS 契約與 trust

量化任意大小有限簡單原 G 及具名 U、L、S、原拒絕 literal β 與 X；不限制
piece 大小、橋長、旁支或附件數。每項 claim 都保以下全部充分前提：

1. 有序 induced C5 外框 B 圍 disk 外面；完整 Σ(G)=933／941 或一個共同整圖 D5 像；
   每條非框邊 Σ-critical，ε(G)=2。
2. 原有效 H=G−B 連通且原 G full B-touch；恰兩個非相鄰完整 degree5 roots r,s，
   其餘有效原內點在 G 完整 degree4，無 rs 邊。
3. H−{r,s} 的完整分量恰是唯一 unary U 及 mixed L、S；三份 one-sided，
   actual support 非空；每份 mixed 的兩側 incidence 均正。
4. U 的唯一原 root-contact 為 rx，無 s 邊；X=G−V(U)=M 是原拒絕 β 的
   inclusion-minimal 45／54 core。共同 root swap 後 r 為降度側；U 外所有頂點、邊完整保留。
5. L support long，意為不包含於任何真框邊的兩端；S actual support 恰一個具名原框點，
   且 k_S^r+k_S^s≥4。
6. 原 degree 等式為 t_r+k_L^r+k_S^r+1=5、t_s+k_L^s+k_S^s=5。
7. 具名 ordered contacts、shared 頂點單坐標、全部 attachments／supports／ownership、
   bridges／原 rotation／一個 literal 色框、完整 relations／全部空與非空 fibres／full lifts 固定。
   D5、S4、root swap 只共同作用整圖及其資料。

與 [BASE cells](frozen/base/artifacts/c5_cells/cells.json) 對回：q0/q1/q2/q3/q4 的 cells
indices 分別是 6/4/3/1/0；941 拒 q0,q1,q3；933 另拒 **q2**；T4 indices={2,5,7,8,9} 全收。
本稿没有略掉 q2，也没有把外部色改名後的新 β 冒稱原 canonical row。

明列 trust：

| ID | 既有依賴與本輪使用 | 信任界 |
| --- | --- | --- |
| T-SHIELD | [BASE unary shield](frozen/base/docs/c5_unary_shield_budget.md) §2 引理1(a–d)、§3 A | 原面／原盾弧限制、互斥及原 unary 費；本輪重讀相關證明，未全鏈形式化 |
| T-U | [原 U](frozen/current/audits/2026-10-09-n45-u/REPORT.md) WIT／S3／U2／SHORT／RES，[SU-A](frozen/current/audits/2026-10-09-n45-su-a/REPORT.md)、[SU 採納](frozen/current/audits/2026-10-09-n45-su-supervision/REPORT.md) | 已採納具名窄結果；WIT 用於 SS，其他用于 §8；未重跑所有上游分類 |
| T-T4 | [BASE 未接框點](frozen/base/docs/c5_unattached_boundary.md) §1 | 同一完整 coloring 中的一點改色；本稿獨立重述證明 |
| T-REL | [BASE 完整介面](frozen/base/docs/c5_degree5_interfaces.md) §1–2 | R_C/F_C 精確接合、strict slack；不取 marginals 或逆轉 F_C 投影 |
| T-T0 | [BASE no-spoke](frozen/base/docs/c5_no_spoke_exterior.md) §1、§4 | sole C、五 contacts、四拒絕 lists 的偶數障礙；不需 §2–3 外路或 K4-free |
| T-T1 | [BASE single-spoke-four](frozen/base/docs/c5_single_spoke_four.md) §1–5 與 [connected-exterior K4](frozen/base/docs/c5_degree5_tree_components.md) §1 | 共同三份 palettes、實際 tethers、K5；原 spoke 提供外部連通及最後鄰接 |
| T-T2 | [BASE two-spoke-three-contacts](frozen/base/docs/c5_two_spoke_three_contacts.md) §1–5 | 三葉 active triangle／任意長含零長 arms／實際 tethers；§5 任意異色 spoke 位置 |
| T-GALLAI | [BASE primary PDF](frozen/base/audits/2026-10-04-task-d4/a3/gallai-primary-source.pdf) 第5–6頁，Lemma7／Theorem10；[本輪抽取](gallai-primary.txt) | 外部 connected degree-list 的 strict slack／tightness／Gallai blockwise-uniform 刻畫；非新 Python/Lean theorem |
| T-LP | [PA](frozen/current/audits/2026-10-10-n45-pa/REPORT.md) §2–4，[LP 採納](frozen/current/audits/2026-10-10-n45-p-supervision/REPORT.md) §2 | 僅 §8 合成用已採納 LP；SS 獨立論證不依其裁決 |

Lemma7 的前提是連通及每點 list size≥internal degree；有一處 strict slack 即可沿生成樹
由葉到根著色。Theorem10 的前提同樣是 connected degree assignment，不可染 iff
Gallai tree 且 block palettes 在各 cut vertex 不交、聯集等於原 list。每次使用都在同一 C、
同一拒絕 pin lists 上滿足；没有假定待證 C5 boundary theorem 或使用四色定理 oracle。
PDF 从 BASE Git object 凍結，本輪未來源搜尋、未作新的官方網路驗證。

## 3. COST、UNTOP、U3、U2

原 rx 的 Σ-criticality 給 γ∈Σ(G−rx)−Σ(G) 的完整 lift。限制到 G−U 是合法 outside
witness，且无法填回整 U，否則 G 接受 γ。此 γ 可不同于 β；只沿同一原 G 收幾何費。
若 U support 包含框邊 hk 兩端，full B-touch 在 B−{h,k} 給 outside 的真實附件。
H−U 連通，故 r 有避 U 的原路到該附件；已採納 U-WIT／BASE A 排 short U，得 |σ_U|≥2。
long L 由 shield 引理1(b) 得 |σ_L|≥2。兩份 one-sided 盾弧邊互斥、總≤5，
故有序身份恰為 **(2,2)、(2,3)、(3,2)**。不需對 singleton S 收正費，不借 LP 的2+2+1。
這個列舉的充分性只是必要域：不表示各身份有 source。

原 K_U=B∪G[U]∪E(U,B) 的面由原 embedding 決定。H−U={r,s}∪L∪S，
兩份 mixed 的正 contacts 保它連通；outside 的開圖及附件開段落在同一內面 𝓕_U。
σ_U 是不在 ∂𝓕_U 的框邊，而非任選 gap。|σ_U|≤3<5，故引理1(c) 的
σ_U≠B 確實成立。N_B(H−U) 全避 σ_U 內點，其中包含 retained root spokes 及 L/S attachments。
X 恰整份刪 U，故每個盾弧內點 v 都有 N_X(v)−B=∅；没有要求 X full B-touch。
長2是一個內點 m；長3是兩個不同原內點 m,n。

X 子圖繼承全部 T4。任一 proper 三色 η 的各色 multiplicity 為2、2、1。
若 v 無 X 內鄰且不是 η singleton，把 v 一次改成未用第四色 D，仍是 proper T4。
取 X 的完整 lift，再在同一完整 coloring 只把 v 改回 η(v)：內鄰为空且框 induced，
仅須核兩條框邊，而 η proper 已保證。不拼不同列的端點資料。

- **U3／(3,2)：** η 的 singleton 不可能同時在 m,n；選非 singleton 的其中一點作上述
  一次改色，即接受每個三色 η。連同 T4 得 Σ(X)=Ω，與拒 β 矛盾。無需同時改兩點。
- **U2／(2,2) 或 (2,3)：** 同一改色接受 Ω−{q_m}。X 拒 β，且β為原三色拒絕列，
  故 β=q_m，Σ(X)=Ω−{q_m}、Q(X)={m}。m不在原Q(G)則已矛盾；否则进入三分。
  L 長3有四個原 support 點也不影響此鏈；沒有錯借 triple-support endpoint lemma。

四項裁決皆成立，無新增 block。原 unary 見證不是聲稱 β 下 F_U 非空。

## 4. X-CORE、COMPONENT：逐邊、完整 degree 與全部關係

`X=M` inclusion-minimal 且拒同一 literal β，直接给每條 retained 非框邊 e 的
β∈Σ(X−e)。這是 X 自己的 edge-β-minimality；原 G criticality 单獨不能給它。
原 H−{r,s} 是完整分量，故無 U–L/S、L–S 邊；U unary 且只有 rx，故無 s–U；無 rs。
原非框邊完整分為 root spokes、U 內邊／框附件／rx、L/S 內邊／框附件／各側 contacts。
X 恰刪 E(U)∪E(U,B)∪{rx}，其他全保留。
所以 r 的完整 degree 從5降4，s仍5，L/S每點仍4。H_X 原連通。

在 X 中由唯一 degree5 s 识別實際
`C=H_X−{s}={r}∪L∪S`。
它由 L/S 的正 r-contacts 連通、恰唯一；所有 C 頂點在 X 完整 degree4。
`E(C)=E(L)∪E(S)∪E(r,L)∪E(r,S)`，
`E(C,B)=E(r,B)∪E(L,B)∪E(S,B)`，`E(s,C)=E(s,L)∪E(s,S)`。
保原 rotation 的限制及全部 bridges，没有收缩 r、改图或保留 U 殘段。

對任意 literal η，令 ℒ_P(η;r=a) 是 P 的全部原頂點 assignments，核全部內邊、
框附件及 r-contact 避 a，暫不施加 s pins。則完整 assignments 恰為

`ℒ_C(η)=⋃_{a∈Col−η(N_B(r))} {r↦a}×ℒ_L(η;r=a)×ℒ_S(η;r=a)`。

左到右是限制原 assignment；右到左因原 L/S 無交點、交邊，且列出的全部邊已核，故可接回。
再在原 ordered s-contact 頂點讀色得到完整 R_C。shared r/s-contact 是 piece 中同一頂點，
只讀一個色；接 s=b 的 fibre 恰是全部 contacts 避 b 的上述 assignments，空 fibre 同樣保存。
再接 s 的原 spoke lists 得 X 的全部 full lifts。十列共用同一 C、原邊及坐標。
兩 claim 成立；此推導沒有以抽象 tuple schedules 替代真圖。

## 5. SPOKES：异色、非空與 F_C 精確

僅長2剩餘情形。β=q_m，m無X內鄰，故s所有spokes避m。
B−{m}在β只有兩色；若兩spokes同色，刪一條不改s的list或其餘約束，仍拒β，
違X自身minimality。因此s的spokes β色互異，t_s∈{0,1,2}。
完整degree5及simple给 `|P_s|=5−t_s` 個互異原s-neighbors；shared contact不重算兩次。

不pin s時，C內每點list size至少deg_C；每個s-contact因少施加一條原s邊而有至少一色slack。
C連通且P_s非空，strict-slack引理给完整R_C(β)≠∅。
定義 `F_C=⋂_{t∈R_C}set(t)`。
X拒β使每個s可用色 `E_s=Col−β(N_B(s))` 都在F_C。
對每條spoke e，X−e接受β。其s色若仍在E_s，便能填回e，矛盾；
spoke色互異，使新s色恰為e唯一释放的β框色。C未變，該同一full lift的全部contacts避該色，
故每個spoke色都不在F_C。結合两方向，**F_C=E_s、|F_C|=4−t_s**。
不是向別列借容量，也沒有漏掉可能空fibre。裁決成立。

## 6. T0、T1、T2：BASE 前提逐項適用

三 theorem 共用前提都在 X 自身核：finite simple induced-C5 disk；H_X非空连通；
X自己edge-minimal拒β；唯一完整degree5 s，其他全部完整4；H_X−s恰sole C；
原spokes與5−t_s個不同具名contacts；完整R_C非空及精確F_C。
β singleton m可由一次共同D5搬到b4，再一次整圖S4命名成01012，全部lists／contacts／
attachments／ownership／rotation／masks／fibres一起搬。没有为不同pieces另选色框。
三 theorem 不另要求 X full B-touch、第二拒絕列或T4。

| 本題已推導條件 | t0 | t1 | t2 |
| --- | --- | --- | --- |
| actual spokes | 0 | 唯一原spoke | 兩原β異色spokes，位置任意 |
| sole C 的互異contacts | 5 | 4 | 3 |
| 同一C完整F_C | Col，四個拒絕pin lists | spoke色的補集，三個拒絕pin lists | 兩spoke色的補集，兩個拒絕pin lists |
| 額外外部連通 | 不要求C外s–B路；允许K4 | B∪{s}由原spoke連通 | K5最後邻接由原spoke給；不借特定六環 |
| 原 theorem | no-spoke §4 | single-spoke-four §1–5 | two-spoke-three-contacts §1–5，尤其§5 |

**T0：** 四拒絕lists在同一原C上tight。接點的框附件若有色d，pin d时出现slack，
故接點無框附件，lists差只在全部五contacts上。block incidence矩陣欄独立由leaf私有點消去；
逐色差的共同係數τ满足Iτ=1_P。四份palettes使positive active block為K4（palette Col−{d}），
negative為bridge（palette {d}），inactive任意保留。contacts恰為active forest葉；
其他active vertex degree2，block nodes degree4/2。h份非空trees及k個K4給
`|P|=2h+2k`，与5矛盾。此处保留K4，未循環使用多分量K4-free或杜撰C外s–B路。

**T1：** 一條原spoke使外部B∪{s}連通，connected-exterior K4引理可用：
四clique點各留一个外接方向，非direct方向是独立bridge支枝；無外touch支枝能全局换色，
不能維持拒絕singleton端色。四原tethers与该連通外袋給K5，排K4。
三份拒絕palettes共用τ；positive不能bridge，四葉active forest恰兩positive triangles及單negative bridge。
左triangle三點完整degree4各留一邊：直達B，或進入無contact inactive旁支。
旁支不碰B则主側有slack、旁支全四色可染并整體置換接回，違拒絕。因此三原tethers存在，
內部互斥、避active結構和s。袋 `{a},{b},{x},{s,c,d,y},B∪tethers內部` 互斥连通；
triangle、contacts、bridge、tether首邊给九邻接，唯一原spoke给最後一對，得K5。
允許任意大旁支；不靠有限minor skeleton枚舉。

**T2：** 兩完整lists的差在三原contacts恰相反兩色indicator。欄独立給active blocks；
contact degree1、非contact degree0/2、原block incidence森林恰三葉，迫一triangle加三bridge arms。
长可任意，含零长；每triangle點完整degree4留一個额外方向，其無contact inactive旁支若不碰B，
同樣slack及全局换色能接回拒絕lists。因此三實際tethers存在且避arms。
`{s}`、三份triangle＋完整arm袋、`B∪tethers內部`给十对真邻接；零臂保留原s-contact边。
原文§5明列任意兩個不同β色spokes，證明只共同改色名，沒有重排框位置或要求相邻。
§1的b0,b1六環是初始表記，不是未滿足的額外前提。

三claims成立；依賴BASE任意大小paper與外部Gallai，而非本輪工具PASS。

## 7. 11 項裁決、覆蓋與 finding

| CLAIM | 裁決 | 最關鍵充分前提／独立證明入口 | 新block |
| --- | --- | --- | --- |
| N45-SS-COST | 成立 | 原witness、fullB、one-sided與原shield互斥；§3 | 無 |
| N45-SS-UNTOP | 成立 | 原H−U連通、原面、σ_U≠B、整U刪除；§3 | 無 |
| N45-SS-U3 | 成立 | 两不同未接原內點、全部T4；§3 | 無 |
| N45-SS-U2 | 成立 | 唯一未接原內點、全部T4及拒β；§3 | 無 |
| N45-SS-X-CORE | 成立 | X=M自身minimality及完整原邊分拆；§4 | 無 |
| N45-SS-COMPONENT | 成立 | 真實sole C、全部full assignments與單坐標shared vertex；§4 | 無 |
| N45-SS-SPOKES | 成立 | X自身minimal、β=q_m、非空slack及刪每spoke witness；§5 | 無 |
| N45-SS-T0 | 成立 | sole C五contacts／F_C=Col；BASE§4無外路前提；§6 | 無 |
| N45-SS-T1 | 成立 | 原spoke／sole C四contacts／三拒絕完整lists；§6 | 無 |
| N45-SS-T2 | 成立 | 三contacts／兩拒絕完整lists／任意異色原spokes；§6 | 無 |
| N45-SS-EXCLUSION | 成立 | 三盾費身份及t_s=0/1/2窮盡，全數反證；§3–6 | 無 |

SSA-F01：原盾弧長3的第二內點和長3四點support均完整處理；没有偷搬LP三點前提。
SSA-F02：X=M、degree、sole C及F_C精確都是推導鏈必要環節；不能删成一般整U derivative。
SSA-F03：933 q2、whole-frame/root swap与原shared单坐標都保留。
SSA-F04：本輪無finite SS source測試，未計trigger，不宣稱not-triggered等於排除。
旧PC/PCA的19N2、7整U及4N1只保既有LP calibration語境，不能改標SS coverage。
SSA-F05：artifact checker只核bytes／结构；BASE與外部信任保留，沒有新Lean／source realization。
未建立本契約中的source反例或新paper gap；不把缺正控制說成已有數學反例。

## 8. 限定父身份覆蓋

父量詞只取 [authority §1](frozen/current/docs/c5_excess_two_nonadjacent_unit_core45.md) 的 **U 身份**：
任意大小有限simple原disk G、induced C5有序外框、完整Σ933/941或整圖D5像、非框Σ-critical、
ε2、有效H連通／原fullB-touch；两原非相鄰degree5 roots、其餘原degree4；
H−roots恰兩完整mixed，其餘unary、所有pieces one-sided／support非空。
省略完整原unary U且唯一root-contact rx，`X=G−V(U)=M` 是原拒絕literalβ的
inclusion-minimal45/54 core；所有outside原邊與完整同源資料保留。
這与原U§1及SU-A§2共同前提一致；不包含S-spoke省略身份。

1. U存在；BASE A給原unary總數≤2。原U§6／SU-A U-U2的前提是該精確整U身份、
   另有两原unaries；只省略者contact incidence=1，另一份可任意。因此排两份後恰唯一U。
   不是把這個排除移到所有一般unary圖。
2. 两mixed support的short/long是互斥、窮盡分類。兩short由原U§7／SU-A U-SHORT排：
   X無其他unary、β三色未用D避原spokes、原兩short完整(D,D) lifts能共同接回X。
   兩long由原U與两mixed各原費≥2及互斥給6>5。故恰long L＋short S。
3. S actual support非空且short，故只能singleton或真框邊的**恰兩端**，沒有第三支。
   Pair支援時原U-RES給shield=(2,2,1)、U/L各連續三點、五邊全分割。
   父的全部原前提、唯一U、X=M及完整原資料恰滿PA§2与LP採納§2，故已採納LP排這支。
   沒有要求任選新的r/s assignment或用PG單頂點S排除替代LP。
4. Singleton支援時原U-S3的≤3總incidence排除适用：原mixed complete degree4、one-sided、
   fullB-touch和自身Σ-critical contact witness全部具備；故其總incidence≥4。
   原U-RES亦明列此必要式；正兩側incidences、原degree等式及其餘SS充分前提全由父原身份保留。
   因而精確落入本次完整SS契約，由N45-SS-EXCLUSION排除。

**限定合成 corollary 成立：在上述 authority §1 的完整 U 原身份中，不存在整U省略
X=M、unique root-contact、保兩原mixed的原source。** 没有额外未覆蓋支；
block=false。此corollary沿用已採納U-U2／U-SHORT／U-RES／U-S3／LP的trust，
加本次SS；它不宣稱本輪重新證完所有已採納依賴。
本稿只提供独立覆蓋核對，正式採納及共享父摘要修改由監督處理。

仍未涵蓋：S LOW／HIGH／long、原55、其他cores、不等於M的整U derivatives、
非unit unary省略、沒有45／54身份的來源、一般N2／E、ε≥3、source realization、
指定coloring repair、一般validator soundness、Lean或remote CI。

## 9. 實際檢查與封存

[checks.json](checks.json) 及 logs/ 記每個實際命令argv／exit／stdout／stderr。
Git BASE reads与blob OIDs、PDF文字抽取實際執行；独立標準庫
[review.py](review.py) 正常與seed17核凍結輸入、candidate自身exact manifest inventory、
完整claim inventory、本稿本地links／JSON／Python語法与新文本格式。
這些没有檢驗任意大小數學定理、運行PC LP checker、source搜尋或Lean。

本輪normal／seed17均實際exit0，stdout逐byte相等；結果保存在
[artifact-review.json](artifact-review.json)。核回24個BASE Git objects、23個current-work inputs、
11項claim metadata、worker 6096項payload及5項postseal metadata的exact inventory／hash。
另有一個非依賴历史BASE缺檔probe实际exit128，未轉稱PASS；tracked/index diff與接手時相同。

原worker verify.py有全工作樹inventory前提；本稿只讀其程式，沒有在新增audit後直接執行它，
也沒有把根在新增audit前回報的normal/seed17 exit0算本稽核新PASS。
独立review.py的candidate manifest只查worker自身payload，允許其他新audit；
因此不把本輪外部新增目錄誤認為worker漂移。

历史E4 provenance／byte replay FAIL、fresh BASE历史缺檔、whole-worktree DocGraph duplicate IDs
依原報告語境保留；本輪没有重跑它們或改成PASS。
正式docs/full-tree檢查本輪未執行，不借其他輪結果冒稱本輪成功。

裁決先封存为 [independent-judgment.json](independent-judgment.json)，再完成本目錄
[MANIFEST](MANIFEST.sha256)／[delivery](delivery.json) exact regular inventory與hash封存後返回。
manifest排除其自身及delivery，以避免自引用；delivery綁manifest／REPORT／裁決hash及完整檔案清單。
所有裁決以凍結版本為準。
