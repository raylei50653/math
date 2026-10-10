# E4 獨立補充：原 core 身份、spoke 與面容量

2026-10-04；基準 `integrate-kprime-e3 @ 2ac279b`；獨立 worktree
`/home/ray/developer/ai/math-task-e4`，branch `task-e4-nonadjacent`。
Python 使用 `/home/ray/developer/ai/math/.venv/bin/python`。
本補充只 exclusive-create 新檔，不修改任何基準文件、checker／證書，不 commit／push。

**本補充的 verdict：N3 整類排除成立；N1、N2 得到新的共同限制，仍保留精確原 relation 殘留。**
另有並行 producer 在同工作樹建立 [canonical REPORT](REPORT.md) 及 control／reductions
檔案。本補充的 canonical REPORT exclusive-create 遇到 FileExistsError，未覆寫；
改以本檔及 [core_validation.json](core_validation.json) 交付自己的證據。
本方 root 另逐步核對該並行 REPORT 的 unrestricted N-empty、N-diagonal／短 mixed
無 unary 排除；独立 reviewer 核對其 N1 mixed22-44 排除。那些較強結論的原始
文字仍由 canonical REPORT 負責，本補充的 checker 不聲稱驗證那些 producer。

| 分支 | 本補充結果 | 完成的共同約束 | 本補充原 relation 殘留 |
| --- | --- | --- | --- |
| N1，一 separating mixed | 部分化約 | unit-side derivative E2 限制；root三spokes024／124排除；空 support 在兩側有 side 因子時排除 | `(4,4)` 各側 unit、單側 `(4,5)/(5,4)`、原 `(5,5)`；至多一 root-deletion 例外；保留完整 sole-C 十列 relations |
| N2，兩 mixed | 部分化約 | selected row 不能兩 roots 同時有重色 spokes；一 root 重色時 qcore 必恰是對應原 spoke omission `(4,5)/(5,4)`；E2 derivative 與原盾弧 | 原 unit-mixed omission `(4,4)`、兩 mixed 全保留的單側 unit 和原 `(5,5)` |
| N3，至少三 mixed | 整類排除成立 | 同一原 disk 的 K₂,m 面容量＋原 N-empty 得 m≤2 | 無 |

不存在本補充新構造的滿足所有三列前提之反例。未找到要求的可實現
nonadjacent 5+5／T4 全收／Σ-critical／ε2 正控制，不能從有限搜尋未找到推一般定理。

## 1. 前提與完整原身份

使用 [E3 REPORT §1、§2](../c5_excess_two_e3/REPORT.md)、
[nonadjacent notes §1–5](../c5_excess_two_e3/nonadjacent_notes.md)、
[E2 REPORT §5](../c5_excess_one_e2/REPORT.md)、
[unary shield](../../docs/c5_unary_shield_budget.md)、
[q-core shield](../../docs/c5_qcore_shield_budget.md)。

G 有限簡單；指定有序 induced-C₅ B 圍 disk 外面；T4 全收；每條非框邊
對自身完整 Σ critical；ε2；z,w 非相鄰 degree5，其他有效內點 degree4。
固定 q₀=01212/index6、q₁=01202/index4、q₃=01021/index1 全拒絕；
q₂=01201/index3、q₄=01012/index0 自由。忽略孤立私有點。
沿用已證 triple-critical、root-deletion 至多一例外、(4,4) 恰保留一 mixed、
m≥2 所有原 pieces one-sided、N-empty。

原 P 永遠是 H−{z,w} 完整連通分量。保留原頂點、原內部 edges、實際框
attachments、所有有序 distinct contacts、ownership、shared contact、原 rotation／face。
跨列比較只在同一個字面色框，不能各自 normalize 原 component。
外部 Gallai／degree-list／K₅ 非平面性依賴沿既有 hub 紙面定理，不計為 Python／Lean 成果。
本輪沒有新 Lean source，未跑 lake build，沒有四色定理 oracle。

## 2. N1：unit-side derivative 不必預填 criticality

**E4-U。** 取原 unit side 因子 f：一條 root-spoke，或一份只有一條原 root-contact
的 unary。X=G−f 保留 B，繼承 induced disk，接受 T4。相應 root 降至4，
另一 root5，其餘保留內點4，移除 degree4 unary 的 surplus 為零，所以 ε(X)=1。
X 不能同時拒絕 q₃ 與 q₀／q₁。

取保留 B 且 `Σ(Y)=Σ(X)` 的 inclusion-minimal 子圖 Y。每條非框邊刪除必擴大
其自身 Σ，所以 **Y** 自己 Σ-critical；不能把原 X 當成預先已 critical。
刪點補色给 Y 的有效內點 degree≥4。若 I 是 X 的有效內點集：

`ε(X)−ε(Y)=Σ_{v∈I−I_Y}(deg_X(v)−4)+Σ_{v∈I_Y}(deg_X(v)−deg_Y(v))≥0`。

故 ε(Y)≤1。Y 繼承 T4、指定 induced disk；Q(Y) 非空時，一般 Σ-critical
前提推導给 H(Y) 非空連通，E2 全部前提滿足。E2 給 Q(Y) 空、一點或相鄰兩點。
3 與0／1皆非相鄰，所述組合不可能。這一步不需 q₂／q₄ 的角色，也不要求
X 是某列自己的 minimal core。

兩側各省略一個 unit，或省略一份 `(1,1)` mixed，若有效度數仍≥4且兩 roots
各降至4，同一推導給 ε(X)=0，其完整 Q 至多一點。這限制原省略圖，不推定它可實現。
checker 的6份 ε0／11份 ε≤1容許 masks僅算有限列身份，不代替上述紙面推導。

## 3. N1：允許經 B 的 N-empty 足夠條件

**E4-N0。** 原 degree4 mixed P 若 `N_B(P)=∅`，且 G−P 有實際 z–w 路徑 L，
則 P 延拓每份合法外部四色染色，不能含 Σ-critical contact 邊。L 可經 B；
H−P 連通只是足夠條件。

固定完整合法外染色ψ。外鄰只有z,w；同色时用V(L)一hub，異色時沿一原邊
把L切成含z/w的兩互斥連通袋，該原邊给兩袋鄰接。hub 的同色條件只在
`X_i∩N(P)`，其他 path 頂點不須同色。完整degree4拒絕lists触發原hub原則，
给 K₅ minor，矛盾。critical contact e 的 G−e 新接受染色限制到 G−P，再填完整P，
便延拓原拒絕列，同樣矛盾。

sole separating C 的 incidences(a,b)若兩者≤4，兩roots各有原C外side incidence：
spoke直接接B；unary的實際支援非空，沿原 unary 接B。兩側由B連通，適用E4-N0，
所以C實際框支援非空。若某 incidence=5，該root沒有C外因子，本補充不產生外路。
並行 canonical REPORT §2給更強的 unrestricted N-empty；本局部推導及checker
沒有假稱已從a,b≤4升成無條件版本。

90份實際合法 outside colorings／hub partitions 使用原 path z–b₀–b₁–b₂–w，
其完整framework與root色均保留；這不是 degree5／Σ-critical 正控制。

## 4. 三列 private-spoke 和 N2 精確 qcore 身份

**E4-S。** 若 root-spoke rb_i 在 q 下的色被同root另一原spoke同時禁止，
刪 rb_i 不會新接受 q：G−rb_i 的任何 q 延拓已因另一原spoke避開该色。
因此 triple-critical 要求每條spoke在至少一個指定列有自己private的框色。
T4 给spokes≤3；26個框subsets的逐格計算只排以下兩型：

| 原三spokes | 永不private的spoke | q₀同色點 | q₁同色點 | q₃同色點 |
| --- | --- | --- | --- | --- |
| 024 | rb₂ | b₄ | b₄ | b₀ |
| 124 | rb₄ | b₂ | b₂ | b₁ |

其他24個subsets沒被這條限制排除，不能把通過當成可實現。

**E4-D。** m=2 時，每指定拒絕列至多一 root 有重色spokes。只有z重色時，
每份 minimal qcore恰是G−zb_i或G−zb_j（重色pair中的一條），degrees(4,5)；
w交換角色。

m=2的root-deletions全Ω，所以所有qcores含兩roots。q-critical core不能
保留一對q-redundant原spokes。rootdegree5飽和保留全部原incidences，故重色root
必降至4；loss1若刪unary，原重色spokes仍在，所以必删一條pair中的spoke。

若兩root都有重色，core必(4,4)。兩側各省略spoke會保留兩mixed，違反
非相鄰(4,4)恰保留一mixed；省略一份(1,1)mixed則保留全部spokes，仍有redundancy。
雙重色不可能。僅一root重色時同樣排(4,4)，剩(4,5)/(5,4)，原degree4飽和和
loss1使core恰為原G减一條原spoke，不能偷換成其他小圖。

| 框pair | 指定重色列 |
| --- | --- |
| 02 | q₃ |
| 03 | q₁ |
| 13 | q₀ |
| 14 | q₃ |
| 24 | q₀、q₁ |

相鄰pair三列均異色。強制出的unit-spoke core再受E4-U限制；同一原derivative
不能跨q₃與q₀／q₁，但這沒有證明所有unit身份不存在。

## 5. N3：同一原 disk 的 K₂,m 面容量

**E4-F（不用三列身份）。** 本題原nonadjacent來源必m≤2。

m≥2時，每原mixed C_j都one-sided；原N-empty与Σ-criticality给其實際框支援非空。
在同一原disk中只作平面obstruction：把互斥完整C_j收縮成c_j，每份保留
一條實際z-contact和一條實際w-contact，删其他incidences、unaries、spokes；
保留B及原C_j–B附件。z,w,B不收縮；忽略重邊後核心恰K₂,m，且每c_j仍有框附件。
收縮只作minor必要論證，不替代原完整染色relation。

m≥2的K₂,m簡單、二連通、二分，V=m+2，E=2m，Euler給F=m。
每面邊界為簡單cycle，長度≥4；總面長2E=4m，所以每面恰四環，含z,w及
恰兩mixed vertices。B連通且與core互斥，其realization在補集單一開面F。
每條c_j–B原附件內部也走F，所以其c_j必在∂F。所有m個c_j皆有附件，
∂F卻只含兩個，故m≤2。

因此N3的單側unit(4,5)/(5,4)與原(5,5)全部同時排除，無需q₂／q₄。
33份固定quotient rotations核對m2…5四環面／每面兩mixed；任意大小涵蓋來自
上述原contraction／面論證。缺少要求的可實現nonadjacent正控制照實保留於§7。

## 6. 完整原 relation 的精確殘留

[core_constraints.json](core_constraints.json)記錄十列及全部16有序root pins的
UNKNOWN whole-fibre介面。UNKNOWN不是空fibre；未選定原圖前没有可誠實填入的
數值tuple表，沒有猜一份抽象relation然後宣稱來源可實現。

对每个原P，以固定有序distinct contacts X_P定义：

`R_P(β)={(f(x))_{x∈X_P}: f完整染色原P，滿足全部原內邊與actual P–B附件}`。

每tuple留原P的full lift，shared contact只一座標。
`R_P(β;a,b)` 保留全部tuple，只过滤各原z-contact避a、各原w-contact避b；
没有該owner的條件留空。`J_P(β)={(a,b):R_P(β;a,b)≠∅}` 是完整query的精確投影，
不可代替R_P、actual attachments、contacts和lifts，不能乘兩側marginals。

A_r(β)由自身spokes及每份原unary的整份避色tuple定義；完整同圖接合恰是
`J_G(β)=(A_z(β)×A_w(β))∩⋂_{原mixed C_j}J_Cj(β)`。
每非空fibre選原tuple與同圖lift即得完整延拓，反向限制完整延拓也得相同join。
指定三列join都空，五個T4都非空；每非框邊的triple-critical witness仍须是
G−e完整字面染色，不能拼接不同圖witnesses。

| 原分支／qcore | 完整原省略 | 本補充保留的完整 relation／限制 |
| --- | --- | --- |
| N1，單root4 | 原unary side S_z／S_w | 全拒絕列至多一例外，該側mixed incidence1 |
| N1，(4,4) | 每側各一unit side因子 | sole C全保留，incidences≤2，各(1,1),(1,2),(2,1),(2,2)；更強external mixed22排除由canonical REPORT另负责 |
| N1，(4,5)/(5,4) | 對應側一原unit | sole C全部十列R_C及16pins；E4-U限制 |
| N1，(5,5) | 無，M=G | sole C及所有side同圖complete joint |
| N2，(4,4) | 一份原(1,1)mixed，無其他省略 | 另一原mixed全保留；重色root-spoke列排除此型 |
| N2，(4,5)/(5,4) | 對應側一原unit | 兩原mixed全保留；單重色時exact原spoke omission |
| N2，(5,5) | 無，M=G | 兩原完整R_C0、R_C1共同交；任何root重色列不能採此型 |
| N3 | 全型排除 | 無 |

N1-R／N2-R停止點：完整同圖跨三列mixed transfer仍沒有uniform分類；
若繼續目前方法須逐actual support／contact key求完整relation，故依(a)在此前停下。
沒有開始這種來源枚舉。也沒有依賴q₂／q₄角色；後續若需要，按E3§3.1分開
941、933、940、932四完整mask，不能把再拒q₂當成q₄接受。

## 7. 正控制與證據缺口

只讀查看E1 k≤5已存minima/scratch代表及tracked cells代表，未見要求控制，
這不是整个k≤5來源空域。Σ951 degree6與Σ935相鄰5+5不属于本題，不能替代。
[獨立控制探查](control_probe/REPORT.md)四固定interior模板共38,500命名接法：
Split951 1000→7 disk/T4→0critical；兩K₂,₂模板10000/2500全部無disk；
K₂,₃+xy模板25000全部無disk。Split951的七張Σ1015×2、959×2、1023×3，
sole mixed兩contact均非critical；完整原圖、Σ、rotation、full accepted relation及
全部刪邊witnesses保存在其JSON，生成／普通／seed17原紀錄全exit0。

| 無指定三列中間引理 | 固定核對 | 缺少要求的nonadjacent可實現控制 |
| --- | --- | --- |
| E4-U：Σ-preserving minimalization與ε單調／E2 | 6/11份字面mask算術＋紙面前提核對 | 是 |
| E4-N0：外路可走B的hub分袋 | 90份合法outside染色與原path袋 | 是；局部圖不滿足degree5/critical |
| E4-F：K₂,m面容量與原N-empty | 33份plane quotient rotations | 是；商圖不是完整Σ-critical來源 |
| 沿用one-sided／unary盾弧 | 具名模板topology，未有critical原正控制 | 是 |

E4-S、E4-D明确使用三列身份。所有新引理是任意大小紙面證據＋固定局部Python，
不是Lean theorem。未找到正控制是CTRL-0，不能隱去，也不以有限無反例取代紙面證明。

## 8. 重播、collision 與 provenance

[本方驗證](core_validation.json)保存 generation（exclusive新的replay output）、
普通／seed17、三probe重播、check_docs、DocGraph、git diff--check及新檔whitespace的
實際exitcode／輸出。沒有還原兩已知封存missing paths：D5 scope_ledger與D2 integration diff；
照實記錄，沒有改歷史報告。沒有新增Lean，未跑lake build。

```sh
/home/ray/developer/ai/math/.venv/bin/python scripts/c5_excess_two_e4_core_constraints.py --check
PYTHONHASHSEED=17 /home/ray/developer/ai/math/.venv/bin/python scripts/c5_excess_two_e4_core_constraints.py --check
/home/ray/developer/ai/math/.venv/bin/python scripts/check_docs.py
/home/ray/developer/ai/math/.venv/bin/python tools/docgraph check
git diff --check
```

另有並行control.py/reductions.py与其兩JSON、canonical REPORT。root與控制agent
均未寫前四檔，來源不與本方合併；原bytes保持。其第一次觀察hash、當前canonical
REPORT hash及FileExistsError紀錄保存在core_validation。canonical REPORT的更強
紙面claims另由root／independent reviewer核對；本方checker有限結果不冒稱承擔那些claims。
本方沒有覆寫canonical REPORT／validation，沒有刪除並行新檔。

交付停止點：N3已證；N1／N2完整原relations與core identities仍保留，本方未全排除。
較強canonical REPORT結果需與本補充一併看其逐步proof及獨立review，不能把兩份
checker的scope或來源provenance混成同一證書。
