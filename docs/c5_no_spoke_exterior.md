---
docgraph:
  id: c5.no-spoke-exterior
  family:
    - c5
    - c5.no-spoke
  requires:
    - c5.degree5-interfaces
    - c5.single-spoke-three-one
    - c5.single-spoke-four
---
# No-spoke 核心：外部連通、K4 排除與六型收窄為兩型

後續（2026-09-28）：[環狀實際支援與指定分離](c5_no_spoke_supports.md)
已完成 (2,1,1,1) 的兩種必要支援型、48 筆全部 p₁／p₂ 延拓，並接回
條件式單側出口。(2,2,1) 支援表原保留 616 筆；後由
[原外部路徑 K5](c5_no_spoke_path_minor.md) 排除 500 筆，剩 116 筆中
108 筆雙列已證、12 個查詢未決；
下文 72 份覆蓋與當輪未決界線保留，不表示目前兩型都尚未分離。

2026-09-28。接續 [single-spoke (4)](c5_single_spoke_four.md) 的下一入口；
研究優先序見 [HANDOFF](HANDOFF.md)。

**唯一完整 degree-5 點 z 沒有 boundary spoke 時，minimal q-core 的
接點分拆只可能是 (2,2,1) 或 (2,1,1,1)，且每個 degree-4 分量都不含
K4 block。** 原六型中的 (5)、(4,1)、(3,2)、(3,1,1) 已排除；
不需要 T4 acceptance 或第二列拒絕，也不限制來源大小。

多分量情形的每一分量都實際碰 B，另一原分量提供避開指定分量的 z–B
路徑，恢復同一外部 hub。單分量 (5) 則由四份拒絕 palettes 迫使接點數
為偶數而排除，沒有假設 z 與 B 在 C 外連通。

證據是任意大小紙面證明、外部 degree-list 定理與 Python 有限控制；
未 Lean 化。兩個保留分拆僅為必要條件，沒有證其 disk 可實現性、完整 Σ
或指定 p 延拓。[一般單側出口](c5_single_sided_exit.md) 與主命題仍未證。

## 1. 同一來源與完整禁色覆蓋

G 有限簡單，B=(b0,…,b4) 是 induced-C5 disk 外框，有效內部 H 非空連通。
G 是 q=01012 的 edge-minimal obstruction。唯一完整 degree-5 內點 z
滿足 N_B(z)=∅；其餘有效內點完整 degree=4。所有 degrees 都在此核心
G 自己計算。記 U={0,1,2,3}，H−z 的原分量為 C₁,…,Cᵣ，
Pᵢ=N(z)∩Cᵢ 為具名、有序且非空的原接點集，Σᵢ|Pᵢ|=5。
保留原 boundary 次序、全部附件、旁支、嵌入與分量身份。

對每個 C 沿用 [完整介面](c5_degree5_interfaces.md)：

\[
R_C(q)=\{(f(u))_{u\in P_C}: f\text{ 是同一 }C\text{ 的合法 boundary-list coloring}\},
\qquad F_C(q)=\bigcap_{t\in R_C(q)}\operatorname{set}(t).
\]

R_C 非空：未指定 z 色時，lists L(v)=U\q(N_B(v)) 滿足
|L(v)|≥deg_C(v)，且每個接點有至少一色 slack。連通貪婪引理可著色。
因此 |F_C|≤|P_C|。minimality 的不可刪減覆蓋給

\[
\bigcup_i F_i=U,\qquad
F_i\setminus\bigcup_{j\ne i}F_j\ne\varnothing. \tag{1}
\]

故 r≤4，原六種必要分拆正是
(5)、(4,1)、(3,2)、(3,1,1)、(2,2,1)、(2,1,1,1)。
所有 F_i 都從同一圖、同一 q、完整接點 tuples 投影，不能獨立指定
各接點的 marginals 或替換某一分量。

固定 d∈F_C，對接點再刪色 d 得 M_d(v)。完整 degree=4 給
|M_d(v)|≥deg_C(v)，拒絕使處處等號。外部
[Dvořák 講義 Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
給 tightness、Gallai tree 及 blockwise-uniform palettes；本輪已重讀。
每點 incident palettes 不交且聯集為 M_d(v)。本報告不將此外部定理
計為 Python 或 Lean 已證。

## 2. 多分量的真實外部路徑

假設 r≥2。由 (1)，每個 F_C 非空且不是 U：若一個等於 U，任何另一
分量都沒有 private color。

**每個 C 都有 boundary 附件。** 否則 C 的全部 boundary lists 都是 U，
完整 R_C 在同一個 S₄ 全域色置換下不變，故 F_C 也在 S₄ 下不變。
U 的不變子集只有 ∅、U，均與上述非空真子集矛盾。
這裡的置換作用於整個 C coloring，沒有逐接點獨立換色。

因此對指定 C，取任何另一原分量 D。D 連通、P_D 非空且 D 碰 B，
可沿原 contact、D 內簡單路徑及實際 boundary 邊得到

\[
Q=z\,w_0\cdots w_k\,b_j,\qquad V(Q)\setminus\{z,b_j\}\subseteq D.
\]

Q 的內部避開整個 C，亦不包含其他 boundary 頂點。令
X=B∪{z}∪V(Q)，則 X 是在 C 外的同一連通集合。
不要求 D 與 C 共享支援色，不收縮 Q 來改寫原 R_D，也不新增 spoke。

## 3. 以另一分量恢復 K4 的外部 hub

仍取 r≥2。假設 C 有 K4 block J，固定 d∈F_C。
J 的每個頂點已有三條 clique 邊，完整 degree=4 留下恰一條外接邊。
它直達 B∪{z}，或是 bridge，進入 C−J 的一個分支 W；不同 J 頂點
的這些分支互不相交，亦不返回 J 的另一點，否則 J 不是 block。

若是 bridge vw，刪邊後兩側在固定 M_d lists 下皆可著色：各連通側
根的 degree 少一，有 slack。原 C 不可著色，所以兩側根的可取色集
必為同一 singleton；只要能選相異色就能拼回。W 必碰 B∪{z}，
否則其 lists 全是 U，可整體置換四色，根不會只取一色。

於是從 J 的四點各有一條原 tether T_v 到 B∪{z}，內部兩兩不交，
且都在 C 中。由 §2 的另一分量 Q，把

\[
O=B\cup\{z\}\cup V(Q)\cup\bigcup_{v\in J}(V(T_v)\setminus\{v\})
\]

合成一個連通 hub。J 的四個 singleton 與 O 互不相交；六條 clique
邊及四條 tether 首邊給 K5 minor，與 planarity 矛盾。

所以 **多分量 t=0 的每個 C 都 K4-free**。這是
[既有連通外框引理](c5_degree5_tree_components.md#1-連通外框排除-degree-4-分量的-k4)
的新適用範圍：連通性由另一原分量提供，不再要求 z 的直接 spoke。
外框在 minor 的 hub 中會被合併；這只用來反證非平面性，不是保持 Σ
的 boundary-state 操作。

## 4. 單分量 (5)：四份 palettes 的偶數接點障礙

本節獨立於 §2–3；不假設 C 外連通或 C 為 K4-free。
若 r=1，(1) 給 F_C=U，五個原接點在每份 M_d 中都刪去 d。
tightness 迫使接點沒有 boundary 鄰居，且對任意 a≠b：

\[
\mathbf1_{M_a(v)}-\mathbf1_{M_b(v)}
 =\mathbf1_{P}(v)(\mathbf e_b-\mathbf e_a). \tag{2}
\]

令 I 為同一原 C 的 vertex–block incidence matrix。其欄線性獨立：
leaf block 的 private vertex 先迫使該欄係數零，刪去該 block 的私有點
再歸納。C 有五個接點，故不是 singleton。

沿用 [共同係數論證](c5_single_spoke_four.md#2-三組差異共用一個係數向量)，
逐色展開 (2)，欄獨立性給唯一共同 τ，滿足

\[
I\tau=\mathbf1_P,\qquad
\mathbf1_{S_K^a}-\mathbf1_{S_K^b}
 =\tau_K(\mathbf e_b-\mathbf e_a),\qquad \tau_K\in\{-1,0,1\}.
\]

現在 d 遍歷全部四個色，沒有剩餘固定色可加入 active palettes：

| τ_K | 四份 S_K^d | block |
| --- | --- | --- |
| 0 | 同一固定 palette | 不 active |
| +1 | U\{d} | K4 |
| −1 | {d} | bridge |

planarity 排除更大 clique；Gallai 結構中 palette 大小三只可能來自
K4，大小一只來自 bridge。此處確實保留了 K4，沒有循環引用 §3。

同一頂點的正、負 palettes 至多各一個。因此接點恰接一個正 K4、
沒有負 bridge；其餘 active 頂點恰接一個正 K4 及一個負 bridge。
取所有 active blocks 的全部 incidence edges，得到原 incidence tree
的一個 forest，vertex-nodes 的葉點恰是五個原接點。
block-nodes 的 degree 則為四（正 K4）或二（負 bridge）。

若該 forest 有 h 個非空分量、k 個 K4 nodes，樹的葉數公式給

\[
|P|=2h+\sum_{\text{block nodes }K}(|V(K)|-2)=2h+2k.
\]

右側為偶數，與 |P|=5 矛盾。故 **(5) 不存在**。
不需要先找到 z–B 路徑，也沒有引用四色定理。
另可核對 degree 飽和：正 K4 在接點已用三條 clique 邊及 contact，
非接點另有負 bridge；active 頂點沒有容納 inactive 旁支的餘額。

## 5. 多分量的三、四接點分量也排除

以下均使用 §3 已證的 K4-free。三接點分量只要 |F_C|≥2，選兩個
不同禁色，便可逐步沿用
[三接點 active triangle 論證](c5_single_spoke_three_one.md#2-三個葉點迫使唯一-triangle-加三臂)：
同一 incidence forest 的三個葉點迫使唯一 triangle 加三條同 parity
bridge arms，終點恰是三個原接點。該證明僅用兩份拒絕 lists、degree=4
與 K4-free，不用 z 的 spoke，也不要求 F_C 恰只有兩色。

triangle 三點各留一條其餘邊；它直達 B，或進入不含任何 contact 的
inactive 旁支。若該旁支不碰 B，slack-list coloring 加全域色置換就能
拼回被拒絕的 M_d coloring。因此三條實際 boundary tethers 存在，
內部互不相交且避開 arms。這正是
[原 tether 論證](c5_single_spoke_three_one.md#3-每個-triangle-頂點的實際-boundary-tether)，
另一原分量的邊不可能進入這些 C 內旁支。

令 V₀、V₁、V₂ 為三條完整 arms（包括 triangle 端點與原 contact），
Z={z}，並取

\[
O=B\cup\bigcup_i(V(T_i)\setminus\{v_i\})\cup(V(Q)\setminus\{z\}).
\]

Q 的內部在另一原分量，故五組互不相交且連通。Vᵢ 兩兩的鄰接來自
triangle，Z–Vᵢ 來自原 contacts，Vᵢ–O 來自 tethers，Z–O 來自
**Q 的第一條原 contact 邊**。這給 K5，排除三接點、至少兩禁色的 C。
未把另一分量併入 C 的 coloring relation。

四接點分量若拒絕三色 A，沿用
[三份 palettes 的共同結構](c5_single_spoke_four.md#3-四葉共同樹恰為兩-triangle-加一條-bridge)：
正 block 不能是 bridge，四葉 forest 恰為兩個正 triangle 加單負 bridge，
四個原 contacts 為兩 triangle 各自另外兩點。此證明只用 |A|=3 與
K4-free，第四個色不必來自 z 的 spoke。

記兩 triangle 為 {a,b,x}、{c,d,y}，bridge 為 xy。沿用左 triangle 的
三條原 boundary tethers，取 {a}、{b}、{x}、Z={z,c,d,y}，以及上式的
O（把三條 tethers 換成左 triangle 的）。Z–O 同樣由 Q 的第一邊給出，
其餘九條鄰接正是 [既有 minor](c5_single_spoke_four.md#5-原圖-k5-的五個-branch-sets)。
故四接點、至少三禁色的 C 亦不存在。

現在直接以 (1) 核對各分拆：

| 分拆 | 覆蓋強迫的必要條件 | 排除 |
| --- | --- | --- |
| (5) | F_C=U | §4 四列偶數接點 |
| (4,1) | 單接點 F_D={c}，F_C=U\{c} | 四接點三拒絕 K5 |
| (3,2) | 二接點至多兩禁色，所以三接點至少兩禁色 | 三接點兩拒絕 K5 |
| (3,1,1) | 單接點各至多一禁色，所以三接點至少兩禁色 | 三接點兩拒絕 K5 |

於是只有 (2,2,1)、(2,1,1,1) 保留；它們都屬多分量，故各分量
K4-free。整個排除不需 T4、p₁／p₂ 拒絕或來源大小界。

## 6. 兩個保留分拆的覆蓋正常形

僅整理 q 下的必要覆蓋，不宣稱有 disk 來源。

- (2,1,1,1)：四個 F 都是不同 singleton，恰分割 U。
  三個單接點的 private colors 必相異，二接點 F 不得包含它們，
  因而也恰為剩下的一色。
- (2,2,1)：單接點為 {d}，兩個二接點都避開 d。若兩者不交，
  大小為 2、1（或 1、2），三份 F 分割 U；若相交，兩者大小均二，
  交集恰一色，聯集 U\{d}。

以具名分量及字面四色計，兩型分別有 24、48 份必要覆蓋，其中後者
的分割型 24 份、共色型 24 份。這些 72 筆不是支援型、來源圖或指定
target 接受證書；反射同時以 ρ(i)=3−i 搬 boundary、π=(0 1) 搬全色框。

下一個窄問題是固定這些覆蓋、保留五個原接點及各分量全部實際支援，
推導 t=0 的平面支援／次序必要條件，再處理相鄰 singleton 的
p₁=01021、p₂=01212。沒有 spoke 時不能直接照抄 single-spoke 的
slit frame 或把不同分量的 root 關係重新命名後相乘。

## 7. Python 控制與實際驗證範圍

[checker](../scripts/c5_no_spoke_exterior.py) 與
[JSON 證書](../artifacts/c5_no_spoke_exterior/observations.json) 保存：

- 六分拆的 111 份具名不可刪減覆蓋，逐份核對 private colors、排除理由
  及反射；72 份保留。空支援的 S₄ 不變子集另核對為 ∅、U。
- 1,808 組四列 block palettes 全測，16 組相容型、52 個 local incidence
  型；另以 35 組 (h,k) 核對偶數葉公式。任意大小結論由 §4 的樹公式
  承擔，不由有限範圍外推。
- 一個及兩個 K4 以 bridge 相接的完整有序接點關係，接點數四、六，
  均有 F=U；五接點刪減負控制則 F=∅。這些是抽象代數控制，沒有
  聲稱加入 z 後平面；刪掉第六 contact 也不再符合完整 degree=4。
  同時核對 endpoint marginals 會錯誤放行全部 z 色。
- 160 份 K4 外部 hub、160 份三接點及 240 份四接點 K5 證書，共 560
  份及其 560 份反射。三／四接點骨架逐份保留五個原 contacts、零 spoke
  及分量分拆；K4 骨架測全部 16 種 tether 終點選 z／B 的模式。
  長度與角色排列只作有限控制，不是完整 degree-list 來源枚舉。
- 九個負控制：每種 minor 各刪外部路徑、刪 tether、破壞 branch-set
  不交性；只聲稱指定 witness 失效，不聲稱修改後整圖必平面。

輸入 SHA256 綁定前序三／四接點 checker 及 artifacts；前序證書只讀。

```bash
python3 scripts/c5_no_spoke_exterior.py --check
python3 scripts/c5_single_spoke_four.py --check
python3 scripts/c5_single_spoke_three_one.py --check
python3 scripts/c5_single_spoke_cores.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際執行與未重跑項目見 [本輪紀錄](history/2026-09-28-no-spoke-exterior.md)。
沒有新增 Lean theorem；外部連通、任意大小 palette 樹及來源 minor 抽取
仍是紙面證明。(2,2) 舊有 278 來源排除及 102 筆／51 型雙列計數未改。
