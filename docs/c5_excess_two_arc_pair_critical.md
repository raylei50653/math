---
docgraph:
  id: c5.excess-two-arc-pair-critical
  family: [c5, c5.excess-two, c5.arc2]
  related:
    - c5.excess-two-arc-component-slack
    - c5.excess-two-n2-ll-cut
    - c5.excess-two-n2-bridge
---
# E-ARC2：真子圖單拒絕與共同核心覆蓋

**後續（2026-10-13，N2-BRIDGE）**：[前提橋接與932來源排除](c5_excess_two_n2_bridge.md)
已排除原 E4 三列完整來源契約的 N2，包括另證的完整 mask 932；
E-ARC2 仍剩 N1 及相鄰 roots 來源，均保持 OPEN。本頁原前提、證明與當輪停止點保留。
完整 Σ933／941 契約的原55覆蓋由 [LL-CUT+diag](c5_excess_two_n2_ll_cut.md)完成，
前置45／54排除見 [spoke closure](c5_excess_two_arc_spoke_closure.md)；基本 LL-CUT 尚未獨立證成。

2026-10-11，基準 `fdbef272c9f74ed95a4dac644b1c7f8b071a7722`。
接續 [E-ARC2 原命題](c5_research_synthesis.md#81-猜想-e超額拒絕定律)；
目前入口及停止點見 [Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口)。
整理發布與本次重播範圍見[三點弧發布紀錄](history/2026-10-11-three-point-arc-publish.md)。

**後續（2026-10-11）**：[原分量共同重色限制](c5_excess_two_arc_component_slack.md)
將逐點(C)提升至同一原分量；完整N2前提接已採納N45-U後，每份原分量刪除全收，
非root點至多接兩個相鄰框點，真core只能省一條root-spoke。三點弧仍OPEN；下文保留本輪證明與控制。

**本輪未證成三點弧命題。** 新增的任意大小必要條件是：在原域的反例前提下，
每個保留 B 的真子圖至多拒絕一個三色 singleton 列。因此任意兩個不同拒絕列，
各取任意 minimal core，其原邊集聯集必為 G；每條非框邊刪除至少釋放
所選三列中的兩列。這比 E5 L1 的「真子圖可拒絕相鄰二列」更強。
推導沿用已採納的兩-root `(4,4)` 排除，不是該排除的新獨立證明。
45／54、原55及單-root例外沒有因此全排，E-ARC2 仍 **OPEN**。

## 1. 完整前提與證據層

G 為有限簡單圖，B=(b₀,…,b₄) 是指定有序 induced C₅ disk 外框。
Σ 是同一色框下完整十列的 S₄ 軌道，不商掉具名框位置；接受全部 T4，
每條非框邊 Σ-critical。有效內圖 H 忽略孤立私有點，
ε(G)=Σ_{v∈H}(deg_G(v)−4)=2，degree 包括全部原附件。
Q(G) 為拒絕的 singleton 位置。

主引理 §3 不要求目標 mask；它另用 §2 的 `|Z(G)|≤1`。
接入 E-ARC2 的 §4 則假設反例位於原域 1≤|Q|≤4，整圖共同 D₅ 搬運後
完整 Σ 為 941、933 或 940。940 以 i↦1−i 連同全部原資料搬至 933。
932 不屬原域，未在 §4 偷用固定完整 Σ 的 `(4,4)` 排除。

以下沿用的結果均有其原外部定理／紙面／有限末端信任鏈：

| 輸入 | 本輪使用的精確結論 |
| --- | --- |
| [E2 §2–3](../artifacts/c5_excess_one_e2/REPORT.md) | 有效 degree≥4、H 連通；degree-4 飽和；ε=0 時只拒絕一列 |
| [E2 §4–5](../artifacts/c5_excess_one_e2/REPORT.md) | 一般 T4／Σ-critical 來源的 ε=1 拒絕集為單點或相鄰 pair |
| [唯一 degree-5 相鄰列分離](c5_excess_one_subcovers.md#2-只用-t4-的-minimal-degree-5-相鄰列分離) | minimal qᵢ-core 若自己只有一個 degree-5 內點，其餘四，則接受 qᵢ₋₁、qᵢ₊₁；不假設完整 Σ 恰缺兩列 |
| [E3 飽和](../artifacts/c5_excess_two_e3/REPORT.md#21-共同-triple-critical-化約) | ε=2 的 degree-valid 子核心若保留全部 excess，便是原 G |
| [刪 root §3](c5_excess_two_root_deletions.md#3-全部拒絕列至多一份-root-省略例外) | 雙 degree-5 來源中，省略 root 的 minimal core 只能是全四原 unary 側；全部此類 core 至多對應一個拒絕位置 |
| [兩-root44 覆蓋](../artifacts/c5_excess_two_c44pp/REPORT.md)、[U1–U4 合成入口](c5_kempe_guide.md#3-停止點與保留缺口) | 完整 Σ933／941 或整圖像的兩-root `(4,4)` minimal core 已排除；其他 core 型保留 |

本輪新增的是下述紙面合成及固定來源控制。沒有新增 Lean theorem；
沒有重跑上游分類、大圖搜尋或全部舊排除。外部 degree-list／Gallai 的信任
沿用原報告；查閱的原始版本為
[Dvořák 講義 Lemma 7、Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)。
本輪新證明不另加一個未證的 Gallai 推廣。

## 2. 低 excess 核心與 Z(G)

所有子圖保留 B；「真」指至少缺一條原非框邊，忽略孤立內點。
minimal q-core 一律指其自己的 inclusion-minimal 拒絕性。
定義

\[
 Z(G)=\{i:\text{G 含有 }\varepsilon(K)=0\text{ 的 minimal }q_i\text{-core }K\}.
\]

**引理 1。** 接受 T4 的 disk minimal qᵢ-core K 若 ε(K)≤1，
則 Q(K)={i}。

*證明。* K 的 qᵢ-minimality 使每条非框邊同時 Σ-critical。
ε=0 用全 degree-4 單缺失。ε=1 時，E2 只容許 Q(K)={i}，
或 {i,j} 且 j 與 i 相鄰；後者違反唯一 degree-5 的相鄰列分離。∎

**引理 2。** 若 M⊆G 的每個有效內點 degree≥4，則 ε(M)≤2；
等號迫 M=G。因此 M 真包含於 G 時，ε(M)≤1。

*證明。* 在原有效內點集 I 及 M 的有效內點集 I_M 上，

\[
\varepsilon(G)-\varepsilon(M)
=\sum_{v\in I\setminus I_M}(d_G(v)-4)
 +\sum_{v\in I_M}(d_G(v)-d_M(v))\ge0.
\]

等號時，原 surplus roots 全部保留且 degree 不降；它們的全部原邊進入 M。
已保留的原 degree-4 點也保留全部 incident 邊。沿原連通 H 傳播得 M=G。
這裡 ε(G)>0 確保有保留的 root 可開始傳播，不把任意非 critical 子圖直接當來源。∎

## 3. 任意真子圖至多單拒絕

**定理 3。** 在 §1 的一般 ε=2 來源前提下，若 |Z(G)|≤1，則

\[
 \boxed{S\subsetneq G, B\subseteq S\quad\Longrightarrow\quad |Q(S)|\le1.}
 \tag{P}
\]

*證明。* 反設某個真子圖 S 拒絕兩列。從 S 反覆刪除不改變完整 Σ 的
非框邊，得到保留同一 B 的 Σ-critical 圖 M，且 Σ(M)=Σ(S)。
M 接受 T4，拒絕集非空；E2 §2 給有效 degree≥4、有效內圖連通。
M⊊G，所以引理 2 給 ε(M)≤1。

若 ε(M)=0，E2 給 |Q(M)|=1，矛盾。因此 ε(M)=1；E2 又給
Q(M)={i,j}，其中 i、j 相鄰。
分別在 **同一原 M** 取 minimal qᵢ-core Kᵢ 與 minimal qⱼ-core Kⱼ。
引理 1 表明 M 不可能自己是任何一列的 minimal core，故兩份 K 都是真子圖。

對 ε(M)=1、有效內圖連通的 M 使用同一飽和等式：若 ε(K)=1，
唯一 surplus root 的全部原邊保留，再沿原 degree-4 點傳播，迫 K=M。
所以兩份 K 的 excess 都為零。它們仍是原 G 的實際子圖，分別拒絕 i、j，
於是 {i,j}⊆Z(G)，違反 |Z(G)|≤1。∎

這個證明不要求 S 自己 degree≥4、連通或 critical；這些性質只在抽出的 M
上使用。沒有把不同子圖的色框正規化後再拼合。

**推論 3.1（任意兩核心覆蓋）。** 若 i≠j 都在 Q(G)，任取各自 minimal
cores Kᵢ、Kⱼ，則 Kᵢ∪Kⱼ=G。
否則其聯集是真子圖，仍拒絕兩列，違反 (P)。這是原邊集的聯集，
不是兩份 coloring witnesses 的拼接；不推出每個 Kᵢ 都等於 G。

**推論 3.2（逐邊釋放）。** 每條非框邊 e 滿足 |Q(G−e)|≤1。
故若 |Q(G)|=3，刪 e 至少釋放兩列；若 |Q(G)|=4，至少釋放三列。
反過來，全部單邊刪除滿足 (P) 就足夠：任意 S⊊G 包含於某 G−e，
刪邊單調性給 Q(S)⊆Q(G−e)。

## 4. 接入三點弧反例前提

E3＋D₈ 排唯一 degree-6 後，原反例恰有兩個 degree-5 roots r,s。
取任何 ε=0 的 minimal q-core K。
原 degree-4 飽和與 H 連通使 K 不可能同時省略 r,s。
若兩者都保留，K 自己的 degrees 都四，屬於已採納全排的兩-root44 身份。
若只保留一個，刪 root 引理使 K 為原 unary 側；所有這類 cores
至多對應一個拒絕位置。因此 |Z(G)|≤1，定理 3 適用。

這一步保留單-root例外，沒有聲稱 Z(G)=∅。不把固定完整 Σ 的44排除
搬到 932，亦不把有限控制中的零觸發當成原來源排除。

**原 spoke 的共同欄位限制。** 對任一內點 v，令 S_v=N_B(v)。
對 b_j∈S_v 定義

\[
 D_{v,j}=\{i\in Q(G):\exists b_k\in S_v\setminus\{b_j\},\ q_i(b_j)=q_i(b_k)\}.
\]

若 i∈D_{v,j}，在同一字面 qᵢ 下，每份 G−vb_j 染色都已由保留的 vb_k
滿足 v≠qᵢ(b_j)；因此刪 vb_j 不能釋放 i。由 (P)，必有

\[
 |D_{v,j}|\le1. \tag{C}
\]

對 canonical q₀=`01212`、q₁=`01202`、q₃=`01021`，
q₀、q₁ 皆在 b₂、b₄ 同色，所以 **任何內點都不能同時接 b₂、b₄**。
完整欄位算術給：

| 原完整 Σ | 禁止任何內點同接的框點對 | 三-spoke 支援只能是 |
| --- | --- | --- |
| 941 | 24 | 012、014、034、123 |
| 933 | 03、14、24 | 012、123 |
| 940 | 02、13、24 | 014、034 |

T4 另使每點至多三 spokes。表格與 E5 L4 的部分局部結果相同，
新增的是 **所有內點、所有 core 身份** 在完整目標前提下的共同適用性。
這仍只是必要支援限制，沒有證這些支援能實現，也沒有排盡保留支援。

## 5. 固定控制、反例與重播

[Checker](../scripts/c5_excess_two_arc_pair_critical.py) 只讀 ER 已保存的
179 個 critical 代表，以及同一原標號的 C44 全部 minimal cores。
沒有新圖搜尋；C44 的 core **完備性** 沿用其原報告，本輪重新驗證
所有列出的 cores 的完整 Σ 與逐邊 minimality，不重跑全部 core 搜尋。
原 disk 嵌入及搜尋覆蓋亦沿用 ER／C44，沒有由重算染色替代拓撲證據。

| 固定核對 | 結果 |
| --- | --- |
| 原代表與完整單邊刪除 | 179 張、4,138 次；全部與原完整 Σ 相同 |
| 已列 core occurrences | 206 份完整 Σ、4,466 次指定列刪邊 minimality 均通過 |
| `\|Z\|≤1` | 172 張 triggered and holds，實際全為 Z=∅；其中 6 張有至少兩個拒絕列 |
| 其餘 7 張 | not triggered：6 張 Z 有2點，1 張 Z 有3點；不是引理反例 |
| 觸發圖的不同拒絕列 minimal-core 聯集 | 6 組比較均等於原 G |
| 完整 Σ933／941 或整圖像 | 0 張，not triggered；不提供目標來源排除證據 |
| 去掉 Z 前提的較強說法 | counterexample：同一 Σ956 原圖有兩個單邊刪除仍拒絕相鄰 pair |

該負控制 Q(G)={0,3,4}，符合三點弧；原私有點為5、6、7，
degrees=(5,5,4)，內邊為 triangle 56、57、67，spokes 為
06、16、17、25、27、35、45、46。
刪45後 Σ=958、Q={0,4}；刪46後 Σ=1020、Q={3,4}。
其 |Z|=3，故不得刪除定理的 Z 前提。
完整邊、原 augmented rotation、cores 和刪邊接受列的整圖染色保存在
[observations.json](../artifacts/c5_excess_two_arc_pair_critical/observations.json)。
兩份負控制另經 numeric-order DFS 核對全部十列；主核對採既有獨立 frontier DP。

生成及重播命令：

```bash
python3 scripts/c5_excess_two_arc_pair_critical.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_arc_pair_critical.py --check
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
lake build
git diff --check
```

目前主產物 SHA-256 為
`38c817fbd42c6362a2eab02e251fa6a96f2783fe37e519d4a4fb40429fc798e7`。
Generator 以 exclusive create 寫入；重建請給新的 `--output`。
較早的完整 Σ 核對輸出保留為
[observations_initial.json](../artifacts/c5_excess_two_arc_pair_critical/observations_initial.json)，
它尚未加入 4,466 次 core minimality 核對，不是現行 `--check` 的比較對象。
首次整合曾將 ES 與 ER 的代表誤當同一字面標號，查找失敗、未寫出產物；
正式版直接使用 C44 引用的原 ER 圖及 SHA，不為了配對而獨立正規化 cores。

以上兩次 `--check` 均 exit 0，主產物 bytes／SHA 完全一致。
`check_docs.py` exit 0（613 Markdown、7,555 local links）；正式 docs 的
DocGraph exit 0（62 documents、213 relations、0 errors）。
`lake build` exit 0（8,831 jobs，保留既有 linter warnings）；
`git diff --check` exit 0。新引理沒有 Lean 化，build 不承擔其證明。
本輪未跑含全部 scratch 的全工作樹 DocGraph，也未重跑上游低 ε／44分類及 ES／ER搜尋。

## 6. 精確停止點

已證到：目標反例必滿足 (P)、任意兩核心覆蓋、逐邊多列釋放及 (C)。
這些條件尚容許 45／54 與原55核心，也容許至多一列的單-root全四例外。
**缺少的步驟仍是：在同一 disk 原图及其完整跨列 relations／fibres 上，
證明上述條件與 q₀、q₁、q₃ 共同拒絕不相容。**
目前沒有這個矛盾，也沒有符合目標全部前提的反例。

因此不更新任何 N45 父身份為 CLOSED，不把必要條件寫成 E-ARC2 證明，
不宣稱 ε≥3、一般出口或 `K∞=K≤5`。沒有 commit／push；既有五份未提交
入口文件修改保留，再添加本輪相連結的報告入口。
