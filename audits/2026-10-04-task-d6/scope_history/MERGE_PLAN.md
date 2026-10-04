# D₆：W ledger 的版本化合併設計

以下是總數學稽核通過後的可操作設計；現有 W verdict 的 strict replay
另有來源文件 hash 漂移，必先修復，不能把原 `--check` 寫成通過。

### 先保留並修復 W verdict 的證據來源

1. 保存原 `verdicts.json` 全部 bytes、SHA256、來源 hash map 與本輪失敗輸出，
   建立有版本的歷史檔，不覆寫成「當時已成功」的資料。
2. 從同一 C₄ predecessor ledger 重新生成修訂版 W verdict。現有 W `--write`
   用 exclusive-create，原檔存在時拒絕覆寫；整合者應先保存原檔至歷史版本
   路徑，再在空的 canonical verdict 路徑生成修訂版，或為 checker 增加明确
   的新輸出路徑。不能手改 artifact hash 來冒充一次重播。
3. 修訂版對比原版，唯一容許的 payload 差異應為
   `/sources/docs~1c5_unary_shield_budget.md/bytes`、`.../sha256`；
   對完整 JSON 做其餘字段完全相等的檢查。keys、IDs、28 份 certificates、
   3,497 個 verdicts、scope-row hashes、完整未知 relation 界線全部不變。
   若有其他差異，停下逐項說明，不視為純文件來源更新。
4. 對修訂版執行 W 一般與 seed17 strict byte replay，應均通過；來源圖檔、
   C₄ ledger、D₅ scope 與全部依賴也重新核 hash。

### 必須處理的循環依賴

原 W checker 行 19、195、229–252 讀 canonical C₄ ledger，只篩當時
`open_unreviewed` 的 3,497 keys。W verdict 把该 ledger bytes SHA256
寫在 sources。若 ledger 原地 `--write` 改成 zero-open，W 後續會重篩
零 keys，而且 W 新關閉的葉不符合舊 D₅ `closed_by=[]`，strict replay
即失效。不能同時聲稱原 predecessor source 不變及 canonical ledger 被更新。

推薦保持原 C₄ `artifacts/c5_open_leaf_ledger/ledger.json`、`trend.csv` 和所有
既有 snapshots 不變；W 版衍生 ledger 輸出至新版本目錄，如
`artifacts/c5_open_leaf_ledger/cw-v1/`。具體在重算器行 20 改 `OUT` 到新目錄，
並保留同一 `COMMON`、`SCOPE`、domain、stable IDs。原 W 仍能對原 C₄
source 完整重播，新 ledger 把修訂 W artifact 列為额外 immutable evidence。
如果一定要求原 canonical ledger 原地更新，則先保存 immutable C₄ predecessor
並為 W 增加明確的 predecessor-input routing；那是額外來源路徑變更，
不能再宣稱修訂版只改了文件 hash。

### `STAGES`、閉合提取與驗證須一起改

原重算器行 24–28 的 STAGES 為 `(stage, producer, single_target)` tuples；
行 124–146 硬編 observations.json、單份 identity、summary=1、scope_delta=-1。
不能只 append `("W","c5_qcore_shield_budget",...)`。

將 STAGES 改成具名規格，各含 `stage`、`kind`、`source`、`targets`；C₂／C₃／C₄
仍是 `kind=single`、原 observations 路徑和原 literal target，新增
`stage=W`、`kind=batch`、修訂 `artifacts/c5_qcore_shield_budget/verdicts.json`。
把行 124–146 分出 `extract_closed_keys(stage_spec, result, open_keys)`：

- single 路線保留原 identity extraction、exact target、summary 一份、零 target
  queries 等檢查，產生一份 key 與其 `/identity` pointer。
- batch 路線從 `/verdicts` 提取 key；驗證無重複、ID=`leaf_id(key)`、判定字串正確、
  恰 3,497 keys，且 key 集合 **等於當時全部 open_keys**，不僅是 subset。
  它與 inherited 三 keys 不相交，兩者聯集等於全部 3,500 domain。
- 驗證 W 的 `domain_sha256`、`common_source`、`scope_source` 和來源 hash map，
  每個 `scope_pointer` 解析至原 D₅ key，`ledger_pointer` 解析至原 C₄ leaf；
  `complete_scope_row_sha256` 是該完整原 row 的 canonical JSON **含末尾 newline**
  SHA256；certificate pointer 可解析且其 canonical hash 等於 certificate ID。
  不重猜 unknown unary 的完整內部圖。
- 對每個 key 建一份 close event，W event ID 用 `W/<stable-leaf-id>` 保持互異，
  保留 `stage="W"`、原 `/verdicts/i` evidence pointer、certificate pointer、
  `scope_delta=-1`、零 target/Lean、研究完成時間 unknown。W 尚未發布，
  `published_commit=null`；不能把旧 `83ca618` 或只是 baseline 的 `ca3870f`
  写成 W 已发布的 commit。然後一次 `census("W",3497)`。
- 用原 `reconcile(universe,before,after,declared_closed)` 檢查本阶段 exactly
  3,497 個關閉，零新葉／拆分／重開，不能略過其 exact-set equality。

原行 148–159 的 D₅閉合檢查需要分清歷史基準和後續事件，不能把 D₅ 改成
W 的新 verdict。先在 C₄ prefix 完成時檢查 historical closure set 恰等於
D₅ 三 keys、每份 sealed closed_by 一致、historical open=3497、下一入口
`(CPP-134-1,35,20)` 當時確實仍 open。W 後再驗證 current closed=3500、
open=0，原三 keys 的閉合來源不變；新 W keys 的 D₅ sealed closed_by 仍空，
新 current row 的 closed_by 才是具名 W event。

保留行 161–175 的三份過寬單 key 刪除負控制；W 另加 missing-key、duplicate-key、
foreign-key、把 historical 三 keys 算成新增等 malformed batch 控制。
行 264 的 printed open=3497/closed=3 改為從當前 leaves 計算；trend 應恰為
`3500→3499→3498→3497→0`，new_closed 恰為 `0,1,1,1,3497`。
行 194 的舊 C₄ 日期樣本保持歷史基準，不改成今天 zero-open。
新的真實觀測只在當時增加新檔，不覆寫既有日期樣本。

### `--write` 前後檢查

先保存 baseline ledger/trend/snapshots 與所有 source hashes；記錄 domain SHA、
全部 3,500 stable IDs、三份 historical closures、精確 3,497 open key 集合。
在新輸出版本目錄尚未發布前，用新 extractor 做 build-only/preflight，核對
上述 exact sets、完整 row hashes、所有 pointers、negative controls 和新 trend。
目前重算器沒有 build-only CLI；整合時應加 `--dry-run`，令其只回報 census
和候選 bytes hashes，從不寫 artifacts。

preflight 全通過後才可由整合者執行一次
`python3 scripts/c5_open_leaf_ledger.py --write`，然後一般/seed17 `--check`。
再次独立比對 new domain、unit、IDs、parents、common/scope pointers 不變；
原 C₄ ledger/trend/snapshots hash 完全不變；原 C₂／C₃／C₄ event 不變；
新 current open=∅、closed=3,500、新 W 恰=舊 open=3,497，不重算三個已關閉 keys。
確認 W strict byte replay仍通過、來源 hash 前後不漂移，再做文件、DocGraph、
`git diff --check`。本稽核未執行上述任何 `--write` 或修改原重算器。
