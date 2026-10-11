# N45：非相鄰 N2 原 unit 省略的 45／54 身份

更新：2026-10-11（完整 U／long／short 契約的 U 在 s 分支採納）；
原研究 BASE `dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`，本輪驗收 BASE
`f2692089ad4259808e27d9b7e882ac09505b180a`。
本頁是已採納 N45 結論與目前 residual 的權威入口；完整新論證分別見
[S 原交付](../audits/2026-10-09-n45-s/REPORT.md)與
[U 原交付](../audits/2026-10-09-n45-u/REPORT.md)。
[SU-A](../audits/2026-10-09-n45-su-a/REPORT.md)獨立核十四項 paper claim，
[SU-J](../audits/2026-10-09-n45-su-j/REPORT.md)核指定有限介面；
[監督採納](../audits/2026-10-09-n45-su-supervision/REPORT.md)對回封存版本及依賴。
第二批 [PG](../audits/2026-10-09-n45-pg/REPORT.md)、
[PR](../audits/2026-10-09-n45-pr/REPORT.md)、[PC](../audits/2026-10-09-n45-pc/REPORT.md)
經 [PGA 幾何稽核](../audits/2026-10-10-n45-pga/REPORT.md)、
[PA 紙面稽核](../audits/2026-10-10-n45-pa/REPORT.md)、
[PCA 工具稽核](../audits/2026-10-10-n45-pca/REPORT.md)與
[本輪監督採納](../audits/2026-10-10-n45-p-supervision/REPORT.md)，完成限定範圍驗收。
後續 singleton-support 交付 [SS](../audits/2026-10-10-n45-u-ss/REPORT.md)
經 [SSA 紙面與覆蓋稽核](../audits/2026-10-10-n45-ssa/REPORT.md)、
[SSG 幾何／改色](../audits/2026-10-10-n45-ssg/REPORT.md)、
[SSC 封存稽核](../audits/2026-10-10-n45-ssc/REPORT.md)及
[SS 監督採納](../audits/2026-10-10-n45-ss-supervision/REPORT.md)，完成限定採納。
後續 [LOW1](../audits/2026-10-10-n45-s-low1/REPORT.md)經
[L1A 紙面](../audits/2026-10-10-n45-l1a/REPORT.md)、
[L1R 原圖與完整關係](../audits/2026-10-10-n45-l1r/REPORT.md)、
[L1C 封存](../audits/2026-10-10-n45-l1c/REPORT.md)及
[LOW1 監督採納](../audits/2026-10-10-n45-low1-supervision/REPORT.md)，完成限定採納。
後續 [LOW2](../audits/2026-10-10-n45-s-low2/REPORT.md)經
[L2A 紙面與覆蓋](../audits/2026-10-10-n45-l2a/REPORT.md)、
[L2R 原圖與完整關係](../audits/2026-10-10-n45-l2r/REPORT.md)、
[L2C 封存](../audits/2026-10-10-n45-l2c/REPORT.md)及
[LOW2 監督採納](../audits/2026-10-10-n45-low2-supervision/REPORT.md)，完成限定採納與 LOW 覆蓋核對。
後續 [HIGH1](../audits/2026-10-10-n45-s-high1/REPORT.md)經
[H1A 紙面](../audits/2026-10-10-n45-h1a/REPORT.md)、
[H1R 原圖與完整關係](../audits/2026-10-10-n45-h1r/REPORT.md)、
[H1C 封存](../audits/2026-10-10-n45-h1c/REPORT.md)及
[HIGH1 監督採納](../audits/2026-10-10-n45-high1-supervision/REPORT.md)，完成完整 H1–H13 內的限定採納。
後續 [HIGH2](../audits/2026-10-10-n45-s-high2/REPORT.md)經
[H2A 紙面／覆蓋](../audits/2026-10-10-n45-h2a/REPORT.md)、
[H2R 原圖／完整 lifts](../audits/2026-10-10-n45-h2r/REPORT.md)、
[H2C 工具／封存](../audits/2026-10-10-n45-h2c/REPORT.md)及
[HIGH2／HIGH3 監督驗收](../audits/2026-10-10-n45-high23-supervision/REPORT.md)，
在完整契約內採納；未用色接回構造明限 proper 三色列，原過寬量詞保留 finding。
[H3A](../audits/2026-10-10-n45-h3a/REPORT.md)、
[H3R](../audits/2026-10-10-n45-h3r/REPORT.md)、
[H3G](../audits/2026-10-10-n45-h3g/REPORT.md)獨立核回完整 HIGH3 契約到 BASE no-spoke 排除，
由同輪監督採納；兩支與既有 HIGH1／LOW 合成的精確覆蓋見§2.8。

**已證的窄排除：** 指定原 spoke 省略身份不能有兩份原 unary；指定整份原
unit unary 省略身份不能有兩份原 unary，也不能讓兩份原 mixed 都 short。
**N45-U-LP 已排除：** 唯一原 U＋long L＋真框邊 pair 支援的 short S，整 U 省略為45／54 core。
**N45-U-SS 已排除：** 唯一原 U＋long L＋singleton-support S、總 incidence≥4 的整 U 省略身份。
與既有 U 化約及 LP 合成，**§1 精確 N45-U 整 U 省略身份已全排**；完整覆蓋見§2.2。
**N45-S-LOW1 已排除：** 原 U incidence=1 在降度側 r，僅省略原 r-spoke，U／兩 short 完整保留。
**N45-S-LOW2 已排除：** 原 U incidence=2 在 r、兩原 contacts 全留，僅省略唯一原 r-spoke。
LOW1／LOW2 窮盡 **§1 精確 S 身份的 S-SHORT-U-LOW**，該限定身份已全排；覆蓋見§2.4。
**N45-S-HIGH1 已排除：** 原 U incidence=1在 s、原 s兩 spokes全留，僅省略原 r一條 spoke；
完整 H1–H13、X=M及 U/P/Q全留，十項 claims已獨立採納，見§2.5。
**N45-S-HIGH2／HIGH3 已排除：** 原 U 在 s 的 incidence／s-spokes 為(2,1)／(3,0)，
各自完整契約與 X=M 保留；HIGH2 未用色構造限定三色列，HIGH3 接回 BASE no-spoke (3,2)。
HIGH1–HIGH3 窮盡限定 HIGH；與 LOW 合成，**§1 精確 S 身份的兩 short 分支已全排**。
**N45-S-LONG-R 已排除：** 完整U在降度側r、long L／short S全留、只刪原r-spoke，
且X=M自身minimal的選定身份；pair／singleton都涵蓋，完整映射見§2.9。
**N45-S-LONG-S 已限定排除：** 完整K1–K12內，原U在s、long L／short S全留、
只刪原r-spoke且X=M自身同β minimal的選定身份；六profiles、pair／singleton全覆蓋，見§2.10。
採納保留原SF-QX／BASE紙面與finite-terminal信任鏈；有限零觸發不承擔排除。
無U的long／兩long、其他45／54身份、原55、無45／54來源、一般 N2／E及ε≥3均仍 OPEN。

## 1. 全部共同前提與原身份

G 是任意大小的有限簡單 disk 圖，外面為有序 induced C5
B=(b0,…,b4)。完整有序 Σ(G)=933／941，或共同搬運整圖的 D5 像；
每條非框邊 Σ-critical。ε(G)=2；有效 H 忽略孤立內點，恰兩個原 degree5
roots r,s，rs 不存在，其餘原內點完整 degree4；有效 H 連通。H−{r,s} 的完整分量恰有
兩份 mixed P,Q，其餘為 unary。沿用 E3 的 full B-touch、one-sided 與原 support 非空。

對原拒絕列 β，M 為 inclusion-minimal core，自身 root degrees 為45／54。
共同 root 交換後 r 是降度側。本頁只含兩種精確身份：

- S：原 spoke e=rb_i 被省略，X=G−e=M。
- U：整份完整原 unary U 被省略，其唯一原 root-contact 是 rx，X=G−V(U)=M。

unit 指原 root incidence=1，並不表示每列禁色必非空。X 的 β-minimality
另給自身 Σ-critical；一般 derivative 要先保完整 Σ minimalize，不能自原 G 遺傳。
兩份原 mixed 與其餘原因子完整保留；不允許刪一段 U 或換成 coloring star。

所有具名 ordered contacts、shared contact 的單一坐標、actual attachments／support、
ownership、原 bridges、rotation、共同字面 β、完整 relations／fibres（含空 fibres）
及 full lifts 保留。原 G、X 與刪 contact 的圖各有自己的 vertices／edges／lifts。
拓撲 minor 不作染色 replacement；不同列的原幾何費可相加，禁色容量不可跨列相加。

canonical q positions 的 cells indices 是 q0=6、q1=4、q2=3、q3=1、q4=0，
T4={2,5,7,8,9}。941 拒絕 q0,q1,q3；933 另拒絕 q2。

## 2. 已採納結論與必要化約

| CLAIM | 已採納的精確結果 | 界線 |
| --- | --- | --- |
| N45-S-01／N45-U-CROSS | ε(X)=1；保完整 Σ minimalize 後用 E2，Q(X) 只能為 Q(G) 內的空集、單點或相鄰 pair；含 core β 的七格必要表保留933 q2 | 必要 masks 不給 disk 實現；X=M 才另有 β-critical⇒Σ-critical |
| N45-S-02／N45-U-CAP | 共同拒絕 β、每個 b∈E_s 的 degree4 側完整 joint 有 D+O+δ+o+λ=0；五項各零，mixed raw columns 滿額、互斥、聯集恰 E_r^X | 要完整 tuples 及 E_s 非空；不從 marginals 或其他列補容量 |
| N45-S-03 | 恢復 spoke 色 c：c∉E_r^X 時唯一 retained side blocker 給 O=1；c∈E_r^X 時每欄唯一 mixed owner 給 λ=1 | owner 可隨欄變；unary blocker 不滿足重色 spoke 的 E4-D 前提 |
| N45-S-04 | 原 singleton mixed support、兩側 incidence 正且總≤3 時，固定 support 色的 S3 軌道與 N-diagonal 迫完整 compatibility 為 Col² | 不排總 incidence≥4；不獨立正規化 pieces |
| N45-S-05 | 指定 S 身份的原 u=2 子型不存在；兩 short 時總 mixed incidence≤5 且兩份原 support 都是真 edge-pair | 含 long 用2+2+2；兩 short 用1+1+2+2，省略原 piece 仍付原費；spoke 不收 piece 費 |
| N45-S-06 | S 身份兩 short 時恰一份原 unary，unary 側／無 unary 側 mixed incidence 為2／3；原輪只留 LOW／HIGH 必要身份 | 原三 spoke star 的唯一長3面論證；不搬 U4 retained44／O11 下界；限定 LOW／HIGH 分別由 LOW1–LOW2／HIGH1–HIGH3 覆蓋排除；只關§1精確 S 的兩 short 分支 |
| N45-U-REL | 原 U 的 contact palette T_U 非空；T_U 單點才 F_U 單點，否則 F_U=∅；整 U 省略與刪唯一 contact 的 root-pair 集合相等 | 在新接受 γ∈Σ(X)∖Σ(G)，全部 X lifts 的 r 投影與 T_U 同 singleton；core 拒絕 β 不迫 F_U 非空 |
| N45-U-WIT | 每份原 piece 由自己的 critical contact 給拒絕接回的 outside witness；原 unary 有避自身外路，省略 U 仍收原盾弧≥2 | 不要求不同 pieces 用同一列，但原圖與幾何不變 |
| N45-U-S3 | 原 one-sided mixed、完整 degree4、full B-touch、原 critical-contact witness、兩側正 incidence 且總≤3，則 actual support 至少二點 | Gallai/K4 tethers／末端計數／triangle K5 bags，另有 N-empty＋N-diagonal＋S3 交叉證明；總≥4未涵蓋 |
| N45-U-U2 | 指定整 U 省略身份的原 u=2 子型不存在 | 原 U 仍收費；有 long 先排，兩 short 再由低 incidence 支援下界收1+1+2+2 |
| N45-U-SHORT | 指定整 U 省略身份不能有兩份 short mixed | 排兩 unary 後 X 無 unary，共同未用色 D 與兩份原 short 的完整 diagonal lifts 接回 X，違反 β 拒絕 |
| N45-U-RES | 整 U 省略化約為唯一原 U、一 long L、一 short S；pair／singleton 支援由 LP／SS 分別排除 | 化約、LP、SS 的完整前提逐項保留，合成只關本頁 U 身份 |
| N45-PG-01／03／RES | 原2+2+1有十個 whole-frame named partitions；L/S 原 r–s 路給 Jordan cycle與非 bridge contacts；八種 spoke sets／56正 incidence profiles | 八張 embedding與56 profiles只作抽象控制／必要身份，沒有有限正常形或來源實現 |
| N45-PG-02 | 共同框 U012／L234／S40 下，三組原 K₃,₃ bags 迫 N_B(r)⊆{b0,b2}、N_B(s)⊆{b4} | 保每條原附件／contact；minor只證非平面 |
| N45-PG-04／05 | core β 的各 raw column 非空迫 s-contact 附件色不在 E_s；排掉 edge-pair 支援、整份 S 單頂點子型 | 頂點數一與 singleton support 分開；逐欄前提不可略 |
| N45-PR-TRANSPORT／ENDPOINT／SATURATION／ESCAPE／FORCING | 全 lifts 的 support-compatible 色雙射、原 hub endpoint 接回、滿額 contact 色集、接受列 escape、singleton 投影的逐欄一單位身份 | 各自充分前提見 PA §5；ENDPOINT 必須是完整原 piece、全部內鄰為指定 owner roots且完整 degree4；不給指定 coloring repair或來源實現 |
| N45-PR-UNTOP／LP-EXCLUSION | 原 U 盾中點未接 X 內部，迫 β=q_m；X−s 為唯一原 degree4 分量，接回既有單-root (5)/(4)/(3) 排除 | 任意大小 paper＋明列 BASE／外部 Gallai；只關 N45-U-LP，沒有新 Lean |
| N45-SS-COST／UNTOP／U3／U2 | 原 U/L 盾費只容(2,2)、(2,3)、(3,2)；長3的兩內點迫Σ(X)=Ω，長2迫β=q_m | singleton S不收pair費；長3 support可有四點，沒有套LP三點前提 |
| N45-SS-X-CORE／COMPONENT／SPOKES／T0／T1／T2／EXCLUSION | X自己minimal、完整degrees及實際sole C；原spokes／精確F_C接回三份BASE排除，N45-U-SS全排 | SSA十一項paper成立；SSG四項幾何／改色另核；SSC只核完整性，SS source count未計算 |
| N45-U scoped composition | 已採納U-U2／SHORT／S3／RES、LP與SS窮盡§1精確整U省略身份，該身份不存在 | 不是一般U省略、spoke省略、原55或全部N2／E；SSA§8獨立核覆蓋 |
| LOW1-CORE／COMP／JOIN／F／MAP／EXCLUSION | X=G−rb_i=M 自己 minimal；U 全留，X−s 恰 sole C，三原 contacts、二異色 s-spokes與精確 F 接回 BASE 原 K₅ 排除 | 完整 LOW1 契約、原 U incidence1；L1A／L1R 各核六 claim，外部 Gallai 明列；LOW2／HIGH／long 未涵蓋 |
| LOW2-CORE／COMP／JOIN／F／MAP／EXCLUSION | 原 U 的兩 r-contacts 與 cycle 全留；X=G−rb_i=M 自己 minimal，r 無框邊，sole C 的完整 join／精確 F 接回 BASE 原 K₅ 排除 | 完整 LOW2 十二項契約；L2A／L2R 各核六 claim；BASE／外部 Gallai 明列，工具 PASS 不證 paper |
| S-SHORT-U-LOW scoped composition | §1 精確 S 身份中，LOW 的原 U incidence／r-spokes 只有(1,2)、(2,1)，各由完整 LOW1／LOW2 排除 | L2A §7 獨立核逐項契約與窮盡；不關 HIGH、long、其他 core 或全部 S／N2／E |
| HIGH1-CORE／COMP／JOIN／RESTORE／F／MAP | X自己的45／54身份；實際C與U的(2,1)完整接合、全部r色fibres與原e恢復條件；BASE (2,1)的排除／指定X延拓分清 | 全部H1–H13；X指定延拓不提升為G；H1A／H1R各核十claim，工具不裁paper |
| HIGH1-K33／ARC／REJECT／EXCLUSION | 原G的六bags九鄰接迫P/Q支援邊頂點互斥；原U盾弧長2、support連續三點；同列未用D的完整G lifts迫Q(G)⊆該三點，矛盾完整933／941 | 任意大小paper＋明列BASE／Gallai信任；只關U incidence1在s且s兩spokes的HIGH1，無新有限來源或Lean |
| HIGH2-CORE／COMP／JOIN／RESTORE／F／K33／ARC／MAP／BRIDGE／SPLIT／PALETTE | 原雙 U-contact／single s-spoke；完整(2,2)接合保 r fibres，原 O′ 補 K₃,₃、完整 W 支援及 rooted assignments 成立 | 全部 H1–H13；H2A／H2R 紙面核對，H2C 只核工具，原錯量詞另列 finding |
| HIGH2-EXCLUSION（精化） | 每 proper 三色 γ 在原 U 三點 T 見三色時，原 r=s=Dγ 的完整 G lifts 含恢復 e；Q(G)⊆B−T，故至多兩拒點 | 只縮窄接回構造的 γ 量詞；JOIN／RESTORE／PALETTE 仍保全部 proper γ；不改原 worker |
| HIGH3 scoped exclusion | X自己 minimal、s無spoke、實際 C/U contacts=(2,3)，完整覆蓋迫三接點 U 至少兩禁色；原 X K₅ 排除 | 完整 K1–K13；H3A／H3R／H3G 獨立核 BASE no-spoke §§1–3、5，無新充分前提 |
| S-SHORT scoped composition | §1精確 S 的 LOW兩支與 HIGH三支互斥窮盡，各自完整契約排除，故兩原 mixed 都 short 的身份不存在 | H2A及父端核覆蓋；含long、其他core身份、一般N2／E均未關 |


U-CAP 恢復原 U 的一單位：F_U=∅ 時是 D；singleton 在 E_r^X 外時是 O；
singleton 在 E_r^X 內時是 λ。這三分在同一 β／欄核算，不能借別列的 singleton forcing。

### 2.1 N45-U-LP 的任意大小排除與信任界

在§1全部共同前提下，另有唯一原 U、L long、S 支援恰真框邊兩端。
原盾弧 (U,L,S)=(2,2,1) 分割五邊；U/L actual support 各為連續三點。
原盾弧 restriction 使 U 中點 m 在 X=G−V(U) 無內鄰。X 繼承全部 T4；
在同一完整 lift 中只改回 m，故 X 唯一可能拒絕 q_m，Q(X)={m}；933 q2照留。

X 自己 β-minimal，r 恰失 rx 成 degree4，s 仍 degree5。
C=H_X−s={r}∪L∪S 是實際唯一連通分量，每點在 X 完整 degree4；全部原 edges／
contacts／shared identity／附件／rotation／full lifts 保留。β=q_m 使 s 的異色 spokes
至多兩條。t_s=0、1、2分別接回 BASE
[no-spoke (5) §4](c5_no_spoke_exterior.md)、
[single-spoke (4)](c5_single_spoke_four.md)、
[two-spoke (3)](c5_two_spoke_three_contacts.md) 的任意大小排除。
t_s=0不要求 C 外的 s–B 路；t_s=2涵蓋任意兩條 β 異色 spokes。三分全矛盾。

完整前提映射、外部 Dvořák Lemma7／Theorem10 的凍結原文及獨立裁決見
[PA §2–5](../audits/2026-10-10-n45-pa/REPORT.md)。沿用具名 BASE 紙面分類與外部定理的信任界，
有限 masks／0觸發沒有承擔此排除。singleton-support S 的後續獨立裁決見§2.2；其他core身份另保留。

### 2.2 N45-U-SS 與指定整 U 身份的完整覆蓋

SS另有唯一原U、L long、S actual support恰一框點且總原incidence≥4。
保§1所有共同前提、X=M、unique原rx及同源完整資料。原U-WIT與原面盾弧限制給
有序U/L盾費(2,2)、(2,3)、(3,2)，H−U不碰U盾弧的全部內點。
整U省略後，長3的兩個不同內點都無X內鄰；對每個三色列選非singleton的一點，
以同一完整T4 lift只改回該點，得Σ(X)=Ω，矛盾拒β。沒有同時改兩點。
長2唯一內點m則迫原β=q_m、Q(X)={m}；933 q2及整圖D5／S4／root swap保留。

X自己的β-minimality、完整degree4/5及實際
C=H_X−s={r}∪L∪S，給全部原邊上的完整relation／空fibres／full lifts接合。
s的原spokes色互異且避m，t_s=0/1/2；5−t_s個互異contacts及精確
F_C=Col−β(N_B(s))，逐項滿足§2.1的BASE三分。t0不借外部s–B路，t2容任意異色位置。
完整新前提映射與十一裁決見[SSA§2–7](../audits/2026-10-10-n45-ssa/REPORT.md)。
沿明列BASE papers與外部Dvořák Lemma7／Theorem10；沒有新Lean、SS finite source或trigger數。

**限定合成覆蓋。** §1的U身份有省略的原U，原unary至多兩份；U-U2排兩份，故唯一U。
兩mixed的short／long互斥且窮盡：U-SHORT排兩short，原2+2+2盾費排兩long，故long＋short。
short支援非空，只有真框邊pair或singleton；pair由U-RES逐项滿足已採納LP全部前提，
singleton由U-S3排總incidence≤3，餘≥4恰滿本SS契約。兩支皆排，沒有未覆蓋子支。
此合成由[SSA§8](../audits/2026-10-10-n45-ssa/REPORT.md)獨立驗收，只排
**X=G−V(U)=M、原unique rx、保原兩mixed及§1全部前提**的N45-U身份。
不含非unit／部分U省略、不等於M的derivative或其他core。

### 2.3 N45-S-LOW1：保留完整 U 的任意大小排除

在§1全部共同前提下，另有唯一原 unary U 歸 r、唯一原 contact rx，
P/Q 皆 short、actual support 各恰真框邊兩端，(m_r,m_s)=(2,3)，原兩 roots 各兩 spokes。
僅刪原 e=rb_i，X=G−e=M 自己是指定原拒絕 literal β 的 inclusion-minimal45／54 core；
原 U/P/Q、其內邊、contacts、附件與其他 spokes 全部保留。

H_X=H_G；r 降為完整 degree4，s 保持 degree5，其他有效原內點完整 degree4。
C=H_X−s 恰 {r}∪U∪P∪Q 的唯一連通分量，s 的三個原 contacts 互異且繼承原 rotation。
同一 r 色坐標接合 U/P/Q 全部 assignments，與 C 全部 lifts 互為 restriction／union 雙射；
shared contact 始終是單一坐標。R_C 是非空 fibre 的支援；fibres仍對全部 Col³ 定義，支援外為空。
所有十列與 pins照留，G 在一般 literal γ 的 lifts 比 X 僅多 r≠γ(b_i) 這條原 spoke 條件。

X 自己的 β-minimality 迫兩條 s-spokes 異色 u,v；逐刪 spoke 的完整 witnesses 給
F_C(β)=Col−{u,v}，strict-slack 給 R_C(β) 非空。兩補色 pin 的完整 degree-lists迫 tight，
外部 Gallai block palettes及同一 C 的 incidence columns獨立，給一個 active triangle與三條可零長原 arms。
原 complete degree4及 inactive branch填色反證給三條實際 boundary tethers；
Z={s}、三份 triangle點＋arms、O=整個 B＋tether內點給原 X 的 K₅ bags，十對鄰接皆有保留原邊。
[BASE 三接點 §1–5](c5_two_spoke_three_contacts.md)允許任意兩個 β 異色 spoke 位置；
不要求 β 是 U 盾中點列，也不刪 U。933 q2、共同整圖 D₅／S₄／root swap一併保留。

完整六項契約與論證見 [LOW1](../audits/2026-10-10-n45-s-low1/REPORT.md)，
[L1A](../audits/2026-10-10-n45-l1a/REPORT.md)與 [L1R](../audits/2026-10-10-n45-l1r/REPORT.md)各自獨立核回。
採納是任意大小 paper＋BASE＋外部 Dvořák Lemma7／Theorem10；封存 PASS 不證紙面。
沒有新 LOW1 finite source、目標 trigger 數、source realization或 Lean；只關上述 LOW1。

### 2.4 N45-S-LOW2 與指定 LOW 身份的完整覆蓋

在§1全部共同前提下，另有唯一原 U 只接 r，原 contacts 恰 rx1、rx2，x1≠x2；
P/Q 各支援真原框邊兩端，(m_r,m_s)=(2,3)，r 對 P/Q 各一 contact，s 分配1與2。
原 r 恰有唯一 spoke e=rb_i；原 s 三 mixed contacts＋兩 spokes全留。
只有 e 省略，X=G−e=M 自己是原拒絕 literal β 的 inclusion-minimal45／54 core；U/P/Q 全留。

r 在 X／C 完整 degree4且無框或 s 鄰；其他 piece 點完整 degree4，s degree5。
C=H_X−s={r}∪U∪P∪Q 恰唯一實際分量。U 兩原 contacts、x1–x2路與 r 形成的原 cycle 全留。
同一 r 色 c 同時施加兩 U-contact 不等式於同一完整 f_U，並接合 P/Q；
restriction／union 與 C 全部 assignments逐項雙射。全十列、全部 pins、ambient 空／非空 fibres、
shared 頂點單坐標及 full lifts保留；G 在一般 literal γ 比 X 僅多 r≠γ(b_i)。

X 自己的 β-minimality 迫 s 兩 spokes β異色 u,v；逐刪 spoke 的 full witnesses給
F_C(β)=Col−{u,v}，contact strict-slack另給 R_C非空。兩補色 pin 在同一 C 上的 degree-lists
接回 BASE 三接點 §§1–5及外部 Gallai；block palettes／column independence給 active triangle與三原 arms。
r 沒有框邊仍滿足 inactive branch的 strict-slack反證：沒有 B／s約束的整支可染並共同換色接回。
因此所需 tethers 在實際 X 真碰 B；不使用省略 rb_i。原五 bags 的十對鄰接給 K₅，與 disk平面性矛盾。
任意長／零長 arms、933 q2及共同整圖 D₅／S₄／root swap均保留，β不須是 U盾中點。

完整十二項契約及六 claims見[LOW2](../audits/2026-10-10-n45-s-low2/REPORT.md)，
[L2A](../audits/2026-10-10-n45-l2a/REPORT.md)與[L2R](../audits/2026-10-10-n45-l2r/REPORT.md)各自獨立核回。
這是任意大小 paper＋明列 BASE／外部 Dvořák Lemma7／Theorem10，沒有新 LOW2有限來源或 Lean。

**限定合成覆蓋。** 只取§1精確 S身份及已採納 S06 的 S-SHORT-U-LOW：唯一原 U在 r，
兩原 mixed真框邊 pair支援、(m_r,m_s)=(2,3)。令 u為原 U incidence，t為原 r-spokes；
完整原 degree5給 2+u+t=5，U接 r給 u≥1，省略原 spoke存在給 t≥1。
故(u,t)只有(1,2)、(2,1)，s原三 mixed contacts另給 t_s=2。
兩支分別逐項滿足已採納 LOW1與本 LOW2的全部契約，互斥且窮盡。
[L2A §7](../audits/2026-10-10-n45-l2a/REPORT.md)獨立核覆蓋，
[監督接受紀錄](../audits/2026-10-10-n45-low2-supervision/acceptance.json)另列此合成 scope。
因此只排 **§1精確 S-SHORT-U-LOW**；HIGH、long、其他 cores／原55及一般 N2／E未關。

### 2.5 N45-S-HIGH1：原 K₃,₃ 與同列完整 G lifts

只取§1精確S身份：原U只接s、唯一原sx且無U–r；P/Q各actual support恰真原框邊兩端，
(m_r,m_s)=(3,2)，s對P/Q各一，r分配1與2。原r/s各兩spokes，僅省略e=rb_i，
X保rb_j及全部s-spokes；U/P/Q整份全留。X=G−e=M自己的β-minimality另列，
有效H連通／full B-touch、原degree4/5、Σ-critical／ε2、所有具名ordered資料、空fibres與full lifts
及共同整圖D5／S4／root swap均保留。全部十三項前提逐字見
[HIGH1 H1–H13](../audits/2026-10-10-n45-s-high1/REPORT.md)。

H_X−s恰C={r}∪P∪Q與U，原s contacts分配(2,1)。接合C完整雙tuple及r色fibres、
U單contact fibre、同一s色與全部isolated free factors，restriction／union逐項雙射；
恢復G僅另加r≠γ(b_i)，不能先丟r投影。X自己的minimality與degree-list slack給精確private cover；
BASE局部N-diagonal限制F_C={β(b_j)}、F_U={未用D}。BASE (2,1)指定列延拓仍只屬X。

若P/Q兩個不同支援邊共端v，在**原G**取左bags P,Q,O=B−{v}，右bags {r},{s},{v}。
三左bags連通且六bags互斥；P/Q各有兩root原contacts與真v附件，O–v有原框邊，
r/s各兩個不同spokes確保O–r／O–s各有原邊，合九鄰接成K₃,₃。O–r可用被省略e，
因這一步在原G；故兩支援邊頂點互斥。原sx的critical witness與避U外路接回BASE unary盾下界，
再用原盾弧連續／邊互斥迫U恰佔唯一剩餘長2框弧，actual support恰其連續三點T。

對任一proper三色literal γ，若T沒有看到全部三個已用色，取已用而未在U support出現的h，
以完整U assignments的(D,h)換色雙射及單contact禁色容量≤1，得到U存在避D的完整lift。
同一γ令**原r=s=D**，BASE E4§4.1提供P/Q完整同色N-diagonal lifts，全部原spokes含e均合法，
union即為原G完整coloring。故原拒絕q_k必有k∈T；完整933的四拒點不能落於T，
941的三個非連續拒點也不能等於T，共同整圖D5像照留，933 q2未漏。

[H1A](../audits/2026-10-10-n45-h1a/REPORT.md)與[H1R](../audits/2026-10-10-n45-h1r/REPORT.md)
各獨立核十claims，無新增前提或gap；[監督接受紀錄](../audits/2026-10-10-n45-high1-supervision/acceptance.json)
逐字保全部H1–H13。這是任意大小paper，沿用BASE原盾／N-diagonal／(2,1)論證及
[外部Dvořák Gallai Lemma7／Theorem10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)信任界；
封存與有限toy只核語義／算術，未建立或執行HIGH1 finite source，沒有trigger數或新Lean。


### 2.6 N45-S-HIGH2：原雙 contact 與恢復 e 的 G lifts

只取§1精確 S 身份，另有原 U 只接 s 的兩個相異 contacts、無 U–r；
P/Q 支援真框邊、(m_r,m_s)=(3,2)。原 r 兩 spokes 只刪 e=rb_i 留 rb_j，
s 唯一 spoke sb_k 全留；U/P/Q 全原邊、原 cycle 及全部 assignments 保留。
X=G−e=M 自己是 β inclusion-minimal45／54 core。完整 H1–H13逐字見
[HIGH2 原交付](../audits/2026-10-10-n45-s-high2/REPORT.md)。

H_X−s恰C={r}∪P∪Q及U、contacts(2,2)。全部 proper literal γ、ambient tuples、
r/s pins及空 fibres 的完整 restriction／union保留原 r 投影；G 只再加 r≠γ(b_i)。
X自己的 minimality／incident-edge witnesses與局部 N-diagonal迫C/U禁色角色(1,2)。
原 U-critical-contact witness先證盾長≥2；P/Q共端且等於唯一s-spoke端點時，
原 O′=(B−v)∪U的六 bags 九鄰接補齊 K₃,₃，故兩支援邊頂點互斥。
原 U support因而恰連續三點 T，C碰 T 外原框點；這些均在原 G／X 各自原邊中核對。

同一 U 的雙拒 palettes給奇數原 bridge 路徑，每個完整旁支塊 W 必見兩供應色。
任意兩 W 的 frame-arc原五 bags／十鄰接及鴿籠原理迫該路徑恰一原邊，
兩完整 W 的 actual supports為 T 左右真框邊；W大小仍無上界。
β完整交換pair關係先證兩 W 的完整 rooted assignments可取色恰其支援pair補集；
再用實際附件的色等變，在同一 γ 框保全部 W assignments及原 bridge接合。

**採納的量詞精化。** JOIN／RESTORE／PALETTE仍對全部 proper γ成立；
未用色接回構造只對 **proper 三色 γ**：若 T看到其三個已用色，取兩 W 的完整
assignments並置原 r=s=Dγ，P/Q的完整 N-diagonal lifts接回原 G，包含恢復 e。
所以 singleton三色拒點 Q(G)⊆B−T、至多兩點，矛盾完整933四拒點／941三拒點。
原文§8及H2-EXCLUSION將此構造寫成所有 proper γ，四色列可能在 T見三色卻無未用Dγ；
兩 paper稽核及父端保此 finding與四色literal witness。四色列的接受原由H2的T4前提保證。
原worker及其封存不改，不採納過寬接回量詞；主排除範圍仍是完整 H1–H13。

[H2A](../audits/2026-10-10-n45-h2a/REPORT.md)與[H2R](../audits/2026-10-10-n45-h2r/REPORT.md)
獨立裁紙面／原圖及全部 fibres；[H2C](../audits/2026-10-10-n45-h2c/REPORT.md)只裁封存與有限工具。
這是任意大小 paper＋BASE＋明列外部 Gallai，沒有 finite HIGH2 source、trigger數或新Lean。

### 2.7 N45-S-HIGH3：原 X 的 no-spoke (3,2) 排除

只取§1精確 S 身份，原 U在s恰三個相異contacts且無U–r，s無spoke；
P/Q真框邊支援、(m_r,m_s)=(3,2)，r兩spokes只刪e留rb_j、X=M自己minimal。
全部原件與具名ordered/shared資料、十列完整 relations、空fibres及孤立自由因子保留；
[完整K1–K13](../audits/2026-10-10-n45-h3a/frozen/authority/common-contract.md)限制本輪採納範圍。

X的唯一完整degree5點是s，其餘有效原內點degree4；H_X−s實際分量恰C={r}∪P∪Q與U，
ordered contacts數(2,3)。完整同列接合、X自己的minimality及slack給F_C∪F_U=Col、
各private非空、|F_C|≤2，從而|F_U|≥2；不預設指定禁色角色。
原拒絕三色β以一次共同整圖D5／S4搬到q，逐前提接回BASE no-spoke §§1–3、5的(3,2)來源排除。
避整U的s–P–r–rb_j原路恢復外hub；U的K4-free、active triangle、任意／零長arms及原tethers
給五個互斥連通bags及十原鄰接，Z–O用另一分量的原s-contact；全部在X、不用省略e。
這是原X非平面反證，不是X指定延拓提升成G，也不是必要表項的來源實現。

[H3A](../audits/2026-10-10-n45-h3a/REPORT.md)、[H3R](../audits/2026-10-10-n45-h3r/REPORT.md)、
[H3G](../audits/2026-10-10-n45-h3g/REPORT.md)各自獨立核回，父端另核原圖／全lifts及封存。
任意大小結論依賴BASE及外部Gallai；抽象toy／bags只校準語義，無有限HIGH3來源或新Lean。

### 2.8 限定 HIGH 與兩 short S 身份的完整覆蓋

在§1精確S身份的两原mixed都short時，已採納S05／S06迫唯一原U、兩mixed真框邊支援，
unary側／另一側mixed incidence=2／3。LOW已由§2.4的兩支窮盡排除。
HIGH令u為原U在s的contact數、t_s為原s-spokes，完整degree5给2+u+t_s=5，
u≥1、t_s≥0，故(u,t_s)恰(1,2)、(2,1)、(3,0)。原r三mixed+兩spokes中只省略e。
這三支逐項滿足HIGH1／HIGH2／HIGH3的各自完整契約、X自己β-minimal性及所有同源資料。
它們互斥窮盡，不另加入充分前提，也不從G遺傳X minimality。

[H2A覆蓋稽核](../audits/2026-10-10-n45-h2a/REPORT.md)與
[父端接受紀錄](../audits/2026-10-10-n45-high23-supervision/acceptance.json)核回三支及LOW／HIGH合成。
故只關 **§1精確S身份的兩原mixed都short分支**；含long、其他省略／core身份、原55、
無45／54來源、一般N2／E及ε≥3仍OPEN，沒有新增有限來源或Lean。

### 2.9 N45-S-LONG-R：保留完整 U／long／short 的 sole C 排除

在[含long同源契約K1–K12](../audits/2026-10-10-n45-s-long-contract/REPORT.md)全部前提內，
另有原U owner=r。[SL-MAP-R完整報告](../audits/2026-10-10-n45-s-long-r-map/REPORT.md)
核 actual C=X−s={r}∪U∪L∪S，全部有效C點完整degree4、s唯一degree5；
原盾弧／star必要式給t_s≤2。完整unpinned-s C assignments保全部r色／空fibres，
X自己同β minimal witnesses給精確F_C=Col−β(N_B(s))，不要求Σ(X)=933／941。
整圖一次D5／S4搬運所有邊／contacts／rotation／full lifts，t_s=0/1/2各接回
BASE sole-C五／四／三接點排除：t0用active forest奇偶，不借外hub；
t1/t2用retained s-spoke及原boundary tethers給X的K₅。反證在X內，毋須先恢復e。
三份只讀分工及父端核全部前提，涵蓋pair／singleton S與U incidence1/2。
這只關 **完整U owner=r、一long L、一short S、只刪原r-spoke、X=M自身minimal**。
紙面依既有BASE／外部Gallai；26省略的260列／4160根pins及250880 ambient r fibres
只校準完整介面，拒絕來源not triggered；無新Lean或來源實現。
U owner=s的後續限定排除見§2.10；無U的long／兩long及其他core／一般N2／E仍OPEN。

### 2.10 N45-S-LONG-S：完整 C/U 與原 r-fibre 恢復的限定覆蓋

只取[含long同源契約K1–K12](../audits/2026-10-10-n45-s-long-contract/REPORT.md)
的全部前提，另有原U owner=s。G任意有限大小、ordered induced-C5 disk，完整Σ=933／941
或整圖共同D5像，非框邊Σ-critical；有效H連通、ε=2、非相鄰原degree5 r/s，
其餘有效原內點完整degree4。H−{r,s}的實際分量恰為完整原U／long L／short S；
原one-sided、full B-touch、S真框邊pair或singleton、自由孤立內點的完整因子均保留。
只刪原e=rb_i，X=G−e=M自己是同一原拒絕literal β的inclusion-minimal(4,5) core。
保G各非框邊的Σ witnesses與X各retained非框邊的同β witnesses，不能從G遺傳X minimality。
每份原ordered/shared contact、actual attachment、ownership、rotation、bridge、旁支、
十literal列／全16pins／diagonal／空fibres／全部tuples、preimages及full lifts均保留。

由原degree5身份m_s+n_U+t_s=5、m_s≥2、n_U≥1，恰有六profiles。
[DIRECT／FIBRE獨立採納及更正](../audits/2026-10-11-n45-s-long-s-review/REPORT.md)
先排四profiles及餘兩profiles的singleton／pair(1,3)/(3,1)，不設pieces大小上界：

| 原 (t_s,m_s,n_U) | 採納的任意大小來源矛盾 |
| --- | --- |
| (0,4,1)、(0,3,2)、(0,2,3)、(1,3,1) | DIRECT四profile排除，全部允許splits；(2,3)角色交換保持原C身份及完整r fibres |
| (1,2,2) | FIBRE先排singleton／pair13／pair31；pair22由T1全部14 schedules／28 spoke queries排除 |
| (2,2,1) | FIBRE先排singleton／pair13／pair31；pair22先由q0→q1排4，再由q0三份與q2七份排除 |

餘pair22在同一整圖色框為U012／L234／S40、e=rb4、r-split(2,2)、s-split(1,1)。
以下每個target query都作用於全部原vertices與完整preimages，沒有以marginals代替接合。

- [T1獨立驗收](../audits/2026-10-11-n45-s-long-s-t1-rfibre-review/REPORT.md)：
  β=q4的七份schedules、兩spoke位置各由retained原邊K₅排除；β=q3的七份、兩位置
  由完整degree-list／Gallai path-stabilizer與原K₅推得原S恰兩點，再在q0／q1構造
  完整同源r≠2 lift，恢復原rb4。包含T1-P22，未預設小S或忽略旁支。
- [T2／q0獨立驗收](../audits/2026-10-11-n45-s-long-s-t2-q0-restore-review/REPORT.md)：
  原G接受q1與完整S雙射迫β下S禁r=2，故q2的r=1 fibre空。沿用已採納Q(X)={β}，
  q2完整X lifts的聯集非空，每份均恢復rb4，排933/0234、941/023、941/024三份。
  非空是root-pair聯集，沒有聲稱每個固定pin非空。
- [T2／q2獨立驗收](../audits/2026-10-11-n45-s-long-s-t2-q2-restore-review/REPORT.md)：
  從β的局部L/S完整assignments及target列U strict-slack，直接構造同一原圖
  L_X(q3;0,3)、L_X(q4;0,3)均非空，全部恢復rb4；兩列覆蓋七份Δ。
  新非空性不以Q(X)或歷史finite-terminal代替。

28個raw必要schedules恰分為既有4＋本輪q0的3＋q2的7＋T1的14，逐份來源矛盾，
並非僅有限搜尋零survivor。[整合ledger](../audits/2026-10-11-n45-s-long-s-t1-rfibre-review/remaining-schedules.json)
保原身份、Δ及全部spoke位置，raw28剩0；本輪24 schedules／38 spoke queries全覆蓋。
與§2.9合成，只排完整K1–K12下的U／long／short選定契約，U owner=r或s皆涵蓋。
不排沒有U、兩long、其他derivative／core身份或一般N45／N2／E。

**採納更正與信任界。** 原FIBRE的30 queries分類以12+4+10+4採納，SF-RESIDUAL補列
SF-T2-Q0-Q1-RESTORED依賴；原worker不改。T1採納副本補352個X空欄位及780個G空欄位；
q2採納副本補112個X空欄位，均有去重field pointers及原SHA pins，不改原coverage／證書。
各固定pin的source preimages仍null，T1的恢復是存在完整lift聯集，不聲稱指定pin非空。
Q(X)={β}的繼承採納仍相對SF-T2-EXTEND／BASE E2紙面及歷史finite-terminal；q0使用此鏈，
T1／q2的新恢復存在性由新紙面構造承擔，亦保留其β-role／N-diagonal／Gallai等上游依賴。
兩份observations缺BASE blob finding保留，dependent finite replay未執行，不以physical檔補作BASE。
target source為not triggered，未執行target來源，沒有來源實現或新Lean。

[D獨立驗收](../audits/2026-10-11-n45-s-long-s-block-transfer-review/REPORT.md)
另採納任意大小完整assignment recurrence、preimage／空fibre保真與字面rb4 filter；
1,344 assignments只作四有效microcases的原邊校準。D不供給上述來源排除或一般非空引理；
其凍結24／38舊ledger與失敗case保留。完整採納／重播及文件傳播界線見
[本輪收尾紀錄](history/2026-10-11-n45-s-long-s-adoption.md)。

## 3. 精確 OPEN 與下一個窄分支

§1指定整U省略身份已由§2.2全排；精確S身份的兩short分支已由§2.8全排。
完整U／long／short且X=G−原spoke=M自身同β minimal的K1–K12選定契約，
已由§2.9的U在r與§2.10的U在s限定排除；不是所有含long殘留的完整分類。
既有S05只給原unary至多一份。沒有U的一long／一short與兩long仍OPEN；
不能把原U/L的盾弧、full B-touch或C/U private covering搬到沒有U的圖。

下一個窄入口是**原unary=0、一long／一short、只刪原spoke且X=M自身同β minimal**：
先重新核實際分量、原spoke／incidence完整必要身份、全部原Σ witnesses與X同β witnesses，
再對同一原圖、字面色框的全16pins及完整r fibres建立來源映射／原邊恢復義務。
兩long另保留；未發布新任務、未執行新來源搜尋。不擴graph/k或重開已採分支。
其他45／54身份、原55、無45／54來源、一般N2／E及ε≥3均仍OPEN。

## 4. 證據、重播與保留失敗

2026-10-11的四份獨立review及DIRECT／FIBRE／JOINT封存保持原bytes；
本輪文件採納是其後的研究狀態更新，舊review的shared_documents_updated=false保當時語境。
採納後不重跑要求live shared pins／tracked diff不變的歷史worker checker。
以下read-only入口核新review完整payload，不以封存PASS裁定紙面；完整命令、
本輪文件／Lean檢查與刻意未重跑項目見[收尾紀錄](history/2026-10-11-n45-s-long-s-adoption.md)。

```sh
python3 -B audits/2026-10-11-n45-s-long-s-t2-q0-restore-review/seal_review.py --directory audits/2026-10-11-n45-s-long-s-t1-rfibre-review --check
python3 -B audits/2026-10-11-n45-s-long-s-t2-q0-restore-review/seal_review.py --directory audits/2026-10-11-n45-s-long-s-t2-q0-restore-review --check
python3 -B audits/2026-10-11-n45-s-long-s-t2-q0-restore-review/seal_review.py --directory audits/2026-10-11-n45-s-long-s-t2-q2-restore-review --check
python3 -B audits/2026-10-11-n45-s-long-s-t2-q0-restore-review/seal_review.py --directory audits/2026-10-11-n45-s-long-s-block-transfer-review --check
```

本輪HIGH2完整118 regular=115payload＋3 exact top-level metadata、41inputs／8pins於採納前核回；
HIGH3三份完整tree、receipts及父端normal／seed17重播亦核回。H2C獨立有限重算只校準toy／工具，
H2A／H2R與父端共同保proper三色γ精化finding；封存不裁無界paper。
同期新增audit造成的原outside custody FAIL、四nested-repository directory markers只核presence的界線、
歷史62duplicate-ID／BASE缺檔／E4provenance FAIL均保留；不宣稱完整worktree零漂移。
本輪共享文件採納後，舊live-current pins不再是重播入口；原worker／reviewer bytes不改。
凍結證據、允許五shared變更及當前文件的只讀入口：

```sh
python3 -B audits/2026-10-10-n45-high23-supervision/verify.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-10-n45-high23-supervision/verify.py
```

此入口核artifact／採納custody，不以tool證paper；完整範圍見[監督報告](../audits/2026-10-10-n45-high23-supervision/REPORT.md)。

本輪HIGH1 worker 91 payload＋3個精確top-level metadata＝94 regular，無symlinks；
34frozen inputs為16BASE／17current／1external，九原派工pins及receipt十二commands／24streams核回。
原checker與完整receipt在共享文件採納前normal／seed17實際exit0且各對stdout一致。
採納後17個current輸入可能變動，改由獨立凍結verifiers與父端custody核回，不宣稱原live-input checker仍適用。
H1A／H1R兩份paper、H1C artifact-only均封存；父端六次完整重播exit0、normal／seed17各對byte一致。
H1C獨立Cartesian算術只校準toy的240literal rows／16rootqueries／2160 X及1560 G lifts，沒有HIGH1來源。
四種父端wrong-artifact probes各實際exit2命中certificate／input-index／receipt／payload-inventory階段；
H1C另核十項工具negatives，均不裁source前提。H1C保5,899 tracked bytes與worker94檔bytes/modes；
父端另核原Git-listed 32,713 regular、27symlinks及四nested repo目錄存在，遞迴內容不在其hash範圍。
既存歷史缺檔／E4 provenance與whole-worktree DocGraph 62 duplicate-ID FAIL保留，formal docs另核。
完整範圍與停L2記錄見[HIGH1監督報告](../audits/2026-10-10-n45-high1-supervision/REPORT.md)。

任意大小結論由 S／U paper 及 SU-A 逐 claim 稽核承擔；沿用 BASE E2、E3、E4、
B-S0/B-C2、原 unary shield 的明列前提，外部 Dvořák Lemma7／Theorem10 另列。
沒有重新證完上游所有分類，也沒有新增 Lean theorem／native_decide。
LP paper沿PA核過的單-root三分及外部Gallai；SS另由SSA／SSG核新圖類前提，
限定U合成沿既有已採納化約。五個relation lemmas仍按各自前提採納。
LOW1 新圖類映射另由 L1A／L1R各核六項，保持完整 U；沒有使用SS整U刪除的未接框點推論。
LOW2 新原 cycle／雙 U-contact完整接合由 L2A／L2R各核六項；限定 LOW合成另由 L2A核覆蓋。

SU-J 只驗23固定圖、7952不同整圖 pin cases、690 piece-row relations、2986 piece lifts、
102容量欄、288抽象 orbit 候選（92界成立、196不觸發），另保555原邊刪除控制。
19 N2 的精確933／941目標與拒絕45／54省略身份仍0觸發；12個45／54 occurrences 全屬N1。
38個 F_U 空列反駁過強的「每列必 singleton」，不反駁 U-REL，也不是目標來源反例。
有限控制不承擔本頁來源排除；來源實現及全型排除均未建立。
PC 與 PCA 採納具名有限 contract工具、23原圖／11整U、完整原 relations／lifts與555刪邊核對，
以及已觀察的錯宣告拒絕路徑。19 N2／7 N2整U的 LP三項仍0觸發；4 N1另列校準。
完整 LP exit0正分支與一般 validator soundness 尚未認證，有限結果沒有新增 paper closure。
PG／PR／PC及PCA的normal／seed17是第二批實跑，見其監督報告；本輪未重播那些finite工具。
SS原artifact verifier在新增稽核目錄前normal／seed17各exit0、6096payload核回；
SSC另核24BASE／11current／5pins、完整BASE archive與5個Git symlinks，只作封存裁決。
SSG的五份copied replay metadata有manifest排除範圍差異，原FAIL保留，
由[SS監督補充清單](../audits/2026-10-10-n45-ss-supervision/ssg-supplement.sha256)與fulltree另綁，四項幾何裁決不變。
LOW1 strict verifier在新增監督／稽核目錄前 normal／seed17各exit0、6049 regular／5 symlinks核回；
L1C另核12 BASE／6 pins／10 final-v4 receipt metadata及七項工具負控制。
四個nested repos初始僅核目錄存在，未遞迴hash；不報完整工作樹零漂移。
worker checks.json 的舊v1索引保留，最終成功以 delivery.json 明綁的 final-v4為準。
L1A三個section索引、空fibre與L1R一般γ記號由監督明列精化；L1R首封nested delivery漏列的FAIL及final-v2亦全保留。
全部 finding、父端實跑與封存版本見 [LOW1監督報告](../audits/2026-10-10-n45-low1-supervision/REPORT.md)。
LOW2 strict verifier在新增本輪目錄前 normal／seed17各exit0；66 payload／0 symlinks，
19個精確排除及 manifest→delivery、receipt→16 logs完整綁定，四BASE／八pins／20frozen inputs核回。
L2C獨立重播六原工具負控制及追加 nested receipt省略控制，全部exit2命中預期階段。
原 bad-receipt封存probe使用synthetic override；父端與L2C另用正式delivery直接核拒絕，兩層明列。
L2R的240 literal rows／61,440 ambient fibres是抽象 joint語義校準，沒有 LOW2 source／trigger數。
本輪三稽核的完整receipt normal／seed17父端重播一致；四nested repos仍無遞迴內容hash，
新增目錄後改核frozen證據與父端custody，不宣稱worker舊live-inventory仍適用。
完整 scope與既存 FAIL見[LOW2監督報告](../audits/2026-10-10-n45-low2-supervision/REPORT.md)。

```sh
python3 -B audits/2026-10-09-n45-su-j/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-09-n45-su-j/checker.py --check
```

輸入 provenance、封存 hashes、每個 exit／log 見 [監督採納](../audits/2026-10-09-n45-su-supervision/REPORT.md)。
兩個歷史 E4 byte replay FAIL（E3 REPORT provenance 差異）、fresh BASE 的兩份歷史缺檔及
whole-worktree DocGraph duplicate IDs 保留；正式 docs PASS 不表示全工作樹 PASS。
目前停止點亦見 [Kempe導覽](c5_kempe_guide.md#3-停止點與保留缺口)。
