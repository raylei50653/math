# N2 九格殘餘統一、原55上下界與共同缺口

**後續（2026-10-12）**：[接口分割與已用色禁色規律](c5_excess_two_n2_partition_rule.md)
把本頁 `D_U≤1` 接到三列出口，排完整來源的三接線U；七個含U低接點同類模板亦一起排除。
完整 `(1,1)` 剩餘必為兩接線U、U三列diagonal全接、long三列diagonal全拒且k≥4。
九格仍七格；三個含long父情形及E-ARC2保留OPEN。

**整理發布（2026-10-11）**：相連四輪成果由[發布紀錄](history/2026-10-11-n2-55-progress-publish.md)
統一保存驗證與提交範圍；下文原生成基準及當輪「未提交」語境保留。

2026-10-11；本輪基準 HEAD `5f0979793c19e452dbb5fc7e9fe7e43cb8a991cc`。
接續 [N2 真核心排除](c5_excess_two_arc_spoke_closure.md)及
[原55大小界](c5_excess_two_arc_size_bound.md)。目前停止點見
[Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口)。

**原輪停止點：九格中的六格已有後續覆蓋，三個原55族仍 OPEN。** 本輪以共同容量及三-hub 引理
統一三族，將大小界寫成保留全部鬆弛的等式，並排除兩 unary 子族。
原55、完整 N2 來源排除及三點弧命題 E-ARC2 均維持 **OPEN**。
紙面推導、既有有限搜尋下界、局部有限控制與 Lean 分開記錄。

**後續採納（同日）**：[三列 diagonal 報告](c5_excess_two_n2_diagonal_three_row.md)
經另人獨立核對採納原 U 的任意大小三列出口，以同列兩 short 完整 lifts 排除
`(ℓ,u)=(0,1)`；與本頁 u=2 排除合成第三 relation 族原55覆蓋。
九格現為七格已有覆蓋，剩 `(2,0)、(1,0)、(1,1)` 三個含 long 情形；
共享接點與接點總數≤3的限定 long 子域亦已縮減。下文九格及四情形表保留原輪語境，
目前採納范围及缺口以後續報告及導覽為準；一般原55／N2／E-ARC2仍 OPEN。

**再續（同日）**：[long 同列同步與 tree 化約](c5_excess_two_n2_long_synchrony.md)
排兩份 long 都 k≤3、無 U 且 long 為全葉接點 tree 的子域；含 U 的低接點
異類 Eq／Diff masks 排除，同類剩七個必要弧模板。沒有新增 Δ 下界或父族 closure。

## 1. 九格對應與完整契約

使用者已確認，九格指 [E4 §4.3](../artifacts/c5_excess_two_e4/REPORT.md#43-n2-精確殘留)
的三個參數化 relation 族，乘三個 core 層；45／54 合為一層。
令 ℓ 是原 long mixed 數，u 是原 unary 數。

| 原 relation 族 | 兩-root44 | 45／54 | 原55 |
| --- | --- | --- | --- |
| ℓ=2,u=0 | 已由既有44覆蓋排除 | 完整 N2 真核心定理排除 | OPEN |
| ℓ=1,u=0或1 | 已由既有44覆蓋排除 | 同上 | OPEN |
| ℓ=0,u=1或2 | 已由既有44覆蓋排除 | 同上 | OPEN；u=2子族見§3 |

這是九個分類格，並非九份具名可實現來源。拆開參數後原本有五個 (ℓ,u) 組合；
不能把歷史殘留表當成目前仍存活的九個分支。

以下所有新推導均採用 [spoke 報告 §1](c5_excess_two_arc_spoke_closure.md#1-完整來源前提與依賴)
的**全部**契約：有限簡單 induced-C₅ disk、有序 B、完整 Σ933／941 或整圖共同
D₅ 像、T4全收、每條非框邊Σ-critical、ε=2、有效 H 連通且 full B-touch；
恰兩個非相鄰完整 degree5 roots r,s，其餘有效內點完整 degree4；
H−{r,s} 恰兩份原 mixed P,Q，其餘 unary；原 pieces one-sided，mixed 支援非空。
共同搬運後 q₀=01212、q₁=01202、q₃=01021 拒絕。
原 contacts、shared contacts、ownership、實際附件、rotation、bridges、旁支、
共同字面色框、完整 relations／空 fibres／full lifts 均保留。
有效大小不計自由孤立座標，其四色乘積因子仍保留。

不能只保留三列拒絕而丟掉完整 Σ，也不能把結果搬至 N1、相鄰 roots、932
或一般 N2 契約之外。既有44／N45／SD-A／Gallai信任鏈沿用各權威報告。

## 2. 三族共享的不變量與一條共同容量引理

既有共同結構已足以取代六格的逐案排除：每條原非框邊刪除全收十列，
每個拒絕列均以有效原 G 自身為唯一55 minimal core；每個內點至多接兩個
相鄰框點。H 是含 r,s 的中央二連通 block 加至多兩個 root 葉 blocks，
每側至多一份 unary；原 C 是 bridge／奇環 cactus，且全 H 內度二點至多五個。
這些是 [spoke 定理3](c5_excess_two_arc_spoke_closure.md#6-含-unary-的契約覆蓋與全-n2-的55化約)
及 [大小界引理1–3](c5_excess_two_arc_size_bound.md#2-含unary的h也只有中央block與root葉blocks)
的同圖結論。

以下 [4]={0,1,2,3}。固定同一列 qᵢ。用完整 unary tuples 定義 owner 禁色 F_U(i)，
用完整 mixed tuples 定義接受有序色對 A_C(i)。記

\[
m_r=k_P^r+k_Q^r,\qquad
D_r^u(i)=\sum_{U\text{ owned by }r}(k_U-|F_U(i)|),
\]
\[
E_r(i)=[4]\setminus\left(q_i(N_B(r))\cup\bigcup_{U\text{ owned by }r}F_U(i)\right).
\]

另令 O_r^u 為具名spoke singleton factors與完整F_U factors的大小總和減其聯集大小。
對每個 b∈E_s(i)，令 G_C(i,b)={a:(a,b)∉A_C(i)}，V=G_P∪G_Q，並設

\[
\delta=\sum_{C=P,Q}(k_C^r-|G_C|),\quad
o=|G_P|+|G_Q|-|V|,\quad \lambda=|V\setminus E_r(i)|.
\]

**共同原55引理。** 對 i∈{0,1,3}、兩種 root 順序及每個 b∈E_s(i)，

\[
\boxed{O_r^u(i)=0,\quad |E_r(i)|=m_r-1+D_r^u(i),\quad
D_r^u(i)+\delta+o+\lambda=1.}
\]

所有項非負，D_r^u(i)∈{0,1}；無 unary 側 D_r^u=0，兩側 E 均非空。

*證明。* 每側至多一份 unary，原 spokes 在 proper row 下色互異。
刪某條 spoke 的同列染色中，root 必取被刪 spoke 的框端色，否則可恢復原邊。
原 unary 完整保留，故其禁色避開全部 spoke 色。因而 external／unary factors
無重疊，O_r^u=0。原 degree 計數 t_r+k_U+m_r=5 給
|E_r|=m_r−1+D_r^u≥m_r−1≥1。
完整拒絕給 E_r⊆V，[B-C2](c5_phase_b_common_lemmas.md#32-b-c2任意两自由roots的條件逐欄容量定理)
取 χ=0、degree5 即得等式。∎

這統一了三族的容量分析，但右端是 **1**；45降度側的右端才是0。
各列及各欄的 witness 可以不同，等式不給跨列費用不重用，不能把三列的費用
相加成同一份 degree 超額。完整證明及量詞核對見
[共同接口分析](../audits/2026-10-11-n2-residual-unification/arc-gap/REPORT.md)。

## 3. 共同三-hub 引理與兩 unary 子族排除

**共同 singleton 引理。** 在§1全部契約下，若任一原 mixed P 的 actual support
恰為 {h}，則必有 u=t=0。換言之，原圖只要有 unary 或任一 root-spoke，
兩份 mixed 的實際支援都至少兩點。這是新紙面推論，已作獨立量詞及原 bags 核對。

*證明。* Q為另一份原 mixed，其 actual support 非空。
G−P全收，故取同一原拒絕列β的一份完整外部染色ψ；它不能補回P。
P 的所有外鄰恰在 {r,s,h}，保留原 contacts，不合併共享頂點。

若有原 unary U，共同交換 roots 使其 owner 為r，取

\[
R=\{r\}\cup U,\qquad S=\{s\}\cup Q,\qquad T=B.
\]

三 bags 互斥且連通；R–S由原r–Q contact，R–T由U的實際框附件，
S–T由Q的實際框附件。U支援至少三點，Q支援非空，這些邊均確實存在。
N(P)與三袋的交集各恰為r、s、h，所以ψ在各交集上常色。
若無 unary 但有原 spoke，共同交换 roots 使r有spoke，改取R={r}，
同一S,T仍成立；R–T改由該原spoke。

若三個 pin 色中有相同者，只合併同色的 bags。三袋兩兩相鄰，合併後仍連通，
不同色 bags仍互斥且兩兩相鄰，在N(P)交集上常色且異色。
這正满足 [hub 原則定理B](c5_unary_shield_budget.md#4-定理-bhub-原則)
的全部前提：P連通，每點完整degree4，ψ是原G−P合法染色而不可延拓。
故得到原G的K₅ minor，違反disk平面性。∎

只要求ψ在bag與N(P)的交集常色，**沒有**假設整袋同色或重新染色外部。
這個證明不旋轉框，不用45／54 derivative，也不需singleton incidence上界。
即使使用共同D₅搬運，拒絕列與全部原資料也須一起搬運。

**推論1（兩 unary 排除）。** u=2時盾弧預算先迫兩 mixed 都short，
共同singleton引理又迫兩份都是真框邊pair。因此四份原pieces須收

\[
2+2+1+1=6>5
\]

條互斥原盾邊，矛盾。故完整目標N2的原55滿足 **u≤1**。
這關閉第三族中u=2子族，未關其u=1或其他原55。

**推論2（含U的支援統一）。** u=1、ℓ=1時，short必為真pair，
原U／long／short盾弧恰為(2,2,1)，U與long支援各恰三個連續框點。
它们的完整relations仍須保留，這個必要模板不提供原55的延拓證明。
u=1、ℓ=0時兩short都是真pair，U盾弧只可能長2或3。

逐條來源與独立核對見
[structure 報告](../audits/2026-10-11-n2-residual-unification/structure/REPORT.md)及
[獨立審閱](../audits/2026-10-11-n2-residual-unification/arc-gap/independent_review.md)。

## 4. 原35上界與既有下界：直接矛盾及精確鬆弛

**下界層次。** [ES](c5_excess_two_finite_search.md)／
[ER](c5_excess_two_independent_search.md)完成全部 NA 型 k≤9，無目標來源。
本契約的 degree、spoke cap、H連通、disk與criticality均在該有限域內，
因此沿用這份有限雙實作證據，目標反例必有 |H|≥10。
這是既有有限覆蓋的下界，不是本輪新來源搜尋或 Lean 無界定理。
既有 ε≥2 恰與本契約 ε=2 相容；完整 ε≥3 下界仍未證，不能借用猜想 E 得矛盾。
44身份的 ℓ+2u≤3 也不能直接搬至原55。

中央 block 及框附件先給 t≤4−u；保留舊 u≤2 的算術檢查如下。

| u | 原容許 t | 原上界隨 t 變化 | 與 H點數≥10 的交集 |
| ---: | --- | --- | --- |
| 0 | 0…4 | 35,32,29,26,23 | 10…(35−3t) |
| 1 | 0…3 | 29,26,23,20 | 10…(29−3t) |
| 2 | 0…2 | 23,20,17 | 算術有交集；本輪§3另作結構排除 |

原上界直接≤9，等價於 2u+t≥9；上述原容許域至多6，故**單靠原上界無直接
矛盾區間**。35−6u−3t=10亦無整數解。一般真正已證下界 L 才能排除
35−6u−3t<L 的區間；不能為消去分支假設尚缺的 L。

把原 cactus 計數中丟掉的量保留，可得更有用的共同式。
對非singleton原 C，記 n₁,C、n₄,C 為 C 內度1、4點數，
e_C 為 C 內度≤2點數，c_C 為奇環 block 數，d_C=|C∩D|，k_C為原root incidences。
設

\[
\alpha_C=k_C+d_C-(e_C+n_{1,C})\ge0,\qquad
\gamma_C=e_C-2-c_C\ge0,
\]
\[
\sigma_C=3\alpha_C+2n_{1,C}+2\gamma_C+n_{4,C}.
\]

對 singleton 另定 σ_C=2（此時 k_C=2,d_C=1）。原握手式逐项給

\[
|C|=3(k_C+d_C)-6-\sigma_C.
\]

令 d=|D|≤5，**不等式精化為原圖等式**

\[
\boxed{|H|=35-6u-3t-\Delta,\qquad
\Delta=3(5-d)+\sum_C\sigma_C\ge0.}
\]

結合有限下界10，可直接排除的條件區間恰為

\[
\boxed{\Delta\ge26-6u-3t.}
\]

存活必要條件是 Δ≤25−6u−3t；等號只迫 |H|=10，不給矛盾。
u=0時排除門檻依 t=0…4為26,23,20,17,14；
u=1時依 t=0…3為20,17,14,11。
缺少的是**所有剩餘來源必達這個鬆弛門檻**的結構證明。
算術控制及精確式重算見 [bounds 報告](../audits/2026-10-11-n2-residual-unification/bounds/REPORT.md)。

## 5. 剩餘四個參數情形的精確缺條件

**後續狀態**：本節保留原輪四情形表；`(0,1)` 已由
[獨立三列出口採納](c5_excess_two_n2_diagonal_three_row.md#2-unary-出口的獨立採納)排除。
目前三個含 long 情形及其限定縮減見該報告§4。

設未用色 D=3；三個指定拒絕列都只用0,1,2。完整原 joint 為

\[
J_G(i)=(E_r(i)\times E_s(i))\cap A_P(i)\cap A_Q(i).
\]

反駁共同三列拒絕須獨立證至少一個 i∈{0,1,3} 的 J_G(i) 非空，且有原pieces的完整
lifts。下表提供各情形足夠的較窄橋梁；未聲稱它們必要或已證。

| (ℓ,u) | 尚缺的充分橋梁 | 現有工具的限制 |
| --- | --- | --- |
| (2,0) | 同一指定列兩 long 都接受(D,D)，或另一共同有序 pair | 各 relation 分別非空不足以保交集 |
| (1,0) | 同一指定列 long 接受(D,D) | short 已全收 diagonal，long 尚無該結論 |
| (1,1) | 同一列 D∉F_U 且 long 接受(D,D)，或完整 off-diagonal joint 非空 | unary escape 與 long 延拓須在同列同pins成立 |
| (0,1) | 至少一指定列 D∉F_U | 否則三列都需同一原U禁D；尚缺排除此共同palette模式的證明 |

**原輪後續候選記錄（現已另人獨立採納）：** [N2-55-U-THREE-ROW-ESCAPE](c5_excess_two_n2_unary_three_row_escape.md)
完整覆蓋k=2／3 unary的單block／兩leaf／三leaf，提出最後一列所需的三列D escape。
若採納，同一列以U lift及兩short的完整(D,D) lifts排(0,1)；已採納表仍保留，
因另人獨立紙面核對未執行。局部42份U觸發並成立、全部97份原U完整fibres重算相符，
target來源仍not triggered。含long的(1,1)仍需long在U escape的同一列接受(D,D)，
不能跨列拼接；其餘兩個long情形及Δ门檻不變。

另一條充分路線是證§4的 Δ 門檻。中央 block 與各 C 的 palettes 如何限制
三列 joint 或 Δ，目前尚無統一的跨列不重用定理。
SD-A只處理一個完整degree5；原 G 是雙degree5，不能直接套用。
刪spoke後雖為45／54，卻已全收，SD-A拒絕前提也不成立。

**三點弧命題的作用。** 若一般 E-ARC2 已獨立證成，當然能排除本目標 N2，
因 {0,1,3} 不含於任何連續三點弧。但本子域正是證 E-ARC2 的剩餘義務之一；
先假設 E-ARC2 再取得 joint／不存在性／缺條件，是循環。
它本身也未提供中央 block、palette、共同pins或鬆弛量的結構陳述。
合法下一步是獨立證上述較弱橋梁或 N2 限定三點弧定理，保留一般 N1／相鄰／
單-root例外；完整母目標仍見 [synthesis §8.1](c5_research_synthesis.md#81-猜想-e超額拒絕定律)。

## 6. 驗證、证据分層與傳播停止點

獨立審閱已接受§2共同容量、§3三-hub／兩unary子族排除、§4鬆弛等式與門檻，
並核對§5三點弧的邏輯方向。驗證證據見
[獨立審閱](../audits/2026-10-11-n2-residual-unification/arc-gap/independent_review.md)及
[本輪receipt](../audits/2026-10-11-n2-residual-unification/verification.json)。
初稿再次D₅搬運後誤保字面q₀的問題已記錄；現行三-hub證法取消該搬運，
舊較繁候選及兩份checker的首次生成失敗紀錄均保留。

| 本輪檢查 | 實際結果及界線 |
| --- | --- |
| bounds checker normal／seed17 | exit0、301,208 bytes、SHA相同；12份整數參數profile、58具名cacti、179原C，其中24份觸發精確鬆弛式並成立；目標0觸發 |
| capacity checker normal／seed17 | exit0、SHA相同；19固定原圖／19同列q-minimal拒絕列、38root方向、74容量欄成立；目標0觸發 |
| bounds毀損副本 | root另重播，按預期exit1、artifact mismatch；副本及失敗receipt保留 |
| 既有size-bound／leaf-block normal | exit0、舊SHA不變；leaf重算28,640 ambient pins cells，含3,372空fibres；沒有改舊證書 |
| ES／ER有限下界 | 讀回NA七層的既有hash、集合計數與Q／Σ分布；沒有重跑來源生成或搜尋 |
| 文件／build | check_docs、正式docs DocGraph、git diff --check通過；lake build通過8,831 jobs，保留既有linter warnings |

bounds產物SHA為`156117b8a3178fc9972311d7d84c7e990bc7d8a91c510b309f5bbff703ca7e00`；
capacity產物SHA為`a2e379f7f3676310a56ebcbfecf50fca7314dac17343a8c72ebf65bace0e651f`。
完整分工為 [structure](../audits/2026-10-11-n2-residual-unification/structure/REPORT.md)、
[bounds](../audits/2026-10-11-n2-residual-unification/bounds/REPORT.md)、
[arc-gap](../audits/2026-10-11-n2-residual-unification/arc-gap/REPORT.md)。

```bash
python3 -B audits/2026-10-11-n2-residual-unification/bounds/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-n2-residual-unification/bounds/checker.py --check
python3 -B audits/2026-10-11-n2-residual-unification/arc-gap/check_capacity.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-n2-residual-unification/arc-gap/check_capacity.py --check
uv run --offline --with networkx==3.5 python -B scripts/c5_excess_two_arc_size_bound.py --check
python3 -B scripts/c5_excess_two_arc_leaf_blocks.py --check
python3 -B scripts/check_docs.py
python3 -B tools/docgraph --include 'docs/**/*.md' check
lake build
git diff --check
```

局部有限控制不构成目標來源實現或任意大小完備枚舉。完整目標仍 `not triggered`；
本輪子族排除依紙面及獨立邏輯核對。沒有搜尋10–35內點，沒有新Lean theorem，
build亦不形式化這些新紙面推導。未重跑上游全部44／N45／SD-A分類、原來源rotation、
ES／ER生成或全工作樹含凍結副本的DocGraph。

**文件傳播。** 本輪子族closure只限完整§1的u=2原55；singleton支援引理另給
必要限制。更新本報告、大小界後續入口、N45§2.16／停止點、Kempe guide、STATUS及
已有直接synthesis摘要。README／HANDOFF研究線路由未變，核對後不改；
Phase B的一般B-C2與OPEN跨列義務仍正確，E4原表保留其歷史範圍，旧audit／證書bytes不改。
傳播停止於這些直接consumers，沒有推升父N2或E-ARC2，也沒有新增發布流程。

**Remaining OPEN：** u=0／1的原55共同矛盾、完整 N2、N2契約外cores、
N1／相鄰／單-root例外、E-ARC2、一般出口及 K∞=K≤5。
本輪未要求 commit／push，不作遠端發布。
