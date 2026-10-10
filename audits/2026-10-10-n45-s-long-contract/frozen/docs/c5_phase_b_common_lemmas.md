# Phase B：共通引理候選的反例與可推廣性

**後續（2026-10-09）：** [N45原unit省略45／54](c5_excess_two_nonadjacent_unit_core45.md)
已採納指定省略身份的窄排除與低incidence支援下界；§2.1效益與§3.2控制入口隨之更新。
以下2026-10-08當輪證據及一般候選界線保留，未排全部45／54／55或一般N2。

2026-10-08；輸入基準 `3f2731b7225d35e12872177eb00d3a5b24aa6468`。
接續 [Phase A 結果對照與共通語言](c5_common_language.md)，比較三組機制，
交付候選陳述、最弱已知充分前提、反例、證明義務與可能消除的分支。
「最弱已知」指現有證明實際需要的充分條件，不宣稱邏輯上的最弱條件。

**目前 U1–U4 已在固定完整 Σ933／941 下完成兩-root `(4,4)` 身份排除。**
仍保留 45／54、原55、單-root例外、無44來源、E5的新證明義務、ε≥3、
一般出口及操作充分性；詳見 [Kempe 導覽](c5_kempe_guide.md)。
本輪沒有新增這些分支的來源排除。新增成果是共通接口、§3.2的紙面容量
恆等式推廣，以及兩張反駁過強容量結論的**非平面** q-critical 圖。

## 1. 三組候選的取捨

| 組別 | 可用的共同定理接口 | 真正未證的升級 | 反例壓力 | 若升級成立可消除的範圍 |
| --- | --- | --- | --- | --- |
| U1–U4／Weak-deletion | B-S0：同一原圖上的有見證盾弧收費；省略 piece 仍付原費用 | B-S1：固定Σ933／941的每份 one-sided mixed 都有長盾弧 | S935短mixed；C44-AD3的44 core；q-core singleton缺點 | 至少三份 one-sided pieces 的來源，不限ε／root數；分隔型另處理 |
| Excess／Mixed／No-mixed | B-C1：條件完整介面的 `D+O(+κ)`；B-C2：任意兩自由roots的逐欄容量等式 | B-E：跨拒絕列的 `ε≥|Q|+c(Q)−2` | degree6有unary重疊或D=2；加孤立點破壞錯誤ε約定 | 933／941整個ε=2來源樹，包含45／54／55、單-root與無44型 |
| Relation／Repair／State | B-RS：密封外部上下文可反覆使用；B-RW：同weak exits推出weak bisimulation | B-RD：合法性、後繼及染色fibres均由同一摘要決定 | 第五port、刪內邊、同Σ不同單步、同R不同幾何續接 | 指定grammar內的多步state合併與操作式repair；不自動給完整grammar／來源分類 |

三組均固定原圖對應、有序contacts、actual attachments、ownership、bridges、
cyclic order與共同字面色框。關係先取完整joint再投影，保留空fibres。
靜態可延拓、從指定染色可達、source排除、有限域無反例分開記錄。

## 2. U1–U4 與 Weak-deletion：原圖收費與臨界見證

### 2.1 B-S0：有原見證的共同盾弧排除準則

**陳述（既有紙面證明可抽出的充分接口）。** G為有限簡單disk圖，
有序induced-C₅外框B；有效H非空連通。取同一G中的互斥、非空連通
原piece族𝒫，每份滿足 `H−P` 非空連通，即one-sided。
令 `K_P=B∪G[P]∪E(P,B)`，F_P是包含H−P的面，
`σ_G(P)=E(B)∖E(∂F_P)`。取三個互斥子族：

- 𝒰：unary U，`N_H(U)={r_U}`，每點完整 `deg_G=4`；有合法
  `ψ_U:G−U→Col`不能接回整份U。若其支援包含於某條框邊兩端，
  可選這樣一條ab及同一G的 `r_U→h` 外路，h在B∖{a,b}，內點避開U與B。
- 𝒧：非𝒰的pieces，已核實際支援不包含於任一框邊兩端。
- 𝒮：非前兩族的pieces，已核實際支援恰為某條框邊兩端。

則

\[
  2|\mathcal U|+2|\mathcal L|+|\mathcal S|
  \le \sum_{P\in\mathcal P}|\sigma_G(P)|\le5.
\]

因此左側超過5即排除這份來源。沒有支援下界的mixed不先付一單位；
singleton支援可能只有零長盾弧。同一unary不能再在𝒧重複收費。
任意 `M⊆G` 抽取或省略原piece O，仍以原 `σ_G(O)` 收費，
沒有聲稱 `σ_G(O)=σ_M(O)`；O可能根本不在M中。

**證明及最弱已知充分前提。** one-sided與同一disk給盾弧邊互斥；
原支援的面標記給𝒧費用≥2、𝒮費用≥1。unary若短，原外路与
拒絕見證構造二／三個互斥連通、兩兩相鄰且在N(U)上常色的hubs。
完整degree4與拒絕迫lists tight，沿用外部Gallai／hub原則得K₅ minor。
故每份unary也付≥2。依據 [原盾弧定理A／B](c5_unary_shield_budget.md)、
[W-A／C-W](c5_qcore_shield_budget.md)。一般q-minimal、Σ-critical或T4
均可被上述**逐piece的見證與外路**代替；外部Gallai依賴仍在。

見證供給有兩種：q-critical接點邊刪除給同一q的外部染色；Σ-critical
接點邊則先指定其新接受列β_e，再限制到G−P。各piece可用不同β_e：
幾何收費在同一G，並未把跨列禁色需求相加。這不把Σ-critical變成
「原G對某個共同q已minimal」。§5的小控制重新確認S935甚至沒有任何
一列使原G成為q-minimal。

**不可省的例外。** 對 `|S_P|≥2` 的one-sided P，固定Σ來源碰齊B時
可用 `S_P=V(σ_P)`；同樣在 `|S_P|≥2` 下，q-core＋T4只保證
`S_P⊆V(σ_P)⊆S_P∪{s(q)}`，盾弧內可能有
未接內點的singleton位置。這不破壞邊互斥，但禁止直接搬「實際支援連續」。
若不保拒絕見證／原接點criticality，三份看似應付兩單位的pieces也可能
實現；[D₆校準](../audits/2026-10-04-task-d6/calibration/REPORT.md)
保存接受q的控制與拒絕q但18條unary相關邊非critical的控制。

**剩餘證明義務。** 將每個core factor映回原piece；核它是整份省略或
片段省略、完整degree、one-sided、actual support、拒絕見證與避開自身的
外路。root-disconnected的分隔piece須有另一份預算，不能冒用本式。

**分支效益。** C-W的 `2+2+2>5` 已關閉共鄰P₃的3497個後續keys；
U4原省略O仍收費的原理可共用。[N45](c5_excess_two_nonadjacent_unit_core45.md#2-已採納結論與必要化約)
已在完整Σ933／941、指定45／54原unit省略身份內補出兩short分支的低incidence支援下界，
用 `1+1+2+2>5` 排兩原unary；含long時用 `2+2+2>5`。整U省略另排兩short，
後續[LP紙面排除](c5_excess_two_nonadjacent_unit_core45.md#21-n45-u-lp-的任意大小排除與信任界)
已在原2+2+1及整U省略45／54身份內採納；後續[SS及限定U覆蓋](c5_excess_two_nonadjacent_unit_core45.md#22-n45-u-ss-與指定整-u-身份的完整覆蓋)
排掉singleton-support支，與既有化約合成排除指定整U省略身份。
後續[LOW1完整U映射](c5_excess_two_nonadjacent_unit_core45.md)在原U incidence1、僅刪原r-spoke且X=M的完整契約內
接回BASE三接點任意大小排除；[LOW2及限定LOW覆蓋](c5_excess_two_nonadjacent_unit_core45.md#24-n45-s-low2-與指定-low-身份的完整覆蓋)
另保原U雙contacts與cycle，r無框邊的原tethers逐項成立。LOW1／LOW2只合成排除§1精確S-SHORT-U-LOW，
後續[HIGH1完整契約](c5_excess_two_nonadjacent_unit_core45.md#25-n45-s-high1原-k₃₃-與同列完整-g-lifts)
另排原U incidence1在s、s兩spokes全留且X=M的spoke身份：原K₃,₃九鄰接、原U三點support
與同列未用D的完整G lifts給矛盾；BASE／外部Gallai明列。
後續[HIGH2／HIGH3與限定兩short覆蓋](c5_excess_two_nonadjacent_unit_core45.md)
另核原雙U-contact、完整W assignments／r fibres恢復e，未用Dγ構造只限proper三色γ；
原過寬量詞保finding，全部properγ的JOIN／RESTORE／PALETTE不縮窄。HIGH3原s無spoke、
實際(2,3)接回BASE no-spoke原K₅排除。LOW兩支及HIGH三支逐契約窮盡，
只關§1精確S的兩原mixed都short身份；含long、其他cores／一般N2／E仍OPEN，無新finite來源或Lean。
這只搬用原B-S0及各自新充分前提；一般N2仍只知mixed非空支援，
singleton總incidence≥4未排，不能把U4專用 `2+ℓ+2u≤5` 直接搬過去。
原省略unit若是spoke，保其原邊限制；spoke不能被冒算成piece盾弧。

### 2.2 B-SD：短mixed的同色pins局部延拓

**陳述（由既有證明推出的接口）。** 在§2.1的有限簡單disk G與外框B內，
P連通、每點在原G中完整degree4；
所有內部外鄰均為具名roots。P是one-sided，`S_P⊆{a,b}`且ab是框邊，
H−P實際碰齊B∖{a,b}。則對每個proper框列β、每個c∈Col，
把全部相鄰roots固定為c後，整份P有局部延拓，使P內邊及全部P–外部邊合法。

這是 [E4 N-diagonal](../artifacts/c5_excess_two_e4/REPORT.md) §4.1
的hub／tight-list證明；ε、root degree、criticality不參與這一步。
它不要求指定pins先能延拓到整個G−P；hubs的其他內部顏色不影響P的lists。
拼回G另須pins合法於root骨架並滿足其餘完整原relations。

**反例壓力與缺口。** 相鄰roots的同色pins違反原root邊，故此接口可能
完全沒有合法整圖用途。兩非相鄰roots則提供對角接受，但不能保證
`E_z(β)∩E_w(β)`非空，也不能排off-diagonal拒絕。45／54仍需完整
unary與兩mixed共同joint。此接口不構造從指定source染色出發的repair。

### 2.3 B-S1：固定目標來源的所有one-sided mixed都長

**候選（未證）。** G是固定完整Σ933／941或整圖D₅像、Σ-critical的
induced-C₅ disk來源，忽略孤立內點；每份one-sided原mixed P都滿足
`|σ_G(P)|≥2`。不限制ε或root數；對應原[猜想S](c5_research_synthesis.md)。

**反例。** [S935／P0={5}](../artifacts/c5_shield_calibration/counterexample_S935.json)
是T4全收、Σ-critical、ε=2的disk，roots6、7相鄰，P0完整degree4，
H−P0=67連通，支援34且盾弧只有34。拒絕列01201在G−5有
`(0,1,2,0,1,_,2,3)`，四鄰3、4、6、7用齊四色。
它否定「只需一般T4全收來源」版本；Σ935未觸發固定933／941前提。

**缺少義務。** 必须從兩目標的多列拒絕迫短mixed矛盾；同色hub原則
只排同色拒絕見證，異色roots的linkage／Kempe阻擋尚缺。
若成立，B-S0一次排掉所有至少三份one-sided pieces的來源，包含
mixed＋兩unary、兩mixed＋unary、三mixed。root骨架連通時所有pieces
one-sided；分隔型、只有兩份mixed且無unary、原55均不因此自動全排。

另一個過強版本「一般ε=2來源沒有兩-root44 core」已被
[C44-AD3-row0-44](../artifacts/c5_excess_two_c44/counterexample_C44-AD3-row0-44.json)
反駁：原Σ956、roots5／6完整degree5；省略7的q=01012 core中
兩roots各degree4，均被三spokes迫色3，原邊56衝突，七條非框邊各有
q刪邊見證。U1–U4的完整目標Σ前提不能移除。

## 3. Excess 與 Mixed／No-mixed：已有任意root容量，欠跨列付款

### 3.1 B-C1：完整條件消去的超額恆等式

**No-mixed已證版。** 固定q逐非框邊minimal圖，H非空連通，非空R恰為
完整degree≥5內點，其餘degree4；每份原C恰接一個root。
令Q=G[R]、k_C為接點數，F_C為非空完整tuple關係的共同禁色，
`E_r=Col∖(q(N_B(r))∪⋃F_C)`，則

\[
D_r+O_r+\kappa_r=\deg_G(r)-4,\qquad
\kappa_r=\deg_Q(r)-|E_r|\ge0,\qquad
\sum_r(D_r+O_r+\kappa_r)=\varepsilon(G).
\]

`D_r=Σ(k_C−|F_C|)`，`O_r=Σ|F_C|−|⋃F_C|`。
不需disk／T4／固定ε或root數；Q是樹時κ=0由初等edge-label引理給出，
一般骨架的block推論才另用外部Gallai。
κ是骨架list缺額，不是環數。[原證明](c5_root_degree_excess.md) §1–5
也說明target p必須重核spoke單射、F避spoke及κ非負。

**Mixed已證版。** 不要求q-minimal；固定一個拒絕列q、一個r及
`f∈Col(G−r;q)`，令η=f在其他roots的共同pins。C仍是原degree4分量，
所有root contacts／共鄰identity保留；完整條件tuple集T_C^r非空，給禁色F_C^r，
但F_C^r本身可空。
將每條r至B／其他root的singleton禁色作为**分開具名**factor，與F_C^r
合併計重疊O，則

\[
D_r+O_r=\deg_G(r)-4.
\]

若該條件fibre可填入r，正確式子多一項 `+|E_r|` 在右側。
此局部恆等式的最弱已知前提是共同外部f、完整tuple消去與原incidence計數，
不需Σ933／941；f已給tuple非空，degree4的slack是對其他pins保非空的較強接口。
Σ-critical為每個r供應至少某列／某f，不供應所有r共用同一q、η。
O含重色spokes與root邊，與前段O不同，不能相加後當成一份共同染色。
見 [包含mixed的原條件預算](c5_independent_support_capacity.md) §2–3。

### 3.2 B-C2：任意两自由roots的條件逐欄容量定理

**陳述（本輪從既有容量證明推得的紙面一般式，未Lean化）。**
任選兩個自由roots r,s，固定同一proper框列β及其他roots的共同pinsη。
所有原C內點完整degree4，保全部原接點、附件與完整tuples。
只按對r／s的接線把C分成relative-unary／mixed；C仍可接其他已固定roots。
不接兩自由roots的分量及外部限制須已有合法填入。

令 `χ=1[rs∈E(G)]`。每條r至B或已固定root的原邊提供一個singleton
禁色factor；relative-unary各提供完整禁色F_D。令

\[
D_r^u=\sum_{D\ {
m unary}}(n_D-|F_D|),\quad
O_r^u=\sum_{F\ {
m external/unary}}|F|-|\bigcup F|,\quad
E_r=\mathrm{Col}\setminus\bigcup F,\quad
m_r=\sum_{C\ {
m mixed}}k_C^r.
\]

假設這份固定外部pins下的**完整兩root接合拒絕**且E_s非空。
對每個 `b∈E_s`，令G_C(b)為原mixed C禁止的r色欄，
`V=⋃G_C(b)`，`A=E_r∖{b}`（χ=1）或A=E_r（χ=0），並定義

\[
\delta=\sum_C(k_C^r-|G_C(b)|),\qquad
o=\sum_C|G_C(b)|-|V|,\qquad \lambda=|V\setminus A|.
\]

則各項非負，且

\[
\boxed{D_r^u+O_r^u+\delta+o+\lambda
=\deg_G(r)-4-\chi+\chi\,1[b\in E_r].}
\]

**證明。** 固定所有其餘root pins及s=b，暫不固定r；逐點有
`|L_C(v)|≥deg_C(v)+1[v∈P_C^r]`，每個r-contact保一份strict slack，
故整份連通C可染，`|G_C(b)|≤k_C^r`。
完整接合拒絕给A⊆V，於是 `δ+o+λ=m_r−|A|`。
保每條外部邊的重數，degree計數給
`|E_r|=4+χ−deg_G(r)+m_r+D_r^u+O_r^u`。代入
`|A|=|E_r|−χ·1[b∈E_r]` 即得等式。這不是把端點marginals相乘。

**最弱已知充分前提。** 同一β、η的完整fibre、其他限制可填入、
拒絕及E_s非空、degree4的slack与原incidence計數；不需disk、T4、
q-minimal、ε=2、兩roots總數或特定root度數。Σ-critical可選一條
r-incident邊的新列見證，捨去r再令s自由，提供某份符合前提的fibre。

相鄰且deg(r)=5時右側至多1。原[Mixed容量報告](c5_mixed_capacity_contacts.md)
另用q-minimal給unary各有私有色，最多三個unary incidences迫O=0，
才得D≤1與十八側型。**一般root度數不能沿用這兩個特殊結論。**

**具體反例（本輪新增並獨立驗證）。**
[輸入](../artifacts/c5_phase_b/capacity_inputs.json)及
[完整證書](../artifacts/c5_phase_b/controls.json)保存兩圖：

| 具名圖 | 原degree／ε | r=5的兩份原unary | D／O | 被反駁的過強版本 |
| --- | --- | --- | --- | --- |
| B-CAP-OVERLAP-D6 | roots5／6為6／5，其餘4；ε=3 | K₂(8,9)、K₂(10,11)，禁色{0,3}／{1,3} | 0／1 | mixed存在便一定unary無重疊，與root度數無關 |
| B-CAP-DEFICIT-D6 | roots5／6為6／5，其餘4；ε=3 | triangles(8,9,10)、(11,12,13)，各兩contacts，禁色{0}／{1} | 2／0 | mixed存在便一定D≤1，與root度數無關 |

兩圖都有原zw邊、共鄰mixed singleton7，q=01012拒絕，全部29／33条
非框邊刪除均接受同一q。完整Σ分别266／0，不收T4，且原邊路徑證書
分别給K₅／K₃,₃ subdivision；**不是disk、猜想E或933／941反例**。
它們觸發B-C2並滿足修正式，否定只保留原非平面容量前提的過強推廣。

**欠缺與效益。** B-C2统一相鄰／非相鄰、mixed／relative-unary容量的
證明模板，可對45／54／55或更多roots的具名pins核容量。
它本身不迫任何target延拓，也没有跨β、η的費用不重用定理；因此没有
新增整分支排除。單份shared-contact mixed每行／每欄至多一格的機制
可沿用，但U4的整型碰撞需要那份core之外的具體延拓見證。

2026-10-09的χ0／兩mixed固定控制另由[N45-J](../audits/2026-10-09-n45-j/REPORT.md)與
[SU-J](../audits/2026-10-09-n45-su-j/REPORT.md)核完整fibres／逐欄等式；
本頁原checker域不改。N45 degree4拒絕core給每欄五項零的新paper應用見
[N45權威入口](c5_excess_two_nonadjacent_unit_core45.md)；精確N2來源控制仍0觸發。

### 3.3 B-E：把條件容量提升為跨列超額–拒絕定律

**候選（原猜想E，任意大小未證）。** 有序induced-C₅ disk圖G，
T4全收、逐非框邊Σ-critical，僅計有效內點；Q為被拒絕的三色singleton
位置，`1≤|Q|≤4`，c(Q)為在C₅上的弧段數。則

\[
\varepsilon(G)\ge |Q|+c(Q)-2=2|Q|-e(Q)-2.
\]

**已知前提／反例狀態。** [ε≤1層](../artifacts/c5_excess_one_e2/REPORT.md)
有任意大小紙面證明；[k≤5的310類](c5_excess_rejection_law.md)及
[ε=2、k≤9的179 critical orbits](c5_excess_two_independent_search.md)
是有限無反例證據，本輪未重跑兩個搜尋。S935是ε=2、三點弧Q的緊正控制，
不容許把所有兩-degree5結構都排掉。若錯把孤立內點計入ε，加一孤立點
就使ε減4而Σ及criticality不變，立刻反駁該錯誤版本。

**缺少義務。** 要在同一G上對多列q-core建立費用不重用：包含／省略
原因子、critical-edge解除哪列、不同列共用root及完整附件都須追蹤。
只知道各root一份 `D+O(+κ)`等式，或q-cores两两相交，均不提供
跨列的單一共同見證／全體共同root。還需把禁色需求連到同一盾弧預算；
存在混合／分隔pieces、非樹root骨架與空fibre時須另證，不能把五邊預算
對每個root複製後相加。H2的root樹跨列分離另缺半樹共同訊息搬運。

**可一次消除。** E給933的四點弧與941的兩點弧＋孤點均需ε≥3，
故所有ε=2身份，包含剩餘45／54／55、單-root与無44來源，一次為空。
它不排ε≥3來源、不證一般出口或 `K∞=K≤5`。

## 4. Relation 與 Repair／State：密封合成與動態匹配

### 4.1 B-RS：完整介面等價的反覆密封上下文定理

**陳述（已證靜態接口及有限次直接推論）。** 固定具名介面I、共同色框，
兩piece的完整extension relations相等，私有點與外部互斥，所有跨界
接線只經I，附件映射相同。每次未來操作僅修改／讀取外部，密封私有點
不再暴露，則任意有限次這類操作後，全部外部染色及其觀測仍相等。

最弱已知充分前提是完整關係、具名附件、private independence與密封；
不需ε、root數、degree、disk、criticality。允許任意pinning外部relation時，
完整R相等也是必要。每次apply
[sealed_congr／cap_sealed_replacement](lean_sealed_four_port.md)，或
[LocalClosure replacement／seal_future](local_closure.md)，再歸納即可。
若还要保持disk操作合法性，必须另保幾何continuation語義。

**Repair精確接口。** 同J再加同可用框族𝓕才固定P；对相同候選條件
K_λ且 `J⊆P`、`J⊆K_λ`，
`P∩⋂K_λ=J iff ⋃(Δ∖K_λ)=Δ`，Δ=P∖J。
[CommonRepair](lean_common_repair.md) 的全部role分類還需三類相對
**全部候選Λ**的exact-rejector witnesses及兩類cover等式。
Ω、Λ均可無限；W／C角色模板及其極小分類不需有限Λ，有限Λ只供一般
从任意repair抽取極小元的步驟。P=J保留空repair退化支。
这是集合條件修復，沒有刪邊／Kempe可達性的量詞。

**具體反例。** D₁₃與wheel四port等價；D₁₃染色
`0101120102321`的前五點01011不能延拓wheel，因wheel原邊1–4同色
（`cap_center_not_preserved`）。D₁₃刪內邊4–6後染色
`0123202121031`接受rainbow四port0123，原piece則拒絕
（`cap_missing_edge_rainbow`）。後者表示刪內邊超出sealed定理，
沒有證明兩來源的完整weak exits不同。

同J而框族不同也可使P不同：新抽象控制用 `J={00,11}`，兩singleton
scopes給P={00,01,10,11}，全scope給P=J；不主張它是disk實現。
真實兩私有核心的[repair-family transport](c5_two_vertex_repair_transport.md)
也不能據同repair形狀搬完整J／P／排除集合。

**欠缺與效益。** D₁₃任意層來源族須持續核ownership、具名附件及
所有可用C₅框。完成這些圖層義務便可统一替換族的J/P與repair傳遞，
不需逐代表重證關係代數；其他不可化約來源、改寫完備性与換色repair仍留。

### 4.2 B-RD：允許操作與完整fibre的多步充分性

**候選充分準則。** 固定action grammar Γ、對其steps封閉的歷史域D，
摘要 `s(h)=(具名live interface,共同frame,完整R_h,幾何residual E_h)`。
保共享實體identity及重複occurrences；成功、中間安全條件與所有允許觀測
輸出均須由s判定。
對所有h,h′與a∈Γ，要求

\[
s(h)=s(h')\Rightarrow
\left\{\begin{array}{l}
\mathrm{Legal}(h,a)\leftrightarrow\mathrm{Legal}(h',a),\\
\{s(k):h\xrightarrow a k\}=\{s(k'):h'\xrightarrow a k'\}.
\end{array}\right.
\]

則ker(s)是保action labels的bisimulation；任意有限action word有相同
合法性、接受性与完整可觀測續接集合。**一般接口的歸納很直接，待證的
内容是可檢查的結構條件推出上述匹配，且摘要不必保存完整歷史。**

已知充分的窄grammar：内部永遠密封、join只引入fresh私有點、完整
共享joint在forget之前受所有後續限制、每步E更新exact且congruent。
固定端點、只插入互斥二邊路徑的[LocalWiring](local_closure.md)已有
`residual_exact`／`chord_residual_exact`與`update_congruent`普通Lean；
一般moving-frontier、active-face或重開內點沒有這份E。

**反例。** [同R不同幾何續接](local_closure.md) §6中，C₄上的
P=0–x–2、Q=1–y–3与T=0–z–2，P／Q及加T後均同84份字面染色；
P+T可施工，Q+T不能在指定同側disk施工。只記R不判幾何合法性。
完整tuple `{01,10}` 的marginals誤接受00；ternary parity
`{000,011,101,110}`的全部pair projections誤接受111。新控制只聲稱
抽象關係反例；真實[R511五階來源](c5_relation_arity.md)保存各四點
restriction有延拓但整五點01232不可延拓的具名圖證書。

**染色操作還缺一層。** R/J量化「存在某個內部延拓」。要搬從指定
source染色c出發的Kempe／安全repair路径，必须對實際colouring states
證允許moves的fibre匹配，或保reachable fibre／Kempe class及step matching。
只投影保存兩時刻 `Θ_a(I,I′)` 仍可能使上一輪target lift與下一輪source
lift不同；須有同一中間witness的saturation／bisimulation。
[同粗cut不同後繼](c5_equal_cut_witness.md)已保存同圖survivor-811的
兩個染色及不同一步結果。另需可構造匹配、進度／步數界，才是repair算法。

**可能消除。** 對已證Γ，统一introduce／join／condition／close／forget
及state合併；若另證換色fibres，可補no-mixed存在性分離到source可達
repair、retained-port多步充分性。未證匹配前，這些仍列為未解；也未得
有限state大小、grammar涵蓋所有圖或來源可實現性。

### 4.3 B-RW：完整Σ的刪邊弱充分性

固定刪邊封閉域D，觀察為完整具名Σ；silent是Σ不變單刪，visible
只標target Σ。令 `W(G)={Σ(H):G→silent* U→visible H}`。
若全域fibre条件 `Σ(G)=Σ(H)⇒W(G)=W(H)` 成立，則ker(Σ)为
divergence-insensitive weak bisimulation，全部有限observable traces相等。
[WeakBisimulation](c5_completion_weak_bisimulation.md)的
`kernel_isWeakBisimulation`／`kernel_observableTraces_eq`已是普通Lean。
最弱已知語義充分條件是hW；不需有限性、termination或degree前提。
**任意k的disk圖是否滿足hW仍未證**；completion任意k不給任意k的hW。

反例的層級必須精確：[k3-t175／t180](c5_disk_deletions.md)同Σ199，
單步後繼分別 `{199,255,967}`／`{255,967}`，前者有silent刪邊後者無。
這兩個C₅ cells含chord03，反駁不另限induced框的強單步版本；
但[完整刪邊格](c5_disk_weak_successors.md)给相同W与weak traces，
**不是H3或B-RW的反例**。k≤3既有audit＋production completeness、
紙面completion與固定boundary的內點重標等變支持該固定域hW；
本輪未重跑大型audit，任意k無新反例或證明。

若hW成立可统一該刪非框邊域的有限observable traces摘要；策略／Goal另須
由Σ判定及可構造匹配。它隱藏edge identity與silent步數／成本，不保發散、
指定原邊操作、Kempe路径或每步代價。

## 5. 本輪證據、重播與精確停止點

新增 [小checker](../scripts/c5_phase_b_controls.py)、
[兩容量圖輸入](../artifacts/c5_phase_b/capacity_inputs.json)及
[controls.json](../artifacts/c5_phase_b/controls.json)。使用標準函式庫，
不import舊數學producer。兩既有disk圖各獨立遍歷全部240份字面框列，
重算22份原critical單刪及C44 core的7份q單刪；按原rotation遍歷darts核
Euler=2与指定C₅外面。兩新容量圖以獨立MRV窮盡回溯確認q拒絕、
62份q單刪、十列Σ、完整unary／mixed relations与修正逐欄等式；其容量控制
只觸發相鄰兩root、唯一shared incidence11 mixed的欄，沒有計算覆蓋χ=0、
多mixed或更多roots的一般域。逐原邊路徑
核Kuratowski subdivision。三個抽象關係控制不宣稱disk實現。
輸入及checker SHA-256保存於新controls；既有artifact未覆寫。

| 本輪實際執行 | 結果與範圍 |
| --- | --- |
| 新Phase B一般／seed17 `--check` | PASS；兩disk、兩非平面容量圖、22＋7＋62份刪邊、三抽象控制 |
| Root budget `--check` | PASS；8樹形／233744 list指派、113 edge-minimal controls、149 source側預算 |
| W shield screen `--check` | PASS；3497個後續keys排除、0剩餘；是已閉分支重播 |
| Shield calibration `--check` | PASS；21圖、220 critical邊、5短mixed；固定目標前提未觸發 |
| U4 primary及獨立audit `--check` | PASS；828 markers、3312三色碰撞、132480 fibres、15460 q刪邊lifts；保228份完整contact非等價控制 |
| CommonRepair／arity `--check` | PASS；6圖／30 covers／88刪條件／384 lifts；132類／20五階圖／100 lifts／6 joins |
| NamedRepair provenance／D₁₃ caps `--check` | PASS；兩35邊cores／6 witnesses／22 U-lifts；8圖／11520 lifts／16負控制 |
| CommonRepairAudit／SealedFourPortAudit／WeakBisimulationAudit | PASS；27／22／8具名theorems，無sorryAx或新增native信任；标准公理範圍依各audit |
| `lake build` | exit0，8831 jobs；沿用既有style／unused simp警告，不表示新紙面推廣已Lean化 |
| 文件／DocGraph／whitespace | PASS；584份Markdown／6953本地links；正式docs範圍62 documents／213 relations；新文字檔亦另核whitespace |

實際命令（除新產物首次生成，以下均為不改既有artifact的重播）：

```bash
python3 scripts/c5_phase_b_controls.py --check
PYTHONHASHSEED=17 python3 scripts/c5_phase_b_controls.py --check
python3 scripts/c5_root_degree_excess.py --check
python3 scripts/c5_qcore_shield_screen.py --check
.venv/bin/python scripts/c5_shield_calibration.py --check
python3 scripts/c5_excess_two_nonadjacent_two_mixed_core44.py --check
python3 scripts/c5_excess_two_nonadjacent_two_mixed_core44_audit.py --check
python3 scripts/c5_two_vertex_common_repair.py --check
python3 scripts/c5_relation_arity_audit.py --check
python3 scripts/c5_lean_named_repair.py --check
python3 scripts/c5_two_vertex_repair_caps.py --check
lake env lean Math/CommonRepairAudit.lean
lake env lean Math/SealedFourPortAudit.lean
lake env lean Math/WeakBisimulationAudit.lean
lake build
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
git diff --check
```

未重跑：E1／ES／ER大枚舉、LC／NamedRepairAudit、全部upstream分類、
大型weak-deletion／Kempe／stepwise／local-closure audits。
本輪未修改Lean；新紙面推廣與Kuratowski核對是Python／紙面證據，
上述既有Lean audit不把它們形式化。

**Phase B交付停止點：** 三組均有精確候選、前提、反例、义務和分支
效益；一般化接口可用，但未新增45／54／55排除、ε≥3下界或操作充分性。
優先的小證明義務是：同一N2 45／54原unit省略身份能否提供B-S0缺少的
mixed支援下界，並在同一β、η用B-C2檢查完整joint；操作線先固定sealed
grammar与exact residual，避免先宣稱一般state。這是Phase B提出的窄
義務，沒有啟動新枚舉。各線停止點與後續入口仍由
[Kempe](c5_kempe_guide.md)、[Weak-deletion](c5_weak_deletion_guide.md)、
[State](c5_state_guide.md)及[兩點重疊](c5_two_vertex_overlap_guide.md)維護。

2026-10-09上述支援義務在[N45指定省略身份](c5_excess_two_nonadjacent_unit_core45.md)內已有窄結果，
沒有升級B-S1／B-E或操作充分性。各精確殘留見該權威入口，
目前排程仍由Kempe導覽維護，原當輪停止點保留。
