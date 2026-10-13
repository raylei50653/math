# W5-NO4CT-BRIDGE：合併定理與證據範圍的獨立終審

2026-10-13。審查者：本輪 rank-four reviewer，重新閱讀根層 `PROOF.md`、
`DEPENDENCIES.md`、全部三份 branch reviews、`evidence.py`、
`validation/normal.json` 及所連結的原低圈秩結構。只新增本檔；沒有修改根層
證明、原材料或任何舊 seal，沒有新增染色枚舉。

**判定：PASS。未發現需要保留 OPEN 的低圈秩數學缺口、未覆蓋分支或證據
範圍過度宣稱。可以採納三支共同、任取合法全內部 induced W5 的條件定理
ρ(G[P])≥5。** 此 PASS 仍承接根層已明列的 no4ct 上游有限計算信任及
歷史完整染色 receipts；不是從零重建其外部證明或全部有限染色。

## 1. 本次檢查的確切版本

| 檔案 | SHA-256 |
|---|---|
| `PROOF.md` | `22b472026cc2e53dd0fc2fa04c171abdfaff9057ba03bb1778d93d4bea56918d` |
| `DEPENDENCIES.md` | `e3affe763fbdc8ebbec633c2cf16f75d87f53b07e248edfa827a1e95657d33c2` |
| `evidence.py` | `625db4891f709ec06c16a3bc365df13405e8e2093157983b51a0937b8e7d7bab` |
| `validation/normal.json` | `3346b3fa08728a2fb760bb687cfaaede4240223d9cbd39b336d70460249c5abf` |

本審查對根層 PROOF／DEPENDENCIES 的18個 Markdown連結逐一檢查實際檔案，
有fragment者另核對標題slug，均存在且吻合，包括 no4ct交接§2及本輪ATT-U
定位。這是本次新執行的輕量文件核對，不是染色核對。

## 2. 局部 L 與 no4ct 前提接點

L 足以承擔原分類，讀作定理已固定之有限簡單原 G 與合法 W5 中的資料：
指定兩個 induced C5 faces、其他原面三角、私人完整degree≥5、每環相鄰
至多兩附件及大小下界。它未混入私人degree≥5、私人連通、singleton支援、
N2或普遍 exterior screen。K132 membership及共同色框在最後矛盾另明列，
沒有錯把它們當作 L 內的純幾何命題。

CAP-REL 對每個原 C4／proper C5 有 i(C)≥1，故s≤k−i(C)<k；此界保留
接觸外框的環，並未要求完全內部。原B點不能嚴格落在一個原內部cap。
受限C4引理因此可用；proper C5則用全域最小性。保外B完整關係只依同一
literal介面指派的延伸存在性，不宣稱兩個不同cap的fibres等量。

ATT-B以空原C4填滿原b的內側sector，推出完整d_G(b)=3的矛盾。
ATT-U用原x-ui-v-uj四環兩側各一段非空U開弧；任取合法W5的盤與中心
ownership足以保證此Jordan論證。這兩個新前提接點與mask無關，包含932。
新k≥16給r≥10，嚴格強於全部舊域起點。proper C5、無occupied triangle
用於上游來源結構與存在性，在L已得到後不再需要放進低圈秩模板引理。

合法W5存在與任取量詞沒有混淆：根層先引用存在，再對任意合法原輪盤供應
同一L。全域目錄外最小性亦未降成固定mask最小性。

## 3. 面位置、圈秩零至四的覆蓋

一般計帳的e(A)、annular面数、PPP／兩私人／同環兩pins／BUP分類逐項
一致；bridges按兩側計incidence。沒有將q個獨立環誤當q個原三角面。
F的有界面數為q；連通U/v只占一面，其餘有界面不能有刪去的G點或原邊，
故本身是PPP原三角面。多邊界、slit和巢狀分量候選由原面條件排除，
不因預先省略而消失。U/v所在面給原embedding中互斥窮盡的FACE-SPLIT。

逐分支核對如下：

| 圈秩／分支 | 根層實際論證 | 審查 |
|---|---|---|
| 0 | contractible式r≤10−2c−a≤8與r≥10矛盾 | 純紙面；不需要消費舊森林染色 |
| 1 contractible | 唯一PPP三角block至少三個不同ear／leaf charges，另加所有樹分量，超過M=2c | 保留原附樹與所有分量；PASS |
| 1 essential | c=1,M=0排leaf，F為纯C_r；r≤10迫r=10；兩側原fans得到252個舊word | 原十pins／附件完整；PASS |
| 2 essential | c=1,M=0、excess二，但PPP三角三個角各至少一excess | 所有essential幾何位置同時排除；PASS |
| 2 contractible | 四類2-core覆蓋；三角blocks的charges排分離雙環、figure-eight與barbell；theta迫diamond。等號迫ear tails及path分量，新大小迫c=1,r=10,a=0 | 70個舊模板完整子域，無需小代表；PASS |
| 3 contractible | q≤4及完整degree使原F outerplane；block／ear預算只留pentagon fan及兩ear tails | 新域484，與原摘要一致；PASS |
| 3 essential | PPP兩面共邊成diamond，excess四迫唯一原ear-to-ear外路 | 新域790，保全部subdivisions；PASS |
| 4 contractible | 完整hexagon型與block分配／ear等號，保留H、DD、H+P、DD+P、D+D | 新域2,955；原共ear、橋長、tails與方位無遺漏；PASS |
| 4 essential | 三PPP面clusters含共兩非相鄰tips的分支，excess六迫pentagon fan及唯一原外路 | 新域2,368；短側B/U與apex一／二附件皆保留；PASS |

q≤4 contractible下「不incident無界面則d_G≤q≤4」是有效的共同outerplane
論證；它也替rank-three block分類提供直接局部理由。所有完整degree界
仍指G；只有使用d_G=d_F+d_T及原面sector後才得私人degree限制。

Contractible crosscuts的region分類包含p=1同一原邊的兩sides及共endpoint
情形。每分量兩個M面與每region最多兩個M面，配合沒有私人分量可跨crosscut，
使全部components及terminal triangles均落入原strip參數。每條環邊唯一
annular incident面迫共同方向及各五步，排除了漏附件或獨立反U的自由度。
Essential原外路的長度和所有細分點亦全數保留。

最後source-to-template是同一原帶嵌入圖同構，g_B／g_U共用ε；全部A/G
full lifts按同一bijection搬運，空fibres也保留。新來源的完整Σ先被證落入
舊模板域，才使用其membership；不存在以「模板Σ在K」直接假設来源覆蓋的循環。

## 4. 證據程式與 normal receipt 的實際範圍

`evidence.py` 消費42份按BASE逐bytes凍結的proof inputs，讀取七份原
DELIVERY／MANIFEST，逐條核對407項sealed records。封存路徑由BASE
`audits/ARCHIVE.json`定位；壓縮blob及解壓原內容都核對SHA與bytes。
曾被舊rank3-C seal綁定的共享docs使用另存歷史gzip，而不是拿今日docs
假冒舊bytes。這與「不改寫舊seal」的要求一致。

程式從固定cells取得K132，重新核對完整C5 pattern order及全部D5作用
封閉，並核對932／933／941不在K。舊summary的所有masks均直接核對在K，
所以rank2原先以小代表排除的四種mask在此可合法改用同一目錄membership
矛盾；沒有引用任意一般W5代表。

`validation/normal.json`的數字彼此一致：七份原證據共15,510必要模板；
r≥10 metadata子域向量為
`[0,252,70,790,484,2955,2368]`，和為6,919。森林摘要沒有mathematical
SHA而記null；該分支本輪採純紙面矛盾，且摘要本身仍受原seal綁定。

程式明寫`colouring_enumeration_replayed=false`、coverage由紙面及reviews
承擔、真正最小來源not triggered、沒有新Lean theorem。它核對歷史正常／
seed17／獨立receipts的bytes，而非重新執行或重新解讀所有舊染色；根層
「沿用有限完整證書、按原SHA接合」的文字與此一致。此審查也未另重播
證書內容；採納的是bytes未變及既有完整計算結果。

## 5. 最終結論與停止點

對任意合法原W5反設q≤4，每種q及兩個原面位置均已被紙面矛盾或來源到
凍結必要模板同構覆蓋；D5封閉把canonical完整Σ∈K搬回原B。因來源Σ∉K，
遂得q≥5。這個最後矛盾不依賴933／941專用singleton identities，亦不需
先證932一般排除，因此是三支共同的no4ct條件定理。

根層保留一般q≥5來源縮減、無界三支與K∞=K≤5的OPEN界線，沒有聲稱
普遍九點W5代表、跨不同圖R³／fibre重數等價、rank-five／rank-six搜尋或
Lean形式化。終審無需另列未修復具名引理；沒有要求修改原根層證明。

## 6. 終審後的 checker 延伸附記

本節追加於前述歷史審閱之後；原§1的版本SHA及當時receipt保持原文。
新增檢查的 `evidence.py` SHA-256 為
`305be32de628f26ea86cdd5641c2ba9c941f2d4c164252d175c229fdf2394bfa`。
`PROOF.md`、`DEPENDENCIES.md` 的bytes及上述SHA均未變。

**延伸判定：PASS。** 新增部分只讀原 rank1、rank2、rank3-essential、
rank3-contractible 的 `controls/templates.json`，以記錄的 `r` 或
`parameters.r` 篩出r≥10；四個索引都在原sealed records中。
所選記錄數與原summary子域數一致，逐份索引Σ亦核對K membership；
rank1／rank2另assert全部為1023。沒有生成新圖、重算fibres或重播染色。

新 `validation/evidence-normal.json` 與 `validation/evidence-seed17.json`
逐bytes相等，兩者SHA-256均為
`f8646fd628605b2073d543771a0feaeafca0a6dad871d2f86757022d4fb560c7`。
它們明列索引子域結果252×1023、70×1023、790×1023、484×1023；
rank4兩支仍以原全域membership及summary大小域接入，沒有新增其索引mask
宣稱。舊模板總數15,510、metadata子域6,919及407筆sealed records不變。
本節實際另核對兩份receipt的bytes相等與四個索引皆受原seal綁定，未再次
執行歷史染色搜尋。

新增 `REPORT.md` 的定理量詞、必要模板／metadata子域區分、no4ct上游信任、
未重播染色與OPEN停止點，均與已審PROOF及此checker延伸一致。報告列的廣泛
文件檢查、負控制與交付seal由各自VERIFICATION承擔；本附記不把那些命令
宣稱為本reviewer另跑的測試。原最終定理採納及本審查的範圍保持不變。
