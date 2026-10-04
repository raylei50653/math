# 任務 B：四-spoke (2,2)、mixed-(2,2) 無 unary 的原身份與窄化約

**獨立驗收（2026-10-04，D₅）**：[最終成果固定快照與稽核](../audits/2026-10-04-task-d5/REPORT.md)
只接受W933-129／04–12／長face{2,3,4}的指定shared原附件{4}支：
六shared身份／八選擇、11tight pairs、連通K=C−v與完整degree握手式，
五袋非空／互斥／連通及十對原邊均獨立核對。整份W933-129、整個長face、
其他附件及原20／20表保留；B₂／B₃的兩primary閉合仍依前輪證據。
以下正文／前綴保持各輪截點，現行具名入口由Kempe導覽維護。

**後續（2026-10-04，B₄）**：[933原04／12的shared-{4}窄支](c5_excess_two_mixed_core_four_spoke_mixed22_shared4.md)
固定W933-129長face，真正shared leaf的原cut parity及五原bags給K₅，
六shared身份／八指定選擇此附件支全排。其餘身份／附件及整份骨架保留；
本層20／20原表與checker／artifact不改寫。

**獨立驗收（2026-10-04，D₄）**：[正式返回工作區稽核](../audits/2026-10-04-task-d4/REPORT.md)
合用B₂／B₃只登記W933-101／W941-139兩primary骨架封閉。
原20／20必要表不刪，其他19／19原列沒有本輪新判；root-swap對應
只保存搬運證據，不另登記新閉合骨架。

2026-10-04。接續 [disjoint-pairs 報告明列的保留分支](c5_excess_two_mixed_core_four_spoke_disjoint_pairs.md#6-重播停止點與下一incidence)，
與任務 A 的 mixed-(1,2) 加 unary 分開。保留接手工作樹全部既有成果；
現況與接續見 [Kempe 導覽](c5_kempe_guide.md)，實際驗證與貼用摘要見
[本輪紀錄](history/2026-10-04-excess-two-four-spoke-mixed22.md)。

**後續（2026-10-04，B₃）**：[同骨架原長 face 的五型 leaf／原 K₅](c5_excess_two_mixed_core_four_spoke_mixed22_long_face.md)
已獨立排除 W933-101／W941-139 的 {0,4,3}，七身份零長-face 殘留。
與 B₂ 的短 face 合用，這兩份骨架的原 mixed-capable faces 才全部封閉；
其他骨架仍保留。本層原 20／20 表、checker／artifact 保持當輪語境。

**後續（2026-10-04，B₂）**：[固定 01／23 原短 face 的 Gallai leaf／原 K₅ 排除](c5_excess_two_mixed_core_four_spoke_mixed22_short_face.md)
已涵蓋 §7 的第一個窄入口：W933-101／W941-139、envelope={1,2} 的
七種 contacts 身份均來源排除，沒有短-face 殘留；同一骨架長 face
{0,4,3} 及其他 faces 保留。下文 20／20 原必要骨架與當輪停止點
保留原語境；B₂ 未覆寫本層 checker 或 artifact。

**新增任意大小窄引理：四條原 spoke 的省略圖各自全收 Ω；每個原
拒絕列的 minimal q-core 就是原 G，兩 roots 都仍 degree 五。**
七種原 contacts 身份全部列明，保持完整 R_C(x₀,x₁,y₀,y₁) 及同框
六角色 joint。前序 933／941 的 47／75 份必要骨架由此只餘各 25 份
相鄰 spoke-pairs，再排相同 pair 各五份，**仍保留 20／20 份具名必要
骨架及其原 face**；本頁沒有排除 mixed-(2,2) 整型，也沒有宣稱來源實現。
共同 ε≥2 不變，ε≥3、一般出口與 K∞=K≤5 未證，未新增 Lean theorem。

## 1. 同一原圖與完整七種身份

G 有限簡單，指定有序 induced-C₅ B=(b₀,…,b₄) 是 disk 外框。
完整 Σ=933／941 或整圖 D₅ 像，每條非框邊 Σ-critical。
有效內部 H 連通，ε=2；a,b 相鄰且完整 degree 五，其餘有效內點
完整 degree 四。H−{a,b} **恰為唯一原連通 C，沒有 unary**。

原 a-spokes 是兩點集 S_a，b-spokes 是兩點集 S_b；原 ab 存在。
另有原邊 ax₀,ax₁,by₀,by₁，且 x₀≠x₁、y₀≠y₁。
兩側之間的共享是部分 matching，因此全部具名身份恰有七份：

| 原身份 | 原頂點相等類（未列相等即互異） | 不同原 contacts 數 |
| --- | --- | ---: |
| D4 | x₀；x₁；y₀；y₁ | 4 |
| S00 | x₀=y₀；x₁；y₁ | 3 |
| S01 | x₀=y₁；x₁；y₀ | 3 |
| S10 | x₁=y₀；x₀；y₁ | 3 |
| S11 | x₁=y₁；x₀；y₀ | 3 |
| Pstraight | x₀=y₀；x₁=y₁ | 2 |
| Pcross | x₀=y₁；x₁=y₀ | 2 |

原 contact 的順序、ownership、所有 C 內邊／bridges／旁支、實際
boundary attachments／supports、嵌入環序及同一字面四色框保持。
共享角色佔同一原頂點，relation 的對應座標必相等，不複製成兩點。

令 U₄={0,1,2,3}，R_C(β) 是原 C 完整合法染色在有序
(x₀,x₁,y₀,y₁) 的 relation，每個 tuple 附一份整個 C 的 witness。
定義 E_r(β)=U₄−β(S_r)。原完整 joint 精確為

\[
J_G(β)=\{(A,D,X_0,X_1,Y_0,Y_1):
 (X_0,X_1,Y_0,Y_1)\in R_C(β),\quad
 A\in E_a,\ D\in E_b,\ A\ne D,\
 A\notin\{X_0,X_1\},\ D\notin\{Y_0,Y_1\}\}.\tag{1}
\]

根色固定後只拼接**同一原 C** 的整份 witness；不相乘四個 marginals，
也不為不同列、兩側或分量各自選色框。

## 2. G−C、原 spoke 省略圖及 q-core 的合法身份

**G−C。** 這是原 B、a,b、ab 與四條 spokes，兩 roots degree 各三。
其完整 root-pair relation 為

\[
Z_{G-C}(β)=\{(A,D)\in E_a(β)\times E_b(β):A\ne D\}.\tag{2}
\]

兩側各至多看到兩色，|E_a|,|E_b|≥2，式 (2) 對每個 proper β 非空；
直接得到 Σ(G−C)=Ω。**它不是 degree≥4 的 q-core**，也沒有套用
mixed-(1,1) 的「省略 C」定理。

**原 spoke 省略。** 取 e=ab_j、j∈S_a，M=G−e，root degrees=(4,5)。
M−b 的唯一原內分量是

\[
K=C\cup\{a\},\qquad P_K=(a,y_0,y_1),\qquad\deg_K(a)=2.\tag{3}
\]

K 透過兩條原 ax₀,ax₁ 連通；三個 b-contacts 永遠互異，包括七份
跨側身份。a **不是 leaf**，保留一條原 boundary spoke。其餘 K 點
及 a 在 M 的完整 degree 都是四；b 保留兩條原 spokes 與三條原
contacts ba,by₀,by₁。

令 E_a^e=U₄−β(S_a−{j})，則

\[
R_K(β)=\{(A,Y_0,Y_1):\exists X_0,X_1,
(X_0,X_1,Y_0,Y_1)\in R_C(β),\ A\in E_a^e,
A\notin\{X_0,X_1\}\}.\tag{4}
\]

J_M 只在式 (1) 把 E_a 換成 E_a^e；接回原 e 恰過濾 A≠β_j。
式 (4) 的存在量詞由完整 C witness 承擔，不能把 K 看成三份 unary。
省略 b-spoke 的對稱原身份是 C+b、contacts=(b,x₀,x₁)、marked b 內度二。

**原 q-core。** 沿用 [原省略身份與飽和](c5_excess_two_mixed_core_spokes.md#2-全部-proper-core-的具名省略表)：
原刪 roots、刪 ab 全收，故 minimal q-core L 含 a,b,ab；C 只能全取
或全不取。省略 C 損失 incidence=(2,2)，使 roots 降到三，不能發生。
每 root 至多失去一條原 spoke。因此合法原身份只有下表九份：

| L 的 root degrees | 可省略的原身份 | 本頁之後的狀態 |
| --- | --- | --- |
| (5,5) | 無，L=G | 保留原 G |
| (4,5) | a 側兩 spokes 任一，共兩份 | §3 全收，不可拒絕 |
| (5,4) | b 側兩 spokes 任一，共兩份 | §3 全收，不可拒絕 |
| (4,4) | 每側各省略一條 spoke，共四份 | 既有原 (4,4) 排除 |

原 Σ-minimality 本身不等於 q-minimality；「L=G」是在上述全部 proper
身份排除後才得到。

## 3. 任意大小窄引理：每條原 spoke 省略均全收

反設 M=G−e 拒絕某 q，取它自己的 minimal q-core L。
a 在 M 已 degree 四，全部原 M 邊必保留；原 C 亦飽和保留。
若 b 再失一條 spoke，便是已排除的原 (4,4) core。
故 b 仍五，**L=M**，不是把 G 的 Σ-minimality直接換成 M 的 q-minimality。

於是 M 符合 [two-spoke 三接點排除](c5_two_spoke_three_contacts.md) 的全部
前提：指定 induced-C₅ disk、唯一 degree-5 root b、兩條原 spokes、
其餘點完整 degree 四、連通 K=C+a、三個不同原 contacts (a,y₀,y₁)。
既有定理給原 M 的 K₅ minor，矛盾。該定理涵蓋任意大小的 K、
實際 tethers、bridges 與旁支，不需要 unary、第二拒絕列或新 T4 假設。

因此

\[
\boxed{\Sigma(G-e)=\Omega\quad\text{對四條原 spokes 各自成立}.}\tag{5}
\]

結合 §2，任一原拒絕 q 的 minimal q-core 均為原 G，root degrees=(5,5)。
這只完成本頁 incidence 的單 spoke 省略；一般唯一 mixed 的单省略仍保留。

### 條件式原 triangle 與 K₅ 的明示提取

在反設 M 拒絕下，既有三接點證明給同一 K 的 active triangle 與三臂，
末端恰為 a,y₀,y₁。K−a=C 連通，故內度二的 a 不是 cut vertex；若
a 的 active block 是 bridge，其另一條 K 邊會使 a 成 cut vertex，矛盾。
所以 a 自己是 active triangle 的頂點、其臂長零，triangle 恰為
**(a,x₀,x₁)，原 x₀x₁∈E(C)**。另兩臂為偶長；共享 x_i=y_j 迫對應臂長零。

五 bags 是 {b}、triangle 的三份原臂 bags（a 的是 {a}）及 B 加實際
tether 內點。原 triangle 三邊、ba/by₀/by₁、三條實際 tethers、任一
保留 b-spoke 給十對鄰接。Checker 按七身份、兩種 a-spoke 省略保存
14 份原邊控制，a、b 的原 degree 五及 C 連通均核對。
**這是反設 M 拒絕的提取控制，不表示保留來源都含 x₀x₁，也不是
完整 degree/list 圖或 Σ-preserving 收縮。** 未用 arm 頂點的 degree 邊未補滿。

## 4. 原 face／hub 的必要收窄與具名保留

若某拒絕 q 讓同側兩原 spokes 同色，刪任一條後染色集合與 G 相同，
仍拒絕 q，違反式 (5)。在固定 Σ 的全部拒絕列上都異色的兩點集，
對 933／941 **恰為五條原 C₅ 邊** 01、04、12、23、34。
這是固定列位置控制；不獨立正規化兩側。

| 原必要骨架 | 933 | 941 |
| --- | ---: | ---: |
| 前序具名四-spoke (2,2) | 47 | 75 |
| 同色 spoke 違反式 (5) | 22 | 50 |
| 兩側皆相鄰 spoke-pair | 25 | 25 |
| 相同 pair：sealed triangle 排除 | 5 | 5 |
| **保留具名必要骨架** | **20** | **20** |

25 份骨架是五條原框邊的有序 pairs，每個原 C 連通且接兩 roots，
必位於一個同時 incident a,b 的固定 open face。完整原 contacts
的共享不改變這個 face 判定。

- **相同 pair**：原 diamond 封 C 於 (a,b,b_h) 或 (a,b,b_k) 的一個
  原三角形；外鄰只有這三個 hubs。原合法三角染色的三個色互異，
  [不限接點數的三-hub 引理](c5_short_support_singleton.md#4-三-hub-引理排除未見色接點數不設上限)
  延拓整個 C。接上原 G−C 全收迫 G 全收，排除各五份。
- **不同 pairs 共用 h**：mixed-capable faces 是原 triangle (a,b,b_h)
  與排除 b_h 的四框點長 face。Triangle 同理排除，故 C 必在後者；
  actual S_C⊆B−{b_h}，共十份有序必要骨架。
- **不相交 pairs**：保留兩個原 mixed-capable faces，一個 boundary
  envelope 是相鄰 pair，一個是兩段框弧的三點集，共十份有序必要骨架。
  **短 face 也保留**；one-root／unary 短支援定理沒有直接提供四-hub
  的原 mixed joint 延拓，不能借任務 A 將它刪掉。

具名入口 W933-101／W941-139：原 a=5,b=6、S_a=01、S_b=23。
保留短 face 的精確原圈為
**a–b₁–b₂–b–a**，envelope={1,2}；長 face 為
**a–b₀–b₄–b₃–b–a**，envelope={0,4,3}。
q=01021 時式 (2) 的完整 literal pairs 正是 {(2,1),(2,3),(3,1)}。
兩個 face 均附原 rotations、所有原邊及完整 root-pair fibres，七種
contact 身份均保留。這些是**必要骨架見證**，不是含 C 的候選來源。
另一具名入口 W933-98／W941-135 的原 pairs 01／04，C 只能在
envelope={1,2,3,4} 的長 face；artifact 保存全部 20／20 原 indexes。

## 5. 任意大小 tightness 及原 leaf 身份限制

固定原拒絕 q。式 (2) 的**每一個**合法 root pair (A,D) 均必被唯一
原 C 阻擋；對原 v∈C 使用全部固定外鄰的 exact lists

\[
L_{A,D}(v)=U_4-\bigl(q(N_B(v))
 \cup(\{A\}\text{ if }v\in\{x_0,x_1\})
 \cup(\{D\}\text{ if }v\in\{y_0,y_1\})\bigr).\tag{6}
\]

完整 degree 四給 |L|≥deg_C；原 C 連通且拒絕，生成樹逆序貪婪
迫**所有點、所有合法 pairs 均 tight**。故每點全部固定外鄰色兩兩
不同，特别是實際 N_B(v) 對每個拒絕列 injective。兩 masks 的固定
拒絕列不容三點 injective，也各在某拒絕列重複每條框對角的色，故
N_B(v) 至多兩點，兩點時必是原框邊。

每個 A∈E_a 可配某 D∈E_b−{A}；因此 a-only contact 的實際框附件
滿足 q(N_B(v))⊆q(S_a)，b-only 對稱，共享 contact 在兩色集合交集。
這些条件對**同一實際附件集合**及全部拒絕列同時成立，再與原固定
face envelope 相交；不將每列容許附件各自拼成來源。

Checker 對每份保留 face 保存四種 owner 身份的全部 actual附件子集。
例如 W933-101／W941-139：短 face 內 a-only 可接 {1}、b-only 可接
{2}；長 face 內分別可接 {0}、{3}；共享 contact 在兩個 faces 都不能
接 boundary，原 deg_C=2。空附件允許。所有非contacts 可接的兩點
附件仍需是 envelope 內原框邊。

對共用 h 的長 face、及不相交 pairs 的短 face，必要表逐份給
**min deg_C≥2**；disjoint 的三點長 face 不一概如此，共享 contact
可能有一條框附件而成 leaf。保留原 933 pairs 04／12、長 envelope
{2,3,4} 的見證：共享 contact 可有 actual attachment {4}。

此外原拒絕 lists 使 C 是 Gallai tree；外部 B+a+b 原樣連通，沿用
[連通外部 K₄ 排除](c5_degree5_tree_components.md#1-連通外框排除-degree-4-分量的-k4)
可使用 bridges／odd cycles。這裡的外部連通只供 topology，沒有合併
原 relations。外部依賴為 [Dvořák Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)：
degree-list tightness 與 blockwise-uniform palettes；本輪核對其原文條件。

另一窄必要引理：**同一 leaf odd-cycle 的所有 private vertices 有同一
原 owner 身份。** 拒絕 singleton q 的缺色 d 不在 boundary 上；相鄰
spokes 使 E_a={d,h_a}、E_b={d,h_b}。比較兩個合法 literal pairs
(d,h_b)、(h_a,d)，exact lists 中「含 d」的兩位編碼為

| 原 owner 身份 | 缺色 membership 編碼 |
| --- | --- |
| 沒有 root owner | (1,1) |
| 僅 a | (0,1) |
| 僅 b | (1,0) |
| 共享 a,b | (0,0) |

同一 leaf block 的 private vertices 在每份 lists 有同一 block palette，
故編碼一致。每種 contact owner 身份最多兩點，因此帶 contact private
vertices 的 leaf odd-cycle 必是有兩個 private vertices 的 triangle。
這是必要 leaf 身份，不宣稱所有 leaf triangles 排除或原 C 已分類。

## 6. 固定完整圖控制與 marginal 負見證

[Checker](../scripts/c5_excess_two_mixed_core_four_spoke_mixed22.py)、
[joint helper](../scripts/c5_excess_two_four_spoke_mixed22_joint_controls.py)、
[artifact](../artifacts/c5_excess_two_mixed_core_four_spoke_mixed22/observations.json)
保存七身份、九份原 q-core 省略身份、全部原必要 indexes、face 與
actual 附件限制、條件式原 K₅、及完整四接點／六角色 witnesses。

28 張手列完整 degree 圖＝七身份×短／較長原 C×root 交換；兩 roots
各完整 degree 五、所有原 C 點完整 degree 四，固定原 spokes 01／23。
較長 C 是另一份原圖，沒有短長 relation 等價宣稱。全部十列原 R_C、
G、四個 G−e、G−C 與原 K 的關係都由原邊回溯獨立核對：
1,680 全圖 joins、26,880 pinned root-pair fibres（含空）、1,120
三接點 carrier joins／原 spoke 接回、840 root swaps、40,320 全域
S₄ witness controls 與 6,720 獨立重算的 S₄ 原 R_C。
這些圖**不宣稱 disk、Σ=933／941、Σ-critical 或來源實現**。

具名 marginal 負見證 control 20、Pstraight、q=01012、roots=(2,3)：
原 C 是 7–8，兩點皆有原 b₀ 附件；contacts=(7,8,7,8)。四個
marginals 都是 {1,2,3}，但完整 R_C 只含不同色 pairs 的六個四角色
tuples，沒有 tuple 同時避開兩 root 色。Spoke／ab guards 均成立，
完整 pinned fibre 為空；artifact 保存每個原 tuple 的整份 witness。

25 份不同骨架核對 2,320 rotation assignments、60 disk rotations。
相同 pair 因原框邊加入 K₄ 有四個 rotations，共點 unequal 有兩個，
不相交亦兩個；沒有強套前序 unary 骨架的 rotation 數字。
12,200 共同 D₅ root-pair controls 搬動整份 boundary／色框／pairs，
122 原 frame root swaps；任意大小 soundness 由紙面論證承擔。

## 7. 重播、停止點與下一窄入口

```bash
python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22.py --check
python3 scripts/c5_two_spoke_three_contacts.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
python3 tools/artifacts.py status
git diff --check
```

無參數只寫本層 observations；`--check` 重算逐 byte 比對。
既有 three-contact 完整 payload 與 three-hub payload 另重算相同，
前序 source artifact SHA256 綁定原 bytes；未覆寫其他來源 artifacts。
實際重播結果與未重跑範圍見本輪紀錄，`lake build` 不形式化本頁 topology。

**停止於 B 的七身份、四原 spoke 省略全收、原 G 自己 (5,5) q-core，
以及 20／20 保留骨架的原 face／tightness／leaf-owner 必要限制。**
下一個 B 的窄入口可固定 W933-101／W941-139、原短 face {1,2}，
從完整 C 的 Gallai leaf 與實際外部 paths 判定能否給原 K₅；或固定
933 的 04／12 長 face、共享 contact 實際附件 {4}，研究原 leaf bridge。
兩者均須保留七身份及完整 (a,b,x₀,x₁,y₀,y₁) fibre，不將必要表
視為 source catalogue。任務 A、其他 incidence／較少 spokes／多 mixed／
no-mixed／非相鄰 roots 仍各自保留；本輪未 commit／push。
