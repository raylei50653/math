# C₅ class 具名兩點接合：完整八點 relation 與同圖核對

2026-09-30。接續[兩點重疊規格](c5_two_vertex_overlap.md)，沿用既有
[132 類目錄](../artifacts/c5_cells/cells.json)，完成單次具名接合 evaluator
及六份固定控制。證據為紙面接合語義＋Python 有限重播，未新增 Lean theorem。
本輪沒有枚舉全部 class-pair 後繼或重新搜尋來源圖。
目前停止點由[導覽](c5_two_vertex_overlap_guide.md)維護。

2026-09-30 後續：[主例拓撲稽核](c5_two_vertex_join_topology.md)已對同一
`reference` 圖完成 36 組環序、24 份外面配置及原 A／B 框判定。
主例抽象平面，兩框各自可作整圖外界；兩份 disk 有四種區域關係。
舊 artifact 仍保存本輪的 `unknown`；新證據由獨立 companion 綁定，
另由[私有內點拓撲](c5_two_vertex_private_topology.md)完成 `private_interiors`：
原十五點三十五邊圖平面，兩來源 disk 可內部互斥，但兩組原路徑
分別阻斷 A、B 原框作整圖外界。
[反向私有內點拓撲](c5_two_vertex_private_reverse_topology.md)也已完成
同樣三項可行性核對，保留正反向完整 J 的差別。其餘三例及一般
transition 政策仍保留。
以下保留本輪語境。

## 1. 前提與完整語義

輸入兩個帶標號 class ID、A 的有序點對 `(i,j)` 及其在 B 的有序像
`(k,l)`。識別 `a_i=b_k`、`a_j=b_l`；B 點對反向就是另一份輸入。
除這兩點以外兩圖頂點互斥，沒有跨塊新增邊，兩側完整實際邊都保留。
若同一 simple-graph 邊出現兩次，合成一條；保留它的兩側來源。

八點次序固定為 `a0,…,a4`，接著依原索引加入 B 未共享的三點。
兩側原五點的嵌入分別為 `map_A`、`map_B`；它們也保留原 C₅ 環序。
八點次序是 relation 的欄序，不宣稱為任何 disk 的邊界環序。

令完整來源 relation 為 $R_A,R_B$，則

\[
J=\{c\in\{0,1,2,3\}^8:
c\circ\mathrm{map}_A\in R_A\quad\land\quad
c\circ\mathrm{map}_B\in R_B\}.
\]

`join_relations` 先將兩份來源 patterns 展開為全部具名賦色，按共享兩點
的實際有序色對接合，最後才對八點做一次共同 S₄ 正規化。沒有逐側
固定色名，也沒有只保留點對型別。每個保存的八點 pattern 代表整個
共同 S₄ orbit；本輪各圖含 proper C₅，故每個 orbit 都有 24 份具名賦色。

紙面正確性：任一整圖染色限制到兩側，即滿足上式；反向則為同一份
八點賦色各選一個來源內部延拓。由私有頂點互斥及無跨塊邊，兩個延拓
可合併。這是精確一次染色語義，不包含指定 embedding 或多步摘要充分性。

回投影仍保留完整五點 relation：

\[
\pi_AJ=\{\alpha\in R_A:(\alpha_i,\alpha_j)
\in\pi_{k,l}R_B\},
\]

B 對稱。Checker 分別核對兩份完整投影與 guard 篩列；artifact 同時保存
完整 patterns、mask 及是否命中既有 catalogue ID。命中 ID 只指 relation
相等，不代表原框在合成圖中是 disk 外界。

## 2. 主例與六份固定控制

主例為 A=B=R1023、`(a0,a2)=(b0,b1)`。共同欄序及兩側嵌入是

```text
U     = (a0, a1, a2, a3, a4, b2, b3, b4)
map_A = (a0, a1, a2, a3, a4)
map_B = (a0, a2, b2, b3, b4)
```

兩份代表都是純 C₅。整圖除 A 的五條框邊，另有
`a0–a2–b2–b3–b4–a0` 的五條邊，共八點十邊。
完整 $J$ 有 **140 個色軌道／3,360 份具名賦色**；
回投影精確為 **A=R1016、B=R1023**。

| 控制 | A／有序點對 | B／有序像 | J 色軌道 | 具名賦色 | π_A／π_B | 整圖點／邊 |
| --- | --- | --- | ---: | ---: | --- | --- |
| `reference` | R1023 `(0,2)` | R1023 `(0,1)` | 140 | 3,360 | R1016／R1023 | 8／10 |
| `reference_reverse` | R1023 `(0,2)` | R1023 `(1,0)` | 140 | 3,360 | R1016／R1023 | 8／10 |
| `free_pairs` | R1023 `(0,2)` | R1023 `(0,2)` | 152 | 3,648 | R1023／R1023 | 8／10 |
| `shared_chord_frame_edge` | R1016 `(0,2)` | R1023 `(0,1)` | 140 | 3,360 | R1016／R1023 | 8／10 |
| `private_interiors` | R127 `(0,2)` | R167 `(1,3)` | 60 | 1,440 | R127／R167 | 15／35 |
| `private_interiors_reverse` | R127 `(0,2)` | R167 `(3,1)` | 60 | 1,440 | R127／R167 | 15／35 |

後兩例使用目錄原 R127 的五個內點及原 R167 的兩個內點；七個私有
內點全部保留，沒有換代表或把內部限制刪掉。六份是語義控制，不是
完整八點後繼表，也不按幾何去重。

反向雙射的色軌道數和兩個五點投影雖相同，具名 relation 可以不同。
主例與反向例在同一 U 欄序下各有 70 個對方沒有的 patterns。例如
`(0,1,2,0,1,0,1,2)` 屬於主例；反向時 `b1=a0=0` 與 `b2=0`
違反 B 框邊。私有內點例與反向例則各有 16 個對方沒有的 patterns。
因此不能從軌道數或兩個投影的 mask 省略具體雙射。

## 3. 同一份代表圖的獨立核對

[Checker](../scripts/c5_two_vertex_join.py)有三條互相比對的路徑：

1. 由完整來源 Σ 展開相對換色並接合。
2. 遍歷全部 $4^8=65,536$ 個八點賦色，直接檢查 §1 的兩份完整限制。
3. 只讀合成後的實際邊與頂點，對全部八點賦色用 backtracking 找私有
   內點延拓。這條路徑不讀 class mask、relation 或前兩條路徑的接受集。

第三條路徑先從 `cells.json` 的 `k_eff`、`edges` 重建來源，**補入五條
C₅ 框邊**。A/B 內點使用不同名稱；源點到整圖的映射及各側補框後
完整邊集全部寫入 artifact。除共享兩點外沒有隱藏識別。

本輪四個不同來源 R127、R167、R1016、R1023 亦各自以全部 $4^5$
邊界賦色及內部回溯重算一次，確認原代表恰好實現目錄所列 Σ。
這只重驗四份選定代表，沒有重驗其最小內點數、目錄完備性或 disk embedding。

[完整 artifact](../artifacts/c5_two_vertex_overlap/eight_point_joins.json)
保存六份 J 的全部 canonical patterns，以及每個 pattern 在同一合成圖
上的完整染色 witness。每個 witness 均逐邊核對；對不存在延拓的賦色，
由只讀重播再次窮盡私有內點搜尋。六份共 393,216 個八點賦色查詢；
artifact 的 source SHA-256 綁定 catalogue、relation API 及本 checker。

## 4. 兩種錯誤壓縮的負控制

若直接拼兩側各自 canonical 的 patterns，不展開相對換色，主例甚至
保留零列，漏掉全部 140 個真實軌道；自由點對例只保留 58 個、漏掉 94 個。
Artifact 保存這種錯誤算法的列數及一個遺漏 witness，以免以後誤用。

另一個控制保留兩個 proper C₅ 框及**所選共享點對**的完整色對投影，
但丟掉兩側其餘完整 Σ 限制。私有內點例會從真實 60 個軌道放大為
152 個，多出 **92 個**不可延拓的軌道；反向亦同。這個數字僅針對
所選點對的鬆弛，不是另測全部二十份來源點對投影。

例如私有內點例的欄序是 `(a0,a1,a2,a3,a4,b0,b2,b4)`，
虛假列 `(0,1,0,1,2,1,2,2)` 通過上述鬆弛，但 B 的實際弦 `b2–b4`
兩端同為 2。完整 relation 與整圖回溯都拒絕它。
兩點 guard 可以核對相容性及回投影，不能替代 J。

## 5. 拓撲界線與剩餘問題

本輪只核對實際共同邊的身份。`shared_chord_frame_edge` 的 A 弦
`a0–a2` 與 B 框邊 `b0–b1` 識別為一條共同邊；其他五例沒有共同邊。
這與染色的 eq／neq guard 分欄保存，不能把強迫異色當作有實際邊。

六例的抽象平面性、原 A／B 框是否為 disk 外界、指定側別及區域重疊
合法性一律標為 `unknown`，沒有使用 planarity oracle。原 C₅ 環序
保留於映射；未指定的 embedding／rotations 不從色軌道推斷。
單一 witness 的拓撲判定亦不能外推至同 Σ 的所有實現。

已完成一次完整八點 evaluator、六份實例與同圖核對。完整後繼表、
拓撲分類、多步可替換性、有限拓撲摘要、生成圖類涵蓋及
$K_\infty=K_{\le5}$ 仍未完成；未將本輪程式或紙面論證 Lean 化。
若之後丟棄 B 的三個私有接口點，仍須證明未來操作不會再接觸它們。

## 6. 重播與單次輸入

```bash
python3 scripts/c5_two_vertex_overlap.py --check
python3 scripts/c5_two_vertex_join.py          # 寫入六份固定控制
python3 scripts/c5_two_vertex_join.py --check  # 只讀重算及逐 byte 比對

python3 scripts/c5_two_vertex_join.py \
  --class-a 1023 --pair-a 0,2 --class-b 1023 --pair-b 0,1 \
  --output /tmp/c5_two_vertex_join_reference.json
python3 scripts/c5_two_vertex_join.py \
  --class-a 1023 --pair-a 0,2 --class-b 1023 --pair-b 0,1 \
  --output /tmp/c5_two_vertex_join_reference.json --check
```

只用 Python 標準函式庫及既有 `boundary_relations.py`。指定單例時四個
選擇參數必須同時給；兩點必須相異、索引在 0..4，ID 必須在現有目錄。
省略 `--output` 時以含 IDs／點對的檔名寫入同一 artifact 目錄。

本輪上述重播、不同 `PYTHONHASHSEED` 的穩定性核對及 `lake build`
均通過；build 僅重播既有 linter warnings，不代表新增 Lean 證明。
文件驗證及工作樹狀態見[本輪紀錄](history/2026-09-30-c5-two-vertex-join.md)。
