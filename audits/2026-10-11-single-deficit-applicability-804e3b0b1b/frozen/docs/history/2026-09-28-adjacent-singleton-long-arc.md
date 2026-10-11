# 2026-09-28：共鄰單點 01／23 長弧分離與出口接合

接手 HEAD 為 main@104c8bc，local main 與既有 origin/main tracking 指向相同；
未重新查遠端。工作樹已有共鄰單點化約、同側限制兩輪成果，本輪保留並接續。
未 commit／push，未開 sub-agents。舊記憶中的唯一 degree-5／record 110
停止點已過時；本輪以即時 HANDOFF、STATUS 及來源報告確認目前主線。

## 成果

[報告](../c5_adjacent_degree5_singleton_long_arc.md) 證 x 接 {b0,b1} 長弧的
指定雙列延拓，完整來源反射另給 {b2,b3}。兩位置接入
[條件式單側出口](../c5_single_sided_exit.md) 第七類；這裡另明用來源雙缺失
與刪邊繼承，沒有只由 T4／指定雙列推完整 Σ。

原三角形 xzw 的內側無 unary 分量，外側 annulus 給兩 root 區塊及各側
分量／spoke 的固定長弧次序。每份 unary actual support 至少兩點；此
任意大小論證沿用外部 degree-list 定理及既有 K4 排除。雙禁色分量的每個
原 bridge 路徑塊有共同支援條件；原 r–x–b_h 提供補弧外部路徑，得到
五個互不相交的 K5 branch sets。

| 新證書項目 | 結果 |
| --- | ---: |
| 四種有序分拆的幾何支援 | 376、88、88、8，共 560 |
| q 必要支援與禁色記錄 | 692 |
| 原 x 路徑 K5／T4 排除 | 356／40 |
| 保留記錄 | 296 |
| 指定 target 接受／未決查詢 | 592／0 |
| 每筆保留的二接點方向 | 4 |
| 反射後字面 target 核對 | 592 |
| K5 skeleton／刪 rx 負控制 | 各 108 |

幾何域由兩種獨立生成法交叉核對。每筆 target 保存完整 F 候選、E 候選
及原 (z,w,x) 三色 witness。這是必要上界的接合證書，不是來源圖 cover
或可實現性證書。兩輪舊 artifacts 保持原內容；新增證書另綁定其 SHA256。

## 驗證

```bash
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

六份 checker 均通過；新 JSON 與 Markdown 表逐 byte 重播相符，每筆必要
資料亦核對回前輪抽象關係的原 index。兩份 single-spoke checker 輸出的
354／144 剩餘數是其歷史來源表，並非本輪雙 root 剩餘數。
`lake build` 通過（8,827 jobs），只有既存 SymRelabel／AttachmentOrder
linter warnings。文件檢查通過 229 份 Markdown／2,641 個本地連結；
DocGraph 通過 37 份 metadata 文件／92 條關係／5 families。HANDOFF
為 146 行。`git diff --check` 通過；未追蹤檔案另作 whitespace／EOF 核對。

外部 Dvořák 講義 Lemma 7／Theorem 10 本輪線上核對。未重跑唯一 degree-5
各完成表、no-spoke 大支援表、雙拒絕 atlas、R 系列大覆蓋、抽象 profiles／
閉包、圖枚舉或 Lean axiom audit；任意大小拓撲與 Gallai／K5 未 Lean 化。

## 停止點

唯一 mixed singleton 的非相鄰支援與 01／23 長弧已處理。下一入口為
x 接 {b1,b2} 的長弧；p₂ 的 x list 已變為 {0,3}，須保留同一來源、
原三角形、兩側區塊、全部 actual supports 及共同色框重新接合。
34／40、較大／多 mixed 分量、一般雙 root、degree≥6、一般單側／共同
出口與主命題仍未證。新結果未 Lean 化。
