# ε=2：t=1、(2,1,1,1) 的整型來源排除

2026-10-03。接續 [兩原 unary 省略排除](c5_excess_two_single_spoke_two_unary.md)。
**933／941 固定完整 Σ 的 edge-minimal C₅ disk 來源，若 ε=2、唯一
degree-6 root r、t=1，則不可能有原接點分拆 (2,1,1,1)。**
本輪排除整型來源；不以「沒有全 degree-4 真子核心」代替這個結論。
證據為任意大小紙面化約及 Python 必要域證書，未新增 Lean theorem。

## 1. 原來源與完整六接點

G 有限簡單，B=(b₀,…,b₄) 是指定有序 induced-C₅ disk 外框，完整
Σ 為 933、941 或整圖 D₅ 像。每條非框邊 e 滿足 Σ(G−e)⊋Σ(G)。
有效內部 H 連通，r 完整 degree 六，其他內點完整 degree 四。唯一
原 spoke 為 rb_s；H−r 的原分量為 binary A 及 unary U₀、U₁、U₂，
有序原接點分別為 (x,y)、u、v、w。全部原邊、實際附件、ownership、
環序及同一嵌入保持。

固定同一字面 proper boundary coloring b，原完整 relations 記為
R_A(b;x,y)、S₀(b;u)、S₁(b;v)、S₂(b;w)。每份皆由接點 slack 及
生成樹逆序貪婪非空。完整接合恰是

\[
\mathcal R_G(b)=\{(a,c,d,e,f,g):(c,d)\in R_A(b),\ e\in S_0(b),
\ f\in S_1(b),\ g\in S_2(b),\ a\notin\{b_s,c,d,e,f,g\}\}.\tag{1}
\]

記 F_A=∩_{(c,d)∈R_A}{c,d}，Fᵢ=Sᵢ 當 |Sᵢ|=1，否則 Fᵢ=∅。
式 (1) 的 root 投影為 U₄∖({b_s}∪F_A∪F₀∪F₁∪F₂)。這只用於
此原 root 接合，不以禁色集代替一般完整 relation，也不拆 binary marginals。

## 2. 四份固定支援皆有正跨度

每份原分量 C 的任一原接點邊有 Σ-minimality 見證列 q。G−e 的
新染色給 root 色 a，而 G 拒絕 q，因此 a∈F_C(q)。其他原因子在
這個 a 下全部可填，故 C 有一個私有禁色。q 必為 singleton 列。

固定 r=a 後，C 不可染，各 list 至少為 deg_C。沿用
[degree-list／解除引理](c5_degree5_interfaces.md#3-刪除分量任一邊禁色全部解除)，
C 為 tight Gallai tree。原 spoke 使 B∪{r} 連通，故沿用
[外部 hub 的 K₄ 排除](c5_degree5_tree_components.md#1-連通外框排除-degree-4-分量的-k4)，
C 是 K₄-free；這一步不要求全圖是 minimal q-core。

令 S_C=N_B(C) 為全部實際支援。若 S_C 空，S₄ 對称排除容量至多二
的非空 F_C。若 S_C 只有一個框點，固定其色 d 的 S₃ 穩定子迫非空
F_C={d}。再固定 r=d，tightness 使每點最多有一個外鄰，否則同色
外鄰產生 slack；因此 min deg_C≥3。K₄-free Gallai tree 的末端
block 有內度至多二的非割點，singleton C 亦不可能，矛盾。

所以四份固定原支援均至少有兩點。[同一 root 相容 lifts](c5_independent_support_capacity.md#42-同一-root-的相容-lifts) 給共同框弧
I_C，原支援包含於其中、開邊段互斥，且

\[
1\le\ell_C,\qquad \sum_C\ell_C\le5.\tag{2}
\]

故只有四份皆跨度一，或唯一一份跨度二、其餘皆一。沒有將弧上點
新增為原附件；較大弧只作支援包絡。

## 3. 短 binary 不可能有兩禁色

若 A 的弧跨度一，其 actual support 恰為一條原框邊的兩端 {b_i,b_j}。
反設任一 proper b 有 |F_A(b)|=2。沿用
[任意列的原 bridge 路徑及逐塊 residual](c5_single_spoke_frame_arc.md#2-任意列的逐塊-residual-穩定子)，
兩原接點間有奇數長原 bridge 路徑 P；刪 P 邊得到含全部旁支的原
路徑塊 W_k，其 residual 都是同一二元集 F_A(b)。每塊實際支援
T_k⊆{b_i,b_j} 的逐色穩定子必保持該二元集。空支援或單點支援的
穩定子不保持任何二元色集，所以每個 W_k 都實際接到 b_i、b_j。

來源拒絕不只一列且接受 T4，[未接內點引理](c5_unattached_boundary.md)
迫整份 G 實際碰齊五個框點。故另有 b_h∉{b_i,b_j} 經原 spoke 或
另一原分量接到 r，得到避開 A、內部避開 B 的原路徑 L。取 P 上
相鄰兩塊 W_k、W_{k+1}，以 {b_i}、{b_j} 及連通補弧 B∖{b_i,b_j}
作三份框弧；後者由 L 接回 r。[原路徑 frame-arc K₅ 引理](c5_single_spoke_frame_arc.md#3-三段框弧與任意兩塊的-k5-引理) 給五個
不交連通 branch sets 及十對原邊鄰接，與 disk 平面性矛盾。

所以短 binary 在**全部十列**都只有空／singleton F；短 unary 本來
亦然。固定框邊兩端在 proper b 中異色，交換未見兩色排除未見色
singleton；沿全部原分量同時換色，F 在十列必始終為空，或始終是
同一個具名端點的顏色。Σ-minimality 的私有色見證排除恆空。
因此每個短分量在全部十列都選擇自己的固定左／右原框端點色。

## 4. 唯一長支援的兩種位置

四份都短時，它們與 spoke 只禁 boundary 已用色；每個三色列的
未用色 D 都存活，與來源有拒絕列矛盾。

若唯一長分量是 unary，另三份短分量及 spoke 均不能禁 D。因此每個
拒絕 singleton 列都須由這份**同一原 unary** 禁 D。穩定子迫其實際
支援看見該列全部三色，故唯一固定長度二包絡 I={b_j,b_{j+1},b_{j+2}}
必為 rainbow。三色 C₅ 列在連續三點 rainbow，恰當其 singleton
位置落在該三點。933 的四個拒絕位置、941 的 {0,1,3} 及其 D₅ 像
均不包含於任一連續三點，矛盾。不需另用 unary D 守恆。

只剩唯一長分量是 A。共同旋轉**整張來源**，令 I_A=012，其餘
三份原 unary 按原環序命名，actual supports 恰為 23、34、40。
每份固定選自己的兩端之一，共 2³=8 份具名選擇。spoke 放寬為
任一 s∈{0,…,4}；未強加全部實際嵌入對 spoke 的額外限制。

A 的實際支援可以稀疏；以包絡 012 決定原 boundary lists 的換色
只會放寬必要條件。局部 proper pattern 只有 ABA、ABC 兩種。
同圖完整 R_A 的 S₄ 搬運迫 F_A 由各局部型的一份固定集合決定：

| 局部字面代表 | 容量至多二且受穩定子保持的 F_A | 數目 |
| --- | --- | ---: |
| 010 | ∅、{0}、{1}、{0,1}、{2,3} | 5 |
| 012 | 全部大小至多二的四色子集 | 11 |

同一局部型的不同列全部由**同一份**集合搬運；不逐列自由挑 F_A，
也不對分量獨立正規化。兩型共 55 份 profiles。將每份 profile、
三份具名端點選擇、spoke 代入式 (1) 的精確 root 投影，全部
**55×8×5=2,200** 份完整十列 masks 均不在 933／941 的十個 D₅ 像中。
必要域已空，故 (2,1,1,1) 整型來源不存在。

## 5. 證書與重播

[Checker](../scripts/c5_excess_two_binary_three_unary.py) 及
[artifact](../artifacts/c5_excess_two_binary_three_unary/observations.json)
保存五份正跨度型、55 份共同色框 profiles、全部 2,200 份比較及
50 份固定 unary 弧排除見證。所有 profiles 保留三份原 unary 身份、
具名端點及 spoke；未宣稱 profiles 都可由圖實現。

完整六接點代數控制含 16 份 singleton binary relation 與全部 15³
非空 unary domains，共 54,000 份；另 120 份二 tuple binary relation
與全部 4³ unary singleton assignments，共 7,680 份。每份核對
完整 tuples、逐 binary tuple 的聯集恆等式、root 投影及四種 spoke
限制，共 **61,680** 份完整接合、246,720 份 spoke 限制。
這些抽象 relation 控制不宣稱 actual disk 實現；一般非空 R_A 的涵蓋
由式 (1) 對原完整 tuples 的集合等式承擔。

```bash
python3 scripts/c5_excess_two_binary_three_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_binary_three_unary.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

任意大小及原 bridge／K₅ 涵蓋沿用上述紙面依賴與外部 degree-list
定理，Python 只核對新有限必要域，未重證全部歷史拓撲或新增 Lean。
本頁只排除指定整型；其餘 t=1／ε=2 分支及共同下界以現行導覽為準。
