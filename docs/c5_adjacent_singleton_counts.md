# C5 adjacent-singleton problem：計數層與剩餘缺口

2026-09-15。接續 [主問題](c5_kempe_screen.md#4-c5-adjacent-singleton-problemunproved)。

**後續進展**：[near-triangulation／文獻 count-cone 歸約](c5_count_cone_bridge.md)
已補上「保留一個關鍵染色的補完仍是反例」紙面引理，並把較強目標 m≤0 對應到
Dvořák–Lidický Conjecture 9。主問題仍未證；最新交接以上述文件為準。

**本輪結果**：得到適用於任意有限 C5 disk cell 的延伸計數恆等式（下文紙面證明；代數半部後續已 Lean 化，見 §2 信任範圍），
並給出滿足該式與 complementary Kempe orbit 計數分解的抽象 independent-support 例子。
因此這兩類計數必要條件，即使加上目前 exterior／push screen，仍不足以證 adjacent-singleton lemma。
**沒有得到 realizing graph、不可實現性證明或 K∞=K5。**

## 1. 定義：每個固定 boundary assignment 的延伸數

固定 C5=(v₀,…,v₄)，四色色盤固定。對每條非相鄰頂點對 uv：

- x_uv：唯一重複色 pair 為 uv 的四色 boundary assignment 的完整延伸數。
- y_i：singleton 位於 v_i 的三色 boundary assignment 的完整延伸數。

同一 S4 orbit 中的固定 assignment 延伸數相等。這裡不是整個 orbit 的染色總數；
若計整個 orbit，兩類均再乘 24。P(G)={i:y_i>0}，T4 全收等價於每個 x_uv>0。

## 2. 紙面定理：五個 chord totals 相同

對任意有限 C5 disk cell G，存在整數 L，使

\[
\boxed{x_{uv}+y_u+y_v=L\qquad(uv\text{ 為 C5 chord}).}
\]

等價地，令 m=L−Σ_i y_i，則

\[
x_{uv}=m+\sum_{i\notin\{u,v\}}y_i.
\]

m 不必非負；它是代數參數，不是一般情況下某個集合的大小。

### 證明

令 H=G−E(C5)。因為 boundary assignment 已 proper，刪除這五條邊不改變延伸數。
對 H 的所有邊做 inclusion–exclusion。每個 A⊆E(H) 的貢獻為

\[
(-1)^{|A|}4^{k_0(A)}\,mathbf 1[b\text{ 在每個 boundary component block 上同色}],
\]

其中 k₀(A) 是 (V(G),A) 中不碰 boundary 的 connected components 數。

不同 components 在 disk 中不相交，因此其 boundary partition noncrossing。
若某個 block 含 C5 相鄰頂點，對所有 proper boundary assignments 的貢獻均為零。
其餘 blocks 大小至多 2，因為 α(C5)=2。若有兩個大小 2 的 blocks，它們必是兩條
vertex-disjoint chords；C5 上這樣的兩條 chords 必交錯，違反 noncrossing。

所以非零項只可能是：全 singleton partition，或一條 chord 的兩端同 block、其餘 singleton。
把各類 signed coefficients 記成 a₀、a_e，便有

\[
x_e=a_0+a_e,\qquad y_i=a_0+a_{e_i}+a_{f_i},
\]

其中 e_i,f_i 是 singleton-i state 的兩個重複色 pairs。
對任意 chord uv，{uv,e_u,f_u,e_v,f_v} 恰好是五條 chords。因此

\[
x_{uv}+y_u+y_v=3a_0+\sum_e a_e,
\]

與 uv 無關。證畢。

**信任範圍**：一般 inclusion–exclusion 與 disk 中不相交 components 的 noncrossing 性是
上述紙面論證，尚未形式化到 Lean。從係數 `a₀, a_e` 到恆等式的代數半部已 Lean 化：
[Math/C5Counts.lean](../Math/C5Counts.lean) 的 `ofCoefficients_chordTotalConst`，以及
`x_eq_m_add`（`x_uv = m + Σ_{i∉{u,v}} y_i`）；§3.2 的 `N_P` 由 `NP_chordTotalConst`、
`NP_support` 對任意 `P` 給出。checker 窮盡 42 個 noncrossing partitions，確認其中
只有 6 個 indicator 非零，且每個都滿足此式；這是有限部分的檢查，不代替 topology bridge。

## 3. 為什麼加上計數仍不能封口

### 3.1 Kempe 計數必要條件

固定四色的一個 complementary split，例如 {0,1}|{2,3}。完整染色按兩組雙色 subgraphs
的 vertex sets 與 connected components 分類。交換任意 components 的兩色不改變這些
subgraphs，因此完整染色被分成可逆的 swap orbits。

一個 orbit 在 boundary 上給出一個 noncrossing partition 的 swap orbit O。
若有 h 個不碰 boundary 的 components，每個 b∈O 恰有 2^h 個完整染色。
所以 240 個固定標號 proper boundary assignments 的延伸數向量，必可寫成

\[
N=\sum_O w_O\mathbf1_O,\qquad w_O\in\mathbb Z_{\ge0}.
\]

三個 complementary splits 都各自必有此分解。這比只檢查「某個 O 包含於 support」保留更多
資訊，但仍未要求三套分解來自**同一張圖**的完整染色空間。

### 3.2 精確的抽象例子

令 t 為「每個四色 state 計數 1，每個三色 state 計數 0」的向量。
令 f_i 是 C5 加上兩條 incident with v_i 的 chords 所得 pentagon fan 的延伸數向量：

\[
(f_i)_{\text{singleton }j}=\mathbf1_{i=j},\qquad
(f_i)_{\text{four-pair }uv}=\mathbf1_{i\notin\{u,v\}}.
\]

f_i 是實際 disk 圖的計數；t **不是**已實現的圖計數，且其 full support 被 exterior wheel + 4CT 排除。
但 t 本身通過三個 splits 的非負整數 orbit 分解。

對任何 independent set P⊆V(C5)，取

\[
N_P=t+\sum_{i\in P}f_i.
\]

則

\[
y_i=\mathbf1_{i\in P},\qquad
x_{uv}=1+|P\setminus\{u,v\}|,\qquad L=1+|P|.
\]

五個 x 都正，singleton support 恰為 P，且滿足 §2 的恆等式。
三套 orbit 分解由 t、f_i 的分解相加即得；checker 用整數逐座標重算所有 240 個計數，
不是浮點 LP 可行性聲明。更一般地，t 與 f_i 的非負整數加權和也通過這兩類條件。

當 P 非空且 independent 時，其 support 還通過既有 Kempe／exterior screen。
因此這些例子證明的是**所列必要條件的不足**，不是 adjacent-singleton lemma 的反例。
把計數向量相加沒有在此對應到任何合法 disk graph operation。

### 3.3 加入 exterior 的 push 閉包

先前只驗證 153 個 Kempe masks 對 10 種 boundary push 封閉。
本輪補驗：加入 exterior 條件後的 142 個 masks，全部 1,420 個 push transitions 仍留在此集合。
所以這十種 push 的任意有限序列，加上每一步重新做 Kempe／exterior screen，也不能排除額外候選。
此處不包含其他 annulus 操作或一般 context。

## 4. 可以直接使用的反證起點

假設 T4 全收，且 P independent。其補集至少三點，所以包含相鄰兩點。
旋轉標號，令這兩個缺失 singleton 位置為 v₃、v₄。選一個延伸

\[
(v_0,v_1,v_2,v_3,v_4)=(A,B,A,C,D)
\]

的完整染色（由 T4 全收存在）。那麼在**每一個**這種延伸中：

1. v₁ 與 v₃ 必在同一個 B–C component；否則只交換包含 v₁ 的 component，得到
   (A,C,A,C,D)，使 singleton-v₄ 可延伸，矛盾。
2. v₁ 與 v₄ 必在同一個 B–D component；否則同理得到 singleton-v₃。
3. v₃–v₄ 已是 C–D boundary 邊。

這給出三個 singleton vertices 的 pairwise Kempe linkage，是可用的具體起始結構。
但兩條 blocking paths 可以在 B 色頂點相交，不能直接當作兩條 vertex-disjoint paths
套用交錯端點障礙。已有 orbit countermodels 也容許此種 blocking。

**目前剩餘的核心缺口**：找出這些 blocking structures 在換色後、或在其他四色 boundary
fibers 中，必須遵守而現有抽象分解未表達的同圖相容性，或使用另一個直接的 disk 結構論證。
若要沿此路走，下一個候選引理應明列保留哪些 paths／components，以及一次換色會如何改變
其他色對的 connectivity；不能把各 split 的 existential witnesses 當成同一張圖的證據。

這不證明所有更強的計數方法或單一染色 Kempe 方法都失敗，也沒有假設整個 extension space
是單一 Kempe class。主引理與一般 K∞=K5 仍未證。

## 5. 與指定文獻的關係

[Dvořák–Swart, §1, arXiv:2504.07764v1](https://arxiv.org/html/2504.07764v1) 的 planar
realizability 定義保留 terminal cyclic order，並以 Kempe constraints 和 reducibility 說明
邊界 extension sets 的限制。這支持本題的問題設定，但沒有給出 adjacent-singleton lemma。

其 Theorem 3 在 k=4 給的是 rooted-K5-minor-free、K6-minor-free realization；
這不是本題要求的 planar disk realization，不能拿來構造反例。
同樣，Theorem 1 的任意三色關係可實現，限制的是**整張圖只用三色**；本題 y_i 允許內部用第四色，
不能把那個定理直接套到 singleton support。

## 6. Computational certificate 與重播

- [checker](../scripts/c5_adjacent_singleton_counts.py)
- [完整 JSON 證書](../artifacts/c5_cells/adjacent_singleton_counts.json)

```bash
python3 scripts/c5_adjacent_singleton_counts.py --check
python3 scripts/c5_kempe_screen.py --check
git diff --check
```

證書包含：132 個既有 witness 的完整延伸計數（逐一重算，support 全吻合）、42 個 noncrossing
partitions 的有限檢查、各 split 的 70 個 boundary swap orbits（附 partition witness）、
11 個 independent P 的整數分解、來源 hashes，以及 142-state push 閉包。

負控制：C5 加兩條交錯 chords 02、13 的計數不滿足 §2；這張圖不能以指定 C5 作 disk boundary。
任意把全 1 計數中的第一項加 1，也被恆等式拒絕。
數字 masks 僅保留於 JSON 對照，production catalogue 沒有修改。本輪成果依使用者指示整理為 commit／push 的提交範圍。
（計數層的代數部分於後續輪次 Lean 化，見上文信任範圍與 [count-cone §6](c5_count_cone_bridge.md#6-lean-化範圍2026-09-15-補)。）
