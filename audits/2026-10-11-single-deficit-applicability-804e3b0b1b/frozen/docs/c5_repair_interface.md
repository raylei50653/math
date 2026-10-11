# Guard 修復：介面碰撞與 retained 分割

2026-09-15。接續 [來源修復報告 §3–6](c5_guard_repair.md#3-修復-guard-的來源集合更新公式)。
**紙面引理未 Lean 化；反例與統計只限既有固定三角化 disk 的完整閉包。**

## 1. 本輪結論

研究目標為一組從來源獨立讀取的共同介面關係
`I(c) ⇒ g(R(c)) ∧ Δχ≤0`。其中 R 是 BC@2 再共同對齊 B/C 色框。
已知 P 是來源充分條件，但仍分別要求成功側與成本側的精確資訊。

本輪排除一份具體候選資料：**完整 Q、boundary 與位置 2 鄰居的色角色、
同一 cut 每條原邊的 type**。即使保留原頂點／邊號與固定 embedding，這些資料
仍不足以區分 B₂ 已知安全修復與一個 χ 上升的來源。

另外給出 primal／dual 的 retained-port 分割壓縮引理，作為下一輪的精確基線。
這仍是兩側連通資料的組合，尚未解釋它們為何共同滿足安全條件，亦未證最小性。

## 2. 有界檢查範圍

只讀 `strategy_safe.json` 已有 5,952 個完整染色，不新增圖或重搜閉包。
取 boundary 能以共同色重命名寫成 `(A,D,C,A,B)` 的來源；只合併全染色相同
的共同色軌道，不獨立重命名系統或按摘要合併來源。

| 篩選或核驗 | 數量 |
|---|---:|
| 指定 boundary 色型來源 | 600 |
| 完整共同色軌道 | 25，每軌道 24 標號 |
| Q boundary trace 為 `{2,4}` 的軌道 | 19 |
| 上列中原 guard 失敗 | 13 |
| 候選介面資料類別（19 軌道） | 12 |
| 同介面且原 guard 失敗、修復觀測不同的類別 | 2 |
| 19 軌道中修復後 guard 成立 | 6 |
| 19 軌道中 guard 成立且 Δχ≤0 | 4 |

所有 19 個代表都以來源公式預測，再獨立實作 swap、重建 guard 與 dual cycles
核對。這次檢查範圍超過原 B₂ 的 3 個準備後色軌道，但仍完全在既有固定圖中。
沒有主張這 600 個來源都是 B₂ 的準備產物。

## 3. 關鍵碰撞：7 與 17

ID 綁定新證書記錄的 `strategy_safe.json` SHA-256。比較時使用完整共同角色框
`A/B/C/D=0/1/2/3`，不直接比較不同色框下的 cycle 欄位。

兩者 Q 都是 `{2,4,5,7,11,13,17,18}`，31 條 cut 原邊及其 type 逐項相同，
boundary 與位置 2 全部鄰居的色角色也相同：
`N_A(2)={3,14}`、`N_B(2)={13}`。只有頂點 8 的原來源色不同：

| 觀測 | 來源 7 | 來源 17 |
|---|---|---|
| 原來源 c(8) | C | B |
| 原 guard | 假 | 假 |
| 修復後 14 是否屬 S* | 是 | 否 |
| 位置 2 在 W* 的鄰居 | 空 | `{14}` |
| 修復後 guard | 真 | 真 |
| X 的 κ(old)→κ(new) | 4→5 | 4→6 |
| Y 的 κ(old)→κ(new) | 5→3 | 4→3 |
| 修復 Δχ | −1 | +1 |

來源 7 的完整角色染色正是原 B₂ 失敗修復的唯一色軌道。來源 17 是它在
頂點 8 做 singleton BC swap 得到的完整合法染色。頂點 8 不在 Q、不鄰接 2，
亦不接觸 cut；它的鄰居是 `{0,1,12,14}`，全用 A/D。

在來源 7，Q 外的 C 色頂點 8 對齊後成 B*，提供 retained primal 路徑
`0–8–14`。在來源 17，8 對齊後成 C*，此路徑退出 `G[V_A∪B*]`。
相應的 marked retained 分割由含 `{0,14}` 一塊改為兩塊 `{0}`、`{14}`。
來源 cut 本身看不到這個改動，dual 的 retained-owner 分割則同時改變。

**精確的排除結論。** 任意只依這份候選資料決定的 predicate，若接受來源 7，
就必須接受來源 17，因而不能保證 `g(R(c)) ∧ Δχ≤0`。這個反例也否定由這些
資料唯一決定隔離或成本。它沒有否定修復後 guard 的可決定性（本對兩者皆真），
沒有否定所有局部介面，也沒有否定加入其他來源限制後的引理。

另一個碰撞類是 `5381、5390`，兩者修復後 guard 都失敗，成本為 −2、+2。
完整資料留在證書；它們不是額外的 B₂ 成功例。

## 4. 精確來源介面的壓縮基線

### 4.1 Primal：只保存 marked retained 分割

令 `T=V_A∪B*`、`F=δ(Q)`、`H=G[T]−F`。標記集合 M 包含：

- root 0；
- `N_A(2)∪N_B(2)`；
- `F∩E(G[T])` 的全部端點。

上述鄰居均在 T：A 色不變，而所有 B 色鄰居均屬 Q，因此仍在 B*。
令 π 為 H 的連通分量在 M 上誘導的分割。以 π 的 blocks 為 vertices，
補回 `F∩E(G[T])` 的邊，則任意標記端點與 0 的連通性，恰等於它是否屬 S*。

**紙面證明。** 任一 G[T] 路徑可分為 H 中的片段與補回的 cut 邊；前者在
quotient 中收縮成點。反向可在各 H 分量內補回片段。沒有標記的 H 分量既不含
受詢端點，也不接補回的邊，刪去不影響查詢。這不需要平面性。

因此 π 加補回邊足以決定鄰居隔離式；只保存分割即可，不需保存分量內部的路徑。
這只決定較強隔離條件，不是修復後 guard 的完整充要介面。

### 4.2 Dual：無 cut port 的 owners 在差值中抵消

對 X、Y 分別令 P_F 為全部 cut dual edges 的端點。把 retained components
限制到 P_F，得到分割 π_X、π_Y。以這些 blocks 為 owners，按來源 cut types
分別補 old/new 邊，**兩邊都保留全部這些 port owners**。

若某 retained owner 不接觸任何 cut port，它在完整 old/new quotient 中均為
孤立點。因此刪除它在 κ(old)、κ(new) 中各減 1，Δκ 不變。於是

```text
Δχ = Δκ(port quotient X) + Δκ(port quotient Y)。
```

loops、parallel edges 與當側孤立的 port owners 仍須保留；不能只刪某一側的
isolates。此引理允許略去兩側共同的無 port owners，並未取消原成本公式的約定。
checker 同時計算完整 quotient 與 port quotient，驗證差值一致。

### 4.3 尚未得到共同機制

上述資料由來源抽取，不讀目標染色、目標 guard 或目標 cycle counts。
但 primal π 與 dual π_X、π_Y 仍各自抽取，沒有證明相互蘊含；ports 數目也沒有
跨圖固定上界。把它們合在一起只建立可檢驗的充分資訊基線。

下一輪應研究**跨 cut 的 retained 路徑如何約束兩側分割**，並要求候選共同
關係能區分 §3 的 singleton-8 改動。若只想描述 B₂ 的準備產物，也可以先證明
準備步為何強制這條路徑／相應分割，不能把來源 17 排除在資料之外就當作證明。

先證充分性，再以刪除資訊後的反例討論必要性；不直接宣稱最小資訊。
準備步的一般產生／保持定理、後續兩步的一般成本保證、一般 K=4 與
`K∞=K≤5` 仍未證。這一輪沒有新增 Lean 定理。

## 5. 重現與證據

- [checker](../scripts/c5_repair_interface.py)：來源抽取、分割重接、實際操作對照及碰撞核驗。
- [證書](../artifacts/c5_cells/repair_interface.json)：全部 19 個來源代表、原始 IDs、
  完整角色染色、候選介面、來源成本資料、port partitions 與來源 hashes。

```bash
uv run --with networkx==3.5 python scripts/c5_repair_interface.py --check
uv run --with networkx==3.5 python scripts/c5_guard_repair.py --check
uv run --with networkx==3.5 python scripts/c5_singleton_preparation.py --check
lake build
git diff --check
```

驗證：上述三個 checker 的 `--check` 與 `lake build`（8,819 jobs，僅既有 lint）
通過；`git diff --check`、新檔 whitespace 與文件連結檢查通過。文件、checker 與新證書隨本次提交發布。
