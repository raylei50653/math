# 局部封環：介面摘要與固定端點接線的第一輪研究

2026-09-13。問題：施工邊界可否內凹、封閉局部區域；封閉後應留下哪些限制；有效端點有界時能否有限狀態化。
本輪完成圖的 separator theorem，以及一個固定圓盤端點、互不交叉路徑的完整 continuation 分類。
沒有宣稱一般 disk patches 已有完整有限幾何 signature，也沒有把固定端點模型當作會移動的施工前緣。

後續討論統一使用 [延伸、接合與強迫的表示法](state_language.md)；含類風格物件、函數記法與可重驗觀察表。

## 1. 可以安全消去的，是未來不會再接觸的內部

以 $B$ 表示具名有效介面，$I$ 為已處理區域的私有頂點，$J$ 為未來區域的私有頂點。
兩圖的頂點分別為 $B\sqcup I$、$B\sqcup J$；接合圖的頂點為 $B\sqcup(I\sqcup J)$。
接合保留兩側所有真實邊，包括各自在 $B$ 上的邊；沒有 $I$–$J$ 邊。

**proved in Lean（普通證明）：**

\[
R_{G\cup_B H}(b)\iff R_G(b)\land R_H(b),\qquad
R_G(b):=\exists x:I\to\mathrm{Color},\ \mathrm{Proper}_G(b,x).
\]

`Math/LocalClosure.lean` 的 `glue` 實際定義上述 simple graph；
`regionOK_glue` 分解圖上的 proper coloring，`summary_glue` 消去兩邊獨立的內部賦色。
`replacement` 隨即證明 $R_G=R_{G'}$ 時，兩塊可對所有這類圖 context 互換。
這比僅將關係交集定義成「接合」多了一個圖語意層。
圖定理本身不含預染色；已承諾的顏色應納入下述 predicates，不能重新自由選色。

**proved in Lean（普通證明）：** `closeRegion`／`seal_future`／`empty_prunes`：

\[
R'(b)=\exists x\,[R(b,x)\land C(b,x)],\qquad
R'(b)\land F(b,y)\iff\exists x\,[R(b,x)\land C(b,x)\land F(b,y)].
\]

$F$ 不可再讀取 $x$。所有仍會被將來的邊、預染色条件或共享 frame 讀取的變數都要留在 $B$。
若某局部環雖已形成、其內部仍準備繼續施工，該區域就還不是可整塊消去的私有部分。
若介面為空，仍有一個空賦色，因此留下 true 或 false，而不是丟掉「不可著色」。

**proved in Lean（普通證明）：** `relation_count`：

\[
\#\{R\subseteq(\mathrm{Fin}\ k\to\mathrm{Fin}\ 4)\}=2^{4^k}.
\]

這是所有 labeled relation tables 的數目，不是可實現 disk patches 的數目，也不表示需要枚舉全部 tables。
全程 $k\le K$ 才得到統一有限的染色狀態空間；每一步有限、最外圈固定，都不足以證明施工前緣有统一界。

**proved in Lean（普通證明）：** R1 `color_free_of_card_le_three`／`exists_colour_of_degree_le_three`／`summary_eq_deletePrivate`：

\[
v\in I,\ \deg(v)\le 3
\Longrightarrow
\operatorname{Summary}(g,b)\iff\operatorname{Summary}(g-v,b).
\]

核心是：最多三個鄰居最多使用三色，`Fin 4` 必有剩餘色。`two_step_free` 現在是這個引理在兩個禁用色時的特例。
C5 形式 `sigma_eq_delete_private` 把同一事實寫成 $\Sigma(G)=\Sigma(G-v)$（$v$ 不在 boundary 像裡）。
這只是染色摘要；不涉及平面、disk embedding，也不重證 `summary_glue`／`replacement`／`seal_future`。

## 2. 一個真正封閉局部環留下的高階條件

取外環 $0$–$1$–$2$–$3$–$0$，內部中心 $x$ 接到全部四點。這是可直接畫在 disk 內的 wheel。
封掉中心後：

\[
R_{\mathrm{wheel}}(b)\iff
\mathrm{Proper}_{C_4}(b)\land\exists c\;\forall i,\ c\ne b_i
\iff\mathrm{Proper}_{C_4}(b)\land b\text{ 沒有用滿四色}.
\]

**proved in Lean（普通證明）：** 泛型 hub 限制 `hub_iff` 證明「中心有可用色」恰等於鄰居賦色不是滿射。
本輪没有另形式化具體 wheel 圖與這個 predicate 的等價。

**computationally observed（獨立整圖回溯）：** C4 的完整關係有 84 個 labeled assignments，wheel 剩下 60 個。
兩者所有六個 pair projections 完全相同，但 `0123` 在 C4 可行、在 wheel 不可行。
因此連「所有兩點精確投影」也不能代替封閉區域留下的完整 joint relation。
全部 256 個邊界賦色均在實際圖上重新判斷，而不是只檢查色數公式。

## 3. 固定端點路徑插入 grammar

固定一個圓盤的 $n\ge3$ 個有序端點 $0,\ldots,n-1$，未來不增加、移動或刪除端點。
字母 $e=(i,j)$、$i<j$ 表示加入新路徑 $i$–$x_e$–$j$，$x_e$ 是新私有頂點。
每條路徑內部互不相交；可共用 boundary 端點。重複同一字母仍是新私有點，形成平行的二邊路徑。

**模型定義（不是一般 topology theorem）：** 歷史合法，當且僅當不存在端點交錯的兩個字母：

\[
\operatorname{Cross}((a,b),(c,d))\iff
(a<c<b<d)\lor(c<a<d<b).
\]

support 記錄出現過哪些字母，不記重數。這個模型允许任意長的歷史，並可形成很多局部環；
例如同一對端點的兩條新路徑形成四環。然而它不允許把新端點開在那些內部路徑上，
也不允许封環後再进入某個內部面施工。

**幾何解釋（紙面論證，未 Lean 化）：** 交錯的兩條內部不相交路徑不能同置於 disk；
無交錯的有限 support 可以畫成凸多邊形內的弦，共端點只在端點相接。
同一弦的有限重數可在窄帶中畫成平行路徑。這支持此 grammar 的幾何模型，
但不構成任意 disk patch 到這個 grammar 的抽取定理。
Python 另用整數凸多邊形 $(i,i^2)$ 的線段 orientation，獨立核對全部 support 的交叉判斷；
這個有限座標檢查不自動證明任意曲線的拓撲必要性或任意重數的窄帶論證。

## 4. 精確幾何摘要：禁止哪些下一條路徑

對合法歷史 support $S$，定義

\[
F(S)=\{e:\exists d\in S,\ \operatorname{Cross}(d,e)\}.
\]

**proved in Lean（普通證明）：** `Math/LocalWiring.lean`：

* `continue_iff_union`：共同 context $T$ 可接上，恰等於 $S\cup T$ 合法（假設 $S$ 原本合法）。
* `forbidden_union`：$F(S\cup T)=F(S)\cup F(T)$。
* `update_congruent`：同摘要的兩個歷史經共同更新後仍同摘要。
* `residual_exact`／`chord_residual_exact`：所有未來 contexts 都無法區分兩個合法歷史，恰等於它們的 $F$ 相同。

最後一項不只是充分性：若 $F(S)\ne F(S')$，從對稱差選一個字母 $e$，單字 context $\{e\}$ 就能區分。
定理先對任何 irreflexive conflict alphabet 證明，再對具體有序端點 `Chord n`、`Cross` 實例化。
有限字串的順序與重數在此 grammar 不影響接受性，因此集合 context 已涵蓋任意長的字串 continuation。
若歷史已不合法，另用吸收 dead state；不可把它混入 live histories 的上述等價。

因此這個模型的更新是：

\[
F\xrightarrow{e}
\begin{cases}
\mathrm{dead},&e\in F,\\
F\cup\{d:\operatorname{Cross}(e,d)\},&e\notin F.
\end{cases}
\]

其活摘要上界為 $2^{\binom n2}$（直接有限集合計數；本輪未單獨 Lean 化此二項式上界）。
這個摘要只回答接線可行性，不是著色約束。固定端點純插入只會增加禁止集合；
它沒有模擬移動前緣、開洞、換面或忘記端點後的更新。

## 5. 小介面的完整分類

**computationally observed（完整有限枚舉，具體類數尚未 Lean replay）：**

| 端點數 | 合法 supports | 活 residual 類 | 含可達 dead 的總類數 |
| ---: | ---: | ---: | ---: |
| 3 | 8 | 1 | 1 |
| 4 | 48 | 3 | 4 |
| 5 | 352 | 11 | 12 |
| 6 | 2,880 | 45 | 46 |

`artifacts/local_closure/classification.json` 保存字母順序、全部 support→class、代表、完整轉移、每對 classes 的 separator。
對 $n=3..6$ 檢查全部 33,864 個 supports、47,032 次合法 support 的單字更新、1,107 組 separator。
Support 的生成使用端點交錯，独立幾何 replay 使用整數 orientation。
對 $n=4$ 全部 48 個合法 supports 另逐一做整圖著色回溯，共 12,288 個邊界賦色查詢。
沒有因表格到 $n=6$ 而主張一般移動前緣或一般 disk patches 的界。

**conjectured／未證：** 在這個固定端點 grammar 中，忽略 boundary-adjacent 字母後，
不同合法 diagonal supports 是否總能被未來區分？$n=3..6$ 的類數與合法 diagonal support 數相等；
尚未證明全 $n$ 的此項結構刻畫。本輪的泛型 $F$ 等價定理不需要這個猜想。

## 6. 完整染色關係仍不能决定接線合法性

固定外環 C4，令：

* $P$：內部路徑 $0$–$x$–$2$。
* $Q$：內部路徑 $1$–$y$–$3$。
* 共同 context $T$：新的內部路徑 $0$–$z$–$2$。

**proved in Lean（普通證明）：** `two_step_free`、`path_network_free`：任意兩個端點色總有不同於兩者的第三色，
任意多個獨立二邊路徑可同時延伸。因此這些路徑不對已給定的邊界色增加限制。
`two_step_free` 由 `color_free_of_card_le_three` 推出；degree $\le 3$ 的密封內點刪除見 §1 的 R1。
這是 path constraints 的泛型證明；本輪未把此特殊路徑圖 constructor 另連到 `Summary`。

**computationally observed（整圖 replay）：** $P,Q,P+T,Q+T$ 全部有相同的 84 個完整 labeled boundary colorings。
但 grammar 中 $P+T$ 合法、$Q+T$ 不合法。$P+T$ 的兩條 0→2 路徑形成可實現的局部四環。
Artifact 保存 $P+T$ 的整數座標 embedding，逐對驗證無共端點的線段不相交。

對 $Q+T$，artifact 保存兩條端點交錯的內部互不相交路徑，以及加 exterior apex 後的 K5 subdivision：
branch vertices 為 $0,1,2,3,6$，十條 branch paths 的真實邊及內部互不相交性由 checker 驗證。
**紙面拓撲推論（未 Lean 化）：** 若指定 C4 可作 disk 邊界，外側可加連到四個 boundary 點的 apex；
得到平面 K5 subdivision，收縮後違反 K5 的平面 Euler 邊界 $10>3\cdot5-6$。
所以這是指定邊界的同側放置障礙；不宣稱原本 $Q+T$ 抽象圖非平面。

此例甚至不需要較大 gadget catalog：染色語意完全一樣，幾何後續已可區分。
因此一般幾何搜尋的 candidate state 至少應把染色資訊與接線資訊分開；
本輪没有證明 $(R,F)$ 可處理 grammar 外的任意連通內部塊。

## 7. 驗證、信任界線與下一個問題

```bash
python scripts/local_closure.py          # 決定性重建本輪 artifact
python scripts/local_closure.py --check  # 完整重算、獨立 replay、逐 byte 比對
lake build
lake env lean Math/LocalClosureAudit.lean
```

新 Lean 定理全部為普通證明（含 R1：`summary_eq_deletePrivate`、`sigma_eq_delete_private`）；
公理審計輸出保存於 `artifacts/local_closure/lean-audit.txt`。無 `sorryAx` 或 native compiler axioms。
Python 表格不是 Lean 的可信輸入，枚舉類數和具體 graph replay 仍標示 computationally observed。
既有大型 catalog、strip 和 topology completeness 搜尋沒有重跑。

下一步應研究**允許在已建路徑上開新端點、或切換活動面時，必須補哪些資訊**。
目前的 $F$ 只記固定端點間的後續衝突，沒有保存活動面的邊界 walk、端點 occurrences 或剩餘可施工區域。
应先明確定義一個帶活動面的 introduce／close／forget 操作，再找同 $(R,F)$ 的歷史被它區分的證書；
不直接增加端點數，也不把這輪有限表格當成一般有限性證明。

## 8. 後續注意：週期與控制策略（暫存，不啟動）

使用者於 2026-09-13 指定：週期／博弈式控制先留作後續注意事項。
將來若研究移動前緣，需區分完整狀態週期、只在染色摘要上重複，以及內部持續累積但摘要不變。
安全循環不等於可強制維持的策略；避免失敗也不等於保證完成。
先建立保留幾何合法性、端點對齊與活動面的狀態，再考慮策略與週期證書；目前未建立一般模型或勝策定理。
