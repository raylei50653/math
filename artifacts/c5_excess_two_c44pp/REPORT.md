# 任務 C44″：兩-root (4,4) 拒絕 q-core 的既有排除覆蓋表

**後續（2026-10-07）。** [no-mixed44](../../docs/c5_excess_two_no_mixed_core44.md)
以 triangle palette 衝突排 U1 的spoke＋unary，並以344份bridge-marker核心的
3,498次完整接回排雙spoke，因此本頁當輪四類44殘留現只剩U2–U4。
本輪亦更正§5的941雙spoke身份收窄：E6-D容許941三-spoke側，不能一律代入t_r≤2；
新排除域已涵蓋此額外保留身份，不依錯誤收窄。
[唯一 mixed 指定稽核](../../audits/2026-10-07-c44pp-mixed-audit/REPORT.md)
亦已核對四份舊報告的化約及固定排除域；沿用上游分類，未重稽核全部上游枚舉。
E5的新證明要求及其他core型仍保留。下文保留C44″當輪覆蓋表與稽核狀態，
目前停止點見[Kempe導覽](../../docs/c5_kempe_guide.md#3-停止點與保留缺口)。

2026-10-06。基準 `integrate-kprime-e3 @ c9f89f0`；分支 `task-c44pp-coverage`，
worktree `/home/ray/developer/ai/math-task-c44pp`。**純紙面整理，沒有新增計算、
新引理或新證明。** 本頁只把既有結果的精確前提對齊到完整 Σ=933／941 來源的各雙 root
分支，標出每格「已排」「部分」「未覆蓋」，並用三份具名 core 逐格檢驗。
研究導覽的停止點由整合者在
[Kempe 導覽 §3](../../docs/c5_kempe_guide.md#3-停止點與保留缺口)更新；本任務未改導覽。

**整合覆核（2026-10-07）。** 更正下文 E5／E6 保留 G1 的任務範圍措辭：
完整 Σ 分支可沿用舊證書，但 E5 另要求新證明，兩種完成標準不能混稱。
§5 補入既有全 degree-4 分類與 E4 core-constraints 的必要限制；沒有新增來源排除。
本輪覆核與實際文件檢查見[整合紀錄](../../docs/history/2026-10-07-c44pp-integration-review.md)。

**結論。**

1. 相鄰 roots、恰一份 mixed（m=1）的兩-root (4,4) cores，在完整 Σ 前提下
   **全排**。依據是舊的完整 Σ mixed-core 系列：雙 spoke、spoke＋unary、雙 unary，
   以及只省略 mixed11。這一格**不依賴 K′**，也沒有 E3 的 J1 精確列缺口；
   E3 的三列前提不足以直接復用部分舊證書；E5／E6 在精確 941／933／940 分支
   也因新證明要求而保留 G1。本表整理舊證書覆蓋，不補該項新證明。
2. 相鄰 m≥3、非相鄰 m≥3（N3）、非相鄰 mixed22 有 (4,4) core（N1-22-44）、
   非相鄰兩 short 無 unary（N2 子類）都是**整個來源分支排除**。唯一 degree-6 分支也已整型排除。
3. 具名 C44-AD3-row0-44 與 C44P-AD2-012-034 屬於同一個 D₅ placement 軌道
   AD-012-034。逐分支檢查後，**它們在任何完整 Σ=933／941、ε=2 來源中都不能是
   兩-root (4,4) core**。相鄰 m=1 由 mixed 省略全收排除，m=0 由 no-mixed 整側預算排除，
   其餘分支由容量或 root 邊排除。第三例 C44P-MIXED3-001 由雙 spoke 排除。
4. **最小未覆蓋子分支（§5）有四項：** 相鄰 no-mixed、相鄰 m=2、
   非相鄰 N1 的 C incidence 11／12／21，以及非相鄰 N2 的五個 (ℓ,u) 族。
   另記一項非 (4,4) 的旁註：具名字面圖若讀成單-root core，會落入 N1 的 root 刪除例外。
5. 未發現使上述排除失效的前提錯置；整合覆核更正了 §6 的任務範圍措辭，
   不把舊證書覆蓋當作 E5 的新證明或完整獨立紙面稽核。

## 1. 前提與兩層假設

**C44″ 目標前提（Σ₀）。** G 有限簡單，B=(b₀,…,b₄) 是指定有序 induced C₅，圍出 disk 外面。
完整 Σ(G) 屬於 933 或 941 的整圖 D₅ 像，每條非框邊都 Σ-critical，
每個有效內點完整 degree≥4，ε=2。由 E2／E3 §2.1，ε=2 只有兩種形態：
唯一 degree-6 root，或兩個 degree-5 roots z,w（其餘完整 degree 四）。
兩-root (4,4) q-core 沿用 [C44 §1](../c5_excess_two_c44/REPORT.md#1-definitions-fixed-before-implementation)
的定義：拒絕同一字面列 q、inclusion-minimal、保留兩個原 roots，且兩者的 core degree 都是四。

**三列前提（Σ₃）。** E3–E6 只假設指定的 q₀＝`01212`、q₁＝`01202`、q₃＝`01021`
被拒絕，四個精確分支是 941、933、940、932
（[E3 §2](../c5_excess_two_e3/REPORT.md#2-第-0-步約化成立)）。
字面 933、941 本身就是 Σ₃ 的 933、941 分支；940 是 933 的整圖反射，
屬於 D₅(933)＝{933,934,940,948,996}
（[C44′ §1](../c5_excess_two_c44p/REPORT.md#1-definitions-and-their-sources)）。
因此 **Σ₀ 經一次整圖 D₅ 搬運後滿足 Σ₃**，E3–E6 的全部結論在 Σ₀ 下都適用。
932 不屬於 Σ₀，本表不處理。

反方向不成立。下列舊報告直接以 Σ₀ 為前提，E3 曾把它們標為三列推廣下的
「精確列缺口」，但這個標註只對 Σ₃ 有效；在 Σ₀ 下它們直接可用：

| 舊報告（前提：完整 Σ=933／941 或 D₅ 像、Σ-critical、disk、ε=2、相鄰、恰一份 mixed） | 結論 |
| --- | --- |
| [雙 spoke 與原省略身份表](../../docs/c5_excess_two_mixed_core_spokes.md) | 保留 mixed 的 (4,4) core 不能省略兩條 spokes；§2 身份表、§3 保留的 C 兩側共用 x |
| [spoke＋unary](../../docs/c5_excess_two_mixed_core_spoke_unary.md) | 一側省略 spoke、另一側省略單接點 unary 的圖全收 Ω |
| [雙 unary](../../docs/c5_excess_two_mixed_core_two_unary.md) | 兩側各省略單接點 unary 的圖全收 Ω |
| [只省略 mixed11](../../docs/c5_excess_two_mixed_omission.md) | Σ(G−C)=Ω；**此來源沒有任何 (4,4) core** |
| [單 spoke 化約](../../docs/c5_excess_two_mixed_core_single_spoke.md)、[五-spoke leaf fibres](../../docs/c5_excess_two_mixed_core_leaf_fibers.md) | 兩側不能同時有三條 spokes；兩候選的總 spokes 都≤4 |

這些報告的前序條件包括 Σ(G−zw)=Ω 與兩個刪 root 圖全收，
見 [root 刪除 §3–§4](../../docs/c5_excess_two_root_deletions.md)。
E3 可移植性表把它們列為「直接」。

**稽核狀態。** E4／E5／E6 的引用引理由 [D₉](../../audits/2026-10-06-task-d9/REPORT.md)
判定 holds。E3 由 [D₈](../../audits/2026-10-04-task-d8/REPORT.md) 判定 holds，
唯一度-6 分支須連同 DG6-1 補表引用。盾弧引理 1／2 由 D₆ 確認，1(d) 採更正後的開面版本。
上表舊 (4,4) 系列只在 [任務 D](../../audits/2026-10-04-task-d/REPORT.md) 中當作輸入做過
byte replay（兩份文件 hash FAIL，數學 payload 未變），**沒有獨立紙面稽核**。
本表照實標示，不把 replay 當成稽核。

## 2. (4,4) core 的共同省略身份

下列身份是各分支共用的介面。它們來自原 degree-4 飽和，
以及每個 root 的 loss 屬於 {0,1}：
[mixed-core spokes §2](../../docs/c5_excess_two_mixed_core_spokes.md#2-全部-proper-core-的具名省略表)、
[E3 nonadjacent §5](../c5_excess_two_e3/REPORT.md#5-第-2-步-ii-a先處理非相鄰雙-roots)、
[E6 §3](../c5_excess_two_e6/REPORT.md#3-e6-bcj6-的共同-core欄位與框邊預算)。

- **保留全部 mixed：** 兩側各省略一個單容量因子，即一條原 spoke，或一整份 capacity-one unary。
- **省略一份 mixed：** 被省略的那份 incidence 必為 (1,1)，且不得再省略任何其他因子。
- **全 degree-4 分類**（[k4 blocks §4](../../docs/c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論)）：
  所有簡單環都是 triangle。所以兩-root (4,4) core 至多保留一份 mixed。
  相鄰時，保留的那份 C 兩側必共用同一 contact x，構成原 triangle zwx；
  非相鄰時，每側至多兩個 contacts。

## 3. 覆蓋表

「已排」表示該分支內的全部兩-root (4,4) 拒絕 q-core 都已有任意大小的來源排除。
「部分」列出已排的子型與剩餘的具名子型。各格的出處均在 Σ₀ 下成立。

| 分支 | 可能的 (4,4) 省略身份 | Σ₀ 狀態 | 出處與精確前提 | Σ₃ 下的對照 |
| --- | --- | --- | --- | --- |
| 唯一 degree-6 | 無兩個原 roots，不定義兩-root core | **已排（整個來源）** | [E3 §4](../c5_excess_two_e3/REPORT.md#4-第-2-步-i唯一-degree-6-全部分拆) t=0–3 全分拆，t=1 的 (4,1)／(3,2) 須連同 [D₈ DG6-1 補表](../../audits/2026-10-04-task-d8/REPORT.md) | 同左 |
| 相鄰 m≥3 | 依 §2 本無 (4,4) core | **已排（整個來源）** | [E6-A](../c5_excess_two_e6/REPORT.md#2-e6-a四條原路證明相鄰-m≤2)：zw 加三條 mixed 路隔離整份 mixed，違反 N-empty；D₉ holds | 同左 |
| 相鄰 m=2 | 省略一份 C₁₁，保留另一份 C₁₁ 並共用 x（zwx triangle），不得再省略其他因子 | **部分** | [root 刪除式 (7)](../../docs/c5_excess_two_root_deletions.md#4-相鄰-mixed刪原-root-邊的全-degree-4-化約)：Σ(G−zw)=Ω、兩刪 root 圖全收；[E6 §3](../c5_excess_two_e6/REPORT.md#3-e6-bcj6-的共同-core欄位與框邊預算) 的身份限制；E6-A 附帶：含 B 的面由兩條 mixed 路圍成，zw 在有界側。**沒有任何結果排除這個身份** | E6「J6 m=2 限」 |
| 相鄰 m=1，C incidence≠(1,1) | 依 §2 本無 (4,4) core（保留 C 須單 contact x；省略 C 須 (1,1)） | **已排** | [mixed-core spokes §2–§3](../../docs/c5_excess_two_mixed_core_spokes.md) | 同左（E6 §3） |
| 相鄰 m=1，保留 C₁₁：雙 spoke | 兩側各省略一條 spoke | **已排** | [mixed-core spokes §4–§5](../../docs/c5_excess_two_mixed_core_spokes.md)；E3 把它列為「三列」可用 | 已排（E3 表） |
| 相鄰 m=1，保留 C₁₁：spoke＋unary | 一側 spoke、一側單接點 unary，含 root 交換 | **已排** | [spoke＋unary](../../docs/c5_excess_two_mixed_core_spoke_unary.md)（Σ₀ 精確 target） | J1／G1：E6-H 只化到 G2 二邊 U 或 J4 入口 |
| 相鄰 m=1，保留 C₁₁：雙 unary | 兩側各省略單接點 unary | **已排** | [雙 unary](../../docs/c5_excess_two_mixed_core_two_unary.md)（Σ₀，不經 K′） | 長 C 由六邊預算排除；短 singleton 待 K′（E3 §6） |
| 相鄰 m=1，只省略 C₁₁ | G−C | **已排** | [mixed 省略](../../docs/c5_excess_two_mixed_omission.md)：Σ(G−C)=Ω | J1／G1：E6 §7 的 J2／J3／J4／J6 原族，Ω 未證 |
| 相鄰 m=0（no-mixed） | 兩側各省略一個單容量因子；恰一份 U_z、一份 U_w；U_r 可省略 ⇔ t_r=3 | **部分** | [E6-D](../c5_excess_two_e6/REPORT.md#4-e6-dno-mixed-的整側預算與精確殘留)：兩側不能都三 spokes；t_r=3 只在 941 且 S_r=013（U 支援 123 或 034）。[盾弧定理 A(4)](../../docs/c5_unary_shield_budget.md#3-定理-a全圖至多兩份-unary-分量)：全部 spokes 落在 3 或 2 個指定框點。刪 root 至多一側只缺一列 | 同左（E6「no-mixed 限」） |
| 非相鄰 m=0 | — | **已排（不存在）** | H 連通迫 m≥1（[E3 §5](../c5_excess_two_e3/REPORT.md#5-第-2-步-ii-a先處理非相鄰雙-roots)） | 同左 |
| 非相鄰 N3（m≥3） | 依 §2 本無 (4,4) core | **已排（整個來源）** | [E4 N-theta／N3](../c5_excess_two_e4/REPORT.md#5-n3theta-排除全部-m≥3)；D₉ holds | 同左 |
| 非相鄰 N1（m=1，separating C），C incidence (2,2) | 兩側各省略一個 unit（spoke 或 capacity-one unary），sole C 不可省略 | **已排** | [E4 N1-22-44](../c5_excess_two_e4/REPORT.md#3-n1-主攻22-mixed-加-44-core-整類排除)；D₉ holds | 同左 |
| 非相鄰 N1，C incidence (1,1)／(1,2)／(2,1) | 同上 | **未覆蓋** | E4 §3.4、§6 只保留完整原 relation 介面；unary≤2，至多一個 root 省略例外列 | 同左 |
| 非相鄰 N2（m=2），兩份都短且無 unary | 省略一份 C₁₁，保留另一份 | **已排（整個來源）** | [E4 N2-short-no-unary](../c5_excess_two_e4/REPORT.md#42-n2-short-no-unary整類接受全部三色列)；D₉ holds | 同左 |
| 非相鄰 N2，其餘 (ℓ,u) | 同上；兩刪 root 圖全收 | **部分（剩五族）** | [E4 §4.3](../c5_excess_two_e4/REPORT.md#43-n2-精確殘留)：ℓ+u≤2；全短時拒絕列兩側 E 互斥；同一 (4,4) 原省略圖只缺一列 | 同左 |
| root 刪除例外 | 不是兩-root core，型為 (4,absent) | **不適用** | [root 刪除 §3](../../docs/c5_excess_two_root_deletions.md)：相鄰有 mixed、非相鄰 m_z,m_w≥2 時兩者全收；其餘情形至多一列例外，且 core＝原 S_r | 同左 |

非相鄰時的完整 relation 介面（R_P、A_P、E_r、J_G 及刪邊 witness）見
[E4 §6](../c5_excess_two_e4/REPORT.md#6-完整原-relation-的參數化交付與-core-身份)。
本表不重述，也不填成有限必要表。

## 4. 具名 core 逐分支檢驗

### 4.1 同一軌道

C44-AD3-row0-44 的 core 非框邊為 06,16,25,35,45,46,56：root 5 的 spokes 是 {2,3,4}，
root 6 的 spokes 是 {0,1,4}，共用框點 4，拒絕 row 0＝`01012`，Σ(M)=1022。
C44P-AD2-012-034 的 spokes 是 {0,1,2}／{0,3,4}，共用 0，拒絕 row 6＝`01212`，Σ(M)=959。
整圖旋轉 i↦i+4 把 {0,1,2}／{0,3,4} 送到 {4,0,1}／{2,3,4}，並交換兩個 roots。
兩者同屬 [C44′ §4](../c5_excess_two_c44p/REPORT.md#4-exhaustive-two-private-vertex-classification-part-b)
的 AD-012-034 軌道（10 個 placements，唯一相容的 disk 軌道）：
C44′ 表中 AD-234-014 的 Σ1022 拒絕 row 0，正對應 C44-AD3。
共同形狀是兩個相鄰 roots、各三條**連續** spokes、spokes 合起來碰齊五個框點，
且沒有其他 private 頂點。

### 4.2 這個形狀需要的來源

以下是代入已知限制的記帳，不是新引理。設這個形狀是兩-root (4,4) core M⊆G。

- M 含 root 邊，所以 G 的 roots 相鄰。
- T4 給 t_r≤3，而 M 已有三條 spokes，所以 G 的 spokes 恰為 M 的 spokes，
  被省略的 incidence 不是 spoke。
- deg_G(r)=5＝3＋1（zw）＋1，所以每個 root 恰有一個 piece incidence，M 省略全部 pieces。
- 因此 G 只有兩種可能：(i) m=1，一份 C₁₁、無 unary，M＝G−C；
  (ii) m=0，兩份 capacity-one unary，M＝G−U_z−U_w。m≥2 需要每側至少兩個 piece incidences，不可能。

| 分支 | 判定 | 依據 |
| --- | --- | --- |
| 相鄰 m=1，(i) | 排除 | 只省略 C₁₁ 的身份由 Σ(G−C)=Ω 排除；另由「兩側不能同時三 spokes」、總 spokes≤4<6 各自排除 |
| 相鄰 m=0，(ii) | 排除 | E6-D：兩側不能都三 spokes。盾弧定理 A(4) 亦排除：spokes 只能落在≤3 個框點，此形狀卻碰齊五點 |
| 相鄰 m=2、m≥3 | 排除 | m=2 時 t_r≤2；m≥3 本身已排 |
| 非相鄰 N1／N2／N3 | 不適用 | core 含 root 邊。非相鄰的兩 private 頂點類比需要四 spokes，違反 T4；C44′ §4.1 也給 disk 不可能 |
| 唯一 degree-6 | 不適用 | 整個來源分支已排 |

所以**兩份具名 core 都沒有 Σ₀ 來源**。這與它們實際的來源 Σ 一致：
C44-AD3 來源為 Σ956，正是 (i) 型；C44P-AD2 未提供完整 Σ=933／941 的來源構造。
在 Σ₃ 下，(i) 型就是 [E6 §7](../c5_excess_two_e6/REPORT.md#7-e6-hg1-用-actual-core-分組不預填-ω)
表中 (k_z,k_w)=(0,0) 的「J6：六 spokes、C11、無 unary」，仍保留。
這說明**完整 Σ 前提正是在 (i) 型上發揮作用**。

### 4.3 第三例 C44P-MIXED3-001

C44P-MIXED3-001 來自同一個 Σ956 AD3 來源的 G−45−46：保留 mixed 單點 7，
triangle 為 567，spokes 為 5→{2,3}、6→{0,1}、7→{1,2}。
它的身份是「相鄰 m=1、保留 C₁₁、雙 spoke」，Σ₀ 下由
[mixed-core spokes §5](../../docs/c5_excess_two_mixed_core_spokes.md#5-完整同框接回及結果) 排除；
依 E3 可移植性表，Σ₃ 下也排除。

### 4.4 旁註：單-root 讀法

同一張字面圖也可讀成單-root core：一個頂點是原 root r，另一個是 r 的原 degree-4
unary 單點 {s}，另一個 root w 完全省略。此時 core 型為 (4,absent)，屬於 root 刪除例外，
**不是兩-root (4,4) core**，不在本表範圍。只依既有結論代入：

| 分支 | 判定 | 依據 |
| --- | --- | --- |
| 相鄰有 mixed、非相鄰 m_z,m_w≥2 | 不可能 | 兩刪 root 圖全收 |
| 相鄰 no-mixed | 不可能 | 整側 {r,s} 碰齊五點；盾弧引理 2 給整側盾弧≥4，另一側≥2，違反 E6-D 的 λ_z＋λ_w≤5 |
| 非相鄰 N1，r 側 mixed incidence 為 1 | **既有結果未排除** | 只受「至多一列例外、core＝原 S_r、只缺一列」限制；Σ959 只拒絕一列，與此相容 |

最後一列未作分析。

## 5. 最小未覆蓋子分支清單

下表保留C44″當輪清單；U1的941身份更正及後續全排見本節更正段，現況只剩U2–U4。

在 Σ₀、ε=2、兩個 degree-5 roots 之下，兩-root (4,4) 拒絕 q-core 只可能出現在：

| # | 子分支 | 精確殘留身份 | 已知必要限制 |
| --- | --- | --- | --- |
| U1 | 相鄰 no-mixed | (spoke_z, spoke_w)，t_z=t_w=2，兩份 U 都保留；或 (spoke_z, U_w)，t_z=2、t_w=3、S_w=013 型、941，保留 U_z（含 root 交換） | 全 degree-4 core 的內部最大度≤3；E6-D 整側盾弧 λ_z＋λ_w≤5；定理 A(4) 指定框點；E6-C 欄位；刪 root 至多一側單列例外 |
| U2 | 相鄰 m=2 | 省略 C₁₁，保留另一份 C₁₁ 並共用 x | Σ(G−zw)=Ω；兩刪 root 圖全收；E6-A 的外界路；每側 t_r＋(unary incidences)＝2；全 degree-4 分類限制保留的枝 |
| U3 | 非相鄰 N1 | C incidence (1,1)、(1,2)、(2,1)；兩側各省略一個 unit | unary≤2；每側 contacts≤2；至多一 root 省略例外；原三-spoke set 不可為 024／124 |
| U4 | 非相鄰 N2 | 省略一份 C₁₁、保留另一份；(ℓ,u)∈{(2,0),(1,0),(1,1),(0,1),(0,2)} | 兩刪 root 圖全收；ℓ+u≤2 及盾弧總長≤5；全短時拒絕列 E_z∩E_w=∅；原三-spoke set 不可為 024／124；該 core 所拒絕列的兩側原 spokes 均不得重色 |

U1 的細化只代入[全 degree-4 core 分類](../../docs/c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論)：
其內部最大度至多三。no-mixed 恰一份 U_r、incidence k_r=4−t_r；
省略 spoke 而保留 U_r 與 zw 時，deg_(H_M)(r)=1+k_r=5−t_r≤3，故 t_r≥2。
結合 E6-D 的 t_r≤2 得 t_r=2；省略 unit U 的另一側則有 k_r=1、t_r=3。
這是已有分類的記帳代入，不排除這兩份來源身份。

**更正（2026-10-07）。** 上段「結合E6-D的t_r≤2」只適用933／940，
不適用941。941的t_r=3側可以保留unit U並省略spoke，此時core內度為2，
最大度≤3的限制並未排除它；因此當輪U1雙spoke仍須保留(2,3)含交换。
[後續no-mixed44](../../docs/c5_excess_two_no_mixed_core44.md)已用全部344份
bridge-marker核心的3,498次接回排雙spoke，不依此收窄；spoke＋unary亦已另排。
這是必要身份論證的更正，沒有提供新增身份的來源實例。
U3／U4 新列出的 private-spoke 與重色限制見
[E4 CORE_CONSTRAINTS §4](../c5_excess_two_e4/CORE_CONSTRAINTS.md#4-三列-private-spoke-和-n2-精確-qcore-身份)。
N2 若一側原 spokes 在 q 下重色，只能有 exact spoke omission 的 (4,5)／(5,4) core，
不能把該列算入 U4 的 (4,4) 身份；五個 (ℓ,u) 族仍保留。

U1 的三-spoke 身份只出現在 941。933／940 的兩-root44 no-mixed 身份只剩兩側恰兩 spokes 的 (spoke, spoke)。
具名軌道 AD-012-034 不落在 U1–U4 的任何一項（§4.2）。
另記 §4.4 的非 (4,4) 項：**N1 root 刪除例外中的單-root 讀法**。
ε≥3 不在本表範圍。

## 6. 前提與引用核對（停止條件）

逐項核對 C44″ 提議所列的引用，以及上表各格的出處：

| 引用 | 原前提 | 本表用法 | 判定 |
| --- | --- | --- | --- |
| 相鄰唯一 mixed (4,4) 全排、總 spokes≤4 | Σ₀、相鄰、恰一份 mixed | 相鄰 m=1 各格、§4.2 (i) | 相符 |
| E3 兩 mixed 互斥路（nonadjacent §5） | Σ₃、非相鄰 | §2 至多保留一份 mixed；相鄰版由 root 刪除 §4 與 E6 §3 給出 | 相符 |
| E4 N1-22-44 | Σ₃、非相鄰、sole mixed22、存在兩-root 44 core | N1 (2,2) 格 | 相符 |
| E6 相鄰 m≤2 | Σ₃、相鄰、任意 core 型 | 相鄰 m≥3 格 | 相符 |
| D₉ 稽核結論 | 指定引理在其前提下 holds | 稽核狀態欄 | 相符；D₉ 的 63 份控制都未觸發三列前提，不能當作來源排除的實驗控制 |
| 盾弧定理 A(4) | (S)＝Σ₀ 並恰兩份 unary | 相鄰 no-mixed、§4.2 (ii) | 相符；引理 1(d) 採 D₆ 更正版 |

**未發現使排除失效的前提錯置；整合覆核更正一項任務範圍措辭。**
G1 的兩個 (4,4) 入口（retaining spoke＋unary、只省略 mixed11）在 Σ₀ 下
已有舊系列覆蓋，J6 的 (0,0) 六-spoke 型亦然。E3 不直接把精確 Σ 結果推廣至 Σ₃；
但 E5 在 941／933／940 分支保留 G1，還有另一個原因：
[E5 §2](../c5_excess_two_e5/REPORT.md#2-依賴項-×-分支狀態表)明言該任務要求新證明，
不直接沿用舊 exact-target solver 作結案。本表只整理既有覆蓋，沒有滿足這项新證明要求，
也沒有完成舊 (4,4) 系列的全部獨立紙面稽核。G2–G4、J6 其他 core 型及來源殘留照舊。

## 7. 證據界線

本頁只做出處對齊與記帳代入，沒有新增 Python、Lean 或圖枚舉，也沒有執行 lake build。
各格的任意大小結論仍由原報告承擔，原報告的外部依賴照舊：
degree-list tightness／Gallai 刻畫、K₅ 不可平面、全 degree-4 分類，以及舊系列的
固定必要域 Python 證書。舊 (4,4) 系列沒有獨立紙面稽核；若後續要以它關閉 Σ₀ 的相鄰 m=1，
建議先補這一層稽核。本頁沒有提出新證明，也沒有在任何未覆蓋分支上嘗試排除。

```sh
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```
