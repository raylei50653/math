# 指定邊普通完美匹配分離：無界來源定理

2026-10-15，BASE `6ddea32a81349821ad3724ae1652bddb9c6a7b04`。
本證使用 Edmonds 的 matching polytope 定理；不使用四色定理。
所有圖有限、無向、簡單；所有匹配均在同一張具名圖上。

## 1. 外部定理及本證自行完成的轉換

外部輸入只有 Jack Edmonds, *Maximum Matching and a Polyhedron With
0,1-Vertices*, J. Res. NBS 69B (1965), 125–130，p.126 Theorem (P)：
[NIST 原文](https://nvlpubs.nist.gov/nistpubs/jres/69B/jresv69Bn1-2p125_A1b.pdf)。
原文描述普通匹配的凸包：非負座標、每點 incident sum 至多1、奇數點集
內部邊座標和至多 `(size−1)/2`。

在該凸包取所有頂點 incident sum 恰1的 face。任何此面上的凸組合只能使用
完美匹配：每個頂點的被覆指標至多1，平均恰1，故每個正權匹配都覆蓋它。
再用 `|X|=2x(E(X))+x(δ(X))`，得到本證所需形式

\[
P(Q)=\operatorname{conv}\{\chi_M:M\text{ perfect matching}\}
=\{x\ge0:Ax=\mathbf1,\ x(\delta(X))\ge1\text{ for every odd }X\}.
\]

其中 A 是無向、無符號的 vertex–edge incidence matrix。
這個 face／cut 轉換在本段完成；沒有把奇環補圖條件放入 P(Q)。

文獻核對：NIST 原 PDF 直接開啟 timeout，精確搜尋同一原 PDF 的 p.126
取得 Theorem (P) 與三組約束原頁內容；書目與 theorem 位置已核對。
[Kothari–Carvalho–Lucchesi–Little v3](https://arxiv.org/pdf/1803.08713)
的 Corollary 9、Proposition 10 提供獨立一致性核對：essentially
4-edge-connected cubic 圖是 brick／brace，brick 的互依邊對刪去後是二分圖。
後兩個結果不是本證的額外定理前提。

## 2. 只有頂點等式決定 affine hull

**Lemma A.** 設 Q 是3-edge-connected cubic 圖，且每個3-edge cut都是
單點或其補集的 cut。則

\[
\operatorname{aff}P(Q)=\{x:Ax=\mathbf1\}.
\]

**證明。** 令 `x*=1/3` 逐邊成立。任意奇數點集 X 的 cut 大小為奇數，
因 `3|X|=2|E(X)|+|δ(X)|`。3-edge-connectivity 使大小至少3；大小3
只能是單點 cut，其約束已由 Ax=1給出，其餘奇數 cut 大小至少5。
所以 x* 滿足全部非負與 odd-cut 約束，且除頂點等式外都嚴格滿足。

更明確地，任取 `d∈ker A`，若 d 非零，可取
`0<t<1/(6 max(1,||d||_1))`。則 `x*±td` 逐邊仍正，頂點和仍1。
單點 cut 的 d 和為0；其餘奇數 cut 的座標和至少
`5/3−t||d||_1>3/2>1`。故兩個擾動都在 P(Q)。
全部 ker A 方向均可作雙向微擾，affine hull 結論成立。□

這同時保證 Q 有完美匹配，不必另用 Petersen 定理，也不必先假設 Tait 可染。
非平凡 tight cut 若存在，x* 會使其大小必為3；故本域也沒有非平凡 tight cut。

## 3. 普通互依邊對的精確例外

固定不同邊 e,f；令 `h=1_e−1_f`，`H=Q−{e,f}`。
Q 的3-edge-connectivity 保證 H 連通。

**Theorem B.** 在 Lemma A 的圖域內，下列兩種情形恰有一種：

1. 存在一份普通完美匹配含 e、不含 f，並存在另一份含 f、不含 e。
2. H 是連通二分圖，且在其二分 `(U,W)` 下，e 的兩端同在 U、f 的兩端
   同在 W（或交換 U,W）；所有完美匹配都同時含 e,f 或同時不含。

**證明。** 若所有完美匹配都有 `χ_M(e)=χ_M(f)`，則由 Lemma A，h
在 ker A 上為零。有限維線性代數給 `h=A^Tλ`。因此每條 H 邊 uv 都有
`λ_u+λ_v=0`。若 H 有奇環，沿環交替會迫環上 λ 為0；連通性再迫
所有 λ 為0，與 h_e=1 矛盾。因此 H 必為二分圖。

沿 H 的路徑，λ 在二分 U 上恆 t，在 W 上恆 −t。由 h_e=1、h_f=−1，
t 非零，兩條被刪邊都不能跨二分，且分別位於兩個不同 parts。

反向若上述二分存在，cubic 的 degree 和給
`3|U|=|E_H|+2=3|W|`。對任何完美匹配 M，跨二分的匹配邊數相同，
而 U、W 的內部匹配邊只有 e、f，故
`|U|−2χ_M(e)=|W|−2χ_M(f)`，從而兩指標相等。

最後，若不在上述例外，h 不能在 ker A 上為零，故有 d 使 `h·d>0`。
Lemma A 的 `x*+td`、`x*−td` 分別使 `x_e−x_f` 正、負。它們各是
完美匹配的凸組合，故各有一份匹配使該差為1、−1。
這補足「兩個方向」的量詞，並非僅排除所有匹配相等。□

**Corollary C.** 若 Q 有一條避開 e,f 的奇環，則兩個方向的普通分離
完美匹配都存在。

不能只用「沒有2-edge cut」代替上述判準：K4 的對邊是例外2。
五角柱也有例外2，且它沒有非平凡3-edge cut。故無非平凡3割本身不足。
這裡稱「二分例外」，沒有額外宣稱 H matching covered 或把它直接命名為
removable doubleton；那個名稱有額外條件。

## 4. 平面原圖的度數排除二分例外

**Theorem D.** 設 T* 是四連通簡單球面三角化圖，指定兩條互不相交原邊
`a1,a2`，其四個端點集合為 S。假設 S 以外的每個頂點度數至少5。
取同一 embedding 的對偶 Q，指定 `e=a1^∨,f=a2^∨`。則兩個方向的
普通分離完美匹配都存在。

**證明。** 四連通給 T* 每點度數至少4，且無 separating triangle。
球面對偶 Q 是 cubic，至少3-edge-connected，且無非平凡3-edge cut。
具體地，大小小於3的對偶 bond 會對應原圖長1或2的 cycle，與原圖簡單
矛盾；任何3-edge cut 在3-edge-connected圖中必為 bond，對應原三角形。
原三角形為面，故其對偶割只隔一個頂點。

Euler 曲率等式為

\[
\sum_{v\in V(T^*)}(6-d(v))=12.
\]

S 只有四點，各度至少4，所以 S 的曲率和至多8；S 外各度至少5，因此
正曲率只能由五度點給出，每點貢獻1。S 外至少有4個五度點。
任取其一 v。其對偶面邊界是一條長5的 cycle，且因 v 不在 S，完全避開
e,f。套 Corollary C 即得。□

本定理可用更弱的假設「S外至少有一個奇度點」替代所有度數界；上面的
曲率只是從既有來源資料供應這個前提。一般四連通性本身不供應該度數界。

## 5. 接回既有 T/T0 來源

原來源、識別和完整 fibre 雙射沿用凍結的
`audits/2026-10-14-c4-triangle-core-b66f592/PROOF.md`。
本輪沒有修改原圖、接點、原 rotation、指定面或色框。

| 分支 | 原指定邊 | S以外的度數事實 | 本輪結論 |
| --- | --- | --- | --- |
| `d_G(b)≥5` | xy、zb | z,x,y,b 以外每點原度至少5；T四連通 | 兩方向普通分離匹配存在 |
| `d_G(b)=4` | xy、pq | z度至少6；除x,y,p,q以外每點至少5；T0四連通 | 兩方向普通分離匹配存在 |

T 支可更強：z度至少7，x,y,b度至少4，其他點至少5，故這四點以外
至少7個五度點。任意兩條原邊的端點合共至多4點，故總有五度點避開它們；
所以 T 的對偶中**任意兩條不同邊**皆能被普通完美匹配雙向分離。
T0 支本證只對具名 xy、pq 作此結論。

來源的全域最小性、小圈條件、附件與空 fibres 仍留在原來源契約中；
本輪是由其已證的四連通與度數後果作推論，並未反稱這些後果足以實現來源。

## 6. 奇環補圖仍是精確剩餘義務

令

\[
\omega_{e,f}(Q)=\min_{M\text{ perfect},\ |M\cap\{e,f\}|=1}
\#\{\text{odd cycles of }Q-M\},\qquad\min\varnothing=\infty.
\]

Q 是 cubic，Q−M 是 spanning 2-factor，且 |V(Q)| 為偶數，因此奇環數
必為偶數。本輪證合法來源 `ω∈{0,2,4,…}`，排除了 `ω=∞`。
既有 Tait 判準要的是 **ω=0**，這一步仍 OPEN。

本證對普通 P(Q) 的 affine hull 作微擾；不能在
`conv{χ_M:Q−M only even cycles}` 沿用同一 affine hull。
Petersen 具名控制每份匹配的補圖都是兩個五環，普通分離仍存在；
此控制非平面，僅證普通推論不含奇環消去，不是合法來源反例。

普通演算法的兩個方向也可寫成：含 e、不含 f 的完美匹配存在，恰等價於
`Q−V(e)−f` 有完美匹配，因刪去／補回 e 給雙射。本輪對合法來源已證
這兩個殘圖都可匹配。因此再找它們的 Tutte 障礙不能作來源主攻；接下來
應研究保指定分離的奇環消去，或偶補匹配凸包中額外的 affine equality。

沒有新來源實現、無界 Tait 解鎖、一般 K 界提高或 Lean theorem。
