# 2026-09-28：singleton-source 首橋相容性、record 87 與 18→2 查詢

接手 HEAD 為 `b770d21`，工作樹乾淨。依使用者訊息先獨立核對首橋引理，
再建立 [報告](../c5_single_spoke_first_bridge.md)、
[checker](../../scripts/c5_single_spoke_first_bridge.py)、新 JSON／套表並重播。
研究階段未 commit／push；其後使用者明確要求發布，核對範圍見末節。
本輪未改 Lean source、舊 checkers 或舊 artifacts。
README、HANDOFF、STATUS 與六份前置報告加入新入口；歷史數字保留當輪語境。

使用者附的 `/mnt/data/math_record87_first_bridge_review/` 與 ZIP 在環境中
不存在，故控制從訊息與 repo 重建，不能視為重播附件。採 document-first；
未使用 Graphify、未開 sub-agents、未重啟來源圖枚舉。

## 審核結論與套表

只由 target pair 取得原 bridge 路徑。rooted-palette 固定色守恆及唯一性
只需旁支非 root lists，不需 q 也為 pair。首橋的 q singleton palette
在兩端相同；record 87 的固定色 1、3 使首兩塊局部 E 都是 {1,β}，
β=0／2 各迫使兩端實際碰 23／34，原 spoke 接補弧給 K5。
局部 E 不是整分量 F；不要求 root list／z 色被置換固定，也不把全部
奇數 bridges 的 β 當作同一色。`joint_supports` 舊 singleton guard 不變。

一般化時明確補上端點 tightness：被刪 z 色 c 不在 root boundary 色或
旁支 palettes，故 c∈E0(q)。若 c 在兩列實際支援上固定、但不在 target
pair，直接矛盾。這個推論另外關閉六個查詢，不需要新的 topology。

18 個查詢保留原 146 組完整拒絕候選，重算前層 128 組已排除證據，
本輪再消去 16 組、剩 2 組。新增延拓分為共用 β 的 K5 10 個、端點固定色
矛盾 6 個。沒有來源移出；來源排除仍 278，保留 102 筆／51 型，A/A 100、
A/? 2。完整原記錄、接點方向、relations、前層證據與反射保存。

下一入口 record 90/p₂（282 為交換分量），支援 (0234,012)、q 禁色
({1},{2,3})；剩餘拒絕候選 ({1,2},{3})。β=2 已排除，β=0 的首兩塊
支援仍可為 {23,023,034,234,0234}：b3 必接，另需 b2 或 b0、b4。
q 色 0 不再只有唯一供應點，不能任選 b2。此候選保持未決；未證可實現性、
完整 Σ、一般 (2,2) 分離或主命題。

## 實際驗證

- 新 checker 生成與 `--check` 逐 byte 比對通過：8 個支援子集、8 個
  共用 β 有序支援配對、8,748 個固定色局部歸納、36 個 record 87 residual、
  48 個端點 tightness、24 個首橋局部控制。
- 576 個 record 87 具名 minor、1,344 個套表使用的 frame／route minor
  與 16 個負控制通過，逐份核對連通、不交、原邊與十條鄰接。
- 前置八支 checker 的 `--check` 全通過：two-arc、cross-row、frame-arc、
  two-two-external、two-two-minor、two-two、bridge-path、branch-palettes。
  原必要表重新核對 1,530 筆必要配置與 380 筆原 T4 保留。
- `lake build` 成功（8,827 jobs）；僅既有 AttachmentOrder／SymRelabel
  linter warnings，沒有新增 Lean theorem，未另作 axiom audit。
- 重讀 Dvořák 講義原 PDF，核對 Lemma 7／Theorem 10 的前提與 palette
  不交性，不需 target minimality。此為外部定理依賴。

文件檢查通過：202 頁、2,392 本地連結，包含 anchors、STATUS 索引與
150 行 HANDOFF。DocGraph 通過：26 份 metadata 文件、61 relations、
4 families，0 errors／0 notes。`git diff --check` 通過；新檔另核對 Python
語法、尾端空白與最後換行。
完整命令見報告 §6；有限控制不取代證書存在性、任意大小歸納或原圖 minor。
未重跑 dual surgery、edge-pair coordinates、circulation、雙拒絕 atlas、
R 系列大覆蓋、大圖 catalogue、其他 single-spoke 支線或全策略閉包。

## 同日發布核對

使用者其後要求 `commit + push`。發布包包含新 checker、JSON／套用表、
證明報告、研究紀錄、README、HANDOFF、STATUS 與六份前置報告的後續入口，
共 14 個檔案；研究結論與 checker 原始碼未再變動。

fetch 後起始 HEAD 與 origin/main 同為 `b770d21`，無遠端新增提交。
發布前新 checker 再次逐 byte 比對證書與輸入 SHA256，仍為新增 16 個
指定列延拓、來源排除累計 278、未決查詢 2 個。前置八支 checker 與
`lake build` 沿用本對話研究階段對相同原始碼完成的通過結果；未重跑範圍
仍如前節。文件／DocGraph 與 staged whitespace 在提交前核對；提交及
遠端結果以 Git 與發布回覆的 SHA 核對為準。
