# 強迫異色構造研究與驗證紀錄

2026-10-13。BASE=`19209f4cf68261fdce5e84a7804cfe04ae0957bf`。
權威敘事入口：[強迫異色可以傳多遠](../../docs/c5_forced_inequality_transport.md)。
本目錄只含本輪新構造與證據；啟動時已存在的其他六份未追蹤研究目錄保持原樣。
期間另有工作者修改共用報告；本輪沒有採用其新結論，也沒有覆寫其修改。

## 結論與範圍

- 紙面任意大小：兩份不交叉圖族可把四色強迫異色傳至任意大原圖距離；
  完整原子 join／forget 證書寬度≤5。原來源域之外的控制，不反駁 F。
- 紙面任意大小：共用相異色雙支援的一棵樹可平面實現當且僅當為 path；
  三叉含原 K₃,₃。共用三角形的第三個 apex 同樣非平面。
- 無外加色釘的完整交錯 Diff×Diff 不可在 disk 實現；固定 β 需重查交換合法性。
- 邊界外 clique 分隔枝塊只要有一份 witness，就對外 Σ 透明；
  Σ-critical 排除本輪巢狀三角形及割點外掛接力機制。
- 有界計算只是核對上述具名例子，不提供目標來源實現或一般 F／Z／E-ARC2 closure。

逐步證明及交叉審閱：
[theory](theory/REPORT.md)、[topology](topology/REPORT.md)、[alternatives](alternatives/REPORT.md)。
兩份理論報告已由不同工作者相互核對；root checker 另經替代構造工作者唯讀審查。

## 完整證據

| 證據 | 範圍 |
| --- | --- |
| [BASE](BASE.json)／frozen | 五份起始輸入的原 bytes、SHA256、初始 Git 狀態；frozen hashes 未變 |
| [主 checker](controls/checker.py)／[certificate](controls/certificate.json) | 28個構造參數項展開64個完整控制，7,608份 full lifts，16格 pair fibres含空格，原邊、rotation／Kuratowski 證書 |
| [替代 checker](alternatives/check_alternatives.py)／[v2](alternatives/results.v2.json) | 84個案例，其中81完整枚舉、12,650份 full lifts；3份大樹只有公式，明列未枚舉 |
| [初版替代資料](alternatives/results.json) | 保留初版，v2才含显式16格 fibre；不覆寫舊證據 |
| [負控制](controls/corrupt_missing_lift.json)／[結果](logs/negative.json) | 刻意刪除第一份 K₄ 控制的一個完整染色，唯讀重算必須拒絕 |
| [構造圖](controls/constructions.svg)／[繪圖來源](controls/draw.py) | 具名 G₁₀、雙支援 path 與三叉 K₃,₃；繪圖座標不表示圖距離 |

主控制一般圖族大小包含 G₄、G₅、G₆、G₉、G₁₀、G₁₄、G₂₆、G₅₀、G₉₈；
三段以下同色模組；三層面內分支；同支持三角形1至4個 apices；兩種 C₅ 弦序。
最大完整核對強迫距離為33，來自 G₉₈ 的 (v₀,v₉₇)。

C₅ 包裝族 n=6,10,14,26：每個 n 保存十個具名 C₅ 色列，各有72份 full lifts，
所有內點至少四度，ε=7,15,23,47，Σ=1023；刪 bridge 後仍全收。
因此 complete low-excess critical source=`not triggered`，並非來源排除的有限證據。

## 重播與檢查

環境使用現有 `.venv/bin/python`／NetworkX 3.5。主 checker 對至多8點的控制
另以完整 Cartesian product 核對回溯結果。完整 pair fibre 從同一原圖、
同一份 full lift 抽取；沒有獨立正規化零件或拼接不同列。

```bash
.venv/bin/python audits/2026-10-13-forced-inequality-19209f4c/controls/checker.py --check audits/2026-10-13-forced-inequality-19209f4c/controls/certificate.json
PYTHONHASHSEED=17 .venv/bin/python audits/2026-10-13-forced-inequality-19209f4c/controls/checker.py --check audits/2026-10-13-forced-inequality-19209f4c/controls/certificate.json
.venv/bin/python audits/2026-10-13-forced-inequality-19209f4c/alternatives/check_alternatives.py --check audits/2026-10-13-forced-inequality-19209f4c/alternatives/results.v2.json
PYTHONHASHSEED=17 .venv/bin/python audits/2026-10-13-forced-inequality-19209f4c/alternatives/check_alternatives.py --check audits/2026-10-13-forced-inequality-19209f4c/alternatives/results.v2.json
```

以上主／替代正常與 seed17 唯讀重播皆通過。負控制必須失敗，不能當正常
證書載入。生成端使用 exclusive-create；沒有重建舊 catalogue。
文件檢查的實際結果保存於 [檢查紀錄](logs/docs_verification.json)：
`check_docs.py` 通過（641 Markdown、7,987 本地連結），正式 docs DocGraph
通過（62 documents／213 relations），`git diff --check` 通過。
全工作樹 DocGraph 失敗：62項 duplicate-id，來自既存 frozen／scratch
副本；[完整輸出](logs/docgraph_all.log)保留，不刪快照遮掩失敗。
另逐行核對本輪9份新文字／繪圖來源無尾端空白，五份 frozen 輸入漂移為0。
没有修改 Lean 或執行 `lake build`，也沒有聲稱紙面拓撲已形式化。
本輪未 commit／push。

## 信任與後續邊界

`triggered and holds`：具名圖的強迫關係、計數、距離與平面性聲明。
`counterexample`：一般平面圖有統一強迫距離上界、雙支援可任意樹分叉。
`not triggered`：原低超額、Σ-critical C₅ 來源的完整前提。
拓撲報告另述外部4CT的共面推論，明確隔離；本輪主構造與 critical 透明性
均由直接證明，不靠4CT搜尋或判定。

Closure scope：只閉合本文明列圖族及必要限制；F／Z、原域半徑與介面寬度仍OPEN。
Updated：新增權威報告及證據、State 導覽、STATUS 直接索引、母提案的後續連結。
Reviewed-unchanged：HANDOFF／README 的研究線與路由未變；Kempe 的原域F／Z
與E-ARC2聲明未由本輪改變。既有cofacial來源只沿用凍結版本的背景契約。
Propagation stop：L1導覽及母提案的L2後續路由；沒有推升跨線定理或來源 closure。
Remaining OPEN：固定同一 β、非 clique 分隔介面、原實際支援與超額如何共同
限制強迫距離。不能把三角形透明性擴張為所有三點介面透明。
