# B₂ guard 的精確判準與來源修復接口

2026-09-15。接續 [singleton 準備策略 §5–7](c5_singleton_preparation.md#5-兩步後綴的來源-connectivity-guard)。
**以下是條件式紙面證明，未 Lean 化；前提在 B₂ 成立是固定圖 Python 證據。**

## 1. 結果與限制

- 固定兩步後綴的 guard 是成功的充要條件，包含 guard 失敗分支的反向核驗。
- BC 修復後的 guard 可完全拉回來源集合計算。在 24 個失敗來源中，修復後
  預測的 AC 誘導圖甚至將位置 2 隔離，不只讓 2、4 不連通。
- 用同一 BC component 的 cut 與 retained owners，得到來源充分條件 P：
  它保證修復後 guard 成立，且 χ **下降 1**。
- 這個 P 仍分別要求隔離與 quotient cycle 條件，**尚未從更小的共同結構推出兩者**。
  不是最小資訊定理，也未證 singleton 準備一般會產生 P。

還有一個影響證據強度的發現：72 個準備後來源，在對完整染色做共同色角色
重命名後只有 **3 種**，每種恰有 24 種色標號；24 個失敗來源全屬其中同一種。
因此 24/24 的修復是單一結構的色置換軌道，不能當作 24 種不同結構的支持。
操作規則仍不查 ID，完整狀態仍保留；這裡的正規化只統計證據的結構多樣性。

## 2. 固定後綴成功 iff guard

沿用 `(A,D,C,A,B)`、`S=Comp_AB(0)` 與來源 W 的定義。AB@0 後
boundary 必為 `(B,D,C,B,A)`，而 AC 誘導頂點集恰為 W。AC@4 只有兩種 trace：

| g(c) | AC@4 boundary trace | 最後 boundary | Goal |
|---|---|---|---|
| 真 | `{4}` | `(B,D,C,B,C)` | singleton-1 |
| 假 | `{2,4}` | `(B,D,A,B,C)` | 四色，否 |

**證明。** boundary 僅位置 2、4 用 A/C，故上述情況窮盡；4 必在其 rooted
component 中，2 是否在其中恰由 g 決定。四色角色互異，所以第二列不可能是 Goal。
因此 `g(c) ↔ Goal(T_AC@4(T_AB@0(c)))`。不需要平面性，也不保證 χ 不增。

## 3. 修復 guard 的來源集合更新公式

以下固定共同角色 `A/B/C/D=0/1/2/3`，令 V_A 等為完整來源色類。
取 `Q=Comp_BC(2)`，先要求其 boundary trace 為 `{2,4}`。
實際 BC@2 交換後 boundary 是 `(A,D,B,A,C)`；共同重命名 B/C 後回到
`(A,D,C,A,B)` 的角色格式。新的色類可以直接從原來源計算：

```text
B* = (V_B ∩ Q) ∪ (V_C \ Q)
C* = (V_C ∩ Q) ∪ (V_B \ Q)
S* = G[V_A ∪ B*] 中含 0 的分量
W* = C* ∪ (V_A \ S*) ∪ (B* ∩ S*)
```

A、D 色類不變。於是有**精確更新公式**：

```text
g(T̂_BC@2(c)) iff 2、4 在 G[W*] 不連通。
```

**證明。** Q 內實際交换 B/C、再全域共同重命名 B/C，故 Q 內角色回到原值，
Q 外 B/C 角色互換，正好得到 B*、C*。代入原 guard 的 S、W 定義即得。
這不是分別重命名不同系統；同一角色映射作用於整份染色。

較強但較簡單的充分條件為 `N_G(2) ∩ W* = ∅`。
trace 前提保證 `2,4 ∈ W*`，而兩頂點相異；位置 2 孤立便保證 guard。
這仍需計算來源的 S*，尚未縮成固定數量的 owner 布林值。

## 4. 同一 cut 的來源成本公式與條件 P

成本部分限於既有三角化 disk／split dual 的設定，使三個雙 type 系統的
非孤立分量皆為 paths 或 cycles，cycle 數等於 multigraph cycle rank β。

令 `F=δ(Q)`、來源 edge type `t(e)=c(u) XOR c(v)`。
BC 的 XOR 為 3；maximality 保證 F 不含 type 3，交換在 F 上互換 1、2。
非 F 邊 type 不变，因此 D12 完整保留。

對 X=D13、Y=D23，取所有不在 F 的來源系統邊為 H_J，保留全部 dual vertices。
收縮 H_J 的連通塊得到 retained owners，並分別補入：

```text
O_J = F 中 t(e) 屬於 J 的邊，兩端改為 retained owners
N_J = F 中 (t(e) XOR 3) 屬於 J 的邊，兩端改為相同 retained owners
```

O_J、N_J 使用全部 owner vertices，保留 loops、parallel edges 與 isolates。
它們都是**來源接線 multigraph**，不讀目標染色或目標 cycle counts。
由 `β(H ∪ E)=β(H)+β(E 在 H owners 上的 quotient)`：

```text
ordered Δcycles = (0, β(N_X)−β(O_X), β(N_Y)−β(O_Y)).
```

這是既有 retained contraction 恆等式的來源版本，不要求 H 為 forest。
一般 swap 也可逐 type pair 用相同公式，checker 對全部 168 個後綴步驟核驗。

### 來源充分引理

定義 P(c) 為以下三個條件的合取：

1. `Q ∩ boundary = {2,4}`。
2. `N_G(2) ∩ W* = ∅`。
3. `β(O_X)=β(N_X)=1`，`β(O_Y)=1`、`β(N_Y)=0`。

則

```text
P(c) ⇒ g(T̂_BC@2(c)) 且 χ(T̂_BC@2(c)) = χ(c)−1。
```

**證明。** 1–2 由 §3 給出 guard；3 與上述成本公式給出角色化增量 `(0,0,−1)`。
共同 B/C 重命名只置換三個系統，因此 χ 總和不變，下降 1 的結論仍成立。
此引理甚至不需要假設原 guard 失敗；將它用於 `P(c) ∧ ¬g(c)` 當然亦成立。

此處的成本條件是完整來源 quotient rank 的明確要求，並非更小的局部幾何解釋。
把隔離與成本並列成 P 提供了可檢查接口，**沒有證明兩個要求互相蘊含，或由
準備前的一組更弱條件自動成立**。也沒有給修復後兩個後綴步驟的一般成本保證。

## 5. 固定 B₂ 核驗

不重搜閉包或最短路；直接讀舊準備證書的 72 個來源及操作序列。

| 核驗 | 結果 |
|---|---:|
| 準備後固定兩步後綴成功 iff guard | 72：48 真、24 假 |
| 失敗來源通過 P | 24/24 |
| 修復後來源公式對照實際 guard 的完整 S、W、分量 | 24/24 |
| 修復後固定兩步後綴成功 | 24/24 |
| 所有後綴步的來源 cut 成本對照實際 dual cycle 增量 | 168/168 |
| 準備後完整來源的共同色軌道 | 3，每個 24 個標號 |
| guard 失敗來源的共同色軌道 | 1 |

唯一失敗角色結構的原頂點資料如下，僅作回放定位，不作 predicate：

```text
Q = {2,4,5,7,11,13,17,18}
S* = {0,3,4,8,14,15,18,21}
W* components = {2}, {4,5,7,11,17,18}, {8}, {9,19}
N_G(2) = {1,3,12,13,14,20}
```

位置 2 的六個鄰居全部不在 W*。修復成本在修復前的共同角色框中為
`(0,0,−1)`；重命名後不能直接逐欄相減，checker 在固定框先核對實際增量。
168 步的回放證實各步 χ 不增，但不把這個有限結果升格成一般後綴成本引理。

## 6. 下一個缺口與重現

下一個有內容的縮減目標是：從更小的 component／cut 接口，推出
`N_G(2) ∩ W* = ∅` 與 §4 的 quotient ranks；或證明更弱、仍能同時保證修復與
不增成本的條件。只把兩項精確計算塞入單一 predicate，尚不足以解釋其耦合。
本輪沒有最小性證明、一般準備保持定理或一般 K=4 定理。

- [checker](../scripts/c5_guard_repair.py)
- [來源接口證書](../artifacts/c5_cells/guard_repair.json)：完整來源集合、retained blocks、
  quotient 接線、72 個 guard 回放、24 個修復、168 個後綴成本與 SHA-256。

```bash
uv run --with networkx==3.5 python scripts/c5_guard_repair.py --check
uv run --with networkx==3.5 python scripts/c5_singleton_preparation.py --check
lake build
git diff --check
```

沒有新增圖、閉包搜尋或 Lean 定理。既有程式與證書保持原樣。

驗證：上述兩個 checker 的 `--check`、`lake build`（8,819 jobs，僅既有 lint）、
`git diff --check`、新檔 whitespace 與報告連結檢查均通過。程式、證書與文件隨本次提交發布。
