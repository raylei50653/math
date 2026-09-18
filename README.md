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

2026-09-18 本次整合 R11–R15 五輪成果，研究三-spoke 型：唯一 degree-5
內點 z 接三條 boundary 邊，H−z 為單一二接點分量，其餘內點完整 degree=4。
在 C5 disk、minimal q-obstruction 及接受全部 T4 的前提下，結果如下。

| 分量範圍 | 已完成結果與證書 | 報告 |
| --- | --- | --- |
| 任意連通二接點分量 | 十二種位置縮為兩個鏡像 pentagon；保存非 minimal 的 disk 雙缺失控制 | [區域化約](docs/c5_degree5_sectors.md) |
| 任意樹 | 分枝消去及色序列縮為五型；648 個實際接線全部非 disk | [樹分量](docs/c5_degree5_tree_components.md) |
| 恰一個 triangle，其餘 bridges | 任意接點位置／臂長／外枝排除；528 個必要模板、89,224 個接線全部非 disk | [單 triangle](docs/c5_degree5_triangle_components.md) |
| 恰一個任意 odd-cycle，其餘 bridges | 保留接點縮成 triangle／樹後排除；147 張來源的固定-q 延拓、minimality 及真正 minors 核對通過 | [單長奇環](docs/c5_degree5_odd_cycle_components.md) |
| 恰兩個共用點 triangles，其餘 bridges | 任意接點位置／外枝排除；888 個必要模板、295,920 個接線全部非 disk | [共用點雙 triangle](docs/c5_degree5_shared_triangles.md) |

另以連通外框 K5 minor 排除 z 至少有一條 boundary spoke 時各 degree-4
分量的 K4 block；此項只需 planarity，t=0 未涵蓋。

前輪 R17：[互斥雙環的任意外臂](docs/c5_degree5_bridge_arms.md) 已排除兩側
外臂各在不同於 bridge 端點的環點接入：36,672 模板的 246,645,568 種接線
由 709 份非平面 subdivisions 完整覆蓋；72 張長來源／216 次縮減通過。
承接 [R16 直接私有接點](docs/c5_degree5_bridge_triangles.md) 的同側化約及短子型。
前輪 R18：[同點接入的標記二色介面](docs/c5_degree5_bridge_marks.md) 已核對
完整 root 公式，得到一側同點 858 型／兩側同點 186 型；每型代表的四種
z 色及逐邊刪除 coloring 通過，另核對 12,711 次標記色序列縮減。
前輪 R19：[標記路徑 minor 與同點排除](docs/c5_degree5_bridge_mark_minors.md)
已補完 1,044 型全部 571,400 接線的非 disk 覆蓋，以及 198 張長來源／432 次
真正 minor 縮減。結合 R15–R17，**三-spoke 分量恰含兩個 triangle blocks、
其餘 bridges 的全部接點位置已排除**，不限路徑長度及外枝分叉。
本輪 R20：[長奇環加 triangle 的完整條件 root](docs/c5_degree5_long_triangle_roots.md)
已證同點／不同點的四列介面與保留接點的 triangle 一致；67 個外臂 profiles、
60,300 次耦合查詢及三色 root／雙禁色控制已保存。
下一步是混合來源的真正 boundary 固定 minor 與逐邊刪除著色，尚未記作排除。
上述成果是紙面化約＋Python 有限證書，未新增 Lean theorem；一般 degree-5、
共同出口與 `K∞=K≤5` 仍未證。精確停止點與重播入口見
[HANDOFF](docs/HANDOFF.md)，本輪驗證見 [STATUS §21](docs/STATUS.md)；
本次提交整合 R16–R20，提交核對見同頁 §22，前次發布見 §16。

前輪成果：[唯一 degree-5 的完整接點介面](docs/c5_degree5_interfaces.md)。
保留 degree-4 分量的全部接點關係，得到 minimality 的不可刪減禁色覆蓋條件；
刪去分量任一邊即解除該分量限制，固定來源圖的全部刪邊後代至多需四個二元開關。
32 個既有 disk witnesses 的完整 boundary rows 已核對；一般 degree-5 的
disk／T4 單缺失結論仍未證；三-spoke 分支的最新停止點見上方報告。

前輪成果：[K4 block 排除與全 degree-4 單缺失](docs/c5_k4_blocks.md)。
K4 的四個外接方向必通往 boundary，產生 K5 minor，故全 degree-4 的 planar
minimal q-obstruction 沒有 K4 block。結合 Gallai-tree 化約與既有 odd-cycle
分類，**接受全部 T4 的 C5 disk minimal q-obstruction 若全 degree-4，便只缺 q**。
不限內點數；依賴外部 degree-choosability 定理、紙面論證與 Python 證書，未新增
Lean theorem；後續 degree-5 染色介面見上方新報告。

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
