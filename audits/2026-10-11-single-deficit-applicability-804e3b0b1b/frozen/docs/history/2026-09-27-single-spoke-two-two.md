# 2026-09-27：single-spoke (2,2) 必要分類

研究報告見 [(2,2) 完整關係／實際支援分類](../c5_single_spoke_two_two.md)。
本輪只處理兩個二接點分量；未重開 (2,1,1)、未生成來源圖 catalog。

任意大小化約先保留兩份原 ordered tuple relations、各點 attachments、
全部 bridges 與 contact 區塊，再利用完整關係穩定子、slit lifts、逐禁色
外部至少兩色、同圖奇數 bridge 結構及未用色對守恆建立有限必要表。
三代表有 1,530 筆必要候選；1,150 筆有 T4 拒絕見證，保留 380 筆／190
個交換名字後的型。104 筆兩個 p 已證接受，其中 80 筆沿用未接 b4 引理。
所有 target 禁色上界、候選集合、強迫拒絕及未決記錄均非可實現性證書。

新增 checker／JSON artifact／190 行支援表，同步 README、HANDOFF、STATUS
及舊 single-spoke 報告的後續入口。完整關係局部控制為 65,535 個非空
binary relations、386 個解除 schemas、9,264 次整關係換色、2,880 次完整
tuple 覆蓋接合及 12 個 bridge 交替轉移。既有 16 個 (2,2) 控制各重播
240 列關係的 F、解除 witnesses、必要上界與接合；全部對應 T4 排除項。
未重新驗證這些來源的 disk rotations 或刪邊著色。

本輪驗證：

- `python3 scripts/c5_single_spoke_two_two.py --check`：重算 JSON 與支援表。
- `lake build`：8,826 jobs 完成；只有既有 linter warnings。
- `python3 scripts/check_docs.py`：本地連結／報告索引／handoff 契約。
- `python3 tools/docgraph check`：19 documents、42 relations、4 families，0 errors／notes。
- `git diff --check`：空白檢查。

未新增 Lean theorem；build 不形式化新紙面化約。未執行舊 (2,1,1) 全表
checker、一般圖枚舉或其他來源 catalog，亦未 commit／push。

精確停止點：record 110 的 s=0、支援 (34,12)、q 禁色 ({1,2},{2,3})。
兩份完整交換 pair 關係強迫兩個 p 拒絕，但必要 screen 未排除 T4；
需要兩份原奇數 bridge 路徑與旁支 tethers 的共同 disk／minor 論證。
這是一份尚未實現的必要候選，不是反例。一般 (2,2) 分離仍未證。
