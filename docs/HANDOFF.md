# 研究交接：目前狀態與接手入口

文件更新與研究依據：2026-09-24。工作目錄 `/home/ray/math`。
本頁是**唯一的研究優先順序入口**；報告索引見 [STATUS](STATUS.md)，
更新約定見 [文件維護規則](DOCUMENTATION.md)。本輪完成指定 sector 圖類的 3703 排除。

## 1. 目前做到哪裡

主命題 **`K∞=K≤5` 仍未證**。目前活躍的是 weak-deletion 候選 A
minimal obstruction 路線下的 sector 目標；先研究單側出口，再處理共同出口。
定義與全域較小代表／局部壓縮的區別見 [研究目標](c5_boundary_relations.md)。

已完成 [C5 雙拒絕分類](c5_two_rejection_proof_zh.md)：在 induced C5 為 disk
外框、C 非空連通、內點完整 degree≤4、b0 恰有兩個不同內鄰點的前提下，
拒絕 α=01212、δ=01213 強迫唯一二內點接線，簽章 1855。
因此 3647、3895、3901、3903 已在指定 sector 圖類內排除。
原 331／A(b)={0,2} 分支由此涵蓋，無須再獨立處理。
603 profiles 未刪除，固定點未重算。

最新 [3703 排除](c5_sector_3703_exclusion.md) 接續
[兩葉鏈化約](c5_sector_3703_structure.md)：葉點 K3,3 minor 排除 024／234，
並迫使 012／234 的其餘內點避開 b1；三列 palettes 隨即使鏈無法延續。
**3703 已在上述指定圖類內排除，五目標皆完成**，不限制 triangle 數或 bridge 長度。

信任層：紙面證明＋外部 degree-list 定理＋Python 局部證書；新排除未 Lean 化。
新證書有 89 個局部轉移、兩個可達狀態及兩份葉點 minor；沿用鏈化約的
207 份局部 minor。雙拒絕的九個 [Lean 共用引理](lean_two_rejection_tools.md)
不代表完整 disk 分類已形式化。本輪驗證見
[研究紀錄](history/2026-09-24-3703-exclusion.md)。

## 2. 精確停止點與下一個窄問題

目前入口為 [3703 排除](c5_sector_3703_exclusion.md) §1–6 與
[五目標](c5_sector_targets.md) §1。兩葉鏈問題已完成，無須擴大生成器；
拒絕 3、7、8 本身已不可能，不必再聯立其餘接受列。

下一個窄問題是核對 **五目標局部不可實現到一般單側出口的邏輯連接**：
來源圖是否必滿足 induced-C5 disk、連通 C、內點 degree≤4、b0 恰兩接點，
以及五目標在欲套用問題中是否窮盡。未完成此核對前，不提升為一般單側
或共同出口定理。603 profiles 與固定點未改寫；舊抽象後繼核對仍為固定域歷史結果。

保留的 R31 缺口：同末端不同二接點的任意長來源到 C3–C3–C3 的
boundary 固定 minors 尚未補完；參考 [R31](c5_degree5_same_terminal_triangles.md)、
[R30](c5_degree5_middle_cycle_minors.md) 與 [R28](c5_degree5_three_cycle_positions.md)。
R27 末端各一臂及 R30 中間不同二接點鏈型已排除；其他三環型仍開放。

一般 degree≥5、單側出口、共同 pivotal edge、候選 A、
一般 weak-deletion congruence 與 `K∞=K≤5` 仍需各自的證明。

## 3. 其他路線的現況

R31 任意長來源 minor 缺口保留，暫不作優先入口。全 degree-4 合成、
三-spoke 零／一／二環及指定三環鏈型的成果，見 [STATUS](STATUS.md)。
Cell catalogue、Kempe、repair、grammar／topology 與 state 充分性均保留各自
證據及缺口；不因整理而重啟。一般 degree-5、共同出口與主命題仍未證。

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

接續目前研究的最小重播：

```bash
uv run python scripts/c5_sector_3703_exclusion.py --check
uv run python scripts/c5_sector_3703_structure.py --check
uv run python scripts/c5_sector_rejection_lists.py --check
uv run python scripts/c5_sector_terminal_blocks.py --check
lake build
python3 scripts/check_docs.py
git diff --check
```

雙拒絕分類的 atlas 與 Lean axiom audit 另見
[分類報告](c5_two_rejection_proof_zh.md) 與 [Lean 工具](lean_two_rejection_tools.md)。
本輪重跑範圍見 [研究紀錄](history/2026-09-24-3703-exclusion.md)；
雙拒絕 atlas、R 系列、抽象 profiles／閉包未重跑。
歷史生成器可能覆寫 artifacts，勿把重建指令當只讀 checker。

早期交接保存於 [HANDOFF_HISTORY](HANDOFF_HISTORY.md)，整理前的近期交接
全文保存於 [2026-09-22 快照](HANDOFF_2026-09-22.md)。
歷史中的「下一步／未提交」不是目前待辦；提交與遠端狀態須查即時 Git。
