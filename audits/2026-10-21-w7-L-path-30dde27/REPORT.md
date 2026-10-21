# W7 profile0／K=1／L：三邊路兩短型與至少五邊長路

2026-10-21；exclusive BASE `30dde27293b5d3ad63c75fae73cda5be96db705b`。

**新排除僅一個來源子支：雙五度型 II、target44466、U=原w。**
普通六度型 I 及普通雙五度型 II 經同一外側、全分量作用、完整共同延拓及原
cap 後仍有必要型，未整型排除。五邊最短路已分類成七種原接線型，並迫出
三個七度＋五度型及一個八度型；另外三型保留任意內點數的 induced C6／C7。
四個原L必要01型、L整支、profile0／1及一般W7均仍OPEN。

## 固定來源與本輪證據

[BASE.json](BASE.json)固定15份輸入，區分Git BASE已提交authority與前輪未提交
audit的精確bytes／SHA。只新增本exclusive目錄，沒有改舊audit或共享文件。
承接[原來源契約](frozen/audits/2026-10-20-r6-941-j1-five-edge-417732f/SOURCE_CONTRACT.md)、
[原完整E閉包](frozen/audits/2026-10-21-w7-k1-mixed-30dde27/FULL_E_PROOF.md)
及[父完整v3證書](frozen/audits/2026-10-21-w7-k1-mixed-30dde27/full-exterior-v3.json.gz)。
原rotation、所有完整原stars、附件、非邊、私有點、全部空fibres與full lifts均保留。

固定同一原D，令`P=(n,u4,u3,u2,u1,L)`、原色`121212`，原`E=D−V(P)`。
其有序原框與字面色為

```text
∂E=(a,z1,z2,z3,z4,z5,Y,q,c,s,v,w,t)
φ  =(0, 3, 0, 3, 0, 3,1,3,1,2,e0,e1,2)
target A44459：(e0,e1)=(0,1)；B44466：(e0,e1)=(1,0)。
```

Y是唯一原H_L點；程式名`HL_0`。原L四型是同一完整K01^E(Y)的contacts

```text
{a,z4,Y,c}，{a,z2,z4,Y,c}，
{a,z4,Y,c,v,w}，{a,z2,z4,Y,c,v,w}。
```

每個target在原E的01／02／03 splits各有4／2／1個必要整partition。
這些是任意真來源必須通過的條件，並非已實現的共同來源。以下沒有把各
palette的獨立存活型拼成一份原圖，也沒有每次重色後重新補滿初始fibre。

## 三邊路：完整star、同一界面及一個真排除

若同一原E有`Y1–U0–V1–z4(0)`，原C5 pocket只容許兩型：

| 型 | 全部原內點與完整star |
| --- | --- |
| I，六度 | `d(z5)=6，N(z5)=(L,u1,z4,V,U,Y)`；原Q5內部空 |
| II，雙五度 | `d(z5)=d(K)=5`；`N(z5)=(L,u1,z4,K,Y)`，`N(K)=(Y,U,V,z4,z5)`，原K色2 |

兩型都有同一原induced界面`B6=(L,u1,z4,V,U,Y)`，其有界側原內點恰為
I的`{z5}`、II的`{z5,K}`。所有界面點的外側附件仍留在同一余圖。
[幾何紙證](geometry/REPORT.md)證明完整界面、所有允許的原點重合及rotation。

U/V不能預設為兩個新私有點。原03 q→零色tip的crosscut及完整12分量迫出：

| 型／target | 尚未排除的U身份 | 尚未排除的V身份 |
| --- | --- | --- |
| I／44459 | E私有 | E私有或原w |
| I／44466 | E私有 | E私有 |
| II／44459 | E私有或原v | E私有或原w |
| II／44466 | E私有 | E私有 |

最後一行的`U=原w`是本輪新增排除：父完整v3中，B的02必要整欄只有
220297、220299，其02塊分別為

```text
220297：{a,z2,w,t} ／ {z4,s}
220299：{a,w,t}    ／ {z2,z4,s}。
```

所以同一原E的w和z4必分離。但型II若U=w，完整原K色2、同時接w0與
z4(0)，原路`w–K–z4`把它們接通，矛盾。這不是邊際接點拼合。
全部整欄、其原orbit及SHA保存在[ALIAS_02.json](geometry/ALIAS_02.json)，
根[check.py](check.py)另直接讀frozen v3重核。A的原v與z4本來同塊，
故這個論證不能排A的U=v，也不能排II整型。

## 三邊路：完整混色作用結果與保留界線

I令`F=D−(P,z5)`；II令`F=D−(P,z5,K)`。固定同一份實際完整F著色後，
共同枚舉所有七點／八點proper延拓，再接同一D的原G／Q1／J1全部cap。
原相位9種身份分案（包含上面已排但局部仍可著色的B alias對照）各有六份
共同延拓，共54份；沒有禁cap。根證書保每個tuple、所有cap原賦值及空列。
這也說明不能從局部六份延拓推來源可實現。

當U、V都私有，F才確是simple C14 disk，有序原框

```text
(a,z1,z2,z3,z4,V,U,Y,q,c,s,v,w,t)。
```

其指定literal的01／02／03 transitions為10／10／8；完整必要NC型為
42／42／14。每個型都作用於同一F的完整分量，含全部私有點，再接全體共同
延拓。初始F須先把原z5（及II的原K）完整加回、以原邊DSU合併，投影
到同一初始E並通過父4／2／1 gate。這一步不能以個數相同或可分別延伸代替。

| 普通私有U/V型 | 初始同E gate＋全分量作用＋完整cap後，01／02／03必要型 |
| --- | --- |
| I，六度 | **4／4／2**，兩target各自如此 |
| II，雙五度 | **4／4／3**，兩target各自如此 |

[六度完整證據](six_degree/REPORT.md)保存全部七點共同延拓、1964個用到的
cap states之完整assignments；父v2／v3的L整欄已逐字比對相同。
[雙五度完整證據](double_five/REPORT.md)保存全部八點共同延拓、完整原D零與
G／Q1／J1 cap，及alias同點合併後的必要cover。兩份都沒有排掉普通短型。
以上是分palette的必要存活型數，不能相乘來算原來源。

六度03 split還迫出同一初始F內的二選一：U的03塊接原a弧而V的12塊只有
V這個boundary contact；或U的03塊只有U這個boundary contact而V接原Y的
12塊。兩種接合互斥，必有其一；「只有一個boundary contact」仍可含任意
私有原點。這是下一步共同來源幾何的具體義務。

若V=w或II的U為原tip，暴露walk重訪原點，不能套simple C14 theorem。
I的V=w目前只完成兩原E01型的全128個合法動作，其他pinched-F splits仍OPEN。
II的alias先按實際原點quotient，再列強制同palette邊下的全部set partitions，
不加simple-disk NC／transition限制，故是保守完整必要cover；存活不證可實現。

## 完整界面否決一個通用較小替換捷徑

根證書獨立保存全部31個proper canonical B6色列的完整內部fibres，包含空列。
令s為原z5色、k為原K色，其精確式為

```text
I ：s不在σ(B6)中。
II：s∉{σ(L),σ(u1),σ(z4),σ(Y),k}，
    k∉{σ(Y),σ(U),σ(V),σ(z4),s}。
```

兩型在14個B6色列上連nonemptiness都不同。例如`010102`的I fibre是
`s=3`，II fibre為空；不能將雙五度直接換成六度。兩型又都接受兩色框
`010101`。任何保同一六圈、沒有內點的triangulated patch都拒絕此兩色框。
若只有一個內點而接受它，則每個三角面都必含該點，故patch只能是W6；
但W6已由`010102`證明不等於II。於是這個**全B6關係相等、嚴格少內點**的
通用disk替換途徑不成立。未排除依實際外側纖維而定的較小bad，也未證明
任何替換保941／原最小性契約。

## 長路：五邊七型及任意奇長的gap引理

若最短01路恰五邊，寫成

```text
Y=X0–X1–X2–X3–X4–X5=z4，色101010，Z=z5色3。
Q7=(X0,X1,X2,X3,X4,X5,Z)。
```

路因最短而induced；Q7可能的原弦只有Z到中間Xi的spokes，且按原rotation
都在其有界側。Q7有界側在同一原E內，舊R在E外。依原C3／C4／C5定理，
相鄰spokes的maximal gap不能為2；gap1是原面，gap3迫唯一原五度中心、色2。
全部16個spoke子集恰剩下列七種：

| Z向中間Xi的原spokes | maximal gaps | 精確原結構 |
| --- | --- | --- |
| ∅ | 5 | induced C7 cell，內點≥1，未得上界 |
| {1} | 1+4 | 原面＋induced C6 cell，內點≥1，未得上界 |
| {4} | 4+1 | induced C6 cell＋原面，內點≥1，未得上界 |
| {1,2} | 1+1+3 | **d(Z)=7**，一個原五度K |
| {3,4} | 3+1+1 | **d(Z)=7**，一個原五度K |
| {1,4} | 1+3+1 | **d(Z)=7**，一個原五度K |
| {1,2,3,4} | 1+1+1+1+1 | Q7內部空，**d(Z)=8** |

這裡完整度數包含另一側原link弧`Y,L,u1,z4`；不是只數已見spokes。
若另假設前三型的殘餘cell恰一原內點，才各為原W7／W6／W6，分別
`(d(Z),d(K))=(5,7)/(6,6)/(6,6)`。這只是明示的one-hub子案，不能推廣到
原cell有兩個以上內點，更不能把新K識別成原R。

對任意最短奇長ell≥5，同一原路加Z仍有相同gap規則：gap1原面、gap2
不可能、gap3唯一原K5、gap≥4為內部未定的更大induced cell。若全部gaps
都在{1,3}且其中r個gap3，則這r個原K5互異，封滿原Z星型，精確

```text
d_G(Z)=ell+3−r。
```

這個一般引理保留至少七邊路的結構義務；五邊的七型沒有冒稱涵蓋更長路。
完整Jordan、原面及link紙證、微型拓撲校準見[geometry/REPORT.md](geometry/REPORT.md)。

## 驗證與下一個窄問題

根[check.py](check.py)獨立核對frozen／live輸入、31個全B6關係、9種身份的
54份原相位共同tuple、所有原cap assignments與兩個B02整欄。三份子項另做
全分量作用、exact initial join、16個spoke子集及原面拓撲校準。
normal與seed17 optimized重播一致，污染完整lift／alias／source scope的
負控制被拒絕；逐份SHA與receipt見[verification.json](verification.json)。

下一個窄問題是I的03互斥接合如何與同一F的02四型共同存在，以及II剩餘
4／4／3型的相同問題；同時保留pinched-F身份分支。長路則先追五邊中
已封滿star的七度＋五度／八度型，再追前三型的多內點induced cell。
本輪沒有新來源實現、完整計數錐、LP、Lean、matching、合法較小bad或一般
W7／J1／J2結論；沒有commit／push。
