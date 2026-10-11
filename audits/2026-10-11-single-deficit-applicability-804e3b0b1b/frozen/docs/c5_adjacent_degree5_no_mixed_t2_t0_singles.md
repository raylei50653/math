---
docgraph:
  id: c5.adjacent-degree5-no-mixed-t2-t0-singles
  family:
    - c5
    - c5.degree5
  derives_from:
    - c5.adjacent-degree5-no-mixed
    - c5.root-degree-excess
  requires:
    - c5.adjacent-degree5-no-mixed-t2
    - c5.no-spoke-exterior
    - c5.no-spoke-supports
    - c5.adjacent-degree5-singleton-long-arc
  related:
    - c5.single-sided-exit
---
# 無 mixed：t_z=2,(2)，t_w=0,(2,1,1) 的四分量支援與雙列分離

後續（2026-09-29）：[t_w=0,(2,2) 缺額型](c5_adjacent_degree5_no_mixed_t2_t0_pairs.md)
已完成本文下一入口：96 份接成 364 份支援，來源 K5 排除 340，保留 24 份
48 查詢全證。不需 T4；本文及原 JSON 的 next_frontier 保留當輪語境。

2026-09-29，基準 `f29b899`，承接現有未提交的 t_z=2、t_w=1 成果。
完成 [前輪交接](c5_adjacent_degree5_no_mixed_t2_t1_endpoints.md#4-完整套表與出口)
指定的 **96 份有序資料**。兩個獨立幾何算法同得 **480 份支援／placements**；
接合後 36 份原資料有支援、60 份纖維為空，形成 **120 份必要支援**。
全部 **240／240 個指定雙列查詢接受**：216 個由完整關係搬運，
24 個由搬運及容量上界；沒有未決查詢或對這 120 份的新來源排除。

本型及整圖 root 交換型已接回 [單側出口第九類](c5_single_sided_exit.md#1-定義與定理)。
不需 T4、不需新增 target K5／first-bridge 排除。四個原分量、六接點、
z 的兩條原 spokes、zw、全部實際附件及共同色框均保留。
任意大小覆蓋是紙面論證，依賴外部 degree-list 定理；Python 重播有限證書。
必要支援不是 disk 實現，未新增 Lean theorem；一般出口與主命題仍未證。
優先序只見 [HANDOFF](HANDOFF.md)。

## 1. 同一來源與原 96 份有序資料

M 有限簡單，B=(b0,…,b4) 為 induced C5 disk 外框，H=M−B 非空連通。
固定 U={0,1,2,3}、q=01012；M 拒絕 q，刪任一非框邊後接受 q。
z、w 是原相鄰 roots，完整 degree=5，其餘內點完整 degree=4。
H−{z,w} 沒有 mixed 分量。z 有兩條原 spokes，唯一二接點原分量 C_z；
w 沒有 spoke，有二接點 C_w 及兩個不同的單接點原分量 D_w、E_w。
具名接點為 (Cz_0,Cz_1)、(Cw_0,Cw_1)、Dw_0、Ew_0。
「單接點」只指與 root 的接點數，不能把分量換成一個點或一條 spoke。

記 root 可用色為 A_r，接合後 residual 為 E_r；分量 E_w 與 root residual
E_w(β) 由有無列參數區分。每份原分量 C 的完整有序關係記 T_C(β)，
禁色 F_C(β)=⋂_{t∈T_C(β)}set(t)。[No-mixed 化約](c5_adjacent_degree5_no_mixed.md)
給出

\[
E_z(q)=E_w(q)=\{c\},\quad |q(B_z)|=2,\quad
F_{C_z}(q)=U\setminus(q(B_z)\cup\{c\}),\quad
(F_{C_w},F_{D_w},F_{E_w})(q)=(\{a\},\{b\},\{e\}),
\quad \{a,b,e\}=U\setminus\{c\}. \tag{1}
\]

固定分量次序，a、b、e 兩兩不同。從原 3,548 份 `retained` joins 讀出
96 份，另直接枚舉 B_z、c 及 (a,b,e) 的排列重建完全相同的集合。
證書綁定原檔 SHA256、原 retained-join ID、side IDs、完整 sides，並逐筆
核對前輪 JSON 的 `next_frontier`；原資料保持不變。
首項仍為 retained-join ID=3048、sides=(133,64)、B_z=01、F_Cz={2}、
(F_Cw,F_Dw,F_Ew)=({0},{1},{2})、c=3；此項的支援纖維為空。

[Root 預算](c5_root_degree_excess.md) 在兩側皆為 (D,O,κ)=(1,0,0)，
分量缺額分別是 z:(1)、w:(1,0,0)。w 的兩個飽和單接點仍各有自己的
完整關係和實際支援；source 預算不限制 target 的 C_z 禁色仍是 singleton。

## 2. 無 w-spoke 時的實際外部路徑

忽略本側 root 色時，C 的 boundary lists 是 degree lists，接點有 slack，
故每列 T_C 非空，|F_C(β)|≤k_C。固定 d∈F_C(q) 後，拒絕 degree lists
處處 tight，C 是 Gallai tree。沿用外部
[Dvořák 講義 Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
（本輪核對第 5–6 頁）；這不是 Python 或 Lean 證明。

**先證每個 C 實際碰 B。** 若支援空，整份 T_C(q) 在 S₄ 全色置換下
不變，singleton F_C(q) 卻不可能在 S₄ 下不變，矛盾。於是每份 C 都有
原 contact—分量內簡單路徑—boundary 附件，不能把這條路徑當成新 spoke。

對 C_w、D_w、E_w，避開指定分量的外部路徑可取 w–z–b_i，i∈B_z。
對 C_z，取原 z–w 邊，接 w–Dw_0、D_w 內簡單路徑及某個真實 D_w–b_j
附件。它避開 C_z，且內部不碰 B。連同 B，各提供本側 root 與 B 的
同一連通外部 hub。[No-spoke 外部連通引理](c5_no_spoke_exterior.md#3-以另一分量恢復-k4-的外部-hub)
因此逐份適用，排除各 C 的 K4 block；並未把 D_w 合併進 C_z。

**每份 |q(S_C)|≥2。** 若只見一色 d，固定 d 的色穩定子迫使 F_C(q)={d}。
令 root 取 d，所有外鄰同色；tightness 迫使每點至多一個外鄰，故
deg_C≥3。這與 K4-free Gallai tree 的 leaf block 私有點內度≤2 矛盾；
單頂點亦不可能。因此四個 actual supports 各至少兩點、正跨度。

C_z、C_w 各使用既有 95 份 singleton-ban 完整 binary schemas，保留
對角 tuples 及每一座標的 contact-edge release witness；checker 由全部
65,535 份非空 binary relations 獨立核對，再按 actual support 穩定子篩整份
關係。D_w、E_w 的完整 q 關係分別恰為 {(b)}、{(e)}，各自保存。
120 份中 C_z 有 96 份留下 17 schemas、24 份留下 95；C_w 全部留下 17。

## 3. 四個正跨度分量與六單位次序

取原 zw 的細閉正則鄰域 N，外側至 B 為 annulus。兩個 root 的其餘
incidences 各成一段。二接點分量的兩個 contacts 在線性 root 段內相鄰：
否則兩條 root 邊與原分量內簡單路徑所圍的 Jordan 曲線，會把某個其他
incidence 隔在不含 B 的一側；該 incidence 沿 spoke、另一原分量或 §2
的 zw 外部路徑可避開此曲線接到 B，矛盾。

所以必要 cyclic word 是

\[
\operatorname{perm}(C_z,z0,z1)\,
\operatorname{perm}(C_w,D_w,E_w), \tag{2}
\]

其中 z0、z1 按 boundary 索引排序，兩份二接點各保留兩個具名方向。
四原分量及兩 spokes 各連接 annulus 兩邊界，不同單位只在 B 共端點。
[同源 crosscut 論證](c5_no_spoke_supports.md#2-每份支援至少兩點且有環狀區塊次序)
使外端按同一 (2) 次序成區塊。切於 C_z 首個外端，存在整數 lifts：

\[
\min T_{C_z}=a,\quad \max T_{O_i}\le\min T_{O_{i+1}},\quad
\max T_{O_5}\le a+5,\quad T_A\bmod5=S_A. \tag{3}
\]

四份分量的跨度皆≥1，總和≤5；每份跨度≤2。Spokes 跨度零。
保留支援中的間隙及不同單位共享的框點，不補齊整弧，也不把兩個
單接點分量的跨度改成零。同一分量跨度<5，所以無需重複提升同一框點。

第一算法按 (2)–(3) 遞增生成；第二算法枚舉每側 actual-support hulls，
檢查同側各 hull 的內部互不交，再要求兩側整體框邊 masks 不交。
兩算法恰同得 **480 份**，每份只有一 placement。四跨度皆一的有 240 份；
指定其中一份跨度二、其餘一，各有 60 份，共另外 240 份。
36 個次序模板保存 4 種具名 contact directions，共核對 1,920 份 rotations。
接上 (1)、兩色支援與完整 schema 穩定子後得 120 份，共同 c 全為 3。
60 份原資料空纖維表示該參數型無相容 disk 必要支援；它們與 240 個
target 接受的計數單位不同。120 份支援全保留，未宣稱可實現。

## 4. 全部指定雙列與出口

若色置換 σ 在原 C 的**全部 actual support** 上滿足 σq=β，則整份
coloring 搬運給 T_C(β)=σT_C(q)、F_C(β)=σF_C(q)。接合仍使用同一
字面 β 及同一 root 色；沒有逐接點改色或獨立重命名共同色框。
不能搬運時，保留所有 |F|≤k_C 且受 β(S_C) 逐色穩定子保持的 F，
包括空集。這只是真實 F 的上界族，不聲稱各候選有共同來源。

每個完整候選 (F_Cz,F_Cw,F_Dw,F_Ew) 按原圖接合：

\[
E_z(\beta)=U\setminus(\beta(B_z)\cup F_{C_z}),\quad
E_w(\beta)=U\setminus(F_{C_w}\cup F_{D_w}\cup F_{E_w}),\quad
Z=(E_z\times E_w)\setminus\Delta. \tag{4}
\]

checker 逐組直接枚舉 U²，保留 zw、兩 spokes 及四份禁色，與 (4) 核對。
只有全部候選 Z 非空才記接受；真實候選遂有共同 root 色對，四個原
分量各從完整 T_C 選取避開其 root 色的 coloring，拼回同一來源。

| 查詢層 | 數量 |
| --- | ---: |
| 120 份 × p₁=01021、p₂=01212 | 240 |
| 四份完整關係皆可搬運 | 216 |
| C_z 用容量／穩定子上界，其餘精確 | 24 |
| 完整候選接合，全部 Z 非空 | 336 |
| 雙列皆證／未決／新支援來源排除 | 120／0／0 |

首份支援 record 0 的 sides=(137,64)，B_z=04，
(S_Cz,S_Cw,S_Dw,S_Ew)=(01,12,23,34)，q 禁色=(1,0,1,2)。
p₁ 可取 (z,w)=(2,3)，p₂ 可取 (3,0)，均由完整搬運。

24 個上界查詢只分兩種 C_z 情境，各 12 個：

| target | B_z | S_Cz | F_Cz(q) | F_Cz(target) 的全部上界候選 | 可選 z≠3 |
| --- | --- | --- | --- | --- | --- |
| p₁ | 14 | 014 | {0} | ∅、{0}、{1}、{0,1}、{2,3} | 前四項取 2，最後取 0 |
| p₂ | 24 | 234 | {1} | ∅、{1}、{2}、{1,2}、{0,3} | 前四項取 0，最後取 1 |

每項 w 側三份關係皆精確搬運，E_w(target) 都含 3，故可固定 w=3，
配上表的 z。上界的二色禁集沒有被省略；不需要 pair residual／bridge 引理。

所有資料另核對 240 次共同字面反射、完整 q schemas 的色置換、
120 次 D_w／E_w **整分量**交換，及 456 次 q／target root 色對的整圖
root 交換。後者一併交換四分量歸屬及全部 spokes，涵蓋反向有序型。

因此 §1 圖類任意大小來源皆接受 p₁、p₂。[出口定理](c5_single_sided_exit.md)
另有 Σ(G)=Ω\{p,q} 的來源前提；minimal q-core M 由刪邊繼承其餘八列，
本結果接受對齊後的 p，而 q 仍拒絕，才推出 Σ(M)=Ω\{q}。
第九類新增本型及 root 交換型，不能單由指定雙列接受推一般完整 Σ。

## 5. 證書、驗證與下一入口

[Checker](../scripts/c5_adjacent_degree5_no_mixed_t2_t0_singles.py)、
[JSON](../artifacts/c5_adjacent_degree5_no_mixed_t2_t0_singles/observations.json)、
[逐筆支援及原纖維表](../artifacts/c5_adjacent_degree5_no_mixed_t2_t0_singles/support_table.md)
保存原 96 份、source 預算、SHA／IDs、全部 lifts／rotations、完整 q schemas、
四分量 target 候選及原 root 色對見證。8 個負控制涵蓋 root 交錯、把
單接點當 spoke、合併 D_w／E_w、遺失 zw、以 marginals 替換 relation、
空／單色 source 支援、未見禁色及把 source 缺額當 target singleton 限制。

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t0_singles.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t1_endpoints.py --check
python3 scripts/c5_adjacent_degree5_singleton_long_arc.py --check
python3 scripts/c5_no_spoke_supports.py --check
python3 scripts/c5_no_spoke_exterior.py --check
python3 scripts/c5_root_degree_excess.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證與省略範圍見 [本輪紀錄](history/2026-09-29-adjacent-no-mixed-t2-t0-singles.md)。
新證書不提供來源圖實現；`lake build` 不形式化紙面環序或外部定理。

下一窄入口為 **t_z=2,(2)，t_w=0,(2,2)，D_w=1、O_w=0**。
只讀原 joins 得 96 份，兩個二接點分量的禁色大小 (1,2)／(2,1) 各 48；
首項 retained-join ID=3036、sides=(133,16)、B_z=01、F_Cz={2}、
w 禁色=({0},{1,2})、c=3。新 JSON 僅綁定原 IDs／SHA，未生成此型支援。
這裡 D_w、O_w 指 w 側預算；下一型有三原分量、六接點、兩 spokes，
須保留飽和二接點的完整關係。另 96 份 D_w=0、O_w=1 型，以及其他
no-mixed、較大／多 mixed、degree≥6、非樹／非相鄰 roots 均保留。
