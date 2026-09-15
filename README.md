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
