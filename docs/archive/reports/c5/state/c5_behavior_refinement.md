# Kempe 行為驅動的遍歷與狀態細化

2026-09-15：由使用者提供的 `/tmp/c5_behavior_refinement.md` 納入專案。
以下保留研究提案；第一輪實作、一般 iff 的紙面證明與有限結果見
[behavior refinement 第一輪報告](c5_behavior_refinement_results.md)。
目前完成 Phase A/B 與第一個 predicate 的 Phase C；尚未證多步 closure。

## 0. 目的

目前的 C5 Kempe 分析已經出現一個關鍵反例：

即使固定

* 同一 embedded C5 disk；
* 同一 Kempe class；
* 相同 boundary coloring；
* 相同三組 pairings；
* 相同三組 cycle counts；
* 相同 rooted Kempe 操作；
* 相同 cut 長度；

交換之後仍可能得到不同的 pairing、cycle counts 與一步 escape 性質。

因此

$$
(\text{boundary},T,\text{cycle counts},\text{rooted action},|\delta K|)
$$

不是一般情況下足以決定下一步的狀態描述。

這表示後續不宜只持續猜測更多 scalar statistics，例如 cut length、component size、cycle count 等，而可以改用另一種策略：

> **由實際未來行為反過來細化狀態。**

基本流程為

$$
\boxed{
\text{粗狀態}
\rightarrow
\text{找到未來行為衝突}
\rightarrow
\text{找出造成分歧的連通條件}
\rightarrow
\text{細化狀態}
}
$$

目標不是立即得到最小 automaton，而是建立一套能逐步發現缺失 invariant 的遍歷方法。

---

# 1. 現有反例提供的第一條 distinguishing continuation

考慮現有 survivor-811 上的兩個合法染色 \(c,d\)。

它們具有相同的粗狀態：

* boundary 相同；
* 三組 source pairings 相同；
* 三組 source cycle counts 相同；
* 都沒有一步 singleton-\(\{1,3,4\}\) escape。

考慮 rooted 操作

$$
a = AB@0
$$

其含義為：

> 交換目前包含 boundary vertex \(0\) 的 maximal \(AB\) component。

注意這裡固定的是 **rooted selection rule**，不是固定 component 頂點集合。

對 \(c,d\) 執行此操作後：

* cut length 都是 \(21\)；
* target boundary 相同；
* 但 target pairing、cycle counts 與一步 escape 性質不同。

因此 `AB@0` 已能在一步後區分兩者的完整 edge-state 行為。

---

## 1.1 若只觀察 escape，兩步即可區分

從 \(c\) 執行 `AB@0` 後，再交換目前包含頂點 \(2\) 的 maximal \(BC\) component：

$$
b = BC@2.
$$

此時會到達 singleton-4。

另一方面，從 \(d\) 執行 `AB@0` 後，不存在任何一步禁止 escape。

因此對 escape observable 而言，可以得到 distinguishing sequence

$$
\boxed{
w=(AB@0,\ BC@2).
}
$$

若定義

$$
E(x)=
\begin{cases}
1,&x\text{ 的 boundary 為禁止 singleton-}\{1,3,4\},\\
0,&\text{否則},
\end{cases}
$$

則

$$
E(\tau_w(c))=1,
\qquad
E(\tau_w(d))=0.
$$

這表示：

> 兩個目前摘要完全相同的 states，可以被一條短的共同未來操作序列區分。

這比單純知道「兩個 targets 不一樣」更有用，因為它提供了一個可直接用於 state refinement 的實際 experiment。

---

# 2. 從兩步 continuation 抽出來源 predicate

上述兩步行為還可以進一步轉寫成來源狀態上的 connectivity condition。

執行 `AB@0` 後，boundary 為

$$
(B,A,C,A,D).
$$

此時 boundary 上使用 \(B/C\) 的頂點只有 \(0,2\)。

考慮交換

$$
BC@2.
$$

若目前的 \(BC\) component 包含 \(2\) 但不包含 \(0\)，則交換後

$$
(B,A,C,A,D)
\longrightarrow
(B,A,B,A,D),
$$

因此頂點 \(4\) 成為唯一使用顏色 \(D\) 的 boundary vertex，即得到 singleton-4。

反之，如果 \(0,2\) 位於同一個 \(BC\) component，則兩者會一起交換，boundary 不會變成 singleton-4。

因此，在這個 boundary frame 下：

$$
\boxed{
BC@2\text{ 到達 singleton-4}
\iff
0\not\leftrightarrow 2
\text{ in the current }BC\text{ subgraph}.
}
$$

這已經把「某條 continuation 是否成功」轉成一個二元 connectivity predicate。

---

## 2.1 將條件搬回第一次交換之前

令

$$
K=\operatorname{Comp}_{AB}^{c}(0)
$$

為第一次操作選中的 component。

設交換前各色頂點集合為

$$
V_A,V_B,V_C,V_D.
$$

交換 \(A/B\) 後，新的 \(B\)-colored vertices 為

$$
V_B'
=
(V_B\setminus K)\cup(V_A\cap K).
$$

而 \(C\)-colored vertices 不變。

因此定義

$$
U(c,a)
=
V_C
\cup
(V_B\setminus K)
\cup
(V_A\cap K).
$$

則第一次交換之後的 \(BC\)-subgraph，正是原圖在

$$
U(c,a)
$$

上的 induced subgraph。

所以可以直接在 source 上定義

$$
\psi_a(c)
=
\left[
0\leftrightarrow 2
\text{ in }G[U(c,a)]
\right].
$$

在指定 boundary 與 rooted-action 前提下，

$$
\boxed{
\neg\psi_a(c)
\Longrightarrow
AB@0;\ BC@2
\text{ 到達 singleton-4}.
}
$$

更理想的目標是證明適當前提下的 iff：

$$
\boxed{
\neg\psi_a(c)
\iff
AB@0;\ BC@2
\text{ 到達 singleton-4}.
}
$$

這可以成為第一個由反例導出的 structural predicate。

---

# 3. 新的 state model：Concrete / Observation / Transition

不應立刻把所有 cut interface 資訊硬塞進單一 state tuple。

較適合的建模方式是分成三層。

---

## 3.1 Concrete branch

完整保存實際 witness：

```text
ConcreteBranch:
    graph
    coloring
    color_frame
    boundary
    history
    legality_evidence
```

Concrete branch 是正確性的底層來源。

只要尚未證明 future equivalence，就不能因為兩個 branches 的摘要相同而刪除其中一個。

---

## 3.2 Observation

Observation 只保存目前研究需要讀取的摘要：

```text
Observation:
    boundary
    pairings
    cycle_counts

    optional predicates:
        connectivity queries
        cut statistics
        proven behavioral summaries
```

例如初始摘要可以是

$$
\sigma_0(c)
=
(
\text{boundary},
\text{pairings},
\text{cycle counts}
).
$$

現有 \(c,d\) 在 \(\sigma_0\) 下相同。

若加入上面的 connectivity predicate：

$$
\sigma_1(c)
=
(
\sigma_0(c),
\psi_a(c)
),
$$

則這對 witness 可以被分開。

重要的是：

> `Observation equality` 只代表目前的觀察語言無法區分兩個 states。

它不自動表示 future equivalence，也不能直接用於安全 deduplication。

---

## 3.3 Transition interface

對每個具體 action，另外保存：

```text
TransitionInterface:
    source
    rooted_action
    actual_maximal_component

    cut_edges
    retained_port_partition
    added_edges

    target
    reconstruction_evidence
```

這裡的 interface 是

$$
I(c,a),
$$

而不是只屬於 \(c\) 的固定 state。

原因是：

* 不同 action 會產生不同 cut；
* 同一 rooted rule 在不同 coloring 上可能選到不同 component；
* retained ports 及 reconnect behavior 是 transition-specific information。

因此應區分：

$$
\boxed{
\text{state observation}
\neq
\text{transition interface}.
}
$$

---

# 4. 新遍歷策略：behavior-guided refinement

普通 BFS / DFS 主要問：

> 從這個 state 還有哪些合法下一步？

新的研究型 traversal 另外問：

> 目前被歸在同一 observation class 的兩個 states，是否存在一條共同操作序列使它們產生不同結果？

---

## 4.1 第一步：按目前 observation 分桶

對所有 concrete witnesses 計算

$$
\sigma(c).
$$

形成 equivalence candidates：

$$
[c]_\sigma
=
\{d:\sigma(d)=\sigma(c)\}.
$$

注意：

> 這只是 bucket，不是已證 equivalence class。

桶內所有 concrete witnesses 都必須保留。

---

## 4.2 第二步：在同桶 witness 間同步探索

取

$$
x,y
$$

滿足

$$
\sigma(x)=\sigma(y).
$$

考慮同一 rooted action \(a\)。

每一側都必須：

1. 從自己的當前 coloring 重新計算 maximal component；
2. 檢查 action 是否存在；
3. 執行自己的合法 action。

形成

$$
(x,y)
\xrightarrow{a}
(
T_a(x),T_a(y)
).
$$

不能把 \(x\) 的 component vertex set 直接套到 \(y\)。

---

## 4.3 action legality 本身也是 observable

可能出現：

$$
a\in Enabled(x),
\qquad
a\notin Enabled(y).
$$

這本身就是一個 distinguishing result。

因此同步搜尋中的 transition outcome 至少應包含：

```text
illegal
```

或

```text
legal + resulting observation
```

即

$$
\operatorname{step}_a(x)
=
\begin{cases}
\bot,&a\text{ illegal},\\
\sigma(T_a(x)),&a\text{ legal}.
\end{cases}
$$

---

# 5. Distinguishing sequence

對 operation word

$$
w=a_1a_2\cdots a_k
$$

定義

$$
T_w(c)
=
T_{a_k}\circ\cdots\circ T_{a_1}(c)
$$

只在所有中間操作合法時定義。

若存在 observable \(O\) 使

$$
O(T_w(x))
\neq
O(T_w(y)),
$$

則稱 \(w\) 是 \(x,y\) 的 distinguishing sequence。

目前 witness 已提供：

### 若 observable 是完整 pairing / cycle state

$$
w=(AB@0)
$$

即可區分。

### 若 observable 只看 forbidden singleton escape

$$
w=(AB@0,\ BC@2)
$$

即可區分。

這表示「需要多少步才能區分」取決於選擇的 observable。

---

# 6. 由 distinguishing sequence 細化 state

令目前已發現的 distinguishing tests 為

$$
W=\{w_1,\dots,w_m\}.
$$

可以定義新的 behavior signature：

$$
B_W(c)
=
\left(
O(T_{w_1}(c)),
\dots,
O(T_{w_m}(c))
\right),
$$

其中：

* 中途 action illegal 時記為獨立值；
* 所有結果都保留 concrete replay witness。

然後定義

$$
\sigma_W(c)
=
(
\sigma_0(c),
B_W(c)
).
$$

於是每找到新的 counterexample，就加入新的 distinguishing test。

得到迭代：

$$
\boxed{
\sigma_0
\rightarrow
\sigma_1
\rightarrow
\sigma_2
\rightarrow
\cdots
}
$$

其中每次 refinement 都有具體 witness 支援。

---

# 7. 不應停在「記錄測試答案」

單純把

```text
AB@0 ; BC@2 -> escape?
```

加入 state 雖然能區分 witness，但這只是一個 behavioral bit。

真正有研究價值的下一步，是問：

> 為什麼這個 test 在兩個 states 上結果不同？

本例的答案是：

$$
0,2
$$

在第一次交換後的 \(BC\) subgraph 中是否連通。

因此 refinement 流程應包含第二個階段：

$$
\boxed{
\text{behavioral distinction}
\rightarrow
\text{structural explanation}
}
$$

也就是：

```text
distinguishing sequence
        ↓
compare transition interfaces
        ↓
locate different connectivity / incidence structure
        ↓
extract compact predicate
        ↓
prove predicate controls the behavior
```

---

# 8. Cut interface 的角色

目前 retained-port interface 已知能對指定 transition 精確重建 target pairing / cycle structure。

因此它很適合當作：

> **解釋 behavioral collision 的高精度 reference representation。**

假設

$$
\sigma(x)=\sigma(y),
$$

但

$$
O(T_a(x))
\neq O(T_a(y)).
$$

可以比較

$$
I(x,a)
\qquad\text{與}\qquad
I(y,a),
$$

尋找：

* 哪些 retained ports 被連在一起；
* 哪些舊 components 被 cut；
* 哪些 blocks 在加入新 edges 後 merge；
* 哪些 closed cycles 出現或消失。

接著嘗試把完整 interface 差異壓成較小 predicate。

---

# 9. Scalar statistics 的新定位

cut length、component cut counts、component sizes 等資訊仍然有價值。

但不再先假設：

$$
\text{某組 scalar statistics}
\Rightarrow
\text{完整 transition}.
$$

而改成：

> 當 behavioral collision 出現時，檢查哪個最小結構特徵足以解釋這一對 collision。

例如可以依序測試：

$$
|\delta K|,
$$

$$
\{\text{component cut multiplicities}\},
$$

$$
\{\text{component sizes + cut multiplicities}\},
$$

最後才到

$$
\text{retained-port partition}.
$$

如果較弱觀察仍有 collision，就得到新的負證書。

如果某一層在明確完整範圍內無 collision，才進一步研究是否存在充分性定理。

---

# 10. 安全 deduplication 所需的條件

behavior-guided refinement 初期只用於：

* 搜尋引導；
* collision discovery；
* state-language refinement。

不應立即用於刪除 concrete witnesses。

若希望某摘要

$$
\sigma
$$

真的能安全 deduplicate，至少需要對指定 action grammar \(\mathcal A\) 證明：

$$
\sigma(x)=\sigma(y)
$$

推出：

### 目前 observable 一致

$$
O(x)=O(y).
$$

### enabled actions 一致

$$
Enabled(x)=Enabled(y).
$$

### 每一步轉移保持摘要一致

對所有

$$
a\in Enabled(x)=Enabled(y),
$$

都有

$$
\sigma(T_a(x))
=
\sigma(T_a(y)).
$$

因此：

$$
\boxed{
\sigma(x)=\sigma(y)
\Longrightarrow
\text{所有有限 action sequences 上的 observable 一致}.
}
$$

這可以按操作序列長度歸納證明。

這才是適合安全 deduplication 的 `future equivalence`。

---

# 11. 為什麼一步 interface 還不等於完整 state

目前的 cut interface 可以回答：

> 已知 source 與某個合法 action 時，target pairing / cycles 是什麼？

但一般還不能只由 interface 回答：

> target 上有哪些新的 maximal Kempe components？

更不能保證：

> 下一步所有可能的 transition interfaces 都能由目前 interface 自足更新。

因此目前應使用：

```text
Concrete coloring
    ↓
enumerate legal actions
    ↓
build TransitionInterface
    ↓
predict / explain target observation
```

而不是：

```text
InterfaceState
    ↓
直接產生全部下一步 InterfaceState
```

後者需要額外的 closure theorem。

---

# 12. Witness coherence

如果把 observation buckets 當抽象圖的 vertices，需要避免另一個問題：

```text
bucket A --a--> bucket B --b--> bucket C
```

第一條 edge 可能由 witness \(x\) 支援，而第二條 edge 只由 bucket B 中另一個 witness \(y\) 支援。

這不代表存在真實路徑

$$
x\xrightarrow{a}?\xrightarrow{b}?
$$

因此：

> 抽象 edge 存在，不代表多條 edge 可以任意拼接。

任何候選操作序列最後都必須由**同一條 concrete branch history**完整重播。

---

# 13. Compatibility 不能當成單純剪枝條件

目前 `compatible` 表示：

* state 本身不是 forbidden singleton；
* 且沒有一步 forbidden escape。

因此一個 state 在操作後變成 incompatible，可能正代表：

> 它已經距離成功 escape 只剩一步。

本例的 \(c\) 正是如此。

所以若研究目標是尋找 escape，不應做：

```text
if not compatible(target):
    prune
```

反而應把

```text
compatible -> incompatible
```

視為重要訊號。

---

# 14. 建議的第一版 traversal

暫時固定 survivor-811，不擴大 catalogue。

## Phase A：建立同步 state-pair explorer

輸入：

```text
same-observation pair (x, y)
action grammar A
max depth d
observable O
```

搜尋：

```text
(x, y)
  |
 same rooted action
  v
(T_a(x), T_a(y))
```

直到：

1. action legality 不同；
2. observable 不同；
3. 到達深度上限。

輸出：

```text
source_x
source_y
common observation
distinguishing word
full replay_x
full replay_y
first divergence
```

---

## Phase B：用現有 witness 作 regression test

第一個固定測試：

```text
sources:
    c
    d

observable:
    full pairing/cycle state

expected:
    distinguish at depth 1 by AB@0
```

第二個：

```text
sources:
    c
    d

observable:
    forbidden singleton

expected:
    distinguish by
        AB@0
        BC@2
```

---

## Phase C：抽 structural predicate

對每個新 distinguishing word：

1. 比較第一次產生分歧之前的 transition interfaces；
2. 找出最小 connectivity / incidence 差異；
3. 嘗試寫成 source predicate；
4. 在固定 corpus 上回放；
5. 尋找 predicate collision；
6. 若沒有 collision，再考慮一般證明。

---

# 15. 第一個建議的一般引理

可以先形式化目前兩步規則，而不是直接 Lean 化完整 22-vertex witness。

候選名稱：

```text
two_move_singleton4_iff
```

概念內容：

> 在指定 boundary coloring 與第一次 rooted AB component boundary trace 的前提下，
> `AB@0` 後再做 `BC@2` 會得到 singleton-4，
> iff 第一次交換後 boundary vertices 0 與 2 不在同一 BC component。

等價地，可以把它寫成 source 上的 induced-subgraph connectivity predicate：

$$
\neg\psi_a(c)
\iff
AB@0;\ BC@2
\text{ yields singleton-4}.
$$

這個引理不依賴 survivor-811 的特定內部圖。

survivor-811 只提供：

* 此 predicate 確實能取兩種值；
* 兩種情況都可實現；
* 且可以出現在相同 coarse state 中。

因此 witness 與 general lemma 可以自然分工。

---

# 16. 與主研究問題的關係

這條 behavior-driven traversal 研究的是：

$$
\text{Kempe recoloring dynamics}.
$$

它試圖回答：

* 哪些粗 states 對未來操作不足；
* 哪些 connectivity predicates 必須保留；
* 是否存在有限且閉合的 future-state language；
* 哪些短 continuation 能區分看似相同的 states。

但主命題若仍是：

> 每個可實現 C5 boundary relation 是否存在至多五個內部頂點的代表，

則只需要保持

$$
\Sigma(H)=\Sigma(G).
$$

它不要求 \(H,G\) 在所有 Kempe 操作 sequence 下都 future-equivalent。

因此需要維持兩條研究線的區分：

```text
Boundary-relation representation
    -> 研究小代表 / replacement / K∞ = K≤5

Kempe behavior state
    -> 研究 recoloring dynamics / escape / future equivalence
```

兩者可以共享 connectivity 與 local-closure 技術，但不能把後者更強的要求誤當成前者主定理的必要條件。

---

# 17. 建議研究迴圈

整體可以固定成：

```text
1. 保留完整 concrete witnesses

2. 用目前 observation 分桶

3. 對同桶 witnesses 搜尋短 distinguishing continuations

4. 找到 collision
       ↓

5. 比較 cut / retained-port interfaces

6. 抽出較簡潔的 connectivity predicate

7. 加入 observation language

8. 在完整指定範圍重跑

9. 若仍有 collision
       -> 產生下一個反例

10. 若無 collision
       -> 嘗試證 transition closure / sufficiency

11. 只有取得 future-equivalence proof
       -> 才允許安全 deduplicate
```

---

# 18. 核心方向

這條路的核心轉變可以概括為：

$$
\boxed{
\text{猜哪些統計量可能夠}
}
$$

轉成

$$
\boxed{
\text{找出哪個未來操作會看穿目前的摘要}
}
$$

再轉成

$$
\boxed{
\text{解釋這個行為差異所需的最小連通資訊}
}
$$

因此遍歷本身不再只是用來找更多 states。

它同時成為：

> **state-language discovery procedure。**

每一次成功搜尋都應該產生至少一種研究成果：

1. 新 distinguishing sequence；
2. 新 coarse-state 反例；
3. 新 connectivity predicate；
4. 新 transition sufficiency theorem；
5. 或證明目前狀態語言在指定 grammar 下閉合。

這比單純擴大 Kempe orbit 或累積更多 transitions 更適合作為下一階段的系統化研究方向。
