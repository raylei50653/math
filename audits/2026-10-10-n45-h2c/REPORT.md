# N45-H2C：HIGH2 artifact 與有限工具獨立稽核

2026-10-10。BASE `dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。
本端只寫 `audits/2026-10-10-n45-h2c/`，遵循
[audit contract](frozen/routing/audit-contract.md)與[H2C task](frozen/routing/h2c-task.md)。
HIGH2 的 [worker REPORT](frozen/worker/REPORT.md)、[12 claims／H1–H13](frozen/worker/claims.json)、
[正式任務全文](frozen/worker/frozen/current/audits/2026-10-10-n45-high1-supervision/high2-task-body.txt)
已完整讀取；不借 H3R 或其他 sibling 結果裁 HIGH2。

裁決：**限定 artifact acceptance 候選成立；不裁十二項無界 paper claims，也不自行採納。**
結構化範圍、逐 claim 界線與 provenance 限制見
[independent-judgment.json](independent-judgment.json)。
沒有建立／執行 finite HIGH2 source，trigger_count=null；沒有新 Lean 或一般工具 soundness 證明。

## 1. Intake、payload 與原資料

先逐檔核原 worker 與父端 frozen intake 的完整 118 regular files：
kind、bytes、mode、SHA256 全一致，無 symlink 或額外 regular file。
本端另凍結全部 118 檔，沒有重寫原 worker／舊 H3R／parent／shared。
[input-index](input-index.json)保存精確原 tree 與父端 frozen 路徑。

正式 worker [manifest](frozen/worker/manifest.json)恰列 115 payload，
只排除 exact top-level `manifest.json`、`delivery.json`、`receipt.json`。
`negative/nested/manifest.json`、`negative/nested/delivery.json`、
`negative/nested/receipt.json` 三者全是 payload。
每項 payload 的 bytes／SHA256 與 intake、原 worker、本端 frozen 一致。
[delivery](frozen/worker/delivery.json)綁 manifest／inputs-final／certificate；
[receipt](frozen/worker/receipt.json)綁 manifest／delivery，兩個真實 seal 子命令及其完整 stdout／stderr。

[41 frozen inputs／8 pins](frozen/worker/inputs-final.json)獨立核回：
22 BASE blobs、19 current origins、八 live pins、HEAD=BASE 全一致。
[initial authority check](authority-check-initial.json)保存逐檔結果；沒有刷新原 pins。
凍結官方 Gallai PDF 的 bytes/hash 也由完整 payload 核回；其數學定理在 H2C 範圍外。

## 2. 完整 receipts、失敗及實際重播

逐一核 17 個 worker log receipts 與其全部 34 stdout／stderr streams：
每筆 command、cwd、environment、exit、stdout／stderr hashes，皆與
worker checks.json／checks-final.json 的對應 records 相同。
另核 top-level receipt 的兩個 actual seal `--check-payload` 子命令：
normal 無 hash seed、seed17 明列17，cwd 為 canonical repo root，exit0、輸出同 bytes。

本端 [actual-checks](actual-checks.json)另跑以下四個正式 read-only 命令：

```
python3 -B audits/2026-10-10-n45-s-high2/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-10-n45-s-high2/checker.py --check
python3 -B audits/2026-10-10-n45-s-high2/seal.py --check-delivery
PYTHONHASHSEED=17 python3 -B audits/2026-10-10-n45-s-high2/seal.py --check-delivery
```

四筆皆 exit0、stderr 空；checker normal／seed17 同 stdout bytes，seal normal／seed17 同 stdout bytes。
完整 actual argv／cwd／environment／開始時間／exit／streams／hashes 在 runs 內 exclusive 保存。
環境明列 `PYTHONDONTWRITEBYTECODE=1`、`GIT_OPTIONAL_LOCKS=0`；normal 先移除 hash seed。

[worker tree before](worker-tree-before.json)與[after](worker-tree-after.json) bytes 完全相同，
118 檔的 kind／bytes／mode／hash 全部保持；tree digest 均為
`344ec5462f615d6891fdd3a485e012fda71f6160b3126acb0adde84d9031ee06`。
完整 certificate 保原 5,775,010 bytes／SHA256
`124b85f922c53e76d80b4c2e395bbecff9b6a9192491e66ecee120d347db575a`。

保留首版 checker-v1.py 與 generation receipts：初版在 BASE mapping 階段 exit2，
尚未生成 certificate。後續 generation-v2、原失敗、exclusive generation 拒絕皆照原 bytes 留存。
沒有把初次 local missing-link、optional BASE freeze finding、outside FAIL 或 DocGraph FAIL 移除。

worker 三個 `python3 -B -` helper receipts（Gallai byte check、input custody、nested negative）
沒有記其 stdin 程式 bytes/hash。H2C 核的是保存的 argv、streams 與結果 bindings，
不宣稱可逐 bytes 重播這三份歷史 stdin 程式。本端以具名 verifier 重核 inputs，
並以正式 seal stdin interface 重做 nested negative；無法恢復的歷史 helper 程式 provenance 明列為限制。
此限制不影響上述具名 checker／正式 delivery 的本端 actual replay。

## 3. 獨立 toy 的原 edges、完整 fibres 及 lifts

[verifier](verifier.py)沒有 import worker checker 或沿用其 brute-force toy 函數。
從 frozen certificate 的具名 vertices、全部原 X edges／actual attachments 重建圖，
以一般遞迴 solver 選最小剩餘色域並列舉完整 assignments；坐標最後按原頂點排序。
由原 edges 重建 H_X−s 的實際 C=(r,p,q1,q2)、U=(uL,uR)，
保兩個 shared r/s contacts p、q1 的單一變量及原 U 邊 uL–uR。

實際完整範圍是同一固定 toy 的所有 240 proper literal rows：

- 15,360 個 C tuple／r-colour ambient cells，其中 13,536 空；每個 literal 都核完整64 cells。
- 3,840 個 U ambient cells，其中 3,192 空；每個 literal 都核完整16 cells。
- 全 3,840 個 r/s pin queries；X／G 空 queries 分別2,400／2,904。
- 全 3,932,160 個 full ambient fibre slots，含 3,915,072 空 fibres。
  r/s、四 contact tuple 座標、孤立 I 色全部保留；每個 fibre 比對 piece union 與獨立整圖 solver。

十個 canonical rows 的完整 matrices／pins 與 frozen certificate 逐結構相同；
全部 240 rows 的完整 detail hashes 都一致。
全 X/G lifts（含孤立 I 的四色自由因子）分別 **21,120／7,488**，與 worker 相同。
G 再用獨立整圖 solver 重算，恰等於 X lifts 加原 `r≠γ(b4)`；不從 X 接受推稱 G 接受。
每一 proper literal 的 toy G 均有 full lift，故 source-boundary 記錄正確：
toy 不拒絕 β、沒有 X 自己的 β-minimality，恢復 e 對 Σ 冗餘；rotation 未提供。
它不是 HIGH2 source，也不是來源排除／任意大小覆蓋的正控制。

另獨立核 certificate 的全部 1,000 K33／180 K5 finite schemas：
原邊上的 bags connected、兩兩不交、九／十對 adjacency，及所有保存的 witness edge lists。
刪 exceptional 原 s–U 邊時 O′–s adjacency 確實消失。
這是有限 schemas 的具名原邊核對，不裁無界 bags 抽取或 source realizability。
其餘 cover／position／factor／orbit 算術由 actual worker checker 的完整 byte replay 核回，
不宣稱 H2C 又獨立重寫其全部分類或證一般 soundness。

[artifact-certificate](artifact-certificate.json)列所有 control status：
toy、算術、schemas 標 `triggered and holds`；marginal／restore／缺原邊的過強命題標 `counterexample`；
finite HIGH2 source 標 `not triggered`、未建立／未執行、trigger_count=null。

## 4. 四種正式負控制及真正拒絕階段

所有錯資料只在本端 negative 目錄或記憶體，原 worker 任何檔皆未動。

| 本端 probe | actual exit／拒絕階段 |
| --- | --- |
| wrong certificate，正式 checker `--check --certificate` | exit2，`certificate byte comparison: mismatch` |
| wrong input index，正式 checker `--check --inputs` | exit2，`input validation: frozen-index binding` |
| 正式 manifest 少 nested receipt，真正 seal `--check-inventory-stdin` | exit2，payload inventory missing **僅** `negative/nested/receipt.json`，extra／drift 皆空 |
| 原 receipt 的 manifest binding 在記憶體改錯 | exit2，真 worker `check_delivery` 路徑先核正式 payload，再在 `metadata binding: receipt to manifest.json` 拒絕 |

最後一项 [probe 程式](negative_receipt_probe.py)只攔 exact worker receipt 的 read_text，
其餘原 payload／manifest／delivery／cwd／正式入口均真實；不製造 synthetic approval 代替正式 delivery。
前兩項的錯 artifact bytes、第三項正式 manifest 及其 stdin hash 都保存；
[run_checks.py](run_checks.py)保存四筆 stdout／stderr／exit 與 runtime provenance。

## 5. Custody FAIL 與合法 shared 採納後的模式

本端 actual 原 worker verify_local.py 再跑 exit1，完整失敗 stdout 留在
[outside-custody stream](runs/outside-custody.stdout.txt)。
該實跑沿接手的 33,139 個既存 indexed paths 核回，regular／symlink drift=0；
另觀察846個新增 paths，outside Git status 不同。因此 outside custody 仍 FAIL。
它只沿原 frozen index 核既存 bytes，非 ignored files／.git 或全 filesystem inventory；不再擴 inventory。

四個既存 nested-repository directory markers 只確認 presence：
PC source、PG base-source、PR base-source、U source；未 hash 其子樹。
原 snapshot 的 missing 誤標保留，改正分類不把這四個目錄內容升為 hash 完整。
既存 indexed bytes、41 source inputs／8 pins、outside 新增狀態三層分明。
上列 drift=0 是 actual receipt 時間的判定，並非將來合法 shared 採納後的 whole-tree 聲明。

worker 的 whole DocGraph actual exit1、stdout62 errors 及 stderr **62條 duplicate-ID errors** 完整保留。
本端未重新跑 global DocGraph、lake、historical E4 provenance 或無關枚舉；
BASE 缺檔、E4 provenance FAIL 與所有舊失敗均未藉刪 scratch／修 shared 解掉。

父端正式採納之後可合法改 shared。那會令原 worker live-current pins 不再相等，
不能冒稱原 checker 此時仍通過，也不代表 frozen evidence 損壞。
本端 verifier 提供如下模式：

```
python3 -B audits/2026-10-10-n45-h2c/verifier.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-10-n45-h2c/verifier.py
python3 -B audits/2026-10-10-n45-h2c/verifier.py --frozen-only
PYTHONHASHSEED=17 python3 -B audits/2026-10-10-n45-h2c/verifier.py --frozen-only
```

一般模式核採納前 live origins／pins／HEAD 與 frozen 一致；`--frozen-only` 核原 worker完整 payload、
本端及父端 frozen bytes／modes、41 frozen inputs／8 frozen pins、全部歷史 actual receipts、
本端獨立有限證書與 immutable manifest，不要求合法改動後的 shared origins／HEAD 等於旧值。
所有 normal／seed17 的 actual worker replay 是在 shared 採納前執行，receipt 不刷新。

## 6. 本端封存與停止點

本端 manifest 精確列 immutable payload，排除僅 exact top-level manifest.json、delivery.json、receipts.json；
nested 同名檔全是 payload，metadata 綁 manifest／artifact-certificate hashes。
本端 final normal／seed17 與 frozen-only normal／seed17 的完整 stdout／stderr／exit 記在 receipts.json。
只讀 verifier 不生成或覆寫證書；preflight-v1 streams／receipt 也留存。
authored local Markdown links／whitespace 核回；frozen 舊 report 的歷史 link 問題不改寫。

H2C 停於 bounded artifact acceptance 候選；12 paper claims 全部 **not adjudicated by H2C**。
沒有 source realization、任意大小 paper 新裁決、Lean 或 generic tool soundness。
無 shared／old worker／parent／siblings edits，無 commit、push、PR、外部訊息或再委派。
