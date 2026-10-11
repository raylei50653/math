# Single-spoke 奇數 bridge 路徑必要化約

2026-09-27。接手 HEAD 為 `4f26efe`；工作樹已有未提交 single-spoke
cores／completion source、artifacts 及文件。本輪接續並保留這些成果。

[新報告](../c5_single_spoke_bridge_path.md) 收窄指定 (01,04,1234) 二接點
分支：若仍拒絕 p₁，兩接點間只能有奇數長 bridge 路徑，所有 b3 接線
位於路徑外旁支。證明比較同一 Gallai tree 的兩份拒絕 palettes；
不是小圖 normal form，也未證此分支不存在。62／52 查詢統計不變。

本輪實際通過：

- `python3 scripts/c5_single_spoke_bridge_path.py --check`：16 個 tight 局部型、12 個 bridge 轉移。
- `python3 scripts/c5_single_spoke_completion.py --check`：繼承 3,492 項接線重播；62／20／32 查詢分類不變。
- `python3 scripts/c5_single_spoke_cores.py --check`：既有必要支援表及控制重播通過。
- `lake build`：8826 jobs 成功；僅既有 AttachmentOrder／SymRelabel lint 警告。
- `python3 scripts/check_docs.py`：162 份 Markdown、2080 個本地連結通過。
- `git diff --check`：通過。

未另跑 nonadjacent／reflection standalone checker、Lean axiom audit、雙拒絕 atlas、
R 系列或一般圖枚舉。未新增 Lean theorem；build 不形式化新 palette 論證。
未 commit／push。下一步保留同圖接線與環序，分析奇數 bridge 路徑外
帶 b3 接線的旁支在 q／p₁ 下的 residual palettes。
