---
docgraph:
  id: c5.degree5-two-spoke-sectors
  family:
    - c5
    - c5.degree5
    - c5.two-spoke
  requires:
    - c5.degree5-interfaces
    - c5.single-sided-exit
---
# 唯一 degree-5 的兩-spoke 區域化約

後續（2026-09-27）：[非相鄰 two-spoke 分離](c5_two_spoke_nonadjacent.md)
已證八個非相鄰表項的指定相鄰 p 可延拓，完成唯一 degree-5 的 t=2 出口接合。
下文未解項與數字保留當輪語境；一般單側出口仍未證。

後續（2026-09-24）：[q-preserving 反射與下一相鄰 orbit](c5_two_spoke_reflection.md)
已將 S={b0,b1} 排除搬到 S={b2,b3}；六個 (2,1) 表項累計排除，尚餘四相鄰、
八非相鄰項。下一相鄰 orbit 有必要 split-support 定理及八個只缺 q 的既有
disk 控制；一般單缺失分離未證。下文數字與停止點保留當輪語境。

後續（2026-09-24）：[中間相鄰 (2,1) 排除](c5_two_spoke_middle_21.md) 已排除
S={b1,b2} 的兩種次序；palette {3} bridge／leaf odd cycle 與三個連通外部
branch sets 給同圖 K5 minor。原 18 個 (2,1) 表項累計四個排除，尚有 14 個
未分類；下文數字及停止點保留當輪語境。

後續（2026-09-24）：[相鄰 (2,1) 排除](c5_two_spoke_adjacent_21.md) 已排除
S={b0,b1} 的兩種 singleton 禁色次序，保留兩個不同分量並抽取同圖 K5 minor。
下文 18 個未解表項為當輪狀態；其餘 16 個表項未在此次續作分類。

後續（2026-09-24）：[三接點排除](c5_two_spoke_three_contacts.md) 已以同圖
palette 差與實際 boundary tethers 的 K5 minor 排除全部兩-spoke (3) 型；
尚餘 18 個 (2,1) 配置。下文 24／23 個配置及下一題保留當輪語境。

後續（2026-09-24）：[未接內點引理](c5_unattached_boundary.md) 已證 (3) 非相鄰
S={b0,b3} 型只缺 q；雙缺失目標尚餘 23 個兩-spoke 配置待分離。

2026-09-24。接續 [完整多接點介面](c5_degree5_interfaces.md) 與
[單側出口接合](c5_single_sided_exit.md)。本輪完成任意大小來源的**必要區域分類**：
80 個具名位置／禁色配置排除 56 個，留下 24 個；沒有證明留下的配置皆可實現，
也沒有完成兩-spoke 核心的單缺失分離。研究優先序見 [HANDOFF](HANDOFF.md)。

## 1. 前提與精確結論

G 是有限簡單 induced-C5 disk 圖，外框依序 b0,…,b4；有效內點誘導圖 H
連通。G 是 q=(0,1,0,1,2) 的 minimal obstruction，接受全部四色 boundary
patterns T4。唯一完整 degree-5 內點 z 恰有兩個 boundary 鄰居 S，其餘
有效內點完整 degree=4。令 U={0,1,2,3}、D=3、
A=U\q(S)={c,D}。q 下 S 的顏色互異。

每個 H−z 分量 C 使用同一張圖的全部接點 P=N(z)∩C；F_C(b) 是使 C 無法
同時避開 z 色的禁色集，定義完全沿用 R10。不可刪減覆蓋立即給出：

- 分拆 (3)：只有一個分量，F_C(q)=A。
- 分拆 (2,1)：依接點數命名 C₂、C₁，兩個禁色集是 {c}、{D}，次序有兩種。

第二項因兩個分量各有 private color、聯集恰為二元素 A，故每個禁色必為
不同 singleton；不能讓 C₂ 禁掉整個 A 而仍稱 C₁ 不可刪減。

**必要位置定理。** 以下保留 boundary 標號，不除以反射或色置換：

| 接點分拆 | S | 分量所在的閉 boundary arc | 配置數 |
| --- | --- | --- | ---: |
| (3) | 任意相鄰對，共五對 | 長 arc，含全部五個 boundary 點 | 5 |
| (3) | {b0,b3} | b0,b1,b2,b3 | 1 |
| (2,1) | 任意相鄰對，共五對 | 兩分量都在長 arc | 10 |
| (2,1) | {b1,b4} | 兩分量分居 arc (b1,b2,b3,b4) 與 (b4,b0,b1) | 4 |
| (2,1) | {b2,b4} | 兩分量分居 arc (b2,b3,b4) 與 (b4,b0,b1,b2) | 4 |

(2,1) 的計數包含 singleton 禁色的兩個次序；非相鄰型另包含兩分量交換
區域的兩個次序。其餘配置均不符合上述前提。**存活不是 disk 實現性證明。**

## 2. 同圖的區域與色交換證明

兩條 z-spokes 將 disk 分成兩區，閉包邊界各由 z 與 S 之間的一條 boundary
arc 組成。每個連通 C 不含 z 或 boundary，故全在其中一個開區域，所有
boundary attachments 都終於該閉 arc。不同分量可在同側；此時仍是不同的
連通分量，不能合併它們的接點關係。

對 C 所在 arc I，若色置換 π 滿足 `b_i=π(q_i)` 對每個 i∈I 成立，則

```
F_C(b) = π(F_C(q)).                                      (1)
```

證明是在 C 的每一個完整 coloring 上同時作用 π。所有實際 boundary
鄰居皆在 I，故這是雙射，並同時搬運全部接點是否避開 z 色的條件。
即使 I 上某些點沒有鄰接 C，要求整段 I 相容仍足以使用 (1)。它是必要
條件的保守查詢，不把 arc 上每點虛構成實際 attachment。

取 b=q，任何固定 arc 色列的置換都必保持 F_C(q)。這給**穩定子檢查**。
例如相鄰 spokes 的短 arc 只見 q(S) 的兩色，交換 c、D 保持此 arc：
(2,1) 的任一 singleton 禁色都不能在短區域，故兩分量必在長區域。

對任一 T4 列 b，只使用可由 (1) 確定的那些分量禁色，記其聯集為 K(b)。
若 `U\b(S) ⊆ K(b)`，則 b 必不延拓，與接受全部 T4 矛盾。
無相容置換的分量保持未知，不為它指定新的禁色；已知分量的聯集足以
覆蓋時才排除。這保留同圖、同一列與共同色框，沒有逐列任選抽象介面。

## 3. 有限位置覆蓋與可重播反證

十個 S 中 {b0,b2}、{b1,b3} 在 q 下同色，先由 minimality 排除。
其餘八對各有兩個區域。(3) 有 8×2=16 個配置；(2,1) 有
8×2²×2=64 個配置。這窮盡的是區域位置及已被 minimality 決定的 q 禁色，
不是窮盡圖、blocks 或實際 attachments。

| 分拆 | 穩定子矛盾 | 必拒絕 T4 | 留下 |
| --- | ---: | ---: | ---: |
| (3) | 0 | 10 | 6 |
| (2,1) | 36 | 10 | 18 |

[checker](../scripts/c5_degree5_two_spoke_sectors.py) 列舉全部 24 個色置換
與 240 個有標號 proper boundary rows。對每個排除配置，
[證書](../artifacts/c5_degree5_two_spoke_sectors/observations.json) 保存穩定子
矛盾的分量／不同像，或具體 T4 row、可用 z 色、各已知分量的置換及禁色。
checker 另直接核對這些反證等式，再與保存的 JSON 逐 byte 比對。

例如 (3)、S={b1,b4}、C 在 arc (b1,b2,b3,b4) 時，b0 未被任何內點
接觸，將 q 的 b0 改為 D 就得到仍被拒絕的 T4 列；另一區域則可改 b3。
所以這對 spokes 在 (3) 全排除，但 (2,1) 分居兩區可避免這個論證。

正控制沿用 R10 的 16 個 (2,1)、Σ=Ω\{q} disk witnesses，不生成新圖。
對每張來源圖，直接枚舉同分量的完整 colorings，核對全部 240 列的 F_C
與整圖 relation；實際 attachments 至少匹配一個留下的配置，而且每個
可匹配 arc 上的式 (1) 都成立。匹配指 boundary attachments 相容，不額外
宣稱重建了新的 embedding；disk 證據沿用來源 rotation。
證書保存來源 SHA256、原始 witness index 及匹配配置 index。

## 4. 下一個窄問題

(3) 的非相鄰分支已只剩 **S={b0,b3}、C 在 arc (b0,b1,b2,b3)**。
可在同一來源圖取區域外框

```
Γ=(z,b0,b1,b2,b3)， N_B(z)={b0,b3}， F_C(q)={2,3}。
```

這是 induced C5 disk，z 在區域中有三個不同內接點，C 仍連通且每點完整
degree=4；b4 不鄰接任何內點。區域拒絕框列 (2,0,1,0,1) 與
(3,0,1,0,1)，兩列為同一 S4 orbit。開口查詢 z=0、1 均可延拓，但與
Γ 的一條框邊衝突，須保留為刪去 z-spokes 後的查詢。

下一步可研究這個三接點區域的同圖 block palettes 與相鄰第二拒絕列。
既有雙拒絕分類要求指定框點恰兩個接點，不能直接套用到這裡。
相鄰 S 則得到六邊形長區域；(2,1) 非相鄰型是四邊形／五邊形兩區耦合。
這些型及 t≤1 尚未完成分離，不可用本輪 24 配置冒充新五目標。

## 5. 證據層與驗證

任意大小的位置限制由平面分離、R10 的不可刪減覆蓋及色置換雙射論證
承擔；位置表由 Python 固定域證書核對。本輪新推導不另用外部 Gallai 定理，
沒有新增 Lean theorem；既有 R10 與 disk witnesses 依賴保留原信任層。

```bash
python3 scripts/c5_degree5_two_spoke_sectors.py --check
uv run --with networkx==3.5 python scripts/c5_degree5_interfaces.py --check
lake build
python3 scripts/check_docs.py
git diff --check
```

本輪實際驗證與未重跑範圍見 [研究紀錄](history/2026-09-24-two-spoke-sectors.md)。
一般 degree-5、單側／共同出口及 K∞=K≤5 仍未證；603 profiles 與固定點未修改。
