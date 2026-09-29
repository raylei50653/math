# 無 mixed E–E：六份正跨度排除全部 disk 來源

後續（2026-09-29）：[B–C 原路徑與雙列分離](c5_adjacent_degree5_no_mixed_bc.md)
完成 t_z=1,(2,1)，t_w=0,(2,2)、D_w=1、O_w=0 及 root 交換型。
608 份必要支援中 584 份 source K5 排除，保留 24 份的 48 個 target 全接受。
累計九類／2,036 份覆蓋，六類／1,512 份保留；下文保留當輪語境，
目前入口見 [weak-deletion 導覽](c5_weak_deletion_guide.md)。


2026-09-29，Git 基準 `47ebbbc`，接續工作區已有的
[B–E 結果](c5_adjacent_degree5_no_mixed_be.md)。E–E 指兩側皆為
**t=0、接點分拆 (2,1,1)**。本型六個原分量各有正支援跨度，
同一 C5 disk 的總跨度卻至多五，故 **不存在本型的 minimal q-core**。
原 144 份必要接合全部作來源排除，必要支援零份，target 查詢零次。
不需 T4，不限制原分量大小；不是把空纖維記成 288 個 target 接受。

證據為任意大小紙面證明、沿用外部 degree-list 定理及 Python 固定域
證書，未新增 Lean theorem。一般單側／共同出口、任意來源完整 Σ、
一般交換機制完備性與 `K∞=K≤5` 仍未證。
目前停止點及下一窄入口由 [weak-deletion 導覽](c5_weak_deletion_guide.md) 維護。

## 1. 同一來源、六原分量與完整關係

M 有限簡單，B=(b0,…,b4) 是 induced C5 disk 外框，H=M−B 非空連通。
固定 U={0,1,2,3}、q=01012；M 拒絕 q，刪任一非框邊後接受 q。
相鄰 roots z、w 完整 degree=5，其餘內點完整 degree=4；H−{z,w}
無 mixed，兩 root 都無 boundary spoke。兩側原分量依次為
(C_z,D_z,E_z)、(C_w,D_w,E_w)，接點數各為 (2,1,1)。
以 Cz_0、Cz_1、Dz_0、Ez_0、Cw_0、Cw_1、Dw_0、Ew_0 記八個具名
接點；保留原 zw、全部內部 bridges／旁支、實際 boundary 附件及共同色框。
下文用 R_r 表 root residual，以免與原分量 E_r 混淆。

對同一原分量 C，T_C(q) 是保留其全部內邊及 C–B 邊的完整有序接點
關係，F_C(q)=交集_{τ∈T_C(q)} set(τ)。接點 slack 給 T_C(q) 非空。
[原 no-mixed 化約](c5_adjacent_degree5_no_mixed.md) 給共同 c，使

\[
R_z(q)=R_w(q)=\{c\},\qquad
(F_{C_r},F_{D_r},F_{E_r})(q)=(\{a_r\},\{d_r\},\{e_r\}),
\quad (a_r,d_r,e_r)\in\operatorname{Perm}(U\setminus\{c\}).
\]

兩側 source (D,O,κ)=(1,0,0)，分量缺額皆 (1,0,0)。共有
4·6·6=144 份有序必要接合；不商掉 D_r、E_r 的身份。
Checker 直接重建此集合，逐筆對回原 retained-join ID、兩側 IDs 及完整
side 記錄；首筆 join=1428、sides=(64,64)、c=3，兩側禁色均 (0,1,2)。
Binary 關係沿用逐座標 release witness 的每禁色 95 個完整 schemas，
四個單接點關係各恰為 {(d_r)} 或 {(e_r)}。證書保存完整 schema 表，
而非將二接點 marginals 相乘；這些必要 schemas 不宣稱可獨立實現。

## 2. 無 spoke 仍有原外部路徑

先不使用 K4-free 或跨度。每個 F_C 是非空 singleton。若 C 不碰 B，
整份 T_C(q) 在全部 S4 色置換下不變，F_C 也必不變，矛盾。
所以六份原分量各自都有實際 boundary 附件。

對任意 C 屬 r 側，令 s 為另一 root。取**另一側**原 D_s 的具名
contact、D_s 內通往任一實際 boundary 附件的簡單路徑，得到

\[
Q_C=r\!-s\!-(Ds_0)\ \cdots\ b_j.
\]

其首邊是原 rs，內部除兩 root 外全部在 D_s，首次抵達 B 即停止；
故 Q_C 避開 C。對 z 側三份可固定用 D_w，對 w 側三份用 D_z。
只需要逐 C 存在此路徑，不要求六條 Q_C 彼此不交。
這沿用 [no-mixed §4](c5_adjacent_degree5_no_mixed.md#4-經原-zw-的外部路徑與平面篩選)
的實際路徑，沒有增加 root-spoke、合併原分量或改變任何完整關係。

固定 root 色 a∈F_C(q)。原 C 的 residual lists 至少為 deg_C，且拒絕
著色。[Dvořák 的 Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
給處處 tight 與 Gallai tree 結構。將 Q_C 代入既有外部 hub 引理，
原 K4 block 的四條外向 tethers 可接入避開 C 的連通集合 B∪V(Q_C)，
造成原 K5 minor，與平面性矛盾。K5 block 也不可能：其各點內度已達四，
無法再接任何外邊，會使整個 C 無 root 接點；更大 clique 超出 degree 四。
因此 C 是 K4-free Gallai tree。
這使用既有任意大小 K4 排除，不新增有限 minor skeleton。

令 S_C=N_B(C)。若 q(S_C) 只含色 d，固定 d 的色置換迫使 singleton
F_C={d}。再令 root=d，所有外鄰都用 d。Tightness 迫使每點至多有
一個外鄰：有外鄰時 list 大小為三，故內度必為三；沒有外鄰時內度四。
所以 min deg_C≥3。但 K4-free Gallai tree 的葉塊有私有點內度≤2；
若 C 只有一個 block 或一個頂點，同樣有內度≤2 的點。矛盾。
因此 **每份 q(S_C) 至少兩色，S_C 至少兩個不同框點**。

## 3. 同源環序與六大於五

取原 zw 的細閉正則鄰域 N。其外側至 B 是 annulus，沿 ∂N，z、w
各四條外部 incidences 成一段。每個 binary C_r 的兩個 contacts
在該段必連續：原接點間簡單路徑加兩條 root 邊形成 Jordan 曲線；
不含 B 的一側不能夾住另一 incidence，因另一原分量可在自身內走到 B，
而原 zw 亦可經另一側原分量走到 B，全避開當前 C_r。

故必要 cyclic word 為

\[
\operatorname{perm}(C_z,D_z,E_z)\,
\operatorname{perm}(C_w,D_w,E_w),
\]

保留兩個 binary 各自的兩個接點方向。以 C_z 起頭，得到 36 個具名
cyclic words、144 份 contact rotations，不商掉反射或單接點交換。

六個原連通分量皆連接 annulus 兩側，內部兩兩不交。在同一框點的
小鄰域可分開附件來讀取次序，但保留原框點及其色。沿用
[原 annulus crosscut 引理](c5_adjacent_degree5_no_mixed_t2_t1.md#3-原-zw-鄰域的六單位次序)：
同一分量內連接外端的 crosscut 切下不含內圓周的區域，不能容納
另一分量的外端，因後者還要連回內圓周。因此所有 actual supports
能在同一循環次序提升成 T_j⊂Z，滿足

\[
\max T_j\le\min T_{j+1},\qquad
\max T_5\le\min T_0+5,\qquad T_j\bmod5=S_j.
\]

不同分量可共享端點，不能重用開框邊；支援可以稀疏，不先填成整弧。
其餘分量有正跨度，故任何一份不可能繞滿一圈。由 §2，各
ℓ_j=max T_j−min T_j≥1，遂

\[
\boxed{6\le\sum_{j=0}^5\ell_j\le5,}
\]

矛盾。這排除所有滿足 §1 的任意大小 disk 來源，不只是排除某個有限
block／bridge 模板。外框是 disk 邊界為必要前提，未宣稱一般 planar C5
同樣排除；亦未使用 p₁、p₂ 的 target 拒絕假設。

## 4. 固定域證書、控制與覆蓋

[Checker](../scripts/c5_adjacent_degree5_no_mixed_ee.py)、
[JSON](../artifacts/c5_adjacent_degree5_no_mixed_ee/observations.json) 及
[逐 ID 排除表](../artifacts/c5_adjacent_degree5_no_mixed_ee/exclusion_table.md)
保存 144 份來源、原側記錄、六分量／八接點、原外部路徑角色、完整
binary schemas、四 unary 關係、36 個 words 及 144 個 rotations。

- 第一算法列舉所有稀疏正跨度 lifts，得到零份 C5 placements。
  第二算法用互不交的非空 cyclic hull-edge masks；它甚至放寬了兩 root
  次序及 q 色限制，仍無法放入六份，故真實必要域必空。
- 六邊框控制：ordered lifts 有 216 份；放寬次序的 masks 有 720 份。
  五邊框放五份正跨度單位有 120 份 mask packings。這些只驗證幾何域，
  不是度數／lists 的來源圖，也沒有把 C6 當成 C5 研究結論。
- 分別將 Dz、Ez、Dw、Ew 誤降成零跨度單位，每次會得到 180 份 C5
  placements。保存四個見證，核對單接點原分量不可當作 root-spoke。
- 從 65,535 份非空 binary relations 重核 380 份完整 schemas；另保存
  marginals 失真控制。144 次整來源 root 交換、144 次 q-preserving
  反射、576 次具名單接點交換與 3,456 次共同色框 q 接合均核對。

原接合 IDs 全分為 `no_disk_source_six_positive_spans`，不是 target 接受。
144 個新增 IDs 與 B–E 累計的 1,532 個不交，累計 **八種 root 交換型／
1,676 份覆蓋，七類／1,872 份保留**。其餘為 B–C、B–D、C–C、C–D、
C–E、D–D、D–E；證書逐類保留全部 IDs。下一窄入口綁定 B–C 的
180 份有序資料，但本輪未建立它的支援或 target 結果。
舊 checker／artifacts 不改寫。

## 5. 出口與驗證界線

[出口第九類](c5_single_sided_exit.md) 可加入 E–E 的來源排除分支：
實際 minimal q-core 不會落在本型，不能聲稱產生了新的 target 著色。
其他已分離型的完整 Σ 接合仍須來源雙缺失與刪邊繼承；本輪未移除該前提。

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_ee.py --check
PYTHONHASHSEED=17 python3 scripts/c5_adjacent_degree5_no_mixed_ee.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_be.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證與未重跑範圍見 [當輪紀錄](history/2026-09-29-adjacent-no-mixed-ee.md)。
`lake build` 不表示新 Jordan／Gallai 證明已形式化；本輪未新增 Lean
theorem，沒有獨立第二審稿者。成果保留在工作區，未 commit／push。
