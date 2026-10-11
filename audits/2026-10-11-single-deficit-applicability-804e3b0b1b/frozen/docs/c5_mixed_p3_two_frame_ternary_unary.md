# C₃：共鄰 P₃ 雙框點三接點 unary 的原葉 block 與 K₅ 排除

**獨立驗收（2026-10-04，D₅）**：[最終成果固定快照與稽核](../audits/2026-10-04-task-d5/REPORT.md)
只新增關閉(CPP-134-1,34,60)、side IDs=(27,1)；九份自身支援配置、
27份完整relation組合、contacts次序／原bridges及逐份2↔3 lift雙射均核對。
未知w完整relation保持符號纖維；不以整側禁色聯集代替逐分量檢查。
連同C₂／C₃合用恰三keys，3500key ledger及原36／140／900表不刪，
其餘3497keys未關閉。以下各輪正文／artifacts保持，現行入口由weak-deletion導覽維護。

**後續（2026-10-04）**：[C₄ 兩份原 unary](c5_mixed_p3_two_frame_two_unary.md)
已排除 §8 的 geometry34／join60：逐份自身附件固定色 0、1，完整原 lifts
對 2↔3 封閉，與兩份指定禁色 {0,3}／{2} 各自矛盾。原兩份 ownership、
bridges／外路保持；其他 joins 及前層表不刪。以下保留 C₃ 當輪截點。

**獨立驗收（2026-10-04，D₄）**：[正式返回工作區稽核](../audits/2026-10-04-task-d4/REPORT.md)
核實八型strict-list、原T／N葉、五袋十對原邊及全部局部witnesses。
只關閉CPP-134-1／geometry34／join20；3500keys保存，下一入口
geometry34／join60。未知D_w完整relation保持符號纖維，局部partial
witnesses不提升為整份M的逐邊minimality證書。

2026-10-04。接續 [C₂](c5_mixed_p3_one_color_ternary_unary.md) 的具名入口
**CPP-134-1／geometry 34／side_join_id 20**。
**原 z 側三接點 unary 自身支援 {b₁,b₂}、禁色 {0,2,3} 時，
任意大小的原 tight blocks／bridges 與原外路共同迫出 K₅ minor，
因此這份固定側接合沒有 disk source。**

非接點可同碰兩框點而內度二；本輪重新證明葉 block 限制。
原 P₃、全部附件、兩側三接點身份、w 側完整未知 relation、同一色框
及原外路均保留。任意大小證明依賴外部 Gallai 定理與紙面原邊 minor；
Python 保存固定控制及完整 tuples／witnesses，未新增 Lean theorem，0 target。

[Checker](../scripts/c5_mixed_p3_two_frame_ternary_unary.py)、
[證書](../artifacts/c5_mixed_p3_two_frame_ternary_unary/observations.json)與
[本輪歷史](history/2026-10-04-mixed-p3-two-frame-ternary-unary.md)
分別保存可重播程序、具名資料及實際驗證範圍。

## 1. 固定同一來源、接點及完整關係

M 有限簡單，B=(b₀,…,b₄) 為 induced C5 disk 外框，q=01012，
U={0,1,2,3}；H=M−B 非空連通。M 拒絕 q，刪任一非框邊後接受 q。
相鄰 roots z,w 完整 degree=5，其餘內點完整 degree=4。
唯一 mixed 原分量為 C*=x₀x₁x₂，兩側 mixed 接點均為同一原 x₂。

原附件、完整三座標關係及禁對為

\[
S_0=\{b_0,b_1,b_4\},\quad S_1=\{b_1,b_4\},\quad S_2=\{b_4\},
\]
\[
\mathcal T_* =\{(3,0,1),(3,0,3)\},\qquad
F_* =\{(1,3),(3,1)\}.
\tag{1}
\]

case ID=86、local ID=134、branch=1、side IDs=(8,1)。
原 E_z={1}、E_w={1,3}，兩 root 均無 spoke；各側只有一份原三接點
unary。原整側實際支援 A_z={b₁,b₂}、A_w={b₂,b₄}，兩側位於
J=b₁b₂b₃b₄，原框色字串為 1–0–1–2。

記 z 側原分量為 D，有序原接點 P_D=(u₀,u₁,u₂) 互異。
因 z 無 spoke 且只有這一份 unary，D 自身實際支援恰為 {b₁,b₂}。
D 外部只有 z、b₁、b₂，沒有 D–w 或 D–C* 邊。
保留完整原關係 \(\mathcal T_D(q)\subseteq U^3\)，其禁色定義為

\[
f_D(q)=\bigcap_{t\in\mathcal T_D(q)}\{t_0,t_1,t_2\}=\{0,2,3\}.
\tag{2}
\]

w 側原分量 D_w 的有序原接點為 (v₀,v₁,v₂)，自身實際支援 {b₂,b₄}。
其完整原關係 \(\mathcal T_{D_w}(q)\subseteq U^3\) 沿用同一 q，
滿足 \(\bigcap_{t\in\mathcal T_{D_w}(q)}\{t_0,t_1,t_2\}=\{0,2\}\)。
本輪保留這一整份未知關係及其 fibres，未為 D_w 指定替代 tuples。
沒有獨立正規化兩側，也沒有以接點 marginals 拼出來源。

## 2. 禁色 0 先排除接點碰 b₂，恢復最小內度二

令 p(v)=[v∈P_D]、sᵢ(v)=[vbᵢ∈E(M)]，i=1,2。
完整 degree 四與原外部身份給

\[
d_D(v)=4-p(v)-s_1(v)-s_2(v).
\tag{3}
\]

固定原 z=h 時，D 的 lists 為

\[
L_h(v)=U\setminus\bigl(\{h:p(v)=1\}\cup
\{1:s_1(v)=1\}\cup\{0:s_2(v)=1\}\bigr).
\tag{4}
\]

這是原 D 的局部延拓問題，未要求 (h,w) 是整圖可用 root pair。
由 (2)，h=0、2、3 時均不可著色。
對 h=0，重複的外部色只可能來自原 z 與 b₂，故

\[
|L_0(v)|=d_D(v)+p(v)s_2(v)\ge d_D(v).
\tag{5}
\]

若存在 p=s₂=1 的點，連通 D 就有一點 strict list；按距該點
由遠至近貪婪著色，每個先處理的點至少留一個未染鄰點，最後該點
有額外一色，遂可完整染成 D，違反 0∈f_D。
因此

\[
p(v)s_2(v)=0\quad\text{對全部原頂點成立},\qquad d_D(v)\ge2.
\tag{6}
\]

這步排除了原內度一接點，**沒有排除非接點雙框點內度二**。
固定 h=2 時外部色 2、1、0 互異，故 |L₂(v)|=d_D(v)。
使用 [Dvořák 的 Lemma 7／Theorem 10，第 5–6 頁](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)：
連通不可染 degree assignment 使原 D 為 Gallai tree，blocks 為 cliques
或 odd cycles，lists 為 blockwise-uniform；共享 cut vertex 的 incident
palettes 互不相交且聯集為該點 list。原文前提本輪 live 核對。
不需要後面的 critical-graph corollary 或 T4。
證明其實只使用原禁色中的 0、2；3 仍完整保存。

## 3. 原 bridges 與連通外部排除 K₄ blocks

原 z–x₂–b₄ 保留，所以 X₀=B∪{z,x₂} 在原 M 中連通且與 D 不交。
原外部附件端 z、b₁、b₂ 都位於 X₀。

若 K 是 D 的 K₄ block，每個原 v∈K 已用三條 clique 邊，
完整 degree 四只留一個原方向。此方向可直達 z／b₁／b₂；
若進入 D−K，只有一條原邊 vv′，且它必是 bridge：否則另一條
回到 K 的路會使 K 不是 block。不同 K 頂點的外側分量互不相交。

在同一原 L₂ 下刪除 vv′，兩個連通側各有一個 strict endpoint list，
均可貪婪著色。若兩側 bridge 端點有不同可用色便能拼回 D，故
原拒絕迫它們的完整端點可取色集皆為同一 singleton。
若外側完全不碰 z／b₁／b₂，其 lists 全為 U；對整份外側染色
作 S₄ 置換，端點可取全部四色，與 singleton 矛盾。
因此每個外側分量都有原 tether 抵達 X₀。

K 四點有四條在 X₀ 之前互不相交的原 tethers；把 X₀ 及各 tether
的尾段合為 connected hub，配四個 singleton clique vertices，得到
K₅ minor。故 disk source 不可能有 K₄ block。
K₅ block 的點已用完整 degree 四，連通性迫 D=K₅ 且沒有原 z 接點；
更大 clique 直接違反 degree 四。因此 blocks 只剩 bridges 與 odd cycles。

此段沿用的是 connected-exterior 的原邊抽取法；三個附件端及 L₂
已在本型重新核對，沒有直接複製 C₂ 的單框點葉數計費。

## 4. 原葉 odd cycle 必為純接點型或純雙框點型

leaf bridge 的 private endpoint 在 D 內 degree 一，違反 (6)。
leaf odd cycle 的每個 private vertex 在 D 內 degree 二。
由 (3)、(6)，恰有下列兩型：

| 原點身份 | (p,s₁,s₂) | L₂ | L₃ |
| --- | --- | --- | --- |
| T：原 z 接點、碰 b₁ | (1,1,0) | {0,3} | {0,2} |
| N：非接點、同碰 b₁,b₂ | (0,1,1) | {2,3} | {2,3} |

在同一 leaf block 中，所有 private vertices 的 L₂ 均等於該 block
的二色 palette。兩型的 L₂ 不同，故整葉 private vertices 必純 T
或純 N。這是同一原 block 的 palette 等式，並非跨點 marginal 比較。
L₃ 核對保存在固定證書；推論只需 L₂。

**純 N 葉不能以接點數排除；它的禁止理由是下面原邊 K₅ minor。**

## 5. 純 N 葉的任意大小原邊 K₅ minor

設 K 為純 N 的 leaf odd cycle，c 為唯一 cut vertex。
沿原環選兩個相鄰 private vertices a,b。至少有兩個 private vertices，
故 triangle 葉也能如此選。a、b 均非原接點，且都有原 b₁、b₂ 附件。

D−{a,b} 仍連通：刪除環上的相鄰兩點後，餘環是一條含 c 的路
（triangle 時只有 c），其他原 blocks 仍經 c 相連。
全部三個原 z 接點位於 N 葉的 private set 之外，所以仍在 D−{a,b}。
因此下列原頂點集合連通：

\[
X=(V(D)\setminus\{a,b\})\cup\{z,x_2,b_0,b_4,b_3\}.
\tag{7}
\]

連通見證是 D−{a,b} 的原路、任一原 zuᵢ、原 z–x₂–b₄，
及原框路 b₀–b₄–b₃。X 不含 a、b、b₁、b₂。
五個 disjoint branch sets 為

\[
\{a\},\quad\{b\},\quad\{b_1\},\quad\{b_2\},\quad X.
\tag{8}
\]

十對鄰接逐份由原邊給出：ab；ab₁、ab₂、bb₁、bb₂；
a、b 各自另一條原環邊抵達 X（triangle 時可共用 c）；
b₁b₂；b₀b₁；b₃b₂。
故 (8) 是 K₅ minor，與 disk planarity 矛盾。
本證明適用任意奇環長、任意其他 blocks／bridges 與任意 unary 大小。
只是從原 M 選取 minor witness，未更換接點、刪除 P₃ 或重定義 relation。

## 6. 補上葉數限制，單 block 也矛盾

多於一個 block 的有限 block-cut tree 至少有兩個 leaf blocks；
cut-vertex nodes 的 degree 至少二，不能算成沒有 private vertices 的葉。
§§3–5 已排除 clique 大 block、bridge 葉及純 N 葉。
每個剩下的 leaf odd cycle 純 T，至少含兩個互異原 z 接點。
兩葉的 private vertices 互不相交，故至少需四個原接點，與 |P_D|=3 矛盾。

因此原 D 只剩一個 block，必為 odd cycle。每點內度二且 list uniform；
D 有原接點，遂全部點都為 T。三接點身份迫

\[
V(D)=\{u_0,u_1,u_2\},\quad
E(D)=\{u_0u_1,u_1u_2,u_2u_0\},\quad
N_B(u_i)=\{b_1\}.
\tag{9}
\]

(9) 的自身支援只為 {b₁}，已與 geometry 34 指定的 {b₁,b₂} 矛盾。
亦可用 C₂ 的原路 z–x₂–b₄–b₃–b₂–b₁ 補上
u₀,u₁,u₂,z,b₁ 之間的第十條 K₅ subdivision 路。
這是條件推導的原 triangle，不是把原雙框點 unary 偷換成單框點 gadget。

## 7. 新非接點葉與 bridge 確實通過局部限制

固定控制建立一族雙框點局部模型：N 奇環
c–a₀–⋯–aₙ₋₂–c，所有 private aᵢ 都接 b₁、b₂，c 接 b₂；
原 bridge cd 接到 triangle d,u₁,u₂，接點恰為 (u₀,u₁,u₂)=(d,u₁,u₂)。
d 只接 z；u₁,u₂ 各接 z、b₁。
每個 D 頂點完整 degree 均為四，自身支援恰 {b₁,b₂}。

同一 q 下，private path 的偶數個點只能交替取 2、3，其兩端異色，
所以原 c 強制取 1。bridge 迫 d≠1，原接點 triangle 的完整關係恰為
六個 permutations(0,2,3)，禁色為 {0,2,3}。
因此原接點 u₀ 的內度三與原非接點 aᵢ 的內度二可同時成立；
N 葉與 T 葉並存只耗三個接點，C₂ 的原葉數論證不能直接沿用。

三個原拒絕 pins 下，N 側 bridge 端 c 與 T 側 bridge 端 d 都被迫取 1。
證書在同一份局部模型上刪 bridge，逐一測試全部 16 個有序 (c,d)
端點 pins；完整端點 relation 恰為 {(1,1)}，每份保存整份局部 coloring lift。
四個模型、三個 pins 共 12 份關係；未以獨立端點 marginals 拼接，
也沒有把這些局部 pins 說成整份 P₃／w 可延拓。

固定重播域為 n=3,5,7,9：

| N 環長 | D 頂點數 | unary 相關邊 | 完整三接點 tuples | 刪邊局部四色 witnesses |
| ---: | ---: | ---: | ---: | ---: |
| 3 | 6 | 17 | 6 | 68 |
| 5 | 8 | 23 | 6 | 92 |
| 7 | 10 | 29 | 6 | 116 |
| 9 | 12 | 35 | 6 | 140 |

證書逐份保存固定奇環模型的完整 contact tuples、內點 lifts、原附件、
完整 degree、各 pin 的接受／拒絕、逐邊刪除解除與實際染色見證。
保留全部原 B、P₃、zw／wx₂ 後，同一模型由 (8) 得原 K₅ minor。
這些是非平面的局部正控制，未宣稱整份 M 的逐邊 minimality：
在 z=0、w=1 的原 context partial witnesses 中，D_w 的避色 fibre
由原禁色 {0,2} 保證非空，但其內點不在此枚舉。
證書中的原 triangle reduct 另保存六份 tuples、九條刪邊／36 份局部
染色及原外路 subdivisions，明標其支援不符合 geometry 34。

## 8. 重播、證據界線與停止點

```bash
python3 scripts/c5_mixed_p3_two_frame_ternary_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_mixed_p3_two_frame_ternary_unary.py --check
python3 scripts/c5_mixed_p3_one_color_ternary_unary.py --check
python3 scripts/c5_mixed_p3_common_endpoint.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際數字、通過情況及未重跑範圍見[歷史紀錄](history/2026-10-04-mixed-p3-two-frame-ternary-unary.md)。
Checker 不重證外部 Gallai 定理或任意大小的原圖抽取；既有 Lean build
不把本輪紙面拓撲論證變成 Lean theorem。固定 q 來源排除不是完整 Σ
或 target 延拓，亦未證一般／共同出口或 `K∞=K≤5`。

本輪只將 **CPP-134-1／geometry 34／side_join_id 20** 記為完成；
前層 36 cases／140 geometries／900 joins 保持原 artifact，零表格刪除。
z 側引理未用 w 的具體 tuples，但其他 w 角色、geometry 35 或 root
交換型的逐份覆蓋未在本輪另立證書，不改寫成整份 case 完成。

下一個具名入口為 **CPP-134-1／geometry 34／side_join_id 60**：
同一 P₃、E_z={1}、E_w={1,3}、A_z={b₁,b₂}、A_w={b₂,b₄}；
z 側改為兩份原 unary，接點數 (2,1)、禁色 ({0,3},{2})，仍無 spoke；
w 側沿用原三接點、禁色 {0,2}，side IDs=(27,1)。須保留兩份 unary 的自身支援、
有序接點、完整關係及原外路，不能把整側支援任意分派給它們。
本輪未分析這份不同分拆。目前入口以
[weak-deletion 導覽](c5_weak_deletion_guide.md#3-精確停止點與下一個窄問題)為準。
