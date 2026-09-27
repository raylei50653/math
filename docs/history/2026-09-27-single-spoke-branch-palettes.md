# Single-spoke 旁支 palette 守恆

2026-09-27。接手 HEAD 為 `4f26efe`；原工作樹已有 single-spoke cores、
completion、bridge-path 三輪未提交 source／artifacts／文件，本輪全部保留。
即時文件已記錄 3703 與唯一 degree-5 的 t=2 指定問題完成，沒有重開舊目標。

[新報告](../c5_single_spoke_branch_palettes.md) 接續 (01,04,1234) 二接點
入口：以 rooted palette 唯一性證明同圖旁支的色 0、3 守恆，給 q 路徑
交替限制，以及五種旁支入口配對所需的 b1／b2／b4 實際接線。
任意大小由紙面歸納承擔，沿用外部 degree-list 定理；局部 Python 證書
不是來源圖枚舉或 disk 實現證明。未新增 Lean theorem。

本輪實際通過：

- `python3 scripts/c5_single_spoke_branch_palettes.py --check`：16 配對、107 closure 案例、20 路徑案例、五種 root 支援限制。
- `python3 scripts/c5_single_spoke_bridge_path.py --check`：16 tight 局部型、12 轉移。
- `python3 scripts/c5_single_spoke_completion.py --check`：繼承完整關係重播；62／20／32 分類不變。
- `python3 scripts/c5_single_spoke_cores.py --check`：必要支援表及控制通過。
- `lake build`：8826 jobs 成功；既有 AttachmentOrder／SymRelabel lint 警告。
- `python3 scripts/check_docs.py`：164 份 Markdown、2091 個本地連結通過。
- `git diff --check`：通過；本輪新增檔另核對行尾空白。

未另跑 nonadjacent／reflection standalone checker、Lean axiom audit、雙拒絕 atlas、
R 系列或一般圖枚舉。未 commit／push。
停止點仍是必要限制：52 個指定查詢未決。下一步結合五種 root 支援限制
與原 slit-disk 次序，處理帶 b3 旁支的共存問題；沒有擴大單側出口定理。
