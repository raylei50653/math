# C5 缺口：歸約到 near-triangulation 與已發表的計數猜想

2026-09-15。接續 [計數恆等式](c5_adjacent_singleton_counts.md)。

**新進展（紙面證明，未 Lean 化）**：任何 adjacent-singleton 反例都能轉成
同一有序 C5 邊界的 near-triangulation 反例（允許 parallel edges）。只需保留一個
關鍵完整染色；補邊後的 T4 全收由計數恆等式重新推出，不需要假設補邊保留全部染色。

這把問題接到 Dvořák–Lidický 的計數猜想。**主引理與 K∞=K5 仍未證**；
本輪沒有得到該猜想的證明。以下區分文獻結果、我們的推導和有限檢查。

## 1. 文獻錨點與精確翻譯

[Dvořák–Lidický, *Coloring count cones of planar graphs*, arXiv:1907.04066v2](https://arxiv.org/pdf/1907.04066v2)
（J. Graph Theory 100 (2022), 84–100）：Observation 3 給出 primal 四色／dual 三色邊染色
的延伸計數對應；Conjecture 9 是 degree-5 near-cubic 圖上的
`3 Σ n(ψ_i^{5,a}) ≥ Σ n(ψ_i^{5,b})`。Corollary 20 證其適用於 **少於 30 個頂點**的
plane near-cubic 圖。這是引用的含電腦輔助文獻結果，本倉庫沒有重播其證書。
一般情形在該文中是猜想；本輪檢索未找到後續解答，不據此斷言已完整查清最新研究狀態。

以下為本輪對本倉庫記號的推導。把四色視為 Z₂²，以 XOR 表示加法，對 boundary coloring b 定義

\[
q_j=b_j\mathbin{\mathrm{xor}}b_{j+1}.
\]

properness 使 q_j∈{1,2,3}，沿 C5 的 XOR 和為零；三種非零元素各出現奇數次。
每個 q 恰有四個 b 原像，分別由 b₀ 決定。固定一個 b₀ 後，完整 dual edge coloring
積分回 primal coloring，故**固定 boundary assignment 的延伸數相等，不乘 4 或 24**。

文獻的 a₀=(1,1,2,3,1) 積分為 (0,1,0,2,1)，是 singleton-3；
b₀=(1,2,1,1,3) 積分為 (0,1,3,2,3)，是 repeated-pair 24。
旋轉五次後，a 類恰對應全部 y_i，b 類恰對應全部 x_uv。

因此 Conjecture 9 在 near-triangulation 的記號下是

\[
3\sum_i y_i\ge\sum_{uv}x_{uv}.
\]

由既有恆等式 x_uv=m+Σ_{i∉{u,v}}y_i，相加得

\[
\sum_{uv}x_{uv}=5m+3\sum_i y_i.
\]

故文獻猜想正好翻譯成 **m≤0**。這不是我們已證的額外不等式。
舊抽象例子 t+Σ_{i∈P}f_i 全有 m=1，故每個例子都以 slack −5 違反它。

## 2. 反例只需保留一個四色 fiber

設 G 全收 T4，且 P(G) independent。C5 的每個 independent set 都包含在某條 chord
e={u,v} 的端點集合內：大小二時自身就是 chord；大小一／零時任選包含它的 chord。

選 repeated-pair e 的一個完整染色 c。考慮任何同邊界 disk supergraph H（允許加私有頂點），
只要求 c 能延伸到 H。那麼

- x_e(H)>0；
- Σ(H)⊆Σ(G)，所以 P(H)⊆P(G)⊆e；
- 計數恆等式給 m(H)=x_e(H)>0；
- 對每條 chord f，x_f(H)=m(H)+Σ_{i∉f}y_i(H)>0。

所以 H **自動重新全收 T4**，且 P(H) independent。這是反例保持引理。
沒有把五個不同染色當成可同時保留的同一個染色，也没有假定換色空間連通。

## 3. 任意反例到 near-triangulation

### 3.1 先移除不影響 boundary support 的枝塊

保留含 C5 的 maximal 2-connected block B。C5 是 cycle，所以存在唯一這樣的 block。
其餘 connected components 與 block-cut tree 的枝塊不改變 Σ：沿 cut vertex 接回時，
可把該枝塊某個既有染色的色名排列成指定 root color。原反例已可染色，故這些既有染色
可由原圖的一個染色限制得到；此步本身不需再使用 4CT。

因此 Σ(B)=Σ(G)。保留原 disk drawing，B 的外界仍為 C5，各 bounded face 邊界為 simple cycle。
對 B 選取 §2 的 c 和 e。

### 3.2 保留 c 的逐面補完

處理每個長度大於三的內面，依其當前邊界環序操作：

1. 若存在一個頂點，其前後鄰點顏色不同，就在面內連此前後鄰點，切下一個 properly colored triangle，
   然後在剩餘 polygon 繼續。
2. 若所有前後鄰點都同色，環上的顏色以週期二交替。properness 保證恰用兩色，長度為偶數。
   在此剩餘面放一個新 hub，選一個未使用色，連到所有剩餘 boundary vertices。

每步縮小 polygon 或結束；最多每個原內面增加一個 hub。所有新三角形保持 proper coloring，
新增邊都在指定面內，因此得到 plane near-triangulation H 且 c 能延伸。
若欲加入的邊在其他面外側已存在，保留一條新的平行邊；不加入 loops。
一般計數恆等式的 inclusion–exclusion 證明也適用於平行邊，因為它仍逐邊求和，
component partitions 仍 noncrossing。

此 H 滿足 §2，故仍是 adjacent-singleton 反例。H 的內點數可能增加；沒有宣稱有界大小歸約，
也没有宣稱某個任意 triangulation completion 保留 Σ。

**結論**：只要在上述 near-triangulation 類別（包括平行邊）證 adjacent-singleton lemma，
就能推出原任意簡單 disk cell 的引理。更強的文獻 Conjecture 9 也足夠：它要求 m≤0，
而反例保持引理給出 m>0。

## 4. 已得到的有界排除與未解範圍

對有 k 個內點、boundary C5 的 near-triangulation H，即使有平行邊，Euler 計數仍給

\[
|E(H)|=3(k+5)-8,\qquad |V(H^*)|=|F(H)|=2k+4.
\]

dual 的 outer-face vertex degree=5，其他 face vertices degree=3，符合文獻 near-cubic 類別。
由引用的 Corollary 20，2k+4<30 時 m≤0。因此 **k≤12 的 near-triangulation 不可能是
本題反例**；任何這類反例至少有 13 個內點。此為文獻定理加上述紙面推導，非本倉庫新枚舉。
不能把此界直接套到未補完的一般 disk 圖：§3 可能增加頂點。

主引理只是 support 限制，比完整計數不等式所要求的資訊少。例如抽象向量 y_i=1、x_e=4
滿足既有計數恆等式與 adjacent-singleton 結論，但 m=1。這個代數例子不聲稱是圖計數，
只說明不可把兩個 statement 當成純代數等價。

**下一個精確目標**：在 near-triangulation 中，排除 `P⊆e 且 x_e>0`。
可以只證此特殊 support 分支，不必先證所有圖上的 m≤0。上一輪 blocking paths 可在這個
三角面背景下重看；仍必須處理共享色頂點與換色後 connectivity，尚無新的路徑矛盾證明。

## 5. 有限驗證與信任邊界

[checker](../scripts/c5_count_cone_bridge.py)／[JSON 證書](../artifacts/c5_cells/count_cone_bridge.json)：

- 全部 240 個 proper boundary assignments 與 60 個 parity edge words，逐一確認四對一和十個類別對應。
- 六個線性基底座標檢查 slack=−5m；11 個 independent supports 全有 containing chord。
- 132 個舊 witness counts 的記號轉換，及 11 個舊抽象例子的 slack −5。
- 長度 3..9 的全部四色 polygon color orbits，檢查補完後三角形顏色、定向邊 incidence、Euler characteristic；
  刪除三角形的負控制會被拒絕。一般長度的成立理由是 §3 的歸納，不是這項有限測試。

checker 不證文獻 Conjecture 9，也不替代 block decomposition、disk embedding、dual integration
的一般數學證明。本輪沒有新 Lean 模組、沒有重跑大圖 catalogue、沒有改 production 或 cells.json。

```bash
python3 scripts/c5_count_cone_bridge.py --check
python3 scripts/c5_adjacent_singleton_counts.py --check
python3 scripts/c5_kempe_screen.py --check
git diff --check
```
