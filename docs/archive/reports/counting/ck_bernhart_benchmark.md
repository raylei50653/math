# C₈ Bernhart 靶標與標準計數錐對照

2026-10-29，基線 `e1a90fe`；接續 [D 與鎖定比較](ck_d_lock_comparison.md)及
[計數錐驗證](../four-color/four_color_counts_surgery_verification.md)。本輪由使用者授權重新選擇
非 D 可約的正向基準，不改寫原 `LOCK-NO-GAIN` 的單 split 停止範圍。

## 先登記的驗證問題

1. 將 C₈ 四內點 diamond 的原頂點、原邊及完整有序框寫成資料，分別核對
   「對角線連兩六度點」與「對角線連兩五度點」；不以 degree multiset 判圖身份。
2. 以原邊窮舉保存全部 274 份固定框 fibre（含空列），與約束引擎逐列核對接受性，
   重播完整 noncrossing 布林 D 固定點。
3. 以 Dvořák–Lidický 的共同 signed-signature 權重建立標準 B₈ 可行性問題，
   強制接受列為零、總質量為一；若 LP 可行，轉成可用整數獨立核對的證書。
4. 核對 Bernhart 1948 原文所證構形與證明層次。共同切口條件若尚無一般正確性證明，
   不把它直接加成 LP 刪列規則，不宣稱新可約性。

此段在實驗前建立；以下為已完成的驗證。

## 1. 必須先更正 diamond 的身份

兩個內部三角形共邊的四點 diamond，有兩種不同的 degree placement，不能只看
內部度數的 multiset `{5,5,6,6}`。Bernhart 的原文證的是**相鄰兩六度點、兩五度點為 guards**；
primal 中共對角線為 **6–6**，不是 5–5。
[Bernhart, *Another Reducible Edge Configuration*, 1948, pp. 144–146](https://www.researchgate.net/publication/239412990_Another_reducible_edge_configuration)。

固定外環 `r₀…r₇`，內點 `a=8,b=9,c=10,d=11`，共同內邊為
`ab,bc,cd,da,ac`。原環邊完整保留；下表列出全部內外附件。

| 具名圖 | a 的框鄰點 | b 的框鄰點 | c 的框鄰點 | d 的框鄰點 | 內點度數 (a,b,c,d) |
| --- | --- | --- | --- | --- | --- |
| Bernhart，6–6 對角線 | 0,1,2 | 2,3,4 | 4,5,6 | 6,7,0 | 6,5,6,5 |
| 另一圖，5–5 對角線 | 0,1 | 1,2,3,4 | 4,5 | 5,6,7,0 | 5,6,5,6 |

兩圖都有 12 點、25 原邊、14 有界三角面及指定簡單外框 C₈。
程式保存整數座標、全部面及附件，沿用既有精確整數幾何 checker，逐邊核對面 incidence、
方向、無交叉與 Euler 圓盤式。這是具名自由補圖的幾何證書，不是未知外側的來源實現。

## 2. 完整 fibre、D 與標準 B₈ 的實算分水嶺

`U₈` 僅取同一 `S₄` 作用的色名商，保留全部環位置及方向，恰 274 列。
每列固定字面色，窮舉全部 `4⁴=256` 份內部指派；報告保存**每份**合法內部四元組及全部空列。
獨立的約束引擎逐列核對有／無延伸，沒有 `limit`。D 使用
[既有完整 noncrossing 分割與同步固定點](ck_d_lock_comparison.md#布林-d-的完整分割與固定點)，
不選取單一交換見證取代完整 options。

| 圖 | 接受／初拒 | 每輪 D 剩餘數 | 標準 B₈ 最大可行支援 | B₈ 額外必零列 |
| --- | --- | --- | --- | --- |
| Bernhart，6–6 對角線 | 81／193 | 178→170→164→157→154 | 76 | 78 |
| 另一圖，5–5 對角線 | 81／193 | 180→162→160 | 130 | 30 |

因此「81 接受、三輪後 160」數字確實可重現，但它對應第二張圖，不能作 Bernhart 古典可約性的正控制。
標準 B₈ 在兩圖都比布林 D 刪更多列，仍各留下非零計數向量；沒有新增可約性。

### 共同權重 LP 及精確證書

依 [Dvořák–Lidický, *Coloring count cones of planar graphs*, §1.2–2、Theorem 5](https://arxiv.org/pdf/1907.04066)，
列舉 1,641 個合法八端口三邊色 words `w`、1,961 個 partial noncrossing signed signatures `S`。
以 `wᵢ=bᵢ XOR bᵢ₊₁` 與積分對回同一有序環；共有 4,923 份 `(w,{i,j})` 方程：

\[
 n_{[b(w)]}=\sum_{S\sim(w,ij)}y_S,\qquad n_c,y_S\ge0.
\]

三個 splits 和全部 words 共用**同一份** `y_S`。先將 D 已刪列的 `n_c` 設零；
再以 `Σ_c n_c=1` 排除零解。共同色名置換的 counts 必相同，沒有取環的旋轉或反射商。
實際完整外側染色數必滿足此式；反方向不成立，`y_S` 不是已實現外側的證書。

浮點 LP 只尋找候選。每輪取得的解轉成整數後相加，直到找不出新的正座標；
兩圖分別得到 76 與 130 個全部可行座標的聯集。固定輸出中保存：

- 一份整數 primal，對所有這些座標同時嚴格為正，4,923 條原式逐式精確成立。
- 一份整數 dual，證其餘 78／30 個 D 座標在**所有**可行向量都必為零。

dual 的精確檢查如下。令 `Az=e` 表示上述式及歸一化，`z=(y,n)≥0`；
令 `q` 在待排除 `n` 座標為 1、其餘為 0。證書給整數 `λ` 及 `s>0`，滿足
`Aᵀλ≤−s q` 與 `eᵀλ=0`，故 `0=λᵀAz≤−s qᵀz≤0`，迫全部待排除座標為零。
此 checker 完全使用整數，預設重播不需要 SciPy。兩份 maximal support 也都通過完整布林 D；
所以再做同一 D 固定點不會多刪列。改壞一個 primal 權重、或改壞 dual 歸一化係數的四個負控制均被拒絕。

這個增益屬**既有 block-count 錐**，不算新跨 split 定理，也沒有更動 `LOCK-NO-GAIN`。

## 3. Bernhart 的古典 C 還原：一份可審閱的正控制

下述紙證適用於 [4CT 導覽 §4](../../../research/4ct_guide.md)的假想全體頂點最小反例 `T`：
簡單平面三角化、最小度至少五、無分離三角形；包含上表 **6–6 對角線**的具名補圖，
四個內點度數恰如表、所有八框點互異。這不假設 4CT；只使用 `T` 的最小性。

刪去 `a,b,c,d`，在留下的圓盤內加入兩條互不交叉的弦 `r₀r₂`、`r₄r₆`，
分別收縮為 `u,v`，再加入 `uv`。此圖較 `T` 少六點，仍平面。
兩條收縮邊不是原外側邊：例如若原有 `r₀r₂`，三角形 `r₀r₁r₂` 由無分離三角形而必為面；
內側在 `r₁` 的完整鄰點只有 `a`，外側該面無其他鄰點，迫 `d_T(r₁)=3`，矛盾。
`r₄r₆` 在 `r₅` 同理。故收縮不使任何原邊成 loop，`uv` 的兩端也互異；
parallel edges 可合併。以最小性染較小圖，再拉回原外側，其環列必在

\[
Q=\{b\in U_8:b_0=b_2,\ b_4=b_6,\ b_0\ne b_4\},\qquad |Q|=18.
\]

這是指定替換的來源義務，不是任選一份偏好的外側染色。
有限 D 證書得 `Q∩B∞=∅`：其中 12 列直接延伸，另六列全在固定點前被刪除。
若 `T` 仍不可染，原外側完整關係 `S` 非空且避開 `A(P)`，依已證 D 必要性有 `S⊆B∞`；
但較小圖又供給 `S∩Q≠∅`，矛盾。因此這張 Bernhart 構形不出現在該最小反例契約中。

原文的較小圖起點與 18 列、12 列直接接受相符；本輪以完整 D 證書獨立重播其後的刪列，
沒有逐字轉錄原文選定的 Kempe 推導。圖的收縮安全性是上段紙證，尚未 Lean 或拓撲程式化。
第二張 5–5 對角線圖在同一 `Q` 還有 11 列 D 存活、九列 B₈ 存活；
上述證書不適用，亦不由此宣稱它一般不可約。

## 4. 共同切口接續與停止邊界

新的跨 split 條件應在上述 **76／130 列**的 block-count 殘餘面測試，避免把已知計數增益當成拓撲新意。
只壓縮一段連續 ports，不會自動保存切口另一側的接點順序、重複端點身份與重接關係；
目前未證一個只依有界 boundary 資料的壓縮是對所有實際外側 sound 的。
本輪沒有把尚未證明的「run 壓縮」加進 LP，亦未以未知的外側圖搜尋代替這項義務。
同一切口的既有具名排除由 [共同切口續進](../four-color/four_color_counts_surgery_continuation.md)承擔，
五葉匹配接口由 [parity／shared-cut 續進](../c5/connections/c5_parity_shared_cut_continuation.md)承擔。

已完成範圍為兩張具名圖的身份校正、完整接受集、D、標準 B₈ 最大支援與古典 Bernhart C 正控制。
一般有界跨 split 相容定理、新可約構形、來源覆蓋、不可避免性及 932／4CT 仍 OPEN；沒有新 Lean。
原四張負控制不再被當作「下一個條件必須排空」的預設正向靶標。

## 證據、重播與文件核對

腳本：[ck_bernhart_benchmark.py](../../../../scripts/ck_bernhart_benchmark.py)；
[完整報告及兩份整數 primal／dual 證書](../../../../audits/2026-10-29-bernhart-benchmark-e1a90fe/)。
`report.json` 保存兩圖的完整圖資料、全部 fibre、D 刪列理由、計數錐與來源 SHA256；
`verification.json` 記本輪命令、證據層及閱讀範圍。

```bash
python3 scripts/ck_bernhart_benchmark.py --out /tmp/bernhart-replay.json
uv run --with-requirements requirements.txt --with scipy==1.18.1 python scripts/ck_bernhart_benchmark.py --solve-lp --out /tmp/bernhart-lp.json
```

第一條只讀已存的整數證書、重算原圖 fibre 及精確核對；第二條會重寫本輪兩份 LP 候選證書，
需另行整數驗證，浮點 solver 成功本身不算證明。主求解器未改，未 commit／push。
L0 權威來源為本頁；L1 的 guide／STATUS 由整合者連入，`HANDOFF` 研究線與活躍標記不變。
L2 的既有 D 無增益報告只新增後續連結，其單 split 命題仍成立。
