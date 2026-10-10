# N45-A：共同前提、原 unit 省略與搬用邊界稽核

2026-10-09。執行者狀態：**完成，含 provenance finding；待監督端交叉驗收**。
本輪只審 BASE 權威來源，未讀取或驗收 N45-S／U／J 的新輸出，未推新來源排除。

**結論：指定共同化約可以在下列精確前提下搬用。一般 N2 的兩 mixed
支援下界仍是缺口；U4 的 44 下界和 E4-D 的重色前提不能直接填入 45／54。
兩個 E4 歷史 byte replay FAIL 均重現，差異只在 E3 REPORT provenance；
fresh 證書的非 provenance payload 與原證書相同。**

## 1. 凍結輸入、授權與交付

- BASE／獨立 source worktree HEAD：`dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。
- Source worktree：`/tmp/math-n45-a-20261009`，detached；接手與結束均無檔案變更。
- 唯一輸出目錄：`/home/ray/developer/ai/math/audits/2026-10-09-n45-a/`。
- 交付未提交，逐檔 hash 見 [MANIFEST.json](MANIFEST.json)；沒有 commit、push、PR、對外訊息或 sub-agent。
- [inputs.json](inputs.json) 凍結 136 份 BASE 檔案的實讀路徑、SHA256、bytes
  及 Git blob identity；每份先與 `git show BASE:path` 比對。
  文件檢查工具及其掃描來源另見 [validation-inputs.json](validation-inputs.json)；
  合併去重後共720份來源，結束核對全部零 byte 漂移。
- 任務文件 [N45 派工紀錄](../../docs/history/2026-10-09-n2-45-54-parallel-tasks.md)
  是主工作樹既有 untracked 指令，不在 BASE。其 hash 與主工作樹兩份既有修改另列，
  不作數學來源。數學只讀 BASE，沒有混用主工作樹的 STATUS／guide 修改。
- 本輪遵照派工限制只寫自己的 audit；共同 report／guide／STATUS 與舊 artifact 不改。
  [checks.json](checks.json) 記錄實跑命令、exit、seed、logs、未跑項與輸入零 byte 漂移。

主要交付：[獨立 checker](checker.py)、[有限證書](certificate.json)、
[claims 與 findings](claims.json)、[provenance 差異](provenance-comparison.json)、
[fresh core 證書](fresh-core-constraints.json)、[fresh reductions 證書](fresh-reductions.json)。
後兩者由原 checker 在新路徑 exclusive-create；不充作獨立數學驗證。

## 2. 全部量詞與共同前提

除特別明列較弱局部前提者，以下 G 量詞為**任意大小有限**來源：

1. G 有限簡單，B=(b0,…,b4) 為有序 induced C5 的 disk 外框；所有完整
   Σ 列共享字面色框。完整 Σ(G)=933／941，或同一整圖 D5 像。
2. 每條非框邊對 G 自己的完整 Σ strict-critical；有效內點忽略孤立點，
   `ε(G)=Σ(deg_G(v)−4)=2`，degree 包含全部原框附件。
3. 恰兩個完整 degree5 roots z,w，zw 不存在；其他有效內點完整 degree4。
   H−{z,w} 的完整原分量恰有兩份 mixed P,Q，其餘為 unary。
4. 共同搬運後 q0=`01212`/index6、q1=`01202`/index4、q3=`01021`/index1
   均拒絕；T4 indices={2,5,7,8,9} 均接受。941 接受 q2/index3、q4/index0；
   933 拒絕 q2 並接受 q4。三列前提本身也容許 932／940，不能替代完整目標。
5. 任一拒絕 β 的 M 是保留 B 的 inclusion-minimal β-obstruction；M 的
   β-criticality、自己的 Σ-criticality 與 G 的 criticality 分開。
   本批只研究 M 的原 root degrees=(4,5)/(5,4)。
6. 保留原頂點、原邊、ordered distinct/shared contacts、ownership、attachments、
   actual support、bridges、cyclic order、完整 relations、空 fibres 與 full lifts。
   Root 交換同時交換全部角色；D5／S4 只共同搬運整圖。

X 另指刪除**一條原 spoke**或**一整份 root incidence=1 的原 unary**所得圖。
`capacity-one` 描述原 incidence，不預設每列 F_U 為 singleton，也不預設 X critical。

各 CLAIM 都適用 933、941 及共同 root 交換；局部工具的量詞／更弱前提另列。
E2、全四分類及 U1–U4 是具名既有依賴，本輪未重審其全部上游有限分類。
外部 Gallai／degree-list／K5 不可平面性沿 BASE 論證標示；本輪沒有重新審文獻、
新 Lean theorem、普通 Lean 證明或 native_decide 證書。

## 3. 逐項 paper 稽核與可用依賴

### N45A-01：精確來源、triple-critical、全框及刪 root

**判定：成立且可搬用。** 對每個 §2 的 G，每條非框邊刪除必新接受
q0／q1／q3 至少一列；G 碰齊五框點；G−z、G−w 均接受全部十列。
因此任一拒絕列的任一 minimal core 都含兩個原 roots。

依據：E3 [REPORT §2.1](../../artifacts/c5_excess_two_e3/REPORT.md#21-共同-triple-critical-化約)
L88–111；[nonadjacent notes §2](../../artifacts/c5_excess_two_e3/nonadjacent_notes.md#2-原分量刪-root-與例外全部可直接移植)
L39–65；[E2 §2](../../artifacts/c5_excess_one_e2/REPORT.md#2-一般-σ-minimal-來源的前提推導)
L49–77；[原 root 刪除 §2–3](../../docs/c5_excess_two_root_deletions.md#2-刪-root-與具名-unary-側的完整-σ-恆等式)。

稽核理由：保三個指定拒絕列的 minimal 子圖若是 proper，ε 飽和等式使
其 ε≤1，而它接受 T4、自己 Σ-critical、仍拒絕非相鄰 singleton 位置，
違反 E2。全框由至少兩個不同拒絕列推出。m=2 給每側 mixed incidence≥2，
原 side root degree≤3；刪另一 root 後原 contact 的 strict slack 填回整份 piece。
三列同時 critical 不表示 G 對每個 q 都 minimal，也不能拼不同 q 的 cores。
證據：paper＋E2 既有紙面／末端證書依賴；本輪 108 次刪 root 有限核對。
精確三列的有限來源前提在本輪 54 圖全部 **not triggered**。

### N45A-02：整 piece 飽和與 45／54 省略分類

**判定：成立且可搬用。** 對每個 §2 的 G、每個拒絕 β 及每份 M，
retained 原 degree4 點的 M-degree≥4，故其全部原 incident 邊保留。
沿原 piece 連通傳播，每份 piece 全取或全不取，所有 contacts／附件不變。
若 M degrees=45／54，恰省 degree 下降侧的一條 spoke 或一整份 incidence-one
unary；兩份 mixed 全保留。若 degrees=55，M=G。

依據：[E3 notes §5](../../artifacts/c5_excess_two_e3/nonadjacent_notes.md#5-每列-q-core-的完整原省略分類)
L119–170；[E4 §6](../../artifacts/c5_excess_two_e4/REPORT.md#6-完整原-relation-的參數化交付與-core-身份)
L248–300；[CORE §6](../../artifacts/c5_excess_two_e4/CORE_CONSTRAINTS.md#6-完整原-relation-的精確殘留)
L147–182。

兩-root44 的 incidence 分類先由全四 core 分類推出；固定完整目標下的
44 身份排除另沿 [U4 §1](../../docs/c5_excess_two_nonadjacent_two_mixed_core44.md#1-同一原圖與原-mixed11-省略)
及其 U1–U3 依賴。這個排除只關 44，不能升成沒有 45／54／55 或沒有來源。
證據：paper；本輪驗 60 份保存 core occurrences 的 rejection、逐邊 β-criticality、
完整 Σ、degree 及原省略身份。12 份 45／54 均屬 **N1**，N2 的此身份 **not triggered**。
沒有獨立重新枚舉所有 cores，故「唯一／完備」仍屬原 E4C 的保存分類。

### N45A-03：E4-U 的 X／Y 與 ε 單調

**判定：成立且可搬用；X criticality 須另證。** 對 §2 的任一原 side unit，
X 保留 induced disk 與 T4，完整 root degrees 45／54、其餘 retained 內點4，
故 ε(X)=1。取保 B、同 Σ 的 inclusion-minimal Y，才有 Y 自己 Σ-critical。
有效 degree≥4 給

`ε(X)−ε(Y)=Σ_{I_X−I_Y}(deg_X−4)+Σ_{I_Y}(deg_X−deg_Y)≥0`。

Q 非空時 Y 的有效內部非空連通，E2 前提齊備；Q(X)=Q(Y) 是空、一點或
相鄰兩點。故**同一原 derivative**不能同時拒絕 q3 和 q0／q1。
q0、q1 相鄰，這一步沒有排除它們同拒；也沒有排除所有 unit 身份。
若 X 本來就是指定 β 的 minimal M，它的 β-criticality 已另供應 Σ-criticality；
E4-U 不要求這種特殊情形。

依據：[CORE §2 E4-U](../../artifacts/c5_excess_two_e4/CORE_CONSTRAINTS.md#2-n1unit-side-derivative-不必預填-criticality)
L46–66；E2 §1–3.3 L17–146；E4 §4.3 L225–228。
標题「N1」不限制這個 unit/minimalization 證明只用 N1：此 proof 沒有用 m=1，
本批 m=2 的單側 unit 同樣保其餘完整 degree，故前提逐項成立。
證據：paper＋E2 依賴；172 份獨立 X／Y 有限核對 **triggered and holds**。
其中 160 個 X 非critical、Σ=1023，Y 為 ε0；其餘 12 個 X 單缺列、Y ε1。
此 160 例明確反駁「刪 unit 後 X 自動 Σ-critical」的過強版本，並非目標來源反例。

### N45A-04：E4-S／E4-D 的重色前提

**判定：有重色前提時成立且可搬用；無重色須額外論證。** 同 root 的
兩條原 spokes 在 β 同色，則刪任一條不改 β 的接受性。故 β-minimal core
不能同留該 pair。對 m=2 的任一拒絕 β，至多一 root 有原重色 spokes；
恰一側重色時，每份 minimal core 恰 G 減該 pair 一條 spoke，為 45／54。

依據：[CORE §4 E4-S／D](../../artifacts/c5_excess_two_e4/CORE_CONSTRAINTS.md#4-三列-private-spoke-和-n2-精確-qcore-身份)
L89–125。若兩 roots 都重色，兩侧各刪 spoke 留兩 mixed，違反 44 的
retained-mixed 分類；刪 mixed11 則仍留重色 pair。單重色同樣排 44，剩單側 spoke loss1。
這是「重色 ⇒ 原 spoke core」，沒有「所有原 spoke core ⇒ 重色」的 converse。
26 個原 spoke subsets 的私有色算術，只排 024／124 且須指定三列及 triple-critical。
證據：paper＋本輪獨立 26 格算術；N2 拒絕列單重色 exact-core 前提仍缺控制，
原 E4C E5 記 **not triggered**（其聲稱沿保存資料，不作新的有限驗證）。

### N45A-05：N-diagonal 的局部性及整圖 joint

**判定：局部結論成立且可搬用；整圖接受需额外條件。** 原 mixed C
連通、每點完整 degree4、one-sided，actual support 含於真框邊 {h,k}，
且 H−C 實際碰齊 B∖{h,k}，則每個 proper β、每色 a 的局部 `(a,a)` fibre 非空。
局部 pins 無须先有 G−C 完整染色；hub 常色只在 N(C) 的交集要求。

依據：[E4 §4.1–4.2](../../artifacts/c5_excess_two_e4/REPORT.md#41-新引理-n-diagonal只指定-nc-的局部-list-版本)
L177–208；[Phase B §2.2](../../docs/c5_phase_b_common_lemmas.md#22-b-sd短mixed的同色pins局部延拓)
L87–103。整圖精確接合為

`J_G(β)=(E_z(β)×E_w(β))∩A_P(β)∩A_Q(β)`。

同色接回兩份 mixed 另需 `a∈E_z∩E_w`，並滿足其餘完整原 relations。
兩份都短的拒絕列只給 E_z∩E_w=∅；off-diagonal 仍查原 joint。
X 可沿用已在原 G 證得、且省略 unit 未改的 mixed relations，不能自行預填
X 全 B-touch。證據：paper＋外部 hub 依賴；本輪未重播原 880 個 diagonal 控制，
不把保存的該項 coverage 改稱本輪驗證。

### N45A-06：B-S0 的逐 piece 見證、外路與原收費

**判定：完整前提下成立且可搬用。** §2 的所有原 pieces one-sided：
刪任一 mixed 仍由另一 mixed 連 z,w；刪 unary 不斷 H。對各原 unary U，
其 critical contact 邊給新列 β_e 的 G−e full witness；限制至 G−U 得
不能接回完整 U 的 outside witness。不同 U 可用不同 β_e。
全 B-touch、H−U 連通在假設短支援時給避 U 的 root→框外路；
degree4 tightness／Gallai／原 hubs 才供應 unary 盾長≥2。

依據：[Phase B §2.1 B-S0](../../docs/c5_phase_b_common_lemmas.md#21-b-s0有原見證的共同盾弧排除準則)
L28–85；[原盾弧 §2–4](../../docs/c5_unary_shield_budget.md#3-定理-a全圖至多兩份-unary-分量)
L52–203；E3 notes §3 L67–91。

互斥原 pieces 在同一 disk 收 `σ_G`：unary／long≥2，actual adjacent-pair≥1，
未證支援下界的 mixed 不預收一邊，singleton 可付零。省略 U 仍付原 U 費，
不以 derivative 的 σ_X 替換；原 spoke 不是 piece。
見證跨列只供應各自幾何下界，不能把兩列禁色放入同一 B-C2 染色容量相加。
證據：paper＋外部 hub；本輪未重新實算全盾弧，沿用原論證的明列前提。

### N45A-07：U4 的 O11／retained44 下界

**判定：搬到一般 45／54 需額外前提；目前一般 N2 下界為缺口。**
U4 的 O 下界使用其**原 incidence11**：原兩條 root-contact、critical outside
witness、完整 degree4、Gallai 末端 incidence 計數及連通外部 K4-block 排除。
P 下界另使用**retained44 全四分類**的原內 degree 限制。
兩份均≥2 才给 U4 的 `2+ℓ+2u≤5`。

依據：[U4 §1–2](../../docs/c5_excess_two_nonadjacent_two_mixed_core44.md#2-原支援下界盾弧與新的三-spoke收窄)
L26–87；Phase B §2.1 L80–85。45／54 省略的是 spoke 或 unary，沒有指定
O11 被省略，也没有 retained44；不能把這兩項理由默認為兩原 mixed 的性質。
要單獨引用 O11 子步，須具名核實它的 incidence11、外部連通與全部原見證依賴；
僅「m=2」不提供這些條件。

可用的既有條件接口仍是：**若另證**兩 mixed actual supports 都至少二點，
且有兩份不同原 unary，B-S0 給至少 1+1+2+2>5。這個前提尚未由一般
N2 的 45／54 身份補出，本輪不宣告新子型排除。一般 N2 目前只知兩 mixed 支援非空。
證據：paper 依賴邊界稽核；不是新無界分類或 finite closure。

### N45A-08：B-C2 的 χ=0 paper 式、slack 及 degree

**判定：局部完整前提下成立且可搬用；不是 target 延拓定理。** 對固定
同一 proper β、共同其他 pins（本題無其他 roots）、原完整 degree4 pieces、
全部 contacts 與 tuples，無關外部限制已能填入，完整兩-root join 拒絕且 E_s 非空：
對每個 b∈E_s，χ=0 使 A=E_r，

`D_r^u+O_r^u+δ+o+λ=deg(r)−4`，各項非負。

依據：[Phase B §3.2](../../docs/c5_phase_b_common_lemmas.md#32-b-c2任意两自由roots的條件逐欄容量定理)
L168–237。暫不固定 r 時，每個原 r-contact 保 strict slack，所以整份 mixed
可染且 |G_C(b)|≤k_C^r；完整 joint 拒絕給 A⊆V。
于是 δ+o+λ=m_r−|A|，代入保原 incidence 重數的 side 計數得等式。
unary 同樣按完整 tuple 消去，F 可空，不拆 endpoint marginals。

原 G degree5 的右側1；unit derivative 在下降 root 的右側0、另一側1。
所有 factors、degree 必在所使用的那個圖計算。join 接受或 E_s 空为
**not triggered**；不能跨 β 或把兩個 root 的等式當費用不重用證明。
paper 不需 disk、T4、criticality、ε2 或恰兩 mixed，但保 full degree4/slack 及完整 fibre。

本輪獨立從原邊重算 19 份 N2 的 19 個實際拒絕列，保存每份 mixed／unary
完整 tuples、shared 坐標、16 個 fibres（含空）及全部 piece lifts；每列另外
做全部16個整圖 pinned queries，均拒絕。38 個 root方向下 74 個 columns
**triggered and holds**，右側皆1：64份向量 `(0,0,1,0,0)`、10份 `(0,0,0,1,0)`。
其餘171個接受列不觸發拒絕前提。未驗 derivative 的 B-C2，也未重建所有
190列的局部 fibres；這部分仍留 N45-J，不能宣稱已完成 J 的3040 queries。

### N45A-09：固定 controls 的 coverage 與獨立性

**判定：局部控制成立；精確目標與 N2-45／54 缺控制。**
原 Phase B capacity checker 固定 roots degrees6／5、原 root 邊及 sole shared
singleton mixed，兩圖非平面且不收 T4；其 PASS 不覆盖 χ=0 兩 mixed。
本輪 A 的独立有限逻辑不 import 任何上游 checker，以 BASE 圖／原邊為輸入，
保存結論僅供比較；新枚舉限同 54 保存圖的染色與其具名 units，沒有擴大 k。

依據：[E4C §1–2](../../artifacts/c5_excess_two_e4c/REPORT.md#2-實算摘要)
L12–54；Phase B §3.2 L219–237；原 `scripts/c5_phase_b_controls.py` L153–247。

| 本輪獨立核對 | 結果 | coverage 界線 |
| --- | --- | --- |
| 54保存圖的原邊、rotation／Euler／C5外面、完整Σ | 全部吻合 | 固定原圖，不承擔來源搜尋完備性 |
| 原非框邊 criticality | 1289次，皆有新列full lifts | 沒有精確目標圖 |
| 原root刪除 | 108次，均Σ1023，保存逐列full lifts | 含N2的19圖局部前提成立 |
| 保存minimal core occurrences | 60份：55×48、45×10、54×2 | 核每份minimality；未重枚舉全部cores |
| 12份45／54省略 | 8spoke、4整unary；全部N1 | N2-45／54 **not triggered** |
| 單unit derivatives | 172=147spoke+25unary；160全收、12單缺 | E4-U局部 **triggered and holds** |
| 非critical X | 160份 | 過強「X必critical」之 **counterexample**；非目標反例 |
| χ=0兩mixed拒絕列B-C2 | 19列、74columns成立、304整圖pins拒絕 | 校準paper式；沒有來源排除 |
| 完整Σ933／941或D5像、指定三列全拒 | 0／54 | **not triggered**；Q只有一點或相鄰二點 |
| 新Lean／新無界排除／新source graph搜尋 | 0 | 未宣稱 |

## 4. Findings、重現與影響

### N45A-F01：BASE 的兩個 E4 byte replay 歷史 provenance FAIL

類型：可重現的證書 provenance 漂移；不等於發現新的數學反例。
在 source worktree 執行：

```sh
python3 scripts/c5_excess_two_e4_core_constraints.py --check
python3 scripts/c5_excess_two_e4_reductions.py --check
```

普通及 seed17 都 exit1，分別報 `Exact core-constraints replay failed.`、
`Exact E4 artifact replay failed.`。原 logs／原 JSON 未修改。
兩份 fresh exclusive 重建只在 `sources.artifacts/c5_excess_two_e3/REPORT.md`
的以下兩字段不同，移除 `sources` 後 JSON 完全相同：

| 字段 | 歷史certificate | 本輪BASE實檔 |
| --- | --- | --- |
| bytes | 30573 | 32469 |
| SHA256 | `6d385639c565e2dd08eb61d7835f5fbfec29cd7c467ce8e5abba1dfc2e39e659` | `73ed652a55b159a44eb6da4608f11537efc0d43603128094101ef044a96b2cd3` |

影響：不能把這兩個歷史 `--check` 寫成 BASE 上 PASS。
所需修正：監督回報保留 FAIL，若引用 current replay，明确引用本輪 fresh
證書及外層 BASE/input hashes，不覆寫舊 artifact。fresh 的硬編碼
`baseline_commit=2ac279b…` 是原生成器的歷史字段，不能當本輪实际 HEAD。
完整新舊證書 hash 及逐字段差異見 provenance-comparison.json。

### N45A-F02：目標 coverage 缺口

類型：既有缺控制，非引理反例。重現 `checker.py --check` 的 summary：
`N2_graphs=19`、`N2_core_45_54=0`、`precise_target_graphs=0`。
12 份保存45／54均为N1；54圖沒有指定三列全拒。
影響：不得把172份derivative或74個B-C2 PASS升成精確目標來源驗證、
S／U新命題驗收或任意大小排除。所需修正：逐CLAIM保留缺失前提；未來
若有具名來源控制，先凍結其完整圖與hash再指定增量稽核。不要求本輪搜尋新圖。

### N45A-F03：一般 N2 mixed 支援下界仍 OPEN

類型：既有 paper portability residual。重現對照 U4 §2 L43–65 與
E4 §6 L282–289：前者分别用O11与retained44，後者45／54保两mixed并删side unit。
影響：`2+ℓ+2u≤5`、兩unary排除及相應44star收窄不能直接給本批一般45／54。
所需修正：S／U對各自原unit身份另證两mixed支援≥2，或提供完整joint的其他
窄結論；不能補到就交具名singleton／long／unary residual。N45-A未解這項義務。

### N45A-F04：BASE 文件檢查的兩條既有缺失路徑

類型：歷史交付／連結缺檔。`python3 scripts/check_docs.py` 在獨立 BASE
worktree exit1（586個Markdown、6982個本地連結），缺：

- `audits/2026-10-04-task-d5/c4/scope_ledger.json`，由 `docs/c5_open_leaf_ledger.md:78` 引用。
- `audits/2026-10-04-task-d2/integration_doc_changes.diff`，由歷史 D2 紀錄第39行引用。

影響：不能宣稱整個 BASE 文件檢查 PASS，與本批共同數學前提無直接關係。
所需修正：交監督端保存缺檔 finding；本任務不恢復或改寫別的任務／歷史產物。
同一獨立 worktree 的正式 docs 與全工作樹 DocGraph 均 PASS：62 documents、
213 relations、5 families。這些結果不代表主工作樹及其他 retained worktrees 已通過。

## 5. 重播、未跑項及交付邊界

從 source worktree，獨立 certificate 可重播：

```sh
python3 /home/ray/developer/ai/math/audits/2026-10-09-n45-a/checker.py --check
PYTHONHASHSEED=17 python3 /home/ray/developer/ai/math/audits/2026-10-09-n45-a/checker.py --check
```

此 checker 不 import 原決策邏輯。生成只用 `open('xb')`，同路徑重生成會拒絕；
`--check` 只讀重算。`run_logged.py` 另保存每次命令 metadata／log，避免來源端寫 cache。
完整命令與退出碼以 checks.json 為準，包含原 Phase B 普通／seed17 PASS、
兩個原 E4 普通／seed17 FAIL、兩份 fresh 普通／seed17 PASS，以及本輪獨立重播。
`verify_delivery.py --sealed` 可另外只讀核720份來源、全部交付hash、報告連結與
工作樹狀態；MANIFEST包含其餘全部交付檔案，自身不放入自身hash清單。

刻意未跑：E3／E4-control／E4C全套生成器、ES／ER／plantri搜尋、U1–U4末端
全枚舉、E2上游全部分類、所有core的完整重新枚舉、N45-J全190列局部介面與
derivative容量、任何Lean build／axioms audit。理由是本輪審共同來源及局部
搬用前提，没有新Lean、未扩图族或新source closure。

本輪只使用 paper／既有外部定理依賴及固定 Python；不宣稱新 Lean 驗證、
disk普遍實現性、完整猜想E或N2來源排除。監督端未另指定受影響版本前，
不審S／U候選，任務管理狀態不由執行者改為「已驗收」。

Remaining OPEN：N2-45／54两mixed下界与同一β、pins、原spokes／unaries完整joint；
spoke省略的非重色身份；一般一unary／long混合族；原55与无45／54来源。
下一個最小義務是對返回的S／U **具名CLAIM及凍結版本**逐項核其新增前提，
並依實際圖／證書補增量有限核對。第一輪任務至此停止。

L0完成；L1核對BASE guide的45／54入口及STATUS相關索引，既有停止點相符。
依派工不修改共同入口。沒有來源closure或已採納結論語義失效，無需擴大L2／L3。
文件機器檢查只檢導航，不承擔本報告的數學驗收；其實跑範圍見 checks.json。
