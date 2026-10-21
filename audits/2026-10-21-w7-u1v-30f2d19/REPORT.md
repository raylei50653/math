# W7 原邊 u1v：同一字面 Kempe 鏈排除八型

2026-10-21；Git BASE `30f2d19275657393b7354ed75eca31439d8ee12b`。
承接既有未提交產物，先以 [BASE.json](BASE.json) 凍結83份輸入及原 dirty
狀態。前輪結構與u3v證據均保留原 bytes；本輪沒有LP、新原圖枚舉、Lean、
commit或push。

**完成：在既定941／J1嚴格 only-R／W7契約下，原邊u1v不可能存在。**
八個原接觸型 `68,69,78,79,88,89,92,93` 整支排除，且在該分支有

```
X48617=X67755=Z44459=Z44466=0。
```

前輪剩餘32型因此減為24型；一般W7及J1／J2仍OPEN。

## 1. 同一原來源與完整 fibres

完整承接[原來源契約](../2026-10-20-r6-941-j1-five-edge-417732f/SOURCE_CONTRACT.md)
與[完整同源計數／orbit覆蓋](../2026-10-20-r6-941-j1-five-edge-417732f/counting/PROOF.md)：
任意大小原plane C5 disk G、原框 `(x,y,a,b,c)`、941、全域最小內點數再
最大邊數、原stars／rotation／全部附件與私有點及短圈前提。固定Q1接受零的
J1 type III實際五邊路，且原induced C7內部恰只有R；僅此only-R子型使用W7。

原核心始終為

```
D=G-{b,p,h,R,x,y,r},
rim(D)=(a,n,u4,u3,u2,u1,L,q,c,s,v,w,t)。
```

每個Z是同一D的全部固定字面框完整著色數，包括不能接回G的著色與全部空
fibres。每個完整分量交換都攜帶所有原私有點；原G／Q1／J1的cap stars與
附件不動，各當前D fibre的全部cap lifts依原模型重新量化。作用不要求
某一份固定G cap assignment保持合法，也不維持選定路徑歷史的額外標籤。

本輪額外前提只有**同一原邊u1v存在**。八型的其他原弦各自保留；沒有
跨型拼接原圖、私有顏色、cap見證或可行片段。

## 2. 兩輪原分量作用與同色終點

[完整紙證](transport/PROOF.md)重新核對三份原字面tuple：

| 名稱 | ID | 原有序rim字面色框 |
| --- | ---: | --- |
| A | 44459 | `(0,1,2,1,2,1,2,3,1,2,0,1,2)` |
| M | 44111 | `(0,1,2,1,2,1,2,0,2,1,3,1,2)` |
| F | 44127 | `(0,1,2,1,2,1,2,0,2,3,1,3,2)` |

對任意A完整著色，原完整family迫實際 `K03(q)` 的rim接觸恰為 `{q,v}`，
實際 `K12(c)` 的接觸恰為 `{c,s}`。交換兩個完整分量得到M。互補palettes
相互不交，各自induced graph與分量vertex sets不變，兩作用交換次序且可逆。

在這份M完整著色上重新分類，全部五種原可能型都迫實際 `K13(v)` 的rim
接觸恰為 `{s,v,w}`。交換整個分量得到F，作用亦可逆。因此

```
Col_D(A) ↪ Col_D(M) ↪ Col_D(F)，
0 ≤ Z44459 ≤ Z44111 ≤ Z44127。
```

兩輪都保持u1色1，終點v也為1。原實際邊u1v遂給 `Col_D(F)=∅`，所以

```
Z44459 ≤ Z44111 ≤ Z44127 = 0。
```

等價的直接矛盾是：M中u1、v色為1、3，原u1v迫它們同在13分量；而
完整來源分類迫 `K13(v)` 不含u1。沒有在boundary上單獨翻點或改用另一張圖。

## 3. 分量 forcing 的唯一數值 family 是原307,197欄

原 `orbits.json.gz` SHA256為
`542ee11de93a846bfbc321b098214b153c5b600318ba2e0bc5621a73ad2a55ad`，
即新增可選原弦零值以前的完整family。其已證原零fibres及orbit覆蓋量詞
適用於全部D完整著色；中途M亦是同一D的完整著色。

- A的03|12 half-row `12302027` 只屬於欄 `306985`，故首輪兩個實際
  components的完整boundary contacts確定；它含M的half-row `12301211`。
- M的02|13 half-row `10064313` 的完整support恰為
  `147448,147449,167802,226130,231666`。全部五欄都有同一完整13分量
  `{s,v,w}`，且包含F的同一half-row `10064365`。

所以本輪可直接使用這條**字面作用本身**。它保持u1與u3色1，並令v最後
變1；不需要u1／u3或v／w的任何頂點自同構、旋轉反射或位置對稱。
forcing不使用前輪u3v新增零值或已裁切closure；本輪X67755也由u1v條件下
的新 `ZA=0` 重新推出，不把前輪條件化零值當作全域零值。

[transport checker](transport/check.py)逐欄重建全部六欄components與cosets，
核對完整incidence及原字面正反作用。[三態支配證書](closure/certificate.json)
另由[精確validator](closure/compact.py)從原完整family核對兩個完整column
support的包含關係，以原式 `2Z=ΣX` 推出同一支配鏈。它拒絕漏欄、錯state、
假同色種子、換成u3v前提、bool欄號、缺型及擴大來源範圍。

證據層是完整來源紙面作用加精確有限邊界分類，沒有新Lean。所有private
component重數仍在原X；沒有把獨立可行的分量型拼成一份著色。

## 4. 兩個X、另一target與八型排除

原欄48617與67755都含A的01|23 half-row `6712710`。該原非負同源方程
與 `ZA=0` 立即迫

```
X48617=X67755=0。
```

44466在u1、v上本來都為1，故實際u1v亦給 `Z44466=0`。原選定完整五邊路
著色卻要求 `Z44459+Z44466>0`，矛盾。八個完整profiles都含共同原u1v，
其餘原弦只留在同一圖上，不需另選來源。因此同契約下可採納原非邊u1v。

[原邊與覆蓋接合](closure/SOURCE_BRIDGE.md)逐份保留八型完整原接觸與弦，
並核對u1v同色種子的量詞涵蓋全部fibres。它也核對本輪刪去的八型與前輪
u3v八型互不重複。[獨立審查](review/PROOF.md)直接從原family重建forcing
及分量作用；數值輸入不包含前輪u3v證據或任何新增edge filter。

## 5. 驗證、完整殘餘與父題邊界

實際normal／seed17 optimized重播、負控制、凍結輸入零漂移及文件檢查見
[verification.json](verification.json)。只讀重播入口：

```
python3 -B audits/2026-10-21-w7-u1v-30f2d19/transport/check.py
python3 -B audits/2026-10-21-w7-u1v-30f2d19/closure/compact.py --controls
python3 -B audits/2026-10-21-w7-u1v-30f2d19/closure/source_bridge.py
python3 -B audits/2026-10-21-w7-u1v-30f2d19/review/check.py
```

四組checker共8次normal／seed17 optimized重播與負控制通過；81份來源／
前輪證據輸入零漂移。正式文件及docs範圍DocGraph通過；全樹仍是72項既有
frozen／scratch重複ID，沒有本輪新audit錯誤，詳[診斷](docgraph-whole-tree.json)。

Closure scope：原941／J1嚴格only-R／W7且有原u1v之全部八型；同圖完整
fibres上的兩X與兩target全零。沒有構造縮減圖、較小bad或新Lean定理。

父W7必要接觸 `32→24`：其餘12份B-joined二欄型與12份全15欄型仍OPEN。
A可用profile `20→12`，B的24份不變；[RESIDUAL.json](RESIDUAL.json)保存
剩餘24型的完整原接觸、原弦與既有target column IDs。這只是必要覆蓋，
未重跑其他型的計數或斷言來源存在。一般W7、一般C7多內點、type I／
更長路、一般J1／J2、未加可選原弦的既有必要錐可行性及主命題仍OPEN。

Updated：Kempe導覽與STATUS採納具名八型closure及24型停止點。
Reviewed-unchanged：凍結的前輪40型／32型報告保留當時語境；State導覽的
完整來源／歷史殘餘及一般J1 OPEN不變；HANDOFF／README研究線不變。
Propagation stop：L2，只有此具名分支關閉，沒有父W7 closure可再上推。
目前接續由 [Kempe導覽](../../docs/c5_kempe_guide.md)維護。
