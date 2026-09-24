# 2026-09-24：未接內點引理與兩-spoke 非相鄰型分離

接續 HEAD `9792201` 上前輪尚未提交的兩-spoke 區域成果，保留全部既有變更。
新證明見 [未接內點 boundary 引理](../c5_unattached_boundary.md)。

指定窄問題 (3)、S={b0,b3} 已完成任意大小分離：其 b4 沒有內鄰點，
接受 T4 即強迫接受全部 singleton 不在 b4 的三色列，因此恰只缺 q。
這是單缺失結論，沒有聲稱這一型不存在。
前輪 24 個必要配置中，雙缺失目標尚有 23 個未分離。

新增一般條件式出口：來源只要有一個未接內點 boundary 頂點的 minimal
q-core，就有只釋放 p 的出口，該核心的內點 degree 不受限。
反向必要條件是每個失敗側 minimal core 都碰到全部五個 boundary 頂點。
證明直接把同圖 T4 coloring 的 boundary 頂點改回，沒有新 Gallai 依賴。

實際重播：

```bash
python3 scripts/c5_unattached_boundary.py --check
python3 scripts/c5_degree5_two_spoke_sectors.py --check
lake build
python3 scripts/check_docs.py
git diff --check
```

- 新 checker 保存及重播 480 份有標號改色，並以 5,120 次完整 signature
  檢查獨立核對「刪去 boundary 座標後同一列必有相同接受值」。
- 前輪 checker 重播 80 個位置、56 份反證與 16 份既有正控制；舊證書未改。
- 新證書用 SHA256 綁定前輪證書，保存已分離一型與其餘 23 型的索引。
- `lake build` 通過（8,823 jobs），僅既有 AttachmentOrder／SymRelabel lint；
  build 不表示新紙面改色論證已 Lean 化。
- 文件檢查通過：143 份 Markdown、1,906 個本地連結，含 anchors、索引與
  HANDOFF；`git diff --check` 通過。

未新增 Lean theorem，未重跑 R10 全 checker、雙拒絕 atlas、3703、R 系列
大覆蓋或抽象閉包；603 profiles 與固定點未改。未 commit／push。
下一題是 (3)、相鄰 S={b0,b1} 的三接點六邊形區域，須保留同圖完整接點
與跨列禁色；既有二接點 C5 分類不能直接套用。

## 兩輪成果整合發布

依使用者要求將兩-spoke 區域化約與未接內點分離一併 commit + push，
範圍含兩份 checker、兩份 JSON 證書、兩份報告、兩份研究紀錄、README、
HANDOFF、STATUS 及三份前置文件的接合／後續入口。
沿用本輪已通過且程式／證書／Lean 未變的 checker 與 build 結果；
發布前重新核對文件及 staged diff。未擴大研究範圍，未重跑無關枚舉。
提交後核對本地、追蹤、遠端 SHA 及工作樹；實際推送結果以發布回覆為準。
