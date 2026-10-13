---
docgraph:
  id: c5.excess-two-n2-bridge
  family: [c5, c5.excess-two, c5.n2, c5.arc2]
  derives_from:
    - c5.excess-two-arc-pair-critical
    - c5.excess-two-n2-unary-three-row-escape
    - c5.excess-two-n2-partition-rule
    - c5.excess-two-n2-unary-diff-closure
    - c5.excess-two-n2-one-long-closure
    - c5.excess-two-n2-ll-cut
  related:
    - c5.excess-two-nonadjacent-unit-core45
    - c5.excess-two-arc-component-slack
---
# N2-BRIDGE：完整Σ與三列來源的缺口及932排除

2026-10-13，BASE `243a125a80e4d8de40957f59d8da0bdbc974cf69`。
本輪只作本地研究；舊封存、manifest、證書與歷史失敗均保留。
後續整理與原證據保存見[發布紀錄](history/2026-10-13-n2-rank2-c8-publish.md)；
原audit的「未commit／push」保留研究完成截點。

**原 E4 契約的廣義 N2 已排除。** 新增的是完整 mask 932 的來源證明，
加上既有 [933／941完整契約九格覆蓋](c5_excess_two_n2_residual_unification.md)
及共同 D₅ 像覆蓋，才得到此結論。
**E-ARC2 仍 OPEN**：其剩餘為 N1 及相鄰雙 root 來源，詳見下表。
證據是任意大小紙面證明、明列外部／上游有限分類及獨立核對，沒有新 Lean theorem。

## 0. 依賴與覆蓋的閱讀順序

以下按結論的適用契約串接；有日期的舊OPEN與控制數字保留當輪語境。
DocGraph metadata記錄報告中實際使用的結果與接口，不代表整份來源契約可直接繼承。
N45節內的後續摘要是導航，不反向成為舊N45採納的前置；本頁移植OL／LL等局部證明前，
另在§2補足932所需前提，沒有把N45完整Σ契約或SD-A套到932。

| 階段 | 權威來源與依賴 | 實際覆蓋 |
| --- | --- | --- |
| 真子圖單拒絕 | [pair-critical §3](c5_excess_two_arc_pair_critical.md#3-任意真子圖至多單拒絕)的一般P引理；須先核對Z前提 | 完整Σ目標用既有44覆蓋；932另用本頁U4三列移植建立Z=∅ |
| 分量必留、45／54排除 | [N45](c5_excess_two_nonadjacent_unit_core45.md)採納＋[分量slack](c5_excess_two_arc_component_slack.md)→[spoke closure](c5_excess_two_arc_spoke_closure.md) | 指定完整Σ的N2全部真cores排除；逐列只剩原G的55 core。932由本頁另證分量witness，不直接沿用N45 |
| 原55共同結構與容量 | [block骨架](c5_excess_two_arc_size_bound.md)→[九格統一](c5_excess_two_n2_residual_unification.md) | 原cactus、leaf contacts、附件單射與共同容量；35點上界／有限下界未構成排除矛盾，數值上界不是OL／LL收尾前提 |
| 原55五個參數子情形 | 下表的unary、OL與LL鏈 | 指定完整Σ933／941或整圖共同D₅像的原55全排；三relation族×44／45-54／55共九格完成 |
| 父三列N2橋接 | 本頁§1–2、[前提帳本](../audits/2026-10-13-n2-bridge-243a125/paper/PREMISE_LEDGER.md)與[Theorem NB](../audits/2026-10-13-n2-bridge-243a125/paper/CLOSURE.md) | 941／933沿用完整Σ鏈，940整圖反射成933；932另補U4／五列slack／CW／UC3，排原E4完整三列來源契約的N2 |

令ℓ為原long mixed數、u為原unary數、t為原root-spoke總數。
以下五個子情形均保[原55完整契約](c5_excess_two_n2_diagonal_three_row.md#1-完整來源契約)，
不是五份可實現來源，也不能把完整Σ直接弱化為任意三列拒絕。

| 原55子情形 `(ℓ,u)` | 排除鏈與同列接回 |
| --- | --- |
| `(0,2)` | [九格統一 §3](c5_excess_two_n2_residual_unification.md#3-共同三-hub-引理與兩-unary-子族排除)：兩mixed為pair，原盾邊收費 `1+1+2+2>5` |
| `(0,1)` | [unary三列候選](c5_excess_two_n2_unary_three_row_escape.md)→[diagonal獨立採納](c5_excess_two_n2_diagonal_three_row.md)：同一U至少一指定列接受D，兩short在同一列以完整 `(D,D)` lifts接回 |
| `(1,1)` | [long同步](c5_excess_two_n2_long_synchrony.md)→[接口分割／已用禁色界](c5_excess_two_n2_partition_rule.md)排三接線U；[兩接線Diff全色出口](c5_excess_two_n2_unary_diff_closure.md)接同列G−U的實際owner pin |
| `(1,0)` | [OL一long排除](c5_excess_two_n2_one_long_closure.md)：原末端block／minor與固定root的完整外側接回，任意原長度皆覆蓋 |
| `(2,0)` | [雙long共同容量](c5_excess_two_n2_double_long_joint.md)排t=0／1；[LL-CUT+diag](c5_excess_two_n2_ll_cut.md)以原leaf minors及新增完整diagonal資訊排剩餘t=2／3 |

**來源排除與基本機制分開。** LL-CUT+diag完成上述完整來源排除；基本LL-CUT只讀基本S，
尚未獨立證成必觸發cut。19,229共同可行投影既不是來源實現，也不是基本LL-CUT反例。
有限完整N2控制仍not triggered；紙面來源排除、上游有限分類及Lean狀態分開，無新Lean theorem。

**對E-ARC2的覆蓋。** 原域 `1≤|Q|≤4` 的N2已由完整Σ鏈涵蓋；932的補證擴展原E4三列N2，
不擴大E-ARC2原域。父命題仍剩N1與相鄰m=0／1／2，精確core例外、已排具名子域及後續入口
見[§3父分類](#3-接回父分類與剩餘來源)與[父覆蓋表](../audits/2026-10-13-n2-bridge-243a125/paper/PARENT_COVERAGE.md)。

## 1. 真正的前提差異

父量詞直接讀 [E4 §1](../artifacts/c5_excess_two_e4/REPORT.md#1-完整前提依賴與證據層)
及 [E3 §2](../artifacts/c5_excess_two_e3/REPORT.md#2-第-0-步約化成立)，不由 STATUS 推定。

**具名定理NB的原來源契約（包括932）。** G為有限簡單planar disk，B是指定有序induced C₅；
T4五列全收，每條原非框邊對完整有序Σ critical，ε=2。
兩個原完整degree5 roots r,s不相鄰，其餘有效內點原完整degree4；
H−{r,s}恰兩份原mixed，其餘分量為unary；在同一原色框拒絕q₀、q₁、q₃，q₂／q₄不預設。
保留全部原接點身份、ordered/shared contacts、owners、實際附件與支援、rotation、bridges、旁支、
完整relations、空fibres及full lifts；自由孤立點只從有效計數略去，四色乘積因子仍保留。
有效H連通／full B-touch及pieces one-sided沿E2／E3／E4導出；
逐列minimality、分量刪除全收與H二連通都不是「三列拒絕」自行提供的前提。
完整陳述及證明以[Theorem NB §1](../audits/2026-10-13-n2-bridge-243a125/paper/CLOSURE.md#1-statement-and-the-exact-missing-bridge)為準。

| 前提 | 完整Σ來源 | 父三列 N2 |
| --- | --- | --- |
| 有序 induced-C₅ disk、完整原圖與色框 | 保留 | 相同 |
| T4 全收、每條非框邊對完整Σ critical | 要求 | 已要求，並非新增假設 |
| ε=2、有效 H 連通／碰齊 B | 要求／由一般來源推出 | 相同；沿 E2／E3 推導 |
| 非相鄰原 degree5 roots、其餘有效內點 degree4；恰兩 mixed | N2 身份 | 相同 |
| q₀=01212、q₁=01202、q₃=01021 | 拒絕 | 拒絕 |
| q₂=01201、q₄=01012 | 完整 mask 決定 | 各自不限定 |
| 每條邊釋放至少一個指定列 | E3 可導出 | E3 可導出；不等於逐列 minimal |
| 分量刪除全收、原55逐列 minimal | 舊44／N45等鏈導出 | 不能直接沿用；本輪另補 witness 橋接 |

固定原色框的完整可能性只有：

| Σ | q₂ | q₄ | 本輪接入 |
| ---: | --- | --- | --- |
| 941 | 接受 | 接受 | 既有完整Σ排除 |
| 933 | 拒絕 | 接受 | 同上 |
| 940 | 接受 | 拒絕 | 整圖共同反射 i↦1−i 成933 |
| 932 | 拒絕 | 拒絕 | 新排除，見§2 |

因此未覆蓋的完整關係恰為932；不是所有舊引理都能刪去完整Σ前提。
逐引理的原前提、可移植性、有限末端與外部依賴見
[前提帳本](../audits/2026-10-13-n2-bridge-243a125/paper/PREMISE_LEDGER.md)。

## 2. 新來源橋接及證明

精確定理及全證明見 [Theorem NB](../audits/2026-10-13-n2-bridge-243a125/paper/CLOSURE.md)。
以下每步都在同一原圖、同一有序 B 上進行。

1. **U4 三列移植。** 原 U4 的必要域化約保完整 root joint；828 份標記 core
   在自身拒絕列以外的每個三色列，都有兩個共用一側座標的實際 root pairs。
   被省略的原 mixed11 每行／每列最多禁一格，故不能另增三色拒絕。
   此證明不讀 q₂／q₄ 的接受性，廣義 N2 的兩-root44因而排除。
   兩 mixed 亦排單-root core，於是 Z=∅；一般真子圖定理 P 可用。
2. **932 的五列 slack。** 每個非相鄰框點對在五列中重色兩次。若同接某個內點，
   刪一條 spoke 仍拒絕兩列，違 P；包括 roots 在內，框附件都至多相鄰兩點。
   P 又給每份 G−C 至少四個三色列的完整外部 lifts。任去一列後的框點／框邊
   signatures 仍互異，Gallai palettes 與原 K₅ minors 因而迫 leaf 私有 root-contact，
   排 unit unary。結合無44／無單-root core，得到所有 **Σ(G−C)=Ω**。
3. **含 unary 的獨立排除。** 原盾弧先給 u≤1；兩 short 以 unary 未用色出口
   同列接回。一 long 時支援恰三點弧：k_U=3 的 owner 沒有 spoke，直接完整 fibre
   容量迫每列 `|F_U|≥2`，與同列未用色出口及已用禁色至多一矛盾；k_U=2則
   原五形 Diff 全色出口接回實際 G−U lift。此步不使用廣義 N45。
4. **無 unary 的接回。** 原 cactus、leaf、H 二連通、度二附件單射及 root 附件界
   已逐項導出。一 long 的 OL 與兩 long 的 LL-CUT+diag 證明只需要這些結構、
   原 degree 計數、三列拒絕與完整 fibres；不再需要 q₂／q₄ 或 spoke 刪除見證。
   兩 short 由 N-diagonal 同列接回，窮盡原兩 mixed 的所有情形。

最小缺失介面可正式寫成 **CW(I)**：對每份原 C、每個 i∈{0,1,3}，
至少一條 C-incident 原邊刪除有同列完整 lift；degree-four 分量解除使它等價於
G−C 在該列有完整外部 lift。另保 root 附件至多相鄰兩點，即足以移植 OL／LL。
這是證明所需的較弱充分前提，不宣稱它在所有可能證明中邏輯最小。
[新局部定理](../audits/2026-10-13-n2-bridge-243a125/paper/BRIDGE_LEMMAS.md)
分開 CW、五列橋接、原 block 結構及容量修補；932 證明不需要 SD-A。

## 3. 接回父分類與剩餘來源

E-ARC2 原域有 `1≤|Q|≤4`，所以932本來就在域外；ε≥3也不是它的剩餘義務。
兩 roots 不相鄰時 H 連通使 mixed 數至少一，E4 已排 m≥3；本輪排 m=2，故只剩N1。
相鄰 roots 的 m≥3 由 E6 排除，m=0／1／2仍須各自原分類。

| 父來源 | 本輪後的精確狀態 |
| --- | --- |
| 唯一 degree6 原 root | 已由 E3＋D₈ 排除；不是單-root core 例外 |
| 非相鄰 m≥3 | E4 已排 |
| 非相鄰 m=2（N2） | 原E4三列契約全排，包括932；所有core身份一併涵蓋 |
| 非相鄰 m=1（N1） | E-ARC2域的兩-root44已排；45／54、原55及允許的單-root4例外仍OPEN |
| 相鄰 m=0／1／2 | E-ARC2域的兩-root44已有覆蓋；其餘未排來源保留45／54、原55，m=0另保允許的單-root4例外 |
| 相鄰 m≥3 | E6 已排 |

上述OPEN列是原分類支持的來源集合，須扣除各權威報告已排的具名子域；
不是聲稱每個組合都可實現。逐項限制、G1–G4／J4／J6路由及具名 ledger 見
[父覆蓋表](../audits/2026-10-13-n2-bridge-243a125/paper/PARENT_COVERAGE.md)。
本輪沒有把N2結論升為E-ARC2、一般 ε≥3下界、一般出口或 `K∞=K≤5`。

## 4. 驗證與反控制

[Audit REPORT](../audits/2026-10-13-n2-bridge-243a125/REPORT.md)保存凍結來源、
兩份紙面審查、主checker、獨立數值DFS及實際驗證範圍。
獨立U4重算保132,480含空fibres及全部原染色，3,312三色接回碰撞成立。
固定平面原圖的完整十列、rotation、degree、minimal cores與逐邊 lifts另存：
Σ956反駁不加Z前提的P及任意選列critical推論；Σ1013提供P正控制；
U4的Σ1018控制反駁把三色列保持誤升為全部十列保持。
它們只反駁實際滿足的弱化命題；完整廣義N2 source皆 **not triggered**。
來源排除由紙面證明承擔，沒有從零觸發推論不存在。

```bash
python3 -B audits/2026-10-13-n2-bridge-243a125/checker.py --check --negative-tests
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-n2-bridge-243a125/checker.py --check --negative-tests
python3 -B audits/2026-10-13-n2-bridge-243a125/independent_checker.py --check --negative-tests
python3 -B audits/2026-10-13-n2-bridge-243a125/independent_checker.py --u4 --check --negative-tests
python3 -B audits/2026-10-13-n2-bridge-243a125/independent_checker.py --arithmetic --check
python3 -B audits/2026-10-13-n2-bridge-243a125/independent_checker.py --u4-t3-negative --check
```

本輪沒有新 Lean theorem；基本LL-CUT作為僅讀基本S的證書機制仍未獨立證成。
