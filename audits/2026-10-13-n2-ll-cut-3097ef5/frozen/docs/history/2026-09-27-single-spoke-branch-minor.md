# Single-spoke 旁支 K5 minor 與指定 p₁ 延拓

2026-09-27。接手時工作樹已有 cores、completion、bridge-path、branch-palettes
四輪未提交成果，本輪保留。未 commit／push。

[新報告](../c5_single_spoke_branch_minor.md) 證明指定 (01,04,1234)、禁 3
者二接點分支接受 p₁。主路徑任一奇數位置 bridge 的兩端，連同各自的
全部旁支，都碰到 b2 及同一 b1／b4；其餘 cycle 路徑與其他兩分量的
實際 z–b1、z–b4 路徑完成同圖 K5 minor。所有 b3 旁支均可保留在
原所屬 branch set，不需大小界、任意加邊或獨立端點 marginals。

新證書覆蓋 20 個局部支撐型及 360 份抽取形狀的 K5 控制；後者不是
完整 degree／list 來源圖。任意大小由紙面抽取證明承擔，外部 degree-list
定理沿用既有報告，未新增 Lean theorem。

只更新原 source_index 24、29 的 p₁ 查詢（交換單接點名字）；114 筆
現為 64 筆兩列皆已證、20 筆只證 p₁、30 筆只證 p₂，50 個指定查詢未決。
原 completion 證書與較早支援證書保持原樣，新表另存輸入 SHA256。

本輪實際通過：

- `python3 scripts/c5_single_spoke_branch_minor.py --check`：20 個局部型、360 份 K5 控制、64／20／30 查詢統計。
- `python3 scripts/c5_single_spoke_branch_palettes.py --check`：16 配對、107 closure、20 路徑型及五種必要支援。
- `python3 scripts/c5_single_spoke_bridge_path.py --check`：16 tight 型與 12 轉移。
- `python3 scripts/c5_single_spoke_completion.py --check`：原 3,492 項完整關係與 62／20／32 歷史表保持一致。
- `python3 scripts/c5_single_spoke_cores.py --check`：原支援表與控制通過。
- `lake build`：8826 jobs 成功；既有 AttachmentOrder／SymRelabel lint 警告。
- `python3 scripts/check_docs.py`：166 份 Markdown、2107 個本地連結通過。
- `git diff --check`，以及本輪新增檔的行尾空白檢查通過。

未另跑 nonadjacent／reflection standalone checker 或 Lean axiom audit。
前述 build 僅驗證既有 Lean 專案，本輪紙面拓撲結果未 Lean 化。

下一入口是 (012,04,234)、禁 3 者二接點的 p₂，原 index 23／28。
completion 已控制 C₃ 不禁 0、3，尚需分析 C₁ 的單接點完整關係及原嵌入。
未重啟 t=2、R 系列、atlas 或一般圖枚舉；未擴大一般單側出口定理。
