# N45-SSC：N45-U-SS 封存、輸入及 evidence boundary 獨立增量稽核

2026-10-10。根 `/home/ray/developer/ai/math`；BASE／本輪 HEAD
`dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。

**裁決：PASS_ARTIFACT_INTEGRITY_ONLY。** 原 worker 主 payload、封存 metadata、
全部指定輸入與既有 shared bytes 核回相同；11 claims 的宣告契約、DAG 及分支元資料完整。
本稽核不採納 SS 任意大小 paper theorem，不判定其數學真偽，亦不給 SS source count。
機讀裁決見 [independent-judgment](independent-judgment.json)。

只寫本 fresh exclusive `audits/2026-10-10-n45-ssc/`。先讀 HANDOFF、STATUS、DOCUMENTATION
及 Git state，依 document-first；未用 Graphify、未讀 SSA／SSG 裁決或監督本輪 adoption。
未改共享／worker／其他 audit，未 commit／push／PR／對外發訊息／開 subagents。

## 1. 原件與凍結方法

受審原件是 `audits/2026-10-10-n45-u-ss/` 的 REPORT、verify.py、inputs、claims、checks、
MANIFEST、delivery、seal-checks 及其保留原 logs／完整 BASE archive。
[freeze.py](freeze.py) 按 bytes 獨立複製，不 import 或執行 worker 程式。
[freeze.json](freeze.json) 綁每個 regular file 的 SHA256／大小與 5 個 symlink targets。
每個 BASE 必要輸入另以 `git show BASE:path` 凍結；實際命令、exit、stdout／stderr
均列於 freeze.json 及 `freeze-logs/`。

監督已在新增 SSA／SSG／SSC directories 之前實跑原 verifier normal／seed17。
本輪只讀並凍結其純執行 [normal receipt](frozen/supervision-execution/logs/worker-normal.json)、
[seed17 receipt](frozen/supervision-execution/logs/worker-seed17.json)、兩份 combined logs，
以及 [先前完整 tree freeze](frozen/supervision-execution/inputs-before.json)。
不讀監督的本輪裁決。這些 receipts 記錄實際 argv、cwd、exit0 與
`before_new_audit_directories=true`；本輪不從 stdout 字樣反推 exit。

原 verifier 的 `outside == set(shared)` 前提在授權新增 audits 之後已不成立。
**本輪沒有再執行原 verify.py，也沒有聲稱它在目前 outside inventory 下 PASS。**
獨立 checker 檢查原 13,146 份 shared-before bytes，另只允許此 SS audit batch 的新增路徑。
新增 SSA／SSG／監督檔案只查路徑是否符合明列前綴，不讀其裁決內容。

## 2. exact inventories、排除及輸入

| 核對 | 實際結果 |
| --- | --- |
| worker full tree | 6,104 regular files＋5 個 BASE Git symlinks；共 6,109 entries，與監督先前 tree freeze 相同 |
| 主 payload MANIFEST | exact 6,096 regular-file inventory、逐 SHA256 全相同，原 MANIFEST SHA256 `324aecf70c3c8d4f40f02bcf58cf1fc39b457c212dbbd4a7770c6d6f07b2ad0f` |
| 主 receipt 排除 | exact `MANIFEST.sha256`、`delivery.json`、`seal-checks/**`；排除理由及 references 與 delivery 核回 |
| seal-checks | 5 個 metadata files 逐 SHA256 相同，另有其自身 MANIFEST；它們不屬主 payload |
| 指定 inputs | 24 BASE blobs／11 current snapshots／5 pins 全相同；current-work 層保留，沒有改稱 BASE |
| BASE archive | 5,899 regular files＋5 symlinks＝5,904 Git blob entries；完整 inventory／每個 Git blob hash／原 tar contents 與 link targets 全核回 |
| 舊 shared bytes | worker shared-before 的 13,146 份全部相同，tracked／cached binary diff 亦相同 |
| strict sealed replay | worker normal／seed17 stdout 相同、stderr 空、receipt exit0；與監督新增 audits 前的兩次實跑 combined stdout 亦逐 byte 相同 |

5 pins 是 authority、原 PR REPORT、PA judgment、原 U REPORT、SU-A judgment；checker
獨立固定任務指定 digest，再核原 current bytes、worker frozen bytes 和本輪 copied bytes。
PA／LP 引用僅作受審宣告 provenance；沒有借 PA 裁決採納 SS。

原 `BASE-missing` 探測
`docs/c5_weak_deletion_minimal_obstruction.md` 的 git show exit128 保留且不計入 24 BASE；
實際 declared input 是 `docs/c5_weak_list_cores.md`。

**工具限制 SSC-F01：** worker verifier 的 inventory 是 `is_file()`，其主 manifest 不綁
5 個 dangling symlink targets。這些 links 是 BASE Git archive 保留的 `.snapshot` links，
不是本輪異常或新來源。獨立 checker 另外用完整 Git tree、Git blob hashes、原 tar 與
監督先前 freeze 核回全部 targets；沒有以 regular-file manifest PASS 遮掩此工具限制。

## 3. claims 宣告契約、DAG 與 coverage 邊界

獨立 [checker.py](checker.py) 不 import worker verifier，採標準函式庫只讀核對。
它要求 8 個完整 declared source clauses 在全部 11 claims 中保留，額外 sufficient premises
恰與明列 branch premises 相符，檢查內部 dependency 存在、acyclic DAG 與預期 edges。

8 clauses 保留：有限簡單 ordered induced-C5 disk；完整 933／941 或共同 D5、原 criticality
及 ε=2；連通 full-B-touch、非相鄰 degree5 roots 及其他完整 degree4；完整 H−roots
恰 U／L／S 三份 one-sided 原分量；U 恰一原 rx、无 s 邊、整 U 省略恰 X=M；
outside-U 原頂點／邊及原 incidence 等式；L long、S 恰一具名框點、S incidence≥4；
具名 ordered contacts、shared 單坐標、附件／支援／ownership／bridges／rotation、
共同 literal frame、完整 tuples／空非空 fibres／全部 full lifts，以及 whole-graph symmetries。

| Claim | 宣告內部 dependencies／branch |
| --- | --- |
| COST | 原 U-WIT／BASE shield／U-RES；宣告盾費恰 (2,2)、(2,3)、(3,2) |
| UNTOP | COST；原盾弧內點 restriction |
| U3 | UNTOP；(3,2) 長度3 branch |
| U2 | UNTOP；(2,2) 或 (2,3) 長度2 branch |
| X-CORE | X=M 定義及完整原邊分割；自身 minimality／完整 degrees 宣告 |
| COMPONENT | X-CORE；同一原 C 及全部 literal rows 的 full-lift join 宣告 |
| SPOKES | U2、X-CORE、COMPONENT；長度2，t_s∈{0,1,2} 宣告 |
| T0 | SPOKES；t_s=0＋明列 preceding-derived prerequisites，BASE no-spoke §4／外部 Gallai |
| T1 | SPOKES；t_s=1＋明列 preceding-derived prerequisites，BASE single-spoke／tree-component／外部 Gallai |
| T2 | SPOKES；t_s=2＋明列 preceding-derived prerequisites，BASE two-spoke §1–5／外部 Gallai |
| EXCLUSION | COST、U3、U2、X-CORE、COMPONENT、SPOKES、T0、T1、T2 |

這是宣告 inventory／DAG 與 branch coverage metadata 核回，沒有把 dependency edge
或 required-field presence 當作論證有效。特別是原面、盾弧、T4 改色、X minimality、
完整 C 與三個 BASE theorem 的充分前提，其数学 truth 不屬 SSC 工具稽核裁決。
所有 claim status 為 `paper_candidate_under_listed_premises`，adoption pending。

**SSC-F02：** original verify.py 只查 11 IDs、required keys、source-contract clauses 的包含及
internal IDs 存在。它沒有檢查 DAG 無環、branch exhaustiveness、數學推導、完整 graph
relations 或 actual source。獨立 checker 補核 DAG／branch 宣告一致性，仍不證 theorem。
worker 原 verifier 也不核被排除 seal-checks 的 metadata manifest／exit receipts／四份 logs
相同、全 BASE archive、receipt 全部 exclusion/scope flags；本輪分别核回這些項目。

**SSC-F03：** 沒有新 finite SS source certificate，SS trigger count 為 `null`／未計算，
不是 0、not-triggered 或 finite source exclusion。舊 PC／PCA 的 LP controls 和 N1
calibrations 不是 SS controls。本輪不重播 PC，也沒有 source search、realization 或原圖反例。
paper、BASE 任意大小 papers、外部 Dvořák Lemma7／Theorem10、finite、Lean 分層保留；
外部來源 frozen PDF bytes 已核，外部 theorem correctness／live web provenance 未重新裁決。

未涵蓋：移除任一 source premise、S spoke-omission LOW／HIGH／long、其他 U／core
身份及原55、一般 N2／E、ε≥3、specified-coloring repair、source realization、Lean theorem、
general validator soundness。本工具 PASS 不更改 authority／共享頁的 SS OPEN。

## 4. 實跑、負控制與歷史失敗

重播命令：

```sh
python3 -B audits/2026-10-10-n45-ssc/checker.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-10-n45-ssc/checker.py
```

[checks.json](checks.json) 保存本輪實際 argv、cwd、env、exit、stdout／stderr。
normal／seed17 exit0 且輸出逐 byte 相同。兩個正控制與六個小規模 fresh 副本負控制
也完成：缺 source premise、DAG cycle、把 finite SS 未計算升格為排除、payload byte drift、
extra file、duplicate manifest path，均被 independent checker 以預期 exit1／精確 reason 拒絕。
這只證六份具體錯資料被攔，沒有宣告一般 validator soundness。

worker 71 個歷史命令的 log paths 均保留且已被主 payload hashes 綁定。
全部非零 receipts 原樣：

| 原失敗 | 保留結果 |
| --- | --- |
| base-blob-12 探測缺檔 | exit128；不列作數學依賴 |
| exact BASE check_docs | exit1；兩個缺檔為 `audits/2026-10-04-task-d5/c4/scope_ledger.json` 與 `audits/2026-10-04-task-d2/integration_doc_changes.diff`；Git tree／archive 均仍缺 |
| current whole-worktree DocGraph | exit1；62 duplicate-ID errors 的 stdout／stderr 保留，不能以 formal docs PASS 改稱全工作樹 PASS |
| initial artifact verify | exit1，`own REPORT link missing: checks.json`；舊程式與 failure receipt 保留 |
| preseal draft verify | exit1，`missing final newline: gallai-primary.txt`；PDF extraction bytes 與舊程式／receipt 保留 |

繼承兩個 E4 provenance byte replay FAIL 仍是歷史 FAIL；原 authority／E4 原文 bytes
未改，本輪未重播，不把本 integrity PASS 當作舊 replay PASS。
worker 原 formal docs、current docs 及 diff checks 的 exit0 只保留當時範圍，本輪沒有
再次宣稱全工作樹文件檢查通過；新 frozen copies 也沒有被刪去隱藏 duplicate IDs。

本稽核自身也保留初始 freeze 對 Git symlink 的拒絕與两次 supervisor metadata key
`target`／`symlink` 誤讀失敗及相應舊 checker。實際欄位是 `link`；最後以標準 schema
核回 Git／tar／prior freeze，沒有改受審資料或跳過該核對。

本輪未跑原 worker verifier（outside inventory 前提已變）、上游 E2／E3／E4／U1–U4
checkers、graph／k／source search、source realization、Lean build／axioms、remote CI、
general validator soundness 或外部 live theorem check。

## 5. 封存與停止點

本 audit payload、全部 frozen 原件、logs、正負控制及 checker 由
[MANIFEST](MANIFEST.sha256)／[delivery](delivery.json) 封存。
symlink targets 另由 [SYMLINKS](SYMLINKS.json) 固定並列入主 manifest。
封存後唯讀 [verify-seal.py](verify-seal.py) normal／seed17 的實際 receipts/logs 在
[seal-checks](seal-checks/commands.json)，該目錄有獨立 metadata manifest。

Canonical Source＋Evidence：本 REPORT 的工具／完整性裁決、independent-judgment.json、
checker.py、checks、完整 frozen 原件與 seals。
Updated：本 fresh audit。Reviewed-unchanged：原 worker、authority、HANDOFF、STATUS、
DOCUMENTATION 與 worker shared-before 全部 existing bytes。
Remaining OPEN：SS paper 數學裁決及全部 §3 未涵蓋範圍。
Propagation stop：只作 evidence audit，不採納 theorem、不修改 shared closure、不選下一 residual。
