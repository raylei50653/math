---
docgraph:
  id: c5.adjacent-degree5-mixed-edge
  family:
    - c5
    - c5.degree5
  derives_from:
    - c5.adjacent-degree5-interfaces
  requires:
    - c5.adjacent-degree5-shared-singleton
    - c5.single-spoke-three-one
  related:
    - c5.single-sided-exit
---
# 相鄰雙 degree-5：唯一 mixed 原 K2、各一接點的必要化約

後續（2026-09-28）：[原四環外側次序](c5_adjacent_degree5_mixed_edge_order.md)
已完成此接線型的 disk 來源排除，不需 T4：576 筆中 552 筆超過 C5
周長，餘 24 筆的飽和次序與 q 支援矛盾。原定一色側 t=2、(1) 亦已
涵蓋。下文與原 artifact 保留必要化約輪的數字及停止點；未 Lean 化。

2026-09-28。接續 [共鄰 singleton 全支援完成](c5_adjacent_degree5_singleton_end_arc.md)
後的新分支。**唯一 mixed 原分量為 uv，且只有 zu、wv 兩條 root incidence
時，minimal q-core 強迫 mixed 關係只禁一個有序非對角色對，兩 root 的
residual 分別為一色與兩色。** 平面來源的一色側剩五種接點分拆，兩色側
只剩 (2) 或 (2,1)；在 disk 來源中，原四環 z–u–v–w–z 的內側為空。

816 筆抽象 minimality 資料經原路徑 K5 排除含三接點分量的 240 筆，
留下 576 筆。另將 u、v 的實際 boundary 支援記為 40 組有序 pair，
disk 交錯 crosscuts 排除 4 組。**576 筆與 36 組是不同層的必要資料**，
尚未加入全部 unary actual supports／環序，不是來源圖或完整支援 cover。
本輪未證 K2 子類的指定雙列分離，沒有新增條件式出口類別。

證據為任意大小紙面化約、沿用的外部 degree-list 定理及 Python 有限控制；
未新增 Lean theorem。研究優先序見 [HANDOFF](HANDOFF.md)。

## 1. 原來源、完整 tuple 與任意列的 K2 關係

G 有限簡單，B=(b0,…,b4) 誘導 C5，H 是非空連通的有效內部。
固定 q=01012、U={0,1,2,3}；G 拒絕 q，刪任一非外圈邊後接受 q。
相鄰有序 roots z、w 的完整 degree=5，其餘內點完整 degree=4。
H−{z,w} 的唯一 mixed 原分量 C*={u,v} 有原邊 uv，且
P*ᶻ={u}、P*ʷ={v}，u≠v。故各有恰兩個不同 boundary 鄰點，記
Sᵤ=N_B(u)、Sᵥ=N_B(v)。其餘原分量各只接一個 root。
每份原分量、接點身份、全部附件及共同色框始終保留。

對任意 proper boundary row β，寫

\[
X_\beta=U\setminus\beta(S_u),\qquad Y_\beta=U\setminus\beta(S_v),\qquad
\mathcal T_*(\beta)=\{(s,t)\in X_\beta\times Y_\beta:s\ne t\}.
\]

完整 root 關係為

\[
R_*(\beta)=\{(a,b):\exists(s,t)\in\mathcal T_*(\beta),\ s\ne a,\ t\ne b\}.
\tag{1}
\]

兩 lists 大小均至少二，扣掉 root 色後均非空。uv 無法著色恰在兩個
residual lists 是同一 singleton。因此 F*=U²∖R* 精確為

\[
F_*(\beta)=
\begin{cases}
\{(a,b):\exists c,\ X_\beta=\{a,c\},\ Y_\beta=\{b,c\},\ a\ne c,\ b\ne c\},
  &|X_\beta|=|Y_\beta|=2,\\
\varnothing,&\text{其他情形}.
\end{cases}\tag{2}
\]

若 X=Y={a,c}，禁的是 (a,a)、(c,c) 兩個對角；若 X∩Y={c}，只禁
唯一 (a,b)，且 a≠b；若 X、Y 不交，則全開。不能套用 singleton 的
「同一兩色 list 禁兩個非對角」公式，也不能將 T* 換成端點 marginals
的乘積。例 X={0,3}、Y={1,3} 時，原 uv 排除 (3,3) tuple，故 root
色對 (0,1) 被拒絕；邊際乘積卻會用假的 (3,3) tuple 接受它。

## 2. q 下的一個禁對與不對稱 residual

沿用 [單 root 精確消去](c5_adjacent_degree5_shared_singleton.md#1-同一來源及精確消去單-root-分量)，
F_Cʳ(β) 從同一 unary C 的完整有序 tuples 定義，容量 ≤k_C=|P_Cʳ|。
令 E_r(β)=A_r(β)∖⋃F_Cʳ(β)，則每列 E_r 非空，且

\[
Z_G(\beta)=(E_z(\beta)\times E_w(\beta))\setminus(\Delta\cup F_*(\beta)).\tag{3}
\]

q 下 u、v 各自的 boundary 鄰色互異，否則原 C* 有 slack，與其邊
critical 矛盾。因此 X_q={d,3}、Y_q={e,3}，d,e∈{0,1,2}。
若 d=e，(2) 只禁對角；刪 C* 的邊後仍須 z≠w，故不可能釋放 q。
所以 **d≠e，F*(q)={(d,e)}**。

刪 C* 的任一邊會使整個原 C* 關係全開，故 E_z×E_w 必含 (d,e)。
原圖拒絕 q 又迫使乘積的其他格只能在 Δ；於是兩 E 均包含於 {d,e}，
且不能同時等於 {d,e}，否則 (e,d) 已延拓。刪 zw 要求非空對角，
排除 E_z={d}、E_w={e}。剩下恰為

\[
(E_z,E_w)=(\{d\},\{d,e\})\quad\text{或}\quad(\{d,e\},\{e\}).\tag{4}
\]

稱 residual 一色的 root 為 rₛ，另一個為 rₗ；這是來源資料中的角色，
不交換原 z、w 或 u、v 身份。後文 s／l 只用來排列必要型。

## 3. 逐類刪邊的充要條件與接點正常形

對各 unary 原分量 C 定義
J_C=F_C∖⋃_{D≠C}F_D，同側的 D 才參與聯集。除了 (4)，minimality
恰要求

\[
F_C\subseteq A_r\quad\text{且}\quad J_C\ne\varnothing
\qquad\text{對每個 unary }C.\tag{5}
\]

這是對同一實際來源的充要式，前提包含本頁 degrees／incidences 與
q-spokes 顏色互異；不是抽象資料的實現定理。逐類理由如下。

| 刪邊類別 | 同一色框中的精確見證或條件 |
| --- | --- |
| zw | (4) 的唯一共同色 c 給 (c,c)；此對由 C* 接受 |
| uv、zu、wv、四條 C*–B 邊 | C* 全開，唯一可用非對角為 (d,e) |
| unary C 的任一內部／root／boundary 邊 | 原 C 全開；釋放 A_r∩J_C 中的色，與另一 root 的原 E 接合 |
| root-spoke，原 q 色 h | root 必取新增 h，故同側每個 unary C 必接受 h，即所有 F_C 避開 h |

最後一列給 F_C⊆A_r。此後刪 unary 邊的條件正是 J_C≠∅：一色側
任何新色都可與兩色側選到合法對；兩色側的新色在 {d,e} 外，可與
一色側的原色接合。root-spoke 的新色也在原 residual 外，理由相同。
各原分量的全開沿用 degree-4 slack 引理，不把 bridge 刪後的兩側當
成兩個可獨立挑選的舊來源。刪後 coloring 的兩個被刪端點必同色。

設 t_r 是 root-spokes 數，n_r 是 unary incidence 總數，則
|A_r|=4−t_r、n_r=3−t_r（zw 與 C* 各佔一條原邊）。

**一色側飽和。** 若 E_s={c}，則
|⋃F_C|=3−t_s=n_s=Σk_C。容量 |F_C|≤k_C 迫使每個 F_C 恰有 k_C 色，
各 F_C 互不相交，且分割 A_s∖{c}。spokes 不能用 c，也不能用 q 未用的
3，所以 t_s≤2。一色側可有全部單接點分量，不能沿用 singleton 的
「每側必有多接點」結論。

**兩色側差一。** E_l={d,e}，spokes 只可能用第三個 q 色 f，故 t_l≤1。
|⋃F_C|=2−t_l=n_l−1；非空私有色互斥，使分量數至多 2−t_l。
t_l=1 時只有 (2)，禁色恰 {3}。t_l=0 時只有 (3) 或 (2,1)；前者禁
{f,3}，後者兩個 F 分別為 {f}、{3}（兩種分配），不允許互相重疊。

## 4. 原 K2 路徑排除三接點，無大小上界

現在加入來源 planarity，不需 T4。對任一 unary C，外部集合
B∪{r,p_r} 連通並避開 C，其中 p_z=u、p_w=v；原 r–p_r–b_i
（b_i∈S_{p_r}）提供實際 r–B 路徑。
非空 F_C 給不可著色 degree assignment；外部
[Dvořák Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
給 Gallai tree 與 block palettes，本輪核對原文。連通外框 K4 引理因
上述 hub 適用，故 C 為 K4-free。

若接點分拆含 (3)，§3 給該 C 至少兩個禁色。
[三接點 active triangle 論證](c5_single_spoke_three_one.md#2-三個葉點迫使唯一-triangle-加三臂)
只用兩份拒絕 palettes、完整 degree=4、三個原接點及 K4-free，遂給
一個 triangle、三條同 parity 的原 bridge arms 與三條原 boundary tethers。
此處不假定唯一 degree-5，也不把四環當成三角形。

令 V₀,V₁,V₂ 含各完整 arm 及 triangle 端點，取 Z={r}，
O=B∪{p_r}∪所有 tethers 去掉 triangle 起點。五組連通、不交；triangle
邊給 V_i–V_j，原 contacts 給 Z–V_i，tethers 給 V_i–O，**原 rp_r
給 Z–O**。得到 K5 minor，與 planarity 矛盾。另一 root 與另一 mixed
端點不必放入 branch sets，且沒有新增或改寫任何接線。

因此任意大小平面來源的必要型恰收窄為下表；表格不主張每型可實現。

| 角色 | t | unary 接點分拆 | q 禁色必要式 |
| --- | ---: | --- | --- |
| 一色側 E={c} | 2 | (1) | F₁={3}；spokes 為另外兩個 q 色 |
| 一色側 | 1 | (2) | F₂=A∖{c}，恰兩色 |
| 一色側 | 1 | (1,1) | 兩 singleton F 分割 A∖{c} |
| 一色側 | 0 | (2,1) | |F₂|=2、|F₁|=1，不交且聯集 U∖{c} |
| 一色側 | 0 | (1,1,1) | 三 singleton F 分割 U∖{c} |
| 兩色側 E={d,e} | 1 | (2) | spoke 色 f；F₂={3} |
| 兩色側 | 0 | (2,1) | F₂、F₁ 是 {f}、{3} 的兩種分配 |

## 5. 實際支援與原四環的第一層 disk 限制

本節另假設 B 是 disk 外框，全部位置與內外側均讀取同一原嵌入。
由 q(Sᵤ)={0,1,2}∖{d}、q(Sᵥ)={0,1,2}∖{e} 且 d≠e，u、v 的
兩個**實際具名** boundary pair 恰有 40 組。若兩 pair 不交且在 B 上
交錯，原 b_i–u–b_j 與 b_k–v–b_l 是兩條內部不交的 disk crosscuts，
Jordan 分離矛盾。排除的有序支援為

\[
(03,14),\ (03,24),\ (14,03),\ (24,03).
\]

剩 36 組只通過這個必要條件；尚未把 unary 支援、root-spokes、原
四環外側 rotation 同時接合。不能把 36 組乘 576 筆稱為來源分類。
反射 ρ(i)=3−i mod 5、π=(0 1) 同步搬運兩 pair 及缺色 d,e；checker
保存 40 組的反射雙射，沒有單獨重命名一個分量的顏色。

**四環內側為空。** 每個 unary C 都有 boundary 附件：若沒有，完整
關係對 S₄ 不變，F_C 也對 S₄ 不變；但 0<|F_C|≤k_C≤3，不可能。
原 z–u–v–w–z 是 simple cycle；每個 unary C 只在一個 root 接觸該
cycle，又有不經 roots 的 C–B 路徑，故不能位於其有界內側。u、v 的
boundary spokes 亦在外側，且該四環沒有額外 chord。因此內側無其他
有效頂點。這為下一輪的外側環序提供來源根據，尚不直接套用 singleton
三角形長弧的單位順序公式。

對任一 unary actual support S_C，F_C(q) 必在逐色固定 q(S_C) 的
置換下不變。特別是 F_C={3} 時，q(S_C) 必含全部三個 q 色，否則把
缺少的 q 色與 3 交換即矛盾。下一窄型 t_s=2、(1) 因而已有明確
支援前提：它的單接點分量須接 b4，且各接 {b0,b2}、{b1,b3} 至少一點。

## 6. 任意列判準、有限控制與停止點

對任意 β，令 E_z、E_w 使用該列在**同一來源**的完整 unary 關係。
若 F*(β) 沒有非對角，(3) 拒絕 iff E_z=E_w={c}。若 F*(β) 的唯一
非對角為 (a,b)，拒絕 iff

\[
E_z=E_w=\{c\}\text{ for some }c,
\quad\text{或}\quad E_z=\{a\},\ E_w\subseteq\{a,b\},
\quad\text{或}\quad E_w=\{b\},\ E_z\subseteq\{a,b\}.\tag{6}
\]

所有 E 非空；證明就是 (3) 的非對角乘積只能含 (a,b)。q 下的私有色
與正常形不自動搬到其他列；β 的 boundary 重色使 K2 全開時，仍須
排除兩 root 相同 singleton 的障礙。

[checker](../scripts/c5_adjacent_degree5_mixed_edge.py)、
[JSON](../artifacts/c5_adjacent_degree5_mixed_edge/observations.json) 與
[必要型／原 K2 支援表](../artifacts/c5_adjacent_degree5_mixed_edge/necessary_table.md)
保存以下分層證據及 source／直接輸入 SHA256。

- 每側 209 個容量候選，九種有序缺色（含 d=e）共 393,129 組，獨立
  逐類刪邊與 (4)–(5) 全相符；816 筆 minimality 資料經 (3) 型排除留
  576 筆。具名同接點數分量仍分開計數。
- 100 組原 K2 支援乘全部 240 proper rows，核對 24,000 份完整關係；
  canonical rows 另有 16,000 個獨立 pinned queries、112,000 個七類
  實際刪邊 queries、6,020 次端點同色核對與 24,000 次共同色框搬運。
- 40 組 q 支援、4 組交錯排除；(6) 核對 22,500 組 list／residual。
  另保留 marginal 乘積誤接合與同 lists 只禁對角的負控制。
- 一張真正 degree=(5,5,4,…,4) minimal q-core，完整保存原圖、240 列
  接合及 27 份逐邊 coloring。canonical 接受列只有 01021、01201、01231，
  所以不接受全部 T4；它只核對 minimality，沒有 disk 正控制宣稱。
- 480 份原 r–u–B／r–v–B 的 K5 skeleton，含零臂／長臂與細分 tethers；
  刪 rp_r 後每個指定 witness 均失效。skeleton 不是完整 degree/list
  來源，也不宣稱刪該邊後整圖平面。

```bash
python3 scripts/c5_adjacent_degree5_mixed_edge.py --check
python3 scripts/c5_adjacent_degree5_shared_singleton.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_single_spoke_three_one.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證及未重跑範圍見 [本輪紀錄](history/2026-09-28-adjacent-mixed-edge.md)。
停止點是上述任意大小必要化約；下一窄題取一色側 t_s=2、(1)，兩色側
為 (2) 或 (2,1)，接合全部 actual supports 與原四環外側次序，再使用
同圖跨列判準。K2 子類全部 p₁／p₂ 分離、無 mixed、其他較大／多 mixed、
一般雙 root、degree≥6、一般單側／共同出口與 K∞=K≤5 仍未證。
