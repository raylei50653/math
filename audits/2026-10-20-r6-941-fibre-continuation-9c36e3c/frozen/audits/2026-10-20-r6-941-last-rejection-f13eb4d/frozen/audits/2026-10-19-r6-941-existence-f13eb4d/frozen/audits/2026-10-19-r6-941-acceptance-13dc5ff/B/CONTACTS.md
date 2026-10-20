# B 補充：同一 induced C10 的私有點最多接四框點

固定本輪[完整來源](../../2026-10-19-r6-941-quotients-13dc5ff/SOURCE_CONTRACT.md)，
原核心 rim 是 `(a,n,R,L,q,c,s,v,w,t)`。本頁結合
[B 的原 n=5,a=6 排除](PROOF.md)與 [D 的原 c=5,q=6 排除](../D/PROOF.md)，
只提出任意大小真來源的必要接觸 envelope，不宣稱其每個子集可實現。

原 D10 的 core 度數下界依序是 `(3,3,4,4,3,3,4,4,4,4)`。
其中 c 的三度下界來自前輪新 c>=5，刪失原 b,x 兩點；其餘下界沿用
凍結短圈分類。取任一原 D10 私有內點 z，令 S 是它的**全部**十圈鄰點。

若 z 同時接框弧 u-v-w 的兩端，則原 C4 u-v-w-z 的 bounded pocket
位於 D10，v 的全部 core 鄰點困在其中。原 C4 內側空，而 u-w 是
induced rim 禁止的 chord，所以唯一填片有 z-v。於是 v∈S 且 v 的
core 度數恰三。故六個下界四的框點不能成為這種中點。

若 z 同時接長三框弧 v0-v1-v2-v3 的兩端，則原 C5
v0-v1-v2-v3-z 的 bounded pocket 也位於 D10。空填片因 induced rim
只能是 z 扇形，W5 例外的兩個中間框點也各只有三個 pocket 鄰點。
兩種完整情形均迫 v1,v2 core 度數三。因此除了 `t-a-n-R`、`L-q-c-s`
之外，八個長三弧立即被中間高下界排除。前一例又迫原 a=6,n=5，
由 B 排除；後一例迫原 q=6,c=5，由 D 排除。故**任一私有點都不能
同時接原十圈距離三的一對點**。原 G 兩側距離結論的外部 cap alias
排除另見本輪主 [PROOF](../PROOF.md)。

此外S不得同時含原a,c。直接證明是：若有私有z同接a,c，原C4
a-b-c-z必內側空；其無內點三角化要求ac或bz。ac為原非邊，而b的完整
鄰集只有a,c,p,q，z既非刪點p亦非rim點q，故bz也非邊，矛盾。
這也與既有原私有點至多接兩個相鄰原B點的結論相容。
以上全部規則同時施於同一 z 的完整 S；沒有把不同 z 或不同來源拼接。

[check_contacts.py](check_contacts.py) 窮盡全部 2^10 個完整子集，包含
空集合，將每個不合格者的完整違反規則保存於 [contacts.json](contacts.json)。
這是十個具名接點的局部窮盡，並非有界圖枚舉。60 個必要容許子集按
大小的數目為 1、10、24、20、5，沒有大小五或以上。故每個原私有
內點最多接四個 C10 點；四接觸時只可能是

```
{a,n,R,s}, {n,R,s,v}, {R,L,v,w}, {L,q,c,t}, {L,q,w,t}.
```

此為必要 envelope；未證這五型可實現，未排它們，未給來源圖或完整
新 count 控制。B/D 的分支證書及原來源輸入在 CONTACT_INPUTS.json
逐份 SHA 綁定；正常、seed17 重播及四負控制通過。

```bash
python3 -B audits/2026-10-19-r6-941-acceptance-13dc5ff/B/check_contacts.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-19-r6-941-acceptance-13dc5ff/B/check_contacts.py
```

舊 allK 向量沒有私有點與 rim 接觸圖，因此本頁對其為 not triggered，
不能據此宣稱已排除。沒有新較小 bad、k 下界、Lean 或主目標閉合。
