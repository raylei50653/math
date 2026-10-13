# 2026-09-28：共鄰單點 34／40 來源排除與全部支援出口

接手 HEAD 為 main@104c8bc，local main 與 origin/main tracking 相同；
未重新查遠端。保留共鄰單點化約、同側限制、01／23 及 12 長弧各輪
未提交成果，接續 HANDOFF 的 34 長弧，再搬運整張來源至 40。
未 commit／push，未開 sub-agents，未重啟圖枚舉。

## 成果與界線

[新報告](../c5_adjacent_degree5_singleton_end_arc.md) 證明在明列 disk、T4、
minimal q-core 及完整 degree 前提下，唯一 mixed 共鄰 singleton x
接 34 或 40 的來源不存在。34 的 q 色框為 T={0,3}、私有外色 {1,2}，
沿用原三角形外側次序與原 r–x–B 的 K5 任意大小化約。

| 證書項目 | 結果 |
| --- | ---: |
| 每位置幾何配置（四種有序分拆） | 376、88、88、8，共 560 |
| 34 q 必要配置 | 152 |
| 34 原 x 路徑 K5／T4 排除 | 120／32 |
| 34 各分拆 q 配置數 | 80、32、32、8 |
| 34 各分拆 K5／T4 | 56／24、28／4、28／4、8／0 |
| 34 K5 後近 b4 側型數 | 8；乘兩種遠側 spoke 及 root 交換得 32 |
| 共同必拒絕 T4 列 | 01213 |
| 40 獨立重算 q 配置及 K5／T4 | 152，120／32 |
| 與前輪抽象 minimality 的逐幾何集合核對 | 1,120 |
| 整張來源反射 record／T4 核對 | 152／32 |
| K5 skeleton／刪 rx 負控制 | 各 216，34／40 各 108 |
| 每筆原 contact 方向 | 4 |
| 保留來源／新增 target 接受／未決查詢 | 0／0／0 |

最後 32 筆在 β=01213 的分量禁色全由原 actual supports 精確搬運，
兩側 residual 恆為 {0,2}、{2}（或交換），x list={0,2}；原三角形必
拒絕 β。這是來源排除，不把空保留集計作新的 target 著色見證。
40 的 q list={1,3}；反射逐筆保留完整禁色、全部接點與嵌入反向次序。
既有 source／artifacts 保持原內容；新證書不是來源可實現性證明。

外部 Dvořák Lemma 7／Theorem 10 本輪線上核對。任意大小 disk／Gallai／
minor 論證仍為紙面＋外部定理，有限域及拓撲 skeleton 由 Python 重播；
未新增 Lean theorem。

結合同側限制與 01／12／23 分離，唯一 mixed 共鄰 singleton 全部 x 支援
已接回 [條件式出口](../c5_single_sided_exit.md)；第七類已移除支援限制。
完整 Σ(M)=Ω∖{q} 仍使用雙缺失來源與刪邊繼承，不只從 T4 推出。

## 實際驗證

```bash
python3 scripts/c5_adjacent_degree5_singleton_end_arc.py --check
python3 scripts/c5_adjacent_degree5_singleton_middle_arc.py --check
python3 scripts/c5_adjacent_degree5_singleton_long_arc.py --check
python3 scripts/c5_adjacent_degree5_singleton_sectors.py --check
python3 scripts/c5_adjacent_degree5_shared_singleton.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_single_spoke_two_two_minor.py --check
python3 scripts/c5_single_spoke_two_two_external.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

八份 checker 全通過；新 JSON 與 Markdown 表逐 byte 重播相同。
`lake build` 通過（8,827 jobs），僅既存 AttachmentOrder／SymRelabel warnings。
文件檢查通過 235 份 Markdown／2,692 個本地連結；DocGraph 通過 39 份
metadata 文件／101 條關係／5 families。HANDOFF 保持 150 行。
`git diff --check` 通過；本輪五份新增 source／artifacts／report／history
另逐檔核對 trailing whitespace 與 EOF。

沿用且未重跑：唯一 degree-5 各完成表、no-spoke 大支援表、雙拒絕 atlas、
R 系列大覆蓋、抽象 profiles／閉包、圖枚舉與 Lean axiom audit。
兩份 single-spoke checker 是依賴重播，其 354／144 為歷史必要表數字，
不是本輪雙 root 剩餘數。build 不形式化新的紙面拓撲。

## 停止點

HANDOFF 下一窄題為唯一 mixed 原 K2、兩 root 各一 incidence，即
原 z–u–v–w–z 四環。先重推完整有序 R_C 與逐邊 minimality，保留
原 u、v 的全部 boundary 接線；不把 singleton 的色對或三角形公式
代入 K2。無 mixed、其他較大／多 mixed、一般雙 root、degree≥6、
一般單側／共同出口及 K∞=K≤5 保留。
