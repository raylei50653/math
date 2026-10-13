# 無 mixed C–E：五正跨度與飽和原路徑來源排除

後續（2026-09-29）：[D–D 四飽和原分量排除](c5_adjacent_degree5_no_mixed_dd.md)
完成兩側 t=0,(2,2)、各 D=0、O=1；352 份必要支援全 source K5，
80 個原 IDs 無相容支援，0 target，不需 T4。四正跨度保證至少三份
框邊支援，飽和原路徑與補弧給統一 minor。累計十四類／3,260 份覆蓋，
只剩 D–E 含交換型一類／288 份；目前入口見
[weak-deletion 導覽](c5_weak_deletion_guide.md)。

2026-09-29。**C–E 及整圖 root 交換型 E–C 的 disk 來源全部排除。**
144 份正向原接合接上 60 份幾何，得到 96 份必要支援，全有 source K5；
108 個原 IDs 無相容支援。五原分量的正跨度恰好用完 C5，飽和分量的
兩框點與補弧給統一 minor。保留支援、target 查詢與 target 接受均為零。
不需 T4，不限制原分量大小。證據是任意大小紙面化約、沿用外部
degree-list 定理及 Python 固定域證書；未新增 Lean theorem。
必要表／minor skeleton 不證 disk 實現，一般／共同出口、任意來源完整 Σ、
一般交換完備性及 K∞=K≤5 仍未證。目前入口見
[weak-deletion 導覽](c5_weak_deletion_guide.md)。

## 1. 前提與同一來源完整關係

沿用 [no-mixed 化約](c5_adjacent_degree5_no_mixed.md)、
[root 預算](c5_root_degree_excess.md)、[C–D 前序](c5_adjacent_degree5_no_mixed_cd.md)、
[C–C 外部路徑](c5_adjacent_degree5_no_mixed_cc.md) 及
[E–E 正跨度](c5_adjacent_degree5_no_mixed_ee.md)。M 有限簡單，
B=(b0,…,b4) 是 induced C5 disk 外框，H=M−B 非空連通；M 拒絕
q=01012，刪任一非框邊後接受 q。相鄰 z,w 完整 degree=5，其餘內點
完整 degree=4，H−{z,w} 無 mixed。兩 root 均無 boundary spoke。
z 側兩原分量 Cz,Dz 各有兩 contacts；w 側 Cw,Dw,Ew 有 (2,1,1)
contacts。保留這五份原分量、八具名接點、原 zw、全部 bridges／旁支、
actual boundary 附件及共同色框，單接點原分量不能改作 spoke。

令 U={0,1,2,3}，T_C(t) 為原 C 的完整有序接點關係，
F_C(t)=⋂_{τ∈T_C(t)}set(τ)。接點 slack 保證 T_C 非空。
Source 預算兩側皆 (D,O,κ)=(1,0,0)，minimality 迫共同 residual {c}：

\[
(F_{Cz},F_{Dz})(q)=(\{a\},U\setminus\{c,a\})\quad\text{或反序},
\qquad a\in U\setminus\{c\},
\]
\[
(F_{Cw},F_{Dw},F_{Ew})(q)=(\{h\},\{r\},\{s\}),
\qquad(h,r,s)\in\operatorname{Perm}(U\setminus\{c\}).
\]

4·6·6=144 份有序原接合由此獨立重建，逐項對回 C–D frontier 的
原 join／side IDs 與 SHA；首項 join=12、sides=(16,64)。逐 contact
刪邊的 release witnesses 給每色 singleton 禁色 95 個完整 binary
schemas，pair K={a,b} 的唯一完整關係為 {(a,b),(b,a)}；兩 unary
關係各為單 tuple。Checker 重核 65,535 份非空 binary relations，
得到 380＋6 份 schemas，再按 actual support 穩定子篩選；不將
marginals 相乘，也不宣稱這些 schemas 可獨立實現。

## 2. 五正跨度迫使每份支援為框邊

各 F_C(q) 都是非空真子集，故 actual support S_C 非空，否則完整
關係在 S4 下不變。對任何 C，經原 zw 及另一側原分量可得避開 C 的
root–B 原路徑。固定一個禁色作 root 色，沿用既有degree-list 定理
得 tight Gallai tree；外部路徑與 B 組成 hub，依既有引理排除 K4 block。
本輪沿用上述報告的外部定理及任意大小 hub 論證，未重查外部文獻。

若 q(S_C) 只有色 d，固定 d 的 S3 穩定子不能保持任何二元禁色集，
故飽和分量不可能；singleton 禁色則只能是 {d}。固定 root=d 時全部
外鄰同色，tightness 迫 min degree_C≥3，但 K4-free Gallai leaf block
存在內度至多二的私有點，矛盾。此論證同時適用 binary 與 unary
原分量。因此五份 supports 都至少見兩個 q 色，均有正跨度。

取原 zw 的細正則鄰域，各 root incidences 成一段；同分量的兩 contacts
必相鄰，否則原內部路徑圍出的 Jordan 曲線會困住仍可沿另一原分量
到 B 的 incidence。故必要 cyclic word 是
perm(Cz,Dz)perm(Cw,Dw,Ew)。切在 Cz 得 12 個具名 words；三個 binary
的兩種 contact 方向給每 word 八個 rotations，不商掉反射或分量身份。

既有 annulus crosscut 引理給同序 lifts T_j⊂Z，前一 max≤後一 min，
最後 max≤首個 min＋5，允許共端點，稀疏支援不先補洞。因五份皆正：

\[
5\le\sum_{j=0}^4(\max T_j-\min T_j)\le5.
\]

所以各跨度恰為一，無間隙，每份 S_C 恰是一條框邊的兩端，五份框邊
互異。沿 lifts 及獨立沿兩側 hull-edge masks 生成均得 60 份幾何，
各一 placement，核對 480 份 contact rotations。接完整 q schemas 後
有 96 份必要支援，落在 36 個原 IDs；108 個空纖維明標
`no_compatible_disk_support`。全部保留必要支援的 c=3 是枚舉結果，
輸入仍遍歷 c=0,1,2,3。必要覆蓋不等於來源實現。

## 3. 統一的原路徑 K5

取 z 側唯一飽和分量 C，K=F_C(q) 為二元集，S_C={a,b} 是相鄰框點。
沿用 [飽和原路徑引理](c5_adjacent_degree5_no_mixed_t2_t0_pairs.md#3-飽和二禁色分量的原路徑-k5)：
兩原 contacts u,v 間有奇數長原 bridge 路徑 P=x₀…xℓ；刪去 P 的
邊後，每個含 x_j 的路徑塊 W_j 保留全部旁支，其 rooted residual
palette 恰為 K。每塊的 actual support T⊆{a,b} 必使 Stab(q(T)) 保持 K。
空集或單點的穩定子都不能保持二元集，所以 **每個 W_j 均同時碰 a,b**。
Checker 的 admissible-support 族亦逐筆恰為 {{a,b}}。

令 X={b_a}、Y={b_b}、D_B=B−{b_a,b_b}。因 a,b 相鄰，D_B 是非空
連通三點框弧，X、Y、D_B 兩兩相鄰。同側另一原分量 C′ 的支援是
另一條框邊，必有 h∈S_C′−{a,b}。經 z、C′ 的原 contact、C′ 內簡單
路徑走到 b_h 得 L，內部不碰 B，且完全避開 C。這裡固定 b_h 為
端點，路徑只走 C′ 內點後才踏上 B；不增加任何 spoke。

令 J=P∪{zu,zv}，五個 branch sets 為

\[
W_0,\quad W_1,\quad
(V(J)\setminus\{x_0,x_1\})\cup V(L)\cup D_B,\quad X,\quad Y.
\]

第三組經 z 連通；ℓ=1 時仍保留 z。五組不交，原 bridge 給第一、二組
相鄰，J 的兩個朝外邊給各自至第三組的相鄰；W₀,W₁ 各有原附件碰
X/Y，L 落在 D_B，三框弧的三切口供其餘相鄰，遂有十對相鄰，即 K5。
這使用同一來源的原 bridges、旁支與同一份框弧分割，適用任意路徑長度。

Record 0：join=104、sides=(19,64)，支援 Cz/Dz/Cw/Dw/Ew=
01/04/12/23/34，禁色 ({1},{0,2},{0},{1},{2})。取 C=Dz、X=0、Y=4、
D_B=123、L=z–Cz₀–…–b1 即得 minor。96 份皆有此種同側見證；證書
另保存經 zw／另一側原分量的見證。實際 disk 來源必落在必要表，但
每份都產生 source K5，因此 C–E 不存在；整圖交換 roots、歸屬與接點
即排除 E–C。不需 T4；不宣稱一般 planar C5 有同樣的 annulus 限制。

## 4. 證書、控制與出口覆蓋

[Checker](../scripts/c5_adjacent_degree5_no_mixed_ce.py)、
[完整 JSON](../artifacts/c5_adjacent_degree5_no_mixed_ce/observations.json)、
[逐筆表及原 ID 纖維](../artifacts/c5_adjacent_degree5_no_mixed_ce/support_table.md)
保存完整 schemas、五分量／八 contacts、rotations、支援、固定框弧、
原外部路徑、反向原 IDs 與明確空纖維。

- 96 份統一兩單點框弧見證各重播 bridge 長度 1、3、5；另 128 次
  控制兩種原外部路徑、四種 tether 形狀及外部鏈長，合計 416 次 minor
  controls，保存 224 份證書。逐份驗證五組連通、不交、十鄰接、完整
  root degree、原分量無互接及 actual supports，並驗證反射和 root 交換。
- 96 份 literal source 反射、96 份整圖 root 交換與 192 份整分量交換，
  重核完整 binary／unary 關係、座標反序、原路徑塊族及全部框弧見證。
- 11 個控制覆蓋遺失 zw／原 bridge／外部附件、branch sets 重疊、
  將原分量當 spoke、跨度二、空族不是 minor、marginals 失真、漏刪對角線。
  有限 skeleton 不要求其他內點滿足原 degree／lists，不作實現證書。

含交換方向新增 288 個原 IDs，累計 **十三類／3,116 份覆蓋，兩類／432
份保留**。D–D 有 144 份，D–E 含交換有 288 份。下一窄入口 D–D
的 144 份正向 IDs 已綁定，首項 join=424、sides=(30,30)；尚未建立
其支援／target 表。本輪不擴大處理其他 class。

[出口第九類](c5_single_sided_exit.md) 增加 C–E／E–C 來源排除分支；
這不是新增 192 個 target 接受。其他雙列分離分支接回完整 Σ 時仍需
來源雙缺失及刪邊繼承，本輪未移除其前提。

## 5. 重播與信任界線

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_ce.py --check
PYTHONHASHSEED=17 python3 scripts/c5_adjacent_degree5_no_mixed_ce.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_cd.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t0_pairs.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證及省略範圍見 [當輪紀錄](history/2026-09-29-adjacent-no-mixed-ce.md)。
`--check` 重算後逐 byte 比對 JSON／表格，無參數只生成本層；舊 artifacts
不改寫。未新增 Lean theorem；`lake build` 不表示新紙面拓撲已形式化。
本輪沒有獨立第二審稿者；成果保留工作區，未 commit／push。
