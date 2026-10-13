# 無 mixed C–C：無 spoke 四分量的來源 K5 排除

後續（2026-09-29）：[C–D 三飽和原分量排除](c5_adjacent_degree5_no_mixed_cd.md)
完成兩側 t=0,(2,2)、一側缺額／另一側重疊及 root 交換型：640 份必要支援
全 source K5，0 target，不需 T4。累計十二類／2,828 份覆蓋，三類／720
份保留；下文保留當輪語境，目前入口見 [weak-deletion 導覽](c5_weak_deletion_guide.md)。


2026-09-29。**C–C（兩側 t=0,(2,2)，各 D=1、O=0）的 disk 來源全部排除。**
144 份原有序接合接上 240 份幾何，得到 1,176 份必要支援，全部有原飽和
分量的 source K5。1,112 份兩側各有見證，另各 32 份只由其中一側的本規則
排除。36 個原接合無相容支援；保留支援、target 查詢與新增 target 接受均為零。
不需 T4，不限制四個原分量大小，沒有新增 root-spoke。

證據是任意大小紙面化約、沿用外部 degree-list 定理及 Python 固定域證書；
未新增 Lean theorem，必要支援／minor skeleton 不是 disk 實現證書。
一般／共同出口、任意來源完整 Σ 及 K∞=K≤5 仍未證。
目前停止點由 [weak-deletion 導覽](c5_weak_deletion_guide.md) 維護。

## 1. 同一來源與完整有序關係

依賴 [no-mixed 化約](c5_adjacent_degree5_no_mixed.md)、[root 預算](c5_root_degree_excess.md)、
[E–E 無 spoke 正跨度](c5_adjacent_degree5_no_mixed_ee.md) 與
[A–C 飽和原路徑](c5_adjacent_degree5_no_mixed_t2_t0_pairs.md)。
M 有限簡單，B=(b0,…,b4) 是 induced C5 disk 外框，H=M−B 非空連通。
M 拒絕 q=01012，刪任一非框邊後接受。相鄰 z,w 完整 degree=5，其他
內點完整 degree=4；H−{z,w} 無 mixed。兩 root 無 boundary spoke，各接
兩份不同原二接點分量 (Cz,Dz)、(Cw,Dw)。保留四分量、八具名 contacts
Cz₀,Cz₁,Dz₀,Dz₁,Cw₀,Cw₁,Dw₀,Dw₁、原 zw、全部原 bridges、旁支、
實際 boundary 附件及共同色框。

令 U={0,1,2,3}，T_C(t) 為同一原 C 的完整有序接點關係，
F_C(t)=⋂_{τ∈T_C(t)}set(τ)。接點 slack 保證 T_C 非空，|F_C|≤2。
兩側 source 預算 (D,O,κ)=(1,0,0)，故存在共同 c，使

\[
E_z(q)=E_w(q)=\{c\},\qquad
(F_{C_r},F_{D_r})(q)=(\{h_r\},U\setminus\{c,h_r\})\quad\text{或反序},
\qquad h_r\in U\setminus\{c\}.
\]

4·6·6=144 份有序資料，獨立重建後逐筆核對原 retained-join IDs 及
[B–D frontier](../artifacts/c5_adjacent_degree5_no_mixed_bd/observations.json)。
首項 join=0、sides=(16,16)。不商掉任一側兩分量、contacts 或 root 次序。
逐 contact 邊 minimality 的 release witnesses 給 singleton 禁色每色
95 份完整 binary schemas；pair K={a,b} 則完整關係恰為 {(a,b),(b,a)}。
Checker 重核全部 65,535 份非空 binary relations 得到 380＋6 份 schemas，
再按 actual support 的 q 穩定子篩選完整 tuple 集合，沒有用 marginals 相乘。

## 2. 無 spoke 外部路徑與四正跨度

每個 F_C(q) 都是非空真子集。若 C 不碰 B，T_C(q) 對 S4 全色置換不變，
F_C(q) 亦然，矛盾。因此每個原分量都有內部通往實際框鄰點的路徑。
對 r 側任一 C，取另一 root s 的任一原分量 A，得到

\[
Q_C=r-s-A_0\cdots b_j.
\]

中段全在原 A、到 B 即止，故避開 C；這只是原 zw 與原分量路徑。
不要求四條 Q_C 彼此不交。沿用 E–E §2 的外部 hub 論證，固定
root 色 d∈F_C(q) 的拒絕 residual 為 tight Gallai tree，原 K4 block
會經避開 C 的 B∪Q_C 形成 K5；較大 clique 由 degree 四及 root 接點排除。
此處使用既有 degree-list 外部定理及 hub 引理，本輪未重新查核外部文獻。

若 S_C=N_B(C) 只見 q 色 d，固定 d 的 S3 穩定子沒有不變二元子集，
故 pair 禁色不可能；singleton 禁色則必為 {d}。後者固定 root=d，所有
外鄰同色，tightness 迫每點內度至少三；但 K4-free Gallai tree 的葉塊有
私有點內度至多二，矛盾。因此四份 actual supports 都至少見兩個 q 色。

取原 zw 的細正則鄰域，兩 root 的四個 contacts 各成一段。同一 binary
的兩接點必相鄰：其原內部路徑與 root 邊形成 Jordan 曲線，若夾住另一
incidence，該 incidence 可經另一原分量（或 zw 及另一側）避開 C 到 B，
與不含 B 的內側矛盾。故必要 cyclic word 是

\[
\operatorname{perm}(Cz,Dz)\operatorname{perm}(Cw,Dw).
\]

切在 Cz 起點得到四個具名 cyclic words，各保留 16 種 contact 方向。
沿用 annulus crosscut 次序，actual supports 有同序 lifts T_j⊂Z，可共端點，
前一 max≤後一 min，最後 max≤第一 min＋5。四個跨度各≥1、總和≤5，
故各至多二；支援可稀疏，不填洞。沿 lifts 與獨立沿兩側 hull／框邊 masks
生成，恰同得 240 份，各一 placement；共核對 3,840 份 rotations。

接上 §1 的禁色與完整 schemas 得 1,176 份必要支援。108 個原 ID 有支援，
36 個是 `no_compatible_disk_support` 空纖維；空纖維不計 minor 或 target。
共同 residual c=0,1,2,3 分別有 376、376、104、320 份，沒有只取未用色 3。
這是任意大小 disk 來源的必要覆蓋，不是支援實現分類。

## 3. 原飽和路徑及固定框弧 K5

分別檢查每側 source pair 分量 C，令 root=r、F_C(q)=K。
[A–C 原路徑引理](c5_adjacent_degree5_no_mixed_t2_t0_pairs.md#3-飽和二禁色分量的原路徑-k5)
給原兩 contacts u,v 間的奇數 bridge 路徑 P=x₀…xℓ。刪除全部 P 邊後，
含 x_j 的路徑塊 W_j 保留全部原旁支，其 rooted residual palette 恰為 K。
全部 actual support T_j 因而屬於

\[
\mathcal T(q,S_C,K)=\{T\subseteq S_C:\operatorname{Stab}(q(T))\text{ 保持 }K\}.
\]

固定同一三個非空連通框弧 B=X⊔Y⊔D_B，若族中每個 T 同時碰 X、Y，
且有避開 C、內部不碰 B 的原 r–B 路徑 L 落在 D_B，令
J=P∪{ru,rv}，則五個 branch sets 為

\[
W_0,\quad W_1,\quad
(V(J)\setminus\{x_0,x_1\})\cup V(L)\cup D_B,\quad X,\quad Y.
\]

第三組經 r 連通；長度一也保留 r。原 bridge、兩條朝外的 J 邊、兩塊
各到 X/Y 的附件及 C5 三切口給十鄰接。L 可經同側另一原分量，或經
zw 加另一側原分量；均避開 C，不合併分量、不增加 spoke。
不同路徑塊可使用不同附件供應點，但全族必共用同一框弧分割。

| 必要支援上的原路徑規則 | 份數 |
| --- | ---: |
| 兩側飽和分量各有 source K5 | 1,112 |
| 只有 z 側有本規則見證 | 32 |
| 只有 w 側有本規則見證 | 32 |
| 兩側皆未排除 | 0 |

Record 0（join 66、sides=(18,18)）支援 Cz/Dz/Cw/Dw=01/03/12/23，
禁色 ({0},{2,3},{0},{2,3})。Dz 路徑塊族只有 {03}；取 X=0、Y=234、
D_B=1 與 L=z–Cz₀–…–b1，即有同側原分量路徑 K5。

Record 176（join 67、sides=(18,23)）支援 01/123/04/34，禁色
({0},{2,3},{2},{0,3})。Dz 的族 {12,23,123} 無一份框弧分割通吃全族；
Dw 的族只有 {34}，取 X=123、Y=4、D_B=0 及 L=w–z–Cz₀–…–b0 即排除。
這說明不能只查固定一側，也不能逐路徑塊自行更換框弧。

任意大小來源必落入必要表，而每份都有上述 source K5，故 C–C disk
minimal q-core 不存在。外框為 disk 邊界是必要前提；不宣稱一般 planar
C5 同樣排除。不使用 target 拒絕假設，也不把本結果記作 2,352 個 target 接受。

## 4. 證書、覆蓋與出口

[Checker](../scripts/c5_adjacent_degree5_no_mixed_cc.py)、
[完整 JSON](../artifacts/c5_adjacent_degree5_no_mixed_cc/observations.json) 及
[逐筆表](../artifacts/c5_adjacent_degree5_no_mixed_cc/support_table.md)
保留原 IDs、來源 SHA、四完整 schemas、八 contacts、rotations、空纖維、
完整路徑塊族、固定框弧與原外部路徑。

- 2,288 個成功的分量見證，各重播長度 1、3、5 的 bridge；另有兩種原
  外部路徑模式的 tethers／旁支控制，合共 6,992 次 minor controls。
  保存 2,288 份長度一證書及 128 份額外控制，合共 2,416 份。
- 每個 minor 都核對五組連通、不交、十鄰接、原 root 度數與 actual supports，
  再核反射及 root 交換。有限 skeleton 不證任意大小拓撲引理或 degree-list 定理。
- 1,176 份 literal source 反射、1,176 份整圖 root 交換、2,352 份整分量交換，
  比對完整 schema、路徑塊族及全部框弧／路徑見證，沒有商掉身份。
- 十個控制包含只查單側的遺漏、移除 zw／外部附件／原 bridge、branch sets
  重疊、把 binary 改成 spoke、跨度三、marginals 失真及漏刪 root 對角線。

新增 144 個原 IDs（整圖交換已在同一 C–C 集合內），累計 **十一類／2,540
份覆蓋，四類／1,008 份保留**。下一窄入口 C–D 的 144 份正向 IDs 已綁定，
首項 join 4、sides=(16,30)；尚未生成其支援／target 表。C–E、D–D、D–E 保留。

[出口第九類](c5_single_sided_exit.md) 增加 C–C 的來源排除分支：實際 minimal
q-core 不會落在本型。其他雙列分離型接回完整 Σ 時仍需來源雙缺失與刪邊繼承；
這裡沒有移除該前提，也沒有證一般交換機制完備性。

## 5. 重播與證據界線

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_cc.py --check
PYTHONHASHSEED=17 python3 scripts/c5_adjacent_degree5_no_mixed_cc.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_bd.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t0_pairs.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證及未重跑範圍見 [當輪紀錄](history/2026-09-29-adjacent-no-mixed-cc.md)。
未新增 Lean theorem，`lake build` 不表示新紙面 minor／annulus 論證已形式化。
本輪沒有獨立第二審稿者，成果保留工作區，未 commit／push。
