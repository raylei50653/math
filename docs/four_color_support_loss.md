# 完整接口支援流失的增量傳播

2026-10-27。接續[delta傳播](four_color_delta_propagation.md)，新增可選
`propagation_method="support"`。已實作完整支援差量與對側刪列、補上等價紙證及Lean核心，
但同40例與原本delta比較，**尚未取得整體改善**；不改原預設scan。

[接口實作](../scripts/four_color_intersections.py) ·
[主引擎](../scripts/four_color_constraints.py) ·
[測試](../tools/tests/test_four_color_support_loss.py) ·
[比較程式](../scripts/four_color_propagation_experiment.py)

## 數學契約：失去最後一份完整支援才傳播刪除

固定原點身份、字面色框及完整有序接口 \(I\)。上次完成兩側半連接並提交後，
兩份完整關係 \(L,R\) 滿足

\[
\pi_I(L)=\pi_I(R)=S.
\]

其後兩側只能刪列，得到 \(L'\subseteq L\)、\(R'\subseteq R\)。定義

\[
\Delta_L=S\setminus\pi_I(L'),\qquad
\Delta_R=S\setminus\pi_I(R').
\]

\(\Delta_L\) 表示整份接口指派在左側已無任何完整列支援。
不能改成 \(\pi_I(L\setminus L')\)：例如左側原有 \((0,1,0),(0,1,1)\)，
接口為前兩欄，只刪第一列後，\((0,1)\) 仍有第二列支援，不能刪掉右側相容列。

新的共同支援及兩側結果恰為

\[
\boxed{S'=S\setminus(\Delta_L\cup\Delta_R)
=\pi_I(L')\cap\pi_I(R'),}
\]
\[
\boxed{L''=\{\ell\in L':\pi_I(\ell)\notin\Delta_R\},\qquad
R''=\{r\in R':\pi_I(r)\notin\Delta_L\}.}
\]

證明：新投影都是S的子集，第一式由集合差及交集直接得到。
任一 \(\ell\in L'\) 的接口已在S中，所以不屬於 \(\Delta_R\)
恰好等於仍屬於 \(\pi_I(R')\)，這正是完整半連接的保留條件；右側同理。
每列私有座標原封保留，不以不同列的各欄支援拼接。
任何滿足全部目前因子的共同指派，其左右限制互相提供同一接口支援，因此不會被刪；
反方向只刪列也不會新增全域解。兩種傳播保留逐份相同的全域解集合。

兩側同時變更仍適用。如果兩側只刪了私有延伸而接口投影未變，兩個差量皆空，
不必再篩選對側。若完整接口是三欄，仍須保留三欄聯合關係；偶／奇parity負控制
即使一元、二元投影相同，完整支援仍互斥，結果必須為空。

有限關係持續刪列，且沒有無限新增因子時，這類傳播只能有有限次嚴格刪減。
這不代表任意多表網路的局部穩定已能保證共同解；最後仍使用原完整消元與共同回填。

## 本次實作到哪裡

沿用delta的變動配對佇列及原處理順序。在每次**完成兩側結果提交後**，保存完整S、
接口欄序與兩側revision。下次由最新完整投影計算兩個差量；對側已有完整分組索引時，
只取失去支援所對應的完整原列刪除，不重收集全部保留列。整表就是接口時用集合差。

此版增量的是**對側列篩選**。差量發現仍需取得當前完整投影；revision改變仍會喚醒配對，
尚未將所有刪列入口改成持續維護每個接口支援的重數，也未做到只有最後支援消失才入列。
一般域掃描與環傳播也未全改成事件驅動。

支援訊息與完整分組索引共用 `interface_cache_max_rows` 上限：
訊息每個接口tuple算一列引用，分組每份完整原列引用算一列。
這是保留索引的容量限制，不是位元組或暫存記憶體上限。
容量不足時淘汰完整快取項目；容量為零、訊息被淘汰、接口欄序改變或新因子沒有完成紀錄時，
回到原精確delta查詢，絕不截掉語義關係的邊界列。
啟用有效訊息快取需同時設 `--interface-cache` 與正容量。

同一因子身份只可刪列，且須增加revision；成長、替換或scope變更須使用新身份。
退休因子的訊息會清除。查詢中斷不提交部分結果或新S，未完成配對仍待處理；
已完成的加速索引可以保留。未查或超限不能當成無支援，回填仍在完整消元之後。

`checks`包含完整投影建構、差量成員檢查、分組及原列存取；
集合複製、排序、佇列及訊息管理並非逐項CPU計數，牆鐘時間則包含這些成本。
支援差量小也不代表整次查詢只花 \(O(|\Delta|)\)：建立投影與複製結果仍可能與表長成正比。

## 同40例比較：未見整體加速

[原排程完整比較](../artifacts/four_color_support_loss/none/comparison.json) ·
[資訊分區完整比較](../artifacts/four_color_support_loss/information/comparison.json)

沿用固定40份原圖與固定色，每例工作5,000,000、完整表列1,000,000、prefix枚舉、
共同接口快取、原環及共同條件傳播。每組依序跑delta、support，計時時未同時跑回歸測試。

| 設定 | 總檢查 | 接口交集檢查 | 求解秒數 |
| --- | ---: | ---: | ---: |
| 原排程＋delta | 10,265,841 | 3,882,700 | 10.710 |
| 原排程＋support | 10,353,366 | 3,970,225 | 10.798 |
| information＋delta | 10,229,773 | 3,895,492 | 10.881 |
| information＋support | 10,313,164 | 3,978,883 | 11.274 |

原排程總檢查增0.85%、接口工作增2.25%、單次時間增0.83%；38例檢查增加、2例相同。
資訊分區分別增0.82%、2.14%、3.61%；37例增加、2例相同、1例減少。
時間只是本機單輪觀察，微小差異不能當成穩定速度比例；確定的計數亦未呈現整體省工。

四次各為27份合法著色、13份精確無解、0份超限。同排程兩模式除工作／快取計數及模式名稱外，
**完整輸出逐份相等**：包含事件、域、全部消元表及fibres、來源、次序與最後回填色。
不是只核對SAT／UNSAT。獨立原圖核對仍分成4例全解枚舉、24例完整投影、
10例指定見證及2例無解參考，不將後12例擴大成全解窮舉。

原排程實際處理配對仍為110,000次；24,795次使用已存訊息，其中18,678次差量為空，
占75.33%。共記錄24,939個方向支援流失、刪除7,135份對側列；同一tuple在不同配對／方向
可重複計數。完整分組建立次數仍為49,490次，與delta相同，沒有省去投影重建。
各案例峰值快取列引用的加總由568,804增為766,602；此加總不是單次峰值或RAM位元組。
原delta已會略過單側改變但投影不縮的情況；新訊息保存、兩側差量辨識與掃描S的成本
沒有被對側刪列收益抵銷。

## 稀疏與密集流失控制

[控制程式](../artifacts/four_color_support_loss/control.py)與
[完整結果核對](../artifacts/four_color_support_loss/control.json)另測一對關係：
16份兩欄接口、左表64列、右表65,536列，每個右接口有4,096份私有延伸。
初始兩模式都需65,618次檢查；保存完成接口後再刪左側支援，完整結果均與純半連接逐列相等。

| 流失支援數 | delta更新檢查 | support更新檢查 |
| --- | ---: | ---: |
| 1／16 | 61,518 | 4,177 |
| 15／16 | 4,104 | 61,479 |

少量流失時，刪除少數失效分組確實比重收集大量保留列省工；大量流失時恰好相反。
這是刻意構造的完整關係控制，沒有當成實際圖整次求解的測速證據。
下一個可檢驗方向是維護最後支援重數，並依保留／刪除工作量選擇方向；本輪尚未實作。

## 形式化與回歸邊界

在[Lean核心](../Math/ColoringElimination.lean)新增 `interfaceSupport`、`interfaceLoss`，
證明 `interfaceSupport_mono`、`common_support_after_losses` 及 `semijoin_by_lost_support`。
一般投影函數表示同一完整有序接口；後兩定理分別對應共同支援差量式與對側刪列式。
這些是關係語義的kernel證明，沒有形式化Python佇列、快取容量或普遍速度界，亦無新四色定理證明。

新增13項測試涵蓋最後支援負控制、雙側變更、私有延伸、三元parity、欄序／身份替換、
隨機刪列、零／小容量、逐工作中斷重試，以及小圖完整紀錄／fibres、儲存上限及CLI。
全套四色測試387項通過。證據目錄另存來源快照、完整壓縮輸出、雜湊及
[測試日誌](../artifacts/four_color_support_loss/tests.log)、
[Lean建置](../artifacts/four_color_support_loss/lean-build.log)、
[公理稽核](../artifacts/four_color_support_loss/axioms.lean)。

重播時用新目錄，避免覆寫當輪證據：

```bash
uv run --with-requirements requirements.txt python scripts/four_color_propagation_experiment.py --out-dir /tmp/support-none --partition none --methods delta support
uv run --with-requirements requirements.txt python scripts/four_color_propagation_experiment.py --out-dir /tmp/support-information --partition information --methods delta support
python3 -B artifacts/four_color_support_loss/control.py --out /tmp/support-control.json
lake build Math.ColoringElimination
lake env lean artifacts/four_color_support_loss/axioms.lean
```

實際本輪使用本機已快取且可載入networkx的Python，執行命令與來源雜湊記在
[驗證收據](../artifacts/four_color_support_loss/verification.json)。
