# C8 no4CT 逐命題依賴表

2026-10-13。前提為 [PROOF §1](PROOF.md#1-同一全域最小來源) 的全域 k 最小、
再邊數最大之來源；共享舊文件保留其歷史 4CT 前提，本表不修改其字句。

| 命題 | 原入口／精確前提 | 本輪替換與量詞 | 有限證据／採納邊界 |
| --- | --- | --- | --- |
| 原內部 C4 的 s<k | 舊普遍 C4 代表 | 原環四點皆內部，s≤k−4；dummy 增廣不增加內點 | 沿用 no4ct-degrees 的完整 16-mask／七份代表 |
| 原內部 C5 的 s<k | 全域最小性 | 原環五點皆內部，s≤k−5；故 cap 關係在 K | K 五內點 witnesses；不適用 Q=B |
| C4 cap 空 | C4 小代表、全圖內度≥5 | 大小下降＋Euler 排除 s=1,2,3 | geometry 小核心；不是任意 C4 圖結論 |
| C5 cap 空或 W5 | C5 小代表、全圖內度≥5 | 大小下降＋outerplane 邊界排除 2≤s≤5 | geometry 小核心；不憑局部度數單獨推得 |
| C3 cap 空 | 原圖有一份完整染色 | 三角形 proper 色型唯一；沿共同色框接回 | no4ct-degrees 已有；未假設任意圖可染 |
| 具名 C8 induced | 上述 caps，五個 apex≥3，三個 y≥4 | 原 chord 環距 2／3／4 完備分類 | 原 cap／ears 有限控制可原樣重播 |
| 小 planar J 可四色 | 舊 quotient 直接引用 4CT | N≤k+5 時，若不可染則下降為 932 disk，內點≤N−6<k | 紙面引理；J 不必是 C5 |
| H 可四色 | 原 H 有 k 個總頂點 | k≤k+5，適用相對 planar 引理 | 不把 H 的 k−8 嚴格內點套 C5 分類 |
| cofacial pair equality | 舊不相鄰商圖＋4CT | H/(u=v) 有 k−1 個總頂點且 loopless planar | 返回同一 H 的完整染色 |
| 91 個 quotient 正性 | induced C8、noncrossing independent blocks | q blocks 時 N=k−8+q≤k；樹輔助點收縮消失 | 全部 91 介面及 274 rows 可原樣核對 |
| c16／c32 整項排除 | U 避免原 (a1,a4) 同色 | 單對 equality 強迫一份原 H 染色，與 U 矛盾 | 各 74 列／固定原位置；完整 U 而非單個向量 |
| 932 的 h=3 排除 | 新目標 mask | 同一原 collar 的必要 transfer／Kempe | 本輪重算全部 35 項；無界 932 仍 OPEN |
| 932 特有 h≥4、n5≥10 | 前輪 h≤2 排除＋本輪 h=3 排除 | 同一全域最小 932 来源的 Euler 等式 | 不提高三支共同的 h≥3、n5≥9 |
| 其餘八項原契約 | 933／941 舊上界及 count 改良 | 紙面 counting／Kempe 都不需存在定理 | 本輪已核對完整原名框、附件、上下界並接回 |
| apex H-degree≥4 | induced C8、原接受列、共同 x | D3 完整 lifts；signed equality span＋nonnegative Kempe cone | 8×5=40 指定 apex 查詢及精確 dual 已重播 |
| 原短弧無距二／三雙接 | 原 C8 全 degree≥4、內度≥5 | 新原內部 C4／C5 cap；無任何外側可染性 | 任意 m 的紙面結論 |
| 至多雙接、t_i 全異、m≥9 | 上一列、原三角面 | 同一原 attachment＋outerplane 耳 | 任意 m 的紙面結論 |
| m=9 排除、k≥18 | m=9 強迫唯一原 annulus＋W8 | 不新增普遍可染性；直接列全部完整染色 | 原 8 圖×10 fibres、3,272 full lifts 已重播 |
| 第一剝層 RING／PINCH／BRIDGE | C3／C4 caps、原 links、最多雙接 | 完整外面 walk、正對同 pair／至多兩點 | 任意 m 的紙面結構；不保證後層同型 |
| m=10 排除、h=3⇒k≥19 | 三型紙面分類及最低度 | 16 個具名 H × 8 個原 collar | 原 128 圖完整 Σ1023／75,936 lifts 已重播 |
| 一般 separator 剝層 | 同一原嵌入、全部 attachment edges | literal full-fibre joins；共享原點色值一致 | 無四色定理依賴；不給固定寬度或來源存在 |
| 任意大小三支排除 | 尚缺同一來源全域矛盾 | 本輪無此結論 | OPEN；932 一般排除仍承擔 4CT 難度 |

本輪新增證明的關鍵不等式是 `s<k` 及 `N−6<k`，不能以「圖較小」代替
數量核對。特別是 `N=k+6` 僅给不增加大小，不能用外側五輪排掉 932。
下游 normal／seed17／負控制已通過，詳見父 audit 的
[結果](../RESULTS.json) 與 [驗證總帳](../VERIFICATION.json)。
