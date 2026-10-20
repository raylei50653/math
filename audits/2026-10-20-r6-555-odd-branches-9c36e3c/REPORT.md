# 兩完整補圈的 5／5／5 型：四點十圈交換完成修復

2026-10-20；Git BASE `9c36e3c4789dfec07d60ec4e042f0bafe17451d1`。
前輪尚未提交證據與當時路由已另凍結，81 個輸入完整 SHA 可重播。

**所問同樹兩奇支條件子案已解。** 在同一原來源和同一 M 上，
交換集合 `X={h,A,B,τ}` 的原 dual 邊界是一條交替十圈，
得到 `N∈P101` 且全部完整補圈恰為 `C4⊔C_(|O|+3)`，兩圈皆偶。
此構造覆蓋整個條件 5／5／5 型；未證所有來源落在這型。

完整任意大小證明見 [PROOF](PROOF.md)，
獨立推導見 [A](A/PROOF.md)、[B](B/PROOF.md)，
交叉審查見 [A review](A/REVIEW.md)、[B review](B/REVIEW.md)。

## 1. 同一原圖上的三項驗收

保留原最少 completed-source no4ct C5 契約、原有序框及實際接觸、
原 rotation、完整 U319 空／非空 fibres、全部原接回和 r lifts。
固定 `J=U/(s=t), D=J*`、原標記 `e=(vw)*, f=(pq)*, g=(mz)*`，
以及同一 `M∈P101` 的完整 `D−M=C7⊔O`。

A、B 是原兩個安全 rim 點，τ 是 AB 外側實際第三點；
條件是三點皆 J 五度且 τ 避 v,w。h 是既有七-cap 的普通五度中心，
另一中心 u 是 p 或 q 且 J 四度，不另加來源假設。
τ 只是本題局部名稱，不是原 split apex t。

| 驗收 | 原圖結論 |
| --- | --- |
| 原 rotation | 四個完整 star 給一條實際簡單交替十圈；所有 12 個涉及三角面逐一合法 |
| 三標記 | X 避六個原標記端點，e、f、g 逐一保持，故 N101 |
| 全部新完整分量偶性 | 恰 `{u}`、`(T−τ)∪{A,B}`、`(U0−{A,B})∪{h,τ}`，原度和奇偶全部零 |

兩條奇支由實際路徑 α−A−B−β 合併。新補圖恰兩圈，
一圈是 u 的完整四度面，另一圈長 `|O|+3`。
不存在只消掉原七圈而漏驗外側奇圈的缺口。

## 2. 獨立固定圖驗證

[C checker](C/check.py)不匯入前輪程式，從凍結原 rotation 重建 primal／dual，
分類前輪七張控制，恰一張符合局部 5／5／5 兩奇支。
對這一張控制重建全部 56 個完美匹配、4096 個 cut、78 個頂點對，
八個完整標記 fibres 及八個全偶標記 fibres 皆保留，包括空者。

四點集合恰 `{2,5,6,8}`，對應完整匹配 row55；原十圈交換保持 101，
全部新完整 primal 分量的原度數和為 4、26、36，完整新補圈長為 4、18。
兩個指定雙點交換仍各留兩個奇圈；另一最小雙點使用三度伙伴，
不作來源修復依據。四點構造的紙證不使用這個低度伙伴。

這張控制仍含原來源不允許的低度點與 primal 平行邊，
沒有原 G、完整來源 fibres 或全部原 lifts。
**來源實現仍為 not triggered；有限控制不證來源覆蓋。**

正常與 seed17 重播相同，11 個污染／覆寫控制均拒絕，
見 [C 證書](C/certificate.json.gz)、[C 驗證紀錄](C/VERIFICATION.json)。
整合重播、custody、文件及 Lean build 的實際執行見 [VERIFICATION](VERIFICATION.md)。

## 3. 收尾與父題邊界

Closure scope：同一原來源、同一 M 的兩完整補圈分支，
兩安全點及 AB 的實際外側第三點皆五度且後者避 v,w，
必有保三標記的全偶補 N101。這包含所問同樹兩奇支。
若另假設偶補 P101 空，此型即與該假設矛盾。

Updated：本 audit、Kempe 導覽的兩圈子節／現況、STATUS 對應索引。
Reviewed-unchanged：README／HANDOFF 的研究線與標記；原兩圈父題、
主動 f 幾何與一般匹配契約仍有效；前輪檔案及 frozen bytes 保留。
直接引用及父摘要核對未發現需更新其他研究線的此子案聲明。
Propagation stop：L2；子案 closure 不給一般度數型覆蓋，父題仍 OPEN。

Remaining OPEN：原來源必落此型的覆蓋、其他度數型的兩圈修復、
`W110+W101>0`、`omega_e=0`、完整319與較小 bad 來源。
無四色定理調用、無新外部定理、無新 Lean theorem；
一般 K≤22、固定 r6 的 k≥25、completed-source 接回成本 k+5 不變。
目前接續入口見 [Kempe 導覽](../../docs/c5_kempe_guide.md)。

本輪未 commit、未 push；其他並行 audit 與既有工作樹修改不屬本輪。
