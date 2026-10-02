# 2026-09-29：無 mixed 兩側 t=2 整條原路徑與最後四項完成

接手 專案根目錄，HEAD=`51ef494`，工作樹已有 bridge／
endpoint 的未提交 checker、artifacts、報告及入口更新。讀 HANDOFF、STATUS
與 Git 狀態後，從 record 54／p₁ 的 β=2 停止點推進。保留既有成果與
原證書 bytes；未開 sub-agents、Graphify、全圖枚舉，未 commit／push。

成果：[報告](../c5_adjacent_degree5_no_mixed_t2_path_palettes.md)、
[checker](../../scripts/c5_adjacent_degree5_no_mixed_t2_path_palettes.py)、
[JSON](../../artifacts/c5_adjacent_degree5_no_mixed_t2_path_palettes/observations.json)、
[完整表](../../artifacts/c5_adjacent_degree5_no_mixed_t2_path_palettes/support_table.md)。

## 結果與下一窄入口

守恆的 source 禁色 d 迫使整條原 bridge 路徑的 q palettes 為
β₁,d,β₃,d,…,βℓ，每個奇數 β 可不同，但其原邊兩端共用 {d,β}。
因此原首橋的支援族與固定框弧反證可套到每條奇數原邊。
record 54 的 β=1 在任何位置均由原 z–w–C_w–b3 路徑給 K5，故只剩
β=2。交換全部 P 邊的 2／3 palettes、固定全部旁支，得到 root 色 2
下的同一 C_z 拒絕證書，與完整 F_z(q)={3} 矛盾。

68／p₂、173／p₂、256／p₁ 同理關閉。重算 2,892 組完整 joins 及
160 組原失敗候選，繼承 156 組反證、新增 4 組。原 322 份、88 份
frontier／side、完整 q schemas、placements、具名 rotations 全保留。
**644／644 查詢全證、322 份雙列皆證、0 個未決；新增來源排除為 0。**
無 mixed 兩側 t=2,(2) 的指定分離接入條件式出口第九類；完整 Σ 的
接合仍使用來源雙缺失及刪邊繼承。

本輪有限控制包括四個 d、長度 1／3／5／7 的獨立 palette words、
96 個局部 list 交換、192 份 Gallai tree 完整有序端點 relations、
704 份任意奇數位置的原圖 K5 skeletons（另核 root 交換及反射）、
322 次 target root 交換、4 組新候選的完整交換／字面反射及 13 個負控制。
不同奇數邊仍可不同 β 的負控制保留；有限圖不作原 disk 實現宣稱。

下一窄入口：**t_z=2,(2)，t_w=1,(2,1)** 的 actual-support／rotation
必要覆蓋。只讀原 no-mixed JSON 的 3,548 份 retained joins，依原
`root_boundary` 長度與 `ports` 過濾，得有序 136 份，首項原 sides
=(133,91)：B_z=01、F_z(q)={2}；B_w=0、兩個 F 為 {1}、{2}，c=3。
保留三個原分量、五個原接點、三 spokes、zw 與完整共同色框；root
交換覆蓋反向，不直接沿用兩側 t=2 的六單位幾何。

證據為任意大小紙面＋外部 degree-list 定理＋Python。本輪重讀核對
Dvořák Lemma 7／Theorem 10 第 5–6 頁，明用後者的充分方向重建第二份
拒絕證書。不需 T4，未新增 Lean theorem、來源實現、一般出口或主命題。

## 實際驗證

以下 9 個 checker 全部通過；新層先生成，再 `--check` 逐 byte 重算。
原 t=2、bridge、endpoint artifacts 均保留原 bytes，SHA256 綁定通過。
`lake build` 通過（8,827 jobs），只有原有 AttachmentOrder／SymRelabel
style／unused simp 等 warnings，沒有新增 Lean 檔。

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_t2_path_palettes.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_endpoints.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_bridge.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_single_spoke_first_bridge.py --check
python3 scripts/c5_single_spoke_branch_palettes.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

文件檢查通過：282 份 Markdown、3,062 個本地連結，HANDOFF 150 行。
DocGraph 通過：54 份文件、168 條關係、5 個 families，0 errors／notes。
`git diff --check` 通過；15 份 untracked 檔另以 no-index whitespace
檢查通過（含前兩輪成果）。
未重跑 no-spoke first-bridge、其他 mixed／singleton 完成表、唯一
degree-5 完成表、雙拒絕 atlas、R 系列大覆蓋、profiles／閉包、全圖
枚舉或 Lean axiom audit。build 不將本輪紙面 palettes／minor 證明形式化。
