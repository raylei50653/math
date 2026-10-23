# 933第四輪：同一原C10六fibre，私有漏色只能經三條原橋

BASE `cb8f8593e273a7426ecadd59797a6e643cc4768e`；2026-10-23。
只寫本 `933/`，前三輪及shared docs不動，沒有commit／push。

**新source結論**：把原r,x,y的八個真三角面帽完整剝下，原E留下真disk
`D=(a,n,R,L,q,c,s,v,w,t)`。此邊界simple，未假設induced；原弦、私有點、
s,t≥6及全部附件保留。[紙證](PROOF.md)明列原點、邊、面、rotation和完整回填。

固定D前六點字面色`(0,1,0,2,3,0)`，把**全部**r,x,y lifts接回同一完整D
著色：24份能產U/V的尾tuple中18份另有回填到原E零字72或74，故整個D
fibre必空。只餘以下六個完整原D fibres，沒有把六列當六張來源圖：

| fibre | (s,v,w,t) | 全部(r,x,y) lifts |
| --- | --- | --- |
| A1 | (2,1,3,2) | (0,1,3)、(0,3,1) |
| A2 | (2,3,1,2) | (0,1,3)、(0,3,1) |
| CU1 | (3,0,3,1) | (2,1,3) |
| CU2 | (3,1,0,1) | (2,1,3) |
| CV1 | (1,0,1,3) | (2,3,1) |
| CV2 | (1,3,0,3) | (2,3,1) |

於是同一實際D的完整計數恰有

```
U=A1+A2+CU1+CU2,
V=A1+A2+CV1+CV2,
2(A1+A2)+CU1+CU2+CV1+CV2>0 （最後一式用原全域最小性）。
```

六fibre的同一完整02|13分量軌道逐子集交換，給更窄原幾何：在四份私有C
行中，**s,t在D13必不連**；原E13只以原路`s–x–y–t`接起兩側，三邊全是
完整E13分量的橋。CU的n,q在同一D13分量；CV另可有唯一交叉掛法
`n屬t-side、q屬s-side`。完整私有及rootless分量均保留。

兩組真逐點雙射也完成：A行的原13分量恰`{x,y}`，翻轉時整份D著色固定；
C行若n,q都不掛s/t兩側，翻同一完整E13分量把CU1↔CV1、CU2↔CV2，保同一D
及全部附件。故A或free-C任一正都使U,V同正；**單側漏色正只可能落在
r=2、v或w=0、nq掛橋的私有C瓶頸**。這是新的source正值分岔，未排除它。

[certificate.json](certificate.json)保70,144份完整generic帽fibres及67,593空
fibres、繼承全部p,h lifts、完整`z_E=K d_D`，並接回G/T0/T1全部十列計數。
本輪不重啟Q1／Q2／fan-B、不篩56支持證書、無廣泛來源圖枚舉或LP。
244份具名分量候選完整保子集輸出；A各12份留3、CU各55份留5、CV各55份留6。
存活只是未被此必要測試排除，不宣稱可行或可實現。

[independent.py](independent.py)不import producer，以另一個r缺色公式和
分palette分割枚舉重建所有kernel及分量清單；另存六份真disk完整著色控制，
包含會隨交換移動的私有點及固定rootless分量。控制不具完整原來源合同，
source一律not triggered。13份數學輸入bytes／SHA及routing界見
[INPUTS.json](INPUTS.json)，重播與exitcode見[VERIFICATION.json](VERIFICATION.json)。

```
python3 -B audits/2026-10-23-three-mask-round4-cb8f859/933/check.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-23-three-mask-round4-cb8f859/933/check.py
python3 -B audits/2026-10-23-three-mask-round4-cb8f859/933/check.py --negative
python3 -B audits/2026-10-23-three-mask-round4-cb8f859/933/independent.py
```

| 權威／控制 | 狀態 |
| --- | --- |
| 真C10分解、完整回填、18/24整fibre排除 | conditional paper proof；finite reconstruction triggered and holds |
| C私有原13橋、nq掛法、兩組完整雙射 | conditional source theorem；finite controls triggered and holds |
| 原最小來源至少一個A/C完整D fibre正 | conditional consequence using original minimality |
| 真disk逐點交換控制 | triggered and holds；完整來源not triggered |
| 6份剩餘fibre／分量的來源可實現或必要可行 | OPEN；沒有聲稱 |
| 六fibre皆空／一般933排除／實際較小bad／K∞／Lean | 未證／OPEN／未得／OPEN／無新增 |

下一義務是原D配對A/free-C正支或掛橋私有C正支的同源排除／可回填縮減。
六fibre全空才會完成第三輪兩張k−2較小bad的零值義務，這一步仍未得。
早期`probe.py`、`D-probe.json`及`D_component_probe.py`只留診斷；最終以紙證、
checker與certificate為準，未覆寫舊證書。
