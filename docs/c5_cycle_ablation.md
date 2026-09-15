# Cycle-count ablation：三步 witness 與來源連通判準

2026-09-15。固定[半徑 2 corpus](c5_behavior_radius2.md) 的 106 個完整染色，
移除 cycle counts，保留 raw boundary、pairings 與既有實際色框 guarded ψ。
這一輪沒有擴 radius 或圖 catalogue。新一般 iff 已有下述紙面證明，尚未 Lean 化；
有限數字與 witness 是 Python 證書證據。

## 1. 消融確實產生可比較的不同染色

令 `S⁻=(boundary,pairings,ψ)`，ψ 的不適用仍記 `None`。

| 摘要 | 桶數 | 同桶不同染色 pairs | 最短深度 2 | 最短深度 3 |
|---|---:|---:|---:|---:|
| S（含 cycles） | 106 | 0 | 0 | 0 |
| S⁻ | 84 | 24 | 21 | 3 |
| S⁻ + 本輪 guarded χ | 87 | 20 | 20 | 0 |

S⁻ 桶大小分布為 64 個單點、18 個雙點、2 個三點。
最短深度限固定 30-action boundary-root grammar，observable 是 escape 加 illegal。
深度 3 的三對中：**兩對是兩側皆合法、escape 布林值不同；一對是 legality 分歧**。
兩對合法 escape witness 同屬一個共同全域換色 pair orbit；包含 legality witness
則有兩個 orbit。沒有把三對當成三個新機制，也未用 orbit key 合併遍歷狀態。

cycle counts 對 `(boundary,pairings,ψ)` 提供額外的未來行為辨識力；
**這不證明 cycle counts 是任何充分狀態的必要欄位。**

## 2. 選定的合法三步 witness

A/B/C/D 對應 0/1/2/3。兩個 source 的 boundary 都是 `(A,C,D,A,B)`，
ψ 都為 true，三組 pairings 都是
`(((0,4),(1,3)), ((1,4),(2,3)), ((0,2),))`。
cycles 分別是 `(1,1,1)` 與 `(0,1,2)`（總數甚至相同）。完整頂點 0..21 染色：

```text
x = (0,2,3,0,1,3,2,3,1,1,2,3,2,1,0,0,2,3,1,3,2,0)
y = (0,2,3,0,1,3,2,3,3,3,2,3,2,1,1,0,2,3,1,0,2,0)
w = AB@0; AC@1; AD@1
```

| 已執行 | x boundary | y boundary | 結構觀察 |
|---|---|---|---|
| 空詞 | A C D A B | A C D A B | cycles 已不同；pairings、六色對 boundary partitions 相同 |
| AB@0 | B C D B A | B C D B A | pairings、六色對 boundary partitions 仍相同 |
| 再 AC@1 | B A D B A | B A D B A | pairings 與 boundary connectivity 首次分歧 |
| 再 AD@1 | B D A B D | B D A B A | singleton-2（非 escape）／singleton-1（escape） |

「首次分歧」在此指上述 boundary 連通觀察；完整染色、cycles 與第一次選中的
內部 component 本來就不同，不能說結構直到第二步才開始不同。

第二步後 AD 的 boundary partition 是 `{1,2,4}`／`{1,2},{4}`；BC 的 partition
也從 `{0},{3}`／`{0,3}` 看出差異。第三步的 component 在兩側各自重新計算。
選定詞對兩側都合法；另用 NetworkX 獨立實作 maximal-component swap 與 boundary
multiplicity observable，核對所有長度 0、1、2 的 **931 個詞**皆不區分，再驗證
上述三步詞確實區分。最短性不只依賴原 Explorer 的 BFS。

## 3. 一般三步 iff：從 source 計算

以下色框是變數，不是上一節固定 A/B/C/D 的命名。設 G 是含指定 C5 的任意圖，
c 是 proper 四染色，五個相異 boundary 頂點依次為

```text
(a,b,s,a,d), 其中 a,b,s,d 互異。
```

用 `V_t` 表示 source 中顏色 t 的頂點集。全部從 source 定義：

```text
K  = Comp_{a,d}^c(0)
A₁ = (V_a \ K) ∪ (V_d ∩ K)
H  = A₁ ∪ V_b
L  = G[H] 中包含 1 的 component
U  = V_s ∪ (A₁ \ L) ∪ (V_b ∩ L)
χ(c) = [1 ↔ 4 in G[U]].
```

**Guard**：`K ∩ boundary = {0,3,4}` 且 `L ∩ boundary = {1}`。
特別注意第二個 trace 是 `{1}`，不包含 4。
指定詞是

```text
(a,d)@0; (a,b)@1; (a,s)@1.
```

在 guard 下，有一般結論：

\[
\boxed{\text{指定三步到達 singleton-1}\iff\neg\chi(c).}
\]

χ=true 時恰為 singleton-2，所以對本研究的 forbidden singleton-{1,3,4}
而言也有 `escape iff ¬χ`。

### 紙面證明

第一次交換後 a 色頂點恰為 A₁，b、s 色頂點不變，因此第二次操作選中的 component
正是來源定義的 L。第一個 trace 給 boundary `(d,b,s,d,a)`。

第二次交換後 a 色頂點恰為 `(A₁ \ L) ∪ (V_b ∩ L)`，s 色仍是 V_s，
所以第三次的 `{a,s}` 誘導子圖恰為 G[U]。第二個 trace 給 boundary `(d,a,s,d,a)`。

第三次 component M 包含 1，也必包含 2：C5 邊 1–2 的兩端目前正是 a、s。
唯一其他可能被它碰到的 boundary 頂點是 4。若包含 4，最終 boundary
是 `(d,s,a,d,s)`，singleton-2；若不包含 4，則為 `(d,s,a,d,a)`，singleton-1。
因此兩方向成立。三次 action 都合法，maximal Kempe swap 保持 properness。
此證明不使用平面性、三角化、dual cycles 或 survivor-811；實際只需上述前提及邊 1–2。

此處是把指定三步的連通問題精確搬回來源的**巢狀查詢**，並非證明它可由目前
摘要自足更新，亦無加速結論。`source_rule` 不執行 swap；獨立 audit 才直接交換，
核對兩個誘導頂點集、components、boundary 與最終 singleton。

## 4. 此 witness 的更局部機制：加入一個頂點是否橋接兩個分量

選定 x、y 的最後誘導集滿足

```text
U_x = W ∪ {12}
U_y = W ∪ {8}
W   = {1,2,4,5,7,9,11,17,18,19}.
```

G[W] 的三個 components 是

```text
P = {1,2}
Q = {4,5,7,11,17,18}
R = {9,19}.
```

頂點 12 在 W 中的鄰居為 `{2,5}`，同時碰到 P、Q；頂點 8 的鄰居只有 `{1}`，
只碰到 P。因此 x 中 1、4 連通，y 中不連通。具體證書為：

- x 的路徑：`1–2–12–5–18–11–4`。
- y 中 1 的完整分量：`{1,2,8}`，不含 4。

這也是一般單頂點加入引理的實例：若 p、q 位於 G[W] 的不同分量 P、Q，且 v 不在 W，
則在 G[W∪{v}] 中 p、q 連通 iff v 在 P、Q 各有一個鄰居。
充分性由兩側分量內路徑接上 v；必要性取一條簡單 p–q 路徑，它必經 v，進入與
離開 v 的兩段分別位於 P、Q。這個引理已有此紙面證明，未 Lean 化。

因此至少對這條三步路線，cycles 的辨識作用可以由明確的來源連通條件取代；
在固定 witness 上還可定位成單一加入頂點的分量鄰接差異。
不宣稱所有同桶 pairs 都有相同 W 或單頂點差異。

## 5. 再細化的效果與限制

以實際 boundary 色框實例化 χ，在 106 個染色中 22 個適用：18 true、4 false。
加入 `None/false/true` 後從 84 桶變 87 桶，同桶 pairs 24→20。

被分開的四對中，兩對合法三步 witness 靠 χ 的 true/false 分開；另兩對（一個
三步 legality、一個兩步 escape）靠適用性 `None` 與 true 分開。
**不能把 guard 不成立當作 χ=false，亦不能把適用性分離說成兩側 iff 的驗證。**
剩餘 20 對都有深度 2 區分詞，故新摘要仍不能安全合併任何這些 pairs。

下一個有界入口是這 20 對的兩步衝突及其來源連通條件；另一項可獨立做的工作是
Lean 化本輪三步 iff。此次停在固定 radius 2、continuation 深度 3，沒有推出 closure、
一般最小狀態、cycle counts 普遍不可刪除，或 K∞=K≤5 的結論。

## 6. 證書與驗證

[checker](../scripts/c5_cycle_ablation.py) 與
[證書](../artifacts/c5_cells/cycle_ablation.json) 保存全部 24 對、最短詞與回放、
選定 pair 的來源歷史、逐步 boundary partitions、完整 cut/retained interfaces、
χ 的來源集合與連通證據、單頂點橋接診斷、剩餘 pairs 及 SHA-256。
來源 corpus 沿用原證書，沒有依新摘要刪除 concrete states。

```bash
uv run --with networkx==3.5 python scripts/c5_cycle_ablation.py --check
uv run --with networkx==3.5 python scripts/c5_behavior_radius2.py --check
uv run --with networkx==3.5 python scripts/c5_behavior_refinement.py --check
lake build
git diff --check
```

以上驗證通過（Lean 僅既有 lint）；本輪沒有新增 Lean 定理。程式、證書與文件隨本次交接提交。
接手入口與剩餘 pairs 的定位方式見 [HANDOFF](HANDOFF.md)。
