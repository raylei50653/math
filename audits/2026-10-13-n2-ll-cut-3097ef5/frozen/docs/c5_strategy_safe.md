# 策略受限相容模式：固定圖上的第一輪落地

2026-09-15。接續使用者「策略受限的子邊界相容模式」提案。
**計算證據**：固定 survivor-811、完整染色轉移閉包；未 Lean 化，沒有跨圖策略、
介面寬度或五內點代表定理。

## 1. 先固定三件事

- **目標**：沿用既有 escape，C5 boundary 恰用三色，唯一色位置在 `{1,3,4}`。
- **複雜度** `χ(c)`：三組 complementary dual systems 的 cycle counts **總和**。
  這是既有 [cycle 消融](c5_cycle_ablation.md) 的結構欄位，不是 primal Kempe
  components 數、顏色數、介面寬度，亦不是所有色對混成一份非交錯分割。
- **候選限制**：只換與 boundary 相交的 maximal component，再分成
  `χ≤K` 全程門檻，以及每一步 `χ(target)≤χ(source)` 兩種策略規則。

保留全部原色與頂點標號。狀態去重只用完整染色；同摘要不合併。
full 基準允許六色對的所有 maximal components，包括私有內部 components。
boundary-root 規則與既有 30-action grammar 有相同的後繼集合；同一 component
上的多個 roots 在表內共用一條邊，但 `boundary_roots` 保存全部合法標籤。
不按全域換色、圖自同構或 boundary 旋轉取商。

## 2. 閉包與證書方法

從 equal-cut 證書的兩個 source 出發，完整 BFS 得 **5,952 個染色、66,720 條
component-labeled 有向邊**；其中 47,616 條與 boundary 相交。
另外直接遍歷 boundary-root 邊，驗證從相同 seeds 可達的集合也恰是這 5,952 states。
所有狀態皆完整展開；不是將舊 radius 2 corpus 當作封閉系統。

對每種限制在目標集合做反向 BFS，保存：

1. `rank[s]`：最短受限成功距離；`None` 表示在這個完整有限系統中不可達。
2. `policy[s]`：一條合法、留在安全集合且 rank 恰下降一的邊。
3. 失敗證書：安全且 rank=None 的 states 不含 Goal，且對全部允許的安全邊封閉。

初始就超過門檻的狀態另計為不滿足初始化，不能混入「安全但失去成功」數字。
枚舉若超過 100,000 states，程式報錯並不寫入新證書；不輸出假不可達結果。

每個 state/pair 的 maximal components 用 NetworkX induced-subgraph components
獨立核對，swap 用另一份逐頂點公式核對，proper coloring 逐狀態檢查。
cycle counts 用 NetworkX dual components 重算；所有限制的距離也以 NetworkX
反圖 shortest paths 核對。幾何背景沿用來源 disk 證書，沒有新增拓撲定理。

## 3. 成功能力比較

| 初始集合 | 狀態數 | full Kempe 可成功 | boundary-root 可成功 | cycle 每步不增可成功 |
|---|---:|---:|---:|---:|
| 原兩個 seeds | 2 | 2 | 2 | 2 |
| 舊 radius 2 corpus | 106 | 106 | 106 | 96 |
| 完整閉包 | 5,952 | 5,952 | 5,952 | 3,168 |

**在此固定閉包，禁止 interior-only swaps 保留所有起點的成功能力。**
這不表示 interior components 不影響 maximal-component 判定，也不授權丟掉內部染色。

**cycle 總數每步不增不完備**：失去 2,784 個原本可成功的 states。
其中 2,280 個甚至不能維持「峰值不超過初始值」；另 504 個可以不超過初始峰值，
但仍不存在每步不增的成功路徑。因此「固定峰值」與「單調下降」確實不同。

| K | 閉包內初始 χ≤K | 存在全程 χ≤K 的 boundary-root 成功路徑 | 初始安全但失去成功 |
|---|---:|---:|---:|
| 1 | 336 | 0 | 336 |
| 2 | 1,416 | 480 | 936 |
| 3 | 3,912 | 2,664 | 1,248 |
| 4 | 5,112 | 5,112 | 0 |
| 5 | 5,832 | 5,832 | 0 |
| 6 | 5,952 | 5,952 | 0 |

所以本例有一個非平凡的有限策略不變集：`Q={χ≤4}`。
Q 的每個非目標 state 都有 boundary-root 操作留在 Q 並下降證書 rank。
它排除 840 個高 cycle 狀態，但仍涵蓋所有原本就在 Q 的起點。
舊 radius 2 中有 94 個起點在 Q，全部可於 Q 內成功；另外 12 個初始就不在 Q。
不能說 K=4 涵蓋全部 106 起點。K=6 則涵蓋整個閉包，沒有排除任何 state。

## 4. 最小必要峰值與具體反例

定義 `κ(c)=min_ρ max_{t∈ρ}χ(t)`，ρ 遍歷 boundary-root 有限成功路徑，含起終點。
逐一求全部 K 的安全勝集，得到每個 state 的 κ 及達到它的成功路徑。
在此閉包計算得到 `κ(c)≤max(χ(c),4)`；這不是跨圖常數 4 的證明。

下列 ID 是本證書 deterministic BFS 的索引；完整染色與 components 均在 JSON 中。
`A/B/C/D=0/1/2/3`，每一步 component 都在當時完整染色重新判定。

### 舊 radius 2 的 state 126：必須從 3 升到 4

```text
states: 126 → 14 → 122 → 630 (Goal)
χ:        3 →  4 →   4 →   3
actions: BD@3; BC@1; AB@2
```

`thresholds["3"].rank[126]=None`，而 `thresholds["4"].rank[126]=3`。
前者有完整安全補集封閉證書，後者有三步路徑；故 κ=4。
這不是只發現「某條路徑升高」，而是排除了所有峰值≤3 的成功路徑。

### state 247：不需要更高峰值，但不能要求每步不增

```text
states: 247 → 84 → 531 → 2026 → 4147 (Goal)
χ:        4 →  2 →   2 →    3 →    2
actions: AD@0; BC@1; AC@0; AB@1
```

κ=4，但 monotone rank=None；成功途中可以先下降再回升，仍不超過初始值。
這個完整閉包 witness 不屬於本輪擴張圖 catalogue；仍是同一張圖。

原兩個 seeds 的 κ 都是 3，分別有 `3→2→2→2` 與 `3→3→2` 路徑。
因此只測兩個 seeds 會錯過上述策略不完備性。

## 5. 和理論提案的接點／下一步

此輪先完成「限制後仍可成功」檢查與完整狀態策略抽取。
沒有增加摘要特徵，也没有檢查摘要桶的共同好操作或確定更新。
更沒有從單圖動態勝集推到靜態完整 Σ 覆蓋。

下一個有界入口：在 `χ≤4` 的已證書化安全成功路徑中，分析回升操作的
cut／retained-component 重接機制，尋找可以紙面證明的受控替換引理。
先解釋 state 126 的必要升高與 state 247 的回升，再問哪個結構條件允許改道；
不要直接把 cycle≤4 猜成所有圖的定理，也不自動擴展到新圖。

實作：[scripts/c5_strategy_safe.py](../scripts/c5_strategy_safe.py)。
證書：[strategy_safe.json](../artifacts/c5_cells/strategy_safe.json)，含完整圖、states、
transitions、全部 rank/policy、κ、witnesses、來源與 checker SHA-256。

```bash
uv run --with networkx==3.5 python scripts/c5_strategy_safe.py --check
lake build
git diff --check
```

`--check` 重算並逐 byte 比較；不帶參數才生成本輪證書。

本輪生成與獨立重播一致；`--check`、`lake build`（僅既有 lint）、文件連結及
`git diff --check` 通過。本輪與後續 [策略障礙分析](c5_strategy_barriers.md)
隨同一次交接提交；最新接手入口以 [HANDOFF](HANDOFF.md) 頂端為準。
