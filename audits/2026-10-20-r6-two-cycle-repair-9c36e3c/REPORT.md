# R6 兩完整補圈的條件匹配修復

2026-10-20；獨立 audit BASE `9c36e3c4789dfec07d60ec4e042f0bafe17451d1`。

**已構造兩個指定 rim 點的條件式完整對偶面修復；尚未證每個來源必有可用點。**
這輪直接改變原 M，不再嘗試已被兩圈定理阻斷的固定 M 參考分離。
任意大小紙證見 [PROOF](PROOF.md)，獨立推導見 [A](A/PROOF.md)、
[B](B/PROOF.md)，固定圖控制見 [C](C/REPORT.md)。

## 1. 精確範圍與成果

保留同一全域最少 completed-source、次級最多邊的 no4ct C5 原 G，
原有序框、x,y,b 四度、r 六度、支持 932／933／941、全部原 rotation
及私人接觸、完整 U319 空／非空 fibres、全部原五點及 r lifts。
字面 `J=U/(s=t), D=J*` 和 `e=(vw)*, f=(pq)*, g=(mz)*` 不變。
固定任意實際 M101，假設 `D−M=C7⊔O_odd`，C7 是含 f 的非面七圈。
無原 v 五度、無奇圈最小性前提。

| 本輪已證 | 精確意義 |
| --- | --- |
| 字面 O 扇區 | e、g 分居 O 兩側；五 spokes 次序固定；g 必在原 z 的區間，不能任放在 cap 側 |
| 兩個安全 rim 點 | 正規 cap 標號 chord03 下，45／56 對應的兩點都避 f、g；其 cap 側交替路亦避 e |
| 任意大小條件修復 | 某一安全點的 incident M*／非 M* 邊在原 rotation 交替，且每條附著子樹有偶數個奇度點，則翻轉其完整對偶面得到全偶補 N101 |
| 全部補圈奇數公式 | 沿對應 O 區間成功走完後，令 j 為偶長跳弧數；完整新奇圈數恰 `j+(j mod 2)` |
| 真來源局部限制 | 成功點度數恰 `2t+4≥6`；原 g 樹枝有 `ell_g≥3b_m+3`，弧內至少 `b_m+4` 個端點接 O 反側 chords |
| 同一 O 的充要介面 | 全部 32 spoke masks 保留；15 個局部 matching fragments 中 13 個無內部奇圈，連同同一 O 的完整配對、奇偶、閉圈及 e/f/g 選擇，精確判斷全部修復 |

安全點及子樹都是同一 M* 的實際物件。成功的交換 Q 是實際單一
M-交替圈，避全部三條標記，因而已是原要求的頂點不交批次。
完整新補圈是各跳弧加 chord 的圈，以及一個剩餘大圈；沒有遺漏遠處奇圈。

若聯合偶補族為空，兩個安全點各自必有以下阻礙之一：
原 rotation 中出現連續兩個 T 鄰點，或有附著子樹含奇數個奇度頂點。
這是必要條件；未證兩點不可能同受阻，也不排除其他修復批次。

## 2. 三路核對與有限控制

A 以完整 matching 遞迴及獨立 O 選邊組裝交叉核對；
B 從 primal 三分量與原 rotation 重建側別、字面扇區及完整面翻轉，
另獨立枚舉全部 15 個 cap fragments。互審見
[A review](A/REVIEW.md)、[B review](B/REVIEW.md)。
根層另逐項核對完整補圈分解與來源度數限制。

C 的四張固定平面 cubic 控制保留 sphere rotation、全部完美匹配、
八個標記 fibres（包括空者）、所有完整補圈、所有 `M△N` 交替圈批次，
以及 e 色為零的全部完整 Tait 染色。合計 160 個完美匹配。

| 控制 | 檢出的事實 | 來源界線 |
| --- | --- | --- |
| 弱幾何無修復 | 有 111／全異參考，但聯合全偶 fibres 都空 | g 的 sector 不符合原 z；不能當 R6 反例 |
| 字面安全消七圈 | 某安全 Q 使 `7+13→9+11`，完整奇數仍二 | 保局部具名 incidence，卻有來源不容許的三度 primal 點 |
| 偶長跳弧 | 跳弧長二，完整補圈成 `3+15` | 檢出真正完整奇圈；仍非來源 |
| 奇長跳弧 | 跳弧長三，完整補圈成 `4+16` | 非空跳躍的正控制；仍非來源 |

三張有局部字面 incidence 的圖沒有原 G、U319 完整 fibres 或全部 lifts。
來源實現一律是 **not triggered**。既有 `k≥25` 已給 `|O|≥37`；
不把這些小控制或較弱局部長度界寫成新的全域來源排除。

## 3. 重播與權威

```sh
python3 -B audits/2026-10-20-r6-two-cycle-repair-9c36e3c/check.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-20-r6-two-cycle-repair-9c36e3c/check.py
```

根 checker 核對 14 份凍結原輸入、額外 J 幾何依賴、A 的完整介面證書，
及 C 的四張固定圖完整證書。它不檢證任意大小紙證、不接受虛構 source，
也不把 finite PASS 提升為來源排除。正常／seed17 重播一致，
缺空 fibre、改路長、丟完整圈、改字面 sector、改跳弧奇偶及缺權威輸入皆拒絕；
exclusive-create 覆寫拒絕。命令與證據分見 [VERIFICATION](VERIFICATION.md)。

原兩圈 checker 另有本輪只讀重播；沒有重跑大來源枚舉。
既有 `lake build` 通過，不表示本輪紙證已形式化。無新 Lean theorem，
無新外部定理，未使用四色定理。

## 4. 停止點與文件範圍

下一個精確問題是：用原來源的 rotation、度數、短割及完整 fibres，
排除兩個安全點同時具有上述真實阻礙，或在這個受阻子類構造其他
保 e、同翻／不翻 f,g 的實際批次。13-state 同 O 介面可完整驗證候選；
它自身不供應存在性。當前入口由 [Kempe 導覽](../../docs/c5_kempe_guide.md)維護。

兩完整補圈普遍修復、其他奇圈分支、H 相連殘案、
`W110+W101>0`、`omega_e=0`、完整319與較小 bad 來源仍 OPEN。
一般 K≤22、固定 r6 的 k≥25、completed-source 接回成本 k+5 不變。

Updated：本 audit、Kempe 導覽的兩圈子題與 STATUS 對應直接索引。
Reviewed-unchanged：README／HANDOFF 的研究線與 tag、原來源及前輪封存證據、
941 其他分支的數學結論。
Propagation stop：L1；只有條件式子成果，父題無 closure。
同工作樹其他獨立 audit 不屬本輪。本輪未 commit、未 push。
