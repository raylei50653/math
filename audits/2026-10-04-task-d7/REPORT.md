# D₇：E2 的 ε≤1 層獨立稽核

2026-10-04；Repo `/home/ray/developer/ai/math`；分支
`shield-budget-hub-principle`；起始 HEAD
`ca3870f9b79684c2100480d0dc04523899666928`。被稽核物以未提交的工作區 bytes 為準。
只新增本目錄檔案，未修改被稽核物、導覽、STATUS、README，未 commit／push。

**總判定：最終論證的 (a)、(b) 確認；交付產物另有一項有缺口。**
本次未找到推翻 ε≤1 結論的反例，亦未找到 §3.3、§5.2–5.4 最終證明的
前提偷換。確認的範圍是 E2 §1 明列的 induced-C₅ disk、T4 全收、
Σ-edge-minimal、忽略孤立內點的來源，以及所引用的全 degree-4 分類／transfer
證據層。沒有把五個 checker 通過當作任意大小證明。

產物缺口位於舊 `interior_bridges_and_sidebranches.json` 及其生成器：
它們仍宣稱長 W 只有一份 pendant 並據此結案。E2 正文已用 final terminal-block
層取代這段，但舊機器欄位沒有標示其結案論述已失效。此缺口可補，且不推翻
已補妥的最終 §5.2；詳見 §7。沒有將未重跑的歷史大枚舉或 Lean 寫成通過。

## 1. 快照、範圍與交付

起始先保存 [sha256_before.json](sha256_before.json)：3,559 份當時 Git
tracked／nonignored untracked 檔案；另以
[audited_sha256_before.json](audited_sha256_before.json) 明列 20 份直接稽核物
及共同前提／控制輸入，包括 E2 報告、五個 scripts、其全部對應 artifacts、
盾弧與 DOCUMENTATION、cells、E1 observations。起始狀態見
[git_status_before.txt](git_status_before.txt)。結束核對見
[sha256_after.json](sha256_after.json) 與 [verification.json](verification.json)。

結束時上述20份直接稽核物**零漂移**，HEAD亦未變；其餘已封存非D₆檔案也未變。
同一工作區的D₆任務在此期間新增48份檔案，並改變其自己的`sha256_before.json`，
完整差異逐份保存。這些是本次工具未寫入的D₆路徑；因此不宣稱整個共享工作區
零漂移，僅宣稱被稽核物未漂移。本次新增檔案全在D₇目錄。

三份歷史 runtime JSON 被 Git ignore，不在起始全工作區 manifest；後來補記於
[direct_runtime_input_hashes.json](direct_runtime_input_hashes.json)。它們目前的 SHA
分別與起始已封存的 E2 JSON 所內嵌 `source_sha256`／`input_sha256` 完全相同。
這是補充的來源一致性核對，不冒稱曾對這三份檔案做獨立的起始讀取。
直接被稽核物的開始／結束 SHA 則逐份直接計算。

| 交付 | 用途 |
| --- | --- |
| [independent_check.py](independent_check.py)、[independent_results.json](independent_results.json) | 標準庫獨立重建 252 形式、十列完整染色、四份原 K₅、656 刪邊及兩張 E1 控制；不 import 任一 repo checker |
| [one_spoke_check.py](one_spoke_check.py)、[one_spoke_results.json](one_spoke_results.json) | 獨立重算 102→30→54、36／14／4 分層、盾弧支援、96 palette 行、12 K₅ 骨架 |
| [cycle_core_crosscheck.py](cycle_core_crosscheck.py)、[結果](cycle_core_crosscheck.json) | 獨立重算 first-cycle 入口、contact signatures、20 T4 反證，核對 18 endpoint bases 與原 K₅ 邊 |
| [source_scope_notes.md](source_scope_notes.md) | §3.3 逐格原文、來源前提及 §2–4 快速複核 |
| [one_spoke_notes.md](one_spoke_notes.md) | §5.2 的 D 歸納、精確 rooted queries、任意 W 集合盾弧與末端 blocks |
| [cycle_core_notes.md](cycle_core_notes.md) | §5.1、§5.3、§5.4 逐步紙面重推及原引用前提 |
| [replays.json](replays.json) | 五個 E2 checker 的普通／seed-17 十條實際命令、exit code、stdout／stderr |

本文 E2 行號均指本次封存的
[原 REPORT](../../artifacts/c5_excess_one_e2/REPORT.md)，沒有改寫原文。

## 2. 證據分層與快速複核

| 層 | 本次核對與限制 |
| --- | --- |
| 紙面 | 自行重推 degree≥4、H 連通、ε=0 飽和、ε=1 原 incidence 省略、來源分支、first-cycle、carrier 歸納、W 盾弧及原圖 minors |
| 外部定理 | 本次打開 [Dvořák 的原講義](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)：Lemma 7 要 connected degree-list assignment；Theorem 10 同前提給 Gallai tree／blockwise-uniform 拒絕刻畫。沒有特定 Σ 或 T4 前提，適用於 E2 的同一原分量拒絕 lists |
| 沿用歷史合成 | 全 degree-4 原圖分類、18 endpoint bases 及保原首點／contacts 的 all-row transfer：打開原文核對證明和前提，未重跑其大枚舉。新有限末端不取代這些無界化約 |
| Python 有限域 | 本次獨立的字面色表、必要接口、252 個形式、完整關係、witnesses、原邊 minors 與兩份指定 E1 圖；沒有新一般來源枚舉，沒有四色定理或 planarity 搜尋 oracle |
| Lean | 未新增 theorem，未執行 lake build；本報告不是 Lean 證明，也不是 native_decide 證書 |

**快速複核：確認。** E2:47–75 的 H 連通證明有效：每個有效內分量必拒絕
某 singleton，否則其邊不是 Σ-critical；未接框點改色迫支援至少四點。
兩個四點支援可各取交錯端點，原內路徑互斥，違反 disk 分離。
E2:82–95 的 ε=0 飽和也有效：core 中 degree≥4，原圖 degree=4，故任何
core 頂點保留全部原 incident 邊；沿連通 H 傳播得 M_q=G。全 degree-4
單缺失分類的 T4／minimal-q／disk 前提相符，得到 |Q|≤1。

E2:189–194 的原 K₃,₃ 九條鄰接有效：左 `{a},{b},{r}`，右
`{x},{y},B−{a,b}`；最後是原三框點 path。六條到 x／y 的原邊加
a、b 的補框弧邊及 r 的原 spoke，恰九條。E2 §5.1 的 palette 表也自行重算，
四個 actual pairs 12／14／23／34 的 joint signatures 各不相同。

## 3. 稽核項 1：§3.3 逐格來源前提

**判定：逐格確認。** 這張表只在 G 自己是所選 q 的 minimal core 時使用。
minimal-q 迫 root spokes 的 q 色互異，各分量禁色覆蓋可用 root 色，
各有 private color。這些推導用完整原 relation，不用分量 marginals。

| t／容量分拆 | 原引用及核對位置 | 判定／重新推導的關鍵 |
| --- | --- | --- |
| 0／(5) | `c5_no_spoke_exterior.md:44–49,128–176` | 確認。正文只有 minimal-q、連通 H、degree(5,4,…)、disk，不需 T4。四份 root 拒絕 palettes 的 signed incidence forest 迫 contact 數為偶數，不能為五 |
| 0／(4,1) | 同檔 `79–126,180–218`；`c5_single_spoke_four.md:73–189` | 確認。private-color 覆蓋給三禁色＋單禁色；另一原分量給避開 C₄ 的 r–B 外路徑，兩原 triangles／tethers 產生 K₅ |
| 0／(3,2) | `c5_no_spoke_exterior.md:180–205,226` | 確認。三接點至少禁兩色便足夠，不必恰禁兩色；三葉 active forest 迫 triangle 加三臂，原 tethers 與外路徑給 K₅ |
| 0／(3,1,1) | 同檔 `180–205,227` | 確認。同上三接點至少禁兩色；另亦違反共同盾弧至多兩分量 |
| 0／(2,2,1)、(2,1,1,1)、(1⁵) | E2:114–122,145–146 | 確認。每份原 unary 非空禁色 witness、外路徑及 degree-4 迫盾長≥2，三份至少六盾邊，與五框邊矛盾 |
| 1／(4) | `c5_single_spoke_four.md:22–39,48–189` | 確認。原文明示不需 T4／第二列；四 contact active forest 恰兩個 triangle 加 bridge，三 tethers 加原 spoke 給 K₅ |
| 1／(3,1) | `c5_single_spoke_three_one.md:22–44,47–150` | 確認。原文亦不需第二列；三葉 active forest、原 tethers、原 spoke 給 K₅ |
| 1／(2,1,1)、(1⁴) | E2:137,145–146 | 確認。原分量至少三，盾弧排除 |
| 1／(2,2) | E2:137 | 確認為剩餘分支；全部四容量整數分拆已涵蓋，排除責任在 §5.2 |
| 2／(3) | `c5_two_spoke_three_contacts.md:28–37,44–159,180–183` | 確認。開頭先寫相鄰 spokes，但 §5 逐步將原三臂／tether K₅ 證明擴張到任意兩條異色 spokes；沒有使用相鄰性、固定 Σ 或第二缺失列 |
| 2／(1,1,1) | E2:138 | 確認。僅兩個可用 root 色，三份各需不同 private color 不可能 |
| 2／(2,1) | E2:138 | 確認為唯一剩餘分支；排除責任在 §5.3 |
| 3／(1,1) | E2:139 | 確認。三異色 spokes 只留一色，不能供兩份不同 private color |
| 3／(2) | E2:139；`c5_degree5_sectors.md:31–70` | 確認為剩餘分支；原區域定位只需 T4／minimal-q，排除責任在 §5.1 |
| t≥4 | E2:141–143 | 確認。可選 proper T4 使任選四 spoke 端點四色互異，root 無色 |

上述直接來源排除本來就沒有 Σ=933／941 或「恰缺兩列」條件。
盾弧 theorem A 的原陳述確有固定 Σ；此處是**重用其證明**，由 E2 §2 自證
H 連通、degree≥4、全框被碰，以及 critical witness／外路徑補足實際所需前提。
沒有把固定 Σ theorem 直接宣稱成無條件 theorem。
逐格 signed forest／minor 的詳細重推見 [來源筆記](source_scope_notes.md)。

省略 spoke 所需的 592／1,194 all-row transfer 也核對：
`c5_941_two_spoke.md:60–134`、`c5_941_three_spoke.md:66–98`
雖然報告頁首談 941，transfer 的證明只讀全 degree-4 原 core、actual
attachments、proper row、parent 色及同一 ordered joint，沒有讀 941 的拒絕角色。
E2 的省略 core 滿足這些條件；接回 spoke 只過濾原 joint 的 r≠b(e)。

## 4. 稽核項 2：§5.1 B′ 與任意數內部 cycles

**判定：確認。** E2:249–264。先排末端 nonbridge blocks，使 block-cut tree
只有兩個末端 bridge、leaf 恰為兩 contacts，故它是一條鏈。若鏈含任何數量
odd cycles，從 contact 出發取第一個 J；入口前只有 ordinary bridges，
joint palette 只能在 A∪{(D,D)}，其中
`A={(2,0),(0,0),(2,1),(0,1)}`。

兩 contacts 已被末端 leaves 使用，所以 J 的入口 cutpoint 不是 contact。
它在 C 內 degree=3，完整 degree=4，恰接一個框點 k；J 的 private 點
定出同一 actual pair ij。两列 palette 包含性迫 k∈{i,j}，入橋的色對等於
另一端框點的兩列色，落在 `B′={(1,1),(0,2),(1,0),(2,2)}`。
B′ 與 A∪{(3,3)} 不交。第一次遇到 cycle 即矛盾，因此涵蓋任意 cycle 數，
不是靠 L4／L6 或有限長度控制。獨立色表核對八份入口。

## 5. 稽核項 3：§5.2 一-spoke (2,2)

| 子項 | 判定 | 核對／重推 |
| --- | --- | --- |
| 通用 102 records 前提 | 確認 | E2:274–279；`c5_single_spoke_residual_locality.md:31–55,134–151` 明列一般 T4／minimal-q、連通 H、唯一完整 degree-5、一 spoke、兩原 binary、disk。§4 的恰缺兩列 exit 另有額外前提，本次沒有使用它 |
| 102→30→54 | 確認 | 獨立從原 102 身份重算 51＋51，連續 actual support、盾邊互斥、spoke 避盾內點剩 30；所有遠列以整圖 D₅／S₄ 搬運及原因子身份匹配得到 54，逐份與原 ledger 相等 |
| 首橋 36 | 確認 | 對每份 residual 支援及原首橋重算；60 個三框弧分割上，36 份的每種必要局部配置皆無支援或含原 K₅，餘 18。五袋從原 W、原 contact-cycle 餘段及原外路徑構造 |
| carrier 14 | 確認 | E2:304–320；D 歸納與精確 rooted 延拓查詢成立，詳見下文。所有 carrier bridge 的支援／原 K₅ 交叉核對排 14，餘 IDs 82／317／477／817 |
| 最後四份 W_j 的引理 1／2 | 確認 | E2:331–338。W_j 原集合連通，H−W_j 經 r／另一 contact／其餘 path 連通；全 G 碰齊 B。引理的面證明只讀這三項，未讀「P 必是 H−r 的整份分量」或固定 Σ |
| 最後四份 terminal blocks | 確認 | E2:340–365。短 W 的旁支由原 critical witness＋短支援 hub 排除；長 W 用任意 rooted block tree 的 terminal block，沒有假設只有一份 pendant。96 joint palette 行及 12 原邊 K₅ 骨架獨立核對 |

**carrier 歸納的實際理由。** pair 列的兩 contacts 間是一條奇數長原 bridge path。
所有 off-path 非根點都不是原 r-contact，两列外部 lists 都含 D。對每個 rooted
block，先由末端扣掉後代 palettes；block palette 等於某個非根點的餘 list。
原 list 的 D membership 相同、後代 membership 由歸納相同、incident palettes
不交，所以該 block palette 的 D membership 相同。逐層扣到 path 根，另一列
residual 仍含 D。這不是整份 binary 的 unary 守恆，也沒假設非 D 色沿 path 不變。

rooted bridge／odd cycle 的 parent 色可延拓，恰當且僅當它不在該 block palette；
前者是 singleton 禁色，後者是兩色 odd-cycle 禁色。葉向根接回所有原子樹，得精確
rooted query。第二列首末橋為 D、橋 palettes 交替；若所有偶橋都為 c，則 residual
全部 {c,D}，原奇數長 path 在 root=c 或 D 都拒絕，與 singleton 禁色 c 矛盾。
故存在原偶橋 palette d∉{c,D}，兩端 residual {d,D}，同一原橋的支援／K₅ 才能排 14。

**W 集合的盾弧實際理由。** 刪去 bridge path 邊得到 W_j；補集經左右 path 段
及 r 相連。引理 1 的開面版本允許不同 W 共享框頂點，仍禁止共享盾邊。
引理 2 只多用全框被碰：未被 W 接的盾弧內點必由補集接，與 1(c) 矛盾。
四份的每個 W 都見同一必要框點，互斥 incident 盾邊迫最多兩 W；奇數 path
因此只有一條橋。保留整份原 binary 支援後，只可能 01＋123 或 01＋034。
長 W 的末端 odd-cycle 私有點在 partner 列只能接同一 actual adjacent pair；
兩個相鄰私有點與框對／連通餘袋給原 K₅。最後長 W 只剩 contact，兩條內邊
加兩框附件不能承擔三點 actual support，四份排完。

102 表此前 pair／pair 型的來源排除屬沿用歷史證據；本次打開相應原文核對
general minimal-q 範圍，未重新生成其 278 份大表。獨立小 checker 是對這份
必要接口及後續轉移的交叉核對，不能單独證明任意大小 interface 完備性。

## 6. 稽核項 4、5：§5.3 與 §5.4

### §5.3 兩-spoke (2,1)

| 子項 | 判定 | 重推要點 |
| --- | --- | --- |
| 必要區域定理 | 確認 | `c5_degree5_two_spoke_sectors.md:46–79` 只需 T4／minimal-q、連通 H、degree(5,4,…)、disk、兩 spokes。split-support 的 singleton-only 來源定理不要求恰缺兩列；nonadjacent §7 明確另分較窄 exit 接合 |
| 四容量型窮盡 | 確認 | spokes14 在兩列都禁1／2；两份各需 private color，故禁色是互異 singleton 0／D。短 J 的全部 actual support 在014，两列逐點相同，完整 relation 相同，角色不換；容量2／1與角色0／D兩個二元選擇恰四型 |
| r=0 contact signatures | 確認 | contact private-cycle 外鄰只能 {r,b1}／{r,b4}，joint palettes 為 ({2,D},{2,D})／({1,D},{1,D})；四個 noncontact signatures 為 ({2,D},{0,D})、({0,D},{0,D})、({2,D},{1,D})、({0,D},{1,D})，逐項不同 |
| 任意長原 path K₅ | 確認 | terminal-block 排除＋first-cycle 入口使 binary L 是原 path。r=D 的 A 橋兩端 actual pair 相同；r=0 首末 D，兩點 path 違反全框，較長 path 必含兩 noncontact 端點的 A 橋。相鄰 pair 用原 r–J–b0 外路徑連補框弧；pair14 用全框接觸連 b2、b3，原五袋十鄰接成立 |

兩個遠列朝向的反射 `i↦3−i` 搬整張圖、兩分量、contacts、attachments、tuple
座標與 boundary rows；每份 row 可作一次整圖 S₄ 換色，沒有逐分量正規化。

### §5.4 有真子核心

| 子項 | 判定 | 重推要點 |
| --- | --- | --- |
| 全單容量 20 T4 | 確認 | 五 root incidences、至多兩原分量、t≤3 迫三 spokes＋兩 unary。盾弧支援012／234、spokes024；四個非rainbow singleton rows 各有唯一可能禁 D 的 unary。capacity1 迫它見全三已用色；支援上的整份 S₄ covariance 搬到 T4，仍禁 root 唯一可用色。五旋轉×四列的20反證獨立重算 |
| binary 的共同 D₅／S₄ | 確認 | K=G−U 碰 B−h，U shield 內點不被 K 碰，迫 U 的盾長2；C340 以整圖反射 i↦2−i 送到C234，U012保留，再將整圖色名0／2交換還原q=01202，兩個遠singleton位置也一起交換 |
| 剩餘 spokes04 | 確認 | 可用端點024；24在q重色不足覆蓋四色，02在遠列重色落入省略spoke分支；只餘04。singleton3遠列的U只見01，capacity1不能禁未見2／D；singleton4遠列同理不能禁D，故只須binary允許root D |
| unattached-singleton cyclic lemma | 確認 | `c5_two_spoke_split_support.md:69–98` 的前提是同一原全degree-4 minimal-q disk、內部連通、有cycle、不碰singleton點，甚至不需T4；K逐項滿足。長環／雙triangle／fork 原文結構結論亦不需固定Σ。Endpoint minor 不會創造新框附件，18封存bases都碰singleton，故無tails |
| 252→40→36／4 | 確認 | actual C 是兩點edge或五點双triangle刪r形。完整degree給附件槽數2,2或1,2,1,2,2；在234各槽3種，9＋243=252。標準庫獨立重建全部原邊、十列完整染色：40 T4／q，36有p／root D完整延拓，4有原K₅；另核對656 q-critical邊與2,600保存full witnesses |
| 最後四份五袋 | 確認 | models0／9／35／99 的私有相鄰點共同接23或34，去掉它們後原H仍連通、補框弧含b0、原rb0連餘袋；五袋及十原邊逐份獨立核對，見下表 |

| model | 五個原 K₅ branch sets |
| --- | --- |
| 0 | {6}；{7}；{2}；{3}；{0,1,4,5} |
| 9 | {9}；{10}；{2}；{3}；{0,1,4,5,6,7,8} |
| 35 | {9}；{10}；{3}；{4}；{0,1,2,5,6,7,8} |
| 99 | {9}；{10}；{2}；{3}；{0,1,4,5,6,7,8} |

252 形式不是 disk 來源枚舉；無界涵蓋由 actual-source cyclic lemma 承擔，
有限 checker 只檢查這兩個已化約的原圖形及全部有標記附件。

## 7. 另列的產物缺口與具體補法

**判定：有缺口，可補；不構成最終 §5.2 的反例。** 具名位置：
[remaining checker](../../scripts/c5_excess_one_e2_951_remaining.py):640–668，
[舊 sidebranch JSON](../../artifacts/c5_excess_one_e2_951_remaining/interior_bridges_and_sidebranches.json)
的 `final_four_sidebranch_schedules[*].paper_mechanism`、`scope` 及
`remaining_t1_double_minimal_schedules=0`。

程式仍生成「The long block has one pendant component」及 conditional
arbitrary-size closure。前面的盾弧計算只把 bridge path 化到兩個 W，沒有證出
長 W 的 off-path block tree 只有一個 pendant，也未證出所有接點邊都屬該 pendant。
因此旧 mechanism 本身推不出任意旁支結案；checker 重播相同文字並不補上該步。

E2:363–365 已明確用
[final_sidebranch_terminal_blocks.json](../../artifacts/c5_excess_one_e2_951_remaining/final_sidebranch_terminal_blocks.json)
的任意 terminal-block 論證取代它，該最終論證本次確認。所以補法是保持歷史
snapshot 內容，但由整合者在其 machine scope／evidence 與生成器加
`superseded_by`、標明舊 one-pendant 論述不承擔結案；若保留剩餘數0，必須
明列它引用 final terminal-block 層，而非舊 mechanism。也應讓 CLI 的
`final_t1_double_minimal_open_schedules` 明確來自最終層，目前它讀的是舊 side 層。
本次依約未修改任何被稽核檔案。

## 8. 稽核項 6：把 E2 論證套到兩張 ε=2 圖

**判定：確認，ε=1 確實被實質使用。** 不重跑 E1 枚舉；只讀使用者指定兩個
JSON pointers，獨立重算原 degrees、完整 Σ、T4、逐邊 Σ-criticality、rotation
的 darts／faces／Euler=2 及原 C₅ 外面。兩份都滿足 E2 的一般來源前提，只有
ε 層不同。完整原邊、單列 cores 與失效步驟保存在 independent_results.json。

### 951：`/exhaustive/4/minima_by_sigma/951`

原 root=5，deg=6，其餘6／7／8／9均degree4。H−5有兩原 binary
`C₀={6,9}`、`C₁={7,8}`，actual supports分別014、123；spokes為35、45。
兩份盾長都2，互斥，故**純盾弧通過是正確的**，它不會排這張圖。

第一個不能套的步驟是 E2:99 的「唯一 degree-5 root」；其後 §3.1:103–105
「真子核心恰省略一條 incidence、容量二不可整份省略」也具體失敗：

- index3／singleton2：省略整份 C₁，root 6→4，保留 C₀，core mask1015。
- index6／singleton0：省略整份 C₀，root 6→4，保留 C₁，core mask959。

兩份 core 均自己 minimal-q、全 degree4；省略的是**兩條**原root incidences。
因此 §5.4「至多一份原 binary」不能推出；本圖恰有兩份。
若誤送入 §5.3 的兩-spoke (2,1)，也會在容量合計失敗：實際是(2,2)，
非root剩餘容量5−2=3。獨立完整 relation 更給 index3 的 C₀ 禁{2,D}、C₁禁空，
index6 的 C₀禁空、C₁禁{0,D}；G不是兩列的full minimal core，
不能套 §5.3 的兩份 singleton private-color 覆蓋。
失效皆由原degree6／ε2造成，沒有把它錯判為ε1排除。

### 935：`/exhaustive/2/minima_by_sigma/935`

原H是triangle567，degrees5=5、6=5、7=4；roots是5與6，而非唯一root。
第一個不能套的仍是E2:99；§3.1的單一root省略身份論證失效。
本次取出的三份全degree4原cores可具體寫成：

- index3／singleton2：省略16、25，core mask1015。
- index4／singleton1：省略15、16，core mask1007。
- index6／singleton0：省略06、15，core mask959。

每份都同時從兩個root各省略一 incidence，沒有單一原root／單因子省略身份。
還可在 singleton1 列直接省略整個 mixed 頂點7：剩5、6皆degree4、兩端都被
spokes強制成D，原56邊拒絕，core mask1007。這不是 §4 假設的唯一root加一份
原binary及三單容量因子。H−{5,6}的{7}是mixed、短支援34；
不能把唯一root的unary最短盾弧／分拆定理拿來排它。
所有失效同樣由兩個degree5／ε2造成。

§2 的一般degree、H連通、T4及disk核對在兩張ε2圖上仍通過，這是預期行為；
§3.1之後的degree／容量前提則不能通過。本次没有发现「本应失效却被继续套用」的
最終证明步骤，亦沒有從純盾弧預算誤推出ε1結論。

## 9. 稽核項 7：重播、文件檢查及結束 SHA

**判定：確認。** 五個 checker 各執行普通與 `PYTHONHASHSEED=17` 的 `--check`，
全部 exit0，每對 stdout相同；原 artifacts逐byte相符。實際命令與全部輸出在
[replays.json](replays.json)。均設定 `PYTHONDONTWRITEBYTECODE=1`，沒有重生成
被稽核artifacts。935讀封存接回表；remaining依原checker重播明列9,504固定
構造族，沒有重跑E1或歷史大枚舉。

```bash
.venv/bin/python scripts/c5_excess_one_e2_935.py --check
.venv/bin/python scripts/c5_excess_one_e2_951_remaining.py --check
.venv/bin/python scripts/c5_excess_one_e2_951_three_spoke.py --check
.venv/bin/python scripts/c5_excess_one_e2_951_two_spoke.py --check
.venv/bin/python scripts/c5_excess_one_e2_951_unary_core.py --check
# 各再以 PYTHONHASHSEED=17 執行一次。
python3 audits/2026-10-04-task-d7/independent_check.py --check
PYTHONHASHSEED=17 python3 audits/2026-10-04-task-d7/independent_check.py --check
python3 audits/2026-10-04-task-d7/one_spoke_check.py
python3 audits/2026-10-04-task-d7/cycle_core_crosscheck.py
```

252小型交叉核對自行生成十種canonical proper rows，再從紙面兩種actual
interior及完整degree生成附件，按固定頂點次序DFS枚舉完整染色。以原edge key
對齊資料，不靠model序號、原checker函數或原計數答案決定接受性。
它逐份重算252個Σ、40份所有root／binary joints與full counts、保存witnesses、
656原刪邊及四份新構造K₅。普通／seed17兩次结果相同。

完成後必做的三條命令、實際exit／輸出及SHA結束結果記在
[verification.json](verification.json)。本節不把文件checker當數學驗證。

| 命令 | 實際結果 |
| --- | --- |
| `python3 scripts/check_docs.py` | exit0：`OK: 545 Markdown files, 5775 local links; anchors, index, handoff checked` |
| `python3 tools/docgraph check` | **exit1**：62 documents、213 relations、5 families；1 error、0 notes。`duplicate-id`：`c5.adjacent-degree5-interfaces` |
| `git diff --check` | exit0，無輸出 |

DocGraph的重複ID同時來自`docs/c5_adjacent_degree5_interfaces.md`與
`audits/2026-10-04-task-d6/scope_history/snapshot/docs/c5_adjacent_degree5_interfaces.md`。
後一個snapshot是本次稽核期間新增的D₆路徑，起始manifest中不存在；原docs檔案
SHA未變。D₇未引入DocGraph ID，也未修改D₆快照來消除錯誤，依約如實保留失敗。
此工作區文件檢查錯誤與E2数学判定、十條checker重播成功分開記錄。

## 10. 整合者應寫回的更正

1. **必要更正：** 對舊sidebranch artifact／生成器加final層取代標記；
   舊「one pendant」不承擔無界結案，CLI的final數字應有真正final層來源。具體補法見§7。
2. **適用範圍澄清：** E2:202「不相鄰二點Q的每個位置沒有拒絕鄰點」在Q恰兩點時
   正確；為銜接§3.3對更大Q的涵蓋，宜改為「所選兩列彼此不相鄰；若Q另含拒絕鄰列，
   相應列已有真子核心」。分支本身完備：兩列皆full-minimal走§5.1–5.3，
   任一列有proper core走§5.4；並未依賴其餘三色列被接受。這是文字澄清，不是數學反例。
3. **補顯式歸納：** §5.2簡寫的D-membership可加入本報告§5／one_spoke_notes的
   rooted leaf-to-root扣palette，以及bridge／odd-cycle exact parent query，避免讀者誤套整份binary的unary守恆。
4. **補標記完備性：** §5.1首次cycle的入口cutpoint非contact，因兩contacts已在末端
   leaves；§5.4双triangle的bridge可從任一contact端出發，原圖isomorphism與兩contact
   同時交換使固定模板及全部附件已涵蓋兩朝向。
5. **保留證據邊界：** ε0單缺失和ε1任意大小結論是紙面化約＋外部Gallai＋歷史分類／transfer
   ＋新有限末端的合成；沒有Lean或一般ε≥2、disk可實現性、完整state轉移、K∞=K≤5的證明。

本次沒有代整合者改寫E2。最終數學鏈的逐項「確認」與舊machine證據的「有缺口」
分開保留，後者不能因重播通過而刪去。
