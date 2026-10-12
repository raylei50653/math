# N2 三點支援的相等分割定律與同列接回

**同輪後續採納（2026-10-12）**：本稿是最初的接口論證，以下「七模板仍OPEN／未新增
來源排除」保留當時範圍。另一作者其後證已用色禁色上界，合原55容量排三接線U，
並將七模板一起排除；完整證明及共同剩餘合同以
[canonical §6](../../../docs/c5_excess_two_n2_partition_rule.md#6-已用色禁色規律與原七模板的統一排除)
及 [獨立審查](../review/independent_review.md)為準。
本稿§6的(1,0)兩代表cells／26-cell化約限於三點實際支援；四／五點須用完整具名分割。

2026-10-12。凍結基準 HEAD：`8b76dcc82adabba679e7b0d2ef6dbe6eb9cc37f3`。
全部十二份輸入及 SHA 見 [BASE](../BASE.json)；本報告只讀
[凍結 long 同步報告](../frozen/docs/c5_excess_two_n2_long_synchrony.md.snapshot)及其直接契約。
沒有來源枚舉、原圖替換、外部新定理、Lean theorem、commit 或 push。

**新的統一規律：固定同一原 piece 後，完整局部 fibre 只依實際接口上的具名相等分割，
差別至多是一個作用於整份 tuple 的共同顏色置換。** 因此任意大小、任意 root 接線數的
三點連續支援，diagonal 拒絕 mask 一律是 `∅ / Eq / Diff / I`。
兩個三點支援的接回可用一個 mask 覆蓋條件處理，不需對每份 cactus 或七個弧模板另證。
這個定律保留完整 fibres，也精確顯示為何高接點的 `I` 類及同類 masks 仍是障礙；
它沒有完成 N2 原55或 E-ARC2。

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

**定理 C（外鄰同色必有完整 lift）。** 若原 `C` 連通，每點在完整原圖 degree 四，
而某原 `v∈C` 的兩個不同實際外鄰在 `η` 下同色，則 `F_C(η)≠∅`。

*證明。* 對每點取原 degree list
\(L(w)=[4]\setminus\eta(N_G(w)\setminus C)\)。因原完整 degree 四，`|L(w)|≥d_C(w)`；
在 `v` 處外鄰重色使 `|L(v)|>d_C(v)`。取一棵以 `v` 為 root 的原 spanning tree，
依距離由遠至近貪婪染色。每個非 root 染色時尚有一個未染的 parent，
已染鄰居至多 `d_C(w)−1`；root 的已染鄰居至多 `d_C(v)<|L(v)|`。
逐點都有可用色，得到全部原 `C` 的完整 lift。singleton 同由 strict list 处理。∎

這給完整 partition table 一個**必要拒絕濾條件**：令 `K_C` 是接口上的輔助 graph，
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
它們是共同幾何加一個相等分割覆盖式的輸出。

## 6. 高接點障礙與精確停止點

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
  **不得同時為空**；short 同列接回已採納。局部 path 表明這句尚需來源拓撲／criticality。
- `(1,1)` 全部 diagonal 同步可统一成一个 coverage 条件；不同非空 Eq／Diff 類
  任意 k 同列接回已證。高 k 的 `I` 類、低 k 同類 coverage 仍需完整 off-diagonal
  joint 或原來源拓撲矛盾。
- `(2,0)` 同一列兩 long 的 mask 聯集亦用同一條件；各自有 escape 不等於共同 escape。
  完整 off-diagonal 問題應使用原 26-cell partition fibres 做同一列 join。

有限控制可校準上述双射及原 tuple 重建，不能替代這些無界初等證明。
完整 target 來源仍 `not triggered`；沒有新增來源排除數、大小下界、Δ 門檻或父 closure。
一般原55、完整 N2、N1／相鄰／單-root例外、E-ARC2、一般出口及 K∞=K≤5 維持 OPEN。
