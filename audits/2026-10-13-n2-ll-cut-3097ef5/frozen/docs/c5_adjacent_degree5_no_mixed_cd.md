# 無 mixed C–D：三飽和原分量的來源 K5 排除

後續（2026-09-29）：[C–E 五正跨度與原路徑排除](c5_adjacent_degree5_no_mixed_ce.md)
完成一側 t=0,(2,2)、D=1、O=0，另一側 t=0,(2,1,1) 及交換型。
96 份必要支援全 source K5；108 個正向原 IDs 無相容支援，0 target，不需 T4。
累計十三類／3,116 份覆蓋，兩類／432 份保留；下文保留當輪語境，
目前入口見 [weak-deletion 導覽](c5_weak_deletion_guide.md)。


2026-09-29。**C–D 及整圖 root 交換型 D–C 的 disk 來源全部排除。**
144 份正向原接合接上 240 份幾何，得到 640 份必要支援，全有原路徑
source K5；576 份三個飽和分量各有見證，其餘 64 份各有兩個。
72 個原 IDs 無相容支援；保留支援、target 查詢與新增 target 接受均為零。
不需 T4，不限制四個原分量大小，兩 root 均無 spoke。

證據是任意大小紙面化約、沿用外部 degree-list 定理及 Python 固定域證書；
未新增 Lean theorem。必要支援與 minor skeleton 不證 disk 實現。
一般／共同出口、任意來源完整 Σ、一般交換完備性及 K∞=K≤5 仍未證。
目前停止點由 [weak-deletion 導覽](c5_weak_deletion_guide.md) 維護。

## 1. 同一來源與完整有序關係

依賴 [no-mixed 化約](c5_adjacent_degree5_no_mixed.md)、[root 預算](c5_root_degree_excess.md)、
[C–C 四分量覆蓋](c5_adjacent_degree5_no_mixed_cc.md) 及
[A–C 飽和原路徑](c5_adjacent_degree5_no_mixed_t2_t0_pairs.md)。
M 有限簡單，B=(b0,…,b4) 是 induced C5 disk 外框，H=M−B 非空連通。
M 拒絕 q=01012，刪任一非框邊後接受。相鄰 z,w 完整 degree=5，其餘
內點完整 degree=4；H−{z,w} 無 mixed。兩 root 各接兩份不同原二接點
分量 (Cz,Dz)、(Cw,Dw)，沒有 boundary spoke。保留四分量、八具名
contacts、原 zw、全部原 bridges、旁支、actual boundary 附件與共同色框。

令 U={0,1,2,3}，T_C(t) 是原 C 的完整有序接點關係，
F_C(t)=⋂_{τ∈T_C(t)}set(τ)。接點 slack 給 T_C 非空且 |F_C|≤2。
Source 預算為 (D_z,O_z,κ_z)=(1,0,0)、(D_w,O_w,κ_w)=(0,1,0)，
minimality 迫共同 residual E_z(q)=E_w(q)={c}，且

\[
(F_{Cz},F_{Dz})(q)=(\{a\},U\setminus\{c,a\})\quad\text{或反序},
\qquad a\in U\setminus\{c\},
\]
\[
(F_{Cw},F_{Dw})(q)=(\{h,r\},\{h,s\}),\qquad
\{h,r,s\}=U\setminus\{c\}.
\]

w 側共享禁色 h 不表示共享內點；四原分量仍互異。4·6·6=144 份
有序接合獨立重建後，逐項等於原 retained-join IDs 與 C–C frontier；
首項 join=4、sides=(16,30)。整圖交換另對回 144 份反向原 IDs，並非
把 roots 或同側分量商掉。Source 預算不施加於 target。

逐 contact 邊 minimality 的 release witnesses 給每色 singleton 禁色
95 份完整 binary schemas；pair K={a,b} 的完整關係恰為 {(a,b),(b,a)}。
Checker 重核 65,535 份非空 binary relations，得到 380＋6 份 schemas，
再以 actual support 的 q 穩定子篩選完整 tuples；沒有用端點 marginals 相乘。

## 2. 無 spoke 的四正跨度與必要覆蓋

[C–C §2](c5_adjacent_degree5_no_mixed_cc.md#2-無-spoke-外部路徑與四正跨度)
只用四份禁色均非空真子集、每分量有兩 contacts，並不要求兩側預算相同，
因此整份適用於 C–D。具體而言，空 support 會使完整關係及 F_C 在 S4
下不變，與非空真禁色矛盾。各分量都有原 contact—分量內部—B 路徑。
對任一 r 側 C，經原 rs 及另一 root 的原分量得到避開 C 的 r–B 路徑。
外部 hub 排除 C 的 K4 block；非空禁色給 tight Gallai tree。此處沿用
既有 degree-list 外部定理與 hub 引理，本輪未重新查核外部文獻。

若 actual support 只見一個 q 色 d，固定 d 的 S3 穩定子無不變二元
子集，故 pair 禁色不可能；singleton 禁色則必為 {d}。固定 root=d
時所有外鄰同色，tightness 迫每點內度至少三，與 K4-free Gallai leaf
block 的私有點內度至多二矛盾。因此四份 supports 都至少見兩色、正跨度。

原 zw 細正則鄰域外，各 root incidences 成一段。同分量 contacts 必相鄰：
否則原內部路徑加兩 root 邊圍出的 Jordan 曲線把別的 incidence 困在
不含 B 的內側，而它可經另一原分量或 zw 到 B，矛盾。因此必要 cyclic
word 為 perm(Cz,Dz)perm(Cw,Dw)。切在 Cz，共四個具名 words；每個
保留四個 binary contacts 的 16 種方向，沒有新增 spoke。

Annulus 次序給同序 lifts T_j⊂Z：前一 max≤後一 min，最後 max≤首個
min＋5，允許共端點，稀疏支援不補洞。四個正跨度和≤5，各至多二。
沿 lifts 與獨立沿兩側 hull／框邊 masks 生成，均得到 240 份幾何、各一
placement，核對 3,840 份 rotations。這與 C–C 共用幾何函式，但重新
接合 C–D 的禁色與完整 schemas，得到 **640 份必要支援**。

72 個原 ID 有支援，另外 72 個空纖維標為 `no_compatible_disk_support`，
不記 minor 或 target。共同 residual c=0,1,2,3 分別有 188、188、96、168
份，沒有只取未用色 3。此為任意大小 disk 來源的必要覆蓋，並非實現分類。

## 3. 三個原飽和分量與固定框弧

令 Pz 為 z 側唯一 pair 禁色分量。分別檢查 Pz、Cw、Dw，對任一
C 及 K=F_C(q)，沿用 [原路徑引理](c5_adjacent_degree5_no_mixed_t2_t0_pairs.md#3-飽和二禁色分量的原路徑-k5)：
兩原 contacts u,v 間有奇數長原 bridge 路徑 P=x₀…xℓ。刪除 P 的全部
邊後，含 x_j 的路徑塊 W_j 保留全部旁支，rooted residual palette 恰為 K。
其全部 actual support 屬於必要族

\[
\mathcal T(q,S_C,K)=\{T\subseteq S_C:\operatorname{Stab}(q(T))\text{ 保持 }K\}.
\]

取同一三個非空連通框弧 B=X⊔Y⊔D_B，使族中**每個** T 都碰 X、Y，
並取避開 C、內部不碰 B 的原 r–B 路徑 L，落點在 D_B。L 經同側
另一原分量，或經原 zw 及另一側原分量；不要求不同見證的 L 彼此不交。
令 J=P∪{ru,rv}，五個 branch sets 是

\[
W_0,\quad W_1,\quad
(V(J)\setminus\{x_0,x_1\})\cup V(L)\cup D_B,\quad X,\quad Y.
\]

第三組經 r 連通，長度一亦保留 r。原 bridge、朝外兩圈邊、兩塊各到
X/Y 的附件及 C5 三切口給十鄰接。五組不交，故是來源 K5 minor。
各塊可用不同附件供應點，但必共用同一框弧分割，不能逐塊另選分割。

| Pz 有見證 | Cw 有見證 | Dw 有見證 | 必要支援數 |
| --- | --- | --- | ---: |
| 是 | 是 | 是 | 576 |
| 否 | 是 | 是 | 32 |
| 是 | 否 | 是 | 16 |
| 是 | 是 | 否 | 16 |

Record 0（join 40、sides=(17,31)）支援 Cz/Dz/Cw/Dw=01/04/12/234，
禁色 ({0},{1,3},{0,1},{0,3})。Dz 的路徑塊族只有 {04}；取 X=0、
Y=234、D_B=1、L=z–Cz₀–…–b1，即有原同側分量路徑 K5。

Record 104（join 70、sides=(18,37)）支援為 01/123/04/34，禁色
({0},{2,3},{0,2},{0,3})。Dz 的族 {12,23,123} 無共同框弧分割，
但 Cw 的族只有 {04}，取 X=0、Y=234、D_B=1、L=w–z–Cz₀–…–b1
即排除。同樣，records 16、40 分別無 Cw、Dw 見證，另兩份仍有。
所以固定只查一個飽和分量不足；本表任意兩個均已足夠，checker 保留三個。

任意大小來源落在必要表，每份都有上述 source K5，故本型 disk minimal
q-core 不存在。整圖交換 roots、所有歸屬及 contacts 給 D–C 同樣結論。
不需 T4；disk 外框是必要前提，不宣稱一般 planar C5 同樣排除。
此為來源排除，沒有把 1,280 個假想 target 查詢記為接受。

## 4. 證書與出口覆蓋

[Checker](../scripts/c5_adjacent_degree5_no_mixed_cd.py)、
[完整 JSON](../artifacts/c5_adjacent_degree5_no_mixed_cd/observations.json)、
[逐筆表](../artifacts/c5_adjacent_degree5_no_mixed_cd/support_table.md)
保存原 IDs／SHA、四份完整 schemas、八 contacts、rotations、空纖維、
三份路徑塊族、固定框弧、原外部路徑及反向 source IDs。

- 1,856 個成功的分量級見證，各重播長度 1、3、5 的原 bridge；另 512 次
  控制兩種外部路徑、雙塊 tethers、不同附件供應點及外部鏈長，合共 6,080 次。
  保存 1,856 份長度一證書與 512 份額外控制，共 2,368 份。
- 每個 minor 核對五組連通、不交、十鄰接、原 root 度數、actual supports，
  再核反射及 root 交換。有限 skeleton 不要求所有其他內點的 degree／lists，
  不證來源實現或任意大小拓撲引理。
- 640 份 literal source 反射、640 份整圖 root 交換及 1,280 份整分量交換，
  核對完整 schemas、路徑塊族及全部框弧／路徑見證。
- 13 個控制含只查單一分量的遺漏、逐塊另選分割、空族不作 minor 見證、
  移除原 zw／附件／bridge、branch sets 重疊、binary 改為 spoke、跨度三、
  marginals 失真及漏刪 root 對角線。

新增正反向 288 個原 IDs，累計 **十二類／2,828 份覆蓋，三類／720 份保留**。
C–E、D–D、D–E 分別保留 288、144、288 份（含交換方向）。下一窄入口
C–E 的 144 份正向 IDs 已綁定，首項 join 12、sides=(16,64)，尚未建立
其支援／target 表；不在本輪擴大研究。

[出口第九類](c5_single_sided_exit.md) 加入 C–D／D–C 來源排除分支。
實際核心不會落在此型；其他雙列分離分支仍須來源雙缺失及刪邊繼承才
接回完整 Σ，這些前提未移除。

## 5. 重播與信任界線

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_cd.py --check
PYTHONHASHSEED=17 python3 scripts/c5_adjacent_degree5_no_mixed_cd.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_cc.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t0_pairs.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證與未重跑範圍見 [當輪紀錄](history/2026-09-29-adjacent-no-mixed-cd.md)。
`--check` 重算後逐 byte 比對 JSON／表格；無參數只生成本層。
未新增 Lean theorem；`lake build` 不表示紙面 minor／annulus 已形式化。
本輪沒有獨立第二審稿者，成果保留工作區，未 commit／push。
