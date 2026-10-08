# E4 新 core 約束的獨立唯讀 review

基準 `2ac279b`；worktree `/home/ray/developer/ai/math-task-e4`。
本 reviewer 只 exclusive-create 本檔，未修改任何其他檔案，未 commit／push。

**判定：本次指定的 N3、條件式 N1 empty-support、unit derivative/E2、
triple-critical spoke 與 N2 duplicated-spoke core 約束均成立。**
另依整合者追加要求，獨立核對並確認並行 REPORT 的 N1-22-44 紙面子引理。
N1、N2 的完整來源排除仍未完成；本次 review 沒有把未知完整 mixed relations
填成已知 fibres，也沒有宣稱已找到要求的非相鄰正控制。

本檔稽核的是如下 bytes：

- `scripts/c5_excess_two_e4_core_constraints.py` SHA256 `e72530d38a26842550fb397430b25bd1622c1d125ee8a80915228fed41a7a33a`。
- 追加 review 的並行 `artifacts/c5_excess_two_e4/REPORT.md` SHA256 `a0053f874ca58322a57391abca877beb5cf26884014280fd0c328ac0d8601b74`，僅 §3 N1-22-44、§5 theta。

**範圍界線。** 不 certify 並行 REPORT 其他 N-diagonal／N2-short、
無條件 N-empty-separating 的紙面論證；不 certify 外部
`c5_excess_two_e4_control.py`、`c5_excess_two_e4_reductions.py`、
`control.json`、`reductions.json`。未重新跑這些 producers。
本 reviewer 也沒有將既有 E3 的任意大小全 degree-4 分類重新證明一遍。

## 1. N3：K₂,m 面預算與 theta

**Verdict：成立。** 新 checker:57–77,212–214；繼承前提來自
E3 `nonadjacent_notes.md:93–116`；並行 REPORT:219–232 是等價的三路 theta 版本。

m≥2 時每份原 mixed P 刪除後仍有另一份原 mixed 給 z–w 路，
所以每份都 one-sided。繼承 N-empty 與來源 criticality，使每份
`N_B(P)` 非空。此步不指定 q₂／q₄ 的角色。

只為 topology，收縮各份相互不交的原 connected mixed P 成一點 p，
每個 root–p 保留一條實際原 incidence 邊，刪多餘 incidence、spokes、unary。
B 保留原連通 C₅，與所有 p、z、w 互斥；每份 P 的一條實際 P–B 邊保留。
這得到原嵌入中的 K₂,m 加 B 及其實際附件；收縮不替換任何原 coloring relation。

K₂,m 對 m≥2 是 2-connected，故 facial boundaries 是 simple cycles。
它是 simple bipartite，面長至少4；V=m+2、E=2m，Euler 給 F=m，
面長總和2E=4m，因此每面恰4，且恰含兩個不同 mixed vertices。
連通且 disjoint 的整個 B 落在 K₂,m 的同一個開面。
每條原 p–B 邊除端點外同在該面，所以每份與 B 相鄰的 p
都在這一面的 boundary。只能有兩份，故 m≤2。

等價 theta proof 亦保留整份原 component：三個原 mixed 各取一條
simple z–w 路；B 在 theta 的外互補面，其 Jordan boundary 是其中兩路。
第三路的內點在 bounded side；其整份原 P connected、與這條 Jordan cycle
互斥，所以整份 P 都在 bounded side。任何 P–B 原附件會穿越 cycle。
故至少一 mixed support 空，再用 inherited N-empty 矛盾。
這不能只把第三條 path 當成整份 P，並行 REPORT 已明確避免此偷換。

新有限控制只列 m=2..5 的33份 quotient rotation；其面長均4的資料
吻合上面無界 Euler 論證。33份不是任意大小 proof 的代用品。
N3 排除包含它原先的 `(4,5)`、`(5,4)` 與 full `(5,5)` cores，沒有殘留。

## 2. 條件式 N1 empty-support strengthening

**Verdict：成立（保留外路條件）。** 新 checker:138–172,196–203；
本節的證明比 inherited one-sided 條件更弱，但仍有明列條件。

若 empty-support 原 mixed P 在 G−P 中存在一條實際 z–w 路 L，
L 可以經 B。任意合法外部染色在 N(P) 上只見兩 roots。
相同 root pins 時用 L 作一個 connected hub；不同 pins 時沿任一
原路邊切成兩個互斥、連通、相鄰 hub，各含對應 root。
每個 hub 的同色條件只看 `hub∩N(P)`；L 其餘頂點不需同色。
完整 degree4 使任何局部拒絕 lists 為 degree assignment，
拒絕 tightness 及 hub 原則給 K₅ contradiction。
因此 P 延拓每份合法外部染色，contact edge 不可能 Σ-critical。

N1 的 sole separating P 若兩側 mixed incidences a,b≤4，
兩 roots 各有至少一條原 side incidence。它是原 spoke，或通過
一份原 unary 到其 actual boundary support；unary 支援非空
由 inherited critical witness／盾弧結果給出。
兩侧各到 B，再沿原 B 連接，構成 G−P 中的實際 z–w walk，
刪重複段得所需 simple path。因此 guarded a,b≤4 的空支援來源可排除。

若 a=5 或 b=5，該 root 在 G−P 中沒有 side incidence，此證明
不提供外路。新 checker 明列這些 guard 外 cases 未由本條件式
論證排除；本 review 不用並行 REPORT 的另一個 appendage 證明
冒充此節前提已满足。

## 3. Unit derivative 不是 critical 時的 E2 接合

**Verdict：成立。** 新 checker:113–135,202,210。

設 X 保留原 B、disk、T4，所有有效內點 degree≥4，ε(X)≤1，
但不假定 X 自己 Σ-critical。在有限非框邊集合中取保留
`Σ(Y)=Σ(X)` 的 inclusion-minimal 子圖 Y，忽略孤立內點。
Y 的每條非框邊必改變自身 Σ，否則還能刪；由刪邊完整 witness
及四色補色論證得 Y 的有效內點 degree≥4。T4、disk、induced B
均由子圖繼承。

每個 Y 的有效點是 X 的點，且 deg_Y(v)≤deg_X(v)，兩者有效 degree
均≥4。因此逐點比較再省去被刪的非負項，得
`ε(Y)≤ε(X)≤1`。Y 若有拒絕列，其有效 H 連通由 E2 一般前提推導；
不必把 X 的 H 連通或 source criticality 偷渡到 Y。
E2 可套在 Y 自身，且 Σ(Y)=Σ(X)，故 X 的 Q 為空、singleton，
或相鄰兩點；尤其 X 不可同時拒 q₃ 與 q₀/q₁。

原 single side unit deletion（spoke 或一份 capacity-one unary）
把對應 root5降4，另一 root維持5，其他保留 degree4，故 X 自身 ε=1。
兩側各 unit 或 unit `(1,1)` mixed deletion 則 ε=0。
這些是原完整 factor 刪除，不是把 minimal-q 子圖的 full Σ 當來源 Σ。

`derivative_masks` 列6個 ε0 masks、11個 ε≤1 masks，與上述
Ω／五 singleton omissions／五 adjacent-pair omissions 一致。
mask 列算術只驗證 E2 的有限結論介面，不建立 minimalization theorem。

## 4. Triple-critical 兩個原 spoke sets

**Verdict：成立。** 新 checker:80–110。

原 spokes={0,2,4} 時，rb₂ 在 q₀、q₁與 rb₄ 同色，在 q₃與 rb₀同色；
所以刪 rb₂ 不會改變三列中任何 root 的避色條件。
原 spokes={1,2,4} 時，rb₄ 在 q₀、q₁與 rb₂ 同色，在 q₃與 rb₁同色；
刪 rb₄ 同樣不會新接受任何指定列，違反 triple-critical。
這保留的是同一條固定原 edge，不是每列另選一條 redundancy edge。

新表覆蓋所有原 ≤3 spoke sets：1+5+10+10=26份；
唯有上述兩份存在 never-private 固定 spoke。
它未固定 spoke=b₀ 作 WLOG，因此沒有 D₈ degree6 的相對位置覆蓋缺口。

## 5. N2 repeated spokes 的精確 core 身份

**Verdict：成立。** 新 checker:204–211；繼承原 core 分類為
E3 `nonadjacent_notes.md:119–169`。

m=2 時所有拒絕 q 的 minimal cores 都含兩 roots。
Minimal-q core 不能保留 q 同色的兩條原 root-spokes，
否則刪其中一條不改 q 著色可行性，違反 q-critical。
若某 root 在原圖有 repeated spoke pair，它在 core 中 degree
不能維持5：degree5會保留全部原 incidences，包含此冗餘 pair。

兩 roots 都有 repeated pair 時，core只能degree(4,4)。
但兩侧各省略spoke會保留兩 mixed，違反 inherited 44 只能保留一 mixed；
另一種44只省略一份unit `(1,1)` mixed，則兩側原重复 spokes都仍保留，
又違反q-critical。因此每指定拒絕列最多一 root 有 repeated spokes。

只有z有repeat時，每core須把z降4。任何loss1省略mixed/unary
都留下原 duplicate spokes，所以z必精確省略兩條重色原 spokes之一。
若w也降4，這種兩側side omission會保留兩 mixed，違反44分類。
所以w degree5，並由 degree4 piece 飽和、w saturation，
其餘原 incidences全部保留。每core精確為
`G−zb_i` 或 `G−zb_j`，degrees(4,5)，其中i,j是此列的原duplicate pair。
w單側repeat則對稱。這比“可能省略一個side factor”更精確，
沒有把一般 mixed relation 投影為獨立 marginals。

## 6. 追加 review：並行 REPORT N1-22-44

**Verdict：成立（沿用全 degree4 的實際分類）。**
僅 review 並行 REPORT:92–152 的紙面 proof，沒有 certify 其 producer/artifact。

原 sole mixed C incidence(2,2)且存在44core時，兩原root triangles
互斥、由一條直接bridge相連且無tails。原 degree4飽和保留整個C，
所以C精確為原path a−b−c−d，z contacts(a,b)、w contacts(c,d)。
a,d各有兩原框附件，b,c各一個；每root core side恰兩spokes。
原每side容量3且只能省略一unit，故原side是三spokes，或兩spokes加
一份被省略的capacity-one unary；沒有其他retained unary。

每原side root自身degree3，其他side點完整degree4，故其degree lists
在root有slack，連通side可延拓任何β。
若terminal兩框附件在某指定q同色，其C-degree lists有slack，
能接回任意合法root pins；原兩side既全收，便使G接受q。
三指定列涵蓋全部五個非框邊pair的重色，因此terminal pair必為真框邊。

沿原bc把H拆成完整原sides A_z、A_w。它們 connected、disjoint、
互為connected complements。純盾弧 Lemma1/2 的逐行 topology proofs
只使用上述連通條件、B outer、full B-touch；沒有使用“P必是degree4原piece”。
所以可以把兩whole sides定義為兩盾弧，二者互斥且 actual support
等於盾弧全部頂點，並没有對sole separating mixed收费。

每side support至少3。若side盾弧≤2，恰support三個連續框點：
有unary時它的support至少3且包含side三點，故等於這三點；
unary盾弧的middle不可被C-terminal碰到，terminalpair只能是兩outer
points，非真框邊，矛盾。
無unary時此side root有三spokes，正好這三框點；terminal真框邊的
兩端是spoke endpoints，terminal所在的star面唯一是对应小triangle。
此case原H−root connected：只有sole C及另一root/其unary，
本root沒有unary可刪後留下另component。
故整個H−root在同一triangle面，其全部框附件只到triangle兩框端。
加回三spokes後全G只碰三框點，違反full B-touch。
所以兩side盾弧各≥3，互斥即6>5，排除該整類。

這不排除沒有44core的原C incidence22；其45／54／55原joint仍未知。

## 7. 控制與證據邊界

讀取新 `core_constraints.json` 可對上33quotient rotations、26spoke sets、
6/11個derivative masks、90份合法boundary-path hub partitions及complete
same-graph schema。這是檔案讀取與紙面 review；本 reviewer 未宣稱另跑其
`--check`。所有正式普通／seed17/文件檢查 exit 應以任務方實際 validation 為準。

要求的“非相鄰兩degree5、ε2、T4、Σ-edge-minimal”實現正控制仍未取得。
因此上述不使用三列的中間引理，尚缺在這個指定控制圖上的實際驗證。
有限quotient/hub controls沒有滿足該graph前提，不能替代；
既有951/935也不滿足nonadjacent雙root前提。

所有殘留的R_P仍由原全圖、原contacts、actual supports、ownership、rotation、
同一literal β及whole-coloring witnesses定義；UNKNOWN fibres不當成empty。
沒有q₂/q₄ exact角色、沒有逐key source枚舉、沒有新增Lean proof。
