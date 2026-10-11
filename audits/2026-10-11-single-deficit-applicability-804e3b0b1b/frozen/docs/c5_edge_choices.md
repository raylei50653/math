# C5 多候選 edge-state：聯合 switch 與結構坍縮

2026-09-15。實作使用者要求的「同時紀錄多個合法相對關係」。
**坍縮在本報告指 switch 後 paths／cycles／區域的重接、合併或消失**；
對候選集合加約束而刪掉分支，另稱「篩選」。

**本輪成果**：已實作 `EdgeModel`、`Branch`、`Choice`；在同一固定 Errera disk 上，
保存兩個起點的全部一步與兩步聯合後繼，並給出一個**局部 BC switch 讓 cycles
減少、前後仍相容**的具體結構坍縮見證。沒有新圖搜尋或新增 Lean 定理。

## 1. 狀態保存什麼

| 物件 | 保存內容 | 用途 |
|---|---|---|
| `EdgeModel` | 固定圖、定向三角面、ordered C5、共同原色框架 | 確認各候選使用同一幾何 |
| `Branch` | 完整染色、起點身份、整條 switch 歷史 | 一個有共同解的候選及到達方式 |
| `Choice` | 多個 branches、起點表、列舉範圍 | 同時保留替代配置 |
| `Choice.view()` | 按 `(w,π12,π13,π23)` 分組，附所有 branch indices | 觀察相對關係，不刪除 witnesses |

完整染色是目前用來保證相對關係共同可實現的**內部見證**；外層可只看聯合關係。
完整 edge types 加一個 anchor 與此等價；每條 transition 都另外以 edge XOR 積分
恢復目標染色，核對與 primal component swap 相同。

[先前 joint incidence 檢查](c5_edge_incidence.md) 也仍發現後繼不足，故本版保留完整 witnesses。

目前不是任意圖的符號求解器。候選關係的完整性只相對於**指定起點、指定深度、
指定操作規則**。同一 `(w,π12,π13,π23)` 下可有多個不同完整見證；
即使顯示只剩一列，也不代表完整配置唯一。

## 2. 可用操作

```python
model = EdgeModel(graph)
choices = Choice.start(model, [c, d], scope="two supplied witnesses")

next_choices = choices.switch()                    # 每個候選的全部單步合法後繼
bc_choices = choices.switch(pair=(1, 2))           # 只選 BC moves
selected = choices.switch(pair=(2, 3),
                          component=(5, 6, 8, 10, 13, 14))
safe = next_choices.condition(lambda b: model.compatible(b.coloring))
yes, no = next_choices.split(lambda b: model.view(b.coloring) == wanted)
status = next_choices.query(lambda b: model.view(b.coloring) == wanted)
rows = next_choices.view()
```

- 每次 `switch` 在**各自當前完整見證**上重新求 maximal components。
- 同一個 switch 可聯合改動多組相對關係，無須拆成獨立 pairing 更新。
- 指定 action 在某分支不合法，該分支不產生這個 action 的後繼。
  直接 `EdgeModel.apply` 非法 action 會報錯。
- 多次 switch 用函數串接；不同色對不能套用舊狀態的 component 清單後假裝同時合法。
- `condition` 在完整 witnesses 上篩選；同時限制多個關係就是同一 predicate 的合取，
  或依次 condition。不能分別找到 witnesses 後把各欄混合。
- `condition` 是目前這一步的篩選，不自動變成未來 invariant；若每步都要求相容，
  必須每次 switch 後篩選。
- 相同完整染色、不同 histories 仍保留，供之後讀取中間條件。
- `query` 的空集合回 `empty`，不以空集合宣稱某條件已強迫。

本輪的 `compatible` 精確指：當前不是 singleton-{1,3,4}，且沒有一步 Kempe move
到達它們。它比 proper coloring 強，但不等於全 class safety。

## 3. 固定兩個起點的多候選研究

起點是原 `edge_states.json/same_class_regression` 的兩個完整 Errera 染色。
兩者同一 embedded disk、同 boundary、同 pairing state，以內部 CD move 相連。

| 階段 | 歷史分支 | 不同完整染色 | 聯合關係列 |
|---|---:|---:|---:|
| 起點 | 2 | 2 | 1 |
| 恰一步 switch | 20 | 20 | 12 |
| 恰兩步 switch | 196 | 119 | 53 |
| 一步後無一步 escape | 16 | 16 | 8 |
| 兩步後無一步 escape，只篩最後狀態 | 132 | 74 | 26 |
| 兩個中間層都無一步 escape | 124 | 72 | 26 |

最後兩列相同的 26 組關係下，實際保留的見證／歷史仍不同。
有 **8 條路徑**最後恢復一步相容，但第一步曾有一步 escape；逐中間狀態檢查會刪去它們。
這沒有說它們是不合法的 Kempe moves，而是沒有滿足指定的整段相容條件。

### 3.1 不可合併來源

兩個起點的一步 successor 關係各有 8 種，其中各有 **4 種**另一個起點不能一步到達。
固定一個只有第二起點可達的聯合 target，再套 condition：20 個候選剩 **1 個**。
它來自 AD `{2}`，同時更新 π13、π23，保留 π12。
若只保留第一起點，同一 target 篩選結果為 0。

這是「新 target 有解，但不能從任意具有相同 pairing 的起點一步切過去」的實例。
checker 用負控制檢查：只按 source pairing 查聯集 transition 會產生虛假接續，
而 `Branch.origin/history` 不允許冒用另一個見證的 move。

### 3.2 不可混合各欄

在恰兩步的結果中，先固定 w，再把三欄 pairings 的各自投影做 Cartesian product，
會多出 **8 列**不在真正兩步後繼關係中的組合。
一個明確例子：

```
w   = (1,2,1,1,3)
π12 = ((0,1),(2,3))
π13 = ((0,2),(3,4))
π23 = ((1,4))
```

每一欄配上這個 w 都分別有實際 witness，但沒有同一個兩步 witness 同時滿足它們。
按 `w → π12 → π13 → π23` 累加條件，分支數為 **11 → 2 → 0 → 0**。
這只證明從這兩個起點恰兩步不可達，**沒有證明它在任意圖或更多步數下不可實現**。

## 4. 結構坍縮：局部 BC switch 消掉一個 cycle，兩端仍相容

從第一個起點，先做 AB component `{0,1,2,9,11,15}`，到達：

```
c = (1,0,1,2,3,2,3,0,3,0,3,0,1,2,2,1)
```

再做 **BC component `{0,5,12,14}`** 的局部 switch，得到：

```
d = (2,0,1,2,3,1,3,0,3,0,3,0,2,2,1,1)
```

這個 component 不含所有 B/C 頂點，故不是全域 B/C 重命名。
其 cut 為 αβ system 的一條完整 path（terminals 0、4），共 14 條邊。

| system | switch 前 | switch 後 |
|---|---|---|
| αβ | paths (0,4)、(1,3)，0 cycles | 完整 system 保留 |
| αγ | paths (0,3)、(1,2)，0 cycles | paths (1,4)、(2,3)，0 cycles |
| βγ | path (2,4)，**2 cycles** | path (0,2)，**1 cycle** |
| 對應 missing-type-1 regions | 4 個 | 3 個 |
| 對應 missing-type-2 regions | 3 個 | 3 個，但分區改變 |
| 對應 missing-type-3 regions | 3 個 | 完整分區保留 |
| 無一步禁止 singleton | 是 | 是 |

βγ 的保留邊交集矩陣（舊 rows 為 cycle、cycle、path；新 columns 為 cycle、path）是
`[[8,1],[5,0],[0,5]]`。一個舊 cycle 的部分保留邊分到新 cycle 與 path，另一個舊 cycle
的保留邊接入新 cycle；因此描述應是**重接後 cycle 數減少**，不是原封不動地刪掉某條圈。

missing-type-1 的舊四區域全部有部分頂點分流，而新三區域都接收多個舊區域的頂點。
這是分裂與合併同時發生，不能只用 `4→3` 當成單純收縮兩個完整區域。
完整頂點交集矩陣存於 `regions[].vertex_overlap`。

**否定的局部猜想**：「一有 cycle／region 坍縮，當前相容性就必失敗」。
本例前後都無一步 escape，但 cycle 數與 region 數確實下降。
指定 component switch 可逆，因此反向也能新生這個 cycle；沒有全 switch 單調下降量。
研究中排除了等同全域色置換、僅交換 system 名稱的 cycle 數變化。

## 5. 證書與驗證

[checker／API](../scripts/c5_edge_choices.py)；[證書](../artifacts/c5_cells/edge_choices.json)。

- `stages` 保存每層候選、分組和完整見證。
- `branches[].history` 是 `transition_table` 的索引；從 `seeds[origin]` 可連續回放。
- `transition_table` 保存 196 個不同 `(source coloring, action)` 的實際轉換。
- 每個 transition 的 `systems` 保留 paths/cycles 的完整 edge sets 與交集矩陣；
  `regions` 保留完整 vertex partitions 及 split／merge 對應。
- `structural_cycle_loss` 保存 §4 的前置 move 與實際坍縮事件。
- `projection_counterexample`／`false_splice` 保存兩種錯誤壓縮的負控制。

驗證包括：直接 primal 枚舉與 Choice 的一步／兩步結果逐集合相等；每條已保存
transition 用 edge XOR 加 anchor 獨立恢復完整染色；dual cut 聯集和 preserved system
核對；非法非 maximal component 拒絕；空集合、分支相容篩選、虛假欄位混合與虛假
來源拼接負控制。這是精確 Python 計算，尚未 Lean 化。

```bash
uv run --with networkx==3.5 python scripts/c5_edge_choices.py --check
uv run --with networkx==3.5 python scripts/c5_edge_incidence.py --check
uv run --with networkx==3.5 python scripts/c5_edge_switches.py --check
uv run --with networkx==3.5 python scripts/c5_edge_states.py --check
lake build
git diff --check
```

## 6. 直接接續入口

下一步可固定 §4 的局部 BC 坍縮，比較其餘同 source relation 的候選：哪些有相同
重接、哪些不會坍縮；再研究保留何種 joint interface 才能預測這個差異。
現有版本以完整 witnesses 支持精確操作，尚沒有證明一個不隨內部圖大小增加的
壓縮 relation 足夠。沒有排除新的 C5 relation、沒有證明 K∞=K≤5，也沒有啟動
polygon grammar、大圖搜尋或 safety-game 求解。
