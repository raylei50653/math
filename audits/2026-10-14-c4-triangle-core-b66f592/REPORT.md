# C4 對角延拓：四連通三角化圖與兩個指定三角面

2026-10-14。BASE `b66f592167bf7c3fab0ed89e57b092e49877be15`，起始工作樹乾淨。
直接輸入的固定 bytes 與 SHA256 見 [INPUTS](INPUTS.json)。
本輪得到新的任意大小結構化約及完整 fibre 雙射，**未證無界 ABCB 延拓，
未完成任一 932／933／941 整支排除，`K≤22=K≤5` 與共同 `k≥23` 不變。**

## 1. 完整來源契約

G 是全部有限簡單 disk-C5 圖中，完整關係不在 K132 者的全域最小內點數 k、
再最大邊數來源。沿用已採納 no4ct 正規形與小 cap 定理，不假設固定 mask
最小性、edge-critical、N2、ε 或 singleton 支援非空。
同一原圖、rotation、具名框 B=(b0,b1,b2,b3,b4) 及四個色名始終作為來源基準；
後述商圖的識別與完整色名搬運逐項明列。

令 `(x,y,a,b,c)=(b0,b1,b2,b3,b4)`，S 是 G 外加 u 及全部五條 spokes，
H=S−ub，外框 Q=(u,a,b,c)。原來源橋給
`F_H(ABCB) ≅ F_G(y1) ⊔ F_G(y0)`，三支均拒絕此 fibre，且 `x24>0`。
本輪的來源依賴是凍結的 [C4 橋](frozen/audits/2026-10-14-c5-c4-boundary-pivot-77fbd5d/PROOF.md)
與 [no4ct 小 cap／接點證明](frozen/audits/2026-10-13-c5-no4ct-frontier-6943561/w5/PROOF.md)。

## 2. 球面與 C4 的小圈限制

[完整證明](SMALL_CYCLES.md)重新接入 no4ct 前提，得到：

- S 最小度至少五，無分離三角形／四環；每個分離五環至少一側恰一個五度點。
  本文稱這組明列性質為 internally-six-connected，**不是六頂點連通**。
- H 除指定外框 Q 外，每個四環的有界側皆空。
- H 的 induced 五環若包至少兩點，只可能是原 B，或在 `d_G(b)=4` 時的
  `link_S(b)`。兩者各包恰 k 點；其餘 induced 五環包空或單一 W5 中心。

這補上真正來源比一般「u 度四 4-candidate」更強的條件。
u 的兩個內鄰點在 link 中連續原本就是三角化下的自動性質。
兩個大五環的內點數恰為 k，整份 H 的內點數為 k+2，均不能套 `s<k`
的相對小代表引理。也沒有假設 H 是全部 restrictive 4-candidates 中最小者。

## 3. 消去 u 並識別指定同色點

原內點不能同接 B 上非相鄰的 a,c，所以 `N_H(a)∩N_H(c)={u,b}`。
在 Q 外側識別 a,c 為 z、抑制兩組空二邊面，再刪掉 u，得到簡單球面
三角化圖 T，以 `(z,x,y)` 為指定外三角；`|V(T)|=k+4`。
這個識別只描述 `a=c` 的那些完整染色，不聲稱保存 H 的全部四態關係。

精確度數為

\[
d_T(x)=d_G(x)\ge4,\quad d_T(y)=d_G(y)\ge4,\quad
d_T(z)=d_G(a)+d_G(c)-1\ge7,\quad d_T(b)=d_G(b)-1\ge3.
\]

其餘點皆為原 G 內點，度數不變、至少五。[完整化約證明](PROOF.md)給出：

| 分支 | 得到的圖 | 剩餘染色義務 |
| --- | --- | --- |
| `d_G(b)≥5` | T 無分離三角形，因此四連通；除指定點 b 外，其餘內點度≥5 | 固定 `(z,x,y)=(B,C,D)`，證 b 能取 C 或 D |
| `d_G(b)=4` | T 恰有一個分離三角形 `N_T(b)=(z,p,q)`；刪 b 得四連通 T0，`|V(T0)|=k+3` | 證同一份 T0 染色中，兩個具名三角面 zxy、zpq 可以使用不同色集合 |

第二支中 x,y,p,q 互異，p,q 是原內點；四點 induced 子圖只有 xy、pq。
T0 的 x,y,p,q 度≥4，z 度≥6，其餘度≥5。兩個三角面只共享原點 z。
T0 有染色不是額外 4CT 假設：下節的非空 `F_A` 已由原來源 `x24>0` 提供。

## 4. 完整 fibres 與單步出口

固定 T 上 `(z,x,y)=(B,C,D)`，F_r 是再指定 `b=r` 的所有完整染色，
r∈{A,C,D}，包含空集合。回到 H 時取 u=A，把 z 拆回同色的 a,c。

- F_C 直接給 H 的 ABCB。
- F_D 在整份染色上共同交換 C,D，亦給 H 的 ABCB，且與前支不交。
- F_A 的原份與整份 C,D 交換各給 H 的 ABAB，兩支不交。

因此有完整集合雙射，而不僅計數：

\[
F_H(ABCB)\cong F_C\sqcup F_D,\qquad
F_H(ABAB)\cong F_A\times\{0,1\}.
\]

固定原色框下 `(|F_A|,|F_C|,|F_D|)=(x24,y1,y0)`。
來源正是 `F_A≠∅, F_C=F_D=∅`；新成果在 T／T0 的結構限制，
這個公式本身沒有消掉既有難題。

在任一 `f∈F_A`，保持三角三個色名逐點不變的一步 Kempe 出口，恰在
`b` 的 AC 分量不含 x，或 AD 分量不含 y 時存在。A↔B 不可能提供出口，
因 bz 是原商圖邊。這只是一步的精確判準。

[完整控制證書](controls/certificate.json)保存 catalogue-823 的同圖反例：
初始兩個分量均被釘住，先交換不碰三角的 CD 分量，再交換 b 的 AC 分量，
兩步取得出口。該圖是實際 near-triangulation，識別後 T 也簡單三角化；
它未具全部最小來源度數前提。故它反駁一般「一步受阻即無出口」，
不反駁尚未證明的強來源延拓命題。

## 4.1 兩個相鄰四度點：七種 C4 關係只剩 13

在原 `d_G(x)=d_G(y)=d_G(b)=4` 子分支，[新增窄引理](ADJACENT4.md)
刪 T0 的 x,y，得到具名 C4 disk `R`，新框 `(z,s,r,t)`，內點恰 `k−3<k`。
p,q 留在 R 嚴格內側，原 zpq 三角面及全部接線保留。
因此這一次確實能用 no4ct 相對 C4 七關係表。

| R 的固定框色 | 接回 (x,y) 的所有完整選擇 |
| --- | --- |
| ABAB | (C,D)、(D,C) |
| ABAC | (C,B)、(C,D)、(D,B) |
| ABCB | 空 |
| ABCD | (D,B) |

每份 ABAC 的同一 R 染色給三種不同 xy 色集合；其 p,q 色值已固定，
恰有兩份 cap lifts 能打破兩面同色集合。因此若來源目標仍失敗，R 必拒 ABAC，
七關係只留12／13。再由 `zr` 非邊、外側識別後 k 點平面圖的相對可染性，
得到 R 有 z=r 的染色，排12，故 **R 完整 C4 mask 恰為13**。
這一步的 C5 dummy 增廣只有 `k−2<k` 個內點，沒有引用普遍四色定理。

仍待攻的精確共同義務是：在每份 R 的 ABAB full lift，pq 色集合都為 {C,D}；
在每份 ABCD full lift，都為 {B,D}。必須保留 `(z,s,r,t,p,q)` 六個原接點
及同一 full lift，不能只保四框 mask13。[cap checker](controls/check_cap.py)
核對全部局部 lifts、24份有序pq指派，並保留一份能滿足此共同義務的抽象
關係反控制；該關係不是實現圖，mask13 仍未排除。

## 5. 本輪有限驗證與信任分層

| 驗證 | 實際範圍 |
| --- | --- |
| [完整 fibre checker](controls/check_quotient.py) | 132 份既有具體 C5 圖、264 份完整集合等式；547 個 T lifts；H 的 56 個空格、T 的 120 個分色空格均保留 |
| 同圖固定三角 Kempe 圖 | 173 份 F_A 狀態核對一步判準；24 份無一步出口，其中 15 份可兩步出去，9 份所在固定三角 Kempe class 無出口 |
| [結構 checker](controls/check_structure.py) | 192 份既有 21 點球面控制逐小圈檢查；157 份符合 S6，10,895 個具名開口全部符合 T/T0 結構，其中 4,891 份 T、6,004 份 T0 |
| 負控制 | 漏分支、錯共同換色、漏 ABAB 第二方向、刪 quotient 邊、非法識別後抹 loop；漏面／重面；另有證書與輸入竄改拒絕 |
| 紙面審查 | [獨立審閱](review/INDEPENDENT.md)檢查 mixed triangle、singleton 例外、完整 fibres 與前提界線 |

結構控制重用已有球面證書，沒有重跑 plantri 或外部≤28點枚舉；它們的
完整來源 mask 全為1023，不是實現932／933／941。真正目標來源為
`not triggered`；一般推導依靠明列的紙面證明，不能由控制的零反例推出。
本輪沒有新增外部排除定理、Lean theorem 或一般 Kempe 連通性結論。
正常／seed17 重播及負控制的實際紀錄見 [VERIFICATION](VERIFICATION.md)。

## 6. 停止點與文件接入

可先續攻 §4.1 的 mask13 六接點共同義務；更一般的 `d_G(b)=4` 分支，則在同一個四連通 T0 中打破兩個指定三角面
zxy／zpq 永遠使用同一色集合的限制；必须保留兩面共同的 z 與全部原接點。
另一支保留 T 上指定 b 的異色出口。兩支都仍 OPEN，不能擅用普遍 Kempe
連通性，或用不同完整染色的兩個三角面投影拼接。

Closure scope：完成上述 S6／H4／H5、T/T0 結構、full-fibre 雙射，及三個原框四度子支的 R=13 必要化約與精確共同殘題。
Updated：C4 新權威入口、舊橋的後續連結、Kempe 導覽及 STATUS；no4ct 交接
只更新下一窄題連結。Reviewed-unchanged：既有 K≤22、共同 k≥23 與三支
未排除的數學狀態。Propagation stop：L1／直接入口；未改 HANDOFF 的研究線
或 README，未 commit／push。
