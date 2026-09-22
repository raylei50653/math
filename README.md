# math

C5 boundary-coloring relation、有限證書與 Lean 形式化研究。
**主命題 `K∞=K≤5` 仍未證。**

## 研究入口

| 文件 | 用途 |
| --- | --- |
| [研究交接](docs/HANDOFF.md) | 當前成果、精確停止點、信任範圍及重播入口；新對話先讀 |
| [文件狀態與變化追蹤](docs/STATUS.md) | 全部專題報告索引、已完成的舊問題，以及值得追蹤的新方向 |
| [研究目標與路線](docs/c5_boundary_relations.md) | 有界代表主命題、最小反例路線、局部壓縮的區別 |
| [歷史交接](docs/HANDOFF_HISTORY.md) | 各輪完整紀錄；其中「下一步／未提交」只描述當時 |

最新：[C5 雙拒絕分類](docs/c5_two_rejection_proof_zh.md)，見 [STATUS §71](docs/STATUS.md#71-c5-雙拒絕分類匯入與獨立核對)。
**在 induced C5 disk、C 非空連通、內點完整 degree≤4、b0 恰有兩個內鄰點下，
拒絕 01212 與 01213 強迫唯一二內點接線，簽章 1855。**
因此五個 sector 目標中的 3647、3895、3901、3903 均排除；3703 仍開放，
為下一個入口。原 331 分支由更一般的 3903 排除涵蓋，603 profiles 未刪除或重算。
紙面證明已逐節核對；獨立 atlas 檢查重現 29,584／2,640／2 主表。
依賴外部 degree-list 定理與紙面拓撲，未新增 Lean theorem；本輪未 commit／push。

保留 R31：[同末端不同二接點正常形拓撲](docs/c5_degree5_same_terminal_triangles.md)
完成 C3–C3–C3 簡單臂的 408 模板、327,968 種接線非 disk 覆蓋；
完整 F={D}、degrees 與 19,020 份刪邊著色通過。
此型任意長來源 boundary 固定 minors 仍待補，暫不作優先入口。
R27 末端各一臂與 R30 中間不同二接點鏈型已排除，**一般三環仍未排除**。
紙面＋Python，未新增 Lean theorem。R24–R31 隨本次提交整合；
發布核對範圍見 [STATUS §37](docs/STATUS.md#37-r24r31-整合提交與發布核對)。

目前主線研究三-spoke 型：唯一 degree-5 內點 z 接三條 boundary 邊，
H−z 為單一二接點分量，其餘內點完整 degree=4；沿用 C5 disk、
minimal q-obstruction、接受全部 T4 與各報告的 forcing-list 前提。

| 範圍 | 目前狀態 | 入口 |
| --- | --- | --- |
| 全 degree-4 | T4 下只缺指定 q；紙面合成與有限證書，未整體 Lean 化 | [K4／degree-4 合成](docs/c5_k4_blocks.md) |
| 三-spoke，零／一／二個 odd-cycle blocks | 任意樹、單環與雙環已排除，含任意環長與既定接點位置 | [單環](docs/c5_degree5_odd_cycle_components.md)、[雙環合成 R24](docs/c5_degree5_shared_cycle_minors.md) |
| 三環共用點鏈，末端各一臂 | 正常形與任意長來源 minors 已完成 | [R25–R27](docs/c5_degree5_three_cycle_minors.md) |
| 三環共用點鏈，兩個不同中間接點 | C3–C5–C3 正常形與任意長來源 minors 已完成 | [R29–R30](docs/c5_degree5_middle_cycle_minors.md) |
| 三環共用點鏈，同末端不同二接點 | R31 正常形完成；任意長來源 minors 是下一個缺口 | [R31](docs/c5_degree5_same_terminal_triangles.md) |
| 其他三環型與一般 degree-5 | 尚未完成；list 介面不等於圖層排除 | [全部接點位置 R28](docs/c5_degree5_three_cycle_positions.md)、[變化追蹤](docs/STATUS.md#4-可能出現新變化的地方) |
| Lean 基礎 | forcing-list 與 15 個接合定理已形式化；不涵蓋整個 minor／disk 論證 | [定理與界線](docs/lean_root_interfaces.md) |

完整報告索引、已被續作解決的舊問題與歷次驗證見 [STATUS](docs/STATUS.md)。
一般 degree≥5、單側／共同出口與 `K∞=K≤5` 仍未證。

| 其他閱讀方向 | 入口 |
| --- | --- |
| 基礎定義與 relation 語意 | [phase 1](docs/phase1.md)、[boundary relations](docs/boundary_relations.md)、[state language](docs/state_language.md) |
| 固定 grammar 與幾何 | [automata](docs/automata.md)、[fan pentagon](docs/fan_pentagon.md)、[topology completeness](docs/topology_completeness.md) |
| 有界 cell 枚舉 | [cell enumerator](docs/c5_cell_enumerator.md) |
| Weak deletion 與目前核心分類路線 | [completion／bisimulation](docs/c5_completion_weak_bisimulation.md)、[候選 A](docs/c5_weak_candidates.md)、[完整進度索引](docs/STATUS.md) |
| Kempe 及 state 充分性 | [behavior 提案](docs/c5_behavior_refinement.md)、[第一輪結果](docs/c5_behavior_refinement_results.md)、[repair 介面碰撞](docs/c5_repair_interface.md) |
| 新增點／邊的影響 | [extension effects](docs/extension_effects.md) |

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
| `Math/RootInterfaces.lean` | 多接點共同關係／禁色、中心 `A \ ⋃ F` 接合、共用 root 交集、單步路徑訊息與 private 色計數；15 個普通 Lean 定理，見 [說明](docs/lean_root_interfaces.md) 及 `Math/RootInterfacesAudit.lean` |
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
