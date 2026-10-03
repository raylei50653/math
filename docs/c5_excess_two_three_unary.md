# ε=2：三 spokes／三原 unary 的共同扇區排除

**後續（2026-10-02）**：[t=3、(2,1) 原 binary 省略排除](c5_excess_two_binary_omission.md)
已完成本輪留下的下一窄題；該型所有容量二省略均全收，無全 degree-4
真子核心。其餘 ε=2 及一般來源仍保留，下文維持當輪證據與範圍。

**後續（2026-10-03）**：[t=3 全分拆排除](c5_excess_two_three_spoke_complete.md)
已完成 (2,1)、(3) 的整型來源排除；本頁 (1,1,1) 結果亦由較強
短支援引理的三份固定支援六跨度直接得到。原證書保持。

2026-10-02，基準 `bbd900a`，接續
[t=3 triangle 位置](c5_excess_two_three_spoke_unary.md)留下的 path／tail 分支。
目前停止點見 [Kempe 導覽](c5_kempe_guide.md)，本輪驗證見
[研究紀錄](history/2026-10-02-excess-two-three-unary.md)。

**結論：933／941 的固定完整 Σ、edge-minimal C₅ disk 來源，在 ε=2、
唯一 degree-6 root r 且 t=3 時，不可能有三份原 unary 分量。**
因此前輪的 spoke＋unary 省略核心中，r 位於 path／tail 的分支排除；
連同既有 triangle 位置，完成 t=3 的 spoke＋unary 省略分支。
新結論本身不需先指定一份省略核心。

證據是任意大小紙面必要化約及有限集合證書，沒有來源圖枚舉、路徑縮減
或新 Lean theorem。共同下界仍為 ε≥2，沒有排除其餘 ε=2 或一般來源。

## 1. 原分量、十列與精確接合

G 有限簡單，B=(b₀,…,b₄) 是指定有序 induced-C₅ disk 外框，Σ(G) 是
933、941 或其整圖 D₅ 像，故接受全部 T4。每條非框邊 e 都滿足
Σ(G−e)⊋Σ(G)。有效內部 H 連通；r 的完整 degree 為六，其他內點
完整 degree 為四；r 的三條具名 spokes 端點為 s₀<s₁<s₂。
本輪假設 H−r 恰有三個原連通分量 U₁、U₂、V，各與 r 恰接一條邊，
原接點依序為 x、y、v。全部原附件、ownership、內部邊與嵌入保持。

固定任一 proper boundary coloring b，原一接點完整 relation 記作
S₁(b)、S₂(b)、S₃(b)。[Unary slack 引理](c5_excess_two_spoke_unary.md#2-原-v-的-relation-非空不需分類其大小或支援)
使各 Sᵢ 非空。原四接點關係恰為

\[
\mathcal R_G(b;r,x,y,v)=
\{(a,c_1,c_2,c_3):c_i\in S_i(b),\quad
a\notin\{b_{s_0},b_{s_1},b_{s_2},c_1,c_2,c_3\}\}. \tag{1}
\]

每個 tuple 分別選同一 b 下三份原分量的完整染色，再檢查原 root 邊；
分量間沒有邊，所以可以拼接。令 Fᵢ(b)=Sᵢ(b)（若 |Sᵢ|=1），否則
Fᵢ(b)=∅。式 (1) 的 root 投影就是四色扣掉三個 spoke 色及全部 Fᵢ。
此投影只用於這個接合判定，不把 Fᵢ 宣稱為完整 Sᵢ 的替代 state。

六個因子的固定次序是三條原 spokes、U₁、U₂、V。所有 singleton 列
共用 D=3 為未用色；D₅ 搬運作用於整張圖，不逐分量正規化。

## 2. 四容量子覆蓋與省略身份

任一拒絕列中，六個空／singleton 因子覆蓋四色，故可以各色取一個
因子，留下恰四個因子。另兩個因子構成具名省略 pair P。
省略 unary 是刪除整份原分量及其 incident 邊；不是縮成自由端點。

令 K_P 為省略 pair 後的原圖子圖。它的有效內部連通、所有內點完整
degree 四，且仍有至少一份 unary。若拒絕某列，任取 minimal core，
degree-4 飽和沿內部傳播迫 core 等於整張 K_P。
[全 degree-4 分類](c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論)給：

1. **同一 P 最多屬於一個拒絕 singleton 列。** K_P 的完整 Σ 只缺該列。
2. **P 不能是兩條 spokes。** 此時 r 在 K_P 仍有三條通往不同原分量的
   bridges，且不在 cycle 上；分類中非 cycle 內點的內部 degree 至多二。

每列須保存所有可省略 pairs，不能只挑一個方便的 pair。不同拒絕列的
pair 集必互斥。這裡直接在全 unary 前提下證明第二項，不依賴先前的
有限雙 spoke 接回表。

## 3. 三份原分量的固定支援下界

### 3.1 每份原 unary 都有至少兩個實際框鄰點

固定 C 及原邊 rc。完整 Σ edge-minimality 給一個原 G 拒絕、G−rc
接受的列 q。刪 rc 後 C 由 slack 引理可染色，故其因子在 q 的覆蓋中
有私有色，且 F_C(q) 非空。任何四因子子覆蓋都保留 C；取一份後，
上一節給全 degree-4 minimal core K。**C 及其全部原附件在 K 中完整保留**，
所以 C 是 K₄-free Gallai tree（沿用既有 degree-4 分類及 degree-list 證據）。

若 C 無框附件，其 relation 在 S₄ 下不變，不能有 singleton F_C。
若全部附件只到 b_j，記 q(b_j)=a。固定 a 的色置換迫 F_C={a}。
再固定 r=a，拒絕的 degree lists 處處 tight；每個 C 點至多有一個
C 外鄰居，否則同色外鄰居使 list 有 slack。因此每點 deg_C≥3。
但非平凡 K₄-free Gallai tree 的末端 block 有內部 degree≤2 的非割點，
singleton C 也不可能，矛盾。

這是[既有單點支援排除](c5_no_spoke_supports.md#2-每份支援至少兩點且有環狀區塊次序)
在本輪前提下的重新接合；沒有把原 degree-5／單列 minimality 直接套上 G。
故每份原支援 S_C=N_B(C) 的共同 lift 都有跨度 ℓ_C≥1。

### 3.2 D 身份與額外一段跨度

沿用[單接點 D 守恆](c5_excess_one_subcovers.md#4-單接點分量的跨列-d-身份不能互換)：
同一 C 在兩個 singleton 列都有非空 F 時，禁色是否等於 D 必相同。
它由同一 block-cut tree 的固定色 membership 歸納得到；非空 F 的拒絕
degree lists 提供所需證書，不要求整張 G 在任一列 minimal。

定義 d_C=1 當且僅當五個 singleton 列中某列 F_C={D}，否則 d_C=0。
因此在每個 singleton 列，d=1 的 F 只可是 ∅／{D}，d=0 的 F 只可是
∅／{0}／{1}／{2}。若 d=1，該份原實際支援在見證列必看見全部三個
boundary 色，否則交換 D 與未見色破壞 singleton。因此

\[
\ell_C\ge 1+d_C. \tag{2}
\]

各 d_C 的見證列可以不同。式 (2) 是對**固定原支援**的幾何下界，
下一節只在同一嵌入的三份互異分量上相加；沒有把跨列染色、兩份 core
或重複使用的原分量當作互不相交物件。

## 4. 三條原 spokes 的共同扇區

三條 spokes 把 disk 分成三個扇區 J₀、J₁、J₂。每個 J_k 的 boundary
弧包含兩端原 spoke 框點，長度 L_k>0，且 ΣL_k=5。
每份 C 連通且不能穿過 spokes，故它全部實際支援落在同一閉扇區弧。
共享 spoke 端點允許，但不把端點當成兩個不同框點。

沿用[同一 root 的相容 lifts](c5_independent_support_capacity.md#42-同一-root-的相容-lifts)：
在每個扇區，按原 root 邊的次序取各分量支援的第一至最後附件，
得到開框邊段互斥的 lifts。三條原 spokes 是固定切口，故

\[
\sum_{C:\,a_C=k}(1+d_C)\le L_k\qquad(k=0,1,2). \tag{3}
\]

這是同一原嵌入的必要式。Checker 為了放寬計算，只使用
S_C⊆J_{a_C}，不把整條 J 弧新增為實際附件。對任一 singleton 列 q：

- d_C=1 時，若 q(J_{a_C}) 未見全部三色，F_C 必空。
- d_C=0 且 F_C={a} 時，a 必屬 q(J_{a_C})；否則 a 和 D 都未見於
  原支援，交換兩色會破壞 singleton。

允許不同列獨立選取符合這些限制的 F，是擴大的必要域；不宣稱它們
有同一原圖實現。若此域已空，真實來源亦不可能。

## 5. 固定小域與結果

[Checker](../scripts/c5_excess_two_three_unary.py)及
[證書](../artifacts/c5_excess_two_three_unary/observations.json)直接列出三條
spokes 的十種具名位置、三份原 unary 的八種 D 身份及兩候選各五個 D₅ 像。
沒有圖生成器。每列列出所有合法空／singleton F，計算**全部**省略 pairs；
逐列動態規劃保留已用 pair 集，只有互斥者才能接上。
狀態合併只用於此必要條件：未來限制僅依賴已用 pair 集，保存一份代表
見證足夠，並非合併實際來源關係。

| 必要域結果 | 933 五像 | 941 五像 |
| --- | ---: | ---: |
| (spokes, D 身份, target) 比較 | 400 | 400 |
| 僅省略共享／D 守恆後存活的具名 cases | 45 | 180 |
| 上述 cases 的終端 pair 集總數 | 180 | 2,070 |
| 無任何符合式 (3) 的扇區配置 | 45 | 75 |
| 剩餘 cases 的具名扇區配置比較 | 0 | 450 |
| 再加扇區見色限制後剩餘 | 0 | 0 |

933 的 45 cases 均有兩份 D carrier，但原 spokes 只有 (1,1,3) 扇區長度，
放不下兩段跨度二。941 的 180 cases 包含 60 份一個 D 身份及 120 份
兩個 D 身份；不能一律假設有兩份 D carrier。剩下 105 cases 的 450 份
扇區配置逐列套上原見色限制後，均沒有互斥的省略 pair 序列。

原始 80 份 spokes／D 身份的式 (3) 配置共 365 份；證書保留全部配置，
以及所有 225 份抽象存活 cases 的具名 witness、每層可達 pair 集與幾何
細化結果。計數是必要集合狀態，並非來源圖數或 disk 實現數。
另對全部 15³ 份非空 unary relation 三元組及十種 spoke 色集合，
直接核對 33,750 份完整 (r,x,y,v) tuples 與式 (1) 的 root 投影。
這是局部代數控制；實際原分量的完整染色存在性由紙面接合承擔。

## 6. 接回交接缺口與驗證界線

原 t=3 spoke＋unary 省略核心若 r 位於 path／tail，r 的兩個內部
neighbors 位於兩份不同原 unary U₁、U₂；加上省略的原 V 正是本輪
三-unary 前提，故排除。若 r 在 triangle 上則由
[前輪結果](c5_excess_two_three_spoke_unary.md)排除。
所以候選唯一 degree-6、t=3 前提下，對每一份原 unary V 和每條原 spoke e，

\[
\boxed{\Sigma(G-V-e)=\Omega.}
\]

這不是整份 ε=2 分類。省略兩 unary／一 binary、無全 degree-4 真子核心、
其他 spoke 數、兩個 degree-5 roots（含 mixed）均保留；新結果未提高 ε≥2，
也未證一般候選排除、共同出口或 K∞=K≤5。

```bash
python3 scripts/c5_excess_two_three_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_three_unary.py --check
python3 scripts/c5_single_spoke_root_conservation.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

本輪新重播範圍與實際輸出見研究紀錄。degree-4 分類、外部 degree-list
與既有拓撲證據按上述報告沿用，未重跑其全部模板全集；`lake build`
不把新紙面拓撲或 Python 空域證書提升為 Lean theorem。
