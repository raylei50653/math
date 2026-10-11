# 無 mixed D–E：五正跨度、雙飽和原路徑與最後一類排除

2026-09-29。**D–E 及整圖 root 交換型 E–D 的 disk 來源全部排除。**
144 份正向原接合與 60 份幾何接合，得到 48 份必要支援，全部有 source
K5；120 個原 IDs 無相容支援。D 側兩份飽和分量各自都能提供統一 minor。
不需 T4，不限制原分量大小，保留支援、target 查詢及 target 接受均為零。
含交換方向新增 288 個原 IDs，no-mixed **十五類／3,548 份原接合全部覆蓋**。

證據為任意大小紙面化約、沿用外部 degree-list 定理及 Python 固定域
證書；未新增 Lean theorem。必要表／minor skeleton 不證 disk 實現，
固定 q 不給任意來源完整 Σ，一般／共同出口、一般交換完備性及
K∞=K≤5 仍未證。目前入口見 [weak-deletion 導覽](c5_weak_deletion_guide.md)。

## 1. 同一來源、預算與完整關係

依賴 [no-mixed 化約](c5_adjacent_degree5_no_mixed.md)、
[root 預算](c5_root_degree_excess.md)、[D–D 前序](c5_adjacent_degree5_no_mixed_dd.md)、
[C–E 五分量幾何](c5_adjacent_degree5_no_mixed_ce.md) 及
[飽和原路徑引理](c5_adjacent_degree5_no_mixed_t2_t0_pairs.md#3-飽和二禁色分量的原路徑-k5)。
M 有限簡單，B=(b0,…,b4) 是 induced C5 disk 外框，H=M−B 非空連通。
M 拒絕 q=01012，刪任一非框邊後接受 q；相鄰 z,w 完整 degree=5，
其餘內點完整 degree=4，H−{z,w} 無 mixed。兩 root 都無 boundary spoke。
z 側 Cz,Dz 各二接點；w 側 Cw,Dw,Ew 的接點數為 (2,1,1)。保留五份
不同原分量、八具名 contacts、原 zw、全部 bridges／旁支、actual boundary
附件與共同色框。單接點原分量仍是原分量，不能替換成 spoke。

令 U={0,1,2,3}，T_C(t) 為原 C 的完整有序接點關係，
F_C(t)=⋂_{τ∈T_C(t)}set(τ)。接點 slack 保證 T_C 非空。
Source 預算 z 側 (D,O,κ)=(0,1,0)，w 側為 (1,0,0)；minimality 迫
兩 root residual 同為 {c}。故

\[
(F_{Cz},F_{Dz})(q)=(\{h,a\},\{h,b\}),\quad
(h,a,b)\in\operatorname{Perm}(U\setminus\{c\}),
\]
\[
(F_{Cw},F_{Dw},F_{Ew})(q)=(\{u\},\{v\},\{s\}),\quad
(u,v,s)\in\operatorname{Perm}(U\setminus\{c\}).
\]

共享禁色 h 不表示共享內點。4·6·6=144 份有序原接合獨立重建後，
逐項對回 D–D frontier 的原 join／side IDs 與 SHA；首項 join=432、
sides=(30,64)，其 root 交換 join=1420。Source 預算不作 target 等式。

每個二元禁色 K={a,b} 的完整 binary 關係必恰為 {(a,b),(b,a)}：
每個 tuple 都含 K，逐 contact 刪邊的 release witnesses 迫兩次序皆存在。
Cw 的 singleton 禁色每色有 95 個完整 binary schemas；Dw,Ew 是單 tuple。
Checker 重核 65,535 份非空 binary relations，重建 380＋6 份 schemas，
再按 actual support 的 q 穩定子篩選完整 tuples。沒有將端點 marginals
相乘，也不聲稱五份 schemas 能獨立實現。

## 2. 五正跨度迫使五份框邊支援

各 F_C(q) 都非空且不等於 U，因此各 actual support S_C 非空。
對任一原分量 C，經原 zw 與另一側原分量，有避開 C 的 root–B 原路徑。
沿用既有 degree-list tight Gallai tree 與外部 hub 排除 K4 block 的論證；
本輪沿用 C–E 及飽和原路徑報告的外部定理，未重新查核文獻。

若 q(S_C) 僅含 d，固定 d 的 S3 穩定子不能保持二元禁色集，故 Cz,Dz
不可能。對其餘 singleton 禁色，穩定性迫禁色={d}。固定 root=d 後，
所有外鄰皆同色；tightness 迫每點內度至少三，但 K4-free Gallai leaf
block 有內度至多二的私有點，矛盾。因此五份支援都至少見兩個 q 色。

沿用 C–E 的原 zw 正則鄰域及 annulus crosscut 論證：每 root 的
incidences 成一段，同分量的兩 contacts 相鄰。必要 cyclic word 為
perm(Cz,Dz)perm(Cw,Dw,Ew)，切在 Cz 得 12 個具名 words；三對 binary
contacts 各有兩方向，不商掉反射或原分量身份。
同序 lifts T_j⊂Z 可共端點，前一 max≤後一 min，最後 max≤首個 min＋5。
五份正跨度給

\[
5\le\sum_{j=0}^4(\max T_j-\min T_j)\le5.
\]

所以每份跨度恰一、沒有間隙，五份 actual supports 是五條互異框邊的兩端。
這保留稀疏支援本身，沒有先補洞。沿 lifts 與獨立沿兩側 hull-edge masks
生成皆得 60 份幾何，各一 placement，共核對 480 份 contact rotations。
接完整 q schemas 後有 **48 份必要支援，落在 24 個正向原 IDs**；
120 個空纖維明標 `no_compatible_disk_support`。共同 residual c=3 是
枚舉結果，輸入仍遍歷四種 c；這只是任意大小來源的必要覆蓋。

## 3. 任一 D 側飽和原分量都給 K5

任取 C∈{Cz,Dz}，K=F_C(q)，S_C={a,b} 是相鄰框點。
飽和原路徑引理給兩 contacts u,v 間的奇數長原 bridge 路徑
P=x₀…xℓ。刪去 P 邊後，各 x_j 的路徑塊 W_j 保留全部原旁支，
其 rooted residual palette 恰為 K。W_j 的 actual support T⊆S_C
須使 Stab(q(T)) 保持 K；空集或單點皆不可能，因此每個 W_j 都同時碰 a,b。
逐筆 admissible-support 族也恰為 {{a,b}}。

令 X={b_a}、Y={b_b}、D_B=B−{b_a,b_b}，三者連通且兩兩相鄰。
同側另一原分量 C′ 的支援是不同框邊，必有 h∈S_C′−{a,b}。
沿 z 的原 contact、C′ 內簡單路徑到 b_h 得 L；L 避開 C，且只在
終點碰 B。令 J=P∪{zu,zv}，五個 branch sets 為

\[
W_0,\quad W_1,\quad
(V(J)\setminus\{x_0,x_1\})\cup V(L)\cup D_B,\quad X,\quad Y.
\]

第三組經 z 連通，ℓ=1 時仍含 z。五組不交；原 bridge 給 W₀–W₁，
J 的兩個朝外邊給兩 W 至第三組，兩 W 各有原附件碰 X,Y，而 L 落在
D_B；三框弧切口供其餘相鄰，合共十對，即來源 K5 minor。
這對任意原路徑長度成立，且全部路徑塊共用同一份框弧分割。

Record 0：join=432、sides=(30,64)，Cz/Dz/Cw/Dw/Ew 支援為
01/04/12/23/34，禁色 ({0,1},{0,2},{0},{1},{2})。
取 C=Cz，X=0、Y=1、D_B=234、L=z–Dz₀–…–b4；或取 C=Dz，
X=0、Y=4、D_B=123、L=z–Cz₀–…–b1，均得 minor。

任意 disk 來源必落在必要表，卻每份都有上述 K5，故 D–E 不存在。
整圖交換 roots、歸屬及 contacts 即排除 E–D。不需 T4，不將 annulus
限制套到一般 planar C5；沒有將 96 個假想 target 查詢記成接受。

## 4. 證書與全分類接合

[Checker](../scripts/c5_adjacent_degree5_no_mixed_de.py)、
[完整 JSON](../artifacts/c5_adjacent_degree5_no_mixed_de/observations.json)、
[逐筆表與原 ID 纖維](../artifacts/c5_adjacent_degree5_no_mixed_de/support_table.md)
保留原 IDs／SHA、完整 schemas、五原分量／八 contacts、rotations、
空纖維、原路徑塊族、兩份統一框弧見證及 root 交換 IDs。

- 48 份支援各對兩個飽和分量重播 bridge 長度 1、3、5，共 288 次；
  另 128 次控制兩種原外部路徑、四種 tether 形狀與外部鏈長，合計
  **416 次 minor controls，保存 224 份證書**。核對五組連通、不交、
  十鄰接、兩 root 完整度數、原分量無互接與 actual supports。
- 48 次 literal source 反射、48 次整圖 root 交換、96 次整分量交換，
  核對完整關係／座標反序、兩個飽和分量的路徑塊族及全部框弧見證。
- 11 個負控制涵蓋遺失 zw／原 bridge／外部附件、branch sets 重疊、
  原分量改作 spoke、跨度二、空族不是 minor、marginals 失真、漏刪對角線。
  有限 skeleton 不要求其他內點滿足原 degree／lists，不是實現證書。

含交換方向新增 288 個原 IDs；與 D–D 覆蓋的 3,260 份不交，聯集逐 ID
恰為原 3,548 份 retained joins。故十五種 unordered cells、二十五個 ordered
cells 的 no-mixed 原分類全部覆蓋，`remaining_cells={}`，沒有下一個
未處理的 no-mixed class。這個分類完成不等於所有 class 都作來源排除：
既有雙列分離分支仍用各自證據。[出口第九類](c5_single_sided_exit.md)
因此涵蓋相鄰雙 degree-5 的全部 no-mixed 分拆；接回完整 Σ 仍明用
來源雙缺失及刪邊繼承。較大／多 mixed、非相鄰 roots、多 degree-5、
degree≥6 與一般／共同出口保留；本輪沒有擴大處理它們。

## 5. 重播與信任界線

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_de.py --check
PYTHONHASHSEED=17 python3 scripts/c5_adjacent_degree5_no_mixed_de.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_dd.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_ce.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t0_pairs.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證與省略範圍見 [當輪紀錄](history/2026-09-29-adjacent-no-mixed-de.md)。
`--check` 重算後逐 byte 比對 JSON／表格，無參數只生成本層；舊 artifacts
未改寫。未新增 Lean theorem，`lake build` 不表示新紙面拓撲已形式化。
本輪沒有獨立第二審稿者；成果保留工作區，未 commit／push。
