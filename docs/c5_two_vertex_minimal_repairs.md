# C₅ 固定反向接合的全部 inclusion-minimal 四點修復

2026-09-30。接續[四點投影最少個數與唯一組合](c5_two_vertex_quaternary_repairs.md)，
固定同一 `private_interiors_reverse` 原圖、原八點 U 與基底 P。
**全部 inclusion-minimal 修復共 15 組：1 組二份、14 組三份，
沒有其他份數。** 組合是不計順序的具名 scope 集合，不按圖自同構、
D₅ 或接口交換取商。

證據為完整排除集合的紙面覆蓋推論與固定圖 Python 證書，未 Lean 化。
目前停止點見[兩點重疊導覽](c5_two_vertex_overlap_guide.md)。

## 1. 固定模型與分類結論

沿用 R127 `(0,2)` 接 R167 `(3,1)`，識別 a0=b3、a2=b1；
保留十五點、三十五條原邊、七個私有內點與共同色框 `D={0,1,2,3}`。

```text
U   = (a0,a1,a2,a3,a4,b0,b2,b4)
C₁  = (a0,a4,a3,a2,b2), relation R255
C₂  = (a0,b4,b0,a2,a1), relation R1022
S_A = (a0,a1,a2,a3), scope 0
S_T = (a0,a2,b0,b2), scope 22
S_B = (a2,b0,b2,b4), scope 64
S_W = (a3,b0,b2,b4), scope 68
```

J 是原圖在 U 上的完整可延拓 relation，P 是 C₁、C₂ 兩份完整
relation 的具名共同拉回。**基底只有 P**；沒有先補三點投影或原邊。
每份新增條件恰為完整四點投影 `π_S J`，且 `S⊆U, |S|=4`。

| 關係 | 全域 S₄ 軌道 | 具名賦色 |
| --- | ---: | ---: |
| J | 60 | 1,440 |
| P | 114 | 2,736 |
| Δ=P∖J | 54 | 1,296 |

對 scope S 定義完整排除集

\[
F_S=\{u\in\Delta:u|_S\notin\pi_SJ\}.
\]

每個投影都保留 J，所以修復恰等價於 `⋃ F_S=Δ`；inclusion-minimal
表示移除任意一份投影後都不再等於 J，與最少個數不同。
令

\[
\mathcal E=\{S\subseteq U:|S|=4,\ \{b2,b4\}\subseteq S\}\setminus\{S_B\}.
\]

則全部 inclusion-minimal 修復正好是

\[
\boxed{\{S_A,S_B\}}
\quad\text{及}\quad
\boxed{\{S_A,S_T,E\}\quad(E\in\mathcal E)}.
\]

`|𝓔|=C(6,2)−1=14`。其中十三個 E 有相同的完整排除集合；
S_W 的完整排除集合較大，須另成一類。

## 2. 先固定 S_A，再分 S_B／S_T 兩支

沿用前輪三份八點見證，字串按 U 欄序，全部屬於 Δ：

| 名稱 | Pattern | 拒絕它的全部四點 scopes |
| --- | --- | --- |
| x | `01232112` | 只有 S_A |
| y | `01212132` | 只有 S_T、S_B |
| z | `01012122` | 全部含 `{b2,b4}` 的十五個 scopes |

x 迫使每個修復含 S_A。若含 S_B，因前輪及本輪均核對
`F_A∪F_B=Δ`，任何額外 scope 都可移除；此支只有 `{S_A,S_B}`。
若不含 S_B，y 迫使 S_T，故餘下全部固定 `{S_A,S_T}`。

這裡使用的是每個見證的**全部拒絕 scopes**。原圖拒絕由原邊強迫／
衝突證明核驗；每個接受 scope 均保存一份十五點正常染色，其四點
限制逐色符合該見證。共有 `69+68+55=192` 份局部延拓。
這些是分別存在的延拓，不是見證的同一份八點延拓。

## 3. 按完整排除集合分類與窮盡枚舉

Scope ID 沿用全部 `C(8,4)=70` 個索引四元組的字典序。
軌道 ID 是 Δ 正規代表的字典序 0–53；其完整對應保存在
[證書](../artifacts/c5_two_vertex_overlap/minimal_repairs.json)的
`difference_orbit_patterns`。每個軌道恰有 24 份具名賦色。
以下區間均含兩端，並且表示完整 ID 集合，而非只有基數。

| Class ID | Scopes | 完整排除軌道 ID 集合 | 軌道數 |
| --- | --- | --- | ---: |
| 0 | S_A，ID 0 | 42–53 | 12 |
| 1 | 其餘 51 scopes；證書逐一具名 | ∅ | 0 |
| 2 | `(a0,a1,a3,b0)`，ID 6 | 42–45 | 4 |
| 3 | 下節的十三份 E，排除 S_W | 0–19, 21,22,24,25,27,28,30,31,33,34,36,37,39,40,42,45,49,50 | 38 |
| 4 | S_T，ID 22 | 20–23,26–29,32–35,38–41,48–51 | 20 |
| 5 | `(a0,a3,b0,b2)`，ID 28 | 20–23,26–29,32–35 | 12 |
| 6 | S_B，ID 64 | 0–42,45,48–51 | 48 |
| 7 | S_W，ID 68 | 0–37,39,40,42,45,49,50 | 44 |

Checker 也直接比較所有類的完整具名排除集合。Class 0、5 雖然
同為 12 軌道，集合不同，不能合併。

固定 A、T 後，剩餘集合為

```text
R = Δ ∖ (F_A ∪ F_T)
  = orbit IDs {0–19,24,25,30,31,36,37}
  = 26 軌道／624 份具名賦色。
```

空排除類不能出現在極小修復；class 2 的排除集包含於 F_A，class 5
包含於 F_T，也不能出現。對 class 3 的共同排除集 F_E 與 class 7：

\[
R\subseteq F_E\subseteq F_W,\qquad
F_W\setminus F_E=\{20,23,26,29,32,35\}\subseteq F_T.
\]

所以 class 3 或 7 任選一份即補足 R。若都未選，R 全部留下；
若選多於一份，已有某個三份子組合修復，故不是 inclusion-minimal。
同一完整排除類的兩個 scopes 也不可能同時不可省。

計算程序先固定 A、T，對其餘四個非空類 `{2,3,5,7}` 遍歷全部
`2⁴=16` 子集合：12 個可修復，只有單選 class 3 或單選 class 7
給出 inclusion-minimal 修復。完整 16 筆剩餘集與每類的私有排除集
均保存。另一路不使用 x/y 化約或 bitmask，對八類全部 `2⁸=256`
子集合直接作集合聯集與逐份刪除，得到同樣三個極小類組合：

```text
{0,6}, {0,3,4}, {0,4,7}。
```

這同時證明分類完備；具名展開只在完整排除集相等時進行，
不使用欄位邊際或只按集合大小取商。

## 4. 全部十五組具名修復與份數分布

M0 是 `{S_A,S_B}`。下表每行各是一個完整組合 `{S_A,S_T,E}`；
S_A、S_T 依 §1 的固定具名次序。M 編號等於證書 `repair_id`。

| 修復 | E 的 scope ID | E 的完整具名 scope | 排除 class |
| --- | ---: | --- | ---: |
| M1 | 14 | `(a0,a1,b2,b4)` | 3 |
| M2 | 24 | `(a0,a2,b2,b4)` | 3 |
| M3 | 30 | `(a0,a3,b2,b4)` | 3 |
| M4 | 33 | `(a0,a4,b2,b4)` | 3 |
| M5 | 34 | `(a0,b0,b2,b4)` | 3 |
| M6 | 44 | `(a1,a2,b2,b4)` | 3 |
| M7 | 50 | `(a1,a3,b2,b4)` | 3 |
| M8 | 53 | `(a1,a4,b2,b4)` | 3 |
| M9 | 54 | `(a1,b0,b2,b4)` | 3 |
| M10 | 60 | `(a2,a3,b2,b4)` | 3 |
| M11 | 63 | `(a2,a4,b2,b4)` | 3 |
| M12 | 67 | `(a3,a4,b2,b4)` | 3 |
| M13 | 68 | `(a3,b0,b2,b4)`，S_W | 7 |
| M14 | 69 | `(a4,b0,b2,b4)` | 3 |

| 投影份數 | Inclusion-minimal 組合數 |
| --- | ---: |
| 0 或 1 | 0 |
| 2 | 1 |
| 3 | 14 |
| 4–70 | 0 |

只有 S_A 出現在全部十五組；S_T 出現在十四個三份解中，
S_B 只出現在唯一二份解中。

## 5. 逐份不可省見證

下表每一格都給出刪掉該 scope 後仍被接受、但不屬 J 的見證；
同一行中它通過所有其餘投影，且由刪去的那份拒絕。
三份見證 x、y、z 的完整 tuples 及全部局部原圖延拓見 §2。

| 修復組別 | 刪 S_A | 刪 S_B 或 S_T | 刪 E |
| --- | --- | --- | --- |
| M0：`{S_A,S_B}` | x；剩 6 軌道／144 賦色 | 刪 S_B：y；剩 42／1,008 | — |
| M1–M12、M14：`{S_A,S_T,E}`，class 3 | x；剩 6／144 | 刪 S_T：y；剩 8／192 | z；剩 26／624 |
| M13：`{S_A,S_T,S_W}` | x；剩 6／144 | 刪 S_T：y；剩 2／48 | z；剩 26／624 |

「剩」均指修復 relation 相對 J 多出的差集，基底一直是 P。
總共 `2+14×3=44` 份逐份刪除記錄。證書為**每一個具名組合**
分別保存被刪 scope、其餘 scope 清單、見證 tuple、完整剩餘軌道
ID 集合、剩餘具名差集及 relation 的大小。每份都直接重新作
具名投影查詢，並與排除集合路徑交叉比對。

## 6. 獨立 relation 核對、重播與範圍

[Checker](../scripts/c5_two_vertex_minimal_repairs.py)先以原邊及七個
原私有內點的回溯重建 J，重新作兩框的具名 natural join 得 P，
再由完整 J 重算七十份投影，與前輪證書比對。

每個 M0–M14 另行掃描全部 `4⁸=65,536` 份具名賦色，直接查詢
兩框及該組四點 relation；此路徑不讀覆蓋 bitmask、軌道 ID 或
預先算好的 P membership。共 `15×65,536=983,040` 次八點賦色查詢，
每組結果均與原 J **逐 tuple 作集合相等比較**，恰為 60 軌道／
1,440 份賦色。沒有以大小相等或 hash 相同取代 relation 相等；
保存的 hash 只是方便查核，完整 J 也隨證書保存。

九項負控制拒絕漏類、同基數錯誤排除集、漏具名展開、重複組合、
scope ID 次序錯誤、加入非極小超集合、同基數錯誤刪除殘留集、
不能通過保留 scope 的見證，以及同基數錯誤修復 relation。
證書 SHA-256 綁定前輪四點證書、完整來源／checker 鏈及新 checker。

```bash
python3 scripts/c5_two_vertex_minimal_repairs.py
python3 scripts/c5_two_vertex_minimal_repairs.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_minimal_repairs.py --check
python3 scripts/c5_two_vertex_quaternary_repairs.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新證書小於 1 MB，直接保存於 Git 工作樹；新 clone 須先重建被它
引用的三點、四點大型證書，指令見[導覽](c5_two_vertex_overlap_guide.md)。
實際執行結果與未重跑範圍見[本輪紀錄](history/2026-09-30-c5-two-vertex-minimal-repairs.md)。

本輪完成固定 P、原 U 與完整四點投影模型的全部 inclusion-minimal
組合。沒有分類一般較弱的局部條件表、Boolean 組合、輔助變數、
其他圖或未來接觸範圍。原圖拓撲、兩框 relation 與先前唯一二份
最優解保持原結論；未新增外部定理、Lean theorem 或 `native_decide`。
一般多步充分性、完整 Σ 壓縮與 `K∞=K≤5` 仍未證。
