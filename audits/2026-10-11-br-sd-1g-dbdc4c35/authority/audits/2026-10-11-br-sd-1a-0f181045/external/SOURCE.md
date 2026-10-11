# BR-SD-1a 的外部正式數學來源

作者 Zdeněk Dvořák，List coloring and Gallai trees，2018-03-24。
[作者的大學網站原 PDF](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)。
這是具完整定理與證明的作者講義；本 audit 不把它標成期刊論文。
正式依賴為印刷頁6／PDF第6頁（zero-based page5）的 Theorem10 (Gallai)，
及同頁緊接之前的 blockwise uniform 定義。已核文字抽取與實際頁面。

連通圖的列表逐點至少 degree 時，不可著色刻畫為 Gallai tree 上的
blockwise uniform assignment。該表示在每個奇環 block 配置二色 palette；
相交 blocks 的 palettes 必互斥，每個點的 list 是包含它的 blocks palettes 聯集。
非割點只屬一個 block，故其原 list 等於該 block palette。
這正是本次引用的三個後果；沒有把相交 blocks 限成只沿 bridge 相邻。

凍結 PDF：`gallai.pdf`，164927 bytes。
SHA256：`50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea`。
下載時間、URL、HTTP metadata 見 `download.json`；全篇抽取見 `gallai.txt`，
第6頁圖像見 `gallai-p6.png`。本證明不引用 SD-A 的單缺額定理、
Cranston–Rabern 分類或 R27 minor；亦未新增 Lean 形式化。
