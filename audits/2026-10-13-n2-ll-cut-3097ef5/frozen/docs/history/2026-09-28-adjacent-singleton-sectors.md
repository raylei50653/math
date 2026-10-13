# 2026-09-28：共鄰單點同側限制與 target 重色排除

接手 HEAD 為 main@104c8bc；前輪共鄰單點的 source、artifact、報告與索引
仍在工作樹，並非乾淨起點。本輪接續保留全部前輪成果，未 commit／push，
未開 sub-agents，也未重新查遠端。研究優先序以 [HANDOFF](../HANDOFF.md) 為準。

## 結果與適用範圍

[新報告](../c5_adjacent_degree5_singleton_sectors.md) 完成原定兩個 target
重色支援的來源排除，並處理全部非相鄰 x 支援。新增論證明確使用 induced-C5
disk、T4 接受、minimal q-core 與原共鄰單點；不宣稱同樣排除一般 planar
或不接受 T4 的來源。前輪每側 (2)／(2,1) 的必要化約與 240 筆資料保持原範圍。

1. 原 zw 連通兩 root，其餘分量仍接 root，所以 H−x 連通。原弧
   b_i–x–b_j 將 disk 分兩側，整個 H−x 必在同側；全部 boundary
   支援包含於該側的閉 arc I。
2. 兩列若在 I 上相同，完整原分量 tuples、root lists、E_z、E_w 及
   root 色對關係全相同。只改 I 外框點，沿用同一份完整 coloring。
3. x 接 {b1,b4} 或 {b2,b4} 時，不論所在側，都有未接的 q 重複色框點。
   改成第四色即得到與 q 同拒絕的 T4 列，矛盾。這是來源不存在，沒有把
   x 全開誤用成 target 延拓充分條件，也不需要猜兩側 singleton 的顏色。
4. 二十個具名支援／側位置中，四個由 q 下 x 重色排除，十個由 T4
   矛盾排除。{b0,b3} 的 arc (b0,b1,b2,b3) 因 b4 未接，必只缺 q；
   剩五個相鄰長弧位置未分離。單缺失支已在出口定理既有第三類內。

新拓撲／改色證明不需 degree-list 定理，不新增 Lean theorem。disk 弧分離
由紙面證明負責，Python 不承擔任意大小 topology 或來源可實現性。

## 有限證據

[新 checker](../../scripts/c5_adjacent_degree5_singleton_sectors.py) 與
[artifact](../../artifacts/c5_adjacent_degree5_singleton_sectors/observations.json)
保存程式及直接輸入 SHA256、二十個位置、具體 T4 改色與全部相容 masks。

| 核對項目 | 數量／結果 |
| --- | --- |
| 具名 boundary pair × 所在側 | 20 |
| q 重色／T4 矛盾排除 | 4／10 |
| 單缺失／尚未分離的位置 | 1／5 |
| 兩個指定 target 支援的所在側 | 全部 4 個作來源排除 |
| 16 位置 × 1,024 signatures | 16,384 次，同 arc 限制列用全部 240 proper rows |
| {b0,b3} 保留側的相容 mask | 只有 1022 |
| 五個相鄰長弧的抽象 masks | 各 16；未作圖實現判定 |
| 原 source_index=8 的實際圖控制 | 240 列、120 份 T4 coloring、15 份刪邊 q-coloring |

source_index=8 取自原單 root 介面 artifact。新 checker 重新核對其 sphere
rotation／apex 五個三角面，證原圖具有指定 C5 disk 嵌入。該圖 separator
接 b1,b4，刪去後兩分量分居兩側，全部框點被碰到，且只缺 q，說明不能
移除 H−x 連通假設。separator degree=5，並非本輪雙 root 圖類反例。

## 驗證與未重跑範圍

```bash
python3 scripts/c5_adjacent_degree5_singleton_sectors.py --check
python3 scripts/c5_adjacent_degree5_shared_singleton.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_unattached_boundary.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

四份 checker 均已重播；前三份保留原報告各自的證據層，未接內點 checker
輸出的 23 個未解配置是其歷史來源表，並非當前雙 root 剩餘位置數。
`lake build` 通過（8,827 jobs），只有既存 AttachmentOrder／SymRelabel
linter warnings；建置不表示新紙面結果已 Lean 化。
文件檢查通過 226 份 Markdown／2,619 個本地連結；DocGraph 通過
36 份 metadata 文件／88 條關係／5 families。HANDOFF 為 141 行。
`git diff --check` 通過，另逐一核對本輪與前輪共八份 untracked 檔案的
whitespace／EOF，全部通過。新 artifact 生成後逐 byte 重播相符。

未重跑唯一 degree-5 各完成表、三接點／no-spoke 外部路徑 checker、
R 系列大覆蓋、雙拒絕 atlas、抽象 profiles／閉包、圖枚舉或 Lean axiom audit。
原單 root 大證書只重播上述指定圖，不宣稱整份 source catalogue 重新驗證。

## 精確停止點

disk＋T4 下，唯一 mixed 共鄰 singleton 的非相鄰 x 支援已處理。
下一題固定 x 接 {b0,b1} 的長弧，保留原六邊形框、zw、每側 (2)／(2,1)
及實際 root-spoke／unary 支援；三列 x list 皆為 {2,3}，但 target 的
兩個 E 必從原分量重新求，不能沿用 q 的私有色條件。
五個相鄰長弧、較大／多 mixed 分量、一般雙 root、一般出口及主命題仍未證。
