# 原 N2-55：兩份低接點 long 的同列／拓撲排除

2026-10-11。權威輸入為本 audit 的 `../BASE.json` 及 `../frozen/`。
本稿只在完整凍結 N2-55 契約下推論；不構造來源、不改原圖或色框。

## 1. 原相鄰雙 spoke 的 K5 障礙

**命題 T-SAME-EDGE。** 在完整 N2-55 契約下，若 r,s 都與同一原框邊
ab 的兩端相鄰，且一份原 mixed C 有框附件 vh、h 不在 {a,b}，則原 G
含 K5 minor。

原 H 的中央二連通 block K0 同時含 r,s；所有原 mixed 的全部頂點均在 K0，
其他 H blocks 只是在 root 上接的一份 unary。對 v∈C，以 K0 的二連通性
取從 v 到 {r,s} 的兩條內點互斥 paths，終點分別為 r,s（兩點 fan）。
把每條路截到首次碰 {r,s}；它此前的頂點都在同一 C，因為 H−{r,s}
的不同分量沒有跨邊。因此其聯集是內部全在 C、通過 v 的原 r–s 路 A。
另一原 mixed C′ 提供內部在 C′ 的原 r–s 路 A′。A 與 A′ 內部互斥，
形成原 cycle。令 B′=B−{a,b}；ab 是框邊，所以 B′ 是非空連通框路。

五個原 branch sets 為

1. R={r}∪(V(A′)−{r,s})；
2. S={s}；
3. X={a}；
4. Y={b}；
5. Z=(V(A)−{r,s})∪B′。

R、Z 各是連通路；Z 另由原附件 vh 接上 B′。五袋互斥。
R–S 是 A′ 的最後一邊，R–Z／S–Z 是 A 的首末邊；四個 root–框點
spokes 給 R–X、R–Y、S–X、S–Y；原 ab 給 X–Y；補框弧的兩端邊
給 Z–X、Z–Y。十對鄰接均為原邊，故是 K5 minor。∎

這個 minor 不用局部 palette，也不要求一份外部染色。兩點 fan 只作選取原路；
不合併 roots，不變動任何 contacts 或完整 fibres。

## 2. 兩份 long 接線總數皆至多三

**命題 T-TWO-LOW-LONG。** 完整 N2-55 的 (ℓ,u)=(2,0) 中，若兩份
原 long P,Q 各有 k≤3，則來源不存在。

若任一有 shared contact，它在所有三列接受 diagonal；另一份由既有低接點
escape 在某一列接受 diagonal，同列完整 lifts 直接矛盾。
以下只看兩份都沒有 shared contact 的情形。

原 r,s degree 都是 5 且不相鄰，u=0，故

`10 = k_P + k_Q + t_r + t_s`。

既有全刪邊釋放給每個 root 框附件至多相鄰兩點，所以 t_r,t_s≤2。
k_P,k_Q≤3 因而迫 k_P=k_Q=3、t_r=t_s=2。
兩 long 的原盾弧邊互斥，各至少長 2。因此盾弧長度只有 (2,2) 或 (2,3)
及交換型。每個 root 的框附件都避開兩段盾弧的內點。

若是 (2,3)，可用框點只有兩盾弧的共同端點；它們不相鄰，與 root 的
兩個相鄰框附件矛盾。若是 (2,2)，可用框點是三個弧端點，兩個相鄰者
恰為唯一未被盾弧使用的原框邊 ab 的兩端。因此 r,s 都接 a,b。
P 的 actual support 等於其盾弧的三個框點，必含一個 h∉{a,b}，取原附件 vh。
命題 T-SAME-EDGE 给原 K5 minor，違反平面性。∎

結果只關閉這個限定子域：剩餘 (2,0) 必有至少一份原 long 的 k≥4。
不能從這裡推導兩份任意 long 的共同 diagonal，也不關閉完整父族。

## 3. 證據界線

兩個結論是任意大小的原圖紙面推導。有限 bag 控制只校驗所列原邊、
互斥／連通袋及十條鄰接，不作來源實現或圖類完備性聲稱。
沒有新 Lean theorem；一般原55、N2、E-ARC2 保留 OPEN。
