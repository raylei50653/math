# 跨邊完整 fibres：固定有限控制

此目錄只處理五個指定的 literal disk 圖；沒有搜尋或實現 933／941 的全域最小來源。
`check_cross_edge.py` 使用 Python 標準庫直接枚舉具名四色完整染色；不匯入舊 checker，
不使用分量各自正規化，也不把不同完整 lifts 的投影做笛卡兒拼接。

## 固定域與證書契約

外框固定為 `B=(0,1,2,3,4)`，顏色為 `(0,1,2,3)`。十列為所有 proper C5
染色的 whole-boundary restricted-growth representatives，依字典序排列；證書明列
`beta_domain`。任何整數 mask 都只按此明列次序解讀。

五圖為 `outer_w5`、`prism`、`triangulated_00`、`triangulated_01`、
`triangulated_03`。第一圖的 rim 就是 B、中心為 5；其他圖的 primary rim 為
`U=(5,6,7,8,9)`、中心為 10。`prism` 含 B 與 U 兩個 C5、五條對應接線及五條
中心 spokes。三個 triangulated 圖在第 i 個 annular 四面
`(B_i,B_(i+1),U_(i+1),U_i)` 加入一條對角線：mask bit i 為 1 時加
`B_i U_(i+1)`，否則加 `B_(i+1) U_i`。

每圖保留原圖 G、每個 degree-five 內點 v 的 H=G−v、各個 G−e 的 literal
edges、完整 oriented faces 及 rotation。checker 驗證每個 dart 出現一次、每個
vertex link 是單一 cycle、連通及 Euler characteristic 2；刪除指定 outer
face 得到 disk embedding。每個 rim 均另驗為 induced C5。所有 degree-five
內點均處理，包括 rim 碰到原 B 的其他中心。

`graphs[g].edge_fibres[e].rows[p].cells` 固定有四格 `(00,01,10,11)`，每格
列出該原圖 G−e 的全部完整 lifts，空格明列 `[]`。相鄰中心的共同 edge 只存
一份，先核對兩個 wheel 重建出的 literal 完整列表相等，再建立
`J_edge_fibre_indices_in_spoke_order` 引用。所有 G−e full vectors 使用
`g_vertices` 次序；每個 wheel 的 H vectors 使用該 wheel 的 `h_vertices`
次序，不能因其他中心的刪點位置不同而直接比較 vector。

每個 H lift 另保存六個二色 induced-component 的完整分割、所有不碰原 B 的
單分量 Kempe switches 及 switched full H lifts。`all_row_T_parts` 是三色
rim 且唯一 singleton 位置為 i 的完整 H lifts。`rejected_row_partition`
保留拒絕列全部五個 `R00`／`R01` fibres，包括空 fibres。

## 有限結果

| 數量 | 值 |
| --- | ---: |
| 指定原圖 | 5 |
| degree-five 內點／wheel | 16 |
| 去重後原邊 J 表 | 61 |
| 相鄰 degree-five 中心的共同原邊 | 19 |
| 十列四格 J cells | 2440 |
| 空 J cells | 1063 |
| 完整 G−e lifts，按去重 edge 表累計 | 4894 |
| 完整 H lifts，按 wheel 累計 | 1253 |
| 完整 G lifts，按原圖累計 | 403 |
| H 非空的 rejected wheel/row instances | 16 |
| 上述 rejected H lifts | 32 |
| 保存的二色 component partitions | 7518 |

所有 rows 的 J 都由 direct DFS 獨立驗證，又由共同 H full lift 加中心色重建。
逐 lift 驗證三色／四色 rim 的 J00/J01 incidence；逐 wheel/row 驗證

`res J_i01 = A_(i+2) ⊔ A_(i+3) ⊔ T_i`，

其中 `A_i=res J_i00`，所有集合都在同一個 H full-fibre 中。並驗證

`sum_i (|J_i01| − 2|J_i00|) = |C_G(p)|`。

同一來源所有 degree-five 中心相加、共同 edge 去重後，另驗證

`sum_e m5(e)(|J_e01| − 2|J_e00|) = n5 |C_G(p)|`。

`triangulated_00` 具有六個 degree-five 內點 `5,6,7,8,9,10`、其中十條相鄰
中心邊；此圖的全部十列均可延伸。它是多中心共邊恆等式的非空控制，沒有達到
933／941 的九／八個 degree-five 內點前提。

## 完整負控制：同一拒絕列的獨立 00 witnesses 不能合併

使用 `triangulated_03`，B、U、v 如上。全部 oriented faces 是：

```text
(4,3,2,1,0)
(0,1,6) (0,6,5) (1,2,7) (1,7,6) (2,3,7)
(3,8,7) (3,4,8) (4,9,8) (4,0,9) (0,5,9)
(10,5,6) (10,6,7) (10,7,8) (10,8,9) (10,9,5)
```

這是六內點 near-triangulated disk，具有全內部 induced W5。在同一拒絕列
`p=01212`，H 的全部完整 lifts 恰為下表；表中 B 均為固定的 `01212`，已
沒有其他 H 頂點。

| U 色列 | 唯一 J00 spoke i | 同 H lift 的兩個 J01 spokes |
| --- | ---: | --- |
| 12303 | 3 | 0,1 |
| 23031 | 2 | 0,4 |
| 32031 | 4 | 1,2 |
| 32301 | 1 | 3,4 |

所以五個完整 R00 fibres 的大小為 `(0,1,1,1,1)`。例如 spoke 1 的唯一
00 lift 是 `(01212,32301,2)`，spoke 2 的唯一 00 lift 是
`(01212,23031,0)`；二者的 H restrictions 不同，交集為空。四條邊各自
存在拒絕列 00 witness，不能推出任何兩條邊的 00 witnesses 共享 H。

反過來，第一個 H lift 確有同步的 mixed-cell triple：中心分別填
`0,1,2`，在 spokes `3,0,1` 得到 `00,01,01`。三者共享整個 H，卻是三份
不同的 full G−e coloring。證書保留三份全部頂點的色列，未把它們認成同一
full coloring。

在 H 色列 `(01212,12303)` 中，singleton vertices 5 與 8 的 colors 為
1、0；兩者不在同一個 0/1 component，但兩個 components 都碰原 B。因此
「不連通就可固定 B 作交換」也是錯誤推論。32 份拒絕 H lifts 的兩對
nonadjacent singleton pairs 均滿足 connected 或兩個 components 都碰 B。

另有以下具名負控制：

* `outer_w5` 的五條 spokes 分別只在 `01231,01023,01213,01232,01203`
  這五個不同拒絕列出現 00 witness，故逐邊存在性不能先交換量詞為共同列。
  此控制的 rim 是外框，全內部 W5 前提為 `not triggered`。
* `prism` 的合法 H lift `(01012,10103)` 若只把 U 獨立正規化為
  `01012`，所得 `(01012,01012)` 違反具名附件邊。證書列出全部違反邊及空
  destination fibre。

正控制：`prism`、`p=01012`、H lift `(01012,10123)` 中，0/2 induced
graph 的 singleton component `{6}` 不碰 B。交換後得到
`(01012,12123)`，rim 只有三色，中心填 0 得到 direct G fibre 中的完整
lift。checker 保存所有可用交換，不只這一份選出的 witness。

## 重播與信任邊界

```bash
python audits/2026-10-13-cross-edge-kempe-19209f4c/controls/check_cross_edge.py --check
python audits/2026-10-13-cross-edge-kempe-19209f4c/controls/check_cross_edge.py --check --seed 17
python audits/2026-10-13-cross-edge-kempe-19209f4c/controls/validate_controls.py --check
```

無旗標時也是 read-only check。`--write` 只能獨占建立本目錄的證書與摘要，
現存輸出必須拒絕覆寫。`validate_controls.py` 重播 normal、default、seed17、
覆寫拒絕及五種破損證書：刪空 J cell、改完整 lift 的具名色、改共邊 incidence
重數、刪 rejected H lift、破壞 Kempe component。九項均通過；原證書、摘要
與 checker 在各項前後 SHA256 一致。

canonical uncompressed certificate SHA256：
`8bcc3f9dd04ae7cec9f3079797cfa669b2e111ff42a190ffbda5b80eab4575d5`。

以上控制評分分別為 `triggered and holds` 或 `counterexample`。全域最小
933／941 來源、九／八個五度內點、一般排除定理及 Lean 驗證都沒有由有限控制
觸發；target/source 前提評為 `not triggered`。有限證書不代替紙面普遍證明。
