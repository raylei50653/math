# A₂：mixed-(1,2)+a-unary 的原 01／12 長／短 face 來源排除

**獨立驗收（2026-10-04，D₅）**：[最終成果固定快照與稽核](../audits/2026-10-04-task-d5/REPORT.md)
核對原04／04及root交換、四rotations、actual C/U支援、完整三hub前提，
整份C替換逐點保持全部外部，只主張(a,b,u)投影等式；六角色joint不等
反例與01202 singleton1／3保持。逐身份ledger為16／20、40／58支援、
50／84schedules；原A至A₃正文／artifacts及各輪數字保持當輪語境。
未用D₅來源搬運，其他mixed12身份／ε≥3未證；現行入口由Kempe導覽維護。

**獨立驗收（2026-10-04，D₄）**：[正式返回工作區稽核](../audits/2026-10-04-task-d4/REPORT.md)
已核對A₃後續；最新ledger為18／22、44／70支援、56／102schedules。
本頁A₂當輪20／24及原artifact保持，其他mixed12身份未驗收。

**後續（2026-10-04，A₃）**：[共用01／01報告](c5_excess_two_mixed_core_four_spoke_mixed12_01_01.md)
已完成本頁停止後的具名入口，含root交換；原三hub延拓使固定ax非critical。
其餘必要域現保存18／22框架、44／70支援、56／102relations。本頁20／24
及原artifact保留當輪語境；mixed12整型與ε≥3仍未證。

2026-10-04，接續 [A 報告 §7](c5_excess_two_mixed_core_four_spoke_mixed12.md#7-重播停止點與下一入口)。
固定原 a=5、b=6、spokes=01／12，包含整對 root 身份交換；沒有擴大
來源圖枚舉，也沒有將同一幾何推廣到其他具名入口。驗證與貼用摘要見
[A₂ 研究紀錄](history/2026-10-04-excess-two-four-spoke-mixed12-01-12.md)，
目前停止點見 [Kempe 導覽](c5_kempe_guide.md)。本輪未 commit／push。

**在 A 的原來源前提下，01／12 的整份原來源排除，含 root 交換。**
Critical U 的固定 actual support 確含框點 2；同一原 U crosscut 把長
face 的 C 封至 {2}，短共同 face 的 C 則只碰 {1}。共同拒絕列
**01202** 上固定 (a,b,u)=(3,0,2)，兩種位置都由既有三-hub Gallai
引理取得完整 C witness，接成原六角色 joint，與拒絕矛盾。
A 的 22／26 具名殘留因此降為 **20／24**；本題殘留 **0／0**。
這是條件式任意大小紙面排除與固定 Python 控制，**mixed-(1,2) 整型、
來源實現、ε≥3、一般出口及 K∞=K≤5 未證，未新增 Lean theorem**。

## 1. 原來源與完整六角色接合

完整前提沿用 [A §1–3](c5_excess_two_mixed_core_four_spoke_mixed12.md#1-原來源完整-ternary-與六角色-joint)：
G 有限簡單、B=(b₀,…,b₄) 是指定有序 induced-C₅ disk 外框，完整
Σ=933／941，每條非框邊 Σ-critical；有效 H 連通、ε=2，恰有相鄰
完整 degree-5 roots a,b，原 ab 保持，其餘有效內點完整 degree 四。
H−{a,b} 恰為原 mixed C（ax、by₀、by₁）及 a 側原單接點 unary U
（au）。固定 S_a=01、S_b=12；y₀≠y₁，x 可與其中一個原頂點相同。

原 C、U 所有內邊、actual attachments／supports、bridges、旁支、
ownership、原嵌入環序及同一字面四色框保持。記原完整有序 relations
R_C(β;x,y₀,y₁)、R_U(β;u)，則

\[
J_G(β)=\{(A,D,X,Y_0,Y_1,T):
(X,Y_0,Y_1)\in R_C(β),\ T\in R_U(β),\
A\notin β(01),\ D\notin β(12),\
A\ne D,X,T,\ D\ne Y_0,Y_1\}. \tag{1}
\]

共享 x=y_j 時兩個座標來自同一原頂點，同時保留 a、b 的不同 guards。
先保留完整 ternary 與全部 witnesses，再取固定 root-pair fibre；
不能相乘接點 marginals。Root 交換搬運整圖、原 U ownership、完整
tuple 欄位及路徑，boundary 與色框不變。

A §2 已證 a-spoke 省略及 N=G−U 各自全收；前者刪 b 後是單一
C+a+U ternary，後者是 C+a ternary。本輪沿用這個紙面身份，沒有
重開其来源分類，也沒有稱 degree 降三的 G−au 是 minimal q-core。
完整五角色 T_N 與原 R_U 的接合給每個原拒絕列

\[
P_N(β)=R_U(β)=\{d_β\},\qquad d_β\in U_4\setminus β(01). \tag{2}
\]

式 (2) 的投影只在完整 N joint 之後取，不替代式 (1) 的原 C relation。

## 2. 同一原 U 的位置、singleton 與 actual 2 附件

原七頂點骨架的 disk faces 為

| 原 face | boundary 包絡 | 原角色 |
| --- | --- | --- |
| a–0–1–a | {0,1} | a incident |
| b–1–2–b | {1,2} | b incident |
| a–1–b–a | {1} | 短共同 face |
| a–0–4–3–2–b–a | {0,2,3,4} | 長共同 face |

整份連通 U 及 au 位於同一 a-incident face。前兩個 a-incident 短
位置的 actual support 均包含於框邊 01；原 a–b–2 是避開 U 的
pair 外路徑。[短支援引理](c5_short_support_singleton.md#1-原圖完整接點-relation-與外部路徑)
使 au 非 critical，故 critical au 迫 **U 固定位於長 face**，
其同一 actual support S_U⊆0234，不能逐列改位置。

取 q=01202（row index 4），兩 masks 都拒絕。q 在整個長 face 的
boundary 包絡只見 0、2。字面置換 π=(1 3) 固定全部 actual
attachments；整份原 U coloring 搬運使完整 R_U(q) 在 π 下不變。
式 (2) 給 singleton 候選 {2,3}，所以

\[
\boxed{R_U(01202)=\{2\}.} \tag{3}
\]

這一步保持實際附件，即使支援是包絡的 proper subset 也成立。
所有原拒絕列都未用色 3；由
[單接點固定未用色守恆](c5_single_spoke_root_conservation.md#2-單接點固定色引理)，
同一原 U 的其他 singleton 不能取 3。因原 a-spokes 在所有拒絕列
均見 0、1，故它們全部也是 {2}。

若 2∉S_U，則 S_U⊆034。在這個同一 actual support 上，字面
(1 2) 把 01212 的全部原附件色搬到 01021，卻把必要 singleton
2 搬成 1，矛盾。這也是 [A §5](c5_excess_two_mixed_core_four_spoke_mixed12.md#5-同一原-u-的三列-relation-矛盾完成具名來源排除)
的三列守恆反證；該論證只用 a-spokes 01 與 S_U⊆034，沒有用
b-spokes 23。因此 **原 U 確有 actual 2 附件**，不是以有限 survivor
表代替任意大小的覆蓋證明。

原 au、U 連通性與該附件給一條 simple 原路徑

\[
P:a-u\leadsto z-2,\qquad P\setminus\{a,2\}\subseteq V(U). \tag{4}
\]

它在原長 face 內，是同一原 U 的 crosscut，與整份 C 頂點互斥。

## 3. 固定共同長／短 face 封閉原 C 支援

因 C 同時接 a、b，它只能位於上述兩個共同 faces。

**短 face** 是原三角 a–1–b，直接給 N_B(C)⊆{1}。

**長 face** 中原 P 的 endpoints 是 a、2。原 b 位於 P 的 b-side；
原 by_j 接線與 C 的連通性迫整份 C 位於該側。若 C 實際接到
0、4 或 3，原 b–y_j↝C–h 與 P 的 endpoints 沿 face 依次為
a,h,2,b，兩條原互斥 paths 交錯，違反同一 disk 嵌入。因此

\[
\boxed{N_B(C)\subseteq\{1\}\quad\text{或}\quad N_B(C)\subseteq\{2\}.} \tag{5}
\]

兩個包絡不相加；empty support 亦保留在局部 lemma 的範圍內。
固定控制在長 face 的每個 forbidden endpoint 0、4、3 保存原
disjoint-path 收縮及 outside-disk apex K₃,₃ subdivision；這是
minor／拓撲反證控制，不是保留 Σ 或完整 joint 的 relation factor。

另由原來源碰齊五框點，式 (5) 與 roots 只接 012 已迫 U 同時
實際碰 3、4。因此繼承的 support 023 在這個 C 幾何階段已不符合
完整来源支援；下面指定列論證仍覆蓋全部繼承身份，不另擴大分類。

## 4. 指定拒絕列的完整 C extension 與 joint 矛盾

固定 q=01202，取式 (3) 的一份整份原 U witness，令

\[
(A,D,T)=(3,0,2). \tag{6}
\]

a 的 spokes 01 見 0、1，b 的 spokes 12 見 1、2，且 A≠D,T，
所以這是一份原 C 外逐點合法 coloring。

| 原 C 位置 | 三個原外鄰 roles | 指定外鄰色 | 原 hub triangle |
| --- | --- | --- | --- |
| 短 a–1–b | a,b,1 | 3,0,1 | ab、a1、b1 |
| 長 face 的 b-side | a,b,2 | 3,0,2 | ab、b2、同一原 P |

在長 face 情形，取 X={a}∪(P 的內點)、Y={b}、Z={2}；短 face
則取原三個 singleton hubs。三組互斥連通，原邊／原 P 使它們
兩兩相鄰。原 C 沒有任何邊到 P 的 U 內點；a、b、h 進入不同
hub，所以每個原 C 頂點完整 degree 四、全部實際 incidences、
內部圖及 exact lists 都保持，包括 x=y₀／y₁。
Hub 的辅助色只匹配 C 的原外鄰色；不聲稱整份原 P coloring 在
收縮後保持，也不將收縮當作 source-state 操作。

若 C 不可延拓，它的原 lists

\[
L(v)=U_4\setminus\bigl(q(N_B(v))\cup
(\{3\}\text{ if }v=x)\cup
(\{0\}\text{ if }v\in\{y_0,y_1\})\bigr)
\]

滿足 |L(v)|≥deg_C(v)。Connected slack-list 引理使拒絕時處處
tight；degree-list 刻畫使 C 是 Gallai tree，lists blockwise uniform。
所用外部依賴已直接核對
[Dvořák，Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)。

拒絕時 C 亦 K₄-free。原 B∪{a,b} 連通；K₄ block 每點的唯一
原外方向若是 bridge，刪橋後兩側 contact 有 list slack，兩個
根域均非空，拒絕迫同一 singleton。外側若不碰原外部，整份
四色置換便不能有 singleton。因此四個互斥方向均到同一連通
外部，與原 K₄ 給 K₅ minor。這是
[連通外部 K₄ 排除](c5_degree5_tree_components.md#1-連通外框排除-degree-4-分量的-k4)
在本原 C 拒絕 lists 的適用；不要求原 G 是 minimal q-core。

於是上述互異色三-hub 圖符合
[三-hub Gallai 引理](c5_short_support_singleton.md#4-三-hub-引理排除未見色接點數不設上限)。
若 C 拒絕，就有原 G 的 K₅ minor，矛盾。即使 C 不碰 boundary
hub，其 unused-hub 分支亦由同一引理涵蓋。故兩個原 face 都有
**一份完整原 C extension witness**，即某個

\[
(X,Y_0,Y_1)\in R_C(q),\qquad X\ne3,\quad Y_0,Y_1\ne0.
\]

它與固定的整份原 U witness、式 (6) 在同一字面 q 接合，得到

\[
\boxed{(3,0,X,Y_0,Y_1,2)\in J_G(01202).} \tag{7}
\]

原 933、941 均拒絕 q，所以整份具名來源不存在。整對 root 身份
交換逐點搬運相同論證。只需指定列的原 (3,0) fibre；本輪不主張
C 的所有 root-pairs 都延拓，也不主張六角色 joints 在 ax 省略後相等。

## 5. 固定證書、繼承域與證據界線

[A₂ checker](../scripts/c5_excess_two_mixed_core_four_spoke_mixed12_01_12.py)、
[完整 joint helper](../scripts/c5_excess_two_four_spoke_mixed12_01_12_joint_controls.py)、
[artifact](../artifacts/c5_excess_two_mixed_core_four_spoke_mixed12_01_12/observations.json)
唯讀 A 的原 artifact，僅重新指定四個 01／12 原框架，逐項核對
原七頂點 rotations、omission identities、actual U support／singleton
relations，保留原選定完整框架及全部其他殘留。沒有覆寫 A 的
149 MB 證書，也没有讀 mixed-(1,1) 完成表作新 incidence 分類。

| 同一 A 必要域，含 root 交換 | 933 | 941 |
| --- | ---: | ---: |
| A 原具名殘留 | 22 | 26 |
| A₂ 新排 01／12 | 2 | 2 |
| **保存其餘具名框架** | **20** | **24** |
| 保存其餘 actual U face／support records | 52 | 86 |
| 保存其餘完整 singleton schedules | 68 | 124 |
| 本具名入口原來源殘留 | 0 | 0 |

本題繼承的 actual U support records 為 4／6，各有唯一完整
singleton schedule，分別為 933 的 023／0234、941 的
023／234／0234，root 交換均保存。每份有同一 rotation 的 C 長／短
faces；本輪只移除這四份具名框架，其他框架、actual 支援及完整
relations 逐項保留，原 A 有限 witnesses 入口與 hash 保持。

新 helper 的手建完整 degree 控制覆蓋 C singleton-support 1／2、
x 獨立／共享 y₀／共享 y₁，三份 exact U supports 023／234／0234
及 root 交換。每份明列 actual attachments／原路径、全部十列
完整 R_C、R_U、原圖与省略圖的六／五角色 tuples、整份 coloring
witnesses 及全部 16 字面 root-pair fibres（包含空纖維）。獨立全圖
回溯核對 join、原 spoke／ax 接回、G−au=T_N×R_U，保留 marginal
假接合及六角色不相等的負控制。這些圖只是有限語義控制；即使
q=01202 上同一 R_U={2}，也不宣稱是 disk、Σ-critical 或 933／941
來源實現。精確計數及實際重播見 A₂ 紀錄。

## 6. 重播與停止點

```bash
python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed12_01_12.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed12_01_12.py --check
python3 scripts/c5_excess_two_four_spoke_mixed12_01_12_joint_controls.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
python3 tools/artifacts.py status
git diff --check
```

主 checker 無參數只生成新的 A₂ artifact，`--check` 唯讀逐 byte 比對；
helper 的 `--check` 重算固定 controls，不寫原 artifacts。原 minimality、
完整支援、未用色守恆及無界 Gallai／K₄ 紙面結果沿用，未全面重跑
它們的歷史證書；`lake build` 不形式化本輪的 disk／palette 論證。

**停止於原 01／12 及 root 交換整份排除，其餘 20／24 保留。**
後續候選入口可固定仍保留的原 01／01，保持四份原 disk rotations、
同一 C ternary、U actual 支援與完整 joint；本輪沒有繼續此題。
目前下一入口由 [Kempe 導覽](c5_kempe_guide.md) 維護。
