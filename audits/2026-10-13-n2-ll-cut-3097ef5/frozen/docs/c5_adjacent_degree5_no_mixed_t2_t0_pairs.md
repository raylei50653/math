---
docgraph:
  id: c5.adjacent-degree5-no-mixed-t2-t0-pairs
  family:
    - c5
    - c5.degree5
  derives_from:
    - c5.adjacent-degree5-no-mixed-t2-t0-singles
    - c5.adjacent-degree5-no-mixed
  requires:
    - c5.single-spoke-two-two
    - c5.single-spoke-frame-arc
    - c5.adjacent-degree5-no-mixed-t2-t1-bridge
  related:
    - c5.exchange-geometry-scope
    - c5.single-sided-exit
---
# 無 mixed t_z=2、t_w=0,(2,2)：缺額型的飽和分量與雙列分離

後續（2026-09-29）：[重疊型 D_w=0、O_w=1](c5_adjacent_degree5_no_mixed_t2_t0_overlap.md)
已獨立重建 212 份必要支援並全部 source K5 排除，0 target 查詢。兩種 (2,2)
預算均完成；覆蓋擴至五類／936 份，下一入口為 B–B。下文及原證書保留缺額型當輪結果。

整理（2026-09-29）：本型與前序四組成果的提交範圍、十四個 checker 重播及
遠端 HANDOFF 整合見 [發布核對](history/2026-09-29-no-mixed-progress-publish.md)。

2026-09-29，Git 基準 `f29b899`，保留工作區已有成果。
**D_w=1、O_w=0 的整型雙列分離完成。** 原 96 份有序資料接上
910 份同源支援／環序後得到 364 份必要配置；原飽和分量的 q 路徑
給 340 份來源 K5，保留 24 份的 48 個指定查詢全部接受。
其中 40 個由完整搬運／容量上界直接完成，8 個再由 target 原路徑 K5 完成。
不需 T4，不需新交換引理，也沒有把二禁色分量套入 singleton 的第二禁色反證。

證據為任意大小紙面化約、外部 degree-list 定理及 Python 有限證書；
未新增 Lean theorem，必要配置與 minor skeletons 均不宣稱可實現。
本型及整圖 root 交換型接回 [出口定理](c5_single_sided_exit.md) 第九類。
一般機制完備性、共同出口及 K∞=K≤5 仍未證；研究優先序見 [HANDOFF](HANDOFF.md)。

## 1. 同一來源、完整接合及 96 份資料

M 有限簡單，B=(b0,…,b4) 是 induced C5 disk 外框，H=M−B 非空連通。
M 為 edge-minimal q=01012 obstruction，minimality 不包含框邊。
相鄰 z、w 完整 degree=5，其餘內點完整 degree=4；H−{z,w} 無 mixed。
z 有兩條原 spokes 及二接點 C_z；w 無 spoke，有兩個不同二接點原分量
C_w、D_w。它們不是單點替代物，六個 contacts 始終具名。

沿用 [no-mixed 化約](c5_adjacent_degree5_no_mixed.md) 的完整關係 T_C(t) 與
F_C(t)=⋂_{a∈T_C(t)}set(a)。T_C 非空，|F_C(t)|≤2。
令 U={0,1,2,3}，p₁=01021、p₂=01212，則精確接合為

\[
E_z(t)=U\setminus(t(B_z)\cup F_{C_z}(t)),\qquad
E_w(t)=U\setminus(F_{C_w}(t)\cup F_{D_w}(t)),\qquad
Z_M(t)=(E_z(t)\times E_w(t))\setminus\Delta. \tag{1}
\]

固定 source q，兩 root residual 同為 {c}；q 在 B_z 上單射。
本輪 w 預算為 (D_w,O_w,κ_w)=(1,0,0)，故

\[
F_{C_z}(q)=U\setminus(q(B_z)\cup\{c\}),\quad
(F_{C_w}(q),F_{D_w}(q))=(\{a\},\{b,e\})\text{ 或反序},\quad
\{a,b,e\}=U\setminus\{c\}. \tag{2}
\]

保持原分量次序，(1,2)／(2,1) 各 48 份。checker 一方面逐 ID 讀取原
3,548 份 joins，另一方面由 (2) 直接重建 96 份，兩者完全相同；並核對
[前輪 next_frontier](../artifacts/c5_adjacent_degree5_no_mixed_t2_t0_singles/observations.json)
的 SHA／IDs。首項仍為 retained-join ID=3036、sides=(133,16)，
B_z=01、F_Cz={2}、w 禁色=({0},{1,2})、c=3。

每個 q 禁色及每個座標都有完整 contact-edge release witness。
因此 singleton 有 95 份完整 binary schema；pair F={a,b} 的完整關係
**恰為 {(a,b),(b,a)}**。每份支援還須讓逐點固定 q(S_C) 的色穩定子
保持整個 schema，不能只檢查 marginals。獨立掃描 65,535 份非空
binary relations 恰重建 380 份 singleton 與 6 份 pair schemas。

## 2. 三分量、五單位的任意大小支援覆蓋

各 F_C(q) 為非空真子集；若 C 不碰 B，整份 T_C(q) 在 S₄ 下不變，
F_C(q) 也須不變，矛盾。因此各 C 都有實際 contact—C 內部—B 路徑。
對 w 側任一 C，原 w–z–b_i（i∈B_z）避開它；對 C_z，使用原 zw
及任一 w 側分量的實際接框路徑。沿用 [外部 hub](c5_no_spoke_exterior.md)
引理，各 C 都 K4-free。

若 d∈F_C(q)，扣 root 色 d 的 lists 逐點至少 deg_C，拒絕迫使處處 tight，
且 C 為帶 block palettes 的 Gallai tree。這一步使用
[Dvořák 講義 Lemma 7／Theorem 10，第 5–6 頁](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，
本輪重讀核對。它是外部定理，並非本專案 Python／Lean 所證。

每份 actual support S_C 至少見兩個 q 色。對 pair F，固定一色的 S₃
穩定子沒有不變二元子集，故不能只見一色；對 singleton F，若只見 d，
穩定子迫 F={d}，root 也取 d 時所有外鄰同色。tightness 使每點最多
一個外鄰，故 deg_C≥3，與 K4-free Gallai leaf block 有私有點內度≤2
矛盾。這證明三份 actual supports 都至少兩點、正跨度。

取原 zw 的細閉正則鄰域。其外側至 B 為 annulus，兩 root 的其餘
incidences 各成一段。每個二接點分量的兩 contacts 在其 root 段內相鄰：
否則原 contact 邊和 C 內路徑形成的 Jordan 曲線，將另一 incidence
困在不含 B 的一側；但該 incidence 可沿原 spoke 或另一原分量到 B，矛盾。
因而必要 cyclic word 為

\[
\operatorname{perm}(C_z,z0,z1)\,\operatorname{perm}(C_w,D_w). \tag{3}
\]

原 crosscut 次序使各單位外端在 B 同序成塊，允許相鄰單位共用框點。
切在 C_z 的首端，所有支援有 lifts，依 (3) 滿足前一 max≤後一 min，
最後 max≤5；三個分量各跨度≥1、總和≤5，spokes 跨度為零。
每份分量跨度≤3，無需重複提升同一框點。保留支援的間隙，不補齊整弧。

一算法按 lifts 和單位次序生成；另一算法直接枚舉每側支援 hulls，
要求同側不交且兩側整體框邊 masks 不交。兩算法恰同得 **910 份**，
每份一 placement；12 個模板各保存 8 種三分量接點方向，共 7,280 次核對。
接上 (2)、支援穩定子和完整 schemas 後有 364 份；原 96 份中 54 份有
支援、42 份纖維空。此為必要覆蓋，不是每份資料的 disk 實現。

## 3. 飽和二禁色分量的原路徑 K5

固定本輪 source 飽和的 w 側分量 C，原兩接點 u,v。
在任一 proper row t，若 F_C(t)={a,b}，既有
[雙禁色路徑化約](c5_single_spoke_two_two.md#雙禁色的同圖奇數-bridge-路徑)
給同一 C 內 u–v 的奇數長原 bridge 路徑 P；比較兩份拒絕 palettes，
每個路徑點連同全部旁支的局部 residual 都恰為 {a,b}。
其旁支大小不受限，端點的直接附件亦保留。

令 W_j 為刪除全部 P 邊後的路徑塊，T_j 為 W_j 全部 actual support。
rooted palette 唯一性給必要族

\[
T_j\in\mathcal T(t,S_C,\{a,b\})
=\{T\subseteq S_C:\text{所有逐色固定 }t(T)\text{ 的置換均保持 }\{a,b\}\}. \tag{4}
\]

先固定同一三個非空連通框弧 B=X⊔Y⊔D_B，以及內部避開 C、B 的
原 w–B 路徑 L，其落點在 D_B。若 (4) 的每個 T 都碰 X、Y，
取第一條 bridge x₀x₁ 及 J=P∪{wu,wv}，五個 branch sets 為

\[
W_0,\quad W_1,\quad
(V(J)\setminus\{x_0,x_1\})\cup V(L)\cup D_B,\quad X,\quad Y. \tag{5}
\]

第三組經 w 連通；長度一時仍有 w。原 bridge、兩條朝外的 J 邊、
兩塊到 X／Y 的四份實際附件，以及 C5 三個切口，給十對鄰接。
同一固定框弧分割、原分量身份與 L 避開 C 保證五組不交，所以是原 K5。
L 可為 w–z–b_i，也可經另一原分量，絕不新增 w-spoke 或合併分量。
不同 W 可用不同附件落點，只須同時落入同一 X、Y。

將 t=q 代入，364 份中 **340 份有來源 K5**。例如 record 0：
B_z=04，(S_Cz,S_Cw,S_Dw)=(01,12,234)，source F=({1},{0},{1,2})。
對 D_w，(4) 恰為 {34,234}。取 X=123、Y=4、D_B=0、L=w–z–b0，
式 (5) 立即排除來源。其他 339 份各有完整、具名的同型 witness。

只剩 24 份支援，分屬 16 個原正常形；其中共同 c 為 3 的有 20 份，
c=0、1 各 2 份，不能只留下未用色 c=3。
此層有來源排除；下一節的 target 反證只排除該 target 失敗候選。

## 4. 剩餘 24 份的完整雙列接合

每個 C 先嘗試在**全部 actual support** 上以同一四色置換對齊 q、t，
能對齊便搬運完整 T_C 與 F_C。否則保存全部大小≤2、受 t(S_C)
穩定子保持的禁色候選，包括空集；不聲稱各候選有共同來源。
對每組完整 (F_Cz,F_Cw,F_Dw) 重算式 (1)，並獨立枚舉 U² 核對原 root 色對。

| 項目 | 數量 |
| --- | ---: |
| 保留支援／指定 target 查詢 | 24／48 |
| 三份完整關係皆搬運即可接受 | 24 |
| 搬運與容量上界即可接受 | 16 |
| target 原路徑 K5 再完成 | 8 |
| 完整 target joins | 640 |
| 原失敗 joins，全部 same_singleton | 8 |
| 雙列皆證／未決查詢 | 24／0 |

最後八個失敗候選都使 E_z=E_w 為 singleton；source 飽和分量的 target F
仍為 pair，故可在 target 直接套 (4)–(5)。不需要跨列 pair residual
聯立、singleton 首橋、第二／第三 source 禁色或整路徑 palette 交換。

以下四筆，加上整分量 C_w／D_w 交換，恰覆蓋全部八筆：

| record／列 | source pair → target pair | target 路徑塊族 | 固定 X／Y／D_B | 原 L |
| --- | --- | --- | --- | --- |
| 79／p₁ | {0,1} → {2,3} | 12、123 | 01／2／34 | w–z–b4 |
| 80／p₁ | {2,3} → {1,3} | 23、123 | 012／3／4 | w–z–b4 |
| 278／p₂ | {0,1} → {0,3} | 12、012 | 01／2／34 | w–z–b4 |
| 279／p₂ | {2,3} → {2,3} | 01、012 | 0／1／234 | w–z–b2 |

例如 record 79 的原 sides=(141,28)、retained-join ID=3299：
B_z=14、支援 (014,123,34)、q 禁色=({0},{0,1},{2})、c=3。
唯一失敗 target 候選 ({2,3},{2,3},{1}) 使 E_z=E_w={0}。
對原 C_w，p₁ 在支援 123 上是 102，保持 {2,3} 的 residual 必見補集色
0、1，故兩塊皆碰 b1、b2；表中固定弧及原 w–z–b4 給 K5。
這只反駁該候選，record 79 source 仍保留。

因此 §1 圖類全部接受 p₁、p₂。整圖交換 roots 時，同時交換原分量歸屬
與兩 spokes，完整 Z 的非對角條件不變，故反向有序型也完成。
出口第九類另在來源 Σ(G)=Ω∖{p,q} 下由刪邊繼承其餘八列，才得
Σ(M)=Ω∖{q}；不由 48 個指定接受單獨推出完整 Σ。

## 5. 證書、控制與下一入口

[Checker](../scripts/c5_adjacent_degree5_no_mixed_t2_t0_pairs.py)、
[JSON](../artifacts/c5_adjacent_degree5_no_mixed_t2_t0_pairs/observations.json) 與
[支援／原纖維表](../artifacts/c5_adjacent_degree5_no_mixed_t2_t0_pairs/support_table.md)
保存完整原 IDs／SHA、910 份幾何、三分量完整 schemas、六接點 rotations、
340 份來源反證、24 份全部 target joins 及每個原外部路徑 witness。

1,812 份 K5 skeleton controls 包含每份 340＋8 反證的長度 1／3／5，
再涵蓋三種原外部路徑、16 種雙塊 tether 形狀、獨立附件供應點及外部鏈長。
各份核對實際支援、三原分量不混接、兩 root 完整 degree=5、十鄰接，
並作 root 交換和反射。skeletons 不保證其餘 degree／lists 或 disk 實現。
13 個負控制涵蓋 root 交錯、具名接點合併、失去 zw／spoke／bridge／contact、
branch sets 重疊、pair marginals、空／單色支援、singleton target、
部分候選覆蓋不足，以及不能把 target K5 改記成 source 排除。

另有 364 次 source 反射、48 次字面 target 反射、364 次整分量交換，
1,004 組完整 root 色對交換。沿用 576 份穩定子代數控制。
`coverage_extension` 綁定前輪範圍表及原 3,548 份：增加本型正反向 192 份，
累計 **四種交換型／744 份**已覆蓋，其餘 2,804 份所在子類仍開放；
這些是必要資料份數，不是來源圖數量。前輪 checker／artifacts 保持原樣。

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t0_pairs.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t0_singles.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t1_bridge.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
python3 scripts/c5_root_degree_excess.py --check
python3 scripts/c5_exchange_geometry_scope.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證與省略範圍見 [當輪紀錄](history/2026-09-29-adjacent-no-mixed-t2-t0-pairs.md)。
`--check` 重算並逐 byte 比對，無參數只生成本層；`lake build` 不形式化紙面拓撲。
另執行舊 `c5_single_spoke_two_two.py --check` 時，只有其封存的
`docs/c5_single_spoke_cores.md` SHA 與目前文件不同。新 checker 的
`legacy_two_contact_replay` 逐項核對全部數學 payload 及 Markdown 生成表
完全相同，保存舊／新 SHA；舊嚴格 hash 檢查仍記失敗，未覆寫舊證書。

下一窄入口為 **同分拆 D_w=0、O_w=1**，原 96 份，兩個 w 側分量均飽和。
首項 retained-join ID=3040、sides=(133,30)，B_z=01、F_Cz={2}，
w 禁色=({0,1},{0,2})、c=3。保留各 pair 的完整交換 relation、六接點、
原 zw 與兩 spokes；新 JSON 只讀出 IDs，不宣稱已掃過此型支援／target。
