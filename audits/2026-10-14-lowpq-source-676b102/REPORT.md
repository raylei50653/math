# 低 p/q 真實來源：相鄰框點至少六度

2026-10-14。BASE `676b1024715f24a0d969fba90baab21b756406e2`。
本輪在獨立 detached worktree 研究；把上一輪尚未提交的
[相對共面識別](../2026-10-14-cofacial-fibres-676b102/REPORT.md)及五份採納文件
另外凍結為輸入，見 [INPUTS](INPUTS.json)。BASE 與這份工作樹疊加層分開記錄。

**新結果是 `p=5 ⇒ a≥6`，反射得 `q=5 ⇒ c≥6`；不是 p、q 普遍至少六度。**
它排除任意大小的 `p=5,a=5` 原來源子支及反射側；接上前輪已排的 a=4，
低 p 現在只剩 a≥6。一般 `K≤22=K≤5`、共同 k≥23、高 p,q 條件 k≥28 均不變。

## 1. 同一來源與交付範圍

G 在所有完整 C5 關係不屬 K132 的合法有限簡單 disk 中先取最小內點數 k，
再取最大邊數；原框共同對齊 `B=(x,y,a,b,c)`，完整關係為 932／933／941。
固定 `d_G(x)=d_G(y)=d_G(b)=4`；所有度數均指原 G。
保留原五 apex `(r,t,p,q,s)`、T0 的指定面 zxy／zpq，以及 R=T0−{x,y}
在原框 `(z,s,r,t)` 的完整 mask13 與逐份 full-lift 條件。

| 任務 | 本輪結論 | 精確證據／停止點 |
| --- | --- | --- |
| 1：低 p/q | p=5⇒a≥6、q=5⇒c≥6；新完整 ABABCAB fibre；指定 ms、mt 非邊 | [主證明](pq/PROOF.md)；p=5,a≥6 仍 OPEN |
| 2：r=6、319 | 原 collar 接點對 r-link 的指定邊子支排除；接入上述低 p/q 新界 | [r6 幾何](r6/PROOF.md)；r6p5、r6q5、319 全支仍 OPEN |
| 3：高 r 低 t/s | p=5,a=5,t=5 及反射側被任務1整支涵蓋 | r≥7,t=5,a≥5 的其餘來源仍 OPEN；未擴張 C6 模型 |
| 4：degree-excess | 依 Σ、h、低／高 p/q、r 原度數分類，保留完整剩餘區間與 k≤27 預算 | [活躍來源表](classification/SOURCE_TABLE.md) |
| 5：一般 T／T0 | 核對原指定染色與 Tait／偶補匹配缺口；列穩定可重用引理 | [審查及長期界線](classification/REVIEW.md)；未證一般延拓 |
| 6：採納／發布 | 合併前輪共面識別與本輪相連證據，保留舊證書及歷史錯誤 | [驗證](VERIFICATION.md)；發布狀態以 Git 為準 |

## 2. 新共同 fibre 與來源排除

p=5 時原 link 為 `(a,b,q,ell,m)`，T0 link 為 `(z,q,ell,m)`。
前輪已排 a=4，故 D=T0−{x,y,p} 的兩個實際面
`Q=(z,s,r,t)`、`P=(z,q,ell,m)` 只共享 z。

首先把小 cap 幾何的推論明列出來：若原 ellr 是邊，proper C5
`(y,a,p,ell,r)` 的有界側含 t；原小 C5 定理迫該側恰為中心 t 的 W5，
所以 tp 是邊，進而 a=4，矛盾。因此 ellr 不存在。
這一步是既有來源幾何的顯式推論，不另冒稱新的獨立全支排除。

在 Q 面內畫 zr 弧，在 P 面內畫 zell 弧。兩弧只共享 z，形成嵌入樹；
識別類 `{z,r,ell}` 內三對皆非邊，收縮後是 loopless planar quotient。
D 有 k 點，商圖有 k−2 點；在其一條邊旁接三個新點成外 C5，內點數
為 k−4<k。全域最小性及 K132 非空性給一份完整商圖染色。

回拉到同一 D，令 z=r=ell=A。p 鄰點 `(A,q,A,m)` 至多三色，故至少
有一個 p lift。原 R 的 ABAC 空，迫 s=t=B；對這份 D 染色的**全部**
p lifts，原 ABAB 條件又迫 pq 恰用 C,D。令 q=C；若 m≠B，則 p=B
會是合法 lift，立刻矛盾。因此 m=B，唯一 p=D。

已證七接點 `(z,s,r,t,q,ell,m)` 的完整 **ABABCAB fibre 非空**。
其全部 xy 接回恰為 CD／DC。因同份染色 s=t=m，ms、mt 不能是原邊。
若 a=5，原 a 的完整 fan 正是 `(y,t,m,p,b)`，必有 tm，矛盾。
故 p=5⇒a≥6。反射整份來源、接線與色框得 q=5⇒c≥6。

舊 ABABCBC 與新 ABABCAB 都在同一 D 上各有完整染色，**不是同一份染色**；
不能把兩者的等式逐項合併。完整來源同時負有這兩個存在義務。
本文未以四色定理、獨立面 witnesses、有限 survivor 或計數模型替代此論證。

## 3. 原幾何、有限控制與證據層

三個 subagent 分別負責低 p 主線、r6／高 r 幾何、來源分類與獨立審查；
整合者提出三點共同識別，低 p 主線與分類審查分別重證其合法性及全部 lifts。
較弱的 a=5,m=5 與 a=5,t=5 探索被完整 a=5 排除涵蓋，保留探索記錄，
不重複計作三項互相獨立的突破。

主 checker 保留局部完整色列、全部合法 cap lifts、空格及負控制；
[整合者獨立原邊核算](review/direct_lifts.py)不 import 主 checker，從全部
4^7 標號指派直接枚舉原兩面邊及 4^3 個 x,y,p 接回。
1764 份 proper face 指派中，324 份滿足三點識別；全 lifts 失敗的恰為
ABABCAB 的 24 個全域色置換，加入 ms 或 mt 原邊即無存活列。

有限核算只覆核局部色算術。任意大小結論由原旋轉、小 C5 cap、同面嵌入樹、
相對最小性與完整染色回拉的紙面證明給出。未新增 Lean theorem，未重新
跑 plantri、外部完整枚舉或舊整數必要模型的求解；舊計數證書只做只讀重播。
`lake build` 只驗證現有 Lean library，不宣稱新來源論證已形式化。

## 4. 採納與停止條件

Closure scope：固定 x,y,b 四度的完整 no4ct 最小來源，排除 p5a5／q5c5，
並採納具名原邊限制。沒有排除整個 p5、r6p5、r6q5 或 mask319。

Updated：本報告、證明與證據、C4 父入口、Kempe 導覽、STATUS 對應索引、
no4ct 直接入口及 synthesis 的 C4 列。

Reviewed-unchanged：README、HANDOFF 的研究線路由；一般 K≤22／k≥23、
高 p,q⇒k≥28 的條件域、一般 T／T0、外部枚舉信任層與 Lean 宣稱。

Remaining OPEN：p5a≥6 與反射、p=q=5 時 ell≥6 的共同來源、r6 的 319、
r≥7 的原 C6、高 r 低 t/s 殘支、一般指定 T／T0 染色及合法保壞嚴格下降。
E-ARC2、C8 RING、高 h 與 W5 縮減保留各自研究線，不在此輪全面展開。

Propagation stop：父摘要與直接 consumers 的低 p/q 界已改變，因此更新到
這些層；一般定理未變，不擴大其他研究線。下一輪從
[Kempe 導覽](../../docs/c5_kempe_guide.md)及本輪來源表接續。
