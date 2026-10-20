# 5／5／5 十圈修復：驗證紀錄

2026-10-20；BASE `9c36e3c4789dfec07d60ec4e042f0bafe17451d1`。
命題與精確條件見 [PROOF](PROOF.md)，固定控制見 [C](C/REPORT.md)。

## 紙面與固定域

- A、B 分別推導任意大小的四點交換，彼此交叉審查 PASS；C 獨立審查亦 PASS。
- 原十面順序及所有 12 個涉及面均逐項合法；三標記逐一保持。
- 全部新完整 primal 分量恰三個，原度和皆偶；全部補圈恰長 4、|O|+3。
- C 不匯入前輪 checker，重建 56 匹配、4096 cut、78 配對、八完整標記 fibres
  及八全偶標記 fibres；完整圈與分量保留在同一 row。
- C 的普通／seed17 stdout 相同、重播前後 checker／certificate SHA 不變。
- C 的 11 個污染／覆寫控制全部拒絕，見 [VERIFICATION.json](C/VERIFICATION.json)。
- 整合 checker 另拒絕改寫來源覆蓋範圍的 authority manifest。

## 本輪執行

下列命令皆由 repo root 執行；stdout、stderr 和 returncode 保留於 `logs/`。

| 命令 | 結果與範圍 |
| --- | --- |
| `python3 -B audits/2026-10-20-r6-555-odd-branches-9c36e3c/check.py` | PASS；81 frozen inputs、immutable drift 0；路由只允許已列檔案漂移 |
| `PYTHONHASHSEED=17 python3 -B audits/2026-10-20-r6-555-odd-branches-9c36e3c/check.py` | PASS；整合 stdout 與普通重播相同 |
| `python3 -B scripts/check_docs.py` | PASS；702 Markdown、9247 local links，含 index／HANDOFF／guide progress |
| `python3 -B tools/docgraph --include 'docs/**/*.md' check` | PASS；97 documents、383 relations、12 families、0 errors |
| `python3 -B tools/check_generated_artifacts.py` | PASS；既有生成物政策 |
| `lake build` | PASS；8832 jobs，既有 linter warnings，無新 Lean 命題 |
| `git diff --check` | PASS；另外核對本輪未追蹤文字檔的空白及 audit 相對連結 |

[整合 checks](checks.json)記錄各命令，
[local verification](local-verification.json)記錄 audit 內連結與額外污染檢查。
[OUTPUTS.sha256](OUTPUTS.sha256)封存本輪紙證、程式及證書的雜湊。

INPUTS 的 79 個原工作樹輸入加補充 2 個原中心／分量來源，全部 bytes 維持。
前輪證據是原工作樹內容，不誤稱已在 Git BASE 內。
凍結路由與當前兩圈路由的差異已授權且逐項列出；不改寫舊 audit。
未跑 whole-worktree DocGraph，亦未重跑與本命題無關的全部舊 audit 或枚舉。
本輪沒有更改 Lean 或來源四色／U319 fibre 程式。

## 證據層與收尾

任意大小結論由紙證成立；固定 Python 證書只校準交換機制。
控制圖的原來源實現為 `not triggered`。
本條件 5／5／5 型（包括同樹兩奇支）已完成；
來源度數型覆蓋、其他度數型及一般兩圈修復仍 OPEN。
無新 Lean theorem、無外部四色可染色性調用。
