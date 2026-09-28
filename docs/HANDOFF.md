# 研究交接：目前狀態與接手入口

文件更新與研究依據：2026-09-28。工作目錄 `/home/ray/math`。
本頁是**唯一的研究優先順序入口**；報告索引見 [STATUS](STATUS.md)，
更新約定見 [文件維護規則](DOCUMENTATION.md)。唯一 degree-5 的全部 t≥1 及 t=0 的 (2,1,1,1) 核心已接回出口。下一入口是 t=0、(2,2,1) 保留支援表的 record 84／p₁；一般出口仍未證。

## 1. 目前做到哪裡

主命題 **`K∞=K≤5` 仍未證**。目前走 weak-deletion 候選 A 的 minimal obstruction 路線，先研究單側出口，再處理共同出口。
定義與全域較小代表／局部壓縮的區別見 [研究目標](c5_boundary_relations.md)。

已完成 [C5 雙拒絕分類](c5_two_rejection_proof_zh.md)：在 induced C5 為 disk
外框、C 非空連通、內點完整 degree≤4、b0 恰有兩個不同內鄰點的前提下，
拒絕 α=01212、δ=01213 強迫唯一二內點接線，簽章 1855。
因此 3647、3895、3901、3903 已在指定 sector 圖類內排除。
原 331／A(b)={0,2} 分支由此涵蓋；603 profiles 與固定點未改寫。

最新 [3703 排除](c5_sector_3703_exclusion.md) 接續
[兩葉鏈化約](c5_sector_3703_structure.md)：葉點 K3,3 minor 排除 024／234，
並迫使 012／234 的其餘內點避開 b1；三列 palettes 隨即使鏈無法延續。
**3703 已在上述指定圖類內排除，五目標皆完成**，不限制 triangle 數或 bridge 長度。

信任層：紙面證明＋外部 degree-list 定理＋Python 局部證書；新排除未 Lean 化。
新證書有 89 個局部轉移、兩個可達狀態及兩份葉點 minor；沿用鏈化約的
207 份局部 minor。[Lean 共用引理](lean_two_rejection_tools.md) 已接上 [實際接線與 degree-list 緊性](lean_boundary_degree.md)；
Gallai／完整 disk 分類仍未形式化。3703 當輪驗證見
[研究紀錄](history/2026-09-24-3703-exclusion.md)；接合驗證見
[出口紀錄](history/2026-09-24-single-sided-exit.md)。

## 2. 精確停止點與下一個窄問題

目前入口為 [single-sided exit 接合定理](c5_single_sided_exit.md) §1–5。
全 degree-4、唯一 degree-5 且 t≥1、唯一 degree-5 且 t=0／(2,1,1,1)，
或未接內點 boundary 核心都已接回出口，來源圖大小不受限。
完整 Σ(M)=Ω\{q} 另用來源雙缺失及刪邊繼承，不能只由 T4 或指定雙列推出。

| 已完成的唯一 degree-5 分支 | 證據入口與界線 |
| --- | --- |
| t=3 | [五目標接合](c5_single_sided_exit.md)；指定圖類紙面＋外部定理＋Python |
| t=2 | [非相鄰分離與前序結果](c5_two_spoke_nonadjacent.md)；全部分支完成，Lean 僅列代數與反射搬運 |
| t=1、(2,1,1) | [單接點上界分類及前序結果](c5_single_spoke_single_contact_bounds.md)；114 筆指定雙列全證 |
| t=1、(2,2) | [局部 residual 與前序結果](c5_single_spoke_residual_locality.md)；來源排除 278，保留 102 筆／51 型全部雙列已證、0 查詢未決 |
| t=1、(3,1)／(4) | [三接點](c5_single_spoke_three_one.md)／[三拒絕共同結構](c5_single_spoke_four.md) 給來源 K5；任意大小、不需 T4 |
| t=0、(2,1,1,1) | [環狀實際支援](c5_no_spoke_supports.md)；48 筆全部指定雙列延拓，保留原五接點與完整關係 |

t=1 與 t=0 新結果均為紙面＋外部定理＋Python，未新增 Lean theorem。
必要支援表、minor skeletons 不是來源可實現性證書，也未分類任意 T4 核心的完整 Σ。
逐輪證明鏈、數字及驗證留在報告與 [STATUS](STATUS.md)，不重啟已完成表的圖枚舉。

**一般單側出口仍未證。** 失敗側每個 minimal core 必碰全部五個 boundary
頂點，且有 degree≥6、至少兩個 degree-5，或唯一 degree-5 且 t=0、(2,2,1)。
[No-spoke 外部連通](c5_no_spoke_exterior.md) 已排除其餘四種 t=0 分拆；
多分量的另一原分量提供實際 z–B 路徑，各分量皆 K4-free；(5) 另用四列奇偶障礙。

(2,2,1) 的 1,952 筆必要支援經 T4 篩選剩 616 筆，
[原外部路徑 K5](c5_no_spoke_path_minor.md) 再於 q 下排除 500 筆，含 record 599。
剩 116 筆新增 104 個延拓後，為 108 筆 A/A、2 筆 A/?、2 筆 ?/A、4 筆 ?/?，
合計 **12 個未決查詢**；來源排除與 target 延拓分開計數。
完整資料見 [保留表](../artifacts/c5_no_spoke_path_minor/support_table.md)。

**下一窄入口：record 84／p₁。** 固定 q=01012、p₁=01021、p₂=01212，
具名原分量 (C₀,C₁,C₂) 的接點數為 (2,2,1)，全部實際支援為 (014,123,34)。
q 禁色為 ({0},{2,3},{1})；p₂ 可取 z=2。p₁ 的七組完整拒絕候選已消去六組，
只剩 ({0,1},{3},{2})。C₀ 的 target 原路徑塊支援只能為 01、04、014。

下一步比較**同一 C₀ 的 source singleton palette 與 target 首橋**；保留
五個原接點、完整有序關係、全部旁支／附件及 C₁／C₂ 的實際外部路徑。
q 在 C₀ 只有 singleton，不能套雙列 pair residual 引理，也不能改用 endpoint marginals。
未決 ID 為 84／1472 的 p₁、408／1561 的 p₂，以及 127／419／1390／1564 的雙列。
不得預設其他查詢由同一新引理解決，亦未證這些候選可實現。
已完成的 t≥1、兩葉鏈與五目標不重開圖枚舉。

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

目前入口的最小重播如下；本次六組成果與直接依賴的完整發布檢查見
[整理紀錄](history/2026-09-28-progress-publish.md)，各研究輪的驗證保留在原歷史頁。

```bash
python3 scripts/c5_no_spoke_path_minor.py --check
python3 scripts/c5_no_spoke_supports.py --check
python3 scripts/c5_single_spoke_cross_row.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

雙拒絕 atlas 與 Lean axiom audit 另見 [分類報告](c5_two_rejection_proof_zh.md) 與 [Lean 工具](lean_two_rejection_tools.md)。
接合輪重跑範圍見 [研究紀錄](history/2026-09-24-single-sided-exit.md)；
雙拒絕 atlas、R 系列大覆蓋、two-spoke 全表、抽象 profiles／閉包及 Lean
axiom audit 未於本次發布重跑；未重新查閱外部定理或擴大研究範圍。
歷史生成器可能覆寫 artifacts，勿把重建指令當只讀 checker。
早期交接見 [HANDOFF_HISTORY](HANDOFF_HISTORY.md) 與 [2026-09-22 快照](HANDOFF_2026-09-22.md)；歷史待辦與 Git 狀態均非現況。
