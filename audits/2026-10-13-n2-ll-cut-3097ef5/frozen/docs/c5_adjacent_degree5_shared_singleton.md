---
docgraph:
  id: c5.adjacent-degree5-shared-singleton
  family:
    - c5
    - c5.degree5
  derives_from:
    - c5.adjacent-degree5-interfaces
  requires:
    - c5.no-spoke-exterior
    - c5.single-spoke-three-one
---
# 相鄰雙 degree-5：唯一共鄰單點與單 root 分量

後續（2026-09-28）：[01／23 長弧分離](c5_adjacent_degree5_singleton_long_arc.md)
以原三角形次序與原 x 路徑 K5 證這兩位置接受指定雙列，已接入條件式出口；
[12 長弧](c5_adjacent_degree5_singleton_middle_arc.md) 亦已完成雙列分離，
[34／40 來源排除](c5_adjacent_degree5_singleton_end_arc.md) 再完成全部 x 支援
並接回出口。下文 240 筆抽象禁色資料及各輪歷史停止點不改寫。

後續（2026-09-28）：[同側限制與 target 重色排除](c5_adjacent_degree5_singleton_sectors.md)
利用原 zw 使 H−x 連通；在額外 disk＋T4 前提下排除 x 接 {b1,b4}、
{b2,b4} 的來源，完成下述指定重色障礙。全部非相鄰支援已排除或證只缺 q，
剩五個相鄰長弧位置未分離。下文當輪停止點及 240 筆必要關係保留原範圍。

2026-09-28。接續 [完整有序色對介面](c5_adjacent_degree5_interfaces.md)。
本輪完成一個任意大小的必要化約：**若唯一同時接兩 root 的原分量是
共鄰 singleton，則平面來源的每個 root 至多一條 boundary spoke，
其餘單 root 分量的接點分拆只可能為 (2) 或 (2,1)。**
另給此子類在任意 boundary row 的精確拒絕判準。

代數部分是初等紙面證明；排除 (3) 沿用外部 degree-list 定理及原圖 K5
抽取，另有 Python 關係／具名 minor 控制。未新增 Lean theorem。
保留的 240 筆是必要禁色資料，不是 disk 實現、完整來源 cover 或指定 p 分離。
研究優先序見 [HANDOFF](HANDOFF.md)。

## 1. 同一來源及精確消去單 root 分量

沿用前報告：有限簡單圖、induced boundary C5、q=01012、U={0,1,2,3}，
H 是連通有效內部，相鄰有序 roots (z,w) 的完整 degree=5，其他內點
完整 degree=4。原 H−{z,w} 分量、所有實際附件、接點身份和嵌入次序均固定。
minimal q-core 指拒絕 q 且每條非外圈邊刪除後皆接受 q。

將原分量分為只接 z 的族 C_z、只接 w 的族 C_w、同時接兩者的族 C_m。
對單 root 分量 C，以完整有序接點關係 T_C(β) 定義

\[
 F_C^r(\beta)=\bigcap_{t\in\mathcal T_C(\beta)}\{t_p:p\in P_C^r\},
 \qquad r=z\text{ 或 }w.
\]

T_C 非空：去掉 root 避色約束後，每點 list 至少等於 deg_C，任一接點
嚴格多一色，故用連通 slack 引理。於是 |F_C^r(β)|≤|P_C^r|。
只接 z 的雙 root 拒絕關係恰是 F_C^z×U，只接 w 則是 U×F_C^w。
這是完整 tuple 的精確投影，沒有把同一 C 的接點拆開。

定義

\[
 E_z(\beta)=A_z(\beta)\setminus\bigcup_{C\in C_z}F_C^z(\beta),\qquad
 E_w(\beta)=A_w(\beta)\setminus\bigcup_{C\in C_w}F_C^w(\beta).
\]

全圖的有序 root 色對恰為

\[
 Z_G(\beta)=\bigl((E_z(\beta)\times E_w(\beta))
                 \cap\bigcap_{C\in C_m}R_C(\beta)\bigr)\setminus\Delta. \tag{1}
\]

**Mixed 分量的逐欄／逐行容量。** 若 k_z=|P_C^z|>0、k_w=|P_C^w|>0，
則固定任意 b，至多 k_z 個 a 使 (a,b)∉R_C(β)；固定任意 a，至多 k_w
個 b 被拒絕。先只固定 w=b，暫不施加 z 約束，則每個 z 接點至少有
一色 slack，C 可著色。固定這一份完整 coloring，每個被拒絕 a 都必在
其 z 接點上出現，所以不超過 k_z。反向同理；共鄰點仍為同一頂點。

令 m_r 是 mixed 分量佔用 root r 的 incidence 總數。root 的剩餘接點總數
為 4−t_r，|A_r(β)|≥4−t_r，故上述 unary 容量給

\[
 |E_r(\beta)|\ge m_r. \tag{2}
\]

這對任意 β 成立，即使 β 下 root spokes 有重色；不是只在 q 的計數。

## 2. 唯一 mixed 分量為原共鄰單點

以下額外假設 C_m 恰含 C_x={x}，P_x^z=P_x^w={x}。因此 x 的其餘
兩條邊是到不同 boundary 頂點 b_i、b_j；沒有省略其他 mixed 分量。
其他原分量可以任意大，但各自只能接一個 root。

minimality 迫使 q_i≠q_j：否則 x 在任意色對下都有 slack，R_x(q)=U²，
刪 x 邊不能改變 q 的拒絕。令

\[
 T=U\setminus\{q_i,q_j\}=\{d,3\},\qquad
 F_x(q)=(T\times T)\setminus\Delta.
\]

由 (2)，E_z、E_w 在每列都非空。以下未標 β 的集合均在 q 下。
刪 zw 的對角見證、C_x 的私有非對角色對與 q 拒絕共同給

\[
 \varnothing\ne E_z,E_w\subseteq T,\qquad E_z=T\text{ 或 }E_w=T. \tag{3}
\]

證明：C_x 的私有對是 E_z×E_w 中的一個非對角，q 拒絕迫使它恰為
T 的一個次序。若任一 E 含 T 外顏色，與另一側已在 T 內的顏色接合
便可延拓，矛盾。刪 zw 可著色排除兩個不同 singleton；C_x 有私有對
排除兩個相同 singleton。剩下恰是 (3) 的五種有序組合。

**Root-spoke 與 unary 私有色條件。** 對每一側 r：

\[
 T\subseteq A_r,\qquad F_C^r\subseteq A_r\quad(C\in C_r), \tag{4}
\]
\[
 J_C=F_C^r\setminus\bigcup_{D\in C_r,\,D\ne C}F_D^r,
 \qquad J_C\setminus T\ne\varnothing. \tag{5}
\]

若 root-spoke 的 q 色 c∈T，刪該邊只釋放 c；另一 root 的 E 包含於 T，
任何不同色對仍被 x 擋住，因此不可能 minimal。這給 (4) 第一式。
對任何 c∉A_r，對應 spoke 的刪後見證必用 r=c，故每個 unary C 都接受
c，給第二式。這裡用 q 下 root spokes 互異；其初等 minimality 證明見前報告。

刪 C 的邊只解除該原分量。若 r 的新色仍在 T，便仍被 zw 或 x 擋住；
若在 T 外，則與另一 root 的任意 E 色皆可接合。因此 C 的私有色對精確為
(J_C\T)×E_w（z 側）或 E_z×(J_C\T)（w 側），證 (5)。

反過來，在本節 degree／接線及 q-spokes 互異前提下，(3)–(5) 給完整
minimality：原圖拒絕 q；對角交集與非對角乘積分別見證刪 zw、刪 C_x 邊；
(5) 見證刪每個 unary C 的邊；root-spoke 釋放 T 外且不被 unary 擋住的
顏色，亦可接合。這是該實際來源的充要判準，不是抽象資料的實現定理。

## 3. 每側的三種必要正常形

單 root 分量的 incidence 總數為 n_r=3−t_r。不同分量的 J_C\T 非空
且互不相交，故分量數 r_r≤|A_r\T|=2−t_r；(4) 先給 t_r≤2，
而 t_r=2 時 n_r=1、r_r≤0 矛盾。所以 **t_z,t_w≤1**。
又 n_r>r_r，每側必有多接點分量，不能全部只用單接點。

把接點數大的分量列在前，所有可能恰為以下必要形式。
表中的 E 可為 T 或 T 的任一 singleton，兩側另須滿足 (3)。

| t_r | 接點分拆 | 完整 unary 禁色投影的必要形式 |
| --- | --- | --- |
| 1 | (2) | A_r\T={h}；F₂={h}∪(T\E_r) |
| 0 | (3) | F₃=(U\T)∪(T\E_r)，故至少禁兩色 |
| 0 | (2,1) | U\T={h,k}；F₁={h}，F₂={k}∪(T\E_r)，或交換 h、k |

例如 (2,1) 的兩個分量各須有一個不同的 T 外私有色；單接點容量為一，
故它不能再禁 T 色，且兩個 T 外色不能重疊。其餘兩行由唯一分量直接得到。
這保留分量身份與兩側次序，沒有將兩份 unary coloring 放進同一個 C。

## 4. 平面來源排除 (3)：使用原 x 提供外部路徑

現在加上來源 planarity；不需 T4、p 拒絕或內點數上界。
對任一 unary C，外部鄰居只有 B 與其 root r。原集合 B∪{r,x} 連通，
因原邊 rx、xb_i 已提供 r–B 路徑，且它們完全避開 C。

C 有被拒絕的 root 色，residual lists 是不可著色的 degree assignment。
[Dvořák Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
給 Gallai 結構與 block palettes。原
[連通外框 K4 引理](c5_degree5_tree_components.md#1-連通外框排除-degree-4-分量的-k4)
可把 hub 擴為 B∪{r,x} 及四條原 tethers，故 C 沒有 K4 block。
hub 中的 x 是同一個原共鄰點，不是新增接線；另一 root 可以留在 branch sets 外。

若 C 是 (3)，§3 給至少兩個禁色。沿用
[三接點 active triangle 證明](c5_single_spoke_three_one.md#2-三個葉點迫使唯一-triangle-加三臂)：
兩份拒絕 palettes 的差異在 block incidence forest 上只有三個接點葉，
故恰有一個 triangle 及三條同 parity 的 bridge arms；每個 triangle 頂點
的第四方向給一條實際 boundary tether。證明只需 C 的完整 degree=4、
K4-free、兩個禁色；不要求唯一 degree-5 或恰有一條 root spoke。

令 V₀,V₁,V₂ 為三條完整 arms（含 triangle 端點及原接點），並取

\[
 Z=\{r\},\qquad
 O=B\cup\{x\}\cup\bigcup_{k=0}^2(V(T_k)\setminus\{v_k\}).
\]

五組 Z,V₀,V₁,V₂,O 非空、連通且互不相交。三條 triangle 邊給 V_k
兩兩鄰接，原 contacts 給 Z–V_k，原 tethers 給 V_k–O，**原 rx 給 Z–O**。
十條鄰接全在原圖，故是 K5 minor，矛盾。
其應用界線與 [no-spoke 外部路徑版本](c5_no_spoke_exterior.md#5-多分量的三四接點分量也排除)
相同，唯此處的原路徑明確是 r–x–b_i。

因此平面來源每側只剩 **t=1 的 (2)** 或 **t=0 的 (2,1)**；每側恰有
一個二接點分量，可能另有一個單接點分量。由 (3)，至少一側的二接點
分量只禁一個 T 外色；另一側至多再禁 T 中的一色。

## 5. 同一來源的任意列拒絕公式

對任意 proper β，仍由原分量完整關係算 E_z(β)、E_w(β)，兩者皆非空。
令 T_β=U\{β_i,β_j}；若 β_i=β_j，x 有三色 list，R_x(β)=U²；
若不同，F_x(β)=(T_β×T_β)\Δ。式 (1) 立即給

\[
 \beta\notin\Sigma(G)\iff
 \left[E_z(\beta)=E_w(\beta)=\{c\}\text{ for some }c\right]
 \quad\lor\quad
 \left[\beta_i\ne\beta_j,\ E_z(\beta),E_w(\beta)\subseteq T_\beta\right]. \tag{6}
\]

若乘積有非對角且全部被 x 擋住，它包含 T_β 的一次序，任一 T_β 外色
會立即提供接受對，所以兩 E 都包含於 T_β；若無非對角，正是相同 singleton。
這也證明任何一側 |E_r(β)|≥3 都保證接受。

特別是 p₁=01021 在 x 支援 {b1,b4} 時、p₂=01212 在 x 支援 {b2,b4}
時會讓 x 的兩條 boundary 邊同色；此時**仍須排除兩側同色 singleton**，
不能僅從 x 全開宣稱延拓。其他列也不能套用 q 的私有色條件。
若在某原分量的全部實際支援上 β=σq，才可用同一 σ 搬運它的完整 tuples
及禁色；不能各分量任選 σ 後忘掉回到同一具名色框。

## 6. 有限證書、重播與停止點

[checker](../scripts/c5_adjacent_degree5_shared_singleton.py) 與
[certificate](../artifacts/c5_adjacent_degree5_shared_singleton/observations.json)
分別保存關係代數、實際圖控制與 minor skeletons，不混用證據層。

- 每側 209 個容量允許的候選，未預先限制 F⊆A；三種 T 共 131,043 個
  組合，獨立逐類刪邊判準與 (3)–(5) 完全相符，留下 375 筆。
  排除含 (3) 側的 135 筆後剩 240 筆；四種有序分拆組合各 60 筆。
  這些只記 q 色與分量角色，**沒有枚舉實際 boundary 支援／環序或證可實現性**。
- 沿用九個固定分量的全部 240 proper rows，核對各 7,680 個行／列容量
  及 240 個 unary 關係；另獨立核對 (6) 的 2,250 個非空 E／T_β 組合。
- 一張完整 degree 序列 (5,5,4,4,4,4,4,4,4) 的真正 minimal q-core，
  保存具名原圖、十個 canonical rows 的完整 tuples、全部 240 列的接合核對，
  及 25 份逐邊刪後 coloring。它有明列 K5 minor，**不是 disk 正控制**。
- 100 份使用原 r–x–b_i 路徑的 K5 skeleton，含零臂／長臂、直接／細分
  tethers 及全部十種具名 x-boundary pair。每份保存 branch sets 與十條
  實際鄰接；刪 rx 後原指定 witness 失效。這不宣稱刪 rx 後整圖平面。

```bash
python3 scripts/c5_adjacent_degree5_shared_singleton.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_single_spoke_three_one.py --check
python3 scripts/c5_no_spoke_exterior.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證與沿用範圍見 [當輪紀錄](history/2026-09-28-adjacent-shared-singleton.md)。
`lake build` 不表示此紙面化約已 Lean 化。

**下一窄入口：** 在 (2)／(2,1) 兩側正常形下，保留 x 的兩個具名
boundary 鄰點與每個 unary C 的實際支援，利用同圖跨列限制處理 (6)；
先排除上述 target 重色時兩側同色 singleton 的可能。
本輪未證此子類全部 p₁／p₂ 分離，未分類較大 mixed 分量或多 mixed 分量，
也未完成一般相鄰雙 root、非相鄰雙 root、degree≥6、一般出口或 K∞=K≤5。
