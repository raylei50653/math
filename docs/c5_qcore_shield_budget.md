# 任務 W：單列 q-core 盾弧預算與共鄰 P₃ ledger 篩選

2026-10-04，分支 `shield-budget-hub-principle`，基準
`ca3870f9b79684c2100480d0dc04523899666928`。本任務完成；研究線的整合入口仍由
[Kempe 導覽 §3](c5_kempe_guide.md#3-停止點與保留缺口)與
[weak-deletion 導覽](c5_weak_deletion_guide.md)維護，本輪不修改它們。

**獨立稽核（2026-10-04，D₆）**：[稽核報告](../audits/2026-10-04-task-d6/REPORT.md)逐項重推，數學判定全部確認；補出零-unary 側排除後，結論升為 C §1 整個共鄰端點 P₃ 來源分支排除完成。交付缺口（verdict 綁定更正前的盾弧文件 hash）已修補，見 §8。

**結論：改色引理成立，且已有同一結論；W 的盾弧移植成立，但必須精確保留
singleton 缺點。任務 C 的全部 3,497 個開放 keys 可作來源排除。**
後者有更強的、不需要 T4 的任意大小紙面證明：原 mixed P₃ 的盾弧至少兩邊，
每份 unary 的盾弧至少兩邊，目錄每葉至少兩份 unary，故需要至少六條互斥框邊，
超過 C₅ 的五邊。Python 只核對固定目錄的原身份、完整 P₃ 關係及預算證書。

交付為 [checker](../scripts/c5_qcore_shield_screen.py)及
[逐 key verdicts](../artifacts/c5_qcore_shield_budget/verdicts.json)。
原 [ledger](../artifacts/c5_open_leaf_ledger/ledger.json)保持 3,497 葉開放，
本報告的獨立 verdict 尚未合併進原帳目；三份既有關閉不計為本輪新增。
沒有 commit／push、producer 重跑、大圖枚舉或既有 artifact 覆寫。

## 1. 原定義、依賴與證據層

M 是有限簡單圖；B=(b₀,…,b₄) 是指定有序 induced C₅，框圍外面，
其餘頂點私有。Σ 是全部可延拓的有序框列，只按同一個 S₄ 色名置換取軌道。
q 是被拒絕的三色 proper 框列，s=s(q) 是唯一 singleton 位置。
§2 的 W0、§3 的 W2 與 W-A 額外假設 T4⊆Σ(M)；內部連通與純拓撲引理不需此項。
T4 的 pattern 索引為 {2,5,7,8,9}，mask 第 i 位仍對應
[cells.json](../artifacts/c5_cells/cells.json) 的 `pattern_order[i]`。

此處 minimal q-obstruction 指保留 B 的 inclusion-minimal 拒絕 q 子圖；
等價使用每條非框邊 e 都讓 M−e 接受 q，忽略孤立內點。
H=M−B 是有效內部，R={v∈H:deg_M(v)≥5}；piece 是 H−R 的原連通分量，
其中每點完整 degree 恰四。Unary piece 只鄰接一個 root。
One-sided 的定義是 H−P 非空連通，不是只要求 P 自己連通。

| 證據層 | 本輪承擔的內容 |
| --- | --- |
| 紙面證明 | §2–3 的任意大小 q-core 引理與盾弧預算；§4–5 的原共鄰 P₃ 來源排除 |
| 外部定理 | 短支援／hub 論證沿用 degree-list／Gallai 刻畫；並使用 K₅ minor 不可平面的標準事實 |
| Python 有限域證書 | 120 份有標號三色列的 480 次非 singleton 改色；3,497 個 literal keys 的前提、來源 pointers、完整 P₃ tuples／fibres 及盾弧下界算術 |
| Lean 普通證明／native_decide | 本輪均無；未執行 Lean build 或 axiom audit |

依賴是[未接內點改色引理](c5_unattached_boundary.md#1-不依賴-degree-或-disk-的改色引理)、
[容量報告 §1](c5_independent_support_capacity.md#1-兩種-minimality-與來源的基本結構)、
[全 degree-4 導覽](c5_degree4_guide.md)、
[原盾弧引理及 hub 原則](c5_unary_shield_budget.md)、
[短支援兩／三 hub 證明](c5_short_support_singleton.md)與
[無 spoke 的外部 hub 補註](c5_excess_two_no_spoke_complete.md#2-無-spoke-的真實外部-hub-與共同跨度)。
外部 degree-choosability 定理的形式是：連通非 Gallai tree 對每份
|L(v)|≥deg(v) 的 lists 都可著色；拒絕的 degree lists 因而迫 Gallai 結構。
本輪閱讀核對了 [Cranston–Rabern 原論文摘要](https://arxiv.org/abs/1511.00350)的此項敘述，
不把此外部定理算作 Python 或 Lean 已證。不以四色定理作 oracle。

## 2. 改色引理與 q-core 內部連通

### 2.1 非 singleton 框點必有內鄰點

**引理 W0。** 若 induced-C₅ 圖 M 接受 T4 且拒絕 q，則
N_B(H)⊇B∖{s}。此項不需要 minimality 或 disk。

*逐行核對。* Proper 三色 C₅ 的色類大小為 2、2、1。假設 v≠s 沒有內鄰点，
則 q(v) 仍在另一框點出現。只將 v 改成 q 未用的第四色 D，所得 q′ 仍 proper，
且恰用四色，故 q′∈T4⊆Σ(M)。取它在同一 M 的一份完整延拓 f′。
保留所有其他頂點的顏色，只把 v 還原為 q(v)。因 B induced，v 的全部鄰點
就是兩個框鄰点，而 q 原本 proper，所以還原後仍是完整合法延拓，矛盾。

草稿的「q′ 的延拓沒有碰到 v，限制後就是 q 的延拓」不能字面照用：
延拓仍有 v，單純限制也尚未還原 q。正確操作是上述同圖、同完整 coloring 的還原。
此結論已在 [c5_unattached_boundary §1](c5_unattached_boundary.md#1-不依賴-degree-或-disk-的改色引理)
完整證明，並由容量報告 §1.1 直接用於 minimal q-core；不是本輪首次證得。

對 v=s，改為 D 會刪掉 singleton 的原色，仍是三色列，故不能用 T4 延拓。
Checker 保存這五份 singleton 負控制，以及全部 480 份合法非 singleton 改色。

### 2.2 非空連通與 degree 四下界

**引理 W1。** Minimal q-core 的有效 H 非空連通，且每個有效內點完整 degree≥4。

*證明。* H 空時 q 自己就是合法延拓，故 H 非空。若 H 有多個分量，且各分量
連同 B 都接受 q，可在同一字面 q 色框中拼回全部延拓，與拒絕矛盾。
故至少一分量拒絕 q。保留它並刪另一有效分量的一條非框邊，仍拒絕 q，
違反 q-minimality；inclusion-minimal 定義下也可直接刪其餘分量。
這正是[容量報告 §1.2](c5_independent_support_capacity.md#12-兩份四點支援不能由不交的內部連通圖承擔)
已記錄的 q-core 連通理由，無須 T4 或交錯支援論證。

若內點 v 的 degree≤3，刪其任一 incident 邊後有 q 延拓。保留其餘頂點的顏色，
再選未被 v 的至多三個鄰點使用的顏色補回 v，便延拓 M，矛盾。∎

H−P 的每個分量都包含與 P 相鄰的 root：H 連通，而 P 在 H 外的鄰點只能是 roots。
所以 unary 必 one-sided；若 R 非空且 M[R] 連通，所有 pieces 都 one-sided。
此即原盾弧引理 0，適用於 q-core。

## 3. q-core 版盾弧引理 1、2 與定理 A

對 one-sided P，仍按原面定義：K_P=B∪M[P]∪E(P,B)，F_P 是包含 H−P 的內面，
σ_P 是不在 ∂F_P 上的框邊集合。S_P=N_B(P) 永遠是原實際支援。
不能任選最短 gap，也不能把其他分量的支援加進 S_P。

### 3.1 引理 1 不需修改

只用 disk、P 連通與 H−P 連通，有：

1. σ_P 是連續框邊弧，可空或全 B。
2. 若 |S_P|≥2，每個支援點至少關聯一條盾弧邊；若 S_P 不包含於任何框邊的兩端點，則 |σ_P|≥2。
3. σ_P≠B 時，H−P 不能接 σ_P 的內點。
4. 不同 one-sided pieces 的盾弧邊集互斥。

*證明連續性。* 在 F_P 內連接兩條面上框邊的內點。此簡單 crosscut 分隔 disk，
P 及其附件連通且不碰 crosscut，故只在一側；另一側無 K_P 的內點，屬 F_P。
所以兩條 F_P 框邊之間至少有一整側框弧屬 F_P，其框邊集合及補集都連續。

*證明支援標記。* 若支援點 v 的兩條框邊都在 F_P，用 F_P 內的短弧和 v 的框角
圍住從 v 出發的附件。連通 P 被圍在其中，卻還有到另一框支援點的附件必須穿出，
矛盾。兩個不相鄰支援點無法同時只關聯同一條盾弧邊，得長度下界。

*證明內點限制。* 若 x∈B 接 H−P，該邊進入 F_P 的 x 角扇區。
若扇區兩側都不是框邊，兩側 P 附件及 P 中路徑圍出只在 x 碰框的閉曲線，
F_P 就不含框邊，迫 σ_P=B。否則至少一條框邊在 F_P，x 不是 proper 盾弧的內點。

*證明互斥。* 假设框邊 e 同屬 σ_P、σ_{P′}。令 Z 為 K_P∪K_{P′} 中
鄰接 e 的內面，它包含在 K_P 鄰接 e 的內面 E 中，而 E≠F_P。
P′ 的內部 realization 及其附件的非框部分都在開面 F_P；每一這樣的內點
都有避開 E 的鄰域，故不會出現在 ∂Z。對稱地也排除 P。
於是 ∂Z⊆B，Z 在連通的開 disk 中具有空相對邊界，只能是整個開 disk，
與非空內部分量矛盾。這裡只使用開面，不要求兩面的閉包不交；
原報告該句的閉包表述可能共享框點，按此修正後仍得到同一引理。∎

### 3.2 引理 2：只允許 singleton 缺點

**引理 W2。** 在 §1 的 q-core＋T4 前提下，one-sided P 若 |S_P|≥2，則

\[
S_P\subseteq V(\sigma_P)\subseteq S_P\cup\{s\}.
\]

Proper 盾弧的端點必屬 S_P；唯一可能缺少的頂點是內點 s。
σ_P=B 時，至少 B∖{s}⊆S_P。若 s 有任何內鄰点，就恢復原引理的
S_P=V(σ_P)。

*證明。* 引理 1 的支援標記給左包含及盾弧非空。Proper 盾弧的端點若不接 P，
在 K_P 的 degree 只有兩條框邊，兩邊必在同一內面，矛盾。
內點 x∉S_P 若 x≠s，W0 迫 x 接 H−P，違反引理 1 的內點限制。
若 σ_P=B，F_P 不含框邊，能碰到的框點都是 P 附件點，故
N_B(H−P)⊆S_P；再用 W0 得 B∖{s}⊆S_P。
若缺少 s，proper 情形的內點限制或全盾弧情形的附件包含亦迫 s 在整張 M 中未接 H。∎

這個例外只影響「支援等於全部盾弧頂點」。引理 1 的限制及互斥沒有 singleton 例外：
別的 piece 或 root spoke 仍不能接盾弧內的 s。
不能無條件照抄「S_P 本身連續」或 unary「至少三個實際支援點」；
兩個非相鄰支援端點夾住未接內點的 s，是此結論允許的形式，未宣稱已給出其實現。

### 3.3 定理 W-A：unary 長盾弧及共同五邊預算

1. 每份 unary U 的實際支援不包含於任何框邊的兩端點，故 |σ_U|≥2。
2. 所有 one-sided pieces 的盾弧互斥，Σ_P|σ_P|≤5。
3. 全圖至多兩份 unary。
4. 恰两份時，長度為 (2,2) 或 (2,3)，可用框點分別為旋轉後的 {b₄,b₀,b₂} 或 {b₀,b₂}；
   roots 的 spokes 與 mixed 支援都避開這兩份盾弧的內點。其他 one-sided pieces 的盾弧至多一邊。

*證明第 1 點。* 取 U 的原 contact 邊 e=rp。M−e 的 q 延拓限制到 M−U，
給合法外部染色 ψ。它不能延拓到 U，否則延拓 M；因此 root 色是原完整 unary 關係的非空禁色。
若 S_U⊆{a,b}，其中 ab 是框邊，W0 提供 h∈B∖({a,b}∪{s}) 的內鄰点。
它在 H−U，且 H−U 連通，故有同一原 M 的 r→h 路徑，內部避開 U 與 B。

在此拒絕見證中，若 ψ(r) 等於 q(a) 或 q(b)，使用兩 hubs；若都不等則使用三 hubs。
具體的未見色情形取 {a}、{b}、(B∖{a,b})∪V(L)，三者連通、互斥且兩兩相鄰；
同色情形合併同色端點與 root 所在外路，另取另一框點為 hub。
每個 hub 在 N(U) 上只見一色。Lists 由完整 degree 四給 |L(v)|≥deg_U(v)，
拒絕使每點 tight，同色外鄰不能在同點重複，故收縮不減 degree。
[hub 原則定理 B](c5_unary_shield_budget.md#4-定理-bhub-原則)
或上述短支援两／三 hub 證明給 K₅ minor，矛盾。
外路本身恢復外部 hub 的連通性，所以不另要求原 spoke。

第 2 點是引理 1；第 3 點由 2+2+2>5；第 4 點由 C₅ 上互斥連續弧的長度配置
及引理 1 內點限制。支援與弧頂點的關係用 W2，保留 singleton 缺點。∎

## 4. 任務 C 的適用前提稽核

沿用[共鄰 P₃ 報告 §1](c5_mixed_p3_common_endpoint.md#1-原-source-前提與完整三點關係)：
q=(0,1,0,1,2)，s=b₄；H 非空連通，z、w 完整 degree 五且有原邊 zw。
H−{z,w} 的唯一 mixed piece 是 C*=x₀x₁x₂，只有 x₂ 同接兩 roots；
其餘原 pieces 都是 unary，完整 degree 四。

刪任一 piece 後，zw 仍將 roots 連在一起；每個其他 piece 至少接一 root。
所以 H−P 非空連通，**所有原 pieces 都 one-sided**。停止條件不觸發。

然而原 C 報告刻意不要求 T4，它比 §1 的 W 圖類更廣。
不能把 W0／W2 無條件套到整份 ledger。逐 key 的全圖支援核對為：

| 原 P₃ 支援加完整 A_z、A_w 的聯集 | 開放 keys |
| --- | ---: |
| B 全部五點 | 2300 |
| {b₀,b₁,b₂,b₄}，缺非 singleton b₃ | 597 |
| {b₁,b₂,b₃,b₄}，缺非 singleton b₀ | 600 |

另有 **8,398 份 unary 的 actual_own_support 未知**。A_r 是整側支援，可能包含
root spokes 及多份 unary；不把它分派為每一份 unary 的 own-support。
本輪不查詢或猜測那些未知完整 relations，原 contacts、ownership、bridges、
共同色框、完整 P₃ tuples／root fibres 與所有 lifts 都保持在 SHA256 綁定的原 payload。

## 5. 批量來源排除：不需要 T4 的六邊矛盾

**紙面定理 C-W。** 若上述原共鄰 P₃ 來源每個 root 至少有一份 unary，則不存在此 disk 來源。
此定理容許任意大小 unary；不假設 T4、固定完整 Σ、原 spoke 或 unary 的具體 own-support。

*證明。* 原 degree 與 lists 給 |S₀|=3、|S₁|=2、|S₂|=1，且 S₀ 見三個不同 q 色。
因此 C* 的原支援包含至少三個不同框點，無法包含於單一框邊；
純拓撲引理 1 的支援標記直接給 |σ_C*|≥2。

對任一 unary D 及其 root r，q-critical contact 的刪邊延拓給 D 的拒絕見證，
如 §3.3。假設 S_D 包含於某框邊 {a,b}。因 |S₀|=3，可選具名
h∈S₀∖{a,b}。同一原圖中有外路

\[
L_D=r-x_2-x_1-x_0-b_h,
\]

避開 D，只有終點碰框；兩個 roots 都實際接 x₂。
依 §3.3 的短支援 hub 論證，D 不可能拒絕該 root 色，矛盾。
所以每份 unary 的盾弧至少兩邊。C*、U_z、U_w 都 one-sided 且互斥，故

\[
6\le |\sigma_{C^*}|+|\sigma_{U_z}|+|\sigma_{U_w}|\le5,
\]

矛盾。證明沒有使用 W0／W2，因而避開原 C 缺少 T4 的前提缺口。∎

有限目錄稽核確認每個開放 key 的兩側原角色都有至少一份 unary：

| Unary 總數 | 開放 keys | 加上 C* 的盾弧下界 |
| ---: | ---: | ---: |
| 2 | 1258 | 6 |
| 3 | 1679 | 8 |
| 4 | 560 | 10 |
| 合計 | **3497** | 全部超過 5 |

結果為 **新增來源排除 3,497，獨立篩選後此固定目錄剩餘 0**。
既有 C₂／C₃／C₄ 三 keys 沿用原關閉，不重算為新增。
原 140 份 rotation 正控制只實現 contracted 側幾何，並未實現 unary 的完整 degree／minimality；
它們與此來源排除並不衝突，原資料不刪除。

## 6. Checker、artifact、實際重播

Checker 只讀原 ledger、其列出的五份 SHA256 綁定來源、cells 與依賴報告。
所有來源目前存在，故未執行封存 restore；缺檔時依
[audits 還原說明](../audits/README.md)操作，不重跑 producer。

每份新 verdict 保存 literal key、stable leaf ID、原 ledger／scope JSON pointers、
完整 scope row 的 canonical JSON SHA256，以及對應的盾弧證書 ID。
證書保留原 mixed 支援、逐份 unary 名稱與 owner、one-sided 分量接合圖、
五種假設短框邊各自的原外路、每份 piece 的下界和共同五邊矛盾。
原完整 payload 另以整檔 bytes SHA256 綁定，沒有以此證書取代完整關係。

Python 會核對原 (3,2,1) 實際附件、原 root masks、共享字面 q 色框、全部 P₃ tuples、
16 個完整 root fibres／lifts、側角色、逐份 ordered contacts 與非空禁色。
其分量接合圖檢查根據原連通 piece 定義承擔的 incidence 骨架；
**它沒有讀到未知 unary 的完整內部圖，也没有有限算法證明無界拓撲或 Gallai 定理。**
兩份長盾弧下界四邊不應排除、三份才超預算的控制亦保存。

實際執行命令如下；`--write` 只用 exclusive-create 新增本任務的 verdict 檔，
已存在便拒絕覆寫，不是原 ledger 的 `--write`：

```bash
.venv/bin/python scripts/c5_qcore_shield_screen.py
.venv/bin/python scripts/c5_qcore_shield_screen.py --write
.venv/bin/python scripts/c5_qcore_shield_screen.py --check
PYTHONHASHSEED=17 .venv/bin/python scripts/c5_qcore_shield_screen.py --check
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

一般及 `PYTHONHASHSEED=17` 的 `--check` 均 exit 0，逐 byte 重播一致：
`screened_keys=3497`、`newly_source_excluded_keys=3497`、
`remaining_open_keys_under_fixed_C_premises=0`，unary 數分布為
`2:1258, 3:1679, 4:560`。Artifact 共 1,283,294 bytes，SHA256 為
`cad8ea9367a96a15be61b117b0a318cddc572bea131ffbebd6888f9c5398a25a`。

`python3 tools/docgraph check` exit 0：62 documents、213 relations、5 families、
0 errors／0 notes。`git diff --check` exit 0，無輸出。
`python3 scripts/check_docs.py` **exit 1**：542 Markdown files、5,697 local links，
僅兩項 STATUS 直接索引缺漏，分別是本任務的 `docs/c5_qcore_shield_budget.md`
及同工作區檢查時另存在的 `docs/c5_shield_calibration.md`；未報連結／錨點錯誤。
依使用者的任務分工不修改 STATUS，留待發派者整合，不能將此檢查記為通過。
新增報告前亦曾執行文件及 DocGraph 基準檢查，當時分別為
540 Markdown files／5,670 links 全通過，以及同樣的 62 documents／213 relations 全通過。

補充後的另一次實際文件檢查為 exit 1，544 Markdown files／5,714 links、6 errors：
同工作區並行新增的 `docs/c5_excess_rejection_law.md`、`docs/c5_kempe_transport.md`
亦未直接索引，且該次檢查時 transport 報告所連的
`artifacts/c5_kempe_transport/observations.json`、`P1-witness-001.json` 尚不存在。
這些是該次觀測的輸出，不改動其他任務的文件或等待它們生成產物來掩蓋本輪結果。
另行只讀核對確認原 ledger SHA256 未變、3,497 verdict keys 互異，全部引用可解析至
28 份共用盾弧證書；完整 scope rows 的各自 SHA256 仍逐 key 保存。

## 7. 完成邊界與保留缺口

紙面 W 的正確移植和原 C 目錄排除已完成；有限重播只核對具名域與紙面前提的對應。
未宣稱任意有限域「沒反例」就是一般定理，也未把必要 rotation／role 控制當成 disk 實現。
本輪沒有新 Lean theorem，未重跑舊大枚舉、hub wiring 枚舉或歷史證書。

其他 mixed 接線、更大或多 mixed、沒有至少兩份 unary 的來源、roots 不連通而非 one-sided
的 pieces、一般 weak-deletion 單側／共同出口、逐染色 repair 及 `K∞=K≤5` 均不由本輪推出。
原 ledger 的合併、導覽／STATUS／README／HANDOFF 索引更新與後續任務由發派者處理。

## 8. 稽核後更正與補證（2026-10-04，D₆ 之後）

依 [D₆ 稽核 §4](../audits/2026-10-04-task-d6/REPORT.md#4-整合者應寫回的更正) 寫回；正文 §1–7 保留原輪語境。

**零-unary 側排除（完備性短證，D₆ §2.5）。** 原拒絕使 E_z、E_w 屬 C §1 的五型。
若某 root 側沒有 unary，degree 五扣去 zw、rx₂ 後恰有三條 spokes；兩條同色時刪其一不改任何限制，
違反 q-criticality，所以三色互異，該側 E={3}。此時另一側必為 T={a,3}；刪它的 a 色 spoke 只新增 root 色 a，
新增對 (a,a) 撞 zw、(a,3) 撞 F*，其餘配對本已拒絕，故仍拒絕 q，再違反 criticality。
因此兩 roots 各至少一份 unary，定理 C-W 涵蓋 **C §1 的整個共鄰端點 P₃ 來源分支**，不只固定目錄。
範圍仍限指定原 degree、唯一 mixed P₃ 與共鄰端點 masks；其他 P₃ 接線、多 mixed 與一般出口不由此推出。

**外部依賴的精確版本。** 拒絕 degree lists 用 Dvořák〈List coloring and Gallai trees〉
Lemma 7、Corollary 8、Theorem 10 的 Gallai tree 與 blockwise-uniform 刻畫。
K₄ block 的排除不能只引用較窄的[連通外框 K₄ 引理](c5_degree5_tree_components.md#1-連通外框排除-degree-4-分量的-k4)：
D₆ §2.2 補出四點各有互斥 tether 到連通外 hub 聯集的論證，再得 K₅。

**收費對象。** 六邊矛盾需要**三個不同**原 one-sided pieces，且依賴 q-criticality（拒絕見證）與完整 degree 四；
不帶這些前提的「任何平面 disk 中一份長支援分量加兩份 unary 不可能」是錯的，D₆ §2.7 保存兩個 disk 反例。

**交付修補。** 原 verdict 綁定 `docs/c5_unary_shield_budget.md` 引理 1(d) 更正前的 bytes，
更正後 `--check` 失敗。原檔（SHA `cad8ea93…a25a`，D₆ 稽核對象）逐 byte 保存在 D₆ 快照
`audits/2026-10-04-task-d6/snapshot/artifacts/c5_qcore_shield_budget/verdicts.json`，
隨稽核封存，新 checkout 依[還原說明](../audits/README.md)還原。以 `--write` 生成修訂版
[verdicts.json](../artifacts/c5_qcore_shield_budget/verdicts.json)（SHA `e84a6b7d…c89d`），
與原版逐欄比較唯一差異為 `/sources/docs/c5_unary_shield_budget.md` 的 `bytes`、`sha256`；
keys、IDs、28 certificates、3,497 verdicts 全同。一般與 `PYTHONHASHSEED=17` 的 `--check` 均 exit 0。
§6 記錄的原輪成功重播保留為歷史。

**ledger 尚未合併。** 依 [D₆ 合併計畫](../audits/2026-10-04-task-d6/scope_history/MERGE_PLAN.md)，
需把重算器的 `STAGES` 改為具名規格、新增 batch 抽取與 `--dry-run`，並輸出到新版本目錄以免與 W 的 predecessor 輸入形成循環依賴。
