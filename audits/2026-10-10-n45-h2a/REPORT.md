# N45-H2A：HIGH2 十二項紙面裁決與限定 HIGH 條件式覆蓋

2026-10-10。BASE `dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。
**HIGH2 無界來源排除成立於 worker 完整 H1–H13，仍為待監督採納候選。**
十二項 claims 逐項核回，無新增 source 充分前提、無數學 source-proof gap。
一項具名量詞精化：EXCLUSION 的 `r=s=Dγ` 構造明限 proper 三色 γ；
JOIN／RESTORE／PALETTE 仍量化所有 proper γ。詳細見§5。
限定 HIGH 三支覆蓋僅為 conditional scoped composition，不自行採納。

交付：[獨立裁決](independent-judgment.json)、[原 tree 初核](initial-intake-check.json)、
[41 inputs／8 pins](input-index.json)、[独立位置／列算術](independent-arithmetic.json)、
[只讀 verifier](verifier.py)、[manifest](manifest.json)、[delivery](delivery.json)。
原 HIGH2 [REPORT](frozen/audits/2026-10-10-n45-s-high2/REPORT.md)、
[claims](frozen/audits/2026-10-10-n45-s-high2/claims.json)及
[正式任務全文](frozen/audits/2026-10-10-n45-s-high2/frozen/current/audits/2026-10-10-n45-high1-supervision/high2-task-body.txt)
逐字保留。以下 Hn 都指其完整十三項 source 契約；每 claim 量化任意有限大小 G。
未讀 H2R／H2C 的判斷取代本稽核。

## 1. 完整凍結與 custody 的不同範圍

專屬目录 exclusive-create。先核 intake 的四棵指定 live／manager frozen worker tree
之 exact file set、每檔 bytes／mode／SHA256，再完整複製至本目錄，所有 mode 保留。
HIGH2 118、H3A 30、H3R 28、H3G 30 regular，合計206，零差異／零 symlinks。
五個 named shared intake hashes 亦吻合；沒有全工作樹 inventory。
HIGH2 原交付的 115 payload＋3 top-level metadata=118 regular 不變；
在本稽核內這118份全部是 nested immutable payload，不再排除其 manifest/delivery/receipt。

41 個 inputs（22 BASE blobs／19 current）、八個 dispatch pins 全核原 bytes，
本 frozen／live／`git show BASE:path` 零漂移。同期其他 audit 新增不在 named input 域。
原 outside custody exit1、generation mapping exit2、本地 link 首次 FAIL、
DocGraph 62 duplicates、BASE historical missing paths、E4 provenance FAIL 均完整保留，
沒有用 named input 通過將其改成 whole-worktree custody PASS。

## 2. CORE／COMP／JOIN／RESTORE／F 的逐原邊核對

H2-CORE：H9/H11 只刪 rb_i，所以 H_X=H_G、有效 H 仍連通。
r 原3 mixed+2 spokes降為完整4；s 原2 mixed+2 U+1 spoke仍完整5；
其餘有效原內點完整4。原孤立 I 不變，其每個完整 lift 保同一 `Col^I` 因子。
H10 單獨給 X 自己每非框邊 f 的完整 β-lift of X−f，不從 G criticality 遺傳。
X 為保原 B 的 disk 子圖；Σ(G)⊆Σ(X) 給 inherited T4。

H2-COMP：H5/H7/H8 給 H_X−s 的 exact components C={r}∪P∪Q、U。
P/Q 各連通且各對 r 正 incidence，使 C 連通；U 只接 s，無 U–r。
C 的三條 r contacts 和 retained rb_j 全留；s contacts為 yP/yQ 與 x1/x2。
不同 piece 的接點不合併，shared r/s contact仍是原同一變量；
保四 contact 總 rotation及兩 ordered sublists。原 x1–x2 路及 s 的 cycle 沒有刪除。

H2-JOIN：對每 proper γ、所有 ambient t/u∈Col²、r pin c、s pin a，
用完整 Fib_C(γ,t,c)、Fib_U(γ,u)；支援外仍是空 fibre。
同一 a 避四 contact 坐標、a≠γ(b_k)、c≠γ(b_j)，加 I 的任意 assignments，
與 X 全 lifts restriction／union 雙射。P/Q 也只在同一 r=c 的完整 assignments 接合。
H2-RESTORE：G 正是這份完整資料另加 c≠γ(b_i) 的子集；不能丟 r 投影。
這兩項包括四色 γ、所有十 canonical cells、所有 pins及空 queries。

H2-F：每 γ 下 R_C/R_U 非空，由接點不扣 s 色時的 strict slack；容量各≤2。
R10 分量解除引理在 X 上逐 incident edge 適用，橋刪後兩側各有 slack。
X 的 β-minimal witnesses給 A=Col\{c0}、F_C∪F_U=A及兩份 private colors；
刪唯一 s-spoke 的 witness迫 c0不在任一 F。
BASE E4 §4.1 是局部 N(C) 版本，量化每 proper γ及每同色 root pin a，
**不需已有完整外部 coloring**。對 a≠γ(b_j) 置原 r=s=a，
P/Q 全 contacts同時避 a；故 F_C(γ)⊆{γ(b_j)}。
在 β 令 a0=β(b_j)、c0=β(b_k)，private cover迫 a0≠c0、
F_C={a0}、F_U=Col\{a0,c0}={D,h}。原 U 完整二元 R 恰兩交換 tuples；
逐刪 sx1/sx2 的解除 witnesses 各供一個方向，不能只留單向 pair。

BASE 精確依賴：`docs/c5_degree5_interfaces.md` §§1–4、
`docs/c5_weak_list_cores.md` §1、`artifacts/c5_excess_two_e4/REPORT.md` §4.1。

## 3. K33／ARC：先取得 U 盾下界，再核例外共端

H2-K33：原 sxν Σ-critical 釋放某 proper 列 δ及完整 Lift(G−sxν)。
它在 s/xν 等色，限制到 G−U 仍保原 e及全部其他原邊。
若 U 可同時避該 s 色，就能接回 G，矛盾；故原 U 有非空 forbidden query。
H−U={r,s}∪P∪Q 原連通、full B-touch，恰滿 BASE shield 定理 A 的來源前提。
其短支援反證可用 H−U 中到 B 外點的原外路，得到 |σ_U|≥2、|S_U|≥3。
這一步發生在原 G，尚未假设 P/Q 支援頂點互斥。

兩 mixed 原 one-sided；shield 引理1/2使其真框邊 pair恰各佔一条互斥盾邊。
若共端 v，P、Q、O=B−v 與 {r},{s},{v} 為六 bags。
b_k≠v 時 O–s 用原 sole spoke；b_k=v 時改 O′=(B−v)∪U，
因 S_U至少三點，可選原 U–b_h 附件 h≠v，故 O′ connected，O′–s 用原 sx1。
六 bags互斥；九鄰接來自四 root contacts、兩 actual v附件、O–v框邊、
原 r兩個不同spokes之一及上述 s 邊。r–O 可使用省略 e，因 minor在原 G。
這給原 K₃,₃，矛盾平面性；沒有替 s 假造第二 spoke。

H2-ARC：P/Q 支援框邊因此頂點互斥，剩三条框邊分成長2、長1兩段。
U 的盾連續、≥2、與兩 mixed盾邊互斥，恰佔長2段；
full B-touch的支援引理迫 actual S_U=T={b_L,b_m,b_R}。
H−U及所有 roots spokes避 b_m。P/Q四支援端點恰 B−{b_m}，
加 retained r-spoke仍得 S_C=B−{b_m}；C實際碰 T外兩點。

BASE：`docs/c5_unary_shield_budget.md` §2引理1/2、§3定理A；
`docs/c5_short_support_singleton.md` §4與 connected-exterior K4/Gallai為其明列信任依賴。
原 bags只證非平面，沒有改 coloring source。

## 4. MAP／BRIDGE／SPLIT：真正前提與任意大小 W

H2-MAP：共同整圖 D5/S4將 β搬為 q=01012，X自己滿 BASE
single-spoke (2,2) §1：unique完整degree5 s、sole spoke、兩actual二接點分量、
其他degree4、effective H connected、edge-minimal q/disk及T4。
原 C/U 的角色確為 (1,2)，完整 ordered identity保留。
slit-cut必有一分量的實際 support lifts整區塊先於另一份；無此 placement就是
BASE crosscut source exclusion。有 necessary record只記 identity／query，不證 source存在。

獨立由 q、T三連點二色、spokes避中點及 a0≠c0 重算全部8個位置。
4個無 slit placement；另外4個對回凍結 record90／511，支持／禁色／lifts逐項相同。
兩 record 的全部 contact words是 necessary允許方向，實際 rotation必落其中。
原 generation失敗把無placement強求表項，原 checker-v1及FAIL全保留。
BASE cross-row／two-arc／first-bridge／locality 的指定 p1/p2延拓只屬 X，
没有用它們代替 G 的 retained r fibres或恢复 e條件。

H2-BRIDGE：同一 β 的兩個拒絕 pins D,h先給 U 的 tight degree lists與Gallai palettes。
B∪{s}經 sole spoke連通，連通外框 K4排除適用。
BASE (2,2) §3 的雙禁色差沿原 block tree給 x1–x2唯一原 bridge路徑、奇數長ℓ≥1。
刪路徑邊只定義 Wν：各路徑點的**全部**原連通旁支塊，互斥並覆蓋 U。
每W的非root lists在兩拒絕證書相同；rooted palette唯一性給同一旁支聯集 Qν。
root直接boundary colors Dν及Qν滿 `Dν∪Qν=Col\{D,h}`。
逐色固定 β(Tν) 的置換必保 residual；交換任何缺席 a0/c0與未用D，會改 residual。
故每 W實際見 a0/c0，不能把這個 residual直接稱為 rooted assignment palette。

H2-SPLIT：若任意 W_i/W_j共同接兩框點 a,b，取 C內原 s–B 外路 L落到 T外的 t。
L內點避 U/B。三個具名標記点在C5上給非空不交連通 frame arcs X_a/X_b/D_t，
且三對框弧各有原切口邊。
對 i<j，A=⋃W_i…W_(j−1)、A′=W_j、
Z=(J−{z_i,…,z_j})∪L∪D_t。五袋連通、互斥；
A–A′用最後bridge，A/A′–Z用兩cycle邊，四條W附件及三框切口給餘七鄰接。
非相鄰 W也適用，中間全部W納A；无需兩條外路，無旁支大小限制。

若 β(T)三色，a0/c0各唯一供應點，任何兩 W共享兩點即K₅；故 β(T)二色。
proper三點框路只可能兩端同色、中點另一色。每W必碰中點及一外端；
≥3份W必兩份共享外端，仍K₅。因此恰兩W、ℓ=1。
任一W若接兩外端也與另一W共享，矛盾；所以 actual supports恰左右真框邊pair。
這是一條原 bridge分割成兩任意大小W，沒有兩內點正常形或部分U刪除。

BASE：`docs/c5_single_spoke_two_two.md` §§1–3；
`docs/c5_single_spoke_two_two_minor.md` §2；
`docs/c5_single_spoke_branch_palettes.md` §2；
`docs/c5_single_spoke_frame_arc.md` §§1–3及
`docs/c5_single_spoke_two_two_external.md` §§1–2。
Gallai Lemma7／Theorem10為外部数学 trust，非Python／Lean定理。

## 5. PALETTE／EXCLUSION：完整 assignments與具名量詞精化

H2-PALETTE：K_W(γ,c)定義整份 W的全部原assignment，所有原框附件全留；
兩W僅以原 bridge root inequality接合，與原U assignments restriction／union雙射。
β下 R_U两交换tuples各提供兩root色D/h。
若任一W另有色c∉{D,h}，與另W已存在的rootD assignment接合，就有tuple(c,D)，
不含h，矛盾完整FU；因此兩 rooted可取色集恰{D,h}，**由完整factor而非 residual推得**。

每 actual support恰真框邊pair，其 β/γ色都互異。一次全資料 S4映 β的該pair色到γ的pair色，
對全部原 W assignments給雙射；其他框值無W附件，故不影響該query constraints。
這是固定來源 W的完整關係等變性證明，不把W各自改成不同來源／獨立normalize。
最終在同一原γ及同一原bridge接合完整 K_W，保所有ambient空／非空fibres。
故每 proper γ（含四色）兩 rooted色支援分別是其actual pair二色補集，
R_U恰全部左右root palette的異色pairs，所有full lifts照留。

H2-EXCLUSION：對每 **proper三色 γ**，若 γ(T)三色，取完整 W_L/W_R assignments，
roots分別 γ(b_R)、γ(b_L)。兩色互異；以γ唯一未用色Dγ置原r=s=Dγ，
P/Q N-diagonal供全部原assignments；U contacts避Dγ，原spokes包含恢复e全合法。
union含任意 I assignments，就是原 G full lift，明确有 r=Dγ≠γ(b_i)。
proper三色C5 singleton k∈T iff γ(T)三色。因此 Q(G)⊆B−T，最多兩點；
933的四拒點（含q2）、941三拒點及所有整圖D5像都矛盾。

**Finding H2A-QDOMAIN-01（query-domain clarification，無新增 source 前提）。**
worker `claims.json` H2-EXCLUSION與REPORT§8的「每γ在T見三色，令Dγ為未用色」
需把此構造的γ明限三色。例γ=01231、T={0,1,2}是proper四色，T見三色但沒有未用Dγ。
這是scalar反例，非HIGH2 source反例。四色列的原G full lift已由H2/T4接受保證；
它們不需要、也不能宣稱使用同一未用Dγ構造。JOIN/RESTORE/PALETTE的全部properγ量詞保留。
故來源排除及Q(G)界本身成立，原兩處construction表述需監督採納時保這項精化。
`new_source_sufficient_hypotheses=[]`；不是添一個圖類假設來補paper。

## 6. 限定 HIGH 的 conditional scoped composition

僅取凍結權威§1精確原spoke省略 S身份的 **S-SHORT-U-HIGH**，保全部共同source契約：
唯一原U只接s、兩原mixed actual支援真框邊pair、incidence(3,2)、原兩非相鄰degree5 roots，
只省略r原spoke e、X=G−e=M自己β-minimal45/54，其餘原圖及full資料全留。
所有completeΣ／criticality／ε2、H連通／full B-touch、one-sided及K/H12–13也必逐項保留。

令 u是原U incidence，t_s是原s-spokes。s degree5扣两mixed contacts给 u+t_s=3；
unary使u≥1、t_s≥0。原r无U且mixed3、degree5，故恰两spokes，正合三支r-spoke契約。

| (u,t_s) | 精確映射 | 保留的全契約 |
| --- | --- | --- |
| (1,2) | 已採HIGH1 | frozen HIGH1 H1–H13；U唯一sx、s兩spokes |
| (2,1) | 本HIGH2候選 | worker H1–H13；U兩不同contacts、s唯一spoke |
| (3,0) | frozen HIGH3候選 | H3A/H3R/H3G共同K1–K13；三不同contacts、s無spoke |

K/H1–6與8、10–13逐項同一source；只有7的u與9的t_s依此三分變化。
有限簡單圖保contacts相異；共同root swap先固定降度r，不另行換piece身份。
三分互斥且窮盡，不遗漏u=3、933 q2或共同D5/S4/root orbits。

HIGH3只讀本 intake凍結 [H3A](frozen/audits/2026-10-10-n45-h3a/independent-judgment.json)、
[H3R](frozen/audits/2026-10-10-n45-h3r/independent-judgment.json)、
[H3G](frozen/audits/2026-10-10-n45-h3g/independent-judgment.json)及共同K1–K13。
其scope均恰(3,0)、無新增充分前提；BASE no-spoke(3,2)排除不借HIGH2推導。
因此 **若監督採納本完整HIGH2與凍結完整HIGH3**，既有HIGH1加這兩支就排精確
S-SHORT-U-HIGH。這只是conditional composition；沒有自行採納任何分支。
全部S、long、原55、其他cores／非M derivatives、一般N2／E與核心存在性不由此關閉。

## 7. 證據分層、只讀重播與精確停止點

paper：十二claims的無界推導由上列原邊／block-tree／frame-arc／full-lift證明承擔。
external：官方Dvořák [Lemma7／Theorem10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
原文已核；本 worker frozen PDF hash `50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea`保留。
BASE paper與外部 theorem並未因hash或工具PASS變成Lean。
抽象控制：8個mapping／600三色singleton checks／100 D5拒集checks為triggered and holds；
QDOMAIN過寬construction量詞為scalar counterexample，不是來源反例。
未建立／未執行finite HIGH2 source，`trigger_count=null`、status `not triggered`；
原toy／schema只校準完整join與具名bags；本稽核不重播其無關枚舉或把toy當source。
source realization未建立、沒有新Lean、lake/global DocGraph未跑。

只讀封存命令實際 normal/seed17各exit0，stdout byte一致、stderr空：

```sh
python3 -B audits/2026-10-10-n45-h2a/verifier.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-10-n45-h2a/verifier.py --check
```

實際 streams／exit／verifier與manifest hash綁定見 [normal](receipt-normal.json)、
[seed17](receipt-seed17.json)。錯artifact負控制從stdin傳漏列nested原worker receipt的manifest，
真正在 immutable payload inventory階段exit2，見 [負控制收據](receipt-negative.json)。
不覆寫任何原Fail或證書，nested同名檔全部payload；只排exact top-level本輪metadata並逐hash綁。
封存前後原worker bytes/modes不變，named inputs零漂移。
本新REPORT local link targets及新文本whitespace核回；frozen歷史原文links保原bytes。
精確停止於候選紙面＋條件覆蓋交付；量詞精化、獨立採納及共享文件傳播留父端。
