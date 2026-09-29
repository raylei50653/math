# Weak-deletion／單側與共同出口導覽

更新：2026-09-29。本頁整理既有成果，不新增研究結論。
研究線標記見 [HANDOFF](HANDOFF.md)，全文件索引見 [STATUS](STATUS.md)，
共通信任界線與工作約定見 [DOCUMENTATION](DOCUMENTATION.md)。

## 1. 目標與範圍

主命題 **`K∞=K≤5` 仍未證**。目前仍走 weak-deletion 候選 A 的
minimal obstruction 路線：先完成 single-sided exit 的可處理核心，再處理
一般／共同出口。唯一 degree-5 全部核心、唯一 mixed singleton、唯一 mixed K2
及 no-mixed 至少一側 t=2 的全部分拆、B–B 型已接回條件式出口；一般出口仍未證。

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
| No-mixed 至少一側 t=2 | 全部分拆及 root 交換型完成 | [重疊型收尾](c5_adjacent_degree5_no_mixed_t2_t0_overlap.md) |
| No-mixed B–B：兩側 t=1,(2,1) | 888 份必要支援的 1,776 個 target 全證；其餘兩側 t≤1 分拆保留 | [B–B 支援／環序及分離](c5_adjacent_degree5_no_mixed_bb.md) |
| 更一般 roots／出口 | degree≥6、多 degree-5、非樹／非相鄰 roots 與共同出口仍開放 | [Root 預算](c5_root_degree_excess.md)、[一般出口界線](c5_single_sided_exit.md) |

先讀候選與 minimal obstruction，再讀條件式出口的適用範圍，最後接到本線停止點。

## 3. 精確停止點與下一個窄問題

**本線精確停止點：B–B 已完成；下一窄入口 B–E。**
[B–B 支援／rotation 分類](c5_adjacent_degree5_no_mixed_bb.md) 逐 ID 綁定 236 份
原接合，兩個獨立算法給 2,520 份幾何及 888 份必要支援。92 份原資料有支援、
144 份纖維空。保留四原分量、六接點、兩 spokes、zw 與完整關係。
第一層接受 1,656／1,776；只對 120 個失敗候選再套原路徑／固定框弧（48）
及原雙端點（72），最終全部接受；888 份支援無新增來源排除。

下一步選 **B–E：t_z=1,(2,1)，t_w=0,(2,1,1)**，先處理沒有 source
飽和二禁色的這一格。新證書只綁定其 180 份 IDs／sides，尚未建立支援覆蓋
或遍歷 targets。首項 retained-join ID=2136、sides=(91,64)：

\[
B_z=\{0\},\quad B_w=\varnothing,\quad c=3,\qquad
(F_{C_z},F_{D_z})(q)=(\{1\},\{2\}),\quad
(F_{C_w},F_{D_w},F_{E_w})(q)=(\{0\},\{1\},\{2\}).
\]

保留五原分量、七具名接點、一條原 spoke、zw、actual supports、原 bridges、
旁支及共同色框。先證五份正跨度與 cyclic-order 必要覆蓋，再接合完整
binary schemas／unary relations；最後只對失敗候選套原路徑／固定框弧。
B–C、B–D 及其他兩側 t≤1 子類仍保留，不重開已完成的大枚舉。
Source 的 D+O+κ 預算不是 target 等式；必要支援及上界失敗不是 disk 反例。

### 可重用證明工具與界線

| 工具／機制 | 可安全使用的結論 | 主要入口 |
| --- | --- | --- |
| 完整關係搬運＋容量上界 | actual support 上存在共同色置換時精確搬運；否則只保留包含真實 F 的完整上界 | [t₂/t₁ 支援表](c5_adjacent_degree5_no_mixed_t2_t1.md) §4 |
| Root degree 超額預算 | source q 的 no-mixed minimal core 有 D+O+κ=degree−4；不是 target 等式 | [Root 預算](c5_root_degree_excess.md) §1–3 |
| 樹上 edge-minimal list obstruction | root 樹有 κ=0，lists 由 incident 邊色完整描述；不能把 source 邊色直接傳到 p | [Root 預算](c5_root_degree_excess.md) §4–5 |
| actual support／annulus 次序 | 保留原分量與具名接點後得到任意大小必要覆蓋；必要表不等於 disk 實現 | [t₂/t₁ 支援表](c5_adjacent_degree5_no_mixed_t2_t1.md) §2–3 |
| 原外部路徑＋固定框弧 minor | 可排除來源或使用 target 拒絕假設排除某候選；兩者必分開記錄 | [t₂/t₁ bridge](c5_adjacent_degree5_no_mixed_t2_t1_bridge.md) |
| 端點／bridge palette 相容性 | source/target 不全域守恆時，仍可利用同一原路徑端點 tightness 與完整 relation | [t₂/t₁ endpoints](c5_adjacent_degree5_no_mixed_t2_t1_endpoints.md) |
| 整份拒絕證書 palette 交換 | 幾何排除其他選擇後，可在同一原 C 上重建額外 source 禁色 | [t₂/t₂ path palettes](c5_adjacent_degree5_no_mixed_t2_path_palettes.md) |

目前已證的高階 source 結構是 [Root 預算](c5_root_degree_excess.md)：
D+O+κ=degree−4，以及樹骨架 κ=0。**尚未證**的是：
「交換或幾何阻斷」機制的一般完備性、no-mixed 雙 root 全分拆分離、
以及任意 degree-5 root 樹的跨列分離。

已關閉的主線家族：唯一 degree-5 全部分支；唯一 mixed singleton 全支援；
唯一 mixed K2 全接線；no-mixed 至少一側 t=2 的全部分拆，含整圖 root 交換；
t_w=0,(2,2) 缺額型已證雙列、重疊型由來源排除完成；B–B 型全雙列已證。
[範圍遍歷](c5_exchange_geometry_scope.md) 原 25 格／15 種交換型分類保持，
後續覆蓋為六類／1,172 份原接合，九類／2,376 份仍開放；1,920 份抽象
路徑控制不證一般機制完備性。B–B 以外兩側 t≤1 的分拆、degree≥6、多 degree-5、
非樹／非相鄰 roots、一般／共同出口均保留；前提及數字查各專題報告。
完整 Σ 的出口接合仍明用來源雙缺失及刪邊繼承。

證據層保持分開：紙面證明、外部 degree-list 定理、Python 固定域控制、
Lean 普通證明與 Lean `native_decide` 不互相代替。必要支援／minor skeleton
不是來源實現證書；固定 q 結論也不自動提升成完整 Σ。

## 4. 重播入口與驗證範圍

B–B 的當輪重播及省略範圍見 [研究紀錄](history/2026-09-29-adjacent-no-mixed-bb.md)。
以下其餘入口保留既有驗證範圍，不代表本輪全部重跑。
2026-09-29 重疊型的證書、驗證及停止點見 [當輪紀錄](history/2026-09-29-adjacent-no-mixed-t2-t0-overlap.md)。
舊 (2,2) 文件 SHA 差異及內容重播沿用 [缺額型紀錄](history/2026-09-29-adjacent-no-mixed-t2-t0-pairs.md)；最小入口：

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_bb.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t0_overlap.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t0_pairs.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t1_bridge.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
python3 scripts/c5_exchange_geometry_scope.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

雙拒絕 atlas 與 Lean axiom audit 另見 [分類報告](c5_two_rejection_proof_zh.md) 與 [Lean 工具](lean_two_rejection_tools.md)。
原重疊型研究輪未單獨重跑 t2 初層／interfaces、其餘 mixed／唯一 degree-5 完成表、雙拒絕 atlas、R 系列、profiles／閉包及 Lean axiom audit。
發布狀態以即時 Git 為準；歷史生成器可能覆寫 artifacts，勿把重建指令當只讀 checker。
早期交接見 [HANDOFF_HISTORY](HANDOFF_HISTORY.md) 與 [2026-09-22 快照](HANDOFF_2026-09-22.md)；歷史待辦與 Git 狀態均非現況。
