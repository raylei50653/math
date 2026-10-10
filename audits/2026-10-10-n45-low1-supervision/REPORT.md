# N45-S-LOW1 監督驗收與限定採納

2026-10-10。BASE／實讀 HEAD `dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。
本輪在既有主管理授權下驗收 [LOW1](../2026-10-10-n45-s-low1/REPORT.md)，
三份獨立稽核各只新增專屬目錄；監督另更新五份直接相關共享文件及新增一份歷史／next-task。
沒有 commit、push、PR或外部訊息。

**採納：完整 LOW1 契約內、原 U incidence=1 的任意大小來源排除。**
LOW1-CORE／COMP／JOIN／F／MAP／EXCLUSION 六項均正式接受；沒有新額外前提。
LOW incidence2（LOW2）、HIGH、long、其他 cores、原55、無45／54來源、一般 N2／E及ε≥3仍 OPEN。
精確逐項量詞、全部十二前提、依賴及 scoped decision見 [acceptance](acceptance.json)，
當前權威入口見 [N45](../../docs/c5_excess_two_nonadjacent_unit_core45.md)。

## 1. 證明與独立裁決

共同原 G：有限任意大小 simple induced-C5 disk、完整Σ933／941及共同D5像、非框邊Σ-critical、
ε2、有效H連通full B-touch、原兩非相鄰degree5 roots、其餘完整degree4。
LOW1另有唯一原U在r、unique rx，mixed P/Q各真框邊pair支援，mixed incidences(2,3)，
原兩roots各兩spokes；僅刪原e=rb_i，X=G−e=M自己β inclusion-minimal45／54。
U/P/Q的全部原頂點與邊、原ordered/sharedcontacts、附件/support/ownership、bridges/rotation、
共同literal色框、全十列relations、全ambient tuple空／非空fibres及full lifts保留。
原孤立內點按有效H慣例自由lift；933 q2不省略，整圖色/框/root搬運共同作用全部資料。

| Claim | 採納的論證 | 獨立核回 |
| --- | --- | --- |
| LOW1-CORE | 刪原r–B spoke不改H；r完整降4、s維持5、其他4；minimality由X=M自己提供 | L1A／L1R |
| LOW1-COMP | C=H_X−s={r}∪U∪P∪Q唯一連通；三s-contacts互異原序，complete degree_X與degree_C分清 | L1A／L1R |
| LOW1-JOIN | 同一r坐標施全部原contact不等式，全部assignments restriction／union互逆；G一般γ只多r≠γ(b_i) | L1A／L1R |
| LOW1-F | X自己minimality給s-spokes異色，逐刪spoke全lift給F_C精確補集，strict slack給非空R_C | L1A／L1R |
| LOW1-MAP | 同一C兩tight lists、Gallai palettes、三葉activeforest、zero arms與原boundarytethers，十對原K₅ bags | L1A／L1R |
| LOW1-EXCLUSION | 同一disk子圖X含K₅ minor矛盾，逐全部完整LOW1契約量化 | L1A／L1R |

[L1A](../2026-10-10-n45-l1a/REPORT.md)獨立重推六項及官方Gallai定理；
[L1R](../2026-10-10-n45-l1r/REPORT.md)另核原頂點／邊、joint全lifts、sharedcontact及theorem搬用。
[監督端重推](paper-reconstruction.md)再對回BASE§1–5與原bags。二異色spoke位置可任意，
不要求βsingleton在U盾中點、不刪U、不使用SS整U省略的未接框點推論。

信任：paper＋固定BASE三接點／R10／list-critical＋
[Dvořák Lemma7／Theorem10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)外部degree-list定理。
Python僅核artifact或有限relation校準；沒有新LOW1有限來源、目標trigger數、source realization或Lean。
L1R toy語義校準已標triggered and holds；LOW1來源契約not triggered，未作來源搜索。
本輪沒有Lean變更，不跑lake build；該build也不能證新紙面映射。

## 2. 版本、封存與只讀重播

監督在添加任何新目錄前已跑worker strict normal／seed17，皆actualexit0且output bytes相同，
corruptedmanifest actualexit2且原因為digest mismatch；[原工具輸出與exit](initial-strict-replays.json)保存combined stream。
strict工具比對完整原Git inventory；新監督／稽核目錄加入後的inventory rejection是預期變化，
不能再要求當前workspace等於worker交付時的快照。採納後authority又有明列已授權更新，
改以凍結pins、完整immutabletree及已採納after-state核對。

Worker final-v4：6049 regular、5 symlinks、10 receipt-bound metadata、12 BASE blobs與6 currentpins。
初始25869 regular hashes、22 symlink identities、4nested repo directory entries；四者未遞迴hash，
不宣稱它們歷史內部零漂移。監督另凍結當前Git列出之existing檔及whole worker tree，
只允許五個共享原檔採納修改與一個新history；舊worker和所有oldaudits完整不動。

| 獨立稽核 | 核回範圍 | 本輪父端完整重播 |
| --- | --- | --- |
| L1A | 26 inputs、12 BASE blobs、41 payload、5 receipt files；六paper claims | normal／seed17 actualexit0、bytes同 |
| L1R final-v2 | 21 frozeninputs、4 BASE blobs、44 payload、8 receipt files；六paper claims及完整relation toy | normal／seed17 actualexit0、bytes同 |
| L1C | 44 payload、7 receiptfiles；workerexact envelope及七項synthetic負控制皆預期exit2 | normal／seed17 actualexit0、bytes同 |

[L1C](../2026-10-10-n45-l1c/REPORT.md)只接受工具envelope，不代紙面裁決。
監督自己的 [intake](intake.py)另核三份exact primary manifests／receiptmetadata與fulltree，
所有hash、實際命令和stdout／stderr收於 [checks](checks.json)、[incoming](incoming-audits.json)及 logs。
監督 [MANIFEST](MANIFEST.sha256)綁全部payload，[delivery](delivery.json)另綁封存實跑metadata。

## 3. 非阻擋 findings 與歷史 FAIL

1. L1C-INDEX-01：worker checks.json.postseal_actual_results仍指failed v1。
   final成功唯一入口是delivery.json明綁的seal-final-v4/commands.json；REPORT也已正確指此。
2. AMBIENT-FIBRE-DOMAIN：Fib_γ(t)對全部t∈Col³定義，R_C是非空fibre支援；未改完整join。
3. L1A-SECTION-INDEX：sealed judgment的COMP/JOIN/F索引應讀L1A REPORT§2/§3/§4。
   主claim表與推導正確，原json／manifest不改。
4. L1R-SEAL-V1：basename排除誤漏nested delivery，被checker以inventory mismatch拒絕；
   原manifest／failure logs／finding完整納final-v2，最終exact intake及父端重播通过。
5. L1R-ROW-NOTATION：sealed REPORT§2的一處β／γ記號歧義，已獲reviewer只讀確認；
   一般γ的原spoke條件是r≠γ(b_i)，固定β才寫β。原worker、judgment與checker用當列實際框色。

上述沒有新數學缺口，原sealedbytes全部保留；正確式亦寫入當前authority及next-task。
Worker v1排序、v2 nestedrepo目錄、v3 inlinecode被誤認link的工具FAIL仍完整保存。
v1初始負控制未到digeststage；v2/v3/final-v4才到digeststage。沒有把失敗首輪寫作成功。
fresh BASE check_docs兩歷史缺檔、本工作樹DocGraph duplicate-ID FAIL與舊E4 provenance FAIL保留；
正式docs PASS不表示whole worktree PASS，舊provenance本輪未重跑。

## 4. 文件傳播與下一任務

Closure scope：只關完整LOW1原U incidence1契約；[acceptance](acceptance.json)綁採納版本。
Updated：N45 authority → Kempe guide／STATUS → E4 dated follow-up／Phase B直接consumer，
另新增[LOW1採納與LOW2任務](../../docs/history/2026-10-10-n45-low1-adoption.md)。五份共享修改有[diff](documentation.diff)。
Reviewed-unchanged：root-deletions與mixed-omission是不同原身份；synthesis仍一般N2/EOPEN；
HANDOFF／README路由未變，舊histories保日期、任務與pins；[傳播核對](propagation-plan.json)。
Remaining OPEN：LOW2／HIGH／long、其他cores／原55、無45／54來源、一般U／nonminimal省略、ε≥3、N2/E及Lean。
Propagation stop：L2，父題仍OPEN。**LOW2任務已備、尚未啟動**；無commit／push。

## 5. 本輪實際檢查結果

21項監督 logged commands均對回實際exit與預期；另保存新增目錄前的三次strict工具結果。
最終check_docs：PASS，592 Markdown／7131 local links，anchors／direct index／handoff核回。
初次adoption文件檢查因漏新history的STATUS直接索引而exit1；補索引後重跑exit0，原失敗log保留。
正式docs DocGraph：PASS，62 documents／213 relations／5 families；全worktree：FAIL，62duplicate IDs，原logs保留。
fresh BASE：FAIL，586 Markdown／6982links中的兩歷史缺檔原樣保留。
tracked／cached whitespace及20份本輪相關文字檔核對通过，沒有新trailing whitespace。
五份共享原檔＋一份新history為全部已授權文件更新；其他原Git inventory檔與worker fulltree未改。
[adoption-state](adoption-state.json)固定after-state，[authored-text-check](authored-text-check.json)記文字核對範圍。
監督封存normal／seed17／corrupt-digest實跑另由delivery精確綁定seal-checks metadata。
