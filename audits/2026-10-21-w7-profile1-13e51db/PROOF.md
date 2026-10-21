# profile 1 的 555 三角 patch：較小完整關係替換不存在

2026-10-21；exclusive BASE `13e51db3ec3d8d7ec7eeef60167afdc19ad956c4`。
本項承接原來源契約、原完整 p/h 五度 star 及 profile 1 的完整 n 五度 star；
三份原 authority 的原 bytes 在 frozen/ 封存；bytes、SHA256、Git BASE 與
原檔的一致性由 checker 逐次核對，見
[certificate.json](certificate.json)。不改原外框、原 rotation、附件或私有點。

**本項沒有排除 profile 1。** 它證明一條具體最小性捷徑不可行：把下面具名
三內點 patch 改成同一六點界面、至多兩內點的任一簡單 plane patch，不能
保持完整界面關係，甚至不能得到原關係的子集。這不排除較大界面、依賴同一
外側完整 fibre 的有條件縮減，或其他同源 Kempe 證明。

## 1. 原完整 star 給出一個完整六點接合界面

profile 1 的原 `a-u4` 邊迫
`N_G(n)=(a,p,h,R,u4)`。連同原 p、h 的完整五度 star，原 patch H 的界面為

```
S=(a,b,q,L,R,u4),
int(H)={p,h,n},
E(H)-E(S)=
  {ph,hn,np}
  ∪{pa,pb,pq}
  ∪{hq,hL,hR}
  ∪{nR,nu4,na}.
```

其十個原三角面是
`abp,bpq,pqh,phn,pna,hqL,hLR,hRn,nRu4,anu4`。
這些面沿原 rotation 接合成六邊 disk，沒有 placeholder 被當成面。
由三個**完整**五度 star，p/h/n 沒有任何遺漏的外側附件。因此 H 的全部內外
接觸確實經同一有序 S；原圖其餘部分 E 及所有未知私有點完整保留。
R 在本 patch 是界面點，不被誤當可刪除的內點。

固定字面 S 色列 σ，`Col_H(σ)` 計 p/h/n 的全部同時合法延伸，包含空 fibre。
31 份 normalized proper 六圈色列中，14 份非空、17 份為空；certificate
保留每列的**全部**完整 lifts。任何字面 proper 列可用同一個全域色置換唯一
正規化；不 proper 的列由原 S 圈邊直接為空。因此表完整涵蓋全部字面界面。

## 2. 完整關係相等的兩色短障礙

對 S 每一對非相鄰點，原 H 均有一份將該對染同色的完整合法 lift。
九份具名見證見 certificate 的 `nonedge_equal_witnesses`。因此任何與 H
完整關係相等的替換 H' 都不能增加 S 的弦；否則會刪去對應的非空 fibre。

考慮交替字面色列

```
(a,b,q,L,R,u4)=(0,1,0,1,0,1).
```

每個 p/h/n 都同時接色 0 與色 1 的界面點，所以只能使用 2、3；三點又互成
原三角形，故此列在 H 的完整 fibre 為空。

任何不增 S 弦、內點至多兩個的簡單替換圖，卻總能延伸這列：把一個內點染2，
另一個若存在則染3。它們與所有界面邊均合法，兩內點之間若有邊亦合法。
這甚至不使用平面性。故這一類替換不可能有 `R_S(H')=R_S(H)`。

以上是直接紙證；不是把局部色數、各點 marginal 或彼此不相容的 lifts 拼接。

## 3. 允許弦也沒有更弱的子集替換

完整關係相等比最小性可能需要的條件更強。若有若干較小候選，個別滿足
`R_S(H'_j)⊆R_S(H)`，再證某個候選保留所需原外框接受列，便可能用同一外側
E 得到較小 bad。所以上一節禁止弦的論證本身並未阻擋這種多候選路線。
本節另作完整、小範圍的替換分類：允許所有原界面對角弦。

先看三角化的簡單 S-disk H'，內點數至多二。全部 S 弦彼此不交叉，將六圈
分成 polygon cells；每個 cell 內沒有其他 S 弦，且總內點數至多二。
每個 cell 的可能填法恰如下。

1. 零內點：cell 必為三角形。
2. 一內點：唯一內點連到 cell 全部圈點，即完整輪。
3. 兩內點：兩點必相鄰。若不相鄰，每個三角面最多有一個內點；沿圈邊的
   第三面點如有變更，接續的三角面就必用兩內點間的邊或一條圈弦，矛盾。
   若始終不變，另一內點不能位於三角化 cell 內。既已相鄰，該內邊兩側的
   三角面第三點是兩個不同圈點 i,j。兩內點分別扇接 i–j 的兩條閉圈弧；
   再多一條圈弦與 cell 定義矛盾，再少一條 spoke 則留下未三角化面。
   這就是按任意不同 i,j 決定的完整雙輪；i,j 相鄰的三度內點情形亦保留。

所以按全部不交叉弦集合、全部 cell 內點分配及每個雙輪的全部 i,j 列出，
沒有遺漏任意大小外側 E 的任何這類局部替換。這只枚舉最多兩內點的小 patch，
不枚舉新來源圖，不截斷原 E。

checker 給出45份完整弦 dissection，以及：

| 替換內點數 | 全部三角化候選 | 完整關係為原關係子集 |
| ---: | ---: | ---: |
| 0 | 14 | 0 |
| 1 | 84 | 0 |
| 2 | 504 | 0 |

602個候選各自以同一31列核對全部內點著色。每個至少接受三份原 H 的空列。
certificate 逐候選保存全體邊、完整非空關係 bitmask、一份這種空列及其完整
候選 lift；checker 重新枚舉全表而不只查這一份反例。

若原候選尚未三角化，可在固定六圈內加入合法邊而不增內點，直至三角化。
增加邊只縮小關係。因此若原候選有子集關係，其三角化完成也會有子集關係，
與上表矛盾。這給出此同一 S、至多兩內點、簡單 plane disk 類別的完整
universal-subset 障礙。

## 4. 明確的剩餘缺口與重播

這個 negative result **不**把602個候選中的外側不相容反例冒稱真正原來源。
某個被排的通用替換，仍可能只在原 E 能產生的 S 列上成立；判斷這件事仍需
同一 E 的完整 fibres。也可能用更大界面，連 R 或原外側私有點一起縮減。
本項未構造這些候選，未證任何原 profile 1 來源矛盾。

profile 0／1、一般 W7、J1／J2、strict smaller bad 及主命題仍 OPEN。
941／全域最小來源的實現檢查為 **not triggered**；本項無 LP、無四色定理、
無 matching、無 Lean。

```
python3 -B audits/2026-10-21-w7-profile1-13e51db/check.py --controls
PYTHONHASHSEED=17 python3 -B audits/2026-10-21-w7-profile1-13e51db/check.py --controls
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-21-w7-profile1-13e51db/check.py --controls
```

重播涵蓋來源全 fibres、全部替換列、原 BASE bytes／SHA。破損控制分別改壞
原空列、漏一候選、污染完整候選 lift、冒稱子集候選及冒稱 profile1 已排除，
均須拒絕；控制不被宣稱為紙證的形式化。
