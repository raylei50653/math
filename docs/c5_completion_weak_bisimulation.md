# Fixed-C5 completion 與 generic weak-bisimulation bridge

2026-09-16。兩個缺口分開交付：**completion 是下述完整紙面拓撲證明；一般
weak-bisimulation 與 finite observable trace equality 已在 Lean 證明。**
既有 [k≤3 audit](c5_weak_deletion_audit.md) 的計算結果不變，也未重跑。

## 1. 精確圖類與 production 對齊

令 B 為具名有序環 `0–1–2–3–4–0`，V={0,…,4+k}。
抽象 cell 類 C_k 為有限簡單圖 G，V(G)=V、E(B)⊆E(G)，且存在一個
closed disk D 中的嵌入：B 恰為 ∂D，其他頂點在 int(D)，非外圈邊的開弧
在 int(D)，邊的內部互不相交且不含頂點。固定嵌入版本記作 (G,ι)；
completion 對**每個**這樣的 ι 成立，保留原頂點位置與原邊弧。
採通常有限 plane graph 的 tame drawing／rotation-system 語義；不另要求
連通、二連通、最小度數、induced boundary、三角化或非空 Σ。

這正使用 [cell 規格 §0.1–0.3](c5_cell_enumerator.md) 的頂點與 U(k)：
五條 chords、5k 條 spokes、所有內點對。孤立內點仍計入 k；catalogue 的
`k_eff` witness 壓縮不會刪除本定理的頂點。`boundaryIsCycle` 只要求外圈邊存在，
不禁止 chords。Σ 始終是 [Math/Boundary.lean](../Math/Boundary.lean) 的
`Sigma G B`，即既有 `Color`、`Proper`、`BoundaryColoring` 的完整具名關係。

production 的 `_setup`／`_dfs` 在 G 外另加一個連向 B 五點的 apex a，測試
G+a 是否 planar。此條件與「存在上述 disk embedding」等價（紙面）：

- disk → apex：在外側 disk 放 a 與五條 spokes 即可。
- apex → disk：取 G+a 的球面嵌入，其中 wheel B+a 分成五個三角區域及
  一個不含 a 的 B-disk。G−B 的每個連通分量位於某個 wheel 面；在三角區域
  a,b_i,b_(i+1) 中的分量只能連向 b_i、b_(i+1)，因 G 中沒有連向 a 的邊。
  保留 B-disk 中的內容，把每個三角區域中的全部 G 內容移入 B-disk 內、
  緊貼對應 rim edge 的空 collar：將該三角 disk 壓入 collar，固定兩端，
  其 a 端移到 collar 內未使用的位置（a 不屬於搬移的圖）。有限 tame drawing
  有這種避開既有邊的 collar；端點處使用 rim edge 旁的空 sector。
  五個 collars 內部可互不相交。沒有 boundary chord 位於三角區域，因其僅
  含兩個相鄰 boundary vertices。無 attachment 的分量（含孤立點）也照搬。
  得到全圖在同一 B-disk 內。這步允許重新選擇抽象 cell 的嵌入；下面 completion
  一旦指定 ι 就不移動它。

所以沒有偷偷將 production 的 apex-planar cells 縮成原本已連通的子類。
單純抽象 planar、但沒有 apex 條件的 C5-containing graph 不在 C_k。

## 2. Completion theorem（紙面）

令 T_k 為 C_k 中具有指定外面 B、每個 bounded face 都是三角形的
simple plane graphs。對任意 k≥0 與任意 disk drawing (G,ι)∈C_k，存在
同一 disk 內延伸 ι 的 T∈T_k，使

\[
V(T)=V(G),\quad E(G)\subseteq E(T),\quad
F=E(T)\setminus E(G)\subseteq U(k),\quad G=T-F.
\]

這裡最後的等式連同頂點集與原圖 drawing 成立。外面仍是同一有序 C5；
不添加外部邊、頂點或外側 chord。

### 2.1 取極大增廣

在所有保留 ι、只在 int(D) 補簡單邊的合法 superdrawings 中，選邊數最大的
T。非空因 G 本身合法；可選因邊數是至多 binom(5+k,2) 的整數。
不需要假設 drawing 集合有限，也不需要預先假設面是 simple polygons。
以下任何合法新增邊都會違反這個最大性。

### 2.2 T 必連通（包括處理孤立點）

若不連通，有一個 bounded complementary region 的邊界接觸兩個不同
連通分量。具體理由：在 int(D) 選一條 general-position 弧，從非 B 分量
到 B 分量，避開頂點、橫切有限條邊；依序記錄遇到的分量，取首次改變
分量的相鄰兩次接觸。兩接觸間在同一 complementary region。沿其兩端
所接觸邊的同側，將端點推至該邊的頂點；對孤立點直接以該點為端點。
在這個連通開區域內取簡單弧，端點用小 sector 接回頂點，即得到不同
分量頂點 u,v 間的新邊。這也可用 regular neighbourhood 的邊界來作同樣的
detour；不穿越任何既有邊。外圈阻隔了無界區域，所以整條新增邊在 D 內。
u,v 不可能已有邊，且 u≠v，矛盾。

此步不把有洞的面當成 disk；只用同一開區域內的 arc connectivity。

### 2.3 T 沒有割點，因而沒有橋

假設 v 是割點。T−v 的每個分量都含 v 的某個鄰點。在 v 的循環 rotation
中，必有兩條連續邊 vu,vw，其鄰點屬於 T−v 的不同分量。沿 vu、vw 的
相鄰側，在 v 附近繞過 v，畫新邊 uw（取很窄的邊 collar 與空 sector）。
u≠w 且 uw 原本不存在，否則兩點屬於同一分量。

這個 sector 必可選在 D 內：若 v 是內點，所有 sectors 都在 D 內；若
v∈B，唯一外側 sector 夾在兩條 B 邊之間，其兩個鄰點由 B−v 的路徑連通，
屬同一分量，故上述「不同分量的連續邊」不會選到它。新增 uw 與外圈無涉，
再次矛盾。T 至少五點且連通，無割點即二連通；若有橋，至少一個端點會是
割點（只有兩點的例外不適用），故橋也被排除。

### 2.4 現在才使用 facial boundary 是 simple cycle

有限二連通 plane graph 的每個 facial boundary walk 都無重複頂點。
其標準 Jordan 論證如下：若某個面兩次經過 v，取該面的兩個不同 v-corners，
在面內以簡單弧相連，再經小鄰域接到 v，構成只在 v 接觸圖的 Jordan curve。
兩個不同 corners 把 v 的 incident darts 分成兩個非空區間，位於 curve
兩側；若 T−v 連通，兩側的鄰點間路徑必穿過此 curve，矛盾。
重複邊的兩側出現在同一 walk 對應橋，也已排除。簡單圖排除長度 1、2
的 facial cycles。由 Jordan–Schoenflies，bounded face 的閉包是此 simple
cycle 所界的 closed disk，內部沒有圖的任何部分。

這段是在二連通性證明**之後**使用；原始 G 的 facial walks 可以任意重複。

### 2.5 排除長度 ≥4 的 bounded face

設某 bounded facial cycle 長度 r≥4，沿其循環順序取四個連續不同頂點
 a,b,c,d。ac 與 bd 都不是該 cycle 的邊。若它們都已是 T 的邊，它們的
開弧均在此 face 的另一側（球面上該 closed disk 的補 disk），而端點在
邊界上交錯。Jordan separation 禁止補 disk 內兩條互不相交的交錯連接弧。
故至少一條不存在，例如 ac；可在空的 face disk 內加入 ac，保持簡單性與
原 drawing，違反最大性。所有 bounded faces 因而均為三角形。證畢。

這也處理「某一條候選 diagonal 已在別的面出現」的情況，不能隨意重複補邊。

### 2.6 Edge cases 與 Σ

| 情況 | 證明中的處理 |
| --- | --- |
| disconnected／isolated interior vertices | §2.2 保留頂點，以新邊連起分量 |
| cut vertices／bridges／repeated facial walks | §2.3–2.4 先消除，才談 polygon diagonal |
| boundary chords | 允許且保留；新增 chord 也只能走 disk 內 |
| boundary degree 2 | 不禁止；割點論證不會越過外側 sector |
| separating triangles | 保留，不要求每個三角環都是面；內側繼續增廣 |
| non-triangular bounded faces | §2.5 以交錯端點排除「兩 diagonal 都已存在」 |

補邊只保證 Σ(T)⊆Σ(G)，由 Proper T 的每個著色也是 Proper G 直接得到。
不要求 Σ(T)=Σ(G)。例如裸 C5 的 boundary coloring `01012` 在加入 chord 02
後不再合法。deletion-domain completeness 要的是 G=T−F，不是保 Σ 的 parent。

## 3. 與 plantri parent 類及具名 audit 的對齊

completion 的 T 二連通，外圈五點，bounded faces triangular；由 Euler 與
face-edge 計數得 |E(T)|=3k+7、|E(T)−E(B)|=3k+2，與既有 parent 規格一致。
內點度至少三：其 incident face sectors 都是三角形，若度為二，兩個 sectors
都須由同一鄰點對的同一條邊封口，使整圖只有該三角形，與外圈 C5 矛盾。

還須核對手冊的「2-cuts 只能是 outer chords」不是額外縮窄：在 T 外側
加 apex a 連向 B，得到 simple sphere triangulation Q。Q 三連通：每個
頂點的 link 是一個 cycle；先刪一點可沿 link 繞路，刪第二點時 link
至多缺一點仍連通，仍可繞路，故刪任意兩點後連通。若 {u,v} 分割 T，
Q−{u,v} 的連通性表示 T−{u,v} 每個分量都含剩餘 boundary vertex。
若 u,v 不全在 B，B−{u,v} 仍連通，矛盾；若它們是相鄰 boundary 點也同理。
最後若 uv 不是邊，u 的內側 link path（連接其兩個 boundary 鄰點，經過
所有鄰點）不含 v，仍可在 T−v 中將經 u 的路徑繞開，與二點割矛盾。
所以每個二點割都是 boundary chord 的端點。

[plantri 5.8 官方手冊](https://users.cecs.anu.edu.au/~bdm/plantri/plantri-guide.txt)
的 `-P` 節將輸出定義為 simple disk triangulations，指定 simple-cycle 外面；
`-P5` 固定長度五，`-c2 -m2` 允許 chords 與外圈二度點。不使用 `-x`、`-w`
或額外度數限制。因此與上述 T_k 相符。手冊聲明按嵌入同構類生成代表；
保存的 [manifest](../artifacts/c5_disk_deletions/plantri/manifest.json) 綁定
版本、來源 hash、命令與四份 raw outputs。**生成沒有漏圖仍是外部工具信任，
不是 Lean kernel 已認證的枚舉定理。**

### 3.1 重要：169,643 並不是所有具名 cells 的數量

parent 程式展開五個 boundary 起點與兩個方向，再只商內點置換。
因此 completion 給定的 T 一般只有某個 boundary-pointwise-fixing 置換 π(T)
在保存的母圖清單內，並非原標號 T 本身。D 記全部保存母圖的 raw deletion
states。則 π(G) 是 π(T) 的某個 retained mask，屬於 D 的圖像。

π 保持完整 Σ（內點賦色作雙射）、保持每條非外圈單刪步，且與任意有限
刪邊路徑交換，所以保持 silent paths、W 與 traces。同一 raw parent 的
mask 格已含該圖的全部後續刪邊；duplicate parents 不增加或減少圖層的 W。
因此任意 G,H∈⋃_{k≤3}C_k 可**各自**用固定 boundary 的內點置換送到 D，
用封存 audit 的 fiber equality，再拉回，得到 W(G)=W(H)。這沒有重命名
boundary，也沒有對兩側顏色作獨立重命名。具體邊名被隱藏至關重要。

若狀態還記錄固定 drawing，單刪與 Σ 仍只依底層圖；每個刪邊序列都可在
繼承 drawing 中執行，故同一推導適用。這不聲稱有限 raw outputs 列出
每種 disconnected embedding 的 component nesting 資料。

**升級後的有界結論：** 接受本篇紙面拓撲證明、plantri 對上述類別的生成
完備性，以及既有 Python audit／標號與 Σ encoding 的正確性，則對全部
k≤3 production C5 cells（且允許跨 k 比較），ker(Σ) 為本觀察語義下的
weak bisimulation，有限 observable traces 相等。

completion 的數學覆蓋缺口因此在紙面層封閉；整條有界結論仍非 Lean 全枚舉
定理。completion 對任意 k 成立，不代表任意 k 的 W fiber equality 成立。

## 4. Lean transition-system bridge

實作：[Math/WeakBisimulation.lean](../Math/WeakBisimulation.lean)。

- `Silent step obs x y`：step x y 且 obs x=obs y。
- `Visible`：step 且 observations 不等；不需要 observation 有偏序。
- `SilentStar`：mathlib `Relation.ReflTransGen Silent`，包含零步。
- `Exit`：τ*;visible；`WeakExits x` 是出口 target observations 的 Set。
  `silentStar_observation` 保證 prefix 保 observation，所以 visible 的不等條件
  等價於 target observation 不等於原始 source，與 audit 的 W 定義一致。
- `WeakVisible`：τ*;visible;τ*，用於標準 weak matching。
- `IsWeakBisimulation R`：R 對稱、保 observation，silent 與 visible steps
  分別可匹配，target 再落入 R。對稱性保證交換來源後也匹配；visible label
  是 target observation，silent suffix 不改該 label。

`kernel_isWeakBisimulation` 的唯一實質假設是

\[
\forall x,y,\quad obs(x)=obs(y)\Rightarrow WeakExits(x)=WeakExits(y).
\]

silent step 用另一側零步匹配；visible step 本身提供 source weak exit，
由假設在另一側找到 τ*;visible witness，suffix 選零步，兩 target 落回 kernel。
不需 finite、DAG、單調性或 termination；結論採 divergence-insensitive 語義。

`Trace` 直接由原始 steps 歸納定義：silent 不加 entry、visible 加 target
observation，任意有限時刻可停止。`ObservableTraces` 再加初始 observation，
正好是 A/B 報告的相鄰重複壓縮序列；允許不相鄰 observation 再次出現。
`IsWeakBisimulation.observableTraces_eq` 對**任意**本定義的 weak bisimulation
證明 trace equality，並非以 trace equality 定義 bisimulation。
`kernel_observableTraces_eq` 才套用 fiber equality 的 bridge。

`FiveBoundary.sigma_kernel_isWeakBisimulation` 直接使用既有 `Sigma`，允許 state
決定不同頂點數，因此可以跨 k。它仍要求 hW；沒有將 Python 結果偷偷設為 axiom。
`boundaryIsCycle`／disk 合法性屬於應用時的 state domain，不是一般 bridge 必需假設。

domain closure：Lean 的 step 是 S→S→Prop，所有 witness 都在 S。
若用 subset D 的 subtype 當 S，得到的是 restricted transitions 的結論；
要對原圖的**全部**刪邊下結論，另須證明 D 對這些 steps 封閉。
本應用 raw mask 格對單刪封閉，而 C_k 刪非外圈邊可繼承 drawing，也封閉。

## 5. 信任鏈、尚缺的 formal primitives 與停止點

| 環節 | 現況 |
| --- | --- |
| apex-planarity ↔ 存在固定 B disk drawing | §1 紙面 collar／wheel 論證，未 Lean 化 |
| 每個固定 drawing 同頂點 completion | §2 完整紙面證明，未 Lean 化 |
| parent 類與 plantri flags 一致 | §3 紙面推導＋官方手冊；generator 外部信任 |
| arbitrary cell → 保存母圖的 descendant（up to interior labels） | §3.1 紙面等變與 closure 論證 |
| k≤3 fiberwise W equality | 封存 Python 有限計算，1,246,132 raw states；未轉成 Lean certificate |
| fiber equality → weak bisimulation → finite traces | 本次 Lean kernel theorem，假設式 |

未 formalize 的 topology primitives 精確為：有限 plane drawing 的 regular
neighbourhood／empty sectors 與 collars；同一 complementary region 中的
端點可達簡單弧；cutvertex 的 rotation-sector 增廣；二連通 plane graph 的
facial-walk simplicity；Jordan–Schoenflies 與 disk 中交錯端點弧必交；
wheel-face 搬移與固定端點 collar extension。Euler／link rerouting 的嵌入
定理亦在紙面層。`Math/LocalClosure.lean` 沒有提供這些 embedding assertions。
沒有為補這個缺口新增 Lean topology axiom 或帶 `sorry` 的假定定理。

審核入口：[Math/WeakBisimulationAudit.lean](../Math/WeakBisimulationAudit.lean)；
保存輸出：[lean-audit.txt](../artifacts/weak_bisimulation/lean-audit.txt)。
它列出新模組全部 theorem 的 axiom dependencies；允許 Lean 標準
`propext`、`Classical.choice`、`Quot.sound`，不允許 `sorryAx` 或新增 unsafe trust。

```bash
lake build
lake env lean Math/WeakBisimulationAudit.lean
lake env lean Math/Audit.lean
git diff --check
```

本次另檢查修改 Markdown 的本地文件連結。未修改任何 checker、封存計算證書、
132-state catalogue 或 production semantics；未跑 k=4、未重跑 k≤3 audit，
未研究一般 weak deletion congruence 或 K∞=K≤5。

驗證結果：`lake build` 通過（8,820 jobs；新模組無 lint 警告，只有既有模組的 lint）。
新 audit 的 8 個 theorem 全部通過；核心 bisimulation bridge、Σ specialization
與 trace transfer 均不依賴任何 axiom，兩個 trace-set equality theorem 僅依賴
`propext`、`Quot.sound`，沒有 `sorryAx`、native-decide 或 unsafe trust。
[既有公開定理 audit 輸出](../artifacts/weak_bisimulation/public-audit.txt) 與
[封存 baseline](../artifacts/boundary/lean-audit.txt) 逐 byte 相同；其中原有
native-decide trust 沒有增減。修改文件的本地連結與新舊檔案 whitespace 均通過。
