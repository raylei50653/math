# 無 mixed D–D：四飽和原分量的框邊與來源 K5 排除

後續（2026-09-29）：[D–E 五正跨度與雙飽和原路徑排除](c5_adjacent_degree5_no_mixed_de.md)
完成最後一類及 root 交換型：48 份必要支援全 source K5，120 個正向原 IDs
無相容支援；0 target，不需 T4。no-mixed 十五類／3,548 份原接合全部覆蓋，
出口第九類涵蓋全部 no-mixed 分拆；一般／共同出口與 K∞=K≤5 仍未證。
下文保留各輪語境，目前入口見 [weak-deletion 導覽](c5_weak_deletion_guide.md)。

2026-09-29。**D–D 的 disk 來源全部排除。**兩側 t=0,(2,2)、各
D=0、O=1 的 144 份原接合接上 240 份幾何，得到 352 份必要支援，
全部有 source K5；80 個原 IDs 無相容支援。四正跨度中至少三份為一，
選其中一個飽和原分量，其兩框點與補弧給統一 minor。
不需 T4，不限制原分量大小，0 target 查詢。

證據為任意大小紙面化約、沿用外部 degree-list 定理及 Python 固定域
證書；未新增 Lean theorem。必要支援與 minor skeleton 不證 disk 實現。
一般／共同出口、任意來源完整 Σ、一般交換完備性與 K∞=K≤5 仍未證。
目前停止點由 [weak-deletion 導覽](c5_weak_deletion_guide.md) 維護。

## 1. 原來源、預算與完整有序關係

依賴 [no-mixed 化約](c5_adjacent_degree5_no_mixed.md)、
[root 預算](c5_root_degree_excess.md)、[C–C 四分量幾何](c5_adjacent_degree5_no_mixed_cc.md)、
[C–E 前序](c5_adjacent_degree5_no_mixed_ce.md) 及
[飽和原路徑引理](c5_adjacent_degree5_no_mixed_t2_t0_pairs.md#3-飽和二禁色分量的原路徑-k5)。
M 有限簡單，B=(b0,…,b4) 是 induced C5 disk 外框，H=M−B 非空連通。
M 拒絕 q=01012，刪任一非框邊後接受 q。相鄰 z,w 完整 degree=5，
其餘內點完整 degree=4；H−{z,w} 無 mixed。兩 root 均無 boundary
spoke，各接兩份不同原二接點分量 (Cz,Dz)、(Cw,Dw)。保留四原分量、
八具名 contacts、原 zw、所有原 bridges／旁支、actual boundary 附件與共同色框。

令 U={0,1,2,3}，T_C(t) 是原 C 的完整有序接點關係，
F_C(t)=⋂_{τ∈T_C(t)}set(τ)。接點 slack 保證 T_C 非空且 |F_C|≤2。
兩側 source 預算均為 (D,O,κ)=(0,1,0)，minimality 迫
E_z(q)=E_w(q)={c}。各側 r 有

\[
(F_{Cr},F_{Dr})(q)=(\{h_r,a_r\},\{h_r,b_r\}),\qquad
(h_r,a_r,b_r)\in\operatorname{Perm}(U\setminus\{c\}).
\]

共享禁色 h_r 不表示共享內點。4·6·6=144 份有序接合由此獨立重建，
逐項對回原 join／side IDs 與 C–E frontier，首項 join=424、sides=(30,30)。
整圖 root 交換仍在同一 144 IDs 內，沒有另計 144 份或將 roots 商掉。
Source 預算不作 target 等式。

每份二禁色 K={a,b} 已迫完整關係恰為 {(a,b),(b,a)}：每個 tuple
必含 a,b，逐 contact 刪邊的 release witnesses 要求兩種次序皆存在。
Checker 重核既有 65,535 份非空 binary relations 的 schema audit，
並對六個 pair schemas 核對這一精確關係及座標反序；本型不使用 singleton
schemas。按 actual support 的 q 穩定子篩選完整 tuples，沒有以 marginals
相乘，也不假設不同分量的 schemas 可獨立實現。

## 2. 四正跨度中至少三條框邊

每份 F_C(q) 是二元集。若 actual support S_C 只見一個 q 色 d，固定
色 d 的 S3 穩定子沒有不變二元子集，與 F_C 的不變性矛盾；空支援也
不可能。因此四份 supports 都至少見兩色且有正跨度。

每個原分量均有 contact—內部路徑—B 的原路徑。對任一 r 側分量 C，
同側另一分量或原 rs 加另一側分量給避開 C 的 r–B 原路徑。
沿用 degree-list tight Gallai tree 與外部 hub 排除 K4 block 的既有
論證，適用任意分量大小；本輪未重新查核外部文獻。

[C–C §2](c5_adjacent_degree5_no_mixed_cc.md#2-無-spoke-外部路徑與四正跨度)
的原 zw 正則鄰域／annulus 論證不依賴缺額或重疊預算，故原樣適用。
兩 root 的 incidences 各成一段，同原分量的兩 contacts 必相鄰，否則
原內部路徑圍成的 Jordan 曲線困住另一個仍可走到 B 的 incidence。
必要 cyclic word 為 perm(Cz,Dz)perm(Cw,Dw)。切在 Cz 得四個具名
words，每個保留四對 contacts 的 16 種方向。

同序 lifts T_j⊂Z 滿足前一 max≤後一 min，最後 max≤首個 min＋5，
可共框端點，但不補稀疏支援的洞。令 s_j=max T_j−min T_j，則

\[
s_j\ge1,\qquad\sum_{j=1}^4s_j\le5.
\]

所以至多一份跨度為二，**至少三份跨度為一、支援恰為一條框邊兩端**。
四份 hull 的框邊不重疊，因此其他任一分量的正跨度支援均不可能包含於
這條框邊的兩端。這一步也保留同側另一原分量在補弧的實際附件。

沿 lifts 與獨立沿兩側 hull-edge masks 生成均得 240 份幾何、各一
placement，核對 3,840 份 contact rotations。接完整 q 關係後有
**352 份必要支援**，落在 64 個原 IDs；其餘 80 個空纖維明標
`no_compatible_disk_support`，不記 minor 或 target。
共同 residual c=0,1,2,3 各有 88 份，沒有只取未用色 3。
這是任意大小來源的必要覆蓋，不是 disk 實現分類。

## 3. 框邊飽和分量的統一原 K5

選跨度一的 r 側原分量 C，S_C={a,b}，a,b 為相鄰框點索引，
K=F_C(q) 為二元集。由飽和原路徑引理，兩原 contacts u,v 間有奇數長
原 bridge 路徑 P=x₀…xℓ。刪去全部 P 邊後，含 x_j 的路徑塊 W_j
保留全部原旁支，其 rooted residual palette 恰為 K。
W_j 的 actual support T⊆S_C 必使 Stab(q(T)) 保持 K。
空集或單點的穩定子不能保持二元集，因此每個 W_j 都同時碰 a,b；
必要支援族恰為 {{a,b}}。

取 X={b_a}、Y={b_b}、D_B=B−{b_a,b_b}。三組皆非空連通且兩兩
相鄰。同側另一原分量 C′ 有實際附件落在 h∈S_C′−{a,b}；經 r 的
原 contact、C′ 內簡單路徑到 b_h 得原 L。L 完全避開 C，內部不碰 B，
沒有新增 spoke。令 J=P∪{ru,rv}，五個 branch sets 為

\[
W_0,\quad W_1,\quad
(V(J)\setminus\{x_0,x_1\})\cup V(L)\cup D_B,\quad X,\quad Y.
\]

第三組經 r 連通，ℓ=1 時仍含 r。五組不交，原 bridge 給 W₀–W₁，
J 的兩條朝外邊給各 W 到第三組，W₀/W₁ 各到 X/Y 的四份附件及
三框弧切口給其餘相鄰，合共十對，故為來源 K5 minor。
任意 disk 來源都有跨度一分量，故全型排除；此紙面結論不依靠
有限表的逐列全稱代替任意大小拓撲。

Record 0：join=424、sides=(30,30)，支援 Cz/Dz/Cw/Dw=01/04/12/234，
禁色 ({0,1},{0,2},{0,1},{0,2})。取 C=Cz、X=0、Y=1、D_B=234、
L=z–Dz₀–…–b4 即得 minor。

Checker 另保存四個飽和分量的全部固定框弧見證：288 份四者皆有，
另外 64 份各有三個，缺 Cz/Dz/Cw/Dw 各 16 份。只固定查某一個分量會
漏掉來源，例如 records 48/120/16/40 分別無該分量見證；選跨度一分量
便避開此問題。每份記錄至少三個統一框邊見證（256 份有三個、96 份有四個）。

不需 T4；不宣稱一般 planar C5 具有相同 annulus 限制。這是來源排除，
沒有把 704 個假想 target 查詢記為接受。

## 4. 證書與覆蓋更新

[Checker](../scripts/c5_adjacent_degree5_no_mixed_dd.py)、
[完整 JSON](../artifacts/c5_adjacent_degree5_no_mixed_dd/observations.json)、
[逐筆表與原 ID 纖維](../artifacts/c5_adjacent_degree5_no_mixed_dd/support_table.md)
保留原 IDs／SHA、完整 schemas、四原分量／八 contacts、rotations、
空纖維、原路徑塊族、固定框弧、原外部路徑與 root 交換 IDs。

- 1,344 個分量級見證各重播 bridge 長度 1、3、5；另 512 次控制兩種
  外部路徑、兩塊 tethers、不同附件供應點及外部鏈長。每份支援另選一個
  統一框邊見證重播三種 bridge 長度，共 5,600 次，保存 2,208 份證書。
- 核對 branch sets 連通、不交及十鄰接、兩 root 完整度數、actual supports、
  反射及 root 交換。有限 skeleton 不要求其他內點滿足原 degree／lists，
  不是來源實現證書，也不形式化任意大小論證。
- 352 份 literal source 反射、352 份整圖 root 交換、704 份整分量交換，
  核對完整 schemas、路徑塊族及全部框弧／路徑見證。
- 14 個控制包括只查單一分量的遺漏、逐塊另選分割、空族不作 minor 見證、
  遺失 zw／原 bridge／外部附件、branch sets 重疊、binary 改為 spoke、
  跨度三、marginals 失真與漏刪 root 對角線。

新增 144 個原 IDs，累計 **十四類／3,260 份覆蓋，只剩 D–E 含交換型
一類／288 份**。D–E 的 144 份正向 IDs 已綁定，首項 join=432、
sides=(30,64)，尚未建立其支援／target 表。本輪不擴大處理 D–E。
[出口第九類](c5_single_sided_exit.md) 加入 D–D 來源排除分支；其他雙列
分離分支接回完整 Σ 仍須來源雙缺失及刪邊繼承，未移除其前提。

## 5. 重播與信任界線

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_dd.py --check
PYTHONHASHSEED=17 python3 scripts/c5_adjacent_degree5_no_mixed_dd.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_ce.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_cc.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t0_pairs.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證與未重跑範圍見 [當輪紀錄](history/2026-09-29-adjacent-no-mixed-dd.md)。
`--check` 重算後逐 byte 比對 JSON／表格；無參數只生成本層。
舊 scripts／artifacts 不改寫。`lake build` 不表示新紙面 topology 已形式化。
沒有獨立第二審稿者；成果保留工作區，未 commit／push。
