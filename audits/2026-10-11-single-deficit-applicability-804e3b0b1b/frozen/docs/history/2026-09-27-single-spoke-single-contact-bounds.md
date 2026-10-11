# 2026-09-27：single-spoke 剩餘單接點上界分類

研究報告：[root 接線與禁色角色守恆](../c5_single_spoke_single_contact_bounds.md)。

從前輪 artifact 的 16 個 open_queries 出發，沒有重啟來源圖枚舉。
同圖單 root block-palette 歸納給未用色角色守恆 `a=c iff d=c`。
未知分量在 q 禁 3，因此 target 的 F⊆{3}；12 個 p₁ 查詢取 z=2，
4 個 p₂ 查詢取 z=0。114 筆全部接受兩個指定 target。

新 checker／artifact 保存全部原記錄、placements、兩個 root 支援 frame
各 16 個接線子集、tightness、固定 z witness 及必要 unary relations。
四點支援的 root 不可能孤立；每 frame 剩九個 tight 候選、一個 target
slack pair。這是局部必要分類，不宣稱候選或禁色上界可實現。

本輪實際檢查：

- `python3 scripts/c5_single_spoke_single_contact_bounds.py --check`：通過，16 查詢、114 both、0 open。
- `python3 scripts/c5_single_spoke_two_contact_bounds.py --check`：通過，原 18 查詢及既有完整 relation／minor 控制保持一致。
- `python3 scripts/c5_single_spoke_root_conservation.py --check`：通過，原任意大小歸納的局部代數證書。
- `python3 scripts/c5_single_spoke_root_sweep.py --check`：通過，繼承原表一致。

- `lake build`：通過（8,826 jobs；既有 linter warnings）。
- `python3 scripts/check_docs.py`：初次因 HANDOFF 超過 150 行失敗；精簡既有摘要及重播入口後通過。
- `git diff --check`：通過。

證據層為紙面任意大小歸納＋既有外部 degree-list／結構＋Python 局部證書；
未新增 Lean theorem。未重新執行全部歷史 graph 搜尋或發布 Git commit。
下一窄入口移至 t=1 其餘分拆，先看 (2,2) 的完整雙分量關係與支援。
一般核心存在／分離、單側／共同出口及主命題仍未證。
