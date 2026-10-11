# ε=2 四-spoke (3,1)：兩原 unary 的六跨度排除

**整理核對（2026-10-03）**：[七輪整理與發布紀錄](history/2026-10-03-excess-two-four-spoke-progress-publish.md)
確認後續四-spoke (3,1) 全 incidence 分拆已排除。原 byte-check 因
leaf-fibers 後續說明造成一份文件 hash 漂移而未通過；新
[唯讀 audit](../scripts/c5_excess_two_four_spoke_progress_audit.py) 重算全部
數學 payload 及非文件 inputs 相同，保留原 artifact 與嚴格 byte-check。

**後續（2026-10-03）**：[一原 binary unary 的 marked-leaf 化約](c5_excess_two_mixed_core_four_spoke_binary.md)
及原 star 篩選後的 32／64 份殘留，已由
[同列端點 hub 排除](c5_excess_two_mixed_core_four_spoke_hubs.md)全部覆蓋。
該 binary 子型及 root 交換全排；下文保留本輪六跨度證明及當時停止點。

2026-10-03，接手基準 `b63a096`。接續
[雙 root 提交紀錄](history/2026-10-03-excess-two-dual-root-progress-commit.md)
選定的四-spoke 子型與 [原 leaf 色纖維](c5_excess_two_mixed_core_leaf_fibers.md)。
目前停止點由 [Kempe 導覽](c5_kempe_guide.md)維護，實際驗證與貼用摘要見
[本輪紀錄](history/2026-10-03-excess-two-four-spoke-singles.md)。

**新結論：相鄰唯一 mixed 的四-spoke (3,1)、原 mixed incidence-(1,1)
加一-spoke 側兩份單接點 unary 子型及 root 交換全部排除。**
原三份分量的共同支援要求至少六段框邊，而同一 disk 只有五段。
這是任意大小紙面來源排除，加同源支援與完整 joint 的 Python 控制；
不需要新的來源圖枚舉。其他三份 (3,1) incidence 分拆、其他四-spoke
型與較少 spokes 仍保留；**共同下界仍是 ε≥2，ε≥3 未證，未新增
Lean theorem。**

## 1. 原 G、分量身份與精確 joint

沿用固定完整 Σ=933／941 或整圖 D₅ 像、每條非框邊刪除都嚴格擴大
Σ 的來源前提。G 有限簡單，B=(b₀,…,b₄) 為指定有序 induced-C₅
disk 外框，有效內部 H 連通。ε=2，恰兩個完整 degree-5 roots，
其餘有效內點完整 degree 四。原 roots 相鄰；三-spoke 側記 a，
一-spoke 側記 b，其唯一原 spoke 為 bb_s。

原 H−{a,b} 恰一份 mixed C，原 incidence 是 (1,1)，有序 contacts
為 (x,y)，owners 為 (a,b)；容許 x=y，仍為同一原頂點。另外恰有
兩份原 unary U、V，各以一條原邊 bu、bv 接 b。a 的三條原 spokes、
ab、ax 及 b 的原 spoke、ab、by、bu、bv 耗盡兩側完整 degree 五。
所有分量、原內邊、實際附件／supports、contacts、ownership、環序
及同一字面四色框保持。

對任一 proper boundary coloring β，用 U₄={0,1,2,3} 記色集。
原完整關係為 R_C(β;x,y)、S_U(β;u)、S_V(β;v)。給定省略
e=ab_j，令 S_a=N_B(a)，原 leaf 接合為

\[
R_{K,e}(\beta;a,y)=\{(A,Y):\exists(X,Y)\in R_C(\beta),\quad
A\notin\beta(S_a\setminus\{j\}),\ A\ne X\}.
\]

完整五點 joint 保留兩份原 unary 的獨立身份：

\[
\mathcal J_e(\beta;b,a,y,u,v)=\{(D,A,Y,T,W):
(A,Y)\in R_{K,e}(\beta),\ T\in S_U(\beta),\ W\in S_V(\beta),
D\ne\beta_s,A,Y,T,W\}. \tag{1}
\]

每份 tuple 都由同一原 C 的一份完整 tuple 及 U、V 的完整 coloring
witnesses 接合，不將 C 的 endpoint marginals 相乘。固定 (b,a)
後保留整個 (y,u,v) 纖維，含空纖維。接回原 spoke 恰為

\[
\mathcal J_G(\beta)=\{t\in\mathcal J_e(\beta):t_a\ne\beta_j\}. \tag{2}
\]

若 β_j 已出現在 a 的另一條保留 spoke，式 (2) 不移除任何 tuple。
下面的主證明直接使用原 G，不把接受的省略圖當成原圖延拓。

## 2. 原 Σ-critical 邊給 unary 的非空禁色見證

原 H−b 的三份連通分量恰為

\[
K=C\cup\{a\},\qquad U,\qquad V. \tag{3}
\]

K 的兩個原 b-contacts 是 (a,y)，a 在 K 中是 leaf，但在完整 G
仍為 degree 五；它保留全部三條原 boundary spokes。U、V 每點
完整 degree 四，各自仍是原 H−b 的一接點分量。

取 Σ-critical 原邊 bu。存在原拒絕、G−bu 新接受的同一列 β，
以及 G−bu 的整圖 coloring f。令 d=f(b)。定義

\[
F_U(\beta)=\bigcap_{T\in S_U(\beta)}\{T\}.
\]

S_U(β) 非空：原 contact u 未固定 b 時有 list slack，連通貪婪
引理可染整份 U。若存在原 U coloring 的 contact 色不等於 d，
只替換 f 在同一 U 內的 coloring 即能接回原 bu，其他原邊與 β
均合法，與原 G 拒絕 β 矛盾。因此

\[
d\in F_U(\beta),\qquad F_U(\beta)\ne\varnothing. \tag{4}
\]

同理，原 bv 的整圖 critical witness 給 V 的非空禁色見證。兩份
見證可以在不同列；下一節相加的是兩份**固定原支援的幾何跨度**，
沒有跨列相加容量，也沒有假設 G 是任何指定列的 minimal q-core。

## 3. 原外路徑排除 unary 短支援

令 P 是任一相鄰框點對。若實際 N_B(U)⊆P，a 的三個不同原框
鄰點保證存在具名 h∈N_B(a)∖P。原圖的簡單路徑

\[
L=b-a-b_h \tag{5}
\]

只用原 ab 與原 a-spoke；唯一內點 a 位於原 H−b 的 K，避開
U 與 b，終點在 B∖P。b 有其原唯一 spoke。

故 [短支援定理](c5_short_support_singleton.md#1-原圖完整接點-relation-與外部路徑)
以 r=b、carrier=原 U 直接適用，得到 F_U(β)=∅ 對每個 proper β
成立，與式 (4) 矛盾。定理只要求 carrier 中每點完整 degree 四；
沒有要求其他分量中的原 a 也是 degree 四。對 V 同理。

因此 U、V 的實際支援不可能包含於任何原框邊。空支援與單點支援
也包含於某份相鄰對，故一併排除。它們的最小 cyclic 支援跨度都
至少二。K 包含 a 的三個不同原框鄰點，任何涵蓋 K 支援的框弧
也至少跨兩段。記這三份原支援的最小 cyclic 跨度為 m_i，則

\[
m_K\ge2,\qquad m_U\ge2,\qquad m_V\ge2. \tag{6}
\]

## 4. 含原 degree-5 點的共同 lifts：六段不能放入五段

這裡單獨證明幾何步驟，不將
[原 unary 的共同 lifts](c5_independent_support_capacity.md#42-同一-root-的相容-lifts)
原封套到含 a 的 K。所需條件只有：三份原分量連通、彼此互斥、
各自碰 B，並有同一 root b 與它的原 spoke。

只為拓撲，在原 K、U、V 各取 spanning tree，收縮各樹的內邊，
刪除產生的 loops／重複邊。每份分量只留一條原 b-contact，並對
每個實際框支援點留一條附件；原 bb_s 與完整 B 保留。所得嵌入
星樹以 b 為中心、三份原分量的 branch sets 為葉。

星樹的小正則鄰域是 disk，各葉的外向附件位於其連續區段。沿
原 b-spoke 切開後，這三份葉區段與長度五的外框線之間的附件
互不交叉。故可在**同一嵌入**選擇 lifts T_K、T_U、T_V，並按
原順序排序，使

\[
\max T_1\le\min T_2,\qquad \max T_2\le\min T_3.
\]

共用框端點允許等號；b_s 的位置 0、5 仍是同一原點，沒有新增
顏色自由度。令 ℓ_i=max T_i−min T_i，則 ℓ_i≥m_i，且區段間
空隙非負，所以

\[
\boxed{6\le\ell_K+\ell_U+\ell_V\le5,} \tag{7}
\]

矛盾，完成選定子型及 root 交換的任意大小排除。上述收縮只承擔
原來源的拓撲反證；全部色關係仍在原 G 計算，不宣稱 minor 保持
完整 Σ。此主證明不需 933／941 的特定拒絕位置、T4 或單列
minimality；固定候選前提仍是本輪的適用範圍。

## 5. 獨立 marked-core 支援核對與完整圖控制

[Checker](../scripts/c5_excess_two_mixed_core_four_spoke_singles.py)／
[artifact](../artifacts/c5_excess_two_mixed_core_four_spoke_singles/observations.json)
另保留最初選定的同色 spoke 省略路線：

- 從既存 `(2,1,1)` 證書取 114 份具名支援及 42 份整圖反射，
  保存原 artifact index、分量順序、實際支援、禁色與共同 lifts。
- 包含 root 交換，933／941 有 20／60 份具名附件，共 200 個
  原省略／拒絕列查詢；保留原 leaf 的兩條附件、slack 禁色限制、
  全十列整圖搬運及 8／6 child masks 的必要相容性。
- 152／536 份必要 child records 接合為 96／192 份同源
  (S_C,S_U,S_V) 域；使用 S_K=S_C∪保留的原 a-spokes，且同一列
  的 K／U／V 禁色必一致。不是逐列獨立挑選分量或色框。
- 這 288 份域中兩份 unary 支援皆為原框邊，576 份原
  b–a–b_h 路徑前提逐邊核對；短支援定理全部排除。零殘留指必要
  域被紙面來源定理排除，不是 Python 證明 disk 實現。

主六跨度論證的固定控制核對全部 21 份跨度至少二的非空 actual
support 子集：五個原 b-spoke 位置，共 **46,305** 組有標號三份
支援，均無共同 lifts；另保存 (1,2,2) 正控制及 50 份具名原
三-spoke／相鄰支援對的外路徑選擇。有限域不代替 §4 的嵌入證明。

[完整圖 helper](../scripts/c5_excess_two_four_spoke_joint_controls.py)
保留十二張含 root 交換的原完整度數圖；C 為 singleton／edge／triangle，
U 為 singleton／edge，V 為 singleton。全部原邊、實際 attachments、
ownership、原 C 的完整 (x,y) tuples、兩 unary witnesses、K 的
(a,y) relation 與五點 joint 保存。**360** 次接合與獨立整圖回溯
相同；**5,760** 次 pinned (b,a) 的完整 (y,u,v) 纖維含空纖維均
相同，並核對 **72** 份同色 spoke 的字面 relation 等式。

原控制 0、row 0 的 C contacts 都是原頂點 7，完整 tuples 為
`{(0,0),(3,3)}`。指定 a=0、b=3 時完整 guarded fibre 為空，
兩 marginals 卻各自有可用色，不能相乘。另存同一控制 row 9
省略原 a–b₂ 後非空 joint `{(0,2,3,3,1)}`，接回原 spoke 全濾空。
這些控制不聲稱 disk、Σ-critical 或候選實現，也不反駁同色省略
情形；它們驗證式 (1)–(2) 的必要資訊。

## 6. 重播、信任界線與停止點

```bash
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_four_spoke_singles.py --check
uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_four_spoke_singles.py --check
PYTHONHASHSEED=17 python3 scripts/c5_short_support_singleton.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_leaf_fibers.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

信任層：原 critical-witness 接合、短支援來源定理、任意大小共同
lifts 的紙面證明；短支援沿用外部 degree-list／Gallai 及既有
連通外框 K₄／minor 證明。Python 核對上述固定域與完整 witnesses，
未使用四色定理 oracle，未重新枚舉原來源圖。沒有新增 Lean theorem，
`lake build` 不形式化本輪紙面 topology。

**停止點：完成選定四-spoke (3,1)、mixed-(1,1) 加兩份單接點
unary 的來源排除，含 root 交換。** 下一窄入口可取同一 (3,1)
的 mixed-(1,1) 加一份原 binary unary；刪同色 spoke 後為 t=1、
(2,2) core，須保留原 K 的 leaf 及 binary 的完整雙接點 joint。
該型與 mixed-(1,2) 加一 unary、mixed-(1,3) 無 unary 均尚未處理。
其他四-spoke／較少 spokes、原 unary 單省略、原 (5,5) q-core、
多 mixed／no-mixed／非相鄰雙 roots 仍保留。單 spoke 省略未整型
排除，共同 ε≥2 不變；ε≥3、一般出口、來源實現及 K∞=K≤5 未證。
