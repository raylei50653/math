# C44″ 後續：相鄰唯一 mixed 的四份 (4,4) 排除稽核

2026-10-07。依 [Kempe 導覽](../../docs/c5_kempe_guide.md#3-停止點與保留缺口)
的窄提議，核對既有任意大小化約與固定必要域；不改寫歷史 producer 或 artifacts。
來源為 [雙 spoke](../../docs/c5_excess_two_mixed_core_spokes.md)、
[spoke＋unary](../../docs/c5_excess_two_mixed_core_spoke_unary.md)、
[雙 unary](../../docs/c5_excess_two_mixed_core_two_unary.md)、
[mixed 省略](../../docs/c5_excess_two_mixed_omission.md)。

**判定：四份報告的指定化約與固定域排除成立，未發現新的缺口。**
前提仍是有限簡單 induced-C₅ disk、完整 Σ=933／941 或整圖 D₅ 像、
每條非框邊 Σ-critical、ε=2、相鄰雙 degree-5 roots、恰一份原 mixed，
其他有效內點完整 degree 四。沿用上游 degree-4／Gallai 分類、root 刪除與
triangle 附件分類；本輪沒有重新稽核這些上游報告的全部有限拓撲枚舉。
這是明確限定範圍的紙面稽核及獨立有限證書驗證，未補 E5 要求的新證明。

## 1. 任意大小化約的紙面核對

### 1.1 原省略身份與保留 mixed

Degree-4 飽和迫每份原 piece 全取或全不取；兩 roots 的 loss 是 (1,1)。
原 zw 與兩 roots 由前序全收引理保留。故省略身份只能是兩側各一個 unit
因子，或恰一份 mixed11。不能省略 capacity≥2 unary 或同時省略其他因子。

保留 C 時，原 C 中任何不同 contacts 之間的路與 zw 形成至少四環；
全 degree-4 分類禁止這種環，故 C11 共用原 x，z,w,x 是同一 triangle。
單 triangle 的剩餘部分是原路徑枝；雙 triangle 只能直接 bridge、沒有外掛樹。
因此保留 mixed 的 roots 都是 triangle 上的 singleton markers。

### 1.2 Run transfer 與共同色框

固定任意 β，同附件 run 的內點可用色集 A 至少有兩色。
若 |A|=2，固定 run 外側兩端色後，存在延拓只依正長度奇偶；
若 |A|≥3，先看長度一：至少一色避開兩端色。歸納增加一個內點時，
從至少兩個可用末色選一色避開新點色，仍能接到下一點，故任意正長度均可。
零長度另是直接邊，不能混入正偶數代表。

所以每個正未標記 gap 縮成一／兩點，保留零 gap、leaf、triangle 及原 roots。
各 gap 的 branch sets 沿原路徑連通互斥；刪多餘 spokes 後收縮，仍是
boundary 固定 minor。固定共同 triangle／root tuple 後，逐枝選原染色，
得到完整聯合 relation 的雙向延拓；不是投影 marginals 的乘積。

保留 mixed 的正常形為 18 單-run＋8 雙-run＋36 裸 triangle＋64 雙 triangle，
合計126。前兩類附件完備性沿用既有分類；裸 triangle 放寬而不先篩 disk。
雙 spoke 是原 root 座標上的字面過濾，因此此 transfer 可直接接回。

### 1.3 原 unary 的接回及固定支援

省略單接點 unary 後，contact 有一份 slack；逆序 spanning-tree 貪婪染色
給其原 endpoint relation 非空。只有 singleton relation 能禁止 root 使用一色。
兩份 unary 只共用固定 B，各避色條件必套到同一個 root-pair tuple。

固定原實際支援 S，支援上的 equality shape 相同時，整份 unary 染色可整體
S₄ 搬運；singleton 必被支援色 stabilizer 固定。同一 shape 的各列要求取交。
雙 unary 的兩個 shape functions 共同滿足各列 binary constraints，不能分開解。
必要域容許尚無來源實現的 choices，這只放寬來源條件。

將同一原連通 unary 收縮成星僅用作拓撲反證；其 branch set 與全部 run
branch sets 互斥。雙 unary 的較小支援證書只是從同一 minor 刪多餘支援邊。
加入外侧 boundary apex 後的 K₅／K₃,₃ subdivision 因而能傳回原 disk 圖。
收縮不被用作染色替換，也不宣稱保持 Σ 或完整 degree。

### 1.4 省略 mixed11 的完整二維介面與344域

G−C 的原 zw 是 bridge，兩側完整全圖 relation 可以共同接合；C 的兩端
必用同一 tuple。固定一個 root pin 時，另一 contact 的 slack 給禁對每列／欄
至多一格。若有兩個禁對 (a,b)、(c,d)，必 a≠c、b≠d；每個 C-tuple 同時
落在兩個十字，故只可能是 (a,d)、(c,b)，不能有第三格。
這給空、單格、兩格且 rows／columns 異的89份必要選項。x=y 的共鄰角色
仍來自同一原變數，包含於這個放寬域。

原 M 的 roots 是相鄰 bridge markers。標記把 uniform run 切成 gaps；
在同一 run 中兩 markers 必相鄰，故沒有正的 marker 間 gap。
單-run triangle 枝原長度為奇数，最多兩 markers 加兩個≤2 gaps，壓縮後
長度只需1、3、5；雙-run 的 X 首點固定、Y 正偶長度只需2、4、6。
偶數路徑的各 run 同理只需2、4、6；跨 run 的相鄰 markers 不改 run 奇偶。
所以344域的160單-run／64雙-run／56 path／64雙 triangle 覆蓋所有原 bridge 位置。
刪 zw 不會刪去未標記 gap 內的邊，故相同 transfer 同時保持 M 與 M−zw。

## 2. 獨立固定域驗證

[verify.py](verify.py) 僅用標準函式庫，沒有 import 舊 producer、搜尋 solver
或 planarity oracle。它自行以最小剩餘色域回溯重算完整 root-pair relations，
重建 S₄ 支援域、逐 constraint 核對既有 UNSAT proof，並在自行重建的星圖邊集
驗證 subdivisions 的實際邊、簡單路、內點互斥與完整九／十份鄰接。
原依賴及四份 artifacts 的 hashes 記於 [validation.json](validation.json)。

| 舊證書 | 本輪獨立核對 |
| --- | --- |
| 雙 spoke | 126核心／570具名root邊／5,700核心列；全部6,068次接回的Σ均非目標 |
| spoke＋unary | 同126核心／5,700核心列；3,732次接回、37,320個目標比較、89,088個固定支援查詢、2,640份subdivisions全部通過 |
| 雙 unary | 同126核心／5,700核心列；5,700個目標比較、368,859份UNSAT proofs、17,189份相容assignments、3,180份subdivisions全部通過 |
| 省略 mixed | 344核心／3,440核心列、3,440個目標比較、9,152個固定支援查詢、188份subdivisions全部通過 |

另獨立生成長度≤12的標記 run 控制：3,386次壓縮全部落入原344域，且
每份原模板都有覆蓋；2,112次色集／外側端點／長度 transfer 核對通過。
這些有限控制支持上節的紙面奇偶化約，不是任意長度完備性的替代。

## 3. 重播、限制與後續

```sh
python3 audits/2026-10-07-c44pp-mixed-audit/verify.py
```

本輪實際執行上述完整獨立驗證；沒有重跑四個原 producer、ES／ER 搜尋、
上游全部拓撲枚舉或 lake build。沒有新 Lean theorem，也沒有構造滿足完整
Σ933／941的來源正控制。有限必要域的排除不要求該來源前提有實例。

新 verifier 首次加入 run 控制時漏處理空 triangle tail，發生 IndexError；
已修正 verifier，完整重跑通過。這是本輪程式錯誤，不是歷史證書或紙面缺口；
沒有因其改寫舊 artifacts。

四份指定排除有此限定範圍的獨立稽核，仍依上游分類及其原信任界線。
E5 的新證明要求、三列推廣與其他 core 型未因此完成。
後續新增的 U1 排除另見 [no-mixed44 報告](../../docs/c5_excess_two_no_mixed_core44.md)；
當前殘留由 [Kempe 導覽](../../docs/c5_kempe_guide.md#3-停止點與保留缺口)維護。
