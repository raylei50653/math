# ε=2 四-spoke (2,2)：mixed-(1,2)+a-unary 的 01／23 來源排除

**獨立驗收（2026-10-04，D₅）**：[最終成果固定快照與稽核](../audits/2026-10-04-task-d5/REPORT.md)
核對原04／04及root交換、四rotations、actual C/U支援、完整三hub前提，
整份C替換逐點保持全部外部，只主張(a,b,u)投影等式；六角色joint不等
反例與01202 singleton1／3保持。逐身份ledger為16／20、40／58支援、
50／84schedules；原A至A₃正文／artifacts及各輪數字保持當輪語境。
未用D₅來源搬運，其他mixed12身份／ε≥3未證；現行入口由Kempe導覽維護。

**獨立驗收（2026-10-04，D₄）**：[正式返回工作區稽核](../audits/2026-10-04-task-d4/REPORT.md)
已核對A₃四rotations、原三hub與完整C替換；最新ledger為18／22。
本頁A當輪22／26及原artifact保持，(a,b,u)投影與六角色joint分開。

**後續（2026-10-04，A₃）**：[共用01／01報告](c5_excess_two_mixed_core_four_spoke_mixed12_01_01.md)
在A₂之後排除原01／01及root交換；目前保存18／22具名框架，原完整
artifacts與各輪必要域保持。其他mixed12身份與ε≥3仍未證。

**後續（2026-10-04，A₂）**：[原 01／12 長／短 face 報告](c5_excess_two_mixed_core_four_spoke_mixed12_01_12.md)
已排本頁 §7 的下一具名入口，含 root 交換；原 U 的 actual 2 crosscut
封長 C 至 {2}，短 C 只碰 {1}，拒絕列 01202 的完整 joint 給矛盾。
本頁 22／26 是 A 當輪必要域；A₂ 保存其餘 20／24。原正文與
artifact 保留，不表示完成 mixed-(1,2) 整型或證明 ε≥3。

2026-10-04，接續 [mixed-(1,1) 子型完成報告 §6](c5_excess_two_mixed_core_four_spoke_disjoint_pairs.md#6-重播停止點與下一incidence)
及 [Kempe 導覽](c5_kempe_guide.md)。保留接手時的未提交成果；本輪
沒有 commit／push。實際驗證及貼用摘要見 [研究紀錄](history/2026-10-04-excess-two-four-spoke-mixed12.md)。

**原 a=5、b=6、spokes=01／23、mixed incidence=(1,2)、a 側一原
單接點 unary 的來源不存在，含 root 交換。** 先核對原 unary crosscut
與省略圖身份，再以同一原 unary 的完整 relation 及未用色守恆完成排除。
新 incidence 自己的必要域有 70／90 份具名框架；同一 unary screen
排除 48／64，保留 **22／26** 份及全部實際支援／relation 條件。
這不是 mixed-(1,2) 的完整分類；**ε≥3 未證，未新增 Lean theorem**。

## 1. 原來源、完整 ternary 與六角色 joint

G 有限簡單，指定有序 induced-C₅ B=(b₀,…,b₄) 是 disk 外框。
固定完整 Σ=933／941 或整圖 D₅ 像，每條非框邊 Σ-critical。
有效 H 連通、ε=2，恰兩個相鄰完整 degree-5 roots a,b；原 ab 存在，
其餘有效內點完整 degree 四。H−{a,b} 恰有原 mixed C 及原 unary U。
兩側各兩條原 spokes；C 的原接線是 ax、by₀、by₁，U 的原接線是 au。
y₀≠y₁，允許 x=y₀ 或 x=y₁，始終是同一原頂點；u∈U 與 C 互異。

全部原內邊、actual attachments／supports、bridges、旁支、ownership、
嵌入環序及同一字面四色框保持。令原完整 relations 為
R_C(β;x,y₀,y₁)、R_U(β;u)，A_r(β)=U₄−β(S_r)。精確接合為

\[
J_G(β)=\{(A,D,X,Y_0,Y_1,T):
(X,Y_0,Y_1)\in R_C(β),\ T\in R_U(β),\
A\in A_a(β),\ D\in A_b(β),\
A\ne D,X,T,\ D\ne Y_0,Y_1\}. \tag{1}
\]

每份 tuple 都有原 C、U 的整份 coloring witnesses；固定同一 β、
同一 roots 後才接合。共享 x 的座標必同色，不能複製成自由接點。
保存每個字面 (A,D) 的完整纖維，包含空纖維；不將 C 的 marginals 相乘。
省略原 spoke 只放寬該原 boundary guard，接回仍在同一 tuple 過濾。

## 2. 原省略圖的 minimal-core 身份與 ternary 銜接

沿用 [原省略身份表](c5_excess_two_mixed_core_spokes.md#2-全部-proper-core-的具名省略表)
及 [單 spoke minimality](c5_excess_two_mixed_core_single_spoke.md#1-同一原-g-與省略圖自己的-minimality)：
原刪 a、刪 b、刪 ab 圖全收，且相鄰唯一 mixed 的原 (4,4)
rejected-row cores 已全排。這裡不把 G 的 Σ-minimality當作 q-minimality。

省略任一原 a-spoke e，令 M=G−e。若 M 拒絕 q，取包含 B 的
minimal q-core L。前序全收迫 L 含 a,b,ab；原 degree-4 飽和使
C、U 只能整份保留或整份省略。a 在 M 已 degree 四，不能再失去
任何原 incidence；C、U 都保留。b 若再降四便是已排的原 (4,4)
身份，故 b 保持五且 L=M。

**M−b 是單一連通分量 K=C+a+U**，原三接點是 (a,y₀,y₁)，
deg_K(a)=2，a 保留一條原 boundary spoke。它不是舊
[(3,1) ternary 報告](c5_excess_two_mixed_core_four_spoke_ternary.md)
的「C+a 加獨立 U」。本次 b 有兩條原 spokes；[two-spoke 三接點定理](c5_two_spoke_three_contacts.md#5-second-rows-scope-and-remaining-cases)
直接排除這份 M：同一 K 的兩個禁色迫 active triangle、三條原
bridge arms 及三條 actual boundary tethers，與 b、B 給原圖 K₅ minor。
無界 arms／旁支由既有紙面證明承擔，沒有從有限 skeleton 外推。
因此對任一 a-spoke，**Σ(G−e)=Ω**。

另令 **N=G−U**，省略整份原 unary 及其 incident 邊。N 的 root
degrees 是 (4,5)；相同飽和與原 (4,4) 排除迫任何拒絕 core 正是 N。
這次 N−b=C+a，contacts 仍為 (a,y₀,y₁)，deg(a)=1；同一
two-spoke 三接點定理給 **Σ(N)=Ω**。三個 contacts 互異，即使
x=y₀／y₁ 也不受影響。

原 U 去掉 au 後的 contact list 有 slack，逆序生成樹貪婪法給
R_U(β)≠∅。因此 **Σ(G−au)=Ω** 亦成立。但 G−au 中 u 的 degree
降三，**不能稱 G−au 自己為 minimal q-core**；上述身份是整份 U
省略圖 N 的身份。

對 b-spoke 省略，若拒絕則省略圖自己以 a 為唯一 degree-5 minimal
core。刪 a 後保留 L=C+b、U，分拆 (2,1)，L contacts=(x,b)，
deg_L(b)=2。此身份本輪只保存，不宣稱其全收。

## 3. 全收 N 與完整 joint 迫同一原 unary 是 singleton

記 T_N(β) 為原 N 的完整五角色 (a,b,x,y₀,y₁) relation，每份 tuple
附整份 N witness。精確式子是

\[
J_{G-au}(β)=\{(t,T):t\in T_N(β),\ T\in R_U(β)\},\qquad
J_G(β)=\{(t,T)\in J_{G-au}(β):t_a\ne T\}. \tag{2}
\]

先保持完整 C ternary 及 T_N，再取其 a 色域 P_N(β)。兩個域都
非空。若原 G 拒絕 β，式 (2) 迫每對 (A,T) 都相等，故

\[
\boxed{P_N(β)=R_U(β)=\{d_β\},\qquad d_β\in A_a(β).} \tag{3}
\]

這是整個原 U relation 及所有原 N witnesses 的必要結論，不是逐列
任選 endpoint 禁色。兩個 masks 的每個原拒絕列都必滿足式 (3)。
同色 a-spokes 在某拒絕列上會使 a-spoke 省略仍拒絕，與 §2 矛盾。
固定 933／941 的十份原 pair 逐列核對，a 的兩 spokes 因而必為
五條原框邊之一；這是新 incidence 的必要限制。

## 4. 原 01／23 的 actual unary crosscut 與 C 支援

固定 a=5、b=6、S_a=01、S_b=23。原骨架的四個 faces 為

| 原 face | 原框包絡 |
| --- | --- |
| 0–a–1–0 | {0,1} |
| a–1–2–b–a | {1,2} |
| 2–3–b–2 | {2,3} |
| a–0–4–3–b–a | {0,3,4} |

U 的兩個短 incident faces 有原外路徑 a–b–3 或 a–0，終點在
相應 pair 外、內部避開 U。由 [短支援引理](c5_short_support_singleton.md#1-原圖完整接點-relation-與外部路徑)，
在這些 faces 中 au 非 critical。故 critical au 迫 U 在長 face
F=(a,0,4,3,b)，且 actual N_B(U) 必含 0、3：不含任何一端的
支援都包含於 04 或 34，仍有原外路徑 a–b–2 或 a–1。
因此實際支援只有 **{0,3}、{0,3,4}**。

原 au、U 的連通性及實際 3 附件給
P:a–u↝z–3，內點全部在同一原 U。若 C 也在 F，任一 by_j 接線
迫整份 C 在 P 的 b-side；否則原 b–y_j↝C 附件路徑與 P 的 endpoints
沿 F 交錯。因而 **N_B(C)⊆{3}**。另一個共同 face 為 (a,1,2,b)，
允許 C 的實際支援包含於 {1,2}。不能把兩份 face 的包絡相加，
也不能每列重新選 C 的位置。

長 face 的封單點 C 還可獨立排除。固定任一合法 C 外 coloring，
外鄰色只有 A,D,t=β₃，原 ab、b3 給 A≠D、D≠t。若拒絕，原
degree 四給 exact degree lists，connected slack-list 引理迫處處 tight。
Degree-list 刻畫給原 C 是 Gallai tree；原 B∪{a,b} 連通，沿用
[crosscut 報告 §3 的 connected-exterior K₄ 排除](c5_excess_two_mixed_core_four_spoke_crosscut.md#3-同一原外路徑保-degree-的二三-hubs)，
以四條原外方向及連通外部 bag 給 K₅，故拒絕時 C 必 K₄-free。
當 A≠t，原 P、ab、b3 提供互異三 hubs，沿用
[三-hub Gallai 引理](c5_short_support_singleton.md#4-三-hub-引理排除未見色接點數不設上限)。
當 A=t，tightness 先禁止 C 的同一點同接 a、3，再合併原 P 的兩端，
degree 與 lists 才保持，沿用 [兩-hub 引理](c5_short_support_singleton.md#3-兩-hub-gallai-引理五個-branch-sets)。
b 的兩條 contact 邊分別接不同 C 點，仍是同一原 b hub，沒有合併
y₀,y₁。兩種情況均得原 K₅ 反證。

因此只替換完整 C witness 即能恢復原 ax，C 外逐點固定，精確式子
為 π_(a,b,u)J_G=π_(a,b,u)J_(G−ax)，使固定 ax 非 critical。
**不主張完整六角色 joints 相等**。這個原圖拓撲收縮不是 relation factor，
不需 Σ(G−C)=Ω；短 face C 暫仍保留。下一節再排整份具名入口。

## 5. 同一原 U 的三列 relation 矛盾，完成具名來源排除

兩 masks 共同拒絕 q₃=01021、q₁=01202、q₀=01212。a 的原
spokes 01 在三列都見色 0、1，故式 (3) 中 d_i∈{2,3}。
U 的 actual support 包含於 034，全部原 U witnesses 的換色給：

| 同一原列／搬運 | 完整 R_U 的必要結論 |
| --- | --- |
| q₁ 在 034 見 0、0、2；π=(1 3) 固定全部實際附件色 | singleton 必被 π 固定，故 R_U(q₁)={2} |
| q₀ 在 034 見 0、1、2，q₃ 見 0、2、1；π=(1 2) 同時搬動整份 U | R_U(q₃)=πR_U(q₀)；兩者都在 {2,3}，故都為 {3} |

這些映射在支援為 03 或 034 時均成立；不能只用 envelope 假造實際
附件。對 03 還有更強 stabilizer 衝突，證書一併保存。

上述三份 singleton 不可能來自同一原 unary。固定唯一 contact u，
R_U(q_i)={d_i} 意味固定 owner 色 d_i 後，原 U 的 degree lists
不可染；每點完整 degree 四使它們至少為 deg_U，拒絕迫 tight。
沿用 [單接點固定色引理](c5_single_spoke_root_conservation.md#2-單接點固定色引理)：
同一 block tree 的兩份拒絕 palettes，若非 contact 點的固定色 membership
相同，root membership 亦相同。這是向 u 的 block-tree 歸納，容許
任意大小、分叉、bridge 與 Gallai clique blocks，不需新的 K₄ 排除。
每個 q_i 都未使用色 3，所有 v≠u 的 list 始終含 3；在 q₁ 禁 2
時 u 的 list 含 3，而在 q₀／q₃ 禁 3 時不含，矛盾。

所以 **01／23 的整份原來源排除，含 root 交換**，並非只給指定列
出口；原 C 位於短或長共同 face、三種 x 身份均涵蓋。
外部 degree-list 依賴為 [Dvořák，Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，
本輪核對其 degree-assignment／tightness／block-palette 前提。紙面任意
大小推導與下面 Python 固定域分開，未形式化此拓撲或 palette 論證。

## 6. 新 incidence 的完整具名必要域與保留殘留

[Checker](../scripts/c5_excess_two_mixed_core_four_spoke_mixed12.py)、
[unary helper](../scripts/c5_excess_two_four_spoke_mixed12_unary_controls.py)、
[joint helper](../scripts/c5_excess_two_four_spoke_mixed12_joint_controls.py) 及
[artifact](../artifacts/c5_excess_two_mixed_core_four_spoke_mixed12/observations.json)
重新指定 C incidence=(1,2)、U-at-a，從 §3 的五份 a-pairs 與
原單 spoke minimal-core 的 b-pair 必要限制構造自己的具名 ledger。
b-pairs 為 933 的 01,02,04,12,13,23,34；941 另有 03,14。
只核對前序 **通用單 spoke 骨架**的原邊與身份，沒有讀取 mixed-(1,1)
完成表作新 incidence 分類。

每份骨架窮盡全部 rotations，保留所有不同原 face 及 actual support
子集；共用 pair 的四份 disk rotations 沒有套用 unequal 的兩份 assert。
每份 U placement 明列支持它的原 rotation indices，以及在同一 rotation
中相容的 C common faces；root 交換核對原 U／C faces、支援與 relations
的具名 bijection，不把不同 embeddings 的 placements 自由拼接。
短支援沿用原外路徑；若共用 pair 的骨架沒有 pair 外 spoke，完整
來源碰齊五框點迫原 C 有 pair 外 actual attachment，原 a–x↝C–h
提供避開 U 的外路徑，證書明分這個紙面存在路徑與骨架內具名路徑。

在每個非短 actual support 上，逐一保存式 (3) 的完整 singleton
R_U schedules、所有 S₄ covariance／stabilizer 約束、明示衝突列與
色置換，並加上固定未用色 3 的 membership 守恆。不同 face 中的
同一 support 仍保留各自原位置身份，不合併成匿名 schedule。

| 新 incidence 必要域，含 root 交換 | 933 | 941 |
| --- | ---: | ---: |
| 具名框架 | 70 | 90 |
| unary 完整 relation／短支援排除 | 48 | 64 |
| **保留框架** | **22** | **26** |
| 保留原 face／actual-U-support 身份 | 56 | 92 |
| 保留完整 singleton relation schedules | 72 | 130 |

以下每行保留 a=5,b=6 及 a=6,b=5 兩種原 root 身份：

| a-spokes／b-spokes | 933 | 941 |
| --- | --- | --- |
| 01／01 | 保留 | 保留 |
| 01／12 | 保留 | 保留 |
| 04／04 | 保留 | 保留 |
| 04／34 | 保留 | 保留 |
| 12／01 | 保留 | 保留 |
| 12／12 | 保留 | 保留 |
| 12／23 | 保留 | 保留 |
| 23／12 | 保留 | 保留 |
| 23／23 | 保留 | 保留 |
| 34／04 | 保留 | 保留 |
| 34／34 | 保留 | 保留 |
| 01／04 | 此 screen 已排 | 保留 |
| 04／01 | 此 screen 已排 | 保留 |

這是本輪 screen 的必要放寬，不宣稱每份通過全部 C 幾何、完整 joint、
criticality 或來源實現。每份殘留保留原 C 的共同 faces、完整 ternary
介面、三種 x 身份、全部 U placements／relations 及原省略身份。
不以這張新表宣稱完成整個 mixed-(1,2) 子型。

72 張手建完整 degree 圖保存原 C／U 的所有接線與附件路徑、x 不共享
及共享 y₀／y₁、原與省略圖的全部十列 relations、整份 witnesses 及
空／非空 fibres。獨立全圖回溯核對完整 joint、G−U 五角色 relation、
G−au 的精確乘積、四條原 spoke 接回，並分別核對兩種 K ternary
及 b-spoke 省略的 L binary。這些控制圖完整 Σ 是 1023／959，
不宣稱 disk、Σ-critical 或候選實現；long-C 的投影等式與六角色
不相等負控制分開保存。225 非空域的完整 guard 算子核對式 (3)。

## 7. 重播、停止點與下一入口

```bash
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed12.py --check
python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed12.py --check
python3 scripts/c5_excess_two_four_spoke_mixed12_joint_controls.py --check
python3 scripts/c5_excess_two_four_spoke_mixed12_unary_controls.py --check
python3 scripts/c5_two_spoke_three_contacts.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
python3 tools/artifacts.py status
git diff --check
```

無參數只生成新 observations；主 checker 的 `--check` 唯讀逐 byte 比對。
兩份 helpers 的 `--check` 直接重算固定 controls，不寫原 artifacts。
實際重跑及沿用範圍見研究紀錄，歷史文件 hash 漂移不由本輪覆寫。

**停止於 01／23 整份來源排除及新必要域的 22／26 具名殘留。**
下一窄題可固定仍保留的 01／12 與 root 交換，保持原 U actual support
及完整 singleton relation，核對 C 的固定共同 face 與
R_C(x,y₀,y₁)，再接式 (1) 的原六角色 joint。共用 pair 及其餘殘留
也原樣保存，沒有繼續擴張分類；目前優先序由 Kempe 導覽維護。
Mixed-(2,2) 無 unary、較少 spokes、單省略、原 (5,5) q-core、
多 mixed／no-mixed／非相鄰 roots 及 unary 側例外仍保留。
一般出口、來源實現、ε≥3、Lean 拓撲定理及 K∞=K≤5 均未證。
