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
| [單側出口接合](docs/c5_single_sided_exit.md) | 涵蓋唯一 degree-5 全部核心、相鄰雙 root 唯一 mixed singleton 全支援及共鄰端點 K2 的 w 側兩條 spoke；一般核心分離仍未證 |
| [相鄰雙 degree-5 介面](docs/c5_adjacent_degree5_interfaces.md) | 保留共鄰點與共同色框的有序色對接合、root-edge 對角強迫、逐類 minimality 與固定來源刪邊公式；紙面＋有限控制，雙 root 分離仍保留 |
| [相鄰雙 root 的唯一 mixed K2](docs/c5_adjacent_degree5_mixed_edge.md)、[原四環次序排除](docs/c5_adjacent_degree5_mixed_edge_order.md)、[共鄰端點化約](docs/c5_adjacent_degree5_mixed_edge_shared.md) 與 [w 側兩條 spoke](docs/c5_adjacent_degree5_mixed_edge_shared_t2.md) | 各一接點型已作 disk 來源排除；共鄰端點型的 t_w=2、(1) 已完成支援／環序與雙列分離，不需 T4，接入出口第八類；其餘 w 分拆保留，必要表未證實現性，未 Lean 化 |
| [相鄰雙 root 的唯一共鄰單點](docs/c5_adjacent_degree5_shared_singleton.md)、[同側限制](docs/c5_adjacent_degree5_singleton_sectors.md)、[01／23](docs/c5_adjacent_degree5_singleton_long_arc.md)、[12 分離](docs/c5_adjacent_degree5_singleton_middle_arc.md) 與 [34／40 排除](docs/c5_adjacent_degree5_singleton_end_arc.md) | 唯一 mixed 共鄰 singleton 的全部支援已接回條件式出口；一般雙 root 仍保留，紙面＋外部定理＋Python，未 Lean 化或證必要表可實現性 |
| [Single-spoke 核心](docs/c5_single_spoke_cores.md) | 四型必要覆蓋、實際支援和接點環序；[外部雙路徑 completion](docs/c5_single_spoke_completion.md) 推進指定 p 分離；[bridge 路徑化約](docs/c5_single_spoke_bridge_path.md) 與[旁支 palette 守恆](docs/c5_single_spoke_branch_palettes.md) 接上[同圖 K5 minor](docs/c5_single_spoke_branch_minor.md)，完成指定 p₁ 分離；[單接點未用色守恆](docs/c5_single_spoke_root_conservation.md) 完成下一指定 p₂ 分離並[掃過全表](docs/c5_single_spoke_root_sweep.md)；[剩餘二接點上界分類](docs/c5_single_spoke_two_contact_bounds.md) 給共同 palette／K5 論證與完整關係重播；[單接點上界分類](docs/c5_single_spoke_single_contact_bounds.md) 完成 114 筆指定雙列延拓；[(2,2) 必要分類](docs/c5_single_spoke_two_two.md) 保存完整關係、實際支援與接點次序，區分禁色上界與可實現性 |
| [非相鄰 two-spoke 分離](docs/c5_two_spoke_nonadjacent.md) | 四代表的指定 p 延拓、反射搬運與 t=2 出口整合；任意大小紙面化約、局部證書及 Lean 列代數 |
| [兩-spoke 區域](docs/c5_degree5_two_spoke_sectors.md)、[三接點排除](docs/c5_two_spoke_three_contacts.md)、[相鄰 (2,1) 排除](docs/c5_two_spoke_adjacent_21.md)、[中間相鄰 (2,1) 排除](docs/c5_two_spoke_middle_21.md)、[反射與下一相鄰 orbit](docs/c5_two_spoke_reflection.md)、[split-support 全列分類](docs/c5_two_spoke_split_support.md)、[未接內點引理](docs/c5_unattached_boundary.md) | degree-5 兩-spoke 必要配置、全部 (3) 型及 S={b0,b1}、S={b1,b2}、S={b2,b3} 各兩種 (2,1) 次序的同圖 K5 排除；Lean 反射搬運；紙面 minor／split-support 全列單缺失定理、Python 完整接點證書與 Lean 列代數 |
| [3703 排除證明](docs/c5_sector_3703_exclusion.md) | 指定 sector 圖類的最後一個目標；紙面證明、局部證書與適用界線 |
| [研究目標與路線](docs/c5_boundary_relations.md) | 有界代表主命題、最小反例路線、局部壓縮的區別 |
| [(2,2) frame-arc K5](docs/c5_single_spoke_frame_arc.md) | [路徑塊支援守恆](docs/c5_single_spoke_two_two_minor.md) 與[外部路徑接合](docs/c5_single_spoke_two_two_external.md) 推廣至非相鄰支援點；區分 q 下來源排除與 target 拒絕反證，含 record 15 的 p₂ 延拓；任意大小紙面證明與局部／minor 證書，未 Lean 化 |
| [(2,2) 跨列 residual 相容性](docs/c5_single_spoke_cross_row.md) | 同一分量、同一原路徑塊的雙列 palettes 隨 boundary 色置換搬運；證 record 16 的 p₁ 並更新完整拒絕候選表；保留 singleton 與無對齊置換的適用界線，未 Lean 化 |
| [(2,2) 兩框弧 K5](docs/c5_single_spoke_two_arc.md) | 另一原分量納入 Z，每塊跨同一份連通兩弧分割；證 record 17 的雙列，來源排除與指定列延拓分開套表；保留支援選言與量詞順序，未 Lean 化 |
| [(2,2) singleton-source 首橋相容性](docs/c5_single_spoke_first_bridge.md) | target pair 的原路徑上，以 source singleton 證書同一首橋 palette 綁定兩端實際支援；record 87 延拓與剩餘表更新，局部 residual 與整分量禁色分開，未 Lean 化 |
| [(2,2) 局部 residual](docs/c5_single_spoke_residual_locality.md) | 同一路徑塊的相同 boundary 列迫使相同 residual；完成 record 90／282 及全部保留型的指定雙列分離，接回條件式單側出口；未 Lean 化 |
| [(3,1) 三接點排除](docs/c5_single_spoke_three_one.md) | 兩份拒絕 palettes 強迫 triangle 加三臂；實際 boundary tethers 與唯一 spoke 給原圖 K5，不需 T4，未 Lean 化 |
| [(4) 三拒絕共同結構](docs/c5_single_spoke_four.md) | 同一 block tree 的三組差異共用係數，強迫兩 triangle 加單 bridge；原 tethers 給 K5，完成 t=1 接合，不需 T4，未 Lean 化 |
| [No-spoke 環狀支援與 (2,1,1,1) 分離](docs/c5_no_spoke_supports.md) | 環狀實際支援及原分量外部雙路徑；48 筆全部指定雙列延拓，(2,2,1) 的必要表由後續路徑 K5 收窄；未 Lean 化 |
| [No-spoke (2,2,1) 首橋與固定框弧](docs/c5_no_spoke_first_bridge.md) | 同一首橋 palette 與原外部路徑、容許不同供應點的固定框弧 K5，完成 116 筆指定雙列及唯一 degree-5 條件式出口；未 Lean 化 |
| [No-spoke (2,2,1) 原外部路徑 K5](docs/c5_no_spoke_path_minor.md) | 逐塊 residual 支援、同圖外部路徑與跨列相容性；排除 record 599，區分來源排除與指定列延拓，未 Lean 化 |
| [No-spoke 外部連通與四型排除](docs/c5_no_spoke_exterior.md) | 另一原分量提供實際 z–B 路徑，恢復 K4／triangle 的外部 hub；(5) 另由四列偶數接點排除，t=0 只剩 (2,2,1)、(2,1,1,1)，未 Lean 化 |
| [邊位置對座標](docs/c5_edge_pair_coordinates.md)、[同染色有序重接](docs/c5_dual_path_surgery.md) | 十態與 Kempe 必要條件；三份邊界配對不足的同圖反例與一步精確重接；record 110 已由來源 K5 排除，有限可迭代 state 仍未證 |
| [循環流與計數限制](docs/c5_circulation.md) | 六維計數、153 個 Kempe 支撐與十二循環的統一表示；三套整數 orbit 分解不再收緊非負整數恆等式解，平面來源仍需額外證明 |
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
| `Math/BoundaryDegree.lean` | 實際邊界接線到 degree-list 緊性、框色單射及延拓準則；[前提與重播](docs/lean_boundary_degree.md)，審計 `Math/BoundaryDegreeAudit.lean` |
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
