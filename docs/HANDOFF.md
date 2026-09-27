# 研究交接：目前狀態與接手入口

文件更新與研究依據：2026-09-27。工作目錄 `/home/ray/math`。
本頁是**唯一的研究優先順序入口**；報告索引見 [STATUS](STATUS.md)，
更新約定見 [文件維護規則](DOCUMENTATION.md)。目前 single-spoke (2,1,1) 的剩餘單接點上界亦已分類；114 個具名配置全部已證兩個指定 p，無剩餘表內查詢。唯一 degree-5 的 t=2 已完成；一般版仍有 t≤1／更高 degree 等缺口。

## 1. 目前做到哪裡

主命題 **`K∞=K≤5` 仍未證**。目前活躍的是 weak-deletion 候選 A
minimal obstruction 路線下的 sector 目標；先研究單側出口，再處理共同出口。
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
207 份局部 minor。雙拒絕的九個 [Lean 共用引理](lean_two_rejection_tools.md)
不代表完整 disk 分類已形式化。3703 當輪驗證見
[研究紀錄](history/2026-09-24-3703-exclusion.md)；接合驗證見
[出口紀錄](history/2026-09-24-single-sided-exit.md)。

## 2. 精確停止點與下一個窄問題

目前入口為 [single-sided exit 接合定理](c5_single_sided_exit.md) §1–5。
五目標的來源假設與窮盡性已核對：若來源有一個全 degree-4，或唯一
degree-5／二或三-spoke 的 minimal q-obstruction，就存在只釋放 p 的出口；
不限制來源圖大小。五目標的窮盡性另有直接 Boolean 紙面推導。

**一般單側出口仍未證。** 下一個窄問題是失敗側 minimal cores 的分離：
每一個都必有 degree≥6、至少兩個 degree-5，或唯一 degree-5 且 t≤1。
[兩-spoke 區域化約](c5_degree5_two_spoke_sectors.md) 的 24 個保留配置中，
[三接點排除](c5_two_spoke_three_contacts.md) 已排除全部六個 (3) 型：
同圖 z=2／3 的 palette 差強迫一個 triangle 加三條同 parity bridge arms，
保留三個原接點；三個 triangle 頂點的實際 boundary tethers 給 K5 minor。
任意臂長由紙面證明，80 份局部 minor 是控制；未 Lean 化。
[相鄰 (2,1) 排除](c5_two_spoke_adjacent_21.md) 再排除 S={b0,b1} 的兩種禁色次序：
兩分量分別提供 odd cycle 與 z–b4 路徑；短側的 {1,3} palettes 及兩色實際
tethers 給 K5 minor，未合併 C₂、C₁，亦未引用 (3) 排除。
[中間相鄰 (2,1) 排除](c5_two_spoke_middle_21.md) 再處理 S={b1,b2} 的兩種次序：
兩個 z–b4 arcs 都見三色，但另一分量的實際路徑把 z、b4 接成一個外部
branch set，與該側的 0、1 點形成三角。palette {3} bridge 的兩側各碰三色，
或 leaf odd cycle 加保留其餘分量，都給同圖 K5 minor；兩種次序皆排除。
[反射與下一相鄰 orbit](c5_two_spoke_reflection.md) 以 ρ(i)=3−i、π=(0 1) 固定 q，
將 S={b0,b1} 排除搬到 S={b2,b3}；ordered relation／禁色搬運已有 Lean 普通證明。
原 18 項累計六項不存在；[split-support 完整列分類](c5_two_spoke_split_support.md)
再證剩四個相鄰表項的所有來源均只缺 q，故不可能作第二缺失核心。
在 S={b3,b4}，A 禁 0 且支援 {b1,b2,b3}，D 禁 3 且支援 {b0,b1,b4}：
任意列 b 的 F_A 是 b1=b3 時的 {b2}、否則空；F_D 是 b1≠b4 時的
U\{b0,b1,b4}、否則空。兩接點／單接點次序皆成立，完整接點 tuples 保留。
任意大小證明沿用 degree-4 結構定理：A padding 後只剩 64 個 disk forms；
D 的例外 completion 在 252 個完整接線中無雙列解。S={b4,b0} 僅由既有
Lean 反射搬運；新 Lean 證明有限列代數，完整 disk 分類仍為紙面＋外部定理。
Order I 的既有 disk witnesses 保留；order II 的一般實現性未證，但已非
第二缺失的缺口。[非相鄰分離](c5_two_spoke_nonadjacent.md) 現已完成八項：
四個 S={b1,b4} 代表均接受 p=01021、01212，S={b2,b4} 僅由既有反射搬運。
01021 用刪除同色 spoke 後的 degree-4 結構及保留 z 色的 path transfer；
74 個正常形增邊候選全部接受 q。01212 先用四邊形側完整關係不變與五邊形
側換色對稱，迫使 C2 在五邊形側；實際 degree-4 completion 只剩兩種結構，
3,492 個接線無相容雙列禁色。任意大小覆蓋為紙面證明；Lean 僅列代數與搬運。
因此唯一 degree-5 的 **t=2 全部分支已完成出口相容分離**；不另宣稱所有
非相鄰來源皆完整單缺失，也不宣稱四類皆可實現。
[single-spoke 必要化約](c5_single_spoke_cores.md) 已完成四種不可刪減覆蓋、
任意大小的接點區塊／實際支援次序及反射；(2,1,1) 三代表剩 19 支援型。
[外部雙路徑 completion](c5_single_spoke_completion.md) 保留二接點分量全部
接線，以其他分量的實際路徑取得 degree-4 disk minor，沿用既有 3,492 項
完整關係證書；原 (01,04,234) 入口的兩個 p 已完成。
[bridge 路徑化約](c5_single_spoke_bridge_path.md) 與 [旁支 palette 守恆](c5_single_spoke_branch_palettes.md) 後，
[旁支 K5 minor](c5_single_spoke_branch_minor.md) 已證 (01,04,1234)、禁 3
者二接點的 p₁ 延拓：任一奇數位置 bridge 的兩端連同旁支都碰同一對
框點，與其餘路徑及 C₁／C₂ 實際路徑給 K5；任意大小，未 Lean 化。
[單接點未用色守恆](c5_single_spoke_root_conservation.md) 以 root palette 歸納證 (012,04,234) 的 p₂；
[全表掃描](c5_single_spoke_root_sweep.md) 新增 14 個接受查詢後剩 34 個。
[二接點上界分類](c5_single_spoke_two_contact_bounds.md) 關閉其中 18 個：
容量 4、外部路徑 K5 6、未用色對 bridge 障礙 8；無直接套原 completion 者。
反射保存 raw target 色列，不僅比相等分割。
[單接點上界分類](c5_single_spoke_single_contact_bounds.md) 再以未用色在 root 的
禁色角色守恆，證剩餘 16 筆皆有 F_C(p)⊆{3}；12 個 p₁ 可取 z=2，
4 個 p₂ 可取 z=0。現為 **114 筆兩列全證、0 個表內查詢未決**；未新增 Lean theorem。
**下一個窄入口：t=1 的其餘接點分拆，先研究 (2,2) 的完整雙分量關係與實際支援。**
沿用既有四型必要覆蓋；不重開 (2,1,1) 表，也不從必要上界推論可實現性。
19 型不代表可實現或小圖正常形。其餘 t=1 分拆、t=0、degree≥6、多 degree-5
及一般核心存在／分離仍保留；先證任意大小限制，再做有限證書，不重啟圖枚舉。
一般失敗側的核心存在性化約仍未證；已完成的 t=2、兩葉鏈與五目標毋須重開。

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

接續目前研究的最小重播（本輪實際範圍見 [單接點分類紀錄](history/2026-09-27-single-spoke-single-contact-bounds.md)）：

```bash
python3 scripts/c5_single_spoke_single_contact_bounds.py --check
python3 scripts/c5_single_spoke_two_contact_bounds.py --check
python3 scripts/c5_single_spoke_root_sweep.py --check
python3 scripts/c5_single_spoke_root_conservation.py --check
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
