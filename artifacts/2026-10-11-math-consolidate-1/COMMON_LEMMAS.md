# MATH-CONSOLIDATE-1：最小共同引理與短證明組織

固定HEAD：`8c56b76922a1c7ac4c011096f2041b49c4a67cc8`。本文件提出共同接口名稱；不採納新定理、不弱化既有端點合同。
**12個局部接口記錄 + 1個外部GA導入**：C1–C7、LD／DP／PW／TERM／PB；GA另列。C4、C6含多個相連子命題，這不是12個unique新定理的計數。
PW／TERM是canonical已明確採納的局部引理；其餘新名稱表示已有證明步驟的重述或包裝。每個新來源的應用仍須另核所有前提。

## 共同語言

使用 [THEOREM_INVENTORY](THEOREM_INVENTORY.md) 的完整 C_S／C_U、HIGH H1–H13/K1–K13、K_LONG、BRC/SK；這些是來源合同，下面局部lemma不取代它們。
`A_Y(v)=N_B^Y(v)` 是**指定原圖Y**的全部原附件；`Col`為同一字面四色。`L_Y(γ;pins)`為全部原vertices上的完整assignments。C的contact relation只在保留全部preimages後投影。
通用ignored-point因子是 `J_γ=∏_{z∈Z}(Col−γ(A_Y(z)))`；真正無鄰居I_free才給Col自由因子。

## C1：完整 assignments 的 restriction／union

**最小已知充分接口。** 任意有限原圖Y，指定同一literal boundary γ、原vertex/edge inventory；以實際subgraphs/factors覆蓋全部原點／邊，交疊頂點保單一變數，因子含全部原內邊、actual B附件、原contact與root-spoke不等式。所有外部邊均已明列，沒有未納入的cross edge。無需disk、degree4、Σ、minimality或Gallai。

**完整命題。** 對每個proper literal γ及全部ambient tuples／pins，將每個完整Y assignment限制到各因子，是到同色shared坐標上的**完整因子assignment natural join**的雙射；其逆為compatible union。限制pin／tuple的每個fibre同樣雙射，包含空cells。逐邊合法性由它所在因子保證；原shared頂點只有一色，因此union唯一。Z因子不能省略，任何中途投影須保其完整preimages。

**原命題映射。** LOW1/LOW2-JOIN在同一r色接U/P/Q，兩U-contact同時限制同一f_U；HIGH1/2/3在同一s色接C/U且保r座標；SL-R-JOIN、SD-JOIN、SF-JOIN、TF-X是各自actual factorization；TF-FIBRES是同一雙射的ordered-tuple限制。TF-BLOCK的vertex/block recurrence按actual incidence tree重複用此restriction/union，不供非空性。
來源：[R10§1](../../docs/c5_degree5_interfaces.md)、[D proof review](../../audits/2026-10-11-n45-s-long-s-block-transfer-review/D-proof-review.md)、[D採納](../../audits/2026-10-11-n45-s-long-s-block-transfer-review/REPORT.md):8–20。

## C2：原一條 spoke 的完整 filter

**最小已知充分接口／完整命題。** 任意原G及原e=rb_i，X的全部vertices與G相同，edges恰E(G)−{e}；所有其他資料同一。∀proper literalγ、∀原root pins(a,b)：

`L_G(γ;a,b)=L_X(γ;a,b)` 若 `a≠γ(b_i)`，否則為空。

證明只核新增的原edge inequality，沒有degree／minimality／disk前提。未固定r時，式子是從全部X assignments中篩 `f(r)≠γ(b_i)`，不是先投影後判定。
它不證某個符合不等式的lift存在；`X`接受γ也可能全部r=γ(b_i)。

**映射。** LOW/HIGH的RESTORE、SL-R的全γ式、SD-JOIN J3、SF-RESTORE、TF-RESTORE全是C2；LONG-S的rb4只是i=4。U整份省略不是C2，不能共稱一條恢復邊。
來源：canonical:199–201,225–227,258–261,290–291,408–419；[D review](../../audits/2026-10-11-n45-s-long-s-block-transfer-review/REPORT.md):17–20。

## C3：connected degree-list slack

**最小已知充分接口／完整命題。** ∀有限非空connected simple C與lists L，若∀v `|L(v)|≥d_C(v)`且∃w strict，則C可L-coloring。以w為根的生成樹按距離由遠而近染；每個非根仍有未染parent，最後w多一色。singleton也包含。故不可染degree assignment逐點tight。

不需planarity／Gallai／minimality。對實際H_Y−s完整degree4分量，未固定s色的boundary lists在每個s-contact多一色，且有contact時給**unpinned**C assignments非空；不推全部root pins非空。完整外鄰與原degree式必須先核。
映射：所有CORE/F中的tightness或unpinned非空、q2 U strict-slack、incident-edge release。來源：[R10§2](../../docs/c5_degree5_interfaces.md):118–129；外部GA的Lemma7為同一已知slack結果。

## C4：incident-edge release、own-β minimal cover 與sole-C特化

**完整已知接口。** 原Y中s以外的有效內點完整degree4；C_i是H_Y−s的實際connected components，有非空ordered contacts P_i，外鄰只在原B與s，全部原edges／lists／assignments保留。∀proper literalγ、∀s pin a，若刪任何至少一端在C_i的原非框edge h，該區域對a可染。

若未刪時拒a，C3迫外部禁色互異及tight；h為外邊則新增一色，內部非bridge則degree少一，bridge則兩側各有slack。C3逐case解除。此全γ／全a的區域解除不需要Y minimal、disk或GA。

固定proper三色β，令`A=Col−β(N_B^Y(s))`，`R_i`為全部未固定s色的完整contact tuples，`F_i={a:每個t∈R_i至少一contact色為a}`。若Y**自己**同β拒絕且每條retained非框edge有Y−h同βfull witness，則s-spokeβ色互異，且

`⋃_i F_i=A`，`Private_i=F_i−⋃_{j≠i}F_j≠∅`。

反向等價須另保原spokesβ色互異、每個原區域的release前提與所有非框edges恰上述區域edges／s-spokes，見R10原iff；這些不省略。刪contact sp full witness在該contact色=s色a，其餘contacts避a；每edge見證選到的a不必相同。原Σ-critical G不供給Y的同βwitness。

**sole-C特化。** 只有一實際C時，C3給R_C非空，`F_C=A`；若s完整degree5、有t條β異色spokes，則 `|P|=5−t`、`|F_C|=4−t`。LOW1/2的兩spokes、U-LP/SS與LONG-R的0/1/2分流是同一數學接口；HIGH／LONG-S為兩分量，須保各自private及actual contact counts。
來源：[R10§3–4](../../docs/c5_degree5_interfaces.md):143–190、[PA](../../audits/2026-10-10-n45-pa/REPORT.md):105–131、[LONG-R](../../audits/2026-10-10-n45-s-long-r-map/REPORT.md):78–91。

## C5：sole-C 的(5)/(4)/(3)分流包裝

**完整量詞／充分接口。** ∀有限簡單induced-C5 disk Y、proper三色literalβ，Y自己同β edge-minimal拒絕；唯一完整degree5內點s，其餘有效內點完整4；H_Y−s為實際sole connected C；有t∈{0,1,2}條原retained s-spokes、β色互異，5−t個互異ordered contacts，完整attachments／rotation／assignments；ignored因子也保留。由C4得精確F_C。

一次共同D5/S4把β搬到BASE q，**不改C、contacts或edges**；t0引用[no-spoke§4](../../docs/c5_no_spoke_exterior.md)，t1引用[single-spoke(4)](../../docs/c5_single_spoke_four.md)，t2引用[two-spoke(3)](../../docs/c5_two_spoke_three_contacts.md)。各得到原Y矛盾。t2允許任意兩個β異色位置；原映射／reviews已核此較廣來源接口。

這是三個已知定理的dispatch wrapper，不是新uniform分類：t0的五葉奇偶允許K4、不借外hub；t1/t2仍需各原retained spoke及原tethers供K5鄰接。不存在以t0為0-spoke K5強行統一的短證明。

**映射。** U-LP：原盾中點無X內鄰→β=q_m，actual C={r}∪L∪S；U-SS：原盾長3兩內點先直接排，長2才同dispatch；LOW1/2：分別驗actual sole C／完整U與cycle，再t2；LONG-R：保owner=r、U/L/S全部原邊，再t0/1/2。原G完整Σ、witnesses、X=M自身minimal合同仍保留，helper不要求Σ(Y)=933/941。

## C6：同一block incidence matrix與palette差異

**最小已知充分接口。** ∀有限connected graph C及其完整非平凡maximal-block family，I是完整原vertex×block incidence matrix，則columns在R上獨立；leaf block的private vertex先定該column係數，再移leaf歸納。單點／空block族另處理。

若同一actual C上兩不可染degree assignments M_a/M_b的全vertex indicator差是`1_P(e_b−e_a)`，GA給原同一blocks上的palettes；I injective迫每block只有a/b互換或不變、其他色membership相同。三份以上pin lists且同一右側給共同係數τ；不能分別挑三張pairwise active trees。

**映射與不合併。** BASE3/LOW1/2及DIRECT三contact得到一triangle+三任意/零長原arms；BASE4/相關DIRECT四contact使用三份拒絕才得兩triangle+一bridge；BASE5/LONG-R t0用四份拒絕得偶葉矛盾。共同的是I獨立與差異式，active分類的前提／結論各不同；原tethers／inactive branch填色／bags仍分別引用。
來源：[BASE3§2](../../docs/c5_two_spoke_three_contacts.md):71–106、[BASE4§2](../../docs/c5_single_spoke_four.md):75–107、[BASE5§4](../../docs/c5_no_spoke_exterior.md):139–176。

## C7：support-compatible完整色搬運

∀同一actual piece P、全部原attachments與ordered/shared contacts，∀proper literalγ/γ′、色雙射π，若`γ′(b)=π(γ(b))`於每個actual support點且全部原pins共同搬運，則`f↦π∘f`在全部完整piece assignments／contact tuples／preimages／空fibres上為雙射。逐原edge與附件合法性互逆，無degree／disk／minimality／GA前提。

只在該piece support上的equivariance，不是把不同來源或不同β的容量相加。拼回整圖前所有pieces都必須已到**同一target literal frame**；π必須固定或共同搬運每個要接合的root pin。它不構造指定coloring的repair。
映射：PR-TRANSPORT／ESCAPE條件、HIGH1單contactsupport換色、HIGH2兩W的完整rooted assignments、q0 S/L transport、q2 β-local seed→q3/q4、TF-COLOR。來源：[PA§5](../../audits/2026-10-10-n45-pa/REPORT.md):180–184、[D proof](../../audits/2026-10-11-n45-s-long-s-block-transfer/transfer-proof.md)（TF-COLOR）、[q2 review](../../audits/2026-10-11-n45-s-long-s-t2-q2-restore-review/REPORT.md):10–29。

## BR共同接口：LD／GA／DP／PW／TERM／PB

下列保持已審的原M及原β量詞。source简称1a/1c/1e/1g分別是`audits/2026-10-11-br-sd-1a-0f181045/`、`...1c-fd6e1112/`、`...1e-337d018b/`、`...1g-dbdc4c35/`；fresh1g review在`...1g-adopt-6eae3597/`。完整可點來源見inventory模組C。

### LD：同一原 M 的 unused-D list／full-lift reduction

對每個有限簡單原 M、literal 四色 Col、原 B、s、connected C 和原內圖孤立點集 Z，若原點分割是 `B⊔{s}⊔C⊔Z`，Z 无任何原內鄰，C 原點全部完整 M-degree4，β 在 B proper且恰用三色、D 唯一未用色，以**全部原鄰居**定義

`A(y)=N_B^M(y), t(y)=1[sy∈E(M)], L^D(y)=Col−(β(A(y))∪({D} if t(y)=1 else ∅))`。

則 `4=d_C(y)+|A(y)|+t(y)`、`|L^D(y)|≥d_C(y)`，並在固定 β／s=D 上有**具名完整 assignments**雙射

`Col_(β,s=D)(M) ≅ Col_LD(C) × ∏_(z∈Z)(Col−β(A(z)))`。

限制與 union 互逆，逐類核 B–B、B–C、s–B、s–C、C–C、B–Z 邊；所有 W 原邊／原附件在 C 中全核。每個 Z factor 含 D，無鄰居孤點的 factor 才是 Col；保 Z 坐標後才是雙射，忘 Z 的 projection 通常不是雙射。任意完整 pin 查詢由限制此雙射得到，空 fibres 全保。M 拒絕 β 則左方空、Z 各 factor 非空，所以 C 不可 L^D-coloring。

來源：1a PROOF `23–42`；1c `56–77`；1e `130–159`；1g `75–95`；最精確獨立形式 1g-adopt `REVIEW.md:15–19`、`agents/proof/REVIEW.md:42–74`。實际推導 degree下界只需 `deg_M(y)≤4`，1a paper reviewer `REVIEW.md:57–61` 已明列；B 非 C5／β 使用≤3色亦可有未用色。但这些弱化**不改本輪 source domain**，不作一般 theorem adoption。

四份 theorem 均先用 LD。未使用 Σ／minimality／disk 幾何來證 LD；這些仍留 BRC。

### GA：外部 Gallai blockwise-uniform characterization

對每個有限簡單非空 connected C及 list assignment L，若 `∀y |L(y)|≥d_C(y)` 且 C 不可 L-coloring，则 C 為 Gallai tree，有每個 maximal block K 的同一 literal色框 palette P_K：odd cycle2色、clique Kn為n−1色（bridge K2為1），`L(y)=⋃_(K∋y)P_K`，兩不同 blocks 共原頂點⇒ palettes disjoint。單-block頂點 w 有 `L(w)=P_K`。不存在二連通／planarity／minimality／先驗 tightness 的額外前提；相交規則不能套到僅有一條 bridge 連接而不共點的兩個 cycles。

來源 [Dvořák author lecture](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf) p.5–6、Theorem10及其前定義；本輪讀 frozen全文 `audits/2026-10-11-br-sd-1a-0f181045/external/gallai.txt:170–221`，`external/SOURCE.md:3–19`，PDF SHA256 `50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea`。這是作者講義，非期刊論文、非 Lean theorem。四 theorem 全部只需 GA 的不可著色⇒刻畫方向。

### DP：shared blocks 的 private-common-colour contradiction

對有限 connected C 和 degree lists L，若 J1/J2 是兩個不同 maximal blocks、共有同一原點 r，且存在各自只屬其本 block 的原 w1/w2，使同一 literal 色 D 同時在 L(w1),L(w2)，則 C 可 L-coloring：若反設不可染，GA 使 `L(wi)=P_Ji`，同一 D 同時在兩相交 blocks palettes，違互斥。用它得到拒絕來源矛盾时，只需這些局部 premises及 GA；cycle長、odd性、J3、uv是來源上保證 witnesses 的工具，非 DP 本身 premises。

來源 1a PROOF `70–85`，paper reviewer `REVIEW.md:95–117`；1e PROOF `161–185`。這是抽取已審推論，不把抽象 list命題當 original-source實現。

映射：BR-A 的 SK 直接給 w1/w2（任意奇長及零臂）；BR-E 用 PW 給 w1/w2，再 LD+DP；BR-C 的部分接點也可用 DP，但最短全域證明不需分這些類。BR-G **不能**用 DP，因 J1 唯一 candidate 已成 cutpoint。

### PW：單接點旁支 private-witness preservation（已採 named helper）

**精確已採局部前提：** 同一具名 SK，保原 cycle／bridge邊；有限非空 off-skeleton 原 W連通，唯一骨架鄰點 x∈J3∪q-arm，无第二接點、cross edge、額外 s-contact、J1/J2新接線；原 p/q-only contacts全保。則每個 `w1∈J1−{r,a1}`、`w2∈J2−{r,u}` 仍各只屬本環 block，非C割點／非s-contact，原C-degree2；兩集合均非空（含 triangle）。

**證明：** 任意跨W與C0−x的二連通 block刪x即分離，故不存在；單接點不能繞過骨架 bridges或合併blocks。每環至少3點排最多2點，w_i存在；刪w_i後原環成含所有骨架接點的連通路，W仍在另一原點x接入，C−w_i連通。原contact排除和無新 incident邊給非s-contact／degree2。

来源 canonical `578–587`；1e PROOF `83–128`、final reviewer `37–49`。PW自身是graph結構statement；含D的list結論另需LD同β／degree条件。BR-E⇒PW⇒DP。BR-A的零W witness直接檢查，不偷偷以W=∅拓寬已採PW量詞。BR-G只保J2半份，不滿足PW完整前提。

### TERM：pair-supported odd-cycle／唯一s-contact bridge arm exclusion（已採 named helper）

對每個同一原M／literal proper三色β、D未用、connected C，逐點完整M-degree4、按全部原邊給degree lists且C不可染。若原奇環maximal block J的其他block接入至多v/a；有未佔用的私有非s-contact環點；q是這側唯一s-contact；J及原q-arm全部B附件在同一兩異色原框點；q-arm為從a到q的原simple bridge path，任意原邊長ℓ≥0，a外所有臂點（含q）无額外C邊，則該配置不可能。

用private點、degree4、simple圖及actual pair迫`P_J={T,D}`。ℓ=0時q=a的list禁D但incident P_J含D；ℓ=1時q list={T}迫首bridge palette={T}卻和J在a相交；ℓ≥2時緊鄰a的非q臂點z list={T,D}，首bridge非空palette subset此集合=P_J，仍違互斥。a=v、任意奇環長及任意其餘旁支大小全包含。不是一般cutpoint D傳遞。

來源 canonical `522–537`；1c PROOF `129–159`（直接分三案）、精確final review `13–34`。

映射：**BR-C全部degree合法x**保持J3/q，所以令J=J3,a=a3、q原q可一次套TERM；r接W先超度。BR-A也符合TERM完整局部前提，可作替代證明（其原已採route仍DP）；BR-E一般x和BR-G一般x2會破壞TERM，不能強行依賴。1g PROOF `67–73`精確區分 x2=v/a3時部分TERM適用，ordinary J3點／q／臂內點則失效。

### PB：J2 T/D barrier 的有限incidence-tree矛盾（已採1g proof step，未另命名採納）

在同一原C的GA palette representation中，T≠D固定。若`C−r=L⊔S`、包含r和S點的唯一block為J2且`P_J2={T,D}`，q∈S的list含T禁D，而`∀y∈S−{q}, {T,D}⊆L(y)`，則此representation不可能。所有maximal blocks須至少2點，完整all-vertex／block incidence graph為有限樹。這就是1g paper已完整證明的局部抽取，不含W2大小界。

**證明：** q incident-union給block K0含T禁D；exclusive意為在T/D中恰含一色，palette可另含A/B，**不是singleton**。exclusive block不可共J2原頂點，因此不含r、留S。block取異於入口的原點，該新點需另一色，因此完整incident-union給另一block；共點palette互斥使另一block恰含另一色。每步換頂點／換block，在有限incidence tree不回頭路不能重複，也不能再次到q。取從q起止於block的最長此路，末block仍有另一點，該點又迫新block，延長兩條incidence edges，矛盾。非割點／leaf／triangle／K4均已在這步處理，不需W2分類或無限選擇。

來源 canonical `662–674`；1g PROOF `109–147`；fresh review `REVIEW.md:22–30`及`agents/proof/REVIEW.md:99–148`。BR-G的J2 private w2＋原degree4＋simple圖＋actual S pair給P_J2={T,D}；p/q-only contacts及raw pair給其它完整lists，ownership／單接點骨架給唯一接口，然後PB矛盾。

**不得宣稱一般多旁支／較弱β或cross-interface源已採納。** 將PB另立generic theorem、套在新來源family或把P_J2={T,D}改為只含某色是後續新proof／scope review，這輪只是提出名稱及重述已審實例。


## 每個焦點原定理的較短組織

| 原採納端點 | 由共用lemma與不可省的原前提推出 |
| --- | --- |
| U-LP | 保原U/L/S盾與未接中點→原unattached-boundary lemma給β=q_m→C1/C3/C4給actual sole-C/F→C5三分 |
| U-SS | 保原U/L有序盾費(2,2)/(2,3)/(3,2)→兩未接點的單點T4改色直接排長3；長2→C1/C3/C4/C5 |
| LOW1 | 保unit U歸r／三contacts／兩s-spokes／原r retained spoke→C1/C4→C5 t2；G/X filter另用C2 |
| LOW2 | 先核雙U-contacts與原cycle、r在X無B邊且完整4→C1/C4→同一C5 t2；不重做BASE active triangle/tethers |
| HIGH1 | 保原G six bags九鄰接→原ARC給U三點T；C7的U capacity≤1換色＋E4 N-diagonal，以同一proper三色γ的原r=s=D完整接G，C1/C2→Q(G)⊆T與933/941矛盾。supporting完整MAP分類可引用另存 |
| HIGH2 | 保double-U contact、原O′ K33/ARC、原double-forbidden bridge與兩W rooted assignments/actual supports、原K5 one-edge結論→C7在共同γ搬運兩W，E4 diagonal＋C1/C2給proper三色G-lift→Q(G)⊆B−T。C4＋局部N-diagonal給禁色角色；BASE pair-bridge/source mapping另保原slit/crosscut前提 |
| HIGH3 | 保original C/U contacts(2,3)與retained避U外路→C1/C3/C4給U至少兩禁色→C6及BASE no-spoke(3,2)原X K5。C5是sole-C不能套本兩分量 |
| LONG-R | 原K_LONG+owner=r，actual sole C、原shield/star给t_s≤2→C1/C3/C4/C5；反證在X，C2不用於最後排除 |
| LONG-S | 原K_LONG+owner=s→C1/C3/C4、原DIRECT四profiles及FIBRE split22；T1原K5或原S二點及構造lift，q0保SF-QX歷史信任鏈，q2保β-role/局部seed+C7+U slack；各以C2恢復。D recurrence只共用C1，不供存在性 |
| BR-1a | BRC+SK無W→LD→GA；SK原雙private witnesses→DP |
| BR-1c | BRC+SK+一W只接J1/J2→原degree筛查→LD/GA；全部合法接點均保J3/q terminal前提→TERM。原PROOF§4/5兩條獨立機制改引用 |
| BR-1e | BRC+SK+一remote W接J3/q→原degree筛查+PW→LD/GA/DP；不調用TERM |
| BR-1g | BRC+SK指定J1triangle及兩Wi→原degree筛查／全部incident blocks保真→LD/GA；J2原private w2與actual S pair給{T,D}，完整S需求與sole interface→PB；不調用DP或TERM作全域步驟 |

前置排除與四個composition仍引用inventory既有原witness-shield／sameβ zero-slack／低incidence lemma及逐contract覆蓋；它們不從以上局部identities自動得到。

## 真相同、相似與待證推廣

**可安全精簡：** C1、C2、C3、C4的完整介面證明，C6 incidence-independent步驟，C7完整色雙射，BR的LD/GA以及1a/1e的DP是相同操作或同一已審特化；可用一次陳述＋逐支應用表。

**不可合併：** 原端點13支、U/S省略、LOW1/LOW2 incidence、HIGH三種contact分拆、LONG owners、BR四個W配置仍各有獨立前提。S04的singleton compatibility=Col²與U-S3的actual support≥2是不同結論；QX singleton、X接受、原G可恢復lift存在也不同。

**需要新證明／仍OPEN：** 多接點或跨骨架旁支保持witness、任意多W的exhaustive來源排除、失actual pair後的terminal或J2 barrier、一般Δ可恢復r-fibre非空、一般derivative minimality繼承、移除U的all-long分類。完整K_LONG下Δ本身非空已證；OPEN的是restorable fibre。沒有以finite 0trigger、新索引名字或新wrapper宣稱採納。
