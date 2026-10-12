# 同色見證識別、共面完備性與最小反例的三角面正規形

2026-10-12。隔離紙面結果；輸入固定於 [INPUTS.json](../INPUTS.json) 的
`ab0862485b30b12b538c734271f354630afa8e26`。本頁不修改既有 source、catalogue
或證書，不宣稱已排除所有反例。下列一般引理是紙面證明，尚未 Lean 化。

## 1. 契約與有限前提

圖類別是有限**簡單**圖，帶固定有序邊界
\(B=(b_0,b_1,b_2,b_3,b_4)\)，有一份畫在閉圓盤中的嵌入，邊界正是這個
指定 C5，其餘頂點在圓盤內；除原 C5 框邊外，每条邊的非端點部分均在圓盤內。
允許內側 boundary chords；
不預設 connected、2-connected 或 triangulated。
\(n(G)=|V(G)\setminus B|\)，\(\Sigma(G)\) 是完整的可延伸關係，固定
`pattern_order`，只商掉同一份完整染色上的全域 S4 色名置換。

令 \(K\) 為 frozen `cells.json` 的 132 個有至多五內點 witness 的關係。
本論證使用的有限前提為：

1. 每個真實 disk cell 的關係屬於 \(K\)，或屬於 933、941 的兩個 D5 軌道。
   這是 frozen Kempe screen、外側相容測試及 4CT 的合併必要條件，並非把有限
   graph 搜尋升格成一般排除。
2. 在固定十 bit 座標中，

   \[
   \{k\in K:k\subseteq933\}=\{165\},\qquad
   \{k\in K:k\subseteq941\}=\{165,424,429\}.
   \]

   這些子關係全部不含 \(p_*=01232\)。933 下的唯一子關係另外不含
   \(01231\)。
3. \(K\) 在整圖 D5 對齊下封閉。若候選來源的關係在上述軌道中，須對**整張圖、
   五個 boundary labels、所有完整染色**施作同一個 D5 對齊，才使用此表。
4. \(K\) 在二元聯集下封閉：\(A,B\in K\Rightarrow A\cup B\in K\)。這是
   132 個 frozen 關係的 8,778 個含對角無序配對的有限聲明，無須為兩個 witness
   構造平面聯集。它將提供比個別 \(p_*\) 表更一般的最小反例正規形骨架。

第 1 項中，1,023 個非空十 bit 關係的篩選分類可從 frozen 檔有限重驗；
「任意 disk cell 都滿足 Kempe／外側相容條件」仍依賴既有紙面平面分離論證
及 4CT。第 2–4 項是可重驗的有限關係聲明。後面的拓撲及最小性論證也不由
有限測試取代。只需要各 \(K\) 元素的五內點 witness，不需要假定 graph
enumeration 已窮盡所有五內點圖。

兩候選皆全收 \(T_4\)，故沒有 boundary chord：每條 chord 的兩端正好是某個
四色 boundary pattern 的唯一同色對，存在此邊便會禁止該 pattern。

## 2. 合法識別的精確語義

在指定 disk drawing 中，稱不同頂點 \(u,v\) 為「內側共面」，若存在一條
端點為 \(u,v\)、其餘部分位於同一內側 face 且避開圖的簡單弧。
即使 face 的邊界 walk 重複頂點或邊，此定義仍指定可用的 incidences；
不預先把面界當成 simple cycle。

假設 \(uv\notin E(G)\)，且至少一個端點為 interior。沿上述弧加一條暫時邊，
再收縮它，刪除生成的平行邊，得到簡單圖 \(Q=G/(u=v)\)。

- 若兩端都是 interior，合併點仍為 interior，五個 boundary vertices 逐一固定。
- 若一端是 \(b_i\)，保留該點及 label \(b_i\)，把另一個 interior 頂點移入它。
  弧除這個端點外全在 disk 內，故收縮可在 disk 中完成，邊界 C5 的五個點、
  邊及 cyclic order 都不被識別。原 interior 點的邊可能變成 boundary chords；
  這符合圖類別。
- 原先 \(uv\) 非邊，故去掉暫時邊後不生成 loop；刪除平行邊不影響正常著色。
  若平行邊中有原 C5 框邊，保留該原框邊、刪去內側 copy，保持原邊界及其 rotation。
  即使原圖有橋、割點或重複面界，該弧的局部收縮仍給合法 disk embedding。
- 不准識別兩個 boundary vertices，因為這會破壞固定五點邊界契約。

令

\[
E_{uv}(G)=\{p:\exists f\text{ extending }p, f(u)=f(v)\},\qquad
D_{uv}(G)=\{p:\exists f\text{ extending }p, f(u)\ne f(v)\}.
\]

著色沿 quotient 映射拉回與下降，逐份 boundary assignment 給出

\[
\Sigma(Q)=E_{uv}(G),\qquad
\Sigma(G+uv)=D_{uv}(G),\qquad
\Sigma(G)=E_{uv}(G)\cup D_{uv}(G).
\tag{1}
\]

兩個子關係可重疊；這不是分割。式 (1) 同時涵蓋 interior–interior 與
interior–boundary。由於至少一個端點為 interior，\(n(Q)=n(G)-1\)。

特別地，當 \(E_{uv}(G)=\Sigma(G)\) 時這是保完整關係的縮減。條件是每個
boundary state 各有一份同色延伸，不要求所有延伸都同色；多對識別不得把
各自存在的見證拼成同一份著色，須逐次重新驗證當前完整關係。

## 3. 一個固定 boundary state 統一阻止所有識別

假設有 \(\Sigma(G)\notin K\) 的來源，在**所有**這类來源中令 \(n(G)\)
最小，然後用一個共同 D5 對齊使其關係為 933 或 941。

**統一異色引理。** 對每份延伸 \(p_*=01232\) 的完整染色 \(f\)，及每一對
不同的內側共面頂點 \(u,v\)，只要至少一端是 interior，就有

\[
f(u)\ne f(v).
\tag{2}
\]

相鄰端點由 properness 得到此結論。若非相鄰且某份 \(p_*\) 延伸使兩端同色，
§2 給出較少內點的 \(Q\)，其關係包含 \(p_*\) 且包含於 \(\Sigma(G)\)。
由最小性 \(\Sigma(Q)\in K\)，卻與 §1 的子關係表矛盾。

933 情況下，完全相同的證明也適用於 \(01231\)。兩者都是每份完整延伸
各自滿足 (2)，不表示存在一份完整染色同時具有兩種不同 boundary patterns。

此處必須在所有 catalogue 外來源中選最小內點，不能只在 \(\Sigma=933\)
或只在 \(\Sigma=941\) 的來源中取最小，因為 quotient 的關係可能改變。

## 4. 最小來源的共面完備性

**一般母題：union-closed 關係目錄與 equality/disequality 分解。**
令 \(\mathcal K\) 是完整 boundary 關係的一個二元聯集封閉集合。假設圖類別
對 §2 的加邊、識別並刪平行邊操作封閉。在所有 \(\Sigma(G)\notin\mathcal K\)
的來源中，先令 interior 數最小，再令簡單圖的邊數最大。
則任意共面且至少一端 interior 的不同頂點都相鄰。

證明：若 \(uv\) 是上述缺邊，\(Q=G/(u=v)\) 的內點減少，所以
\(\Sigma(Q)\in\mathcal K\)。由 (1)，

\[
\Sigma(G)=\Sigma(Q)\cup\Sigma(G+uv).
\]

若 \(\Sigma(G+uv)\) 也在 \(\mathcal K\)，聯集封閉性會迫使
\(\Sigma(G)\in\mathcal K\)，矛盾。因此加邊所得圖仍在目錄外，內點數相同、
簡單邊數卻增加，違反最大性。此證明不需要 \(p_*\)、D5、四色或特定十 bit 表；
只需操作合法、識別降低衡量大小及完整關係滿足 (1)。

套用 \(\mathcal K=K\) 即得本題的**共面完備引理**。固定頂點數只有有限多張
簡單圖，故上述 extremal 選擇存在。§3 的 \(p_*\) 證明則提供額外資訊：在
任意內點最小來源中，尚未作 edge maximization 前，所有相關點對就已在每份
固定 \(p_*\) 的延伸中統一異色。

亦可在「最小內點」與「最大邊數」之間插入 \(|\Sigma|\) 最小的選擇。
因為 \(\Sigma(G+uv)\subseteq\Sigma(G)\)，上面的聯集論證先迫它在目錄外，
\(|\Sigma|\) 最小性再迫 \(\Sigma(G+uv)=\Sigma(G)\)，最後仍與最大邊數矛盾。
這個可選副序的作用只是額外證明 hypothetical 加邊保留完整 \(\Sigma\)。

此處的 extremality 是**在所有 catalogue 外來源中全域最小 interior 數，再最大
邊數**。它不是既有固定 \(\Sigma\) 的 edge-minimal／edge-critical source，
不能將後者的 deficiency、Gallai 結構或其餘邊臨界前提直接套在本圖上。

## 5. 割點與面界：不偷渡三角化前提

先證所選 \(G\) connected 且 2-connected，這只使用 §3 的內點最小性。

\(\Sigma(G)\) 非空，故固定一份既有完整著色。若有不含 boundary 的 connected
component，把它刪除。該 component 已有正常著色，可獨立接回，所以刪除保留
完整 \(\Sigma\)，並嚴格減少內點，矛盾。

若 connected \(G\) 有割點 \(z\)，五邊界點除去可能的 \(z\) 仍由 C5 的剩餘
path 連通，故它們全在 \(G-z\) 的同一 component。取另一個 component \(W\)，
其頂點皆為 interior。從既有著色限制得到 \(G[W\cup\{z\}]\) 的著色；對任意
\(G-W\) 的著色，對枝塊的色名做一次全域排列，使 \(z\) 的顏色相合，即能
接回整塊。因此刪除 \(W\) 保完整 \(\Sigma\) 並減少內點，矛盾。

所以 \(G\) 是有至少五點的 2-connected plane graph；特別地沒有橋，每個
face 的 boundary walk 是 simple cycle。這一步不需額外使用 4CT，因為枝塊
可著色性直接來自 \(G\) 的既有完整著色。

## 6. 三角面正規形：排除「已存在的對角線在面外繞行」

**正規形定理。** 若存在 catalogue 外 disk cell，就存在內點数同樣最小的
**簡單、2-connected、外界恰為指定 chordless C5、所有 bounded faces 都是三角形**
的 catalogue 外來源。

取 §§4–5 的 \(G\)。設一個 bounded face 的 simple boundary cycle \(F\)
長度至少四，且含 interior 頂點 \(x\)。沿 \(F\) 取與 \(x\) 不連續的
頂點 \(y\)。§4 迫使邊 \(xy\) 已在圖中；因 \(F\) 是 face，這條非面界邊
畫在 \(F\) 的另一側，不能把它假裝成可直接新增的對角線。

在兩條 \(x\)–\(y\) 面界弧的內部分別選頂點 \(u,v\)。四點在 \(F\) 上的
循環次序為 \(x,u,y,v\)。在球面上考慮 \(F\) 的另一側，它是一個閉圓盤。

- 若 \(u,v\) 至少一個是 interior，§4 給出已存在的邊 \(uv\)。它也在 \(F\)
  的另一側，且與 \(xy\) 端點互異。
- 若 \(u,v\) 都在 boundary，在原 disk 外添一個 apex \(a\)，連接所有五個
  boundary vertices。五條邊可在外側 disk 中畫成無交叉 star。於是
  \(uav\) 是位於 \(F\) 另一側的簡單路徑，且與 \(xy\) 頂點不交。

兩種情形都在同一圓盤內給出頂點不交的 \(x\)–\(y\) 與 \(u\)–\(v\) 連線，
而四端點在圓周上交錯，違反 Jordan 分離性。因此 bounded face 若含 interior
vertex，其長度只能是三。

剩下全由 boundary vertices 組成的 bounded facial cycle。因 \(G\) 沒有 boundary
chord，它只能是整個 C5。該 C5 的有界側就是原 disk 內部；若它整側是一個
face，便沒有任何 interior 圖。連通性遂使 \(G=C5\)，其關係為
\(1023\in K\)，矛盾。故不存在這種面。

這個證明明確處理了已存在於面外的對角線，沒有對原圖預設 triangulation，
也不新增 hub、interior vertex 或平行邊。apex 只用於分離論證，不是最後 cell
的一部分。結論是條件式最小反例正規形，不是「任意給定來源都可逐步保 Σ
而在同樣頂點集補成三角化」的演算法聲明。

## 7. 接上既有文獻的有界推論

引用 Dvořák–Lidický，*Coloring count cones of planar graphs*，
[arXiv:1907.04066v2](https://arxiv.org/pdf/1907.04066v2)，Observation 3、Corollary 20。
Corollary 20 證明文中的 degree-5 near-cubic 計數不等式適用於少於 30 個頂點
的 plane near-cubic 圖。這是外部、含電腦輔助的文獻定理，本 audit 沒有重播
其計算證書。其與本題記號的轉換沿用
[frozen count-cone bridge](../frozen/docs/c5_count_cone_bridge.md) §§1、4。

為清楚標出新的推論，假設 \(G\) 是 §6 的最小 catalogue 外來源，令其內點數
為 \(n\)。Euler 計數給出

\[
|E(G)|=3n+7,\qquad |V(G^*)|=|F(G)|=2n+4.
\]

dual 的 outer-face vertex degree 為五，其餘頂點 degree 都是三，符合文獻類別。
simple primal 不保證 simple dual，但該文允許 parallel edges；本圖無橋，dual
也不因橋而產生 loop。對固定 boundary assignment 的延伸數，文獻 inequality
在本題記號為

\[
3\sum_i y_i\ge\sum_{uv}x_{uv}.
\]

既有計數恆等式
\(x_{uv}=m+\sum_{i\notin\{u,v\}}y_i\) 給出
\(\sum x=5m+3\sum y\)，故文獻 inequality 是 \(m\le0\)。
反之，933 或 941 的 singleton support 都包含於 \(\{2,4\}\)，而固定
\(p_*=01232\) 的延伸存在。因此 \(x_{24}=m>0\)，矛盾。

Corollary 20 在 \(2n+4<30\)，亦即 \(n\le12\)，適用。故得到

\[
\boxed{\text{任何 catalogue 外 disk cell 若存在，其最少內點數至少是 }13.}
\]

因此，由每個 \(K\) 元素已有五內點 witness，再得

\[
\boxed{K_{\le12}=K_{\le5}=K.}
\]

這是**既有有限 screen／catalogue 聯集封閉性 + 本頁一般正規形引理 + 外部 Corollary 20**
的紙面推論，不是本 audit 新枚舉了六至十二內點圖。與 frozen 文件只直接排除
「已是 near-triangulation 且內點不超過十二」相比，新處在於正規形不增加
最小來源的內點，因此把同一文獻界轉移到一般簡單 disk cells。

## 8. 保留界線

- \(K_\infty=K_{\le5}\) 仍然 OPEN；\(n\ge13\) 的最小反例未被排除。
- 933、941 仍只是尚未排除的完整關係，沒有任何 source realizability 聲明。
- 共面完備性與三角面正規形不表示每個 interior 有低度數；任意大三角化仍是
  尚待研究的可能形狀。固定 \(p_*\) 的 (2) 在三角面上退化為 properness。
- 本頁不聲稱跨不同 fibres 的 Kempe 操作可同步，也不聲稱任意邊 flip 或刪除
  保留 \(\Sigma\)。兩對各自可識別仍不等於可同時識別。
- 拓撲弧收縮、割點消除、Jordan 分離、最小性選擇、dual 翻譯及外部文獻引用
  尚未由本頁提供 Lean 證書。有限檢查、紙面引理與外部定理保持分開。
