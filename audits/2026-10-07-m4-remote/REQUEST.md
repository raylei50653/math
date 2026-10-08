# 可直接發布：M4-R 遠端交付與 CI 驗收

M4-L 已由 [監督驗收](REPORT.md)通過，限保留的具名例外。
本任務更新原 [M4-R 派工](../2026-10-07-merge-supervision/M4_REMOTE.md)的 final SHA
及 whitespace 分類；原封存派工不改寫。

**任務：將下列已驗收 final SHA 正常 push 至 `integrate-kprime-e3`，
建立或更新 base=main 的 PR，取得該 head 的 CI 結果並回報，停止於待監督驗收。**
不 merge、不啟用 auto-merge、不 force push。不要為納入本輪旁掛監督輸出再作 commit。

| 欄位 | 固定值 |
| --- | --- |
| final head | `1f21c8f09dfcb5110ea1a3d66399e9c0a54ceeaf` |
| 直接 parent／原 M1–M3 候選 | `ba0b447f09617591d9f2ba81c988f537af771791` |
| 本地驗收 main 基準 | `2ddc6b4a4e412ab2cb7917fe4fb6fdeef2e86090` |
| 正式包 | `audits/2026-10-07-m4-local/DELIVERY.json`，572 entries＋seal＝573 檔 |
| 已保存 final receipt | `audits/2026-10-07-m4-supervisor/acceptance/final-receipt/FINAL_RECEIPT.json` |

1. 先讀即時 remote main／同名 branch、PR 狀態及本地 tracked diff。
   核對本地 head 是上述完整 SHA、tracked/staging 乾淨，保留 scratch 與旁掛監督包。
   遠端有新提交時先讀差異；不覆寫其他工作。main 若前進，回報完整新 base 與差異，
   不自動 rebase／merge main 或改 final head；監督端需要重新評估驗證覆蓋。
2. 正常 push 已驗收 commit，建立或更新同名 branch→main PR。
   使用 [PR_BODY.md](PR_BODY.md)覆蓋整分支成果；回報精確實際 base。
   PR 必須揭露五項 strict FAIL、原 86／匯入 log 85 whitespace、新 authored 0、
   缺失歷史證據、工作區 scratch DocGraph 62 duplicate-id 與 fresh checkout PASS 的差別。
3. 等待對應 final head 的 Lean CI 完成，保留 run URL、event、head SHA、各 job 結論。
   優先取 push／branch run 的 exact head 證據；PR merge-ref run 另外列出其 checkout SHA
   與關聯 PR head，不混稱兩者相同。舊 SHA 成功、空 checks、skipped/cancelled/pending
   都不當成已通過。必要時可 dispatch 現有 Lean workflow 到該 branch，並核對實際 SHA。
4. 文件 workflow 目前只有 workflow_dispatch。可以交付同 final SHA 的既有本地文件／
   anchors/index／預設 DocGraph 證據；若 dispatch，回報該 run 的實際 SHA 與結論。
   預設 Lean CI 是 `lake build --no-ansi`、defaultTargets=Math；
   顯式 LC build／558 項公理依沿用的同 hash M3 證據，不宣稱由預設 CI 重跑。
5. 結束前重新核對 local／tracking／remote branch 三者都為固定 final SHA，
   重新讀 PR head／base、mergeability／review／required checks／待解 threads。
   若 checks 失敗，保存原 logs 與失敗分類，不自動改候選或更新舊證書。

回傳至少：

- PR URL、PR head／base 完整 SHA、base branch、是否 draft、mergeability／review／checks 狀態。
- local／tracking／remote branch SHA、即時 remote main SHA、是否 main 前進及差異摘要。
- Lean CI run URL／event／head SHA／實際 checkout 證據／各 job 結論；文件證據路徑或 run。
- 正式交付 manifest 與 final receipt 路徑、source/seal 零漂移確認、工作樹狀態。
- 本次操作命令／logs、所有未完成或失敗項，以及未 merge／未啟用 auto-merge 的確認。

監督端收齊並核對後才判可合併；實際 merge 仍依使用者另行明確指示。
U2–U4 等一般研究缺口保持本 PR 的停止點，不在本次發布任務另開證明輪次。
