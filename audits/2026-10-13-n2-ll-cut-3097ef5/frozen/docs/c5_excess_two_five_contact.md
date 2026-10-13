# ε=2：t=1 五接點整型的共同 active tree 與 K5 排除

2026-10-03。接續 [t=1 原 binary 省略](c5_excess_two_single_spoke_binary.md)，
本頁處理另一份原接點分拆；目前總入口見 [Kempe 導覽](c5_kempe_guide.md)。

**933／941 固定完整 Σ、edge-minimal C₅ disk 來源，在 ε=2、唯一
degree-6 root、t=1 下，不可能只有一份五接點原分量。** 這次排除
整份 `(5)` 來源，並非只排除全 degree-4 真子核心。

原 spoke 的刪邊見證給同一原 C 的三個禁色。共同差異係數 τ 的
active forest 有五個具名接點葉，只有兩種形狀：一個正 C₅，或三個
正 triangles 以兩條負 bridges 相連。原邊及實際 boundary tethers
在兩種情況都給出 K5 minor。此任意大小證明不新增圖枚舉；Python
核對固定 palettes、完整五接點 relations 及 4,800 份具名 minor 控制。
未新增 Lean theorem，不排除其他 ε=2 來源或提高共同 ε≥2。

## 1. 原 spoke 的私有色見證

G 有限簡單，B=(b₀,…,b₄) 為指定有序 induced-C₅ disk 外框。
有效內部 H 連通；r 完整 degree 六，其他內點完整 degree 四。
r 的唯一原 spoke 是 rb_s；H−r=C 連通，P=(u₀,…,u₄) 是五個
不同的原接點。保留原接點順序、全部實際附件、ownership 及嵌入。

完整 Σ edge-minimality 提供 q：G 拒絕 q，而 G−rb_s 接受 q。
因 G 接受全部 T4，q 是 singleton 列。令 e=q(b_s)、U={0,1,2,3}、
A=U∖{e}。記原 C 的完整有序 relation 為

\[
R_C(q)=\{(f(u_0),\ldots,f(u_4)):f\text{ 是原 C 的完整 boundary-list coloring}\},
\qquad F_C(q)=\bigcap_{t\in R_C(q)}\operatorname{set}(t).
\]

刪 r 後每個接點都有 list slack，故生成樹逆序貪婪給 R_C(q)≠∅。
原圖拒絕迫 A⊆F_C(q)。刪 spoke 的延拓必令 r=e，否則原 spoke
也成立；該延拓的 C tuple 避開 e，故 e∉F_C(q)。因此

\[
\boxed{F_C(q)=A.} \tag{1}
\]

三個 root 色 d∈A 都使同一 C 的 lists

\[
M_d(v)=U\setminus\bigl(q(N_B(v))\cup
 (\{d\}\text{ if }v\in P\text{ else }\varnothing)\bigr)
\]

不可著色。完整 degree 四給 |M_d(v)|≥deg_C(v)；連通 slack-list
引理迫處處等號。外部 degree-list 刻畫給同一 C 為 Gallai tree 及
每份 M_d 的 block palettes，見 [完整介面 §2](c5_degree5_interfaces.md#2-gallai-結構tight-lists-與-block-palettes)。
原 B∪{r} 由 rb_s 連通；[連通外框 K4 論證](c5_degree5_tree_components.md#1-連通外框排除-degree-4-分量的-k4)
只用 C 內點 degree 四、拒絕 lists 及此外部連通性，不用 r degree 五。
其四條真實外路徑仍給 K5，故本題 C 亦 K4-free。其 blocks 只有
bridges 及 odd cycles。

## 2. 同一 τ 與五葉的任意大小分類

沿用 [三拒絕共同係數證明](c5_single_spoke_four.md#2-三組差異共用一個係數向量)：
原 vertex–block incidence matrix I 的欄線性獨立，而
\(\mathbf1_{M_a}-\mathbf1_{M_b}=\mathbf1_P(\mathbf e_b-\mathbf e_a)\)。
故三個色對共用唯一 τ，滿足

\[
I\tau=\mathbf1_P,\qquad
\mathbf1_{S_K^a}-\mathbf1_{S_K^b}
=\tau_K(\mathbf e_b-\mathbf e_a),\qquad \tau_K\in\{-1,0,1\}. \tag{2}
\]

τ=+1 的 block palette 是 A∖{d}，必為 odd cycle；τ=−1 的
palette 是 {d}（bridge）或 {d,e}（odd cycle）。τ=0 保持固定
palette。所有列仍在同一字面四色框。

同頂點的 palettes 不交，迫正、負 active blocks 各至多一個。
原接點恰接一個正 active block；非接點或沒有 active blocks，或
恰接一正一負。active incidence forest 的 vertex-nodes 因而
degree 一或二，**全部葉恰為五個原接點**。

每個非空 active 分量至少三葉：若只有兩葉，樹必為一條 path，
所有 block-nodes degree 二，即都是 bridges；但其葉須接正 block，
而正 bridge 不存在。五葉因此不能分成兩個 active 分量，forest
實為一棵樹。葉數公式給

\[
5=2+\sum_{\text{active odd cycles }K}(|V(K)|-2). \tag{3}
\]

**負 odd cycle 不可能。** 它的每個頂點都不是接點，且須另接一個
正 odd cycle；這些正 blocks 各異，否則 incidence tree 有環。
負 cycle 至少三點，所以有至少三個不同正 cycles。這四個 cycle
blocks 對式 (3) 至少貢獻四，使葉數至少六，矛盾。

餘下只有正 odd cycles 與負 bridges。每個負 bridge 的兩端都接
正 cycle，不能接另一負 bridge，亦不能以接點結束。因此它是兩個
正 cycles 之間的一條**原邊**，不存在未記錄的 active path 臂。
式 (3) 的正奇數分拆只有 3 或 1+1+1，得到：

1. 一個正 C₅，五點恰為原 P，沒有 active bridge；
2. 三個頂點互斥的正 triangles，以兩條原負 bridges 形成一條鏈。
   兩個末端 triangles 各有兩個原接點，中間 triangle 有一個。

正 cycles 不能共享頂點，否則同列兩個正 palettes 相交。
所有 inactive 旁支仍保留，可任意大；本分類沒有枚舉原來源圖。

## 3. 選定正 cycle 的實際 boundary tethers

第一型選整個 C₅；第二型選 active 鏈的一個末端 triangle T。
每個所選 cycle 頂點 v 有兩條 cycle 邊，另外恰有一條原 root-contact
邊或原 active bridge。因此 degree 四留下恰一條其他原邊。

該邊若不直達 B，便為進入 inactive 旁支 W_v 的 bridge：另一個
cycle 要再占兩條邊，超過 degree。W_v 不能返回 active tree，
不能含任何原接點（五個原接點都已在 active tree），各份 W_v
互不相交。因此它沒有 r 鄰居。

W_v 必碰 B。否則 C−W_v 的 v 出現 degree slack，固定任一 d∈A
即可貪婪著色；W_v 沒有外部色限制，其 bridge 端點內部 degree 三，
全 U lists 亦可貪婪著色。整體置換 W_v 的色使 bridge 兩端異色，
拼回原 C 的 M_d-coloring，違反拒絕。

所以每個選定頂點有原圖路徑 Q_v 到實際 boundary 附件。這些
tethers 的內部互斥，避開 r 及其餘 active tree；末端可相同。
此處沒有把整條支援弧新增為附件，也未替換原 relation。

## 4. 兩種形狀均有原圖 K5 minor

令
\[
O=B\cup\bigcup_{v\text{ 選定}}(V(Q_v)\setminus\{v\}).
\]
O 連通且避開 active tree 與 r。

**正 C₅ 型。** 按其真實 cycle 次序寫 v₀,…,v₄；這是幾何角色，
不更換原 relation 的具名座標。取五個 branch sets

\[
\{v_0,v_1,v_2\},\quad\{v_3\},\quad\{v_4\},\quad\{r\},\quad O.
\]

前三組都是連通 cycle 弧，兩兩相鄰；每組有原 r-contact 及
實際 boundary tether。最後 r–O 由唯一 spoke 給出，故是 K5。

**三 triangle 型。** 寫末端 T={a,b,x}，a、b 是原接點，而 x 的
原負 bridge 通往其餘 active 部分 A′。取

\[
\{a\},\quad\{b\},\quad\{x\},\quad Z=\{r\}\cup A',\quad O.
\]

A′ 是另外兩個 triangles 及其中的 bridge，連通並含其餘三個
原接點；Z 因而連通。前三組由 T 相鄰，並分別經 ar、br 及 x 的
原 bridge 接 Z；三條實際 tethers 接 O，rb_s 接 Z–O。再次得到
K5，與 planarity 矛盾。

兩個 minor 都只用於來源非平面性反證；合併 boundary 的 O 並非
保持完整 Σ 的狀態操作。式 (1)–(3) 與真實 tethers 涵蓋任意大小
原 C，故完成整份 `(5)` 來源排除。

## 5. 固定控制、重播與界線

[Checker](../scripts/c5_excess_two_five_contact.py)與
[artifact](../artifacts/c5_excess_two_five_contact/observations.json)保存：

- 四個 spoke 色的 52 份共同 palette 型及 188 個完整 incidence 控制；
- 五葉式的 26 個帶符號 cycle-tree 控制，恰四個帶標號可行型，
  對應上述兩種幾何形狀；
- 兩形狀乘四個 omitted 色，共八份抽象 residual 圖的完整五接點
  relations，456 tuples 及各自完整染色 witnesses；完整六接點
  root 接合只允許 omitted 色，加入該色 spoke 後全拒絕；
- 120 個具名接點刪邊 lifts，核對各 root 色都由原完整 tuple 解除；
- 五個 spoke 位置、全部 120 個原接點角色排列、直接／細分 tethers、
  共用／不同 boundary 末端，合計 4,800 次 K5 minor 核對。保存
  40 份幾何代表的全部原邊、實際路徑、branch sets、十條鄰接 witness，
  並以具名排列域及 digest 綁定全部控制；
- 六份缺 spoke、branch sets 重疊及虛構 tether 頂點的負控制。

這些 residual 圖及 minor skeletons 是抽象控制，不宣稱有 disk
來源。有限五葉樹控制的上界由 §2 的紙面公式導出，並非任意大小
結論的實驗替代。外部 degree-list 定理、無界共同 τ 及 topology
沿用上述紙面依賴，未由 Python 或 Lean 重新形式化。

```bash
python3 scripts/c5_excess_two_five_contact.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_five_contact.py --check
python3 scripts/c5_single_spoke_four.py --check
```

本頁停止於唯一原五接點整型排除；其餘 t=1 分拆的整型來源仍須
各自給出證明，不能由「無全 degree-4 真子核心」推得不存在。
