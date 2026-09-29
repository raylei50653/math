---
docgraph:
  id: c5.adjacent-degree5-no-mixed-t2-t0-overlap
  family:
    - c5
    - c5.degree5
  derives_from:
    - c5.adjacent-degree5-no-mixed-t2-t0-pairs
    - c5.adjacent-degree5-no-mixed
  requires:
    - c5.single-spoke-two-two
    - c5.single-spoke-frame-arc
    - c5.adjacent-degree5-no-mixed-t2-t1-bridge
  related:
    - c5.exchange-geometry-scope
    - c5.single-sided-exit
---
# 無 mixed t_z=2、t_w=0,(2,2)：重疊型的雙飽和分量來源排除

2026-09-29，Git 基準 `c1be8fb`。**D_w=0、O_w=1 的 disk 來源全部排除。**
原 96 份有序資料重新接上 actual-support／rotation 必要覆蓋，得到 212 份
必要配置；每份至少一個原飽和分量給出 source K5，無保留配置、無 target 查詢。
188 份兩分量各自可排除，12 份只由 C_w 排除、12 份只由 D_w 排除。
每份成功的證據已可使用原 w–z–b_i 路徑，不需新增交換引理或 T4。

這完成[範圍表](c5_exchange_geometry_scope.md) 的 A–D 及 D–A：累計五種
root 交換型、936 份原有序接合；尚有十種／2,612 份所在子類開放。
所有含 t=2 側的 no-mixed 分拆均已涵蓋，[出口第九類](c5_single_sided_exit.md)
可移除另一 root 的分拆限制。一般機制完備性、一般／共同出口及 K∞=K≤5 仍未證。

證據分為任意大小紙面化約、外部 degree-list 定理與 Python 有限證書；
未新增 Lean theorem。必要支援和 minor skeletons 不宣稱實現任意 degree-list
來源，更不是 disk 反例。研究優先序只見 [HANDOFF](HANDOFF.md)。

## 1. 同一來源的兩個飽和分量

M 有限簡單，B=(b0,…,b4) 為 induced C5 disk 外框，H=M−B 非空連通。
M 是 edge-minimal q=01012 obstruction，minimality 不刪框邊。
相鄰 z、w 完整 degree=5，其餘內點完整 degree=4；H−{z,w} 無 mixed。
z 有兩條原 spokes 及二接點分量 C_z；w 無 spoke，有不同的二接點原分量
C_w、D_w。六接點、原 zw、實際附件與全部旁支始終保留。

U={0,1,2,3}。令 T_C(t) 為同一 C 的完整有序接點關係，
F_C(t)=⋂_{a∈T_C(t)}set(a)，則

\[
E_z(t)=U\setminus(t(B_z)\cup F_{C_z}(t)),\qquad
E_w(t)=U\setminus(F_{C_w}(t)\cup F_{D_w}(t)),\qquad
Z_M(t)=(E_z(t)\times E_w(t))\setminus\Delta.
\]

source minimality 給 E_z(q)=E_w(q)={c}，且 q 在 B_z 上單射。
本輪 (D_w,O_w,κ_w)=(0,1,0)，所以對互異的 h,a,b，

\[
F_{C_z}(q)=U\setminus(q(B_z)\cup\{c\}),\quad
F_{C_w}(q)=\{h,a\},\quad F_{D_w}(q)=\{h,b\},\quad
\{h,a,b\}=U\setminus\{c\}. \tag{1}
\]

按 B_z、c、(h,a,b) 直接重建恰有 96 份，逐項等於原 3,548 份 joins
中的本型 IDs；另與[缺額型證書](../artifacts/c5_adjacent_degree5_no_mixed_t2_t0_pairs/observations.json)
的 next_frontier 及 SHA256 相核。原入口 retained-join ID=3040、
sides=(133,30) 保留，並非重新編號後丟失原身份。

兩個飽和分量各有自己完整的交換 relation：
T_Cw(q)={(h,a),(a,h)}、T_Dw(q)={(h,b),(b,h)}。
它們不能合併，也不能以兩端 marginals 的乘積替代；後者會丟失兩個禁色。
C_z 仍保留所有適用的 singleton schemas 與每個 contact-edge release witness。
獨立遍歷全部 65,535 份非空 binary relations，重核 380 份 singleton、6 份
pair schemas，再逐份以 actual-support 的色穩定子檢查完整 tuple 集合。

## 2. 重建支援覆蓋，不沿用缺額型保留表

三分量的每份 F_C(q) 均非空真子集；若 C 不接 B，完整關係在 S₄ 下不變，
其 F 也須不變，矛盾。故每個 C 都有原 contact–C–B 路徑。
w 側分量有避開自身的原 w–z–b_i 路徑；C_z 則經 zw 及任一 w 側分量到 B。
[外部 hub 論證](c5_no_spoke_exterior.md) 因而對三分量各自給 K4-free。

固定 d∈F_C(q)，扣 root 色 d 後的 lists 大小逐點至少 deg_C。
拒絕迫使 lists tight，且 C 是 blockwise uniform Gallai tree，依據
[Dvořák 講義 Lemma 7、Theorem 10，第 5–6 頁](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)。
本輪重讀核對此外部定理；Python 與本專案 Lean 均不替代它。

pair F 不能只見一個 boundary 色，因固定該色的 S₃ 沒有不變二元子集。
singleton F 若只見一色，穩定子迫 F 為該色；扣同色 root 後 tightness 使
每點內度至少 3，違反 K4-free Gallai leaf block 的私有點內度至多 2。
因此三份 actual supports 各見至少兩色，跨度至少一。

原 zw 細閉鄰域外至 B 為 annulus，z／w 的其餘 incidences 各成一段。
同分量兩接點必相鄰，否則原 C 路徑與兩 contact 邊形成的 Jordan 曲線
把另一 incidence 隔在不含 B 的一側，違反它沿原 spoke／另一原分量到 B。
故五單位必要 word 仍為

\[
\operatorname{perm}(C_z,z0,z1)\,\operatorname{perm}(C_w,D_w). \tag{2}
\]

這裡只沿用[缺額型 §2](c5_adjacent_degree5_no_mixed_t2_t0_pairs.md#2-三分量五單位的任意大小支援覆蓋)
中與禁色大小無關的拓撲引理。各支援 lift 依 (2) 同序成塊，max≤下一 min，
可共用框點但不交錯；總跨度至多五。三分量各跨度至少一，故各至多三，
無需重複提升同一框點；actual supports 內的缺口仍保留。

本輪重新執行 lifts 算法與獨立的兩側 hull／框邊 mask 算法，兩者同得
910 份幾何。12 個模板各有八種具名接點方向，核對 7,280 次 rotations。
再接上本輪的 (1) 與完整 schema 穩定子，得到 **212 份**必要支援。
40 份原資料有支援，56 份纖維空；缺額型的 364 份表及 24 份保留表均未拿來替代。
共同 c=0、1、2、3 的支援數分別為 18、18、4、172，並未只留下未用色 3。

## 3. 每個原 pair 各自的固定框弧 K5

對 C=C_w 或 D_w，記 F_C(q)=K={r,s}。沿用
[雙禁色同圖奇數 bridge 路徑](c5_single_spoke_two_two.md#雙禁色的同圖奇數-bridge-路徑)：
其兩個原接點 u、v 在同一 C 內由奇數長原 bridge 路徑 P 相連；每個路徑點
連同全部旁支的局部 residual 都是 K。令 W_j 為刪除所有 P 邊後含 x_j 的
原路徑塊，T_j 為其全部 actual boundary support。rooted palette 唯一性給

\[
T_j\in\mathcal T(q,S_C,K)
=\{T\subseteq S_C:\operatorname{Stab}(q(T))\text{ 保持 }K\}. \tag{3}
\]

先選**同一份固定**連通三框弧分割 B=X⊔Y⊔D_B，使 (3) 中每個 T 都碰
X、Y，且某 i∈B_z 落在 D_B。取原 L=w–z–b_i；它內部避開 C 與 B。
J=P∪{wu,wv} 為原圈。第一條 bridge x₀x₁ 給五個 branch sets

\[
W_0,\quad W_1,\quad
(V(J)\setminus\{x_0,x_1\})\cup V(L)\cup D_B,\quad X,\quad Y. \tag{4}
\]

五組不交且各自連通；第三組經 w 與 L 連通，P 長度一時仍含 w。
原 bridge、J 上兩條朝外邊、兩路徑塊各到 X／Y 的實際附件，及 C5 的三個
切口，給全部十對鄰接，故 (4) 是原圖 K5 minor。附件落點可以不同，但
兩塊必須同時用這一份 X、Y；未合併分量或新添 w-spoke。

| 對 212 份支援逐一檢查 | 份數 |
| --- | ---: |
| C_w、D_w 各自有 source K5 | 188 |
| 只有 C_w 的本規則成功 | 12 |
| 只有 D_w 的本規則成功 | 12 |
| 兩者均未排除 | 0 |

「只有」指這項固定框弧規則，並不聲稱另一分量不存在任何其他 minor。
400 個成功的分量級反證各有一份以原 w–z–b_i 為外部路徑的 witness。
另外原 C_z／另一 w 分量的外部路徑也保存，但非本輪來源排除所必需。

原首項 ID=3040 恰落在新 records 66、68。兩筆皆有
B_z=01、S_Cz=04、S_Cw=12，S_Dw 分別為 234、24。
C_w 的 (3) 只有 {12}，選 X={1}、Y={2,3,4}、D_B={0}，
L=w–z–b0，即由 (4) 排除兩份。

record 4 更說明必須保存兩分量：其 sides=(137,32)，B_z=04，
(S_Cz,S_Cw,S_Dw)=(01,123,34)，source F=({1},{0,1},{1,2})。
C_w 的族為 {12,23,123}；每項單獨可找到框弧，但沒有一份分割通吃全族，
所以此規則不能在 C_w 下結論。D_w 的族只有 {34}，取
X=123、Y=4、D_B=0、L=w–z–b0，便有來源 K5。
record 10 是交換整個 C_w、D_w 的對應情形，不能固定只查第一個 pair。

任意大小來源必落在 §2 的必要表，而表中每份都違反 disk 平面性。
故本型不存在。**本輪 target 查詢與新增 target 接受數均為零**；
source 排除不記成 424 個雙列延拓。

## 4. 證書、出口接合與精確下一入口

[Checker](../scripts/c5_adjacent_degree5_no_mixed_t2_t0_overlap.py)、
[JSON](../artifacts/c5_adjacent_degree5_no_mixed_t2_t0_overlap/observations.json) 與
[支援表](../artifacts/c5_adjacent_degree5_no_mixed_t2_t0_overlap/support_table.md)
保留原 ID／SHA、完整 schemas、910 份幾何、三分量與六接點方向、兩份獨立
source evidence、全部固定框弧選言及具名原外部路徑。

1,968 份 K5 skeleton controls 中，1,200 份對全部 400 個分量級反證各核
長度 1／3／5；其餘 768 份涵蓋三種原外部路徑、16 種雙塊 tether 形狀、
不同附件供應點及外部鏈長。每份核對 actual supports、兩 root 完整 degree=5、
三分量不混接、branch sets 的不交／連通／十鄰接，另作反射與 root 交換。
skeletons 未要求其餘內點 degree／lists，不能當作來源實現。

13 個負控制包括：root 交錯、接點合併、pair marginals、空／單色支援、
只查 C_w 或只查 D_w 各漏 12 份、逐支援另選框弧、空族不是 K5，及遺失
原 zw／spoke／bridge／contact 或 branch sets 重疊。另核對全部 212 份
source 反射、整分量交換、整圖 root 交換及完整關係的色置換。

coverage_extension 逐 ID 綁定前輪 744 份與本輪正反向新增的 192 份。
936 份恰為原表中至少一側 t=2 的全部 joins，共九個有序格／五種交換型。
本輪兩格由來源排除完成；其餘四類沿用原雙列分離，不混稱 target 新結果。
[出口定理](c5_single_sided_exit.md) 第九類因此涵蓋所有至少一側 t=2 的
no-mixed 核心。實際來源只會落在已分離的四類；完整 Σ 仍由來源雙缺失與
刪邊繼承補回，不能由固定 q 排除另行推出任意來源的完整 Σ。

下一窄入口為 **B–B：t_z=t_w=1,(2,1)**，原 236 份有序 joins。
首項 retained-join ID=2142、sides=(91,91)，B_z=B_w={0}，兩側各有
F_pair(q)={1}、F_single(q)={2}，共同 c=3。保留四個原分量、六個具名
接點、兩條不同 root 的原 spokes 與 zw；即使首項兩 spoke 同落 b0，也不
合併。新 JSON 只綁定其 IDs／首項，尚未建立支援／rotation 覆蓋或遍歷 targets。

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t0_overlap.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t0_pairs.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t1_bridge.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
python3 scripts/c5_exchange_geometry_scope.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際執行與省略範圍見[當輪紀錄](history/2026-09-29-adjacent-no-mixed-t2-t0-overlap.md)。
`--check` 重算後逐 byte 比對，無參數只生成本層；舊證書保持原樣。
`lake build` 只驗既有 Lean 專案，未形式化本輪任意大小支援覆蓋或 K5 論證。
