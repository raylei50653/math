# BR-SD-1g-ADOPT：獨立原來源與量詞審查

2026-10-11；本輪固定 `main@c15a635e17d4be814e19aeeeeb765f3d6024099a`。
本 mapping reviewer 與原 1g mapping reviewer 為不同 worker；本輪直接重讀
canonical、原 PROOF、原 MAPPING、1c／1e 原 PROOF，未以原 review 的結論作前提。
僅新增本任務 `agents/mapping/`；沒有修改任何原輸入、canonical、STATUS 或 HANDOFF。

**Mapping 裁決：ACCEPTABLE，沒有阻斷的原來源／量詞 finding。**
這是完整原來源合同與本證明所用座標相容的裁決；全任務裁決仍須 root 合併
獨立数学與 custody 審查。本檔未執行正式採納。actual source 是 `not triggered`；
無新 Lean theorem，完整 OPEN 身份新增無條件關閉數為 **0**。

## 1. 讀取證據与可重播紀錄

[READS.json](READS.json) 保存各次原輸入讀取的 argv、cwd、exit code、
stdout／stderr 檔名與 SHA256；[read_inputs.py](read_inputs.py) 為擷取工具。
所有列出的讀取命令 exit 0。固定 HEAD 的實際 readback 是
[read-01.stdout](read-01.stdout)；工作樹 readback 是 [read-02.stdout](read-02.stdout)。

主要原輸入：

- [1g PROOF](../../../2026-10-11-br-sd-1g-dbdc4c35/PROOF.md) §1–7。
- [1g MAPPING](../../../2026-10-11-br-sd-1g-dbdc4c35/MAPPING.md) §1–8。
- [canonical N45](../../../../docs/c5_excess_two_nonadjacent_unit_core45.md) §1／§2.11／§3。
- [1c PROOF](../../../2026-10-11-br-sd-1c-fd6e1112/PROOF.md) §1–8。
- [1e PROOF](../../../2026-10-11-br-sd-1e-337d018b/PROOF.md) §1–6。

本 worker 另直接讀 degree-5 guide、interfaces、Kempe guide 及 STATUS／HANDOFF 的相關入口，
保存於 read-09 至 read-12。本文的回寫內容只是提案，不在本輪改上述文件。

## 2. 完整原來源逐項對照

| 必要來源身份 | 獨立核對 |
| --- | --- |
| 同一原 G、M、β、Σ、ε | 1g §1.1–3 保同一有限簡單 ordered induced-C5 disk G，完整有序 Σ933／941 或整圖共同 D5 像，ε=2；M=G−e 原點全留，仅刪 r 唯一原 spoke，β 為同一 proper 三色 literal 拒絕列。不是把抽象 lists 當作另一張來源。 |
| roots／有效 degree | 原 G 的 r/s 不相鄰、完整5，其餘有效原內點完整4；M 僅 s 完整5，r 及其餘有效原內點完整4。r 的 C-degree4／M 框附件0，加回原 e 恰回 G-degree5。 |
| 原完整 pieces | U=0，`H_G−{r,s}=L⊔S` 恰兩份完整原 mixed；L long，S 為原 actual 真框邊 pair-short，保 full B-touch、one-sided、support 非空。W1／W2 分別是 L／S 的原部分。 |
| M 自身 minimal／拒絕 | 1g 明列 M 自己對同 β inclusion-minimal 且拒絕；保 M retained 非框邊自己的同 β full witnesses。G 的 Σ-critical 性沒有代替此條件。短證明只用 M 的拒絕，但没有删去 minimality／witness 合同。 |
| 原 s contacts | s 的有序相異內鄰恰 p∈L、q∈S，三條原框 spokes全留；Wi 無 s-contact。固定 s=D 與全部 s–B 邊相容，因同一 β 未使用 D。 |
| r split22／sole C | `C=H_M−s={r}∪L∪S` 為同一實際 sole connected component；r 向 L/S 各兩原 C contacts。不是另選 minimal core，亦没有假定 H_M 二連通。 |
| 三原環／原 bridge | J1 指定 triangle `(r,a1,x1)`，J1∩J2={r}，J2／J3 任意奇長≥3，J3 不交前兩環；uv 是 u∈J2−r、v∈J3 的唯一原環間 bridge。全部骨架原邊保留。 |
| W1／W2 | Wi 有限非空、互斥骨架與彼此，C[Wi] 連通；唯一骨架鄰點分別為 x1、x2，x2∈J3∪q-arm。沒有 Wi 相互接線、第二骨架接點、額外 s-contact、第三旁支或 cross edge；允許同 xi 的多條原 Wi 邊。 |
| ownership／actual attachments | J1−r／p 臂／W1 完全在 L；J2−r／uv／J3／q 臂／W2 完全在 S。只刪 r-spoke，故 `N_B^M(S)=N_B^G(S)=T_B={b_i,b_(i+1)}`，每點附件 subset 與整份聯集恰 pair 兩項都保留。W1 不受 S 兩框點上限。 |
| 原座標／完整資料 | 所有原點／邊、named／ordered／shared contacts、ownership、attachments、rotation、bridge 端點、字面 β／Col、G/M 各自完整 relations／空 fibres／full lifts 都保留。45／54 只整圖共同交換 roots roles。沒有逐 component 調色或只檢邊際。 |

量詞精度：1g 以「保 frozen canonical §1／§2.11 與既採 1a／1c／1e 合同」继承 S short。
原 1g 独立列出的正文说 S actual pair，未重新写 short，與 canonical 不衝突。
正式提案應明寫 **S short 且 actual support 恰同一真框邊 pair**，避免讀者把結果當作
移除原 long／short 身份前提的新 theorem。這是提案需明寫的精度，非原證明缺口。

## 3. 獨立 degree／attachment 重建

全部 y∈C 的原鄰居恰在 C、B、s，且 `d_M(y)=4`。
令 `A(y)=N_B^M(y)`、`k(y)=|A(y)|`、`t(y)=1[sy∈E(M)]`，則

`4=d_C(y)+k(y)+t(y)`。

只有 p／q 的 t=1。xi 的額外原內鄰數 `mi=|N_C(xi)∩Wi|≥1` 必使用
原已有附件的同一预算，不是允許把附件删掉後再填表。

- x1 是 J1 的第三點，d0=2、t=0，故 k=2−m1：仅 m1=1／k=1 或 m1=2／k=0。
- J3 上的完整骨架度是 `2+1[x=v]+1[x=a3 and ell>0]`。
  若 x2=a3=v，零臂再有 t=1、正臂骨架度4，两者均得 k=−m2，任何非空 W2 都超度。
- x2=v≠a3，或 x2=a3≠v（含零臂 q=a3）：d0+t=3，故 m2=1／k=0。
- ordinary J3 點、正長 q 臂內點、正長末端 q：d0+t=2，故 m2=1／k=1 或 m2=2／k=0。
- 非接點 J2 的 u：dC=3、t=0、k=1；`J2−{r,u}` 的所有點：dC=2、t=0、k=2。
- 非接點 p 臂內點／正長末端 p 分別 dC=2,t=0 和 dC=1,t=1，均 k=2，原附件歸 L。
- 非接點 q 臂內點／正長末端 q 同度數，但 S pair 恰供其兩附件。
- W1 各點無 s-contact，k=4−dC 可為3；W1 degree1 葉只是局部容量可行。
  W2 各點附件在 pair，k≤2，故必须 dC≥2；degree1 葉要求三原 B 鄰點，直接違合同。

以上重建窮盡 x2 的具名位置与全部允許重合：p=a1、q=a3、a3=v；
正長 off-cycle 臂點由原身份與 cycles／另一臂互斥，没有把同一點算成兩個坐標。
J1 的 x1 与 r/a1/p/q 不重合；x2 不可能与 r/u/a1/x1/p 重合。

[degree_table_control.py](degree_table_control.py) 由原圖骨架 adjacency 独立計数，
校準 J2/J3 長3／5／7、h／ell=0／1／2／3、a3=v／a3≠v、全部 x2、m=1／2／3。
[DEGREE_CHECK.json](DEGREE_CHECK.json) 保存命令、stdout／stderr與exit0；
[degree-table.stdout](degree-table.stdout) 為完整結果：288個具名骨架、1,872個接點位置、
5,616個 x2 budget rows、864個 J2 witness rows，全部 formula assertions 通過。
3,168個 locally valid capacity rows 是必要容量，**没有聲稱3,168個來源存在**。
控制范围止於上述有限具名結構，不提供任意大小量詞或 actual source。
`PYTHONHASHSEED=17` 的同一控制再執行exit0，stdout逐byte相同；命令及原始紀錄見
[DEGREE_CHECK_HASH17.json](DEGREE_CHECK_HASH17.json)、[degree-table-hash17.stdout](degree-table-hash17.stdout)。

負控制另核 a3=v 旁支／x1 第三邊／W2 degree1葉／刪旧附件才容納旁支的第一失敗。
`P_J1={A,B}`、`P_branch={D}` 的互斥聯集含D，而 J1 palette 不含D，
是禁止推論 `D∈L(x1)⇒D∈P_J1` 的 **counterexample**；不是完整原來源反例。

## 4. 原 blocks、private witness 與旧lemma边界

Wi 到骨架只經 xi。一條同时经过 Wi 与骨架−xi 的 simple cycle 必須重訪 xi，
所以旁支不能合併原 J1/J2/J3 blocks，也不能使 uv／原外臂繞過 bridge。
新 blocks 完全位於 `C[Wi∪{xi}]`。Wi 連通使 xi 在此分支子圖非割點，僅属一個首 block。
若 Gallai 刻畫已觸發，m=1 首 block只能 bridge，m=2 只能奇環（triangle亦可）；
K4 首 block需3條原邊，degree预算排除。分支深處的 K4 没有被這項局部预算排除。

1e 的双private-witness lemma **不可整体套用**：W1佔 J1 triangle唯一 witness x1，
x1已有另外block，a1是正臂割點或零臂 s-contact，r已有J2，沒有替代w1。
`D∈L(x1)` 只能由全部incident palettes聯集供给，不能强迫J1含D。
J2则完全没有W1／W2接入；任意J2奇长≥3，`w2∈J2−{r,u}` 非空，
只属J2、非割点、非s-contact、dC=2。S pair与完整degree4迫A(w2)=T_B，
故坏degree assignment下 `P_J2=L^D(w2)={T,D}`。两旁支与全部零臂／重合均不影响这一步。

1c terminal lemma只有完整局部前提保留时可用：x2∈{v,a3}且a3≠v时，
J3其他接入仍仅v/a3、q臂其他点无额外内邻、q唯一s-contact，故已有局部lemma排除。
x2=a3=v先超度；ordinary J3接入可能佔private witness，off-cycle臂／q接入改变臂度数，
因此不能普遍套完整terminal lemma。仍保J3 witness與原首臂点的部分配置可以重用其
明列局部证明依赖，原1g没有把它們冒充新OPEN。三项已採单旁支scoped theorem
本身都不涵盖本双旁支来源；本轮只核其局部lemma必要前提，未自动继承结论。

## 5. 完整 lists／fibres 与 S 接口核对

原 list 是

`L^D(y)=Col−(beta(A(y)) ∪ ({D} if t(y)=1 else empty))`。

原boundary邻点可能同色，但禁色数至多k+t，所以逐点
`|L^D(y)|≥4−k(y)−t(y)=dC(y)`；没有先把lists假定为tight。
把C的完整list assignment接β与s=D，逐类满足B–B、B–C、s–B、s–C、C–C，
包括Wi全部原内边、接入边和附件。反向限制M着色得到同一具名C assignment。

令Z为effective-H忽略的原内图孤立点。其各自允许色集为
`Q(z)=Col−beta(N_B^M(z))`，至少含D；原邻边均到B，各Z因子相互独立。
所以固定β／s=D的完整lift集合是具名接合

`{beta} × {s=D} × Color(C,L^D) × product_(z∈Z) Q(z)`。

完全无邻居的原孤点才Q(z)=Col。此乘积保被忽略原坐标；只有Z为空才可把
C assignments与M full lifts直接称为一对一。原1g §3明确写出这些因子与此界线。
空C fibre对应空M fibre；没有以存在性等价替代full-lift坐标保真。
其他s色的原完整relations／fibres只作为来源保留，证明未伪称用s=D部分重建全部关系。

S侧所有非q原点附件在pair且不邻s，所以其lists同时含固定原T/D；q含T而禁D。
原C−r恰L⊔S，S所有原C-blocks位于S∪{r}；唯一含r的S block是J2。
W1属L、W2属S且各单接点，无旁支越过原ownership；所有S到L接口必先经过J2。
`P_J2={T,D}` 使恰含T/D之一的block不能与J2共享任何原点。
从q的T-block起，下一点仍在S且不同q，缺的另一色由另一incident block供给。
这是完整palette联集的使用，未把割点list含D分给每个palette。
非割点无另一block便直接矛盾；任意有限Wi的bridge／triangle／奇环／K4都至少两点，
可选不同出口。该映射支持原proof在有限block–vertex incidence tree内不回头的追色；
任意大小结论应由独立数学review的树证明承担，非上述有限controls承担。

## 6. ACCEPTABLE時的精確定理量詞建议

建议名字：**BR-SD-1g 双原旁支 J2屏障 scoped exclusion**。

对每个任意大小有限简单ordered induced-C5 disk原G及同一具名完整来源資料，
在本檔§2完整G／Σ933或941／整图D5像／ε2／Σ-critical full witnesses／非相邻5-roots／
其余有效完整4／原full B-touch／one-sided／nonempty support全部合同下，
且U=0、L long、S short的actual support恰同一真框边pair，exact-S仅删r唯一原spoke、
同一M=G−e自己同一proper三色literalβ inclusion-minimal且拒绝并保其原retained-edge full witnesses，
M仅s完整5且其余有效完整4，s原有序相异p∈L/q∈S与三spokes全保，
sole connected C与r split22成立；若原C骨架为J1=(r,a1,x1) triangle、任意奇长≥3的J2/J3、
J1∩J2={r}、J3与其不交、u∈J2−r至v∈J3的唯一原环间bridge，
原p/q simple bridge臂长任意h/ell≥0并允许p=a1、q=a3、a3=v，
且C恰分骨架与两份有限非空连通原off-skeleton Wi，唯一骨架邻点为x1与
x2∈J3∪q-arm，W1/W2原ownership分别L/S、无额外s-contact／相互边／第二接口／
其他旁支／cross edge，所有原内边、actual附件、rotation、ordered/shared contacts、
bridge身份、同一字面β／Col、G/M完整relations／空fibres／full lifts及ignored原因子全保，
则以上完整原来源合同不可能同时成立。

此定理包括全部合法x2、原附件实际mi值、任意有限Wi大小及所有允许重合；
先超完整degree者为结构排除，其余由同一S/J2屏障的纸面矛盾排除。
不得以证明实际只需部分强前提为由，把正式定理扩展为一般多旁支／Gallai tree结果。

## 7. 逐檔回写裁决建议与OPEN

仅当全任务最终ACCEPTABLE且owner另行批准正式采用后：

| 檔案 | 最小同步建议 |
| --- | --- |
| N45 canonical §2.11 | 置於1e采用段之后、§3之前新增完整1g精确合同与J2屏障／有限incidence tree证明摘要，连接本轮最终audit。§2表新增独立1g scoped row；§3残留表新增此精确双旁支subset、保一般多旁支与父身份OPEN。 |
| degree-5 guide §4 | 将1g窄候选段改为此完整合同已采用，并明确W1失去双witness、W2可能破坏terminal但J2／S接口保持；保R31原义务。 |
| degree-5 interfaces §7 | 追加1g独立证据／scoped合同、无二连通要求、full-lift因子与零closure；原SD-A及历史conditional段不改。 |
| Kempe guide状态列／§3 | 与canonical新增1g精确入口同步；不得把一般两旁支、split22或N2行改为全排。 |
| STATUS对应入口 | 新增最终1g audit／采用记录入口，写actual source not triggered、无新Lean、完整closure0及父OPEN；不用PASS概括扩大身份。 |
| HANDOFF | 需要同步当前接续到已采用的精确1g结果和下一个尚未覆盖残留，保现有父OPEN；更新研究接续不等于把一般多旁支关掉。 |
| 历史1a／1c／1e与原1g audit／publication／seals | 保全部bytes；本轮采用证据与历史candidate语境分开，不回写旧review。 |

依赖：原1g PROOF／MAPPING，canonical完整来源定义、同β原M拒绝与完整degree，
外部Dvořák degree-assignment／blockwise-uniform刻画（数学review独立核版本），
以及本轮独立proof／mapping／custody最终bytes审查。有限degreecontrols只校准具名行。

完整 `N45-S-NOU-LS-PAIR` 仍OPEN；未覆盖split22／非split22、其他多旁支、
其他三环形状／更多环、一般非二连通來源、R31、其他45／54／55与无45／54、ε≥3、
一般N45／N2／E、一般出口、主命题与 `K∞=K≤5` 均不升级。
actual source **not triggered**，finite degree controls **triggered and holds**，
禁止cutpoint推论负控制 **counterexample**；无新Lean theorem。
**完整OPEN身份新增无条件关闭数为0；本檔没有正式采用、commit、push或merge。**
