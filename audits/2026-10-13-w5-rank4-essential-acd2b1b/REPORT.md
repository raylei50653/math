# W5-RANK4-E：essential 私人圈秩四完整排除

2026-10-13，固定 BASE **acd2b1beea6c909edade565a00eeeeac05d2b3a7**。
本輪結果 **A — 完整排除 essential ρ=4**：在完整最小目錄外 disk-C5
來源契約下，任取合法全內部 W5，若私人 F 含分隔 B/U 的 essential 環，
則 **ρ(F)≥5**。證據是任意來源的紙面完備化約＋完整有限 Python 證書。
沒有新增 Lean theorem，一般 K∞=K≤5 仍 OPEN。

## 1. 原圖契約與紙面完備化約

保留同一原 G、原中心 v、十個有序 B/U pins、原邊／面／rotation、私人
分量與全部 subdivisions。G 先最小化來源內點数 k 再最大化邊數；不增加
N2、ε、edge-critical、Gallai 或 F 連通假設。所有 degree 指定為完整 G
或私人 F，不混用。完整論證見 [PROOF](structure/PROOF.md)。

一般原面式在 essential ρ=4 下給 c=1、a=p=M=0、三份 PPP 原三角面、
8≤r≤13、δ(F)≥2、每個 PPP 面點私人 degree≥3，以及總私人 excess 六。
完整檢查三面依原邊 adjacency 的全部 clusters，包括 diamond 與第三面
共享兩個非相鄰 tips 的易漏分支，排除除了三角化五邊形 fan 的所有形狀。
私人 excess 等號迫兩 ears 由唯一原外路徑相接，其他原點全 degree 二。

原嵌入再迫短側 apex 接一或兩 terminals，長側兩點各接兩個 terminals。
保留短側 B/U 兩種方位；原兩環各精確走五條邊，得到完整 word domain。
這是任意來源到模板的帶 pins／rotation 同構，沒有縮減或更換原圖。

[獨立紙面審查](review/e_arc2_gap_review.md) PASS；另有不導入生成器的
[三角面／係數核對](review/triangle_and_count_check.py)與
[结果](review/triangle_and_count_results.json)。它們是論證與有限域的
額外核對，不代替原面的紙面覆蓋或完整染色。

## 2. 完整 fibres 與結果

| r | 8 | 9 | 10 | 11 | 12 | 13 | 合計 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 必要模板 | 96 | 408 | 840 | 912 | 504 | 112 | **2,872** |

全部模板完整 Σ=1023，原 B 的 D5 pin 拉回仍然全收十列，故與目錄外
來源身份矛盾。全部模板也滿足 B degree≥4、U degree≥5，但仍是必要域
超集；未證模板具有真正最小來源身份。

[完整證書](controls/certificate.jsonl.gz)逐圖保存原邊／faces／rotation、
十 pins、中心 ownership、G/F degrees，以及十個 beta rows 每列全部
1,024個 literal U cells、空 fibres、全部 A/G full lifts。主 checker
直接枚舉 G，再核對從三色 U 的 A lifts 補中心所得完整列表；獨立 checker
用不同的 increment recursion／neighbours 構造、rotation walk、固定
U→中心→私人點 DFS，逐格逐份比較。沒有只比較 masks 或 marginals。

| 項目 | 數量 |
|---|---:|
| cells | 29,409,280 |
| 空 fibres | 28,345,408 |
| A full lifts | 2,051,516 |
| G full lifts | 1,017,324 |

canonical 解壓證書 SHA-256：
`621fc7c1c57bdcb3917943d03911d768cd251e37cd570087cff191bdd0436f26`。
[summary](controls/summary.json)保存相同 receipt。

## 3. 冻結輸入、獨立性與重播

[BASE](BASE.json)區分固定 HEAD 的數學來源與 exact working-tree snapshots。
rank4-contractible 尚未追蹤的 REPORT／結構／checker／summary 已按當時
bytes 冻結；它不是本 essential 證明的前提，合併結論須另行審查採納。
舊 rank3-essential independent checker 也存在於工作樹但不在 HEAD，故
明列為工作樹**演算法**依賴。新主／獨立 checker 的幾何和有限域分開實作；
染色核心分別沿用已凍結的 MRV 與固定次序 DFS，沒有聲稱從零第三方實作。
所有 Markdown 輸入可逆 gzip 保存以免增加重複 DocGraph 節點。

normal、真正改變 MRV tie／color search order 的 seed17、独立全部
fibres／lifts 重播相同。四個 d／方位正控制通過；十四種破損由兩個
validators各拒絕，共二十八次，另由完整 coverage validator 拒絕缺模板。
正控制／反控制見 [negative-v2-results](logs/negative-v2-results.json)。

第一個 freeze 嘗試發現舊 independent checker 不在 HEAD，之後改以明示
工作樹 snapshot 保存。第一個獨立 replay 對反向方位使用了過強的 face
陣列起點相等測試；改成有向 cyclic face 相等，ordered pins 與原證書
均未改。[失敗記錄](logs/independent-v1-failure.txt)保留原因。
這不是漏邊修補或更換來源。舊證據和既有 seals 沒有改寫。

從 repository root 只讀重播：

```bash
python3 -B audits/2026-10-13-w5-rank4-essential-acd2b1b/controls/check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-w5-rank4-essential-acd2b1b/controls/check.py --check --seed 17
python3 -B audits/2026-10-13-w5-rank4-essential-acd2b1b/independent/check.py
python3 -B audits/2026-10-13-w5-rank4-essential-acd2b1b/independent/negative.py
python3 -B audits/2026-10-13-w5-rank4-essential-acd2b1b/review/triangle_and_count_check.py
python3 -B audits/2026-10-13-w5-rank4-essential-acd2b1b/verify.py
```

生成器 `--write` 使用 exclusive-create 且拒絕覆寫。完整命令／exit status
見 [VERIFICATION](VERIFICATION.json)，交付 bytes 見 [DELIVERY](DELIVERY.json)。

## 4. 採納邊界

本輪 essential 結果本身完全排除ρ=4。若另行完整審查採納已凍結的
rank4-contractible audit，兩個互斥拓撲分支才共同推出
**任取合法全內部 W5，ρ(G[P])≥5**；本報告不代替該父層採納。

真正最小目錄外來源為 `not triggered`；所有必要模板／驗證控制為
`triggered and holds`，破損控制被拒絕。來源排除依靠完備化約＋全模板
Σ=1023，不從零實例推出。沿用 K132、K≤13、4CT及外部計數的既有信任
範圍；沒有重建上游全部證明，沒有新增 Lean theorem或宣稱縮減代表／R³
等價。ρ≥5的一般排除、一般 annulus 小代表與 K∞=K≤5仍 OPEN。

本 audit 只在其 exclusive 目錄寫入；未改共享文件或他人證書，沒有
commit、push、PR 或 merge。文件整合、既有 rank4-C 採納及廣泛 repository
回歸由父任務另行記錄。[E-ARC2觀察](review/earc2-observations.md)僅是
獨立 reviewer 的非採納研究筆記，不是本 W5 定理依賴。
