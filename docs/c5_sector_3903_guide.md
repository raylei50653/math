# 3903 系列導讀：結論、推導順序與證據入口

文件整理：2026-09-23；研究依據截至 2026-09-22。本頁不新增研究結論。
研究優先序只見 [HANDOFF](HANDOFF.md)，全專案索引見 [STATUS](STATUS.md)。

## 1. 目前結論與最短閱讀路徑

**3903 已在指定 sector 圖類內排除。** 直接引用
[雙拒絕分類 §0–7](c5_two_rejection_proof_zh.md#0-精確命題與適用範圍)：
有限簡單圖 K 的 induced C5 為 disk 外框 Γ，內部 C 非空連通，
內點在 K 中的完整 degree≤4，且 b0 恰有兩個不同內部鄰點。
若 α=01212、δ=01213 同時拒絕，整張圖只能是分類中的二內點接線，
其十二位簽章為 1855，故不能是 3903。
此分類無須假設 minimality 或 397→330／331 交換。

只查結論時，讀「[十二列定義](c5_sector_targets.md#1-查詢域與五個目標)
→ [分類命題與證明](c5_two_rejection_proof_zh.md)
→ [Lean 支援與未形式化部分](lean_two_rejection_tools.md)」。
要追溯早期 Kempe 路線，按 §3 的表格由上而下讀。
早期各分支的排除是獨立局部成果；分類不需要把全部交換介面串成前提。

| 容易混淆的結論 | 目前範圍 |
| --- | --- |
| 指定 sector 的 3903 排除 | 已由任意大小的紙面分類涵蓋；依賴外部 degree-list 定理 |
| 指定 397/action 2→330 禁令 | 需同圖 sector 結構、兩拒絕列與指定交換；空／非空分支均已處理 |
| 不加兩拒絕列的一般 397→330 排除 | 不成立；[disk 正控制](c5_sector_corner_even_cycle.md#3-為何不能只排除單步具體-disk-正控制) 的十二位簽章為 4095 |
| 603 profiles | 原規則加單條禁令仍保留全部 603；未將後續分類編入抽象規則或重算固定點 |
| 非平面 3903 正控制 | 仍有效，與指定 disk 圖類的排除相容 |
| 完整形式化與主命題 | 九個 Lean 共用引理不是完整分類；一般單側／共同出口及 `K∞=K≤5` 仍未證 |

## 2. 符號與共同前提

| 記號 | 本系列的用法 |
| --- | --- |
| K、Γ、C | K 是含框邊的圖；Γ=(b0,…,b4)，常寫為 (0,…,4)，b0=z；C 是非空連通內部 |
| G 或 K° | 從 K 刪除 b0b1、b0b4 兩條框邊的開口圖；其餘邊保留 |
| 3903 | 十二列接受 mask，索引從 0 起算；只拒絕第 6、7 列 α、δ，其餘十列接受；不是全部十九列的完整 relation |
| 831 | 3903 在前十個 proper C5 列的 mask；另兩個查詢列接受才得到 3903 |
| 397、330、331 | 既有 catalogue 的 profile IDs，不是接受 mask 或圖的編號 |
| action 2 | 來源 397 的舊框列 01021，交換 maximal 0/1 分量 S，S∩Γ={0,1,2}；新原始列 10121，正規化為 01020 |
| B₃、空／非空分支 | B₃ 是新原始 02 圖刪去框點 1 後含框點 3 的分量；依 N_G(0)∩B₃ 是否為空分支 |
| C 的葉點與 S 的葉點 | 是不同誘導圖中的度數；w 可為二色分量 S 的葉點而 deg_C(w)=3 |

每個局部引理的完整假設仍以原報告為準；較早下界有些只需部分轉移條件，
不能反過來宣稱它們已使用全部拒絕列。跨列論證須保留同一圖、同一染色與
交換分量、具名框點（尤其 2／4）、實際 attachments、cyclic order 與中間 bridges。
兩列 lists 或兩側 root 色集不可獨立拼成新的圖見證。

## 3. 系列閱讀順序

下列表格記錄研究推進次序與各篇保留用途，不是當前待辦清單。
舊正文的「未解／下一步／未提交」按當輪語境閱讀；頁首狀態指向後續結果。

### 3.1 目標與拓撲起點

| 報告（依閱讀順序） | 保留用途與界線 |
| --- | --- |
| [五目標與十二列位元定義](c5_sector_targets.md) | 五目標的查詢投影；3903 只拒絕索引 6、7 |
| [非 disk 正控制](c5_sector_positive_control.md) | 既有 22 份控制；非平面見證不構成 disk 反例 |
| [831 與平面／disk 等價](c5_sector_structural.md) | induced 框圈＋非空連通內部下的拓撲引理 |
| [強迫連通](c5_sector_forced_connectivity.md) | 拒絕列推出必要連接；固定控制有共同路徑證書 |
| [跨列閉包與交換軌道](c5_sector_cross_row.md) | 抽象閉包與固定圖軌道分開；603 profiles 保留 |

### 3.2 單步介面與共同身份

| 報告（依閱讀順序） | 保留用途與界線 |
| --- | --- |
| [混合色對與碰撞](c5_sector_mixed_transition.md) | 同來源 profile、同交換分量仍可有不同混合後繼 |
| [帶框 incidence](c5_sector_marked_incidence.md) | 一次查詢的安全刪減；不能任意刪去無框節點 |
| [共同核心](c5_sector_common_core.md) | 舊／新兩側擴張；框分割投影不足以排除轉移 |
| [框點 4 的跨色身份](c5_sector_joint_identity.md) | 同圖聯立 retained 分量與實際鄰點；共同鄰點障礙 |

### 3.3 指定轉移的分離與下界

| 報告（依閱讀順序） | 保留用途與界線 |
| --- | --- |
| [兩種飽和 star 分離集](c5_sector_saturated_cuts.md) | 刪框點 1 未切斷時的條件式六內點下界 |
| [框點 1 切斷分支](c5_sector_frame_cut.md) | 補另一分支，合成五內點必要下界 |
| [五內點分類](c5_sector_five_inner.md) | 合成六內點必要下界，不保證可達 |
| [任意長路徑與鄰點障礙](c5_sector_neighbor_barrier.md) | 非空交集迫使飽和的二色分量葉點例外 |

### 3.4 非空交集分支

| 報告（依閱讀順序） | 保留用途與界線 |
| --- | --- |
| [葉點例外下界](c5_sector_leaf_exception.md) | 完整 degree=4 的條件式八內點下界 |
| [葉點刪除介面](c5_sector_leaf_reduction.md) | 固定染色的分割回復；非完整 Σ 壓縮 |
| [葉點接回 corners](c5_sector_leaf_corners.md) | 24 → 12 → 6 → 2 種必要次序 |
| [corner 入口分離集](c5_sector_corner_gates.md) | 兩種次序各自的必要分離條件 |
| [第一種次序偶圈排除](c5_sector_corner_even_cycle.md) | 拒絕列下排除第一種；另存簽章 4095 的 disk 單步正控制 |
| [兩拒絕列緊 lists](c5_sector_rejection_lists.md) | 第二種次序下 C 無葉；保留同一實際 attachments |
| [末端 block 接合](c5_sector_terminal_blocks.md) | 完整 root 接合＋拓撲排除指定非空分支 |

### 3.5 空交集、抽象後繼與後續涵蓋

| 報告（依閱讀順序） | 保留用途與界線 |
| --- | --- |
| [空交集身份](c5_sector_empty_branch.md) | 不借用非空分支的 b 身份，證 C 無葉 |
| [空分支末端排除](c5_sector_empty_terminal.md) | 與非空結果合成指定前提下的 397/action 2→330 禁令 |
| [全部後繼核對](c5_sector_successor_audit.md) | 十個存活後繼；單禁 330 後仍有原 603 閉合集合 |
| [331 同圖必要條件](c5_sector_331_barriers.md) | 原停止點由雙拒絕分類涵蓋；不是新的抽象閉包計算 |

### 3.6 不依賴指定交換的分類

[雙拒絕分類](c5_two_rejection_proof_zh.md) 直接分析同圖 block palettes，
涵蓋 3903 空／非空分支及原 331 同圖問題，並排除五目標中的
3647、3895、3901、3903。[Lean 共用工具](lean_two_rejection_tools.md)
列出已形式化步驟及仍在紙面／外部定理層的部分。
3703 不屬於這個雙拒絕情形；其[兩葉鏈化約](c5_sector_3703_structure.md)
由 [葉點 minor 與三列 palette 排除](c5_sector_3703_exclusion.md) 完成，
五目標皆在指定 sector 圖類內排除。研究入口仍以 HANDOFF 為準。

## 4. 證書、重播與歷史

各篇末節保留 script、artifact、依賴及當輪重播範圍。
多數使用同名 `scripts/c5_sector_<主題>.py` 與
`artifacts/c5_sector_<主題>/observations.json`；下列是容易找錯的入口：

| 報告／用途 | 程式與證書 |
| --- | --- |
| 偶圈報告中的 disk 單步正控制 | [transition_control.py](../scripts/c5_sector_transition_control.py)、[JSON](../artifacts/c5_sector_transition_control/observations.json) |
| 雙拒絕分類的獨立有限核對 | [two_rejection_audit.py](../scripts/c5_two_rejection_audit.py)、[JSON](../artifacts/c5_two_rejection_audit/observations.json) |
| 分類的 Lean 支援 | [TwoRejectionTools.lean](../Math/TwoRejectionTools.lean)、[axiom audit](../Math/TwoRejectionToolsAudit.lean) |

重播時使用各原報告的 `--check` 指令及指定依賴；有限核對不能代替任意大小
證明，`lake build` 也不表示 disk 拓撲已形式化。歷史生成命令可能覆寫 artifacts。
本次僅整理文件，未重跑研究 checker、枚舉或 Lean build。
文件檢查使用 `python3 scripts/check_docs.py` 及 `git diff --check`。

逐輪研究與提交／發布紀錄見 [STATUS_HISTORY](STATUS_HISTORY.md)：
§38–45 為目標、控制與跨列閉包，§46–52 為混合介面，§53–59 為下界與葉點，
§60–65 為非空排除，§66–70 為空分支與後繼，§71–73 為分類與 Lean 工具。
歷史快照、來源原稿和既有 artifacts 保留原貌；發布狀態以即時 Git 為準。
