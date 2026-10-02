# 941 excess-one：兩個原省略核心與 single-spoke 來源排除

2026-10-02，基準 `f4aa8b5`。接續 [四容量子覆蓋 §6.2](c5_excess_one_subcovers.md#62-941恰一份共同二接點原分量)。
目前停止點見 [Kempe 導覽](c5_kempe_guide.md)。

**結論：941 的 ε=1、t=1、(2,1,1) normal form 不能由 C₅ disk source
實現。** 同一 C₂ 若有原邊 xy 以外的頂點，兩個省略核心迫出三份原末端
三點支援，共同跨度至少六；若 C₂ 就是原邊 xy，完整 ordered two-contact
relation 不可能只禁 D。故 941 的 ε=1 只餘 t=2、(2,1) 及 t=3、(2)。
941 的 ε≥2、一般候選來源排除、共同出口與 K∞=K≤5 仍未證。

這是任意大小紙面來源排除，沿用既有全 degree-4 結構分類及其外部
degree-list／有限拓撲證據。新 Python 僅核對支援次序和完整局部 relations；
沒有新來源圖枚舉、planarity oracle 或 Lean theorem。

## 1. 同一原圖與兩個省略 witnesses

沿用固定完整 Σ 的 edge-minimal source：G 有指定 induced 外框
B=(b₀,…,b₄)，有效內部 H 連通，唯一 degree-5 root 為 r，其他內點
完整 degree=4。唯一 spoke 是 rb_s；H−r 的原分量為 C₂、U₀、U₁。
C₂ 的原有序接點為 (x,y)，兩個 unary 的原接點為 u₀、u₁。
所有分量的全部內邊、boundary 附件、原接點與環序都固定。

共同色框 U={0,1,2,3}，D=3；q_i 指 singleton 在 b_i 的三色列：

| 列 | 字面 boundary tuple | 條件 |
| --- | --- | --- |
| q₀ | 01212 | 拒絕；省略 U₀ 後仍拒絕 |
| q₁ | 01202 | 拒絕；省略 U₁ 後仍拒絕 |
| q₂ | 01201 | 接受 |
| q₃ | 01021 | 整張 G 為 minimal obstruction |
| q₄ | 01012 | 接受 |

另接受全部 T4。以原完整有序 relation 定義

\[
R_{C_2}(b)=\{(f(x),f(y)):f\text{ 是原 }C_2\text{ 在 }b\text{ 下的染色}\},
\qquad
F_{C_2}(b)=\bigcap_{t\in R_{C_2}(b)}\{t_1,t_2\}.
\]

R 非空由 degree-4 接點 slack 保證。沿用前報，

\[
|F_{C_2}(q_0)|=|F_{C_2}(q_1)|=2,
\quad D\in F_{C_2}(q_0)\cap F_{C_2}(q_1),
\quad F_{C_2}(q_3)=\{D\}. \tag{1}
\]

省略 witness 始終是下列兩張**原子圖**，不是獨立選的四容量集合：

\[
K_0=G-U_0=B\cup\{r\}\cup C_2\cup U_1,
\qquad
K_1=G-U_1=B\cup\{r\}\cup C_2\cup U_0. \tag{2}
\]

這裡刪 U_i 包含它全部 incident 邊；其餘附件、唯一 spoke 及原邊完全保留。
K_i 拒絕 q_i、接受 T4，有效內部連通且每點完整 degree=4。取任一
minimal q_i-core，degree-4 飽和沿其連通內部傳播，必取整個 K_i。
因此兩個 K_i 都可套用 [全 degree-4 分類](c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論)。

式 (1) 的最後一項亦可從前報重述：兩個 unary 各在另一個省略核心中
飽和且不禁 D；其未用色身份守恆，故 q₃ 的 D 只能由 C₂ 承擔。
q₃ 無可省略身份，容量五的唯一缺額必放在 C₂；其餘三個單容量因子
互異地覆蓋三個已用色。這不把 C₂ 拆成兩個 unary。

## 2. 兩個省略核心共有同一個原 triangle

全 degree-4 分類提供的原內部形態是：路徑；一個 triangle 加樹枝
（後續已證枝為路徑）；或兩個頂點互斥 triangles 由一條直接 bridge
相連且無其他外掛樹。最後一型的精確形態見
[雙 triangle 分類](c5_two_triangle_blocks.md#1-範圍與結果)。

在每張 K_i 中，C₂ 連通且含 x,y，所以 rx、C₂ 內的 x–y 路徑、yr
構成一個經 r 的 cycle。上述分類迫該 cycle 是 triangle，故 **xy 是
原邊**，兩個核心共有同一個 rxy；這不是收縮後的新 triangle。

r 在 K_i 中恰有三個內部鄰居：x、y、u_{1−i}，另有原 spoke rb_s。
若 K_i 是雙 triangle 型，r 必為唯一 bridge 的一端，該 bridge 就是
ru_{1−i}。第二個 triangle 全在 U_{1−i}，沒有外掛樹，因而原 C₂
必恰為 {x,y} 與邊 xy。

因此得到保留原分量身份的二分：

1. C₂ 恰為原邊 xy；或
2. C₂ 還有其他原頂點，則 K₀、K₁ 都只有原 triangle rxy，其餘為樹枝。

第二型只需要「其餘是樹」，無須使用路徑長度／palette／附件壓縮，
也不需重新跑長尾或分叉分類。

## 3. 非平凡 C₂ 的三份原末端支援：六跨度矛盾

假設 C₂≠xy。由 §2：

- K₀ 中的 U₁ 是透過 ru₁ 接到 triangle 的非空樹。
- K₁ 中的 U₀ 是透過 ru₀ 接到 triangle 的非空樹。
- C₂−{x,y} 非空；它由附在 x 或 y 的樹枝組成，至少有一個末端。

在每份 unary 中取離 r 最遠的樹葉；若 unary 只有一點，就取該點。
在 C₂ 的附枝中取離 rxy 最遠的樹葉。得到互異的原頂點
w₂∈C₂、w₀∈U₀、w₁∈U₁，且

\[
\deg_H(w_2)=\deg_H(w_0)=\deg_H(w_1)=1.
\]

三點都不是 r，完整 degree=4；G 簡單，故每點恰有**三個不同的原
boundary 鄰點**。以全部實際附件定義 S_C=N_B(C)，因此

\[
|S_{C_2}|,|S_{U_0}|,|S_{U_1}|\ge3. \tag{3}
\]

這三個 w 同時存在於原 G。雖然其存在性由不同省略核心確認，核心保留
原分量全部 incident 邊，所以 (3) 是同圖支援事實，沒有把不同列的
染色或獨立跨度相加。

套用 [共同 root 的相容 lifts](c5_independent_support_capacity.md#42-同一-root-的相容-lifts)：
僅為拓撲，把三份原分量各收縮成一點，C₂ 的兩條 r-contact 邊只保留
一條，所有實際支援邊保留。所得內部是三臂星；原 spoke 可切開框環，
在共同 [s,s+5] lift 中，三份支援成不交內部的有序區段。相同框端點
可共用，b_s 的兩份拷貝仍是同一原點。因此存在同一嵌入的跨度滿足

\[
\ell_{C_2}+\ell_{U_0}+\ell_{U_1}\le5.
\]

每份至少含三個不同框點，任何涵蓋它的區段長度至少二。於是

\[
\boxed{6\le\ell_{C_2}+\ell_{U_0}+\ell_{U_1}\le5,}
\]

矛盾。收縮與刪一條 root 邊僅用於這個來源拓撲證明；原 R_{C₂} 的兩個
有序座標始終保留，沒有宣稱這張 minor 保持 relation 或完整 Σ。

## 4. 原 C₂=xy 的完整 ordered relation

剩下 C₂ **原本就是** xy。x,y 各有原鄰居 r 及另一接點，因此各恰有
兩個不同 boundary 鄰居；記為 A_x、A_y，保持其具名位置。
任取 boundary row b，包括全部十個 representatives，令

\[
L_x(b)=U\setminus b(A_x),\qquad L_y(b)=U\setminus b(A_y).
\]

兩個 lists 都至少二色，完整關係恰為

\[
R_{C_2}(b)=\{(a,c)\in L_x(b)\times L_y(b):a\ne c\}. \tag{4}
\]

式 (4) 明確保留原邊 xy 的耦合條件，並不是 endpoint marginals 的乘積。
對任一色 d，d∈F 等價於 (L_x−{d})、(L_y−{d}) 無法各選一個異色。
兩集合非空；這只可能在它們同為一個 singleton {a} 時發生。
原 lists 大小至少二，故 L_x=L_y={a,d}。因此精確地

\[
F_{C_2}(b)=
\begin{cases}
L_x(b),&L_x(b)=L_y(b),\ |L_x(b)|=2;\\
\varnothing,&\text{其他情形}.
\end{cases} \tag{5}
\]

所以 F 永遠為空或二色集，與原 q₃ 要求 F={D} 矛盾。
尤其兩個含 D 的飽和列不能在這份同圖、同附件的 binary relation 上
轉成 singleton-D 列。

§3–4 完成全部 t=1 normal form 的任意大小來源排除。q₂、q₄ 的接受
仍是完整 941 前提，但此處不需額外 target 查詢；T4 用於繼承的省略
核心分類。沒有聲稱僅憑三個抽象 F 集就可排除未帶 omission witnesses
的任意 binary component。

## 5. 有限控制、重播與信任界線

[Checker](../scripts/c5_941_single_spoke.py) 與
[artifact](../artifacts/c5_941_single_spoke/observations.json) 保存：

- 49 對含 D、大小至少二的 lists，逐一保存完整 ordered relation 並核對 (5)。
- 5 個具名 spoke 位置 × 1,000 組具名三點支援，全部無共同有序 lift；
  另有 (2,3,3) 支援可放置的正控制。任意大小的 leaf／span 證明在 §2–3，
  此有限控制不代替 embedding 論證，也不生成圖。
- 10 份 q₃ minimal 四因子覆蓋控制，保留 spoke、C₂、U₀、U₁ 身份，
  全部只有 C₂={D}；省略 witnesses 在 artifact 中明標為定理前提。
- 原 C₂=xy 的 100 組具名附件 A_x、A_y；各自完整重播同一圖的十列，
  保存全部 ordered tuples、tuple colorings 及 4,000 次 pinned-root 查詢。
  1,000 個 binary row 結果中 805 個 F=∅、195 個 |F|=2。
  其中 13 組附件同時滿足 q₀、q₁ 含 D 二色飽和，無一可在 q₃ 禁 {D}。
  這些是局部必要模型，沒有冒稱它們帶著 unary 的 disk 實現。

```bash
python3 scripts/c5_941_single_spoke.py --check
PYTHONHASHSEED=17 python3 scripts/c5_941_single_spoke.py --check
python3 scripts/c5_excess_one_subcovers.py --check
python3 scripts/c5_independent_support_capacity.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證及未重跑範圍見 [本輪紀錄](history/2026-10-02-941-single-spoke.md)。
任意大小化約仍依賴全 degree-4 分類、雙 triangle 原結構、外部
degree-list 定理及既有有限拓撲證據；新 Python 未重新證明它們。
本輪沒有新 Lean theorem，`lake build` 不形式化六跨度論證。

本輪停止於排除 t=1。下一入口是 941 的 t=2、(2,1)：保留同一 C₂、
兩條具名 spokes、一份 unary，以及 q₀、q₁ 的不同省略身份；須分開
「兩列都省略 spoke」與「一列省略 unary」的來源形態。該型與 t=3
尚未在本輪處理；933 下界仍為 ε≥2，941 下界仍為 ε≥1。
