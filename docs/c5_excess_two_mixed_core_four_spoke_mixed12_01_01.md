# A₃：mixed-(1,2)+a-unary 的原共用 pair 01／01 來源排除

**獨立驗收（2026-10-04，D₅）**：[最終成果固定快照與稽核](../audits/2026-10-04-task-d5/REPORT.md)
核對原04／04及root交換、四rotations、actual C/U支援、完整三hub前提，
整份C替換逐點保持全部外部，只主張(a,b,u)投影等式；六角色joint不等
反例與01202 singleton1／3保持。逐身份ledger為16／20、40／58支援、
50／84schedules；原A至A₃正文／artifacts及各輪數字保持當輪語境。
未用D₅來源搬運，其他mixed12身份／ε≥3未證；現行入口由Kempe導覽維護。

**後續（2026-10-04，A₄）**：[原 04／04 具名入口](c5_excess_two_mixed_core_four_spoke_mixed12_04_04.md)
重新核對四 rotations、原 actual supports／完整 schedules 與三-hub
前提後另作來源排除，含 root 交換；其餘框架為 16／20。
本報告的 18／22 ledger 與原 artifact 保留當輪截點。

**獨立驗收（2026-10-04，D₄）**：[正式返回工作區稽核](../audits/2026-10-04-task-d4/REPORT.md)
核實原01／01及交換、四rotations／三hub、完整C替換與18／22ledger。
360份(a,b,u)投影相等；六角色joint不等反例保留。36份指定列固定控制
只有U singleton2；singleton3由原schedules與任意大小紙面論證涵蓋，
不稱為另36份singleton3實現控制。

2026-10-04，接續 [A₂ 停止點](c5_excess_two_mixed_core_four_spoke_mixed12_01_12.md#6-重播與停止點)
及 [Kempe 導覽 §3](c5_kempe_guide.md)。只固定原 spokes=01／01，
包含整對 root 身份交換；四份原 disk rotations、原 C 完整 ternary、
原 U actual supports／singleton relations 及完整六角色 joint 均保留。
實際驗證與貼用摘要見 [A₃ 研究紀錄](history/2026-10-04-excess-two-four-spoke-mixed12-01-01.md)。
本輪未 commit／push。

**在 A 的原來源前提下，01／01 的整份原來源排除，含 root 交換。**
本 incidence 自己的原兩條 0–1 crosscuts 與 ab 迫 C 位於 0ab 或
1ab；完整 degree 握手式再迫 C 實際只碰該框點。完整來源支援使
U 實際碰齊 234，所以 U 只能在 a 的固定長 face。逐點核對原 C
exact lists、連通外部 K₄ 排除及不限接點數的三-hub 引理，得到每份
合法 C 外 coloring 的完整 C extension。固定原 ax 因而非 Σ-critical；
共同拒絕列 01202 的兩種 singleton 亦各有完整 joint 矛盾。

A₂ 的 20／24 具名殘留降為 **18／22**；本具名入口殘留 **0／0**。
這是條件式任意大小紙面排除與固定 Python 控制，沒有直接套用
mixed11 的 sealed triangle 結論或其原 mixed 省略定理。
**mixed-(1,2) 整型、其他共用 pairs、来源實現、ε≥3、一般出口及
K∞=K≤5 未證，未新增 Lean theorem。**

## 1. 原來源、完整 ternary 與六角色 joint

完整來源前提沿用 [A §1–3](c5_excess_two_mixed_core_four_spoke_mixed12.md#1-原來源完整-ternary-與六角色-joint)：
G 有限簡單，B=(b₀,…,b₄) 是指定有序 induced-C₅ disk 外框，完整
Σ=933／941，每條非框邊 Σ-critical。有效 H 連通、ε=2，恰有相鄰
完整 degree-5 roots a,b，原 ab 存在，其餘有效內點完整 degree 四。
H−{a,b} 恰為原 mixed C 與 a 側原 unary U，接線分別為
ax、by₀、by₁ 及 au。y₀≠y₁；x 可以與其中一個原頂點相同，
u∈U 與整份 C 互異。兩側原 spokes 都恰為 01。

原分量的全部內邊、actual attachments／supports、bridges、旁支、
ownership、環序及同一字面四色框不變。令原完整有序 relations 為
R_C(β;x,y₀,y₁)、R_U(β;u)，則

\[
J_G(β)=\{(A,D,X,Y_0,Y_1,T):
(X,Y_0,Y_1)\in R_C(β),\ T\in R_U(β),\
A,D\in U_4\setminus\{β_0,β_1\},\
A\ne D,X,T,\ D\ne Y_0,Y_1\}. \tag{1}
\]

每份 tuple 有原 C、U 的整份 coloring witnesses。固定同一 β 與
字面 (A,D) 後保留全部纖維，包括空纖維。若 x=y_j，兩個座標
必同色，兩條 owner guards 作用於同一原頂點；不能複製接點或
將 ternary marginals 相乘。Root 交換搬運整圖、U 的 owner、
contacts、tuple 欄位、actual 附件及 rotations，boundary 與色框固定。

A 已證原 a-spoke 省略與 N=G−U 各自全收。完整五角色 T_N 與
原 R_U 接合後，任何原拒絕列必滿足

\[
P_N(β)=R_U(β)=\{d_β\},\qquad
d_β\in U_4\setminus\{β_0,β_1\}. \tag{2}
\]

這是所有原 N witnesses 及整份原 U relation 的必要身份，不是
逐列任選 endpoint 禁色。以下指定列論證沿用式 (2)；ax 非 critical
的全列論證只使用同一原 C 外合法 coloring。

## 2. 四份原 rotations、C 的實際支援與 U 的固定位置

只取同一原骨架的兩條 0–1 paths，0–a–1 與 0–b–1。
它們只在原 endpoints 相交，將 disk 分成兩個 root 外側區域與
中間區域。原 ab 必在中間區域，將它切成原三角 0ab 與 1ab。
原 C 非空連通、避開骨架，且 ax、by₀、by₁ 同時存在，所以 C
及三條接線的內部在同一原 face；其 closure 必含兩 roots。
因此固定原 h∈{0,1}，

\[
C\subseteq\operatorname{int}(hab),\qquad
N_B(C)\subseteq\{h\}. \tag{3}
\]

這是本 incidence 的原嵌入論證，沒有借用 mixed11 的已完成結論。
不能將兩份 face 的包絡相加，也不能每列重新選 h。

每個具名七頂點骨架有 144 份 rotation assignments，恰四份
disk rotations。沿用 artifact 的原 index，其 faces 如下；face
用無向 cyclic key 顯示，完整有向 vertex rings 仍逐份保存。

| 原 rotation indices | 長 face | 另一個 root 外側短 face | 共同 C faces |
| --- | --- | --- | --- |
| 0、3 | 0–4–3–2–1–5–0 | 0–1–6–0 | 0–5–6–0、1–5–6–1 |
| 1、2 | 0–4–3–2–1–6–0 | 0–1–5–0 | 0–5–6–0、1–5–6–1 |

這張表逐份核對兩個 masks 與兩種原 root roles，沒有把四份
rotations 合成一個匿名 embedding。原 root 交換的 index 搬運為
`[0,1,2,3] → [1,0,3,2]`；反射方向也保留，沒有另選 canonical
rotation 取代搬運後的原環序。

原 C 完整 degree 握手式是

\[
4|V(C)|=2|E(C)|+3+|E(C,B)|. \tag{4}
\]

三條原 root incidences 正是 ax、by₀、by₁，即使 x=y_j 仍是
三條不同原邊。式 (4) 迫 boundary attachment 邊數為奇數，故
不能為零；結合式 (3)，原 actual support **正是 {h}**。
Checker 先保存空／singleton 支援子集，再明列此奇偶排除。

沿用 [完整來源支援引理](c5_independent_support_capacity.md#11-degree-與完整支援)，
原來源碰齊五框點。兩 roots 只接 01，C 只碰 h，故

\[
\boxed{\{2,3,4\}\subseteq S_U=N_B(U).} \tag{5}
\]

U 連通，au 存在，所以 U 也位於一個固定 a-incident face。
0ab／1ab 或原 a–0–1 短 face 的包絡都不能包含 234；原 U
只能位於 **0–4–3–2–1–a–0**。當 a=5 時，允許原 rotations
0、3；當 a=6 時，允許 1、2。每份 U placement 的 C faces
只從同一 rotation 取得，不能跨 embeddings 自由拼接。

繼承的 singleton schedules 逐份保存；下表的 d 指同一原 U 在
所有原拒絕列的 singleton 色。933 的拒絕 rows 是 1、3、4、6，
941 是 1、4、6；每個 support 與 schedule 均另保留 root 交換。

| 原 actual U support | 933 繼承 schedules | 941 繼承 schedules | 式 (5) |
| --- | --- | --- | --- |
| 023 | d=2 | d=2 | 缺 4 |
| 134 | 無 | d=2 | 缺 2 |
| 234 | 無 | d=2 | 保留 |
| 0123 | d=2 或 d=3 | d=2 或 d=3 | 缺 4 |
| 0134 | 無 | d=2 或 d=3 | 缺 2 |
| 0234 | d=2 | d=2 | 保留 |
| 1234 | 無 | d=2 | 保留 |
| 01234 | d=2 或 d=3 | d=2 或 d=3 | 保留 |

含 root 交換，繼承 selected supports／schedules 是 **8／16** 及
**12／22**；來源幾何仍相容者是 **4／8** 及 **6／10**。
這些不是來源實現：下一節的完整 C extension 排除全部。

## 3. mixed12 自己的完整 C extension

固定任一 proper β 及原 C 外逐點合法 coloring。原兩側 spokes
同為 01，原 ab 使 A≠D，因此 A、D、β_h 三色互異，原
a,b,h 是三個兩兩相鄰的字面 singleton hubs。

原 C 的 exact lists 為

\[
L(v)=U_4\setminus\bigl(β(N_B(v))
\cup(\{A\}\text{ if }v=x\text{ else }\varnothing)
\cup(\{D\}\text{ if }v\in\{y_0,y_1\}\text{ else }\varnothing)\bigr).
\tag{6}
\]

每點完整 degree 四，外鄰只在 a,b,h；故 |L(v)|≥deg_C(v)。
三個 hub 色互異，沒有因同色外鄰合併而丟掉 degree。by₀、by₁
接不同原 C 點，但均是同一原 b hub；不是兩份獨立禁色。
若 x=y_j，式 (6) 同時去掉 A,D，所有原 incidences 仍在。

反設 C 不可著色。Connected degree-assignment 的 slack 引理迫
處處 tight，degree-list 刻畫使 C 是 Gallai tree，且 lists
blockwise uniform。外部依賴已直接核對
[Dvořák，Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)。
這裡拒絕的是固定原 C lists，不要求整份 G 是 minimal q-core。

先展开 [連通外部 K₄ 排除](c5_degree5_tree_components.md#1-連通外框排除-degree-4-分量的-k4)
在此 lists 的適用。若 C 有 K₄ block Q，每個 clique 點已有三個
內部鄰居，完整 degree 四使它恰有一個原外方向：直接接到
X={a,b,h}，或經 C 中一條 bridge 離開 Q。不同 clique 點的
bridge 外側互不相交，否則 Q 不會是原 block。

對一條這樣的 bridge，刪除它後兩側 endpoint 各有 list slack，
兩側都是 connected degree assignments，所以各自可著色，兩個
endpoint domains 非空。若可選不同色便能接回 C，與拒絕矛盾；
所以兩個 domains 必為同一 singleton。外側若完全不碰 X，
便無任何固定外鄰色；整份 coloring 可置換四色，endpoint domain
不可能只有一色。因此 Q 每點的一個原外方向都能抵達 X。

四條原 paths 的內部互不相交。X 本身是原連通三角形，將 X
與四條 paths 去掉 clique endpoints 後的部分合成一個外部
branch set，加四個原 clique singletons，得到 K₅ minor。
這與原 G planar 矛盾，故 C 的拒絕 Gallai tree 是 K₄-free。
更大的 clique 亦由 planarity 排除；剩餘 blocks 是 bridges 或
odd cycles。

現在完整符合 [不限接點數的三-hub Gallai 引理](c5_short_support_singleton.md#4-三-hub-引理排除未見色接點數不設上限)：
C 非空連通、K₄-free Gallai，每點完整 degree 四，三個外部
hubs 兩兩相鄰且固定不同色。其末端 odd-cycle／bridge 紙面
分支給原 K₅ minor，所以 C 必可著色。此適用直接核對 ax、
by₀、by₁；沒有把 binary 結論升為 ternary，沒有把 C 收縮成
有限 skeleton，也沒有使用 mixed11 的 Σ(G−C)=Ω。

故對每份合法原 C 外 coloring，都有一份完整原 C witness，
其原有序 ternary tuple 滿足

\[
\boxed{(X,Y_0,Y_1)\in R_C(β),\quad
X\ne A,\quad Y_0\ne D,\quad Y_1\ne D.} \tag{7}
\]

共享接點仍逐點同色，C 外的原 coloring 可全部保持。

## 4. 原 ax 非 critical 與指定拒絕列的完整 joint

固定任一 G−ax 的完整 coloring。忘掉它的整份 C witness，保留
B、a、b 及原 U 全部頂點的字面顏色。所有 C 外原邊仍合法；
式 (7) 給一份原 C coloring，接回 ax、by₀、by₁，C 外逐點不動。
反方向是原 G coloring 的限制。因此精確結論是

\[
\boxed{\pi_{a,b,u}J_G(β)=\pi_{a,b,u}J_{G-ax}(β)
\quad\text{對每個 proper }β.} \tag{8}
\]

式 (8) 保留的是完整 C 外 witness；完整六角色 tuples 可能改變，
**不主張 J_G=J_(G−ax)**。投影是否非空恰判定該列是否接受，
所以 Σ(G)=Σ(G−ax)，固定原非框邊 ax 不 critical，與來源前提
矛盾。Root 交換保持同一 owner incidence 與這條原 a–x 邊。

另逐份保存指定拒絕列出口。q=01202（row index 4）被兩 masks
拒絕，式 (2) 給完整 R_U(q)={d}，d∈{2,3}；取其一份整份
原 U witness，固定

\[
(A,D,T)=(5-d,d,d)=
\begin{cases}(3,2,2),&d=2,\\(2,3,3),&d=3.\end{cases} \tag{9}
\]

兩側 spokes 的 guards、原 ab 與 au 均合法。C 在 0ab 時原
三-hub 色是 A,D,0；在 1ab 時是 A,D,1，兩種皆互異。
式 (7) 提供同一完整 ternary witness，與式 (9) 及固定 U witness
在同一字面 q 接合，得到

\[
\boxed{(5-d,d,X,Y_0,Y_1,d)\in J_G(01202).} \tag{10}
\]

式 (10) 覆蓋所有繼承 schedules，包括必要 singleton 為 3 的
身份，不把它誤改成 A₂ 的 singleton 2。原拒絕列獲得完整 extension，
也給來源不存在的矛盾。本入口最後殘留 0／0。

## 5. 固定證書、完整殘留與證據界線

[A₃ checker](../scripts/c5_excess_two_mixed_core_four_spoke_mixed12_01_01.py)、
[完整 joint helper](../scripts/c5_excess_two_four_spoke_mixed12_01_01_joint_controls.py)、
[artifact](../artifacts/c5_excess_two_mixed_core_four_spoke_mixed12_01_01/observations.json)
唯讀繼承 A₂ artifact，逐份重建選定四個原 01／01 框架，核對完整
四份 rotations、U placements、actual supports、singleton schedules、
原 omission identities 及 root 交換。原 A／A₂ 證書不覆寫。
未選定的完整具名框架與 relations 逐項原樣保存。

| 同一 mixed12 必要域，含 root 交換 | 933 | 941 |
| --- | ---: | ---: |
| A₂ 原具名殘留 | 20 | 24 |
| A₃ 新排 01／01 | 2 | 2 |
| **保存其餘具名框架** | **18** | **22** |
| 保存其餘 actual U face／support records | 44 | 70 |
| 保存其餘完整 singleton schedules | 56 | 102 |
| 本具名入口原來源殘留 | 0 | 0 |

新 helper 有 **36 張手建完整 degree 圖**及 18 份 root 交換：
C actual support 0／1、x 獨立／共享 y₀／共享 y₁，三份 exact
U supports 023／234／0234。三種 contact 身份各有 12 張圖。
每份保留所有原內邊、actual 附件與路徑、十列完整 R_C／R_U、
原圖與省略圖的六／五角色 joints、整份 witnesses 及全部 16
字面 root-pair fibres，包括空纖維。

獨立全圖回溯核對 **2,880 joins／46,080 fibres**，其中 38,112
空 fibres；保存 51,248 份六角色及 2,400 份五角色 tuple witnesses。
核對 360 份 ax 投影等式，明列 **5,712 次只替換整份 C、C 外
逐點固定的 witnesses**；720 份合法 C root-pair fibres 均保存
完整 extension。原四條 spokes 接回、G−au 的完整乘積與
singleton guard 身份亦逐份核對。36 張圖在 q=01202 的完整
R_U={2}，同一 (a,b,u)=(3,2,2) 的完整 C extension 各自保存。
字面 d=3 的指定列紙面 instances 則由 selected schedules 全部保留。

兩份負控制分開保存：ternary marginals 的假接合不能代替完整
relation；六角色 joint 在 ax 省略後也可不同。後者在 control 6、
row 01012 的 omission-only tuple 是 **(2,3,2,2,0,1)**，因 X=A
違反原 ax；artifact 保存它的整份 G−ax coloring，及保持同一
C 外 coloring 的原 G 替換 witness。這個例子符合式 (8)，
不符合完整六角色相等。

36 張控制圖的獨立完整 Σ 均為 **1023**。它們只是有限 relation／
witness 控制，不宣稱 disk、Σ-critical 或 933／941 來源實現。
任意大小拓撲、Gallai 與 K₄／K₅ 推導由上述紙面證明承擔；
有限 controls 不提供無界覆蓋、一般出口或新的 Lean theorem。

## 6. 重播與停止點

```bash
python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed12_01_01.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed12_01_01.py --check
python3 scripts/c5_excess_two_four_spoke_mixed12_01_01_joint_controls.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
python3 tools/artifacts.py status
git diff --check
```

主 checker 無參數只生成新的 A₃ artifact；`--check` 唯讀逐 byte
比對。Helper 的 `--check` 重算固定 controls，不寫原 artifacts。
以上是重播入口，實際本輪結果由 A₃ 研究紀錄記載；原 minimality、
完整支援及無界紙面引理沿用，沒有全面重跑其歷史證書。
`lake build` 不形式化本輪的 disk／Gallai／minor 論證。

**停止於原 01／01 與 root 交換整份排除，其餘 18／22 完整具名
框架保留。** 其他共用 pairs 與 unequal 入口仍按原支持、完整
ternary／singleton relations、同一 rotation 及六角色 joint 保存；
不由本輪推廣為其他具名來源排除，也沒有重開來源圖枚舉。
後續窄入口與目前停止點由 [Kempe 導覽](c5_kempe_guide.md) 維護。
