# 研究交接：目前狀態與接手入口

文件更新與研究依據：2026-09-29。工作目錄 `/home/ray/developer/ai/math`。
本頁是**唯一的研究優先順序入口**；完整專題索引見 [STATUS](STATUS.md)，
文件角色與更新規則見 [DOCUMENTATION](DOCUMENTATION.md)。歷史輪次只保留在
各專題報告與 `docs/history/`，不在此頁重述。

## 1. 現在從這裡開始

主命題 **`K∞=K≤5` 仍未證**。目前仍走 weak-deletion 候選 A 的
minimal obstruction 路線：先完成 single-sided exit 的可處理核心，再處理
一般／共同出口。唯一 degree-5 全部核心、唯一 mixed singleton、唯一 mixed K2
及 no-mixed 兩側 t=2,(2) 已接回條件式出口；一般出口仍未證。

**目前唯一優先入口：**
[t_z=2,(2)，t_w=1,(2,1)](c5_adjacent_degree5_no_mixed_t2_t1.md) 的
**record 14／p₁=01021**。

當前子表由原 136 份有序資料接成 560 份必要支援；1,002／1,120 個 target
已證，剩 118 個查詢／146 組失敗候選。第一個停止點為：

\[
B_z=04,\quad B_w=3,\quad
(S_z,S_w,S_D)=(01,123,34),
\]

\[
(F_z,F_w,F_D)(q)=(\{1\},\{0\},\{2\}),\quad c=3.
\]

p₁ 下 F_z={1}、F_D={1} 已可精確搬運；唯一失敗候選是

\[
\boxed{F_w(p_1)=\{0,3\}}.
\]

使 E_w(p₁)=∅。下一步只比較**同一原 C_w** 的 source singleton
F_w(q)={0} 與 target pair F_w(p₁)={0,3}：保留原 C_z、C_w、單接點 D_w、
五個接點、三 spokes、zw、actual supports、bridges、旁支與共同色框。

優先檢查順序：
1. 完整關係／actual-support 色置換是否再收緊 F_w(p₁)；
2. 端點 tightness、原 bridge palettes 或固定框弧是否排除 {0,3}；
3. 若只剩單一 palette 模式，是否可重建第二個 source 禁色，與 F_w(q)={0} 矛盾；
4. 若幾何要求本身不可能，才記為來源／候選的支援或 minor 阻斷。

**不要**重開已完成的兩側 t=2 大枚舉；不要把飽和 D_w 當成 spoke 或刪掉；
不要把 source 的 D+O+κ 預算直接套到 target；未決上界候選不是 disk 反例。

## 2. 可重用證明工具與界線

| 工具／機制 | 可安全使用的結論 | 主要入口 |
| --- | --- | --- |
| 完整關係搬運＋容量上界 | actual support 上存在共同色置換時精確搬運；否則只保留包含真實 F 的完整上界 | [t₂/t₁ 支援表](c5_adjacent_degree5_no_mixed_t2_t1.md) §4 |
| Root degree 超額預算 | source q 的 no-mixed minimal core 有 D+O+κ=degree−4；不是 target 等式 | [Root 預算](c5_root_degree_excess.md) §1–3 |
| 樹上 edge-minimal list obstruction | root 樹有 κ=0，lists 由 incident 邊色完整描述；不能把 source 邊色直接傳到 p | [Root 預算](c5_root_degree_excess.md) §4–5 |
| actual support／annulus 次序 | 保留原分量與具名接點後得到任意大小必要覆蓋；必要表不等於 disk 實現 | [t₂/t₁ 支援表](c5_adjacent_degree5_no_mixed_t2_t1.md) §2–3 |
| 原外部路徑＋固定框弧 minor | 可排除來源或使用 target 拒絕假設排除某候選；兩者必分開記錄 | [t₂/t₂ bridge](c5_adjacent_degree5_no_mixed_t2_bridge.md) |
| 端點／bridge palette 相容性 | source/target 不全域守恆時，仍可利用同一原路徑端點 tightness 與完整 relation | [t₂/t₂ endpoints](c5_adjacent_degree5_no_mixed_t2_endpoints.md) |
| 整份拒絕證書 palette 交換 | 幾何排除其他選擇後，可在同一原 C 上重建額外 source 禁色 | [t₂/t₂ path palettes](c5_adjacent_degree5_no_mixed_t2_path_palettes.md) |

目前已證的高階 source 結構是 [Root 預算](c5_root_degree_excess.md)：
D+O+κ=degree−4，以及樹骨架 κ=0。**尚未證**的是：
「交換或幾何阻斷」機制的一般完備性、no-mixed 雙 root 全分拆分離、
以及任意 degree-5 root 樹的跨列分離。

已關閉的主線家族：唯一 degree-5 全部分支；唯一 mixed singleton 全支援；
唯一 mixed K2 全接線；no-mixed 兩側 t=2,(2) 的 644／644 target。
目前活躍的是 no-mixed t₂/t₁；其餘 no-mixed 分拆（特別是 O=1 型）、
degree≥6、多 degree-5、非樹／非相鄰 roots、一般／共同出口均保留。
完整數字、前提與證據入口一律查 [STATUS](STATUS.md) 與各專題報告。

證據層保持分開：紙面證明、外部 degree-list 定理、Python 固定域控制、
Lean 普通證明與 Lean `native_decide` 不互相代替。必要支援／minor skeleton
不是來源實現證書；固定 q 結論也不自動提升成完整 Σ。

## 3. 其他路線的現況

保留的 [R31](c5_degree5_same_terminal_triangles.md) 缺口：同末端不同二接點的
任意長來源到 C3–C3–C3 的 boundary 固定 minors 尚未補完。
R27 末端各一臂及 [R30](c5_degree5_middle_cycle_minors.md) 中間不同二接點鏈型
已排除；[其他三環型](c5_degree5_three_cycle_positions.md) 仍開放。
其他 R 系列、cell catalogue、Kempe、repair、grammar／topology 與 state 缺口見 [STATUS](STATUS.md)。
[同染色有序重接](c5_dual_path_surgery.md) 的一步公式及同圖三配對反例保留；record 110 已另由原圖 K5 排除，有限可迭代 state 仍未證。
[邊位置對座標](c5_edge_pair_coordinates.md) 把 Kempe screen 等價化為 20 條蘊涵；1,024 masks 已核對，未新增排除或關閉一般 degree-5、共同出口與主命題。
[循環流](c5_circulation.md) 統一六維計數／153 支撐／十二循環；36 份基底覆蓋證三套分開的整數 orbit 條件不再收緊恆等式解。紙面＋Python，未 Lean 化或排除平面來源；重播見報告與[當輪紀錄](history/2026-09-27-circulation.md)。

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

## 5. 重播入口與驗證範圍

本輪五個 checker 見 [預算及支援紀錄](history/2026-09-29-root-degree-excess.md)；提交整理見 [發布核對](history/2026-09-29-root-degree-excess-publish.md)。
兩側 t=2 的三輪成果及發布驗證沿用 [既有紀錄](history/2026-09-29-adjacent-no-mixed-t2-publish.md)。

```bash
python3 scripts/c5_root_degree_excess.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t1.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

雙拒絕 atlas 與 Lean axiom audit 另見 [分類報告](c5_two_rejection_proof_zh.md) 與 [Lean 工具](lean_two_rejection_tools.md)。
本輪未重跑 t=2 bridge／endpoint／path-palettes、其他 singleton／唯一 degree-5 完成表、雙拒絕 atlas、R 系列大覆蓋、profiles／閉包及 Lean axiom audit。
發布狀態以即時 Git 為準；歷史生成器可能覆寫 artifacts，勿把重建指令當只讀 checker。
早期交接見 [HANDOFF_HISTORY](HANDOFF_HISTORY.md) 與 [2026-09-22 快照](HANDOFF_2026-09-22.md)；歷史待辦與 Git 狀態均非現況。
