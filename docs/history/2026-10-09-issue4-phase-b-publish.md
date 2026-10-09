# 2026-10-09：Issue #4 與 Phase B 相連變更發布

使用者明確要求 `commit + push`。基準為
`main @ 3f2731b7225d35e12872177eb00d3a5b24aa6468`；發布前本地 HEAD、
origin/main 與遠端 main 三者相同。本紀錄保存提交前的範圍與本輪預檢，
提交及推送結果以 Git 與本輪交付的 SHA 核對為準。

## 提交範圍

- [Issue #4 試點](2026-10-09-issue4-documentation-pilot.md)：DOCUMENTATION
  的責任分工／L0–L3 契約、weak-deletion 現況整理、STATUS 對應條目與
  [8 個隔離案例](../../artifacts/docs_issue4_pilot/fixtures.json)。
- 接手時已存在的 [Phase B 分析](../c5_phase_b_common_lemmas.md)、
  [小型 checker](../../scripts/c5_phase_b_controls.py)、兩份容量輸入／控制證書，
  以及 README、HANDOFF、STATUS、common-language 與相關 guide 的相連入口。
- 本發布紀錄及 STATUS 的歷史索引。明確列檔 staging，不納入 scratch、
  audits 快照或無關檔案；保留原研究／歷史證據。

沒有新增一般出口、45／54／55 來源排除或 Lean 定理；Phase B 的條件容量
紙面式、restricted Python 控制、source realizability 與操作充分性仍分層。
Issue #4 是文件契約與小幅試點；GitHub Issue 不由本次 push 自動裁決關閉。

## 本輪發布前驗證

| 檢查 | 本輪結果 |
| --- | --- |
| `python3 scripts/c5_phase_b_controls.py --check` | PASS；2 disk 圖、2 非平面容量圖、22＋7＋62 份刪邊與 3 個抽象控制，證書 byte 相同 |
| `PYTHONHASHSEED=17 python3 scripts/c5_phase_b_controls.py --check` | PASS；同一摘要及證書 byte 相同 |
| `lake build` | PASS；8831 jobs，既有 style warnings，不表示新紙面容量式已 Lean 化 |
| `python3 scripts/check_docs.py` | PASS；586 Markdown、6982 local links，anchors／index／HANDOFF 通過 |
| `python3 tools/docgraph --include 'docs/**/*.md' check` | PASS；62 documents、213 relations、5 families，0 errors |
| `git diff --cached --check` | PASS；明確 staging whitelist 為 16 檔，scratch／audits 不在 index |
| 全工作樹 DocGraph | 保留此前已重現的 62 duplicate-ID errors，位於 scratch 副本；正式 docs 通過不改稱全工作樹通過 |
| 試點 fixture 輸入 | 5／5 SHA256 相同，原隔離資料與數學來源未改寫 |

本輪未重跑其餘 Root-budget／W／U4／repair／arity checker、大型枚舉或額外
Lean axiom audits；它們的先前驗證仍以 Phase B 原報告及各原紀錄為準。
沒有推升來源分類、有限 completeness 或拓撲形式化宣稱。
歷史試點中的「未 commit／push」描述其交付截點，保留原語境。
