# 第 1 份回覆整理：本地驗證範圍

2026-10-14。對應 [REPORT](REPORT.md)。以下均是兩張控制圖與本輪文件的驗證；
沒有一般來源排除、外部大型枚舉重播或新增 Lean theorem。

## 有限控制

[原樣保存的正二十面體程式](controls/verify_icosahedron_lock.py)重播通過，
輸出見 [icosahedron.stdout.log](controls/icosahedron.stdout.log)。檢查明列球面嵌入、
全部五度、五連通、具名位置、兩份完整染色及三條長 20 的雙色 Hamilton 環。

[獨立匹配控制](controls/check_matchings.py)以標準函式庫重算
[完整證書](controls/matchings.json)，對回全部列。

| 圖 | 固定三角色框完整染色 | 對偶完美匹配 | 偶環補圖匹配 | 全部不同邊對等價式 |
| --- | ---: | ---: | ---: | ---: |
| 正二十面體／正十二面體 | 10 | 36 | 30 | 435 |
| 五角雙錐 | 5 | 11 | 10 | 105 |

- 兩個 XOR 等價式分別核對 72／144 份合法局部指派。
- 每個偶補匹配均實際構造 Tait 染色，再沿同一原圖積分並核對所有原邊。
- 全列色名商後的 edge-Kempe 類；正二十面體有 10 個 singleton 類，
  每個對應 6 份未商掉色名的 Tait 染色。沒有核對原圖全部 vertex-Kempe 可達類。
- 正二十面體指定原邊 `(2,3)`、`(0,5)`：2 個類鎖定，8 份固定框染色解鎖，
  16 個偶補匹配恰含一條指定邊；原樣保存的 f、g 及 Hamilton 環在證書內逐項核對。
- 五角雙錐指定原邊 `(0,5)`、`(0,6)`：所有完整染色鎖定；兩邊共享 0。
  固定控制中所有全染色鎖定邊對均核對雙環必要條件。
- 刪除一個正二十面體偶補匹配的獨立暫存破損證書，被 `--check` 拒絕，
  exit 1，訊息為 `FAIL: stored certificate differs from complete recomputation`。
  原證書未覆寫；破損檔只置於 `/tmp/c4-tait-matchings-corrupt.json`。

## 本輪重播與文件檢查

以下命令於本輪重新執行：

```bash
python3 -B audits/2026-10-14-c4-tait-lock-review-fdd3e22/controls/verify_icosahedron_lock.py
python3 -B audits/2026-10-14-c4-tait-lock-review-fdd3e22/controls/check_matchings.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-14-c4-tait-lock-review-fdd3e22/controls/check_matchings.py --check
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
python3 tools/docgraph check
lake build --no-ansi
git diff --check
```

- 原樣正二十面體控制及獨立匹配 checker 均 PASS。普通與 seed17 的輸出逐 byte 相同，
  分別保存於 [check.stdout.log](controls/check.stdout.log)、
  [check-seed17.stdout.log](controls/check-seed17.stdout.log)。
- 文件檢查 PASS：683 份 Markdown、8,900 個本地連結，anchors、直接索引、HANDOFF
  及導覽現況卡均通過。此數字是本輪檢查時的工作樹，包含同期已有文件更新。
- 正式 docs DocGraph PASS：97 documents、379 relations、12 families，零 errors／notes。
- 全樹 DocGraph FAIL，exit 1：70 errors，來自保留快照的 duplicate ID；
  [stdout](docgraph-tree.stdout.log)及[完整 stderr](docgraph-tree.stderr.log)均保存。
  正式 docs PASS 不代表全樹 PASS，也沒有刪除歷史快照以隱藏失敗。
- `lake build --no-ansi` PASS，8,832 jobs；既有 `Math.SymRelabel`、
  `Math.AttachmentOrder` linter warnings 沿用。本輪沒有新增 Lean 證明，
  build 通過不能稱上述紙面化約已形式化。
- `git diff --check` PASS。沒有 stage、commit、push 或更新 Lean／mathlib 鎖檔。

未重跑外部≤28點枚舉、既有 JOINT6 全包、同期 C4／C5 遞迴全包或其他不相關研究生成器。

## 整理範圍

新增這包 Tait／匹配整理與控制，更新 C4 權威入口、Kempe 導覽、STATUS
及 no4ct 直接 consumer；同一工作樹其他 audit／最新遞迴更新保留。
HANDOFF 研究線、README 路由與跨線一般界沒有因這份回覆改變。
初次整理時依使用者指示等待第 2 份回覆；兩份到齊後的發布檢查另見
[統一紀錄](../../docs/history/2026-10-14-c4-tait-return-publish.md)。
