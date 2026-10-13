# A₄：mixed-(1,2)+a-unary 的原共用 pair 04／04 來源排除

**獨立驗收（2026-10-04，D₅）**：[最終成果固定快照與稽核](../audits/2026-10-04-task-d5/REPORT.md)
核對原04／04及root交換、四rotations、actual C/U支援、完整三hub前提，
整份C替換逐點保持全部外部，只主張(a,b,u)投影等式；六角色joint不等
反例與01202 singleton1／3保持。逐身份ledger為16／20、40／58支援、
50／84schedules；原A至A₃正文／artifacts及各輪數字保持當輪語境。
未用D₅來源搬運，其他mixed12身份／ε≥3未證；現行入口由Kempe導覽維護。

2026-10-04，接續 [A₃ 的 01／01 停止點](c5_excess_two_mixed_core_four_spoke_mixed12_01_01.md)
與 [Kempe 導覽 §3](c5_kempe_guide.md#3-停止點與保留缺口)。本輪只固定原
spokes=04／04，含整對 root 身份交換；四份 disk rotations、原 C 完整
ternary、U actual supports／singleton schedules、同一字面色框與六角色
joint 均逐份核對。實際驗證見 [A₄ 研究紀錄](history/2026-10-04-excess-two-four-spoke-mixed12-04-04.md)。

**在 A 的原來源前提下，04／04 的整份原來源排除，含 root 交換。**
本入口自己的原 0–4 crosscuts 與 ab 迫 C 位於固定 0ab 或 4ab；
完整 degree 握手式迫 actual support 正是 {0} 或 {4}。原互異色三角
a,b,h 滿足 exact degree-list、連通外部 K₄ 排除與三-hub 引理的全部
前提。每份合法 C 外染色都可只替換整份原 C，故固定原 ax 非 Σ-critical。
拒絕列 01202 的 U singleton **1／3** 亦各給完整原 joint 矛盾。

A₃ 的 18／22 具名框架降為 **16／20**，本入口殘留 **0／0**。
這是條件式任意大小紙面排除與固定 Python 關係控制；沒有搬運 A₃ 的
來源結論，沒有套用 mixed11 sealed triangle 或其原 mixed 省略定理。
Mixed12 整型、其他共用 pairs、來源實現、ε≥3、一般出口與 K∞=K≤5
仍未證，未新增 Lean theorem。本輪未 commit／push。

## 1. 原來源與完整有序關係

完整來源前提沿用 [A §1–3](c5_excess_two_mixed_core_four_spoke_mixed12.md#1-原來源完整-ternary-與六角色-joint)：
G 有限簡單，指定有序 induced-C₅ 外框 B=(b₀,…,b₄) 是 disk 邊界；
完整 Σ=933／941，每條非框邊 Σ-critical。有效 H 連通、ε=2，恰有
相鄰完整 degree-5 roots a,b，原 ab 存在，其他有效內點完整 degree 四。
H−{a,b} 恰為原 mixed C 與 a 側原 unary U，原接線是 ax、by₀、by₁、au。
y₀≠y₁；x 可獨立或與其中一個原接點相同；u∈U 與 C 互異。
兩 roots 的原 spokes 都恰為 04。所有原內邊、actual attachments、
bridges、旁支、ownership、接點身份與原環序保持。

在一個共同字面四色框 U₄={0,1,2,3} 中，原完整 relations 是
R_C(β;x,y₀,y₁)、R_U(β;u)。六角色 joint 是

\[
J_G(β)=\{(A,D,X,Y_0,Y_1,T):
(X,Y_0,Y_1)\in R_C(β),\ T\in R_U(β),\
A,D\in U_4\setminus\{β_0,β_4\},\
A\ne D,X,T,\quad D\ne Y_0,Y_1\}. \tag{1}
\]

每份 tuple 使用整份原 C、U coloring witnesses，固定 (β,A,D) 保留
完整 fibres，包括空 fibres。若 x=yⱼ，同一原頂點的兩個座標必同色；
兩個不同 owner guards 同時作用，不複製頂點，也不乘 contact marginals。
Root 交換搬運實體 5↔6、C owners、U owner、contacts、原邊與 rotations；
tuple 按搬運後的具名角色排序，boundary 與字面色框固定。

沿用 A 已證原 a-spoke 省略與 N=G−U 各自全收。在每個原拒絕列，
先完整接合原 C 與 roots，再取 N 的 a-domain，得到必要身份

\[
P_N(β)=R_U(β)=\{d_β\},\qquad
d_β\in U_4\setminus\{β_0,β_4\}. \tag{2}
\]

式 (2) 是同一原 U 的整份 relations，不是逐列任選 endpoint 禁色。
以下 ax 非 critical 的全列論證不依赖式 (2)；指定拒絕列出口才使用它。

## 2. 四份原 rotations、共同 faces 與 actual supports

原 paths 0–a–4、0–b–4 只在原框 endpoints 相交；ab 在兩 paths
中間，切出兩個原三角 0ab、4ab。C 連通、避開骨架，ax、by₀、by₁
均存在，所以 C 和三條接線只能位於同一份 closure 含兩 roots 的 face。
固定某個原 h∈{0,4}，便有

\[
C\subseteq\operatorname{int}(hab),\quad N_B(C)\subseteq\{h\},\quad
4|V(C)|=2|E(C)|+3+|E(C,B)|. \tag{3}
\]

三條原 contact edges 即使 x=yⱼ 仍是三條不同邊。最後一式迫
boundary attachment 邊數為奇數，所以空 support 不可能；actual support
**正是 {h}**。h 固定於原圖，不能隨染色列改選，也不能合併兩 face 的包絡。

每份原七頂點骨架重新核對 144 rotation assignments，恰四份 disk
rotations；完整有向 vertex rings 逐份保留，下表仅用無向 cyclic key 顯示。

| 原 rotation indices | 長 face | 另一個 root 外側短 face | 原 C 共同 faces |
| --- | --- | --- | --- |
| 0、3 | 0–1–2–3–4–6–0 | 0–4–5–0 | 0–5–6–0、4–5–6–4 |
| 1、2 | 0–1–2–3–4–5–0 | 0–4–6–0 | 0–5–6–0、4–5–6–4 |

四個具名 frames 是 `933:a5:b6:Sa04:Sb04`、
`933:a6:b5:Sa04:Sb04` 及兩份同名 941 frames；generic source indices
分別是 128／198。Root swap 的原 rotation bijection 為 `[1,0,3,2]`；
不重新 canonicalize 成另一份 embedding。

[完整來源支援引理](c5_independent_support_capacity.md#11-degree-與完整支援)
迫有效內部碰齊五框點。Roots 只碰 04、C 只碰 h，所以

\[
\boxed{\{1,2,3\}\subseteq S_U=N_B(U).} \tag{4}
\]

U 連通且 au 存在，只能位於固定 a-incident face。式 (4) 排除
0ab、4ab 及 a–0–4 短 face，故 U 位於原長 face 0–1–2–3–4–a–0。
a=5 使用 rotations 1、2，a=6 使用 0、3；每份 U placement 的 C
faces 只從同一 rotation 取得。此 index 對應與 A₃ 不同。

以下保留完整繼承 schedules；933 的拒絕 row indices 是 1、3、4、6，
941 是 1、4、6，表內色序逐一對應這些原字面列。

| 原 actual U support | 933 schedules | 941 schedules | 含 123 |
| --- | --- | --- | --- |
| 013 | 無 | (2,1,1) | 否，缺 2 |
| 134 | 無 | (2,1,1) | 否，缺 2 |
| 0123 | (3,3,3,3) | (2,1,1) 或 (3,3,3) | 是 |
| 0134 | 無 | (2,1,1) 或 (3,3,3) | 否，缺 2 |
| 1234 | 無 | (2,1,1) | 是 |
| 01234 | (2,2,1,1) 或 (3,3,3,3) | (2,1,1) 或 (3,3,3) | 是 |

含 root 交換，繼承 support records 是 4／12，完整 schedules 是
6／18；式 (4) 相容者分别是 **4／6**、**6／10**。每份 support 的
完整 relation 与原 face／rotation 相容資料均保留，不將表內 schedules
稱為來源實現。Actual support 123 在兩 masks 都沒有必要 schedules。

## 3. 互異色、完整 degree-list 與原外部路徑逐項核對

固定任一 proper β 與原 C 外逐點合法 coloring。a,b 都避開 β₀、β₄，
ab 迫 A≠D，因此 A,D,β_h 三色互異。原 a,b,h 是三個兩兩相鄰的
字面 singleton hubs，不涉及外點收縮。原 C 的 exact lists 是

\[
L(v)=U_4\setminus\bigl(β(N_B(v))
\cup(\{A\}\text{ if }v=x\text{ else }\varnothing)
\cup(\{D\}\text{ if }v\in\{y_0,y_1\}\text{ else }\varnothing)\bigr). \tag{5}
\]

每點外鄰恰為 {a,b,h} 的一個實際子集；G 簡單，三 hub 色互異，故
\(|L(v)|=4-|N_G(v)\setminus C|=\deg_C(v)\)。by₀、by₁ 是同一 b
的兩條不同原邊；x=yⱼ 時式 (5) 同時扣除 A,D，保留完整 degree。
Checker 在每個 h、十列及兩份合法 ordered root pairs 上逐一核對
八個實際外鄰子集；不是將三種 contact 色獨立任選。

若 C 拒絕，connected degree-list 刻畫迫原 C 是 Gallai tree，lists
blockwise uniform；直接核對的外部依賴為
[Dvořák Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)。
前提是原 C 連通與 degree assignment，不需要 G 或 G−ax 是 minimal q-core。

**K₄ 的原外部。** 若 C 有 K₄ block Q，每個 clique 點已有三個內鄰，
完整 degree 四迫恰一個離開 Q 的原方向：直接接到原 X={a,b,h}，或
經 C 中一條 bridge 離開 Q。不同 clique 點的 bridge 外側互不相交；
否則 Q 不是原 block。刪 bridge 後兩側 endpoint 各有 list slack，
兩側均可著色；若 endpoint domains 可選不同色便可接回 C，故拒絕
迫兩側同一 singleton。外側若完全不碰 X，其完整 coloring 可置換
四色，endpoint domain 不可能 singleton。因此四條原 paths 都抵達 X。
X 本身是**原連通三角形**；四 paths 去掉 clique endpoints 的部分與
X 合成外部 branch set，再加 Q 四 singletons，得到原 G 的 K₅ minor。
此核對不假定另一条外部 path，也不使用 U 的收縮。

K₄-free 後剩餘 blocks 只有 bridges 或 odd cycles，逐項符合
[三-hub 引理](c5_short_support_singleton.md#4-三-hub-引理排除未見色接點數不設上限)。
末端 odd-cycle 的相鄰 private u,w 由同一二元 block palette 接同一
對 hubs；第三 hub 與 C′=C−{u,w} 合成第五 branch set，原 cycle
端邊與 hub triangle 給所有鄰接。若第三 hub 不碰 C，用原兩-hub
分支。末端 bridge 的 private u 接齊三 hubs、list 是唯一未用色；
刪 uv 使 C′ 有 slack，拒絕迫 v 完整 domain 為該 singleton。若 C′
漏某 hub，交換未用色與其 hub 色便破壞 singleton，所以 C′ 接齊三
hubs；三原 hub singletons、{u}、C′ 再給原 K₅。所有 branch sets
互斥連通，鄰接來自原邊，與 planarity 矛盾。

因此每份合法原 C 外 coloring 都有**完整原 C extension**，得到
\((X,Y_0,Y_1)\in R_C(β)\)，同時满足 X≠A、Y₀≠D、Y₁≠D，包含
所有接點共享情形、任意 C 大小、原 bridges 與旁支。

另逐項保存 A 繼承的短 U 外路徑前提：包住 support 的框邊若不是
04，原 skeleton 可用 a–0／a–4 或 a–b–h 提供避開 U、C 的實際路徑，
checker 逐邊核對。若包絡框邊是 04，skeleton 沒有到外側框點的邊；
原完整支援引理只能条件式迫 C 接到 04 外。但式 (3) 已禁止這件事，
所以該短 U 與本入口來源幾何不相容，不能捏造 skeleton path。
本節完整 C extension 只使用原三角 X，**不依賴任何短 U 路徑排除**。

## 4. 原 ax 非 critical 與拒絕列的完整 joint

取任一 G−ax 完整 coloring，保留 B、a、b 與原 U 每個頂點的
字面顏色，忘掉整份 C witness。這仍是一份原 C 外合法 coloring；
上一節只重染原 C，恢復 ax、by₀、by₁，C 外逐點不動。因此

\[
\boxed{\pi_{a,b,u}J_G(β)=\pi_{a,b,u}J_{G-ax}(β)}. \tag{6}
\]

更強的 witness 敘述保持原 U 全部頂點，而不只是 u。完整六角色
tuple 的 X,Y₀,Y₁ 可以改變，**不主張 J_G=J_(G−ax)**。投影非空
恰判定列接受，故 Σ(G)=Σ(G−ax)，原非框邊 ax 不 critical，與來源
前提矛盾。Root 交換也搬運這條原 owner incidence。

共同拒絕列 q=01202（row 4）有 spoke 色 0、2。式 (2) 迫
R_U(q)={d}，d∈{1,3}，同一原 schedule 與整份 U witness 均保持。
取

\[
(A,D,T)=(4-d,d,d)=
\begin{cases}(3,1,1),&d=1,\\(1,3,3),&d=3.\end{cases} \tag{7}
\]

原 spoke guards、ab、au 均合法；h=0／4 時第三 hub 色是 0／2，
兩份情形皆三色互異。完整 C extension 因而在同一字面 q 下接出
\((4-d,d,X,Y_0,Y_1,d)\in J_G(q)\)，違反原拒絕。不把 A₃ 的
d=2／3 或 (5−d,d,d) 抄到此入口。

## 5. D₅ 界線、固定控制與完整 ledger

本來源排除直接在原 04／04 證明，**沒有使用 D₅ 來源搬運**。
Checker 另保存兩份 01→04 的幾何捷徑診斷：

| 原 boundary move i↦p(i) | 完整 Σ933 image | 完整 Σ941 image |
| --- | ---: | ---: |
| p=(0,4,3,2,1) | 948 | 950 |
| p=(4,0,1,2,3) | 934 | 950 |

每份診斷同時保存十列 index map、完整拒絕列、搬運後 boundary 及
同一列的**一份共同 S₄ 色置換**；這份色置換須同時作用於 C ternary、
U relation 及六角色全部欄位，不能各自正規化。這兩個 boundary moves
保持原 a,b roles；另加 root swap 才搬運實體 5↔6、U owner 與所有
contacts／rotations。診斷未搬運 source relations 或登記來源結論；
沒有任何固定 933／941 mask 的 01→04 shortcut。

[A₄ checker](../scripts/c5_excess_two_mixed_core_four_spoke_mixed12_04_04.py)
唯讀 A₃ ledger，從 generic source 逐份重建四個選定原 frames；核對
四 rotations、同 embedding 的 C／U faces、完整原 omission identities、
實際 supports、全部 singleton schedules、原短 U 路徑前提與 root swaps。
[新 joint helper](../scripts/c5_excess_two_four_spoke_mixed12_04_04_joint_controls.py)
以明列有限完整 degree 圖獨立全圖回溯核對完整 ternary、R_U、六／五
角色 joints、全部 16 root-pair fibres 與整份 witnesses；只替換 C 的
coloring 保持全部 exterior 頂點，保存投影等式與六角色不等負控制。
共有 24 張完整 degree 圖與 12 份 root swaps；三種 x 身份各八張。
獨立全圖回溯核對 1,920 joins／30,720 fibres，其中 25,632 空 fibres；
保存 25,568 份六角色及 1,600 份五角色 tuple witnesses。240 份 ax
投影等式、2,912 份只替換整份 C 的 witnesses 與 480 份合法 root-pair
完整 C extensions 均核對；另有 2,080 份逐點 exact degree-list checks。

q=01202 的兩種 singleton 各有 12 張控制：triangle U 支援 124 給
d=1，缺本來源必要端點 3；singleton U 支援 123 給 d=3，只符合
支援包含條件，仍不實現繼承的完整 schedules（123 在必要表無 survivor）。
兩族圖的完整 Σ 都是 1023。有限 controls 不宣稱 disk、Σ-critical、
933／941 或必要 schedules 的來源實現。

六角色不等負控制在 control 4、row 01012：G−ax 獨有 tuple
是 (1,3,1,1,0,0)，原 ax 因 X=A 不合法；重染完整 C 得原 G tuple
(1,3,0,0,1,0)，同一 exterior (a,b,u)=(1,3,0) 及原 U witness
逐點固定。Artifact 另保留 ternary marginals 假接合負控制；其原
root-spoke 資格另列，不當成合法 source root pair。

| 同一 mixed12 必要域，含 root 交換 | 933 | 941 |
| --- | ---: | ---: |
| A₃ 原具名 frames | 18 | 22 |
| A₄ 新排原 04／04 | 2 | 2 |
| 選定原 U face／support records | 4 | 12 |
| 選定完整 singleton schedules | 6 | 18 |
| 完整來源支援相容 records／schedules | 4／6 | 6／10 |
| 本入口來源殘留 | 0 | 0 |
| **保存其餘完整具名 frames** | **16** | **20** |
| 保存其餘 actual U face／support records | 40 | 58 |
| 保存其餘完整 singleton schedules | 50 | 84 |

完整 [A₄ artifact](../artifacts/c5_excess_two_mixed_core_four_spoke_mixed12_04_04/observations.json)
保存上述全部資料、輸入 SHA-256 及 witnesses；A／A₂／A₃ artifacts
不覆寫。其他原具名物件逐項原樣保存，沒有將此次結果登記到其他 pairs。
任意大小拓撲、Gallai 與 K₅ minor 是紙面層；Python 是固定域／關係
證書；`lake build` 不形式化這份原圖幾何或一般延拓。

## 6. 重播與停止點

```bash
python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed12_04_04.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed12_04_04.py --check
python3 scripts/c5_excess_two_four_spoke_mixed12_04_04_joint_controls.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
python3 tools/artifacts.py status
git diff --check
```

主 checker 無參數只生成 A₄ 的新 artifact；`--check` 唯讀逐 byte 比對。
Helper 重算有限 controls，不寫前序 payload。實際執行與沿用範圍見
[本輪研究紀錄](history/2026-10-04-excess-two-four-spoke-mixed12-04-04.md)。
未全面重跑來源 minimality、歷史容量／省略或 R 系列，不重開圖 catalogue。

**停止於原 04／04 與 root 交換整份來源排除，其餘 16／20 frames
保留。** 后續窄入口與目前停止點由 [Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口)
維護；其他共用 pairs 須各自核對原 geometry、完整 degree-list 與外部
路徑前提。Mixed12 整型與 ε≥3 仍未證。
