# ε=2 四-spoke (3,1)：原 mixed-(1,2) 的三接點身份與整型排除

**後續（2026-10-03）**：[mixed-(1,3) 原四接點 leaf-slack](c5_excess_two_mixed_core_four_spoke_quaternary.md)
已排除無 unary 的最後 incidence 身份，含 root 交換；結合 singles／
binary hubs／本頁，完成相鄰唯一 mixed 的四-spoke (3,1) 全部四份原
incidence 分拆。下文保留當輪停止點與驗證數字；目前下一窄題見
[Kempe 導覽](c5_kempe_guide.md)。ε≥3 仍未證。

2026-10-03，接手基準 `b63a096`，保留前序未提交成果。接續
[binary 同列端點 hub 排除](c5_excess_two_mixed_core_four_spoke_hubs.md)；
目前研究入口由 [Kempe 導覽](c5_kempe_guide.md)維護，實際驗證及貼用摘要見
[本輪紀錄](history/2026-10-03-excess-two-four-spoke-ternary.md)。

**在下列固定來源前提下，四-spoke (3,1)、mixed incidence-(1,2)
加一原單接點 unary 的全部來源均不存在，含 root 交換。**
原 a=6、b=5、a-spokes=012、b-spoke=2、q=01021 入口先完成；
省略 a0 或 a2 後，整份原 C 加 a 是三接點分量，並非 binary。
完整 K 禁色為 {2,3}，原 unary 禁色為 {1}；既有 single-spoke
(3,1) active-triangle 引理在同一原圖給 K₅ minor。

紙面身份傳遞及既有任意大小定理負責整型結論；Python 核對具名必要域、
完整同框 relations／纖維及原 minor 控制。**共同 ε≥2 不變，ε≥3
仍未證，未新增 Lean theorem。**

## 1. 同一原圖與原分量

G 有限簡單，B=(b₀,…,b₄) 是指定有序 induced-C₅ disk 外框。
完整 Σ 是 933、941 或其整圖 D₅ 像；刪每條非框邊都嚴格擴大 Σ。
有效內部 H 非空連通，恰兩個完整 degree-5 roots a,b，原 ab 存在，
其餘有效內點完整 degree 四。H−{a,b} 恰有一份 mixed C 與一份 unary U。

- a 的原 spokes 為三點集 S_a，另接 b 及 C 的原接點 x。
- b 的原 spoke 為 b_s，另接 a、C 的兩個不同原接點 y₀,y₁，及 U 的接點 u。
- x 可以等於 y₀ 或 y₁；y₀≠y₁。u 在另一原分量，與 C 的點互異。

保留任意大小的 C、U、全部原內邊與 bridges、實際 boundary 附件／supports、
ownership、有序 contacts、嵌入環序及同一字面四色框。不把原 C 換成
三份單接點因子，也不將 (y₀,y₁) 的 marginals 相乘。

前序 [原省略身份表](c5_excess_two_mixed_core_spokes.md#2-全部-proper-core-的具名省略表)
及 [單 spoke 核心化約](c5_excess_two_mixed_core_single_spoke.md#1-同一原-g-與省略圖自己的-minimality)
已證：原刪 a、刪 b、刪 ab 圖全收；相鄰唯一 mixed 的全部原 (4,4)
rejected-row cores 均不存在。這些前序結論是本頁身份傳遞的依賴。

## 2. 同色原 spoke 省略與 M 自己的 minimality

對 S_a 中的原 spoke e=ab_j，若 G 拒絕的同一列 q 有 k∈S_a−{j}
滿足 q_j=q_k，保留的 ab_k 已施加 e 的完整色限制。因此

\[
\operatorname{Col}_q(G-e)=\operatorname{Col}_q(G)=\varnothing. \tag{1}
\]

這是同一字面列、同一原圖的染色集合等式。原 Σ edge-minimality 只迫
其他某列被釋放，與式 (1) 並不矛盾。

令 M=G−e，取包含 B 的 minimal q-core L。原刪 roots／ab 全收迫
L 含 a,b,ab。原 degree-4 分量飽和，保留時所有原內邊、附件與
incidences 都保留。a 在 M 已 degree 四，不能再失去任何原邊；
b 至多再失去一條 incidence。若 b 降四，L 是已排除的原 (4,4)
q-core。因此 b 仍五，全部原因子都保留，**L=M**。

故 M 自己是 q-edge-minimal obstruction，唯一完整 degree-5 點是 b。
這不假設原 G 對 q minimal，也不將 G 的 Σ-minimality直接換成 q-minimality。
有限身份核對另列出所有保 degree≥4 的後續省略：無省略、只省略
原 b-spoke、只省略原 U；後兩份都是已排除的原 (4,4) 身份。
mixed-(1,2) 的原 C 不能省略。

M−b 恰有兩份原分量

\[
K=C\cup\{a\},\quad U;\qquad
P_K=(a,y_0,y_1),\quad P_U=(u). \tag{2}
\]

K 經原 ax 連通，a 是 K 的 leaf，deg_K(a)=1，保留兩條原 boundary
spokes；K、U 每點在 M 的完整 degree 四。a,y₀,y₁,u 四點互異，
即使 x=y₀／y₁ 也不合併這些 contacts。原 b 的唯一 spoke、四條
contact edges、C／U 的全部附件都仍是原邊。

## 3. 完整原 joint 與指定入口

令 R_C(q) 是原有序三點 (x,y₀,y₁) 的完整 relation，R_U(q) 是
原 u 的完整 relation，均附同一分量 coloring 的存在量詞。
記 A_a(q)=\{0,1,2,3\}−q(S_a−{j})，A_b(q)=\{0,1,2,3\}−\{q_s\}。
M 的完整六座標 joint 是

\[
J_M(q)=\{(d,h,c,t_0,t_1,v):
(c,t_0,t_1)\in R_C(q),\ v\in R_U(q),\
h\in A_a(q),\ h\ne c,\
d\in A_b(q),\ d\notin\{h,t_0,t_1,v\}\}. \tag{3}
\]

原 G 只在同一 joint 上加回 h≠q_j。K 的完整三接點 relation 為

\[
R_K(q)=\{(h,t_0,t_1):\exists c,
(c,t_0,t_1)\in R_C(q),\ h\in A_a(q),\ h\ne c\}. \tag{4}
\]

每個存在量詞都由同一原 C 的整份 coloring 承擔；固定 boundary 及
root 顏色後，C／U 的完整 witnesses 才拼接。式 (4) 是精確 leaf
接回的投影，不是對三個接點獨立選色。

沿用 [不可刪減覆蓋](c5_single_spoke_cores.md#2-四種不可刪減覆蓋任意大小結論)，
M 的 (3,1) 給某 c₀∈A_b，使 F_U(q)={c₀}、F_K(q)=A_b−{c₀}。
對 d∈F_K，原 K 的拒絕 degree lists 必處處 tight。如果
d∈q(S_a−{j})，a 的 list 大小仍二、deg_K(a)=1，連通 slack-list
貪婪引理反而可染。因此

\[
F_K(q)\subseteq A_a(q),\qquad
|F_K(q)|=|A_a(q)|=2. \tag{5}
\]

指定原 S_a=012、s=2、q=01021、j=0 或 2 時，
A_a={2,3}、A_b={1,2,3}，故完整 relation 的禁色必為
**F_K={2,3}、F_U={1}**。若某具名 query 的 A_a 不包含於 A_b，
式 (5) 已直接矛盾；其餘 query 適用下一節的三接點定理。

## 4. 既有 active-triangle 引理的全部前提銜接

逐項對照 [single-spoke (3,1) 報告 §§1–4](c5_single_spoke_three_one.md)：

| 既有定理前提 | 本頁同一原 M |
| --- | --- |
| 指定 induced-C₅ disk，q-edge-minimal | 刪原 e 繼承 disk；§2 已證 M 自己 minimal |
| 唯一完整 degree-5 root，恰一 spoke | b 的原 degree 五及原 b_s 都保留 |
| 其餘點完整 degree 四 | 原 C／U degree 四，a 在 M 降四 |
| H−root 的連通三接點＋單接點分量 | 正是整份 K=C+a 與原 U |
| 三接點與第四接點互異、完整 relations | (a,y₀,y₁,u) 互異，式 (3)–(4) 保存全部 tuples |
| 原 boundary 附件、bridges、旁支 | 原樣保留，沒有縮短、換圖或拆因子 |
| 同一分量的兩個不同禁色 | 不可刪減覆蓋給 F_K 的兩色；指定入口為 2、3 |
| 一条 root-boundary 邊給 minor 的外部鄰接 | 原 b_s；無需 a 的額外 spokes 作 minor oracle |

整圖只做一次 boundary／四色搬運，把 q 送到 01012；三接點的身份
及原 x 的可能共享一併搬運，不為分量各選色框。既有定理不要求
另一 boundary 列拒絕，亦不要求額外的 T4 或來源大小上限。

該紙面引理以同一 K 的兩份 tight lists、Gallai block palettes
迫出一個 active triangle 及三條原 bridge arms，終點恰為 a,y₀,y₁。
三個 triangle 點各有實際 boundary tether；旁支的 tether 由原邊抽取。
以 {b}、三條 arm 的 connected bags、B 加 tethers 的外部 bag 得
五份互斥非空 connected branch sets；triangle 三邊、原三條 b-contact
邊、三條 tether 首邊及原 b_s 給十對鄰接。故 **M⊆G 含 K₅ minor**。
U 原樣保留，只是不需納入這份 minor。

外部 degree-list 依賴是 [Dvořák 講義 Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，
本輪已核對其 degree assignment、tightness 與 blockwise-uniform 前提。
任意長 arms／旁支的 soundness 由既有紙面證明承擔，沒有從有限 skeletons 外推。

## 5. 固定證書、完整圖控制與重播

[Checker](../scripts/c5_excess_two_mixed_core_four_spoke_ternary.py)／
[joint helper](../scripts/c5_excess_two_four_spoke_ternary_joint_controls.py)／
[artifact](../artifacts/c5_excess_two_mixed_core_four_spoke_ternary/observations.json)
保存原單 spoke 證書中全部剩餘具名 (3,1) 框架，含 root 交換：

| 固定必要域 | 933 | 941 |
| --- | ---: | ---: |
| 原具名框架 | 20 | 60 |
| 同色原 spoke／拒絕列 queries | 40 | 160 |
| marked-leaf slack 覆蓋已矛盾 | 8 | 40 |
| 對齊既有三接點 cover／active triangle | 32 | 120 |
| 未排框架 | **0** | **0** |

每份框架至少有一個同色省略 query，足以排除同一原來源；不宣稱
不同 query 的染色可同時選出。另核對 80 個 root 交換框架及 2,000 次
整體 D₅ query 搬運。具名框架是前序必要骨架，不是可實現圖 catalogue。

320 份 marked 原 K₅ skeletons 將原 a 固定為第一 arm 的原末端，
保留原 x,y₀,y₁,u 及全部四條 root spokes；逐份檢查 C 連通、a／b
degree 五、原 a-spoke 刪除後同一 minor 仍在、五 bags 及十對原鄰接。
這些仍是缺少未用 degree/list 邊的 topology 控制，不能混稱完整 degree 圖。
既有 (3,1) checker 的全部 payload 原樣重算相等，包括 800 minors、
800 reflections、15 covers、356 tight 接線、792 palette states、512 parity
及八個負控制；舊 artifact 不覆寫。

另有 **50 張完整 degree 圖**：五種原 C 形狀（含 shared x、不同接點、
path 中點及 triangle 旁支）×五種原單接點 U×root 交換。
各有全部十列、完整原 (x,y₀,y₁)／u relations、整份 coloring witnesses、
M／G 的六點 joint、K 的三點 tuples 及所有固定 (b,a) 的空／非空纖維。
1,500 次獨立全圖接合、1,500 次完整 K relation 及 24,000 份纖維相等；
300 次同色原 spoke 等式通過。保存一份原 ternary marginal 假允許／
完整 guarded fibre 空的反例。完整圖只核對 relation 身份，沒有宣稱
它們 disk、Σ=933／941 或 Σ-critical。

```bash
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_ternary.py --check
python3 scripts/c5_excess_two_mixed_core_four_spoke_ternary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_single_spoke_three_one.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
python3 tools/artifacts.py status
git diff --check
```

無參數只寫新層；`--check` 重算逐 byte 比對。實際重播及未重跑範圍見
本輪紀錄；前序 two-two 的舊 docs hash 漂移仍保留，本頁不覆寫其
artifact，也不宣稱該舊 byte-check 通過。`lake build` 不形式化本頁 topology。

本輪亦嘗試原單 spoke 的歷史 byte-check，因三份既有 docs input hashes
漂移而未通過；另唯讀重算完整數學 payload 相同。新 observations 保留
三份 drift、原 source digest，詳見本輪紀錄；未覆寫原單 spoke artifact。

## 6. 停止點與保留界線

**停止於四-spoke (3,1)、mixed-(1,2) 加一原單接點 unary 的完整
原身份銜接及任意大小來源排除，含 root 交換。** 本輪不 commit／push。

同 spoke 分拆的 mixed-(1,3) 無 unary 仍保留：下一窄題可固定同一
012／2、q=01021、省略原 a0／a2，核對整份 C+a 的四個原 contacts
(a,y₀,y₁,y₂)、三禁色覆蓋與 marked-leaf slack；此處不宣稱已完成該型。
其他四-spoke／較少 spokes、原 unary 單省略、原 (5,5) q-core、多 mixed、
no-mixed、非相鄰雙 roots 及 unary 側例外仍保留。一般原單 spoke 省略
尚未整型排除；ε≥3、來源實現、一般出口與 K∞=K≤5 均未證。
