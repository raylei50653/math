# ε=2：t=2、(2,2) 的同一原首橋與整型排除

2026-10-03。**933／941 固定完整 Σ、edge-minimal induced-C₅ disk
來源，在 ε=2、唯一 degree-6 root、t=2 下，不可能有原接點分拆
`(2,2)`。** 兩份原 binary 的實際支援落在同一對原 spoke 扇區；
40 份具名包絡乘十個目標，共 400 份必要查詢全部無解。

本輪直接復用 t=1 的[原路徑支援 helper](c5_excess_two_ternary_binary.md#4-同一原-binary-路徑塊的跨列支援)、
[singleton 首橋](c5_single_spoke_first_bridge.md)及
[局部 residual](c5_single_spoke_residual_locality.md)。只用 pair 列仍有
20 份具名必要 profiles；加入 singleton 列在**同一原首橋兩端**的
共同局部 residual 才全排除。沒有把 binary 的 singleton 禁色當作
每個路徑袋的 residual，也沒有跨不同列共用一個 β。

任意大小涵蓋由紙面 Gallai／原 bridge 路徑／原圖 K₅ 論證負責；
Python 核對固定必要域與完整五接點接合。無來源圖枚舉、disk
實現宣稱或新 Lean theorem。既有省略結果見
[兩 binary 省略](c5_excess_two_two_binary.md)及
[雙 spoke 省略](c5_excess_two_double_spoke.md)，現況見
[Kempe 導覽](c5_kempe_guide.md)。

## 1. 同一原來源與完整五接點接合

G 有限簡單，B=(b₀,…,b₄) 是指定有序 induced-C₅ disk 外框。
完整 Σ 为 933、941 或整圖 D₅ 像；每條非框邊 e 皆有
Σ(G−e)⊋Σ(G)。有效內部 H 連通，唯一 root r 完整 degree 六，
其餘內點完整 degree 四。兩條原 spokes 是 rb_s、rb_t，s<t；
H−r 恰有兩份原連通分量 A、C，各有兩個不同原有序接點
(x,y)、(u,v)。全部原邊、附件、ownership、環序及嵌入保留。

對 proper boundary row b，原完整有序 relations R_A(b;x,y)、
R_C(b;u,v) 都由接點 slack 的生成樹貪婪法非空。原完整接合是

\[
\mathcal R_G(b)=\{(a,c,d,e,f):(c,d)\in R_A(b),\ (e,f)\in R_C(b),
\quad a\notin\{b_s,b_t,c,d,e,f\}\}.\tag{1}
\]

令 F_A(b)=∩_{z∈R_A(b)}set(z)，F_C 同理。容量均至多二，式 (1)
的精確 root 投影為

\[
U_4\setminus(\{b_s,b_t\}\cup F_A(b)\cup F_C(b)).\tag{2}
\]

F 只用於原 root 接合查詢；兩個完整 ordered relations 始終是
聯合 tuples，不拆成 marginals。所有列及分量共用字面色框。

既有兩份 original binary 省略全收及雙 spoke 省略全收，對每列給

\[
\{b_s,b_t\}\cup F_A(b)\ne U_4,\qquad
\{b_s,b_t\}\cup F_C(b)\ne U_4,\qquad
F_A(b)\cup F_C(b)\ne U_4.\tag{3}
\]

本輪保留這三份具名原省略身份，未把沒有全 degree-4 真子核心
直接當作整型排除。

## 2. 兩原扇區中的 40 份共同包絡

完整 Σ edge-minimality 使每份原分量在某列有私有禁色見證：
若一個分量在所有列都不禁 root 色，刪其任一 root-contact 邊也
不會改變 Σ，矛盾。G 碰齊五個框點，故若分量支援包含於相鄰
框點 {a,b}，總有避開它的原 r–h 路徑，h∉{a,b}。
[短支援引理](c5_short_support_singleton.md)遂使該分量在每列
F 都空，與私有見證矛盾。因此兩份共同支援包絡跨度均至少二。

兩條原 spokes 把 disk 分成兩個閉扇區，其框弧長度合計五。
每份原分量连通、避開 r 與 spokes，故完全位於一個扇區。
只為證明位置限制，刪每份 binary 的一條 root 邊後，收縮該
原分量成一點；[共同 root 相容 lifts](c5_independent_support_capacity.md#42-同一-root-的相容-lifts)
給同區內包絡的開框邊段互斥，允許共用端點。**兩端點取同一
原嵌入的第一與最後實際附件**；包絡內部只是容許位置，並非
新增附件。relations 仍在原圖上計算。

- 相鄰 spokes：扇區長度為一與四。短區放不下任何分量；長區
  必有兩份跨度二的包絡，各占前後兩段，兩種具名 ownership。
- 不相鄰 spokes：扇區長度為二與三。兩分量不能共處同區，故
  各區一份。短區包絡唯一；長區可取前兩段、後兩段或全部三段，
  再交換兩份原分量，共六種具名配置。

五對相鄰、五對不相鄰 spokes 因而共 5×2+5×6=40 份配置。
每份包絡、扇區、原分量及接點身份固定後，才處理全部十列。

## 3. Pair 列的同一原路徑與局部 residual

對某份原 binary W，任一列 p 若 |F_W(p)|=2，兩個被禁 root 色
給兩份不可染的 degree lists。[外部 degree-list 刻畫](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
（本輪核對 Lemma 7／Theorem 10）給 tightness 及 Gallai block
palettes。B∪{r} 由原 spokes 連通，既有 K₄-block 排除適用，
所以 blocks 只有 bridges 與 odd cycles。

[二接點 pair 化約](c5_single_spoke_two_two.md#雙禁色的同圖奇數-bridge-路徑)
給兩原接點間的奇數長 bridge 路徑 P=(x₀,…,x_ℓ)，ℓ≥1。
這是原圖唯一的接點路徑，全部 pair 列共用同一 P。刪全部 P 邊
後，W_j 是包含 x_j 與全部旁支的原連通袋，彼此不交；T_j 是
其全部實際 boundary 支援，包含 x_j 的直接附件。

对任何已存在的拒絕證書，記

\[
D_j^q=q(N_B(x_j)),\quad Q_j^q=\text{全部路徑外 block palettes 的聯集},
\quad E_j^q=U_4\setminus(D_j^q\cup Q_j^q).\tag{4}
\]

这里 E 尚未扣 root 色，是局部 residual；在 pair 列 p，兩份
拒絕證書迫每個 j 都有 E_j^p=F_W(p)。在 singleton 列不作此等同。

旁支非 root 點不含另一接點，也沒有 r 邊。由葉 block 向袋 root
歸納，其 lists 唯一決定路徑外 palettes；直接附件則決定 D。
因此，不論兩列整分量 F 是 pair 或 singleton，只要各自拒絕
證書存在，便有

\[
q'|_{T_j}=\pi\circ q|_{T_j}\quad\Longrightarrow\quad
E_j^{q'}=\pi E_j^q.\tag{5}
\]

這是[局部 residual 相同列引理](c5_single_spoke_residual_locality.md#2-同一路徑塊的相同列引理)
在全域色置換下的同一歸納；不要求 root 的完整 list 相同，
也不要求 π 固定 r 色。逐点固定 q(T_j) 的置換亦須保持 E_j^q。
无對齊置換時，式 (5) 沒有額外限制。每次核對全部 24 个置換。

## 4. Singleton 列在同一原首橋的 β

固定同一 W，取 singleton 列 q 的 F_W(q)={c}，另有 pair 列 p。
令 I_W 是 W 的已固定包絡，並取

\[
K_I(q,p)=\{h:\forall i\in I_W,\ q_i=h\iff p_i=h\}.\tag{6}
\]

實際支援包含於 I_W，所以 K_I 是實際支援上守恆色集合的子集，
足以套[首橋固定色守恆](c5_single_spoke_first_bridge.md#2-固定色守恆與端點的額外一色)。
此處 K 是逐色 membership，不是要求整列相同。

在原接點 x₀，q、root=c 的 tightness 使 c 不在直接附件色集 D₀^q
及路徑外 palettes Q₀^q。原首橋 x₀x₁ 的 q palette 為 {β}，所以

\[
E_0^q=\{c,\beta\},\qquad \beta\ne c.\tag{7}
\]

如果 c∈K_I，但 c∉F_W(p)，固定色 residual 守恆與式 (7) 立即
矛盾。这只用原端點，不把 singleton 擴成 pair。

若 c∈K_I∩F_W(p)，固定色守恆亦使 c∈E₁^q；同一首橋 palette
β 屬 E₁^q。ℓ=1 時 x₁ 是另一接點，亦用式 (7)；ℓ≥3 時它是
路徑內點，兩個 incident bridge palettes 互異且 |E₁^q|=2。因此

\[
\boxed{E_0^q=E_1^q=\{c,\beta\},}\qquad
\{c,\beta\}\cap K_I=F_W(p)\cap K_I.\tag{8}
\]

β 在**這一列、這一條原首橋**的兩端相同。不同 singleton 列
的 β 各自選擇，不要求它們相等，也不推論其他路徑袋共用 β。
c∉K_I 時跳過這個首橋条件，保留放寬選項。

## 5. 同一兩袋的全部局部列與原圖 K₅

每份 pair 列對 W₀、W₁ 有 E=F_W(p)；每個符合 §4 的 singleton
列，在选择自己的 β 后，对这**同一兩份原袋**有式 (8) 的 E。
枚舉 β 的全部組合，再對所有這些局部 residual 列合用 stabilizer
及式 (5)。由此得到必包含兩份真實 T₀、T₁ 的支援族 𝒯⊆2^{I_W}。

純 pair 列時，直接復用 t=1 的
[path_evidence helper](../scripts/c5_excess_two_ternary_binary.py)。加入
singleton 時仍復用同一支援運算，但輸入是式 (8) 的**局部 E**，
输出覆盖的仅是首橋两袋；不将 F_W(q)={c} 送作 pair。
Helper 对 admissible_supports／joint_supports 的結果另以直接
24 置換定义核对，輸出另標 `local_residual_rows` 以保留這個區別。

外部 anchors 只取兩條真實原 spokes 的框端點，以及**另一原
分量包絡的兩個真實端點**：

\[
O_0=\{b_s,b_t\}\cup\{\text{另一分量的第一與最後實際附件}\}.\tag{9}
\]

若存在一份固定連通框弧分割 B=X⊔Y，O₀ 碰兩側且每個 T∈𝒯
都碰兩側，取原 branch sets

\[
W_0,\quad W_1,\quad
Z=(V(P\cup\{rx_0,rx_\ell\})\setminus\{x_0,x_1\})
\cup V(\text{另一原分量}),\quad X,\quad Y.\tag{10}
\]

Z 經 r 連通；ℓ=1 時仍包含 r 與另一原分量。原首橋、兩條朝外
cycle 邊、兩袋各到 X／Y 的實際附件、Z 到 X／Y 的真實 spoke
或另一分量附件，以及框分割的切口邊，給全部十對鄰接。
故是同一原 G 的 K₅ minor，與 planarity 矛盾。

此为[兩框弧引理](c5_single_spoke_two_arc.md#2-兩框弧與另一原分量納入-z)
的原构造，多一條 spoke 只增加真实 Z 附件，不要求 r degree 五。
每个 β 组合都要排除才删除选项。空支援族独立矛盾，不能用
vacuous 全称制造 minor；helper 的三框弧备选规则亦保留，本轮
实际所有 minor 排除均为两框弧型。

## 6. 十列共同必要域与有限结果

每份固定包络上的局部 equality pattern，只選一次容量至多二、
stabilizer 不变的 F 选项；其余列用共同 S₄ 搬运。实际附件可能
稀疏，允许 profile 依赖整个 envelope 只扩大必要域。DFS 逐列
保留式 (2) 的完整目标接受性、式 (3) 的三个原省略条件、共同
profile、纯 pair 路径及 §4–5 全部适用的首橋条件。

**400 queries 全部無解。** 搜尋计数为：618 個節點、684 次
共同 profile 衝突、1,044 次純 pair 共同兩框弧 K₅、211 次首端
固定色矛盾、335 次全部 row-local β 組合排除。这些是搜尋
操作次數，不是來源圖或不同 minors 的數量。

停用 singleton 首橋层后，仍有 20 queries 存活，全部为 941
轨道；每个目标像恰四份。它们的原 spokes 不相邻，一份 binary
占完整跨度二扇区，另一份占完整跨度三扇区。证书保存每份完整
十列 F profile、具名 geometry、ownership 及共同目标，作负控制。
这证明纯 pair 路径条件尚不足；沒有宣稱殘留 profile 可由 disk
或同一来源图实现。

## 7. 完整关系控制、重播及界线

[Checker](../scripts/c5_excess_two_two_spoke_binary.py)及
[artifact](../artifacts/c5_excess_two_two_spoke_binary/observations.json)
保存 40 份共同扇区包络、400 queries 的局部 profile domains、
逐列选项数、搜尋顺序及排除 digest；每个首橋理由保留原分量、
singleton／pair 列、membership 守恆色、全部 β 组合、实际袋
支援族及共同框弧 witness。沿用 helpers 的程式闭包以 SHA256 绑定。

完整五接点控制保留 324-tuple star 算子，及全部 16² 份有序
binary singleton-tuple fibers。先核对全部 65,535 个非空完整
binary relations 的三接点投影，再以全部十一种可达 F 的关系
代表、同 marginals 不同 F 的相关性反例及全集，共十三份完整
relations，核对全部 13²×16=2,704 次关系对／spoke 色集接合。
完整 tuples 与独立 Cartesian-product 定义逐项相等；一般完整
relations 的涵盖由 singleton-tuple union 恒等式负责。這些是
抽象代数控制，不是来源 realizability witnesses。

```bash
python3 scripts/c5_excess_two_two_spoke_binary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_two_spoke_binary.py --check
python3 scripts/c5_excess_two_ternary_binary.py --check
python3 scripts/c5_short_support_singleton.py --check
python3 scripts/c5_single_spoke_first_bridge.py --check
python3 scripts/c5_single_spoke_residual_locality.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
python3 scripts/c5_single_spoke_cross_row.py --check
python3 scripts/c5_single_spoke_two_arc.py --check
```

本页排除指定 t=2、(2,2) 整型，没有将 first-bridge binary 定理
套到三／四接点分量。其他 t=2 分拆由各自报告负责；共同 ε≥2、
两個 degree-5 roots（含 mixed）、一般来源／出口及 K∞=K≤5 的
证据边界不变。任意大小 topology 与 Gallai 依赖尚未 Lean 化。
