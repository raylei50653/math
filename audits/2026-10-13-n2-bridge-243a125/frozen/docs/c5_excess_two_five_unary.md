# ε=2：t=1 五原 unary 的整型來源排除

2026-10-03，接續 [t=1 原 binary 省略](c5_excess_two_single_spoke_binary.md)
及 [四原 unary 排除](c5_excess_two_four_unary.md)。目前研究停止點見
[Kempe 導覽](c5_kempe_guide.md)。

**結論：933／941 的固定完整 Σ、edge-minimal C₅ disk 來源，在 ε=2、
唯一 degree-6 root r、t=1 前提下，不可能有五份原 unary 分量。**
本輪排除整份 `(1,1,1,1,1)` 型，不只是某個省略身份。
較強地，在下述 degree／disk／T4 前提下，五原 unary 圖必接受全部 Ω；
這一步不需要完整 Σ edge-minimality。

證明由同一拒絕列的四因子子覆蓋，構造必須存在的全 degree-4 核心；
其 root 有至少三條內部 bridges，與既有分類矛盾。任意大小涵蓋依賴
紙面論證及既有分類；Python 僅核對具名省略和完整接合的小固定域。
未新增 Lean theorem、圖枚舉或 disk 實現主張；其他 t=1 分拆、其他
ε=2 來源、一般出口及 K∞=K≤5 不由本報告排除。

## 1. 原來源與六接點完整接合

G 有限簡單，B=(b₀,…,b₄) 是指定有序 induced-C₅ disk 外框，G 接受
全部 T4。有效內部 H 連通；r 的完整 degree 六，其餘內點完整 degree
四。r 的唯一原 spoke 是 rb_s；H−r 的原連通分量是 U₀,…,U₄，
各以唯一原邊 rxᵢ 接 r。每份原分量、接點、全部附件、ownership、
環序與同一嵌入保持。分量自身可以含 cycles；沒有假定它們是樹。

固定任一 proper boundary coloring b，令 Sᵢ(b) 是原 Uᵢ 在 xᵢ 的
完整可取色集。每個 Sᵢ 非空：刪 r 後，xᵢ 的 boundary list 至少比
deg_Uᵢ(xᵢ) 多一色，其他點的 list 至少為其 Uᵢ degree。以 xᵢ 為
生成樹根，逆樹序貪婪即可染色。這就是
[unary slack 引理](c5_excess_two_spoke_unary.md#2-原-v-的-relation-非空不需分類其大小或支援)。

在同一字面四色框 U₄={0,1,2,3}，完整有序關係恰為

\[
\mathcal R_G(b;r,x_0,\ldots,x_4)=
\{(a,c_0,\ldots,c_4): c_i\in S_i(b),\quad
a\notin\{b_s,c_0,\ldots,c_4\}\}. \tag{1}
\]

每個 tuple 由同一 b 下五份原分量的完整染色拼接，再核對六條原 root
邊。原分量間無邊，故此式雙向成立；沒有逐分量重選色框或拆分多接點。

只為此 root 判定，令 Fᵢ=Sᵢ（若 |Sᵢ|=1），否則 Fᵢ=∅。式 (1)
的 root 投影為

\[
U_4\setminus\bigl(\{b_s\}\cup F_0(b)\cup\cdots\cup F_4(b)\bigr). \tag{2}
\]

Fᵢ 沒有取代完整 Sᵢ 或有序 tuples；式 (2) 僅因單一接點在 domain
至少兩色時能避開任何已指定 root 色。

## 2. 每個拒絕列都迫出四因子原子圖

反設 G 拒絕 q。因 G 接受 T4，q 是 singleton 列。由式 (2)，具名六
因子 `{q(b_s)},F₀(q),…,F₄(q)` 覆蓋四色；每因子至多一色。各色
選一個包含它的因子，得到四個互異因子的子覆蓋。保留這四份原因子，
另兩份按原身份省略：spoke 刪原邊；unary 刪整份 Uᵢ 及 incident
邊。得到同一原圖的子圖 K，未新增接線、附件或收縮路徑。

K 仍拒絕 q，並因是 G 的子圖而接受全部 T4。root 的完整 degree
恰為四，其餘保留內點完整 degree 仍為四；有效內部連通。
所有十五個具名省略 pairs 分成：

| 省略原因子 | 身份數 | 保留原 unary 數 | root 內部 degree |
| --- | ---: | ---: | ---: |
| 兩份 unary | 10 | 3 | 3 |
| 唯一 spoke 與一份 unary | 5 | 4 | 4 |

保留的 rxᵢ 都是 K 的內部 bridges：在原 H−r 中 Uᵢ 已是不同連通
分量，而且每份只接 r 一條邊。因此 **r 不在 K 的任何內部 cycle**。
這與 Uᵢ 自己是否含 cycles 無關。

## 3. Degree-4 飽和與結構矛盾

在 K 中取 minimal q-obstruction M，保留指定外框。M 的每個有效
內點完整 degree 至少四，否則刪去該點後的染色可用四色貪婪接回。
但 K 的全部內點完整 degree 已恰四；因此只要 M 保留一個有效內點，
便保留其全部 K-incident 邊。沿 K 的連通內部傳播，迫 M=K。
M 必有有效內點，因 proper q 不會被只有外框的圖拒絕。

套用 [全 degree-4 分類](c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論)：
接受全部 T4 的 C₅ disk 全 degree-4 minimal q-obstruction，內部只
可能是路徑、triangle 接不分叉的 paths／tails，或兩個 triangle 以
一條 bridge 直接相連。特別是

\[
v\text{ 不在內部 cycle 上}\quad\Longrightarrow\quad
\deg_{H(K)}(v)\le2. \tag{3}
\]

式 (3) 沿用 [樹核心](c5_tree_cores.md)、
[triangle 外掛樹](c5_triangle_forks.md)與
[雙 triangle](c5_two_triangle_blocks.md)的結構結果，並非僅由
「完整 Σ 單缺失」推出。r 不在 cycle 上卻有三或四條內部 bridges，
違反式 (3)，矛盾。

故 G 沒有拒絕列，Σ(G)=Ω。933、941 及其整圖 D₅ 像皆有拒絕列，
因此此五原 unary 整型來源全數排除。關鍵是每個拒絕列都**必須**有
四因子子覆蓋；這補上了從「所有全 degree-4 真子核心皆不存在」到
整型來源排除的必要一步。其他含 binary／更高容量分拆沒有在此被
替換成獨立 unary factors。

## 4. 有限證書與驗證界線

[Checker](../scripts/c5_excess_two_five_unary.py)與
[artifact](../artifacts/c5_excess_two_five_unary/observations.json)保存：

- 全部十五個具名四因子保留／兩因子省略身份及 root bridge degree。
- 原 spoke 四種色、五份原 unary 各空或 singleton 的必要域中，全部
  3,000 份四色覆蓋，以及每份的**所有**四因子子覆蓋，共 8,400 份。
  每份都指向上述十五個不可能的結構身份之一。
- 十六種 root domains 乘十五種非空原 unary domains，共 240 份
  完整有序二接點 transition 表。這控制逐次接合的精確 root 投影；
  紙面式 (1) 保留接合前的全部 coordinates。
- 972 個完整六接點 star tuples；在五種字面 domains（四色
  singletons 及 U₄）的全部 5⁵ 份五元組上，分別接四種原 spoke 色，
  核對 12,500 次完整六接點 tuples、獨立 Cartesian product 接合及
  式 (2)。這是代表 domain 的有限控制，沒有聲稱遍歷全部 15⁵ 份
  非空 domains；其餘 domains 的投影公式由上述完整 transition 表
  及紙面逐次接合涵蓋。
- 兩候選各五個 D₅ 像的拒絕列身份，共十份目標排除紀錄。

抽象 domains 及 forbidden factors 不宣稱來自可實現 disk。所有
原圖的任意大小、degree-4 飽和及結構分類仍是紙面輸入；本 checker
沒有驗證拓撲，亦未重新驗證所引用的全部歷史分類證書。

```bash
python3 scripts/c5_excess_two_five_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_five_unary.py --check
```

上述兩次新 checker 重播已通過。整批文件、artifact 與 Lean 驗證由
本輪總研究紀錄保存；未新增 Lean 定理，`lake build` 不把本證明變成
Lean 形式化。此報告停止於五原 unary 整型排除；其餘 t=1 分拆及
下一步以 [Kempe 導覽](c5_kempe_guide.md)為準。
