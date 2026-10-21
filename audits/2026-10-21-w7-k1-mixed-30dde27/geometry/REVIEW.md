# 原 mixed 排除與完整 E 閉包：只讀獨立量詞審核

2026-10-21。PASS；本項沒有重跑132型或新來源枚舉。
本次實際讀取的五份 paper／code 原 bytes 與 SHA256 固定在
[REVIEW_INPUTS.json](REVIEW_INPUTS.json)，快照都留在本 `geometry/frozen/`。
以下結論適用這一份精確快照。

## 1. 原 E 的132型與完整動作

`exterior/REPORT.md`、`exterior/check.py` 的必要覆蓋正確：原 E 是同一
triangulated C13 disk，兩palette全部boundary contacts為NC；同palette
相鄰原邊強制同block，12個transitions迫總共七個boundary components。
active-block完整遞迴與獨立Bell(6)²逐partition pair比較逐項一致，沒有偷用
舊 D filtered columns 作 E 的可行型。

每個型的128個動作都可由同一實際E著色的七個完整boundary components
選擇交換產生；全部私有點一起作用，其他boundary-free分量可以原相位
不動。每個動作固定一份當前完整E，再枚舉六P全部共同延伸與原全部caps，
所以不是邊界點獨立翻色、也沒有補滿目的fibre。空P延伸不作E零值。
cap canonical ID僅供矩陣比對，逆置換全域施於同一份完整cap，沒有獨立換框。

u3／u1每個必要型各有禁止01021的真完整action，故量詞可排這兩個原細分支。
L的38存活型只屬本kernel必要型，不是來源實現或各palette共同模型。

## 2. 原 D 完整欄與 marked Y

`transport/PROOF.md`、`transport/check.py` 以原兩target全部incident
columns分案；每個zi與其唯一同palette原P端點有原邊，故實際分量身份
精確固定。Y在缺側palette與其局部鄰點分離；將其實際分量分為任一
同palette rim block或boundary-free，為完整且互斥的必要分類。

每份標記的整個原component動作保其全部E私有點同步變色；再以同一當前
E重色六P，完整cap逐份接回。F0與F1–F3所給單分量、P色列與cap都滿足
原邊。沒有要求最初target可接回G，也沒有為後繼觀測另找新來源。

L的01 strip僅三片pendant leaves `n–a,u3–z2,u1–z4`；不合併不同E塊。
所以D迫Y與a／c同塊，可以嚴格降到同一E；這不自行迫z4，後者須父閉包。

## 3. full_exterior.py 的零種子與跨palette必要閉包

父 `full_exterior.py` 的 zero_seeds 枚舉**全部原E boundary canonical
states**及其全部六P共同延伸。若某個延伸是原D已證零state，則任何具有
該E boundary的完整E著色都能接這一份P延伸，構成零D著色；因此該E state
確為零。無P延伸的E fibre明確保留，沒有把空D fibre反推成空E fibre。

universal C13 columns由未過濾完整NC族重建、核原全family SHA。舊D零值
只用於上面的合法零種子，不作E universal family的刪除authority。
原E可能有弦不影響原disk orbit lemma；其實際著色orbit仍包含在這個族。

每輪只做兩種必要歸納：碰已證零half-row的整個column為零；若某個
half-row已無可能actual orbit column支援，所屬完整canonical E state為零。
同一state的三個palette split共享同一全E著色域，所以此刪除可以相互傳播。
程式以all states／all columns保留這個共同關係，沒有把不同palette的
獨立可行partition拼成一份來源，也沒有宣稱共同計數錐可行。

L_residual對同一最終column重建全部boundary blocks，讀出Y所在完整block。
因此 `{a,z4,Y,c}` 是對每個實際存活來源分量的必要接點結論；有限存活
數4／2／1仍不是E來源實現。對應幾何報告的F必須引用這份必要閉包，
不能只引用前兩個較弱單palette審核。

本review沒有發現實質量詞或same-source漏洞。其限制：核對的是紙證合同
與程式語義，未另行重建132型、428506全族或根證書數值；數值重播由各自
checker與父獨立checker負責。本目錄小控制只校準原短圈star，不代替那些證書。
