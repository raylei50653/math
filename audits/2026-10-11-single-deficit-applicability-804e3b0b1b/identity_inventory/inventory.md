# 45/54 身份適用性盤點

本子盤點以 BASE `4dd11f422c6fa49265a412085116b088786d0344` 的已凍結 docs 為主；另讀的權威非 docs 檔為 `artifacts/c5_excess_two_e4/REPORT.md`、`audits/2026-10-09-n45-s/REPORT.md`、`audits/2026-10-10-n45-s-long-contract/REPORT.md`，已請父工作凍結。下文 file:line 指原路徑，其 docs bytes 位於本輪 `frozen/docs/`。未改權威輸入、舊證書或共享文件，未 commit／push／發布。所有 OPEN 目標均沒有本輪 actual source；因此只給條件適用性／unknown，沒有 source 排除的 finite trigger。

最重要的分界是：唯一 degree5 並不意味二連通。任何完整保留的 unary U，其 owner root 都是具名割點，因為刪該 root 使 U 與另一 root／mixed 部分分離。反之沒有 unary 只排除 root 割點，還沒有排除 mixed 裡的內部割點。二連通不能從 Σ-critical、β-minimal、H−s 連通或「兩 mixed」名稱推出。

本輪若引用單缺額定理／LIT-SD-A，均以 A 已通過及定理完整前提為條件。直接可見的效益是無U兩long、無U long/singleton-short及相鄰兩mixed的二連通45/54 subset條件排除，與無U long/edge-pair-short的原block-chain收窄；本盤點没有證成任一 OPEN source 身份全部不存在。

## 共同記號與真正 core 的 degree 檢核

G 的全圖 degree、X 的 degree、M 的 degree 是三份計算。原拒絕三色列為同一 literal β；`H_M=M[V_int,eff]` 忽略孤立自由內點，但完整 lifts 保留其自由因子。`t_v^M=|N_B^M(v)|`、`d_H(v)=|N_{H_M}(v)|`、`deg_M(v)=t_v^M+d_H(v)`。

β-minimal 自己給每個有效內點 `deg_M≥4`、H_M 連通，且同一內點在 β 下的 retained boundary 附件色互異。這些只來自 M 自己的逐邊 witnesses，不來自 G 的 Σ-critical。於是 β 的未用色 D 在全部 lists，`Lβ(v)=Col−β(N_B^M(v))` 且 `|Lβ(v)|=4−t_v^M`；真正45/54 M 若只有 s degree5、其他點degree4，則 `|Lβ(v)|=d_H(v)`（v≠s），`|Lβ(s)|=d_H(s)−1`。來源：`docs/c5_weak_list_cores.md:18–35`。

原 degree4 piece 的全取／全不取只能由「M 自己 deg≥4」與原 degree4 飽和共同推出：保留一點就保留全部 incident 原邊，再沿 piece 傳播。它保留 complete attachments、ordered/shared contacts、ownership、rotation、bridges 和 full lifts，不能換成 coloring star。來源：`docs/c5_excess_two_root_deletions.md:41–66`。

若只删原 spoke `e=rb_i` 且 **X=M**：從 E(M)=E(G)−{e} 逐邊得到 `deg_M(r)=4,deg_M(s)=5`，其他有效點degree4；H_M=H_G。若省略完整原 unit U、唯一原 contact rx 且 **X=M**：從 E(M) 保留邊得到 r 恰失 rx、s不失邊、其他保留 piece 點不失邊，仍是同一profile；H_M=H_G−V(U)。兩個結論都不能延伸到只删 contact 的 derivative，或 X≠M 的 derivative。

## 優先 OPEN N2 身份

| 原身份 | G／X／真正 M | M 的 degree profile 與內度 | H_M 連通／二連通證據 | 定理前提與可縮減範圍 | 缺橋接／既有覆蓋 |
| --- | --- | --- | --- | --- | --- |
| N45-S-NOU-LS：原 unary=0、一 long L、一 short S | G 為 N45 §1 的 ordered C5 disk、完整 Σ933/941、Σ-critical、rs∉E、原 roots5/5、其他4；H_G−{r,s}=L⊔S。只删原 e=rb_i，X=G−e=M 自身 β-minimal | retained 原邊給 (r,s)=(4,5)，其餘4；`d_H(s)=m_s=5−t_s`，`m_s≥2`，每個 mixed 至少一 contact。original r `m_r=5−t_r≥2,t_r≥1` | H_M 由 M β-minimal 連通；H_M−s={r}∪L∪S、H_M−r={s}∪L∪S各連通，因此 r/s 均不是割點；mixed內的具名割點尚無 actual source，unknown。沒有二連通證書 | A＋二連通给`d_H(s)=2,t_s=3`、L/S各恰一原s-contact；C block-path给各piece r-contact≤2。因此 singleton S 总inc≤3，被既有S04排除；只餘真框邊pair S。r splits为(1,1)/(1,2)/(2,1)/(2,2)，原r-spokes3/2/2/1，X retains2/1/1/0 | 二連通source證據缺；pair subset可映R11/12/14/22/24以已採來源排除涵蓋0/1/2oddblocks；三oddblocks直接共用點鏈末端各一接點可映R27。橋接其餘block-chain與原restoration仍缺。不能搬U盾弧/private cover |
| N45-S-NOU-LL：原 unary=0、兩 long P/Q | G 同前，H_G−{r,s}=P⊔Q，兩份 support 各不包含於框邊；X=G−rb_i=M 自身 β-minimal | 同上，但原三-spoke-star重新逐前提给 **t_s≤2,d_H(s)≥3** | r/s不是割點，內部割點未知；無actual source二連通unknown | **A＋二連通時矛盾，整個此二連通subset條件排除**：SD给d_H(s)=2，原star/shield给d_H(s)≥3 | 两long原one-sided各付≥2盾邊；H_G−s連通與原fullBtouch使三spoke若有就迫兩σ都在long3弧，4≤3矛盾。這是重新核原P/Q前提，未借U的2+2+2。非二連通subset仍OPEN |
| N45-other derivative/core：未滿 X=M 或原 pieces全保留 | G 可以仍為原N2，但 X 的删邊／删點身份須個別給出；真正 M 是 X 中取的 β-minimal core，可能 M⊊X | 根名／G degrees不給 M profile；須M原邊與完整 incidence計算。若發現 M45/54才進上述翻譯，否则unknown | M β-minimal才給H_M連通；二連通与s身份unknown；無actual source不得填割點 | 不能以X的ε=1、Σ-minimalize結果替代M45/54或β-minimality。SD適用unknown | 先補實際M、邊集、逐邊βwitness；本頁§1不含此身份，保持OPEN |

權威定位：`docs/c5_excess_two_nonadjacent_unit_core45.md:71–90,410–422`；`artifacts/c5_excess_two_e4/REPORT.md:274–290,338–351`。short／long 的定義是原 support 是否包含於一條框邊（E4:274），不是 cycle 長度。

對前兩列，定理導出的兩個 s-neighbors 必是**原** ordered contacts `p∈L,q∈S`（或 `p∈P,q∈Q`），而且 p≠q，因為兩份原分量互斥。`H_M−s={r}∪L∪S` 是同一 retained graph，所有 r-contact、框附件及旁支仍在。若 H_M 真二連通，C 的 block-cut tree 不能有避開 p/q 的終端 block：該 block 的 cutpoint 會成為 H_M 的割點；因此得到以 p/q 為兩端的 block-path 必要結構。這是內部圖論必要條件，沒有給十列 Σ、指定 root pair 非空、完整 assignments／full lifts保持，更沒有把 long 的原 support 改小。

無U兩long的原star收窄不依賴A：原`H_G−s={r}∪P∪Q`連通，若s有三原spokes，整塊及全部實際框附件只能落於一star面。原fullBtouch迫兩個非spoke框點在同一面，所以三spokes的gaps=1,1,3。每份原P/Q的one-sided由另一mixed實際連r/s給出；其非框部分在long3面，另外兩個小面可經原s-star接s∈H−piece，因此那些框邊在F_piece邊界，兩σ都包含於long3弧。long支援的定義與原盾弧引理給各σ≥2且互斥，得到4≤3矛盾。每步只用同一原G、原rotation／attachments。來源：`docs/c5_unary_shield_budget.md:54–70,101–110`；對照已採原star模板 `audits/2026-10-09-n45-s/REPORT.md:183–191`、`audits/2026-10-10-n45-s-long-contract/REPORT.md:94–103`，新應用以P/Q的兩long費替換原U/L費。

LS的singleton條件排除也沒有把Col²當作full lifts：原S one-sided、完整degree4、兩側inc正，s-contact=1且r-contact≤2使總≤3，既有S04給S完整compatibility=Col²；於同β刪整S不改root-pair可延拓性，所以M−S仍拒β，違反M minimality。其所有assignments、relations、空fibres仍須保留，Col²只是已採整S compatibility的精確投影。定位：`docs/c5_excess_two_nonadjacent_unit_core45.md:102,107`。

## 其他明確45/54身份

| 原身份 | G／X／真正M及degree核算 | 二連通證據／具名割點與s內度 | 條件適用與縮減 | 既有覆蓋與缺口 |
| --- | --- | --- | --- | --- |
| N1-45-S：非相鄰sole mixed C，一側單spoke省略 | E4 §6 45/54身份，保完整 C及所有未省略side factors；r降度，X=G−rb_i=M β-minimal（須以 actual source 核 X=M）；保邊給r4/s5/others4 | retained unary的owner root是割點；若無 retained unary，r/s不是割點，C內部割點未知；`d_H(s)=m_s+u_s=5−t_s` | A＋二連通必沒有retained unary，`d_H(s)=m_s=2,t_s=3`；C有兩原s-contacts | 包含N1 mixed22且無44core的殘留，不得以U3完成44排掉；source unknown。須保原C root fibres与attachments |
| N1-45-U：非相鄰sole mixed C，整側unit unary省略 | 唯一rx屬被省略完整U；X=G−V(U)=M，r恰失一原 incidence；保邊给r4/s5/others4 | 剩餘unary owner root為割點；若無retained unary，r/s不是割點，C內部未知；`d_H(s)=5−t_s` | 同上；二連通subset縮至原s三spokes、C兩原s-contacts | N45整U排除只關N2；不能套N1。N1明确OPEN，無actual source |
| AD1-45-S：相鄰rs、sole mixed C，單spoke省略 | docs已證若 X=G−rb_i拒β，则真正minimal core K=X=M，而不是從G遺傳；保rs/C、保邊給r4/s5/others4 | retained unary owner root為割點；无retained unary時`d_H(s)=1+m_s`，內部割點仍未知 | A＋二連通給`m_s=1,t_s=3`。r原有被删spoke故t_r≥1；原總spokes≤4給t_r=1，原spoke分拆(1,3)、mixed incidence(3,1) | 此二連通subset已经落在既有四spoke(3,1)整型排除／root swap，沒有新涵蓋；一般單spoke殘留仍OPEN |
| AD1-45-U：相鄰rs、sole mixed C，完整unit unary-at-r省略 | 原身份表：X=G−V(U)=M，r失unique rx；保rs/C及所有其他原factors，r4/s5/others4 | retained unary仍令owner root割點；無retained unary時`d_H(s)=1+m_s`，二連通unknown | A＋二連通給原s三spokes、m_s=1。原省略U incidence1，r有`1(rs)+1(U)+m_r+t_r=5`，故`m_r=3−t_r`；原總spokes≤4令t_r=0/1 | t_r=1為原(1,3)、mixed(2,1)+r-unitU，既有(3,1)ternary排除；t_r=0是總三spoke、mixed(3,1)+r-unitU，這次僅條件收窄，不宣稱排除 |
| AD1-M12-b-spoke：四spokes(2,2)、mixed在(a,b)為(1,2)、unitU只接a；删b-spoke | 指定 `X=G−bb_i=M`；真正唯一degree5 s=a，r=b degree4，其他4。原ab、C、U全留 | **具名割點 a=s**；`H_M−a=(C+b)⊔U`，实际 `d_H(a)=3`（ab、a–C、a–U），无二連通 | SD二連通前提不觸發；d_H=3不反駁SD。一般unique-deficit不推出2connected | 此明確殘留見A原paper:93–95；已排部分original frames不重開。其a-spoke／整U省略另已全收。尤其`G−au`把u降3，不能叫actual core |
| AD2-45-unit：相鄰rs、兩原mixed，一側unit省略 | docs明列45/54仍保留；β-core保r/s/rs；單侧spoke或unit unary只能失一incidence，两mixed保留。actual X=M仍須逐source核；若如此profile為r4/s5/others4 | retained unary owner root為割點；无retained unary，二連通unknown。unique degree5 s至少rs＋每份mixed一contact，故 **d_H(s)≥3** | **A＋實際H_M二連通時整個AD2-45 subset條件排除**，因直接与SD `d_H(s)=2`矛盾；此处不需染色replacement或lift transfer | U2只排44，不含45；這是未證來源二連通的條件增益。一般AD2残留仍OPEN，缺split/biconnectivity橋接 |
| AD0-45-unit：相鄰no-mixed，保两roots，單侧unit省略 | profile须实际M核；保rs（否则两独立sides一侧已阻礙，可省另一root）；原unary只能整份省略；若M45/54则r4/s5/others4 | **rs是原内部bridge**。s有至多三β异色spokes且deg_M(s)=5，故d_H(s)≥2、s侧至少一retained unary；**s是具名割點**，删s分離r與其unary | 二連通SD不觸發；不能偷删bridge再套定理 | U1只排44；45/54明列OPEN。保same-source bridge及两side full lifts；不扩一般no-mixed |

定位：N1：`artifacts/c5_excess_two_e4/REPORT.md:224–230,338–351`。AD1：`docs/c5_excess_two_mixed_core_spokes.md:35–86`、`docs/c5_excess_two_mixed_core_single_spoke.md:31–62`。原總spokes≤4與(3,1)既有覆蓋：`docs/c5_kempe_guide.md:200–205`。AD1-M12：`docs/c5_excess_two_mixed_core_four_spoke_mixed12.md:60–95`。AD2：`docs/c5_excess_two_adjacent_two_mixed_core44.md:18–38`。AD0：`docs/c5_excess_two_no_mixed_core44.md:18–33`；「bridge／s割點」是保same-source無mixed及M自己β-minimality的圖論推論，不是舊44分類的移植。

## 已採納限定排除：僅比較

| comparison身份 | 真正M與profile | H_M及s內度 | SD效益／既有覆蓋 |
| --- | --- | --- | --- |
| N45-U-LP／SS | X=G−V(U)=M β-minimal；r4/s5/others4；完整L/S留 | H_M−s={r}∪L∪S sole C；在其契約β=q_m下t_s≤2，所以d_H(s)≥3；二連通unknown | 已全排此精確整U身份。若二連通SD可给同一条件矛盾，但沒有新增覆盖，不重開 |
| N45-S-SHORT-LOW1／LOW2 | X=G−rb_i=M；U/P/Q全留，r4/s5/others4 | **r割點**（U owner r），LOW `t_s=2,d_H(s)=3`；H_M−s sole C不證二連通 | LOW1/2全排；SD二連通前提不觸發 |
| N45-S-SHORT-HIGH1／2／3 | X=G−rb_i=M；U/P/Q全留，r4/s5/others4 | **s割點**（U owner s）；`H_M−s=C⊔U`；d_H(s)=3/4/5，对应t_s=2/1/0 | HIGH限定各完整契約已排；SD不觸發 |
| N45-S-LONG-R | X=G−rb_i=M；U/L/S全留，r4/s5/others4 | **r割點**；H_M−s sole C；t_s≤2、d_H(s)≥3 | K1–K12 U@r限定已排；SD不觸發 |
| N45-S-LONG-S | X=G−rb_i=M；U/L/S全留，r4/s5/others4 | **s割點**；H_M−s=C⊔U；六profiles t_s=0/1/2，即d_H(s)=5/4/3 | K1–K12 U@s限定已排；SD不觸發 |

定位：`docs/c5_excess_two_nonadjacent_unit_core45.md:135–175,179–221,238–277,304–311,337–361,367–371,389–406`。comparison的沒有actual source不使割點推論變unknown：它們是完整契約的條件圖論結論；但沒有actual named source圖及finite trigger，不能把它們說成新replay反例。

## 55 障礙及舊R系列邊界

原兩roots在M仍degree5時，degree4飽和迫M=G；M自己的β-minimality仍須另給。若β-minimal，则r/s各有一個list deficit：`|Lβ(r)|=d_H(r)−1`、`|Lβ(s)|=d_H(s)−1`。這是**兩個缺額**，單缺額定理不能使用。只記障礙，不扩55证明。來源：`docs/c5_excess_two_root_deletions.md:68–78`。

`docs/c5_degree5_guide.md:16–31,36–49` 的 R31／三環等是 generic唯一degree5的 source block分類，不是具名45/54原省略身份。只有先證同一實際45/54 M滿足全部R前提，才可作既有覆蓋的conditional comparison；不能把「兩long mixed」當作「兩odd-cycle blocks」。舊四列介面也不是完整Σ或全16pins：guide:39–46。

對無U LS二連通subset，可逐前提映回既有R系列的實際圖是 **M**（不是原G，也不是任意normalized piece）：M繼承disk/T4且自身β-minimal；s唯一degree5，三原s-spokes在β看三色；C=M−s恰sole connected component，two contacts p/q互異，每個C頂點在M完整degree4。删各spoke的M full β witnesses使C对該原spoke色可填；β拒絕唯一s可用D，使 **F_C(β)={D}** 精確成立。R11一次共同D5/S4搬運M所有原vertices/edges/rotation/attachments及β，使其落于兩mirror長區域；不能逐piece獨立搬運。

| C的實際內部結構 | 已有覆蓋及精確前提 | 本輪可用／不可推出 |
| --- | --- | --- |
| 含K4 block | R12 `docs/c5_degree5_tree_components.md:20–24,32–53`：s有原boundary spoke使B∪{s}連通，private-color與全degree4給原K5 | 条件M图排除K4；不是把K4 contraction當染色replacement |
| 0 odd-cycle blocks（tree，允許任意bridges） | 同R12:22–28,59–96；兩actual contacts、F_C={D}、same-source disk/T4/βminimal | 任意大小已排，不需新來源控制 |
| 恰1 odd-cycle block＋其餘bridges | R14 `docs/c5_degree5_odd_cycle_components.md:17–25,30–54` | 所有原兩接點位置、arms／旁支已排 |
| 恰2 odd-cycle blocks＋其餘bridges | R22 `docs/c5_degree5_two_long_cycles.md:14–21` 的互斥型＋R24 `docs/c5_degree5_shared_cycle_minors.md:12–19` 的共用點型 | 任意環長與arms已排；這是M的block count，與long pieces數無關 |
| 恰3 oddcycles依次共用cutpoints的chain，two contacts在兩終端環的私有點／各自外臂 | R27 `docs/c5_degree5_three_cycle_minors.md:11–17,65–84` | H_M二連通block-path迫兩contacts分跨terminal ends，故此指定shared-chain型已排；R27不声称fullΣ／任意pins保持 |
| R30兩contacts同在中環；R31同在一終端環 | R30 `docs/c5_degree5_middle_cycle_minors.md:9–18`；R31 `docs/c5_degree5_same_terminal_triangles.md:16–36` | 存在避p/q的原終端cycle，它在连接cutpoint处分離s，故H_M不是二連通；不是本二連通residual。R31未完成任意長source minor也不影響此判別 |
| 恰3 oddcycles但至少一對由非零bridge path分開，或≥4 oddcycles沿p/q block-path | 上列R27僅shared cutpoints，沒有完整覆蓋這些bridge-separated／更多環型 | **真正二連通LS-pair remaining block-chain；unknown actual source**。保原contacts／attachments、原r身份及full fibres，不能從內部Gallai／R26有限模板宣稱來源排除 |

原r在C是具名割點，因C−r=L⊔S；H_M二連通时r只属于block-path上相鄰的兩個blocks。K4-free的Gallai block每一側在r貢獻1（bridge）或2（oddcycle），所以r局部貢獻(1,1)/(1,2)/(2,1)/(2,2)。`d_C(r)=5−t_r`，原r-spokes=3/2/2/1，且每份L/S的r contacts≤2。這是same-source retained邊的必要身份，不是完整colour relation replacement。

## 最小後續義務的庫存提示

優先 no-U LS 的必要內度縮減已清楚，但缺的第一件事不是再列全pins，而是**是否能在同一 actual M上證二連通或完整處理內部割點**。最窄可發布義務可只選 `N45-S-NOU-LS` 內部 cutpoint 分支：證任意割點 a 必給至少一份可在原字面β和原attachments下可删／可接回的分支，與M β-minimality矛盾；若失敗，保存具名原edge graph、完整β-critical witnesses和十列fibres，停止於確切割點身份。這不能預設A，成功只建立二連通橋接；A未通過时再引用SD仍conditional。

另一個極小的條件性義務是AD2的二連通source橋接：因其d_H(s)≥3与SD已直接衝突，無需先做block replacement。但這偏離使用者優先no-U LS，宜只列為次候選。

本子盤點未新增literal控制；finite狀態只有 **not triggered**（未提供／執行actual目标source）。沒有零觸發推成來源排除，沒有marginals／独立正規化piece或內部Gallai冒充完整Σ／lifts保持。
