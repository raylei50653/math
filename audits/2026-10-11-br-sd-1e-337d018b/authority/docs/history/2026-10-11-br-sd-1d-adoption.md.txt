# 2026-10-11：BR-SD-1d 單一原旁支 canonical 採納與 residual 對帳

本輪為 adoption／reconciliation：將已獨立紙面審查、封存及發布的 BR-SD-1c 精確排除
接入 [N45 canonical§2.11](../c5_excess_two_nonadjacent_unit_core45.md#211-單缺額查證與無-u-二連通子域)。
沒有重證1c、擴大數學結論、新枚舉或 Lean theorem；1a／1b 與原 audit 全部唯讀。
起始 actual HEAD、origin/main、`git ls-remote origin refs/heads/main` 均為發布基準
`46cd053b2b320d380eb0ee9326bf126551dd8a41`，工作樹乾淨，沒有後續 HEAD 成果須避讓。
1c 的研究 BASE `fd6e1112e6f5e9fd23c50d2f3b5d2ef874954d69` 是原 provenance，不是本輪基準。
[PUBLICATION](../../audits/2026-10-11-br-sd-1c-fd6e1112/PUBLICATION.md) 說明原 REPORT 的未採納／未發布
文字屬 audit 當輪；本輪不改寫其歷史欄位。文件 diff 留在工作樹供 owner 審查，未 commit／push。

## 採納前獨立核對與精確 scope

讀取 HANDOFF、DOCUMENTATION、STATUS、N45§1／§2.11／§3、degree-5 guide§4、
interfaces§7 及 [1b 歷史](2026-10-11-br-sd-1b-adoption.md)，逐項對照1c的
[REPORT](../../audits/2026-10-11-br-sd-1c-fd6e1112/REPORT.md)、
[最終 PROOF](../../audits/2026-10-11-br-sd-1c-fd6e1112/PROOF.md)、
[MAPPING](../../audits/2026-10-11-br-sd-1c-fd6e1112/MAPPING.md) 與
[REVIEW.final-v2](../../audits/2026-10-11-br-sd-1c-fd6e1112/agents/paper/REVIEW.final-v2.md)。
本輪獨立核對未發現阻止該精確範圍採納的必要前提映射缺口。

| 完整原合同 | 封存證據映射／本輪裁決 |
| --- | --- |
| 同一原有限簡單 ordered induced-C5 disk G，完整 Σ933／941 或共同整圖 D₅ 像、ε=2、原 Σ-critical 與全部 witnesses | N45§1；PROOF§1、MAPPING§1／§6 全保，未以固定 β 取代完整 Σ |
| 原非相鄰 degree5 roots r/s，其餘有效原內點完整 degree4 | PROOF§1–3、MAPPING§1／§3；W 原點也須完整度4 |
| exact-S 僅省略 r 唯一原 spoke，X=M=G−e 自身拒絕同一 proper 三色 β、自身同 β inclusion-minimal 與 retained-edge full witnesses | PROOF§1／§3、MAPPING§1／§6；不從原 G 遺傳 minimality |
| 原 U=0、L long、S actual support 恰真框邊兩端 | PROOF§1／§6、MAPPING§1／§5；raw support 定義為整份原 piece 的全部 B 鄰居聯集 |
| sole C、r split22、三原 odd-cycle blocks J1/J2/J3、J1∩J2={r}、不交 J3、原 uv bridge、p/q 外臂及 a1/a3 | PROOF§1、MAPPING§2；u≠r，允許 a3=v，任意奇環長≥3及外臂長≥0 |
| 恰一份有限非空原 pendant W 只在具名 x∈J1/J2 接骨架，無額外 s-contact、cross edge 或其他接線 | PROOF§1–2、MAPPING§2–4；J1／J2 側 W 分屬完整原 L／S，繼承其全部附件合同 |
| J3／q 外臂的原附件及接線限制，全部 relations／fibres／ownership／rotation／full lifts | PROOF§1／§3／§6、MAPPING§1／§5；正長 q 為 C 末端，a3 以外臂點無額外 C 邊，孤立自由原點的 full-lift 因子保留 |

W 採 PROOF 的 off-skeleton 內點約定，非空連通且 `N_C(W)={x}`；
MAPPING 的 W 含 x，故兩者由 W 與 W∪{x} 對應，原 vertices／edges／附件完全相同。
不能把旁支解讀為向已完整 degree4 的舊圖任意加邊或刪附件。

**採納結果：** N45-S-NOU-LS-PAIR、split22、原三環單 bridge 骨架，保 actual S pair support
及未改動 J3／q 外臂時，一份原有限非空 W 只接 J1/J2 的完整來源合同不可能成立。
任意奇環長、p/q 原外臂長、有限 W 大小與所有允許具名接點均涵蓋。

## 紙面路徑、局部引理與證據層

本輪核原任意大小論證，未新增證明：

| 原路徑／分支 | 核對結果 |
| --- | --- |
| 原 degree 限制 | PROOF§2：r 的四環邊已飽和，不能接非空 W；a1／u 只容首 W bridge，其他私有點最多兩條 W incident 邊；必要 degree 可行不等於 disk 實現 |
| 兩個 private witnesses 保留 | PROOF§4：未接入環必有 witness；接入環長≥5或 x 是原 a1／u 時仍有，非割點、非 s-contact 各迫本環 palette 含同一 D，與 r 的互斥矛盾 |
| J2 triangle 唯一 witness 被耗盡 | PROOF§5：未動 J3 的 private witness 迫 D∈P_J3，故 D∉P_uv；u 只 incident J2／uv 且非 s-contact，合法 routing 迫 D∈P_J2，與 J1 矛盾 |
| J1 triangle 唯一 witness 被耗盡 | PROOF§6：以未動 J3／q 臂的 actual pair-supported terminal lemma 排除；該路徑同時涵蓋其他 degree 合法接點，不將 D 傳給割點的所有 palettes |

局部引理獨立使用時仍須完整前提：同一原 M／三色 β、未用 D、連通 C 的 degree lists
及不可著色；原奇環與原 q 臂全部 B 附件位於同一真框邊兩個異色框點；
其他 block 接入只在 v／a，保私有非 contact 環點；q 為該側唯一 s-contact；
外臂是 simple bridge path，a 以外全部臂點（含末端 q）只有原路徑 C 鄰居。
本輪 J=J3、a=a3；不另假定 a3≠v。正長時 q 的 d_C=1、內點 d_C=2。

| q 原外臂長 | 原附件／palette 核對 |
| --- | --- |
| 0 | q=a3 禁 D，但原 J3 私有點迫 P_J3={T,D}⊆L^D(q)，矛盾 |
| 1 | q 的兩個原 B 附件恰 pair，L^D(q)={T}；首 bridge palette={T} 與 J3 在 a3 不互斥 |
| ≥2 | 首 off-cycle 臂點非 contact、C-degree2，兩 B 附件恰 pair，list={T,D}；首 bridge 非空 singleton 包含於該 list，與 P_J3 在 a3 不互斥 |

三案完整涵蓋任意非負臂長；不能省去正長末端 q 無額外 C 邊的前提。
原精度 finding、PROOF.reviewed-v1／v2、舊 REVIEW 及負控制全保留。

外部依賴為 [Dvořák 作者講義 Theorem10／blockwise-uniform 定義，印刷頁6](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)；
已核作者 PDF 的原定理與同頁定義，現下載164927 bytes與 [1c frozen PDF](../../audits/2026-10-11-br-sd-1c-fd6e1112/external/gallai.pdf)
逐 byte 相同，SHA256 `50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea`。
[SOURCE](../../audits/2026-10-11-br-sd-1c-fd6e1112/external/SOURCE.md) 保存原依賴 provenance；講義不是期刊論文或 Lean theorem。

最終 PROOF／REPORT 的 SHA256 分別為
`abbdfcd48eadb2e2ca56ad74802c4ca21a98394d54b8b114aec27ebc58a5c4f0`／
`937262167c4011abec6f2297ec26468a07e028b7bb4d058fd16bcae7917e86ec`，與 REVIEW.final-v2 的接受 bytes 相符。
[controls REPORT.v2](../../audits/2026-10-11-br-sd-1c-fd6e1112/agents/controls/REPORT.v2.md) 的四份 synthetic M
前三份完整 β lifts=54／12／48、皆接受 β；第四份0、拒絕但 S 使用三框點，違 actual pair support。
原邊／lists／完整 fibres／lifts、private-witness／routing 校準為 `triggered and holds`；
「cutpoint list 含 D ⇒ 每個 incident palette 含 D」為 `counterexample`；
actual disk／完整 Σ／minimality／完整來源合同均 `not triggered`，無新 source realization。
normal／seed17 證書 hash `0b2193d4d13f715272f78f3df2431aca915efd2dd77f60ef52de3549d230906a`
及1→9損壞 tuple、歷史 REPORT 原色誤記與修正版均沿用原封存，本輪未重跑 controls。
有限校準與 seal 只核既有證據；任意大小排除由紙面 PROOF／獨立審查承擔，無新 Lean。

## Residual 與 OPEN／CLOSED 對帳

| 來源身份／義務 | 本輪後狀態 |
| --- | --- |
| BR-SD-1a 無旁支精確子域 | 既有 Scoped exclusion 保持；1b 採納不重開 |
| BR-SD-1c 一份原 W 只接 J1/J2，保 actual S pair 及未動 J3／q 臂 | 本輪採納 Scoped exclusion；該精確子域排除完成，無父身份 closure |
| 可重用 pair-supported terminal lemma | 僅在上列完整局部前提下採納；不作一般來源域 CLOSED 宣告 |
| 完整 N45-S-NOU-LS-PAIR、其他 split22／非 split22、無 U 兩 long | OPEN |
| 一份 W 接 J3／q 外臂、或多份旁支 | OPEN |
| actual pair support 不成立或 terminal lemma 任一必要前提失效 | OPEN |
| 其他 bridge-separated 三環、不同接點位置、更多奇環、一般 Gallai block tree／非二連通來源 | OPEN |
| R31 任意長來源 minor | OPEN，正常形證書不補來源 minor |
| 其他45／54、原55、無45／54來源 | OPEN |
| 一般 N45／N2／E、ε≥3、一般單側／共同出口、主命題及 K∞=K≤5 | OPEN |

**完整 OPEN 身份新增無條件關閉數仍為 0。** 既有 LOW／HIGH／LONG／U 排除保持其完整合同，未重開。

## 文件傳播核對

依 [DOCUMENTATION](../DOCUMENTATION.md) 與只讀即時 [Issue #4](https://github.com/raylei50653/math/issues/4)
的文件責任／L0–L3 規則核 direct consumers。Issue 為 OPEN、updatedAt=`2026-10-08T16:32:54Z`、無 comments；
本輪沒有外部寫入。ordinary file search 已足以辨認關係，未使用 Graphify 或 sub-agents。

Updated：N45 頁首／採納表／§2.11／§3，新增精確1c與局部引理界線、分列1a及殘留；
degree-5 guide§4 的已採狀態與1e義務；interfaces§7 的1c接續與停止點；
Kempe guide 相關狀態列／§3；STATUS 對應直接索引／短狀態／歷史連結；本紀錄。

Reviewed-unchanged：N45§1與既有 LOW／HIGH／LONG／U 合同未受本排除影響；
interfaces§2 的一般 palette 語義與四-query／M-query 分工保持；
直接 consumer Phase B§2.1／§3.2／§4 只使用既有支援／容量與 U 身份結果，無 U 的完整父域仍 OPEN；
1a／1b 與1c所有 frozen audit／review／證書／hash／歷史失敗／負控制不改。
HANDOFF／DOCUMENTATION 的現有入口、研究線與責任無變更；README 未觸發更新。

Remaining OPEN：上表全部父身份／未涵蓋來源與1e義務。
Propagation stop：完成 L0／L1及直接父主題／consumer 的 L2 核對；scoped exclusion 未關完整父身份，
上層語義與研究線／活躍 tag 未變，不擴至 L3、synthesis 或全域路由，不新增平行權威總帳。

## 驗證與操作邊界

修改文件前已執行發布後適用的1c frozen verifier，不使用綁原 HEAD 的 `--live`。

| 實際命令 | Exit code | 範圍／結果 |
| --- | --- | --- |
| `python3 -B audits/2026-10-11-br-sd-1c-fd6e1112/verify.py --check` | 0（修改前／後） | 81 sealed payloads、17 frozen authority inputs與 BASE blobs，live=false |
| `python3 -B audits/2026-10-11-br-sd-1a-0f181045/verify.py --check` | 0（修改前／後） | 65 sealed payloads、14 authority inputs與 BASE blobs；actual_head 為歷史 provenance |
| `python3 -B scripts/check_docs.py` | 0 | 601 Markdown、7,384 local links；anchors／index／HANDOFF 通過 |
| `python3 -B tools/docgraph --include 'docs/**/*.md' check` | 0 | 62 documents、213 relations、5 families，0 errors／0 notes；僅正式 docs |
| `git diff --check` | 0 | 本輪 tracked diff whitespace 通過 |

修改前另核1c authority.json 的原1a custody 89檔，SHA256／size 全相符；
兩份 audit 目錄的全部204檔、8,207,810 bytes 前後 SHA256／size／mode／路徑清單完全相同，
只讀 custody 核對 exit0，無新檔、缺檔或漂移；涵蓋原 frozen payloads、證書、hash、review、
歷史失敗、負控制及 publication receipts。未改其他既有 audits 或1b歷史文件。
完成後 HEAD／origin/main／遠端 main 再讀仍同為 `46cd053b…`，Git index 無 diff；
工作樹只有五份既有 live docs 變更及本份新增歷史紀錄。

未執行：原1a／1c `--live`（發布後 HEAD／index／canonical drift 不適用）；
綁五份舊 live provenance 的1c controls checker／seed17／independent_edges 重播；
大型來源枚舉、全部 finite controls、來源搜尋、全工作樹 DocGraph與 Lean build。
若需重播 controls 應回發布 snapshot，不能為求 PASS 改 frozen bytes。
本輪沒有 verifier 失敗或數學證據漂移 finding；沒有以 byte PASS 取代紙面審查。

## BR-SD-1e 的窄研究義務

下一輪只考慮同一原骨架的一份新增原 W 接 J3 或 q 外臂的具名子域。
沿 [1c PROOF§6](../../audits/2026-10-11-br-sd-1c-fd6e1112/PROOF.md#6-路線-b2保-actual-pair-support-的局部末端引理)、
MAPPING§3／§5及原抽象反例，先核 actual pair support、degree、未佔用私有環點、
臂的 bridge 身份、正長 q 末端無額外 C 邊等哪一條必要前提首先失效；
再問其他 private witness 或合法 palette routing 能否恢復矛盾。
完整原 G／Σ與 witnesses、M 自身同 β minimal、原 contacts／附件／ownership／rotation／完整 lifts
仍是依賴入口，不能只提供抽象 palette。當前入口由 [degree-5 guide§4](../c5_degree5_guide.md#4-r31-保留缺口與重播入口) 維護。
本輪只記錄此義務，沒有開始新證明、指定新來源或枚舉。

## 採納文件發布階段

採納審查交付後，owner 明確授權「整理後 commit + push，只提交 BR-SD-1d 這六份相連文件」。
本階段只發布 N45 canonical、degree-5 guide／interfaces、Kempe guide、STATUS 與本紀錄。
原 audit／review／證書／hash／歷史失敗／負控制保持原 bytes，1a／1b 歷史及 archive 不改。
本階段不新增數學採納或 Lean 宣稱；完整 OPEN 身份新增無條件關閉數仍為0。
發布前重跑「驗證與操作邊界」所列五項命令，並對回兩份 audit 全部204檔的 custody 清單；
stage 與提交均以這六份文件為白名單。發布結果以實際 commit、HEAD／origin/main／遠端 main
及工作樹回讀為準。前述未 commit／push、46cd053b 與工作樹欄位保留原採納審查時點。
