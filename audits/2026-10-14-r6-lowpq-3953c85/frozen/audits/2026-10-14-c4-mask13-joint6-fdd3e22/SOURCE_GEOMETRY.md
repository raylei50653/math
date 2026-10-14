# C4-MASK13-JOINT6：原接點幾何與条件大小界

2026-10-14。這是固定 no4ct 全域最小來源上的紙面推導。一般六接點殘題
仍 OPEN；本文的 `k≥28` 只適用於明列的高 degree 子域。

## 1. 來源、命名與實際依賴

沿用 [原相鄰四度化約](../2026-10-14-c4-triangle-core-b66f592/ADJACENT4.md)
及 [球面證明](../2026-10-14-c4-triangle-core-b66f592/PROOF.md)：
G 是所有完整 C5 關係不在 K132 的圖中，全域最小內點 k、再最大邊數者；
整份原圖共同搬到 `B=(x,y,a,b,c)`、`Σ∈{932,933,941}`，並假設
`d_G(x)=d_G(y)=d_G(b)=4`。球面 S 是外加五度 u；識別 a,c 為 z 並刪 u,b
得四連通三角化圖 T0；再刪 x,y 得 induced 外框 `Q=(z,s,r,t)` 的 R。
其總點數為 `k+1`，內點數為 `k−3<k`，其完整 C4 關係必為 mask13。

幾何依賴是 [no4ct 小 cap 證明](../2026-10-13-c5-no4ct-frontier-6943561/w5/PROOF.md)
§§3–4：原 G 的每個 C4 有界側空；原內點至多接兩個相鄰 B 點；每条原 B
邊恰有一個雙接 apex。degree 與超額使用
[no4ct collar](../2026-10-13-c5-no4ct-collar-6cafdfb/REPORT.md) 的 `h≥3`，其中
`h=Σ_B(d_G−4)`。條件 C8/C9 加強在 §4 逐份列明，不移植到其他 h。

## 2. 五個原 apex 的精確 induced 骨架

五條原框邊 `xy,ya,ab,bc,cx` 的 apex 依次是

`r,t,p,q,s`。

它們互異；原 B 接觸恰分別為 `xy,ya,ab,bc,cx`。原三角面及 x,y,b 的
四度鄰序給三條必有邊

`rs,rt,pq`。

五個非連續 apex 對全部無邊。若其中某邊存在，下表給一個原 C4；其兩條
diagonal 都由原接觸限制排除。這與該 C4 有界側空、且所有原內面三角形
矛盾：空四邊形仍必有一條 diagonal。

| 假設的邊 | 原 C4 | 兩條不存在的 diagonal |
| --- | --- | --- |
| rp | r-y-a-p-r | ra, yp |
| rq | r-x-c-q-r | rc, xq |
| st | s-x-y-t-s | sy, xt |
| sp | s-c-b-p-s | sb, cp |
| tq | t-a-b-q-t | tb, aq |

餘下兩個連續 apex 對有精確判準：

`tp∈E(G) ⇔ d_G(a)=4`，`qs∈E(G) ⇔ d_G(c)=4`。

例如若 tp 存在，atp 是原三角形，必為面；它佔滿 a 在 ya、ab 兩個框面
之間的內側 sector，所以 a 的完整鄰集正是 `{y,t,p,b}`。反向由四度鄰序
直接得到 tp。c 支同理。

因此六個原接點 `(z,s,r,t,p,q)` 在 R 中的 induced 子圖恰是四環
`z-s-r-t-z` 與三角面 `z-p-q-z`，再加符合以上判準的 tp、qs。
兩條可選邊不能同時存在，否則原五個 B 點全部四度、h=0，違反 h≥3。
這是原圖接線定理；沒有由抽象色關係推斷來源存在。

還有全圖的共同鄰點等式 `N_R(z)∩N_R(r)={s,t}`。若另一共同鄰點 w
來自原 a 鄰點，取球面原五環 `u-a-w-r-x-u`。u 處的兩個 sector 使 y
在一側、b,c 在另一側；後者至少兩點。由已採納 S6，前者只能是 singleton
y，且 y 與五環每點相鄰。原 y 恰五度的鄰集 `{u,x,r,t,a}` 遂迫 w=t。
原 c 鄰點則用 `u-c-w-r-y-u`，同理迫 w=s。所有例外 B 端點已由原
接觸限制排除，兩個五環都是 simple。

所以把非相鄰 z,r 沿 R 外面識別時，只有 s,t 兩處原框平行邊對；抑制
這兩對後得 k 點的簡單 sphere triangulation J。這補強原商圖的幾何身份，
不提高其染色結論，也不引入普遍平面圖可染性。

## 3. 精確 degrees 與較小 4-candidate

逐點保留所有原邊可得

| R 頂點 | 精確 degree |
| --- | --- |
| z | `d_G(a)+d_G(c)−4 = h+4 ≥7` |
| r | `d_G(r)−2 ≥3` |
| s,t | `d_G(s)−1, d_G(t)−1 ≥4` |
| p,q | `d_G(p)−1, d_G(q)−1 ≥4` |
| 其他 R 內點 | 原 G degree，至少五 |

p,q 是原 b 的兩個內鄰點，刪 b 各失一條邊；它們均不接 x,y，且只接
a,c 之一，故沒有其他 degree 損失。r 失去 x,y；s,t 各失去其中一點。

**命題 G28。** 在本節固定來源下，若另外

`d_G(p)≥6` 且 `d_G(q)≥6`，

則 `k≥28`。

證明。R 是外框 C4、全部內面三角形的簡單 plane graph。每個 R 三角形
是 T0 的三角形，而 T0 沒有非面三角形；Q 是 induced，所以 R 不是四點
diamond。degree 表保證 R 的每個內點 degree 至少五。因此 R 完全符合
Dvořák–Lidický–Mohar 的 **4-candidate** 定義。原完整 mask13 缺 ABAC，
所以它禁止一種 diagonal 染色；把 Q 循環改名即可採用論文的具名 diagonal。

沿用 [已採納的外部有限結果](../2026-10-14-c5-c4-boundary-pivot-77fbd5d/EXTERNAL.md)：
[arXiv:2504.08327v2 §2、Table 1](https://arxiv.org/html/2504.08327v2#S2)
完整枚舉至多 28 個**總頂點**的 4-candidates，唯一 diagonal-forbidding 圖
是四點 diamond。故 `|V(R)|=k+1>28`，即 `k≥28`。證畢。

這是對同一較小 R 重新匹配外部結果，沒有重跑作者枚舉。外部 C++ 至28點、
独立 Python/Sage 至25點及生成器完備性信任界均沿用；不使用未證無界
diagonal 猜想，也不把原來源的最小性轉成「R 是最小 4-candidate」。

## 4. 確實覆蓋的兩個現有子域

### 4.1 本分支的 h=3

[no4ct C8 接入](../2026-10-13-c5-no4ct-c8-6cafdfb/REPORT.md) §3 的八項
必要殘留中，施加本分支的 `e_x=e_y=e_b=0`，只剩

| 查詢 | 原 extras `(e_x,e_y,e_a,e_b,e_c)` | 原 `(d_G(a),d_G(c))` |
| --- | --- | --- |
| c04-941 | (0,0,1,0,2) | (5,6) |
| c07-941 | (0,0,2,0,1) | (6,5) |

同一報告 §4 已把全部40項 apex 低度排除接入 no4ct：五個原 apex
`r,t,p,q,s` 全部 degree 至少六。故 G28 適用，得到

`本 C4-MASK13-JOINT6 分支且 h=3 ⇒ Σ=941，k≥28`。

此時 R 的 z 恰七度，r 至少四度，s,t,p,q 至少五度，tp、qs 都不存在。
兩份 necessary query 沒有被宣稱可實現，任意大小來源亦尚未排除。

### 4.2 本分支的 Σ=932、h=4

[T2 C9-932 原 apex 定理](../2026-10-13-c9-932-source-d521163/REPORT.md)
直接採用 no4ct 全域最小來源，證全部20份原殘留的五個 apex degree 至少六。
其三組 extras 中，施加 `e_x=e_y=e_b=0` 只可能兩個非相鄰的2，即
本名字中的 `(0,0,2,0,2)`，即 [原身份表](../2026-10-13-c9-932-source-d521163/SOURCE_CONTRACT.md)
的 c09-induced-932。因此 G28 也給

`本 C4-MASK13-JOINT6 分支且 Σ=932、h=4 ⇒ k≥28`。

此時 z 恰八度，r 至少四度，s,t,p,q 至少五度，tp、qs 都不存在。
沒有把 T2 的 apex 下界移植到 933/941 的 h≥4，或932的 h≥5。

## 5. 原 r 五度時的下一個精確小介面

這一節不作排除，也不使用 §4 的高 apex 子域。假設 `d_G(r)=5`。
由原面鄰序可寫

`N_S(r)=(x,y,t,v,s)`。

v 是另一原內點且不接 B：x,y,b 的完整鄰集與 §2 無邊排除這三個接觸；
若 va 存在，原 C4 `a-y-r-v-a` 的兩 diagonal ar、yv 均不存在，矛盾；
若 vc 存在，使用 `c-x-r-v-c`。因此 zv 也不存在。

刪 r 得外框 `Q'=(z,s,v,t)` 的 R'。原 r 的兩個剩餘面為 rsv、rvt，
所以這確為三角化 C4 disk；st、zv 均不存在。它有 `k` 總點、`k−4<k`
內點，可套同一相對 C4 七 mask 定理。重新插入 r 時恰加 `rs,rv,rt`，
其全部完整局部延伸為：

| R' 固定框色 `(z,s,v,t)` | r 的全部可能色 | R 框色 `(z,s,r,t)` |
| --- | --- | --- |
| ABAB | C,D | ABCB, ABDB |
| ABAC | D | ABDC |
| ABCB | A,D | ABAB, ABDB |
| ABCD | A | ABAC |

最後一列會產生 R 禁止的 ABAC，所以 R' 不含 ABCD。七 mask
`{7,10,11,12,13,14,15}` 中只有7不含 ABCD，故 **R' 恰為 mask7**。
表的前三列也顯示 mask7 接回 r 後恰給原 mask13。

只使用原 ADJACENT4 的兩個共同條件時，原殘題等價於 R' 的 mask7 加：

- 對每份 Q'=ABAC 的完整染色，`{f(p),f(q)}={B,C}`；
- 對每份 Q'=ABCB 的完整染色，`{f(p),f(q)}={C,D}`。

這裡比較的都是同份 R' 全染色及表中全部 r lifts。Q'=ABAB 的兩份 lifts
都落在原不可接 x,y 的 ABCB 型，因此原 cap 表本身不給額外條件。

再接本輪獨立於 r degree 的 [JOINT_FIBRES](JOINT_FIBRES.md) §3：原
Q=ABCB 每份完整染色的 pq palette 必含缺失色 D。固定一份 R' 的 ABAB
染色，r=C 的 lift 迫 pq∈`{{C,D},{B,D}}`；r=D 的 lift 迫
pq∈`{{C,D},{B,C}}`。两份 lift 保持同一 R' 上 p,q 的顏色，所以取交集得
pq 必為 `{C,D}`。因此可把較小介面的完整必要且充分殘題寫成：

| R' 框色 | 每份完整染色必有的 pq palette |
| --- | --- |
| ABAB | {C,D} |
| ABAC | {B,C} |
| ABCB | {C,D} |

充分性由表中全部 r lifts 直接接回原 ABAB／ABCD 兩項壞 palette；必要性
的第一列另用了原圖 Kempe 定理，沒有冒充 cap 表結論。普通 mask7 小代表
仍不能代換保內部 p,q 的六接點關係。

**更窄的條件界。** 若本節另有 `d_G(p),d_G(q)≥6`，R' 也是
4-candidate：刪 r 只改變 s,v,t 的 degrees，而三點現在全在新外框；
所有新內點仍至少五度，三角形面性由 T0 保留。mask7 缺 ABCD，即
rainbow-forbidding。相同外部 Table 1 在至多28總點範圍內沒有任何此型，
所以 `|V(R')|=k>28`，得到 **`k≥29`**。這只屬
`d_G(r)=5, d_G(p),d_G(q)≥6` 的更窄交集。§4 的兩個子域已保證 r≥6，
不能把這個29界接到它們上面。

## 6. 停止點

新結論是五 apex 接線、精確 degree 表、G28 的條件式界、原 r 五度的
mask7 化約及其高 p,q 子域的29界。一般分支仍允許 p 或 q 在原 G 恰五度，這時它在 R 只有
四度，G28 的4-candidate前提不成立。本節不宣稱排除這些子型。
一般 k≥23、K≤22 及任意大小六接點殘題的 OPEN 狀態均保留。
沒有新來源實現、沒有重跑外部枚舉、沒有新增 Lean theorem。
