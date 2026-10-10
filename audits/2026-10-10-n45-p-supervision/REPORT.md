# N45 第二批：監督驗收、LP 採納與進度整合

2026-10-10；BASE／實際 HEAD `dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。
使用者交回 PG／PR／PC並要求繼續監督；本輪先凍結三交付、核版本與重播，再安排互不讀新判定的
PA／PGA／PCA獨立增量審閱，最後只按封存裁決採納。所有 worker及獨立稽核目錄保留原 bytes。

**正式採納 N45-U-LP 的任意大小紙面排除。** 只限指定原身份及下列全部前提／明示信任依賴。
PG必要幾何、PR五個relation lemmas、PC有限工具各在自身前提內採納；一般N2／E保持OPEN。
當前權威入口是[N45](../../docs/c5_excess_two_nonadjacent_unit_core45.md)。

## 1. 版本、獨立裁決與採納範圍

| 交付／獨立增量 | 正式裁決 | 限界 |
| --- | --- | --- |
| [PG](../2026-10-09-n45-pg/REPORT.md)／[PGA](../2026-10-10-n45-pga/REPORT.md) | PG01/02/04/05原paper成立；PG03原路／Jordan／bridge成立；PGRES必要算術成立 | 八張embedding只作abstract minor；56不是survivors/source；排單頂點S僅指edge-pair支援 |
| [PR](../2026-10-09-n45-pr/REPORT.md)／[PA](../2026-10-10-n45-pa/REPORT.md) | 15個獨立子裁決成立；採納N45-U-LP及五relation lemmas各自範圍 | 明依BASE紙面三分與外部Gallai；ENDPOINT單獨引用须完整原piece、全部內鄰為指定owner roots及完整degree4 |
| [PC](../2026-10-09-n45-pc/REPORT.md)／[PCA](../2026-10-10-n45-pca/REPORT.md) | 固定有限交付、完整原邊獨立核算與已觀察fail-closed路徑採納 | 19N2三項0觸發／4N1校準另列；完整LP exit0正分支、一般validator soundness未認證；無paper closure |

三份獨立裁決先封存後返回；本監督讀完整論證及前提映射，另核其精確清單與原輸入。
PGA未讀PR/PC新判定；PA未讀PG/PC；PCA未讀PG/PR；各自沒有用監督的新判定作證。
獨立同源核算不等於任意大小來源實現，工具也不負責證明紙面拓撲。

## 2. LP 命題、完整前提與任意大小對接

量詞為任意大小有限簡單原disk G，有序induced C5 B為外面；完整Σ=933/941或整圖共同D5像，
每非框邊Σ-critical、ε2、有效H連通／full B-touch。恰非相鄰原degree5 roots r,s，其他有效
內點完整degree4；H−{r,s}恰唯一原unary U及兩完整mixed L,S，pieces one-sided／support非空。
U唯一contact rx，X=G−V(U)=M是原拒絕literal β的inclusion-minimal45/54 core，r降度。
L actual support long，S actual support恰真框邊兩端；原盾弧(U,L,S)=2+2+1分割五邊，
U/L support各為連續三點。原ordered contacts、shared單一坐標、attachments/support、ownership、
bridges/rotation、同一字面色框、完整tuples／空fibres／全部full lifts固定。

PA獨立重推並封存以下前提鏈：

1. 原U盾中點m不被H−U碰到，故X中的m無內鄰；X繼承T4，在同一完整lift只改回m，
   得Q(X)={m}、β=q_m，保933 q2。941／933的Δ分別恰2／3列。
2. 使用X=M自己的β-minimality；r只失rx成4，s仍5，其餘retained內點完整4。
   C=H_X−s={r}∪L∪S是唯一實際連通分量；沒有合併頂點、改圖或拆shared坐標。
3. β=q_m的其餘四框點只有兩色，spokes重色會違X minimality，故t_s=0/1/2。
   完整C非空relation與刪spoke witness给F_C=Col−β(N_B(s))。
4. BASE no-spoke(5)§4、single-spoke(4)§1–5、two-spoke(3)§1–5逐一全排。
   t0不需C外s–B路；t2允许任意兩條β異色spokes。全部ordered interfaces與full lifts保原。

信任界：原shield／未接框點改色／BASE三條具名任意大小paper，以及外部Dvořák
Lemma7／Theorem10。PA另核Git凍結primary PDF與第5／6頁陳述；沒有重證外部分類的全部證明。
沒有新任意大小有限正常形假設、graph/k枚舉、來源實現或Lean theorem/native_decide。
七格／150 masks／14相容項／42單-root條件分支是紙面覆蓋帳，沒有把它們叫來源圖。

## 3. Integrity 與本輪實際重播

[review.py](review.py)只用標準函式庫，不import worker checker；對回精確inventory、Git BASE與
原bytes/mtime，另將每個子命令實際exit及完整stdout/stderr寫入本目錄logs。
它不裁決任意大小paper，也不是另一個整圖solver。獨立solver由PCA提供。

| 證據封存／核對 | 實際範圍 |
| --- | --- |
| PG／PR／PC三份原manifest | 6008／6061／6026項；exact regular inventory與所有SHA256相符，receipts另核 |
| 共用authority | 九個派工anchors核原件與可用worker frozen bytes；135個unique BASE paths逐byte對Git objects |
| PA／PGA／PCA新manifest | 42／66／311項；精確payload及receipt hashes核回，裁決前提與source版本對回 |
| worker normal／seed17 | PG checker.py、PR checker-final.py、PC checker.py各exit0，證書bytes核回，stdout各對相等 |
| PC五錯資料與合法缺LP | 五個counterexample finding各exit2且expected reason吻合；合法缺LP exit2／not triggered，保missing欄 |
| PGA獨立checker | 根監督另重播exit0；10 partitions／27原袋間邊模型／60模板／8抽象embedding／56必要profiles |
| PCA獨立checker normal／seed17 | 根監督另重播各exit0；23原圖、11整U、690relations／2986lifts／555critical edges完整一致 |
| PCA fresh probes | 獨立稽核實跑六項缺／錯rotation、漏空fibre、漏component、錯L support、空critical witness宣告，各预期exit2；五舊負控制與合法缺LP另列 |
| 原件零漂移 | worker全部regular payload、symlink targets/mtime與所列共享輸入在重播前後相同；管理更新另記，未冒稱新authority仍是舊hash |

正式證書入口：PG certificate.json；PR certificate-final.json；PC certificate-final-v2.json。
原初版、空檔及開發失败保留，没有改寫成PASS。

```sh
python3 -B audits/2026-10-09-n45-pg/checker.py --check
python3 -B audits/2026-10-09-n45-pr/checker-final.py --check
python3 -B audits/2026-10-09-n45-pc/checker.py --check
python3 -B audits/2026-10-10-n45-pca/independent_checker.py --check
```

上述四入口本輪亦各以PYTHONHASHSEED=17重播；root命令／exit在logs，
三增量原命令及exclusive-create／探索包裝failures留在各自封存，沒有覆寫舊證據。

PC有限三項仍0觸發：19N2無完整LP幾何／targetΣ；7整U皆X全Σ1023，無拒絕45/54 core。
4N1只作校準，4個拒絕core／zero slack與4個新γ不補N2。混合long endpoint与forcing d_r=1
正控制仍缺；paper各自適用性由PA裁決，沒有由缺控制推出成立或反例。

## 4. 文件檢查、管理diff與保留失敗

三份原封存的fresh BASE兩缺檔、whole-tree duplicate-ID FAIL及歷史E4 provenance FAIL均保留。
本根監督fresh重跑BASE check_docs：exit1，586 Markdown／6982 links、恰兩歷史missing paths；
正式docs DocGraph在管理前exit0：62documents／213relations／5families／0errors。
管理後實際文件檢查、完整stdout與exit另記logs與[integration-checks.json](integration-checks.json)；
正式docs PASS不改稱whole-worktree PASS。沒有補造歷史缺檔或刪source副本來改綠。

| 管理後本輪實跑 | 實際結果 |
| --- | --- |
| 主worktree check_docs | exit0；590 Markdown／7079 local links，anchors／index／HANDOFF通過 |
| 正式docs DocGraph | exit0；62 documents／213 relations／5 families／0 errors |
| whole-worktree DocGraph | **exit1；62 duplicate-ID errors**，全部source副本保留 |
| tracked git diff --check | exit0；本新增report／history／JSON／links另核，不以tracked check代驗untracked文字 |

主worktree與fresh BASE是不同輸入；主worktree既有歷史檔案可被找到，不會改寫BASE兩缺檔的FAIL。

根首次inventory將既存dangling BASE symlink當regular payload而exit1；
[bootstrap-failure.json](bootstrap-failure.json)保留原因，修正為匹配regular manifest並另記symlink。
没有改任何worker，也没有已寫input snapshot被覆寫。

未跑lake build／axioms（無Lean源或新形式化claim）、全上游分類／E3/E4大枚舉、U1–U4或remote CI。
初始與重播後共享bytes在inputs-before／after保存；後續採納管理diff與新authority SHA另封存。
既有四份tracked修改保留，本輪只更新與此窄結果有關的區段；沒有commit／push／PR或外部訊息。

## 5. 傳播與下一窄題

Closure scope：只N45-U-LP原pair支援／整U省略45/54身份。Canonical Source＋Evidence：N45權威入口，
連PG/PR/PC及PA/PGA/PCA與本監督裁決。

- Updated：N45 source／Kempe相關子節／STATUS；直接父E4頁首後續與§4.3入口、Phase B B-S0 consumer；
  原第二批歷史只加有日期後續，原任務全文／pins與未啟動語境保留；新採納暨下一題歷史另存。
- Reviewed-unchanged：E4當輪三列族表／原CORE_CONSTRAINTS、E3原化約、U1–U4、跨線common language。
  本paper不改原三列量詞或原控制，父N2仍OPEN；HANDOFF／README研究線與入口不變。
- Remaining OPEN：U唯一U＋long L＋singleton-support S；S LOW／HIGH／long、原55、其他cores、
  無45/54來源、一般N2/E、ε≥3；PC完整LP正分支與generic soundness／來源實現未認證。
- Propagation stop：L2。直接父題與consumer同步窄效益，父題與跨線語義未變，停止向L3擴張。

下一題只選 **N45-U-SS**：先獨立核singleton-support S下原U盾弧2/3的內點限制與
整U省略後的實際sole C，判斷已採納LP對接能否在此新前提下搬用。
明列原盾費(U,L)=(2,2)/(2,3)/(3,2)，不擅把LP theorem視為已證此任務外圖類；
不開k或廣域graph搜尋。[發布文本](../../docs/history/2026-10-10-n45-lp-adoption.md)已備，尚未啟動。

完整input envelopes、incoming audit hashes、管理diff、檢查與delivery見本目錄；
root與三獨立審閱者只新增／管理明列範圍，全部原worker輸出及舊FAIL不改。
