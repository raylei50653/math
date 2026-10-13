# Signed chord cap 的獨立全域覆核

本覆核不 import `search/` producer，也不連結其 C++。
[signed_independent.cpp](signed_independent.cpp)對每張 frozen plantri 輸出直接
驗證 simple adjacency、rotation 中所有 faces、唯一簡單 C8 外面、三角內面
與 Euler identity。列次序與八份 U 由 frozen 原始資料重新建立。

Producer 對每份 boundary row 做 private DFS，並以 DSU 驗 Eq contraction。
本覆核改為枚舉所有 `4^h` private 指派（按私人邊集合 cache），用 274-bit
邊界相容集接回原 spokes；從而重建每份 ignored-chord fibre 的**全部**
私人 tuple。逐 fibre 比較數量與完整 tuples，零 fibres 不略去。
對每份 literal row 重新算所有 boundary chord 的 Eq／Diff signature；
每個候選 Eq 集以布林 transitive closure 驗證 cycle/Diff loops。

一份 literal row 有唯一 Eq signature，故各合法 signed gadget 的完整
fibre 恰由「該 signature 的原 ignored-chord fibre」或空 fibre 決定。
這同時覆蓋全部 signed fibres，不只覆核 producer 所選最小 witness。
所有 16 份具名 D8 邊界接法直接作用到同一列次序，未分別正規化接合件。

| 覆核量 | 數量 |
| --- | ---: |
| 原 disk triangulations | 334,512 |
| 合法 Eq／Diff signed graphs | 2,599,458 |
| 完整 signed fibres | 712,251,492 |
| 空 signed fibres | 643,620,314 |
| 完整 lifts（各原 row 歸唯一 signature） | 204,250,566 |
| signed graph／query／orientation 檢查 | 332,730,624 |
| 與 U 空交 | 0 |

八份最小交集依 frozen query 次序為 `[2,2,1,3,1,2,3,2]`。
全部 singleton intersection 的原 U row 聯集亦獨立重建：

- `c15-933`：`[19,33,188,249]`。
- `c18-933`：`[44,67,157,188]`。
- 其餘六項：空集。

這些 singleton controls 在相對頂點預算契約下迫實際 H 的對應 counts
為正；並非來源排除。先前[共同計數覆核](COUNT_REVIEW.md)已給整份 U
全正的 exact witnesses，故它們與既有必要條件同時相容。

[正常 receipt](SIGNED_VERIFICATION.json)與[seed17 receipt](SIGNED_VERIFICATION.seed17.json)
記錄全部結果。正常重播另分別破壞一個 fibre count、一個完整 tuple、一個
row signature；三项皆被拒絕。生成完備性仍依賴 frozen plantri；本 checker
獨立覆核全部已生成 embeddings 及所有 signed 条件，沒有把 generator
本身的無遺漏性稱為獨立形式化證明。

```bash
python3 -B audits/2026-10-13-c8-joint-gadgets-6943561/review/signed_independent.py --negative
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-c8-joint-gadgets-6943561/review/signed_independent.py --output audits/2026-10-13-c8-joint-gadgets-6943561/review/SIGNED_VERIFICATION.seed17.json
```

Scope 僅是本 audit 的 `h≤5` triangulation + signed boundary chord grammar。
沒有涵蓋所有頂點淨預算內的 quotient gadgets；主命題與八項來源仍 OPEN。
