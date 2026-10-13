---
docgraph:
  id: c5.adjacent-degree5-no-mixed-t2-bridge
  family:
    - c5
    - c5.degree5
  derives_from:
    - c5.adjacent-degree5-no-mixed-t2
  requires:
    - c5.no-spoke-first-bridge
    - c5.single-spoke-first-bridge
    - c5.single-spoke-branch-palettes
    - c5.single-spoke-frame-arc
---
# 無 mixed 兩側 t=2：原 bridge、固定框弧與 68 個新增延拓

三輪成果的整合提交與驗證見 [發布紀錄](history/2026-09-29-adjacent-no-mixed-t2-publish.md)。

後續（2026-09-29）：[原雙端點](c5_adjacent_degree5_no_mixed_t2_endpoints.md)
新增 60 個延拓後，[整條原路徑 palettes](c5_adjacent_degree5_no_mixed_t2_path_palettes.md)
再關閉最後 4 項；原 322 份全保留、644／644 查詢全證、0 筆來源排除，
接入出口第九類。以下與本頁 artifact 保留原輪數字及 record 5 停止點。

2026-09-29，接手基準 `51ef494`。接續 [支援與環序表](c5_adjacent_degree5_no_mixed_t2.md)
的 record 4／p₁；研究優先序見 [HANDOFF](HANDOFF.md)。

**record 4 的 p₁ 必延拓。** 將同一來源上的固定三框弧及 singleton-source
首橋引理套回原表，新增 **68 個指定列延拓、0 筆來源排除**。原 322 份
必要資料全部保留，已證 **580／644 個 target 查詢**；258 份雙列皆證，
64 份各剩一列未決。無 mixed 兩側 t=2 尚未整型接回出口。

證據為任意大小紙面 palette 歸納／原圖 minor、外部 degree-list 定理
與 Python 有限控制。不需 T4；未新增 Lean theorem，未證必要表可實現、
完整 Σ、一般單側／共同出口或 `K∞=K≤5`。

## 1. 同一來源與雙禁色路徑

完整沿用 [原表 §1–3](c5_adjacent_degree5_no_mixed_t2.md#1-同一來源與原-88-份資料)：
G 有限簡單、B=(b0,…,b4) 為 induced disk 外框，有效 H 非空連通；
G 是 edge-minimal q=01012 obstruction。相鄰 roots z、w 的完整 degree
恰為 5，其餘內點完整 degree=4。H−{z,w} 無 mixed；每側有兩條原
boundary spokes 及唯一二接點原 unary C_r。U={0,1,2,3}，p₁=01021、p₂=01212。

保留原 zw、四條 spokes、兩個原分量、四個具名有序接點、所有原 bridges、
旁支與 actual supports S_r。T_r(t) 是同一 C_r 的完整接點關係，
F_r(t) 是其所有 tuples 色集的交集；精確接合仍為

\[
E_r(t)=U\setminus(t(B_r)\cup F_r(t)),\qquad
Z_G(t)=(E_z(t)\times E_w(t))\setminus\Delta. \tag{1}
\]

忽略 root 色時，原接點有 slack，所以 T_r(t) 非空。對任意 d∈F_r(t)，
在兩原接點 lists 扣去 d 得被拒絕的 degree assignment。
[Dvořák Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
給 tightness 與 Gallai block palettes；本輪重新核對第 5–6 頁。這不要求
target minimality，亦非本專案 Python／Lean 所證的外部定理。

原表已排除 C_r 的 K4 block。若 F_r(t)=D 是 pair，既有
[雙禁色 bridge 化約](c5_no_spoke_path_minor.md#1-前提完整關係與共用路徑塊)
只用 C_r 的 degree-4 頂點、兩接點、兩份拒絕 palettes 及 K4-free，
故可搬至此處：兩接點間是奇數長原 bridge 路徑 P=(x₀,…,xℓ)，ℓ≥1。
刪去全部 P 邊得到原路徑塊 W_j；其實際支援 T_j⊆S_r 包含 x_j 的
直接附件。W_j 連通、兩兩不交，保留全部旁支。

令 D_j^t 為 x_j 的直接 boundary 色，Q_j^t 為所有路徑外 palettes 聯集。
未扣 root 色的局部 residual 為

\[
L_j^t=U\setminus(D_j^t\cup Q_j^t)=D. \tag{2}
\]

此處 L 是局部 residual 記號，與 (1) 的 root 可用色 E_r 及整分量 F_r
分開。rooted-palette 唯一性給：每個逐點固定 t(T_j) 的色置換皆保持 D。
故每個實際 T_j 都在有限族

\[
\mathcal T(t,S_r,D)=\{T\subseteq S_r:\quad
  \forall\sigma\in S_4,\ \sigma t|_T=t|_T\Rightarrow\sigma D=D\}. \tag{3}
\]

singleton F 不套 (2) 的 pair 路徑 residual 結論。

## 2. 保留 zw 的外部路徑與固定三框弧

對 C=C_r，s 是另一 root。到 boundary 的原外部路徑 L 可取三種：

- 原 spoke r–b_h，h∈B_r；
- 原 r–s–b_h，h∈B_s；
- 原 r–s、s 的一個具名 C_s 接點及 C_s 內到 b_h 的簡單路徑，h∈S_s。

第三種使用另一原分量的實際附件；取第一次抵達 boundary 的路徑，內部
在 {r,s}∪C_s，完全避開 C。它可以與 C_s 的另一接點路徑共用內點。

固定一份 B=X⊔Y⊔D_B，三組非空且各沿原 C5 連通。假設 L 的落點
h∈D_B，且某條原 bridge 的兩端路徑塊 W_i、W_(i+1) 都實際碰 X、Y。
令 J=P∪{rx₀,rxℓ}，取五個 branch sets

\[
W_i,\quad W_{i+1},\quad
Z=(V(J)\setminus\{x_i,x_{i+1}\})\cup V(L)\cup D_B,\quad X,\quad Y. \tag{4}
\]

J 刪去相鄰兩點後的餘部經 r 連通，ℓ=1 時為 {r}；原 L 接到 D_B。
原分量身份與 W 分割保證五組不交，且每組連通。
兩 W 由原 bridge 相鄰，各自經 J 的朝外邊接 Z；四份實際附件接 X、Y；
三份框弧之間各有原 C5 邊。因此十對相鄰，得到來源 G 的 K5 minor。
完整來源圖、染色約束與分量關係不因選取 minor witness 而改寫。

對容許族的量詞是先取**同一份** X、Y、D_B 及一條原外部路徑，再驗
全部 T∈𝒯 均碰 X、Y。兩 W 可用不同供應點；不逐 T 重選分割，亦不
以共同必接點取代整個支援族。空族另證不可能有 W，不用空全稱構造 minor。
這是 [既有三框弧引理](c5_no_spoke_first_bridge.md#4-同一份三框弧容許不同供應點)
在相鄰兩 root 的原外部路徑上的搬運。

## 3. record 4／p₁

原 frontier 31、原 sides=(137,147)：

\[
B_z=04,\ S_z=01,\ F_z(q)=\{1\};\qquad
B_w=34,\ S_w=123,\ F_w(q)=\{0\}.
\]

p₁ 下 F_z={1}、E_z={2,3}，唯一失敗候選為 F_w={0,3}，使 E_w=∅。
反設此候選。p₁ 在 S_w 的色為 102；(3) 迫使每個 W_j 都見色 1、2，
所以 T_j 只能為 13 或 123，每塊均碰 b1、b3。

在 (4) 取 i=0、X={b1,b2}、Y={b3}、D_B={b4,b0}，L 為原 wb4。
五組即為 W₀、W₁、(J−{x₀,x₁})∪{b4,b0}、{b1,b2}、{b3}。
原 wb4 保證第三組連通；首橋、兩端朝外邊、四附件及三框邊給 K5。
故 F_w(p₁)≠{0,3}，所有完整候選皆有合法 root 色對，p₁ 必延拓。
p₂ 的既有完整換色證明保留；record 4 因而雙列皆證。

## 4. 同一首橋 β 的跨列限制

原表每側 F_C(q)={d}。若 target t 的 F_C(t)=D 是 pair，P 仍只從
target 抽取，q 證書沿用同一原路徑。令

\[
K=\{a:\forall i\in S_C,\ q_i=a\iff t_i=a\}.
\]

[固定色 palette 歸納](c5_single_spoke_branch_palettes.md#2-rooted-palette-唯一性與固定色守恆)
只用同一 W_j 的非 root lists 與原 boundary 附件，得
L_j^q∩K=L_j^t∩K。旁支非 root 點沒有任一 root 邊；兩 root 的 degree
為 5 不參與這份歸納。

若 d∈K，端點 tightness 給 d∈L₀^q，故 **d∉D 時立刻矛盾**。
若 d∈K∩D，首橋 q palette 為同一 singleton {β}；端點 tightness 及
下一點的兩條 bridge palettes（ℓ=1 時則為另一接點）給

\[
L_0^q=L_1^q=\{d,\beta\},\quad \beta\ne d,\qquad
\{d,\beta\}\cap K=D\cap K. \tag{5}
\]

兩個首橋路徑塊的 T 必同時屬於
𝒯(q,S_C,{d,β})∩𝒯(t,S_C,D)。每個 β 分別用 §2，但兩端不可獨立
選 β；全部 β 排除後才否定候選。d∉K 時本層跳過，不能宣稱共用 residual。
(5) 的局部二色集合亦不能換成整分量 singleton F_C(q)。

例如 record 43／p₂ 的 C_w 有 S_w=234、d=1、D={0,3}、K={1,3}，
由 d∉D 排除。record 54／p₂ 的 C_w 有相同 S_w、d=3、D={0,3}，
K={1,3}；β=0 迫使首橋兩塊均接 34，β=2 則均接 23。兩側原 spoke
都接 b2、b4，分別用 wb2、wb4 及固定三弧得到 K5。這些只是否定
指定 target 的失敗候選，沒有在 q 下排除來源。

## 5. 完整套表、證書與停止點

[Checker](../scripts/c5_adjacent_degree5_no_mixed_t2_bridge.py) 只讀原 JSON，
綁定 SHA256、322 個原 IDs、88 份 frontier／side 記錄、原 q schemas、
全部原記錄、各記錄的完整 placements 與四個具名 contact rotations。
原 118／3,548 表、88 份子表及 322 份支援表均未覆寫或重編。

重算 644 個查詢的全部 2,892 組完整 F-product joins；原來 160 組沒有
合法 root 色對。逐組保留兩側完整禁集及空 residual／同 singleton 的
失敗見證。三框弧消去 72 組，首橋再消去 24 組；餘 64 組各對應一個
未決查詢。每組候選都排除或有原 root-pair 見證後，才標示該列接受。

| 層 | 已證 target | 雙列皆證 | 未決查詢 | 新增來源排除 |
| --- | ---: | ---: | ---: | ---: |
| 原支援／環序 | 512 | 206 | 132 | 0 |
| 固定三框弧、三種原外部路徑 | 556 | — | 88 | 0 |
| 再加同一首橋 | 580 | 258 | 64 | 0 |

最終 A/A、A/?、?/A、?/? 為 **258、32、32、0**。原 322 筆全部保留；
已證延拓並不保證該筆存在符合前提的 disk 來源。

[JSON](../artifacts/c5_adjacent_degree5_no_mixed_t2_bridge/observations.json) 與
[完整套表](../artifacts/c5_adjacent_degree5_no_mixed_t2_bridge/support_table.md) 另保存：

- 60 份具名連通三弧分割，由三切口及獨立 3⁵ 份頂點指派核對。
- 576 個逐塊穩定子控制、48 個 pair residual 控制；沿用並重算 8,748 個
  固定色歸納步、48 個 tight endpoint 及 24 個首橋相容控制。
- 682 份 K5 skeletons 及其反射：保留兩 roots、四 spokes、兩個二接點
  unary 與原 zw，含三種外部路徑、奇數長度 1／3／5、16 種雙端 tether
  形狀及兩塊獨立供應點；每份驗五組連通不交與十對原邊鄰接。
- 322 次 root 交換、160 次失敗候選的字面 target 反射；搬運全部支援族、
  β、色框、框弧及外部路徑類型，不以正規化列取代原字面列。
- 12 個負控制，涵蓋 singleton guard、非守恆 d、部分候選、獨立 β、
  固定分割量詞、空族，以及缺原 zw／spoke／bridge／附件／框邊或不交性。
  刪邊控制只否定所存 witness，不宣稱整圖變平面。

**第一個未決為 record 5／p₂**，原 frontier 28、sides=(137,141)：
B_z=04、S_z=01、F_z(q)={1}；B_w=14、S_w=1234、F_w(q)={0}。
p₂ 唯一失敗候選仍為 (F_z,F_w)=({1},{0,3})，給 (E_z,E_w)=({3},∅)。
此時 K={1,3}、d=0∉K；target 路徑塊族有九份，最小支援為
12、14、23、34，沒有本層所需的統一三弧 witness。

下一步保留原 wb1、wb4、zw、C_z 及完整 C_w，研究 q／p₂ 只在 b2
改色所施加的**端點與沿原 bridge 的 palette 限制**；先補上 d 不守恆時
的有效引理，再套餘 64 個查詢。必要支援不能任意當作可實現路徑塊，亦
不能跳過 q 的 singleton 證書。一般出口及整型 t=2 分離仍開放。

## 6. 重播與界線

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_t2_bridge.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared.py --check
python3 scripts/c5_adjacent_degree5_singleton_long_arc.py --check
python3 scripts/c5_no_spoke_supports.py --check
python3 scripts/c5_no_spoke_exterior.py --check
python3 scripts/c5_no_spoke_first_bridge.py --check
python3 scripts/c5_single_spoke_first_bridge.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
python3 scripts/c5_single_spoke_two_two_minor.py --check
python3 scripts/c5_single_spoke_branch_palettes.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證與省略項目見 [當輪紀錄](history/2026-09-29-adjacent-no-mixed-t2-bridge.md)。
有限 skeletons 不要求整份來源 degree/list 條件，並非 realizability 證書；
任意大小由既有 palettes、rooted-block 歸納與 (4) 的原圖 branch sets 承擔。
`lake build` 僅驗既有 Lean 專案，不將本輪紙面論證形式化。
