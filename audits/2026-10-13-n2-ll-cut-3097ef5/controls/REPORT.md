# 同一原圖完整 fibres、接回與反控制

本目錄只作固定控制；完整目標 **not triggered**。基準固定為
`3097ef5be241b7777451a5ef8a663f3987d6b866`，輸入只讀
[BASE](../BASE.json) 所封存的
[上游完整資料](../frozen/audits/2026-10-13-n2-double-long-joint/controls/observations.json)。
本輪 [checker](checker.py) 不載入或呼叫上游枚舉程式，從完整原邊另算 fibres，
再與凍結資料逐格比較。這不是完整來源枚舉，也沒有新增來源排除。

## 1. 固定原圖與完整關係

保留原 `B=(0,1,2,3,4)`、`r=5,s=6`；
`P=(7,8,9,10)`、`Q=(11,12,13,14)` 各為原 path。
P 的附件依序為 `01,0,2,12`，Q 為 `23,2,4,34`；owners 均為 `r,r,s,s`。
兩條原 spokes 是 `r0,s4`，原框邊及全部其他原邊存於
[observations](observations.json) 的 `source.original_edges`。
原 root 完整 degree 為5，其餘8個原內點完整 degree 為4，`epsilon=2`；
H 連通、二連通、full B-touch，沒有 shared 或自由孤立座標。
此固定控制的自由座標乘積因子明記為1，沒有刪去任何原座標。

使用上游十個完整字面框列，每列保持16份有序 root pins：

- 320份局部 cells，80份為空；856份局部完整 tuples。
- 160份原圖 joint cells，126份為空；181份完整原圖 lifts。
- 兩 piece 的有序 contacts、owners、實际附件、support、W、root incidences 全部保留。
- 全圖 tuple 順序固定 `(r,s,7,8,9,10,11,12,13,14)`，每列原 B 顏色另存。

局部四點用獨立 `4^4` Cartesian 枚舉；全圖另用逐原頂點 DFS，
直接選兩個 roots 及兩份 pieces。每列、同一 pins 的兩份完整 fibres 乘積
加上原 spoke 因子，逐 tuple 等於原全圖 DFS，且每個接回 lift 逐條原邊核對。
空 fibres 保留在原表位置，不壓縮成非空格列表。沒有跨列或分別換框後合併。

十列均接受，因此此控制的完整關係是1023，非933／941。
這連同下面原 K3,3 阻礙，排除了將此控制標記為合格完整來源的可能；
不以「沒有完整 target 觸發」推論來源不存在。

## 2. 基本 S 的局部正控制

S 完全由原 `W`、spokes、shared 身份算出，不加入枚舉才知道的其他接受格。
三個固定列各有以下完整 joint pins，也恰為此固定控制的 `S_P intersect S_Q`：

| 指定列 | 完整 joint pins／基本 S 重疊 |
| --- | --- |
| `q0=01212` | `(1,0),(1,1),(1,3),(2,1),(3,1)` |
| `q1=01202` | `(1,0),(2,1)` |
| `q3=01021` | `(1,2),(2,0)` |

每列兩份 `(D,D)=(3,3)` fibres 同時為空，所有上述 joint 都有原完整 lifts。
這維持既有「兩份 diagonal 皆拒，但 off-diagonal joint 存在」控制；
局部基本 S 重疊為 **triggered and holds**。
每格完整 fibres 另保存，不把 S 當作一般 piece 的完整接受表。
本目錄沒有加入 `LL-CUT+diag`。

新紙面拓撲引理另有 [不同 owners 的 K3,3](SUPPLEMENTAL_REPORT.md) 及
[沒有 root-h spoke 的同附件 K5](SAME_H_REPORT.md) 有限控制；
它們只校準原 minor，不改變本節基本 S 的定義或此固定原圖的完整 fibres。

## 3. 原 K3,3 bags、連通性與九條原跨邊

第一證書的左右 bags：

```
left:  {2,3}, {1,5,7,8}, {6}
right: {9},   {10},      {11,12,13,14}
```

按 left 與 right 的顯示順序，九條原跨邊是：

| left bag | right {9} | right {10} | right Q |
| --- | --- | --- | --- |
| `{2,3}` | `2–9` | `2–10` | `3–11` |
| `{1,5,7,8}` | `8–9` | `1–10` | `5–11` |
| `{6}` | `6–9` | `6–10` | `6–13` |

第二證書的左右 bags：

```
left:  {0,4}, {1,6,9,10}, {5}
right: {8},   {7},         {11,12,13,14}
```

九條原跨邊依同一順序為
`0–8,0–7,4–13; 8–9,1–7,6–13; 5–8,5–7,5–11`。
兩份證書逐袋提供原 spanning trees，逐項檢查 bags 非空、頂點原有且互斥、
原樹邊連通及全部九條原跨邊。沒有將強迫同／異色視為原邊。
第一份證書特意保留 `3–11`，所以其 outside attachment3 在證書中實際使用；
第二份同樣使用 outside attachment4 的 `4–13`。

此處只重新驗證上游精確 path 控制的原 minor；不從這兩份有限證書
推出任意 high-contact long 都含此 path 或此 minor。

## 4. 十項對應負控制

[觀測檔](observations.json) 逐項保留拒絕原因與需要的具體失敗 lift：

1. 從宣告原圖漏掉 `8–9`：原來源核對拒絕。
2. 漏掉 `8–9` 後多出的 tuple：成功在弱化圖染色，但接回違反原 `8–9`，逐原邊核對拒絕。
3. Q 獨立置換顏色2與3，保留兩個 root pins 並重建該外來框的完整 fibre：共同色框核對拒絕。
4. 上項跨框 tuple 直接接回原框：逐原邊核對亦拒絕。
5. P、Q 分別取不同原框列、相同 root pins：列身份核對拒絕。
6. 上項跨列 tuple 直接接回 P 列：原 `3–11` 及 `4–13` 核對拒絕。
7. 使用不同 root pins：共同 pins 核對拒絕。
8. 將原本非空的完整 fibre 改成空：完整局部關係核對拒絕。
9. 把 minor 的原跨邊換成不存在的 `2–14`：原 minor 核對拒絕。
10. 將已認證 K3,3 的圖標成合格完整來源：資格核對拒絕。

另外，驗證紀錄將產物中的一個原邊刪去，另存暫存毀損產物；
`--check --artifact` 以 `artifact mismatch` 非零退出，正式產物不改動。
容量界／矩陣固定格的負控制由本輪共同介面 checker 負責。

## 5. 實際重播與界線

```bash
python3 -B audits/2026-10-13-n2-ll-cut-3097ef5/controls/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-n2-ll-cut-3097ef5/controls/checker.py --check
```

正常／seed17 同一產物逐 byte 相符；執行前後 SHA 不變，
詳見 [verification](verification.json)。產物160,534 bytes，SHA256
`79388be85546b25d0ab616957f8462c412547c2ae1087f41bbc5f1c1acb946d5`。

完整 target 及基本 LL-CUT 的合格來源觸發數都為0，狀態 **not triggered**。
已驗證局部 S 重疊及原 minor，沒有來源枚舉、來源 rotation 實現、
新 Lean theorem、Lean build、commit、push、PR 或外部發布。
