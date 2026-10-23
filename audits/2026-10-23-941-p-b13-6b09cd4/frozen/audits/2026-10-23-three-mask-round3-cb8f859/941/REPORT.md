# 941第三輪：最後橋點定位、完整後繼禁邊

2026-10-23；BASE `cb8f8593e273a7426ecadd59797a6e643cc4768e`。

**新增同源限制，沒有排掉03／02配對。** 普通短型I的02型13／36，交換同一
完整K02(U)後，原邊固定完整分量樹路
`A03(a)–C12(U)–Q03(q)–D12(c)`，所以兩完整分量A、D之間沒有任何原邊，
包含它們所有未知私有點。此限制適用兩個初始03型。

在同一條最短原01 U→c路上，改取**最後離開C**的色0橋點T，可證T必屬
同一實際完整Q03(q)，且T與其全部原色2鄰點都在K外。這是新指定的最後點，
沒有把第二輪首次橋點改稱必在Q。T的boundary身分只剩原色0 tip：44459的v
或44466的w；a、z2、z4均不可能。四個原01型中，兩型不含tip，故可指定
最後橋點必私有。四份target／02列的16份完整01分支中，共8份必私有，另外
8份仍保留tip；這不是8項型別排除。
boundary T的鄰點義務只指原F內；T私有時才使用完整原G cyclic link。

再需初始03型4時，第二輪同一私有最後出口X∈B13(V,Y,q,c)∩A03(a)，而
本輪T∈Q03(q)。因此原XT非邊，X更與完整D12(c)無原邊；不能拿X充作T的
色3鄰點。同一完整B的任一原13 X→q路必經C，故存在原色1 R∈B∩C。
R可能V／Y，未識別成01路上T的鄰點；T所在原02分枝亦未識別成L。
完整量詞、原rotation／link與樹論證見[PROOF](PROOF.md)。

[certificate](certificate.json)逐份保留前輪四列完整記錄，含原03二型、原01
四型、完整七點lifts、全域inverse及全部原cap assignments；上游完整二步
證書包含1,186份空fibre，按bytes／SHA凍結，沒有重寫上游枚舉。[INPUTS](INPUTS.json)
共凍結18份數學authority，另存六份routing入口，兩者drift分開。所有rootless
分量、私有度5兩側及至少六度、boundary tip均保留。沒有新增有限生存控制、
來源disk枚舉或LP。

```sh
python3 -B audits/2026-10-23-three-mask-round3-cb8f859/941/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-three-mask-round3-cb8f859/941/check.py --seed 17
python3 -B audits/2026-10-23-three-mask-round3-cb8f859/941/check.py --negative
```

正常／seed17獨立程序一致，16項semantic反控制及外部破壞／缺欄證書均拒絕，
immutable drift為零；詳見[VERIFICATION](VERIFICATION.json)。有限checker驗的是
來源合同與必要身分表，任意大小的樹及最後離開證明由紙證承擔。沒有完整941
來源，來源控制為`not triggered`，不能當來源存在或來源排除。

兩target各八個原03／02配對仍OPEN；本項只適用02型13／36，型12／35未由
此關閉。03型9不能套X引理；V=w、型II、長路、profile1、K≥2、一般941／W7／
J1／J2、較小bad、Lean與matching均未升級。下一窄義務是同一B13的R與同一
原01路的r／s如何在原rotation相遇，以及T的原02分枝；不得丟掉tip及高階。
只寫本941目錄，未改前兩輪、shared docs或Git，未commit／push。
