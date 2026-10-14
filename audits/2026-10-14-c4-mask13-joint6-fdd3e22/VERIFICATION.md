# C4-MASK13-JOINT6 重播與證據界線

2026-10-14。每條實際命令、exit code 與 stdout/stderr 檔名見
[receipts](logs/receipts.json)。本包所有三份主 checker 的正常及
`PYTHONHASHSEED=17` 重播、独立完整染色 checker 與直接輸入 SHA 核對
均由本輪執行；具體結果見下表與 receipts。

```sh
python3 -B audits/2026-10-14-c4-mask13-joint6-fdd3e22/controls/check_interface.py --check
python3 -B audits/2026-10-14-c4-mask13-joint6-fdd3e22/controls/check_fibres.py --check
python3 -B audits/2026-10-14-c4-mask13-joint6-fdd3e22/controls/check_geometry.py --check
python3 -B audits/2026-10-14-c4-mask13-joint6-fdd3e22/controls/check_subrelations.py --check
python3 -B audits/2026-10-14-c4-mask13-joint6-fdd3e22/review/check_fibres_independent.py
```

主 checker 為 read-only replay；不加 `--check` 的首次生成採 exclusive-create，
不能拿來覆寫既有證書。全部重播只使用標準 Python library 與本包明列輸入。
幾何資料保留三份舊21點球面的原 record IDs／來源 certificate SHA，以及
一張明列二十面體；驗證會自行重算圖與 face sides，不需讀取原3.6MB全集。

| 證據 | 實際範圍 |
| --- | --- |
| interface | 216→168標號列、9→7全色軌道、10→8固定框列；全部必要component partitions及同步交換 |
| subrelations | 每域128個子集；無額外邊／tp／qs／兩邊的必要mask13閉包數9／1／1／0；無額外邊有4個極小五軌道閉包 |
| fibres | 七張具體plane disks、42份完整染色（含空fibres）、14份集合雙射與逆映射；r的16局部指派及pq共同交集 |
| independent | 不import主checker，Cartesian product完整染色枚舉；重算42份集合、14份雙射及原色值r表 |
| geometry | 四張球面樣本、八個具名開口、八次r五度刪除；S6的實際face sides、原接線、degree、共同鄰點及J |
| frozen inputs | INPUTS.json的16個直接輸入逐SHA核對；上游歷史證書未整套重播 |

負控制包括原邊component拆開、交錯路、錯誤pq列、漏完整lift、兩份破損
球面faces，以及[篡改介面證書](controls/interface_stale_negative.log)的預期拒絕。
初版漏lift控制的兩份歷史證書保留為 `fibres-initial.json`、
`fibres-before-recomputed-negative.json`；當前權威是 `fibres.json`。
錯誤pinched-boundary模型與輸出保留於 [rejected](rejected/README.md)，不計為有效排除。
獨立review最初缺NetworkX的失敗紀錄保留，最終checker已用標準庫完成。

文件检查採 repo 的 `check_docs`、正式 docs DocGraph、全樹 DocGraph 及
`git diff --check`；正式與全樹結果分開，不刪 frozen 證據使全樹通過。
最終狀態記在下方。

真正目標來源為0，幾何控制不測mask假設。有限重播不證無界排除，
本輪沒有Lean theorem、沒有重跑外部≤28枚舉或plantri；兩個條件界依賴
已核對的外部§2完整計算，見 [EXTERNAL](EXTERNAL.json)。

## 實際檢查結果

- 三份主checker正常／seed17共六次PASS，子關係checker另一次PASS，独立checker PASS，16份凍結輸入SHA全部一致。
- `check_docs` PASS：683個Markdown、8,890條本地引用。
- 正式docs DocGraph PASS：97份文件、375條關係、12個families，0錯誤。
- 全樹DocGraph **FAIL**：70項全為duplicate IDs，來自保留的frozen／scratch副本；包含本輪凍結的C4權威文件。不刪除證據，也不將正式docs PASS稱為全樹PASS。
- `git diff --check` PASS。

三份主checker與獨立checker的PASS均限本頁所列控制域；沒有完成一般來源排除。

最終檔案身份見 [MANIFEST](MANIFEST.json)；manifest本身不自列，Python bytecode不屬研究證據。
