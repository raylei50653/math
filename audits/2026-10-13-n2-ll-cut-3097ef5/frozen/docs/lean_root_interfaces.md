# 可重用 Lean 基礎：共同接點、中心接合與共用 root

後續（2026-09-28）：連通 degree-list 的 slack 貪婪引理已由
[TwoRejectionTools](lean_two_rejection_tools.md) 完成；
[BoundaryDegree](lean_boundary_degree.md) 再接上實際附件、完整度數與拒絕迫緊。
下文的全列刪邊解除及完整 minor／disk 形式化仍待補。

2026-09-18。接續既有 `ForcingLists.lean`，將 R10、R17–R23 反覆使用且
語義已定型的接合代數補為普通 Lean 證明。這是基礎形式化，不新增 disk
排除，也不改變 R23 的來源 minor 停止點。

實作：[Math/RootInterfaces.lean](../Math/RootInterfaces.lean)。
命名空間 `FiveBoundary.RootInterfaces`；沿用既有 `ListProper`、`avail`、
`availOn` 與共同四色 `Color`，由 `Math.lean` 匯入。

## 1. 定理與報告對照

| 定理 | 精確結論及用途 |
| --- | --- |
| `not_mem_forbidden_iff` | 完整有序接點關係的禁色投影：同一個 coloring 在每個接點都避開中心色；對應 R10 §1，不能用各接點 marginals 取代 |
| `forbidden_antitone` | 放寬共同關係只會減少禁色，適用關係層的單調性 |
| `mem_forbidden_single_iff` | 單接點拒絕 a iff root 集包含於 `{a}`；含空 root 集的情況 |
| `mem_forbidden_single_iff_eq` | 明列 root 集非空前提後，單接點拒絕 a iff root 集恰為 `{a}` |
| `mem_avail_hub_iff`、`avail_hub`、`listColorable_hub_iff` | 在 `hubGraph` 上，中心完整可用色集恰為 `A \ ⋃ Fᵢ`，整圖可著色 iff 此集非空；對應 R10 §1 |
| `avail_eq_inter` | 任意圖被兩區域覆蓋、交集恰為 `{r}`、每條邊完整位於其中一區域時，root 集恰為兩區域 root 集的交集；對應 R15／R23 的共用點接合 |
| `listColorable_iff_avail_nonempty`、`listColorable_iff_inter_nonempty` | 將完整 root 介面轉成可延拓布林值；此投影不保證可逆 |
| `transfer_empty`、`transfer_singleton`、`transfer_of_two` | 單一步不等色接合：空訊息保持空；singleton 刪除一色；訊息含兩個不同色則下一步恢復整份 list；供外臂／路徑傳遞使用 |
| `private_colours`、`card_le_of_irredundant_cover` | 覆蓋 A 且移除任一 Fᵢ 均釋放 A 中一色時，每個分量有互異 private 色，故分量數 ≤ `A.card`；對應 R10 §4 的組合部分 |

`hubGraph` 的頂點為 `Option (ι × V)`：`none` 是中心，`some (i,v)`
屬於第 i 個分量。各分量的接點索引型別 `Q i` 可不同，也容許重複或
空接點；每份關係都保留單一 coloring witness。定理允許任意索引／
頂點型別；只有計數定理要求分量索引有限。套用既有來源圖時，仍須
給出其分量分解與此模型的對應。沒有自動把 Python 圖轉成 Lean 圖。

`avail_eq_inter` 直接對任意 `SimpleGraph V` 證明，以區域 coloring 在
唯一共用 root 上同色來拼接；不預設兩側可著色、不依賴它們是奇環。
路徑 `transfer` 本身定義為存在相鄰異色的集合運算；未另形式化整條
Python path-profile 遞迴或其 67 種閉包分類。

## 2. 信任範圍與未完成部分

15 個具名定理均為普通證明；axiom audit 僅見 `propext`、
`Classical.choice`、`Quot.sound` 的子集，沒有 `sorryAx` 或
`Lean.ofReduceBool`，不使用 `native_decide` 或外部有限表。

以下仍為原報告的紙面論證／Python 證書，不能因本模組 build 通過
就改標成 Lean theorem：

- degree-4 分量刪除任一 incident edge 後，對全部 boundary rows 解除禁色。
- 上述解除引理與實際 edge-minimality／固定來源圖四開關公式的連接。
- R23 自由 root 奇環至少二色、恰二色 iff 私有 lists 為共同 palette 的剛性。
- 縮環保持四列可延拓與 F、真正 boundary 固定 minor、degrees、minimality 及拓撲合成。

尤其 `avail_eq_inter` 證明的是同一圖的精確接合，**不**宣稱縮環前後
完整 root 集或交集相同。R23 保存的反向控制仍然有效。

## 3. 重播與下一入口

```bash
lake build
lake env lean Math/RootInterfacesAudit.lean
git diff --check
```

形式化輪核對全部新定理的 axiom 輸出及全庫 build；當時未重跑研究 Python
checkers。其後發布輪另重播 R20–R23 checkers，全數通過，見 STATUS §27；
未重跑 R15／R17／R19 大型拓撲覆蓋，既有 scripts／artifacts 不變。

後續 Lean 可先補一般連通 degree-list 的 slack 貪婪引理，再推導 R10
全列刪邊解除；R23 圖層研究仍按 [HANDOFF §2](HANDOFF.md) 推進。
一般 degree-5、共同出口與 `K∞=K≤5` 未解。本次與 R21–R23 一併發布。

後續狀態（2026-09-18 文件盤點）：R23 來源 minor 缺口已由
[R24](c5_degree5_shared_cycle_minors.md) 補完；目前圖層停止點移至
[R31 同末端型](c5_degree5_same_terminal_triangles.md) 的任意長來源 minors。
上述 Lean 待補項仍保留，未因 R24–R31 的紙面／Python 成果而完成。
