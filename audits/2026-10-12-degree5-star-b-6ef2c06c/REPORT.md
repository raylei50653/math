# 任務 B：同源 degree-5 star 的完整十列重接控制

2026-10-12。**固定域的 1,020 次合法單項操作，沒有一次保持完整 Σ。**
本包完成 132 份 literal catalogue witnesses 加上明示五輪 W5 的有限操作表、
完整 relations／空 fibres／full lifts、局部平面操作及可重播 checker。
這是重接條件的 soundness 控制；沒有排除任意大小來源，也沒有證明一般縮減。

BASE 為 `bc7c0820e6b5e585869b8a59e04f52da0dad2d33`。
授權入口是該 BASE 的 `docs/tasks/c5_degree5_link_tasks.md` 任務 B。
所有本輪產出只在本目錄；沒有修改共用文件、舊證書或其他任務，也沒有 commit／push。

## 1. 凍結來源與嵌入界線

[INPUTS.json](INPUTS.json) 保存 BASE 檔案副本、SHA-256、開始時 Git 狀態。
132 個 literal 圖依原 cofacial v2 證書及其 checker 的 `cells.json` 讀取，
全部原檔與凍結副本在開工時一致；沒有以 candidate masks 代替圖。
[DESIGN.json](DESIGN.json) 在重接著色計算前凍結
[紙面公式及候選條件](paper/CONTRACT.md)、[domain.json](controls/domain.json)、
標記規則及預期列數。
收尾時，共用任務文件及兩份上游說明已有本輪之外新增的外圈研究路由；
任務 B 規格未改。本包仍以凍結 BASE 驗收，不吸收那些新結論。
[CUSTODY.json](CUSTODY.json) 分開記錄 live 文件差異及零漂移的凍結副本。

**上游沒有保存歷史 rotation。** 本輪先依 literal edges，用固定 NetworkX 3.5、
排序 nodes／edges 及外側 apex 得到一份 disk embedding，移除 apex，再共同反射方向，
使具名 `(0,1,2,3,4)` 成為正向外面，然後凍結。
以下所有操作保留這份選定嵌入並由局部 surgery 導出；沒有聲稱還原未知歷史 rotation，
也沒有遍歷一個 literal 圖的所有可能嵌入。
來源 rotation 集合 digest 為
`a8b4561a3425b7b42f14e196c34b21ce3ced8e4c10417637c30648263d2366c4`。

標記規則是各圖**每個** full literal degree 恰五的原內點，無對稱去重；
76 個目錄標記加 W5 中心，共 77 個，即 770 個 marked-star 邊界列。
W5 的 literal edges 為
`01,12,23,34,04,05,15,25,35,45`，中心 `v=5`。
它與 catalogue 91 的圖相同，仍依任務要求獨立列為具名控制；其外框 degree 三，
不符合全域最小目錄外來源身份。

77 個循環鄰點列表中，57 個逐邊核對為 C5 link；其餘 20 個只稱循環鄰點列表。
其外框接觸數分布為 `m=2:5, m=3:55, m=4:15, m=5:2`。
沒有從控制域的分布推斷條件來源必須有這些位置。

## 2. 完整操作域及結果

各標記枚舉五條原 spoke 的刪除及五個 flip 候選。
flip 僅在原邊兩側為內三角面、四個頂點互異、相對角線原先不存在時接納。
quotient 逐標記枚舉五個實際鄰點的全部 52 個 set partitions：
identity 記為不適用；排除交錯 blocks、識別兩個不同外框 label、識別原相鄰點。
「非相鄰」指 literal 圖上非鄰接；L 非環時，不因循環位置相鄰就誤判為有邊。

共 385 個 flip 候選中 345 個合法；4,004 個 partition 候選中 290 個合法。
所有不合法候選也保留原因。290 個 quotient 分為 275 個單 pair、10 個 triple block、
5 個雙 pair；265 項需簡化平行邊，共移除 340 份重複原邊像，保留全部 preimages。
原五條外框邊優先保留，外框 labels 始終互異。

| 操作 | 相等 | 嚴格縮小 | 嚴格擴大 | 互不包含 | 合計 |
|---|---:|---:|---:|---:|---:|
| 刪 spoke | 0 | 0 | 385 | 0 | 385 |
| 合法 flip | 0 | 20 | 5 | 320 | 345 |
| 刪中心後合法 equality quotient | 0 | 75 | 10 | 205 | 290 |
| 合計 | 0 | 95 | 400 | 525 | 1,020 |

[OPERATIONS.csv](OPERATIONS.csv) 是完整 1,020 行操作表，包含原圖／中心／L、
操作 ID、兩個完整 Σ、差異列、所有舊 lifts 是否保留及 full-lift reference。
[certificate.v2.json](controls/certificate.v2.json) 另保存每項差異列的 literal
全圖著色見證；空列由全量枚舉及獨立回溯確認。

## 3. 同一色框的完整關係與雙向 full lifts

固定十列的順序為
`01012,01021,01023,01201,01202,01203,01212,01213,01231,01232`。
圖的色向量位置永遠是該圖記錄的 `nodes`，保留原整數 label；刪點及 quotient
不把剩餘 labels 壓成連續編號，也不另行更名顏色。

對每個 beta，令 H=G-v，R_beta(tau) 是 H 上固定 `(B,L)` 的**全部** full lifts，
令 M(tau) 為五鄰點沒有使用的色。逐份實際 lift 驗證

    eta 可接回中心 ⇔ M(eta(L)) 非空 ⇔ 五鄰點至多用三色。

中心可用色逐 fibre 保存，加入每個可用中心色恰重建原圖的完整 lift 集合。
介面編碼的總 domain 是全部 `4^5` 有序 L 指派；與共享 B label 不一致的指派
及未列出的 fibre 明定為空。非空 fibre 保留整份 H lift 索引，並逐一檢查其完整性。
這是可無損展開的完整 relation，不是單點或 pair marginals。

刪 spoke 的共同圖 D=G-vl_i 上，保存每份**同一著色**的
`A=[color(v) != color(l_i)]` 及 `F=[新相對角線兩端異色]`。
四個 `(A,F)` fibres 全部保留，包含空格；A 子集恰是原圖 lifts，F 子集恰是 flip
lifts。刪邊本身取 F 恒真。完整 Σ 相等要求十列的兩個存在量詞逐列等價，
不能只憑某列有共同 lift，也不能只憑所有舊 lifts 都保留。

quotient 的每份著色經原 label map 拉回，恰等於 H 上滿足**全部 block equalities**
的 lifts；反向由 block 常值著色唯一下降。接回中心另需 M 非空。
所有實際 edges、rotation、faces、attachments／supports、外部分量與 bridge ownership、
quotient maps／edge preimages／弧加入及 contraction steps 都在嵌入 domain 中。
兩向構造與精確公式詳見 [CONTRACT](paper/CONTRACT.md)。

## 4. 預先凍結的候選條件

每項結果按 antecedent 判為 `triggered and holds`、`not triggered` 或 `counterexample`。
下列三個 ANY 條件都要求一份同源、同列、同色框的共同 lift；即使如此仍不足。

| 候選 | 評分單位 | 觸發 | 成立 | 反控制 | 狀態 |
|---|---|---:|---:|---:|---|
| D-ANY：有一份可還原 spoke 的 lift 就保全 Σ | 操作 | 385 | 0 | 385 | counterexample |
| D-OLD-ALL：所有舊 lifts 保留就保全 Σ | 操作 | 385 | 0 | 385 | counterexample |
| F-ANY：有一份原圖／flip 共同 lift 就保全 Σ | 操作 | 345 | 0 | 345 | counterexample |
| F-OLD-ALL：flip 保留全部舊 lifts 就保全 Σ | 操作 | 0 | 0 | 0 | not triggered |
| Q-ANY：有一份 equality lift 可接回中心就保全 Σ | 操作 | 290 | 0 | 290 | counterexample |
| Q-PAIR-CENTER：單 pair equality lift 必可接回中心 | 指定列及 H lift | 2,340 | 1,710 | 630 | counterexample |
| Q-SEPARATE-JOIN：各凍結 pair 各有 witness 就有共同 witness | 合法多重 partition 及指定列 | 60 | 60 | 0 | triggered and holds |

Q-SEPARATE-JOIN 的 constituent pairs 依每個 block 的最小**原頂點 label**選代表，
再排序；60 次成立只是這個預先固定條件的有限校準。
不能換一套 pair 分解後沿用這個數字，更不能提升為一般完整 join 定理。

紙面另證 F-SOUND／Q-SOUND 的兩向充分條件：舊接受列須有一份可共同接合的 lift，
且每份新圖 lift 都能還原原約束／中心。兩條件在本固定域都是 `not triggered`。
完整十列相等的精確 iff 在全部 1,020 項均核對正確；其「相等 antecedent」觸發數零。
中心 full-lift identity（770 列）及操作 full-lift identities（10,200 列）
則是 `triggered and holds`，不是零觸發的真空成功。

## 5. 兩個明示 literal 反控制

**W5。** 原 Σ=91，固定 L=`(0,4,3,2,1)`。
刪 `05` 得 Σ=987，新增列 7、8、9；所有舊 lifts 仍逐份保留。
在同一四邊形中 flip `05 -> 14` 得 Σ=721，丟列 1、3，新增列 7、9。
列 0 的全圖著色 `(0,1,0,1,2,3)` 同時適用於原圖及 flip；這份共同成功不能保全 Σ。
列 7 的 `(0,1,2,1,3,0)` 適用於刪邊及 flip，原邊 `05` 卻同色。

**Catalogue 95，v=6。** 原頂點 `0..7`，L=`(0,4,3,2,5)`，原邊為

    01,04,05,06,07,12,17,23,25,26,27,34,36,46,56,57。

刪 6 後合法識別 `4=5`，保留外框 label 4；所得節點 `[0,1,2,3,4,7]`，原邊像為

    01,04,07,12,17,23,24,27,34,47。

Σ 從 95 變成 271，丟列 4、6，新增列 8。
列 0 的 H 著色在 nodes `[0,1,2,3,4,5,7]` 上為 `(0,1,0,1,2,2,3)`，
滿足 `4=5` 且中心可取色 3；仍不足以保全十列。
列 8 的 H 著色 `(0,1,2,3,1,1,3)` 同樣滿足 equality，
L 色為 `(0,1,3,2,1)`，已用四色，中心無可用色。
兩個控制的獨立 literal 枚舉見 [PAPER_REVIEW](review/PAPER_REVIEW.md)。

## 6. 驗證、版本與重播

權威有限證書是 **controls/certificate.v2.json**。
首版 `controls/certificate.json` 與 `logs/generation.log` 保留供追溯，
**不能作為候選條件的驗收證據**：審查發現 Q-SEPARATE-JOIN 使用 L 順序首點，
未符合凍結的最小原 label 規則；Q-PAIR-CENTER 也曾錯用每操作計分。
修正實作後產生新 v2，沒有覆寫首版，也沒有更改凍結公式。
原圖／操作的完整 Σ 分類不受這兩項評分修正影響。

兩套獨立著色實作為 product 直接枚舉及 MRV 回溯；共同核對 994 個不同 literal
圖的全部 lifts，儲存為 1,230 份具名圖記錄、12,300 個含空格的邊界列。
另獨立檢查 literal 操作 edge arithmetic、全部候選 partitions、rotation／face walks、
Euler、具名 B 為外面，以及 literal／apex 平面性。
完整審查紀錄見 [INDEPENDENT](review/INDEPENDENT.md)、[TOPOLOGY](review/TOPOLOGY.md)。

正常重播及 `PYTHONHASHSEED=17 --seed 17` 從其他 cwd 重播均已匹配**同一份完整 v2**。
破損測試涵蓋漏列、錯外框 label、錯 full lift、非法 quotient、漏掉空 fibre；
另檢查不能覆寫既有證書。凍結輸入、設計、程式與證書在重播中保持不變。
最終程式整合後的 exit codes、負測試 mutation recipes 與 hashes 見
[VALIDATION.final.json](VALIDATION.final.json) 和 `logs/final-*.log`；
`VALIDATION.json` 保留較早一輪，最終版另外接入獨立完整操作域及 literal map 核對。
檔案總清單見 [MANIFEST.json](MANIFEST.json)。

從 repository root 重播（本機 `.venv` 已有 NetworkX 3.5）：

```sh
.venv/bin/python -B audits/2026-10-12-degree5-star-b-6ef2c06c/controls/check.py --check audits/2026-10-12-degree5-star-b-6ef2c06c/controls/certificate.v2.json
PYTHONHASHSEED=17 .venv/bin/python -B audits/2026-10-12-degree5-star-b-6ef2c06c/controls/check.py --seed 17 --check audits/2026-10-12-degree5-star-b-6ef2c06c/controls/certificate.v2.json
```

checker 的 `--write` 僅能在本包 controls 內建立**不存在**的新檔；`--check` 不寫檔。
NetworkX 版本固定是為重播 source embedding 選擇，不能靜默換版後沿用舊操作域。

## 7. 證據層與停止點

| 層次 | 結果／界線 |
|---|---|
| 紙面普遍 identity | 中心、刪邊、flip、quotient 的完整 relation 公式及兩向 full lifts；以具名圖及合法操作為前提 |
| 固定域有限校準 | 133 個 literal controls、77 個標記、1,020 次操作完成；沒有一項保全 Σ |
| 嵌入來源 | 一份重建並凍結的合法 embedding；歷史 rotation 未提供，不聲稱全部 embedding 完備 |
| 933／941 整圖 D5 像的實際條件來源 | `not triggered`，沒有供應或構造任何這類來源 |
| 全域最小、同內點數最大邊數身份 | `not triggered`，不能以目錄 controls 或 W5 代替 |
| 132 關係目錄 K | 重播原 cofacial v2 checker 並重新著色全部 literal witnesses；目錄完備性仍是上游前提 |
| 必要 Kempe／外側 screen | 原 checker 的有限 screen 核對已重播；普遍必要性沿用 BASE，不由本包有限操作推得 |
| 四色定理（4CT） | 上游 disk 黏合論證的外部依賴；本包不重證，也不由 Python lifts 升格為 4CT 證明 |
| Dvořák–Lidický 外部計數定理 | 上游十二內點界的依賴；其計算證明本輪未重播，本包不以它推出新普遍縮減 |
| Lean | 沒有新增 theorem；沒有執行 lake build；本包沒有 Lean 驗收聲明 |
| 一般 reducibility、十三內點以上、K∞=K≤5 | **OPEN**；不能從本固定域零相等外推一般不可能，也不能由候選有限成功推出普遍可縮減 |

任務 B 在指定有限域到此停止；沒有搜尋任意大小來源，沒有借用 edge-critical
假設，也不依賴任務 A 的位置分類或任務 C 的 cap 閉合結論。
