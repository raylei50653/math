# math

C5 boundary-coloring relation、有限證書與 Lean 形式化研究。
**主命題 `K∞=K≤5` 仍未證。**

## 研究入口

| 文件 | 用途 |
| --- | --- |
| [研究交接](docs/HANDOFF.md) | 當前成果、精確停止點、信任範圍及重播入口；新對話先讀 |
| [文件狀態與變化追蹤](docs/STATUS.md) | 專題報告索引、研究狀態與證據入口 |
| [全 degree-4／block 導讀](docs/c5_degree4_guide.md) | 小核心至 K4 的合成依賴、單缺失結論、介面限制與證書入口 |
| [degree-5／R 系列導讀](docs/c5_degree5_guide.md) | R9–R31 依賴順序、排除範圍、R31 保留缺口與證書入口 |
| [3903 系列導讀](docs/c5_sector_3903_guide.md) | 系列結論、推導順序、適用範圍與證書入口 |
| [單側出口接合](docs/c5_single_sided_exit.md) | 五目標及唯一 degree-5 全部 two-spoke 核心到條件式出口的橋接，以及一般版尚缺的核心分離 |
| [非相鄰 two-spoke 分離](docs/c5_two_spoke_nonadjacent.md) | 四代表的指定 p 延拓、反射搬運與 t=2 出口整合；任意大小紙面化約、局部證書及 Lean 列代數 |
| [兩-spoke 區域](docs/c5_degree5_two_spoke_sectors.md)、[三接點排除](docs/c5_two_spoke_three_contacts.md)、[相鄰 (2,1) 排除](docs/c5_two_spoke_adjacent_21.md)、[中間相鄰 (2,1) 排除](docs/c5_two_spoke_middle_21.md)、[反射與下一相鄰 orbit](docs/c5_two_spoke_reflection.md)、[split-support 全列分類](docs/c5_two_spoke_split_support.md)、[未接內點引理](docs/c5_unattached_boundary.md) | degree-5 兩-spoke 必要配置、全部 (3) 型及 S={b0,b1}、S={b1,b2}、S={b2,b3} 各兩種 (2,1) 次序的同圖 K5 排除；Lean 反射搬運；紙面 minor／split-support 全列單缺失定理、Python 完整接點證書與 Lean 列代數 |
| [3703 排除證明](docs/c5_sector_3703_exclusion.md) | 指定 sector 圖類的最後一個目標；紙面證明、局部證書與適用界線 |
| [研究目標與路線](docs/c5_boundary_relations.md) | 有界代表主命題、最小反例路線、局部壓縮的區別 |
| [歷史交接](docs/HANDOFF_HISTORY.md) | 早期交接快照；近期紀錄由 STATUS 的歷史入口查閱 |

研究優先順序與最小重播命令只在 [HANDOFF](docs/HANDOFF.md) 維護。
各結論的適用範圍、證據層級及保留缺口見 [STATUS](docs/STATUS.md)。
文件更新方式與檢查命令見 [文件維護規則](docs/DOCUMENTATION.md)。

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

只有刻意升級依賴時才執行以下指令；一般接手沿用 `lean-toolchain` 與
`lake-manifest.json` 的鎖定版本：

```bash
lake update
lake exe cache get
```

## 檔案

| 路徑 | 用途 |
| --- | --- |
| `Math/Basic.lean` | Lean 起始例子；研究入口見 HANDOFF |
| `Math/ColorDFA.lean`, `Math/GeometryDFA.lean` | triangle grammar 的染色／幾何自動機與 Lean 證明 |
| `scripts/triangle_automata.py`, `artifacts/automata/` | 自動機資料的產生器與決定性輸出 |
| `Math/BoundaryRelations.lean`, `Math/C5PairForcing.lean` | 泛型完整 boundary relation 與同一 C5 的投影／條件強迫 |
| `scripts/c5_relation_library.py`, `artifacts/boundary_relations/` | 87 個完整 states、派生 pair 查詢與最小條件規則 |
| `Math/C5Counts.lean`, `Math/C5ParityWord.lean`, `Math/NearTriangulation.lean` | C5 延伸計數恆等式、XOR 邊字四對一、polygon 補完二分法與 Euler 計數；審計 `Math/C5CountsAudit.lean` |
| `Math/KempeSurgery.lean` | 一次 Kempe swap 的六色對精確更新（AC／BD 不動、混合色對＝retained graph＋stars）與「刪 cut、收縮 components、加邊」的連通分量一一對應；審計 `Math/KempeSurgeryAudit.lean` |
| `Math/ForcingLists.lean` | block 報告反覆使用的 forcing-list 基礎引理：bridge 兩側同色 singleton 強迫、forcer 的 c/D swap 對稱（c-forcer 必碰 c 色 boundary）、incident palettes 互異且恰覆蓋 list、兩色 list 環不可著色 iff 奇環且 lists 全同（含 `C5`、triangle、`P=Q=四色\R` 介面、apex 36-case 規則）；審計 `Math/ForcingListsAudit.lean` |
| `Math/RootInterfaces.lean` | 多接點共同關係／禁色、中心 `A \ ⋃ F` 接合、共用 root 交集、單步路徑訊息與 private 色計數；15 個普通 Lean 定理，見 [說明](docs/lean_root_interfaces.md) 及 `Math/RootInterfacesAudit.lean` |
| `Math/TwoRejectionTools.lean` | 雙拒絕證明的九個一般引理；[依賴與重播](docs/lean_two_rejection_tools.md)，審計 `Math/TwoRejectionToolsAudit.lean`；完整 disk 分類仍未形式化 |
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
