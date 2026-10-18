# 四列保壞接口與較小原圖候選發布

2026-10-18；研究及提交父 BASE `9f1fe84f73aabfa87a33d28754633bae6bf0b707`。
使用者授權 `commit + push`。本次交付相連的兩輪研究 audit、Kempe 導覽、
STATUS、本發布紀錄及一項精確產物例外。原報告「未 commit／push」及研究輪
未跑 Lean 的收據保留當輪語境；發布輪檢查另記於此，實際發布狀態以 Git 為準。

## 交付範圍

[抽象與瓶頸審核](../../audits/2026-10-18-abstraction-bottleneck-9f1fe84/REPORT.md)
供應三支共同的最少四列證書：同一合法 disk 接受01232，拒絕01021／01202／01212，
即可排出 K132；另六列及 r6 身份不必保持。任意邊界回應支配、標記秩及整區
參考交換的限制分別保留其前提，未宣稱改善存在性。

[原圖候選構造](../../audits/2026-10-18-smaller-source-9f1fe84/REPORT.md)
在四個具名原兩星位置直接產生兩個完成 k−2 的合法 disk。每份原接受完整
著色恰落入一個分支；固定全部外側回填當且僅當四接點非 rainbow。固定六圈
零／一內點的 1193 圖無通用支持包含替換；實際來源的完整外側仍須接入。

**尚未排除同一接受候選的三個完整 rainbow fibres，故未構造較小 bad 來源。**
所有來源必有該位置、完整319、`W110+W101>0`、`omega_e=0` 及一般閉合仍 OPEN。
普通完美匹配非空不提升為偶補正值；本次沒有新增 Lean theorem。

## 封存與產物政策

兩 audit 分別 42、64 份檔案，共 106 份，約 4.48 MB；發布不改任何 audit bytes。
各自的 INPUTS／OUTPUTS 雜湊與完整重播保留，後輪另精確區分 BASE 輸入與前輪
未提交成果。研究控制中的完整 fibres、空 fibres、負控制與交叉審核皆一併交付。

唯一超過 1 MB 的新 JSON 為
`audits/2026-10-18-smaller-source-9f1fe84/A/hexagon_obstruction.json`，
1,814,650 bytes，SHA256
`f2cad7410cc0a7a444838613847c839bd631f12d92bfedbccf235823bb2a226d`。
在 [產物例外](../../tools/generated_artifact_exceptions.json)登記此精確路徑的
`frozen` 例外，理由為保留已封存的完整有限證書與唯讀重播；沒有放寬一般政策。

## 發布驗證

本發布輪已重跑兩 audit 根 checker：封存／BASE custody、完整平面控制與
全部十列 fibres、兩 fan 的完整著色分割及污染證書拒絕均通過。
正常／seed17 一致性沿用未改 bytes 的研究輪收據，未額外重跑 seed17：
[前輪收據](../../audits/2026-10-18-abstraction-bottleneck-9f1fe84/checks.json)、
[後輪收據](../../audits/2026-10-18-smaller-source-9f1fe84/checks.json)。
本輪 `lake build` 通過既有 8832 jobs，保留既有 linter 警告；94 項工具測試通過。
這不把本輪紙證／Python 結果升為 Lean 形式化。

```bash
python3 -B audits/2026-10-18-abstraction-bottleneck-9f1fe84/check.py
python3 -B audits/2026-10-18-smaller-source-9f1fe84/check.py
lake build
uv run --with-requirements requirements.txt python -m unittest discover -s tools/tests -p 'test_*.py'
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
python3 tools/check_generated_artifacts.py
git diff --cached --check
```

正式文件檢查通過（697 Markdown、9169 本地連結）；formal DocGraph 通過
（97 documents、383 relations）。Git index 產物政策通過（6310 generated files、
83 項精確大型例外、166 registered outputs），staged whitespace 亦通過。
whole-tree DocGraph 不重跑：研究輪已記錄歷史／凍結副本重複 ID，包含本輪
凍結副本；正式 docs scope 與全樹結果分開，不以修改封存原件消除此類錯誤。

Updated：兩輪研究證據、Kempe 導覽、STATUS 研究及歷史入口、精確產物例外、
本發布紀錄。Reviewed-unchanged：README／HANDOFF 的研究線與 tag、全部封存
研究 bytes、一般界及父題 OPEN。Propagation stop：L1，沒有父題 closure。
