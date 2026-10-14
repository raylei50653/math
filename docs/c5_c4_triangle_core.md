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
---

# C4 指定延拓壓到四連通三角化圖

2026-10-14。**新的任意大小結構化約；無界延拓仍 OPEN，K≤22 與 k≥23 不變。**
來源沿用 [C5→C4 橋](c5_c4_boundary_pivot.md)的 no4ct 全域最小來源契約，
完整證明及實際重播見 [本輪報告](../audits/2026-10-14-c4-triangle-core-b66f592/REPORT.md)。

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

132 份既有圖的264份完整 fibre等式、192份球面控制中157份符合前提者的
10,895個具名開口均核對通過。另保存真圖的「無一步出口、但有兩步出口」
反控制。有限控制沒有真正目標來源，不構成無界排除；紙面、Python與
未新增Lean的界線見報告。當前接續入口由 [Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口)維護。
本次整理、封存還原與發布重播另見 [發布紀錄](history/2026-10-14-c4-triangle-core-publish.md)。
