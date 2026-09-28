# 文件狀態與可能變化追蹤

文件更新與研究依據：2026-09-28。
本頁維護研究狀態與完整報告索引；**優先順序只以 [HANDOFF](HANDOFF.md) 為準**。
兩-spoke 全部 (3) 型，以及 S={b0,b1}、S={b1,b2}、S={b2,b3} 各兩種 (2,1) 次序已排除。剩四個相鄰表項已有 split-support 完整列分類，兩次序皆只缺 q；八個非相鄰表項已證指定 p=01021、01212 可延拓；唯一 degree-5 的 t=2 全支已接回單側出口。single-spoke 已有四型必要覆蓋與 (2,1,1) 的 19 種必要支援型；外部雙路徑 completion、旁支 K5 minor 與單接點未用色守恆（含全表掃描）之後，二接點上界分類再關閉 18 個查詢；其後單接點 root 接線／禁色角色守恆關閉最後 16 筆，114 筆全部兩列已證；(2,2) 必要分類、框弧／兩框弧 K5、跨列 residual 與首橋相容性後剩 102 筆／51 型，其中 100 筆雙列已證，僅 record 90／282 各剩 p₂，但可實現性與完整分離仍開放；一般單側出口與 R31 來源 minor 缺口保留。
2026-09-28 的 [singleton-source 首橋相容性](c5_single_spoke_first_bridge.md) 已證 record 87 的 p₂，套剩餘 18 查詢新增 16 個延拓：10 個由共用首橋 palette 的 K5、6 個由端點固定色矛盾。來源排除仍 278 筆，保留 102 筆／51 型，100 筆雙列已證、2 個查詢未決。舊 `joint_supports` 的 singleton 限制保留；新層分開保存局部 E 與整分量 F，全部 β／完整拒絕候選排除才接受。
逐輪數字、驗證與發布紀錄已移至 [歷史快照](STATUS_HISTORY.md)。

## 1. 閱讀順序與文件角色

| 需求 | 入口 |
| --- | --- |
| 接續研究、找停止點與最小重播 | [HANDOFF](HANDOFF.md) |
| 查證結論及證據 | 本頁 §2 專題索引；詳細前提、證書與 theorem 以報告為準 |
| 看後續成果與保留缺口 | 本頁 §3–4 |
| 更新文件 | [文件維護規則](DOCUMENTATION.md) |
| 查當時的研究／發布狀態 | [研究歷史](STATUS_HISTORY.md)；即時提交狀態查 Git |

「已完成」僅限明列前提；紙面、外部定理、Python 有限證書、Lean 普通證明與
`native_decide` 分開標示，不能從有限控制外推一般 disk 或完整 Σ 結論。

## 2. 專題文件全索引

### 2.1 目前主線：weak deletion 與 minimal obstruction

以下結論僅在各報告明列的圖類與前提下成立；當前研究優先序只見 HANDOFF。

| 文件 | 現況與剩餘界線 |
| --- | --- |
| [Single-spoke (2,2) singleton-source 首橋相容性](c5_single_spoke_first_bridge.md) | record 87 的 p₂ 已證；首橋共用 β 與端點固定色共證 16 個 target；來源排除仍 278，102 筆／51 型中 100 筆 A/A，僅 90／282 的 p₂ 未決；紙面＋外部定理＋Python，未 Lean 化 |
| [Single-spoke (2,2) 兩框弧 K5](c5_single_spoke_two_arc.md) | 同一份兩弧分割與另一原分量納入 Z；record 17 雙列已證，新排除 6 筆來源、另證 20 個 target；當輪 102 筆、84 筆 A/A、18 查詢，後由首橋層更新為 100 筆 A/A、2 查詢；未 Lean 化 |
| [Single-spoke (2,2) 跨列 residual](c5_single_spoke_cross_row.md) | 同圖共用原 bridge 路徑的雙列 residual 換色相容性；record 16 的 p₁ 已證，新增 16 個 target；當輪 108 筆／54 型、74 筆 A/A、50 查詢，後由兩框弧／首橋層更新為 102 筆、100 筆 A/A、2 查詢；未 Lean 化 |
| [Single-spoke (2,2) frame-arc K5](c5_single_spoke_frame_arc.md) | 三段具名框弧及任意兩路徑塊 minor；record 15 的 p₂ 已證，另排除 36 筆來源、另證 18 個 target；當輪剩 108 筆／54 型、58 筆 A/A、66 查詢，後由跨列／兩框弧／首橋層更新至 102 筆、100 筆 A/A、2 查詢；任意大小紙面＋外部定理，未 Lean 化 |
| [Single-spoke (2,2) 外部路徑接合](c5_single_spoke_two_two_external.md) | record 104 的原分量路徑接至補弧，逐塊相鄰支援對 K5 再排除 210 筆；當輪剩 144 筆／72 型，後由框弧層降至 108；186 支援式、496 minor 控制，任意大小紙面證明，未 Lean 化 |
| [Single-spoke (2,2) 路徑塊支援 K5](c5_single_spoke_two_two_minor.md) | 雙禁色 residual 的逐塊穩定子與實際 b3、b4 接線，來源 K5 排除 record 110、119 及 26 筆；當輪剩 354 筆，後由外部路徑接合降至 144；48 局部式、192 支援式、256 minor 控制，未 Lean 化 |
| [同染色 dual 路徑有序重接](c5_dual_path_surgery.md) | 任意大小一步精確公式；同圖三配對同 state／不同後繼反例；record 110 的 α 配對及共同必要等式，來源已由後續 K5 排除；56 個既有圖、8,420 個混合更新重播，有限可迭代 state 未證 |
| [Single-spoke (2,2) 必要分類](c5_single_spoke_two_two.md) | 完整二元 relation schemas、actual supports、全部接點方向及奇數 bridge 化約；1,530 必要候選、原 T4 保留 380 筆／190 型，框弧／兩框弧 K5、跨列 residual 與首橋相容性後剩 102 筆／51 型，其中 100 筆雙列已證、2 查詢未決；可實現性／完整分離未證 |
| [Single-spoke 剩餘單接點上界分類](c5_single_spoke_single_contact_bounds.md) | 16 筆皆有 F_C(p)⊆{3}；12 個 p₁ 取 z=2、4 個 p₂ 取 z=0；114 筆雙列全證，root 接線局部分類及任意大小守恆，未 Lean 化 |
| [Single-spoke 剩餘二接點上界分類](c5_single_spoke_two_contact_bounds.md) | 18 查詢分為 9 組／6 幾何 orbits；容量 4、外部路徑 K5 6、未用色對 bridge 障礙 8 全部關閉；該輪 98 筆雙列已證，剩餘 16 筆由單接點分類關閉，未 Lean 化 |
| [Single-spoke root 守恆全表掃描](c5_single_spoke_root_sweep.md) | 通用單接點條件套用全部 228 查詢，新增 14 個接受；該輪 80 筆兩列已證、34 查詢未決，後由二接點及單接點分類完成 114／0；紙面引理＋有限上界計算，未 Lean 化 |
| [Single-spoke 單接點未用色守恆](c5_single_spoke_root_conservation.md) | 指定 (012,04,234) 二接點分支已證 p₂ 延拓，取 z=3；任意大小 root palette 歸納，該輪 66 筆兩列已證，後由全表掃描增至 80 筆、34 查詢未決，未 Lean 化 |
| [Single-spoke 旁支 K5 minor](c5_single_spoke_branch_minor.md) | 指定 (01,04,1234) 二接點分支已證 p₁ 延拓；任意大小同圖 K5 抽取、20 局部型與 360 份拓撲控制；該輪 64 筆兩列已證，後由單接點守恆增至 66 筆、48 查詢未決，未 Lean 化 |
| [Single-spoke 旁支 palette 守恆](c5_single_spoke_branch_palettes.md) | 色 0、3 守恆給 q 路徑交替限制，以及五種旁支入口 palette 配對與必要實際接線；任意大小必要限制；後由旁支 K5 minor 證指定分支 p₁ 延拓，未 Lean 化 |
| [Single-spoke 雙禁色 bridge 路徑](c5_single_spoke_bridge_path.md) | 指定未決分支的兩接點間必為奇數 bridge 路徑，b3 接線全在旁支；任意大小必要化約；後接旁支 K5 minor 完成指定 p₁，未 Lean 化 |
| [Single-spoke 外部雙路徑 completion](c5_single_spoke_completion.md) | 任意大小來源 minor 接回既有 degree-4 分類；該輪新增 30 個接受查詢，62 筆兩列已證，後由旁支 K5 minor 與單接點守恆增至 66 筆；紙面證明與繼承 3,492 項完整關係重播，未 Lean 化 |
| [Single-spoke 覆蓋與嵌入必要化約](c5_single_spoke_cores.md) | 四型覆蓋與反射；(2,1,1) 任意大小化為 19 必要支援型，原 114 具名配置有 40 筆兩個 p 延拓，後由 completion、旁支 K5 minor 與單接點守恆增至 66 筆；完整關係與接點角色保留，未證全部 t=1 |
| [非相鄰 two-spoke 出口分離](c5_two_spoke_nonadjacent.md) | 四代表接受兩個指定 p，另四項僅反射；74 個保留 z 的正常形增邊候選與 3,492 個 completion 接線；紙面任意大小化約、Python 完整接點證書、Lean 列代數及搬運 |
| [split-support 相鄰 (2,1) 完整列分類](c5_two_spoke_split_support.md) | 兩接點次序皆單缺失；64 個 A disk forms、252 個 D 例外接線；保留完整 tuples，反射側只搬運，紙面任意大小化約＋Lean 有限列代數 |
| [q-preserving 反射與下一相鄰 orbit](c5_two_spoke_reflection.md) | Lean ordered-relation／禁色搬運；S={b2,b3} 兩項由既有排除搬運；下一 orbit 的 split-support 紙面定理與八個 disk 控制；單缺失已由後續完整列分類完成 |
| [中間相鄰兩分量 (2,1) 排除](c5_two_spoke_middle_21.md) | S={b1,b2} 兩次序皆排除；三外部 branch sets 加 palette {3} bridge／leaf odd cycle 給同圖 K5，保留兩分量關係，未 Lean 化 |
| [相鄰兩分量 (2,1) 排除](c5_two_spoke_adjacent_21.md) | S={b0,b1} 的兩種禁色次序皆不可能；兩個不同分量提供 odd cycle 與 z–b4 路徑，實際雙色 tethers 給 K5 minor；未 Lean 化 |
| [三接點兩-spoke 排除](c5_two_spoke_three_contacts.md) | 同圖 palette 差強迫 triangle／三臂及實際 boundary tethers，K5 minor 排除全部 (3)；任意長度紙面證明＋局部證書，未 Lean 化 |
| [未接內點 boundary 引理](c5_unattached_boundary.md) | 完成兩-spoke 非相鄰 (3) 單缺失分離；一般失敗側每個核心必碰全部五個 boundary 頂點，內點 degree 不限 |
| [兩-spoke 區域化約](c5_degree5_two_spoke_sectors.md) | t=2 的 (3)／(2,1) 任意大小必要位置分類；56 個排除、24 個保留；全部 (3) 由後續 K5 minor 排除，其後 S={b0,b1}、S={b1,b2} 的四個 (2,1) 表項亦已排除 |
| [單側出口接合](c5_single_sided_exit.md) | 五目標窮盡與來源假設已接通；有全 degree-4、唯一 degree-5／二或三-spoke 或未接內點 boundary 核心即有單側出口，一般版未證 |
| [3703 任意長度排除](c5_sector_3703_exclusion.md) | 葉點 minor 加三列 palettes 排除兩種剩餘鏈；完成指定圖類的五目標，紙面＋外部 degree-list＋局部證書，未 Lean 化 |
| [C5 雙拒絕分類](c5_two_rejection_proof_zh.md) | 指定 disk／degree≤4／兩接點圖類內，雙拒絕強迫二內點 1855；排除四個目標；3703 由三拒絕續作排除，紙面未 Lean 化 |
| [3703 兩葉鏈化約](c5_sector_3703_structure.md) | 三拒絕迫使 bridges／互斥 triangles 的 block 鏈；兩葉只剩 012／234 或 024／234，b0 第二接點在鏈內；剩餘兩型已由 [排除報告](c5_sector_3703_exclusion.md) 處理 |
| [397/action 2 全部後繼](c5_sector_successor_audit.md) | 十個存活候選，禁 330 後可換 331；單條禁令下 603 最大閉合集合不變，331 同圖分支已由雙拒絕分類涵蓋；固定域計算仍保留 |
| [3903 空分支末端排除](c5_sector_empty_terminal.md) | 空／非空合成排除指定 397→330 轉移；需 sector 結構與兩拒絕列，一般 3903 在指定 sector 圖類內已由雙拒絕分類排除 |
| [3903 空交集分支](c5_sector_empty_branch.md) | δ(C)≥2；舊色 1 的 0 鄰點恰有框鄰集 {0}，內部度數 3；末端 block 拓撲合成由 [空分支末端報告](c5_sector_empty_terminal.md) 完成 |
| [3903 末端 block 介面](c5_sector_terminal_blocks.md) | 兩列完整 root 接合、實際 attachments 與末端 blocks 的 disk 障礙，排除指定非空分支；空交集由後續末端報告處理；一般 3903 在指定 sector 圖類內由雙拒絕分類涵蓋 |
| [同末端不同二接點正常形](c5_degree5_same_terminal_triangles.md) | R31：408 模板／327,968 接線非 disk；任意長來源 minors 待補，列為保留缺口，非目前優先入口 |
| [中間二接點來源 minors](c5_degree5_middle_cycle_minors.md)、[中間 C5 正常形](c5_degree5_middle_pentagon.md) | R29–R30：正常形覆蓋與 boundary 固定來源 minors 合成，排除任意長中間不同二接點鏈型 |
| [三環鏈全部接點位置](c5_degree5_three_cycle_positions.md) | R28 完整 list 接合；不同點 F={D}，同點保留完整 F；中間二接點圖層由 R29–R30 補完，同末端由 R31 完成正常形 |
| [末端二臂來源 minors](c5_degree5_three_cycle_minors.md)、[三個 triangle 正常形](c5_degree5_three_triangles.md)、[三環鏈 root](c5_degree5_three_cycle_roots.md) | R25–R27：完整接合、正常形與來源 minors 已接通，排除末端各一臂的任意長共用點鏈型；一般三環未完成 |
| [共用點雙奇環來源 minors](c5_degree5_shared_cycle_minors.md)、[共用點四列介面](c5_degree5_shared_cycle_roots.md) | R23–R24：四列布林縮環與真正來源 minors 分開驗證；結合互斥型完成恰兩個 odd-cycle blocks，完整 root／交集不保持 |
| [互斥雙長環](c5_degree5_two_long_cycles.md)、[混合雙環來源 minors](c5_degree5_long_triangle_minors.md)、[混合雙環 root](c5_degree5_long_triangle_roots.md) | R20–R22：混合 root 介面、來源 minors 與連續縮減已接通，互斥雙環任意長度排除 |
| [標記路徑 minor 與同點排除](c5_degree5_bridge_mark_minors.md) | 1,044 型／571,400 接線完整非 disk 覆蓋；198 長來源／432 次真正 minors；結合 R15–R17 排除恰兩個 triangles；含長環後由 R21–R24 補完 |
| [同點接入標記介面](c5_degree5_bridge_marks.md) | 36 組 root 查詢、858＋186 型及 12,711 次色序列縮減；來源 minors 與拓撲覆蓋由 R19 補完 |
| [互斥雙環任意外臂](c5_degree5_bridge_arms.md) | 兩側不同環點接入的任意外臂排除；36,672 模板／246,645,568 接線完整覆蓋，同點接入後由 R18–R19 補完 |
| [互斥雙環 bridge](c5_degree5_bridge_triangles.md) | 同側接點化回單環；直接私有接點子型任意長 bridge 排除，132 模板／43,696 lifts 非 disk；剩餘外臂位置後由 R17–R19 補完 |
| [單邊刪除](c5_disk_deletions.md)、[A/B weak successors](c5_disk_weak_successors.md) | 同 Σ 不決定完整單步後繼；指定 A/B 的 silent closure／weak successors 已核對，不能外推全部圖 |
| [完整 k≤3 audit](c5_weak_deletion_audit.md)、[completion／bisimulation](c5_completion_weak_bisimulation.md) | 1,246,132 raw states 無碰撞；同頂點 completion 已有紙面證明，一般 bisimulation／finite traces 有假設式 Lean 定理；拓撲與生成器未形式化 |
| [87-state quotient](c5_weak_quotient.md)、[候選 A/B/C](c5_weak_candidates.md) | W 不等於 inclusion Hasse diagram，可達閉包也不等於 inclusion order；三個候選的一般版仍未證 |
| [最小阻礙與三出口](c5_weak_critical_cores.md)、[repair sets／dual flows](c5_weak_flow_repairs.md) | 一般紙面充要條件已建立；非同面控制指出 disk 前提不能省；一般單側與共同出口仍未證 |
| [至多三內點](c5_weak_list_cores.md)、[四內點](c5_four_vertex_cores.md) | disk／T4 小核心的單缺失分類已完成；存在無界大小的單缺失核心，不能改猜全部 minimal core 內點數有界 |
| [odd-join 家族](c5_odd_join_cores.md)、[degree-4 樹](c5_tree_cores.md) | 各自整個無界家族的單缺失分離已有紙面化約＋有限證書；不是一般 minimal quotient 分類 |
| [triangle 接枝](c5_triangle_branches.md)、[root 介面](c5_root_interfaces.md) | 兩尾可同面；兩點 forcer 的完整 root 介面替換已有反例，必須保留適用範圍；後續路徑／分叉工作已處理原窄問題 |
| [triangle 路徑枝](c5_triangle_path_reduction.md)、[第一分叉](c5_triangle_forks.md) | 任意長路徑、任意外掛樹的全 degree-4 單 triangle 分支已處理；T4 下只缺 q |
| [cycle-5／單環](c5_pentagon_branches.md)、[兩 triangle blocks](c5_two_triangle_blocks.md) | 全 degree-4 單環長度至少 5 排除；兩 triangle blocks 只剩直接 bridge 六內點正常形，存活者只缺 q |
| [互斥多環](c5_three_triangle_blocks.md)、[三環共用點](c5_shared_triangle_blocks.md) | 頂點互斥 triangles 任意總數至多二；恰三環全部連接型排除；不能把「互斥」限制去掉 |
| [四環鏈](c5_four_triangle_chain.md)、[四環分叉](c5_four_triangle_star.md)、[bridge pruning](c5_shared_pair_bridge.md) | 恰四環全部連接型排除；其下一題由 triangle-tree 報告處理；一般替換仍是紙面，介面及拓撲控制為 Python 證書 |
| [任意 triangle tree](c5_triangle_tree_palettes.md) | 七種介面歸納、非 D 二色禁集吸收與閉鄰域 minor；全 degree-4 連通 triangles／bridges 類別中，triangles 必互斥且至多二，不需 T4；未 Lean 化 |
| [長 odd-cycle root](c5_odd_cycle_roots.md) | 一般 root 有十一種介面；不可著色時仍為互補 pairs；保留三點縮成 triangle，排除恰一個長環加任意 triangles／bridges，不需 T4；紙面＋既有證書，未 Lean 化 |
| [多長 odd-cycle](c5_multi_odd_cycles.md) | 十一種介面在任意有限環樹封閉；連續 minor 排除 odd-cycles／bridges 類別中的所有長環，剩餘 triangles 互斥且至多二；不需 T4，紙面＋有限證書，未 Lean 化 |
| [K4 block／全 degree-4 合成](c5_k4_blocks.md) | K4 經 boundary 接路給 K5 minor；結合 Gallai-tree 與既有分類，接受 T4 的全 degree-4 disk minimal obstruction 只缺 q；紙面＋證書，未 Lean 化 |
| [唯一 degree-5 完整接點介面](c5_degree5_interfaces.md) | 共同端點關係、禁色覆蓋的 minimality 充要條件、分量刪邊解除及固定來源圖至多四開關；disk／T4 幾何排除仍開放，紙面＋證書，未 Lean 化 |
| [三-spoke 區域化約](c5_degree5_sectors.md) | 單一二接點分量縮到兩個鏡像 pentagon；完整接合代數與非 minimal disk 控制，最終排除仍未解；紙面＋證書，未 Lean 化 |
| [三-spoke 任意樹分量／連通外框](c5_degree5_tree_components.md) | 任意樹的固定-q 化約與五種閉色序列、648 個必要 lifts 排除；t≥1 的 degree-4 分量不含 K4；含 cycle 的分拆 (2) 仍未解，未 Lean 化 |
| [三-spoke 單 triangle 二接點](c5_degree5_triangle_components.md) | 旁支／共同／不同接點三型全部排除；528 模板、89,224 接線非 disk，不限 bridges 長度或分叉；單長環由下一列處理，未 Lean 化 |
| [三-spoke 單長奇環二接點](c5_degree5_odd_cycle_components.md) | 保留接點縮成 triangle，保持全部固定-q z 色及 minimality；任意單 odd-cycle 加 bridges 排除，147 張具名來源 minor 控制；雙環由 R15–R24 補完，一般多環仍開放，未 Lean 化 |
| [三-spoke 共用點雙 triangle](c5_degree5_shared_triangles.md) | 共用 cut vertex 的任意二接點位置／外枝排除；888 模板、295,920 接線非 disk；互斥雙 triangle 後由 R16–R19 補完，未 Lean 化 |

### 2.2 Kempe、計數與固定圖策略

| 文件 | 現況與剩餘界線 |
| --- | --- |
| [C5 循環流與整數 orbit 分解](c5_circulation.md) | 六維／153 支撐／十二循環等價；36 份有限基底覆蓋推出任意非負整數恆等式解皆通過三套分開的 orbit 分解；獨立 singleton 支撐分解唯一，未新增平面來源排除或 Lean theorem |
| [C5 代數—邊位置對座標](c5_edge_pair_coordinates.md) | 十態完整對照、S4／D5 搬運與 20 條蘊涵；1,024 masks 核對與既有 Kempe screen 等價，仍為 153／142／10，未增加排除力；紙面＋Python，未新增 Lean theorem |
| [Kempe screen](c5_kempe_screen.md)、[adjacent-singleton 計數](c5_adjacent_singleton_counts.md) | 必要條件與剩餘候選已保存；一般 adjacent-singleton lemma 未證，與主線的相鄰雙「缺失」候選 A 不同 |
| [count-cone bridge](c5_count_cone_bridge.md)、[B₅ face](c5_b5_face.md)、[Kempe-class 計數](c5_kempe_class_counts.md) | near-triangulation 化約、部分 Lean 代數及 class 級紙面計數已完成；普通 pairing 不給最終矛盾，cone／connectivity 缺口仍在 |
| [connectivity surgery](c5_kempe_connectivity.md)、[AB 立方體](c5_ab_swap_cube.md)、[complementary 立方體](c5_complementary_cube.md)、[高度數 disk](c5_corner_disks.md) | 同圖 connectivity 更新與控制可重播；AB-only 必逃逸、固定 AB\|CD 必失敗等推測已有反例；較早低度數零 survivor 不再是一般候選依據 |
| [edge states](c5_edge_states.md)、[incidence](c5_edge_incidence.md)、[edge switches](c5_edge_switches.md)、[多候選 choices](c5_edge_choices.md) | pairing／incidence 壓縮不足與 coherent witness 操作已核對；多候選欄位不能任意拼成同一個可實現 state |
| [cut interfaces](c5_cut_interfaces.md)、[cut observations](c5_cut_observations.md)、[equal-cut witness](c5_equal_cut_witness.md) | retained components 的一般重建已有 Lean 支援；粗 cut 量與同 cut 長度不足已有實現反例；一步重建不等於多步充分狀態 |
| [behavior 提案](c5_behavior_refinement.md)、[第一輪](c5_behavior_refinement_results.md)、[radius 2](c5_behavior_radius2.md)、[cycle ablation](c5_cycle_ablation.md) | 提案與有限結果分開；兩／三步 iff 為條件式紙面引理，未 Lean 化，也未證閉包充分性 |
| [策略閉包](c5_strategy_safe.md)、[barriers](c5_strategy_barriers.md)、[禁補償](c5_strategy_no_comp.md)、[alternative exit](c5_alternative_exit.md) | survivor-811 固定閉包與必要低谷／回升已保存；不能據此證一般 K=4 策略或要求每步 cycle complexity 不增 |
| [local exit](c5_local_exit.md)、[singleton preparation](c5_singleton_preparation.md)、[guard repair](c5_guard_repair.md)、[repair interface](c5_repair_interface.md) | 條件引理與 B₂ 有限準備已保存；來源 7／17 同候選介面卻 Δχ=−1／+1，共同安全機制仍未證 |

### 2.3 基礎、枚舉、grammar 與其他支線

| 文件 | 現況與剩餘界線 |
| --- | --- |
| [Lean 接合基礎](lean_root_interfaces.md) | 15 個普通 Lean 定理與報告對照；各項形式化範圍見原報告；完整 minor／disk 層仍未形式化 |
| [Lean 實際邊界與 degree-list 基礎](lean_boundary_degree.md) | 原圖延拓 iff 框列 proper 且內圖 list 可染；完整 degree 拆分、拒絕迫 degree=4／框色單射、低度數與重色延拓；13 個普通定理，Gallai／disk 分類仍未形式化 |
| [研究目標](c5_boundary_relations.md) | 主命題未證；全域存在小代表、指定局部規則的完備性必須分開 |
| [phase 1](phase1.md)、[BAD 構造](construction.md)、[gadgets](gadgets.md) | 基礎 exact relation／有限 Lean 證書與 gadget synthesis；一般 planar、separating C5 的 BAD 不構成 disk 反例 |
| [automata](automata.md)、[attachment normal form](attachment_normal_form.md)、[topology completeness](topology_completeness.md) | 固定 triangle grammar 的染色語義、normal form、GeoReject 與 endpoint-order 編譯已形式化；embedding 抽取與 topology soundness 仍在紙面層 |
| [fan pentagon](fan_pentagon.md)、[boundary relation 庫](boundary_relations.md)、[pp relations](pp_relations.md) | 固定 grammar 的 87 states 與完整 relation／pair 查詢已保存；pp 求值器仍屬 Python 層，87 不是一般 cell catalogue 的 132 |
| [state language](state_language.md)、[stepwise sufficiency](stepwise_state_sufficiency.md)、[local closure](local_closure.md)、[C5 interface 想法](c5_interface_idea.md) | 表示法、strip／fan 的有界控制及 separator 引理可用；一般移動前緣、context／future 充分性、C6／C7 轉接仍待證或未啟動 |
| [cell enumerator](c5_cell_enumerator.md) | R1／SYM／prefix／DFS／bitmask／integer viable 的 Lean 鏈與外部信任已明列；k=6、7 獨立重現僅為有界計算證據；原重複 §14 已整理為 §16 |
| [extension effects](extension_effects.md) | 一般圖的新增點／邊完整 relation 變化已觀察；pair projections 漏掉高階限制，geometry=unknown 的 rows 不能當 disk transitions |

各表只概括成果層級；具體 theorem 名稱、公理審計、證書及完整重播命令仍放原報告。

### 2.4 3903 系列與 sector 前置證據

完整推導順序、符號、適用範圍及證書入口見 [3903 系列導讀](c5_sector_3903_guide.md)。
指定 sector 圖類的 3903 已由 [雙拒絕分類](c5_two_rejection_proof_zh.md) 排除；
以下保留各階段的直接報告入口，舊停止點不是目前待辦。

| 階段 | 報告（由左至右為閱讀順序） |
| --- | --- |
| 目標與拓撲起點 | [五目標與十二列位元定義](c5_sector_targets.md) → [非 disk 正控制](c5_sector_positive_control.md) → [831 與平面／disk 等價](c5_sector_structural.md) → [強迫連通](c5_sector_forced_connectivity.md) → [跨列閉包與交換軌道](c5_sector_cross_row.md) |
| 單步介面與共同身份 | [混合色對與碰撞](c5_sector_mixed_transition.md) → [帶框 incidence](c5_sector_marked_incidence.md) → [共同核心](c5_sector_common_core.md) → [框點 4 的跨色身份](c5_sector_joint_identity.md) |
| 指定轉移的分離與下界 | [兩種飽和 star 分離集](c5_sector_saturated_cuts.md) → [框點 1 切斷分支](c5_sector_frame_cut.md) → [五內點分類](c5_sector_five_inner.md) → [任意長路徑與鄰點障礙](c5_sector_neighbor_barrier.md) |
| 非空交集分支 | [葉點例外下界](c5_sector_leaf_exception.md) → [葉點刪除介面](c5_sector_leaf_reduction.md) → [葉點接回 corners](c5_sector_leaf_corners.md) → [corner 入口分離集](c5_sector_corner_gates.md) → [第一種次序偶圈排除](c5_sector_corner_even_cycle.md) → [兩拒絕列緊 lists](c5_sector_rejection_lists.md) → [末端 block 接合](c5_sector_terminal_blocks.md) |
| 空交集、抽象後繼與後續涵蓋 | [空交集身份](c5_sector_empty_branch.md) → [空分支末端排除](c5_sector_empty_terminal.md) → [全部後繼核對](c5_sector_successor_audit.md) → [331 同圖必要條件](c5_sector_331_barriers.md) |
| 分類與形式化界線 | [雙拒絕分類](c5_two_rejection_proof_zh.md) → [Lean 共用工具](lean_two_rejection_tools.md) → [實際接線與緊性](lean_boundary_degree.md) |

來源原稿：[雙拒絕中文原稿 v1](sources/c5_two_rejection_proof_zh_v1.md)，作為匯入來源保存；目前結論以審閱後報告為準。

### 2.5 degree-5／R 系列

[degree-5／R 系列導讀](c5_degree5_guide.md) 統整 R9–R31 的輪次對照、
共同前提、介面／正常形／來源 minor 依賴與重播入口；各原報告仍直接列於 §2.1。
三-spoke／連通二接點分量的零／一／二環與兩個指定三環鏈型已排除；
R31 同末端不同二接點僅完成正常形，任意長來源 minors 仍是保留缺口。
一般 degree-5 與一般三環尚未排除，研究優先序只見 HANDOFF。

### 2.6 全 degree-4／block 化約系列

[全 degree-4／block 系列導讀](c5_degree4_guide.md) 統整小核心、樹、triangle、
任意 block tree、長奇環與 K4 的依賴順序；原報告仍直接列於 §2.1。
接受 T4 的 C5 disk minimal q-obstruction，若所有有效內點完整 degree=4，
則只缺 q；此任意大小合成依賴紙面化約、外部 degree-list 與有限證書，未完整 Lean 化。
兩 triangle 的直接 bridge 型可存活；固定 q 的 minor 不自動保持完整 Σ。
一般 degree≥5 與共同出口仍開放，研究優先序只見 HANDOFF。

## 3. 已被後續成果處理的舊停止點

以下是既有成果的後續入口，不是本次重新證明；表內「下一題」是當時的演進順序。

| 舊問題或容易誤讀的字樣 | 目前讀法／後續入口 |
| --- | --- |
| (2,2) record 87 的「singleton/pair 相容性未證」 | [首橋相容性](c5_single_spoke_first_bridge.md) 以 q 證書同一首橋 palette 綁定兩端實際支援，β=0／2 均給 K5；p₂ 已證，未排除來源，舊 pair 介面不變 |
| (2,2) record 16 的「p₁ 未決」 | [跨列 residual](c5_single_spoke_cross_row.md) 迫使每塊實際接 b1、b2，原 spoke 完成 K5 反證；已證指定列延拓，未排除來源或求完整 Σ |
| (2,2) record 17 的「缺第三外部落點／雙列未決」 | [兩框弧 K5](c5_single_spoke_two_arc.md) 把另一原分量納入 Z，每塊跨同一份兩弧分割即可；兩列均延拓，不需 bridge 長度上界，未排除 record 17 來源或求完整 Σ |
| (2,2) record 15 的「p₂ 未決」 | [frame-arc K5](c5_single_spoke_frame_arc.md) 在 target 拒絕下重建 residual 穩定子，迫使每塊接 b0、b3，配 C0 的 z–b1 路徑證 p₂ 延拓；不是來源排除或完整 relation 分類 |
| (2,2) record 104 的「補弧外部接合未證」 | [外部路徑接合](c5_single_spoke_two_two_external.md) 已由另一原分量的實際路徑完成；當輪再排除 210 筆、54 筆 A/A 保留；後續框弧層另有來源排除與 target 延拓，見新報告 |
| (2,2)／dual surgery 的「record 110 尚未排除」 | [路徑塊支援 K5](c5_single_spoke_two_two_minor.md) 已在原來源圖排除；原必要表及 surgery 證書保留各自當輪語境 |
| triangle path 報告說「外掛樹分叉仍未解」 | [第一分叉報告](c5_triangle_forks.md) 已排除任意深度分叉 |
| 第一分叉報告的「下一題 cycle-5」 | [單環報告](c5_pentagon_branches.md) 已排除長度至少 5 的唯一 cycle |
| 兩環報告的「下一題三環」 | [互斥三環](c5_three_triangle_blocks.md) 與 [共用點三環](c5_shared_triangle_blocks.md) 已補齊恰三環 |
| 三環共用點的「下一題四環鏈」 | [四環鏈](c5_four_triangle_chain.md) 已完成 |
| 四環鏈的「下一題分叉型」 | [四環分叉](c5_four_triangle_star.md) 已完成 |
| 四環分叉的「bridge 混合型未涵蓋」 | [bridge pruning](c5_shared_pair_bridge.md) 已補齊恰四環；任意 cluster 再由下一列的新報告處理 |
| bridge pruning 的「任意共用點 cluster 未解」 | [palette／minor 報告](c5_triangle_tree_palettes.md) 已排除任意大小的非平凡 cluster；下一題是較長 odd-cycle 的共用點介面 |
| triangle-tree 的「下一題一個長 odd-cycle」 | [長環 root 報告](c5_odd_cycle_roots.md) 已完成介面分類及恰一個長環的排除 |
| 長環 root 的「下一題兩個長環」 | [多長環報告](c5_multi_odd_cycles.md) 已完成兩環的連續縮減，並明列任意多長環的歸納與終止論證；K4／bridge 下一題已由下列新報告處理 |
| 多長環的「含 K4 未處理」 | [K4 報告](c5_k4_blocks.md) 已排除 K4 並合成全 degree-4 的單缺失結論；下一題為恰一個 degree-5 內點 |
| K4 報告的「degree-5 完整接點介面尚未啟動」 | [新介面報告](c5_degree5_interfaces.md) 已完成染色與 minimality 公式；下一題縮到三條 z-spokes 及單一二接點 Gallai 分量 |
| 完整接點報告的「三-spoke／二接點 disk 位置未處理」 | [區域化約](c5_degree5_sectors.md) 已縮到兩個鏡像 pentagon；四色列與刪-spoke minimality 的共同實現仍未解 |
| 區域報告的「pentagon 尚無 block／path 排除」 | [樹分量報告](c5_degree5_tree_components.md) 已排除任意樹 C、t≥1 的 K4 block；含 cycle 的二接點介面仍開放 |
| 樹報告的「下一題 C 恰含一個 triangle」 | [單 triangle 報告](c5_degree5_triangle_components.md) 已處理全部接點位置及外枝；下一題為恰一個長 odd-cycle |
| 單 triangle 報告的「下一題恰一個長 odd-cycle」 | [單長奇環報告](c5_degree5_odd_cycle_components.md) 已完成保留接點縮環及三型排除；下一題為恰兩個 triangle blocks |
| 單長奇環報告的「下一題恰兩個 triangles」 | [共用點雙環報告](c5_degree5_shared_triangles.md) 已排除共用 cut vertex 分支；下一題收窄為兩個互斥 triangles 的 bridge 路徑 |
| R16／R17 的「外臂／同點接入未處理」及 R18 的「來源 minor／拓撲覆蓋未完成」 | [R19](c5_degree5_bridge_mark_minors.md) 補齊同點接入；結合 R15–R17，恰兩個 triangle blocks 已排除。下一題是長奇環與 triangle 的耦合 root 介面 |
| R20／R23 的「長環來源 minor 未完成」 | [R21](c5_degree5_long_triangle_minors.md)、[R22](c5_degree5_two_long_cycles.md)、[R24](c5_degree5_shared_cycle_minors.md) 補完混合、互斥雙長環與共用點雙奇環 |
| R24 的「下一題三環完整二接點關係」 | [R25](c5_degree5_three_cycle_roots.md) 已完成末端二臂介面；[R28](c5_degree5_three_cycle_positions.md) 擴至同鏈全部接點位置 |
| R25／R26 的「末端二臂來源 minor 待補」 | [R27](c5_degree5_three_cycle_minors.md) 已補完任意長來源與拓撲合成 |
| R28／R29 的「中間二接點圖層／來源 minor 未解」 | [R29](c5_degree5_middle_pentagon.md) 完成正常形，[R30](c5_degree5_middle_cycle_minors.md) 補完來源 minors |
| R30 的「同末端不同二接點正常形待做」 | [R31](c5_degree5_same_terminal_triangles.md) 已完成正常形；此型任意長來源 minors 仍開放 |
| 較早 handoff 的「completion 未證」 | [同頂點 completion](c5_completion_weak_bisimulation.md) 已有紙面證明；topology 未 Lean 化仍成立 |
| 較早 block 報告說「未新增 Lean theorem」 | 指該輪整個化約；後來共有 list 引理進入 [ForcingLists.lean](../Math/ForcingLists.lean)，不代表 minor／disk 論證也進入 Lean |
| 各輪「尚未提交／推送」 | 只描述研究當時；詳見 [發布歷史](STATUS_HISTORY.md)，即時發布狀態以 Git 為準 |
| enumerator 兩個「§14」 | edge-mask 仍為 §14；獨立 cross-check 改為 §16，對應導引一併更正 |

歷史交接以快照保存，不逐句改寫當時的未知或發布紀錄。

## 4. 可能出現新變化的地方

以下區分已完成結果與保留缺口，不在此另排研究優先序。

| 狀態 | 項目 | 證據與界線 |
| --- | --- | --- |
| 已完成 | 3703 兩葉鏈 | [排除報告](c5_sector_3703_exclusion.md) 完成任意長度三拒絕排除；限定 sector 圖類，未 Lean 化 |
| 已完成 | 五目標到三-spoke 核心出口的接合 | [定理](c5_single_sided_exit.md) 核對來源假設、五目標窮盡及 first strict step；條件式結論無大小限制 |
| 活躍 | 一般單側出口的核心分離 | 唯一 degree-5 的 t=2 已由 [非相鄰分離及既有結果](c5_two_spoke_nonadjacent.md) 完成出口接合；失敗側每個核心必碰全部五點，且有 degree≥6、多個 degree-5，或唯一 degree-5 且 t≤1；一般存在／分離仍未證 |
| 已完成 | 指定 sector 圖類的雙拒絕分類 | [紙面分類](c5_two_rejection_proof_zh.md) 排除四個目標；依賴外部 degree-list，完整分類未 Lean 化 |
| 被後續涵蓋 | 3903 空／非空分支、331 同圖分支 | 既有局部證據保留；後續分類已涵蓋原排除問題，不代表抽象 603 profiles 已改寫 |
| 保留 | R31 任意長來源 minors | 正常形已完成；仍需 boundary 固定 branch sets、四列、degrees、刪邊著色與拓撲合成，見 [R31](c5_degree5_same_terminal_triangles.md) |
| 保留 | 其他三環位置與更多環 | [R28](c5_degree5_three_cycle_positions.md) 是 list 介面；不是一般三環 disk 排除 |
| 保留 | 完整形式化 | [接合工具](lean_root_interfaces.md)、[雙拒絕工具](lean_two_rejection_tools.md) 及 [實際接線／緊性](lean_boundary_degree.md) 已有具名定理；Gallai 與完整紙面分類／minor／disk 論證尚未形式化 |
| 保留 | 一般單側／共同出口與主命題 | 分別需要一般分離、共同 pivotal edge 等證明；兩個單側出口不推出共同出口 |

## 歷史紀錄與舊連結

- [2026-09-28：首橋相容性、record 87 與 18→2 查詢](history/2026-09-28-first-bridge.md)

- [2026-09-28：兩框弧 K5、record 17 雙列與分開套表](history/2026-09-28-two-arc.md)

- [2026-09-28：跨列 residual、record 16 與 66 查詢掃描](history/2026-09-28-cross-row.md)

- [2026-09-28：框弧 K5、record 15 延拓及分開套表](history/2026-09-28-frame-arc.md)

- [2026-09-28：(2,2) 兩輪 K5 排除整合發布](history/2026-09-28-two-two-publication.md)

- [2026-09-28：record 104 與 (2,2) 外部路徑接合](history/2026-09-28-two-two-external.md)

- [2026-09-28：record 110 與 (2,2) 路徑塊支援 K5](history/2026-09-28-two-two-minor.md)

- [2026-09-27：C5 循環流重述與整數 orbit 覆蓋](history/2026-09-27-circulation.md)

- [2026-09-27：同染色 dual 路徑有序重接](history/2026-09-27-dual-path-surgery.md)

- [2026-09-27：single-spoke (2,2) 必要分類](history/2026-09-27-single-spoke-two-two.md)

- [2026-09-27：single-spoke 剩餘單接點上界分類](history/2026-09-27-single-spoke-single-contact-bounds.md)

- [2026-09-27：single-spoke 剩餘二接點上界分類](history/2026-09-27-single-spoke-two-contact-bounds.md)

- [2026-09-27：single-spoke root 守恆全表掃描](history/2026-09-27-single-spoke-root-sweep.md)

- [2026-09-27：single-spoke 六輪成果整合驗證](history/2026-09-27-single-spoke-publication.md)

- [2026-09-27：single-spoke 單接點未用色守恆](history/2026-09-27-single-spoke-root-conservation.md)

- [2026-09-27：single-spoke 旁支 K5 minor 與指定 p₁ 延拓](history/2026-09-27-single-spoke-branch-minor.md)

- [2026-09-27：single-spoke 旁支 palette 守恆](history/2026-09-27-single-spoke-branch-palettes.md)

- [2026-09-27：single-spoke 奇數 bridge 路徑必要化約](history/2026-09-27-single-spoke-bridge-path.md)

- [2026-09-27：single-spoke 外部雙路徑 completion 與 62 筆雙列分離](history/2026-09-27-single-spoke-completion.md)

- [2026-09-27：single-spoke 覆蓋、實際支援與接點次序](history/2026-09-27-single-spoke-cores.md)

- [2026-09-27：非相鄰 two-spoke 分離與 t=2 出口整合](history/2026-09-27-nonadjacent-two-spoke.md)

- [2026-09-24：split-support 完整列分類與兩次序單缺失](history/2026-09-24-split-support.md)

- [2026-09-24：q-preserving 反射、相鄰 support 分離與既有 disk 控制](history/2026-09-24-two-spoke-reflection.md)

- [2026-09-24：中間相鄰兩分量 (2,1) 的三外部集合與 K5 排除](history/2026-09-24-middle-two-one.md)

- [2026-09-24：相鄰兩分量 (2,1) 的同圖 K5 排除](history/2026-09-24-adjacent-two-one.md)

- [2026-09-24：三接點兩-spoke 的同圖 K5 排除](history/2026-09-24-three-contact-exclusion.md)

- [2026-09-24：未接內點引理與非相鄰型分離](history/2026-09-24-unattached-boundary.md)
- [2026-09-24：兩-spoke 區域化約](history/2026-09-24-two-spoke-sectors.md)
- [2026-09-24：單側出口接合與界線](history/2026-09-24-single-sided-exit.md)
- [2026-09-24：3703 排除與驗證](history/2026-09-24-3703-exclusion.md)
- [早期交接快照](HANDOFF_HISTORY.md)
- [2026-09-22 交接快照](HANDOFF_2026-09-22.md)
- [研究與發布歷史，原 STATUS 全文](STATUS_HISTORY.md)

以下保留原章節錨點供舊引用導向歷史；不在此追加研究輪次。

- <a id="r1bridge-pruning-給出任意總環數的-cluster-隔離"></a>[R1：bridge pruning 給出任意總環數的 cluster 隔離](STATUS_HISTORY.md#r1bridge-pruning-給出任意總環數的-cluster-隔離)
- <a id="r2鏈與分叉的-palette-規則統一為樹上遞迴"></a>[R2：鏈與分叉的 palette 規則統一為樹上遞迴](STATUS_HISTORY.md#r2鏈與分叉的-palette-規則統一為樹上遞迴)
- <a id="r3從大-cluster-抽出保留閉鄰域的小-minor"></a>[R3：從大 cluster 抽出保留閉鄰域的小 minor](STATUS_HISTORY.md#r3從大-cluster-抽出保留閉鄰域的小-minor)
- <a id="r4bridge-pruning-的證明已穩定可能值得接入-lean"></a>[R4：bridge pruning 的證明已穩定，可能值得接入 Lean](STATUS_HISTORY.md#r4bridge-pruning-的證明已穩定可能值得接入-lean)
- <a id="r5candidate-a-的共同出口仍需獨立追蹤"></a>[R5：candidate A 的共同出口仍需獨立追蹤](STATUS_HISTORY.md#r5candidate-a-的共同出口仍需獨立追蹤)
- <a id="r6retained-port-與-weak-quotient-的充分性仍是不同問題"></a>[R6：retained-port 與 weak quotient 的充分性仍是不同問題](STATUS_HISTORY.md#r6retained-port-與-weak-quotient-的充分性仍是不同問題)
- <a id="r7較長-odd-cycle-與-triangles-共用點的介面"></a>[R7：較長 odd-cycle 與 triangles 共用點的介面](STATUS_HISTORY.md#r7較長-odd-cycle-與-triangles-共用點的介面)
- <a id="r8兩個長-odd-cycle-blocks-的介面與連續縮減"></a>[R8：兩個長 odd-cycle blocks 的介面與連續縮減](STATUS_HISTORY.md#r8兩個長-odd-cycle-blocks-的介面與連續縮減)
- <a id="r9k4-block-的三色-residual-lists-與-bridge-介面"></a>[R9：K4 block 的三色 residual lists 與 bridge 介面](STATUS_HISTORY.md#r9k4-block-的三色-residual-lists-與-bridge-介面)
- <a id="r10唯一-degree-5-內點與-degree-4-分量的接點介面"></a>[R10：唯一 degree-5 內點與 degree-4 分量的接點介面](STATUS_HISTORY.md#r10唯一-degree-5-內點與-degree-4-分量的接點介面)
- <a id="r11三-spoke二接點分量的-disk-區域"></a>[R11：三-spoke／二接點分量的 disk 區域](STATUS_HISTORY.md#r11三-spoke二接點分量的-disk-區域)
- <a id="r12三-spoke-任意樹與-degree-4-分量的-k4"></a>[R12：三-spoke 任意樹與 degree-4 分量的 K4](STATUS_HISTORY.md#r12三-spoke-任意樹與-degree-4-分量的-k4)
- <a id="r13三-spoke-單-triangle-二接點"></a>[R13：三-spoke 單 triangle 二接點](STATUS_HISTORY.md#r13三-spoke-單-triangle-二接點)
- <a id="r14三-spoke-單長奇環二接點"></a>[R14：三-spoke 單長奇環二接點](STATUS_HISTORY.md#r14三-spoke-單長奇環二接點)
- <a id="r15三-spoke-共用點雙-triangle-二接點"></a>[R15：三-spoke 共用點雙 triangle 二接點](STATUS_HISTORY.md#r15三-spoke-共用點雙-triangle-二接點)
- <a id="5-前輪文件整理與驗證紀錄基準-fb6216e"></a>[5. 前輪文件整理與驗證紀錄（基準 fb6216e）](STATUS_HISTORY.md#5-前輪文件整理與驗證紀錄基準-fb6216e)
- <a id="6-本輪接手研究與驗證紀錄基準-76e6f44"></a>[6. 本輪接手研究與驗證紀錄（基準 76e6f44）](STATUS_HISTORY.md#6-本輪接手研究與驗證紀錄基準-76e6f44)
- <a id="7-長-odd-cycle-研究與驗證紀錄基準-7fdc19e"></a>[7. 長 odd-cycle 研究與驗證紀錄（基準 7fdc19e）](STATUS_HISTORY.md#7-長-odd-cycle-研究與驗證紀錄基準-7fdc19e)
- <a id="8-多長-odd-cycle-研究與驗證紀錄基準-7fdc19e接續未提交成果"></a>[8. 多長 odd-cycle 研究與驗證紀錄（基準 7fdc19e，接續未提交成果）](STATUS_HISTORY.md#8-多長-odd-cycle-研究與驗證紀錄基準-7fdc19e接續未提交成果)
- <a id="9-k4-排除與-degree-4-合成基準-dad5940"></a>[9. K4 排除與 degree-4 合成（基準 dad5940）](STATUS_HISTORY.md#9-k4-排除與-degree-4-合成基準-dad5940)
- <a id="10-唯一-degree-5-接點介面接續未提交-r9"></a>[10. 唯一 degree-5 接點介面（接續未提交 R9）](STATUS_HISTORY.md#10-唯一-degree-5-接點介面接續未提交-r9)
- <a id="11-三-spoke-區域化約基準-be97121"></a>[11. 三-spoke 區域化約（基準 be97121）](STATUS_HISTORY.md#11-三-spoke-區域化約基準-be97121)
- <a id="12-三-spoke-任意樹排除接續未提交區域成果"></a>[12. 三-spoke 任意樹排除（接續未提交區域成果）](STATUS_HISTORY.md#12-三-spoke-任意樹排除接續未提交區域成果)
- <a id="13-三-spoke-單-triangle-二接點排除"></a>[13. 三-spoke 單 triangle 二接點排除](STATUS_HISTORY.md#13-三-spoke-單-triangle-二接點排除)
- <a id="14-三-spoke-單長奇環二接點排除"></a>[14. 三-spoke 單長奇環二接點排除](STATUS_HISTORY.md#14-三-spoke-單長奇環二接點排除)
- <a id="15-三-spoke-共用點雙-triangle-排除"></a>[15. 三-spoke 共用點雙 triangle 排除](STATUS_HISTORY.md#15-三-spoke-共用點雙-triangle-排除)
- <a id="16-r11r15-成果整理與發布前核對"></a>[16. R11–R15 成果整理與發布前核對](STATUS_HISTORY.md#16-r11r15-成果整理與發布前核對)
- <a id="17-r16-互斥雙-triangles-的-bridge-切口與直接私有接點"></a>[17. R16 互斥雙 triangles 的 bridge 切口與直接私有接點](STATUS_HISTORY.md#17-r16-互斥雙-triangles-的-bridge-切口與直接私有接點)
- <a id="18-r17-互斥雙-triangles-不同環點接入的任意外臂"></a>[18. R17 互斥雙 triangles 不同環點接入的任意外臂](STATUS_HISTORY.md#18-r17-互斥雙-triangles-不同環點接入的任意外臂)
- <a id="19-r18-同點接入的標記二色介面與候選正常形"></a>[19. R18 同點接入的標記二色介面與候選正常形](STATUS_HISTORY.md#19-r18-同點接入的標記二色介面與候選正常形)
- <a id="20-r19-標記路徑來源-minors-與同點接入排除"></a>[20. R19 標記路徑來源 minors 與同點接入排除](STATUS_HISTORY.md#20-r19-標記路徑來源-minors-與同點接入排除)
- <a id="21-r20-長奇環加-triangle-的完整條件-root-介面"></a>[21. R20 長奇環加 triangle 的完整條件 root 介面](STATUS_HISTORY.md#21-r20-長奇環加-triangle-的完整條件-root-介面)
- <a id="22-r16r20-提交整理與核對"></a>[22. R16–R20 提交整理與核對](STATUS_HISTORY.md#22-r16r20-提交整理與核對)
- <a id="23-r21-混合互斥雙環的來源-minor-與排除"></a>[23. R21 混合互斥雙環的來源 minor 與排除](STATUS_HISTORY.md#23-r21-混合互斥雙環的來源-minor-與排除)
- <a id="24-r22-兩個互斥長奇環的連續縮減"></a>[24. R22 兩個互斥長奇環的連續縮減](STATUS_HISTORY.md#24-r22-兩個互斥長奇環的連續縮減)
- <a id="25-r23-共用點雙奇環的四列可延拓介面"></a>[25. R23 共用點雙奇環的四列可延拓介面](STATUS_HISTORY.md#25-r23-共用點雙奇環的四列可延拓介面)
- <a id="26-可重用接合語義的-lean-基礎"></a>[26. 可重用接合語義的 Lean 基礎](STATUS_HISTORY.md#26-可重用接合語義的-lean-基礎)
- <a id="27-r21r23-與-lean-接合基礎發布核對"></a>[27. R21–R23 與 Lean 接合基礎發布核對](STATUS_HISTORY.md#27-r21r23-與-lean-接合基礎發布核對)
- <a id="28-r24-共用點雙奇環來源-minor-與排除"></a>[28. R24 共用點雙奇環來源 minor 與排除](STATUS_HISTORY.md#28-r24-共用點雙奇環來源-minor-與排除)
- <a id="29-r25-三環共用點鏈的-fixed-q-介面"></a>[29. R25 三環共用點鏈的 fixed-q 介面](STATUS_HISTORY.md#29-r25-三環共用點鏈的-fixed-q-介面)
- <a id="30-r26-三個-triangle-鏈正常形拓撲"></a>[30. R26 三個 triangle 鏈正常形拓撲](STATUS_HISTORY.md#30-r26-三個-triangle-鏈正常形拓撲)
- <a id="31-r27-三環共用點鏈來源-minors"></a>[31. R27 三環共用點鏈來源 minors](STATUS_HISTORY.md#31-r27-三環共用點鏈來源-minors)
- <a id="32-r28-三環鏈全部接點位置介面"></a>[32. R28 三環鏈全部接點位置介面](STATUS_HISTORY.md#32-r28-三環鏈全部接點位置介面)
- <a id="33-r29-c3c5c3-中間二接點正常形"></a>[33. R29 C3–C5–C3 中間二接點正常形](STATUS_HISTORY.md#33-r29-c3c5c3-中間二接點正常形)
- <a id="34-r30-中間二接點三環鏈來源-minors"></a>[34. R30 中間二接點三環鏈來源 minors](STATUS_HISTORY.md#34-r30-中間二接點三環鏈來源-minors)
- <a id="35-r31-同末端不同二接點正常形"></a>[35. R31 同末端不同二接點正常形](STATUS_HISTORY.md#35-r31-同末端不同二接點正常形)
- <a id="36-文件現況盤點與變化追蹤"></a>[36. 文件現況盤點與變化追蹤](STATUS_HISTORY.md#36-文件現況盤點與變化追蹤)
- <a id="37-r24r31-整合提交與發布核對"></a>[37. R24–R31 整合提交與發布核對](STATUS_HISTORY.md#37-r24r31-整合提交與發布核對)
- <a id="38-相鄰雙缺失的-12-bit-定向實驗"></a>[38. 相鄰雙缺失的 12-bit 定向實驗](STATUS_HISTORY.md#38-相鄰雙缺失的-12-bit-定向實驗)
- <a id="39-3903-的既有非-disk-正控制"></a>[39. 3903 的既有非 disk 正控制](STATUS_HISTORY.md#39-3903-的既有非-disk-正控制)
- <a id="40-831-的平面disk-等價與必要連接"></a>[40. 831 的平面／disk 等價與必要連接](STATUS_HISTORY.md#40-831-的平面disk-等價與必要連接)
- <a id="41-sector-三輪研究整合提交"></a>[41. Sector 三輪研究整合提交](STATUS_HISTORY.md#41-sector-三輪研究整合提交)
- <a id="42-tutte-依賴鏈與較小證書"></a>[42. Tutte 依賴鏈與較小證書](STATUS_HISTORY.md#42-tutte-依賴鏈與較小證書)
- <a id="43-3903-強迫連通抽取"></a>[43. 3903 強迫連通抽取](STATUS_HISTORY.md#43-3903-強迫連通抽取)
- <a id="44-3903-跨列分割閉包與實際交換軌道"></a>[44. 3903 跨列分割閉包與實際交換軌道](STATUS_HISTORY.md#44-3903-跨列分割閉包與實際交換軌道)
- <a id="45-3903-兩輪成果整合提交與發布"></a>[45. 3903 兩輪成果整合提交與發布](STATUS_HISTORY.md#45-3903-兩輪成果整合提交與發布)
- <a id="46-3903-單步混合色對相容性與介面碰撞"></a>[46. 3903 單步混合色對相容性與介面碰撞](STATUS_HISTORY.md#46-3903-單步混合色對相容性與介面碰撞)
- <a id="47-3903-單步混合相容性提交與接手核對"></a>[47. 3903 單步混合相容性提交與接手核對](STATUS_HISTORY.md#47-3903-單步混合相容性提交與接手核對)
- <a id="48-3903-單步帶框-incidence-安全刪減"></a>[48. 3903 單步帶框 incidence 安全刪減](STATUS_HISTORY.md#48-3903-單步帶框-incidence-安全刪減)
- <a id="49-3903-單步共同核心與框投影限制"></a>[49. 3903 單步共同核心與框投影限制](STATUS_HISTORY.md#49-3903-單步共同核心與框投影限制)
- <a id="50-3903-框點-4-跨色身份與共同鄰點障礙"></a>[50. 3903 框點 4 跨色身份與共同鄰點障礙](STATUS_HISTORY.md#50-3903-框點-4-跨色身份與共同鄰點障礙)
- <a id="51-3903-degree-4-stars-兩種分離集與條件式六內點下界"></a>[51. 3903 degree-4 stars 兩種分離集與條件式六內點下界](STATUS_HISTORY.md#51-3903-degree-4-stars-兩種分離集與條件式六內點下界)
- <a id="52-3903-四輪成果整理與提交核對"></a>[52. 3903 四輪成果整理與提交核對](STATUS_HISTORY.md#52-3903-四輪成果整理與提交核對)
- <a id="53-3903-框點切斷分支與五內點必要下界"></a>[53. 3903 框點切斷分支與五內點必要下界](STATUS_HISTORY.md#53-3903-框點切斷分支與五內點必要下界)
- <a id="54-3903-五內點路徑分類與六內點下界"></a>[54. 3903 五內點路徑分類與六內點下界](STATUS_HISTORY.md#54-3903-五內點路徑分類與六內點下界)
- <a id="55-3903-任意長路徑互斥與鄰點障礙"></a>[55. 3903 任意長路徑互斥與鄰點障礙](STATUS_HISTORY.md#55-3903-任意長路徑互斥與鄰點障礙)
- <a id="56-3903-飽和葉點例外的條件式八內點下界"></a>[56. 3903 飽和葉點例外的條件式八內點下界](STATUS_HISTORY.md#56-3903-飽和葉點例外的條件式八內點下界)
- <a id="57-3903-葉點刪除介面與自動分離"></a>[57. 3903 葉點刪除介面與自動分離](STATUS_HISTORY.md#57-3903-葉點刪除介面與自動分離)
- <a id="58-3903-葉點接回的兩種必要-corner-次序"></a>[58. 3903 葉點接回的兩種必要 corner 次序](STATUS_HISTORY.md#58-3903-葉點接回的兩種必要-corner-次序)
- <a id="59-3903-六輪成果整理與提交核對"></a>[59. 3903 六輪成果整理與提交核對](STATUS_HISTORY.md#59-3903-六輪成果整理與提交核對)
- <a id="60-3903-corner-次序的飽和入口分離集"></a>[60. 3903 corner 次序的飽和入口分離集](STATUS_HISTORY.md#60-3903-corner-次序的飽和入口分離集)
- <a id="61-3903-第一種-corner-次序的偶圈排除與單步正控制"></a>[61. 3903 第一種 corner 次序的偶圈排除與單步正控制](STATUS_HISTORY.md#61-3903-第一種-corner-次序的偶圈排除與單步正控制)
- <a id="62-3903-拒絕列緊-list-與內部葉點排除"></a>[62. 3903 拒絕列緊 list 與內部葉點排除](STATUS_HISTORY.md#62-3903-拒絕列緊-list-與內部葉點排除)
- <a id="63-3903-三輪成果整合與發布"></a>[63. 3903 三輪成果整合與發布](STATUS_HISTORY.md#63-3903-三輪成果整合與發布)
- <a id="64-3903-末端-block-介面與非空分支排除"></a>[64. 3903 末端 block 介面與非空分支排除](STATUS_HISTORY.md#64-3903-末端-block-介面與非空分支排除)
- <a id="65-3903-非空分支排除成果發布"></a>[65. 3903 非空分支排除成果發布](STATUS_HISTORY.md#65-3903-非空分支排除成果發布)
- <a id="66-3903-空交集分支的框鄰點與葉點排除"></a>[66. 3903 空交集分支的框鄰點與葉點排除](STATUS_HISTORY.md#66-3903-空交集分支的框鄰點與葉點排除)
- <a id="67-3903-空分支末端-block-排除與指定轉移禁令"></a>[67. 3903 空分支末端 block 排除與指定轉移禁令](STATUS_HISTORY.md#67-3903-空分支末端-block-排除與指定轉移禁令)
- <a id="68-397action-2-全部後繼與單條禁令閉包核對"></a>[68. 397/action 2 全部後繼與單條禁令閉包核對](STATUS_HISTORY.md#68-397action-2-全部後繼與單條禁令閉包核對)
- <a id="69-331-交換外飽和分離集與無葉核心"></a>[69. 331 交換外飽和分離集與無葉核心](STATUS_HISTORY.md#69-331-交換外飽和分離集與無葉核心)
- <a id="70-3903-空分支後繼與-331-四輪成果發布"></a>[70. 3903 空分支後繼與 331 四輪成果發布](STATUS_HISTORY.md#70-3903-空分支後繼與-331-四輪成果發布)
- <a id="71-c5-雙拒絕分類匯入與獨立核對"></a>[71. C5 雙拒絕分類匯入與獨立核對](STATUS_HISTORY.md#71-c5-雙拒絕分類匯入與獨立核對)
- <a id="72-雙拒絕分類的-lean-共用引理與證明依賴表"></a>[72. 雙拒絕分類的 Lean 共用引理與證明依賴表](STATUS_HISTORY.md#72-雙拒絕分類的-lean-共用引理與證明依賴表)
- <a id="73-雙拒絕-lean-工具整合發布"></a>[73. 雙拒絕 Lean 工具整合發布](STATUS_HISTORY.md#73-雙拒絕-lean-工具整合發布)
- <a id="74-3703-三拒絕的兩葉-triangle-鏈化約"></a>[74. 3703 三拒絕的兩葉 triangle 鏈化約](STATUS_HISTORY.md#74-3703-三拒絕的兩葉-triangle-鏈化約)
- <a id="75-3703-鏈化約整合發布"></a>[75. 3703 鏈化約整合發布](STATUS_HISTORY.md#75-3703-鏈化約整合發布)
