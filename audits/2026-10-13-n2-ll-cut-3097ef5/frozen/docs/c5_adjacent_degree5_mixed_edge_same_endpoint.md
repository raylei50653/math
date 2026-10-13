---
docgraph:
  id: c5.adjacent-degree5-mixed-edge-same-endpoint
  family:
    - c5
    - c5.degree5
  derives_from:
    - c5.adjacent-degree5-interfaces
  requires:
    - c5.adjacent-degree5-shared-singleton
    - c5.adjacent-degree5-mixed-edge-order
  related:
    - c5.adjacent-degree5-mixed-edge-shared-t0-singles
    - c5.single-sided-exit
---
# 唯一 mixed K2 同端點型：完整關係與原 v-star 來源排除

後續（2026-09-29）：[四 incidence 原 K4](c5_adjacent_degree5_mixed_edge_k4.md)
已以完整分量改色與實際外部路徑排除 P*ᶻ=P*ʷ={u,v} 的一般平面來源，
不需 T4 或 degree-list 定理；唯一 mixed K2 的全部接線遂已處理。
下文保留本輪數字與停止點，現行優先序見 [HANDOFF](HANDOFF.md)。

2026-09-29，接手 main@c178cf1 及前三輪未提交成果。
**P*ᶻ=P*ʷ={u} 的 induced-C5 disk minimal q-core 不存在。**
先重推原 uv 的完整 tuples 與逐邊 minimality，得到 240 筆必要正常形；
原外部路徑 K5 排除 105 筆含三接點分量者，餘 135 筆中 123 筆超出
框周長，12 筆由五邊飽和及原 v 的三條 boundary 邊排除。

不需 T4、不限制 unary 分量大小，**target 查詢為零**。證據為任意大小
紙面論證、外部 degree-list 定理與 Python 有限控制；未新增 Lean theorem。
必要正常形與支援 placements 不是來源圖枚舉。其他 K2 接線及一般單側／
共同出口、K∞=K≤5 保留；研究優先序見 [HANDOFF](HANDOFF.md)。

## 1. 同一來源與完整 uv 關係

G 有限簡單，B=(b0,…,b4) 是 induced disk 外框，有效內部 H 非空連通。
固定 q=01012、U={0,1,2,3}；G 拒絕 q，刪任一非框邊後接受 q。
有序相鄰 roots z、w 的完整 degree=5，其餘內點完整 degree=4。
H−{z,w} 的唯一 mixed 原分量是 C*={u,v}，root incidences **恰為 zu、wu**。
因此 N_B(u)={b_i}，N_B(v)={b_j,b_k,b_l}，三個框點互異。
其他原分量各只接一個 root。保留全部原分量、具名接點、實際 boundary
附件、bridges、root rotation、原 uv 與共同色框，未複製共鄰 u。

對任意 proper row β，令 X=U∖{β_i}、Y=U∖β({j,k,l})。完整局部關係為

\[
\widehat{\mathcal T}_*(\beta)=\{(s,t)\in X\times Y:s\ne t\},\qquad
S_\beta=\{s\in X:Y\setminus\{s\}\ne\varnothing\}.
\tag{1}
\]

供兩 root 使用的接點 tuple 只有同一個座標 u，其關係為 {(s):s∈S_β}；
式 (1) 另保留非接點 v 的值。必有 |S_β|≥2：若 |Y|≥2 則 S_β=X；
若 Y={c} 則 S_β=X∖{c}。故完整 16 格 root 禁對恰為

\[
F_*(\beta)=
\begin{cases}(S_\beta\times S_\beta)\setminus\Delta,&|S_\beta|=2,\\
\varnothing,&|S_\beta|=3.
\end{cases}\tag{2}
\]

q-minimality 使同一內點的 boundary 鄰色互異，所以 q({j,k,l})={0,1,2}。
令 h=q_i、T={0,1,2}∖{h}={a,b}，則

\[
\widehat{\mathcal T}_*(q)=\{(a,3),(b,3)\},\quad
S_q=T,\quad F_*(q)=\{(a,b),(b,a)\}.\tag{3}
\]

這不是前型 zu、zv、wu 的兩格直積禁對，也沒有原 diamond。

## 2. 五種 residual 與完整逐邊 minimality

沿用 [完整有序介面](c5_adjacent_degree5_interfaces.md)：每份原 unary C
的完整 ordered relation 非空；其禁色 F_C 是所有 tuples 色集的交集，
|F_C|≤k_C，其中 k_C 是它與唯一 root 的實際 incidence 數。
定義 E_r=A_r∖⋃_{C∈C_r}F_C。每 root 的 mixed incidence 為一，故
**每一列皆有 |E_z|,|E_w|≥1**。全圖 root 關係為

\[
Z_G(\beta)=(E_z(\beta)\times E_w(\beta))\setminus(\Delta\cup F_*(\beta)).\tag{4}
\]

q 拒絕、刪 zw 的對角見證及刪 C* 邊的私有非對角色對，精確給

\[
\varnothing\ne E_z,E_w\subseteq T,\qquad E_z=T\text{ 或 }E_w=T.\tag{5}
\]

確實，mixed 的私有對必是 (a,b) 或 (b,a)；任何 T 外 residual 色都
立即接受。兩個不同 singleton 不容刪 zw，兩個相同 singleton 不容
刪 mixed 邊。故只剩 (T,T)、({a},T)、({b},T)、(T,{a})、(T,{b})。

對每側令 J_C=F_C∖⋃_{D≠C}F_D，同一來源逐邊條件為

\[
T\subseteq A_r,\qquad F_C\subseteq A_r,\qquad J_C\setminus T\ne\varnothing.
\tag{6}
\]

刪 spoke 只釋放其原色，若在 T 中仍被 zw 或 (3) 擋住。因此 spoke
只能用 T 外且不被任一 unary 禁止的顏色。刪 unary 邊只解除該原分量，
新增可接受色正是 J_C∖T。反向由 degree-4 原分量解除引理，(5)–(6)
加上 q-boundary 鄰色互異，亦足以保證每條非框邊的刪後延拓。

| 刪除的原邊 | 同一來源的精確 root 見證集合 |
| --- | --- |
| zw | {(c,c):c∈E_z∩E_w} |
| uv、zu、wu、ub_i、v 的三條 boundary 邊 | (E_z×E_w)∖Δ |
| z-unary C 的任一內／root／boundary 邊 | (J_C∖T)×E_w |
| w-unary C 的任一內／root／boundary 邊 | E_z×(J_C∖T) |
| z-spoke／w-spoke | {h}×E_w／E_z×{h} |

表中 mixed 七條邊逐條解除原 C*，沒有刪 uv 後重定義兩份來源分量。
刪 zu 仍保留 wu；每份刪後染色的被刪邊兩端同色，否則可加回該邊。

因 T⊂{0,1,2}、U∖T={h,3}，每側至多一條 spoke，且若有必用 h。
各 unary 必佔一個不同的 T 外私有色，總 incidence 是 3−t_r，故
每側的必要正常形如下；令 D_r=T∖E_r，大小為零或一。

| t_r | unary 分拆 | 完整禁色投影 |
| --- | --- | --- |
| 1 | (2) | F₂={3}∪D_r；唯一 spoke 色 h |
| 0 | (3) | F₃={h,3}∪D_r |
| 0 | (2,1) | F₁={c}、F₂=({h,3}∖{c})∪D_r，c∈{h,3} |

每個 E_r 有四個形式。三種 h、五種有序 residual 組合給
3×5×4²=**240** 筆。這些是保留原分量身份的必要關係資料。

若二接點 F₂ 禁兩色，完整關係恰有兩個相反次序；若 F₂={c}，完整
tuples 色集交集為 {c}，且刪各 root incidence 都給 c 恰在該座標的
解除見證。因此有 [既有 95 個必要 schemas](c5_single_spoke_two_two.md#2-完整-ordered-relation-的必要-schema)。
checker 保存四種 singleton 色的全部 schemas，未用接點 marginals 代替。

對任意 β，(1)–(4) 另給拒絕判準

\[
\beta\notin\Sigma(G)\iff
[E_z=E_w=\{c\}\text{ for some }c]
\ \lor\ [|S_\beta|=2,\ E_z,E_w\subseteq S_\beta].\tag{7}
\]

若 v 的附件重色使 mixed 全開，仍須排除同色 singleton 障礙。非 q 列
不能獨立指定各 E 或沿用 q-minimality。本輪來源排除不需查詢 target。

## 3. 原 r–u–B 路徑、K5 與支援下界

對任一 unary C，原 r–u–b_i 路徑避開 C，將 B∪{r,u} 接成連通外部 hub。
固定被 C 拒絕的 root 色，其 lists 是不可著色 degree assignment。
[Dvořák Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
給 tightness 與 Gallai／block palettes。本輪重讀原文第 5–6 頁。
沿用 [局部連通外框 K4 引理](c5_degree5_tree_components.md#1-連通外框排除-degree-4-分量的-k4)：
K4 block 四點的第四方向給互不相交原外向分枝，連到上述 hub 即成 K5。
故 C 是 K4-free Gallai tree；這裡只用 C 內 degree=4，不假設全圖唯一 degree-5。

若 k_C=3，表中 F_C 至少兩色。[三接點 active triangle 引理](c5_single_spoke_three_one.md#2-三個葉點迫使唯一-triangle-加三臂)
迫使原 triangle、三條同 parity bridge arms 與三條原 boundary tethers。
五個 branch sets 為 {r}、三條完整 arms，以及 B∪{u} 加各 tether 內點；
原 ru 提供 root–hub 的第十條鄰接，故為來源 K5，不需 T4。
240 筆中有 105 筆含此分量，全部排除，**餘 135 筆**。

每側因而只有 (2) 或 (2,1)，其中各恰一份二接點分量；兩側合計的
完整 q-schema 計數為 253,935（只計必要關係，不計支援或 disk 實現）。

令 S_C=N_B(C)。每份 unary 的 q(S_C) 至少兩色：空支援的全色對稱
不容非空容量≤2 禁色；若只見色 c，其穩定子迫使 F_C={c}。固定 r=c
後全部外鄰同色，tightness 使每點至多一個外鄰，故 deg_C≥3；
K4-free Gallai tree 的葉塊私有點內度≤2，矛盾（singleton 亦矛盾）。
若 F_C={3}，其支援更須見全部 q 色：漏掉 d∈{0,1,2} 時，交換 d、3
會固定全部原附件色而改變 F_C。這是整份 relation 的必要不變性。

## 4. 原三角形外側與 123 筆跨度矛盾

原 Q=z–w–u–z 為三角形。每份 unary 都碰 B，v 亦有實際 boundary 邊，
故所有外側分枝都在 Q 面向 B 的一側。取 Q 及閉內部的細正則鄰域，
外側為 annulus。每個原 unary C 為一個單位；每條 root-spoke 為零跨度
單位；**uv、v 的三條 boundary 邊與 ub_i 合成一個 u 單位 M**。
M 的 actual support 是 S_M={i,j,k,l}，其中允許 i 與 v 的附件重合。
M 的兩條 u-incidences 在原三角形外側，沿 u 的小鄰域接起其截短端，
只是讀取原連通樹的鄰域，沒有把 uv 收縮成新的著色問題。

同一 unary 的二接點不能夾住其他單位：其原內路徑與兩條 contacts
成 Jordan 曲線，不含 B 的一側若有被夾單位，就不能再接 B；若該側
包含 Q 的方向，M 也不能接 B。故各接點形成連續區塊。
各單位的連通細鄰域互不相交；外端 crosscut 的不含內圓周側不能
容納另一單位的外端。與 [原四環 annulus 論證](c5_adjacent_degree5_mixed_edge_order.md#2-原四環外側的同序區塊與周長界)
相同的 Jordan 步驟，現由**原三角形**給 z、w、u 的區塊次序。

因此 actual supports 可同序提升，前單位最大值≤後單位最小值，
最後最大值≤起點+5。允許支援有間隙、不同單位共享端點，不能重用
開框邊。每份 unary 跨度至少一，禁 {3} 者至少二；M 包含 v 的三個
不同框點，跨度至少二。故

\[
2+\sum_{C\text{ unary}}\bigl(1+\mathbf1_{F_C=\{3\}}\bigr)\le5.\tag{8}
\]

至少一側 E_r=T；該側必有一份原 unary 恰禁 {3}。若任一側為 (2,1)，
共有至少三份 unary，左端至少 2+3+1=6。若兩側均為 (2) 且 E_z=E_w=T，
左端也是 2+2+2=6。135 筆中 **123 筆由此排除**。

剩下恰 12 筆：兩側各一條 h-spoke、各一個二接點分量，恰一側 residual
為 T。以 L 表示該兩色側、S 表示另一側，原 root 身份仍保留。必有

\[
F_L=\{3\},\quad F_S=\{3,c\}\ (c\in T),\qquad
\ell_L=2,\quad\ell_S=1,\quad\ell_M=2.\tag{9}
\]

三個單位恰填滿五條框邊，無間隙。L 支援連續三點且見三色；S 支援
一條框邊兩端；M 的支援恰等於 v 的三個連續附件。u 的附件必在其中。
兩條原 root-spokes 各只能落在自己 unary 區塊的端點，且都用 h。

## 5. 原 v-star 排除最後 12 筆

**扇區引理。** H−v 連通：原三角形 zwu 與所有 unary 分量仍相連。
三條 v-boundary 邊把 disk 分成三個扇區，因此 H−v 全在同一個扇區內，
它的 boundary 附件只能在該扇區的閉框弧上。這保留同一 v、原 uv、
ub_i 及全部 unary 接線，不能把 u 與 v 的 boundary 支援各自挑選。

在 (9) 下，M 三個連續框點的補弧長三，L、S 的支援聯集正是這條
補弧的四個框點；它們不可能同在另外兩個只有一條框邊的扇區。
故此補弧就是 H−v 所在扇區，**u 的附件只能是 M 的兩個端點**。

L 的三色支援只可能 234、340、401。每份配合兩種整體方向，共六行；
保留次序而不把 401 改成互不相關的三點集合：

| S_L | S_S | S_M=S_v | 同一來源矛盾 |
| --- | --- | --- | --- |
| 234 | 40 | 012 | v 的附件只見 0、1，違反 q-minimality |
| 234 | 12 | 401 | L／S spoke 端點共同可用 q 色只有 h=0；u 被迫接 b0，但它是 M 中點，位於錯誤扇區 |
| 340 | 01 | 123 | v 的附件只見 0、1 |
| 340 | 23 | 012 | v 的附件只見 0、1 |
| 401 | 12 | 234 | L／S spoke 端點共同可用 q 色只有 h=1；u 被迫接 b3，但它是 M 中點，位於錯誤扇區 |
| 401 | 34 | 123 | v 的附件只見 0、1 |

兩條非重色行的矛盾甚至不需額外使用 F_S 的支援穩定子。兩種 L/S
root 身份、每份二接點的兩個原次序都涵蓋。故 **12 筆亦全部來源排除**。

## 6. 有限證書、出口接合與停止點

[Checker](../scripts/c5_adjacent_degree5_mixed_edge_same_endpoint.py)、
[JSON](../artifacts/c5_adjacent_degree5_mixed_edge_same_endpoint/observations.json) 與
[逐筆排除表](../artifacts/c5_adjacent_degree5_mixed_edge_same_endpoint/exclusion_table.md)
分開保存以下層次：

- 每側 209 個容量候選，131,043 次直接逐類 minimality 與正常形比對；
  240 筆中 105 筆原路徑 K5、123 筆跨度、12 筆飽和扇區排除。
- 50 組 u／v 實際局部支援、12,000 份 proper-row 關係、8,000 次獨立
  pinned queries、56,000 次七類刪邊 queries、3,290 次刪邊端點強迫，
  12,000 次完整 uv-tuples 共同色框搬運。q 局部相容支援為 20 組。
- 遞增三段弧與獨立框邊 masks 得同一 10 份飽和幾何；12×10=120 次
  正常形接合，保留 1,440 組 u 附件／兩 spoke 端點候選及全部 pair
  contact orders。省略 v 扇區時恰留下 4 份假候選，加入後全矛盾。
- 五張真正 degree=(5,5,4,…) minimal q-core 實現五種 residual；保存
  原圖、1,200 列完整接合與 150 份逐邊 coloring。**沒有 disk／T4 宣稱**。
- 80 份長短 arms／tethers 的原 ru K5 skeleton；刪 ru 後每份指定
  branch-set witness 失效。它們不是完整 degree/list 來源實現。
- 任意列 (7) 的 12,600 個關係控制；另保存複製 u 的誤接受及刪 zu
  卻忘掉 wu 的非法 coloring。這些不是必要來源表的 target 查詢。

本型不存在，接入 [失敗核心限制](c5_single_sided_exit.md#5-為何尚不是無條件的一般定理)，
不新增空的出口類型，也不把排除計為 p₁／p₂ 接受。既有第八類維持
zu、zv、wu 接線的範圍。一般出口與完整 Σ 的來源雙缺失前提未變。

```bash
python3 scripts/c5_adjacent_degree5_mixed_edge_same_endpoint.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t0_singles.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_order.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared.py --check
python3 scripts/c5_adjacent_degree5_shared_singleton.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_single_spoke_three_one.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證及省略範圍見 [當輪紀錄](history/2026-09-29-adjacent-mixed-edge-same-endpoint.md)。
沒有獨立第二審稿者；`lake build` 不形式化本輪 Gallai／Jordan 證明。
下一窄入口為唯一 mixed K2 的 **P*ᶻ=P*ʷ={u,v}**，root incidences
zu、zv、wu、wv 全在，u、v 各有一個 boundary 附件。先核對原 K4
與實際外部路徑，不能把本型 v 的三附件或三角形次序搬過去。
無 mixed、較大／多 mixed、非相鄰雙 root、degree≥6 保留。
