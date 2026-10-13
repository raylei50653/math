# W5-RANK4-C：contractible 私人圈秩四完整排除

2026-10-13。固定 BASE **acd2b1beea6c909edade565a00eeeeac05d2b3a7**。
本輪成果判定 **A — 完整排除**：

\[
\boxed{\text{完整最小目錄外 disk-}C_5\text{ 來源，不存在 contractible 的 }\rho(F)=4.}
\]

證據由**任意來源的紙面完備化約＋完整有限 Python 證書**組成；不是純紙面
染色證明，也不是由搜尋未找到反例而推出。沒有新增 Lean theorem。
**essential 圈秩四仍 OPEN；一般私人圈秩下界仍為四，K∞=K≤5 仍 OPEN。**

## 1. 來源契約、隔離範圍與依賴

G 在全部完整外框關係不屬 K132 的 disk-C5 圖中先最小化內點數 k，再
最大化邊數。任取合法全內部 induced W5，保留原中心 v、原外框 B、原
鄰環 U、十個有序 pins、原 rotation、原面、bridges、cut vertices 與
全部 subdivisions。令 P=V(G)\(B∪U∪{v})、F=G[P]、r=k−6、c=c(F)。
本輪反設 ρ(F)=4 且 U/v 在 F 無界面。

不增加 N2、edge-critical、Gallai、F 連通或縮減代表假設。沿用 BASE 的
K≤13=K≤5，故 k≥14；沿用任取合法 W5 的 ρ≥4。來源正規形、degree、
原 C4 cap 與每環附件界的精確依賴在 [FORMULAS](structure/FORMULAS.md)。
22份直接輸入依 BASE 保存，Markdown 用可逆 gzip 防止新增 DocGraph
重複節點；原 bytes、git blob 與壓縮 bytes 的 hashes 均在 [BASE](BASE.json)。

本輪只新增本 audit；本輪不修改舊證據、舊 seals、共享文件或真實 Git index。
沒有 commit、push、PR 或 merge。W5正式主線導航沿用 BASE 狀態；本報告
是本輪獨立交付入口，未將獨立 audit 寫入既有原始證據。

## 2. 新證明的一般計帳與分量界

設 t_P 為 PPP 原三角面數，a 為全 terminal 原三角面數，p 為 B–U 原邊數，
M 為 BUP 原三角面數。逐原面／原邊 incidence 重新證明

\[
M=2(c-\rho+t_P),\quad p=a+c-\rho+t_P,\quad
\sum_{x\in P}d_G(x)=4r+10+\rho-c-p.
\]

contractible 使每個有界 F 面恰為原 PPP 三角面，包含不連通及 slit 的
情況，故 t_P=ρ=4。於是 M=2c、p=a+c，並得到

\[
\boxed{8\le r\le14-2c-a},\qquad
\sum_{P}(d_G-5)=14-2c-a-r.
\]

每個私人點在 B/U 各至多兩個相鄰附件；完整 d_G≥5 排除孤立點。c≥4
已與 r≥8 矛盾。c=3 迫 r=8,a=0，各分量至少兩點，大小只能4+2+2或
3+3+2，最多8或7條私人邊；但圈秩四要求9條，矛盾。因此正式得到：

| c | 私人點數 r | 來源內點數 k | 全 terminal 面 a |
|---:|---|---|---|
| 1 | 8≤r≤12 | 14≤k≤18 | 0≤a≤12−r |
| 2 | 8≤r≤10 | 14≤k≤16 | 0≤a≤10−r |

此表由紙面證明得到，沒有直接採用任務描述為定理。

## 3. 完整 cyclic-block 分類與原附件覆蓋

[CORE](structure/CORE.md) 證明不 incident F 無界面的私人點完整 degree
至多四，故 F 在**原嵌入**中 outerplane。每個 cyclic block 的有界面
全是原三角面；rank h 的 block 满足 b+2i=h+2。rank≤4 的完整清單是
triangle、diamond、五邊形 fan、K4，以及 rank4 的三種六邊形三角化、
四角錐、帶一個內點的三角化四邊形。含內點者由完整 degree 排除。

對含 m 個 cyclic blocks 的分量，block-cut skeleton 至多用2(m−1)個
ear incidences；每個未用 ear 或其附樹 leaf 注入一個不同 BUP 面。因此
全圖 M≥2c+Σ(ear數−2)。因 M=2c，所有 triangle blocks 與三-ear
central hexagon 排除，從而排除3+1、2+1+1、1+1+1+1的全部 block 分配。

等號進一步排除非 ear 附樹、分叉附樹及 branching tree components。
恰剩下列五族；tails 可空，所有原橋與細分點均保留。

| 族 | 完整私人形狀 | 必要模板 |
|---|---|---:|
| H | 一個兩-ear hexagon（fan或zigzag），兩 ears 各一 tail | 4,256 |
| DD | 兩 diamonds 共 ear 或經 ear-to-ear 原橋路徑連接，另兩 ears 各一 tail | 1,665 |
| H+P | H 分量加一個非平凡 path 分量 | 212 |
| DD+P | DD 分量加一個非平凡 path 分量 | 4 |
| D+D | 分開的兩個 diamond 分量，各有兩條可空 ear tails | 252 |
| 合計 | c=1：5,921；c=2：468 | **6,389** |

[ATTACHMENTS](structure/ATTACHMENTS.md) 由每分量恰兩次原 terminal
切換推導兩側 contour，再由全部原 B–U crosscuts 推導完整 strip/triangle
循環次序。兩環各精確前進五條原邊，得到 E/D/H0–H3 atoms、全部 letters、
side bits 與 terminal triangle words。反向逐面構造恢復**同一原圖**。

特別保留 DD 共 ear 的同一原點（其完整 degree至少六）、兩種 hexagon
方向、fan apex 至少一個 terminal、c=2 的 DD+P 四份及各原 subdivision。
這是對任意 k 的結構分類；有限模板大小來自已證上界。

全部模板的私人完整 degree≥5；B全度數≥4及U全度數≥5的組合另保存：
兩者都成立5,573份，僅前者396份，僅後者396份，兩者皆否24份。保留這816份
形成必要域超集，沒有把必要條件稱為充分條件，也不宣稱任何模板是最小來源。

## 4. 完整十列、空 fibres、全部 lifts 與目錄排除

[certificate.jsonl.gz](controls/certificate.jsonl.gz) 逐份保存 literal
原邊、A/G faces、rotation、B/U pins、中心、components、完整 G/F degrees、
十個固定 β rows、每列全部1,024個 literal U cells，以及全部 A/G full lifts。
非法 U 色列也保留為空格。沒有投影成 marginals，沒有獨立正規化 U 或私人分量。

主程式用 MRV DFS 直接枚舉 A 與 G，另核對從 U三色 cells 補回中心的結果；
獨立 checker 從 neighbours 重建原邊、由 rotation walk 恢復原面，用固定
U→中心→私人點次序直接枚舉完整染色。所有列表逐字相同。

| 完整 Σ | 511 | 639 | 767 | 895 | 1019 | 1023 |
|---|---:|---:|---:|---:|---:|---:|
| 模板数 | 3 | 30 | 3 | 1 | 1 | 6,351 |

六種皆在固定 [K132輸入](CATALOGUE_INPUT.json)。兩套程式亦確認全部132個
masks 在外框 D5 搬運下封閉；來源 pin map 保共同方向、各環原起點及同一
全局 palette。因此每個原來源的完整 Σ 也在 K132，與目錄外身份矛盾。
這一步完成 contractible rank-four 的全部排除，沒有使用較小代表。

| 完整核對項 | 數量 |
|---|---:|
| cells | 65,423,360 |
| 空 fibres | 63,749,179 |
| A full lifts | 3,343,426 |
| G full lifts | 1,645,614 |

canonical解壓內容的 SHA-256：
`d72dcbdab3fbb00ac79344d7645ff0921f89fa798030e76fd9ed51bdd6b4ee8d`。
摘要與逐圖索引見 [summary](controls/summary.json)、[templates](controls/templates.json.gz)。

## 5. 獨立核對、負控制與可重播證據

[獨立紙面與程式審查](review/REVIEW.md) 核對任意來源覆蓋、pin搬運、
source degree超集及全部6,389個 parameter keys；兩套枚舉分別使用固定
rooted gadgets與非交叉 chords，原邊分別從faces與neighbours重建。

主 normal與seed17重播一致；seed17同時改變MRV tie order與色彩搜尋順序，
不只是更改hash seed。獨立固定次序DFS亦逐圖核對全部fibres與lifts。
14種內容破損由兩套validator各拒絕一次，共28次，包括漏原邊、錯rank/M、
錯pin/rotation/U面、漏分量、G/F度數混淆、錯degree/catalogue flag、漏A/G
lift、偽造空fibre及漏row；另由實際coverage checker拒絕缺一模板。

五族各有一份完整正控制。另存一份完整 prism 的全部染色，與本輪Σ=1023
模板在一個三色U fibre的支援不同，構成**同Σ但不同R³**反控制。
所有負控制材料見 [negative-results](independent/negative-results.json) 與
[prism-control](independent/prism-control.json.gz)。最小目錄外實例為
`not triggered`；必要模板和驗證控制為`triggered and holds`；保存強度
控制為`counterexample`。來源排除依靠完備化約，絕非零實例觸發。

第一版負控制正控制比較漏補證書的 `Sigma_in_K132` metadata，故未完成生成；
原失敗log保留於[negative-generate](logs/negative-generate.log)。補齊該欄
並另加破損測試後，v2生成及只讀重播通過；未覆寫任何失敗證書或舊證據。

由 repository 根目錄執行以下只讀重播：

```bash
python3 -B audits/2026-10-13-w5-rank4-contractible-acd2b1b/controls/check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-w5-rank4-contractible-acd2b1b/controls/check.py --check --seed 17
python3 -B audits/2026-10-13-w5-rank4-contractible-acd2b1b/independent/check.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-w5-rank4-contractible-acd2b1b/independent/check.py
python3 -B audits/2026-10-13-w5-rank4-contractible-acd2b1b/independent/negative.py
python3 -B audits/2026-10-13-w5-rank4-contractible-acd2b1b/controls/catalogue.py --check
python3 -B audits/2026-10-13-w5-rank4-contractible-acd2b1b/review/domain_check.py
python3 -B audits/2026-10-13-w5-rank4-contractible-acd2b1b/verify.py
```

`--write` 僅供新目錄exclusive-create生成；現有證書重播應用 `--check`。
全部程式使用 Python standard library，不新增套件依賴。

## 6. 文件、儲存、Lean與信任界線

正式文件、audit連結及正式DocGraph檢查、儲存工具測試、臨時index的全套
儲存政策與 `lake build` 的實際命令／結果見 [VERIFICATION](VERIFICATION.json)。
主證書約29 MiB gzip、索引約287 KiB gzip；没有大於1 MB的未壓縮新JSON。
儲存检查只在 `/tmp` 的index/object目錄加入明列新audit文件，真實index不變。

系統Python初跑工具測試因缺既有networkx依賴而失敗，保留原log，改以專案
`.venv/bin/python`補跑。收尾時出現無關atlas並行變更，另記於
[concurrent-worktree](validation/concurrent-worktree.json)，未被本輪編輯或納入臨時index。

全域 DocGraph 的 **62項既有duplicate-ID錯誤**單獨保存 BASE／final logs，
不修復舊項、不改稱全域通過，也不計作新研究失敗。`lake build` 通過是
既有Lean回歸，未形式化本輪紙面或Python完備枚舉。新seal及原輸入核對
見 [DELIVERY](DELIVERY.json) 與 [verify.py](verify.py)。

證據層分開：紙面是原圖計帳／blocks／附件覆蓋；有限Python證書是上述
6,389份的完整Σ membership；外部依賴沿用固定BASE來源链的4CT及有界
計數結果（本輪未重跑外部證明）；Lean没有新theorem。K132與K≤13的上游
證書沿用固定BASE，不把本輪重播聲稱為重建整份上游目錄。

## 7. 精確剩餘與下一個最窄問題

本輪 contractible ρ=4 沒有來源殘留。在完整最小來源、任取合法 W5 的
量詞下，現在可說 **ρ=4若出現，F必含分隔B/U的essential環**。
BASE 的essential定理僅排除ρ=3，尚不足以提高一般下界為五。

下一個窄題為 **W5-RANK4-E：essential 圈秩四完整分類與排除**。先核對
一般面式在essential域的專用值、含U的原F面及其boundary walks；保留
全部PPP faces、blocks、cutvertices與bridges，再給來源到有限必要域的
完備證明。不得直接套用本輪outerplane、M=2c、兩切換或H/DD條帶結論。

一般annulus小代表、保R³縮減、一般私人圈秩≥5及K∞=K≤5全部保持OPEN。
Closure scope只到contractible rank-four。直接父題的ρ≥4仍正確，故
不改寫舊rank-three報告或seals；本輪隔離交付的導航停在此報告，沒有發布。
