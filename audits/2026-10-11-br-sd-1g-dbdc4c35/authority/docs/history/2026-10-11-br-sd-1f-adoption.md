# 2026-10-11：BR-SD-1f J3／q 外臂單一原旁支 canonical 採納與 residual 對帳

本輪為 adoption／reconciliation：將已獨立紙面審查、封存及發布的 BR-SD-1e
接入 [N45 canonical§2.11](../c5_excess_two_nonadjacent_unit_core45.md#211-單缺額查證與無-u-二連通子域)。
沒有重證1e、新枚舉、擴大來源排除或新增 Lean theorem。起始 actual HEAD、origin/main、
`git ls-remote origin refs/heads/main` 均為發布基準 `0edb05b42d7b096103cdf241df7fb81e08dc16c7`，
工作樹乾淨，沒有 HEAD 前進的其他成果須避讓。
1e 研究 BASE `337d018bfaddfe6b39f7cdc3f3c8ec8bc7c4075f` 保持原 provenance；
發布 commit 的內容與說明已核，原 REPORT／MAPPING／REVIEW／final.json 的 candidate、
待 owner、未發布文字屬原 audit 時點，不改 frozen bytes。
本輪授權採納文件；diff 留在工作樹供 owner 審查，未 commit／push。

## 採納前獨立核對與逐項映射

已讀 HANDOFF、DOCUMENTATION、STATUS、N45§1／§2.11／§3、degree-5 guide§4、
interfaces§2／§7、Kempe guide、unary shield§1，以及 [1d 採納基線](2026-10-11-br-sd-1d-adoption.md)。
對照1a／1c原證明及既採合同，逐項核1e的
[最終 PROOF](../../audits/2026-10-11-br-sd-1e-337d018b/PROOF.md)、
[MAPPING](../../audits/2026-10-11-br-sd-1e-337d018b/MAPPING.md)、
[REPORT](../../audits/2026-10-11-br-sd-1e-337d018b/REPORT.md)、
[獨立 REVIEW.final](../../audits/2026-10-11-br-sd-1e-337d018b/agents/paper/REVIEW.final.md) 與
[ACCEPTANCE](../../audits/2026-10-11-br-sd-1e-337d018b/agents/paper/ACCEPTANCE.json)。
本輪未發現阻止上述精確 scope 採納的必要前提或版本映射缺口；審查 PASS 不放寬合同。

| N45 原合同／核對義務 | 1e 封存映射及本輪裁決 |
| --- | --- |
| 有限簡單 ordered induced-C₅ disk 原 G，完整 Σ933／941 或整圖 D₅ 像、ε=2、逐非框邊 Σ-critical及原 full witnesses | N45§1、PROOF§1.1、MAPPING§2全保；固定 β 不取代完整 Σ |
| 原非相鄰 degree5 roots r/s，其餘有效內點完整 degree4 | PROOF§1.1／§2、MAPPING§2／§4–5；W 原點同樣須完整 degree4 |
| 原 U=0、L long、S actual support恰同一真框邊兩端 | PROOF§1.2／§2、MAPPING§2–3；support為整份原 S 的全部 B 鄰居聯集，恰 pair，不只是逐點 subset |
| exact-S 只省略 r 唯一原 boundary spoke，X=M=G−e自身拒絕同一 proper三色 β、對 β inclusion-minimal與原 retained-edge witnesses | PROOF§1.3、MAPPING§2；不從 G 的 Σ-critical遺傳 M-minimality |
| M僅 s完整 degree5，其餘有效內點4，原 p/q contacts及三原 s-spokes全留 | PROOF§1.3–4、MAPPING§2；G roots=5/5、M roots=4/5，共同交換45／54全部資料 |
| sole C=H_M−s、r split22、三原 odd-cycle blocks、J1∩J2={r}、不交 J3、原 uv及 p/q外臂 | PROOF§1.4–5、MAPPING§3；u≠r、私有 a1/a3，奇環長≥3、臂長≥0、允許 a3=v |
| 恰一份有限非空原 W只接具名 x∈J3／q-arm，無 cross edge、W–s或 J1/J2接線，繼承 S pair-support | PROOF§1.6、MAPPING§3–5；off-skeleton W連通，N_C(W)={x}，可有多條 x–W邊；全部 C恰骨架加 W |
| 所有原 contacts、attachments、ownership、rotation、邊、共同色框、完整 relations／fibres含空與 full lifts | PROOF§1.7／§4、MAPPING§2／§7；孤立 B-only點從原剩餘 list填色，真正無鄰居點才任填 Col，原 lifts坐標／因子全保 |

PROOF與MAPPING均以 W為 off-skeleton原點集、分支子圖為 C[W∪{x}]，版本定義一致。
W是候選原來源自己的結構，C0只是同一原 C內骨架；不是向已完整 degree4的舊圖任意加邊。
原實際 A(x)=N_B^M(x)不得縮減；degree容量不是 disk／Σ／minimality來源實現。

**採納結果：** 僅 N45-S-NOU-LS-PAIR／split22／原三環單 bridge骨架、恰一份來源自己的
有限非空 W唯一接 J3／q外臂，保同一原 G／M、actual S pair、完整 degree與全部原資料時，
該精確來源合同不可能成立。全部允許接點、任意三環奇長、p/q外臂長、有限 W大小及允許具名重合均涵蓋。

## Degree、private-witness preservation及外部刻畫核對

對原 x，m=|N_C(x)∩W|≥1、k=|A(x)|、t=1[sx∈E(M)]，
同一原 M給 `4=d_C0(x)+m+k+t`；以下為 PROOF§2／MAPPING§4的窮盡核對，未新增證明。

| 原 x／q臂長 ℓ | d_C0／t | 必要預算 |
| --- | --- | --- |
| a3=v，ℓ=0，亦即 q=a3=v | 3／1 | 已飽和，非空 W結構排除 |
| a3=v，ℓ>0 | 4／0 | 已飽和，非空 W結構排除 |
| v≠a3，任意 ℓ | 3／0 | m=1、k=0 |
| a3≠v，ℓ=0，q=a3 | 2／1 | m=1、k=0 |
| a3≠v，ℓ>0 | 3／0 | m=1、k=0 |
| J3−{v,a3}，任意 ℓ | 2／0 | m=1、k=1或 m=2、k=0 |
| off-cycle q，ℓ>0 | 1／1 | m=1、k=1或 m=2、k=0 |
| q-arm內點，ℓ≥2 | 2／0 | m=1、k=1或 m=2、k=0 |

ℓ=0無 off-cycle臂點；正長臂點互斥於 cycles及其他臂，無其他命名重合漏列。
所有 k須吻合來源自己的原附件，不能刪 boundary attachments容納 W。
W每點無 s-contact且 pair給 k≤2，須 `d_C+k=4`，所以 `2≤d_C≤4`；degree1 W葉不合法。

| 原紙面核心 | 本輪核對結果 |
| --- | --- |
| witnesses永遠存在 | PROOF§3、MAPPING§6：w1∈J1−{r,a1}、w2∈J2−{r,u}，簡單奇環至少3點、排除至多2點；包含兩環皆 triangle |
| W不改 J1/J2結構 | 唯一骨架鄰点 x在別處；單接點不能合併原 blocks或繞過 bridges。刪 wi後本環餘路保全部接入口，其餘 C含 W仍連通 |
| 完整鄰居及 D-presence | wi各非割點、非 s-contact、只屬本環，完整 C-degree2；M-degree4迫两原 B附件，均不使用 β未用 D，因此 D∈L^D(wi) |
| degree lists及拒絕 | PROOF§4、MAPPING§7：原全部邊給 |L^D(y)|≥d_C(y)，完整 C染色 iff同一 M有 β延拓且 s=D，含全部 W邊／附件及原 lifts因子。M拒絕 β迫 C不可著色 |
| 外部刻畫及矛盾 | PROOF§5：連通 C的不可著色 degree assignment給 blockwise-uniform palettes。wi只屬 Ji，L^D(wi)=P_Ji；兩者均含同一 D，但 J1/J2在 r相交須 palettes互斥 |

可重用 preservation lemma須完整具名骨架、原 cycle／bridge邊、唯一接點在 J3／q臂、
無其他 cross edge、s-contact或 J1/J2接線；不能擴大為一般多旁支保持。
**本證明不依 BR-SD-1c terminal lemma。** W接 q或臂內點可增加 C-degree、破壞末端／
無額外 C邊前提，接 J3可佔其 witness；1e只使用仍完整的 J1/J2。
不把 cutpoint list含 D推成每個 incident palette含 D，不依 SD-A／二連通／R27 minor。

外部依賴是 [Dvořák作者講義 Theorem10及 blockwise-uniform定義，印刷頁6](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，
degree assignment的≥定義在頁5。本輪讀原定理及定義，現下載與
[1e frozen PDF](../../audits/2026-10-11-br-sd-1e-337d018b/external/gallai.pdf)逐 byte相同：
164927 bytes、SHA256 `50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea`。
[SOURCE](../../audits/2026-10-11-br-sd-1e-337d018b/external/SOURCE.md)的版本／provenance保持；不是新增 Lean或期刊論文宣稱。

最終接受的 PROOF／MAPPING／REPORT hashes分別為
`f184188fc6a18fe84a593b30514ff930783a2d268be9b209775f5c7e223dfd40`／
`e1b6abc4dd2a27474fc93c40207551e92acd0d8f9b275403788b3b269e0392fc`／
`e6386fabd931c4482186331ab22d839987ec1e2fd59f733ace4adf3ecee054c7`，
與 ACCEPTANCE及 REVIEW.final接受 bytes相符。

## 證據分層、residual及 OPEN對帳

[controls REPORT.v3](../../audits/2026-10-11-br-sd-1e-337d018b/agents/controls/REPORT.v3.md)的四份
synthetic M/G完整 β lifts為112/56、256/128、112/56、16/16；四份 M都接受 β。
前三份 private-witness／degree-list校準、數值 ε(G)=2及飽和接點為 `triggered and holds`；
禁止 J1 witness接入的泛化保持、cutpoint D推每個 palette含 D為 `counterexample`。
actual disk／完整 Σ／逐邊 critical／M自身同 β minimal拒絕來源為 `not triggered`。
normal／seed17 v2證書 byte-equal、479749 bytes，hash
`df640b4b5a60929ccd5d1fda4a8018876fff34ff83221d0a92ba3838e41c6705`沿用原封存；
本輪未重跑 controls。原 ε metadata更正、失敗比較、早期稿重建及負控制全保。
任意大小排除由原紙面證明／獨立審查承擔；verifier只核 bytes與既錄 checks，無新 actual source或 Lean。

| 來源身份／研究義務 | 本輪後狀態 |
| --- | --- |
| BR-SD-1a無旁支精確合同 | 既採 Scoped exclusion；[1b](2026-10-11-br-sd-1b-adoption.md)與原證明可追溯 |
| BR-SD-1c單 W只接 J1/J2，保 actual S pair及未動末端 | 既採 Scoped exclusion；[1d](2026-10-11-br-sd-1d-adoption.md)與原證明可追溯 |
| BR-SD-1e單 W唯一接 J3／q臂、保完整合同 | 本輪採納 Scoped exclusion；所有允許接點及任意大小全涵蓋 |
| 兩個可重用局部引理 | 各僅在完整局部／結構前提下成立，不登記一般來源 closure |
| 完整 N45-S-NOU-LS-PAIR、其他 split22／非 split22、無 U兩 long | OPEN；三個子域不關父身份或全部 split22 |
| 兩份或更多原旁支、其他 Gallai block接線 | OPEN，先核是否被既有局部引理覆蓋；不宣稱全部形狀存活 |
| 其他三環形狀／接點位置／更多環及一般非二連通來源 | OPEN |
| R31任意長來源 minor | OPEN；正常形證書不補來源 minor |
| 其他45／54、原55、無45／54來源 | OPEN |
| 一般 N45／N2／E、ε≥3、一般單側／共同出口、主命題及 K∞=K≤5 | OPEN |

**完整 OPEN身份新增無條件關閉數仍為0。** 既採 LOW／HIGH／LONG／U排除不重開。

## 文件傳播核對

依 [DOCUMENTATION](../DOCUMENTATION.md)及只讀即時 [Issue #4](https://github.com/raylei50653/math/issues/4)
的 L0–L3規則，Issue仍 OPEN、updatedAt=`2026-10-08T16:32:54Z`、comments=0。
ordinary file search找到直接 consumers且足以解釋關係，未用 Graphify或 sub-agents，沒有外部寫入。

Updated：L0 N45頁首／採納表／§2.11／§3，分列1a／1c／1e及 preservation lemma界線；
L1 degree-5 guide§4的1e已採與1g窄義務、Kempe相關狀態列／§3、STATUS短索引及本歷史入口；
L2 interfaces§7撤掉當前1e全域 OPEN措辭、接入精確1e及保父身份 OPEN；本紀錄保存逐項核對。

Reviewed-unchanged：N45§1與既採 LOW／HIGH／LONG／U；interfaces§2一般 palettes及四-query／M-query分工；
unary shield§1的 actual support定義；直接 consumer Phase B§2.1／§3.2／§4只使用原支援／容量／U身份，
無 U父身份仍 OPEN、一般化量詞與停止點未變；全部1a／1c／1e audits及1b／1d歷史不改。
HANDOFF的研究線／活躍 tags及 DOCUMENTATION責任未變，README無更新觸發。

Remaining OPEN：上述 residual表全部父身份／未涵蓋來源與1g研究義務。
Propagation stop：完成 L0／L1與直接父主題／consumer的 L2對帳；沒有完整父身份 closure或上層語義變更，
停在 L2，不擴到 L3、synthesis、HANDOFF或 README，不新增平行狀態系統。

## 驗證、frozen custody與未執行項目

修改 live docs前已執行三份 frozen verifiers，採發布後適用的非 `--live`模式。

| 實際命令 | Exit code | 結果／範圍 |
| --- | --- | --- |
| `python3 -B audits/2026-10-11-br-sd-1e-337d018b/verify.py --check` | 0（修改前／後） | 106 payloads、15 BASE authority inputs、206舊 custody檔、13既錄 checks及3最終 review bindings |
| `python3 -B audits/2026-10-11-br-sd-1c-fd6e1112/verify.py --check` | 0（修改前／後） | 81 payloads、17 authority inputs，live=false |
| `python3 -B audits/2026-10-11-br-sd-1a-0f181045/verify.py --check` | 0（修改前／後） | 65 payloads、14 authority inputs；actual_head是歷史 provenance |
| `python3 -B scripts/check_docs.py` | 0 | 602 Markdown、7412 local links，anchors／index／HANDOFF通過 |
| `python3 -B tools/docgraph --include 'docs/**/*.md' check` | 0 | 62 documents、213 relations、5 families，0 errors／0 notes；僅正式 docs |
| `git diff --check` | 0 | 本輪 tracked diff whitespace通過 |

額外只讀核對命令：`gh issue view 4 --repo raylei50653/math --json number,state,updatedAt,url,body,comments`
（exit0，輸出保存 issue-4.json）；`git status --short`、`git rev-parse HEAD`、
`git rev-parse origin/main`、`git ls-remote origin refs/heads/main`與 `git show --format=fuller --stat HEAD`
均 exit0。外部 byte比較 `python3 -B /tmp/br-sd-1f-20261011-y0s_oqte/check_external.py` exit0。
起始 custody用 `python3 -B -`的 stdin快照程式（exit0）保存全部 paths／SHA256／size／mode／symlink；
修改後以 `python3 -B /tmp/br-sd-1f-20261011-y0s_oqte/custody.py`對帳，exit0。
`python3 -B /tmp/br-sd-1f-20261011-y0s_oqte/final_review.py` exit0，另核六檔 whitelist、
新歷史 whitespace與無未完成欄位；N45§1／§2.1–2.10／原1a及1c採納論證、interfaces§2逐 byte不變。
驗證欄位回填後重跑正式 docs／DocGraph／whitespace及 frozen custody，實際結果保存命令紀錄。

起始三份 audit全部313檔、12,569,942 bytes：1a=89、1c=115、1e=109；
排序完整 JSON清單 hash為 `96c4ba750be6cbb21f006667353e624b0767334226776d962d47c69074b1046a`。
修改前後排序完整 JSON逐 byte相同，全部 paths／SHA256／size／mode／symlink無新增、缺失或漂移。
審查用完整 custody清單、命令／stdout／exit codes及 diff保存於
`/tmp/br-sd-1f-20261011-y0s_oqte/`，是本輪本機交付，不是新的權威狀態管理系統。
1e verifier另核1a／1c及1b／1d的206份舊 custody bytes／modes；原 seal／證書／hash／negative controls／
歷史失敗及 postseal輸出均保留。最新 canonical更新與 controls原 BASE／live provenance分開。

未執行：三份 audit的 `--live`（固定原 HEAD／index／live canonical，發布後不適用）、
原 controls checker／seed17／independent_edges solver重播、全部 finite controls、大型枚舉、source搜尋、
全工作樹 DocGraph與 Lean build；沒有為求 PASS改舊 checker或證書。
完成後三份 Git refs再讀仍同發布基準，Git index無 diff；工作樹只有五份既有 live docs及本份新歷史。
沒有 verifier失敗或數學證據漂移 finding，沒有 commit／push。

## BR-SD-1g只保存窄研究義務

當前入口由 [degree-5 guide§4](../c5_degree5_guide.md#4-r31-保留缺口與重播入口)維護。
候選限定同一原三環單 bridge骨架有兩份來源自己的原旁支：
W1接 J1 triangle唯一 private witness，W2接 J3或 q外臂。
這可能同時破壞原 J1/J2雙 witness保證與未改動 J3 terminal lemma前提；
先核原 degree／實際附件、S pair含 W2、W1原 L ownership、原 p/q接線及完整 G／M來源合同。
不能只提供 abstract palettes、不能由容量合法推來源存在。
兩旁支只佔 J1/J2 triangle witnesses且 J3／q末端仍完整時，須先核既採1c terminal lemma是否直接排除，
避免重做已有局部覆蓋。此候選不是 actual來源、已證存活格或完整 residual分類。
本輪未進行任何1g新證明、搜尋或枚舉。

## 採納文件發布階段

採納審查交付後，owner明確授權「整理後 commit + push」。本階段只發布 N45 canonical、
degree-5 guide／interfaces、Kempe guide、STATUS與本紀錄這六份相連文件。
原1a／1c／1e audits、1b／1d歷史、封存證據、證書、hash、負控制及歷史失敗全部保持原 bytes。
本階段不新增數學採納、來源實現或 Lean宣稱；完整 OPEN身份新增無條件關閉數仍為0。
發布前重跑上列六項必要命令及313檔完整 custody對帳，以六檔 whitelist核 stage與提交；
發布結果以實際 commit、HEAD／origin/main／遠端 main及工作樹回讀為準。
前述未 commit／push、發布基準與工作樹敘述保留採納審查時點。
