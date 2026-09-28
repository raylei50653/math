# 2026-09-28：相鄰雙 degree-5 九組成果整理與發布驗證

本次依使用者「整理目前進展後 commit + push」要求，整理基準
`104c8bcccb32486dbddd7d23183c47b0c7282526` 上的九組既有未提交成果。
發布前以 `git ls-remote origin refs/heads/main` 核對遠端仍在此基準。
本次沒有推進新數學結論；目前研究優先序見 [HANDOFF](../HANDOFF.md)，
最終提交及遠端狀態以 Git 為準。

## 成果與停止點

以下均限各報告明列的原圖、minimality、degree 與 disk 前提；保留同一
來源的完整有序關係、全部接點、實際支援、環序及共同色框。

| 成果 | 本次保留的精確結論 |
| --- | --- |
| [唯一共鄰單點化約](../c5_adjacent_degree5_shared_singleton.md) | 每側 t≤1，只剩 (2)／(2,1)；375 筆關係資料經原 x 路徑 K5 留 240 筆必要資料 |
| [共鄰單點同側限制](../c5_adjacent_degree5_singleton_sectors.md) | 20 個支援／側位置排除 14，03 唯一保留側只缺 q；5 個相鄰長弧由後續完成 |
| [01／23 長弧](../c5_adjacent_degree5_singleton_long_arc.md) | 692 筆必要支援，K5／T4 排除 356／40；296 筆、592 查詢全接受，整張來源反射至 23 |
| [12 長弧](../c5_adjacent_degree5_singleton_middle_arc.md) | 728 筆必要支援，K5／T4 排除 320／112；296 筆、592 查詢全接受，保留 p₂ 的 x list={0,3} |
| [34／40 長弧](../c5_adjacent_degree5_singleton_end_arc.md) | 每位置 152 筆，K5／T4 排除 120／32；結合前序完成 singleton 全支援，接入出口第七類 |
| [Mixed K2 各一接點化約](../c5_adjacent_degree5_mixed_edge.md) | 完整關係與逐邊 minimality 強迫一色／兩色 residual；816 筆資料經原路徑 K5 留 576 筆 |
| [原四環次序排除](../c5_adjacent_degree5_mixed_edge_order.md) | 576 筆中 552 筆超周長，24 筆飽和次序矛盾；各一接點型全部 disk 來源排除，不需 T4 |
| [Mixed K2 共鄰端點化約](../c5_adjacent_degree5_mixed_edge_shared.md) | 原 root incidences 恰為 zu、zv、wu；z 無 spoke、唯一二接點 unary，w 容量飽和；306 筆留 288 筆，9,312 完整 q schemas 保持 |
| [共鄰端點 w 側兩條 spoke](../c5_adjacent_degree5_mixed_edge_shared_t2.md) | t_w=2、(1) 的原 18 筆接合 280 份幾何成 38 筆必要支援；76 查詢及 202 組完整禁色候選全接受，不需 T4，接入出口第八類 |

下一窄入口仍是 **共鄰端點型 t_w=1、(2) 的 36 筆**。保留兩份二接點
完整關係、原 diamond 外側環序與 w-spoke，再用飽和雙禁色的原 bridge／
逐塊 actual supports 處理同圖跨列；不重啟唯一 degree-5 或大圖枚舉。

本次一併發布九份 checker、九組 JSON／必要表、九份報告及各輪歷史，
同步 README、STATUS、HANDOFF、degree-5 導讀、介面及條件式出口。
HANDOFF 將重複摘要收斂為成果表，保持 140 行；修正現況入口中已被後續
涵蓋的待辦，補上出口第八類。原各輪 artifact 數字與歷史「未提交」保持
當輪語境，沒有重新生成證書。

## 本次實際驗證

九份新 checker 與既有相鄰雙 root 介面 checker 全數通過；JSON 與適用的
Markdown 表均由 `--check` 重算並逐 byte 比較一致。

```bash
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_adjacent_degree5_shared_singleton.py --check
python3 scripts/c5_adjacent_degree5_singleton_sectors.py --check
python3 scripts/c5_adjacent_degree5_singleton_long_arc.py --check
python3 scripts/c5_adjacent_degree5_singleton_middle_arc.py --check
python3 scripts/c5_adjacent_degree5_singleton_end_arc.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_order.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t2.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
git diff --cached --check
```

`lake build` 通過（8,827 jobs），只有既有 AttachmentOrder／SymRelabel
linter warnings；未修改 Lean 源碼或新增 theorem。文件檢查通過 248 份
Markdown／2,791 個本地連結；DocGraph 通過 43 份 metadata 文件、117 條
關係、5 families，零錯誤。整理後重新核對 43 個證書輸入雜湊，全數相符；
工作樹與暫存區 `git diff --check` 均通過。發布包共 50 份檔案。

未另跑唯一 degree-5 完成表及其全部依賴 checker、雙拒絕 atlas、R 系列
大覆蓋、抽象 profiles／閉包、來源圖枚舉或 Lean axiom audit；未重新
查閱外部定理。未列出的證據沿用各原研究紀錄；本次發布重播不代表
重新驗證整個專案或任意大小紙面證明。

任意大小結論仍由紙面論證及外部 degree-list 定理承擔；Python 是固定域
控制，必要表與 minor skeletons 不是 disk 可實現性證書，`lake build`
不形式化新拓撲。完整 Σ 的出口接合另用來源雙缺失及刪邊繼承。
其餘 w 分拆、其他 mixed、一般雙 root、degree≥6、非相鄰 roots、一般
單側／共同出口與 `K∞=K≤5` 仍未證。
