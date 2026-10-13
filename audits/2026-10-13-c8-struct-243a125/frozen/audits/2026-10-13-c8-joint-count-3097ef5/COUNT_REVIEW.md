# C₈ 共同計數證書的獨立審查

審查對象是 BASE `3097ef5be241b7777451a5ef8a663f3987d6b866` 下本包的
[完整介面](interface.json) 與 [最終計數證書](counts/certificate.v2.json)。
結論為 **PASS：70 項全部有精確驗收；57 項 transfer 排除、3 項共同計數
排除、10 項必要條件殘留。** 這些殘留已有自身 Kempe 閉包的完整正計數
support，不能依本包三類必要條件提高共同下界至 h≥4。

獨立可重播程式 [count_review.py](count_review.py) 不匯入 interface producer、
count generator 或 primary checker；結果與實際 consumed bytes 的 SHA256
存於 [count_review.json](count_review.json)。本次 normal／seed17 均已執行：

```bash
python3 audits/2026-10-13-c8-joint-count-3097ef5/count_review.py --check
PYTHONHASHSEED=17 python3 audits/2026-10-13-c8-joint-count-3097ef5/count_review.py --check
```

两次結果相同，均逐項檢查 25 個恆等式與全部 70 個查詢。

## 1. 獨立重建與信任邊界

主 checker 以 restricted-growth words 產生 partitions。本審查從集合 blocks
插入下一個點來生成全部 partitions，剔除交錯 blocks，再依原具名位置排序。
內列則從全部 4⁸ 份 literal words 直接檢查環邊並取共同 S₄ 軌道。結果為
274 個 proper C₈ 軌道、1430 個 noncrossing partitions、91 個非零 equality
columns，與證書的完整順序一致。

本審查把各列及 partition 的同塊位置對編為 bitmask；partition 的同塊對
全部包含於色列的相等位置對，恰等於 equality entry=1。以這條獨立表示重建
全矩陣，再用 int／Fraction 核對。每個恆等式在全部 1430 個 equality vectors
上為零，包括 1339 個零向量；不存在只核對矩陣 rank 或浮點殘差的步驟。

本審查逐項依賴的 interface transfer 與 Kempe options，另由
[controls/checker.py](controls/checker.py) 從 literal attachments 與全部
noncrossing partitions 獨立重建。因此 count_review 的 PASS 必與介面 checker
的 PASS 一起使用；本審查沒有假裝獨立重算每一份 literal 環帶。

來源覆蓋、二色穩定子、完整接合、Kempe 刪除歸納及 inclusion–exclusion 的
一般紙面證明已另審於 [COVERAGE.md](COVERAGE.md)。原 C₇ 論證的 odd-cycle
全部軌道大小 24 不可直接套用；本輪正確採用二色軌道大小 12，以及
24 T_(r,p)=|Orb(p)| L_(p,r)。

## 2. 每個排除證書的邏輯

對最終三份 count exclusions，獨立核對每個左式項：index 與完整具名 word
一致；係數嚴格正；列仍在當時必要上界中。每個右式項都在該上界外，因此
其**實際計數**為零；沒有要求右式係數非負。

全部 equality-vector 殘差為零後，同一 H 的普遍計數公式使左式等於零。
由 x≥0，左式每一列的實際計數均零。審查重算接受外列的完整必要 preimages，
證明 required `01232` 的全部 preimages 都在該左式中；沒有只取其中一份
witness 或忽略空 fibre。三份新排除是：

| 具名分配 | Σ | 左式正項數 | 右式零列項數 | `01232` 的全部上界內 preimages |
|---|---:|---:|---:|---|
| (0,0,1,1,1) | 941 | 4 | 46 | 28,207,225 |
| (0,1,1,0,1) | 941 | 10 | 64 | 18,59,87,131,205,250,269,272 |
| (1,0,1,0,1) | 941 | 10 | 71 | 18,21,59,60,176,270,271,272 |

indices 僅用於短表；證書逐項帶完整 word，獨立 checker 核對兩者一致。
另外 57 項由必要上界缺某接受外列的全部 preimages 而排除。它們不需要
存在某個 equality identity，也不要求必要上界本身為空。

## 3. 計數迫零與 Kempe 交替收窄

每個 refinement stage 的所有正左式恆等式都只用當時上界中的列，右式只
用已知零列，故可普遍證明更多實際計數為零。逐項驗證後才刪去這些列，
再從同一份界面 Kempe 表重新計算每輪完整失敗 split 與同步刪除集合。
整条上界鏈因此一直包含任何實際 H 的完整關係。

主發現器用浮點 LP 找候選，再用 Fraction 還原並以精確證書驗收；此審查
不匯入 SciPy，也不信任 LP 的 infeasible 訊息。全部 25 份恆等式由三個
最終排除恆等式及 refinement 的 22 個迫零恆等式組成。

每份最終殘留都核對：274 座標皆非負；上界外全部為零；以同一份有理
equality 展開係數逐座標重建；十個 literal 外列的完整 T x 計數吻合；
接受列全正，拒絕列全零。每個最終上界座標都在該單一向量中嚴格正，
且對每個正座標及每個互補 split，至少有一份完整交換軌道包含於這個
向量自己的 support。不能以較大的舊上界替代這項實際 support 核對。

| case | 具名分配 | Σ | 最終正計數 support 大小 |
|---|---|---:|---:|
| c04 | (0,0,1,0,2) | 941 | 193 |
| c07 | (0,0,2,0,1) | 941 | 193 |
| c15 | (0,1,2,0,0) | 933 | 134 |
| c15 | (0,1,2,0,0) | 941 | 173 |
| c16 | (0,2,0,0,1) | 941 | 102 |
| c18 | (0,2,1,0,0) | 933 | 134 |
| c18 | (0,2,1,0,0) | 941 | 175 |
| c20 | (1,0,0,0,2) | 941 | 173 |
| c30 | (2,0,0,0,1) | 941 | 175 |
| c32 | (2,0,1,0,0) | 941 | 102 |

向量可清分母成整數，不改 support 或接受／拒絕。這證明本輪給定的線性
計數、非負性、transfer 及 Kempe 存在性必要條件有這十份殘留；它們仍非
任何實際 H 的計數或來源實現。

## 4. 審查發現、修正與保留

初版 `certificate.json` 的六份可行向量 support 不滿足全部 Kempe 必要
閉包。它們作為第一輪線性放鬆結果沒有錯，但不能用作最終「三條條件
共同通過」的證據。初版保持歷史原樣；v2 以共同計數最大可行 support 與
Kempe 收窄解決此問題，十份最終向量均通過。

審查亦要求 v2 verifier 不可把 `residual_support_mask` 當成 optional：
當有 joint_refinement 時，每份 residual 必含完整 refinement、final upper、
final preimages 與 residual support 欄位。主 checker 已加此 schema 核對；
負控制實際刪去該欄位時回報 `incomplete joint residual`。獨立 checker
無條件要求最終 residual 的這些欄位。

真實來源控制仍是 `not triggered`。未證哪一條額外原圖結構足以排除十份
殘留；原面配置、最小度數、無分離三角形、所有 partition 由同一 H 實現，
以及不同染色間的完整 Kempe 交換雙射均比本輪必要條件強。沒有把有限
controls 或不等式放鬆提升成圖實現，也沒有新增 Lean 形式化結論。
