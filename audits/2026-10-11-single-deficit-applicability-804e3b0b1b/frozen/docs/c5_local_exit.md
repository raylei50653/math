# 四度 boundary singleton 的局部出口

2026-09-15。接續 [替代出口](c5_alternative_exit.md)。
**一般引理有下述紙面證明，未 Lean 化；固定圖實例為 Python 計算證據。**

## 1. 結果

boundary 為 `(C,D,C,A,B)`，若位置 3 的 degree 為 4、鄰居全用 B/C，
直接交換 singleton component `{3}` 的 A/D，即得 `(C,D,C,D,B)`，唯一色位置為 4。
這個操作完整保留 D₁₂；另外兩系統各自最多增減一個 cycle。因此：

- `χ(after) ≤ χ(before)+2`。
- 增量不可能是指定禁用型 `[-1,0,2]` 的排列。
- 若起點 `χ≤2`，這是一條峰值≤4 的直接成功路徑。

這給出了不需要舊引理完整 quotient shapes 的另一個操作。
未證明舊 AD@1 操作的前提 1–2 能推出其前提 3–4；本輪選擇的是 **AD@3**。
不要求 cut 恰為大 component 的 path、不要求另一條保留 cycle 存在，
也不要求 retained graphs 是 forests。

既有 R 的 48 個狀態全滿足這個局部條件與 `χ=2`。在整個既有 5,952-state
閉包中，符合上述 ordered boundary 型的來源有 384 個，其中 96 個滿足局部條件；
這 96 個的角色化 cycle 向量全為 `(1,0,1)→(1,1,2)`。
全色角色同時作用於完整來源和三套系統；原頂點、邊、face 編號不變，沒有合併狀態。

## 2. 四條 cut 邊的 retained owner 公式

色角色固定為 `A/B/C/D=0/1/2/3`，edge type 是兩端顏色 XOR。
令 `P=δ({3})`。在三角化 disk 的 boundary 四度頂點，其 incident faces 是一個
三面 fan，P 在 split dual 中形成以下四邊 path：

```text
terminal 2 --type 2-- a --type 1-- b --type 2-- c --type 1-- terminal 3
```

terminal i 位於 boundary edge `(i,i+1 mod 5)`。
這裡 a、b、c 是三個 incident faces，並非原圖的顏色或 boundary vertices。
鄰居沿 fan 相鄰且只用 B/C，properness 迫使它們交替，因此 edge types 如圖。
交換 `{3}` 在 P 上互換 type 1、2；type 3 和非 cut 邊不變。

對 X=D₁₃、Y=D₂₃，分別從來源刪除 P，得到 retained graph H_X、H_Y。
**使用全部 dual vertices，保留 isolates、loops、parallel edges。**
以 `u ~_X v` 表示兩個 face 在 H_X 同一連通塊，Y 同理。
定義四個來源布林值：

```text
L_X = [a ~_X b]       R_X = [b ~_X c]
L_Y = [a ~_Y b]       R_Y = [b ~_Y c]
```

則有精確公式：

```text
cycles_X(before) = β(H_X) + L_X
cycles_X(after)  = β(H_X) + R_X
cycles_Y(before) = β(H_Y) + R_Y
cycles_Y(after)  = β(H_Y) + L_Y

ordered Δcycles = (0, R_X-L_X, L_Y-R_Y).
```

`β(G)=|E|−|V|+#components` 是 multigraph 的 cycle rank。
對本研究的 dual systems，每個非孤立分量都是 path 或 cycle，故 β 正是 cycle 數。

### 公式的紙面證明

先收縮 H 的各連通塊，使用
`β(H∪A)=β(H)+β((H∪A)/H)`。此等式可直接代入邊數、頂點數和分量數得到，
不需要 H 是 forest；收縮只將 H 的邊移入 β(H)，A 的 loop／平行邊仍保留。

在 X 的 old 接線中，只補回 `ab` 和 `c–terminal 3`；new 接線則補回
`terminal 2–a` 和 `bc`。兩個 terminal 在 H 中都是 isolates。
因此每次補回的 terminal 邊都只連接一個新孤立點，對 β 沒有貢獻。
剩下唯一一條邊恰在兩端已有共同 retained owner 時成 loop，貢獻 1；否則貢獻 0。
這給出 X 的兩式。Y 的 old/new 接線恰相反，得到另兩式。證畢。

每個布林差都在 `{-1,0,1}`，所以總增量≤2，而且沒有任何系統能增加 2。
故不會出現禁用型 `[-1,0,2]`。這個局部論證不依賴各系統獨立接線可被同一圖實現：
實際使用的是同一 cut、同一來源的兩個 retained graphs。

checker 額外對 a,b,c 的全部 5 種集合分割逐一計算 multigraph β，再對兩套系統
的 25 種分割組合核對公式。這是公式的有限 sanity check；包含可能無法由 disk
實現的組合，不當成一般幾何 soundness 證明。

## 3. 局部出口引理

**紙面引理，未 Lean 化。** 設有限三角化 disk 有 proper 四染色，ordered C5
boundary 是 `(C,D,C,A,B)`。假設 boundary 位置 3 有四個鄰居，且全用 B/C。
dual 採用本研究的 boundary split terminals；三個 incident faces 形成 §2 的 fan。
則 AD@3 是合法 boundary-root 操作，直接到 singleton-4，完整保留 D₁₂，
另兩系統增量各在 `{-1,0,1}`；若起點 χ≤2，則此操作是峰值≤4 的禁補償成功路徑。

**證明。** 位置 3 使用 A，但鄰居均不用 A/D，因此 `{3}` 本身就是 maximal
AD component。交換後仍 proper，boundary 明算為 `(C,D,C,D,B)`。
cut 上沒有 type 3；type 1、2 互換，故 D₁₂ 的完整邊集與分量都保留。
§2 的四邊 path 與 owner 公式給出剩餘計數和禁用型排除。
成功路徑僅此一步，含起終點的最大 χ 不超過 `χ(before)+2≤4`。證畢。

若離開三角化 disk 語境，也可以直接以前述四邊 dual path、端點為 retained isolates、
proper singleton swap 及 dual systems 為 paths/cycles 作組合前提；公式證明不變。
這裡未建立 Lean disk embedding 或 topology soundness。

## 4. 固定圖的實體邊與回放

anchor 仍為原色來源 3022。AD@3 只將頂點 3 的 A 改成 D：

```text
3022 --AD@3, component={3}--> 1112 (singleton-4)
χ: 2 → 4
ordered cycles: (1,0,1) → (1,1,2)
```

其 dual path 按 terminal 2 到 terminal 3 排序為：

```text
39 --e13--> 8 --e20--> 18 --e19--> 7 --e18--> 40
```

39、40 是 terminal dual vertices，a=8、b=18、c=7 是 face IDs。
cut 的原圖邊是 `e13=(2,3), e20=(3,20), e19=(3,7), e18=(3,4)`。
來源 retained owner 關係為：

| 系統 | 左側 a,b | 右側 b,c | retained β | Δcycles |
|---|---|---|---:|---:|
| X=D₁₃ | 不同塊 | 同塊 | 0 | +1 |
| Y=D₂₃ | 同塊 | 不同塊 | 1 | +1 |

這是兩次新的閉合，Y 原有 cycle 完整留在 H_Y。
舊 AD@1 出口為 `3022→1027`、增量 `(0,2,0)`，涉及舊 cycle 轉移；
本輪 AD@3 的局部公式適用於不同操作，沒有把兩個出口當作同一個重接。

`local_source(model,c)` 僅讀圖和完整來源，先建立 path、retained owners、預測增量；
之後才查轉移表並獨立交換、重算目標系統、核對 Goal 與 χ。
全部 96 個來源皆通過，其中覆蓋完整 R 的 48 個 ID。
R 外的另 48 個只用來核對來源引理，沒有聲稱它們同屬 R 或需要峰值 4。

## 5. 研究判斷與下一個缺口

對 R 的峰值≤4 直接出口，四度 singleton 是較短的來源充分條件；不需要再用
大 component 的 hexagon 形狀來保證這一存在性。舊完整重接報告仍解釋 AD@1。

接下來值得研究的是：在沒有這種 boundary singleton 的障礙區域，何種等高
boundary-root 操作能形成它，或是否需要另一種局部出口。
目前沒有證明一般障礙區域可到達四度 singleton，也沒有證明任意 disk 具有四度
boundary 頂點。沿固定圖做 Kempe swaps 不會改變度數，因此本規則的適用範圍明確。
一般 K=4 策略及 `K∞=K≤5` 仍未證。

本輪沒有新增圖或重搜閉包；沒有修改既有 transition grammar、Goal 或舊證書。

## 6. 重現

- [checker](../scripts/c5_local_exit.py)
- [證書](../artifacts/c5_cells/local_exit.json)：原始 cut 邊、retained blocks、來源 owners、
  96 筆完整回放索引與來源 SHA-256；state IDs 由 hashes 綁定。

```bash
uv run --with networkx==3.5 python scripts/c5_local_exit.py --check
uv run --with networkx==3.5 python scripts/c5_alternative_exit.py --check
uv run --with networkx==3.5 python scripts/c5_strategy_no_comp.py --check
lake build
git diff --check
```

驗證：以上三個 checker 的 `--check`、`lake build`（僅既有 lint）、新報告與
交接連結及 whitespace 檢查均通過。程式、證書與報告隨本次交接一併提交；沒有待完成驗證或背景工作。
