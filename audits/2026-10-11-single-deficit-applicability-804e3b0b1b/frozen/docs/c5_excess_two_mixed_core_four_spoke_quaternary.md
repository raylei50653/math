# ε=2 四-spoke (3,1)：原 mixed-(1,3) 四接點 leaf-slack 排除

**後續（2026-10-03）**：[四-spoke (2,2) 共用 pair 的 sealed mixed 排除](c5_excess_two_mixed_core_four_spoke_equal_pair.md)
已接續本頁的下一窄型：mixed-(1,1) 加各側一原 unary 的相同 spoke-pair
排除 7／9 份，含原 01／01；unequal pairs 尚有 40／66 份，整個子型未完成。
下文保留本頁當輪四接點結論及停止點，現況由 Kempe 導覽維護。

2026-10-03，接手基準 `b63a096`，保留前序未提交工作樹。接續
[mixed-(1,2) 原三接點身份](c5_excess_two_mixed_core_four_spoke_ternary.md)；
目前研究入口由 [Kempe 導覽](c5_kempe_guide.md)維護，實際驗證及貼用摘要見
[本輪紀錄](history/2026-10-03-excess-two-four-spoke-quaternary.md)。

**固定完整 Σ=933／941、下列相鄰唯一 mixed 來源前提下，四-spoke
(3,1)、mixed incidence-(1,3) 無 unary 的全部來源均不存在，含 root 交換。**
同色原 spoke 省略保留唯一原 K=C+a，四接點為 (a,y₀,y₁,y₂)。拒絕要求
K 禁掉 b 的三個可用色；marked leaf a 的完整 list 則迫禁色至多二。
指定原 012／2、q=01021 入口取 b=1，整份 K 可由原 spanning tree
逆序貪婪染色，接回同色原 spoke 後仍是 G 的完整延拓。

任意大小結論由本頁直接貪婪證明承擔；Python 證書核對具名必要框架及
完整原 relations／witnesses。新反證不需要 q-minimality、Gallai 分類或
四接點 K₅ 定理。**共同 ε≥2 不變，ε≥3 未證，未新增 Lean theorem。**

## 1. 同一原來源與原四接點身份

沿用前序來源前提：G 有限簡單，B=(b₀,…,b₄) 為指定有序 induced-C₅
disk 外框；完整 Σ 是 933、941 或其整圖 D₅ 像，刪每條非框邊均嚴格
擴大 Σ。有效內部 H 非空連通，恰兩個完整 degree-5 roots a,b，原 ab
存在，其餘有效內點完整 degree 四。H−{a,b} **恰為唯一原連通 C**，
沒有 unary，原 incidence 為 (1,3)：

- a 的三條原 spokes 接到 S_a；另有 ab 及 ax。
- b 的一條原 spoke 接到 b_s；另有 ba 及 by₀,by₁,by₂。
- y₀,y₁,y₂ 互異；x 可等於其中任一點，也可不同。

保留任意大小的原 C、所有原內邊／bridges、實際 boundary 附件及 supports、
有序 contacts、ownership、原嵌入環序及同一字面四色框。不為各 contact
獨立換色，不把原 C 的四點 relation 換成 marginals。

選一條原 e=ab_j，其中同一拒絕列 q 滿足 j∈S_a，且有 k∈S_a−{j}
使 q_j=q_k。令 M=G−e。原 ab_k 已施加被省略 e 的完整限制，故

\[
\operatorname{Col}_q(M)=\operatorname{Col}_q(G). \tag{1}
\]

M−b 恰為 **K=C∪{a}**，a 經原 ax 接到整份 C；a 是 K 的 leaf，
deg_K(a)=1，保留兩條原 boundary spokes。b 的四條 contact edges
仍是原 ba、by₀、by₁、by₂，因此 K 的四個原 contacts 恰為
(a,y₀,y₁,y₂)，互不相同，即使 x 與 yᵢ 共享亦不改變這個身份。

原 proper-q-core 的 incidence audit 只有「保留 M」或「再省略原 b-spoke」
能保持兩 roots degree≥4；原 C 的 (1,3) incidence 不能省略。後者是
前序排除的 (4,4) 身份。這份 audit 保存在證書，但本頁直接證 M 可染，
**不需要先把 M 認成 minimal q-core**；也不從 G 的完整 Σ-minimality
推 G 對 q minimal。

## 2. 完整原 relation 與精確 leaf 接回

令 U={0,1,2,3}，R_C(q) 是原有序 (x,y₀,y₁,y₂) 的完整 relation；
每份 tuple 來自同一原 C 的全部內點染色及實際附件。共享 x=yᵢ 時
兩個座標必相等，並非兩個頂點。

設 T=S_a−{j}、A_a=U−q(T)、A_b=U−{q_s}。M 的完整六座標 joint 為

\[
J_M(q)=\{(d,h,c,t_0,t_1,t_2):
(c,t_0,t_1,t_2)\in R_C(q),\ h\in A_a,\ h\ne c,\
d\in A_b,\ d\notin\{h,t_0,t_1,t_2\}\}. \tag{2}
\]

G 的 joint 只在同一份式 (2) 上加回 h≠q_j。K 的完整四接點 relation 是

\[
R_K(q)=\{(h,t_0,t_1,t_2):\exists c,
(c,t_0,t_1,t_2)\in R_C(q),\ h\in A_a,\ h\ne c\}. \tag{3}
\]

存在量詞由同一原 C 的整份 coloring witness 承擔。只有在式 (3) 的
全部 tuples 建立後，才定義其完整 forbidden-color set

\[
F_K(q)=\{d\in U:\forall t\in R_K(q),\ d\text{ 出現在 }t\}.
\]

故 M 接受 q iff A_b−F_K≠∅；若拒絕，必 A_b⊆F_K，要求至少三禁色。
不是逐接點取禁色後相加，也沒有另一份 unary 可補足 cover。

## 3. 原 connected K 的 constructive slack 引理

同色省略使 q(T)=q(S_a)。三個 C₅ 框點不能同色；而被省略色已有重複，
故兩條保留 spokes 恰看到兩色，|A_a|=2，|A_b|=3。

任取 d∈q(T)。固定 b=d 及原 boundary q，對 K 中每個原頂點 v 使用
**所有原固定鄰點**得到 exact list

\[
L_d(v)=U-\{q_i:b_i\in N_M(v)\}
       -\bigl(\{d\}\text{ 若 }v\in\{a,y_0,y_1,y_2\}\bigr). \tag{4}
\]

對 v∈C，其在原 G 的 degree 四，離開 K 的邊只有實際 boundary 邊，
以及 v=yᵢ 時的一條原 bv。因此除去不同固定顏色的數目不超過這些邊數，
始終 |L_d(v)|≥deg_K(v)，包括 x=yᵢ 的情形。
對 marked a，d 已在保留 spoke 色集 q(T) 中，故

\[
L_d(a)=A_a,\quad |L_d(a)|=2>1=\deg_K(a). \tag{5}
\]

取整份原連通 K 的 spanning tree，以 a 為根，按 tree depth 由大至小
染色。每個非根點染色時，原 parent 還未染，因此已染鄰點至多
deg_K(v)−1；式 (4) 留至少一色。最後根 a 的式 (5) 留至少一色。
所有非 tree 原邊亦納入每次已染鄰點檢查，旁支、環及長 bridges 都保留。
這直接給整份原 K 的合法 list coloring，故 d∉F_K。

因此在這些同色省略 queries 上

\[
F_K\subseteq U-q(T)=A_a,\qquad |F_K|\le2<3=|A_b|. \tag{6}
\]

更直接地，q(T) 的兩色至少有一色 d≠q_s；取此 d 即是合法 b 色。
式 (4)–(5) 的整份 K coloring 接上 b，得到 M 的全染色，再由式 (1)
得到 G 的全染色，與「同一 q 被 G 拒絕」矛盾。

指定 S_a=012、s=2、q=01021、j=0／2 時，A_a={2,3}、A_b={1,2,3}；
取 **b=1**，a 的 exact list={2,3}，即得到這份 constructive contradiction。
只用兩條保留 spokes，沒有將 contact marginals 當作延拓 witness。

此引理對任意大小連通 K 成立，沒有 embedding、T4、degree-list 文獻
或 minor oracle 依賴。將它用於全部目標來源仍需前序具名框架覆蓋；
有限控制不承擔任意大小的證明。

## 4. 具名必要域與完整圖證書

沿用 [原單 spoke 必要框架](c5_excess_two_mixed_core_single_spoke.md)，
以相同原 roots／boundary 身份抽出所有 (3,1) 及 root 交換框架。
[Checker](../scripts/c5_excess_two_mixed_core_four_spoke_quaternary.py)／
[joint helper](../scripts/c5_excess_two_four_spoke_quaternary_joint_controls.py)／
[artifact](../artifacts/c5_excess_two_mixed_core_four_spoke_quaternary/observations.json)
保存原邊、來源 index、原 skeleton 的 apex rotation、完整 incidence 與 queries：

| 目標 | 原具名框架 | 同色原 spoke／拒絕列 queries | leaf-slack 矛盾 | 未排框架 |
| --- | ---: | ---: | ---: | ---: |
| 933 | 20 | 40 | 40 | **0** |
| 941 | 60 | 160 | 160 | **0** |

每份框架都有至少一份這種 query，故足以排除同一原來源。另核對
80 個 root 交換框架、2,000 次整體 D₅ query 搬運；必要 skeleton 的
rotation 不冒充完整原來源的 disk embedding，實際原嵌入仍由紙面保留。

另有 **80 張完整 degree 圖**：八種原 C 形狀×五份附件選擇×root 交換。
包含 x 分別共享 y₀／y₁／y₂、不同接點 star／cycle、triangle 旁支及
長 path，全部附件由每點原 degree 四逐點核對。保存全部十列、原 C
四點 relation、原 G／省略 a0／a2 的六點 joints、K 四點 relation，
每份 tuple 均保存整份 coloring witness，並保存所有固定 (b,a) 的纖維。

2,400 次完整 joint、2,400 次完整 K relation 與獨立全圖回溯相等；
38,400 份 pinned 纖維、480 次同色省略等式全部核對。另保存 **2,400
份 spanning-tree 貪婪延拓**：exact lists、degree、parent、逆序順序及
整份 G／M coloring 均驗證實際原邊，並核對 witness 存在於完整 joint。
保留一份四點 marginals 假允許、完整 guarded fibre 為空的反例。

這些完整 degree 圖只核對關係身份／constructive extension，不宣稱
disk、Σ=933／941 或 Σ-critical。原 G 在某些其他列的三條 spokes
看到三色時，a 可能無 slack；式 (6) 不套那些列，helper 亦明確分開。

## 5. 重播與證據邊界

```bash
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_quaternary.py --check
python3 scripts/c5_excess_two_mixed_core_four_spoke_quaternary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_ternary.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
python3 tools/artifacts.py status
git diff --check
```

無參數只寫新層，`--check` 重算逐 byte 比對；大型 observations 留本地，
MANIFEST／generated ignore 保存 digest 及 producer。實際執行、數字及
未重跑範圍見本輪紀錄。前序原 single-spoke 歷史 byte-check 的三份 docs
hash 漂移仍明存；沿用前輪完整數學 payload 相等的唯讀 audit，本輪不
再次宣稱該舊 byte-check 通過，也不覆寫舊產物。`lake build` 不形式化
本頁的原 connected-list 染色證明。

## 6. (3,1) 全 incidence 分拆與停止點

a 的原三 spokes、ab 與唯一 mixed 已用滿 degree 五，故原 mixed
a-incidence 必一、a 側沒有 unary。b 的 spoke 與 ab 用兩 incidence，
餘額三必且只能分成下列四份身份：

| 原 mixed incidence | 原 b-unary 分拆 | 完成報告 |
| --- | --- | --- |
| (1,1) | (1,1) | [兩原 unary 六跨度](c5_excess_two_mixed_core_four_spoke_singles.md) |
| (1,1) | (2) | [原 binary 同列端點 hub](c5_excess_two_mixed_core_four_spoke_hubs.md) |
| (1,2) | (1) | [原三接點身份](c5_excess_two_mixed_core_four_spoke_ternary.md) |
| (1,3) | 空 | 本頁原四接點 leaf-slack |

因此結合各頁相同來源前提，**相鄰唯一 mixed 的四-spoke (3,1) 全部
原 incidence 分拆已排除，含 root 交換**。不是一般四-spoke 全排。

**停止於 mixed-(1,3) 無 unary 的原四接點任意大小排除，以及上述
(3,1) incidence 完備身份。** 本輪不 commit／push。下一窄入口是
四-spoke (2,2) 的 mixed-(1,1) 加各側一原單接點 unary：先保留同一
R_C(x,y)、R_U(u)、R_V(v)、全部實際附件／支持及完整
(a,b,x,y,u,v) joint，固定原必要框架 a=5、b=6、兩側 spokes=01，
分清 x=y 與 x≠y；尚未分析或排除該型。其他 (2,2) incidence、較少
spokes、原 unary 單省略、原 (5,5) q-core、多 mixed、no-mixed、非相鄰
roots 與 unary 側例外仍保留。ε≥3、一般出口、來源實現及 K∞=K≤5 未證。
