---
docgraph:
  id: c5.no-spoke-first-bridge
  family:
    - c5
    - c5.no-spoke
  requires:
    - c5.no-spoke-path-minor
    - c5.single-spoke-first-bridge
    - c5.single-spoke-branch-palettes
---
# No-spoke (2,2,1)：首橋、固定框弧與指定雙列完成

2026-09-28，接手基準 `60b98ee`。從 record 84／p₁ 推進；研究優先序見
[HANDOFF](HANDOFF.md)。

**record 84 的 p₁ 必延拓；(2,2,1) 保留的 116 筆必要配置全部接受
p₁=01021、p₂=01212。** 首橋共用 β 關閉四個查詢，再將具名框點改為
同一份連通框弧，關閉其餘八個。新增 **12 個延拓、0 筆來源排除**；
來源排除仍為 500 筆，表內未決查詢由 12 降為 0。

結合任意大小必要覆蓋，完成唯一 degree-5 的最後 t=0 分支，接回
[條件式單側出口](c5_single_sided_exit.md#3f-no-spoke-221-與唯一-degree-5-完成)。
一般出口仍須處理 degree≥6 或至少兩個 degree-5 的核心。
證據為紙面歸納／原圖 minor、外部 degree-list 定理及 Python 控制；
未新增 Lean theorem，未證必要配置可實現或任意 T4 核心的完整 Σ。

## 1. 前提、完整關係與原路徑塊

G 有限簡單，B=(b0,…,b4) 為 induced-C5 disk 外框，有效內部 H 非空連通。
G 為 edge-minimal q=01012 obstruction，唯一完整 degree-5 點 z 沒有
boundary spoke，其餘有效內點完整 degree=4。H−z 的具名原分量
(C₀,C₁,C₂) 有 (2,2,1) 個接點；S_k 是全部實際 boundary 支援。
套表及最後的指定雙列定理另假設接受全部 T4。

原五接點、各二接點的有序座標、全部旁支、附件、bridges 與環序均保留。
R_k(t) 的每個 tuple 來自同一 C_k 完整著色；忽略 z 的接點 slack 保證
R_k(t) 非空，並有精確接合

\[
F_k(t)=\bigcap_{a\in R_k(t)}\operatorname{set}(a),\qquad
Z_G(t)=U\setminus\bigcup_k F_k(t),\quad U=\{0,1,2,3\}.
\]

接合先固定同一列、同一 z 色，再各選完整 tuple；不使用 endpoint marginals。
沿用 [外部連通](c5_no_spoke_exterior.md)，各 C_k 都 K4-free Gallai tree。
每個 d∈F_k(t) 給不可著色 degree lists；
[Dvořák 講義 Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
給 tightness 與 incident palettes 的不交聯集。本輪重新核對原文：
連通、degree assignment 與拒絕已足夠，不需 target minimality。

若 F_k(t) 是 pair，既有 [雙禁色化約](c5_no_spoke_path_minor.md#1-前提完整關係與共用路徑塊)
給兩原接點間的奇數 bridge 路徑 P=(x₀,…,x_ℓ)，ℓ≥1。
刪去全部 P 邊得原路徑塊 W_j，保留 root x_j、全部旁支及實際支援 T_j。
T_j 包含 root 的直接 boundary 附件；W_j 連通且兩兩不交。
令 D_j^t 為直接 boundary 色，Q_j^t 為旁支 palettes 聯集，
E_j^t=U\(D_j^t∪Q_j^t)。pair 列有 E_j^t=F_k(t)，包括兩端。

## 2. 無 spoke 時的 singleton-source 首橋

取同一 C，F_C(q)={c}、F_C(r)={a,d}，只從 target pair 取得上述 P。
q 的拒絕證書仍在同一原 bridge 上給 singleton palette；不從 q 重選路徑。
令

\[
K=\{h:\forall i\in S_C,\ q_i=h\iff r_i=h\}.
\]

旁支非 root 不含其他接點且沒有 z 邊；兩列 lists 對 h∈K 相同。
[Rooted-palette 歸納](c5_single_spoke_branch_palettes.md#2-rooted-palette-唯一性與固定色守恆)
從非 root lists 扣除後代 palettes，保證 Q 對 h 的 membership 相同。
直接附件同樣守恆，故 E_j^q∩K=E_j^r∩K。
歸納只用同一分量，與 z 有無 spoke、其餘分量數無關。

在 x₀，完整 degree=4 與 (q,z=c) tightness 給 c∉D₀^q；旁支 palettes
也不含 c。若首橋 palette 為 {β}，則

\[
E_0^q=\{c,\beta\},\quad\beta\ne c.
\]

假設 c∈K∩{a,d}。守恆給 c∈E₁^q，同一首橋給 β∈E₁^q；ℓ≥3 時
x₁ 的兩個 bridge palettes 不交且聯集大小二，ℓ=1 時它是另一原接點，
端點等式同樣成立。因此

\[
E_0^q=E_1^q=\{c,\beta\},\qquad
\{c,\beta\}\cap K=\{a,d\}\cap K. \tag{1}
\]

若 c∈K 卻不在 target pair，已在 x₀ 矛盾；c∉K 時不套 (1)。
逐點固定 q(T_j) 的色置換保持局部 E_j^q：旁支唯一性不需 root list，
因此也不需置換固定 z 色。target 的穩定子同時保持 E_j^r。
兩端必屬於**同一 β** 的兩份穩定子容許支援族。
這是局部 E={c,β}，不能換成整分量 F_C(q)={c}。

## 3. record 84 及四個延拓

record 84 有 (S₀,S₁,S₂)=(014,123,34)，q 禁色 ({0},{2,3},{1})。
p₂ 已可取 z=2；p₁ 的七組完整拒絕候選，前層已消去六組，只剩
({0,1},{3},{2})。取 C=C₀，K={0,3}、c=0，(1) 給 β∈{1,2}。

| 共用 β | E₀^q=E₁^q | 首橋兩端各自的容許 T | 兩端必接對 |
| ---: | --- | --- | --- |
| 1 | {0,1} | 01、014 | b0、b1 |
| 2 | {0,2} | 04、014 | b0、b4 |

q 不用色 3，穩定子迫使 residual 內的兩色都出現在 q(T)。q 在 014
的三色各只有一個供應點，直接給上表；target 穩定子同時成立。
不能令第一端只接 01、第二端只接 04，因它們無法支承同一 β。

C₁ 有實際 b2 附件，從其任一原接點取原路徑 L=z…b2，內部完全在 C₁。
β=1 取三框弧 X={b0}、Y={b1}、D_B={b2,b3,b4}；β=2 取
X={b0,b1}、Y={b4}、D_B={b2,b3}。令 J=P∪{zx₀,zx_ℓ}，五組為

\[
W_0,\quad W_1,\quad
(V(J)\setminus\{x_0,x_1\})\cup V(L)\cup D_B,\quad X,\quad Y.
\]

這正是 [原外部路徑 K5](c5_no_spoke_path_minor.md#2-沒有-spoke-的原外部路徑-k5)：
L 將經 z 的剩餘 J 接到補弧，兩塊同接 X、Y，十對原邊鄰接齊備。
第三分量與全部五接點仍在來源中，沒有虛構 spoke。兩個 β 皆矛盾，故 p₁ 延拓。

record 1472 交換 C₀、C₁ 得同證。record 408 的 p₂ 有支援 (234,012,04)、
q 禁色 ({1},{2,3},{0})，唯一候選 ({1,2},{3},{0})；K={1,3}，β=0、2
分別迫使首橋兩端同接 23、34。C₁ 的原路徑到 b0 給同一 K5 論證。
record 1561 交換二接點分量得同證；四項均是 target 反證，不排除來源。

## 4. 同一份三框弧容許不同供應點

**引理。** 取任一 pair 分量的原路徑 P。若有同一份分割
B=X⊔Y⊔D_B，三組皆非空且沿原 C5 連通，首橋兩塊 W₀、W₁ 各自
實際碰 X、Y，而另一原分量有實際附件落在 h∈D_B，則 G 含 K5 minor。
四份 W–框弧附件可使用不同框點。

證明：從外部分量取 L=z…b_h，使用 §3 相同五個 branch sets。
W₀、W₁ 連通不交；J 刪去相鄰 x₀、x₁ 後的餘部經 z 連通，ℓ=1 時
為 {z}。L 在另一原分量並把它接到 D_B。原分量、W、B 的身份保證
五組兩兩不交。三份非空連通 C5 弧之間各有原框邊。

| branch-set pair | 原邊 witness |
| --- | --- |
| W₀–W₁ | 首橋 |
| W₀–Z、W₁–Z | J 的兩條朝外邊，端點時為原 z-contact 邊 |
| W₀／W₁–X／Y | 四份實際附件，供應點可不同 |
| X–Y、X–Z、Y–Z | 三份框弧間的原 C5 邊 |

因此十對相鄰，證畢。Z 內的原外部路徑不必與其餘原接點互斥；所有
使用的外部點均在同一 Z，且不在 C。這是任意長度／旁支的 composed witness。

對容許支援族 𝒯，使用順序是**先選同一份 X、Y、D_B，再驗每個 T∈𝒯
都碰 X、Y，及另一分量碰 D_B**。不逐 T 重選分割；空族另作不可能性。
共同必接點只有一個時，仍可能有這種固定框弧 witness。

## 5. 其餘八項與完整套表

record 127、419 的 pair 分量是 C₁，支援均為 0123；1390、1564
交換二接點分量。剩餘完整拒絕候選的該分量禁色及單列穩定子為

| target | F_C(target) | 每個原路徑塊的實際支援限制 | X、Y、D_B |
| --- | --- | --- | --- |
| p₁ | {1,3} | 必碰 b3，且碰 b0／b2 至少一點 | 012、3、4 |
| p₂ | {2,3} | 必碰 b0，且碰 b1／b3 至少一點 | 0、123、4 |

例如 p₁ 未用 3；要讓 {1,3} 在局部穩定子下不變，支援須見補集的
色 0、2，恰為表中限制。p₂ 同理須見色 0、1。兩列各有六種容許 T。
另一二接點分量的支援是 04 或 34，均有實際 b4 附件。§4 直接給
K5，八項皆延拓。這一步只用 target 單列穩定子，不需 q／target 換色等式。

[Checker](../scripts/c5_no_spoke_first_bridge.py) 以原路徑層 JSON 為只讀輸入，
核對 SHA256，保留 116 個原記錄、整數 lifts、五接點環序與完整 F 候選。
重算 12 個未決查詢的 36 組完整覆蓋：24 組繼承反證，4 組由首橋消去，
8 組由固定框弧消去。每份完整候選都排除後才接受 target。
框弧條件亦在 q 下掃過同一 116 筆，**沒有新增來源排除**。

| 階段 | 保留來源 | 雙列已證 | 未決查詢 | 新增延拓 |
| --- | ---: | ---: | ---: | ---: |
| 原路徑層 | 116 | 108 | 12 | — |
| 同一首橋 β | 116 | 112 | 8 | 4 |
| 固定三框弧 | 116 | 116 | 0 | 8 |

任意大小 necessary-support 覆蓋來自 [環狀支援表](c5_no_spoke_supports.md)，
不是本輪的 skeleton 枚舉。T4 保留 616 筆中 500 筆已有來源排除、其餘
116 筆全接受兩個 p，故完成 §1 圖類的指定雙列定理。
完整 Σ(M)=Ω\{q} 另需出口來源 Σ(G)=Ω\{p,q} 及刪邊繼承；T4 本身不足。

## 6. 控制、重播與停止點

[JSON](../artifacts/c5_no_spoke_first_bridge/observations.json) 與
[完整表](../artifacts/c5_no_spoke_first_bridge/support_table.md) 保存：

- 沿用首橋的 8,748 個固定色歸納步、48 個緊端點及 24 個首橋相容控制；
  32 個本輪首橋支援／β 控制，以全部 24 色置換獨立核對必接對。
- 768 份首橋 minor 及反射：四個具名必接對、長度 1／3／5、16 種雙端
  tether 形狀、外部分量一／二接點及兩種原路徑長度。
- 三弧分割以三個框切口及獨立的 3⁵ 份逐頂點指派核對，共 60 份具名分割；
  32 個剩餘雙列支援控制。另有 768 份 minor 及反射，允許兩塊獨立
  使用不同供應點，保留三個原分量、五個接點與零 spoke。
- 27 個負控制，含獨立 β、E/F 混同、舊 singleton guard、部分候選、
  缺原外部邊／附件／bridge、框弧不連通、重疊 branch sets 及量詞錯置。
- 分量交換與反射保存原接點身份；反射檢查**字面 target 列**、β、residual、
  全部支援與同一份框弧，不僅比較正規化分割。

skeletons 不要求完整 degree/list 來源條件，並非可實現性證書；刪邊負控制
只否定指定 witness，不斷言整圖變平面。無參數生成新層，`--check` 逐 byte 重算。

```bash
python3 scripts/c5_no_spoke_first_bridge.py --check
python3 scripts/c5_no_spoke_path_minor.py --check
python3 scripts/c5_no_spoke_supports.py --check
python3 scripts/c5_no_spoke_exterior.py --check
python3 scripts/c5_single_spoke_first_bridge.py --check
python3 scripts/c5_single_spoke_cross_row.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
python3 scripts/c5_single_spoke_branch_palettes.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證與未重跑範圍見 [研究紀錄](history/2026-09-28-no-spoke-first-bridge.md)。
目前完成唯一 degree-5 的全部分支；下一個窄入口是恰兩個 degree-5 的
雙 root 完整關係接合，先研究兩 root 相鄰子類的必要介面。這是新研究入口，
尚無該類分離定理；不能把各 root 的禁色集合獨立相乘。
degree≥6、多 degree-5、一般核心存在／分離、共同出口及 `K∞=K≤5` 仍未證。
