# 兩核心 D₁₃ 具名替換的 Lean 證明

2026-10-14。接續 [NamedRepair](lean_named_repair.md) 與
[SealedFourPort](lean_sealed_four_port.md)，將
[D₁₃ 來源族](../archive/reports/c5/two-vertex/c5_two_vertex_repair_caps.md)的首層替換接到兩個具名核心。
本輪範圍是正、反方向，以及 A 單側、B 單側、雙側各一次替換；
先保留共同十三點外部染色的完整接受關係，再投影回原八點 U。
原內點延拓的數量不作相等宣稱。

實作見 [NamedRepairReplacement.lean](../../Math/NamedRepairReplacement.lean)，
32 條公開定理的公理依賴見
[NamedRepairReplacementAudit.lean](../../Math/NamedRepairReplacementAudit.lean)，已由 [Math.lean](../../Math.lean) 匯入。
目前停止點由 [Lean 導覽](lean_guide.md)及
[兩點重疊導覽](../archive/guides/c5_two_vertex_overlap_guide.md)維護。

## 1. 同一具名核心與完整附件

沿用原十五點核心的頂點次序、35 條原邊、四種顏色與兩方向：

```text
U=(x,l,y,m,n,p,q,r)=(a0,a1,a2,a3,a4,b0,b2,b4)
A private=(h5,h6,h7,h8,h9)=原點8,…,12
B private=(v,w)=原點13,14
正向 (s,t)=(x,y)；反向 (s,t)=(y,x)
```

只密封兩個中心 h5、v。共同外部 X 的十三點依序為原點
`(0,1,2,3,4,5,6,7,9,10,11,12,14)`；外部附件不分別換色。

| 來源 | 原中心 | 原有序四接點 | X 上有序附件 |
| --- | --- | --- | --- |
| A | h5／8 | (h7,y,h9,x)／(10,2,12,0) | (9,2,11,0) |
| B | v／13 | (r,q,w,p)／(7,6,14,5) | (7,6,12,5) |

中心的全部 incident 邊恰是各自的四條 spokes。刪除這八條邊及兩中心後，
外部保留完整27條原邊，包括所有原框邊、q–r 與依方向選取的 s–w。
兩個局部四環的 rim 邊已在外部；接回 wheel／cap 時重複列出 rim，
不改變 `graphOfEdges` 所定義的圖。

替換圖使用 `Fin (13 + (kA + kB))` 的實際頂點與明列邊表，依序排列外部、A 內點、B 內點。
兩個 tail 彼此互斥，只能透過上述四接點接到共同外部，沒有額外跨邊。
每側的 wheel 有一個密封內點，D₁₃ 有九個密封內點；所有內點顏色均存在量化。
保留原中心名字作 cap 內點，不把中心加成第五個觀察點。

| A／B 局部圖 | 頂點數 | 不重複無向邊數 | 本輪結論 |
| --- | --- | --- | --- |
| wheel／wheel | 15 | 35 | 與原核心的具名染色語義等價 |
| cap／wheel | 23 | 59 | A 替換一次，保完整外部關係、J、指定 P |
| wheel／cap | 23 | 59 | B 替換一次，保完整外部關係、J、指定 P |
| cap／cap | 31 | 83 | 雙側各一次，保完整外部關係、J、指定 P |

表中不重複邊數由只讀來源核對計算；替換圖頂點數另有 `vertex_counts` 定理。

## 2. 證明接線

第一步直接從 `coreEdges rev` 的全部原邊，證原圖 proper coloring
等價於外部27邊正常、A wheel 正常與 B wheel 正常，並保留同一份十三點外部染色。
第二步從替換圖的實際邊表，證 proper coloring 等價於同一外部條件
及兩側局部圖各自的密封內點延拓。

對同一份外部染色 x，兩側的局部 boundary row 都由 x 及固定附件讀取。
`cap_wheel_equivalent` 逐份替換這兩個局部延拓條件，因而保留整個外部關係。
這個推導包含沒有延拓的空列；沒有拼接來自不同外部 rows 的 witnesses。

再以同一原 U 觀察十三點外部，得到替換圖的完整 J 等於原 `NamedRepair.J rev`。
每份任意 scope 的接受集合由完整 J 投影，因此逐 scope 保持。
P 僅取既有 `frame₁`／`frame₂ rev` 的兩份完整投影之共同拉回；
這是指定框族的 P，並未證這兩框恰為全部 disk 可用框。
由 J、P 與 scopes 保持，接回既有 repair 系統、極小分類及投影 arity 結論。

以下名稱省略命名空間 `FiveBoundary.NamedRepairReplacement`；全部公開定理均列入 audit。

| 定理 | 精確結論 |
| --- | --- |
| `attachments_literal`、`core_proper_decomposition` | 固定原有序接點、完整原35邊及兩中心密封分解 |
| `graft_no_loops`、`graft_edgeProper_iff`、`exteriorRelation_iff` | 替換圖無 loop；actual graph proper iff 同一完整外部條件及兩局部延拓 |
| `coreExterior_eq_unpatched`、`exteriorRelation_eq_core` | 原核心與首層替換保留逐份完整十三點外部染色 |
| `joint_iff_graph`、`joint_eq` | 替換圖原 U 的 J 確由同一份 actual proper coloring 給出，且等於原 J |
| `accept_iff`、`candidate_eq`、`system_eq` | 任意具名 scope、指定框 P 及完整 repair 系統保持 |
| `witness_coverage`、`repairs_iff`、`minimal_repairs_iff` | 三份原完整 witnesses、全部 rejectors、W／C 與所有 repair 模板保持 |
| `fifteen_minimal_repairs`、`unique_minimum_pair`、`forced_scope_iff` | 每個方向／模式恰15組極小 repairs、唯一最少對及唯一 forced A |
| `no_small_projection_repair`、`four_point_repair` | 原 J 投影合取、無輔助變數模型的 r*=4 保持 |

## 3. 驗證、信任及未涵蓋範圍

使用普通 Lean 證明及有限 kernel reduction，不增加公理、`sorry`
或 `native_decide`。具名定理的實際公理審計與重播結果見
[本輪紀錄](../history/2026-10-14-lean-named-replacement.md)。
[只讀來源核對](../../scripts/c5_lean_named_replacement.py)以 Lean `#eval` 匯出實際邊表，
核對兩方向、四模式共八圖的點序、附件及邊是否與原 Python 來源一致；
`#eval` 僅作資料核對，不作 theorem 證明。原來源 artifacts 不改。

```bash
python3 scripts/c5_lean_named_repair.py --check
python3 scripts/c5_lean_named_replacement.py --check
lake build
lake env lean Math/NamedRepairReplacementAudit.lean
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
git diff --check
```

本輪未形式化任意層數族的遞迴圖結構與 ownership、不證 disk embedding、
全部可用框、其他四接點實現或改寫完備性。一般後繼、多步摘要充分性、
一般出口及 `K∞=K≤5` 仍保留；LC 枚舉 completeness 與預設 build 接入也另行處理。
沒有使用四色定理或重新生成原來源 artifacts。
