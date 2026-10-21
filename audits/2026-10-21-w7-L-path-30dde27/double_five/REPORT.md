# L三邊路型II：雙五度共同kernel、原點重合與一個精確子案排除

2026-10-21；exclusive BASE `30dde27293b5d3ad63c75fae73cda5be96db705b`。
[BASE.json](BASE.json)凍結十份authority的原bytes／SHA；正式原輸入對回Git
BASE，前輪未提交審核另標 `prior-working-tree-audit`。只寫本 `double_five/`，
未改舊證據、共享文件或push。

**已排：原target B44466中，型II三邊路的U恰為原w的子案。**
原八點共同重色本身沒有排除型II；U／V均私有的三split必要型仍為4／4／3。
其他原點重合分支也仍有必要型存活。各split未被證明可共同實現同一F。

## 1. 固定原來源及兩個真正完整五度star

完整承接[原來源契約](frozen/audits/2026-10-20-r6-941-j1-five-edge-417732f/SOURCE_CONTRACT.md)、
[原短路幾何](frozen/audits/2026-10-21-w7-k1-mixed-30dde27/geometry/REPORT.md)
及[父完整E零值權威](frozen/audits/2026-10-21-w7-k1-mixed-30dde27/FULL_E_PROOF.md)。
原941、最小性、C3／C4／C5 pocket、全部stars、rotation與任意外側附件均保留。

本項固定profile0、K=1、唯一障礙Y位於H_L，以及同一份原完整target著色中的

```text
Y1–U0–V1–z4(0)，
Q5=(Y,U,V,z4,z5)，int_G(Q5)={原K}，
N_G(z5)=(L,u1,z4,K,Y)，d_G(z5)=5，
N_G(K)=(Y,U,V,z4,z5)，d_G(K)=5，φ(K)=2。
```

K與z5是原點，不是補入的中心。型II原非邊 `z5–U`、`z5–V` 亦保留。
Y與原cap點y不同；表中cap assignment仍用原y。

令P=(n,u4,u3,u2,u1,L)。共同可重色集合恰

```text
I=(n,u4,u3,u2,u1,L,z5,K)。
```

P的全部外鄰由原完整links給出；z5、K的完整stars如上。故I的全部向外
接觸恰經下面列出的固定原點，沒有漏掉任何原私有附件。固定同一原圖
`F=D−I` 的一份完整著色ψ，I的每份共同proper延伸與同一ψ真正接回D，
再對同一份當前D色列枚舉全部G／Q1／J1 cap lifts。沒有假定最初target
本身能接回G，也沒有分別重色兩個五度點後拼接。

## 2. U／V可能是哪些原tail點

原幾何給U、V不在S；U色0、V色1。因此U只能是新命名的原私有點，或
target的色0 tip z0；V原本只有私有點、c或色1 tip的可能。

原K2同時接Y1、V1，故在**同一原E**中給12路Y–K–V。父完整03|12欄已證：

```text
A44459：K12^E(Y) 的rim contacts={Y,t,w}；
B44466：K12^E(Y) 的rim contacts={Y,t}。
```

所以V≠c；B亦V≠v。必須完整分列的身份恰為：

| 原target | U原身份 | V原身份 |
| --- | --- | --- |
| A44459 | 私有U或原v | 私有V或原w |
| B44466 | 私有U或原w | 私有V |

共六個身份case。若是tail原點，就在圖和色列中真正識別同一原點，不能
當成另外一份可獨立染色的U／V。K是原Q5內點，不會被冒稱原tail點s／t；
那些tail點還有原cap附件，與此完整K star不相容。

## 3. 原相位的全部八點共同lifts：六份而非排除

對六個身份case分別固定原F字面色、U0、V1及其全部原附件。原外側字面walk
為

```text
(a,z1,z2,z3,z4,V,U,Y,q,c,s,v,w,t)
 (0, 3, 0, 3, 0,1,0,1,3,1,2,e0,e1,2)，
(e0,e1)=(0,1) 或 (1,0)。
```

每個case都恰有以下六份完整共同I-lifts；順序為P、z5、K：

```text
12121023
12121032
12121232
12123023
21212032
21213023
```

三個原cap的禁止列均沒有完整lift；這些D列亦都在原已證零閉包外。
[certificate.json.gz](certificate.json.gz)不只保數量：逐份保全部八點色、
完整D字面rim、所有左cap assignments、右cap assignments與三圖十列的
所有共同lift pairs，含空列；全部與原cap矩陣逐項相等。

## 4. 固定同一F partition後，才作完整分量動作

當U、V均為私有原點，剝掉原z5、K後，三角面patch把原E的
`z4–z5–Y`邊界弧改為`z4–V–U–Y`，剩下真正的simple C14 disk F。
固定上述同一字面row，三個split的palette transition數為10／10／8，
完整typed noncrossing partitions恰42／42／14。

枚舉採原active-block stack：同palette相鄰boundary點必同塊；只可回到
仍開放的同palette塊，或開新塊；三角disk的塊數滿足 `2(b−1)=transitions`。
這逐一涵蓋每個實際F分量partition，而不重建全C14 family。

**初始同來源接合gate。** 每個F partition先加回原z5=3、K=2及完整原邊，
以同一DSU精確合併後投影到原E十三框；所得必恰是父證書同target、同split
的4／2／1份完整E partitions之一。這是對**同一份初始著色**的接合，不是
從不同palettes各挑一個可行欄。

通過後，固定這個**原F partition**，逐一翻其boundary-touch完整components
的全部聯集。每次都攜帶全部原F私有點；其他boundary-free components留
原相位。在同一當前F完整著色上枚舉全部八點共同lifts。若其中某份D列已
由原完整D權威證零，便否定這個來源partition。若共同patch fibre為空，
只代表該份F著色無法延D，**不**據此把F fibre判零。

兩target得到相同的數字：

| split | 全部specific partitions | 加回原patch並匹配原E後 | 真全分量動作＋完整joint kernel後 |
| --- | ---: | ---: | ---: |
| 01|23 | 42 | 4 | 4 |
| 02|13 | 42 | 7 | 4 |
| 03|12 | 14 | 3 | 3 |

所有partition、每步完整字面F row及全部joint/cap fibres均存入證書。
4／4／3只是各split的必要殘餘，沒有證明它們能共同實現一張原F。

## 5. 有tail重合時不冒用simple C14；B的U=w直接排除

若U或V等於原tail點，上述walk出現重複原點，F可有cutvertex或多disk。
本項對這些case**不用**simple-disk的塊數等式或NC充分性。
先把相同原點及同palette原walk邊union，再枚舉各palette全體set partitions。
任意實際F的分量接觸一定屬於這個保守完整必要覆蓋；它也容許不少無法
平面實現的分割，所以不稱為完整multi-disk可實現family。

然後仍按第4節對同一partition作初始原E接合、真全分量動作及八點共同
延伸。存活數如下，括號內依次是01／02／03三split：

| 原identity | 接合與全動作後的必要型數 |
| --- | --- |
| A：U私有，V=w | (2,5,6) |
| A：U=v，V私有 | (2,8,3) |
| A：U=v，V=w | (2,2,2) |
| B：U=w，V私有 | (2,0,3) |

最後一案有一個不需任何新orbit枚舉的短證：原K2同時接U=w0、z4=0，
故同一原E中有02原路

```text
w0–K2–z4(0)。
```

但B原兩份完整02|13欄220297、220299，分別將w放在`{a,z2,w,t}`或
`{a,w,t}`，將z4放在`{z4,s}`或`{z2,z4,s}`；兩欄都迫w與z4不同完整02
分量。這與原路直接矛盾。因此**B、U=w的型II來源子案已排**。
A的U=v則與父02型所迫的v／z4連通相容，不能照搬這個排除。

## 6. 刪原K、加z5U／z5V：完整Q5關係確實不相等

這個變更在Q5內把原五輪改為型I fan，內點少一個。即使平面合法，也
必須保同一外側完整界面關係，不能從原target兩邊都有六份joint lifts
就宣稱它保持原Σ。

固定完整有序Q5界面 `(Y,U,V,z4,z5)`，全部十個proper canonical色列如下：

| Q5色列 | 原wheel可接K | 新fan可接 |
| --- | --- | --- |
| 01012 | 是 | 是 |
| 01021 | 是 | 否 |
| 01023 | 否 | 是 |
| 01201 | 是 | 否 |
| 01202 | 是 | 否 |
| 01203 | 否 | 是 |
| 01212 | 是 | 否 |
| 01213 | 否 | 是 |
| 01231 | 否 | 否 |
| 01232 | 否 | 否 |

原wheel恰接受5份三色列；fan恰接受4份，其中3份使用四個boundary色而無法
接原K。交集只有01012；兩個完整關係互不包含。
原相位六份joint lifts全落在這個交集，因此六份相同不提供全界面替換。

本項未證那些差異色列可由同一原F供應，亦未證它們在原F的完整fibres皆空。
所以這是通用縮減的精確障礙，不是條件替換已成功或原來源已實現。
若要援用最小性，仍須補這份同原F條件下的全支援接合，不能只保目前
target orbit或幾個必要partitions。

## 7. 證書、重播與停止點

正式[checker](check.py)核對6個原identity、6份初始joint lifts各自完整保留、
6,131份完整partition必要分案、2,101份字面joint kernels與3,132份完整cap
kernels。原E4／2／1的接合逐份使用同一初始F partition；全部動作保原
partition身份與字面row，沒有補滿中途觀測fibre。

normal／seed17加`-O`唯讀重播一致。漏joint lift、把原tail重合拆成simple14、
把空patch fibre冒稱F零、冒稱可刪K及冒稱整型II排除五項污染均拒絕；另
以外部整型排除污染證書驗證拒絕。frozen／live輸入漂移為零。

```text
python3 -B audits/2026-10-21-w7-L-path-30dde27/double_five/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-21-w7-L-path-30dde27/double_five/check.py
```

Closure scope：B中U=w的具名型II來源子案；完整有限joint／cap關係、特定
字面F的必要分量gate及Q5通用替換障礙。其他型II、整個L、原profile0／1、
長路≥5、一般W7／J1／J2、合法較小替換、strict smaller bad及主命題仍OPEN。
沒有新來源圖枚舉、LP、四色定理、matching或新Lean。
