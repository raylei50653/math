# 2026-10-03：ε=2 唯一 mixed 的原 spoke＋unary 省略全收

接手基準 `722bfa6`。使用者要求「繼續推進 ε ≥ 3」；先讀 HANDOFF、
STATUS、Kempe 導覽、Git 與相關記憶，沿用 math-research-handoff-publish。
保留前序未提交的 root 刪除、原路徑、單 triangle 接回及雙 spoke
bundle；未用 Graphify 或 sub-agents，未 commit／push。
成果見 [專題報告](../c5_excess_two_mixed_core_spoke_unary.md)，目前停止點
由 [Kempe 導覽](../c5_kempe_guide.md) 維護。

## 任意大小結論及來源邊界

完整 Σ=933／941、Σ edge-minimal、有序 induced-C₅ disk、ε=2、
相鄰雙 degree-5 roots 且恰一份原 mixed 的前提下，省略一側原 spoke
及另一側原單接點 unary 必全收 Ω，含 root 交換。
結合前輪雙 spoke 排除，保留 mixed 的 (4,4) minimal rejected-row
core 若存在，兩份原省略因子必都是單接點 unary。
**共同下界仍 ε≥2，尚未證 ε≥3；未新增 Lean theorem。**

原 unary V 保持任意大小。原逐點 degree-4 與 endpoint slack 給
全部十列非空 S_V；接合保留原 core 的全部 root/contact tuples，
對字面原 spoke 過濾，再加原 wv 的不等式。
同一原支援 S=N_B(V) 的整體換色使 F_V 在同一局部 equality shape
上只有一份 transport 一致的選項。非空 shape 交集仍只是必要放寬，
不能宣稱十列 endpoint relations 有同圖實現。

相容時，僅為非平面反證，把同一原連通 V 收縮成一點，保留其
原 support 及唯一 root 邊。原 core 的 run 縮減是另一組互斥、保留
B,z,w 的 minor branch sets，且保持 roots 的完整 relation；兩步
能在同一來源同時進行。必要 minor 的 boundary-apex 圖皆有明示
K₅／K₃,₃ subdivision，故真正 disk 原來源不可能。
此 contraction 不保持原 V 染色，亦未把 V 換成任選 spoke。

## 固定必要域、完整證書與負控制

重用 126 必要正常形、570 份具名原 root 邊，兩個 root 方向的原
spoke＋unary 接合共 3,732 份；不重開一般來源 graph catalogue。
933、941 各五像合計 37,320 比較：

| 目標 | 已空列 | 兩色迫接受 | 固定支援階段 |
| --- | ---: | ---: | ---: |
| 933 | 5,880 | 11,552 | 1,228 |
| 941 | 9,382 | 7,722 | 1,556 |

2,784 抽象殘留的 89,088 次同原支援比較中，83,644 次 shape
交集空；其餘 5,444 次由 2,640 份具名原收縮星 minor 全排。
其中 2,637 份 K₃,₃、3 份 K₅；每條 path 的邊及 branch／內部
互斥性獨立驗證，沒有只保存 NetworkX boolean。

[Checker](../../scripts/c5_excess_two_mixed_core_spoke_unary.py)／
[artifact](../../artifacts/c5_excess_two_mixed_core_spoke_unary/observations.json)
保存原完整邊集、critical witnesses、全部 contacts／attachments／support、
ownership、原 joint tuples、完整原 core coloring、完整接合算子、
32 份支援 local shapes、逐候選衝突列及具名 subdivision 路徑。
5,700 core 列核對、37,320 spoke 接回列核對、559,800 次十五份
非空 endpoint relation 的完整算子接合通過。
Core coloring indices 只證原 core 全染色，沒有虛構 V 內點的見證。

26 張固定原長圖保持原 roots 為 singleton branch sets，保存各自
全部原 contacts 與 joint witnesses；780 次 root-pair 比較、5,240 次
spoke 接回後原 unary-owner 色集比較相等。
32 張實際接上 singleton／edge／path／triangle 原 unary 的完整圖，
320 次十列接合與全圖回溯一致，保存原 V 完整邊、附件及全圖
coloring；它們不是 disk 或 Σ-minimal 正控制。

負控制是 form 0、原 roots (5,7)、spoke (4,7)、unary owner 5、
目標 948。逐列獨立禁色 `[-1,0,-1,2,-1,-1,2,-1,-1,-1]` 可使
算子匹配目標；它無法來自任何符合固定支援及 disk 必要 minor 的
同一原 V。此 schedule 只是代數负控制，不是來源實現。

## 實際驗證及未重跑範圍

已執行以下檢查；新 checker 兩種 hashseed 的逐 byte 重播一致：

```bash
uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_spoke_unary.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_spoke_unary.py --check
python3 scripts/c5_excess_two_mixed_core_spokes.py --check
uv run --with networkx==3.5 python scripts/c5_triangle_path_reduction.py --check
lake build
```

前輪 6,068 雙 spoke 接回、242,720 原 spoke 子集比較及 26 長圖
重播通過。Path reduction 的 120 palette-switch、20 三-run、8
第一段重複排除及八份兩-run 正常形通過。`lake build` 通過
（8,831 jobs，僅既有 style／unused simp warnings），未形式化新結論。

新大型 artifact 為 189,362,323 bytes，MANIFEST 及 generated ignore
登錄後共 121 份產物／116 producers；其直接大型輸入是原雙 triangle
artifact，小型原枝及 run 證書亦明列在 producer source hashes。
專題、前輪後續標記、README、導覽與 STATUS 一併更新。
HANDOFF 的研究線及 tag 未變，依薄索引規則保持原內容。

```bash
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

文件檢查通過（476 Markdown、4,922 local links）；DocGraph 通過
（62 documents、213 relations、5 families，0 errors／notes）。大型
產物 `ok=121`，無 missing／changed／stale；`git diff --check` 通過。

未重跑：原 177,280 triangle lifts 全分類、triangle fork 全批、
全 degree-4 Gallai 合成、唯一 degree-6 全分拆、root 刪除／原 zw
接回的其他分支、一般來源 catalogue、其他 mixed／no-mixed 出口
與 Lean axiom audit。沿用它們既有任意大小及有限 topology 信任界線；
新 checker 重驗實際採用的 core 與完整染色，不重證外部 degree-list 定理。

## 跨對話接手摘要

```text
工作目錄 /home/ray/developer/ai/math；基準722bfa6，保留既有未提交bundle，
本輪未commit/push。先讀HANDOFF、STATUS、Kempe導覽與即時git status，
再讀docs/c5_excess_two_mixed_core_spoke_unary.md及本輪history。
固定完整Σ933/941、Σ edge-minimal induced-C5 disk，ε=2只剩雙degree5。
相鄰mixed的刪roots/zw均全收；本輪完成唯一mixed、(4,4)保留core的
spoke＋原單接點unary省略，含root交換，所得原省略圖必全收Ω。
3732接合/37320目標比較；2784弱殘留经同原支援89088次S4 shape transport，
83644跨列不相容，其餘5444由2640原收縮星K5/K3,3 subdivisions全排。
559800完整算子控制、26原長圖/780色對/5240原spoke比較、32原unary圖保存。
完整root/contact tuples、同框full witnesses、actual supports及ownership保留。
V只在minor反證收縮，不宣稱保持V染色；自由endpoint只檢查接合算子。
重播uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_spoke_unary.py --check，另hashseed17。
紙面+Python，無新Lean theorem；共同ε≥2仍未升為ε≥3。
下一窄題：(4,4)保留原mixed及原triangle z,w,x，兩側各省略一份原unary U,V，
保留二者任意大小/全部附件/完整endpoint relations/固定支援與同一root-pair joint。
只省略mixed、(5,4)/(4,5)、整圖(5,5)q-core仍保留；不可套錯唯一degree5定理。
多mixed、no-mixed、非相鄰roots/unary側例外、一般出口與K∞=K≤5仍未證。
```
