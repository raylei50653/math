# 941第二輪：最後出口落在完整B13，原01另迫K外橋點

2026-10-23；exclusive BASE `cb8f8593e273a7426ecadd59797a6e643cc4768e`。

**新增兩項同源限制，沒有排除任何初始配對。** 在普通短型I／初始02型13、36，
完整02|13分量的原鄰接圖是樹，原boundary邊固定唯一樹路
`K02(U)–B13(V,Y,q,c)–L02(z4)`。因此03型4在實際03路上「最後離開K0」
的私有色3點X，必屬完整B13；每個原色1鄰點亦在B。rootless13分枝不能作
這個最後出口，但完整保留，X的下一色0點也不必立即屬L。

原01四型與實際交換後的唯一12後繼另迫：一條最短原01 U→c路含原色0點T，
T在K外，其兩個路鄰色1點分屬後繼12的不同完整分量。若T私有，完整原link
至少有兩個色3鄰點；五度時恰為`{1,1,2,3,3}`且第五色2在K外；無色2的
偶數度至少六仍保留。所有色3鄰點經T接入同一實際後繼03分量。T碰框的
全部可能點則依原01四型明列，沒有證明它必私有。見[紙證](PROOF.md)。

這比前輪完整無邊／最後出口標記更強：現在要求同一個私有X確有原13路
連向V、Y、q、c，不能以獨立palette survivor或私有13分枝補空缺；T則把
原01與同一份真實delete/insert後的12分隔接到一條原路和完整link上。

[certificate](certificate.json)逐份保留四份target／02列的全部初始01 contacts、
03二選一、唯一後繼blocks、全域inverse、全部七點lift與原cap assignments；
完整上游二步證書含1,186份空七點fibre按bytes保管，沒有重寫上游枚舉。
[INPUTS](INPUTS.json)凍結13份數學authority，含前輪未提交的精確bytes／SHA；
HANDOFF及三份dirty routing docs共四份另外封存，只供路由背景，live drift不作數學失敗。

七個顯式三角化disk控制核完整原面／link、原分量鄰接樹及獨立零界面對偶，
並在同一圖上交換完整K後直接核六個palette的全部分量。兩種出口五度side、
兩種橋點色2的後繼12 side、原六度及rootless分枝均保留。另有缺三角化四圈
的具體反控制。這些局部控制的完整941來源前提均為 **not triggered**。
全稱條件引理由紙證承擔；局部有限通過不提供原圖實現、較小bad或來源排除。

```sh
python3 -B audits/2026-10-23-three-mask-round2-cb8f859/941/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-three-mask-round2-cb8f859/941/check.py --seed 17
```

正常／seed17、11項反控制、外部破壞證書拒絕及drift見
[verification](verification-v2.json)。只寫本941目錄；舊audit、既有dirty docs與其他
工作者檔案不改，未commit／push。

交叉審查將HANDOFF由數學輸入改列routing，精確entry bytes仍保存；證書內容不變，
新版receipt保留前版驗證記錄。

兩target各八配對、W7其餘兩profile、一般J1／J2仍OPEN。下一個窄義務是用
**同一B13的原私有路線與同一條Q的橋點**接合X／T及唯一後繼，保留boundary T、
五度兩側、至少六度與任意大小私有分量；本輪沒有再擴枚舉或LP。
