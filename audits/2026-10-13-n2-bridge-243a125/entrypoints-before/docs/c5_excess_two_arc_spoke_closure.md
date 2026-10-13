# E-ARC2：末端 block 接點與 N2 的全部真核心排除

**後續（2026-10-13）**：[LL-CUT+diag](c5_excess_two_n2_ll_cut.md)已完成指定完整Σ契約的
原55九格覆蓋；基本LL-CUT、較廣N2／E-ARC2仍OPEN。
下文保留本報告當轮45／54定理、有限控制及停止點。

2026-10-11，工作樹基準 `df60ef5b6a386e5b1e4e3137a145c915875897ce`，
接續未提交的[原分量共同限制](c5_excess_two_arc_component_slack.md)。
目前入口及停止點見 [Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口)。
整理發布與本次重播範圍見[三點弧發布紀錄](history/2026-10-11-three-point-arc-publish.md)。

**完整 N2 目標前提下，剩餘 root-spoke 45／54 也已排除。**
每個拒絕列的唯一 minimal core 必為原 G 自身的55；每條非框邊 e 都滿足
`Σ(G−e)=Ω`。因此連 roots 在內，每個內點至多接兩個相鄰框點。
**原55的共同矛盾、N2來源排除及三點弧命題仍未證成。**

**後續（同日）**：[原55大小界](c5_excess_two_arc_size_bound.md)把含unary的H收窄為
中央block加至多兩個root葉blocks，並由K₅／K₃,₃及cactus計數證
`|H|≤35−6u−3t`（有效內點）。這是原圖上界，原55及三點弧仍OPEN。

新步驟是同一分量的跨列 palette 限制、原 leaf-block minor，以及在同一 H 上
對兩個相反方向的 spoke derivatives 各用一次已查證 SD-A。含 unary 的 S 身份
則逐项接回既有已採納覆蓋，沒有將其限定契約略去。
證據層是外部定理＋紙面證明／合成；固定控制另列，沒有新 Lean theorem。

## 1. 完整來源前提與依賴

G 是任意有限簡單 disk 圖，外框為指定有序 induced C₅，B=(b₀,…,b₄)。
完整有序 Σ(G)=933／941 或整圖共同 D₅ 像，全部非框邊 Σ-critical，ε=2。
有效 H 連通且 full B-touch；恰兩個非相鄰原 degree-5 roots r,s，其餘有效內點
完整 degree 四。H−{r,s} 恰有两份原 mixed P,Q，其餘 unary；原件 one-sided，
兩 mixed actual support 非空。自由孤立座標仍保留完整染色因子。
共同搬運整圖後固定三個拒絕列

\[
q_0=01212,\qquad q_1=01202,\qquad q_3=01021.
\]

C 始終是原 H−{r,s} 的完整分量。所有原頂點、ordered／shared contacts、
ownership、實際框附件、rotation、bridges、旁支與完整 relations／空 fibres／full lifts
跨列不变；不同列的 witness pins **可以不同**，不得另行正規化分量或框。
沿用前報告的有效圖慣例：「真子圖」指至少缺一條原非框邊；minimal core
忽略自由孤立內點，所有完整染色比較仍保留它們的非空乘積因子。
下文「唯一原G核心」均在這個慣例下陳述，不包含只刪自由孤立點的字面真子圖。

| 依賴 | 本文使用的精確內容 |
| --- | --- |
| [分量必留定理3](c5_excess_two_arc_component_slack.md#5-n2-的全分量必留推論) | 每份 C 刪除全收；非root框附件至多相鄰兩點；每份真 minimal core 恰為 G 減一條原root-spoke |
| [Degree-list 刻畫](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf) | Dvořák 2018 講義 Lemma7／Theorem10：不可染 degree lists 緊，原圖為 Gallai tree，lists 是 incident block palettes 的互斥聯集 |
| [SD-A](c5_degree5_interfaces.md#7-二連通單缺額查證與-4554-接入) | 二連通內圖、恰一完整 degree5，其餘4，拒絕任意 proper β，則該degree5點的內度為2；不要求該圖 β-minimal 或 full B-touch |
| [N45 §2.8–2.10](c5_excess_two_nonadjacent_unit_core45.md#28-限定-high-與兩-short-s-身份的完整覆蓋) | exact-S 的兩short及完整K1–K12的U／long／short，兩owner均已排；另用S05的兩unary排除 |
| [原盾弧引理](c5_unary_shield_budget.md)、[N-diagonal](../artifacts/c5_excess_two_e4/REPORT.md#4-n2局部-diagonal-接回與共同盾弧預算) | 原one-sided pieces的支援弧／互斥收費；short mixed的完整同色pins延拓 |

本輪重新讀取外部 Gallai 原文的定義及 Theorem10；SD-A 的
Cranston–Rabern／disk minor 信任鏈，以及既有 N45 的紙面／外部定理／finite-terminal
依賴仍沿用其已查證報告，未重跑全部上游採納。下述新推論不歸稱外部定理原文。

## 2. 同一原分量在三列下的 block 附件一致性

固定任一 C 及 i∈{0,1,3}。分量必留给 G−C 一份 qᵢ 的**完整**染色。
限制到實際 r,s 得 pins (aᵢ,bᵢ)；若 C 可在這份外部染色下補完，就得到 G 的
qᵢ 染色，矛盾。因此對每列都有 C 的不可染 degree assignment

\[
L_i(v)=\{0,1,2,3\}\setminus
\bigl(q_i(N_B(v))\cup\{a_i:rv\in E\}\cup\{b_i:sv\in E\}\bigr).
\]

完整 degree 四給 `|L_i(v)|≥d_C(v)`。Gallai 刻畫使 C 的 blocks 為 bridges、
奇環或 K₄（更大 clique 違反平面性），且每列各有 palettes Pᵢ,K，
`L_i(v)=⊔_{K∋v}Pᵢ,K`。單點 C 另直接用 degree 式處理。
這是同一原 C 的三份 lists；沒有把不同 pins 的染色相乘。

称 v 為 K 的普通私有點，若 v 不是 C 的割點且不接 r,s。
若 K 是奇環，v 的兩個實際框鄰居必為一條原框邊，且
`L_i(v)=Pᵢ,K`。同一 K 的任意兩個普通私有點，其框邊在三列的色對都相同。
下表的五個 signatures 互異，故這些點的**原框邊相同**：

| 原框邊 | q₀色對 | q₁色對 | q₃色對 |
| --- | --- | --- | --- |
| 01 | 01 | 01 | 01 |
| 12 | 12 | 12 | 01 |
| 23 | 12 | 02 | 02 |
| 34 | 12 | 02 | 12 |
| 40 | 02 | 02 | 01 |

若 K 是 K₄，普通私有點恰有一個框鄰居。同理其原框鄰居相同，因五個框點的
三列色 signatures `(0,0,0),(1,1,1),(2,2,0),(1,0,2),(2,2,1)` 互異。

這裡只需要三列中每列有至少一組拒絕 pins，不要求 pins 跨列相同；
也沒有宣稱不同 blocks 的 palettes 相等。只看 q₀、q₁不足以辨別23與34，
§7 保存同一原 triangle 的負控制。

**原圖的進一步限制：每個奇環 block 至多一個普通私有點。**
若u,v同接ab，由H連通及full B-touch，從`B−{a,b}`取一條首次碰該原奇環J
的路徑，除首條框附件外全走H，端點記x。u,v的全部H鄰居已是兩個J鄰居，
且只碰ab，故x≠u,v。
u–v兩條J弧中，取內部含x的一條；其內點、上述tether及`B−{a,b}`合成連通hub。
另一條弧的內點併入u的bag，形成u–v鄰接。這兩bags、單點a,b及hub互斥，
u/v經保留的第一條弧接hub，hub經剩餘框路接a,b；加ab及四條原附件得K₅。
此minor不縮掉任何未聲明的接點，也不宣稱保完整Σ。

## 3. 末端 block 必有私有 root 接點；原 unit unary 不存在

**引理1。** 若 C 有至少兩個 blocks，每個 leaf block 的非割點中至少有一個
原 root-contact。因此其 leaf-block 數至多為 C 的不同 root-contact 點數，
更至多為原 root incidence 數。割點上的 root 邊不算該 leaf 的私有接點。

*證明。* 反設 leaf block K 的全部私有點都不接 roots，記唯一割點為 x。

- K=K₂：私有葉的完整 degree 四需要三個框鄰居，違反相鄰兩點上限。
- K 是長度至少五的奇環：至少四個普通私有點依§2同接框邊 ab。
  取其中三點，將原環的三段弧分成三個互斥連通 branch sets，縮成 triangle；
  加單點 a,b 及原邊 ab，得到 K₅ minor。
- K 是 triangle xuv：u,v 依§2同接 ab。`H−{u,v}` 仍連通；
  u,v 只碰 ab，故 full B-touch 给剩餘 H 到 `B−{a,b}` 的原邊。
  `X=(H−{u,v})∪(B−{a,b})` 是連通 bag。五組 `{u},{v},{a},{b},X`
  互斥，X經x接u,v，經剩餘框路接a,b，其餘六鄰接來自uv、ab及四條原附件，
  正是 K₅。
- K=K₄：三個私有點 u,v,w 依§2同接框點 a。`H−{u,v,w}` 連通，
  由 full B-touch 接上連通的 `B−{a}`；兩者合成 X。
  `{u},{v},{w},{a},X` 給 K₅，X經x接三私有點、經框路接a。

全部矛盾在原圖的 branch sets 上完成；只作非平面證明，不宣稱保 Σ 的縮圖。∎

**推論1.1。** 原 incidence-one unary U 不存在。更一般，每份 C 至少有兩條
root incidences。

若 U 多block，有限block-cut tree至少兩個leaf，各須不同私有root-contact，矛盾。
若 U 單點，只能有一個root鄰居及至多兩個框鄰居，degree不足四。
若 U 單bridge，兩端各需至少一個root incidence。
若 U 單奇環，除唯一root-contact外至少兩個普通點；長環用三普通點minor，
triangle用上段同一hub，保留接root的第三點。
若 U 單K₄，三普通點同接a，同一hub再次給K₅。
零root incidence已由H連通排除；總incidence一只能是上述unary。

此處沒有得到任意分量大小上界。leaf數上界不能當成內部block鏈長度上界。

## 4. 無 unary 時原內圖必二連通

**引理2。** 在完整§1前提下，若原 unary 數 u=0，H 二連通。

兩份mixed各給一條原r–s路，內點互斥，所以r,s在H的同一個block K₀中。
而 H−r、H−s 都連通：每份mixed內部連通且仍接另一root。
故r,s都不是H割點。

若H還有其他blocks，其有限block-cut tree有一個K₀以外的leaf block K。
K不含r,s，全部私有點也無root鄰居，否則該原root邊會使它不是H的leaf。
K完整落在一份原C內；它仍是C的block，且至多只有原H的唯一割點x是C割點。
K可能是C的leaf block或唯一block。無論x在C內是否仍為割點，
§3的四種原leaf-H-block minor都照用：
私有點只屬此一C-block，且 `H−私有點` 連通。bridge的degree矛盾亦不變。
因此K不存在，H只有K₀，且至少含兩條r–s路的四個點，為二連通。∎

這個引理使用三列及分量必留，不把一般 β-minimality 誤作二連通。
刪任意root-spoke不改H，所以其derivatives有**同一份**二連通內圖。

## 5. 無 unary 的所有 spoke 拒絕均不可能

**定理2。** 在§1及u=0下，對每條原root-spoke e，`Σ(G−e)=Ω`。

反設 X=G−rb_j 拒絕某個原拒絕列 β。X 的完整degrees為r=4、s=5、其餘4，
仍為induced-C₅ disk；內圖就是引理2的H。對X用已查證SD-A，得

\[
d_H(s)=2,\qquad |N_B^G(s)|=3.
\]

任何三個框點在q₀、q₁、q₃中至少一列重色：三點必含非相鄰pair，而五個
非相鄰pairs的重色列依序為13→0、03→1、02→3、14→3、24→0/1。
取s的重色spokes sb_k、sb_ℓ及對應列qᵢ。保留sb_ℓ使刪sb_k不放寬該列的
s禁色條件，故Y=G−sb_k仍拒絕qᵢ。Y的degrees為r=5、s=4、其餘4，
內圖**仍是同一H**。再用SD-A，得

\[
d_H(r)=2,\qquad |N_B^G(r)|=3.
\]

第二次不需要先證Y minimal；SD-A本來就不要求minimality。兩次也不要求
β=qᵢ，更沒有拼接兩份不同列的coloring witnesses。

以下原star幾何不使用44分類。H−r連通，全部落在r三spoke star的一個面中；
full B-touch迫兩個非spoke框點都在該面框弧，所以三spokes連續、star gaps為1,1,3。
共同D₅搬成r-spokes012，該長面的框點是{0,2,3,4}。
H−s同樣連通，s三spokes亦連續，且全在上述面；故只能是234或340。
每份原mixed的actual support必在兩長面的交集，分別為

\[
\{0,2,4\}\quad\text{或}\quad\{0,2,3\}.
\]

兩集合都不含三個連續框點。原one-sided／full B-touch盾弧引理2使long mixed
的actual support包含連續三點，故P,Q都short。這是
[既有雙star幾何](c5_excess_two_nonadjacent_two_mixed_core44.md#2-原支援下界盾弧與新的三-spoke收窄)
在原G上的直接重證，沒有搬用該報告的44身份。

取任一原拒絕三色列及其未用色D。r=s=D滿足全部原spokes，原rs不存在；
N-diagonal給兩份short mixed在**同一**(D,D)下的完整local lifts。
兩份實際分量互斥，接合其完整assignments及原框得到G的染色，矛盾。∎

## 6. 含 unary 的契約覆蓋與全 N2 的55化約

反設任一G−e（e為root-spoke）仍拒絕β。分量必留定理使其任一minimal core
只能為G減一條spoke；包含關係迫它恰是**X=G−e=M自身**。
共同交換roots後e在降度側r，逐項符合[N45§1的exact-S](c5_excess_two_nonadjacent_unit_core45.md#1-全部共同前提與原身份)。
令u為原unary數、ℓ為兩mixed中的long數。以下覆蓋互斥且窮盡：

| 原身份 | 排除及契約核對 |
| --- | --- |
| u=0 | 本文定理2，涵蓋兩short、一long及兩long，不先假設某個split |
| u≥2 | 原盾弧先給u≤2；已採納N45-S05排兩unary的exact-S身份 |
| u=1、ℓ=0 | N45§2.8的完整LOW／HIGH合成，兩short已全排 |
| u=1、ℓ=2 | 同一原圖的U及兩long各收至少兩条互斥盾邊，6>5 |
| u=1、ℓ=1 | 完整原分量恰U/L/S；S支援非空且short，故為pair或singleton。逐項符合K1–K12，再由N45§2.9（owner=r）或§2.10（owner=s）排除 |

最後一行的[K1–K12](../audits/2026-10-10-n45-s-long-contract/REPORT.md#1-原身份十二項契約)
沒有額外的未證形狀前提：K1–K3為本來源；K4–K5來自u=ℓ=1；K6–K7為上述
原e與X=M；K8保真實owner及任意正incidence，不假設unit；K9–K10使用同圖的
全部原資料及其完整relations／fibres；K11為G的Σ-witnesses；K12為X自己的
同β minimality witnesses。沒有從G直接遺傳X minimality，也沒有省略空fibres。
因此這是既有限定結論的完整適用性合成，不以「含long」名稱代替契約。

**定理3（N2全部真核心排除）。** 在§1完整前提下，

\[
\boxed{\Sigma(G-e)=\Omega\quad\text{對每條非框邊 }e.}
\]

分量incident邊由前報告全收；root-spokes由本節全排，且rs不存在，已窮盡原非框邊。
因此每個保B真子圖全收十列；對每個i∈Q(G)，原G自身是唯一minimal qᵢ-core，
其root degrees仍55。這比任意真子圖至多單拒絕更強，但仍不是G的存在或排除。

**共同框附件推論。** 若任何內點同接某個非相鄰框pair，表中至少一個拒絕列
讓該pair重色；刪其中一spoke不改該列拒絕，違反定理3。
所以**包括r,s在內**每個內點至多接兩個相鄰框點。
兩roots的原內度皆至少3；其餘有效內點的原內度皆至少2。
無U時H仍二連通。含U時每份U至少兩個root incidences（§3），不能由此宣稱H二連通。

## 7. 固定控制與重播

[Checker](../scripts/c5_excess_two_arc_leaf_blocks.py)及
[產物](../artifacts/c5_excess_two_arc_leaf_blocks/observations.json)另列有限控制。
它們不重開來源圖搜尋，也不把目標來源零觸發當成定理2／3的證據。
從前報告的63張原圖／179份原分量，獨立numeric-order DFS重新計算十列、
全部16pins的完整local fibres；逐tuple比較後保存原檔SHA、精確JSON pointers、
每個完整fibre集合hash及各cell大小，包括全部空fibres。未重驗原disk rotation。

| 固定控制 | 本輪結果／觸發界線 |
| --- | --- |
| 完整local fibres | 1,790份逐列比較、28,640個ambient pin cells，含3,372個空fibres，全部相等 |
| 三指定列各有local禁對 | 45份C triggered and holds，全部也滿足相鄰兩點附件条件；不表示這些列全圖拒絕 |
| cycle palettes控制 | 17個block觸發，普通私有點對0；leaf-contact block亦0觸發，不能聲稱原來源的非空末端覆蓋 |
| 原框欄位 | 五條框邊signatures互異；全部10個三框點集合均在指定三列之一重色；五個非相鄰pair均有重色列 |
| 正控制 | 固定root-free leaf triangle＋bridge，保存十列160cells及原K₅五bags／十鄰接；這是非平面局部控制，不是disk來源 |
| 撤掉q₃的負控制 | 同一triangle的兩普通點分別接23、34；q₀／q₁均可禁r=2，q₃全部16pins接受；完整160cells保留。較強的兩列說法為counterexample |
| 完整Σ933／941目標來源 | 0張，not triggered；新來源排除依紙面及明列上游契約 |

生成採exclusive create，主產物SHA-256為
`b048d567e287807c8eaafa5aeb17a229457ed9cac1a93c5bcdb802b17c7b206b`。
普通及`PYTHONHASHSEED=17`只讀重播均通過。
[故意毀損產物](../artifacts/c5_excess_two_arc_leaf_blocks/observations_corrupt_negative.json)
及[失敗紀錄](../artifacts/c5_excess_two_arc_leaf_blocks/negative_check.json)保留，
重播以`artifact mismatch`、exit1失敗，符合預期。

```bash
python3 scripts/c5_excess_two_arc_leaf_blocks.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_arc_leaf_blocks.py --check
python3 scripts/c5_excess_two_arc_component_slack.py --check
python3 scripts/c5_excess_two_arc_pair_critical.py --check
uv run --with networkx==3.5 python -B scripts/c5_excess_two_e3_foundation.py --check
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
lake build
git diff --check
```

前兩輪component-slack／pair-critical只讀重播通過，原產物SHA不變；
E3 foundation重播亦通過，原951／935兩圖及完整控制保留，沒有被本輪前提誤排。
`check_docs.py`通過（616 Markdown、7,616 local links），正式docs的DocGraph通過
（62 documents、213 relations、0 errors）；`lake build`通過（8,831 jobs，保留既有
linter warnings），`git diff --check`通過。Build不承擔新紙面證明。
未重跑全部上游分類、N45封存驗收、ES／ER搜尋或含scratch的全工作樹DocGraph。

兩路只讀論證檢查均核回leaf minor、無U二連通、同H兩次SD-A及含U完整契約；
指出的自由孤立點措辭已以§1慣例及有效內點限制修正。這不是新的封存採納流程，
亦不把有限checker的通過寫成獨立紙面證明。

## 8. 精確停止點與傳播

**已收尾的範圍：** 完整§1目標N2契約的全部45／54真minimal cores，包含
原unit unary省略及原root-spoke省略。前者沿既有N45-U，後者由本輪§4–6完成。
原unit unary本身另由§3排除。這不改寫歷史audit當時的OPEN或not-triggered證書。

**仍OPEN：** 同一原G／同一色框、每個拒絕列都以原G自身作55 minimal core，
且每條非框邊刪除全收的共同矛盾。無U時已有H二連通及兩roots內度至少3；
SD-A僅限單缺額，不能直接套到這份雙degree5的G。
含非unit unary的原55亦保留。N1、相鄰、單-root例外、一般E-ARC2及主命題未完成；
沒有新Lean證明或符合全部目標前提的有限來源。

傳播更新N45權威入口、Kempe導覽與STATUS；直接consumer的舊45／54缺口需標示
本輪完整N2範圍的後續涵蓋。README／HANDOFF僅維持既有研究線路由，
不新增研究線或逐輪摘要。沒有commit／push。
直接父題的degree-5 guide／interfaces與雙色唯一缺口報告已補後續涵蓋；
synthesis的E-ARC2段落同步55停止點。傳播停在這些直接consumer及既有跨線摘要；
R31的一般minor、N1／相鄰及E-ARC2父題均保持OPEN，未改歷史audit產物。
