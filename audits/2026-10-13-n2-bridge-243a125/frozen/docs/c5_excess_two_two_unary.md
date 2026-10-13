# ε=2：t=2、(2,1,1) 的兩份原 unary 省略排除

**後續（2026-10-03）**：[通用短支援引理](c5_short_support_singleton.md)
迫本型三份原分量各至少兩段跨度，因而排除整型來源；見
[合成報告的共同推論](c5_excess_two_single_spoke_complete.md#4-結論證據層與停止點)。
下文保留當輪省略核心的證明及證書。

**後續（2026-10-03）**：[同型原 binary 省略分支](c5_excess_two_binary_two_unary.md)
亦已排除；t=2、(2,1,1) 的全部容量二省略均全收，已無全 degree-4
真子核心。當輪尚未排除整型；後續整型排除見頁首。共同 ε≥2 不變，
下文保留當輪範圍。

2026-10-03，基準 `bbd900a`，接續工作樹的
[t=2 雙 binary 省略](c5_excess_two_two_binary.md)。目前接手點見
[Kempe 導覽](c5_kempe_guide.md)，實際驗證見
[研究紀錄](history/2026-10-03-excess-two-two-unary.md)。

**結論：933／941 的固定完整 Σ、edge-minimal C₅ disk 來源，若 ε=2、
唯一 degree-6 root r、t=2，且 H−r 的原接點分拆為 (2,1,1)，則同時
省略兩份原 unary U、V 後，必接受全部十列。**

任意大小涵蓋沿用全 degree-4 分類及原接點 tail transfer；新增證據為
紙面接合與 Python 固定必要域證書。3,980 個比較全排除，甚至不需
兩份 unary 的 D 身份守恆或新增支援弧限制。沒有新增 Lean theorem。
原 binary 省略、整份 (2,1,1) 來源及其餘 ε=2 仍保留；共同下界仍 ε≥2。

## 1. 完整前提與原五接點關係

G 有限簡單，B=(b₀,…,b₄) 是指定有序 induced-C₅ disk 外框，完整 Σ
為 933、941 或其整圖 D₅ 像。每條非框邊 e 都有 Σ(G−e)⊋Σ(G)。
有效內部 H 連通，r 完整 degree 六，其餘內點完整 degree 四。
r 的兩條原 spokes 是 rb_s、rb_t；H−r 的三份原連通分量為 A、U、V，
原接點分別是 (x,y)、u、v。全部附件、ownership、root 邊與原分量保持。

固定 proper boundary coloring b，原完整 relations 記作 R_A(b;x,y)、
S_U(b;u)、S_V(b;v)。刪去 r 後，接點有 slack；在各連通分量選接點
作生成樹根、逆序貪婪染色，故三份 relation 對全部十列皆非空。詳見
[容量介面](c5_independent_support_capacity.md#2-任意-root-的完整條件介面包含-mixed)
及 [unary slack](c5_excess_two_spoke_unary.md#2-原-v-的-relation-非空不需分類其大小或支援)。

原五接點關係恰為

\[
\mathcal R_G(b;r,x,y,u,v)=
\{(a,c,d,e,f):(c,d)\in R_A(b),\ e\in S_U(b),\ f\in S_V(b),
\quad a\notin\{b_s,b_t,c,d,e,f\}\}. \tag{1}
\]

各 tuple 由同一 b 下三份原分量的完整染色接合，並檢查四條原 root 邊。
令 F_A=∩_{(c,d)∈R_A}{c,d}；F_U=S_U 若 |S_U|=1，否則 F_U=∅，
F_V 同理。因分量只共用已固定的 B，式 (1) 在 r 的精確投影為

\[
U_4\setminus(\{b_s,b_t\}\cup F_A\cup F_U\cup F_V),\qquad
U_4=\{0,1,2,3\}. \tag{2}
\]

這只用於原 root 接合判定，未以 binary marginals 或禁色取代完整 relation。
U、V 的原染色由它們的完整 S 提供，不把它們替換成自由 degree-one 點。

## 2. 同時省略兩份 unary 的原核心

反設 K=G−U−V 拒絕 q。K 有效內部連通、完整 degree 全為四，並繼承
disk 與 T4 全收。任一 minimal q-core 的 degree-4 飽和沿內部傳播，
迫它等於整張 K。由[全 degree-4 分類](c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論)，
Σ(K)=Ω∖{q}。原 A 內的 x–y 路徑連同 rx、ry 給經 r 的 cycle；分類
迫 r 位於原 triangle rxy，xy 是原邊，r 在 K 的內部 degree 為二。

對整張 G 共同作 D₅／S4 搬運，令 q=q₄=01012（十列索引 0）。其後
三份原分量不再各自正規化。K 的原位置落在
[three-spoke 報告 §2–3](c5_941_three_spoke.md#2-原-degree-2-root-的完整位置分類)
的 118 bases／398 個具名原 r 位置：36 份無枝 triangle 必要 bases、
18 份帶枝 bases、64 份直接 bridge 雙 triangle bases。
不使用該報告新增第三條 spoke 的圖；本輪只取原兩-spoke 核心。

任意長 tails 的化約保持全部 proper b 的原有序 R_A，原 x、y 及兩條
spokes 保持，因此式 (1) 在接上任意原 U、V 時仍精確。U、V 的內部、
附件及支援不作縮減。無枝 bases 未全部篩 disk；本輪在此較大必要域
已全排除，沒有為這些必要模型宣稱 disk 實現性。

## 3. 另一份省略圖與五個已知全收限制

令 L=G−A，保留同一原 U、V、spokes、B 與 r。L 有效內部連通且
完整 degree 全為四。若 L 拒絕任一列，飽和傳播與全 degree-4 分類使
它自己成為單缺失核心。因此 **同一 L 至多拒絕一列**。

另沿用候選來源的兩項已證結果：

1. [雙 spoke 省略全收](c5_excess_two_double_spoke.md)：每列均有
   F_A∪F_U∪F_V≠U₄。
2. [t=2 spoke＋unary 省略全收](c5_excess_two_spoke_unary.md)：對 j=s,t
   及 W=U,V，每列均有 {b_j}∪F_A∪F_W≠U₄。這是保留一條 spoke 及
   一份 unary、刪掉另一條 spoke 及另一份 unary 的四種具名圖。

上述圖全是同一原來源的子圖；不將獨立的核心或不同色框拼成來源。
L 的拒絕判準是 {b_s,b_t}∪F_U∪F_V=U₄，亦由式 (1) 刪去 A 因子得到。

## 4. 放寬的有限必要域已空

對 398 個 marked cores、兩候選各五個 D₅ 像及十列，獨立容許
F_U、F_V 各取 ∅、{0}、{1}、{2}、{3}，共 25 對。只保留符合式 (2)
的目標接受性及 §3 五個全收限制者。若某列沒有選項，該比較排除；
否則若兩個不同列的每個剩餘選項都迫 L 拒絕，違反 L 至多拒絕一列。

跨列選項完全獨立，比同一原 unary 可實現的 relations 更寬。
因此這個放寬域的排除對任意原 U、V 成立；**正式證書不需使用 D 身份
守恆，也不需新增支援跨度、共同扇區或 planarity oracle**。

| 排除原因 | 933 五像 | 941 五像 |
| --- | ---: | ---: |
| K 已拒絕目標須接受的 q₄ | 398 | 796 |
| 某列的 25 對 unary 禁色全部不符必要限制 | 508 | 333 |
| 同一 L 被迫拒絕至少兩列 | 1,084 | 861 |
| 合計 | 1,990 | 1,990 |

全部 3,980 個比較排除，故反設不成立：

\[
\boxed{\Sigma(G-U-V)=\Omega.}
\]

## 5. 證書、重播與停止點

[Checker](../scripts/c5_excess_two_two_unary.py)及
[artifact](../artifacts/c5_excess_two_two_unary/observations.json)保存 source hashes、
原 marked-core 索引、目標 mask 及逐比較的排除列；迫 L 拒絕兩列時，
保存兩列全部剩餘的具名 (F_U,F_V) 選項。
Checker 沿用原邊 verifier，重算 398 個位置、全部十列完整 binary／
三接點 relations、逐 tuple 核心染色及帶枝／雙 triangle 的 rotations。

3,980 份原核心列給 111 份不同的字面接合輸入。每份保存完整五接點
算子及其所有 (mark,row) 來源索引，前面三欄可直接查原 artifact 的
完整核心染色 witness。逐一限制到全部 15×15 對非空 unary domains，
以獨立 Cartesian-product 定義核對完整五接點 tuples 及式 (2)，合計
24,975 次控制。相同輸入只在這個代數驗證中共用算子；未合併來源身份。
尚未指定原 U、V 的圖，故不宣稱這些抽象 domains 都有來源染色或 disk 實現。

```bash
python3 scripts/c5_excess_two_two_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_two_unary.py --check
python3 scripts/c5_excess_two_two_binary.py --check
python3 scripts/c5_excess_two_spoke_unary.py --check
python3 scripts/c5_excess_two_double_spoke.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

本輪只完成指定兩-unary 省略分支。連同既有雙 spoke 及 spoke＋unary
結果，t=2、(2,1,1) 的全 degree-4 rejected-row core 若存在，省略身份
只可能是整份原 binary A。理由是其他內點原 degree 已為四，飽和沿
原分量傳播，任何保留分量都必完整保留其接線；r 要從 degree 六降到
四，只能省略容量二，即一份 binary 或四個 unit 因子中的一對。
本輪及前序已排除所有 unit-pair 身份。

下一窄入口是同型的 binary 省略分支，詳見導覽。未排除整份 (2,1,1)、
其餘 ε=2、兩個 degree-5 roots（含 mixed）或一般來源，未提高共同
ε≥2，未證一般出口或 K∞=K≤5。任意大小覆蓋與外部 degree-list 前提
沿用依賴報告；Python 負責固定必要域，`lake build` 不表示新紙面證明
已 Lean 化。
