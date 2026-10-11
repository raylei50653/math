# N2 unary 三列出口及 root ownership 消去：獨立紙面審查

2026-10-11。審查者為 `arc_status_crosscheck`，與候選作者不同。
精確基準：[`../BASE.json`](../BASE.json)，HEAD
`5f0979793c19e452dbb5fc7e9fe7e43cb8a991cc`；數學輸入一律讀該 BASE 的
`../frozen/` 副本。本審查只寫新 `paper/`，未改 shared docs、舊證書，未 commit／push。
沒有讀候選作者的 `AUTHOR_REVIEW`，沒有 import 作者 checker。

**判定：ACCEPT，限於下面四個精確結論。**

1. 候選 `N2-55-U-THREE-ROW-ESCAPE` 的任意大小 block-tree 證明成立。
   在完整凍結來源前提下，原 unary U 的 owner 至少於同一原三列中的一列可取 D=3。
   因而 `(ℓ,u)=(0,1)` 的原55身份可由兩份 short 的同列完整 `(D,D)` lifts 排除。
2. 另加的 ownership transfer 成立：在同一完整 N2 來源內，long mixed C 若
   `k_C=k_C^r+k_C^s≤3`，則至少一指定列接受完整 diagonal `(D,D)`。
   因而可排除 `(ℓ,u)=(1,0)` 中 **long 的實際 root incidences≤3** 子域。
3. shared-contact 的一般局部結論成立：在原mixed C中同接r,s的實際頂點
   使每個proper框列β／每個色a的原diagonal `(a,a)` 都有完整C lift。
4. 新衍生稿§4的四列mask排除推論成立；共享mixed提供所有指定列的diagonal，
   可與另一份piece的同列出口接合，精確子域見本報告§8。

這不關閉無 shared contact 且 k_L>3 的一long剩餘身份、一般兩long的跨列同步、
含U與無shared long的同列同步、一般原55、完整N2或 E-ARC2。紙面判定不依有限 source
觸發；target finite controls 仍 `not triggered`，沒有新 target realization 或 Lean theorem。

## 1. 精確來源及外部定理適用性

候選凍結稿行14–43，spoke凍結稿§1及大小界凍結稿§1的全部來源契約保留：
指定有序 induced-C5 disk、完整 Σ933／941或整圖共同 D5 像、T4全收、
所有非框邊 Σ-critical、ε=2、有效H連通且 full B-touch、非相鄰原degree5 roots
r,s、其餘有效內點完整degree4、恰两原mixed及原one-sided pieces。
實際 ordered／shared contacts、ownership、框附件、rotation、bridges、旁支、
完整 relations／空fibres／full lifts 全保留。跨列只變 q，沒有單件正規化。

由同一原來源取得的局部輸入為：原 C 是只含bridge／奇環blocks的cactus；
每個多block leaf有私有root-contact；每個奇環block最多一普通私有點；
每個內點的框附件至多兩個相鄰框點；H內度二點到實際框邊的映射單射。
unary有至少三個框點支援。來源依賴分別在凍結spoke稿§2–3、§6、
凍結大小界稿§3–4及凍結unary盾弧稿定理A；本審查逐條核對了它們的原圖推論。
未重審上游全部N45／SD-A採納及其有限terminal信任鏈。

U的owner r有degree5，另兩mixed各至少耗一條原r-contact；簡單性使
k=|N_U(r)|與U的root incidence數相同，因此2≤k≤3。
下界2由凍結spoke稿推論1.1；上界只用原degree5，沒有借45／54 derivative。

直接下載並核讀 [Dvořák 2018 原PDF](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)。
保存在 [`gallai.pdf`](gallai.pdf)，SHA256
`50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea`；
文字在 [`gallai.txt`](gallai.txt)。頁5 Lemma7（文字行170–181）給連通不可染
degree-assignment的每點tightness；頁6 Theorem10及其定義（文字行206–221）
給Gallai blocks及incident palettes互斥聯集。bridge palette大小1，奇環大小2。
這些輸入是內部list定理，不要求預先給一份外部完整合法染色。

## 2. 原局部lists與固定三列算術

反设三列都不允許owner D=3。在原U上固定

`L_i(v)=[4] \ (q_i(N_B(v)) ∪ ({D} if rv∈E else ∅))`，

其中 q0=01212、q1=01202、q3=01021。原完整degree4直接給
`|L_i(v)|≥d_U(v)`。連通拒絕由Lemma7迫tight；Theorem10給每個原block的palette。
因框只用0,1,2，D∈L_i(v)恰當且僅當v不是原root-contact。
所以contact的每個incident block palette都不含D；非contact恰有一個incident
palette含D。所有後續推論只使用這份原lists，未改原圖。

獨立腳本 [`signature_check.py`](signature_check.py) 從三個字面q重算：

| 原框邊 | 未見已用色三列signature |
| --- | --- |
| 01 | 222 |
| 12 | 002 |
| 23 | 011 |
| 34 | 010 |
| 40 | 112 |

五個框點signatures為000、111、220、102、221；兩張表均單射。
25個有序edge pairs中只有01／23和01／34及逆序逐列異色；第三已用色signature
分別100、101，均不在框點表。十個不同框邊triples中八個在某列已見齊0,1,2。
餘下12／23／40及12／34／40分別逼中央已用色220、221，至少一條臂所需的
框點signature為001、110，均不存在。這不是有限圖來源枚舉；只核字面C5算術。

## 3. 無界cycle縮限：contacts如何逐一計帳

固定原奇環block K。每個K上的U割點x至少有一個環外方向；有限block-cut tree
中沿該方向可找到一個K外leaf block，其私有contact不在K。
不同x的方向彼此互斥，選出的contacts互異，也不等於K上的私有contacts。
K上剩下的普通私有點最多一個。因此

`|K|≤1+(K上割點數)+(K上私有contact數)≤1+k≤4`。

奇環只能是triangle。若K有contact，它的palette不含D；若還有普通私有點，
該點的唯一incident palette就是L_i(v)，卻含D，矛盾。故三個triangle點
各為私有contact或有環外方向的割點，至少需三個不同contacts。
任何割點本身又接root，便是在既有三個之外的第四contact，故不可能。
這明確涵蓋cycle上的contact割點，沒有把它偷偷計成leaf的私有contact。

於是含contact triangle只在k=3時出現；其每個外方向恰耗一個contact，
沒有額外分枝或額外contact。無contact triangle若有三個割點，同樣耗完三個
外部contacts。若有兩個割點，它的第三點是普通私有點，原框附件是邊f，
palette逐列為 `{D,T_i(f)}`。若只有一個割點則有兩普通私有點，來源前提排除。

## 4. 末端第一個原鄰點已排任意長鏈

leaf bridge的私有端p只有一條U邊。完整degree4、框附件上限2及一root邊
迫p接root及原框邊e；palette必是 `{T_i(e)}`，不含D。
設該bridge另一端w在沒有額外contact或branch的terminal chain上：

* 若w只屬兩bridges且不接root，w也有框邊f，L_i(w)={D,T_i(f)}。
  incident palettes互斥迫T(e)=T(f)，三列edge表单射迫e=f。
  p,w原H內度都為2，違框邊附件單射。
* 若w的另一block是普通triangle，w原U內度3，故恰接一框點h。
  triangle palette是{D,T_i(f)}，bridge palette與它互斥，迫q_i(h)為
  T_i(e)、T_i(f)的第三已用色，違上節pair signature算術。
* 若另一block是含contact triangle，該triangle palette不含D。
  w不是contact時L_i(w)含D，故bridge palette只能含D，與leaf端矛盾。

這些都是原leaf邊的第一個鄰點判斷，沒有收縮鏈、替換triangle、丟掉共享割點
或宣稱縮圖保relation。branch/contact以前的任意多bridges／普通triangle因此均被排除。

## 5. block-cut tree的互斥窮盡

單block另列。多block時tree至少兩leaf，每leaf需要不同私有contact，故至多三leaf。
在D拒絕下，cycle leaf的兩個私有點不能一contact一普通點；它們必全為contacts。
下列完整列出所有無界tree形狀，沒有用有限短圖外推。

| 形狀 | 原圖排除 |
| --- | --- |
| singleton | 只接一root及至多兩框點，完整degree不足4 |
| 單bridge | 兩端都接root及框邊；同palette迫同框邊，違原H內度二附件單射 |
| 單triangle | 有普通點便與contact的D判定矛盾；三點全contact則各恰一框附件，同lists與point-signature單射迫全接同一框點，違U跨度≥3 |
| 两leaf，有cycle leaf | cycle兩私有contacts加另一bridge leaf正好耗三contacts；bridge端的第一個鄰點或為上節普通链，或直接接特殊triangle，全部矛盾；兩cycle leaves需≥4contacts |
| 两bridge leaves，k=2 | tree是路徑，沒有第三contact；非單bridge時第一個鄰點只可為普通bridge或普通triangle cutpoint，已排 |
| 两bridge leaves，第三contact在cycle | triangle只能有兩cutpoints加一私有contact；兩端chain普通部分或直接接該triangle，均已排 |
| 两bridge leaves，第三contact不在cycle | 它只能是两bridge間cutpoint w；兩端chain被排，故原圖只剩p-w-q且三點全contact。w恰接一框點，pair signature排除 |
| 三leaf，branch為cutpoint，三bridges | 三leaf全為bridge且耗完三contacts。普通末端chain排除後三bridge都直接接branch；三palette全不含D而branch不接root，矛盾 |
| 三leaf，branch為cutpoint，cycle+兩bridges | 原完整degree≤4只容此另一組合；cycle恰有另一cutpoint及普通私有點，為普通triangle。第三臂的原leaf第一鄰點無論有chain或直接接该triangle均已排 |
| 三leaf，branch為cycle block | block是三cutpoints triangle，三臂必直接接contact bridge葉。葉框邊互異（H內度二單射）；triangle palette若不含D，臂palette被迫D，矛盾；否则{D,c_i}与臂T_i(e_j)互斥，各cutpoint的一框附件須供第三已用色，triple signature排除 |

三leaf的唯一branch由有限樹恆等式
`Σ_{deg≥3}(deg−2)=leaf數−2=1` 給出。
branch可能在block節點或割點節點，兩者均已列；bridge block不能branch。
若branch在割點，三incident blocks的U內度總和≤4，只能3bridges或cycle+2bridges。
後一組合的cycle不能另有三cutpoints，否則tree會有第二branch；也不能只有一
cutpoint，否則有兩普通私有點。這補明候選行157「普通triangle」的來源。

所有反設形狀均矛盾，因此確有某一同列i使原U完整L_i-coloring存在。
這就是owner D的full lift，等價於D不在該列F_U；不是只證contact marginals。
沒有發現必須補上的數學前提或遗漏branch。

## 6. `(ℓ,u)=(0,1)` 的同列完整接回

在上述同一i固定r=s=D。q_i只用0,1,2，所以全部原root-spokes均合法；
原rs不存在。U的完整lift避開owner D。
凍結E4報告§4.1的N-diagonal是**局部**list結論：任何one-sided degree4 mixed
若actual support含於一原框邊，則任何proper q及同色pins均有原C的完整lift，
不要求事先給G−C染色。在本來源兩short的support確實含於一框邊；
若要使用後續pair必要性，含U的singleton排除亦已在凍結統一稿§3成立，但不是本步必需。

核對N-diagonal的原hub適用性：對任一short C，K=H−C連通，且每個
B之外框邊的框點都由K原附件碰到。另一mixed仍連r,s，unary仍接owner，
故含U並不破壞K連通。取兩框點singletons及K連剩餘框路為第三hub；
在N(C)交集上第三hub只見root色D，各hub兩兩相鄰且互斥連通。
局部拒絕的tightness若因shared root contact已失敗，便直接得到full lift；
否則hub收縮保持C的degree及lists，凍結short-support三hub/Gallai minor反證照用。
沒有假造外部完整染色。

於是兩short P,Q各有該**同一q_i／同一(D,D)**下的完整assignments。
P,Q,U是原H−{r,s}互斥components，沒有跨component邊；接合保留原shared contacts
及所有原附件，每份只用一次。自由孤立四色因子非空。得到原G的完整q_i染色，
違原拒絕。故候選的限定原55子族排除可正式採納。

## 7. 另加的 long mixed ownership transfer

**限定命題 L-K≤3-DIAGONAL-ESCAPE。** 仍在同一完整N2來源前提下，
對原long mixed C，若k_C=k_C^r+k_C^s≤3，則存在i∈{0,1,3}使
`(D,D)∈A_C(q_i)`，並有原C的full lift。

先固定兩roots同為D。實際lists為

`L_i^C(v)=[4] \ (q_i(N_B(v)) ∪ ({D} if v接r或s else ∅))`。

**有shared root contact。** 該點v接兩個不同roots但只禁一次D；因此
`|L_i^C(v)|≥d_C(v)+1`。其他點均為degree assignment。C連通，Lemma7的
逆否命題或其生成樹貪婪證明直接給原C完整L_i^C染色，對每個指定i都成立。
這不需要k_C≤3；把D換成任意色a、q_i換成任意proper框列β，完全相同的
原degree計數仍成立，故每份原diagonal `(a,a)` 都有完整lift。

**無shared root contact。** 每個contact恰耗一root incidence，故
`K=N_C(r)∪N_C(s)`的點數正是k_C，既有原incidence下界給2≤|K|≤3。
原外部lists與上節unary case split完全相同：只禁D於K，root ownership標籤
不進lists。逐項映射如下，不能把兩root自由重接成一個root來源。

| unary局部輸入 | 同一原mixed C的實際對應 |
| --- | --- |
| 每點degree4、每contact一root邊 | 無shared contact，故degree等式d_C(v)+1_K(v)+|N_B(v)|=4 |
| contact數2／3 | k_C≤3且原incidence至少2 |
| cactus | 凍結大小界§4對每份原C成立 |
| leaf私有contact | 凍結spoke§3對兩種root ownership皆成立，選leaf上的實際contact，不重新接線 |
| cycle普通私有點≤1 | 普通指非C割點且不接任何root；凍結spoke§2對每份C成立 |
| H內度二框附件單射 | d_H(v)=d_C(v)+1_K(v)，原H／原框附件不變 |
| 支援跨度≥3 | 原long one-sided mixed的實際support至少含三個連續框點 |

因此反設C在q0、q1、q3都拒絕(D,D)，會逐字觸發§2–5的局部矛盾。
那裡真正用到owner唯一性的僅是**每contact一條外部root邊及統一禁色D**，
本情形已由無shared及diagonal給出；没有步驟要求不同contacts的實際root相同。
證明沒有合併r,s，沒有改原嵌入，沒有宣稱合併後圖是disk。
所得完整L_i^C染色同時避開原r及s的D，故是實際ordered diagonal full lift。

若`(ℓ,u)=(1,0)`且long k_L≤3，取它的escape列；另一short在该列由N-diagonal
完整接受(D,D)。無unary，root-spokes避D，原rs不存在，兩原mixed完整接合成G染色。
因此這個限定子域排除 **ACCEPT**。不能把兩long各自的「存在一列」相乘，
也不能把U escape列與long的另一列相拼；這兩同步義務未被本transfer證成。

## 8. 新衍生稿的精確裁決與mask推論

另讀root新撰 [`docs/c5_excess_two_n2_diagonal_three_row.md`](../../../docs/c5_excess_two_n2_diagonal_three_row.md)
（shared doc只讀）。精確審查版本保存於
[`diagonal_three_row.reviewed.md.snapshot`](diagonal_three_row.reviewed.md.snapshot)，
bytes=8396，SHA256=`4a46e29d5b77fe685faeafe1c684c9073b61967aef077079363738e1fae5857d`；
記錄見 [`derived_document_review.json`](derived_document_review.json)。
這是原BASE以後的衍生稿，沒有拿它替換冻结的原數學輸入。

逐項判定：該稿§2定理1與推論1.1 **ACCEPT**；§3引理2的任意proper β／任意色a
結論 **ACCEPT**；引理3的原k_C≤3與ownership transfer **ACCEPT**；
§4的mask含義、同列full joint充分条件及下表限定排除 **ACCEPT**。

| 原參數域 | 精確採納的排除 | 必須保留的剩餘界線 |
| --- | --- | --- |
| (0,1) | 完整子族 | 父N2仍OPEN；與既有u=2合併只閉第三relation族的55格 |
| (1,0) | long有shared contact，或long k_L≤3 | 無shared且k_L≥4仍OPEN |
| (1,1) | long有shared contact；取U escape列接回long／short | 無shared long與U的同步仍OPEN，即使long k_L≤3亦然 |
| (2,0) | 一long有shared contact，另一long有shared contact或k≤3 | 两份無shared的低接點long各有出口仍不足；其他同步仍OPEN |

证明mask推論時，只需取同一i不在所有piece的diagonal拒絕mask中。
short或shared mixed的mask空；long k≤3及U只保證mask是I的真子集。
同一列的root pins皆D，原spokes及無rs已檢查，完整piece assignments可如§6接回。
两个真子集的聯集可能覆蓋I，因此稿中沒有宣稱一般兩long或U／long同步。
原u=2已另排，故本次接合含U時只有一份U。

關九格第三relation族的55格後是七格覆蓋；另三列參數域的上述子域排除，
不會把其中任何一個完整原55格升格CLOSED。沒有新Δ下界或原55大小上界矛盾。
未發現需要修正的 theorem／corollary scope。

## 9. 有限核對及保留邊界

[`signature_check_final.json`](signature_check_final.json)保存原字面表、全部25 pairs／10 triples、
11份冻结輸入hash、外部PDF hash；normal及seed17重播命令為：

```bash
python3 -B audits/2026-10-11-n2-unary-adoption-long-joint/paper/signature_check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-n2-unary-adoption-long-joint/paper/signature_check.py --check
```

初次啟動時的working inputs對照另外保留於
[`signature_check.json`](signature_check.json)，當時11份working inputs均與BASE相同。
其後root獲授權更新canonical docs，故最終checker只以BASE的不可變frozen inputs
為數學authority，不把允許的routing／adoption drift視為冻结輸入失敗。

* 字面算術控制：`triggered and holds`；4個逐列異色pairs全不可實現第三框點，
  10個different-edge triples全不可實現中央triangle的三列附件。
* 原Σ933／941完整target source：本紙面worker未生成或搜尋，`not triggered`。
  固定97U／42局部trigger的作者有限報告由別的獨立replay負責，不作本紙面採納依據。
* 無界結論由上述有限樹leaf恆等式、原degree及原palette論證承擔，
  不由checker表大小、source零觸發或10–35點搜尋推斷。
* 沒有新Lean theorem，沒有重跑Lean build。未替代上游已採納依賴的信任邊界。
* 精確採納上述unary、shared diagonal、lowcontact transfer及§8限定接合子域；
  一般原55／N2／E-ARC2 OPEN。
