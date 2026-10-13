# W5-NO4CT-BRIDGE：圈秩三兩支的來源覆蓋審查

固定本輪 BASE `d521163`。本審查只寫本檔；舊 BASE、證明、seal、模板與
完整染色證書均保持原 bytes。結論是 **PASS：兩個 rank-three 分支均可接到
新 no4ct 的 932／933／941 全域最小來源契約**。這是逐項前提替換與原圖
覆蓋的紙面審查；沒有重跑舊完整染色，也不是直接把舊 theorem 的 4CT 前提刪掉。

## 1. 被接入的精確條件命題

G 是所有完整關係不在 K132 的有限簡單 plane disk-C5 圖中，先最小化
原 B 內點數 k、再最大化邊數的來源。任取合法全內部 induced W5，中心 v
的完整鄰集為原循環 U，B/U 十 pins 互異，U disk 恰含 v 及五個原三角面。
置 A=G−v、P=V(G)\(B∪U∪{v})、F=G[P]、r=|P|、c=c(F)、q=ρ(F)。

本檔接入的是 `q≠3`，包含 U/v 位於 F 有界面、無界面的兩支。
若本輪其他檔案已接通 q≤2，才可合併讀成 q≥4。
圈秩四排除及 q≥5 的合併結論由各自審查承擔。

## 2. 實際所需共同前提及 no4ct 來源

上游定位為
[frontier W5 PROOF](../../2026-10-13-c5-no4ct-frontier-6943561/w5/PROOF.md)
與 [DEPENDENCIES](../../2026-10-13-c5-no4ct-frontier-6943561/w5/DEPENDENCIES.md)。
它們的原 BASE 是 `6943561e644e7598342d1ccd7df44dac0ebcd5cf`。

| 圈秩三實際使用的命題 | 新契約如何供應 | 三支範圍 |
|---|---|---|
| A 簡單 plane annulus；B/U induced C5，其餘面三角化 | frontier §1 的來源正規形，加上任取合法 W5 的原五面 ownership | 932／933／941 共同 |
| r≥7 | frontier §1 給 k≥16，實際 r=k−6≥10；這蘊含舊起點而不修改舊證明 | 共同 |
| 私人點完整 d_G≥5 | frontier §1，來源原內點 degree 定理 | 共同；絕非 d_F≥5 |
| 每個私人點對 B 至多兩個相鄰附件 | frontier §4；只用原 C4 無內點、B induced 及 B 點完整 degree≥4 | 共同 |
| 每個私人點對 U 至多兩個相鄰附件 | 下列 U-C4 原圖論證；只用 frontier §3 的原 C4 無內點與合法 W5 | 共同 |
| 每個原 C4 有界內部皆空 | frontier §§2–3：相對大小 s<k 的 C4 完整關係代表與 cap degree 計帳 | 共同；沒有普遍 C4 screen |
| proper C5 內部空或恰一個 W5 中心 | frontier §§2–3：相對大小與 K132 witnesses | 共同；僅作 essential 小環交叉檢查，非圈秩三模板化必要輸入 |
| 模板完整 Σ∈K132，K132 對整圖 D5 pin 拉回封閉 | 原 finite certificates、K132 實際 witnesses 與 membership receipt | 不需 singleton support，也不需 933／941 專屬身份 |

**U-C4 附件論證。** 設私人 x 同接 U 中非相鄰 ui、uj。原簡單四環
`x–ui–v–uj–x` 的兩條 v spokes 在 v 的 rotation 中把其餘 U 點分成兩條
非空的開弧。因 x 在 U disk 之外，這些弧的內點各位於四環的不同側；
四環的有界側因此含至少一個原 U 點，違反原 C4 無內點。故沒有非相鄰
U 雙附件；U 是 C5，所以至多兩個，雙接相鄰。此四環本身使用四個原內點，
若追溯受限 C4 代表，其有界 cap 私有點數 s≤k−4<k，大小限制確實滿足。

**原 B-C4 不是額外的來源假設。** x 接 B 的非相鄰 a,c 時，取短弧
a−b−c。原四環 a−b−c−x−a 的有界 cap 至少有 x 這個原內點位於介面，
故 s≤k−1<k。無內點及 B induced 迫唯一 diagonal bx，填滿 b 的內側
sector；d_G(b)=3 與已證 d_G(b)≥4 矛盾。這已由 frontier §4 供應。

兩環附件界給 d_T(x)≤4，因 x 不接中心 v，故
`d_G(x)=d_F(x)+d_T(x)`。只由這一步推出 F 無孤立點；私人 leaf 若存在則
恰接兩環各兩個相鄰 pins。不能直接假定私人無葉或 d_F≥5。

舊 essential 證明 §1 的 4CT 信任聲明是當時取得上述輸入的歷史路徑；
本次逐條以 no4ct 定理替換。其 §§2–6 及 contractible 的實際面式、block、
原附件和有限 membership 論證均沒有剩餘普遍 4CT 引理，也沒有只對
933／941 成立的 colouring support 引理。

## 3. 兩個幾何分支確實窮盡

F 是保留全部私人原點與私人原邊的 induced plane 圖，開始不假定連通。
連通的 U∪{v} 與 F 不交，所以位於 F 的同一個面。B 在 F 無界面。
若 U/v 所在面有界，該面的外邊界包含一個分隔 U 與 B 的私人簡單環；
反之任何此種 essential cycle 強迫 U/v 位於 F 有界面。
因此「有 essential cycle」與「U/v 在無界面」互斥且窮盡，並非只覆蓋
某個預先選出的 cycle basis。

F 有恰 q 個有界面。任何不含 U/v 的有界 F 面也不含 B；其 open region
沒有私人點，否則它們已屬 F。其餘 G 邊不能穿越 F 邊界進入，因此此面
恰是原 PPP 三角面。這同時排除空的多邊界面、bridge slit 或另一私人
分量藏在此面等情形；沒有先假定所有 F 面都是 disk。

置 h 為 PPP 原三角面數，a 為全 terminal 三角面數，p 為 B–U 原邊數，
M 為 BUP 原三角面數。只由原面 Euler、逐私人邊及逐 cross-edge 計數，

```
e(F)=r−c+q,
M=2(c−q+h),
p=a+c−q+h,
sum_{x in P} d_G(x)=4r+10+q−c−p,
r≤10+q−c−p.
```

這些式子不依賴來源 mask；每個 degree 是完整 G-degree。

## 4. Essential 圈秩三：全部原分量與 subdivisions 都被覆蓋

接入原
[structure/PROOF §§2–6](../../2026-10-13-w5-rank3-essential-45bc1c3/structure/PROOF.md)
及 [獨立審查](../../2026-10-13-w5-rank3-essential-45bc1c3/review/REVIEW.md)。
原 BASE 保持 `45bc1c3dc9dacaee1b10df9d64f1c6a27bb0e954`。

Essential 時 h=q−1，Jordan 分隔迫 p=0，故 `a=0,c=1,M=0`。
私人 leaf 的 terminal link 必有 B/U 切換，產生 M 面，因此沒有 leaf。
PPP 面上私人度二的點也須至少三個 terminal 附件，兩環皆出現而產生 M，
所以每個 PPP 面點私人度至少三。q=3 時 h=2 且
`sum(d_F−2)=4`，兩個 PPP 三角面恰共一條原邊，形成 diamond；四個
diamond 點皆私人度三，其他點皆度二。連通性遂迫其餘全部原邊恰是一條
連接 diamond tips 的路徑 Q；沒有額外分量、附樹、branch 或被刪除的
subdivision。共享邊兩端的 terminal sectors 分別只見 B、只見 U，完整
degree 及附件界迫各接相應環兩個相鄰 pins。

原計帳給 `7≤r≤12`；新來源實際 `10≤r≤12`。Q 的每個原點保留，
並由原兩側三角面建立共同方向的字 `(δB,δU)`。兩 tips 可用 00/10/01/11，
其餘点排 00；diamond 各環用一步，所以所有其他字的兩座標總和各四。
這正是舊完整域。它同時恢復十條 B/U 原邊、全部 Q 原邊、五條 diamond
原邊及全部 terminal 附件，沒有添加 tips 間的假想 gap 原邊。

原域有 1,283 描述，新 r≥10 只取其中 790 描述（440+280+70）。
引用舊全域每份 Σ=1023 的證據已足夠；不必重生域或重跑染色。
1023 在每個原 B 的 D5 拉回下仍為 1023 且屬 K132，因此直接違反
`Σ(G)∉K132`。舊文字在最後提及 933／941 不是必要輸入；加入 932 不改變
任何來源覆蓋步驟，也不要求新的模板。

## 5. Contractible 圈秩三：blocks、bridges 與所有 strip 分支

接入原 [FORMULAS](../../2026-10-13-w5-rank3-contractible-50d5474/structure/FORMULAS.md)、
[CORE](../../2026-10-13-w5-rank3-contractible-50d5474/structure/CORE.md)、
[ATTACHMENTS](../../2026-10-13-w5-rank3-contractible-50d5474/structure/ATTACHMENTS.md)
及 [CORE_REVIEW](../../2026-10-13-w5-rank3-contractible-50d5474/review/CORE_REVIEW.md)。
原 BASE 保持 `50d5474f2446403f3b3001d5943571184c8c9936`。

此支 h=q=3，所以 `M=2c,p=a+c,r≤13−2c−a`。舊 r≥7 配合無孤立點
已完整排 c≥3；新 r≥10 更直接迫 c=1，因 c≥2 便有 r≤9。仍可以接入
舊 c=1、c=2 全必要域，以保留原 seal 與來源覆蓋證據不變。

對每個含環 maximal block H，若其 bounded face 內藏其他私人点、block
或 bridge，該面 boundary disk 的原三角化擴成更大的二連通私人 block，
矛盾。因此 bounded block faces 都是原 PPP 三角形。若 block rank=h、
外邊長=b、嚴格內点=i，則 `b+2i=h+2`。h≤3 的完整清單恰是 triangle、
diamond、五邊形 fan、帶一內點的 K4。K4 內點所有 sectors 已是原空面，
故完整 G-degree=3，不合法。沒有將完整 degree 下界套在私人圖上。

跨 blocks 的連接樹保留原 cut vertices 和橋路徑。m 個 cyclic blocks
最多消耗 `2(m−1)` 個 block-ear incidences；未消耗 ear 本身或其附樹
的一個 leaf 各供應不同 M 面。由 M 預算排掉 diamond+triangle、三個
triangles、及 c=2 的 (2,1) 分配。等號迫唯一存活形狀為一個 pentagon
fan、兩 ear 各帶一條可空原路徑，以及 c−1 個非平凡路徑分量。所有
原 bridges、tails、cut vertices 和 subdivisions 都仍在圖中。

每個分量恰兩個 BUP 面，所以其原 contour 恰兩次 B/U 切換；每條
bridge 的兩側各走一次。Fan 短弧 apex 可在 B 或 U 一側，且該 apex
可接一個或兩個相鄰 pins，故四種 gap 步長
`(0,2),(1,2),(2,0),(2,1)` 全保留。長弧兩點各需兩個相鄰 pins。
無尾 ear／帶尾 ear、ordinary internal／leaf 的 letters 分別由完整
`d_F+2+δB+δU≥5` 決定，沒有私人 degree≥5 的偷換。

因 `p=a+c≥1`，全部原 B–U edges 可依 rotation 切成 cyclic regions；
允許共端點，也允許 p=1 的同一 edge 成為切開 disk 的兩側。每個 region
的兩個 boundary-edge sides 最多承擔兩個 M 面；每分量恰需兩個，因此
每個有私人點的 region 恰含一個分量。無私人點者無同環 chords 或內部
cross edge，恰為一個 BBU/BUU 原三角面。所有 strips 和所有 terminal
triangles 的循環次序都屬原參數域，兩環總前進量各精確五。

所以舊 2,270 必要模板仍覆蓋新來源。新 r≥10 僅落在舊 c=1 的 484
份（r=10 的 384、r=11 的 100）。舊 complete masks 為
`{91,511,639,767,1007,1021,1022,1023}`，全部在凍結 K132 中；原
[catalogue receipt](../../2026-10-13-w5-rank3-contractible-50d5474/controls/catalogue.json)
另核對其全 D5 拉回仍在 K132。這直接與目錄外身份矛盾，未使用某份
933／941 singleton row 可染，也未要求新 932 source 有任何既定 full lift。

## 6. 同一原圖、同一色框與證據重用

兩支的 source-to-template 都是完整原帶嵌入圖同構。兩環的 canonical
pin maps 是 `g_B(i)=s_B+εi,g_U(i)=s_U+εi (mod 5)`，共用同一方向 ε，
各起點可以不同；若原 U 採 face-boundary 方向，顯式保存固定換算。
所有私人點與中心逐點映回，沒有獨立正規化 U 顏色，也沒有拼接不同 rows
的見證。因此同構逐份搬運所有 A/G full lifts、全部空與非空 fibres；
最終排除只使用其完整 Σ∈K132。這個同構不減點，不是一份新小代表。

| 舊證据包 | 保留的完整染色數據與 mathematical SHA | 本次用途 |
|---|---|---|
| rank3 essential，BASE `45bc1c3…` | 1,283 模板；13,137,920 cells；A lifts 730,480；G lifts 352,020；`98ecc77b4b7affbd61dbdb5e84f7818f96f2128ff057dbe539de5e6c47d30a2c` | 原 normal／seed17／independent receipts，接入全模板 Σ=1023 |
| rank3 contractible，BASE `50d5474…` | 2,270 模板；23,244,800 cells；A lifts 928,404；G lifts 465,866；`4cab09423e33b04109669daed9f5c3388ade6486b9943f55ec0cd32bcb5edd2b` | 原 normal／seed17／independent／catalogue receipts，接入完整 membership |

原 essential [MANIFEST](../../2026-10-13-w5-rank3-essential-45bc1c3/MANIFEST.json)
記錄 gzip 證書 SHA
`201876d9dceab3a6e3fd675cb0e990b1eda80415c396177b22c00f7e654b8bd1`。
本輪 checkout 該 gzip 位於 archive，不能把其工作樹缺席報成重新染色失敗，
也不能把歷史 receipt 報成本輪再次完整枚舉。Root custody 檢查負責 archive
及本輪輸入清單；本 reviewer 未還原或改寫舊 paths。

本審查逐一閱讀原結構證明、必要域參數、獨立紙面審查、summary 及原
VERIFICATION receipts，採納其未變動有限內容；本次新增工作是 §§2–5
的 no4ct 前提與原來源覆蓋接入。沒有新 Lean theorem、真實目錄外 source
construction、普遍九點 W5 代表、rank-five／rank-six 枚舉，亦沒有新增
一般三支排除。rank-three 橋接本身沒有剩餘具名數學缺口。
