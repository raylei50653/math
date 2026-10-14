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
---

# C4 指定延拓壓到四連通三角化圖

2026-10-14。**無界延拓仍 OPEN，一般 K≤22 與 k≥23 不變。**
本日後續 [C4-MASK13-JOINT6](../audits/2026-10-14-c4-mask13-joint6-fdd3e22/REPORT.md)
已補上 ABCB 的同份 fibre 分解及高 p,q 子域的 k≥28。
[返回單射與 C4／C5 遞迴](../audits/2026-10-14-c4-c5-recursion-fdd3e22/REPORT.md)
進一步排除 r 原五度全支；r 原六度時也迫 s,t 至少六度，七接點 C5 關係只留271／314／319。
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
| r 原六度 | 刪 r 露出 C5，保留 p,q 後完整關係只可能271、314、319；再剝除與同圖交換迫 s,t 原度數≥6 |

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
| p=5；q=5對稱 | 以T0−p的原link作外框，完整C4支持恰14；rainbow分成兩個完整fibre palette sectors，單低度支仍OPEN |
| p=q=5 | pq的另一面頂點ell原度≥6；交換指定面角色後使用原返回單射，未排ell≥6支 |
| a=4；c=4對稱 | 直接刪t的424子支被外面z=r商圖的較小來源可染性排除，故t≥6；反射給s≥6，932／933／941均適用 |
| t=5；s=5對稱 | 必a≥5；直接刪t後的C5完整支持只留956／1012／1020，仍保內部p,q逐列full lifts |
| 932／933且a=4 | 整份原圖旋轉給p≥6；p=6⇒t,q≥6。若k≤27，必q=5、p≥7 |
| 932且c=4 | 對稱旋轉給q≥6；q=6⇒p,s≥6。若k≤27，必p=5、q≥7 |
| r=7 | 刪r露出C6，必要全lift／Kempe模型保留26外框型、111joint orbits；沒有來源排除 |

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
