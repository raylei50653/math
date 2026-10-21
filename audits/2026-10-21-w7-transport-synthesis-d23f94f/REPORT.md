# W7 證明整理與逐型排除：24 型縮為兩個原面點問題

2026-10-21；BASE `d23f94f739468593db653ec03f903c30adfd5fb0`。
[BASE.json](BASE.json) 凍結14份既有權威／路由輸入，數學輸入均對回 BASE bytes。
這輪依使用者要求先整理證法，再分派 u3w、u1w 及其他十二型各自排除；
後續依補充要求，繼續保留原平面嵌入、完整度數與私有面點。

**已證：在完整原941／Q1接受零／J1 type III五邊路／嚴格 only-R-W7契約下，
本輪二十四份必要原接觸再排二十二份，只餘 profile0、profile1。**
這是具名來源分支排除；一般W7、J1／J2與較小bad仍OPEN。

## 1. 兩個 w 分支的完整證明

[共用證法](PROOF.md)把既有 u3v／u1v 的實際分量傳輸整理為兩條規則：
原邊同色使完整 fibre 為零；若某 half-row 的**全部原 incident columns**
各含一個已證零 fibre，則由同一來源的 `2Z=ΣX` 回推該 fibre 為零。
每次只作用同一 D 的完整分量，私有點與全部 cap lifts 都保留。

| 原邊分支 | 短證結構 | 完成排除 |
| --- | --- | --- |
| u3w | 四個推導態，29個完整 incident 分支；49643、60707先零，再49955，最後B44466 | 八型16,17,46,47,62,63,66,67；X66602=X67765=0 |
| u1w | 五個推導態，40個完整 incident 分支；44722、45945、65628先零，再45034，最後B44466 | 四型96,97,100,101；X48647=X67765=0 |

兩支的另一 target A44459 都直接在所假設原邊同色。因此兩 target 全零，
與原選定五邊路的 `Z44459+Z44466>0` 矛盾。

- [u3w完整紙證與來源覆蓋](../2026-10-21-w7-u3w-d23f94f/REPORT.md)
- [u1w完整紙證與字面操作](../2026-10-21-w7-u1w-d23f94f/REPORT.md)

兩個 w 分支都重新讀原307,197欄，沒有使用 v／w 圖對稱或其他已排邊零值。
例如 B 的完整12分量接觸是 `{c,s,v}`，會連帶改 v；不能直接套 A 的 `{c,s}`。

## 2. 同一引理排其餘十型

[其他十二型的逐原邊證明](../2026-10-21-w7-other-types-d23f94f/REPORT.md)
獨立處理 u4v、u3s、u2v、u2w。前三個有一至兩步共同輸出的字面短鏈；
u2w 使用完整分支零證書。每個單邊引理都在原未加可選弦的 family 上成立。

這四個引理在原 full15 十二型中覆蓋
`3,5,6,8,40,41,60,61,64,65`。覆蓋可重疊，這裡只計十個不同 profiles。
加上本輪 u3w八型與u1w四型，恰排目前24型中的22型；連同舊v分支，
原40份正witness必要覆蓋已有38型排除。

## 3. 獨立核對與完整殘餘

[short_check.py](short_check.py)不讀三位worker的checker實作，從原全部欄
重新核對[八個條件式短證](short-proofs.json)的每個原邊種子、完整incident清單、
欄內零見證及拓撲次序。漏欄、錯原邊、假零種子、錯half-row、bool欄號與
擴大來源範圍均拒絕。[SHORT_INPUTS.json](SHORT_INPUTS.json)釘住三份原短證書。

另一套[independent.py](independent.py)使用同步位元集合運算：完整欄取各態
存活交集、half-row取incident欄聯集、state取三個half-rows交集。
它同時獨立重算原40型與8條單邊，19輪穩定，確認只餘0、1型。
[完整48組state／column殘餘](independent-results.json.gz)保留全部IDs，
[RESIDUAL.json](RESIDUAL.json)保留兩型的完整原接觸、全部原弦與支持量。

| 原型 | 全部可選原弦 | 完整原度數區別 | 必要live states／columns |
| --- | --- | --- | ---: |
| 0 | 無 | d_G(n)≥6 | 61,308／307,197 |
| 1 | 僅au4 | d_G(n)=5 | 38,647／133,271 |

這些存活量不代表同一精確計數解，更不代表來源實現。不同正性條件可以
由同一原圖的不同完整著色供應；共同來源不要求所有正量同屬一份著色。

## 4. 原面點提供的下一層條件排除

[原第三面點、完整link與03分量](../2026-10-21-w7-private-face-points-d23f94f/REPORT.md)
專門處理使用者補充的原圖資訊。令 t=(n,u4,u3,u2,u1,L)，zi為路邊
`t(i−1)t(i)` 的原W7外側第三面點。

profile0的五個zi全是不同D私有點；profile1則z1=a，僅z2至z5私有。
每個zi對原C7的接觸恰為該邊兩端，在兩target完整著色中只能用0／3。
不能據此假設它們彼此相鄰或同分量；需逐項使用原rotation與完整link。

經原完整link可把「相鄰面點有邊」與五度條件接通；配合兩target實際
03分量中a、q分離，進一步證明，令 U={u4,u3,u2,u1,L}：

- profile1 必有某個 t∈U 滿足 d_G(t)≥6。
- profile0 必有 d_G(n)≥7，或某個 t∈U 滿足 d_G(t)≥6。

更精確地，每份實際target著色都在該外側完整link上有一個原D私有點y，
色為中心t的相反12色，且原接觸恰 `N_G(y)∩C7={t}`。不同著色的y可不同；
不把單C7接觸誤當全圖只有一個鄰點。

[共用證法第6節](PROOF.md#6-可直接使用最小性的完整關係替換引理)亦證明：
同一完整有序接合界面上的完整支援關係相等，配合法定plane接合與嚴格內點
下降，已足以保原Σ941並違反全域最小性；無需再要求計數相等。目前仍缺
具體合法替代與關係相等證書，兩個profile繼續OPEN。

## 5. 重播、證據層與路由

```
python3 -B audits/2026-10-21-w7-transport-synthesis-d23f94f/short_check.py --controls
python3 -B audits/2026-10-21-w7-transport-synthesis-d23f94f/independent.py --controls
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-21-w7-transport-synthesis-d23f94f/short_check.py --controls
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-21-w7-transport-synthesis-d23f94f/independent.py --controls
```

實際重播、負控制、frozen-input零漂移及文件檢查結果見
[verification.json](verification.json)。任意大小來源的orbit覆蓋與count恆等式
沿用原紙證；本輪有完整同源紙面推論與有限邊界證書，沒有新Lean。
四次獨立normal／seed17 optimized重播逐字相等，原14份快照與10份即時數學
輸入零漂移。正式文件與docs範圍DocGraph通過；全樹仍有72項既有封存
duplicate-ID診斷，沒有本輪新audit出現在錯誤中，與正式文件結果分開記錄。

Closure scope：u3w八型、u1w四型、其餘十型；原40型共38型排除。
Updated：本報告、共用證法、兩型殘餘、Kempe導覽與STATUS的直接來源索引。
Reviewed-unchanged：前輪凍結40／32／24型證據保留當時語境；一般J1兩項、
J2六項與State歷史語義不變，HANDOFF研究線標記及README不變。
Remaining OPEN：profiles0／1的較高度數來源、精確必要計數錐、來源實現、
一般W7／C7多內點／J1／J2、嚴格較小bad及主命題。
Propagation stop：L2；只關閉具名子分支，父W7仍OPEN。
目前接續由[Kempe導覽](../../docs/c5_kempe_guide.md)維護。
