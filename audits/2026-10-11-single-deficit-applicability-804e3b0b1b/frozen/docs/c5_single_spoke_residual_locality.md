---
docgraph:
  id: c5.single-spoke-residual-locality
  family:
    - c5
    - c5.single-spoke
  requires:
    - c5.single-spoke-first-bridge
    - c5.single-spoke-branch-palettes
    - c5.single-spoke-frame-arc
---
# Single-spoke (2,2)：局部 residual 相同列引理與 record 90 延拓

後續（2026-09-28）：[(3,1) 三接點排除](c5_single_spoke_three_one.md) 已完成
下文的下一入口；active triangle／三臂及唯一 spoke 給來源 K5，未 Lean 化。
(2,2) 計數不變；最新窄問題是 (4) 的三份拒絕 palettes，見 HANDOFF。

2026-09-28，接手基準 `2de13f7`。研究優先序見 [HANDOFF](HANDOFF.md)。

**record 90 的 p₂=01212 必延拓，record 282 由交換原分量搬運。**
首橋 β=0 的兩端若不接 b2，source 與 target 在整個路徑塊上的 boundary
lists 相同，局部 residual 就必相同；但兩者分別是 {0,1}、{1,2}。
因此兩端各必接 b2，連同既有的 b3 接線給原圖 K5 minor。

本輪新增 **2 個指定列延拓、0 筆來源排除**。累計來源排除仍為 278 筆；
保留 **102 筆／51 個交換型全部雙列已證，0 個表內查詢未決**。
結合任意大小必要覆蓋，完成明列前提下的 (2,2) 指定雙列分離。
保留型可實現性、完整 Σ 及其他 single-spoke 分拆仍未證。
證據為紙面歸納＋沿用外部 degree-list 定理＋Python 有限控制；未新增 Lean theorem。

## 1. 完整前提及既存證書

G 有限簡單，B=(b0,…,b4) 是 induced-C5 disk 外框，有效內部 H 連通。
G 是 edge-minimal q=01012 obstruction；唯一完整 degree-5 點 z 的唯一
boundary spoke 為 zb_s，其餘有效內點完整 degree=4。H−z 恰有 C0、C1，
各保留兩個不同原有序接點 (u_k,v_k) 及全部實際 boundary 支援 S_k。
套表時另要求 G 接受全部四色 boundary patterns T4。U={0,1,2,3}，
p₁=01021、p₂=01212；完整接點關係 R_k(t) 的每個 tuple 來自同一 C_k coloring。

沿用 [(2,2) 必要分類](c5_single_spoke_two_two.md) 的精確接合：

\[
F_k(t)=\bigcap_{a\in R_k(t)}\operatorname{set}(a),\qquad
Z_G(t)=(U\setminus\{t_s\})\setminus(F_0(t)\cup F_1(t)).
\]

record 90 有 s=0、(S0,S1)=(0234,012)、(F0(q),F1(q))=({1},{2,3})。
p₁ 已證；[首橋層](c5_single_spoke_first_bridge.md) 保存全部拒絕候選及既有
反證，p₂ 只剩 (F0(p₂),F1(p₂))=({1,2},{3}) 尚未排除。
下文以此候選反設，始終取同一 C=C0。

拒絕 (q,z=1)、(p₂,z=1)、(p₂,z=2) 各提供一份 tight blockwise-uniform
palette 證書。存在性沿用 [Dvořák 講義 Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
（本輪重讀核對）：連通圖、degree lists 及不可著色已足夠，不需要 target
minimality。K4-free 化約與 bridge／odd-cycle 結構沿用既有報告。

target pair 給兩原接點間的奇數長原 bridge 路徑 P=(x0=u,…,xℓ=v)，ℓ≥1。
刪去全部 P 邊，令 W_j 為含 x_j 的原連通分量，包含其全部旁支；T_j 是
W_j 的全部實際 boundary 支援，**包含 root 自身的直接附件**。
對 t=q,p₂，令 D_j^t=t(N_B(x_j))，Q_j^t 是 root 所有路徑外 palettes 的聯集，
E_j^t=U\(D_j^t∪Q_j^t)，尚未扣除 z 色。

首橋層已證 E_j^{p₂}={1,2}；對 j=0,1 有同一份

\[
E_0^q=E_1^q=\{1,\beta\},\qquad\beta\in\{0,2\}.
\]

β 來自同一原邊 x0x1 的 q palette，不逐端或逐列選擇。
端點公式包含既有 tightness 對被扣 z 色的補回；ℓ=1 時 x1 是另一接點，
ℓ≥3 時是內點，兩種情況均已涵蓋。此處 E_j^q 不是 F_C(q)={1}。

## 2. 同一路徑塊的相同列引理

**引理。** 在上述同圖 palettes 存在的條件下，若兩列 t、r 在 T_j 上逐點
相同，則 E_j^t=E_j^r。不要求 t、r 的整分量 F 都是 pair，也不要求兩份
root 完整 lists 相同。

證明：每個旁支非 root 點都沒有 z 邊，也不含另一個原接點。它的全部
boundary 鄰居屬於 T_j，所以兩列給它相同 lists。對有限 rooted block tree
由葉向 root 歸納：任一 block 的非 root 頂點，其 list 扣除已確定的後代
palettes，就決定該 block 的 palette。bridge 至少有一個、odd cycle 至少
有兩個非 root 頂點；既存證書確保不同選點所得相容。因此兩列的全部
旁支 palettes 相同，Q_j^t=Q_j^r。這是
[rooted-palette 唯一性](c5_single_spoke_branch_palettes.md#2-rooted-palette-唯一性與固定色守恆)
的同列特例，不需旁支大小或深度上限。

root 的直接 boundary 接線也包含於 T_j，故 D_j^t=D_j^r。代入 E 的定義
即得結論。root 的 z 色及路徑 block palettes 不參與此歸納，不能將 root
完整 list 取代 E。若 W_j 無旁支，Q_j^t=Q_j^r=∅，論證仍成立。

**差異支援推論。** 若 E_j^t≠E_j^r，則 T_j 必碰兩列的差異位置集
Δ(t,r)={i:t_i≠r_i}。它只是一個必要條件，不聲稱碰 Δ 就足以實現 palettes。

## 3. record 90 的兩個共用 β

q、p₂ 只在 b2 不同，故 Δ(q,p₂)={2}。在 β=0 時，對 j=0,1，
E_j^q={0,1}≠{1,2}=E_j^{p₂}，引理迫使 **b2∈T_j**。
首橋層原本已迫使 b3∈T_j；因此兩端都實際接 b2、b3。

| 共用 β | 原容許 T_j | 加入相同列引理後 | 兩端必接對 |
| ---: | --- | --- | --- |
| 0 | 23、023、034、234、0234 | 23、023、234、0234 | b2、b3 |
| 2 | 34、034、234、0234 | 同左 | b3、b4 |

β=0 唯一刪掉的 034 上，兩列完全相同，卻要求不同 E，故不可能。
β=2 兩份 E 相同，不靠新引理刪支援；沿用首橋穩定子所給的 b3、b4。
沒有把 q 色 0 的 b0／b2 供應點直接指定為 b2，而是用同圖跨列相容性
排除另一種供應方式。

令 {a,b} 分別為 {2,3} 或 {3,4}，J=P∪{zu,zv}。五個 branch sets 取

\[
A=W_0,\quad A'=W_1,\quad X=\{b_a\},\quad Y=\{b_b\},\qquad
Z=(V(J)\setminus\{x_0,x_1\})\cup(B\setminus\{b_a,b_b\}).
\]

W0、W1 是互不相交的原連通分量；J 刪掉相鄰 x0、x1 後餘部經 z 連通，
ℓ=1 時為 {z}。兩種補弧分別 b1–b0–b4、b0–b1–b2，均包含 b0，原 spoke
zb0 使 Z 連通。五組兩兩不交，且十條鄰接如下：

| branch-set pair | 原圖 witness |
| --- | --- |
| A–A' | 首橋 x0x1 |
| A–Z、A'–Z | J 上兩條朝外的邊；端點時為原 z 接點邊 |
| A／A'–X／Y | 兩塊各自到兩框點的四份實際附件 |
| X–Y、X–Z、Y–Z | 原 C5 的框邊 |

故兩個 β 均給原圖 K5 minor，與平面性矛盾。旁支到兩框點的路徑可在同一
W 內共用內點，因整個 W 屬於同一 branch set；兩個 W 仍不相交。
沒有重選接點、修改附件、混合不同來源圖或刪旁支來改寫完整關係。
唯一剩餘拒絕候選被排除，record 90 的 p₂ 延拓；交換 C0、C1 得 record 282。

## 4. 完整表與條件式出口的接合

[新 checker](../scripts/c5_single_spoke_residual_locality.py) 以首橋 artifact
及原 (2,2) 表為只讀輸入，核對 SHA256，保存所有原記錄、完整 relation
schemas、slit lifts、contact words、反射及前層 target 證據。只處理原來
兩個未決查詢，重算完整 F 候選接合，36 組中繼承 34 組反證、新排除 2 組。
每個 β 都排除、每份完整候選都排除後才接受 target；來源 ID 集保持不變。

原 T4 保留 380 筆中，278 筆來源已有排除，其餘 102 筆如今全部接受兩個 p。
任意大小的 actual-support／ordered-relation 覆蓋及反射來自必要分類，
因此**符合 §1 前提且接受 T4 的 (2,2) 來源皆接受 p₁、p₂**。
這是指定列分離，未求出其餘 boundary rows 的完整 Σ。

在 [single-sided exit](c5_single_sided_exit.md) 的額外來源假設
Σ(G)=Ω\{p,q} 下，若選出的 minimal q-core 屬於本類，刪邊繼承接受列，
且本定理給 p 延拓，才可推得該核心恰只缺 q，接上既有第一個 strict
deletion 的出口證明。此結論也適用既已完成的 (2,1,1) 分支；不能只從
T4 acceptance 宣稱任意來源完整單缺失。

## 5. 控制、重播與精確停止點

- 1,944 個 list／後代 palette 扣除與四色置換的歸納步控制；250 個
  root 直接附件／旁支聯集的同列 residual 控制。
- 32 個 record 90 支援／β 控制：全部 16 個 T⊆0234、兩個 β，各以
  24 色置換核對前層兩份穩定子，再核對局部同列條件與具名必接對。
- 576 份 K5 skeletons：兩種必接對、奇數長度 1–17、16 種雙端 tether
  形狀及反射；逐份保存原邊、實際路徑、五組與十條鄰接。
- 13 個負控制：局部列不同／residual 相同時不得誤刪、root 接線不可漏、
  E/F 區別、舊 singleton guard、部分候選不能結案，以及缺原邊／附件／
  框連通／branch-set 不交性的錯誤。
- 逐候選核對 90／282 的分量交換；反射保持**字面 target 色列**、β、E、
  支援與框弧，反射側不重複計數。

資料見 [JSON](../artifacts/c5_single_spoke_residual_locality/observations.json)
及 [完整套用表](../artifacts/c5_single_spoke_residual_locality/support_table.md)。
無參數僅生成新層；`--check` 重算並逐 byte 比對。

```bash
python3 scripts/c5_single_spoke_residual_locality.py --check
python3 scripts/c5_single_spoke_first_bridge.py --check
python3 scripts/c5_single_spoke_two_arc.py --check
python3 scripts/c5_single_spoke_cross_row.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
python3 scripts/c5_single_spoke_two_two_external.py --check
python3 scripts/c5_single_spoke_two_two_minor.py --check
python3 scripts/c5_single_spoke_two_two.py --check
python3 scripts/c5_single_spoke_bridge_path.py --check
python3 scripts/c5_single_spoke_branch_palettes.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際檢查及沿用範圍見 [研究紀錄](history/2026-09-28-residual-locality.md)。
有限 skeletons 不滿足整份 degree/list 來源條件，不能當作實現證書；任意
大小結論由既存 palettes、rooted-block 歸納與原圖 branch sets 承擔。
`lake build` 通過不將上述新紙面證明形式化。

下一個窄方向為 **single-spoke (3,1)**：F₃(q)=A\{c}、F₁(q)={c}，
A=U\{q_s}。先保留三個原有序接點，研究兩份拒絕證書在連接三接點的
最小 block subtree 上可有的第一個分叉／odd-cycle block；其餘旁支與
單接點分量完整保存。二接點奇數 bridge 路徑定理不能直接套到三接點。
先證任意大小的必要結構，再做有限證書，不重開 (2,2) 圖枚舉。
其餘 (4)、t=0、更高 degree、多 degree-5、一般核心存在／分離、共同
出口與 `K∞=K≤5` 均仍開放。
