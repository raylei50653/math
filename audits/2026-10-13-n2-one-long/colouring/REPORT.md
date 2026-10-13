# N2 原55一 long：共同同列重色與完整外部接回

2026-10-13。本文只使用父稽核 [BASE](../BASE.json) 凍結的完整 N2 原55來源，
只寫本 `colouring/` 目錄。主張是任意大小紙面排除；有限 fibres 控制另由父稽核承擔。
沒有新外部定理、來源枚舉、Lean theorem、commit 或 push。

**定理 ONE-LONG。** 完整 N2 原55來源的 `(ell,u)=(1,0)` 子分支不存在。
此定理不排 `(2,0)`，不接到 N1、相鄰 roots、932 或其他未核對來源。

## 1. 精確原資料與沿用前提

有限簡單 induced-C5 disk，原有序框 `B=(0,1,2,3,4)`；完整 Sigma933／941
或整圖共同 D5 像、T4 全收、全部非框邊 Sigma-critical、epsilon=2；有效 H
連通且 full B-touch。原 roots r,s 不相鄰，完整 degree 都五，其他有效內點
完整 degree 四。原 `H-{r,s}` 恰為 long mixed L 與 short mixed S，沒有 U。
H 二連通。S 的實際支援包含於某條原框邊；L 的實際支援至少三個不同框點。
原 ordered/shared contacts、ownership、attachments、rotation、bridges、旁支
及全部十列完整 fibres（包括空 fibres、全部原頂點 tuples）均保留。

共同搬運整圖後，固定拒絕列 `I={0,1,3}`：

| 原框點 | q0=01212 | q1=01202 | q3=01021 |
| --- | ---: | ---: | ---: |
| 0 | 0 | 0 | 0 |
| 1 | 1 | 1 | 1 |
| 2 | 2 | 2 | 0 |
| 3 | 1 | 0 | 2 |
| 4 | 2 | 2 | 1 |

令 D=3。沿用已採納結果如下。

1. 每個內點最多有兩個框鄰，兩個時必為原框邊；每個 root 同樣成立。
2. L 的 blocks 是 bridges／奇環。多 block 時每個 leaf block 有私有 root-contact。
3. 不同 H 內度二點的實際框邊附件互異。
4. short S 對每份 proper 原框列與每個色 a 都有完整 `(a,a)` lift。
5. L 若有 shared contact，或 `k_L<=3`，已存在指定同列完整 diagonal 出口。
   因而反設來源只需處理 L 無 shared contact、`k_L>=4`。

這些分別來自凍結的原55骨架／大小界、E4 N-diagonal 及三列 diagonal 報告。
Gallai block palettes 沿用相同外部 degree-list 依賴。以下新論證不以有限圖形
控制代替這些任意大小前提，也不以 Eq/Diff 兩位元壓縮四／五點介面。

設 `T_r=N_B(r), T_s=N_B(s), T=T_r union T_s`；`t_x=|T_x|`，
`t=t_r+t_s`。各 root 的原接線等式為

`t_x+k_L^x+k_S^x=5`，其中兩份 mixed 的各側 incidence 都至少一。

令 `W_x` 為所有原 x-owned L contacts 的實際框鄰聯集，`W=W_r union W_s`。
W 只用來陳述必要限制；不把 W 當作原附件配置，也不用它重建 fibres。

## 2. 任意大小的兩條完整接回引理

**引理 A（共同 diagonal collision）。** 任一拒絕列 q 滿足

`q(W) subseteq q(T)`。

否則取原 contact v、其 owner x、實際框鄰 h，使色 `a=q(h)` 未出現在任何
root-spoke 上。固定原 r=s=a。S 有完整同 pins lift；L 中 v 的兩個實際外鄰
x,h 同色。原 degree 四給所有 residual lists 至少內度，且 v 嚴格多一色。
沿以 v 為根的原 spanning tree 從葉到根染色，給全部 L 的完整 lift。
兩份完整 tuples 在同一 q、同一 `(a,a)` 接回全部原邊，違反拒絕。注意 a
可以是已用框色；這一步不要求未用色 D，也不改框列。∎

**引理 B（固定一 root 的完整外部接回）。** 若 `k_L^s>=2`，任一 proper q
及任一 `a notin q(T_r)`，原 `G-L` 有一份完整染色，固定原 r=a。

在原連通圖 `S union {s}` 上取 lists，固定全部框點及 r=a。每個 S 點原
degree 四，故可用色數至少在這個原圖內的 degree。s 的 list 恰是
`[4] minus q(T_s)`，原框附件是最多兩個相鄰點，故

`|list(s)|=4-t_s=k_S^s+k_L^s-1 > k_S^s=degree_{S+s}(s)`。

以 s 為根的原 spanning tree 從葉到根染色，給 S 及 s 的全部原座標。
r 的 spokes 合法，rs 不存在，因此這恰是一份完整 `G-L` lift。此處沒有
從 root marginal 猜一份外部 lift；完整外部 tuple 由原圖直接構造。∎

**推論 B1。** 若 `k_L^s>=2`，任一拒絕列 q 有 `q(W_r) subseteq q(T_r)`；
交換 r,s 得對称結論。若某原 h in W_r 的色 a 避開 r-spokes，引理 B 給
固定 r=a 的完整外部染色。保持其實際 s pin 不變；L 的原 r-contact 與 h
造成 collision slack，補回完整 L，得到同列完整 G 染色。∎

兩引理都不限制 L／S 長度。引理 B 的 spanning tree 只是染色次序，沒有
收縮任何來源鏈或移植 relation。全部自由孤立座標可任選四色，原乘積因子保留。

## 3. 具名框點閉包：局部必要限制

對具名框點集合 X 定義

`Cl(X)={h in B : for every i in I, q_i(h) belongs to q_i(X)}`。

這是三份字面框列的集合查詢，不是 L 的 fibre quotient。引理 A 給
`W subseteq Cl(T)`；推論 B1 在其 incidence 前提下給
`W_x subseteq Cl(T_x)`。

表中的五個三列 signatures 互異，所以單點閉包仍為自己。直接逐個具名
框點查表，對任何 X 都有

`Cl(X) minus X = ({2} if {0,4} subseteq X and 2 notin X else empty)`

`                    union ({4} if {1,2} subseteq X and 4 notin X else empty)`。

理由是 0、1、3 分別有一列的色只在該點出現，所以不能新增。未取 2 時，
q0／q1 中須由 4 提供色 2，q3 中須由 0 提供色 0；未取 4 時，同理須由
2 提供前兩列色 2，並由 1 提供 q3 色 1。這兩種新增不能同時發生。
完整 32 份 X 可作有限查表控制，但上述公式已逐點窮盡全部 X。

## 4. 原 leaf-cycle 的任意長 K5 排除

反設來源存在。S 的完整 D diagonal lift 與 D 對原 spokes 合法，迫 L 在
三份指定列都拒絕 `(D,D)`。因此各列 L 的 degree lists 都 tight，並由原
Gallai block palettes 合成。

先排單 block。singleton／單 bridge 不可能有四個無 shared 的 contacts。
若 L 是單奇環，它至少有 contact；contact 的 list 不含 D，普通點的 list
含 D，單一 cycle palette 迫所有點都是 contacts。它們各有恰一框附件，
三列 palette 一致迫所有附件有相同三列 signature，即同一原框點。
這違反 L actual support 至少三點。因此 L 有至少兩個原 blocks。

假設有 leaf cycle J，其唯一割點為 z。J 有私有 contact p。對每一指定列，
所有私有點的 lists 都等於 J palette；contact 不含 D，普通私有點含 D，
故全部私有點都為 contacts。它們各恰有一個框鄰；三列 palettes 加上五個
框點 signatures 互異，迫全部私有點都附同一原 h。

取沿 J 相鄰的兩個私有點 p,q；任何奇長至少三均可，**沒有先假設 triangle**。
`L0=L-{p,q}` 仍連通。p、q 各有一條原 cycle 邊接 L0（triangle 時同接 z）。
它們各恰一個 root incidence，故 `k_L>=4` 保 L0 至少還有一個 root-contact。
記原連通 `R0={r,s} union S`。

若 h 是任一 spoke 端點，取五 bags

`R0, {h}, {p}, {q}, F=L0 union (B-{h})`。

F 由 L 的 long 支援及 p,q 只附 h 而連通。四個 singleton／R0 間的六對
鄰接為 root-spoke、兩條 root-contact、hp、hq、pq；F 接 p,q 用原 cycle
邊，接 R0 用剩餘 contact，接 h 用原框邊。故全十對鄰接，給原 K5 minor。

若 h 不在 T，但存在 spoke 端點 t，long 支援給實際附件 `j notin {h,t}`。
它必附在 L0。沿原 C5 選 h-t 弧不經 j，及 h-j 弧不經 t，兩弧除 h 外
互斥。去 h 後記其頂點集為 P_t、P_j。取五 bags

`R=R0 union P_t, {h}, {p}, {q}, F=L0 union P_j`。

R 由原 t-spoke 接通，F 由原 j-附件接通，bags 互斥。R-h、F-h 是兩條原
框弧靠 h 的邊；其餘八對與前案相同。這仍是原 K5 minor。
未把 bags 當作單色染色，也未要求 minor 保留 Sigma。

最後若 t=0，任一 leaf block 的私有 contact 都有實際框鄰：leaf bridge
有兩個，leaf cycle 有一個。故 W 非空，違反引理 A 的 `q(W) subseteq empty`。

結論：所有原 leaf blocks 都必為 bridges，且 t>0。此排除覆蓋任意 cycle
長度、任意剩餘 L 結構、任意私有 contacts 的 r／s ownership。

## 5. 兩份 leaf bridges 迫唯一具名 spoke 形狀

對任一 leaf bridge，令 p 為私有端、z 為 L 內鄰。無 shared contact 加原
degree 四迫 p 恰有一 root-contact，實際框附件為原框邊 `e={a,b}`。

**原 minor。** 若 a,b 都在 T，取

`R0, {p}, {a}, {b}, F=(L-{p}) union (B-{a,b})`。

L-p 連通；long 支援有一份框附件在 {a,b} 外，故 F 連通。R0 接 p 用原
contact，接 a,b 用原 spokes；p 接 a,b 用原附件；ab 是原框邊。F 接 p 用
pz，接 R0 用剩餘 contact，接 a,b 用補框弧的兩端邊。十對原鄰接給 K5。

因此每個 leaf bridge 的附件 e 都滿足

`e subseteq Cl(T), e notsubseteq T`。

有限 block-cut tree 至少兩 leaves。Cl(T) 若等於 T 就立即矛盾；否則依
§3 恰多一點 h，且 h 為 2 或 4。所有 leaf bridge 附件都必是 incident h
的原框邊。其私有端是原 H 內度二點，附件單射使每條原框邊至多用一次。
因此恰兩個 leaf blocks，附件恰為 h 的兩條 incident 原框邊。

若 h=2，閉包新增條件迫 `0,4 in T`；兩 leaf 附件 12、23 又迫 `1,3 in T`。
故 `T=B-{2}`。若 h=4，同理 `T=B-{4}`，leaf 附件 34、40。

四個不同 spoke 端點加每 root 至多兩 spokes，迫 t=4、`t_r=t_s=2`，且
兩份原 spoke 邊互斥。按原 C5 的邊，唯一可能是

| h | 原 T | 兩 roots 的原 spoke 邊（可交換 roots） | L leaf 附件 |
| --- | --- | --- | --- |
| 2 | 0134 | 01、34 | 12、23 |
| 4 | 0123 | 01、23 | 34、40 |

原 degree 和給 `k_L+k_S=10-t=6`。因 `k_L>=4,k_S>=2`，恰為 `k_L=4,k_S=2`。
mixed S 兩側各有一 incidence；每 root 的三條內部邊迫 `k_L^r=k_L^s=2`。
block-cut tree 此時也是一條 chain；內部奇環與 contact 割點均仍保留，
後一步不必分類它們或限制這條 chain 的長度。

## 6. 完整同列矛盾，關閉一 long 分支

由 `k_L^r=k_L^s=2`，推論 B1 兩側均適用，得

`W_r subseteq Cl(T_r), W_s subseteq Cl(T_s)`。

表中各原 spoke 邊 `01、34、23` 的三列闭包都等於自身。故每個 L contact
的全部原框鄰都必落在其 owner 的原 spoke 邊。但任一 leaf contact 的
原附件邊，在上表兩行中都不包含於任一 owner spoke 邊，矛盾。

等價的具體同列接回是：取任一 leaf contact p 及其實際 owner x。其附件
中有 h0 不在 `Cl(T_x)`，因此某份同一指定 q_i 滿足 `q_i(h0) notin q_i(T_x)`。
令原 x 色為 `a=q_i(h0)`。引理 B 在這一 q_i 下先構造完整原 `G-L` lift，
保留其另一 root 的實際 pin；再由 p 的 owner／框鄰 collision slack 構造
全部原 L tuple。兩份按原頂點順序接回，原 q_i、spokes、root 接線、L／S
內邊及附件全部合法，得到被拒絕原列的完整 G 染色。這是完整同列矛盾，
不是不同列非空 fibres 的乘積，也不需要把未用 D 的永久障礙本身消掉。

因此完整來源 `(ell,u)=(1,0)` 被排除。剩餘 `(2,0)` 的第二份 long 不享有
任意色 diagonal 引理，以上全圖入口不能照搬；父原55、N2、E-ARC2仍 OPEN。

## 7. 對拓撲部分的獨立逐項核對與證據邊界

本作者在完整 fibre 接回引理之外，重新核對兩種 leaf minors：

- R0 用全部原 S 及兩 roots，S mixed 使其連通；L 與 S 頂點互斥。
- leaf cycle 的 p,q 必能選為相鄰私有點，刪去後剩餘原 cycle 與其餘 L 仍連通。
  不要求它是 triangle，也不刪割點 z。
- p,q 每點只有一 root incidence；移除兩點後仍有原 contact，支撐 R-F 邊。
- long 的三個以上原框支援，給所有 F 所需的實際 attachment；沒有推定虛構邊。
- h-t 與 h-j 原框弧除 h 外互斥，附進 R,F 後仍是互斥 branch sets。
- leaf bridge 的補框弧連通性使用 ab 是原框邊；原附件單射只用在 H 內度二端點。
- 每個 K5 只作原圖非平面證書；不聲稱收縮後保完整 Sigma 或 source identity。

紙面論證覆蓋任意 block 數與奇環長度。完整十列、四／五點具名介面及全部
16 pins 的控制，由父 checker 保存；它們是重播校準，不承擔任意大小窮盡。
完整 target source 保持 `not triggered`；新 theorem 的證據是上列原契約下
的紙面矛盾，不能把零來源控制改寫成來源枚舉排除。沒有新 Lean theorem。
