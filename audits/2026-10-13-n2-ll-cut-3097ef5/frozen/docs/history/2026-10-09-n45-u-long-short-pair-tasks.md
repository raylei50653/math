# N45 第二批：唯一原 U＋long／short pair 的三份並行任務

**後續（2026-10-10）：** 三份已返回，經三份獨立增量與[監督採納](../../audits/2026-10-10-n45-p-supervision/REPORT.md)
完成限定验收，N45-U-LP任意大小paper已排。下一singleton-support窄題見
[採納紀錄及發布文本](2026-10-10-n45-lp-adoption.md)。下文「未啟動」與派工hash是2026-10-09原任務快照。

2026-10-09。第一批與SU-A／SU-J增量已分層驗收，見
[採納裁決](../../audits/2026-10-09-n45-su-supervision/REPORT.md)及
[權威入口](../c5_excess_two_nonadjacent_unit_core45.md)。
只選 **N45-U-LP**：指定整份原unit U省略的45／54 core、唯一原U、
一long mixed L、一short edge-pair mixed S。幾何、跨列關係與來源契約工具
三路各自從已採納前提出發，沒有互相等待的新結論依賴。
以下是可發布文本，尚未啟動；使用者各發布「共用任務頭＋一份任務全文」。

## 1. 共用任務頭

```text
根目錄：/home/ray/developer/ai/math
BASE：dc8e9aa7d6fccb51f63d30aa3f9c132296d44744
從BASE使用自己的clean checkout／worktree，先核HEAD／Git與BASE HANDOFF、STATUS、DOCUMENTATION。
本輪新前提以指定frozen交付及以下N45權威頁為準；不把未提交新頁冒稱BASE Git blob。
新source：docs/c5_excess_two_nonadjacent_unit_core45.md
SHA256：d27e84297a20a14e793bd74d4d223983e67e9b4378eb22f3c6b17bfe4a895462
S原REPORT SHA256：51ea0e8406998e0a2f8dda8edf785e3a67cbeee412cc8a5d3272430bd0138fa1
U原REPORT SHA256：0c3d117f1c804bc0695fc97fd570f2ede6451d5a21ca036f337f4d11c5de72a7
U final certificate SHA256：1f7dc2f13fa372150f2d915fd10494986c2f0a3aa08fa965c8b2f013315980d0
SU-A REPORT SHA256：6a2fbd8d1c2225265dd053070ed59e3e4dd129d9ba825090d197ce0c088820ca
SU-A independent judgment SHA256：97ba9e80fedeb1fef95c767f525b17ffde6e676cd4b06131a8b295741ac95872
SU-J REPORT SHA256：b09822e90beff372b54653b42674035c0568dee886b6389c14e3b98ff0ebad24
SU-J certificate SHA256：a4b5b4c148f823f8df22a2672700eb40516bae0fd673edf8210a477af3b508ee
J certificate SHA256：ecdef656ec2eff887c6725cda21a6d205fce41e5387ce14b2270468f20a861d4
先核上述hash與精確manifest；BASE數學依賴對Git objects，不混讀主worktree後續header。
權威新頁導向S/U、SU-A、SU-J及supervisor；paper與finite的適用範圍分開。

G為任意大小有限簡單disk圖，ordered induced C5 B=(b0,...,b4)為外面；
完整Σ(G)=933/941或共同搬運整圖的D5像，非框Σ-critical，epsilon2。
恰兩個非相鄰原degree5 roots r,s，其餘有效內點原degree4，full B-touch。
H−{r,s}恰兩完整mixed L,S與唯一原unary U。
U唯一原root-contact為rx，X=G−V(U)=M是原拒絕beta的inclusion-minimal45/54 core，r降度。
L原support long；S原actual support恰某框邊的兩個端點，不含singleton分支。
保原具名contacts/shared identity、attachments/support、ownership、原bridges/rotation、
共同字面beta、完整tuples/fibres/空fibres/full lifts；root交換與D5只能搬整圖。

已採納：原盾弧(U,L,S)長度恰(2,2,1)、分割五框邊，U/L原support各連續三點。
原incidence：t_r+k_L^r+k_S^r+1=5，t_s+k_L^s+k_S^s=5，各mixed兩側正。
core beta：X保留spokes色各側互異，共同未用色D在兩側E；short接受(D,D)，long必禁止。
每個b∈E_s，L/S原完整禁色欄滿額、互斥，union=E_r^X，五項zero slack。
Delta=Σ(X)−Σ(G)非空：941至少1列、933至少2列；
每個gamma∈Delta，原U contact palette與全部X lifts的r投影同singleton。
同Sigma epsilon1 minimalization給Q(X)空/單點/相鄰pair，core beta必在Q(X)，保933 q2。
不同列的geometry可同原圖收費，禁色不能跨列相加；不由marginals或各piece色名置換拼source。

只寫自己的下列fresh目錄；新檔exclusive-create，已有目錄/檔則改具名版本並回報。
不改共享文件、其他任務/worker/supervisor輸出、舊證書與source副本；不刪歷史FAIL。
不commit/push/PR/對外訊息，不委派sub-agents，不擴大k或廣域graph枚舉，不重開U1–U4。
singleton short、S LOW/HIGH/long、原55/其他core/一般N2/E不在本輪。
每項有CLAIM、量詞、全部前提、依賴、證據層、coverage缺前提、未涵蓋範圍及finding。
至少交REPORT.md、inputs.json、checks.json、完整hash清單與逐命令exit/log。
新finite計算另交checker/certificate與normal/seed17只讀重播；不假造Lean或source實現。
若需要未證任意大小有限化約，交精確lemma義務停止，不以模板零survivor當一般排除。
歷史E4 provenance FAIL、fresh BASE兩缺檔、whole-worktree duplicates分列保留。
```

## 2. N45-PG：原五盾邊分割與 root／附件幾何

```text
任務：N45-PG
輸出：audits/2026-10-09-n45-pg/
讀U REPORT WIT/U2/RES、SU-A對應逐claim與N45權威頁§1–3，
BASE E3 nonadjacent、E4 §4/6、原unary shield及Phase B B-S0。

在N45-U-LP前提下，重新畫同一原圖的盾弧2+2+1與outside面。
先列whole-frame D5/root swap允許的named shield partition，禁止逐piece独立正規化。
由實際root-contact、one-sided與原外路推原roots的可處面、spokes可落的框點、
shared contacts/bridges及跨盾弧附件的限制；若只是必要identity，保完整原拓撲。
探求一項任意大小的幾何排除或可搬用拓撲lemma，優先原minor/subdivision或面分隔。
若用K5/K3,3，交原vertex互斥bags或具名paths，核連通/互異/每條原邊；
只作非平面證明，不把收縮當coloring replacement。
若需G−piece outside witness，逐原critical contact供給，不假設X full B-touch。
若幾何仍可行，交最小精確profile與缺失的原graph obligation；
明列哪些是proved necessary，哪些只抽象可行，不能宣稱source存在。
不等待PR；可獨立用已採納跨列條件，但不能假設其新結果。
若排除成功，只關N45-U-LP，不排singleton branch或全部U/N2。
```

## 3. N45-PR：同一原圖十列完整接合與新列 forcing

```text
任務：N45-PR
輸出：audits/2026-10-09-n45-pr/
讀U REL/CROSS/CAP/RES、SU-A對應裁決、BASE E2同Sigma minimalization、
Phase B B-C2、E4完整relation介面。幾何只用已採納2+2+1，不等待PG。

同一原G的每個proper literal beta，保R_U/R_L/R_S全部ordered contact tuples及full lifts。
將core beta的五項zero slack、每欄L/S精確分割、long禁止(D,D)，
與同一X新gamma的U palette=全部X r-projection singleton一起施加。
共同搬運whole frame後，覆蓋941與933的七格Q(X)必要表，保933 q2與root交換。
不能逐列選另一個piece relation、使用端點marginals、各piece独立S4，或把不同列容量相加。
嘗試證任意大小跨列矛盾，或一個有明確充分前提的relation transport/forcing lemma。
不把靜態完整relation equality當specified-colouring repair；若用replacement，
須證原named interface、private interiors、attachments、literal frame與原geometry皆保。
若只得到必要tensor/profile，列真實same-source可實現義務；
抽象relation table、mask一致或有限零survivor都不能作source排除。
沒有任意大小正常形時不枚舉新pieces、不開k上限；交具名最小residual並停止。
若找到碰撞，交完整原graph/rotation/relations/lifts，逐項核target/criticality/core身份；
不滿全部前提只叫abstract/control碰撞，不能叫來源反例。
```

## 4. N45-PC：N45-U-LP 完整來源契約的只讀有限 validator

```text
任務：N45-PC
輸出：audits/2026-10-09-n45-pc/
從已驗收J/SU-J介面出發，自行寫或精確延伸只讀來源契約validator；
不 import PG/PR未返回判定，沒有新proof候選依賴。

對具名原graph/rotation與declared U/L/S、literal beta，分欄核：
ordered induced C5 disk/原degrees/rs不存在/fullB-touch/完整分量/one-sided、
唯一incidence-one U、原L long/S真框邊pair、盾弧2+2+1及五邊分割；
完整10-row Σ target(含wholeD5)、逐非框critical witness、X=整U省略、
beta拒絕與每條retained非框邊刪除可接受的beta-minimality。
重建原contacts/shared coordinate及完整relations/fibres/full lifts，
同beta的zero slack/滿額分割與所有Delta gamma的singleton forcing另核。
每層分類triggered and holds/not triggered/counterexample，列缺的充分前提；
不得給「沒有觸發即PASS來源排除」的aggregate status。

首次只讀現有19 N2與7份N2整U省略；另4份N1整U只列介面校準，絕不補N2 coverage。
監督初筛：現有固定N2沒有完整「唯一unit U＋long＋short pair」幾何控制，
更沒有精確933/941拒絕45/54控制；你須獨立核此0觸發，而不是補造positive sample。
本工具的新增价值是能對後續具名source proposal逐條fail-closed查契約，
不是再次宣稱原7200pins重播等於新paper驗收。
保留至少兩項可重現negative input檢查，例如完整relation漏tuple/錯shared ownership、
相同graph下的stale source hash或错误declared unit omission；
必須拒絕錯資料，且以原合法lift/完整原edge為oracle，不是implementation鏡像測試。
negative改動只寫本fresh目錄副本，不改原證書，不能叫数学source反例。
固定控制若無LP契約前提，就明列缺控制；不擴大graph/k搜尋，不找新source。
交獨立checker/certificate、normal/seed17只讀replay、exclusive-create guard及hash inventory。
```

## 5. 返回後的監督順序

| ID | 狀態 | 返回後用途 |
| --- | --- | --- |
| N45-PG | 可發布；未啟動 | 核原拓撲lemma或新精確profile，先判是否真正涵蓋任意大小LP |
| N45-PR | 可發布；未啟動 | 核完整同源跨列lemma，與PG的充分前提逐項交叉 |
| N45-PC | 可發布；未啟動 | 驗工具的具名來源契約與負控制；不裁決paper |

返回即凍結hash，監督先核版本/寫入/coverage。paper候選另指定獨立增量審閱，
PC只驗真實具名source的有限部分，0觸發不阻塞可獨立成立的paper證明。
成功只採納N45-U-LP或明列更窄子型；新必要式仍OPEN。
未完整覆蓋任意大小分支前不選下一個新residual、不更新一般N2/E為CLOSED。
commit／push與對外發布依使用者另行指示；本文件只準備可審、可發布的任務。
