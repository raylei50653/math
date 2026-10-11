# C₅ class 兩點重疊：研究設計與交接整理

2026-09-30。Git 基準 `e700ff91e0b24ed432dc23c5713f3a4a3f8e226a`。
本整理輪開始時工作樹乾淨，`git status` 顯示 main 與本地 origin/main
無分歧；沒有 fetch 或遠端 SHA 驗證。

使用者先要求討論研究設計、不改檔，後續明確要求把資料與接手狀態
整理供新對話使用。本輪依後者新增連接文件與小型點對索引；不展開
八點後繼搜尋。早先輪次中的 P₃ 未提交狀態不是本輪起始狀態。

## 保存內容

- [專題報告](../c5_two_vertex_overlap.md)保存使用者指定的「兩個 C₅
  各取兩點識別」、接合前提、完整八點語義、單側投影公式與拓撲界線。
- [導覽](../c5_two_vertex_overlap_guide.md)維護停止點及一次精確接合的
  下一步；HANDOFF 新增此研究線，既有 weak-deletion 標記保留。
- [Checker](../../scripts/c5_two_vertex_overlap.py)及
  [artifact](../../artifacts/c5_two_vertex_overlap/pair_interfaces.json)保存
  全部 132 類／1,320 點對、子 masks、完整五點染色 witnesses、來源 SHA。

相鄰點對 660 份全強迫異色；對角點對 35 份強迫異色、625 份自由。
無空接口或強迫同色接口。全部點對允許異色，加上紙面相容引理，只能
推出既有 class 的指定兩點接合染色非空；不證拓撲合法或多步充分。

## 驗證範圍

```bash
python3 scripts/c5_two_vertex_overlap.py
python3 scripts/c5_two_vertex_overlap.py --check
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

產生及只讀逐 byte 重播已通過。Checker 以全部 240 個 labeled proper
C₅ 賦色獨立核對十種色型及 1,320 份 pair projection，另核對 87 個
library ID／完整 patterns 與 catalogue 一致。750 條規則只清點數量，
未重驗其最小性；132 類來源圖的實現與目錄完備性亦沿用原證據。

Artifact 為 544,201 bytes，低於大型 artifact 門檻，不改 manifest。
本輪不修改 Lean；整理輪不重跑 `lake build` 或 Lean audit，也不重跑
來源圖染色、disk embedding、cell 枚舉、weak-deletion 或其他研究家族。
紙面引理、既有 Lean 基礎、Python 資料重播與未證拓撲各自標示。

文件檢查通過 364 份 Markdown／3,717 個本地連結；DocGraph 通過
62 documents／213 relations／5 families，零 errors／notes。
`git diff --check` 通過，新檔另查尾端空白及最終換行。
另核對全部 132 個代表的 `edges` 都未含 C₅ 框邊，以及 R1023 在
`(0,2)` 異色篩列後確為 R1016；未把這兩項稱為整圖重播。
沒有 commit／push、沒有使用 Graphify、沒有開 sub-agents，沒有更新 Codex 記憶。
