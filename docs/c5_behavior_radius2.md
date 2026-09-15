# 固定 predicate 的半徑 2 辨識實驗

2026-09-15。接續使用者對[第一輪](c5_behavior_refinement_results.md)的覆核。
一般兩步策略的來源 iff 已有紙面證明，尚未 Lean 化；它不是僅由 18 例支持的猜測。
本輪固定該 predicate，未增加觀察欄位或新圖。

## 問題與結果

是否存在非全域換色等價的兩個完整染色，在細化摘要下仍同桶，卻可由短 continuation 區分？

**同圖半徑 2 沒有提供候選：細化後 106 桶全部是單點。**
這不回答更大範圍的存在性，也不構成充分性或 closure 證據。

| 半徑 | 摘要 | 染色 | buckets | 同桶不同染色 pairs | 深度 ≤2 escape 衝突 |
|---|---|---:|---:|---:|---:|
| 1 | boundary + pairings + cycles | 18 | 15 | 3 | 3 |
| 1 | 基底 + 固定色框 ψ | 18 | 16 | 2 | 2 |
| 1 | 基底 + 實際色框 ψ | 18 | 18 | 0 | 0 |
| 2 | boundary + pairings + cycles | 106 | 100 | 6 | 6 |
| 2 | 基底 + 固定色框 ψ | 106 | 101 | 5 | 5 |
| 2 | 基底 + 實際色框 ψ | 106 | 106 | 0 | 0 |

半徑 1／2 分別保存 32／482 條長度不超過該半徑的合法歷史（含兩條空歷史）。
半徑 2 基底的 6 對各自最短 escape 區分深度都是 2，完整觀察可一步區分。
**6 對全部是原 (c,d) 的共同全域換色版本，只有一個 pair color orbit。**
沒有發現新的反例機制。各對內的兩個染色彼此都不是全域換色等價；
「一對內互為換色」與「整對是既有反例的共同換色」是兩個不同檢查。

半徑 1 剩餘兩對的完整 22 頂點比對也已寫成斷言：

- boundary `(A,C,B,A,D)`：同時對原 c、d 做 B↔C。
- boundary `(A,D,C,A,B)`：同時做 B↔D，排序後的兩側順序相反。

這是同一來源連通判準的色框泛化成功，並非另兩條獨立結構規則。

## 可重現範圍

[checker](../scripts/c5_behavior_radius2.py) 從既有證書兩起點列舉全部長度 ≤2
合法歷史，保留所有完整染色與到達歷史。沿用原 30-action boundary-root grammar，
對每個同桶染色對同步搜尋長度 ≤2 的 full／escape continuation，保存完整回放。
無 compatibility 剪枝；visited 只按完整染色對，不依摘要刪除狀態。

摘要的附加值只有 guarded ψ 的 `None/false/true`；實際色框和指定詞已由 raw
boundary 唯一決定。沒有把 component 或 induced vertex 集合偷偷加進分桶 key。
共同全域換色的 orbit key 僅作反例分類，固定所有頂點標號，不用於遍歷或 action
正規化，也沒有判定圖自同構下的機制等價。

[證書](../artifacts/c5_cells/behavior_radius2.json) 保存圖、grammar、corpus、
非單點桶、衝突、兩側回放、換色診斷與來源 SHA-256。

```bash
uv run --with networkx==3.5 python scripts/c5_behavior_refinement.py --check
uv run --with networkx==3.5 python scripts/c5_behavior_radius2.py --check
lake build
git diff --check
```

以上驗證通過。這是 Python 有界搜尋證據，沒有新增 Lean 定理。

## 策略規則與停止點

一般 iff 可先作完整染色上的策略規則：guard 成立且 ψ=false 時，執行按實際色框
實例化的兩步，保證 singleton-4；ψ=true 僅排除這條路線；guard 不成立則不適用。
計算仍需完整圖的 component 與誘導連通性，沒有執行加速或可丟棄完整染色的結論。

本輪停在半徑 2。下一個有辨識力的入口仍是先取得固定細化摘要的非單點桶，
再檢查非換色副本的短 continuation 衝突；單純提高染色數量不是充分性進展。
一般 iff 的 Lean 化是另一項明確可做的形式驗證工作。

後續依使用者指定改做 [cycle-count ablation／三步機制分析](c5_cycle_ablation.md)，
保持本輪 corpus 不變；已找到一般三步來源 iff 與單頂點橋接診斷。
