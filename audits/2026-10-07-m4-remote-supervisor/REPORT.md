# M4-R 監督驗收與合併就緒判定

**M4-R 驗收通過；PR #3 滿足本輪既定合併條件，限已明列例外。**
文件 CI 仍為 FAIL；不是全 CI PASS。實際 merge 尚未獲另行授權，也未執行。
此判定限 `live/state.json` 的 UTC 查詢時間與下列精確 head/base；合併前須再次核對。

| 欄位 | 驗收值 |
| --- | --- |
| PR | [raylei50653/math #3](https://github.com/raylei50653/math/pull/3)，OPEN，非 draft |
| Local／tracking／remote／PR head | `1f21c8f09dfcb5110ea1a3d66399e9c0a54ceeaf` |
| PR base／remote main | `2ddc6b4a4e412ab2cb7917fe4fb6fdeef2e86090`，未前進 |
| Mergeability | MERGEABLE／CLEAN |
| Reviews／待解 threads | 0／0，完整頁面已核對 |
| Required checks policy | branchProtectionRule=null、effective branch rules=[] |
| Auto-merge | null |
| Lean push／PR jobs | SUCCESS／SUCCESS |
| 文件 dispatch | FAIL，保留原失敗，不改寫為成功 |

監督端透過 GitHub connector 與只讀 `gh api` 重新核對 PR、兩個分支 refs、
main rules、reviews／threads、三個 run metadata 與 jobs。
原始讀回見 [live/state.json](live/state.json)、[commands](live/commands.json)
及 [connector-readback](connector-readback.json)。此輪未修改 GitHub、Git refs/index 或候選。
初次 sandbox 網路連線失敗；只讀網路重試成功，未修改 remote 設定。

## CI 與交付證據

[獨立 verifier](verify_remote_delivery.py)核對 M4-R 原 inventory 的 341 檔與 inventory 自身、
56 份 command records／112 份原 stdout/stderr hashes、三份原 ZIP 全部 entries hashes
及實際 checkout 命令／SHA 行；原包不修改。結果見 [acceptance/review.json](acceptance/review.json)。

- [Lean push 37592725527](https://github.com/raylei50653/math/actions/runs/37592725527)：
  checkout 為固定 final head，build SUCCESS，原 log 顯示 8,831 jobs。
- [Lean PR 37592797376](https://github.com/raylei50653/math/actions/runs/37592797376)：
  checkout 為 synthetic merge `ca65f8796c6d83296fee2b22a77467d46b37ebec`，
  build SUCCESS，原 log 顯示 8,831 jobs。
  GitHub commit API 確認 parents 為 `[base, final head]`，tree 為
  `d614893520c70b4c1ce6034e17fd1901146c10ce`，與 final head tree 全等。
- [文件 dispatch 37592841563](https://github.com/raylei50653/math/actions/runs/37592841563)：
  checkout 為固定 final head，check FAIL。失敗的 ordinary paths 是
  `audits/2026-10-04-task-d5/c4/scope_ledger.json` 與
  `audits/2026-10-04-task-d2/integration_doc_changes.diff`。

兩個 Lean jobs 是預設 Math build，不代替顯式 LC／公理證據。
109 份同 hash Lean 來源／設定／生成證書與 M3 顯式 LC build／558 公理沿用界線保持；
本輪沒有重跑 LC build 或 Lean 公理程序。
正式 M4-L seal 再核對 exit0，原來源與正式交付 commit 未更動。

## 文件 CI 例外的獨立重現與驗收依據

使用 `git archive` 匯出完整 final Git tree 到新的 scratch-free `/tmp` 目錄，
未攜入工作區 materialized archives 或旁掛證據。
原樣執行 `scripts/check_docs.py` exit1，正好重現遠端兩個 missing paths。
只從此 Git tree 已提交的 gzip blobs 還原那兩份 targets，大小及 SHA256
逐份符合該 tree 的 `audits/ARCHIVE.json`。未刪連結、未改 checker／workflow／原證書。
隨後文件 checker exit0：573 Markdown、6,714 links、anchors/index/handoff 通過；
預設 DocGraph exit0。完整命令與 raw log hashes 見 [新重現 logs](acceptance/commands.json)。

這確認兩份證據已保存在 commit，失敗是 `.github/workflows/docs.yml` 缺少 archive
materialization 步驟；不是原 M1 缺失證據的另一份替代敘述。
按既定 [M4-R 派工第 4 項](../2026-10-07-m4-supervisor/M4_REMOTE.md)，
文件驗收允許同 final SHA 的本地文件／anchors/index／預設 DocGraph 證據，
不強制文件 dispatch 成功。本次依這個事先明列的選項滿足文件 gate，
沒有把 required checks 未設定當作成功依據，也沒有事後改寫 gate。
此次文件 run 的 FAIL 永久保留；workflow 還原修復列為後續維護，不改此受驗 head。
若使用者另增「全部遠端 workflows 必須成功」要求，則本判定不滿足該新增要求，
必須修復 workflow 並對新 head 重新驗收。

## 停止點與剩餘任務

M1–M4 的證據與已約定 gate 已收齊。五份 strict FAIL、原 86＋匯入 log 85 whitespace、
原工作區 scratch DocGraph 62 duplicate-id、M1 歷史缺失、native／上游信任及
U2–U4 等數學界線全部保持，不以 PR 技術可合併推升研究結論。

剩餘執行任務為 [M5：授權後合併與回讀](M5_MERGE.md)，執行前再次核對
精確 head/base、CI 與 review/policy 狀態。尚未獲另行明確 merge 指示，因此本輪不執行。
新監督資料只作未 commit 旁掛證據；原 M4-R 原包、M4-L seal、先前監督 inventory 均不改写。
