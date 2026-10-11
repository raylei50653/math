# 四色 pp-expression 層

2026-09-12。已加入可保存的 pp 公式與完整 relation 求值器，沿用現有同一有序
C5 catalog。這一層的程式與測試結論是 **computationally observed**；尚未建立
pp 語法／求值器的 Lean soundness theorem。既有 R767 Lean 證書不自動證明新程式。

## 語法與語意

入口：[scripts/pp_relations.py](../scripts/pp_relations.py)。採用存在量化前綴加原子
合取的形式：

\[
\varphi(x)=\exists z\;\bigwedge_i R_i(v_{i,1},\ldots,v_{i,k_i}).
\]

JSON 明確列出 `free`、`exists` 和 `atoms`。Free ports 按列出的順序解讀；
所有名稱必須宣告、自由／量化名稱不能重複或重疊。原子內可以重複同一變數，
例如 `NEQ(x,x)` 為無解。空合取為 true；空自由介面的 relation 仍區分 true／false。
沒有隱式 capture 或自動改名，也不提供任意 Python predicate 作為 pp 原子。

語言包含 `EQ`、`NEQ` 與現有 catalog 的 87 個五元 `R{id}`。
`EQ` 是邏輯等式，並不附帶實體 disk equality wire 的承諾。
NEQ 是基本關係名稱，不是公式否定。可表示合取與存在量化；不提供 OR、NOT、
implication 語法。Forcing 是求值後的非空 entailment 查詢，不是另一種 pp connective。

每個 relation 原子表示完整的全域 S4 orbits。求值在**同一個全域 assignment** 上
檢查全部原子，再存在量化隱藏變數，最後輸出自由介面的完整 relation。
每個輸出 orbit 保存一份全部公式變數的 satisfying assignment；這不是各個
catalog gadget 內部節點的染色，後者仍由原始 witness／replay 支持。
不支援固定絕對色名的非 S4-invariant relation。

小型求值器預設最多十個自由加量化變數，超限明確失敗，不回傳部分結果。
這是 evaluator 的成本限制，不是 pp-definability 的大小界。沒有跨 C5 合成搜尋、
圖展開 compiler、最短定義搜尋或 polymorphism 搜尋。

## 可直接重現的例子

```bash
python scripts/pp_relations.py examples
python scripts/pp_relations.py eval artifacts/pp_relations/r767_guard.json --pair b0 b3
python scripts/pp_relations.py eval artifacts/pp_relations/r767_pair.json --pair b0 b3
python scripts/pp_relations.py eval artifacts/pp_relations/r91_meet_r935.json --pair b0 b2
python scripts/check_pp_relations.py
```

`examples` 只重建 `artifacts/pp_relations/` 下五份公式和對應結果；`eval` 只向 stdout
輸出。`check_pp_relations.py` 更新此目錄的 `replay.json`，不重跑原始圖搜尋。

令 \(C=(b_1=b_4\land b_0\ne b_2)\)。獨立 labeled replay 的結果：

| 公式 | 自由變數 | 完整 labeled assignments | 查詢 |
| --- | --- | ---: | --- |
| R767 ∧ C | b0…b4 | 24 | b0=b3 |
| R1023 ∧ C | b0…b4 | 48 | b0、b3 同色異色皆可 |
| ∃b1,b2,b4. R767 ∧ C | b0,b3 | 4 | 恰為 EQ |
| R91 ∧ R935 | b0…b4 | 48 | b0=b2 |
| R767 ∧ EQ(b0,b1) | b0…b4 | 0 | infeasible，不回報 forcing |

第一個公式完整 pattern 為 `01201`；第三個公式是同一 C5 的派生投影。
交集例子完整 patterns 為 `01012`、`01021`。

## 來源與幾何界線

載入 catalog 時核對其記錄的 fan `states.json`／`summary.json`／`replay.json`
SHA-256，並核對每個 entry 的 ordered patterns、ID、mask 與 source 路徑。
結果逐原子保存符號、實際變數接線、catalog hash、entry ID、graph witness mask
及原有的染色／幾何 evidence 描述。這些是**既有證據引用**，不表示本輪重新執行
graph coloring、rotation checker 或 Lean build。

每個合成結果一律標示 geometry unchecked。特別是 R91∧R935：原有
`artifacts/boundary_relations/inside_outside.json` 保存特定真實 union 的幾何證據，
但本公式求值器不因此宣稱其他接線或其他同 Σ witnesses 也合法。
不能從不同原子的 disk witness 推出合取能同側實現。

## 驗證範圍

**Computationally observed：** 106 個公式案例通過獨立完整 labeled assignment
枚舉，checker 用 24 個色置換展開 relation，與 evaluator 的 canonical assignment
路徑分開；另核對所有輸出 witness 和全部 free pair 的非空 forcing。
涵蓋全部 87 個 catalog 原子、自由介面重排、顯式接線旋轉、重複變數、
共享／獨立 existential witnesses、空合取、nullary relations 和 unused 變數。

共享測例 `∃z. EQ(x,z)∧EQ(y,z)` 恰四組同色；獨立測例
`∃z,w. EQ(x,z)∧EQ(y,w)` 接受全部十六組。另以 NEQ 的 `K5-xy` 公式核對
隱藏三角形能定義 EQ，結果仍不宣稱 cofacial geometry。
七個不合法輸入案例確認 fail-closed。五份序列化公式及結果也逐份 replay。
source／artifact hashes 保存於 [replay.json](../artifacts/pp_relations/replay.json)。

**尚未 proved in Lean：** 新 pp evaluator 的一般正確性、任何自動幾何合成 theorem。
下一個可選方向是形式化 pp syntax／denotation 與現有 relation operations 的對應；
若研究幾何，需另定義合法接線 grammar。兩者本輪都未啟動。
