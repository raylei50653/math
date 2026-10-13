# E-ARC2：原55的 block 骨架與35內點上界

**後續（2026-10-13，BASE 243a125）**：[N2-BRIDGE](c5_excess_two_n2_bridge.md)
另排932，完成原E4完整來源契約的廣義N2；E-ARC2仍OPEN，未新增Lean證明。
以下各輪大小界與停止點保留當時語境。

**後續（2026-10-13）**：[LL-CUT+diag](c5_excess_two_n2_ll_cut.md)已排指定完整Σ契約的
原55最後雙long，九格全覆蓋；基本LL-CUT、較廣N2／E-ARC2仍OPEN。
下文保留原輪大小界、控制及OPEN語境，沒有新增Δ門檻。

2026-10-11，工作樹 HEAD `f428f6be3ee1eb59e3cb0b356239c4f16c4a6444`。
接續未提交的[完整N2真核心排除](c5_excess_two_arc_spoke_closure.md)；
目前停止點見 [Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口)。
整理發布與本次重播範圍見[三點弧發布紀錄](history/2026-10-11-three-point-arc-publish.md)。

**後續（2026-10-11）**：[N2殘餘統一與下界衝突檢查](c5_excess_two_n2_residual_unification.md)
以共同三-hub引理排完整目標域的兩unary原55子族，故u≤1；原大小界精化為
`|H|=35−6u−3t−Δ`。既有有限下界10與原上界無直接衝突，
還須證足夠的Δ或同列完整joint。原55及E-ARC2仍OPEN；下文保留原上界證明與控制。

**在前報告的完整目標 N2 前提下，原55來源的有效內點數滿足**

\[
\boxed{|V(H)|\le35-6u-3t\le35.}
\]

其中 u 是原 unary 分量數，t 是兩 roots 的原 boundary-spokes 總數。
因此 u=0、1、2 時分別至多35、29、23個有效內點；加五個原框點至多40點。
這是原圖大小界，沒有 contraction、替換、重新標號或丟棄完整 relations。
任意自由孤立座標不計入有效H，仍保留它們的完整四色乘積因子。

**這並未排除原55，亦未證 N2 或三點弧。** 新結果是紙面證明；有限控制
只核對具名 minors、cactus 計數及既有固定圖的適用部分，沒有新來源搜尋或 Lean theorem。

## 1. 完整前提與依賴

採用[前報告§1](c5_excess_two_arc_spoke_closure.md#1-完整來源前提與依賴)的全部契約：
有限簡單 induced-C₅ disk，指定有序 B，完整Σ=933／941或整圖共同D₅像，
全部非框邊Σ-critical，ε=2，連通full-B-touch的有效H；恰兩個非相鄰
完整degree5 roots r,s，其餘有效內點完整degree4。H−{r,s}恰兩份原mixed，
其餘unary；原pieces one-sided，兩mixed的actual supports非空。
固定三拒絕列 q₀=01212、q₁=01202、q₃=01021。

原頂點、ordered／shared contacts、ownership、實際框附件、rotation、bridges、
旁支與完整relations／空fibres／full lifts不變。下文的block均指原圖的maximal block；
bridge亦算K₂ block，不能把一段方便的cycle當成整份block。

| 已有輸入 | 本文使用的內容 |
| --- | --- |
| [N2全刪邊釋放](c5_excess_two_arc_spoke_closure.md#6-含-unary-的契約覆蓋與全-n2-的55化約) | 每條非框邊刪除全收；所有內點的框鄰居至多相鄰兩點；每列以有效原G作55 minimal core |
| [原分量與末端block](c5_excess_two_arc_spoke_closure.md#3-末端-block-必有私有-root-接點原-unit-unary-不存在) | C有至少兩blocks時，每個leaf C-block有私有root-contact；各C原root incidence至少二；root-free leaf-H-block的四種minor論證 |
| [分量必留與三列palettes](c5_excess_two_arc_spoke_closure.md#2-同一原分量在三列下的-block-附件一致性) | 每份原C是Gallai tree；普通私有點的實際附件受三列共同限制 |
| [連通外框K₄方法](c5_degree5_tree_components.md#1-連通外框排除-degree-4-分量的-k4) | 四條原外接方向與連通外部hub給K₅；本文另核N2的外部連通，未直接搬用單root的spoke前提 |

Gallai輸入依 [Dvořák 2018講義 Lemma7／Theorem10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
的不可染degree-list刻畫。本輪核讀定義及定理；其他N45、44、SD-A上游信任鏈
沿用前報告，未重新審核全部採納。新的block骨架、兩種minor及大小界不是該外部定理原文。

## 2. 含unary的H也只有中央block與root葉blocks

**引理1。** H有一個同時含r,s的二連通block K₀。除此以外，每個block都是
只在r或s接K₀的二連通leaf block；每root至多一個。每份原unary U恰為其中
一個leaf block刪去owner，故u≤2，若u=2則owners不同。H沒有bridge。

*證明。* 兩份原mixed各給一條r–s路，內點互斥，其聯集含同過r,s的cycle；
故r,s落在同一個K₀，且各自在K₀已有至少兩個鄰居。

先看任何不含root的leaf H-block K。其私有點沒有root鄰居，否則該原邊是
離開K的另一接點，違反leaf性。K完整落在某份C中，仍是C的block，
至多原H割點x可能是C割點。若K為bridge，私有點內度一，需三個框鄰居，
違反相鄰兩點上限。其餘K為奇環或K₄；前報告§3的原leaf minors原樣適用：
普通私有點附件由三列palettes固定，H刪去私有點仍連通，full B-touch提供
剩餘框路的hub。單block C的情形也包含在同一論證。因此這種K不存在。

現在用H的block-cut tree。任一K₀以外的leaf K必含r或s，例如r。
K₀也含r，故這兩block在block-cut tree中的唯一路徑恰為K–r–K₀。
若還有不直接接K₀的block，往遠離K₀方向走到leaf，會與上述唯一路徑矛盾。
所以所有其他blocks都是在r或s直接接上的leaves。

任何此種leaf bridge的私有端點內度一，仍違反框鄰居上限；故所有blocks二連通。
每個leaf至少使用owner的兩條內邊，K₀亦至少使用兩條。root完整degree五，
因此不能接兩個leaf blocks。刪去leaf的owner後仍連通，且只接此owner，
恰是一份原unary。反向地，K₀內不可能藏有unary：否則刪其owner會使K₀斷開。
於是所有unary與這些leaves一一對應。∎

這比「含U時H可能非二連通」更精確，但沒有把H直接宣稱二連通。
所有內點內度至少二、兩roots內度至少三；特別是內度二點不是root，
且由H無bridge，它只屬一個二連通block，不是H割點。

## 3. 每條原框邊至多承擔一個內度二點

令 D={v∈H:d_H(v)=2}。完整degree四及框附件限制給

\[
v\in D\quad\Longrightarrow\quad N_B(v)=\{a,b\}\in E(B).
\]

**引理2。** 此映射D→E(B)單射，因此|D|≤5。

*證明。* 反設不同u,v∈D同接原框邊ab，分兩種互斥情形。

**同一H-block。** 二連通圖的兩指定點同在一條簡單cycle J上（兩條內點互斥u–v路）。
full B-touch及H連通給從B−{a,b}到J的原路徑：首邊為框附件，其後全走H，
截到第一次碰J，端點記x。u,v的全部H鄰居都在J上，且只碰a,b，故x≠u,v。
取內部含x的u–v弧A，另一弧為A′。五個bags為

\[
\{u\}\cup(V(A')-\{u,v\}),\quad\{v\},\quad\{a\},\quad\{b\},\quad
(V(A)-\{u,v\})\cup V(\text{tether去框首點})\cup(B-\{a,b\}).
\]

tether中的J端點本來就在A內；全部bags互斥且連通。前兩bags沿A′相鄰，
各沿A接最後hub；四條原spokes接a,b；ab保留，hub沿剩餘框路接a,b。
因此十對皆相鄰，是原G的K₅ minor。

**不同H-blocks。** u,v各只屬自己的二連通block，均非割點。從不同blocks
各刪一點後，每個block的剩餘仍連通，原block-cut tree接合未斷，
故 X=H−{u,v}連通。取K₃,₃的兩側三bags為

\[
(\{a\},\{b\},X)\qquad\text{與}\qquad(\{u\},\{v\},B-\{a,b\}).
\]

a,b各經原spokes接u,v，亦各接剩餘框路；X接u,v的原H鄰居。
full B-touch使X還接B−{a,b}：u,v只碰a,b，不可能代替這條原附件。
九個跨側鄰接全部存在，得到K₃,₃ minor。

兩種都違反planarity，故無重複。∎

這裡跨blocks不能直接沿用「共同cycle」；第二種minor是全N2大小界必需的補步。
兩個minors都僅證非平面，不聲稱收縮後保Σ。缺full B-touch的disk負控制見§6。

## 4. 原C不含K₄；cactus的初等計數

**引理3。** 每份原C只有bridges及奇環blocks（或C是singleton）。

*證明。* C已是Gallai tree，planarity排K₅及更大clique，只須排K₄ block J。
X=G−C連通：H−C連通；若C為mixed，另一mixed的非空actual support
使H−C碰B；若C為unary，任一mixed提供這条接線。原B亦連通。

J每點完整degree四，已有三條clique邊，恰有一個外接方向。
它或直接到X，或是一條C內bridge進入J外的分支。後一分支的block tree
含一個C的leaf block，其私有root-contact由前報告保證，故分支有原路徑到X。
四個方向的C內部互斥，否則J不是maximal block。把X與這些路徑去J端點後
合成一個連通hub，J四個singleton再加hub給K₅，矛盾。∎

固定非singleton C。寫n_j為C內度j的點數，ℓ=n₁+n₂，c為奇環block數。
C內最大degree四，由cactus的邊數m=n−1+c及握手式，

\[
n=\ell+n_1+2c-2-n_4.\tag{1}
\]

把每個cycle的邊刪去，另設一個cycle節點，接其全部原頂點；原bridges保留。
得到一棵樹T（這只是計數輔助圖，不是來源替換）。每個cycle節點degree≥3；
T的所有葉都來自C內度≤2的原點：內度3或4的原點在T中degree至少二。
有限樹的degree≥3節點數至多葉數減二，故

\[
c\le\ell-2,\qquad n\le3\ell+n_1-6.\tag{2}
\]

n₁項不能丟掉：triangle每點各接一片葉的cactus有n=6、ℓ=3、n₁=3，
但3ℓ−6=3。這份負控制並非目標disk來源。

令k_C為C的原root incidences總數，d_C=|C∩D|。
若v的C內度為一，其root incidences至少二，或只有一而v∈D；
若C內度為二，其root incidences至少一，或為零而v∈D。
原因是完整degree四、至多兩條框附件，且非root只可能接r,s。
對所有C內度≤2點相加，較高內度的root incidences只增加右側：

\[
\ell+n_1\le k_C+d_C.\tag{3}
\]

因此(2)給

\[
|C|\le3(k_C+d_C)-2n_1-6\le3(k_C+d_C)-6.\tag{4}
\]

若C是singleton，完整degree四及相鄰两框點上限迫它同接r,s及兩框點，
所以k_C=2、d_C=1，(4)的較弱最右式仍成立（1≤3）。
沒有對singleton使用不存在的樹葉數公式。

## 5. 全N2的原圖大小界

恰有2+u份C，且rs不存在，兩root完整degree五，所以

\[
\sum_C k_C=10-t,\qquad \sum_C d_C=|D|\le5.
\]

將(4)對全部**原分量**相加，再加r,s，得到

\[
\begin{aligned}
|H|&=2+\sum_C|C|\\
&\le2+3(10-t+|D|)-6(2+u)\\
&\le35-6u-3t.
\end{aligned}
\]

u≤2由引理1，t≥0。因此完整N2若有反例，必在至多35個有效內點的原圖中。
此上界沒有宣稱sharp，沒有宣稱所有界內配置可實現，亦不由「有限」推出來源不存在。
之前「leaf數不限制一般block鏈長度」仍正確；這裡另有全圖內度二點≤5，
以及root incidence總量≤10，才足以控制鏈長和分量大小。

## 6. 固定控制、反例與重播

[Checker](../scripts/c5_excess_two_arc_size_bound.py)及
[產物](../artifacts/c5_excess_two_arc_size_bound/observations.json)使用NetworkX 3.5。
生成採exclusive create，沒有覆寫前輪產物或執行新來源枚舉。

| 控制 | 本輪結果及界線 |
| --- | --- |
| 既有63圖／179份C | 原edges、roots、頂點與1,790份完整16-pin fibres的精確JSON pointers／SHA／各cell大小全保留；未改座標或投影資料 |
| block分解 | 原Tarjan與NetworkX逐份相同；沒有重算原disk rotation或全染色 |
| 內度二點單射 | 4張固定圖觸發較弱的拓撲前提，triggered and holds |
| 分量大小不等式(4) | 24份原C觸發框附件及cactus前提，triggered and holds；其餘not triggered |
| 同cycle K₅ | 480份指定弧長／tether長／整框D₅控制，逐份保存原邊、五bags、bag樹與十對原鄰接；minor triggered and holds，disk來源not triggered |
| 異block K₃,₃ | 90份指定雙奇環／整框D₅控制，保存六bags及九對原鄰接；同樣都是非平面局部控制 |
| cactus計數 | 58份具名path、奇環鏈、共用點triangle鏈、補葉及分叉；57份非singleton逐式核對，singleton另處理 |
| 撤掉cactus前提 | K₄內度全三，ℓ=0，反駁無前提的計數版本 |
| 丟掉n₁項 | triangle各接一葉，反駁一般n≤3ℓ−6 |
| 撤掉full B-touch | 同一內四環的兩點同接01；保存coned graph的rotation／faces／Euler=2，確為disk；其餘框點未碰，部分完整degrees不足四，僅反駁較弱拓撲單射版本 |
| 完整Σ933／941目標來源 | 0張，not triggered；沒有新的原55來源或排除證書 |

完整fibres在本輪只作凍結引用，全部28,640個ambient cells仍可由前輪checker重算。
本輪的結構性計數不以這些fibres的數量代替共同拒絕前提。

主產物SHA-256為`a63e2bd7ef6c32c6f983b54064371cba3d46e20c32e78e222d3a335d59c46291`。
重播命令：

```bash
uv run --with networkx==3.5 python -B scripts/c5_excess_two_arc_size_bound.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python -B scripts/c5_excess_two_arc_size_bound.py --check
python3 -B scripts/c5_excess_two_arc_leaf_blocks.py --check
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
lake build
git diff --check
```

正常及`PYTHONHASHSEED=17`只讀重播均exit0、bytes及SHA相同；前輪leaf-block重播
重新核對全部28,640個pins cells，原產物SHA不變。
[故意毀損產物](../artifacts/c5_excess_two_arc_size_bound/observations_corrupt_negative.json)及
[失敗receipt](../artifacts/c5_excess_two_arc_size_bound/negative_check.json)保留，checker以
`artifact mismatch`、exit1按預期失敗。
`check_docs.py`、正式docs的DocGraph及`git diff --check`通過；
`lake build`通過（8,831 jobs，保留既有linter warnings）。Build不承擔新紙面證明。
未重跑上游44／N45／SD-A全部分類、ES／ER搜尋、原63圖rotation、pair-critical／
component-slack生成或含scratch的全工作樹DocGraph。

## 7. 精確停止點與文件傳播

**已證：** 完整目標N2的H是中央block加至多兩個root葉blocks；所有原C
K₄-free；H內度二點至多五個；有效原55圖的內點數至多35，含unary的界更低。
紙面推導依前報告已列上游信任鏈，本輪沒有另作獨立封存採納審查。

**仍OPEN：** 界內原55的同圖、同色框、完整跨列共同矛盾。既有ES／ER的
至多九內點結果不能覆蓋本輪35點界；本輪未搜尋10–35點，亦未宣稱可直接廣搜完成。
下一個窄義務是利用中央block／至多五個degree-two點與兩份mixed的完整relations，
進一步排除原55或收窄到既有已覆蓋域。N1、相鄰roots、一般單-root例外、
E-ARC2、一般出口、K∞=K≤5及新論證的Lean化均保留。

更新本報告、Kempe導覽、STATUS及N45權威入口；前報告補後續連結，synthesis只同步
原55已有大小界。README／HANDOFF研究線及路由未變，核對後不增加逐輪摘要。
其他研究線、歷史audit與舊證書不改，傳播在這些直接consumer停止。沒有commit／push。
