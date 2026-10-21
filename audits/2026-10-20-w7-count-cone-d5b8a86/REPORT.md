# 嚴格 only-R／W7 完整同源計數錐：尚無精確證書

2026-10-20；BASE `d5b8a8605bcbcef7aebbcf1934dad7ba255ccf02`。
**本輪落在「仍無證書」：既有必要計數錐維持 OPEN。**
尚不能排除嚴格 only-R／W7 子型，也未取得同時滿足全部十個正量的有理／整數
共同可行點。模型完整性檢查通過與數值停止都不是可行性裁定。

## 固定範圍與完整殘餘

承接[前輪來源契約](../2026-10-20-r6-941-j1-five-edge-417732f/SOURCE_CONTRACT.md)
的全部原圖前提，只處理同一 J1 type III 實際五邊路圍出的 induced C7 內部
恰只有原 R 的嚴格 W7 子型。一般 C7 多內點、type I／更長路及一般 J1／J2
不在此子型內。詳[本輪模型](MODEL.md)及[獨立合同審核](review/REVIEW.md)。

初始工作樹乾淨，HEAD 即指定 BASE；證據工作前凍結前輪2,649份檔案的 bytes
與 SHA256，見 [BASE.json](BASE.json)。前輪報告、輸入及證書均未改寫。
完整計數系統保留同一組 Z,X、全圖完整 fibres、全部 private components
重數與同列完整 cap lifts；沒有把選路後殘餘或各自可行的 marginals 當成全來源。

[RESIDUAL.json](RESIDUAL.json) 是完整殘餘的復原入口，逐項列出全部61,308個
live Z、5,098個初始零格及24個閉包零格、X欄編號、十個正量、方程與完整
輸入檔的 Git blob／bytes／SHA256。其引用的原始整數檔保留所有66,430個
canonical states、完整 cap 矩陣、199,290個 half-row 對應及307,197個存活欄，
不是只保存統計摘要。所有183,924條方程同時要求

```
2 Z_i(h) = Σ_{j: h∈C_j} X_j，Z≥0，X≥0。
```

正量是原 G 七個支持列、h=a／h=b兩個 sectors，以及
`Z_44459+Z_44466>0`，共十項。兩個 target 不被各自強求正。
112份共同接觸型所迫的額外原弦／零 fibre 尚未逐型加入，沒有默認它們成立。

## 實際求解與停止原因

[solve.py](solve.py) 組合完整凍結矩陣，[exactify.py](exactify.py) 只在候選
通過獨立整數 checker 後才允許建立精確證書。HiGHS版本為1.15.1。
目標單獨正性的子問題是原十項正性的放寬：其精確不可行足排此嚴格子型，
其可行則還需補齊其他原正量。本輪沒有把放寬問題的停止當成全模型答案。

| 嘗試 | 實際停止 | 可用精確證書 |
| --- | --- | --- |
| target正性、內點法、600秒 | 4次內點迭代後建基底至時限；回傳 primal/dual 均 invalid | 無 |
| 齊次最大化target、dual simplex、600秒 | 39,097次迭代後到時限，仍在phase I；回傳 primal/dual 均 invalid | 無 |
| 同一齊次問題、primal simplex | 約7.49秒回報 `Solve error`，沒有有效基底／解 | 無 |
| target正性、PDLP、300秒 | 24,785次迭代後到時限；回傳 primal/dual 均 invalid | 無 |
| 直接完整target對偶、300秒 | 13,797次迭代後到時限，`x=None`，沒有 primal/dual/ray | 無 |
| 全十正量、內點法、300秒 | 9次內點迭代後建基底至時限；回傳 primal/dual 均 invalid | 無 |

每次 root 求解的 `input.json` 記錄 arguments、變數順序所依據的凍結模型、
矩陣大小與 nnz；同目錄的 `highs.log`、`result.json`、`solution.pickle` 保存
實際回傳。直接對偶的完整 SciPy OptimizeResult 在
[full-dual.pickle](review/full-dual.pickle)。invalid／None 表示沒有可用迭代點，
不假造可供有理化的解；原始非有限數值診斷保留原貌，不作證書使用。

740個 singleton half-rows 的整數 dominance／SCC 推導沒有新增零欄；
兩個目標仍存活。[精確停止記錄](review/singleton-reduction.json) 只證這種
指定消去法已停止。三個局部對偶支援搜尋亦未得證書，其數值 infeasible
只限制指定 multiplier 支援，不能證原錐可行。

消去 Z 的 column-generation 保存 restricted master 與逐全欄定價殘餘。
最後有效 master 有5,528個欄，phase-I optimum為1/8；下一個5,631欄 master
在累積140秒時限停止，primal infeasibility約2.798，沒有可用點。
其[精確殘餘](sparse/warm2-44459/exact-dual-residual.json.gz)用13個整數
half-row weights 得到真正恆等式

```
2 Z_44459 = Σ_j price_j X_j。
```

其餘61,307個live states的係數全為零。307,197個欄的整數prices完整保存：
103個為+1、95個為−1、8個為−2、306,991個為0。
**103個正價欄仍是這份指定 potential 的完整未消殘餘**，所以它不是不可行
證書；另一個target 44466也未由此排除。restricted phase-I非零也不是可行點。
殘餘replay只驗證上述恆等式和完整價格清單，明示計數可行性仍OPEN。
[獨立重播](sparse/replay_exact_residual.py)在normal、seed17及seed17加`-O`
結果相同；half-row／state／漏正價欄及bool係數四種竄改，在normal與`-O`
共八次均被拒絕。

## 獨立驗證與交付邊界

[獨立 checker](independent/check.py) 不 import solver、只用標準函式庫，
從原邊重建66,430×(30+2)個完整 cap／sector 係數、原 C10 繼承零值、
S4 canonical states及H8 half-row map，與凍結資料逐項相等。
完整 orbit 家族也由前輪生成器唯讀重建，742,900個 noncrossing partitions、
41,834個 admissible partitions、428,506筆去重前欄及最終307,197欄皆吻合。
4種模型竄改、8種 malformed certificate 控制遭拒；沒有把全零解當可行。

```bash
python3 -B audits/2026-10-20-w7-count-cone-d5b8a86/check.py --controls --orbits
PYTHONHASHSEED=17 python3 -B audits/2026-10-20-w7-count-cone-d5b8a86/check.py --controls --orbits
```

這兩個命令核對完整性、來源 custody、負控制及完整 orbit 重建；目前輸出
`necessary_cone=OPEN`，**不輸出 feasibility PASS**。若日後提供整數 primal／dual，
可用 `--certificate PATH` 對全部座標逐一驗證。[證書格式](independent/README.md)
及 [MODEL](MODEL.md) 寫明兩種證書的精確意義。

本輪 `lake build` 通過8832 jobs，只有既有 linter warnings；沒有新增 Lean。
normal／seed17、輸入零漂移、文件檢查、Git diff及輸出seal的實際結果見
[verification.json](verification.json)。正式docs的DocGraph通過；全樹DocGraph
仍有72個既有frozen／scratch duplicate-ID errors，沒有本輪新目錄的錯誤；
未刪舊副本來製造全域PASS。未重跑無關研究證書，沒有commit或push。

Closure scope：完整必要錐已獨立核對並保留可重播裁定入口；**可行性仍 OPEN**。
Canonical source：本文、MODEL、RESIDUAL及獨立checker；來源覆蓋沿前輪紙證。
Updated：Kempe導覽與STATUS的相關入口。
Reviewed-unchanged：State殘餘／cap語義、README與HANDOFF，沒有新來源排除或研究線變動。
Remaining OPEN：嚴格W7計數可行性、112接觸型強化、一般C7多內點、J1／J2、
嚴格較小bad及主命題。
Propagation stop：L1；沒有子型排除、共同可行點或Lean新定理可傳向父題。
接續時應先利用本輪完整定價殘餘或改善退化系統的求解，不因 timeout
宣稱必須增加幾何限制；目前接續入口見 [Kempe導覽](../../docs/c5_kempe_guide.md)。
