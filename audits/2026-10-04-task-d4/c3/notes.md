# D₄：C₃ 獨立稽核

2026-10-04。只讀 `../snapshot/` 所固定的正式返回工作區；生產腳本、
原 artifacts、既有 audits 和共享文件均未修改。獨立程序只 import 本目錄
的 `independent_helpers.py`，它由 D₃ 的原邊／染色／minor／subdivision
validator 截取，沒有 import 生產 checker。著色器另以 MRV backtracking
實作，完整重算 relations 與所有具名 fibres。

## 驗收結果

- 第一版 `attempt1/`：13,574 checks，0 failures。
- 加強版 `attempt2-seed17/`：13,579 checks，0 failures。
- 加強版一般 seed 重播另存 `attempt3-default/`。
- 最終版保留兩份固定 keys 的 literal 原接點名稱 u₀,u₁,u₂／v₀,v₁,v₂，
  輸出另存 `attempt4-default/` 與 `attempt5-seed17/`，均13,579 checks、0 failures。
  两个 seed 的 results、完整 ledger、relations、source versions 和 source
  全部逐 byte 相同；SHA256／bytes 保存於 `final-comparison.json`。
- 稽核 source、SHA256、log、每次結果各自保存；沒有覆蓋旧版本。
  初次錯誤文件路徑讀取另存 `initial_read_failure.txt`。
- 初版和加強版 attempt2／attempt3 的 `scope_ledger.json`、`relations.json` 相同；後續增加的是
  stored lifts 覆蓋、衍生數字和 source hash 檢查，未修改證據或閉合範圍。
  最終版 ledger 明確区分已具名原接點與尚未實現來源的 ordered contact symbols。
- 檢查器的負例刻意破壞 ten-pair edge、bags 不交及 X 連通性，三份
  不合法 minor 均被拒絕，逐項失敗明細保存在 relations 的 negative controls。

精確接受 **CPP-134-1／geometry 34／side_join 20** 的任意大小來源排除；
此處任意大小是紙面推導加外部 Gallai 定理，固定 Python 的控制域另列。
與 C₂ 合用只登記 **CPP-134-1／geometry 30／side_join 20** 和
**CPP-134-1／geometry 34／side_join 20** 兩個具名 keys。沒有驗收其他 w
角色、root 交換、geometry 35 或整個 case。

## 完整 C 前層與具名 scope ledger

`audit_c3.py` 獨立產生必要側角色、125 個每色接合、500 個原接點配置、
560 個具名 cases、fan sectors、保色 stabilizer 條件及四種線性順序，
逐欄比對 predecessor artifact，不 import 其程序。140 份 geometry
各自與所屬 case 的 25 個 side joins 做具名組合，得到 **3,500 distinct keys**。

`scope_ledger.json` 的每個 key 均保留同一 q、原 x₀/x₁/x₂ 身份、
全部原附件、完整 P₃ triples、禁對、全部 16 份 P₃ fibres（含空份）、
每份 tuple 的原 P₃ lift、case／geometry 全欄、兩份 side-role 全欄、
每份原 unary 的有序接點、未知完整同源 relation 及其符號 fibres。
只有單份 unary 且無 spoke 的側把整側支援辨認為該 unary 自身支援；
其他分拆的各自支援保存為未知，未任意分派。

3,500 keys 中只將上述兩個 keys 標為 closed，其他 **3,498 keys** 明標
`not_audited_by_C2_C3`。這是 geometry／join 組合的 ledger 粒度，不能把
它與 900 個 retained case-role joins 混為同一個集合。
原 predecessor **36 cases／140 geometries／900 case-role joins** 全部保留，
沒有刪除、篩選或重寫 artifact 的表格。

下一停止點精確為 **CPP-134-1／geometry 34／side_join 60**，
side IDs=(27,1)。原 z 側分拆為兩份 unary，接點數 (2,1)、禁色
({0,3},{2})，無 spoke；w 側三接點、禁色 {0,2}、無 spoke。
兩側整側支援仍 {b₁,b₂}/{b₂,b₄}；本輪未分析兩份 z unary 的各自支援、
blocks 或完整 relations。ledger 保存下一 key，而未把前一引理外推。

## 任意大小紙面推導

固定原 unary D，外部只有 z,b₁,b₂。三個原 z 接點互異，D 連通，
每個原點完整 degree 四，所以 d_D=4−p−s₁−s₂。原禁色等式
f_D={0,2,3} 表達完整原 relation 的拒絕，不要求 z=h 的局部問題
可接成整份 M；w 的未知完整原 relation 沒有被換成控制模型。

對 h=0，重複外部色只能來自 z 和 b₂，所以
|L₀|−d_D=p s₂。若某點 strict，按到該點距離遞減排列可把連通 D
貪婪染成，違反禁色 0。因此接點不能碰 b₂；這一步仍保留非接點
同碰 b₁,b₂ 的內度二身份。所有點 d_D≥2。h=2 的外部色 2,1,0
互異，所有 lists tight；D 不可染且連通，Gallai 給出 blockwise palettes。

外部 X₀=B∪{z,x₂} 保留原 z−x₂−b₄，連通而與 D 不交。K₄ block
的四個頂點每個只留一個完整 degree 方向。方向或直達外部，或進入
一份只以原 bridge 抵達該 clique 頂點的原外側分量；不同 clique 頂點
的外側分量不交。刪 bridge 後兩側 lists strict，均可染；原拒絕使两個
完整端點可取色集是同一 singleton。若外側不碰 z,b₁,b₂，其全部 lists
為 U；S₄ 置換原染色使端點可取四色，矛盾。因此四條原 tethers
各有一條原路抵達 connected X₀；四個 clique singleton bags 與外部
hub 合成 K₅。K₅ block 耗尽 degree 四，不能再含原 z 接點；更大 clique
違反 degree。此段推導的是原邊，沒有把 finite route controls 當成源圖。

leaf bridge 的 private endpoint degree 一，已排除。leaf odd cycle
的 degree 二 private identities 恰是 T=(接點＋b₁)、N=(非接點＋b₁＋b₂)。
L₂(T)={0,3}，L₂(N)={2,3}，同一 leaf block 的 private lists 等於
同一 block palette，所以一葉必純 T 或純 N。這是原 block palette
等式，沒有從 marginals 拼接。同一 cycle 的 L₃ 控制亦保存，但證明只需 L₂。

多 block 純 N 葉選兩個相鄰 private 原點 a,b。D−{a,b} 仍連通，且
三個原接點全在 N private set 之外。原 X=(D−{a,b})∪{z,x₂,b₀,b₄,b₃}
連通、不含 a,b,b₁,b₂。五袋 {a},{b},{b₁},{b₂},X 的十對原鄰接為
ab，a/b 各接 b₁/b₂，a/b 各一條另一原環邊到 X，b₁b₂，b₀b₁，b₃b₂。
即使 N 葉為 triangle，a,b 的原環外側端也可同為 cut c，仍是合法
五袋 K₅ minor。任意奇環長、任意其他 blocks／bridges 與任意 D 大小
都在此原圖抽取論證內。

有限 block-cut tree 若多 block，至少两份 leaf blocks，cut nodes 不會
假扮葉。排除 N 葉之後，每份 T 葉有至少两个 private 原接點；兩份
葉 private sets 不交，需至少四接點，與原三接點矛盾。剩單一 block
必 odd cycle；它含原接點且 palette uniform，故所有點 T。原三接點
遂迫回三點 triangle，自身支援 {b₁} 與指定 {b₁,b₂} 矛盾。此是條件
reduct，未更換原 unary。原外路亦給兩份 K₅ subdivisions 作控制。

## 固定控制與完整關係

八種 (p,s₁,s₂) 身份的四個 root pins 共32份 list identities 已重算；
两種 p=s₂=1 由 strict-list 紙面引理排除，其餘六種仍保存。
两種 degree-two 身份及 pin2/pin3 的 T/N palettes 正確。

四個 N cycle＋原 bridge＋T triangle 控制為 n=3,5,7,9。每份 D 的
原頂點全部完整 degree 四、自身支援恰 {b₁,b₂}，完整接點 relation
恰六個 permutations(0,2,3)，共24份 tuples及其原內點 lifts。
每份原 root relation 有 16 個具名 fibres：z=1 的四份各有六 tuples／
12 全染色，另12份完全空。稽核 `relations.json` 保存所有16份與實際 lifts。

每模型在三拒絕 pins 下刪原 bridge，逐份測完全部16个有序 (c,d)
pins，共192份 endpoint fibres、12份完整同圖 endpoint relations；每份
恰 {(1,1)}。成功 pins 的全部局部 lifts 与失败 pins 的空份都保存，
不以端點 marginals 取代 joint，也不宣稱這些 root pins 皆可接原 P₃／w。

四份邊數17/23/29/35，共104條。逐邊刪除後獨立重算全部16个 root
fibres，完整 root relation 均 U²；各份刪邊後的完整接點 tuples、fibres
及實際 lifts 均保存。原416份局部 witnesses、312份拒絕 pins 的同色
刪邊兩端、104份 context partial witnesses 全部核對。partial context
只保留原 B、P₃、zw/zx₂/wx₂ 及 unary 控制，固定 z=0,w=1、P₃=(3,0,3)。
原 D_w 避 w=1 fibre 的非空性由禁色等式保證，其內點不在枚舉，
這些資料沒有證明整份 M 逐邊 minimality。

四份 N 原 K₅ minor 的五 bags 逐份檢查非空、互不交、連通，以及
全部十對的實際原邊端點。162份 K₄ routes 的四個端點逐項由 z,b₁,b₂
取值，兩種统一 tether 長度；所有五 bags、十對原邊及完整 context
均正確。它們是固定 connected-exterior 路由控制，非 degree／source 實現。

條件 T triangle 保存六 tuples、九條刪邊、36局部 witnesses、九份
partial contexts和兩份原外路 K₅ subdivisions。其支援明標 {b₁}，
與原 geometry34 所需 {b₁,b₂} 不相容。完整 ten routes 的端點、内部
点不交、原边 provenance 和 branch degree 均核對；沒有用它替換原 D。

## 外部定理與證據界線

已 live 打開並核對 [Dvořák 的原始大学托管講義](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
PDF 第5–6頁的 Lemma7、blockwise-uniform 定義與 Theorem10。保存原 PDF
及 `gallai-primary.json` 的 URL、頁碼、SHA256、檢索日期。
Lemma7 適用連通 degree assignment；Theorem10 的 connected hypothesis
及 shared cut palettes 不交／聯集条件都与本轮 D 的原身份匹配。
沒有使用 critical-graph Corollary11 或 Theorem4。

任意大小原 block／tether／葉數是上述獨立紙面審查；Python 驗證固定
四個控制及有限路由，沒有外推控制域。既有 Lean build 另由 D₄主線
驗證，不是 C₃ 紙面拓撲的 Lean theorem。0 target queries；沒有完整 Σ、
disk source realization、一般／共同出口或 K∞=K≤5 的新增宣稱。

```bash
python3 audits/2026-10-04-task-d4/c3/audit_c3.py --output audits/2026-10-04-task-d4/c3/replay-fresh-default
PYTHONHASHSEED=17 python3 audits/2026-10-04-task-d4/c3/audit_c3.py --output audits/2026-10-04-task-d4/c3/replay-fresh-seed17
```

每次輸出路徑必為新目录；若已存在，程序拒絕覆蓋。生產重播、全局文件、
DocGraph、artifact和diff检查由 D₄ 主線另存，不能從本份独立audit
推論它們已通過。
