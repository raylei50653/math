# 2026-09-29：No-mixed 十五類整理與共同側跨度

Git 基準 `47ebbbc`。接手時 B–C、B–D、B–E、C–C、C–D、C–E、D–D、
D–E、E–E 的 scripts／artifacts／報告／歷史未追蹤，六份既有文件有修改；
全數保留。使用者要求整理實驗並尋找通用結構，未要求 commit／push。

## 本輪產出

- [統整報告](../c5_no_mixed_span_budget.md)：source 側跨度下界
  A/B/C/D/E=2/2/3/4/3，紙面必要式 m+s+a≤5 統一八類來源排除。
  推得至少一條 root-spoke、兩側無 source 重疊、至多一個飽和二禁色分量。
- [Checker](../../scripts/c5_no_mixed_span_budget.py)與
  [JSON](../../artifacts/c5_no_mixed_span_budget/observations.json)、
  [總表](../../artifacts/c5_no_mixed_span_budget/summary_table.md)：
  原 3,548 IDs 無重複全覆蓋；5,842 份必要支援中 3,760 原 source 排除、
  2,082 保留，4,164 原 target 全接受。原資料與證書未覆寫。
- 獨立 circular interval masks 核對每份支援的兩側跨度；3,624 份的
  框邊飽和分量各重播 bridge 長度 1/3/5，共 10,872 次 K5 controls。
  另 136 份 source 排除仍依賴舊固定框弧規則，未將必要式當充分條件。
- 新 source 排除與新 target 接受皆零。紙面統一論證不等於新增 Lean
  theorem；未使用獨立第二審稿者。

## 實際驗證

下列既有 17 個 checker 全部 `--check` 通過；僅重播本組證據與兩份
共同前提，沒有重開來源圖枚舉。

```bash
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_root_degree_excess.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_path_palettes.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t1_endpoints.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t0_pairs.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t0_overlap.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t0_singles.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_bb.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_bc.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_bd.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_be.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_cc.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_cd.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_ce.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_dd.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_de.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_ee.py --check
```

新增 checker 的預設及 `PYTHONHASHSEED=17` 重播、文件／DocGraph 與
diff 檢查見以下命令。`lake build` 成功（8,827 jobs），只有既有 linter
警告。未新增 Lean theorem，build 不形式化本輪紙面引理。

```bash
python3 scripts/c5_no_mixed_span_budget.py --check
PYTHONHASHSEED=17 python3 scripts/c5_no_mixed_span_budget.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

重新取得並讀取外部 Dvořák Gallai 講義的 Lemma 7／Theorem 10；外部
定理的連通及 degree-assignment 前提未移除。沒有重跑獨立 mixed／唯一
degree-5 全表、interfaces 初層、雙拒絕 atlas、R 系列、profiles／閉包、
舊範圍遍歷的抽象路徑控制或 Lean axiom audit；沒有 Graphify 或 sub-agents。

目前入口更新到 [weak-deletion 導覽](../c5_weak_deletion_guide.md)，
README 增加總覽閱讀入口，STATUS 增加專題及本紀錄直接索引。
HANDOFF 的研究線及進行中標記未變，依文件治理保留其短入口。
一般交換機制、較大／多 mixed、root 樹、一般／共同出口與 K∞=K≤5
仍未證。成果留在工作區，未 commit／push。

## 後續提交與發布核對

使用者隨後明確要求 `commit + push`。本節保存提交前核對；上文的
「未 commit／push」是整理輪結束時的歷史狀態。

提交範圍包含原未追蹤的 B–C、B–D、B–E、C–C、C–D、C–E、D–D、
D–E、E–E 九類 scripts／JSON／生成表／專題／歷史，以及本輪跨度
checker／JSON／總表／報告／歷史與相連的 README、STATUS、研究導覽、
no-mixed／B–B／root 預算／範圍遍歷／出口文件。HANDOFF 的短研究線
入口保持不變；沒有缺少其指向的導覽或證據。

發布前 fetch 確認本機與 `origin/main` 同為基準 `47ebbbc`，無分歧。
重新執行上列十七份原 checker 與新跨度 checker 的 `--check`，全部通過；
新跨度 checker 的 hash-seed 17 重播沿用同一對話整理輪的通過結果。
再次 `lake build` 成功（8,827 jobs；既有 linter 警告），再驗文件連結、
DocGraph、工作區與暫存差異。其他未重跑範圍保持上節所列。

本次提交不增加數學結論。Push 後以 `HEAD`、`origin/main`、
`git ls-remote origin refs/heads/main` 的 SHA 相等及 clean worktree
核對交付；實際提交 SHA 與遠端狀態以 Git 和本次回覆的 readback 為準。
