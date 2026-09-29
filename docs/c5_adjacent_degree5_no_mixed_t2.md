---
docgraph:
  id: c5.adjacent-degree5-no-mixed-t2
  family:
    - c5
    - c5.degree5
  derives_from:
    - c5.adjacent-degree5-no-mixed
  requires:
    - c5.no-spoke-supports
    - c5.adjacent-degree5-singleton-long-arc
    - c5.adjacent-degree5-mixed-edge-shared
---
# 無 mixed、兩側 t=2,(2)：原 zw 鄰域的實際支援與環序

後續（2026-09-29）：[原 bridge 與固定框弧](c5_adjacent_degree5_no_mixed_t2_bridge.md)
已證 record 4／p₁、新增 68 個延拓；[原雙端點](c5_adjacent_degree5_no_mixed_t2_endpoints.md)
再證 record 5／p₂、新增 60 個延拓；[整條原路徑 palettes](c5_adjacent_degree5_no_mixed_t2_path_palettes.md)
再關閉最後 4 項。原 322 份全保留、0 筆來源排除，全部雙列皆證，
644／644 個 target 已證、0 個未決，接入出口第九類；原表保持不變。
以下數字與 record 4 停止點保留原輪語境，現況見後續報告與 HANDOFF。

2026-09-29。接續 [無 mixed 必要化約](c5_adjacent_degree5_no_mixed.md)，
完成交接指定的 **88 份原資料之 actual-support／rotation 必要覆蓋**。
兩套獨立幾何算法同得 2,550 份支援及 2,560 個 placements；與原資料
接合後，42 份有相容支援，產生 **322 份必要資料**，其餘 46 份纖維為空。
原 118／3,548 表及其 88 份子表未改寫。

進一步使用完整禁色集合的跨列搬運，上界已證 **512／644 個 target
查詢接受**，其中 206 份兩列皆證；另有 **132 個查詢未決**。
不需 T4。本型尚未整體接回出口，未證必要資料的 disk 實現。
證據為任意大小紙面化約、外部 degree-list 定理及 Python 有限控制；
未新增 Lean theorem。研究優先序只見 [HANDOFF](HANDOFF.md)。

## 1. 同一來源與原 88 份資料

G 有限簡單，B=(b0,…,b4) 是 induced disk 外框，有效內部 H 非空連通。
固定 U={0,1,2,3}、q=01012；G 拒絕 q，刪任一非框邊後接受 q。
有序相鄰 roots z、w 完整 degree=5，其餘內點完整 degree=4。
H−{z,w} 沒有 mixed 分量；兩側各有兩條原 spokes 及唯一二接點
原 unary C_z、C_w。保留原 zw、全部原附件、bridges、旁支與兩個
具名接點 (Cz_0,Cz_1)、(Cw_0,Cw_1)。

root 的原 boundary 鄰點記為 B_r={s_r0,s_r1}，s_r0<s_r1；
原 spoke r–b_srk 命名為 rk。actual support
S_r={i:N(b_i)∩C_r≠∅} 是全部實際附件，不能以可用支援超集替代。
令 T_r(β) 為同一 C_r 的完整有序接點關係，F_r(β) 為全部 tuples
色集的交集。前報告給

\[
q_{s_{r0}}\ne q_{s_{r1}},\qquad
F_r(q)=\{h_r\}=U\setminus(q(B_r)\cup\{c\}),\qquad
E_z(q)=E_w(q)=\{c\}. \tag{1}
\]

兩側用同一 c 及同一字面色框。所有滿足 (1) 的有序 B_z、B_w、c
獨立重建恰有 88 份，與原 JSON 的 `two_spoke_frontier` 一對一核對。
新證書保留 frontier ID、原 side IDs、兩份完整原 side 記錄及原檔 SHA256；
沒有重編原 149 份側資料或修改原正常形。

## 2. 每份 unary 的局部支援與完整 schemas

對 C_r，另一 root 不在分量內也不鄰接它；忽略 r 色時，接點有 slack，
故 T_r(β) 非空，任意列均有 |F_r(β)|≤2。固定 h_r∈F_r(q)，
不可著色 degree lists 處處 tight，且 C_r 為 Gallai tree。
這沿用外部 [Dvořák Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，
本輪核對原文第 5–6 頁；定理並非本專案的 Python 或 Lean 證明。

C_r 的 K4 block 已由前報告的外部 hub 排除。此型外部路徑可直接
取原 r–s–b_j，j∈B_s，內部避開 C_r；保留 zw，不把另一側收縮入 C_r。
因此 C_r 的 blocks 只可能為 bridges／odd cycles。

**|q(S_r)|≥2。** 空支援的全色對稱不能保持 singleton F；若只見一色 a，
固定 a 的穩定子迫使 h_r=a。固定 r=a 後，所有外鄰只用 a；tightness
迫使每點最多一個外鄰，由完整 degree=4 得 deg_C≥3，與 K4-free
Gallai tree 的 leaf-block 非 cut 點內度≤2 矛盾。singleton C 亦不可能。
特別地 |S_r|≥2；若 h_r=3，固定 q(S_r) 的穩定子又迫使 S_r 見滿
{0,1,2}。這是 [局部支援引理](c5_adjacent_degree5_singleton_long_arc.md#2-原三角形外側給固定長弧次序)
在原 zw 外部路徑下的搬運，沒有假定整個 H 的最高 degree 為四。

刪除一條 r-contact 後，degree-4 區域解除。固定 r=h_r，該被刪接點
必取 h_r，另一接點不取 h_r，否則仍無法延拓。因此真實 T_r(q) 必在
既有 **95 份 singleton-ban 完整 binary schemas** 中。checker 另從
全部 65,535 個非空 binary relations 獨立核對四個 h 的 95 份 schemas，
保留對角 tuples；再用 actual S_r 的逐色穩定子篩選整份關係。
322 份資料的每側均留下 17 或 95 份相容 schemas，沒有空 schema 纖維。
這只是必要完整關係覆蓋，不是任一 schema 的來源實現。

## 3. 原 zw 的細鄰域與六個具名單位

在原 disk 中取原 edge zw 及兩端的細閉正則鄰域 N。N 是 disk，
其外側至 B 是 annulus；這只是讀取原嵌入，沒有刪 zw、合併兩 root
或替換染色來源。沿 ∂N，z 的四條其餘 incidences 成一段，w 的亦然。

同一 C_r 的兩個 contacts 在 root 的此線性段中相鄰。否則 C_r 中
連接兩 contacts 的簡單路徑，加兩條原 r-contact 邊成內部 Jordan 曲線；
其不含 B 一側不能放任何另一 incidence：spoke 直接到 B，zw 經另
一 root 的原 spoke 也到 B，均會被曲線擋住。因此可將二 contacts
**僅在次序記號中**寫成一單位 C_r，其內部兩個具名次序仍分別保留。

六個單位的 cyclic word 必為

\[
\operatorname{perm}(C_z,z0,z1)\,
\operatorname{perm}(C_w,w0,w1). \tag{2}
\]

兩側各自連續，不允許在全局任意交錯六個單位；反向亦已包含。
每份 C 加截短 contacts 及全部 boundary 附件，是連接 annulus 兩邊界
的連通集合；spoke 是單條連接弧。不同單位只可能在 B 共端點。
在框點的小鄰域分開入射邊端、仍保留同一框點身份與顏色。

沿用 [annulus crosscut 論證](c5_no_spoke_supports.md#2-每份支援至少兩點且有環狀區塊次序)：
同一 C 連接兩外端的 crosscut，其不含 ∂N 一側不能有另一單位的外端，
否則後者不能接回 ∂N。外端因此也按 (2) 成同序區塊。此論證使用全部
實際連通分量，容許任意大小、旁支與 bridge 長度。

以 C_z 第一外端起讀，把六份支援提升為整數集 T_A，存在 a∈{0,…,4}：

\[
\min T_{C_z}=a,\qquad
\max T_{O_j}\le\min T_{O_{j+1}},\qquad
\max T_{O_5}\le a+5,\qquad T_A\bmod5=S_A. \tag{3}
\]

spoke 的支援恰是具名 singleton；C_z、C_w 各跨度至少一。每份 C
跨度<5，因另一份 C 也需正跨度，故同一框點在同一份支援不會首尾
重複提升。不同單位仍可共享端點，支援內可有間隙，沒有擅取最短 hull。

## 4. 有限必要覆蓋與原資料纖維

第一算法直接按 (2) 遞增生成 (3)。第二算法獨立枚舉整個單側
S_r∪B_r 的 cyclic hull，要求兩條 spoke 不在 C_r hull 的開弧內，
再要求 z、w **整側 hull** 的框邊 masks 不交。單側共有 370 份 hull
資料，兩算法支援集合恰同為 **2,550**。這裡 mask 只檢查具名框弧，
並非把原 C 壓成可安全替換的 state。

全部幾何有 2,560 個 placements；每個保存 lifts、六單位次序及兩側
具名 degree-5 rotation 的四種 contact 方向，共核對 **10,240** 份。
相同次序以 `rotation_template_id` 引用完整模板，原 zw 始終是每個
root rotation 的第一個具名 incidence。不同 placements 不因支援相同而丟棄。

接合原 88 份及 §2 的支援／完整 schema 條件後：

| 層 | 數量與意義 |
| --- | --- |
| 原 frontier | 88 份具名同色資料，原表不改寫 |
| 有相容支援的原資料 | 42 份；另 46 份無 disk 必要支援 |
| 新必要支援 | 322 份，每份恰一 placement，保留四個接點方向 |
| 共用 residual 色 c | c=3 有 310 份；c=0、c=1 各 6 份；c=2 無相容支援 |
| q 的整份 schema | 每側 17 或 95 份，全部原 tuples 與相容 IDs 另存 |

數量指必要資料，**不是來源圖數、實現數或完整 Σ 數**。尚未用原圖
minor 或 T4 刪除這 322 份中的任何一份，支援本身不保證實現。
原 root 交換的 322 次核對與共同反射 ρ(i)=3−i、π=(0 1) 亦保留，
spoke 名稱隨具名 boundary index 重排，兩側不得獨立換色。

## 5. 同圖 target 搬運與精確停止點

在原 C_r 及 actual S_r 上，若 σq|S_r=β|S_r，整份 coloring 經 σ
搬運，故 T_r(β)=σT_r(q)、F_r(β)=σ{h_r}。這是局部原關係的精確
等式；兩側搬運後仍用同一字面 β 色框接合。若沒有相容 σ，僅取容量≤2
且受 β(S_r) 的逐色穩定子保持的全部 F 候選，包括空集。

每組候選在同一有序 root 色對下計算

\[
E_r(\beta)=U\setminus(\beta(B_r)\cup F_r(\beta)),\qquad
Z_G(\beta)=(E_z\times E_w)\setminus\Delta. \tag{4}
\]

只有所有候選皆有非對角色對才標 A；固定此色對後，各原 C 從完整
relation 選一份避開 root 色的 tuple 及 coloring。沒有乘端點 marginals，
沒有聲稱未知列可在同一來源獨立實現每組候選。

322 份×p₁=01021、p₂=01212，共 644 個查詢、2,892 組完整禁色候選，
每組公式均與保留 zw 及四條原 spokes 的直接 root-pair 枚舉一致：

| p₁／p₂ | 必要資料數 |
| --- | ---: |
| A／A | 206 |
| A／? | 50 |
| ?／A | 50 |
| ?／? | 16 |

因此已證 512 個單列接受，剩 132 個單列未決。另有 644 次字面反射
target 核對；沒有把反射後正規化的相等分割當成同一列。
本結果未完成此型的全表分離，也未新增整型出口類別。

**第一個未決是新 record 4／p₁**，原 frontier ID=31、原 sides=(137,147)：

\[
B_z=04,\quad S_z=01,\quad F_z(q)=\{1\};\qquad
B_w=34,\quad S_w=123,\quad F_w(q)=\{0\},\quad c=3.
\]

p₁ 下 F_z={1}，E_z={2,3}；C_w 支援從 q 的 101 變成 102，
不能全分量換色搬運。唯一失敗候選是 **F_w(p₁)={0,3}**，使
E_w=∅。p₂ 則精確搬運得 F_w={2}、E_w={0,3}，取 (z,w)=(3,0)。
下一步可針對同一 C_w 的 p₁ 雙禁色 residual，保留原 wb3、wb4、zw、
C_z 及實際支援，檢查既有原 bridge／固定框弧 minor 能否排除此候選。
這是未決上界見證，**不是實際不可延拓圖**；不能先刪除 F={0,3}。

其餘分拆、較大／多 mixed、一般單側／共同出口及 K∞=K≤5 仍未證。
必要表的 disk 實現、完整 Σ 與新拓撲的 Lean 形式化均保留。

## 6. 證書與重播

[Checker](../scripts/c5_adjacent_degree5_no_mixed_t2.py)、
[JSON](../artifacts/c5_adjacent_degree5_no_mixed_t2/observations.json)、
[322 份支援及 88 份纖維表](../artifacts/c5_adjacent_degree5_no_mixed_t2/support_table.md)
保存來源 SHA／ID、全部幾何、lifts、root rotations、完整 q schemas、
逐候選 root-pair 見證與 132 個未決項。負控制包括兩側分組交錯、
錯誤 marginal 乘積，以及 record 4 的空 residual。

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_t2.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared.py --check
python3 scripts/c5_adjacent_degree5_singleton_long_arc.py --check
python3 scripts/c5_no_spoke_supports.py --check
python3 scripts/c5_no_spoke_exterior.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證與省略範圍見 [當輪紀錄](history/2026-09-29-adjacent-no-mixed-t2.md)。
`lake build` 只檢查既有 Lean 專案，未形式化本輪紙面環序或跨列覆蓋。
