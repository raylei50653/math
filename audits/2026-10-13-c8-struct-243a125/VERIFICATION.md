# C8-STRUCT 驗證紀錄

本輪正常及 `PYTHONHASHSEED=17` 的整包重播、凍結輸入負控制與文件檢查，
保存於 [validation-02/verification.json](validation-02/verification.json)，全部數學
checker 通過，正常／seed17 輸出逐位元一致。
根重播只读輸入與證書，不呼叫 LP solver，不重跑上游排除搜尋。

```bash
python3 -B audits/2026-10-13-c8-struct-243a125/check.py
python3 -B audits/2026-10-13-c8-struct-243a125/check_results.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-c8-struct-243a125/check.py
python3 -B audits/2026-10-13-c8-struct-243a125/verify.py
```

`verify.py` 每次建立新的 `validation-NN/`，保留既有重播紀錄。
`check.py` 先核對59份凍結輸入，再呼叫四份獨立 checker，最後另行接合
「兩項來源排除＋八項新必要向量」，核對148列等色 preimages 與八份向量
各91個 cofacial 非空條件。它不把兩份已排來源的中間計數錐可行向量
重新標成最終殘留。結果為2/10排除、8/10殘留，總計62/70排除。

## 分項與負控制

| 核對 | 結果與證據 |
| --- | --- |
| 原具名分類 | 五對完整映射、13,700 transfer係數；[紀錄](classification/verification.json) |
| cofacial 有限核心 | 91 partitions、910完整交集、兩份各74列等色清單；同上 |
| 幾何有限核心 | 200具名弦子域、C4/C5全部空剖分、兩份有完整oriented faces的反控制；[正常](geometry/check.log)、[seed17](geometry/check.seed17.log) |
| 可逆Kempe共同計數 | 821列、1,552一般／981三角化生成元、四份迫零dual、六份舊向量分離dual、十份中間計數解；[紀錄](kempe/verification.json) |
| 發現流程重播 | 精確證書與生成資料逐位元一致；[紀錄](kempe/discovery.replay.json) |
| 輸入漂移 | 59份SHA256與大小一致；錯誤SHA的實際checker CLI必非零退出 |

分類／cofacial 的11項實際 CLI 破損證書全部拒絕。幾何的5項負控制
見 [negative_controls.log](geometry/negative_controls.log)。Kempe的5項
程式內負控制及2項實際CLI控制見 [VERIFICATION.md](kempe/VERIFICATION.md)。
這些是 fail-closed 證書控制，不是實際目標來源樣本。
最終 [RESULTS.json](RESULTS.json) 另由 `check_results.py` 核對八份完整新向量
與兩份排除證書，並拒絕將結果改成「十項全排」的負控制。

兩份有限圖控制分別反駁「只靠局部度數就迫小C5為五輪」及「私人點H度數
只需三仍可排內弦」。其狀態為 `counterexample to weakened claim`；
完整最小933／941來源前提為 `not triggered`。紙面小cap／quotient定理的
有限介面則為 `triggered and holds`，具有任意大小完備性論證。

## 獨立紙面審查

* [幾何審查](classification/GEOMETRY_REVIEW.md)：小代表替換只保完整關係，
  不宣稱計數雙射；outerplane與ear論證保留全域最小性。
* [Kempe審查一](geometry/KEMPE_REVIEW.md)、[審查二](classification/KEMPE_REVIEW.md)：
  固定頂點色對集合、可逆軌道、穩定子權重及三角面介面論證。
* 迫零dual只需、也只宣稱在支援落於原U的生成元上非負；外於U的生成元
  已由原零列排除。舊向量分離dual才是在全部一般生成元上非負。

## 文件與修改界線

首次全域文件檢查遇到並行N2文件尚未完成的連結／索引；本輪沒有修改該文件。
最終live文件檢查、正式docs DocGraph、本輪audit連結與差異空白檢查均通過。
全工作樹DocGraph仍失敗，恰為62項既有duplicate-ID，沒有其他錯誤類型；
不把正式docs的通過改稱全域通過，也不刪除快照修飾結果。
本輪新audit的Markdown另逐一檢查本地連結，排除frozen歷史副本。

[validation-01](validation-01/verification.json) 保留第一次整包驗證的文件發布
時序失敗：數學與seed17已通過，但當時 `VERIFICATION.md` 尚未寫入，導致
REPORT的連結檢查失敗。補齊文件後另建validation-02，沒有覆寫首次紀錄。

直接更新：`docs/c5_neartri_boundary_collar.md`、`docs/c5_kempe_guide.md`、
`docs/STATUS.md` 的外圈對應條目。其他session並行新增或修改不在本輪範圍。
README／HANDOFF不改，因研究線與路由未變；度數下界consumer不改，因共同
下界仍為h≥3、n5≥9。上游audit、舊manifest及歷史失敗均保留。

新紙面定理未Lean化，未執行不相關的Lean重建；没有commit、push、PR或Issue。
