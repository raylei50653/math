# 2026-10-30 研究成果提交核對

整理基準 `e1a90fea41702d7c98747716a5960198aecbecb3`；本批成果的跨線說明見
[整理紀錄](../../docs/history/2026-10-30-research-results.md)。只作本地 commit，沒有推送。

- `SOURCE_SHA256SUMS`：389 份原研究來源；含原 audit、報告與腳本，還原 ARCHIVE 後可用 `sha256sum -c` 核對。
- `source-preservation.json`：294 份原 audit 檔保持 bytes；舊 ARCHIVE 的 6,150 筆檔案與 3,125 筆 blob records 不變。相對基準新增 23 路徑／23 blobs，其中本次補封存 3 份，其餘沿用研究階段已備內容。
- `c5-replays.json`、`4ct-replays.json`、`bernhart-z-replays.json`：本次實際執行的 17 項有限重播。已保留的輸出／完整 logs、摘要、計時與未量測欄位各依收據標示。
- `checks-*.json` 與對應 logs：本次文件、測試、封存及 Git index 檢查的原始結果。正式 docs 與全樹 DocGraph 分開記錄。

本次沒有重跑 P4 的完整來源分類、既有其他大型枚舉或 Lean build，沒有新增 Lean 定理。
保存來源及通過有限重播，均不提升一般 932、4CT、Bernhart 目標來源或交叉數不可避免性的結論。

已知檢查限制：全樹 DocGraph 有歷史快照的 72 項 duplicate-id；正式 docs 另驗。
本次提交來源 `scripts/c5_six_cross_round_review.py` 末尾原有一個額外空白行，
標準 staged whitespace 檢查會報該處。該腳本與原證書以 `checker_sha256` 綁定，
本次保留兩者原 bytes 及精確 `--check`，不把該檢查寫成通過，也不新增 whitespace 例外。
這是本次待提交來源的格式問題，並非聲稱基準 HEAD 已有同一問題。
