# M5：另行授權後合併 PR #3，並驗收合併結果

**就緒任務，尚未啟動。須使用者明確指示合併後才執行。**
本輪只讀監督與使用者的 M4-R 回報不構成 merge 授權。
M4-R 驗收與文件 CI 具名例外詳見 [REPORT](REPORT.md)。

| 固定條件 | 值 |
| --- | --- |
| PR | `raylei50653/math#3` |
| 受驗 head | `1f21c8f09dfcb5110ea1a3d66399e9c0a54ceeaf` |
| 已驗收 main/base | `2ddc6b4a4e412ab2cb7917fe4fb6fdeef2e86090` |
| Lean push／PR runs | `37592725527`／`37592797376`，SUCCESS |
| 文件 gate | 相同 head 的本地 restore 後 docs／DocGraph PASS；dispatch `37592841563` 的 FAIL 保留 |

授權後依序：

1. 即時核對 PR OPEN／非 draft、head/base、remote main 與 branch、reviews／待解 threads、
   required checks/rules 與各 CI run/job。固定 head 必須相同，main/base 不得前進。
   有新提交、新失敗、新 required gate、review 阻擋或任何狀態差異，先回報監督重新評估。
   保留五份 strict FAIL、whitespace、文件 dispatch FAIL 與本地替代證據的分類。
2. 核對 tracked/staging 乾淨與正式 seal 無漂移；不要為提交旁掛證據改 head。
   保留 scratch、M4-R 與各 supervisor 目錄，不刪除本地證據。
3. 用可保留受驗 head ancestry 的普通 merge commit，附 exact-head guard：

   ```sh
   gh pr merge 3 --repo raylei50653/math --merge \
     --match-head-commit 1f21c8f09dfcb5110ea1a3d66399e9c0a54ceeaf
   ```

   不開 auto-merge、不 force、不 bypass/admin、不刪分支。
   若 repository 不允許此策略，停止回報，不擅改 squash/rebase 策略或規則。
4. 合併後重新讀 PR state／mergedAt／mergeCommit、remote main；確認 PR 為 MERGED、
   merge commit 包含受驗 final head，且記錄實際 parents/tree 與 base。
   Fetch main 到 tracking ref 後驗受驗 head ancestry；以獨立 checkout 同步／驗證 main，
   不覆蓋原工作區旁掛證據。若再有 main 新進展，分開記錄 merge commit 與 latest main。
5. 核對 merge commit 的後續 Lean CI，保存 run URL／實際 checkout SHA／結論。
   預設文件 workflow 的 archive 還原缺陷仍保留；不宣称未跑或失敗的文件 CI 成功。
   數學／LC 範圍不因 merge 擴張，不新開證明輪次。

回傳 PR URL、MERGED 狀態／時間、merge SHA／parents／tree、remote／tracking main SHA、
受驗 head ancestry 結果、合併後 CI 與正式證據包路徑、工作樹保留狀態及未完成事項。
合併後 CI 未完成時如實記 pending；不能以 merge 命令 exit0 代替最終回讀。

文件 workflow 還原修復為另案維護：在新的分支按 archive 工具既有介面先還原再 check，
另跑文件 CI，保留本次原 FAIL 與報告；不在 M5 偷渡新候選／證書重生成。
