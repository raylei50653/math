# 未接內點的 boundary 頂點：單缺失分離與兩-spoke 非相鄰型

2026-09-24。接續 [兩-spoke 區域化約](c5_degree5_two_spoke_sectors.md)
及 [單側出口接合](c5_single_sided_exit.md)。
**完成 (3)、S={b0,b3} 的任意大小單缺失分離**；並將條件式單側出口擴至
任何具有未接內點 boundary 頂點的 minimal core，不限制內點度數。
一般 degree-5 與一般單側出口仍未證。研究優先序見 [HANDOFF](HANDOFF.md)。

## 1. 不依賴 degree 或 disk 的改色引理

令 G 為有限簡單圖，B=(b0,…,b4) 是 induced C5，Ω 是十個 proper 四色
boundary patterns 的 S4 等價類。假設 G 接受全部四色 patterns T4。
若 v∈B 沒有 B 外的鄰居，則

```
Ω\{q_v} ⊆ Σ(G)，
```

其中 q_v 是唯一 singleton 位於 v 的三色 pattern。因此 Σ(G) 只能是
Ω 或 Ω\{q_v}。不要求 G 是 disk，不要求 minimality 或內點 degree 界。

**證明。** 取任一三色 proper boundary row b，其 singleton 不在 v。
C5 的 independent set 大小至多二，故三個色類大小恰為 2、2、1；v 的
顏色在別處仍有出現。令 D 為未使用的第四色，只將 v 改為 D 得到 b′。
b′ 仍 proper，且恰使用四色，故有 G 的延拓 f′。

保留同一份 f′ 在其餘全部頂點的顏色，只將 v 改回 b(v)。v 沒有內鄰點，
又因 B induced，其鄰居只有兩個框鄰點；b 原本 proper，故這兩條邊仍正確。
於是得到 b 的延拓。這是同圖、同一完整 coloring 的操作，沒有拼接不同列
的端點投影。全部 T4 已接受，唯一可能缺失的三色類就是 q_v，證畢。

等價地，對任何兩個 proper boundary rows，只要它們在 B\{v} 完全相同，
可延拓性便相同；內部 lists 不看 v，框邊則已由 properness 保證。
此觀察也提供獨立的有限核對方法。

**一般必要條件。** 在接受 T4 的 induced-C5 圖中：

- 若拒絕 q，至少四個 boundary 頂點有內鄰點；唯一可能未接內點者是 q 的 singleton。
- 若兩個 boundary 頂點都未接內點，則 Σ(G)=Ω。
- 若拒絕兩個不同三色 patterns，則五個 boundary 頂點都有內鄰點。

上述「有內鄰點」只說至少一條實際邊，不是 minimality、disk 實現或分離的充分條件。

## 2. 完成兩-spoke 的非相鄰三接點支

沿用兩-spoke 報告全部前提：q=01012，G 是接受 T4 的 disk minimal
q-obstruction，唯一 degree-5 點 z 有 t=2 spokes，其餘有效內點 degree=4。
分拆 (3) 表示 H−z 是連通三接點分量 C。必要位置表的非相鄰型唯一為

```
N_B(z)={b0,b3}， C 在 arc (b0,b1,b2,b3) 一側， F_C(q)={2,3}。
```

z 不鄰接 b4，C 的所有 boundary attachments 也避開 b4，因此 b4 在
整張 G 中沒有內鄰點。由 §1，Σ(G)⊇Ω\{q}；G 又拒絕 q，所以

```
Σ(G)=Ω\{q}。
```

這不只是接受兩個相鄰的第二缺失，而是接受其餘全部九個 patterns。
兩個相鄰情形可直接檢查：

| 欲延拓的三色列 p | 只改 b4 得到的 T4 列 p′ |
| --- | --- |
| 01021 | 01023 |
| 01212 | 01213 |

先取 p′ 的同圖完整 coloring，再還原 b4，即得 p 的 coloring。
不需把區域的三接點變成二接點，不需新 block palette 或外部 Gallai 定理。
來源的 z=0、1 開口查詢仍成立，但本分離證明不需查詢它們。

**範圍。** 本支被證明只缺 q，沒有證明本支不存在。前輪在 minimal q＋T4
前提下保留的 24 個必要配置仍是有效分類；加上「還拒絕第二個三色 p」的
目標前提後，此支排除，尚未分離者降為 **23 個**：
(3) 的五個相鄰 S，及 (2,1) 的十八個配置。

## 3. 擴大的條件式單側出口

令來源 G 是 Σ(G)=Ω\{p,q} 的 C5 disk 圖，p、q 為不同三色 patterns
（此項不需 singleton 相鄰）。若存在 minimal q-obstruction M=G[A]，
且 M 的某個 boundary 頂點沒有有效內鄰點，則 Ω\{q}∈W(G)。
這裡未接內點的條件在 **M 本身**計算；來源 G 可以五點都有內鄰點。

證明：M 繼承 G 的全部 T4，又拒絕 q。§1 迫使未接內點的頂點是 q 的
singleton，且 Σ(M)=Ω\{q}。按任意次序刪去 E(G)\A，過程始終含 M，
所以始終拒絕 q；取第一個接受 p 的刪邊步驟，就只釋放 p。
這沿用出口接合的 first-strict-step 論證，不是刪掉 M 的 critical edge。

故**單側出口失敗時，每一個 minimal q-obstruction 都必碰到全部五個
boundary 頂點**。它還須滿足既有的高 degree／多 degree-5／t≤2 限制。
這是附加必要條件，尚未證明任何失敗側必有未接內點的核心。
一般單側出口與共同 pivotal edge 仍開放。

## 4. 固定域證書、信任與下一步

[checker](../scripts/c5_unattached_boundary.py) 與
[證書](../artifacts/c5_unattached_boundary/observations.json) 保存：

- 全部 120 個有標號三色列，每列四個可改色頂點，共 480 份具體 T4 改色。
- 對五個 v 各核對全部 1,024 個 S4-invariant signatures，共 5,120 次；
  要求 T4 接受及 B\{v} 同一限制列的接受值相同，恰只剩 §1 的兩種 masks。
- 以 SHA256 綁定前輪區域證書；24 個保留配置中恰一個由 arc 支持範圍
  保證 b4 未接內點，保存兩個具體相鄰改色，另 23 個標為未解。

任意大小結論由 §1 的紙面改色證明承擔；抽象 signature 核對不是 disk
實現性證明。本輪不使用新外部定理、不新增 Lean theorem 或圖枚舉。
沒有改動前輪 80 配置證書、603 profiles 或固定點。

```bash
python3 scripts/c5_unattached_boundary.py --check
python3 scripts/c5_degree5_two_spoke_sectors.py --check
python3 scripts/check_docs.py
git diff --check
```

實際驗證範圍見 [研究紀錄](history/2026-09-24-unattached-boundary.md)。

下一題取 (3) 的相鄰 S={b0,b1}：C 位於長 arc (b1,b2,b3,b4,b0)，
F_C(q)={2,3}，區域框為六邊形 (z,b1,b2,b3,b4,b0)。若還拒絕第二個
三色列，全部五個 boundary 頂點必有內鄰點，尤其 b2、b3、b4 都須接 C。
須保留三個共同接點、全部實際 attachments 及同圖跨列禁色；本輪引理
不能再直接處理這個沒有空白 boundary 頂點的情形。
