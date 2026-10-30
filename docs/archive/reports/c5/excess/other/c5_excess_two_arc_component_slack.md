---
docgraph:
  id: c5.excess-two-arc-component-slack
  family: [c5, c5.excess-two, c5.arc2]
  derives_from:
    - c5.excess-two-arc-pair-critical
  requires:
    - c5.excess-two-nonadjacent-unit-core45
  related:
    - c5.excess-two-n2-ll-cut
    - c5.excess-two-n2-bridge
---
# E-ARC2：原分量的共同重色限制與 N2 必留分量

**後續（2026-10-13，BASE 243a125）**：[N2-BRIDGE](../n2/c5_excess_two_n2_bridge.md)
以五列slack與完整分量刪除witness另橋接932，排原E4三列完整來源契約的廣義N2。
E-ARC2仍剩N1及相鄰roots來源，均保持OPEN；本頁原前提、證明與當輪停止點保留。

2026-10-11，接續工作樹基準 `df60ef5` 及未提交的
[真子圖單拒絕定理](c5_excess_two_arc_pair_critical.md)。
目前入口及停止點見 [Kempe 導覽](../../../../guides/c5_kempe_guide.md#3-停止點與保留缺口)。
整理發布與本次重播範圍見[三點弧發布紀錄](../../../../../history/2026-10-11-three-point-arc-publish.md)。

**後續（2026-10-11）**：[末端block與N2真核心排除](c5_excess_two_arc_spoke_closure.md)
已接回剩餘root-spoke45／54；完整N2前提下每條非框邊刪除均全收，roots亦至多接
兩個相鄰框點，所有拒絕列只剩原55。三點弧仍OPEN；下文保留本輪證明與控制。

**三點弧命題仍未證成。** 本輪把逐點框色限制提升為同一原分量的共同限制：
同一 degree-4 分量內，不同點的框鄰居重色不能涉及兩個不同拒絕列。
再接既有核心排除，非相鄰、恰兩份 mixed 的 N2 來源中，
**每份原分量的每條 incident 邊都必對所有拒絕列 critical**；
每個非 root 內點至多接兩個相鄰框點，所有真 minimal cores 只能省一條原 root-spoke。
這是 N2 的必要結構，仍未排除其餘 spoke 省略或原55來源。

## 1. 前提、原座標與依賴

G、指定有序 induced-C₅ disk 外框 B、完整十列 Σ、T4 全收、Σ-criticality、
ε=2 均沿用上輪完整前提。目標來源經整圖共同搬運後，Σ=941、933 或940；
固定 q₀=`01212`、q₁=`01202`、q₃=`01021` 拒絕。940 隨全部原資料反射至933。
不把本結論接到原域以外的932。

原 roots 為 r,s，完整 degree 都五；其餘有效內點完整 degree 四。
C 始終是 **原 H−{r,s}** 的完整連通分量，保留原頂點、接點、root incidences、
框附件、bridges 及 rotation。令 E_C 為至少一端在 C 的全部原邊。
G−C 指刪除 C 的頂點；G−e 則保留原頂點座標，包括刪邊後的孤立點。

以下輸入均為既有已採納結論；本輪沒有重新稽核全部上游分類：

| 依賴 | 使用範圍 |
| --- | --- |
| [真子圖定理 P](c5_excess_two_arc_pair_critical.md#3-任意真子圖至多單拒絕) | 目標來源任意保 B 真子圖至多拒絕一列 |
| [分量解除定理](../../adjacent-degree5/c5_adjacent_degree5_interfaces.md#4-degree-4-的-tightness共鄰點與分量解除) | 只用原 C 每點完整 degree 四，任意字面 β、任意 root pins；不需 roots 相鄰 |
| [刪 root 與飽和](c5_excess_two_root_deletions.md#3-全部拒絕列至多一份-root-省略例外) | 省略 root 的 core 為原 unary 側、ε=0；所有此類 core 至多涉及一個拒絕列 |
| [兩-root44 已採納覆蓋](../../../../guides/c5_kempe_guide.md#3-停止點與保留缺口) | 固定完整Σ933／941或整圖像；保留單-root例外 |
| [N45-U 完整限定合成](c5_excess_two_nonadjacent_unit_core45.md#22-n45-u-ss-與指定整-u-身份的完整覆蓋) | 非相鄰、恰兩 mixed、X=G−U=M 自身同列 minimal、原 U 恰一 root incidence 的全部 §1 前提 |

新推導是紙面合成與初等 list slack。未增加外部定理；上游44及N45-U的
Gallai／紙面／finite-terminal信任鏈仍沿用。沒有新 Lean theorem。

## 2. 刪一條分量邊與整份省略的精確投影

令 U₄={0,1,2,3}。固定任何 proper β 及同一有序 pins (a,b)∈U₄²。
C 的 residual list 為

\[
 L(v)=U_4\setminus\{\text{v 的實際外部鄰居在 }\beta,a,b\text{ 下的色}\}.
\]

原完整 degree 四給 |L(v)|≥deg_C(v)。若某點的兩個實際外鄰同色，
該點有嚴格 slack。以它為根取生成樹，子點先於 parent 貪婪著色，
最後根使用多出的一色，即可補完整份 C。此論證包含 singleton C。

對 e∈E_C，若原 C 已可染就沿用；若不可染，每點 lists 都 tight，
所有外鄰色互異。刪外接邊新增一色；刪內邊則在 C−e 的每個連通分量
留下至少一個端點 slack，故均可補完。這重述既有分量解除的適用範圍，
不把它列為新的拓撲定理。

因此對完整外部座標 W=V(G)−C，有更明確的全染色等式：

\[
 \boxed{\pi_W\operatorname{Col}_\beta(G-e)
       =\operatorname{Col}_\beta(G-C)\qquad(e\in E_C).} \tag{1}
\]

任取右側一份完整染色，固定它的全部外部頂點，再用上述方法填 C；
故這不是只比較兩個 root 的 marginals。內部染色的數量及完整 fibre 可以不同，
式(1)只宣稱指定外部投影相等。特別地，

\[
 \Sigma(G-e)=\Sigma(G-C),\qquad Q(G-e)=Q(G-C). \tag{2}
\]

同一 C 的全部原 incident 邊有同一刪邊拒絕集，包含內部 bridge、框邊附件及 root 接線。
原 root-spokes 與 rs 不屬 E_C，不能併入這個等式。

## 3. 原分量的共同單列限制

對目標來源定義

\[
 D_C=\{i\in Q(G):\exists v\in C,\ \exists x\ne y\in N_B(v),\ q_i(x)=q_i(y)\}.
\]

**定理 1。** 每份原 C 滿足

\[
 \boxed{D_C\subseteq Q(G-C),\qquad |Q(G-C)|\le1.} \tag{3}
\]

*證明。* 若 i∈D_C，固定任意原 root pins 都有 boundary 重色 slack，
故 C 在 qᵢ 下接受所有16個 pins。若 G−C 有 qᵢ 染色，就能固定整份外部染色補回 C，
違反 qᵢ∈Q(G)。因此 i∈Q(G−C)。第二式由 P，因 C 非空且有原 incident 邊。∎

這會排除同一 C 的兩個不同點分別在不同拒絕列重色，強於只逐點使用上輪(C)。
canonical 三列的完整非相鄰框點對如下；相鄰框點在 proper row 永不同色。

| 同接的框點對 | 在指定拒絕三列中的重色位置 |
| --- | --- |
| 13 | 0 |
| 03 | 1 |
| 02、14 | 3 |
| 24 | 0、1 |

故24仍全面禁止；同一 C 內的13不能與03、02或14並存，03不能與02或14並存。
例如一個點同接012、另一個點同接123，即使兩點各自通過上輪逐點檢查，
只要它們在同一原 C，就分別造成 q₃、q₀ slack，已構成來源矛盾。
此結論不要求兩點相鄰，不限制 C 大小；跨兩份不同 C 不能這樣合併。

## 4. 接回45／54／55及單-root例外

保留上輪 Z(G) 的原定義：有 ε=0 minimal core 的拒絕位置。
在目標來源中，兩-root44已排，故 Z 只可能來自單-root原 unary 側，且 |Z|≤1。

**定理 2。** 若 C 是 mixed，或 C 是 unary 而其原 root incidence 至少二，則

\[
 \boxed{Q(G-C)\subseteq Z(G).} \tag{4}
\]

*證明。* 在 G−C 中任取一份被拒絕列的 minimal core K。
若 K 保留兩 roots，mixed 省略使兩 roots 的 degree 都至多四，
而 minimality 要求至少四，故它是已排除的兩-root44 core。
若 C 為 incidence≥2 的 unary，其 owner 在 G−C 中 degree≤3，不能保留於 K。
兩種情況皆迫 K 省略至少一個 root；它不能同時省兩個，
由刪 root 引理必為 ε=0 的原 unary 側，因此該列在 Z。∎

若 Z=∅，這些分量刪除均全收十列。由式(3)，它們任一點的框附件
不能包含表中任一非相鄰 pair。因此

\[
 \boxed{v\in C\quad\Longrightarrow\quad
 |N_B(v)|\le2,\quad |N_B(v)|=2\Rightarrow N_B(v)\in E(B).} \tag{5}
\]

這也排除其三-spoke葉。若 Z 非空，必保留例外列，不能直接使用(5)。
一般 unit unary 亦未被定理2涵蓋。

**45／54 的原身份。** 任一保兩 roots 的真 core 若是45／54，降度側恰少一個
原 incidence，高度側保留全部原 incident 邊。degree-4飽和使原分量全取或全不取，
故只可能省一條降度側 root-spoke，或整份原 incidence-one unary。
不可能省 mixed、rs、兩份 unary 或分量的一部分。若兩 roots 仍55，core就是G。
此身份化約不假定每個拒絕列都有真 core。

## 5. N2 的全分量必留推論

再假設 roots 非相鄰，原 H−{r,s} 恰有兩份 mixed，其餘 unary，
並保留 [N45 §1](c5_excess_two_nonadjacent_unit_core45.md#1-全部共同前提與原身份)
的全部原來源前提。

**定理 3。** 在此完整 N2 契約下，對每份原 C 及每條 e∈E_C，

\[
 \boxed{\Sigma(G-C)=\Sigma(G-e)=\Omega.} \tag{6}
\]

*證明。* 兩份 mixed 使 m_r,m_s≥2，刪 root 引理排全部單-root core；
再加兩-root44排除得 Z=∅。定理2先處理 mixed 及 incidence≥2 unary。

剩下原 unit unary U，owner記為r。反設 G−U 拒絕β，取 minimal core M。
兩 roots 皆保留；r 在 G−U 中degree四，M亦四；s不能再降四，否則是已排44。
故 s仍五。r的四條保留接線與s的全部接線，再由degree-4飽和傳遍其餘原分量，
迫 **M=G−U**。於是 X=G−U=M 本身同β minimal、degrees45、原U恰一接線，
兩份原 mixed 與其餘分量全留，逐項滿足 N45-U §1 的精確身份。
既有已採納 N45-U 全排適用，矛盾。全部 C 均全收，式(2)給所有 e。∎

因此 N2 的每個非 root 內點都滿足(5)，包括所有 unit unary。
每份被拒絕列的每份 minimal core 都保留全部原分量及其全部 incident 邊；
若不等於G，只能是 **G減一條原root-spoke**，degree為45／54。
若原兩 roots 都沒有 spokes，就必由G自身作每個拒絕列的55 core；尚未排除這種來源。

式(6)沒有聲稱 root-spoke 刪除全收，亦沒有完成剩餘 N45-S 全部身份或原55排除。
其新內容是將限定 N45-U 排除接成整個 N2 的分量必留必要條件，
沒有把另一 derivative 未經 minimalize 就當成 M。

## 6. 有限控制、失敗紀錄與重播

[Checker](../../../../../../scripts/c5_excess_two_arc_component_slack.py)從上輪179個原ER代表中
固定選出全部63張雙degree-5圖；直接保存並使用原邊、root／頂點座標及來源引用。
不重新標號、不生成新來源圖。來源disk及C44 core完備性沿用既有證據，未重驗rotation。
每列用新的numeric-order DFS枚舉完整染色，來源Σ另與既有frontier DP核對。

[產物](../../../../../../artifacts/c5_excess_two_arc_component_slack/observations.json)保存
原179份分量、完整16-pin local fibres、全部外部full lifts；局部接合重建整圖完整染色，
逐邊比較式(1)的完整外部投影。刪邊的完整fibres保存數量及規範序列hash，由checker重算。
不能由相同投影推論刪邊前後內部fibres相同。

| 固定控制 | 結果 |
| --- | --- |
| 原來源Σ | 63張、630列與原Σ及frontier DP一致 |
| 完整local／outside接合 | 1,790次與直接整圖full lifts相等 |
| 分量邊刪除的完整外部投影 | 13,010次式(1)相等；刪除一條分量邊後，208,160個ambient root-pin cells的局部fibres全非空，包含外部full lifts為空的pins |
| boundary重色slack | 全十列有156個正觸發，全部16-pin關係全開 |
| P 的實際逐邊判定 | 62張 triggered and holds；1張不滿P。上輪充分前提 \|Z\|≤1 在此子集只觸發57張 |
| 無兩-root44的非unit原分量 | 134份觸發式(4)，此域Z皆空，整份省略均全收 |
| 拒絕列中的boundary重色 | 0觸發；不將156個已接受列的slack控制說成此來源排除的正控制 |
| 目標Σ933／941或整圖像 | 0張，not triggered；N2定理3依紙面前提接入，無目標來源控制 |
| 逐點條件不足的local控制 | 原path 7–8–9，7接012、9接123、8接r/s；每點完整degree四，逐點通過、整份D_C={0,3}。不是disk／Σ-critical／目標來源 |

首次生成把「\|Z\|≤1足以推出P」誤寫成兩個布林值等價，assertion失敗，
尚未寫出產物。修正為單向蘊涵後通過：另五張有兩個Z位置的Σ957控制其實也滿足P。
這是checker對充分條件的誤用，未改上輪定理，也未將充分條件提升為必要條件。

重播命令：

```bash
python3 scripts/c5_excess_two_arc_component_slack.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_arc_component_slack.py --check
python3 scripts/c5_excess_two_arc_pair_critical.py --check
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
lake build
git diff --check
```

主產物SHA-256：`e57dd4e28b1029fb53fd740da3aa79378c67fe4a336ee146dd9fda2a49105d20`。
生成使用exclusive create；需要另存時指定新的`--output`。

本輪一般及`PYTHONHASHSEED=17`重播均exit 0，產物bytes／SHA一致；
上輪pair-critical的`--check`亦exit 0、原SHA不變。
`check_docs.py`通過（614 Markdown、7,572 local links），正式docs的DocGraph通過
（62 documents、213 relations、0 errors）。`lake build`通過（8,831 jobs，
保留既有linter warnings）；`git diff --check`通過。Build不承擔新紙面證明。
未重跑全工作樹含scratch的DocGraph、上游44／N45-U分類、原來源搜尋或rotation驗證。

文件傳播：更新本報告、Kempe導覽、STATUS索引、N45直接父入口及E-ARC2 synthesis，
在上輪報告加後續連結。README及HANDOFF已核對，研究線與入口未改，保留既有未提交修改；
其他研究線及歷史worker證據不改。這次只收窄必要結構，沒有完整父身份closure。

## 7. 精確停止點

本輪完成同一原分量的跨列重色排除，以及完整N2契約下式(6)和全部非root附件限制。
仍缺：在保留這些條件的同一disk原圖上，排除剩餘root-spoke 45／54及原55的共同三列拒絕。
N1、相鄰roots、一般單-root例外仍各保留；沒有將N2、E-ARC2或猜想E改為CLOSED。
沒有新增Lean證明，沒有commit／push。
