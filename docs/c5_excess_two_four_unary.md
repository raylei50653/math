# ε=2：t=2 四原 unary 的固定三點支援排除

**後續（2026-10-03）**：[t=1、(2,1,1,1) 兩原 unary 省略](c5_excess_two_single_spoke_two_unary.md)
已完成本輪留下的下一窄題，並由分類得到該型無全 degree-4 真子核心；
後續 [t=1 全分拆總報告](c5_excess_two_single_spoke_complete.md)再排除該整型。
下文保留本輪四原 unary 整型排除範圍。

2026-10-03，基準 `bbd900a`，接續
[t=2、(2,1,1) binary 省略排除](c5_excess_two_binary_two_unary.md)。
目前接手入口見 [Kempe 導覽](c5_kempe_guide.md)，當輪驗證見
[研究紀錄](history/2026-10-03-excess-two-four-unary.md)。

**結論：933／941 的固定完整 Σ、edge-minimal C₅ disk 來源，在 ε=2、
唯一 degree-6 root r、t=2 前提下，不可能有四份原 unary 分量。**
本輪排除整份 `(1,1,1,1)` 型；共同下界仍 ε≥2，其餘 ε=2、兩個
degree-5 roots（含 mixed）、一般出口及 K∞=K≤5 均保留。

核心是任意大小紙面化約：四份原支援共用五段框邊，只能有一份 D
分量；其支援是固定的三個連續框點，所有拒絕 singleton 位置都須落在
這三點。Python 核對小型必要域及完整五接點接合，沒有圖枚舉、新 Lean
theorem 或來源可實現性主張。全 degree-4 分類、外部 degree-list 與
D 守恆沿用既有證據，不由本輪有限控制重新證明。

## 1. 同一原來源與完整五接點關係

G 有限簡單，B=(b₀,…,b₄) 是指定有序 induced-C₅ disk 外框；Σ(G)
為 933、941 或其整圖 D₅ 像，故接受全部 T4。每條非框邊 e 都滿足
Σ(G−e)⊋Σ(G)。有效內部 H 連通，r 完整 degree 六，其他內點完整
degree 四。r 的兩條原 spokes 是 rb_s、rb_t，s<t；H−r 的四份
原連通分量 U₀,…,U₃ 各以一條原邊 rxᵢ 接 r。保持原分量、接點、
全部附件、ownership、環序及同一嵌入。

對任一 proper boundary coloring b，記原接點可取色集為 Sᵢ(b)。
[Unary slack 引理](c5_excess_two_spoke_unary.md#2-原-v-的-relation-非空不需分類其大小或支援)
給 Sᵢ(b)≠∅：刪除 root 後 xᵢ 的 list 有 slack，沿 Uᵢ 生成樹由葉
至根貪婪即可。完整有序關係恰為

\[
\mathcal R_G(b;r,x_0,x_1,x_2,x_3)=
\{(a,c_0,c_1,c_2,c_3):c_i\in S_i(b),\quad
a\notin\{b_s,b_t,c_0,c_1,c_2,c_3\}\}. \tag{1}
\]

四份原完整染色共用同一 b，原分量間無邊，故可拼接。定義 Fᵢ=Sᵢ
若 |Sᵢ|=1，否則 Fᵢ=∅。式 (1) 的精確 root 投影為

\[
U_4\setminus\bigl(\{b_s,b_t\}\cup\bigcup_i F_i(b)\bigr),
\qquad U_4=\{0,1,2,3\}. \tag{2}
\]

Fᵢ 只用於這個原接合的 root 判定，沒有取代完整 Sᵢ。五個 singleton
列共用未用色 D=3；D₅ 只搬運整張來源，不逐列或逐分量重新選色框。

## 2. 每份原分量的正跨度都有來源見證

固定 Uᵢ。完整 Σ edge-minimality 使原邊 rxᵢ 有一個見證列 q：G 拒絕
q，而 G−rxᵢ 接受 q。q 必為 singleton 列。由式 (2)，Fᵢ(q)={a}
且 a 不在其餘五個 unit 因子的聯集；這是該原因子的私有色。

六個空／singleton 因子覆蓋四色，可以各色取一個因子，得到恰四因子
子覆蓋。任何這樣的子覆蓋必保留 Uᵢ。刪去另外兩個原因子（spoke
刪原邊，unary 刪整份原分量），得原子圖 K，仍拒絕 q 且接受 T4。
K 至少保留兩份 unary，故有效內部連通；其所有內點完整 degree 四。
任取 minimal q-core，degree-4 飽和沿內部傳播，迫它等於 K。
[全 degree-4 分類](c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論)
於是使完整保留的 Uᵢ 成為 K₄-free Gallai tree。

令實際框支援 Aᵢ=N_B(Uᵢ)。以下證 |Aᵢ|≥2，沿用
[三原 unary 的支援論證](c5_excess_two_three_unary.md#31-每份原-unary-都有至少兩個實際框鄰點)：

- 若 Aᵢ=∅，原 relation 在 S₄ 下不變，不可能強迫 singleton。
- 若 Aᵢ={b_j}，固定 q(b_j)=a 的色置換迫 Fᵢ(q)={a}。再固定 r=a，
  Uᵢ 不可染且各 list 至少為 deg_Uᵢ；連通圖若有任何 slack 就可貪婪
  染色，故處處 tight。若某點有兩個外鄰點，它們只能是 r、b_j，且
  同為 a，便產生 slack。因此每點至多一個外鄰點，deg_Uᵢ≥3。
  但非平凡 K₄-free Gallai tree 的末端 block 有非割點 degree≤2；
  singleton Uᵢ 也不可能，矛盾。

每份 Uᵢ 可使用不同 edge-minimality 見證列及不同 K；結論是對**同一份
固定原支援**的下界。後面只將四份互異原分量的幾何量相加，不相加
不同核心或不同列的染色負載。

## 3. 唯一 D 分量與固定長度二框弧

[原 unary 的 D 守恆](c5_excess_one_subcovers.md#4-單接點分量的跨列-d-身份不能互換)
給固定 dᵢ∈{0,1}：dᵢ=1 當且僅當某 singleton 列 Fᵢ={D}。
在所有 singleton 列，dᵢ=1 的 Fᵢ 只可為 ∅／{D}，dᵢ=0 的 Fᵢ
只可為 ∅ 或 boundary 色 singleton。這是同一原 block-cut tree 的
membership 歸納，不假設非 D 色名守恆。

若 dᵢ=1，其見證列必在 Aᵢ 看見全部三種 boundary 色：否則交換 D
與未見色，保持全部原附件色而破壞 singleton。結合 |Aᵢ|≥2，任何
包含 Aᵢ 的框弧跨度至少 1+dᵢ。

由[同一 root 的相容 lifts](c5_independent_support_capacity.md#42-同一-root-的相容-lifts)，
同一原嵌入有包含四份原支援的弧 Iᵢ，開框邊段互斥、可共享端點，且

\[
5\ \ge\ \sum_i\ell_i\ \ge\ 4+\sum_i d_i. \tag{3}
\]

這裡只為拓撲論證收縮各 Uᵢ、保留原 root 邊及實際框支援；完整
relations 仍在原圖計算。忽略兩條 spokes 的額外扇區限制只是放寬
必要條件，不改變共同 lifts 的有效性，也未把弧上點新增為附件。

存在拒絕列時，spokes 只禁 boundary 色，故至少一份 Uᵢ 禁 D。
式 (3) 迫 **恰一個 dᵢ=1**。令該原分量為 U_*，則
ℓ_*=2，其餘三份的跨度各一，總跨度恰五。
U_* 在其見證列須看到三色，故其實際支援恰是

\[
A_*=I_* = \{b_j,b_{j+1},b_{j+2}\}\quad (\bmod\ 5). \tag{4}
\]

每個原拒絕 singleton 列都必由**同一 U_*** 禁 D。因此每個這樣的列
都必在固定三點 A_* 上看到三色，不能逐列改挑框弧。

## 4. 拒絕位置必落在同一連續三點

proper 三色 C₅ coloring 有唯一 singleton 位置 p，另兩色各出現兩次。
刪去 p 後，剩餘四點路徑交替使用兩色。因此任一連續三點框弧上三色
互異，當且僅當該弧包含 p：不含 p 時只見兩色；包含 p 時另兩點
分屬上述兩色。

令 Q 為全部拒絕 singleton 位置集合。式 (4) 給

\[
\boxed{Q\subseteq\{j,j+1,j+2\}\quad\text{對同一個 }j.} \tag{5}
\]

933 的 Q={0,1,2,3} 有四點，不可能滿足 (5)。941 的 Q={0,1,3}
不是連續三點，也不可能。整圖 D₅ 搬運保持這兩個障礙，故完成所述
四原 unary 型來源排除。無須枚舉兩-unary 省略身份的跨列配對，亦不
需要重跑 binary 分支或 spoke＋unary 的有限接回表。

## 5. 有限控制、重播與停止點

[Checker](../scripts/c5_excess_two_four_unary.py)與
[artifact](../artifacts/c5_excess_two_four_unary/observations.json)保存：

- 16 份具名 D 身份及其跨度下界；有拒絕列且符合五段預算者恰四份，
  每份只含一個 D 身份。
- 五個 singleton 列乘五個固定弧的 25 次 rainbow／位置等價檢查。
- 兩候選各五個 D₅ 像乘五個固定 D 支援弧，共 50 次比較；每次保存
  具名拒絕位置、弧索引及所有阻斷列，全部排除。
- 五組連續三點作正控制，均通過自身弧的必要條件；它們只是抽象控制，
  沒有宣稱有 edge-minimal disk 來源。
- 全部 3,360 個六-unit 四色覆蓋，核對四因子子覆蓋存在，且每個私有
  色因子出現在全部子覆蓋內。
- 全部 15⁴=50,625 份非空 unary domains，先以完整五接點 star 關係
  的限制與獨立 Cartesian product 核對 tuples，再接全部 16 個 spoke
  色集，合計 810,000 次完整五接點控制及 root 投影核對。保存完整
  star 算子、domain 表與 tuples digest；局部集合不宣稱來自 disk。

```bash
python3 scripts/c5_excess_two_four_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_four_unary.py --check
python3 scripts/c5_single_spoke_root_conservation.py --check
lake build
uv run --with-requirements requirements.txt python tools/artifacts.py status
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

本輪停止於整份 t=2、(1,1,1,1) 排除。其餘 ε=2 及一般來源仍保留；
目前下一窄題由導覽維護。紙面化約涵蓋任意大小原 unary，Python 只
控制有限關係／位置域。未新增 Lean theorem，`lake build` 只驗證
既有 Lean 專案；未重跑全 degree-4／外部 degree-list 的歷史證據。
