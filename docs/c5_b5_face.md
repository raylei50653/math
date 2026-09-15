# B₅ 特殊 support face：Petersen＋fans 與 gluing 的限制

2026-09-15。接續 [count-cone bridge](c5_count_cone_bridge.md)。

**結論**：使用文獻的完整 12-ray 定理，兩個 face 猜測都成立。
但 fan filter 給出的是 **正的**黏合染色數 `6c`，不是 4CT 矛盾。
任何非零 plane 5-pole 的一次完整黏合，都不能使這兩個候選向量的染色數為零。
Adjacent-singleton lemma 與 K∞=K5 仍未證。本輪不新增 Lean 或大圖搜尋。

## 1. 來源與重播範圍

- Dvořák–Lidický, [Coloring count cones of planar graphs, arXiv:1907.04066v2](https://arxiv.org/pdf/1907.04066v2)：
  Theorem 5（plane counts 屬於 B₅）、Lemma 6（12 條 rays）、Figure 3（印刷頁 7 的圖與 port 標號）、
  equation (1)（黏合 pairing）、Lemma 7（純特殊 ray 與 4CT）、Conjectures 8/9。
- Inoue–Kawarabayashi–Miyashita–Mohar–Thomassen–Thorup,
  [arXiv:2603.24880v1, Lemma 13.2](https://arxiv.org/html/2603.24880v1#S13.SS1)：
  從 boundary 使用三色的完整染色產生三種 boundary families 之一。

[checker](../scripts/c5_b5_face.py) 逐邊轉錄 Figure 3 的 12 張 5-poles，
枚舉 60 個有標號 parity words 的完整邊染色，再經既有 XOR 對應壓成十座標。
圖的 raw count 向量 gcd **全部等於 1**，因此下面的 primitive rays 就是原圖 counts。
PDF SHA-256：`d5460af5e98369b0e704ee043ba8daed806944db8dd5854b8b1d990bc104f26e`。

**信任邊界**：圖的轉錄經 Figure 3 視覺核對；checker 另核對 tripod 的 equality predicates、
五個 primal pentagon fans、wheel 與 t。沒有重新證明或用 polyhedral solver 重算
Lemma 6 的 ray completeness，也沒有形式化平面性或完整 Kempe dynamics。
以下 face 完備性與一般 context 排除使用引用的 Theorem 5／Lemma 6。

## 2. Fan-trap corollary：精確的可達性敘述

取 chord `j={j,j+2}`，令

\[
F_j=\{y_j\}\cup\{x_f:j\notin f\}.
\]

對適用 Lemma 13.2 的 near-triangulation，若 `P≠∅` 且 `P` independent，
從任一 boundary 使用三色的完整染色出發，該 lemma 只能產生 case (i)。理由：

- case (iii) 產生所有五個 y，與 independent 矛盾。
- case (ii) 的三個 orbits 恰為 `x_j,y_(j+3),y_(j+4)`；後兩個 singleton 位置相鄰。
  checker 逐一核對五個 equality predicates。
- case (i) 產生某個 `F_j` 的四個 orbits，因此 `j∈P`。

故可稱 **fan-trap corollary（輸出 family 版本）**：每個三色 boundary extension
所在的 Kempe component 都包含某個完整 fan family，lemma 的至多六次單一 Kempe changes
足以產生它。色名視為可整體重命名。

**不能加強成**「該 Kempe component 的所有 boundary states 都落在同一 F_j」，
也不能推出 arbitrary Kempe moves 永遠留在該 fan，或不同初始染色選到同一 j。
論文提供的是可達 family，不是 component 分割／不變集定理。
這一引用推論未 Lean 化；平行邊版本需保留 near-triangulation／planar Kempe 的適用前提。

## 3. 十二條 rays 的完整 support

`x_uv` 以 unordered chord 端點表示；Fᵢ 是計數向量，四個 support 座標皆為 1。
表中每個列出的座標值都是 1，未列者皆為 0。

| 論文 ray | 非零 y | 非零 x | m |
|---|---|---|---:|
| R₅,₁ | y₀,y₁ | x₂₄ | −1 |
| R₅,₂ | y₀,y₄ | x₁₃ | −1 |
| R₅,₃ | y₃,y₄ | x₀₂ | −1 |
| R₅,₄ | y₂,y₃ | x₁₄ | −1 |
| R₅,₅ | y₁,y₂ | x₀₃ | −1 |
| R₅,₆ = F₃ | y₃ | x₀₂,x₁₄,x₂₄ | 0 |
| R₅,₇ = F₂ | y₂ | x₀₃,x₁₃,x₁₄ | 0 |
| R₅,₈ = F₁ | y₁ | x₀₂,x₀₃,x₂₄ | 0 |
| R₅,₉ = F₀ | y₀ | x₁₃,x₁₄,x₂₄ | 0 |
| R₅,₁₀ = F₄ | y₄ | x₀₂,x₀₃,x₁₃ | 0 |
| R₅,₁₁ = W | 全部五個 | 無 | −3 |
| R₅,₁₂ = t | 無 | 全部五個 | 1 |

每條 ray 都滿足既有線性恆等式。由非負性，若 `n=Σ λᵣr` 在某座標為零，
所有 `λᵣ>0` 的 rays 在該座標也必須為零；不存在相消。因此令
`S(P)=T4∪{y_i:i∈P}`，對任何 independent P，

\[
B_5\cap\{n:\operatorname{supp}(n)\subseteq S(P)\}
=\operatorname{cone}\bigl(t,\{F_i:i\in P\}\bigr).
\]

checker 檢查全部 11 個 independent supports，包含空集；requested representatives 為：

| face | 保留的論文 rays | 唯一非負分解 |
|---|---|---|
| S₁=T4∪{y₀} | 12,9 | n=ct+aF₀ |
| S₂=T4∪{y₀,y₂} | 12,9,7 | n=ct+aF₀+bF₂ |

唯一性直接由 y 座標讀出 `a=y₀,b=y₂`，再由 `x₀₂` 讀出 `c`。
所以 special branch `P⊆{0,2},x₀₂>0` 下，

\[
c=m=x_{02}>0.
\]

這不只表示某個 cone 分解需要 t；在此 face 上分解確實唯一。
若 support **恰好**為 S₁，則 a>0；恰好為 S₂，則 a,b>0。
若只是 support 包含關係，a,b 可為零。真正圖的這些係數為整數。
這個標準形也已由既有 count identity 直接給出；新計算確認它恰是文獻 B₅ 的 face，
而不是新增一條能排掉 c>0 的不等式。

## 4. Gluing pairing 與現成的 fan filter

保留同一組有序 ports，對兩向量定義

\[
\langle n,q\rangle=\sum_{\psi\in\mathcal P_5}n(\psi)q(\psi)
=6\sum_{s\in\mathrm{REPS}}n_s q_s.
\]

這是 dual cubic gluing 的三色**邊**染色總數。因每個 boundary orbit 對應六個 edge words，
乘數是 6；若數 primal 黏合後的有標號四**頂點**染色，則是 `24Σ n_s q_s`。
固定 assignment 的 extension count 本身仍不乘 4。

證書給出完整 12×12 整數 pairing table，以及所有 10 個 D₅ port alignments。
同標號 gluing 與論文 equation (1) 一致；可在球面上反射另一塊來接合。
不能獨立重新命名兩邊的 boundary frame 再把 dot product 當成原 gluing。

最相關的表格如下：

| 第一個向量 | Q=R₅,₃ | Q=W=R₅,₁₁ |
|---|---:|---:|
| t | 6 | 0 |
| F₀ | 0 | 6 |
| F₂ | 0 | 6 |
| ct+aF₀+bF₂ | **6c** | **6(a+b)** |

**fan filter 已存在**：取 Q=R₅,₃，其 support 是 `{x₀₂,y₃,y₄}`。
原圖是 ports 2,3,4 接一個 cubic vertex，ports 0,1 直接以一條邊相連。
最後這條邊在補回指定 degree-5 頂點時是 loop，屬論文允許的 near-cubic 類別。
它正是 primal 邊界條件 `v₀=v₂` 的 equality context。

在前 11 個 planar ray generators 中，消掉 F₀ 且保留 t 的是 R₅,₃、R₅,₅；
同時消掉 F₀,F₂ 且保留 t 的只有 R₅,₃。這是對 generators 的分類，
不宣称任意 planar context 必須落在前 11 rays 生成的子錐（那仍是 Conjecture 8）。

## 5. 為什麼這尚未給出 Lemma 7 式矛盾

Lemma 7 的 wheel closure 把純 t 變成零染色數，接著用 4CT 和 bridge/parity argument。
加入 fan 後 wheel closure 的染色數變為 `6(a+b)>0`。
改用 Q=R₅,₃ 雖然消掉 fans，卻得到 `6c>0`；4CT 完全容許這個結果。

還能給出一個一般的限制（引用 B₅ 完整性後的紙面推論）：

> 若 c>0 且至少一個 aᵢ>0，則對任意非零 q∈B₅，
> `⟨ct+ΣaᵢFᵢ,q⟩>0`。

理由：十二條 rays 中，只有 W 與 t 的 pairing 為零。
而 W 與每個 Fᵢ 的 pairing 都是 6。因此没有一條 ray 同時消掉 t 和任一正係數 fan；
非負 ray 組合也不可能相消。此論證涵蓋全部 B₅，無須假設 Conjecture 8，
也涵蓋任意大小、非零 count 的 plane 5-pole。D₅ alignment 不改結論。

所以**單一、非零、同五個 terminals 的普通 count-pairing closure 無法產生零染色矛盾**。
不能藉此排除更複雜的圖變換、多步構造或用 bridge 結構建立額外條件；
若選本身 count vector 為零的 context，則對所有輸入都給零，不能區分這些成分。

### 後續方向與已知缺口

下一個精確目標仍是：證明真正 plane graph 的這個 face 只能有 c=0。

1. 若繼續 gluing 路線，先提出超出上述單次 pairing 的圖變換或 bridge 結構引理，
   明列輸入圖類別、輸出與所需前提，再證平面性、count 變換與 bridge 性質。
   目前尚無滿足這些要求的構造；不能把「量到 6c」當成「排除 c」。
2. 若轉回 Kempe 路線，需要同圖不同完整染色間的 connectivity 相容性定理。
   Lemma 13.2 只提供可達 fan family，尚無 component confinement 或 fan 間轉移限制。
3. 文獻／形式化缺口分開保留：12-ray 完備性依賴引用，未在 repo 重算；
   fan corollary 的平行邊適用性需補明確論證，相關平面拓撲尚未 Lean 化。
   補這些驗證本身不會消除 c>0。

Adjacent-singleton lemma 與 K∞=K5 仍未證。以上是接續入口，本輪不啟動新搜尋。

## 6. 驗證

```bash
python3 scripts/c5_b5_face.py --check
python3 scripts/c5_count_cone_bridge.py --check
git diff --check
```

[JSON 證書](../artifacts/c5_cells/b5_face.json) 包含來源 hash、程式與依賴 hash、12 張圖的 edges、
raw／primitive counts、11 個 faces、完整 pairing 與 D₅ tables，以及兩個負控制：
漏乘 6 和只旋轉一側 ports 都會改變實際計數。沒有新增 Lean 模組，因此本輪不重跑 Lean build。
