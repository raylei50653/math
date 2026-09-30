# C₅ 兩混合框的四點投影修復：最少兩份且組合唯一

2026-09-30。接續[全部三點投影與 arity 下界](c5_two_vertex_ternary_projections.md)，
固定同一 `private_interiors_reverse` 十五點三十五邊原圖、完整八點 J
及兩混合框拉回 P。**以原 U 上完整四點投影合取修復 P，最少恰為
兩份，全部最小組合只有一組：**

```text
S_A = (a0,a1,a2,a3)
S_B = (a2,b0,b2,b4)
```

此處以 **P 單獨為基底**，不另加三點投影或原邊。組合是不計順序
的具名 scope 集合；沒有再按圖自同構、D₅ 或接口交換取商。
證據為原圖完整 Python 證書及關係覆蓋的紙面推導，未 Lean 化。
目前停止點由[兩點重疊導覽](c5_two_vertex_overlap_guide.md)維護。

## 1. 模型與精確覆蓋問題

來源為 R127 `(0,2)` 接 R167 `(3,1)`，識別 a0=b3、a2=b1。
保留七個原私有內點、全部原邊及共同顏色集合 `D={0,1,2,3}`：

```text
U  = (a0,a1,a2,a3,a4,b0,b2,b4)
C₁ = (a0,a4,a3,a2,b2), relation R255
C₂ = (a0,b4,b0,a2,a1), relation R1022
```

J 是原圖在 U 上的完整可延拓關係；P 是上述兩份完整框 relation
沿具名欄序的共同拉回。原圖與來源 maps 由
[反向拓撲](c5_two_vertex_private_reverse_topology.md)、
[兩框拉回](c5_two_vertex_mixed_pullback.md)固定。
J 有 60 軌道／1,440 份賦色，P 有 114／2,736。
記 `Δ=P∖J`，完整差集有 54 軌道／1,296 份賦色。

對每個四元素 scope S⊆U，從原圖重建的 J 計算完整 `R_S=π_SJ`，令

\[
F_S=\{u\in\Delta:u|_S\notin R_S\}.
\]

每份 J 賦色自動滿足每份投影，故對任意 scope 集合 \(\mathcal S\)，

\[
P\cap\bigcap_{S\in\mathcal S}\pi_S^{-1}(R_S)=J
\quad\Longleftrightarrow\quad
\bigcup_{S\in\mathcal S}F_S=\Delta.
\]

這是完整有序 relation 的有限覆蓋問題。Membership 一律用具名
顏色 tuples，不將局部 tuple 各自換色後拼接；全域 S₄ 只用來索引
差集。Δ 每個軌道大小皆為 24，證書同時保存全部 1,296 份具名賦色。

## 2. 全部 70 個 scope 的八種排除集合

按 U 索引的字典序排列全部 `C(8,4)=70` 個 scope，編號 0–69。
相同的 F_S 合為一類，得到下表；同樣基數不代表同一集合。

| Scope 或 scope 群 | 編號 | Scope 數 | 排除軌道 | 排除具名賦色 |
| --- | --- | ---: | ---: | ---: |
| 其餘 scopes | 證書逐一列出 | 51 | 0 | 0 |
| `(a0,a1,a2,a3)`，S_A | 0 | 1 | 12 | 288 |
| `(a0,a1,a3,b0)` | 6 | 1 | 4 | 96 |
| 含 `{b2,b4}`，但排除下列 S_B 及編號 68 | 證書逐一列出 | 13 | 38 | 912 |
| `(a0,a2,b0,b2)`，S_T | 22 | 1 | 20 | 480 |
| `(a0,a3,b0,b2)` | 28 | 1 | 12 | 288 |
| `(a2,b0,b2,b4)`，S_B | 64 | 1 | 48 | 1,152 |
| `(a3,b0,b2,b4)` | 68 | 1 | 44 | 1,056 |

十三份共同排除集恰為違反 b2–b4 的原 38 軌道。兩個各排除 12
軌道的 singleton 類互不相同，不能按基數合併。全部 70 份投影
的具名 tuples、每份單投影的完整剩餘軌道索引及八份完整排除集合
均保存在[證書](../artifacts/c5_two_vertex_overlap/quaternary_repairs.json)。

沒有單一 scope 排除全部 54 軌道。對全部 `C(70,2)=2,415` 個
無序相異 scope 對計算剩餘差集，只有 `{0,64}` 為空：

\[
|F_{S_A}|/24=12,\quad |F_{S_B}|/24=48,\quad
|F_{S_A}\cap F_{S_B}|/24=6,\quad
F_{S_A}\cup F_{S_B}=\Delta.
\]

完整投影沿用前輪數值，並從原 J 再算核對：

| 投影 | 全部 S₄ 軌道代表 | 具名賦色 |
| --- | --- | ---: |
| π_{S_A}J | `0101`, `0102`, `0120`, `0121` | 84 |
| π_{S_B}J | `0110`, `0112`, `0123` | 60 |

因此最少個數是 2，唯一最小組合為 `{S_A,S_B}`。省略 S_A 時仍
多 6 軌道／144 份；省略 S_B 時仍多 42 軌道／1,008 份。
後一個數字以 P 為基底，與前輪先補回原邊後的 8 軌道不同。

## 3. 三份見證給出的最小性與唯一性

以下每列均屬 Δ，字串依 U 次序讀取：

| 見證 | 會拒絕它的全部四點 scopes | 接受 scopes 數 |
| --- | --- | ---: |
| x=`01232112` | 只有 S_A | 69 |
| y=`01212132` | 只有 S_T、S_B | 68 |
| z=`01012122` | 全部含 `{b2,b4}` 的 15 個 scopes | 55 |

對每列、每個接受 scope，證書保存一份原十五點正常染色，其該
四點限制逐色等於此列，並核對全部 35 條原邊。總共
`69+68+55=192` 份延拓，另核對共同 S₄ 換色後的 4,608 份。
原圖拒絕由完整 Δ 記錄的原邊強迫／衝突證明給出。這些是分別
存在的延拓，沒有把它們當作一份共用八點延拓。

紙面覆蓋論證如下：

1. 要排除 x，任何四點投影修復都必須包含 S_A，即使允許更多份。
2. 單獨 S_A 接受 y，所以至少需要兩份；若恰有兩份，第二份必為
   S_T 或 S_B，才能排除 y。
3. S_A 與 S_T 都接受 z，所以 `{S_A,S_T}` 仍不足；第二份只能是 S_B。
4. `{S_A,S_B}` 的完整拉回確實等於 J，給出上界。

這個短論證不需逐對引用 2,415 筆表格；其 scope 接受／拒絕分類
仍依上述固定圖有限證書，而不是任意圖的拓撲定理。

實際上，只有 S_A 在**所有四點投影修復**中都不可省：它獨有的
四份排除軌道為 `01232112`、`01232113`、`01232331`、`01232332`。
對任何其他 scope，全部其餘 69 份仍覆蓋 Δ；checker 核對每列的
全部拒絕 scopes，確認沒有其他 singleton 拒絕集合。因此
「S_B 屬於唯一兩份最優解」不能讀成「任何較大修復也必含 S_B」。

## 4. 與任意局部條件的關係

若任意條件 H_S 只讀取 S，而且合取後仍保留全部 J，則必有
`π_SJ⊆H_S`。以完整投影取代 H_S 只會加強篩選，仍保留 J。
因此在原 U、無輔助變數、最大 arity≤4 的局部合取模型中，
新增條件的個數也至少為兩個。

更進一步，若恰用兩個條件精確修復 P，它們的 scopes 也必恰為
S_A、S_B：將不足四點的 scope 任意補足四點，改用完整投影，
必得到上述唯一最小組合。若真有不足四點的 scope，就有多種
四點補法，與唯一性矛盾；若兩份補到同一 scope，則會產生已被
排除的單投影修復。此結論只限制必要的 scope，不宣稱任意 H_S
的關係表本身也唯一。

不涵蓋一般 Boolean 組合、存在量化的輔助變數或改變未來可接觸
範圍的模型。本輪分類的是**最少個數**的全部組合；尚未列出
所有個數較大、但刪掉任一份就失效的 inclusion-minimal 修復。

## 5. 重播與證據界線

[Checker](../scripts/c5_two_vertex_quaternary_repairs.py)只用標準函式庫，
SHA-256 綁定前輪三點證書、其完整來源／checker 鏈及自身。
J 再從原邊及七內點回溯重建，P 再作具名 natural join。
70 份投影全部從 J 產生，不從 guard 公式或投影基數推測。

證書保存全部 54 份差集軌道的拒絕 scope 清單與原邊拒絕證明；
每份單投影及每個 scope 對的剩餘集合以這份固定軌道表的索引
完整列出，可由同一全域 S₄ 展開。雙投影先用軌道 bitsets 計算，
再以具名賦色集合交集獨立核對；唯一解另經全部 `4^8` 賦色查詢
重建，與完整 J 集合相等。沒有以基數相等代替 relation 相等。

```bash
python3 scripts/c5_two_vertex_quaternary_repairs.py
python3 scripts/c5_two_vertex_quaternary_repairs.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_quaternary_repairs.py --check
python3 scripts/c5_two_vertex_ternary_projections.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

九項負控制須拒絕：漏掉 scope、改錯具名欄序、刪合法投影 tuple、
加不可延拓 tuple、用同基數錯誤集合取代剩餘差集、漏掉 scope 對、
漏報最小解、加入假最小解、原圖延拓違反原邊。實際驗證範圍見
[本輪紀錄](history/2026-09-30-c5-two-vertex-quaternary-repairs.md)。

本輪不新增來源圖、嵌入或外框，不改動既有拓撲證書。未新增
Lean theorem、`native_decide` 或外部定理依賴；`lake build` 僅驗證
既有 Lean。其餘代表、完整 class-pair 後繼、一般多步充分性、
完整 Σ 的一般壓縮定理與 `K∞=K≤5` 均仍保留。
