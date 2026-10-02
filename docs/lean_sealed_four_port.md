# D₁₃ 完整四接點與密封替換的 Lean 證明

**2026-10-02 具名實例後續：** [NamedRepair](lean_named_repair.md) 已形式化
兩個十五點核心的原圖 J、指定兩框 P、全部 W／C、各15組極小 repairs、
唯一最少對與 r*=4。下文保留當輪界線；四個退化圖、disk 框完備性與
D₁₃ 替換來源族仍未形式化。


2026-10-02。接續 [D₁₃ 紙面與 Python 證書](c5_two_vertex_repair_caps.md)，
將局部具名關係及外部染色保留接成普通 Lean 定理。
實作為 [SealedFourPort.lean](../Math/SealedFourPort.lean)，命名空間
`FiveBoundary.SealedFourPort`；22 個 theorem 全部列入
[公理審計](../Math/SealedFourPortAudit.lean)，由 [Math.lean](../Math.lean) 匯入。
目前停止點見 [Lean 導覽](lean_guide.md)及[兩點重疊導覽](c5_two_vertex_overlap_guide.md)。

## 1. 原圖、具名框與完整接受關係

沿用原 D₁₃ 的點 `0,…,12`、32 條無向邊，以及順序固定的接點
`0,1,2,3`。`capEdges` 逐邊與既存 artifact 相同；`wheelEdges` 是同一
四環加中心 `4` 的八條邊。兩者皆使用既有 `graphOfEdges` 及 `Proper`。
`proper_graphOfEdges_iff` 在無 loop 前提下證明逐條原邊檢查與真正
`SimpleGraph` proper coloring 等價，並非另設未連到圖的接受表。

對 `b : Fin 4 → Fin 4`，`Extends edges ports b` 定義為：存在一份
完整 proper coloring `c`，在每個具名接點上逐一等於 `b`。
內點全部由同一份 `c` 量化，不各自換色或拼接不同 witnesses。

主定理 `cap_extends_iff` 及 `wheel_extends_iff` 各自證成：

```text
Extends b ↔ b0≠b1 ∧ b1≠b2 ∧ b2≠b3 ∧ b3≠b0
              ∧ ∃ missing : Fin 4, ∀ i, b i ≠ missing
```

也就是 proper 且使用至多三色的四框。`cap_wheel_equivalent` 將兩式
合成，涵蓋所有具名賦色，包括不 proper 的框；沒有只比軌道個數。

必要方向 `cap_no_rainbow` 沿原邊推導：四色框迫點11用框3色；
點5／12恰分用框0／1色，進而迫點6用框2色、點9用框1色，
使點4的鄰點用滿四色。充分方向保留原三份模板 `0101`、`0102`、
`0121` 的完整內點染色，以實際框色及未用色構造延拓。
兩色框另外選出第四色，所有點共用同一組色名。

## 2. 密封內點與任意外部上下文

`Sealed edges attach outside` 是**完整外部染色的集合**。對任意外部
頂點型別 `X`、同一附件映射 `attach : Fin 4 → X`，及任意共同外部
關係 `outside : Set (X → Color)`，其成員條件為：

```text
x ∈ outside ∧ ∃ inside : Fin k → Color,
  Proper (graphOfEdges edges) (Fin.addCases (x ∘ attach) inside)
```

D₁₃ 取 `k=9`，四輪星取 `k=1`。只有前四個點讀取外部顏色，
其餘點單獨密封量化；`outside` 無法讀取這些內點。
真正圖的應用須將所有跨界接線留在四個接點上；額外接到內點的邊
不在此模型內。若接回四個不同外部點，使用單射 `attach` 即可；
純關係定理本身亦容許重複的附件值。

| 定理 | 結論 |
| --- | --- |
| `extends_iff_sealed_tail` | 全圖延拓 iff 四接點固定、剩餘內點存在；明證 `Fin.addCases` 與原完整 coloring 的對應 |
| `sealed_congr` | 任意兩個完整四接點關係相等，便在同一 `attach` 與 `outside` 下保留整個外部關係 |
| `cap_sealed_replacement` | 將上式實例化至 D₁₃／四輪星；逐份外部染色完全保留 |
| `cap_exterior_observation` | 保留外部關係後，任何外部觀察／投影亦相等；可觀察全部外部點 |
| `cap_center_not_preserved` | D₁₃ 有五點字 `01011`，四輪星無同一五點延拓；舊中心不能升為額外接點 |
| `cap_missing_edge_rainbow` | 刪去原邊4–6即有完整 `0123202121031` 染色，接受四色框 `0123`；完整接線不可省 |

上下文定理不需 `X` 有限、外部平面或外部可染的預先假設；外部關係
可為空，結論仍是精確相等。它保持實際附件及外部共同色框，沒有
將單獨框的存在性延拓當成同一份全域延拓。

## 3. 證據層、驗證及剩餘界線

22 個 theorem 無 `sorry`、新增 `axiom` 或 `native_decide`。
小型四色窮盡、未用色存在、原邊合法性及固定反例使用 `decide` 的
kernel reduction；其餘由具名推導及明列構造組成。
22 條公理審計至多依賴 `propext`、`Classical.choice`、`Quot.sound`，
不含 `sorryAx` 或 `Lean.ofReduceBool`。實際驗證見
[研究紀錄](history/2026-10-02-lean-sealed-four-port.md)。

原 D₁₃ checker 本輪重播，8圖、11,520份完整延拓、88份稀疏延拓及
16項負控制通過，artifact bytes 未改。其 `new_lean_theorem=false`
保留原生成輪次的意思；新 Lean 層由本報告及模組另行記錄。

本輪沒有形式化原 face／rotation 證書、disk 嵌入、全部可用框、
兩來源 ownership、任意層數族的圖結構不變量，或 J/P 與 W／C 的具體
前提。因此尚不能把兩個非平凡來源各十五組 repairs、`r*=4` 或來源
族稱作端到端 Lean theorem。一般後繼、多步充分性、一般共同出口與
`K∞=K≤5` 仍未證；沒有使用四色定理。

下一個可分離接口是將具名來源 J/P、附件及 W／C 實例接到既有
[CommonRepair](lean_common_repair.md)；幾何框可用性仍須獨立形式化。

## 4. 重播

```bash
python3 scripts/c5_two_vertex_repair_caps.py --check
lake build
lake env lean Math/SealedFourPortAudit.lean
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

未重跑其他來源替換族、大枚舉、共同 repair Python checker 或其他
Lean 模組的獨立 audit；沒有更新工具鏈或重新生成 artifacts。
