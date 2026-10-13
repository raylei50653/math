# N2 三點支援的相等分割定律與同列接回

**最新後續（2026-10-13）**：[一long來源排除](c5_excess_two_n2_one_long_closure.md)
以任意長末端block的原K₅及固定root完整外側接回，關閉完整原55 `(1,0)`。
合既有含U覆蓋，九格八格、完整目標只剩 `(2,0)`；父N2／E-ARC2仍OPEN。
以下舊日期的剩餘表與證據保留當輪語境。

**後續（2026-10-12）**：[兩接線 U 的全色 Diff 出口](c5_excess_two_n2_unary_diff_closure.md)
已排完整 `(ℓ,u)=(1,1)`：任意大小 U 的五形窮盡及原 K₅ 排除給同列完整接回。
本頁推論 UL 保留當輪必要 residual 語境；該含 U 來源現已全排。
完整目標原55只剩 u=0 的 `(1,0)`、`(2,0)`；九格仍七格，N2／E-ARC2 OPEN。

2026-10-12。凍結基準 HEAD：`8b76dcc82adabba679e7b0d2ef6dbe6eb9cc37f3`。
全部十二份輸入及 SHA 見
[BASE](../audits/2026-10-12-n2-boundary-partition-law/BASE.json)；完整來源契約沿用
[三列 diagonal §1](c5_excess_two_n2_diagonal_three_row.md#1-完整來源契約)，
實際 arc／低接點前提沿用 [long 同步](c5_excess_two_n2_long_synchrony.md)。
目前停止點見 [Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口)。
沒有來源枚舉、原圖替換、外部新定理、Lean theorem、commit 或 push。

**新的統一規律：固定同一原 piece 後，完整局部 fibre 只依實際接口上的具名相等分割，
差別至多是一個作用於整份 tuple 的共同顏色置換。** 因此任意大小、任意 root 接線數的
三點連續支援，diagonal 拒絕 mask 一律是 `∅ / Eq / Diff / I`。
兩個三點支援的接回可用一個 mask 覆蓋條件處理，不需對每份 cactus 或七個弧模板另證。
再以一條「已用色禁色至多一個」引理合用原55容量，排除三接線 U，並一起排除
原七個低接點同類弧模板。**完整 `(ℓ,u)=(1,1)` 的剩餘來源必為 `k_U=2`、
`M_U=∅`、`M_L=I`、`k_L≥4`；每列 U 恰禁止一個實際支援上的已用色。**
原55、完整 N2 及 E-ARC2 仍 OPEN。

## 1. 原資料與局部 fibre

固定原圖的一份 piece `C`，原頂點數字順序 `v₁,…,vₙ` 不改。令
`S_C=N(C)∩B` 是實際框支援，`R_C=N(C)∩{r,s}` 是實際 root 接口。
mixed 的兩個 roots 都在 `R_C`；unary 只有原 owner。令 `X_C=S_C∪R_C`。
局部約束邊恰為原圖所有至少一端在 `C` 的邊；没有添加接口之間的新邊。
對接口賦色 `η:X_C→[4]`，定義

\[
\mathcal F_C(\eta)=\{(f(v_1),\ldots,f(v_n)):
 f\cup\eta\text{ 滿足全部這些原邊的異色約束}\}.
\]

所有 tuple 都賦色全部原 `C`，空 fibre 亦保留。原 ordered/shared contacts、owner、
附件、rotation、bridges、旁支完全不動。框在 `S_C` 外的色不影響這個局部 fibre，
因為按實際支援定義沒有 `C` 到那些框點的邊；它們仍是全圖接回時的固定原座標。
若使用兩 roots 的 ambient 16-pin 格式，unary 的非 owner pin 仍保留為等值副本，
不把這個維度從原證書删除。

令 `ker η` 為 **具名接口點** 的相等分割：`x,y` 同一 block 當且僅當 `η(x)=η(y)`。
這不是 root 接點 incidence 的計數，也不是各色出現次數；接口標籤不能交換。

## 2. 完整 fibre 的分割定理

**定理 P（任意原 piece）。** 若 `η,η′` 是同一原 `X_C` 的賦色，而且
`ker η=ker η′`，存在一個 `[4]` 的顏色置換 `π`，使

\[
\eta'=\pi\circ\eta,\qquad
\boxed{\mathcal F_C(\eta')=\pi^{\times n}\mathcal F_C(\eta).}
\]

右式是完整 tuple 集合的相等，不只是非空性或 fibre 大小相等。
若某些接口點在兩賦色中都 pin 到同一字面色，`π` 可固定所有那些色。
若另要求固定尚未在接口出現的字面色，先附加對應的具名 constant anchors，
再要求包含 anchors 的相等分割相同。

*證明。* 相同分割給已用顏色間的雙射：把 `η(x)` 送到 `η′(x)`。
同一 block 的點不會產生不同像，不同 blocks 的顏色亦不會合併。
兩邊已用色數相同，故這個雙射可擴張為 `[4]` 上的置換 `π`。
原接口已固定的字面色按定義被送到自己；未用的固定 anchors 亦可保留。
置換保持且反映每一條原邊的異色，所以對每份原完整 lift 逐座標作用 `π`
得到另一份完整 lift。`π⁻¹` 是逆映射，故是精確雙射，包括兩邊皆空的情形。∎

定理不需平面、degree 四、cactus、Gallai、接點上界或有限圖形分類。
它比較的是同一原圖同一具名接口；不能用兩份不同 piece 有同一分割推斷 fibres 相同。

**定理 C（既有 slack 的分割表述）。** 若原 `C` 連通，每點在完整原圖 degree 四，
而某原 `v∈C` 的兩個不同實際外鄰在 `η` 下同色，則 `F_C(η)≠∅`。

*證明。* 對每點取原 degree list
\(L(w)=[4]\setminus\eta(N_G(w)\setminus C)\)。因原完整 degree 四，`|L(w)|≥d_C(w)`；
在 `v` 處外鄰重色使 `|L(v)|>d_C(v)`。取一棵以 `v` 為 root 的原 spanning tree，
依距離由遠至近貪婪染色。每個非 root 染色時尚有一個未染的 parent，
已染鄰居至多 `d_C(w)−1`；root 的已染鄰居至多 `d_C(v)<|L(v)|`。
逐點都有可用色，得到全部原 `C` 的完整 lift。singleton 同由 strict list 处理。∎

這是 [原分量解除 §2](c5_excess_two_arc_component_slack.md#2-刪一條分量邊與整份省略的精確投影)
的同色 slack；本輪把它接到完整 partition table，給出一個**必要拒絕濾條件**：
令 `K_C` 是接口上的輔助 graph，
其邊 `xy` 當且僅當某原 `v∈C` 同接兩個不同實際外鄰 `x,y`。
若 `η` 在任一 `K_C` 邊上同色，該 cell 必接受；所以

\[
\boxed{\mathcal F_C(\eta)=\varnothing
\ \Longrightarrow\ \eta\text{ 是 }K_C\text{ 的 proper 賦色}.}
\]

`K_C` 只記錄原外鄰相遇，不向原來源添加邊、不替換 piece，也不聲稱此必要條件充分。
例如 shared contact 使 `rs∈E(K_C)`，因此所有 diagonal cells 必接受。
令 `W_C^r` 是所有原 r-contacts 的實際框鄰居聯集；若 `x∈q(W_C^r)`，
就有 root／框外鄰同色，故 mixed 的完整 root-pair 拒絕集合必包含於

\[
([4]\setminus q(W_C^r))\times([4]\setminus q(W_C^s)).
\]

這是同一個原外鄰碰撞規律，可直接在第 3 節的 26 個完整 partition cells 上使用；
不得以聯集 `W` 取代原附件去反推所有接受 cells。

## 3. 三點弧：兩個 diagonal 測試與完整 26-cell quotient

固定實際支援恰為原連續三點 `A=(a,b,c)`。proper 框列使 `a≠b`、`b≠c`，
接口框色因此只有兩種具名分割：

\[
\text{Eq 型}:a=c\ne b,\qquad
\text{Diff 型}:a,b,c\text{ 兩兩異色}.
\]

在指定 `I={0,1,3}`、`q₀=01212`、`q₁=01202`、`q₃=01021` 上，未用色 `D=3`。
mixed 固定兩 root pins `(D,D)`；unary 固定原 owner `D`。
定義 `Eq(A)={i∈I:qᵢ(a)=qᵢ(c)}`、`Diff(A)=I\Eq(A)`。

**定理 D（任意大小、任意接線數）。** 在同一 Eq 型內，所有指定列的完整 diagonal
fibres 由一個固定 `D` 的顏色置換雙射；Diff 型內亦然。因此存在兩個原 piece 的
拒絕位元 `z_C^=,z_C^≠∈{0,1}`，使

\[
m_C(i)=z_C^=\mathbf1_{i\in Eq(A)}+
z_C^\ne\mathbf1_{i\in Diff(A)},\qquad
\boxed{M_C\in\{\varnothing,Eq(A),Diff(A),I\}}.
\]

*證明。* 相同型的支援分割相同；全部 root 接口都另 pin 到 `D`，而 `D` 不在支援上。
定理 P 給固定 `D` 的雙射。空／非空只能按兩種類型變化。∎

同一論證亦適用任一 proper 框列及一個不在該列出現的 pin 色；以共同顏色置換
把該 pin 色送回代表 `3` 即可。故兩個拒絕位元實際是同一原 piece 的局部規律，
不限於這三份指定列。這不准許略去某列的其他原 pieces 或 external factor。

兩個代表測試可取支援 `010`、`012`，兩 roots 同 pin `D=3`。只要保存那兩格的
**完整原 tuple 集合**及實際 `π`，便能恢復指定三列的完整 diagonal fibres。
這是證明支援型決定 fibres；並非從兩份有限控制外推所有 piece。

完整 off-diagonal 亦有有限而與 `|C|,k_C` 無關的接口規律。對 mixed：

- Eq 支援規範為 `010`。穩定它的置換只有未用色 `2↔3`；16 個 ordered root pins
  分為 10 個軌道，代表可取 `00,01,10,11,02,12,20,21,22,23`。
- Diff 支援規範為 `012`。剩餘色只有 `3`，穩定群平凡，所以要保留全部 16 個 pins。

故 **26 份具名相等分割代表完整 mixed 16-pin fibres**；unary 則是 Eq 的
owner pins `0,1,2` 三類，加 Diff 的四個 pins，共 **7** 類。
上述 26／7 是顏色對稱的代表 cell 數；某些原 piece 可再有等值 cells 或空 cells，
本定律不預先合併它們。重建各字面 cell 時，對原 tuple 的每一座標使用同一 `π`，
並還原原 root pin、框支援與全部 ambient 副本。不能只保留 projected marginals。

## 4. 全圖的唯一接回條件

固定同一原列 `qᵢ` 及同一 ordered pins `(x,y)`。各原 piece 的完整 tuple 座標互斥，
共同接口仍是字面 `B,r,s`；全部 root spokes 與其他接口邊形成 external factor。
令 `F_ext(i,x,y)` 是該 factor 的異色約束。原全圖完整 fibre 恰為

\[
\boxed{\mathcal F_G(q_i;x,y)=
 \begin{cases}
 \displaystyle\mathop{\Join}_{C}\mathcal F_C(q_i|_{S_C};x,y),&F_{ext}=1,\\
 \varnothing,&F_{ext}=0.
 \end{cases}}
\]

`Join` 把各份 **同列、同 pins** 的完整 tuples 按原頂點順序拼回。
此式的兩方向都直接成立：完整全圖 lift 限制到每個原 piece；反向地，選各 cell
一份完整 lift，再加已固定接口，覆盖全部原邊且沒有漏掉交界约束。

對分割代表所用的 local `π`，只可先重建某個共同目標 `qᵢ,x,y` 的 cell，再作上式。
不能把不同列／不同 pins 的非空代表直接相乘，也不能把各 piece 獨立正規化的框列
當成一份共同全圖框列。定理 P 本身不給不同 `qᵢ` 的全圖 lift 雙射。
若要直接搬運一份完整全圖 lift，必須有**同一個** `π` 同時搬運整个 `B,r,s`
及全部 pieces。

在指定列的 `(D,D)` 下，root-spokes 自动合法。已採納 short diagonal 定理给
short 的完整 lift。因而本題的 diagonal 接回完全等價於

\[
\boxed{\exists i\in I:\ i\notin\bigcup_{C\text{ 要求 diagonal 的原 pieces}}M_C.}
\]

這是一個共同覆盖不變量；各份 mask 非全 `I` 不足以推出它。

## 5. 兩份盾弧的統一幾何與七模板來源

在完整 `(ℓ,u)=(1,1)` 原契約中，U／long／short 的盾弧長 `(2,2,1)`。
令 U 與 long 的兩個邊互斥三點弧為 `A=(a,b,h)`、`L=(h,c,d)`。
它們覆蓋原 C₅ 的四條邊，剩餘原邊是 `da`。

**引理 A（所有 proper 框列）。** `Eq(A)∩Eq(L)=∅`。

*證明。* 若一列同時有 `q(a)=q(h)` 及 `q(h)=q(d)`，便有 `q(a)=q(d)`，
違反剩餘原框邊 `ad` 的 proper 異色。∎

不需按五份弧 pair 分別證明。結合定理 D，U／long 的 diagonal 判準只剩
`M_U∪M_L≠I`。若两份皆非空且非 `I`，一般布林公式為：

| 兩份 mask 類 | 覆盖 `I` 的充要條件 |
| --- | --- |
| Eq／Eq | `Eq(A)∪Eq(L)=I` |
| Diff／Diff | `Eq(A)∩Eq(L)=∅` |
| Eq(A)／Diff(L) | `Eq(L)⊆Eq(A)` |
| Diff(A)／Eq(L) | `Eq(A)⊆Eq(L)` |

本題五個三點弧在 `I` 都有非空 Eq set；引理 A 使兩個 Eq sets 不相交。
因此**任意接線數**下，只要 U／long 的实际非空 masks 一 Eq、一 Diff，便有同列出口：
選 Diff-mask piece 所在弧的一份 Eq 列，它與另一弧 Eq 列互斥，兩份均接受。
這把原低接點混類排除提升為只依 actual mask 類的任意接線數條件定理；
它不聲稱任意高接點 long 必屬 Eq／Diff。

Eq／Eq 的 remaining 條件是兩個 Eq sets 並集覆盖指定 `I`。
Diff／Diff 在兩邊弧邊互斥時**必定**覆盖；甚至對所有 proper、至多三色的原框列，
只要各 piece 的拒絕型確實是 Diff，任何共同未用色的 diagonal 都失敗。
這是通往 off-diagonal／拓撲的明確界線，不能靠增加 diagonal 框列解除。

原七模板是這個单一條件在 `I` 上的字面 instances：Eq／Eq 的兩份覆盖 pair、
Diff／Diff 的五份邊互斥 pair。七模板不是七份可實現原來源，也无需七份專門證明。
它們是共同幾何加一個相等分割覆盖式的輸出；以下一條容量引理將它們一起排除。

## 6. 已用色禁色規律與原七模板的統一排除

固定一份 proper 三色框列 `q`，令 `T=q(B)`，故 `|T|=3`。
對 unary U 令 `F_U(q)` 為使原 U 沒有完整 lift 的 owner 色集合。
局部引理使用：U 連通，每點完整 degree 四，原 blocks 為 bridges／奇環，
`2≤k_U≤3`；多 block 時每個 leaf block 有私有 owner-contact；
每奇環至多一個普通私有點；各點框附件至多相鄰兩點；actual support 至少三點。
這些都是完整來源已採納的原圖結論。附件單射在後述三點弧分類接入時使用，
不需要把它額外加入這條已用色引理。

**定理 U（任意大小的已用色禁色上界）。**

\[
\boxed{|F_U(q)\cap T|\le1.}
\]

*證明。* 先由原 block-tree 的接線計數知每奇環長度至多 `1+k_U≤4`，
因此都是 triangles：對某環上的每個 U 割點，選其環外分支的 leaf 私有 contact；
这些 contacts 互異，且與環內私有 contacts 互斥，普通私有點至多一個。
此計數與 owner pin 色無關。

反設兩個不同已用色 `x,y∈F_U(q)∩T`，第三已用色記為 `z`。
定理 C 迫所有 contacts 的框附件避開 x、y，因此只能取色 z。
每個原拒絕 pin 下的 degree lists 都 tight，且原 Gallai block palettes 的互斥聯集
等於各點 list；這裏沿用 [既有 degree-list 輸入](c5_excess_two_n2_diagonal_three_row.md#1-完整來源契約)。

leaf bridge 的私有端必是 contact；其完整 degree 四迫接兩個相鄰框點，
兩個 proper 框色不能都為 z，故 leaf bridge 不存在。
leaf triangle 的兩個私有點若只有一個 contact，另一個普通點的二色 list
不依 owner pin，故 cycle palette 在 x、y 兩個拒絕下須相同。
但 contact 的一個實際框附件取色 z，其 lists 分別為 `[4]∖{x,z}`、
`[4]∖{y,z}`，二者不同且各等於該 cycle palette，矛盾。
所以每個 leaf triangle 至少有兩個私有 contacts；多 block tree 有至少兩個
leaf blocks，就需要至少四 contacts，違 k_U≤3。

单 block 的 singleton 不能有 k_U≥2；bridge 同上。
triangle 若有普通私有點，仍由固定普通 list 排除兩個禁色；
若三點全為 contacts，它們的實際框附件全取 z，故 actual support 包含於
一個 q 色類。proper C₅ 的色類至多兩點，違 support 至少三點。∎

**推論 U3（完整來源只有兩接線 U）。** u=1 的完整 N2 原55來源中，`k_U=2`。

原 degree5／兩 mixed 接線給 `k_U∈{2,3}`；
[共同原55容量](c5_excess_two_n2_residual_unification.md#2-三族共享的不變量與一條共同容量引理)
在每個 i∈I 給 `k_U−|F_U(q_i)|≤1`。
採納的 unary 三列出口給某 i 的 `D∉F_U(q_i)`。
該列全 B 的唯一未用色是 D，故全部禁色都是已用色，定理 U 給 `|F_U(q_i)|≤1`。
k_U=3 則容量要求 `|F_U(q_i)|≥2`，矛盾。
這裏比較的是**同一列、同一份完整 F_U**，沒有把各列容量相加。

**推論 UL（完整 `(1,1)` 的共同剩餘合同）。**

\[
\boxed{k_U=2,\quad M_U=\varnothing,\quad M_L=I,\quad k_L\ge4,}
\qquad
\boxed{F_U(q_i)=\{c_i\},\ c_i\in q_i(S_U)\quad(i\in I).}
\]

*證明。* 由推論 U3 得 k_U=2。U 在 `(1,1)` 的 actual support 是三點弧 A。
若 M_U 非空，已採納 [M-LOW-ARC](c5_excess_two_n2_long_synchrony.md#4-含-u-的兩邊弧-mask-分類與同步)
的 k=2 部分迫原 U 是單 bridge，兩個 contact 端各附 A 的一條不同框邊。
取任一 Diff(A) 列；它非空。在這列，任何支援上已用 owner 色都與某端框附件
同色，定理 C 給完整 lift；未在支援上出現的 owner 色則使兩端 singleton lists
為兩條邊的不同缺色，亦可染。故該列 `F_U=∅`。
完整來源的 `G−U` 全收，任取其該列完整外部染色並固定 owner，U 的 full lift
就接回原 G，違原拒絕。這個排除不限制 L 的接線數。

因此 M_U 空；原 short 的 M 亦空，所有 root spokes 在 `(D,D)` 合法，
原 G 三列拒絕便迫 M_L=I。低接點 long 出口排 k_L≤3。
容量給每列 `|F_U|≥1`；D 已接受，定理 U 使 `|F_U|≤1`，所以恰一個已用禁色。
若該色不在 U 的 actual support 色集合，交換它與 D 而固定支援各色，
定理 P 將 D 的完整 lift 搬到此色，矛盾。因此禁色在 qᵢ(S_U) 上。∎

原七模板因此一起排除。這是原源 `k_U=3` 的共同容量矛盾及 k_U=2 的既有
分類後果，不是七份專門證明。即使 k_L≥4，只要 U 的 M 非空也同時排除。
剩餘 L 不可能有 shared contact，也不可能是全部 root contacts 都為原 C 葉的 tree，
否則既有出口與 M_L=I 矛盾。因此它須含 cycle 或某個 C cutpoint 接 root。
L 的 I 類及 U 的每列單一已用禁色仍須完整 off-diagonal 同列接回或來源拓撲矛盾。
原 root degree 計數 `10=k_U+k_L+k_S+t`、k_U=2及k_S≥2另給 **`4≤k_L≤6`**。
以r為U owner時，原 ordered incidences 還有 `1≤k_L^r≤2、1≤k_L^s≤4`。
這是原接線的必要範圍，不限制原L頂點數，不把它當作來源有限枚舉。

## 7. 高接點障礙與精確停止點

凍結的四-contact path 控制 `p₀–p₁–p₂–p₃`，原附件依次 `01、0、2、12`，
前兩點接 r、後兩點接 s，支援正好 `012`，其 `M_C=I`。
這和定理 D 完全相容，且指出 `I` 不能從任意接點定律排除。
該控制的完整 degree 四、無 shared contact、框邊附件單射均成立；它不是完整
Σ933／941 disk N2 來源。以它否定的是「只靠這些局部前提必有 diagonal escape」的泛化。

本輪紙面結果及剩餘義務：

- 任意原 piece 的具名分割→完整 fibre 雙射；三點支援任意 k 的四類 mask；
  mixed 26／unary 7 代表 cells；degree 四的外鄰同色→完整 lift；
  同列同 pins 的精確 full-lift join，均已由初等論證證明。
- `(1,0)` long 的任意大小 diagonal 出口問題可统一成兩個代表 cells
  **不得同時為空**，條件是 long 實際支援為三點弧；short 同列接回已採納。
  支援四／五點的 long 仍用定理 P 的完整具名分割，不能套兩位元。
  局部 path 表明不得同空這句尚需來源拓撲／criticality。
- `(1,1)` 全部 diagonal 同步可统一成一个 coverage 条件；§6 已排全部低接點
  同類模板及任意 k_L 的 M_U 非空子域。剩餘必滿足推論 UL；
  high-contact L 的 I 類須完整 off-diagonal joint 或原來源拓撲矛盾。
- `(2,0)` 同一列兩 long 的 mask 聯集亦用同一條件；各自有 escape 不等於共同 escape。
  三點支援的完整 off-diagonal 問題應使用原 26-cell partition fibres 做同一列 join；
  更長支援仍保存完整具名接口分割。

有限控制可校準上述双射及原 tuple 重建，不能替代這些無界初等證明。
完整 target 來源仍 `not triggered`；本輪新來源子域排除由無界紙面證明承擔，
沒有新增來源圖搜尋、大小下界、Δ 門檻或父 closure。九格仍七格已有覆蓋。
一般原55、完整 N2、N1／相鄰／單-root例外、E-ARC2、一般出口及 K∞=K≤5 維持 OPEN。

## 8. 完整控制、獨立審查與重播

紙面分割推導見 [paper](../audits/2026-10-12-n2-boundary-partition-law/paper/REPORT.md)，
已用色／容量推導見 [第二作者報告](../audits/2026-10-12-n2-boundary-partition-law/review/REPORT.md)，
其無界量詞及來源接回經 [獨立審查](../audits/2026-10-12-n2-boundary-partition-law/review/independent_review.md)
核對。分割作者對自身 P／C／D 的重讀另明示，不稱為第二作者獨立證明；根 agent 亦逐原邊
核對分割雙射、leaf 計數、同列容量及完整接回。外部 degree-list 信任鏈沿用已採納報告，
本輪沒有新增外部定理或 Lean theorem。

[固定控制](../audits/2026-10-12-n2-boundary-partition-law/controls/REPORT.md)只重算保存的原資料：

| 核對 | 實際範圍 |
| --- | --- |
| 228份原分量 | 36,480完整cells，106,760原tuples；含3,643空cells，完整置換雙射一致 |
| 65份固定圖 | 10,400同列同pins完整joins及650完整global rows，獨立DFS一致 |
| 外鄰同色 filter | 24,715 cells `triggered and holds`，11,765 `not triggered`；未觸發不推拒絕 |
| 三點完整接口 | 每弧160個ambient cells按色名對稱合成26類；保留tuple置換及凍結來源指標 |
| 已有800附件控制 | 重算四個equal pins的完整lifts，已用禁色上界零違反；不是新来源搜尋 |
| 已用禁色引理局部觸發 | 228原分量中89份符合全部前提；445三色列 `triggered and holds`，341交集空、104單一禁色 |
| 更強說法的負控制 | 10份局部控制每列F_U非空；顯示不能把D出口當成全色出口 |
| 完整N2 target | `not triggered`；有限控制不承擔無界來源排除 |

具名負控制 `triangle 7,8,9 + 7–10–11`，contacts為8,9,11，框附件依次
`7→0、8→2、9→2、10→01、11→12`；三列禁色為 `{0}、{0}、{2,3}`。
它满足上述局部度數／block／支援條件，但在 Diff 列 `k−|F|=2`，違完整來源容量。
其 unary 解讀另有 K₅ minor；故不是 full disk source 反例。
新引理只限制**已用**禁色至多一個，恰能與容量合用；不要求全色禁色表有空列。
完整十列四owner及原mixed十列16-pin fibres、空cells與負控制均保存於
[probe](../audits/2026-10-12-n2-boundary-partition-law/review/equal_pin_full_probe.json)。
[補充局部前提校準](../audits/2026-10-12-n2-boundary-partition-law/controls/PAPER_REPORT.md)
保留實際ownership並獨立算blocks／leaves／完整度數；89份觸發中42份為原unary，
47份是兩個原roots同pin下的局部lists查詢，沒有合併roots後推回來源。
所有2,280列禁色及9,120完整equal-pin cells保留；完整target仍未觸發。

```bash
python3 -B audits/2026-10-12-n2-boundary-partition-law/controls/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-12-n2-boundary-partition-law/controls/checker.py --check
python3 -B audits/2026-10-12-n2-boundary-partition-law/review/equal_pin_probe.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-12-n2-boundary-partition-law/review/equal_pin_probe.py --check
python3 -B audits/2026-10-12-n2-boundary-partition-law/controls/paper_controls.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-12-n2-boundary-partition-law/controls/paper_controls.py --check
python3 -B scripts/check_docs.py
python3 -B tools/docgraph --include 'docs/**/*.md' check
lake build
git diff --check
```

實際重播與 hashes 見 [本輪 receipt](../audits/2026-10-12-n2-boundary-partition-law/verification.json)。
未重跑上游N45／44／SD-A／ES／ER生成、來源rotation或全工作樹DocGraph。
既有Lean build不形式化本頁紙面推導。本輪沒有commit／push。
