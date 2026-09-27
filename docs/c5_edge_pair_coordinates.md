# C5 的代數—位置座標：十態、二十條 Kempe 蘊涵與研究界線

2026-09-27。來源為使用者提出的 Galois／Klein 四元群研究角度。
本頁整理並接續 [研究目標](c5_boundary_relations.md)、[Kempe screen](c5_kempe_screen.md)、
[計數恆等式](c5_adjacent_singleton_counts.md) 與 [count-cone bridge](c5_count_cone_bridge.md)。
研究優先序見 [HANDOFF](HANDOFF.md)。

**2026-09-27 後續：** [同染色有序重接](c5_dual_path_surgery.md) 已證 §5 所提的一步更新公式，
並以同一 induced-C5 圖證明三份 boundary matchings 不足以決定後繼；record 110 新增共同切口必要等式，仍未排除。

**完成範圍**：十態的邊位置對座標、完整換色／D5 搬運規則，以及舊 Kempe screen 的
20-clause 等價表示。證據為紙面代數推導＋Python 固定域證書；未新增 Lean theorem。
新座標沒有增加已知排除力，任意 disk 的可實現性、單側出口及 `K∞=K≤5` 仍未證。

## 1. 應借用的 Galois 方法

有用的是建立「存在解」與「結構障礙」間的精確橋接。全域顏色群 S4 的可解性
不保證四色可染：K4 與 K5 的限制同樣尊重 S4，但只有前者可四色染色。

四色取值於 V=F₂²，以 0,1,2,3 表示，群加法為 XOR。對連通圖令

\[
d(uv)=c(u)+c(v).
\]

proper coloring 等價於 d(e)≠0；每個 cycle 的 d 和為零。反之，所有 cycle 和為零
保證沿路徑積分與路徑選擇無關，固定一個頂點顏色便唯一恢復 c。
因此是「染色模全域平移」與「非零 exact edge labels」的雙射；未商平移前每個 d 有四個原像。
一般不連通圖要逐分量固定根色，不能只保留一個全域平移。

在連通 plane graph，face boundary walks 生成 cycle space，橋在面邊界重複兩次而抵消。
primal face 的守恆正是 dual vertex 的 V-flow 守恆。三角面對應三價 dual vertex，
三條非零標記必為 1,2,3 各一次。一般非三角面只給守恆，不能冒稱 dual 三價。
線性守恆的零解永遠存在；真正染色問題還要求每條邊非零。

Bar-Natan 的確提出與 4CT 等價的 Lie-algebra 命題，見
[原文 Statement 1／Propositions 1.2–1.3](https://www.math.toronto.edu/~drorbn/papers/4CT/4CT.pdf)。
這是背景等價表述，沒有替本題證出新的 boundary-extension 結論。

## 2. 十態的自然座標與完整對照表

固定有標號的 boundary vertices v₀,…,v₄，**edge position i 指 eᵢ=vᵢvᵢ₊₁**。
對 proper b 設 dᵢ=bᵢ+bᵢ₊₁。若三種非零差的重數為 n₁,n₂,n₃，則
Σdᵢ=0 等價於三個重數同奇偶。總數為 5，因此三者皆奇數，重數必為 (3,1,1)。
定義 P(b) 為兩個少數差所在的 edge positions。

所有色置換唯一寫成 x↦Ax+t：平移有 4 個，可逆線性 A 有 6 個，合計 24 個不同置換，
恰為 S4。取差後 t 消失，GL(2,2) 任意置換三種非零差。
所以 P 在 S4 下不變；反之同一 P 的兩個 edge words 可由某個 A 對齊，
積分後再由 t 對齊頂點顏色。故

\[
\{\text{合法 } C_5 \text{ 邊界染色}\}/S_4\;\cong\;\binom{\mathbb Z_5}{2}.
\]

以下 bit 順序完全沿用 `cells.json`，沒有重新編碼既有 masks。

| bit | boundary pattern | XOR word | P：edge positions | 頂點色數 |
| --- | --- | --- | --- | --- |
| 0 | 01012 | 11132 | {3,4} | 3 |
| 1 | 01021 | 11231 | {2,3} | 3 |
| 2 | 01023 | 11213 | {2,4} | 4 |
| 3 | 01201 | 13211 | {1,2} | 3 |
| 4 | 01202 | 13222 | {0,1} | 3 |
| 5 | 01203 | 13233 | {0,2} | 4 |
| 6 | 01212 | 13332 | {0,4} | 3 |
| 7 | 01213 | 13323 | {0,3} | 4 |
| 8 | 01231 | 13121 | {1,3} | 4 |
| 9 | 01232 | 13112 | {1,4} | 4 |

少數位置相鄰對應三色；不相鄰對應四色。可由兩種 D5 位置型的代表積分直接證明。
若三色 singleton 在 vertex i，則 P={i−1,i}。
四色的 P 不是其重複色 **vertex pair**，兩種 pair 不可混用。

共有 240 個固定色名 proper assignments，每個 S4 orbit 有 24 個：C5 至少用三色，
固定三個使用色的置換只能是 identity。edge words 共 60 個，每個有四個 assignments 原像。

## 3. 反射、黏合與色框

採 active convention：原 vertex i 被送到 ρ(i)。旋轉 ρ(i)=i+r 將 edge i 送到 i+r；
反射 ρ(i)=r−i 則將 edge i 送到 r−i−1，**不能直接沿用 vertex 公式**。
例如主線的 ρ(i)=3−i，在這裡對應 edge i↦2−i，故 q=01012 的 P={3,4} 固定。
本輪只核對座標搬運，沒有重新枚舉既有反射側的來源 minors。

令 HΣ 為五個 edge positions 上的普通圖，以 P∈Σ 作為邊。這只是完整十 bit Σ 的無損畫法；
它不是原 disk graph 的子圖或 minor，HΣ 的邊也不是內部 Kempe paths。

若 G、H 的私有內部不交，且只沿完整對齊的 C5 黏合，則

\[
\Sigma(G\cup H)=\Sigma(G)\cap\Sigma(H).
\]

同一 orbit 的具體 assignment 可由全域色置換對齊，足以證上式。
對固定 boundary assignment 的延伸數 N_G(P)，還有

\[
\#\mathrm{Col}_4(G\cup H)=24\sum_P N_G(P)N_H(P).
\]

但對只共享部分接點的兩個 components，分別取 S4 商會丟失相對色框；必須先在共同色框中
接合完整有序 tuples，再投影。邊差表不授權把 C₂ 的二元關係換成兩個獨立 marginals。
本頁十 bit masks 也不是 sector 文獻中的十二 bit masks，例如 3703、3903。

## 4. 本輪推進：Kempe 必要條件化為二十條蘊涵

給定 P={j,k}，先固定 k。從 cyclic edge positions 中刪掉 k，剩下四個位置依原環序形成 C4。
令 r₋、r₊ 是 j 在這個 C4 中的兩個鄰點。必要條件為

\[
\boxed{\{j,k\}\in\Sigma\quad\Longrightarrow\quad
\{r_-,k\}\in\Sigma\ \lor\ \{r_+,k\}\in\Sigma.}
\]

每個無序對有兩種 fixed endpoint，故共 20 條。等價地：對每個 k，HΣ 中的鄰點集合
N(k)，在上述 C4 上誘導的圖不能有孤立點。允許空集、相鄰兩點、任意三點、四點；
不允許單點或對角兩點。這是必要條件，不是 disk realization 判準。

### 4.1 near-triangulation 上的直接幾何解釋

固定一個完整染色，取 dual 並移去 outer-face vertex，保留五條 boundary half-edges。
除無內部端點的退化 strand 外，所有內部 vertices 三價，incident colors 恰為 a,b,c。
假設 a 出現三次，b 在 j、c 在 k。保留 a,b 邊後，每個內部 vertex 度數 2，
boundary ends 恰是刪掉 k 的四個位置，故由 disjoint paths 成對連接，另可有 closed cycles。
平面性只容許四點的兩種 noncrossing perfect matchings；j 的 mate 只能是 r₋ 或 r₊。
交換 j 到 mate 路徑上的 a,b，使少數 b 位置由 j 移至 mate，c 留在 k。
所得 edge coloring 仍 proper，積分回 primal coloring，得到上式。
這是 dual edge-color path switch，不應不經證明等同於一次 primal vertex Kempe switch。

### 4.2 一般 disk 圖的證據鏈與有限等價

一般 disk 不假設三角化。沿用 [Kempe screen §2](c5_kempe_screen.md#2-kempe-必要性為何與內點數量無關)
已證的必要性：每個 boundary pattern、每個 complementary split，存在 noncrossing
boundary-component partition，其全部獨立交換結果都在 Σ。
新 checker 直接按 edge positions 生成 20 條，獨立呼叫舊 partition generator，並在
全部 **1,024** 個 masks 上比對二者接受與否。結果完全一致。
因此一般 disk 的推導是「既有任意大小紙面必要性＋固定域完整等價證書」。
未將 §4.1 的三價前提套到一般圖，也未新增 Lean topology 證明。

例如 q=01012 對應 {3,4}，兩條要求是

\[
q\in\Sigma\Rightarrow(01023\in\Sigma\lor01212\in\Sigma),
\qquad
q\in\Sigma\Rightarrow(01021\in\Sigma\lor01213\in\Sigma).
\]

它們以「q 已接受」為前提；主線的 q-obstruction 拒絕 q，不能倒用這兩條直接推出出口。

### 4.3 實際結果：更簡單，沒有更強

| 篩選 | 非空關係數 | 證據 |
| --- | ---: | --- |
| 全部 | 1023 | 十 bit |
| 二十條蘊涵 | 153 | 與舊 Kempe screen 完全相同 |
| 加已知外側 132 relations 的非空相交 | 142 | 有限比對；一般必要性另依賴 4CT |
| 扣掉已知 132 個實現 | 10 | 原有未決候選，沒有新排除 |

尤其 T4 在 HΣ 中恰是五條對角邊。對每個 k，它的兩個 T4 鄰點在刪 k 後的 C4 上相鄰；
補入任意其餘鄰點也不會產生孤立點。因此 **全部 32 個包含 T4 的 masks 都通過**。
這個紙面觀察直接解釋本方法為何不能單獨解決 adjacent-singleton 問題。

## 5. 計數層與下一個真正的橋接

舊計數定理已给出五個 vertex chords uv 的共同值

\[
x_{uv}+y_u+y_v=L,\qquad
x_{uv}=m+\sum_{i\notin\{u,v\}}y_i,
\quad m=L-\sum_i y_i.
\]

這是任意 disk 的既有紙面定理；係數代數已有 [C5Counts.lean](../Math/C5Counts.lean)。
新 edge-pair 表只是重排這十個座標，沒有產生額外線性恆等式。
在 near-triangulation 上，文獻 count-cone 不等式 3Σy≥Σx 等價於 m≤0，
在 [Dvořák–Lidický 的指定 v2](https://arxiv.org/abs/1907.04066v2) 中仍作為猜想，
詳見 [既有精確翻譯](c5_count_cone_bridge.md)。本輪不聲稱已查清所有後續文獻或證明該猜想。

研究可具體化為以下兩層，但目前沒有證明它們足夠：

1. 對三角化 disk 的**同一個完整 dual coloring**，同時保留三個 two-color path matchings。
   每次 switch 後，重算另兩色對的真實 paths；不是各自任選一份合法 noncrossing matching。
2. 若要形成可迭代 state，除 boundary P 與三份 matchings 外，還須保留其他 paths 在交換路徑
   上的接合順序；先證交換後資訊可由 state 決定，或給出兩個同 state 不同後繼的反例。
   後續已給出「三份 boundary matchings」不足的同圖反例及一步精確切口公式，見頁首連結；可迭代充分 state 仍未證。

Kempe 可達性與 Σ 的存在性不同；plane triangulations 可以有多個四色 Kempe classes，
見 [Mohar 的原始綜述及構造](https://users.fmf.uni-lj.si/mohar/Reprints/2006/BM06_GTP06_Bondy_KempeEquivalence.pdf)。
沿這條線前進，必須與 [既有 connectivity 研究](c5_kempe_connectivity.md) 的不足對照。

與當前主線的接點是 [single-spoke (2,2)](c5_single_spoke_two_two.md) record 110：
q={3,4}、p₁={2,3}、p₂={0,4} 可用新座標清楚標出，但來源的兩份完整 relations、
bridge paths、實際 tethers 與 cyclic order 仍必須保留。座標本身不排除此 record。
下一個有內容的成果應是同圖來源連接的限制或 minor 證明，而非再次枚舉十態。

## 6. 證書與重播

- [checker](../scripts/c5_edge_pair_coordinates.py)
- [完整 JSON 證書](../artifacts/c5_cells/edge_pair_coordinates.json)

```bash
python3 scripts/c5_edge_pair_coordinates.py --check
python3 scripts/check_docs.py
python3 tools/docgraph check
lake build
git diff --check
```

本輪實際核對：240 assignments、60 edge words、5,760 色置換等變檢查、
2,400 D5 搬運檢查、1,024 個 mask 判準等價、32 個 T4 supersets。
證書記錄十態表、全部二十條、153／142／10 的固定標號清單及來源 SHA-256。
132 個 catalogue keys 只讀取比對，未重新驗證 witness 圖；未重跑圖枚舉。
以上重播均通過：文件檢查 179 頁／2,203 本地連結，DocGraph 0 errors，
`lake build` 成功（8,826 jobs，保留既有 linter warnings）。
未新增 Lean 定理；build 只作既有形式化的整合檢查，不認證本頁新紙面推導。
