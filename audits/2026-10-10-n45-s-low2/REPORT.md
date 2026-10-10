# N45-S-LOW2：雙原 U-contact 全保留的三接點排除候選

2026-10-10。BASE／執行 HEAD：`dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。
任務見 [task](task.md)，八個 current-work pins及額外只讀 inputs見
[inputs](inputs-initial.json)，四個獨立 Git-object inputs見 [BASE inputs](base-inputs.json)。

**結論：完整 LOW2 契約內的任意大小來源不存在；這是待獨立採納的 paper 候選。**
原 U 的兩條 `rx1,rx2` 全保留。只刪 r 的唯一原 spoke `e=rb_i`，得到自身
β-minimal 的 X；r 在 X 無 spoke、完整 degree4，s 為唯一完整 degree5。
實際 `C=H_X−s` 仍唯一連通，有原三 s-contacts及兩条異色 s-spokes。
完整 joint／精確 F 接回 BASE 三接點排除，K₅ 十對鄰接全部使用 X 的保留原邊。
沒有把 LOW1 的單 contact 身份直接搬來當 LOW2 已證，也沒有刪 U。

## 1. 完整來源契約、量詞及依賴

以下每個 claim 均量化任意大小有限簡單 disk 原圖 G、有序 induced 外框
B=(b0,…,b4)、原 spoke e、原拒絕 literal β，以及指定 `X=G−e=M`。
完整契約逐項是：

1. B 是 G 的外面；原 rotation、每條實際原邊和全部原附件固定。
2. 完整有序 Σ(G)=933／941，或其一次共同整圖 D₅ 像；每條非框邊 Σ-critical，ε(G)=2。
3. 有效原 H 忽略原孤立內點，連通且 full B-touch；被忽略的孤立點只提供自由 lift 因子。
4. 恰兩個非相鄰原完整 degree5 roots r,s；其他有效原內點完整 degree4。
5. `H−{r,s}` 的完整原分量恰唯一 unary U及 mixed P,Q；三份 connected、one-sided、actual support 非空。
6. LOW2 的 U只接 r，全部原 contact恰 `rx1,rx2`，x1≠x2，沒有 U–s 邊；U整份保留。
7. P/Q各支援恰一條真原框邊的兩端，每側 incidence皆正；保其具名身份及所有 actual attachments。
8. mixed總原 incidence `(m_r,m_s)=(2,3)`：r對P/Q各一，s的分配為1與2。r唯一原spoke是e，s原有兩spokes。
9. β是原拒絕 literal row；X=M自己為β inclusion-minimal45／54 core。一次共同 root swap只命名降度側r。
10. 唯一省略e；全部U/P/Q頂點、內邊、rootcontacts、框附件、其餘spokes均保留；無新邊、替換或收縮。
11. 原named／ordered／shared contacts單一坐標，actual support／ownership、bridges／rotation、共同literal四色框、全十列relations、空與非空fibres及全部full lifts保留。
12. D₅／S₄／root swap只共同作用整圖和全部資料；canonical933的q2照留；不假設β是U盾中點列。

量詞沒有內點數或臂長上界。JOIN另逐每個proper literal γ、每個r／s pin與全ambient
`Col³` contact tuple成立。逐claim完整契約與依賴均寫入 [claims](claims.json)。
契約內的原Σ／criticality／one-sided／short是固定來源身份；下面不藉它們取代X自己的minimality。

| 依賴 | 本輪使用及證據界線 |
| --- | --- |
| [BASE R10](frozen/BASE/docs/c5_degree5_interfaces.md) §1–4 | 完整contact介面與degree-list語義；本輪以LOW2原邊重證C及F |
| [BASE三接點](frozen/BASE/docs/c5_two_spoke_three_contacts.md) §§1–5 | active triangle、任意／零長arms、inactive branch實際boundary tethers、原K₅ bags；§5涵蓋任意兩個異色spoke位置 |
| [BASE list-critical](frozen/BASE/docs/c5_weak_list_cores.md) §1 | minimality的同色spoke冗餘；§5另給直接刪邊證明 |
| [官方Dvořák講義](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf) Lemma7／Theorem10 | 外部degree-list定理；不是本輪Python或Lean證明 |
| [S舊交付](frozen/current/audits/2026-10-09-n45-s/REPORT.md)、[SU-A](frozen/current/audits/2026-10-09-n45-su-a/independent-judgment.json) | 已採納的LOW必要身份參照；不代替LOW2推導 |
| [LOW1](frozen/current/audits/2026-10-10-n45-s-low1/REPORT.md)、[L1A](frozen/current/audits/2026-10-10-n45-l1a/independent-judgment.json)、[L1R](frozen/current/audits/2026-10-10-n45-l1r/independent-judgment.json) | 已核論證的參照；兩原U-contact及r無spoke仍由本輪重證 |

八個指定pins核對吻合，current-work與BASE層分開。官方PDF與BASE PDF byte相同，
見 [external source](external/source.json)及 [PDF文字](logs/gallai-text.stdout.log)。
外部陳述及證明已讀取，沒有把講義當本地形式化成果。

## 2. LOW2-CORE：逐原邊degree及X自己的minimality

**前提：** §1全部契約。**層：** 任意大小paper。
e只碰r與B，所以有效內點誘導邊完全不變：`H_X=H_G`。

| 點 | 原G全部incident edges | X全部保留incident edges |
| --- | --- | --- |
| r | rx1、rx2、對P一contact、對Q一contact、rb_i：degree5 | 前四條原邊全留，degree4；boundary degree0 |
| s | 三條mixed contacts、兩條原spokes：degree5 | 五條全留；rs原不存在 |
| 每個U／P／Q有效點 | 原內邊、rootcontacts及actual框附件合計degree4 | 沒有incident edge被刪，完整degree4 |
| B | induced C₅及全部原附件 | 只少rb_i；C₅及其順序保留 |

X是原disk子圖，rotation僅刪e的dart，不重新選embedding。X唯一完整degree5內點為s，
自身有效ε=1，沒有新有效孤立點。**完整degree是在X量測，並非deg_C。**

X的β-minimality由`X=M`本身提供，沒有從原G的Σ-criticality推給derivative。
對每條X非框邊h，X−h必有完整β-lift，否則仍拒β的真子圖違反minimality。
刪邊與後續witness均在此同一X上，不借用G−h的其他列。

## 3. LOW2-COMP：實際sole C及原三contacts

**前提：** §1及CORE。**層：** 原圖paper。

`V(C)={r} ⊔ V(U) ⊔ V(P) ⊔ V(Q)`，且完整邊清單為

`E(C)=E_G(U) ⊔ E_G(P) ⊔ E_G(Q) ⊔ {rx1,rx2,rp_r,rq_r}`。

p_r及q_r是原r在P及Q的唯一具名neighbor。三個原分量互斥、各自connected，且各接入r；
U的兩contacts共同接到同一r。因此Cconnected且沒有其他有效分量。
U兩contact若在U內由長路相連，該路與兩原r邊都留在C；沒有將它改成LOW1的bridge。

令有序K=(p1,p2,p3)是s原rotation刪去兩個B-neighbors後的繼承清單。
此清單由原P/Q contacts給出，不為論證交換P/Q身份；簡單性使三個neighbor互異。
r及U均不在K。若p_r或q_r也在K，那就是同一原點、同一變數，同時承受r與s邊約束。
bridges／cut vertices保原身份；此處只命名X中的集合，没有收縮、換附件或刪原piece。

對v∈C，令d_B(v)=|N_B^X(v)|，則逐原邊有

`deg_C(v)=4−d_B(v)−1_[v∈K]`。

尤其r沒有boundary或s鄰居，`deg_C(r)=4`；U點沒有s-contact。
其餘點的deg_C依實際框附件及s-contact計，不一律寫成4。

## 4. LOW2-JOIN：兩原U接點、全ambient fibres及full lifts

**前提：** §1及COMP。**量詞：** 任意proper literal γ，所有pins及assignments。**層：** paper雙射。
設Col={0,1,2,3}。Λ_T(γ)對T=U/P/Q保存全部T頂點assignments，滿足T全部原內邊
及actual boundary attachment不等式；rootcontacts在下面共同接入。
U的contact資料保留ordered pair `(f_U(x1),f_U(x2))`及每個pair的全部fibre。
不能把兩個一維投影相乘，或分別選不同的U colouring。

r在X沒有spoke，故`A_r^X(γ)=Col`。原C的全部lifts恰為

```text
J_γ = { (c,f_U,f_P,f_Q) :
  c∈Col, f_T∈Λ_T(γ) for T=U,P,Q,
  f_U(x1)≠c AND f_U(x2)≠c,
  f_P(p_r)≠c AND f_Q(q_r)≠c }
L_C(γ) = union assignments of members of J_γ, with r=c
Φ_γ(c,t) = { f∈L_C(γ) : f(r)=c, (f(p1),f(p2),f(p3))=t }
Fib_γ(t) = disjoint union over c∈Col of Φ_γ(c,t), for EVERY t∈Col³
R_C(γ) = { t∈Col³ : Fib_γ(t)≠∅ }
L_C(γ;a) = { f∈L_C(γ) : f(pj)≠a for j=1,2,3 }
F_C(γ) = { a∈Col : L_C(γ;a)=∅ }
```

任意C coloring限制到r及三原pieces即給J_γ；反向union因pieces互斥、全部跨piece邊
只有列明的r-contacts而給C coloring。restriction與union逐完整assignment互逆。
shared r/s-contact只有同一個f_T(v)坐標，不拆ports，不獨立換色。
任意pin c只保Φ_γ(c,t)；任意pin a另要求每個t_j≠a。
Col³所有64個ambient tuples的空fibre也保留，不把R_C以外的tuples從fibre定義域刪去。

設s兩原spokes為sb_j,sb_k，`A_s(γ)=Col−{γ(b_j),γ(b_k)}`。
令I是原被忽略的孤立內點。所有X full lifts恰為

```text
for a∈A_s(γ), f∈L_C(γ;a), h∈Col^I:
  B=γ, s=a, C=f, I=h
```

完整G lifts在同一assignment上再加**唯一**原邊條件`f(r)≠γ(b_i)`。
此式逐所有c,a及t成立，包括空fibre；不是只在β寫r≠β(b_i)。
十列及整列S₄搬運都使用相同原資料；D₅連同B labels／attachments／rotation全圖搬運。
933的q2並未去掉。沒有用marginals或自行正規化pieces接成假lift。

**未pin s的完整R_C(γ)非空。** 令`L_γ(v)=Col−γ(N_B^X(v))`。
上節degree式給`|L_γ(v)|≥4−d_B(v)=deg_C(v)+1_[v∈K]`。
三原contacts都strict slack；Cconnected，生成樹由葉到slack根的貪婪法（Lemma7）
給一個完整L_γ-coloring。因此L_C(γ)與R_C(γ)非空；沒有聲稱每個pin或每個tuple有lift。

## 5. LOW2-F：X自己minimality的精確兩色補集

**前提：** §1、CORE及JOIN；只在指定拒絕β使用minimality。**層：** paper。
寫u=β(b_j)、v=β(b_k)。若u=v，刪任一s-spoke不改任何β-list，仍拒β，
違反X自己的minimality。因此u≠v，`A_s(β)=Col−{u,v}`恰兩色。
X拒β與精確full join給`A_s(β)⊆F_C(β)`。

刪sb_j後的完整β-lift必令s=u；否則原sb_j已proper，這份lift也可接回X，矛盾。
限制到完整未改動C便給L_C(β;u)非空。刪sb_k同理給L_C(β;v)非空。
故精確有

`F_C(β)=Col−{u,v}=A_s(β)`，而`R_C(β)≠∅`。

F是完整三contact共同避色查詢，不能反向重建R_C或其fibres。
這裡沒有用U盾中點forcing，也沒有搬SS整U刪除後的未接框點結論。

## 6. LOW2-MAP：BASE §§1–5的充分前提及任意大小抽取

**前提：** §1及CORE／COMP／JOIN／F。**層：** paper、BASE及明列外部定理。

| BASE使用處 | LOW2自己的對應 |
| --- | --- |
| §1有限簡單induced-C₅ disk、minimal q-obstruction | 同一X、原B與rotation限制；β-minimality來自X=M |
| §1唯一完整degree5 z、其他完整degree4 | z=s；r無spoke但有四條保留contact，U/P/Q全邊保留 |
| §1 sole connected C及三個互異原contacts | §3實際頂點／全部邊、s原rotation清單K及shared單坐標 |
| §1完整非空R_C及精確兩色F | §4 strict slack；§5 X−s-spoke完整witness |
| §1–2同一C的兩份degree-lists | 全部actual X boundary lists，兩pin色只作用K，不刪U或r |
| §2完整block／active差／任意長arms | 以下重核整個C的palettes；無cycle長度或臂長上界 |
| §3inactive branch的實際boundary tether | 使用X完整degree及X邊；r沒有框邊不構成額外假設 |
| §4原K₅ bags及root–B edge | s兩spokes保留；十對bag adjacency不用e |
| §5任意兩個異色spoke位置 | u≠v；不要求j,k相鄰或另換attachments |
| §5第二列／T4 | 較強三接點矛盾只需此β；原完整Σ仍在來源契約內 |

留在原β，只用一次共同S₄將u,v命名0,1、其餘兩色命名2,3；B次序和contact資料不變。
BASE §5的論證只使用這兩個spoke色及完整boundary lists，所以不必另要求printed
`q=01012`與相鄰spoke位置，也不必把β singleton移到U盾中點。

對a=2,3設`M_a(v)=L_β(v)−({a} if v∈K else ∅)`。
每個M_a都是degree-assignment且不可染；Lemma7迫全部tight。
在contacts，actual boundary colors互異且避2,3；兩list指示函數差只在K，
為`1_[v∈K](1_[color=3]−1_[color=2])`。
Theorem10给同一C的Gallai blocks與兩組blockwise-uniform palettes。
block-versus-vertex incidence columns以leaf-block私有點逐塊消去而線性獨立。
因此0／1在每塊不變，2／3的變化互為相反；每個active block只交換2↔3。

palette disjointness使同點至多各有一個兩種sign的active block。
三原contacts各active-degree1；非contact為0或2。active incidence forest的block-node
degree至少2，恰三葉；每棵非空tree至少兩葉，因此只有一棵，tree degree identity
迫恰一個三點active block及其餘二點blocks。這就是一個active triangle及三條bridge arms。
arms可任意長、可零長，終點恰三原contacts，除triangle外互斥；inactive blocks仍完整在C。
兩contact的U所產生的真cycle若屬某block，也未被替換成單contactbridge。

每個triangle點v_i有兩triangle邊，加一arm首邊；零長arm時第三邊是原s-contact。
X中完整degree4恰剩一條actual邊。它是直接B附件，或bridge进入inactive branch W_i；
block-cut tree禁止其重接active structure。所有s-contacts已在active structure，故W_i無s-contact，
不同W_i互斥。若W_i在X不碰B，connected C−W_i在v_i獲strict slack、可染M_2；
W_i內entry degree3、其餘點degree4且沒有B或s constraints，四色slack貪婪可染。
對這整份無外部pin的W_i coloring共同換色使bridge兩端異色，即延拓拒絕的M_2，矛盾。
故每個W_i真有X boundary attachment。這一步即使W_i包含r也只用X邊；
沒有以被省略rb_i冒充tether，沒有在relation資料中獨立正規化U/P/Q。

選三條actual tethers，內部互斥且避active structure，endpoint可在B重合。
令Z={s}，V_i為v_i及其全部原arm，O為整個原B及三tethers內點。
五bags非空、connected、pairwise disjoint。全部十對原邊鄰接是：

| pairs | X中的實際原邊見證 |
| --- | --- |
| V0–V1、V0–V2、V1–V2 | 三條active triangle邊 |
| Z–V0、Z–V1、Z–V2 | 三條原s-contact邊 |
| V0–O、V1–O、V2–O | 三條actual tether各自離開V_i的原邊 |
| Z–O | 保留的sb_j（sb_k也可） |

零長arm仍有原sv_i；任意長arm都在其V_i內。O用原C₅保連通，沒有新增框邊。
因此K₅是X原邊上的minor，違反原disk平面性。B僅作最終minor bag，沒有當保染色replacement。

## 7. LOW2-EXCLUSION、coverage及停止點

對每個滿足§1完整LOW2契約的(G,e,β,X)，§2–6給矛盾，故該任意大小來源族為空。
六claims均為新paper候選，**本執行者未自行採納LOW2或整LOW**。
沒有新數學gap finding；後續獨立review仍應核完整契約、新圖類映射與外部trust。

| 證據層 | 本輪狀態 |
| --- | --- |
| 任意大小paper | LOW2-CORE／COMP／JOIN／F／MAP／EXCLUSION；待獨立採納 |
| 外部信任 | BASE §§1–5、R10／list-critical、Dvořák Lemma7／Theorem10及K₅非平面性 |
| 新有限source control | **未建立、未執行，沒有trigger數**；未作LOW2 source search |
| 工具控制 | 只核封存、pins、bytes、workspace、links與負控制；不是任意大小數學證明 |
| source realization／來源counterexample | 未建立；沒有新的具名來源 |
| Lean／一般N2／E | 無新Lean，未跑lake build／axioms；一般N2／E維持OPEN |

不存在本輪finite source evaluation，故不寫source觸發為0，也不把缺正控制當來源排除。
沒有重開已採納U／LP／SS／LOW1，不用PC的LP schema充LOW2控制。

## 8. 實跑驗證、既存FAIL及只讀封存

[checks](checks.json)保存每條文件命令的cwd／stdout／stderr／exit。
[receipt](receipt.json)保存normal／seed17及六工具負控制的實際命令與拒絕階段；
[delivery](delivery.json)精確綁定receipt和 [MANIFEST](MANIFEST.sha256)。
payload含巢狀的舊delivery／manifest及receipt commands。只有本頂層manifest／delivery／receipt
及逐名列出的16份receipt logs排除，沒有basename或整目錄排除。
失敗若發生須保其完整封存並另開版本；不得覆寫既存sealed檔案。

| 文件／來源檢查 | 實際範圍 |
| --- | --- |
| HEAD、八pins、四BASE blobs | 與凍結inputs核回；current與BASE不混用 |
| current check_docs及正式docs DocGraph | 各exit0；592 Markdown／7,131 local links；62正式documents／213 relations |
| 既存LOW1 BASE checkout只讀check_docs | exit1，恰兩歷史缺檔：D5 c4 scope_ledger.json及D2 integration_doc_changes.diff；沒有新增full checkout或修舊檔 |
| 既存BASE正式docs DocGraph | exit0，62documents／213relations；與BASE歷史缺檔分列 |
| whole-worktree DocGraph | exit1，62 duplicate-ID errors；retained copies及本audit凍結docs都保留在實跑結果中 |
| tracked／cached git diff --check | 各exit0；既有shared diff不改 |
| 本輪report本地links／authored whitespace | verify逐links及末行／尾空白核對；frozen歷史文本不改寫 |
| 歷史E4 provenance | FAIL保留，本輪未重跑，未宣稱全部工具PASS |

負控制逐一核：錯digest、漏巢狀舊delivery、重複path、不安全path、漏claims payload，以及錯receipt。
前五份是實際alternate manifests；第六份以persisted bad receipt及獨立delivery fixture
執行同一receipt checker，fixture注入範圍於receipt明列。工具calibration成功只屬artifact語義。

```bash
python3 -B audits/2026-10-10-n45-s-low2/verify.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-10-n45-s-low2/verify.py
```

normal／seed17只讀重播核全列明preexisting inventory：32,177 regular檔的bytes與modes、
27 symlink identities及4 nested-repository directory entries；後四項**初始未遞迴hash內部**。
既有tracked／staged diff另逐byte核回。只有新exclusive audit被寫入，四nested repos不動。
完整metadata與只讀before／after相等以receipt／delivery綁定，工具不證paper。
沒有整份scratch clone、graph／k擴大、其他來源控制或新Lean。

Closure scope：僅§1完整LOW2契約的任意大小paper候選。
Updated：只此audit的Source／Evidence；原authority及adoption history的OPEN／尚未啟動文句保持當時語境。
Reviewed-unchanged：共享N45／STATUS／Kempe／Phase B／HANDOFF／README及全部舊audit。
Remaining OPEN：LOW2待獨立採納、整LOW合成、HIGH、long、其他cores／原55、一般N2／E及ε≥3；無新Lean。
Propagation stop：L0交付、L1本輪窄自核；獨立採納及共享文件傳播不在本輪授權內。
沒有commit／push／PR、再委派或外部訊息。
