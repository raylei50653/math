# 研究交接：目前狀態與接手入口

更新：2026-09-17。工作目錄 `/home/ray/math`。
本輪接手基準是本地 HEAD `76e6f44`；開始時工作樹乾淨。
新增任意 triangle tree 的紙面 palette／minor 論證與 Python 控制；未新增
Lean theorem。本輪產物隨本次 commit 保存，未 push；前輪整理基準 `fb6216e` 見 STATUS §5。

先讀本頁，再讀 [文件狀態與變化追蹤](STATUS.md) 及指定報告。
逐輪數字、舊停止點與發布紀錄完整保存在 [歷史交接](HANDOFF_HISTORY.md)。
歷史中的「下一步／未提交」不是目前待辦；提交與遠端狀態須另讀即時 Git 資料。

## 1. 目前做到哪裡

主命題 **`K∞=K≤5` 仍未證**；定義、全域較小代表與局部壓縮的區別見
[C5 boundary relations](c5_boundary_relations.md)。目前活躍的是 weak-deletion
候選 A 的 minimal obstruction 路線：先研究單側出口，再處理共同出口。
這裡的「相鄰雙缺失」與舊 Kempe 路線的「相鄰可實現 singleton」是不同命題。

最新報告是 [任意 triangle tree 的 palette 與共用點排除](c5_triangle_tree_palettes.md)：
在 C5 disk、固定三色 pattern q、所有有效內點完整 degree=4、內部連通、
逐非 boundary 邊 minimal q-obstruction 的前提下，若 blocks 只有 triangles
與 bridges，則 **triangles 必頂點互斥，且總數至多二**。不需 T4，
允許任意外掛樹、bridge 連接樹，原先不限制環數。

相鄰 triangle palettes 必互補。不含 D 的子樹二色禁集可替換成共享點上的
兩條 spokes，保持 boundary 固定的 minor、degree-4、固定 q 及逐邊 minimality。
保留一個不含 D 的中心環及全部鄰環，便縮到已排除的二／三／四環星形。
**沒有證明替換保持完整 Σ；較長 odd-cycle／K4 混合 blocks 仍未處理。**

| 已處理範圍 | 結果與前提 | 報告 |
| --- | --- | --- |
| 至多四個有效內點的 minimal cores | disk 且接受全部 T4 者只缺指定 q；紙面化約＋有限分類 | [小核心](c5_weak_list_cores.md)、[四內點](c5_four_vertex_cores.md) |
| 任意 odd-join 家族、全 degree-4 樹核心 | 各自報告的 disk／T4 假設下，得到單缺失分離；不限制內點數 | [odd-join](c5_odd_join_cores.md)、[樹核心](c5_tree_cores.md) |
| 全 degree-4、連通且只有一個 cycle | 長度至少 5 的唯一 cycle 排除；triangle 加任意外掛樹在 T4 下只缺 q | [單環](c5_pentagon_branches.md)、[triangle 分叉](c5_triangle_forks.md) |
| 恰兩個 triangle blocks，其餘為 bridges | 只剩直接 bridge 的六內點正常形，存活者只缺 q；不需另假設 T4 | [兩環](c5_two_triangle_blocks.md) |
| 所有 triangles 頂點互斥，其餘 blocks 為 bridges | triangle 數至多二，允許任意總環數；不需 T4 | [互斥多環](c5_three_triangle_blocks.md) |
| 恰三／四個 triangle blocks，其餘為 bridges | 全部連接型排除；不需 T4 | [三環](c5_shared_triangle_blocks.md)、[四環](c5_shared_pair_bridge.md) |
| 任意 triangles／bridges block tree | 無非平凡共用點 cluster，triangles 必互斥且至多二；不需 T4 | [任意 triangle tree](c5_triangle_tree_palettes.md) |

以上各 block 結果都是紙面化約配合 Python 有限證書；不能統稱已 Lean 化。
共同 forcing-list 基礎已有 [Math/ForcingLists.lean](../Math/ForcingLists.lean)：
bridge singleton、swap 對稱、palettes 覆蓋、二色 list 環、triangle 與 apex 規則。
其具名定理對照仍見 [歷史交接的 Lean 化紀錄](HANDOFF_HISTORY.md) 與
[Math/ForcingListsAudit.lean](../Math/ForcingListsAudit.lean)。

## 2. 精確停止點與下一個窄問題

**一個長度至少 5 的 odd-cycle block，與 triangles 共用 cut vertices 時的 root 介面。**
先讀 [新 palette／minor 報告 §2–4](c5_triangle_tree_palettes.md)，再讀
[單環排除](c5_pentagon_branches.md)。triangle-tree 分支已完成，不再增加環數。

1. 求 odd-cycle 的 rooted 可取色集合，先檢查 triangle 的七種介面是否仍封閉。
2. 區分一般 list 配置與 minimal obstruction 真正允許的配置，再找必要 minor。
3. 若使用兩-spoke 替換，核對禁集不含 D、對側 root 能取禁集中的每色、
   degree 與 boundary 固定等前提；完整 Σ 不在已證保留範圍。

不直接增加五環 catalog、bridge 路徑長度或外掛樹深度。
R1–R3 已由本輪處理；其他追蹤項目與新 R7 見 [STATUS.md](STATUS.md)。

一般多環中較長 odd-cycle／K4 blocks、degree≥5 內點仍未處理。
triangle-tree 分支完成後，一般單側出口、共同 pivotal edge、候選 A、
一般 weak-deletion congruence 與 `K∞=K≤5` 仍需各自的證明。

## 3. 其他路線的現況

| 路線 | 已完成 | 保留缺口 |
| --- | --- | --- |
| Cell catalogue | k≤5 的 132 個 relations；k=6、7 的獨立搜尋重現未見新 Σ | 有界計算不能推出 K∞；scheduler、planarity 等外部信任仍在。見 [enumerator](c5_cell_enumerator.md) |
| Weak deletion／completion | k≤3 保存母圖後代的 1,246,132 raw states 無同 Σ／不同 W 碰撞；同頂點 completion 為紙面證明；generic bisimulation／finite traces 為條件式 Lean 定理 | 任意 k 的 W 充分性未證；topology 與生成器仍外部。見 [completion](c5_completion_weak_bisimulation.md) |
| Kempe／計數／B₅ | screen、計數與固定圖控制已保存；Kempe surgery 的一般連通重建已 Lean 化 | adjacent-singleton lemma、最終 connectivity／cone obstruction 未證。見 [總覽](c5_boundary_relations.md) |
| 固定圖策略與 repair | survivor-811 閉包與來源 7／17 的介面碰撞已保存 | retained primal／dual 分割的共同安全機制、一般準備與成本保證未證。見 [repair](c5_repair_interface.md) |
| Triangle grammar 與 topology | normal form、GeoReject bridge、endpoint-order 編譯已有 Lean 定理 | embedding → endpoint order 與 topology soundness 未 Lean 化。見 [topology](topology_completeness.md) |
| 狀態／composition 介面 | 完整 relation、共同色框、固定 grammar／separator 的證明與控制已保存 | 沒有一般 future-sufficient 壓縮狀態或跨圖有限 frontier。見 [表示法](state_language.md) |

這些支線保留各自的證據與停止點，不因文件整理而重啟。

## 4. 信任範圍與工作約定

- **Lean 普通證明**：以具名 theorem 及 `#print axioms` 為準；
  **Lean 有限 `native_decide` 證書**另含 native compiler 信任，不能混稱純 kernel reduction。
- **紙面證明／化約**與 **Python 固定域計算／拓撲證書**分開記錄；
  `lake build` 通過不表示新紙面 minor 或 disk 論證已形式化。
- 完整有序 Σ 是關係語意的基線；先共同對齊色框及 boundary，再投影。
  Pair projections、觀察桶或一次 cut 介面不自動是可安全合併的多步 state。
- 區分一般 planar C5 與 C5 是 disk 外邊界；一般 planar BAD 構造不是 disk 反例。
  固定 q 的 minor 不自動保持全部 boundary patterns 或 T4。
- 不以四色定理作搜尋 oracle，不假設待證 boundary-state 命題。
  使用文獻條件的報告須保留其前提與信任標示。
- 接手先讀文件及 `git status`，沿用既有 witnesses／證書；不重跑已完成的大枚舉。
  未獲要求不開 sub-agents、不 commit／push；不刪除研究產物或無關變更。
- 採 document-first。僅使用者 `/graphify`，或文件不足以解釋跨檔關係時才用 Graphify。
- Lean／mathlib 鎖定 `v4.34.0-rc2`；不為接手自動 `lake update`。
  Python 使用報告指定的 `uv run --with ...`；不並行寫同一 `.olean`。

## 5. 重播入口與本次核對

最新研究的最小入口（完整六份依賴重播見 [報告 §5](c5_triangle_tree_palettes.md)）：

```bash
uv run --with networkx==3.5 python scripts/c5_triangle_tree_palettes.py --check
lake build
lake env lean Math/ForcingListsAudit.lean
git diff --check
```

本輪研究的實際驗證範圍與結果見 [STATUS.md](STATUS.md) 末節。
查舊實驗時讀對應報告；歷史生成器可能覆寫 artifacts，勿把重建指令當只讀 checker。
