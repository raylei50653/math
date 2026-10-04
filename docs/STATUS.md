# 文件狀態與可能變化追蹤

更新：2026-10-04。研究線標記見 [HANDOFF](HANDOFF.md)；項目現況、停止點與重播由各線導覽維護。
本頁保留所有文件的直接索引、短狀態與後續關係；詳細前提及數字以原報告為準。
**一般單側／共同出口與 `K∞=K≤5` 仍未證。**

## 1. 閱讀順序與文件角色

| 需求 | 入口 |
| --- | --- |
| 選擇研究線 | [HANDOFF](HANDOFF.md) 的導覽連結與進行中標記 |
| 接續研究、找項目現況／停止點／重播 | 下列各研究線導覽 |
| 查證結論及證據 | 本頁 §2 專題索引；詳細前提、證書與 theorem 以報告為準 |
| 看全線整合與實驗提案 | [C₅ 全線進展與高階假設](c5_research_synthesis.md)；研究快照，不取代各線停止點 |
| 看後續成果與保留缺口 | 本頁 §3–4 |
| 更新文件 | [文件維護規則](DOCUMENTATION.md) |
| 查當時的研究／發布狀態 | [研究歷史](STATUS_HISTORY.md)；即時提交狀態查 Git |

「已完成」僅限明列前提；紙面、外部定理、Python 有限證書、Lean 普通證明與
`native_decide` 分開標示，不能從有限控制外推一般 disk 或完整 Σ 結論。

### 研究線導覽

| 導覽 | 負責範圍 |
| --- | --- |
| [Weak-deletion／出口](c5_weak_deletion_guide.md) | 候選、minimal obstruction、核心分離與一般出口缺口 |
| [C₅ class／兩點重疊](c5_two_vertex_overlap_guide.md) | 兩個 class 各選兩點識別、完整染色後繼與拓撲界線 |
| [Degree-4／block](c5_degree4_guide.md) | 全 degree-4 合成、前提及證書 |
| [Degree-5／R 系列](c5_degree5_guide.md) | 來源結構、R31 minor 與其他環型缺口 |
| [Sector／雙拒絕分類](c5_sector_3903_guide.md) | 3903、3703 與指定 sector 分類 |
| [Kempe／計數與策略](c5_kempe_guide.md) | 同圖換色、有序重接、計數限制與 repair |
| [State／grammar／topology](c5_state_guide.md) | 充分性、固定 grammar、embedding 及枚舉 |
| [Lean 形式化](lean_guide.md) | 具名定理、形式化依賴與公理審計 |

## 2. 專題文件全索引

### 2.1 目前主線：weak deletion 與 minimal obstruction

以下結論僅在各報告明列的圖類與前提下成立；項目現況與停止點見 [weak-deletion 導覽](c5_weak_deletion_guide.md)。

| 文件 | 現況與剩餘界線 |
| --- | --- |
| [Weak-deletion 開放葉 ledger](c5_open_leaf_ledger.md) | 共鄰 P₃ 固定3500具名keys：C₂／C₃／C₄各閉合一葉，W batch（D₆稽核）閉合其餘3497，版本化cw-v1趨勢3500→3499→3498→3497→0；C₄ ledger逐byte保留為predecessor；全主線葉總數及每日速度未知 |
| [Mixed P₃ 中點／端點六跨度排除](c5_mixed_p3_middle_endpoint.md) | 保留原末端三色附件，原四環外側四區塊排除全部 residual 及整份對稱型；連同兩端接線完成不同接點各一 incidence；任意 unary 大小、0 target，未 Lean 化 |
| [任務 C：Mixed 共鄰 P₃ 雙扇區與部分來源排除](c5_mixed_p3_common_endpoint.md) | 保留原鏈與 (3,2,1) 附件；任意 unary 大小的短子弧／tether 引理，x₁ 強制唯一框色 2 時全排除；36 具名必要 residual、140 rotation 正控制及 900 側接合保留，0 target；現行入口見 weak-deletion 導覽，未 Lean 化 |
| [C₂：共鄰 P₃ 一色支援三接點 unary](c5_mixed_p3_one_color_ternary_unary.md) | CPP-134-1／geometry 30／side_join 20：任意 unary 大小的原 degree／葉數化約迫 triangle，原外路給 K₅ subdivision；保存完整 tuples／刪邊 witnesses，僅關閉這份側接合，0 target，外部 Gallai＋紙面＋Python，未 Lean 化 |
| [C₃：共鄰 P₃ 雙框點三接點 unary](c5_mixed_p3_two_frame_ternary_unary.md) | CPP-134-1／geometry 34／side_join 20：禁色 0 排接點碰 b₂，原 palette 分 T／N 葉；N 葉由原外路 K₅ 排除後重證葉數，任意 unary 大小來源排除。原雙框點 degree 四／bridges／完整 tuples 控制保存，僅關閉這份側接合，0 target，未 Lean 化 |
| [C₄：共鄰 P₃ 雙框點兩份 unary](c5_mixed_p3_two_frame_two_unary.md) | CPP-134-1／geometry 34／side_join 60、side IDs=(27,1)：九份自身支援必要配置、三份 binary 完整 relation 與唯一 unary relation 均違反原 lifts 的 2↔3 封閉性；任意大小來源排除。兩份 ownership／原 bridges、整側相同禁色負控制保存，其他 joins 及 36／140／900 不刪，0 target，未 Lean 化 |
| [Mixed P₃ 非對稱六跨度排除](c5_mixed_p3_asymmetric.md) | (1,2) 及 root 交換型容許一色側零跨度，完整側支援迫至少六框邊；完成兩端各一 incidence 全 residual；中點／端點由後續排除，任意 unary 大小、0 target，未 Lean 化 |
| [Mixed P₃ 對稱兩色分支](c5_mixed_p3_symmetric.md) | 兩端各一 incidence、兩側同 pair 時，原五環空內側與完整側支援排除全部 disk 來源；非對稱由後續完成；任意 unary 大小、不需 T4／Gallai、0 target，未 Lean 化 |
| [Mixed 容量與最小三點介面](c5_mixed_capacity_contacts.md) | 任意大小逐欄容量、unary 無重疊／缺額至多一與十八側型；各一 incidence 至多兩禁對；P₃ 不同接點各一 incidence 全來源排除，共鄰端點由後續作部分排除／36 具名殘留，其餘幾何與 Lean 化保留 |
| [No-mixed 增長完備性與共同分離](c5_no_mixed_growth_completion.md) | 三個側弧位置直接排除影響 R 的增長；結合無增長定理免查支援表地完成指定 p₁、p₂ 分離，未 Lean 化，逐染色 repair 未構造 |
| [No-mixed 無增長共同分離](c5_no_mixed_no_growth.md) | 短側弧與未見兩色交換不變性，免查支援表地證明無增長時必有異色 root pair；7,848 joins 回歸通過；增長缺口由後續共同分離涵蓋，未 Lean 化 |
| [No-mixed 統一局部增長篩選](c5_no_mixed_local_screen.md) | 同一守恆／非守恆規則排除 2,208 個局部 pair，32 份不影響 R；重建原 434 失敗排除。後續無增長及增長位置引理已免表完成共同分離，原較強篩選數字保留 |
| [No-mixed 搬運與介面驗證](c5_no_mixed_hypothesis_audit.md) | 沿用共同 lifts 與側跨度，紙面證成每 root 至多一份不可搬運分量；4,164 查詢／11,096 joins 的完整、A_h、D_p 介面相同，434 舊失敗 joins 互斥分組；守恆不升 pair 及指定雙列共同分離由後續免表證成，逐染色 repair 未構造，未 Lean 化 |
| [No-mixed 十五類與側跨度預算](c5_no_mixed_span_budget.md) | 紙面必要式 m+s+a≤5 統一八類來源排除；七類沿用雙列分離。5,842 支援／4,164 target 的跨表稽核，未證實現或一般機制完備性，未 Lean 化 |
| [D–E 五正跨度與雙飽和原路徑排除](c5_adjacent_degree5_no_mixed_de.md) | 48 必要支援全 source K5、120 空纖維，含交換型；十五類／3,548 原接合全覆蓋，0 target，不需 T4，未 Lean 化 |
| [D–D 四飽和原分量與框邊排除](c5_adjacent_degree5_no_mixed_dd.md) | 352 必要支援全 source K5；80 空纖維，0 target，不需 T4，未 Lean 化 |
| [C–E 五正跨度與原路徑排除](c5_adjacent_degree5_no_mixed_ce.md) | 96 必要支援全 source K5，108 原 IDs 無相容支援，含交換型；0 target，不需 T4，未 Lean 化 |
| [C–D 三飽和原分量排除](c5_adjacent_degree5_no_mixed_cd.md) | 640 必要支援全 source K5，含 root 交換型；0 target，不需 T4，未 Lean 化 |
| [C–C 無 spoke 四分量排除](c5_adjacent_degree5_no_mixed_cc.md) | 1,176 必要支援全 source K5；保留原分量外部路徑，0 target；不需 T4，未 Lean 化 |
| [B–D 雙飽和來源排除](c5_adjacent_degree5_no_mixed_bd.md) | 312 必要支援全 source K5；八份須原分量外部路徑，0 target，含交換型；不需 T4，未 Lean 化 |
| [B–C 飽和原路徑與雙列分離](c5_adjacent_degree5_no_mixed_bc.md) | 608 份必要支援中 584 source K5；保留 24 份／48 target 全證，含 root 交換型，不需 T4，未 Lean 化 |
| [E–E 六份正跨度來源排除](c5_adjacent_degree5_no_mixed_ee.md) | 144 份原接合全無 disk 支援；六正跨度超出五框邊，0 target 查詢，不需 T4，未 Lean 化 |
| [B–E 五分量正跨度及完整關係搬運](c5_adjacent_degree5_no_mixed_be.md) | 180 份原接合成 144 份必要支援；288 target 全證，含 root 交換型；無新增 minor 排除，不需 T4，未 Lean 化 |
| [B–B 四分量支援／環序及分離](c5_adjacent_degree5_no_mixed_bb.md) | 236 份原接合成 888 份必要支援；1,776 個 target 全證，120 失敗候選由原路徑／雙端點排除；無新增支援刪除，不需 T4，未 Lean 化 |
| [Root degree 超額預算](c5_root_degree_excess.md) | No-mixed source 的 D+O+κ=degree−4 與樹骨架 κ=0 已證；不是 target 等式，一般交換／幾何機制未證；紙面＋Python，未 Lean 化 |
| [交換或幾何阻斷的範圍遍歷](c5_exchange_geometry_scope.md) | 原 25 格／15 種交換型分類保留；後續含 t=2 側及 B–B／B–C／B–D／B–E／C–C／C–D／C–E／D–D／D–E／E–E 共十五類全覆蓋；抽象控制不證一般機制完備性 |
| [無 mixed t_w=0,(2,2) 重疊型](c5_adjacent_degree5_no_mixed_t2_t0_overlap.md) | D_w=0、O_w=1 重疊型全作 source K5 排除，0 target 查詢；完成含 t=2 側的全部分拆，不需 T4，未 Lean 化 |
| [無 mixed t_w=0,(2,2) 缺額型](c5_adjacent_degree5_no_mixed_t2_t0_pairs.md) | 缺額型以來源排除及保留支援雙列分離接回第九類；重疊型由後續報告全排除，不需 T4，未 Lean 化 |
| [無 mixed t_z=2、t_w=0、(2,1,1)](c5_adjacent_degree5_no_mixed_t2_t0_singles.md) | 四原分量／六接點的支援覆蓋完成，全部查詢接受並接回出口第九類；不需 T4，未 Lean 化 |
| [無 mixed t_z=2、t_w=1 原雙端點](c5_adjacent_degree5_no_mixed_t2_t1_endpoints.md) | 原完整 bridge 端點 tightness 與固定框弧 K5 關閉最後查詢，整型及 root 交換型接回出口；無新增來源排除，不需 T4，未 Lean 化 |
| [無 mixed t_z=2、t_w=1 原外部路徑與首橋](c5_adjacent_degree5_no_mixed_t2_t1_bridge.md) | 原路徑／首橋層的舊未決由後續原雙端點層全部涵蓋；原支援與 artifacts 保留 |
| [無 mixed t_z=2,(2)、t_w=1,(2,1)](c5_adjacent_degree5_no_mixed_t2_t1.md) | 必要支援／環序與完整 schemas 已建立；舊 target 上界由後續原雙端點層完成整型分離，原資料保留，未 Lean 化 |
| [無 mixed 兩側 t=2 整條原路徑 palettes](c5_adjacent_degree5_no_mixed_t2_path_palettes.md) | 整條原路徑 palette 交換關閉最後查詢，原必要支援全雙列並接回出口第九類；無新增來源排除，不需 T4，未 Lean 化 |
| [無 mixed 兩側 t=2 原雙端點](c5_adjacent_degree5_no_mixed_t2_endpoints.md) | 不守恆 q 禁色仍可用原完整 bridge 端點 tightness；舊停止點由後續整條路徑層涵蓋，原證書保留 |
| [無 mixed 兩側 t=2 原 bridge 與框弧](c5_adjacent_degree5_no_mixed_t2_bridge.md) | 原 bridge／固定框弧新增延拓；舊未決由後續雙端點及整條路徑層涵蓋，原證書保留 |
| [無 mixed 兩側 t=2,(2) 支援與環序](c5_adjacent_degree5_no_mixed_t2.md) | 同序支援、完整 q schemas 與具名 rotations 已建立；整型雙列由後續路徑 palettes 完成，未證 disk 實現或 Lean 化 |
| [相鄰雙 root 無 mixed](c5_adjacent_degree5_no_mixed.md) | 同色 residual、minimality 與容量缺額／重疊化約完成；含 t=2 側分拆及 B–B／B–C／B–D／B–E／C–C／C–D／C–E／D–D／D–E／E–E 全由後續涵蓋，未證 disk 實現或 Lean 化 |
| [唯一 mixed K2 四 incidence 型](c5_adjacent_degree5_mixed_edge_k4.md) | 四 incidence 原 K4 與實際外部路徑排除一般平面來源，完成唯一 mixed K2 全接線；不需 T4／degree-list，0 target 查詢，未 Lean 化 |
| [唯一 mixed K2 同端點型](c5_adjacent_degree5_mixed_edge_same_endpoint.md) | 同端點型由原 K5、跨度與 v-star 排除全部 disk 來源；保留 v 扇區，不需 T4，0 target 查詢，未 Lean 化 |
| [共鄰端點 K2 的 w 側兩條 spoke](c5_adjacent_degree5_mixed_edge_shared_t2.md) | 共鄰端點型 t_w=2,(1) 的必要支援與指定雙列分離完成，接回出口；不需 T4，未證實現或 Lean 化 |
| [共鄰端點 K2 的 t_w=1、(2)](c5_adjacent_degree5_mixed_edge_shared_t1_pair.md) | 原 diamond／spoke 路徑排除與局部搬運完成 t_w=1,(2) 雙列分離；保留原 ID／完整關係，不需 T4，未證實現或 Lean 化 |
| [共鄰端點 K2 的 t_w=1、(1,1)](c5_adjacent_degree5_mixed_edge_shared_t1_singles.md) | 三份 unary 跨度與飽和環序完成 t_w=1,(1,1) 雙列分離；不需 T4 或新 K5，未證實現或 Lean 化 |
| [共鄰端點 K2 的 t_w=0、(2,1)](c5_adjacent_degree5_mixed_edge_shared_t0_pair_single.md) | 完整 relation 搬運完成 t_w=0,(2,1) 雙列；另有原 diamond 路徑來源排除，不需 T4，未證實現或 Lean 化 |
| [共鄰端點 K2 的 t_w=0、(1,1,1)](c5_adjacent_degree5_mixed_edge_shared_t0_singles.md) | 六跨度矛盾排除 t_w=0,(1,1,1) 全部 disk 來源，完成共鄰端點型五分拆；0 target 查詢，不需 T4，未 Lean 化 |
| [唯一 mixed K2 共鄰端點型](c5_adjacent_degree5_mixed_edge_shared.md) | 完整 tuples 與逐邊 minimality 已建立；全部五分拆由後續雙列分離或來源排除完成，原必要資料保留，未 Lean 化 |
| [相鄰雙 degree-5 唯一 mixed 原 K2](c5_adjacent_degree5_mixed_edge.md) | 各一接點的完整關係／逐邊 minimality 已建立；disk 來源由原四環次序報告全排除，原資料保留，未 Lean 化 |
| [唯一 mixed K2 原四環次序排除](c5_adjacent_degree5_mixed_edge_order.md) | 各一接點型由支援跨度與原四環飽和次序排除全部 disk 來源；不需 T4，其他接線由後續涵蓋，一般出口未證 |
| [相鄰雙 degree-5 共鄰單點 34／40 排除](c5_adjacent_degree5_singleton_end_arc.md) | 34／40 支援以 K5／T4 全來源排除，唯一 mixed singleton 全部支援接回出口；紙面＋Python，未 Lean 化 |
| [相鄰雙 degree-5 共鄰單點 12 長弧](c5_adjacent_degree5_singleton_middle_arc.md) | 12 長弧經原 K5／T4 排除後全部保留支援雙列接受；34／40 由後續涵蓋，未證實現或 Lean 化 |
| [相鄰雙 degree-5 共鄰單點 01／23 長弧](c5_adjacent_degree5_singleton_long_arc.md) | 01／23 長弧的必要支援與指定雙列分離完成；12／34／40 由後續涵蓋，未 Lean 化 |
| [相鄰雙 degree-5 共鄰單點同側限制](c5_adjacent_degree5_singleton_sectors.md) | Disk＋T4 下非相鄰 x 支援來源排除／單缺失分離完成；相鄰長弧由後續涵蓋，未證實現或 Lean 化 |
| [相鄰雙 degree-5 唯一共鄰單點](c5_adjacent_degree5_shared_singleton.md) | 單 root 消去與 mixed 容量化約完成，只剩 (2)／(2,1)；全部 x 支援由後續接回出口，必要表實現性與 Lean 化保留 |
| [相鄰雙 degree-5 完整有序色對介面](c5_adjacent_degree5_interfaces.md) | 有序色對完整接合、逐邊 minimality 與固定來源多步刪邊式完成；一般雙 root 分離／平面實現性未證，未 Lean 化 |
| [No-spoke (2,2,1) 首橋與固定框弧](c5_no_spoke_first_bridge.md) | 首橋與固定框弧關閉最後查詢，唯一 degree-5 全部核心接回條件式出口；無新增來源排除，未 Lean 化 |
| [No-spoke (2,2,1) 原外部路徑 K5](c5_no_spoke_path_minor.md) | 原外部路徑 K5 排除來源並新增延拓；剩餘查詢由首橋／框弧完成，未證實現性或 Lean 化 |
| [No-spoke 環狀支援與 (2,1,1,1) 分離](c5_no_spoke_supports.md) | 兩種獨立環狀支援枚舉、原分量外部雙路徑；48 筆全部指定雙列延拓，(2,2,1) 原 616 筆／268 筆雙列已證，後由原外部路徑 K5 與首橋／框弧更新為 116 筆全雙列；原 artifact 保留當輪數字，未證可實現或 Lean 化 |
| [No-spoke 外部連通與四型排除](c5_no_spoke_exterior.md) | t=0 多分量的實際外部路徑恢復 K4／triangle hub；(5) 另由四列偶數接點排除，六型只剩 (2,2,1)、(2,1,1,1)；72 份必要覆蓋、560 份 minor 及反射控制，任意大小、不需 T4，未 Lean 化 |
| [Single-spoke (4) 三拒絕共同結構](c5_single_spoke_four.md) | 共同 τ 迫使兩 triangle 加單 bridge，原 tethers 與擴大的 Z 給 K5；任意大小、不需 T4，960 minor 控制；t=1 全部接回出口，未 Lean 化 |
| [Single-spoke (3,1) 三接點排除](c5_single_spoke_three_one.md) | 任意大小 active triangle／三臂、原 boundary tethers 與唯一 spoke 給 K5；不需 T4，保留另一分量及有序接點；800 minor 控制，未 Lean 化，後續 (4) 亦已排除 |
| [Single-spoke (2,2) 局部 residual 與完成表](c5_single_spoke_residual_locality.md) | 同圖局部 residual 關閉最後查詢，(2,2) 全部保留型雙列接回出口；未證實現性／完整 Σ，未 Lean 化 |
| [Single-spoke (2,2) singleton-source 首橋相容性](c5_single_spoke_first_bridge.md) | record 87 的 p₂ 已證；首橋共用 β 與端點固定色共證 16 個 target；該輪來源排除仍 278、102 筆中 100 筆 A/A；剩 90／282 已由局部 residual 完成；紙面＋外部定理＋Python，未 Lean 化 |
| [Single-spoke (2,2) 兩框弧 K5](c5_single_spoke_two_arc.md) | 同一份兩弧分割與另一原分量納入 Z；record 17 雙列已證，新排除 6 筆來源、另證 20 個 target；當輪 102 筆、84 筆 A/A、18 查詢，後由首橋／局部 residual 更新為 102 筆 A/A、0 查詢；未 Lean 化 |
| [Single-spoke (2,2) 跨列 residual](c5_single_spoke_cross_row.md) | 同圖共用原 bridge 路徑的雙列 residual 換色相容性；record 16 的 p₁ 已證，新增 16 個 target；當輪 108 筆／54 型、74 筆 A/A、50 查詢，後由兩框弧／首橋／局部 residual 更新為 102 筆 A/A、0 查詢；未 Lean 化 |
| [Single-spoke (2,2) frame-arc K5](c5_single_spoke_frame_arc.md) | 三段具名框弧及任意兩路徑塊 minor；record 15 的 p₂ 已證，另排除 36 筆來源、另證 18 個 target；當輪剩 108 筆／54 型、58 筆 A/A、66 查詢，後由跨列／兩框弧／首橋／局部 residual 更新至 102 筆 A/A、0 查詢；任意大小紙面＋外部定理，未 Lean 化 |
| [Single-spoke (2,2) 外部路徑接合](c5_single_spoke_two_two_external.md) | record 104 的原分量路徑接至補弧，逐塊相鄰支援對 K5 再排除 210 筆；當輪剩 144 筆／72 型，後由框弧層降至 108；186 支援式、496 minor 控制，任意大小紙面證明，未 Lean 化 |
| [Single-spoke (2,2) 路徑塊支援 K5](c5_single_spoke_two_two_minor.md) | 雙禁色 residual 的逐塊穩定子與實際 b3、b4 接線，來源 K5 排除 record 110、119 及 26 筆；當輪剩 354 筆，後由外部路徑接合降至 144；48 局部式、192 支援式、256 minor 控制，未 Lean 化 |
| [同染色 dual 路徑有序重接](c5_dual_path_surgery.md) | 任意大小一步精確公式；同圖三配對同 state／不同後繼反例；record 110 的 α 配對及共同必要等式，來源已由後續 K5 排除；56 個既有圖、8,420 個混合更新重播，有限可迭代 state 未證 |
| [Single-spoke (2,2) 必要分類](c5_single_spoke_two_two.md) | 完整二元 relation schemas、actual supports、全部接點方向及奇數 bridge 化約；1,530 必要候選、原 T4 保留 380 筆／190 型，框弧／兩框弧 K5 及跨列／首橋／局部 residual 後剩 102 筆／51 型全 A/A；指定雙列分離完成，可實現性／完整 Σ 未證 |
| [Single-spoke 剩餘單接點上界分類](c5_single_spoke_single_contact_bounds.md) | 16 筆皆有 F_C(p)⊆{3}；12 個 p₁ 取 z=2、4 個 p₂ 取 z=0；114 筆雙列全證，root 接線局部分類及任意大小守恆，未 Lean 化 |
| [Single-spoke 剩餘二接點上界分類](c5_single_spoke_two_contact_bounds.md) | 18 查詢分為 9 組／6 幾何 orbits；容量 4、外部路徑 K5 6、未用色對 bridge 障礙 8 全部關閉；該輪 98 筆雙列已證，剩餘 16 筆由單接點分類關閉，未 Lean 化 |
| [Single-spoke root 守恆全表掃描](c5_single_spoke_root_sweep.md) | 通用單接點條件套用全部 228 查詢，新增 14 個接受；該輪 80 筆兩列已證、34 查詢未決，後由二接點及單接點分類完成 114／0；紙面引理＋有限上界計算，未 Lean 化 |
| [Single-spoke 單接點未用色守恆](c5_single_spoke_root_conservation.md) | 指定 (012,04,234) 二接點分支已證 p₂ 延拓，取 z=3；任意大小 root palette 歸納，該輪 66 筆兩列已證，後由全表掃描增至 80 筆、34 查詢未決，未 Lean 化 |
| [Single-spoke 旁支 K5 minor](c5_single_spoke_branch_minor.md) | 指定 (01,04,1234) 二接點分支已證 p₁ 延拓；任意大小同圖 K5 抽取、20 局部型與 360 份拓撲控制；該輪 64 筆兩列已證，後由單接點守恆增至 66 筆、48 查詢未決，未 Lean 化 |
| [Single-spoke 旁支 palette 守恆](c5_single_spoke_branch_palettes.md) | 色 0、3 守恆給 q 路徑交替限制，以及五種旁支入口 palette 配對與必要實際接線；任意大小必要限制；後由旁支 K5 minor 證指定分支 p₁ 延拓，未 Lean 化 |
| [Single-spoke 雙禁色 bridge 路徑](c5_single_spoke_bridge_path.md) | 指定未決分支的兩接點間必為奇數 bridge 路徑，b3 接線全在旁支；任意大小必要化約；後接旁支 K5 minor 完成指定 p₁，未 Lean 化 |
| [Single-spoke 外部雙路徑 completion](c5_single_spoke_completion.md) | 任意大小來源 minor 接回既有 degree-4 分類；該輪新增 30 個接受查詢，62 筆兩列已證，後由旁支 K5 minor 與單接點守恆增至 66 筆；紙面證明與繼承 3,492 項完整關係重播，未 Lean 化 |
| [Single-spoke 覆蓋與嵌入必要化約](c5_single_spoke_cores.md) | 四型覆蓋與反射；(2,1,1) 的 19 必要支援型及完整接點角色保留；後續已完成 114 筆雙列、(2,2) 分離及 (3,1)／(4) 排除，t=1 全部接回出口，非可實現性分類 |
| [非相鄰 two-spoke 出口分離](c5_two_spoke_nonadjacent.md) | 四代表接受兩個指定 p，另四項僅反射；74 個保留 z 的正常形增邊候選與 3,492 個 completion 接線；紙面任意大小化約、Python 完整接點證書、Lean 列代數及搬運 |
| [split-support 相鄰 (2,1) 完整列分類](c5_two_spoke_split_support.md) | 兩接點次序皆單缺失；64 個 A disk forms、252 個 D 例外接線；保留完整 tuples，反射側只搬運，紙面任意大小化約＋Lean 有限列代數 |
| [q-preserving 反射與下一相鄰 orbit](c5_two_spoke_reflection.md) | Lean ordered-relation／禁色搬運；S={b2,b3} 兩項由既有排除搬運；下一 orbit 的 split-support 紙面定理與八個 disk 控制；單缺失已由後續完整列分類完成 |
| [中間相鄰兩分量 (2,1) 排除](c5_two_spoke_middle_21.md) | S={b1,b2} 兩次序皆排除；三外部 branch sets 加 palette {3} bridge／leaf odd cycle 給同圖 K5，保留兩分量關係，未 Lean 化 |
| [相鄰兩分量 (2,1) 排除](c5_two_spoke_adjacent_21.md) | S={b0,b1} 的兩種禁色次序皆不可能；兩個不同分量提供 odd cycle 與 z–b4 路徑，實際雙色 tethers 給 K5 minor；未 Lean 化 |
| [三接點兩-spoke 排除](c5_two_spoke_three_contacts.md) | 同圖 palette 差強迫 triangle／三臂及實際 boundary tethers，K5 minor 排除全部 (3)；任意長度紙面證明＋局部證書，未 Lean 化 |
| [未接內點 boundary 引理](c5_unattached_boundary.md) | 完成兩-spoke 非相鄰 (3) 單缺失分離；一般失敗側每個核心必碰全部五個 boundary 頂點，內點 degree 不限 |
| [兩-spoke 區域化約](c5_degree5_two_spoke_sectors.md) | t=2 的 (3)／(2,1) 任意大小必要位置分類；56 個排除、24 個保留；全部 (3) 由後續 K5 minor 排除，其後 S={b0,b1}、S={b1,b2} 的四個 (2,1) 表項亦已排除 |
| [單側出口接合](c5_single_sided_exit.md) | 全 degree-4、唯一 degree-5、未接內點 boundary，以及相鄰雙 root 的唯一 mixed singleton／K2、無 mixed 至少一側 t=2 的全部分拆及 B–B 核心皆給單側出口；失敗側必有 degree≥6 或至少兩個 degree-5 且避開已處理子類，一般版未證 |
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
| [唯一 degree-5 完整接點介面](c5_degree5_interfaces.md) | 共同端點關係、禁色覆蓋的 minimality 充要條件、分量刪邊解除及固定來源圖至多四開關；唯一 degree-5 的指定雙列分離後由單側出口主線完成；完整圖分類／可實現性仍開放，紙面＋證書，未 Lean 化 |
| [三-spoke 區域化約](c5_degree5_sectors.md) | 單一二接點分量縮到兩個鏡像 pentagon；完整接合代數與非 minimal disk 控制，最終排除仍未解；紙面＋證書，未 Lean 化 |
| [三-spoke 任意樹分量／連通外框](c5_degree5_tree_components.md) | 任意樹的固定-q 化約與五種閉色序列、648 個必要 lifts 排除；t≥1 的 degree-4 分量不含 K4，後續 no-spoke 結果補上 t=0；原 cycle 缺口已有 t≥1 出口接合，完整圖分類／形式化仍有界線 |
| [三-spoke 單 triangle 二接點](c5_degree5_triangle_components.md) | 旁支／共同／不同接點三型全部排除；528 模板、89,224 接線非 disk，不限 bridges 長度或分叉；單長環由下一列處理，未 Lean 化 |
| [三-spoke 單長奇環二接點](c5_degree5_odd_cycle_components.md) | 保留接點縮成 triangle，保持全部固定-q z 色及 minimality；任意單 odd-cycle 加 bridges 排除，147 張具名來源 minor 控制；雙環由 R15–R24 補完，一般多環仍開放，未 Lean 化 |
| [三-spoke 共用點雙 triangle](c5_degree5_shared_triangles.md) | 共用 cut vertex 的任意二接點位置／外枝排除；888 模板、295,920 接線非 disk；互斥雙 triangle 後由 R16–R19 補完，未 Lean 化 |

### 2.2 Kempe、計數與固定圖策略

| 文件 | 現況與剩餘界線 |
| --- | --- |
| [任務 A：ε=2 四-spoke mixed-(1,2)+a-unary](c5_excess_two_mixed_core_four_spoke_mixed12.md) | 原01／23及root交換來源排除；a-spoke省略為原C+a+U單一ternary、整份G−U亦Ω，完整joint迫U三列singleton3／2／3違反未用色守恆。當輪22／26必要殘留由A₂再排01／12；原artifact、72完整degree控制與witnesses保留，未排整型、ε≥3未證，紙面＋Python、未Lean化 |
| [A₂：mixed-(1,2) 原01／12共同長／短face](c5_excess_two_mixed_core_four_spoke_mixed12_01_12.md) | 原actual U接2的crosscut封長C至{2}，短C至{1}；01202完整R_U={2}，固定(a,b,u)=(3,0,2)的三hub引理给完整原joint，來源及root交換全排。其餘20／24框架、52／86支援、68／124relations保存；36完整degree控制、2,880joins／46,080fibres。未排mixed12整型、未證ε≥3，紙面＋Python、未Lean化 |
| [A₃：mixed-(1,2) 共用01／01原三hub](c5_excess_two_mixed_core_four_spoke_mixed12_01_01.md) | 每份四disk rotations與完整ternary保持；C原face支援為{0}或{1}，原互異色三hub延拓使ax非critical，01202的U singleton2／3亦給完整joint矛盾。含root交換全排；其餘18／22框架、44／70支援、56／102relations保存。36完整degree控制、360投影等式與5,712整份C替換witnesses；mixed12整型與ε≥3未證，紙面＋Python、未Lean化 |
| [A₄：mixed-(1,2) 共用04／04具名入口](c5_excess_two_mixed_core_four_spoke_mixed12_04_04.md) | 原四rotations迫C支援{0}／{4}、U實際含123；逐項核對原互異色三hub、exact degree-list與連通外部路徑，完整C替換使ax非critical。01202的U singleton1／3均接完整joint，含root交換全排；其餘16／20框架、40／58支援、50／84schedules保存。24完整degree控制、240投影等式與2,912整份C替換witnesses；未用D₅來源搬運，mixed12整型／ε≥3未證，紙面＋Python、未Lean化 |
| [任務 B：ε=2 四-spoke mixed-(2,2) 無 unary](c5_excess_two_mixed_core_four_spoke_mixed22.md) | 七具名身份、原 R_C 四接點與完整 root-pair fibres；四原 spoke 省略各自 Ω，原拒絕 q-core 必是 G (5,5)。47／75 骨架各縮至25相鄰pairs，equal各排5，20／20必要face與tightness見證保留。28完整degree控制、1,680 joins／26,880 fibres、14條件式原K₅；與A分開，未排整型、未證來源實現或ε≥3，紙面＋Python、未Lean化 |
| [B₂：mixed-(2,2) 原01／23短 face](c5_excess_two_mixed_core_four_spoke_mixed22_short_face.md) | W933-101／W941-139短face{1,2}的七contact身份全來源排除，零殘留；任意大小Gallai leaf的四owner用實際外部路徑提取原K₅。完整四接點／root-pair fibre保持；同骨架長face由B₃獨立涵蓋，整型、ε≥3保留，紙面＋Python、未Lean化 |
| [B₃：mixed-(2,2) 同骨架原長 face](c5_excess_two_mixed_core_four_spoke_mixed22_long_face.md) | W933-101／W941-139長face{0,4,3}七身份獨立全排，零殘留；shared leaf bridge由跨拒絕列slack排除，五種leaf以原外路提取K₅，內部shared bridges與完整四接點fibre保持。只合用B₂／B₃封閉兩W全部faces；其他骨架、整型及ε≥3保留，紙面＋Python、未Lean化 |
| [B₄：933 原04／12的shared附件{4}](c5_excess_two_mixed_core_four_spoke_mixed22_shared4.md) | W933-129長face{2,3,4}；原shared leaf全部11pairs tight，bridge鄰点13附件排5留8。原cut parity迫C−v有奇數框附件，五原bags給K₅，六shared身份／八指定選擇此支全排。完整relation／fibres保持；40degree圖、2,400joins／38,400fibres，其他附件與整份骨架保留，未證ε≥3、未Lean化 |
| [ε=2 四-spoke (2,2) 不相交 pairs 與 mixed-(1,1) 子型完成](c5_excess_two_mixed_core_four_spoke_disjoint_pairs.md) | 最後14／18份由一側全短faces4／8及共同兩段長框弧10／10全排，原unary接線非critical；完成相鄰唯一mixed、四spoke(2,2)、mixed11+各側一unary的47／75原必要身份。2,048rotations／1,280支援對／60apex subdivisions；完整原relations保留，只替換固定短unary的整份witness，C與另一unary外部頂點逐點保持，五角色投影相等；其他incidence及ε≥3保留，任意大小紙面＋Python，未Lean化 |
| [ε=2 四-spoke (2,2) 共用短框弧原拒絕列延拓](c5_excess_two_mixed_core_four_spoke_short_arc.md) | 原941 02／03及六份共用點殘留全排；C短支援Fempty與未見色交換給原01021完整joint，含整圖Σ949搬運身份。963C schemas／101,115六角色tuple witnesses，1,320整圖joins／21,120fibres；當輪14／18不相交殘留由後續全排。指定列出口，不宣稱C全rootpair延拓；紙面＋Python，ε≥3未證 |
| [ε=2 四-spoke (2,2) 原 unary crosscut 與 mixed hubs](c5_excess_two_mixed_core_four_spoke_crosscut.md) | 原 941 01／03、933 01／13 與 root 交換：critical unary 的原 crosscut 封 C 支援至一框點，同色 tightness 保 degree 的二／三 hub K₅ 使原 ax 非 critical。同機制排8／16，當輪14／24後由短框弧及不相交pairs全排；48 apex subdivisions、720 joints／11,520 fibres、7,752 C 替換 witnesses。任意大小紙面＋Python，ε≥3未證，未Lean化 |
| [ε=2 四-spoke (2,2) 同一長 face 的原 unary 次序](c5_excess_two_mixed_core_four_spoke_long_face.md) | 原 01／04 與 root 交換的兩 unary 若 critical 必在共同三段 face；原實際支援次序與短支援引理迫4≤3，固定原接線非 critical。同機制排10／10，當輪22／40後由crosscut收窄至14／24；子型由[不相交 pairs 完成報告](c5_excess_two_mixed_core_four_spoke_disjoint_pairs.md)封閉，其他 incidence 保留。5,120支援對、120 apex K₃,₃ subdivisions、1,620 joints／25,920 fibres。任意大小紙面＋Python，ε≥3未證，未Lean化 |
| [ε=2 四-spoke (2,2) 原 unary 短 face](c5_excess_two_mixed_core_four_spoke_short_face.md) | 原 01／02 與 root 交換的 unary 全 incident faces 都短，原外部路徑與既有短支援迫 au 非 critical；同機制排 8／16 份，後續長 face 再排10／10，unequal剩22／40；子型由[不相交 pairs 完成報告](c5_excess_two_mixed_core_four_spoke_disjoint_pairs.md)封閉，其他 incidence 保留。74 原骨架／7,104 rotations，完整六角色 joints、空纖維及原 U witness 替換；任意大小紙面＋Python，ε≥3 未證，未 Lean 化 |
| [ε=2 四-spoke (2,2) 共用原 pair 的 sealed mixed](c5_excess_two_mixed_core_four_spoke_equal_pair.md) | mixed-(1,1) 加各側一原 unary，共用 spokes 的 diamond 封 C 在一個原三角；既有三-hub 延拓接 G−C 全收，排除 7／9 份，含 01／01 及 root 交換。原40／66 unequal殘留經短／長face、crosscut、短框弧及[不相交pairs](c5_excess_two_mixed_core_four_spoke_disjoint_pairs.md)全部封閉；同一mixed11+各側unary子型完成，原證書保留。36 完整 degree 圖、2,520 joints／40,320 fibres；紙面＋Python，ε≥3 未證，未 Lean 化 |
| [ε=2 四-spoke (3,1) 原 mixed-(1,3) 四接點 leaf-slack](c5_excess_two_mixed_core_four_spoke_quaternary.md) | 原 K=C+a 的四 contacts 要求三禁色，marked leaf 迫至多二；原 spanning-tree 貪婪構造 G／M 延拓，20／60 框架全排，含 root 交換。80 完整 degree 圖、2,400 joints／38,400 纖維、2,400 貪婪 witnesses；結合前三子型封閉全部 (3,1) incidence 分拆。(2,2) 的 mixed11+各側 unary 已由後續完成，其他 (2,2) incidence 保留，紙面＋Python，ε≥3 未證，未 Lean 化 |
| [ε=2 四-spoke (3,1) 原 mixed-(1,2) 三接點身份排除](c5_excess_two_mixed_core_four_spoke_ternary.md) | 同色原 spoke 省略後 M 自己 minimal，M−b保留原K=C+a的(a,y₀,y₁)與U；既有active-triangle K₅／leaf slack全排20／60框架，含root交換。200 queries、2,000 D₅、320 marked minors、50完整degree圖、1,500 joints／24,000纖維。後續mixed-(1,3)亦全排，(3,1)全incidence完成；紙面＋Python，ε≥3未證，未Lean化 |
| [ε=2 四-spoke binary 同列端點 hub 整型排除](c5_excess_two_mixed_core_four_spoke_hubs.md) | 原32／64具名域全部由保degree的同色端點hub及二／三hub Gallai K₅排除，含root交換，完成mixed-(1,1)加一原binary unary子型。192原queries、10,752完整U schemas、2,208 tightness、42完整degree圖／原K₅。不需新跨列palette定理，ε≥3未證，紙面＋Python，未Lean化 |
| [ε=2 四-spoke binary 原 star 的同源扇區排除](c5_excess_two_mixed_core_four_spoke_star.md) | 原a-star／連通H−a將116／256縮至32／64，276 subdivisions與24原degree圖；後續同列端點hub已排除全部殘留及整個binary子型。原012／0作K₃,₃排除，原star證書保留；ε≥3及跨列palette定理未證，紙面＋Python，未Lean化 |
| [ε=2 四-spoke (3,1) 一原 binary 的 marked-leaf 化約](c5_excess_two_mixed_core_four_spoke_binary.md) | 完整leaf反像與原C對角pair／偶數bridge給116／256域，star後32／64已由同列端點hub整型排除。720全圖joints、11,520 pinned纖維、原證書及單列代數資料保留；ε≥3未證，紙面＋Python，未Lean化 |
| [ε=2 四-spoke (3,1) 兩原 unary 六跨度排除](c5_excess_two_mixed_core_four_spoke_singles.md) | mixed-(1,1) 加兩單接點 unary 及 root 交換全排；原 critical witnesses、短支援外路徑與共同 lifts 給6≤5。288 同源支援域、46,305 支援核對、360 全圖 joints／5,760 pinned 纖維。後續已完成 (3,1) 全分拆；舊 byte-check 有一文件 hash 漂移，完整數學 payload audit 相同，原證書保留。紙面＋Python，ε≥3 未證，未 Lean 化 |
| [ε=2 唯一 mixed 原 leaf 色纖維與五-spoke 排除](c5_excess_two_mixed_core_leaf_fibers.md) | 八份具名附件共同化到998／1004；完整 (b,a,y,u) 接合迫同一原 unary 雙列只取0，palette 比較及原圖 K₅ 排除全部五-spoke來源。兩候選總 spokes 都≤4；450 全圖接合／7,200 pinned 色纖維、24 extracted K₅ 控制。選定的四-spoke 兩 unary 子型已由後續排除；單省略尚未全排，紙面＋Python，ε≥3 未證，未 Lean 化 |
| [ε=2 唯一 mixed 單 spoke 省略原附件化約](c5_excess_two_mixed_core_single_spoke.md) | 省略圖若拒絕便自己是唯一 degree-5 minimal core；8／6 child masks 與同色原 spoke 身份限制。666 骨架／58 subdivisions、五-spoke 原形給933≤4、941≤5；剩下四組941附件及 root交換已由後續原 leaf／unary 雙列比較全排。60 完整接合／960 pinned 查詢；單省略仍保留，紙面＋Python，ε≥3 未證，未 Lean 化 |
| [ε=2 唯一 mixed 省略原 mixed 必全收](c5_excess_two_mixed_omission.md) | 344 保留原 bridge roots 的必要核心／3,440 目標比較；9,152 固定支援查詢經 8,508 跨列衝突與 188 明示收縮星 subdivisions 全排。Σ(G−C)=Ω，完成相鄰唯一 mixed 的全部 (4,4) 核心身份；後續單 spoke 原附件化約已推進，(5,4)/(4,5)/(5,5) 仍保留。紙面＋Python，共同 ε≥2 不變，未 Lean 化 |
| [ε=2 唯一 mixed 兩側原 unary 省略全收](c5_excess_two_mixed_core_two_unary.md) | 5,700 目標比較／2,184,192 支援對必要比較全排，實際 386,048 互異查詢保存 UNSAT proofs／assignments；100,859 代數相容者由 3,180 明示雙收縮星 subdivisions 全排。完成 (4,4) 保留 mixed 全身份；只省略原 mixed 後續亦全排。1,282,500 完整雙接合、64 原雙 unary 圖，紙面＋Python，共同 ε≥2 不變，未 Lean 化 |
| [ε=2 唯一 mixed 原 spoke＋unary 省略全收](c5_excess_two_mixed_core_spoke_unary.md) | 37,320 目標比較的 2,784 抽象殘留經同一原支援 89,088 次 S₄ transport 及 2,640 明示 K₅／K₃,₃ 收縮星 subdivisions 全排，含交換型；後續雙 unary 亦全排，(4,4) 不能保留 mixed。559,800 完整算子控制，任意大小紙面＋Python，共同 ε≥2 不變，未 Lean 化 |
| [ε=2 唯一 mixed 原省略身份與雙 spoke 核心排除](c5_excess_two_mixed_core_spokes.md) | Proper core 原 incidence 省略表完整；(4,4) 保留 mixed 迫原共鄰 triangle。126 必要正常形／6,068 雙 spoke 接回全無 933／941 五像；後續 spoke＋unary 及雙 unary 全排，故 (4,4) 必省略 incidence-(1,1) 的原 mixed。26 長圖保存完整原關係，共同 ε≥2 不變，未 Lean 化 |
| [ε=2 單 triangle 保留原兩點接回排除](c5_excess_two_triangle_edge.md) | 同枝原環 K₅；其餘保留 z,w 的區段縮減給 528 必要正常形，392 份 T4 全收者均保持原單缺失。528 長圖／3,040 獨立 pinned 查詢、280 原 K₅ 控制；完成刪 zw 仍拒絕的相鄰 mixed 全分支，因此刪 zw 必全收。共同 ε≥2 不變，未 Lean 化 |
| [ε=2 原路徑接回 root 邊的 K₅](c5_excess_two_path_edge.md) | 同 singleton 框鄰點與原環直接給 apex K₅，任意長度樹／偶數路徑分支整型排除；八份 T4 基底、14 固定原路徑／226 具名接回／2,260 完整色對控制。單 triangle 停止點後由保留原兩點縮減完成；相鄰 mixed 刪 zw 必全收，共同 ε≥2 不變，未 Lean 化 |
| [ε=2 雙 roots 的原刪除與接回](c5_excess_two_root_deletions.md) | 至少一個原刪 root 圖全收，另一個至多只缺一列；相鄰 mixed 兩者均全收。全 degree-4 雙 triangle 分支由 64 原核心／512 完整色對接回排除，樹與單 triangle 後續亦全排；相鄰 mixed 刪 zw 必全收。全收、非相鄰與 no-mixed 保留，共同 ε≥2 不變，未 Lean 化 |
| [ε=2 t=0 全部分拆排除](c5_excess_two_no_spoke_complete.md) | 十一原分拆全排；多分量用真實外部路徑恢復跨度，(6) 飽和兩原 K₄ 給 K₅；(4,2) 的 200 查詢／7,200 弱 profiles 經 160 同源 binary 框弧證書全排。完成唯一 degree-6 的 ε=2 分支，只剩雙 degree-5 roots；共同 ε≥2 不變，未 Lean 化 |
| [ε=2 t=3 全部分拆排除](c5_excess_two_three_spoke_complete.md) | (2,1) 的十份 span-two 配置／8,250 同源 S₄ profiles 全排；(3) 的 100 容量比較及 (1,1,1) 六跨度矛盾完成整型。後續亦完成 t=0，唯一 degree-6 全分支排除；共同 ε≥2 不變，雙 degree-5 roots／一般來源保留，未 Lean 化 |
| [ε=2 t=2 全部分拆排除](c5_excess_two_two_spoke_complete.md) | 復用 t=1 的固定支援、共同 active forest 與原首橋；五種原接點分拆均整型排除，後續亦完成 t=3 及 t=0。共同 ε≥2 不變，雙 degree-5 roots／一般來源保留；任意大小紙面＋Python，未 Lean 化 |
| [ε=2 t=2 四接點整型排除](c5_excess_two_two_spoke_four.md) | 200 份 spoke／扇區／目標查詢全排；100 份三禁色 K₅、100 份非空支援族的固定兩末端袋無法並排；5,120 原 minor、526,336 完整五接點控制，未 Lean 化 |
| [ε=2 t=2 ternary／unary 整型排除](c5_excess_two_two_spoke_ternary.md) | 直接復用 t=1 singleton profiles；16 具名扇區位置、107,296 同框十列 profile 對無目標，不需 D 守恆；499,200 完整七接點控制，未 Lean 化 |
| [ε=2 t=2 兩 binary 整型排除](c5_excess_two_two_spoke_binary.md) | 40 具名扇區位置／400 查詢；原 pair 路徑留 20 份弱條件控制，補入同一首橋的共用 β 及局部 residual 跨列搬運後全排；保留完整原關係，未 Lean 化 |
| [ε=2 t=1 全部分拆排除](c5_excess_two_single_spoke_complete.md) | 唯一 degree-6 root 的七種原接點分拆均作整型來源排除；後續復用原工具完成 t=0、2、3，唯一 degree-6 分支全完成。兩候選共同 ε≥2 不變，雙 degree-5 roots 及一般來源保留；任意大小紙面＋Python，未 Lean 化 |
| [兩／三外部 hubs 的短支援排除](c5_short_support_singleton.md) | 原 degree-4 分量支援包含於一條框邊，且有避開它的原外部路徑時，全部禁色皆不可能；不限接點數，迫本題每份原分量跨度至少二；紙面＋原 K₅ controls，未 Lean 化 |
| [不依賴 ε 的盾弧預算與 hub 原則](c5_unary_shield_budget.md) | 固定來源、任意 ε：one-sided 分量支援為連續框弧且盾弧邊互斥，全圖至多兩份 unary；hub 原則統一短支援／K₄／二三-hub K₅ 並推廣到同色 roots 的 mixed 分量；A₄ 殘留 U 支援 40／58→24／30，無 frame 排除；紙面＋Python 控制，未 Lean 化 |
| [猜想 S 的可實現圖校準](c5_shield_calibration.md) | 21 張 T4 全收 Σ-edge-minimal 圖找到 5 份短支援 one-sided mixed；具名反例 S935／P0={5}（Σ=935）否定可實現圖類上的推廣，限定 933／941 的原猜想 S 未決；unary 盾弧性質全無違反；有限 Python 證書，未 Lean 化 |
| [q-core 盾弧預算與共鄰 P₃ 目錄排除](c5_qcore_shield_budget.md) | 改色引理（既有）＋盾弧引理移植到單列 q-core，保留 singleton 缺點；不需 T4 的定理 C-W（2+2+2>5）把共鄰 P₃ 目錄 3497 keys 全部來源排除；D₆ 稽核確認並補零-unary 側，C §1 整個共鄰端點 P₃ 分支排除完成；verdict 修訂版（v1 保存）；ledger 已合併為 cw-v1；紙面＋外部 Gallai＋Python 證書，未 Lean 化 |
| [Kempe 轉運有限表與 hub-linkage 停止見證](c5_kempe_transport.md) | 933／941 各 20 筆單 block 轉運，共同 partition 候選全部非交錯；單點 P 控制得 Σ=1012 停止見證（無 hubs、非交錯，對角鏈交換碰框入 Σ）；否定一般局部二分，固定來源 K 未決；有限 Python，未 Lean 化 |
| [超額–拒絕定律 E 的有限證據](c5_excess_rejection_law.md) | 有效內點 k≤5 完整窮舉 310 個 T4 全收 Σ-edge-minimal disk 類，全部滿足 ε≥2\|Q\|−e(Q)−2；四種可實現形狀最小 ε=0／1／2／2 等於下界；933／941 形狀在 k≤5 無合格圖；任意大小與 k≥6 未決；Python 有限證書，未 Lean 化 |
| [猜想 E 的 ε≤1 層（任務 E2）](../artifacts/c5_excess_one_e2/REPORT.md) | ε=0 ⇒ \|Q\|≤1；ε=1 ⇒ Q 為一點或相鄰兩點：935 以真子核心＋原 K₃,₃，951 以雙列 full-minimal／Gallai palette／盾弧全排；任意大小紙面＋外部 Gallai＋五個 checker；D₇ 稽核確認，舊 one-pendant 產物層已標為被取代；未 Lean 化 |
| [單點對角 Kempe 轉運（任務 K′）](c5_kempe_diagonal_transport.md) | \|P\|=1、N(P) 四色、相鄰 degree-5 roots：紙面引理 1–6 含 Jordan 側別（只需 disk／四色／rotation）迫兩條對角鏈皆斷開；L2 仍有 933：192、941：384 筆一致指派，與可實現的 1012／935 控制同型，K′ 未決；具名 KD933-0001／KD941-0001；整合時另核對同 split 多鏈＋自由 block 交換亦無新排除；有限 Python，未 Lean 化 |
| [猜想 E 的 ε=2 層（任務 E3，部分）](../artifacts/c5_excess_two_e3/REPORT.md) | 約化：\|Q\|+c(Q)>4 ⇔ Q 含 941 形三點，只需排除拒絕 q₀、q₁、q₃；triple-critical 引理（每條非框邊刪除新收三列之一）；唯一 degree-6 的 t=0–3 共 26 分拆在三列前提下全排；雙 degree-5 roots 留 N1–N3、J1–J6 及待 K′ 入口；精確 E1 951／935 控制保留；[D₈ 稽核](../audits/2026-10-04-task-d8/REPORT.md)：有缺口但可補，t=1 的 (4,1)／(3,2) 漏相對 spoke 位置（DG6-1），稽核補表 100 份幾何 0 存活（報告 §10）；紙面＋外部 Gallai＋四個 checker，未 Lean 化 |
| [猜想 E 的 ε=2 層：非相鄰雙 roots（任務 E4，部分）](../artifacts/c5_excess_two_e4/REPORT.md) | N-theta（三份 mixed 的 z–w 路徑把一份困離框）＋N-empty 迫 m≤2，N3 全排；N-empty-separating、tree-H Euler（ε=2 ⇒ H 有環）為純拓撲；N1 排 mixed (2,2) 有 (4,4) core 整類（3+3>5），N2 排兩短無 unary；其餘 N1／N2 完整 relation 殘留；未找到合格非相鄰正控制；附並行 core-constraints 補充與兩份獨立複核；紙面＋Python，未 Lean 化 |
| [猜想 E 的 ε=2 層：相鄰分支精確列依賴（任務 E5，部分）](../artifacts/c5_excess_two_e5/REPORT.md) | 依賴項×四分支（941／933／940／932）表；L1：任一真子圖只拒絕空、單點或相鄰二點（不需三列）；四分支排 J2 mixed12、J3 ternary、A equal pairs、B mixed22 全 leaf，932 另排五-spoke 與 J3 binary；A 的 N 全收與 singleton-U 身份補齊；殘留 G1–G4；停止 (c)：E3 對 A 前序的依賴判定過強（C12 長環已排除），數學 payload 無誤；紙面＋Python，未 Lean 化 |
| [ε=2 特化有限搜尋（任務 ES）](c5_excess_two_finite_search.md) | 單調 T4 剪枝、一次 criticality、完整對稱 canonical orbits；k≤6 與獨立暴力版逐計數／逐 orbit 一致。非相鄰、相鄰、唯一 degree-6 三型完整搜到 k=9：179 個 crit orbits，Q 只有單點／相鄰二點／非相鄰二點／三點弧，無 \|Q\|+c(Q)>4；含 935、951 及 NA6-1–3 正控制；整合者獨立重驗 179 代表並重播全量 `--check`；有限證據，不升格為定理，未 Lean 化 |
| [四接點短支援 pair 排除](c5_short_support_four_contact.md) | 四接點未見二色 pair 的原 Gallai leaf blocks／active 結構 K₅；保留獨立證明及固定控制，通用短支援引理另涵蓋此型 |
| [ε=2 t=1 四接點與 unary](c5_excess_two_four_one.md) | 同一四接點 active forest、兩 triangle K₅及固定末端區塊的跨列 residual，100 個必要查詢全排；(4,1) 整型排除，未 Lean 化 |
| [ε=2 t=1 ternary／binary](c5_excess_two_ternary_binary.md) | 新 ternary D 身份守恆與原 binary 路徑塊共同支援，100 查詢全排；去掉路徑條件仍有八份抽象殘留；(3,2) 整型排除，未 Lean 化 |
| [ε=2 t=1 五接點排除](c5_excess_two_five_contact.md) | 原 spoke 私有色迫共同五葉 active tree；正 C₅或三正 triangles 均原 K₅，4,800 minor 控制；(5) 整型排除，未 Lean 化 |
| [ε=2 t=1 三接點加兩 unary](c5_excess_two_ternary_two_unary.md) | 三接點容量至多一，168 份具名支援／146,496 份同源十列 profiles 無目標；(3,1,1) 整型排除，未 Lean 化 |
| [ε=2 t=1 binary 加三 unary](c5_excess_two_binary_three_unary.md) | 共同支援包絡及同源 S₄ profiles 完成 2,200 次比較，另有 50 固定弧排除；(2,1,1,1) 整型排除，未 Lean 化 |
| [ε=2 t=1 五原 unary](c5_excess_two_five_unary.md) | 四容量子覆蓋迫 root 帶至少三條 bridges 的全 degree-4 核心，違反既有分類；3,000 覆色配置／8,400 子覆蓋；T4／degree 前提下較強得 Σ=Ω，未 Lean 化 |
| [ε=2 t=1 原 binary 省略](c5_excess_two_single_spoke_binary.md) | (2,2,1) 任一原 binary 省略全收；1,480 次比較全排除，2,192 次 singleton／16,440 次二元素完整六接點控制，16,576 個染色 lifts。結合分類，該型無全 degree-4 真子核心；整型後由 t=1 全分拆報告排除，原省略證書保留 |
| [ε=2 t=1 兩原 unary 省略](c5_excess_two_single_spoke_two_unary.md) | (2,1,1,1) 任意兩原 unary 省略全收；1,480 次比較由三 root 色存活等排除，30,825 次完整六接點控制。結合分類，該型無全 degree-4 真子核心；整型後由 t=1 全分拆報告排除，原省略證書保留 |
| [ε=2 t=2 四原 unary 排除](c5_excess_two_four_unary.md) | 固定支援五段預算迫唯一 D 分量及連續三點拒絕位置；933／941 整份 (1,1,1,1) 型排除。50 次目標／弧比較、810,000 完整五接點控制；任意大小紙面＋Python、未 Lean 化，共同 ε≥2 不變 |
| [ε=2 t=2、(2,1,1) 原 binary 省略排除](c5_excess_two_binary_two_unary.md) | 560 代數殘留的 65,100 次共同支援弧比較全排除；46,800 完整五接點控制。所有容量二省略均全收；整型後由短支援引理三分量六跨度排除，原省略證書保留；未 Lean 化，共同 ε≥2 不變 |
| [ε=2 t=2、(2,1,1) 兩份原 unary 省略排除](c5_excess_two_two_unary.md) | 3,980 比較全排除、24,975 次完整五接點接合控制；不需 D 守恆或新增支援幾何，當輪留下的 binary 身份由後續排除，整型再由短支援引理六跨度排除；原證書保留，未 Lean 化 |
| [ε=2 t=2、(2,2) 原 binary 省略排除](c5_excess_two_two_binary.md) | 3,980 比較、原核心 apex K₃,₃ 及第二核心 2,376 次同框五接點接合全排除；兩份 binary 省略均全收，該型無全 degree-4 真子核心。後續原首橋報告排除整型，原省略證書保留；未 Lean 化 |
| [ε=2 t=3、(2,1) 原 binary 省略排除](c5_excess_two_binary_omission.md) | 250 份共同支援包絡／2,030 比較全排除；983,025 四接點接合控制。刪除原 binary 必全收，該型無全 degree-4 真子核心；整型後由 t=3 同源 S₄ profiles 排除，原省略證書保留，未 Lean 化 |
| [ε=2 三 spokes／三原 unary 共同扇區排除](c5_excess_two_three_unary.md) | 800 個必要比較、225 份抽象存活 cases 經原支援跨度與共同扇區全排除；33,750 份四接點接合控制。任意大小紙面＋Python，關閉 t=3 path／tail 及整份 spoke＋unary 省略分支，未 Lean 化；其餘 ε=2 保留 |
| [ε=2 t=3 原 triangle 的 spoke＋unary 排除](c5_excess_two_three_spoke_unary.md) | 398 marked roots／1,194 接回的 11,940 比較全排除；兩色存活留 1,254 個，由同一 binary 省略圖單缺失排除 1,200 個、既有雙 spoke 省略排除 54 個。完整 (r,x,y,v) 及任意大小原 unary 保持，紙面＋Python、未 Lean 化；path／tail 由後續三 unary 排除，其餘 ε=2 保留 |
| [ε=2 t=2 的 spoke＋原 unary 排除](c5_excess_two_spoke_unary.md) | 省略一條原 spoke 及一份原 unary 仍拒絕列的分支，以五接點精確接合與兩 root 色存活排除；148 marked cores／592 接回、5,920 次候選比較全排除。原 unary 任意大小及附件保持，紙面＋Python、未 Lean 化；後續完成 t=3 原 triangle 位置，共同下界仍 ε≥2 |
| [ε=2 唯一 degree-6 root 雙 spoke 排除](c5_excess_two_double_spoke.md) | 省略兩條原 spokes 仍拒絕列的條件分支，由原四接點化約及 888 次接回排除 933／941；候選刪任意兩條原 spokes 必接受全部十列。432 個 T4 全收模型至多兩個相鄰 singleton 拒絕；後續另完成 t=2 spoke＋unary 分支。紙面＋Python、未 Lean 化，其餘 ε=2 未涵蓋 |
| [941 three-spoke 排除與 ε≥2](c5_941_three_spoke.md) | 原 triangle degree-2 root 的 (r,x,y) 完整關係化約；118 必要核心／398 marked roots 的 1,194 次接回全無 941，完成 ε=1 最後 t=3、(2)，合成 ε≥2。後續排除 ε=2 的條件式雙 spoke 分支；紙面＋Python、沿用既有分類，未 Lean 化，一般來源仍未排除 |
| [941 excess-one two-spoke 來源排除](c5_941_two_spoke.md) | 原首點／四接點完整關係化約及 592 次接回排除 t=2、(2,1)；後續完成 t=3 並得到 ε≥2。任意大小紙面＋Python、沿用既有分類，未 Lean 化 |
| [941 excess-one single-spoke 來源排除](c5_941_single_spoke.md) | 三份原末端支援的六跨度與原邊完整 relation 排除 t=1、(2,1,1)；後續排除 t=2、3 並得到 ε≥2；紙面＋局部 Python，未 Lean 化 |
| [ε=1 四容量子覆蓋與共享](c5_excess_one_subcovers.md) | 933 已證 ε≥2；941 的三種 spoke 殘餘由後續全排除。省略身份跨列互斥、五單容量至多兩拒絕；同源 943 十列／16 因子子集控制，任意大小紙面合成沿用既有分類，未 Lean 化，兩候選一般來源仍未排除 |
| [933／941 excess、容量與跨度下界](c5_independent_support_capacity.md) | 第一輪共同 ε≥1、mixed 條件容量與 unary 六跨度禁形保留；後續兩候選均提高至 ε≥2。未證候選必含六跨度禁形；紙面＋三張固定圖控制，未 Lean 化 |
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
| [D₂文件整合與新增成果稽核](../audits/2026-10-04-task-d2/REPORT.md) | 套用原D的18項修訂，同步A₂／B₂／C₂停止點；新增A／A₂、B／B₂固定域身份、完整joint及witness獨立稽核。原D的40 PASS／4文件hash FAIL與兩份完整payload相同紀錄保留；新增版本及漂移另記，原artifacts不改 |
| [D₃：C／C₂獨立稽核](../audits/2026-10-04-task-d3/REPORT.md) | 固定D₂截點的完整P₃／側角色／空fibres、原unary刪邊witnesses及原K₅全部獨立核對；只關閉geometry30／join20，保存3500具名keys。當時未接收A₃／B₃／C₃及未同步live文件；原strict漂移失敗保留 |
| [D₄：正式返回A₃／B₃／C₃快照與整合稽核](../audits/2026-10-04-task-d4/REPORT.md) | 獨立核對三份新增成果與13份並行更新，A保存18／22；B₂＋B₃只登記W933-101／W941-139兩骨架封閉；C₃只關閉geometry34／join20。前輪交付hash／完整relations／空fibres／witnesses與失敗紀錄保持，未commit／push |
| [D₅：A₄／B₄／C₄最終快照與獨立稽核](../audits/2026-10-04-task-d5/REPORT.md) | 逐身份A ledger降至16／20；B只關閉W933-129長face的shared-{4}支；C只新增geometry34／join60，3500keys及36／140／900表保持。三項最終重播、版本／實際依賴與歷史失敗分別封存；當輪未發布，本批發布及還原入口見下方歷史紀錄 |
| [C₅ 全線進展與高階假設](c5_research_synthesis.md) | 八線成果與證據界線整合；H1 已在固定完整 Σ933／941 的 Σ-edge-minimal induced-C₅ disk source 等原前提下成立；H2／H3 及一般推廣仍未證；保存當輪快照，不替代導覽排程 |
| [C₅ 關係階數與接合上界](c5_relation_arity.md) | 132類為11個二階、101個四階、20個五階；原邊重驗20反例及100份局部延拓；紙面證接合r*≤來源最大階數≤5、T4全收時≤4；六圖回歸，非一般五階接合實現或多步state定理，未Lean化 |
| [C₅ class 兩點重疊](c5_two_vertex_overlap.md) | 132 類／1,320 點對索引與兩點相容、單側投影語義已保存；695 強迫異色、625 自由；六份接合與三份控制拓撲由後續完成，完整後繼表及多步充分性保留 |
| [C₅ 具名八點接合與同圖核對](c5_two_vertex_join.md) | 一次 evaluator 與六份完整八點 relation／雙側回投影全經整圖核對；主例 140 軌道、A=R1016／B=R1023；主例及正反向私有內點原框由後續完成，六圖 U 上五框可用性由跨例 audit 完成，其餘拓撲、完整後繼表與多步充分性保留 |
| [C₅ 兩點接合主例拓撲](c5_two_vertex_join_topology.md) | 同一八點十邊圖的 36 組環序／24 份外面配置全核對；兩原框各自可作整圖外界，四種區域關係有見證，無八點 simple 外框；政策及其他代表保留，紙面＋Python，未 Lean 化 |
| [C₅ 私有內點接合與兩原框阻斷](c5_two_vertex_private_topology.md) | 指定十五點三十五邊圖平面，兩來源 disk 可內部互斥；兩組交錯原路徑排除 A、B 作整圖外界，完整 J 仍 60 軌道；反向控制由後續完成，紙面＋Python，未 Lean 化 |
| [C₅ 私有內點反向接合拓撲](c5_two_vertex_private_reverse_topology.md) | 反向原十五點三十五邊圖平面、來源 disk 可內部互斥、兩原框皆被阻斷；完整 J 與正向各有 16 個獨有 patterns；混合外面 relation 由後續完成，紙面＋Python，未 Lean 化 |
| [C₅ 反向混合外框完整 relation](c5_two_vertex_mixed_frame.md) | 指定 `(a0,a4,a3,a2,b2)` 外框為完整 R255／8 軌道／192 賦色，原 J 纖維及十內點延拓全核對；等於既有單內點 disk 代表，替換須密封其餘點，未 Lean 化 |
| [C₅ 反向第二混合外框完整 relation](c5_two_vertex_second_mixed_frame.md) | 指定 `(a0,b4,b0,a2,a1)` 外框為完整 R1022／9 軌道／216 賦色，只拒絕 `01012`；原 J 纖維、十內點延拓及雙內點 disk 代表一致，與 R255 非 D₅ 等價，未 Lean 化 |
| [C₅ 兩混合框共同拉回與精確修復](c5_two_vertex_mixed_pullback.md) | 拉回114軌道、J為60；具名精確 repair 等式已由 NamedRepair 對指定兩框形式化；完整差集、原邊拒絕及拓撲仍為紙面＋Python |
| [C₅ 全部三點投影與四點 arity 下界](c5_two_vertex_ternary_projections.md) | 指定兩框 P 的無輔助變數投影合取模型 r*=4 已由 NamedRepair 形式化；56份三點投影、16個殘留軌道／384賦色與896份延拓仍為 Python 證書 |
| [C₅ 四點投影的最少個數與全部最小組合](c5_two_vertex_quaternary_repairs.md) | 指定兩框 P 的最少兩份、唯一組合 `(a0,a1,a2,a3)` 與 `(a2,b0,b2,b4)` 已由 NamedRepair 形式化；70 scopes 的完整排除表及2,415配對仍為 Python 證書 |
| [C₅ 全部 inclusion-minimal 四點修復](c5_two_vertex_minimal_repairs.md) | 指定反向圖、原 U 與兩框 P 的完整15組極小分類已由 NamedRepair 形式化；一組二份、十四組三份；原排除表、44份刪除見證與拓撲證書保留 |
| [C₅ 六例 local-repair transport audit](c5_two_vertex_repair_transport.md) | 兩核心指定框的各15組極小 repairs、唯一 forced A 及 r*=4 已 Lean 化；四例 P=J、全20條五環的14條可用性及 transport 差異仍為紙面＋Python |
| [C₅ 共同 repair 充要 lemma](c5_two_vertex_common_repair.md) | 抽象 W／C 雙向判準及極小／極大失敗分類等已有普通 Lean 證明；兩核心指定框前提由 NamedRepair 形式化；四個退化圖及拓撲／獨立性控制仍為 Python |
| [C₅ repair 來源充分條件](c5_two_vertex_repair_sources.md) | 原私有接線及每例十一份補全證成 W／C；保核心的度數三消去與外框證書給任意大小指定族、r*=4；兩原框可用另給 P=J；兩核心指定框 J/P、W／C 及 r*=4 已 Lean 化；任意大小及拓撲仍為紙面＋Python，增大族見後續補片 |
| [C₅ 不能逐點消去的密封 clique 補片](c5_two_vertex_repair_patches.md) | 完整 clique 附件＋一份染色延拓全部核心染色；三角剖分核心自動給保核心 disk 擴張的附件，配合保框證書保留十五組 repairs／r*=4；不含舊核心的奇偶路徑族由後續完成，未完成全部代表分類，紙面＋Python，未 Lean 化 |
| [C₅ 不含舊核心的私有路徑奇偶定理](c5_two_vertex_repair_strips.md) | 指定完整接線族內，A 兩臂偶長及 B 奇長充要保持 R127／R167；加長圖無保持框點及 ownership 的舊核心副本，仍保十五組 repairs／r*=4；十圖14,400份延拓及八奇偶控制；非路徑輪環骨架由後續推進，全部代表未分類，紙面＋Python，未 Lean 化 |
| [C₅ 舊補片／路徑之外的完整四接點輪環替換](c5_two_vertex_repair_rings.md) | 四輪星與四環帶加中心的完整四接點關係相等；任意層數同 class disk 族無密封 clique 補片、私有圖含環且無舊核心副本，保十五組 repairs／r*=4；八圖11,520份延拓；輪環逆化約後的其他骨架由後續雙扇推進，必要分類仍未完成，紙面＋Python，未 Lean 化 |
| [C₅ 輪環逆化約之外的完整四接點偶長雙扇替換](c5_two_vertex_repair_fans.md) | 偶長雙扇與四輪星完整四接點關係相等；任意大小同 class 族無密封 clique 補片、私有圖含環且無私有度數五點，三種舊縮減均無起點；保十五組 repairs／r*=4，八圖11,520份延拓；加入雙扇後的其他骨架由後續 D₁₃ 推進，必要分類保留，紙面＋Python，未 Lean 化 |
| [C₅ 輪環與偶長雙扇之外的十三點非對稱 disk](c5_two_vertex_repair_caps.md) | D₁₃／四輪星完整四接點等價及密封替換已由後續 Lean 證成；任意大小來源族、私有度數障礙、完整 J/P、十五組 repairs／r*=4 仍為紙面＋Python，全部代表必要分類保留 |
| [Lean 接合基礎](lean_root_interfaces.md) | 15 個普通 Lean 定理與報告對照；各項形式化範圍見原報告；完整 minor／disk 層仍未形式化 |
| [Lean 共同 repair 判準](lean_common_repair.md) | 27 個普通 theorem：W／C 充要判準、極小修復／極大失敗與完整殘留、唯一最少解、退化支及具名投影；公理審計通過，兩核心指定框前提由後續 NamedRepair 完成 |
| [Lean D₁₃ 四接點及密封替換](lean_sealed_four_port.md) | 22 個普通 theorem：原32邊完整關係、三型延拓、任意外部共同關係保留、中心及缺邊控制；公理審計通過，無 native_decide；disk 與來源族未形式化；兩核心 W／C 由 NamedRepair 完成 |
| [Lean 具名來源 J/P 與 W／C](lean_named_repair.md) | 34 個普通 theorem：兩核心原35邊延拓、指定框 P、完整70 scopes、各15組極小 repairs、唯一最少對及 r*=4；audit 通過，無 native_decide；disk 框完備性與替換來源族保留 |
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
唯一 degree-5 的指定核心分離已由後續主線完成；R31 任意長來源 minor
與一般三環構造問題仍保留，研究線標記見 HANDOFF。

### 2.6 全 degree-4／block 化約系列

[全 degree-4／block 系列導讀](c5_degree4_guide.md) 統整小核心、樹、triangle、
任意 block tree、長奇環與 K4 的依賴順序；原報告仍直接列於 §2.1。
接受 T4 的 C5 disk minimal q-obstruction，若所有有效內點完整 degree=4，
則只缺 q；此任意大小合成依賴紙面化約、外部 degree-list 與有限證書，未完整 Lean 化。
兩 triangle 的直接 bridge 型可存活；固定 q 的 minor 不自動保持完整 Σ。
一般 degree≥5 與共同出口仍開放，研究線標記見 HANDOFF。

## 3. 已被後續成果處理的舊停止點

以下是既有成果的後續入口，不是本次重新證明；表內「下一題」是當時的演進順序。

| 舊問題或容易誤讀的字樣 | 目前讀法／後續入口 |
| --- | --- |
| 雙扇報告的「輪環與偶長雙扇化約後的其他骨架」 | [十三點非對稱四接點 disk](c5_two_vertex_repair_caps.md) 給兩種局部逆化約均無起點的任意大小同 class 族及新充分規則；完整 J/P、全部外框及 repairs 保留，必要分類與改寫完備性仍未證 |
| 輪環報告的「加入輪環化約後的其他骨架」 | [完整四接點偶長雙扇替換](c5_two_vertex_repair_fans.md) 給私有圖含環且無私有度數五點的任意大小同 class 族；三種舊縮減無起點，新雙扇規則可化約，全部代表必要分類與改寫完備性仍保留 |
| 奇偶路徑報告的「補片及奇偶化約外的骨架」 | [完整四接點輪環替換](c5_two_vertex_repair_rings.md) 給無密封 clique 補片、私有圖含環的任意層數同 class disk 族；新局部化約保持完整關係及 repairs，加入輪環化約後其餘骨架與必要分類保留 |
| 補片報告的「不含指定核心」 | [私有路徑奇偶定理](c5_two_vertex_repair_strips.md) 已給不含保持框點及 ownership 的舊核心副本的任意長度同 class 族；指定接線內必要及充分奇偶分類完成，密封補片及奇偶化約後的其他骨架仍未分類 |
| 來源充分報告的「不能作私有度數三消去」 | [密封 clique 補片](c5_two_vertex_repair_patches.md) 已給任意大小、最低新增度數五而保 repairs 的來源族，證明舊消去條件非必要；後續奇偶路徑定理亦跨過含舊核心限制，全部代表仍未分類 |
| 共同 repair lemma 的「下一步可檢查來源結構」 | [來源充分條件](c5_two_vertex_repair_sources.md) 已證指定核心、私有度數三消去與保框證書足夠；後續補片定理放寬逐點消去要求；兩原框可用給獨立退化支，未完成全部代表必要分類 |
| 六例 transport audit 的「下一步抽象共同 repair lemma」 | [共同 lemma](c5_two_vertex_common_repair.md) 已證 witness／覆蓋充要條件並核對六圖；[抽象 Lean 判準](lean_common_repair.md) 已完成，兩核心指定框前提已由 [NamedRepair](lean_named_repair.md) 形式化；來源充分條件見後續報告，四個 P=J 仍為獨立退化支 |
| P₃ 非對稱報告的「下一題 masks=(0,1,2)」 | [中點／端點接線](c5_mixed_p3_middle_endpoint.md) 已保留原末端三條附件並排除全部 residual；不同接點各一 incidence 已全涵蓋，共鄰接點仍保留 |
| P₃ 中點／端點報告的「下一題 masks=(0,0,3)」 | [共鄰端點雙扇區](c5_mixed_p3_common_endpoint.md) 給任意 unary 短子弧與部分來源排除；保留原鏈，尚留 36 具名必要 residual，未證指定出口 |
| Mixed 容量的「P₃ 對稱分支內外側／實際附件未處理」 | [原五環與完整側支援](c5_mixed_p3_symmetric.md) 已排除兩端各一 incidence、兩側同 pair 的 disk 來源；非對稱及其他接線不在本結論內，未新增 target 接受 |
| Single-spoke 的「下一題 (4) 三份拒絕 palettes」 | [共同結構與 K5](c5_single_spoke_four.md) 以共同 τ 排除正 bridge，四葉只剩兩 triangle 加單 bridge；t=1 全部接回出口，t=0 後由 no-spoke 報告收窄為兩型 |
| Single-spoke 完成後的「t=0 外部連通與 K4」 | [No-spoke 排除](c5_no_spoke_exterior.md) 以另一原分量恢復外部 hub，(5) 另作四列奇偶排除；六型剩兩型；後續 [環狀支援](c5_no_spoke_supports.md) 已完成 (2,1,1,1) 指定分離，(2,2,1) 再由 [首橋／框弧](c5_no_spoke_first_bridge.md) 完成 |
| Single-spoke 的「下一題 (3,1) 最小三接點 subtree」 | [三接點排除](c5_single_spoke_three_one.md) 已由 active triangle 加三臂及原 tethers／唯一 spoke 給 K5，不需 T4；後續 (4) 亦已排除 |
| (2,2) record 90／282 的「β=0／p₂ 未決」 | [局部 residual](c5_single_spoke_residual_locality.md) 以相同局部列迫使相同 E，排除支援 034；首兩塊皆接 b2、b3，原圖 K5 關閉最後兩查詢；非來源排除 |
| (2,2) record 87 的「singleton/pair 相容性未證」 | [首橋相容性](c5_single_spoke_first_bridge.md) 以 q 證書同一首橋 palette 綁定兩端實際支援，β=0／2 均給 K5；p₂ 已證，未排除來源，舊 pair 介面不變 |
| (2,2) record 16 的「p₁ 未決」 | [跨列 residual](c5_single_spoke_cross_row.md) 迫使每塊實際接 b1、b2，原 spoke 完成 K5 反證；已證指定列延拓，未排除來源或求完整 Σ |
| (2,2) record 17 的「缺第三外部落點／雙列未決」 | [兩框弧 K5](c5_single_spoke_two_arc.md) 把另一原分量納入 Z，每塊跨同一份兩弧分割即可；兩列均延拓，不需 bridge 長度上界，未排除 record 17 來源或求完整 Σ |
| No-mixed 的「影響 R 的增長完備性仍依表」 | [三個側弧位置與固定配方](c5_no_mixed_growth_completion.md) 已免查支援表證成，結合無增長定理完成指定雙列存在性分離；逐染色 repair、一般出口及完整 Σ 仍未證 |
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

各線保留缺口與下一步由上列導覽維護，這裡不重複研究排程。
核心分離與一般出口見 [weak-deletion](c5_weak_deletion_guide.md)，
R31 來源 minors 見 [degree-5](c5_degree5_guide.md)，
完整形式化依賴見 [Lean](lean_guide.md)。
所有「已完成」均限於原報告前提；來源排除與指定列延拓不互換。

## 歷史紀錄與舊連結

- [2026-10-04：併行成果、D至D₅獨立稽核與完整封存發布](history/2026-10-04-c5-parallel-progress-publish.md)

- [2026-10-04：D₂文件整合、A／B新增成果稽核與保存核對](history/2026-10-04-task-d2-integration-audit.md)
- [2026-10-04：正式返回A₃／B₃／C₃的固定快照與D₄獨立整合稽核](history/2026-10-04-task-d4-returned-integration-audit.md)
- [2026-10-04：A₄／B₄／C₄最終快照與D₅獨立整合稽核](history/2026-10-04-task-d5-final-integration-audit.md)
- [2026-10-04：任務 A，mixed-(1,2)+a-unary 的01／23來源排除與具名殘留](history/2026-10-04-excess-two-four-spoke-mixed12.md)
- [2026-10-04：A₂，mixed-(1,2) 的01／12長／短face與完整joint排除](history/2026-10-04-excess-two-four-spoke-mixed12-01-12.md)
- [2026-10-04：A₃，mixed-(1,2) 共用01／01四rotations與原ax非critical](history/2026-10-04-excess-two-four-spoke-mixed12-01-01.md)
- [2026-10-04：A₄，mixed-(1,2) 原04／04具名三hub與完整joint來源排除](history/2026-10-04-excess-two-four-spoke-mixed12-04-04.md)
- [2026-10-04：任務 B，四-spoke mixed-(2,2) 無 unary 的七身份與窄化約](history/2026-10-04-excess-two-four-spoke-mixed22.md)
- [2026-10-04：B₂，mixed-(2,2) 原短 face 的 Gallai leaf／原 K₅ 排除](history/2026-10-04-excess-two-four-spoke-mixed22-short-face.md)
- [2026-10-04：B₃，mixed-(2,2) 同骨架原長 face 的 leaf bridge／原 K₅](history/2026-10-04-excess-two-four-spoke-mixed22-long-face.md)
- [2026-10-04：B₄，933 原04／12的shared附件{4}／原cut parity](history/2026-10-04-excess-two-four-spoke-mixed22-shared4.md)

- [2026-10-03：ε=2 四-spoke 七輪進展整理與發布](history/2026-10-03-excess-two-four-spoke-progress-publish.md)
- [2026-10-03：ε=2 四-spoke 同一長 face 的兩原 unary 次序排除](history/2026-10-03-excess-two-four-spoke-long-face.md)
- [2026-10-03：ε=2 四-spoke 原 unary crosscut 與 mixed 二／三 hub 排除](history/2026-10-03-excess-two-four-spoke-crosscut.md)
- [2026-10-03：ε=2 四-spoke 共用短框弧的原拒絕列延拓](history/2026-10-03-excess-two-four-spoke-short-arc.md)
- [2026-10-03：ε=2 四-spoke mixed-(1,1) 加各側 unary 子型完成](history/2026-10-03-excess-two-four-spoke-disjoint-pairs.md)
- [2026-10-03：ε=2 四-spoke 原 unary 短 face 與非 critical 接線](history/2026-10-03-excess-two-four-spoke-short-face.md)
- [2026-10-03：ε=2 四-spoke (2,2) 共用原 pair 的 sealed mixed 窄排除](history/2026-10-03-excess-two-four-spoke-equal-pair.md)
- [2026-10-03：ε=2 四-spoke 原 mixed-(1,3) 四接點 leaf-slack 排除](history/2026-10-03-excess-two-four-spoke-quaternary.md)
- [2026-10-03：ε=2 四-spoke 原 mixed-(1,2) 三接點身份整型排除](history/2026-10-03-excess-two-four-spoke-ternary.md)
- [2026-10-03：ε=2 四-spoke binary 同列端點 hub 整型排除](history/2026-10-03-excess-two-four-spoke-hubs.md)
- [2026-10-03：ε=2 四-spoke binary 原 star 的同源扇區排除](history/2026-10-03-excess-two-four-spoke-star.md)
- [2026-10-03：ε=2 雙 degree-5 root 九輪進展整理與提交](history/2026-10-03-excess-two-dual-root-progress-commit.md)
- [2026-10-03：ε=2 四-spoke (3,1) 一原 binary 的 marked-leaf 必要化約](history/2026-10-03-excess-two-four-spoke-binary.md)
- [2026-10-03：ε=2 四-spoke (3,1) 兩原 unary 六跨度排除](history/2026-10-03-excess-two-four-spoke-singles.md)
- [2026-10-03：ε=2 唯一 mixed 的原 leaf 色纖維與五-spoke 排除](history/2026-10-03-excess-two-mixed-core-leaf-fibers.md)
- [2026-10-03：ε=2 唯一 mixed 的單 spoke 原附件化約](history/2026-10-03-excess-two-mixed-core-single-spoke.md)
- [2026-10-03：ε=2 唯一 mixed 的省略原 mixed 全收](history/2026-10-03-excess-two-mixed-omission.md)
- [2026-10-03：ε=2 唯一 mixed 的兩側原 unary 省略全收](history/2026-10-03-excess-two-mixed-core-two-unary.md)
- [2026-10-03：ε=2 唯一 mixed 的原 spoke＋unary 省略全收](history/2026-10-03-excess-two-mixed-core-spoke-unary.md)
- [2026-10-03：ε=2 唯一 mixed 的原省略身份與雙 spoke 核心排除](history/2026-10-03-excess-two-mixed-core-spokes.md)
- [2026-10-03：ε=2 單 triangle 保留原兩點接回排除](history/2026-10-03-excess-two-triangle-edge.md)
- [2026-10-03：ε=2 原路徑接回 root 邊的 K₅ 排除](history/2026-10-03-excess-two-path-edge.md)
- [2026-10-03：ε≥3 入口的雙 root 刪除與原邊接回](history/2026-10-03-excess-two-root-deletions.md)
- [2026-10-03：ε=2 唯一 degree-6 分支成果整理與發布](history/2026-10-03-excess-two-degree-six-publish.md)
- [2026-10-03：ε=2 t=0 全部分拆與唯一 degree-6 分支排除](history/2026-10-03-excess-two-no-spoke-complete.md)
- [2026-10-03：ε=2 t=3 全部分拆整型排除](history/2026-10-03-excess-two-three-spoke-complete.md)
- [2026-10-03：ε=2 t=2 成果整理與發布](history/2026-10-03-excess-two-two-spoke-publish.md)
- [2026-10-03：復用 t=1，完成 ε=2 t=2 全部分拆整型排除](history/2026-10-03-excess-two-two-spoke-complete.md)
- [2026-10-03：ε=2 省略證書與 t=1 全分拆進展整理、發布](history/2026-10-03-excess-progress-publish.md)
- [2026-10-03：ε=2 t=1 全部分拆整型排除](history/2026-10-03-excess-two-single-spoke-complete.md)
- [2026-10-03：t=1 原 binary 省略與完整六接點接合](history/2026-10-03-excess-two-single-spoke-binary.md)
- [2026-10-03：t=1 兩原 unary 省略與三色存活](history/2026-10-03-excess-two-single-spoke-two-unary.md)
- [2026-10-03：t=2 四原 unary 固定支援排除](history/2026-10-03-excess-two-four-unary.md)
- [2026-10-03：t=2、(2,1,1) 原 binary 省略排除](history/2026-10-03-excess-two-binary-two-unary.md)
- [2026-10-03：t=2、(2,1,1) 兩原 unary 省略排除](history/2026-10-03-excess-two-two-unary.md)
- [2026-10-02：t=2、(2,2) 原 binary 省略與同框第二核心排除](history/2026-10-02-excess-two-two-binary.md)
- [2026-10-02：t=3、(2,1) 原 binary 省略分支排除](history/2026-10-02-excess-two-binary-omission.md)
- [2026-10-02：三 spokes／三原 unary 共同扇區排除](history/2026-10-02-excess-two-three-unary.md)
- [2026-10-02：933／941 excess 進展整理與發布](history/2026-10-02-excess-progress-publish.md)
- [2026-10-02：ε=2 t=3 原 triangle 的 spoke＋unary 省略核心排除](history/2026-10-02-excess-two-three-spoke-unary.md)
- [2026-10-02：ε=2 t=2 的 spoke＋原 unary 省略核心排除](history/2026-10-02-excess-two-spoke-unary.md)
- [2026-10-02：ε=2 唯一 degree-6 root 的雙 spoke 省略核心排除](history/2026-10-02-excess-two-double-spoke.md)
- [2026-10-02：941 three-spoke 排除與共同 ε≥2 下界](history/2026-10-02-941-three-spoke.md)
- [2026-10-02：941 two-spoke 的原接點保持與來源排除](history/2026-10-02-941-two-spoke.md)

- [2026-10-02：C₅ 全線整合、可反駁假設與投影階數初驗](history/2026-10-02-c5-research-synthesis.md)

- [2026-10-02：941 single-spoke 的共同支援與來源排除](history/2026-10-02-941-single-spoke.md)

- [2026-10-02：四容量子覆蓋共享、933 的 ε≥2 與 941 殘餘](history/2026-10-02-excess-one-subcovers.md)
- [2026-10-02：933／941 的第一個 excess／容量／跨度下界](history/2026-10-02-independent-support-capacity.md)
- [2026-10-02：具名來源 J/P 與 W／C 的 Lean 實例](history/2026-10-02-lean-named-repair.md)

- [2026-10-02：D₁₃ 四接點及密封替換的 Lean 證明](history/2026-10-02-lean-sealed-four-port.md)
- [2026-10-02：共同 repair 判準的 Lean 形式化](history/2026-10-02-lean-common-repair.md)
- [2026-10-02：C₅ 共同 repair 與來源替換族發布核對](history/2026-10-02-c5-two-vertex-repair-publish.md)
- [2026-09-30：C₅ 輪環與偶長雙扇之外的十三點非對稱四接點 disk](history/2026-09-30-c5-two-vertex-repair-caps.md)
- [2026-09-30：C₅ 輪環逆化約之外的完整四接點偶長雙扇替換](history/2026-09-30-c5-two-vertex-repair-fans.md)
- [2026-09-30：C₅ 舊化約之外的完整四接點輪環替換](history/2026-09-30-c5-two-vertex-repair-rings.md)
- [2026-09-30：C₅ 不含舊核心的私有路徑奇偶定理](history/2026-09-30-c5-two-vertex-repair-strips.md)
- [2026-09-30：C₅ 不能逐點消去的密封 clique 補片](history/2026-09-30-c5-two-vertex-repair-patches.md)
- [2026-09-30：C₅ repair 來源充分條件](history/2026-09-30-c5-two-vertex-repair-sources.md)
- [2026-09-30：C₅ 共同 repair 充要 lemma](history/2026-09-30-c5-two-vertex-common-repair.md)
- [2026-09-30：C₅ 六例 local-repair transport audit](history/2026-09-30-c5-two-vertex-repair-transport.md)
- [2026-09-30：C₅ 全部 inclusion-minimal 四點修復](history/2026-09-30-c5-two-vertex-minimal-repairs.md)
- [2026-09-30：C₅ 兩點接合、混合框與最小修復發布整理](history/2026-09-30-c5-two-vertex-publish.md)
- [2026-09-30：C₅ 四點投影的最少個數與唯一組合](history/2026-09-30-c5-two-vertex-quaternary-repairs.md)
- [2026-09-30：C₅ 全部三點投影不足與四點 arity 下界](history/2026-09-30-c5-two-vertex-ternary-projections.md)
- [2026-09-30：C₅ 兩混合框共同拉回與跨框條件修復](history/2026-09-30-c5-two-vertex-mixed-pullback.md)
- [2026-09-30：C₅ 反向接合第二混合外框的完整 relation 核對](history/2026-09-30-c5-two-vertex-second-mixed-frame.md)
- [2026-09-30：C₅ 反向接合混合外框的完整 relation 核對](history/2026-09-30-c5-two-vertex-mixed-frame.md)
- [2026-09-30：C₅ 私有內點反向接合的具名拓撲核對](history/2026-09-30-c5-two-vertex-private-reverse-topology.md)
- [2026-09-30：C₅ 私有內點接合的平面與兩原框阻斷](history/2026-09-30-c5-two-vertex-private-topology.md)
- [2026-09-30：C₅ 兩點接合主例的原框與區域拓撲](history/2026-09-30-c5-two-vertex-topology.md)
- [2026-09-30：C₅ 具名八點接合與同代表整圖核對](history/2026-09-30-c5-two-vertex-join.md)
- [2026-09-30：C₅ class 兩點重疊資料與接手整理](history/2026-09-30-c5-two-vertex-overlap-handoff.md)
- [2026-09-30：mixed P₃ 中點／端點與保留原末端的六跨度排除](history/2026-09-30-mixed-p3-middle-endpoint.md)
- [2026-10-04：mixed 共鄰 P₃ 雙扇區、部分來源排除與具名殘留](history/2026-10-04-mixed-p3-common-endpoint.md)
- [2026-10-04：C₂ 一色支援三接點 unary、原 triangle 與 K₅ 外路](history/2026-10-04-mixed-p3-one-color-ternary-unary.md)
- [2026-10-04：C₃ 雙框點三接點 unary、新非接點葉與原 K₅](history/2026-10-04-mixed-p3-two-frame-ternary-unary.md)
- [2026-10-04：C₄ geometry34／join60、兩份原 unary 的完整 relation 排除](history/2026-10-04-mixed-p3-two-frame-two-unary.md)
- [2026-09-30：mixed P₃ 非對稱六跨度與兩端接線完成](history/2026-09-30-mixed-p3-asymmetric.md)
- [2026-09-29：mixed P₃ 對稱分支的原五環與側支援排除](history/2026-09-29-mixed-p3-symmetric.md)
- [2026-09-29：mixed 容量、十八側型與最小三點接線](history/2026-09-29-mixed-capacity-contacts.md)
- [2026-09-29：no-mixed 增長完備性與免表共同分離](history/2026-09-29-no-mixed-growth-completion.md)
- [2026-09-29：no-mixed 無增長短側弧與共同 singleton 排除](history/2026-09-29-no-mixed-no-growth.md)
- [2026-09-29：no-mixed 統一局部增長篩選與非守恆原端點](history/2026-09-29-no-mixed-local-screen.md)
- [2026-09-29：逐 root 不可搬運紙面界與精確接合介面](history/2026-09-29-no-mixed-root-transport.md)
- [2026-09-29：三 agent 驗證搬運、單框點與守恆 palettes](history/2026-09-29-no-mixed-hypothesis-audit.md)
- [2026-09-29：no-mixed 十五類整理與共同側跨度](history/2026-09-29-no-mixed-span-budget.md)

- [2026-09-29：D–E 排除與 no-mixed 全分類完成](history/2026-09-29-adjacent-no-mixed-de.md)

- [2026-09-29：D–D 四飽和原分量與統一框邊 K5](history/2026-09-29-adjacent-no-mixed-dd.md)

- [2026-09-29：C–E 五正跨度與原路徑來源排除](history/2026-09-29-adjacent-no-mixed-ce.md)

- [2026-09-29：C–D 三飽和原分量來源排除](history/2026-09-29-adjacent-no-mixed-cd.md)

- [2026-09-29：C–C 無 spoke 四分量來源排除](history/2026-09-29-adjacent-no-mixed-cc.md)

- [2026-09-29：B–D 雙飽和來源排除](history/2026-09-29-adjacent-no-mixed-bd.md)

- [2026-09-29：B–C 飽和原路徑與雙列分離](history/2026-09-29-adjacent-no-mixed-bc.md)

- [2026-09-29：E–E 六份正跨度來源排除](history/2026-09-29-adjacent-no-mixed-ee.md)

- [2026-09-29：B–E 五份正跨度與完整關係搬運](history/2026-09-29-adjacent-no-mixed-be.md)

- [2026-09-29：B–B 四分量支援、完整關係與 target 分離](history/2026-09-29-adjacent-no-mixed-bb.md)

- [2026-09-29：無 mixed (2,2) 重疊型全來源排除與五類覆蓋](history/2026-09-29-adjacent-no-mixed-t2-t0-overlap.md)

- [2026-09-29：No-mixed 五組成果、十四個 checker 與發布核對](history/2026-09-29-no-mixed-progress-publish.md)
- [2026-09-29：無 mixed t_w=0,(2,2) 缺額型的 340 份排除與 48 查詢全證](history/2026-09-29-adjacent-no-mixed-t2-t0-pairs.md)
- [2026-09-29：交換或幾何阻斷的 25 格範圍與完整路徑控制](history/2026-09-29-exchange-geometry-scope.md)
- [2026-09-29：t_z=2、t_w=0、(2,1,1) 四分量覆蓋與 240 查詢全證](history/2026-09-29-adjacent-no-mixed-t2-t0-singles.md)
- [2026-09-29：record 22 原雙端點、66 個新增延拓與整型出口](history/2026-09-29-adjacent-no-mixed-t2-t1-endpoints.md)
- [2026-09-29：record 14 原外部路徑、首橋與 52 個新增延拓](history/2026-09-29-adjacent-no-mixed-t2-t1-bridge.md)
- [2026-09-29：Root 預算與 no-mixed t_z=2、t_w=1 成果發布核對](history/2026-09-29-root-degree-excess-publish.md)
- [2026-09-29：Root degree 超額預算、樹引理與 136 份入口的支援覆蓋](history/2026-09-29-root-degree-excess.md)
- [2026-09-29：無 mixed 兩側 t=2 三輪成果整合發布](history/2026-09-29-adjacent-no-mixed-t2-publish.md)
- [2026-09-29：無 mixed 兩側 t=2 整條原路徑與最後四項完成](history/2026-09-29-adjacent-no-mixed-t2-path-palettes.md)
- [2026-09-29：無 mixed 兩側 t=2 原雙端點與 60 個新增延拓](history/2026-09-29-adjacent-no-mixed-t2-endpoints.md)
- [2026-09-29：無 mixed 兩側 t=2 原 bridge、固定框弧與 68 個新增延拓](history/2026-09-29-adjacent-no-mixed-t2-bridge.md)
- [2026-09-29：相鄰雙 degree-5 七輪成果整理與發布驗證](history/2026-09-29-adjacent-progress-publish.md)

- [2026-09-29：無 mixed 兩側 t=2 的實際支援、環序與 target 上界](history/2026-09-29-adjacent-no-mixed-t2.md)

- [2026-09-29：無 mixed 的同色 residual、容量與逐邊 minimality](history/2026-09-29-adjacent-no-mixed.md)
- [2026-09-29：唯一 mixed K2 四 incidence 型，原 K4 與實際外部路徑](history/2026-09-29-adjacent-mixed-edge-k4.md)
- [2026-09-29：唯一 mixed K2 同端點型，完整關係與原 v-star 來源排除](history/2026-09-29-adjacent-mixed-edge-same-endpoint.md)
- [2026-09-29：共鄰端點 K2 的 t_w=0、(1,1,1)，六跨度來源排除](history/2026-09-29-adjacent-mixed-edge-shared-t0-singles.md)
- [2026-09-29：共鄰端點 K2 的 t_w=0、(2,1)，原 diamond 路徑與雙列分離](history/2026-09-29-adjacent-mixed-edge-shared-t0-pair-single.md)
- [2026-09-29：共鄰端點 K2 的 t_w=1、(1,1)，飽和環序與雙列分離](history/2026-09-29-adjacent-mixed-edge-shared-t1-singles.md)
- [2026-09-28：相鄰雙 degree-5 九組成果整理與發布驗證](history/2026-09-28-adjacent-progress-publish.md)
- [2026-09-28：共鄰端點 K2 的 t_w=1、(2)，局部 K5 搬運與雙列分離](history/2026-09-28-adjacent-mixed-edge-shared-t1-pair.md)
- [2026-09-28：共鄰端點 K2 的 w 側兩條 spoke、實際支援與雙列分離](history/2026-09-28-adjacent-mixed-edge-shared-t2.md)
- [2026-09-28：唯一 mixed K2 共鄰端點的完整關係與逐邊 minimality](history/2026-09-28-adjacent-mixed-edge-shared.md)
- [2026-09-28：原四環外側次序排除唯一 mixed K2 各一接點型](history/2026-09-28-adjacent-mixed-edge-order.md)
- [2026-09-28：唯一 mixed 原 K2、各一接點的必要化約](history/2026-09-28-adjacent-mixed-edge.md)
- [2026-09-28：共鄰單點 34／40 來源排除與全部支援出口](history/2026-09-28-adjacent-singleton-end-arc.md)
- [2026-09-28：共鄰單點 12 長弧分離與出口擴充](history/2026-09-28-adjacent-singleton-middle-arc.md)
- [2026-09-28：共鄰單點 01／23 長弧分離與出口接合](history/2026-09-28-adjacent-singleton-long-arc.md)

- [2026-09-28：共鄰單點同側限制與 target 重色排除](history/2026-09-28-adjacent-singleton-sectors.md)

- [2026-09-28：相鄰雙 root 唯一共鄰單點化約](history/2026-09-28-adjacent-shared-singleton.md)
- [2026-09-28：相鄰雙 degree-5 有序色對介面與刪邊必要條件](history/2026-09-28-adjacent-degree5-interfaces.md)

- [2026-09-28：no-spoke 最後 12 查詢與唯一 degree-5 完成](history/2026-09-28-no-spoke-first-bridge.md)

- [2026-09-28：single-spoke／no-spoke 六組成果整理與發布驗證](history/2026-09-28-progress-publish.md)

- [2026-09-28：no-spoke 原外部路徑 K5 與 record 599 排除](history/2026-09-28-no-spoke-path-minor.md)
- [2026-09-28：no-spoke 環狀支援與 (2,1,1,1) 指定分離](history/2026-09-28-no-spoke-supports.md)
- [2026-09-28：no-spoke 外部連通與六型收窄為兩型](history/2026-09-28-no-spoke-exterior.md)

- [2026-09-28：single-spoke (4) 排除與全部 t=1 接合](history/2026-09-28-four-contact.md)

- [2026-09-28：single-spoke (3,1) 任意大小排除](history/2026-09-28-three-one.md)

- [2026-09-28：局部 residual、record 90 與 (2,2) 完成](history/2026-09-28-residual-locality.md)

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
