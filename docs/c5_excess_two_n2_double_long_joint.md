---
docgraph:
  id: c5.excess-two-n2-double-long-joint
  family: [c5, c5.excess-two, c5.n2]
  requires:
    - c5.excess-two-n2-diagonal-three-row
  derives_from:
    - c5.excess-two-n2-residual-unification
    - c5.excess-two-n2-long-synchrony
    - c5.excess-two-n2-partition-rule
---
# N2 原55雙 long：共同容量接回與九格接口子命題

**後續（2026-10-13，BASE 243a125）**：[N2-BRIDGE](c5_excess_two_n2_bridge.md)
另排932，完成原E4完整三列來源契約的N2；E-ARC2仍OPEN，未新增Lean證明。
以下各輪證明與停止點保留當時語境。

**後續（2026-10-13，BASE 3097ef5）**：[同來源 LL-CUT+diag](c5_excess_two_n2_ll_cut.md)
以原 leaf K₅／K₃,₃、接線數及最後行容量cut排除全部剩餘t=2／3來源，
完成本頁完整原55 `(2,0)` 契約的來源排除。基本LL-CUT機制未獨立證成，
19,229份抽象共同可行profiles保留；LL-CUT當輪未涵蓋的原E4三列N2，
後由上述N2-BRIDGE排除。E-ARC2仍OPEN；以下保留原輪證據與停止點。

2026-10-13。基準 HEAD `19209f4cf68261fdce5e84a7804cfe04ae0957bf`；
十三份原輸入與 SHA 見 [BASE](../audits/2026-10-13-n2-double-long-joint/BASE.json)。
接續 [residual](c5_excess_two_n2_residual_unification.md)、
[long synchrony](c5_excess_two_n2_long_synchrony.md)及
[完整接口分割](c5_excess_two_n2_partition_rule.md)。
目前停止點見 [Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口)。
本頁已納入[2026-10-13整理發布](history/2026-10-13-progress-publish.md)；
文末「本輪不commit／push」保留原独立研究交付語境，後續狀態以發布紀錄及Git為準。

**完整原55 `(ℓ,u)=(2,0)` 的零／一條 root-spoke 子域已排除，不限制 long 的大小。**
這裏 `t=t_r+t_s` 是兩 roots 接原框的 spokes 總數，不是 long 數或接點數。
同列碰色與容量給一般共同接回引理；原 leaf block 與 K₅ 進一步排 `t=0、1`。
剩餘支援大小 `{3,3}`、`t=2或3`，以及 `{3,4}`、`t=2`。
其完整共同 joint 尚未證成；本輪交付明確可反駁的 **LL-CUT** 子命題，
每列至多九個 binary cells、512 份分配，與原 pieces 大小無關。

這是任意大小紙面證明＋独立審查，沿用既有 degree-list／Gallai 與容量輸入；
有限完整 fibres 僅作校準。完整 target `not triggered`，沒有新 Lean theorem。
完整 `(2,0)`／N2／E-ARC2 仍 **OPEN**。

## 1. 完整來源與同一原 H 的接回

沿用 [原契約](c5_excess_two_n2_diagonal_three_row.md#1-完整來源契約)：
有限簡單 induced-C₅ disk、有序原 B、完整 Σ933／941 或整圖共同 D₅ 像、
T4 全收、每條非框邊 Σ-critical、ε=2、連通且 full-B-touch 的有效 H；
恰兩個非相鄰完整 degree5 roots r,s，其餘有效內點完整 degree4。
本題 `H−{r,s}` 恰為兩份原 long mixed P,Q，沒有 U，H 二連通，pieces one-sided。
全部原 ordered/shared contacts、ownership、actual attachments、rotation、bridges、
旁支、具名色框、完整 relations、空 fibres、full lifts 及自由座標因子保留。

固定 `I={0,1,3}`、`q₀=01212`、`q₁=01202`、`q₃=01021`、`D=3`。
記 `k_C^v` 為 C 到原 root v 的 incidences，`T_v=N_B(v)`，
`E_v(i)=[4]∖q_i(T_v)`。原 root-spokes 至多相鄰兩條，因此

\[
|E_r|=4-t_r=k_P^r+k_Q^r-1,\qquad
|E_s|=4-t_s=k_P^s+k_Q^s-1.
\]

`F_C(i;x,y)` 是原 C 的全部完整 tuples，`A_C(i)` 是其非空 cells。
唯一完整接回條件仍為

\[
J_i=(E_r(i)\times E_s(i))\cap A_P(i)\cap A_Q(i)\ne\varnothing.
\]

在同一 `i,x,y` 選兩份完整 tuples，按原頂點順序與 B,r,s 合併，恰覆蓋全部原邊。
所有下述非空結論都按這個公式接回，不合併不同列或不同來源的 witnesses。

## 2. 任意大小的碰色與容量同步

定義實際接點附件集合

\[
W_C^v=\{h\in B:\exists w\in C, vw,wh\in E(G)\},\qquad
X_C^v(i)=q_i(W_C^v)\cap E_v(i).
\]

**共同碰色引理。** 若 `X_P^r(i)` 與 `X_Q^s(i)` 都非空，或交換 P,Q 後成立，
則 `J_i≠∅`。取兩個 root pins 分別等於對應原框附件色，每份 C 都有一個
外鄰重色的原點；strict degree-list slack 給兩份同列同 pins 的完整 lifts。

**碰色加容量引理。** 若 `X_C^v(i)≠∅` 且另一 root 的 `k_C≥2`，亦有 `J_i≠∅`。
例如固定 `x∈X_P^r(i)`，P 對所有 s pins 都可染；Q 至多拒絕 `k_Q^s` 個 s 色，
但 `|E_s|=k_P^s+k_Q^s−1>k_Q^s`，故有一個共同可接受的 y。
所用逐欄上界是既有 B-C2 對**完整 fibres**的個別分量上界。

所以三列共同拒絕會迫

\[
k_C^{\mathrm{other}}\ge2\Longrightarrow W_C^v\subseteq Z(T_v),\qquad
Z(T)=\{h:q_i(h)\in q_i(T)\text{ 對全部 }i\in I\}.
\]

空 spoke 集的 Z 為空；單點的 Z 為該點。相鄰 pairs 中只有
`Z(12)=124`、`Z(40)=024` 擴大，其餘 Z 都等於原 pair。
這是同一字面框的三列 signature 計算，不能逐 piece 旋轉使用。
完整量詞與證明見 [paper §§1–2](../audits/2026-10-13-n2-double-long-joint/paper/REPORT.md)。

## 3. 零／一條 spoke 的來源排除

**定理 T0：`t=0` 不可能。** 每份沒有 shared contact 的原 mixed C 都有某個
帶框附件的 root-contact：多 block 用已採納的 leaf 私有 contact，單 block
用 bridge／奇環上的 contact；原完整 degree4 迫其另有一或兩個框鄰居。
singleton 必 shared，另行處理。

固定任一指定列。若 P shared，它接受所有 diagonal；Q 若也 shared 即接回，
否則取 Q 上述實際附件的框色作共同 root pin，兩份都由 slack 接回。
若兩份皆不 shared，各選一個帶框附件的 contact。owners 不同時用共同碰色引理；
owners 相同時，另一 root 的兩份 incidences 總和為5，至少一份≥2，
用碰色加容量引理。所有 pins 都合法，因沒有 spokes。故同列原 G 可染。

**原 K₅ 引理 H。** 設原 C 的同一 leaf cycle 有相鄰私有 contacts p,z，
各只有框附件 h，且原圖有 root-spoke 到 h。五個原 bags 是

`{h}`、`H−C`、`{p}`、`{z}`、`(C−{p,z})∪(B−{h})`。

另一 long 使第二袋連通且接 B−h；刪兩個相鄰 cycle 私有點後 C 仍連通，
C 的 h 外附件未被刪去，使第五袋連通。原 spoke、contacts、cycle 邊、
框邊及另一 long 的實際附件給全部十對鄰接，違平面性。owners 可相同或不同。

**隱藏附件引理 HD。** 若 C 沒有 shared contact，且
`W_C^r∪W_C^s⊆{h}`，有原 root-spoke 到 h，則 C 在三個指定列都接受 `(D,D)`。
若拒絕，leaf bridge 的私有 contact 需兩個不同框鄰居，已矛盾。
leaf 奇環的私有 lists 都等於同一 block palette；普通私有點的 list 含 D，
contact 的 list 不含 D。因此拒絕迫全部私有點都是 contacts，
取相鄰兩點便觸發 H。單 cycle 同理，singleton／單 bridge 已另涵蓋。

**定理 T1：`t=1` 不可能。** 名唯一 spoke 為 rh。r,s 的 mixed incidences
總和為4、5。若兩份都 shared，直接用 `(D,D)`。若只有 P shared，Q 沒有 shared contact；
Q 的任何 h 外接點附件在某個指定列
與 h 異色，給合法 diagonal joint；五個框點的三列 signatures 互異。
故三列拒絕迫 `W_Q^r∪W_Q^s⊆{h}`，HD 又給 `(D,D)` joint。

沒有 shared 時，每份兩側 incidences 都≥2的 C，由§2迫
`W_C^s=∅、W_C^r⊆{h}`，所以 HD 給三列全部 diagonal acceptance。
r-incidences 只須分成 `(2,2)` 或 `(1,3)`，不是逐接點圖形分類：

- `(2,2)`：若兩份 s-incidences 都≥2，兩份直接用 HD；若一份只有1，
  它的總接線數為3，既有低接點 long 出口給一列，另一份 HD 在該列亦接受。
- `(1,3)`：對應 P,Q。若 `k_Q^s≥3`，Q 用 HD，P 總接線數≤3，仍同列接回。
  若 `k_Q^s≤2`，固定任一列的 `3×4` 合法 pins，P 至多拒4格，Q 至多拒6格；
  `4+6<12` 留下共同接受格，並取其兩份完整 lifts。

任意 block 長度、single block、shared 情形及 minor bags 的完整證明見
[structure §§2–7](../audits/2026-10-13-n2-double-long-joint/review/structure.md)，
另經 [獨立核對](../audits/2026-10-13-n2-double-long-joint/paper/REPORT.md#6-independent-review-of-the-zeroone-spoke-theorems-and-current-scope)。

## 4. 剩餘域與可反駁的 LL-CUT

兩份 long 的原盾弧互斥，各至少兩邊，故長度只有 `(2,2)` 或 `(2,3)`。
沿用 full-B-touch 與[原支援區間引理](c5_unary_shield_budget.md#2-盾弧純平面拓撲)，
actual support 恰為原盾弧頂點集，故支援大小分別為 `{3,3}` 或 `{3,4}`。
前者根 spoke sites 只有三個弧端點；兩 roots 若各有兩 spokes，必同接唯一
剩餘框邊，既有 K₅ 排除，故 t≤3。後者只能在兩個不相鄰公共端點接 spokes，
每 root 至多一條，故 t≤2。合 T0／T1 得精確剩餘表：

| 原 actual supports 大小 | root-spoke 分配（容交換 roots） | 同列合法 pins 格數 |
| --- | --- | ---: |
| `{3,3}` | `(2,0)` | 8 |
| `{3,3}` 或 `{3,4}` | `(1,1)` | 9 |
| `{3,3}` | `(2,1)` | 6 |

至少一份 long 的原接線數仍≥4。沿用原大小等式，本分支
`|H|=35−3t−Δ`，所以剩餘 t=2 時≤29、t=3 時≤26；沒有新有限搜尋下界。

固定一列，只從原接點資料取已證接受 cells

\[
S_C=\{(x,y)\in E_r\times E_s:x\in X_C^r\text{ 或 }y\in X_C^s
\text{ 或 }(x=y\text{ 且 C 有 shared contact})\}.
\]

**共同容量矩陣定理 M。** 若 `J_i=∅`，必有一份 0/1 矩陣 M，列標籤是原
`E_r` 色、欄標籤是原 `E_s` 色，且

\[
M=0\text{ 於 }S_P,\quad M=1\text{ 於 }S_Q,\qquad
k_P^s-1\le\sum_y M(x,y)\le k_P^s,\quad
k_P^r-1\le\sum_x M(x,y)\le k_P^r.
\]

證法是在每一格選一份**實際拒絕**的 piece，指派 P 記1、Q 記0；
兩份都拒絕時仍只指派一次。兩方向的容量及 degree5 等式恰給上述上下界。
所以 `S_P∩S_Q≠∅` 或這個矩陣不可行，便證同列原完整 joint。
固定 cells 後的直接計數 cut 不等式見
[paper §4](../audits/2026-10-13-n2-double-long-joint/paper/REPORT.md#4-small-cut-certificates-without-a-contact-template-classification)。

**LL-CUT（OPEN，下一個子命題）。** 在本節剩餘域，保留§1全部來源前提及
同一原圖，至少一個 `i∈I` 的上述 S 重疊，或其容量矩陣不可行。
這只詢問原附件、shared 身份、spokes、接線數及最多九格的分配；
不需預先知道任意大小 long 的完整接受表，因此比直接重述 `J_i≠∅` 更強。

反駁這條充分路線，須交付**同一份合格原來源**及三列各一份可行矩陣，
並保留完整來源資格、relations、空 fibres、full lifts。局部控制上的三份矩陣
只反駁削弱前提的版本。**可行矩陣不代表實際拒絕，更不是來源實現證書。**
各色框、圖源或列都不能在三份矩陣之間替換。

三點支援的 Eq／Diff masks 仍只標示 `(D,D)` 是否接受；四點支援不套三點兩位元。
把原完整 diagonal lifts 加入 S 可得到另名 `LL-CUT+diag`，但不能在驗證基本
LL-CUT 時暗中加入。這保留共同 joint 與 diagonal-only 命題的精確差別。

## 5. 反控制、完整證據與重播

既有四接點 path `p₀–p₁–p₂–p₃`、附件 `01,0,2,12`、owners `r,r,s,s`
在支援色 `(A,B,C)` 下的**完整拒絕集合**恰為
`([4]∖{A,B})×([4]∖{B,C})`，故三列全拒 `(D,D)`。
它是保留局部前提下最小 k=4 的 diagonal 障礙，不是完整來源反例。

若另一原 mixed Q 有框附件3，原 K₃,₃ bags 可取
`({b₂,b₃},{r,p₀,p₁,b₁},{s})` 與 `({p₂},{p₃},Q)`；
附件4有反射版本。兩 long 的互斥原盾弧迫 Q 有012外附件，故這份**精確原 path**
不能進入本目標來源。這不排除其他高接點 `M=I` pieces。

[固定控制](../audits/2026-10-13-n2-double-long-joint/controls/REPORT.md)
保留同一具名 H：兩份原 path 分別支援012、234，spokes `r0,s4`。
兩份三列 diagonal 都拒絕，卻有同列 off-diagonal 完整 joints；例如 q₁ 的全部
接受 pins 恰為 `(1,0)、(2,1)`。原圖 degree5/4、H二連通及 full B-touch 都成立，
但有上述 K₃,₃，且十列全收，所以完整 target 仍 `not triggered`。

| 證據 | 範圍 |
| --- | --- |
| 原完整 fibres／joint | 320局部 cells（80空）、856 tuples；160 joint cells、181全圖 lifts；逐原邊 DFS 與獨立 tuple 篩選／整圖 DFS 一致 |
| 同列同步校準 | 48碰色加容量、29交叉碰色，均 `triggered and holds`，各存完整原 lift |
| K₅ 補充控制 | 四種 owners、20棵原 bag spanning trees、40條原鄰接；只觸發 minor 前提，HD／T1完整來源未觸發 |
| 容量矩陣 | 原控制十列及81份抽象 incidence profiles 雙實作一致；另保留各自有接受格而矩陣仍可行的負控制 |
| 完整目標／Lean | 完整 target `not triggered`；没有新 Lean theorem；有限控制不證無界來源排除 |

```bash
python3 -B audits/2026-10-13-n2-double-long-joint/controls/checker.py --check
python3 -B audits/2026-10-13-n2-double-long-joint/controls/supplemental_minor_checker.py --check
python3 -B audits/2026-10-13-n2-double-long-joint/joint/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-n2-double-long-joint/joint/checker.py --check
python3 -B scripts/check_docs.py
python3 -B tools/docgraph --include 'docs/**/*.md' check
lake build
git diff --check
```

三份 checker 的正常／seed17、毀損負控制、凍結輸入 hashes 及文件／build 結果
見 [verification](../audits/2026-10-13-n2-double-long-joint/verification.json)。
未重跑上游 N45／44／SD-A／ES／ER 生成，沒有新來源枚舉。
本轮凍結後工作樹另新增一-long 排除；本頁證明不依賴該並行成果。
本輪不 commit／push。完整 `(2,0)`、LL-CUT、N2契約外情形及 E-ARC2 保持 OPEN。
