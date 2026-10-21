# Root短型整合與六度F gate：只讀獨立review

2026-10-21。精確三份原code／report快照見
[REVIEW_INPUTS.json](REVIEW_INPUTS.json)，均留在geometry/frozen/。沒有重枚舉
42／42／14型或新來源圖。

## 1. 根checker：PASS

根`check.py`直接由原完整stars核31份proper B6色列、兩型全部內點tuples，
包含所有空值。9個U/V原身份分案保同一點身份；已被同E02排除的型II／B／
U=w仍可作局部校準，程式明確標其不屬原來源，沒有把六份局部延伸當實現。

每份短型共同mutable集合為原P加z5，型II再加K。這些點的完整原stars都已
封滿，外面任意原附件只接固定boundary點，故局部共同延伸可接回同一實際
余圖。六份initial共同色列逐份接原G／Q1／J1所有完整cap，原字面色框共用，
對原三矩陣計數交叉核對；沒有以獨立列表／獨立cap或不同E拼接。

same_E_alias精確讀父B572的兩份完整02column：w和z4在每份都不同塊，
而原w−K−z4色020路將它們連起，足排這一個alias來源子支。A560的
v／z4本來同塊，程式不把此排除誤用到A，亦不排整個型II或L。

## 2. 普遍全B6嚴格較小替換障礙：PASS，限triangulated disk合同

兩色boundary `010101` 在兩原patch都有lift：型I內色2或3；型II內色對
23或32。任何同一simple B6的0-inner triangulated disk，其三角面全在
兩色rim上，無proper lift，所以不能替代型I。

任何1-inner triangulated disk若能接受這份兩色rim，每個原三角面都必含
唯一內點；否則只用兩個boundary色的三角面必衝突。因此所有面均圍此內點，
圖必是完整W6。可是boundary `010102`，W6有唯一內色3，原型II完整fibre空。
所以型II也無同一全B6支援相等的≤1-inner替換。

這個論證甚至用完整支援的非空／空就足夠，不需要相等計數。它只封閉
**全boundary普遍、triangulated disk、完整有序B6不變、嚴格較小**合同；
不封閉原余圖限制下的條件替換、不同界面縮減或較小bad。

## 3. 六度審核的同initial F→E partition gate：PASS

`six_degree/check.py::add_back_z5`以同一份初始F著色、z5=3及其全部F鄰點
`{z4,V,U,Y}`精確合併同palette blocks，再投影原B13；沒有未知鄰點可漏。
01時z5新增孤立23 boundary block；02時合V/Y的13塊；03時合U/z4的03塊。
只對初始來源partition套父4／2／1 residual，完整F動作後的像不補滿成
初始fibre，量詞正確。

直接讀v2證書的兩target03完整存活F partition，確各恰以下二型：

```
U03塊={a,z1,z2,z3,z4,U}，V12 boundary block={V}；
U03 boundary block={U}，V12塊={V,Y,t}（A另含w）。
```

這是同一初始F上的互斥接合，不能在不同palette或不同來源間獨立選路。
單一boundary contact仍容許任意私有點，report沒有把它說成單點分量。
V=w別名只用原E的真完整01作用，沒有將pinched F套simple C14族。

以上沒有發現實質same-source或覆蓋量詞漏洞。數值大域重播由各自checker
與root獨立checker負責；本review不再重算必要partition族。
