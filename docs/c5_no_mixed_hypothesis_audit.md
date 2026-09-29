# No-mixed 三假設驗證：完整搬運、單框點化約與守恆禁色

2026-09-29，基準 `0ab88ce`。依使用者要求由三個 agent 分別驗證，主 agent
審閱證明、整合 checker 並重播。沿用[十五類總覽](c5_no_mixed_span_budget.md)
的圖類、任意大小必要支援覆蓋及原路徑引理；不重新枚舉來源圖。

**結果：完整搬運給出可直接證明的充分條件；單框點化約將未知原分量關係
減至至多兩份；守恆 singleton 不升為 target pair 有七類表依賴證書。**
尚未得到取代分類的共同延拓證明。全部 4,164 個 target 原已接受，本輪
沒有新增 source 排除或 target 接受。必要支援不是 disk 實現證書。

目前停止點與後續入口見 [weak-deletion 導覽](c5_weak_deletion_guide.md)。
本輪實際檢查及未重跑範圍見[驗證紀錄](history/2026-09-29-no-mixed-hypothesis-audit.md)。

## 1. 同一來源與三項問題

除 §2 的一般搬運引理外，完整沿用總覽 §1：M 有限簡單、B 為 induced C5
disk 外框、H=M−B 非空連通；q=01012 是非框邊 edge-minimal obstruction。
恰有相鄰 z,w 完整 degree=5，其餘內點完整 degree=4；H−{z,w} 每個原分量
C 恰接一個 root。U={0,1,2,3}，p₁=01021、p₂=01212。

S_C 是 actual boundary support；T_C(β) 是原 C 的完整有序接點關係，
F_C(β)=⋂_{τ∈T_C(β)}set(τ)。保留所有原接點、bridges、旁支、spokes、zw、
環序及共同字面色框。T_C 非空，source E_z(q)=E_w(q)={c}。
「飽和」仍專指二接點分量的 |F_C(q)|=2。

三項待驗證內容分別是：共同 source 色的完整搬運是否充分、單框點是否
真能集中未知關係，以及奇數 bridge palettes 換色是否必遭幾何阻斷。
下文區分一般紙面引理、沿用支援覆蓋的化約及依表判定的推論。

## 2. 完整搬運的充分條件，以及較弱版本

定義

\[
\Pi_C(q,p)=\{\pi\in S_U:\pi(q_i)=p_i\text{ for every }i\in S_C\},
\quad K_C(c)=\{\pi(c):\pi\in\Pi_C(q,p)\},
\]
\[
H_r(p)=\bigl(U\setminus p(N_B(r))\bigr)\cap\bigcap_{C\sim r}K_C(c).
\]

**引理。** H_r(p)⊆E_r(p)。若 H_z、H_w 有不同顏色 a_z、a_w，則 p 延拓。
此引理只需 no-mixed 與 M−zw 有 roots 同色 c 的 q 染色；不需要 disk、
degree、缺額或飽和前提。

**證明。** 固定一份 M−zw 的完整 q 染色 f。每個原 C∼r 選擇
π_C∈Π_C 使 π_C(c)=a_r，對 C 的全部頂點施 π_C；boundary 設為字面 p，
root r 設 a_r。分量內邊由置換保持 proper，C–B 邊由所有 actual support
上的對齊保持，C–r 邊由原接點全部避開 c 保持；root-spokes 由 H_r 定義
處理。a_z≠a_w 可接回原 zw。沒有跨分量邊或 mixed 分量，故全部原邊
均 proper。這也逐側證明 H_r⊆E_r。

各 π_C 只作用在原分量內部，所有附件仍對齊同一 p 與 a_r；沒有獨立
重命名 shared frame。完整 tuples 與中間路徑並未投影或刪去。

Π_C 非空恰等於 q、p 在 S_C 上具有相同的等色分割。令 φ_C 為支援給的
部分單射 q_i↦p_i，則 c 已見時 K_C={φ_C(c)}，否則 K_C=U∖p(S_C)。
這可只用 actual support 與 c 檢查，不需先知道 target relations。

**較弱的 G 判準。** 允許各原分量使用不同 source root preimage：

\[
G_r(p)=\bigl(U\setminus p(N_B(r))\bigr)\cap
\bigcap_{C\sim r}\ \bigcup_{\pi\in\Pi_C(q,p)}\pi\bigl(U\setminus F_C(q)\bigr).
\]

有 H_r⊆G_r⊆E_r(p)；若每個 incident Π_C 非空，則 G_r=E_r(p)。因為
完整搬運給 T_C(p)=πT_C(q)、F_C(p)=πF_C(q)，其像不依相容 π 的選擇。
G 的每個 local witness 都來自同一原 C；不同 C 的 source preimages
不必組成一份 source 整圖染色，但搬運後均避開同一 target root 色，
故 no-mixed 接合仍合法。不得把它說成搬運單一 M−zw 染色。

| 類型 | 查詢 | H 通過 | G 通過／全部分量可搬運 | 有不可搬運分量 |
| --- | ---: | ---: | ---: | ---: |
| AA | 644 | 364 | 364 | 280 |
| AB | 1,120 | 724 | 724 | 396 |
| AC | 48 | 20 | 24 | 24 |
| AE | 240 | 216 | 216 | 24 |
| BB | 1,776 | 1,296 | 1,296 | 480 |
| BC | 48 | 24 | 24 | 24 |
| BE | 288 | 288 | 288 | 0 |
| 合計 | 4,164 | 2,932 | 2,936 | 1,228 |

H 比 G 嚴格的四項是 AC80/p₂、98/p₂、279/p₁、290/p₁。例如 AC80/p₂
有 c=0、B_z={1,4}、B_w=∅，三份 (support,F_C(q)) 依序為
(014,{3})、(123,{2,3})、(34,{1})。H_z={0}、H_w=∅，但
G_z=E_z={0}、G_w=E_w={2}。Cw 可把 source 0 送到 target 2；Dw 可把
source 2 保持為 target 2。要求兩份都從 c=0 出發才造成漏失。
這是必要資料上的判準嚴格性控制，不是來源實現證書。

[搬運 checker](../scripts/c5_no_mixed_hypothesis_transport.py) 與
[逐查詢資料](../artifacts/c5_no_mixed_hypothesis_audit/transport.json)
保留 input SHA、具名支援、相容置換、H/G、完整搬運後的 root 關係；
另核對全部 32 支援子集、兩 target、四色 c 的 256 個等色分割控制。

## 3. 單框點化約與精確共同介面

對 p₁ 取 σ=(1 2)，則 σ(q)=02021，只需在 h=b₁ 把 2 改為 1；
對 p₂ 取 σ=id，只需在 h=b₂ 把 0 改為 2。令
A_h={C:h∈S_C}。若 C∉A_h，則 T_C(p)=σT_C(q)、F_C(p)=σF_C(q)。
因此不能以任何色置換搬運的分量集合 D_p⊆A_h。

**引理。** 在既有共同同序、正跨度且框邊內部不交的支援 lifts 下，
|A_h|≤2；若有兩份，其 hull 分別在 h 的相反方向終止／開始。

**證明。** 每份含 h 的正跨度 hull 至少占用 h 的一條相鄰框邊；h 在
hull 內部時兩條都占用。不同 hull 的框邊內部不交，h 只有兩條相鄰
框邊，故至多兩份；兩份時 h 必為兩個不同方向的端點。稀疏支援中的
空白框點不解除 hull 所占框邊。Cyclic cut 的 0、5 是同一框點的左右
lifts，未複製身份或顏色。每份跨度<5，由另一份正跨度分量保證。

此論證沿用[共同支援引理](c5_no_mixed_span_budget.md#21-同序支援與兩側框弧)，
不能改用彼此不相容的最短 hull；若容許零跨度分量或 root 樹的多區段，
必須另證前提。Root-spokes 的零跨度不計入 A_h，但接合時全部保留。

固定的是其它完整關係，不是一份 source 染色。精確介面為

\[
B_r(p)=p(N_B(r))\cup\bigcup_{C\sim r,\ C\notin A_h}\sigma F_C(q),
\quad E_r(p)=U\setminus\left(B_r(p)\cup\bigcup_{C\sim r,\ C\in A_h}F_C(p)\right).
\]

原圖延拓恰等於 (E_z×E_w)∖Δ 非空。至多兩份未知 F 必由各自完整原關係
計算；外部原分量仍可能供應必要的幾何路徑，不能從證據中刪除。

也可在原 lists 上表述這一變動。令 a=σ(q)_h、b=p_h；固定 root 色 t，
D_v(t) 收集除 h 外的實際 boundary 禁色及存在時的 root 禁色 t。
原 h 鄰點的舊、新 lists 分別是 U∖(D_v(t)∪{a})、U∖(D_v(t)∪{b})；
其他頂點不變。不能無條件用 (L_old∪{a})∖{b}，因其他外鄰可能仍禁 a。
每份分量可含任意多個 h 鄰點，這不是有限頂點 repair。

| 分量數 | 0 | 1 | 2 |
| --- | ---: | ---: | ---: |
| 不可色置換搬運 | 2,936 | 1,184 | 44 |
| Actual support 含 h | 152 | 1,736 | 2,276 |

44 份雙不可搬運查詢分 AA24、AB12、AC8，均接不同 roots；這裡只是表中
統計。2,276 份雙含 h 查詢則有 **880 同 root、1,396 不同 roots**，
不能把一般介面預設成每側一份。

[單框點 checker](../scripts/c5_no_mixed_hypothesis_anchor.py) 與
[逐查詢資料](../artifacts/c5_no_mixed_hypothesis_audit/anchor.json)
獨立解析分量／spokes，核對 2,082 份保存 placements、1,820 個三弧與
50 個不交雙弧控制，並逐候選核對完整式、anchor 式與 D_p 式相等。
容量／穩定子上界仍有 434 個失敗 joins（AA160、AB146、AC8、BB120），
原後續證書已排除它們；局部化本身尚不提供共同 repair 定理。

## 4. 守恆 singleton 的 target pair：表依賴結果

固定缺額二接點原 C，F_C(q)={d}，並令
K={a:∀i∈S_C，q_i=a iff p_i=a}。本節假設 d∈K；不把 AB22/p₂ 的
非守恆 d=2 偷換成守恆色。反設 F_C(p)=D 是二元集。

沿用[原路徑與 palette 引理](c5_adjacent_degree5_no_mixed_t2_path_palettes.md)：
target pair 給奇數長原 bridge 路徑 P；刪 P 的邊所得 W_j 保留全部
旁支與 actual support。局部 residual L_j 尚未扣 root 色，p 下為 D。
q 的端點 residual 含 d，固定色歸納給 L_j(q)∩K=D∩K，因此 d∉D
立即矛盾。這是同一 W_j 的 residual 限制，不是假設 F_C 跨列不變。

d∈D 時，q 下 bridge palettes 為 β₁,d,β₃,d,…,β_ℓ。
每條奇數 bridge 的兩端共用 residual {d,β}。枚舉所有必要 β 及其
實際支援族，再使用同一原外部路徑／固定三框弧引理，逐 β 排除：

| 計數單位：支援 record × target × 具名分量 × target pair D | 數量 |
| --- | ---: |
| d 守恆的 pair 候選總數 | 1,780 |
| d∉D，固定色端點條件排除 | 890 |
| d∈D，原三弧規則排除全部 β | 850 |
| d∈D，只剩一個 β | 40 |
| d∈D，仍剩至少兩個 β | 0 |

只剩 β=b 時，每條奇數邊都用 b，偶數邊用 d；交換整條原 P 的 d,b
palettes，保留所有旁支，可重建 b∈F_C(q)，與 singleton 矛盾。
所以既有七類必要覆蓋加上原路徑引理及此證書，給**表依賴的守恆
singleton 不升 pair 推論**。這不需要先假定整圖 p 拒絕。

其中 776 個 d∈D 候選曾出現在有合法 root 色對的上界 join，142 個曾
出現在失敗 join，兩者有 28 個重疊；它們不是互斥類別。排除有 root
色對的候選是在收緊局部上界，不能記作新增 target 接受或 source 排除。

另加同一 W 的完整支援色置換相容性：若 π 在 W 的全部支援 T 上
對齊 q、p，則 π({d,β})=D。這由 direct attachments 與 rooted branch
palettes 的唯一性得到。若無相容 π，不添加此限制。加入後有 886 個
d∈D 候選零 β、4 個單 β；最後四個正是 AA54/p₁、68/p₂、173/p₂、256/p₁。
較強篩選不是上面 850+40 證明的必要前提。

因此原先「palette 換色必迫 K5」的免分類猜想仍未證。本輪取得的是
**逐支援排除其它 β，再作全路徑交換**。抽象 Gallai 控制仍可有
bridge word (2,3,1)、source d=3、完整禁色僅 {3}；這否定純 palette
代數足以強迫 β 一致，但不是 induced-C5 disk 來源反例。

[Palette checker](../scripts/c5_no_mixed_hypothesis_palettes.py) 與
[逐候選證書](../artifacts/c5_no_mixed_hypothesis_audit/palettes.json)
保存全部 1,780 個候選、原 context、逐 β 支援族、原外部路徑／固定框弧
的一份具名見證，以及全部替代見證的數量／hash、imported scripts SHA。
重播仍計算全部替代見證；不納入未完成的額外探索。

## 5. 可用結論、剩餘問題與重播

可直接重用的是 H/G 搬運引理與單框點 exact reduction；守恆不升 pair
目前仍靠既有七類的必要覆蓋與逐支援證書。下一個窄問題是：固定外部
完整關係後，對 A_h 的一份或兩份原分量，是否能用不查表的局部相容
規則統一處理守恆與非守恆禁色。AB22 非守恆端點及 AA54 全路徑交換
仍是必要控制；外部原路徑不因未知關係減少而可刪去。

```bash
python3 scripts/c5_no_mixed_hypothesis_transport.py --check
python3 scripts/c5_no_mixed_hypothesis_anchor.py --check
python3 scripts/c5_no_mixed_hypothesis_palettes.py --check
PYTHONHASHSEED=17 python3 scripts/c5_no_mixed_hypothesis_transport.py --check
PYTHONHASHSEED=17 python3 scripts/c5_no_mixed_hypothesis_anchor.py --check
PYTHONHASHSEED=17 python3 scripts/c5_no_mixed_hypothesis_palettes.py --check
```

無 `--check` 只生成本輪對應 JSON；不覆寫既有十五類資料。
證據層：§2 初等紙面證明；§3 依既有拓撲引理的任意大小紙面化約；
§4 沿用外部 degree-list／Gallai 定理及原路徑證明，再以 Python 核對
固定支援域。未新增 Lean theorem；lake build 不形式化這些論證。
未證必要資料可實現、一般共同出口或 K∞=K≤5。
