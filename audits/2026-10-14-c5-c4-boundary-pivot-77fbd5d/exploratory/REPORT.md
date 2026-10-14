# 次方向：同圖 matching 與偶圈條件

本子包保存這次轉向中的探索結果。**不作為主包 C4 有界排除的證明依賴**，也沒有排除任意大小的 933／941。一般 matching 交換出口仍 OPEN；以下正結果是任意大小的表示引理及既有固定圖上的有限實驗。

## 1. 完整 matching 表示

固定 near-triangulation 的原三價 dual 5-pole H，保留五個有序 terminals、全部原 edge ids 及 rotation。給定少數色位置對 P，令 M(P) 為覆蓋全部內點、恰覆蓋 P 外三個 terminals 的 matchings；亦即刪去 P 的兩個 terminal vertices 後的 perfect matchings。

刪除 matching 邊後，每個內點度數二，恰有一條連接 P 的路徑，其餘分量為閉圈。內點數 n 為奇數，因為 3n+5 為偶数。若所有閉圈均為偶圈，路徑就含奇數個內點、偶數條邊（計入兩條 terminal 邊），可按固定兩端的不同少數色交替染色。

將 matching 邊染多數色 1；每個偶圈有兩種獨立 phase，而路徑的 phase 已由固定端色決定。因此對一份固定色名邊字：

\[
N_P=\sum_{M\in M(P),\;H-M\text{ 無奇圈}}2^{c(H-M)}.
\]

這是完整染色雙射，無額外 6／24 乘數；空 fibre 也保留。直接 terminal-to-terminal strand 照常納入 component tracing。任意 matching 還滿足「路徑邊數奇偶＝奇圈數奇偶」，但偶數個奇圈仍不合格，不能只查總 parity。

原色框的 933 只有 y4，941 有 y2、y4；關鍵 x_vertex24 對應少數位置 {1,4}，其延伸數為 m>0。共同旋轉成 singleton 支援包含於 {0,2} 後，關鍵少數位置是 {2,4}，被拒絕的相鄰位置對是 {0,1}、{2,3}、{3,4}。

## 2. 同圖交換與精確缺口

稱補圖無奇圈的 matching 為合格。若兩個合格 matchings M、N 的對稱差只有一條 alternating path 或 cycle，就得到一次同圖交換：直接交替染 N 的完整補圖，便構造同一 H 的另一份完整染色。這不假設它是原染色的一步 Kempe move。

確切區別如下。把 H−M 每個分量的邊交替標為 parity 0／1。交換路徑 A 能在獨立調整舊分量 phase 後成為「matching 色與同一少數色」的雙色路徑，當且僅當 A 的非 M 邊在每個舊補圖分量內都屬同一 parity。前後均合格不保證這件事。

可繼續研究的窄目標是：若相鄰少數位置只容許 {0,4}、{1,2}，能否從關鍵 {2,4} 的某個合格 matching，沿保持補圖無奇圈的原圖交換到達被拒絕位置？只需存在一條路徑便足以給該固定来源的矛盾；不必證一般計數不等式 m≤0，也不必先證整個交換圖連通。此一般出口尚未證明。

## 3. 有限核對與反控制

[checker.py](checker.py) 只讀既有 76 份 near-triangulated catalogue 控制與三份 survivor 控制；沒有生成新來源圖。NetworkX 3.5 回復原控制的 embedding，沿用 helper 逐 directed incidence／Euler 核對面。結果見 [results.json](results.json)。

| 核對 | 結果 |
|---|---:|
| 固定圖實例／固定 boundary fibres | 79／790 |
| 完整 primal 染色 representatives | 1,351 |
| 全部 terminal matchings／合格 matchings | 2,109／868 |
| 合格 matching 交換邊 | 3,842 |
| 不滿足舊補圖 phase 相容的交換邊 | 2,140 |
| 關鍵 {2,4} 起點 | 68 |
| 這 68 起點沒有禁位置出口者 | 0 |
| 最短出口距離的最大值 | 2 |

790 份固定延伸計數均與上式獨立匹配。三個舊 survivor 的關鍵 matchings 全部有一步同圖 matching 出口。具名 survivor-590 使用一條 **20 邊 alternating path**，由少數位置 {2,4} 轉到 {2,3}；前後補圖均無閉圈，但原補圖 phase 不相容。JSON 保存原圖、oriented faces、原 dual edge ids、兩份 matchings，並實際積分出前後完整 primal 染色，邊界分別為 01023、01021。

同時保留三個失敗捷徑：

- **忽略奇圈不成立。** 七點 catalogue-189 的四邊 alternating path，把合格 matching（補圖一條八邊路徑）變成不合格 matching（補圖一條三邊路徑及一個五圈）。
- **閉圈數單調下降不成立。** 枚舉全部單一 dual 雙色 path／cycle swaps 後，229 份可到禁 singleton 的染色無法在多數色補圖圈數不增加下到達。另有 107 份四色狀態已是零圈且無一步出口。最小保存控制 catalogue-199 有六個 primal 頂點：零圈可達狀態的禁出口必增加到一圈。
- **普通 delta-matroid 交換不能直接套用。** 真實 pentagon 5-pole（primal wheel）的單色 terminal 支援 family 包含五個 singleton 與五個循環連續 triples。取 A={0,3,4}、B={0,1,2}、x=2，所有 y∈A△B 都使 A△{x,y} 不在 family。JSON 保存全部 family 與逐 y 負控制。

這些有限控制不包含完整 Σ=933／941 的來源；零失敗不是一般出口定理。主包若有新的有界排除，依其獨立證據鏈，不依賴本子包的探索性推測。

## 4. 重播

```bash
uv run --with networkx==3.5 python audits/2026-10-14-c5-c4-boundary-pivot-77fbd5d/exploratory/checker.py --check
```

不帶 `--check` 才會重寫本子目錄的 `results.json`；帶參數時獨立重算並作逐 byte 比對。證書記錄直接來源腳本、三個原始 JSON 的 SHA-256。當輪使用本機唯讀 NetworkX 3.5 cache 執行，default／seed17 的 `--check` 均須通過；沒有新增 Lean theorem。
