# 2026-09-24：五目標到單側出口的接合

從乾淨 `8333c62` 接手。成果見 [接合定理](../c5_single_sided_exit.md)。
完成三-spoke 核心繼承 sector 假設、五目標 Boolean 窮盡性、核心分離，
以及沿刪向核心序列取得第一個只釋放 p 的 strict step。

一般來源圖若有全 degree-4 或唯一 degree-5／三-spoke 的 minimal
q-obstruction，即有只釋放 p 的出口；其餘內點在後一型須完整 degree=4。
無條件一般出口仍未證：失敗側每個核心都必有 degree≥6、多個 degree-5，
或唯一 degree-5 且 boundary spokes≤2。既有五目標不是一般核心的完備分類。

本輪實際通過：

```bash
uv run --with networkx==3.5 python scripts/c5_sector_targets.py --check
uv run --with networkx==3.5 python scripts/c5_degree5_sectors.py --check
uv run --with networkx==3.5 python scripts/c5_degree5_interfaces.py --check
uv run python scripts/c5_sector_3703_exclusion.py --check
lake build
```

- targets：重播 4,096 個投影的五目標 screen 及既有 |C|≤3 小控制，證書一致。
- sectors：12 個位置、兩個鏡像、245,760 次完整列接合核對，證書一致。
- interfaces：108 局部控制、32 既有 disk witnesses、30,720 次固定 z
  查詢及 19,200 次 canonical deletion 核對，證書一致。
- 3703：56 bridge／33 triangle 轉移、兩個可達狀態、兩份 minor，證書一致。
- Lean build 成功（8,823 jobs），只有既有 AttachmentOrder／SymRelabel lint。

沒有新增或修改 Lean／Python／JSON。任意大小排除沿用既有紙面與外部
degree-list 依賴；本輪新結果是紙面接合，不因 build 通過就成為 Lean 定理。
未重跑雙拒絕 atlas、兩葉鏈 checker、R 系列大覆蓋或抽象閉包；未修改
603 profiles、固定點或記憶。研究完成時尚未 commit／push。

`python3 scripts/check_docs.py` 通過：139 份 Markdown、1,875 個本地連結，
含 anchors、索引與 handoff 檢查；`git diff --check` 通過。

隨後依使用者要求整理 commit + push，範圍為接合報告、研究紀錄、
README、HANDOFF、STATUS 與五份前置報告的後續入口，共十份文件。
發布前沿用上述已通過且程式／證書未變的四份 checker 與 Lean build，
重新檢查文件與 staged diff。提交後核對本地、追蹤與遠端 SHA 及工作樹；
實際推送結果以發布回覆為準。
