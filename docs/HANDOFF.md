# 研究交接：目前狀態與接手入口

文件更新與研究依據：2026-09-24。工作目錄 `/home/ray/math`。
本頁是**唯一的研究優先順序入口**；報告索引見 [STATUS](STATUS.md)，
更新約定見 [文件維護規則](DOCUMENTATION.md)。本輪以同圖 K5 minor 排除全部兩-spoke (3) 型；一般單側出口仍有核心分離缺口。

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
不代表完整 disk 分類已形式化。3703 當輪驗證見
[研究紀錄](history/2026-09-24-3703-exclusion.md)；接合驗證見
[出口紀錄](history/2026-09-24-single-sided-exit.md)。

## 2. 精確停止點與下一個窄問題

目前入口為 [single-sided exit 接合定理](c5_single_sided_exit.md) §1–5。
五目標的來源假設與窮盡性已核對：若來源有一個全 degree-4，或唯一
degree-5／三-spoke 的 minimal q-obstruction，就存在只釋放 p 的出口；
不限制來源圖大小。五目標的窮盡性另有直接 Boolean 紙面推導。

**一般單側出口仍未證。** 下一個窄問題是失敗側 minimal cores 的分離：
每一個都必有 degree≥6、至少兩個 degree-5，或唯一 degree-5 且 t≤2。
[兩-spoke 區域化約](c5_degree5_two_spoke_sectors.md) 的 24 個保留配置中，
[三接點排除](c5_two_spoke_three_contacts.md) 已排除全部六個 (3) 型：
同圖 z=2／3 的 palette 差強迫一個 triangle 加三條同 parity bridge arms，
保留三個原接點；三個 triangle 頂點的實際 boundary tethers 給 K5 minor。
任意臂長由紙面證明，80 份局部 minor 是控制；未 Lean 化。
兩-spoke 尚餘 **18 個 (2,1) 配置**，不是已實現的圖分類。
一般失敗側的每個 minimal core 還必碰到全部五個 boundary 頂點，內點 degree 不限。
下一題取 (2,1)、相鄰 S={b0,b1}，兩分量都在長 arc
(b1,b2,b3,b4,b0)，q 禁色為 {2}／{3} 的兩種次序。
須保留 C₂ 的兩個共同接點、C₁ 的單接點、實際 attachments 及跨列共同色框；
本輪 (3) 的三葉 incidence tree 不能直接套到不同分量。
一般失敗側的核心存在性化約仍未證；兩葉鏈、五目標與 (3) 毋須重開。
603 profiles 與固定點未改寫；共同出口仍需獨立的共同 pivotal-edge 證明。

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

接續目前研究的最小重播（本輪實際範圍見
[三接點排除紀錄](history/2026-09-24-three-contact-exclusion.md)）：

```bash
python3 scripts/c5_two_spoke_three_contacts.py --check
python3 scripts/c5_unattached_boundary.py --check
python3 scripts/c5_degree5_two_spoke_sectors.py --check
uv run python scripts/c5_sector_3703_exclusion.py --check
uv run --with networkx==3.5 python scripts/c5_sector_targets.py --check
uv run --with networkx==3.5 python scripts/c5_degree5_sectors.py --check
uv run --with networkx==3.5 python scripts/c5_degree5_interfaces.py --check
lake build
python3 scripts/check_docs.py
git diff --check
```

雙拒絕分類的 atlas 與 Lean axiom audit 另見
[分類報告](c5_two_rejection_proof_zh.md) 與 [Lean 工具](lean_two_rejection_tools.md)。
接合輪重跑範圍見 [研究紀錄](history/2026-09-24-single-sided-exit.md)；
雙拒絕 atlas、R 系列大覆蓋、抽象 profiles／閉包未重跑。
歷史生成器可能覆寫 artifacts，勿把重建指令當只讀 checker。

早期交接保存於 [HANDOFF_HISTORY](HANDOFF_HISTORY.md)，整理前的近期交接
全文保存於 [2026-09-22 快照](HANDOFF_2026-09-22.md)。
歷史中的「下一步／未提交」不是目前待辦；提交與遠端狀態須查即時 Git。
