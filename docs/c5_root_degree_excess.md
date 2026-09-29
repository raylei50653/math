---
docgraph:
  id: c5.root-degree-excess
  family:
    - c5
    - c5.degree5
  derives_from:
    - c5.adjacent-degree5-no-mixed
    - c5.adjacent-degree5-interfaces
  related:
    - c5.adjacent-degree5-no-mixed-t2-path-palettes
    - c5.single-sided-exit
---
# No-mixed root 骨架：degree 超額預算與樹上拒絕證書

後續（2026-09-29）：[交換或幾何阻斷範圍遍歷](c5_exchange_geometry_scope.md)
核對 §6 的 A／B／C 邊界；雙 root 已完成兩側 t=2、t_z=2 配 t_w=1
或 t_w=0,(2,1,1)，以及 [t_w=0,(2,2) 缺額型](c5_adjacent_degree5_no_mixed_t2_t0_pairs.md)
四類及整圖 root 交換型。原 3,548 份分類與 1,920 份
抽象路徑控制不構成一般 A 的證明；下文表格保留本報告當輪狀態。

2026-09-29，基準 `30a2e59`。將使用者本輪提出的兩個推導補齊前提與
證明，並以獨立有限控制重播。**已證的是 source 預算恆等式及樹上
edge-minimal list obstruction 的完整描述；跨列分離仍是猜想。**
本報告主引理為初等紙面證明，不依賴平面性、Gallai 或來源接受其他列。
§5 的一般骨架推論另用外部 Gallai 定理。Python 只核對有限 lists／
既有必要資料；未新增 Lean theorem。研究優先序見 [HANDOFF](HANDOFF.md)。

## 1. 同一來源上的完整消去

M 是有限簡單圖，B 為指定 induced C5，H=M−B 非空連通，
U={0,1,2,3}，q 是固定 proper boundary coloring。
M 不延拓 q，刪任一非框邊後均延拓 q；此處的 edge minimality
**不包含刪除 B 的框邊**。R 非空，恰為完整 degree≥5 的內點，
其餘內點完整 degree=4。每個原分量 C⊆H−R 恰接一個 root r；
記 Q=M[R]、P_C=N_M(r)∩C、k_C=|P_C|、t_r=|N_B(r)|。
H 連通及 no-mixed 使 Q 連通；允許 Q 只有一個點，或 H−R 為空。

對每個 proper row β，T_C(β) 是**原 C** 所有內邊及 C–B 附件下的
完整有序 P_C-tuples；暫不固定 r 的色。任一接點的 boundary list
有嚴格 degree slack，其他點至少等於 deg_C，故 T_C(β) 非空。
這是 [生成樹貪婪 slack 引理](c5_adjacent_degree5_interfaces.md#4-degree-4-的-tightness共鄰點與分量解除) 的直接應用。
定義

\[
F_C(\beta)=\bigcap_{t\in T_C(\beta)}\operatorname{set}(t),\quad
A_r(\beta)=U\setminus\beta(N_B(r)),\quad
E_r(\beta)=A_r(\beta)\setminus\bigcup_{C\sim r}F_C(\beta).
\tag{1}
\]

由非空完整 tuple 立即有 |F_C(β)|≤k_C。給 r 色 a 時，C 可填入
恰當且僅當有完整 tuple 避開 a，即 a∉F_C(β)。因此

\[
\boxed{\beta\in\Sigma(M)\iff Q\text{ 可用 lists }E_r(\beta)\text{ proper 著色}.}
\tag{2}
\]

證明先固定**同一份** root coloring，再各自選原 C 的完整見證；
沒有把同一 C 的端點 marginals 相乘，也沒有改動共同色框。
式 (2) 適用所有 β；以下 minimality 的後果僅在 source q 使用。

## 2. Minimality 提供的三個前提

**Spokes 異色且 F_C(q)⊆A_r(q)。** 刪 rb_i 後取完整延拓。
被刪兩端必同色 d=q_i，否則原圖也可延拓。因此同一 root 的
其他 spoke 不可有色 d，而每個同側原 C 都能避開 d。
逐條 spoke 如此，得到 q 在 N_B(r) 上單射，以及所有 F_C 避開
q(N_B(r))。無 spoke 時後一包含式自動成立。

**固定 lists 的骨架 edge minimality。** 刪 e∈E(Q) 不改任何原 C、
root-spoke 或 E_r(q)。式 (2) 及原圖 minimality 給
Q 不可 E-color，但 Q−e 可 E-color。

**|E_r(q)|≤deg_Q(r)，包括孤立 root。** 選任一 incident 非框原邊
e（deg_M(r)≥5 保證存在），取 M−e 的延拓。捨去 r 及只接 r 的
所有原分量後，其餘 roots 的色仍給 Q−r 的 E-coloring：其他 roots
的 spokes／原分量均未受這次刪邊影響。若 |E_r|>deg_Q(r)，便可
貪婪補回 r，再用 (2) 填回它的原分量，矛盾。若 Q 單點，這證明
E_r=∅，不需要選一條不存在的 root edge。

## 3. Degree 超額的精確 source 預算

本節所有 F、A、E 都指 q。定義

\[
D_r=\sum_{C\sim r}(k_C-|F_C|),\qquad
O_r=\sum_{C\sim r}|F_C|-\left|\bigcup_{C\sim r}F_C\right|,\qquad
\kappa_r=\deg_Q(r)-|E_r|.
\tag{3}
\]

容量界、集合聯集界及 §2 分別保證三者非負。Spokes 異色及
F_C⊆A_r 給

\[
\left|\bigcup_C F_C\right|=4-t_r-|E_r|,\qquad
\sum_C k_C=\deg_M(r)-\deg_Q(r)-t_r.
\]

兩式相減，得任意 root 度數下的恆等式

\[
\boxed{D_r+O_r+\kappa_r=\deg_M(r)-4.}\tag{4}
\]

對其他內點完整 degree=4 求和，得到

\[
\boxed{\sum_{r\in R}(D_r+O_r+\kappa_r)
=\varepsilon(M):=\sum_{v\in H}(\deg_M(v)-4).}\tag{5}
\]

degree-5 是一單位，degree-6 是兩單位；κ 是骨架 list 缺額，
不是環數。若取消 source minimality，spokes 可能重色、F 可能碰
spoke 顏色，κ 也可能為負；不能把 (4) 原封不動套給 target p。
式 (1)–(2) 在 target 仍成立，(4) 的這些前提須重新檢查。

## 4. 樹上 edge-minimal list obstruction 的完整描述

**引理。** Q 是有限非空樹，lists E_r 為有限集合。以下等價：

1. Q 不可 E-color，且每個 Q−e 均可 E-color；
2. 存在邊標色 c_e，同一點 incident 邊的標色互異，且
   E_r={c_e:e∋r}。單點基底為 E_r=∅。

**必要性。** Q 有邊時，刪 e=rs 分成兩棵半樹；令 S_{r|s}、
S_{s|r} 為兩半在端點可實現的**完整色集合**。刪邊可著色使兩者
非空；若可選異色就能接回 e，故

\[
S_{r|s}=S_{s|r}=\{c_e\}.\tag{6}
\]

每個 c_e∈E_r。若 a∈E_r 不在 incident 邊標色中，可把 r 設 a，
各鄰接半樹取其 c_e 見證，接成整棵樹，矛盾，故 E_r 恰為此聯集。
若 rs、rt 同標 c，刪 rs 後 r 側端點只能是 c，但仍保留的 t 側
半樹也只能是 c，與 rt proper 矛盾。因此 incident 標色兩兩不同。

**充分性。** 假設有 E-coloring。每點所取色唯一對應一條 incident
邊，將其指向那條邊的另一端。有限樹中每點有一條出邊，必形成
一個兩點有向環；兩端都用了同一 c_e，矛盾。刪 e 後，對兩半
分別以 e 的端點為根：根用 c_e，其餘點用通向 parent 的邊標色。
incident 標色互異保證每條保留邊 proper，且各點顏色都在 list 中。
單點空 list 的兩方向亦成立。

因此對 §1 的樹狀骨架，

\[
\boxed{|E_r|=\deg_Q(r),\quad\kappa_r=0,\quad
D_r+O_r=\deg_M(r)-4.}\tag{7}
\]

任意 degree-5 root 樹的每點恰一單位；單 root、相鄰雙 root 都是
特例。還有 deg_Q(r)≤4；這是 source list 容量限制，不是 target 分離。
當 O=1 時所有分量飽和，恰一色出現兩次；不能把重疊預算誤認為
必有一份缺額分量。既有平面雙 root 表保留 94 份 D=1 與 24 份 O=1。

## 5. 跨列須保留的完整半樹關係

對固定原樹、固定原分量和**每一列 β**，定義 M_{r|s}(β) 為刪 rs
後 r 半樹的完整可實現端點色集。式 (2) 給精確遞迴

\[
M_{r|s}(\beta)=\{a\in E_r(\beta):
\forall t\in N_Q(r)\setminus\{s\},\
\exists b\in M_{t|r}(\beta),\ b\ne a\}.\tag{8}
\]

給整樹任取根時，對它的全部鄰點使用同一公式，非空恰等於可延拓。
這是**同源、逐列計算的完整關係**，不是把 source 的 {c_e} 當成
target 的 spoke／色點。只知道 (6)，不能決定任何 M_{r|s}(p)。
如果要壓縮成可多步合併的 state，仍須另證所有所需列與邊界身份的保存。

一般連通 Q 若全部 κ=0，則 E 是被拒絕的 degree assignment。
外部 [Dvořák，Theorem 10，第 6 頁](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
因此給 Q 為 Gallai tree，E 具有 blockwise-uniform palettes。
本輪核對了該定理；這一推論不是新 Lean 證明。若任何 κ>0，E
不滿足該定理的 degree 下界，不能直接套用。

## 6. 已證機制與三層待證目標

主線是完整接合失敗，迫使禁色需求，再比較同一原圖的 palettes；
結果可能是支援／拓撲矛盾，也可能重建額外 source 禁色。
保留三種不同結論：來源排除、指定列延拓、帶額外來源條件的出口接合。
使用 target 拒絕才取得的 K5，只排除該拒絕候選。

例如 [兩側 t=2](c5_adjacent_degree5_no_mixed_t2_path_palettes.md) 的
512→580→640→644，是原 bridge、雙端點、全路徑交換在同一來源上的
逐層相容性。三輪共新增 132 個延拓，原 322 份支援資料未新增來源排除；
完整 Σ 及出口仍另用來源雙缺失與刪邊繼承。

| 層次 | 精確工作目標 | 現況 |
| --- | --- | --- |
| A：交換或幾何阻斷 | 對 target 額外禁色需求，完整關係、source 預算及跨列約束是否總能導向實際支援不可能，或重建額外 source 禁色？ | 機制完備性假設，並無一般證明；現有規則失效不等於數學反例 |
| B：no-mixed 雙 root 全分拆 | 指定 C5 disk 的 minimal q-core，恰有相鄰雙 degree-5，其餘 degree-4、無 mixed；若接受 Ω∖{p,q}，p、q 為 singleton 位置相鄰的三色 patterns，則接受 p | 兩側 t=2 已達較強的、不需其他來源接受列的 p₁／p₂ 分離；其他四型組合仍開放 |
| C：degree-5 root 樹分離 | 將 B 的兩 root 改為任意非空 degree-5 root 樹，其餘及來源接受條件保持 | (7) 提供 source 結構，跨列半樹關係相容性未證；不把 (6) 直接傳到 p |

較強版本「只要求 minimal q=01012 即接受 p₁=01021、p₂=01212」
可另外測試；它若失敗，未必否定帶 Ω∖{p,q} 來源條件的 B／C。
這些目標即使完成，也不提供可處理核心的存在性；較大／多 mixed、
非樹骨架、degree≥6、共同出口及 K∞=K≤5 仍另有缺口。

## 7. 有限控制與重播

[Checker](../scripts/c5_root_degree_excess.py) 與
[JSON](../artifacts/c5_root_degree_excess/observations.json) 保存八個具名樹型：
四個顏色、1–4 點全部五型；三個顏色、5 點全部三型。Lists 包含空集，
頂點具名，**未以色置換或頂點對稱商掉 assignments**。

完整半樹訊息遞迴與直接枚舉全部 literal colorings 的 bitset oracle
逐 assignment 核對；每份拒絕再核全部刪邊。共 **233,744 份**，
其中 **113 份** edge-minimal 拒絕，全符合 (6)–(7)；每份保存邊標色
及每條刪邊的完整染色。另獨立窮盡 proper edge labels，所得 list
assignments 與這 113 份恰相同，核對引理的兩個方向。
三點路徑全用 {0} 是「沒有 edge minimality 就不能推出 κ=0」的負控制。
原 149 份側資料均重算 (4)，118 份保留側型分成 94 份 (1,0,0)、
24 份 (0,1,0)。這不是 C5 原圖枚舉或來源實現證書。

```bash
python3 scripts/c5_root_degree_excess.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
```

下一份 [t_z=2、t_w=1 支援表](c5_adjacent_degree5_no_mixed_t2_t1.md)
把這個預算接入原 136 份有序資料，保存拒絕原因與關閉機制。
實際驗證及省略範圍見 [本輪紀錄](history/2026-09-29-root-degree-excess.md)。
