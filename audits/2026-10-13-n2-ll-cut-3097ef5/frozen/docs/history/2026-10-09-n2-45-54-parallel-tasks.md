# 2026-10-09：N2 的 45／54 原 unit 省略並行任務

使用者負責對外發布任務並回傳結果；本對話負責範圍、依賴、證據驗收及下一批安排。
初次準備時尚未收到開工或結果；2026-10-09四份及SU-A／SU-J均已回報且限定scope驗收，
S／U窄排除正式採納，見§3。[第二批](2026-10-09-n45-u-long-short-pair-tasks.md)只選U的long／short pair residual。
數學停止點與本線下一步由
[Kempe 導覽 §3](../c5_kempe_guide.md#3-停止點與保留缺口) 維護。
這是指定缺口的派工紀錄，不建立全研究案例帳目，也不宣告猜想 E 完成。

## 1. 選線、基準與本次實查

選擇 **非相鄰雙 degree-5 roots、恰兩份原 mixed（N2），拒絕列 core 為
degree-(4,5)／(5,4)，恰省略一個原 side unit**。
此入口由 [E4 原 relation 與省略身份](../../artifacts/c5_excess_two_e4/REPORT.md#6-完整原-relation-的參數化交付與-core-身份)
及 [Phase B 分析](../c5_phase_b_common_lemmas.md) 指定。
可拆成兩種互斥的省略身份，另由完整 joint 工具與前提稽核支援。
固定完整 Σ 下的兩-root44身份已有 U1–U4 排除，毋須重派。

| 項目 | 本次確認 |
| --- | --- |
| canonical root | `/home/ray/developer/ai/math` |
| 凍結研究基準 BASE | `dc8e9aa7d6fccb51f63d30aa3f9c132296d44744` |
| 接手 Git | `main`；HEAD與本地`origin/main`均為BASE；接手工作樹乾淨；未查遠端即時SHA |
| 權威入口 | E3 nonadjacent notes §5、E4 REPORT §4／§6、CORE_CONSTRAINTS §2／§4、Phase B §2／§3.2 |
| 保存控制的實際範圍 | E4C有54份controls；19份m=2圖各一個拒絕列core，全部55；12份45／54 cores全屬m=1（10份45、2份54） |
| 本次重播 | `python3 scripts/c5_phase_b_controls.py --check` exit0，只驗原固定controls |
| 未重跑 | E3／E4／E4C全套、U1–U4、ES／ER枚舉、Lean；19／12統計是保存資料的字段核對 |

初次派工時Phase B原capacity checker只覆蓋相鄰roots、sole shared-(1,1) mixed，
沒有覆蓋本批需要的 `χ=0`、兩mixed。E4C的19份N2圖可以提供這層校準，
但完整Σ不是933／941，三列來源前提沒有觸發，也沒有N2的45／54正控制。
不得把這些缺控制寫成已驗證目標來源。

第一批接受精確子型排除、具名反例或必要化約；不要求各執行者完成一般N2。

指定來源路徑：
[E3 REPORT](../../artifacts/c5_excess_two_e3/REPORT.md)、
[E3 nonadjacent notes](../../artifacts/c5_excess_two_e3/nonadjacent_notes.md)、
[E4 REPORT](../../artifacts/c5_excess_two_e4/REPORT.md)、
[CORE_CONSTRAINTS](../../artifacts/c5_excess_two_e4/CORE_CONSTRAINTS.md)、
[U4](../c5_excess_two_nonadjacent_two_mixed_core44.md)、
[E4C REPORT](../../artifacts/c5_excess_two_e4c/REPORT.md)、
[Phase B](../c5_phase_b_common_lemmas.md)、
[原capacity checker](../../scripts/c5_phase_b_controls.py)。任務頭已指定讀BASE版本。

## 2. 共用任務頭

**每份發布內容＝本節任務頭＋§4對應任務全文。四份可同時發布。**

```text
研究根目錄：/home/ray/developer/ai/math
BASE：dc8e9aa7d6fccb51f63d30aa3f9c132296d44744
任務：下方指定的 N45-S／N45-U／N45-J／N45-A。
從BASE使用自己的獨立checkout／worktree；先核完整HEAD、Git狀態，
讀BASE版本的docs/HANDOFF.md、docs/STATUS.md、docs/DOCUMENTATION.md及指定來源。
HEAD不同須列實際差異，不混用版本。輸入只讀，只寫自己的獨立輸出目錄。
不改共同報告、guide、STATUS、舊artifact或其他任務輸出；保留既有資料。
不commit／push／開PR／對外發訊息；使用者回傳研究結果給監督端。
本任務自行完成，不再委派sub-agents。不擴大k搜尋，不重開U1–U4或一般猜想E。

目標G：有限簡單圖，有序induced C5外框B=(b0,...,b4)為disk外面；
完整有序Σ(G)=933／941或整圖D5像，每條非框邊Σ-critical，ε(G)=2。
有效H忽略孤立內點，恰兩個完整degree5 roots z,w且zw不存在，其他內點完整degree4。
H−{z,w}的完整分量恰有兩份mixed P,Q，其餘為unary。
共同搬運整圖後採canonical mask，不獨立搬框、roots或pieces。
q0=01212（cells index6）、q1=01202（index4）、q3=01021（index1）皆拒絕。
941接受q2=01201（index3）、q4=01012（index0）；933拒絕q2且接受q4。
T4為cells indices {2,5,7,8,9}。不把932／940或僅三列前提當成精確目標。

對拒絕列β的minimal core M，本批只研究root degrees (4,5)/(5,4)：
E3／E4給恰省略對應側一條原spoke，或整份只有一條原root-contact的unary，
兩份mixed全部保留。capacity-one指原root incidence=1，不指每列禁色恆為singleton。
G的Σ-critical、M的β-minimal、X=G−unit的性質分開，不預填X已Σ-critical。

保存同一原圖、具名頂點、ordered distinct／shared contacts、actual attachments/supports、
ownership、原bridges、cyclic order、共同字面色框及完整relations/fibres、空fibres、full lifts。
拓撲收縮只能證拓撲；染色替換另須完整relation及上下文證明。
paper、外部Gallai／degree-list、有限Python、Lean普通證明／native_decide分層。
不能用有限無反例、Σ相容、端點marginals或lake build代替來源排除／實現。
找不到充分前提時交具名residual並停止；來源反例逐項驗全部目標前提。

每個實質結論有CLAIM-ID、量詞、全部前提、依賴、證據層及未涵蓋範圍。
至少交REPORT.md、inputs.json（BASE與實讀路徑／SHA256）、checks.json（命令／exit／logs／未跑項）。
有限核對另交checker與證書，普通及PYTHONHASHSEED=17重播；--check只讀，生成exclusive-create。
控制分triggered and holds／not triggered／counterexample，逐项記缺失前提。
純paper／Python不假造Lean驗證；有新Lean才在獨立cache跑具名build／axioms audit。
依§6回報，不只說完成或PASS。
```

兩原mixed都one-sided，目前一般N2只知其actual support非空。
省略原unary仍按原 `σ_G(U)` 收費；spoke是原邊，不能當piece收盾弧費用。
U4的支援至少二點及 `2+ℓ+2u≤5` 依44身份證明，不能直接搬用。
僅在另證兩mixed各至少二點支援且有兩份不同原unary時，B-S0才給 `1+1+2+2>5`。

## 3. 第一批依賴與狀態

| ID | 工作 | 依賴 | 獨立輸出目錄 | 目前管理狀態 |
| --- | --- | --- | --- | --- |
| N45-S | 原spoke省略的任意大小必要化約／窄子型排除 | BASE | `audits/2026-10-09-n45-s/` | 已驗收；六項claim限定scope正式採納，LOW／HIGH／long仍OPEN |
| N45-U | 整unit unary省略的支援／見證／預算化約 | BASE | `audits/2026-10-09-n45-u/` | 已驗收；八項claim正式採納，唯一U＋long／short仍OPEN |
| N45-J | χ=0兩mixed完整joint與逐欄容量獨立checker | BASE保存controls | `audits/2026-10-09-n45-j/` | 已驗收：工具與固定控制；來源排除仍OPEN |
| N45-A | 省略分類、E2 derivative及可搬用前提獨立稽核 | BASE來源 | `audits/2026-10-09-n45-a/` | 首輪已驗收；9 CLAIM／4 findings，未審新S／U |
| N45-SU-A | S／U十四claim的獨立paper增量 | frozen S/U及BASE | `audits/2026-10-09-n45-su-a/` | 已驗收；明列前提內成立，未見新推理缺口 |
| N45-SU-J | 固定圖／完整relations／容量有限增量 | frozen S/U/J及BASE | `audits/2026-10-09-n45-su-j/` | 已驗收；7952pins／2986lifts／102欄，精確來源仍0觸發 |

S／U按指定core的省略因子分工；同一G不同列可能屬不同任務，仍保其全部跨列限制。
這只覆蓋45／54原身份，不覆蓋原55。J先完成校準工具，不等S／U。
A首輪審共同依賴，不宣稱已審尚未返回的新證明。

**J返回／驗收（2026-10-09）：** [原交付](../../audits/2026-10-09-n45-j/REPORT.md)及
[監督裁決](../../audits/2026-10-09-n45-j-supervision/REPORT.md)。N2的3040原圖／8640省略queries及74容量欄
重播與獨立重算相同，N1校準分列；66個BASE輸入及89個交付hash通過。
完整目標來源與N2降度側右值0的拒絕控制未觸發，沒有新增45／54排除；
J首輪當時尚未收到S／U／A回報，未讀其目錄或判定成果。

**S返回／預審（2026-10-09）：** [原交付](../../audits/2026-10-09-n45-s/REPORT.md)及
[監督預審](../../audits/2026-10-09-n45-s-supervision/REPORT.md)。六項claim的指定前提／依賴紙面核對未見缺口；
原spoke省略身份下兩原unary的窄排除、拒絕列零slack及兩short的2／3 incidence待獨立增量採納。
69份BASE輸入、21項交付hash核對，正常／seed17重播通過；獨立枚舉237份圖／列、3792個root-pair cells
與J一致，218份S full lifts合法；19圖／47份省略查詢全部未觸發N45-S目標來源前提。
fresh BASE文件缺歷史目標及全域DocGraph副本duplicate-ID失敗保留。
[N45-SU-A／N45-SU-J增量發布全文](../../audits/2026-10-09-n45-s-supervision/cross-audit-tasks.md)
已凍結S／U／J hashes；U回報後合併為兩份可併行增量，未啟動或對外發布。
LOW／HIGH及long配置仍OPEN，尚未選第二批研究。

**A／U返回與批次裁決（2026-10-09）：** [A原交付](../../audits/2026-10-09-n45-a/REPORT.md)、
[U原交付](../../audits/2026-10-09-n45-u/REPORT.md)及[批次監督裁決](../../audits/2026-10-09-n45-batch-supervision/REPORT.md)。
A首輪共同依賴與固定controls已驗收；720份BASE bytes、56個manifest entries通過；
54圖／172units接受性獨立相等，74欄與J一致，兩個歷史E4 provenance replay FAIL及文件缺檔保留。
U八項paper預審未見缺口；原兩unary與兩short子型的窄排除待獨立採納。
70份BASE來源及39份authored檔凍結；23圖7200個原／省略／contact-deletion pins、
690份localrelations／2986piece lifts及102容量欄與J一致，精確目標來源仍0觸發。
U剩唯一被省略U＋一long／一short的完整同源跨列接合。
A／U返回當時下一步為合併SU-A新paper稽核與SU-J有限增量；後續採納見下段。

**SU-A／SU-J返回與正式採納（2026-10-09）：**
[SU-A](../../audits/2026-10-09-n45-su-a/REPORT.md)、[SU-J](../../audits/2026-10-09-n45-su-j/REPORT.md)
及[監督採納](../../audits/2026-10-09-n45-su-supervision/REPORT.md)。十四paper裁決与先前預審一致；
S-spoke/u2、U-whole/u2、U-whole/two-short窄子型正式排除，必要化約已採納。
SU-J7952指定整圖pins／690relations／2986piece lifts／102欄正常与seed17重播通過；
兩份exactinventory、S/U/J原交付與432declared BASE reads對回87unique路徑bytes／mtime零漂移。
紙面、finite、來源實現、Lean分層；完整目標仍0觸發，歷史FAIL保留。
權威入口為[N45原unit省略45／54](../c5_excess_two_nonadjacent_unit_core45.md)；
直接父E4與Phase B效益更新，父N2仍OPEN，傳播停L2。
第二批只選唯一U＋long／short pair，见[三份可併行任務](2026-10-09-n45-u-long-short-pair-tasks.md)。
LOW／HIGH／long、singleton short與原55／一般N2等仍OPEN；未commit／push。

## 4. 可發布的四份任務

### N45-S：原 spoke 省略身份

接續共用任務頭。只寫 `audits/2026-10-09-n45-s/`。
先讀E3 nonadjacent notes §5、E4 REPORT §4／§6、CORE_CONSTRAINTS §2／§4、
Phase B §2.1／§2.2／§3.2；U4 §2只用來判別44專用前提。

固定原spoke `e=rb_i`，r是degree下降root，`X=G−e=M` 是某拒絕列β的45／54 minimal core。
涵蓋root交換，保兩完整mixed與另一側所有因子。

1. 重建最小充分前提及跨列限制。沿E4-U，X繼承T4且ε=1；需用Σ-critical結論時
   先取保Σ minimalization，不直接給X該前提。列同一X不能跨q3與q0／q1拒絕的用途。
2. 核省略仍拒絕β時，此spoke色是否已被另一spoke禁止，或由完整unary／兩mixed的joint封住。
   E4-D重色spoke迫省略身份只在其前提下引用，不能假設所有spoke省略都重色。
3. 優先嘗試由這個原身份補出兩mixed支援下界，或由同一β的完整joint給指定target延拓。
   只證某種support／spoke子型便明列範圍及其餘residual，不作全型結論。
4. 有限正常形先證任意大小適用及保完整relation；沒有化約便停於必要式／具名配置，
   不開廣域模板枚舉，spoke不冒算盾弧。

交一份可審窄命題或精確失敗義務，列933／941、root交換、β及原spoke身份的適用性。
新排除由paper承擔，有限表只作控制；碰撞交原圖、字面pins及full lifts。
未實現的抽象relation只標必要介面控制。

### N45-U：整份 capacity-one unary 省略身份

接續共用任務頭。只寫 `audits/2026-10-09-n45-u/`。
讀E3 nonadjacent notes §5、E4 REPORT §4／§6、CORE_CONSTRAINTS §2、
[原unary盾弧](../c5_unary_shield_budget.md)、Phase B §2.1／§3.2及U4 §2的下界依賴。

固定完整原unary U，唯一原root-contact為 `rx`；`X=G−V(U)=M` 是某拒絕列β的45／54 minimal core。
U任意大小，每個U點在原G完整degree4；涵蓋root交換，兩mixed全保留。

1. 將省略core映回整份原U，不用接點禁色singleton替代U。每列保存R_U、contact full lifts及F_U；
   F_U允許空，保原唯一root-contact及所有框附件，不抽成新頂點。
2. 由原critical contact刪除給逐piece拒絕見證及避U外路，核B-S0前提。
   U雖不在M仍支付原盾弧；見證列β_e可以不同於M的β，不能將兩列當同一染色容量。
3. 優先檢查有兩份不同原unary的子族，能否由此身份另證兩mixed各有至少二點支援，
   使預算超五框邊。singleton支援不能排就保存原必要配置及缺失criticality／hub義務。
   一份unary、long mixed等其餘族只保精確必要式。
4. 用E4-U核同一X的ε1跨列限制。B-C2只在同一β／pins／完整joint內用；
   原G degree5預算與X degree4預算分開。

交窄命題／residual／反例及完整前提。任意大小paper與小控制分列。
沒有N2的45／54前提觸發便列缺控制；不能證mixed下界則交最小待補義務並停止。

### N45-J：非相鄰兩 mixed 的完整 joint 與容量校準

接續共用任務頭。只寫 `audits/2026-10-09-n45-j/`。
讀E4 REPORT §6、E4C REPORT §1–2、Phase B §3.2及原capacity checker。
自己的backtracking／tuple join不import原checker決策邏輯；JSON的圖與邊可作輸入，
預存relation及結論只作比較對象。

輸入固定為BASE的 `artifacts/c5_excess_two_e4c/controls/*.json` 中19份m=2圖。
如需unit省略校準另用其餘controls已保存的12個45／54 core occurrences，標N1，
不混入N2目標控制，不搜尋新圖族。

1. 從原邊重建pieces、distinct／shared contacts、完整R_P。每個canonical proper框列查全部16有序pins，
   包括diagonal與空fibres；非空保存全圖lift。`J_G=(E_z×E_w)∩A_P∩A_Q` 與獨立整圖染色逐pair相等。
   原19圖共190列／3040 root-pair queries，derivative及額外校準另計。
2. 在完整join拒絕且E_s非空時，每個b∈E_s、兩個root方向核B-C2各項非負，
   `D^u+O^u+δ+o+λ=deg_G(r)−4`，χ=0且A=E_r。
   原G右側1；unit derivative降degree側0、另一側1。join接受或E_s空等情況標not triggered。
3. 對每條spoke及原單接點unary給精確derivative查詢，兩mixed原relation保持。
   spoke只移除原不等式；unary整份省略但保存其原relation與support metadata。
   提供具名source graph輸入介面，供S／U新控制返回後增量重算。
4. 列局部前提coverage及完整933／941、N2的45／54是否觸發。
   可保存原資料中的tuple-vs-marginal／shared坐標碰撞；沒有碰撞便列未覆蓋，
   不任意改relation後聲稱找到disk反例。

交獨立checker、inventory、證書、普通／seed17只讀重播及coverage。
本任務完成只代表工具與固定controls校準，尚未驗S／U新命題，
不能從19圖推來源不存在或任意大小枚舉完備。

### N45-A：共同前提與搬用邊界的獨立稽核

接續共用任務頭。只寫 `audits/2026-10-09-n45-a/`。只讀審BASE權威來源，不推新排除。
讀E3 REPORT §2.1／nonadjacent notes §2–5、E4 REPORT §4／§6、CORE_CONSTRAINTS §2／§4、
U4 §1–2、Phase B §2.1／§3.2、E4C REPORT §1–2。

每項判「成立且可搬用／需額外前提／缺口／反例」，附來源段落、量詞及證據層：

- 精確來源推triple-critical、全B-touch、m=2 root-deletions全收；不拼不同列q-core。
- 原degree4飽和的整piece全取／全不取；45／54只省一spoke或整unit unary，兩mixed原樣保留。
  U1–U4只排兩-root44，原55仍保留。
- E4-U先同Σ minimalize X再用E2、ε不增加，X與G的criticality分開。
- E4-D重色列限定；N-diagonal局部對角接受拼整圖仍需兩側E交集及joint。
- B-S0逐piece見證、one-sided、外路、原收費；U4的O11／retained44下界不當一般N2性質。
- B-C2在χ=0兩mixed的paper式與slack前提；checker未覆蓋域及控制觸發分開記錄。

新有限邏輯須獨立。原 `--check` 有歷史byte／provenance FAIL就保原FAIL與具名差異、hash。
需要fresh重建時使用新的exclusive輸出，分數學payload／provenance，不能覆寫舊JSON。
不無條件重跑大枚舉或全部上游分類。
交精確可用依賴清單及finding（ID、重現、影響、所需修正）。
首輪只審BASE；S／U返回凍結後，監督端另指定受影響CLAIM增量審閱。

## 5. 結果返回後的監督與第二批

管理狀態用「可發布／執行中／待補件／待交叉驗收／已驗收」，收到回報才更新。
執行者說完成先視為待交叉驗收；已驗收只限交付與CLAIM scope，不表示父命題CLOSED。

```text
同一BASE
 ├─ N45-S：spoke證明 ─┐
 ├─ N45-U：unary證明 ─┼─ 逐份凍結 → A增量paper稽核＋J增量有限核對 → 監督裁決
 ├─ N45-J：先做工具 ──┤
 └─ N45-A：先審依賴 ──┘
```

不必等四份全回才審已有交付。監督端依序：

1. 核BASE、输入hash及寫入範圍；版本不符／缺來源／缺full lift開具名補件。
2. 核各CLAIM量詞、全部假設、依賴與分層證據。共同前提失效即通知受影響任務，暫停相關宣稱。
3. S／U候選凍結檔案hash或交付SHA，A／J再在獨立輸出增量驗收。
   A核任意大小paper；J只驗有具名圖／可核證書的有限部分，沒有來源控制便保留缺控制。
4. 窄排除只關其子型；必要式保OPEN；反例辨是否觸發全部來源前提。
   finding開修正項，修後只重驗受影響CLAIM與版本。
5. 第一批交付裁決後才選一個最小residual作第二批。即使45／54身份全排且分類完備，
   仍只得「N2沒有45／54 core」，原55及無45／54來源須另證，不宣告N2來源全排。

採納後依 [DOCUMENTATION](../DOCUMENTATION.md) 更新canonical來源、guide相關子節及STATUS直接索引。
真正closure核直接父題／consumers，無上層語義影響便停在L2；HANDOFF／README不逐輪堆摘要。
此階段管理研究結果；commit／push或外部發布依使用者另行指示。

## 6. 統一回報格式

```text
任務ID：N45-S／N45-U／N45-J／N45-A
執行者狀態：完成／部分完成／待補件／finding
BASE完整SHA／實際HEAD／交付SHA（未提交則交檔案hash）：
輸出位置與REPORT／checker／證書／inputs.json／checks.json：
CLAIM-ID、精確命題／量詞、全部前提、依賴：
適用933／941／root交換／β／省略unit／support子型：
證據層：paper／外部定理／有限Python／Lean普通／native_decide
coverage：triggered and holds／not triggered／counterexample、缺失前提：
實跑命令／exit／seed／logs／hash；未跑項與沿用理由：
findings：ID、重現、影響範圍、所需修正
仍OPEN的精確residual及下一個最小義務：
輸入零byte漂移核對／修改檔案清單／Git狀態：
```

回傳順序不限。只有文字摘要先判scope，缺報告／來源／證書保持待補件。

## 7. 本次準備交付的驗證界線

本節保留首次派工準備時的驗證；後續J／A驗收、S／U預審見§3及各監督報告。
首次只新增任務文件及guide／STATUS入口，未新增數學結論。

| 實跑檢查 | 結果 |
| --- | --- |
| `python3 scripts/check_docs.py` | exit0；587份Markdown、6997本地連結，anchors／index／HANDOFF通過 |
| `python3 tools/docgraph --include 'docs/**/*.md' check` | exit0；62 documents、213 relations、5 families，0 errors／notes |
| `python3 tools/docgraph check` | exit1；62 duplicate-id errors，皆涉及 `scratch/task-c44-delivery/repository/docs/` 留存副本 |
| `git diff --check` | exit0 |
| `git diff --no-index --check -- /dev/null docs/history/2026-10-09-n2-45-54-parallel-tasks.md` | 2026-10-09監督核對更正：逐命令exit1，診斷為空；新增內容的no-index差異，不是whitespace錯誤 |

更正說明：首次把整段shell最後的exit0誤記成上述個別命令的exit；本輪已逐命令保存真實exit，
舊0記錄撤回。`git diff --check`本輪獨立exit0，新增檔另核沒有whitespace診斷。
全工作樹失敗保留，不把正式docs PASS當全域PASS；不刪scratch隱藏失敗。
纯文件準備未跑Lean或研究枚舉；Phase B原controls單次重播範圍見§1。
未commit／push，未啟動四個任務或代使用者對外發布。
