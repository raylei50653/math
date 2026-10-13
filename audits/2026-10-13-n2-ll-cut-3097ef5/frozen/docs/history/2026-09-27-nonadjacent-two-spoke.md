# 2026-09-27：非相鄰 two-spoke 指定列分離與出口整合

接手本地 main／origin tracking 為 `18cb826`，工作樹起初乾淨；本輪未查遠端
即時 SHA，未 commit／push。研究報告見
[非相鄰分離](../c5_two_spoke_nonadjacent.md)，整合見
[單側出口](../c5_single_sided_exit.md)。

## 成果與證據範圍

- S={b1,b4} 四個必要代表均接受 p=01021、01212。
- 01021 的同色 spoke 刪除化為全 degree-4；任意大小結構及固定 triangle
  colors 的 path-tail transfer 保留 z 查詢。74 個正常形增邊候選均接受 q。
- 01212 先用四邊形側完整關係不變、五邊形側換色對稱及接點數界；
  原 C2 與 z 的 degree-4 completion 只剩 triangle／兩 triangles 直橋。
  36＋3,456 個實際接線無所需雙列禁色；528 個拒絕 p 的 completion
  另保留全部非 boundary 邊刪除 coloring。
- 原接點次序、actual attachments 與共同色框留在證書；同分量不乘 marginals。
  短枝替換只用已證的固定 parent-color 查詢保持，不聲稱不同來源 root 集合相同。
- {b2,b4} 僅用既有正式 reflection transport；反射交換兩個 p 的色置換等價類。
- 唯一 degree-5 的全部 t=2 分支已完成出口相容分離。僅在來源雙缺失的
  繼承前提下推出核心完整單缺失；未證所有非相鄰來源在 T4 下都單缺失。

任意大小覆蓋依賴既有紙面 degree-4／minor／path-transfer 定理及外部
degree-list 定理。新 Python 是有限候選證書；Lean 是普通有限列代數及
反射接合，沒有 `native_decide`，圖層證明與 74／3,492 分類未 Lean 化。

## 驗證

以下全部通過：

```bash
python3 scripts/c5_two_spoke_nonadjacent.py --check
python3 scripts/c5_two_spoke_split_support.py --check
python3 scripts/c5_two_spoke_reflection.py --check
python3 scripts/c5_degree5_two_spoke_sectors.py --check
uv run --with networkx==3.5 python scripts/c5_triangle_path_reduction.py --check
uv run --with networkx==3.5 python scripts/c5_two_triangle_blocks.py --check
lake build
lake env lean Math/TwoSpokeNonadjacentAudit.lean
python3 scripts/check_docs.py
git diff --check
```

`lake build`：8,826 jobs，只有既有 lint warnings。新模組五個 theorem 的
公理清單均為 `propext, Classical.choice, Quot.sound`，沒有 `sorryAx` 或
native-decide axiom。新證書重算後逐 byte 一致，另核對反轉 C2 接點次序
必同時反轉 tuples 的兩個座標。

未重跑舊全量 deletion audit、全部早期 Gallai／K4／long-cycle／fork minors、
雙拒絕 atlas 或一般圖 catalog；其任意大小定理保留既有信任依賴。
18 個 triangle bases 及 64 個 q-critical 雙 triangle bases 的 rotation
均在新 checker 內核對；74 個合格 (base,z) 項另核對拒絕及刪邊延拓，
涉及 10 個單 triangle bases 及 32 個雙 triangle bases。兩份來源 artifact
hashes 一併封存。沒有新的 planarity 搜尋。

初次 Lean build 有 doc-comment 與 `set_option` 次序錯誤，修正後完整 build
及公理審計通過；初次 docs check 在研究紀錄尚未建立時報四個缺檔連結，
補齊紀錄後檢查通過。

## 停止點

本輪未做非相鄰來源完整全列分類，未另查四代表的一般實現性。
t≤1、多個 degree-5、degree≥6、一般核心存在／分離、共同出口與主命題
仍開放；下一窄入口見 HANDOFF。未改 603 profiles、固定點及 R31。
