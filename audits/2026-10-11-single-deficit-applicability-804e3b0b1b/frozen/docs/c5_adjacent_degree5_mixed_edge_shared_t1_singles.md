---
docgraph:
  id: c5.adjacent-degree5-mixed-edge-shared-t1-singles
  family:
    - c5
    - c5.degree5
  derives_from:
    - c5.adjacent-degree5-mixed-edge-shared
  requires:
    - c5.adjacent-degree5-mixed-edge-shared-t1-pair
    - c5.adjacent-degree5-mixed-edge-shared-t2
    - c5.adjacent-degree5-singleton-long-arc
  related:
    - c5.single-sided-exit
---
# 共鄰端點 mixed K2：t_w=1、(1,1) 的飽和環序與雙列分離

後續（2026-09-29）：[t_w=0、(1,1,1) 六跨度排除](c5_adjacent_degree5_mixed_edge_shared_t0_singles.md)
已逐筆排除原 108 筆：四份 unary、v 的總跨度至少 6>5，不需 T4，0 target 查詢。
zu、zv、wu 共鄰端點接線的全部五型已完成，出口第八類移除 w 分拆限制。
原資料保持；下列通知與正文保留各輪語境，現行入口見 [HANDOFF](HANDOFF.md)。

後續（2026-09-29）：[t_w=0、(2,1)](c5_adjacent_degree5_mixed_edge_shared_t0_pair_single.md) 已由原 diamond 路徑 K5 及完整關係搬運完成：
102 筆必要支援排除 94，保留 8 的 16 查詢全接受，不需 T4。下文下一步
已被涵蓋；共鄰端點型只剩 t_w=0、(1,1,1)，現行優先序見 HANDOFF。

2026-09-29，接手基準 main@c178cf1。**本型必接受 p₁=01021、p₂=01212，
不需 T4，不限制原 unary 分量大小。** 原 72 筆正常形經同序 actual supports
接合，只剩 32 筆必要資料，64 個指定查詢全部接受。原正常形中 56 筆
無相容支援；本輪沒有新增來源 K5 排除，也不需要跨列 first-bridge 引理。

證據為任意大小紙面支援／環序化約、沿用外部 degree-list 定理與 Python
有限接合證書。必要資料不是來源圖數，未證 disk 可實現性；未新增 Lean
theorem，一般單側／共同出口與 K∞=K≤5 仍未證。優先序見 [HANDOFF](HANDOFF.md)。

## 1. 同一來源與 72 筆具名正常形

G 有限簡單，B=(b0,…,b4) 為 induced disk 外框，有效內部 H 非空連通。
固定 q=01012、U={0,1,2,3}；G 拒絕 q，刪任一非框邊後接受 q。
相鄰 z、w 完整 degree=5，其餘內點完整 degree=4。H−{z,w} 的唯一
mixed 原分量恰為 uv，root incidences 恰為 **zu、zv、wu**。
w 有唯一原 spoke wb_s，其 unary 接點分拆為 (1,1)。

[共鄰端點化約](c5_adjacent_degree5_mixed_edge_shared.md) 給 z 無 spoke，
恰有一份二接點原分量 C_z，具名接點 (x₀,x₁)；w 的兩份不同原分量
C_w0、C_w1 分別有接點 y₀、y₁。記 actual supports 為 S_z、S₀、S₁，
N_B(u)={b_i}、N_B(v)={b_j,b_k}，j≠k。全部邊、附件、bridges、接點
身份及同一色框保留。存在 {h,e,d}={0,1,2}，使

\[
q_i=h,\quad\{q_j,q_k\}=\{h,e\},\quad c=q_s\in\{h,d\},
\quad F_z(q)\in\{\{h\},\{h,d\},\{h,3\}\},
\quad F_0(q)=\{a_0\},\ F_1(q)=\{a_1\},\quad
\{a_0,a_1\}=U\setminus\{e,c\}.
\tag{1}
\]

F 是完整有序接點關係中全部 tuple 色集的交集；C_wℓ 的 q 關係恰為
{(a_ℓ)}。兩個具名禁色順序各保留，故有 6×3×2×2=72 筆。
若 |F_z(q)|=2，完整關係是兩個相反次序；若 F_z(q)={h}，仍保留原
95 個完整必要 schemas，再以 actual S_z 的逐色穩定子篩選整份關係。
未把兩個 z 接點投影後獨立相乘，也未把兩個 w 分量合併成二接點分量。

checker 獨立重建 (1)，與原 JSON 的 72 筆逐一核對，保存原 ID、完整
原記錄、局部 K2 支援 ID、全部原 schemas 與相容 schema IDs。
原 observations.json SHA256 為
`6b9b689c1f45b22feb182958c953b18989fe47655f69d5d2a17d8ed509555532`；
原 306／288 筆及 9,312 schemas 不改寫。

## 2. 三份 unary 的局部支援下界

對每份 C，唯一相鄰 root 是 r=z 或 w，另一 root 不在 C 內也不鄰接 C。
忽略 r 色時，原接點有 slack，故完整 R_C 非空；其禁色容量分別為二、一、一。
若 a∈F_C(q)，固定 r=a 後得到不可著色 degree lists，沿用
[前輪局部 degree-list／K4 論證](c5_adjacent_degree5_mixed_edge_shared_t1_pair.md#2-局部-degree-list-前提與-k4-排除)。
該段只需要 C 內每點完整 degree=4、所有外鄰在 B∪{r}，不要求恰有兩個
接點。因此也適用兩份單接點 C_wℓ；外部 degree-list tightness／Gallai
定理的信任層與前輪相同，本輪未另行核對外部原文。

具體地，K4 block 每點除 clique 外恰有一個方向，直達 B∪{r} 或經一條
原 bridge 進入旁支。刪 bridge 後兩側可著色，原拒絕迫使兩側根色為
同一 singleton；旁支若不碰 B∪{r} 就可自由換色，矛盾。四個方向因
block 結構互不相交，且原 r–u–b_i 路徑避開 C，將 B∪{r,u} 接成外部
hub；四個 clique 點與此 hub 給 K5 minor。故 C K4-free，Gallai blocks
只剩 bridges／odd cycles（以及整個 C 為 singleton 的可能）。

**每份 S_C 至少見兩個 q 色。** 空支援的全色對稱使非空 F 不可能有
容量≤2；若只見一色 a，固定 a 的穩定子迫使 F={a}。固定 r=a 後，
所有外鄰都只用 a。tightness 迫使每點最多一個外鄰，從完整 degree=4
得到 deg_C≥3；K4-free Gallai tree 的葉塊私有點卻有內度≤2，矛盾。
singleton C 的內度零同樣不可能。因此三份支援的 cyclic span 都至少一。

兩份 w 禁色中恰一個是 3。以 C₃ 表示這份原分量，只作角色稱呼、不改
其具名身份。固定 q(S₃) 的色置換必保持 {3}；若漏掉 q 色 h，交換 h、3
就矛盾。因此 **q(S₃)={0,1,2}，其跨度至少二**。

## 3. 原 diamond 外側同序與五邊飽和

原 diamond D 保留 zw、wu、uv、vz、zu。u、v、w 各有原 spoke 到 B，
z 經 C_z 到 B，路徑內部都避開 D。故四頂點同在 D 面向 B 的面上，
其面界是 Q_D=z–w–u–v–z，原 chord zu 位於另一側。三份 C 均連通且
碰 B，故都在 Q_D 外側。取 Q_D 閉內部的細正則鄰域，外側成 annulus。

z 外側只有 C_z 的兩條 contacts，形成一個區塊；w 外側有 C_w0、C_w1
各一條 contact 及原 spoke，保留三者的全部六種次序。u、v 外侧各有
一個原 boundary 附件區塊。因此內側六個單位的環序是

\[
C_z,\quad\operatorname{perm}(C_{w0},C_{w1},s),\quad u,\quad v
\tag{2}
\]

或整體反向。每個單位有連通細鄰域連接 annulus 兩邊界，單位間不交。
同一框點上的不同附件在小鄰域分開，框點身份及顏色仍相同。
沿用 [前輪 annulus crosscut 論證](c5_adjacent_degree5_mixed_edge_shared_t1_pair.md#3-c_w-二接點的-annulus-同序搬運)：
一單位連接兩個外端的 crosscut 所切下、不含內圓周的一側，不能包含
另一單位的外端，否則後者無法連回內圓周。故外端支援區塊與 (2) 同序。

從 C_z 的第一個外端切開，可將各 actual support 提升為整數集 T_A，
min T_Cz=a，前單位的 max≤後單位的 min，最後 max≤a+5，T_A mod5=S_A。
同一支援首尾若重複同一框點就佔滿一圈，與其餘正跨度單位矛盾，故
每份跨度<5。允許不同單位共享端點與支援內有間隙，不先取最短 cyclic hull。

兩套獨立算法（遞增 lifts／不交 hull-edge masks 與整個 w 區間）均給
**780** 份幾何及 780 個 placements，再接合 (1) 與完整關係穩定子。
更強的紙面限制是

\[
\operatorname{span}(C_z)+\operatorname{span}(C_3)
+\operatorname{span}(C_{w\ne3})+\operatorname{span}(v)\ge1+2+1+1=5.
\tag{3}
\]

總跨度≤5，故全為等號，區塊間沒有正長間隙：C₃ 恰佔三個連續框點，
其餘三份恰各佔一條框邊；spoke 與 u 的零跨度端點仍依 (2) 放置。
C₃ 的三色條件只容許 234、340、401，完整接合另排除 340。
最後 **32 筆**來自 16 個原正常形，其餘 56 筆纖維為空；每筆保存兩個
具名 z-contact 次序，並核對 (3) 的等號與支援內無間隙。
原必要表的計數只縮到幾何／色關係的必要資料，非來源實現定理。

## 4. 同一色框的完整禁色上界與指定雙列

對任意 target β，在同一原 C 與 actual S 上，若 σq|S=β|S，整份關係
經 σ 搬運，故 F_C(β)=σF_C(q)。否則枚舉容量≤k_C 且受 β(S) 逐色
穩定子保持的全部 F 候選，包括空集。真實 F 必在其中；只要求對每組
候選都能延拓，不宣稱候選可實現，也不讓同一來源跨列自由選 relation。

尤其 C₃ 在一列支援重色時，單接點容量仍為一；沒有把 F={3} 無條件
搬到另一列。這個較寬的上界已足夠，不需單接點未用色守恆引理。
對三份候選 F_z′、F₀′、F₁′，在共同色框定義

\[
E_z=U\setminus F_z',\quad E_w=U\setminus(\{\beta_s\}\cup F_0'\cup F_1'),
\quad X=U\setminus\{\beta_i\},\quad Y=U\setminus\{\beta_j,\beta_k\}.
\]

|E_z|≥2、|E_w|≥1。由原 mixed K2 的精確關係，當 |Y|=2、Y⊂X 時
F_*=Y×(X∖Y)，否則 F_*=∅。原圖接受 β 恰在

\[
(E_z\times E_w)\setminus(\Delta\cup F_*)\ne\varnothing.
\tag{4}
\]

32 筆的 64 個 target 共 **128 組完整禁色候選**，(4) 全部非空；每個
target 還有一份對其所有候選通用的 (z,w,u,v) 局部見證。選定同一 (z,w)
後，各原 unary 再從自己的完整 relation 選全部接點避開 root 色的 tuple
及 coloring；三個不同原分量才能接合。u、v 始終共用一份 coloring，
直接著色核對包含原 chord zu、原 uv 及全部 root／boundary 邊。

例如第一筆 S_z=01、S₀=04、S₁=234、s=0、i=2、{j,k}=12，原 ID=62，
q 下禁色依次是 {0}、{2}、{3}。p₁ 下精確禁色是 {0}、{1}、{3}，
可用 (z,w)=(1,2)；p₂ 下前兩份禁 {0}、{2}，第三份上界是
∅／{1}／{2}，每種都可用 (z,w)=(1,3)。同一分量從未被拆成接點 marginals。

全部結果見 [必要支援與共同見證表](../artifacts/c5_adjacent_degree5_mixed_edge_shared_t1_singles/support_table.md)。
表另按禁色角色顯示 16 列；JSON 仍保留 C_w0／C_w1 的全部 32 筆，具名
交換是兩張原資料間的對應，不是合併。ρ(i)=3−i mod5、π=(0 1) 同時
搬運全部支援及色框，Tβ=π∘β∘ρ、Tq=q；64 個字面反射 target 亦逐份
檢查，不只比較正規化後的相等分割。兩個固定 targets 在全部 32 筆上
另有直接計算，沒有僅憑反射就把一列當成另一列。

## 5. 出口接合、證書與停止點

若本型 M 是 Σ(G₀)=Ω∖{p,q} 來源的一個 minimal q-core，刪邊繼承給
Σ(M)⊇Ω∖{p,q}。共同對齊 q 後，p 為 p₁ 或 p₂；本輪接受 p 且 M 仍拒絕
q，才推出 **Σ(M)=Ω∖{q}**。依既有刪邊序列接回
[條件式出口](c5_single_sided_exit.md) 第八類；不從兩列接受單獨推完整 Σ。
連同 t_w=2、(1) 及 t_w=1、(2)，共鄰端點型的 **t_w≥1 全部完成**。

[Checker](../scripts/c5_adjacent_degree5_mixed_edge_shared_t1_singles.py) 與
[JSON](../artifacts/c5_adjacent_degree5_mixed_edge_shared_t1_singles/observations.json)
保存原 ID／完整記錄／SHA256、全部幾何、具名 contact words、完整 q schemas、
三份 F 候選及局部見證。有限核對包括 160 次 q／target 公式與原四點直接
著色比對、64 次字面 target 反射、32 次具名分量交換及 3,072 次共同色框
見證。共享端點與有間隙幾何保留；spoke 落在單接點分量開弧內的負例
被排除。任意大小覆蓋由 §2–3 紙面論證承擔，並非有限圖枚舉。

```bash
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t1_singles.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t1_pair.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t2.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared.py --check
python3 scripts/c5_adjacent_degree5_singleton_long_arc.py --check
python3 scripts/c5_adjacent_degree5_shared_singleton.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證與未重跑範圍見 [本輪紀錄](history/2026-09-29-adjacent-mixed-edge-shared-t1-singles.md)。
停止點為 t_w=1、(1,1) 指定雙列分離；下一窄入口是 t_w=0、(2,1) 的
54 筆，須保留 C_z 二接點、w 的另一二接點與單接點、原 diamond 外側
次序及完整關係。t_w=0、(1,1,1) 的 108 筆及一般雙 root／degree≥6
核心仍保留。沒有獨立第二審稿者；未新增 Lean theorem，`lake build`
不形式化上述拓撲／外部定理，也不證必要表的 disk 可實現性。
