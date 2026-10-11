# 實際邊界接線與 degree-list 緊性的 Lean 基礎

2026-09-28。接續 [雙拒絕工具的依賴表](lean_two_rejection_tools.md)，補齊
「實際圖 → 剩餘 lists → degree-list 前提 → 拒絕迫緊」這一層。
實作為 [BoundaryDegree.lean](../Math/BoundaryDegree.lean)，已由
[Math.lean](../Math.lean) 匯入；命名空間 `FiveBoundary.BoundaryDegree`。
研究優先序仍見 [HANDOFF](HANDOFF.md)。

## 1. 前提與同圖語義

來源是任意有限簡單圖 `G : SimpleGraph (B ⊕ V)`，`B` 為具名邊界頂點，
`V` 為內部頂點；二者是完整、不交的頂點分割。`interiorGraph G` 直接由
G 限制到 V，`attachments G v` 直接讀取 v 在 G 的 B 鄰點，並非另給的
數字或附件表。固定同一個 `q : B → Color`，其中 `Color = Fin 4`，定義

```
A(v) = {b ∈ B : G 中有 vb 邊}
L_q(v) = U \ q(A(v))
deg_G(v) = deg_V(v) + |A(v)|。
```

不要求 B 是 C5、G 平面、disk 嵌入或 minimal obstruction。邊界可有弦；
`BoundaryProper G q` 明確要求 q 尊重所有實際 B–B 邊。
`Extends G q` 是整張 G 的同一份 proper coloring 在每個具名 B 點等於 q。
`extends_iff` 把它精確等價為 boundary properness 與內圖 list 可染的合取，
因此不會把一個本來就違反框邊的 q 誤當成內部拒絕。

緊性及其延拓推論另要求 **V 誘導圖連通、每個 V 點在完整 G 的 degree≤4**。
連通性不可省略：某分量的 slack 不能替另一個拒絕分量解套。
單點內圖也涵蓋；空內圖可用延拓等價，但不滿足緊性定理的 Connected 前提。

## 2. 具名定理

| 定理 | 精確結論 |
| --- | --- |
| `mem_attachments`、`mem_lists_iff` | 鄰點與 list membership 都由實際 G 邊給出；可用色恰與每個邊界鄰點的 q 色不同 |
| `proper_sum_iff`、`extends_iff` | 固定框列後，完整 coloring 與同一份內部 list coloring 精確接合 |
| `degree_split` | 完整 degree 恰為內部 degree 加實際邊界鄰點數；沒有把等色鄰點合併 |
| `card_lists_add_image` | `card(L_q(v)) + card(q(A(v))) = 4`，由四色補集推出 |
| `degree_le_card_lists` | 完整 degree≤4 自動給出每點 `deg_V(v) ≤ card(L_q(v))` |
| `tight_of_rejection` | 連通且完整 degree≤4 的內圖拒絕 L_q 時，每點完整 degree=4、list 大小等於內部 degree，且 q 在該點的實際 A(v) 上單射 |
| `tight_of_not_extends` | 在 q proper 的前提下，由原圖拒絕延拓直接取得上一列三個結論 |
| `listColorable_of_degree_lt_four`、`extends_of_degree_lt_four` | 同樣的連通／上界下，只要一點完整 degree<4，內圖即可染；q proper 時延拓到原圖 |
| `listColorable_of_repeated_boundary_colour`、`extends_of_repeated_boundary_colour` | 同樣前提下，一個內點若碰到兩個不同但 q 同色的邊界點，即有足夠 slack 可染；q proper 時給原圖延拓 |

證明沿用 `TwoRejectionTools.lists_tight_of_rejection` 的連通貪婪論證。
`degree_split` 先把實際鄰點集拆成兩個互斥部分，四色補集與 image 上界再給
degree-list 條件；拒絕後等號迫使 image 與 attachments 同基數，最後由
`Finset.card_image_iff` 得到單射。沒有使用外部 degree-list 結構定理。

## 3. 已補部分與剩餘界線

這補齊 [雙拒絕分類 §1](c5_two_rejection_proof_zh.md#1-拒絕列使所有-lists-緊並得到-block-palettes)
在進入 Gallai 定理**之前**的圖／list 連接。原工具的純數值
`tight_of_no_slack` 現在有從同一實際圖產生全部前提的呼叫入口。
對 B=`Fin 5`，本模組 lists 與既有 `TwoSpokeReflection.boundaryLists`
在 A=`attachments G` 時是同一個四色補集公式。

若要套到 degree-5 報告的單一分量 C，可以把所有外部頂點（包含 z）放入
B，固定其顏色後使用 `tight_of_rejection`；這個 list 層定理不要求外部
q proper。必須保留 C 的全部實際外鄰邊，並證 C 連通及 C 內每點的完整
degree≤4；不能將 z 的 degree=5 當作符合內點上界。

來源以其他頂點型別表示時，仍需給出其 `B ⊕ V` 重新標記及對應圖；
本輪沒有把 Python 圖、disk embedding 或具名研究來源自動匯入 Lean。
Gallai blocks／palettes、block-cut tree、bridge-chain 抽取、刪邊解除的完整
定理、Jordan 次序、來源 minors、雙拒絕完整分類仍未由本模組形式化。
single-spoke 的 root palette 歸納與 record 15 的研究停止點也未變。

## 4. 重播與信任範圍

```bash
lake build
lake env lean Math/BoundaryDegreeAudit.lean
lake env lean Math/TwoRejectionToolsAudit.lean
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

[Audit](../Math/BoundaryDegreeAudit.lean) 列出本模組全部 13 個定理的公理依賴，
本輪輸出全部僅有 `propext`、`Classical.choice`、`Quot.sound`，沒有
`sorryAx`、`Lean.ofReduceBool` 或外部定理公理；實作不使用 `native_decide`。

本輪 `lake build` 通過（8,827 jobs），新模組沒有警告；舊
`AttachmentOrder`／`SymRelabel` 的既有 linter 警告保留。新模組及
`TwoRejectionTools` 的兩份 axiom audit、文件檢查、DocGraph 檢查與
`git diff --check` 均通過。未改動或重跑 Python 研究證書、大型枚舉、
minor 控制及 profiles／閉包。
