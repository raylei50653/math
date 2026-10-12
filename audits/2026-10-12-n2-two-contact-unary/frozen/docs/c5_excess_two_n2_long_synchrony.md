# N2 原55：long 同列同步與葉接點 tree 化約

**後續（2026-10-12）**：[完整fibre分割與已用色禁色規律](c5_excess_two_n2_partition_rule.md)
以共同容量排三接線U，並將本頁七個低接點同類弧模板一起排除。
完整 `(1,1)` 剩餘必 `k_U=2、M_U=∅、M_L=I、k_L≥4`，U每列恰禁一個支援已用色。
本頁四形分類、原控制及當輪停止點保留；父原55／N2／E-ARC2仍OPEN。

**整理發布（2026-10-11）**：相連四輪成果由[發布紀錄](history/2026-10-11-n2-55-progress-publish.md)
統一保存驗證與提交範圍；下文原生成基準及當輪「未提交」語境保留。

2026-10-11；基準 HEAD `5f0979793c19e452dbb5fc7e9fe7e43cb8a991cc`，
包含前輪未提交採納成果；13 份精確工作樹輸入見
[BASE](../audits/2026-10-11-n2-long-mask-sync/BASE.json)。接續
[三列 diagonal 採納](c5_excess_two_n2_diagonal_three_row.md)，
目前停止點見 [Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口)。

**新增三項限定排除：兩份 long 都接線至多三；一 long 無 U 且全部 root 接點
都是原 tree 的葉；含 U 的低接點 long 與 U 有不同類 diagonal masks。**
另將含 U 的低接點同步缺口縮成七個具名字面弧模板。
九格仍為七格已有覆蓋，三個含 long 父情形及 E-ARC2 均 **OPEN**。

新結論是任意大小紙面證明＋另人獨立審查，沿用既有外部 degree-list／Gallai
依賴；有限完整 fibres／joins 作校準。target 來源仍 `not triggered`，未新增 Lean
theorem、10–35 內點搜尋、commit 或 push。

## 1. 完整來源、原 pins 與局部查詢

沿用 [前輪完整契約](c5_excess_two_n2_diagonal_three_row.md#1-完整來源契約)：
有限簡單 induced-C₅ disk、有序原 B，完整 Σ933／941 或整圖共同 D₅ 像、
T4 全收、全部非框邊 Σ-critical、ε=2、連通且 full B-touch 的有效 H；
恰兩個非相鄰原完整 degree5 roots r,s，其餘有效內點原完整 degree4；
H−{r,s} 恰兩份原 mixed P,Q，其餘 unary，全部 pieces one-sided。
原 ordered／shared contacts、ownership、actual attachments、rotation、bridges、
旁支、同一字面色框、完整 relations／空 fibres／full lifts 全保留。

固定 `I={0,1,3}`、`q₀=01212`、`q₁=01202`、`q₃=01021`、未用色 `D=3`。
mixed 的 `M_C={i∈I:(D,D)∉A_C(q_i)}`；unary 的 M 記 owner=D 無完整 lift 的列。
這些 masks 只標示出口位置，接回仍要全部原頂點的完整 lifts。
接線數 k 計原 root incidences，有 shared contact 時不改成不同接點數。

## 2. 兩份低接點 long 的原圖排除

**原相同框邊 spoke 引理。** 若兩 roots 都接原框邊 ab 的兩端，且原 mixed C
有附件 vh、h∉{a,b}，則 G 含 K₅ minor。

原中央二連通 block 包含 r,s 及全部 mixed 頂點。從 v 到 {r,s} 的兩點 fan
截到首次碰 roots，給內部在同一 C、通過 v 的原 r–s 路 A；另一 mixed 給內部
互斥的原路 A′。五個原 bags 為

`{r}∪(A′−{r,s})`、`{s}`、`{a}`、`{b}`、`(A−{r,s})∪(B−{a,b})`。

最後一袋由原 vh 接通，所有袋互斥連通。兩路首末邊、四條原 spokes、原 ab
及補框弧兩端邊給全部十對鄰接。完整證明及另人核對见
[原 topology](../audits/2026-10-11-n2-long-mask-sync/review/root_topology.md)、
[獨立核對](../audits/2026-10-11-n2-long-mask-sync/synchrony/REPORT.md#5-對原-topology-證明的獨立核對)。

**定理1。** `(ℓ,u)=(2,0)` 若 `k_P,k_Q≤3`，完整來源不存在。

shared-contact 情形沿用前輪同列接回。否則原 degree 計數
`10=k_P+k_Q+t_r+t_s` 及每 root 至多兩個相鄰框附件，迫
`k_P=k_Q=3,t_r=t_s=2`。兩 long 邊互斥的原盾弧各至少長2，只有 (2,2) 或 (2,3)。
後者只留兩個不相鄰的弧端点，不能容 root 的兩個相鄰框附件；前者三個可用端點
只有一對相鄰，恰為唯一剩餘框邊 ab。兩 roots 都接 a,b，而 long 有 pair 外的
原附件。上引理给 K₅，矛盾。因此 `(2,0)` 剩餘必有一份 long 的 `k≥4`。

## 3. 任意接線數的葉接點 tree 出口

**定理2。** 原 mixed C 若是 tree、沒有 shared contact，且所有原 root 接點
都是 C 的葉，則至少一指定列有原完整 `(D,D)` lift；不限制 k。

反設三列皆失敗。原 tight degree lists 的 bridge palettes 中，D 邊是覆蓋全部
普通點、避開全部 contacts 的 matching。普通點誘導 forest 的 perfect matching
唯一，故三列共用同一原 D 邊集。只在輔助 counting tree 收縮這些 matching 邊，
取一個末端 unit 的原端點 y，使其除 matching 伴點外只接 contact 葉。
原完整 degree 四迫葉數為1、2、3。

一葉迫 y 與葉重複同一實際框邊；兩葉迫不存在的原框點第三色 signature；
三葉迫三條不同原框邊的 T signatures 在三列都見齊0,1,2，字面五邊表排除。
單bridge另由框邊附件單射排除。沒有省去原鏈後移植 relation；出口是原 C
的完整 list coloring。完整無界證明見
[H-TREE-LEAVES](../audits/2026-10-11-n2-long-mask-sync/high-contact/REPORT.md#1-an-arbitrary-size-escape-beyond-the-contact-three-bound)，
[獨立紙面採納](../audits/2026-10-11-n2-long-mask-sync/review/independent_paper_review.md)。

**推論2.1。** `(1,0)` 的 long 符合定理2時，取其出口列及 short 的同列完整
diagonal lift，原 G 可染，故該子域排除，包括 k≥4 的任意大小形狀。
`(2,0)` 若另一 long 有 shared contact，亦在 tree 的出口列接回。
含 U 時，tree 出口仍要與 U 在同列，不能單由定理2排除。

## 4. 含 U 的兩邊弧 mask 分類與同步

在 `(1,1)` 中，原 U／long L／short S 的盾弧恰長 (2,2,1)。令兩邊弧
`A=(a,b,c)`，定義 `Eq(A)={i:q_i(a)=q_i(c)}`、`Diff(A)=I\Eq(A)`。

**定理3。** 原 C 是 U 或沒有 shared contact 的 L，k≤3 且 actual support
恰為 A 三點時，`M_C∈{∅,Eq(A),Diff(A)}`。

固定一個原拒絕列，原 cycle/contact 計數迫所有 cycles 是 triangles。
框邊附件單射只許兩個 H 內度二點，所以三 leaf blocks 不可能；兩 leaf blocks
的任意長鏈也只能保留下列四份原圖形。其完整 palette 計算給精確 masks：

| 原圖形 | k | 非空 M |
| --- | ---: | --- |
| 兩 contact 的單bridge | 2 | Eq(A) |
| 三 contact 的三點 path | 3 | Diff(A) |
| leaf triangle 加兩bridge tail，共五點 | 3 | Eq(A) |
| leaf triangle 共享普通 triangle，再接leaf bridge，共六點 | 3 | Diff(A) |

不能漏掉五／六點形，也不能只用兩葉短 path 校準外推任意大小。
完整窮盡與 same-row palette 計算見
[M-LOW-ARC](../audits/2026-10-11-n2-long-mask-sync/synchrony/REPORT.md#2-單一拒絕列即足夠的無界-block-tree-覆蓋)，
另經 [獨立採納](../audits/2026-10-11-n2-long-mask-sync/review/independent_paper_review.md)核對。

| 原弧 A | Eq(A) | Diff(A) |
| --- | --- | --- |
| 012 | {3} | {0,1} |
| 123 | {0} | {1,3} |
| 234 | {0,1} | {3} |
| 340 | {1} | {0,3} |
| 401 | {3} | {0,1} |

**推論3.1。** `(1,1)` 中 k_L≤3，若 U／L 至少一份 M 空，或兩份 M 分屬
Eq／Diff，來源排除。原盾弧邊互斥時，表中的 Eq sets 互斥；一 Eq 及另一 Diff
的聯集必留一列。該同列取 r=s=D，U、L、short S 全部原 lifts 接回 G。

因此低接點 L 的同步剩餘只保留兩份非空同類 masks：Eq／Eq 的原弧 pair 只有
`(012,234)`、`(234,401)`；Diff／Diff 仍有五份
`(012,234)`、`(012,340)`、`(123,340)`、`(123,401)`、`(234,401)`。
這七個是必要字面弧模板，U／L 的身份與 ownership 仍須保留，並非七份來源。

## 5. 新反控制與父情形停止點

四contact long path `p₀–p₁–p₂–p₃`，附件依次為 `01、0、2、12`，前兩點接 r、
後兩點接 s，三列均拒絕 `(D,D)`。原 degree 四、long 支援012、leaf 邊附件單射
均成立，兩內部 cutpoints 也是 contacts。全部十列16-pin fibres 已保存。
這反駁僅由既有局部前提將低接點 escape 推至 k=4；不是完整 Σ933／941 N2 反例。

| 父情形 | 本輪後仍須處理 |
| --- | --- |
| (2,0) | 至少一份 long k≥4；一般同列完整 joint 仍缺 |
| (1,0) | 無 shared contact、k_L≥4，且 long 含 cycle 或有 C cutpoint 接 root |
| (1,1) | k_L≥4；或低接點的七個非空同類弧模板，仍須原同列 joint |

新原圖引理另排兩 roots 各兩 spokes 且 spoke 邊相同的任意大小子域。
沒有改 Δ 門檻或大小上下界，沒有推升九格覆蓋數；一般原55／N2、N1／相鄰／
單-root例外、E-ARC2、一般出口及 K∞=K≤5 均 OPEN。

## 6. 實際驗證與證據分層

[本輪 audit](../audits/2026-10-11-n2-long-mask-sync/REPORT.md)保存原輸入 hashes、
各作者成果、獨立審查、負控制及 [驗證 receipt](../audits/2026-10-11-n2-long-mask-sync/verification.json)。
獨立 DFS 重算 179 原分量的28,640 cells（含3,372空 cells）及63原圖的10,080
同列同 pins joins，與全部原 tuples／完整外部 lifts／global SHA 相同。
800份固定四形等附件控制及45份完整 fibres exemplars 校準 mask 表；有限控制
不承擔無界窮盡。原兩-long共同出現及完整 target sources 仍零觸發。

```bash
python3 -B audits/2026-10-11-n2-long-mask-sync/controls/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-n2-long-mask-sync/controls/checker.py --check
python3 -B audits/2026-10-11-n2-long-mask-sync/high-contact/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-n2-long-mask-sync/high-contact/checker.py --check
python3 -B audits/2026-10-11-n2-long-mask-sync/synchrony/signatures.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-n2-long-mask-sync/synchrony/signatures.py --check
python3 -B scripts/check_docs.py
python3 -B tools/docgraph --include 'docs/**/*.md' check
lake build
git diff --check
```

正常／seed17 bytes 及 SHA 一致，毀損副本按預期拒絕，凍結輸入零漂移。
文件檢查及既有 Lean build 的實際結果由 receipt 記錄；build 不形式化上述新證明。
未重跑上游全部 N45／SD-A／44、ES／ER 生成、來源 rotation 或全工作樹 DocGraph。
