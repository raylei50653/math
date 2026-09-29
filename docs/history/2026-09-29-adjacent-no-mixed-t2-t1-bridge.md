# 2026-09-29：record 14 原外部路徑、首橋與 52 個新增延拓

接手 `/home/ray/developer/ai/math`，HEAD=`f29b899`，工作樹初始乾淨。
使用者要求繼續推進 record 14。讀 HANDOFF、STATUS、原支援表及
既有局部引理後，完成 record 14／p₁ 的幾何反證與同表套用。
未開 sub-agents、Graphify 或新圖枚舉，未 commit／push。

## 結果與同源界線

[報告](../c5_adjacent_degree5_no_mixed_t2_t1_bridge.md)、
[checker](../../scripts/c5_adjacent_degree5_no_mixed_t2_t1_bridge.py)、
[JSON](../../artifacts/c5_adjacent_degree5_no_mixed_t2_t1_bridge/observations.json) 與
[逐筆表](../../artifacts/c5_adjacent_degree5_no_mixed_t2_t1_bridge/support_table.md)
保留原 C_z、C_w、D_w、五接點、三 spokes、zw、支援及完整共同色框。
原 136 份、560 份、3,150 份幾何、完整 q schemas、rotations、原 ID／SHA
與 3,148 組完整候選皆綁定，前序 artifacts 不覆寫。

record 14 唯一失敗候選 F_w(p₁)={0,3} 迫使 C_w 的每份原路徑塊
碰 b1、b3。原 w–z–b0 及固定三框弧 12／3／40 給 K5 minor，
因此 p₁ 必延拓，與既有 p₂ 合成雙列已證。關閉機制是幾何阻斷；
不需重建額外 source 禁色，亦沒有排除 source q。

局部引理的外部路徑分成原本側 spoke、經 zw 的另一側 spoke、同側
另一原分量、經 zw 的另一側原分量。特別保存 D_w 的具名接點、
內部路徑及實際附件；未把它或 target 的 F_D={1} 當作新 spoke。
首橋限制另保留 source singleton 與 target pair，同一 β 綁定兩端。

| 階段 | 已證 target | 未決 |
| --- | ---: | ---: |
| 原支援／容量 | 1,002 | 118 |
| 固定框弧 | 1,044 | 76 |
| 同一首橋 | 1,054 | 66 |

新增 52 個延拓，494 份 A/A、33 份 A/?、33 份 ?/A。
146 組原失敗候選排除 70＋10，餘 66 組；empty_z 36、empty_w 30，
same_singleton 全關閉。新增來源排除為 0，沒有新增出口類別。

1,374 份 K5 skeletons 核對五組連通／不交／十鄰接、原分量支援、
root 完整 incidence、反射及 root 交換；15 份負控制含 D_w 的接點、
內部邊與附件缺失。146 組失敗候選核對字面反射與完整 root 交換，
3,148 組原 root 色對亦逐一核對交換。沿用的局部代數控制由本層重算。
控制圖不是 degree/list 或 disk 實現；任意大小由紙面引理承擔。

本輪讀回 Dvořák 講義 Lemma 7／Theorem 10，第 5–6 頁，確認 tightness
與 blockwise-uniform characterization。新成果為紙面＋外部定理＋Python，
不需 T4；未新增 Lean theorem，也未證整型分離、完整 Σ 或一般出口。

## 停止點

下一筆 record 22／p₂：原子表 ID=39、retained-join ID=3189、
sides=(137,102)，B_z=04、B_w=1、支援 (01,234,12)，source
F=({1},{2},{0})。target 的 F_z={1}、F_D={2} 精確，唯一失敗候選
為 F_w={0,3}，E_z={3}、E_w=∅。source d=2 不守恆，K={1,3}，
target 路徑塊族為 23／34／234。下一步研究兩端 tightness 及全原 bridge
路徑，保留 D_w 的 12 支援；未以此候選宣稱 disk 反例。

## 實際驗證

新 checker 先生成再 `--check`，與下列五個依賴重播皆通過。
`lake build` 通過（8,827 jobs），只有既存 AttachmentOrder／SymRelabel
style 及 unused simp warnings。文件檢查通過（291 份 Markdown、3,132 個
本地連結），DocGraph 通過（57 documents、183 relations、5 families，
0 errors／notes），HANDOFF 為 150 行。`git diff --check` 及新增檔案
空白檢查通過；原支援 JSON 另與 HEAD blob 逐 byte 核對一致。

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t1_bridge.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t1.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_bridge.py --check
python3 scripts/c5_single_spoke_first_bridge.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
python3 scripts/c5_single_spoke_branch_palettes.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

未重跑 root 預算、no-mixed 基層／interfaces、t=2 支援／endpoints／
path-palettes、其他 mixed／唯一 degree-5 完成表、雙拒絕 atlas、R 系列
大覆蓋、profiles／閉包及 Lean axiom audit。重播 t=2 bridge 的 580／644
及 single-spoke 歷史層數字只核對當層原證書，不取代其後已完成的結論。
