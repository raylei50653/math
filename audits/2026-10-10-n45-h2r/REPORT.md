# N45-H2R：完整 relations／原圖幾何的獨立裁決

BASE `dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`；2026-10-10。
**原文裁決：11 claims 成立；H2-EXCLUSION 有量詞 gap。限定三色 γ 後，完整 HIGH2
來源排除仍成立，屬待監督採納的 paper 候選。** 不記原文12項全 PASS，也不修改 worker。
唯一 finding `H2R-EXCLUSION-FOUR-COLOR-UNUSED`：對四色情況不存在全框未用色 Dγ。
這個 query 限定不增加來源 H1–H13；它修正原文過寬的局部構造量詞。

## 1. 凍結、authority 與精確裁決範圍

exclusive 新目錄只寫本 audit；shared、worker、parent、siblings、舊 H3G 均未改。
未再委派、commit／push／PR 或送外部訊息。HIGH2 已正式交付，因此本輪可讀。
[契約](frozen/dispatch/audit-contract.md)、[任務](frozen/dispatch/h2r-task.md)、
[intake](frozen/dispatch/intake.json)完整凍結。
[input index](input-index.json)核 worker 全118檔與原 tree、parent frozen 的 bytes／mode／SHA256 一致。
包括 worker nested manifest／delivery／receipt、失敗版 checker、generation FAIL 與 custody FAIL；
沒有因檔名是 metadata 而從 nested payload 排除。
[source 核對](source-input-verification.json)另核41 inputs（22 BASE、19 current）與8 pins，全部零漂移。
這不能把 worker whole-worktree outside custody exit1 改成 PASS：同期新增與 named input 漂移分明。

量詞為每一任意有限大小 G，滿足 worker [REPORT §1 H1–H13](frozen/worker/REPORT.md)及
[正式全文](frozen/worker/frozen/current/audits/2026-10-10-n45-high1-supervision/high2-task-body.txt)。
以下子引理均保此完整 domain。關係查詢涵蓋每 proper literal γ、全部 r/s pins、
ambient tuples（含空 fibres）、所有原 attachments／shared contact 單變量／rotation 和孤立因子。
[independent judgment](independent-judgment.json)逐12 claim另列 raw／qualified verdict、BASE章節及殘留。

## 2. CORE／COMP／JOIN／RESTORE／F

只有原 e=rb_i 被省略，r 在 X 有3 mixed contacts＋retained rb_j，完整 degree4；
s 有2 mixed＋2 U contacts＋唯一 sb_k，完整 degree5；其餘有效點完整 degree4。
X 自己的 β minimality 直接由 H10 給；不从 G-criticality 遺傳。內部邊未改，
H_X−s 恰 C={r}∪P∪Q 與完整 U，ordered contacts 各兩個，兩份 connected 且沒有跨邊。

對每 γ 定義 C 的 Fib_C(γ,t,c) 與 U 的 Fib_U(γ,u)，如 worker §3，保留全部原 assignments。
X full lift 與 f_C、f_U、s=a≠γ(b_k)、I→Col 的 restriction／union 是雙射，
条件為同一 t,u 四座標皆避 a，且 f_C(r)=c≠γ(b_j)。固定任何 r/s pins只取對應 fibre，
空集合也保留。P/Q 的所有 r contacts 同時查同一 c；shared contact 是一原變量。
G 的 full lifts 恰此全集再加 **c≠γ(b_i)**。這直接從原 edge set 證，非 marginal 接合。

R10 的 contact slack 給每 γ 的 R_C、R_U 非空，兩份 |F|≤2。
在 X 的 β 下，incident-edge 解除與 X 自己的 minimality 給
F_C∪F_U=Col\{c0}、兩份皆有 private color，c0=β(b_k)。
BASE E4 §4.1 的局部 N-diagonal 適用原 P/Q：其 degree4、真框邊支援、one-sided；
H−P／H−Q connected，full B-touch 在支援外提供原附件，不要求外部已合法染色。
對每 γ、每 a≠γ(b_j)，原 r=s=a 的 P/Q full assignments 因而給 C 避 a，
故 F_C(γ)⊆{γ(b_j)}。在 β 下 private cover 迫
a0=β(b_j)≠c0、F_C={a0}、F_U=Col\{a0,c0}={D,h}。
兩原 s–U contact 各自解除，給同一完整 U 的兩個方向，故 R_U(β)={(D,h),(h,D)}。
這不是兩個 endpoint palettes 的乘積，也不借 HIGH1 unary 容量。

## 3. K33／ARC：G 的例外 O′ 與 shield

在原 G 取 critical sxν 的新接受 full lift：f(s)=f(xν)。限制到 G−U 仍含 e；
若原完整 U 可避 f(s)就接回 G，矛盾，故有非空 U forbidden query。
H−U={r,s}∪P∪Q connected，full B-touch、one-sided 和 degree4 符合 BASE shield
§§2–3／Theorem A，故 |σ_U|≥2、|S_U|≥3。此步不先假設 P/Q 支援頂點互斥。

若兩真支援框邊共端 v，六互斥連通 bags 左 P,Q,O、右 {r},{s},{v}。
b_k≠v 時 O=B−{v}。b_k=v 時 **O′=(B−{v})∪U**：U actual support 至少三點，
所以至少一條 U 原附件接到 B−v，使 O′ connected。九原鄰接如下：

| pairs | 原 G edges |
| --- | --- |
| P–r、P–s、Q–r、Q–s | 四正 incidence 的原 contact edges |
| P–v、Q–v | 兩 actual support 附件 |
| O／O′–v | 原框邊 |
| O／O′–r | r 兩不同 spokes 至少一端≠v；可用 e，因 minor 在 G |
| O–s／O′–s | b_k≠v 用 sb_k；例外用原 sx1 |

故 G 有 K3,3 minor。P/Q 支援框邊必頂點互斥；其一邊盾彼此互斥。
剩餘框邊分長2／長1兩弧；U 連續盾至少長2，只能是長2弧。
BASE full B-touch support lemma 給 T={b_L,b_m,b_R}、σ_U=b_Lb_mb_R。
H−U 不碰盾中點；原 r/s spokes 避 b_m。P/Q 四端點恰 B−{b_m}，
所以 X 的 actual S_C=B−{b_m}，C 真碰 T 外兩框點。

## 4. MAP／BRIDGE／SPLIT：任意兩 W 的 X 原 K5

X 逐項满足 BASE single-spoke (2,2) §1：s sole spoke、兩二-contact 分量、完整degree4、
自己的 β minimality、disk、從 G 繼承 T4。一次整圖 D5/S4 搬 β 到 q，保全部資料與933 q2。
八個具名位置的必要 records 在本次 verifier 獨立對照 BASE artifact：四個無 slit placement
是 crosscut source exclusion；其餘核 record90／511 的 actual supports、ban roles、spoke及placements。
記錄僅必要 identity；後續 p1/p2 延拓是 **X query**，沒有原 r fibre 即不能恢復 e。

F_U(β)={D,h} 給兩份真正拒絕 degree-lists。s spoke 使 B∪{s} connected，
BASE tree-component §1 給 U K4-free；Gallai、(2,2) §3 兩 palette 差沿同一 incidence tree
迫唯一原 x1–x2 bridge 路徑 z0,…,zℓ，ℓ≥1 奇數。所有 path 外 blocks 原樣留在 Wν；
刪 path edges 只定義各 W，彼此不交且合起來是完整 U。
每 W 的 residual 固定為 {D,h} 需這兩份既存拒絕證書；旁支非 root lists相同，
rooted-palette 唯一性先給旁支 palettes相同。逐色固定 β(Tν) 的置換保持 residual；
因 D 未出現在 β，若 a0 或 c0 未供應，交換該色與 D 即矛盾，故各 W 真見 a0,c0。
沒有假定 residual 就是完整 rooted root palette。

任取 i<j，若 Wi、Wj 都真接 b_a,b_b∈T，在原 C 由 s-contact 到任一 actual T 外附件
取簡單路 L 到 b_t∈B−T，內部在 C，只在終點碰 B。它可經 shared contacts／r；
零長 C 內子路亦可，且避整個 U。沿三標記框點分三非空互斥連通弧 X_a,X_b,D_t。
J 為原 bridge 路加 sx1、sx2 的 cycle。五 bags：
A=⋃_(ν=i)^(j−1)Wν，A′=Wj，Z=(V(J)\{zi,…,zj})∪V(L)∪D_t，X_a，X_b。
A 沿原 bridges connected；A′ connected；cycle 外段經 s，L 接 s 與第三框弧，故 Z connected。
W 全旁支互斥、L 避 U、三框弧互斥，使五 bags不交，任意大小及不相鄰 i,j 均適用。

| 十 pairs | X 的保留原邊 |
| --- | --- |
| A–A′ | z_(j−1)z_j |
| A–Z | z_i 的前向 cycle 邊；i=0 用 z0s |
| A′–Z | z_j 的後向 cycle 邊；j=ℓ 用 zℓs |
| A–X_a、A–X_b | Wi 的两 actual attachments |
| A′–X_a、A′–X_b | Wj 的两 actual attachments |
| X_a–X_b、X_b–Z、Z–X_a | 三原框切口邊 |

全部在 X，不使用 e；minor 只反證非平面，不替換 coloring。
若 β(T) 三色，a0,c0 各唯一供應點使任兩 W 出現此 K5，矛盾。
故 β(T) 二色，左右端同色異於中點；各 W 碰中點與至少一外端。
三份以上 W 的兩外端鴿籠也給 K5，故恰兩份、ℓ=1。
任一 W 接兩外端也與另一份共享供應點，所以實際支援恰左右兩真框邊。
這限制 bridge 數，不限制兩完整 W 的大小、旁支或 blocks。

## 5. PALETTE 與有資格的 EXCLUSION

K_W(γ,c) 是完整原 W 的 rooted assignments，A_W 是非空 root fibres 的色集。
原唯一 bridge 的 full-assignment restriction／union 等價於 root 色相異。
R_U(β) 的兩交換 tuple 使兩 A_W 都含 D,h；若任何一邊還有另一色，與另一邊的 D
full assignment 拼合就產生漏掉 h 的 tuple，矛盾。故 A_WL=A_WR={D,h}。
这才證實真 rooted palettes，沒有把 residual 直接認成 A_W。

每 W 的 actual support 恰真框邊兩端；β 與任意 proper γ 在该 pair 均兩色互異。
完整 assignments 在 S4 下有雙射；在 W 的其餘無入射框點改值不改 constraints。
因此在**同一 literal γ**內 A_WL=Col\{γ_L,γ_m}、A_WR=Col\{γ_m,γ_R}，
完整 R_U 為此兩色集笛卡兒积限制不等式。這個 all-proper-γ 結論保留，四色也成立。
兩份 W 最終接合同一 γ 的原 full assignments；不是兩分量各自 normalized query。

原 H2-EXCLUSION 的「每 proper γ在T见三色，令全框未用色Dγ」須限定：
**γ 全框恰使用三色，且 T 上三色互異。** 此時取原完整 W assignments
x_L=γ_R、x_R=γ_L，兩色相異且都避 Dγ。原 r=s=Dγ 的 P/Q N-diagonal full assignments
與兩 W、任意 I assignments 拼合成原 **G** full lift；所有原 spokes均合法，
包括 e，因 Dγ≠γ(b_i)。這有明確原 r fibre，並非把 X 指定延拓當 G。

proper 三色 C5 的 singleton 位置在 T iff T 上見三色。所以 Q(G)⊆B−T，大小≤2。
933 的全部四個拒絕（含q2）、941 的三個拒絕都矛盾；共同 D5/S4/root naming保包含性及大小。
四色情況的接受已由 H2 的完整 Σ 给出，无需用不存在的 Dγ 補足此 singleton 排除。
完整 HIGH2 no-source conclusion因此 **holds with explicit qualification**；原過寬構造仍是 gap。

## 6. Finding：raw 與 qualified 分明

[finding](findings.json)及[proof witness](proof-witness.json)保 γ=(0,1,2,3,1)、T=(b0,b1,b2)：
proper C5、T 三色、全框四色，Col\γ(B)=∅，不能按原文取 r=s=Dγ。
這是 scalar／query 構造的 `counterexample`，不是滿足 H1–H13 的 HIGH2 來源反例。
受影響 claim ID 僅 H2-EXCLUSION（worker §8 lines238–243及 claims.json量詞）。
H2-JOIN／RESTORE／PALETTE 的 all-proper queries不須改；EXCLUSION 的 source conclusion
不須改H1–H13，但其中構造的 query domain必在採納時明列 three-color。
父端已要求保 raw finding並分開裁定縮窄範圍；本稽核不刪 finding，不自行採納。

## 7. 證據與實際重播

外部信任：[Dvořák primary Gallai lecture](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，
本次 [frozen PDF](frozen/worker/frozen/gallai.pdf) hash與已核primary bytes一致。
Lemma7／Theorem10只在連通 degree-lists已拒絕後給tightness、Gallai及block palettes。
BASE E4、shield、rooted uniqueness、bridge、frame-arc是具名paper依賴；不將歷史E4 provenance FAIL掩去。
沒有新增任意大小 Lean proof、finite HIGH2 source或source realization；source trigger_count=null。

[semantic checks](semantic_checks.py)只核一份固定 toy 的完整 C tuple/r fibres、U fibres與X/G
full lifts restriction／union（包括孤立4因子與所有空r/s pins），及具名K33/K5 partial skeletons。
它們不是 HIGH2 source，也不替代上述無界論證。[verifier](verifier.py)另核凍結118檔、41inputs／8pins、
manifest、raw finding、BASE具名 mapping和本REPORT local links／whitespace。

```sh
python3 -B audits/2026-10-10-n45-h2r/verifier.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-10-n45-h2r/verifier.py --check
python3 -B audits/2026-10-10-n45-h2r/verifier.py --check --negative-control
```

normal／seed17實跑 exit0、stdout byte一致；negative在記憶體移去K5必要原框切口邊，
於 missing original bag adjacency 階段 exit2。三份完整stdout／stderr／exit receipts綁manifest hash，
delivery再綁receipts；payload前後不變。exact top-level metadata才排除，nested同名全部在payload。
未重跑worker大型控制、全樹inventory、lake、global DocGraph或歷史provenance。
原 generation mapping FAIL、62 duplicates、BASE missing-doc／optional-artifact lookup及outside custody FAIL均保留。
停於本限定獨立裁決交付：監督需明列 H2-EXCLUSION query量詞修正；不傳播shared或擴一般N2／E。
