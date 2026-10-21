# W7 兩型完整界面與局部縮減：相連證據發布核對

2026-10-21；Git BASE `13e51db3ec3d8d7ec7eeef60167afdc19ad956c4`。
依使用者要求整理並 commit + push 四組既有研究；完整結論及OPEN邊界見
[整理紀錄](../../docs/history/2026-10-21-w7-interface-publish.md)與
[原整合報告](../2026-10-21-w7-remaining-two-13e51db/REPORT.md)。
原40型仍排38、餘0／1；本次不擴大研究枚舉，沒有新增來源排除或Lean定理。

## 來源保存

[來源清單](source-inventory.json)凍結64份原研究產物及12份不可變重播依賴，
共76個不同檔案、26,465,807 bytes。
[SOURCE_SHA256SUMS](SOURCE_SHA256SUMS)從專案根目錄逐檔核對。
20份凍結輸入另直接對回exclusive Git BASE；當前routing更新不當作數學輸入漂移。
12份舊依賴皆已在Git，沒有被忽略的重播來源。既有gzip完整資料直接納入提交，
沒有新增archive索引、忽略規則或artifact例外。
原研究報告、證書、logs與receipts保持bytes，其「未commit／未push」保留當輪語境。

## 實際驗證

[本次重播](replay.json)列出五個checker各normal與seed17 optimized的十次命令、
退出碼、耗時及新log SHA，stdout逐字相等；未使用`--build`或`--write`。
另重跑三份既有外部污染證書，均拒絕exit 1；profile1五項與n-star三項內部負控制通過。
獨立555檢查由另一套adjacency-list backtracking逐列重建全部602個候選關係。
[建置核對](build-checks.json)記錄`lake build`成功8832 jobs與94項工具測試通過。
Lean原有linter warnings保留於log；build不形式化本輪紙面拓撲。

[發布檢查](checks.json)記錄文件、正式docs DocGraph、Git index artifact policy、
whitespace與來源SHA；全樹仍有72項歷史duplicate-ID診斷，逐項與前輪相同，
沒有本輪新audit出現在錯誤中。初次whitespace檢查發現新歷史檔尾多一空行，
修正後另存final重播；[初次檢查](checks-first.json)保留原失敗紀錄。
[隔離重播](portability.json)由Git stage匯出來源，核對全部76份bytes後再重播，
不借用未追蹤原檔。[獨立審閱](review.json)記錄兩組唯讀範圍及來源核對。

```bash
sha256sum --check --quiet audits/2026-10-21-w7-interface-publish-13e51db/SOURCE_SHA256SUMS
python3 -B audits/2026-10-21-w7-profile0-13e51db/check.py
python3 -B audits/2026-10-21-w7-profile1-13e51db/check.py --controls
uv run --with-requirements requirements.txt python -B audits/2026-10-21-w7-remaining-two-13e51db/check_n_star.py
```

未重跑大型LP、數值求解、廣泛來源枚舉或不相連研究線。
兩型來源排除、精確計數錐、原E條件替換、一般W7／J1／J2及具體較小bad仍OPEN。
發布後commit、遠端分支與CI狀態以即時Git／GitHub核對為準。
