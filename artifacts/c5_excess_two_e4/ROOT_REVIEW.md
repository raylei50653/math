# E4：並行紙面產物的獨立複核

本檔由主稽核新增。canonical [REPORT](REPORT.md)、control.py／reductions.py
與 control.json／reductions.json 是本 worktree 執行期間由另一個並行程序新增；
本次沒有覆寫這些檔案，也不冒稱為本次代理所寫。
本檔直接複核其紙面結論，附加 [core constraints](core_constraints.json)的
獨立前提／殘留結果，來源身份與證據層分開。
本次讀取 REPORT SHA256：`a0053f874ca58322a57391abca877beb5cf26884014280fd0c328ac0d8601b74`。

## 1. unrestricted N-empty-separating（REPORT §2.1）

**Verdict：成立。** C 沒有 B 附件時，若原 G−C 中有 z–w 路（可經B），
同色一hub／異色切成相鄰兩hub。hub色常數只要求與N(C)的交集，
拒絕 degree4 lists tight與hub/Gallai給K₅；所以 C 對每份外合法染色都可接回。
任一contact邊刪後新接受的完整染色限制到G−C，再填回完整C，違反criticality。

若 G−C 不連通，因B連通、H−C分量各含z或w，至少有一個root側A完全不碰B；
另一側必碰B（原圖full B-touch，且C沒有框附件）。m≥2原H−C已連通，
所以此情形只會在sole mixed。A∪C只經另一root r接到其餘原圖，沒有其他框附件。
原G接受任一T4提供A∪C∪{r}的一份完整合法染色；將整份appendage共同S₄
改色可匹配任何外部r色。於是它能接回每份合法外染色，刪appendage任何
非框邊不改完整Σ，與原Σ-criticality矛盾。
這完成 core_constraints 的 guarded外路版本尚未使用的incidence5情形，
沒有四色定理oracle，也沒有給separating C借one-sided盾弧。

## 2. N-diagonal 局部版與 N2-short-no-unary（REPORT §4.1–4.2）

**Verdict：成立。** 局部 λ 只在 N(C) 指定色，不需能延拓成整份 G−C 染色。
若 C 的list assignment不可染，完整degree4仍使lists≥deg_C，连通slack
排除後处处tight。每個hub與N(C)的交集只有一常色，則同一C點不能有
兩鄰在同一hub，否則同色外鄰會给slack。收縮原連通hub因而保持C degree、
lists與拒絕性；外hub間的色不同，所以contracted hub clique顏色合法。
Hub／Gallai／K₅證明完全在這個contracted圖與原C lists中成立，不要求已刪
外部點原先合法染色。

原 one-sided short-support C 的 hubs 分別為框端點與
(H−C)∪框補弧；fullB-touch讓後一袋連通，原框邊／框補弧給兩兩鄰接。
同色root pins=a，若a與框兩端色不同，三hub；若等於一端色，把該端
合併到root袋，兩hub。這滿足全部局部条件，所以整個原 R_C 的 diagonal
fibres都非空，不是contact marginals拼接。

N2兩份mixed都short、無unary時，任一三色β的未用色D避全部root spokes；
沒有zw，兩roots都D合法。各原mixed diagonal fibre的完整lift可在同一β、
同一root pin接回原G，因此β被接受；与三列拒絕矛盾。
這是一份uniform整類排除，不需選per-key來源，也不讀q₂/q₄角色。

## 3. N1-22-44、N3 與 tree-H

**N1-22-44：成立。** 另由 [independent_review](independent_review.md)逐步
複核；原全degree4 core的無tails使C為四點path、兩root各保留兩spokes。
Terminal框pair若在某指定列重色，C degree-list slack且side rootdegree3
本身全收，故三列迫terminalpair是真框邊。每個whole connected side的
complement也連通，general盾弧的純拓撲證明適用；若side盾長≤2，unit-unary
的middle限制或三spoke star-face分别矛盾，故兩side各≥3，6>5。
只排原incidence(2,2)且有兩root44core，不排incidence22但三列cores全非44。

**N3：成立。** Theta原路證明與K₂,m contraction face證明一致：
B連通、與core互斥，落在一個面；m≥2時K₂,m每面4-cycle，只碰兩mixed。
原mixed整份連通及附件保留使其他mixed不能接B；與N-empty矛盾。
Contraction只用於拓撲，不替代原color relations。

**Tree-H Euler：成立。** 原degree總和4k+2與H tree給框附件2k+4，
總edges=3k+8；connected simple plane disk外面長5的上界3(k+5)−3−5=3k+7。
这是原圖限制，不可以q-core的tree替代原H。

## 4. 影響與檢查界線

上述紙面結果可採納 canonical REPORT 的部分完成：N1指定mixed22/44子類
與N2雙short無unary子類排除、N3全排除。其餘N1/N2保留完整same-graph
relation schema。額外原unit derivative／spoke身份見本次CORE_CONSTRAINTS附件。
這次沒有提出外部並行producer的來源窮盡或全repo身份證明，checker需另看
實際validation。沒有找到指定非相鄰Σ-edge-minimal正控制；所有不使用三列
的新一般引理仍缺這種realizable控制，固定局部rotation／lists不能替代它。
有限模板無控制的結果不構成一般不存在定理。沒有改原報告或commit／push。
