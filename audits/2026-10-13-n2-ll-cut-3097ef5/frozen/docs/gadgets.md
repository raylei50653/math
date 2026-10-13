# 從 primitive constraints 反向合成 boundary relation

2026-09-11。這一階段不再擴大無結構的 n-vertex 枚舉，而是選定有限 gadget grammar，指定 exact target `T4` 再合成。未使用四色定理、SAT 的不透明結論或 boundary-state conjecture。

## 三種信任分類

* **proved in Lean**：relation 的交集、串接、隱藏變數定義；串接結合律與 identity；graph relation 的 S4-equivariance 及其在串接／交集下保持；NEQ、EQ、frame exclusion、frame force 的 exact 染色規格；shared / independent frame 區別；42 份 library exact Σ 證書；10 份 target 的 exact `Σ=T4`；五份三角形排色衝突證書。
* **computationally observed**：有限 grammar 的枚舉完整性、7,194 張 disk 測試通過、42 states 的搜尋完備性、有限 grammar 下最少 26 邊、planarity／ports cofacial 測試、決定性重現。這些不是 Lean 拓撲或全域最小性定理。
* **conjectured / unresolved**：什麼額外 embedding-interface 資料足以讓 quotient 保持幾何可接線性；更一般 grammar 的 closure／有限 frontier；單側 disk 的無界結論與 closed SCC。沒有將它們當成已證前提。

Lean 大部分有限染色驗證使用 `native_decide`，包含原生編譯信任。一般 relation laws、pigeonhole rejection 及 checker soundness 是普通證明；五份具體 pigeonhole 證書使用 `decide +kernel`。不把所有結果稱為純 kernel reduction。

## Primitive 規格與接線陷阱

| Primitive | 圖 | Exact relation | 同面 port 測試 |
| --- | --- | --- | --- |
| NEQ(x,y) | 一條邊 xy | x≠y，共 12 組 | 通過 |
| EQ(x,y) | x,y 共同鄰接一個 K3，即 K5−xy | x=y，共 4 組 | 不通過 |
| frame exclusion | K4[A,B,C,D]，x 鄰接 A,C | x∈{B,D}，共 48 組五元組 | 五個 ports 不同面 |
| frame force | K4[A,B,C,D]，x 鄰接 A,B,C | x=D，共 24 組五元組 | 五個 ports 不同面 |

所有這些圖本身通過平面性檢查，但「平面」不代表「可當 disk 接線元件」。EQ gadget 尤其直接：若 x,y 同面，就可以加邊 xy，得到 K5。它能強迫相等，卻不能直接當成兩個外露同面 terminals 的 disk wire。這是此具體 gadget 的限制，沒有聲稱已證所有 equality gadgets 都不可能同面。

K4 frame 的四個 reference vertices 本身也不能全部同面；加入共鄰接 apex 就形成 K5。故不可把它當成免費、可任意扇出的外露四線顏色匯流排。

Frame 只是 `Equiv.Perm Color` 表示的相對座標。Lean 檢查：

```text
∃ 同一個 frame f, x=f(D) ∧ y=f(D)    iff x=y
∃ 各自的 frame f,g, x=f(D) ∧ y=g(D)  對任何 x,y 都成立
```

後一個不是前一個；隱藏 frame 前必須明確指定是否共用。無預染色的 graph relations 仍對整體 S4 作用封閉。

這不推翻先前固定 boundary labels 的十-bit S4 無損壓縮：共用 frame 與獨立 frame 是不同的接線／存在量詞規格，不是同一個 exact Σ 的兩種任意解讀。

## 第一個有限合成 grammar

每個 component 固定為：

```text
有序 induced C5 + 內部 K3[5,6,7] + 任意 boundary-to-K3 edges
```

15 條可能接線，共 `2^15=32,768` 個 conjunction-of-exclusions 程式；沒有 boundary chords。直接以每個 boundary pattern 下三角形的 24 種互異 assignment 計算 relation，不用隨機生成圖。允許少接線或 disconnected interior，這是 grammar 的明確範圍。

| 搜尋項目 | 結果 |
| --- | ---: |
| 全部 attachment sets | 32,768 |
| disk 必要邊數上界內 | 22,819 |
| apex-planarity disk 測試通過 | 7,194 |
| 不同 labeled Σ | 42 |
| 單一 component 的 Σ=T4 | 0 |
| unordered state pairs，含自配對 | 903 |
| intersection 恰為 T4 | 10 |

10 組目標各輸出一個最省邊的實現：5 個為 11 頂點／26 邊，5 個為 11 頂點／27 邊。兩側 interior disjoint，只共享相同 ordered C5。每張候選都輸出 deterministic certificate，Lean 不信任搜尋器而重算 exact Σ。

這裡最少 26 邊的範圍是「兩個此 grammar 的 disk-tested components、獨立內部、aligned intersection=T4」；不是所有 planar graphs 的最少邊結論。每個 component 的頂點數固定 8，兩個黏合固定 11，未做全域 vertex minimization。

十張代表圖都 planar，但指定 C5 都不 cofacial。**這個測試只針對每個 state 的選定最省邊實現，不代表窮舉了同 Σ 的全部幾何實現。** 只為染色 target／邊數最佳化時保留最便宜 state witness 是安全的；若還要求任意未來的 disk 接線可行性，不能未經證明地做同樣 pruning。

## 合成器產出的可讀排除證書

最省邊的決定性解具有以下接線。每側自己的三個內部頂點仍編號 5,6,7；黏合時右側改名為 8,9,10。

| 內部頂點 | 左側 boundary neighbors | 右側 boundary neighbors |
| --- | --- | --- |
| 5 | 0,1,2 | 0,1 |
| 6 | 0,3,4 | 0,4 |
| 7 | 2,3 | 1,2,3 |

左右的三色 acceptance sets 分別為：

```text
L: 01021, 01201
R: 01012, 01202, 01212
```

兩側都接受全部五類四色 patterns，因此交集為 exact T4。五個排除原因如下；顏色編號只針對表列 canonical pattern，不是全域固定色名。

| 排除側 | boundary pattern | 必須互異的內部頂點 | 它們合計可用色 |
| --- | --- | --- | --- |
| L | 01012 | 5,6,7 | {2,3} |
| L | 01202 | 5,6,7 | {1,3} |
| L | 01212 | 5,6 | {3} |
| R | 01021 | 5,6,7 | {2,3} |
| R | 01201 | 5,6,7 | {2,3} |

每列都是 pigeonhole 衝突。`TriangleConstraints.lean` 證明一般的「互異頂點數大於可用色數 ⇒ 不可染」並逐列檢查；另檢查這兩個 component 的 constraint formula 與實際 graph checker 一致。`GadgetSynthesis.lean` 將接線綁定到 library 中的實際圖，並證明全部十份 target 證書的語意正是 T4。

因此結果不只是「找到一張 BAD 圖」，而是「L 排除三種 patterns，R 排除另外兩種 patterns」的可讀 constraint circuit。

後續：[Finite-state synthesis of triangle disk gadgets](automata.md) 把本 grammar 的染色與幾何都寫成沿邊界掃描的自動機，並把 `compiled_meaning` 推廣為所有 links 的普通證明。

## 下一步的精確問題

目前已把兩層分開：

1. **染色 relation 語意**：交集與存在量詞串接精確；固定 terminals 下 S4-saturated relation 可以保留位置後壓縮。
2. **可接線幾何語意**：還需要 ports 所在的面、循環順序、內外側以及 frame identification。尚未建立一般圖接線 compiler 的 planar soundness。

候選研究方向是同時保存 relation 與 embedding-interface 資料，再測試這種 signature 是否是 composition congruence。不能先假設某個 cofacial partition 或單一 rotation system 就足夠；同一圖可能有不同 embedding choices。

目前没有定義完整的 topology-aware transition grammar，所以沒有計算或宣稱 closed SCC 的排除結果。

## 檔案與重現

* `Math/GadgetRelations.lean`、`PrimitiveGadgets.lean`：relation algebra 與 primitive exact specifications。
* `Math/GadgetLibrary.lean`：42 個 exact relation certificates，允許 GOOD／BAD／empty 的通用 checker。
* `Math/GadgetTargets.lean`、`GadgetSynthesis.lean`：十個合成目標的 exact T4 證書。
* `artifacts/gadgets/`：library、候選圖、summary、primitive ports、逐 pattern 排除原因。

```bash
uv run --with networkx==3.5 python scripts/synthesize_gadgets.py
python3 scripts/export_certificates.py --split --relation --namespace FiveBoundary.GadgetLibrary --input artifacts/gadgets/library.jsonl --output Math/GadgetLibrary.lean
python3 scripts/export_certificates.py --split --namespace FiveBoundary.GadgetTargets --input artifacts/gadgets/bad_certificates.jsonl --output Math/GadgetTargets.lean
lake build
uv run --with networkx==3.5 python scripts/check_gadgets.py
lake env lean Math/GadgetAudit.lean
```

實際信任依賴記錄於 [lean-audit.txt](../artifacts/gadgets/lean-audit.txt)。其中五份 pigeonhole 證書沒有 native 計算公理依賴；library／target 的完整染色重驗則有，兩者不混用。

驗證完成：`lake build` 通過且無 warning；42 份 library 與 10 份 target 的獨立全染色 replay 通過；primitive port 測試與逐列排除理由重驗通過。完整合成重跑後的 summary、library、候選、explanation、兩份 Lean generated sources 均逐 byte 一致；既有 250 份 exporter 產物不變且回歸 replay 通過。通用 relation checker 另通過 GOOD 正例、漏 coloring 與缺 boundary edge 的拒絕測試。
