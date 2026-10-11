---
docgraph:
  id: c5.adjacent-degree5-no-mixed-t2-t1-bridge
  family:
    - c5
    - c5.degree5
  derives_from:
    - c5.adjacent-degree5-no-mixed-t2-t1
  requires:
    - c5.adjacent-degree5-no-mixed-t2-bridge
    - c5.no-spoke-first-bridge
    - c5.single-spoke-first-bridge
    - c5.single-spoke-branch-palettes
  related:
    - c5.root-degree-excess
---
# 無 mixed t_z=2、t_w=1：record 14 的原外部路徑與首橋套表

後續（2026-09-29）：[原雙端點與完整 bridge 路徑](c5_adjacent_degree5_no_mixed_t2_t1_endpoints.md)
已關閉 record 22／p₂ 及其餘 65 個查詢；新增 66 個延拓，原 560 份全保留、
1,120／1,120 全證、0 未決／新來源排除，接入出口第九類。下文及原 artifacts
保留本輪 1,054／1,120 與 record 22 停止點；目前入口見 HANDOFF。

2026-09-29，接手基準 `f29b899`。[原支援表](c5_adjacent_degree5_no_mixed_t2_t1.md)
的 **record 14／p₁ 必延拓**：target 雙禁色迫使原 C_w 的每個路徑塊
碰 b1、b3，原 w–z–b0 路徑與同一份框弧分割給 K5 minor。
這筆由幾何阻斷關閉，不需要重建第二個 source 禁色。

局部引理套回既有 560 份必要支援，固定框弧新增 42 個指定列延拓，
同一首橋再新增 10 個；共 **1,054／1,120 查詢已證，66 個未決**。
494 份雙列皆證，33 份 A/?、33 份 ?/A；新增來源排除為 0。
原 136 份、560 份、完整關係與前序 artifacts 均保留。

證據為任意大小紙面抽取／palette 歸納、外部 degree-list 定理及
Python 有限控制。不需 T4，未新增 Lean theorem；未證必要支援
可實現、整型指定分離、完整 Σ、一般出口或 `K∞=K≤5`。
研究優先序只見 [HANDOFF](HANDOFF.md)。

## 1. 同一來源與局部引理的適用範圍

完整沿用 [原表 §1–3](c5_adjacent_degree5_no_mixed_t2_t1.md#1-同一來源五接點與-source-預算)：
M 有限簡單，B=(b0,…,b4) 是 induced C5 disk 外框，H=M−B 非空連通；
M 拒絕 q=01012，刪任一非框邊後接受。相鄰 z、w 完整 degree=5，
其餘內點完整 degree=4。H−{z,w} 無 mixed；z 有兩條原 spokes 及
二接點原分量 C_z，w 有一條原 spoke、二接點原分量 C_w 及單接點 D_w。

保留原 zw、三條 spokes、三份原分量、五個具名接點、全部附件、
bridges、旁支、環序與共同色框。D_w 是任意大小的原連通分量，
不是 spoke。U={0,1,2,3}，p₁=01021、p₂=01212。

對各原分量，完整接點關係 T_C(t) 非空，F_C(t) 是所有 tuples 色集
的交集。各列均以同一字面色框精確接合：

\[
 E_z(t)=U\setminus(t(B_z)\cup F_z(t)),\qquad
 E_w(t)=U\setminus(t(B_w)\cup F_w(t)\cup F_D(t)),\qquad
 Z_M(t)=(E_z(t)\times E_w(t))\setminus\Delta. \tag{1}
\]

source 的 F_z、F_w、F_D 均為已知 singleton；C_z、C_w 缺額一，
D_w 飽和。source 的預算沒有直接套到 target，D_w 的完整關係仍在 (1)。

固定 C=C_z 或 C_w，反設 target F_C(t)=A 是 pair。原表已證 C
K4-free；C 的兩個接點有 slack，固定任一 a∈A 後得到不可著色
degree lists。[Dvořák Lemma 7／Theorem 10，第 5–6 頁](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
給 tightness 與 Gallai block palettes，本輪核對原文。這個外部定理
不是 Python／Lean 所證，也不要求 target minimality。

[雙禁色 bridge 化約](c5_no_spoke_path_minor.md#1-前提完整關係與共用路徑塊)
只用 C 的 degree-4 點、兩接點、兩份拒絕證書及 K4-free；所以在本型
仍給兩接點間的奇數長原 bridge 路徑 P=(x₀,…,xℓ)，ℓ≥1。
刪全部 P 邊得到互不相交的原路徑塊 W_j，保留 x_j 的直接附件與
所有旁支。記全部實際支援 T_j⊆S_C。

在既存拒絕證書中，x_j 的直接 boundary 色為 D_j^t，路徑外 palettes
聯集為 Q_j^t。局部 residual L_j^t=U\(D_j^t∪Q_j^t)=A。
rooted-palette 唯一性迫使每份 T_j 屬於

\[
 \mathcal T(t,S_C,A)=\{T\subseteq S_C:
   \sigma t|_T=t|_T\Longrightarrow\sigma A=A\text{ for every }\sigma\in S_4\}. \tag{2}
\]

這個 L 不等於 root residual E；也不將 singleton F 當成 pair residual。
D_w 的接點數為一，沒有對它套用雙接點路徑引理。

## 2. 四種原外部路徑與固定三框弧

令 r 是 C 的 root，s 是另一 root。避開 C、第一次在 b_h 遇 B 的
原外部路徑 L 可以是：

- r–b_h：本側原 spoke。
- r–s–b_h：另一側原 spoke，保留 zw。
- r–D–b_h：同側另一具名原分量；本型即 r=w、D=D_w。
- r–s–D–b_h：另一側具名原分量，可為 C_z、C_w 或 D_w。

涉及 D 的記號是從其具名接點沿 D 的實際簡單路徑到實際附件，
不是新增邊或壓成 spoke。原分量的連通性與 h∈S_D 保證路徑存在；
它的內部避開 C 及 B。這補足三分量型的路徑來源，沒有直接套用
「兩分量＋四 spokes」的整份舊幾何表。

固定同一份 B=X⊔Y⊔D_B，各組非空且沿 C5 連通，L 的落點 h∈D_B。
若同一條原 bridge x_ix_(i+1) 的兩塊都碰 X、Y，令
J=P∪{rx₀,rxℓ}，取原圖的五個 branch sets：

\[
 W_i,\quad W_{i+1},\quad
 Z=(V(J)\setminus\{x_i,x_{i+1}\})\cup V(L)\cup D_B,\quad X,\quad Y. \tag{3}
\]

J 去掉相鄰兩點後的餘部經 r 連通；ℓ=1 時餘部是 {r}。L 接到 D_B，
所以 Z 連通。W 分割、原分量身份與框弧分割保證五組兩兩不交。
原 bridge 給 W_i–W_(i+1)，J 的兩條朝外邊給兩組 W–Z；四份實際
附件給兩組 W 各接 X、Y，三個 C5 切口給 X、Y、Z 彼此相鄰。
十對原邊鄰接形成 K5 minor，與 planarity 矛盾。

套 (2) 時，先固定一份三弧與一條原 L，再驗全部 T∈𝒯 都碰 X、Y。
兩塊可以用不同框點作供應點；不能逐支援另選框弧。空族表示原 W
不可能存在，另記 `no_possible_bag`，不把空全稱稱為 minor。
minor witness 未用到的分量、spokes 與接點仍保留在來源 M 與 (1)。

## 3. Record 14／p₁ 的關閉

原子表 ID=42，retained-join ID=3192，sides=(137,118)，共同 c=3：

\[
 B_z=04,\quad B_w=3,\quad (S_z,S_w,S_D)=(01,123,34),\qquad
 (F_z,F_w,F_D)(q)=(\{1\},\{0\},\{2\}).
\]

p₁ 下 F_z=F_D={1} 可完整搬運；E_z={2,3}，w-spoke 色為 2。
原完整候選表唯一失敗者為 F_w(p₁)={0,3}，使 E_w=∅。

反設該候選。p₁ 在 S_w=123 的字面色為 102，(2) 恰允許
T=13 或 123，故每個 W_j 都碰 b1、b3。在 (3) 取

\[
 i=0,\qquad X=\{b1,b2\},\quad Y=\{b3\},\quad
 D_B=\{b4,b0\},\quad L=w-z-b0.
\]

原 zw、zb0 使 Z 連通；五組即為 W₀、W₁、
(J−{x₀,x₁})∪{z,b0,b4}、{b1,b2}、{b3}。因此有原圖 K5 minor。
F_w(p₁)≠{0,3}，其餘十組完整 F 候選均有原 root 色對，p₁ 必延拓。
p₂ 的既有完整搬運保留，所以 record 14 雙列皆證。

這裡沒有宣稱 source q 本身不存在，也沒有添加 source 禁色。
原 D_w、34 支援、單接點及內部路徑仍完整保留。另一路合法 witness
可走 w–D_w–b4；它用原 D_w 路徑，也沒有假設 wb4 是原 spoke。

## 4. 同一首橋的 source singleton 限制

為套同一張表，另搬運 [首橋引理](c5_adjacent_degree5_no_mixed_t2_bridge.md#4-同一首橋-β-的跨列限制)。
令 F_C(q)={d}、F_C(t)=A 是 pair，P、W 仍由 target 的同一 C 抽取。
設 K={a:∀i∈S_C，q_i=a iff t_i=a}。旁支點沒有 root 邊，原
[固定色 palette 歸納](c5_single_spoke_branch_palettes.md#2-rooted-palette-唯一性與固定色守恆)
適用同一 W_j，給 L_j^q∩K=A∩K。

若 d∉K，本層不作首橋推論。若 d∈K，端點 tightness 給 d∈L₀^q，
所以 d∉A 立即矛盾。其餘情況首橋的 q palette 為同一 {β}、β≠d，
端點 tightness 及下一點的 bridge palettes 給

\[
 L_0^q=L_1^q=\{d,\beta\},\qquad
 \{d,\beta\}\cap K=A\cap K. \tag{4}
\]

ℓ=1 時下一點是另一原接點，仍由端點 tightness 得到 (4)。
兩塊的實際支援因此同時屬於
𝒯(q,S_C,{d,β})∩𝒯(t,S_C,A)。對每個 β 用 §2，全部 β 都不可能
才排除該 target 候選；不讓兩端各選獨立 β。
本型 root 的額外分量不進入 W 的歸納，只提供 §2 的真實外部路徑。
未套整條路徑 palette 交換或不守恆 d 的雙端點引理。

## 5. 完整套表、有限控制與停止點

[Checker](../scripts/c5_adjacent_degree5_no_mixed_t2_t1_bridge.py) 驗原生成器及
其依賴 SHA256，另綁定原 JSON hash；保留原 136 份、560 個 IDs、
3,150 份幾何、全部 placements、五接點 rotations、完整 q schemas
與原 unary relation。重算全部 3,148 組三分量完整 F 接合；每組先有
原 root 色對或被反證，才把整個 target 記為接受。

| 層 | 已證 target | 未決查詢 | 新來源排除 |
| --- | ---: | ---: | ---: |
| 原支援／容量 | 1,002 | 118 | 0 |
| 固定三框弧與原外部路徑 | 1,044 | 76 | 0 |
| 再加同一首橋 | 1,054 | 66 | 0 |

原 146 組失敗候選中，三框弧消去 70，首橋再消去 10；剩 66 組各屬
一個查詢，empty_z 36、empty_w 30，same_singleton 18 組全已排除。
候選數與查詢數不同；新增 52 個延拓，不能把消去 80 候選稱為 80 延拓。

有限控制包含：

- 獨立 3⁵ 指派重建 60 份三弧分割；576 份穩定子與 48 份 pair residual
  控制，並重算既有 8,748 個固定色歸納步、48 份端點及 24 份首橋控制。
- 1,374 份 K5 skeletons：保留三分量、三 spokes、五接點及 root degree=5；
  涵蓋四種外部路徑、奇數長度 1／3／5、16 種雙塊 tether 形狀、獨立
  框點供應及長度 1／3 的外部分量內部鏈，每份驗十鄰接、反射與 root 交換。
- 146 組失敗候選的字面反射及完整 root 交換，另有 3,148 組完整 root
  色對交換；交換整份分量歸屬與 spokes，D_w 仍是同一具名分量。
- 15 個負控制，含 singleton／單接點 guard、非守恆 d、固定分割量詞、
  部分候選尚未覆蓋、空族，以及缺 zw／spoke／bridge／附件／框弧、
  branch sets 重疊、D_w 接點／內部邊／實際附件缺失。

這些 skeletons 不要求全部 degree/list 來源條件，並非 disk 實現；
刪邊負控制只否定指定 witness，不宣稱刪後圖平面。任意大小覆蓋由
§1–4 的紙面論證及外部定理承擔。

**下一窄入口為 record 22／p₂**：原子表 ID=39、retained-join ID=3189、
sides=(137,102)，B_z=04、B_w=1，支援 (S_z,S_w,S_D)=(01,234,12)，
source F=({1},{2},{0})、c=3。p₂ 下 F_z={1}、F_D={2} 精確；唯一失敗
候選仍為 F_w={0,3}，給 E_z={3}、E_w=∅。
此處 C_w 的 d=2 不在 K={1,3}；target 路徑塊族為 23、34、234，
沒有本層的統一三框弧 witness，首橋固定色條件亦不適用。
後續需保留 C_w 的 source singleton 證書、兩端點及全原 bridge 路徑，
並保留 D_w 的 12 支援與實際外部路徑，處理不守恆 source 禁色的限制。
record 22 仍是未決上界候選，不是已找到的 disk 反例。

## 6. 重播與信任界線

[JSON](../artifacts/c5_adjacent_degree5_no_mixed_t2_t1_bridge/observations.json)
與 [逐筆表](../artifacts/c5_adjacent_degree5_no_mixed_t2_t1_bridge/support_table.md)
保存每筆閉合原因及剩餘候選。原支援與前序證書不覆寫。

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t1_bridge.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t1.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_bridge.py --check
python3 scripts/c5_single_spoke_first_bridge.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
python3 scripts/c5_single_spoke_branch_palettes.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證與省略範圍見 [當輪紀錄](history/2026-09-29-adjacent-no-mixed-t2-t1-bridge.md)。
`--check` 重算並逐 byte 比對，無參數只生成本層。`lake build` 僅驗既有
Lean 專案，不形式化本輪的紙面證明、外部 degree-list 定理或 disk 拓撲。
