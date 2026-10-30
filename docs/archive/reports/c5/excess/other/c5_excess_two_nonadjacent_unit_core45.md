---
docgraph:
  id: c5.excess-two-nonadjacent-unit-core45
  family: [c5, c5.excess-two, c5.arc2, c5.n2]
  requires:
    - c5.degree5-interfaces
  related:
    - c5.excess-two-arc-component-slack
    - c5.excess-two-arc-spoke-closure
    - c5.excess-two-arc-size-bound
    - c5.excess-two-n2-ll-cut
    - c5.excess-two-n2-bridge
---
# N45：非相鄰 N2 原 unit 省略的 45／54 身份

更新：2026-10-13（指定完整Σ契約的45／54與原55全排；N2-BRIDGE另排原E4三列契約的932，
該契約N2全排；基本LL-CUT未獨立證成，E-ARC2的N1／相鄰來源仍OPEN）；
原研究 BASE `dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`，既有 N45 驗收 BASE
`f2692089ad4259808e27d9b7e882ac09505b180a`；BR-SD-1b 採納基準為
`fc3d3d8b4c5b8e6378268edb5cd3f04b50940b5a`；BR-SD-1d 採納基準為
`46cd053b2b320d380eb0ee9326bf126551dd8a41`；BR-SD-1f 採納基準為
`0edb05b42d7b096103cdf241df7fb81e08dc16c7`；BR-SD-1g 正式採納基準為
`c15a635e17d4be814e19aeeeeb765f3d6024099a`。
本頁是已採納 N45 結論與目前 residual 的權威入口；完整新論證分別見
[S 原交付](../../../../../../audits/2026-10-09-n45-s/REPORT.md)與
[U 原交付](../../../../../../audits/2026-10-09-n45-u/REPORT.md)。
[SU-A](../../../../../../audits/2026-10-09-n45-su-a/REPORT.md)獨立核十四項 paper claim，
[SU-J](../../../../../../audits/2026-10-09-n45-su-j/REPORT.md)核指定有限介面；
[監督採納](../../../../../../audits/2026-10-09-n45-su-supervision/REPORT.md)對回封存版本及依賴。

**目前完整覆蓋：** [新紙面合成](c5_excess_two_arc_spoke_closure.md)已排除本頁§1的全部
exact-S root-spoke身份，連同既有exact-U，完整N2目標前提的45／54真cores已全排。
這一步使每條非框邊刪除全收，將來源化約為每列以原G自身作55核心（忽略自由孤立因子）。
後續[原55大小界](c5_excess_two_arc_size_bound.md)證`|H|≤35−6u−3t`，見§2.15。
後續[LL-CUT+diag](../n2/c5_excess_two_n2_ll_cut.md)已完成指定完整Σ契約的原55九格覆蓋，見§2.20。
**後續（2026-10-13，N2-BRIDGE）**：[前提橋接與932來源排除](../n2/c5_excess_two_n2_bridge.md)
另證932而完成原E4三列完整來源契約的廣義N2，見§2.21；未刪去本頁§1的原完整Σ前提。
基本LL-CUT尚未獨立證成，E-ARC2的N1／相鄰來源仍OPEN；契約外來源不作推廣。
新論證未Lean化，有限目標仍not triggered。
以下歷次採納及其當時限定範圍保留，目前缺口以§3為準。
第二批 [PG](../../../../../../audits/2026-10-09-n45-pg/REPORT.md)、
[PR](../../../../../../audits/2026-10-09-n45-pr/REPORT.md)、[PC](../../../../../../audits/2026-10-09-n45-pc/REPORT.md)
經 [PGA 幾何稽核](../../../../../../audits/2026-10-10-n45-pga/REPORT.md)、
[PA 紙面稽核](../../../../../../audits/2026-10-10-n45-pa/REPORT.md)、
[PCA 工具稽核](../../../../../../audits/2026-10-10-n45-pca/REPORT.md)與
[本輪監督採納](../../../../../../audits/2026-10-10-n45-p-supervision/REPORT.md)，完成限定範圍驗收。
後續 singleton-support 交付 [SS](../../../../../../audits/2026-10-10-n45-u-ss/REPORT.md)
經 [SSA 紙面與覆蓋稽核](../../../../../../audits/2026-10-10-n45-ssa/REPORT.md)、
[SSG 幾何／改色](../../../../../../audits/2026-10-10-n45-ssg/REPORT.md)、
[SSC 封存稽核](../../../../../../audits/2026-10-10-n45-ssc/REPORT.md)及
[SS 監督採納](../../../../../../audits/2026-10-10-n45-ss-supervision/REPORT.md)，完成限定採納。
後續 [LOW1](../../../../../../audits/2026-10-10-n45-s-low1/REPORT.md)經
[L1A 紙面](../../../../../../audits/2026-10-10-n45-l1a/REPORT.md)、
[L1R 原圖與完整關係](../../../../../../audits/2026-10-10-n45-l1r/REPORT.md)、
[L1C 封存](../../../../../../audits/2026-10-10-n45-l1c/REPORT.md)及
[LOW1 監督採納](../../../../../../audits/2026-10-10-n45-low1-supervision/REPORT.md)，完成限定採納。
後續 [LOW2](../../../../../../audits/2026-10-10-n45-s-low2/REPORT.md)經
[L2A 紙面與覆蓋](../../../../../../audits/2026-10-10-n45-l2a/REPORT.md)、
[L2R 原圖與完整關係](../../../../../../audits/2026-10-10-n45-l2r/REPORT.md)、
[L2C 封存](../../../../../../audits/2026-10-10-n45-l2c/REPORT.md)及
[LOW2 監督採納](../../../../../../audits/2026-10-10-n45-low2-supervision/REPORT.md)，完成限定採納與 LOW 覆蓋核對。
後續 [HIGH1](../../../../../../audits/2026-10-10-n45-s-high1/REPORT.md)經
[H1A 紙面](../../../../../../audits/2026-10-10-n45-h1a/REPORT.md)、
[H1R 原圖與完整關係](../../../../../../audits/2026-10-10-n45-h1r/REPORT.md)、
[H1C 封存](../../../../../../audits/2026-10-10-n45-h1c/REPORT.md)及
[HIGH1 監督採納](../../../../../../audits/2026-10-10-n45-high1-supervision/REPORT.md)，完成完整 H1–H13 內的限定採納。
後續 [HIGH2](../../../../../../audits/2026-10-10-n45-s-high2/REPORT.md)經
[H2A 紙面／覆蓋](../../../../../../audits/2026-10-10-n45-h2a/REPORT.md)、
[H2R 原圖／完整 lifts](../../../../../../audits/2026-10-10-n45-h2r/REPORT.md)、
[H2C 工具／封存](../../../../../../audits/2026-10-10-n45-h2c/REPORT.md)及
[HIGH2／HIGH3 監督驗收](../../../../../../audits/2026-10-10-n45-high23-supervision/REPORT.md)，
在完整契約內採納；未用色接回構造明限 proper 三色列，原過寬量詞保留 finding。
[H3A](../../../../../../audits/2026-10-10-n45-h3a/REPORT.md)、
[H3R](../../../../../../audits/2026-10-10-n45-h3r/REPORT.md)、
[H3G](../../../../../../audits/2026-10-10-n45-h3g/REPORT.md)獨立核回完整 HIGH3 契約到 BASE no-spoke 排除，
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
無U的long／兩long之exact-S身份由後續§2.14涵蓋；原55、N2外其他45／54、
一般 N2／E及原Σ933／941來源的ε≥3下界仍 OPEN。
其二連通 subsets、**BR-SD-1a 三環單 bridge 無旁支子域**、
**BR-SD-1c 同骨架單一原 W 只接 J1/J2 子域**與
**BR-SD-1e 單一原 W 只接 J3／q 外臂子域**與
**BR-SD-1g 雙原旁支／J2 屏障子域**的精確排除見§2.11；
四個 BR-SD 結果不依二連通，均不計作完整父身份關閉。
後續§2.12以唯一雙色缺口統一四支：保完整原 S、degree lists／拒絕、actual 異色 pair、
唯一 s-contact q 而 r 對 S 至少兩個原 contacts，即排除任意有限 block 形狀。
新紙面證明不需三環骨架、旁支數／位置或 private witness；父身份仍 OPEN。

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

本節依研究次序保存各輪證明及當輪停止點；§2.13–2.19所列尚缺的來源排除，
其後續涵蓋見§2.20–2.21，目前狀態以§3為準。歷史audit、採納契約及not-triggered證據不改。

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
| BR-SD-1a scoped exclusion | N45-S-NOU-LS-PAIR 的 split22／共用 r 雙環／三環單 bridge 無旁支精確合同不可能成立；任意奇環長與原外臂長 | 完整前提見§2.11；獨立紙面驗證、封存與發布已完成，不依 SD-A／二連通；父身份仍 OPEN |
| BR-SD-1c scoped exclusion | 同一 N45-S-NOU-LS-PAIR／split22 原三環單 bridge 骨架，新增一份有限非空原 pendant W 只接 J1/J2，保 actual S pair support 及未改動 J3／q 外臂的精確合同不可能成立 | 任意奇環／p、q 外臂長／有限 W 大小及所有允許接點；完整前提與局部引理界線見§2.11，父身份仍 OPEN，無新來源或 Lean |
| BR-SD-1e scoped exclusion | 同一 N45-S-NOU-LS-PAIR／split22 原三環單 bridge 骨架，恰一份有限非空原 W 唯一接 J3／q 外臂、保 actual S pair support 及完整原 degree／資料的精確合同不可能成立 | 全部允許接點、任意奇環／p、q 外臂長／有限 W 大小及具名重合；完整前提與 private-witness preservation lemma 界線見§2.11，不依1c terminal lemma，父身份仍 OPEN |
| BR-SD-1g scoped exclusion（雙原旁支／J2 屏障） | 同一 N45-S-NOU-LS-PAIR／split22 原三環單 bridge，J1 指定 triangle，恰兩原 W1/W2 分別唯一接 J1 的 x1 與 J3／q 臂的 x2；完整精確來源合同不可能成立 | 任意原 J2/J3 奇長、可零長 p/q 臂、有限非空 Wi 大小、合法接點與重合；S short／actual pair、M 自身同 β minimal 且拒絕及全部原資料全保，完整八項合同見§2.11。父 OPEN，actual source NOT TRIGGERED，無新 Lean |
| 雙色唯一缺口的共同排除 | 不可著色 degree lists；完整 S 僅 q 含 T 缺 D，其餘原 lists 含 T/D，則唯一 r-contact 且 r–q 全為 bridges；因此§2.12原圖前提加至少兩個 r-contacts 全排 | 任意有限圖／色集的紙面證明＋外部 Gallai；四份 BR 為特例，不需旁支／三環／private witness 分類；未另經獨立審查，無新來源或 Lean，父 OPEN |


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
[no-spoke (5) §4](../../structure/c5_no_spoke_exterior.md)、
[single-spoke (4)](../../single-spoke/c5_single_spoke_four.md)、
[two-spoke (3)](../../structure/c5_two_spoke_three_contacts.md) 的任意大小排除。
t_s=0不要求 C 外的 s–B 路；t_s=2涵蓋任意兩條 β 異色 spokes。三分全矛盾。

完整前提映射、外部 Dvořák Lemma7／Theorem10 的凍結原文及獨立裁決見
[PA §2–5](../../../../../../audits/2026-10-10-n45-pa/REPORT.md)。沿用具名 BASE 紙面分類與外部定理的信任界，
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
完整新前提映射與十一裁決見[SSA§2–7](../../../../../../audits/2026-10-10-n45-ssa/REPORT.md)。
沿明列BASE papers與外部Dvořák Lemma7／Theorem10；沒有新Lean、SS finite source或trigger數。

**限定合成覆蓋。** §1的U身份有省略的原U，原unary至多兩份；U-U2排兩份，故唯一U。
兩mixed的short／long互斥且窮盡：U-SHORT排兩short，原2+2+2盾費排兩long，故long＋short。
short支援非空，只有真框邊pair或singleton；pair由U-RES逐项滿足已採納LP全部前提，
singleton由U-S3排總incidence≤3，餘≥4恰滿本SS契約。兩支皆排，沒有未覆蓋子支。
此合成由[SSA§8](../../../../../../audits/2026-10-10-n45-ssa/REPORT.md)獨立驗收，只排
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
[BASE 三接點 §1–5](../../structure/c5_two_spoke_three_contacts.md)允許任意兩個 β 異色 spoke 位置；
不要求 β 是 U 盾中點列，也不刪 U。933 q2、共同整圖 D₅／S₄／root swap一併保留。

完整六項契約與論證見 [LOW1](../../../../../../audits/2026-10-10-n45-s-low1/REPORT.md)，
[L1A](../../../../../../audits/2026-10-10-n45-l1a/REPORT.md)與 [L1R](../../../../../../audits/2026-10-10-n45-l1r/REPORT.md)各自獨立核回。
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

完整十二項契約及六 claims見[LOW2](../../../../../../audits/2026-10-10-n45-s-low2/REPORT.md)，
[L2A](../../../../../../audits/2026-10-10-n45-l2a/REPORT.md)與[L2R](../../../../../../audits/2026-10-10-n45-l2r/REPORT.md)各自獨立核回。
這是任意大小 paper＋明列 BASE／外部 Dvořák Lemma7／Theorem10，沒有新 LOW2有限來源或 Lean。

**限定合成覆蓋。** 只取§1精確 S身份及已採納 S06 的 S-SHORT-U-LOW：唯一原 U在 r，
兩原 mixed真框邊 pair支援、(m_r,m_s)=(2,3)。令 u為原 U incidence，t為原 r-spokes；
完整原 degree5給 2+u+t=5，U接 r給 u≥1，省略原 spoke存在給 t≥1。
故(u,t)只有(1,2)、(2,1)，s原三 mixed contacts另給 t_s=2。
兩支分別逐項滿足已採納 LOW1與本 LOW2的全部契約，互斥且窮盡。
[L2A §7](../../../../../../audits/2026-10-10-n45-l2a/REPORT.md)獨立核覆蓋，
[監督接受紀錄](../../../../../../audits/2026-10-10-n45-low2-supervision/acceptance.json)另列此合成 scope。
因此只排 **§1精確 S-SHORT-U-LOW**；HIGH、long、其他 cores／原55及一般 N2／E未關。

### 2.5 N45-S-HIGH1：原 K₃,₃ 與同列完整 G lifts

只取§1精確S身份：原U只接s、唯一原sx且無U–r；P/Q各actual support恰真原框邊兩端，
(m_r,m_s)=(3,2)，s對P/Q各一，r分配1與2。原r/s各兩spokes，僅省略e=rb_i，
X保rb_j及全部s-spokes；U/P/Q整份全留。X=G−e=M自己的β-minimality另列，
有效H連通／full B-touch、原degree4/5、Σ-critical／ε2、所有具名ordered資料、空fibres與full lifts
及共同整圖D5／S4／root swap均保留。全部十三項前提逐字見
[HIGH1 H1–H13](../../../../../../audits/2026-10-10-n45-s-high1/REPORT.md)。

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

[H1A](../../../../../../audits/2026-10-10-n45-h1a/REPORT.md)與[H1R](../../../../../../audits/2026-10-10-n45-h1r/REPORT.md)
各獨立核十claims，無新增前提或gap；[監督接受紀錄](../../../../../../audits/2026-10-10-n45-high1-supervision/acceptance.json)
逐字保全部H1–H13。這是任意大小paper，沿用BASE原盾／N-diagonal／(2,1)論證及
[外部Dvořák Gallai Lemma7／Theorem10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)信任界；
封存與有限toy只核語義／算術，未建立或執行HIGH1 finite source，沒有trigger數或新Lean。


### 2.6 N45-S-HIGH2：原雙 contact 與恢復 e 的 G lifts

只取§1精確 S 身份，另有原 U 只接 s 的兩個相異 contacts、無 U–r；
P/Q 支援真框邊、(m_r,m_s)=(3,2)。原 r 兩 spokes 只刪 e=rb_i 留 rb_j，
s 唯一 spoke sb_k 全留；U/P/Q 全原邊、原 cycle 及全部 assignments 保留。
X=G−e=M 自己是 β inclusion-minimal45／54 core。完整 H1–H13逐字見
[HIGH2 原交付](../../../../../../audits/2026-10-10-n45-s-high2/REPORT.md)。

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

[H2A](../../../../../../audits/2026-10-10-n45-h2a/REPORT.md)與[H2R](../../../../../../audits/2026-10-10-n45-h2r/REPORT.md)
獨立裁紙面／原圖及全部 fibres；[H2C](../../../../../../audits/2026-10-10-n45-h2c/REPORT.md)只裁封存與有限工具。
這是任意大小 paper＋BASE＋明列外部 Gallai，沒有 finite HIGH2 source、trigger數或新Lean。

### 2.7 N45-S-HIGH3：原 X 的 no-spoke (3,2) 排除

只取§1精確 S 身份，原 U在s恰三個相異contacts且無U–r，s無spoke；
P/Q真框邊支援、(m_r,m_s)=(3,2)，r兩spokes只刪e留rb_j、X=M自己minimal。
全部原件與具名ordered/shared資料、十列完整 relations、空fibres及孤立自由因子保留；
[完整K1–K13](../../../../../../audits/2026-10-10-n45-h3a/frozen/authority/common-contract.md)限制本輪採納範圍。

X的唯一完整degree5點是s，其餘有效原內點degree4；H_X−s實際分量恰C={r}∪P∪Q與U，
ordered contacts數(2,3)。完整同列接合、X自己的minimality及slack給F_C∪F_U=Col、
各private非空、|F_C|≤2，從而|F_U|≥2；不預設指定禁色角色。
原拒絕三色β以一次共同整圖D5／S4搬到q，逐前提接回BASE no-spoke §§1–3、5的(3,2)來源排除。
避整U的s–P–r–rb_j原路恢復外hub；U的K4-free、active triangle、任意／零長arms及原tethers
給五個互斥連通bags及十原鄰接，Z–O用另一分量的原s-contact；全部在X、不用省略e。
這是原X非平面反證，不是X指定延拓提升成G，也不是必要表項的來源實現。

[H3A](../../../../../../audits/2026-10-10-n45-h3a/REPORT.md)、[H3R](../../../../../../audits/2026-10-10-n45-h3r/REPORT.md)、
[H3G](../../../../../../audits/2026-10-10-n45-h3g/REPORT.md)各自獨立核回，父端另核原圖／全lifts及封存。
任意大小結論依賴BASE及外部Gallai；抽象toy／bags只校準語義，無有限HIGH3來源或新Lean。

### 2.8 限定 HIGH 與兩 short S 身份的完整覆蓋

在§1精確S身份的两原mixed都short時，已採納S05／S06迫唯一原U、兩mixed真框邊支援，
unary側／另一側mixed incidence=2／3。LOW已由§2.4的兩支窮盡排除。
HIGH令u為原U在s的contact數、t_s為原s-spokes，完整degree5给2+u+t_s=5，
u≥1、t_s≥0，故(u,t_s)恰(1,2)、(2,1)、(3,0)。原r三mixed+兩spokes中只省略e。
這三支逐項滿足HIGH1／HIGH2／HIGH3的各自完整契約、X自己β-minimal性及所有同源資料。
它們互斥窮盡，不另加入充分前提，也不從G遺傳X minimality。

[H2A覆蓋稽核](../../../../../../audits/2026-10-10-n45-h2a/REPORT.md)與
[父端接受紀錄](../../../../../../audits/2026-10-10-n45-high23-supervision/acceptance.json)核回三支及LOW／HIGH合成。
故只關 **§1精確S身份的兩原mixed都short分支**；含long、其他省略／core身份、原55、
無45／54來源、一般N2／E及ε≥3仍OPEN，沒有新增有限來源或Lean。

### 2.9 N45-S-LONG-R：保留完整 U／long／short 的 sole C 排除

在[含long同源契約K1–K12](../../../../../../audits/2026-10-10-n45-s-long-contract/REPORT.md)全部前提內，
另有原U owner=r。[SL-MAP-R完整報告](../../../../../../audits/2026-10-10-n45-s-long-r-map/REPORT.md)
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

只取[含long同源契約K1–K12](../../../../../../audits/2026-10-10-n45-s-long-contract/REPORT.md)
的全部前提，另有原U owner=s。G任意有限大小、ordered induced-C5 disk，完整Σ=933／941
或整圖共同D5像，非框邊Σ-critical；有效H連通、ε=2、非相鄰原degree5 r/s，
其餘有效原內點完整degree4。H−{r,s}的實際分量恰為完整原U／long L／short S；
原one-sided、full B-touch、S真框邊pair或singleton、自由孤立內點的完整因子均保留。
只刪原e=rb_i，X=G−e=M自己是同一原拒絕literal β的inclusion-minimal(4,5) core。
保G各非框邊的Σ witnesses與X各retained非框邊的同β witnesses，不能從G遺傳X minimality。
每份原ordered/shared contact、actual attachment、ownership、rotation、bridge、旁支、
十literal列／全16pins／diagonal／空fibres／全部tuples、preimages及full lifts均保留。

由原degree5身份m_s+n_U+t_s=5、m_s≥2、n_U≥1，恰有六profiles。
[DIRECT／FIBRE獨立採納及更正](../../../../../../audits/2026-10-11-n45-s-long-s-review/REPORT.md)
先排四profiles及餘兩profiles的singleton／pair(1,3)/(3,1)，不設pieces大小上界：

| 原 (t_s,m_s,n_U) | 採納的任意大小來源矛盾 |
| --- | --- |
| (0,4,1)、(0,3,2)、(0,2,3)、(1,3,1) | DIRECT四profile排除，全部允許splits；(2,3)角色交換保持原C身份及完整r fibres |
| (1,2,2) | FIBRE先排singleton／pair13／pair31；pair22由T1全部14 schedules／28 spoke queries排除 |
| (2,2,1) | FIBRE先排singleton／pair13／pair31；pair22先由q0→q1排4，再由q0三份與q2七份排除 |

餘pair22在同一整圖色框為U012／L234／S40、e=rb4、r-split(2,2)、s-split(1,1)。
以下每個target query都作用於全部原vertices與完整preimages，沒有以marginals代替接合。

- [T1獨立驗收](../../../../../../audits/2026-10-11-n45-s-long-s-t1-rfibre-review/REPORT.md)：
  β=q4的七份schedules、兩spoke位置各由retained原邊K₅排除；β=q3的七份、兩位置
  由完整degree-list／Gallai path-stabilizer與原K₅推得原S恰兩點，再在q0／q1構造
  完整同源r≠2 lift，恢復原rb4。包含T1-P22，未預設小S或忽略旁支。
- [T2／q0獨立驗收](../../../../../../audits/2026-10-11-n45-s-long-s-t2-q0-restore-review/REPORT.md)：
  原G接受q1與完整S雙射迫β下S禁r=2，故q2的r=1 fibre空。沿用已採納Q(X)={β}，
  q2完整X lifts的聯集非空，每份均恢復rb4，排933/0234、941/023、941/024三份。
  非空是root-pair聯集，沒有聲稱每個固定pin非空。
- [T2／q2獨立驗收](../../../../../../audits/2026-10-11-n45-s-long-s-t2-q2-restore-review/REPORT.md)：
  從β的局部L/S完整assignments及target列U strict-slack，直接構造同一原圖
  L_X(q3;0,3)、L_X(q4;0,3)均非空，全部恢復rb4；兩列覆蓋七份Δ。
  新非空性不以Q(X)或歷史finite-terminal代替。

28個raw必要schedules恰分為既有4＋本輪q0的3＋q2的7＋T1的14，逐份來源矛盾，
並非僅有限搜尋零survivor。[整合ledger](../../../../../../audits/2026-10-11-n45-s-long-s-t1-rfibre-review/remaining-schedules.json)
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

[D獨立驗收](../../../../../../audits/2026-10-11-n45-s-long-s-block-transfer-review/REPORT.md)
另採納任意大小完整assignment recurrence、preimage／空fibre保真與字面rb4 filter；
1,344 assignments只作四有效microcases的原邊校準。D不供給上述來源排除或一般非空引理；
其凍結24／38舊ledger與失敗case保留。完整採納／重播及文件傳播界線見
[本輪收尾紀錄](../../../../../history/2026-10-11-n45-s-long-s-adoption.md)。

### 2.11 單缺額查證與無 U 二連通子域

後續§2.14已在完整N2目標前提證無U的原H二連通，並完成該域全部spoke45／54排除。
下列鏈形缺口保留原查證時語境；一般degree5／R31方法義務不因此完成。

本節保留各輪獨立採納的精確合同與證據。後續[§2.12](#212-雙色唯一缺口的共同排除)
給出共同紙面推論；下文各輪「其他形狀／多旁支 OPEN」須扣除該新推論的完整適用域，
目前 residual 以§3為準，原歷史證明及 audit bytes 保留。

查證 BASE `4dd11f422c6fa49265a412085116b088786d0344`。
[SD-A](../../degree5/c5_degree5_interfaces.md#7-二連通單缺額查證與-4554-接入) 已完成指定前提的紙面查證；
[B 適用性與身份表](../../../../../../audits/2026-10-11-single-deficit-applicability-804e3b0b1b/APPLICABILITY.md)
原樣保留其封存時 A 待驗的 conditional 語境。應用須明列本頁原 G 合同、
原具名省略、X=M 自身同 β minimal、M 的完整 degree4/5及 H_M 二連通，
不從 Σ-critical G 自動推 X 對 β minimal，也不從 β-minimality 推二連通。

在上述實際前提下，無 U exact-S 的兩 long 被原 s-star 盾弧預算與 SD-A 排除；
long／singleton-support short 被 contact 預算與既有 S04／S3 排除。
long／真 edge-pair short 剩餘映到兩原 s-contacts p/q 間的無旁支 Gallai block 鏈，
r 為 C=H_M−s 的割點；每側 r-contact 數是1或2。P/Q內的 H_M 割點仍須逐來源核實。
完整保留 unary 的 owner root 是 H_M 割點，不屬此二連通域；已採納 LOW／HIGH／LONG 不重開。
相鄰兩 mixed45／54的二連通子域亦由 rs＋兩 mixed 原contacts迫 s內度≥3而排除，
其原合同與其他具名障礙見[B報告](../../../../../../audits/2026-10-11-single-deficit-applicability-804e3b0b1b/REPORT.md)。

零／一／二 odd-cycle blocks及既有 R27共用點鏈按精確前提接回原結果；
一般環間 bridges、三環其他位置與更多環仍 OPEN。
上述 SD-A／B 的查證與歷史 conditional 語境仍見[整理紀錄](../../../../../history/2026-10-11-single-deficit-progress.md)。

**BR-SD-1a canonical 採納（2026-10-11，BR-SD-1b）：**
[獨立 REPORT](../../../../../../audits/2026-10-11-br-sd-1a-0f181045/REPORT.md) 與
[原點／原邊 PROOF](../../../../../../audits/2026-10-11-br-sd-1a-0f181045/PROOF.md) 已驗證、封存並由
[publication commit fc3d3d8b4c5b8e6378268edb5cd3f04b50940b5a](https://github.com/raylei50653/math/commit/fc3d3d8b4c5b8e6378268edb5cd3f04b50940b5a)
發布；[PUBLICATION](../../../../../../audits/2026-10-11-br-sd-1a-0f181045/PUBLICATION.md) 區分原 audit 的未發布歷史欄位。
本次正式採納以下完整合同的 **Scoped exclusion**；不承接前段 SD-A 的二連通必要前提。

1. 保留§1全部原 G 合同：任意大小有限簡單 ordered induced-C₅ disk，完整有序
   Σ933／941 或共同搬運整圖的 D₅ 像、ε=2、各非框邊 Σ-critical 與自己的完整 witnesses，
   原非相鄰 degree5 roots r/s。`H_G−{r,s}` 恰原 L/S 兩份完整 mixed，原 unary U=0；
   L long，S short 且 actual support 恰一條真框邊的兩端。
2. exact-S 只省略 r 的唯一原 boundary spoke `e=rb_i`；`X=M=G−e` 保留其他全部原點／邊。
   M 自己是同一原拒絕 literal proper 三色 β 的 inclusion-minimal core，各 retained 非框邊
   保同 β 的完整刪邊 witness。M 的唯一 degree5 內點為 s，其餘有效內點完整 degree4；
   45／54 只共同交換原 roots roles 與全部資料，使 r 為降度側，不各自正規化 components。
3. s 恰有不同的原有序內鄰 p/q，分屬 L/S，三條原 B-spokes 全留。
   `C=H_M−s={r}∪L∪S` 是同一實際 sole connected component；r 對 L/S 各有兩個原 contacts
   （split22），在 C 度4且在 M 無 boundary spoke。
4. C 的全部 blocks 恰三個原 odd-cycle blocks J1/J2/J3 與指定原 bridges；
   `J1∩J2={r}`，J3 與兩者不交。J2 私有 u≠r 與 J3 私有 v 由唯一環間原 bridge uv 相連。
   p/q 經原外臂分別到 J1/J3 的私有錨點 a1/a3，臂可零長；無其他 blocks／旁支。
   三環長為任意奇數≥3，兩外臂長為任意非負整數；不另假定 a3≠v。
5. 所有 ordered/shared contacts、actual attachments/supports、ownership、rotation、bridge 端點、
   boundary assignments、完整 relations／fibres（含空 fibres）／full lifts 與同一 literal 四色框均保留。
   D 是此同一 β 未使用的第四色；不以抽象 lists 或獨立色正規化替换原來源。

在此完整合同下，原 M 邊定義的 `L^D` 逐點至少 C-degree；若 C 可染，與原 β、s=D
接成 M 的完整染色，違反拒絕。任意環長均可選
`w1∈J1−{r,a1}`、`w2∈J2−{r,u}`；無旁支形狀保它們非 C 割點、非 s-contact。
兩點各只屬本環一個 block，兩個原 B 附件均未使用 D，故兩份 lists 都含同一 D。
外部 Gallai 刻畫給各 list 等於本環 palette，J1/J2 在 r 相交卻要求 palettes 互斥，矛盾。
四步任意大小推論與逐前提映射由原 PROOF／REPORT 及
[MAPPING](../../../../../../audits/2026-10-11-br-sd-1a-0f181045/agents/mapping/MAPPING.md) 承擔。

外部依賴是 [Dvořák 作者講義 Theorem10／blockwise-uniform 定義，p.6](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，
凍結來源與 hash 見[外部來源紀錄](../../../../../../audits/2026-10-11-br-sd-1a-0f181045/external/SOURCE.md)；
不是新增 Lean theorem。31,296 列與 synthetic M 的有限 controls 是 `triggered and holds` 校準，
撤去 witness 的 D-presence 負控制不滿足原來源合同；actual target source 未提交、`not triggered`。
有限 controls 與 seal PASS 不承擔任意大小量詞，也沒有新增來源實現。
保留具名精度 finding：a3 可等於 v，不能由私有錨點推 H_M 二連通；此證明不依
SD-A、二連通、T4 定位、uv→R27 minor 或 target 四-query／minimality，沒有宣稱補完舊 minor 路線。
完整 `N45-S-NOU-LS-PAIR` 仍 OPEN；既有 LOW／HIGH／LONG 與 U 排除不重開。
採納／重播／傳播核對見[BR-SD-1b 紀錄](../../../../../history/2026-10-11-br-sd-1b-adoption.md)。

**BR-SD-1c canonical 採納（2026-10-11，BR-SD-1d）：**
[REPORT](../../../../../../audits/2026-10-11-br-sd-1c-fd6e1112/REPORT.md)、
[最終 PROOF](../../../../../../audits/2026-10-11-br-sd-1c-fd6e1112/PROOF.md) 與
[MAPPING](../../../../../../audits/2026-10-11-br-sd-1c-fd6e1112/MAPPING.md) 已經
[精確最終 bytes 的獨立紙面審查](../../../../../../audits/2026-10-11-br-sd-1c-fd6e1112/agents/paper/REVIEW.final-v2.md)、
封存及 [publication commit 46cd053](https://github.com/raylei50653/math/commit/46cd053b2b320d380eb0ee9326bf126551dd8a41)
發布；[PUBLICATION](../../../../../../audits/2026-10-11-br-sd-1c-fd6e1112/PUBLICATION.md) 保留 audit 當輪與發布後的分工。
本次正式採納以下 **Scoped exclusion**，不重證或擴大原結果：

- 完整沿用上列 BR-SD-1a 合同1–3、5，包括同一原 G／完整 Σ933／941 或整圖 D₅ 像、
  ε=2、原 Σ-critical 與全部 witnesses、原非相鄰 degree5 roots r/s、其餘有效原內點4；
  exact-S 只省略 r 唯一原 spoke，`X=M=G−e` 自己對同一 proper 三色 β minimal 且拒絕，
  原 U=0、L long、S actual support 恰一條真框邊兩端，全部原資料及 full lifts 保留。
- 原 C 仍為 sole connected component、r split22，保 J1/J2/J3 三原 odd-cycle blocks、
  `J1∩J2={r}`、不交的 J3、唯一原環間 bridge uv、原 p/q 外臂與錨點 a1/a3，允許 a3=v。
  只放寬合同4的無旁支限制：一份來源自己的有限非空原 W，其 off-skeleton 內點連通，
  只在具名 `x∈J1∪J2` 接入骨架，無額外 s-contact、cross edge 或其他骨架接線。
  W 接 J1／J2 分別屬完整原 L／S；其原 B 附件、blocks、ownership、rotation 全保留。
  這是候選原來源自己的骨架與 W，不向已 degree4 的舊來源任意加邊或刪附件。
- J3／q 外臂的原附件及接線不變：J3 的其他 block 接入只在 v、a3，q 是該側唯一
  s-contact；外臂每邊都是 C 的 bridge，a3 以外各臂點只有原路徑 C 鄰居。
  正長時 q 的 `d_C=1`、臂內點 `d_C=2`，包括末端 q 都不能有額外 C 邊。

**正式結果僅限上述單一原 W 只接 J1/J2 的精確來源合同不可能成立。**
任意奇環長≥3、p/q 外臂長≥0、有限 W 大小及所有允許具名接點均已涵蓋。
採納前逐項映射與量詞核對見[BR-SD-1d 紀錄](../../../../../history/2026-10-11-br-sd-1d-adoption.md)。

原證明的三條路徑分清：r 已被四條原環邊飽和，接非空 W 違完整 degree4；
a1/u 只容首 W bridge，其他私有點最多容兩條 W incident 邊。
若兩個 private witnesses 仍存在，非割點 lists 各等於本環 palette、都含同一 D，
與 J1/J2 在 r 相交的 palette 互斥矛盾。
接入環為 triangle、旁支佔用唯一 private witness 時，J2 例外由未改動 J3 迫
`D∉P_uv`，u 只 incident J2／uv，故 D 回到 J2；J1 例外由下述局部末端引理排除。

**可重用 pair-supported terminal lemma 的完整局部前提與界線：**
在同一原 M／proper 三色 β（D 未用）的連通 C 中，每點完整 M-degree4，
原 β／s=D 給 `|L^D(y)|≥d_C(y)` 且 C 不可 L^D 著色；原奇環 J 及 q 外臂的
全部 B 附件位於同一真框邊兩個異色框點；J 的其他 block 接入至多在 v、a，
存在未佔用的私有非 s-contact 環點；q 為該側唯一 s-contact；臂是原 simple bridge path，
a 以外全部臂點（包括 q）無額外 C 邊。只有在這些完整前提下採納局部排除，
不把它登記為一般多旁支或 Gallai block tree closure。
在本輪 J=J3、a=a3，raw support `N_B^M(S)=N_B^G(S)={b_i,b_{i+1}}`，
原私有點 degree4 強迫兩 B 附件恰為該 pair，故 `P_J3={T,D}`，T 是 β 第三已用色。
q 臂長0時 q 禁 D；長1時末端 q list={T}；長≥2時首個 off-cycle 臂點 list={T,D}。
正長臂首 bridge 的非空 singleton palette 包含於該 list，卻須在 a3 與 J3 palette 互斥。
三案完整涵蓋任意臂長及 a3=v；不縮臂、不作一般 cutpoint D 傳遞。

`D∈L^D(x)` **不能推出每個 incident block palette 都含 D**。
原 PROOF§7 的 abstract palettes 與[負控制](../../../../../../audits/2026-10-11-br-sd-1c-fd6e1112/agents/controls/REPORT.v2.md)
保留此 `counterexample`：D 可全落在 W bridge；其 synthetic S 使用三個框點，違 actual pair support。
四份固定 synthetic M 只校準原邊／lists／完整 fibres／lifts及 witness／routing：前三份接受 β，
第四份拒絕但撤 pair support，全部 actual target source 為 `not triggered`。
任意大小排除由封存 PROOF 與獨立審查承擔，沒有新來源實現或 Lean theorem。
外部依賴仍是 Dvořák Theorem10／blockwise-uniform characterization，
版本與 hash 見[1c SOURCE](../../../../../../audits/2026-10-11-br-sd-1c-fd6e1112/external/SOURCE.md)。
1a 無旁支排除與1c 單一 W 排除分列；兩者原範圍保持，後續1e採納如下。

**BR-SD-1e canonical 採納（2026-10-11，BR-SD-1f）：**
[最終 PROOF](../../../../../../audits/2026-10-11-br-sd-1e-337d018b/PROOF.md)、
[MAPPING](../../../../../../audits/2026-10-11-br-sd-1e-337d018b/MAPPING.md) 與
[REPORT](../../../../../../audits/2026-10-11-br-sd-1e-337d018b/REPORT.md) 已由
[獨立紙面審查](../../../../../../audits/2026-10-11-br-sd-1e-337d018b/agents/paper/REVIEW.final.md)／
[ACCEPTANCE](../../../../../../audits/2026-10-11-br-sd-1e-337d018b/agents/paper/ACCEPTANCE.json)
接受精確最終 bytes，封存並由
[publication commit 0edb05b](https://github.com/raylei50653/math/commit/0edb05b42d7b096103cdf241df7fb81e08dc16c7)
發布。本輪正式接入以下 **Scoped exclusion**；原 audit 的 candidate／未發布措辭保留當輪語境。

- 完整沿用上列 BR-SD-1a 合同1–3、5：同一有限簡單 ordered induced-C₅ disk 原 G、
  完整 Σ933／941 或共同整圖 D₅ 像、ε=2、逐非框邊 Σ-critical 與原 full witnesses；
  原非相鄰 degree5 roots r/s、其餘有效內點完整4；原 U=0、L long、S actual support
  恰同一真框邊兩端。exact-S 僅省略 r 唯一原 spoke，`X=M=G−e` 自身對同一
  proper 三色 β inclusion-minimal 且拒絕，保 retained-edge witnesses；不由 G 遺傳 minimality。
  M 僅 s 完整5，其餘有效內點完整4，s 的原有序 p/q contacts 與三原 spokes 全留。
- 同一實際 sole C、r split22，保三原 odd-cycle blocks J1/J2/J3、`J1∩J2={r}`、
  不交 J3、J2 私有 u≠r 與 J3 私有 v 間唯一原環間 bridge uv，以及原 p/q simple bridge
  外臂與私有錨點 a1/a3；環長任意奇數≥3、兩臂長任意≥0，允許 a3=v。
  僅放寬合同4：恰一份有限非空原 off-skeleton W，`C[W]` 連通，
  `V(C)=V(C0)⊔W`、`N_C(W)={x}`，具名 `x∈J3∪q-arm`；可有多條 x–W 邊。
  無其他旁支、cross edge、W–s 邊或 J1/J2 新接線。
- W 屬來源自己的完整原 S，全部 W 附件在同一 pair，整份原 S 支援聯集仍恰為
  `N_B^M(S)=N_B^G(S)={b_i,b_{i+1}}`。所有原點／邊、contacts、attachments、ownership、
  rotation、bridges、共同 literal 色框、完整 relations／fibres（含空 fibres）及 full lifts 全保。
  C0 是候選原 C 的骨架，不向已完整 degree4 的舊圖任意加邊，也不刪原附件容納 W。

**正式結果僅限上述精確來源合同不可能成立；全部允許接點、任意三環奇長、
p/q 外臂長、有限非空 W 大小及允許具名重合均涵蓋。**
在 `x=a3=v`，零長臂的骨架度3＋s-contact1、正長臂的骨架度4均已飽和，
非空 W 結構超度。其餘接點由同一原 M 的 `4=d_C0(x)+m+k+t` 核容量；
k 是原實際附件數，不准刪附件。W 各點無 s-contact且 k≤2，仍須完整 degree4。

**可重用 private-witness preservation lemma 僅在完整結構前提下採納：**
同一具名骨架、原 cycle／bridge 邊全保，有限非空連通 W 的唯一骨架鄰點在 J3／q 臂，
無第二接點、cross edge、額外 s-contact 或 J1/J2 新接線。則原
`w1∈J1−{r,a1}`、`w2∈J2−{r,u}` 永遠存在（含 triangle），
各只屬本環 block、非 C 割點、非 s-contact、完整 C-degree2。
本輪完整 M-degree4及同一 β 未用 D 給兩原 lists 均含 D。
原邊給 `|L^D(y)|≥d_C(y)`，完整 C list-coloring 與同一 M 的 β 延拓且 s=D 等價；
含全部 W 邊／附件及被 effective-H 忽略點的原 full-lift 因子。M 拒絕 β 迫 C 不可著色，
Dvořák 的 blockwise-uniform 刻畫給 `L^D(w_i)=P_Ji`，兩 palette 均含 D，
卻因 J1/J2 在 r 相交而須互斥，矛盾。完整論證只引用原 PROOF§2–5，不新增證明。

**1e 不依賴 BR-SD-1c terminal lemma：** W 接 q／臂內點可破壞末端／無額外 C 邊前提，
接 J3 可佔用其 private witness；J1/J2 的雙 witness 路線仍全保。
不使用 SD-A、H_M 二連通、R27 minor 或一般 cutpoint D 傳遞。
外部版本見[1e SOURCE](../../../../../../audits/2026-10-11-br-sd-1e-337d018b/external/SOURCE.md)。
[controls v3](../../../../../../audits/2026-10-11-br-sd-1e-337d018b/agents/controls/REPORT.v3.md)
僅是固定域機制校準／負控制；actual target source 為 `not triggered`，無新來源實現或 Lean。
紙面任意大小結論、有限 controls 與 byte seal 分層，audit PASS 不擴大來源合同。
逐項映射、驗證與傳播停止見[BR-SD-1f 紀錄](../../../../../history/2026-10-11-br-sd-1f-adoption.md)。
1a／1c／1e 分列排除；一般多旁支、其他三環形狀與完整父身份仍 OPEN。

**BR-SD-1g canonical 採納（2026-10-11，owner APPROVED）：**
紙面定理名稱為 **BR-SD-1g scoped exclusion（雙原旁支／J2 屏障）**，
識別 `BR-SD-1g-DUAL-PENDANT-J2-EXCLUSION`；這是紙面識別，非 Lean 名稱。
原 [PROOF](../../../../../../audits/2026-10-11-br-sd-1g-dbdc4c35/PROOF.md)／
[MAPPING](../../../../../../audits/2026-10-11-br-sd-1g-dbdc4c35/MAPPING.md) 的 candidate 語境與 bytes 保留。
採納依 [獨立 proof review](../../../../../../audits/2026-10-11-br-sd-1g-adopt-6eae3597/REVIEW.md)、
[mapping review](../../../../../../audits/2026-10-11-br-sd-1g-adopt-6eae3597/MAPPING_REVIEW.md)、
[ACCEPTABLE 裁決](../../../../../../audits/2026-10-11-br-sd-1g-adopt-6eae3597/ADOPTION_DECISION.md)、
[最終 bytes acceptance](../../../../../../audits/2026-10-11-br-sd-1g-adopt-6eae3597/final_review/ACCEPTANCE.json)、
[SEAL](../../../../../../audits/2026-10-11-br-sd-1g-adopt-6eae3597/SEAL.json) 及
[REPORT](../../../../../../audits/2026-10-11-br-sd-1g-adopt-6eae3597/REPORT.md)。

**精確定理：對每個任意大小有限簡單原圖 G 及其同一完整具名來源資料，
若下列八項條件全部成立，則此完整原來源合同不可能成立。**

1. G 是 ordered induced-C5 disk，原外框 `B=(b0,…,b4)`；完整有序 `Σ(G)=933／941`
   或共同搬運全部具名原資料的 D5 像，`ε(G)=2`。每條非框原邊 Σ-critical，
   其原刪邊全部完整 witnesses 保留。原有效 H 連通；不相鄰 r/s 是原完整 degree5 roots，
   其餘有效原內點完整 degree4。沿用§1的 full B-touch、one-sided、原 support 非空合同。
2. `H_G−{r,s}=L⊔S` 恰兩份完整原 mixed，原 U=0；L long，**S short** 且其 actual
   boundary support 恰同一真框邊兩端 `T_B={b_i,b_(i+1)}`。全部 W1/W2 原附件分別
   計入完整 L/S 的原 support，不用 marginals／capacity 或另一圖代替。
3. exact-S 只省略 r 唯一原 boundary spoke `e=rb_j`；`V(M)=V(G)`、
   `E(M)=E(G)−{e}` 且 `X=M`，其他全部原點／邊保留。對同一 literal proper 三色 β，
   M 自己拒絕且自己 β inclusion-minimal；保 M 自己全部 retained 非框原邊的同 β
   完整刪邊 witnesses，不以 G 的 Σ-critical 代替。
4. M 中 s 完整 degree5，其他有效原內點完整 degree4；s 的三條原 B-spokes 全留，
   恰有相異有序原內鄰 `p∈L`／`q∈S`。`C=H_M−s={r}∪L∪S` 是實際 sole connected
   component；r split22，對原 L/S 各有兩個原 contacts，在 C 度4、在 M 無 B-spoke。
   45／54 只共同交換 roots roles 和整份原資料。
5. 同一原 C 的骨架 C0 有原 triangle `J1=(r,a1,x1)`、任意奇長≥3的原 cycle blocks
   J2/J3；`J1∩J2={r}`，J3 與兩者不交。原 `u∈J2−{r}` 與 `v∈J3` 間恰唯一原
   環間 bridge uv。p/q 原外臂分別從 J1/J3 私有錨點 a1/a3 開始，是 simple bridge paths、
   長 `h/ℓ≥0`。零長只作 `p=a1`／`q=a3` 原同點身份，允許 `a3=v`；正長臂 off-cycle
   點與原 cycles／另一臂及非本臂具名端點互斥。C0 原邊恰三環、uv 及兩臂，沒有另加骨架邊。
6. `V(C)=V(C0)⊔W1⊔W2`。Wi 各是有限非空 off-skeleton 原內點集，`C[Wi]` 連通，
   `N_C(W1)={x1}`、`N_C(W2)={x2}`，`x2∈V(J3)∪V(q-arm)`。可有多條原 xi–Wi 邊；
   Wi 原內邊及接入邊全保。無 Wi 間邊、第二骨架接點、額外 s-contact、第三旁支、
   其他 blocks 接線或 cross edge。
7. W1 屬同一原 L，W2 屬同一原 S；J1−r／p-arm off-cycle 在 L，J2−r／J3／q-arm
   off-cycle 在 S，uv 全在 S。全部原附件是來源自己的 `A(y)=N_B^M(y)`；逐原點
   `4=d_C(y)+|A(y)|+1[sy∈E(M)]`，不向已飽和舊來源加邊，不為容納 Wi 刪原附件。
   S 所有附件在 T_B 且完整聯集恰 T_B；L 不受此 pair 兩端限制。所有實際 mi 值、
   x2 位置及合法重合皆包含；已超原 degree 的列先結構排除。
8. 所有原 vertices／edges、named／ordered／shared contacts 的單一坐標、actual
   attachments／supports、完整 ownership、原 bridge 身份、rotation／disk embedding、
   同一 literal 四色 Col／β 保留。G/M 各自所有原 witnesses、完整 relations／fibres 含空／
   full lifts 全留；effective-H 忽略的原內圖孤立點也保其原坐標及允許色因子。
   不得獨立正規化 blocks／pieces 或只保 marginals。

以上完整合同涵蓋任意原 J2/J3 奇長、任意 h/ℓ≥0、任意有限非空 Wi 大小，
全部允許 x2／mi 及 a3=v 重合；不把必要 degree／support 配置當成 actual source realization。

**採納的紙面推論：** 同一 β 未用色為 D，actual pair 兩異色外的第三已用色為 T。
對原 y∈C，以完整原鄰居定義
`L^D(y)=Col∖(β(A(y))∪{D:sy∈E(M)})`；完整 degree 式給 `|L^D(y)|≥d_C(y)`。
C list-coloring 與 M 同 β、s=D 的完整延拓存在性等價；完整 lifts 包含被 effective-H
忽略原坐標的允許色乘積，這些 B-only 原點的因子均含 D，無附件原孤立點有整份 Col。
省略這些坐標後的投影不宣稱 bijective。M 自身拒絕 β 迫 C 不可 list-coloring。
有限連通簡單 C 的完整 degree lists 適用外部 Gallai characterization：每個 maximal block
為 clique／odd cycle，有 bridge 大小1、odd cycle 大小2、Kn 大小 n−1 的 palette；
各原點 list 恰為 incident palettes 聯集，共享原點的 palettes 互斥。

原 `w2∈J2−{r,u}` 必存在（含 triangle），未受 W1/W2 影響，非割點、非 s-contact，
原 C-degree2及完整 degree4 迫其兩原附件恰 actual pair，故 `P_J2={T,D}`。
S 除 q 外的每個原 list 含同一 T、D；q 含 T 且禁 D。q 的 incident-union 給一個
含 T 不含 D 的起始 block（只就 T/D 而言）。選 block 的另一原點；該點需要的另一色
由不同 incident block 提供，palette 互斥使它恰含 T/D 的另一色。反覆交替，每步換原點
與 block，不回頭。任何此種 exclusive block 都不能 incident 於 J2 原點，因其必與
`{T,D}` 相交；S 到 L 的唯一接口經 J2／r，故整條 walk 留在原 S 且不碰 r。
有限 all-vertex block incidence tree 不允許此不回頭路徑持續延長。非割點／leaf block
會立即缺色；triangle／K4 同样有不同出口原點。此論證涵蓋任意有限 W2。

W1 可以佔用 J1 唯一 private witness，W2 可以破壞舊 terminal 前提；
本證明不使用已失效的 `D∈L^D(x1)⇒D∈P_J1`，不依 SD-A、H_M 二連通、
BR-SD-1c terminal lemma、R31 minor 或六份 synthetic fixtures 的大小外推。
外部依賴為 [Dvořák 作者講義 degree assignment／blockwise-uniform 及 Theorem10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，
本次獨立審查的版本 hash 見 [FETCH](../../../../../../audits/2026-10-11-br-sd-1g-adopt-6eae3597/agents/proof/FETCH.json)。
Finite controls 只證其具名 synthetic 測例；**actual source NOT TRIGGERED，新增 Lean theorem 0**。
完整 `N45-S-NOU-LS-PAIR` 父身份仍 **OPEN**；**新增完整 OPEN 無條件關閉 0**。
正式採納、歷史 verifier 白名單限制及獨立 immutable adapter 證據見
[採納紀錄](../../../../../history/2026-10-11-br-sd-1g-adoption.md)；歷史資料及既有採納範圍不改。

### 2.12 雙色唯一缺口的共同排除

[雙色唯一缺口的 bridge 路徑定理](../../structure/c5_two_color_single_gap_bridge.md)給出任意大小紙面證明：
有限連通簡單 C 的不可著色 degree lists，若 S 是 C−r 的完整分量、S−{q} 的 lists
均含同一 T/D 而 q 含 T 缺 D，則 r 對 S 恰有一個 contact，r–q 的 blocks 全為原 bridges。
核心是完整 exclusive-block incidence 森林的缺口計數；限制到 S 側後計入出口葉 r，
不假定 r 的原 list 缺色，也不需要先找到一個含 T/D 的 private-witness block。

對§2.11的同一原 M／literal proper 三色 β，以其未用色 D 固定 s=D，保留完整原鄰居
定義的 L^D、逐點 degree-list 不等式與全部原坐標的延拓等價。M 自身拒絕 β 迫 C 不可著色。
S 的全部 actual attachments 在同一異色 pair、s 在 S 恰有唯一原 contact q，
即給上述雙色 lists；S 必是 C−r 的完整分量。故再有 `|N_C(r)∩S|≥2` 就矛盾。
原點／邊、ordered contacts、ownership、attachments／support、rotation、bridges、同一色框、
完整 relations／空 fibres／full lifts 及 effective-H 忽略原坐標的因子全保。

四份 BR-SD-1a／1c／1e／1g 都有這些共同條件與 r split22，逐份映射見
[報告§5](../../structure/c5_two_color_single_gap_bridge.md#5-同一原圖的共同排除與四份-br-接入)。
共同推論涵蓋任意有限旁支與 block 形狀，不再要求三環骨架、旁支數／位置、
terminal lemma 或 private witness。這不把失去完整 S／唯一 q／雙色 lists 的來源納入。

本輪為外部 Gallai 刻畫＋新紙面推論，未另經獨立採納審查、未新增有限來源或 Lean theorem；
四份既有 scoped 合同及其採納證據保留。完整父身份未關閉，驗證與傳播見
[整理紀錄](../../../../../history/2026-10-11-two-color-single-gap.md)。

### 2.13 E-ARC2 接入：N2 的全部原分量必留

[原分量共同限制定理3](c5_excess_two_arc_component_slack.md#5-n2-的全分量必留推論)
在本頁§1完整原來源前提下，先由兩mixed及兩-root44排除得Z=∅。
若省略unit unary U後仍拒絕β，minimal core必保兩roots，degrees只能45／54；
原degree-4飽和迫M=G−U，逐項滿足§2.2已採納的U身份，故矛盾。
Mixed與非unit unary省略則由兩-root44／單-root排除直接全收。

因此每份原C及其每條incident邊e都有Σ(G−C)=Σ(G−e)=Ω，
每個非root內點的原框附件至多兩個、兩個時必相鄰。每個拒絕列的所有minimal cores
皆保留全部原分量；真core只能省一條原root-spoke，否則就是原G的55 core。
這是新紙面合成，沿用已採納U排除；63固定來源的完整fibres控制不含目標來源。
沒有完成剩餘S／55或一般N2／E，亦未新增Lean theorem。

### 2.14 E-ARC2 接入：全部 spoke45／54 排除與原55化約

[新報告](c5_excess_two_arc_spoke_closure.md)從§2.13的每列分量必留取得同一原C的
三列不可染degree lists。Block palette與字面框欄位單射迫普通私有點的原附件相同；
原K₅ minor排除沒有私有root接點的leaf block，亦排除原incidence-one unary。
無U時兩roots在H同一block，其餘leaf blocks皆無root接點，故原H必二連通。

對拒絕的G−rbᵢ用已查證SD-A，迫s三spokes；其中某pair在原拒絕三列之一重色，
故另一側G−sbⱼ仍拒絕。其內圖仍是同一H，再用SD-A迫r亦三spokes。
原雙star長面的交集容不下long支援，兩mixed都short後以未用色D的完整diagonal lifts
接回G，矛盾。這完成無U全部exact-S，沒有借44分類或假定跨列pins相同。

含U的exact-S逐項窮盡：至少兩U用S05；一U兩long用原盾弧6>5；一U兩short用§2.8；
一U一long一short逐項符合完整K1–K12，按owner接§2.9／§2.10。因此本頁§1的
S與U兩個原省略身份均全排；§2.13又已證每個N2真core必為S，故只剩原55。

精確結論為每條非框邊e都有Σ(G−e)=Ω。每個拒絕列的唯一minimal core是有效原G；
連roots在內每個內點至多接兩個相鄰框點。新結果為紙面證明／既有採納合成，
兩路只讀檢查核對論證並補明自由孤立因子慣例，未另作封存採納流程。
63圖控制只核完整local fibres，目標0觸發；外部Gallai、SD-A及N45上游信任链明列於報告，
沒有新Lean theorem、原55矛盾或N2來源排除。

### 2.15 原55的block骨架與有效內點上界

[新報告](c5_excess_two_arc_size_bound.md)在§2.14的完整N2前提下，進一步證H只有
含兩roots的中央block，以及各root至多一個unary葉block；H無bridge。
內度二點同接一條原框邊時，同block以共同cycle給K₅，異block以連通H−{u,v}給K₃,₃，
故全H至多五個內度二點。每份原C的連通外部hub排K₄，剩bridges／奇環cactus。
以完整root incidence與原block計數，得`|H|≤35−6u−3t`，u為unary數、t為原root-spoke總數。
這是原圖上界，不替換完整relations或縮圖；自由孤立座標仍保留完整染色因子。
新紙面必要條件尚未另作封存採納或Lean化；63固定圖及570份具名minors不含目標來源。
沒有把至多35點寫成來源排除，亦未擴大ES／ER來源搜尋。

### 2.16 原55共同容量、singleton hub排除與上下界

[N2九格統一報告](../n2/c5_excess_two_n2_residual_unification.md)對回三族乘三core層：
原輪六格真core已有覆蓋；後續§2.17排第三族原55，現七格已有覆蓋。
另兩族原55仍OPEN；後續§2.18排含U的(1,1)，參數情形剩(1,0)及(2,0)。每列每欄的原55容量統一為
`Dᵘ+δ+o+λ=1`，Oᵘ=0；不能沿用45降度側的零容量。
共同三-hub引理排有unary或root-spoke時的singleton mixed，故singleton迫u=t=0。
两unary時兩short都須為pair，盾弧6>5，獨立核對後排此原55子族，得u≤1。
一U／一long／一short的實際盾弧恰2+2+1，仍只為必要模板。

原大小界保全部cactus鬆弛為`|H|=35−6u−3t−Δ`；既有ES／ER有限覆蓋給反例
有效內點至少10，原u/t域的上界仍不低於20，故無直接大小矛盾。
条件Δ≥26−6u−3t才与有限下界衝突；仍缺一般來源必達該門檻或三列joint不能皆空。
新結果是紙面推導與獨立核對，局部算術控制非來源排除，沒有新Lean或10–35點搜尋。

### 2.17 一U兩short的三列D escape採納與限定long化約

[新候選](../n2/c5_excess_two_n2_unary_three_row_escape.md)由完整原degree5及兩mixed正incidence
先得原U恰2或3條owner接線；用原Gallai palettes、leaf-block私有contacts、
H內度二附件單射及三列字面signatures，完整覆蓋任意大小的單block／兩leaf／三leaf，
推出同一U至少在q₀/q₁/q₃之一允許owner=D。
後續[獨立採納與diagonal報告](../n2/c5_excess_two_n2_diagonal_three_row.md)已核對無界case split，
以兩short該同一列的完整(D,D) lifts排(ℓ,u)=(0,1)，與u=2合成第三族原55全排。
另證原mixed共享接點使全部同色pins可接回；原long接點總數≤3有一指定列完整出口。
因此一long無U的共享／低接點子域已排，含U的共享long亦排；其餘同列同步仍缺。
97原U全fibres及63原整圖joins經獨立重算一致，42局部前提triggered and holds；
target not triggered，沒有新來源或Lean。原55全族／N2／E-ARC2仍OPEN。

**後續 long 推進**：[同列同步與葉接點 tree](../n2/c5_excess_two_n2_long_synchrony.md)
另排兩 long 都 k≤3、無 U 的全葉接點 tree long（任意k），以及含 U 低接點
Eq／Diff 異類 masks。非空同類只剩七個必要字面弧模板。完整 fibres／joins
重播與紙面獨立採納分層；四接點 path 三列全拒的局部反控制保留，父族仍 OPEN。

### 2.18 兩接線 U 的全色 Diff 出口與含 U 原55排除

[接口分割與已用色規律](../n2/c5_excess_two_n2_partition_rule.md)合原55容量排三接線U，
並排七個同步模板，完整(1,1)剩兩接線U及三點弧支援。
[新全色出口](../n2/c5_excess_two_n2_unary_diff_closure.md)以原block-tree私有contacts與
兩條框邊附件容量，任意大小化約為五原形；任一Diff列拒絕只可能是六點barbell，
其精確原附件給K₅ minor，故planar U在該列每個owner色都有完整lift。
固定同一列G−U完整染色的實際ownerpin接回，排完整原55(1,1)，不限制long接線數。
與(0,1)及u=2既有覆蓋合成，完整目標原55必u=0、H二連通。
九格仍七格，因第二relation格仍含(1,0)；剩(1,0)/(2,0)，父N2／E-ARC2 OPEN。
任意大小紙面＋獨立審查，完整控制target not triggered，無新Lean／來源搜尋。

### 2.19 一 long 的末端 block 與完整外側接回

[一long来源排除](../n2/c5_excess_two_n2_one_long_closure.md)在完整原55的(1,0)中，
以原框弧K₅排任意長leaf cycles；全色同pins接回、leaf bridge minor及附件單射
迫兩個具名四spoke配置。固定一個root後，另一root在原S加root中有strict list
slack，完整外側染色再接回L，排除兩型。沒有內部長度cutoff，也不壓縮四／五點
完整具名接口。合§2.18，九格八格已有覆蓋，完整原55只剩(2,0)；N2／E-ARC2 OPEN。

### 2.20 LL-CUT+diag 與指定完整Σ契約的原55全覆蓋

[LL-CUT+diag](../n2/c5_excess_two_n2_ll_cut.md)保留§1的完整Σ933／941或共同D₅像契約，
以原leaf K₅／K₃,₃ minors、同來源接線容量及完整diagonal lifts排最後原55 `(ℓ,u)=(2,0)`。
合§2.17–2.19的含U與一long排除，指定完整契約的三relation族乘三core層九格均已覆蓋。
這是任意大小的來源排除；有限目標仍not triggered，沒有新Lean theorem。

基本LL-CUT尚未獨立證成：本輪沒有證明基本contact／框碰色／shared diagonal cuts
本身必觸發矛盾。19,229份共同可行投影只屬抽象介面控制，不是來源實現或LL-CUT反例。
原E4三列來源在該輪未涵蓋的前提橋接，另由下一節承擔。

### 2.21 N2-BRIDGE：原E4三列契約與932來源排除

[N2-BRIDGE](../n2/c5_excess_two_n2_bridge.md#1-真正的前提差異)另證完整mask 932，
連同既有933／941及整圖共同反射的940，排除**原E4三列完整來源契約的廣義N2**。
原契約仍要求ordered induced-C₅ disk、T4全收、每條非框邊對完整Σ critical、ε=2、
非相鄰原degree5 roots及其餘有效內點原degree4、恰兩份原mixed，並拒絕q₀／q₁／q₃；
全部具名原資料、同一色框、完整relations／空fibres及full lifts照留。

932不能直接引用本頁完整Σ排除。該報告以U4三列移植、五列slack與原分量刪除witness
另補CW橋接，再逐項接回含U、OL及LL-CUT+diag來源排除；原前提帳本與全證明由其§1–2承擔。
本頁§1及舊採納的契約保持原範圍。對父題的實際覆蓋見
[N2-BRIDGE父分類](../n2/c5_excess_two_n2_bridge.md#3-接回父分類與剩餘來源)：
932原在E-ARC2的`1≤|Q|≤4`域外；E-ARC2剩N1及相鄰m=0／1／2來源，仍OPEN。

## 3. 精確 OPEN 與下一個窄分支

**指定完整Σ契約的九格來源排除已完成；原E4三列完整來源契約的廣義N2亦已排除。**
前者沿§2.2、§2.13–2.14完成全部45／54真cores，再由§2.17–2.20排原55；
後者由§2.21另橋接932。本頁§1的完整Σ前提及N45各具名採納契約照留。

反設原55來源時曾推出的每條非框邊刪除全收、唯一有效原G核心、框附件相鄰pair、
含U全排後的u=0／H二連通及`|H|=35−3t−Δ`等，都是來源排除鏈中的必要條件；
它們不再構成本契約內的存活來源清單。

| 來源身份／義務 | 目前狀態 |
| --- | --- |
| §1 exact-U及exact-S；完整N2目標契約的全部45／54真cores | 紙面排除完成；既有採納＋§2.14新共同證明，未Lean化 |
| N45-S-NOU-LS-PAIR、無U兩long及其原split／旁支子型 | 作為§1 exact-S均由§2.14涵蓋；不再以一般非二連通形狀列為此域存活理由 |
| BR-SD-1a／1c／1e／1g、雙色唯一缺口 | 原限定採納／任意大小共同引理保留；封存bytes及當時OPEN語境不改 |
| 指定完整Σ契約的原55，沒有45／54的N2來源 | §2.18排含U、§2.19排(1,0)，§2.20排最後(2,0)；九格全覆蓋 |
| 原E4三列完整來源契約的廣義N2，包括932 | §2.21的N2-BRIDGE另補前提與witness後排除；未把舊完整Σ證明擅自推廣 |
| 基本LL-CUT的獨立cut必觸發機制 | 尚未獨立證成；LL-CUT+diag的來源排除不承擔此義務 |
| E-ARC2的N1與相鄰m=0／1／2來源 | OPEN；保留未排的45／54、原55及原分類允許的單-root4例外，扣除各權威報告已排具名子域 |
| 本頁及原E4來源契約外的其他來源 | 不作推廣；其各自義務與證據範圍保留 |
| 一般degree5／R31任意長來源minor | OPEN；本輪N2排除不補該一般minor路線 |
| E-ARC2、一般單側／共同出口、主命題及K∞=K≤5 | OPEN |

只指定三列不能自動提升為完整Σ933／941契約；N2-BRIDGE是另證932與前提移植，
保留原E4完整來源契約，並非刪除舊引理的前提。父題剩餘來源見
[N2-BRIDGE覆蓋表](../n2/c5_excess_two_n2_bridge.md#3-接回父分類與剩餘來源)，
跨線缺口見[Kempe導覽§3](../../../../guides/c5_kempe_guide.md#3-停止點與保留缺口)。
原雙long的同列joint已由LL-CUT+diag完成，沒有新增Δ門檻；基本LL-CUT仍可另行研究。
未搜尋10–35內點，不能把SD-A直接套到雙degree5的G，亦不能先假設三點弧取得缺條件。
§2.11的歷史block-chain缺口及B適用性表不再是本頁完整N2 exact-S的存活清單；
它們在一般degree5／其他來源合同中的方法義務仍由
[degree-5導覽](../../../../guides/c5_degree5_guide.md#4-r31-保留缺口與重播入口)維護。
有限目標來源仍not triggered，沒有由控制圖數量推得來源排除。

## 4. 證據、重播與保留失敗

2026-10-11的四份獨立review及DIRECT／FIBRE／JOINT封存保持原bytes；
本輪文件採納是其後的研究狀態更新，舊review的shared_documents_updated=false保當時語境。
採納後不重跑要求live shared pins／tracked diff不變的歷史worker checker。
以下read-only入口核新review完整payload，不以封存PASS裁定紙面；完整命令、
本輪文件／Lean檢查與刻意未重跑項目見[收尾紀錄](../../../../../history/2026-10-11-n45-s-long-s-adoption.md)。

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

此入口核artifact／採納custody，不以tool證paper；完整範圍見[監督報告](../../../../../../audits/2026-10-10-n45-high23-supervision/REPORT.md)。

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
完整範圍與停L2記錄見[HIGH1監督報告](../../../../../../audits/2026-10-10-n45-high1-supervision/REPORT.md)。

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
由[SS監督補充清單](../../../../../../audits/2026-10-10-n45-ss-supervision/ssg-supplement.sha256)與fulltree另綁，四項幾何裁決不變。
LOW1 strict verifier在新增監督／稽核目錄前 normal／seed17各exit0、6049 regular／5 symlinks核回；
L1C另核12 BASE／6 pins／10 final-v4 receipt metadata及七項工具負控制。
四個nested repos初始僅核目錄存在，未遞迴hash；不報完整工作樹零漂移。
worker checks.json 的舊v1索引保留，最終成功以 delivery.json 明綁的 final-v4為準。
L1A三個section索引、空fibre與L1R一般γ記號由監督明列精化；L1R首封nested delivery漏列的FAIL及final-v2亦全保留。
全部 finding、父端實跑與封存版本見 [LOW1監督報告](../../../../../../audits/2026-10-10-n45-low1-supervision/REPORT.md)。
LOW2 strict verifier在新增本輪目錄前 normal／seed17各exit0；66 payload／0 symlinks，
19個精確排除及 manifest→delivery、receipt→16 logs完整綁定，四BASE／八pins／20frozen inputs核回。
L2C獨立重播六原工具負控制及追加 nested receipt省略控制，全部exit2命中預期階段。
原 bad-receipt封存probe使用synthetic override；父端與L2C另用正式delivery直接核拒絕，兩層明列。
L2R的240 literal rows／61,440 ambient fibres是抽象 joint語義校準，沒有 LOW2 source／trigger數。
本輪三稽核的完整receipt normal／seed17父端重播一致；四nested repos仍無遞迴內容hash，
新增目錄後改核frozen證據與父端custody，不宣稱worker舊live-inventory仍適用。
完整 scope與既存 FAIL見[LOW2監督報告](../../../../../../audits/2026-10-10-n45-low2-supervision/REPORT.md)。

```sh
python3 -B audits/2026-10-09-n45-su-j/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-09-n45-su-j/checker.py --check
```

輸入 provenance、封存 hashes、每個 exit／log 見 [監督採納](../../../../../../audits/2026-10-09-n45-su-supervision/REPORT.md)。
兩個歷史 E4 byte replay FAIL（E3 REPORT provenance 差異）、fresh BASE 的兩份歷史缺檔及
whole-worktree DocGraph duplicate IDs 保留；正式 docs PASS 不表示全工作樹 PASS。
目前停止點亦見 [Kempe導覽](../../../../guides/c5_kempe_guide.md#3-停止點與保留缺口)。
