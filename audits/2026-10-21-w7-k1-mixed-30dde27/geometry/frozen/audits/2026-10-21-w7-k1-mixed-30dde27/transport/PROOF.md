# profile 0、K=1：u3／u1 兩個原位置的單分量短證

2026-10-21；exclusive BASE `30dde27293b5d3ad63c75fae73cda5be96db705b`。
[BASE.json](BASE.json) 保九份 authority 的 bytes／SHA；原正式數學輸入亦對回
Git BASE，前輪未提交的兩份局部審核另標 `prior-working-tree-audit`。
全部原 bytes 留在 `frozen/`；本項不改舊審核或共享路由。

**定理。** 承接原完整941、Q1接受零、J1 type III五邊路及 strict only-R/W7
合同，若完整原 profile 0 的全部 H 點恰一點，這一點不能位於 H2(u3) 或
H4(u1)。兩個 target 在這兩個條件來源上全部為零。K=1 的 L 位置未由本項
排除，但被迫 `K01(Y)=K01(a)`，特別連到原 a、n、c。

這裡 Y 是唯一 H 點，不是原外框 cap 點 y。原各點身份、完整 stars、
rotation、任意外側 E、私有點及全部空／非空 fibres 均保留。沒有構造替代
原圖、使用四色定理、matching、LP 或較小 bad。

## 1. 同一實際原 D 的來源量詞

固定

```text
D = G − {b,p,h,R,x,y,r},
rim(D) = (a,n,u4,u3,u2,u1,L,q,c,s,v,w,t),
P = (n,u4,u3,u2,u1,L),  φ(P)=121212,
A = 原完整外側 links 給出的 a–q 原弧。
```

使用[原來源契約](frozen/audits/2026-10-20-r6-941-j1-five-edge-417732f/SOURCE_CONTRACT.md)
及[原完整計數 family](frozen/audits/2026-10-20-r6-941-j1-five-edge-417732f/counting/PROOF.md)。
原 cap-zero 與完整非負 orbit 方程所得到的307,197欄 family 不另加可選弦
零值。每份實際完整 D 著色的 actual orbit 必在此完整必要 family 中。

兩 target 為

```text
A44459: (0,1,2,1,2,1,2,3,1,2,0,1,2),
B44466: (0,1,2,1,2,1,2,3,1,2,1,0,2)。
```

原 target 的完整03欄迫 a／q 分離。K=1 時 A 唯一 H 點 Y 因而必是反色12
障礙；否則 A 全03，直接連通 a／q。對中心u3或u1，Y色2，兩側03鄰點均色0。

以下證明對任一份這樣的實際 φ 開始。從來沒有選一份新 D 著色來供應
下一個動作，也沒有把下一個觀測 fibre 補滿。

## 2. 原完整01|23欄給出的四個互斥來源族

兩 target 的原01|23 half-row 分別是6712710、6712722。完整掃描原family，
各恰十個 incident columns；按完整 K01(a) 的 P 接點分類如下：

| 族 | K01(a)∩P | A44459 全部原欄 | B44466 全部原欄 | 完整 K23(u4) 的 rim contacts |
| --- | --- | --- | --- | --- |
| F0 | n | 43330,43331,43335,43336 | 43335,43336,43380,43381 | 此族不用 |
| F1 | n,u1 | 48617,48620 | 48620,48647 | u4,u2 |
| F2 | n,u3 | 66582,66584 | 66584,66602 | u4 |
| F3 | n,u3,u1 | 67755,67756 | 67756,67765 | u4 |

每一族的 K01(a) rim contacts 還必含 a、c，並可能同時多含 v、w。
兩 target 的欄 ID 與 v／w 身份均逐一保留，沒有援用圖的反射對稱。
完整每欄全部 component contacts、全部 half-rows 均存在證書中。

**原第三面點的 exact membership。** 每個 zi 接該原 P 路邊的兩個端點，
其色為0或3，而這兩端點分別色1、2。在01|23分割中恰有一個端點與 zi
同 palette；原邊直接迫它們在同一個**完整 D 分量**。所以一旦固定當前
原欄，其所有 zi 的實際分量完全由這個端點決定，不是可自由猜的標記。

Y 的 palette 為23。它的實際完整分量，或者是原欄的一個23 boundary block，
或者不碰 rim。這是完整互斥分類；後者亦可保留不翻，無需假造 boundary
contacts。選定原欄及 Y 的歸屬後，翻任一原完整 boundary component 對全 A
與原 rim 的作用因而完全確定。其所有未知 E 私有點也同步翻色。

## 3. 同一當前 E 上可以重色哪些 P 點

原 profile 0 的完整第二層定理給：六個 P 點的全部 D 外鄰都在 A 上，沒有
漏掉的私有附件；P 的原內邊恰五邊路。原外側 E 的有序界面是

```text
∂E = (A 從a到q, c,s,v,w,t)，本項長度恰13。
```

故對任一份實際完整 D 著色作真完整分量交換，得到同一 D 的完整著色 φ′。
固定它在**同一張 E 全部原點**上的限制 ψ′。此時 P 的全部合法重色，精確
是六個完整外鄰列表中的 proper 路著色。每份此種重色與 ψ′ 逐點相容，
可真正接回同一 D，不是在不同 E 或不同 σ 之間拼 witness。

接著對該份當前 D 著色重新枚舉全部原 G／Q1／J1 cap lifts。改 P 可能改變
cap assignment 的合法性，所以不固定最初的 cap；原 G 的全部七個被刪原
點均依原完整 stars 同時接回，這正是原 counting 合同所允許的量詞。

## 4. 四族逐一產生原 G 的禁止01021

下面均令 ε=2 當 Y 在所翻的 K23(u4) 中，否則 ε=3。Y若是原boundary-free
分量，當然屬第二種；沒有漏掉這個分類。

| 來源族 | 所翻的單一完整原分量 | Y 中心u3時重色P | Y 中心u1時重色P |
| --- | --- | --- | --- |
| F0 | K01(a) | (2,1,3,2,1,2) | (2,1,2,1,3,2) |
| F1 | K23(u4) | (3,1,ε,1,3,1) | (3,1,3,1,ε,1) |
| F2、F3 | K23(u4) | (3,1,ε,1,2,1) | (3,1,2,1,ε,1) |

這些 proper 路逐一符合交換後**同一份 ψ′**的完整外鄰列表。核對只須原
完整 stars 及第2節的 zi exact membership：F0 的 K01(a) 避開u3、u1，
故兩個候選 Y 中心的兩個03鄰點仍色0、Y仍色2，中心可改3；F1翻u4、u2
連帶的03面點，F2／F3只翻u4連帶的03面點。若Y同在該23分量，它亦2→3，
故其中心選2；若Y不在，它仍2，中心選3。表中的其他 P 點均可直接按完整
外鄰弧核對，沒有任意改 E 的點。

**F0 的完整 G lift：**

```text
(b,p,h,R)=(2,0,1,0),  (x,y,r)=(1,0,3)。
```

此時 a=1、c=0、q=3；P不用0，n=L=2，全部原cap邊 proper。原外框字面色
`(x,y,a,b,c)=(1,0,1,2,0)`，canonical row恰01021。

**F1／F2／F3 的完整 G lift：**

```text
(b,p,h,R)=(2,1,2,0),  (x,y,r)=(0,1,3)。
```

此時 a=0、c=1、q=3；P不用0，n=3、L=1，全部原cap邊 proper。原外框字面色
`(0,1,0,2,1)`亦為01021。v／w的兩種原target均已按其原身份核對。

兩類所得都是原**同一 G**的真正完整著色，與原已證 `N01021(G)=0` 矛盾。
F0–F3 覆蓋兩target的全部原 incident columns；Y所有可能分量歸屬亦全覆蓋。
所以這兩個原 K1 位置的兩target完整 fibres皆空，與所選原五邊路的
`Z44459+Z44466>0` 矛盾。兩個條件來源位置因而排除。

注意：初始問題是翻 Y 的缺側混色分量；完整分類的探索找出了更短的單分量
短證。F0不用先翻Y分量，F1–F3只須保留Y是否同在 K23(u4) 的真實分類。
這避免多餘的中途 fibre，卻保留同一份原始完整 witness。

## 5. L 位置的新強迫與這個方法的停止點

對 K1、中心L，Y色1，A順序為

```text
a0–z1(3)–z2(0)–z3(3)–z4(0)–z5(3)–Y1–q3。
```

同樣固定原01|23完整欄，逐一標記Y位於任一01 rim block，或boundary-free。
對每個標記分支，原欄的所有 boundary-touch完整components可以各自真交換；
不碰rim的其他原components一律不動。每個動作後固定同一當前E的完整ψ′，
枚舉六P點的全部共同lifts及全部原caps。

兩target各有25個觸框標記分支，其中15個導禁止cap；10個boundary-free
標記分支亦全導禁止cap。各恰10個剩餘分支，且全部恰是

\[
\boxed{K_{01}(Y)=K_{01}(a)\supseteq\{a,n,c\}.}
\]

這是條件來源上的必要連通，不是E來源實現。其原D contacts恰為
`{a,n,c}`加可選u3、u1及同時出現的v、w；每個原欄保留一種Y歸屬。

這還可嚴格降到同一原E中：在此01著色下，strip僅加三片pendant leaves
`n–a`、`u3–z2`、`u1–z4`，沒有連起兩個不同E01分量的通路。因此
`K01,E(Y)=K01,E(a)`且含c。Y的缺側01連通不能只靠P在strip內接合。

本項沒有再擴L的外側來源搜尋；父審核的另一份完整E證據可能施加更強
限制，本項的20個必要分支不宣稱都是最終存活來源。

## 6. 完整證書、重播與層級

[check.py](check.py)只使用已存在的原D完整family，不重跑來源圖枚舉：

- 完整掃307,197欄，恢復兩target各十欄及15個不同原欄的全部component
  partitions；逐一翻非anchor blocks重生各欄全部half-rows。
- 三個原位置、兩target、全部rim-block或boundary-free的Y歸屬，共250個
  互斥必要分支；每個固定同一原partition的全部 `2^b` 個完整動作。
- 保1,856份**字面E邊界**的完整strip kernels、5,208份**字面D rim**的完整
  cap kernels。每個cap kernel列全部左cap assignments、全部右assignments
  及三圖十列所有共同lift pairs，含空fibres，並與原cap矩陣逐項相等。
- 對u3／u1每份來源記錄上節固定的一個真完整分量、同E P lift及G01021
  full cap witness；證書亦保全部動作，以免只保存有利樣本。

不同字面E tuple沒有各自正規化後拼在一起；cap canonical ID只用於與原
矩陣比較，完整字面row與原全局色框仍保存在pool中。所有privatecomponents
保留；未翻的boundary-freecomponents以原相位留在同一完整witness內。

normal及seed17加`-O`唯讀重播一致。漏原column、拆開原facecomponent、破壞
full-cap witness及冒稱整個profile0排除的四項污染均拒絕；另作外部污染
證書拒絕。輸入frozen／live漂移為零。

```text
python3 -B audits/2026-10-21-w7-k1-mixed-30dde27/transport/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-21-w7-k1-mixed-30dde27/transport/check.py
```

Closure scope：原profile0、K1、中心u3／u1兩個具名來源子案；L的具名必要
連通與完整固定域校準。一般profile0／1、L來源排除、K≥2、一般W7／J1／J2、
strict smaller bad及主命題均未由本項關閉。沒有新Lean或原來源實現聲稱。
