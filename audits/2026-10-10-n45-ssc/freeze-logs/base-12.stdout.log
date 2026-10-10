# ε=2 雙 degree-5：刪 root 的完整 Σ 與原 root 邊省略

**提交整理（2026-10-03）**：本頁、checker 與研究紀錄的本次提交範圍、
實際重播及整理發現見 [九輪進展紀錄](history/2026-10-03-excess-two-dual-root-progress-commit.md)。
下文的未提交字句保留當輪語境；即時提交狀態以 Git 為準。

**後續（2026-10-03）**：[原路徑接回 zw 的 K₅ 排除](c5_excess_two_path_edge.md)
完成樹／偶數路徑；[單 triangle 保留原兩點接回排除](c5_excess_two_triangle_edge.md)
再完成最後一型。連同本頁雙 triangle，刪 zw 仍拒絕的相鄰 mixed
分支全部排除，所以其原刪邊圖必全收 Ω。共同下界仍 ε≥2。
下文保留本輪的原停止點。

2026-10-03，接手基準 `722bfa6`。接續
[唯一 degree-6 的 ε=2 分支排除](c5_excess_two_no_spoke_complete.md)，
在剩餘的兩個完整 degree-5 roots 上建立任意大小的來源必要條件。
目前入口見 [Kempe 導覽](c5_kempe_guide.md)，實際驗證與跨對話摘要見
[本輪紀錄](history/2026-10-03-excess-two-root-deletions.md)。

**933／941 固定完整 Σ、edge-minimal induced-C₅ disk 來源若 ε=2，
刪除至少一個原 root 必接受全部十列；另一個刪 root 圖至多只缺一列。**
相鄰 roots 且存在 mixed 原分量時，兩個刪 root 圖都必全收。
非相鄰 roots 必有 mixed；全部拒絕列中，至多一列能有省略任一原 root
的 minimal core，且該 core 是具名的原 unary 側、全 degree 四、恰只缺該列。

相鄰且有 mixed 時，刪原 root 邊後若仍拒絕某列，整張刪邊圖就是全
degree-4 minimal core。兩份以上原 mixed 分量會產生長度至少四的環，
故刪 root 邊必全收；恰兩 triangle 的六內點分支另由 512 次完整同源
接回排除。剩餘分支仍保留，**共同下界仍 ε≥2，未證 ε≥3**。
證據是紙面來源化約、沿用全 degree-4 分類的外部定理與 topology 依賴，
以及 Python 固定必要域控制；未新增 Lean theorem。

## 1. 同一原來源、原分量與兩種 minimality

G 有限簡單，B=(b₀,…,b₄) 是指定有序 induced-C₅ disk 外框。
完整 Σ(G) 是 933、941 或其整圖 D₅ 像，接受全部 T4；每條非框邊 e
都有 Σ(G−e)⊋Σ(G)。沿用
[容量報告的來源結構](c5_independent_support_capacity.md#1-兩種-minimality-與來源的基本結構)，
有效內部 H 非空連通，原 roots 恰為 z、w，完整 degree 都是五，
其餘有效內點完整 degree 四。忽略孤立內點。

固定被拒絕的 singleton 列 qᵢ，minimal qᵢ-core M 是包含 B 的
inclusion-minimal 拒絕子圖。M 接受 T4，每個有效內點在 **M 自己**
的完整 degree 至少四，且其有效內部連通。Σ(M) 不必等於 Σ(G)，
原 G 也不自動是任何指定 qᵢ 的 minimal obstruction。

C 始終是原 H−{z,w} 的連通分量，保存原邊、具名有序 contacts、
全部實際 boundary attachments、support、ownership 與嵌入環序。
每份 C 至少接一個 root；只接 z 或 w 者稱 unary，兩者都接者稱 mixed。
共鄰點始終只有一個原頂點座標，同時帶兩個 incidences。
定義

\[
\delta=1_{zw\in E(G)},\qquad
m_z=\sum_{C\text{ mixed}}|N_G(z)\cap C|,\qquad
m_w=\sum_{C\text{ mixed}}|N_G(w)\cap C|.
\tag{1}
\]

H 連通使 δ+m_z≥1、δ+m_w≥1。δ=0 時至少有一份 mixed，故
m_z,m_w≥1；兩個根的 nonadjacent 情形不可能是 no-mixed。

**Degree-4 飽和。** 若 M 含原 C 的任一有效內點，該點的 M-degree
至少四，而 G-degree 恰四，所以保留其全部原 incident 邊。沿 C
連通傳播，M 必保留整份原 C、全部原附件及所有 root incidences。
因此每份原 C 在 M 中只能全取或全不取；這不是將原 relation 換成
端點 marginals。若 M 不含任何原 root，就不可能含原 C，因而不能拒絕 qᵢ。

另一個直接後果是：若 M 中 z、w 的完整 degrees **都仍為五**，
M 就保留兩 roots 的全部原 incident 邊，再由飽和傳到每份 C，故

\[
\deg_M(z)=\deg_M(w)=5\quad\Longrightarrow\quad M=G.
\tag{2}
\]

式 (2) 沒有證成一般雙 root 的相鄰列分離。
[唯一 degree-5 的相鄰列分離](c5_excess_one_subcovers.md#2-只用-t4-的-minimal-degree-5-相鄰列分離)
只適用於 M 自己恰有一個 degree-5 內點；不能用它排除非相鄰雙 roots 的原 G。

## 2. 刪 root 與具名 unary 側的完整 Σ 恆等式

令 S_z 保留 B、z、**全部**原 unary-at-z 分量及其全部原邊與附件，
不保留 w、mixed 或 unary-at-w；S_w 同樣定義。這是 G 的實際子圖，
不是抽象側 profile。其 root degree 是

\[
\deg_{S_z}(z)=5-\delta-m_z,\qquad
\deg_{S_w}(w)=5-\delta-m_w.
\tag{3}
\]

所有保留的 unary 點仍完整 degree 四。由 δ+m_r≥1，兩側的 root
degree 都至多四。

**完整刪 root 引理。** 對所有 proper boundary colorings β，

\[
\boxed{\Sigma(G-w)=\Sigma(S_z),\qquad
       \Sigma(G-z)=\Sigma(S_w).}
\tag{4}
\]

證明以刪 w 為例。限制 G−w 的任一染色便得到 S_z 染色。反向先固定
同一 β 下 S_z 的一份完整染色，特別固定 z 色 a。對每份 mixed C，
扣除實際 boundary 色及 z-contact 上的 a；由原完整 degree 四，
每點剩餘 list 至少等於 deg_C，而任一原 w-contact 因 w 已刪除而
留有嚴格 slack。連通 C 可由
[生成樹 slack 引理](c5_adjacent_degree5_interfaces.md#4-degree-4-的-tightness共鄰點與分量解除)
填入。對每份 unary-at-w C，同一理由在其原 w-contact 留下 slack。
各原 C 在同一 β、同一 a 下選完整見證即可拼回 G−w；交換 roots 得另一式。

這個證明保留每份 C 的完整關係。式 (4) 只給刪 root 圖的完整 Σ，
沒有把 mixed relation 分成兩個獨立側，也沒有提供原 G 的逐染色 repair。

## 3. 全部拒絕列至多一份 root 省略例外

若 M 是拒絕 qᵢ 的 minimal core 且省略 w，飽和使 M 不能保留任何
mixed 或 unary-at-w C；又不能同時省略 z，故 M⊆S_z 且含 z。
若 δ+m_z≥2，式 (3) 使 z 的 M-degree 至多三，矛盾。
所以只可能 δ+m_z=1，此時 z 的 S_z-degree 恰四。
M 含 z 就必取 S_z 的全部 z-incident 邊，再沿 unary 飽和傳播，得到

\[
\boxed{w\notin M\ \Longrightarrow\
       \delta+m_z=1,\quad M=S_z,\quad
       \Sigma(S_z)=\Omega\setminus\{q_i\}.}
\tag{5}
\]

最後的完整 Σ 等式沿用
[全 degree-4 單缺失定理](c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論)。
反之，若 S_z 拒絕某列，取其 minimal core；同一飽和證明使 core
就是 S_z，因此 S_z 要麼接受 Ω，要麼恰只缺一列。S_w 同理。

兩側不可能同時拒絕，甚至不能同時拒絕同一列。若都拒絕，它們的
有效內部各連通，接受 T4 的拒絕支援引理使各碰至少四個框點。
S_z、S_w 的內部互不相交，兩份四點支援在 C₅ 環序中必有交錯端點，
違反 disk 路徑分離；詳見
[原四點支援交錯引理](c5_independent_support_capacity.md#12-兩份四點支援不能由不交的內部連通圖承擔)。
這裡使用同一原嵌入的實際附件，沒有把兩份任選最短 hulls 相加。

結合式 (4)、(5)，得到：

| 原 root 配置 | 完整刪 root Σ／省略 core 必要條件 |
| --- | --- |
| 任意雙 degree-5 | 至少一個刪 root 圖全收 Ω；另一個至多只缺一列。全部拒絕列中至多一列有任何省略原 root 的 minimal core |
| 相鄰且有 mixed | δ=1、m_z,m_w≥1，所以兩個刪 root 圖都全收；每份被拒絕列的每份 minimal core 都含兩 roots |
| 相鄰且 no-mixed | δ=1、m_z=m_w=0；兩側至多一側只缺一列，不能直接宣稱兩個刪 root 圖都全收 |
| 非相鄰且 m_z≥2 | G−w 全收；每份 minimal rejected-row core 都含 w |
| 非相鄰且 m_w≥2 | G−z 全收；每份 minimal rejected-row core 都含 z |
| 非相鄰且 m_z,m_w≥2 | 兩個刪 root 圖全收；每份 minimal rejected-row core 都含兩 roots |
| 非相鄰且有省略 w 的 core | m_z=1，恰一份 mixed 且其 z-incidence 恰一；core 必為原 S_z，全 degree 四、完整 Σ 只缺該列。其餘列的每份 core 含兩 roots |

在最後一型，因已存在只含 z 的 core，而任何兩份 minimal cores 都
共用一個原 root，所以 **所有** minimal rejected-row cores 都含 z。
這個共同 root 結論只在有此例外時成立；沒有把一般 pairwise intersection
任意升成所有 cores 的共同交集。

對 933 至少有三個拒絕位置、對 941 至少有兩個拒絕位置，其每份 core
都必含兩 roots。這是原 root **存在性**，不是兩 roots 在 core 中都 degree 五。
在式 (4) 已提供刪 root 延拓的那些列，可安全使用
[完整條件容量公式](c5_independent_support_capacity.md#3-degree-excess-是缺額及重疊的精確容量預算)
D_r+O_r=1；另一 root 色 η 必來自該列同一份刪 root 染色。
不同 roots 的見證仍可能不同，不能因此合成一份跨 root 的共同染色或跨度。

## 4. 相鄰 mixed：刪原 root 邊的全 degree-4 化約

另令 δ=1 且至少一份原 mixed C。記 N=G−zw。Mixed 提供避開 zw
的原 z–w 路徑，所以 N 的有效內部仍連通；兩 roots 的 N-degree
都是四，其餘內點亦完整 degree 四。N 繼承 disk 與全部 T4。

若 N 拒絕 qᵢ，取其 minimal qᵢ-core。全部內點 degree 四及內部連通
使該 core 飽和到整張 N，因此

\[
\boxed{\Sigma(G-zw)=\Omega\quad\text{或}\quad
       \Omega\setminus\{q_i\},\qquad q_i\notin\Sigma(G).}
\tag{6}
\]

第二型中 N 自己就是 minimal qᵢ-obstruction，不能只取一份未具名
marker core 再忽略原邊。其任意大小分類沿用全 degree-4 合成：內部是
樹、單 triangle 加樹，或兩個頂點互斥的 triangles 由直接 bridge 相連。
最後一型恰六內點且沒有外掛樹，見
[兩 triangle 的任意大小化約](c5_two_triangle_blocks.md#1-範圍與結果)。

若原 G 至少有兩份 mixed C、D，它們各給一條 z–w 路徑，內部互不
相交，長度各至少二。兩路合成 N 中長度至少四的簡單環。上述全
degree-4 minimal core 分類的所有簡單環都只是 triangle，故第二型
不可能，得到

\[
\boxed{\text{相鄰 roots、至少兩份原 mixed}\quad
       \Longrightarrow\quad\Sigma(G-zw)=\Omega.}
\tag{7}
\]

同一工具還給條件式省略限制：若某份 minimal q-core 保留 zw，但在
自己圖中 z、w 的 degrees 都降到四，該 core 是全 degree-4。因此
它最多保留一份原 mixed，且該份 C 的原接點必為
P_C^z=P_C^w={x}，共用同一 x。兩份 mixed 會給四環；不同接點間的
原 C 路徑與 zw 會給長度至少四的環；額外不同的 root 接點亦如此。
這只限制被該 core **整份保留**的原 C，未將任意大的 C 換成 singleton。

## 5. 兩 triangle 六內點分支的完整接回排除

固定 q₄=01012。沿用
[兩 triangle 證書](../artifacts/c5_two_triangle_blocks/observations.json)
保存的 64 份具名直接-bridge q₄-core N；每份有六個內點、兩個原
triangles、七條內部邊及全部實際 boundary attachments。
它們是固定內部模板標號的 64 份 lifts，不是 64 個同構類。

若式 (6) 的第二型落在兩 triangle，原 G 恰為 N 加回原 root 邊 zw。
z、w 是 N 中原本不相鄰的兩個內點；六內點共有十五對，N 有七條
內邊，所以只需保留原邊資料、嘗試八份具名 nonedges，共
64×8=512 次。全部框邊和實際附件不變；不是重新枚舉來源圖，也
沒有壓縮原 G 的 path、tail 或外枝。

對每個 N、具名 (z,w) 和每個十列 β，保存 N 全部染色在有序
(z,w) 上的完整 relation K_β。加入原邊的精確查詢為

\[
Z_{N+zw}(\beta)=\{(a,b)\in K_\beta:a\ne b\}.
\tag{8}
\]

每個 surviving 色對有同一份 N 全染色 witness；式 (8) 與直接在
原完整邊集上回溯核對。結果是 **512 份接回全部仍為 Σ=1022**，
即仍只拒絕 q₄。整圖 D₅ 搬運同時搬動 q、contacts、全部原邊與
attachments，故覆蓋任意 singleton 位置。

因此這一型既不可能是完整 Σ=933／941，也違反原 root 邊必嚴格
擴大 Σ 的來源 minimality：Σ(G−zw)=Σ(G)。染色排除容許接回圖
不限 disk，是涵蓋真實來源的放寬。原 64 份 N 的保存 apex rotations
會驗證；沒有為全部 512 份接回圖宣稱新的 disk 實現。

## 6. 證書、重播與精確停止點

[Checker](../scripts/c5_excess_two_root_deletions.py)／
[artifact](../artifacts/c5_excess_two_root_deletions/observations.json)
保存既有 64 份具名來源、原邊與附件、原 q-critical／degree 控制、
原 apex rotations，以及 512 份接回的十列完整有序 root-pair relations、
字面色框下的 witness、直接回溯與式 (8) 的比較。
對既有 128 份原 disk 基底先以實際邊集重算完整 Σ，再辨識其中
64 份 q₄ 基底，不以保存的接受／排除 flag 作 oracle；接回共有
5,120 次十列 edge 查詢。

[固定刪 root 控制](../scripts/c5_excess_two_root_deletion_controls.py)
另保存三張明列邊的 ε=2 圖，包括相鄰共鄰接點、非相鄰四-spoke
及非相鄰原 unary-edge 例外。60 次刪 root／原 unary 側的延拓色集
比較全相等，400 份固定另一 root 色的原分量完整接點關係保留所有
tuple witnesses。這些只是固定染色控制，不帶 disk、Σ-minimality
或 933／941 來源前提。第三張原圖的完整 Σ 是 958，G−z 為 959、
G−w 為 1022，兩側各缺不同 singleton；兩份原 unary 側的實際支援
皆為全部五個框點，且內部互不相交，由 §3 的交錯路徑論證可知
它不能是 disk。這是刪除 disk 前提便允許兩份 root 省略例外的
負控制，不是只有一例外的 disk 來源證書。

二元關係代數另窮盡全部 65,536 份 U² 子關係，核對式 (8) 的
同 tuple 異色過濾。負控制
K₁={(0,0),(1,1)}、K₂={(0,1),(1,0)} 的兩個端點 marginals 相同，
接上原 root 邊後的允許對數卻分別為零、二。這只是完整 relation
不可由 marginals 取代的代數控制，不聲稱兩份關係是 disk 來源。

Root 刪除與支援交錯的任意大小結論由 §1–4 的紙面證明負責；
有限接回控制不替代那些一般推導。

```bash
python3 scripts/c5_excess_two_root_deletions.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_root_deletions.py --check
python3 scripts/c5_independent_support_capacity.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
uv run --with networkx==3.5 python scripts/c5_two_triangle_blocks.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

本輪執行及未重播範圍以 [本輪紀錄](history/2026-10-03-excess-two-root-deletions.md)
為準。全 degree-4 分類的 degree-choosability、Gallai、minor 與有限 topology
證據保持既有信任界線；本輪 Python 不形式化它們，`lake build` 亦不表示
新增 Lean theorem。未證一般出口、來源實現或 `K∞=K≤5`。

**停止點：** 原 root 刪除已縮到至多一份單缺失例外；相鄰且有 mixed
時兩個刪 root 圖全收。相鄰 mixed 的原 root 邊若刪後仍拒絕，兩
triangle 分支已排除，且原 mixed 只能恰一份。**下一窄入口是相鄰、
恰一份原 mixed、Σ(G−zw)≠Ω，且 G−zw 的全 degree-4 內部為樹。**
沿用 [樹核心結構](c5_tree_cores.md#1-結論與限制)，這份原內部是偶數
頂點路徑；保存原邊 zw 的兩個具名端點 z、w 及其原路徑位置、
整條原路徑與實際附件，直接分析同源接回 zw。不得從未保留這兩點的既有 run 縮減
偷推接回後的完整 Σ。

刪原 root 邊後為單 triangle、Σ(G−zw)=Ω 的相鄰 mixed、no-mixed、
非相鄰原 mixed 及具名 unary 側例外仍保留。
一般 path／tail 不作保持 marker 的縮圖，完整 relations、原 contacts、
實際支援與同一共享色框持續保存。這些必要條件尚未排除全部 ε=2，
故不能提高共同下界至 ε≥3。
