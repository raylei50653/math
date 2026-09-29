# 全 degree-4／block 化約系列導讀

文件整理：2026-09-23；研究依據截至 2026-09-22。本頁不新增研究結論。
研究線標記見 [HANDOFF](HANDOFF.md)，全專案索引見 [STATUS](STATUS.md)。
本系列從 minimal obstruction 的 list 翻譯，經樹、triangle、長奇環與 K4，
合成全 degree-4 的單缺失結論；後續唯一 degree-5 見 [R 系列導讀](c5_degree5_guide.md)。

## 1. 完成的結論與完整前提

**全 degree-4 分支已完成：接受全部 T4 的 C5 disk minimal q-obstruction，
若所有有效內點在該 obstruction 中的完整 degree 都等於 4，則 `Σ(G)=Ω\{q}`。**
任意內點數的合成及依賴見 [K4 報告 §4](c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論)。
這是紙面化約、外部 degree-choosability 定理及 Python 有限證書的合成，
不是整套論證已完成 Lean 形式化。

| 符號／前提 | 本系列的意思 |
| --- | --- |
| C5 disk | 有序五點 boundary 是 disk 外框；一般 planar 圖不夠 |
| Ω、Σ(G)、T4 | Ω 是合法 boundary patterns，Σ 是可延拓者；T4 是使用四種顏色的 patterns，見 [關係定義](c5_boundary_relations.md) 與 [小核心](c5_weak_list_cores.md) |
| q、D、U | 固定三色 singleton pattern；經允許的對齊取 q=01012，U={0,1,2,3}，未用色 D=3；實際 boundary 位置仍保留 |
| minimal q-obstruction | q 不延拓，但刪任一非 boundary 邊後可延拓；等價於非 boundary 邊集 inclusion-minimal，不是頂點最少 |
| 有效內點與 H | 忽略孤立內點；H 是其內部誘導圖，minimality 給出連通性 |
| 完整 degree=4 | 在 obstruction 整張圖中計算，包含 boundary spokes；不是只算 H 中的 degree，也不是只在原來源圖中計算 |
| L(v) | U 扣除 boundary 鄰居的 q 色；minimality 排除重複同色 spokes，故 D∈L(v)、全 degree-4 時 `|L(v)|=deg_H(v)` |

小核心與 odd-join 是前置／平行成果，部分包含 degree>4 的型，不能反向當作
全 degree-4 假設的推論。多數 block **結構排除**不需 T4，但最後一般單缺失
結論仍保留 T4；逐項差異列於下文。

## 2. 合成依賴：從任意 block tree 到三種末端類別

1. [List-critical 翻譯](c5_weak_list_cores.md) 給出緊 lists；外部
   degree-choosability 定理使不可著色的連通 H 為 Gallai tree，blocks 只能是
   cliques 或 odd cycles。外部定理的來源與使用條件沿用原報告。
2. Planarity 排除 K5 以上 clique；[K4 排除](c5_k4_blocks.md) 利用四個外接方向
   各自接到 boundary，構造 K5 minor。外側可含任意 blocks，此步不需 T4。
3. [Bridge pruning](c5_shared_pair_bridge.md) 隔離共用點 cluster；
   [任意 triangle tree](c5_triangle_tree_palettes.md) 用七種 root 介面、互補
   palettes 與保留閉鄰域的 minor，排除共用點 cluster。結合
   [互斥多環](c5_three_triangle_blocks.md)，只剩至多二個互斥 triangles。
4. [長環 root](c5_odd_cycle_roots.md) 將一般介面擴為十一種；
   [多長環](c5_multi_odd_cycles.md) 證明任意有限環樹的遞迴封閉與連續縮減，
   排除所有長 odd-cycle blocks，接回第 3 步。此結構結論不需 T4。
5. 對剩餘零／一／二 triangle 分別套下表，得到完整 `Σ(G)=Ω\{q}`。

| 剩餘 H | 結構與單缺失結論 | T4 的角色 |
| --- | --- | --- |
| 樹 | [樹核心](c5_tree_cores.md)：偶數點路徑、palette 至多切換一次；無界家族化到至多六內點 | 單缺失結論保留 T4 |
| 恰一個 triangle，其餘 bridges | [路徑枝](c5_triangle_path_reduction.md) ＋ [分叉排除](c5_triangle_forks.md)：外掛樹不分叉，任意長枝接回 canonical 分類 | 分叉排除不需 T4；單缺失結論保留 T4 |
| 恰二個 triangles，其餘 bridges | [兩環正常形](c5_two_triangle_blocks.md)：兩環互斥、直接一條 bridge、無其他外掛樹；64 個具名 disk lifts 全只缺 q | 不另需 T4，接受 T4 是結果 |

任意大小覆蓋來自紙面歸納／minor 化約；有限正常形與拓撲證書負責各個
有限排除端。不能僅從二、三、四環枚舉推論任意 block tree。

## 3. 全系列閱讀與後續對照

先讀合成報告掌握終點，再按下表回查依賴。表中的舊窄問題已完成者，
仍保留原報告與證書供重播；不當作目前待辦。

| 階段與報告 | 成果與後續定位 |
| --- | --- |
| [最小阻礙與三出口](c5_weak_critical_cores.md) | 固定圖 obstruction 族與三種出口的充要條件；一般 disk 單側／共同出口仍未證 |
| [至多三內點](c5_weak_list_cores.md) | List 翻譯、小核心分類與 degree-list 入口；四內點由下一篇補完 |
| [四內點與 odd-path](c5_four_vertex_cores.md) | 四內點 disk／T4 單缺失分類；無界單缺失家族否定「全部 minimal cores 大小有界」 |
| [Odd-join 家族](c5_odd_join_cores.md) | 指定 K2 join odd-cycle quotient 家族的任意長分離；不是一般 quotient 分類，也不全限 degree-4 |
| [Degree-4 樹](c5_tree_cores.md) | 任意樹的分叉排除、palette 與路徑化約；含 cycle 的分支由後續 block 工作補完 |
| [Triangle 接枝](c5_triangle_branches.md) | 至多兩個不同接枝位置，兩尾仍可同面；不能把「至多一枝」當引理 |
| [Root 介面反例](c5_root_interfaces.md) | 任意 standalone forcer 不能一概換成兩點；後續正結果需要整個 triangle context |
| [Triangle 路徑枝](c5_triangle_path_reduction.md) | 指定 triangle context 的任意長路徑枝保持全部 boundary rows 的 bridge 介面；分叉由下一篇補完 |
| [Triangle 第一分叉](c5_triangle_forks.md) | 任意深度外掛樹分叉排除，完成單 triangle 的單缺失結論 |
| [Cycle-5／唯一長環](c5_pentagon_branches.md) | 唯一 cycle 長度至少 5 的全 degree-4 disk obstruction 排除；多 block 由長環系列補完 |
| [兩 triangle blocks](c5_two_triangle_blocks.md) | 共用點、長 bridge 與額外外枝排除；直接 bridge 六內點型存活且只缺 q |
| [互斥三環／任意互斥多環](c5_three_triangle_blocks.md) | Triangles 兩兩頂點互斥時，任意總數至多二；共用點由後續處理 |
| [共用點三環](c5_shared_triangle_blocks.md) | 補齊恰三環全部連接型；不是當時已處理任意環數 |
| [四環共用點鏈](c5_four_triangle_chain.md) | 四環鏈 transfer 與拓撲排除；分叉由下一篇補完 |
| [四環共用點 star](c5_four_triangle_star.md) | 中央 triangle 的三個共用點分叉型排除；混合 bridge 型由下一篇補完 |
| [Bridge pruning／四環混合型](c5_shared_pair_bridge.md) | 可移除任意連通 bridge 側的 singleton 替換，補齊恰四環；一般 cluster 由下一篇補完 |
| [任意 triangle-tree palettes](c5_triangle_tree_palettes.md) | 七介面歸納與閉鄰域 minor，任意 triangles／bridges 圖類只剩互斥至多二環；不需 T4 |
| [長 odd-cycle root（R7）](c5_odd_cycle_roots.md) | 一般需十一介面；拒絕時仍互補 pairs，排除恰一個長環加任意 triangles／bridges |
| [多長 odd-cycle（R8）](c5_multi_odd_cycles.md) | 任意有限長環數的封閉與終止論證；所有長環排除，K4 由下一篇補完 |
| [K4 與全 degree-4 合成（R9）](c5_k4_blocks.md) | 任意外枝 K4 排除，完成全 degree-4 分支；唯一 degree-5 由 [R10](c5_degree5_interfaces.md) 接續 |

R7–R9 是此段研究輪次，不是參考文獻編號。較早 R1–R6 是
[triangle-tree 輪的觀察與路線](STATUS_HISTORY.md)，並非六篇獨立 block 排除報告。

## 4. 可重用介面與不能省略的條件

- **Bridge 與共用點不同。** 刪 bridge 後的兩側都可著色，原圖拒絕才推出
  兩 root 是同色 singleton；共用 cut vertex 的兩側則以 root 集合交集接合，
  不可偷換為獨立 singleton forcers。
- **固定 q 與完整 Σ 不同。** 一般 bridge pruning、palette 吸收與縮環只保留
  原文明列的固定 q／degree／minimality。Triangle 路徑枝的完整 bridge
  介面保持是帶 context 的另證結果；[standalone 反例](c5_root_interfaces.md) 仍有效。
- **Minor 與 minimality 不同。** Boundary 固定 minor 保持 disk，但新 spoke
  的刪邊可著色仍需獨立構造。必須保留實際 boundary attachments、循環次序與
  同一來源圖中的 branch sets，不能只比 list palettes。
- **七介面與十一介面不同。** Triangle 子樹為六個 pairs 加 U；一般長奇環
  還有四種三色集合。不可著色才強迫切口兩側為互補 pairs，不能先刪三色訊息。
- **K4 的最後 boundary 收縮只作非平面證書。** 它識別五個 boundary 點以得到
  K5，並非保留 boundary relation 的壓縮操作。

[ForcingLists.lean](../Math/ForcingLists.lean) 已提供普通 Lean 支援，例如
`bridge_forced`、`forced_palettes`、`cycle_two_lists_uncolorable_iff`、
`triangle_two_lists_uncolorable_iff` 與 `shared_chain_interface`，均在
`FiveBoundary.ForcingLists` namespace；審計入口為
[ForcingListsAudit.lean](../Math/ForcingListsAudit.lean)。
[RootInterfaces 的十五個定理](lean_root_interfaces.md) 支援一般共同接合。
原報告「未新增 Lean theorem」描述當輪整個化約；這些後續共用工具不代表
Gallai 分解、任意來源 minors 或完整 disk 分類已形式化。

## 5. 證書、重播與本次驗證範圍

各篇同名 `scripts/c5_<主題>.py` 與 `artifacts/c5_<主題>/observations.json`
是 checker／產物入口；實際依賴及控制範圍以報告的重播節為準。例如：

| 化約端 | Checker | 既有證書 |
| --- | --- | --- |
| 樹 | [c5_tree_cores.py](../scripts/c5_tree_cores.py) | [observations](../artifacts/c5_tree_cores/observations.json) |
| 單 triangle | [c5_triangle_forks.py](../scripts/c5_triangle_forks.py) | [observations](../artifacts/c5_triangle_forks/observations.json) |
| 兩 triangles | [c5_two_triangle_blocks.py](../scripts/c5_two_triangle_blocks.py) | [observations](../artifacts/c5_two_triangle_blocks/observations.json) |
| 任意 triangle tree | [c5_triangle_tree_palettes.py](../scripts/c5_triangle_tree_palettes.py) | [observations](../artifacts/c5_triangle_tree_palettes/observations.json) |
| 多長環 | [c5_multi_odd_cycles.py](../scripts/c5_multi_odd_cycles.py) | [observations](../artifacts/c5_multi_odd_cycles/observations.json) |
| K4／合成 | [c5_k4_blocks.py](../scripts/c5_k4_blocks.py) | [observations](../artifacts/c5_k4_blocks/observations.json) |

合成報告列出的重播入口如下；這不是完整依賴全部重跑的宣告：

```bash
uv run --with networkx==3.5 python scripts/c5_k4_blocks.py --check
uv run --with networkx==3.5 python scripts/c5_multi_odd_cycles.py --check
uv run --with networkx==3.5 python scripts/c5_tree_cores.py --check
uv run --with networkx==3.5 python scripts/c5_triangle_forks.py --check
uv run --with networkx==3.5 python scripts/c5_two_triangle_blocks.py --check
lake build
```

Python 的 planarity oracle、保存的 subdivision／minor branch sets 與純 list
枚舉各有不同信任範圍。例如早期 triangle 接枝仍用 NetworkX planarity 核對，
不應一律說成逐例已保存拓撲路徑證書。歷次實際重跑／沿用範圍見原報告及
[研究歷史](STATUS_HISTORY.md)；本次只整理文件，未重跑研究 checker 或 Lean build。
文件檢查：`python3 scripts/check_docs.py`、`git diff --check`。

## 6. 對後續問題的精確含義

若來源 `Σ(G)=Ω\{p,q}` 有一個全 degree-4 的 minimal q-obstruction，
依上述前提它只拒絕 q，沿刪邊路徑的 first strict step 因而只釋放 p。
反過來，該單側出口若失敗，每個 minimal q-obstruction 都必含完整
degree≥5 內點；交換 p、q 同理。兩個單側結論不推出共同 pivotal edge。

唯一 degree-5 的多接點分量不能直接套整圖的全 degree-4 結論，須使用
[degree-5 導讀](c5_degree5_guide.md) 的共同關係與來源 minors。
[雙拒絕 sector 分類](c5_two_rejection_proof_zh.md) 與
[3703 必要鏈結構](c5_sector_3703_structure.md) 另有 degree≤4、b0 接點及多列
條件，也不能僅由本系列固定 q 的結論代替。
一般單側／共同出口、候選 A 與 `K∞=K≤5` 仍未證。
