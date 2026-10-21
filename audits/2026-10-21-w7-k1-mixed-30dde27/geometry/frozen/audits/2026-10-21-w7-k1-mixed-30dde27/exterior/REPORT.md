# Profile 0、K=1：原外側混色 orbit 排除 u3、u1，L 留38種必要接觸型

2026-10-21；exclusive BASE `30dde27293b5d3ad63c75fae73cda5be96db705b`。
[BASE.json](BASE.json)凍結八份輸入；六份原正式 authority 對回 Git BASE，
兩份前輪未提交紙證另記精確 bytes／SHA。
完整承接原941、Q1接受零、J1 type III、五邊路與 strict only-R/W7
[來源契約](frozen/audits/2026-10-20-r6-941-j1-five-edge-417732f/SOURCE_CONTRACT.md)。
原圖、ordered C5 frame、stars、rotation、全部附件、空 fibres 及 full lifts 均保留。

**本項新排除 profile 0 的 K=1、Y中心 u3 與 u1 兩個原來源分支。**
兩個原 target 各自完整排除，故沒有以不同來源拼出矛盾。
加上前輪已排 n、u4、u2，profile 0 的 K=1 六個位置只剩 L 未排。
此處只使用原 `N01021(G)=0` 就足夠；沒有援用原 D 已過濾的 orbit family，
沒有把其必要支持直接移到 E，也沒有較小 bad、LP 或四色定理。

L 的兩個 target 各有38個原 E 必要 partition 通過這個 mixed orbit；
它們不是實際來源，也不是多 palette 共同相容的見證。整個 profile 0／1、
其他 K 及多障礙均仍 OPEN。

## 1. 同一原 E 與六個固定字面輸入

原 P 與 D 為

```text
P=(n,u4,u3,u2,u1,L)，原色121212，
D=G−{b,p,h,R,x,y,r}，
rim(D)=(a,P,q,c,s,v,w,t)。
```

前輪[原外側拆分紙證](frozen/audits/2026-10-21-w7-single-barrier-30dde27/exterior/REPORT.md)
已證：D 由完整 P–A 原三角 strip 與同一實際 E 沿 A 接合；E 是原
triangulated disk。0型 K=1 時其有序外框恰13點：

```text
∂E=(A 由a到q, c,s,v,w,t)。
```

六個字面輸入依原點身份分開，沒有以反射或 v／w 任意互換合併。

| Y中心 | A原點順序 | A字面色 | 追蹤 split |
| --- | --- | --- | --- |
| u3 | `a,z1,z2,Y,z3,z4,z5,q` | `03020303` | `23|01` |
| u1 | `a,z1,z2,z3,z4,Y,z5,q` | `03030203` | `23|01` |
| L | `a,z1,z2,z3,z4,z5,Y,q` | `03030313` | `01|23` |

每列各接兩個原 target 的 `(c,s,v,w,t)=(1,2,0,1,2)` 或 `(1,2,1,0,2)`。
Y的名字在證書分別是原 `H2_0、H4_0、HL_0`。
u3／u1 的 Y 色2、其缺側03色為3，故追23；L的 Y色1、缺側03色為0，故追01。

## 2. E 的全部實際分量接觸必落在完整132型中

固定上述任一原完整 D 著色，限制成同一原 E 的**完整**著色 ψ。
取一個 split 的兩個 palette induced subgraphs 的全部實際分量；把每個
碰 ∂E 的分量記為一個 block。完全不碰 ∂E 的私有分量保留，並不刪去。

原 plane triangulated disk 的 boundary-component lemma 給出：

1. 所有 boundary contacts 共同形成 noncrossing partition；每塊只屬一個 palette。
2. 原邊若兩端同 palette，兩端必在同一塊；這些邊的實際連通不容獨立選擇。
3. 若碰邊界的分量共 b 個，沿邊界的 block transitions 恰為 `2(b−1)`。

本項六個字面輸入的 palette transitions 恰12，所以 b=7；每側 palette
各有六段 boundary runs。這裡用的是 E 的原三角 disk 前提，並非任意
noncrossing 模型都能實現原 E 的充分性。

[checker](check.py)直接對每個字面 palette membership 生成符合上述條件的
**全部** partition，各有132型。沒有讀取舊 D 的307,197個已過濾 columns。
另以獨立方法核 coverage：每側六段 runs 的全部集合分割有 Bell(6)=203種，
逐份檢查 `203²=41,209` 對分割的共同ABAB交叉及七塊條件，與前者的132型
逐項相等。這個完整有限覆蓋包含每一實際 E 的接觸型，容許額外非來源型。

## 3. 每個型都保全部128個完整分量作用及全部 P／cap fibres

固定實際 ψ 的七個 boundary components。任選其中若干**完整實際分量**
翻其 palette 兩色，兩側 palette 的動作互不相交且可交換，得到 `2^7=128`
個不同邊界字面色列。所有不碰 ∂E 的私有分量可保原色；選中的分量則連同
其全部 E 私有點一起翻。只儲存 boundary projection，不代表只翻這些接觸點。

對每個像字面色 η，固定這份由真實動作得到的**同一完整 E 著色** ψη。
原 P 中心 t 的完整列表為

```text
L_t={0,1,2,3} \ {η(z): z是t在A上的全部原鄰點}。
```

程式枚舉六個 P 點在這六份完整列表中的所有共同 proper 路延伸；它們與
同一 D 延伸 ψη 的完整 fibre 逐份雙射。每份延伸再逐份接原 G／Q1／J1 的
**全部**完整 cap assignments，保存十個原框 rows 的所有空／非空 fibres。
原完整 stars 與零列見[原 cap 契約](frozen/audits/2026-10-20-r6-941-j1-five-edge-417732f/counting/PROOF.md)。

3454個實際用到的 cap states 都由原邊直接枚舉完整 assignments，再與原
凍結66,430-state矩陣逐係數比對。證書的 cap fibres 以 canonical D tuple
儲存一次；每份 literal D tuple 決定同一全域色置換的逆，據此將完整 cap
所有點一起還原為原字面色。禁止見證另明列 literal cap 與 literal C5 框，
沒有讓不同片各自正規化後拼接。

若某個 E 像沒有 P 延伸，其 D fibre 是空，**不能**據此判 E fibre 為零。
本 kernel 保留這種空 fibre 的規則；本次六個像域恰好沒有觸發這種情形。

## 4. 同一原來源排除與 L 的精確停止點

假設有一份實際原 target ψ。其實際 E partition 必在132型中。對該型，
128個作用全部由同一 ψ 的完整分量產生；若其中一像的某份共同 P 延伸
及完整原 cap 得到禁止框列，便構成同一原圖的禁止完整著色，直接矛盾。
這個論證不要求最初的 target 本身可接回 G，也不將動作像補滿成目的整 fibre。

精確結果如下，兩 target 的數字各自相同：

| Y中心 | 完整必要型 | 通過全部128像的型 | 最少翻完整分量數的分布 |
| --- | ---: | ---: | --- |
| u3 | 132 | **0** | 121型單翻可矛盾；11型須至多雙翻 |
| u1 | 132 | **0** | 122型單翻可矛盾；10型須至多雙翻 |
| L | 132 | **38** | 75型單翻、11型雙翻、8型三翻可矛盾；38型未排 |

每個 case 的128像聯集有1848個不同 E 字面 tuple，其中可產生禁止 cap 的
數量分別為 u3的240、u1的176、L的128。所有禁止像都已可接成原 G 的
`01021` 完整著色；Q1／J1及另外兩個 G 零列沒有增加本項的排除。

因此 **K=1、profile0的u3／u1分支已排**。這是兩個真正原來源子分支，
不是把必要型「未實現」當作排除；coverage 與實際作用一起提供全稱矛盾。
原40個 profiles 的排38、餘2計數不變，因這是其中0型的更細分案。

L的38型完整保存於 `cases[*].surviving_partitions`。它們的Y之01 block
可碰a或c，沒有本項已證必為單一端點的結論；20種完整Y-block contacts中，
`{Y,c}`有7型，`{z4,Y,c}`有5型，`{Y,c,v,w}`有3型，其餘完整記於證書。
這些僅是原 E 的必要型，未通過其他 palette、原短圈幾何或共同 full fibres。
本項沒有把不同 palette 各自存活的 partition 拼成同一來源。

## 5. 證據、重播與負控制

```sh
python3 -B audits/2026-10-21-w7-k1-mixed-30dde27/exterior/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-21-w7-k1-mixed-30dde27/exterior/check.py --seed 17
```

[certificate.json.gz](certificate.json.gz)完整保存六個字面 case 的132 partitions、
每型全部128個 action image IDs、每個像全部共同 P lifts、3454個原 cap state 的
全部完整 assignments，以及 L38型。固定有限域可由 checker 正常重建及逐項核對。
seed17打亂像處理與列表色順序後輸出仍逐字相同。

五個負控制分別污染完整 coverage、整型排除、來源實現、偷用舊 D family、
以及把空 P fibre 當 E zero。外部另污染一份完整 action fibre 的像索引，
驗證器必拒絕。完整 receipt 與 frozen／live authority 零漂移見
[verification.json](verification.json)。

Evidence：原 disk 分量接觸全稱 lemma＋固定 literal family 完整有限證書＋
同一原 E 的完整分量作用／P fibre／原 cap 拼接。已排：profile0、K=1的
u3／u1兩細分支。OPEN：profile0、K=1的L分支，profile1、其他K與多障礙，
一般W7／J1／J2、原共同計數錐、來源實現、較小bad及主命題；沒有新Lean。
未改舊審核或共享文件，未 commit／push。
