# 無 mixed B–D：雙飽和原分量與來源 K5 排除

後續（2026-09-29）：[C–C 無 spoke 四分量排除](c5_adjacent_degree5_no_mixed_cc.md)
完成兩側 t=0,(2,2)、各 D=1、O=0：1,176 份必要支援全部 source K5，
0 target 查詢，不需 T4。累計十一類／2,540 份覆蓋，四類／1,008 份保留；
下文保留當輪語境，目前入口見 [weak-deletion 導覽](c5_weak_deletion_guide.md)。


2026-09-29。**B–D 及整圖 root 交換型的 disk 來源全部排除。**
180 份原有序接合接上 780 份幾何，得到 312 份必要支援，全部有 source
原路徑 K5。288 份在 Cw、Dw 各自有見證，另各 12 份只由其中一個分量
的固定框弧規則排除。沒有保留支援，target 查詢及新增 target 接受均為零。
不需 T4。八份支援必須使用另一原分量的外部路徑，原 w–z–spoke 不足。

證據是任意大小紙面化約、沿用外部 degree-list 定理及 Python 固定域證書；
未新增 Lean theorem。必要支援與 minor skeleton 不是 disk 實現證書。
一般／共同出口、任意來源完整 Σ 與 K∞=K≤5 仍未證。
目前停止點見 [weak-deletion 導覽](c5_weak_deletion_guide.md)。

## 1. 同源前提與雙飽和完整關係

沿用 [no-mixed](c5_adjacent_degree5_no_mixed.md)、[root 預算](c5_root_degree_excess.md)、
[B–C 四分量覆蓋](c5_adjacent_degree5_no_mixed_bc.md) 及
[A–D 雙飽和原路徑](c5_adjacent_degree5_no_mixed_t2_t0_overlap.md) 的前提與引理。
M 有限簡單，B=(b0,…,b4) 是 induced C5 disk 外框；H=M−B 非空連通。
M 拒絕 q=01012，刪任一非框邊後接受。相鄰 z,w 完整 degree=5，其他
內點完整 degree=4；H−{z,w} 無 mixed。z 有一條原 spoke z–b_i、二接點
Cz 與單接點 Dz；w 無 spoke，有二接點 Cw、Dw。四原分量可任意大；
保留七具名 contacts、zw、全部原 bridges、旁支、actual attachments 與共同色框。

令 U={0,1,2,3}，T_C(t) 是完整有序接點關係，F_C(t)=⋂_{τ∈T_C(t)}set(τ)。
接點 slack 與既有 degree-list 引理保證 T_C 非空且 |F_C|≤接點數。
Source 預算分別為 (D_z,O_z,κ_z)=(1,0,0)、(D_w,O_w,κ_w)=(0,1,0)。
Minimality 給共同 residual {c}，所以有

\[
(F_{Cz},F_{Dz})(q)=(\{a\},\{d\}),\qquad \{a,d\}=U\setminus\{q_i,c\},
\]
\[
(F_{Cw},F_{Dw})(q)=(\{h,r\},\{h,s\}),\qquad \{h,r,s\}=U\setminus\{c\}.
\]

按 i 的五選擇、c 的三選擇、(a,d) 的兩次序及 (h,r,s) 的六次序，獨立
重建恰為 180 份，逐項等於原表及 B–C frontier 的 IDs。首項 join 2128、
sides=(91,30)。保留 Cw/Dw 的有序身份，不把共享禁色 h 當成共享內點。

逐 contact 邊 minimality 的 release witnesses 給 Cz 每禁色 95 份 binary
schemas；Dz 關係恰為 {(d)}。兩個飽和分量分別有完整關係
{(h,r),(r,h)}、{(h,s),(s,h)}，不能用 marginals 的乘積代替。
Checker 遍歷全部 65,535 份非空 binary relations，重核 380 份 singleton、
六份 pair schemas；再以各 actual support 的 q 穩定子檢查完整 tuple 集合。

## 2. 四分量正跨度與必要環序

此處沿用 B–C §2 的拓撲引理，與 w 側是缺額還是重疊無關。
對 z 側分量，原 z–b_i 避開它；對 w 側分量，原 w–z–b_i 避開它。
外部 hub 排除 K4 block。非空禁色使扣 root 色後的拒絕 residual 為 tight
Gallai tree。此步沿用既有 degree-list 外部定理，本輪未重新查核文獻。
空支援違反全色對稱；只見一個 q 色時，pair 禁色違反色穩定子，singleton
禁色必為該色，tightness 迫每點內度至少三，違反 K4-free Gallai leaf block
有私有點內度至多二。因此四份 actual supports 各見至少兩色，皆有正跨度。

原 zw 細正則鄰域把兩 root incidences 各排成一段；原分量內路徑與其他
incidence 到框的路徑迫同分量 contacts 連續。必要 cyclic word 是

\[
\operatorname{perm}(Cz,Dz,z0)\operatorname{perm}(Cw,Dw).
\]

Annulus 次序使 actual supports 在 [0,5] 的 lifts 同序成塊，可共端點，
前一 max≤後一 min；四份正跨度之和≤5，故每份跨度至多二。
稀疏支援不填洞。按 lifts 與獨立按兩側 hull／框邊 masks 生成的集合
相等，均為 780 份，各一 placement。12 個 cyclic words 各含三 binary
的八種 contact 方向，核對 6,240 次 rotations，兩 root 度數均保留五。

接合本輪 source 禁色及完整 schemas 後為 312 份必要支援；72 個原 IDs
有支援，108 個是無相容 disk 支援的空纖維。空纖維不計 minor 或 target。
共同 residual c=0、1、2、3 各有 8、8、16、280 份；沒有只取未用色 3。

## 3. 兩個原 pair 分別取固定框弧

對 C=Cw 或 Dw，設其 source pair 為 K。沿用
[A–C 原路徑引理](c5_adjacent_degree5_no_mixed_t2_t0_pairs.md#3-飽和二禁色分量的原路徑-k5)：
兩原 contacts u,v 由奇數長原 bridge 路徑 P=x₀…xℓ 連接。
刪除全部 P 邊後，含 x_j 的路徑塊 W_j（包含全部原旁支）有 rooted
residual palette K。令 T_j 為其全部 actual boundary support，則

\[
T_j\in\mathcal T(q,S_C,K)
=\{T\subseteq S_C:\operatorname{Stab}(q(T))\text{ 保持 }K\}.
\]

選同一份連通三框弧分割 B=X⊔Y⊔D_B，使族中每個 T 同時碰 X、Y，
且有避開 C 的原 w–B 路徑 L 落在 D_B。L 可經原 spoke、另一 w 分量，
或 zw 加任一 z 分量；取首次到 B 的段，不加邊。設 J=P∪{wu,wv}，則

\[
W_0,\quad W_1,\quad
(V(J)\setminus\{x_0,x_1\})\cup V(L)\cup D_B,\quad X,\quad Y
\]

是五個不交連通 branch sets。原 bridge、朝外的兩圈邊、兩路徑塊各到
X/Y 的實際附件及 C5 三個切口給十對鄰接。這是同一來源的 K5 minor；
附件供應點可以不同，但不得逐塊改用不同的框弧分割。

| 本規則在 312 份支援的結果 | 份數 |
| --- | ---: |
| Cw、Dw 各自有 K5 | 288 |
| 只有 Cw 有本規則見證 | 12 |
| 只有 Dw 有本規則見證 | 12 |
| 兩者皆未排除 | 0 |

Record 0 即原 join 2128，支援 Cz/Dz/z0/Cw/Dw=01/04/0/12/234，
禁色 ({1},{2},{0,1},{0,2})。Cw 路徑塊族只有 {12}，取
X=1、Y=234、D_B=0、L=w–z–b0 即得 source K5。

Record 4（join 2129、sides=(91,32)）支援為 01/04/0/123/34，
禁色 ({1},{2},{0,1},{1,2})。Cw 的族為 {12,23,123}，沒有一份框弧
分割通吃全族；Dw 的族只有 {34}，取 X=123、Y=4、D_B=0 與同一 L
即可排除。只查第一個 pair 會漏掉 12 份；只查第二個亦漏 12 份。

**不能直接套用 A–D 的「原 spoke 足夠」結論。** Record 30（join 2927、
sides=(129,32)）支援是 01/04/4/123/34，禁色 ({1},{0},{0,1},{1,2})。
Dw 仍取 X=123、Y=4、D_B=0；原 spoke 落在 b4，不能當此分割的外部路徑。
改取原 w–z–Cz₀–…–b0，內部避開 Dw 與 B，便有 K5。
共有八份支援在任一 pair 上都無 spoke-route 見證，但有原分量路徑見證。
新增 Dz 始終是原分量，沒有壓成 spoke。

任意大小來源必落在上述必要表，每份都違反 disk 平面性，故本型不存在。
整圖交換 roots、所有分量歸屬、contacts 與 spoke 保持此反證，D–B 亦排除。
這是來源排除，不記作 624 個 target 接受。

## 4. 證書、覆蓋與重播

[Checker](../scripts/c5_adjacent_degree5_no_mixed_bd.py)、
[完整 JSON](../artifacts/c5_adjacent_degree5_no_mixed_bd/observations.json)、
[逐筆支援表](../artifacts/c5_adjacent_degree5_no_mixed_bd/support_table.md)
保存來源 IDs／SHA、空纖維、完整 schemas、四分量支援、七 contacts、rotations，
及兩個飽和分量分開的框弧／原外部路徑見證。
600 個成功的分量級見證各重播路徑長度 1、3、5，共 1,800 次；另 768 次
控制三種原外部路徑、雙塊 tether 形狀、不同附件供應點與外部鏈長，總計
2,568 次 minor controls，每份另核對反射及 root 交換。
全部 312 份亦逐項核 source 反射、完整關係搬運、整分量交換及整圖 root 交換。
13 個負控制涵蓋遺失原邊、分量／marginal 替代、逐塊另選框弧、只查一個 pair、
只用 spoke 及 branch sets 重疊。有限 skeleton 不要求其餘內點 degree／lists，
不是來源實現或任意大小拓撲的機器證明。

本輪正反向新增 360 個原 IDs，累計十類／2,396 份覆蓋，五類／1,152 份
保留。[出口第九類](c5_single_sided_exit.md) 加入 B–D 來源排除分支；
實際核心不會落在此型。其他分支的完整 Σ 仍另用來源雙缺失與刪邊繼承。

下一窄入口 C–C：兩側 t=0,(2,2)，各 D=1、O=0。JSON 綁定其 144 份
原 IDs，首項 join 0、sides=(16,16)，尚未生成其支援或 target 表。
其餘 C–D、C–E、D–D、D–E 保留，當前排程見研究線導覽。

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_bd.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_bc.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t0_overlap.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證及省略範圍見 [當輪紀錄](history/2026-09-29-adjacent-no-mixed-bd.md)。
`--check` 重算後逐 byte 比對新 JSON／表格；無參數只生成本層。
`lake build` 不表示本輪紙面支援覆蓋與 K5 已 Lean 化。
