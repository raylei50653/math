# 2026-09-29：無 mixed 兩側 t=2 原雙端點與 60 個新增延拓

接手 專案根目錄，HEAD=`51ef494`，工作樹已含前輪未提交的
bridge checker／artifacts／報告與入口更新。先讀 HANDOFF、STATUS、Git 狀態，
確認 580／644 已證及 record 5／p₂ 停止點。完整保留接手成果；未開 sub-agents、
Graphify 或來源圖枚舉。使用者未要求 commit／push，本輪未執行。

成果：[報告](../c5_adjacent_degree5_no_mixed_t2_endpoints.md)、
[checker](../../scripts/c5_adjacent_degree5_no_mixed_t2_endpoints.py)、
[JSON](../../artifacts/c5_adjacent_degree5_no_mixed_t2_endpoints/observations.json)、
[完整套表](../../artifacts/c5_adjacent_degree5_no_mixed_t2_endpoints/support_table.md)。

## 結果與停止點

record 5／p₂ 的 C_w source 禁色 0 不守恆，故不能把首橋的下一點設成
同一 residual。但原兩個接點各自的 tightness，加固定色 {1,3}，使兩端
局部 q residual 均為 {0,3}，各必接 b4 並接 b1／b3。固定框弧 123／4／0
及原 w–z–b0 路徑，將全部中間原 bridges 納入第一 branch set，得 K5。

完整保留原 322 份、88 份 frontier／side 資料、所有 q schemas、placements、
具名 contact rotations、原 IDs／SHA 與前層證據。重算 644 個查詢的
2,892 組完整 joins，逐項重算原 160 組失敗候選的前層證據；96 組既有
排除保持，本輪新增 60 組反證。**新增 60 個延拓、0 筆來源排除**，現為
**640／644 已證、318 份雙列皆證、4 個查詢未決**，A/A、A/?、?/A、?/?
為 318、2、2、0。原兩層 artifact 不改寫。

有限控制含 1,536 個 endpoint β 域／支援穩定子項、572 份兩 root 原路徑
K5 skeletons 及反射、322 次 root 交換、160 次字面 target 反射及 15 個
負控制。負控制保留不同端邊的 β 不必相等，以及 d 不守恆時不能推出
下一點 residual；原中間橋、contact、zw、spoke、附件與固定框弧不可漏。

剩餘為 54／p₁、68／p₂、173／p₂、256／p₁，root 交換及反射相關。
下一窄項 **record 54／p₁**：B_z=B_w=24、S_z=0124、S_w=234，兩側
F(q)={3}；唯一失敗候選 ({2,3},{3})。C_z 首橋 β=1 已排除，β=2
的兩塊支援族為 01、12、012、014、124、0124，尚無統一三弧。
保留原 C_w 的 234 支援、四 spokes、zw、同一首橋 β，研究 b0／b2
供應點選言與原接線次序；不把支援族當作來源實現。

證據是任意大小紙面證明＋外部 degree-list 定理＋Python；已核對 Dvořák
Lemma 7／Theorem 10 第 5–6 頁。不需 T4，未新增 Lean theorem、整型出口，
未證 disk 實現、完整 Σ、一般單側／共同出口或 `K∞=K≤5`。

## 驗證命令與範圍

下列 9 個 checker 全部通過；新層先生成，再以 `--check` 逐 byte 重算比對，
兩個前序 t=2 artifacts 保持原 bytes。`lake build` 通過（8,827 jobs），
只重播既有 AttachmentOrder／SymRelabel 的 style／unused simp 等 warnings。
文件檢查通過：279 份 Markdown、3,032 個本地連結，HANDOFF 149 行；
DocGraph 通過：53 份文件、164 條關係、5 個 families，0 errors／notes。
`git diff --check` 通過；新檔另以 no-index whitespace check 核對。

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_t2_endpoints.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_bridge.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_no_spoke_first_bridge.py --check
python3 scripts/c5_single_spoke_first_bridge.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
python3 scripts/c5_single_spoke_branch_palettes.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

未重跑其他 mixed／singleton 子類、唯一 degree-5 完成表、雙拒絕 atlas、
R 系列大覆蓋、profiles／閉包、全圖枚舉或 Lean axiom audit。build 僅驗證
既有 Lean 專案，不形式化本輪紙面拓撲；本輪重播與歷史大搜索分開記錄。
