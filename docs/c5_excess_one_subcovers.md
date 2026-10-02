# ε=1：四容量子覆蓋共享、933 的 ε≥2 與 941 的單 binary 殘餘

**後續（2026-10-02）**：[941 single-spoke 來源排除](c5_941_single_spoke.md)
已以兩個原省略核心的共同三葉支援及原邊完整 relation 排除 t=1、(2,1,1)。
[Two-spoke 接回排除](c5_941_two_spoke.md)再完成 t=2、(2,1)，
[three-spoke 排除](c5_941_three_spoke.md)完成最後 t=3、(2)，故 933、941
現均已證 ε≥2；下文保留本輪三型殘餘及當時停止點。

2026-10-02，基準 `1274894`，接續尚未提交的
[容量與跨度下界](c5_independent_support_capacity.md)。沿用**固定完整 Σ 的
edge-minimal disk source**；目前停止點見 [Kempe 導覽](c5_kempe_guide.md)。

**新下界：933 必有 ε≥2。941 仍只有 ε≥1，但其 ε=1 來源若存在，必恰有
一份二接點原分量，其餘三條 root incidences 都是單容量因子。**
941 的唯一 degree-5 root 有 t=1、2 或 3 條 spokes，原分量接點分拆依序是
`(2,1,1)`、`(2,1)`、`(2)`。沒有排除兩候選的一般來源，也沒有證 941 的 ε≥2。

本輪的共享限制來自同源十列及單接點未用色守恆，不把跨列跨度直接相加。
任意大小結論是紙面合成，依賴既有全 degree-4 分類、degree-5 指定雙列
分離、sector 分類及其外部 degree-list／有限拓撲證據。新增 Python 只做
有限集合控制與一張既有圖的完整重播；無新 Lean theorem、無新圖枚舉。

## 1. 同源因子、真子核心與省略區域

G 接受 T4，完整 Σ 為 933 或 941；B 是指定有序 C5 外框。
反設 ε=1，沿用前報：有效內部 H 連通，唯一高 degree 點 r 的完整 degree=5，
其餘內點完整 degree=4；所有 minimal rejected-row cores 都含 r。

保留 H−r 的原分量 C、全部實際附件及有序接點 P_C。因子族 \(\mathcal F\)
包含每條具名 root-spoke，以及每份完整原 C。spoke 的容量為 1、禁色為
\(\{b(v)\}\)；C 的容量 \(k_C=|P_C|\)，禁色為

\[
F_C(b)=\bigcap_{t\in R_C(b)}\{t(p):p\in P_C\},\qquad |F_C(b)|\le k_C.
\]

R_C 始終是原圖全部接點的完整有序 relation。所有列共用同一圖、因子身份
和色框；F 只是共同 root 色查詢的精確投影，不用端點 marginals 取代 R。
容量總和為 5，拒絕 b 恰等價於所有具名因子的禁色聯集為 U。

對容量一因子 i，G\i 表示刪除該 spoke，或省略整份單接點原分量及其
全部 incident 邊；孤立點忽略。稱 q 有**真子核心**，若有 minimal q-core
嚴格小於 G。前報的 degree-4 飽和給出：

- 每個真子核心恰為某個 G\i，且 r 在其中 degree=4。
- 容量至少二的原分量出現在每一個 minimal core 中。
- 若沒有真子核心，G 自己就是 minimal q-obstruction。

### 1.1 一個省略身份只能屬於一個拒絕列

若 G\i 拒絕 q，它繼承 T4，且有效內部全 degree=4、連通。任取其
minimal q-core：degree-4 飽和沿有效內部傳播，必取整張 G\i。
所以 [全 degree-4 合成](c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論) 給

\[
\Sigma(G\setminus i)=\Omega\setminus\{q\}. \tag{1}
\]

因此不同拒絕列的省略身份集互不相交；同一列可能有兩個省略身份。
若有 a 個不同列具真子核心，原圖至少有 a 個不同的單容量因子。
這是在同一原圖比較完整十列，不是只檢查某列的色數。

分量解除引理又使刪除原 C 的任一 incident 邊，與關閉整個 C 因子在
全部十列上等價；這不表示任意刪邊後的圖仍符合原 degree 條件。

### 1.2 每列的精確四容量分類

固定一個拒絕列 q。前報的 D+O=1 只有下列情形。

| 預算 | 因子結構 | 四容量省略身份 |
| --- | --- | --- |
| D=1、O=0 | 唯一因子少一個禁色，其餘飽和且禁色互斥 | 缺額因子容量為一時，恰可省略它；否則沒有 |
| D=0、O=1 | 全部飽和，恰一色出現在兩個不同因子，其餘色各出現一次 | 恰為那兩個因子中容量一者 |

證明：禁色總大小分別為 4、5，聯集大小為 4。省略容量≥2 者只剩容量≤3，
不可能仍覆蓋 U；在第二列，容量一重色因子正好沒有私有色。故任一列
至多有兩個真子核心，且沒有省略身份時每個因子都有私有色。
配合分量解除引理，後者恰使每條非框邊都是 q-critical。

## 2. 只用 T4 的 minimal degree-5 相鄰列分離

本節抽出既有結果的正確共同推論：

> 若 M 是 T4-accepting disk minimal q_i-obstruction，恰有一個 degree-5
> 內點、其餘 degree-4，則 M 接受 q_{i−1} 和 q_{i+1}。

此處**沒有假設 M 恰缺兩列**。不能直接引用帶該前提的單側出口定理；
要分別核對它的來源分離引理。

共同對齊 q=01012，兩個相鄰 singleton 列為 p₁=01021、p₂=01212。
minimality 使 root-spokes 在 q 下異色，故 t≤3。

| t | 只需 T4／minimal q 的來源結果 |
| --- | --- |
| 2 | [非相鄰 two-spoke 分離](c5_two_spoke_nonadjacent.md)及其相鄰來源排除／split-support 前序，接受兩個指定 p |
| 1 | [(2,1,1) 單接點完成](c5_single_spoke_single_contact_bounds.md)、[(2,2) 局部 residual](c5_single_spoke_residual_locality.md)；(3,1)、(4) 已作來源排除 |
| 0 | [(2,1,1,1) 支援分離](c5_no_spoke_supports.md)、[(2,2,1) 首橋／框弧](c5_no_spoke_first_bridge.md)；其餘四型已作來源排除 |

### 2.1 三-spoke 不必要求其餘列接受

[區域化約](c5_degree5_sectors.md)只用 T4 與 minimal q，給
`S={b0,b1,b4}`、C 位於長弧 1234，及 F_C(q)={D}；反射型共同搬運。
令 x 為原 sector 的十二開口列，則

\[
x_0=x_{10}=x_{11}=1,\quad x_7=0,\qquad
y_1=x_3\vee x_8,\quad y_6=x_6.
\]

- 若 p₁ 拒絕，則 x₃=x₇=x₈=0，直接違反
  [3703 三拒絕定理](c5_sector_3703_exclusion.md#1-前提與結論)。該定理不要求
  其餘九列接受。
- 若 p₂ 拒絕，則 x₆=x₇=0；[雙拒絕分類](c5_two_rejection_proof_zh.md#0-精確命題與適用範圍)
  迫 sector 的實際圖為指定二內點 edge，因而 x₁₁=0，違反 F_C(q)={D}。

這補明了三-spoke 的前提差異，不以舊五目標表的完整 y 條件代替論證。
因此上面的 minimal degree-5 分離推論對全部 t 成立。

### 2.2 候選中哪些列必有真子核心

令 Q 為拒絕的 singleton 位置。若 i∈Q 且 i 的某個框鄰點也在 Q，
G 不可能是 minimal q_i-obstruction，故 q_i 必有真子核心。

| Σ | Q | 必有真子核心 | 仍可能以 G 為 minimal core |
| --- | --- | --- | --- |
| 933 | {0,1,2,3} | 0、1、2、3 | 無 |
| 941 | {0,1,3} | 0、1 | 3 |

這只判定 core 形態；尚未從兩列分離推出任何候選的完整 Σ 不可能。

## 3. 全 degree-4 核心在共同 root 的局部限制

沿用 [全 degree-4 合成](c5_k4_blocks.md)：有效內部為路徑、單 triangle
加不分叉路徑枝，或兩個頂點互斥 triangles 由一條直接 bridge 相連。
這裡只使用以下原圖結構，不收縮或替換有標記的 root：

1. 不在 cycle 上的內點，其內部 degree 至多二。
2. 一個內點至多在一個 triangle 上；在 triangle 上至多另接一條 bridge。
3. Triangle 的 obstruction palette 含未用色 D。

依賴分別是 [樹核心](c5_tree_cores.md)、[triangle 分叉排除](c5_triangle_forks.md)、
[triangle 接枝](c5_triangle_branches.md#1-任意大小的單-triangle-核心接枝位置限制)
及 [雙 triangle 分類](c5_two_triangle_blocks.md)。長奇圈／K4 由合成的前序排除。

所以只要 G 有一個真子核心，任一被保留原 C 都滿足 k_C≤2，而且至多
一份 C 有 k_C=2。r 及 C 的兩個原接點構成該核心的一個 triangle block；
C 的其餘原頂點及旁支仍保留。其飽和禁色恰是該 block 的二色 palette，包含 D。
單接點分量的 root 邊是 bridge；不把它當成新添 spoke。

## 4. 單接點分量的跨列 D 身份不能互換

所有五個三色 canonical rows 都用 {0,1,2}，共同未用色 D=3。
固定同一原單接點 C，唯一接點為 v。若 F_C(q)={a}、F_C(p)={b} 都非空，則

\[
\boxed{a=D\quad\Longleftrightarrow\quad b=D.} \tag{2}
\]

套用 [單接點固定色引理](c5_single_spoke_root_conservation.md#2-單接點固定色引理)：
固定 root 色 a、b 後，兩份拒絕 lists 各有 tight Gallai block-palette 證書。
在所有非接點，D 都在 list 內；接點的 D membership 分別是 a≠D、b≠D。
同一 block-cut tree 由葉向根歸納迫這兩個 membership 相同。

該歸納只用各 block 共同 palette 與在割點的不交聯集；即使先不套 K4
排除，clique blocks 也遵守相同歸納。singleton C 的兩份 tight lists 都為空。
因此不需要 q 或 p 在整張 G 中 minimal，也不需要原報告的指定支援 012。

F_C 可以在某列變空；(2) 並未保證每列都禁止一色，也未保證非 D 色名
守恆。我們只在已有非空拒絕證書的列使用同一個 D／非 D 身份。

## 5. 五個單容量因子不可能拒絕三個 singleton 列

假設所有 k_C=1；root-spokes 也是單容量，所以共五個具名因子。
每個拒絕列的五個空／singleton 集覆蓋四色，必有冗餘因子。
由 §1，每個拒絕列都有真子核心。

首先 t≤3：若有四條 spokes，可取一個 T4 列，使這四個框鄰點互異色，
立即阻斷 r。具體地，把唯一未選框點與其一個非相鄰框點同色，其餘各異色。

若 t≤1，省略一個因子後，r 仍有至少三條通往不同原 C 的 bridge，
卻不在任何 cycle 上，違反 §3.1。所以只須 t=2 或 3。

### 5.1 t=2：三份原分量的奇數矛盾

原分量為 C₁、C₂、C₃。省略 spoke 仍保留 r 的三條內部 bridges，不可能
是全 degree-4 minimal core；所以每個拒絕列只能省略某個 C_i。

若有三個不同拒絕列，(1) 迫它們各自使用三個不同省略身份。
令 q_i 為省略 C_i 後仍拒絕的列。在該四容量覆蓋中，兩條 spokes 和
另兩份 C 必各禁一色且四色互異。spokes 不含 D，所以另兩份 C 恰有一份禁 D。

每份 C 在另外兩列都非空，以 (2) 定義固定 d_i∈{0,1} 表示其禁色是否為 D。
三列遂同時要求

\[
d_2+d_3=d_1+d_3=d_1+d_2=1.
\]

相加給 2(d₁+d₂+d₃)=3，矛盾。這是原分量跨列共享的限制，沒有把不同
完整染色合併，也沒有為每列獨立重命名 C_i。

### 5.2 t=3：rainbow 列與重色 spoke 列

只有 C₁、C₂ 兩份原分量。對 root 的三個框鄰點：

- 若它們在 q 下三色互異，拒絕恰需某份 C 禁 D。這時只保留該 C 和三條
  spokes 已拒絕，故每份 C 最多承擔一個這樣的列，由 (1) 知總共至多兩列。
- 若只有兩色，拒絕迫 C₁、C₂ 分別禁 D 與尚未被 spokes 禁止的已用色。
  三條 spokes 的一個同色 pair 都可各自省略。

兩個不同的第二類列，其同色 pair 都是三個具名 spokes 中的二元子集，
必有共同 spoke；省略它便仍拒絕兩列，違反 (1)。故第二類至多一列。
若有第二類列，(2) 又把兩份 C 固定成一份 D 身份、一份非 D 身份，第一類
便至多一列。若沒有第二類，第一類本來至多兩列。

因此在全部情況下

\[
\boxed{\text{ε=1 且所有原分量單接點}\ \Longrightarrow\ |Q|\le2.} \tag{3}
\]

這不是完整 Σ 分類，也未證兩個拒絕位置必相鄰；它足以排除本題兩個候選
的此一來源分支。證明不需新的六跨度配置。

## 6. 新下界及 941 的精確殘餘

### 6.1 933：ε≥2

由 §2，933 的四個拒絕列都有真子核心。由 (1)，至少需四個不同單容量
因子。總容量只有五，若有容量≥2 的因子，最多只剩三個單容量因子。
所以所有因子只能全為一，違反 (3)。因此 ε=1 不可能；連同前報 ε≥1，得

\[
\boxed{\Sigma(G)=933\quad\Longrightarrow\quad\varepsilon(G)\ge2.}
\]

同一結論可隨整圖 D5 重標搬運到該 orbit；未聲稱 ε=2 可實現，也未排除 933。

### 6.2 941：恰一份共同二接點原分量

q₀、q₁ 必有真子核心。§3 迫每個 k_C≤2 且至多一份 binary C；
(3) 排除全單接點，所以恰一份 C₂ 有 k=2，另外三份因子容量各一。
由 §3.2，t=0 時省略任一 unary 後，r 仍為 triangle 上接兩條 bridges，
不可能。因此只餘：

| root-spokes t | 原分量接點數 | q₀、q₁ 的不同省略身份 | q₃ |
| --- | --- | --- | --- |
| 1 | (2,1,1) | 恰為兩份 unary C 的各自身份 | 必以整張 G 為 minimal core |
| 2 | (2,1) | 兩條 spokes／一份 unary 中的不同身份 | 真子核心或整圖 |
| 3 | (2) | 三條 spokes 中的不同身份 | 真子核心或整圖 |

t=1 不能省略唯一 spoke：否則 r 在 triangle 上仍接兩條 bridges。
q₀、q₁ 已用盡兩個 unary 省略身份，(1) 排除 q₃ 的真子核心。

在 q₀、q₁，每份四容量子覆蓋都保留同一 C₂；它飽和，且 §3 給

\[
|F_{C_2}(q_0)|=|F_{C_2}(q_1)|=2,\qquad D\in F_{C_2}(q_0)\cap F_{C_2}(q_1). \tag{4}
\]

每份 unary 至少在 q₀、q₁ 其中一列被保留，因兩列的省略身份不共用。
其禁色非空且不是 D；由 (2)，它在任何三色列都不能禁 D。因此 q₃ 的 D
亦必由同一 C₂ 承擔：

\[
F_{C_2}(q_3)=
\begin{cases}
\{D\},&G\text{ 是 minimal }q_3\text{-core};\\
\text{包含 D 的二色集},&q_3\text{ 有真子核心}.
\end{cases} \tag{5}
\]

第一種由 §1.2：只有一份非單容量因子，重疊必使某個單容量因子可省略；
要全圖 minimal，只能把唯一缺額放在 C₂，其禁色大小為一。第二種是四容量
覆蓋的飽和性。這也表明沒有把 q₃ 的 binary 拆成兩份可獨立選色的 unary。

**目前停止點：** 下一步固定同一 C₂ 的兩個有序接點、全部原附件及三個
具名單容量因子，研究完整十列能否同時滿足 (4)、(5)、T4 與接受 q₂、q₄。
優先 t=1 的「兩份二色飽和列＋一份 singleton-D minimal 列」，連同其原
unary 省略見證。尚未證此必要介面可實現，也尚未排除它。

## 7. Checker、實際驗證與信任範圍

[Checker](../scripts/c5_excess_one_subcovers.py) 與
[artifact](../artifacts/c5_excess_one_subcovers/observations.json) 保存：

- 容量五的七種整數分拆中全部四色覆蓋，核對 §1.2 的缺額／重疊分類。
- 120 組具名 spokes／原分量 D 身份的 Boolean 放寬模型；完整跑五個三色列，
  省略身份不能跨列重用，最多兩拒絕。此層不生成圖、附件或來源 tuples。
  移除 D 守恆的抽象三拒絕控制亦保存，不能當作 disk 反例。
- 三-spoke 的十二列接合蘊涵；僅核對 Boolean 代數，sector 拓撲仍由既有
  任意大小紙面定理承擔。
- 既有 `943/k3-t382/submask 2045` 原圖的全部十列、原有序 contacts／tuples、
  tuple colorings，以及 16 個具名因子子集的 160 次完整染色接合核對。
  兩個真子核心恰省略 spoke 05、15；保留 root=5 及原 C={6,7}。

```bash
python3 scripts/c5_excess_one_subcovers.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_one_subcovers.py --check
python3 scripts/c5_independent_support_capacity.py --check
python3 scripts/c5_single_spoke_root_conservation.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際檢查與未重跑的依賴見 [本輪紀錄](history/2026-10-02-excess-one-subcovers.md)。
新有限控制不重新證明全 degree-4 topology、degree-5 指定雙列分類或外部
degree-list 定理。943 的 disk rotation 沿用既有來源。新下界沒有進 Lean；
一般 adjacent-singleton lemma、共同出口及 K∞=K≤5 都仍未證。
