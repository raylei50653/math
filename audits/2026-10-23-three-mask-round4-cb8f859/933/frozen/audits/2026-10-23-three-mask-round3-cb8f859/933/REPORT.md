# 933：兩張新原洞填片，縮為同一E的兩個完整fibre

BASE `cb8f8593e273a7426ecadd59797a6e643cc4768e`；2026-10-23。
只寫本 `933/`；未改前輪、shared docs、Git，沒有commit或push。

**新構造**已離開前輪固定Q1／Q2／fan-B。在原p,h刪除後的真六邊洞
`(a,n,R,L,q,b)`，兩張非交叉填片

```
T0=(G−{p,h})+{aL,bL,nL},
T1=(G−{p,h})+{aL,bL,aR}
```

都保原rotation、原E、原外框及全部附件，嚴格完成k−2。新增邊若與E原邊
同端點，只刪新副本、保留E原邊；結果是合法simple plane disk-C5競爭圖。
完整合法性與紙證見 [PROOF.md](PROOF.md)。

令同一實際 `E=(a,n,R,L,q,c,x,y)` 的完整延拓數為
`U=z73=z196`、`V=z76=z198`、`W=z257`、`W'=z259`。精確等式為

| 完整字面列 | T0 | T1 |
| --- | --- | --- |
| 01021 | 0 | 0 |
| 01202 | U | U |
| 01212 | V | V |
| 01232 | N01232(G)=4(U+W)>0 | W+W' |

另有 `U+W=V+W'`。因此兩張圖的原四查詢bad證書都等價於同一義務
**U=V=0**；若成立，兩張都真接受、真三拒絕，完整支持必在K132外。
原來源的全域最小性反過來迫 **U+V>0**。這是合法較小競爭圖所給的
必要幾何條件；不是單靠18維必要空間已證的可行性或一般圖結論。
下一窄問題可直接追原E字面完整fibres `01023013`、`01023031`：
須用原幾何證兩者皆空，才能與最小性矛盾。此次未完成該步。

本輪只審核這一原洞的全部14種無新點三角剖分。其餘12張若01212全空，
已由完整投影及精確非負等式迫原01232全空；故都不能走原四查詢證書。
其中T6就是舊fan-B，另11張為新no-go。**沒有宣稱14張完整支持皆在K132**，
沒有重新篩56支持證書、外側圖枚舉或LP。

[certificate.json](certificate.json)保留全部14張10×274矩陣，以及2560份
原字面局部fibre、175個完整p,h lifts、2392個空fibre。兩新圖的完整十列
同源計數逐列列於紙證。 [independent.py](independent.py)以E-word-first、
單一共同S4作用反向重建全部矩陣，並在一個真cone-over-C8原E上直接枚舉
14張整圖全部十列full fibres核對。該控制不滿足原r6／933合同，明列not triggered。

`U=V=0`的必要線性切片16維，原六個正列皆未被迫為零泛函；完整必要
Kempe支持診斷亦不增新零。W／W'的02|13及03|12各12個分割只餘1個，
完整子集交換均封存。這些只是**尚未被此診斷排除**，沒有精確primal，
不宣稱必要系統可行，更不宣稱原來源可實現。

[INPUTS.json](INPUTS.json)凍結15份數學權威bytes／SHA，routing獨立允許漂移。
checker只讀重播；`--build` exclusive create。所有命令與exitcode見
[VERIFICATION.json](VERIFICATION.json)：

```
python3 -B audits/2026-10-23-three-mask-round3-cb8f859/933/check.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-23-three-mask-round3-cb8f859/933/check.py
python3 -B audits/2026-10-23-three-mask-round3-cb8f859/933/check.py --negative
python3 -B audits/2026-10-23-three-mask-round3-cb8f859/933/independent.py
```

| 權威／控制 | 狀態 |
| --- | --- |
| 原洞合法性、k−2 ledger、完整同E矩陣及等式 | conditional paper proof；finite controls triggered and holds |
| 12張原四查詢no-go | triggered and holds |
| 兩張新圖在U=V=0時為較小bad | conditional paper proof；未構造實際來源 |
| 全域最小原來源迫U+V>0 | conditional consequence using explicit minimality |
| 真cone整圖full fibres | triggered and holds；原來源合同not triggered |
| 真完整r6／933來源圖 | not triggered |
| 16維必要系統可行／來源可實現 | OPEN；沒有聲稱 |
| 一般933排除／實際較小bad／K∞／Lean | OPEN／未得／OPEN／無新增 |

保留 `probe.py`、`closure_probe.py`、`identity_probe.py`、`nogo_probe.py`及
`closure-0.json`、`closure-1.json`為非權威診斷；最終結果以紙證、certificate、
check.py及independent-certificate為準。初版獨立枚舉遇到未用色名的重複軌道，
在生成獨立證書前改為按同一完整字面tuple去重；沒有覆寫任何既有證書。
