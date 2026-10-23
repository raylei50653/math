---
docgraph:
  id: c5.equivalent-formulations
  family: [c5, c5.minimal-source, c5.no4ct]
  related: [c5.no4ct-handoff, c5.c4-boundary-pivot]
  verified_by:
    - scripts/c5_equivalent_forms_check.py
---

# 三支共同目標的等價表述：四列延拓、偶補匹配與 4-candidate

2026-10-23；基準 `78375cc`。本頁整理三支 932／933／941 共同目標的幾種等價改寫，
以及它們與 Dvořák–Lidický（D–L）、Dvořák–Lidický–Mohar（DLM）猜想的強弱關係。
四列延拓 (E) 與偶補匹配 (M) 兩個表述由使用者於同日提出並核對；本頁補上
有限核對、4-candidate 一側的 R5 分解與證據界線。

**狀態：各改寫之間的等價是紙面證明加有限核對；改寫所表達的普遍排除仍 OPEN。**
本頁沒有新增來源排除、沒有新 Lean theorem，也不改變 `K≤22=K≤5`、共同 `k≥23`。

## 1. 記號與三支

固定有序外框 `B=(b0,…,b4)`。`N_β(G)` 是固定字面邊界列 β 的完整四色延伸數；
`x_uv` 是唯一重複色在 `b_u,b_v` 的四色邊界延伸數，`y_i` 是 singleton 在 `b_i`
的三色邊界延伸數，`P(G)={i:y_i>0}`。「三色」只描述邊界，內部可用第四色。
計數定義與恆等式見 [adjacent-singleton 計數 §2](c5_adjacent_singleton_counts.md)。

| 分支 | 四色邊界型 | 可延伸三色型 | P(G) |
| --- | --- | --- | --- |
| 932 | 全部 | 無 | ∅ |
| 933 | 全部 | `01012` | {4} |
| 941 | 全部 | `01012`、`01201` | {2,4} |

共同障礙：T4 全收，但可行的 singleton 位置落在 C₅ 的一個獨立集內。
三支分類只對 [no4ct 全域最小來源](tasks/c5_no4ct_handoff.md#2-接手必須保留的精確契約)成立。

## 2. 四列延拓命題 (E)

四列證書是

\[
N_{01232}(G)>0,\qquad N_{01021}(G)=N_{01202}(G)=N_{01212}(G)=0,
\tag{1}
\]

即 `x24>0` 且 `y0=y1=y3=0`。任意有限 C₅ disk 的恆等式
`x_uv = m + Σ_{i∉{u,v}} y_i` 給 `m=x24>0`；令 `a=y2`、`b=y4`，

\[
(x_{02},x_{03},x_{13},x_{14},x_{24})=(m+b,\ m+a+b,\ m+a+b,\ m+a,\ m).
\]

五項全正，只剩 a、b 是否為零，得固定標號 mask 932（a=b=0）、933（b>0）、
940（a>0）、941（a,b>0）；940 是 933 的整圖反射像。故對**實際 disk**：

\[
\text{(1)}\iff\Sigma(G)\in\{932,933,940,941\}.
\tag{2}
\]

不需最小性。原 [四列證書](../audits/2026-10-18-abstraction-bottleneck-9f1fe84/REPORT.md#2-優先抽象目錄外的四列證書)
對抽象十位向量容許 64 個 masks；加入恆等式後只剩這四個。共同主命題寫成：

\[
N_{01232}(G)>0\ \Longrightarrow\ N_{01021}(G)+N_{01202}(G)+N_{01212}(G)>0.
\tag{E}
\]

**(E) 對全部具名 disk 成立 ⇔ `K∞=K≤5`。** 若主命題成立，K132 沒有任何 key
在任一 D₅ 位置違反 (E)（§7 核對）。若主命題不成立，全域最小來源經整圖 D₅
對齊後落入 932／933／941，三者都違反 (E)。後一方向使用 no4ct 歸約鏈，
不使用 4CT；歸約鏈的信任界線見 [no4ct 交接 §3](tasks/c5_no4ct_handoff.md#3-已完成的證明鏈與不能省略的步驟)。

## 3. 相鄰 singleton 形式 (AS)

整圖搬運後，(E) 等價於

\[
T_4\subseteq\Sigma(G)\Longrightarrow P(G)\text{ 不是 }C_5\text{ 的獨立集}
\iff
\Bigl(\min_{uv}x_{uv}>0\Rightarrow\sum_{i}y_iy_{i+1}>0\Bigr).
\tag{AS}
\]

(E) 失敗時五個 x 全正且 `P⊆{2,4}`；反之 C₅ 的每個獨立集都含在某條對角線
兩端內，搬到 {2,4} 即得 (E) 的反例。相鄰兩位置可來自兩份不同完整著色。
這就是 [Kempe screen §4](c5_kempe_screen.md#4-c5-adjacent-singleton-problemunproved) 的候選引理，含 P=∅。

外加一個連五框點的 hub v 時，邊界必須三色才能延伸到 v：932 封上後不可四色，
933／941 封上後鄰圈 singleton 只能在 {4}／{2,4}。`不存在 Σ=932 的 disk ⇔ 4CT`
已在 [no4ct 交接 §4](tasks/c5_no4ct_handoff.md#4-精確停止點與未完成項目)；
933／941 的一般排除**不**因此稱為與 4CT 等價。

## 4. 五端點偶補匹配形式 (M)

設 G 是內面皆三角形的 C₅ disk。取平面對偶並把外面頂點拆成五個端點，得網路 Q：
內點（G 的內面）皆三度；端邊 `e_i` 對應框邊 `b_i b_{i+1}`。四色取為 `F₂²`，
邊色 `q_i=β_i⊕β_{i+1}`；固定 b0 後積分唯一，固定邊界列的延伸數不乘 4 或 24
（D–L Observation 3）。S₄ 恰為 `AGL(2,2)`，色名置換只令三種邊色互換，
singleton 邊位置不變。

| 邊界列 | 端邊色字 | 只出現一次的端邊 |
| --- | --- | --- |
| 01232 | 13112 | {1,4} |
| 01021 | 11231 | {2,3} |
| 01202 | 13222 | {0,1} |
| 01212 | 13332 | {0,4} |

令 `𝓜_ij(Q)` 為匹配 M：每個內點恰一條 M 邊；五條端邊中恰 `e_i,e_j` 不在 M；
`Q−M` 的每個閉環為偶環。內點數 `2k+3` 為奇數，M 覆蓋內點及三個端點，
故閉環皆偶時，連 `e_i,e_j` 的開路邊數為偶，可交替填另兩色且兩端異色。
每個偶環有兩種交替方向，開路方向由固定端色決定，因此

\[
N_\beta(G)=\sum_{M\in\mathcal M_{ij}(Q)}2^{c(M)}=:W_{ij},
\qquad
N_\beta(G)>0\iff\mathcal M_{ij}(Q)\neq\varnothing,
\]

c(M) 為閉環數。於是 (E) 改寫為

\[
\mathcal M_{14}(Q)\neq\varnothing\ \Longrightarrow\
\mathcal M_{23}(Q)\cup\mathcal M_{01}(Q)\cup\mathcal M_{04}(Q)\neq\varnothing.
\tag{M}
\]

量化範圍是由合法 C₅ 近三角 disk 得到的具名網路。全域最小來源已可取成
[近三角正規形](c5_cofacial_normal_form.md)，所以對此範圍證 (M) 已足以處理主命題。
「暴露兩個端點」不能換成普通全圖完美匹配；閉環偶性是整份補圖條件。

**強弱界線。** 加權版本 `W14 ≤ W23+W01+W04` 由 `x24=m+y0+y1+y3` 恰為 `m≤0`，
即 [D–L Conjecture 9](c5_count_cone_bridge.md#1-文獻錨點與精確翻譯)，比 (M) 強。
匹配路線只需某一份目標匹配存在，不要求來源匹配有保權單射；
也不要求「任意起點經 Kempe 交換可達」，後者另背可達性障礙。

## 5. 與文獻猜想的強弱關係

DLM（arXiv:2504.08327v2，[保存原文](../audits/2026-10-13-singleton-literature-6cafdfb/sources/one-crossing-2504.08327v2.txt)）
Corollary 12：Conjecture 2（無分隔三角形、單交叉、其餘點度≥5 的圖可四色）
⇔ 對所有 n 的 D(n)（至多 n 點、內面皆三角形、三角形皆為面的 diagonal-forbidding
平面圖必有度≤4 內點）⇔ 對所有 n 的 R(n)（rainbow 版本）。D–L Conjecture 9 即 m≤0。

**反向構造。** 4-candidate H 的外框 `(x1,…,x4)`，禁止 x1-對角型。若非對角外框點 u
有 deg(u)=4，則 `G=H−u` 是 C₅ disk，u 的兩個內鄰點成 b0、b1；依
[C5→C4 表](c5_c4_boundary_pivot.md#1-只改外框的完整來源橋) ABCB 計數為 `y0+y1`。
內點度不變（≥5），b0、b1 度≥4；弦 b0b2、b1b4、b2b4 會與 u 成非面三角形，不出現。
令 **D₄** 為 D(n) 限於「有非對角外框點度為 4」的子類，則

\[
D_4\iff\Delta:\ \text{沒有滿足上述度數與面條件、且 }y_0=y_1=0\text{ 的 C₅ disk}.
\]

既有來源橋產生的 H 正落在此子類，故 Δ ⇒ E。反方向卡在 K132 本身：
**45 個 key、8 個 D₅ 軌道**拒絕某對相鄰 singleton（代表 165、167、199、231、429、
431、935、943），目錄代表都含度 4 內點或框弦。令

> **R5**：這 8 個軌道都不能由滿足 Δ 度數與面條件的 C₅ disk 實現。

則 **Δ ⇔ E ∧ R5**。(E) 只描述可實現的 Σ 集合，而這 8 軌道本已可實現；
「能否以內度≥5 的圖實現」不是 Σ 可見的資訊，外接環帶亦不能把它們送出 K132，
故任何只用 Σ 的論證都不能由 (E) 推出 R5。

\[
\text{DLM Conj 2}\iff\forall n\,D(n)\Rightarrow D_4\iff E\wedge R5\Rightarrow E\iff K_\infty=K_{\le5}\Rightarrow\text{4CT};
\qquad
\text{D–L Conj 9}\Rightarrow E.
\]

DLM 的 ≤28 點完整計算同時涵蓋 E 與 R5，均只到 k≤22。D(n) 依 u 的度數 d 分層，
對應 C_{d+1} 邊界問題：d=3 為 C4、d=4 為本題、d≥5 在本 repo 範圍外。

**未驗證的強化假設 U。** [no4ct 交接 §3 第5步](tasks/c5_no4ct_handoff.md#3-已完成的證明鏈與不能省略的步驟)
記錄 19／20／21 點最小度五球面三角剖分刪任一五度點後 Σ 皆為 1023。若
「內點度≥5、框點度≥4 的 C₅ 近三角化必有 Σ=1023」成立，即推出 (E)。
此假設只有上述三個點數的證據，未另行核對。

## 6. 接續目前分支的精確局部接口

以下是既有報告中的等價式，按 (E)／(S) 的語言重寫；範圍仍是原報告的完整契約。

**932，h=4。** [第五輪 §4](../audits/2026-10-23-three-mask-round5-cb8f859/932/paper/PROOF.md)
對固定 literal Q word σ 定 `P_i(σ)={0,1,2,3}∖σ(L_i)`，L_i 為原 c_i 在 Q 上的全部鄰點路。
L_i 至少兩個相鄰點，故 `|P_i|≤2`；σ 能穿過原環帶 ⇔ C₉ 有 `a_i∈P_i(σ)` 的列表染色。
可問：同一實際內側 J 能產生哪些九列表組合？環帶無解的 σ 仍須保留於必要拉回。

**933，兩星。** [第三輪](../audits/2026-10-23-three-mask-round3-cb8f859/933/REPORT.md)證兩張
k−2 候選 T0、T1 通過四列證書皆 ⇔ `U=V=0`；
[第四輪 (5)](../audits/2026-10-23-three-mask-round4-cb8f859/933/PROOF.md)給
`U=A1+A2+CU1+CU2`、`V=A1+A2+CV1+CV2`，六項皆同一原 D 的非負完整 fibre 計數，
故**指定兩候選成功 ⇔ 六個 fibre 全空**。全域最小性迫 U+V>0；此 iff 不表示
所有 933 證明都須經六 fibre 全空。

**941，K8。** 固定同一原外側 E、密封 K8 補片 P 與完整八接點 I；
[第七輪 §4](../audits/2026-10-23-941-types-wrong-side-round7-6b09cd4/PROOF.md)的八接點及七個內點
都是原 C₅ 內點，故補片關係與框列無關。令 `A_q` 為同一 E 在框列 q 下可實現的
完整接點 tuples，`A=A_{01232}`、`L=A_{01021}∪A_{01202}∪A_{01212}`。
對合法、完成後嚴格變小的候選 Q（加弦／識別後的商圖，原外側無識別端點間的邊）：

\[
E\cup_I Q\text{ 通過四列證書}\iff A\cap R_Q\neq\varnothing\ \wedge\ L\cap R_Q=\varnothing.
\tag{S}
\]

既有 72 份安全候選用 `R_Q⊆R_P`，是 (S) 的充分條件；(S) 容許 Q 接受 P 不接受的
tuples，只要新增部分避開 L，接受 witness 也不必是原先那一份。
新問題：若每個能接住 A 的候選都碰到 L，同一平面外側 E 能否同時供應全部這些阻斷 tuples？

## 7. 證據與重播

```bash
python3 scripts/c5_equivalent_forms_check.py
```

| 項目 | 結果 | 證據層 |
| --- | --- | --- |
| (2) 的 mask 集合 | 恆等式加四列只得 932／933／940／941；940 為 933 的 D₅ 像 | 紙面＋窮舉 |
| (E) 對 K132 | 64 個抽象四列 masks 全在 K132 外；132 keys 在 10 個 D₅ 位置皆不違反 (E) | 窮舉 |
| 相鄰拒絕 keys | 45 keys、8 軌道 | 窮舉 `cells.json` |
| 端邊色字 | 四列色字及 singleton 端邊與 §4 表一致 | 窮舉 |
| `N_β=Σ2^{c(M)}` | 60 張隨機近三角化（內點 1–8，seed 17）×10 列全等，312 列為正 | 隨機控制 |

負控制：拿掉閉環偶性檢查，或把權重 `2^{c(M)}` 改成 1，隨機控制均失敗。
匹配公式本身是標準對偶的紙面論證；隨機控制不是證明。
DLM／D–L 陳述引自 repo 保存的原文文字，未重播其計算。
R5、Δ 與 U 均未證；§6 三個局部 iff 沿用原報告證書，本頁未重跑其 checker。
