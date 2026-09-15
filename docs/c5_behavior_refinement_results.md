# Behavior refinement：第一輪固定圖實驗

2026-09-15。接續 [研究提案](c5_behavior_refinement.md) 與
[同 cut witness](c5_equal_cut_witness.md)。本輪是可重播 Python 有限證書與
一般引理的紙面證明，**沒有新增 Lean 定理**。

## 1. 實作範圍與語意

[checker](../scripts/c5_behavior_refinement.py) 固定 survivor-811 與既有 c、d。
顏色 A/B/C/D 固定為 0/1/2/3，根固定在 boundary 頂點 0..4。
action grammar 為六個無序色對乘五個根，共 30 個規則；根的當前色不在該色對
時記 `illegal`，否則重新計算該側的 maximal component。
這不包含完全不接 boundary 的 Kempe components。

同步 BFS 比較同一 action word 在兩側的結果，搜尋深度至 2。
完整觀察保存原色 boundary、三組 dual pairings、三組 cycle counts；escape
觀察只看目前是否 singleton-{1,3,4}，另把 illegal 記為不同值。
搜尋可穿過有一步 escape 的狀態，沒有 compatibility 剪枝。
visited 只用完整染色對，沒有依 observation 刪除 concrete states。
每條區分詞保存兩側完整中間染色、實際 component、結果，避免拼接不同 witnesses。

## 2. 原 witness 與最短區分詞

- 完整觀察：`AB@0` 可區分；最短深度 **1**。
- escape 觀察：`AB@0; BC@2` 可區分；最短深度 **2**。

最短性限上述 30-action grammar，由 BFS 檢查所有更短詞；不宣稱唯一最短詞。
證書同時保存指定詞與 BFS 首次找到的詞。

## 3. 一般 source predicate 的 iff（紙面證明）

設 G 為任意 proper 四染色圖，五個相異 boundary 頂點的顏色為
`(A,B,C,A,D)`，四個色標互異。令 K 是包含 0 的 maximal AB component，
**明確假設 `K ∩ boundary = {0,1}`**。令

```text
U = V_C ∪ (V_B \ K) ∪ (V_A ∩ K)
ψ(c) = [0 與 2 在 G[U] 連通].
```

則 `AB@0; BC@2` 的最終 boundary 是 singleton-4 **iff `¬ψ(c)`**。

證明：第一次交換後 B 色頂點恰為 `(V_B \ K) ∪ (V_A ∩ K)`，C 色頂點不變，
故 BC 誘導子圖恰為 G[U]。trace 假設給第一次交換後 boundary `(B,A,C,A,D)`。
其 BC 頂點只有 0、2。包含 2 的 component 若不含 0，第二次交換給
`(B,A,B,A,D)`，為 singleton-4；若包含 0，則給 `(C,A,B,A,D)`，仍使用四個色，
不為 singleton-4。兩次 rooted actions 都合法，maximal Kempe swap 保持 properness。
因此兩方向成立；不需要平面性、三角化或 survivor-811 的內部結構。

checker 從 source 集合 U 計算連通分量，再與直接 swap 的 BC 頂點集合及最終
singleton 比較。原 c、d 的 ψ 分別為 false、true。
一般 iff 尚未 Lean 化；已有 `Math/KempeSurgery.lean` 可提供 swap 的一般基礎。

## 4. 有界細化實驗

corpus 完整取 c、d 的半徑 **1** 鄰域（以上 boundary-root grammar，含起點），
共 **18** 個不同完整染色、**32** 條起點／一步歷史；重複到達同染色仍保存全部歷史。
沒有擴大圖 catalogue，也沒有枚舉整個 Kempe class。

| 觀察 | buckets | 同桶不同染色 pairs | 深度 ≤2 escape 衝突 |
|---|---:|---:|---:|
| 原色 boundary + pairings + cycles + 固定色框 ψ | 16 | 2 | 2 |
| 上述基底 + 隨實際 boundary 色框實例化的 ψ | 18 | 0 | 0 |

固定色框 ψ 僅在 2 個染色適用，其餘記 inapplicable，不能視為 false。
剩餘兩對的 boundary 分別為 `(A,C,B,A,D)` 與 `(A,D,C,A,B)`，區分詞為
`AC@0; BC@0` 與 `AB@0; AC@2`。它們均在原 ψ 適用範圍外；
因此不是指定色框 iff 的反例。

把 §3 的四個色標按當前 boundary `(a,b,c,a,d)` 實例化，並仍要求相同
boundary trace，可在 **9** 個染色上定義對應 predicate，也分開上述兩對。
原色 boundary 與 action labels 全程保留，沒有獨立正規化兩側的色框。

**18 buckets 恰好都是 singleton，所以零衝突是沒有剩餘比較對的結果，
不是 transition closure 或 future equivalence 的證據。** 本輪只建立有來源解釋
的細化操作，不能把它拿來合併一般染色或推論 K∞=K≤5。

## 5. 重現與下一步

```bash
uv run --with networkx==3.5 python scripts/c5_equal_cut_witness.py --check
uv run --with networkx==3.5 python scripts/c5_behavior_refinement.py --check
lake build
git diff --check
```

[證書](../artifacts/c5_cells/behavior_refinement.json) 保存圖、grammar、corpus
與歷史、兩類回放、兩組剩餘衝突、predicate 分量、來源與程式 SHA-256。
`--check` 重新執行有界搜尋與驗證並逐 byte 比對；不修改既有證書。

本輪驗證：上列兩個 checker、`lake build`（8819 jobs，僅既有 lint）、
新增文件的本地連結與 `git diff --check` 均通過；成果隨本輪提交。

下一個有價值的步驟：先 Lean 化 §3 的 boundary-trace iff；之後可在同圖半徑 2
corpus 尋找加入色框 predicate 後仍同桶的不同染色，再搜尋短區分詞。
半徑 2 corpus 尚未執行，沒有有限狀態充分性／最小性結論。
