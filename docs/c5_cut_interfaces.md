# 固定 BC switch：同 source relation 的坍縮差異與 cut 接口

2026-09-15。接續 [多候選 edge-state](c5_edge_choices.md) §6。
**成果是固定圖的精確 Python 證書，加上一個一般圖連通性的紙面重建引理；未 Lean 化。**

## 1. 比較範圍與結果

固定同一 Errera disk、原色框架 `A=0,B=1,C=2,D=3`，只使用既有證書的
`one_switch_compatible` 與 `prefix_safe_two_switches`。
取與前輪坍縮 source 相同的**完整 boundary 染色** `(1,0,1,2,3)` 及
`T=(w,π12,π13,π23)`，得到 4 個不同完整 witnesses、10 條歷史。
所有歷史的起點及每個中間狀態都無一步禁止 singleton escape。
這是上述已保存階段的完整篩選，沒有宣稱涵蓋同圖所有染色。

固定 action 規則為 **交換當前 `Comp_BC(0)`**。這是同一選取規則，
各 witness 的 maximal component 頂點集合必須重新求出。
若嚴格指定前輪頂點集合 `{0,5,12,14}`，只有第一列合法；其餘三列明確拒絕。

四列 source 都有同樣的 cycle counts `(0,0,2)`：

| witness | 當前 BC component | cut 邊數 | 目標 cycles (αβ,αγ,βγ) | 目標 αγ pairing | 目標無一步 escape |
|---|---|---:|---|---|---|
| 0 | `{0,5,12,14}` | 14 | `(0,0,1)` | `(1,4),(2,3)` | 是 |
| 1 | `{0,5}` | 8 | `(0,0,1)` | `(1,4),(2,3)` | 是 |
| 2 | `{0}` | 4 | `(0,1,1)` | `(1,2),(3,4)` | 否 |
| 3 | `{0}` | 4 | `(0,1,1)` | `(1,2),(3,4)` | 否 |

每列 αβ system 都完整保留，目標 βγ pairing 都為 `(0,2)`。
βγ cycles **全部 2→1**，但後兩列同時新生 αγ cycle。
後兩列再交換 BD component `{2}`，立刻得到禁止的 singleton-1；
證書也列出其所有一步 escape（每列兩個）。

因此 `T+cycle counts` 不能決定這個 rooted BC 操作的目標相容性或完整 cycle 變化。
單看「βγ 少了一個 cycle」也不能判斷是否打破相容。
此處「相容」仍只指當前及一步內沒有 singleton-{1,3,4}，不是全 class invariant。
本組 cut 長度已能區分兩種結果，故本輪**沒有證明**下節接口是最小必要觀察量。

## 2. 一步 cut 接口：先切開，再保存連通分區

對指定合法 swap，令 `C=δ(S)`、`k=a xor b`。
每條 cut 邊的 type XOR k，其他邊不變。對任一 two-type system Q：

1. 從舊 Q **刪除所有 cut 邊**，取得 retained graph H。
2. 保存 H 的每個連通塊接觸哪些 cut ports、哪些 ordered boundary terminals。
   內部孤立頂點也要保存；沒有 ports／terminals 的完整舊 cycle 仍是一個獨立塊。
3. 保存 switch 後屬於 Q 的 cut 邊端點；按端點所屬的 retained blocks 重新接線。
4. 每個重接後連通塊的 boundary terminals 給出一個 pairing；無 terminals 者計為 cycle。

**紙面引理（指定一步的連通性）**：若 H 是刪除 cut 後保留的圖，A 是待加入的
cut 邊，將 H 的每個連通分量視為一個節點，再按 A 接線，所得圖的連通分量與
H∪A 的連通分量一一對應。證明：H∪A 的路徑可壓成分量間 walk；反向可用
H 各分量內的路徑連接相鄰 A 邊，抬回原圖。boundary terminal 標記隨此對應保留。
因合法染色在三角化 dual 上給出內點度數 2、有效 boundary terminals 度數 1，
目標分量必為 path 或 cycle，故上述標記足以恢復 pairing 與 cycle 數。

這裡是在 quotient 上計算**連通分量**，不是計算 quotient 的 graph cycle rank；
一個已完整保留的舊 cycle 即使被壓成孤立節點，也必須仍算一個 cycle。
不可先壓縮完整舊 system 再刪 cut：那會丟失切開同一舊 component 的分裂資訊。

實作 `interfaces` 從 source 與 action 建接口；`predict` 只讀 ports 的分區、
boundary terminal 標記與 added-edge endpoints，不讀染色或目標 systems。
原始 retained edges／vertices 另存為核查證據，並非 `predict` 的輸入需求。
這是對**已指定合法 action**的一步充分描述，沒有解決從壓縮 state 列舉全部合法
components、產生下一步接口，或將大小限制為不依賴內部圖的常數。

## 3. 證書與驗證

[checker](../scripts/c5_cut_interfaces.py)；
[證書](../artifacts/c5_cells/cut_interfaces.json)。

- `comparisons` 保存四個完整 source、全部原始歷史索引、實際 component、完整重接
  事件、一步 escapes、三組 cut 接口與預測。
- 每條歷史由既有 seeds 開始，逐步重驗 maximal component、完整染色及中間相容性。
- 既有全部 **196 個 transitions × 3 systems = 588 次**接口預測，與直接從目標染色
  重算的 dual systems 完全一致；完整 audit 的 deterministic hash 另存。
- 負控制：三個非法的舊 component 選取都拒絕；把真實接口的所有 retained blocks
  錯合成一塊會產生四 terminals 的非法分量，checker 能偵測此連通資訊損失。
- 證書包含來源與腳本 hashes；`--check` 重算後逐 byte 比對，沒有覆寫舊證書。

```bash
uv run --with networkx==3.5 python scripts/c5_cut_interfaces.py --check
uv run --with networkx==3.5 python scripts/c5_edge_choices.py --check
uv run --with networkx==3.5 python scripts/c5_edge_switches.py --check
uv run --with networkx==3.5 python scripts/c5_edge_incidence.py --check
uv run --with networkx==3.5 python scripts/c5_edge_states.py --check
lake build
git diff --check
```

上述五個 checkers、`lake build`、新增文件連結與 `git diff --check` 均通過；
Lean build 只有既有 lint 警告。

## 4. 下一個有界問題

在同一批 196 transitions 內，比較「只留 cut 長度／各舊 component 被切次數」與
「保留 cut ports 的連通分區」，找同一較粗觀察却有不同目標 pairing 的見證。
這能定位接口中哪種連通資訊不可省略；尚未執行，亦不等於建立多步充分 state。
本輪沒有新增圖 catalogue、Lean 定理或排除 C5 masks；K∞=K≤5 仍未證。
