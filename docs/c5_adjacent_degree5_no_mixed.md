---
docgraph:
  id: c5.adjacent-degree5-no-mixed
  family:
    - c5
    - c5.degree5
  derives_from:
    - c5.adjacent-degree5-interfaces
    - c5.adjacent-degree5-shared-singleton
  requires:
    - c5.no-spoke-exterior
    - c5.single-spoke-three-one
    - c5.single-spoke-four
---
# 相鄰雙 degree-5 無 mixed：同色 residual、容量與逐邊 minimality

後續（2026-09-29）：[兩側 t=2,(2) 實際支援與環序](c5_adjacent_degree5_no_mixed_t2.md)
已將原 88 份資料接成 322 份必要支援（42 份原資料有支援，46 份纖維空）；
512／644 個 target 查詢已證、132 個未決。原表保留，未證整型分離或 disk
實現；下文保留本輪語境，現行入口見 [HANDOFF](HANDOFF.md)。

2026-09-29。接續 [完整有序介面](c5_adjacent_degree5_interfaces.md) 與
[unary 精確消去](c5_adjacent_degree5_shared_singleton.md)。本輪完成無 mixed
型的任意大小必要化約：**兩側 residual 必為同一 singleton，每側容量缺額
加重疊量恰為一；平面來源每側只剩四種接點分拆。**

精確接合、逐邊 minimality 與容量計數為初等紙面證明；平面篩選沿用
外部 degree-list 定理及既有原圖 K5 論證，補上經原 zw 的實際外部路徑。
Python 核對有限代數、固定非平面來源與具名 minor 子圖。未新增 Lean theorem，
未證無 mixed 的指定雙列分離或新增出口類別。研究優先序見 [HANDOFF](HANDOFF.md)。

## 1. 同一來源與無 mixed 的完整接合

G 有限簡單，B=(b0,…,b4) 是 induced C5；U={0,1,2,3}，q=01012。
H 為非空連通有效內部；有序相鄰 roots z、w 的完整 degree=5，其他
內點完整 degree=4。原 H−{z,w} 的每個分量 C 恰接一個 root；沒有 mixed。
記只接 r 的分量族為 C_r，S_r=N_B(r)，P_C=N(r)∩C，k_C=|P_C|。
保留原 zw、原分量身份、有序接點、實際 boundary 附件及存在時的 rotation。

對任意 proper boundary row β，以原圖所有 C 內邊及 C–B 邊定義完整
接點關係 T_C(β)，並令

\[
 F_C(\beta)=\bigcap_{t\in T_C(\beta)}\operatorname{set}(t),\quad
 A_r(\beta)=U\setminus\beta(S_r),\quad
 E_r(\beta)=A_r(\beta)\setminus\bigcup_{C\in C_r}F_C(\beta).
 \tag{1}
\]

未指定 root 色時，C 每點的 boundary list 大小至少 deg_C，任一接點
有 slack，所以 T_C 非空。因此 |F_C(β)|≤k_C；禁色指**每份完整
coloring 的接點上都出現該色**，不是要求某一指定接點固定取該色。

沒有跨 C 邊或 mixed 約束，故完整接合恰為

\[
 Z_G(\beta)=(E_z(\beta)\times E_w(\beta))\setminus\Delta,\qquad
 Z_{G-zw}(\beta)=E_z(\beta)\times E_w(\beta).
 \tag{2}
\]

每次接合先固定同一有序色對，再為每個原 C 選一份完整見證。
不能把同一 C 的端點 marginals 相乘，或對兩側獨立換色。

假設 q 拒絕 G 而接受 G−zw。由 (2)，乘積非空且包含於 Δ。
選一對 (a,b)；它必有 a=b=c。任一 a′∈E_z 與 b 接合迫使 a′=c，
另一側同理。因此

\[
 \boxed{E_z(q)=E_w(q)=\{c\}.} \tag{3}
\]

這使用無 mixed；一般雙 root 的非空對角關係未必 singleton。
也不能先假定 c=3：§6 的真正 minimal q-core 分別有 c=3、c=2。

## 2. 原圖逐邊 minimality 的充要條件

以下集合均在 q 下。定義

\[
 J_C=F_C\setminus\bigcup_{D\in C_r,\,D\ne C}F_D.
 \tag{4}
\]

在 §1 的實際來源與 degree 規格下，**G 是 minimal q-core iff 存在
同一 c∈U，使每側同時滿足**：

1. q 在 S_r 上互異，且 c∈A_r；
2. 所有 F_C 的聯集恰為 A_r∖{c}；
3. 每個原 C 的 J_C 非空。

必要性：式 (3) 先給 A_r∩⋃F_C=A_r∖{c}。刪 root-spoke rb_i 時，
若其 q 色在另一 spoke 重複，root list 不變，不可能使拒絕轉為接受。
所以 spokes 異色。刪除後 root 必用唯一新色 d=q_i，另一 root 的完整
residual 仍為 {c}；同側所有 unary 都須接受 d。逐條 spoke 如此，得到
每個 F_C⊆A_r。聯集於是恰等於 A_r∖{c}。

由 [degree-4 分量解除](c5_adjacent_degree5_interfaces.md#4-degree-4-的-tightness共鄰點與分量解除)，
刪任一至少一端在 C 的原邊，會解除**整個原 C 區域**的 root 約束。
其他 C、另一 root 與原 zw 仍保留。此時 r 的可用色恰為 {c}∪J_C，
其中 c 被 zw 擋住，故 minimality 等價於 J_C≠∅。

充分性：以上三條使兩側 E_r={c}，故 G 拒絕 q 而 G−zw 接受。
各類刪邊的完整有序 root 關係如下，均非空：

| 被刪原邊 e | G−e 的完整 q root 關係 |
| --- | --- |
| zw | {(c,c)} |
| zb_i | {(q_i,c)} |
| wb_i | {(c,q_i)} |
| 任一 e∈E_C，C∈C_z | J_C×{c} |
| 任一 e∈E_C，C∈C_w | {c}×J_C |

E_C 包括 C-root、C-boundary、內部 bridge 與非 bridge 邊。C−e 即使
分裂，也仍以原 C 為一個被解除區域。每份刪後完整染色的被刪兩端
必同色，否則可加回原邊；此端點強迫適用表中每個可用色對。

這是**給定實際來源**的充要式；任意抽象 F 表滿足它，不表示有來源圖。

## 3. 每側恰一單位的容量缺額或重疊

令 t=|S_r|、n=Σk_C=4−t=|A_r|。式 (3)–(4) 給

\[
 \left|\bigcup_C F_C\right|=n-1,\qquad
 |C_r|\le n-1.
\]

q 只用三色，故 t≤3、n≥1；原 H 連通且每個分量接一側。
t=3 會有一個接點卻無私有色，矛盾。所以 **每側 t≤2**，亦不能全為
單接點分量。定義

\[
 d_r=\sum_C(k_C-|F_C|),\qquad
 o_r=\sum_C|F_C|-\left|\bigcup_C F_C\right|.
\]

每項非負，且有精確恆等式

\[
 \boxed{d_r+o_r=1.} \tag{5}
\]

若 d_r=1，恰一份 C 少禁一色，其他分量達到 |F_C|=k_C，且所有禁色
集合兩兩不交。若 o_r=1，所有分量飽和，恰一個色被兩份分量共用，
其餘色只出現一次；那兩份分量各還需私有色，所以各至少二接點。
Σk_C≤4 遂強迫 t=0、分拆 (2,2)，兩份 F 均大小二、交集一色。

由 (5) 及私有色非空，得到完整必要表。h、k、ℓ 都是同一側
A_r∖{c} 中互異的字面顏色；對等大小分量仍保留具名次序。

| t | 接點分拆 | 各原分量的 F，允許表內角色排列 | 類型 |
| ---: | --- | --- | --- |
| 2 | (2) | {h} | 容量缺額一 |
| 1 | (3) | {h,k} | 容量缺額一；§4 排除 |
| 1 | (2,1) | {h}、{k} | 容量缺額一 |
| 0 | (4) | {h,k,ℓ} | 容量缺額一；§4 排除 |
| 0 | (3,1) | {h,k}、{ℓ} | 容量缺額一；§4 排除 |
| 0 | (2,2) | {h,k}、{ℓ}，或反序 | 容量缺額一 |
| 0 | (2,2) | {h,k}、{k,ℓ} | 重疊一；私有色 h、ℓ |
| 0 | (2,1,1) | {h}、{k}、{ℓ} | 容量缺額一 |

兩側只能以**相同 c** 接合；不將兩側顏色各自正常化成不同的 c。

## 4. 經原 zw 的外部路徑與平面篩選

先證每個 unary C 實際碰 B。它的 F_C 非空且不含 c，故是 U 的
非空真子集。若 C 不碰 B，其完整接點關係在整份 coloring 的 S4
置換下不變，F_C 亦不變；U 的不變子集只有 ∅、U，矛盾。
T_C 非空已由 slack 證明，沒有以空 relation 的交集假裝禁色。

固定 C∈C_r，令 s 為另一 root。§3 給對側至少一份 unary D；取 D
的原 s-contact、D 內簡單路徑及 boundary 附件，接上原 rs，得到

\[
 Q=r\,s\,x_0\cdots x_m\,b_j,
 \quad x_i\in D.
 \tag{6}
\]

也可在 s 有 spoke 時直接取 Q=r s b_j。內部全部避開 C、B，
B∪V(Q) 是避開 C 的連通外部集合。這不把 D 併入 C，不改 R_D，
不新增 r-spoke，也不把原 rs 收縮後的圖當作來源。

現在加上 **G 平面**，不要求 B 為外面或接受 T4。固定 d∈F_C，
拒絕的 residual lists 逐點至少 deg_C，故處處 tight。
[Dvořák Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
給同一 C 的 Gallai 結構與 blockwise-uniform palettes；本輪已重讀。

將 (6) 代入 [外部 hub 引理](c5_no_spoke_exterior.md#3-以另一分量恢復-k4-的外部-hub)：
若 C 有 K4 block，其四條實際外接 tethers 到 B∪{r}，經同一
B∪V(Q) 接成第五個 branch set，得到原 K5。因此各 C 都 K4-free。
前報告的 Q 走另一同-root 分量，本輪 Q 走原 rs 與另一側 D；
所需前提同為「Q 避開 C、以原邊連 r 到 B」，沒有其他替換。

三接點且至少兩禁色時，沿用
[三接點 active triangle](c5_single_spoke_three_one.md#2-三個葉點迫使唯一-triangle-加三臂)
與其原 boundary tethers。三條完整 arms 為 V0,V1,V2，
取 Z={r}，O=B∪(V(Q)∖{r})∪全部截尾 tethers。
V_i 兩兩由 triangle 邊相鄰，Z–V_i 是原 contacts，V_i–O 是
原 tether 首邊，Z–O 是**原 rs**。五組給 K5。

四接點且至少三禁色時，沿用
[三份 palettes 共同結構](c5_single_spoke_four.md#3-四葉共同樹恰為兩-triangle-加一條-bridge)：
原兩 triangle {a,b,x}、{d,e,y} 以 xy 連接，四 contacts 為 a,b,d,e。
取 {a}、{b}、{x}、Z={r,d,e,y} 及上述 O（使用左 triangle 的 tethers）。
Z–O 仍由原 rs 給出，其餘九鄰接同既有 minor。故亦非平面。

因此 §3 的 (3)、(3,1)、(4) 側皆排除。任意大小平面來源每側只剩

\[
 \boxed{t=2:(2),\quad t=1:(2,1),\quad
        t=0:(2,2)\text{ 或 }(2,1,1).} \tag{7}
\]

這是必要分拆與完整禁色限制；沒有證表中配置的 disk 實現，也沒有
使用 C5 的環序來配製兩側互相獨立的支援。

## 5. 任意列及固定來源多步刪邊的界線

對任意 β，式 (2) 精確給出

\[
 \beta\notin\Sigma(G)\iff E_z(\beta)=\varnothing\ \lor\
 E_w(\beta)=\varnothing\ \lor\
 E_z(\beta)=E_w(\beta)=\{d\}\text{ for some }d.
 \tag{8}
\]

無 mixed 的容量下界只是 |E_r(β)|≥0；不能套用共鄰 singleton 型的
非空結論。q 下的 (3)／私有色也不能直接搬到 p₁、p₂。

對任意已刪非外圈邊集 J，令

\[
 E_r^J(\beta)=A_r^J(\beta)\setminus
 \bigcup_{C\in C_r:\,J\cap E_C=\varnothing}F_C(\beta).
\]

保留原分量身份，則 G−J 的完整 root 關係是 E_z^J×E_w^J，若
zw∉J 再刪 Δ。刪邊碰到某原 C 就解除它，未碰到的 C 繼續用同一
原關係；root lists 則按剩餘實際 spokes 計算。這不是跨來源的可合併 state。

下一窄研究入口可先取 **t_z=t_w=2、兩側 (2)**：兩組原 spokes、
各二接點 unary 的單禁色及同一 c 已固定，保留原 zw 與兩份完整
relation，推導 disk 中的實際支援／rotation，再研究 (8) 的指定 p。
其餘四型組合、多 mixed／較大 mixed、一般出口與 K∞=K≤5 仍保留。

## 6. 有限控制、證書與驗證

[Checker](../scripts/c5_adjacent_degree5_no_mixed.py)、
[JSON](../artifacts/c5_adjacent_degree5_no_mixed/observations.json) 與
[正常形表](../artifacts/c5_adjacent_degree5_no_mixed/normal_forms.md) 分層保存：

- 256 組任意 E_z、E_w（包含空集）核對 (3)、(8)。2,502 份單側候選
  包含空禁色、重複 q-spokes 及 A 外禁色；10,008 次固定對側 c 的
  獨立刪邊判準核對 §2，留下 149 份正常形及 149 次共同反射控制。
- 保留 root 的具名 boundary 子集、各原 unary 的具名欄位及共同色框。
  149 份側資料以同一 c 接成 5,647 份有序雙側必要資料；§4 排除
  31 份側型，剩 118 份側資料／3,548 份雙側資料。其中 t_z=t_w=2
  有 88 份。這些沒有 unary 實際支援或環序，不是來源圖數量。
- 兩張真正 degree=(5,5,4,…) 的 minimal q-core：一張每側 t=2、
  三角形 unary 單禁色，c=3；另一張每側兩份 unary K2，禁色
  {0,3}、{1,3} 重疊，c=2。各自有 23、29 份逐邊完整染色及
  明列原 K5 minor，所以都是**非平面**控制。全部 480 proper-row
  接合皆與獨立全圖回溯相符，保存 q 的完整接點 tuples。
  六份局部 relation 的 marginals 相乘皆會錯失禁色。
- 400 份具名原外部路徑 minor 子圖：320 份 K4 hub、60 份三接點、
  20 份四接點；明列原 zw、經 w 到 B 的路徑、全部 branch sets
  及十條鄰接。刪 zw 後這 400 份**指定 witness**皆失效；未宣稱
  刪後圖平面。有限長度／附件選取不替代任意大小的原路徑證明。

target 分離查詢為零；固定非平面圖的 480 列僅是公式控制。
外部定理只用於 §4 的結構／minor 篩選，§1–3、5 不依賴它。
未新增 Lean theorem，未把必要資料稱為 disk 可實現性或完整 Σ 證書。

```bash
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_adjacent_degree5_shared_singleton.py --check
python3 scripts/c5_no_spoke_exterior.py --check
python3 scripts/c5_single_spoke_three_one.py --check
python3 scripts/c5_single_spoke_four.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證與省略範圍見 [當輪紀錄](history/2026-09-29-adjacent-no-mixed.md)。
`lake build` 只確認既有專案可建置，不表示本輪紙面化約／minor 已形式化。
