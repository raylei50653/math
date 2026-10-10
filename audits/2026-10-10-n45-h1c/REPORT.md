# N45-H1C：HIGH1 工具、輸入與封存獨立稽核

日期：2026-10-10。BASE／HEAD：`dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。
唯一新增目錄為本 audit；HIGH1 worker、共享文件及其他舊 audit 均保持只讀。
沒有 commit、push、PR、外部訊息、再委派、新 Lean 或具名有限來源。

## 1. 裁決與精確範圍

[HIGH1 原交付](../2026-10-10-n45-s-high1/REPORT.md)的 **artifact integrity 通過**，
沒有阻擋本工具裁決的 finding。[獨立判定](independent-judgment.json)只接受本節以下
輸入、封存、重播及有限域校準；HIGH1 十項 paper claims 的任意大小數學論證未在本稽核裁決。
原候選仍須由獨立紙面與 relation reviewer、supervisor 決定是否正式採納。

有限 HIGH1 source controls **未建立、未執行，沒有 trigger count**。
certificate 的 `not triggered` 標籤只表達未建立控制，不能讀成「跑過來源而零觸發」。
source realizability、一般 N2／E、Lean 不由本 audit 關閉。

## 2. 獨立輸入與 custody

[獨立 intake](inputs.json)記錄 worker 全樹 **94 regular files、0 symlinks** 的
SHA256、bytes、mode；主 manifest 僅排除三個 exact top-level 名稱
`manifest.json`、`delivery.json`、`receipt.json`，因此 **91 payload＋3 metadata＝94**。
`negative/nested/receipt.json` 和每份 `logs/*.receipt.json` 都是主 payload。
沒有以 basename 或整個 receipt／logs 目錄排除。

worker `inputs.json` 為 34 份獨立綁定輸入：**16 BASE、17 current、1 external**；
9 個 HIGH1 task pins 與 frozen task-pin JSON 完全對應。
16 份 BASE 均逐 byte 對 Git `BASE:path`，17 份 current 在 intake 時逐 byte 對原路徑；
external Gallai PDF 僅核本交付的 URL／frozen byte pin，沒有在此裁決外部定理數學。
證書的 input index SHA256 為
`8295f37e0b931e49cce54961439903d2b515c2909123cad7f9c96f0e0b13e5a8`。

[起始 custody](custody-start.json)與[custody checker](custody.py)另核 worker 原有
**5,899 tracked files bytes**、cached diff，以及排除明列 supervisor／H1A／H1R／H1C
新目錄後的 Git 狀態；正確保留預先存在的修改。
worker 原聲明僅涵蓋 tracked bytes 與實讀 untracked inputs，沒有舊 untracked 全樹 hash。
本 H1C 額外覆蓋 worker 94 檔 bytes／modes 與實讀 inputs；parent 的額外 whole-tree
custody 是另一證據層，不能歸給 worker 或本 H1C。

後續採納可以更動共享 current authority。本[獨立 checker](checker.py)重播只讀
已綁定 frozen current bytes，並重核 BASE Git objects、HEAD 與 worker 全樹，
不因 supervisor 正式採納而重新要求共享 current 文件維持舊 hash。

## 3. Manifest、delivery、receipt 與實跑 ledger

獨立 payload gate 檢查 JSON manifest 的安全相對路徑、唯一性、排序、精確 inventory、
每檔 SHA256／bytes、0 symlinks。delivery 綁 manifest／REPORT／claims／certificate／receipt，
[正式 receipt](../2026-10-10-n45-s-high1/receipt.json)再綁 inputs 與 checks-final。

checks-final 與 receipt 完整對應 **12 unique runs、24 stdout／stderr streams**，
所有 exit 都按各項真正範圍比對；其中 whole DocGraph 的 expected／actual exit 1 是保留 FAIL。
12 份巢狀 actual-run receipt JSON 逐項等於 ledger record，且由主 manifest 作為 payload 綁定。
原 checks.json、第一次 local log、generation log與 inputs-v1 亦保留於 91 檔 payload，
沒有覆寫成最新版或以新 receipt 隱去舊紀錄。
normal／seed17 的命令、cwd、environment、stdout／stderr、certificate bytes 均核回。

本 H1C 的各次實跑記錄於 `logs/*.json` 與最終 `checks.json`。
自封存另用 `MANIFEST.sha256`、`delivery.json` 及十個逐一具名 receipt metadata 檔。
[完整重播入口](verify.py)同時核本 audit 的精確 seal 與 worker frozen gate；
[封存程式](seal.py)exclusive-create，normal／seed17＋錯 digest 實跑後綁所有 metadata。
任何巢狀同名 manifest、delivery、receipt 都仍屬 payload。

## 4. Certificate 重算及獨立有限域核對

本稽核只讀載入已由 intake 綁定的 worker 標準庫 fixed-domain 函式，
**不呼叫 worker 的 live `inputs()`、`main()` 或上游決策 oracle**。
它的 `inputs` reader 被明示替換為本 audit 的獨立 frozen gate，保留同一真實 frozen index；
其餘 fixed-domain controls 只读执行以重建完整 certificate。
這是執行 worker 控制的證據層，並未宣称把整份 worker checker 獨立重寫。

此外用本 audit 自己的 Cartesian assignments enumerator，按原 edges／attachments
重新核全 **240 literal C5 rows、10 canonical rows、每列 16 root pins**。
十份保存的 C 完整 ambient tuple／r-pin fibres 各 64 項、U 各 4 項，包含所有空 fibres；
240 列的完整 record SHA 逐項從獨立枚舉重算。
完整 restriction／union 與直接 whole-X、restore-spoke whole-G assignments 相等；
全列 X／G lifts 分別 **2,160／1,560**，原 isolated point 自由因子为 4。
兩條過強推論的 witness 均另核：marginal 假接受與「X 有 lift 故 G 有 lift」失敗。
toy 沒有 disk rotation／HIGH1 minimality／Σ 前提，這兩者都是校準反例。

另獨立核 **1,000** K₃,₃ adjacency schemas、**10** ordered disjoint support metadata、
**1,200** capacity-one pointwise-support S4 stabilizer records、**100** whole-D5 missing-position
算術，以及 **70** beta metadata 的 whole-D5／共同 literal S4／spoke 映射；933 的 q2 全留。
這些是有限 metadata／抽象圖校準，並非 1,000 個平面來源，亦不裁 BASE 路由定理。

certificate 重建 **1,960,670 bytes**，SHA256
`0aa93b73a4a46b204004752d8c32fce899f689d875d4e3368c4808b1e8e0f1bf`。
[normal 實際輸出](logs/normal.stdout.txt)與[seed17 實際輸出](logs/seed17.stdout.txt)
逐 byte 相同、stderr 皆空、actual exit 0。

## 5. 實際負控制與拒絕階段

| 控制 | 實際 exit／階段 | 本次限定證據 |
| --- | --- | --- |
| worker 原 bad-certificate 的只讀複本 | 2／certificate byte comparison | 錯 certificate bytes；不是來源前提拒絕 |
| worker 原 bad-input-index 的只讀複本 | 2／independent frozen input binding | 尚未進固定域重算或證書比較 |
| 原 certificate 的專屬目錄複本重複 generation | 2／exclusive certificate create | FileExistsError；原 worker certificate 與本複本 bytes 皆未改 |
| 刪除 nested receipt manifest entry | 2／payload inventory | 唯一 missing 為 `negative/nested/receipt.json`，extra=[] |
| duplicate manifest path | 2／payload inventory | unique path gate 拒絕 |
| unsafe `../REPORT.md` path | 2／payload inventory | safe relative path gate 拒絕 |
| 錯 REPORT digest | 2／payload inventory | 真實 inventory／hash 比對拒絕 |
| 破壞正式 receipt 的專屬目錄複本 | 2／delivery/receipt exact binding | 正式 delivery 的 receipt SHA 不符；沒有 delivery／inventory override |
| worker 原 seal 的正式 receipt 破壞重播 | 2／delivery/receipt exact binding | 真正讀原 formal delivery，錯 receipt 用 `--receipt` 指向本 audit 複本 |
| worker 原 seal 的 nested omission 重播 | 2／payload inventory | `--manifest` 指向本 audit 複本，同一真實 worker inventory 拒絕 |

八份 negative fixtures 全部 exclusive-create；其中僅 existing certificate probe嘗試
exclusive write 且立即 FileExistsError。所有 negative 都是真實命令 exit／stdout／stderr。
完整 worker 94 檔在 probes 前後 SHA256、bytes、modes 全不變。

## 6. 保留的失敗與停止點

worker whole-worktree DocGraph 的 **62 個 duplicate-ID errors／actual exit 1**
完整 log 已核 hash 和逐 error count；不刪 scratch、frozen copies，也不把它稱作 PASS。
worker 正式 docs DocGraph 的 exit 0 與 current check_docs exit 0 是不同 scope。
本輪不重跑歷史 BASE 缺檔、E4 provenance、上游 finite source search、Lean build／axiom audit，
依原交付保留這些歷史 FAIL 的身份。

本 H1C 只核新 audit authored syntax／local links／whitespace及 `git diff --check`；
paper、外部 Gallai、來源實現與 Lean 證據層仍分開。
HIGH2／HIGH3、long、其他 S 身份、原 55、一般 N2／E、ε≥3 均不在本裁決範圍。

封存後只讀重播：

```bash
python3 -B audits/2026-10-10-n45-h1c/verify.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-10-n45-h1c/verify.py
```
