# ε=2：t=1、(3,1,1) 的同框支援 profile 排除

2026-10-03。接續 [t=1 原 binary 省略](c5_excess_two_single_spoke_binary.md)
及 [五接點整型排除](c5_excess_two_five_contact.md)。目前總入口見
[Kempe 導覽](c5_kempe_guide.md)。

**933／941 固定完整 Σ、edge-minimal C₅ disk 來源，在 ε=2、唯一
degree-6 root、t=1 下，不可能有原分拆 `(3,1,1)`。** 三接點原
分量在每列至多禁一色；三份原分量各需至少兩個實際框接點。沿唯一
spoke 切開的同一支援弧配置，配合同框局部 S4 等變性，給 168 份
具名必要位置及 146,496 份十列 profiles，無一得到兩候選的十個 D₅ 像。

本頁排除整型來源；任意大小論證與有限必要域空性各負責自己的步驟。
沒有來源圖枚舉、實現性主張或新 Lean theorem，共同下界仍 ε≥2。

## 1. 同一原來源與完整六接點接合

G 有限簡單，B=(b₀,…,b₄) 為指定有序 induced-C₅ disk 外框。
有效內部 H 連通，r 完整 degree 六，其餘內點完整 degree 四。
唯一原 spoke 為 rb_s；H−r 的原分量為三接點 C 及單接點 U、V，
具名有序接點分別為 (x,y,z)、u、v。所有原邊、附件、ownership、
接點環序及嵌入固定。

對同一字面 boundary coloring b，記原完整 relations 為 R_C(b;x,y,z)、
S_U(b;u)、S_V(b;v)。刪 r 後各分量至少有一個 list-slack 接點，
以此為生成樹根逆序貪婪，三份 relations 都非空。完整接合恰為

\[
J_b=\{(a,c,d,e,f,g):(c,d,e)\in R_C(b),\ f\in S_U(b),\ g\in S_V(b),
\quad a\notin\{b_s,c,d,e,f,g\}\}. \tag{1}
\]

每個 tuple 都由三份原分量的完整染色在同一 b 下拼接；同一 C 的
三個座標一直共同取自同一 tuple。令 F_C=∩_{t∈R_C}set(t)，而
F_U=S_U 若 |S_U|=1，否則 F_U=∅；F_V 同理。式 (1) 精確給

\[
\operatorname{proj}_r J_b=\{0,1,2,3\}\setminus
\bigl(\{b_s\}\cup F_C(b)\cup F_U(b)\cup F_V(b)\bigr). \tag{2}
\]

F 只用於這個固定 root 接合；不將 F 視為完整 relation 或一般可迭代
state，也不把三接點 marginals 相乘。

## 2. 三接點在所有列都至多禁一色

若任一 proper b 有兩個不同色 a,d∈F_C(b)，固定 r=a、d 給同一
C 的兩份不可著色 degree lists。完整 degree 四及連通性迫兩份
lists 處處 tight，degree-list 刻畫給同一 Gallai block tree。
原 B∪{r} 經 spoke 連通，故 [連通外框 K4 論證](c5_degree5_tree_components.md#1-連通外框排除-degree-4-分量的-k4)
排除 C 的 K4。

[三接點兩禁色證明 §2–4](c5_single_spoke_three_one.md#2-三個葉點迫使唯一-triangle-加三臂)
於是逐步適用：同一 incidence matrix 的 palette 差迫 active
triangle 加三條原 bridge arms，三個 triangle 頂點各留一條實際
boundary tether；三條原 root-contact 邊及唯一 spoke 給 K5。

該構造只用三個原接點、兩份拒絕 degree lists、r 的一條 spoke
及 C 內點完整 degree 四；沒有用 r degree 五、整張 G 在 b 下
minimal、另一分量個數或 b 的三色性。因此在本題每個 proper b 都有

\[
\boxed{|F_C(b)|\le1.} \tag{3}
\]

兩份原 unary 的禁色本來就至多一色。四個具名因素是原 spoke、
C、U、V；它們在每個拒絕列恰各禁一個不同色。

## 3. 每份固定原支援至少兩點

固定任一原分量 W∈{C,U,V}，選它的一條原 root-contact 邊。
完整 Σ edge-minimality 提供原 G 拒絕、刪該邊後接受的列 q。
刪邊 [解除整份原分量的禁色](c5_degree5_interfaces.md#3-刪除分量任一邊禁色全部解除)，
故 W 在 q 的 root 覆蓋中有私有色，F_W(q) 非空。由 §2 它是
singleton，固定其色後 W 的 degree lists 不可著色且處處 tight。
W 因而是 Gallai tree；原 spoke 使它同樣 K4-free。

記實際支援 A_W=N_B(W)。若 A_W=∅，S4 不變性與 |F_W|≤1
迫 F_W=∅，矛盾。若 A_W={b_j}，令 q(b_j)=a。固定 a 的色
置換只有 singleton {a} 能保持不變，故 F_W(q)={a}。

固定 r=a 時，W 的所有外鄰點都同色 a。若某點有兩個外鄰點，
會產生嚴格 list slack，與拒絕矛盾；所以每點至多有一個外鄰點，
完整 degree 四迫 deg_W≥3。但 K4-free Gallai tree 的末端 block
有 degree≤2 的非割點；singleton W 也不可能。故

\[
\boxed{|A_C|,|A_U|,|A_V|\ge2.} \tag{4}
\]

見證列可因分量而異；式 (4) 是對同一固定原支援的下界，不相加
不同列的染色負載。

## 4. 同一 spoke 切口與支援 envelope

對整張來源共同作 D₅ 搬運，使唯一 spoke 是 rb₀；目標完整 Σ
同時搬到 933／941 的某個 D₅ 像，所有原分量仍共用同一色框。
沿這條原 spoke 切開 disk，外框成為

\[
0,1,2,3,4,5\quad\text{其中位置 }0,5\text{ 都是原 }b_0.
\]

[共同 root 的相容 lifts](c5_independent_support_capacity.md#42-同一-root-的相容-lifts)
給三份包含原 A_W 的閉區間 I_W=[a_W,b_W]。沿切口的實際次序
排列後，0≤a₁<b₁≤a₂<b₂≤a₃<b₃≤5；正長度由 (4) 保證。
不同區間可共端點，其開框邊段不重疊。只為這個拓撲論證收縮原
分量及保留一條 root 邊；完整 relations 仍在原圖計算。

共有 **28 份有序區間三元組**，原 C、U、V 的全部 3! 個具名
位置都保留，共 **168 placements**。r 對 C 的其他兩条原接線
只會加強限制，忽略它們的額外幾何要求是必要放寬。

I_W 是包含實際稀疏支援的 envelope，**不是新增附件**。下面允許
F_W 依賴整條 I_W 的字面色序列；這比只依賴 A_W 更寬，因此包含
每個可能原來源，而不需要把整弧冒充原圖支援。

## 5. 同一原分量跨列的 S4 profile

固定 W 及其 envelope I。若兩列 b、b′ 在 I 上有相同 equality
pattern，便有一個全域色置換 π 把 b|_I 搬到 b′|_I。因 A_W⊆I，
π 同時搬運全部原 boundary 附件色；對 W 的完整染色逐點施 π，給
R_W(b′)=πR_W(b)，故

\[
F_W(b')=\pi F_W(b). \tag{5}
\]

同時 F_W(b) 必對固定 b(I) 的所有色置換不變。配合空／singleton
限制，若 I 只見一或兩色，非空 F 只能是某個已見色；若 I 至少見
三色，任一 literal 色 singleton 都可作必要選項。空集一直允許。
每個 equality class 選一個代表值，再用同一 π 搬到其他列。
未見色的置換 completion 不影響結果，因代表值已通過 stabilizer
檢查。這裡絕不逐列或逐分量把原接合改用另一份色框。

完整 Σ edge-minimality 使每份原分量至少在一列有非空 F，故排除
全十列都空的 profile。其餘 profiles 全部保留，沒有要求它們實現
degree lists、D 守恆、原附加接線或來源 topology；這是可驗證的
必要放寬。

對 168 placements，把三份 profile 代入式 (2)，直接重建全部十列
接受 mask。**146,496 次具名 profile 比較沒有任何一個 mask 等於**

\[
\{933,934,940,948,996\}\ \cup\ \{941,949,950,998,1004\}.
\]

甚至不需再檢查各因素的私有色 essentialness，就已得到空域。
每個真實來源必落在此必要域，故 `(3,1,1)` 整型排除。

## 6. 固定證書與重播

[Checker](../scripts/c5_excess_two_ternary_two_unary.py)及
[artifact](../artifacts/c5_excess_two_ternary_two_unary/observations.json)保存
28 個具名區間三元組、168 placements、各區間的局部 equality classes、
代表字面色、完整 transports、所有十列 profile codes，以及每個 placement
的完整 Σ histogram 與具名 profile 索引見證。全部比較另有 digest。
本域只存 root 禁色必要資訊，不宣稱存有完整原來源關係。

完整關係代數另外逐 tuple 核對：972-tuple 六接點 star 算子，全部
64 個 ordered ternary tuples、225 對非空 unary domains 及四個 spoke
色，共 **57,600 次 singleton relation 接合**；全部 2,016 個二元素
ternary relations 接全部 unary domains，共 **453,600 次完整接合**，
其中 274,050 次的 ternary 禁色容量至多一。二元素 relations 包含
不可寫成三個 marginals 乘積的例子。

任意原 R_C 的一般涵蓋由逐 tuple 恆等式
\(J(R_C,S_U,S_V)=\bigcup_{p\in R_C}J(\{p\},S_U,S_V)\)
及式 (2) 負責，沒有枚舉全部 2⁶⁴−1 個非空 ternary relations。
原 tuple 的完整內部染色由其原 relation 定義提供；抽象控制沒有
冒充 disk 來源。

```bash
python3 scripts/c5_excess_two_ternary_two_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_ternary_two_unary.py --check
python3 scripts/c5_single_spoke_three_one.py --check
```

本頁停止於此整型排除。其他 t=1 分拆、其餘 ε=2、兩個 degree-5
roots、一般出口與 K∞=K≤5 不由本頁解決；Python 空域證書及紙面
topology 均未新增 Lean 形式化。
