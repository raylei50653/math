# N45-S／U 返回後：兩份可併行的增量交叉驗收任務

2026-10-09。使用者可各別發布「共用任務頭＋一份任務全文」。
這是第一批增量驗收，不開第二批新研究；兩份無互相等待依賴。
[S監督預審](REPORT.md)及[A／U批次裁決](../2026-10-09-n45-batch-supervision/REPORT.md)
已完成新紙面預審與固定控制重算，執行者須獨立判定。
使用者隨後回傳A及U，因此合併原S增量安排為以下SU-A／SU-J兩份，尚未啟動。
N45-A 首輪只審 BASE、N45-J 首輪只驗工具，均不自動涵蓋 S／U 的新紙面 claim。

## 共用任務頭

```text
根目錄：/home/ray/developer/ai/math
BASE：dc8e9aa7d6fccb51f63d30aa3f9c132296d44744
先核 HEAD／Git，讀 BASE docs/HANDOFF.md、STATUS.md、DOCUMENTATION.md。
研究前提及證據分層沿用 docs/history/2026-10-09-n2-45-54-parallel-tasks.md §2。
只讀 BASE 來源及以下凍結交付；共享導航是未提交管理更新，不作 BASE 數學來源。
不改共用文件、S/J/A/U 原目錄、舊證書；只寫各自下列 fresh 輸出目錄。
不得覆寫既有輸出；已存在則改用新具名目錄並回報。自行完成，不委派 sub-agents。
不 commit/push/開 PR/對外訊息，不擴大 k 搜尋，不重開 U1–U4，不推一般 N2 排除。
每個結論列 CLAIM、量詞、原圖前提、依賴、證據層、未涵蓋範圍與 finding。
完整 Σ／paper／有限 Python／來源實現／Lean 分開；同原具名 contacts、shared identity、
actual support、ownership、bridges、rotation、字面 β、完整 fibres／空 fibres及full lifts不丟失。

凍結 S：audits/2026-10-09-n45-s/
REPORT.md SHA256：51ea0e8406998e0a2f8dda8edf785e3a67cbeee412cc8a5d3272430bd0138fa1
checker.py SHA256：94b3fb13e8268080e80a441f595fd3fcab449ea2c2937b2bf92c1725e5977dae
certificate.json SHA256：9acb2a6b40de32aeca60ecf9a5b33065c9cba60ad47f5243c1eccadf31f59a02
inputs.json SHA256：09aeaaa919c299c5a8c3ed44ef250e6e90a96ab1040e3fd8bea6fbc57b1e63de
先核 S delivery.json 的21項精確inventory/hashes，再另核delivery.json自身hash與監督inputs.json。
S 69份來源须對 BASE Git objects 或指定clean BASE checkout核bytes，不能只信保存PASS。
凍結 U：audits/2026-10-09-n45-u/
REPORT.md SHA256：0c3d117f1c804bc0695fc97fd570f2ede6451d5a21ca036f337f4d11c5de72a7
checker.py SHA256：37da93a6fe6109f82287eac67db518515b6718c30013f020acfd21e6364162e3
certificate-final.json SHA256：1f7dc2f13fa372150f2d915fd10494986c2f0a3aa08fa965c8b2f013315980d0
inputs.json SHA256：ed32a320d7924af82f87fbbe78c12a667fb34222299414ac4fb4839b6895355d
U 70份權威來源對BASE核bytes；39份authored檔凍結於批次supervision/inputs.json，
source/獨立BASE checkout分列。初版certificate.json、failed attempts與路由漂移保留。
N45-A首輪9項依賴已驗收：audits/2026-10-09-n45-batch-supervision/REPORT.md §1。
原A的4 findings及歷史E4 provenance FAIL仍保留；新S/U claim必须另外稽核。
J frozen certificate：audits/2026-10-09-n45-j/results/certificate.json
SHA256：ecdef656ec2eff887c6725cda21a6d205fce41e5387ce14b2270468f20a861d4
J原工具驗收：audits/2026-10-09-n45-j-supervision/REPORT.md。

至少交 REPORT.md、inputs.json、checks.json、完整輸出hash清單，逐命令exit/log及未跑理由。
有新有限計算另交獨立checker/證書、普通及seed17只讀重播；新檔exclusive-create。
原文件／provenance FAIL照實保留，禁止覆寫或刪副本把FAIL變PASS。
回報 BASE/實際HEAD、CLAIM裁決、coverage缺前提、finding及輸入零漂移；不只說完成。
```

## N45-SU-A：S六項／U八項新 claim 的獨立紙面增量稽核

```text
任務：N45-SU-A
輸出：audits/2026-10-09-n45-su-a/
讀 S REPORT §1–7，逐條審 N45-S-01–06；不得只重述首輪BASE依賴稽核。
先獨立形成判定，再對監督預審 REPORT §2／§2.1。

01：同Σ minimalize derivative的ε不增公式、X=M的β-critical⇒Σ-critical、
    933 q2與941 q0/q1/q3的完整Q(X)必要域、新接受列deleted-spoke同色full lift。
02：非空局部完整relation、shared contacts同時避色、E_s>0，B-C2在χ0/degree4
    逐欄五項零slack，不偷換為marginals或只核一欄。
03：c∈E／c∉E blocker二分及原degree5一單位预算；unary blocker不能用重色spoke E4-D。
04：singleton support固定c的S3色軌道、全部diagonal的原G fullB-touch/N-diagonal前提、
    兩方向contact界；只能排總incidence≤3，不能提升一般mixed至少pair。
05：兩short得到m_r+m_s≤5再排singleton，每個原unary的拒絕見證/one-sided/避自身外路，
    原盾弧1+1+2+2及含long的2+2+2窄排除；不得對spoke收piece費。
06：重新核原H−t連通、三spoke star唯一長3面、三份原盾弧都在此弧內的拓撲步驟，
    不借U4 retained44/O11下界；核LOW/HIGH原incidence与E域，仍屬必要身份。

用 BASE E2、E3 nonadjacent notes、E4 §4/6、CORE_CONSTRAINTS、Phase B §2/3.2、
原unary shield及Dvořák Lemma7/Theorem10原始來源核適用性，列沿用／本輪重新核的邊界。
每項判成立且可搬用／需額外前提／缺口／反例；finding要具名精確到推理步與受影響CLAIM。
若全過，只關指定spoke-omission原u2子型，LOW/HIGH/long/原55/一般N2仍OPEN。
不需要新增Lean或重新跑全部上游枚舉；缺精確target正控制須記，不能當紙面命題PASS證據。

再獨立讀U REPORT §1–7，逐條核以下八項，不因A首輪或S預審而省略新步驟：
REL：完整U唯一contact relation非空、F允許空；刪contact與整U省略精確root-pairs等價，
     新接受γ的全部X lifts与U palette同singleton；不能推core拒絕β的F非空。
WIT/CROSS/CAP：逐原critical-contact witness/避自身外路/原盾弧收費；保同Σ minimalize、
     933 q2必要表；χ0低度側逐欄五項零、恢復U的D/O/lambda三分，不能跨列加費。
S3：總root incidence≤3的原mixed、fullB-touch、one-sided及critical-contact witness，
    重新核Gallai的K4 block四支tethers、握手式、末端private點計數、最後triangle的原K5 minor。
    另核批次supervision REPORT §2.1 的N-empty/diagonal/S3色軌道交叉論證；不得先假定新claim。
U2：兩原unary先排long，X拒絕兩short給總mixed incidence≤5，再依S3收1+1+2+2；
    原U即使省略仍收原費，不套U4 retained44/O11支援下界。
SHORT：排兩unary後X無unary，共同未用色D接回兩原short；不假定X fullB-touch。
RES：唯一被省略U+一long/一short的必要incidence、盾長、L禁止(D,D)、β逐欄滿額與Δ forcing。
    pair S是(2,2,1)盾長；singleton S incidence≥4仍OPEN，完整同源跨列未排。

核S/U原u2窄排除的不同前提與其剩餘身份是否正確；比較S04與U-S3只搬實際充分前提。
逐claim返回獨立裁決，若全過U只關指定整U省略的u2和兩short子型，餘唯一U+long/short仍OPEN。
```

## N45-SU-J：S／U固定圖與抽象介面的獨立有限增量核對

```text
任務：N45-SU-J
輸出：audits/2026-10-09-n45-su-j/
只驗S/U新有限證據；不承擔S-01–06或U任意大小paper及來源排除。
讀S checker全碼/certificate及J已驗收工具接口；不得import S checker或監督review決策。
只重算已凍結輸入及指定表，不生成新圖搜尋。

1. 獨立重建288份singleton色置換軌道/完整16pairs；核92份接點界成立與196未觸發，
   特別核低incidence只留通用relation。分清接點界觸發與graph/source前提觸發。
2. 核3份抽象容量模型全部16pairs/空pairs、4容量欄、zero-slack與spoke blocker二分；
   模型缺具名graph/full lifts/Σ-critical/targetΣ/minimality，保持「非來源控制」。
   核12份incidence必要scalar、933/941完整Q(X)必要表，不宣稱disk實現。
3. 從原邊核19份N2與原piece identities/support/rotation，獨立查190份fullΣ rows及
   47份原spoke×原拒絕row derivatives；與J完整16root-pair fibres及S full lifts對。
   同時驗空pairs；47全部接受時記目標來源not triggered，不把無來源反例當一般paper驗證。
4. 不能用N1的12個45/54 occurrences補N2正控制，也不能拿非拒絕derivative觸發degree4容量式。
5. 正常/seed17只讀重播、新輸出exclusive-create，原S/J全檔bytes與mtime前後零漂移。

U增量：只用其固定23圖（19N2+4N1），不搜索新圖。
6. 從原邊核3680個original pins、11份整U省略的1760 pins、原唯一contact刪除的1760 pins，
   包含空fibres；整U X与G−rx root-pairs相等，vertices/full lifts分列。
7. 全690份local tuples及fibres、2986份piece lifts核原contact/shared identity，與J對回。
   新接受γ的U contact palette与X r投影必同singleton；38個F空列保過強版本負控制。
8. 核原G90/X12共102個容量欄、4份N1低度側lambda placement；D/O與N2拒絕X缺控制分列。
   22個小incidence支援instance只核必要式，不能代證S3的無界Gallai反證或U2/SHORT排除。
9. 核七格完整target Q(X)必要表與15個非空contact palette算術；不宣稱圖實現。
   正常/seed17只讀重播後，S/U/J authored與BASE輸入前後零漂移。

獨立實算完才對監督review.py/results作差異分析；需人工修正時只開finding，不改原證書。
保留fresh BASE docs缺兩歷史目標及全worktree DocGraph duplicate-ID FAIL；
正式docs PASS、來源bytes PASS與有限payload PASS分開報。
返回精確查詢數、full lifts、觸發/未觸發/反例及未檢查paper範圍。
```

兩份回報後由監督端對回凍結 hash，處理 finding，再裁決 S／U 正式採納與第一批下一個 residual。
