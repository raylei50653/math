# 完整 r6 同標記六圈排除：採納、獨立重建與控制圖

2026-10-17；凍結 BASE `6c420f3ca77d60952ed76f93dff7449c522715ca`。
本輪採納使用者提出的 **R6-MARKED-SIX 紙面來源定理**：不假設原 v
五度，在既定完整 r6 原來源中，每個同含 vw、pq 的簡單 J 圈長至少七；
每個同含 e、f 的 cyclic D cut 亦至少七邊。
**`W110+W101>0`、`omega_e=0` 及完整319仍 OPEN。**

## 1. 完整契約與採納範圍

固定全域最少內點、再最多邊的 no4ct C5 原來源 G，原框
`(x,y,a,b,c)`，原 x,y,b 四度、r 六度及 r 鄰序 `(x,y,t,w,v,s)`。
逐圖固定完整原支持 S∈{932,933,941}；同一 U319、`J=U/(s=t)`、
`m=[s=t]`、實際 D=J*，及 `e=(vw)*, f=(pq)*, g=(mz)*` 均不變。
保留全部原接線、扇區、私人染色、完整及空 fibres、原五點接回及 r lifts。

[完整整合紙證](PROOF.md)涵蓋兩種連接配對、全部 hub 情形、disk
邊界中點與 α=p／β=q 端點情形，以及不預設兩側連通的 cyclic cut。
本結論適用任意來源大小；沒有以有限圖或 checker PASS 代替來源證明。

採納的是新的原五圈方法，不恢復前輪錯誤的跨扇區反射。
[前輪 B 的修正版](../2026-10-17-r6-joint-positive-113e41f/B/PROOF.md)
正確指出 `(m,q,p,h,w)` 不能用同一 s/t 還原；本輪改用原五圈
`(a,p,h,w,t)`，補掉它留下的 c4 型，並推廣到沒有 v5 前提的全部 r6 支。
舊證明、被拒初稿與錯誤 PASS 均作凍結歷史證據保留，不改寫其封存 bytes。

## 2. 證明的三個獨立檢查點

| 檢查點 | 原來源推導 | 獨立重建 |
| --- | --- | --- |
| 兩步路徑 | `p-h-w⇒a≤5`、`q-h-v⇒c≤5`；h=m 迫相應原框點四度，h=z 被非邊排除；其餘用接觸外框的真正原五圈 | [A 紙證](A/PROOF.md) |
| 全部六圈／小割 | 第一配對違反 a+c≥11；第二配對由實際 disk 交錯端點迫經 m，兩個原 cap 分別迫 p5/a4 或 q5/c4；小 cyclic cut 先證為 bond | [B 紙證](B/PROOF.md) |
| 弱前提控制圖 | 固定原 marking，重建球面 rotation、對偶、全部匹配、完整補圈與實際割兩側 | [C 固定圖證據](C/PROOF.md) |

小 cap 定理明確容許 proper C5 接觸原外框。兩步引理還必須使用
非空 cap 恰為「單 W5 且無額外 boundary chord」的完整結論：若只取
「內部至多一點」，會漏算 ah/ch 可能多出的一個鄰點。
第二配對的 p/q cap 各直接在原 G 逐面計算，沒有支持933→940的權威跳躍。
root 整合另經 [A 交叉審核](A/REVIEW-INTEGRATION.md)、
[B 交叉審核](B/REVIEW-INTEGRATION.md)及 [C 整合審核](C/REVIEW-INTEGRATION.md)。

## 3. 控制圖確實被新來源限制排除

C 從保存的十二點 J 原始圖獨立重建實際球面嵌入與二十點 cubic D，
保留全部原邊索引與 marking `(e,f,g)=(0,29,6)`，不匯入舊 checker。
全部普通 PM 恰38個，聯合族恰3個且全為101，完整補圈長為

`(5,15)`, `(5,5,10)`, `(7,13)`。

因此該圖仍有聯合最小奇數二。全部258個簡單原六圈中，恰五個同含 e,f；
其中恰兩個的實際對偶割兩側均含圈：

| 原六圈 | 一側 (V,E) | 另一側 (V,E) |
| --- | --- | --- |
| `(0,2,11,10,5,4)` | (14,18) | (6,6) |
| `(0,2,11,10,9,4)` | (12,15) | (8,9) |

另外三個的較小側均為 (4,3) 的樹。完整五圈表、兩側原 face/edge IDs、
全部38個 matching 及每份完整補圈見 [C 證書](C/certificate.json)。
它缺原兩面與 hub 接線，仍是 **not triggered 的弱前提控制圖**，不是
來源反例。本輪確認新六圈／六割限制有舊四／五割條件沒有的資訊，
但沒有證出每個正奇數障礙必迫這種小割。

## 4. 下一個窄問題與交換契約

普通 P101 已證非空，因此 F_e=P110∪P101 非空，omega_e 有定義。
下一個窄入口是：在聯合奇數最小的 matching 中，對
[前輪 A 分類的非面七長奇缺陷](../2026-10-17-r6-joint-positive-113e41f/A/PROOF.md)，
保留它唯一 matching 弦、相鄰四／五面及五條有序 matching spokes，
在同一任意大小外側證真正的奇數下降，或證受阻必迫同含 e,f 的
實際小 cyclic cut。後一連接本輪沒有證明。

若從 M∈F_e 出發，交換一批實際且頂點互不相交的 M 交替圈 A，保持
聯合身份的精確條件是

`e∉E(A)` 且 `1[f∈E(A)]=1[g∈E(A)]`。

即 f,g 零條或兩條同翻，允許101↔110；從111進入聯合族則須恰翻一條。
[整合紙證 §6](PROOF.md#6-聯合匹配交換的精確契約與停止點)給逐位 XOR 證明，
[root checker](check.py)另窮盡核對三個起點的全部翻動組合。
保住標記身份仍須重算完整補圖每個圈，不能據此假定奇圈數下降。

新定理不限制 D-M 的奇圈長度；目標族已有 e∈M，補圖本來不含 e。
五長缺陷、七面、遠處奇圈與九長以上奇圈仍待處理。
全九框必要計數仍沿用前輪精確可行證書，本輪沒有重跑或提高其排除力。

## 5. 證據層與重播

輸入由 [INPUTS](INPUTS.json)及[直接父入口追加凍結](ADDITIONAL_INPUTS.json)
綁定 BASE。root checker 將22個 frozen 檔案逐一對回 BASE 的 Git object，
並檢查所有數學來源的 live bytes；routing 文件可作本輪現況更新。

從 repository root 執行：

```sh
python3 -B audits/2026-10-17-r6-marked-six-exclusion-6c420f3/check.py --check
python3 -B audits/2026-10-17-r6-marked-six-exclusion-6c420f3/A/check.py
python3 -B audits/2026-10-17-r6-marked-six-exclusion-6c420f3/B/check.py --check audits/2026-10-17-r6-marked-six-exclusion-6c420f3/B/certificate.json
python3 -B audits/2026-10-17-r6-marked-six-exclusion-6c420f3/C/check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-17-r6-marked-six-exclusion-6c420f3/C/check.py --check --seed 17
sha256sum -c audits/2026-10-17-r6-marked-six-exclusion-6c420f3/SHA256SUMS
```

正常／seed17、篡改負控制及排他建立結果分別見
[A receipt](A/VERIFICATION.json)、[B receipt](B/VERIFICATION.json)、
[C receipt](C/VERIFICATION.json)與[root 驗證紀錄](VERIFICATION.md)。
這些程式只驗有限 cap／連接分類、固定圖及原檔身份；任意大小扇區、
Jordan 分離與 cut 對偶是紙面層。真正最小來源實例供應為零，not triggered。
沒有使用四色定理、額外外部枚舉或新增 Lean theorem。

`lake build` 僅檢查既有 Lean 庫；正式 docs、scoped 與 whole-tree DocGraph
分開報告。舊大型有限枚舉與九框計數未重跑；新定理不依賴新的枚舉。

## 6. 收尾範圍與文件傳播

Closure scope：完整既定 r6 原來源的同標記簡單六圈／cyclic 六割排除，
以及那一張固定弱前提控制圖違反新限制的精確驗證。
Canonical Source：[PROOF](PROOF.md)；Evidence：A/B/C 與 root checker。

Updated：本 audit、Kempe 導覽及 STATUS 的現況與直接索引，
以及 C4 直接父入口中被新結果取代的六圈殘支摘要。
Reviewed-unchanged：README／HANDOFF 的路由與研究線、degree5 導覽的 R9–R31
範圍、跨線 synthesis 的父命題狀態；舊封存證據及一般界均保留。
Remaining OPEN：聯合偶補正值、omega_e=0、完整319、原 v/w 五度排除、
一般 T/T0、r≥7、K∞=K≤5，以及任意大小修復失敗到同標記小割的連接。
Propagation stop：直接父入口；父題仍 OPEN，無更高層 closure。
一般 K≤22、固定 r6 的 k≥25 與原來源接回成本 k+5 未變。
本輪沒有 commit 或 push。
