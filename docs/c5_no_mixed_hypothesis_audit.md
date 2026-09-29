# No-mixed 三假設驗證：完整搬運、單框點化約與守恆禁色

後續（2026-09-29）：[增長完備性與共同分離](c5_no_mixed_growth_completion.md)
已從三個共同側弧位置直接指定排除配方，免查必要支援表地排除影響 R
的增長；結合無增長定理完成指定 p₁、p₂ 的存在性分離。下文未解描述
保留當輪語境；逐染色建構式 repair、完整 Σ 與一般出口仍未證。

後續（2026-09-29）：[無增長共同分離](c5_no_mixed_no_growth.md) 已用短側弧與
未見兩色的交換不變性，紙面證明所有 F 大小不增長時兩 roots 必有異色
pair。這不取代有增長時的局部排除，也未證完整的免表共同 repair。

後續（2026-09-29，基準 `3174f08`）：[統一局部篩選](c5_no_mixed_local_screen.md)
重算全部 2,240 個 singleton→pair 候選，守恆規則及非守恆原端點排除
2,208 個，另 32 個不影響 R；7,880 保留 joins 全有 root pair，涵蓋本頁
434 個舊失敗。此為共同局部規則的必要表覆蓋，尚非免表共同 repair；
本頁數字與當輪停止點保留。

後續（2026-09-29，基準 `98b26b7`）：本頁 [§3.1–3.3](#31-逐-root-不可搬運界)
補入不查支援表的逐 root 紙面界及 D_p 精確介面：**搬運全部可精確搬運的
原分量後，每個 root 至多剩一份未知 target 禁色關係**。雙不可搬運的
側型只可能 AA、AB、AC。新獨立 checker 重播 4,164 查詢、11,096 joins，
三種介面的 E_z、E_w 逐筆相同；434 個舊失敗 joins 分為 0／184／192／58。
這不新增 source 排除、target 接受或共同 repair 定理；本輪驗證與未重跑
範圍見[逐 root 紀錄](history/2026-09-29-no-mixed-root-transport.md)。
下列三 agent 分工與舊重播清單保留前輪語境，本輪未開 sub-agents。

2026-09-29，基準 `0ab88ce`。依使用者要求由三個 agent 分別驗證，主 agent
審閱證明、整合 checker 並重播。沿用[十五類總覽](c5_no_mixed_span_budget.md)
的圖類、任意大小必要支援覆蓋及原路徑引理；不重新枚舉來源圖。

**結果：完整搬運給出可直接證明的充分條件；單框點化約將未知原分量關係
減至至多兩份；守恆 singleton 不升為 target pair 有七類表依賴證書。**
尚未得到取代分類的共同延拓證明。全部 4,164 個 target 原已接受，本輪
沒有新增 source 排除或 target 接受。必要支援不是 disk 實現證書。

目前停止點與後續入口見 [weak-deletion 導覽](c5_weak_deletion_guide.md)。
本輪實際檢查及未重跑範圍見[驗證紀錄](history/2026-09-29-no-mixed-hypothesis-audit.md)。

## 1. 同一來源與三項問題

除 §2 的一般搬運引理外，完整沿用總覽 §1：M 有限簡單、B 為 induced C5
disk 外框、H=M−B 非空連通；q=01012 是非框邊 edge-minimal obstruction。
恰有相鄰 z,w 完整 degree=5，其餘內點完整 degree=4；H−{z,w} 每個原分量
C 恰接一個 root。U={0,1,2,3}，p₁=01021、p₂=01212。

S_C 是 actual boundary support；T_C(β) 是原 C 的完整有序接點關係，
F_C(β)=⋂_{τ∈T_C(β)}set(τ)。保留所有原接點、bridges、旁支、spokes、zw、
環序及共同字面色框。T_C 非空，source E_z(q)=E_w(q)={c}。
「飽和」仍專指二接點分量的 |F_C(q)|=2。

三項待驗證內容分別是：共同 source 色的完整搬運是否充分、單框點是否
真能集中未知關係，以及奇數 bridge palettes 換色是否必遭幾何阻斷。
下文區分一般紙面引理、沿用支援覆蓋的化約及依表判定的推論。

## 2. 完整搬運的充分條件，以及較弱版本

定義

\[
\Pi_C(q,p)=\{\pi\in S_U:\pi(q_i)=p_i\text{ for every }i\in S_C\},
\quad K_C(c)=\{\pi(c):\pi\in\Pi_C(q,p)\},
\]
\[
H_r(p)=\bigl(U\setminus p(N_B(r))\bigr)\cap\bigcap_{C\sim r}K_C(c).
\]

**引理。** H_r(p)⊆E_r(p)。若 H_z、H_w 有不同顏色 a_z、a_w，則 p 延拓。
此引理只需 no-mixed 與 M−zw 有 roots 同色 c 的 q 染色；不需要 disk、
degree、缺額或飽和前提。

**證明。** 固定一份 M−zw 的完整 q 染色 f。每個原 C∼r 選擇
π_C∈Π_C 使 π_C(c)=a_r，對 C 的全部頂點施 π_C；boundary 設為字面 p，
root r 設 a_r。分量內邊由置換保持 proper，C–B 邊由所有 actual support
上的對齊保持，C–r 邊由原接點全部避開 c 保持；root-spokes 由 H_r 定義
處理。a_z≠a_w 可接回原 zw。沒有跨分量邊或 mixed 分量，故全部原邊
均 proper。這也逐側證明 H_r⊆E_r。

各 π_C 只作用在原分量內部，所有附件仍對齊同一 p 與 a_r；沒有獨立
重命名 shared frame。完整 tuples 與中間路徑並未投影或刪去。

Π_C 非空恰等於 q、p 在 S_C 上具有相同的等色分割。令 φ_C 為支援給的
部分單射 q_i↦p_i，則 c 已見時 K_C={φ_C(c)}，否則 K_C=U∖p(S_C)。
這可只用 actual support 與 c 檢查，不需先知道 target relations。

**較弱的 G 判準。** 允許各原分量使用不同 source root preimage：

\[
G_r(p)=\bigl(U\setminus p(N_B(r))\bigr)\cap
\bigcap_{C\sim r}\ \bigcup_{\pi\in\Pi_C(q,p)}\pi\bigl(U\setminus F_C(q)\bigr).
\]

有 H_r⊆G_r⊆E_r(p)；若每個 incident Π_C 非空，則 G_r=E_r(p)。因為
完整搬運給 T_C(p)=πT_C(q)、F_C(p)=πF_C(q)，其像不依相容 π 的選擇。
G 的每個 local witness 都來自同一原 C；不同 C 的 source preimages
不必組成一份 source 整圖染色，但搬運後均避開同一 target root 色，
故 no-mixed 接合仍合法。不得把它說成搬運單一 M−zw 染色。

| 類型 | 查詢 | H 通過 | G 通過／全部分量可搬運 | 有不可搬運分量 |
| --- | ---: | ---: | ---: | ---: |
| AA | 644 | 364 | 364 | 280 |
| AB | 1,120 | 724 | 724 | 396 |
| AC | 48 | 20 | 24 | 24 |
| AE | 240 | 216 | 216 | 24 |
| BB | 1,776 | 1,296 | 1,296 | 480 |
| BC | 48 | 24 | 24 | 24 |
| BE | 288 | 288 | 288 | 0 |
| 合計 | 4,164 | 2,932 | 2,936 | 1,228 |

H 比 G 嚴格的四項是 AC80/p₂、98/p₂、279/p₁、290/p₁。例如 AC80/p₂
有 c=0、B_z={1,4}、B_w=∅，三份 (support,F_C(q)) 依序為
(014,{3})、(123,{2,3})、(34,{1})。H_z={0}、H_w=∅，但
G_z=E_z={0}、G_w=E_w={2}。Cw 可把 source 0 送到 target 2；Dw 可把
source 2 保持為 target 2。要求兩份都從 c=0 出發才造成漏失。
這是必要資料上的判準嚴格性控制，不是來源實現證書。

[搬運 checker](../scripts/c5_no_mixed_hypothesis_transport.py) 與
[逐查詢資料](../artifacts/c5_no_mixed_hypothesis_audit/transport.json)
保留 input SHA、具名支援、相容置換、H/G、完整搬運後的 root 關係；
另核對全部 32 支援子集、兩 target、四色 c 的 256 個等色分割控制。

## 3. 單框點化約與精確共同介面

對 p₁ 取 σ=(1 2)，則 σ(q)=02021，只需在 h=b₁ 把 2 改為 1；
對 p₂ 取 σ=id，只需在 h=b₂ 把 0 改為 2。令
A_h={C:h∈S_C}。若 C∉A_h，則 T_C(p)=σT_C(q)、F_C(p)=σF_C(q)。
因此不能以任何色置換搬運的分量集合 D_p⊆A_h。

**引理。** 在既有共同同序、正跨度且框邊內部不交的支援 lifts 下，
|A_h|≤2；若有兩份，其 hull 分別在 h 的相反方向終止／開始。

**證明。** 每份含 h 的正跨度 hull 至少占用 h 的一條相鄰框邊；h 在
hull 內部時兩條都占用。不同 hull 的框邊內部不交，h 只有兩條相鄰
框邊，故至多兩份；兩份時 h 必為兩個不同方向的端點。稀疏支援中的
空白框點不解除 hull 所占框邊。Cyclic cut 的 0、5 是同一框點的左右
lifts，未複製身份或顏色。每份跨度<5，由另一份正跨度分量保證。

此論證沿用[共同支援引理](c5_no_mixed_span_budget.md#21-同序支援與兩側框弧)，
不能改用彼此不相容的最短 hull；若容許零跨度分量或 root 樹的多區段，
必須另證前提。Root-spokes 的零跨度不計入 A_h，但接合時全部保留。

固定的是其它完整關係，不是一份 source 染色。精確介面為

\[
B_r(p)=p(N_B(r))\cup\bigcup_{C\sim r,\ C\notin A_h}\sigma F_C(q),
\quad E_r(p)=U\setminus\left(B_r(p)\cup\bigcup_{C\sim r,\ C\in A_h}F_C(p)\right).
\]

原圖延拓恰等於 (E_z×E_w)∖Δ 非空。至多兩份未知 F 必由各自完整原關係
計算；外部原分量仍可能供應必要的幾何路徑，不能從證據中刪除。

也可在原 lists 上表述這一變動。令 a=σ(q)_h、b=p_h；固定 root 色 t，
D_v(t) 收集除 h 外的實際 boundary 禁色及存在時的 root 禁色 t。
原 h 鄰點的舊、新 lists 分別是 U∖(D_v(t)∪{a})、U∖(D_v(t)∪{b})；
其他頂點不變。不能無條件用 (L_old∪{a})∖{b}，因其他外鄰可能仍禁 a。
每份分量可含任意多個 h 鄰點，這不是有限頂點 repair。

| 分量數 | 0 | 1 | 2 |
| --- | ---: | ---: | ---: |
| 不可色置換搬運 | 2,936 | 1,184 | 44 |
| Actual support 含 h | 152 | 1,736 | 2,276 |

44 份雙不可搬運查詢分 AA24、AB12、AC8，均接不同 roots；前輪只記為
表中統計，現在由下述 §3.1 給不依該統計的紙面證明。2,276 份雙含 h
查詢則有 **880 同 root、1,396 不同 roots**；A_h 仍不能預設每側一份。

[單框點 checker](../scripts/c5_no_mixed_hypothesis_anchor.py) 與
[逐查詢資料](../artifacts/c5_no_mixed_hypothesis_audit/anchor.json)
獨立解析分量／spokes，核對 2,082 份保存 placements、1,820 個三弧與
50 個不交雙弧控制，並逐候選核對完整式、anchor 式與 D_p 式相等。
容量／穩定子上界仍有 434 個失敗 joins（AA160、AB146、AC8、BB120），
原後續證書已排除它們；局部化本身尚不提供共同 repair 定理。

### 3.1 逐 root 不可搬運界

固定 §1 的**同一原來源圖**、字面色框及任一 proper boundary coloring p。
本小節及 §3.2 的 D_p 界不需 p 是指定的兩個 target；A_h 的單框點表示及
§3.3 的有限重播才限於 p₁、p₂。定義

\[
D_{p,r}=\{C\sim r:\Pi_C(q,p)=\varnothing\},\qquad
D_p=D_{p,z}\cup D_{p,w}.
\]

此集合不要與 source 預算中的數值缺額 D_r 混淆。沿用前提如下，並非
把「不查支援表」提升成「不依既有結構定理」：

1. [總覽 §1](c5_no_mixed_span_budget.md#1-適用前提與精確語義) 的 induced-C5
   disk、相鄰雙 degree-5、其餘內點 degree-4、no-mixed、minimal q-core，
   以及由 source 預算與原平面化約得到的 A–E 五側型。q、p 都 proper。
   不另假設 T4、target 拒絕或來源接受其他列。
2. [總覽 §2.1](c5_no_mixed_span_budget.md#21-同序支援與兩側框弧) 的共同
   同序支援 lifts：每個原分量的 hull 有**正整數跨度**，不同分量的
   hull 框邊內部不交；spokes 依原次序保留。兩側在這同一份 lift 上的
   區段 I_z、I_w 包含各自全部分量支援、spokes 及側內間隙，滿足
   ℓ_z+ℓ_w≤5。不能分別替各分量另選互不相容的最短弧。
3. [總覽 §2.2–2.4](c5_no_mixed_span_budget.md#22-飽和二禁色分量不能只佔一條框邊)
   的側跨度下界 ℓ_r≥ω_r，其中 A/B/C/D/E 的 ω 為 2/2/3/4/3。
   這依賴 source 飽和原路徑 K5 引理與 A 側兩 spoke 相容性；正跨度
   又依賴外部 hub、tight degree-list／Gallai 結構與同序支援引理。
   本輪沿用這些紙面／外部定理，不另以有限 placements 證成它們。

**引理 1（不可搬運至少二跨度）。** 設 span_L(C) 為上述既有共同 lift
L 中 S_C 的 hull 長度。若 C∈D_p，則 span_L(C)≥2。

**證明。** 在任意支援 S 上，Π(q,p) 非空恰當 q、p 的等色分割相同：
相同分割使 q_i↦p_i 成為已見色間的良定單射；兩邊未見色數目相同，故
可補成 U 的置換。反向由置換保持等號得到。若 S 為空、包含於一個框點，
或包含於一條框邊的兩端，properness 保證這兩個分割相同；在最後情況，
兩端同時出現時兩列均異色。因此 Π 為空迫 S 不包含於任何長度≤1 的框弧。

這先是關於「存在某條短弧容納支援」的結論。若既有 L 的 hull 長度≤1，
其投影本身就是這樣一條短弧，造成矛盾；所以**每份相容的共同 lift**
都滿足 span_L(C)≥2。不必也不能把 L 換成逐分量最短弧。反向不成立：
在某份 L 中跨度較長，不能推出不可搬運。證畢。

**引理 2（逐 root 界）。** 在以上前提下，

\[
\boxed{|D_{p,z}|\le1,\qquad |D_{p,w}|\le1.}
\]

**證明。** 若同一側 r 有兩份不可搬運原分量，依引理 1，它們在同一
L 中各有至少二的 hull 跨度。框邊內部不交，且都包含於 I_r，故 ℓ_r≥4；
共用端點不會抵消框邊長度，側內間隙只會增加 ℓ_r。另一側 r′ 不論
A–E 何型，沿用 ω_{r′}≥2，故 ℓ_z+ℓ_w≥4+2=6，與至多五矛盾。
這個證明不引用 44 筆查詢、|A_h|≤2 或指定 target 的接受狀態。證畢。

**推論 3（雙不可搬運的側型範圍）。** 若 D_{p,r}≠∅，則

\[
\ell_r\ge\lambda_r:=\max\{\omega_r,m_r+1\}.
\]

**證明。** 選一份不可搬運 C，其跨度至少二；其餘 m_r−1 份原分量各有
正整數跨度至少一。共同 hull 的框邊內部不交給 ℓ_r≥2+(m_r−1)=m_r+1。
再與已有 ℓ_r≥ω_r 合併取最大值。不能無條件取 ω_r+1：不可搬運的分量
可能正是 ω_r 已計入額外跨度的飽和分量，A 側的額外成本也可能重複。

| 側型 | A | B | C | D | E |
| --- | ---: | ---: | ---: | ---: | ---: |
| 原分量數 m_r | 1 | 2 | 2 | 2 | 3 |
| 既有 ω_r | 2 | 2 | 3 | 4 | 3 |
| 含不可搬運分量時的 λ_r | 2 | 3 | 3 | 4 | 4 |

若兩側都有不可搬運分量，必有 λ_z+λ_w≤5。沒有 A 時總和至少六；一側
為 A 時另一側只能 A、B、C。因此無序側型只可能 **AA、AB、AC**，含交換
方向。這只是必要的類型範圍；不證存在實際來源圖，也不證範圍內任何
支援 record 可實現。證畢。

### 3.2 搬運後每側至多一份未知的精確介面

**完整關係搬運引理。** 對 C∉D_p 及任意 π_C∈Π_C(q,p)，

\[
\boxed{T_C(p)=\pi_C T_C(q),\qquad F_C(p)=\pi_C F_C(q).}
\]

右式均不依相容置換的選擇。這個引理本身只需同一原 C、全部 actual
support 及完整有序接點關係；不需要跨度或 minimality。

**證明。** T_C(β) 枚舉原 C 在 boundary β 下的全部 proper 染色之有序
contact tuples，root 尚未指定顏色。將一份 q 染色在 C 的**全部頂點**
施 π_C，分量內每邊仍 proper；每條 C–B 邊的框端屬 S_C，且
π_C(q_i)=p_i，故也 proper。全部 contacts、bridges、旁支與附件均保持，
得到 π_C T_C(q)⊆T_C(p)。對 π_C⁻¹ 做相同論證得反向包含。置換是雙射，
與 tuple 色集的交集可交換，故

\[
F_C(p)=\bigcap_{\tau\in T_C(q)}\operatorname{set}(\pi_C\tau)
      =\pi_C\bigcap_{\tau\in T_C(q)}\operatorname{set}(\tau).
\]

兩個相容置換都給同一 T_C(p)，故兩個像相同；等價地，π_C′⁻¹π_C
逐色固定 q(S_C)，是完整 T_C(q) 的穩定子。F 的像也相同。證畢。

將所有可搬運原分量與原 root-spokes 吸收入已知可用色：

\[
R_r(p)=U\setminus\left(p(N_B(r))\cup
     \bigcup_{\substack{C\sim r\\C\notin D_p}}\pi_C F_C(q)\right).
\]

每份 π_C 可獨立選，但都對齊同一字面 p；沒有重命名 shared frame。
由 no-mixed 的原完整接合式與引理 2，

\[
\boxed{E_r(p)=
\begin{cases}
R_r(p)\setminus F_{C_r}(p),&D_{p,r}=\{C_r\},\\
R_r(p),&D_{p,r}=\varnothing.
\end{cases}}
\]

理由是 root 色 a 可用恰當對每個 incident 原分量存在一個完整 tuple
全部避開 a，即 a∉F_C(p)，且 a 避開原 spokes。T_C(p) 非空沿用接點
[slack 引理](c5_root_degree_excess.md#1-同一來源上的完整消去)。不同原分量
沒有跨邊，故這些 local witnesses 可共同接合；
最後必保留原 zw，要求 (E_z×E_w)∖Δ≠∅。

這裡的「每側一份未知」指完整 target 關係尚未由 source 完整關係的
色置換決定，**不是固定一份 source 染色後只修一份分量**。各 root 色的
local witnesses 可以來自不同 source 染色。所有 F 均是完整 ordered
tuples 的色集交集；不能換成 endpoint marginals。R 是代數吸收，並未
刪去任何原分量；它們提供的外部幾何路徑仍須保留於後續證明。

對指定 p₁、p₂，D_p⊆A_h；A_h 是 actual support 含 h 的**全部**原分量，
兩份可能接同一 root。D_p 則只含完全無相容置換者，每側至多一份。
A_h∖D_p 也應精確搬運；不能因它碰到變動框點就把它當成未知。

接合失敗恰分成以下互斥類別，其餘為 `PASS`：

| 類別 | 精確條件 |
| --- | --- |
| `EMPTY_BOTH` | E_z=E_w=∅ |
| `EMPTY_Z_ONLY` | E_z=∅，E_w≠∅ |
| `EMPTY_W_ONLY` | E_w=∅，E_z≠∅ |
| `SAME_SINGLETON` | E_z=E_w={a}，某 a∈U |

非空兩集合若沒有異色 pair，任取 a∈E_z、b∈E_w 必有 a=b；再固定其中
一個，另一集合每色皆等於它，故兩集合都是同一 singleton。這證明分類
完備，但**沒有排除任何失敗類別**，也尚未給共同 repair 定理。

### 3.3 獨立重播、失敗 joins 與證書入口

[本輪 checker](../scripts/c5_no_mixed_root_transport.py) 只用 Python stdlib，
不 import 既有研究 checker；七類來源 artifact 全部只讀，不重新枚舉
來源圖或幾何。新[逐 record 證書](../artifacts/c5_no_mixed_root_transport/observations.json)
保存 input SHA-256、本 script SHA-256、原記錄／geometry 的 JSON pointer
與內容 hash、具名全部原分量／contacts／spokes／zw、共同 placements、
A_h／D_p、所有相容置換與候選、R_r、逐候選 E_r 及原排除證書入口。

- 全部 32 支援子集 × 2 targets 共 **64** 項，獨立重建全部相容置換，
  比對等色分割，並窮盡單圈 injective lifts，分別核對最短容納弧及
  每份 hull 的跨度下界。另以 **256** 對任意 root 色集合控制互斥分類。
- **2,082** 份 retained records／保存 placements 全核對正跨度、環序、
  框邊內部不交、原 spokes、同一 lift 的側跨度及 λ 下界；每側至多
  一份不可搬運，雙不可搬運只在 AA、AB、AC。
- 從保存的完整 ordered schemas／unary relations 重算 F，核對 source
  穩定子、置換像及反向搬運。共 **111,152** 份帶 record 身份的 relation
  instances、**289,332** 次相容置換控制；重複 schema 隨 record 計數，
  不宣稱枚舉了實際來源圖的完整 T_C。
- 每分量獨立重建「有相容置換則精確像；否則 |F|≤接點數且受 target
  支援逐色穩定子保持」的既有上界域。其 Cartesian product 與原保存
  joins 的具名 F tuple 集合逐項相等，無重複；依原 join index 比對
  **11,096** 個候選的完整接合式、A_h 式及 D_p 式，E_z、E_w 完全相同，
  並核對原 root pairs 及前輪 anchor artifact 的每份失敗清單。

這些候選 F 是包含真實 F 的上界域，可能無完整來源實現；不能因其中
一個候選 `PASS` 就宣稱 target 已證。所有原 final statuses 仍為 accept，
只作沿用狀態核對。結果：

| 不可搬運分量數 | 0 | 1 | 2 | 合計 |
| --- | ---: | ---: | ---: | ---: |
| 本輪實際重播查詢 | 2,936 | 1,184 | 44 | 4,164 |

雙不可搬運為 AA 24、AB 12、AC 8，全部分屬不同 roots；此為紙面引理的
資料一致性檢查，並非引理的全稱性依據。

| 類型 | 全部候選 joins | EMPTY_BOTH | EMPTY_Z_ONLY | EMPTY_W_ONLY | SAME_SINGLETON | PASS |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| AA | 2,892 | 0 | 64 | 64 | 32 | 2,732 |
| AB | 3,148 | 0 | 60 | 68 | 18 | 3,002 |
| AC | 640 | 0 | 0 | 0 | 8 | 632 |
| AE | 336 | 0 | 0 | 0 | 0 | 336 |
| BB | 3,504 | 0 | 60 | 60 | 0 | 3,384 |
| BC | 288 | 0 | 0 | 0 | 0 | 288 |
| BE | 288 | 0 | 0 | 0 | 0 | 288 |
| 合計 | 11,096 | **0** | **184** | **192** | **58** | **10,662** |

四失敗類合計仍是 **434 joins**，涉及 **378 個有上界失敗候選的查詢**；
不是 434 個未決 target，也不是新增排除。計數鍵保持「retained record ×
字面 target × 按具名原分量次序排列的 F tuple」；不對 root 交換、反射、
E 或 target 去重。434 份皆連到已存在的排除證書；本輪驗證入口、join
身份及保存的 eliminated 狀態，不重新執行其幾何排除證明。

代表性入口如下。`failures` 下標、record ID、join index 均為零起算；
p₁、p₂ 為一、二。

| 類別／控制 | 新證書入口 | 具名未知、R 與候選 F | 得到的 E_z；E_w |
| --- | --- | --- | --- |
| EMPTY_BOTH | `representative_failure_indices.EMPTY_BOTH=null` | 本候選域零份，不補造代表 | — |
| EMPTY_Z_ONLY | [failures/10：AA41/p₂/j9](../artifacts/c5_no_mixed_root_transport/observations.json#/failures/10) | D_z={Cz}；R_z={1,3}、R_w={0,3}；F_Cz={1,3} | ∅；{0,3} |
| EMPTY_W_ONLY | [failures/0：AA4/p₁/j8](../artifacts/c5_no_mixed_root_transport/observations.json#/failures/0) | D_w={Cw}；R_z={2,3}、R_w={0,3}；F_Cw={0,3} | {2,3}；∅ |
| SAME_SINGLETON | [failures/12：AA43/p₂/j39](../artifacts/c5_no_mixed_root_transport/observations.json#/failures/12) | D_z={Cz}、D_w={Cw}；R_z={1,3}、R_w={0,1,3}；F_Cz={3}、F_Cw={0,3} | {1}；{1} |
| AA54 全路徑交換 | [failures/27：AA54/p₁/j4](../artifacts/c5_no_mixed_root_transport/observations.json#/failures/27) | D_z={Cz}；R_z={2,3}、R_w={2}；F_Cz={2,3} | ∅；{2} |
| AB22 非守恆端點 | [failures/162：AB22/p₂/j4](../artifacts/c5_no_mixed_root_transport/observations.json#/failures/162) | D_w={Cw}；R_z={3}、R_w={0,3}；F_Cw={0,3} | {3}；∅ |

各入口的 `exclusion_certificate` 給既有 artifact 路徑、JSON pointer 與
內容 SHA；完整保留外部原分量路徑的證據仍在該原證書。AA54 與 AB22
繼續作共同 repair 的必要控制，不能由「每側一份未知」跳過。

本輪實際執行以下驗證；無 `--check` 只生成新的 root-transport artifact：

```bash
python3 scripts/c5_no_mixed_root_transport.py
python3 scripts/c5_no_mixed_root_transport.py --check
PYTHONHASHSEED=17 python3 scripts/c5_no_mixed_root_transport.py --check
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

詳細結果、既有建置檢查與未重跑清單見[本輪紀錄](history/2026-09-29-no-mixed-root-transport.md)。
本輪是依既有結構引理的任意大小**紙面證明＋Python 固定域 audit**，未新增
Lean theorem 或 `native_decide`；`lake build` 不能替代本節形式化證明。
未新增 source 排除、target 接受、來源可實現性、共同 repair、一般共同
出口或 K∞=K≤5 結論。

## 4. 守恆 singleton 的 target pair：表依賴結果

固定缺額二接點原 C，F_C(q)={d}，並令
K={a:∀i∈S_C，q_i=a iff p_i=a}。本節假設 d∈K；不把 AB22/p₂ 的
非守恆 d=2 偷換成守恆色。反設 F_C(p)=D 是二元集。

沿用[原路徑與 palette 引理](c5_adjacent_degree5_no_mixed_t2_path_palettes.md)：
target pair 給奇數長原 bridge 路徑 P；刪 P 的邊所得 W_j 保留全部
旁支與 actual support。局部 residual L_j 尚未扣 root 色，p 下為 D。
q 的端點 residual 含 d，固定色歸納給 L_j(q)∩K=D∩K，因此 d∉D
立即矛盾。這是同一 W_j 的 residual 限制，不是假設 F_C 跨列不變。

d∈D 時，q 下 bridge palettes 為 β₁,d,β₃,d,…,β_ℓ。
每條奇數 bridge 的兩端共用 residual {d,β}。枚舉所有必要 β 及其
實際支援族，再使用同一原外部路徑／固定三框弧引理，逐 β 排除：

| 計數單位：支援 record × target × 具名分量 × target pair D | 數量 |
| --- | ---: |
| d 守恆的 pair 候選總數 | 1,780 |
| d∉D，固定色端點條件排除 | 890 |
| d∈D，原三弧規則排除全部 β | 850 |
| d∈D，只剩一個 β | 40 |
| d∈D，仍剩至少兩個 β | 0 |

只剩 β=b 時，每條奇數邊都用 b，偶數邊用 d；交換整條原 P 的 d,b
palettes，保留所有旁支，可重建 b∈F_C(q)，與 singleton 矛盾。
所以既有七類必要覆蓋加上原路徑引理及此證書，給**表依賴的守恆
singleton 不升 pair 推論**。這不需要先假定整圖 p 拒絕。

其中 776 個 d∈D 候選曾出現在有合法 root 色對的上界 join，142 個曾
出現在失敗 join，兩者有 28 個重疊；它們不是互斥類別。排除有 root
色對的候選是在收緊局部上界，不能記作新增 target 接受或 source 排除。

另加同一 W 的完整支援色置換相容性：若 π 在 W 的全部支援 T 上
對齊 q、p，則 π({d,β})=D。這由 direct attachments 與 rooted branch
palettes 的唯一性得到。若無相容 π，不添加此限制。加入後有 886 個
d∈D 候選零 β、4 個單 β；最後四個正是 AA54/p₁、68/p₂、173/p₂、256/p₁。
較強篩選不是上面 850+40 證明的必要前提。

因此原先「palette 換色必迫 K5」的免分類猜想仍未證。本輪取得的是
**逐支援排除其它 β，再作全路徑交換**。抽象 Gallai 控制仍可有
bridge word (2,3,1)、source d=3、完整禁色僅 {3}；這否定純 palette
代數足以強迫 β 一致，但不是 induced-C5 disk 來源反例。

[Palette checker](../scripts/c5_no_mixed_hypothesis_palettes.py) 與
[逐候選證書](../artifacts/c5_no_mixed_hypothesis_audit/palettes.json)
保存全部 1,780 個候選、原 context、逐 β 支援族、原外部路徑／固定框弧
的一份具名見證，以及全部替代見證的數量／hash、imported scripts SHA。
重播仍計算全部替代見證；不納入未完成的額外探索。

## 5. 可用結論、剩餘問題與重播

可直接重用的是 H/G 搬運引理、單框點 exact reduction，以及 §3.1–3.2
的逐 root 不可搬運界與 D_p 精確介面；守恆不升 pair 目前仍靠既有七類
的必要覆蓋與逐支援證書。下一個窄問題是：精確搬運其餘全部原分量後，
對 D_p 每側至多一份未知關係，是否能用不查表的共同相容規則統一處理
守恆與非守恆禁色。AB22 非守恆端點及 AA54 全路徑交換
仍是必要控制；外部原路徑不因未知關係減少而可刪去。

```bash
python3 scripts/c5_no_mixed_hypothesis_transport.py --check
python3 scripts/c5_no_mixed_hypothesis_anchor.py --check
python3 scripts/c5_no_mixed_hypothesis_palettes.py --check
PYTHONHASHSEED=17 python3 scripts/c5_no_mixed_hypothesis_transport.py --check
PYTHONHASHSEED=17 python3 scripts/c5_no_mixed_hypothesis_anchor.py --check
PYTHONHASHSEED=17 python3 scripts/c5_no_mixed_hypothesis_palettes.py --check
```

本段命令為前輪三假設 audit 的重播入口，本輪實跑清單見 §3.3。
無 `--check` 只生成相應 audit JSON；不覆寫既有十五類資料。
證據層：§2 初等紙面證明；§3 依既有拓撲引理的任意大小紙面化約；
§4 沿用外部 degree-list／Gallai 定理及原路徑證明，再以 Python 核對
固定支援域。未新增 Lean theorem；lake build 不形式化這些論證。
未證必要資料可實現、一般共同出口或 K∞=K≤5。
