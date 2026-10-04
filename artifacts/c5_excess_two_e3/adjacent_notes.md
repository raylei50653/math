# E3：相鄰雙 root 的移植稽核與共同約束

本檔是 E3 主報告的研究輸入，基準 main `2ddc6b4`。只新增本檔、
[checker](../../scripts/c5_excess_two_e3_adjacent.py) 與
[有限列證書](adjacent_rows.json)。沒有修改共用文件、舊 checker 或舊 artifacts。
本檔不宣告 ε=2 全層成立；尚未閉合的入口列於末節。

## 1. 列身份及證據層

原 `cells.json` 的十列，三色 singleton 身份為
row 0=`01012`/singleton 4、row 1=`01021`/singleton 3、
row 3=`01201`/singleton 2、row 4=`01202`/singleton 1、
row 6=`01212`/singleton 0。E3 所選 941 形三列是 **1、4、6**，
亦即 Q 的指定子集 {0,1,3}。本檔不假定 row 0、3 被接受。
每次整圖 D5 搬運同時搬動全部列、框點、contacts、ownership 與色名。

`adjacent_rows.json` 是有限必要表：十份共同 D5 搬運、十份三-spoke
支援的同色省略見證、十份 pair 的同色列見證、B₂/B₃ 的 actual 外鄰
tightness 表及同框 leaf signatures。沒有枚舉任意來源圖，没有四色定理 oracle，
沒有使用不存在反例的有限搜尋作紙面定理。Gallai 與拓撲的任意大小部分
仍由所連原論證和下文證明承擔，沒有新增 Lean theorem。

## 2. 可移植性表

「局部可直接移植」表示該引理在已列 actual 圖形前提下成立，
不表示固定 933/941 的舊 frame ledger 已涵蓋 E3 的全部來源。
對含未閉合前序身份的工具，明列前序缺口，不把形式上的三列計算稱為整型結案。

| 工具/分支 | E3 移植判定 | 精確列、原身份及限制 |
| --- | --- | --- |
| 原 root 刪除、S_z/S_w 恆等式與至多一份省略-root 例外 | 可直接移植 | T4、完整 degree、原分量飽和與 disk；不讀其餘三色接受位。原 side-degree=5−δ−m_r；相鄰且 mixed 時兩個 root 刪除圖各自 Ω |
| 原 zw 省略：多 mixed、樹、單 triangle、雙 triangle | 可直接移植 | 多 mixed 形成長≥4環；其餘全 degree4 q-core 的原 joint 接回接受 T4 時仍只缺同一 q，違反原 zw 的 Σ-criticality。q 不限 933/941 列 |
| 唯一 mixed 的 proper-core 原 incidence 表 | 可直接移植 | 省略總向量在 {0,1}²；容量≥2 unary 不可省略；(4,4) 保留 C 迫兩側 contact 同是 x，不省略原 zw |
| (4,4) 保留 mixed、双 spoke 省略 | 只需所選三列 | 既有完整接回的 T4 masks 942,956,958,1006,1012,1014,1020,1022 均不含任何 941 形三拒絕子集；亦無932。沿用任意大小原 triangle/roots joint 正常形 coverage，不把 hist 作圖來源 oracle |
| (4,4) 保留 mixed、spoke+unary 省略 | 舊完整證書依賴精確 Σ；E3 留缺口 | 既有 support solver 對十列同時 imposing equality。明示反例式證據：原 form26、root_order=(5,7)、restored spoke=(4,7)、omitted V_at5、target1004，使用 **接受 row3=01201** 排除空列；此列在搬運後所選三列之外。原同類共有12次比較。不能把這步當三列排除 |
| (4,4) 保留 mixed、双 unary 省略 | 通用六邊機制可替代長 mixed 部分；短 singleton 待 K′ | 原 G 至少兩份 critical unary，各盾弧≥2；若保留 C 支援非短，σ_C≥2，6>5。短支援且兩 root contacts 同一 x 的任意大小分量由 §3 化至 singleton 四色外鄰，為 K′ 的精確輸入。原完整 shape solver 仍是 exact-target 證書，不直接提升 |
| (4,4) 省略唯一 mixed incidence-(1,1) | 舊完整證書依賴精確 Σ；E3 留缺口 | `mixed_omission` 令每列 bool(K−F)=target bit；同原 support 的跨列禁對 transport/收縮星本身通用，但原 zero-residual 含可選三色接受條件。須改成三列必要 constraints 才能登記 E3；不重跑逐 key 表 |
| 單 spoke 省略自己為 unique-degree5 q-core | 條件移植 | 需先排除相應 (4,4) 身份。省略圖自己 ε=1 時可用 E2 相鄰列分離；不能在未解 spoke+unary/mixed omission 前宣稱所有 G−e 自己 minimal |
| 五-spoke 原來源全排 | 依賴精確接受/拒絕對；E3 留缺口 | 原八份搬運至 masks998/1004、a-spokes123、b-spokes14。leaf-fibers §3 用 **p_A=01021 與 p₂=01201 恰一收一拒**，得 U singleton0。三列假設允许兩列皆拒絕，故该二列不等身份未推出。原雙列 U palette/K5 引理本身通用 |
| (3,1)、mixed11+两份單接點 unary | 可直接移植 | 原三份 pieces、critical contact witnesses、共同原外路徑與六跨度 2+2+2>5；原 singles §4 明言不需特定拒絕位置、T4、q-minimality |
| (3,1)、mixed11+一份 binary unary | 同列 hub 引理可直接移植；整型 coverage 條件移植 | hub 只需 U 的同列拒絕、同色端點 tightness、原外部三 bags。指定 S_a012、S_b2、S_C04、S_U234 用 **row1=01021**。旧32/64 domains 来自省略圖自己 minimal，E3 前序身份仍須补齐 |
| (3,1)、mixed12+一份單接點 unary | 同列 active-triangle 可直接移植；整型身份留缺口 | 刪同色 a-spoke後 K=C+a 是原三 contacts(a,y0,y1)，指定012/2 用 **row1=01021** 得 F_K={2,3},F_U={1}。舊 M 自己 q-minimal 用已排(4,4)spoke+unary；該前序在 E3 尚未補 |
| (3,1)、mixed13、無 unary | **只需所選三列；整個 incidence 子型可移植** | 不需 q-minimal/Σ exact/embedding。十份三-spoke 支援各有一份 **row1/4/6** 同色 query，K=C+a marked leaf 的 list2>degree1，取合法 b 色即貪婪延拓。新 checker 保存每份 actual spoke witness；包含 root 交換 |
| (2,2)、mixed11+各側一 unary，共用 pair | 局部可直接移植 | 原 diamond 封 C 到固定三角，完整 C 延拓任一合法三角外染色；可用固定 ax 的 witness 替換表達非critical，不需要確切拒絕列。旧Σ(G−C)=Ω依赖mixed omission，E3不借该上游结论 |
| 同子型，原短 face/同一長 face/原 crosscut | 局部可直接移植 | 短 unary 與共同面 actual 支援次序及外路證明不讀特定拒絕集合；crosscut 後二/三 hubs 需原完整 tightness、实际外路逐項核對。不能以數量预算虚设hub |
| 同子型，原941共用短框弧 | 只需相應所選三列 | canonical02/03 用 **row1=01021** 完整 joint 延拓；原IDs155,175用row1，179用row4，239用row6，243,263用row1。F_C empty 是共同根色避色，不宣稱所有異色 roots 可延拓；六角色原 witnesses 保持 |
| 同子型，不相交 pairs | 局部可直接移植 | 原短 face 或兩份 unary 共同框弧跨度≤2，但各≥2；不讀拒絕列。舊47/75整型 ledger 的前序 necessary-frame coverage依 exact-target(4,4)輸入，E3暫不把整个0/0当已证 |
| A：mixed12+a-unary，原 identity/N 全收/singleton U | 條件移植 | ternary/完整 six-role identity、active-triangle 與 singleton直積引理通用；N/U/spoke 省略图自己 minimal 需要先补对应(4,4)spoke+unary。不能先套旧N=Ω |
| A 原01/23來源排除 | 只需三列，但須補前序 N 全收 | **row1=01021、row4=01202、row6=01212**；S_U⊆034 上完整同色框換色+未用色membership守恆矛盾，不需额外row0/3接受 |
| A₂ 原01/12 | 只需三列，但須補前序 N 全收 | **row4** 迫 U={2}；若無actual2附件，用 **row6↔row1** 的(1 2)搬運矛盾。原actual crosscut封C到{1}或{2}後，row4完整joint延拓 |
| A₃ 原01/01 | 局部C替換可直接移植；指定列出口需前序singleton身份 | critical U 與fullB-touch迫U含234；C封於{0}或{1}後原三hub回復ax，不讀exact mask。**row4=01202** 的 U singleton2/3完整joint可重用，但不能先假定 N全收 |
| A₄ 原04/04 | 同 A₃ 的範圍 | critical U 與fullB-touch迫U含123；C封於{0}或{4}。指定列 **row4=01202** 的 U singleton1/3可重用；四份rotations與实际支援不跨列改選 |
| B：mixed22、無 unary 的四spoke省略Ω及 G 自身(5,5)q-core | 可移植至三列前提 | (4,4) 唯一可能省略兩spokes，已由上表直接双spoke必要域排除；C incidence(2,2)不能省略。省略後 unique5 two-spoke三contactsactive-triangle排除。旧spoke pair必要域可重新由十份pair表只用三列推出：每個非框pair有选定同色列 |
| B₂ W933-101/W941-139，原01/23短face12 | 只需 **row1、row6**；可獨立移植 | row6=01212排a-only接2與b-only接1；row1=01021的兩合法pins(3,1),(2,3)区分四owner列表。tightness/Gallai叶+原五bags不需其他三色接受；新checker重新得到原全部actual附件表 |
| B₃ 同原01/23長face043 | 只需所選三列；可獨立移植 | row4=01202排nonowner03附件；row6排shared額外0；row1排shared3/4。row1兩pins的五個joint list signatures單射；terminal leaf pair及原外路K5均保留。單列row1不足 |
| B₄ W933-129、原04/12、shared实际附件{4} | **主要 cut parity 引理可直接移植** | 原 genuine shared leaf v、C incidence(2,2)、C−v非空連通，原 degree4給 4|K|=2|E(K)|+3+n_B，迫 actual K−B邊；五bags {a},{b},{v},B,K直接K5，**不需任何拒絕列**。旧13附件slack縮表另用933的第四拒絕 **row3=01201** 排t接3，但此表不是主排除引理前提 |
| 盾弧引理1/2、定理A | 可直接移植 | 純面拓撲+H連通；fullB-touch由任何兩個不同所選拒絕列+T4推出。Σ-critical原 unary接线的witness只需任一拒絕列，或主報告的三列critical改進 |
| hub原則定理B、B2 roots同色 | 可直接移植相應原hubs前提 | 不讀mask；相鄰roots在完整合法外部染色不同色，不能据此自动构造四個K4 hubs；935的短mixed正控制必须留下 |
| 定理 C-W，原共鄰端點mixedP3 | 局部可直接移植；q-core來源套用需分開 | 共鄰endpoint、原(3,2,1)附件色、每個root至少一unary及q-critical。修補后的零-unary侧排除只用q-critical。不是任意Sigma-critical图都q-critical；E3须在所选q自己的core驗前提 |

## 3. 短支援、共用 contact 的共同約束

**引理（沒有 ε 或特定列假設）。** 設指定 disk 外框 B，H 連通且碰齊 B，
a,b 是相鄰兩 roots。P 是 one-sided degree4 原 mixed 分量，
兩側 incidence 各一，且**同是原 contact x**；实际 S_P 包含於一条原框邊 hk。
若某份原合法 P 外染色不能延拓 P，则 P 必为 singleton{x}；这时完整 degree4
迫 x 实际接 h,k，且 h,k,a,b 的外鄰色四色互異。

*證明。* 固定同一份拒絕 pin，P 的 exact degree lists 至少为 deg_P；
生成樹slack引理迫 tight。Gallai 外部定理給 P 的 block结构。
X=B∪(H−P) 连通：H−P连通且fullB-touch及S_P⊆{h,k}迫外部碰B−{h,k}。
K4 block 每点唯一原外方向，若是bridge，有限Gallai外侧的terminal private点
deg_P≤3迫实际X附件；四互斥原方向到连通X给原K5，所以没有K4 block。

任何没有 x 作private点的 terminal bridge，其private叶必须有三个实际
框邻点（完整degree4、原内部degree1），违反S_P⊆{h,k}。
没有x-private的terminal odd cycle有两个相邻private原点u,v，原内部degree2，
故它们都实际接h,k；剩余P−{u,v}连通且包含x。
取原图五袋 {u},{v},{h},{k},
O=(H−{u,v})∪(B−{h,k})。
O连通：剩余P通过原x-a/x-b接H−P，后者接B−{h,k}的全部三点；
u,v各有原cycle边接O，h,k各有原框补弧边接O。
四个singleton构成原K4，得到全部十份原邻接的K5矛盾。

如果至少两个blocks，至少两个terminal blocks，其中至少一个没有唯一
contact x 作private点，已排除。只一个bridge同样有非contactprivate叶；
只一个oddcycle有两个相邻非contact点，仍用同五袋（剩余cycle包含x）。
所以只剩 P={x}。它原邻点就是a,b及两个不同实际框点h,k；固定pin拒绝x
当且仅当这四邻色互异。∎

这份论证的外部Gallai依赖是
[Dvořák, Lemma7/Corollary8/Theorem10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，
采用 E2 已核對的精确版本。Python 没有声称证明Gallai或拓扑。
正控制935的原mixed就是singleton，故本引理允许它的四色外鄰拒絕；
951沒有相鄰雙root設定。实际控制核對由主報告的 E3 controls checker承擔。

**對雙 unary 的作用。** (4,4)保留原mixed core时，全degree4分类迫两侧contact
共用x。若原G又有两份unary，各长盾弧≥2；mixed非短支援会再收费≥2，
6>5。短支援混合由引理化至 |P|=1、四色外鄰，正是「待 K′」的输入。
本檔不執行任何 K′ chain partition/transport 計算。

## 4. E3 的精確剩餘入口

本檔已登記相鄰generic root/zw 化约、三列双spoke(4,4)排除、
(3,1)mixed13無unary整型、B 的身份与 B₂/B₃兩个指定01/23 faces、
B₄实际shared leaf及上述短共contact新引理。
没有宣称其他branches只等K′就全关。

仍需补：

1. 唯一mixed的(4,4)spoke+unary、只省略mixed身份，及其对单spoke/M自己minimal的依赖。
2. 五-spoke：上述两指定列相反接受性不能从选定三列推出；应改用同图三列criticality新约束，或分开指定第四列/精确mask分支，不能硬套旧(7)。
3. (3,1)binary/ternary整型的必要frame覆盖以及上述省略身份；局部hub/active-triangle引理保持可用。
4. mixed11+两unary的旧47/75 necessary-frame覆盖：局部七机制可逐项移植，但完整覆盖含旧前序exact-target输入，不能据0/0直接宣布E3全排。
5. A剩余mixed12 frames、B剩余mixed22 faces/身份；更少spokes、多mixed、no-mixed，以及原(5,5)core尚不能从本表排除。
6. 短one-sided mixed：|P|=1且N(P)四色、adjacent degree5 roots，**待K′**；|P|≥2且不同原contacts、其他incidence的短支援仍是本任务自身缺口，不混同待K′。

没有开始逐key新枚举，也没有为修补旧exact-target表改写历史产物。
旧archive只读，路径在原工作区 `/home/ray/developer/ai/math/artifacts/`；
新worktree缺这些ignored artifacts，沒有复制/还原进旧路径。

## 5. 本 checker 的實際執行

```text
python3 scripts/c5_excess_two_e3_adjacent.py                       exit 0
python3 scripts/c5_excess_two_e3_adjacent.py --check               exit 0
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_e3_adjacent.py --check   exit 0
```

普通与seed17的artifact SHA256同为
`3a339495538988b425f718d8c6c5fa6fba2616c7eed62a8ee4480a800511389c`。
该byte-check覆盖新row表；不宣称重跑原大checker。全局文件/DocGraph/diff
实际执行与exit code由主 E3 报告统一记录。
