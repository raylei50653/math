---
docgraph:
  id: c5.c4-boundary-pivot
  family: [c5, c5.minimal-source, c5.no4ct]
  related: [c5.no4ct-handoff, c5.cofacial-normal-form]
  verified_by:
    - audits/2026-10-14-c5-c4-boundary-pivot-77fbd5d/REPORT.md
    - audits/2026-10-14-c5-c4-boundary-pivot-77fbd5d/PROOF.md
    - audits/2026-10-14-c5-c4-boundary-pivot-77fbd5d/controls/check_transfer.py
    - audits/2026-10-14-c5-c4-boundary-pivot-77fbd5d/review/INDEPENDENT.md
---

# C5 換到 C4：共同拒絕列與二十二內點界

2026-10-14。**新紙面來源橋加外部完整計算結果：`K≤22=K≤5=K132`。**
全域最小目錄外來源必有至少 23 個內點，涵蓋 932／933／941 三支。
一般 `K∞=K≤5`、二十三內點以上來源排除及 Lean 化仍 **OPEN**。

2026-10-14 後續：[四連通 T／T0 化約](c5_c4_triangle_core.md)補強來源小圈限制，
將指定延拓變成 b 出口或兩個具名三角面色集合問題；無界仍 OPEN，以上有界結論不變。

完整證明、外部來源及重播見
[本輪報告](../audits/2026-10-14-c5-c4-boundary-pivot-77fbd5d/REPORT.md)；
目前停止點由 [Kempe 導覽](c5_kempe_guide.md) 維護。

## 1. 只改外框的完整來源橋

令 G 是已正規化的最小来源，有 induced 外框 `(b0,b1,b2,b3,b4)`，
內度至少五、框度至少四、全部內面三角形，且每個三角形皆界定面。
在外側加新點 u，只連 `b0,b1,b2,b4`，保留原 G 全部頂點與邊。
得到外框 `Q=(u,b2,b3,b4)` 的 H。

![C5 到具名 C4 的外側接合](../audits/2026-10-14-c5-c4-boundary-pivot-77fbd5d/diagram.svg)

H 的四種固定框色之完整延伸數為：

| Q 固定染色 | H 的延伸數 |
| --- | --- |
| ABAB | `2 x24` |
| ABAC | `y3 + x02 + x14` |
| ABCB | `y0 + y1` |
| ABCD | `y2 + y3 + y4` |

這是原完整 fibres 的不交聯集雙射，包含空 fibres；不只比較非空性。
ABCB 時原 b0、b1 必為 `(C,D)` 或 `(D,C)`，恰回到原 singleton-1／0。
三個候選都拒絕 y0、y1，故 H 禁止這種對角染色。

H 的內點是原內點加上 b0、b1，後兩者各增一度；所有內度至少五。
新三角形只有三個新面；原三角面均保留。Q 無弦，H 因此是非 diamond 的
**4-candidate**，總頂點數 `k+6`。

## 2. 已證有界結論與外部依賴

Dvořák–Lidický–Mohar，
[arXiv:2504.08327v2 §2、Table 1](https://arxiv.org/html/2504.08327v2#S2)，
報告至多 28 個總頂點的完整 4-candidate 枚舉中，只有四點 diamond 禁止對角染色。
故 H 必有 `k+6>28`，得到 `k≥23`。

若有至多 22 內點的目錄外圖，取全域最少內點、再最多邊的來源。
[no4ct 分類與度數修復](tasks/c5_no4ct_handoff.md)使它落入上述三支與前提，
與 `k≥23` 矛盾。配合 K132 的既有五內點 witnesses，得到 `K≤22=K≤5`。
不把全域最小性誤作任意固定 mask 來源的最小性。

本地化約不用四色定理；直接使用外部 §2 的生成／計算結果，沒有使用該文的
無界猜想或 one-crossing 等價定理作排除。外部 C++ 枚舉至 28、另一實作核對至 25
的信任保留，**本輪沒有重跑其十億級枚舉**。
[精確外部界線](../audits/2026-10-14-c5-c4-boundary-pivot-77fbd5d/EXTERNAL.md)
與本地有限控制分開。

## 3. 驗證與新的無界問題

主 checker 核對 132 個既有實圖的 528 份完整 C4 fibres、完整轉移矩陣、
1,024 個抽象輸入 supports 與具名負控制；另有
[獨立審查](../audits/2026-10-14-c5-c4-boundary-pivot-77fbd5d/review/INDEPENDENT.md)。
命令與實際結果見 [驗證紀錄](../audits/2026-10-14-c5-c4-boundary-pivot-77fbd5d/VERIFICATION.md)。
無新 Lean theorem；有限控制沒有真正的 932／933／941 實現。

新的窄方向是保留 **u 度四及原 b0、b1 內鄰點**的具名 C4 子類，
證其任意大小皆有 ABCB 延拓。外部一般 diagonal 猜想足夠但更強；本輪未證此無界子類。
舊 C8／W5 的拓撲結論繼續保留，新的 k≥23 不代表 RING 或私人圈秩五以上已排除。
