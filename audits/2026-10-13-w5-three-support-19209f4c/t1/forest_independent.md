# 私人 forest 排除：獨立紙面及完整染色審查

2026-10-13。審查父包的 [`forest/check.py`](../forest/check.py) 所編碼的來源
分類。結論 **PASS**：在凍結最小來源前提下，若全內部 W5 外的私人圖是
forest，則來源落在明列的 70 個模板的具名重標記中；70 個模板補回中心後
均接受全部十個外框列。因此該 forest 條件與最小目錄外身份矛盾。

這個普遍結論需要下面的紙面覆蓋證明，並不由 70 圖搜尋的數量自行推出。
原實際 933／941 最小來源仍未構造，標為 `not triggered`。

## 1. 來源前提與 ring 附件界

使用凍結來源提供的全域最小性正規形：`k≥13`、原內點度數至少 5、原 B
為 chordless C5、全內面三角化、没有 occupied C3，且每個 C4 有界內部
沒有頂點。固定任何全內部五輪 `(v,U)`，其中 U 為 induced C5，內盤只有 v。

令 `F=G−(B∪U∪{v})`，假設 F 為 forest，記私人點數 r、分量數 c。
由 `k≥13` 得 `r=k−6≥7`。每個私人點的鄰點均屬 F、B 或 U；v 的鄰點
恰是 U，因此沒有私人點至 v 的邊。

凍結來源已證每個原內點在 B 上至多有兩個鄰點，若兩個則相鄰。
對 U 亦成立：若 x∈F 同時接 U 上不相鄰的 ui、uj，則
`ui−v−uj−x−ui` 是簡單 C4。其在 U 內的兩條 spokes 與在 U 外的兩條
x-edges 合成 Jordan 環，U 的兩個 ui–uj 開弧分處環的兩側。非相鄰性
使兩開弧都含 U 頂點，故該 C4 的有界側有頂點，矛盾。
所以每個私人點在每一環最多兩個、且是相鄰的鄰點。

## 2. Euler 與面計數

記 p 為 B–U 邊數，t 為 `(B∪U)–F` 邊數，a 為 annulus 中只含 B/U
頂點的三角面數，M 為一點來自 B、一點來自 U、一點來自 F 的三角面數。

原圖有 `r+11` 點，disk 三角化給 `E=3r+25`。已知 B、U、中心 spokes
共 15 邊，F 有 `r−c` 邊，所以

\[
t=2r+10+c-p,\qquad
\sum_{x\in F}\deg_G(x)=2(r-c)+t=4r+10-c-p.
\]

私人點至少五度，故

\[
r\le 10-c-p. \tag{1}
\]

annulus 有 `2r+10` 个三角面。因 F 為 forest，含兩個私人點的三角面
恰有 `2(r−c)` 个：每條 F 邊兩側各一面，第三點都是 terminal。
只含 B/U 的三角面恰有一條 B 或 U 的環邊；沒有 BBB 或 UUU 三角面。
因此一個私人點加兩個同環 terminal 的面恰有 `10−a` 個。故

\[
2r+10=2(r-c)+(10-a)+a+M,
\qquad M=2c.
\]

再數 B–U 邊兩側：每個只含 terminal 的面使用兩條 B–U 邊，每個 M 面
使用一條；其餘面不使用。得到

\[
2p=2a+M,\qquad p=c+a\ge c. \tag{2}
\]

這些都是原嵌入中的面計數，不需要添加 edge-critical 或 Gallai 身份。

## 3. 每個分量必為 path，且只剩三組參數

F 無孤立點：否則其原 degree 至多 `2+2=4`。每個私人 leaf 的唯一私人
鄰點，加每環至多兩個附件，以及 degree≥5，一起迫使它恰有
`1 F + 2 B + 2 U` 個鄰點。

此 leaf 的兩個 B 鄰點在其原 rotation 中相鄰，兩個 U 鄰點也相鄰。
理由：這兩對各自有一條原環邊；若該邊跨過 leaf link 中的其他鄰點，則
它與 leaf 形成的 C3 兩側都含鄰點，違反沒有 occupied C3。因此 leaf
刪去唯一私人鄰點後，其 terminal link 是兩個相鄰 pairs 接成的四點鏈，
恰有一個 B/U 轉換，亦即恰有一個 M 面。

每個非平凡 tree 至少兩個 leaves，所以 M 至少 `2c`；而上節已證等號。
因此每分量恰有兩個 leaves，亦即每分量是 path。所有 M 面都由這些
endpoints 貢獻，任何 private internal path vertex 都沒有 M 面。

由 (1)、(2) 與 `r≥7` 得

\[
7\le r\le10-2c,
\]

故 `c=1`。再用 `r≤9−p`、`p≥1`，只剩

\[
(r,p,a)=(8,1,0),\ (7,1,0),\ (7,2,1).
\]

此步把所有可能大的 forest 來源先紙面壓到 `r≤8`；有限枚舉沒有假定一個
任意截斷半徑。

## 4. Path 的兩側與 70 個 word 的完備性

沿唯一 private path 定向。每條 private edge 的兩側各有一個 terminal
third vertex。在 internal path vertex 的 link 中，兩條 private edges
把其 terminal 鄰點分成两段。因該點沒有 M 面，每段全屬同一環；沿 path
同一側的環類型保持不變。endpoint 的唯一 M 面表明兩側分屬 B、U。
故整條 path 的兩側恰是一側 B、一側 U。

每個私人點在每環有一個或兩個連續鄰點，故可編碼為在兩側環上走過的
環邊數 `(db,du)∈{0,1}²`。endpoint 恰為 `(1,1)`。internal path vertex
有兩個私人鄰點且原 degree≥5，故 `(0,0)` 不可，餘下三種 steps：

```
(1,0), (0,1), (1,1).
```

此處沒有漏掉回頭或跳接：每一個所走環邊的三角面在原環的 annulus 側，
由固定面方向決定前進方向；同一環邊不可能供應兩個 annular 面。
沿一側連續走過的 terminal fan 不會跳過環邊。所有環邊恰由某私人點的
fan 或僅 terminal 的三角面使用，故步數總和精確如下。

| 原參數 | 兩個 endpoint 之外的 step 多重集 | word 數 |
| --- | --- | ---: |
| `r=8,p=1,a=0` | `3×(1,0),3×(0,1)` | 20 |
| `r=7,p=1,a=0` | `2×(1,0),2×(0,1),1×(1,1)` | 30 |
| `r=7,p=2,a=1`，terminal 面為 BBU | `2×(1,0),3×(0,1)` | 10 |
| `r=7,p=2,a=1`，terminal 面為 BUU | `3×(1,0),2×(0,1)` | 10 |

p=1 時兩個 ring 都有五條邊由 path fans 使用；p=2 時唯一 terminal 面
消耗 B 或 U 的一條環邊。上表因而無其他參數、step 種類或順序。
不同 words 可能給同構圖；本分類只需要覆蓋，不要求同構去重。

父 generator 固定：p=1 時從 `b0u0` 開始並回到同一 B–U 邊；BBU case
把唯一 terminal 面取為 `b0b1u0`，從 `b1u0` 開始；BUU case 把唯一
terminal 面取為 `b0u1u0`，從 `b0u1` 開始。這三種 cut 開的 annulus
槽位，都由上述兩側 fans 與起訖 mixed faces 唯一填滿。

## 5. 原 labels、rotation 與 full lifts 的對照

從 canonical template 回到實際來源，保存如下顯式映射：

\[
g_B(i)=s_B+\varepsilon i\pmod5,\qquad
g_U(i)=s_U+\varepsilon i\pmod5,
\qquad \varepsilon\in\{1,-1\}.
\]

B、U 可各自選循環起點；orientation 的 sign 必須共用。只反轉一個環
不保持 annulus 的相對方向，不能當作自由 normalization。private vertices
按原 path 順序逐點對應，必要時整條 path 反向；中心回到原 v。
它是整張原圖的一份具名嵌入同構，所有原 attachments、edge ownership、
rotation 都由此搬回，並不只比較外框 masks。

若取原 β，先依 `g_B` 把五個實際色名搬到模板，不獨立更名 U；必要時再對
**整份染色共同**作一次色名標準化以查十列證書。由 template 全 lift 經
同一 label map 與色名逆置換返回原圖。這給原圖與其實際模板的完整雙向
染色 bijection。證書同時保存 U 的具名 cells 與所有空 fibres。

70 個補中心模板的 Σ 全為 1023，故不論 B 的起點和方向如何，其完整 Σ
仍為 1023。結論甚至不需要使用 catalogue 對 D5 的封閉；只用 `1023∈K`。

## 6. 獨立完整重算

[`forest_independent.py`](forest_independent.py) 不 import 主程式，使用三項
不同的實作選擇：

1. 用三種 letters 的全部 `3^5` 或 `3^6` words 按步數總和過濾；不使用
   主程式的多重集 permutations。獨立得到 `20+30+10+10=70` 個 keys，
   與主證書集合精確相同。
2. 依每個私人點在 B/U 上的 neighbor intervals 加邊；不由主程式的 faces
   取 edges。每份原 annulus literal edge set 與主證書精確相同。
3. 對 H 和完整 G 各自直接做 fixed-order DFS。G 的實際 center 參與 DFS，
   不由 H 染色的 U 色數篩選。逐份比較全部 H fibres 和全部 G full lifts。

實際執行：

```bash
python3 -B audits/2026-10-13-w5-three-support-19209f4c/t1/forest_independent.py
```

結果：

| 獨立核對 | 數目／結果 |
| --- | ---: |
| 模板 | 70 |
| 完整 H cells | 716,800 |
| 空 cells | 701,956 |
| H full lifts | 18,282 |
| G full lifts | 9,308 |
| G 的 Σ | 全部 70 份恰為 1023 |
| 與主證書的 edges、cells、full lifts | 全部逐份相等 |
| 132 關係的 10 個具名 D5 變換 | 1,320 項全在 K；此額外核對不是排除的必要依賴 |

所以：**任一滿足凍結最小来源前提的全內部 W5，其私人補圖 F 不可能是
forest，必含 cycle。** 此結論涵蓋任意選取的該類 W5，因為前述證明未對
W5 再加特殊選擇條件。

它沒有排除含 cycle 的私人補圖，沒有把代表私人圖也限制為 forest，沒有
構造一般 `r≤6` annulus 代表，亦沒有宣稱 `K∞=K≤5` 或新增 Lean theorem。
