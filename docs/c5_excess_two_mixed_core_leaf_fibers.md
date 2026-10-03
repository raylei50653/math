# ε=2 唯一 mixed：原 leaf 色纖維與五-spoke 來源排除

**提交整理（2026-10-03）**：本頁、checker 與研究紀錄的本次提交範圍、
實際重播及整理發現見 [九輪進展紀錄](history/2026-10-03-excess-two-dual-root-progress-commit.md)。
下文的未提交字句保留當輪語境；即時提交狀態以 Git 為準。

2026-10-03，接手基準 `722bfa6`，保留前序未提交成果。接續
[單 spoke 原附件化約](c5_excess_two_mixed_core_single_spoke.md)的原四點
relation 停止點；目前入口由 [Kempe 導覽](c5_kempe_guide.md)維護，
實際驗證及跨對話摘要見 [研究紀錄](history/2026-10-03-excess-two-mixed-core-leaf-fibers.md)。

**新結論：固定 933／941 的相鄰、唯一原 mixed、ε=2 來源，
原總 spokes 都至多四。** 941 前輪剩下的四組五-spoke 附件及 root
交換全部排除。這是任意大小紙面來源排除，加完整關係／palette／
minor 的 Python 控制；**單 spoke 省略仍未全排，ε≥3 未證，未新增
Lean theorem。** 沒有重新枚舉一般來源圖。

## 1. 同一原圖與共同標準框

完整沿用前輪前提：G 有限簡單，B=(b₀,…,b₄) 是指定有序 induced-C₅
disk 外框；完整 Σ 是 933／941 或整圖 D₅ 像，刪每條非框邊都嚴格
擴大 Σ。有效 H 非空連通，恰兩個完整 degree-5 roots，相鄰且有
原 root 邊；其餘有效內點完整 degree 四。刪兩 roots 後恰一份原
mixed C，其餘為原 unary。保留全部原分量、實際附件、ownership、
接點次序、原嵌入及同一字面四色框。

前輪已證 933 的總 spokes≤4、941≤5；941 的五-spoke 型只餘
(012,03)、(014,13)、(034,13)、(123,03) 及 root 交換。三-spoke
側記 a，二-spoke 側記 b。必為原 C incidence-(1,1)，另有 b 側
原單接點 unary U。原 a–C contact 記 x、b–C contact 記 y；容許
x=y，始終是同一原頂點。U 的原 contact 為 u。

對整張 G 作一次 D₅ 搬運，全部原列、附件及 colors 同步搬動，八份
有序支援都化到

\[
N_B(a)=\{1,2,3\},\quad N_B(b)=\{1,4\},\quad
q=q_4=01012. \tag{1}
\]

完整 Σ 的必要像只餘 **998、1004**，拒絕 singleton 集依序是
{1,2,4}、{1,3,4}。不是每份分量獨立選一個 orbit。

在 q 下，a 的原 spokes 1、3 同色。兩份原省略圖 M₁=G−ab₁、
M₃=G−ab₃ 都仍拒絕 q；前輪 (4,4) 排除迫它們自己是以 b 為
唯一 degree-5 的 minimal q-core。Mₑ−b 的原 binary 是 K=C∪{a}，
原有序 contacts=(a,y)，a 是 leaf；另一分量就是同一原 U。
Two-spoke 區域定理給

\[
N_B(C)\subseteq\{1,2,3,4\},\qquad
N_B(U)\subseteq\{0,1,4\}. \tag{2}
\]

因 a 保留 b₂ 這條原邊，K 必在五邊形側，U 在四邊形側。
b 的 q-available colors 是 {0,3}。固定 b=0 沒有減少 leaf a 的
二色 list，連通 slack-list 貪婪引理使 K 可染；minimal q-core 的
singleton 禁色分配遂迫

\[
F_K(q)=\{3\},\qquad S_U(q)=\{0\}. \tag{3}
\]

S_U 是原 U 的完整 endpoint 色集，不是可任選的禁色 schedule。

## 2. 原四點聯合關係及精確 leaf 纖維

任意 proper boundary coloring β，令 R_C(β;x,y) 為同一原 C 的
完整有序 relation，S_U(β) 為同一原 U 的完整 endpoint relation。
兩者均非空：未固定 roots 時，原 contact 的 list 有 slack。
x=y 時 R_C 只含對角 tuples，沒有把這個原點複製成兩個自由座標。

對 e∈{1,3}，Mₑ 的 K 完整 relation 恰為

\[
R_{K,e}(\beta;a,y)=\{(A,Y):\exists(X,Y)\in R_C(\beta),
\ A\notin\beta(\{1,2,3\}\setminus\{e\}),\ A\ne X\}.
\]

同一 β、同一 b 色下，原四點 relation 是

\[
\mathcal J_e(\beta;b,a,y,u)=\{(D,A,Y,V):
 (A,Y)\in R_{K,e}(\beta),\ V\in S_U(\beta),
\ D\notin\beta(\{1,4\}),\ D\ne A,Y,V\}. \tag{4}
\]

每個 tuple 有同一份 K 全染色及原 U 全染色，僅共用固定 B，再檢查
原 ba、by、bu 邊即可拼接。接回原 spoke 只作字面過濾

\[
\mathcal J_G(\beta)=\{t\in\mathcal J_e(\beta):t_a\ne\beta_e\}. \tag{5}
\]

原 leaf 纖維是固定 b 色後從完整 joint tuples 取出的 a 色集；每份
固定 (b,a) 的整個 (y,u) 纖維另保留，含空纖維。Mₑ 接受只給式 (4)
非空，並不保證式 (5) 非空；checker 保存一張實際全圖的非空 M
纖維全被原 spoke 濾空，以及共同 contact 的 marginal 假接合控制。

## 3. 兩個指定列的完整接合迫同一 U 再次只取 0

記

\[
p_A=q_3=01021,\qquad p_2=q_2=01201,\qquad \pi=(0\ 2).
\]

它們在 U 的全部實際支援 {0,1,4} 上字面相同；在 C 的全部實際
支援 {1,2,3,4} 上恰相差 π。對同一原分量的整份染色換色，得到

\[
S_U(p_A)=S_U(p_2),\qquad R_C(p_2)=\pi R_C(p_A). \tag{6}
\]

兩列的三條原 a-spokes 都見到三色，故原 G 必有 a=3；原 ba 邊後
b 只餘 {0,2}。U 的支援只見 0、1，交換 2、3 必保存它的完整
endpoint relation。S_U 非空，singleton 禁色因而只可能是
∅、{0} 或 {1}。

若禁色為 ∅ 或 {1}，兩個 b queries 0、2 都有原 U 完整 witnesses。
式 (6) 對同一完整 C tuple 把 a=3、b=0 的查詢與 a=3、b=2 的查詢
互換；式 (4)–(5) 遂給 G 對 p_A、p₂ 同時接受或同時拒絕。這裡
只比較接受性，**沒有宣稱 π 搬運整份 joint relation**：U 不必對
π 不變，兩個 queries 各自從同一 S_U 選合法完整 witness。

但 Σ=998／1004 都恰接受這兩列中的一列。因此五-spoke 原來源必有

\[
\boxed{S_U(q)=S_U(p_A)=S_U(p_2)=\{0\}.} \tag{7}
\]

Python 對完整 C tuples 的兩個 guarded-query 位元作窮盡代數核對：
四種位元組合、七份非空且對 (2 3) 不變的 U endpoint 色集，共
28 份完整 joint 接合。這是必要 relation 代數，不聲稱這些 relations
都能由原 degree-4 disk 分量實現。

## 4. 同一原 unary 的雙列 palette 比較

下面的引理不限制 U 大小、奇圈數或 bridge 長度。

> b 有原 spokes b₁、b₄；原連通 unary U 僅接 b 一次，每點完整
> degree 四，實際框支援包含於 {0,1,4}。若原圖 planar，則
> S_U(01012) 與 S_U(01021) 不能同為 {0}。

反設兩者都是 {0}，在**同一原 U**固定 b=0。兩列皆給不可染的
degree lists L_q、L_A；它們至少有 deg_U 色。連通 slack-list 引理
迫兩份都 tight，每個外部鄰色在各列互異。特別是任何 U 點不能
同時接 b₁、b₄，u 也不能接 b₀。

沿用外部 degree-list／Gallai block-palette 定理。B∪{b} 由原 spokes
連通，既有連通外框 K₄ 引理排除 U 的 K₄ block；更大 clique 違反
degree 界。對 p_A，每點的 list 都含 2、3。原 block incidence
columns 的獨立性迫每個 block 的 palette 同時含 2、3 或同時不含。
因此原 blocks 只有 palette {2,3} 的奇圈與 palette {0}／{1} 的
bridges，每點恰屬一個奇圈。列獨立性由 leaf block 的私有點逐層
剝除證明；不是 checker 對有界 graph 的觀察。

從 p_A 改到 q，只有原 b₄ 附件的外部色由 1 改為 2。因此每個點的
list 對 0、3 的 membership 不變。對兩份 palette 聯立，再用**同一**
原 incidence matrix 的列獨立性，逐原 block 的 0、3 membership
都不變，palette 大小則由原 block 決定。故

| 原 block | p_A palette | q palette |
| --- | --- | --- |
| 奇圈 | {2,3} | {1,3} 或 {2,3} |
| bridge | {0} | {0} |
| bridge | {1} | {1} 或 {2} |

尤其每個原奇圈在 q 的 palette 都**不含 0**。取任何一個原奇圈 T，
記其 q palette 為 U_colors∖{0,h}，h∈{1,2}。每個圈點的兩個
圈外原方向，恰一個標 0、一個標 h：直達原外部鄰點，或是相應
singleton-palette 的原 bridge。沒有替換 contact、bridge 或附件。

## 5. 實際 tethers 與原圖 K₅ branch sets

沿用既有 [actual-tether 引理](c5_two_spoke_adjacent_21.md#4-each-labeled-bridge-direction-reaches-the-matching-actual-exterior)：
刪除標 j 的原 bridge，外側 root 可取色非空，且只能取 j；去掉 j
會恢復該側的 tight block assignment。若外側沒有實際外部色 j，
在其整份染色交換 j 與未用色 3 便矛盾。因此方向必有實際路徑
到對應外部色，不同 bridge 外側互斥。對同一原圈 T 可選

- 0-tethers，止於原 b 或 b₀；
- h-tethers，h=1 時止於 b₁，h=2 時止於 b₄。

全部 tethers 的內點互斥、避開 T 和 B∪{b}，直達邊容許零個內點。
當 h=1，外部原路徑 b–b₄–b₀ 把兩個 0 端點接起；當 h=2，使用
b–b₁–b₀。另一個 hub 是相應 b_h（h=2 時為 b₄）。

將 T 分成三個非空連續 arcs V₀,V₁,V₂，構造

\[
O_0=V(b-b_{other}-b_0)\cup\{
\text{全部 0-tether 內點}\},\quad
O_h=\{b_h\}\cup\{\text{全部 h-tether 內點}\}.
\]

五份 branch sets 連通、互斥。三份 arcs 由原圈邊彼此相鄰；每份
arc 各有一條原 tether 到兩個 hubs；兩 hubs 由原 b–b_h spoke
相鄰。這是同一原圖上的十份 K₅ 鄰接，與 planarity 矛盾。
只在最終 minor 識別 branch sets，不宣稱它保持 Σ、degree 或 relation。

故引理排除式 (7)，進而排除八份原五-spoke 支援。連同前輪，得到

\[
\boxed{t_a+t_b\le4\quad\text{對固定 933、941 來源都成立}.}
\]

## 6. 證書、重播與停止點

[Checker](../scripts/c5_excess_two_mixed_core_leaf_fibers.py)／
[artifact](../artifacts/c5_excess_two_mixed_core_leaf_fibers/observations.json)
保存八份整圖具名搬運、全部十列的共同色置換、998／1004 原目標
身份、28 份 full-joint 代數、五份 block palette 選项與八份 degree-4
圈點方向代數。24 份 extracted-shape K₅ 控制取奇圈長 3、5、7、9，
兩種 h、三種原 tether subdivision 長度；逐原邊核對 branch-set
連通／互斥與全部十份鄰接，不用 planarity boolean 作 oracle。
它們不是完整 degree-4 候選來源；任意大小 coverage 由 §4–5 負責。

另有十五張完整原圖，C 為 singleton／edge／triangle，U 為
singleton／edge／path／兩種 triangle。所有原邊、實際附件、contacts、
ownership、十列 C／U／K／(b,a,y,u) 全部 tuples 及 coloring witnesses
都明列。450 次完整 joint 接合與獨立全圖窮盡相同；7,200 次固定
(b,a) 的完整 (y,u) 色纖維含空纖維，與獨立 pinned 回溯相同。
三張同源圖確有 S_U(q)=S_U(p_A)={0}，附各自原圖 K₅ branch sets；
說明双列 singleton 的排除依賴 planarity，不能把代數限制當來源。

```bash
uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_leaf_fibers.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_leaf_fibers.py --check
uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_single_spoke.py --check
uv run --with networkx==3.5 python scripts/c5_two_spoke_adjacent_21.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

信任範圍：任意大小紙面接合與 palette／minor 證明，沿用前輪全
degree-4 排除、two-spoke 區域、外部 degree-list 定理及連通外框
K₄／actual-tether 引理；Python 只核對明列固定域，未新增文獻 oracle。
`lake build` 不形式化本輪 topology、block incidence 或 leaf 證明。

**停止點：五-spoke 原來源全排，兩候選總 spokes 都≤4。** 下一窄
入口是原四-spoke 的 (3,1) 及 root 交換，先固定 mixed incidence-(1,1)
與一-spoke 側兩份原單接點 unary；省略三-spoke 側的同色原 spoke
所得 t=1、(2,1,1) core，保留原 leaf 與兩份原 unary 的完整 joint
relation。其他四-spoke 型、較少 spokes、原 unary 單省略、原 G
自己 (5,5) core 及多 mixed／no-mixed／非相鄰來源保留。單 spoke
省略尚未全排；共同 ε≥2 不變，ε≥3、一般出口、來源實現及
K∞=K≤5 未證。
