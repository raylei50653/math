# N2-BRIDGE：完整Σ與三列來源的缺口及932排除

2026-10-13，BASE `243a125a80e4d8de40957f59d8da0bdbc974cf69`。
本輪只作本地研究；舊封存、manifest、證書與歷史失敗均保留。

**原 E4 契約的廣義 N2 已排除。** 新增的是完整 mask 932 的來源證明，
加上既有 933／941 及共同 D₅ 像覆蓋，才得到此結論。
**E-ARC2 仍 OPEN**：其剩餘為 N1 及相鄰雙 root 來源，詳見下表。
證據是任意大小紙面證明、明列外部／上游有限分類及獨立核對，沒有新 Lean theorem。

## 1. 真正的前提差異

父量詞直接讀 [E4 §1](../artifacts/c5_excess_two_e4/REPORT.md#1-完整前提依賴與證據層)
及 [E3 §2](../artifacts/c5_excess_two_e3/REPORT.md#2-第-0-步約化成立)，不由 STATUS 推定。

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
