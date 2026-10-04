# B₄：933 原 04／12 的 shared-contact 附件 {4}

**獨立驗收（2026-10-04，D₅）**：[最終成果固定快照與稽核](../audits/2026-10-04-task-d5/REPORT.md)
只接受W933-129／04–12／長face{2,3,4}的指定shared原附件{4}支：
六shared身份／八選擇、11tight pairs、連通K=C−v與完整degree握手式，
五袋非空／互斥／連通及十對原邊均獨立核對。整份W933-129、整個長face、
其他附件及原20／20表保留；B₂／B₃的兩primary閉合仍依前輪證據。
以下正文／前綴保持各輪截點，現行具名入口由Kempe導覽維護。

2026-10-04。接續 [B 的原身份與 tightness](c5_excess_two_mixed_core_four_spoke_mixed22.md)
及 [B₃ 的不同長 face](c5_excess_two_mixed_core_four_spoke_mixed22_long_face.md)。
先從原 B artifact 鎖定 **W933-129、a=5、b=6、spokes 04／12、原長
face 2–b–a–4–3–2**，再完成指定 shared contact 實際附件為 {4} 的
任意大小來源排除。六種有 shared 的身份、八種指定原頂點選擇均無
此附件支殘留；**沒有排除 W933-129 整個骨架或整個長 face**。
其他附件、身份與骨架保留；目前停止點見 [Kempe 導覽](c5_kempe_guide.md)。
實際驗證及貼用摘要見 [B₄ 紀錄](history/2026-10-04-excess-two-four-spoke-mixed22-shared4.md)。

本支容許真正的原 C-leaf，不能沿用 B₃ 的 min deg_C≥2 分類。
主要證據是原 degree 握手式與十對原邊給出的任意大小 K₅ minor；
跨列 list slack 另用 connected-slack 引理與固定 Python 算術核對。
沒有新增 Lean theorem，`lake build` 不形式化本頁論證。
共同 ε≥2 不變；mixed22 整型、ε≥3、來源實現、一般出口及 K∞=K≤5 未證。

## 1. 原 artifact、精確 frame 及指定 shared 身份

沿用 B 的全部前提：G 有限簡單，B=(b₀,…,b₄) 是指定有序
induced-C₅ disk 外框；完整 Σ(G)=933，每條非框邊 Σ-critical。
有效 H 連通、ε=2，原相鄰 roots a,b 完整 degrees=(5,5)，其餘
有效內點完整 degree 四。H−{a,b} 恰為唯一原連通 C，沒有 unary。
原 ab、四 spokes ab₀、ab₄、bb₁、bb₂，以及原 contacts
ax₀、ax₁、by₀、by₁ 全部保持；x₀≠x₁、y₀≠y₁。
B 已證四原 spoke 省略各自 Ω，每個原拒絕 q-core 均是 G (5,5)。
下文不把 Σ-minimality 或這份 q-core 結論換成 pinned pair 的逐邊 minimality。

[原 B observations](../artifacts/c5_excess_two_mixed_core_four_spoke_mixed22/observations.json)
中 source_sigma=933、original_spoke_supports=[[0,4],[1,2]] 的
inherited_named_skeleton_index 是 **129**。原長 face 的 literal 圈
為 [2,6,5,4,3]，envelope={2,3,4}；另一 mixed-capable 短 face 為
[0,5,6,1]。原兩份 disk rotations 及 mirror 外框次序完整保存，
不以 B₃ 的 W933-101 或其 {0,4,3} 長 face 代換。

指定原 v 是某 xᵢ=yⱼ，且 **N_B(v)={b₄}**。

| 原身份 | 指定 shared 原頂點選擇 |
| --- | --- |
| D4 | 無 shared，這個附件支不適用；身份保留 |
| S00、S01、S10、S11 | 各自唯一原 shared 頂點 |
| Pstraight | x₀=y₀ 或 x₁=y₁，各自條件式排除 |
| Pcross | x₀=y₁ 或 x₁=y₀，各自條件式排除 |

一份原圖若有兩個 shared 點，只需其中任一個有此實際附件便適用。
共享角色始終是同一原頂點，不複製，不把原 bridge 或旁支刪成模型。

同一字面四色框 β 下保留完整 R_C(β) 的有序
(X₀,X₁,Y₀,Y₁) tuples 與整份 C witnesses，及完整 joint

\[
J_G(β)=\{(A,D,X_0,X_1,Y_0,Y_1): (X_0,X_1,Y_0,Y_1)\in R_C(β),\
A\ne D,\quad A\notin β(\{0,4\})\cup\{X_0,X_1\},\quad
D\notin β(\{1,2\})\cup\{Y_0,Y_1\}\}.
\]

全部 16 個 pinned (A,D) 四接點 fibres，包括空 fibre，連同 actual
attachments、ownership、原 C 內邊、bridges、環序與 witnesses 保持。
後面的 minor 只供原圖非平面反證，不宣稱保存 relation、fibres 或 Σ。

## 2. 真正 tight 的 shared leaf 與跨拒絕列 bridge slack

原 v 的全部外鄰恰為 a,b,b₄，完整 degree 四迫 deg_C(v)=1。
令 vt 是唯一原 C 邊；它確為 bridge。K=C−v 非空且連通，
其餘原 C 邊／bridges／旁支全部留在 K。

933 原拒絕 rows 為 1、3、4、6。原 G−C 的每一合法 pair 均被
完整 C 拒絕；exact lists 是

\[
L_{q,A,D}(w)=U_4\setminus\bigl(q(N_B(w))\cup
\{A:a\in N_G(w)\}\cup\{D:b\in N_G(w)\}\bigr).
\]

完整 degree 四給 |L(w)|≥deg_C(w)，connected-slack 迫同圖每點
tight。指定 v 的全部 11 個合法 pairs **都確有 singleton list**：

| 原拒絕 row | 全部 literal (A,D) | 對應 L(v) |
| --- | --- | --- |
| 1：01021 | (2,3)、(3,2) | {0}、{0} |
| 3：01201 | (2,0)、(2,3)、(3,0) | {3}、{0}、{2} |
| 4：01202 | (1,0)、(1,3)、(3,0) | {3}、{0}、{1} |
| 6：01212 | (1,0)、(1,3)、(3,0) | {3}、{0}、{1} |

所以 v 自己沒有 B₃ 的 strict slack。固定其 singleton 色 c 後，
K 的 exact lists 只在原鄰點 t 刪除 c；deg_K(t)=deg_C(t)−1。
若 c∉L(t)，此點有一份 strict slack，連通 K 可染，接回 v=c 便
延拓原拒絕列，矛盾。這項必要性須對同一實際 t 跨全部 rows/pairs 求交。

| 原 t owner | 原 B tightness 容許附件 | leaf 刪除 slack 排除 | 此層尚保留 |
| --- | --- | --- | --- |
| none | ∅、2、3、4、23、34 | 2、3、23、34 | ∅、4 |
| a-only | ∅、4 | 無 | ∅、4 |
| b-only | ∅、2、4 | 2 | ∅、4 |
| shared a,b | ∅、4 | 無 | ∅、4 |

這是 13 份實際附件候選、143 份同框 row/pair 檢查，排五份、留八份。
例如 t 接 2 時 row1/(2,3) 的 c=0 已被 q₂ 禁止；t 接 3 時
row3/(2,3) 的 c=0 已被 q₃ 禁止。各失敗候選均保存完整 exact list
與原 pair；保留候選亦保存全部 11 份 lists，沒有把它們稱為來源。
不同身份可能另限制 t 的 owner；這份表只是所有身份的必要候選上界。
若 K 是 singleton，deg_K(t)=0 的同樣 slack 算術仍適用。

connected-slack 只用 [Dvořák Lemma 7](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
的連通 degree-assignment 結論，亦可直接按生成樹逆序貪婪證明。
主要來源排除不依賴 Gallai terminal-block 定理或此表的完備性。

## 3. 原 cut 的奇數附件與五個原 K₅ bags

v 耗用一條 a-contact 與一條 b-contact。令另一原 contacts 為 x*、y*；
它們都在 K。Sij 時兩點可能不同；雙 shared 時 x*=y* 仍有
**兩條不同原邊 ax*、by***。不得把它們算成一條外部 incidence。

K 的原 cut 邊恰為 ax*、by*、vt，加上所有實際 K–B 附件。
令 n_B=|E_G(K,B)|。每個 K 點的原完整 degree 仍是四，故

\[
\boxed{4|V(K)|=2|E_G(K)|+3+n_B.}
\]

因此 n_B 是奇數且至少一，必有某條實際原 zw、z∈K、w∈B。
這是同一原圖的完整 degree 等式，沒有補邊、收縮、虛設支援或使用跨列邊數。

五個原 bags 是

\[
\boxed{\{a\},\ \{b\},\ \{v\},\ V(B),\ V(K).}
\]

它們互斥、非空且連通；B 是原五環，K 是原 leaf 刪除後的完整
連通部分。十對鄰接均有原邊：

| bags pair | 原鄰接見證 |
| --- | --- |
| a–b、a–v、b–v | ab、av、bv |
| a–B、b–B、v–B | 任一原 a-spoke、任一原 b-spoke、vb₄ |
| K–a、K–b、K–v | ax*、by*、vt |
| K–B | 握手式迫存在的實際框附件 zw |

原 B bag 可用路徑 4–3–2–1–0 明示連通。K 中從 t 到 x*、y*、z
的實際路徑由原連通性給出，保持 shared 頂點、全部內部 bridges 與
旁支；固定控制逐份保存這些原路徑及十條原鄰接。
因此原 G 含 K₅ minor，違反 disk 平面性。

此任意大小證明涵蓋 C 只有兩個 shared 點的原 edge：此時 K 只有
另一點，n_B=1，五 bags 與十條邊仍成立。也涵蓋任意長 bridges、
任意 blocks 與旁支，無須分類 terminal leaves 或假設 min deg_C≥2。
**指定 shared-{4} 窄支全部來源排除，八種指定選擇零殘留。**

### 原長 face 的獨立幾何交叉核對

在兩份原 rotations 中插入同一實際 av、bv、b₄v，原長 face 分成
三角 abv、三角 ab₄v，以及五圈 b–2–3–4–v–b。
K 連通並接 a,b,v，故只能位於 abv 三角 face；其框附件數必為零，
與原 cut 的奇數式矛盾。Checker 核對 108 份保持原環序的插入，
每份原 rotation 恰一份指定長-face extension。
這項封閉位置是另一路交叉核對；主證明的原 K₅ 不需先用 face sealing。

## 4. 獨立證書、重播與精確停止點

[Checker](../scripts/c5_excess_two_mixed_core_four_spoke_mixed22_shared4.py)、
[literal controls](../scripts/c5_excess_two_four_spoke_mixed22_shared4_controls.py)、
[B₄ observations](../artifacts/c5_excess_two_mixed_core_four_spoke_mixed22_shared4/observations.json)
構成新層；SHA256 綁定原 B／B₃ bytes，原 artifacts 不覆寫。
保留 W933-129 整份原 frame、兩 rotations、兩 faces、七種身份，
單列指定 shared-{4} 附件支的六身份／八選擇結論。

固定完整 degree 圖包含真正的 shared terminal bridge、雙 shared 的
兩點 C、cycle 接 bridge 與較長 cycle；每份同一原圖保留全部十列
R_C、G／四個 G−spoke／G−C 六種 joints、16 fibres（含空）與
完整 witnesses，直接由原邊獨立重算。Root swaps 只作 literal 控制，
不登記其他具名骨架排除；global S₄ 同時搬運整個原色框。
固定圖給原 K₅ 連通袋與 actual paths 的正控制，**不宣稱 disk、
Σ=933、criticality 或來源實現**。任意大小結論由 §3 的紙面證明承擔。

```bash
python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22_shared4.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22_shared4.py --check
python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22.py --check
python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22_long_face.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

無參數只生成 B₄ observations；`--check` 重算逐 byte 比對。
實際數字、驗證及未重跑範圍見本輪紀錄。
**在此 shared-contact 窄支停止。** W933-129 的 D4、shared 空附件、
其他 contact 附件、原短 face 與其他骨架均不新增排除。
原 B 必要 20／20 表及 B₃ 固定兩 W 的歷史結論保持；沒有刪完整
必要列、沒有證成 mixed22 整型或 ε≥3，未 commit／push。
