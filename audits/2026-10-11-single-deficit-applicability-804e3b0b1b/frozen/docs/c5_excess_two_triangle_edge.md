# ε=2 雙 roots：單 triangle 保留原兩點的接回排除

**提交整理（2026-10-03）**：本頁、checker 與研究紀錄的本次提交範圍、
實際重播及整理發現見 [九輪進展紀錄](history/2026-10-03-excess-two-dual-root-progress-commit.md)。
下文的未提交字句保留當輪語境；即時提交狀態以 Git 為準。

**後續（2026-10-03）**：[原省略身份與雙 spoke 核心排除](c5_excess_two_mixed_core_spokes.md)
已核對 N 全收、唯一 mixed 的全部 proper core 原身份；(4,4) 且
保留 mixed 的雙 spoke 省略分支由 126 必要正常形／6,068 接回全排。
再後續[spoke＋unary](c5_excess_two_mixed_core_spoke_unary.md)、
[雙 unary](c5_excess_two_mixed_core_two_unary.md)及[省略原 mixed](c5_excess_two_mixed_omission.md)
亦全排，完成相鄰唯一 mixed 的 (4,4) 核心排除。
共同 ε≥2 不變，目前停止點見 [Kempe 導覽](c5_kempe_guide.md)。下文保留當輪語境。

2026-10-03，接手基準 `722bfa6`，保留前兩輪未提交成果。接續
[原路徑 K₅ 排除](c5_excess_two_path_edge.md) 的單 triangle 停止點，沿用
[原 root 刪除與邊接回](c5_excess_two_root_deletions.md)、
[triangle 接枝分類](c5_triangle_branches.md)、
[路徑枝正常形](c5_triangle_path_reduction.md)及
[任意第一分叉排除](c5_triangle_forks.md)。目前入口見
[Kempe 導覽](c5_kempe_guide.md)，實際驗證見
[研究紀錄](history/2026-10-03-excess-two-triangle-edge.md)。

**933／941 固定完整 Σ、edge-minimal induced-C₅ disk 來源若 ε=2，
兩個 degree-5 roots 相鄰且有原 mixed，則刪原 root 邊必接受全部十列：**

\[
\boxed{zw\in E(G),\quad\text{有原 mixed}\quad\Longrightarrow\quad
       \Sigma(G-zw)=\Omega.}\tag{1}
\]

新完成的是刪 zw 仍拒絕時的最後一種全 degree-4 內部：單 triangle 加
任意原樹枝。同枝兩點由原環 K₅ 排除；其餘兩點使用**保留原 z,w 的
區段縮減**，528 份完整有序色對正常形中，392 份 T4 全收者接回後
仍只缺原 q，違反原 zw 的完整 Σ minimality。前兩輪的樹與雙 triangle
排除共同完成式 (1)。

證據為任意大小紙面化約及 Python 固定必要域證書；分類的外部定理與
topology 信任範圍沿用原報告，未新增 Lean theorem。刪 zw 全收的相鄰
mixed、相鄰 no-mixed 與非相鄰雙 roots 仍保留，**共同下界仍 ε≥2，
未證 ε≥3、一般出口或 `K∞=K≤5`。**

## 1. 原來源與刪邊圖的精確前提

G 有限簡單，B=(b₀,…,b₄) 是指定有序 induced-C₅ disk 外框。
Σ(G) 屬於 933／941 的整圖 D₅ 軌道，接受全部 T4；刪任一非框邊
都嚴格擴大完整 Σ。有效內部 H 連通，恰有原 z,w 的完整 degree 五，
其他有效內點的完整 degree 四。原 zw 存在且 H−{z,w} 至少一份原
分量同時接兩 roots。C 的原邊、具名 contacts、ownership、actual
attachments、支援及同一嵌入環序保持。

反設 N=G−zw 仍拒絕 singleton 列 q。由
[原刪邊化約](c5_excess_two_root_deletions.md#4-相鄰-mixed刪原-root-邊的全-degree-4-化約)，
N 的有效內部連通、全部完整 degree 四，拒絕列 minimal core 飽和到
整張 N；所以 N 本身是 minimal q-obstruction，Σ(N)=Ω∖{q}。
已有分類只容許樹、單 triangle 加樹、直接 bridge 相接的雙 triangle。
樹由前輪原環 K₅ 排除，雙 triangle 的 512 份原接回已全部保持 Σ(N)。

以下只處理單 triangle。一次共同搬運整圖，使 q=q₄=01012、未用色
D=3、singleton 框點為 b₄；不獨立換名原分量。所有列的色對在同一
字面色框 U={0,1,2,3} 下記錄。原 z,w 必是 N 中不相鄰的兩個內點，
因為 G 簡單且 N 恰刪掉原 zw。

## 2. 任意大小分類的原附件資訊

沿用第一分叉排除，所有原外掛樹都是路徑；triangle 至多在兩個不同
頂點接枝。零枝時三個內點已兩兩相鄰，無原 zw 可接回。

有枝時，保留 triangle、原 branch root 與原 leaf 的 endpoint minor
落在十八份具名 canonical disk lifts：十六份單枝、兩份雙枝。
這是既有分類的覆蓋，未重新枚舉所有內部圖。固定 q₄，十八份的
triangle palette 都是 {D,2}；枝的強迫色 c 是 0 或 1。
路徑枝報告把每份**原**枝限制成以下兩種實際附件序列：

\[
\begin{array}{ll}
\text{單 run：}& X^{2a+1},L,\quad a\ge0;\\
\text{兩 runs：}& X,Y^{2a},L,\quad a\ge1.
\end{array}\tag{2}
\]

兩 runs 只出現在八份單枝 contexts，第一段恰一個原點；雙枝都只有
單 run。X,Y 各為兩個實際框鄰點，L 是原 leaf 的三個實際框鄰點。
若 c=0，X,Y 是 {b₁,b₄}、{b₃,b₄}；若 c=1，則是
{b₀,b₄}、{b₂,b₄}。因此每個原枝點，包括 leaf，都接 b₄ 且至少
接一個其他框點。這個資訊不能套到 triangle 頂點。

新 checker 用十八份原邊集重算十列 Σ、degree、逐邊 q-critical
witnesses 及保存的 apex rotations；八份兩-run 正常形也核對實際
附件與 rotation。原 177,280 個 canonical lifts 的完備性及任意大小
分叉／接線排除沿用其原論證，不以保存的 Σ flag 作新查詢 oracle。

## 3. z,w 同在一條原枝：不縮原兩點的 K₅

若原 z,w 在同一枝，原枝中的 z–w 路徑至少有一個中間點；原 zw
與這段路徑形成原環。取 branch sets

\[
\{z\},\quad P=\text{原枝中 z,w 間全部點},\quad\{w\},\quad
\{b_4\},\quad\{\alpha,b_0,b_1,b_2,b_3\}.\tag{3}
\]

α 是外側 apex。前面三組非空連通，首末原枝邊及原 zw 使它們
兩兩相接。式 (2) 給三組各一條到 b₄ 的原附件及一條到其餘 B 的
原附件；αb₄ 是最後一條接線。五組互斥，十對都有原邊，得到 K₅。
Disk 的 boundary-apex 圖必平面，因此整型不可能。

此步不加不同列的跨度，不壓縮 z,w；原 triangle 與另一枝可以完全
保留，minor 無須使用其全部原點。固定控制用 26 張原枝圖、280 份
同枝 nonedge 接回，逐一核對原 branch sets 的連通、互斥及十條原接線。

## 4. 保留 z,w 的完整區段縮減

剩餘原兩點只能是一個 triangle 點與一個枝點，或兩個不同枝上的點。
每枝因而至多有一個 marker。Triangle、每個 marker、原 leaf 都保持
為 singleton；不把含 marker 的原整枝套用舊 endpoint 縮減。

在每個同附件 run 裡，marker 把**未標記原點**分成前後區段。對每份
非空區段，奇長縮成一點、正偶長縮成兩點；空區段仍為空。
兩-run 的第一個原 X 點及原 X／Y 次序也保持。縮減只收縮同附件
的未標記原路段，B、z,w 不識別，原 marker 的 branch set 恰為其自身。
同區段的 boundary edges 在收縮後成為同一組實際附件；路徑首末邊
及原 zw 的兩個端點不變，所以 N 與 N+zw 都得到 boundary 固定、
保留兩個 marker 的 minor。原嵌入在這些內部收縮下誘導目標嵌入，
不為目標重新指定獨立環序。

**完整 relation 保持。** 固定任意 proper boundary coloring β，某區段
每點的共同可用色集 S=U∖β(X) 至少兩色。固定區段兩側原端點色：
若 |S|=2，路段必交替，可延拓性只依正長度奇偶；若 |S|≥3，任意
兩側端點色在任意正長度都可延拓。空區段只有原端點間的一條邊，
另作零長度類，不能與正偶長混同。逐區段替換，便保存 triangle、
所有 marker 與 leaf 在同一 β 下的完整聯合 relation。

令 N′ 是所得圖，仍用 z,w 表示保持的原 marker 座標，則

\[
K_\beta(N)=\{(f(z),f(w)):f\text{ 是原 N 的完整 β 染色}\}
            =K_\beta(N'),\qquad
\Sigma(N+zw)=\Sigma(N'+zw).\tag{4}
\]

每個 surviving tuple 有同一原圖的完整 witness；相同 endpoint 色可
按區段傳遞填回所有被縮原點。這是本輪新增的兩個 marker 聯合等價，
不從舊 bridge 介面等價推導它。其他原 contacts 的座標不宣稱逐一保留
為目標頂點；來源仍保存全部原分量／附件，且每個收縮都有原 branch
set 與目標映射，不把目標分量當成獨立重新正規化的原分量。

## 5. 528 份固定必要正常形與精確接回

單 run 的非葉 marker 兩側區段長度各在 {0,1,2}，總和為偶數，
恰五種；marker 為 leaf 時未標記奇長 run 縮成一點，共六種。
兩-run 中，marker 在 X 有一種、在 Y 有四種前後奇偶配置、在 leaf
有一種，亦共六種。另一個未標記單-run 枝縮成一點加原 leaf。

在十八份基底及八份兩-run contexts 中保留所有三個 triangle
位置、所有六種枝 marker 型及所有原 nonedges；雙枝再保留六乘六
份跨枝位置。這是式 (2)–(4) 導出的固定必要域，容許其中非 disk
或其他不滿足來源前提的正常形，不作來源實現判定。

| 原 marker 配置 | 必要正常形 |
| --- | ---: |
| Triangle／枝，單 run | 320 |
| Triangle／枝，兩 runs | 136 |
| 兩條不同原枝 | 72 |
| 合計 | 528 |

對每份正常形及十列 β，完整 triangle／tail DP 保留兩個 marker
座標，每個 tuple 保存該圖的完整內點染色；再與原邊集的獨立完整
回溯比較。加回 zw 的精確查詢始終是

\[
K^{zw}_\beta=\{(a,b)\in K_\beta:a\ne b\},\tag{5}
\]

並與接回後的直接回溯比較；共 5,280 次完整正常形查詢。

| 接回後完整 Σ | 數量 | 接受全部 T4 |
| --- | ---: | --- |
| 894 | 52 | 否 |
| 990 | 32 | 否 |
| 1018 | 52 | 否 |
| 1022=Ω∖{q₄} | 392 | 是 |

因此原來源接受 T4 時，式 (4)–(5) 迫 Σ(G)=Σ(N)=Ω∖{q}。
這既不可能是 933／941，也違反原 zw 的完整 Σ edge-minimality。
同枝已由 §3 排除，所以單 triangle 分支任意大小全部封口。

## 6. 原長圖控制、證據界線與接續

[Checker](../scripts/c5_excess_two_triangle_edge.py)／
[artifact](../artifacts/c5_excess_two_triangle_edge/observations.json) 另對每份
正常形的每個正未標記區段增加兩個原點，保存共 528 張原長圖：完整
原邊、triangle／枝順序、z,w、原分量 contacts、ownership、實際
attachments／support、全部收縮 branch sets 及原長圖的 tuple witnesses。
縮圖前後的十列完整色對全相等；N 和 N+zw 的 quotient 邊集各自
核對。19 份長圖的 3,040 次獨立 pinned 色對回溯也逐纖維比較，包含
空纖維；最長原圖有 28 個頂點，包括五個框點。

區段傳遞另核對十一份 |S|≥2 的色集、1,408 次 endpoint 比較及
零區段的差異。280 份同枝 K₅ 控制另有 2,800 次完整色對查詢。
實際同枝圖的一列有 K={(0,0),(3,3)}：兩 marginals 都為 {0,3}，
相乘會誤造異色對，原完整 K 接回 zw 卻為空。Artifact 保留這份
實際圖／列與完整 witnesses，沒有以 marginals 接合。

十八份基底及任意大小原附件分類由沿用的紙面／有限 topology 證據
承擔；新 Python 證固定必要域、明列 minor 與完整 relation 代數。
固定長圖控制不是任意長度證明或 disk 實現證書。`lake build` 不把
新區段縮減與式 (1) 形式化為 Lean theorem。

```bash
python3 scripts/c5_excess_two_triangle_edge.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_triangle_edge.py --check
python3 scripts/c5_excess_two_path_edge.py --check
python3 scripts/c5_excess_two_root_deletions.py --check
uv run --with networkx==3.5 python scripts/c5_triangle_path_reduction.py --check
uv run --with networkx==3.5 python scripts/c5_triangle_forks.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

**停止點：刪原 zw 仍拒絕的相鄰 mixed 分支全部排除。** 剩餘相鄰
mixed 必有 Σ(N)=Ω，每份原拒絕列的所有 N 染色都令 z=w；接受列
必有同一列的一份 z≠w witness。下一窄入口是在**原 N 全收、恰一份
原 mixed**的情形，核對拒絕列 minimal cores 必保留原 zw 後的原省略
身份與 degree：proper core 至少一個 root 降到四；(4,4) 時若保留原
mixed，其 root contacts 只能共用單接點。完整 G 若本身是 q-core，兩 roots 都仍為五，
不能套唯一 degree-5 分離定理；詳見原 root 報告的飽和界線。

相鄰 no-mixed、非相鄰 mixed、全收的多 mixed 及 unary 側例外亦
保留。式 (1) 是來源必要條件，尚未排除所有 ε=2，不提高為 ε≥3。
