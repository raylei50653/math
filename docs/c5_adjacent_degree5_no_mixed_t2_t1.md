---
docgraph:
  id: c5.adjacent-degree5-no-mixed-t2-t1
  family:
    - c5
    - c5.degree5
  derives_from:
    - c5.adjacent-degree5-no-mixed
    - c5.root-degree-excess
  requires:
    - c5.adjacent-degree5-no-mixed-t2
    - c5.adjacent-degree5-singleton-long-arc
  related:
    - c5.single-sided-exit
---
# 無 mixed：t_z=2,(2)，t_w=1,(2,1) 的預算、支援與拒絕原因

2026-09-29，基準 `30a2e59`。完成原 **136 份有序必要資料**的實際
支援／環序覆蓋，並依 [degree 超額預算](c5_root_degree_excess.md)
記錄 source 缺額與 target 拒絕原因。兩個獨立幾何算法同得 3,150 份
支援／placements，接合後產生 **560 份必要支援**：66 份原資料有支援，
70 份原資料的纖維為空。原 136 份及所有前序 artifacts 保留不變。

完整關係搬運及容量上界證 **1,002／1,120 個 target 接受**；
442 份支援兩列皆證，另外 118 份各剩一列。這 560 份支援資料沒有
另做來源排除，未完成整型分離或新增出口類別。70 份空纖維表示其
原參數型無相容 disk 支援；不能把它們與 target 接受數混算。

證據為任意大小紙面支援化約、沿用外部 degree-list 結構定理、Python
固定域證書。必要支援不是來源圖實現；未新增 Lean theorem，不需
來源接受其他八列或 T4。優先序只見 [HANDOFF](HANDOFF.md)。

## 1. 同一來源、五接點與 source 預算

M 有限簡單，B=(b0,…,b4) 是 induced C5 disk 外框，H=M−B 非空
連通。固定 U={0,1,2,3}、q=01012；M 拒絕 q，刪任一非框邊後接受。
原相鄰 roots z、w 完整 degree=5，其餘內點完整 degree=4，沒有
mixed 分量。z 的兩條原 spokes 為 z–b_i、z–b_j，i<j；唯一二接點
分量為 C_z，具名接點 (Cz_0,Cz_1)。w 的唯一原 spoke 為 w–b_k，
二接點原分量為 C_w，接點 (Cw_0,Cw_1)，另有單接點原分量 D_w，
接點 Dw_0。**單接點不表示 D_w 只有一個頂點，也不把它當成 spoke。**

保留原 zw、三條 spokes、三個原分量、全部 boundary 附件／bridges、
五接點身份、完整有序關係及共同色框。記 root boundary 鄰點為
B_z、B_w，三份原分量的 actual supports 為 S_z、S_w、S_D。
[原 no-mixed 化約](c5_adjacent_degree5_no_mixed.md) 給

\[
E_z(q)=E_w(q)=\{c\},\quad
F_z(q)=\{h\}=U\setminus(q(B_z)\cup\{c\}),\quad
F_w(q)=\{a\},\quad F_D(q)=\{b\},\quad
\{a,b\}=U\setminus(q(B_w)\cup\{c\}),\ a\ne b.
\tag{1}
\]

q 在 B_z 上異色。原 3,548 份 `retained` joins 中按上述分拆過濾得
136 份；另直接選 B_z、B_w、c，再排列 (a,b) 獨立重建完全相同的集合。
新 JSON 綁定原檔 SHA256、原 retained-join ID、原 side IDs 與完整
side 記錄。子表第 0 筆仍為 sides=(133,91)，其支援纖維為空。

Q=zw 是樹，兩側 (D,O,κ)=(1,0,0)。更細地，C_z 缺額 1，
C_w 缺額 1，D_w 缺額 0；F_w、F_D 不重疊。這是 source q 的
必要結構，**不能由飽和就刪除 D_w，或把同樣預算套到 p**。

## 2. 三份原分量的支援及完整 q schemas

對任一 C∈{C_z,C_w,D_w}，另一 root 不在 C 也不鄰接 C。
暫不固定本側 root 色時接點有 slack，完整 T_C(β) 非空，
任意列 |F_C(β)|≤k_C。固定 source 禁色 d∈F_C(q) 後，拒絕
degree lists 處處 tight，C 為 Gallai tree。這沿用
[前報告的外部定理及局部論證](c5_adjacent_degree5_no_mixed_t2.md#2-每份-unary-的局部支援與完整-schemas)。

每份 C 都有避開它的原 r–s–b_j 路徑：r 是本側 root，s 是另一
root，b_j 用另一側任一原 spoke。該路徑連同 B 是外部 hub，故
前報告的 K4 block 原圖 K5 論證仍成立。三份 C 都 K4-free；
即使 D_w 的接點數不同，完整 degree=4 及外部路徑前提完全相同。

每份 q(S_C) 至少兩色。空支援的全色對稱不能保留 singleton F；
只見一色 d 時，穩定子迫使 F={d}。令 root 也取 d，tightness
使每點至多一個外鄰，因而 deg_C≥3，與 K4-free Gallai tree 的
leaf block 私有點內度≤2 矛盾；單頂點情況亦不可能。因此每份
actual support 至少兩個框點、cyclic span 至少一。

C_z、C_w 各用既有 **95 份 singleton-ban 完整 binary schemas**。
固定 root=d 並刪某接點邊後，該接點必取 d、另一接點避開 d；
所以每個座標都有相應 release witness。checker 由全部 65,535 份
非空 binary relations 獨立核對這個 schema 表，再按 actual support
的 source 色穩定子篩選整份 relation，每份保留 17 或 95 個 schema IDs。
D_w 的完整 unary 關係恰為 {(b)}，不是以 pair residual 公式代替。

## 3. 原 zw 鄰域的六單位次序

取原 edge zw 的細閉正則鄰域 N，其外側至 B 為 annulus。
沿 ∂N，z、w 的其餘 incidences 各成一段。每份二接點 C 的兩個
contacts 在其 root 線性段中連續：若中間夾另一 incidence，C 中
連接兩接點的原簡單路徑加兩條 root 邊形成 Jordan 曲線。不含 B
的一側不能容納該 incidence，因它若是 spoke 直接到 B，若是
另一原分量則在避開 C 下連到 B；原 zw 亦經另一 root spoke 到 B。

因此六個具名單位的 cyclic word 恰有必要形式

\[
\operatorname{perm}(C_z,z0,z1)\,
\operatorname{perm}(C_w,D_w,w0),\tag{2}
\]

並保留 C_z、C_w 各兩種具名接點方向。每單位連接 annulus 的
兩邊界；不同分量／spokes 只可在 B 共端點。同源 crosscut 論證
使外 boundary 支援按同一 (2) 次序成區塊，不能互相穿插。
這裡重新使用三份原分量及三條 spokes 的實際接線，不把舊的
「兩份原分量＋四條 spokes」幾何表拿來替代。

從 C_z 的首個外端切開，支援各取整數提升 T_i，滿足

\[
\min T_{C_z}=a,\quad \max T_i\le\min T_{i+1},\quad
\max T_{\rm last}\le a+5,\quad T_i\bmod5=S_i.\tag{3}
\]

允許不同單位共用框點端點及支援內部有間隙，不填成整弧。
三份原分量各有正跨度，使任一份跨度嚴格小於五；故同一單位內
同一框點不必重複提升。Spokes 跨度零，z0、z1 以框點索引排序。

依 (2)–(3) 的遞增 lifts，及另一路徑「每側 actual-support hulls、
整側框邊 mask 互不交」兩算法均得 **3,150 份**支援及 placements。
每份保存兩個 root 的 degree-5 rotation、原 zw、三 spokes 與
五接點的四個方向模板。接入 (1)、source 支援色及完整 schema
穩定子後得 560 份。這是任意大小來源的必要覆蓋，不保證每份可實現。

## 4. 完整跨列搬運、精確接合及拒絕原因

對每個原 C，若存在全域色置換 π，於**所有 actual support 框點**
滿足 π(q_i)=β_i，則逐點改色得到 T_C(β)=πT_C(q)，因而
F_C(β)=πF_C(q)。所有這類 π 的 F 像必一致。
各原分量的改色只是導出同一字面 β 下的關係；接合時共用同一
root 色與 boundary 色，沒有獨立重命名它們。

若沒有這樣的 π，保留所有容量 |F|≤k_C 且在 β(S_C) 穩定子下
不變的 F 候選，包括空集。這是合法上界；不假設各候選或不同
分量的任意組合有共同來源。它完整包含真實 F，所以只有當
**所有**候選接合都成功，才記指定列延拓。

每次使用三份完整禁色候選 (F_z,F_w,F_D)，原圖的 root 關係是

\[
E_z=U\setminus(\beta(B_z)\cup F_z),\qquad
E_w=U\setminus(\beta(B_w)\cup F_w\cup F_D),\qquad
Z=(E_z\times E_w)\setminus\Delta.\tag{4}
\]

接合失敗恰為以下三個條件之一：E_z=∅、E_w=∅，或
E_z=E_w={d}。前兩條可同時成立，因此 JSON 用
`obstruction_reasons` 列表保存所有成立條件，不以先遇到者覆蓋。
本輪實際 146 組失敗候選沒有同時兩側空的情況。

| 計數單位／類型 | 數量 |
| --- | ---: |
| 必要支援 × 兩 target | 1,120 |
| 三份完整關係均可搬運而接受 | 724 |
| 搬運及容量上界合用而接受 | 278 |
| 未決 target 查詢 | 118 |
| 所有 target 候選接合 | 3,148 |
| 失敗候選：empty_z | 60 |
| 失敗候選：empty_w | 68 |
| 失敗候選：same_singleton | 18 |

118 是查詢數，146 是候選接合數；同一查詢可能有多個失敗候選。
閉合原因存於 `closure_reason`：`complete_relation_transport` 或
`transport_and_capacity_bound`，未決為 null。這輪未套用新 minor、
端點限制或證書交換，不能把這些機制記為已使用。

442 份支援為 A/A，59 份為 ?/A，59 份為 A/?。
每份的字面共同反射（含 root-spoke 排序及全部分量 F）均核對，
共 1,120 次；反向有序型由交換整個 z／w 角色與所有原分量覆蓋，
不是只交換端點 marginals。尚未建立整型出口或完整 Σ。

## 5. 首筆未決：record 14 的 p₁

下一窄入口固定為 **record 14／p₁=01021**，原子表 ID=42、
原 retained-join ID=3192、原 sides=(137,118)，c=3：

\[
B_z=04,\quad B_w=3,\quad
(S_z,S_w,S_D)=(01,123,34),\quad
(F_z,F_w,F_D)(q)=(\{1\},\{0\},\{2\}).
\]

p₂ 已由完整搬運接受。p₁ 下 F_z={1}、F_D={1} 均精確，
z 的 residual 是 {2,3}；w-spoke 的色為 2。唯一失敗候選因此是

\[
F_w(p_1)=\{0,3\},\qquad E_w(p_1)=\varnothing.\tag{5}
\]

跨列難點確實落在承擔 source 缺額的二接點 C_w。D_w 雖飽和且
這一列可搬運，仍保留其原支援 34、單接點、內部及附件路徑；
z–w、z 的 04 spokes 也都保留。下一步比較同一 C_w 在 q 的
singleton 禁色 {0} 與 p₁ 的雙禁色 {0,3}，檢查實際端點／bridge
支援及 source 拒絕證書重建，不能直接套入僅為兩側 t=2 證成的結論。
目前 (5) 是上界候選，不是已找到拒絕 p₁ 的 disk 來源。

## 6. 證書、重播與界線

[Checker](../scripts/c5_adjacent_degree5_no_mixed_t2_t1.py)、
[JSON](../artifacts/c5_adjacent_degree5_no_mixed_t2_t1/observations.json)、
[支援表](../artifacts/c5_adjacent_degree5_no_mixed_t2_t1/support_table.md)
保存全部原 136 份、source 預算、原 ID／SHA、3,150 份幾何、
所有具名 rotations、完整 q schemas、全部 3,148 組 target joins、
118 份未決查詢及每一筆反射。每次接合另直接枚舉 U² 檢查原 zw、
三條 spokes 與三份 F，交叉核對 (4) 及拒絕原因。

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t1.py --check
python3 scripts/c5_root_degree_excess.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證與省略項目見 [本輪紀錄](history/2026-09-29-root-degree-excess.md)。
`lake build` 不形式化新增的紙面預算、樹引理或 disk 支援覆蓋。
其餘 no-mixed 分拆，尤其 t=0,(2,2) 的 O=1 型，仍保留；
一般單側／共同出口及 K∞=K≤5 仍未證。
