# N45-L1A：LOW1 六項主張的獨立紙面稽核

2026-10-10。BASE `dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。本稽核只新增
`audits/2026-10-10-n45-l1a/`，沒有讀取本輪其他獨立稽核判決。

**裁決：LOW1-CORE／COMP／JOIN／F／MAP／EXCLUSION 六項均在完整指定契約內成立，
可供監督採納任意大小 LOW1 紙面排除。** 這不是本稽核自行修改正式 OPEN 狀態。
依賴 BASE 紙面論證及外部 Gallai 定理；沒有新增有限來源、來源實現或 Lean。

受驗交付是 [凍結 worker REPORT](frozen/worker/REPORT.md)、
[完整契約](frozen/worker/task.md)及 [逐項 claims](frozen/worker/claims.json)。
[inputs](inputs.json)分開保存十二個 Git BASE blobs、六個 current-work pins及八個交付檔案。
本稽核從原邊重推以下論證，沒有 import worker checker 或其他 reviewer 的裁決。

## 1. 精確範圍與逐項裁決

任取有限、任意大小、簡單 disk 圖 G，有序 induced 外框 C5 B，完整 Σ=933／941 或
一次共同整圖 D5 像；每條非框邊 Σ-critical，ε=2；有效 H 連通、full B-touch；
恰兩個非相鄰原完整 degree5 roots r,s，其他有效內點原完整 degree4。
H−{r,s} 的完整原分量恰 U、P、Q：U 是唯一 unary，唯一原 contact rx 歸 r；
P、Q 是 mixed、每側 incidence 正、各支援為一條真原框邊兩端；三份 one-sided且
actual support 非空。mixed incidence總數 (m_r,m_s)=(2,3)，兩 roots 原各兩 spokes。
只刪原 spoke e=rb_i，X=G−e=M 自身為原拒絕 literal β 的 inclusion-minimal 45／54 core。
全部 U/P/Q、其原內邊、root contacts、框附件和其他 spokes 留在 X。
具名 ordered contacts、共頂點单坐標、附件/support/ownership、bridges/rotation、共同色框、
十列完整 relations、每個可能 tuple 的空／非空 fibres及所有 full lifts 均同源保留。
root swap、D5、S4只能共同搬整圖和資料；933 q2包括在量詞內。

| Claim | 獨立裁決 | 充分理由 | 額外前提／反例 |
| --- | --- | --- | --- |
| LOW1-CORE | 成立 | 唯一 r–B 刪邊；r降至4，s維持5，其他點維持完整4；X=M提供自身最小性 | 無新前提；未發現反例 |
| LOW1-COMP | 成立 | r+完整U/P/Q經三條原r-contacts連成 H_X−s 的唯一分量，s原有三個互異contacts | 無新前提；未發現反例 |
| LOW1-JOIN | 成立 | 依原邊在唯一r色坐標接合全部 assignments；對任意 literal row及pin均有restriction／union雙射 | 無新前提；未發現反例 |
| LOW1-F | 成立 | X最小性排除同色 s-spokes；刪兩條spoke的full lifts排除兩個spoke色，得到精確補集 | 無新前提；未發現反例 |
| LOW1-MAP | 成立 | X自己的degree-lists、兩份tight assignments、三葉active tree及實際tethers給全部十對K5原邊 | 無新前提；使用明列BASE／外部依賴 |
| LOW1-EXCLUSION | 成立 | X本為disk子圖，卻含原邊K5 minor；排除每個滿足完整契約的有限任意大小來源 | 無新前提；範圍限LOW1 |

原孤立內點只屬免費 lift 的歷史有效-H慣例；X=M的有效點清單不新增孤立点。
一般U省略、LOW incidence2、HIGH、long、原55、其他cores、非unit／非minimal identities、
一般 N2／E及ε≥3均不在本裁決內，仍 OPEN。

## 2. CORE／COMP：從原邊確定新圖類

e只有原r與框點兩端，所以 H_X=H_G。原r的邊是 rx、對P/Q各一contact、兩spokes；
只刪其中一條spoke後完整degree4。原s的三mixed contacts及兩spokes都留存，完整degree5。
其他有效內點全部原邊保留、完整degree4。B的五條cycle邊、induced性、外面與disk嵌入
都由原G限制到X；有效ε_X=1。这里「完整degree4」是 X 的度，不是 C 的內部度。

由完整原分量清單，C=H_X−s 恰為原頂點集 {r}∪U∪P∪Q及其全部原誘導邊。
r分別以rx與對P/Q各一原邊接入三個connected pieces，故C connected且沒有別的分量。
不刪U、不收縮r，不替換成star。s的三contacts落在P/Q，簡單性使其三個neighbors互異；
接點順序就是原s rotation刪去兩條B-spokes後的順序。若接點同時鄰r，仍是一個原頂點。

X的β-minimality來自 X=M 的契約，不能由原G的完整Σ-criticality直接繼承。
對每條X非框邊h，X−h必接受同一β，因否則有拒β的真子圖，違反指定最小性。
以下只使用這個自有最小性，不需要原G的criticality替代它。

## 3. JOIN：全 assignments 的雙射與非空關係

固定任意同框 proper row γ，Col={0,1,2,3}。令 Λ_T(γ)為T=U/P/Q所有原內點
assignments：滿足T全部內邊及每一條原B附件，保留每個contact原坐標；暫不pin roots。
令 A_r^X(γ)=Col−γ(N_B^X(r))。C的完整lifts恰為

```text
L_C(γ) = {(c,f_U,f_P,f_Q): c∈A_r^X(γ), f_T∈Λ_T(γ),
          f_U(x)≠c, f_T(v)≠c 對每個原rv contact (T=P,Q)}.
```

restriction將每個原C coloring唯一映到此資料；反向以同一c和三份assignments取union，
恰檢查C全部原邊，且pieces間沒有漏掉的邊，故得到雙射。具名s-contacts p1,p2,p3
皆讀同一assignment。R_C(γ)是 L_C 在這三坐標的投影；對每個t∈Col³明定
Fib_γ(t)={f∈L_C(γ): (f(p1),f(p2),f(p3))=t}，包括不在R_C的空fibre。
這精確說明「保空fibre」，避免把只列非空投影的R_C誤當全部fibres。

pin s=a時只再共同要求 f(pj)≠a。若一contact也鄰r，兩項不等式同時作用同一坐標。
X的全部γ-full lifts是 a∈A_s(γ) 下上述各完整fibre的union，加上s=a、B=γ。
G的full lifts再加唯一原被刪spoke限制 c≠γ(b_i)。沒有用endpoint marginals代替joint，
也沒有獨立選取P/Q/U的色框、列或witness。這個等式逐所有十列及每個root pin成立。

非空性可獨立由degree4推出。對v∈C，寫d=deg_C(v)、k=|N_B^X(v)|、
δ=1_[v是s-contact]。完整度恰 d+k+δ=4。boundary-list
L_γ(v)=Col−γ(N_B^X(v)) 的大小至少4−k=d+δ。
因此它是C的degree assignment，且三contacts各有strict slack。C connected，依
[官方 Lemma 7](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，L_C和R_C非空。
這尚未pin s，不能誤讀成每個s色都能接回。

## 4. F：精確禁色只用 X 自身最小性

設s保留的兩條原spokes是sb_j、sb_k，字面β色為u,v。若u=v，刪一條spoke不改任何
有效list，仍拒β，違反X最小性，故u≠v。X拒β及上節精確join给
A_s(β)=Col−{u,v}⊆F_C(β)。

X−sb_j的β-full lift存在。其s色必為u：若不是u，同一lift也滿足被刪spoke而延拓X。
將該同源lift限制到完整C，便有C coloring在全部三contacts避u，故u∉F_C(β)。
刪sb_k同理證v∉F_C(β)。因此F_C(β)=Col−{u,v}，並已有R_C(β)非空。
這裡兩個witness屬X−s-spoke，不是其他原G刪邊或另列coloring。

此論證不使用U盾中點、第二拒絕列、任何非相鄰框位置或某一原mask的singleton身份。
933 q2亦是原literal β，完全適用。整圖S4可把u,v命名0,1、另外兩色命名2,3，
而每個原頂點、附件與次序保留。若要搬printed q=01012，三色C5 row亦可整圖D5/S4
搬運，必须同時搬整個mask和十列資料；沒有要求搬後仍印作canonical 933/941。

## 5. MAP：獨立重推 BASE 充分前提、active structure與十對原邊

[凍結 BASE theorem](frozen/base/docs/c5_two_spoke_three_contacts.md) §1的printed位置
S={b0,b1}不是通用充分前提：§5明允許任意兩個異色spoke位置。上述唯一原s、sole C、
完整degrees、三互異contacts、非空R及精確F均已在X自己得到。第二拒絕列及T4並非
§§2–4排除鏈必要条件。以下直接留在原β的共同色框重推，沒有只引用worker的映射表。

把兩個spoke色整圖命名0,1後，對a=2,3令
M_a(v)=L_β(v)−({a} if v是contact else ∅)。全部degree4给
|M_a(v)|≥deg_C(v)。因为a∈F_C，两份lists都不可染；connected strict-slack引理
迫使处处tight。特别是contact的boundary颜色互異且避2、3，因此两份lists的indicator差
仅在三contacts出现：3色多一，2色少一；0/1色没有变化。

独立读取的 [官方 Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
给同一C的Gallai blocks及两套block palettes；同顶点所属palettes互斥，union恰等该点list。
clique block palette大小为其点数减1，odd-cycle为2。这里把该刻画列为外部依赖，
没有把原图「critical」替代该定理，也没有把外部定理说成本Python或Lean证明。

令A是原C顶点×blocks incidence矩阵。若Aλ=0，leaf block有私有顶点，先迫其λ=0，
删该block及其私有点，再归纳到最后block；故columns线性独立。对0、1色差分别用A，
各block palette成员不变；对2、3色差之和用A，二者变化恰相反。故每个block固定，
或恰交换2与3。称后一种active。palette互斥使每个顶点至多邻一个正号active block、
一个负号active block；差式给contact恰active-degree1，非contact为0或2（相反号）。

active blocks与其vertices的incidence图是原block-cut tree的子森林，非空且只有三个
leaves，就是原三contacts。每个非空tree至少两叶，故整森林只有一个非空tree。
tree恒等式 L=2+Σ(deg−2)及block-node至少degree2迫使恰一block-node degree3，
其余degree2。因此唯一active triangle及三条active bridge arms，末端恰原contacts。
K4、较长odd-cycle不能作为这个degree3 block；degree2 block即原K2 bridge。
arm可任意有限长且可零长；此时triangle顶点就是原contact。三臂除triangle外互斥。
同号末端也给三臂同奇偶性，但K5构造不需要有限长度上界或枚举样本。

triangle点v_i已有两条triangle原边和一条首arm原边；零长则第三条为原sv_i。
X完整degree4恰留一条别的原边。若到B，直接得到tether；否则它只能是bridge进
inactive W_i：任何另一非trivial block需要至少两条新增边，而block-cut tree禁止它
重接已connected的active subtree。所有contacts已在active structure内，故W_i没有
s-contact；不同W_i互斥。U/r若在其中，仍保留其所有原边和实际框附件。

若W_i不碰B，C−W_i connected，M_2不变而v_i的内部degree减1，strict slack给coloring。
W_i无B或s约束；接入口w_i在W_i degree3，其余点degree4，全Col lists再由strict slack
可染。仅置换这个没有外部色约束的完整W_i coloring使w_i避v_i，便延拓M_2到C，矛盾。
所以W_i必有实际X框附件。从w_i取原路到该附件，连v_iw_i成为实际tether。
三条tethers内部互斥、避active structure，框端点允许相同。这里局部换色只用于上述
boundary-free反证，不是对跨列资料独立正規化；没有删U或使用省略的rb_i补路。

取Z={s}；V_i={v_i}加其整条原arm；O=原完整B加三条tethers内部顶点。
五bags非空connected且互斥。全部十对实际邻接如下。

| Bag pair | X 的原边见证 |
| --- | --- |
| V0–V1，V0–V2，V1–V2 | 唯一active triangle的三条原边 |
| Z–V0，Z–V1，Z–V2 | 三条原s-contact边，各臂端的原sp_i |
| V0–O，V1–O，V2–O | 各原tether的第一条边；直接spoke亦适用 |
| Z–O | 任一保留原s-spoke sb_j（或sb_k） |

零长arm时V_i={v_i}，原sv_i仍见证Z–V_i。O以完整原C5相连，tether框端可重合但
内部仍不重合。只在最后minor中把B列作connected bag，不宣称此收缩保染色relations。
得到X自身原边K5 minor，与disk子图平面性矛盾。这是任意大小抽取，不是有限controls外推。

## 6. 验收边界与重播

[independent judgment](independent-judgment.json)记录完整scope和六项成立裁决。
官方PDF本轮重新从primary URL取得，与worker和BASE PDF逐bytes相同，SHA256
`50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea`；
[source check](external-source-check.json)及[本轮文本](external/gallai-text.stdout.log)可核。
本轮重新读取Lemma7和Theorem10的陈述、blockwise定义及证明；没有声称新证明外部定理。

本checker只核26个冻结inputs、十二个BASE Git blobs、六个历史current pins、官方PDF、
逐claim的裁决契约及本稽核seal；它不判任意图的数学正确性。所有当前共享文档按初始
pin冻结，之后监监督合法采纳修改不会使这个历史snapshot失效；所列原audit仍核live bytes。
新增兄弟稽核目录不列为worker旧workspace的零漂移，不将预期旧inventory差异报成数学FAIL。

```bash
python3 -B audits/2026-10-10-n45-l1a/checker.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-10-n45-l1a/checker.py
```

实际normal／seed17日志与exit收于[checks](checks.json)。
精确payload inventory、manifest及seal metadata分别由[delivery](delivery.json)绑定。
工具PASS只确认这些bytes和scope记录；没有新source control、trigger数、来源反例或Lean。
未跑lake build：没有Lean改动，build不能形式化此新纸面映射。未重跑全树DocGraph或历史
check_docs；worker保留的历史缺檔与duplicate-ID FAIL未删除、未覆盖，独立工具稽核另处理。

无数学gap finding；空fibre的ambient-tuple定义在§3明确化，属于记号精化。
没有对共享文档正式采纳、commit、push、PR，未再委派。
