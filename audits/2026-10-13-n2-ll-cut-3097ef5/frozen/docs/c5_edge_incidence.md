# C5 joint incidence 壓縮：固定 corpus 的不足見證

2026-09-15。補齊 edge-state 表示實驗的交接紀錄；主接手入口為
[多候選 edge-state](c5_edge_choices.md)，本報告解釋為何仍保留完整 witnesses。

## 觀察量與範圍

沿用 `edge_states.json` 的 199 個三角化 disk 實例，共 11,351 個染色 representatives；
沒有生成新圖。三個候選觀察量都包含 boundary word、各 system 的 terminal pairings
及 cycle 個數，再依序保存：

- `edge_support`：不同 systems 的 components 是否共享邊。
- `edge_counts`：共享邊的數量。
- `face_counts`：共享邊數，再加三個 systems 的 component triples 共用三角面的數量。

paths 依 ordered terminal pair 命名；cycles 的名稱用**共同置換**在所有矩陣／張量中
一起 canonicalize，不能各個矩陣獨立改名。checker 另核對 face marginal 與
shared-edge counts 的恆等式：內部邊計兩次、boundary 邊計一次。

## 結果

三者都能區分原 Errera 的 `same_class_regression`，但仍不足以精確決定後繼。

| 候選觀察量 | distance collision 圖實例 | successor collision 圖實例 | 起點無一步 escape 的 successor collision 圖實例 |
|---|---:|---:|---:|
| edge_support | 1 | 7 | 2 |
| edge_counts | 0 | 122 | 122 |
| face_counts | 0 | 122 | 122 |

各欄比較的是同圖、同候選 source state；successors 使用**該候選本身**的 target state，
保留共同原色框架，但忽略 action 名稱。候選越精細，target 的差異也越可能被讀出，
所以這裡 collision 圖數不必隨精細程度遞減。

`edge_support` 的 distance 見證在 survivor-811：同 state 的最短 escape 距離 4、3。
`edge_counts`／`face_counts` 的安全起點 successor 見證在 errera-0：距離同為 2、2，
但後繼集合不同。沒有 distance collision 不代表後繼充分，更不是一般充分性定理。
這些 witnesses 的圖、定向面、完整染色與獨立有標號 escape routes 均保存在證書。
本報告不額外主張全部 collision pairs 都已驗證同一 Kempe class。

## 重播與接續

```bash
uv run --with networkx==3.5 python scripts/c5_edge_incidence.py --check
```

[checker](../scripts/c5_edge_incidence.py)／[證書](../artifacts/c5_cells/edge_incidence.json)。
它們與 switch traces、多候選 API 一起整理提交。結果屬固定 corpus 的精確 Python
驗證，沒有 Lean 定理、一般最小性或新 relation 排除。

下一輪不必重做這三種壓縮的第一輪篩查。若沿局部 BC 結構坍縮研究，先讀
[c5_edge_choices.md §4–6](c5_edge_choices.md#4-結構坍縮局部-bc-switch-消掉一個-cycle兩端仍相容)，
並用保留完整 witnesses 的 `Choice` 操作，避免丟失同 state 下不同的實際後繼。
