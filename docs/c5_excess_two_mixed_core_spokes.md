# ε=2 唯一 mixed：原省略身份與雙 spoke 核心排除

**提交整理（2026-10-03）**：本頁、checker 與研究紀錄的本次提交範圍、
實際重播及整理發現見 [九輪進展紀錄](history/2026-10-03-excess-two-dual-root-progress-commit.md)。
下文的未提交字句保留當輪語境；即時提交狀態以 Git 為準。

**後續（2026-10-03）**：[原 spoke＋unary 省略](c5_excess_two_mixed_core_spoke_unary.md)
及 [兩側原 unary 省略](c5_excess_two_mixed_core_two_unary.md)均已由
同原固定支援 transport 與明示收縮星 subdivisions 整型排除。
因此保留 mixed 的 (4,4) core 全部原省略身份均不可能；若有
(4,4) core，必只省略 incidence-(1,1) 的原 mixed。下文保留當輪雙 spoke 結論；
共同 ε≥2 不變，目前停止點由 Kempe 導覽維護。再後續
[省略原 mixed 必全收](c5_excess_two_mixed_omission.md)亦已排除最後身份，
故相鄰且恰一份 mixed 的 (4,4) rejected-row cores 全部不可能。

2026-10-03，接手基準 `722bfa6`，保留原 root 刪除、原路徑及單 triangle
接回的未提交成果。接續 [單 triangle 報告](c5_excess_two_triangle_edge.md)
留下的原 N=G−zw 全收分支；目前停止點見 [Kempe 導覽](c5_kempe_guide.md)，
本輪驗證及跨對話摘要見 [研究紀錄](history/2026-10-03-excess-two-mixed-core-spokes.md)。

**新增排除：933／941 的 ε=2 相鄰雙 roots、恰一份原 mixed 來源，
任何 minimal rejected-row core 若兩 roots 都降到四且保留原 mixed，
其兩個原省略因子不能都是 spokes；至少一份必是原單接點 unary。**

本輪另給全部 proper core 的原省略身份表，並把保留 mixed 的全
degree-4 core 限制到原共鄰 triangle 及兩種原 mixed 形狀。
6,068 次具名雙 spoke 接回全部無兩候選的 D₅ 像；保留原 z,w 的
任意大小化約由紙面傳遞證明負責，Python 核對固定必要域。
**共同下界仍 ε≥2，尚未證 ε≥3；未新增 Lean theorem。**

## 1. 同一原圖與前提

G 有限簡單，B=(b₀,…,b₄) 是指定有序 induced-C₅ disk 外框；
完整 Σ 是 933、941 或其整圖 D₅ 像，且刪去每條非框邊都嚴格擴大 Σ。
有效內部 H 非空連通，恰兩個完整 degree-5 roots z,w，其餘有效
內点完整 degree 四。本輪要求原 zw 存在，H−{z,w} 恰一份原 mixed C。
其他原分量為 unary，保持所有原邊、實際附件、有序 contacts、ownership
及原嵌入環序；共鄰點只佔一個頂點座標。

[前序結果](c5_excess_two_triangle_edge.md#6-原長圖控制證據界線與接續)
給 Σ(N)=Ω，其中 N=G−zw；兩個刪 root 圖亦全收。
固定 G 拒絕的 singleton 列 q，取包含 B 的 inclusion-minimal q-core M。
因此 M 必含 z,w 及原 zw。M 繼承 disk 與全部 T4；G 不自動是 q-core。

Degree-4 飽和使每份原 H−{z,w} 分量在 M 中只能全取或全不取；
保留時全部原附件、內邊及 root incidences 都仍在，見
[原 root 報告](c5_excess_two_root_deletions.md#1-同一原來源原分量與兩種-minimality)。
因 M 的每個有效內點 degree 至少四，兩 roots 各只能失去零或一條
原 incidence。若都仍為五，飽和迫 M=G。

## 2. 全部 proper core 的具名省略表

把每條原 root-spoke 及每份完整原分量視為具名因子。
spoke 的 incidence 向量是 (1,0) 或 (0,1)，unary 是 (k,0) 或 (0,k)，
唯一 mixed 是 (k,ℓ)，k,ℓ≥1。原 zw 保留，不列為省略因子。
兩側其他 incidences 各總共四。令 I 是 M 省略的原因子身份集，則

\[
\sum_{f\in I}(k_f,\ell_f)
   =(5-\deg_M(z),\,5-\deg_M(w))\in\{0,1\}^2.\tag{1}
\]

| M 的 root degrees | 全部可能原省略身份 |
| --- | --- |
| (5,5) | 無；M=G |
| (4,5) | 恰一份 z-spoke 或單接點 unary-at-z |
| (5,4) | 恰一份 w-spoke 或單接點 unary-at-w |
| (4,4)，保留 C | z 側、w 側各恰一份單容量因子：spoke 或單接點 unary |
| (4,4)，省略 C | 恰只省略 C，且 C 的 incidence 向量必為 (1,1) |

這個表是窮盡式 (1) 的初等推論；容量至少二的 unary 不可省略。
省略 C 時不能再省略任何其他因子。兩側原因子身份保持，不按每列
重新挑選一份獨立正規化的分量。

Checker 另對恰一 mixed、每側 incidence 預算四的 **196 份整數配置／
7,442 個因子子集**直接窮盡核對表格。這只是容量身份代數，不是圖、
支援或來源實現枚舉；表格的任意大小 soundness 由 degree-4 飽和及
式 (1) 負責。

若 M 有 (5,4) 或 (4,5)，可在 **M 自己**套唯一 degree-5 的指定
相鄰列分離。不能因此宣稱 G 接受那兩列；G 可能用不同原省略身份
阻斷它們。若 M=G 且仍 (5,5)，該唯一-root 定理不適用。

## 3. (4,4) 且保留 mixed：原形比 contact 數更受限

此時 M 全 degree 四，自己就是 minimal q-obstruction，故其有效
內部是路徑、單 triangle 加不分叉路徑枝，或兩個互斥 triangles
由直接 bridge 相連；沿用 [全 degree-4 合成](c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論)。

任意不同的 z-contact、w-contact 之間的原 C 路徑，與原 zw 形成
長度至少四的環。任何額外不同 contact 同樣產生四環。因此必有

\[
P_C^z=P_C^w=\{x\},\qquad z,w,x\text{ 是同一原 triangle}.\tag{2}
\]

原 C 完整保留，不能把它換成新 singleton。全 degree-4 分類進一步給：

- 單 triangle 時，C 是從原 x 開始的一條路徑，允許 C={x}。
  若 C 非 singleton，該枝已占用一個接枝位置，兩 roots 合計至多
  再帶一份保留的 unary；C singleton 時至多各帶一枝。
- 雙 triangle 時，C 是 singleton x，或 x 經一條原 bridge 接到
  另一個原 triangle、恰四點；第二型 z,w 都沒有保留的 unary。

每個 root 在原 triangle 上至多另帶一條內部 bridge；所以保留的
unary 必單接點，每側至多一份。若其數為 uᵣ∈{0,1}，則 M 的原
spokes 數是 2−uᵣ≥1。

這些是原 C 的必要形狀，不是任意 mixed 原圖的一般正常形。
只在 M 保留 C 且兩 roots 自己 degree 四時成立。

## 4. 雙 spoke 省略的任意大小覆蓋

再假設式 (1) 省略的恰為原 zb、wc 兩條 spokes。沒有任何分量省略，
因此 G 就是這份原 M 加回這兩條具名 spokes。兩 roots 已在原 triangle
上，任何原路徑枝都不含 z,w；可使用已有單 triangle 原附件分類。

整圖共同搬運 q 至 q₄=01012，只進行一次 boundary／色框對齊。
單 run 枝的實際附件是 X^(2a+1),leaf；兩 runs 僅容許八份 contexts
的 X,Y^(2a),leaf，見 [原路徑枝報告](c5_triangle_path_reduction.md)。
兩枝時每枝僅一個 run。原 run 內每點的可用色集 S 至少兩色：
|S|=2 時只依正長度奇偶，|S|≥3 時任意正長度的兩側端點關係相同。
故縮成一點或兩點，保存對 triangle parent 顏色的完整可延拓條件。

此替換保留三個原 triangle 頂點的**聯合 relation**，即使刪去原 zw
而放寬其中一條 triangle 邊仍成立。各原枝只共用已固定的 boundary
及其一個 triangle parent；固定同一 triangle tuple 後逐枝選完整
witness，便保存原 M、M−zw 在 (z,w) 上的完整有序關係。
加回 zb、wc 是這兩個原座標上的字面色過濾，也保持等價。

固定必要域如下；原兩點都在 triangle 上，沒有使用未保留 markers
的 tail 化約偷推 root-pair 等價。

| 原 core 家族 | 必要正常形 |
| --- | ---: |
| 單 triangle、至少一枝、單 run | 18 |
| 單 triangle、原兩-run contexts | 8 |
| 無枝 triangle 的 T4 全收必要支援 | 36 |
| 雙 triangle、原直接 bridge | 64 |
| 合計 | 126 |

無枝 triangle 先重算全部 80 份 q₄-critical 支援，再按實際 T4
結果保留 36 份，不篩 disk。雙 triangle 先由實際原邊集重算全部
128 份保存 lifts 的 Σ，再取 64 份 q₄ 核心。十八份單 triangle 及
八份兩-run 輸入的原附件、apex rotations／minor contexts 沿用並
直接核對。Triangle 標號必要時由一次整圖同構搬運，全部原 triangle
邊都作 roots 位置，不為每份分量重新選色框。

其他 contacts 可落在被縮原區段；沒有宣稱它們都保留為目標 singleton
座標。長圖控制保存各自全部原分量、contacts、附件及完整聯合關係；
跨縮減只宣稱原 triangle／roots 的聯合 relation 相等。

## 5. 完整同框接回及結果

對每份正常形及每條原 triangle 邊 (z,w)，先完整染色 M−zw。
Kβ 是其完整有序 root-pair relation；另保留 roots 及所有原分量
contacts 的完整聯合 tuples，共鄰 x 只列一次。每個 tuple 都附該
圖全部內點的一份 coloring witness，空纖維亦保留。

加回兩條原 spokes，及原 zw 的精確接合為

\[
K_\beta(N)=\{(a,d)\in K_\beta:a\ne\beta(b),\ d\ne\beta(c)\},
\qquad
K_\beta(G)=\{(a,d)\in K_\beta(N):a\ne d\}.\tag{3}
\]

實作先在完整 root/contact tuples 過濾，再投影 roots；同一個 tuple
及字面色框貫穿查詢。所有 roots 位置、兩條各自不存在於 M 的原 spokes
全部展開，共 **570 份具名原 root 邊／6,068 次雙 spoke 接回**。
60,680 次十列查詢與完整原邊集回溯比較；四份 spoke 子集另有
242,720 次獨立完整回溯比較，保留每個原省略身份的 Σ。

全部接回均無 933／941 的任何 D₅ 像。T4 全收者的完整 Σ 為：

| Σ(G) | 數量 |
| --- | ---: |
| 942 | 70 |
| 956 | 36 |
| 958 | 306 |
| 1006 | 122 |
| 1012 | 70 |
| 1014 | 122 |
| 1020 | 306 |
| 1022 | 2,434 |

合計 3,466 份，其 N 都全收 Ω。這個放寬域容許非 disk 或非 Σ-minimal
圖；其中有其他三拒絕型，不能概括為所有雙 spoke 接回至多兩拒絕。
來源 exclusion 只需「必要域全無兩個目標」，不以來源實現判定作 oracle。

因此固定候選中，保留原 mixed 的 (4,4) core 之原省略因子至少一份
是單接點 unary；雙 spoke 子分支任意大小全部排除。

## 6. 證書、重播與停止點

[Checker](../scripts/c5_excess_two_mixed_core_spokes.py)／
[artifact](../artifacts/c5_excess_two_mixed_core_spokes/observations.json) 保存
原 core 邊、q₄-critical witnesses、全部原分量、contact 順序、實際
attachments／support、所有雙 spoke 接回及其十列完整聯合 tuples。
Witness indices 指向同一原 kernel 的完整 coloring；式 (3) 保證這份
witness 同時滿足所指名 N／G 的原邊，不把不同染色拼成一份見證。

對 26 份單 triangle 正常形另保留同附件 run 增長的原長圖及收縮
branch sets，兩 roots 的 branch sets 為 singleton。780 次長圖完整
色對比較、8,720 次具名接回逐列比較全相等；原長圖的全部 contacts
聯合 relation 各自保存，沒有要求它等於短圖的 contact relation。
證書另有一張實際圖／列的非空對角 K，兩側 marginals 相乘會誤造
異色對；原完整 K 接回 zw 卻為空，附全部原圖 coloring witnesses。

```bash
python3 scripts/c5_excess_two_mixed_core_spokes.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_spokes.py --check
python3 scripts/c5_excess_two_triangle_edge.py --check
python3 scripts/c5_excess_two_root_deletions.py --check
uv run --with networkx==3.5 python scripts/c5_triangle_path_reduction.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

實際重播及未重跑範圍見 [本輪紀錄](history/2026-10-03-excess-two-mixed-core-spokes.md)。
任意大小 degree-4 分類及 disk／minor 的外部與有限 topology 信任
範圍沿用前序報告；新身份表與傳遞是紙面證明，Python 證固定完整域。
`lake build` 不形式化本頁結論；沒有新文獻 oracle 或來源實現證書。

**停止點：** 相鄰、唯一 mixed、N 全收的 proper core 已有完整原身份表；
保留 mixed 的 (4,4) 雙 spoke 省略分支全排。下一窄入口是同樣保留
原 mixed、(4,4)，**一側省略原 spoke、另一側省略原單接點 unary V**，
含 root 交換型。先固定原共鄰 triangle 的 z,w,x，保留 V 任意大小、
全部附件及其非空完整 endpoint relation，分析 core 加原 spoke 再與
同一原 V 接合；不得把 V 當作可任選 boundary-spoke。

兩份原 unary 省略、省略唯一 mixed、(5,4)/(4,5) cores、整張 G 自己
為 (5,5) q-core，及多 mixed、no-mixed、非相鄰 roots／unary 側例外
仍保留。未排除全部 ε=2、未證 ε≥3、一般出口或 `K∞=K≤5`。
