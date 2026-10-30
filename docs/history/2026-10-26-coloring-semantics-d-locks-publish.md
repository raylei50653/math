# 著色關係核心、六跨邊與 D 鎖定比較整理發布

2026-10-26。從基準 `8d28accea79cf8c6418cdb6da4d94010c1c975bf` 整理本次相連成果。
目前入口為[四色求解導覽](../tools/four_color_guide.md)、[4CT導覽](../research/4ct_guide.md)及
[Lean導覽](../verification/lean_guide.md)。本頁保存成果範圍、本地驗證與來源保管；
提交、push及遠端CI狀態以即時Git／GitHub核對為準。

## 成果與停止裁決

| 工作 | 已完成範圍及證據 | 保留界線 |
| --- | --- | --- |
| 完整解空間與 Lean 核心 | [數學模型](../tools/solver/four_color_mathematical_model.md)與 `Math.ColoringElimination`：完整解與同一接口／完整fibre一一對應，精確bucket投影、共同回寫與有限座標消元；接入預設Math。28份完整執行、21,844份指派符原邊／固定色。 | `reduceAll`是命題值關係語義；未形式化Python、動態選點、資源限制或平面必可染。多步歷史合取及袋樹接合仍為紙證。 |
| 六跨邊必要條件 | [完整分類與雙色鎖定](../archive/reports/planar-sources/four_color_six_edge_cuts.md)：34,969型對全核，1,690不相容分成1,570星形與120矩形；平面最小性迫壓色端點族的固定二／三色方向及同染色連通義務。 | 紙證與有限核對，沒有新增該來源層的Lean。16點真平面負控制證明一份矩形配對不足判無解；SIX-SOURCE與六割排除仍OPEN。 |
| C₆–C₈ D／交換鎖定比較 | [化約與五圖證據](../archive/reports/counting/ck_d_lock_comparison.md)：458份完整接口判定符原邊枚舉；C5重現153 masks，Birkhoff的15個拒絕型經5／2／4／3／1五輪排空。 | 5-5／W₆／W₇／W₈仍餘16／20／70／231型；34份阻擋導出的同色鎖定已包含於D。LOCK-NO-GAIN限定單split交換後果，未排除額外跨split同源定理。 |

C₆–C₈本次條件已化回布林D，新增排除為0，**依使用者指定停止條件結束此路線，不擴大構形枚舉**。
沒有實作或宣稱完成block-count比較；沒有新可約構形、不可避免性或4CT證明，932仍OPEN。

## 原證據與歷史來源保管

三包原始report／verification保持原bytes，原有「未commit／push」欄位保留當輪語境：

- [完整解模型與公理稽核](../../audits/2026-10-26-four-color-mathematical-model-8d28acc/)
- [六跨邊全型對與原圖負控制](../../audits/2026-10-26-four-color-six-edge-cuts-8d28acc/)
- [C₆–C₈完整接口及D閉包](../../audits/2026-10-26-ck-d-lock-comparison-8d28acc/)

模型收據的STATUS與四色導覽綁定較早版本；本次保存逐SHA命中的
[當時STATUS](2026-10-26-coloring-semantics-d-locks-publication/pre-model-docs/STATUS.md.txt)及
[當時四色導覽](2026-10-26-coloring-semantics-d-locks-publication/pre-model-docs/four_color_guide.md.txt)，
沒有將目前文件hash回寫舊收據。Ck收據的STATUS另保存在
[發布前快照](2026-10-26-coloring-semantics-d-locks-publication/pre-publication-docs/STATUS.md.txt)，
以區分本頁新增發布索引前後的來源。
[保管核對程式](2026-10-26-coloring-semantics-d-locks-publication/audit_sources.py)
只允許上述具名文件使用精確歷史副本；可執行來源漂移直接判失敗。

## 本次發布驗證

[工具測試](2026-10-26-coloring-semantics-d-locks-publication/tool-tests.log)共416項通過；
環境為Python3.14.8，`networkx==3.5`、`numpy==2.4.3`、`rustworkx==0.17.1`，
版本及實際命令見[環境紀錄](2026-10-26-coloring-semantics-d-locks-publication/tool-test-environment.json)。
[預設Lean建置](2026-10-26-coloring-semantics-d-locks-publication/lean-build.log)通過8833 jobs；
[九項公理稽核](2026-10-26-coloring-semantics-d-locks-publication/axioms.log)
最多依賴 `propext`、`Quot.sound`，無 `sorryAx`、`native_decide` 或 `Classical.choice`。
既有模組的linter warnings保持原狀，不混稱新形式化範圍。

三包各自一般與seed-17的確定性重播均寫到新目錄，沒有覆寫保存報告。
重播、來源hash、文件、docs-only DocGraph、實際Git index產物政策及空白檢查見
[本次檢查收據](2026-10-26-coloring-semantics-d-locks-publication/checks.json)。
未執行全工作樹DocGraph或RSST原始對偶程式；docs-only通過不代表全域DocGraph通過。

## 收尾與上游

Completed scope是關係核心形式化、必要條件紙證與指定有限新意審計，沒有關閉4CT父題。
L0報告／證據、L1四色與Lean導覽及STATUS已核對；4CT直接父題保留無增益停止裁決。
README／HANDOFF研究線入口及活動標記不變；本次只補歷史索引，不改目前研究排程。
文件傳遞止於直接父題，其他C₅／W7／J1／J2來源義務不受影響。
push後另核本機、tracking及遠端分支SHA與clean狀態；遠端CI與push結果分開回報。
