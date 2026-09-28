# 2026-09-28：共鄰單點 12 長弧分離與出口擴充

接手 HEAD 為 main@104c8bc，local main 與 origin/main tracking 相同；
未重新查遠端。工作樹已有共鄰單點化約、同側限制、01／23 長弧三輪
未提交成果，本輪保留並接續即時 HANDOFF 指定的 12 長弧。
未 commit／push，未開 sub-agents，未重啟圖枚舉。

## 成果與界線

[新報告](../c5_adjacent_degree5_singleton_middle_arc.md) 證在明列 disk、T4、
minimal q-core 與完整 degree 前提下，唯一 mixed singleton x 接 {b1,b2}
必接受 p₁=01021、p₂=01212。q=01012 固定，以新長弧 (2,3,4,0,1)
重算原 supports；沒有旋轉支援卻忘記 q 色框。

任意大小覆蓋沿用原三角形外側 annulus、兩 root 區塊、每份 unary
至少兩個 actual support、原 r–x–b_h 的 K5 minor。有限接合始終使用
整份 F 集合及原 (z,w,x) 三色 witness，p₂ 的 x list 是 {0,3}。
外部 Dvořák Lemma 7／Theorem 10 本輪線上核對；未新增 Lean theorem。

| 證書項目 | 結果 |
| --- | ---: |
| 幾何支援（四種有序分拆） | 376、88、88、8，共 560 |
| q 必要記錄 | 728 |
| 原 x 路徑 K5／T4 排除 | 320／112 |
| 保留記錄 | 296 |
| 保留分拆計數 | 144、72、72、8 |
| 指定 target 接受／未決查詢 | 592／0 |
| 每個 target 的候選 E 色對 | 456，全部有三色 witness |
| 每個 target 含非精確搬運分量的記錄 | 40 |
| 二接點方向／每筆 | 4 |
| 自反射字面 target 核對 | 592 |
| K5 skeleton／刪 rx 負控制 | 各 108 |
| 錯用 q 的 x list 負控制 | 2 |

每筆保留前輪抽象關係 index，幾何域另由 Cartesian hull 分離獨立核對。
反射同步搬運原支援、q 禁色、單位次序、接點方向及字面 target；12 支援
保持不變，沒有額外解決另一個長弧。必要資料與 skeletons 都未證來源
實現性；新 artifact 另存，前輪 source／artifact 保持原內容。

在出口的雙缺失來源與刪邊繼承前提下，新增 12 分離給 Σ(M)=Ω∖{q}，
故 [條件式出口](../c5_single_sided_exit.md) 第七類擴為 01／12／23。
一般 T4 來源本輪只證指定雙列，未另分類完整 Σ。

## 實際驗證

```bash
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

七份 checker 全通過，新 JSON 與 Markdown 表逐 byte 重播相同。
兩份 single-spoke checker 的 354／144 是其歷史必要表，不是雙 root 剩餘數。
`lake build` 通過（8,827 jobs），僅既存 AttachmentOrder／SymRelabel warnings。
文件檢查通過 232 份 Markdown／2,668 個本地連結；DocGraph 通過 38 份
metadata 文件／96 條關係／5 families。HANDOFF 為 150 行。
`git diff --check` 通過；本輪新增的四份 source／artifact／report 加一份
history 另逐檔檢查 trailing whitespace 與 EOF。

沿用且未重跑：唯一 degree-5 各完成表、no-spoke 大支援表、雙拒絕 atlas、
R 系列大覆蓋、抽象 profiles／閉包、圖枚舉與 Lean axiom audit。
build 不表示 annulus、Gallai 或任意大小 K5 論證已形式化。

## 停止點

下一入口 x 接 {b3,b4}，長弧 (4,0,1,2,3)。三列的 x list 都為 {0,3}，
q 的 T 外色改為 {1,2}；須以相同原三角形及 root 區塊重算完整支援和
禁色，再以整張來源反射搬至 40。一般雙 root、較大／多 mixed 分量、
degree≥6、一般單側／共同出口及 K∞=K≤5 仍未證。
