---
docgraph:
  id: c5.adjacent-degree5-singleton-long-arc
  family:
    - c5
    - c5.degree5
  derives_from:
    - c5.adjacent-degree5-singleton-sectors
  requires:
    - c5.adjacent-degree5-shared-singleton
    - c5.no-spoke-supports
    - c5.single-spoke-two-two-external
---
# 相鄰雙 degree-5：共鄰單點 01 長弧的指定雙列分離

後續（2026-09-28）：[12 長弧分離](c5_adjacent_degree5_singleton_middle_arc.md)
已完成本頁的下一窄題；728 筆必要記錄保留 296 筆，全接受雙列並接回
條件式出口。[34／40 來源排除](c5_adjacent_degree5_singleton_end_arc.md) 再完成
全部 singleton 支援；下文 01／23 證書及當輪停止點保持原範圍。

2026-09-28。接續 [同側限制](c5_adjacent_degree5_singleton_sectors.md)。
**唯一 mixed 分量為共鄰 singleton x，且 x 接 {b0,b1} 時，接受 T4 的
disk minimal q-core 必接受 p₁=01021、p₂=01212。** q=01012 固定。
相同結果由完整反射搬運至 x 接 {b2,b3}。這完成原五個相鄰長弧位置中的
兩個；{b1,b2}、{b3,b4}、{b4,b0} 仍保留，下一入口見 [HANDOFF](HANDOFF.md)。

證明先以原三角形 xzw 的外側次序化約任意大小來源，再以原 r–x–B
路徑抽取 K5，最後用完整分量禁色集合的有限上界接合。692 筆必要資料中，
356 筆由 K5 排除，40 筆違反 T4；保留 296 筆的 592 個指定查詢全接受。
每筆另保留四種二接點方向。這些數字不是來源圖數，也不證可實現性。

信任層為紙面拓撲／來源 minor 化約、沿用外部 degree-list 定理、Python
固定域證書；未新增 Lean theorem。不由 T4 與雙列接受直接推出完整 Σ。

## 1. 同一來源與兩側完整分量

G 是有限簡單 induced-C5 disk 圖，外圈 B=(b0,…,b4)，有效內部 H
連通；G 拒絕 q，刪任一非框邊後接受 q。z、w 相鄰、完整 degree=5，
其餘內點完整 degree=4。H−{z,w} 的唯一 mixed 分量是原單點 {x}，
N(x)={z,w,b0,b1}。此外假設 G 接受全部 T4。

每側沿用 [共鄰單點化約 §3–4](c5_adjacent_degree5_shared_singleton.md#3-每側的三種必要正常形)：

- (2)：原二接點分量 C_r，加一條原 root-spoke r–b_s；
- (2,1)：原二接點分量 C_r，加一份單接點原分量 D_r，沒有 root-spoke。

各二接點固定為 (u_r,v_r)，單接點為 a_r。對任何列 β，完整 tuple
關係先取所有 tuple 色集的交集 F_C(β)，再精確消去該**整份分量**。
E_r(β) 是 root list 扣去該側所有 F；由容量知 E_r 非空。全圖接受 iff

\[
\exists a\in E_z(\beta),\ b\in E_w(\beta),\ c\in
U\setminus\{\beta_0,\beta_1\},\quad |\{a,b,c\}|=3. \tag{1}
\]

這三色分別用在原 z、w、x。固定它們後，才在每份原分量選一個所有
接點避開其 root 色的完整 tuple。保留 zw、zx、wx 與 x 的兩條框邊。

q 下令 T={2,3}。前報告的 minimality 給非空 E_z,E_w⊆T，且至少一側
E_r=T。每側精確必要禁色形式為

\[
\begin{array}{ll}
(2):&q_s\in\{0,1\},\quad F_{C_r}(q)=\{1-q_s\}\cup(T\setminus E_r);\\
(2,1):&F_{D_r}(q)=\{h\},\quad
F_{C_r}(q)=\{1-h\}\cup(T\setminus E_r),\quad h\in\{0,1\}.
\end{array} \tag{2}
\]

下面不把 (2) 套到 target；target 禁色須由同一 actual support 另行限制。

## 2. 原三角形外側給固定長弧次序

**每個 unary 分量的 actual support 至少兩點。** 每份 F_C(q) 非空且
容量≤2。若不碰 B，全色置換保持 F，故只能是空集，矛盾。若只碰一個
色 a，另外三色的置換迫使 F={a}。固定 root=a 後，所有外部鄰色只有 a；
拒絕 degree lists 的 tightness 使每點至多一個外鄰居，故 deg_C≥3。
但前報告已由原 r–x–B 外部 hub 排除 K4，而有限 K4-free Gallai tree
必有 deg_C≤2 的 leaf-block 非 cut 點，矛盾；singleton C 也不例外。
同理，每個 f∈F_C(q) 都要求 |q(S_C)∪{f}|≥2。

這是 [no-spoke 支援引理](c5_no_spoke_supports.md#2-每份支援至少兩點且有環狀區塊次序)
的局部版本；只使用完整 degree=4、非空容量≤2 的 F、原外部 hub。
拒絕時的 tightness、Gallai／blockwise palettes 沿用
[Dvořák Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，
本輪已核對原文；它是外部定理，並非 Python 或 Lean 證明。

三角形 xzw 的有界內側沒有其他有效頂點：若有，所在原 unary 分量
不能跨越三角形去碰 B，與前段矛盾。因此所有 unary 接線及 root-spokes
均在這個三角形的外側。取其閉內部的小正則鄰域，外側形成一個 annulus。
沿內圓周，各 x、z、w 的外側入射邊各佔一個連續區塊；x 的區塊恰是
xb0、xb1，其餘是 z、w 的兩個區塊，順序可互換。

同側定理已把 H−x 放在 b1–b2–b3–b4–b0 的長弧一側。沿 xb1、xb0
切開上述 annulus，得到四個具名單位的線性次序：每個 root 的兩個單位
是 C_r 與其 spoke／D_r，它們相鄰，但內部次序均可反轉。

每個原 C 的兩個 contact 也成連續區塊。否則 C 內連接兩 contact 的
簡單路徑，加回兩條 root 邊，給完全位於 disk 內的 Jordan 曲線；
被夾在不含 B 側的另一單位無法到達 B。外圓周附件亦保持同序：在同一
C 中連接兩條 boundary 附件得到 crosscut，不含內圓周的一側不能再有
另一單位的附件。相同 b_i 處先分開原入射邊端，仍記作同一框點。
這正是 no-spoke 的 annulus 引理；此處另保留三角形給的 root 分組。

以 L=(1,2,3,4,0) 的位置 0,…,4 記每個 actual support 的提升 Ŝ。
對這四個單位的原次序 O，有

\[
\max\widehat S_{O_j}\le\min\widehat S_{O_{j+1}}. \tag{3}
\]

分量支援至少兩點、spoke 支援恰一點。等號允許不同原分量共用框點，
不複製其色；支援可有間隙，不要求等於整條區間。z 的兩單位相鄰，w
亦然。兩 root 的次序有兩種，每側單位次序各兩種；二接點方向另各兩種。
此化約只讀取原嵌入，不改動 coloring 所在的 G 或任何完整關係。

## 3. 原 r–x–B 路徑排除雙禁色來源

對任一原 C_r，若 F_C(q)=F 有兩色，沿用
[原 bridge 路徑及逐塊 residual](c5_single_spoke_two_two_minor.md#2-路徑塊-residual-的穩定子引理)：
原接點間是一條奇數長 bridge 路徑 P。刪掉 P 的邊，含其每個點 v_j
的原連通塊 W_j 保留全部旁支；每個 actual support T_j 都滿足

\[
D(F)\subseteq q(T_j),\qquad
D(F)=F\ (3\notin F),\quad D(F)=U\setminus F\ (3\in F). \tag{4}
\]

此處 C 的外部仍只有 B 與 r；拒絕 lists、兩個原接點、degree=4 與
K4-free 的局部前提全部相同。另一 degree-5 root 不鄰接 C，不改變此證明。

若 D(F) 的兩個色在 S_C 中各只有一個供應點 b_a、b_b，則每個 W_j
都實際接到兩者。若 a,b 相鄰且 h∈{0,1}∖{a,b}，**原路徑 r–x–b_h**
內部避開 C 與 B。令 J=P 加回兩條原 r-contact 邊，取 P 上任意相鄰
v_j,v_{j+1}。下列五組是來源 K5 minor：

\[
W_j,\quad W_{j+1},\quad
Z=(V(J)\setminus\{v_j,v_{j+1}\})\cup\{x\}\cup(B\setminus\{b_a,b_b\}),
\quad\{b_a\},\quad\{b_b\}. \tag{5}
\]

Z 包含 r；原 rx、xb_h 把 J 剩餘路徑接到三點補弧，所以 Z 連通。
各 W 只含 C 的內點，且不含 J 的其他路徑點；五組因此互不相交。
P 原邊給 W_j–W_{j+1}，J 的兩條其餘鄰邊給它們到 Z，四條 actual
tethers 給它們到 b_a、b_b，三條框邊給最後三個 branch sets 的三角形。
全部十條鄰接皆為原邊。這是
[外部路徑 K5](c5_single_spoke_two_two_external.md#2-補弧外部路徑與一般-k5-抽取)
的原 x 版本，r 的 degree、spoke 數不參與 minor 抽取。

不能在同色有多個供應點時任挑一點，也不能在 {a,b}={0,1} 時使用此
rx 路徑。checker 明確檢查這兩個限制。此排除不需 T4 或 target 拒絕。

## 4. 完整集合的有限接合

對一份 actual support S、原禁色 F_C(q)，若某 σ∈S₄ 在 S 上把 q
搬到 β，整份原關係及 F 都由同一 σ 搬運，故 F_C(β)=σF_C(q)。
所有可用 σ 必給相同集合；否則此 q 資料已違反穩定子必要條件。

無相容 σ 時，保留所有滿足以下條件的**整份集合** F′：

1. |F′|≤原接點數，允許空集；
2. 逐色固定 β(S) 的每個色置換都保持 F′。

這是上界，不要求其中各選項可實現。對每種完整 F′ 選擇，精確算兩側
E，再檢查式 (1)。若每種選擇都接受，就證該列延拓；若每種選擇都拒絕
某 T4 列，就排除來源；其餘保留未決。從不把不同接點 marginals 相乘。

有限域完全由 (2)、(3)、q 穩定子與至少兩外部色的條件指定：

| 兩側分拆 | 幾何支援配置 | 最終保留、兩列皆接受 |
| --- | ---: | ---: |
| (2) / (2) | 376 | 144 |
| (2) / (2,1) | 88 | 68 |
| (2,1) / (2) | 88 | 68 |
| (2,1) / (2,1) | 8 | 16 |

幾何配置尚未指定禁色，故最後一欄可能大於前欄。全部 560 份幾何資料
與禁色接合得 692 筆，式 (5) 排除 356 筆，再以全部 120 份具名 T4 列
檢查剩餘 336 筆，排除 40 筆。最後 296 筆全部二接點分量在 q 只禁一色；
這是套表的結果，不能事先當 target 的容量上限，target 仍保留容量二。
兩個 target 的 x list 皆為 {2,3}；保存的每份候選 E_z/E_w 均有具體
三色 witness (z,w,x)，故 **592 個查詢接受、0 個未決**。

任意大小覆蓋由 §1–3 的來源論證負責；有限上界的逐項核對由
[checker](../scripts/c5_adjacent_degree5_singleton_long_arc.py)、
[JSON](../artifacts/c5_adjacent_degree5_singleton_long_arc/observations.json) 與
[692 筆表](../artifacts/c5_adjacent_degree5_singleton_long_arc/support_table.md) 負責。
不由這份有限資料斷言任意 support 可嵌入或任意禁色組合可實現。
前兩輪的 240 筆抽象關係與 20 個位置證書保持不變。

## 5. 全來源反射與出口接合

取 ρ(i)=3−i mod 5、π=(0 1)，對整張來源及全部接線反射，列搬運為
(Tβ)_i=π(β_ρ(i))。有 Tq=q，{0,1} 搬至 {2,3}，並且

\[
Tp_1=21010=(0\ 2)p_2,\qquad Tp_2=02012=(1\ 2)p_1.
\]

因此 01 來源的雙列分離亦證 23 來源的雙列分離。checker 對每份保留
資料搬運 supports、禁色與兩個 target，核對 592 次共同色框接合；沒有
只正規化 target 而固定其餘來源資料。接點身份不變，嵌入次序整體反向。

若 M 是雙缺失來源 Σ(G)=Ω∖{p,q} 的 minimal q-core，刪邊繼承給
Σ(M)⊇Ω∖{p,q}，其 q-aligned p 恰為 p₁ 或 p₂。M 符合本報告 01／23
前提時必接受 p，故 **Σ(M)=Ω∖{q}**，可接回
[條件式單側出口](c5_single_sided_exit.md)。這一步明用雙缺失來源與繼承；
本報告的一般 T4 來源只證指定雙列，沒有另外宣稱完整 Σ。

## 6. 重播、控制與停止點

新證書保存 source／直接輸入 SHA256、全部具名支援、四種 binary 接點
方向、K5 或 T4 排除見證，以及保留項的完整候選 F、E 與接合色對。
幾何域由遞增區間生成與獨立 Cartesian hull 分離兩種方法一致重算。
另核對 root 名字交換；108 份原 x 路徑 K5 skeleton 涵蓋五邊框的可用
tether pair、兩個 landing、長度 1／3／5 的每條 bridge 與直接／共幹
tethers。每份刪原 rx 後，指定 witness 必失效；不宣稱刪後整圖平面。
skeletons 不是完整 degree/list 來源。另保存完整 binary relation 與其
marginal 乘積不同禁色的負控制。

```bash
python3 scripts/c5_adjacent_degree5_singleton_long_arc.py --check
python3 scripts/c5_adjacent_degree5_singleton_sectors.py --check
python3 scripts/c5_adjacent_degree5_shared_singleton.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_single_spoke_two_two_minor.py --check
python3 scripts/c5_single_spoke_two_two_external.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際執行範圍見 [當輪紀錄](history/2026-09-28-adjacent-singleton-long-arc.md)。
未新增 Lean theorem；build 不形式化 annulus、Gallai 或 K5 抽取。
下一題是 x 接 {b1,b2} 的長弧，保留原 root 區塊與所有支援；此時 q、
p₁ 的 x list 為 {2,3}，p₂ 的 x list 為 {0,3}，須同步重算完整接合。
{b3,b4}／{b4,b0}、較大／多 mixed 分量、一般雙 root、degree≥6、
一般單側／共同出口與 K∞=K≤5 仍未證。
