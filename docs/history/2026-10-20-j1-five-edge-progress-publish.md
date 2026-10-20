# J1 五邊路、W7 同源計數與精確殘餘整理發布

2026-10-20；發布前HEAD為`417732fc5ef0a012829fd6712333b1c906128d3a`。
使用者明確要求整理目前進展並`commit + push`。
原研究報告與verification中的「未commit／push」保留研究交付當時語境，
本次以新的發布紀錄承接，不改寫原證據或seal。

## 成果與未完成範圍

| 範圍 | 本次保存的結果 | 仍OPEN |
| --- | --- | --- |
| 一般J1 type III實際五邊路 | [原幾何紙證](../../audits/2026-10-20-r6-941-j1-five-edge-417732f/geometry/PROOF.md)逐項排14條弦，得原induced C7；不先假定路點全私有或R五度。 | C7內多點的來源結構、type I與更長路。 |
| 嚴格only-R子型 | 原C7內恰R才推出完整W7、R七度及同源C13；720份完整接觸選擇保112份共同必要型。 | 此子型未排除，也未證覆蓋一般五邊路。 |
| 完整同源計數 | [全部66,430類cap](../../audits/2026-10-20-r6-941-j1-five-edge-417732f/counting/PROOF.md)獨立重建一致；完整orbit支援閉包留61,308類、307,197欄；兩個目標仍存活。C11的132行直接拉回有±4反控制。 | 支援存活不證共同計數可行。單次LP無結論，無可行點、對偶或來源排除。 |
| 精確殘餘與接回 | [一般transport紙證與真disk控制](../../audits/2026-10-20-r6-941-j1-five-edge-417732f/residual/REPORT.md)保原始／當前見證，逐步傳輸再共同篩選；真14點disk全枚舉核對2→1→1→0、全源3/3對selected2/0及cap1→0。 | 局部控制不觸發完整J1來源；一般壓縮、cap-compatible來源下降及較小bad未得。 |

一般J1兩項／J2六項、H4、同候選三拒絕、嚴格較小bad、
`W110+W101>0`、`omega_e=0`、完整319及主命題仍OPEN。
沒有新Lean theorem；紙證、固定域整數證書與`lake build`分開。
完整研究結果及下一入口見[原報告](../../audits/2026-10-20-r6-941-j1-five-edge-417732f/REPORT.md)、
[Kempe導覽](../c5_kempe_guide.md)與[State導覽](../c5_state_guide.md)。

## 原始bytes、封存與提交範圍

本次[來源清單](../../audits/2026-10-20-j1-five-edge-publication-417732f/SOURCE_FILES.json.gz)
固定2,649份非快取檔案、245,969,917 bytes；包含凍結依賴、全部空fibres、
完整lifts、負控制及無結論的探索紀錄。
其中2,593份凍結輸入、236,677,985 bytes追加到既有ARCHIVE，去重後新增915個
gzip blobs、50,648,795 compressed bytes；舊files與blobs records完全不改。
原始路徑仍留在本機，Git保存精確索引與gzip，沒有修改封存來源。

新checkout先還原，再重播：

```bash
python3 -B tools/audit_archive.py restore --artifacts
python3 -B audits/2026-10-20-r6-941-j1-five-edge-417732f/check.py
python3 -B audits/2026-10-20-j1-five-edge-publication-417732f/check_custody.py
```

提交只含此研究包、發布核對、所需新blobs、ARCHIVE與ignore路徑、兩份導覽及STATUS。
README／HANDOFF已核對，研究線與活躍標記未變，沒有新增逐輪摘要。
本輪不增加大型JSON例外、不放寬儲存政策。

## 發布核對

獨立唯讀審查未發現來源、量詞或摘要越界，見[審查紀錄](../../audits/2026-10-20-j1-five-edge-publication-417732f/independent-review.md)。
正常／seed17研究重播、原seal、竄改負控、原始來源與Git index／gzip逐bytes一致、
從Git index匯出並還原的新checkout重播、文件、正式docs DocGraph、
artifact policy及staged空白檢查的實際結果見
[發布檢查](../../audits/2026-10-20-j1-five-edge-publication-417732f/publication-checks.json)。
`lake build`完成8,832 jobs，只有既有linter warnings；工具測試94項通過。
全工作樹DocGraph未重跑，正式docs範圍通過不代表frozen／歷史副本全樹通過。

最終commit、push、本地／tracking／遠端SHA及工作樹狀態以完成時的即時Git核對為準；
本紀錄不預先宣稱遠端CI成功。
