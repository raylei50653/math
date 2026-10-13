# Cut 粗觀察：固定 196 transitions 的完整比較

2026-09-15。接續 [cut 接口報告](c5_cut_interfaces.md) §4。
**精確 Python 有限重播，未新增 Lean 定理。**

## 1. 問題與結果

原問題是：只留 cut 長度或各舊 component 被切次數，能否找到相同觀察、
不同目標 pairing 的反例？本輪完整檢查既有 `edge_choices.json` 的 196 條
transitions，**沒有找到這種反例**；cut 長度在這批資料中已能消除所有後繼衝突。
沒有擴大圖、染色或 action 搜尋範圍。

共同基底 `B=(原色 boundary, T, 三組 cycle counts, 交換色對)`。
顏色與 boundary terminal 標號固定，未對不同 witnesses 各自重命名。
目標比較同時包含原色 boundary、T、三組 cycle counts、一步相容性。

| 觀察 | 分組數 | 含多條 transitions | 含不同 source 染色 | 目標衝突組 |
|---|---:|---:|---:|---:|
| B | 78 | 54 | 30 | 44 |
| B + cut 長度 | 150 | 34 | 34 | 0 |
| 再加各舊 component 的切邊數 | 180 | 14 | 14 | 0 |
| 再加各舊 component 的原邊數 | 186 | 10 | 10 | 0 |

切邊數指 `|E(component) ∩ cut|`，不是沿曲線的連續切割段數。
Path 以其兩個 boundary terminals 識別；cycles 保存為排序後的多重集，
不假設不同 witnesses 的第 i 個 cycle 有共同身分。
第三列記 `(terminals, 切邊數)`；第四列記 `(terminals, 原邊數, 切邊數)`。

零衝突不是只因所有輸入各自唯一：cut 長度層的 34 個重複組全部含不同 source。
但它仍只證明：**這張有限 transition 表上的目標函數可經由該觀察分解**。
沒有證明同圖其他合法 transitions 或一般 disk 也如此。

## 2. Cut 長度確實區分了一個 rooted switch 衝突

證書 `pairing_witness=[2,12]` 指向原 transition table 的零起算索引。
兩個不同完整染色具有同 B，且都交換當前 `Comp_AC(0)`。
兩者目標原色 boundary 也相同，因此差異不只是全域換色或 boundary 改色。

| transition | AC component | cut 長度 | 目標 αβ pairing | 目標 cycles | 目標無一步 escape |
|---|---|---:|---|---|---|
| 2 | `{0,5}` | 8 | `(1,4),(2,3)` | `(0,0,1)` | 是 |
| 12 | `{0}` | 4 | `(1,2),(3,4)` | `(1,0,1)` | 否 |

三組 cycles 的順序為 `(αβ,αγ,βγ)`；兩列其餘 pairings 相同。
此見證說明 B 對這個 rooted 選取規則不足，cut 長度能分開這一對；
不宣稱 cut 長度是唯一可用或最小的補充資訊。
表中 44 個衝突組允許同色對的不同 component，不能全部解讀為同 rooted action
的反例；上面另行挑出的這一對才滿足同 rooted rule。

## 3. 重播與信任範圍

[checker](../scripts/c5_cut_observations.py)；
[完整證書](../artifacts/c5_cells/cut_observations.json)。
每條 transition 重驗完整 proper coloring、maximal component、cut 邊集合與實際
target；588 組 system 的 cut 接口預測逐項對照 target 直接重算。
證書保存所有觀察分組、每個不同目標及其 transition 索引、完整染色、
原表索引、接口預測與來源／實作 hashes。`--check` 重算後逐 byte 比較。

```bash
uv run --with networkx==3.5 python scripts/c5_cut_observations.py --check
uv run --with networkx==3.5 python scripts/c5_cut_interfaces.py --check
lake build
git diff --check
```

上述 checks 與新報告連結檢查通過；`lake build` 僅既有 lint 警告。

## 4. 下一步

本批資料不足以證明 ports 分區不可省略，也不足以證明 cut 長度普遍充分。
有價值的下一步是針對一般 cut 重接構造紙面歧義：同舊 pairing／cycle counts、
同切邊數，卻有不同 retained-port 分區與目標 pairing。
先區分「抽象接口可重接」與「同一合法三角化 disk 的染色／Kempe action 可實現」；
只有後者才能反駁本研究的圖上充分性猜想。仍未建立多步充分 state 或常數大小界，
K∞=K≤5 未證。本輪未啟動新 catalogue、polygon grammar 或 safety game。
