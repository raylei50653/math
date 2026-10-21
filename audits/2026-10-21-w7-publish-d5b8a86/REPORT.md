# W7 相連證據發布核對

2026-10-21；BASE `d5b8a8605bcbcef7aebbcf1934dad7ba255ccf02`。
使用者明確授權 commit + push。本次包含三個相連工作目錄：完整計數錐、
數值優化探索、可復用結構與專用CPU算子；沒有新數學排除或Lean定理。
數學與性能結果由[當輪報告](../2026-10-21-w7-reuse-d5b8a86/REPORT.md)保存。
當時「未提交」及原始成功／失敗診斷保留；目前發布入口為
[整理紀錄](../../docs/history/2026-10-21-w7-operator-publish.md)。

## 保存範圍

[依賴清單](dependency/inventory.json)記錄251個相連非暫存檔案，共119118856 bytes。
35份大型或含歷史whitespace的檔案追加至既有ARCHIVE，32個新去重blobs共
54556051 compressed bytes。原始111777792 bytes在本機保留，checkout依
ARCHIVE還原；其餘216檔作普通Git來源／報告／小型證據。
原archive records逐項不變，詳[增量](archive-additions.json)及原metadata的gzip快照。
編譯的`.so`、build與bytecode是暫存，未納入研究交付。

三包原始證據、cone的88個sealed outputs、reuse的69個sealed檔與原BASE輸入
均保留bytes與SHA。共享README／STATUS／guide更新前的原文存於
`routing-before/`，新verifier用快照核對原pin，將授權routing變動與科學輸入分開。
沒有以目前HEAD或目前docs替換舊證據。完整依賴另包含先前已封存的輸入，
新checkout必先執行`tools/audit_archive.py restore --artifacts`。

## 實際重播

[完整cone重播](cone-replay/report.json)：normal／hash17均核對2649個來源輸入、
88個sealed outputs、全部cap／orbit及十項正量；獨立normal／seed17各拒絕
四種模型污染與八種malformed certificates。計數錐明示OPEN。

[算子獨立重播](independent/replay-summary.json)保存normal／seed17、
Fourier及試跑的唯讀檢查；所有舊sealed bytes不變。沒有再跑solver或測速。
`verify.py --numerical`從repository-relative warm path核對舊絕對路徑所記錄的SHA，
以顯式A重算原始／最佳／最終點；不執行舊腳本對原workspace的絕對路徑讀取。
舊腳本與trial input都保持原bytes。

舊GPU wrapper `gpy`的scratchpad預設屬歷史環境，重跑GPU探索須另指定有效
`CUOPT_VENV`；CPU算子與本批可攜重播沿用`py`的鎖定環境，不依賴該scratchpad。

發布時另執行`lake build`、文件連結／索引、正式docs及全樹DocGraph、stage
artifact政策與whitespace核對，結果收於本目錄publication檢查紀錄。
全樹DocGraph的既有歷史重複ID與正式docs結果分開；不刪舊資料製造PASS。
新checkout以暫存stage匯出、還原完整archive後重播保存與數值入口。

## 重播入口

```bash
python3 -B tools/audit_archive.py restore --artifacts
python3 -B audits/2026-10-21-w7-publish-d5b8a86/verify.py
audits/2026-10-20-w7-count-opt-d5b8a86/py -B \
  audits/2026-10-21-w7-publish-d5b8a86/verify.py --numerical
python3 -B audits/2026-10-20-w7-count-cone-d5b8a86/check.py --controls --orbits
```

下一個窄問題仍是共享Z限制的獨立基底與完整重建，或精確共同primal／dual；
數值試跑的密度增加沒有解決精確化。研究停止點見[Kempe導覽](../../docs/c5_kempe_guide.md)。
本批沒有把算子測速、近似殘差或`lake build`提升為來源排除、一般覆蓋或Lean結果。
