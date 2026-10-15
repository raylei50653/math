# 七接點完整關係的六階下界與有限域橋接

BASE: `6ddea32a81349821ad3724ae1652bddb9c6a7b04`。

## 1. 本輪實質結果及範圍

固定具名順序 `X=(z,s,v,w,t,p,q)`，把原 degree-six transfer 的
26 個共同 S4 軌道展開成 624 份具名賦色，記作 A。本輪證明並逐份驗證：

1. A 的投影接合階數恰為 **6**。全部至多五接點的投影仍誤收 96 份賦色；
   全部六接點投影恰等於 A。
2. 以下六接點條件與 A 的全部四接點投影合取，恰好定義 A：
   `s=t => {p,q} intersects {v,w}`。
3. 上述六點條件有明確 F4 消失式，且 96 份假陽性都違反該式。
   不引入輔助變數時，A 的消失理想無法只由各涉及至多五接點的多項式生成。
4. 兩份具名六點投影已足夠，scope 為 `(z,s,v,w,p,q)` 與 `(s,v,w,t,p,q)`。
5. 七點 relation 的每個非空五框 pq fibre 大小都是偶數；在 F4 直接加總
   指示值會使整個外框張量為零，雖然其 Boolean support 是 mask319。

這些是**既有必要允許表的精確邏輯及代數結構**。A 不是已知實際來源的
完整 relation，也不是對每個合法來源都可實現全部 26 列的聲明。
任意具名 r=6 來源的七點 relation 只保證包含於 A；其五框支援由既有
cofacial 引理恰為319。本輪沒有新排除任何平面來源，沒有提高 k 下界。

## 2. 凍結來源與同圖契約

`../INPUTS.json` 綁定八份 BASE 檔案，其副本位於 `../frozen/`。
具體資料來自 frozen `r6-319-enumeration/src/search.py` 的 `WORDS/PQ`，
並與 frozen `degree4/transfer.json` 的完整26軌道及624具名列數交叉核對。
checker 不匯入或執行舊 solver。

來源 G 的原框 `(x,y,a,b,c)`、apices `(r,t,p,q,s)` 與
`d_G(x)=d_G(y)=d_G(b)=4,d_G(r)=6` 均保持既有契約。
R 由既有識別 `a=c=z` 及刪除而得；U=R-r 的外框是 `(z,s,v,w,t)`。
七接點互異，原面 zpq 保留，恢復 r 恰加入 `rs,rv,rw,rt`。
原 r fan 的次序是 `(x,y,t,w,v,s)`。本輪不更換圖、不另行正規化 p,q，
也不新增關於 rotation 的推論。

局部 mandatory edges 是
`zs,sv,vw,wt,tz,zp,zq,pq`。其 proper 七點賦色共1440份（60個S4軌道）。
可選原邊 tp 或 sq 等來源子域，應再與這張具名表合取；本輪研究的是共同
必要上界，不把沒有列入的來源條件當成自動成立。

對一份完整 U 染色的七點限制 x，合法 r 色集恰為
`L(x)=F4 \ {s,v,w,t}`。因 r 的全部鄰點已列出，這些且僅這些色能把
**該同一份完整 U 染色**接成 R 染色。令 Q(x,r) 是 frozen R 必要條件：

- z=r：要求 s=t，且 pq palette 為四色中排除 z,s 的兩色；
- z!=r 且 s=t：要求 pq 至少包含未在 z,s,r,t 使用的色；
- z!=r 且 s!=t：要求 pq palette 恰為 {s,t}。

於是 `A={x: local-proper(x) and every r in L(x) satisfies Q(x,r)}`。
空 L 必須按全稱量化真值保留，不能被存在量化誤刪。

## 3. 一般有限域／完整關係橋接引理

令 K=F4=F2[omega]/(omega^2+omega+1)。對任意有限圖 H=(V,E)，定義

\[
 I_H=\langle z_v^4-z_v:v\in V;\ (z_u-z_v)^3-1:uv\in E\rangle.
\]

其 K 零點恰為 H 的所有 proper 四色染色，因非零元素的三次方為1。
設 `Gamma_V=<z_v^4-z_v>`，則逐點求值給

\[
 K[z_V]/\Gamma_V\cong\prod_{a\in K^V}K.
\]

右端是有限多個域的乘積，每個理想均為根理想並由其零點集合唯一決定。
故 `I_H=I(Col_4(H))`。對任意有序具名保留集 B，

\[
 I_H\cap K[z_B]=I(R_{H,B}),\qquad
 R_{H,B}=\pi_B\operatorname{Col}_4(H).
\]

證明第二式只需：B 上多項式在全圖每份染色上為零，等價於在其投影每個
B tuple 上為零。這是精確有限集投影，沒有代數閉包造成的虛假額外點。
有限域 Nullstellensatz 的外部標準形式見
[Ghorpade, A Note on Nullstellensatz over Finite Fields, p.2](https://arxiv.org/pdf/1806.09489)。
本節圖染色、共同接合和 all-r-lifts 應用由上述乘積環論證直接導出。

若 A_1,A_2 是兩張完整具名關係，先在共同色框識別它們的全部共用變數，
則在共同多項式環中

\[
 I(A_1\Join A_2)=I(A_1)+I(A_2),\qquad
 I(\pi_C(A_1\Join A_2))=(I(A_1)+I(A_2))\cap K[z_C].
\]

每個輸入理想都含自己變數的 field equations，因此理想和含全部共同
變數的 field equations，仍是根理想。若要把此式解釋為圖的接合，還須
原私有點互斥、所有共用接點已記錄、跨來源邊全有相應方程。
平面 rotation、外框順序與合法 disk 施工另屬來源資料，並未藏在純理想中。

**保存六／七接點與完整來源 lifts。** 只需把 B 選為全部六或七個接點，
而非預先刪去 p,q 的五框。若之後還要引用其它原頂點，其變數亦須保留。
要保留完整全圖染色纖維，保留 I_H 本身及到 B 的投影，或保留全圖 tuples
及映射；只保留消元後的 I(R_{H,B}) 會丟失內點延拓數及內點身份。
本輪的 r lifts 是全部指定 r 顏色及相應八點 tuples，**不是未知全圖 U
所有私有內點延拓的替代證書**。

對任何有限關係 S，可定義逐點指示多項式

\[
 P_S(x)=\sum_{a\in S}\prod_i(1-(x_i-a_i)^3),\qquad
 I(S)=\langle x_i^4-x_i,\ 1-P_S\rangle.
\]

每個 tuple 恰有至多一個 summand 非零，故此加總不會誤抵消。
checker 在全部4^7份賦色，以實際F4乘法核對 P_A 與上節逐個r量化的
獨立關係判定完全相同。

全稱 lift 的正確形式也可寫成 Boolean-valued F4 circuit。
若 L(x,r)、Q(x,r) 分別是合法 lift 與 R 允許指示值，則

\[
 P_A(x)=P_{\rm local}(x)\prod_{r\in K}\bigl(1-L(x,r)(1-Q(x,r))\bigr).
\]

這裡用乘積表示「沒有壞 lift」，而非任選一個好 lift；L 全零時乘積為1。

## 4. 六接點共同條件的紙面推導

在 x 屬 A 且 s=t=B 時，由邊 sv、vw、wt 可知 s,v,w 恰用三種不同顏色。
令 D 是第四色，則 r 的合法色唯一為D。又 z!=B，故 z 是 v、w、D之一。

- 若 z=v，R 的 `(z,s,r,t)` 是 ABCB 型；Q 要求 pq 含 w 色。
- 若 z=w，同理 Q 要求 pq 含 v 色。
- 若 z=D=r，R 為 ABAB 型；Q 要求 pq palette 恰為 {v,w}。

三種情況均推出

\[
 \boxed{s=t\ \Longrightarrow\ \{p,q\}\cap\{v,w\}\ne\varnothing.}
\]

這使用同一份 U 染色及其唯一合法 r lift，無獨立選色。
對應禁止多項式為

\[
 F=(1-(s-t)^3)(p-v)^3(p-w)^3(q-v)^3(q-w)^3.
\]

F在且僅在 `s=t and {p,q} disjoint {v,w}` 時為1。因此 `F=0` 是明確的
六接點必要式。它不使用 z，並對所有全域色置換成立。

## 5. 精確階數與有限證書

定義 `C_m(A)= intersection_{|S|=m} pi_S^{-1}(pi_S(A))`。
若一張 relation 可由原七變數上至多m接點約束的合取定義，它必包含
C_m(A)：每條真正在A上成立的scope約束都必包含該scope的完整投影。
故 `C_m(A)>A` 排除所有這類m階合取表示，不只排除某個選定算法。

完整核對結果：

| m | 與1440份local-proper賦色的交集大小 | 誤收 |
|---:|---:|---:|
| 1 | 1440 | 816 |
| 2 | 1440 | 816 |
| 3 | 1440 | 816 |
| 4 | 720 | 96 |
| 5 | 720 | 96 |
| 6 | 624 | 0 |
| 7 | 624 | 0 |

對m>=2，所有原邊約束已由投影蘊含；表中 m>=2 數字也是全4^7空間的
閉包大小。全部4點與全部5點閉包相同，差集的四個全域S4軌道代表是

`0102113, 0102131, 0120113, 0120131`。

以第一份為例：`(z,s,v,w,t,p,q)=(0,1,0,2,1,1,3)`，唯一合法r=3，
但原R的ABCB條件要求pq含2，故禁止。每個五點scope卻有A內完整七點
tuple與它相同。certificate逐一保存四份代表乘21個scope的84份見證，
附每份見證的全部r lifts；96份具名差集亦全部保存。
四份代表上F均為1，故

\[
 A=C_4(A)\cap Z(F).
\]

這證明精確最小arity為6。代數版本：任何涉及至多五個原接點且在A上
消失的多項式，在96份假陽性上也消失，因各scope都可lift到A。
故 I(A) 不可能由這類多項式（連同field equations）生成。
另一方面全部四點投影的消失理想加單一F已有精確零點A；其含field
 equations，故根理想性給出正好I(A)。**此下界不涵蓋使用輔助變數後
再消元的表示，也不宣稱每個實際來源的真實七點子relation都有arity6。**

另直接核對全部4^7份賦色得

\[
 A=\pi_{zsvwpq}^{-1}(\pi_{zsvwpq}A)
   \cap\pi_{svwtpq}^{-1}(\pi_{svwtpq}A).
\]

因此兩份具名六點指示多項式及field equations也能精確生成I(A)。
這是具名關係接合等式；未宣稱這兩張投影分別由可合法拼接的平面子圖實現。

## 6. 空纖維、all-r-lifts 與特徵2負控制

canonical外框依原十列順序，其完整pq纖維大小為
`[2,4,6,4,2,6,0,0,2,0]`；因此支援恰為319。
624份允許七點tuple中，288份沒有合法r lift，但必須保留；其餘336份
各有一個lift。certificate保存全部336份八點tuple、全部288份無lift
七點tuple、全部60份局部canonical rows的所有合法／壞r色，以及三個
空外框fibres。八點tuple均逐邊核對上述完整local skeleton加四條r邊。

若錯把存在量化實作成F4加法收縮
`sum_{p,q} P_A(z,s,v,w,t,p,q)`，每列偶數個1都抵消成0。
例如外框01023有六份允許pq，且都沒有r lift：Boolean存在為真，
F4總和卻是0。實際上這個錯誤收縮在全部十外框列都為0。
因此有限域理想消元與有限域計數加總不可混用。

## 7. 可重播性與結果層級

從repo root執行：

```sh
python3 -B audits/2026-10-15-f4-relation-6ddea32/checks/check_relation.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-15-f4-relation-6ddea32/checks/check_relation.py --check
```

`../logs/receipts.json` 保存正常、seed17、故意加入假陽性之損壞證書拒絕、
及exclusive-create覆寫拒絕的stdout/stderr/exit status與前後hash。
所有checks均重新核對凍結檔及live authority檔，要求drift=0。

| Claim | Status |
|---|---|
| 一般有限域／染色／具名接合橋接 | 紙面一般證明；未Lean化 |
| 原26軌道與all-r-lifts一致 | triggered and holds：完整有限核對 |
| 六點共同式、精確arity6及理想generator arity下界 | 紙面推導加完整有限證書 |
| 所有五點投影已足夠 | counterexample：96份完整具名假陽性 |
| F4直接加總等於存在量化 | counterexample：七個非空外框列全抵消 |
| 存在合法r lift是U列必要條件 | counterexample：288份必要表允許列無r lift |
| A由某個實際最小平面來源實現 | not triggered：未提供／建立來源 |
| 無界r=6來源排除、一般T/T0、K_infinity=K_<=5 | OPEN |

本輪不修改共享docs、不寫其他audit、不commit或push。
