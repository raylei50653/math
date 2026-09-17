# math

新對話接手請先讀 [研究交接文件](docs/HANDOFF.md)：目前進展、最新拓撲障礙、信任分類、未完成事項與重現方式。

五邊界染色研究的定義、有限枚舉、反例證書與信任分類見 [第一階段報告](docs/phase1.md)；最新的 triangle grammar 有限狀態模型（ColorDFA／GeometryDFA、Nerode quotient、Z5 profiles）見 [automata.md](docs/automata.md)。

內部五邊形加兩條對角線的 87-state 研究見 [fan_pentagon.md](docs/fan_pentagon.md)；
以完整 boundary relation 為主狀態、派生同一 C5 條件 pair forcing 的庫見
[boundary_relations.md](docs/boundary_relations.md)。

C5 有界代表主命題、最小反例路線與局部壓縮的區分見
[c5_boundary_relations.md](docs/c5_boundary_relations.md)。

Kempe 行為驅動的狀態細化見 [研究提案](docs/c5_behavior_refinement.md) 與
[第一輪結果](docs/c5_behavior_refinement_results.md)。

新增點／邊對完整染色關係、兩點強迫與影響範圍的第一輪觀察見
[extension_effects.md](docs/extension_effects.md)。
固定 C5 disk 三角化母圖的 `k≤3` 單邊刪除實驗、具體碰撞與排除範圍見
[c5_disk_deletions.md](docs/c5_disk_deletions.md)。
A/B 完整刪邊格的 same-Σ closure、共同兩因子判準與 weak bisimulation 有限驗證見
[c5_disk_weak_successors.md](docs/c5_disk_weak_successors.md)。
完整 k≤3 母圖刪邊閉包的 weak-deletion congruence audit（1,246,132 raw states，零碰撞）見
[c5_weak_deletion_audit.md](docs/c5_weak_deletion_audit.md)。
固定 C5 同頂點 completion 的紙面證明、Lean weak-bisimulation／trace bridge，
及全部 k≤3 cells 的條件式覆蓋與外部信任邊界見
[c5_completion_weak_bisimulation.md](docs/c5_completion_weak_bisimulation.md)。
87-state weak quotient 的 inclusion covers／可達 order 反例、完整 mismatch 與 D5 audit 見
[c5_weak_quotient.md](docs/c5_weak_quotient.md)。
相鄰雙 singleton 完全釋放等候選定理、87-state 有限核對與反例控制見
[c5_weak_candidates.md](docs/c5_weak_candidates.md)。
三出口的最小阻礙充要條件與五個代表的兩因子機制見
[c5_weak_critical_cores.md](docs/c5_weak_critical_cores.md)；一般候選仍未證。
其 deletion-side repair／plane-dual flow 化約及平面但非同面控制見
[c5_weak_flow_repairs.md](docs/c5_weak_flow_repairs.md)。
最新的 list-critical core 分類、至多三內點的單側出口條件式結論、
degree-4 Gallai 結構與局部構造探針見
[c5_weak_list_cores.md](docs/c5_weak_list_cores.md)。
四內點核心的完整 list 分型、單側出口障礙的五內點下界，
以及無界 odd-path 最小阻礙家族見
[c5_four_vertex_cores.md](docs/c5_four_vertex_cores.md)。
整個 `K2 ∨ C_(2m+1)` quotient 家族的單缺失分離、有限拓撲 minor 證書與
任意長度的 relation-preserving 路徑縮減見
[c5_odd_join_cores.md](docs/c5_odd_join_cores.md)；一般三出口仍未證。
任意大小的 degree-4 樹核心分離、forcing minor 排除分叉、至多一次 palette 切換，
以及第一個五內點 cyclic quotient 探針見
[c5_tree_cores.md](docs/c5_tree_cores.md)。
單 triangle block 的接枝位置限制、兩尾 disk 存活者與 root-color 介面缺口見
[c5_triangle_branches.md](docs/c5_triangle_branches.md)。
兩點 root／bridge 介面的四點路徑反例，以及 triangle context 的有限篩選見
[c5_root_interfaces.md](docs/c5_root_interfaces.md)。
任意長度的 triangle 路徑枝單缺失化約、160 個拒絕端 subdivision 與分叉停止點見
[c5_triangle_path_reduction.md](docs/c5_triangle_path_reduction.md)。
任意外掛樹的第一個分叉已由 90,112 個 minors 全數排除；單 triangle、全 degree-4
的單缺失推廣與下一個 cycle-5 問題見 [c5_triangle_forks.md](docs/c5_triangle_forks.md)。
Cycle-5 的 67,648 個必要 minors 全非 disk；任意連通單環 degree-4 核心歸到
triangle 的紙面化約、證書與多 block 停止點見 [c5_pentagon_branches.md](docs/c5_pentagon_branches.md)。
恰兩個 triangle blocks 的直接 bridge 六內點正常形、64 個單缺失 lifts 與
16,000 個必要模板見 [c5_two_triangle_blocks.md](docs/c5_two_triangle_blocks.md)。
互斥 triangle blocks 的數目至多二：三環 152,128 個正常形全非 disk，
末端吸收的任意環數推廣見 [c5_three_triangle_blocks.md](docs/c5_three_triangle_blocks.md)。
三環共用 cut vertex 的二色禁集介面、18,688 個必要 minors 與恰三環的完整排除見
[c5_shared_triangle_blocks.md](docs/c5_shared_triangle_blocks.md)；任意多個共用點環仍未解。
四環共用點鏈的禁集 transfer、24,576 個必要 minors 全排除與下一個分叉型問題見
[c5_four_triangle_chain.md](docs/c5_four_triangle_chain.md)。
四環共用點分叉型的 532,608 個必要 minors 全排除，完成四環純共用點連接的
兩種形狀；bridge 混合型停止點見 [c5_four_triangle_star.md](docs/c5_four_triangle_star.md)。
Bridge forcer 替換保留 degree-4 與逐邊 minimality，補齊恰四環全部混合連接型；
任意共用點 cluster 的剩餘缺口見 [c5_shared_pair_bridge.md](docs/c5_shared_pair_bridge.md)。

Lean 4 + mathlib 專案。工具鏈版本由 `lean-toolchain` 鎖定，目前對齊 mathlib `v4.34.0-rc2`。

## 本機需求

- `elan`（已裝在 `~/.elan`；zsh 的 PATH 已寫入 `~/.zshrc`）
- VS Code + [Lean 4](https://marketplace.visualstudio.com/items?itemName=leanprover.lean4) 擴充

新開一個終端機，或先：

```bash
source ~/.zshrc
```

確認：

```bash
lean --version
lake --version
```

## 日常指令

第一次（或更新 mathlib 之後）拉編譯快取，避免從零編 mathlib：

```bash
lake exe cache get
```

編譯這個專案：

```bash
lake build
```

更新 mathlib 與 Lean 版本：

```bash
lake update
lake exe cache get
```

## 檔案

| 路徑 | 用途 |
| --- | --- |
| `Math/Basic.lean` | 起始例子，從這裡改 |
| `Math/ColorDFA.lean`, `Math/GeometryDFA.lean` | triangle grammar 的染色／幾何自動機與 Lean 證明 |
| `scripts/triangle_automata.py`, `artifacts/automata/` | 自動機資料的產生器與決定性輸出 |
| `Math/BoundaryRelations.lean`, `Math/C5PairForcing.lean` | 泛型完整 boundary relation 與同一 C5 的投影／條件強迫 |
| `scripts/c5_relation_library.py`, `artifacts/boundary_relations/` | 87 個完整 states、派生 pair 查詢與最小條件規則 |
| `Math/C5Counts.lean`, `Math/C5ParityWord.lean`, `Math/NearTriangulation.lean` | C5 延伸計數恆等式、XOR 邊字四對一、polygon 補完二分法與 Euler 計數；審計 `Math/C5CountsAudit.lean` |
| `Math/KempeSurgery.lean` | 一次 Kempe swap 的六色對精確更新（AC／BD 不動、混合色對＝retained graph＋stars）與「刪 cut、收縮 components、加邊」的連通分量一一對應；審計 `Math/KempeSurgeryAudit.lean` |
| `Math/ForcingLists.lean` | block 報告反覆使用的 forcing-list 基礎引理：bridge 兩側同色 singleton 強迫、forcer 的 c/D swap 對稱（c-forcer 必碰 c 色 boundary）、incident palettes 互異且恰覆蓋 list、兩色 list 環不可著色 iff 奇環且 lists 全同（含 `C5`、triangle、`P=Q=四色\R` 介面、apex 36-case 規則）；審計 `Math/ForcingListsAudit.lean` |
| `Math.lean` | 函式庫根，`import` 子模組 |
| `lakefile.toml` | 依賴（mathlib）與編譯選項 |
| `lean-toolchain` | 這個專案用的 Lean 版本 |

開 `Math/Basic.lean` 後，右邊 infoview 會顯示目標與型別。把游標放在 `by` 後面即可逐步看 tactic 狀態。

## 授權與引用

本 repository 以 **Apache License 2.0** 釋出，全文見 [`LICENSE`](LICENSE)；授權涵蓋整個 repo：Lean 證明（`Math/`、`Math.lean`）、產生器（`scripts/`）、文件（`docs/`）與決定性輸出（`artifacts/`）。`lakefile.toml` 亦宣告 `license = "Apache-2.0"`、`licenseFiles = ["LICENSE"]`。

引用資訊見 [`CITATION.cff`](CITATION.cff)；GitHub 頁面右上角 "Cite this repository" 會依它產生 APA／BibTeX：

```bibtex
@software{lei_boundary_colouring_math,
  author  = {Lei, Yue-Hui},
  title   = {Lean 4 formalization of boundary-colouring structure and triangle disk-gadget synthesis for the four-colour problem},
  version = {0.1.0},
  year    = {2026},
  url     = {https://github.com/raylei50653/math},
  license = {Apache-2.0}
}
```

## GitHub configuration

To set up your new GitHub repository, follow these steps:

* Under your repository name, click **Settings**.
* In the **Actions** section of the sidebar, click "General".
* Check the box **Allow GitHub Actions to create and approve pull requests**.
* Click the **Pages** section of the settings sidebar.
* In the **Source** dropdown menu, select "GitHub Actions".

After following the steps above, you can remove this section from the README file.
