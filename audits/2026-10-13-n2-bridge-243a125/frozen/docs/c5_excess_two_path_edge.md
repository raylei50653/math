# ε=2 雙 roots：原路徑接回 root 邊的 K₅ 排除

**提交整理（2026-10-03）**：本頁、checker 與研究紀錄的本次提交範圍、
實際重播及整理發現見 [九輪進展紀錄](history/2026-10-03-excess-two-dual-root-progress-commit.md)。
下文的未提交字句保留當輪語境；即時提交狀態以 Git 為準。

**後續（2026-10-03）**：[單 triangle 保留原兩點接回排除](c5_excess_two_triangle_edge.md)
已完成本頁的下一窄題：同枝原環 K₅ 及保留 z,w 的完整區段縮減，
528 份必要正常形中 T4 全收者都保持原單缺失。連同雙 triangle，
刪 zw 仍拒絕的相鄰 mixed 分支全部排除；其原刪邊圖必全收 Ω。
共同下界仍 ε≥2；下文保留本輪的原停止點。

2026-10-03，接手基準 `722bfa6`，保留上一輪未提交成果。接續
[原 root 刪除與邊接回](c5_excess_two_root_deletions.md) 的偶數路徑停止點，
依賴 [degree-4 樹分類](c5_tree_cores.md) 與 [odd-join 基底](c5_odd_join_cores.md)。
目前入口見 [Kempe 導覽](c5_kempe_guide.md)，實際驗證與跨對話摘要見
[研究紀錄](history/2026-10-03-excess-two-path-edge.md)。

**933／941 固定完整 Σ、edge-minimal induced-C₅ disk 來源若 ε=2，
roots 相鄰且刪原 zw 後仍拒絕某列，刪邊圖的全 degree-4 內部不可能是樹。**
此任意長度分支整型排除：既有分類迫原內部是偶數頂點路徑，所有內點
都接同一個原 singleton 框點，也各接至少一個其他框點。接回原 zw
形成的原內部環直接給 boundary-apex 圖中的 K₅ minor。

不需要刪掉或重新定位 z、w，也不需宣稱舊 run 縮減保持這兩點的 relation。
結合前輪的雙 triangle 排除，**刪 zw 後仍拒絕的相鄰 mixed 分支，
只剩單 triangle 加原樹枝。** 刪 zw 全收、no-mixed、非相鄰 roots 等
分支保留；共同下界仍 **ε≥2，尚未證 ε≥3**。
證據為任意大小紙面 minor 論證、沿用分類及 Python 固定具名控制；未新增 Lean theorem。

## 1. 前提與原圖

G 有限簡單，B=(b₀,…,b₄) 是指定有序 induced-C₅ disk 外框；
Σ(G) 是 933、941 或其整圖 D₅ 像，每條非框邊都嚴格擴大完整 Σ。
有效內部 H 非空連通，恰兩個完整 degree-5 roots z,w，其餘有效內點
完整 degree 四。原 zw 存在，且至少有一份原 mixed 分量。
令 N=G−zw，假設 N 仍拒絕 singleton 列 q，且 N 的有效內部是樹。

依 [前輪的原刪邊化約](c5_excess_two_root_deletions.md#4-相鄰-mixed刪原-root-邊的全-degree-4-化約)，
N 內部連通且全 degree 四，接受 T4；拒絕列的 minimal core 由飽和
就是整張 N，Σ(N)=Ω∖{q}。所以可以使用任意大小 degree-4 樹分類。
固定同一整圖的框、附件與 contacts，將 q 搬運至 q₄=01012；其唯一
singleton 框點為 b₄。這是一次整圖 D₅／色框對齊，沒有獨立重標原分量。

N 的原內部路徑記為 v₀,…,vₙ₋₁，n 偶數，保留全部原邊及實際框附件。
z=vᵢ、w=vⱼ，交換 roots 可令 i<j。因 G 簡單且 zw 是在 N 中刪掉的
原邊，z,w 不會在 N 路徑上相鄰，所以 j≥i+2。
原 H−{z,w} 的 mixed 正是中間原路段；兩端非空路段為各自 unary。

## 2. 分類留下的共同原框鄰點

樹分類證明同 palette 的所有中段點具有相同的**實際** boundary
neighborhood，且 palette word 至多兩 runs。縮成二／四／六內點只是
辨識可能的附件；回到原 N，每個 run 的全部頂點仍帶同一組原附件。

令 L={b₀,b₁,b₄}、R={b₂,b₃,b₄}、A={b₁,b₄}、C={b₂,b₄}。
接受 T4 的具名 q₄ 路徑基底恰為：

| 原附件族 | 基底數 | 任意長度的原附件序列 |
| --- | --- | --- |
| 空 word | 2 | L,R，或反向 R,L |
| 單 run | 4 | L,A^(2a),R 或 L,C^(2a),R，及各自反向；a≥1 |
| 兩 runs | 2 | L,A^(2a),C^(2c),R，及反向；a,c≥1 |

表中反向同時反轉整條具名路徑；不重新選附件或色框。空 word 沒有
可接回的內部 nonedge，因為只有兩個原內點且已相鄰。

二／四內點的原 disk 路徑基底保存於 odd-join 證書；兩-run 的兩份
原基底保存於 tree 證書。新 checker 先用保存的實際邊集重算全部
16 份 disk 路徑基底的完整 Σ：894 四份、1018 四份、1022 八份，
再以重算的 T4 判定選出上表八份，不以舊 Σ flag 決定收錄。
每份選入基底另核對原 apex rotation、完整 degree 四、原逐邊 q-critical
見證與全部實際附件。

因此對原 N 的每個內點 v 都有

\[
\boxed{b_4\in N_N(v)\cap B,\qquad
       (N_N(v)\cap B)\setminus\{b_4\}\ne\varnothing.}
\tag{1}
\]

任意長度的式 (1) 來自分類的原附件恆定性及八份基底的覆蓋；有限
染色控制不是一般分類的替代證明。此步只回讀每個原頂點的附件，
沒有把含 z,w 的原圖換成一張聲稱保持 marker relation 的短圖。

## 3. 原環與外側 apex 的五份 branch sets

較一般地，若 disk 圖的某個原內部環上，每個頂點都接同一原框點 b，
且各接至少一個 B∖{b} 的原框點，就不可能有 disk 嵌入。把環分為
三個非空、連通、兩兩接邊的原路段；加上 {b} 以及
{外側 apex}∪(B∖{b})，直接得到 K₅ minor。

在本題可把五份 branch sets 寫得更具名。於原 G 的 boundary-apex
圖中令外側 apex 為 α，取

\[
Z=\{z\},\quad P=\{v_{i+1},\ldots,v_{j-1}\},\quad
W=\{w\},\quad F=\{b_4\},\quad
X=\{\alpha,b_0,b_1,b_2,b_3\}.
\tag{2}
\]

這五份非空且互不相交。P 沿整段原路徑連通；X 由原 apex 星連通；
其餘是 singleton。Z–P、P–W 用原路徑的首末邊，Z–W 就是原 zw。
式 (1) 給 Z、P、W 各一條到 F 的原 spoke，以及各一條到 X 的原 spoke。
F–X 用 αb₄。十對 branch sets 全有原邊，收縮便是 K₅。

特別地，P 沒有被當作與原圖無關的抽象點：整段原頂點及其實際附件
都是 branch set 的 witness。z,w、所有框點、原 contacts 與 ownership
持續具名。證明只用這份原圖的一個 minor，不加不同列／不同根的跨度。

Disk 嵌入允許在外框外側加 α 接全 B，所以其 boundary-apex 圖必平面；
式 (2) 與 K₅ 非平面矛盾，整個原路徑接回分支排除。這個拓撲排除
不依賴接回後接受哪幾列，也不需要把兩端色 marginals 合成一份染色。

## 4. 完整有序色對與固定原圖控制

[Checker](../scripts/c5_excess_two_path_edge.py)／
[artifact](../artifacts/c5_excess_two_path_edge/observations.json) 保留上述八份
原基底，並加入同附件的固定 run 增長：單 run 用長度二、六，兩 runs
用 (2,2)、(4,6)，共十四份原路徑。這些長圖是紙面原環公式的控制，
不是任意長度覆蓋所需的 marker 縮減，也沒有新增一般圖 catalogue。

每份原路徑嘗試全部原內部 nonedges，共 226 份具名 zw 接回。
所有接回的實際 apex 邊集都有式 (2) 的 K₅ certificate；checker 核對
branch sets 的內部連通、互斥及十份跨集合的原邊。每份原圖另保存
原 z,w 路徑位置、原環、H−{z,w} 的全部原分量、contacts、ownership、
實際附件與支援。全部接回都是非 disk 的負控制。

對每份原路徑、原 (z,w) 及十列 β，保存原 N 的完整有序關係 Kβ
及每個 tuple 的同一份原路徑完整染色 witness；精確接回是

\[
K^{zw}_\beta=\{(a,b)\in K_\beta:a\ne b\}.
\tag{3}
\]

全部 2,260 次查詢都由原路徑動態傳遞保留兩個 marker 座標，再與
原邊集的獨立完整回溯比較；接回後另直接回溯核對式 (3)。原字面
色框共用，沒有獨立 S₄ 正規化。Witness 在 boundary_order／interior_order
下可重建完整染色；空 relation 明確保存。

固定接回的 Σ histogram 為 266:35、592:35、830:8、894:21、990:14、
1016:8、1018:21、1022:84。84 份仍接受 T4 者都保持 Σ=1022；
它們也全部帶原 K₅ minor。這個染色數字僅屬固定控制，任意長度來源
排除由 §2–3 的紙面覆蓋與原環公式負責。

## 5. 重播、信任界線與停止點

```bash
python3 scripts/c5_excess_two_path_edge.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_path_edge.py --check
python3 scripts/c5_excess_two_root_deletions.py --check
uv run --with networkx==3.5 python scripts/c5_tree_cores.py --check
uv run --with networkx==3.5 python scripts/c5_odd_join_cores.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

本輪實際重播與未重播範圍見 [研究紀錄](history/2026-10-03-excess-two-path-edge.md)。
任意大小的全 degree-4 分類、forcing/minor soundness 與 disk/apex 關係
沿用原報告的紙面及有限 topology 信任範圍。新 checker 直接核對 K₅
branch sets，沒有新增文獻 oracle 或 Lean theorem；`lake build` 不形式化式 (1)–(2)。

**停止點：** 相鄰 mixed、刪原 zw 仍拒絕時，原樹／偶數路徑分支已
整型排除，雙 triangle 已由前輪排除。下一窄入口是同樣原前提下，
N 的有效內部為單 triangle 加原樹枝：保留原 z,w 及它們在 triangle／
原枝的位置、原有序關係與所有附件，分析原 zw 接回。既有未保留這兩點
的 tail 縮減不能直接提供接回後的完整 Σ。

Σ(G−zw)=Ω 的相鄰 mixed、相鄰 no-mixed、非相鄰 mixed 與原 unary 側
例外仍保留。尚未排除所有 ε=2，未證 ε≥3、一般出口、來源實現或 `K∞=K≤5`。
