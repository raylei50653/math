---
docgraph:
  id: c5.single-spoke-two-two-external
  family:
    - c5
    - c5.single-spoke
  requires:
    - c5.single-spoke-two-two-minor
    - c5.single-spoke-two-two
---
# Single-spoke (2,2)：record 104 的外部路徑接合與相鄰支援對排除

後續（2026-09-28）：[singleton-source 首橋相容性](c5_single_spoke_first_bridge.md)
已證 record 87 的 p₂，套表共新增 16 個指定列延拓；來源排除仍 278 筆，保留
102 筆／51 型、100 筆雙列已證，僅 record 90／282 的 p₂ 未決。下文與舊
artifact 保留當輪語境；新層保留首橋共用 β，未放寬舊 pair 引理的 singleton 限制。

後續（2026-09-28）：[兩框弧 K5](c5_single_spoke_two_arc.md) 已證 record 17 的
p₁、p₂；新排除 6 筆來源、另證 20 個指定列延拓，現為累計排除 278 筆，
保留 102 筆／51 型、84 筆雙列已證、18 個查詢未決。以下正文與既有 artifact
保留當輪數字及停止點；新證據另存兩框弧層。

後續（2026-09-28）：[跨列 residual 相容性](c5_single_spoke_cross_row.md)
新增 16 個指定列延拓，來源仍為 108 筆／54 型，現為 74 筆雙列已證、
50 個查詢未決。以下前輪數字與 artifact 保留當輪語境。

後續（2026-09-28）：[frame-arc K5](c5_single_spoke_frame_arc.md) 以三段具名框弧
放寬相鄰限制，另排除 36 筆來源、另證 18 個指定列（含 record 15 的 p₂）。
現剩 108 筆／54 型，其中 58 筆雙列已證、66 個查詢未決。下文與本頁 artifact
保留本輪 144 筆與 record 15 待辦的歷史語境；新結果另存後續證書層。

2026-09-28。接續 [路徑塊支援守恆](c5_single_spoke_two_two_minor.md)，
研究優先序見 [HANDOFF](HANDOFF.md)。

**record 104 已由原圖 K5 minor 排除。** C1 的相鄰兩個路徑塊都接
b0、b4；另一分量 C0 的實際 z–b1 路徑，把剩餘環段接到補弧 b1–b2–b3。
這給五個互不相交的連通 branch sets，全部十條鄰接均有原邊 witness。
相同引理套用三個 spoke 代表，再排除 **210 筆／105 型**，含交換分量
名字後的 record 148。連同先前 26 筆，累計排除 236 筆，剩 **144 筆／72 型**。

剩餘表中 54 筆兩個指定 p 已證延拓；原 104 筆條件式雙列延拓中，另
50 筆現在排除來源，既有延拓結論不變。這次沒有新增 p 延拓證明。
證據為任意大小紙面 minor、沿用外部 degree-list 結構與 Python 有限
控制；未新增 Lean theorem，未證其餘來源可實現或完整 (2,2) 分離。

## 1. 前提與逐塊具名接線

沿用 [(2,2) 必要分類](c5_single_spoke_two_two.md) 的完整前提：G 有限、
簡單且 B=(b0,…,b4) 是 induced-C5 disk 外框；有效 H 連通，G 是
edge-minimal q=01012 obstruction；唯一完整 degree-5 點 z 只有 spoke
zb_s，其餘內點完整 degree=4；H−z 恰有二接點分量 C0、C1。
每份分量的原接點 (u_k,v_k)、完整 R_k(q)、全部 boundary 接線與
接點環序均保留。S_k 是實際支援，不能用允許接線的超集代替。
本頁來源排除不需要 T4；只在套用原保留表時使用其 T4 篩選。

選雙禁色分量 C=C_k，F_C(q)=F={c,d}。既有任意大小化約給原 bridge
路徑 P=(x0=u_k,…,xℓ=v_k)，ℓ≥1 為奇數。刪掉 P 的所有邊，含 x_j
的連通分量記 W_j；它包含該 root 的所有旁支。各 W_j 互不相交，且
只含一個路徑點。T_j 是 W_j 全部頂點的實際 boundary 支援。

前報告 §2 已證每個 W_j 都必見下列兩色：

\[
E(F)=\begin{cases}F,&3\notin F,\\ U\setminus F,&3\in F.\end{cases}
\qquad E(F)\subseteq q(T_j),\quad U=\{0,1,2,3\}.
\]

若 E(F) 的每色 c 在 S_k 中各只有一個具名供應點 b_i，則每個 T_j
都含該 i。因 T_j⊆S_k，這是實際原接線，不是可任選的代表。設這兩點
為 b_a、b_b；以下只處理它們在 C5 上**相鄰**的情況。
例如 record 104 的 C1 有 S1={0,4}、F1={1,3}，故 E(F1)={0,2}，
兩色分別只由 b0、b4 供應，每個 W_j 都實際接到兩者。

若同色在 S_k 有兩個供應點，不能逕選其一當每塊的接線。例如
S={0,2,3,4}、F={2,3} 只迫使每塊見 b3 及 b0、b2 至少一者。
新 checker 保存所有局部支援子集，特別核對這個未被涵蓋的情況。

## 2. 補弧外部路徑與一般 K5 抽取

令 D=B\{b_a,b_b}。因 b_a、b_b 相鄰，D 是含其餘三點的連通框弧，
而 b_a、b_b 各與 D 有一條原框邊。假設有一條原圖路徑 L，從 z
到某 b_h∈D，內部避開 B、C 及 z。以下任一條件足以提供這份路徑：

1. s∉{a,b}：取原 spoke L=z–b_s。
2. 另一原分量 C_(1−k) 的實際支援含 h∉{a,b}：選其原接點 r=u_(1−k)，
   及實際邊 t–b_h，其中 t∈C_(1−k)。由原分量連通，取其中的 simple
   r–t 路徑，前接原邊 zr、後接原邊 t–b_h。r=t 亦可。L 的內點全在
   另一分量，故避開 C；路徑只在末端碰 B。

不需要兩條外部路徑互不相交，也不使用另一分量的禁色值。選取的是
**同一來源圖**的實際路徑；其內部可經過該分量另一接點，沒有關係投影
或合併 C0、C1 的步驟。

任取 P 的一條原邊 xy=x_(i−1)x_i。P 加 zu_k、zv_k 是 simple cycle J，
且 J−{x,y} 是含 z 的非空連通路徑；ℓ=1 時就是 {z}。定義

\[
A=W_{i-1},\quad A'=W_i,\quad
Z=(V(J)\setminus\{x,y\})\cup V(L)\cup D,\quad
X=\{b_a\},\quad Y=\{b_b\}.
\]

**連通。** A、A' 由定義連通；J−{x,y} 與 L 在 z 相接，L 與 D 在
b_h 相接，因此 Z 連通。X、Y 是單點。
**不交。** 原 bridges 使 A、A' 互不相交，且不含 J 的其他路徑點；
它們都是 C 的內點。L 的內點在 C 外，D、X、Y 是互不相交的框點集，
故五個 branch sets 兩兩不交。W_j 的額外 boundary 邊不把框點納入 W_j。

十條鄰接如下；每列只要求存在一條原邊，不要求各條 tether 的內路互不相交。

| branch-set pair | 原邊 witness |
| --- | --- |
| A–A' | xy |
| A–Z、A'–Z | J 上 x、y 各自另一條 cycle 邊 |
| A–X、A'–X | 各 W 的實際 b_a 接線 |
| A–Y、A'–Y | 各 W 的實際 b_b 接線 |
| Z–X、Z–Y | D 兩端與 b_a、b_b 的框邊 |
| X–Y | 原框邊 b_a b_b |

故原 G 含 K5 minor，與平面性矛盾。任意路徑長度、旁支大小、接線
位置與 L 長度均由這份具名集合構造涵蓋；minor 本身不需要奇偶性，
來源化約才給 ℓ 為奇數。這是來源不存在的證明，不是保留完整 Σ 的壓縮。

## 3. record 104 的具體接合

原記錄是 s=0、(S0,S1)=(01234,04)、(F0,F1)=({1,2},{1,3})。
選 C=C1；每個 W_j 都接 b0、b4。C0 實際碰 b1，故從原接點 u0 經
C0 到某個 b1 的鄰點，再接 b1，得到 L=z–u0–…–b1。
L 內點全在 C0，和 C1 的兩個 W 及其餘路徑點沒有共同頂點。

取任一原 bridge xy，五組就是

\[
W_{i-1},\quad W_i,\quad
(V(J)\setminus\{x,y\})\cup V(L)\cup\{b1,b2,b3\},\quad
\{b0\},\quad\{b4\}.
\]

Z–X 用 b1b0，Z–Y 用 b3b4，X–Y 用 b0b4；其餘七條鄰接由原
bridge、cycle 邊及四條 W 到 b0、b4 的實際接線提供。因此 record 104
排除，record 148 只交換兩分量名字。原 spoke zb0 不用作 Z 的接合邊，
也不將 b0 加入 Z；這正是上一輪尚待補齊的分離條件。

## 4. 全表套用、反射與計數

[新 checker](../scripts/c5_single_spoke_two_two_external.py) 只讀原
[(2,2) 表](../artifacts/c5_single_spoke_two_two/observations.json) 及
[先前排除層](../artifacts/c5_single_spoke_two_two_minor/observations.json)，
核對輸入 SHA256、26 筆原記錄與 354 個剩餘 IDs，再對每個分量檢查：
雙禁色、兩種必要色各有唯一具名供應點、兩點相鄰、存在 §2 的接合路徑。
每個 witness 保存原有序接點、外部分量／接點、具名落點及補弧；所有
來源記錄連同完整 relation schema IDs、slit lifts、contact words、targets
與反射資料原樣保存。沒有把未知來源路徑捏造成已知頂點清單。

| s | 本輪排除 | 剩餘 |
| --- | ---: | ---: |
| 0 | 48 | 58 |
| 1 | 86 | 62 |
| 4 | 76 | 24 |
| 合計 | 210 | 144 |

210 筆中，106 筆需要另一分量的外部路徑；另 104 筆也能直接使用
落在補弧的 spoke。每筆可能有多份 witness，計數只算一次。
交換 C0、C1 名字保持判準，剩餘 144 筆恰為 72 型。反射沿用原來
完整關係的 ρ=(3,2,1,0,4)、π=(0 1) 搬運；checker 額外核對強迫框點、
外部落點、spoke 與支援都搬到同一份反射來源，未另加反射側計數。

| p₁ / p₂ | A/A | A/? | ?/A | ?/? | 含 R |
| --- | ---: | ---: | ---: | ---: | ---: |
| 本輪排除 | 50 | 28 | 18 | 96 | 18 |
| 排除後保留 | 54 | 30 | 42 | 18 | 0 |

原 104 筆 A/A 的條件式延拓定理保留；其中 50 筆的前提現知無平面來源，
剩餘表的 A/A 因而是 54，不能誤報成延拓定理退步或新增 210 筆延拓。
完整排除 IDs 與每筆 witness 見 [支援表](../artifacts/c5_single_spoke_two_two_external/support_table.md)，
其全部資料與剩餘 IDs 見 [JSON](../artifacts/c5_single_spoke_two_two_external/observations.json)。

## 5. 證書、重播與信任界線

新證書保存 186 個「六種 F × 31 非空 S」局部支援控制：逐一遍歷 T⊆S，
檢查必要色條件與唯一具名供應點的結論；非唯一供應點不會被當作固定接線。
496 份 K5 控制分為原路徑長 1、3、5、7 的全部選邊與四種 tether 形狀
組合 256 份；五個相鄰框點對、五個 spoke、三個補弧落點及 1、2、5
個外部內點的 225 份；直接 spoke 接合的 15 份。
每份保存原邊、路徑、五個 branch sets、十條鄰接並核對連通與不交。
缺外部首邊、末邊、tether、原 bridge、重疊 branch sets，以及無補弧
落點六個負控制皆必被拒絕。

這些 skeletons 不是完整 degree-4／list 來源或小圖 cover。任意大小
成立依賴繼承的 palette／bridge 紙面證明及 §2 的原圖集合構造。
沒有新增外部定理，也沒有新增 Lean theorem；`lake build` 不把這份
拓撲證明變成 Lean 形式化。原表與先前 artifact 都保持原內容。

```bash
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

新 checker 無 `--check` 時產生新 JSON 及支援表；有參數時重算逐 byte
比對。實際驗證與未重跑範圍見 [研究紀錄](history/2026-09-28-two-two-external.md)。
兩輪成果的整合重播與發布範圍見 [發布紀錄](history/2026-09-28-two-two-publication.md)。

下一個窄入口為 record 15：s=0、支援 (01,0234)、禁色 ({1},{2,3})，
p₁ 已證，p₂ 未決。雙禁色 C1 每塊都見 b3，且見 b0、b2 至少一者；
兩個同色供應點不能各自任選。應保留各塊實際支援、原 bridge 次序與
C0 的 z–b1 外部路徑，研究這份逐塊分配的任意大小限制。
其餘 (2,2) 可實現性／分離、(3,1)/(4)、t=0、高 degree／多 degree-5、
一般核心存在性、單側／共同出口及 K∞=K≤5 仍未證。
