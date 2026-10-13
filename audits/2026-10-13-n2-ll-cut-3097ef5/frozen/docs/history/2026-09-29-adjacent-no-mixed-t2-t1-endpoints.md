# 2026-09-29：record 22 原雙端點與 t_z=2、t_w=1 整型出口

接手基準 `f29b899`，工作目錄為專案根目錄。使用者要求
繼續推進 record 22，未要求 commit／push；保留進場時 record 14 的 checker、
artifacts 與文件變更。本輪新增獨立 endpoints 層，不覆寫前層證書。
目前優先序見 [HANDOFF](../HANDOFF.md)，完整證明見
[原雙端點報告](../c5_adjacent_degree5_no_mixed_t2_t1_endpoints.md)。

## 本輪結論

record 22／p₂ 的唯一失敗候選 F_w={0,3} 下，source d=2 雖不守恆，
原兩端 tightness 與 K={1,3} 仍迫使 β₀=βℓ=3。兩端 q residual={2,3}，
端點支援族由 target 的 23／34／234 收緊為 23／234；固定框弧
12／34／0、原 w–z–b0 與全部中間 bridges 給 K5 minor。
不推論下一點有相同 q residual，不把 D_w 視為 spoke。

同一原雙端點引理關閉全部 66 個前層未決查詢：

| 數量 | 結果 |
| --- | ---: |
| 新增指定列延拓 | 66 |
| 全部已證／總查詢 | 1,120／1,120 |
| 雙列皆證的原支援記錄 | 560 |
| 未決查詢／新來源排除 | 0／0 |
| 重算完整 joins／原失敗候選 | 3,148／146 |
| 繼承／新增候選反證 | 80／66 |
| K5 skeletons／負控制 | 732／18 |

原 136 份正常形、560 份記錄、3,150 份幾何、完整 schemas、rotations、
三原分量、五接點及三條 spokes 均保持。前層有序 context 從原正常形
重建，避免 JSON 將 root 字典排序為 w,z 後改變 witness 列序；證據內容
不變。D_w 的刪邊負控制選 record 14，因 record 22 原 wb1 會提供替代
連接，不能把仍成立的 witness 當作預期失敗。

出口第九類擴至無 mixed t_z=2,(2)、t_w=1,(2,1) 及整圖 root 交換型；
完整 Σ 仍另用來源雙缺失及刪邊繼承。不需 T4，紙面＋外部 degree-list
定理＋Python 有限控制；未新增 Lean theorem、必要表可實現性或一般出口。
本輪核對 Dvořák 原文 Lemma 7／Theorem 10 第 5–6 頁。

## 實際驗證

下列八個 checker 均通過，重算後逐 byte 核對原 artifacts：

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t1_endpoints.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t1_bridge.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t1.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_endpoints.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_bridge.py --check
python3 scripts/c5_single_spoke_first_bridge.py --check
python3 scripts/c5_single_spoke_branch_palettes.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

`lake build` 通過（8,827 jobs），只有既有 AttachmentOrder／SymRelabel
linter warnings；不是新紙面 minor／degree-list 的 Lean 形式化。
文件檢查通過：294 份 Markdown、3,159 個本地連結，HANDOFF 為 150 行。
DocGraph 通過：58 份文件、188 個關係、5 個 families，0 errors／notes。
`git diff --check` 通過；未 commit／push。

未重跑 root 預算、兩側 t=2 path-palettes、no-mixed 固定圖／完整介面、
其他 mixed／唯一 degree-5 完成表、雙拒絕 atlas、R 系列大覆蓋、profiles／
閉包或 Lean axiom audit；既有證據沿用其報告，不宣稱整庫全重驗。

## 精確交接

下一窄型為 t_z=2,(2)、t_w=0,(2,1,1)。本輪只讀原 3,548 份同色 joins，
綁定 96 份有序子表及 hash；首項 retained-join ID=3048、sides=(133,64)，
B_z=01、F_z={2}，w 無 spoke、F=({0},{1},{2})，共同 c=3。
尚未建立 actual-support／rotation 必要覆蓋；需保留四原分量、六接點、
兩條 spokes、zw 及完整關係。其他分拆及 O=1 型保留。
