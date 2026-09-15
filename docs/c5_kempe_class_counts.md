# C5：把計數恆等式與關鍵 fibre 定位到同一 Kempe class

2026-09-15。接續 [研究路線總覽](c5_boundary_relations.md) 與
[B₅ face 的 connectivity 缺口](c5_b5_face.md)。

**本輪推進**：對任意有限 C5 disk 圖，每個完整四色染色的 Kempe class 都滿足
五個 chord totals 相等。這比只對全部染色求和的計數恆等式更細，並將特殊反例的
正參數定位到同一 class。**紙面證明＋精確有限證書，未 Lean 化**；主命題仍未證。
沒有新增 graph catalogue 搜尋，也沒有把單一 class 當成另一張 disk 圖。

## 1. 定義與主敘述

固定同一有序 C5 邊界。完整染色空間以「交換一個兩色 induced component」為邊；
其連通分量記為 K（Kempe class）。允許交換接觸邊界的 component，沒有固定 boundary
assignment 不動；否則下列敘述不適用。

任意全域顏色 transposition 可藉由依次交換該兩色的全部 components 完成，
故每個 K 都對 S₄ 封閉。對固定 boundary assignment b 定義 n_K(b) 為屬於 K 的延伸數。
它在每個 S₄ orbit 上相等，所以可定義 x_e(K)、y_i(K)、P(K)，記號同
[計數報告 §1](c5_adjacent_singleton_counts.md)。計的是每個固定 assignment，不乘 24。

**Classwise chord-total identity：**

\[
x_{uv}(K)+y_u(K)+y_v(K)=L_K\qquad(uv\text{ 為 C5 chord}).
\]

令 m_K=L_K−Σᵢyᵢ(K)，則

\[
x_e(K)=m_K+\sum_{i\notin e}y_i(K).
\]

這裡不能直接套用整張圖的 inclusion–exclusion：K 不一定是某張圖的完整染色集。
下面用 class 內確實存在的 Kempe 操作證明。

## 2. 四個 boundary words 的局部證書

固定 complementary split {0,1}|{2,3}。考慮線性泛函

\[
D(n)=n(02012)-n(02013)-n(02102)+n(02103).
\]

對每種合法 boundary component partition，獨立交換其 blocks 得到一個 boundary orbit O。
合法性條件為：每個 block 位於 split 的同一側；同側 boundary 邊端點在同一 block；
所有 blocks 合在一起 noncrossing。最後一條由 disk 內互不相交的兩色 components 給出。

[checker](../scripts/c5_kempe_class_counts.py) 枚舉全部 **70** 個不同 O，逐一驗證

\[
\sum_{b\in O}D(\mathbf1_b)=0.
\]

再對五個 boundary rotations 核對，共 **350** 個精確整數等式。
[JSON 證書](../artifacts/c5_cells/kempe_class_counts.json) 保存每個 O 的起始染色、
partition witness、五個泛函的係數與全部零殘差；不依賴浮點數或線性規劃求解器。
70 個 O 沿用既有 partition 枚舉器，來源 hash 一併記錄。

### 為何局部證書能用在整個 K

把 K 按此 split 的完整 swap orbits 分組。從一個完整染色出發，交換任何 component
不改變兩個 induced vertex sets 或它們的 component partition，所有交換互相可交換。
若有 r 個完整 components，其中 s 個接觸 boundary，完整 orbit 的大小為 2ʳ。
每個 boundary orbit member 恰有 2ʳ⁻ˢ 個完整染色原像：其餘 r−s 個 component swaps
完全不改變 boundary。

因此，每個完整 orbit 對 D 的貢獻都是 2ʳ⁻ˢ 乘上一個已驗證的零；相加得 D(n_K)=0。
依 S₄ 不變性，四個項目分別是 y₃、x₀₂、y₂、x₀₃，所以

\[
x_{03}(K)+y_0(K)+y_3(K)=x_{02}(K)+y_0(K)+y_2(K).
\]

五次旋轉把全部五條 chord totals 連成同一值，完成證明。

**信任範圍**：一般 disk 的 noncrossing soundness、完整 swap-orbit 分組與均勻原像
是上述紙面論證；有限 70-orbit 窮盡與等式由 Python 整數檢查。
這不是 Lean kernel 證明。允許平行邊不影響 induced components 或此論證。

## 3. 正參數出現在同一個 class

假設特殊反例 G 滿足 P(G)⊆e，且 x_e(G)>0。選取 repeated-pair e 的一個完整染色 c，
令 K 為其 Kempe class。由 P(K)⊆P(G)⊆e 與 x_e(K)>0，得到

\[
m_K=x_e(K)>0,\qquad\forall f,\quad x_f(K)>0.
\]

**因此從 c 出發，五種四色 boundary orbits 都能在同一 Kempe class 中到達。**
這不是把五個互不相干的 class 的 extensions 拼成全收 T₄；也不表示全部四色 extensions
都屬於 K，更沒有給固定長度的換色路徑。

更精確地，令 t 是五個 x 座標皆 1、y 皆 0 的向量，Fᵢ 是 singleton-i fan 向量。
對 G 的每個 class J 都有

\[
n_J=x_e(J)t+\sum_{i\in e}y_i(J)F_i,\qquad x_e(J)\ge0.
\]

故全圖的正參數不是不同 classes 的正負抵消：m(G)=Σⱼm_J=Σⱼx_e(J)>0，
至少一個 class 自身具有正 t 係數。這個分解直接來自恆等式，不依賴 B₅ ray 完備性。
既有 [C5Counts.all_chords_positive](../Math/C5Counts.lean) 可承接其代數半部；
目前沒有把本節 class 計數接到 Lean 的圖語義。

### 與既有 screen 的關係

上述「同 class 全收 T₄」的 support 結論，也能由既有 Kempe screen 直接套在 class support
得到；它不是新的 mask 排除條件。本輪新增的是 classwise **計數**恆等式、
均勻原像論證與正參數的逐 class 分解。

仍不能從這裡推出 class 中有三色 boundary extension，更不能把單次 fan family 的
可達性提升成 component confinement。若某個 class 的 P(K)=∅，其向量形式允許 x_e(K)t。
不能用 exterior wheel＋4CT 排除該 class：gluing 可由 G 的其他 classes 提供染色。
即使 P(K)≠∅，前輪 ordinary pairing 的限制也仍存在。

## 4. 實際圖驗證與負控制

- 全部 **132** 個既有 catalogue witnesses：枚舉完整染色的 S₄ orbits，逐個真實
  Kempe move 建立 class；這些 witnesses 各只有一個 class。
  每個 class 都滿足恆等式，分量求和也與既有獨立全染色計數證書完全相等。
- 因上述 samples 沒有測到多 class，另加入一張固定圖：把 icosahedron 放在面三角形
  (0,1,4) 內側，在外側增加路徑 1−2−3−4，指定外界為 0−1−2−3−4−0。
  共有 14 個頂點、9 個內點。重播得到 **10 個 classes**，每個 class 有 7 個完整染色
  S₄ orbits，十個分量分別滿足恆等式。完整 edge list 與計數在 JSON control 中。
  此例只是固定驗證圖，不是新 relation 搜尋。
- 加入交錯 chords 02、13 的非 disk 圖：存在違反恆等式的 class。
  這檢查指定邊界的 disk 假設確實不可省略。
- 刪掉泛函的一項：至少一個 boundary orbit 立即出現非零殘差。

S₄ quotient 不會錯誤合併不同 classes，因每個全域色置換本來就能由 Kempe moves 實現。
proper C5 使用至少三色，S₄ 在 boundary assignments 上的作用自由；
每個完整染色 orbit 恰對其 canonical boundary assignment 貢獻一次。

## 5. 下一個精確入口

對同一 disk 圖 G，保留**全圖** P(G)⊆e 的假設，從 x_e 的一個完整染色 c 開始。
現在可以在 c 的同一 class 中自由選取所需四色 boundary fibre 的代表；
下一步應指定一個實際換色序列與其保留的 paths/components，證明能得到 singleton
位置在 e 外的延伸，或從所有這些換色都被阻擋的條件導出 disk 結構矛盾。

新增的定位引理消除了「所需四色 states 可能全在互不連通 classes」這個疑問，
**沒有**解決一次換色如何改變其他色對 connectivity 的核心缺口。
不應把「每個 class 自己可被某張 disk 圖實現」或「每個 class 都與 exterior 相交」
當作中間假設。Adjacent-singleton lemma 與 K∞=K≤5 仍未證。

## 6. 重播

```bash
python3 scripts/c5_kempe_class_counts.py --check
python3 scripts/c5_adjacent_singleton_counts.py --check
python3 scripts/c5_kempe_screen.py --check
git diff --check
```

本輪沒有新增 Lean 模組，未改既有 checker、production catalogue 或先前證書。
