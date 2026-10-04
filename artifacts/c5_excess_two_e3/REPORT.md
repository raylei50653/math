# 任務 E3：猜想 E 的 ε=2 層

2026-10-04；基準 main `2ddc6b4a4e412ab2cb7917fe4fb6fdeef2e86090`；
分支 `task-e3-excess-two`，獨立 worktree `/home/ray/developer/ai/math-task-e3`。
只新增 E3 scripts、artifacts 與本報告；不改導覽、STATUS、README、HANDOFF、
綜合報告或歷史產物，不 commit／push。

**獨立稽核（2026-10-04，D₈）**：[稽核報告](../../audits/2026-10-04-task-d8/REPORT.md)總 verdict 為「有缺口但可補」；唯一缺口 DG6-1 見 §10，已由稽核補表補足。

**部分完成：(i) 唯一 degree-6 的 t=0–3 全部分拆，在三列前提下排除（t=1 的 (4,1)／(3,2) 依 §10 的 D₈ 補表）；
(ii) 雙 degree-5 的非相鄰、相鄰分支都有精確殘留。**
因此本輪沒有證成 E 的整個 ε=2 層，也不能寫成「只條件於 K′」。
K′ 只承擔下述指定短 singleton mixed；非相鄰 separating mixed 等仍是 E3 自身缺口。
沒有構造出符合全部前提的候選反例；沒有從有限搜尋無反例推定任意大小結論。

## 1. 完整前提與證據層

前提與 [E2 §1](../c5_excess_one_e2/REPORT.md#1-完整前提與證據層) 相同：
G 有限簡單，B=(b₀,…,b₄) 是指定有序 induced C₅，圍出 disk 外面；
其餘頂點私有。Σ 是十個完整有序合法框列的共同 S₄ 軌道，
不商去 D₅ 框位置，不各自正規化分量。接受全部 T4，
每條非框邊 e 都滿足 Σ(G−e)⊋Σ(G)。有效內點忽略孤立點，
ε=Σ_{v∈H}(deg_G(v)−4)，degree 包含全部實際框附件。
Q 為拒絕的三色 singleton 位置；c(Q) 是 C₅ 上的連續弧段數。

本報告的主排除前提只另外指定 `q₀,q₁,q₃` 被拒絕，
不要求 Q 恰三點，不要求另外兩個三色列接受。
以下名稱固定使用 [cells.json](../c5_cells/cells.json) 的索引：

| singleton 位置 | 列索引 | 字面列 | E3 前提 |
| --- | ---: | --- | --- |
| 0 | 6 | `01212` | 拒絕 q₀ |
| 1 | 4 | `01202` | 拒絕 q₁ |
| 3 | 1 | `01021` | 拒絕 q₃ |
| 2 | 3 | `01201` | 不限定 q₂ 的接受性 |
| 4 | 0 | `01012` | 不限定 q₄ 的接受性 |

T4 索引仍為 `{2,5,7,8,9}`，mask 932。
每次 D₅ 搬運都搬動整圖、全部列、actual attachments、contacts、ownership、
root roles、環序與共同色框；若再換色，只用整圖共同的 S₄。

| 證據層 | 本輪內容與界線 |
| --- | --- |
| 新紙面化約 | §2 的三列約化與共同 triple-critical 飽和；degree-6 最後單橋 carrier；非相鄰 `(4,4)` mixed 數限制／N-empty；短共用 contact 化至 K′ |
| 沿用任意大小論證 | E2 的 ε≤1 層、全 degree-4 實際原圖分類、active forest、rooted block palettes、原 hubs／tethers、root／zw 接回；使用前逐項核對前提，未重跑舊大枚舉 |
| 新 Python 有限證書 | 框列／32 子集／D₅ 算術；160 個必要 palette queries；固定 bridge residual 表；兩張精確 E1 正控制及補充 cells 控制；非相鄰整數預算／具名外路 bags；B₂/B₃ 同框附件表 |
| 外部定理 | Degree-list tightness 與 Gallai blockwise-uniform 刻畫，及 K₅/K₃,₃ minor 的不可平面性；不是 Python 或 Lean 成果 |
| Lean | 沒有新增 theorem，沒有執行 lake build；本輪拓撲與來源涵蓋沒有 Lean 化 |

本輪重新讀取 Dvořák 講義
[List coloring and Gallai trees，Lemma 7、Corollary 8、Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)。
使用的版本是：連通圖的 degree lists 若不可著色，lists tight，
並由同一原 block tree 的不交 block palettes 刻畫。沒有使用四色定理 oracle。

## 2. 第 0 步：約化成立

[Foundation checker](../../scripts/c5_excess_two_e3_foundation.py) 直接讀 cells 的
pattern_order 與 singleton 映射。目錄中恰有以下五個四點 Q 代表；
此步只讀 Q 的組合形狀，這些 mask 不是本題 T4 全收的來源 witness。

| cells key | 四點弧 Q | 所含兩個 941 形三點子集 |
| ---: | --- | --- |
| 165 | 0123 | 013、023 |
| 424 | 0134 | 013、134 |
| 564 | 0234 | 023、024 |
| 774 | 0124 | 024、124 |
| 960 | 1234 | 124、134 |

五個四點弧全部覆蓋；checker 另核對 B 的全部 32 個子集：

`|Q|+c(Q)>4 ⇔ Q 含兩點弧＋孤點的三點子集`。

包括 Q=B 的情形。每個這類三點子集都是 `{0,1,3}` 的共同 D₅ 像。
因此只要排除指定 q₀,q₁,q₃ 的來源，便涵蓋 933 形、941 形與更大的 Q；
不必假設 Q 恰三點，也不必假設第四／第五三色列的精確接受性。
[foundation.json](foundation.json) 保存五份原 key、32 子集及十份共同搬運。

在固定 canonical 三列下，可能的完整 mask 為 `932、933、940、941`：

| 完整 mask | Q | 非指定兩列的角色 |
| ---: | --- | --- |
| 941 | 013 | q₂、q₄ 都接受 |
| 933 | 0123 | q₂ 拒絕、q₄ 接受 |
| 940 | 0134 | q₄ 拒絕、q₂ 接受；四點弧的另一朝向 |
| 932 | 01234 | q₂、q₄ 都拒絕 |

這是完整列的有限算術，不是存在性聲明。

### 2.1 共同 triple-critical 化約

E2 §2 已從一般來源前提推導：每個有效內點 degree≥4；只要 Q 非空，
H 非空連通；兩個不同拒絕 singleton 列迫全圖碰齊 B。
ε=2 因而只有唯一 degree-6 或兩個 degree-5 roots，其餘 degree 四。
T4 使每個內點至多三條 spokes。

取保留 B、仍拒絕 q₀,q₁,q₃ 的 inclusion-minimal 子圖 M，忽略孤立內點。
每條 M 的非框邊都讓其中至少一個指定列新獲延拓，所以 M 自己也是
Σ-critical。刪點補色論證給每個有效內點 deg_M≥4。對原有效內點集 I：

`ε(G)−ε(M) = Σ_{v∈I−I_M}(deg_G(v)−4) + Σ_{v∈I_M}(deg_G(v)−deg_M(v)) ≥0`。

若 ε(M)=2，等式兩項都為零，所有原 surplus roots 必保留且 degree 不降，
故它們的全部原邊進入 M；沿原 H 的路徑，每個 degree-4 原點一旦進入 M，
便保留全部 incident 邊。H 連通使 M=G。
若 M 是真子圖，就有 ε(M)≤1；M 接受 T4、繼承 induced disk、自己 Σ-critical，
而仍拒絕不相鄰的 q₀/q₃（亦可用 q₁/q₃），與 E2 結論矛盾。

因此 **G 每條非框邊的刪除都必新接受 q₀、q₁、q₃ 中至少一列**。
這個加強沒有使用 q₂/q₄ 的接受性，也沒有把 G 當成每列自己的 minimal core。
同一飽和等式另給：任一 minimal-q core 若仍 ε=2，就必等於 G。
[獨立核對](nonadjacent_foundation_review.json)確認上述推導與孤立點慣例一致。

## 3. 第 1 步：可移植性表

判定說明：「直接」仍需該引理的具名 actual 圖形前提；「三列」僅用
q₀/q₁/q₃；「精確列」表示舊整型證書含額外接受或拒絕條件，不能直接計入 E3。
局部引理可移植與整個舊必要 ledger 已覆蓋所有 E3 來源是兩個不同結論。
完整逐工具、列及原身份表另見 [degree-6 審查](degree6_notes.md) 與
[相鄰審查 §2](adjacent_notes.md#2-可移植性表)。

| 既有工具／分支 | E3 判定 | 精確使用或缺口 |
| --- | --- | --- |
| degree、全框支援、原飽和、D+O、完整 root 查詢接合 | 直接 | 一般 T4／Σ-critical；F 只作共同避色查詢的精確投影，完整 relations 不拆成 marginals |
| 唯一 degree-6：t=0 十一分拆 | 三列 | 多分量盾弧；(6) 原兩 K₄；(5,1)/(3,3) 容量；(4,2) 共同原袋與 partial-row table；§4 |
| 唯一 degree-6：t=1 七分拆 | 三列 | (5) 原 spoke 私有色／active tree；(4,1)、(3,2) 共用支援／palette；其餘六邊預算；§4 |
| 唯一 degree-6：t=2 五分拆 | 三列，含新補證 | (4)、(3,1) 必要表；(2,2) 原 exact omission screen 移除後用 q₁/q₀ 单橋 carrier；其餘盾弧 |
| 唯一 degree-6：t=3 三分拆 | 三列 | (3) ternary≤1 對所選三列的重色 spoke；(2,1) T4-only 必要表；(1³) 六邊預算 |
| 舊 degree-6 雙 spoke／spoke+unary／binary omission 的全 Ω 斷言 | 不作新前提 | 舊 exact-target omission screens 未直接移植；E3 從整型 necessary queries 證明；951 控制的 binary omissions 實際非 Ω |
| 雙 roots 原刪除與至多一例外 | 直接 | 原 S_z/S_w、slack、四點支援交錯；不讀特殊拒絕列 |
| 相鄰 mixed 原 zw 省略 | 直接 | 多 mixed 長環、tree／one-/two-triangle 的 T4 同源接回；Σ(G−zw)=Ω |
| 唯一 mixed 的 proper-core incidence 身份 | 直接 | 每 root loss≤1；原 degree-4 pieces 全取或全不取；(4,4) retaining C 兩側共用 x |
| (4,4) retaining mixed、雙 spoke | 三列 | T4 接回結果均無 941 形三拒絕；原 triangle／roots 全 joint transfer |
| (4,4) retaining mixed、spoke+unary | 精確列缺口 | form26、roots(5,7)、spoke(4,7)、V_at5、target1004 用接受 row3=`01201`；不是三列假設 |
| (4,4) retaining mixed、雙 unary | 長 mixed 直接；短 singleton 待 K′ | 兩 unary 加長 C 需六邊；短共用 contact 的 §6 新引理化至 K′ |
| (4,4) 只省略唯一 (1,1) mixed | 精確列缺口 | 舊 mixed_omission 對十列 imposing exact-target equality；另兩個三色位不能預填 |
| 單 spoke omission 自己 minimal | 條件移植 | 依前序 (4,4) 身份排除；不把未證前序當成所有原單省略已 minimal |
| 五-spoke 整型 | 精確接受性缺口 | 搬至998/1004後 p_A=`01021`、p₂=`01201` 恰一收一拒；三列前提未給後者角色 |
| (3,1)、mixed11＋兩 unary1 | 直接 | 三個不同原 pieces、critical witnesses、原外路；2+2+2>5 |
| (3,1)、mixed11＋一 binary unary | 局部直接；coverage 缺口 | 同列 hubs；指定012/2用 row1=q₃；32/64 必要身份的 minimal 前序尚缺 |
| (3,1)、mixed12＋一 unary1 | 局部直接；coverage 缺口 | 三接點 active triangle；指定012/2用 row1=q₃；依 spoke+unary 前序 |
| (3,1)、mixed13，無 unary | 三列，全子型 | 每個三-spoke set 有所選 row1/4/6 重色；marked-leaf list slack 直接延拓，不需 q-minimal |
| (2,2)、mixed11、共用 pair | 局部直接 | 原 diamond 封 C 到三角；完整外染色的 C witness 替換；不先借 G−C=Ω |
| 同子型短 face／同一長 face／crosscut | 局部直接 | 原面次序、短支援、外路、tightness；hubs 必逐項構造 |
| 同子型共用短框弧 | 三列的局部 joint | 原 IDs155/175 用q₃，179 用q₁，239 用q₀，243/263 用q₃；完整 relations／空 fibres 保持 |
| 同子型不相交 pairs 與47/75整型 ledger | 局部直接；coverage 缺口 | 幾何排除通用；舊0/0 ledger的前序 exact-target 必要域不直接移植 |
| A：mixed12＋a-unary identity | 条件移植 | 原三 contacts與六角色保持；N=Ω／U singleton 前序依未排 (4,4) spoke+unary |
| A 原01/23 | 三列局部 | q₃/q₁/q₀；未用色membership與完整joint；仍需原 N 全收身份 |
| A₂ 原01/12 | 三列局部 | q₁ 迫U={2}；q₀↔q₃ 的共同(1 2) transport；原 actual crosscut |
| A₃ 原01/01 | 局部直接／三列出口 | C 三hub替換不讀mask；q₁ 的 U singleton2/3仍需前序身份 |
| A₄ 原04/04 | 同上 | C 支援{0}/{4}、U含123；q₁ 的 singleton1/3；保留原四 rotations |
| B：mixed22、無 unary | 三列身份可移植 | (4,4)只可雙spoke；四個原spoke omissions Ω；原拒絕 core (5,5)；五個非框spoke pair皆有指定重色query |
| B₂ W933-101／W941-139 的01/23短face12 | 三列局部，可獨立 | q₀ tightness與q₃兩原 pins 的四個 joint list signatures；無額外接受位 |
| B₃ 同骨架長face043 | 三列局部，可獨立 | q₁ 排nonowner03；q₀ 排shared0；q₃ 排shared3/4；五 signatures 與原 bags |
| B₄ W933-129、04/12、shared附件{4} | 主 cut parity 直接 | 五袋與完整degree握手式不讀拒絕列；旧13附件缩表另用第四拒絕 row3=q₂，未借此縮表作新主引理前提 |
| 盾弧引理1/2／A | 直接 | 全B-touch使實際支援等於盾弧頂點；unary≥2；同原圖互斥≤5 |
| hub B／短 mixed 同色 roots 推論 | 直接，相應原hubs前提 | 只用固定拒絕 pin與完整degree四；不能假定四色外鄰自動形成四個 clique hubs |
| 定理 C-W | q-core 條件移植 | 原共鄰端點P₃、(3,2,1)附件、q-critical；在該 q 的 core 驗前提；一般 Σ-critical 不等於每列 q-critical |

### 3.1 必須分開的第四列／精確 mask 分支

上述 spoke+unary、五-spoke、mixed-omission 仍有精確列依賴；在這裡依停止條件 (b)
保留缺口，沒有把旧933/941排除硬推到E3。其後應分開：

- 941 精確分支：額外保證 q₂、q₄ 接受，才可使用相應歷史 exact-target 表。
- 933 形分支：三列之外再拒絕 q₂，q₄ 暫不限定；舊933精確表還需要 q₄ 接受。
- 940 朝向：三列之外再拒絕 q₄，整圖共同搬運成四點弧；搬後仍保留剩餘列的實際身份。
- 932 五列分支：q₂、q₄ 皆拒絕；旧精確933/941表沒有覆蓋這個來源。

本輪完成的唯一 degree-6 論證對這四項統一成立。双 roots 尚未完成的項目
按這個拆分明列；沒有聲稱補了第四拒絕就自動得到另一列接受。

## 4. 第 2 步 (i)：唯一 degree-6 全部分拆

原 H−r 每份 C 都是 unary、one-sided。原 critical witness 给非空禁色，
完整B-touch给避开C的原外路。短支援／hub排除支援包含於一條框邊；
盾弧跨度≥2且彼此互斥≤5，所以原分量至多兩份。
这段没有使用 q₀/q₁/q₃ 的特定身份，在951正控制的两binary上成立。

固定字面框列 β，保留完整 ordered R_C(β) 及原 contacts，
F_C(β)=⋂_{t∈R_C(β)}set(t)。
原 root 可以用色 a，恰當且僅當 a 避開原 spokes 與各 F_C；
这是整份 R_C 的共同避色查询的精确投影。
接点slack使R_C非空；容量、local共同S₄、D身份、固定支援以及原active/bridge必要约束
均从同一实际来源推导。有限表只是这些必要条件的外包络。

| t | 全部分拆 | 三列前提下的排除 |
| ---: | --- | --- |
| 0 | (6)、(5,1)、(4,2)、(3,3)、(4,1,1)、(3,2,1)、(3,1,1,1)、(2,2,2)、(2,2,1,1)、(2,1,1,1,1)、(1⁶) | 三份以上直接六邊；(6) 沿用原 palette-incidence 飽和兩 K₄／K₅；(5,1)、(3,3) 容量；(4,2) partial-row 必要表 |
| 1 | (5)、(4,1)、(3,2)、(3,1,1)、(2,2,1)、(2,1,1,1)、(1⁵) | 三份以上六邊；(5) 原 spoke 的 selected-critical 私有色逼三禁色，active tree/K₅；(4,1)、(3,2) partial-row 必要表 |
| 2 | (4)、(3,1)、(2,2)、(2,1,1)、(1⁴) | 三份以上六邊；(4)、(3,1) partial-row 必要表；(2,2) 本節單橋補證 |
| 3 | (3)、(2,1)、(1³) | (1³) 六邊；(3) ternary最多一禁色、所選重色query要至少二；(2,1) T4-only接回表已至多一拒絕 |

t≥4 已由 T4 排除。
新 [degree-6 checker](../../scripts/c5_excess_two_e3_degree6.py) 的八個形狀必要域
只在 indices1/4/6要求拒絕、2/5/7/8/9要求接受，0/3完全自由；
没有保留原「某binary/spoke省略图全部Ω」screen。
固定 queries 是支援／spoke／原分量角色的有限 palette 算術，不是新來源圖枚舉或逐 ledger key 工作。

### 4.1 最後雙 binary：不用精確接受位的補證

未加單橋 carrier 的必要域恰留下兩份 ownership 互換的弱控制：
原 spokes `02`，短 binary C_s 支援`012`，長 binary C_l 支援`2340`。
指定三列下的精確共同root禁色投影是：

| 列 | F_s | F_l |
| --- | --- | --- |
| q₃=`01021` | {1} | {2,D} |
| q₁=`01202` | {D} | {1,D} |
| q₀=`01212` | {D} | {1} |

这里的D=3，保留同一原分量，不交换它们的独立色框。
只有上述三列及T4来自假设；角色由必要表强制。

省略短C_s后，r degree降至四，其餘有效點仍四，內部連通。
q₁ 下 spokes 禁0、2，而長C_l禁1、D，故原K=G−C_s拒絕q₁。
全degree4飽和使K自己是q₁-core，完整Σ只缺q₁。
K實際不碰singleton b₁；r有原cycle，且內部degree二。
沿用 [unattached-singleton cyclic lemma](../../docs/c5_two_spoke_split_support.md#2-a-useful-consequence-of-the-existing-degree-four-classification)
的**實際原圖**分類：K是原triangle，或兩個互斥triangles以直接bridge相連，無tails。
因此長C_l的兩個原r-contacts x,y之间就是一條原邊 xy。

切开原xy，保留原rooted pieces W_x,W_y及所有off-path blocks。
每份只有一个原r-contact。用精确rooted block-parent query接回所有原子树，
令E_x,E_y为未加r-pin前原contacts的可取色。
q₁下F_l={1,D}迫 E_x(q₁)=E_y(q₁)={1,D}；
这用的是单桥避色充要条件，未把一般binary relation拆成marginals。

比较 q₁、q₀时**两份原Gallai assignment均固定r=1**，它们都拒絕。
off-path所有private点都不是原r-contact；其外部只见三色框，
所以D在两列的原lists中同样出现。
按同一rooted block tree从叶向根扣除disjoint palettes，
每份off-path palette的D-membership逐项固定；这正是
[E2 §5.2 的 carrier 归纳](../c5_excess_one_e2/REPORT.md)
的原接点／parent保持版本。故D仍在E_x(q₀)、E_y(q₀)中。

q₀下拒絕root1，单原桥要求
`E_x(q₀)−{1}=E_y(q₀)−{1}={D}`。
因此固定rootD时，两端remaining sets各为空或{1}，原xy仍不可染。
这迫D∈F_l(q₀)，与表中F_l(q₀)={1}矛盾。
无需断言 E_x(q₀)、E_y(q₀)本身都精确等于{1,D}；集合{D}亦得到相同矛盾。

由此两份弱控制全部排除，(i) 完成。
任意大小涵盖来自原分类／active forest／rooted-block归纳，
Python只核对必要域、同框单桥表及固定图控制。

## 5. 第 2 步 (ii-a)：先處理非相鄰雙 roots

完整論證、原省略分類及證書見
[nonadjacent_notes.md](nonadjacent_notes.md)與 [nonadjacent.json](nonadjacent.json)。
令 m 为原mixed分量数，m_z,m_w为全部mixed原incidences；没有zw。
H连通使m≥1，所以非相邻no-mixed直接排除。

原root删除等式 `Σ(G−w)=Σ(S_z)` 的slack证明可直接重用，
`deg_{S_z}z=5−m_z`。若省略w仍拒絕，唯一可能core就是原S_z，
全degree4且恰只缺一列。两侧不交的四点support不能同时在disk实现，
故全部拒絕列至多一列有任何原root省略例外。
当m≥2，两份原root删除皆Ω；所有拒絕core都含两roots。

**新的原core限制。** 一个两root `(4,4)` core只能恰保留一份原mixed：
兩份 retained mixed 各给原z–w路徑，合成至少四邊的简单環，
违反全degree4實際分類的全simple-cycle triangle性质。
loss(1,1)至多省略一份incidence(1,1)mixed，因此：

- m=1：不能省略sole mixed，只能兩側各省略一個單容量side因子。
- m=2：只能省略一份(1,1)mixed，保留另一份。
- m≥3：根本沒有(4,4)core。

(4,5)/(5,4)只可省略该侧一条原spoke或一份capacity1 unary，保留全部mixed；
同一个这样的原省略图自己ε=1，依E2不能同时拒絕q₃与q₀/q₁。
(5,5)由原饱和必是G自己。这些是来源必要条件，尚未排除每种省略。

**新的 N-empty。** 若原mixed P为one-sided且N_B(P)=∅，
在原H−P取z–w路径L。拒絕pin同色时一个hub取L；异色时沿L的一条原边切成
两个各含对应root的连通邻接hub。它们在N(P)上分别只见该root色。
由hub原則與完整degree4 tightness得K₅，矛盾。
故P能延拓每份合法外染色，其接点边不能Σ-critical。
这不要求hub内部全同色，只要求其N(P)交集同色。

m≥2时所有pieces one-sided，所以每份mixed支援非空，
两unary再加一份不包含于框边的mixed直接六边矛盾。
m=1时sole mixed的删除断开roots，**不是one-sided**，
不能套它的盾弧或假想一条避开它的外z–w路。

| 非相鄰分支 | 本輪所得 | 精確殘留 |
| --- | --- | --- |
| N1：m=1，separating mixed | unary≤2、最多一root省略例外；sole mixed不可省略 | 原两侧各unit因子的(4,4)、一侧unit省略(4,5)/(5,4)、原(5,5)共同三列；保留完整mixed relation的跨列证明 |
| N2：m=2 | 全pieces one-sided、非空支援；(4,4)仅省略一个原(1,1)mixed | unit-mixed原接回、两侧单因子core、原(5,5)；未被盾弧预算排除的支援／relations |
| N3：m≥3 | 两root删除Ω、没有(4,4)core、盾弧及N-empty约束 | (4,5)/(5,4)单侧unit身份与原(5,5)full-minimal |

这些全部独立于K′。未开始逐key mixed-joint分类。
1,284份有限整数预算只核验degree/incidence算術，不含图实现或Σ断言。

## 6. 第 2 步 (ii-b)：相鄰雙 roots及 K′ 輸入

[adjacent_notes.md](adjacent_notes.md)逐项保持原列及named scopes。
本轮已可独立使用root/zw化约、雙spoke(4,4)排除、
(3,1)mixed11＋两unary、(3,1)mixed13無unary、B身份、
B₂/B₃原01/23短／长faces，及B₄指定shared-leaf的主cut-parity证明。
A、其他(3,1)、mixed11旧47/75coverage的前序身份仍依未补的exact-row项，
不能从旧「0/0」升成E3整型结案。

**新的共同短支援约束。** 若one-sided degree4 mixed P两側唯一contact同为x，
实际支援包含于框边hk，且有拒絕外部pin，則P必是singleton{x}。
固定pin的degree lists tight，Gallai末端bridge的非contact leaf需要三个框附件，
短支援容不下；末端odd cycle的相邻private u,v均实际接h,k。
原五袋 `{u},{v},{h},{k},(H−{u,v})∪(B−{h,k})` 连通互斥且全部十邻接，给K₅；
K₄用原连通外框和四tethers排除。
有多blocks时至少一个terminal block不以唯一x作private，仍排除；
单bridge／单odd-cycle亦同。因此只剩singleton，完整degree4迫
N(x)={a,b,h,k}，而拒絕pin恰使这四色互异。
完整证明见 [相鄰審查 §3](adjacent_notes.md#3-短支援共用-contact-的共同約束)。

(4,4) retaining mixed 的全degree4分類迫兩contact共用x；
若原source有两unary，长C先由6>5排除，短C由本引理化至：
**|P|=1、N(P)四色、相鄰degree-5 roots、短one-sided mixed ⇒ 待 K′**。
本輪沒有做其chain partition、diagonal transport或指派枚舉。
这份引理保留935的singleton短mixed正控制，没有把其拒絕pin误排。

| 相鄰殘留 | 輸入缺口／停止點 |
| --- | --- |
| J1：唯一mixed的(4,4) spoke+unary、只省略mixed | 精確十列證書中的額外三色接受條件未移除；按§3.1分開933形／941精確分支 |
| J2：五-spoke | p_A/p₂相反接受性未由三列推出；不能引用原(7) |
| J3：(3,1) binary／ternary整型 | 局部hub／active-triangle可用，前序minimal身份与必要frame coverage仍缺 |
| J4：(2,2)、mixed11＋各侧unary | 局部七机制可用；原47/75coverage的前序exact-target尚缺；部分入口化至待K′ |
| J5：mixed12＋a-unary；mixed22無unary | A前序N全收与剩余frames；B除原01/23faces、指定B₄shared附件外的原faces／contacts／bridges仍保留 |
| J6：較少spokes、多mixed、no-mixed、原(5,5)core | 未被本轮共同引理覆盖；原完整relations与root-pair fibres待三列论证 |
| K′ 指定入口 | 待 K′；仅singleton、四色外鄰、相鄰degree5、短one-sided mixed。其他短支援不同contacts／incidence并不自动归K′ |

## 7. 必做正控制：兩張精確 E1 圖都保留

[positive_control_inputs.json](positive_control_inputs.json)只从E1原artifact只读提取：
`/exhaustive/4/minima_by_sigma/951` 与 `/exhaustive/2/minima_by_sigma/935`。
原文件SHA256为`23a92b56f325bd4bd496d7e8dfb14714d8481618253f88243df4cb7916ca999e`；
每份record另存canonical-JSON SHA及原全部边、Σ、rotation与critical witnesses。
没有复制ignored旧产物进新worktree的历史路径，也没有重跑E1的k≤5枚举。

| 精確控制 | 完整degree／roots | 原pieces／盾弧 | 重算结果 |
| --- | --- | --- | --- |
| 951 | (4,4,4,4,6)，r=5 | 两binary，原vertices69/78，supports014/123，盾边各二且互斥 | Σ=951、ε=2；16/16非框边critical；全部原完整joins吻合；H连通、全B-touch、spokes≤3 |
| 935 | (4,5,5)，roots5/6相邻 | 原mixed singleton7，support34、盾边34，外邻5/6/3/4 | Σ=935、ε=2；11/11非框边critical；两root删除和zw省略皆Ω；四色外鄰拒絕仍保留 |

两图都不含任何941形三拒絕子集；指定三列假设为false。
所有不读指定三列的中间引理都按自身完整前提在两图实际核对：
度数、连通／全框支援、spoke上界、同ε饱和、完整同框piece接合、
unary盾弧／共同预算、拒絕lists的tightness、短mixed同色roots排除，
以及短shared-contact引理。
特定前提未出现（例如nonadjacent、empty-support mixed、C-W原P₃、B₄incidence22）
明确记为不适用，不能把空前提控制称为任意大小证明。

Foundation在两张控制各自的非框边子集上实际检查65,536＋2,048份固定子图：
只有原图本身能保留完整ε=2且有效degree≥4；这是两个固定图的饱和控制，
不是新来源图搜尋。分别保存7、19份degree-valid子图及完整Σ。
固定P外拒絕pin有16、4份，逐份保存同图完整外染色与tight lists。
完整各piece relations与原join全部在同一框列／原颜色中核对。

**校准纠错点。** 951原两binary的省略Σ分别为959与1015，并非Ω。
所以「删binary必Ω」不能当成不含三列前提的通用引理。
新degree-6必要表已彻底移除旧exact-source omission screen；控制没有被排除。
Nonadjacent checker另重算tracked cells的951/935 scratch代表作补充控制，
不将其与上述精确E1 exhaustive图的原vertex身份合并。

## 8. 證書與交付清單

主重播使用以下四個新checkers；producer一律exclusive-create，已有输出就拒绝覆写，
`--check`只读，seed17重播保持确定。缺NetworkX的系统python不能跑foundation；其余三个checker只用stdlib。
使用本机既有 `/home/ray/developer/ai/math/.venv/bin/python`，无需改共享环境。

| 新 checker | 新證書 | 固定範圍 |
| --- | --- | --- |
| [foundation](../../scripts/c5_excess_two_e3_foundation.py) | [foundation.json](foundation.json) | 五四点弧、32子集、十D5；精确E1正控制、full joins与同ε子图控制 |
| [degree6](../../scripts/c5_excess_two_e3_degree6.py) | [degree6.json](degree6.json) | 三列partial palette queries与单桥carrier；general local controls |
| [nonadjacent](../../scripts/c5_excess_two_e3_nonadjacent.py) | [nonadjacent.json](nonadjacent.json) | 两个补充正控制、完整contact tuples／fibres、整数预算、64外路bags |
| [adjacent](../../scripts/c5_excess_two_e3_adjacent.py) | [adjacent_rows.json](adjacent_rows.json) | 同色spoke queries、完整D5 rows、B₂/B₃ actual attachments与joint signatures |

新增文件全部在本任务branch，没有修改任何既有tracked文件。完整列表见最终
`validation.json`的`new_files`。数学入口与辅助审查还包括：
本REPORT、degree6_notes.md、adjacent_notes.md、nonadjacent_notes.md、
positive_control_inputs.json、nonadjacent_validation.json、nonadjacent_foundation_review.json。
最终实际命令、exit code、源文件不变性与文件检查结果续列§9。

未覆盖的双root branches停在上述named scopes；没有扩展逐key案例树、
没有有限no-survivor到一般来源的推断，也没有证明一般出口或K∞=K≤5。

## 9. 實際執行、exit code 與停止點

F 表示 `/home/ray/developer/ai/math/.venv/bin/python scripts/c5_excess_two_e3_foundation.py`。
D/N/A 分別表示 `python3 scripts/c5_excess_two_e3_degree6.py`、
`python3 scripts/c5_excess_two_e3_nonadjacent.py`、`python3 scripts/c5_excess_two_e3_adjacent.py`。
以下都是實際執行結果；生成只在檔案不存在時執行，重播不覆寫。

| 實際命令 | exit code | 結果 |
| --- | ---: | --- |
| F 生成 | 0 | foundation.json，100270 bytes，SHA f98f8b2b…f9cd36 |
| F `--check` | 0 | 精確 E1 兩圖／約化／full joins 通過 |
| `PYTHONHASHSEED=17` F `--check` | 0 | bytes 與普通重播相同 |
| D 生成 | 0 | degree6.json，2027696 bytes，三列必要域及 carrier 完成 |
| D `--check` | 0 | 八組必要域全部零殘留；兩份弱 controls 保留於初層 |
| `PYTHONHASHSEED=17` D `--check` | 0 | bytes 與普通重播相同 |
| N 生成 | 0 | nonadjacent.json，328844 bytes，必要預算／補充控制 |
| N `--check` | 0 | 完整 tuples／criticality／64 bags 通過；分支仍 open |
| `PYTHONHASHSEED=17` N `--check` | 0 | bytes 與普通重播相同 |
| A 生成 | 0 | adjacent_rows.json，D5／三列 local tables |
| A `--check` | 0 | B₂/B₃ 附件與 joint signatures 通過 |
| `PYTHONHASHSEED=17` A `--check` | 0 | bytes 與普通重播相同 |
| `python3 scripts/check_docs.py` | **1** | 兩個既有 missing-path；沒有 E3 新連結或 STATUS 索引錯誤 |
| `python3 tools/docgraph check` | 0 | 62 documents、213 relations、5 families；0 errors／notes |
| `git diff --check` | 0 | 無輸出；另核對所有新檔的 whitespace |

文件檢查的兩個實際錯誤是：

```text
missing path: docs/c5_open_leaf_ledger.md:78: ../audits/2026-10-04-task-d5/c4/scope_ledger.json
missing path: docs/history/2026-10-04-task-d2-integration-audit.md:39: ../../audits/2026-10-04-task-d2/integration_doc_changes.diff
```

這兩檔都不在基準 git tracked files，原工作區中實際存在，新worktree未還原。
沒有複製、重生成、修改它們，也沒有改共用文件消除錯誤。
E3報告位於artifacts，現行check_docs只要求docs下Markdown直接列入STATUS，
所以新報告尚未被STATUS索引沒有產生索引失敗；不能把exit1寫成通過。
最終檢查完整stdout、SHA、命令及新增檔清單保存於 [validation.json](validation.json)。

早期失敗亦保留界線：degree6第一次生成因控制欄位 `sigma`/`sigma_mask`
錯配exit1，未寫出artifact；跨filesystem的rename修正嘗試exit1，後以exclusive-create
建立修正版。Foundation的/tmp草稿首次生成把原P–root邊錯算進K_P，assertion exit1；
正式checker建立前已修正成只保留B、P、P–B邊。補充review首次systempython因
缺NetworkX exit1，改既有venv後exit0。新檔whitespace wrapper首次把no-index正常
「有新增差異」的exit1誤判為錯誤，修正判讀後exit0，沒有任何空白錯誤。
這些是實作／環境失敗，沒有更動數學前提或排除正控制。

截至交付，HEAD仍為基準2ddc6b4、未commit／push，tracked diff為空。
新增文件完整列於validation；既有歷史checker沒有被重跑或覆寫。
(i)完成；(ii)停在N1–N3、J1–J6及精確「待K′」輸入。
後續需要保留同源完整relations補三列共同約束，不能用精確mask接受位代替。

## 10. 稽核後更正（2026-10-04，D₈ 之後）

[D₈](../../audits/2026-10-04-task-d8/REPORT.md) 的 DG6-1：degree6 checker 的兩個 t=1 分拆
`(4,1)`、`(3,2)` 只以原 spoke=b₀ 求解，卻同時固定拒絕位置 {0,1,3}。
Q={0,1,3} 的 D₅ 穩定子只有恆等與反射 i↦1−i，spoke orbits 為 {0,1}、{2,4}、{3}，
所以 spoke 2、3 的相對位置未被涵蓋。§4 表與 degree6_notes 中這兩格各「10 份具名幾何」的涵蓋聲明不完整。

[稽核補表](../../audits/2026-10-04-task-d8/degree6_t1_spoke_coverage.py)在同一固定三列下，
以原 helper 對五個 spoke 位置各求解，同步旋轉整份原 slit 幾何與 ownership：
兩分拆各 5×10=50 份具名幾何，全部 0 存活（`--check` 與 seed17 重播 exit 0，整合者重播確認）。
因此 (i) 的結論維持，引用時須連同此補表；原 producer 與 degree6.json 未改，
其 t=1 兩格的數字仍是 spoke=b₀ 子域。D₈ 其餘項目（約化、triple-critical、§4.1 carrier、
§6 共用 contact、§5 非相鄰限制、K′ 引理 1–6）全部成立。

**E5 之後的更正（2026-10-04）。** [任務 E5](../c5_excess_two_e5/REPORT.md#51-l6n-與-a-spoke-omissions-全收恢復完整-singleton-u-身份)
指出 §3 可移植性表與 adjacent_notes 對 A（mixed12＋a-unary）「需先補一般 spoke+unary (4,4) 前序」的判定過強：
C12 的原長環已排除全 degree-4 retained core，故 N=G−U 全收、兩 a-spoke 省略全收與每個拒絕列的 singleton-U 身份
可在四分支直接證得（E5 L6）。這是依賴範圍的誤判，不影響本報告任何已證排除。
