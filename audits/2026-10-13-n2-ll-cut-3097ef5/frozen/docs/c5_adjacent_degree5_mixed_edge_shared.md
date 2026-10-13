---
docgraph:
  id: c5.adjacent-degree5-mixed-edge-shared
  family:
    - c5
    - c5.degree5
  derives_from:
    - c5.adjacent-degree5-interfaces
  requires:
    - c5.adjacent-degree5-shared-singleton
    - c5.single-spoke-three-one
    - c5.single-spoke-two-two
  related:
    - c5.adjacent-degree5-mixed-edge-order
---
# 相鄰雙 degree-5：唯一 mixed K2 的共鄰端點型

後續（2026-09-29）：[t_w=0、(1,1,1) 六跨度排除](c5_adjacent_degree5_mixed_edge_shared_t0_singles.md)
已逐筆排除原 108 筆：四份 unary、v 的總跨度至少 6>5，不需 T4，0 target 查詢。
zu、zv、wu 共鄰端點接線的全部五型已完成，出口第八類移除 w 分拆限制。
原資料保持；下列通知與正文保留各輪語境，現行入口見 [HANDOFF](HANDOFF.md)。

後續（2026-09-29）：[t_w=0、(2,1)](c5_adjacent_degree5_mixed_edge_shared_t0_pair_single.md) 已完成無 root-spoke 的支援／環序與原 diamond
路徑 K5：原 54 筆接合為 102 筆必要支援，204 查詢全接受；另排除 94、
保留 8，不需 T4。出口第八類已擴充；此接線只剩 t_w=0、(1,1,1) 的
108 筆。原資料保持；下列後續通知與正文保留各輪語境。

後續（2026-09-29）：[t_w=1、(1,1)](c5_adjacent_degree5_mixed_edge_shared_t1_singles.md)
已由飽和環序及完整禁色上界完成：原 72 筆綁定 32 筆必要支援，64 查詢
全接受、不需 T4。共鄰端點型的 t_w≥1 全部接回出口；只剩 t_w=0 的
(2,1)／(1,1,1)。原 306／288 筆及 9,312 schemas 保持，下列為各輪語境。

後續（2026-09-28）：[w 側 t_w=1、(2)](c5_adjacent_degree5_mixed_edge_shared_t1_pair.md)
已由局部化的相鄰支援對／原 diamond 路徑 K5 及完整禁色集合上界完成。
原 36 筆綁定 356 筆必要支援，排除 292、保留 64 的 128 查詢全接受，
不需 T4 或新 first-bridge 引理；出口第八類已擴充。其餘三種 w 分拆保留，
原 306／288 筆與 9,312 schemas 保持，下列通知與正文保留各輪語境。

後續（2026-09-28）：[w 側兩條 spoke](c5_adjacent_degree5_mixed_edge_shared_t2.md)
已完成 t_w=2、(1) 的原 18 筆：280 份幾何接合成 38 筆必要支援，全部
76 個指定查詢接受，不需 T4，已加入條件式出口第八類。其餘四種 w 分拆
仍保留；原 306／288 筆與 9,312 schemas 不改寫，下文保留本輪語境。

2026-09-28。接續 [各一接點型來源排除](c5_adjacent_degree5_mixed_edge_order.md)，
改取唯一 mixed 原分量 uv、P*ᶻ={u,v}、P*ʷ={u}。本輪完成任意大小的
完整關係及逐邊 minimality 化約：**z 沒有 boundary spoke，且恰有一個
二接點 unary 分量；w 的 residual 恰為 singleton，各 unary 禁色容量飽和。**
平面來源再排除 w 側 (3)，留下五種 w 接點分拆。

306 筆抽象 minimality 資料中，原路徑 K5 排除 18 筆，保留 288 筆；
展開 z 側完整二元關係後有 9,312 份必要 schemas。它們尚未與全部
unary actual supports／環序接合，**不是 disk 實現或指定雙列分離**。
代數為初等紙面證明；(3) 排除另沿用外部 degree-list 定理及原圖 minor。
Python 是有限控制，未新增 Lean theorem。研究優先序見 [HANDOFF](HANDOFF.md)。

## 1. 原接線與完整 ordered tuples

G 有限簡單，B=(b0,…,b4) 誘導 C5，q=01012，U={0,1,2,3}。
有效內部 H 連通；有序相鄰 roots z、w 完整 degree=5，其餘內點完整
degree=4。G 拒絕 q，刪每條非外圈邊後接受 q。H−{z,w} 的唯一 mixed
原分量 C* 恰是原 K2={u,v}，root incidences **恰為 zu、zv、wu**。
其餘原分量各只接一個 root，大小不限；全部接點與實際附件保留。

degree 立即給 N_B(u)={b_i}，N_B(v)={b_j,b_k}，j≠k。
允許 i=j 或 i=k，不將相同 q 色誤當同一 boundary 頂點；u、v 不交換。
對任意 proper boundary row β，設

\[
X=U\setminus\{\beta_i\},\qquad Y=U\setminus\{\beta_j,\beta_k\},\qquad
\mathcal T_*(\beta)=\{(s,t)\in X\times Y:s\ne t\}.
\]

同一個 u 只有一個變數 s，兩 root 必共同使用同一份 tuple：

\[
R_*(\beta)=\{(a,b):\exists(s,t)\in\mathcal T_*(\beta),\quad
s\ne a,\ s\ne b,\ t\ne a\}. \tag{1}
\]

令 F*=U²∖R*。此處 |X|=3、|Y|≥2；扣除 root 色後，兩端 lists
X∖{a,b}、Y∖{a} 都非空。原邊 uv 不能著色恰在兩者同為 singleton。
因此精確公式為

\[
F_*(\beta)=
\begin{cases}
Y\times\{e\},& |Y|=2,\ Y\subset X,\ \{e\}=X\setminus Y,\\
\varnothing,&\text{其他情形}.
\end{cases} \tag{2}
\]

證明：若兩 residual 都為 {c}，則 a≠b、X={a,b,c}、Y={a,c}；
反之這些等式確使 uv 兩端被迫同色 c。因此唯一拒絕欄 b=e 有兩格，
且皆非對角。對所有 β 都有 Δ⊆R*。

尤其 β_j=β_k 或 β_i 不屬於 {β_j,β_k} 時 F*=∅。
這不同於各一接點型的一個禁對，也不同於共鄰 singleton 的兩個對稱禁對。
例 X={1,2,3}、Y={2,3} 時，(a,b)=(2,1) 拒絕；端點 marginals
的乘積會用不存在的 (s,t)=(3,3) 誤接受。將 u 拆成分別避 a、b 的
兩份 coloring 亦會誤接受，故完整 tuple 與共鄰身份都不可省略。

## 2. 同一來源的接合與 q 正常形

沿用 [unary 精確消去](c5_adjacent_degree5_shared_singleton.md#1-同一來源及精確消去單-root-分量)：
對只接 r 的原 C，由其完整 tuples 定義 F_Cʳ(β)，且 |F_Cʳ|≤k_C=|P_Cʳ|。
令 A_r(β)=U∖β(N_B(r))、E_r(β)=A_r(β)∖⋃F_Cʳ(β)，則

\[
Z_G(\beta)=(E_z(\beta)\times E_w(\beta))\setminus(\Delta\cup F_*(\beta)),
\qquad |E_z(\beta)|\ge2,\quad |E_w(\beta)|\ge1. \tag{3}
\]

最後兩個界由 mixed 佔用 z 的兩條、w 的一條 incidence 得出，每列都成立。
不同 unary 分量是在固定同一 (a,b) 後才接合，未將單一分量拆成 marginals。

以下省略 q 下標。minimality 要求 C* 有私有非對角色對，故 F*≠∅。
所以 q_j≠q_k 且 h:=q_i 屬於 {q_j,q_k}。定義其餘兩個 q 色

\[
\{q_j,q_k\}=\{h,e\},\qquad \{h,e,d\}=\{0,1,2\},\qquad T=\{d,3\}.
\]

此時 X={e,d,3}、Y=T、F*=T×{e}。完整 \(\mathcal T_*(q)\) 恰為
(e,d)、(e,3)、(d,3)、(3,d) 四個有序 tuples。

**q 下的 residual 定理。** 必有

\[
E_w=\{e\},\qquad E_z=\{e\}\cup D,\quad\varnothing\ne D\subseteq T. \tag{4}
\]

證明：對任一 b∈E_w，|E_z|≥2 保證至少一個 a≠b。q 拒絕使 (a,b)
必在 F*，故 b=e；進而 E_z⊆X。刪 zw 的染色要求兩 E 有共同色，
因此 e∈E_z；容量界給 D 非空。刪 C* 邊的私有對正是 D×{e}。

## 3. z 無 spoke、唯一二接點；w 容量飽和

下述等價式的前提為 §1 的實際來源 degree／incidence 規格，且 q 下
每個內點的 boundary 鄰色互異；後者由 edge-minimality 必然得出。
對每側原 unary 分量 C，寫
J_C=F_C∖⋃_{C'≠C}F_C'，聯集只取同側其他原分量。

**z 側。** 另一 root 固定為 e。新增 z 色 a 能接受，恰在 a=h：
a=e 違反 zw，a∈T 被 mixed 擋住。因此每個 z-spoke 的原色只能為 h，
每個 z-unary 分量都須有 h∈A_z∩J_C。spokes 在 q 下互異，先得 t_z≤1；
不同分量的私有色互斥，至多一個 z-unary 分量。

其 incidence 總數是 2−t_z≥1，故至少有一個分量。如果 t_z=1，
唯一 spoke 用 h，使 h∉A_z，與 unary 刪邊見證矛盾。所以

\[
t_z=0,\qquad C_z=\{C_0\},\quad |P_{C_0}^z|=2,\qquad
F_{C_0}(q)\in\bigl\{\{h\},\{h,d\},\{h,3\}\bigr\}. \tag{5}
\]

最後一式由 E_z=U∖F_{C_0}、(4) 及容量二得出。三種情形的 D 分別為
T、{3}、{d}；不是把兩接點視為兩個 unary 分量。

**w 側。** E_w={e}，故 root-spokes 不能用 e，而只能用 h、d；t_w≤2。
刪任一 spoke，其 root 必取釋放的新色 c，所有原 w-unary 必接受 c，
因此每個 F_C⊆A_w。設 k_C=|P_C^w|，則

\[
\bigcup_{C\in C_w}F_C=A_w\setminus\{e\},\qquad
|A_w\setminus\{e\}|=3-t_w=\sum_C k_C.
\]

由 |F_C|≤k_C，所有不等式都須等號：**每個 |F_C|=k_C，各 F_C 互不
相交，恰分割 A_w∖{e}。** 每個分量的私有色即其全部 F_C。

**完整逐邊充要定理。** 在本節實際來源前提下，minimal q-core 恰等價於：
§2 的 h、e、d 支援條件、(5)，以及上述 w 側飽和分割。
必要性已證；充分性由下表及 degree-4 原分量解除引理得到。

| 刪除原邊 | 固定同一來源的精確 root 見證集合 |
| --- | --- |
| zw | {(e,e)} |
| uv、zu、zv、wu、u 的一條或 v 的兩條 boundary 邊 | D×{e}；解除整個原 C* |
| 唯一 z-unary C₀ 的任一內部／root／boundary 邊 | {(h,e)}；其他原分量仍保留 |
| w-unary C 的任一內部／root／boundary 邊 | {(a,b): a∈E_z, b∈F_C, a≠b} |
| w-spoke，原色 c∈{h,d} | {(a,c): a∈E_z, a≠c} |

表中集合全部非空，因 D≠∅、F_C≠∅、|E_z|≥2；原圖由 (2)–(4)
拒絕 q。每次只解除被碰到的**原分量**；刪 bridge 後也不拆成新來源。
任一刪邊 coloring 的被刪兩端必同色，否則可加回該邊。
特別是刪 zu 時 u=a 但原 wu 仍要求 u≠b；刪 wu 時 u=b 而 zu、zv
仍保留。這三條 root incidence 不能一起解除或把共鄰點複製。

## 4. 完整 unary 關係與平面來源的五種 w 分拆

固定 C₀ 的兩個具名接點 (x₀,x₁)。若 F_{C₀}={h,c}，其完整 q 關係
必恰為 {(h,c),(c,h)}：每個 tuple 都含這兩色；刪各自的 root incidence
給各座標的解除見證，所以兩個次序都必存在。
若 F_{C₀}={h}，每個 tuple 都含 h，且每個座標都要有恰在該座標出現 h
的非對角見證；全部 tuples 色集交集恰為 {h}。因此沿用
[二接點完整 schema](c5_single_spoke_two_two.md#2-完整-ordered-relation-的必要-schema)，
恰有 95 個必要 schema（包含允許 (h,h) 的情形）。這仍非 95 份來源實現。

w 側 k=1 時，原接點完整 unary tuple 恆為唯一禁色；k=2 時，由飽和
與同一解除理由，完整關係恰為禁色對的兩個次序。未先投影再拼湊接點。

現在額外假設 G 平面。若 w 側分拆為 (3)，t_w=0 且 F_C=U∖{e}，
至少有兩個禁色。原 B∪{w,u} 經原 wu、ub_i 連通並避開 C，因此
[連通外框 K4 引理](c5_degree5_tree_components.md#1-連通外框排除-degree-4-分量的-k4)
適用。[Dvořák Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
給不可著色 degree lists 的 Gallai／block palettes；此輪已核對原文。
由 [三接點 active triangle 證明](c5_single_spoke_three_one.md#2-三個葉點迫使唯一-triangle-加三臂)，
兩個禁色迫使 triangle、三條同 parity 原 bridge arms 及三條 boundary tethers。

取五個 branch sets 為 {w}、三條完整 arms（含 triangle 端點及原接點）、
以及 B∪{u} 加三條 tethers 的內點。triangle 邊、原 root contacts 與
tethers 給九條鄰接，**原 wu** 給 {w} 與外部 branch set 的第十條。
各組連通且互不相交，故為原圖 K5 minor。(3) 不存在，不限臂長或來源大小，
不需 T4。這是沿用外部定理的紙面排除，不由有限 skeleton 外推。

| t_w | w-unary 分拆 | 飽和禁色分配 | 六種 (h,e,d)、三種 z 禁色合計 |
| --- | --- | --- | ---: |
| 2 | (1) | spokes 用 h,d；F₁={3} | 18 |
| 1 | (2) | spoke 用 c∈{h,d}；F₂=U∖{e,c} | 36 |
| 1 | (1,1) | U∖{e,c} 分成兩個具名 singleton | 72 |
| 0 | (2,1) | U∖{e} 分成具名 pair 與 singleton | 54 |
| 0 | (1,1,1) | U∖{e} 的三個具名 singleton | 108 |

合計 288 筆；排除的 (3) 有 18 筆。具名同接點數分量保留其身份。
每種 z 禁色各 96 筆，展開完整 q 關係得 96×(95+1+1)=9,312 份必要
schemas；w 各分量的完整 tuples 已由飽和固定。此數未乘 boundary 支援，
也未給各列獨立挑選 schemas 的權利。

## 5. 同一來源的任意列拒絕判準

對任意 β，重算同一來源的 X、Y、E_z、E_w；仍有 |E_z|≥2、|E_w|≥1。
若 F*=∅，一定接受，因可取不同 root 色。若 F*=Y×{e}，則

\[
\beta\notin\Sigma(G)\quad\Longleftrightarrow\quad
E_w(\beta)=\{e\}\ \text{且}\ E_z(\beta)\subseteq X. \tag{6}
\]

證明：每個 w 色 b 都與某個 z 色形成非對角；若拒絕，就只能 b=e，
且所有 z 色都在 Y∪{e}=X。反向立即由 (2)–(3) 得出。
在非 q 列不要求 e∈E_z，也不要求刪 zw 後可著色；不能直接搬用 (4)。
尤其 v 的兩 boundary 附件重色時，這次確有延拓：關鍵是 |E_z|≥2。
若沒有重色，仍須取得原 unary 分量的同圖跨列完整關係，不能由 q 表
獨立指定 p₁、p₂ 的 E 集合。

## 6. 有限控制、重播與停止點

[checker](../scripts/c5_adjacent_degree5_mixed_edge_shared.py)、
[JSON](../artifacts/c5_adjacent_degree5_mixed_edge_shared/observations.json) 與
[必要表](../artifacts/c5_adjacent_degree5_mixed_edge_shared/necessary_table.md)
保存 source／直接輸入 SHA256，將下列層次分開。

- z 側 41、w 側 209 個容量候選，九種 h／d 共 77,121 組；逐類刪邊
  直接判準與正常形完全一致。306 筆中按原路徑 K5 排除 18，留 288。
- u 的五個單點支援乘 v 的十個 pair，全部 240 proper rows 共 12,000
  份關係核對；canonical rows 另有 8,000 個獨立 pinned queries、
  56,000 個七類刪邊 queries、3,640 次刪邊端點強迫及 12,000 次共同色框搬運。
- q 下有 28 組具名 K2 支援，逐份保存 h/e/d 與反射 ID；這只是局部
  支援，不是 288 筆的 disk completion。任意列公式另核對 6,600 組。
- 三張真正 degree=(5,5,4,…) minimal q-core，分別實現三種 z 禁色；
  保存原圖、720 列完整接合、canonical tuples 及 71 份逐邊 coloring。
  沒有 disk／T4 正控制宣稱。
- 84 份原 w–u–B 的 K5 skeleton，包括零臂、長臂、細分 tethers；
  刪 wu 後每份指定 branch-set witness 都失效。skeleton 不是完整
  degree/list 來源，亦不宣稱刪 wu 後整圖平面。
- 負控制保存 marginals 誤接合、複製共鄰 u 的誤接受，以及刪 zu
  卻一併忘掉 wu 會放入的非法 coloring。

```bash
python3 scripts/c5_adjacent_degree5_mixed_edge_shared.py --check
python3 scripts/c5_adjacent_degree5_shared_singleton.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_single_spoke_three_one.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證及未重跑範圍見 [本輪紀錄](history/2026-09-28-adjacent-mixed-edge-shared.md)。
本輪停止於任意大小必要化約與完整逐邊等價式。下一窄型為 **w 側
t_w=2、(1)** 的 18 筆：先由原 z–w–u–v–z 四環及原 chord zu 證
unary actual supports／環序，再接合 28 組局部 K2 支援，使用 (6)
處理同圖指定雙列。各一接點型的四環周長排除不能直接搬過來。
本型 disk 來源排除／雙列分離、其他 mixed、一般雙 root、degree≥6、
一般單側／共同出口與 K∞=K≤5 仍未證；未新增 Lean theorem。
