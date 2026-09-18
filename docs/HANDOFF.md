# 研究交接：目前狀態與接手入口

更新：2026-09-18。工作目錄 `/home/ray/math`。
本次提交整合基準 `be97121` 之後的 R11–R15 五輪成果：三-spoke 區域化約，
以及樹、單 triangle、單長奇環、共用點雙 triangles 的二接點分量排除。
各排除涵蓋報告所列的任意接點位置及外枝；成果為紙面化約與 Python 證書，
未新增 Lean theorem。發布前核對見 STATUS §16，各輪研究紀錄保留於 §11–15。

先讀本頁，再讀 [文件狀態與變化追蹤](STATUS.md) 及指定報告。
逐輪數字、舊停止點與發布紀錄完整保存在 [歷史交接](HANDOFF_HISTORY.md)。
歷史中的「下一步／未提交」不是目前待辦；提交與遠端狀態須另讀即時 Git 資料。

## 1. 目前做到哪裡

主命題 **`K∞=K≤5` 仍未證**；定義、全域較小代表與局部壓縮的區別見
[C5 boundary relations](c5_boundary_relations.md)。目前活躍的是 weak-deletion
候選 A 的 minimal obstruction 路線：先研究單側出口，再處理共同出口。
這裡的「相鄰雙缺失」與舊 Kempe 路線的「相鄰可實現 singleton」是不同命題。

最新報告是 [共用點雙 triangle 二接點排除](c5_degree5_shared_triangles.md)：
互補 palettes 的共同 root 接合，將同環不同點、分處兩環及同點會合三型
化為 888 個必要模板，295,920 個實際接線全部非 disk。保留全部 fixed-q
z 色、degrees 及 minimality；58 張長來源共 116 次縮減，另有五張整個
cluster 位於旁支的來源 minor。下一題是兩個互斥 triangles 的 bridge 路徑。

前輪 [單長奇環二接點排除](c5_degree5_odd_cycle_components.md)：
拒絕 D 強迫環上共同二色 palette，保留接點縮為 triangle 後，四種 z 色的
延拓性、degrees 及 minimality 保持；共同接點另保留完整 root 色集。
旁支型化回樹。147 張具名來源的 minor、逐邊刪除 coloring 與來源非平面
證書通過。故 C 至少含兩個 odd-cycle blocks；共用點雙 triangles 由本輪處理。
這不保持任意二元接點關係或完整 Σ；已保存具體的二元關係反向控制。

前輪 [單 triangle 二接點排除](c5_degree5_triangle_components.md)：
按兩接點到 triangle 的位置分成旁支、共同接點、不同接點三型。
旁支化回樹；共同接點化成五種帶標記閉色序列；不同接點的兩臂各縮成
簡單色序列。528 個必要模板、89,224 個實際接線全部非 disk。
故 C 不能恰含一個 triangle、其餘為 bridges，不限路徑長度或外枝分叉。
單長 odd-cycle 已由後續排除；雙 triangle 的共用點分支亦已完成。

前輪 [任意樹分量排除](c5_degree5_tree_components.md)：任意樹經分枝消去及
閉色序列縮減，化為五型；648 個必要 lifts 全部非 disk。另以連通外框
K5 minor 排除 t≥1 時各 degree-4 分量的 K4 block；t=0 未涵蓋。

前輪 [三-spoke 區域化約](c5_degree5_sectors.md)：連通二接點分量只能
位於同一 spoke 區域；禁色交換排除八種位置，T4 改色排除兩種，只剩兩個
鏡像 pentagon。精確接合公式已核對，但 proper-C5 relation 漏掉 z 與區域
端點同色的刪-spoke 測試。另保存一張 disk／degree／相鄰雙缺失皆符合、
卻因 F_C(q)={C,D} 而不 minimal 的控制；不能視為目標反例。

前輪 [唯一 degree-5 完整接點介面](c5_degree5_interfaces.md)：
分量所有接點的共同關係給出精確禁色；刪除任一碰到 degree-4 分量的邊，
對所有 boundary rows 都解除該分量限制。minimality 等價於 z 可用色的
不可刪減覆蓋，至少一個分量必有多接點。固定來源圖的全部刪邊後代至多需
四個二元開關；這不是跨圖 state 或小型 disk 代表定理。
32 個既有 witnesses 的 7,680 個完整 boundary rows 通過核對；一般 degree-5
disk／T4 單缺失排除仍未證，尚未新增 Lean theorem。

前輪 [K4 block 排除與全 degree-4 單缺失](c5_k4_blocks.md)：
K4 四個外接方向都必經 spoke 或 forcing bridge 到達 boundary，因此產生
K5 minor；此排除只需一般 planarity，不需 T4，外側可含任意 blocks。

結合 degree-choosability 的 Gallai-tree 化約、既有多長環排除及零／一／二
triangle 分類，現在得到：**接受全部 T4 的 C5 disk minimal q-obstruction，
若所有有效內點完整 degree=4，則 `Σ(G)=Ω\{q}`。** 不限內點數。
這是紙面合成與有限證書，包含外部 degree-choosability 定理，尚未 Lean 化。
故某個單側出口若失敗，對側每個 minimal obstruction 都必有 degree≥5 內點；
一般共同出口仍需獨立證明。

| 已處理範圍 | 結果與前提 | 報告 |
| --- | --- | --- |
| 至多四個有效內點的 minimal cores | disk 且接受全部 T4 者只缺指定 q；紙面化約＋有限分類 | [小核心](c5_weak_list_cores.md)、[四內點](c5_four_vertex_cores.md) |
| 任意 odd-join 家族、全 degree-4 樹核心 | 各自報告的 disk／T4 假設下，得到單缺失分離；不限制內點數 | [odd-join](c5_odd_join_cores.md)、[樹核心](c5_tree_cores.md) |
| 全 degree-4、連通且只有一個 cycle | 長度至少 5 的唯一 cycle 排除；triangle 加任意外掛樹在 T4 下只缺 q | [單環](c5_pentagon_branches.md)、[triangle 分叉](c5_triangle_forks.md) |
| 恰兩個 triangle blocks，其餘為 bridges | 只剩直接 bridge 的六內點正常形，存活者只缺 q；不需另假設 T4 | [兩環](c5_two_triangle_blocks.md) |
| 所有 triangles 頂點互斥，其餘 blocks 為 bridges | triangle 數至多二，允許任意總環數；不需 T4 | [互斥多環](c5_three_triangle_blocks.md) |
| 恰三／四個 triangle blocks，其餘為 bridges | 全部連接型排除；不需 T4 | [三環](c5_shared_triangle_blocks.md)、[四環](c5_shared_pair_bridge.md) |
| 任意 triangles／bridges block tree | 無非平凡共用點 cluster，triangles 必互斥且至多二；不需 T4 | [任意 triangle tree](c5_triangle_tree_palettes.md) |
| 恰一個長 odd-cycle，其餘 triangles／bridges | 全部排除，不需 T4；一般 root 有十一種介面，obstruction 仍用互補 pairs | [長環 root](c5_odd_cycle_roots.md) |
| 任意 odd cycles／bridges block tree | 沒有長環；triangles 互斥且至多二，不需 T4；任意深度遞迴與連續縮減 | [多長環](c5_multi_odd_cycles.md) |
| K4 block 加任意 bridge 外側 | K5 minor 排除；全 degree-4、planar、minimal q，不需 T4 | [K4／bridge](c5_k4_blocks.md) |
| 全 degree-4 的 minimal q-obstruction | disk 且接受全部 T4 時只缺 q；Gallai-tree 與全部 block 結果的紙面合成 | [degree-4 合成](c5_k4_blocks.md) |
| 唯一 degree-5，其餘 degree-4 | 完整接點關係、禁色覆蓋的 minimality 充要條件、至多四開關的固定來源圖刪邊公式；disk／T4 排除未完成 | [degree-5 介面](c5_degree5_interfaces.md) |
| 唯一 degree-5、三條 z-spokes、單一二接點分量 | 任意大小化約到兩個鏡像 pentagon 區域；剩餘四色延拓／minimality 問題未解 | [三-spoke 區域](c5_degree5_sectors.md) |
| 唯一 degree-5、至少一條 z-spoke | 各 degree-4 分量不含 K4 block；連通外框 K5 minor，只需 planarity | [連通外框](c5_degree5_tree_components.md) |
| 唯一 degree-5、三條 z-spokes、H−z 是樹 | 接受全部 T4 的 disk minimal q-obstruction 不存在；允許任意兩接點位置及分叉 | [任意樹排除](c5_degree5_tree_components.md) |
| 唯一 degree-5、三條 z-spokes、H−z 恰含一個 triangle，其餘 bridges | 任意接點位置及外枝均排除；528 個必要模板／89,224 接線非 disk，紙面＋證書 | [單 triangle](c5_degree5_triangle_components.md) |
| 唯一 degree-5、三條 z-spokes、H−z 恰含一個任意 odd-cycle，其餘 bridges | 保留接點縮環、全部固定-q z 色及 minimality；任意長度排除，紙面＋有限 minor 控制，未 Lean 化 | [單長奇環](c5_degree5_odd_cycle_components.md) |
| 唯一 degree-5、三條 z-spokes、H−z 恰含兩個共用點 triangles，其餘 bridges | 任意接點位置／外枝排除；888 模板、295,920 接線非 disk；紙面＋Python，未 Lean 化 | [共用點雙環](c5_degree5_shared_triangles.md) |

以上各 block 結果都是紙面化約配合 Python 有限證書；不能統稱已 Lean 化。
共同 forcing-list 基礎已有 [Math/ForcingLists.lean](../Math/ForcingLists.lean)：
bridge singleton、swap 對稱、palettes 覆蓋、二色 list 環、triangle 與 apex 規則。
其具名定理對照仍見 [歷史交接的 Lean 化紀錄](HANDOFF_HISTORY.md) 與
[Math/ForcingListsAudit.lean](../Math/ForcingListsAudit.lean)。

## 2. 精確停止點與下一個窄問題

**三-spoke 的單一二接點分量 C，恰含兩個頂點互斥 triangles，以 bridge 路徑
相連，其餘為 bridges。** 共用 cut vertex 分支已排除。
先讀 [共用點雙環報告 §1–6](c5_degree5_shared_triangles.md)，再查單 triangle、
樹及完整介面。固定 N_B(z)={b0,b1,b4}，C 位於 arc b1,b2,b3,b4 一側。

1. 按兩個 z 接點位於兩環、連接路徑或旁支分型；先辨識哪些 bridge
   切出不含接點的分量，哪些切口兩側仍經同一 z 關聯。
2. 保留兩個 z 接點在 block-cut tree 的實際位置與完整 F_C(q)={D}；
   消去不含接點的單 bridge 外枝，再推共同色框下的正常形與真正 minor。
3. 不把各環 root marginals 獨立拼接，不直接套全 degree-4 的連接路徑縮短；
   每步須核對固定 q 的全部 z 色、degree、實際 spokes 與 minimality。

R15 共用點雙環分支已完成，R11–R14 成果保留。兩環中含長環、更多環的一般
分拆 (2)、其他接點分拆仍開放。不增加 k、環數或外枝深度的 catalog；
其餘追蹤項目見 [STATUS.md](STATUS.md)。

一般 degree≥5、單側出口、共同 pivotal edge、候選 A、
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

最新研究重播入口（依賴與信任範圍見 [報告 §6](c5_degree5_shared_triangles.md)）：

```bash
uv run --with networkx==3.5 python scripts/c5_degree5_sectors.py --check
uv run --with networkx==3.5 python scripts/c5_degree5_tree_components.py --check
uv run --with networkx==3.5 python scripts/c5_degree5_triangle_components.py --check
uv run --with networkx==3.5 python scripts/c5_degree5_odd_cycle_components.py --check
uv run --with networkx==3.5 python scripts/c5_degree5_shared_triangles.py --check
uv run --with networkx==3.5 python scripts/c5_degree5_interfaces.py --check
lake build
git diff --check
```

五輪成果的發布前重播範圍與結果見 [STATUS §16](STATUS.md)。
查舊實驗時讀對應報告；歷史生成器可能覆寫 artifacts，勿把重建指令當只讀 checker。
