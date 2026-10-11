---
docgraph:
  id: c5.single-spoke-frame-arc
  family:
    - c5
    - c5.single-spoke
  requires:
    - c5.single-spoke-two-two-external
    - c5.single-spoke-two-two-minor
    - c5.single-spoke-two-two
    - c5.single-spoke-branch-palettes
---
# Single-spoke (2,2)：frame-arc K5 與 record 15 的 p₂ 延拓

後續（2026-09-28）：[singleton-source 首橋相容性](c5_single_spoke_first_bridge.md)
已證 record 87 的 p₂，套表共新增 16 個指定列延拓；來源排除仍 278 筆，保留
102 筆／51 型、100 筆雙列已證，僅 record 90／282 的 p₂ 未決。下文與舊
artifact 保留當輪語境；新層保留首橋共用 β，未放寬舊 pair 引理的 singleton 限制。

後續（2026-09-28）：[兩框弧 K5](c5_single_spoke_two_arc.md) 已證 record 17 的
p₁、p₂；新排除 6 筆來源、另證 20 個指定列延拓，現為累計排除 278 筆，
保留 102 筆／51 型、84 筆雙列已證、18 個查詢未決。以下正文與既有 artifact
保留當輪數字及停止點；新證據另存兩框弧層。

後續（2026-09-28）：[跨列 residual 相容性](c5_single_spoke_cross_row.md) 已證
record 16 的 p₁ 並新增 16 個指定列延拓；來源仍為 108 筆／54 型，現為 74 筆
雙列已證、34 筆含未決項、50 個查詢未決。下文與本頁 artifact 保留當輪數字。

2026-09-28，檢視基準 `9b13ef8`。本輪審核使用者提供的非相鄰框弧推導，
並從 repo 既有結構重新核對 target-row 前提。研究優先序見 [HANDOFF](HANDOFF.md)。
訊息所連 ZIP 在本工作環境不存在；本頁與 checker 是依訊息重建，沒有重播附件，
也不把附件所報 6,000／1／6 個控制算成本輪驗證。

**record 15 的 p₂=01212 延拓成立，因此兩個指定 p 都已證。**
關鍵是將相鄰支援對的兩個單點／補弧，改成三段有具名落點的連通框弧。
反設 p₂ 拒絕後，在同一來源圖的 p₂ lists 上重新取得雙禁色 palettes，
每個路徑塊都接 b0、b3；C0 的 z–b1 原路徑完成 K5 minor。
這是條件式延拓，沒有排除 record 15 的來源或求出完整 boundary relation。

同一引理套用上一輪 144 筆表項，**另排除 36 筆來源、另證 18 個指定列查詢**。
累計來源排除 272 筆；剩 **108 筆／54 型**，A/A、A/?、?/A、?/? 為
**58、12、22、16**，即 50 筆含未決項、66 個單列查詢。
任意大小論證為紙面證明，依賴既有外部 degree-list 定理；Python 僅核對有限
支援代數、拓撲 skeletons 與套表。**本輪沒有新增 Lean theorem。**

## 1. 來源前提與任意列的拒絕證書

完整沿用 [(2,2) 必要分類](c5_single_spoke_two_two.md) §1–3：G 有限簡單，
B=(b0,…,b4) 為 induced-C5 disk 外框，有效 H 連通；G 為 edge-minimal
q=01012 obstruction；唯一完整 degree-5 點 z 僅有 spoke zb_s，其餘內點
完整 degree=4；H−z 的 C0、C1 各有兩個不同的原接點 (u_k,v_k)。
S_k 為全部實際 boundary 附件，R_k(r) 保留同一完整 coloring 的有序 tuples。
來源接受 T4 只在套原保留表時使用；以下 record 15 的證明不需要 T4。

對任意 proper row r，先忽略 z 的顏色。C_k 的 boundary lists 在各點至少
有 deg_C(v) 色，在原接點至少有 deg_C(v)+1 色。C_k 連通，嚴格多色貪婪
引理給 coloring，故 **R_k(r) 非空**，其共同禁色交集 F_k(r) 大小至多二。
沿用 [R10 完整關係接合](c5_degree5_interfaces.md)：

\[
F_k(r)=\bigcap_{t\in R_k(r)}\operatorname{set}(t),\qquad
Z_G(r)=(U\setminus\{r_s\})\setminus(F_0(r)\cup F_1(r)).
\]

若 a∈F_k(r)，把 a 從兩個接點的 lists 去掉，得到同一 C_k 上不可著色的
degree lists M_(r,a)。[Dvořák 的 Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
分別給逐點緊性與 blockwise-uniform palettes 的存在；其 palettes 在每個
頂點兩兩不交，聯集等於該點 list。C_k 的 K4-free 結構沿用既有來源化約，
所以 blocks 只有 bridges／odd cycles。這裡**不要求 G 是 minimal r-obstruction**。
本輪已讀取並核對此外部定理；它不是本輪 Python 或 Lean 證書的一部分。

若 F_k(r)={a,d}，比較 (r,z=a)、(r,z=d) 兩份既存 palettes。
原分類 §3 的任意列版本給唯一的原 bridge 路徑 P=(x0=u_k,…,xℓ=v_k)，
ℓ≥1 為奇數。旁支不含其他 z 接點；odd-cycle 上第三個頂點使 palette
無法承擔沿 u–v 傳播的非零差，故路徑全是原 bridges。
這個化約從 r 的拒絕重新取得，沒有將 q 證書更名成 r 證書。

## 2. 任意列的逐塊 residual 穩定子

刪 P 的全部邊，含 x_j 的連通分量為 W_j；它們兩兩不交，各只含一個
路徑點，且含該 root 的全部旁支。T_j⊆S_k 是整塊的實際支援，包含 root
自己的接線。令 D_j=r(N_B(x_j))，Q_j 為 root 上所有路徑外 palettes 的聯集。

兩份拒絕證書在每個旁支的非 root 頂點有相同 lists：boundary row 同是 r，
那些頂點沒有 z 邊，也沒有另一原接點。[Rooted palette 唯一性](c5_single_spoke_branch_palettes.md#2-rooted-palette-唯一性與固定色守恆)
因此給兩份相同的 Q_j。其證明從葉 block 向 root 歸納：任取非 root 頂點，
其 list 扣去已決定的後代 palettes 就是該 block palette。存在性保證不同
選點相容；唯一性本身不創造拒絕證書，也不需要 root 的 list。

路徑內點的 residual 為 {a,d}。端點則令 E=U\(D_j∪Q_j)，兩份等式為
E\{a}={d}、E\{d}={a}，同樣迫使 E={a,d}。故所有 j 皆有

\[
D_j\cap Q_j=\varnothing,\qquad D_j\cup Q_j=U\setminus\{a,d\}.
\]

若 π 逐色固定 r(T_j)，則 π 固定全部非 root lists，也固定 D_j。
將**已存在的旁支 palettes** 用 π 搬運，所得證書的非 root lists 相同，
唯一性給 πQ_j=Q_j。搬運後 root 的完整 list 不必不變；唯一性不使用它。
因此 π{a,d}={a,d}，即 residual 必受局部實際支援的逐色穩定子保持。

對 q、p₁、p₂，boundary 都不使用色 3。若 3∉F，則 F 每色必出現於 r(T_j)，
否則交換該色與 3 矛盾；若 3∈F，則 U\F 每色必出現。反向亦成立，故

\[
E(F)\subseteq r(T_j),\qquad
E(F)=\begin{cases}F&3\notin F,\\U\setminus F&3\in F.\end{cases}
\]

如果這兩種必要色在 S_k 各只有一個供應框點 b_a、b_b，則每個 W_j 都有
到這兩點的**原邊**。非唯一供應時只保留選言，不能任選一個代表。
checker 直接遍歷全部 24 色置換及 T⊆S 計算強迫支援，沒有相鄰性篩選。

## 3. 三段框弧與任意兩塊的 K5 引理

本節單純是圖論構造，不需要 lists、parity 或完整 boundary relation。
設 P=(x0,…,xℓ) 的原 bridges 與兩條原邊 zx0、zxℓ 組成 simple cycle J；
W_j 如前節。取 **任意兩個不同的** W_i、W_j（i<j），兩者各實際接到
不同框點 b_a、b_b。另有原圖 simple path L，從 z 到第三個框點 b_h，
a、b、h 互異，且 L 內點避開 B、C、z。

沿框的循環次序，在三個標記點各開始一段，取到下一個標記點前為止。
得到 B 的三個非空、不交、連通分割 X、Y、D，分別含 b_a、b_b、b_h。
三個切口都是原框邊，故 X–Y、Y–D、D–X 各有鄰接。亦可使用任何具有
這些性質的具名三弧分割；**不能沿用可能不連通的 B\{b_a,b_b}**。

定義五個 branch sets：

\[
\begin{aligned}
A&=\bigcup_{t=i}^{j-1}W_t,& A'&=W_j,\\
Z&=\bigl(V(J)\setminus\{x_i,\ldots,x_j\}\bigr)\cup V(L)\cup D.
\end{aligned}
\]

A 沿原 bridges 連通；A' 連通；J 去掉這一連續段後的其餘部分經 z 連通，
與 L 在 z、與 D 在 b_h 相接，所以 Z 連通。五組互不相交：W_t 只含自己的
路徑點，L 的內部避開 C，框弧互不相交。A、A' 的額外 boundary 邊不將
boundary 頂點納入 W_t，也不破壞集合不交。

| branch-set pair | 原邊 witness |
| --- | --- |
| A–A' | x_(j−1)x_j |
| A–Z | x_i 在 J 上向前一點的邊；i=0 時為 x0z |
| A'–Z | x_j 在 J 上向後一點的邊；j=ℓ 時為 xℓz |
| A–X、A–Y | W_i 到 b_a、b_b 的實際接線 |
| A'–X、A'–Y | W_j 到 b_a、b_b 的實際接線 |
| X–Y、Y–Z、Z–X | 三段框弧的三個原框切口 |

十條鄰接全部存在，故 G 有 K5 minor。i、j 不相鄰時，把中間塊納入 A
正是保住 A–A' 原邊及 Z 連通性的步驟；旁支可任意大，tethers 可在同一
W 內共用頂點。這是原圖非平面 witness，容許框點合入同一 branch set，
**不宣稱這份 minor 保存完整 Σ 或 boundary 標號的壓縮語意**。

L 的來源與 [外部路徑引理](c5_single_spoke_two_two_external.md) 相同：
若 s∉{a,b}，用 spoke；否則另一原分量實際碰某 h∉{a,b}，从它的原接點
走連通路徑到 b_h 的內鄰點即可。內部可經該分量另一接點；不需要額外的
兩路不交條件，也沒有合併兩分量的 coloring relations。

## 4. record 15 的 p₂ 反證與具名集合

原記錄 s=0，S0={0,1}、S1={0,2,3,4}，F0(q)={1}、F1(q)={2,3}。
p₁ 延拓沿用原表；反設 p₂=01212 拒絕。p₂ 與 q 在 S0 逐點相同，故同圖
完整 R0 不變，F0(p₂)={1}。z 的可用色仍為 {1,2,3}，接合式迫使
{2,3}⊆F1(p₂)；由 §1 的非空 R1 及二接點容量，F1(p₂)={2,3}。

對同一 C1 的 (p₂,z=2)、(p₂,z=3) 套用 §1–2，所有 W_j 必見色 0、1。
在 **p₂ 的實際 S1** 中，色 0 唯一由 b0、色 1 唯一由 b3 供應，故
每塊實際接 b0、b3。C0 連通且實際接 b1，提供避開 C1 的原 z–b1 路徑 L。

任取原 bridge xy，取 §3 的相鄰兩塊特例與框弧

\[
A=W_x,\quad A'=W_y,\quad
Z=(V(J)\setminus\{x,y\})\cup V(L)\cup\{b1,b2\},\quad
X=\{b0,b4\},\quad Y=\{b3\}.
\]

X 由 b0b4 連通。X–Y 用 b4b3、X–Z 用 b0b1、Y–Z 用 b3b2；
其餘七條原邊如 §3。故 G 有 K5 minor，與來源平面性矛盾，p₂ 必延拓。
這並未指定所有來源都可使用同一 z 色，也沒有求出 F1(p₂) 的精確值。

附帶地，在原 q 下，每塊必接 b3 及 b0、b2 至少一者。若 P 至少有三塊，
選各塊一個實際供應點，鴿籠原理给兩塊共同接 b0 或共同接 b2；再配 b3
與同一條 z–b1 路徑，由 §3 矛盾。故 record 15 的原 bridge 路徑只有一邊。
兩端的旁支仍可任意大；這**不是兩內點正常形**，p₂ 證明亦不依賴此附帶推論。

## 5. 全表套用與分開計數

[Checker](../scripts/c5_single_spoke_frame_arc.py) 只讀原必要表及上一輪
外部路徑 artifact，保存輸入 SHA256。先在 q 下套 §2–3 排除來源；再對
未排除者的每個未知 target，重算原完整 forbidden-set 候選族的接合覆蓋。
**只有所有拒絕候選各有 minor witness，才記該 target 接受**；沒有把
逐接點邊際或候選聯集替換完整關係，也沒有把消掉部分拒絕候選算成延拓。

| s | 新來源排除 | 剩餘來源候選 |
| --- | ---: | ---: |
| 0 | 10 | 48 |
| 1 | 14 | 48 |
| 4 | 12 | 12 |
| 合計 | 36 | 108 |

| 階段 | A/A | A/? | ?/A | ?/? |
| --- | ---: | ---: | ---: | ---: |
| 上一輪 144 筆 | 54 | 30 | 42 | 18 |
| 本輪來源排除的 36 筆 | 14 | 8 | 12 | 2 |
| 來源排除後、延拓更新前 | 40 | 22 | 30 | 16 |
| 18 個指定列延拓後 | 58 | 12 | 22 | 16 |

18 個新增查詢為 p₁ 八個、p₂ 十個，各使一筆保留來源成為 A/A。
原 104 筆 A/A 中 64 筆來源現已排除，40 筆仍保留，加上本輪 18 筆才得到 58。
所有數字含交換 C0、C1 的有標號記錄；108 筆恰為 54 個交換型。
反射沿原 ρ=(3,2,1,0,4)、π=(0 1) 搬運**字面 target、整份 F 候選、具名
框弧、支援及落點**，另核對交換分量的結論一致，不另加反射側計數。

完整原記錄（有序接點、relation schema IDs、slit lifts、contact words、
原 targets、反射）原樣保存在 [JSON](../artifacts/c5_single_spoke_frame_arc/observations.json)。
來源 witness 保存五組集合的符號構造、X/Y/Z 的具名框弧、路徑分量、外部分量及原接點、落點；
未知大小的來源路徑仍用存在性構造表示，沒有偽造實際頂點清單。
查詢狀態與 IDs 見 [套用表](../artifacts/c5_single_spoke_frame_arc/support_table.md)。

## 6. 有限證書、重播與信任界線

- 48 個端點／內點 residual 聯集控制，沿用舊 checker 並本輪重播。
- 576 個局部支援控制：三列 × 六種雙禁色 × 32 個支援，核對全部 24 色置換。
  record 15 在 q 下的必接交集是 {b3}，在 p₂ 下重算為 {b0,b3}。
- 4,980 個一般 K5 skeleton 控制：60 個有序框點三元組 × 長度 1–5 的
  全部 35 個兩塊位置，共 2,100；再以非相鄰塊核對 60 × 16 種 tether 形狀
  × 3 種外部內點數，共 2,880。包含偶數長度是因 minor 引理本身不需 parity。
- 一個 record 15 具名控制，使用 §4 的確切框弧。每份控制保存原邊、五組集合、
  外部路徑、tethers 與十條鄰接；逐份核對連通、不交及鄰接。
- 11 個負控制：缺外部首／末邊、缺 tether、缺 bridge、框弧斷裂、缺框側鄰接、
  集合重疊、舊補弧不連通、落點與支援點重合、未併入中間路徑、無外部落點。

```bash
python3 scripts/c5_single_spoke_frame_arc.py --check
python3 scripts/c5_single_spoke_two_two_external.py --check
python3 scripts/c5_single_spoke_two_two_minor.py --check
python3 scripts/c5_single_spoke_two_two.py --check
python3 scripts/c5_single_spoke_bridge_path.py --check
python3 scripts/c5_single_spoke_branch_palettes.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 checker 無 `--check` 時只生成本輪 artifact 與套用表；有參數時重算逐 byte
比對。JSON 的每個一般 skeleton 以單行儲存，完整記錄仍在同一標準 JSON。
當輪實際檢查與未重跑範圍見 [研究紀錄](history/2026-09-28-frame-arc.md)。

有限 skeleton 不是 degree/list 來源圖、可實現性證書或任意大小 cover。
任意大小由 §1–4 的來源拒絕 → palettes、block-tree 歸納及具名集合證明承擔；
不以 conditional palette theorem 隱藏來源到證書的外部依賴。
`lake build` 不使新 palette／minor 論證成為 Lean 證明。

目前尚有 66 個 (2,2) 單列查詢；下一個具名入口見 HANDOFF。
其餘 (3,1)/(4)、t=0、更高 degree、多 degree-5、一般核心存在／分離、共同出口
及 K∞=K≤5 仍各有缺口。後續 Lean 可抽出 rooted-palette 唯一性與 frame-arc
branch-set 引理，仍須保留從實際來源取得 palette 證書的存在性依賴。
