# 目前進展跨線整合與發布

2026-10-14。依使用者「幫我整理目前進展 commit + push」授權，核對基準
`701590f796521f866fdfa7dfd0e6cb78047c059d`；開始時 main 工作樹乾淨，
本地 HEAD、origin/main 與遠端 main 一致。既有成果已由
`b66f592167bf7c3fab0ed89e57b092e49877be15` 及基準提交發布。
本次補齊跨線摘要與查找入口，沒有新增數學排除、Lean theorem 或枚舉。
實際提交及遠端同步仍以即時 Git 為準。

## 整理成果與保留界線

[跨線總覽的目前進展](../c5_research_synthesis.md#目前進展)集中呈現：

- [C5→C4](../c5_c4_boundary_pivot.md)接外部完整 ≤28 總點計算得
  `K≤22=K≤5=K132`；no4ct 全域最小目錄外來源三支共同 `k≥23`。
- [C4 的 T／T0 化約](../c5_c4_triangle_core.md)及原 `b0,b1,b3` 皆四度時
  R 的完整 C4 關係 mask13；六接點必保同份 full lift，mask13 尚未排除。
- [T1-CROSSCUT](../c5_c8_peeling.md#t1-crosscut)的 `h=3⇒p=0`，第一剝層
  只留 RING；[W5 no4ct 橋](../../audits/2026-10-13-w5-no4ct-bridge-d521163/REPORT.md)
  在全域最少內點、再最多邊的目錄外來源契約下，給任取合法輪的私人圈秩至少五。
- [廣義 N2](../c5_excess_two_n2_bridge.md)只在原 E4 來源契約內收尾；
  E-ARC2 仍留 N1／相鄰 roots，基本 LL-CUT 未獨立證成。
- [具名首層替換](../lean_named_replacement.md)的32個普通 theorem 保完整
  外部接受關係、原 J／指定 P、repair 分類及 r*=4；任意層數與 disk 框仍待形式化。

每項分開紙面、Python 有限控制、外部計算及 Lean；當輪局部 `k≥18／19`
不代替當前共同 `k≥23`。沒有真正目標來源控制不能當作無界來源排除。
一般 T／T0、mask13、RING／h≥4、20項較高度數 C9-932、W5 一般縮減、
E-ARC2、一般出口、多步充分 state 與 `K∞=K≤5` 均保留 OPEN。

## 本次驗證

原 C4／T1 完整研究證書的先前重播見
[三包成果發布](2026-10-14-c4-t1-lean-progress-publish.md)及
[三角化圖發布](2026-10-14-c4-triangle-core-publish.md)，不混稱本次新驗證。

本次實際執行：

```bash
python3 -B audits/2026-10-14-c4-triangle-core-b66f592/controls/check_cap.py --check
python3 scripts/c5_lean_named_replacement.py --check
lake build --no-ansi
lake env lean Math/NamedRepairReplacementAudit.lean
python3 -B scripts/check_docs.py
python3 -B tools/docgraph --include 'docs/**/*.md' check
python3 -B tools/docgraph check
python3 tools/check_generated_artifacts.py
git diff --check
git diff --cached --check
```

- Cap 的四列延拓數 `(2,3,0,1)`、24份有序 pq 指派及 mask13 殘留通過；
  真正目標來源控制仍為0，不外推來源排除。
- 具名替換核對8份實際圖、兩方向與四種首層模式；原 U、有序接點及
  sealed centres 一致。頂點／邊數分別為15／35、23／59、31／83。
- `lake build` 通過8,832 jobs，只有既有 linter warnings；32項具名 theorem
  審計的公理聯集為 `propext`、`Classical.choice`、`Quot.sound`，
  無 `sorryAx`、`Lean.ofReduceBool` 或新增自訂公理。
- 正式 docs DocGraph 通過97份文件、372條關係、12個 families，零 errors／notes。
  全樹 DocGraph exit 1，69項錯誤均為保留的 frozen／scratch 等副本 duplicate IDs；
  完整失敗輸出保留於本地 `/tmp/math-progress-20261014-docgraph-3hfb5y6c/whole-tree.log`，
  未刪證據或把正式 docs PASS 改稱全樹 PASS。
- 文件檢查通過683份 Markdown 的連結、anchors、直接索引、HANDOFF 及
  導覽現況卡；生成物政策通過4,960 indexed files、8份有明列例外的大檔、
  166 registered outputs。工作樹及暫存區 whitespace 檢查均通過。

本次未重跑外部 ≤28 點枚舉、C4 的 quotient／structure 完整控制、T1 安全矩形
生成、W5／N2 舊分類、archive 全量還原或 LC 顯式 build；沿用其已封存證據。
未更新 Lean／mathlib 或依賴鎖檔。

## 文件傳播與發布範圍

Updated：跨線 synthesis 補2026-10-14現況表及權威入口；歷史建議表補
mixed P₃ 與 Lean 首層的後續完成連結；STATUS 更新 synthesis 短索引及
本紀錄的歷史入口。

Reviewed-unchanged：C4／C8／N2／W5 的權威來源、Kempe／兩點重疊／Lean
導覽與 no4ct 交接已一致；README 的研究路由、HANDOFF 的研究線與活躍
tags 無新變化。本次沒有改寫舊 audit、frozen 證書或原發布紀錄。

Propagation stop：只補已採納成果的 L3 跨線摘要；沒有新的 closure，
各題前提與停止點仍由原權威來源及導覽維護。
提交白名單為 synthesis、STATUS 及本紀錄三份文件。
