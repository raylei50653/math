# 外部數學依賴

2026-10-11。本輪唯一外部數學黑盒為 Zdeněk Dvořák，
*List coloring and Gallai trees*（2018-03-24），
[作者大學網站講義](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)。
實際讀取 Theorem 10 與 blockwise-uniform 定義（印刷頁6），另核 degree assignment 定義（p.5）。

連通圖逐點至少 degree 的 lists 若不可著色，便得到 Gallai blocks 與 blockwise-uniform
palettes：各頂點 list 恰其 incident palettes 聯集，相交 blocks palettes 互斥。
奇環 palette 大小2；clique K_n 大小 n−1，包含 bridge K2 與 triangle K3。
本輪在原 C 的 degree lists 上使用此正式刻畫，不要求額外二連通或先驗 tight。
不是本輪 Python 或 Lean 的一般定理證書，也不是期刊論文版本的宣稱。

作者 PDF 本輪重新下載至 [gallai.pdf](gallai.pdf)，164927 bytes，SHA256
`50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea`，
與 BR-SD-1a／1c 既有凍結版本相同。
[page6.png](page6.png) 由本 PDF 第6頁以 pdftoppm 渲染，root 已用 view_image 核對。
獨立 paper reviewer 另外檢查該頁。

重現原頁：

```sh
pdftoppm -f 6 -singlefile -scale-to 1600 -png audits/2026-10-11-br-sd-1e-337d018b/external/gallai.pdf /tmp/br-sd-1e-page6
```

不使用 terminal lemma、SD-A 或 Cranston–Rabern，也不以外部文獻取代原來源身份映射。
