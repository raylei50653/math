# 六私人點 C6 cap：完整枚舉與 fibres

此 producer 對 frozen plantri 執行 `-aP6c2m2 12`，生成 **89,038** 份 disk
embeddings；逐份從 rotation 重建面，留下無 boundary chord 的 8,796 份，再以
六私人點的 cap 度均至少五篩成 **三份**：兩份 maximal outerplane core、一份
deep W5。本 producer 的枚舉來源仍是 plantri；獨立 annulus 分類及覆核另見
`../theory` 與 `../review`，不可將本檔單獨稱為獨立 generator。

| cap | 私人核心 | 31 個 C6 rows 中非空數 | 完整 C6 lifts |
| --- | --- | ---: | ---: |
| cap-43569 | deep W5 | 22 | 42 |
| cap-43570 | maximal outerplane | 21 | 44 |
| cap-81910 | maximal outerplane | 20 | 40 |

每份 cap 保留 plantri 原 rotation、原外面、old-to-named mapping、具名 rotation、
全部普通邊及 private order。C6 names 為 `0..5`，私人點為 `6..11`。
每份再覆蓋八個 `b_i=b_(i+2)`，以及 C6 六個 rotation、兩個 direction，總計
**288 份具名接線**，含對稱重複，不宣稱都是不同嵌入。原 digon pin `b_(i+1)`
仍留在全部原 C8 rows 中；具名 pin map 明確保存。

## 完整 fibres 與同一 literal 色框

[CERTIFICATE.json.gz](CERTIFICATE.json.gz) 明存 93 個 C6 fibres，空者 30 個；
並明存全部 **78,912 個原 C8 canonical fibres**，空者 **60,864**、非空者
18,048，總計 **35,904 個六私人點完整 lifts**。每份 C8 fibre 都經整份 cap DFS
逐列重算，並與 C6 fibre 的全域換色 pullback 相等；不拼接不同列的成功。

完整 6,564 literal rows 的展開使用 lossless codec：證書保留 frozen interface
的逐 literal row 原 canonical index 及完整 `0..3` 色值 permutation。依該 row
的 permutation 同時改寫一個六私人點 tuple 的每個色值，再排序整份 fibre，
得到且僅得到該 literal row 的完整 fibre。未出現在 boundary 的色值也補入
permutation，故三色、二色 rows 的私人四色 lifts 不會遺失。

此展開涵蓋 **1,890,432 個 literal fibres**，空者 **1,458,432**、非空者
432,000，總計 **857,088 個完整 literal lifts**。每份接線均保存逐列展開
的 SHA256：按 literal index `l=0..6563`，串接 compact JSON
`[l, decoded_fibre]` 與一個 ASCII newline，空 fibre 也加入 digest。
此 codec 保存全部資料；不以支持 mask 取代 fibres。

## 八份 U 的精確原列交集

每份接線、每份 U 均保留全部交集的**原 C8 indices**，並保存第一個原 C8 row
及同色框完整私人 lift。八份 U 的最小交集如下：

| query | 最小原 C8 交集 |
| --- | ---: |
| c04-941 | 25 |
| c07-941 | 25 |
| c15-941 | 24 |
| c15-933 | 12 |
| c18-941 | 22 |
| c18-933 | 12 |
| c20-941 | 24 |
| c30-941 | 22 |

[RESULTS.json](RESULTS.json) 保存所有達到各最小值的具名接線及 witness。
沒有空交拒絕；也沒有 singleton 交集，所以這個 cap 域沒有新增 singleton
forced row。八份 U 全部保留，未知原 H 的 source realizability 與主命題仍 OPEN。

## 重跑與保管

`python3 search/produce.py --check` 及 `--check --seed 17` 都重新編譯 frozen
plantri、生成完整原始域、重算所有 fibres 與接線，兩者均 exit 0；seed17
打亂 candidate traversal 與 DFS tie-order，但要求完整證書仍逐值相等。
由 repository root 執行的完整指令、實際 exit codes、輸出 hash 與空 fibre
計數見 [VERIFICATION.json](VERIFICATION.json)，stdout 見
[REPLAY.json](REPLAY.json) 及 [REPLAY_SEED17.json](REPLAY_SEED17.json)。

完整原始 89,038 份 embedding rotations 保存在
[all-c6-n12.ascii.gz](all-c6-n12.ascii.gz)。`produce.py --write` 拒絕覆寫任何
既有結果。此工作未使用四色定理、未新增 Lean theorem、未 commit／push。
