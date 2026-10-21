# 同一原E的完整fibre零值傳播，及L的四種必要接觸型

2026-10-21；BASE `30dde27293b5d3ad63c75fae73cda5be96db705b`。
本項只處理 profile0、K=1、Y中心為u3／u1／L的原圖。
[原E拆分](../2026-10-21-w7-single-barrier-30dde27/exterior/REPORT.md)給實際
十三圈界面 `∂E=(A,c,s,v,w,t)`，P六點的全部外鄰在A，全部外側附件保留。
本項使用整個 `Col4(E)`，不是只取最初target的像或可延伸回原G的子集。

## 1. 同一E完整fibre給出的零種子

固定任意原E的完整著色ψ。令σ是其完整有序∂E字面色列。對每個P點，
用其**全部**A鄰點給可用列表，再枚舉六點共同proper延伸。
原圖的完整stars保證這些延伸與同一ψ的全部D延伸逐份雙射。

令 D(σ) 表示這些延伸的完整有序D rim色列。若存在一份延伸落在舊D的
已證零完整fibre，就得到同一原D的一份不可能著色，故原E的σ完整fibre亦零。
這裡舊D的零權威是[原完整orbit來源](../2026-10-20-r6-941-j1-five-edge-417732f/counting/PROOF.md)：
它作用於整個Col4(D)，不是只取121212路見證子集，因此可用於重著色P。

若D(σ)為空，只表示ψ無法延伸成D，**不能**判E fibre為零。
程式保留這個分支；本次三個shape的全部66,430個proper canonical σ恰皆有P延伸。

[full_exterior.py](full_exterior.py)的最終 [certificate v3](full-exterior-v3.json.gz)
逐σ保存全部六點字面P延伸與對應D state，包括重數，不只留可達state集合。
σ本身沿同一全域色置換正規化；全部P、D rim及原cap一起使用這個色框。
完整原cap計數由凍結三矩陣與完整stars決定；具體action域的全部cap assignments
另由[直接E核對](exterior/REPORT.md)逐份保留。

## 2. 必須重新使用未經D零值篩選的通用C13 family

原D存活的307,197欄不能當作E的完整family；D與E的cap關係不同。
本項從原NC生成法重建通用C13全部428,506欄，不施D的零值filter。
742,900個NC partitions中41,834個滿足原disk的必要條件；生成序列SHA
逐位元吻合原紀錄的未過濾full-family SHA：

```text
530aeac43e108f7c94f1e120ec341c18528d36dc3fd41356b5f3b79b3b94a7d5
```

[universal-C13.json.gz](universal-C13.json.gz)保全部整數欄與完整row-to-state map；
checker另釘住整份payload SHA，會拒絕刪欄或偷換成舊D過濾family。

原plane triangulated disk的實際完整分量orbit包含所有private點。
不碰邊界的分量只增加每個框tuple的共同正重數，不能從原圖刪掉。
依原完整orbit lemma，同一E的非負整數關係仍是 `2Z=ΣX`。
每個canonical state有三份split half-rows，共用同一完整Z fibre。

若一整欄含已證零state，該欄X必零；若某half-row的全部原incident欄皆零，
該state的完整Z必零。這是對同一來源的必要零值推論，不是把不同palettes
各自存活的欄拼成來源。每步完整incident集合均來自未過濾通用family。

## 3. 三個固定shape的結果

| Y中心 | 完整零種子 | 閉包存活E states／columns | 原兩target |
|---|---:|---:|---|
| u3 | 12,386 | 47,264／212,419 | E7548、7557皆第一輪零 |
| u1 | 12,642 | 47,156／212,111 | E987、996皆第一輪零 |
| L | 12,256 | 47,348／212,725 | E560、572皆存活 |

上述E IDs與舊D的44459／44466不是同一套座標，不能混用。
u3／u1已有更短的[單split完整作用證明](exterior/REPORT.md)，只需原G01021零列；
這裡作獨立全界面驗證。L存活不給共同計數錐可行解，更不給真實原來源。

## 4. L初始同一字面target的完整殘餘

L的原有序界面及色列為

```text
∂E=(a,z1,z2,z3,z4,z5,Y,q,c,s,v,w,t)，
σ =(0, 3, 0, 3, 0, 3,1,3,1,2,e0,e1,2)。
```

兩個target分別(e0,e1)=(0,1)或(1,0)。逐target、逐split完整保留：

| split | 未過濾全部incident欄 | 零種子後 | 完整閉包後 |
|---|---:|---:|---:|
| 01\|23 | 132 | 6 | **4** |
| 02\|13 | 14 | 4 | **2** |
| 03\|12 | 5 | 1 | **1** |

同一實際原E的完整K01(Y)接觸必為下列四種之一：

```text
{a,z4,Y,c}
{a,z2,z4,Y,c}
{a,z4,Y,c,v,w}
{a,z2,z4,Y,c,v,w}。
```

因此Y與a、z4、c在**同一份原著色的同一完整01分量**；z2及v/w有明確聯合分案。
在原D中，n、u3、u1分別只經a、z2、z4向E的01圖添pendant leaf，
所以K01(Y)還必含原n與u1。這不是宣稱四個框點間的路可獨立挑選。

02|13的Y分量必含 `{z5,Y,q,c}`，由原邊Y–q–c及Y–z5已給局部連通。
03|12仍為先前原兩塊接合：Y的12塊接t，第一target另接w。
完整whole columns、全部component blocks與零種子／每輪刪除在v3中保存；
程式以block signatures重新生成每一存活整欄，拒絕漏動作或錯anchor。

表中4／2／1是各split的必要殘餘；**沒有證明任何選擇可共同實現同一E**。
四型也不是四張來源圖，不能稱為來源存在證書或一般有限狀態壓縮。

## 5. 界線

u3／u1的原來源子案已排；L仍OPEN。後續可在這個同一E01分量內追
Y到z4／c的最短原路，結合原03 crosscut與C3/C4/C5 pocket。
[幾何細分](geometry/REPORT.md)把短路給出的原star義務與未排分案另行記錄。
所有更外側附件及原full fibres均保留；沒有新LP、Lean或較小bad。
