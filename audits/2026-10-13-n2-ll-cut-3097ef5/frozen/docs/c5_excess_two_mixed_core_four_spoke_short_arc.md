# ε=2 四-spoke (2,2)：短框弧 mixed 的完整關係與原拒絕列延拓

**後續（2026-10-03）**：[不相交pairs完成報告](c5_excess_two_mixed_core_four_spoke_disjoint_pairs.md)
已排最後14／18份，完成四spoke(2,2)、mixed11+各側一原unary。
下文保留本輪原拒絕列出口、當輪殘留及證書；其他incidence及ε≥3未證。

2026-10-03，接手 HEAD=`0e38127`，接續
[原 unary crosscut 排除](c5_excess_two_mixed_core_four_spoke_crosscut.md)
所留 941 原 a=5、b=6、spokes=02／03、source indices=155／175。
使用者在續研中要求「繼續」，本輪沿用同一固定必要域，保留前序未提交
成果及 artifacts。現況見 [Kempe 導覽](c5_kempe_guide.md)，驗證及
貼用摘要見 [本輪紀錄](history/2026-10-03-excess-two-four-spoke-short-arc.md)。

**原 02／03、root 交換及剩餘六份共用框點的 941 框架均作任意大小來源排除。**
原 mixed 的短支援使完整 R_C 可避開任意共同 root 色；再用同一 β 的
未見色交換，構造原候選拒絕列的一份完整六角色 joint。941 的共用
一框點框架因此從 6 降至 **0**，unequal 殘留從 **14／24 降至 14／18**，
全部是不相交 spoke-pairs。**共同 ε≥2 不變，ε≥3 未證，未新增 Lean theorem**。

## 1. 原圖、faces 與完整有序接合

來源前提與前序相同：有限簡單 G，B=(b₀,…,b₄) 為指定有序
induced-C₅ disk，完整 Σ=941 或其整圖 D₅ 像，每條非框邊 Σ-critical。
有效 H 連通、ε=2，相鄰完整 degree-5 roots a,b，其餘有效內點完整
degree 四。H−{a,b} 恰為原 mixed C（incidence=(1,1)、ordered contacts
(x,y)、owners=(a,b)）及 U、V（原單接點 u、v，各接一 root）。
x=y 保持同一原點，原 ab、各側兩 spokes、所有原附件、actual supports、
bridges、旁支、ownership、嵌入環序及共同字面色框保持。

Canonical 原 spokes=02／03 的四個 faces 為

| 原 face | 原框包絡 | 可接入原分量 |
| --- | --- | --- |
| b₀–a–b₂–b₁–b₀ | {0,1,2} | U |
| b₀–a–b–b₀ | {0} | C、U、V |
| a–b₂–b₃–b–a | {2,3} | C、U、V |
| b₀–b₄–b₃–b–b₀ | {0,3,4} | V |

共用四邊形與三角 face 對 U、V 都是短支援，原 spoke 到 pair 外提供
外路徑：{2,3} 用 owner–b₀，{0} 用 a–b₂ 或 b–b₃。因此
[短支援引理](c5_short_support_singleton.md)與原 au／bv criticality
迫 U、V 分居各自原外 face，actual supports 分別含 {0,2}、{0,3}。
C 仍在原 0ab 三角形或共同四邊形，故其固定 actual support 滿足

\[
S_C\subseteq\{0\}\quad\text{或}\quad S_C\subseteq\{2,3\}. \tag{1}
\]

記原完整 relations R_C(β;x,y)、R_U(β;u)、R_V(β;v)。原 joint 仍是

\[
J_G(β)=\{(A,D,X,Y,T,W):(X,Y)\in R_C,\ T\in R_U,\ W\in R_V,
\ A\notin β(\{0,2\}),\ D\notin β(\{0,3\}),\ A\ne D,X,T,\ D\ne Y,W\}.
\tag{2}
\]

Relations 附整份原分量 coloring witnesses，所有 guards 在同一字面 β
接合；不相乘 C marginals，也不逐分量另作色正規化。

## 2. 原 C 的共同避色：不同接點與同一原接點分開證明

令

\[
F_C(β)=\bigcap_{(X,Y)\in R_C(β)}\{X,Y\}. \tag{3}
\]

原 R_C 非空：刪兩份 root guards 後，contact 點有 list slack，按原
生成樹逆序貪婪可染整份 C。式 (3) 只用於同一共同 root 色，不能
代替完整 R_C 的異色 root-pair 接合。

**x≠y。** 在原 planar 圖中收縮 ab 為輔助 root r，simplify 重複的
r–b₀ spoke。唯一原 C contacts 是 x、y 不同兩點，所以沒有 C 頂點
同接 a、b；C 的每點完整 degree 四均保持，C 仍是 H′−r 的原連通分量。
C 的內邊、boundary attachments 及 boundary-only R_C 完全沒動。
若式 (1) 的支援在 {2,3}，r–b₀ 是 pair 外的原 spoke；若在 {0}，
以相鄰 pair {0,1} 包住支援，r–b₂ 是 pair 外的原 spoke。
短支援引理因此使原 C 能避開每個共同 root 色，即 F_C=∅。

這次收縮只用來套用原 C 的局部避色引理；它**不保存整份 G 的染色
或完整 Σ**，原 ab 的異色 guard 亦沒有被當作可合併的 coloring factor。

**x=y。** 不收縮重複 contact edges。對任意 c，兩個原 roots 同禁 c
在同一 contact 頂點只有一個不同禁色。該點有至少一份 list slack，
其餘原 C 點仍有 degree lists，connected greedy 給避 c 的完整 C
coloring。因此亦有

\[
\boxed{F_C(β)=\varnothing\quad\text{對每個 proper }β.} \tag{4}
\]

這裡只沿用短支援的既有任意大小證明與 connected slack-list 事實，
不將 fixed Python relations 當作任意大小 C 的實現。

## 3. 一份原拒絕列的同框完整 witness

取 canonical β=q=`01021`。U 在原外 face 012，只看见 boundary 色
{0,1}；完整 R_U 與整份原 U colorings 因此在 **2↔3** 交換下不變。
原 R_U 非空，不能恰為 singleton {2}，故有一份原 witness 令 u=T≠2。
固定 a=A=2，满足原 a-spokes=02 的 guards。

C 的實際支援在 {0} 或 {2,3}，所見 boundary 色包含於 {0,2}，故
完整 R_C 在 **1↔3** 交換下不變。下面的完整 relation 引理適用：

> R 非空、在同時交換兩個 contacts 的 1↔3 下不變，且
> \(\bigcap_{(X,Y)\in R}\{X,Y\}=\varnothing\)。則對 D=1、3 都有
> \(\exists(X,Y)\in R:\ X\ne2,\ Y\ne D\)。

若 D=1 的 fibre 為空，R 包含於 X=2 或 Y=1；以同一整份 witness
交換 1↔3，R 又包含於 X=2 或 Y=3。兩者交集迫所有 tuples 都 X=2，
與共同避色式 (4) 矛盾。D=3 同理。這一步用完整兩接點 R，沒有
從兩個 endpoint 各自可用推出共同 tuple。

選任一原 V coloring，v=W。從 **{1,3}∖{W}** 選 b=D，集合必非空。
原 b-spokes=03 看見 {0,2}，所以 D 合法；D≠A，且 bv guard 成立。
上述引理在這個同一 D 下給原 C 的完整 witness，與已選 U、V witness
在同一 β、同一 roots 接合，得到式 (2) 的一份完整 tuple。因此

\[
\boxed{q=01021\in\Sigma(G).} \tag{5}
\]

此列被下節每份整圖搬運後的來源 Σ 拒絕，故原來源不存在。
本證明只構造這一份原拒絕列的延拓，**不宣稱 C 延拓所有異色 root
pairs**。例如原四邊形內的 C triangle 可以阻斷 swapped seen pair，
原共鄰 singleton 可阻斷四個不同外色；完整 relation 的負控制保留。

## 4. 六份原身份與共同 D₅ 搬運

每份骨架、β、actual supports、root roles、C contacts 與 U／V 身份
一起搬到 canonical 02／03。必要時交換整對 root roles，同時交換
整份 C tuple 欄位及 U／V ownership；不獨立重新正規化分量。

| 原 941 index | boundary permutation g(0)…g(4) | 交換 root roles | 搬運後 Σ | 原拒絕 row index |
| --- | --- | --- | ---: | ---: |
| 155 | 0,1,2,3,4 | 否 | 941 | 1 |
| 175 | 0,1,2,3,4 | 是 | 941 | 1 |
| 179 | 2,3,4,0,1 | 否 | 949 | 4 |
| 239 | 3,2,1,0,4 | 否 | 949 | 6 |
| 243 | 1,0,4,3,2 | 是 | 941 | 1 |
| 263 | 1,0,4,3,2 | 否 | 941 | 1 |

原 row 1=`01021`、row 4=`01202`、row 6=`01212` 都被原 Σ941 拒絕；搬運後 q=`01021`
亦被 Σ941／949 拒絕。不能任選 reflection 後假設 q 仍是拒絕列；
證書逐份核對 chosen 原 identity、整圖 mask／列／四色 transport。

| 原必要域 | 933 | 941 |
| --- | ---: | ---: |
| 前序 unequal-pair 框架 | 14 | 24 |
| 本輪短框弧排除 | **0** | **6** |
| 剩餘共用一框點 | 0 | 0 |
| 剩餘不相交 pairs | 14 | 18 |
| 剩餘合計 | **14** | **18** |

## 5. 有限證書與重播

[Checker](../scripts/c5_excess_two_mixed_core_four_spoke_short_arc.py)、
[joint helper](../scripts/c5_excess_two_four_spoke_short_arc_joint_controls.py)、
[artifact](../artifacts/c5_excess_two_mixed_core_four_spoke_short_arc/observations.json)
唯讀前序原身份與完整支援引理證書；所有固定 relation 及圖 controls
只核對本頁的必要語義，不提供 disk／來源 Σ／criticality 實現。
固定 1↔3 的 16 ordered tuples 分成10orbits，1,023非空不變relations中
963份滿足F_C=∅，含5份共鄰對角型；完整schema保存A=2、D=1／3的
guarded fibres，不只存root marginals。7份非空U不變palettes與15份
非空V palettes，合成 **101,115** 份同框六角色 witnesses。
這些是完整抽象relation的tuple witnesses；不宣稱963份relations均有
原圖實現，原分量coloring存在量詞由紙面關係語義承擔。

12張完整degree圖保存C共鄰singleton／不同contacts triangle、三種
unary配對與root交換，11種原圖變體共 **1,320整圖joints／21,120
pinned fibres**；1,080原邊接回、660swaps及12份原q完整colorings
逐邊核對。Triangle swapped-seen-pair與singleton四外色拒絕保存，
防止把指定列出口誤稱為所有root pairs延拓。實際hash與驗證範圍見本輪紀錄。

```bash
python3 scripts/c5_excess_two_mixed_core_four_spoke_short_arc.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_short_arc.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_crosscut.py --check
PYTHONHASHSEED=17 python3 scripts/c5_short_support_singleton.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
python3 tools/artifacts.py status
git diff --check
```

## 6. 精確停止點

**相鄰唯一 mixed、四-spoke (2,2)、mixed-(1,1) 加各側一原 unary 的
共用一框點框架全封閉。** Unequal pairs 仍剩14／18份，全為不相交
spoke-pairs；其他 (2,2) incidence、較少 spokes、單省略、(5,5) q-core、
多 mixed／no-mixed／非相鄰與 unary 側例外均保留。
下一具名不相交入口由 [Kempe 導覽](c5_kempe_guide.md)保存，保留原 C／U／V、
actual supports、原環序與完整 joint，先分析兩側原 crosscuts 的相對位置。
紙面＋Python，ε≥3、來源實現、一般出口與 K∞=K≤5 未證，未 commit／push。
