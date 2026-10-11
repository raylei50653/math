---
docgraph:
  id: c5.single-spoke-three-one
  family:
    - c5
    - c5.single-spoke
  requires:
    - c5.single-spoke-cores
    - c5.two-spoke-three-contacts
---
# Single-spoke (3,1)：三接點 active triangle 與原圖 K5 排除

後續（2026-09-28）：本頁最後的 (4) 入口已由
[三拒絕共同結構與 K5](c5_single_spoke_four.md) 完成。三組差異共用 τ，
正 bridge 不可能，四葉只剩兩 triangle 加單 bridge；t=1 全部接回出口。
本頁的兩列／四接點負控制仍有效，未將兩列條件誤升為三列。

2026-09-28。接手 HEAD `2de13f7`，沿用工作樹中的
[residual 局部性成果](c5_single_spoke_residual_locality.md)；優先序見
[HANDOFF](HANDOFF.md)。本輪不改 (2,2) 的來源或 target 計數。

**在 single-spoke 必要覆蓋的來源前提下，(3,1) 不可能。**
三接點分量的兩個禁色強迫一個 active triangle 及三條同 parity 的 bridge
arms。三個 triangle 頂點各有一條原 boundary tether，唯一 spoke 足以把
五個 branch sets 接成 K5。此結論不需 T4 acceptance 或第二列拒絕。

這是 [two-spoke 三接點證明](c5_two_spoke_three_contacts.md) 的明確適用範圍
擴充：其差異樹僅使用三個接點與兩個禁色；最後 hub 鄰接只需一條 spoke。
下文重新核對 degree、旁支與另一原分量，沒有套用二接點路徑定理。
證據為任意大小紙面證明＋外部 degree-list 定理＋Python 局部／minor 控制；
未新增 Lean theorem。

## 1. 來源、兩份完整 lists 及不可刪減覆蓋

G 有限簡單，B=(b0,…,b4) 是 induced-C5 disk 外框，有效內部 H 連通。
G 是 q=01012 的 edge-minimal obstruction；唯一完整 degree-5 點 z 的
boundary 鄰居恰為 b_s，其餘有效內點完整 degree=4。H−z 有 C、D 兩個
分量，原有序接點分別為 P=(u0,u1,u2)、(w)，四點互異。
每個分量的全部實際 boundary 附件、bridges 與嵌入次序均保留。

令 U={0,1,2,3}、A=U\{q_s}。完整關係 R_C(q) 是同一 C coloring 在
三個具名接點的 tuple 集，F_C(q)=⋂_{t∈R_C(q)} set(t)；D 亦同。
[不可刪減覆蓋](c5_single_spoke_cores.md#2-四種不可刪減覆蓋任意大小結論)
給出某 c∈A，使 F_D(q)={c}、F_C(q)=A\{c}={a,b}，a≠b。
不是把三個接點的 marginals 分別指定顏色。

對 d=a,b，定義同一原分量上的拒絕 lists

\[
M_d(v)=U\setminus\bigl(q(N_B(v))\cup(\{d\}\text{ if }v\in P\text{ else }\varnothing)\bigr).
\]

由完整 degree=4，有 |M_d(v)|≥deg_C(v)；不可著色及連通 slack-list
貪婪引理使處處等號。每點的外鄰顏色因此互異；接點的 boundary 色同時
避開 a、b。令 e_d 是色 d 的指標向量，則

\[
\mathbf1_{M_a(v)}-\mathbf1_{M_b(v)}=\mathbf1_{v\in P}(e_b-e_a). \tag{1}
\]

外部 [Dvořák 講義 Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
給 C 的 Gallai 結構及兩份 blockwise-uniform palettes，本輪已重讀核對。
每點的 incident block palettes 不交且聯集恰是 list。由既有
[連通外框 K4 引理](c5_degree5_tree_components.md#1-連通外框排除-degree-4-分量的-k4)，
B∪{z} 經唯一 spoke 連通，故 C 沒有 K4 block；planarity 排除更大 clique。
所以只有 bridge（palette 大小一）與 odd cycle（palette 大小二）。

## 2. 三個葉點迫使唯一 triangle 加三臂

記兩份 palettes 為 S_K^a、S_K^b。C 的 vertex–block incidence matrix
各欄線性獨立：leaf block 的 private vertex 決定該欄係數，從共享 cut
vertex 方程扣掉後移除該 block，有限歸納直到最後一個 block。

把 (1) 逐色相加，欄獨立性給每個 block：a、b 以外的 membership 完全
相同，a、b 的差值相反。因此 palette 或保持不變，或恰交換 a、b。
稱後者為 active；其 sign 為 1_{b∈S_K^a}−1_{b∈S_K^b}∈{−1,+1}。

在同一頂點，同份 palettes 互斥，故正、負 active blocks 至多各一個。
式 (1) 進一步給：

- 原接點恰 incident 一個 active block，sign=+1。
- 其他點 incident 零個或兩個 active blocks；兩個時 signs 相反。

取全部 active blocks 及其全部頂點的 incidence forest。每個 block-node
degree 為 |V(K)|≥2；vertex-node 的 degree 只有一或二，degree 一的點
恰是三個原接點。非空 tree 至少兩葉，所以這個 forest 只有一個分量。
樹的葉數公式

\[
3=2+\sum_{\deg(x)\ge3}(\deg(x)-2)
\]

迫使恰有一個 degree-3 block-node，其他 block-nodes 全 degree 二。
故 active 結構是**一個 triangle 與三條 bridge arms**，終點恰為原
u0、u1、u2。它亦是 incidence tree 中連接三接點的最小 subtree；
沒有 inactive block 能介入其路徑，也不能有額外的無接點 active 分支。

令 triangle 頂點 vi 的 arm 通往 ui，長度 ℓi 計原 bridges；允許 ℓi=0，
此時 vi=ui。三條臂在 triangle 外互不相交，沿臂 sign 每步反轉，終點
sign 皆 +1，所以 ℓ0、ℓ1、ℓ2 同 parity。triangle palette 的另一色
h 屬於 U\{a,b}。不限制臂長、旁支數、旁支深度或非 active odd cycles。

## 3. 每個 triangle 頂點的實際 boundary tether

vi 已有兩條 triangle 邊；若 ℓi>0，再有第一條 arm 邊；若 ℓi=0，再有
原接點邊 zvi。完整 degree=4 留下**恰一條**其他邊。

該邊或直達 B，或為 viwi 進入 C 的 inactive 旁支 Wi。後者是 bridge：
另一個 cycle block 會再佔至少兩條 incident edges，超過 degree。
它不可能再接 z，因三個原接點在 active 結構上已全部用完；也不可能
接 D，因 C、D 是 H−z 的不同分量。Wi 不含接點，且不能回接 active
結構的其他點，否則違反 block incidence tree 無環。三個 Wi 互不相交。

**Wi 必有 boundary 鄰居。** 若沒有，它也沒有 z 鄰居。C−Wi 仍連通，
lists M_a 不變，而 vi 的 degree 減一，故 slack-list 貪婪法可著色。
Wi 的 wi 在 Wi 內 degree=3，其餘點 degree=4，以全 U lists 再用同一
貪婪法著色；Wi 沒有 boundary／z 限制，可整體置換四色，使 wi 避開
已著色的 vi。拼回得到 C 的 M_a-coloring，與拒絕矛盾。

故可在每個 Wi 選一條到實際 boundary 附件的簡單路徑，接上 viwi 得
tether Ti；直達 B 是長度一的情形。三條 tethers 內部互不相交，並避開
triangle、arms、z 與 D；boundary 終點可以相同。這些路徑全部在原圖中，
未指定新的接線，也沒有收縮旁支來改寫原完整關係。

## 4. 只有一條 spoke 的五個原圖 branch sets

取

\[
Z=\{z\},\qquad V_i=\{\text{vi 至 ui 的原 arm 上全部頂點}\},\qquad
O=B\cup\bigcup_{i=0}^2\bigl(V(T_i)\setminus\{v_i\}\bigr).
\]

五組非空、連通且互不相交；O 經原 C5 連通，即使三個 tether 終點相同
也成立。十條鄰接分別來自：

| branch-set pair | 原圖 witness |
| --- | --- |
| Vi–Vj，i≠j | 三條 triangle 邊 |
| Z–Vi | 三條原接點邊 zui |
| Vi–O | 三條 tether 的第一條邊 |
| Z–O | **唯一 spoke zb_s** |

故 G 含 K5 minor，與 planarity 矛盾。原單接點分量 D、zw 與 D 的全部
附件仍存在，只是不屬於此 minor 的 branch sets。沒有將 D 合併進 C，
也未把三接點換成二接點。本構造僅作非平面性反證，不宣稱保持完整 Σ
的 boundary 固定壓縮。

因此 single-spoke (3,1) minimal q-core 不存在，對五個 s 及三種 c 全部
成立；不需支援型枚舉、T4、p₁／p₂ 拒絕或任何來源大小界。

## 5. 重播證書與證據界線

[checker](../scripts/c5_single_spoke_three_one.py) 與
[artifact](../artifacts/c5_single_spoke_three_one/observations.json) 保存：

- 五個具名 spoke 位置的 15 個不可刪減覆蓋，356 個 tight 接線局部型；
  反射同時搬運 boundary index、色框與 lists，保留原接點身份。
- 十二個有序禁色對的 792 個 palette incidence 型：接點一個 active
  block，非接點零或兩個，保留完整 palettes 的互斥與兩列共同色框。
- 512 個 arm parity 控制；任意長度由 §2 歸納承擔。
- 800 份只有一條 spoke 的 K5 skeletons，涵蓋五個 s、八種零臂模式、
  odd arms、直接／細分 tethers、不同／相同 boundary 終點；每份列出
  原邊、具名三接點與第四接點、實際路徑、branch sets 及十條鄰接。
  另逐份驗證 boundary 反射，共 800 份搬運控制。
- 8 個負控制：缺 spoke、原接點邊、triangle 邊、tether，hub 不連通、
  branch sets 重疊、捏造頂點，以及四接點可有兩個 active 分量的界線。

證書以 SHA256 綁定沿用的 two-spoke 三接點及 single-spoke 覆蓋輸入；
不覆寫前序 artifacts。skeletons 省略未用邊，**不是完整 degree/list
來源、disk 實現或任意大小 cover**。任意大小結論由 §§1–4 紙面證明及
外部 degree-list 定理承擔。原 (2,2) 的 278 排除／102 雙列結果未重算改表。

```bash
python3 scripts/c5_single_spoke_three_one.py --check
python3 scripts/c5_two_spoke_three_contacts.py --check
python3 scripts/c5_single_spoke_cores.py --check
python3 scripts/c5_single_spoke_residual_locality.py --check
python3 scripts/c5_single_spoke_first_bridge.py --check
python3 scripts/c5_single_spoke_two_two.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

無參數只生成新層；`--check` 重算並逐 byte 比對。實際執行及未重播範圍見
[當輪紀錄](history/2026-09-28-three-one.md)。`lake build` 不驗證上述新紙面證明。

## 6. 精確停止點

[單側出口](c5_single_sided_exit.md) 失敗側唯一 degree-5 的核心，現在只剩
t=0 的六種必要分拆，以及 t=1 的 **(4)**；(3,1) 是來源不存在，不是
多算一批指定 p 的接受查詢。一般核心存在／分離、共同出口與主命題仍未證。

下一窄入口：(4) 的單一原分量 C，有四個原有序接點及 F_C(q)=A 三禁色。
比較三份拒絕 palettes：每兩份的 active forest 有四葉，不能沿用三葉
連通結論。K4-free 下，它可為兩條分離 bridge 路徑，或兩個 triangle
branch nodes 的連通樹；兩 triangle 可以共用 cut vertex，該點可能沒有
剩餘 boundary tether 邊。須在**同一 block incidence tree**上同時滿足
三組差異、保留全部附件，先限制三組 forest 的共同結構，才談原圖 minor。
不把每對比較各自可行當作同一來源可行，也不開始任意大小圖枚舉。
