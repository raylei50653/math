---
docgraph:
  id: c5.single-spoke-four
  family:
    - c5
    - c5.single-spoke
  requires:
    - c5.single-spoke-cores
    - c5.single-spoke-three-one
---
# Single-spoke (4)：三份拒絕 palettes 的共同結構與 K5 排除

後續（2026-09-28）：本頁 §7 的 t=0 外部連通入口已由
[no-spoke 排除](c5_no_spoke_exterior.md) 完成：多分量恢復 K4 hub，
單分量 (5) 由四列偶數接點排除；t=0 只剩 (2,2,1)、(2,1,1,1)。
下文「尚未新增 t=0 排除」保留本輪原語境。

2026-09-28。接續 [(3,1) 排除](c5_single_spoke_three_one.md) 及
[single-spoke 必要覆蓋](c5_single_spoke_cores.md)。研究優先序見
[HANDOFF](HANDOFF.md)。

**在 single-spoke minimal q-core 的前提下，(4) 不可能。**
三份拒絕 palettes 在同一原 block tree 上共用一個差異係數向量。
其 active 部分恰是兩個互斥 triangle，由一條原 bridge 相連；四個原接點
是兩個 triangle 各自的另外兩點。原 boundary tethers 給 K5 minor。
不需 T4 acceptance 或第二 boundary row 拒絕，不限制來源大小或旁支。

這是任意大小紙面證明＋外部 degree-list 定理＋Python 有限控制，未 Lean
化。與既有 (3,1) 排除、(2,2)／(2,1,1) 分離合成後，唯一 degree-5 的
t=1 全部接回 [條件式單側出口](c5_single_sided_exit.md)；一般單側出口、
t=0、高 degree、多 degree-5 及主命題仍未證。

## 1. 同一原分量的三份 tight lists

G 有限簡單，B=(b0,…,b4) 是 induced-C5 disk 外框，有效內部 H 連通。
G 是 q=01012 的 edge-minimal obstruction；唯一完整 degree-5 點 z 的
boundary 鄰居恰為 b_s，其餘有效內點完整 degree=4。H−z=C 連通，
P=(u0,u1,u2,u3) 是四個互異、具名、有序的原接點。全部 boundary 附件、
旁支、原嵌入與接點順序保留。令 U={0,1,2,3}、e=q_s、A=U\{e}。

沿用完整 relation

\[
R_C(q)=\{(f(u_0),f(u_1),f(u_2),f(u_3)):f\text{ 是同一 }C
\text{ 的合法 boundary-list coloring}\}.
\]

不可刪減覆蓋給 F_C(q)=⋂_{t∈R_C(q)}set(t)=A。故每個 d∈A 都拒絕
下列同一 C 的 lists：

\[
M_d(v)=U\setminus\bigl(q(N_B(v))\cup
 (\{d\}\text{ if }v\in P\text{ else }\varnothing)\bigr).
\]

完整 degree=4 給 |M_d(v)|≥deg_C(v)。連通 slack-list 貪婪引理使所有
拒絕列處處緊：|M_d(v)|=deg_C(v)。外鄰顏色因此逐點互異，接點的
boundary 色避開 A；特別接點最多有一個 boundary 鄰居，其色只能是 e。
對任意不同 a,b∈A，

\[
\mathbf1_{M_a(v)}-\mathbf1_{M_b(v)}
 =\mathbf1_{v\in P}(\mathbf e_b-\mathbf e_a). \tag{1}
\]

外部 [Dvořák 講義 Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
給 tightness 與 blockwise-uniform degree-list 刻畫，本輪已重讀。C 是
Gallai tree；每個 block K 有 palette S_K^d，incident palettes 在每個
頂點互斥且聯集恰為 M_d(v)。[連通外框 K4 引理](c5_degree5_tree_components.md#1-連通外框排除-degree-4-分量的-k4)
適用，因 B∪{z} 經原 spoke 連通。故 blocks 只有 bridges（palette 大小一）
與 odd cycles（palette 大小二）；更大 clique 由 planarity 排除。

## 2. 三組差異共用一個係數向量

令 I 是 C 的 vertex–block incidence matrix，I_{vK}=1 iff v∈K。
I 的欄線性獨立：在 I x=0 中，leaf block 的 private vertex 給出該欄
係數零；移去該 block 及 private vertices，歸納至最後一個 block。
此處包含全部原 vertices、blocks，並未另選三張 pairwise 樹。

固定 a≠b，將 (1) 按每個顏色展開。b 的 membership 差向量 τ^{ab}
滿足 Iτ^{ab}=1_P；a 的差向量為 −τ^{ab}，其餘色的差向量皆零，均由
欄獨立性推出。所有 pairs 的右側相同，故

\[
\tau^{ab}=\tau,\qquad I\tau=\mathbf1_P,\qquad
\mathbf1_{S_K^a}-\mathbf1_{S_K^b}
 =\tau_K(\mathbf e_b-\mathbf e_a). \tag{2}
\]

每個 membership 是 0/1，故 τ_K∈{−1,0,+1}。把三份 palettes 同時
代入 (2)，只剩下列可能（每列 d 遍歷同一 A）：

| τ_K | 三份 palette S_K^d | block 限制 |
| --- | --- | --- |
| 0 | 同一固定 palette | bridge 或 odd cycle |
| +1 | A\{d} | 必是 odd cycle，不能是 bridge |
| −1 | {d} | bridge |
| −1 | {d,e} | odd cycle |

例如 τ=+1 迫使 S_K^d 含 A 的另外兩色、不含 d；大小至多二使 e 也
不在其中。這個**正係數 block 不能是 bridge**的限制需要三份拒絕，
兩份拒絕本身不能給出。

同頂點同列 palettes 互斥，所以正係數 block 至多一個、負係數 block
至多一個。Iτ=1_P 於是給：接點恰 incident 一個正 block、沒有負 block；
非接點或沒有 active block，或恰有一正一負。三組 pairwise active
forests 完全相同，不能獨立選配。

## 3. 四葉共同樹恰為兩 triangle 加一條 bridge

取 τ_K≠0 的全部 block-nodes 及其全部 vertex-nodes，保留 incidence
edges。這是原 incidence tree 的 forest；block-node degree 是 |V(K)|，
vertex-node degree 只有一或二，四個葉點恰為四個原接點。

每個非空分量的葉點 incident 正 block，而正 block 是至少三點的
odd cycle。因此每個分量至少三葉；總共四葉使 forest 必連通。
樹的葉數公式給

\[
4=2+\sum_{\deg(x)\ge3}(\deg(x)-2).
\]

vertex-nodes 不貢獻右側；block 大小只有二或奇數，所以恰有兩個
triangle-nodes，其餘 active blocks 都是 bridges，沒有長 odd cycle。

**沒有負 triangle。** 負 triangle 的每個頂點都不是接點，且都另接
一個正 block。這三個正 blocks 必互異，否則原 incidence tree 有環。
但總共僅兩個 triangle，而正 block 不能是 bridge，矛盾。

因此兩個 triangles 都正，其餘 active bridges 都負。負 bridge 的
兩端都須 incident 正 triangle；不能形成連續兩條負 bridges，也不能
以負 bridge 結束於接點。故沒有接點外臂，兩個 triangles 由恰一條
bridge 相接。兩 triangle 也不能共享 cut vertex，因兩個正 palettes
在共享點不互斥。

按原具名接點在兩 triangle 的實際角色，記它們為

\[
T=\{a,b,x\},\qquad T'=\{c,d,y\},\qquad xy\in E(C),
\qquad \{a,b,c,d\}=P.
\]

這只是角色命名，不重排 relation 的四個原座標，也不把同色框點合併。
T、T' palettes 為 A\{d_0}，bridge xy palette 為 {d_0}（d_0∈A）。
inactive 旁支可任意大，仍在原 C 中。此結構由任意大小證明得出，
不是用有限長度控制猜出的正常形。

## 4. 左 triangle 的三條實際 boundary tethers

a、b 已各有兩條 triangle 邊及原 z-contact 邊；x 已有兩條 triangle 邊
及 bridge xy。完整 degree=4 使每點各恰有一條其餘邊。

該邊或直達 B，或是進入 inactive 旁支 W_v 的 bridge vw_v。另一個
cycle 在此要佔兩條邊，超過 degree；邊也不能接到 z（四個接點已用完）
或 active 結構其他點（違反 block tree）。各 W_v 互不相交，不含接點，
且不回接 active 結構。

若 W_v 不碰 B，它也沒有 z 鄰居。刪去 W_v 後 C−W_v 仍連通，M_{d_0}
lists 不變，v 的 degree 少一，slack-list 貪婪法給其 coloring。
W_v 沒有外部色限制：w_v 在 W_v 內 degree=3，其餘點 degree=4，
故全 U lists 再由 slack-list 引理可著色。整體置換 W_v 的四色可使
w_v 避開 v，拼回成 C 的 M_{d_0}-coloring，與拒絕矛盾。

所以每個 v∈{a,b,x} 都有原圖內的簡單路徑 Q_v 到 B。三條 tethers
內部互不相交，避開 active 結構其他點及 z；它們的 boundary 終點可
相同。以上保留真實附件與任意旁支，不以自選的新接線替代來源。

## 5. 原圖 K5 的五個 branch sets

取

\[
\{a\},\quad\{b\},\quad\{x\},\quad
Z=\{z,c,d,y\},\quad
O=B\cup\bigcup_{v\in\{a,b,x\}}(V(Q_v)\setminus\{v\}).
\]

五組互不相交、非空且各自連通。Z 由原 edges zc、zd 與右 triangle
連通；O 由整個 B 及三條原 tethers 連通。十條兩兩鄰接為：

| 鄰接 | 原圖 witness |
| --- | --- |
| a–b、a–x、b–x | 左 triangle 的三條邊 |
| a–Z、b–Z、x–Z | az、bz、xy |
| a–O、b–O、x–O | 各自 tether 的首邊 |
| Z–O | 唯一 spoke zb_s |

因此有 K5 minor，與 planarity 矛盾，完成 (4) 排除。此 minor 只作
非平面性反證；O 會合併 boundary，**不是**保持完整 Σ 的狀態操作。
沒有引用四色定理或假定待證出口命題。

## 6. Python 控制、負控制與證據界線

[checker](../scripts/c5_single_spoke_four.py) 與
[JSON 證書](../artifacts/c5_single_spoke_four/observations.json) 保存：

- 四個 e 的 1,120 組 block palette triples 全測，52 組相容型；
  188 個局部 incidence 型，104 個實際 tight attachment 型，並核對反射。
- 1,280 個連通四葉結構控制（central bridge 數 0…4、四臂長 0…3），
  唯一相容型為兩個正 triangle、單 bridge、零臂；49 個雙路徑控制均失敗。
  任意長度覆蓋由 §3 承擔，控制的上界不是來源大小假設。
- 四個抽象六點圖完整接點關係，每份恰 24 tuples，F=A；逐接點、逐禁色
  保留解除 witness。這些使用 U\{e} residual lists，不宣稱 disk 可實現。
- 960 份原圖 K5 skeleton 證書及 960 份反射核對；涵蓋五個 spoke 位置、
  四接點 24 種具名角色排列、四種 tether 長度及共用／不同 boundary 終點。
  skeleton 省略未用邊，不假稱完整 degree-list 來源或圖枚舉。
- 八個負控制：缺 spoke／contact／central bridge／triangle edge／tether、
  Z 不連通、branch sets 重疊、兩列正 bridge 無法接上第三列。
  前七項僅驗證指定 minor witness 失效，不宣稱修改後整圖必平面。

輸入 SHA256 綁定前序 (3,1) 及覆蓋 checker／artifact；前序證書只讀。
所有 palette 和 relation 查詢固定同一圖、同一列及具名座標，沒有使用
endpoint marginals 代替完整關係。

```bash
python3 scripts/c5_single_spoke_four.py --check
python3 scripts/c5_single_spoke_three_one.py --check
python3 scripts/c5_single_spoke_cores.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際執行範圍見 [本輪紀錄](history/2026-09-28-four-contact.md)。未新增
Lean theorem；任意大小共同樹、tether 及 minor 抽取仍屬紙面證明。
(2,2) 的 278 筆來源排除及 102 筆／51 型雙列計數不變。

## 7. 接合與下一個窄問題

t=1 的必要覆蓋只有四型；(3,1)、(4) 無來源，(2,1,1)、(2,2) 在
出口來源繼承的 T4 假設下均接受指定 p。故 [出口定理](c5_single_sided_exit.md)
的 single-spoke 條件可刪去接點分拆限制。失敗側唯一 degree-5 的核心
只剩 t=0 六型；仍須保留 degree≥6、多 degree-5 及一般核心存在／分離。

下一入口為 t=0 的連通外部集合問題：五個原接點分配在同一或多個原分量，
何時有避開指定 block 的實際 z–B 路徑，使 K4 的四條 tethers 可接成
同一外部 hub？先核對多分量的實際 boundary 支援與完整禁色覆蓋；
單分量 (5) 不能假設 z 與 B 已連通。這裡只指定下一問題，尚未新增
t=0 排除。優先序以 [HANDOFF](HANDOFF.md) 為準。
