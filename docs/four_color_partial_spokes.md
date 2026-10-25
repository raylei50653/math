# 部分輻條搜尋補上九點傳播缺口

2026-10-25。接續[共同條件接口](four_color_cycle_contexts.md)及
[九點固定色反例](four_color_guarantee_gap.md#有限核對的預先範圍)。
本輪只處理有限圖約束引擎的搜尋缺口；不改其他 C₅／W7 研究線。
後續[共同限制登記](four_color_joint_constraints.md)另保存此九點構型的三點等色必要表及完整fibres，
該輪先做手動角色映射原型；再後續[自動找型與主傳播](four_color_joint_propagation.md)已接入必要三元表。

## 預先構造與核對範圍

既有純查詢 `derive_cycle_context` 已允許中心只與部分環點有原輻條，
但自動搜尋限於中心的原鄰點誘導子圖，只會找到全部環點皆有輻條的環。
新增可選 `cycle_context_search="partial"`：對活動原中心 `h`，
在活動原圖刪去 `h` 後找有界基本環，交回同一純查詢。
只使用實際原輻條；原弦、外側附件及其他原限制仍由既有因子保存。

仍保留同一中心色及同一環首點色，輸出原有完整二／三元投影，再經完整共同接口交集
及候選域傳播反覆回饋。不指定任何試查色為已染色，也不加入四元表或完整原圖枚舉作推理。
歷史模式 `neighbours` 保留為預設，不改寫前輪凍結資料及來源快照。

正確性沿用[全部解保留論證](four_color_cycle_contexts.md#全部整圖解保留空關係可靠否定延伸)：
任一整圖解在新找到的原中心／原環上的限制，仍是該局部查詢的一列，
其完整接口投影必保留。改變找到哪些原環不改此論證；局部非空仍不保證全域可解。

先核對原四份缺口／多解控制及三十六份較大圖，以同一五百萬工作上限比較原交集＋原環
與擴大搜尋後的共同條件模式。保留全部原邊獨立枚舉的 6／90 份控制解；
另外解除九點圖固定色，核對全部 48 解均被保留。另測非連續原 ID、搜尋上限及 CLI。
正常／seed-17 使用新輸出目錄核對位元組，不覆寫舊證據。

## 驗證結果

[四十份原圖及固定色](../artifacts/four_color_partial_spokes/inputs.json) ·
[完整比較](../artifacts/four_color_partial_spokes/report.json) ·
[完整記錄](../artifacts/four_color_partial_spokes/runs/) ·
[九點兩模式重播](../artifacts/four_color_partial_spokes/index.html) ·
[驗證收據](../artifacts/four_color_partial_spokes/verification.json) ·
[來源快照](../artifacts/four_color_partial_spokes/baseline-source/)

同一凍結九點原圖、同一字面固定色 `0=0,6=3`：歷史鄰域模式仍在四次消元後判無解，
部分輻條模式在 **零次消元**取得矛盾。使用原有 128 份構型上限及 200,000 步搜尋上限，
共 104 份構型、68,914 次主檢查，未超限。這次沒有單一條件原環為空，也沒有條件原環
直接刪去單點候選；二／三元投影回到完整接口交集後才使共同限制矛盾。

這補上指定固定色的消元前判否，沒有聲稱未固定圖的求解流程已直接輸出 `(0,6)` 等色表。
紙面上，若 `0、6` 異色，可用整體色名置換改成這份固定框，原邊矛盾即證明任一合法解必有
`c(0)=c(6)`；這份紙證與實作是否顯式學到等色因子是兩項不同的結果。

### 可以逐列核對的跨區接口

在歷史模式首次消元前的候選域下，取原中心 `8` 與三個有序原環：

```text
A = (0,1,4,7,5)
B = (0,1,4,9,7,5)
C = (1,5,6)
```

只用環邊及實際原輻條。三份局部關係各自非空，但 A、B 在完整接口 `(8,1,4)`
的交集，與 C 在 `(8,1)` 的投影要求不同的共同配置：

| 同一中心條件 | A、B 的 `(8,1,4)` 交集 | C 的 `(8,1)` 投影 |
| --- | --- | --- |
| `8=1` | 僅 `(1,2,1)` | 僅 `(1,1)` |
| `8=2` | 僅 `(2,1,2)` | 僅 `(2,2)` |

因此共同接口排除 `8=1,2`，只餘 `8=3`，既有原限制再取得矛盾。
三份查詢及表列核對保存在[回歸測試](../tools/tests/test_four_color_partial_spokes.py)；
這是解釋用的小見證，實際有界搜尋不以頂點 ID 或這三份環作硬編碼。

### 同源核對及成本

四十份凍結原圖的兩模式比較，原交集＋原環為 27 可解／13 無解；
部分輻條模式為 **17 可解／13 無解／10 未判定**。所有已完成判定均與獨立參考相同。
十份 `limit` 均達五百萬工作上限，不當成無解或提前成功；擴大搜尋有明顯成本，
因此歷史模式仍為預設。兩份反例（十二點奇輪及九點）均在零次消元取得矛盾。

六份及九十份完整控制解均逐記錄保留；二十四份結構例沿用精確全域投影核對，
十二份隨機例仍只有指定見證／凍結窮盡無解參考，不擴大為全部解枚舉。
另獨立核對未固定九點圖的全部 48 份原邊解，在候選域、原因子、完整回填表及每份輸出接口
均保留；非連續 ID 重標後仍零消元判出指定固定色矛盾。

未固定九點在五百萬上限下完成，使用 1,663,565 次檢查；沿用預設一百萬則回傳 `limit`。
零構型或零掃描上限安全退回原精確消元；搜尋仍只找有界基本環，不保證查遍全部部分輻條構型。
跨區一般傳播完備性、固定大小接口的全域存在保證及直接學到一般等色表仍未解決。

178 項相關測試通過，包含新增七項部分輻條回歸，保存[完整測試紀錄](../artifacts/four_color_partial_spokes/tests.log)。
正常／seed-17 的三份輸入、摘要及八十份 gzip 記錄共 84 檔逐位元組一致；
32 份來源快照的 SHA256 與當輪來源及摘要一致。未固定九點的全部 48 解另對
1,488 張輸出接口逐份核對，共 71,424 次投影 membership；[完整未固定記錄](../artifacts/four_color_partial_spokes/controls/unfixed-nine.json.gz)
及收據均保存。本輪沒有改播放器模板或新增 Lean 定理，未重跑瀏覽器與 Lean build。

## 使用與重播

```bash
python3 scripts/four_color_lab.py solve graph.json --engine constraints --intersections --cycles --cycle-contexts --cycle-context-search partial --max-checks 5000000 --json /tmp/four-color-partial.json --html /tmp/four-color-partial.html
uv run --with-requirements requirements.txt python scripts/four_color_cycle_context_experiment.py --cycle-context-search partial --out-dir /tmp/four-color-partial-replay
PYTHONHASHSEED=17 uv run --with-requirements requirements.txt python scripts/four_color_cycle_context_experiment.py --cycle-context-search partial --out-dir /tmp/four-color-partial-seed17-replay
python3 -m unittest discover -s tools/tests -p 'test_four_color*.py'
```

Python API：`solve_constraints(graph, use_intersections=True, use_cycles=True,
use_cycle_contexts=True, cycle_context_search="partial", max_checks=5_000_000)`。
本選項須與交集、原環及共同條件模式一起開啟。條件計算及接口提交的中斷語義沿用原流程，
仍不提交半份條件支援，不提前寫色。
