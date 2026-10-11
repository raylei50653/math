# BR-SD-1c 外部依賴與治理查核

2026-10-11。正式數學依賴為 Zdeněk Dvořák，*List coloring and Gallai trees*，2018-03-24，
[作者大學網站原講義](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，Theorem 10 及同頁 blockwise-uniform 定義，印刷頁6。
連通圖逐點至少 degree 的列表若不可著色，則是 Gallai tree 的 blockwise-uniform assignment；
每個點 list 為 incident block palettes 的聯集，相交 blocks palettes 互斥；
odd-cycle palette 為二色，bridge palette 為一色。講義含正式定理與證明，不標為期刊論文或 Lean theorem。

本輪使用 web 讀作者 PDF，另以 view_image 核對原封存第6頁圖像（原文件未修改），
並在本專屬目錄重新下載 [gallai.pdf](gallai.pdf)。
164927 bytes，SHA256 `50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea`，
與 BR-SD-1a frozen PDF 逐 byte 相同。時間／HTTP metadata 見 [download.json](download.json)。
無第二份外部數學黑盒；不使用 SD-A 或 Cranston–Rabern。

治理依賴只讀即時 [GitHub Issue #4](https://github.com/raylei50653/math/issues/4)，
gh 完整 body／comments／updatedAt snapshot 見 [issue-4.json](issue-4.json)。
Issue 只管理文件責任與 bounded propagation，不裁決數學採納。
本輪 user 明確只授權 exclusive audit、canonical 採納另行裁決，
所以 L0/L1 核對及 direct-parent residual 審閱記入 REPORT，shared canonical files 保持原 bytes。
沒有 GitHub comment、commit、push 或其他外部寫入。
