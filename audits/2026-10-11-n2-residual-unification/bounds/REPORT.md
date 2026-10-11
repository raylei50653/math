# N2 原55：大小界與同域下界的衝突核對

2026-10-11。獨占新增目錄 `audits/2026-10-11-n2-residual-unification/bounds/`；
BASE HEAD `5f0979793c19e452dbb5fc7e9fe7e43cb8a991cc`。
只讀共享 docs/scripts/artifacts；沒有修改上游、來源圖搜尋、commit 或 push。

**結論：既有同域有限結果給有效 `|H|≥10`，與原 `35−6u−3t` 上界在全部
必要 incidence/spoke 參數域均有交集，沒有直接大小矛盾。** 保留原計數的
全部 slack 可得到一條精確等式及明確整數衝突門檻；目前沒有證成足够大的
共同 slack。原55、一般N2及E-ARC2保持 **OPEN**。

## 1. 同域契約及可使用的下界

本報告完整採 `docs/c5_excess_two_arc_spoke_closure.md:24–40` 與
`docs/c5_excess_two_arc_size_bound.md:23–34`：同一有限簡單 induced-C₅ disk、
具名 ordered B、完整Σ933／941或整圖共同D₅像、全部非框邊Σ-critical、ε=2、
full-B-touch 的連通有效H、非相鄰完整degree5 roots r,s、其餘完整degree4、
兩份原mixed、其他原unary、one-sided及非空mixed actual support。
自由孤立座標不計入有效H；其完整染色乘積因子仍保留。

目前真正能搬到這個有效H點數域的最強既有下界是

\[
|H|\ge10. \tag{L}
\]

它依靠已完成的有限NA域而非新的任意大小定理。ES的完整定義在
`docs/c5_excess_two_finite_search.md:15–30`；ER逐項同域在
`docs/c5_excess_two_independent_search.md:13–20`。本N2契約滿足這些前提：
兩roots不相鄰、degree prescribed 5/5/4、H連通、T4全收、非框邊critical、
每點至多兩spokes更強於有限域三spokes上限。
933的Q={0,1,2,3}有 `|Q|+c(Q)=5`，941的Q={0,1,3}有
`|Q|+c(Q)=5`；共同D₅搬運保持此數。
有限NA的k≤9沒有這些完整Σ，因而反例的有效k至少10。
ES的排除結果及任意大小界線見
`docs/c5_excess_two_finite_search.md:369–378`、`:484–486`；
ER的獨立一致結果及界線見
`docs/c5_excess_two_independent_search.md:8–9`、`:140–148`、`:199–200`。

本次checker只讀回NA k=3..9的兩套凍結結果，逐層核ES檔hash與ER保存值、
一致性、crit數及全部NA Q／Σ summaries；沒有重跑兩套來源生成器、全部
刪邊染色或嵌入證書。k=1,2由prescribed degree/spoke限制為空，已有說明見
`docs/c5_excess_two_independent_search.md:98–99`。

以下數值不能升格為這個H的點數下界：

| 已有量 | 正確適用範圍 | 本次結論 |
| --- | --- | --- |
| ε≥2 | degree excess；兩roots的總超額已恰2 | 不是 `|H|≥2` 以外的新點數估計，更不是ε≥3 |
| 原框support至少四、全圖full-B-touch | 框點數／支援跨度 | 不是內點數≥4或≥5；一點可碰兩框點 |
| 每份C的root incidence≥2 | 原 `H−{r,s}` 分量，見spoke closure:122–131 | 加總限制u,t；不能把每條root邊當不同原內點，mixed可有shared contact |
| 固定root禁色容量≤k | 完整原contact tuple的條件禁色集，见capacity:110–125 | 不是k個互異全圖點的跨分量／跨列額外下界 |
| 44身份的 `ℓ+2u≤3` | omitted mixed11及retained44都另證support≥2；见nonadjacent two-mixed core44:43–68 | 原55未有這兩份身份，不可移用；一般short mixed的actual support可能singleton |
| 一般原盾弧 | 原one-sided pieces、full B-touch、criticality，见unary shield:101–128 | unary每份至少兩框邊；long每份至少兩；short pair一；short singleton可零，不能每份mixed一律收一邊 |

在現有點數估計中，純incidence的粗下界也可寫成
`|H|≥2+ceil((10−t+2u)/2)`：兩份mixed每條root incidence至多由同一點
同時承擔兩root角色；unary每點只能承擔一條owner incidence且總unary
incidence≥2u。這個下界在本表都不超過9，因此(L)更強。

## 2. 允許的必要參數域與原上界核對

由全部非框邊刪除全收，roots亦至多碰兩個相鄰框點；
`docs/c5_excess_two_arc_spoke_closure.md:219–233`。
故 `t_r,t_s∈{0,1,2}`。原H的中央block和至多兩個root葉blocks，且
u=2時owners不同，見 `docs/c5_excess_two_arc_size_bound.md:48–75`。
有unary的owner，兩份mixed各至少一條原內邊、unary至少兩條原內邊，
所以其內度≥4，完整degree5迫該owner `t_owner≤1`。因而：

\[
u=0:\ 0\le t\le4;\qquad
u=1:\ 0\le t\le3;\qquad
u=2:\ 0\le t\le2. \tag{P}
\]

(P)是必要的incidence screen，沒有宣稱每個split可實現為完整目標來源。
相較只記t≥0，這足以去掉不可能的大t偽衝突。
原上界的推导在 `docs/c5_excess_two_arc_size_bound.md:134–194`：
非singleton的cactus握手式、cycle incidence tree、root incidence加degree-two
點計數，逐份原C相加再加兩roots。singleton另按k=2,d=1，沒有使用不存在
的樹葉式。`Σk_C=10−t` 中沒有rs邊，`Σd_C=|D|≤5` 中roots不在D。
本輪獨立核算未發現這條上界的代數錯誤。

| u | t | 原上界U₀ | 用(L)後未排除的有效H點數 | Δ相等點：H=10 | Δ整數衝突開始：H≤9 |
| ---: | ---: | ---: | --- | ---: | ---: |
| 0 | 0 | 35 | 10–35 | 25 | 26 |
| 0 | 1 | 32 | 10–32 | 22 | 23 |
| 0 | 2 | 29 | 10–29 | 19 | 20 |
| 0 | 3 | 26 | 10–26 | 16 | 17 |
| 0 | 4 | 23 | 10–23 | 13 | 14 |
| 1 | 0 | 29 | 10–29 | 19 | 20 |
| 1 | 1 | 26 | 10–26 | 16 | 17 |
| 1 | 2 | 23 | 10–23 | 13 | 14 |
| 1 | 3 | 20 | 10–20 | 10 | 11 |
| 2 | 0 | 23 | 10–23 | 13 | 14 |
| 2 | 1 | 20 | 10–20 | 10 | 11 |
| 2 | 2 | 17 | 10–17 | 7 | 8 |

**沒有額外slack條件時，表內沒有矛盾或相等強迫。** 原上界本身≤9的整數
条件是 `2u+t≥9`；(P)給 `2u+t≤6`，完全不會觸發。
原上界本身等於10也不可能，因 `35−6u−3t≡2 (mod 3)`。
上界的模3只是粗估值，不可據此限制實際H的模3。

## 3. 保留全部slack的精確等式

對非singleton原C，採上游記號：n_j為C內度j點數、ℓ_C=n₁+n₂、
c_C為奇環block數、k_C為原root incidence數、d_C=|C∩D|。定義

\[
a_C=k_C+d_C-(\ell_C+n_{1,C})\ge0,\qquad
b_C=\ell_C-2-c_C\ge0.
\]

上游(1)保留所有項，逐式代入給

\[
\begin{aligned}
|C|&=\ell_C+n_{1,C}+2c_C-2-n_{4,C}\\
&=3(k_C+d_C)-6-\delta_C,\\
\delta_C&=3a_C+2n_{1,C}+2b_C+n_{4,C}\ge0.
\end{aligned}
\]

singleton原C則k_C=2,d_C=1、|C|=1，故精確 `δ_C=2`。
不為singleton定義上面的a_C,b_C或n₁葉數式。
全圖因此满足

\[
\boxed{|H|=35-6u-3t-\Delta,\quad
\Delta=3(5-|D|)+\sum_C\delta_C\ge0.} \tag{S}
\]

這是精確等式；丟掉Δ才是舊上界。特別可以保留較容易觀察的
`−2Σ_non-singleton n₁−2s₀`，其中s₀為singleton原分量數。
但沒有將別處的候選／假設當成對全域Δ的新正下界。

结合(L)，每份實際反例必满足

\[
\Delta\le25-6u-3t.
\]

因此一旦另證同域結構強制
`Δ≥26−6u−3t`，就可直接與既有有限下界矛盾；
`Δ=25−6u−3t`只强制H=10，仍在未搜尋域，不能寫排除。
表中列了每個整數門檻。所缺的是同一完整來源的Δ下界，並非更多整數算術。

## 4. 另路收窄的界線

同批結構工作另提出u=2的支持預算／低incidence singleton-support mixed
候選。其可移植輸入的量詞見 `audits/2026-10-09-n45-u/REPORT.md:176–205`：
任意兩roots、full-B-touch、原degree4 mixed、H−P連通、Σ-critical原contact、
k_P≤3，则actual support≥2，不需要44身份。
若结合两unary互斥盾弧得其中一mixed只有singleton actual support，則其
k≥4；配另一mixed k≥2和两unary各k≥2，10−t預算迫t=0且各項飽和。
這條更強候選由結構worker交獨立審查；本表刻意保留完整必要screen(P)，
不以尚未驗收的收窄或排除删除u=2行。若採納u=2全排，剩餘u=0/1的
點數衝突結論仍相同：沒有無額外slack條件的矛盾。

小型unary尺寸的新分析（例如|U|≥3、≥4）也沒有加入本次權威下界或checker
參數表，沒有借尚未獨立採納的論證宣布任何來源排除。

## 5. 控制、重播與精確停止點

[獨立checker](checker.py)只用標準函式庫，沒有import歷史producer或
NetworkX。由凍結原vertices/edges以另寫的Tarjan DFS重新求blocks、cycle、
degree counts，核對所有58份已保存具名cacti（57非singleton精確計數式成立，
singleton另列）。這58份只有cactus計數附件，沒有root incidence／disk來源
契約；完整δ_C來源式在這層為 **not triggered**。

另重讀63圖／179原C的完整原邊及實際root adjacency，重算k_C,d_C；
框附件＋odd cactus局部前提觸發24份，24份精確δ_C等式均 **triggered and holds**。
其餘155份的完整incidence版本為 **not triggered**。
完整目標來源仍0份 **not triggered**。既有完整fibres只凍結引用，沒有重算，
沒有將24份局部式觸發冒充原55來源排除。

[主產物](observations.json)保存輸入路径／bytes／SHA、全部具名控制與來源
JSON pointers、12份必要(u,t)行、ES/ER凍結讀回以及OPEN欄位。
SHA256 `156117b8a3178fc9972311d7d84c7e990bc7d8a91c510b309f5bbff703ca7e00`。

```sh
python3 -B audits/2026-10-11-n2-residual-unification/bounds/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-n2-residual-unification/bounds/checker.py --check
```

兩次exit0，bytes／SHA相同。最初生成因ROOT父目錄索引多一層而失敗，未寫產物；
修正為math根後採exclusive-create生成。此錯誤及負控制另保留於
[重播receipts](validation.json)。故意改動第一行上界的副本保留；對副本重播
預期 `artifact mismatch`、exit1，沒有覆寫正式產物或上游舊證書。

**停止點：** 上界代數及全部可用下界域已分清，直接大小衝突區間為空；
精確slack的條件衝突／相等門檻已封存。要完成來源排除仍須證同圖共同Δ
下界或完整mixed relations的跨列矛盾。本次沒有新Lean theorem、未重跑全部
ES/ER生成，未搜尋10–35點；原55、N2及三點弧命題仍OPEN。
