# 三個互斥 triangle blocks 的排除

後續狀態（2026-09-17 文件整理）：本文下一題的共用 cut vertex 情形已由
[共用點三環](c5_shared_triangle_blocks.md) 處理；本報告的任意環數結論仍限頂點互斥。現況見 [交接](HANDOFF.md)。

2026-09-17。接續 [兩環分類](c5_two_triangle_blocks.md)。
全 degree-4 的 disk minimal q-obstruction，若內部連通、所有非 bridge blocks
都是**頂點互斥的 triangles**，則 triangle 數至多二。
本輪先證三環排除，再由末端吸收歸納到任意有限環數。
允許任意連接樹、外掛樹與路徑長度；**尚未涵蓋 triangles 共用 cut vertex**。
這是紙面化約加有限 Python 證書，未新增 Lean theorem。

## 1. 設定及 palette

沿用固定 boundary C5、`q=01012`、未用色 `D=3`、全有效內點完整 degree=4，
以及逐非 boundary 邊刪除後可延拓 q 的 minimality。
內部圖 H 連通，triangle blocks 兩兩頂點互斥，其餘 blocks 皆 bridges。
每個內點 `D∈L(v)`、`|L(v)|=deg_H(v)`；boundary 鄰居的 q 色互異。

對任一 triangle，移除三個頂點外接 bridge components，扣掉其強迫色後，
三個剩餘二色 lists 必是共同 palette P。否則 triangle 可著色並拼回各分量。
若 P 不含 D，三個頂點各有 D-forcing component。連通 forcer 單點壓縮
不要求是樹，故即使它含其他 triangles，仍可取得兩環報告 §3 的 no_D minor。
該 1,088-lift 證書全非 disk，所以每環 `P={D,a}`。
所有直接 incident 於 triangle 的 bridge 強迫色皆非 D。

## 2. 吸收末端分量：保留 q-minimality 的版本

設內部 bridge uv 切開後，v 側連通分量 F 在固定 q 下唯一強迫 v 為 c，
且 `c≠D`。刪 uv 後兩側均可著色，u 亦唯一強迫 c。
F 必碰到 c 色 boundary，否則交換 F 內 c 與 D 即矛盾。

把 F 及 uv 收縮到 u，只保留 F 的一條 c 色 boundary spoke ub，刪除其他
從 F 帶來的 spokes。剩下的圖 G' 是 boundary 保持固定的 minor。
這次除了 minor 性，還可證固定 q 下的以下性質：

1. F 對剩餘圖的限制恰為 `u≠c`，與 ub 相同，因此 G' 仍不延拓 q。
2. u 原本沒有 c 色 spoke：刪 uv 後 u 能取 c。故新 spoke 不是重複邊；
   它取代 uv，所有保留內點的 degree 仍為 4。
3. 對 G' 的任一舊非 boundary 邊 e，取 G-e 的 q-extension 並限制到剩餘
   頂點。未刪 uv 或 F 內邊，故 v 仍取 c、u≠c，這給出 G'-e 的延拓。
4. 對新邊 ub，限制 G-uv 的 q-extension，即得 G'-ub 的延拓。

因此 G' 仍為 degree-4 disk minimal q-obstruction。此處只保存**固定 q 的
阻擋與逐邊 minimality**；沒有聲稱完整 boundary relation 或 rooted interface
等價，也沒有把含 cycle 的 F 化成兩點樹 forcer。

## 3. 三環的任意連接樹歸到兩條直接 bridges

將每個 triangle 縮為一個標記節點，得到樹。在連接三個標記的最小子樹中，
選末端標記 A。取原圖緊鄰 A、朝向另兩環的 bridge；切開後 A 側 F 只含
A 這一環及其外掛樹。其強迫色非 D，故可用 §2 吸收。

所得圖恰有另兩環 B、C，仍滿足前輪兩環分類的全部條件。因此剩餘內部圖
必恰為 B、C 及一條直接 bridge，沒有其他內點。
所以原圖 A 的鄰接點必在 B 或 C 上，A 到該環也是直接 bridge；
三環若原本透過額外 Steiner 頂點作 Y 形連接，也在這一步排除。
剩下可能的外掛樹都在剛才刪去的 A 側。

現在三環形成鏈，改對另一末端環作同一吸收。兩環分類便排除 A 側的所有
外掛樹。於是原圖恰有九個內點、三個 triangles 與兩條直接 bridges。
中間環上，兩條 bridges 只有接於**同點**或**異點**兩種標號正常形。

## 4. 九內點正常形全部非 disk

三環依序編號 `(0,1,2)`、`(3,4,5)`、`(6,7,8)`（lift 時加 5）。
其 palettes 分別 `{D,a}`、`{D,b}`、`{D,c}`；bridges 色為 x、y。
必有 `x∉{D,a,b}`、`y∉{D,b,c}`。

- 同點：bridges 為 0–3、3–6，且 x≠y。中間點 list 為 `{D,b,x,y}`。
- 異點：bridges 為 0–3、4–6，容許 x=y。

每點 list 是其 triangle palette 加 incident bridge colors。
對每個缺失 q 色，枚舉該色在 boundary 的所有鄰居選擇；每色恰一條 spoke。
這完整覆蓋 degree-4 正常形，沒有同構去重。

| 模板 | lifts | disk |
| --- | ---: | ---: |
| 中間環同點接兩條 bridges | 50,688 | 0 |
| 中間環異點接兩條 bridges | 101,440 | 0 |
| 合計 | 152,128 | 0 |

全部由 **806 份共用 Kuratowski subdivisions** 覆蓋（754 個 K3,3、52 個 K5）。
每種 palette assignment 各取一個代表，合計 72 個，獨立回溯核對 q 不可延拓、
全部內點 degree=4，以及每條非 boundary 邊刪除後可延拓。
同 palette 的 boundary 鄰居選擇具有相同 q lists；criticality 因而涵蓋所有 lifts。
沒有存活者，故不需從有限正常形再推導完整 relation。

## 5. 任意多個互斥 triangles

若有 k>3 個互斥 triangle blocks，在連接所有環的最小標記子樹取末端環，
沿緊鄰它的 bridge 吸收其一環分量。§2 保持所有假設並將環數減一。
反覆操作直到三環，與 §4 矛盾。因此這一類的 triangle 數至多二。

零／一／二環仍分別接回既有樹、單 triangle、兩 triangle 研究；
本輪沒有移除單 triangle 單缺失結論所用的 T4 假設。
本結論也不適用於共用 cut vertex、K4 blocks、混合較長 cycle blocks、
degree≥5，或一般 `K∞=K≤5` 問題。

## 6. 證書、重播及停止點

[checker](../scripts/c5_three_triangle_blocks.py)、
[證書](../artifacts/c5_three_triangle_blocks/observations.json)。
保存每個 lift 的 witness index、共用 subdivisions、枚舉 digest、72 個
criticality controls、九個來源 hashes 及前輪兩環證書 hash。
`--check` 重建所有 lifts、驗證 subdivision 的內點互斥與模型邊、逐例包含性，
並要求 JSON 逐 byte 一致；不呼叫 planarity search。
無界化約與末端吸收由 §1–3、§5 的紙面論證承擔。

```bash
uv run --with networkx==3.5 python scripts/c5_three_triangle_blocks.py --check
uv run --with networkx==3.5 python scripts/c5_two_triangle_blocks.py --check
lake build
git diff --check
```

下一個窄問題是**三個 triangle blocks 中至少一對共用 cut vertex**。
目前不能把共用 cut vertex 當作 bridge 切開，也不能直接套用本輪末端吸收。
應先建立共享頂點上的禁色集合，保留另一環的介面，再找必要 minors；
不要增加互斥 triangles 的環數、連接路徑或外掛樹深度。

驗證通過：本輪與兩環 checkers、`lake build`（8,820 jobs，僅既有 lint）、
166 個本地文件連結、九個來源 hashes、一個依賴證書 hash 及 `git diff --check`。
本輪與前兩輪產物尚未提交或推送，沒有背景研究程序。
