# 共同 exterior gadget 的 pocket 化約：獨立紙面覆核

2026-10-13。只寫本隔離包。覆核 frozen 的
[前輪證明](../frozen/audits/2026-10-13-c8-joint-gadgets-6943561/theory/PROOF.md)、
[前輪報告](../frozen/audits/2026-10-13-c8-joint-gadgets-6943561/REPORT.md)、
[相對 C4 報告](../frozen/audits/2026-10-13-c5-no4ct-degrees-6cafdfb/REPORT.md)
及其 [完整 C4 證書](../frozen/audits/2026-10-13-c5-no4ct-degrees-6cafdfb/C4_CERTIFICATE.json.gz)。
本覆核沒有重證來源最小性、132 目錄或 plantri 生成完備性。

## 1. 精確適用域

原 H 保持全部原邊及具名 induced C8，原總點數為 k，沿 frozen 契約有
`k≥19`，且至多 `k+5` 點的 loopless planar 圖可四色。
所有新增限制在原 C8 的同一空側 disk 同時畫入；不得操作 H 的其他點。
等式 scaffold 的 connected components 全部共同收縮，原 C8 pins 的像
給 independent noncrossing partition π。合法性必須以完整 Diff 圖核對：
任何原邊或新增 Diff 邊兩端不可落在同一 equality component。

記 d 為原 C8 pins 的識別淨省數，a 為收縮後不屬於原 C8 pin images 的
新頂點數。本文高點域為 `a∈{6,7,8}`、`a−d≤5`；frozen 預算給 `d≤3`。
不把 scaffold 中將被收縮的 Steiner 點算成 a；私人 equality component
若不含原 pin，其收縮像仍是一個新點，必須計入 a。

下述紙面化約對既有實際 scaffold 的收縮商圖操作，不先把它任意換成
另一套 chord fans。任意換樹可能撞上其實際附件；這不是合法的 isotopy。
§3 的替代是保完整 quotient 圖及原 pin map 的重新構造，理由另列。

## 2. C8 商圖是保留 digons 的 plane cactus

對 boundary-only noncrossing chord forest，逐條收縮 chord：第一條把一個
boundary cycle 分成兩個在收縮像共用一點的 cycles；剩餘 chords 位於
某一側的實際 disk。遞迴套用相同操作，每次只把一個現存 cycle 分成
兩個。forest 保證不收縮已經相同的端點，independence 保證不把原環邊
變成 loop。因此原 C8 邊的商圖是 cactus multigraph，每条原邊恰屬一個
cycle。兩條平行原環邊形成的 C2 必须保留，不能先簡化掉其幾何口袋。

Steiner scaffold 也給相同結論。先只看其原 boundary pin partition；
它由互不相交的 connected scaffolds 實現，故 noncrossing。以每個 block
的 boundary chord tree 得到同一 C8/π。這裡只是在證明商環的結構，尚未
把帶附件的原 scaffold 直接換掉。商環的 cyclic block orders 與原 C8
boundary word 都固定；它的 H 側 distinguished face 也保持。

商環共有 d+1 個 cycle pockets，各長至少二，長度總和八。所有可能性為：

| d | 原 C8 邊分配的 pocket 長度 |
| ---: | --- |
| 1 | (2,6)、(3,5)、(4,4) |
| 2 | (2,2,4)、(2,3,3) |
| 3 | (2,2,2,2) |

此表列長度 multiset，沒有丟棄具名環序、同一 original pin map 或不同
pockets 在 cutvertex 的共同顏色。完整關係是各 pocket 在同一 row 下
的 conjunction，不是它們各自另選一份成功列。

## 3. 從任意合法 exterior scaffold 回到 signed C8 圖

**重構引理。** 收縮原 exterior equality scaffold 後，令 K=C8/π。
所有剩餘 exterior vertices/edges 都位於 K 的非 H 側 faces；每個嚴格
私人點屬唯一 pocket，各 pocket 只在 K 的 boundary images 相交。
這來自原全圖的實際 embedding：收縮只在空側操作，並未使任何 exterior
邊穿過原 C8 或進入 H 側 face。

選另一套 boundary-only chord forest T 實現同一 π。K 的 pocket cycle
順序由原 C8 image word 固定；把每個原 quotient pocket 圖按同一具名
cycle 插入 T 對應的面。每個 quotient boundary image 在該面的原邊界
上是被 T 連起的一段 boundary path；把這個 image 展開成該 path，將
pocket 的內側 incident edges 接到該段的一個 pin，並保留原環邊於兩端。
局部只需在該面角內展開，沒有跨面接線。將 T 再收縮後，得到原本的
quotient pocket 圖，原 C8 到 K 的命名映射完全相同。

因此這個重新構造保留原 literal C8 rows 的完整 pullback relation。
它沒有宣稱原未收縮 scaffold 的 edge drawing 可由一次 isotopy 移到 T，
也沒有移動 H 的原附件。若同 block 的 exterior 邊改接另一 pin，其
商圖端點與原 pin map 必須明列；這由 block 常值保證關係相等。

若原 equality scaffold 有冗餘 cycles，先取每個 connected component
的 spanning tree：等色約束沒有改變，Diff 邊保持，原 embedding 仍合法。
接著共同收縮。沒有 original boundary pin 的 equality component，其
商點是普通私人點；含單一 original pin 的樹只增添該 pin 的 exterior
附件。這些情形均不新增 C8 識別，並沿相同 pocket 構造處理。

**same-point completion。** 重構後的 signed C8 disk 在同一頂點集增廣
成 simple 內面三角化，保留其全部現有 underlying edges 及 rotation。
新加 boundary chord 若兩端在同一 π block，標 Eq；其餘新邊標 Diff。
如此沒有新增 Diff loop。新 Eq 是原等式的推論，新 Diff 只收緊關係：

`Σ_completed ⊆ Σ_reconstructed`。

故任何拒絕 U 的重構圖，也給一份拒絕 U 的已三角化 signed 圖。
當其私人點數至多五，即落入 frozen 完整 signed h≤5 測試域。
**這一步採用前輪已測域無排除，必須保留 plantri 完備性依賴。**
重構引理及完成時的符號選擇本身是紙面 topology／monotonicity 證明。

## 4. Pocket 替代的量詞與預算

C2 的 proper boundary 指派、C3 的 proper boundary 指派各只有一個 S4
軌道。每份實際 pocket 圖的點數至多 `a+3≤11≤k+5`，故相對可染性先
給一份完整染色；共同換色到任意固定 proper boundary row 即給其延伸。
因此可刪掉 C2/C3 pocket 的全部私人點，保留完整 boundary relation。
這不表示舊 fibres 數量相等。

每個 C4 pocket 的私人數 s≤8<k，故相對 C4 引理給七個 masks
`7,10,11,12,13,14,15`。採 frozen 的 row 順序
`0101,0102,0121,0123`：四輪 W4 的 relation 為7，對角線 1–3 的 relation
為10，對角線 0–2 的 relation 為12。七個 masks 各含至少一份 7、10、12。
故每份 C4 pocket 可用**至多一私人點、完整關係包含於原 relation**的
合法 disk 替代。這是拒絕 U 足夠的單向縮減，不是完整 relation 相等。

C5 pocket 的私人數 s≤8<k，其完整關係由全域 C5 最小性落入132目錄，
可用至多五私人點的具名 witness 取代；此處是完整 relation 相等。
不同 pocket 的私人名字取互不相交，全部邊界仍用同一 row 的顏色。

| pocket 型 | 替代後私人點上界 | 判定 |
| --- | ---: | --- |
| d=1，(3,5) | 5 | 已測 signed 域 |
| d=1，(4,4) | 2 | 已測 signed 域 |
| d=2，(2,2,4) | 1 | 已測 signed 域 |
| d=2，(2,3,3) | 0 | 已測 signed 域 |
| d=3，(2,2,2,2) | 0 | 已測 signed 域 |
| d=1，(2,6) | C6 的私人點數 | 至多五即已測；六點仍需處理 |

由 `a−d≤5`，a=7 必有 d≥2，a=8 必有 d=3。所以上述高點域中，
真正未被本次 pocket 縮減回既有 signed 域的只有 d=1、a=6、(2,6)，
而且六個私人點全部在 C6 pocket；C2 上若有私人點，刪去後 C6 至多五點。

這是方法域的縮窄，不是來源存在、主命題、八份 U 或同圖計數錐的排除。

## 5. 殘留六私人 C6 的低度縮減：接受

令 P 是上述 C6 pocket 的 simple Diff 圖，恰有六私人點；平行 Diff 邊
先只就 colouring 簡化，原 C6 cycle 保留。所有度數指不同鄰點數。

若私人 v 度數至多三，刪 v 保持完整 boundary relation；P−v 五私人點，
與原短 C2 等式 pocket 合起來後，已屬 §3 的 signed h≤5 域。

若私人 v 度數四，四鄰不能形成 K4，否則連 v 是 K5。取其中一對沒有
Diff 邊的鄰點，在刪 v 露出的實際面內加弧並收縮。四鄰若來自已三角化
的 link C4，可取合法 opposite pair；一般未三角化圖只須取任一非邊對，
不要求稱它們相對。單一弧在该露出面內可畫，不另引入 simultaneous
cofacial 假設。

每份 quotient 染色拉回到 P−v 後，四鄰至多三色，所以能接回 v：

`Σ_Q ⊆ Σ_P`。

因此 P 若拒絕某個原 U，同一 pin map 拉回的 Q 也拒絕該 U。
這裡只需一支的完整 lift 提升；沒有宣稱單支 counts 等於 P 的 counts，
也沒有使用兩支各自的成功 rows 拼染色。

三種合法非邊收縮的準確私人點數為：

| pair 的類型 | 剩餘新點 | 原 boundary 識別 |
| --- | ---: | --- |
| 私人／私人 | 4 | d=1 不變 |
| 私人／C6 boundary image | 4 | d=1 不變 |
| 兩個 C6 boundary images | 5 | d=2 |

前兩類由內側面弧的 contraction 得原 C6 disk。第三類使原 boundary
partition 多合一對；因該 pair 沒有 P 邊，特別不是 C6 相鄰點。
原 H 的 C8 induced，故其全部原 pin images 也沒有 H 邊被合成 loop。
新增弧位於實際 C6 pocket，與原短等式 scaffold 同側共同實現，故仍
noncrossing。若它接到舊 scaffold 內部角，可能產生 Steiner junction；
此時使用 §3 的 quotient pocket 重構，不能直接聲稱原弧已是 boundary
chord。三類均以同一 original C8 pin map 進入至多五新點的 signed 域。

**覆核結论。** 低度四縮減在上述明列域內成立，無需另作條件式保留。
故若存在未被既有測試排除的六私人 C6 直接拒絕 gadget，可先要求其每個
私人點在 simple P 中度數至少五。這沒有要求 H 的度數，也沒有刪掉
原 named boundary pin。原來源幾何、其他原面及其他 H 點的縮減仍未覆蓋。

## 6. 證據層與獨立 verifier 建議

本輪可以獨立覆核的有限內容是：274 原 literal C8 rows、全部合法 π、
cactus pockets 的具名 cycle order、七份 C4 masks 的 mini-relation inclusion、
每份重構 gadget 的原 pin map、私人名字以及全 row fibres。checker 應
直接從邊／映射重算 proper full assignments，不 import producer；正確
比較目標是完整 tuple sets 與零 cells，而不是只有正性或交集大小。

C4 單向替代、C2/C3 刪私點、C5 witness 替代可能改變 counts，應各自
保存原／新 fibres 並核對 relation inclusion 或 equality，不能宣稱其
完整 fibres 相等。若檢查 degree4 示例，須將 quotient 的每份完整 lift
按同一原 pin map 拉回，再保存至少一個可接回 v 的實際顏色；僅驗對角
equality 或兩份 masks 均非空不足夠。

有限 π、mini-cap 示例或負控制不證明任意實際 pocket／scaffold 的 topology；
該義務由 §§2–3 的紙面重構承担。既有 signed 完備域無排除仍依賴 frozen
plantri 與其逐圖／完整 fibres 證據。本覆核沒有新增 Lean、外部來源實現、
主命題 closure、commit 或 push。
