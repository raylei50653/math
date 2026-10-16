---
docgraph:
  id: c5.c4-triangle-core
  family: [c5, c5.minimal-source, c5.no4ct]
  derives_from: [c5.c4-boundary-pivot]
  verified_by:
    - audits/2026-10-14-c4-triangle-core-b66f592/REPORT.md
    - audits/2026-10-14-c4-triangle-core-b66f592/PROOF.md
    - audits/2026-10-14-c4-triangle-core-b66f592/ADJACENT4.md
    - audits/2026-10-14-c4-triangle-core-b66f592/controls/check_quotient.py
    - audits/2026-10-14-c4-triangle-core-b66f592/controls/check_structure.py
    - audits/2026-10-14-c4-triangle-core-b66f592/controls/check_cap.py
    - audits/2026-10-14-c4-mask13-joint6-fdd3e22/REPORT.md
    - audits/2026-10-14-c4-mask13-joint6-fdd3e22/JOINT_FIBRES.md
    - audits/2026-10-14-c4-mask13-joint6-fdd3e22/SOURCE_GEOMETRY.md
    - audits/2026-10-14-c4-tait-lock-review-fdd3e22/REPORT.md
    - audits/2026-10-14-c4-tait-lock-review-fdd3e22/controls/check_matchings.py
    - audits/2026-10-14-c4-c5-recursion-fdd3e22/REPORT.md
    - audits/2026-10-14-c4-c5-recursion-fdd3e22/fibre/PROOF.md
    - audits/2026-10-14-c4-return-branches-a11d4bb/REPORT.md
    - audits/2026-10-14-cofacial-fibres-676b102/REPORT.md
    - audits/2026-10-14-lowpq-source-676b102/REPORT.md
    - audits/2026-10-14-r6-lowpq-3953c85/REPORT.md
---

# C4 指定延拓壓到四連通三角化圖

2026-10-14。**無界延拓仍 OPEN，一般 K≤22 與 k≥23 不變。**
2026-10-16 再續[R6-CAP-BARRIERS](../audits/2026-10-16-r6-cap-barriers-c4c3d99/REPORT.md)
以具名奇偶曲率排除單一W5／W7輪障礙；雙W5迫原s,t≤8、h≤6及精確度數餘量。
同一111族的跨割飽和與原五圈扇區定位當輪迫101單一五割必有弦。
後續[R6-CHORDED-FIVE](../audits/2026-10-16-r6-chorded-five-c4c3d99/REPORT.md)
再排全部101有弦五割，故其五割全為W5、單一五割整列排除；101只剩雙W5或非輪七割，110其餘割及偶補正值仍OPEN。

2026-10-16 後續[R6-JOINT-ZERO](../audits/2026-10-16-r6-joint-zero-c4c3d99/REPORT.md)
已任意大小排除固定三框點四度、r6來源的全單點Tutte障礙；
兩族普通失敗均須非單點5／7割，聯合偶補正值及完整319排除仍OPEN。

2026-10-15 後續[四輪具名路線](../audits/2026-10-15-route-round4-6ddea32/REPORT.md)：
合法T／T0已證指定邊普通PM雙向分離，偶補正值仍OPEN；r六度支的來源J四連通，
完整all-r為(e=f)⇔(e=g)，兩星disk W保留全部hub fibres並迫兩個二色缺集相等。
三標記普通障礙與Layer0二層共同圖均未完成319排除或保壞嚴格下降。
目前停止點見[Kempe導覽](c5_kempe_guide.md#3-停止點與保留缺口)，重播見[整理紀錄](history/2026-10-15-kempe-routes-publish.md)。

本日後續 [C4-MASK13-JOINT6](../audits/2026-10-14-c4-mask13-joint6-fdd3e22/REPORT.md)
已補上 ABCB 的同份 fibre 分解及高 p,q 子域的 k≥28。
[返回單射與 C4／C5 遞迴](../audits/2026-10-14-c4-c5-recursion-fdd3e22/REPORT.md)
進一步排除 r 原五度全支；r 原六度時也迫 s,t 至少六度。
[相對共面識別](../audits/2026-10-14-cofacial-fibres-676b102/REPORT.md)再把該C5支持由271／314／319縮為恰319；
同一T0的兩面共同商圖先證p=5⇒a≥5、q=5⇒c≥5；
[低p/q來源續進](../audits/2026-10-14-lowpq-source-676b102/REPORT.md)再以三點共同識別提高為 **p=5⇒a≥6、q=5⇒c≥6**，三種來源皆適用。
[共同W與原內圈](../audits/2026-10-14-r6-lowpq-3953c85/REPORT.md)再證r6p5的ell-v、ell-w原非邊及反射側對應結論；
固定x,y,b四度支有k≥ceil((3h+16)/2)，故k≤27⇒h≤12。
[其他返回分支](../audits/2026-10-14-c4-return-branches-a11d4bb/REPORT.md)再給
a=4⇒t≥6、c=4⇒s≥6；p=q=5時另一個原共同鄰點至少六度，單低p/q化成精確mask14。
來源沿用 [C5→C4 橋](c5_c4_boundary_pivot.md)的 no4ct 全域最小來源契約，
原T／T0證明及實際重播見 [前輪報告](../audits/2026-10-14-c4-triangle-core-b66f592/REPORT.md)。

寫原 C5 為 `(x,y,a,b,c)=(b0,b1,b2,b3,b4)`，H 外框為 `(u,a,b,c)`。指定 a=c 的染色中，
在外側識別 a,c 為 z、刪除 u，得到以 zxy 為外三角的簡單三角化圖 T。
原非相鄰框點的共同鄰點限制保證識別合法；不能對任意 C4 候選忽略平行邊問題。

固定 `(z,x,y)=(B,C,D)`，令 F_r 為 b=r 的所有完整染色。
原目標有雙射 `F_H(ABCB)≅F_C⊔F_D`，而 `F_H(ABAB)≅F_A×{0,1}`。
因此要找的是 T 中讓 b 取 C 或 D 的一份完整染色；來源確有 `F_A≠∅`。

| 原來源分支 | 已證結構 | 尚待證明 |
| --- | --- | --- |
| `d_G(b)≥5` | T 有 k+4 點且四連通；除 b 外其餘內點度≥5 | 固定外三角時，b 可取 C 或 D |
| `d_G(b)=4` | T 唯一分離三角形包住三度 b；刪 b 得 k+3 點四連通 T0 | 同一染色中，具名三角面 zxy、zpq 可使用不同色集合 |

第二支兩面只共享 z，四點 x,y,p,q 互異且只有 xy、pq 兩條互相間的邊。
T0 的四點度≥4、z度≥6，其餘度≥5。新推導亦給 H 的非外框四環全空；
induced 五環包至少兩點時，只可能原 B 或原 b 四度時的 `link_S(b)`，
兩個例外各包 k 點，不能套 `s<k` 的小代表引理。

進一步在原 `d_G(b0)=d_G(b1)=d_G(b3)=4`，即 `d_G(x)=d_G(y)=d_G(b)=4`
子分支，刪 x,y 得內點 `k−3<k`
的 R，合法接入相對 C4 七關係表。完整 cap 接回先拒 ABAC，相對平面可染性
再排12，故 **R 的完整 C4 關係只剩 mask13**。剩餘是六個原接點
`(z,s,r,t,p,q)` 的同份 full-lift 義務；mask13 尚未排除。
[精確命題與完整表](../audits/2026-10-14-c4-triangle-core-b66f592/ADJACENT4.md)
保留 `k−3<k`、`k−2<k` 及所有空 fibres。

目標失敗的精確殘題是：每份 R 的 ABAB 完整染色都迫
`{f(p),f(q)}={C,D}`，每份 ABCD 完整染色都迫 `{f(p),f(q)}={B,D}`。
須在同一份完整染色中打破其中一項共同強迫；四框 mask13 本身不保存這項資訊。

## 共同 Tait 化約與全染色鎖定

[採納整理與控制](../audits/2026-10-14-c4-tait-lock-review-fdd3e22/REPORT.md)
把兩支化為同一問題。將四色識別為 `F₂²`，定義 `Δ(vw)=f(v) XOR f(w)`：
T 支的 `b=μ(zxy)` 等價於 `Δ(zb)=Δ(xy)`；T0 支的兩面色集合相同
等價於 `Δ(xy)=Δ(pq)`。兩組指定原邊均互不相交。
球面 Tait 染色可沿原邊反向積分成一份完整四色染色，整圖共同換色可恢復
指定三角色框，並保持兩條色差是否相等。

令 `Q=(T*)^∨`，`T*` 為 T 或 T0，指定對偶邊為 ε₁、ε₂。完全失敗迫使
**每份** Tait 染色都令它們同色，且對另外兩色各自的雙色環都同時包含兩邊。
任意合法交換後也必重新滿足；只看當前雙環或一個 edge-Kempe 類不夠。
雙環共用同色邊，不能直接套互不相交跨路的 Jordan 矛盾；四連通排除
對偶非平凡三邊割，但鎖定是否迫出該割仍須證明。

更精確地，令 `M_even(Q)` 為補圖全由偶環組成的完美匹配集合，則

`存在完整 Tait 染色令 ε₁、ε₂ 異色 ⇔ 存在 M∈M_even(Q) 恰含其中一條指定邊`。

正二十面體控制確認合法互不相交位置可在整個對偶 edge-Kempe 類鎖定，
而另一類有成功染色；五角雙錐的全染色鎖定邊對則共享端點。
兩者均非完整最小來源反例。完美匹配判準涵蓋全部染色，不假設 Kempe 連通性；
原來源的位置、度數與小圈限制能否迫出所需匹配，及最小性接回，仍 OPEN。
本整理不提高任何一般或 JOINT6 條件大小界，也沒有新增 Lean。

## C4-MASK13-JOINT6 的共同 fibre 與條件界

[新紙面證明](../audits/2026-10-14-c4-mask13-joint6-fdd3e22/JOINT_FIBRES.md)
證每份 ABCB 完整染色的 p,q 必含缺失色 D，排除 BC／CB。
其全部 fibres 恰分為兩個非空部分：pq=CD 者與 ABAB 作 r-AC component
交換雙射，逐點固定 p,q；pq=BD 者與 ABCD 作 t-BD component 交換雙射，
可能同時交換 p,q 色值。因此 `n(ABCB)=n(ABAB)+n(ABCD)`，並保留完整集合對應。
有限六接點必要閉包由10列縮至8列，剩餘閉包非空；沒有證圖可實現或來源排除。

[原接點幾何](../audits/2026-10-14-c4-mask13-joint6-fdd3e22/SOURCE_GEOMETRY.md)
給出以下更窄結論；degree 均指原 G。

| 附加前提 | 新結果 |
| --- | --- |
| p,q 都至少六度 | R 是 k+1 點的 diagonal-forbidding 4-candidate；同一外部≤28計算給 k≥28 |
| 本分支 h=3 | 只剩 c04／c07-941，已採納 apex 下界滿足上列，故 k≥28 |
| 本分支完整932、h=4 | 只剩 c09-induced-932，同樣 k≥28 |
| r 恰五度 | 刪 r 的 mask7 共同表已由返回單射排除，故原 r≥6 |
| r 原六度 | 刪 r 露出 C5；全lift加兩個較小外面商圖迫完整支持恰319，並有 s,t 原度數≥6；舊三份計數模型保留 |

一般 p 或 q 原五度時，R 有四度內點，不能套用高 p,q 的候選界；
若 k≤27，這個低度情況必發生。無界八列殘題仍 OPEN；
[新證明](../audits/2026-10-14-c4-c5-recursion-fdd3e22/fibre/PROOF.md)已排除原 r=5 的較小 mask7。
因此原 r=5、高 p,q 的 k≥29 子域為空，不再作目前未解分支。
新的七接點狀態仍須保同份全部接回，純刪點的完成成本尚未嚴格下降。

### 其他返回分支與新的低度介面

[新分支證明](../audits/2026-10-14-c4-return-branches-a11d4bb/REPORT.md)全部限定於上述
原x,y,b四度的同一最小來源；degree均指原G，不提高共同k≥23。

| 附加原條件 | 已證結果／保留義務 |
| --- | --- |
| p=5；q=5對稱 | 以T0−p的原link作外框，完整C4支持恰14；rainbow分成兩個完整fibre palette sectors；同圖兩面識別已排p=5,a≤5及反射側，其餘低度支OPEN |
| p=q=5 | pq的另一面頂點ell原度≥6；交換指定面角色後使用原返回單射，未排ell≥6支 |
| a=4；c=4對稱 | 直接刪t的424子支給t≥6；新共同商圖另給p≥6。反射給s,q≥6，932／933／941均適用 |
| t=5；s=5對稱 | 必a≥5；直接刪t後的C5完整支持只留956／1012／1020，仍保內部p,q逐列full lifts |
| 932／933且a=4 | 整份原圖旋轉給p≥6；p=6⇒t,q≥6。若k≤27，必q=5、p≥7 |
| 932且c=4 | 對稱旋轉給q≥6；q=6⇒p,s≥6。若k≤27，必p=5、q≥7 |
| r=7 | 刪r露出C6，必要全lift／Kempe模型保留26外框型、111joint orbits；沒有來源排除 |

[共同來源補件](../audits/2026-10-14-cofacial-fibres-676b102/REPORT.md)保留D=T0−{x,y,p}的兩個實際C4面；
p=5時的原link接點m=t恰對應a=4，該整個子支已由同一商圖染色排除。
m與t互異時，七接點(z,s,r,t,q,ell,m)有完整ABABCBC fibre，迫ell s、ell t非邊。
[新來源證明](../audits/2026-10-14-lowpq-source-676b102/pq/PROOF.md)先由原小C5幾何得ell r非邊，
再在兩個實際面內共同識別z=r=ell，迫另一個完整ABABCAB fibre非空；
後者s=t=m給ms、mt非邊，與a=5的原tm邊矛盾，故p=5⇒a≥6，反射q=5⇒c≥6。
兩個fibre分別存在，不能合併成同一染色。p5a≥6及反射、r6的319仍OPEN。
[r6原幾何](../audits/2026-10-14-lowpq-source-676b102/r6/PROOF.md)另排第一層a/c鄰點接r的兩個私人link點；
[前輪來源表](../audits/2026-10-14-lowpq-source-676b102/classification/SOURCE_TABLE.md)的degree、旋轉與預算仍保留；
[本輪活躍域](../audits/2026-10-14-r6-lowpq-3953c85/REPORT.md#4-更新的活躍來源域與剩餘義務)把k≤27的h上界降為12。
原collar無弦、私人圖連通無葉且圈秩rho≥2，精確式2k=3h+12+E_C+rho給上述界。
r6p5在同一W的兩個合法商圖另迫ell-v、ell-w非邊，反射側取對應結論；兩份完整fibre聯集分別非空，整支仍OPEN。
[獨立有限枚舉](../audits/2026-10-14-r6-319-enumeration-676b102/REPORT.md)已排固定四度框支中r6的k=23、24，
因此r6另有k≥25；合上述任意大小幾何界，k≤27時只留25≤k≤27、h≤12，不能提高一般K≤22。

一般mask13另有缺色端點連通及條件式BC子fibre雙射，但返回落入允許的另一ABCB
sector，沒有空fibre矛盾。旋轉必保留兩個完整singleton fibres皆空的前提，
不可把上述p/q旋轉界直接套941。紙面、有限控制及獨立審閱分見新報告；無新Lean。

本輪七張明列圖的42份完整染色、14份集合雙射與有限閉包重播見
[驗證紀錄](../audits/2026-10-14-c4-mask13-joint6-fdd3e22/VERIFICATION.md)；真正目標來源0，未新增Lean。

前輪132 份既有圖的264份完整 fibre等式、192份球面控制中157份符合前提者的
10,895個具名開口均核對通過。另保存真圖的「無一步出口、但有兩步出口」
反控制。有限控制沒有真正目標來源，不構成無界排除；紙面、Python與
未新增Lean的界線見報告。當前接續入口由 [Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口)維護。
本次整理、封存還原與發布重播另見 [發布紀錄](history/2026-10-14-c4-triangle-core-publish.md)。
