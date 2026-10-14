# 外部4-candidate計算：引用身份與信任界線

本輪新增的外部排除輸入為 Dvořák–Lidický–Mohar，[arXiv:2504.08327v2](https://arxiv.org/pdf/2504.08327v2)，2025-04-14。
本輪核對 primary PDF 的文字，保存 [版本、URL、hash 與 custody](external/source.json)。
不宣稱已核實正式期刊出版，不宣稱已重新下載／重播作者全部計算。

- 印刷 p.13 定義：4-candidate 的外面為C4，所有內面三角形、每個三角形facial、全部內點度至少5。
- 印刷 pp.24–25／Table1 報告完整生成全部至多28個**總頂點**的4-candidates；沒有rainbow-forbidding，diagonal-forbidding只有四點diamond。
- p.24註1：C++達28點；另一位作者的Python/Sage實作獨立核對至25點。程式入口：[作者頁](https://lidicky.name/pub/mindeg5/)。本輪未重播。

本包直接使用上述有限計算結論。Theorem10只是等價式；Conjecture2仍未證。
沒有以Theorem11把28降成27，也沒有把外部上界升成無界。

no4ct依賴核對：§2 的 Observation18、Lemma19、Observation20、Lemmas21–24、Corollary25
構成度數、discharging及平面reduction的完整生成鏈，不使用§1的4CT-dependent命題。
本包直接匹配4-candidate定義與diagonal拒絕，不走one-crossing等價。
這是紙面依賴核對；外部生成器／染色檢查的實際正確性仍屬引用信任，沒有本地獨立證書。

既有正規形／度數前置另保留原 frozen 報告的計算與文獻依賴，本頁不重寫其信任鏈。
