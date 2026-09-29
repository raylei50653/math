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
| No-mixed 跨列分離 | 2,082 份保留必要支援的 4,164 target 全接受；尚無取代七類證書的共同機制證明 | [完整關係及通用化界線](c5_no_mixed_span_budget.md#4-通用結構的兩層及尚未統一的部分) |
| 更一般 roots／出口 | degree≥6、多 degree-5、非樹／非相鄰 roots 與共同出口仍開放 | [Root 預算](c5_root_degree_excess.md)、[一般出口界線](c5_single_sided_exit.md) |

先讀候選與 minimal obstruction，再讀條件式出口的適用範圍，最後接到本線停止點。

## 3. 精確停止點與下一個窄問題

**本線精確停止點：no-mixed 全分類及 source 側跨度整理完成。**
[總覽](c5_no_mixed_span_budget.md)將十五類分成八類來源排除、七類雙列分離，
並給 source 必要式 m+s+a≤5；A/B/C/D/E 側成本為 2/2/3/4/3。
原 3,548 IDs 全覆蓋；5,842 份必要支援不是來源圖，4,164 次原 target
接受不記成本輪新增。此條件不保證 disk 實現，也不取代跨列證書。

若要繼續**整理通用證明**，窄問題是將七類的 target 論證統一到「每側
一缺額、至多一份 source 飽和分量」的完整關係介面；以 AA 的最後四項
全路徑 palette 交換及 AB 的非守恆色端點作控制，未證一般機制完備性。

若要**擴大圖類**，原下一入口仍是相鄰雙 degree-5 的較大 mixed 原分量：
先由[完整有序色對介面](c5_adjacent_degree5_interfaces.md)核對超出
singleton／K2 的必要接點與 minimality 條件，尚未建立其支援表。
多 mixed、非相鄰 roots、多 degree-5、degree≥6 與一般／共同出口仍保留。
完整 Σ 的出口接合仍明用來源雙缺失與刪邊繼承。

### 可重用證明工具與界線

| 工具／機制 | 可安全使用的結論 | 主要入口 |
| --- | --- | --- |
| 完整關係搬運＋容量上界 | actual support 上存在共同色置換時精確搬運；否則只保留包含真實 F 的完整上界 | [t₂/t₁ 支援表](c5_adjacent_degree5_no_mixed_t2_t1.md) §4 |
| Root degree 超額預算 | source q 的 no-mixed minimal core 有 D+O+κ=degree−4；不是 target 等式 | [Root 預算](c5_root_degree_excess.md) §1–3 |
| 雙 root source 側跨度 | m+s+a≤5，八類來源排除；不能將成本未超額視為來源存在 | [十五類總覽](c5_no_mixed_span_budget.md) §2 |
| 樹上 edge-minimal list obstruction | root 樹有 κ=0，lists 由 incident 邊色完整描述；不能把 source 邊色直接傳到 p | [Root 預算](c5_root_degree_excess.md) §4–5 |
| actual support／annulus 次序 | 保留原分量與具名接點後得到任意大小必要覆蓋；必要表不等於 disk 實現 | [t₂/t₁ 支援表](c5_adjacent_degree5_no_mixed_t2_t1.md) §2–3 |
| 原外部路徑＋固定框弧 minor | 可排除來源或使用 target 拒絕假設排除某候選；兩者必分開記錄 | [t₂/t₁ bridge](c5_adjacent_degree5_no_mixed_t2_t1_bridge.md) |
| 端點／bridge palette 相容性 | source/target 不全域守恆時，仍可利用同一原路徑端點 tightness 與完整 relation | [t₂/t₁ endpoints](c5_adjacent_degree5_no_mixed_t2_t1_endpoints.md) |
| 整份拒絕證書 palette 交換 | 幾何排除其他選擇後，可在同一原 C 上重建額外 source 禁色 | [t₂/t₂ path palettes](c5_adjacent_degree5_no_mixed_t2_path_palettes.md) |

目前已證的高階 source 結構是 [Root 預算](c5_root_degree_excess.md)：
D+O+κ=degree−4，以及樹骨架 κ=0。**尚未證**的是：
「交換或幾何阻斷」機制的一般完備性，以及任意 degree-5 root 樹的跨列分離。
相鄰雙 degree-5 的 no-mixed 分拆已全部由雙列分離或來源排除涵蓋。

已關閉的主線家族：唯一 degree-5 全部分支、唯一 mixed singleton 全支援、
唯一 mixed K2 全接線，以及 no-mixed 十五類。原輪的分類、支援、具名
見證與當輪未決保持歷史語境，現況及數字統一由[新總覽](c5_no_mixed_span_budget.md)
連回各完成報告。一般化缺口不因有限表覆蓋完成而消失。

證據層保持分開：紙面證明、外部 degree-list 定理、Python 固定域控制、
Lean 普通證明與 Lean `native_decide` 不互相代替。必要支援／minor skeleton
不是來源實現證書；固定 q 結論也不自動提升成完整 Σ。

## 4. 重播入口與驗證範圍

本輪重跑十五類完成 checker、no-mixed 化約、root 預算、新總覽 checker
及既有 Lean build；確切命令與未重跑範圍見
[整理驗證紀錄](history/2026-09-29-no-mixed-span-budget.md)。最小重播入口：

```bash
python3 scripts/c5_no_mixed_span_budget.py --check
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 checker 讀取原證書，核對逐 ID 覆蓋、側弧配置、框邊飽和 minor 與
原 target 最終狀態；不代替十五份完成 checker，也不把 snapshot 狀態當
本輪新 target 定理。舊 (2,2) 文件 SHA 差異及內容重播見
[缺額型紀錄](history/2026-09-29-adjacent-no-mixed-t2-t0-pairs.md)。

雙拒絕 atlas 與 Lean axiom audit 另見 [分類報告](c5_two_rejection_proof_zh.md) 與 [Lean 工具](lean_two_rejection_tools.md)。
原重疊型研究輪未單獨重跑 t2 初層／interfaces、其餘 mixed／唯一 degree-5 完成表、雙拒絕 atlas、R 系列、profiles／閉包及 Lean axiom audit。
發布狀態以即時 Git 為準；歷史生成器可能覆寫 artifacts，勿把重建指令當只讀 checker。
早期交接見 [HANDOFF_HISTORY](HANDOFF_HISTORY.md) 與 [2026-09-22 快照](HANDOFF_2026-09-22.md)；歷史待辦與 Git 狀態均非現況。
