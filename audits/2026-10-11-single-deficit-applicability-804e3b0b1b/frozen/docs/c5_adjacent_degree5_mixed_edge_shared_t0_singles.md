---
docgraph:
  id: c5.adjacent-degree5-mixed-edge-shared-t0-singles
  family:
    - c5
    - c5.degree5
  derives_from:
    - c5.adjacent-degree5-mixed-edge-shared
  requires:
    - c5.adjacent-degree5-mixed-edge-shared-t0-pair-single
    - c5.adjacent-degree5-mixed-edge-shared-t1-singles
  related:
    - c5.single-sided-exit
---
# 共鄰端點 mixed K2：t_w=0、(1,1,1) 的六跨度來源排除

後續（2026-09-29）：[同端點 K2](c5_adjacent_degree5_mixed_edge_same_endpoint.md)
已重推 P*ᶻ=P*ʷ={u} 的完整關係／逐邊 minimality，並以原路徑 K5、
跨度及原 v-star 將整型來源排除；不需 T4、0 target 查詢。下文保留
本輪原 108 筆及當時停止點，現行優先序見 [HANDOFF](HANDOFF.md)。

2026-09-29，接手 main@c178cf1 及前兩輪尚未提交的完整成果。
**本型的 disk minimal q-core 不存在。** 原 108 筆正常形全部需要至少
六條框邊的跨度，與 C5 周長五矛盾。不需 T4，不限制原 unary 分量大小，
也不需 target 拒絕假設或新增 pair K5 排除。

這完成 root incidences 恰為 **zu、zv、wu** 的共鄰端點接線：其餘四型
已證指定雙列，本型作來源排除；[出口第八類](c5_single_sided_exit.md)
遂可移除 w-spoke／unary 分拆限制。這不是所有 mixed K2 接線的分類。
證據為任意大小紙面論證、外部 degree-list 定理與 Python 有限控制；
未新增 Lean theorem，一般單側／共同出口及 K∞=K≤5 仍未證。

## 1. 同一來源與原 108 筆完整正常形

G 有限簡單，B=(b0,…,b4) 為 induced disk 外框，有效內部 H 非空連通。
固定 q=01012、U={0,1,2,3}；G 拒絕 q，刪任一非框邊後接受 q。
相鄰 z、w 完整 degree=5，其餘內點完整 degree=4。H−{z,w} 的唯一
mixed 原分量恰為 uv，root incidences 恰為 zu、zv、wu。
w 無 boundary spoke，其 unary 接點分拆為 (1,1,1)。

[共鄰端點化約](c5_adjacent_degree5_mixed_edge_shared.md) 給 z 亦無 spoke，
且有唯一二接點原分量 C_z，具名接點 (x₀,x₁)。w 的三份**不同原分量**
C_w0、C_w1、C_w2 具名接點為 y₀、y₁、y₂。另有
N_B(u)={b_i}、N_B(v)={b_j,b_k}，j≠k。全部原接點、實際附件、bridges、
框點身份與共同色框保留；尤其沒有合併三份單接點分量。

存在 {h,e,d}={0,1,2}，使

\[
q_i=h,\qquad \{q_j,q_k\}=\{h,e\},\qquad
F_z(q)\in\{\{h\},\{h,d\},\{h,3\}\},\qquad
(a_0,a_1,a_2)\in\operatorname{Perm}(h,d,3),\quad F_{w\ell}(q)=\{a_\ell\}.
\tag{1}
\]

F 是原完整 ordered relation 中全部 tuple 色集的交集；三份 w 關係
各恰為 {(a_ℓ)}。z 禁兩色時保留兩個 tuple 次序，禁一色時保留原
95 個完整必要 schemas。未投影成接點 marginals。
共有 6×3×6=108 筆。checker 重建 (1)，逐一綁定原 ID、完整原記錄、
全部 schemas 及相應局部 K2 支援 IDs。它們尚未獨立選支援拼成來源。

原 shared JSON SHA256 保持
`6b9b689c1f45b22feb182958c953b18989fe47655f69d5d2a17d8ed509555532`；
原 306／288 筆與 9,312 份 schemas 不改寫。

## 2. 四份 unary 的實際支援下界

對任一 unary C，唯一相鄰 root 為 r=z 或 w。忽略 r 色時原接點有
slack，故完整 relation 非空。若 a∈F_C(q)，固定 r=a 後的 lists
M_a 是不可著色的 degree assignment。[Dvořák Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
給 tightness 與 Gallai 結構；本輪重讀原文第 5–6 頁。

沿用 [無 spoke 局部引理](c5_adjacent_degree5_mixed_edge_shared_t0_pair_single.md#2-無-root-spoke-時的局部支援與-diamond-外側)：
每點完整 degree=4，外鄰只在 B∪{r}，原路徑 r–u–b_i 避開 C。
因此原 K4 block 的四個互不相交外向分枝可接到連通外部 hub
B∪{r,u}，給 K5 minor。故 C 是 K4-free Gallai tree。這裡只套用
已局部化的 degree-4 分量引理，未假設全圖僅一個 degree-5。

令 S_C=N_B(C)。**每份 q(S_C) 至少含兩色。** 空支援的全色對稱
不容許 0<|F_C|≤2。若只見色 a，固定 a 的色穩定子迫使 F_C={a}。
固定 r=a 後所有外鄰都用 a；tightness 使每點最多一個外鄰，故
deg_C≥3。但 K4-free Gallai tree 的葉塊私有點內度≤2，矛盾；整個
C 為 singleton 時內度零同樣矛盾。四份 S_C 因此都非空且至少兩點。

由 (1) 恰有一份原 C_wℓ 禁色為 {3}，記其角色為 C₃，保持原 ℓ 身份。
若 q(S_C₃) 漏掉 h∈{0,1,2}，交換 h 與 3 就固定所有實際 boundary
色，卻把原完整 singleton relation {(3)} 變成 {(h)}，矛盾。因此

\[
q(S_{C_3})=\{0,1,2\},\qquad |S_{C_3}|\ge3.
\tag{2}
\]

這是同一原分量的完整關係不變性，不依賴跨列任選新禁色。新跨度
排除不需 pair K5，但上述局部 K4-free／平面性仍是支援下界的前提。

## 3. 原 diamond 外側的六個具名單位

保留原 D={zw,wu,uv,vz,zu}。u、v 經原附件到 B，z 經 C_z 到 B，
w 經任一 C_wℓ 到 B，路徑內部避開 D。因此四點都在 D 面向 B 的
face boundary 上；唯一包含四點的面界為 Q_D=z–w–u–v–z，chord zu
位於內侧。四份 unary 各連通且碰 B，必在 Q_D 外側。

沿 Q_D 閉內部的細正則鄰域，外側為 annulus。z 只有 C_z 的兩條
外側 contacts，保留 (zx₀,zx₁) 的兩個方向。w 的三條外側 contacts
分屬三份不同原分量，各一條，所以保留全部六種次序。u 與 v 的原
boundary incidences 各作一個星狀單位，與四份 unary 共六個單位：

\[
C_z,\quad \operatorname{perm}(C_{w0},C_{w1},C_{w2}),\quad u,\quad v
\tag{3}
\]

或整體反向。同一框點的小鄰域內可分開不同附件，仍是原框點與同一色。
沿用 [原 diamond 同序論證](c5_adjacent_degree5_mixed_edge_shared_t0_pair_single.md#3-二接點區塊與-actual-supports-的完整環序)：
單位內連接兩外端的 crosscut 所切下、不含內圓周的一側，不能含
另一單位的外端，因後者還須連回內圓周。因此各 actual supports
可同序提升為 T_A⊂Z，滿足

\[
\max T_{O_j}\le\min T_{O_{j+1}},\quad
\max T_{O_5}\le\min T_{O_0}+5,\quad T_A\bmod5=S_A.
\tag{4}
\]

支援可有間隙，未填成整弧；不同單位可共享端點，不能重用開框邊。
每個正跨度單位不能繞滿一圈，因其餘仍有正跨度單位。故同一框點
不會為了減少跨度而任意重複取 lift。

## 4. 六跨度矛盾與有限證書

令 ℓ_A=max T_A−min T_A。四份 unary 至少兩點，ℓ_C≥1；由 (2)，
ℓ_C₃≥2。u 恰一個附件，ℓ_u=0；v 恰兩個不同附件，ℓ_v≥1。因此

\[
\boxed{6=1+(1+1+2)+0+1
\ \le\ \ell_{C_z}+\ell_{C_{w0}}+\ell_{C_{w1}}+\ell_{C_{w2}}+\ell_u+\ell_v
\ \le\ 5.}
\tag{5}
\]

矛盾。此論證不限制 unary 的橋長、block 數或分叉，直接排除全部
108 筆對應的任意大小 disk 來源。無需用 p₁／p₂ 接受來掩蓋來源排除。

[Checker](../scripts/c5_adjacent_degree5_mixed_edge_shared_t0_singles.py)、
[JSON](../artifacts/c5_adjacent_degree5_mixed_edge_shared_t0_singles/observations.json)
及 [逐筆排除表](../artifacts/c5_adjacent_degree5_mixed_edge_shared_t0_singles/exclusion_table.md)
另作以下有限控制：

- 十種非空容量≤2 禁色集合的 actual-support 穩定子域；只有 {3} 的
  最小跨度為二，其餘為一。這不替代 §2 的局部支援證明。
- 先只要求四 unary 與 v 各至少兩點：ordered lifts 與獨立 cyclic
  hull-edge masks 均得 **60 份**具名同序幾何／placements。後者先得
  120 份五正跨度單位的無次序 packing，再讀取原 diamond 次序。
  每份保留兩個 z contact words、三份 w 原身份、u／v 附件及共享端點。
- 60 份幾何的五個正跨度均為一。108×60=**6,480 次**逐來源接合，
  每次都保存 C₃ 漏掉的 q 色、固定其支援卻改變完整 {(3)} 的置換，
  以及 mixed 支援相容性、整份 z schema 穩定子 IDs。全部來源纖維為空。
- 保存 108 個來源反射、60 個幾何反射、108×6=648 個具名 w 分量
  排列對照，以及 108×24=2,592 次共同色框 q 接合核對。
  共享端點的周長五幾何為正控制，交錯支援為負控制；幾何域本身非空。

**必要支援保留零筆，target 查詢數為零。** 這是來源排除，不報成
216 個接受查詢，也不聲稱必要幾何可實現為 degree/list disk 圖。

## 5. 出口接合、重播與停止點

原化約已排除 w 側 (3)，留下五種正常形；前三種 t_w≥1 與
[t_w=0、(2,1)](c5_adjacent_degree5_mixed_edge_shared_t0_pair_single.md)
接受指定雙列，本型不存在。因此出口第八類只須保留 incidences
zu、zv、wu，不再限制 w-spoke 或 unary 分拆。
對來源 Σ(G₀)=Ω∖{p,q} 的 minimal q-core，仍先用上述來源排除／雙列
結果接受 p，再以刪邊繼承得到 Σ(M)=Ω∖{q}；完整 Σ 不是由有限表單獨推出。

```bash
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t0_singles.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t0_pair_single.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t1_singles.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t1_pair.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t2.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared.py --check
python3 scripts/c5_adjacent_degree5_singleton_long_arc.py --check
python3 scripts/c5_adjacent_degree5_shared_singleton.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_single_spoke_two_two_minor.py --check
python3 scripts/c5_single_spoke_two_two_external.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證見 [本輪紀錄](history/2026-09-29-adjacent-mixed-edge-shared-t0-singles.md)。
停止於本型來源排除及原共鄰端點接線完成。下一窄入口改取唯一 mixed
K2 的 **P*ᶻ=P*ʷ={u}**，即兩 root 都只接 u、v 有三個 boundary 附件：
先重推同一 u／v 的完整 tuples 與逐邊 minimality，不能搬用本型的
兩格禁對或 diamond 次序。其他 K2 接線、無 mixed、較大／多 mixed、
非相鄰雙 root 與 degree≥6 保留。沒有獨立第二審稿者；`lake build`
不形式化本輪 Jordan／Gallai 證明。
