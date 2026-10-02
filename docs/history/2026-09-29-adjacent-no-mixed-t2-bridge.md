# 2026-09-29：無 mixed 兩側 t=2 原 bridge、固定框弧與 68 個新增延拓

接手 專案根目錄，`main` 在 `51ef494`、工作樹乾淨，
本地 tracking branch 無差距；本輪未重新查遠端 SHA。先讀 HANDOFF、STATUS
及現行報告，沿交接 record 4／p₁ 推進。未啟動 sub-agents 或 Graphify；
使用者未要求 commit／push，本輪未執行。

成果：[報告](../c5_adjacent_degree5_no_mixed_t2_bridge.md)、
[checker](../../scripts/c5_adjacent_degree5_no_mixed_t2_bridge.py)、
[JSON](../../artifacts/c5_adjacent_degree5_no_mixed_t2_bridge/observations.json)、
[完整套表](../../artifacts/c5_adjacent_degree5_no_mixed_t2_bridge/support_table.md)。

## 結果與界線

- record 4／p₁ 的唯一失敗候選 F_w={0,3} 迫使每個原路徑塊均接 b1、b3；
  原 wb4 與固定框弧給 K5，故此列延拓。保留 wb3、zw、C_z 與全部接點。
- 固定三框弧允許原 own-spoke、經 zw 的 other-spoke、經 zw 及另一原 unary
  的實際路徑。首橋仍用同一 β、同一原路徑塊及字面色框；局部二色 residual
  不與整分量 singleton F 混用。任意大小結論沿用 rooted-palette 歸納。
- 原 322 份資料、88 份 frontier、完整 q schemas、placements、rotations、
  來源 ID／SHA 保留。重算 644 個 target 的全部 2,892 組禁色接合，其中
  原 160 組失敗候選由三框弧排除 72、首橋另排除 24，剩 64 組。
- 三框弧先新增 44 個延拓，首橋再新增 24 個；合計 **68 個延拓、0 筆
  來源排除**。累計 **580／644 target 已證，258 份雙列皆證，64 個未決**。
  A/A、A/?、?/A、?/? 為 258、32、32、0；原表沒有覆寫。
- 576 個穩定子控制、48 個 pair residual 控制、既有首橋歸納代數；
  682 份保留兩 roots／四 spokes／原 zw 的 minor skeletons 及反射；
  322 次 root 交換、160 次字面 target 反射、12 個負控制全部通過。

初探時另試既有兩框弧及相同列 locality 條件，這 64 個查詢未再減少；
沒有因此引入新排除或擴大圖枚舉。新 checker 的正式範圍只含報告所證
三框弧與固定色首橋。

紙面＋外部 degree-list 定理＋Python；本輪核對 Dvořák Lemma 7／Theorem 10
第 5–6 頁，僅使用連通 degree assignment 拒絕的結構結論，不需 target
minimality 或 T4。未新增 Lean theorem，未證 disk 實現、完整 Σ、整型
t=2 分離、一般單側／共同出口或 `K∞=K≤5`；未新增整型出口類別。

下一窄項為 **record 5／p₂**（frontier 28、sides 137,141）：
B_z=04、S_z=01、F_z(q)={1}；B_w=14、S_w=1234、F_w(q)={0}。
唯一失敗候選 ({1},{0,3}) 使 E_w=∅；K={1,3}、d=0 不守恆，現有首橋
引理不適用。保留 wb1、wb4、zw、C_z，研究 q／p₂ 只改 b2 的端點與
原 bridge palette 限制，再套其餘 64 個查詢。

## 實際驗證

下列 13 個 checker 的 `--check` 全部通過；新 artifact 先生成，再逐 byte
重算比對。相關既有證書保持原 bytes。

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_t2_bridge.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared.py --check
python3 scripts/c5_adjacent_degree5_singleton_long_arc.py --check
python3 scripts/c5_no_spoke_supports.py --check
python3 scripts/c5_no_spoke_exterior.py --check
python3 scripts/c5_no_spoke_first_bridge.py --check
python3 scripts/c5_single_spoke_first_bridge.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
python3 scripts/c5_single_spoke_two_two_minor.py --check
python3 scripts/c5_single_spoke_branch_palettes.py --check
```

`lake build` 通過，8,827 jobs；僅重播既有 AttachmentOrder／SymRelabel
style、unused simp 等 warnings。未新增 Lean 檔，build 不表示紙面拓撲已形式化。

文件檢查通過：276 份 Markdown、3,010 個本地連結，HANDOFF 148 行。
DocGraph 通過：52 份文件、160 條關係、5 個 families，0 errors／notes。
`git diff --check` 通過。收尾命令如下：

```bash
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

未重跑其他 mixed 子類、唯一 degree-5 完成表、雙拒絕 atlas、R 系列大覆蓋、
profiles／閉包、全圖枚舉或 Lean axiom audit。歷史大搜索與此 13 個任務相關
重播分開；README、STATUS、HANDOFF、前序報告及出口狀態已連入本輪結果。
