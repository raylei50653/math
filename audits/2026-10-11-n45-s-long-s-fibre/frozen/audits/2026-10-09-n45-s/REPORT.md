# N45-S：原 spoke 省略的零容量化約與兩 unary 子型排除

2026-10-09；執行者交付完成，**待監督端／N45-A／N45-J 交叉驗收**。
BASE 與實讀 checkout HEAD 均為
`dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。
指定任務凍結於 [task.md](task.md)，來源雜湊見 [inputs.json](inputs.json)。

**紙面窄結論：在本任務的原 spoke 省略 45／54 身份下，原 G 不可能有兩份 unary。**
另外得到完整 joint 的零 slack 正常式；兩 mixed 都短時，它們各有至少二點
實際支援，且唯一 unary 側的 mixed incidence 為 2、另一側為 3。
這些是任意大小的條件命題，依賴下列 BASE 引理；有限表只核對介面算術。
沒有排完 N45-S、N2 或猜想 E，也沒有給保存控制補出新的目標來源。

## 1. 原圖、量詞及依賴

任取有限簡單圖 G，有序 induced C5 外框 B=(b0,...,b4) 圍 disk 外面；
完整有序 Σ(G)=933／941 或整圖 D5 像，每條非框邊 Σ-critical，ε(G)=2。
忽略孤立內點；完整 degree-5 roots r,s 非相鄰，其餘有效內點完整 degree 4。
H−{r,s} 的完整原分量恰有兩份 mixed P,Q，其餘為 unary。
共同搬運整圖後用 canonical mask，不獨立搬框、roots、pieces 或色名。

固定原 spoke e=r b_i，固定任一原拒絕列 β，使
**X=G−e=M 是 β 的 inclusion-minimal 拒絕 core**。
X 的 root degrees 是 (4,5)，root 交換給 (5,4)；兩 mixed、所有 unary、
所有原 contacts、內邊、框附件、bridges、ownership 都完整保留。
`m_r=k_P^r+k_Q^r`、`m_s=k_P^s+k_Q^s`；u 是原 unary 數。
各 k 是不同原 root-contact 邊數；shared contact 始終只用一個原頂點坐標。
「短」指實際支援包含於一条真框邊的兩端，允许 singleton；「長」指其餘。

| 依賴 | 使用內容／證據層 |
| --- | --- |
| [E3 REPORT §2.1](../../artifacts/c5_excess_two_e3/REPORT.md#21-共同-triple-critical-化約) | triple-critical、全 B-touch；紙面，沿用 E2 |
| [E3 nonadjacent notes §2–5](../../artifacts/c5_excess_two_e3/nonadjacent_notes.md) | root-deletions 全收、原 pieces 飽和、N2 one-sided、mixed 支援非空、45／54 省略身份；紙面＋既有分類 |
| [E4 REPORT §4／§6](../../artifacts/c5_excess_two_e4/REPORT.md) | 完整 R_P／A_P／J、局部 N-diagonal；紙面 hub 證明 |
| [CORE_CONSTRAINTS §2／§4](../../artifacts/c5_excess_two_e4/CORE_CONSTRAINTS.md) | E4-U、E4-S、E4-D；紙面，mask 算術另有有限控制 |
| [Phase B §2.1／§2.2／§3.2](../../docs/c5_phase_b_common_lemmas.md) | B-S0 原盾弧收費、B-SD、χ=0 的 B-C2；紙面，未 Lean 化 |
| [原盾弧 §2–3](../../docs/c5_unary_shield_budget.md) | 原盾弧互斥、unary 費用≥2；紙面＋外部 Gallai／hub 依賴 |
| [E2 REPORT](../../artifacts/c5_excess_one_e2/REPORT.md) | ε≤1 的 Q 空／單點／相鄰二點；沿用其紙面化約與有限末端證書，本輪未重跑 |
| [U4 §2](../../docs/c5_excess_two_nonadjacent_two_mixed_core44.md) | 只辨認 O11／retained44 專用下界；本輪支援證明不使用它們 |

外部 degree-list slack 使用 [Dvořák 講義 Lemma 7](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)：
連通 degree-list 若有一點 strict slack，便可由生成樹順序貪婪填入。
本輪重新核其陳述與證明；同份講義 Theorem 10 是沿用盾弧／N-diagonal 的
Gallai 依賴。留存 [PDF](gallai.pdf) 及 SHA256；沒有用四色定理 oracle。

## 2. N45-S-01：導數與完整跨列限制

**量詞／前提：** §1 全部原來源前提、任一原 spoke e；本節的 E4-U 步驟
甚至不要求 X 已是 β-core。**結論／層：** 以下任意大小必要式，紙面依賴 E2。

X 保留 induced disk，繼承 T4，全體保留非 root 點仍 degree 4，
r 降為 4，s 仍 5，故 ε(X)=1。若要用 Σ-critical 前提，先取
保 B、保完整 Σ(X) 的 inclusion-minimal Y；Y 自己 Σ-critical。
X 的有效點 degree≥4 給

`ε(X)−ε(Y)=Σ_deleted(deg_X−4)+Σ_retained(deg_X−deg_Y)≥0`。

所以 E2 適用於 Y，`Q(X)=Q(Y)` 空、單點或相鄰二點。
在本任務 X=M 時，β-minimal 本身也使 X 每條非框邊 β-critical，
因而 X 自己 Σ-critical；這是由新前提推出，並非原 G 自動傳給所有 derivative。

以 singleton 位置記 Q，同一 X 的完整容許表為：

| Σ(G) | Q(G) | Q(X) 的必要域 |
| --- | --- | --- |
| 941 | {0,1,3} | ∅、{0}、{1}、{3}、{0,1} |
| 933 | {0,1,2,3} | ∅、四個單點、{0,1}、{1,2}、{2,3} |

X=M 時另要求 β 的位置在 Q(X) 中。故同一 X 不能跨 q3 與 q0／q1；
933 的 q2 不得略去：β=q2 時可為 {2}、{1,2}、{2,3}。
941 的 β 只能是 q0/q1/q3，933 另含 q2；q4 與全部 T4 均接受。
原 spoke 的新接受列恰為 Q(G)\Q(X)；每份 X 延拓若屬這些列，必有
`f(r)=β(b_i)`，否則它也延拓 G。這仍要求同圖、字面 pins 與 full lift。
不把必要 mask 當作 disk 實現證書。

## 3. N45-S-02：拒絕列上的零 slack 正常式

**量詞／前提：** §1；固定 X 拒絕的 β、任一 `b∈E_s(β)`。
**結論／層：** 以下完整介面等式，任意大小紙面；依賴 B-C2 與 degree-list slack。

R_U、R_P、R_Q 始終是原 piece 的完整 contact tuples 與 full lifts。
F_U 只作完整 R_U 的避色查詢，不替代 R_U；允許其他列 F_U 為空。
令 E=E_r^X，E_s 是未改的 s-side；spoke 單獨提供其字面框色 singleton 因子。
令 C_P(b)={a:(a,b)∉A_P(β)}，C_Q 對稱。

一份 unary 的禁色数 `|F_U|≤n_U`：拿掉 root 時原 connected U 有
root-contact slack，故存在完整 coloring；F_U 是每份完整 contact tuple
色集合的交集，因此不超過原 root-contact 數 n_U。
每個 mixed 有類似欄界 `|C_P(b)|≤k_P^r`，反向行界亦成立。
這保所有 ports 同時避色，shared port 的兩個不等式同時核，並未乘 marginals。

兩 mixed 各接每側，故 m_r,m_s≥2；原 s 的 side incidence=5−m_s。
所以 `|E_s|≥4−(5−m_s)=m_s−1≥1`。原 e 存在也給 m_r≤4。
對 X、χ=0、完整 join 拒絕套 B-C2：

`D_r^u+O_r^u+δ_r(b)+o_r(b)+λ_r(b)=deg_X(r)−4=0`。

每項非負，於是對**每個** b∈E_s 同時有：

- 每份 r-unary `|F_U|=n_U`；全部保留 r-spoke／unary 禁色因子兩兩不交。
- `|E|=m_r`，不是把 degree5 的一單位預算帶入 degree4。
- `|C_P(b)|=k_P^r`、`|C_Q(b)|=k_Q^r`；兩欄不交且
  **`E=C_P(b) ⊔ C_Q(b)`**，沒有落在 E 外的禁色。

這是一份原完整 relation 的必要正常式，不是有限圖模板，也沒有把
R_P／R_Q 或其 full lifts 換成這些數量。適用任意大小、任意 support。
若 side 因子重疊、unary deficit、mixed 欄 deficit／重疊／外溢有任何一項，
該精確 spoke-omission 拒絕身份即不可能。

## 4. N45-S-03：省略 spoke 的色被誰禁止

**量詞／前提：** N45-S-02；c=β(b_i)。**結論／層：** 紙面完整因子二分。

| c 相對 E | 原 G 中該色的禁止來源 | 原 degree5 的一單位預算 |
| --- | --- | --- |
| c∉E | 恰一份保留 r-side 因子；可能是一條原 spoke，也可能是整份原 unary 的 F_U | O=1、λ=0，其餘 0 |
| c∈E | 每個 b∈E_s 的完整 joint 中，恰 P 或 Q 的欄禁止 c | O=0、λ=1，其餘 0 |

第一種只有 blocker 真是另一 spoke 才屬重色 spoke；unary blocker 不能
套 E4-D。第二種的 owner 可以隨 b 改變，不保證有一份 fixed mixed 封住所有欄。
刪 e **仍拒絕本列** 與 e 在**其他列**的 Σ-critical witness 是不同用途。
E4-D 的「單 root 重色迫 exact spoke core」只在其重色前提下沿用。

## 5. N45-S-04：低 incidence 的 singleton mixed 是通用 relation

**量詞／前提：** 任一原 one-sided degree4 mixed C，全 B-touch 的同一 disk；
actual support 恰 {h}；兩側正 incidence k_r,k_s 且 k_r+k_s≤3。
**結論：** 每個 proper β 的 `A_C(β)=Col²`。
在 N45-S-02 中這與 `|C_C(b)|=k_r≥1` 矛盾。
**層／依賴：** 任意大小紙面，N-diagonal、兩方向 contact 界與色名雙射。

固定 c=β(h)。C 的局部染色限制只見 c 與兩個 pins；整份 relation
在固定 c 的共同 S3 色置換下不變。N-diagonal 已給全部四個 diagonal pairs。
剩餘的 forbidden pairs 只能是下列三個完整軌道的不交聯集：

| 軌道 | ordered pairs | 若存在，所需 contact 界 |
| --- | --- | --- |
| I | (c,b)，b≠c，共 3 個 | k_s≥3（同一行） |
| II | (a,c)，a≠c，共 3 個 | k_r≥3（同一欄） |
| III | a,b≠c 且 a≠b，共 6 個 | k_r,k_s≥2（每行／欄 2 個） |

k_r+k_s≤3 且各正，三軌道皆不能存在，故完整 compatibility 通用。
這個色置換只對局部存在性施行雙射，沒有独立正規化后拿來拼全圖；
拼回時仍使用原 β 與原 ordered pins。
因此本任務的 singleton mixed 必滿足 `k_C^r+k_C^s≥4`。
此式仍容許 singleton(2,2)、(1,3) 等；沒有證成一般 N2 mixed 支援下界。

## 6. N45-S-05：兩 short 下界與兩 unary 窄排除

**量詞／前提：** §1；下界部分另假設 P,Q 都短。
**結論：** 兩 short 時 m_r+m_s≤5、兩份 actual support 均至少二點；
完整 §1 的原 G 均有 u≤1。**層：** 任意大小紙面；依賴 S-02、S-04、
原 N-diagonal 及 B-S0，不使用 U4 的 O11／retained44 下界。

兩 short 的 diagonal 均接受，X 拒絕 β 必有 `E∩E_s=∅`。
S-02 的 |E|=m_r 與 |E_s|≥m_s−1 給

`4≥|E|+|E_s|≥m_r+m_s−1`，所以 `m_r+m_s≤5`。

另一份 mixed 至少貢獻兩條 contacts，因此每份 C 的總 incidence≤3。
其 actual support 非空；若 singleton，S-04 給通用 A_C，違反 S-02 的
正值欄飽和。故每份至少二點，兩 short 恰為真框邊 pair，原盾弧各長 1。
這裡 N-diagonal 使用的是全 B-touch 的**原 G**；X 可能少碰 b_i，
沒有假設 X 自己碰齊框或借用 X 的盾弧。

原盾弧已給 u≤2。若 u=2 且有 long mixed，原三份不同 pieces 收費
`2+2+2>5`，沿用既有排除。若兩 mixed 都 short，本輪下界給

`|σ_G(P)|+|σ_G(Q)|+|σ_G(U1)|+|σ_G(U2)|≥1+1+2+2=6>5`。

U1/U2 的拒絕見證分別由各自原 critical contact 的刪邊 full lift 限制到
G−Uj；兩 mixed 使 H−Uj 連通。若 Uj 短，原全 B-touch 提供位於其外的
框點及避 Uj 的 root 外路，所以 B-S0 全部原前提成立。見證可來自不同列，
这里只加同一原 G 的幾何費用，没有加跨列禁色容量。
因此 **N45-S 的原兩-unary 子型排除**。spoke e 沒有付任何 piece 盾弧費用。
此窄排除不适用整 unary 省略、原55或無45／54 core來源。

## 7. N45-S-06：兩 short 加一 unary 的具名 residual

**量詞／前提：** §1 且兩 mixed 都短。**結論／層：** 下列必要原身份，紙面；
依賴 S-05 與本段重新給出的 star 面論證。

u=0 已由原兩 short 的未用色 diagonal 接回排除；S-05 排 u=2，故 u=1。
令 t 是没有 unary 的那側 root，a 是 unary 側。若 m_t=2，原 t 有三條
spokes；H−t 由另一 root、兩 mixed、唯一 unary 連成一份。
所以其全部原邊／框附件都落在 B 加 t-star 的同一面。
原全 B-touch 迫這個面包含兩個非 spoke 框點，故三 spokes 必連續，
該面的框弧恰長 3。每份 P,Q,U 的原盾弧都在該弧內：刪除 piece 後
F_piece 含 t 及 star 外的兩個小面，弧外框邊仍在其面邊界。
但本輪下界要求 `1+1+2=4` 條互斥盾邊，矛盾。
這段只使用原 H−t 連通，與44分類無關。

因此 m_t≥3；m_a≥2 及 S-05 總和≤5 迫
**`(m_a,m_t)=(2,3)`**。在 unary 側兩 mixed 各一 contact；另一側一份
一 contact、一份兩 contacts；兩 mixed 都是原真框邊 pair。

| 名稱 | unary 所在側／e 所在側 | 原 side incidence 與本列必要域 |
| --- | --- | --- |
| S-SHORT-U-LOW | U 在 r，e 也在 r；m_r=2,m_s=3 | s 恰兩 spokes；(n_U,t_r)=(1,2)或(2,1)；|E|=|E_s|=2，彼此互補 |
| S-SHORT-U-HIGH | U 在 s，e 在 r；m_r=3,m_s=2 | r 原兩 spokes，X 留一；(n_U,t_s)=(1,2)/(2,1)/(3,0)；|E|=3，E_s 恰為保留 r-spoke 的框色 |

表中 n_U 是原 contact 數，不指每列 F_U 一定為 singleton。
未證這兩身份可實現，也未證它們不存在；完整 R_U、R_P、R_Q、
所有十列／16 pins（含空 fibres）、full lifts 與 critical witnesses 仍是必要輸入。
下一個最小義務是 S-SHORT-U-LOW 的原 U incidence1、兩側各兩 spokes：
在同一原支援／共同色框上，判其完整兩 mixed joint 能否同時滿足 S-01 的
Q(X)、原 933／941 及逐邊 criticality。不能把 (1,2) incidence mixed 收縮成染色 star。

其餘 residual 仍包含一 long、零／一 unary；兩 long、零 unary。
帶 singleton 的 long／short 配置未排，除 S-04 的低 incidence 禁型之外，
其完整同列欄必滿足 S-02，而跨列仍須 S-01。

## 8. 有限控制、coverage 與證據邊界

獨立 [checker.py](checker.py) 不 import 任何原 checker 決策。
生成 exclusive-create；`--check` 只讀計算、逐 byte 比對 [certificate.json](certificate.json)，
並核 BASE HEAD、69 份實讀 BASE 檔案 SHA256。正式結果及命令见 [checks.json](checks.json)。

| 控制 | 本輪實算範圍／判定 |
| --- | --- |
| singleton 必要介面 | c 的 4 個字面色 × k_r,k_s∈{1,2,3} × 8 軌道聯集＝288 項；92 項 contact 界觸發且成立，196 項不觸發并列缺失 contact 界；低 incidence 只容許通用 relation |
| 完整抽象容量介面 | 3 份各保存全部 16-pair compatibility／空 pair；side blocker、joint blocker、singleton22＋long residual 的局部等式觸發且成立；圖來源前提均不觸發 |
| both-short 計數 | m_r∈{2,3,4}、m_s∈{2,3,4,5} 的 12 個 scalar 預算；只留下 (2,2)/(2,3)/(3,2)，不代表圖實現 |
| BASE E4C 保存原圖 | 从54份原邊重建分量，選恰兩 mixed 的19圖；獨立重算190份框列接受性與完整接受 full lift |
| 原 spoke derivative | 19圖的47份「原 spoke × 原拒絕列」查詢全部接受，保存同圖字面 β 及完整 lift；全部 **not triggered**（X 未拒絕 β），沒有 N45-S source 正控制 |
| 精確來源 | 19圖無完整 canonical 933／941；保存 core degrees 皆55，此字段只作保存資料 inventory，未重跑 core 枚舉 |

抽象 singleton22＋long 控制说明零容量／singleton色對稱本身仍留必要介面；
它没有具名 graph、component full lifts、disk、完整Σ、Σ-criticality、β-minimality，
**不是來源反例**。19圖的 rotation、原 contacts／support 與原完整 R_P／fibres
仍由凍結 BASE JSON 及其 hash 保留；本輪不宣稱重建全部 component tuples。
完整圖接受／spoke-deletion lifts 是本輪獨立回溯的新增有限證據。
沒有「counterexample」格；缺前提的控制不寫成目標命題 PASS。

paper 承擔 S-01–06；Python 沒有核實任意大小拓撲、B-S0、N-diagonal 或 E2 證明。
沒有新 Lean theorem，未執行 lake build／axioms audit。
未重跑 E3／E4／E4C 全套、U1–U4、ES／ER 或其他上游分類；沿用 BASE 報告的
已列證據，既有 JSON 全不覆寫。

普通及 `PYTHONHASHSEED=17` 的 `--check` 均 exit0；證書 SHA256
`9acb2a6b40de32aeca60ecf9a5b33065c9cba60ad47f5243c1eccadf31f59a02`。
再執行生成命令對既有證書得到預期 exit1／FileExistsError，前後 bytes 不變。

由 canonical root 重播（保留的 BASE checkout 路徑見 inputs.json）：

```bash
python3 audits/2026-10-09-n45-s/checker.py --source-root /tmp/math-n45-s-20261009 --check
PYTHONHASHSEED=17 python3 audits/2026-10-09-n45-s/checker.py --source-root /tmp/math-n45-s-20261009 --check
```

| 文件／來源檢查 | 實際結果與範圍 |
| --- | --- |
| 69 份 BASE 輸入 hash／Git | 零 byte 漂移；獨立 checkout 保持 clean、HEAD=BASE |
| 獨立 BASE `check_docs.py` | **exit1**，2 個缺檔連結；586 Markdown、6982 links。兩個歷史 audit 目標未入 BASE Git，新 worktree 不含它們；不是本輪檔案修改造成 |
| 主工作樹 `check_docs.py` | exit0；587 Markdown、6997 links。此結果包含原工作樹留存的兩份 audit，不能改稱 fresh BASE 文件檢查 PASS |
| 獨立 BASE 正式 docs DocGraph | exit0；62 documents、213 relations、5 families，0 errors／notes |
| 主工作樹全域 DocGraph | **exit1**；保留 scratch 副本及並行 N45-U 的 source/docs 副本造成 duplicate IDs；具體路徑保存在 log，未刪副本隱藏失敗 |
| BASE／主工作樹 `git diff --check` | 均 exit0；新增檔另作逐檔 whitespace 與本報告本地連結核對，結果見 checks.json |

## 9. 驗收返回與寫入界線

任務狀態：完成可審窄命題／必要化約，等待交叉驗收；未由本執行者採納到共用報告。
CLAIM-ID 為 N45-S-01–06，全部適用 933／941、root 交換及任一原拒絕 β；
S-04 有明列的一般局部前提，S-05／06 的額外 short 條件如上。
本任務只處理原 spoke 省略，不宣稱 N45-U、原55、一般 N2、來源實現性或 E 完成。

findings：**N45-S-COVERAGE-01**，固定控制無 N2 45／54 spoke-core 前提觸發；
影響有限 source 校準，不是紙面反例。需要有具名圖、原邊、β、實際省略 e、
全部 contacts／tuples／full lifts 的控制才可增量交 N45-J 驗。
S-01–06 尚待 N45-A 核紙面；不把本輪自查當獨立驗收。
另記 **N45-S-DOC-01**：fresh BASE 缺兩個未追蹤的歷史 audit link targets；
`audits/2026-10-04-task-d5/c4/scope_ledger.json`、
`audits/2026-10-04-task-d2/integration_doc_changes.diff`。
影響 fresh checkout 文件完整性，來源與存在性核對在 validation_records.json；
共用文件修正不屬本任務，不以主工作樹 PASS 覆蓋此 FAIL。

L0 更新僅此任務目錄。L1 已核 BASE Kempe guide／STATUS 的45／54仍開放入口，
未改共同文件；本輪提出子型候選，不推升父题，不啟動上層摘要改寫。
任務的獨立輸出要求優先於 skill 的一般共用文件更新流程。
只新增 `audits/2026-10-09-n45-s/`；接手時已有 STATUS／guide／任務brief 變更保留。
來源零 byte 漂移、檔案 hashes、Git 狀態及重播命令见 [checks.json](checks.json)
與 [delivery.json](delivery.json)。未 commit／push／開PR／對外發訊息，未委派 sub-agent。
