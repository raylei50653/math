# 唯一 mixed P₃：對稱兩色分支的原五環與實際側支援排除

後續（2026-09-30）：[非對稱六跨度排除](c5_mixed_p3_asymmetric.md)已完成
(1,2) 及整份 root 交換型，容許一色側零跨度；結合本頁，兩端各一
incidence 接線的全部 residual 均無 disk 來源。下文當輪數字與證書保留。

2026-09-29，驗證時 Git 基準 `11335c1`，接續工作區的
[mixed 容量與接點化約](c5_mixed_capacity_contacts.md)。
**唯一 mixed 原分量為 P₃=x₀x₁x₂、z 只接 x₀、w 只接 x₂，且
E_z(q)=E_w(q) 為同一 pair 的 minimal q-core，不存在 induced-C5 disk 來源。**
不限制 unary 分量的頂點數、bridge 長度或旁支數，接點保持原位置。

紙面證明先確定三個原 lists 相同與原五環內側為空，再將兩側各自的
完整附件讀成一份幾何支援。五份同序支援恰用完五條框邊，色置換
不變性卻迫使整個 B 只用兩色，矛盾。不需要 T4、Gallai／degree-list
外部定理、minor 搜尋或 target 假設；未新增 Lean theorem。

[Checker](../scripts/c5_mixed_p3_symmetric.py)／
[證書](../artifacts/c5_mixed_p3_symmetric/observations.json)提供固定域控制，
不代替任意大小的 Jordan 論證。驗證見
[研究紀錄](history/2026-09-29-mixed-p3-symmetric.md)，目前停止點見
[weak-deletion 導覽](c5_weak_deletion_guide.md)。

## 1. 前提、完整關係與三個相同 lists

M 有限簡單，B=(b0,…,b4) 是 induced C5 disk 外框；H=M−B 非空連通。
固定 q=01012、U={0,1,2,3}。M 拒絕 q，刪任一非框邊後接受 q。
相鄰 z,w 完整 degree=5，其餘內點完整 degree=4。H−{z,w} 的唯一
mixed 原分量恰為 C*=x₀x₁x₂，P*ᶻ={x₀}、P*ʷ={x₂}。
其餘原分量各只接一個 root，全部原頂點、具名接點與邊保留。

對只接 r 的 unary 原分量 D，以 f_D(q) 表示從整份有序接點 tuples
取得的一維禁色集合，並使用原定義

\[
E_r(q)=U\setminus\left(q(N_B(r))\cup\bigcup_{D\sim r} f_D(q)\right).
\tag{1}
\]

本頁的額外前提是 E_z(q)=E_w(q)=T={a,b}。
[各一 incidence 引理](c5_mixed_capacity_contacts.md#53-唯一-mixedm_zm_w1-的-source-residual)
給 **完整** (x₀,x₂)-tuple 關係恰為 {(a,a),(b,b)}，以及
F*={(a,b),(b,a)}。沒有使用兩端 marginals 的笛卡兒積。

由完整 degrees，三個 x_i 各有恰兩個不同原 boundary 鄰點 S_i；
令 L_i=U∖q(S_i)，則 |L_i|≥2。對每個 c∈L₀，先選 L₁∖{c} 中的色，
再選 L₂ 中不同於該色的一色，即可延拓整條 P₃。因此每個 L₀ 色都會
出現在完整 tuple 的第一座標；反向同理，故 L₀=L₂=T。
若 L₁ 有 c∉T，則 (a,c,b) 是合法三點染色，與完整關係矛盾。
|L₁|≥2 再給 L₁=T。於是

\[
\boxed{L_0=L_1=L_2=T=\{d,3\},\quad
q(S_0)=q(S_1)=q(S_2)=U\setminus T.}
\tag{2}
\]

此處 3∈T 因 q 未使用 3。三份實際 S_i 仍可不同，不能把 b0、b2
或 b1、b3 因為同色而識別；完整三點染色恰為 (a,b,a)、(b,a,b)。

## 2. 原五環的內側為空，外部路徑保留

每個 unary D 有 0<|f_D(q)|≤k_D≤3。容量界由完整 tuple 交集得到；
若 f_D 空，刪一條 r–D 邊也不會擴大原來已全開的 D 介面，原 q
拒絕仍在，違反 minimality。上界三來自原 r 的 zw 與 mixed incidence
已佔兩條 degree。

若 D 沒有實際 boundary 附件，其完整關係及 f_D 對 S₄ 全色置換
不變，只能有 f_D=∅ 或 U，矛盾。故 **每份 unary 都實際碰 B**。
任取原 contact u∈D 與一個實際附件 v–b_j，D 內的原簡單 u–v 路徑
連同 r–u、v–b_j 給 r–B 路徑，內部避開其他原分量與 C*。
此外 z–x₀–b_i、w–x₂–b_j 各提供避開全部 unary 的原外部路徑。
這些是原圖的路徑，沒有新增 spoke 或把分量改為一條邊。

J=z–x₀–x₁–x₂–w–z 是原 simple cycle，且沒有 chord：C* 恰為 P₃、
兩份 root contact 恰如前提。J 完全在 B 內，每份 unary D 與 J 不交，
又有不經 J 的 D–B 實際邊路徑；由 Jordan 分離，D 只能在 J 外側。
所有 root／x_i 到 B 的 spokes 也在外側。其餘內點全屬這些 unary，
所以 **J 的開內側沒有頂點或額外邊**，J 是原嵌入的一個面。

## 3. 兩份完整側支援與五份同序區塊

定義原 r 側的實際支援

\[
A_r=N_B(r)\cup\bigcup_{D\sim r} S_D,\qquad
S_D=\{b_i:N(b_i)\cap D\ne\varnothing\}.
\tag{3}
\]

這只是實際附件的聯集。仍逐份保留 f_D、原接點次序、全部 bridges 與
旁支；沒有把幾份 unary 當成一個新的可獨立選擇的著色分量。
尤其 (1) 的 E_r 是原側圖「r 加所有原 unary 及 spokes」的精確 root
可取色集，不是以 A_r 重新建立的 list。

**完整側支援不變性。** 任何逐色固定 q(A_r) 的置換 π，可作用於
這份原側圖的整個 coloring；它對每份完整 tuple 同步作用，故
π(E_r)=E_r。若 A_r 只見零色或一色，穩定子分別為 S₄ 或固定一色的
S₃；都不可能保持一個二元子集。因此

\[
|q(A_z)|\ge2,\qquad |q(A_w)|\ge2.\tag{4}
\]

這個下界不需要先證每份 unary 至少見兩色，也不需要限制 k_D≤2。

取 J 的細正則鄰域，其外側到 B 是 annulus。內圓周保留五個具名區塊

\[
\mathcal U_z,\quad x_0,\quad x_1,\quad x_2,\quad\mathcal U_w
\tag{5}
\]

或整體反向。\(\mathcal U_r\) 包含 r 的全部外側 incidences、原 unary
及原 root-spokes；沿 r 的小 collar 區段連接截短邊端，僅用來讀取
原鄰域。x_i 區塊同樣保留兩條實際 boundary 邊。五個區塊可取兩兩
不交的連通細鄰域，各碰內、外圓周；它們的實際外支援分別為
A_z,S₀,S₁,S₂,A_w。

在每個 b_i 的小鄰域分開入射端，仍記成同一具名框點。同一區塊中
連接兩個外端的 crosscut，其不含內圓周的一側不能容納另一區塊的
外端，因後者還須接回內圓周。因此外端不能交錯，各支援成同序
區塊；兩側次序不符也會給交錯的兩條不交 crosscuts。
這是[原四環 annulus 論證](c5_adjacent_degree5_mixed_edge_order.md#2-原四環外側的同序區塊與周長界)
的 Jordan 步驟，此處重新以原 J 的五個區塊確定次序。

故有共同整數 lifts T₀,…,T₄，某起點 h 下

\[
\min T_0=h,\quad \max T_i\le\min T_{i+1},\quad
\max T_4\le h+5.
\tag{6}
\]

Lifts 模五是各自的實際支援，允許相鄰共享框端點，不能重用開框邊。
每份支援至少含兩點，且有其他正跨度區塊，故不能繞滿一圈並重複
端點。令 ℓ_i=max T_i−min T_i；由 (2)、(4)，

\[
5\le\sum_{i=0}^4\ell_i\le5.
\tag{7}
\]

因此五份支援各恰是一條原框邊的兩端，跨度全一，且無間隙。
保留了共享框端點；沒有預先把一般稀疏支援填成整弧。

## 4. 五條框邊同一色對的矛盾

由 (2)，S₀、S₁、S₂ 的三條框邊都見色對 U∖T。
對 A_r 所佔的一條框邊，q 的 proper 性給恰兩個已見色。交換另外
兩個未見色會逐色固定 q(A_r)，所以必保持 E_r=T。因 3 是其中一個
未見色且屬 T，另一個未見色也必屬 T；故

\[
q(A_z)=q(A_w)=U\setminus T.\tag{8}
\]

五份支援恰覆蓋 B 的五條框邊，(2)、(8) 遂使整個 B 只用色對 U∖T。
這既與 q=01012 用三色矛盾，也與奇數 C5 的 proper 兩色染色不可能
相矛盾。**指定對稱分支的 disk 來源不存在。**

可用兩個具名配置直接讀出最後矛盾：三條 P₃ 框邊同色只可能依次
01,12,23 或反序，此時 T={2,3}。

| A_z | S₀ | S₁ | S₂ | A_w | 逐色固定 q(A_z) 卻改變 T 的置換 |
| --- | --- | --- | --- | --- | --- |
| 04 | 01 | 12 | 23 | 34 | (1 3)，把 {2,3} 送至 {1,2} |
| 34 | 23 | 12 | 01 | 04 | (0 3)，把 {2,3} 送至 {0,2} |

兩種 root 身份與原環方向皆涵蓋。不需要逐份 unary 的支援分類，
也沒有查詢 p₁、p₂；來源排除不計為 target 接受。

## 5. 固定域證書、重播與剩餘界線

新 checker 只用標準函式庫，直接重用前層完整 tuples、逐邊角色接合
及獨立 pinned 回溯；不讀取舊證書的排除 flags。保存：

- 三個具名 x_i 各取兩個實際框鄰點的全部 10³=1,000 配置，包括
  同 q 色附件的候選；逐份記 ordered triple／contact／F bitmasks，
  以 16,000 個獨立 pinned queries 核對完整 root-pair 關係。
- 80 份對稱配置：T={0,3}／{1,3}／{2,3} 分別 8／8／64 份，三點
  完整 tuples 及原附件皆保存。每個 T 有 25 份完整側角色接合，共
  2,000 份必要附件／角色候選；不是來源圖數或 disk 實現證書。
- 由原五環方向直接生成十份飽和幾何，另窮盡所有大小≥2 支援的
  cyclic hull 框邊 masks，得到 120 份具名 packing；再篩原五環次序，
  獨立得到相同十份。共享端點合法，開框邊不可重疊。
- 78 份附件／1,950 份角色接合不符原五環次序；剩兩份附件／50 份
  角色接合由實際側支援的不變性排除。零保留、零 target 查詢。
- 所有 80 份配置的框反射 ρ=(3,2,1,0,4)、共同色置換 π=(0 1)，及
  整份 root 交換控制；另有 15 份框邊穩定子控制。
- 一份保留共享端點的 annulus 正控制：10 點、20 邊、12 個有向面，
  每個 dart 恰一次、每點 rotation 單圈、Euler characteristic=2。
  它只驗證有限拓撲配置，並非符合 degree／minimality 的來源。

```bash
python3 scripts/c5_mixed_p3_symmetric.py --check
PYTHONHASHSEED=17 python3 scripts/c5_mixed_p3_symmetric.py --check
python3 scripts/c5_mixed_capacity_contacts.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

無 `--check` 生成本層證書；`--check` 重算並逐 byte 比較。本 checker、
capacity 與前層 interface Python SHA 均綁定在新證書，不改舊 artifacts。
紙面證明不依有限表；未新增外部定理或 Lean 證明，`lake build` 只
確認既有專案。前層的非平面 minimal P₃ 控制仍然成立，未被本定理否定。

本輪停止於**兩端各一 incidence、兩側同 pair**的來源排除；可加入
[單側出口的失敗核心限制](c5_single_sided_exit.md#5-為何尚不是無條件的一般定理)，
不新增空的出口類別。下一窄題是同一 P₃ 端點接線的非對稱 residual
(1,2) 及 root 交換型；一色側不再由 (4) 保證正跨度，不能直接套 (7)。
其他 P₃ 接線、triangle、更大／多 mixed、完整 Σ、逐染色 repair、
一般／共同出口及 `K∞=K≤5` 仍未證。
