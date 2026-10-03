# ε=2 唯一 mixed：單 spoke 省略的核心與原附件限制

**提交整理（2026-10-03）**：本頁、checker 與研究紀錄的本次提交範圍、
實際重播及整理發現見 [九輪進展紀錄](history/2026-10-03-excess-two-dual-root-progress-commit.md)。
下文的未提交字句保留當輪語境；即時提交狀態以 Git 為準。

**後續（2026-10-03）**：[原 leaf 色纖維與五-spoke 排除](c5_excess_two_mixed_core_leaf_fibers.md)
已用原四點 joint relation 及同一 unary 雙列 palette／K₅ 排除本頁
剩下的四組941五-spoke附件與 root 交換。因此兩候選總 spokes 都≤4；
單 spoke 省略仍未全排，ε≥3 未證。下文保留本輪化約及當時停止點。

2026-10-03，接手基準 `722bfa6`，保留前序未提交成果。接續
[原 mixed 省略全收](c5_excess_two_mixed_omission.md)的停止點；目前入口
由 [Kempe 導覽](c5_kempe_guide.md)維護，實際驗證與跨對話摘要見
[研究紀錄](history/2026-10-03-excess-two-mixed-core-single-spoke.md)。

**本輪是任意大小的必要化約，尚未排除原單 spoke 省略子型。**
在固定 933／941 的相鄰、唯一 mixed 來源前提下，新增：

- 任一原 spoke e 的省略圖 M=G−e，若拒絕 q，M 自己就是唯一
  degree-5 的 minimal q-core；其拒絕 singleton 位置形成獨立集。
- 固定標號下，933／941 每個 root 的三-spoke 附件分別只餘兩組／六組。
- 兩側不能同時各有三条 spokes；進一步 **933 有 t_z+t_w≤4，
  941 有 t_z+t_w≤5**。941 的五-spoke 型只餘四組具名附件及 root 交換，
  且必為原 mixed incidence-(1,1) 加二-spoke 側的一份單接點 unary。

證據為紙面合成、固定位置代數／明示 subdivision 證書與原圖完整接合
控制。**ε≥3 仍未證；沒有新增 Lean theorem。** 剩餘具名附件是必要
放寬，不是來源實現、完整 relation 模型或新的圖 catalogue。

## 1. 同一原 G 與省略圖自己的 minimality

G 有限簡單，B=(b₀,…,b₄) 是指定有序 induced-C₅ disk 外框。
完整 Σ 是 933、941 或其整圖 D₅ 像；刪任一非框邊都嚴格擴大 Σ。
有效內部 H 非空連通，恰兩個完整 degree-5 roots z,w，其餘有效
內點完整 degree 四。原 zw 存在，H−{z,w} 恰一份原 mixed C，
其餘均為原 unary。所有原分量、實際附件、有序 contacts、ownership、
原嵌入環序及共同字面四色框保持。

沿用已證的 Σ(G−z)=Σ(G−w)=Σ(G−zw)=Ω 及全部 (4,4) q-core 排除。
取原 e=wb_s，M=G−e 的 root degrees 為 (5,4)。反設 M 拒絕 q，
取其 minimal q-core K。前述全收迫 K 含 z,w,zw。其他原 degree-4
點飽和，使原分量只能全取或全不取；w 在 M 已為四，故其全部
原 M 邊都保留。z 最多再失去一條 incidence。

若 z 降四，K 便是原 G 的 (4,4) q-core，已不可能。因此 z 仍五；
原省略身份表迫 K=M。這對 M 的**每個**拒絕列成立，並非假設
G 自己 q-minimal。故 M 的每條非框邊都同時釋放它的每個拒絕列。

在 M 自己使用 [只需 T4 的唯一 degree-5 相鄰列分離](c5_excess_one_subcovers.md#2-只用-t4-的-minimal-degree-5-相鄰列分離)。
令 Q_e 是 M 拒絕的 singleton 位置，Q 是 G 的拒絕位置，則

\[
Q_e\subseteq Q,\qquad Q_e\text{ 在原 }C_5\text{ 上無相鄰位置}.\tag{1}
\]

固定 masks 的 Q 分別為 933 的 {0,1,2,3}、941 的 {0,1,3}。
包含 Q_e=∅ 的全收情形，式 (1) 給 **8／6 份必要 child masks**；
非空情形為 7／5 份。單點任取 Q；兩點只可能為
933 的 {0,2}、{0,3}、{1,3}，941 的 {0,3}、{1,3}。
這不是每份 mask 可實現的宣稱。原 Σ edge-minimal 給嚴格擴大，
但不能從式 (1) 推出 M 必全收。

## 2. 同色原 spokes 迫省略圖仍拒絕

固定 root r 的原 boundary 鄰居 S_r。唯一 mixed 與原 zw 各占至少
一條 incidence，故 t_r=|S_r|≤3。對 e=rb_s，定義

\[
D_e=\{i\in Q:\exists b_t\in S_r\setminus\{b_s\},
\ q_i(b_t)=q_i(b_s)\}.
\]

在這些**同一列**上，保留的 spoke rb_t 已排除與 e 完全相同的
root 色；因此 G−e 與 G 的染色集合在該列相同，D_e⊆Q_e。
若 D_e 含相鄰兩位置，便違反式 (1)。不需把不同列的染色拼在一起。

| 原 t_r | 933 的必要附件數 | 941 的必要附件數 |
| --- | ---: | ---: |
| 0 | 1 | 1 |
| 1 | 5 | 5 |
| 2 | 7 | 9 |
| 3 | 2 | 6 |

933 的三-spoke 集只餘 **012、123**；941 只餘
**012、014、023、034、123、134**。數字表示具名框點集合，不作
獨立 orbit 正規化。每份被排附件均保存具名省略 spoke、兩個相鄰
拒絕列及其保留同色 spoke；十個 D₅ 映射共同搬動全部位置與 masks。

## 3. 兩側各三 spokes 的排除

只保留 B、原 zw、兩側全部原 spokes，再於外側加 apex α 連全 B。
這是原 disk 來源的必要子圖；不是把 C 或 unary 換成染色星點。
§2 的兩側附件組合共 225／441 份有序具名支援對。
其中 10／48 份有明示 K₅／K₃,₃ subdivision，逐原邊、簡單路徑、
branch 頂點、互斥內點及全部鄰接核對。其餘骨架附可核對的 apex
rotation；骨架平面不代表原 G 可實現。

若兩側各三 spokes，唯一 mixed 必為 incidence-(1,1)，且沒有
任何 unary。故保留骨架**正是原 G−C**，不是獨立挑選的替代圖。
933 的四份這種支援對全部非 disk。941 的 36 份中 22 份非 disk；
其餘十四份的全部十列原 root-pair relations 直接重算：八份拒絕
某個原 T4 列，另六份接受 T4 但只缺 singleton 0、1 或 3。
後六份與既有 Σ(G−C)=Ω 矛盾。因此兩側不能各有三 spokes。

## 4. 五 spokes 的原形與進一步排除

設三-spoke 側為 a，二-spoke 側為 b。原 incidence 預算只有兩型：

| 原 mixed 在 (a,b) 的 incidence | 其他原分量 |
| --- | --- |
| (1,2) | 無 unary |
| (1,1) | 恰一份單接點 unary U，只接 b |

在 §2 所保留的每份三-spoke 集，都有某個原 spoke e 在某個原
拒絕列 q 與另一條保留 spoke 同色。因此 M=G−e 仍拒絕 q，並由
§1 是以 b 為唯一 degree-5 的 minimal core；a 在 M 的 degree 四。

第一型的 M−b 恰為**整份原 C 加原 a**，連通且有三個不同
b-contacts：a 及原 C 的兩個接點。這違反既有
[two-spoke 三接點來源排除](c5_two_spoke_three_contacts.md)。任意原
C 大小、原 bridges、旁支與附件皆保留，不能把它拆成三份 unary。

第二型的 M−b 恰為 K=C∪{a} 與原 U，contacts 分拆 (2,1)。
K 的原有序接點為 (a,y)，其中 y 是原 C 的 b-contact；a 是 K
的 leaf，deg_K(a)=1，保留兩條原 boundary spokes。綜合既有
[two-spoke 必要位置](c5_degree5_two_spoke_sectors.md)、
[相鄰排除](c5_two_spoke_adjacent_21.md)、
[中間相鄰排除](c5_two_spoke_middle_21.md)與
[反射](c5_two_spoke_reflection.md)，minimal q_i 的 two-spoke (2,1)
root 必接 singleton b_i。套到全部被同色 e 迫出的 q，24／88 份
五-spoke 骨架先排除 16／64 份。

若 b 的兩條 spokes 相鄰，剩餘式子還可排除。令 b 在 q 的
available colors 為 {h,D}，D=3。M minimal 迫 K、U 各禁其中一色。
a 保留的兩條 spokes 見到 q 的兩個重複色，包含 h；固定 b=h
沒有減少 a 的 list，該 list 大小二而 deg_K(a)=1。連通 slack-list
貪婪引理使 K 可染，所以 F_K(q)≠{h}，必為 {D}，F_U(q)={h}。

在 q 同步搬到 q₄=01012 後，
[split-support 完整附件定理](c5_two_spoke_split_support.md#1-source-contacts-and-proof-boundary)
要求：b-spokes 為 34 時 N_B(K)=014；為 04 時 N_B(K)=234。
兩條同色原 spokes 各自省略都提供 M。至少一份 M 仍保留 a 到
上述 D 支援之外的**原實際框邊**，直接矛盾。Checker 對每份這種
衝突保存同一 q、e、a 的保留附件、h、必要 D 支援與違反的框邊。
這再排除 8／16 份，沒有獨立重選 K 或 U。

故 933 不可能有五 spokes；941 只餘下列四組及 root 交換：

| 三-spoke 側 a | 二-spoke 側 b | 同色省略迫出的 q singleton |
| --- | --- | ---: |
| 012 | 03 | 3 |
| 014 | 13 | 3 |
| 034 | 13 | 1 |
| 123 | 03 | 0 |

它們都必有原 mixed incidence-(1,1) 與 b 側原單接點 U；二-spoke
側的框鄰點非相鄰。這八份有序附件尚未證可實現或排除。

## 5. 接回原 e 的精確介面與剩餘障礙

一般 M=G−wb_s 保存全部原 contacts 的 joint relation
\(\mathcal T_M(\beta)\)，每份 tuple 附 M 全圖 witness。
接回只有一條原邊，精確式子是

\[
\mathcal T_G(\beta)=\{t\in\mathcal T_M(\beta):t_w\ne\beta_s\}.
\tag{2}
\]

因此 M 接受、G 拒絕的列恰有非空 M relation，卻**所有** tuples
都滿足 t_w=β_s。M 的指定列分離只提供非空性，沒有提供不同
於 β_s 的原 w 色。不能把兩個 root marginals 相乘或直接搬出口。

對 §4 的餘下五-spoke 型，令 U 的 contact 為 u。應保留原
四點聯合座標 **(b,a,y,u)**，K 的完整有序 relation (a,y)，及
原 C 的全部實際附件、a–x 邊、原 b–y 邊和 b–u 邊。先在同一
β、同一 b 色接合 K、U，再過濾 a 色不等於原省略 spoke 的框色。
已完成的非相鄰 two-spoke 分離沒有保存這個被標記的 leaf a
在指定列的完整色纖維；這是下一個具體缺口。

## 6. 固定證書、重播與停止點

[Checker](../scripts/c5_excess_two_mixed_core_single_spoke.py)／
[artifact](../artifacts/c5_excess_two_mixed_core_single_spoke/observations.json)
保存完整十列位置／附件約束、8／6 child masks、20 份共同 D₅
搬運核對、666 份具名 skeleton、58 subdivisions、十四份雙三-spoke
原 G−C 完整 relations，以及全部 112 份五-spoke 原 incidence
化約與具名衝突。紙面依賴 hashes 明列；checker 不重證這些任意大小
topology／degree-list 定理。

另沿用既有 `943/k3-t382/submask 2045` 原八點圖，標記其中一個
degree-4 鄰點後接回六條具名 spokes。**60 次**全部 joint tuple
接合與獨立全圖回溯相同；**960 次** pinned 原 root-pair 查詢包含
空纖維，完整 witnesses、原 singleton mixed、實際附件與 ownership
保存。這些圖不聲稱 disk、Σ edge-minimal 或 933／941 實現。
原 943 圖對其兩個拒絕列均非 q-minimal，明列仍拒絕的刪邊身份；
控制只驗證式 (2)，沒有拿它反駁唯一 degree-5 定理。

```bash
uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_single_spoke.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_single_spoke.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

**停止點：完成單 spoke 省略的 minimality／同色附件化約及五-spoke
來源限制；尚未證 Σ(G−e)=Ω。** 下一窄入口固定 §4 的941 四組
附件與 root 交換，研究同源非相鄰 (2,1) core 的原四點 relation
及 leaf a 的指定列色纖維。較少 spokes、原 unary 省略、原 G
自己 (5,5) q-core，以及多 mixed、no-mixed、非相鄰 roots 的
其他來源分支仍保留。共同下界仍 ε≥2，ε≥3、一般出口、來源
實現及 K∞=K≤5 都未證；`lake build` 不形式化本輪紙面化約。
