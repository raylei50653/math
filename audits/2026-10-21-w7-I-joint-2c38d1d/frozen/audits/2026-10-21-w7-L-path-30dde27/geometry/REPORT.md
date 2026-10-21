# L的原混色路：先核兩個短型完整界面，再追五邊路的七種原spoke型

2026-10-21；exclusive BASE `30dde27293b5d3ad63c75fae73cda5be96db705b`。
只寫本輪 `geometry/`；六份原authority的bytes／SHA及Git／工作樹來源分級
見[BASE.json](BASE.json)。沒有改舊audit或共享文件、沒有commit／push。

本項新增兩項原圖結構：短型皆有同一原induced C6完整界面及精確1／2內點；
五邊最短01路只容許七種原z5-spoke型，其中三型迫原z5七度及一個原五度
中心、全spoke型迫原z5八度。剩餘是induced C6／C7且本項未證內點數上界。
本項另排除型II／targetB／`U=原w`這一個alias來源子支，沒有排整個短型或L，
沒有把未知長路當成strict only-R wheel。

## 1. 固定同一原E的量詞

完整承接[原SOURCE_CONTRACT](frozen/audits/2026-10-20-r6-941-j1-five-edge-417732f/SOURCE_CONTRACT.md)、
[原第二層定理](frozen/audits/2026-10-21-w7-profile0-13e51db/PROOF.md)、
[原第三面點與完整link](frozen/audits/2026-10-21-w7-private-face-points-d23f94f/PROOF.md)。
固定原941、原C5色框、全域最小性、所有原stars／rotation／附件／非邊、
原C3/C4/C5 pocket定理及全部完整fibres；不使用四色定理或matching。

只看profile0、K=1、唯一H點Y位於H_L的來源子型。原

```
P=(n,u4,u3,u2,u1,L)，色121212，
A=(a,z1,z2,z3,z4,z5,Y,q)，色03030313，
∂E=(A,c,s,v,w,t)，(c,s,t)=(1,2,2)。
```

兩target保原身份：A44459的(v,w)=(0,1)，B44466的(v,w)=(1,0)。令z0為
色0的舊tip（A的v／B的w），z1_old為另一色1舊tip（A的w／B的v），避免
與原第三面點z1混淆。原所有未知外側附件仍在同一實際E。

[父完整E必要閉包](frozen/audits/2026-10-21-w7-k1-mixed-30dde27/FULL_E_PROOF.md)
已迫同一完整K01^E(Y)的boundary contacts恰下列四種之一：

```
{a,z4,Y,c}，{a,z2,z4,Y,c}，
{a,z4,Y,c,v,w}，{a,z2,z4,Y,c,v,w}。
```

原E03(q)的boundary contacts恰{q,z0}；原E03(a)包含a與全部z1,…,z5。
取同一份原著色的一條簡單03原路`Q:q→z0`。Q是proper crosscut，將整個
K12(Y)放在含Y,t的外側、整個K12(c)放在含c,s的另一側。兩target的原12塊為
`{Y,t,w}/{c,s}`及`{Y,t}/{c,s,v}`。這些完整分量與Q取自同一實際E，
沒有用各自存在的路拼來源。

下文所有01路都在這一份完整K01^E(Y)內。Y與z4色不同，最短路長為奇數；
原S induced排一邊路，故先核三邊，再進至少五邊。

## 2. 三邊路兩型的完整界面，不漏U/V與舊tail的識別

若有三邊原路`Y1–U0–V1–z4(0)`，[前輪原C5紙證](frozen/audits/2026-10-21-w7-k1-mixed-30dde27/geometry/REPORT.md)
已證U、V在原S外，且原`Q5=(Y,U,V,z4,z5)`只有：

```
I：d_G(z5)=6，N_G(z5)=(L,u1,z4,V,U,Y)；
II：d_G(z5)=5，N_G(z5)=(L,u1,z4,K,Y)，
    d_G(K)=5，N_G(K)=(Y,U,V,z4,z5)，φ(K)=2。
```

型II的K是Q5有界側原內點，因此必為D/E私有原點，不能識別為舊boundary
點s或t。兩型中U、V互異、亦與L,u1,z4,Y相異。

**完整原界面。** 兩型都得到同一原簡單圈

```
B6=(L,u1,z4,V,U,Y)。
I：int_G(B6)={z5}；  II：int_G(B6)={z5,K}。
```

它確是原induced C6。型I中完整六輪的非相鄰rim點若有原弦，與中心z5
成非面C3，違反原C3空內部。型II共同五輪排除所有共中心的非相鄰點弦；
其餘L／u1到U／V的邊因U/V在S外且不接原C而不存在，L−z4與u1−Y由原
C contacts禁止，Y−z4由S induced禁止。原面把界面有界側完全封滿成一個
disk，沒有未列內點。這不是只核六個點的邊際接觸。

固定任意同一份B6字面色列σ，完整patch fibres精確為：

```
I：s∈4色 \ σ(B6)，其中s是原z5色；
II：(s,k)，s∉{σ(L),σ(u1),σ(z4),σ(Y),k}，
             k∉{σ(Y),σ(U),σ(V),σ(z4),s}。
```

若σ不proper於B6，fibre為空。所有解逐份保留，包括所有空列。固定此
界面後，所有boundary原點的外側完整附件仍在同一余圖，沒有偷偷刪去。
這份公式可供短型重色／cap kernel共同使用，不是已完成較小替換。

### 2.1 U/V與原tail究竟可重合哪些

U色0，V色1，且皆在S外。舊E boundary中的全部候選因此只有
`U=z0`及`V=c或z1_old`。其餘a／z2／z4在S，s/t色2，均不是候選。

型II的原K2同時接Y1與V1，所以V在**同一完整K12(Y)**；故不能是c，
也不能是B的v（它在K12(c)）。型I的原邊z5−U迫U∈K03(a)，所以U≠z0；
U必為原E私有點。其短patch完全避開Q：Y、U、z4、z5在Q外側，V與
U／z4有原邊且不在Q上，也只能在外側。所以V及其完整12分量不能在
c側；再次排V=c及B的v。

| 原短型／target | U的完整可能身份 | V的完整可能身份 |
| --- | --- | --- |
| I／A44459 | E私有 | E私有或原w |
| I／B44466 | E私有 | E私有 |
| II／A44459 | E私有或原v | E私有或原w |
| II／B44466 | **E私有；原w分支由下節排除** | E私有 |

表中是尚未排除的必要身份分案，不宣稱每個笛卡兒組合均有原來源實現。
若U或V等於舊tip，01邊vw令兩tip都進同一K01(Y)，因此只可能落在上面
包含(v,w)的兩個完整01型；不能單獨標其中一tip而漏另一個。

**原02兩列排除型II／B的U=w。** 直接讀父完整v3證書的兩個完整02欄，
targetB的E state572只有220297／220299：前者的02塊是`{a,z2,w,t}`、
`{z4,s}`，後者是`{a,w,t}`、`{z2,z4,s}`。所以原w與z4在每個可能實際
02 partition都不同塊。但型II的原K色2，且同時鄰U=w0及z4=0，原路
`w–K–z4`直接將兩塊連起，矛盾。這使用同一E的兩條實際原邊，不是
把不同02欄的邊際接點拼合。完整兩target02欄與父v3 bytes／SHA保存於
[ALIAS_02.json](ALIAS_02.json)。targetA的02必要塊允許v與z4同塊，本項
不沿用此論證排A的U=v；型II的U私有及其他短型亦不由此排除。

### 2.2 重新暴露外側時不總是simple C14

若短型kernel把z5（及型II的K）收進內部，余原圖的有序outer-face walk為

```
(a,z1,z2,z3,z4,V,U,Y,q,c,s,v,w,t)。
```

當U、V皆為原E私有點，這是simple C14。若V是原w，或型II的U是原z0，
walk重訪該舊boundary點，余圖可在這個原點pinch，不能直接套simple-disk
C14的orbit family。型II/A若同時U=v、V=w，原vw邊在移去K後成為連接
兩個余disk的橋；這也不能冒稱成另一條simple boundary。

固定這個實際余圖、其全體點色及同一B6界面作full-fibre join仍完全合法；
是否為simple disk是另外的拓撲條件。短型kernel若只靠直接原stars枚舉
共同內部色列，不需要假設余圖為disk。所有原附件仍必保留。

## 3. 長路從五邊開始：Q7在原E內，R不在其中

現在假設Y到z4最短01路至少五邊。先處理恰五邊的具名子案：

```
P01=(X0,X1,X2,X3,X4,X5)=(Y,U1,U2,U3,U4,z4)，
色依序1,0,1,0,1,0。
Q7=(X0,X1,X2,X3,X4,X5,z5)。
```

最短路沒有任何非相鄰路點原邊：這些點均在E，若有原邊就仍是E的01邊，
直接給更短路。因此P01是原induced路。z5色3，不是路點；Y−z4由原S
induced禁止，所以Q7是原簡單C7。

Q7全部在原E closed disk，且沿其boundary兩邊z4−z5−Y閉合。E的外部
可連到無窮遠而不遇Q7，因此Q7有界側完全在E內。原R及原W7的八個原
內點都在E外，故都在Q7外；**它們不是新C7的內部hub**。Q7內點只能是
E私有原點，數量尚無上界。路可能中途碰原E boundary的a／z2等，不能
未經證明就說整條路是proper crosscut，但這不破壞Q7的上述有界側定位。

Q7全部可能的原弦恰為`z5−Xi (1≤i≤4)`。這些邊若存在，開邊一定在
Q7內：z5在E boundary，原內向E的整個link角正是Q7在z5的有界側角；
原邊不能離開這個角後再穿越Q7。故各spoke按路點原順序切成真正的原
subdisk cells。這一步保留原rotation，不是在抽象多邊形中任意挑對角。

## 4. 七種原spoke型：C3／C4／C5逐gap處理

令`I={i∈{0,…,5}:z5−Xi是原邊}`。原兩側邊給0,5∈I。
按序取I中相鄰兩指標i<j；其中沒有其他spoke，稱gap長g=j−i。對應原cell
為`(z5,Xi,X(i+1),…,Xj)`，所有path chords由最短性禁止。

- g=1：原C3有界側空，cell是原三角面。
- g=2：原C4有界側空，三角化須有對角；Xi−Xj是induced path非邊，故
  必有z5−X(i+1)，與maximal gap矛盾。**gap2不可能。**
- g=3：原C5的兩條可能對角只能是兩個中間spokes，均被gap定義排掉；
  所以其有界側不能空，原C5 pocket迫唯一原五度中心K。cell色含0、1、3，
  故K色2，接其全部五個boundary點，且完整原五度star保留。
- g=4或5：分別為原induced C6／C7，三角化迫至少一內點，但沒有原C5
  pocket提供的上界；本項不對內點數另設上界。

把總長5分解成上述可行gaps，四個中間spoke的原集合只剩七種：

| 中間spokes | maximal gaps | 原cell結構與z5完整度數 |
| --- | --- | --- |
| ∅ | 5 | induced C7 cell，內點≥1但尚無上界 |
| {1} | 1+4 | 一原面＋induced C6 cell，內點≥1但尚無上界 |
| {4} | 4+1 | induced C6 cell＋一原面，內點≥1但尚無上界 |
| {1,2} | 1+1+3 | 兩原面＋原五輪；**d_G(z5)=7**，K原五度、色2 |
| {3,4} | 3+1+1 | 原五輪＋兩原面；**d_G(z5)=7**，K原五度、色2 |
| {1,4} | 1+3+1 | 原面＋原五輪＋原面；**d_G(z5)=7**，K原五度、色2 |
| {1,2,3,4} | 1+1+1+1+1 | 五個原面、Q7內部空；**d_G(z5)=8** |

度數是精確值。原z5的另一側完整link弧仍是`Y,L,u1,z4`。三個gap3型的
外側完整弧各有兩個Ui及K，連同兩端Y,z4封滿原link，所以原四個既有
鄰點`{L,u1,Y,z4}`再加三點，恰七度。全spoke型外側加四個Ui，恰八度。
沒有餘下link角可插其他原鄰點，沒有漏外側附件。

若原d_G(z5)≤6，四個已封閉的高階型皆不可能；在恰五邊路子案中只剩
∅／{1}／{4}的較長induced cell。這個推論不是新的普遍度數上界。

## 5. 一般奇長最短路的原gap引理

固定同一份原著色，令最短01路長為任意奇數`ell≥5`，路點為
`X0=Y,X1,…,Xell=z4`。與原z5閉合所得原圈長`ell+2`。第3節的同一E
disk定位、原induced path及spoke原rotation論證逐字適用；沒有因ell變長
便改選E或補滿任何fibre。

對原z5全部spokes（包含兩端0,ell），逐相鄰指標形成maximal gaps：

```
gap1：原三角面；gap2：不可能；
gap3：唯一原五度中心K、φ(K)=2；
gap≥4：原induced (gap+2)-cycle cell，內點≥1，本項未證上界。
```

這是一般長度引理；第4節七型則只分類`ell=5`。

若這條原路的**所有**gaps都在{1,3}，令gaps總數為m，其中r個是3，則

```
ell=m+2r，
d_G(z5)=4+(m−1)+r=ell+3−r。
```

原四鄰點是L,u1,Y,z4；m−1個中間spoke點全為不同路點；每個gap3另給
一個原五度中心。不同gap的有界cell內部互不相交，所以這r個K兩兩不同，
且都不是boundary路點、舊tail或原R。gap1的原面和gap3的原五輪完全填滿
z5外側角，故度數是精確值，不是從有限例子猜的下界。

若存在任一gap≥4，上式不能直接使用：該cell內z5的原鄰點弧未知，可能
含多個原點，不能以一個假造hub替代。ell=5時r=1的三個已封閉型給七度，
r=0且五個gap1給八度，與第4節一致。

## 6. 一內點是假設分案，不能冒充任意C6／C7

對∅／{1}／{4}，若**另行固定**殘餘cell有界側恰一個原點K，三角化
迫它接整條cell boundary，得到條件結果：

```
∅：cell為原W7，d_G(K)=7，φ(K)=2，d_G(z5)=5；
{1}或{4}：cell為原W6，d_G(K)=6，φ(K)=2，d_G(z5)=6。
```

這裡的K始終是新cell內的**原點**，不是舊原R；舊R已證在E外。若cell
有兩個或更多原內點，上述star與度數不承接。不能僅因最短路長五便套
舊strict W7的only-R前提，也不能從有限one-hub校準外推一般內點數。

若最短路長≥7，仍有同一E的induced01路及原Q_(length+2)圈；本項的
七型是長度恰五的完整分類，不涵蓋更長路。原crosscut與同一01分量中
Y/a/z4/c的連通仍保留，沒有逐段選新來源。

## 7. 小控制與範圍

[check.py](check.py)只核對全部16個中間spoke子集及C4 gap2規則，精確得
七型；對三個gap3、全spoke及三個明確標作one-hub的殘餘cell建立微型
原面校準，核全部完整link、面數／Euler與顏色。另對兩短型的B6全部
proper canonical boundary色列，逐份比完整內點回溯與上節完整fibre式，
保全部空值，不枚舉新來源或未知E。
一般奇長gap式另以ell=5,7,9,11的全部spoke子集核對，並以獨立1／3有序
composition重生全封閉型，逐份校準精確度數`ell+3−r`；任意ell由紙證承擔。

normal／seed17 optimized一致；污染spoke coverage、gap2、hub色、以及
把one-hub條件冒稱一般來源的負控制拒絕。這些小圖未觸發完整941來源，
不作來源實現或排除；全稱來源必要性由上述原Jordan／rotation／pocket
紙證承擔。證據與SHA見`verification.json`及`runs/`。

完成：兩短型完整induced C6與1／2內點、全部tail識別候選及非simple余圖
界線；五邊最短路的七spoke型、三個原七度＋原五度star與一個原八度star；
剩餘induced C6／C7任意內點的精確OPEN界線；型II／B的U=w alias子支已排。
沒有新的純C3/C4/C5矛盾排整個短型。
短型是否由同一余圖重色＋cap排除交由兩份獨立kernel審核；本項不預告結果。
L整支、其他長度／K、profiles0／1、一般W7／J1／J2、完整計數錐、來源實現、
合法較小bad及主命題均未由本幾何項關閉，沒有新Lean／LP／matching。
