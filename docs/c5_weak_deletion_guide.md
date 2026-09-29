# Weak-deletion／單側與共同出口導覽

更新：2026-09-29。本頁整理既有成果，不新增研究結論。
研究線標記見 [HANDOFF](HANDOFF.md)，全文件索引見 [STATUS](STATUS.md)，
共通信任界線與工作約定見 [DOCUMENTATION](DOCUMENTATION.md)。

## 1. 目標與範圍

主命題 **`K∞=K≤5` 仍未證**。目前仍走 weak-deletion 候選 A 的
minimal obstruction 路線：先完成 single-sided exit 的可處理核心，再處理
一般／共同出口。唯一 degree-5 全部核心、唯一 mixed singleton、唯一 mixed K2
及 no-mixed 全部分拆均已由指定雙列分離或來源排除接回條件式出口；
一般出口仍未證。No-mixed 的統整與共同 source 結構見下列總覽。

## 2. 項目現況與閱讀順序

以下完成狀態均限於原報告前提；必要表不代表 disk 可實現性。

| 項目 | 現況／剩餘範圍 | 證據入口 |
| --- | --- | --- |
| Weak successors／候選 A、B、C | 固定域 audit 與同頂點 completion 已有；一般候選仍未證 | [候選](c5_weak_candidates.md)、[completion](c5_completion_weak_bisimulation.md) |
| Minimal obstruction 與出口 | 條件式接合已完成；一般單側與共同出口未證 | [三出口](c5_weak_critical_cores.md)、[單側出口](c5_single_sided_exit.md) |
| 全 degree-4 | 指定 disk／T4 前提下只缺 q；紙面＋外部定理＋證書 | [degree-4 導覽](c5_degree4_guide.md) |
| 唯一 degree-5 | 全部核心的指定雙列分離接回條件式出口；不是完整來源分類 | [單側出口](c5_single_sided_exit.md)、[R 系列的獨立缺口](c5_degree5_guide.md) |
| 相鄰雙 root／唯一 mixed singleton | 全部支援完成並接回出口 | [34／40 收尾](c5_adjacent_degree5_singleton_end_arc.md) |
| 相鄰雙 root／唯一 mixed K2 | 全部九組接線完成；區分雙列分離與來源排除 | [四 incidence 收尾](c5_adjacent_degree5_mixed_edge_k4.md) |
| No-mixed 全十五類 | 八類來源排除、七類雙列分離，原 3,548 接合全部覆蓋 | [十五類總覽與證據總表](c5_no_mixed_span_budget.md) |
| No-mixed 通用 source 結構 | m+s+a≤5；至少一條 root-spoke、無 source 重疊、至多一份飽和二禁色分量 | [側跨度紙面推導](c5_no_mixed_span_budget.md#2-從原圖導出框弧成本) |
| No-mixed 跨列分離 | 2,082 份必要支援的 4,164 target 全接受；既有局部篩選保留較強上界；後續已給免查表存在性證明 | [局部規則與覆蓋](c5_no_mixed_local_screen.md) |
| No-mixed 搬運與精確介面 | 紙面證成每 root 至多一份不可搬運分量，雙不可搬運只可能 AA/AB/AC；全部候選介面無損，守恆不升 pair 由後續免表證成，逐染色 repair 未構造 | [逐 root 界及獨立重播](c5_no_mixed_hypothesis_audit.md#31-逐-root-不可搬運界) |
| No-mixed 統一局部篩選 | 2,240 增長候選排除 2,208，32 份不影響 R；增長排除的免表完備性由後續三弧位置證成 | [增長、端點與全路徑交換](c5_no_mixed_local_screen.md) |
| No-mixed 無增長共同分離 | 短側弧與未見兩色交換不變性，免查表地排除同 singleton；7,848 joins 回歸通過 | [無增長紙面證明](c5_no_mixed_no_growth.md) |
| No-mixed 增長完備性／共同分離 | 三個側弧位置直接指定框弧，排除所有影響 R 的增長；指定 p₁、p₂ 存在性分離已免查表證成 | [增長完備性](c5_no_mixed_growth_completion.md) |
| 較大 mixed 容量／最小接點型 | 任意大小逐欄容量、unary 無重疊及缺額至多一，收成十八側型；各一 incidence 至多兩禁對；唯一 mixed 三點形完成必要接線控制，其餘幾何未完成 | [容量與三點介面](c5_mixed_capacity_contacts.md) |
| 唯一 mixed P₃ 對稱分支 | 兩端各一 incidence、兩側 E 同 pair 時，原五環空內側與五份實際支援排除全部 disk 來源；任意 unary 大小、不需 T4／Gallai | [原五環與完整側支援](c5_mixed_p3_symmetric.md) |
| 更一般 roots／出口 | degree≥6、多 degree-5、非樹／非相鄰 roots 與共同出口仍開放 | [Root 預算](c5_root_degree_excess.md)、[一般出口界線](c5_single_sided_exit.md) |

先讀候選與 minimal obstruction，再讀條件式出口的適用範圍，最後接到本線停止點。

## 3. 精確停止點與下一個窄問題

**本線精確停止點：no-mixed 指定 p₁、p₂ 已有免表共同存在性分離；
mixed 容量／三點接線化約之後，唯一 P₃ 兩端各一 incidence、兩側 E
同 pair 的對稱分支已作任意 unary 大小的 disk 來源排除。未 Lean 化。**

[Mixed 容量](c5_mixed_capacity_contacts.md)從完整關係證明：固定另一 root
顏色後，禁止本側顏色至多等於本側 incidences；source unary 禁色互不
重疊且缺額至多一，共十八必要側型。此容量部分容許多 mixed。
各一 incidence 的任意大 mixed 分量至多禁兩個有序色對；唯一 mixed 時，
新出現兩側 E 同為一個 pair、mixed 恰禁兩個非對角的分支。
固定 q 三點控制保留 P₃ 的 (1,1)／(1,2)／(2,1)，triangle 另留 (2,2)。
這些必要色角色不自動帶有實際支援或 disk 實現。
[P₃ 對稱分支](c5_mixed_p3_symmetric.md)現已證三個原 lists 相同、
原五環內側為空。兩份完整 root 側支援與三份星狀附件各有正跨度，
恰用完五條框邊；整側 E 的色置換不變性給矛盾。這是來源排除，
不是 target 接受；未把 P₃ 換成 shared singleton，未限制 unary 大小。

下一窄題是**唯一 mixed 原 P₃、兩端各接一 root 的非對稱 source
residual (|E_z|,|E_w|)=(1,2)，以及整份 root 交換型**。
保留原五環 z–x₀–x₁–x₂–w–z、實際 S₀/S₁/S₂、全部 unary 與原
外部路徑，先從完整 P₃ 關係導出必要附件及一色側跨度，再研究 p₁、p₂。
一色側沒有二元 residual 的正跨度引理，不能套用本輪五跨度等號。

[無增長](c5_no_mixed_no_growth.md)與[增長完備性](c5_no_mixed_growth_completion.md)
已關閉 no-mixed 有害增長缺口；不重啟十五類支援枚舉。
更大 mixed、多 mixed 的跨列／幾何、逐染色 repair、非相鄰 roots、多
degree-5、degree≥6 與一般／共同出口仍保留。
完整 Σ 的出口接合仍明用來源雙缺失與刪邊繼承。

### 可重用證明工具與界線

| 工具／機制 | 可安全使用的結論 | 主要入口 |
| --- | --- | --- |
| 完整關係搬運＋容量上界 | actual support 上存在共同色置換時精確搬運；否則只保留包含真實 F 的完整上界 | [t₂/t₁ 支援表](c5_adjacent_degree5_no_mixed_t2_t1.md) §4 |
| Root 色相容搬運／局部 preimages | H⊆G⊆E；全部可搬運時 G=E，必保留同一 target 色框 | [搬運引理](c5_no_mixed_hypothesis_audit.md#2-完整搬運的充分條件以及較弱版本) |
| 單框點精確化約 | 固定外部完整關係後至多兩份未知原分量；不刪外部幾何路徑 | [單框點介面](c5_no_mixed_hypothesis_audit.md#3-單框點化約與精確共同介面) |
| 逐 root 不可搬運界與 D_p 介面 | 各 root 至多一份未知 target 關係，雙不可搬運只可能 AA/AB/AC；不是固定一份 source 染色後的單分量 repair | [紙面界與精確搬運](c5_no_mixed_hypothesis_audit.md#31-逐-root-不可搬運界) |
| 禁色增長的共同局部篩選 | 守恆 palettes／非守恆原端點規則加 R 不相交條件；後續三弧位置補齊影響 R 的免表完備性 | [統一規則及界線](c5_no_mixed_local_screen.md#3-同一局部規則的兩個分支) |
| 無增長共同分離 | 短側弧 singleton 限為中間色或第四色；對側兩個未見色的交換不變性排除同 singleton | [短側引理與定理](c5_no_mixed_no_growth.md#4-三色-c5-的唯一單現點與無增長定理) |
| 增長完備性與共同分離 | 三弧位置固定配方排除有害增長，與無增長定理合成指定 p₁、p₂ 的存在性分離 | [位置引理及合成](c5_no_mixed_growth_completion.md#4-剩下的-pair-必不影響-r並完成共同分離) |
| Root degree 超額預算 | source q 的 no-mixed minimal core 有 D+O+κ=degree−4；不是 target 等式 | [Root 預算](c5_root_degree_excess.md) §1–3 |
| Mixed 容量與接點化約 | source unary 無重疊、D≤1；各一 incidence 至多兩禁對；三點控制不外推任意大小接線 | [Mixed 容量](c5_mixed_capacity_contacts.md) §2–6 |
| 完整 root 側支援不變性 | 原 E 為 pair 時，全部 unary／spokes 的實際支援聯集至少見兩色；P₃ 對稱分支五跨度排除，不替換原分量介面 | [P₃ 紙面排除](c5_mixed_p3_symmetric.md) §3–4 |
| 雙 root source 側跨度 | m+s+a≤5，八類來源排除；不能將成本未超額視為來源存在 | [十五類總覽](c5_no_mixed_span_budget.md) §2 |
| 樹上 edge-minimal list obstruction | root 樹有 κ=0，lists 由 incident 邊色完整描述；不能把 source 邊色直接傳到 p | [Root 預算](c5_root_degree_excess.md) §4–5 |
| actual support／annulus 次序 | 保留原分量與具名接點後得到任意大小必要覆蓋；必要表不等於 disk 實現 | [t₂/t₁ 支援表](c5_adjacent_degree5_no_mixed_t2_t1.md) §2–3 |
| 原外部路徑＋固定框弧 minor | 可排除來源或使用 target 拒絕假設排除某候選；兩者必分開記錄 | [t₂/t₁ bridge](c5_adjacent_degree5_no_mixed_t2_t1_bridge.md) |
| 端點／bridge palette 相容性 | source/target 不全域守恆時，仍可利用同一原路徑端點 tightness 與完整 relation | [t₂/t₁ endpoints](c5_adjacent_degree5_no_mixed_t2_t1_endpoints.md) |
| 整份拒絕證書 palette 交換 | 幾何排除其他選擇後，可在同一原 C 上重建額外 source 禁色 | [t₂/t₂ path palettes](c5_adjacent_degree5_no_mixed_t2_path_palettes.md) |

目前已證的高階 source 結構是 [Root 預算](c5_root_degree_excess.md)：
D+O+κ=degree−4，以及樹骨架 κ=0。**尚未證**的是：
超出本文 no-mixed 圖類的「交換或幾何阻斷」完備性，以及任意 degree-5 root 樹的跨列分離。
相鄰雙 degree-5 的 no-mixed 分拆已全部由雙列分離或來源排除涵蓋。

已關閉的主線家族：唯一 degree-5 全部分支、唯一 mixed singleton 全支援、
唯一 mixed K2 全接線，以及 no-mixed 十五類。原輪的分類、支援、具名
見證與當輪未決保持歷史語境，現況及數字統一由[新總覽](c5_no_mixed_span_budget.md)
連回各完成報告。一般化缺口不因有限表覆蓋完成而消失。

證據層保持分開：紙面證明、外部 degree-list 定理、Python 固定域控制、
Lean 普通證明與 Lean `native_decide` 不互相代替。必要支援／minor skeleton
不是來源實現證書；固定 q 結論也不自動提升成完整 Σ。

## 4. 重播入口與驗證範圍

最近 P₃ 對稱分支輪重跑新 checker（一般及 `PYTHONHASHSEED=17`）、
mixed 容量、完整有序色對介面、既有 Lean build 及文件／DocGraph；
確切命令與未重跑範圍見[P₃ 紀錄](history/2026-09-29-mixed-p3-symmetric.md)。最小入口：

```bash
python3 scripts/c5_mixed_p3_symmetric.py --check
PYTHONHASHSEED=17 python3 scripts/c5_mixed_p3_symmetric.py --check
python3 scripts/c5_mixed_capacity_contacts.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
```

先前增長完備性輪重跑新 checker（一般及 `PYTHONHASHSEED=17`）、前層
no-growth／local-screen／root-transport、文件／DocGraph 與既有 Lean build；
確切命令及未重跑範圍見[增長紀錄](history/2026-09-29-no-mixed-growth-completion.md)。最小入口：

```bash
python3 scripts/c5_no_mixed_growth_completion.py --check
PYTHONHASHSEED=17 python3 scripts/c5_no_mixed_growth_completion.py --check
python3 scripts/c5_no_mixed_no_growth.py --check
python3 scripts/c5_no_mixed_local_screen.py --check
python3 scripts/c5_no_mixed_root_transport.py --check
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

增長 checker 重播紙面指定框弧及原外路，不搜尋舊框弧規則；
無增長 checker 只用標準函式庫，獨立重建原共同側弧、候選域及短側
論證步驟；不讀舊接受 flags。局部 checker 重算全部增長候選，重用
既有支援穩定子、固定框弧及 minor 控制函式，不讀取舊 target 接受或
排除 flags 作判定。Root-transport
獨立核對搬運、側弧配置、候選域及三介面逐候選相等。十五類完整
重播屬[前輪跨度整理](history/2026-09-29-no-mixed-span-budget.md)，不是
最近增長完備性輪重跑。舊 (2,2) 文件 SHA 差異及內容重播見
[缺額型紀錄](history/2026-09-29-adjacent-no-mixed-t2-t0-pairs.md)。

雙拒絕 atlas 與 Lean axiom audit 另見 [分類報告](c5_two_rejection_proof_zh.md) 與 [Lean 工具](lean_two_rejection_tools.md)。
原重疊型研究輪未單獨重跑 t2 初層／interfaces、其餘 mixed／唯一 degree-5 完成表、雙拒絕 atlas、R 系列、profiles／閉包及 Lean axiom audit。
發布狀態以即時 Git 為準；歷史生成器可能覆寫 artifacts，勿把重建指令當只讀 checker。
早期交接見 [HANDOFF_HISTORY](HANDOFF_HISTORY.md) 與 [2026-09-22 快照](HANDOFF_2026-09-22.md)；歷史待辦與 Git 狀態均非現況。
