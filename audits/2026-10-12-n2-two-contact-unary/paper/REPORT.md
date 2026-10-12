# N2 原55：兩接線 unary 的全 owner 色出口與原 K₅ 排除

2026-10-12。權威輸入為本 audit 的 [BASE](../BASE.json) 及逐份凍結的
`../frozen/`；基準 HEAD 為 `8b76dcc82adabba679e7b0d2ef6dbe6eb9cc37f3`。
本稿是任意大小紙面推導；有限附件校準不承擔窮盡性或來源排除。
不替換原 piece、不省去 tuple 座標，不變動 ordered contacts、ownership、
actual attachments、rotation、bridges、旁支、原框及完整 fibres／空 cells。

**新局部結論 U2-DIFF-ALL：** 若一份原 planar unary U 有恰兩條 owner 接線，
actual support 恰為原連續三點 `A=(a,b,c)`，並滿足下列已採納原圖結構，
则在 A 三色互異的任何 proper 原框賦色 q 下，**每個 owner 色都有 U 的完整 lift**：

\[
\boxed{q(a),q(b),q(c)\text{ 互異}\quad\Longrightarrow\quad F_U(q)=\varnothing.}
\]

**完整來源推論：** 凍結 partition report §6 已把 `(ℓ,u)=(1,1)` 收窄為
`k_U=2`、`S_U=A`、每列 `F_U(q_i)` 是一個支援已用禁色。五個三點弧均在
`I={0,1,3}` 有 Diff 列，與本定理矛盾。等價地，在任一 Diff 列先取原
`G−U` 的完整外部染色，再以該份染色的原 owner pin 接回全部原 U，即得原 G
的完整 lift。故這個完整原55格可排除。`(1,0)`、`(2,0)`、完整 N2、原55及
E-ARC2 的父問題仍 OPEN。本稿沒有新增外部定理或 Lean theorem。

## 1. 精確局部前提與已採納信任鏈

U 是原 `H−{r,s}` 的一份完整 unary 分量，owner 記 r。使用的局部前提如下：

1. U 有限簡單且連通，`k_U=|N_U(r)|=2`，不接另一原 root；每個原 U 點
   在完整原 G 的 degree 恰四，外鄰恰為原 owner（若是 contact）與 actual 框附件。
2. 原 U 的 blocks 是 bridges／奇環；若有多個 blocks，每個 leaf block 有
   私有 owner-contact。每個奇環至多一個普通私有點，指不是 U 割點且不接 r。
3. 每點的框附件至多是相鄰兩點，actual support 恰是 `S_U={a,b,c}`，其中
   `ab,bc` 是原 C₅ 的兩條連續框邊。
4. 原 `d_H(v)=2` 點的实际框邊附件，在同一原 H 中單射。
5. 原 G 平面；沒有只假設抽象 attachment table 可平面實現。

凍結來源依賴為 `c5_excess_two_n2_diagonal_three_row.md` §1、
`c5_excess_two_arc_spoke_closure.md` §§2–3、
`c5_excess_two_arc_size_bound.md` §§2–4 及
`c5_excess_two_n2_unary_three_row_escape.md` §1。
`c5_excess_two_n2_partition_rule.md` §6 提供完整 `(1,1)` 的 `k_U=2` 與
三點弧支援，而本稿不假設尚未解決的 E-ARC2。

外部 degree-list 輸入只沿用已採納的 Dvořák 2018 Lemma 7／Theorem 10：
不可染的連通 degree assignment 是 tight；lists 等於 incident 原 Gallai block
palettes 的互斥聯集。橋 palette 大小一，奇環 palette 大小二。
本輪沒有把本稿五形窮盡或 K₅ minor 歸稱外部定理的原文。

若 q 固定原 B，owner 固定色 d，原 U 的 lists 是

\[
L_d(v)=[4]\setminus\bigl(q(N_B(v))\cup\{d:rv\in E(G)\}\bigr).
\]

因完整 degree 四，`|L_d(v)|≥d_U(v)`。若某兩個不同實際外鄰同色，該點有
strict slack；沿以此點為根的原 spanning tree 逆序貪婪即可染全部 U。
所以任何拒絕 pin 使所有 lists tight，並可使用上述 block palettes。
這裏的 list coloring 是全部原 U 頂點的賦色，精確等於原局部完整 lift。

## 2. 任意大小原 U 的五形窮盡

**引理 S（結構，與 owner pin 無關）。** 在前提 1–4 內，原 U 恰為下列五形之一：

| 原 U 形狀 | 原頂點數 | U 中的 H 內度二點 |
| --- | ---: | --- |
| 單 bridge，兩端皆 owner-contact | 2 | 兩個 contact 端點 |
| 單 triangle，兩個 contacts、一個普通點 | 3 | 普通點 |
| leaf triangle 加一條 leaf bridge | 4 | triangle 普通點、bridge contact 端 |
| 兩個 triangles 共享唯一割點 | 5 | 每個 triangle 的普通私有點 |
| 兩個 triangles 由一條 bridge 連接 | 6 | 每個 triangle 的普通私有點 |

*證明。* Singleton U 至多有一 owner 鄰居及兩框鄰居，完整 degree 不足四。

固定任一原奇環 K。對 K 的每個 U 割點，取一個環外 block-tree 分支，走到
leaf block 並取其私有 contact。不同環割點的分支互斥，取到的 contacts 互異，
也不與 K 上的私有 contacts 重複。K 至多一個普通私有點，故

\[
|K|\le1+\#(K\text{ 的 U 割點})+\#(K\text{ 的私有 contacts})\le1+k_U=3.
\]

原奇環因此都是 triangles。這裏不要求 owner 的某個 pin 拒絕，也沒有把原環
縮成一個小圖後搬回 relation。

若 U 多 block，其 block-cut tree 至少兩個 leaves；每 leaf 有不同私有 contact。
兩個 contacts 迫恰兩個 leaf blocks，且兩 contacts 均為這兩個 leaf 的私有點；
沒有 cutpoint contact 或第三份 contact。有限 tree 恰兩 leaves 就是一條 path，
所以原 blocks 的 incidence 是一條 chain。每个 triangle 至多有兩個割點。
普通私有點至多一個：內部 triangle 的兩割點之外恰一普通私有點；
leaf triangle 的兩私有點恰為一 contact、一普通點。

注意：在本稿的任意 owner 色問題中，**leaf triangle 可以只用一個 contact**。
不能沿用 pin 為未用色 D 時「leaf triangle 至少兩 contacts」的結論。

每个普通 triangle 點的 H 內度為二；每个 bridge leaf contact 的 H 內度亦為二；
每个兩 bridge 之間的普通割點也為 H 內度二。這些點完整 degree 四，故其
實際框附件恰是一條原框邊。支援 `S_U=A` 只有 `ab,bc` 兩條可用框邊；
由原附件單射，U 中 H 內度二點至多兩個。

因此至多兩個 triangles。以下對任意 block-chain 長度逐一計數：

- 沒有 triangle：所有原 chain 點（兩個 contact 端及普通中間點）都是 H
  內度二點，故 chain 至多兩點，只能是單 bridge。
- 恰一 triangle：若沒有 bridge，是單 triangle。若 triangle 在 chain 內部，
  triangle 普通點加兩個 bridge leaf contacts 已有三個 H 內度二點，矛盾。
  故 triangle 是 leaf；另一端是一個 bridge contact。兩點已用盡附件容量，
  不能有 bridge–bridge 割點，故只有一條 bridge，得到四點形。
- 恰兩 triangles：它們的普通點已用盡兩條框邊附件。不能另有 bridge leaf
  contact，故两 triangles 都是 terminal blocks。中間若有兩條以上 bridges，
  會有 bridge–bridge 割點。故它們只能共享原割點，或由唯一一條原 bridge
  連接，得到五／六點形。

單 block 的 bridge 兩端都必為 contacts：否則其 degree 一加至多兩框鄰居
不足四。單 triangle 恰用兩 contacts，第三點是普通私有點。這完成全部原形狀
的窮盡。原 U 的有限性只用於 block tree，沒有設定搜尋大小或長鏈 cutoff。∎

## 3. Diff 列的全部 owner pins

固定原 q 使 `x=q(a),y=q(b),z=q(c)` 互異；令 D 為 `[4]` 中唯一未在 A
使用的色。q 在 A 外可以使用 D，本局部引理不要求整個 B 只用三色。
假設某 owner pin d 沒有完整 lift，取 tight block palettes。
對 H 內度二的普通 triangle 點，其唯一 triangle palette 是
`[4]∖q(e)`，其中 e 是它的實際框邊。

### 3.1 單 bridge

兩 contact 端的实际附件是互異的 `ab,bc`。若 `d∈{x,y,z}`，它至少與某端
的一個實際框鄰居同色；該端有 slack，全部 U 有完整 lift。
若 `d=D`，兩端 lists 分別是 `{z}`、`{x}`，不同色，亦可直接染原 bridge。
故此形每個 owner 色均接受。

### 3.2 單 triangle

記普通點的框附件為 e，兩 contact 框附件各為一個原框點 h₁,h₂。
triangle palette P 由普通點迫定為 `[4]∖q(e)`。兩 contact 的 tight lists
均為 P，故

\[
\{d,q(h_1)\}=q(e)=\{d,q(h_2)\}.
\]

因此 d 是 e 的一個端色，h₁,h₂ 均取另一端色。Diff 使 q 在三個具名原支援點
上單射，故 h₁,h₂ 恰是 e 的同一原端點。全部實際框附件均落在 e，違
`S_U=A` 三點。故此形没有拒絕 pin。

### 3.3 Leaf triangle 加一條 bridge

普通 triangle 點附 e，bridge leaf contact 附 f；兩者是互異的 `ab,bc`。
對調名稱後可記 `e=ab,f=bc`，不改任何實際框座標或附件。
triangle contact 的 tight list 迫 `d∈{x,y}`；bridge leaf 的 tight list 迫
`d∉{y,z}`。故 `d=x`，bridge palette 只能為 `{D}`。
triangle palette 是 `{z,D}`。在二者相遇的同一原割點上它們不互斥，矛盾。

### 3.4 兩 triangles 共享原割點

兩個普通點的框邊 e,f 互異，故恰為 `ab,bc`。兩个 triangle palettes 分別
為 `{z,D}`、`{x,D}`，在共享原割點上同含 D，違反互斥。此論證不依 owner pin。

### 3.5 兩 triangles 由唯一 bridge 連接

保留全部原 labels：第一個 triangle 是 `p₁ z₁ w₁`，第二個是 `p₂ z₂ w₂`，
原 bridge 是 `w₁w₂`，contacts 恰為 `p₁,p₂`；普通點是 `z₁,z₂`。
它們分別附原框邊 `ab,bc`，triangle palettes 因此是

\[
P_1=\{z,D\},\qquad P_2=\{x,D\}.
\]

兩 contacts 的 tight lists 使 `d∈{x,y}∩{y,z}={y}`，所以 owner pin 必為
`d=y=q(b)`。原 bridge palette 必須避開兩个 cycle palettes，故是 `{y}`。
其餘實際附件由 tight 聯集唯一迫定：

\[
\begin{array}{c|cccccc}
\text{原點}&p_1&z_1&w_1&w_2&z_2&p_2\\
\hline
N_B&\{a\}&\{a,b\}&\{a\}&\{c\}&\{b,c\}&\{c\}.
\end{array}
\]

例如 contact p₁ 的 list 必為 `{z,D}`，故其一個框附件色是 x；原橋端 w₁
的 list 必為 `{z,D}⊔{y}`，故其一個框附件色亦是 x。Diff 在 A 上單射，
這兩個實際附件都必是同一原 a；第二側同理都必是原 c。
本步從原拒絕 pin 推出原附件，沒有製造不同的 piece 或以顏色邊際代替原鄰接。

這個精確原配置雖滿足局部 degree／block／框邊單射條件，卻已有 K₅ minor：

\[
\boxed{\{a\},\ \{p_1\},\ \{z_1\},\ \{w_1\},\ X=\{b,r,p_2,z_2,w_2\}.}
\]

前四 bags 為原 clique：`p₁z₁w₁` 是原 triangle，三點都原接 a。
X 以第二個 triangle、原 `rp₂`、原 `bz₂` 連通，並與前四 bags 互斥。
剩餘四個 cross 鄰接逐一是 `ab`、`p₁r`、`z₁b`、`w₁w₂`。
因此十對 bags 全部由原邊相鄰，得到原 G 的 K₅ minor，違 planarity。
不要求收縮後保存 Σ；minor 只用來否定這份原平面來源。

五形均不能在 planar 原圖中拒絕任一 owner pin，證得 U2-DIFF-ALL。∎

## 4. 完整 `(ℓ,u)=(1,1)` 的同列原接回

凍結 partition report §6 的推論 U3 已由同一列完整禁色表與原55容量，排除
`k_U=3`；推論 UL 的剩餘是 `k_U=2`、三點支援 A、每个 i 的禁色 singleton
屬 `q_i(S_U)`。本稿不重證該共同容量信任鏈。

五個字面兩邊弧的 Diff 列為：

| 原 A | Diff(A) 在 I 中的列 |
| --- | --- |
| 012 | 0,1 |
| 123 | 1,3 |
| 234 | 3 |
| 340 | 0,3 |
| 401 | 0,1 |

故同一原 A 有至少一個指定原拒絕列 qᵢ 在 A 上三色互異。本稿證
`F_U(q_i)=∅`，直接違反凍結推論 UL 的 `|F_U(q_i)|=1`。

亦可不用後半部 singleton 結論來表述最後接回：完整來源的非框邊全刪釋放
給原 `G−U` 在這份同一 qᵢ 下完整可染。固定其中一份完整外部染色 ψ，保留
它的全部 original pins／root spokes／其餘 pieces；令 `d=ψ(r)`。
U2-DIFF-ALL 對這個實際 d 給全部原 U 頂點的一份完整 lift。將它與 ψ 按原
頂點順序拼回，U 所有外鄰只在原 B 及原 owner r，全部接口值一致，覆盖原 G
的每一條原邊。自由孤立座標亦保留原四色乘積因子。所得是原 G 的完整染色，
違 qᵢ 為原指定拒絕列。沒有混拼不同列、不同 owner pins 或獨立正規化色框。
若局部證書採兩 roots 的 ambient 16-pin 格式，U 的非 owner pin 仍保留為
等值副本；本定理只說原 owner 每色都有完整 lift，不删除非 owner 維度。

這個來源排除不需要限制 long L 的 `k_L` 或大小，不使用其 off-diagonal
relation，不假設一般高接點 long 有 diagonal 出口。原先 `(1,1)` 的
`4≤k_L≤6` 和 `M_L=I` 不再是本格的存活來源；它們仍是舊化約報告中保存的
必要 residual 描述，不能當成已存在來源。

## 5. 邊界、校準及作者重讀

本稿紙面範圍為前提 1–5 下的全 owner Diff 出口，以及完整原55 `(1,1)` 的
來源排除。五形界是由任意 block tree 和兩條實際框邊附件容量推出；沒有以
六點有限圖搜尋代替任意大小證明。六點非平面配置是必要負控制：若撤掉
planarity，它在所有 proper 原框列恰拒絕 owner 色 `q(b)`，包括 Eq／Diff，
所以其非空禁色表不能僅靠局部 list 前提排除。

本稿作者重讀核對：兩-contact 多 block 的 contacts 均是 leaf 私有點；
leaf triangle 的一-contact 情況保留；每種 bridge-chain 長度以实际 H 內度二
點計數，不省去原 cutpoints；Diff 色單射只在同一原 A 上使用；原 K₅ 的五個
bags 互斥且連通，六個 clique edges、四個 cross edges 均存在；最終接回固定
同一 qᵢ、同一實際 ψ(r)，保留全部原 tuple 座標。

本稿的獨立審查與固定控制由本 audit 另份報告記錄。完整 target 未由有限
控制提供來源，必須標為 `not triggered`；採納任意大小排除由紙面證明承擔。
原55的 `(1,0)`、`(2,0)`，N1／相鄰／單-root 例外、完整 N2、E-ARC2、一般出口
及 `K∞=K≤5` 仍 OPEN。沒有提交、push、來源搜尋或新 Lean theorem。
原九格仍七格已有完整覆蓋：包含 `(1,1)` 的第二 relation 格亦含尚未排除的
`(1,0)`，故不能把本稿的新子參數排除提升成該整格 CLOSED。含 long 的參數
residual 由三個縮為 `(1,0)`、`(2,0)` 兩個。
