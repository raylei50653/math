# 2026-09-24：唯一 degree-5 的兩-spoke 區域化約

從乾淨 HEAD `9792201` 接續 HANDOFF 指定的 t=2、(3)／(2,1) 缺口。
成果見 [必要位置定理](../c5_degree5_two_spoke_sectors.md)。
未重啟圖 catalogue 或 R31 長來源問題。

新增同圖色置換搬運引理及可重播位置反證：80 個具名配置中，36 個因
穩定子矛盾、20 個因必拒絕 T4 排除；留下 (3) 的 6 個、(2,1) 的 18 個。
這是任意大小來源的必要位置分類，不是留下配置的實現性或核心分離定理。
新增 checker 只需 Python 標準函式庫，不使用 planarity oracle。

沿用 R10 的 16 個 (2,1) 單缺失 disk witnesses，以完整分量 colorings
獨立重算全部 240 列禁色與 relation，共 3,840 個整圖列核對。
它們匹配留下配置中的四個具名配置，不冒充全部 24 個配置的正控制。
來源 SHA256 與 witness indices 保存於新證書；disk rotation 沿用 R10。

本輪實際通過：

```bash
python3 scripts/c5_degree5_two_spoke_sectors.py --check
uv run --with networkx==3.5 python scripts/c5_degree5_interfaces.py --check
lake build
```

- 新 checker：80 配置、56 份排除反證及 16 份既有正控制，JSON 逐 byte 一致。
- R10：108 局部控制、32 disk witnesses、30,720 固定 z 查詢、
  19,200 canonical deletion 查詢通過。
- Lean：8,823 jobs 成功，僅既有 AttachmentOrder／SymRelabel lint。
  沒有新增 Lean theorem；build 不形式化新紙面區域論證。

未重跑 sector 五目標、3703、雙拒絕 atlas、R 系列大覆蓋或抽象閉包。
603 profiles、固定點及既有 JSON 未改。尚未 commit／push。
下一題：處理 (3) 唯一非相鄰型 S={b0,b3}，其 C5 區域的 z 有三個
內接點，F_C(q)={2,3}；仍須保留 z=0、1 的開口查詢及同圖跨列條件。

文件檢查通過：141 份 Markdown、1,890 個本地連結，含 anchors、索引與
HANDOFF 檢查；`git diff --check` 通過。
