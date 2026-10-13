# N2-BRIDGE controls：實際原圖與 mask-free U4 末端

本目錄只讀既存原圖／marked core 資料，重新核對同一有序
`B=(0,1,2,3,4)`。未搜尋新來源，不改舊證書。所有 full lifts 都使用
各筆保存的 `vertices`／`coloring_vertex_order`；完整十列順序保存於 JSON，
不獨立正規化框、core、分量或 roots。

## 1. 實際平面圖：criticality 與 Z 的前提不能任意刪除

[graphs.json](graphs.json) 保存兩張固定原圖、原邊、原 rotation 及加外 apex 的
rotation、degree、effective H、原 roots、實際分量附件、十列全部 root fibres
（16 格，含空格），以及每格的**全部完整染色**。原圖每條非框邊刪除、每份
minimal q-core 及其逐邊刪除都保存相同完整資料。沒有只保存逐 root marginal。

| 圖 | 完整 Σ | 原內 degree | Q | Z | 用途及狀態 |
| --- | ---: | --- | --- | --- | --- |
| SIGMA956-AD3 | 956 | 5、5、4 | {0,3,4} | {0,3,4} | 刪除 Z 前提之反控制：counterexample |
| SIGMA1013-NA6 | 1013 | 5、5、4、4、4、4 | {2,3} | ∅ | `|Z|≤1 ⇒ 真子圖至多單拒絕`：triggered and holds |

兩圖均為有限簡單 induced C5 disk，T4 全收、每條非框邊 Σ-critical、ε=2。
Σ956 的 roots 5、6 相鄰；Σ1013 的 roots 5、6 非相鄰。**兩圖均未拒絕
canonical q0、q1、q3，故廣義 N2 完整目標均為 not triggered。**
這個標籤不提供任何來源排除。

Σ956 的原非框邊為 `06,16,17,25,27,35,45,46,56,57,67`，內 H 是 triangle
`56,57,67`。刪 `45` 得 Σ958、Q={0,4}；刪 `46` 得 Σ1020、Q={3,4}。
因此它實際反駁的是：

> 每個 T4 全收、Σ-edge-critical、ε=2 的 disk G，其每個保 B 真子圖都至多拒絕一個 singleton 列。

此命題缺少 `|Z(G)|≤1`。原 arc-pair 定理仍成立。

同一圖也反駁下述**較弱指定集**的無條件 criticality 推廣：

> 對任意非空 S⊆Q(G)，若每條非框邊 Σ-critical，則每條非框邊都釋放 S 中某列。

取 `S={0,4}`，刪 `45` 只釋放 q3，S 中兩列仍拒絕。新接受 q3 的同列完整
染色之一為 `[0,1,0,2,1,1,2,3]`，頂點順序0至7。此控制**不反駁** E3 的
指定非連續三列 triple-critical 化約；三列、ε 與 minimal-core 理由不能省掉。

Independent checker 在這兩張固定原圖內以拒絕保留的原邊刪除 DFS **窮盡**
minimal cores：Σ956 六份、Σ1013 兩份；與既有 core 清單逐字面原邊相符。
因此本控制的 Z 不再僅靠舊清單完備性；窮盡範圍僅這兩張原圖的子圖。
29 份原圖單邊刪除、86 份 core minimality 刪除、242 個不同完整十列染色查詢
均通過；同一原 rotation 的 darts 面遍歷給 Euler characteristic 2，原 B 確為面。

## 2. Mask-free U4：同列完整 pin 碰撞

[u4_mask_free.json](u4_mask_free.json) 對原 U4 828 份 marked necessary cores
逐一重算全部十列，程式**不讀取 target masks 或 target comparisons**。
保存每份字面原邊、原 root 次序、完整 port 次序、全部 joint tuples、16 root fibres
及全部 full lifts。這次獨立 numeric-order DFS 不 import 舊 producer、舊 auditor、
frontier DP 或任何圖搜尋器。

核對結果：

- 828 份 cores × 10 列 = 8,280 份完整關係。
- normalized core 拒絕列是 q4=`01012`，其 fibre 為空；其他九列皆接受。
- 828 × 4 = 3,312 份其他 T3 列，都有兩個不同 root pins 共用同一座標；
  每份碰撞附兩份同列、同一原 core 的 full lifts。
- 132,480 格 fibres = 102,536 空格 + 29,944 非空格。
- 98,096 份舊 full witnesses 逐原邊驗證；新 DFS 枚舉 122,240 份全部 full lifts。
- 15,460 份 q-minimality 原邊刪除 witnesses 逐字面原圖驗證。

這是與完整 Σ 無關的有限末端驗證。任意大小來源涵蓋、標記 roots 的長路
縮減與完整共同座標傳遞仍由原 U4 紙面 §2–3 負責；這裡不把828份資料本身
當成任意大小分類證明。normalized q4 是整圖共同色框選擇；將其他 q-core
接入定理時必須共同搬運全部原資料，再逆搬回原 B。

## 3. U4 接回只保 T3，不能加強為十列相等

[u4_t3_negative.json](u4_t3_negative.json) 重新核對既有實際原圖
`U4-SHORT-NEAR-1018`：roots 次序是 `[8,7]`，原 G 有11點、24邊，ε=2，
兩 roots 非相鄰，19條非框邊均對完整 Σ critical。保存原 B、原邊、rotation、
全部十列 fibres/full lifts、19份原邊刪除的完整關係。

其 `Σ(M)=1022`、`Σ(G)=1018`，兩者 singleton 拒絕集均為 `{4}`；但 T4 列
`01023` 在 M 接受、G 拒絕。因此：

- omitted-mixed11 的 T3 保持：**triggered and holds**。
- 將該保持加強成完整十列 Σ(G)=Σ(M)：**counterexample**。
- T4 全收來源、canonical 廣義 N2／E-ARC2 來源：**not triggered**。

此圖的 counterexample 僅針對上列更強恢復命題，不能稱為一般 N2 或 E-ARC2 反例。

## 4. 重播與負控制

在 repository root 執行：

```bash
python3 audits/2026-10-13-n2-bridge-243a125/independent_checker.py --check --negative-tests
python3 audits/2026-10-13-n2-bridge-243a125/independent_checker.py --u4 --check --negative-tests
python3 audits/2026-10-13-n2-bridge-243a125/independent_checker.py --u4-t3-negative --check
```

`--generate` 只以 exclusive create 建立新產物；既存產物不覆寫。普通 `--check`
只讀資料，重新計算並比對。再以 `PYTHONHASHSEED=17` 重播得到相同 bytes。

實際控制的八份 semantic corruption 均被拒絕：捏造 selected-critical、刪掉 Z、
漏空 fibre、破坏原56邊的 full lift、獨立重排 B、交換 rotation、把 not triggered
升格成排除、任意改 q2 接受。U4另拒絕破坏原邊的碰撞 full lift、獨立改 root pin
及漏掉第16格 fibre。負控制作用是防止證據欄位被靜默放寬；不是來源存在性搜尋。

## 5. 獨立框列算術

[boundary_arithmetic.json](boundary_arithmetic.json) 窮舉32個全收T4的十列mask，
直接核得 q0/q1/q3 同拒只容許 `932,933,940,941`。它也獨立核对任四q列的
五個vertex signatures及五個原框邊color-pair signatures均互異；非相鄰框點
對各在恰好兩個q列同色。E原域 `1≤|Q|≤4` 中不在連續三點弧內的Q，恰為
933／941的整框D5像。i↦1−i的同一整框反射將940搬至933。此為有限框列
算術，不是圖來源存在性或 arbitrary-size theorem 的替代。

```bash
python3 audits/2026-10-13-n2-bridge-243a125/independent_checker.py --arithmetic --check
```

U4及U4實際控制讀取本audit `frozen/` 內封存輸入，其hash與`U4_INPUTS.json`
吻合；產物仍保留原來源路徑作provenance。四個模式各用seed0及seed17重播，
8次exit0，stdout逐模式一致，紀錄見[verification/SUMMARY.json](verification/SUMMARY.json)。
