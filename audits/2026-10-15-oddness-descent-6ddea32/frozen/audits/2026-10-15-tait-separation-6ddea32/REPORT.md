# T/T0 的指定邊普通匹配分離已證；偶補障礙保留

2026-10-15，凍結 BASE `6ddea32a81349821ad3724ae1652bddb9c6a7b04`。
本輪只寫本獨占 audit；未改共享 docs、歷史證書、其他 audit，未 commit／push。

**本輪得到任意大小的來源推論：合法 T/T0 的兩條指定對偶邊，必有普通
完美匹配恰含其中一條，而且兩個方向各有一份。** 因而 constrained
oddness 的 `ω=∞` 分支已排除；`ω=0`、一般指定 Tait 延拓及
`K∞=K≤5` 仍 OPEN。一般 `K≤22=K≤5` 與來源 `k≥23` 不變。

## 1. 可採納的定理

**平面版本。** T* 為四連通簡單球面三角化圖；a1,a2 是兩條互不相交
具名原邊，四端點之外每點度數至少5。令 Q 為原 embedding 對偶，
`e=a1^∨, f=a2^∨`。則存在完美匹配 M1,M2，使

\[
e\in M_1,\ f\notin M_1,\qquad f\in M_2,\ e\notin M_2.
\]

兩份匹配是分別存在的 witnesses；沒有把它們合併成同一份匹配或染色。
完整證明見 [PROOF](PROOF.md)，根據如下：

1. Edmonds 的普通 matching polytope 定理，在 cubic、3-edge-connected、
   無非平凡3-edge cut 的域，推出普通 PM convex hull 的 affine hull
   僅由各頂點 incident sum=1 決定。
2. 若所有 PM 都令 e、f 的指標相同，線性代數迫 `Q−{e,f}` 為連通二分圖，
   且 e、f 各在相反 parts 內部；反向亦成立。這是精確的普通互依例外。
3. 原圖 Euler 曲率12，加上四端點最多貢獻8，迫至少四個端點外五度點。
   其中任一對偶五邊面都避 e,f，排除上述二分例外。

證明使用的外部定理是 [Edmonds 1965 原文 p.126 Theorem (P)](https://nvlpubs.nist.gov/nistpubs/jres/69B/jresv69Bn1-2p125_A1b.pdf)。
PM face、odd-cut 形式、雙向微擾、互依分類與 Euler 接回均在本輪寫出。
沒有使用四色定理、外部圖全集或外部圖生成器。

## 2. 與原來源的精確對應

| 原來源 | T* | 指定原邊 | 已證來源事實 |
| --- | --- | --- | --- |
| `d_G(b)≥5` | T | xy、zb | 四連通；端點外每點至少五度 |
| `d_G(b)=4` | T0 | xy、pq | 四連通；端點外 z至少六度，其餘至少五度 |

來源事實由凍結的原 [T/T0 證明](../2026-10-14-c4-triangle-core-b66f592/PROOF.md)
§§2、4、5供應；全部原圖、具名接點、原 rotation、色框、空 fibres 及
完整染色雙射原樣沿用。從度數後果推出匹配存在，不反稱任意這種三角化圖
都能由完整最小 C5 來源實現。

T 支另有強化：z≥7，而 x,y,b≥4，其他點≥5，Euler 迫至少七個
四特點外五度點。因此 **T 對偶的任意兩條不同邊**都能被普通匹配雙向
分離。T0 的本輪聲明仍限原 xy、pq 的具名邊對。

## 3. 精確剩餘義務

定義

\[
\omega_{e,f}(Q)=\min_{M\text{ perfect},\ |M\cap\{e,f\}|=1}
\#\{Q-M\text{ 中的奇環}\},\quad\min\varnothing=\infty.
\]

本輪已證合法來源 `ω<∞`；cubic 補圖是2-factor且圖階為偶數，故
`ω∈{0,2,4,…}`。原 Tait 判準所需的是 **ω=0**，尚未證明。

普通 PM polytope 的 affine hull 不能直接搬到偶補 PM 的凸包。Petersen
有限控制全部六份 PM 都有兩個奇五環，且全部105個邊對可普通分離，
所以逐對 ω=2。它非平面，只校準普通結論的邏輯範圍，不是來源反例。

在合法來源中，普通殘圖 `Q−V(e)−f` 及 `Q−V(f)−e` 都已有完美匹配，
所以「先找普通匹配 Tutte 障礙」已不是剩餘研究任務。
下一個窄問題是：來源是否排除 **偶補 PM 全部互依，而普通 PM 不互依**？
等價地，保留指定邊分離時能否消除正偶數個奇補環。

同輪 [雙切割／匹配橋](../2026-10-15-route-research-6ddea32/CUT_BRIDGE.md)
另給同圖的表示：普通匹配對應每三角非單色的二元切割；偶補進一步要求
兩個同側 induced 圖都二分。該橋的證明及控制由其作者獨立維護。

## 4. 有限證據及反控制

本輪只算以下六張具名小圖的完整 PM，沒有啟動來源全集枚舉。
證書 [controls.json](controls.json) 保存完整邊表、每份 PM、每份補環、
全部邊對的兩方向 PM 索引、二分例外與 ω，以及所有大小至多3的 cut。
正二十面體對偶另保存原具名面、完整 coherent orientation、逐邊對偶身份
與 `(z,x,y,b)=(0,2,3,5)`；沒有逐列獨立改色框。

| 控制 | 全部PM | 偶補PM | 互依邊對 | 角色 |
| --- | ---: | ---: | ---: | --- |
| K4 | 3 | 3 | 3 | 對邊二分例外；沒有2割仍可互依 |
| cube | 9 | 9 | 0 | 二分 cubic 的正控制 |
| 三角柱 | 4 | 3 | 3 | 有非平凡3割，Lemma A不觸發 |
| 五角柱 | 11 | 10 | 5 | 無非平凡3割仍有二分例外 |
| Petersen | 6 | 0 | 0 | 非平面；全部邊對ω=2 |
| 正二十面體對偶 | 36 | 30 | 0 | 具名位置正控制；全部邊對可普通分離 |

共69份 PM、762個邊對。五圖符合 Lemma A 的域，對其726個邊對完整
核對 Theorem B；三角柱36對只作對照，未套用域外定理。
普通 PM 列表另以獨立 vertex-subset DP 計數核對完整性；直接核每份 PM
確覆蓋全部點恰一次，補圖確為全體環。以有理數 Gaussian elimination
核五圖 PM affine rank 等於 `|E|−rank A`。

Coverage labels：Lemma A/B 的五圖為 `triggered and holds`；三角柱為
`not triggered`。K4／五角柱是「只靠連通與3割就可分離」的反控制；
Petersen 是「普通分離就有偶補」在一般 cubic 域的 `counterexample`。
**真正全域最小 C5 來源：0，source realization `not triggered`。**

## 5. 驗證與權限

[check_controls.py](check_controls.py) 僅用 Python 標準函式庫。
`--check` 完整重建並逐字比較整份證書，拒絕缺漏或多餘內容；`--write`
使用 exclusive-create，既有證書不覆寫。沒有接受弱化 `--source` 的介面。
凍結輸入及其目前原檔 SHA256 全部逐次核對，drift=0。

```sh
python3 -B audits/2026-10-15-tait-separation-6ddea32/check_controls.py --check audits/2026-10-15-tait-separation-6ddea32/controls.json
PYTHONHASHSEED=17 python3 -B audits/2026-10-15-tait-separation-6ddea32/check_controls.py --check audits/2026-10-15-tait-separation-6ddea32/controls.json
python3 -B audits/2026-10-15-tait-separation-6ddea32/check_controls.py --check audits/2026-10-15-tait-separation-6ddea32/negative/controls-one-matching-omitted.json
```

前兩項 exit0且輸出相同；第三項刻意從K4刪去一份匹配，應且實際 exit1。
正常／seed17／負控制各約0.19秒；命令、時間、exit與hash見
[VERIFICATION.json](VERIFICATION.json) 和 [logs](logs/)。Python AST parse通過。
根整合者已獨立紙面審閱 PROOF 的 polytope、量詞、對偶與 Euler 推論；
採納範圍仍以本輪明列命題為限。

Closure scope：合法 T/T0 指定邊普通 PM 不存在的 `ω=∞` 分支。
Remaining OPEN：`ω=0`、完整來源指定 Tait 延拓、無界 mask319、一般K∞。
無新增 Lean theorem；未把本有限控制當作無界證明；未 commit／push。
