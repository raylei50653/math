# L三邊路型 I：原z5六度完整star與同一外側七點關係

2026-10-21；exclusive BASE `30dde27293b5d3ad63c75fae73cda5be96db705b`。
[BASE.json](BASE.json)凍結九份輸入，區分Git BASE原authority及前輪未提交證據。
完整承接原941／Q1接受零／J1 type III／strict W7
[來源契約](frozen/audits/2026-10-20-r6-941-j1-five-edge-417732f/SOURCE_CONTRACT.md)。
同一原G、C5字面框、完整原star、rotation、全部私有附件、空fibres與full lifts均保留。

**本項尚未排除六度型 I。** 已完成：普通 U、V 均為原E私有點時的合法十四圈
界面、全部七點共同延伸及三個指定literal split的完整分量作用；與原E初始
4／2／1型精確接合後，分別仍有4／4／2個必要型。另證U必私有，V唯一可能
的舊框身份為target44459的w；該別名沒有套用普通十四圈NC定理。

## 1. 固定原短路與z5的完整六度star

只看profile0、K=1、唯一障礙Y在H_L。兩個原target均固定

```text
P=(n,u4,u3,u2,u1,L)，色121212；
A=(a,z1,z2,z3,z4,z5,Y,q)，色03030313；
(c,s,v,w,t)=(1,2,0,1,2) 或 (1,2,1,0,2)。
```

前輪[原三邊路紙證](frozen/audits/2026-10-21-w7-k1-mixed-30dde27/geometry/REPORT.md)
考慮同一完整E01分量中的原路

```text
Y1–U0–V1–z4(0)，Q5=(Y,U,V,z4,z5)。
```

型I指Q5有界側空。原三角化迫z5–U、z5–V兩邊，封滿原完整cyclic link：

```text
d_G(z5)=6，N_G(z5)=(L,u1,z4,V,U,Y)，允許整體反向。
```

本項沒有給U、V任何完整度數上界；它們的所有其他原附件始終留在外側。

## 2. U必私有；V只剩私有或target44459的w

原短路證明已給U、V在S外，不能識別成原A中的其他點。U、V在原D中，
也不能是已刪去的cap點。若它們碰舊E框，只能按當前字面色為：U是色0的
q-tip z0；V是c或另一個色1的v／w點。

但原z5–U是03原邊，且z5屬原完整K03(a)，故U亦屬該同一實際分量。
原z0屬另一完整K03(q)，兩分量不同，所以U≠z0，**U必為原E私有點**。

再取同一原K03(q)中的q→z0 proper crosscut。前輪已證它把完整K12(Y)
與完整K12(c)分到兩側，z5在Y側。原邊z5–V不遇這條03路：V色1，z5在
不同03分量，兩端均不在crosscut上。因此V同在Y側，不可能屬K12(c)。
這排V=c及target44466的V=v。唯一尚容許的舊框身份是

```text
target44459：V=w1；其他情形V必原E私有。
```

這是同一原crosscut分隔下的真實身份限制，不是依兩份獨立palette模型拼接。

## 3. 固定同一F，七點共同重著色的完整fibre

令

```text
F=D−(V(P)∪{z5})。
```

固定一份實際完整F著色，保U、V的實際色與所有附件不動。P的全部原外鄰點
已由原完整link列出，z5完整star亦已封滿，所以可同時枚舉七個原點
`(n,u4,u3,u2,u1,L,z5)`的所有proper延伸。這些tuple與同一D的完整fibre
逐份雙射，沒有獨立挑選各點列表或遺漏未知z5鄰點。

原相位下兩個target各恰六份完整延伸：

| P字面色 | z5色 |
| --- | ---: |
| 121210 | 2 |
| 121210 | 3 |
| 121212 | 3 |
| 121230 | 2 |
| 212120 | 3 |
| 212130 | 2 |

每份再逐份接原G／Q1／J1全部完整cap。原G的cap fibres在此六列均空；
Q1、J1有各自可產生01021的列，但它們各自禁止的是其他原框列，故不矛盾。
沒有要求原target本身可接回G，也沒有把「無G lift」誤稱為D或F零fibre。

## 4. 普通U、V私有時，F確是完整C14 disk

若U、V均不在原E框，原E內的z4–V–U–Y是proper crosscut；它與原
z4–z5–Y框弧圍出的恰是型I三個原三角面。移去這個原面ear及z5後，另一側
是實際triangulated disk，完整有序界面為

```text
B14=(a,z1,z2,z3,z4,V,U,Y,q,c,s,v,w,t)，
literal=(0,3,0,3,0,1,0,1,3,1,2,e0,e1,2)。
```

沒有漏原附件：移入內kernel的全部點恰原P及z5，其外接觸全部在B14。
程式另核原面strip加完整z5扇形共有16點、15個三角面、單一15邊界，
唯一strip內點z5；這是原面拼接的有限校準，不是新來源圖實現。

**01 split的transitions是10而非12。** 原z4–z5–Y的兩次palette transition，
改成z4–V–U–Y的單一01 run後消失。因此01／02／03三split分別有
10、10、8個transitions，碰B14的完整分量數為6、6、5。指定literal的完整
必要NC型分別為42、42、14；它們的完整分量作用數為64、64、32。

每個literal都直接從原plane triangulated disk lemma產生全部必要型；另以
同palette cyclic runs的全部集合分割獨立校準，01／02各Bell(5)²=2704對，
03為Bell(4)²=225對。02的首尾run相接，明確合併原t–a邊，沒有漏掉seam。
沒有生成通用C14 family、任意大小來源圖或LP。

對每個必要型，枚舉其兩palette所有碰框的**完整實際分量**翻色組合。
不碰框的私有分量可保原色；選中的分量則連同其全部原私有點一起翻。
每個像都固定同一份完整F著色，再接全部七點共同tuple及完整原cap。
有些像的七點fibre為空，照樣保留該F像，不能拿空內fibre推外側為零。

## 5. 與原E的4／2／1型在同一初始著色上精確join

F的初始partition不是獨立於原E可任選。本項把原z5=3加回，依其在E中的
全部原鄰點`{z4,V,U,Y}`合併同palette分量，然後投影到原十三圈B13。

* 01：z5與這四點全異palette，所以z5新增一個23孤立boundary block。
* 02：z5、V、Y同屬13，必把V與Y所在F13塊合一。
* 03：z5、z4、U同屬03，必把U與z4所在F03塊合一。

只有這個**同一初始F著色**的精確join，才與前輪原E完整必要4／2／1型比較。
之後真實F動作的像不被強行補滿或重新套成初始target；各步只接其完整內fibre。

本項凍結前輪v2完整證書；其`L_complete_residual`已逐字對比父審核凍結v3，
包含兩target的全部整column與component blocks，完全相同，見
[v2／v3比較receipt](parent-v2-v3-L-residual-equality.json)。不是只比4／2／1個數。

結果如下，兩target各自相同：

| split | 指定literal完整NC型 | 全F作用＋cap後 | 再保同一初始E residual gate |
| --- | ---: | ---: | ---: |
| 01／23 | 42 | 20 | **4** |
| 02／13 | 42 | 4 | **4** |
| 03／12 | 14 | 2 | **2** |

所有通過初始E gate的型，都通過全部F作用＋七點＋cap。因此這個完整有限kernel
沒有排掉型I；也沒有用不同palette各自存活，宣稱有一份共同原來源。

**03 split留下的一個精確二選一義務。** 在同一初始F中恰為下列之一：

1. U的03塊接`{a,z1,z2,z3,z4}`，V的12 boundary block僅`{V}`；
2. U的03 boundary block僅`{U}`，V的12塊接原`{Y,t,w}`（target44459）
   或`{Y,t}`（target44466）。

所以繞過z5的U→a03接合，與V→Y12接合在同一F partition中互斥。
「僅一個boundary contact」仍容許任意原私有點，不能解讀成單點分量。
02 split亦按每個原E兩型，各留「U併z4塊、V為孤立boundary block」或
「U為孤立boundary block、V併Y的13塊」兩個必要型；全部整型見證書。

## 6. V=w別名保原身份，不套單一C14定理

target44459的V=w時，暴露walk為

```text
a,z1,z2,z3,z4,w,U,Y,q,c,s,v,w,t，
```

原w重訪，只有13個不同點。F的單一簡單C14前提不成立；原邊及附件仍保留。
本項只以原E的完整01分量動作做合法控制：因V=w且原Y–U–V是01路，
必選原四型中w與Y同塊的兩型；U亦在同一完整01分量。其全部128個實際E
boundary-component作用，連同U／w共同翻色後，固定同一F再枚舉七點完整
fibre與cap，兩型均未矛盾。

這個別名控制**沒有**涵蓋pinched F的02／03完整分量型，也沒有將兩個disk
或cutvertex圖的NC條件冒充普通C14條件。別名的其餘來源幾何仍OPEN。

## 7. 證書、重播與停止點

```sh
python3 -B audits/2026-10-21-w7-L-path-30dde27/six_degree/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-21-w7-L-path-30dde27/six_degree/check.py --seed 17
```

[certificate-v2.json.gz](certificate-v2.json.gz)保六個ordinary literal/split cases的
全部必要partition、全部真分量作用、每個像的全部七點延伸、1964個用到的原cap
states之全部完整assignments，以及V=w的兩個實際E01型全部動作。cap canonical
表示以同一D tuple的全域逆色置換還原literal完整cap，不獨立換框。

第一版[certificate.json.gz](certificate.json.gz)保留：初次build的驗證失敗是
記憶體tuple與JSON list比較不同，非數學數值差異；改為序列化後的同型表示，
另建v2，沒有覆寫首證。normal／seed17含打亂列表與像處理順序後逐字相同。

八個負控制含：冒稱型I已排、冒稱來源實現、跨palette拼來源、冒稱通用C14
枚舉、拿空內fibre當外側零、錯認01有12 transitions、把V=w視為簡單C14，
以及刪一份七點完整lift。另做外部污染完整action像的拒絕控制。SHA及正常／
seed17結果見[verification.json](verification.json)。

已完成：原身份與合法界面、完整七點fibre、三個指定split全作用及同初始E
gate、03精確二選一。尚缺：普通型I三palette的共同來源幾何或矛盾、V=w的
其餘完整pinched-F分析、型II、最短路至少五邊情形、整個L／profile0／1／
一般W7／J1／J2、較小bad與主命題。沒有新來源實現、LP、Lean或matching結論。
僅改本exclusive目錄，舊audit與共同文件未改；未commit／push。
