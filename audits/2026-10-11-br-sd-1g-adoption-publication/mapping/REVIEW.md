# BR-SD-1g：授權採納的精確量詞與直接 consumer 同步

2026-10-11；固定採納 BASE `c15a635e17d4be814e19aeeeeb765f3d6024099a`。
Owner 後續明確批准精確 BR-SD-1g 採納、文件同步及 root 完成檢查後 commit＋push main。
本 worker 只改四份指定 consumer 文件及本新 publication audit 的 `mapping/`，沒有 git stage／commit／push。
原 1g、原 publication、獨立採納審查、全部歷史 audit／seals 均未修改。

## 1. 固定依據與本輪操作

依據已封存的 [CANONICAL_DELTA_PROPOSAL](../../2026-10-11-br-sd-1g-adopt-6eae3597/CANONICAL_DELTA_PROPOSAL.md)，
其完整八項合同由 root 同步到 [canonical N45§2.11](../../../docs/c5_excess_two_nonadjacent_unit_core45.md#211-單缺額查證與無-u-二連通子域)。
[原 PROOF](../../2026-10-11-br-sd-1g-dbdc4c35/PROOF.md)、
[獨立 REVIEW](../../2026-10-11-br-sd-1g-adopt-6eae3597/REVIEW.md)、
[獨立 MAPPING_REVIEW](../../2026-10-11-br-sd-1g-adopt-6eae3597/MAPPING_REVIEW.md) 保持原 bytes，
本轮不重證或擴大數學結論。

寫入在 root 的 **CREATION READY** 通知及新 TASK／PREFLIGHT 建立後開始。
[READS.json](READS.json) 保存13個重新執行的讀取命令、stdout／stderr、exit0及其hash；
[FAILED_INITIAL_READ.json](FAILED_INITIAL_READ.json) 保留初讀 zsh glob 展開失敗的實際exit1 receipt，
其後 exact-path 查閱已成功，沒有用此讀取失敗掩蓋任何未讀來源。
[BEFORE.json](BEFORE.json)／[AFTER.json](AFTER.json) 保存四份修改文件及五份 reviewed-unchanged 文件hash。
[CHECKS.json](CHECKS.json) 保存四份 consumer diff、`git diff --check` 與限定詞查閱的實際命令／原始輸出／exit0。

## 2. 四份直接 consumer 的精確同步

| 本 worker 修改檔案 | 修改與停止點 |
| --- | --- |
| [degree-5 guide](../../../docs/c5_degree5_guide.md) §4 | 現有1g candidate改成已授權採納的完整精確子域；明列J1 triangle、兩原Wi唯一接點／L/S ownership、S short／actual pair、同原G/M/β、M自己同β minimal拒絕、degree／attachments／witnesses與full lifts。含任意奇長、零臂與a3=v；摘要说明J2屏障与incidence tree，不用失效cutpoint推論，並連原proof／独立review／canonical／新history及新custody入口。R31與一般多旁支OPEN保留。 |
| [degree-5 interfaces](../../../docs/c5_degree5_interfaces.md) §7 | 保SD-A及歷史conditional語境、1a／1c／1e原合同；追加1g精確同來源合同、完整lists／M s=D全延拓、ignored原坐標因子及J2屏障。明列無二連通要求、finite仅校準、source not triggered／Lean0／closure0。 |
| [Kempe guide](../../../docs/c5_kempe_guide.md) 狀態表／§3 | 當前非相鄰45／54摘要與1g candidate入口同步為独立的精確scoped排除；保父OPEN與上游SF-QX／BASE／Gallai信任界，不把一般兩旁支／N2升級。原1a／1c／1e採納說明及歷史引用保留。 |
| [STATUS](../../../docs/STATUS.md) | 更新degree5入口、N45摘要及當前日期說明；新增独立採納審查與新history索引，保原1f當輪「1g僅記義務」等歷史列。短狀態不取代八項完整合同，也不把publication檢查概括成數學／來源認證。 |

新 history 由 root 建立：[BR-SD-1g 採納紀錄](../../../docs/history/2026-10-11-br-sd-1g-adoption.md)。
本 worker 沒有改 canonical 或 history。新 publication custody 入口為
`python3 audits/2026-10-11-br-sd-1g-adoption-publication/verify.py --check`，提交後加 `--require-tracked`；
本 worker 未把尚未實際發生的commit／push結果寫成已驗證事实。

## 3. 八項合同的量詞覆蓋審查

Consumer 使用完整 canonical 合同的明確 reference，只摘要其窄適用身份；
沒有用短摘要取代或減少完整八項前提。以下對照 sealed proposal 的每項：

| 合同項 | 必保量詞／原來源資料 | Consumer同步判定 |
| --- | --- | --- |
| 1 | 任意有限簡單ordered induced-C5 disk原G、完整Σ933／941或整圖D5像、ε2、原Σ-critical全witnesses、連通有效H、不相鄰原5-roots及其他完整4、full B-touch／one-sided／nonempty support | guide明寫G／Σ／ε／witnesses，全部四檔固定canonical入口；沒有新source realization。 |
| 2 | 完整原L/S mixed、U0、L long、**S short**、actual support恰同一真框邊兩端，Wi附件计入owner完整support | 四檔均明确S short／actual pair；guide／interfaces明确W1/W2归L/S，沒有将W1也限制到S pair或將兩点subset代替整份聯集恰pair。 |
| 3 | exact-S僅删r唯一原spoke、同一V(M)=V(G)、E(M)=E(G)−e、X=M；M自己同literal proper三色β minimal且拒絕，保M自己retained-edge全witnesses | 四檔均明写M自己同β minimal拒絕，source合同用canonical固定；沒有由G critical性推M minimal。 |
| 4 | M仅s完整5、其餘有效完整4，原s三spokes／相異有序p∈L,q∈S；sole C、r split22／C度4／M無框spoke；45／54共同roles交換 | 每份摘要限定同原G/M/β及r split22、完整degree；其他細節由明確canonical完整合同固定，不重新normalise components。 |
| 5 | J1指定triangle `(r,a1,x1)`；J2/J3任意奇長≥3，J1∩J2={r}且J3不交；原uv唯一環間bridge、任意原simple bridge臂h/ℓ≥0，含p=a1、q=a3與a3=v，正臂off-cycle互斥 | guide与interfaces明确任意奇長／零臂／a3=v；Kempe及STATUS保相同量詞，沒有偷偷假設h／ℓ>0或a3≠v。 |
| 6 | 原C恰骨架⊔W1⊔W2，Wi任意有限非空連通、唯一接x1和x2∈J3∪q-arm，可多條xi–Wi原邊；無相互邊／第二接點／額外s-contact／第三旁支／cross edge | guide／interfaces／Kempe明确兩份原Wi及其唯一接點、ownership與禁止額外接線；STATUS摘要固定八項合同。全部合法mi及有限Wi大小保留，沒有只登記六個fixtures。 |
| 7 | 完整L/S ownership與原实际A(y)，逐點原完整4=dC+k+t；actual S聯集恰pair，L不受pair兩點限制；所有合法位置／mi／重合，先超degree者結構排除，禁止刪附件容納旁支 | guide明确原degree／附件與必要容量≠來源，interfaces保原實際degree与attachments。沒有引入free attachment選擇、改源或Wi大小上界。 |
| 8 | 每原點／邊、named／ordered／shared单一坐標、actual附件／support、ownership、bridge身份、rotation、同literalCol/β、G/M各自witnesses／完整relations／空fibres／full lifts及effective-H忽略原點允许色因子 | guide／interfaces／Kempe都写full lifts与ignored原坐標因子；interfaces另明named／ordered／shared、rotation／bridges；STATUS引用完整原資料及八項合同。所有因子均保，不把C assignment直接冒稱M全坐標bijection。 |

任意大小結論只來自原紙面證明及已封存的獨立審查。
六個 synthetic fixtures 是具名有限機制控制；没有來源／Σ／disk／minimality全稱觸發，也没有大小正常形結論。
固定同一T/D及J2原private witness、唯一S–L接口是已審查的推論，未重用
`D∈L(x1)⇒D∈P_J1`。非割點、leaf block、triangle、K4與任意有限Wi的處理仍由原proof／review承担。

## 4. Reviewed-unchanged 文件與傳播止點

| 只讀檢查的檔案 | 無需改bytes的同步理由 |
| --- | --- |
| [HANDOFF](../../../docs/HANDOFF.md) | 實際17行thin入口，無1g候選文字；已有degree5与Kempe guide連結承接本次精确採納／接续。依封存proposal明确裁决guide同步、HANDOFF不增長。 |
| [STATUS_HISTORY](../../../docs/STATUS_HISTORY.md) | 歷史快照，當輪未知／candidate語境須保留；新history與STATUS已提供當前採納及publication入口，無需回寫舊快照。 |
| [Phase B](../../../docs/c5_phase_b_common_lemmas.md) | 既有B-S0／B-C2及B-S1／B-E量詞不变，当前一般N2／無U残留OPEN合理；精確後續与排程已明確路由canonical／Kempe。原當輪stop保留，無新增共通引理推廣。 |
| [unary shield](../../../docs/c5_unary_shield_budget.md) | 原不依ε的support／hub定理不被本精確source exclusion改寫；停止點由Kempe維護，無1g候選文字需改。沒有把S局部palette屏障提升為通用盾弧結果。 |
| [README](../../../README.md) | 高階研究路由及主命題未證、degree5／R31／完整來源分類缺口仍真；delegate細節到更新後guide／STATUS已足夠，无1g特定candidate需改。 |

上述五檔AFTER与BEFORE的SHA256全部相同。傳播停 **L2**。
根層正式採納與publicationcheck／commit＋push的權限及執行由root負責，
本worker不修改舊publication whitelist；舊pubexit1與新immutable-adapterexit0需在root記錄保持兩層。

## 5. 保留邊界與裁決

Consumer同步裁決：**ACCEPTABLE，無阻斷的量詞／同來源／上游傳播finding。**
完整 `N45-S-NOU-LS-PAIR` 父身份仍 **OPEN**；未涵蓋split22／非split22、兩／多旁支、
其他三環形狀／更多環／一般Gallai接線、R31、其他45／54／55／無45／54、ε≥3、
一般N45／N2／E、一般出口、主命題及 `K∞=K≤5` 都不升級。
Actual source **not triggered**，新Lean theorem **0**，完整OPEN身份新增無條件關閉 **0**。
完整數學／custody／final-byte採納裁決及實際publication結果依root新history與本audit最終證據。

## 6. Canonical／新history最終bytes核對

Root通知canonical與新history ready後，本worker直接逐項重讀實際canonical八項合同及紙面摘要，
再讀實際newhistory；[FINAL_READS.json](FINAL_READS.json)保存完整命令與原始stdout／stderr、exit0。
八項量詞與sealed proposal逐項相符：明保S short、h/ℓ≥0與原零長身份、a3=v、
所有mi／x2合法位置、任意有限非空Wi、M自己同β minimal拒絕、全部relations／空fibres／full lifts
及effective-H忽略原坐標的允許色乘積。未把必要capacity改為actual source realization。
紙面摘要沒有使用失效cutpoint推論；父OPEN、source NOT TRIGGERED、Lean0與完整closure0均明列。
新history將歷史pubexit1與immutable adapterexit0分開，未回寫歷史white list或原候選bytes。

[FINAL_DOCS.json](FINAL_DOCS.json)固定本輪六份live文件的最終hash如下；
本mapping裁決對這些exact bytes為ACCEPTABLE，沒有阻斷finding。後續若改文件bytes須重核。

| 文件 | SHA256 |
| --- | --- |
| `docs/c5_excess_two_nonadjacent_unit_core45.md` | `ec80d3f0b053d6c7776b9b7fc0fdfa8432e0e4aef69feb052d3b69e53aa76be8` |
| `docs/c5_degree5_guide.md` | `370f220db159466b27d6e305235e9c69abbe26dbc107243fe750e8a357529ce7` |
| `docs/c5_degree5_interfaces.md` | `6fbca9d1d82a50dbe29105091a60f41b8e11d161c4f347fa01d710840b0c9260` |
| `docs/c5_kempe_guide.md` | `626b85aa256a45fa92420125523ff64cd7d7d51f21d3f319c7d4faa6a1a7db25` |
| `docs/STATUS.md` | `abd6dad64bc18840770ee61b3c17e392f90f2a2673dfd47e87a2a51e4b5d5654` |
| `docs/history/2026-10-11-br-sd-1g-adoption.md` | `e29e568062e449462e642fa7db791578a0c68a905476b4b29fb384831259e14b` |
