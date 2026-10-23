# 原 C9 距四雙接點：一種 pair、至多兩點

2026-10-23；BASE `cb8f8593e273a7426ecadd59797a6e643cc4768e`。
固定 [SOURCE_CONTRACT](../SOURCE_CONTRACT.md) 的同一全域最小 no4ct、完整
Σ932、h=4 原來源。這不是在932內另取最小圖。全部二十份原 annulus
名字、attachments、rotation、820列及完整空／非空 fibres 都照原合同保留。

**新結論：所有距四雙接點只能使用同一個原 C9 pair；這個 pair 至多有兩個
原內點，若有兩個，它們必有原邊相連。** 沒有排除這一／二點情形，也沒有
排除無距四雙接點的原來源。一般932、h≥5、smaller bad、K∞、Lean仍OPEN；
現行共同k≥23不變。

## 1. 原來源前提與有界側

寫原有序 induced C9 為 `C=(c0,...,c8)`，`I=V(H)\C`。指標mod9。
繼承的來源事實為：原有界面皆三角形；`d_H(C)≥4`、`d_H(I)≥5`；
原C3／C4 cap空，原C5 cap空或恰為W5；內點的任兩個C contacts距離只能為
1或4。[T2原度數／contact證明](../frozen/audits/2026-10-13-c9-932-source-d521163/geometry/PROOF.md)
及其[原cap前提](../frozen/audits/2026-10-13-c9-932-source-d521163/frozen/audits/2026-10-13-c5-no4ct-frontier-6943561/c9/geometry/PROOF.md)
分開保管。[第二輪](../frozen/audits/2026-10-23-three-mask-round2-cb8f859/932/paper/PROOF.md)
已證每個I點至多兩個C contacts。

所以接相鄰兩點者恰為該原C邊的面第三點t_i：形成的原C3有界側在C內，
原C3 cap空，故它就是原邊的內側三角面。九個t_i互異，且各自完整C contacts
恰為該邊兩端。本輪只追其餘可能的二接點

`P_i={c_i,c_(i+4)}`，`i=0,...,8`。

所有下述二邊路的開部都嚴格在原C內。以這些路及原C邊構成的簡單圈，其
有界開部亦在C內，沒有原B或外側attachments。它們的圈點都是原H頂點，
因此具名原small-cap定理適用；沒有用一般平面圖可染性。

## 2. 不同 pair：27個交錯與9個原C5 pocket

任兩個不同P_i、P_j，在九圈上只有兩種位置：

- 27對沒有共同端點，四個端點沿原C交錯；
- 9對共享一個端點a，另外兩個端點b、d在原C相鄰。

這個固定位置事實可直接由P_i重建，獨立checker逐份核對全部36對。
它不枚舉來源圖，也不假定任一pair已實現。

假設原點x接P_i、原點y接P_j。無三接點已保證x≠y。在第一種位置，原路
`c_i-x-c_(i+4)`與`c_j-y-c_(j+4)`除端點外在C內且互不相交。
交錯四端點的Jordan分離卻迫它們相交，矛盾。

第二種位置中，原路`a-x-b`、`a-y-d`和原邊`bd`形成簡單原五圈

`Q=(a,x,b,d,y)`。

它的有界側是同一原H的一個C5 pocket。五條可能對角線中，`ab,ad`是原C弦，
故不存在；`xd,yb`各會使x或y有三個C contacts，故不存在。只剩`xy`。
若cap空，三角剖分五邊形需要兩條不同對角線，只剩一條不夠。若cap為W5，
其原中心z接全部Q，尤其同時接三個不同原C點a、b、d，違反無三接點。
兩個原cap分支都矛盾。

因此在任意內側大小的同一來源中

`|{P_i : 存在原x∈I，N_H(x)∩C=P_i}| ≤ 1`。                 (1)

此處的xy是否原邊不影響矛盾；空cap最多只有這一條可用對角線。

## 3. 同 pair：空原C4 lens及第三條路

固定同一pair `{a,b}=P_i`。兩個不同原中心x、y的路`a-x-b`、`a-y-b`
形成簡單原C4 `L=(a,x,b,y)`。其有界側在C內，是原C4空cap。原三角化需要
一條對角線；`ab`是被禁止的原C弦，所以必為**有界側的原邊xy**。因此原lens
恰由兩個空原三角面`axy,bxy`構成，沒有私有點、附件或隱藏完成成本。

若同pair有三個原中心，三條內部互斥a–b弧在原disk內有線性順序。從a的
原內側rotation依序取最外兩條，它們構成的原C4有界側嚴格包含中間弧的
中心。因原C其餘點都在這個C4的無界側，這確是上述原內cap，而非錯取含B
的一側。它非空，直接違反原C4 cap空。

故

`每個P_i至多兩個原中心；若恰有兩個，原xy邊被迫存在。`       (2)

這個證明甚至不需要用五度下界。不能把兩中心當成三中心的四度矛盾；兩中心
可以分別在lens兩側接任意大的原cell。

(1)–(2)給每份原collar的19份**必要接觸模板**：沒有距四pair，或選9種pair
之一並有一／二個中心。二中心按原嵌入定義x靠短C弧、y靠長C弧。它們是
`1+9×2=19`份接觸資料；不是19張來源圖、19個完整relation或正支持解。
合二十份具名collar為380份必要模板。單接點、零接點及所有cell內點均無大小界。

## 4. 同一原H的C6／C7 cells及完整fibre雙射

有一個pair時，令a=c_i、b=c_(i+4)。短弧有4條C邊，長弧有5條。
若只有一個中心x，原二邊路a-x-b分出原induced cells

`D+=(x,c_i,c_(i+1),c_(i+2),c_(i+3),c_(i+4))`，

`D-=(x,c_(i+4),c_(i+5),c_(i+6),c_(i+7),c_(i+8),c_i)`。

它們沿同一原路a-x-b相交，嚴格內部互斥，沒有跨cell原邊。若恰有兩個
中心x、y，取x靠短弧、y靠長弧；D+用x，D-用y。兩cell只交於a、b，原圖
其餘部分正是空lens的兩個三角面及原邊xy。這些邊界induced，因原C無弦，
且x／y的完整C contacts已恰為a、b。所有原頂點、原邊及有向面都在此分解中。

固定一份完整literal proper C9 row σ，令α=σ(a)、β=σ(b)，
`K={0,1,2,3}\{α,β}`。令F⁺κ(σ)、F⁻κ(σ)為同一固定原D⁺、D⁻的**全部**
full lifts，沿各自原C弧取σ、原中心色為κ。定義保留所有空fibres。

單中心的限制／聯集給真正集合雙射

`F_H(σ) ≅ ⨆_(κ∈K) F⁺κ(σ) × F⁻κ(σ)`。                  (3)

雙中心的原xy邊則給

`F_H(σ) ≅ ⨆_(κ,λ∈K, κ≠λ) F⁺κ(σ) × F⁻λ(σ)`。            (4)

各份product共同頂點的literal colors完全相同；(4)的原xy邊proper，兩個原
三角面也proper。反向聯集正是同一原H的一份full lift，各sector因中心色不同
互斥。沒有新點、新邊、替代來源或可選completion。

固定α≠β時，K有兩色，(3)、(4)的完整count matrix都是**兩個**非負outer
products之和，只得rank≤2。固定α=β時，K有三色；(4)可按κ分組成
`Σκ Aκ(u)·(Σλ≠κ Bλ(v))`，故兩情況都只得rank≤3。此處u為短弧三個
中間點的literal tuple，v為長弧四個中間點的literal tuple；矩陣大小分別
20×61及21×60。絕不能沿用第二輪三色anchors迫第四色唯一時的rank-one
rectangle規則；也不能對兩cell各自正規化後接合。

## 5. 固定幾何與full-lift控制

`certificate.json`保存36份不同pair阻礙、9份原C4 lens、全部19模板及二十份
原合同綁定。獨立checker不import producer；從九圈位置重建全部分類，核
原annulus完整canonical SHA及原C9真名。原820×10 annulus fibres（含空）
及full lifts照凍結authority保留；本輪沒有新增任何無條件C9 row deletion，
也沒有重跑第二輪180份刪除或外部C4 census。

另有兩張具名有向disk，分別有一／二個距四中心；其嚴格內點數為12／13。
checker核逐邊兩側、完整links、Euler、所有度數、原C邊面第三點與全部C
contacts；還枚舉控制圖的全部C3／C4／C5簡單圈，以原面dual判定有界側。
全部C3／C4皆空，C5皆空或W5。這只校準控制圖，沒有重證任意來源small-cap定理。

對每張控制的同一C6／C7分解，checker逐full vertex-color tuple比較(3)/(4)
的Cartesian union與直接whole graph枚舉。在共同literal anchors `(a,b)=(0,1)`
時，各有1220份完整C9 fibres，其中536空，whole full lifts各2000份。
在共同anchors `(0,0)`時，各有1260份fibres；單中心354空、2772 lifts，
雙中心90空、5544 lifts。每份空／非空fibre都比較，不只總數。

兩張控制還給rank-one誤用的具體反例。同一anchors `(0,1)`，取短弧tuple
`u=(1,0,2),u'=(1,0,3)`，長弧tuple `v=(0,1,0,1),v'=(0,2,0,3)`，
實際完整count minors分別為

`[[4,2],[4,6]]`及`[[4,6],[4,2]]`，行列式為+16、−16。

兩份皆是同一控制圖、同一literal frame的真實full counts，不是抽象可行表。
rank-one推論狀態為`counterexample`；full-lift接合控制為`triggered and holds`。
控制沒有原B、完整Σ932或全域最小性；完整來源狀態一律`not triggered`，
不能把它們當成原來源實現。共同k≥23也不適用於這些不帶原B的控制。

## 6. 精確停止點

本輪排除的是兩個**不同**距四pair共同出現在原來源的分支及同pair三中心
分支。單pair一中心／兩中心尚未排除，無距四接點分支也仍OPEN。原接合
(3)–(4)是任意大小必要條件，沒有本輪計數錐、rank-two補閉或可行解宣稱。

下一窄義務是利用同一原C6／C7兩cell的完整關係與原annulus，排單pair的
兩sector共同實現，或建立可回填的具名化約；不能從分別可行的兩cell推來源。
一般932、h≥5、smaller bad、K∞及新Lean仍OPEN；共同k≥23保持不變。
