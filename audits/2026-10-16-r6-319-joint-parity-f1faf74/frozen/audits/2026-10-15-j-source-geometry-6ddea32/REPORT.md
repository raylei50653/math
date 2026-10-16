# 第四輪：J 四連通、兩個原鄰弧介面與新完整 fibre 排除

BASE `6ddea32a81349821ad3724ae1652bddb9c6a7b04`。只寫本獨占目錄，
前12 audit 的388份凍結檔案無漂移；未 commit／push。

本輪從原小 C5 與原 rotation 證明 **J 是四連通球面三角化圖**。
任何新三角形只能來自原 s、t 鄰集間的跨邊 AB；原五環
`(r,s,A,B,t)` 的有界側含未落在環上的 v,w。兩點都在內違小C5；
恰一在內則被迫為W5中心，產生原禁邊 sw 或 vt。因此唯一跨邊是 vw。
這是任意大小來源推論，不是有限搜尋的零命中。

同一來源還給以下精確幾何（[完整證明](PROOF.md) §§2–5）：

- `d_J(m)=d_G(s)+d_G(t)−5≥7`、`d_J(z)=h+3≥6`；只有v,w,p,q可能四度。
- 每個induced C4必經m或z；每個避兩者的induced C5必有一側為原五度W5中心。
- J*每個3-edge-cut皆為單一頂點的三條邊，故至多包含一條標記e,f,g。
- 刪除相鄰m,z，得到保留全部其餘原邊的實際三角化disk W；其外圈由兩條
  原link路徑拼成，長 `d_G(s)+d_G(t)+h−6≥9`。端點α=p或β=q的情況保留原身份。

對每份**完整 W 染色**χ，兩原鄰弧的缺色集合Am、Az各至多兩色。
全部J lifts恰為 `Am×Az` 去掉對角；空fibre亦保留。完整原all-r表等價於

`(d(vw)=d(pq)) ⇔ (d(vw)=d(mz))`。

由此得到一個新的來源必要定理：

**若某份完整W染色滿足 `|Am|=|Az|=2`，則必須 `Am=Az`。**

否則兩原路徑各用兩色、共享端點色但另一色不同，三份合法hub lifts讓
`d(mz)`遍歷三種非零值；其中恰一份違反完整all-r條件。這排除的是完整
同源fibre，尚未證明來源W必有該fibre。此型只可能在d_J(m)、d_J(z)皆偶時出現。

有限驗證只校準上述精確介面，沒有新增弱球面反控制。三份九邊界兩star
patch各有2760份全染色、19680份proper boundary fibres，其中17040份為空；
另十邊界偶／偶patch有5688份全染色、59052份proper fibres，其中53712份為空。
其24份不同兩色路徑row都保留三份完整hub lifts，且恰一份違規。

[check.py](check.py)與[check_two_palette.py](check_two_palette.py)的正常／seed17
均一致；缺完整lift、缺空fibre、錯all-r判定、錯hub返回及兩項重寫證書均被拒絕，
詳見[VERIFICATION.json](VERIFICATION.json)。這些patch不是原最小來源。

完成後成本仍為 `(k−3)+2+1+5=k+5`，沒有保壞嚴格下降。剩餘義務是用
此四連通、原鄰弧與短圈幾何，強迫一份違規完整W lift或實際雙色環返回。
真來源 **not triggered**；完整319排除、ω=0、一般主命題仍OPEN；未新增Lean或使用4CT。

對Kempe covers組的[交叉審查](CROSS_REVIEW.md)已完成：75點圖由本組獨立從原邊
重枚完整864染色，全部8160個component交換與26112個cube均通過；正常／seed17一致，
缺完整染色的損壞證書被拒絕。確認其無section結果只承諾Layer0共同圖，不升格為平面來源排除。
