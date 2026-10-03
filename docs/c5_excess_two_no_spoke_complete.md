# ε=2：唯一 degree-6 root 的 t=0 全部分拆排除

**發布整理（2026-10-03）**：本頁與 t=3 的 checker、證書及導覽更新
一併提交推送；本次重播及範圍見 [發布紀錄](history/2026-10-03-excess-two-degree-six-publish.md)。
下文的「本輪未 commit／push」保留研究輪次語境；即時發布狀態以 Git 為準。

2026-10-03，接手基準 `4701f4c`。接續 [t=3 全分拆排除](c5_excess_two_three_spoke_complete.md)，
沿用 [原 no-spoke 外部連通](c5_no_spoke_exterior.md)、
[短支援引理](c5_short_support_singleton.md)與
[同一 binary 路徑塊](c5_excess_two_ternary_binary.md#4-同一原-binary-路徑塊的跨列支援)。
目前停止點見 [Kempe 導覽](c5_kempe_guide.md)，實際重播範圍見
[本輪紀錄](history/2026-10-03-excess-two-no-spoke-complete.md)。

**933／941 固定完整 Σ、edge-minimal induced-C₅ disk 來源，在 ε=2、
唯一完整 degree-6 root 的前提下，t=0 的十一種原接點分拆全部不可能。**
連同 t=1、t=2、t=3 及 T4 的 t≤3，排除唯一 degree-6 root 的整條 ε=2 分支。
因此同一來源若 ε=2，必有兩個完整 degree-5 roots；尚未排除這個情形，
共同下界仍為 ε≥2。證據是任意大小紙面化約、明列外部 degree-list 定理及
Python 固定必要域證書，未新增 Lean theorem，不宣稱一般出口或 `K∞=K≤5`。

## 1. 同一原來源與完整七接點接合

G 有限簡單，B=(b₀,…,b₄) 是指定有序 induced-C₅ disk 外框。
Σ(G) 為 933、941 或整圖 D₅ 像，接受全部 T4；每條非框邊 e 皆有
Σ(G−e)⊋Σ(G)。有效內部 H 非空連通，r 的完整 degree 六，其他有效
內點完整 degree 四；r 沒有任何原 boundary spoke。

H−r 的原連通分量 Cᵢ 有非空具名有序接點 Pᵢ=N(r)∩Cᵢ，
Σᵢ|Pᵢ|=6。原邊、actual attachments、ownership、環序、嵌入及
接點座標保持；每列仍在同一字面四色框 U={0,1,2,3}。
對同一 proper boundary coloring b，Rᵢ(b) 是原 Cᵢ 的完整有序接點
relation。未指定 r 色時，完整 degree 四給 degree lists，接點提供
slack；以接點為生成樹根逆序貪婪，故 Rᵢ(b) 非空。原完整接合是

\[
J_b=\{(a,t_1,\ldots,t_m):t_i\in R_i(b),\quad
a\notin\bigcup_i\operatorname{set}(t_i)\}.\tag{1}
\]

令 Fᵢ(b)=∩_{t∈Rᵢ(b)}set(t)，式 (1) 的精確 root 投影為

\[
\operatorname{proj}_rJ_b=U\setminus\bigcup_iF_i(b).\tag{2}
\]

每份 surviving root 色都有各原分量的一份完整避色 tuple 及完整
染色 witness，能在同一 b 下拼回。式 (2) 只是這個 root 查詢的精確
投影，沒有替換 Rᵢ，沒有拆 marginals 或逐分量重新正規化。

不可著色的 degree lists 沿用
[Dvořák 講義 Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)：
連通圖的拒絕 degree assignment 處處 tight，且有同一 Gallai tree 的
blockwise-uniform palettes。此次重讀原文；定理不要求整份 G 在每列
都是 minimal obstruction。下文 incidence matrix 欄獨立性及共同 τ
沿用 [原四列證明](c5_no_spoke_exterior.md#4-單分量-5四份-palettes-的偶數接點障礙)。
此外部依賴與紙面來源化約不算作 Python 或 Lean 已證。

## 2. 無 spoke 的真實外部 hub 與共同跨度

每份原 C 都有完整 Σ minimality 提供的私有色見證。選一條原 contact
邊 rp；G−rp 的新接受列 q 有完整染色，記 r 色為 a。其他原分量的
完整 tuples 已避開 a。若 a∉F_C(q)，換入原 C 的一份完整避 a 染色
即可恢復 G 的染色，矛盾。因此 a∈F_C(q)，且 a 不在其他分量的 F 中。
這是原 G 的完整 Σ 邊見證，沒有把 G 當成每列的 q-minimal core。

若 N_B(C)=∅，原 R_C 不依賴 boundary row，並在同一全域 S₄ 作用下
保持；其非空 F_C 只能為 U。這使原 G 拒絕所有 proper rows，與 T4
全收矛盾。因此每份原分量都實際碰 B。

當 m≥2，對指定 C，取另一原分量 D 的 contact 到其實際框附件的
原簡單路徑 Q=r…b_h。Q 內部在 D，避開 C 與其他框點；
B∪{r}∪V(Q) 是 C 外的同一連通 hub。原
[K₄-block 四 tether 論證](c5_no_spoke_exterior.md#3-以另一分量恢復-k4-的外部-hub)
因而成立：只在 C 某列 F 非空時使用拒絕 degree lists，四條原 tethers
及該 hub 給 K₅，故這份 C 為 K₄-free。沒有新增或替換原 spoke。

若 C 的實際支援包含於相鄰兩框點 {a,b}，來源
[完整支援引理](c5_independent_support_capacity.md#11-degree-與完整支援)
迫 G 碰齊五個框點，故另一原分量提供避開 C 的 r–h 路徑，h∉{a,b}。
[短支援的兩／三 hub 證明](c5_short_support_singleton.md#2-tightness-使同色-hub-合併保留-degree)
的唯一 spoke 用途是恢復 C 外的連通性；改用上述 Q，即保留其原
branch sets、tightness 後的 degree 及所有原邊鄰接。因此無 spoke 時
亦有 F_C(b)=∅，與該固定 C 的私有見證矛盾。

所以每份固定原支援不能包含於單一框邊。由
[環狀區塊次序](c5_no_spoke_supports.md#2-每份支援至少兩點且有環狀區塊次序)，
各原分量的 contact 與附件在 annulus 上同序；在同一環狀提升中，
各支援從第一個到最後一個實際附件的包絡 Iᵢ 開框邊段互不重疊。
不為各分量獨立選最短循環弧。於是

\[
\boxed{\ell_i\ge2,\qquad\sum_i\ell_i\le5.}\tag{3}
\]

這相加的是同一原圖固定支援的幾何量，私有見證可來自不同列。
三份以上原分量立即需要至少六段，故 m≥3 全排。
單分量 (6) 沒有這個外部 Q，須使用下一節的獨立論證。

## 3. 單分量 (6)：四 palettes 的飽和 K₄ 與原 K₅

固定任一原拒絕列 q；式 (2) 給 F_C(q)=U。四個 root 色 d∈U 都使
同一原 C 的 degree lists M_d 不可著色。由 tightness，接點的
boundary 鄰色不能等於任何 d，所以接點沒有 boundary 鄰居；四份
lists 的差是 1_P(e_b−e_a)。對同一 vertex–block incidence matrix I，
欄獨立性迫一份共同 τ：

\[
I\tau=\mathbf1_P,\qquad
\mathbf1_{S_K^a}-\mathbf1_{S_K^b}
=\tau_K(\mathbf e_b-\mathbf e_a),\qquad\tau_K\in\{-1,0,1\}.\tag{4}
\]

四個色全部參與，故正 active palette 只能是 U∖{d}，其原 block
是 K₄；負 active palette 只能是 {d}，其原 block 是 bridge。
同頂點的 palettes 不交，迫正、負 blocks 各至多一個。原 contact
恰接一個正 K₄、沒有負 bridge；其餘 active 點恰接一正 K₄及一負 bridge。

每個 active 點已在完整原 G 飽和：三條 K₄ 邊加原 root-contact，
或三條 K₄ 邊加原負 bridge。沒有 inactive 邊或 boundary tether 的
餘額。C 連通且 P 非空，因此一個 active 分量就是整份原 C。
原 active incidence tree 的葉恰為六個原接點；正 block node degree 四、
負 block node degree 二。葉數公式 6=2+2k 迫恰有兩個正 K₄，
以一條原負 bridge 相接。

寫兩份原 blocks 為 {x,a₀,a₁,a₂}、{y,c₀,c₁,c₂}，bridge 為 xy；
六個原接點是 aᵢ、cᵢ。這只是指派幾何角色，原有序座標仍保存。
取五個 branch sets

\[
\{x\},\ \{a_0\},\ \{a_1\},\ \{a_2\},\
Z=\{r,y,c_0,c_1,c_2\}.
\]

Z 由右 K₄ 及三條原 rcᵢ 邊連通；Z–x 用原 xy，Z–aᵢ 用原 raᵢ。
前四組的六條邊是左原 K₄，故得到 K₅，矛盾。此處沒有假設 C
K₄-free，也沒有假造 C 外的 root–B 路徑；只需一份拒絕列。

[Reduction checker](../scripts/c5_excess_two_no_spoke_reduction.py)及
[artifact](../artifacts/c5_excess_two_no_spoke_reduction/observations.json)
核對 16 個四-palette 型、52 個 local incidence 型，並保存這個原 K₅。
兩 K₄ 抽象控制的完整六接點 relation 恰有 432 tuples：兩個 injective
三元組的缺色不同。每份 tuple 都看齊 U，所以完整七接點 root join
為空；六個 marginals 卻全為 U，乘它們會錯誤放行四個 root 色。
六條具名 contact 的刪邊 lifts 核對共 864 份，每 root 色／contact 有 36 份；
保存 24 份代表、各自計數及完整 relation 的染色 witnesses，全部 lifts
可從它們重建。破壞 bridge、contact、hub 連通性的負控制另保存。
這個非平面抽象圖不是來源實現證書。

## 4. 十一種分拆只留下 (4,2)

m=2 時另一原分量提供 §2 的外部 hub，因此原
[三接點兩禁色](c5_no_spoke_exterior.md#5-多分量的三四接點分量也排除)
及四接點三禁色 K₅ 在每個 proper row 都適用，給 |F₃|≤1、|F₄|≤2。
[五接點三 palettes](c5_excess_two_five_contact.md#2-同一-τ-與五葉的任意大小分類)
只需任選三色 A⊆F₅，無須原 spoke 的私有色見證。原正 C₅／三 triangle
分類及實際 tethers 保持，把另一原分量的 Q 加入 boundary hub，便提供
兩種 K₅ 原先使用 spoke 的唯一 r–O 鄰接。因此 |F₅|≤2，即使原先
F₅=U 也可選任意三色來反證。

| 原接點分拆 | 整型來源排除 |
| --- | --- |
| (6) | §3 飽和兩 K₄、原 bridge 與六 contacts 給 K₅ |
| (5,1) | 五接點至多禁二色，unary 至多一色，不能覆蓋 U |
| (4,2) | 每列容量 (2,2)，由下一節的同源 binary 路徑支援全排 |
| (3,3) | 兩份 ternary 各至多禁一色，不能覆蓋 U |
| (4,1,1)、(3,2,1)、(3,1,1,1)、(2,2,2)、(2,2,1,1)、(2,1,1,1,1)、(1,1,1,1,1,1) | 同一嵌入至少三份跨度二，超過五段 |

Reduction checker 核對全部十一分拆與 201 個字面容量組合，只留下
(4,2) 的六種互補 pair 覆蓋；另測 480 份零-spoke 短支援 two-hub
lifts、40 份五接點外部原 unary 路徑 K₅。後兩者是具名 minor
skeleton 控制，任意大小涵蓋由上述紙面推導承擔。

## 5. (4,2)：環狀 profiles 與同一原 binary 路徑

原分量記 C（四接點）與 V（兩接點），原有序 contacts 為
(C₀,C₁,C₂,C₃,V₀,V₁)。式 (2) 及 |F_C|,|F_V|≤2 迫每份原
拒絕列有兩份互補、不交的 pair。四接點 C 始終保留完整 R_C；
只有原兩接點 V 使用 binary 路徑定理。

由式 (3)，兩份環狀包絡跨度均至少二，總和至多五。共同旋轉整份
原來源，使 C 的第一個實際附件為 b₀，四種模板恰為

\[
(012,234),\ (012,340),\ (012,2340),\ (0123,340).\tag{5}
\]

全部五個 named rotations 共 20 份配置；獨立以兩包絡開框邊的
edge masks 互斥重算，得到同一域。每份端點仍是真實附件，內部
位置只是容許範圍，沒有全部新增為附件。相同原分量在十列共享
一個局部 equality-class profile；每個至多二色 F 對該列支援的
S₄ stabilizer 不變，所有字面色名共同搬運。容許 profile 依賴整條
包絡是必要域放寬，涵蓋真正稀疏支援。

20 份配置乘兩候選十個 D₅ 像，共 **200 次同源必要查詢**。
局部 S₄ profiles 先排除 180 次；其餘 20 次各有 360 份完整十列
資料，共 **7,200 份抽象殘留**。不能把此層誤報為空域。

在任一 |F_V(q)|=2 的列，兩份拒絕 lists、K₄-free 及兩個原 contacts
迫同一原 V₀–V₁ 奇數 bridge 路徑 P，長度至少一；與有無 spoke
無關，適用前提見 [no-spoke 原路徑報告](c5_no_spoke_path_minor.md#1-前提完整關係與共用路徑塊)。
刪 P 邊得到固定原袋 W_j，含路徑點、全部旁支及實際附件；T_j⊆I_V
是其真實支援。每袋完整 rooted residual 等於 F_V(q)。原 P 唯一，
因此全部 pair rows 使用同一批 W_j，而非各列另挑同構路徑。

逐袋支援穩定子及 [跨列完整搬運](c5_single_spoke_cross_row.md#2-跨列-residual-換色引理)
給出同一容許族 𝒯：固定 q(T) 的每個置換保持 F_V(q)；若
p|T=πq|T，則 F_V(p)=πF_V(q)。全部 24 個置換都核對；無對齊
置換時不排除。此次只用原拒絕列（其 F_V 都是 pair），不對 singleton
或 accepted-row pair 套用額外公式。

7,200 profiles 依原拒絕列的 binary pair schema 分成 **160 組，
每組 45 份**。每份共同容許族都非空，但均有同一份兩連通框弧
分割 B=X⊔Y，使每個 T∈𝒯 都碰兩側，且 C 的兩個真實包絡端點
也碰兩側。取 P 任意相鄰兩點 x_j、x_(j+1)，令 J=P 加兩條原
root-contact 邊，五個原 branch sets 為

\[
W_j,\quad W_{j+1},\quad
Z=(V(J)\setminus\{x_j,x_{j+1}\})\cup V(C),\quad X,\quad Y.\tag{6}
\]

J 刪相鄰兩點後的其餘部分經 r 連通，長度一時就是 {r}；整份原
C 由其 contact 邊接到 r，故 Z 連通。原 C 的兩個實際端點附件
給 Z–X、Z–Y；兩袋各有實際附件到兩框弧，給四條鄰接。原 bridge
及 J 朝外的兩邊給前三組的三對鄰接；原框切口給 X–Y。五組互斥，
十對均有原邊，故為 K₅。C 的其餘兩條 contacts、原 relation 及
全部附件仍在來源中；minor 不必使用所有原點。

**160 份同源原路徑證書全作共同兩框弧 K₅，200 queries 最終皆無解。**
不需原首橋、四接點 active forest、D 身份 screen 或省略全收。
四接點 pair 可含 D、可不含 D，也可跨列變動，本證明沒有假設
它在所有原拒絕列都含 D。

[Four/two checker](../scripts/c5_excess_two_no_spoke_four_two.py)及
[artifact](../artifacts/c5_excess_two_no_spoke_four_two/observations.json)
保存 20 份 named geometry、200 queries、全部弱 profiles 的 digest、
160 個原拒絕列 pair schemas、每 query 的代表完整 profile、共同真實袋支援族
及框弧 witness。逐族以直接 24 置換及獨立框弧分割定義重算；完整
七接點代數另保留四個 C contacts 與兩個 V contacts，核對 tuple fibers
與直接接合及非 Cartesian relation 的 marginal 碰撞。這些計算不證
任何抽象 profiles 具有 disk 實現。

## 6. 結論、重播與精確停止點

十一種原分拆全排，故同一來源前提下 t≠0。連同前序 t=1、2、3
整型排除及 T4 的 t≤3，得到

\[
\boxed{\Sigma(G)\in\operatorname{Orb}_{D_5}\{933,941\},\quad
\varepsilon(G)=2\quad\Longrightarrow\quad
\text{兩個完整 degree-5 roots，沒有唯一 degree-6 root。}}
\]

此處沿用原 excess／有效內點 degree 前提；並未排除兩個 degree-5
roots（相鄰或非相鄰、含 mixed）。因此 **不能提高為 ε≥3**，也
沒有一般來源排除、一般單側／共同出口或 `K∞=K≤5`。

```bash
python3 scripts/c5_excess_two_no_spoke_reduction.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_no_spoke_reduction.py --check
python3 scripts/c5_excess_two_no_spoke_four_two.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_no_spoke_four_two.py --check
python3 scripts/c5_no_spoke_exterior.py --check
python3 scripts/c5_short_support_singleton.py --check
python3 scripts/c5_excess_two_five_contact.py --check
python3 scripts/c5_excess_two_ternary_binary.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

實際執行與未重跑項目見本輪紀錄。任意大小 Gallai palettes、共同 τ、
真實支援次序及原 minor 抽取由紙面與明列依賴承擔；Python 證固定必要域
及完整 relation 代數。`lake build` 驗證既有專案，不把新拓撲變成 Lean theorem。
本輪未 commit／push，接手時已有的 t=3 成果保持。

下一窄入口是 ε=2 的兩個 degree-5 roots：先核對相鄰型的既有共同
分離定理對兩候選完整 Σ 的適用範圍，保留原 mixed／no-mixed、具名
接點、實際支援及同一字面色框。指定 q／p 出口不自動等於完整候選
來源排除；目前停止點由 Kempe 導覽維護。
