# ε=2 四-spoke (2,2)：不相交 spoke-pairs 排除與 mixed-(1,1) 子型完成

**後續（2026-10-04，任務 A）**：[mixed-(1,2)+a-unary 的具名來源排除](c5_excess_two_mixed_core_four_spoke_mixed12.md)
已排原01／23及root交換，核對原crosscut與單一ternary省略身份；
新70／90必要域保存22／26具名殘留。下文§6保留當輪接手點，
沒有把mixed11的完整表當成新incidence分類；ε≥3仍未證。

**後續（2026-10-04，任務 B）**：[mixed-(2,2) 無 unary 的原四接點身份](c5_excess_two_mixed_core_four_spoke_mixed22.md)
獨立完成七共享身份及四條原 spoke 省略全收，20／20必要骨架的原face／
tightness見證仍保留；沒有借本頁 unary crosscut 排除該整型。任務 A 的
mixed-(1,2) 加 unary 入口及下文當輪停止點保持。

2026-10-03，接續[短框弧 mixed 的原拒絕列延拓](c5_excess_two_mixed_core_four_spoke_short_arc.md)，
保留同日既有未提交成果及原 artifacts。接手 HEAD=`0e38127`，使用者
要求繼續推進 ε≥3。本頁沿用原 933／941 固定必要域，處理剩餘 **14／18**
份不相交 spoke-pairs，不重開來源 catalogue。現況見
[Kempe 導覽](c5_kempe_guide.md)，驗證及貼用摘要見
[本輪紀錄](history/2026-10-03-excess-two-four-spoke-disjoint-pairs.md)。

**全部剩餘不相交 pairs 均作任意大小來源排除。** 其中4／8份由一側
unary的所有incident faces都短排除；10／10份迫兩份critical unary
同在唯一共同兩段長框弧，實際支援跨度和≤2卻各至少二，矛盾。
因此在以下前提下，**四-spoke `(2,2)`、mixed-(1,1) 加各側一原
單接點 unary 的整個子型已封閉，含 root 交換**。其他 incidence
與雙 root 分支保留，**共同 ε≥2 不變，ε≥3 未證，未新增 Lean theorem**。

## 1. 同一原圖、固定 faces 與完整接合

G 有限簡單，指定有序 induced-C₅ B=(b₀,…,b₄) 是 disk 外框。
完整 Σ=933／941 或整圖 D₅ 像，每條非框邊 Σ-critical。
有效 H 連通、ε=2，相鄰完整 degree-5 roots a,b，其餘有效內點完整
degree四；H−{a,b} 恰為原 C、U、V。原 mixed C incidence=(1,1)，
contacts=(x,y)、owners=(a,b)，可 x=y 但不複製原點；原 au、bv
各接一原單接點 unary，兩側各兩條 spokes，原 ab 存在。本頁額外
假設兩份原 spoke-pairs 不相交。

保留原 C／U／V 全部內邊、actual attachments／supports、bridges、
旁支、ownership、嵌入環序及一個字面色框。完整原關係及 joint 為

\[
J_G(β)=\{(A,D,X,Y,T,W):(X,Y)\in R_C(β),\ T\in R_U(β),\ W\in R_V(β),
\ A\notin β(S_a),\ D\notin β(S_b),\ A\ne D,X,T,\ D\ne Y,W\}. \tag{1}
\]

所有 tuple 由原分量完整 coloring witnesses 承擔，保存字面 root-pair
的完整纖維與空纖維。以下 geometry 只固定某份原 unary 的短支援，
不改動原 C，亦不將 C marginals 相乘。

## 2. 一側所有 faces 都短：原 unary 非 critical

以原 a-spokes=02、b-spokes=34 為具名例子。原 faces 為

| 原 face | 原框包絡 |
| --- | --- |
| b₀–a–b₂–b₁–b₀ | {0,1,2} |
| a–b₂–b₃–b–a | {2,3} |
| b₃–b₄–b–b₃ | {3,4} |
| a–b₀–b₄–b–a | {0,4} |

V 的所有 incident faces 只有 {2,3}、{3,4}、{0,4} 三個相鄰 pair
包絡。對各 pair 都有原 b-spoke 或 b–a–spoke 外路徑，終點在 pair
外且避開原 C／U／V。原連通 V 位於一個固定 open face，因此
actual S_V 包含於該原 pair。[短支援引理](c5_short_support_singleton.md)
使 V 對每列能避開任何 b 色，原 bv 非 critical，矛盾。
同一紙面機制含 root 交換及共同 D₅ 搬運，排除 **4／8** 份。

## 3. 兩 unary 同在唯一共同兩段長框弧

以原 a-spokes=01、b-spokes=23 為具名例子。原四個 faces 為

| 原 face | 原框包絡 |
| --- | --- |
| b₀–a–b₁–b₀ | {0,1} |
| a–b₁–b₂–b–a | {1,2} |
| b₂–b₃–b–b₂ | {2,3} |
| a–b₀–b₄–b₃–b–a | {0,4,3} |

U、V 各自的兩個短 faces 都有 pair 外的原外路徑；criticality 迫
兩份原 unary 同在最後一個固定長 face F。沿 F 的原框弧次序
I=(b₀,b₄,b₃) 用位置0、1、2。若 U 的實際附件位置 j 大於 V 的
實際附件位置 k，原 U 的 a-to-b_j 路徑及原 V 的 b-to-b_k 路徑
內部互斥，四個 endpoints 沿 F 邊界交錯，違反 disk crosscut。
因此對非空 actual supports

\[
\max\operatorname{pos}(S_U)\le\min\operatorname{pos}(S_V),\qquad
d_U+d_V\le2. \tag{2}
\]

共用原框端點允許等號；空或單點支援已短，不假造缺失的 max／min。
至少一份原 unary 的區間 diameter≤1，actual support 包含於原框邊
04或34。對兩owners都能從原 skeleton 找到 pair 外的原 spoke或
另一root路徑，短支援引理使其原接線非 critical。

等價地，兩條原 critical 接線各迫固定實際支援跨度至少二，式 (2)
卻給 4≤2。相加的是**同一原圖固定幾何支援**，不是不同列的禁色
容量。本證明是[前序三段共同框弧](c5_excess_two_mixed_core_four_spoke_long_face.md)
的同一交錯路徑論證，在兩段框弧上的實例，不需新的跨列 palette 定理。
同機制排除 **10／10** 份。

## 4. 固定原 unary 的完整 witness 替換

按原 embedding及actual supports，在β之前固定已證短的原 W及
接線 e=au或bv。對任意G−e完整coloring，只替換原W的整份witness，
使其contact避開固定owner色；β、roots、原C完整(x,y)witness及另一
unary逐點保持。精確等式為

\[
W=U:\ \pi_{a,b,x,y,v}J_G=\pi_{a,b,x,y,v}J_{G-au},\qquad
W=V:\ \pi_{a,b,x,y,u}J_G=\pi_{a,b,x,y,u}J_{G-bv}. \tag{3}
\]

因此固定原e滿足Σ(G−e)=Σ(G)，與來源edge-minimality矛盾。
不宣稱六角色joint相等、不需Σ(G−C)=Ω或逐列minimal q-core，
也不要求C延拓每個合法root pair。

## 5. 固定證書與整個原子型完成

[Checker](../scripts/c5_excess_two_mixed_core_four_spoke_disjoint_pairs.py)／
[artifact](../artifacts/c5_excess_two_mixed_core_four_spoke_disjoint_pairs/observations.json)
唯讀前序具名frames及原edges、rootorder、spokes、apex rotations。
不相交骨架每份有64cyclic rotation assignments，恰兩份disk
rotations，原faces的頂點集合相同；32份共 **2,048／64**。
這與共用框點骨架每份96assignments不同，沒有修改前序checker
或把舊assert強行套在新圖上。任意嵌入soundness由原crosscut分隔承擔。

每份共同長face保存8×8份actual支援子集，允許空支援、單點及共用
原框端點；區間次序直接核對，不只存跨度或sector包絡。原交錯paths
及外側apex K₃,₃ subdivision只是拓撲控制，不補滿來源degree，
不作染色factor。完整joint替換沿用前序已核對的原unary operator，
其實際沿用／重跑範圍與控制數字見本輪紀錄。

合共1,280actual支援對、80雙非短pairs全部不相容，60明示apex
K₃,₃ subdivisions；32root swaps、12,800共同D₅支援對、3,200列搬運、
1,400短face外路徑搬運及600搬運後subdivision檢查。原01／04完整
degree圖的conditional unary replacement payload重新核對相同，
只作接合算子證據，不宣稱那些圖有本輪不相交spokes。
完整47／75原identity ledger綁定六階段排除，確認無重複／遺漏。

| 完成機制 | 933 | 941 |
| --- | ---: | ---: |
| 共用pair sealed mixed | 7 | 9 |
| 一側短face | 8 | 16 |
| 同一三段長face | 10 | 10 |
| 原unary crosscut | 8 | 16 |
| 共用短框弧指定列延拓 | 0 | 6 |
| 本輪不相交pair：一側全短 | 4 | 8 |
| 本輪不相交pair：共同兩段長face | 10 | 10 |
| **完整原必要域** | **47** | **75** |
| **剩餘同子型frames** | **0** | **0** |

此表只完成明列原incidence子型；所有每份normal form都保留原來源
identity及證據入口，必要表不提供disk實現或候選完整Σ。

## 6. 重播、停止點與下一incidence

```bash
python3 scripts/c5_excess_two_mixed_core_four_spoke_disjoint_pairs.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_disjoint_pairs.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_short_arc.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
python3 tools/artifacts.py status
git diff --check
```

**停止於相鄰唯一mixed、四spoke(2,2)、mixed-(1,1)+各側一原unary
整個子型封閉。** 下一窄incidence是原mixed-(1,2)+a側一原unary，
含root交換：保留原R_C(x,y₀,y₁)，兩個b-contacts為不同原頂點，
允許x與其中一點是同一原頂點；原rootguards為a≠b,x,u及
b≠y₀,y₁。不能把原ternary拆成pair或把兩contacts獨立正規化。
先取原a=5,b=6、spokes01／23的幾何入口，核對原unary crosscut能否
封C及一條原spoke省略後的core身份，再接回同一完整
relation與witness。Mixed-(2,2)無unary、較少spokes、單省略、原
(5,5)q-core、多mixed／no-mixed／非相鄰roots及unary側例外保留。
任意大小紙面＋固定Python，ε≥3、一般出口、來源實現及K∞=K≤5未證；
本輪未commit／push。
