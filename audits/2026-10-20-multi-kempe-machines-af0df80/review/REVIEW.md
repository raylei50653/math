# 同圖多監視器：獨立複核

狀態：**PASS（固定 cell95 有限域）**。BASE 是
`af0df8081e79b51f8b24e17e01b2bd5572e46a0a`。
本複核未修改舊來源、正式文件、其他工作樹變更，也未 commit／push。

## 獨立性與完整性

[check_independent.py](check_independent.py) 只讀本輪凍結 catalogue：
枚舉全部 `4^8` 字面染色，逐邊檢查 proper，使用 adjacency BFS
重建每個 maximal 雙色分量，再以完整染色索引建立交換。
它不 import 主實驗、舊 checker 或 coupling 的演算法。
首次獨立計算完成後才讀主實驗結果作
[compare_certificates.py](compare_certificates.py) 交叉比對。

固定同一圖的全部 264 份 proper 染色已保留。
240 份 proper 字面 C5 框色中，144 個 fibre 非空、96 個為空；
所有 240 個 fibre 均在
[independent_certificate.json](independent_certificate.json) 明列，
並保存其全部完整延拓。三份觀測都由同一染色列產生，
接點固定為原來的 `0,1,2,3,4`，不作換色商。

主實驗的每一染色、全部 30 個 partial action 後繼及每一觀測列，
均與獨立結果逐項一致。交叉比對證書見
[cross_review.json](cross_review.json)。

## 核對結果

| 同時觀測 | 目前可分辨狀態 | 加入一層未來 | 加入二層未來 |
|---|---:|---:|---:|
| 任一單通道 | 160 | 224 | 264 |
| 任二通道 | 176 | 240 | 264 |
| 三通道 | 192 | 240 | 264 |

每個通道只允許自身兩個互補色對的 action 時，160 狀態已可確定更新；
完整 30 action 下，單、雙、三通道分別有
288、240、96 個「同觀測／同 action，但後繼觀測不唯一」的組合。
主實驗保存的全部首次碰撞與最深最短區分序列，
亦使用獨立後繼重播，並以 paired-state BFS 核對最短長度。

這裡的未來層數指**所有可選 action word 的行為比較**。
它不保證任選一條實際操作序列，走兩步便知道完整染色。
coupling 保存的重複 involution 例子，經獨立重播後仍保持兩個候選；
此不區分循環可任意重複。

固定框色後，三通道 Cartesian product、pairwise join 與真聯合關係
的總大小都為 192，沒有額外不可實現靜態 tuple。
其原因可直接從完整表看出：96 個非空框色的 marginal 大小是
`(1,1,1)`，另外 48 個各只有一個通道大小為 2
（`(2,1,1)`、`(1,2,1)`、`(1,1,2)` 各 16 個）。
同一 joint source／action 的後繼 Cartesian product 也未產生假 tuple。
因此本例不能宣稱三通道提供了新的靜態相容性排除。

**時間上的共同見證有可量化差別。**
獨立計算先逐染色走兩步，形成完整 observed trace 集合；
另把 existential quotient 邊直接合成，再比較集合：

| 兩步 observed trace | 數量 |
|---|---:|
| quotient 邊可拼出的路徑 | 46,272 |
| 一份完整染色可實走的路徑 | 45,888 |
| 沒有共同完整染色見證的路徑 | 384 |

首個負例兩步都用 `(1,2,root=1)`。在真圖上同一 Kempe swap
做兩次必回原染色；quotient 卻可以在中間偷偷換成另一個同觀測 lift，
走到不同的最終觀測。交叉複核有檢查第一步的**實際中間觀測**，
再限制所有可達完整 lifts，未把同一 source fibre 的另一條中間分支混入。

跨通道改變的計數也一致：每個色對有 660 個合法 rooted-action 實例；
自身通道分割不變，另兩通道的 raw 分割每次都改變。
若只比較交換前後都仍在該色對內的接點，排除單純改變色對 domain，
另兩通道各有 140 個實例真的改變了接點連通等價關係。

不計重複 action label 的 unordered action pairs 中：
同色對有 3,600 個兩種順序皆合法實例，互補色對有 4,320 個，
均可交換。共享一色有 6,240 個兩順序皆合法實例，其中
5,664 個完整結果不同、5,616 個三通道觀測不同、5,520 個框色不同。

## 負控制與證據凍結

- 移除來源邊 `5–6` 會得到 432 份染色；其中 168 份違反原來源邊，
  原圖 checker 全部拒絕。
- 直接混合不同框色的三份獨立通道見證，雖各自有 proper 完整染色，
  沒有共同完整染色；證書保存此拒絕例。
- 兩條各自存在的 quotient 邊可通過逐邊檢查，但首個兩步假路徑
  被共同完整來源檢查拒絕；見 `cross_review.json` 的
  `temporal_negative_control`。
- 曾預期能找出同框色 Cartesian-product 假 tuple，但獨立枚舉沒有找到。
  此預期已撤回，保存結果明列 `null`；不能把不存在的負例寫成成果。

開發期間 `independent_certificate.json` 曾隨新增核對項目重新產生；
**未宣稱早期開發版本的 bytes 已保留**。本輪凍結輸入未因而修改。
最終證書已完整重新建構，`--check` 位元組核對通過，其 SHA256 為
`50e524737cd6db0734525cee6075cfed8d410bd0bf066479bd76b71d8f2e9d76`。
最終 generation 改用 exclusive-create；後續更版應另存新檔。

重播：

```sh
python3 -B audits/2026-10-20-multi-kempe-machines-af0df80/review/check_independent.py --check
python3 -B audits/2026-10-20-multi-kempe-machines-af0df80/review/compare_certificates.py --check
```

本例只回答固定 cell95 的資訊／更新問題。完整 r6／941／J1 來源
`not triggered`；一般閉合、原來源排除與 Lean 證明仍未由此完成。
