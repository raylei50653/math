# Kempe／重接／計數與策略導覽

## 最新進度

現況核對：2026-10-16；[319同源雙補全](../audits/2026-10-16-r6-319-joint-parity-f1faf74/REPORT.md)把原v五度的兩個實際C5支持迫為(1022,1022)，原九框全部接回再將共同H必要關係縮至58列。cyclic四割避e,f已證；v/w五度、W110+W101>0及完整319仍OPEN，既有界不變。

| 欄位 | 現況 |
| --- | --- |
| 階段／生命週期 | 普通101及兩個全異完整染色扇區已證存在；主攻110／101聯合偶補正值，主命題仍OPEN。其他保留線不變。 |
| 最近研究更新 | 2026-10-16：[同源雙C5／九框全接回與全域奇數反控制](../audits/2026-10-16-r6-319-joint-parity-f1faf74/REPORT.md)；保留上一輪兩個全異非空扇區，仍未證聯合正值。 |
| 上次完成 | cyclic四割避e,f；原v五度的雙C5完整支持只剩(1022,1022)，原九框全五點lift把H必要關係縮至58列。完整交換矩形及singleton判準成立；弱平面條件下仍可全域omega_e=2，無新Lean。 |
| 目前停止點 | 普通聯合族非空，但 omega_e=0／W110+W101>0 仍OPEN；不要求兩項各自正。110其餘普通障礙、完整319及一般T／T0未證，接回仍k+5。 |
| 下一步 | 使用同一原九框、58列H上界與兩份完整1022補全，尋找違規全接回；聯合奇數路線須同時用原兩面、hub接線、扇區與非邊。正起點及短割條件單獨不足。見[精確停止點](../audits/2026-10-16-r6-319-joint-parity-f1faf74/REPORT.md#6-精確停止點與證據界線)。 |
| 接手入口 | 本頁 §3及[本輪整合](../audits/2026-10-16-r6-319-joint-parity-f1faf74/REPORT.md)；[同源雙補全](../audits/2026-10-16-r6-319-joint-parity-f1faf74/C/PROOF.md)、[全異來源雙射](../audits/2026-10-16-r6-319-continuation-f1faf74/A/PROOF.md)、[原普通101證明](../audits/2026-10-16-r6-seven-disk-rigidity-120aae9/PROOF.md)。 |

### 近期里程碑

| 日期／階段 | 進展與來源 |
| --- | --- |
| 2026-10-16／同源雙補全與九框 | [雙C5完整1022與58列H必要關係](../audits/2026-10-16-r6-319-joint-parity-f1faf74/REPORT.md)保留同一原G全部五點接回；cyclic四割避e,f已證，完整319與偶補正值仍OPEN。 |
| 2026-10-16／完整全異來源 | [兩份全異fibre與精確正值](../audits/2026-10-16-r6-319-continuation-f1faf74/REPORT.md)補至少一個真實z接回；原五圈分類及受保護外弧收窄奇圈路線，主目標仍OPEN。 |
| 2026-10-16／319接回缺口 | [來源商圖與變色奇偶式](../audits/2026-10-16-r6-319-complete-e98a1cc/REPORT.md)保留空fibres；實際四連通平面控制顯示ordinary101與even111仍不足，來源正值未證。 |
| 2026-10-16／普通101存在性 | [前輪障礙排除](../audits/2026-10-16-r6-double-w5-101-0b639cf/REPORT.md)後，[七disk結構](../audits/2026-10-16-r6-101-nonwheel-seven-cut-120aae9/REPORT.md)先排I≤4無界子類，[任意excess三耳矛盾](../audits/2026-10-16-r6-seven-disk-rigidity-120aae9/REPORT.md)再排全部七割，得普通P101非空；偶補正值仍OPEN。 |
| 2026-10-15／完整接回與共同圖 | [四輪整合](../audits/2026-10-15-route-round4-6ddea32/REPORT.md)：普通分離存在、批次交換連通、J四連通與兩星必要條件；特定720模型無單值section，但Layer0有二層真圖。偶補正值及完整來源排除仍OPEN。 |

本頁維護本線現況；證明及實際重播範圍見各報告。
研究線標記見 [HANDOFF](HANDOFF.md)，完整索引見 [STATUS](STATUS.md)，
共通信任界線見 [DOCUMENTATION](DOCUMENTATION.md)。

## 1. 目標與範圍

研究固定來源圖上的換色、完整有序關係及計數限制，尋找可證的出口機制。
必要條件、固定圖閉包與一般 disk 定理分開；本線不宣稱已證 `K∞=K≤5`。

本輪接續[普通101存在性](../audits/2026-10-16-r6-seven-disk-rigidity-120aae9/REPORT.md)：
在固定三框點四度、r六度的同一來源證W110+W101>0；原兩星幾何作支援。
本線亦保留[猜想 E：拒絕位置的複雜度由 degree 超額支付](c5_research_synthesis.md#81-猜想-e超額拒絕定律)。
沿用已證 ε≤1 層，剩餘共同目標 E-ARC2 為：在原來源前提及 1≤|Q|≤4 下，
ε=2 ⇒ Q 包含於某個連續三點弧。原域內猜想右端至多為 3，故完成 E-ARC2
便完成猜想 E；本線各 core 身份排除只按其完整前提計入這項義務。

## 2. 項目現況

| 項目 | 已知結果與未涵蓋範圍 | 報告入口 |
| --- | --- | --- |
| R6-SEVEN-DISK-RIGIDITY／普通101 | 任意大小排除最後七割障礙；同一D的普通P101非空，故普通聯合族非空。omega_e=0、W110+W101>0及完整319仍OPEN | [最終證明、審查及驗證](../audits/2026-10-16-r6-seven-disk-rigidity-120aae9/REPORT.md)、[七disk結構及完整介面](../audits/2026-10-16-r6-101-nonwheel-seven-cut-120aae9/REPORT.md) |
| 原內圈與r6有限排除 | 2026-10-14：p5⇒a≥6／q5⇒c≥6；r6p5另迫ell-v、ell-w非邊並有反射對應，固定三框點四度支k≤27⇒h≤12。完整k23／24枚舉得同一固定支r6⇒k≥25；完整319仍OPEN，一般K≤22不變 | [共同W及高h排除](../audits/2026-10-14-r6-lowpq-3953c85/REPORT.md)、[完整k23／24枚舉](../audits/2026-10-14-r6-319-enumeration-676b102/REPORT.md) |
| 四輪具名匹配／完整來源續進 | 普通雙向分離及保XOR批次交換連通已證；完整all-r需同時拒e=f≠g及e=g≠f。來源J四連通、兩星W完整fibre與三標記窄割表成立，尚未迫偶補正值或來源矛盾 | [最新整合](../audits/2026-10-15-route-round4-6ddea32/REPORT.md)、[四輪證據與歷史重播](history/2026-10-15-kempe-routes-publish.md) |
| Kempe共同原圖與多值細分 | 特定720-state表無交換相容單值section；Layer0有75／121點二層共同圖且各864份完整染色。兩圖非平面、只覆18列；完整720／22列及平面來源仍OPEN | [共同原圖障礙](../audits/2026-10-15-kempe-common-graph-6ddea32/REPORT.md)、[二層共同圖](../audits/2026-10-15-kempe-state-covers-6ddea32/REPORT.md) |
| C4具名四連通三角化圖 | 同色點識別及刪u得到四連通T，或刪唯一三度b得到四連通T0；完整fibres把延拓變成b出口／兩個同圖三角面色集合差異。無界仍OPEN，不提高K≤22 | [權威入口](c5_c4_triangle_core.md)、[證明與控制](../audits/2026-10-14-c4-triangle-core-b66f592/REPORT.md) |
| C5→C4完整來源橋與K≤22 | 四-spoke外點與原圖全部相容lifts作完整接合；共同拒絕y0、y1化為ABCB空fibre，面／度數符合非diamond 4-candidate。接外部完整≤28點計算得K≤22=K≤5；無界具名子類及K∞仍OPEN | [權威入口](c5_c4_boundary_pivot.md)、[證明及驗證](../audits/2026-10-14-c5-c4-boundary-pivot-77fbd5d/REPORT.md) |
| 新封存的 no4ct／C8 隔離成果 | 三支 W5 前提修復、C8 零端部排除、h=4 的 induced C9 與 84 項殘留；C6 補完同側、僅原 C8 pins、a−d≤5 的 gadget 域，全部與八份 U 非空相交。量詞為 ∀G∀U∃row(G,U)，八項來源與主命題仍 OPEN | [五包成果、前提、重播及接續入口](history/2026-10-13-multi-commit-status.md) |
| 無四色定理前提路線／交接 | C4來源橋接外部計算得K≤22及共同k≥23；三支外圈／C8已接入，T1-CROSSCUT 證 h=3⇒p=0，只留 RING。T2的apex結構及三支私人ρ≥5保留；一般來源仍OPEN | [停止點、證據與下一窄任務](tasks/c5_no4ct_handoff.md) |
| C8 一般正對切口 T1-CROSSCUT | 原 no4ct 全域最小內點、再最大邊數契約下 h=3⇒p=0；共同 literal 接合、完整支援直積及全部安全矩形排除 PINCH／BRIDGE，不限 s 或兩片大小。RING、h≥4、主命題 OPEN，無新 Lean | [C8 權威入口](c5_c8_peeling.md)、[採納審查與完整重播](../audits/2026-10-14-t1-crosscut-review-77fbd5d/REPORT.md) |
| C8 單接末端排除（歷史 T1） | 640份具名外側完整轉移全部排除s=1，不限剩餘C6內點數；保留2,515,696份P lifts及全部空fibres。當輪 s≥2 剩餘分支現已由 T1-CROSSCUT 全部排除，原證據不改寫 | [T1證明與證書](../audits/2026-10-13-c8-terminal-s1-d521163/REPORT.md) |
| C9-932 原apex下界 | no4ct、完整932、h=4的20×5低度假設全排；五apex的d_H≥4、d_G≥6，九原邊第三點互異，k≥18。20項較高度數來源仍OPEN | [T2證明與證書](../audits/2026-10-13-c9-932-source-d521163/REPORT.md) |
| W5 私人圈秩 no4ct 接入 | 全域最小來源三支任取合法W5皆ρ≥5；森林至圈秩四前提及來源分支已接通，沿用七seal／407記錄的完整染色證據 | [T3證明與依賴表](../audits/2026-10-13-w5-no4ct-bridge-d521163/REPORT.md) |
| 共面識別／聯集封閉正規形 | global 最小內點、最大邊數來源的共面完備及簡單三角面正規形；接文獻 Cor20 得一般 disk 的 K≤12=K≤5。132 witnesses／8778 unions／十候選及完整 fibres 重播；後續K13／K14／K15及C4來源橋已提高至K≤22；二十三內點以上與完整關係重接仍 OPEN，未 Lean 化 | [權威入口、證明及重播](c5_cofacial_normal_form.md) |
| 近三角化完整外圈 | h≤2全部排除；h=3的70查詢已排62、留8。小cap／無內弦與cofacial識別新排c16/c32-941；可逆Kempe計數使c15/c20-941各由173降至171列。仍只採納h≥3、n5≥9；同圖原面／跨split實現OPEN，未Lean化 | [完整外圈](c5_neartri_boundary_collar.md)、[C8-STRUCT精確結果](../audits/2026-10-13-c8-struct-243a125/REPORT.md) |
| 跨原邊 Kempe 缺陷搬運 | 五度輪十列四格逐lift雙射、相鄰五度中心搬運及全域恆等式；同一拒絕列至少六條原邊有單邊缺陷。一步交換精確判準及實際拼接反控制；933／941排除仍OPEN，無新Lean | [精確定理、證明與控制](c5_cross_edge_kempe.md) |
| C₈ apex度數與分支大小界 | 八項全部40個apex-H三度假設排除（38支援閉包＋2精確計數證書）；原apex≥6度、H嚴格內側至少六個五度點，原h=3⇒k≥14後由原面配對、短弧／內圈及m=10分類加強為k≥19。八項仍留；一般k≥16由K15-SPHERE另證，h≥3、n₅≥9不提高 | [局部引理、精確證書與剩餘界線](c5_c8_apex_degree.md) |
| 十四內點完整球面覆蓋 | K≤14=K≤5；73球面嵌入／1,001根圖全部Σ1023，180,228完整lifts獨立一致；另有純紙面h=3⇒k≥16。十五內點後由K15排除，主命題OPEN，未Lean化 | [權威入口、證明與驗證](c5_k14_sphere.md) |
| 十五內點完整球面覆蓋 | K≤15=K≤5；192球面嵌入／2,714根圖全Σ1023，624,617完整lifts獨立一致。後續C4來源橋得K≤22；二十三內點以上及一般主命題OPEN | [權威入口、證明與驗證](c5_k15_sphere.md) |
| C8原接點與反覆剝層 | 任意大小三型分類與一般原面separator完整轉移已證；T1-CROSSCUT 已排全部 PINCH／BRIDGE，只剩 RING，同型C8遞迴仍有七障礙。m=10分類自身給h=3⇒k≥19，當前共同C4界為k≥23；原八項的RING來源仍OPEN | [原短弧與m=9](c5_c8_inner_collar.md)、[結構、T1-CROSSCUT及完整轉移](c5_c8_peeling.md) |
| 十三內點完整外圈 | K≤13=K≤5；h4的41根圖與h5的4根圖皆Σ1023，h6／h7紙面排除。全部736具名配置、兩路球面生成與直接內側分類完整覆蓋，完整lifts獨立一致；十四內點已由後續K14-SPHERE排除，一般命題OPEN，未Lean化 | [權威入口、證明與驗證](c5_k13_collar.md) |
| 最小來源度數／五度鄰環 | 沿用全域最小性，C4 關係≤3內點、邊界度數≥4、內部≥5；後續已保證全內部 induced W5。A九種位置契約、B固定域1020項操作及C全部17424組cap閉合已交付，一般縮減仍OPEN，無新Lean | [度數界](c5_saturation_degree_bound.md)、[全內部五輪與交付界線](c5_degree5_link_reductions.md) |
| 全內部 W5 具名完整關係縮減 | 五個合法 k−2 商圖的完整拉回無損重建十 pin H／G fibres；重數二恰唯一接回中心。34圖完整控制；普通正聯集及 r≤6 annulus 代表仍OPEN，無新Lean | [精確公式、反控制及重播](c5_w5_marked_relation.md) |
| W5 最弱保存契約與小代表 | 最弱為補中心後完整Σ＝pr_B R³；保R³較強且不需染色數相等。已認出K132的102個induced-B關係都有r′≤5合法環帶代表，另有任意m→0嚴格替換族及16→6完整控制。K15使r′≤9足以排目錄外來源；一般九點存在及真正最小來源私人ρ≥5的縮減仍OPEN，無新Lean | [正式入口與全部證據](c5_w5_three_color_support.md)、[本輪保存契約及構造](../audits/2026-10-13-w5-small-representatives-6cafdfb/REPORT.md) |
| W5 私人單環排除 | 任取合法全內部 W5，最小來源私人圈秩≥2；contractible 純紙面排除，essential 完備化成7–10點純環及1652模板，全部Σ1023。後者可換只保Σ的r′=0 prism，減少7–10內點，不保R³；後續雙環至圈秩四排除提高至圈秩至少五，一般縮減仍OPEN，未Lean化 | [正式入口與完整證據](c5_w5_private_unicyclic.md) |
| W5 私人雙環排除 | 完整最小來源的私人圈秩≥3；四型及全部essential位置完備覆蓋，theta 974模板全有四份實際保Σ嚴格代表之一。完整9,973,760 cells、八次破損拒絕及獨立審閱PASS；只保Σ、不保R³；後續圈秩三兩分支均排除，私人圈秩下界後由圈秩四排除提高為五；一般縮減仍OPEN，未Lean化 | [正式入口與完整證據](c5_w5_private_rank2.md) |
| W5 私人圈秩三環繞分支 | 任意合法W5的私人圖若含essential環則ρ≥4；1,283份完整模板皆Σ1023。當輪留下的contractible分支由後續完整排除，曾得一般ρ≥4，後續圈秩四亦排除而得ρ≥5；小代表及主命題OPEN，無新Lean | [紙面完備化約、全部fibres與獨立重播](c5_w5_private_rank3_essential.md) |
| W5 私人圈秩四兩分支 | contractible 6,389模板與essential 2,872模板完整排除，任取合法W5私人ρ≥5；原十pins、空fibres、全部A/G lifts及原rotation保留。一般縮減／小代表及K∞仍OPEN，未Lean化 | [合併權威入口與兩包證據](c5_w5_private_rank4.md) |
| W5 私人圈秩三contractible分支 | c≤2、原block及M預算完整化約；c=1的2,162與c=2的108模板全部Σ∈K132，直接排除。接essential結果，任取合法W5私人ρ≥4，後續圈秩四亦排除至ρ≥5；一般縮減及小代表OPEN，未Lean化 | [正式入口與全部證據](c5_w5_private_rank3_contractible.md) |
| 廣義N2來源橋接 | 原E4三列域恰比完整Σ多932；mask-free U4、五列slack／完整分量witness、UC3及局部OL／LL移植排除932。廣義N2完成，E-ARC2仍OPEN；紙面＋明列上游有限末端，無新Lean | [定理、前提帳本、父ledger與重播](c5_excess_two_n2_bridge.md) |
| 猜想 E／E-ARC2 共同目標 | ε≤1 已證；ε≥3 在原域自動滿足。ε=2 的三點弧命題仍 OPEN，等價排除 941 形三點及四點弧來源；Q=B 的 932 是較強版本的另項義務 | [母猜想與等價證明](c5_research_synthesis.md#81-猜想-e超額拒絕定律)、[E2 低 ε 證明](../artifacts/c5_excess_one_e2/REPORT.md)、[E3 三列化約](../artifacts/c5_excess_two_e3/REPORT.md) |
| E-ARC2 真子圖與共同核心 | 沿用 E2／唯一 degree-5 相鄰列分離及兩-root44排除，目標反例的任意真子圖至多單拒絕；任意兩個不同拒絕列的 minimal cores 聯集必為 G，所有內點皆不可同接24。179固定圖中172觸發一般 Z 引理並成立，目標來源0觸發；後續45／54與LL-CUT+diag合成指定完整Σ的N2契約九格覆蓋，其他域與E-ARC2仍OPEN，未Lean化 | [完整紙面證明與負控制](c5_excess_two_arc_pair_critical.md) |
| E-ARC2 原分量共同限制 | 同一degree-4原分量的boundary重色至多涉及一個拒絕列；完整N2前提再接已採納N45-U，所有原分量刪除均全收，每個非root點至多接兩個相鄰框點，真core只能省一條root-spoke。63固定圖／13,010完整外部投影核對，目標0觸發；後續spoke與LL-CUT+diag涵蓋指定完整Σ契約的45／54及原55，廣義N2由N2-BRIDGE排除，N2外及E-ARC2仍OPEN，未Lean化 | [證明、完整fibres與控制](c5_excess_two_arc_component_slack.md) |
| E-ARC2 N2全部真核心排除 | 原leaf block必有私有root接點；無U的H二連通，同H兩次SD-A加雙star／diagonal排spoke core，含U接既有完整契約。全部非框邊刪除均全收，roots亦至多接相鄰兩框點，當輪只剩原55；後續LL-CUT+diag完成指定完整Σ契約九格覆蓋。63圖完整local fibres校準，目標0觸發，廣義N2由N2-BRIDGE排除，N2外及E-ARC2仍OPEN，未Lean化 | [完整證明、契約覆蓋及控制](c5_excess_two_arc_spoke_closure.md) |
| 933／941 的 excess／容量／跨度 | 兩候選均已證 ε≥2。唯一 degree-6 root 的 t=0、1、2、3 全部分拆均已作整型來源排除，T4 迫 t≤3，完成此 ε=2 分支。t=0 的 (6) 用飽和兩 K₄，(4,2) 用原 binary 路徑的同源框弧 K₅；若 ε=2，只剩兩個 degree-5 roots。任意大小紙面＋Python、未 Lean 化，一般來源保留 | [t=0 全分拆總報告](c5_excess_two_no_spoke_complete.md)、[t=3 全分拆總報告](c5_excess_two_three_spoke_complete.md)、[t=2 全分拆總報告](c5_excess_two_two_spoke_complete.md)、[t=1 全分拆總報告](c5_excess_two_single_spoke_complete.md)、[941 ε≥2](c5_941_three_spoke.md) |
| 不依賴 ε 的盾弧預算與 hub 原則 | 任意 ε、任意 roots：one-sided 分量的支援是連續框弧、盾弧兩兩邊互斥；全圖至多兩份 unary，且 spokes／mixed 支援被限制在 2–3 個框點。短支援、K₄ 引理、二／三-hub K₅ 統一成 hub 原則，並推廣到 roots 同色的 mixed 分量。A₄ 殘留 U 支援紀錄 40／58→24／30，無整份 frame 排除。紙面＋Python，未 Lean 化 | [盾弧預算與 hub 原則](c5_unary_shield_budget.md) |
| 雙 root 的 ε=2 收窄 | 相鄰 mixed 刪 roots／zw 全收；相鄰唯一 mixed 已全排 (4,4) 核心、五-spoke 原來源、四-spoke (3,1) 全部 incidence 分拆及 (2,2) 的 mixed-(1,1) 加各側一 unary 整個子型，含 root 交換。原47／75必要身份全部封閉；其他 (2,2) incidence、較少 spokes、單省略及原 (5,5) 核心保留。紙面＋Python，原Σ933／941來源的ε≥3下界未證，未 Lean 化 | [mixed-(1,1) 子型完成](c5_excess_two_mixed_core_four_spoke_disjoint_pairs.md)、[短框弧原拒絕列延拓](c5_excess_two_mixed_core_four_spoke_short_arc.md)、[原 crosscut 與 mixed hubs](c5_excess_two_mixed_core_four_spoke_crosscut.md)、[同一長 face 次序排除](c5_excess_two_mixed_core_four_spoke_long_face.md)、[原四接點 leaf-slack](c5_excess_two_mixed_core_four_spoke_quaternary.md)、[原三接點身份](c5_excess_two_mixed_core_four_spoke_ternary.md)、[binary 端點 hub](c5_excess_two_mixed_core_four_spoke_hubs.md) |
| Kempe screen／邊位置對座標 | screen 等價於 20 條蘊涵，1,024 masks 已核對；未新增排除，一般 adjacent-singleton lemma 未證 | [screen](c5_kempe_screen.md)、[座標](c5_edge_pair_coordinates.md) |
| adjacent-singleton 原始文獻稽核 | 本輪核對未找到可直接排除任意大小933／941的定理；count-cone的可用排除結果僅有界或附條件，普遍猜想仍OPEN，不新增來源排除 | [文獻身份、適用性及缺口](../audits/2026-10-13-singleton-literature-6cafdfb/REPORT.md) |
| 非相鄰N2的全部45／54真core身份 | 指定整U及全部spoke省略已排；含U逐項接回LOW／HIGH／LONG完整契約，無U由原leaf block、H二連通與兩次SD-A排除。BR四支、共同雙色引理及SF-QX／BASE／Gallai信任界保留；後續LL-CUT+diag完成指定完整Σ契約的原55覆蓋，廣義N2由N2-BRIDGE排除，N2外其他cores及E-ARC2仍OPEN，目標來源not triggered，無新Lean | [N45權威入口](c5_excess_two_nonadjacent_unit_core45.md)、[新完整覆蓋](c5_excess_two_arc_spoke_closure.md) |
| 二連通單缺額工具與45／54適用性 | SD-A指定前提紙面查證通過；新N2接入已由同圖三列推得無U的H二連通，兩次用單缺額定理排該域所有spoke cores。一般非二連通／雙缺額55及R31不由SD-A解決，exact source controls未觸發，無新Lean | [精確定理](c5_degree5_interfaces.md#7-二連通單缺額查證與-4554-接入)、[N45接入](c5_excess_two_nonadjacent_unit_core45.md#214-e-arc2-接入全部-spoke4554-排除與原55化約) |
| 循環流與計數 | 六維／153 支撐／十二循環；36 份基底覆蓋證三套分開整數 orbit 條件不再收緊恆等式解；未排除平面來源 | [循環流](c5_circulation.md) |
| Count cone／class 計數 | near-triangulation 化約、部分 Lean 代數與 class 級紙面計數已有；cone／connectivity 缺口仍在 | [count cone](c5_count_cone_bridge.md)、[B₅ face](c5_b5_face.md)、[class 計數](c5_kempe_class_counts.md) |
| 同染色有序重接 | 一步精確公式及同圖三配對同 state／不同後繼反例；record 110 已另由原圖 K5 排除，有限可迭代 state 未證 | [有序重接](c5_dual_path_surgery.md)、[來源排除](c5_single_spoke_two_two_minor.md) |
| Connectivity／候選 state | 同圖更新與有限控制可重播；AB-only／固定 AB\|CD 猜測有反例，多候選不能任意拼成可實現 state | [connectivity](c5_kempe_connectivity.md)、[AB cube](c5_ab_swap_cube.md)、[choices](c5_edge_choices.md) |
| Cut／behavior | retained-component 重建有 Lean 支援；粗 cut 摘要有反例，有界 behavior 控制不證多步充分性 | [cut](c5_cut_interfaces.md)、[behavior](c5_behavior_refinement_results.md)、[state 導覽](c5_state_guide.md) |
| 固定圖策略與 repair | survivor-811 固定閉包、必要低谷／回升與 B₂ 準備已保存；一般 K=4 策略、共同安全 repair 機制未證 | [barriers](c5_strategy_barriers.md)、[repair](c5_repair_interface.md) |
| 閉環一致／零邊修復猜想 | 固定可延拓 C₅ 邊界，猜想任意 flat 標記可經內部 cut XOR、零邊數不增而修復；容許持平步，未初驗，不推出邊界可延拓或其他來源排除。驗證需完整不增轉移圖，不能只找一步下降 | [猜想 Z 與驗證計畫](c5_forcing_transport_conjectures.md)、[State 導覽](c5_state_guide.md) |
| N2原55共同引理與下界衝突檢查 | 原55每欄容量為1，singleton與兩unary限制保留；後續LL-CUT+diag排最後雙long，指定完整Σ契約內九格全覆蓋。大小式與有限下界10仍無直接衝突，沒有以Δ排除；廣義N2由N2-BRIDGE排除，N2外及E-ARC2仍OPEN | [九格、共同證明及父前提](c5_excess_two_n2_residual_unification.md) |
| N2三列diagonal採納及long限定縮減 | unary接線2／3的無界block-tree證明及同列完整lifts經另人採納，排(0,1)，第三relation族原55全排。shared contact迫所有同色pins全接回；long接點總數≤3有一指定列(D,D)出口，排一long無U的該子域。當輪long殘留後由下列含U／一long排除收窄至(2,0)；97U及63整圖完整joins獨立重算，target not triggered，無新Lean | [採納、完整證明及殘餘](c5_excess_two_n2_diagonal_three_row.md) |
| N2 long同步與葉接點tree | 兩long都k≤3全排；一long無U的全葉接點tree任意k排除；含U低接點mask精確Eq／Diff，異類同列接回。當輪七個同類必要模板已由下列統一規律一起排除；k4 path局部全拒diagonal反控制保留，廣義N2由N2-BRIDGE排除，E-ARC2仍OPEN，無新Lean | [新證明、獨立採納及完整fibres](c5_excess_two_n2_long_synchrony.md) |
| N2原55的統一接口與禁色規律 | 相同具名接口分割給完整tuple雙射；三點支援任意k有四類mask，mixed完整表26代表、unary7代表。每份低接線U在三色框至多禁一個已用色，合原55容量排k_U=3及七個同步模板；當輪兩接線U residual已由下列全色Diff出口完整排除。紙面＋完整fibres校準，未Lean化，廣義N2由N2-BRIDGE排除，E-ARC2 OPEN | [統一證明與當輪剩餘合同](c5_excess_two_n2_partition_rule.md) |
| N2原55含U子情形完成 | 任意大小兩接線U由原附件容量化約五形；Diff列拒絕唯一六點形有原K₅，故每個owner色均有完整lift。同列G−U實際ownerpin接回，排完整(1,1)，不限制long接線數；目標必u=0、H二連通。當輪(1,0) residual由下列排除；target not triggered，無新Lean，E-ARC2 OPEN | [完整證明、審查與重播](c5_excess_two_n2_unary_diff_closure.md) |
| N2原55一long子分支完成 | 原框弧K₅、leaf bridge附件單射及固定root完整接回排全部(1,0)；其當輪雙long殘留現由下列加強版排除。任意長度紙面＋獨立審查＋完整fibres，target not triggered，無新Lean | [來源排除、完整witnesses與checker](c5_excess_two_n2_one_long_closure.md) |
| N2原55雙long共同容量接回 | 原碰色＋容量與leaf K₅排t=0／1；剩餘t=2／3已由下列LL-CUT+diag排除。本頁基本S與至多九格矩陣定理保留；target not triggered，無新Lean | [原定理、基本子命題與控制](c5_excess_two_n2_double_long_joint.md) |
| N2原55同來源LL-CUT+diag | 原K₅-H／K₃,₃-O、leaf接線數及2≤行和≤1排全部剩餘spokes，完整原55(2,0)來源排除。基本LL-CUT未獨立證成；19,229必要共同可行投影保留。完整契約內九格全覆蓋；廣義N2由N2-BRIDGE在原E4契約排除，E-ARC2仍OPEN；無新Lean | [完整證明、父覆蓋與獨立checker](c5_excess_two_n2_ll_cut.md) |

## 3. 停止點與保留缺口

**同源雙補全與九框接回（2026-10-16）。** [本輪整合](../audits/2026-10-16-r6-319-joint-parity-f1faf74/REPORT.md)
在原v五度支構造同一H上的兩個真正C5補全；1521組K132支持對只剩(1022,1022)。
保留原a≠c染色及全部(v,r,x,y,b)接回，三個原Σ分開計算後給共同58列H上界。
這是紙面化約＋有限必要排除，未證58列實現或v五度不可能；反射給w支。
逐一缺列排除另迫12份字面完整H fibre非空，卻全無v lift；真K=J-v四框
閉包34列全保留，不能把這些空接回當作違規J見證。
每個cyclic四割避e,f；完整AB/CD矩形與整cube的singleton z接回成立。
新的真平面圖同時有111／全異起點、普通101與四／五割限制，但整個聯合族
omega_e=2；它缺原兩三角面與hub接線，不是來源反例。
主攻須保留這些具名條件及同一完整fibres，不能以正起點或短割限制自行收尾。

**完整全異來源（2026-10-16）。** [前輪整合](../audits/2026-10-16-r6-319-continuation-f1faf74/REPORT.md)
證原ABABC、ABCAC完整fibres分別與z=v、z=w的全異J扇區雙射。
若原兩份字面fibre計數為n0、n4，則全異J染色數為24(n0+n4)，
W010=W001=2(n0+n4)>0；它們不是主目標的110／101正值。
至少一個定義好的H_p／H_q有實際非空z接回，仍為來源相容singleton。
[原五圈扇區分類](../audits/2026-10-16-r6-319-continuation-f1faf74/C/PROOF.md)保留
跨扇區及原六度p/q中心例外，有弦cyclic五割回到三角耳加induced四割核心。
[原共同鄰點補充](../audits/2026-10-16-r6-319-continuation-f1faf74/C/MARKED_CUTS.md)再證每個cyclic五割至多通過e,f,g其中一條。
[最短交換的受保護外弧](../audits/2026-10-16-r6-319-continuation-f1faf74/B/PROOF.md)
證遠端單port奇輪的一條真實快捷修復必刪f；三port、受保護外弧及長奇圈仍未排除。

**完整319續進（2026-10-16）。** [整合證明鏈](../audits/2026-10-16-r6-319-complete-e98a1cc/REPORT.md)
當輪在同一來源證至少一個`(J-z)/(m=p或q)`合法商圖非空；上述新雙射已補
至少一方向的實際非空z接回，尚未迫出違規lift；非空者仍須為來源相容singleton。[變色奇偶式](../audits/2026-10-16-r6-319-complete-e98a1cc/B/PROOF.md)
從已知完整111染色與普通101取得實際含f交替環，精確計算每個新補圈奇偶。
兩個變色位置須在同圈才成功，分圈仍留兩奇圈；尚未證可取t≤2，亦未排除分圈。
[四連通平面反控制](../audits/2026-10-16-r6-319-complete-e98a1cc/C/PROOF.md)
有144份完整J染色、18個PM及唯一普通101，卻W110=W101=0；它違反原度數、小C4與
完整U fibres，不能當319來源反例。原來源特有條件仍須進入最後一步。

**聯合零值（2026-10-16）。** [R6-CAP-BARRIERS](../audits/2026-10-16-r6-cap-barriers-c4c3d99/REPORT.md)
接續[全單點排除](../audits/2026-10-16-r6-joint-zero-c4c3d99/REPORT.md)，
以奇偶最低度數的精確Euler式排除單一W5與單一W7輪障礙。
單一5割若為induced，其原圈必跨split扇區；相容扇區已由強制四點辨認W5側後排除。
後續[R6-CHORDED-FIVE](../audits/2026-10-16-r6-chorded-five-c4c3d99/REPORT.md)
以補外側三角面得到induced四圈，再逐S／X位置排除101有弦五割。
故101每個五割分量必為W5，單一五割整列已排。
後續[R6-DOUBLE-W5-101](../audits/2026-10-16-r6-double-w5-101-0b639cf/REPORT.md)
再以m原扇區與精確曲率迫兩輪鄰域互不相交，f兩端皆單點；
至少一輪中心及rim全五度，展開15個原面後的induced C5由來源提升迫外側W5，
整J全五度與m≥7矛盾。因此101雙W5整類已排，無圖大小限制。
來源已知的每份111匹配都恰跨每個障礙奇分量一次，禁止標記跨兩分量；
可在同一族使用交叉割等式。[七disk結構](../audits/2026-10-16-r6-101-nonwheel-seven-cut-120aae9/REPORT.md)
先證實際簡單七disk、I+B≥12及I≥5；[最終七割排除](../audits/2026-10-16-r6-seven-disk-rigidity-120aae9/PROOF.md)
保留全部內部excess，精確抵消後迫三個普通外耳，填耳得到induced C4，再逐原m/z扇區排除。
故普通P101非空，普通聯合族亦非空；110的非輪五割、雙五割及非輪七割仍保留。
非空聯合族的正奇補最短原圈，仍可能是W5、跨原扇區五圈或長至少七；
合法單環交換至少六長，雙環含四圈時須另配含g的至少六長環。
主攻W110+W101>0，不要求兩項各自正；完整319、一般界及k+5接回成本不變。

**四輪續進（2026-10-15）。** [最新整合](../audits/2026-10-15-route-round4-6ddea32/REPORT.md)
接通[普通分離存在](../audits/2026-10-15-tait-separation-6ddea32/REPORT.md)及
[保XOR批次交換連通](../audits/2026-10-15-xor-batch-descent-6ddea32/REPORT.md)：
合法T／T0的ω已知有限，但尚未證ω=0；連通性不供應偶補終點。
在固定三框點四度、r六度的原來源中，J=U/(s=t)四連通，令e=d(vw)、f=d(pq)、g=d(mz)，
完整all-r恰為(e=f)⇔(e=g)，兩個禁止事件皆須排除。
刪m,z所得兩原鄰弧disk W的每份完整染色，hub fibre恰為Am×Az去對角；
來源迫|Am|=|Az|=2⇒Am=Az，但尚未迫出違規染色。
當輪三標記普通PM失敗留四類；全單點類已由上述10月16日定理排除，
110目前只留一個5割、兩個5割或一個7割；101普通障礙已由上述七割定理全排；
仍須在同一非空普通聯合族證omega_e=0，即偶補正值。完成後點數回到k+5，未有保壞嚴格下降。
特定720模型的單值共同圖障礙與Layer0二層真圖相容；後者非平面且未涵蓋完整22列。
既有低p/q、k≤27⇒h≤12、一般K≤22／k≥23及固定r6⇒k≥25均保留；
完整319來源排除、r≥7、無界延拓與K∞仍OPEN。原始報告與凍結證據不改寫，
重播契約見[整理紀錄](history/2026-10-15-kempe-routes-publish.md)。

**換邊界方向（2026-10-14）。** [C5→C4](c5_c4_boundary_pivot.md)已得共同 k≥23。
[本輪化約](c5_c4_triangle_core.md)把義務壓到四連通T／T0：原b四度時，先攻同一T0
兩個指定三角面zxy／zpq能否取不同色集合；原b至少五度時，保留T上固定三角的b出口。
兩面只共享z，四個其餘接點沒有交叉邊；須保留同份完整染色。
[共同 Tait 介面](../audits/2026-10-14-c4-tait-lock-review-fdd3e22/REPORT.md)
已將兩支精確化為指定對偶邊異色問題，等價於一個偶補完美匹配恰含其中一邊。
完全失敗是全部完整染色的鎖定；正二十面體的整個 edge-Kempe 類受阻不能代替它。
可先全列匹配作固定圖測試，再證原位置、度數及小圈限制迫出所需匹配；
無界排除與最小性接回仍 OPEN。
原x,y,b皆四度的窄支已由[完整cap表](../audits/2026-10-14-c4-triangle-core-b66f592/ADJACENT4.md)
將R的完整C4關係縮至mask13。[JOINT6續進](../audits/2026-10-14-c4-mask13-joint6-fdd3e22/REPORT.md)已排ABCB的pq=BC，得到CD／BD兩個非空完整fibre分支；八列必要閉包仍非空。原p,q都至少六度則k≥28，故k≤27必有p或q五度，可先攻這個低度子域。[返回單射](../audits/2026-10-14-c4-c5-recursion-fdd3e22/REPORT.md)已排除原r五度，r六度另迫s,t≥6，下一層C5完整關係經[共面商圖](../audits/2026-10-14-cofacial-fibres-676b102/REPORT.md)縮為恰319；舊三份計數模型仍保留。高p,q的k≥28子域及一般T／T0另留。仍須打破同份ABAB／ABCD對p,q的共同強迫。以下C8／W5保留各輪原結構及較弱歷史大小界，不將條件界升格為全域界或無界排除。

[其他返回分支](../audits/2026-10-14-c4-return-branches-a11d4bb/REPORT.md)將單低p/q改以原link作外框，取得精確mask14及rainbow完整fibre分解；雙低p=q=5迫另一共同鄰點ell≥6。直接刪t並作外面z=r商圖另排a=4,t=5，給a=4⇒t≥6、c=4⇒s≥6；一般t=5只留C5支持956／1012／1020。原旋轉的p/q界須保相應singleton fibres皆空，941不能沿用；新同圖兩面商圖另直接證a=4⇒p≥6、c=4⇒q≥6，三支皆適用。一般mask13的BC返回只接到允許sector；r=7的C6必要模型仍存活，來源排除OPEN。

[低p共同來源證明](../audits/2026-10-14-cofacial-fibres-676b102/pq/PROOF.md)保留D=T0−{x,y,p}的兩個實際C4面。
七接點(z,s,r,t,q,ell,m)有非空完整ABABCBC fibre，迫ell s、ell t非邊。
[後續三點共同商圖](../audits/2026-10-14-lowpq-source-676b102/pq/PROOF.md)再得ABABCAB完整fibre與ms、mt非邊，
從而p=5⇒a≥6，反射q=5⇒c≥6。兩個fibre分別存在，不能合一。
兩面只共享z，識別弧各在原面內並共端z；不任作跨面識別。
[前輪來源表](../audits/2026-10-14-lowpq-source-676b102/classification/SOURCE_TABLE.md)的單低／雙低與r預算保留；
[共同W與原內圈續進](../audits/2026-10-14-r6-lowpq-3953c85/REPORT.md)在r6p5中再排ell-v、ell-w原邊，反射側取對應結論，
並證原collar無弦、私人圖連通無葉且圈秩≥2，給精確式2k=3h+12+E_C+rho。
故固定三框點四度支k≤27的h上界由18降為12；933／941留4≤h≤12，932留5≤h≤12。
[已發布的有限枚舉](../audits/2026-10-14-r6-319-enumeration-676b102/REPORT.md)另給同一固定支r6⇒k≥25，故k≤27的r6只留25≤k≤27。
一般p5a≥6、r六度319與高r低t/s仍OPEN，不把局部必要列或整數配置當來源實現。

**無四色定理前提路線（2026-10-14）。** [完整外圈三支接入](../audits/2026-10-13-c5-no4ct-collar-6cafdfb/REPORT.md)
已證共同 h≥3、n5≥9；[C8 接入](../audits/2026-10-13-c5-no4ct-c8-6cafdfb/REPORT.md)
排除 932 的全部 h=3 查詢，給該支 h≥4、n5≥10。修復後的原八項只屬
933／941 必要條件殘留，apex／內圈／剝層亦已接入，h=3⇒k≥19。
受限 C4 仍須 s<k，平面商圖可染性仍須本全域最小來源下 N≤k+5。
[T1-CROSSCUT](../audits/2026-10-14-t1-crosscut-review-77fbd5d/REPORT.md) 在全域最小內點、再最大邊數契約下
證 h=3⇒p=0；p 是原 C8 嚴格內點的正對雙接點數。全部 PINCH／BRIDGE
排除，不限單接點或兩側大小；一般 RING 仍 OPEN，剝層自身給 k≥19，
當前另接 C4 來源橋的共同 k≥23。
原 T1 的 s=1 里程碑及證書保留，其 s≥2 接續任務已由一般定理涵蓋。
採納核對用 `python3 -B audits/2026-10-14-t1-crosscut-review-77fbd5d/check_adoption.py --check`；
完整 64 項重算改用 `--replay`，原 `verify_review.py` 保留為歷史凍結審查入口。
[T2](../audits/2026-10-13-c9-932-source-d521163/REPORT.md)
另證 932、h=4 的五 apex 下界與 k≥18；20項較高度數來源及其餘 h≥4 仍 OPEN。一般 separator 轉移不給固定
C8 寬度或逐層度數／接點傳遞。無界三支、一般主命題與新論證 Lean 化仍 OPEN；
N2 的具名 932 排除及 W5 小代表構造中的 4CT 前提各保留原契約，詳見[交接](tasks/c5_no4ct_handoff.md)。

**共面正規形／完整關係重接（2026-10-12）。** 有界等式 `K≤12=K≤5` 已由紙面、
有限核對及外部定理接合；後續[K15-SPHERE](c5_k15_sphere.md)及
[C4來源橋](c5_c4_boundary_pivot.md)已提高至 `K≤22=K≤5`，二十三內點以上仍保留。重接方向追蹤刪一條內邊後同一原圖
的十列四格關係 `J_e(p;[s≠t],[u≠v])`。`01232` 的同色 opposite 見證已迫某個
原拒絕列有 `(0,0)` 的二色四邊形完整 lift。後續
[跨原邊定理](c5_cross_edge_kempe.md) 已證同一五度中心的一份 `(0,0)` lift
精確配出其他兩條 spokes 的 `(0,1)` lifts，只改中心色；相鄰五度中心另可經
共同原邊 lift 搬運。一般不同邊的任選 witnesses 仍不能拼接。
單獨保留 `01232` 的 flip／識別有 567→854／774 反控制。
此路線採 global 最小內點／最大邊數來源，不能挪用下列 edge-critical／ε／N2
前提，亦未更動那些分支的證書或覆蓋。詳見[權威報告](c5_cofacial_normal_form.md)。

**最小來源五度鄰環（2026-10-12）。** [度數界](c5_saturation_degree_bound.md) 已排
這個 global 最小來源的全部四度內點；後續[完整外圈限制](c5_neartri_boundary_collar.md)
已提高至 933／941 均至少九個五度內點；一般 k≥16 曾由 K15-SPHERE 證成，
當前由 C4 來源橋提高至 k≥23。二邊 crosscut 定理
亦已排除[三份任務](tasks/c5_degree5_link_tasks.md)中 C 的來源子域及另一 C4＋C6
非相鄰兩框接點方向；C另獨立完成全部132² cap閉合，A的位置／pinned契約與
B的固定域重接控制亦已交付。[全內部五輪](c5_degree5_link_reductions.md)已保證
有 degree-5 中心與五個鄰點全在原內部；尚未證這個位置可保持完整Σ縮減。
任意 Σ-飽和族無全內部 C5、四度單分支識別丟列的反控制均保存。

目前五度縮減的窄入口仍是原 B/U 十個 pins 的 annulus 完整 J_p。
[五份單對商圖](c5_w5_marked_relation.md) 已能以同圖、同色框的 full-lift 重數重建
全部 H／G fibres；單份商圖的外框投影或各自成功的 witnesses 均不足以完成該重建。
後續[三色支援與私人森林排除](c5_w5_three_color_support.md)把代表比較義務
收窄為三色U的1,200個具名cells；[私人單環排除](c5_w5_private_unicyclic.md)
證任取合法W5，原最小來源的私人圈秩至少二；後續
[私人雙環排除](c5_w5_private_rank2.md)覆蓋四型及所有essential位置，得到至少三。
974個theta模板全部有r′=0或4的實際annulus代表，減少3或7–10內點，只保完整Σ、
不保R³。後續[圈秩三環繞排除](c5_w5_private_rank3_essential.md)已排essential分支，
1,283模板皆全收十列；[contractible分支](c5_w5_private_rank3_contractible.md)也已完整排除。
後者由block-ear/leaf的M預算迫pentagon fan及原尾路徑，2,270份完備必要模板
全部Σ∈K132。後續[圈秩四兩分支](c5_w5_private_rank4.md)以contractible 6,389份及essential 2,872份完整模板再排ρ=4，
故任取合法W5的私人圈秩至少五，圈秩四沒有來源分支殘留。
依來源挑選五商圖及額外加邊的正聯集亦已排除；一般私人圈秩至少五的來源仍須
構造保完整Σ且嚴格減少內點的合法代表，或取得其他來源排除。
目前[最弱保存契約與合法替換](../audits/2026-10-13-w5-small-representatives-6cafdfb/REPORT.md)
只要求同色框完整Σ＝pr_B R³相等；保R³、環帶χ相等與完整染色數量相等均無須作為驗收條件。
K15已把小代表門檻提高為r′≤9，補中心後內點6+r′≤15；真正最小來源r≥10，
因此九點代表會嚴格縮小。另可找任何r′<r的合法同Σ代表，無須固定上界。
已認出的K132關係有102份r′≤5實際代表，另有一般annulus的嚴格替換族；
它們不觸發真正目錄外最小來源。一般九點代表仍OPEN，且在允許合法橋面的類中
與K∞=K≤5條件等價；來源含環不限制代表必須含環。
B固定域的1020項操作均不等價，不能據此排除一般縮減；其餘必要介面與重播
見[交付入口](c5_degree5_link_reductions.md)。

**完整外圈 h≤2 已排除（2026-10-13）。** 令 h=Σ_B(deg−4)。933／941 均必
h≥3、n5≥9。原最後 `(4,4,5,4,5)` 的具名 C7 55列上界，受到同一圖全部
延伸計數的 noncrossing 恆等式限制；外列 `01232` 的三個內列前像皆被迫
計數為零。既有 fan cap 另證沒有任何合法 disk C7 完整關係包含於該上界。
3,383 caps 與72個僅通過舊必要條件的抽象關係保留為反控制，沒有新增來源枚舉。
同日 [C₈ 完整 transfer 與共同計數](../audits/2026-10-13-c8-joint-count-3097ef5/REPORT.md)
已覆蓋 h=3 的70項查詢，普遍排除60項，保留933的2項、941的8項必要條件殘留。
後續 [C8-STRUCT](../audits/2026-10-13-c8-struct-243a125/REPORT.md) 以小cap／無內弦
定理與 cofacial 識別排除 c16-941、c32-941，現留933的c15/c18，以及941的
c04/c07/c15/c18/c20/c30。新增可逆軌道計數另使c15/c20-941各迫零兩列；
八項新向量通過共同計數、可逆交換與全部91個cofacial非空條件。
後續[C₈ apex度數](c5_c8_apex_degree.md)已排全部40項三度H假設，迫原apex
均degree≥6、H嚴格內側至少六個五度點；新[原面配對／無葉點證明](c5_k14_sphere.md)
排六、七個嚴格內點；後續[原短弧與內圈](c5_c8_inner_collar.md)證每I點至多兩個C附件、八條C邊third points全異，
迫m≥9。等號唯一W8內圈的八份完整關係皆1023，再排m=9；後續[原接點三型與剝層](c5_c8_peeling.md)
對任意大小證RING／PINCH／BRIDGE及完整separator轉移。m=10紙面三族16H回接八collars，128圖全Σ1023，故h=3只留k≥19。
後續 T1-CROSSCUT 已排除全部正對點，原八項只剩 RING；此定理本身不提高 k 下界，
當前另接 C4 來源橋的共同 k≥23。
下一個精確缺口是這八份原完整 target 能否由同一無內弦、符合度數及小cap限制的
RING 來源 H 實現，尤其三組色對分割間的共同分量／原面一致性；下一層度數、無弦與最多雙接不傳遞，需在完整具名separator轉移上另證更強縮減。更大h與普遍
跨邊同步亦保留。十三內點的h4–7已由[K13-COLLAR](c5_k13_collar.md)完整排除，
十四、十五內點由[K14](c5_k14_sphere.md)及[K15](c5_k15_sphere.md)全部覆蓋，
後續[C4來源橋](c5_c4_boundary_pivot.md)已排至二十二內點，當前共同k≥23；h≥3、n₅≥9不提高。
二十三內點以上及任意大小來源仍OPEN。
跨邊方向的下一個窄義務是：在上述共同 H lift 或其固定外框 Kempe 軌道中，
迫一對非相鄰 singleton 分量分離且至少一個避開原 B；一步交換便能補回中心。
兩者至少九點與全內部 W5 尚未供應此條件；各邊自己的拒絕列 full lifts 不能直接合併。
來源、全部欄與重播見[外圈報告](c5_neartri_boundary_collar.md)及[跨邊定理](c5_cross_edge_kempe.md)。

**主攻的共同義務（2026-10-11）：證 E-ARC2。**
把反例的拒絕三點整圖搬到 {0,1,3}，在同一來源、完整 relations／fibres／full lifts
及同一色框下排除三列共同拒絕。原域只需完整 941／933／940；940 隨整圖反射
回到 933。沿用 E3 的不限定其餘兩列版本時，另列 932，不預填接受列。
E3＋D₈ 已排唯一 degree-6，故證明工作集中於雙 degree-5；下列 N45 是其中的
窄入口；廣義N2後由N2-BRIDGE在原E4完整契約排除，N1、相鄰及其單-root／原55義務仍須覆蓋。
新增[真子圖單拒絕定理](c5_excess_two_arc_pair_critical.md)：兩-root44排除與單-root例外至多一列
給 |Z(G)|≤1，再由低 ε 合成推出每個真子圖至多單拒絕、任意兩核心覆蓋原 G。
逐邊至少釋放指定三列中的兩列，進而所有內點不可同接 b₂、b₄；這些是必要條件。
後續[原分量共同重色限制](c5_excess_two_arc_component_slack.md)把限制提升至整份C，
並在完整N2前提以飽和性接入N45-U：所有分量邊刪除均全收，所有非root點至多接
兩個相鄰框點，真core只剩單root-spoke省略。
再由[末端block與spoke共同排除](c5_excess_two_arc_spoke_closure.md)，完整N2的45／54
真cores全排；每條非框邊刪除全收，連roots在內每點至多接兩個相鄰框點。
**這個完整N2契約的原55共同矛盾已由下列LL-CUT+diag完成**：每個拒絕列都以有效原G作minimal core；
後續[原55大小界](c5_excess_two_arc_size_bound.md)已證H是中央block加至多兩個root葉blocks，
全H內度二點至多五個，所有原C為bridges／奇環cactus，且`|H|≤35−6u−3t`。
u=0／1／2時至多35／29／23內點；這是原圖必要界，尚未排除界內來源。
後續[N2殘餘統一](c5_excess_two_n2_residual_unification.md)以共同三-hub排兩unary，故u≤1；
singleton mixed只能在u=t=0。原55每欄仍有一單位容量；精確大小式保留Δ，
已知有限下界10沒有直接衝突。當輪含long的三個參數情形，
當時收窄至下列(2,0)，現以同列完整joint排除；未證新Δ門檻，未搜尋10–35內點。
其中(0,1)已由[三列diagonal獨立採納](c5_excess_two_n2_diagonal_three_row.md)排除，
當輪剩(2,0)、(1,0)、(1,1)，其中(1,1)已由下述全色Diff出口涵蓋。
[long同步新化約](c5_excess_two_n2_long_synchrony.md)
另排兩long都k≤3，以及一long無U的全葉接點tree（任意k）。含U的低接點long
與U非空mask若分屬Eq／Diff亦排除；原同類七模板已由
[接口與已用色禁色規律](c5_excess_two_n2_partition_rule.md#6-已用色禁色規律與原七模板的統一排除)
一起排除，不再逐模板處理。再由[兩接線U全色Diff出口](c5_excess_two_n2_unary_diff_closure.md)
以原五形及K₅排除全部完整(1,1)，不必先處理high-contact long接口。
再由[一long末端block與固定root接回](c5_excess_two_n2_one_long_closure.md)，
任意長leaf cycle由原框弧K₅排除；leaf bridges迫兩種四spoke必要配置，
固定root後完整外側染色與L碰色slack給同列全圖矛盾，關閉完整(1,0)。
**[LL-CUT+diag](c5_excess_two_n2_ll_cut.md)現排全部完整原55(2,0)，
指定完整Σ契約內九格全覆蓋。** 既有t=0／1與新t=2／3證明相接；
原leaf K₅／K₃,₃排除失敗diagonal的cycle接點型，leaf接線容量及最後2≤行和≤1
给同列完整joint。基本LL-CUT機制未獨立證成；19,229份共同可行投影及64,408份
contact介面組合保留，不能當作原圖實現或反例。若續研基本機制，可檢驗新報告的
BASIC-11-SAME-SITE弱化結構子命題；它已非完整原55來源排除的必要缺口。
四點支援未套三點弧兩位元；既有雙diagonal拒、off-diagonal接回控制及原K₃,₃
完整保存。所有新接回仍在同列、同pins取兩份完整原lifts。
SD-A只有單缺額，不能直接用於這份双degree5原G。N1、相鄰及單-root例外仍各保留。
較廣三列N2的前提不能自動提升為完整Σ，未取得整個 E-ARC2 的來源排除；
N2外45／54、原55及單-root例外不因此改為 CLOSED。
不使用指定三列拒絕前提的新共用引理須保留可實現的 ε=2、Σ=951／935 控制；
只證局部必要條件不算完成主目標。

跨線接續（2026-10-08）：[Phase B 共通引理候選分析](c5_phase_b_common_lemmas.md)
將原piece盾弧收費、任意兩自由roots的條件容量及跨列猜想E分開。
45／54入口須先核原unit省略身份與mixed支援下界，再核同一pins的完整joint；
U4的44專用下界不能直接搬用。一般化候選未證成新的來源排除，以下分支狀態保持。

**目前停止點（2026-10-13）：[N2-BRIDGE](c5_excess_two_n2_bridge.md)已排原E4契約的廣義N2，包含932。
E-ARC2仍OPEN：剩非相鄰N1，以及相鄰m=0／1／2；各自45／54、原55與允許的單-root4 core例外另保留。**
精確具名來源為EARC-NA1、EARC-AD0、EARC-AD1-A4、EARC-AD1-LOW及EARC-AD2，見
[父分類ledger](../audits/2026-10-13-n2-bridge-243a125/paper/PARENT_COVERAGE.md)。
唯一degree6原來源已由E3＋D₈排除；932與ε≥3不是原E-ARC2額外義務。
U4的原mixed11省略身份由原盾弧／star收窄、保留root的任意長run化約與
828份標記核心完整接回全排；3,312份三色列同座標容量碰撞均經獨立重算。
無44 core的來源、單-root例外與N2外45／54、原55 cores保留。
U3 mixed12／21的容量一由原star面、完整原側及C的重色列slack排除；
容量二固定為六內點，3,072雙spoke接回及10,240 unit-unary必要比較全排。
mixed11前輪以兩份原unary盾弧、原star面與完整slack排除；
U2 的126份triangle正常形／570標記、完整二接點接回及固定原支援排除保留；
前序唯一 mixed 四份指定稽核及U1來源身份排除保留。
各報告保留當輪停止點與歷史計畫，其他core型照舊。
原 A／B 的逐 pair 必要表仍供追溯，後續三列結論以 E3–E6 的完整前提為準。

| 已返回任務 | 已完成範圍與證據界線 |
| --- | --- |
| K′ | 在同一G−p的拒絕見證ψ（q∉Σ(G)）下，[引理1–6及Jordan側別](c5_kempe_diagonal_transport.md)迫單點四色鄰域的兩條對角鏈皆斷開；933／941仍有192／384筆一致指派，可實現1012／935控制各192。同 ψ 多鏈交換無新排除，局部資料不能分辨來源；K′未決，K型局部題停止 |
| E3／D₈ | [三列約化與triple-critical](../artifacts/c5_excess_two_e3/REPORT.md)；唯一degree-6全分支排除須引用[D₈](../audits/2026-10-04-task-d8/REPORT.md)的DG6-1補表：t=1的(4,1)／(3,2)相對spoke位置100份幾何零存活。E3對A前序的依賴過強更正已保存 |
| E4 | [非相鄰m≤2與N3全排](../artifacts/c5_excess_two_e4/REPORT.md)；N1排mixed22有(4,4)core，N2排兩短無unary，其餘N1／N2保留。當輪缺少的非相鄰正控制後由ES／E4C提供；N∅／L-spoke已由NA6-1–3否定 |
| E5／E6 | [四分支依賴表](../artifacts/c5_excess_two_e5/REPORT.md)與[相鄰m≤2](../artifacts/c5_excess_two_e6/REPORT.md)關閉J6的m≥3。G2的U盾弧恰二；G3剩具名支援約束；G4只剩盾弧恰三；no-mixed為941的013三-spoke或兩側≤2。G1依actual core轉交，G1–G4、J6的m≤2及J4其餘殘留未全排；紙面＋Python，未Lean化 |
| E4C | [54個NA critical orbits ×60項](../artifacts/c5_excess_two_e4c/REPORT.md)不用三列的控制：42項有觸發前提的圖、18項無控制、0反例。真正控制缺口為singleton盾弧、root刪除例外、(4,4)core、根間bridge整側、單root重色core；不把未觸發前提當作引理已驗證 |
| ES／ER | [ES](c5_excess_two_finite_search.md)與[獨立ER](c5_excess_two_independent_search.md)三型k≤9的q／critical orbit集合、計數及Q分布逐層一致，179個critical orbits（NA54／AD9／D6 116），無\|Q\|+c(Q)>4。完整性為有限雙實作證據，ER另依賴plantri；k≥10未搜尋 |
| LC | [179／179個Lean soundness證書](c5_excess_two_lean_certificates.md)，558項axioms audit無sorryAx。拒絕列用native_decide，組合嵌入不等於拓撲disk定理，也不證搜尋完整性。未接入Math.lean／預設CI；是否接入的提議保留 |
| D₉ | [E4／E5／E6紙面引理獨立稽核](../audits/2026-10-06-task-d9/REPORT.md)：N-empty-separating、N-theta、N1-22-44、L1–L8、相鄰m≤2、G2–G4及no-mixed預算全部成立，無新缺口；54 NA＋9 AD控制零反例。指定三列來源前提0／63觸發，三列下的來源排除無有限控制。歷史provenance FAIL與E3 degree6.json未入封存照實保存 |
| C44 | [三型k≤9全部minimal cores](../artifacts/c5_excess_two_c44/REPORT.md)：9,644 q-orbits／179 critical，k≤6逐邊集與暴力一致。具名[C44-AD3-row0-44](../artifacts/c5_excess_two_c44/counterexample_C44-AD3-row0-44.json)（Σ956、Σ-critical；相鄰兩root各三spoke見框色0,1,2，皆迫色3）反駁一般「無兩-root (4,4) core」。當輪加完整Σ933／941前提的窄命題未證；後續U1–U4完成此兩-root44身份。有限域無目標來源，有限統計本身對該前提無控制 |
| C44′ | [Σ相容篩](../artifacts/c5_excess_two_c44p/REPORT.md)：C44保存的2,416份兩-root (4,4) occurrences（213份literal core）全部相容；兩private頂點型125 placements中30份可嵌disk、10份相容（一個orbit，具名C44P-AD2-012-034，Σ959）。**篩本身近乎無效：** 933的D₅像恰為T4加任一個非T4列（五列皆可），941為T4加兩列；同框子圖繼承T4，故只拒一個非T4列的core必相容。Σ層必要條件不能排(4,4) core，排除須用來源的多列聯合、criticality或spoke預算；停止此方向 |
| C44″ | [雙-root (4,4) 覆蓋表](../artifacts/c5_excess_two_c44pp/REPORT.md)：完整Σ=933／941下，相鄰m=1已有舊系列全排且不需K′；兩份AD-012-034具名core不能來自此前提的兩-root44來源。當輪整理覆蓋與必要限制；後續指定稽核及U1–U4排除見下列各項 |
| 唯一 mixed 指定稽核 | [四份舊排除稽核](../audits/2026-10-07-c44pp-mixed-audit/REPORT.md)：任意大小化約與固定域核對通過，獨立重算root pairs／S₄支援／368,859份UNSAT proofs／6,008份subdivisions；344域的標記run覆蓋亦通過。沿用上游分類，未重稽核其全部枚舉，未補E5的新證明 |
| U1 no-mixed44 | [U1排除](c5_excess_two_no_mixed_core44.md)：spoke＋unit-U由單點D-forcer與triangle palette衝突；雙spoke以全部344份bridge-marker核心的3,498次接回全排，涵蓋941三-spoke側並更正原收窄。兩-root44身份全排；其他no-mixed core型及root刪除例外保留，紙面＋Python，未Lean化 |
| U2 相鄰兩 mixed44 | [U2排除](c5_excess_two_adjacent_two_mixed_core44.md)：任一原mixed11 D的Σ(G−D)=Ω；126份triangle正常形／570root標記、5,700比較及2,016固定支援查詢全排，99份相容者由27份明示subdivisions排除。獨立支援計算一致；其他相鄰m=2 core型保留，紙面＋Python，未Lean化 |
| U3 非相鄰 sole mixed11 | [U3 mixed11 排除](c5_excess_two_nonadjacent_one_mixed_core44.md)：兩側各有一份原 unary，容量11由外側apex K₃,₃、22由雙triangle直接bridge排除；12／21容量由原star face迫C全部附件為同一非相鄰pair，指定拒絕列重色給兩側與整份C的完整slack延拓。全部unit省略身份涵蓋，mixed12／21 incidence由下列後續涵蓋；紙面＋Python控制，未Lean化 |
| U3 非相鄰 sole mixed12／21 | [U3 mixed12／21排除](c5_excess_two_nonadjacent_mixed12_core44.md)：排兩份unary同接一-contact root；容量一由原star面與盾弧迫C支援落在同一非相鄰pair，完整原圖slack延拓；容量二用64份六內點核心／256標記的完整接回全排。補充336單triangle標記／208明示K₃,₃亦零殘留；單-root及45／54／55保留，紙面＋Python，未Lean化 |
| U4 非相鄰兩 mixed | [U4排除](c5_excess_two_nonadjacent_two_mixed_core44.md)：原O11仍支付盾弧，ℓ+2u≤3排兩unary；三-spoke star排u1的無unary側d1。單triangle316必要上界標記與雙triangle512標記的完整joint全排，3,312三色列碰撞使原O11不能新增三色拒絕列。8,280目標比較／132,480含空fibres／316長圖及獨立回溯均通過；紙面＋Python，未Lean化 |

**完整Σ933／941或整圖D₅像下的兩-root44身份已全排。** 沿用disk、Σ-critical、
ε=2、完整degrees、同源contacts／attachments；逐格前提與前序出處見C44″，
本輪最後一格見[U4報告](c5_excess_two_nonadjacent_two_mixed_core44.md)。

U1 已由 [no-mixed44](c5_excess_two_no_mixed_core44.md)、U2 已由
[相鄰兩 mixed44](c5_excess_two_adjacent_two_mixed_core44.md) 排除；U3 的 incidence11 已由
[原 star 與重色列延拓](c5_excess_two_nonadjacent_one_mixed_core44.md)、incidence12／21由
[同源star面及六點接回](c5_excess_two_nonadjacent_mixed12_core44.md)排除，22沿用E4；
U4由[原mixed11完整接回](c5_excess_two_nonadjacent_two_mixed_core44.md)排除。
這些結果只處理兩-root44 core；單-root 的 N1 刪 root 例外另保留，
(5,4)/(4,5) 及原 G 的 (5,5) core 也未因此排除。
E3 的三列推廣不能直接復用部分精確 Σ 證書；E5／E6 在精確 941／933／940
也依其「新證明」要求保留 G1。C44″ 與本輪指定稽核不完成那項任務；
上游degree-4／triangle分類的全部枚舉沒有重新稽核。
**既有45／54入口及後續：** 非相鄰N2的原unit省略身份，見
[N45權威入口](c5_excess_two_nonadjacent_unit_core45.md)及
[E4完整原relation介面](../artifacts/c5_excess_two_e4/REPORT.md#6-完整原-relation-的參數化交付與-core-身份)。
原工作先固定spoke或capacity-one unary省略、完整mixed／附件／盾弧與空fibres，
分開G的Σ-criticality與core的q-minimality。此完整N2的45／54義務現由
[spoke共同排除](c5_excess_two_arc_spoke_closure.md)收尾；當輪原55缺口現由
[LL-CUT+diag](c5_excess_two_n2_ll_cut.md)完成指定完整Σ契約的覆蓋，單-root例外另保留。
U4三色列相等不推升成全部十列Σ相等，1018控制界線保留。

下列N45／SD-A／BR批次保留各輪採納及當時OPEN語境；目前完整N2的45／54覆蓋以
上方停止點及N45§2.14為準，歷史子型缺口不再作此域的存活清單。

**N45批次（2026-10-09）：** 此45／54入口拆為原spoke省略、整unit unary省略、
非相鄰完整joint校準與共同前提獨立稽核，四份可併行；發布全文、凍結基準及驗收見
[N45任務批次](history/2026-10-09-n2-45-54-parallel-tasks.md)。[N45-J](../audits/2026-10-09-n45-j/REPORT.md)
已通過[監督驗收](../audits/2026-10-09-n45-j-supervision/REPORT.md)，限χ=0兩mixed的工具與固定控制。
[N45-A首輪](../audits/2026-10-09-n45-a/REPORT.md)已驗收共同依賴；
[N45-S](../audits/2026-10-09-n45-s/REPORT.md)六項及[N45-U](../audits/2026-10-09-n45-u/REPORT.md)八項
經[SU-A紙面](../audits/2026-10-09-n45-su-a/REPORT.md)、[SU-J有限](../audits/2026-10-09-n45-su-j/REPORT.md)
及[監督採納](../audits/2026-10-09-n45-su-supervision/REPORT.md)，第一批驗收完成。
只關指定spoke省略的兩原unary、整U省略的兩原unary與兩short子型；
零slack、2／3 incidence及新γ singleton forcing等必要化約已採納。
**第二批採納（2026-10-10）：** [PG／PR／PC與三份獨立稽核](../audits/2026-10-10-n45-p-supervision/REPORT.md)
完成限定驗收；N45-U-LP（唯一U＋long L＋真框邊pair S，整U省略45／54）已由任意大小
paper及單-root三分排除。原拓撲必要條件、五個relation lemmas與PC有限工具分層採納；
ENDPOINT另保完整原piece的owner-neighbor與degree4前提，沒有新Lean或source實現。
**SS後續採納（2026-10-10）：** [SS與SSA／SSG／SSC](../audits/2026-10-10-n45-ss-supervision/REPORT.md)
完成限定驗收；原盾費(2,2)/(2,3)/(3,2)全排，長3兩內點由T4直接排，長2由實際sole C接回BASE三分。
加上已採納U化約及LP，指定X=M、unique原rx、保兩原mixed的整U省略45／54身份已全排，
完整覆蓋見[N45§2.2](c5_excess_two_nonadjacent_unit_core45.md#22-n45-u-ss-與指定整-u-身份的完整覆蓋)。
**LOW1後續採納（2026-10-10）：** [LOW1與L1A／L1R／L1C](../audits/2026-10-10-n45-low1-supervision/REPORT.md)
排除原 U incidence1在降度側、只刪原 r-spoke的完整LOW1契約。U／兩short全留，
實際X−s sole C、完整join與兩異色s-spokes接回BASE三接點原K₅；任意大小paper／Gallai與工具分層。
該輪只採納LOW1；原[LOW2任務文本](history/2026-10-10-n45-low1-adoption.md)及八pins保留日期語境。
**LOW2與限定LOW覆蓋（2026-10-10）：** [LOW2與L2A／L2R／L2C](../audits/2026-10-10-n45-low2-supervision/REPORT.md)
採納原 U incidence2在r、兩contacts及cycle全留、僅刪唯一r-spoke的完整LOW2契約。
r無框邊的實際sole C／完整join／精確F與原K₅ tethers逐項重核，仍依賴BASE與外部Gallai。
L2A另核degree5身份u+t=3、u,t≥1，只有LOW1(1,2)與LOW2(2,1)；
故[N45§1精確S身份的S-SHORT-U-LOW](c5_excess_two_nonadjacent_unit_core45.md#24-n45-s-low2-與指定-low-身份的完整覆蓋)已全排。
該輪[HIGH1任務](history/2026-10-10-n45-low2-adoption.md)保留發布時語境；沒有新LOW2來源或Lean。
**HIGH1限定採納（2026-10-10）：** [H1A／H1R／H1C及監督](../audits/2026-10-10-n45-high1-supervision/REPORT.md)
核十claims與全部H1–H13，排除原U incidence1在s、s兩spokes全留、僅刪r原spoke且X=M的HIGH1。
實際(2,1)接合保全部r色fibres；原G的K₃,₃九鄰接、U盾support及同列未用D的完整原G lifts成立。
BASE／外部Gallai、paper與toy分層，沒有新HIGH1有限來源或Lean。
**HIGH2／HIGH3與限定兩short覆蓋（2026-10-10）：**
[監督驗收](../audits/2026-10-10-n45-high23-supervision/REPORT.md)採納完整HIGH2／HIGH3契約。
HIGH2保雙U-contact／cycle、全部r fibres與恢復e，原兩W完整assignments給三色列的原G lifts；
未用Dγ構造明限proper三色γ，原「全部properγ」過寬量詞由H2A／H2R及父端保finding，原worker不改。
HIGH3原s無spoke、實際C/U=(2,3)逐項接回BASE no-spoke原K₅排除。
在上述限定HIGH身份中，原U incidence／s-spokes只有(1,2)/(2,1)/(3,0)，由HIGH1–HIGH3窮盡；加LOW兩支，
[§1精確S身份的兩原mixed都short分支](c5_excess_two_nonadjacent_unit_core45.md)已全排。
目前窄殘留為S含至少一份原long；先有[保留U/L/S的同源契約與必要化約](../audits/2026-10-10-n45-s-long-contract/REPORT.md)，
分pair／singleton原盾費，核全pins／空fibres與恢復e。
後續[U在r的sole C完整映射](../audits/2026-10-10-n45-s-long-r-map/REPORT.md)已接回
BASE(5)/(4)/(3)，排除完整U owner=r、long／short全留、只刪原r-spoke且X=M自身minimal身份。
**U在s後續限定採納（2026-10-11）：**
[DIRECT／FIBRE驗收](../audits/2026-10-11-n45-s-long-s-review/REPORT.md)先排四profiles及
餘兩profiles的singleton／pair13／pair31。pair22的28個raw schedules中既有4已排，
本輪[q0三份](../audits/2026-10-11-n45-s-long-s-t2-q0-restore-review/REPORT.md)、
[q2七份](../audits/2026-10-11-n45-s-long-s-t2-q2-restore-review/REPORT.md)、
[T1十四份](../audits/2026-10-11-n45-s-long-s-t1-rfibre-review/REPORT.md)逐份給同源完整恢復lift或原K₅，
全部24 schedules／38 spoke queries獨立採納，整合必要域剩0。六profiles及所有允許splits的
精確覆蓋／前提見[N45§2.10](c5_excess_two_nonadjacent_unit_core45.md#210-n45-s-long-s完整-cu-與原-r-fibre-恢復的限定覆蓋)。
q0保已採納SF-QX/E2紙面及歷史finite-terminal信任鏈；q2/T1的新非空性由新紙面構造承擔。
q2補112 X空cells、T1補352 X及780 G空欄位，採納副本與原bytes分開。
[D完整assignment transfer](../audits/2026-10-11-n45-s-long-s-block-transfer-review/REPORT.md)
另採納恆等式與1,344原邊assignments校準，新增來源排除0，未證一般Δ非空引理。
JOINT固定21省略／210列／3,360pins只校準；target來源not triggered，兩份缺BASE blob finding保留。

**單缺額接續：** [A查證](../audits/2026-10-11-c5-single-deficit-biconnected-5e7a5ffd/REPORT.md)已通過，
[B適用性](../audits/2026-10-11-single-deficit-applicability-804e3b0b1b/REPORT.md)的歷史conditional保留；
各實際core仍須核X=M／degrees／二連通。[N45§2.11](c5_excess_two_nonadjacent_unit_core45.md#211-單缺額查證與無-u-二連通子域)
記三項subset排除與Gallai鏈縮減，完整OPEN身份新增關閉0。
**BR-SD-1a 已採納：** [N45§2.11](c5_excess_two_nonadjacent_unit_core45.md#211-單缺額查證與無-u-二連通子域)
接入已獨立驗證、封存及發布的任意大小 D-palette 矛盾，只排 split22／共用 r／
三環單 bridge 無旁支精確合同；此直接證明不依二連通，完整父身份仍 OPEN。
**BR-SD-1c 已採納：** 同骨架的一份原有限非空 W 只接 J1/J2，保 actual S pair support
及未改動 J3／q 外臂的任意大小精確合同亦排除，完整前提與 terminal lemma 界線見 N45§2.11。
**BR-SD-1e 已採納：** 同骨架恰一份原有限非空 W 唯一接 J3／q 外臂，保 actual S pair、
完整 degree與原資料的任意大小精確合同排除；J1/J2 private witnesses 對全部允許接點保持。
此證明不依1c terminal lemma；W 可破壞其末端／無額外 C 邊前提，preservation lemma 另有完整結構界線。
完整父身份、多旁支及一般 Gallai block tree 仍 OPEN，完整 OPEN 身份新增無條件關閉仍為0。
**BR-SD-1g 已採納：** [原 PROOF](../audits/2026-10-11-br-sd-1g-dbdc4c35/PROOF.md) 經
[獨立採納審查](../audits/2026-10-11-br-sd-1g-adopt-6eae3597/REPORT.md) 通過並封存，owner 批准採納
W1 唯一接 J1 triangle 原 witness x1、W2 唯一接原 x2∈J3∪q-arm 的雙原旁支精確合同。
保同一原 G／M／β、無 U／L long／S short／actual pair、r split22、完整degree／原附件／witnesses與
M 自身同 β minimal 拒絕；W1/W2 原 ownership 為 L/S，無第二接口、額外 s-contact／相互邊／其他旁支或cross edge。
任意 J2/J3 奇長≥3、原 p/q 臂長≥0（含零長及 a3=v）、有限 Wi 大小、全部合法接點／mi
與具名重合，原完整 relations／空 fibres／full lifts及被忽略原坐標因子均保留；完整八項前提見 N45§2.11。
保留的 J2 witness 與唯一 S–L 接口給同一 `P_J2={T,D}` 屏障，q 起始T/D追色在有限原S incidence tree矛盾；
不使用失效的 cutpoint 推論，不依二連通或 R31 minor。任意大小是独立審查的紙面結果，六個 synthetic fixtures不作外推。
actual source `not triggered`，無新 Lean；完整 `N45-S-NOU-LS-PAIR`、未涵蓋兩／多旁支與一般N45／N2／E、ε≥3、
`K∞=K≤5` 仍 OPEN，完整 OPEN 身份新增無條件關閉0；詳見[degree-5 導覽§4](c5_degree5_guide.md#4-r31-保留缺口與重播入口)。
舊 B 的 R27 minor 任務保持封存語境，1a／1c／1e 採納與 residual 對帳分別見
[BR-SD-1b](history/2026-10-11-br-sd-1b-adoption.md)／[BR-SD-1d](history/2026-10-11-br-sd-1d-adoption.md)／
[BR-SD-1f](history/2026-10-11-br-sd-1f-adoption.md)。
1g 的精確採納、reviewed-unchanged consumers 與實際 publication custody 另見
[BR-SD-1g 紀錄](history/2026-10-11-br-sd-1g-adoption.md)；原 1g candidate audit與既有 seals保原bytes。
**後續唯一缺口共同排除：** [新紙面定理](c5_two_color_single_gap_bridge.md)與
[N45§2.12](c5_excess_two_nonadjacent_unit_core45.md#212-雙色唯一缺口的共同排除)已統一四份 BR。
保同一原圖的 degree lists／拒絕／完整延拓、完整 S、actual 異色 pair、唯一 s-contact q，
r 對 S 至少兩個原 contacts 即矛盾；旁支數／位置、三環形狀及 private witness 不再需要。
上列「多旁支／其他形狀 OPEN」扣除這個完整域；剩餘須按單 r-contact、多個 s-contacts、
未證雙色 lists／其他出口及更廣父身份區分。任意大小紙面＋外部 Gallai，無新有限來源或 Lean，E 仍 OPEN。
該共用引理當輪保留一般非二連通來源及其他cores；後續N2 exact-S已由[N45§2.14](c5_excess_two_nonadjacent_unit_core45.md#214-e-arc2-接入全部-spoke4554-排除與原55化約)涵蓋，
指定完整Σ契約的原55再由[LL-CUT+diag](c5_excess_two_n2_ll_cut.md)覆蓋；N2外其他core及一般N2／E仍保留，未執行新來源搜尋。
原[HIGH2派工](history/2026-10-10-n45-high1-adoption.md)保留當輪語境；
兩支的採納／finding／完整tree與custody界線見[本輪紀錄](history/2026-10-10-n45-high23-adoption.md)。
來源paper依BASE／外部Gallai，無新finite來源或Lean，其他cores／一般N2／E仍OPEN，傳播停止L2。
精確N2目標45／54控制仍0觸發，finite不承擔新paper排除；歷史provenance／文件FAIL保留。
原55及無45／54來源不在這批身份排除的範圍。

本輪驗證見[U4紀錄](history/2026-10-08-u4-two-mixed-core44.md)；U3見
[mixed12紀錄](history/2026-10-08-u3-mixed12-core44.md)；mixed11見
[前輪U3紀錄](history/2026-10-08-u3-one-mixed-core44.md)；U2見
[U2紀錄](history/2026-10-08-u2-two-mixed-core44.md)；U1見
[前輪紀錄](history/2026-10-07-no-mixed-core44.md)，整合見
[整合覆核紀錄](history/2026-10-07-c44pp-integration-review.md)。

不新開逐spoke-pair輪次、擴大k搜尋、案例樹ledger、K型局部題或Lean
枚舉completeness試點。雙degree-5的N1／N2、G1–G4、J6剩餘、no-mixed、
較少spokes、原(5,5)core及一般來源未全排；猜想E任意大小、一般出口與K∞=K≤5未證。
另一個保留題目是把Σ|σ|≤5與逐列D+O恆等式合成單一不等式。
本次重播、歷史文件hash漂移與分支發布見
[發布紀錄](history/2026-10-04-kprime-excess-two-progress-publish.md)。

以下保存固定完整Σ933／941的A／B原身份與停止點；其逐pair下一步不覆蓋上方窄提議。

本線候選來源前提是固定完整 Σ=933／941 或整圖 D₅ 像、每條非框邊
Σ-critical、指定有序 induced-C₅ disk、所有有效內點完整 degree≥4。
原分量、有序 contacts、實際 attachments／supports、ownership、嵌入
環序及同一字面四色框始終保持。任意大小化約由紙面與明列外部依賴
承擔；Python 檢查固定必要域、完整 tuples／fibres 及具名 minors。

**共同 ε≥2；唯一 degree-6 的 ε=2 分支已全排。** 941 的 ε=1
全部分支及唯一 degree-6 的 t=0、1、2、3 全分拆見 §2 原報告。
因此 ε=2 只剩兩個完整 degree-5 roots。

| 雙 root 分支 | 最新已完成範圍 | 精確報告 |
| --- | --- | --- |
| 原 root 刪除 | 至少一個刪 root 圖全收，另一個至多缺一列；相鄰且有 mixed 時兩者均全收 | [完整 Σ 與原刪除](c5_excess_two_root_deletions.md) |
| 相鄰 mixed 的原 zw 省略 | 雙 triangle、原樹／偶數路徑與單 triangle 接回全排；Σ(G−zw)=Ω | [雙 triangle](c5_excess_two_root_deletions.md)、[原路徑](c5_excess_two_path_edge.md)、[單 triangle](c5_excess_two_triangle_edge.md) |
| 相鄰唯一 mixed 的 (4,4) q-core | 保留 mixed 的雙 spoke、spoke＋unary、雙 unary 身份及只省略 incidence-(1,1) mixed 的身份均全排 | [原身份表](c5_excess_two_mixed_core_spokes.md)、[spoke＋unary](c5_excess_two_mixed_core_spoke_unary.md)、[雙 unary](c5_excess_two_mixed_core_two_unary.md)、[mixed 省略](c5_excess_two_mixed_omission.md) |
| 相鄰唯一 mixed 的單 spoke 省略 | 省略圖若拒絕 q，自己就是唯一 degree-5 minimal q-core；同色原 spoke 身份限制三-spoke 附件 | [單 spoke 原附件化約](c5_excess_two_mixed_core_single_spoke.md) |
| 相鄰唯一 mixed 的五-spoke 原來源 | 八份具名附件共同搬運至 998／1004；原 (b,a,y,u) joint leaf 纖維、同一 unary 雙列 palette 與原圖 K₅ 全排；兩候選總 spokes 都≤4 | [原 leaf 色纖維](c5_excess_two_mixed_core_leaf_fibers.md) |
| 四-spoke (3,1) 的 mixed-(1,1) 加兩原單接點 unary | 原 Σ-critical witnesses、b–a–框點外路徑與短支援定理迫三份原分量跨度至少六，與共同五段 lifts 矛盾，含 root 交換；288 同源支援域與完整五點 joint 核對 | [兩原 unary 的六跨度排除](c5_excess_two_mixed_core_four_spoke_singles.md) |
| 四-spoke (3,1) 的 mixed-(1,1) 加一原 binary unary | 原 star 殘留32／64份由同列 tightness／端點 hub 的二、三 hub Gallai K₅ 全排，含root交換；192原query、10,752完整U schemas與42原degree圖核對。完成這個原incidence子型，ε≥3未證 | [同列端點 hub 排除](c5_excess_two_mixed_core_four_spoke_hubs.md)、[原 star](c5_excess_two_mixed_core_four_spoke_star.md)、[marked-leaf](c5_excess_two_mixed_core_four_spoke_binary.md) |
| 四-spoke (3,1) 的 mixed-(1,2) 加一原單接點 unary | 同色原 spoke 省略後 M 自己 minimal；原 K=C+a 的三接點 (a,y₀,y₁) 接上既有 active-triangle K₅，全部20／60框架全排，含root交換。200 queries、50完整degree圖、1,500 joints／24,000纖維；紙面＋Python，ε≥3未證 | [原三接點身份與整型排除](c5_excess_two_mixed_core_four_spoke_ternary.md) |
| 四-spoke (3,1) 的 mixed-(1,3) 無 unary | 原 K=C+a 的四 contacts=(a,y₀,y₁,y₂) 要求三禁色，但 marked leaf 迫至多二；原逆序貪婪直接構造 M／G 延拓，20／60 框架全排，含 root 交換。80 完整 degree 圖、2,400 joints／38,400 纖維及 2,400 貪婪 witnesses；結合前三子型完成全部 (3,1) incidence 分拆 | [原四接點 leaf-slack 排除](c5_excess_two_mixed_core_four_spoke_quaternary.md) |
| 四-spoke (2,2) 的 mixed-(1,1) 加各側一原 unary：共用 pair | 原 spoke diamond 封 C 於一個原三角形，既有三-hub 引理延拓每份合法原三角染色；接原 G−C 全收迫 G 全收，排除相同 pair 的 7／9 份，含原 01／01 與 root 交換。當輪 unequal 殘留由下列短 face 進一步收窄；36 完整 degree 圖、2,520 joints／40,320 fibres | [共用 pair 的 sealed mixed 排除](c5_excess_two_mixed_core_four_spoke_equal_pair.md) |
| 四-spoke (2,2) 的 mixed-(1,1) 加各側一原 unary：短 face | 原 01／02 的 a-side unary 只能碰 01、0 或 12；原外部路徑與短支援引理使 au 非 critical。含 root 交換及同機制 8／16 份；後續長 face 進一步收窄。74 原骨架的 7,104 rotation assignments、完整六點 joints／空纖維與原 unary witness 替換保存 | [原 unary 短 face 與非 critical 接線](c5_excess_two_mixed_core_four_spoke_short_face.md) |
| 四-spoke (2,2) 的 mixed-(1,1) 加各側一原 unary：同一長 face | 原 01／04 的 U、V 若 critical 必同在三段長 face；實際支援次序迫跨度和≤3，短支援引理迫≥4，故固定一條 unary 邊非 critical。含 root 交換及同機制 10／10 份，unequal pairs 剩 22／40；5,120 actual support pairs、120 explicit apex K₃,₃ subdivisions 與完整六角色 joints 保存 | [同一長 face 的原 unary 次序排除](c5_excess_two_mixed_core_four_spoke_long_face.md) |
| 四-spoke (2,2) 的 mixed-(1,1) 加各側一原 unary：原 crosscut | 原 941 01／03、933 01／13 的 critical unary 迫原 owner-to-support crosscut，封 C 至一框點；同一外路徑及 tightness 保 degree 的二／三 hubs 使完整 C 延拓每份原外部染色，原 ax 非 critical。含 root 交換新排 8／16，unequal 剩 14／24；48 apex subdivisions、720 joints／11,520 fibres、7,752 C 替換 witnesses | [原 unary crosscut 與 mixed hubs](c5_excess_two_mixed_core_four_spoke_crosscut.md) |
| 四-spoke (2,2) 的 mixed-(1,1) 加各側一原 unary：共用短框弧 | 941原02／03及最後六份共用點身份用原C短支援Fempty與完整relation穩定子構造候選拒絕列01021的同框joint；963C schemas、101,115六角色tuple witnesses、1,320整圖joins／21,120fibres。當輪殘留14／18由下列完成報告全排 | [短框弧原拒絕列延拓](c5_excess_two_mixed_core_four_spoke_short_arc.md) |
| 四-spoke (2,2) 的 mixed-(1,1) 加各側一原 unary：不相交pairs及整型完成 | 原不相交pairs一側全短faces4／8、共同兩段長框弧10／10全部非critical，完成原47／75必要身份。2,048rotations、1,280actual支援對、60apex subdivisions與完整identity ledger；所有原C/U/V保持，其他incidence及ε≥3保留 | [原子型完成](c5_excess_two_mixed_core_four_spoke_disjoint_pairs.md) |
| 任務 A／A₂／A₃／A₄：四-spoke (2,2)、mixed-(1,2)+a 側原 unary | 原01／23、01／12、01／01、04／04及root交換來源排除。A₄重核四rotations，原C支援{0}／{4}、U含123；原互異色三hub及exact degree-list延拓完整C使ax非critical，01202的U singleton1／3均給完整joint矛盾。保存其餘16／20框架、40／58actual支援與50／84schedules；24完整degree控制、240投影等式與2,912整份C替換witnesses。紙面＋Python、整型未排、ε≥3未證 | [A 的原身份](c5_excess_two_mixed_core_four_spoke_mixed12.md)；[A₂的01／12排除](c5_excess_two_mixed_core_four_spoke_mixed12_01_12.md)；[A₃的共用01／01排除](c5_excess_two_mixed_core_four_spoke_mixed12_01_01.md)；[A₄的原04／04排除](c5_excess_two_mixed_core_four_spoke_mixed12_04_04.md) |
| 任務 B：四-spoke (2,2)、mixed-(2,2) 無 unary | 七份具名跨側共享身份及完整四接點／root-pair joint；四條原 spoke 省略各自 Ω，原拒絕 q-core 必是 G (5,5)。47／75 骨架各縮至25相鄰pairs，sealed triangle各排5，20／20原face必要見證保留；tightness及leaf-owner限制、28完整degree控制。任意大小紙面＋Python，未排整型、未證ε≥3 | [B 的原四接點身份與窄化約](c5_excess_two_mixed_core_four_spoke_mixed22.md) |
| B₂：mixed-(2,2) 固定原01／23短 face | W933-101／W941-139的原短face{1,2}全來源排除，七身份零殘留；Gallai leaf的四種owner各由實際外鄰及原外部路徑給K₅。完整四接點fibres保持；同骨架長face由B₃獨立涵蓋，整型保留，紙面＋Python、未Lean化 | [B₂ 原leaf／路徑提取](c5_excess_two_mixed_core_four_spoke_mixed22_short_face.md) |
| B₃：mixed-(2,2) 同骨架原長 face | W933-101／W941-139長face{0,4,3}獨立全排，七身份零殘留；shared leaf bridge由跨列slack排除，五種原leaf各以實際外部路徑給K₅。完整四接點fibre與原bridges保持；兩W的短／長faces分別證成，其他骨架及整型保留，紙面＋Python、未Lean化 | [B₃ 原長face窄引理](c5_excess_two_mixed_core_four_spoke_mixed22_long_face.md) |
| B₄：933 原04／12、shared contact附件{4} | 精確W933-129長face{2,3,4}；shared leaf在11原pairs全tight，刪leaf後13鄰點附件排5留8。原K=C−v的完整degree cut迫奇數框附件，五原bags給K₅，六shared身份／八指定選擇此支全排；40完整degree圖、2,400joins／38,400fibres。其他附件／身份及整份骨架保留，紙面＋Python、未Lean化 | [B₄ 原shared leaf／cut parity](c5_excess_two_mixed_core_four_spoke_mixed22_shared4.md) |

**停止點：(3,1) 全部四份incidence分拆封閉；(2,2)、mixed-(1,1)
加各側一原單接點unary整個子型亦封閉，含root交換。** 原47／75
具名必要身份由共用pair7／9、短face8／16、三段長face10／10、
原crosscut8／16、共用短框弧0／6及不相交pairs14／18完整覆蓋；
identity ledger核對無重複／遗漏，最後殘留0／0。
三種最新論證分清原C替換的四角色投影、原拒絕列的完整joint、
原短unary替換的五角色投影；不把六角色joint或來源Σ當作收縮不變量。
完整原relations與actualsupports保留；只替換固定短unary的整份witness，
C與另一unary外部頂點逐點保持，主張五角色投影相等。固定必要表不提供來源實現。

**任務 A／A₂／A₃／A₄ 停止於 mixed-(1,2)+a 側原 unary 的01／23、01／12、01／01、04／04來源排除，含root交換。**
原a-spoke省略及整份G−U各自Ω的ternary身份沿用A；A₂的原crosscut、
A₃的01／01四rotations／singleton2／3與18／22歷史ledger保持。
A₄重新核對原04／04及root交換：四rotations的共同C faces始終為0ab、4ab，
完整degree握手式迫actual support為{0}或{4}；完整來源支援迫U實際含123，
U長face使用a=5的indices1,2、a=6的0,3，root交換index map為[1,0,3,2]。
原a,b,h三角本來連通、三色互異，逐點exact list等於deg_C，原外部路徑
與K₄排除前提完整核對，故任意大小C皆能延拓。只替換整份原C、固定其餘
原頂點，得π_(a,b,u)J_G=π_(a,b,u)J_(G−ax)，使固定原ax非critical；
完整六角色joints不必相等。01202的原R_U={d}、d=1或3時，
取(a,b,u)=(4−d,d,d)再接出完整原joint而違反拒絕，不沿用A₃色表。
保留完整R_C(x,y₀,y₁)、R_U(u)、actual supports／原schedules及字面色框；
y₀≠y₁、x獨立或共享其中一原接點均保持。新incidence必要域70／90
經A至A₄保存16／20框架、40／58actual U支援與50／84完整schedules。
24張固定完整degree圖／30,720fibres及2,912份整份C替換witnesses只是
關係控制，不實現來源或ledger schedules。詳見[A₄報告與完整殘留](c5_excess_two_mixed_core_four_spoke_mixed12_04_04.md)。
後續[盾弧預算](c5_unary_shield_budget.md)以支援連續性與 spoke 限制，將其餘actual U支援紀錄刪至24／30、schedules刪至30／50，16／20框架各仍有殘留。
原pair層停止於此；其他共用pairs與unequal入口保留。歷史提議是固定原12／12
及root交換，再逐項核對自身四rotations、原support／schedules與完整ternary。
未將04／04結果登記到其他pairs，mixed12整型與ε≥3仍未證。
A₄直接證明原入口，未用D₅來源搬運；01→04兩份幾何moves將933送至934／948、
941送至950，完整Σ、拒絕列及共同色框的診斷保持，不能當成固定mask shortcut。
933原01／13的幾何D₅搬運將Σ933送至940，原941部分身份搬至949；
所有mask／row／color／rootrole搬運均明列，不識別不同來源relations。
原rotation隨同一relabeling搬運並保持合法；完整Σ、row、共同色框、
owner角色與原分量一同搬運，不要求另行選出的canonical rotation相同。
mixed11的16份equal-pair self-identities已由[原D身份稽核](../audits/2026-10-04-task-d/REPORT.md#逐-identity-的完整性與搬運)
記錄此canonical face集差異，不能把合法搬運寫成canonical embedding字面相等。

**任務 B／B₂／B₃ 停止於 mixed-(2,2) 無 unary 的固定01／23短／長 face 分別全排。**
原 G 的每個拒絕 q-core 仍 (5,5)；B 的原20／20必要骨架證書保持歷史層。
B₂ 排 W933-101／W941-139短face{1,2}，B₃ 獨立排長face{0,4,3}，
各自七身份零殘留；因此僅這兩W的原mixed-capable faces已全部封閉。
長face的shared leaf bridge以全部拒絕列slack排除，degree二的shared
內部bridge鏈保持；nonowner 04／34、a0、b3、shared ab五leaf型的
原外部路徑完成K₅。完整C、actual附件、四接點fibres不作minor不變量。
其他骨架與faces、mixed22整型及ε≥3保留。
詳見 [B₃報告](c5_excess_two_mixed_core_four_spoke_mixed22_long_face.md)、
[B₂報告](c5_excess_two_mixed_core_four_spoke_mixed22_short_face.md)
及 [B原身份](c5_excess_two_mixed_core_four_spoke_mixed22.md)；A的入口如上。

**B₄停止於W933-129、原933 04／12長face的指定shared-contact附件{4}全排。**
此點確有deg_C=1，全部拒絕rows的11個合法pair均tight；原鄰點
leaf刪除slack只排13必要候選中的5份，保留8份另由原cut parity關閉。
K=C−v的外接恰為剩餘兩條root接線、原bridge及n_B框邊，完整degree四
迫n_B奇數且非零；{a},{b},{v},原B,整份K給十對原鄰接的K₅。
六shared身份的八指定選擇此附件支零殘留；D4與shared空附件、其他
contact附件／短face及其他骨架均不新增排除，W933-129整份骨架仍保留。
完整C／四接點relation、root-pair fibres、shared bridges及原(5,5)q-core
保持，minor不作其不變量。不沿用B₃的min-degree二分類，亦不證ε≥3。
在此窄支停止；下一具名候選入口是同份W933-129、04／12長face{2,3,4}，
指定shared頂點的實際框附件為空集；保留原frame、七身份及全部原bridges。
此入口未分析、未排除，其他contact附件亦保持。

其他 (2,2) incidence、較少 spokes、原 unary 單省略，以及原 G 自己是
(5,5) q-core 的分支仍保留；不能套唯一 degree-5 分離定理。
相鄰多 mixed 在刪 zw 全收後的原來源、no-mixed、非相鄰雙 roots
與 unary 側例外亦保留。**單 spoke 省略尚未整型排除，ε≥3 未證。**
指定列出口不提升為完整候選排除，不重開來源圖枚舉。

本線另保留一般 connectivity、可迭代充分 state 及共同安全 repair
的缺口。固定圖成功歷程不提供跨圖常數上界；一般單側／共同出口
與 K∞=K≤5 未證，接手點見 [weak-deletion 導覽](c5_weak_deletion_guide.md)。

## 4. 閱讀與重播入口

本批成果及D至D₅稽核的發布驗證見[發布紀錄](history/2026-10-04-c5-parallel-progress-publish.md)；
新checkout的凍結快照／完整輸出先依[封存還原說明](../audits/README.md)還原。
U2–U4與後續M4／M5交付證據的整批發布見[2026-10-08紀錄](history/2026-10-08-core44-batch-publish.md)。
三點弧的四份相連報告、固定證書及本輪重播見[2026-10-11整理發布紀錄](history/2026-10-11-three-point-arc-publish.md)。

U1的[M2獨立稽核](../audits/2026-10-07-m2-u1-audit/REPORT.md)已驗收指定前提化約與完整必要域，
上游分類／拓撲信任及來源正控制未觸發界線保留。
[M3 fresh驗證](../audits/2026-10-07-m3-fresh-checkout/REPORT.md)經
[監督補件](../audits/2026-10-07-merge-supervision/REPORT.md)驗收具名presence／文件hash例外；
原strict FAIL及歷史whitespace保持原紀錄，不推升數學或Lean結論。
最終文件版本的fresh provenance診斷及本地交付見
[M4-L報告](../audits/2026-10-07-m4-local/REPORT.md)與
[發布紀錄](history/2026-10-07-m4-local-delivery.md)；遠端驗收及可合併判定仍分開。

A₄／B₄已由[D₅固定快照與獨立稽核](../audits/2026-10-04-task-d5/REPORT.md)驗收：
A逐身份16／20及全部保留support／schedules不變；B只登記W933-129的
shared-{4}附件支，不刪骨架或長face。十二份producer兩seed byte-check、
獨立最終重播與完整scope／版本／runtime inputs見D₅包；D₄封存不改写。

正式返回A₃／B₃的固定快照與獨立驗收見[D₄整合稽核](../audits/2026-10-04-task-d4/REPORT.md)。
A₃的(a,b,u)投影等式與六角色joint不等反例分開保存；B₂＋B₃只登記
W933-101／W941-139兩primary骨架封閉，原20／20表與其他19／19原列保留。
前序[D₂](../audits/2026-10-04-task-d2/REPORT.md)的A／A₂、B／B₂覆蓋保持當輪截點，
原artifact、witnesses及所有hash／版本失敗不改寫。

任務 A 先讀 [原 unary／ternary 身份](c5_excess_two_mixed_core_four_spoke_mixed12.md)，
再讀 [A₂的01／12長／短face排除](c5_excess_two_mixed_core_four_spoke_mixed12_01_12.md)，
接續 [A₃的共用01／01原三hub排除](c5_excess_two_mixed_core_four_spoke_mixed12_01_01.md)
及 [A₃研究紀錄](history/2026-10-04-excess-two-four-spoke-mixed12-01-01.md)，
再讀[A₄的原04／04具名入口](c5_excess_two_mixed_core_four_spoke_mixed12_04_04.md)
與[A₄研究紀錄](history/2026-10-04-excess-two-four-spoke-mixed12-04-04.md)。最新重播：
`PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed12_04_04.py --check`。
其餘16／20完整具名殘留、原四rotations、完整support／schedules與六角色
joint controls保存在A₄ artifact；A／A₂／A₃原artifacts保持，mixed12整型仍保留。

任務 B 先讀 [原四接點身份與窄化約](c5_excess_two_mixed_core_four_spoke_mixed22.md)
及 [B 的獨立紀錄](history/2026-10-04-excess-two-four-spoke-mixed22.md)。重播：
`python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22.py --check`。
固定短 face 的接續讀 [B₂ 報告](c5_excess_two_mixed_core_four_spoke_mixed22_short_face.md)
及 [B₂ 紀錄](history/2026-10-04-excess-two-four-spoke-mixed22-short-face.md)，重播：
`python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22_short_face.py --check`。
同骨架長 face 讀 [B₃報告](c5_excess_two_mixed_core_four_spoke_mixed22_long_face.md)
與 [B₃紀錄](history/2026-10-04-excess-two-four-spoke-mixed22-long-face.md)，重播：
`python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22_long_face.py --check`。
原933 04／12的shared-{4}支讀 [B₄報告](c5_excess_two_mixed_core_four_spoke_mixed22_shared4.md)
與 [B₄紀錄](history/2026-10-04-excess-two-four-spoke-mixed22-shared4.md)，重播：
`python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22_shared4.py --check`。

前序已發布七輪的完成範圍、具名殘留、文件 hash 漂移及實際發布驗證見
[四-spoke 整理與發布紀錄](history/2026-10-03-excess-two-four-spoke-progress-publish.md)。
其後short_face、long_face、crosscut、short_arc、disjoint_pairs為另五輪
當時尚未提交成果；本批連同A／B／C及稽核封存一併發布，發布批次數不是成果總輪數。
原五輪與前置的[任務D只讀稽核](../audits/2026-10-04-task-d/REPORT.md)
保留44次check的40 PASS／4文件hash FAIL，以及兩份歷史完整payload相同的結果。
本次文件修訂、A／B新增身份／完整joint／witness覆蓋及新增hash漂移見
[D₂整合稽核](../audits/2026-10-04-task-d2/REPORT.md)與
[整理紀錄](history/2026-10-04-task-d2-integration-audit.md)。
前序九輪的完成範圍、整理發現、實際重播與貼用摘要見
[雙 root 進展整理與提交紀錄](history/2026-10-03-excess-two-dual-root-progress-commit.md)。
最新先讀 [mixed-(1,1) 子型完成](c5_excess_two_mixed_core_four_spoke_disjoint_pairs.md)
與 [本輪完成紀錄](history/2026-10-03-excess-two-four-spoke-disjoint-pairs.md)，
再讀 [共用短框弧原拒絕列延拓](c5_excess_two_mixed_core_four_spoke_short_arc.md)
與 [短框弧紀錄](history/2026-10-03-excess-two-four-spoke-short-arc.md)，
再讀 [原 unary crosscut 與 mixed hubs](c5_excess_two_mixed_core_four_spoke_crosscut.md)
與 [本輪紀錄](history/2026-10-03-excess-two-four-spoke-crosscut.md)，
再讀 [同一長 face 次序排除](c5_excess_two_mixed_core_four_spoke_long_face.md)
與 [本輪紀錄](history/2026-10-03-excess-two-four-spoke-long-face.md)，
再讀 [原 unary 短 face 排除](c5_excess_two_mixed_core_four_spoke_short_face.md)
與 [短 face 紀錄](history/2026-10-03-excess-two-four-spoke-short-face.md)，
再讀 [共用 pair 的 sealed mixed 排除](c5_excess_two_mixed_core_four_spoke_equal_pair.md)
與 [本輪研究紀錄](history/2026-10-03-excess-two-four-spoke-equal-pair.md)，
再讀 [原四接點 leaf-slack 排除](c5_excess_two_mixed_core_four_spoke_quaternary.md)，
再讀 [原三接點身份與整型排除](c5_excess_two_mixed_core_four_spoke_ternary.md)，
再讀 [同列端點 hub 整型排除](c5_excess_two_mixed_core_four_spoke_hubs.md)，
再讀 [原三-spoke star 扇區排除](c5_excess_two_mixed_core_four_spoke_star.md)，
再讀 [四-spoke binary 必要化約](c5_excess_two_mixed_core_four_spoke_binary.md)，
再讀 [四-spoke 六跨度排除](c5_excess_two_mixed_core_four_spoke_singles.md)，
再讀 [原 leaf 色纖維](c5_excess_two_mixed_core_leaf_fibers.md)，
再讀 [單 spoke 原附件化約](c5_excess_two_mixed_core_single_spoke.md)
與 [省略原 mixed](c5_excess_two_mixed_omission.md)；前置核心身份及
刪 root／zw 化約由 §3 報告表往回追。各輪詳細驗證保留在報告所連研究紀錄。

前序九份 checker 的歷史重播命令（本次只重跑 leaf；文件 hash 漂移另述）：

```bash
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_root_deletions.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_path_edge.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_triangle_edge.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_spokes.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_spoke_unary.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_two_unary.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_omission.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_single_spoke.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_leaf_fibers.py --check
```

原不相交pairs完成證書以
`PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_disjoint_pairs.py --check`
重播，保存32原骨架全部rotations、actual支援次序／外路徑與47／75完整identity ledger。
原短框弧證書以
`PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_short_arc.py --check`
重播，保存963完整C schemas、字面六角色witnesses與原拒絕列／Σ共同搬運。
原 crosscut 證書以
`PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_crosscut.py --check`
重播，保存 actual 原路徑、48 apex K₃,₃ subdivisions、同列 hub／degree
與完整 C 替換；四角色投影相等，六角色 joint 不相等控制分開。
同一長 face 證書以
`PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_long_face.py --check`
重播，保存原身份、5,120 actual support pairs、交錯原路徑與120
apex K₃,₃ subdivisions；完整六角色 joints 與固定五角色投影替換分開。
原 unary 短 face 證書以
`PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_short_face.py --check`
重播，保存完整具名框架、所有固定骨架 rotations、原短支援外路徑、
完整六角色接合及其他五角色投影的原 U witness 替換。共用 pair 證書以
`PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_equal_pair.py --check`
重播，保存完整原 C／U／V、六點 joints、空纖維、全部 unequal-pair
具名殘留；並唯讀重算既有三-hub payload 相同。原四接點 leaf-slack 證書以
`PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_quaternary.py --check`
重播，保存完整四點 relations、六點 joints 及原 spanning-tree 全圖 witnesses。
原三接點身份證書以
`PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_ternary.py --check`
重播，並精確重算既有(3,1)完整payload；其獨立checker為
`PYTHONHASHSEED=17 python3 scripts/c5_single_spoke_three_one.py --check`。
原單spoke歷史byte-check有三份既有docs hash漂移；前輪完整數學payload
已唯讀重算相同，本輪沿用該audit，詳見[原三接點身份紀錄](history/2026-10-03-excess-two-four-spoke-ternary.md)。
同列端點 hub 證書以
`PYTHONHASHSEED=17 python3 scripts/c5_excess_two_four_spoke_binary_hubs.py --check`
重播。原 star 證書以
`PYTHONHASHSEED=17 python3 scripts/c5_excess_two_four_spoke_binary_star.py --check`
重播，只需 Python 標準函式庫。四-spoke binary 證書另以
`PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_four_spoke_binary.py --check`
重播。兩 unary 的原 `c5_excess_two_mixed_core_four_spoke_singles.py --check`
因 leaf 文件的一份 hash 漂移而未通過；以
`PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_four_spoke_progress_audit.py --check`
完整重算數學 payload 及非文件 inputs，保存差異與原證書。
原 byte-check 狀態與實際沿用／重跑範圍見本次整理紀錄。

前序唯一 degree-6 分支依序讀 [t=0](c5_excess_two_no_spoke_complete.md)、
[t=3](c5_excess_two_three_spoke_complete.md)、
[t=2](c5_excess_two_two_spoke_complete.md)、
[t=1](c5_excess_two_single_spoke_complete.md) 的全分拆總報告，
再追各報告所連原省略證書、[短支援引理](c5_short_support_singleton.md)、
原首橋及末端區塊。共同下界見 [941 ε≥2](c5_941_three_spoke.md)，
minimality 前提見 [容量下界](c5_independent_support_capacity.md)。
前序實際發布範圍見 [唯一 degree-6](history/2026-10-03-excess-two-degree-six-publish.md)、
[t=2](history/2026-10-03-excess-two-two-spoke-publish.md)、
[t=1](history/2026-10-03-excess-progress-publish.md) 的紀錄；沿用證據不等於本輪重跑。

其他路線先讀 screen／座標與循環流的必要條件，再讀有序重接的一步
公式和反例；策略由 barriers 接到 repair interface。各報告列出
checker 與 artifact，使用原報告指定範圍，生成器會寫檔。
循環流驗證見 [2026-09-27 紀錄](history/2026-09-27-circulation.md)。
紙面推導、Python 固定域證書與個別 Lean 代數結果分開；未形式化平面來源排除。
