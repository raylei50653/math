# C5 + C5 完整有限證書

`DOMAIN.json` 在 cap composition 開始前以 exclusive creation 凍結全部
132² 組有序 pair、外框／link／cap 次序、十列及 literal source manifest hash。
`certificate.json` 是完整證書；`generation.log` 是首次生成紀錄。

從 repo root 重播：

```sh
.venv/bin/python audits/2026-10-12-degree5-c5-c5-cap-dcdad039/controls/checker.py --check
.venv/bin/python audits/2026-10-12-degree5-c5-c5-cap-dcdad039/controls/checker.py --check --seed 17
```

需求為 Python 與 NetworkX；本輪環境 Python 3.14、NetworkX 3.5。
`--check` 只讀；import frozen reader 時也停用 bytecode 寫入。
`--seed` 只改 cap／pair 的驗證順序，輸出資料仍按凍結順序排列。
`--write` 只可建立尚不存在的目標，不能覆寫證書。

## 無損 full-lift 編碼

固定全域頂點次序為
`a,b,c,d,e,x,y,z,v,P:5,...,Q:5,...`；`P:5`、`Q:5` 是不同點。
每個 cap 保留原 literal edges、edge-id rotation、內面 darts，以及
`actual_boundary_order` 的全部 240 個 proper 四色指派。
`actual_boundary_full_private_fibres[i]` 列出該**實際色名指派**下的全部
private 頂點著色；包含空 fibres，不把各 cap 個別重新更名。

每個 pair 的十列都保留；列中的每個 `joint` block 是

```text
[X,Y,Z,V,P_assignment_index,Q_assignment_index]
```

其中 P 指派是 `(A,B,C,Y,Z)`，Q 指派是 `(A,X,C,D,E)`，且
`V` 異於 `A,X,C,Y,Z`。該 block 表示所指向 **完整** P private fibre
與 **完整** Q private fibre 的 Cartesian product。對每組 `(p,q)`，完整
整圖著色恰為

```text
[A,B,C,D,E,X,Y,Z,V] + p + q
```

因此不是單點／成對 marginals，也不是每列只存一份 witness。
`literal_full_witness` 是每個非空列額外存的一份完整著色；空列為 `null`。
checker 另用不讀 cap fibres 的 literal 整圖 MRV 回溯，逐列枚舉全部著色，
要求排序後與上述 product 的完整展開逐項相等，並排除重複。

## 嵌入與目錄索引

每個 cap 由 apex-planar embedding 取得以原 C5 為外面的 disk rotation。
把 cap 內面貼入固定九點 skeleton 的 P／Q 面，先建立帶 edge-id 的完整
multigraph rotation；同端點重複邊按 skeleton、P、Q 次序留第一條，從
rotation 刪去後一條的兩個 darts。`parallel_edge_simplifications` 保留兩條
原嵌入邊及其 owner，`edge_owners` 保留 simple 圖每條邊的 owner。
逐 pair 檢查 Euler 球面式、固定 B 外面、中心 L 次序、五個原三角面、
simple graph、連通及獨立 NetworkX planarity。

`catalogue_index` 是 `catalogue_order` 中從 0 開始的索引；`mask` 是原
十列關係識別。`k_eff` 直接來自凍結目錄 witness，沿用上游最少代表的
證據地位，這支 checker 沒有重新證明目錄完備性或任意大小圖的最小性。
每個 pair 都附輸出 `sigma`、`in_K` 及其 `representative`。

有限結果及通過狀態以主 `REPORT.md` 與重播 logs 為準；此證書未提供
933／941 或全域最小目錄外來源的實際圖，也未作 Lean 驗證。
