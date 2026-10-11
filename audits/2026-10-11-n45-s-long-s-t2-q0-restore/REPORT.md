# N45-S-LONG-S-T2-Q0-RESTORE：三 schedules 的完整 q2 原邊恢復

日期：2026-10-11。BASE：`f2692089ad4259808e27d9b7e882ac09505b180a`。
**成果全部待獨立驗收。** 本輪只新增本目錄，不自行採納或更新共享研究狀態。

本輪建立指定三 schedules 的任意大小紙面排除候選：在同一原來源上，
`q2=01201` 的每份完整 X lift 都滿足 `r≠1=q2(b4)`，全部恢復原 `e=rb4`。
已採納 `Q(X)={β}` 提供 q2 非空，因此每個 schedule 都有一份完整 G(q2) lift，
與原 q2 拒絕矛盾。q1 僅作原 G 已接受的輔助查詢，不計為本任務 Δ 的突破。
q2 的存在性保留上輪 SF-QX 的明列繼承依賴；本輪新增的是完整 r-fibre 的排除及恢復。

## 1. 權威與完整來源範圍

首先只讀執行派工 `check_dispatch.py --check`，exit0、status=passes；
本輪原生再次核驗保在 `logs/dispatch-preflight.*`。HEAD=固定 BASE，tracked diff 為空。
派工 `input-pins.json` 的 12 個 BASE Git blobs 和 11 個 sealed audit SHA256 分列於
[inputs.json](inputs.json)，已驗收 review 沒有被稱為 BASE blob。
較早 long-contract REPORT 的 BASE 只保歷史 provenance。

已讀 frozen long-contract §1 K1–K12 全部條款，review 的 REPORT、acceptance、
corrections、fibre-paper-review，以及原 B REPORT §§2–9／obligations。
原 B pending bytes 保持不動；採納依 review 附錄，沿用 `12+4+10+4` 分類，
SF-RESIDUAL 依賴補列 SF-T2-Q0-Q1-RESTORED。沒有引用同批其它任務的新結論。

| 契約 | 本輪保留的原來源資料／前提 |
| --- | --- |
| K1 | 任意大小有限簡單 disk G，具名 ordered induced C5 `B=(b0,…,b4)`；完整原 vertices、edges、rotation。 |
| K2 | 完整 ordered Σ=933/941 或同一整圖 D5 像；全部非框邊 Σ-critical，Q(G) 為下表之一。 |
| K3 | 原有效 H 連通、full B-touch、ε=2；非相鄰原 degree5 r/s，其餘有效內點完整 degree4；自由孤立內點保全部染色因子。 |
| K4 | H−{r,s} 的完整原分量恰 U/L/S；U 只接 s，L/S 各接兩 roots，原 one-sided，支援非空。 |
| K5 | actual U012、long L234、原 pair S40；S 的原 vertices／bridges／旁支均保留，不預設單頂點。 |
| K6 | 原 `e=rb4`、t_r=1；X=G−e，vertices 及其餘原 edges／attachments 全留，無 retained r-spoke。 |
| K7 | 固定 β=q0=01212，X=M 本身是 inclusion-minimal β-core，完整 root degrees=(4,5)。 |
| K8 | U owner=s、n_U=1；named/ordered contacts 與 shared vertex 保原單一座標。 |
| K9 | 一次共同 whole-source normalization；跨列原 contacts／ownership／supports／rotation／bridges／框順序不變。 |
| K10 | 十 literal 列、每列全部16 ordered (r,s) pins，diagonal／空 fibres／全部 tuples、preimages、full lifts。 |
| K11 | G 每條原非框邊的 Σ-critical 完整 witness 分開保留，各邊列可不同。 |
| K12 | X 每條 retained 非框邊的同一 β 完整刪邊 witness；不拿 G 的 witness 替代，不改取另一 core。 |

固定 `(t_s,m_s,n_U)=(2,2,1)`，原 s-spokes b0/b2，
`(k_L^r,k_S^r)=(2,2)`、`(k_L^s,k_S^s)=(1,1)`。
actual `H_X−s` 的兩完整分量為 `C={r}∪L∪S` 與 U；r 在 C 上完整 degree4，
incident 兩個原 odd-cycle blocks。所有原件、環長、bridges、旁支大小無上界。
沿用已採納 `F_C(β)={3},F_U(β)={1},Q(X)={β}`。

| schedule | 原 Σ orbit／Q(G) | 完整 Δ | 新完整恢復列 |
| --- | --- | --- | --- |
| B-933-0234 | 933／0234 | q2,q3,q4 | q2；每份 X lift 的 r≠1 |
| B-941-023 | 941／023 | q2,q3 | q2；每份 X lift 的 r≠1 |
| B-941-024 | 941／024 | q2,q4 | q2；每份 X lift 的 r≠1 |

這是三個必要 schedules 的紙面候選覆蓋，不是三份來源圖。只含 s-spokes `[b0,b2]`
這一變體，不涉及 t_s=1、β=q2 或其餘21 schedules。

## 2. 完整 fibres 與 β 的滿額 r 欄

Col={0,1,2,3}。對原 T=L/S，`Λ_T(η;a,b)` 保全部滿足原 internal edges、
actual B attachments 及原 r/s contacts 避色約束的完整 assignments。
若某原 contact 同時接 r/s，兩約束作用在同一原 vertex。
每個完整 ordered tuple 保全部 preimages；空 pinned fibre 仍有位置。

定義完整 r-forbidden 欄

\[
D_T(\eta;3)=\{a\in\mathrm{Col}:\Lambda_T(\eta;a,3)=\varnothing\}.
\]

這是全 assignment 的特定 emptiness 查詢，不能代替原 R_T 或 r-fibres。
在 β、q1、q2 上，actual U012 的附件字面都為012，故 U 的全部 assignments、
ordered tuples、preimages 及 pinned fibres 相同，`F_U={1}`。
原 s-spokes b0/b2 的色都是0/2。因此這三列任何完整 X lift **必取 s=3**；
U 避3的完整 preimage 集非空。自由孤立點保相同 `Col^I` 全因子。

X 自己拒 β、r 無 retained spoke，frozen long-contract §5 的同一 β／s=3
zero-slack 欄給（亦對回原 B REPORT §4 末段）

\[
\boxed{D_L(\beta;3)\sqcup D_S(\beta;3)=\mathrm{Col},
\qquad |D_L(\beta;3)|=|D_S(\beta;3)|=2.}\tag{1}
\]

完整 degree4/contact slack 給每欄至多兩禁色；β 的全 pins 拒絕迫聯集四個色，
故滿額且互斥。這是同源必要式，沒有把 β 欄填入其它列。
原 short N-diagonal（同一 frozen §5）給 `Λ_S(β;3,3)≠∅`，因此

\[
\boxed{3\notin D_S(\beta;3).}\tag{2}
\]

這只用原完整 S 的局部 theorem，S 不被替換為單點。其外側原 U/L/r/s 仍連通，
U012/L234 保 B\{b4,b0} 的 actual attachments；原 e 在 S 外。

## 3. 原已接受 q1 強制 β 的 S 禁 r=2

令 `q1=01202`，π01=(0 1)。actual L support 的 ordered values 是
β234=212、q1_234=202，所以逐一對**原 L 的全部 vertices**施 π01 是完整雙射

\[
\Lambda_L(\beta;a,3)\longleftrightarrow
\Lambda_L(q1;\pi_{01}(a),3),\qquad
D_L(q1;3)=\pi_{01}D_L(\beta;3).\tag{3}
\]

π01 固定 s=3；r pin 按 π01 搬，不假稱所有 r pins 不變。
原 internal edges、ordered/shared contacts 的兩避色不等式、全部 tuples／preimages
同搬，空 fibres 亦同搬。原 S40 在两列均為20，U012 均為012，故 S/U 用恒等。
這是同一原件的查詢雙射；接合時全部回到同一 q1 literal frame。

若 `2∉D_S(β;3)`，由(1)(2)迫
`D_S(β;3)={0,1}`、`D_L(β;3)={2,3}`。
π01 逐色固定{2,3}，故 q1 的 L/S forbidden 欄仍聯集 Col。
s≠3 pins 已被 actual U/spokes 排除；s=3 的每個 r pin 又至少一份 L/S 完整 fibre 空。
restriction／union 因而給 **q1 的全部16個完整 X fibres 都空**。

三 assigned schedules 都有 `q1∉Q(G)`。K2 的完整原 signature 給原 G(q1) 非空，
restriction 到原 X 給 X(q1) 非空，矛盾。故

\[
\boxed{2\in D_S(\beta;3).}\tag{4}
\]

此處 q1 只是原已接受的輔助列，不重證舊 q1 RESTORE，也不以 q1 充當 Δ 突破。
若列全部必要二色欄，純集合算術如下；不是 actual source relations 或 preimage 數值：

| β 的 D_S | β 的 D_L | q1 可能 r 色 | q2 的 D_S |
| --- | --- | --- | --- |
| {0,1} | {2,3} | 無，違反原 q1 接受 | {0,2}；此分支已排 |
| {0,2} | {1,3} | {1} | {0,1}，禁 r=1 |
| {1,2} | {0,3} | {0} | {1,2}，禁 r=1 |

## 4. q2 的完整 r=1 空 fibre 與原 rb4 恢復

令 `q2=01201`，π12=(1 2)。actual S40 的 ordered values 是
β40=20、q2_40=10，π12 固定0/3。對**原 S 的全部 vertices**施 π12，給

\[
\Lambda_S(\beta;2,3)\longleftrightarrow
\Lambda_S(q2;1,3).\tag{5}
\]

這是全部 assignments／ordered tuples／每個 preimage 的雙射，含 empty fibres；
原 edges、attachments、contacts、shared identity 與 rotation 不改。
由(4)，左側空，所以右側空；任何完整 X(q2;1,3) lift 的 S restriction 都會落入右側，故

\[
\boxed{\mathcal L_X(q2;1,3)=\varnothing.}\tag{6}
\]

q2 的其餘 s pins 0/2 被 retained 原 s-spokes 排除，s=1 被 actual U 排除。
所以 `L_X(q2;1,b)=∅` 對全部 b 成立。
已採納 `Q(X)={β}` 給至少一份完整 X(q2) lift；結合(6)，每份 such lift 都 r≠1。

對任意 proper literal η、全部 ordered pins，恢复唯一原 e 的精確全集合等式仍是

\[
\mathcal L_G(\eta;a,b)=
\begin{cases}
\mathcal L_X(\eta;a,b),&a\ne\eta(b4),\\
\varnothing,&a=\eta(b4).
\end{cases}\tag{7}
\]

q2(b4)=1，故每份完整 X(q2) lift 已滿足原 rb4，均為完整 G(q2) lift。
C 的 r、全部 L/S assignments、同一 s=3 的 U 全 preimages 及自由孤立點因子同步接合，
沒有先丟掉 r 的投影或另選其它來源 witness。
三 schedules 都 q2∈Δ，因而各自與原 G 拒 q2 矛盾。
沒有新增充分前提，也不需要 source-minor、四色 virtual-frame singleton theorem 或虛設 T4 繼承。

## 5. Coverage、依賴與證據分層

[claims.json](claims.json)逐 claim 列量詞、前提、結論種類、依賴與原 e/r 座標。
[coverage.json](coverage.json)保存三 schedules 的完整 Δ、唯一 spoke 變體、
從原 obligations 提取的全部十列／16 pins，另列本輪 q2 必空 pins 與 collectively nonempty
恢復池。未指定哪個 r=0/2/3 fibre 非空，不捏造來源 assignments、tuples 或 preimages 數值。
原來源拒 q2 本需所有 r≠1 fibres 空；本輪證它們的聯集非空，正是紙面矛盾。

q3 的 r≠1、q4 的 r≠2 個別恢復 fibres 沒有新增證明，精確列在 coverage 的
`individual_restoration_not_proved`。三 schedules 已各由 q2 覆蓋，故沒有 assigned schedule
殘留需靠 q3/q4 才能結案；這些個別查詢不升格為未解來源反例。
T4 五列仍按原 e 的字面 b4 色核，不借未用色。

| 層 | 本輪結論與界線 |
| --- | --- |
| 紙面 | 三 assigned schedules 的任意大小來源排除候選，全部待獨立驗收；新證完整 q2 r-fibre 恢復。 |
| finite calibration | 只核固定3個 forbidden-column cases、2個 support colour transports 及480個 coverage pin positions；純紙面介面算術，非來源 controls。 |
| target source | executed=false、trigger_count=null、status=`not triggered`；沒有提供或枚舉 K1–K12 actual source。 |
| source realizability | 未建立；紙面排除候選不能報為有限實現。 |
| Lean | 未新增 theorem／未執行 build；本輪紙面未形式化。 |
| 一般 N45/N2/E | 未建立；不擴 owner=s 全域、t_s=1、β=q2、其它 core、ε≥3。 |

finite metadata／algebra 的只讀普通及 seed17 結果、兩指定 corrupted-certificate 負控制
及全部原生 commands/stdout/stderr/exit 保在 `logs/` 與 [checks.json](checks.json)。
這些核查只支援交付算術與輸入 custody；來源排除由§2–4的全 assignment 紙面論證承擔。
上輪19 controls 不重跑，新圖數=0；不以零 triggers 作排除。

交付後只讀核驗命令（不要重跑 exclusive metadata generation）：

```sh
python3 -B audits/2026-10-11-n45-s-long-s-t2-q0-restore/audit.py check
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-n45-s-long-s-t2-q0-restore/audit.py check
python3 -B audits/2026-10-11-n45-s-long-s-t2-q0-restore/audit.py verify-delivery
```

q2 存在性引用 sealed review 的 SF-QX／SF-T2-EXTEND／E2 既有紙面及 inherited
finite-terminal 信任鏈。本輪未重證或重新執行該鏈。zero-slack／N-diagonal 引用固定
BASE long-contract §5，外部 degree-list/Gallai theorem pin 另列 inputs，屬上游依賴，
本輪沒有重抓 PDF 或新增外部／Lean theorem。
q1 存在性在這三 schedules 直接由 K2 得到，無須依賴 missing 終局 JSON。

## 6. Findings、custody 與停止點

兩指定 observations 缺 BASE blob：no-spoke-exterior 及 single-spoke-residual-locality。
原生 `git show BASE:path` 均 exit128，見 [findings.json](findings.json)及 logs。
physical／quarantine 不入權威，依賴其 bytes 的 finite replay 未執行，紙面部分照續。

[custody-before.json](custody-before.json)與 [custody-after.json](custody-after.json)
對全部派工權威、採為數學權威的 originals 及原 B certificate/input manifest 核前後零漂移。
HEAD／tracked diff 不變；只新增本專屬目錄，沒有改共享 docs、原交付、舊證書或其它 worker。
三份本任務內部只讀核對支持本證明；不替代使用者要求的後續獨立驗收。
兩個 metadata 欄位的精確化另存 [metadata-corrections.json](metadata-corrections.json)，
先前 metadata／native logs 保在 `metadata-initial/`，未作最終 claims 權威。
[delivery.json](delivery.json)列精確 payload hashes、metadata exclusion 及 pending 狀態。

**停止點：指定三 schedules 已完成紙面全覆蓋候選，待獨立驗收。**
本輪不 commit／push／PR，不發外部訊息，亦不繼續其它 schedules。
