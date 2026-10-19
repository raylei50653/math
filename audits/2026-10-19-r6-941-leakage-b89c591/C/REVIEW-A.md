# C 對 A 的獨立實作與必要模型邊界審查

已閱讀 A/PROOF.md、model.py、check.py，並執行完整 A/check.py
`--negative-controls`；全部整數等式、兩份新來源正性控制及六項負控制通過。

另以 [review_a.py](review_a.py)直接重建 11 條原右 cap 邊及 12 條原左
cap 邊，沒有呼叫 A/model。此 checker 從邊不等式獨立重建 T，將新證書
的同一個 2461 維 Z 投影為 E，再與 C 的全部完整矩陣比較：原 G、Q1、Q2、
GB 十列以及 U 十列均逐格相等。它從兩份固定 D_old 七 pin 賦色再枚舉
全部 R,L,v,w，獨立重建六格與四格的來源正子 fibres。

[精確結果及受審檔 SHA](review-a-results.json)為：

| 控制 | `(G,Q1,Q2,GB)` | `(d_a,d_b)` | `(A_a,A_b)` |
| --- | --- | --- | --- |
| Q2_source_positive | `(941,1021,941,1021)` | `(4,4)` | `(16,16)` |
| allK_source_positive | `(941,1023,1023,1023)` | `(10,16)` | `(40,64)` |

兩者均有完整 U 支持 319。另逐份核對 C 的新 fan-B 精確恆等式；其 GB
支持都有 01212，故與新 fan-B no-go 相容。

A 的 noncrossing signed span 重建正確使用有號整數係數；component
columns 直接保存起點、完整分割與重數，所有 7382 個 H 軌道等式均由 A
checker 精確核對。paper 將此必要模型與真正圖實現分開，未把兩份控制
合併為同一來源。第一份控制足以阻擋本必要模型中的普遍 Q2 四列 no-go，
第二份阻擋本必要模型中的「至少一候選必在 K132 外」。兩者都不是原來源
存在證明，也不否定加入其他真實原圖條件後可能的排除。

審查結論：通過；主目標仍須真正來源結構／完整著色映射，不能用有限
必要向量作結論。review_a.py 是唯讀標準庫程式，重播只輸出 JSON。
