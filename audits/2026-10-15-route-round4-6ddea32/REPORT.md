# 第四輪：完整 J 接回、來源兩星幾何、三標記障礙與二層共同圖

2026-10-15，BASE `6ddea32a81349821ad3724ae1652bddb9c6a7b04`。
續接[第三輪](../2026-10-15-route-round3-6ddea32/REPORT.md)，三組 subagent
並行研究並循環交叉審查。新成果只在四個獨占 audit；原十二個 audit
的388份檔案與五份權威輸入由 [BASE.json](BASE.json) 凍結。

本輪得到任意大小來源的 J 四連通與兩個原鄰弧介面、完整接回的第二個
禁止事件、三標記普通匹配失敗的窄割表，以及 Layer0 的二層共同原圖。
**完整319來源排除、ω=0、一般主命題及完成後保壞嚴格下降仍 OPEN。**

## 1. 完整 all-r 條件比單一禁止事件更強

在同一合法球面 `J=U/(s=t)` 中，令 `m=[s=t]`，以 F₂² 表示顏色，
記 `e=d(vw), f=d(pq), g=d(mz)`。對每份完整 J 染色，原 r 的 lift
唯一；原完整 all-r 表恰等價於

`(e=f) ⇔ (e=g)`。

因此不只要排第三輪的 `E₁: e=f≠g`，還必須排互斥的 `E₂: e=g≠f`。
432份 proper 六點列恰240份通過、兩個禁止事件各96份。主 agent
另逐份對比原 transfer.json，不只重寫一份局部公式。

[FULL_J_BRIDGE.md](FULL_J_BRIDGE.md) 給完整證明與117個三邊色型／
cycle-partition的精確合併表：全同或 `f=g≠e` 時，相關色對須使 f,g
同環；全異時，兩個相關色對須分別使 e,f 及 e,g 同環。任一必要
同環條件失敗，一次實際原環交換即回到禁止事件。

在同一對偶圖定義偶補匹配加權數 W110、W101，則

`|E₁(J)|=12W110`、`|E₂(J)|=12W101`。

真正來源迫兩者同時為零，尚未證任何一項為正。前輪12點控制的216份
E₁-free閉合集中仍有72份違反E₂；故該閉合不能當完整all-r閉合。
本式只是完整 U 來源在 `s=t` fibre 的必要條件，未刪去其餘 U fibres。

## 2. 六接點組：從原來源得到四連通 J 與完整 W fibre

[報告](../2026-10-15-j-source-geometry-6ddea32/REPORT.md)及
[證明](../2026-10-15-j-source-geometry-6ddea32/PROOF.md)利用原 rotation
及小 C5 定理，證 s/t 鄰集間唯一跨邊是 vw。因此 J 的每個三角形
都是面，J 四連通。進一步得到：

- `d_J(m)=d_G(s)+d_G(t)−5≥7`，`d_J(z)=h+3≥6`；僅v,w,p,q可能四度。
- induced C4 必經m或z；避兩者的induced C5有一側是保留的原五度W5。
- 刪m,z得到實際三角化disk W，外圈為兩條原link路徑，長至少9；
  α=p、β=q等端點相等情況保留原身份。

對同一份完整 W 染色χ，兩路徑缺色集合為Am、Az，所有 J lifts
恰為 `Am×Az` 去掉對角，空fibre照樣保留。由完整接回式得到新定理：

**每份完整來源 W 染色都滿足 `|Am|=|Az|=2 ⇒ Am=Az`。**

若兩個二色集合不同，三份合法hub lifts恰讓g取遍三個非零值；其中
恰一份違規。尚未證來源 W 必有這類染色。四份局部patch只校準全部
纖維與端點身份；它們不是原來源。完成後成本仍為
`(k−3)+2+1+5=k+5`，故沒有以刪點本身聲稱嚴格下降。

## 3. 匹配組：二入一出普通匹配的精確障礙

[報告](../2026-10-15-three-edge-matchings-6ddea32/REPORT.md)及
[證明](../2026-10-15-three-edge-matchings-6ddea32/PROOF.md)將110／101
兩族各精確化成 `H=J*−X−h` 的普通PM，其中X是兩條強制邊的四端點，
h是禁止邊。原來源令兩組強制邊均為induced matching；J四連通令
J*的全部3割皆單點割。

用明列外部輸入 Tutte 1-factor theorem，若普通PM不存在，可選
最大刪點障礙S，使全部剩餘分量奇階、factor-critical，且

`q=|S|+2`，

`Σ_C (|δ(C)|−3)/2 + |E(S)| + |E(S,X)| = 1+τ ≤2`。

因此非單點分量只能是：沒有、一個5割、兩個5割、或一個7割。
對偶圈避m,z的5割還被原小圈條件定位成原五度W5的對偶C5。這是完整
普通失敗障礙的結構限制，尚未排除表中所有來源實現。

四份控制保留87份全部PM、262784份Tutte刪點集與完整Tait fibres
（含奇補空fibre）。前三張原J控制的 `(W110,W101)` 分別為
`(2,6)、(8,6)、(0,2)`。Petersen僅校準非平面的普通失敗，不能作
來源反例。**普通PM非空仍不能推出偶補PM非空。**

## 4. Kempe組：允許二層後已有完整共同原圖

[報告](../2026-10-15-kempe-state-covers-6ddea32/REPORT.md)及
[證明](../2026-10-15-kempe-state-covers-6ddea32/PROOF.md)研究hidden-state
covers，接續第三輪single-valued section的障礙。

在固定 Layer0 的432個literal states上，二層cover已有共同原圖：
75點353邊與121點711邊兩份具名見證。每張圖的**全部**四色染色
恰為864份，逐份二對一投影到432態；六色對的原分量及交換在同一
張圖中實現，沒有用獨立路徑代替共同圖。七個具名接點均為不同原點。
75點圖還有六步可見交換閉路，回到同一base state卻翻轉sheet；故無
交換相容的單值section。這給二層共同圖與單值lift差異的直接見證。

另有任意有限圖的hidden分量界：同一literal接點色列的完整染色數至少
為三個互補色對之 `2^(hidden分量數)` 總和減2。此界不能不加條件地
套到跨layer表的一個state fibre。固定完整720表的抽象二層visible-cube／
S4 covers有 `2^117` 個gauge類；加上每色對可見交換乘積等於全域換色
的額外限制後為 `2^13`。這些是抽象cover類數，並非共同圖或來源數。

主 agent 對121點見證另寫 [check_cover_graph.py](check_cover_graph.py)，
不用原組程式，從原邊重枚全部染色、8160次分量交換與26112份整個
cube；完整集合與投影逐份相同，見
[cover-graph-independent.json](cover-graph-independent.json)。

兩圖均非平面；這只描述兩份具體見證，**不排除其他平面實現或平面
子圖**。結果限Layer0，還沒有完整720態共同圖，更沒有原最小來源。
完整共同圖與single-valued section是不同義務，二層見證不推翻前輪
section障礙，也不把一般cover縮成可任選一份lift。

## 5. 驗證、採納與剩餘義務

完整命令、正常／seed17重播、損壞證書拒絕與循環交叉審查見
[VERIFICATION.md](VERIFICATION.md)。主 agent 另核完整all-r原表與
共同原圖，數字由有限證書支持；任意大小來源幾何與匹配障礙由紙面
證明支持，沒有新增Lean或使用4CT。

[check_bundle.py](check_bundle.py)核舊388份內容及成員集合、五份權威
輸入、HEAD／tracked diff、新檔語法與本地連結；最終收據
[bundle-check.json](bundle-check.json)，本輪封存[MANIFEST.json](MANIFEST.json)。
尚未commit／push。

接下來的具體缺口是：用原兩star與短圈幾何，迫一份違規完整 W lift；
或排三標記普通障礙並證偶補正計數；或把Layer0共同cover接上其餘狀態
與平面原來源約束。控制上的成功或非平面見證本身均未完成這三件事。
