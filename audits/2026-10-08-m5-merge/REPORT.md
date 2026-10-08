# 2026-10-08：M5 PR #3 合併與回讀

**PR #3 已使用普通 merge 合併；合併與 ancestry 驗收通過。合併後 Lean CI 目前 in_progress，未宣稱 PASS。**

使用者授權：「你查看後達條件就能合併」。見 [REQUEST](REQUEST.md)。
驗收沿用 [M4-R 既定 gate／具名例外](../2026-10-07-m4-remote-supervisor/REPORT.md)與 [M5 任務](../2026-10-07-m4-remote-supervisor/M5_MERGE.md)。

| 項目 | 實際驗收 |
| --- | --- |
| PR | [raylei50653/math #3](https://github.com/raylei50653/math/pull/3)，MERGED |
| 合併時間 | 2026-10-08T09:45:07Z（台北 2026-10-08 17:45:07） |
| Merge SHA | `2971d46d715d213f25f534958bdab499d2573b69` |
| Parents | `2ddc6b4a4e412ab2cb7917fe4fb6fdeef2e86090`、`1f21c8f09dfcb5110ea1a3d66399e9c0a54ceeaf` |
| Tree | `d614893520c70b4c1ce6034e17fd1901146c10ce`；與受驗 head tree 完全相同 |
| Remote／tracking main | `2971d46d715d213f25f534958bdab499d2573b69` |
| 受驗 head ancestry | `git merge-base --is-ancestor <受驗 head> origin/main` exit0 |
| 獨立 checkout | `/tmp/math-m5-main-hm0keg_b`，detached於精確 merge SHA、tracked／staging乾淨、無scratch |
| M3／M4 seals | 原工作區及獨立 checkout PASS；原328檔與正式封存包保持 |
| 原工作區 | HEAD仍為受驗整合head，tracked／staging乾淨；原scratch／旁掛證據與分支保留 |

## 合併前核對與實際執行

[Preflight](preflight/state.json)核對local／tracking／remote／PR head一致，main／base未前進；PR OPEN、非draft、MERGEABLE／CLEAN；reviews／待解threads為0，main保護規則無新增。兩份既定Lean runs仍SUCCESS，沒有同head新失敗。Repository允許普通merge，auto-merge與merge後刪分支均未啟用。

[合併命令](commands/merge/command.json)exit0：

```sh
gh pr merge 3 --repo raylei50653/math --merge \
  --match-head-commit 1f21c8f09dfcb5110ea1a3d66399e9c0a54ceeaf
```

隨後透過PR readback、remote refs、commit API、fetch main、Git parents／tree／ancestry及獨立checkout核對；沒有以合併命令exit0代替驗收。詳細結果見 [merge-verification](merge-verification.json)、[independent-checkout](independent-checkout.json)及各commands原始stdout／stderr與hash。

## CI與保留界線

合併後[Lean CI 37758822896](https://github.com/raylei50653/math/actions/runs/37758822896)的run head為精確merge SHA，status=`in_progress`、conclusion=`pending`。Checkout step成功；完整raw log／實際checkout SHA與最終build結論尚未取得，不宣稱合併後CI成功。最新snapshot见 [post-merge-ci-02](commands/post-merge-ci-02/stdout.log)。

文件dispatch `37592841563` 的FAIL保持；缺少archive還原步驟的workflow修復仍為另案維護。同一受驗tree還原後docs／DocGraph的M4-R證據沿用，本輪未再還原或重跑文件checker。五份strict FAIL、歷史whitespace、M1缺失及數學／native／上游信任界線均照原驗收保留，未改寫原報告。

本輪未重跑LC build／558公理程序、證書生成器或研究枚舉，亦未新增數學結論。此包僅新增未commit的M5證據；沒有新增來源commit、修改受驗head、刪分支或刪本地研究資料。

停止點：合併與main核對已完成；合併後Lean CI仍pending。狀態以 [status.json](status.json)的查詢時間為準。
