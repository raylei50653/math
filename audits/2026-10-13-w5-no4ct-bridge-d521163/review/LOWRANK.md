# W5-NO4CT-BRIDGE：森林至圈秩二的獨立前提／覆蓋審閱

審閱 BASE：`d521163`。本檔只新增於本輪 review；舊 BASE、seal、manifest、
證書和歷史 receipts 均未修改。本次只讀紙面、程式參數、模板 metadata、
summary 與 receipts，並對可見 metadata 核對原 DELIVERY SHA；**沒有重算
任何染色，沒有重播完整舊證書**。完整 archive-byte custody 由本輪主報告另記。

**結論：在 frontier 的 932／933／941 三支共同 no4ct 全域最小來源契約下，
任取合法全內部 induced W5，森林、圈秩一及圈秩二的來源排除全部可接通。**
舊低圈秩證明沒有需要 singleton support 非空的步驟；`933/941 not triggered`
是歷史實例狀態，並非其結構分類前提。新 `k≥16` 反而縮小必要模板域：
森林直接由大小矛盾排除；圈秩一只留 252 個舊 C10 模板；圈秩二只留 70 個
舊 `c=1,r=10,a=0` diamond 模板。後兩域的原完整 Σ 全為 1023。

## 1. 具名來源與實際所需前提

固定全部完整有序外框關係不屬 K132 的 finite simple plane disk-C5 圖，
先全域最小化內點數 `k`，再最大化邊數，取 G。不是固定某一 mask 最小化。
對任何合法 W5，B 為原外框，v 的完整原鄰集恰為循環有序 U，B/U 十 pins
互異；U 為 induced C5，其有界盤恰含 v 及五個原三角面。
令 `A=G−v, P=V(G)\(B∪U∪{v}), F=G[P], r=k−6`。

本輪讀取的新來源依據為
[frontier w5/PROOF](../../2026-10-13-c5-no4ct-frontier-6943561/w5/PROOF.md)
與其 [DEPENDENCIES](../../2026-10-13-c5-no4ct-frontier-6943561/w5/DEPENDENCIES.md)。
其 BASE 是 `6943561e644e7598342d1ccd7df44dac0ebcd5cf`，本審阅没有更改其採納域。

| 低圈秩實際使用項目 | no4ct 接入 | 判定 |
|---|---|---|
| G 簡單、二連通、B induced、內面三角化 | frontier PROOF §1 的已凍結 degrees/collar 結果 | 新三支共同供應 |
| `k≥13`，即 `r≥7` | 同處更強的 `k≥16`，即 `r≥10` | 新三支共同供應；可縮小域 |
| 每個原內點 `d_G≥5` | frontier PROOF §1 | 新三支共同供應；不得改成 `d_F≥5` |
| 原 B 點 `d_G≥4` | frontier PROOF §1 | 用於原 B 附件界 |
| 原 occupied triangle 不存在 | frontier PROOF §1 | 新三支共同供應；主要用於 W5 槽位存在／唯一 apex |
| 每個原簡單 C4 有界內部空 | frontier PROOF §§2–3 | 受限 C4 代表＋實際 `s<k` 已修復；不是普遍 4CT screen |
| 每個私人點至多接兩個 B，雙接必相鄰 | frontier PROOF §4 | 新三支共同供應，包括接觸 B 的 C4 |
| 每個私人點至多接兩個 U，雙接必相鄰 | 下述 U-ATTACH 推導 | 三支共同局部後果 |
| proper C5 內部空或一 W5 中心 | frontier PROOF §§2–3 | 已供應，但森林／rank1／rank2 分類不需要再使用 |
| singleton support 非空、Σ 限於 933/941 | 沒有任何低圈秩結構步驟需要 | 不採納此舊來源限制 |
| 普遍 exterior screen、任意大小 C4 代表 | 原低圈秩只消費其來源結構後果 | 本接入不消費；不用它們補缺口 |
| 一般 annulus 小代表 | 低圈秩接入可直接利用縮小域的 Σ=1023 | 不需要；尤其沒有九點代表命題 |

### SMALL-CAP：boundary-touching 的嚴格大小沒有漏掉

原簡單 C4 或 proper C5 至少有一個不在 B 的介面原點，否則 B induced
迫四環不可能、五環只能是 B 本身。若 `i(C)=|V(C)\B|`，其有界側的
嚴格內點數 `s≤k−i(C)<k`；嚴格位於 cap 裡的 B 點不可能存在，因 B 位於
原外面。因此 frontier 的受限 C4 定理足夠給至多三內點代表；proper C5
由全域最小性給至多五內點代表。替換不識別任何介面原點，沿 literal
同色介面列接合，保持原 B 的完整 Σ，故來源內點數變成 `k−s+s′`。

再用原 cap 三角化、cap 嚴格內點的完整 degree 及 Euler，可排非空 C4
並得 proper C5 只能空或一中心。這個大小論證適用與 B 共點／共邊的環，
不能把「完全位於原內部」偷偷當作必要条件。

### B-ATTACH／U-ATTACH：限制的是原 attachments

若 x 接非相鄰 B 點 a,c，取短框弧 a−b−c；原 C4 `a−b−c−x` 內空，
B induced 排除 diagonal ac，故 triangulation 迫 bx。這兩原三角面佔滿
b 的內側 sector，給完整 `d_G(b)=3`，與來源 `d_G(b)≥4` 矛盾。

若 x∈P 接非相鄰 ui,uj，原 C4 `ui−v−uj−x−ui` 的兩段 spokes 與
外側 x 路徑把 U 的兩條非空開弧分居兩側；有界側必含 U 原點，違反
SMALL-CAP。因此 U 也至多接兩個且必相鄰。於是

```
d_T(x)=|N_G(x)∩(B∪U)|≤4,
d_G(x)=d_F(x)+d_T(x)≥5.
```

等式使用 v 的完整鄰集為 U。它只推出 F 無孤立點；若 x 為 F leaf，則
x 恰接兩個相鄰 B pins 和兩個相鄰 U pins，完整 degree 恰五。
沒有私人最小度數五的推論。沿 x 的原 cyclic link，至少一個 B/U 切換
供應 BUP 三角面；不同 leaf 供應不同面，因每個 BUP 面只有一個私人點。

## 2. 任意分量的共同面式

令 `q=ρ(F), c=c(F), p=#BU edges, a=#terminal-only annular triangles,
h=#PPP triangles, M=#BUP triangles`。所有量數原邊與原面。
annulus Euler 給 `e(A)=3r+20, t(A)=2r+10, e(F)=r−c+q`。
兩私人三角面數為 `2e(F)−3h`；恰一私人且兩同環 pins 的面數為 `10−a`。
因此

```
M = 2(c−q+h),     p = a+c−q+h,
sum_{x∈P} d_G(x) = 4r+10+q−c−p,
r ≤ 10+q−c−p.
```

這是同一原圖的完整 degree sum。`c` 起初容納全部分量，孤立點是在附件界
之後才排除。所有 bridges、附樹和私人 degree-two subdivisions 都仍在 F。

## 3. 森林：新大小界使有限核心不再被消費

`q=0` 迫 `h=0`，故 `M=2c, p=a+c`，從而

```
r ≤ 10−c−p = 10−2c−a ≤ 8 < 10 ≤ r.
```

已直接矛盾。這對任意大小、多分量、任意附枝森林成立，甚至不需進一步
leaf 等號分類。舊 70 模板的 completeness 與 full-colouring 結果仍有效，
但新接入不需重新調用。原論證對應
[forest REPORT §§1–3](../../2026-10-13-w5-three-support-19209f4c/forest/REPORT.md)；
原獨立原面／旋轉審閱見
[forest_independent](../../2026-10-13-w5-three-support-19209f4c/t1/forest_independent.md)。

## 4. 圈秩一：任意大小分類後只留舊 C10 子域

完整原論證：
[unicyclic STRUCTURE §§1–8](../../2026-10-13-w5-private-unicyclic-3097ef5/structure/STRUCTURE.md)。

`q=1` 的分量圈秩分配恰為一個單環分量加任意樹分量。單環分量的每棵
off-cycle 原樹只能從一個 root 接回原環；多根接回會多出一環。
唯一環 C 的 Jordan 位置只有 contractible 或分隔 B/U 的 essential。

contractible 分支中，若 C 內有私人附樹或其他樹分量，取其 leaf：它無法
越 C 接 terminal，也不能多接 C 而不增加圈秩，故完整 degree 至多一。
所以 C 內空，且沒有私人 chord；原 triangulation 迫 C 為 facial triangle。
此時 `h=1,M=2c`。三個 triangle roots 各由自身的 facial degree-two
terminal-link 或其附樹 leaf 供應不同 M 面；其他 c−1 樹分量各供應兩份，
合計 `M≥3+2(c−1)>2c`，矛盾。此步涵蓋全部附樹及分量，不使用 C5
separator，也不使用染色或 source mask。

essential 分支中 `p=h=0`，共同面式迫 `c=1,a=M=0`。原 leaf 必貢獻 M，
故沒有附樹；F 恰為 C_r。degree sum 給 `r≤10`，新 `r≥10` 迫 `r=10`。
每個 cycle edge 的兩個原三角面頂點分別在 B、U。原附件界給每側
fan 前進零／一步；原 B/U 的每條環邊在 annular 側恰使用一次，故各側
總前進五步。`d_G=4+δB+δU≥5` 排除 `(0,0)`；r=10 再迫沒有 `(1,1)`。
因此必要 domain 恰是五個 B=(1,0) 和五個 U=(0,1) 的 252 個 linear words。

原每條 cycle edge、terminal fan、定向面及 rotation 都由這個 word 和
原兩環起點恢復，Euler 邊數已滿，不存在省掉的私人或 terminal 邊。
source→template 是整圖帶嵌入同構：兩環起點可不同，但方向同步；保留
逆 pin map 後逐點搬運同一份完整染色，含全部 empty cells 與 full lifts。
沒有兩側各找一份私人 cycle 色列再拼湊的步驟。

252 詞是舊 1,652 詞域的 r=10 子集；全部原完整 Σ=1023。此 mask 在原
B 的 D5 搬運後仍是 1023，故直接違反目錄外身份。無需 prism 替換。

## 5. 圈秩二：四型／全部幾何位置後只留舊 diamond 子域

完整原論證分別為
[TOPOLOGY §§1–7](../../2026-10-13-w5-rank2-243a125/structure/TOPOLOGY.md) 與
[STRUCTURE §§1–8](../../2026-10-13-w5-rank2-243a125/structure/STRUCTURE.md)，
另參見 [原 FINAL_REVIEW](../../2026-10-13-w5-rank2-243a125/review/FINAL_REVIEW.md)。

分量圈秩分配為 1+1 或 2。取原 2-core，僅為分類而 suppress degree-two
paths，excess `Σ(d_core−2)=2` 得唯一 degree-four 分支點，或兩個
degree-three 分支點；恢復原 paths 後恰為分離雙單環、figure-eight、
barbell、theta。所有 subdivision 長度、off-core 原根樹及獨立樹分量
均保留；suppression 不是保染色的實際圖操作。

F 有恰 q=2 個 bounded complement faces。任一不含 U/v 的 bounded F
face 也不含 B；G 除 F 外的任何邊均有 terminal/v endpoint，不能進入
該 face。因此該區域就是原 G 的 PPP 三角面。這裡使用完整嵌入 F 的
實際 complement face，容許起初有 bridge slit、重複 boundary walk、
多重邊界和巢狀分量；它們不是在分類前被刪掉，而是無 terminal 的
這類區域會違反原三角化。故 U 在 bounded F face 時 `h=1,p=0`，
否則全部 cycles contractible 且 `h=2`。這涵蓋 nested/tangent 分量、
theta 兩個 essential cycles 共享路徑等全部位置。

essential 分支面式給 `c=1,a=M=0`，leaf 見證排全部附樹。私人 core excess
僅二，唯一 PPP triangle 三頂點至少一個有私人 degree 二。它的全部
terminals 在 triangle 另一側的連續 link 中；完整 degree≥5 與附件界
迫 B/U 切換，即 M≥1，矛盾。

contractible 分支 `h=2,M=2c,p=a+c,r≤12−2c−a`。兩個 bounded faces
都是原 PPP triangles。分離雙單環、figure-eight、barbell 的不同
facial degree-two roots 由自身／原附樹 leaf 供應 M，連同其他樹分量
均得 `M≥2c+2`。theta 的三條原路長由兩個三角面迫為 `(1,2,2)`；
另一形式 `(2,1,1)` 會有兩條相同 endpoints 的原邊，違簡單性。
因此唯一 core 是 diamond K4−e，沒有漏掉細分長路徑。

diamond 兩 tips 的 root-or-leaf 見證，加其他樹分量，恰用盡 `M=2c`。
等號迫 branchpoints 無附樹；tip 只容許單一路徑；其他樹分量也只能
為 paths；只有指定末端有 M。沿原 facial contour（每條 bridge 兩側
各走一次），兩個末端之間的一段全 B、另一段全 U，兩個 branchpoints
恰分居兩段，各只接該側兩相鄰 pins。這是原 rotation 的結論。

再用 `r≥10` 得 `r=10,c=1,a=0,p=1`：沒有其他分量，也没有 terminal
triangle。沿唯一 BU cross edge 切開 annulus；同一原邊的兩個 sides
是 strip 的兩邊，不能因 p=1 漏掉這個 region。完整 F 是一個 diamond
和兩端可空 paths；舊 backbone 記法為長八的 word、七個 gap 位置，
gap 原共享邊 `qBqU` 仍保留。

附件 letters 恰由原 `d_G≥5` 給出；兩側總前進五，gap 各消耗一步。
新域 degree sum 取等號，所有私人原完整 degree 均五。gap 在任一端時，
其餘六個需前進一次的位置為三 B 三 U，各給 20 詞；gap 在五個內部
位置時，兩 tips 為 O、兩 leaves 為 D，其餘四位置為二 B 二 U，各給
6 詞。完整 domain 大小是 `2×20+5×6=70`。

所有原 edge 類型（十條環邊、diamond／尾路私人邊、terminal fans、BU
cross edge）及原面皆由參數恢復。source→template 同樣是同步方向、
保全部原 attachments/rotation/full lifts 的整圖同構。70 個模板是舊
974 域的 `c1_r10_a0` 子域，全部原完整 Σ=1023，直接違反目錄外身份。
舊大域另外四個非 1023 模板存在於 r<10，不能說舊 974 圖全部全收；
本接入不需要四份較小代表，也不需宣稱全域一般代表定理。

## 6. 本次 metadata 核對及原證据對接

以下 filter 是只讀 `controls/templates.json`，條件為記錄的 `r≥10`；
rank2 的 r 位於 `parameters.r`。沒有重算 graph、cell 或 colouring。

| 原包／BASE | 舊完整 domain | 新必要子域 | 子域 Σ metadata |
|---|---:|---:|---|
| `w5-private-unicyclic-3097ef5`／`3097ef5be241b7777451a5ef8a663f3987d6b866` | 1652 | 252 (`r=10`) | 252×1023 |
| `w5-rank2-243a125`／`243a125a80e4d8de40957f59d8da0bdbc974cf69` | 974 | 70 (`c=1,r=10,a=0`) | 70×1023 |

下列 live bytes 的 SHA256 已與各包原 `DELIVERY.json` 條目逐項相符：

| 包 | 原檔 | SHA256 |
|---|---|---|
| unicyclic | `controls/templates.json` | `e205718a907c4cefd22969bb39da2c379b47b03f779ffe64516466a15663c473` |
| unicyclic | `controls/summary.json` | `309dbe6dac789c9cb3c8d4ced8eb32848e1eb44d44ce809b62f0b84e085f7607` |
| unicyclic | `math-verification.json` | `2c59df72e29bd393cec304b755e5c447cccfb43b1c357e8fdce84a92c116cf46` |
| unicyclic | `independent/verification.json` | `2dd2e0df4c3e76c336debedfcf8dd7f95deb3e830967a7fb3a4a3ab436623520` |
| rank2 | `controls/templates.json` | `04659917561d206456777329f49221f9ceb5efc5b5ac9116a3c00effaa9ee748` |
| rank2 | `controls/summary.json` | `e8af33fffda32a3f687fbfc7f42dbc188c516899bc7aa1063a0d059f979aeb1e` |
| rank2 | `independent/verification.json` | `74843b47faf4d6d55b472810efb55e75395a71b9a1121275bc6abb7cb7ed50a9` |

完整 certificate 均為 `controls/certificate.jsonl.gz`；在新 worktree 中
按既有 archive policy 不直接存在。本次未 restore、更未改寫。原 manifest
指定 unicyclic 為 6,212,275 bytes、SHA
`bb2ee2dced4f7c7e695c50bc37da68474fbe430a34ff3a16dd09eff1c66dbce4`；
rank2 為 3,394,766 bytes、SHA
`798dcd066633d542c287e75c26adf3a7b4edf9b1591aa070d7721fde4fd20672`。
本輪主 custody report 應從 archive 核對這些 bytes，不能把本檔 metadata
filter 說成新的完整染色重播。

原 unicyclic receipt 記主 normal/seed17 exit 0 且一致，獨立 normal/seed17
exit 0 且一致；其 mathematical SHA 是
`2bb83ff21becff13042b4fcefa10085ce3bb1c059fbd6f98470b263a0d91b99a`。
原 rank2 主／獨立 normal/seed17 同樣通過且一致；mathematical SHA 是
`daf4b2524be46c2615202ddc42430eb11be7d0329bfd3aa4c529a6be0fb0c326`。
這些是保留的歷史驗證，不是本輪新跑的宣稱。

## 7. 採納界線

本審閱接通三支共同的 `ρ(F)≥3`。後續 rank3/rank4 由本輪另項審閱承擔；
本檔不單獨宣稱 `ρ≥5`。低圈秩範圍沒有殘留 singleton、普遍 4CT screen、
一般 C4 代表或代表存在缺口。其數學輸入仍包括新 no4ct 上游明列的有限
目錄／計數／plantri 信任；不把它們說成已 Lean 形式化或重新外部計算。

真正目錄外來源仍未構造；來源排除來自已接通的紙面覆蓋與有 custody 的
原有限結果，並非 `not triggered`。本輪不展開圈秩五／六，不處理一般九點
W5 代表，也不擴大到 N2、edge-critical、Gallai 或任意 annulus 來源。
