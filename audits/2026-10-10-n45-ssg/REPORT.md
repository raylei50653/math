# N45-SSG：SS 原盾弧與 T4 增量獨立稽核

2026-10-10。BASE／實際接手 HEAD：`dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。

**獨立裁決：N45-SS-COST、N45-SS-UNTOP、N45-SS-U3、N45-SS-U2 在完整 SS contract 及下列 BASE／外部紙面信任內成立；未辨識新增 block gap。** 這只裁決幾何/T4 增量。SS 的實際 sole-component、單-root 三分與主命題採納交 SSA／根監督裁決。

本輪先讀 HANDOFF、STATUS、DOCUMENTATION 與普通檔案搜尋，未用 Graphify。沒有讀本輪 SSA、SSC 或根新 SS 裁決；沒有委派、共享修改、commit、push、PR 或外部訊息。所有新寫入均在本 fresh exclusive 目錄。

## 1. 凍結輸入、量詞與信任

[inputs.json](inputs.json) 區分必要 current work-delivery snapshots 與 BASE 原 Git blobs。**HEAD=BASE 不表示未提交 current 交付就是 BASE。** 新候選 [REPORT](frozen/current/audits/2026-10-10-n45-u-ss/REPORT.md)、[claims](frozen/current/audits/2026-10-10-n45-u-ss/claims.json)、[當前 authority](frozen/current/docs/c5_excess_two_nonadjacent_unit_core45.md)、[原 U paper](frozen/current/audits/2026-10-09-n45-u/REPORT.md) 及 [SU-A 舊採納裁決](frozen/current/audits/2026-10-09-n45-su-a/independent-judgment.json) 均是 current snapshots，不是 BASE blob。BASE 的盾弧、短支援與 unattached-boundary 文件由 `git show BASE:path` 直接取得，保留 blob OID、SHA256、命令與實際 exitlogs。

量詞是所有符合候選 §1 全部條件的任意大小有限簡單原 G：指定有序 induced C5 為 disk 外框；完整 Σ=933/941 或一次共同整圖 D5 像；每條原非框邊 Σ-critical；原 ε=2、有效 H 連通、full B-touch；恰兩個非相鄰完整 degree5 roots r,s，其餘有效原內點 degree4；H−{r,s} 恰為 unary U 與 mixed L,S 三個完整分量，one-sided、actual support 非空、L/S 兩側 incidence 正；U 唯一 root-contact rx、無 s 接線；X=G−V(U)=M 為同一原拒絕 literal β 的 inclusion-minimal 45/54 core，r 是降度側，所有 U 以外原邊完整保留；L long，S actual support 恰 singleton 且總 incidence≥4；原 incidence 等式、全部具名 contacts／attachments／ownership／bridges／rotation、共同色框、完整 relations、全部空非空 fibres/full lifts 保留。共同 D5/S4/root swap 只作用於整圖與整份資料。

本稽核將舊採納 U-WIT 當具名可搬用依賴，並重新核 SS 的前提映射。BASE [盾弧 §2–3](frozen/base/docs/c5_unary_shield_budget.md)、[短支援 §§1–4](frozen/base/docs/c5_short_support_singleton.md)、[無 spoke 外路補註 §2](frozen/base/docs/c5_excess_two_no_spoke_complete.md)、[連通外框 K4](frozen/base/docs/c5_degree5_tree_components.md) 是沿用紙面信任；沒有重證其所有上游分類。短支援/hub 鏈沿用 Dvořák Lemma 7 的 degree-list tightness 與 Theorem 10 的 Gallai/blockwise-uniform 刻畫。其 [原 PDF](frozen/base/audits/2026-10-04-task-d4/a3/gallai-primary-source.pdf) 已自 BASE 凍結並本輪 `pdftotext` exit0 讀取，沒有新增來源搜尋。T4 改色本身只依 [BASE unattached-boundary §1](frozen/base/docs/c5_unattached_boundary.md)，不需 Gallai、disk 或 minimality。

## 2. 四項逐 claim 裁決

| Claim | 獨立裁決 | 最小 block gap |
| --- | --- | --- |
| N45-SS-COST | 成立，原有序 U/L 費恰只容 (2,2)、(2,3)、(3,2) | 無新增缺口，依上述完整原前提與明列紙面信任 |
| N45-SS-UNTOP | 成立，U 原盾弧每個內點在整 U 省略 X 無內鄰 | 無新增缺口；不得省略 H−U 真連通、原面定義或 σ_U≠B |
| N45-SS-U3 | 成立，(3,2) 的兩個不同內點迫 Σ(X)=Ω，矛盾 β 拒絕 | 無新增缺口；須保全部 T4 與整 U 省略 |
| N45-SS-U2 | 成立，(2,2)/(2,3) 的唯一內點 m 迫 β 的 singleton 在 m，Σ(X)=Ω−{q_m} | 無新增缺口；β=q_m 指同一原 literal β 的 S4 pattern，不能重選 piece frame |

**COST 的真 witness 與外路。** 原 rx Σ-critical 給 γ∈Σ(G−rx)−Σ(G) 與一份完整 lift f。限制 f 到 G−U 得真正 outside witness ψ。若 ψ 能填回全部原 U，則得到原 G 的 γ lift，矛盾；γ 不需等於 core β。假如 U support 包含於原框邊 hk 的端點，full B-touch 給任一 t∈B−{h,k} 的真內鄰 z∈H−U。原 L/S 各連通且各有 r/s contacts，所以 r,s,L,S 所成 H−U 連通；在其中取 r–z 原路，再接 zt，得到避 U、路內點避 B 的原 outside path。U 唯一鄰 r，因而亦是 H−r 的完整分量，可套短支援/hub 論證；無直接 r spoke 也有明列外路補註。原 degree4、ψ 拒絕接回與此真外路排短 support，BASE 引理1(b) 給原 |σ_U|≥2。這不是從 β 的 F_U 非空、singleton 或有限控制推出收費。

L 的原 long support 由同一 BASE 引理1(b) 給 |σ_L|≥2。三份原 pieces 在同一 G one-sided，引理1(d) 給兩兩盾邊互斥，故原費總和≤5。只用 |σ_S|≥0，就得有序身份 (2,2)、(2,3)、(3,2)。沒有對 singleton S 收 pair 費，沒有借 LP 的 2+2+1，也沒有以 S incidence 換支援下界。舊 U-RES 的 σ_S=0 在候選有引用，本增量推論不依赖其等號。U/L 的 actual support 點數不先指定；若另用 BASE 引理2，長2/3弧分別有3/4個支援點，不能把長3硬填為三點。

**UNTOP 的同一原面。** K_U=B∪G[U]∪E(U,B)。H−U 的非框點真連通而不交 K_U，故位於 K_U 同一開內面 F_U。保留 root spokes、L/S 框附件的開邊部分也在此面：它們的非框端在 H−U，開邊不穿 K_U，只有框端點可碰 B。σ_U 正是該原面邊界沒有的原框邊，沒有任選 gap。COST 給 |σ_U|≤3<5，所以引理1(c) 的 σ_U≠B 條件適用，N_B(H−U) 避開所有盾弧內點；r/s spokes 與 L/S attachments 都在此集合內。X 恰刪整份 U，沒有殘留 U 片段，因此每個盾內點 v 的全部非框鄰點已被刪去，N_X(v)−B=∅。X 不需 full B-touch。長2有唯一 m；長3有兩個不同 m,n，兩個都被 restriction 覆蓋。

**U3/U2 的完整 lift 操作。** X 是原 G 子圖，故繼承所有 T4，且 B 仍 induced C5。任何 proper 三色 literal η 的色類大小為 2,2,1。若沒有內鄰的框點 v 不是 η 的 singleton，只改 v 到未用第四色 D，得到 proper T4 literal η′。取一份 X 的完整 η′ lift；在同一 coloring 中只把 v 改回 η(v)，其餘全部原頂點、contacts 與坐標固定。v 僅有兩個框鄰點，η proper 保證還原後仍合法。沒有拼合列或端點 marginals，也沒有同時改兩點。

(3,2) 的 m,n 至少有一個不是任意 η 的 singleton，故每個三色 η 都由一次上述操作延拓，連同 T4 得 Σ(X)=Ω，矛盾 β∉Σ(X)。長2唯一 m 則接受全部除 q_m 以外的 patterns；β 被 X 拒絕迫其原 singleton 恰在 m，進而 Σ(X)=Ω−{q_m}、Q(X)={m}。原 Σ 若已接受該 q_m，X⊆G 也接受，即立即矛盾。933 q2/index3/singleton b2 保留；941 也保留其全部實際拒絕列。共同 D5 搬整份 B/β/位置/masks，S4 搬同一完整 coloring，root swap 搬 ownership/fibres；沒有逐 piece 正規化。

## 3. 獨立固定算術與實際檢查

[controls.py](controls.py) 是本輪自寫、無 worker import 的極小固定 C5 arithmetic。normal 與 PYTHONHASHSEED=17 均 exit0，stdout/stderr byte equal；結果見 [controls.json](controls.json)，實際命令與 exitlogs 見 [checks.json](checks.json)。

- 240 個 literal proper rows：120 三色、120 四色；獨立生成十個 S4 pattern、T4 indices、q_i 對應與933/941拒絕 masks。
- 480 次合法單點三色→T4→原色的 boundary 檢查；1200 個兩個未接點／三色列檢查；五個單未接點所能覆蓋的 masks 恰 Ω−{q_m}。
- 20 份有序互斥 C5 U/L 弧：長身份 (2,2)/(2,3)/(3,2) 計數10/5/5，逐弧驗內點數與長3的4頂點算術。
- 原 q2 經共同 D5/S4 的240次作用與960次合法單點改色，singleton 位置與 literal 同步搬運。

**這些是驗算，不證原面、不生成原圖、不認證來源、不提供 target-source trigger。** 任意大小論證仍由 §2 紙面鏈承擔；SS source controls 未計算，不能說「觸發且成立」或零反例來源排除。

對 worker 正式 normal/seed17，本輪只凍結既有 exit0 receipt、比較兩份 stdout/stderr bytes 相等，並核必要選定輸入 hash；沒有在 fresh audit 出現後重跑 worker 的全工作樹 inventory verifier，也沒有把舊 inventory PASS 當作目前工作樹 PASS。根監督已在新增目錄前另做的 worker verify 不由本報告重新宣稱。

保留 worker 的真歷史 FAIL：初次 seal 資料未齊的 verifier exit1、pdftotext form-feed newline check exit1、BASE docs 缺兩歷史路徑 exit1、當時 whole-worktree DocGraph 重複 IDs exit1。其 JSON 與實際 stdout/stderr 已凍結。本輪未重跑这些治理檢查。authority 的兩個歷史 E4 byte-replay FAIL 亦保留其既有紀錄，本輪不將其改稱 PASS 或重跑。沒有 Lean、PC/PCA LP checker、新 graph/k 搜尋或新增 source realization。

## 4. 交付與停止點

[independent-judgment.json](independent-judgment.json) 逐項保留四項量詞、原前提、derived prerequisites、信任、裁決及最小 gap，並將候選其餘七項明列 out-of-scope。先封存本獨立裁決，再交根監督；[MANIFEST](MANIFEST.sha256) 與 [delivery](delivery.json) 绑定本目錄 payload。後封存只讀驗證使用本目錄自己的 frozen inputs／BASE 原 blobs，沒有全工作樹 inventory 假設。

已完成：完整 SS contract 內的四項幾何/T4 增量稽核。待 SSA／根裁決：實際 sole-component、原完整 relation 與單-root (5)/(4)/(3) 適用、N45-SS-EXCLUSION 及正式採納。仍不涵蓋 S spoke-omission LOW/HIGH/long、其他 U/core 身份、原55、一般 N2/E、ε≥3、指定 coloring repair、來源實現或新 Lean；沒有推一般閉合。
