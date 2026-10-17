# 非面七缺陷的五接點修復：完整區域下降與一個六割位置排除

2026-10-17；BASE `5b9a7b3190c84bc10ff99608e372a9b4be57a0f6`。
**研究狀態 PARTIAL：三-spoke 子案沒有完整排除，聯合正值與完整319仍 OPEN。**

本輪已有兩項任意大小結果：不含唯一標記阻斷圈的完整交換區域可真正嚴格下降；
101 非面七圈若含 f，其五條 spokes 不能有 e，否則有具名 cyclic 六割。
前者排除一個條件子類，後者確實接上已採納的 R6-MARKED-SIX。
它們沒有證明剩餘受阻情形必迫禁止割。

## 1. 完整來源與額外子類假設

固定原全域最少內點、再最多邊的 no4ct C5 來源 G，原框 `(x,y,a,b,c)`、
原 x,y,b 四度、r 六度及 r 鄰序 `(x,y,t,w,v,s)`。同一完整支持
S∈{932,933,941}、全部原接線、扇區、私人頂點、完整 U319 fibres 包括空格、
全部原五點接回及 r lifts 不變。`J=U/(s=t)`、`m=[s=t]`、D=J*，
`e=(vw)*, f=(pq)*, g=(mz)*` 均是字面同圖對象，不另假設原 v 五度。

普通101非空與同圖偶補111匹配 M0 均沿用既有來源紙證。
取聯合族 `P110∪P101` 的奇數最小 M，**另假設** D−M 含非面七圈 C。
既有 A1–A3 給唯一 M 弦、相鄰四／五面與五條 M spokes 的 cyclic 五割 B_C。
不宣稱每個正奇數最小匹配必有 C。主攻 `|M0∩B_C|=3`；任意大小外側
及其他差分圈、完整遠處補圈始終保留。

## 2. 本輪證明到哪裡

[完整整合紙證](PROOF.md)及三路獨立重建給出：

| 結果 | 精確範圍 | 證據 |
| --- | --- | --- |
| 參考匹配五割奇偶 | `|M0∩B_C|∈{1,3}`，五-spoke 會保留完整奇七圈 | [B1](B/PROOF.md#2-the-five-spoke-exclusion) |
| 完整局部關係 | 32列全部保留，12列非空、15個內部匹配；三-spoke七個匹配中一個因封閉五圈被拒，餘六個局部相容態 | [B2–B4](B/PROOF.md)及[證書](B/certificate.json) |
| 唯一接觸差分圈 | 三-spoke恰一個 Q 接觸 X；其餘差分圈在外側；唯一含省略標記的圈 H 不可翻 | [A §1–3](A/PROOF.md)、[B3](B/PROOF.md#5-the-exact-actual-difference-interface-for-arbitrary-size-exteriors) |
| 真正完整區域下降 | W 是 D−(M∩M0) 的分量；翻其中全部差分圈，使 W 內補圖恰成 M0 偶補、外側逐圈不變。若 W 有奇圈且不含 H，保持聯合身份並至少下降二 | [A1–A2](A/PROOF.md#4-a-larger-actual-batch-gives-a-stronger-all-size-criterion) |
| 標記中心三分類 | 內弦=e；或110內弦=f；或101的f在四面弧上。最後一類 Q=H，直接參考交換必受阻 | [C §2–4](C/PROOF.md) |
| 接入新六割定理 | 101且f∈C若e是spoke，取非弦f端點a、Y=X−{a}，得到同含e,f的cyclic六割；故e兩端都在X外 | [C1](C/PROOF.md#3-a-concrete-forbidden-six-cut-construction)、[整合 §5](PROOF.md#5-實際接上-r6-marked-six主動-f-七圈不容-e-spoke) |

位置排除不需 M0、三-spoke 前提或奇數最小性，故也適用一-spoke 案，
但沒有提供一-spoke 修復。完整區域下降同樣不限於七圈或三-spoke。

因此在聯合最小 M 中，**所有奇補圈都被迫位於同一個含 H 的完整區域 W_H**。
這是一項必要結構，不是正奇數情形的矛盾。

## 3. 為何不能只翻安全 Q

從 M△M0 選批次時，e與另一條已選標記是共同匹配邊，只有省略標記 h
可能翻；因此保持聯合身份恰好是略去 H，實際保留原方向。
一般交替批次仍允許 f,g 同翻，101↔110 的可能性沒有被禁止。

即使 Q≠H、局部七圈消失，也不能推出全圖奇數下降。A 給一張明確平面
cubic 控制圖，舊完整補圈長 `(7,8,5)`，安全 Q 交換後為 `(15,5)`，
全圖奇圈數二保持不變；再翻阻斷 H 才到111偶二十圈。
此圖僅反駁忽略外側補圈的推理，沒有主張完整來源、最小性或新六割限制。

整區交換處理了這項問題：它必須一次包含 W 中全部實際差分圈。
若七圈與 H 已在同一區域，這個批次不安全，下降定理沒有觸發。

## 4. 精確剩餘義務與停止規則

剩下的是三-spoke且 `W_C=W_H` 的同圖無界外側；101主動f七圈甚至直接 Q=H。
尚須證某個其他實際批次安全且嚴格下降，或構造同含e,f、大小≤6、兩側有圈的 Y。
本輪未證「受阻⇒禁止割」。

也不能直接取完整區域邊界：所有三類七-cap都有一條e或f完全在 X 內，
任何包含整個 X 的頂點集都不會讓這條標記進入其割。新的禁止割構造必須
切開 X，並另外證兩側仍有圈；整區邊界也沒有≤6的既有上界。

按窄研究停止規則，本輪停在上述已證條件下降與實際位置排除，沒有擴大到
新來源枚舉。五長、面七圈、九長以上奇圈、一般110↔101批次及一-spoke修復
仍另保留。`omega_e=0`、`W110+W101>0`、完整319、一般K∞=K≤5仍 OPEN。
不要求 W110、W101 分別為正；一般K≤22、固定r6的k≥25、k+5接回成本均不變。

## 5. 有限驗證、獨立審查與重播

11份主輸入逐一對回 BASE Git object；非routing數學來源 live bytes 亦零漂移。
A 另凍結既有固定圖輸入，獨立重建38個普通匹配、24個偶參考匹配，核對全部
912組(M,M0)、928個完整區域及28份三-spoke非面七圈對。
B 從兩套獨立 matching 重建方法比對全部32列及完整補圖片段。
C 保留25個非共端的標記位置，逐份構造Y及兩側完整圈。
這些是有限校準；**真正最小來源實例供應為零，source-realizability not triggered**。

A 的 active certificate 是 `certificate-v2.json`；初始 `certificate.json`
是保留的開發seal，沒有覆寫。正常／seed17重播、污染拒絕與排他建立拒絕分別見
[A receipt](A/VERIFICATION.json)、[B receipt](B/VERIFICATION.json)、
[C receipt](C/VERIFICATION.json)及[root receipt](integration/root-checks.json)。
三份[獨立整合審查A](A/REVIEW-INTEGRATION.md)、[B](B/REVIEW-INTEGRATION.md)、
[C](C/REVIEW-INTEGRATION.md)均核可整區下降與具名六割證明。

由repository root執行只讀重播：

```sh
python3 -B audits/2026-10-17-r6-seven-five-repair-5b9a7b3/check.py --check
python3 -B audits/2026-10-17-r6-seven-five-repair-5b9a7b3/A/check.py
python3 -B audits/2026-10-17-r6-seven-five-repair-5b9a7b3/B/check.py
python3 -B audits/2026-10-17-r6-seven-five-repair-5b9a7b3/C/check.py check audits/2026-10-17-r6-seven-five-repair-5b9a7b3/C/certificate.json
```

相同命令前加 `PYTHONHASHSEED=17` 可重播該hash順序。
本輪整合、既有Lean庫建置及文件檢查的實際結果見 [VERIFICATION](VERIFICATION.md)。
沒有新增Lean theorem，`lake build`僅驗既有庫；新紙面拓撲與下降尚未Lean化。
沒有使用四色定理、外部枚舉或新增外部文獻。

## 6. 文件傳播範圍

Closure scope：僅完整區域避H的條件下降、局部完整關係及主動f七圈的e-spoke位置排除；
整個三-spoke子案未closure。Canonical Source：[PROOF](PROOF.md)；Evidence：A/B/C及root。

Updated：本audit、Kempe導覽現況／精確停止點、STATUS直接索引。
Reviewed-unchanged：README／HANDOFF研究線與tag；原六割定理及舊封存證據不變。
直接父題的受阻到小割義務仍OPEN，故沒有改寫舊報告或跨線摘要。
Propagation stop：L1現況與索引；沒有父題closure或supersession，無L2／L3語義變動。
目前接續入口見 [Kempe導覽](../../docs/c5_kempe_guide.md)。本輪未commit、未push。
