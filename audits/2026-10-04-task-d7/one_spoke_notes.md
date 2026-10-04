# D7 子稽核：§5.2 一-spoke (2,2)

日期：2026-10-04。只新增本稽核目錄的檔案，未修改 E2 報告、scripts 或 artifacts。
總 baseline／結束 SHA-256 核對與五個 checker 的重播由主稽核執行。

稽核直接讀取現行 [E2 報告](../../artifacts/c5_excess_one_e2/REPORT.md)、
[盾弧工具](../../docs/c5_unary_shield_budget.md)、
[文件證據規則](../../docs/DOCUMENTATION.md)，並開啟下列引用原文。
此子稽核沒有 import 任何 repository checker，也沒有重跑來源圖大枚舉。

## 逐項判定

| 項目 | 判定 | 具名位置與理由 |
| --- | --- | --- |
| 102 筆通用必要表的前提 | 確認 | E2:274–279；residual-locality:31–55、134–151，two-two:55–75。必要前提為連通 H、induced C5 disk、minimal q、唯一完整 degree-5、唯一 spoke、兩份不同原二接點分量、T4；沒有要求 Σ=933／941 或恰缺兩列。 |
| 102→30→54 | 確認 | E2:280–281；獨立 checker 從 102 原身份重算 51+51，按連續支援、盾邊互斥及 spoke 不落盾弧內點剩 30，再保留整圖 D5／S4 同步搬運的遠列必要覆蓋，得到字面相同的 54 份身份。 |
| 原首橋排除 36 | 確認 | E2:288–302；獨立重算所有 residual 支援候選與三框弧 K5 判準，36 份所有局部變體都無支援或有原圖 K5，餘 18。 |
| carrier 的 D-membership 歸納 | 確認 | E2:304–320；branch-palettes:43–55、first-bridge:79–112。歸納只在 path 外、沒有原 r-contact 的點上做；沒有將 binary 改成 unary。精確 rooted queries 與橋交替見下文。獨立有限表再排 14。 |
| 四份 W_j 的盾弧前提 | 確認 | E2:331–338；shield-budget:54–109。W_j 連通，H−W_j 經其餘 path 段與 r 連通，整圖碰齊五框點；引理 1、2 的證明只需這些結構，不需 W_j 是 H−r 的整份分量，也不需 Σ=933／941。 |
| 四份的短 W 與末端 block 排除 | 確認 | E2:340–362；完整 terminal-block 推導處理任意旁支數、深度與環長。獨立核對 96 份共同色框 list 表與 12 份 minor skeleton 的五袋連通、不交及全部十條原邊鄰接。 |
| 舊 sidebranch artifact 的結案聲明 | 有缺口 | remaining.py:641–645、650–668 及 interior_bridges_and_sidebranches.json 的 paper_mechanism 仍寫「The long block has one pendant component」，並以 remaining=0 宣告 arbitrary-size closure；此數量斷言沒有獲得所需證明。E2:363–365 已明示 final_terminal layer 取代它，因此不能將此舊 artifact 當最終任意旁支證明。 |

## 引用前提與必要域的獨立推導

residual-locality §1 明列一般 minimal-q 來源；§4 又明確分開一般指定列分離
與額外 Σ=Ω\{p,q} 下的 single-sided exit。本輪只使用一般來源必要表，
沒有將後者較窄的恰缺兩列出口偷渡進來。

完整 relation 下的禁色 F 是所有同一分量完整 coloring 的 tuple 色集交集。
minimal-q 的兩 binary 因子必各有 private color，禁色大小至多二，但兩個
pair 重疊本來仍可能形成不可刪減覆蓋；不能用 ε=1 本身禁止 pair/pair。
102 表是既有一般來源排除後的必要接口，剩 51 份 (1,2)、51 份 (2,1)。
本獨立 checker 以這個既有接口為資料輸入，沒有聲稱重新生成此前 278 份
來源排除的整份證書。

二接點分量 C 忌 pair {a,d} 時，對同一 C 比較 root=a 與 root=d 的
兩份拒絕 degree lists。path 外的 block 消去後兩份 palette 一致；兩
contacts 殘差交換 a/d。沿 block-cut tree 的 contact 路徑，每個 block
的 palette 必不同；odd cycle 有第三個不在 contact 路徑的頂點，其
相同 residual 又會迫 palette 相同，因此 path 上只能是原 bridges。
首橋差 (d,a)，逐頂點交換為 (a,d)，末端又須 (d,a)，故原 path 長度奇數。
補回 contacts 扣掉的 root 色後，每個 W_j 的 residual E_j 恰為 {a,d}。

由 rooted palette 唯一性，固定 W_j 全部實際框色的置換必保持 E_j；
兩列在某色的逐點 membership 相同時，E_j 對該色的 membership 也相同。
若兩列在 W_j 的實際支援上由一個共同色置換相連，E_j 則協變。
這給小 checker 的三類局部支援必要條件。

三個非空連續框弧 X、Y、Z 分割 B 時，它們兩兩有框邊鄰接。若相鄰的
兩個 W 均實接 X、Y，且 Z 含 spoke 或另一原分量的實際落點，則取
W、W′、X、Y、Z 加 contact-cycle 餘段與原外部路徑為第五袋。
五袋連通不交；W–W′ 用所選原 bridge、兩 W 到第五袋用 contact-cycle
朝外原邊、四條框附件加三条框弧間原邊給十條鄰接。此構造涵蓋首橋
與內部橋。獨立 checker 用 3^5 指派直接生成 60 個框弧分割。

## D-membership 與精確 rooted queries

在 carrier 分支，先選 pair 列 root=a、root=D 的同圖拒絕證書；另一列
root=c 拒絕，c≠D。所有 path 外非 root 頂點不是原 r-contact，兩列
框上都未用 D，因此它們的原 lists 都含 D。

對每個 rooted block，任選一個非 root 頂點，扣除已由葉向根確定的後代
palettes；餘 list 正是該 block palette。扣除前的 D membership 相同，
每個後代 palette 的 D membership 由歸納相同，且 incident palettes
不交，所以餘 palette 的 D membership 相同。這包括任意多層 bridges
及 odd cycles；歸納不使用整份 binary 的 unary 禁色守恆。

pair 列每個 E_j={a,D}，root 直接框附件未用 D，故扣除旁支 palette
後，singleton 列的每個 E_j 仍含 D。其 endpoints 補回 c 後為 {c,D}，
bridge palette 因此在 D／非 D 間交替，第一與最後 bridge 都為 D。

精確延拓是可直接證的。對一個已消去後代的 rooted bridge，唯一非 root
點的 list 是 singleton palette，parent 色在此 palette 時不可延拓，
不在時可延拓。对一個 rooted odd cycle，全部非 root 點的餘 list
是同一兩色 palette；parent 色在 palette 時 odd cycle 不可二染，
parent 色不在時將剩下的偶數個頂點沿路交替染兩色即可。各 rooted
後代只有這個 parent 碰外部，逐層接回給「parent 色可延拓 iff 不在
incident palettes 聯集」；不同後代的完整 coloring 接在同一原 parent
色上，不是獨立相乘端點 marginals。

若所有偶數橋 palette 都是 c，則全部 E_j={c,D}。同一奇數長原 path
在 root 固定 c 或 D 時兩個 contacts 都被迫另一色而矛盾，所以 F_C
至少含 {c,D}，違反另一列只禁 c。故有一條偶數原內橋 palette d∉{c,D}，
其兩端 E={d,D}。對此原橋的雙列支援表及上述五袋 minor 重算，排掉 14
份，沒有假設各處非 D 色沿 path 守恆。path 長一時同一論證已直接矛盾。

## W_j 盾弧與最後四份

W_j 是刪去 C 的原 bridge path 邊後含 x_j 的原連通分量。其他 W 經 path
的左右殘段與 r 接在一起；即使 j 是 contact endpoint，H−W_j 仍透過
另一 contact 接 r，另一原分量也接 r。因此每個 W_j 及其補集都連通。

盾弧引理 1 的面論證只有連通集 P、连通補集 H−P、disk 外框之需；
1(d) 的更正使用 P′ 內点所在開面避開另一面，允許共享框頂點。
引理 2 唯一額外使用的是「整圖碰齊五框點」：盾弧內點若不被 P 接，
就須由補集接，與 1(c) 矛盾；端點若無 P 附件，兩框邊同面，亦矛盾。
此推導對 W_j 原頂點集合逐步成立；未使用其為 H−r 的整份分量。

82/317 每個 W_j 的必要支援見 b1 且至少另見一點；477/817 則見 b0。
1(b) 使各 W_j 占此點一條 incident 盾邊，1(d) 互斥，最多兩份 W_j。
奇數長 path 至少兩個頂點，因此恰兩份。保留原 pair 分量全部支援後，
兩個連續支援只能是 01 與 123，或 01 與 034；兩 contact 朝向可互換。

短 W01 的 path 外連通分量 P 只有 parent 這個外部內點鄰居，完整 degree=4。
某條原 parent incidence 的 Σ-critical witness 給 P 一份拒絕；H−P 連通，
且包含碰框補弧 B−01 的內點。三個 hubs {b0}、{b1}、(H−P)∪(B−01)
相鄰；parent 色若等於一端框色，就將該端加入第三袋，只需兩 hubs。
這直接滿足 hub 原則，故 P 不存在，短 W 只有原 contact。

長 W123 在 q 下只見 0、1，長 W034 在 p 下同樣只見 0、1。若有 path
外 blocks，block tree 有 terminal block，其 private 點不含原 contact。
bridge leaf 需要三個框鄰点且 tightness 要三異色，與只見兩色矛盾；
K4 由连通外框排除。terminal odd cycle 的 private 點只容兩個相異
框鄰點；可能為 12/23 或 04/34。第一列都產生 {2,D} palette，partner
列兩個 actual pair 卻產生不同 palette，所以同一原 cycle 的全部
private 點只能接同一 actual pair。

取相鄰 private 點 u,v，H−{u,v} 仍連通；adjacent pair {b_i,b_j} 的
框補弧包含原 spoke 端點。五袋 {u},{v},{b_i},{b_j},
(H−{u,v})∪(B−{b_i,b_j}) 的十條鄰接都為原圖邊，故 K5。
這包括 triangle、任意長 terminal cycle 及 terminal cycle 穿過 W 根的情形。
長 W 遂無旁支，僅其 contact；完整 degree=4 只容 r 邊、path 邊及兩條
直接框附件，不能承擔三點支援，四份全部排除。

## 舊 artifact 的具體補法

保留舊 sidebranch snapshot 的歷史內容，但在其 scope/evidence 加
`superseded_by: final_sidebranch_terminal_blocks.json`，明列舊
one-pendant 敘述不承擔任意大小結案。生成器也應產生這個標記；
`remaining=0` 若保留，應明確寫由 final terminal-block 層承擔。
最終 REPORT §5.2 的 terminal-block 證明本身已補上此缺口，無需改判錯誤。

## 有限重播與證據分層

```bash
python3 audits/2026-10-04-task-d7/one_spoke_check.py
PYTHONHASHSEED=17 python3 audits/2026-10-04-task-d7/one_spoke_check.py
```

獨立小 checker 兩次相同：102→30→54→18→4，36 首橋及 14 carrier 排除，
最終 IDs 82、317、477、817；八個具名支援朝向，96 palette 行、12 K5 skeletons。

紙面任意大小：bridge-path／rooted block 歸納、shield 面論證、原圖 minor。
外部定理：不可著色 degree-list 的 Gallai／block-palette 刻畫；本子稽核
沒有將它稱為自己證出的定理。Python：只重算這個必要接口的有限域及
minor skeletons，沒有提供 disk 實現性或任意大小來源枚舉。Lean：沒有新增
或重播 theorem。全 repo 文件檢查由主稽核統一執行。
