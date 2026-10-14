# T1 廣化試驗：固定雙 C6 介面與 C8 正對雙接點

狀態：**有限核對 PASS；來源覆蓋證明草案，待正式獨立審查／採納。**

研究來源固定於 `raylei50653/math@77fbd5da7ba273f0af7c75175dc08376d2282f46`。
本包在 ChatGPT 當前容器中產生；未修改或提交遠端 repository，未執行 Lean build。
兩個核對程式採不同建圖、著色、分割與矩形枚舉路徑，但都是本次對話撰寫，
不應稱為已完成第三方數學審查。下面明確區分普遍接合引理、來源幾何及有限證書。

## 1. 候選來源結論

保留 no4ct 全域最小目錄外 C5 來源契約及原八份 h=3 collars／targets。
對其中的原 C8 內側 H，候選結論是

\[
 h=3\quad\Longrightarrow\quad p=0.
\]

即任何嚴格內點都不能同接原 C8 的一對正對點；由已發布的接點分類，
第一剝層只剩 RING。這將同時涵蓋全部 PINCH／BRIDGE、所有非負 s_+,s_-，
以及任意有限兩側內點數，而不僅是 s=1 或 s=2。

本結論未排除 RING，未提高一般 K≤15 等式、一般 h=3 的 k≥19，
也不處理 h≥4／C9。一般 K∞=K≤5 仍 OPEN。

## 2. 直接來源與固定資料

使用下列已讀的 immutable 路徑。Git blob SHA 不是 SHA256：

| 路徑 | Git blob SHA／用途 |
|---|---|
| `docs/c5_c8_peeling.md` | `6905c30a808cb0329788fe37a4360b989b7148dd`；原 C8 與接點分類 |
| `audits/2026-10-13-c8-terminal-s1-d521163/theory/PROOF.md` | `5f44cbd4d5da7f80b58e23727b01ac0fcbc4b0e2`；literal 接合與安全軌道判準 |
| `audits/2026-10-13-c8-terminal-s1-d521163/review/independent_transfer.py` | `ae35095273264782cc536cca30db2629badeb566`；原 B 十列、八份 query、collar 命名 |

本包不是整個 repository 的 frozen-input／seal 重播；它只固定上述引用及
實際使用的資料。原 no4ct 來源契約和外部有限計算信任保持原狀。

B 十列按 bit 0..9：
`01012 01021 01023 01201 01202 01203 01212 01213 01231 01232`。

八份 query（tuple 是原超額配置 e）：

```
c15-933 (0,1,2,0,0) 933
c18-933 (0,2,1,0,0) 933
c04-941 (0,0,1,0,2) 941
c07-941 (0,0,2,0,1) 941
c15-941 (0,1,2,0,0) 941
c18-941 (0,2,1,0,0) 941
c20-941 (1,0,0,0,2) 941
c30-941 (2,0,0,0,1) 941
```

沒有用 U 的近似大小替代原外框完整 target，沒有把 933／941 分別最小化。

## 3. T1 的一般形式

設 G=P∪L、V(P)∩V(L)=D，所有原邊均在某片中，B 在固定外側 P。
對原有序 D 的四色軌道 q，先在同一 literal 色框完成 P 的延伸枚舉，再定義
M_P(q) 為它能產生的 B 原列集合。未知 L 的完整支援 R_L 是 S4 軌道聯集。
因此

\[
 \Sigma_B(G)=\bigcup_{q\in R_L}M_P(q).
\]

對固定 target τ，令

\[
 \Phi_P(\tau)=\bigcup_{M_P(q)\subseteq\tau}M_P(q).
\]

若 Φ_P(τ)≠τ，任何未知 L 都不可能產生 target，無論 L 有多少內點。
若相等，只表示任意抽象 S4 支援的放寬有解，不證可由平面圖實現。
這個接合判準不要求 D 為 C6；平面性是後續 Kempe 限制所需，而非聯集等式所需。

## 4. 更外層的切口：不必讓介面隨 s 增長

假設原 x∈V(H)\C 同接 c_i,c_(i+4)。原嵌入中的路徑

\[
 c_i-x-c_{i+4}
\]

是 C8 disk 的一條內部簡單 crosscut。兩側閉 disk 的原邊界分別為

\[
 D_+=(x,c_i,c_{i+1},c_{i+2},c_{i+3},c_{i+4}),
\]
\[
 D_-=(x,c_{i+4},c_{i+5},c_{i+6},c_{i+7},c_i).
\]

它們都是具名 C6，交集是同一條三頂點、兩條邊的原路徑；不是兩個獨立的 x。
平面性禁止兩個開 disk 之間有未經交界的跨片原邊。
將各側全部原圖內容（原 terminal、其附件、任意多單接點、其他正對點、
任意深的內部及全部原邊）都留在該側 L_±。

外側 P 只含固定 B–C8 annulus、x 及兩條 spokes。這個 P 不隨 s_± 或內點數改變。
B/C 原點的其他同側邊由 L_± 保留，不預設兩片無弦、最低度或有限內點數。

程式中這個一般單點 crosscut 的歷史標籤是 `PINCH`。
**它不需要先假定 Q 屬於 PINCH 型：即使原 Q 是 BRIDGE，選其任意一個正對點
作上述 crosscut，另一個正對點及橋也被吸收進某一側 L。**
所以 8 collars×4 正對位置=32 份 `PINCH` 核心已足以支撐候選結論。
另有 32 份帶兩個正對點與橋的 `BRIDGE` 固定外殼作額外檢查，不是主結論所必需。

尚需正式獨立覆核的幾何責任是：確認上述 cut 對已發布的八份來源身份完全覆蓋，
並確認原 annulus 命名與 source-to-shell 映射沒有遺漏；小圖建模測試不能取代這一任意來源證明。

## 5. 雙片的完整關係必須是同一個直積

每個 proper C6 有 31 個 S4 軌道。令 R_+、R_- 為同一原圖兩個固定 disk 的完整支援。
枚舉同一 P 的全部 literal 著色後，定義 M_P(q,r)：兩個界面同時落在 q,r 時能產生的 B 列。
界面共享的 x、c_i、c_(i+4) 及原邊都由這份 P literal 著色同步。
先共同 literal 枚舉，才轉成兩個軌道 index；絕不分片先改色再直接黏合。

對任一殼著色，q∈R_+、r∈R_- 保證兩份同 literal 界面的完整 lifts 都存在，
其內點互不重疊、交界同色，因此能唯一黏合。反向任意 G 著色限制到 P 與兩片即得該資料。
所以支援有精確等式

\[
 \Sigma_B(G)=\bigcup_{q\in R_+,\ r\in R_-}M_P(q,r).
\]

對 target τ，令 E_τ={(q,r):M_P(q,r)⊆τ}。必要有

\[
 R_+\times R_-\subseteq E_\tau.
\]

0 輸出 mask 的軌道對也保留。不同接受 B 列不能各自挑選不同 R_+、R_-。
僅把所有安全 pair 取聯集會丟掉此直積要求，是不夠強的放寬。

## 6. 只使用必然的 C6 Kempe 支援限制

固定某個 C6 row 與一組互補色對，例如 {0,1}/{2,3}。
任意真實平面 disk 染色的兩色連通分量，在 C6 上誘導一個非交叉分割：
每塊屬於同一色對，且邊界上同色對相鄰頂點必在同一分量。
兩個 vertex-disjoint 連通子圖不能連接交錯的圓周端點，故實際分割一定在所列必要域中。

對每個候選分割，獨立交換每個分量的兩色得到完整 row 軌道 O。
不同分量之間的邊若跨互補色組，交換後仍異色；同一色組的不同分量沒有邊。
因此交換的每個 row 都是同一 disk 的合法染色。

對候選支援 S，若 row r 的某色對 split 沒有任何候選 O 完全包含於 S，就可刪 r。
任何真實支援 R⊆S 都不會被刪：其真正染色供應實際分割與全部交換。
反覆刪除得到 κ(S)，仍包含 S 中任何真實 planar 支援。
這不假設普遍四色可染性，也不宣稱通過 Kempe 條件就可實現。

## 7. 為何有限枚舉窮盡所有未知雙片支援

任何 R_+×R_-⊆E_τ 都包含於某個極大安全矩形 A×B。
令 N(q)={r:(q,r)∈E_τ}。所有極大矩形可由所有 N(q) 的交集 B 及
A={q:B⊆N(q)} 枚舉；包括空側的退化項。

由真實支援的 Kempe 必要性，R_+⊆κ(A)、R_-⊆κ(B)。因此必有

\[
 \tau\subseteq \bigcup_{q\in\kappa(A),r\in\kappa(B)}M_P(q,r)\subseteq\tau.
\]

若每個矩形的右端聯集都少了 target 某列，就排除任意兩個 planar disk，
無論其內點數、接點數或內部結構。

## 8. 本輪實際結果

| 核對域 | 具名 cases | 完整極大安全矩形 | 結果 |
|---|---:|---:|---|
| 一個正對點 crosscut（檔名 PINCH） | 32 | 512,568 | 全部排除 target |
| 兩正對點＋原橋外殼（額外控制） | 32 | 188,452 | 全部排除 target |
| 合計 | 64 | 701,020 | 全部排除 target |

這些是有限外側與抽象支援矩形的數量，不是來源圖數，不是枚舉內點的階數。
所有矩形經 Kempe 收縮後的外框聯集只出現 `0,165,424,429`。
它們均不含 bit 9 的 `01232`，而 933、941 都必須接受該原列。
這給出共同的缺失接受列矛盾。

主程式與獨立 verifier 的 64 cases、完整矩形、所有外側矩陣和著色數完全一致。
外側完整 literal lifts 另由獨立程式保存；共 59,156 份，按具名 query 計數、含重複 collar。
同側有隱藏多少原頂點並未列入外側；它们始終留在未知 L_±。

7 個實際 planar C6 disk 正控制（cycle、wheel、兩種三角化、兩種單 chord、stacked fan）
都保留其全部真實支援。8 個負控制在同一獨立 validator 下被拒絕：
外框 mask 破損、遺漏矩形、錯誤支援收縮、偽造 target coverage、原界面改序、
刪原 bridge、拆共享 x、改 full-lift count。

正常與 PYTHONHASHSEED=17 的 8 份主結果、8 份獨立結果、8 份 full-lift gzip 均逐 byte 相同。

## 9. 程式與重播

Python 3.10+，僅標準庫。建議先複製到獨立目錄再重播，因 producer 會重寫本地結果。

```
python3 twohole_fast.py
python3 independent_verify.py
python3 negative_controls.py
```

也可分組：

```
python3 twohole_fast.py PINCH 2
python3 independent_verify.py PINCH 2
```

主程式從 `probe.py`／`twohole_probe.py` 建圖與 literal DFS，從 `kempe_probe.py` 取得規則。
獨立 `independent_verify.py` 不 import producer：
- 用原三角 fan 的面列表重建 annulus；填入兩個 dummy caps 後核對 Euler、edge incidence、vertex links；
- 用固定原點順序 DFS 重算全部外側 literal lifts，而不是主程式的動態最小 domain DFS；
- 用 set-block 遞迴與圓周 gap 判準重建非交叉分割，用 BFS 生成交换軌道；
- 用轉置相容矩陣的交集族獨立枚舉矩形，並用同步刪除重算 κ。

JSON `rectangles` 每列為 `[A,B,kappa(A),kappa(B),possible,missing]`；
前四個整数是 31-bit C6 支援集合，後兩個是原 B 的 10-bit masks。
每個檔案保存完整 row 順序。zero output pairs 不得省略其語義。

## 10. 保留的探索過程與嚴格界線

第一輪只固定一個零單接 W5 端、把另一側整體吸收入固定 C6 切口：
128 配置的純安全聯集排除 122，剩餘 6 個加 C6 Kempe 條件後也排除。
這是過渡結果；後來的雙片切口已不需固定任何 W5。

`pair_prune.py`／`pair_prune_results.json` 保留一個未成功的較弱放寬：
只逐 pair 做兩側 Kempe 刪除，64 cases 全部仍覆蓋 target。
因此有效排除依賴整份 R_+×R_- 的共同限制，不能把不同 pair 的成功拼成同一解。

本包沒有新增 Lean theorem、没有重跑原上游全部 checker、沒有驗證任意 RING、
沒有改變 repository 現況。正式採納仍需獨立審查 source-to-cut 覆蓋、核對凍結來源
身份及按專案流程重播／發布。審查前應稱為「廣化候選＋完整有限核對」，
而非已更新主定理或已關閉整條 h=3 研究線。
