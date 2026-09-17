# 三個 triangle blocks 共用 cut vertex 的排除

後續狀態（2026-09-17 文件整理）：本文下一題的 [四環鏈](c5_four_triangle_chain.md)
及其 [分叉](c5_four_triangle_star.md)、[bridge 混合型](c5_shared_pair_bridge.md) 已完成。現況見 [交接](HANDOFF.md)。

2026-09-17。接續 [互斥三環](c5_three_triangle_blocks.md) 與
[兩環分類](c5_two_triangle_blocks.md)。固定 boundary C5、`q=01012`、
未用色 `D=3`，所有有效內點完整 degree=4，內部圖 H 連通，
且刪除任一非 boundary 邊後 q 可延拓。

**若 H 恰有三個 triangle blocks，其餘 blocks 都是 bridges，則不可能是
disk minimal q-obstruction。** 本輪補齊至少一對環共用 cut vertex 的情形，
不需 T4 假設，允許任意外掛樹與 bridge 連接樹。
這是紙面化約加 Python 有限證書，未新增 Lean theorem。

## 1. 連接型態與第三環的介面

共用兩個 triangle 的頂點 v 已有四個內部鄰居。因此 v 沒有 boundary
spokes、bridge 或第三個 triangle，且 `L(v)={0,1,2,3}`。
不同 blocks 不能共用兩點；block-cut incidence graph 是樹。
所以有共用點的三環只有以下兩型：

1. 恰一對共用點，第三環以 bridge path／連接樹接到這一對。
2. 三環構成共用點鏈，中間環與兩端環分別共用不同頂點 v、w。

第一型的第三環 T 沒有共用點。刪去 T 後，各外接 bridge component 互相
獨立，其中朝向另外兩環的一側可以含 cycles。每條 bridge 刪除後，兩側
root 都唯一強迫同一個色；否則可選不同色拼成原圖的 q-extension。
因此對 T 扣除各 incident bridge 的強迫色，三個剩餘二色 lists 必相等，
記為 P。若 `D∉P`，每個 T 頂點各有一個 D-forcing component。
用連通 forcer 的單點壓縮、吸收其他非 D 分量，得到兩環報告 §3 的
1,088 個 no_D minors 之一，全部非 disk。因此 `D∈P`。

取 T 上朝另兩環的第一條 bridge；其強迫色 c 不在 P，所以 c≠D。
沿這條 bridge，把 T 側整個分量吸收成母點的一條 c 色 spoke，套用
互斥三環報告 §2：得到仍全 degree-4、逐邊 minimal 的 q-obstruction，
且保留原共用點的兩個 triangles。這與兩環共用點排除矛盾。
任意長度連接路徑、Steiner 點及外掛樹均在兩環分類的範圍內。
這裡使用的是連通分量吸收，沒有把含 cycle 的分量當成兩點樹 forcer。

## 2. 共用點鏈的禁色集合

現在三個 triangles 為 `(v,a,b)`、`(v,w,x)`、`(w,c,d)`。
v、w 沒有外枝，其餘五點只可能外掛樹。扣除這些外樹 bridge 的強迫色後，
a、b、c、d、x 各剩一個二色 list。

此處「恰二色」來自 degree 與 minimality：原 `|L(u)|=deg_H(u)`；
每個 incident bridge 的強迫色必在 L(u) 且互異。否則刪去該 bridge
不能釋放母點的任何可用色，與逐邊 minimality 矛盾。
每扣除一條外枝便扣除一色，最後各點只剩所屬 triangle 的內部 degree 2。

對左端環，若 a、b 的二色 lists 不同，它可接受 v 的任意色；若兩者相同
為 P，恰好禁止 v 使用 P。右端同理。這是兩環報告的 36-case 禁色規則。

若任一端的禁色集合為空，對應共享點可用四色；另兩個中間環頂點各至少
可用兩色，先為它們選相異色，再為四色點選第三色即可。因此兩端禁色
集合都必為二色，記為 P、Q。中間 triangle 的 lists 為

```
v: 四色 \ P       w: 四色 \ Q       x: R（兩色）
```

三個二色 lists 的 triangle 不可著色，當且僅當三個 lists 全相同。
例如可由三集合的 Hall 條件直接看出：單集合至少二色，兩集合聯集至少二色，
唯一失敗是三集合聯集只有二色。所以必有

```
P = Q = 四色 \ R。
```

這也充分造成 q 不可延拓。第三環的介面因此是禁用兩色的集合，不能當作
bridge 的單一強迫色。新 checker 遍歷五個二色 lists 的全部 `6^5=7,776`
種配置，將此判準、禁色介面拼接、七點核心直接枚舉三者交叉核對；
恰有六個拒絕配置。

## 3. 外掛樹化約及有限 minors

所有 residual lists 都是 P 或 R，原始 lists 一定含 D。

- 若 `D∈R`，四個端環非共用點的 residual palette P 不含 D；每點都有
  一棵 D-forcing 外樹，保留成單點 D-forcer。其餘非 D 外枝吸收為 spokes。
  得到七個 triangle 頂點加四個 D 葉點。
- 若 `D∈P`，只有中間環的 x 必有 D-forcing 外樹；保留成一個 D 葉點，
  其餘非 D 外枝吸收。得到七個 triangle 頂點加一個 D 葉點。

這些外掛分量互相不交，可以同時操作。D-forcer 的 root 唯一可用 D，
所以它必碰到全部三個 q 色，否則交換 D 與缺失色即矛盾。收縮成一點，
每色保留一條 spoke。非 D 的 f-forcer 必碰到 f 色 boundary，
故可連同 bridge 吸收到母點，只保留一條 f 色 spoke。
此處只需 boundary 固定的 minor 性，不宣稱保持完整 relation。

化約後，共享點 lists 為四色；其餘 triangle 點的 lists 是 residual palette
加上 D；所有新增葉點 list={D}。每一缺失 q 色恰接一條 boundary spoke。
枚舉該色所有 boundary 頂點選擇，便完整覆蓋必要 minors，無同構去重。

| 中間 palette R | 內點數 | lifts | disk |
| --- | ---: | ---: | ---: |
| 含 D | 11 | 17,408 | 0 |
| 不含 D | 8 | 1,280 | 0 |
| 合計 | | **18,688** | **0** |

全部由 **54 份 K3,3 subdivisions** 覆蓋。六個 palette 配置各取一個
boundary 接線代表，獨立回溯核對所有內點 degree=4、q 不可延拓及逐非
boundary 邊刪除後可延拓。其他同色 boundary 接線具有相同 q lists，
因此這六個 controls 涵蓋所有 lifts 的 q-criticality。

## 4. 結論與邊界

§1 排除只有一對共用點的情形，§2–3 排除共用點鏈。
結合前輪的互斥三環排除，**恰三個 triangle blocks** 的全 degree-4
連通disk minimal q-obstruction 已全部排除，外掛樹大小與深度不限。

不能僅由「恰三環不存在」推出「任意環數至多二」：前輪的任意環數吸收
只涵蓋頂點互斥 triangles。末端環若經 cut vertex 相接，施加的是二色
禁集，不能直接套單 bridge 吸收。四個以上、含共用點的 block trees 仍未解。
也未處理混合較長 odd cycles、K4 blocks、degree≥5 或 `K∞=K≤5`。

## 5. 重播與下一步

[checker](../scripts/c5_shared_triangle_blocks.py)、
[證書](../artifacts/c5_shared_triangle_blocks/observations.json)。保存逐 lift 的
witness index、共用 subdivisions、枚舉 digest、六個 criticality controls、
7,776 個介面配置的重算結果、十個來源 hashes 與兩份前輪證書 hashes。
`--check` 重建所有 lifts，驗證模型路徑、內點互斥及逐例包含性，要求 JSON
逐 byte 一致；不呼叫 planarity search。無界覆蓋由 §1–3 的紙面化約承擔。

```bash
uv run --with networkx==3.5 python scripts/c5_shared_triangle_blocks.py --check
uv run --with networkx==3.5 python scripts/c5_three_triangle_blocks.py --check
uv run --with networkx==3.5 python scripts/c5_two_triangle_blocks.py --check
lake build
git diff --check
```

下一個窄問題：**四個 triangles 依序共用不同 cut vertices 的鏈**。
先推導末端二色禁集穿過下一環的 transfer，檢查是否能保留所需 minor
而縮到已排除三環；不要把二色禁集當 singleton bridge 色，也不要據此
宣稱任意 shared-cut block tree 已排除。暫不增加 bridge 路徑或外掛樹深度。

驗證通過：本輪、互斥三環與兩環 checkers，`lake build`（8,820 jobs，
僅既有 lint），README／HANDOFF／本報告的 160 個本地連結、十個來源 hashes、
兩個依賴證書 hashes 與 `git diff --check`。
本次發布一併包含本輪與前三輪的 scripts、證書、報告及 README／HANDOFF；
另補驗 cycle-5 checker。沒有背景研究程序。
